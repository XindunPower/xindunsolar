#!/usr/bin/env python3
"""Prepare page 1 Russian images.

Duomi gpt-image-2 only for English marketing/diagram overlays.
Factory, certificate, and plain product photos are compressed and renamed only.
"""

from __future__ import annotations

import json
import re
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
UA = "Mozilla/5.0 (compatible; XindunRussianBot/1.0)"
PAGE_NUM = 1

PROMPT_BASE = (
    "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. "
    "Only translate English marketing/diagram overlay text to Russian. "
    "Do NOT change product casing text, logos, model numbers, certificates, "
    "Chinese exhibition signs, or wall company names "
    "(Xindun / Xindun GREEN POWER / XINDUN POWER)."
)

# Marketing/diagram overlays only. Product studio shots and install photos are compress-only.
DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a night-and-day marketing banner: stormy house and solar array on the left, "
        "a large golden question mark in the center, three white inverter/battery units on the right. "
        "Translate only the large headline overlay to Russian: "
        "'Is Battery Necessary for Inverter?' → 'Нужен ли аккумулятор для инвертора?'. "
        "Keep the question mark graphic, products, solar panels, house, lightning, and split background. "
        "Do NOT change text printed on the product casings (including HYBRID SOLAR INVERTER and LifePO4 Lithium Battery), "
        "the xindun logo, CE marks, or model markings. Do not add or remove objects. Do not redesign the poster."
    ),
    (1, 0): (
        "This is a daylight marketing banner of six white inverter units in front of a house with rooftop solar panels. "
        "Translate only the headline overlay to Russian, keeping the two-line layout and the green 3kW 24V emphasis: "
        "'What Can a 3kW 24V Off Grid Hybrid Solar Inverter Run?' → "
        "'Что может питать автономный гибридный солнечный инвертор 3 кВт 24 В?'. "
        "Keep every inverter, the house, panels, sky, and ground unchanged. "
        "Do NOT change product casing text, the xindun logo, or model markings. Do not redesign."
    ),
    (2, 0): (
        "This is an infographic with a central white inverter, a left blue panel and a right orange panel, "
        "plus four photos along the bottom. Translate only these English overlay labels to Russian: "
        "'Can Off Grid Inverter Power Appliances Directly?' → 'Может ли автономный инвертор питать приборы напрямую?'; "
        "'WITH BATTERY' → 'С АККУМУЛЯТОРОМ'; "
        "'DIRECT SOLAR POWER' → 'ПРЯМОЕ СОЛНЦЕ'; "
        "'STABLE POWER' → 'СТАБИЛЬНОЕ ПИТАНИЕ'; "
        "'24/7 RELIABILITY' → 'НАДЁЖНОСТЬ 24/7'; "
        "'LOWER COST' → 'НИЖЕ ЗАТРАТЫ'; "
        "'SIMPLE & EFFICIENT' → 'ПРОСТО И ЭФФЕКТИВНО'; "
        "'HOME' → 'ДОМ'; "
        "'REMOTE AREAS' → 'ОТДАЛЁННЫЕ РАЙОНЫ'; "
        "'TELECOM' → 'СВЯЗЬ'; "
        "'RV & OUTDOOR' → 'АВТОДОМ И УЛИЦА'. "
        "Keep the inverter, diagrams, arrows, icons, house, cabin, telecom site, and RV photos unchanged. "
        "Do NOT change product casing text or the xindun logo. Do not add or remove icons. Do not redesign."
    ),
    (3, 0): (
        "This is a marketing comparison banner: two white inverters, a red question mark, "
        "a brown left ground and a green right ground. Translate only the English overlay text to Russian: "
        "'Can an Inverter Be Too Big' → 'Может ли инвертор быть слишком мощным'; "
        "'and How to Choose the Right Size?' → 'и как выбрать подходящую мощность?'; "
        "'Is Bigger Always Better?' → 'Больше — всегда лучше?'; "
        "'High Costs' → 'Высокие затраты'; "
        "'Energy Waste' → 'Потери энергии'; "
        "'Overheating Risk' → 'Риск перегрева'; "
        "'Match Your Load' → 'Подберите нагрузку'; "
        "'Proper Power Source' → 'Верный источник'; "
        "'Efficient & Safe' → 'Эффективно и безопасно'. "
        "Keep both inverters, solar roofs, sky, question mark, icons, and the brown/green split unchanged. "
        "Do NOT change product casing text or the xindun logo. Do not redesign."
    ),
    (4, 0): (
        "This is a diagram banner: solar panels on grass at left, a green 80%-90% block, a red 100% block, "
        "and a white inverter at right. Translate only the English overlay text to Russian: "
        "'How to Match PV Power' → 'Как согласовать мощность PV'; "
        "'with Inverter Max PV Input Power?' → 'с макс. входной мощностью PV инвертора?'; "
        "'MAX PV INPUT POWER' → 'МАКС. ВХОДНАЯ МОЩНОСТЬ PV'; "
        "'Optimal Zone' → 'Оптимальная зона'; "
        "'Risk Zone' → 'Зона риска'. "
        "Keep the figures 80%-90% and 100%, the check mark, warning icons, dashed divider, panels, grass, and inverter unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER), the xindun logo, or CE marks. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/30/202601301651044545.jpg",
            "alt_ru": "Нужен ли аккумулятор для инвертора",
            "title_ru": "Нужен ли аккумулятор для инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ru": "Гибридный инвертор HFP",
            "title_ru": "Гибридный инвертор HFP",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ru": "Солнечный инвертор HFP-C RGB",
            "title_ru": "Солнечный инвертор HFP-C RGB",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ru": "Гибридный инвертор HFP-E с аккумулятором",
            "title_ru": "Гибридный инвертор HFP-E с аккумулятором",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg",
            "alt_ru": "Аккумулятор HP PLUS+ для инвертора",
            "title_ru": "Аккумулятор HP PLUS+ для инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg",
            "alt_ru": "Параллельный гибридный инвертор HU",
            "title_ru": "Параллельный гибридный инвертор HU",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/28/202604281725459553.jpg",
            "alt_ru": "Автономный гибридный инвертор 3 кВт 24 В",
            "title_ru": "Автономный гибридный инвертор 3 кВт 24 В",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/28/202604281727364190.jpg",
            "alt_ru": "Пример установки автономного инвертора 24 В",
            "title_ru": "Пример установки автономного инвертора 24 В",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/28/202604281728509031.jpg",
            "alt_ru": "Гибридный инвертор HFP 3,3 кВт",
            "title_ru": "Гибридный инвертор HFP 3,3 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/28/202604281729414139.jpg",
            "alt_ru": "Автономный инвертор HFP-S 24 В",
            "title_ru": "Автономный инвертор HFP-S 24 В",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/28/202604281730393966.jpg",
            "alt_ru": "Инвертор HFU 3 кВт 24 В",
            "title_ru": "Инвертор HFU 3 кВт 24 В",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/28/202604281731345837.jpg",
            "alt_ru": "Инвертор LU 3 кВт 24 В",
            "title_ru": "Инвертор LU 3 кВт 24 В",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/28/202604281732219885.jpg",
            "alt_ru": "Солнечный инвертор LF 3 кВт 24 В",
            "title_ru": "Солнечный инвертор LF 3 кВт 24 В",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/25/202604251400021354.jpg",
            "alt_ru": "Питание от автономного инвертора",
            "title_ru": "Питание от автономного инвертора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/25/202604251352156964.jpg",
            "alt_ru": "Может ли инвертор быть слишком мощным",
            "title_ru": "Может ли инвертор быть слишком мощным",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/04/21/202604211150408298.jpg",
            "alt_ru": "Максимальная входная мощность PV инвертора",
            "title_ru": "Максимальная входная мощность PV инвертора",
        },
    ],
]

