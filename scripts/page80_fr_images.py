#!/usr/bin/env python3
"""Prepare page 80 French images: duomi for EN overlay/diagrams, compress-only otherwise."""

from __future__ import annotations

import json
import subprocess
import time
import unicodedata
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageChops, ImageStat

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "output" / "duomi"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (compatible; XindunFrenchBot/1.0)"
PAGE_NUM = 80

PROMPT_BASE = (
    "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. "
    "Only translate English marketing/diagram overlay text to French. "
    "Do NOT change product casing text, logos, model numbers, certificates, "
    "Chinese exhibition signs, or wall company names "
    "(Xindun / Xindun GREEN POWER / XINDUN POWER)."
)

# Overlay/diagram English:
# a0i0 marketing labels "Power inverter" / "Inverter generator" under product groups.
# a1i0 bottom caption "Various types of residential solar inverters".
# a2i0 waveform labels DC / AC next to black inverter.
# a4i0 UPS circuit-diagram English labels.
# Compress-only: a3i0 RV/truck car inverter product photo (casing labels kept).
DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "Translate only the two English overlay captions under the products to French: "
        "'Power inverter' → 'Onduleur de puissance'; "
        "'Inverter generator' → 'Générateur-onduleur'. "
        "Keep the colorful 'VS' graphic, the three yellow/white inverters on the left, "
        "the three white inverter-generator cabinets on the right, the gray/blue split "
        "background, and overall layout unchanged. "
        "Do not redesign. Do not change product casing, logos, LCD screens, or wheels."
    ),
    (1, 0): (
        "Translate only the bottom English marketing caption to French: "
        "'Various types of residential solar inverters' → "
        "'Divers types d’onduleurs solaires résidentiels'. "
        "Keep the city skyline, green ground band, and every product photo unchanged, "
        "including the white/black/blue/yellow inverters and the casing text "
        "'STORAGE Power Inverter'. Do not change logos, LCD screens, or model labels. "
        "Do not redesign."
    ),
    (2, 0): (
        "Translate only the English waveform labels to French: 'DC' → 'CC'; 'AC' → 'CA'. "
        "Keep the white background, black axes and arrows, red DC flat line, green AC sine wave, "
        "and the black inverter product on the right unchanged. "
        "Do not change product casing, LCD, vents, or logos. Do not redesign."
    ),
    (4, 0): (
        "Translate only the English schematic overlay labels to French: "
        "'Non Inverting Input' → 'Entrée non inverseuse'; "
        "'Inverting Input' → 'Entrée inverseuse'; "
        "'Output' → 'Sortie'. Keep 'ESD', 'Vcc', 'VEE', 'Cc', μA current values, "
        "circuit symbols, transistors, resistors, capacitors, and schematic layout unchanged. "
        "Do not redesign. Do not add extra labels."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/upload/2020-09/24/vs.jpg",
            "alt_fr": "Onduleur de puissance vs générateur-onduleur",
            "title_fr": "Onduleur de puissance vs générateur-onduleur",
        }
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/upload/2020-09/23/Varioustypesofresidentialsolarinverters.jpg",
            "alt_fr": "Divers types d’onduleurs solaires résidentiels",
            "title_fr": "Divers types d’onduleurs solaires résidentiels",
        }
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/upload/2020-09/19/dctoacinverter.jpg",
            "alt_fr": "Comment les onduleurs de 12 V convertissent-ils le courant continu en courant alternatif ?",
            "title_fr": "Comment les onduleurs de 12 V convertissent-ils le courant continu en courant alternatif ?",
        }
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/upload/2020-09/18/carinverterpowersupply.jpg",
            "alt_fr": "Utilisation du chargeur-onduleur automobile pour camping-car / camion",
            "title_fr": "Utilisation du chargeur-onduleur automobile pour camping-car / camion",
        }
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/upload/2020-09/17/upsyuanlitu.jpg",
            "alt_fr": "Principe de fonctionnement de l’alimentation sans interruption de secours",
            "title_fr": "Principe de fonctionnement de l’alimentation sans interruption de secours",
        }
    ],
]

IMAGE_LOG: list[dict] = []
USED_FILE_STEMS: set[str] = set()


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    import re

    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:90] or "image"


def unique_stem(base: str) -> str:
    stem = base
    n = 2
    while stem in USED_FILE_STEMS:
        stem = f"{base}-{n}"
        n += 1
    USED_FILE_STEMS.add(stem)
    return stem