IMAGE_LOG: list[dict] = []
USED_FILE_STEMS: set[str] = set()

_TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "",
    "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def slugify(text: str) -> str:
    text = text.lower()
    text = "".join(_TRANSLIT.get(ch, ch) for ch in text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
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
        "3:1": 3.0,
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
    timeouts = [240, 600]
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
            # Near-square diagrams come back as 1:1; 0.11 still rejects a real crop.
            if ratio_delta > 0.11:
                print(f"[duomi] reject ratio {cw}x{ch} vs {orig_wh} delta={ratio_delta:.3f}", flush=True)
                time.sleep(3)
                continue

            diff_score = image_mean_diff(orig_path, raw, orig_wh[0], orig_wh[1])
            # Text-heavy banners change many pixels; a full redesign scores much higher.
            if diff_score > 55.0:
                print(f"[duomi] reject redesign diff={diff_score:.2f}", flush=True)
                time.sleep(3)
                continue
            print(f"[duomi] accept {cw}x{ch} diff={diff_score:.2f} ratio_delta={ratio_delta:.3f}", flush=True)

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
            stem = unique_stem(slugify(im["alt_ru"]))
            ext = Path(im["src"]).suffix.lower() or ".jpg"
            if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
                ext = ".jpg"
            local = OUT / f"_src_ru_p{PAGE_NUM}_a{article_idx}_i{img_idx}{ext}"
            if not local.exists() or local.stat().st_size == 0:
                rr = requests.get(im["src"], timeout=60, headers={"User-Agent": UA})
                rr.raise_for_status()
                local.write_bytes(rr.content)
            with Image.open(local) as pil:
                orig_wh = pil.size

            need_duomi = (article_idx, img_idx) in DUOMI_MAP
            method = "duomi" if need_duomi else "compress"
            duomi_path = None
            final: Path
            tagged = OUT / f"{stem}.jpg"
            marker = OUT / f"{stem}.method.json"
            reused = False
            if tagged.exists() and tagged.stat().st_size > 0 and tagged.stat().st_size <= 100 * 1024 and marker.exists():
                meta = json.loads(marker.read_text(encoding="utf-8"))
                with Image.open(tagged) as chk:
                    size_ok = chk.size == orig_wh
                expected = "duomi" if need_duomi else "compress"
                if size_ok and meta.get("method") == expected and meta.get("src") == im["src"]:
                    final = tagged
                    method = "duomi-reuse" if need_duomi else "compress-reuse"
                    duomi_path = meta.get("duomi_path")
                    reused = True
                    print(f"[img] reuse {tagged.name} method={method}", flush=True)
            if reused:
                pass
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

            stored_method = "duomi" if method.startswith("duomi") and method != "duomi-fallback-original" else "compress"
            if method == "duomi-fallback-original":
                stored_method = "duomi-fallback-original"
            marker.write_text(
                json.dumps(
                    {"method": stored_method if not method.endswith("reuse") else ("duomi" if "duomi" in method else "compress"),
                     "src": im["src"],
                     "duomi_path": duomi_path},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            entry = {
                "local": final,
                "alt_ru": im["alt_ru"],
                "title_ru": im["title_ru"],
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
    Path(f"/tmp/page{PAGE_NUM}_ru_image_log.json").write_text(
        json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return prepared_all


if __name__ == "__main__":
    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