def size_for(w: int, h: int) -> str:
    ratio = w / h if h else 1.0
    candidates = {
        "1:1": 1.0,
        "3:2": 1.5,
        "2:3": 2 / 3,
        "16:9": 16 / 9,
        "9:16": 9 / 16,
        "4:3": 4 / 3,
        "3:4": 3 / 4,
        "21:9": 21 / 9,
        "2:1": 2.0,
    }
    return min(candidates.items(), key=lambda kv: abs(kv[1] - ratio))[0]


def encode_jpeg(src: Path, dest: Path, tw: int, th: int, max_kb: int = 100) -> None:
    with Image.open(src) as im:
        img = im.convert("RGB")
    if img.size != (tw, th):
        img = img.resize((tw, th), Image.Resampling.LANCZOS)
    for quality in [92, 88, 84, 80, 74, 68, 62, 56, 50, 44, 38, 32, 28, 24, 20, 16, 12, 10]:
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
        data = buf.getvalue()
        if len(data) <= max_kb * 1024:
            dest.write_bytes(data)
            return
    raise RuntimeError(f"cannot keep {dest.name} <= {max_kb}KB without changing dimensions")


def image_mean_diff(orig: Path, candidate: Path, tw: int, th: int) -> float:
    with Image.open(orig) as im1, Image.open(candidate) as im2:
        a = im1.convert("RGB").resize((tw, th), Image.Resampling.BICUBIC)
        b = im2.convert("RGB").resize((tw, th), Image.Resampling.BICUBIC)
    diff = ImageChops.difference(a, b)
    mean_rgb = ImageStat.Stat(diff).mean
    return float(sum(mean_rgb) / len(mean_rgb))


def compress_only(local: Path, stem: str, orig_wh: tuple[int, int]) -> Path:
    dest = OUT / f"{stem}.jpg"
    encode_jpeg(local, dest, orig_wh[0], orig_wh[1], 100)
    return dest


def run_duomi(
    image_url: str,
    extra_prompt: str,
    stem: str,
    size: str,
    orig_wh: tuple[int, int],
    orig_path: Path,
    attempts: int = 2,
) -> Path | None:
    prompt = f"{PROMPT_BASE} {extra_prompt}"
    final = OUT / f"{stem}.jpg"
    timeouts = [180, 600]
    for attempt in range(attempts):
        out_name = f"{stem}-try{attempt + 1}"
        timeout = str(timeouts[min(attempt, len(timeouts) - 1)])
        print(f"[duomi] {stem} attempt={attempt + 1} size={size} timeout={timeout}", flush=True)
        cmd = [
            "python3",
            str(REPO / "scripts" / "duomi_image.py"),
            "--image-url",
            image_url,
            "--prompt",
            prompt,
            "--size",
            size,
            "--output-name",
            out_name,
            "--max-kb",
            "0",
            "--print-json",
            "--timeout",
            timeout,
        ]
        p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
        combined_err = (p.stderr or "") + "\n" + (p.stdout or "")
        if "余额不足" in combined_err or "没有权限" in combined_err:
            print(f"[duomi] API no balance/permission: {combined_err[-300:]}", flush=True)
            return None
        files: list[str] = []
        for line in (p.stdout or "").splitlines()[::-1]:
            line = line.strip()
            if line.startswith("{"):
                try:
                    files = json.loads(line).get("files") or []
                    break
                except Exception:  # noqa: BLE001
                    pass
            if line.startswith("SUCCESS:"):
                files = [line.split("SUCCESS:", 1)[1].strip()]
                break
        if not files:
            print(f"[duomi] no files stderr={(p.stderr or '')[-400:]}", flush=True)
            time.sleep(3)
            continue

        raw = Path(files[0])
        if not raw.exists():
            print(f"[duomi] output missing: {raw}", flush=True)
            time.sleep(3)
            continue

        try:
            with Image.open(raw) as chk:
                cw, ch = chk.size
            ratio_delta = abs((cw / ch) - (orig_wh[0] / orig_wh[1]))
            if ratio_delta > 0.18:
                print(f"[duomi] reject ratio {cw}x{ch} vs {orig_wh} delta={ratio_delta:.3f}", flush=True)
                time.sleep(3)
                continue

            diff_score = image_mean_diff(orig_path, raw, orig_wh[0], orig_wh[1])
            if diff_score > 42.0:
                print(f"[duomi] reject redesign diff={diff_score:.2f}", flush=True)
                time.sleep(3)
                continue

            encode_jpeg(raw, final, orig_wh[0], orig_wh[1], 100)
        except Exception as exc:  # noqa: BLE001
            print(f"[duomi] layout/compress failed: {exc}", flush=True)
            time.sleep(3)
            continue

        if final.exists() and final.stat().st_size > 0:
            return final
    return None


def prepare_all() -> list[list[dict]]:
    prepared_all: list[list[dict]] = []
    for article_idx, images in enumerate(IMAGE_SOURCES):
        prepared: list[dict] = []
        for img_idx, im in enumerate(images):
            stem = unique_stem(slugify(im["alt_fr"]))
            ext = Path(im["src"]).suffix.lower() or ".jpg"
            if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
                ext = ".jpg"
            local = OUT / f"_src_a{article_idx}_i{img_idx}{ext}"
            if not local.exists() or local.stat().st_size == 0:
                rr = requests.get(im["src"], timeout=60, headers={"User-Agent": UA})
                rr.raise_for_status()
                local.write_bytes(rr.content)
            with Image.open(local) as pil:
                orig_wh = pil.size

            tagged = OUT / f"{stem}.jpg"
            need_duomi = (article_idx, img_idx) in DUOMI_MAP
            method = "duomi" if need_duomi else "compress"
            duomi_path = None
            if (
                not need_duomi
                and tagged.exists()
                and tagged.stat().st_size > 0
                and tagged.stat().st_size <= 100 * 1024
            ):
                with Image.open(tagged) as chk:
                    tagged_ok = chk.size == orig_wh
                if tagged_ok:
                    method = "compress-reuse"
                    final = tagged
                else:
                    tagged_ok = False
            else:
                tagged_ok = False
            if method == "compress-reuse":
                pass
            elif (
                need_duomi
                and tagged.exists()
                and tagged.stat().st_size > 0
                and tagged.stat().st_size <= 100 * 1024
            ):
                with Image.open(tagged) as chk:
                    tagged_ok = chk.size == orig_wh
                if tagged_ok:
                    method = "duomi-reuse"
                    final = tagged
                    duomi_path = str(tagged)
                else:
                    size = size_for(*orig_wh)
                    result = run_duomi(
                        im["src"],
                        DUOMI_MAP[(article_idx, img_idx)],
                        stem,
                        size,
                        orig_wh,
                        local,
                    )
                    if result is None:
                        print(
                            f"[duomi] fallback original compress for a{article_idx}_i{img_idx}",
                            flush=True,
                        )
                        final = compress_only(local, stem, orig_wh)
                        method = "duomi-fallback-original"
                    else:
                        final = result
                        duomi_path = str(result)
            elif need_duomi:
                size = size_for(*orig_wh)
                result = run_duomi(
                    im["src"],
                    DUOMI_MAP[(article_idx, img_idx)],
                    stem,
                    size,
                    orig_wh,
                    local,
                )
                if result is None:
                    print(
                        f"[duomi] fallback original compress for a{article_idx}_i{img_idx}",
                        flush=True,
                    )
                    final = compress_only(local, stem, orig_wh)
                    method = "duomi-fallback-original"
                else:
                    final = result
                    duomi_path = str(result)
            else:
                final = compress_only(local, stem, orig_wh)

            if final.stat().st_size > 100 * 1024:
                raise RuntimeError(f"image exceeds 100KB: {final}")
            with Image.open(final) as chk:
                if chk.size != orig_wh:
                    raise RuntimeError(f"image dimensions changed for {final}: {chk.size} vs {orig_wh}")

            entry = {
                "local": final,
                "alt_fr": im["alt_fr"],
                "title_fr": im["title_fr"],
                "src_orig": im["src"],
                "method": method,
                "duomi_path": duomi_path,
                "orig_wh": orig_wh,
            }
            IMAGE_LOG.append(
                {
                    "article": article_idx,
                    "img": img_idx,
                    **{k: (str(v) if k == "local" else v) for k, v in entry.items()},
                }
            )
            prepared.append(entry)
            print(
                f"[img] a{article_idx}_i{img_idx} method={method} -> {final.name} "
                f"{final.stat().st_size}b {orig_wh}",
                flush=True,
            )
        prepared_all.append(prepared)
    Path(f"/tmp/page{PAGE_NUM}_fr_image_log.json").write_text(
        json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return prepared_all


if __name__ == "__main__":
    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
