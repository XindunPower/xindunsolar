#!/usr/bin/env python3
"""Publish xindun-power news page 82 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator, MyMemoryTranslator

import publish_page55 as base

base.PAGE_NUM = 82
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 0: diagram labels MPPT/PWM on product photo.
# Article 1: award ceremony at Chinese expo — compress only.
# Article 2: product composite — compress only.
# Article 3: three-panel diagram with English captions.
# Article 4: hexagon marketing infographic with English labels.
base.DUOMI_MAP = {
    (0, 0): (
        "Translate the white diagram labels 'MPPT' and 'PWM' at the bottom to Spanish. "
        "Keep all products, sunset background, and composition unchanged."
    ),
    (3, 0): (
        "Translate the three caption labels below the photos to Spanish: "
        "'Small DC system', 'M-scale off-grid system', 'L-scale off-grid system'. "
        "Keep all three photos, layout, and composition unchanged."
    ),
    (4, 0): (
        "Translate the hexagon labels to Spanish: 'Solar energy system', "
        "'Wind energy system', 'Telecom system', 'Emergency light', 'Power station'. "
        "Keep hexagon frames, product photo, and layout unchanged."
    ),
}

TITLE_OVERRIDES = {
    "Which is better, PWM or MPPT solar controller?": (
        "¿Qué es mejor, un controlador solar PWM o MPPT?"
    ),
    'Xindun Power won the "2020 Excellent Manufacturer in Solar Photovoltaic Industry" award': (
        'Xindun Power ganó el premio "Excelente Fabricante en la Industria Fotovoltaica Solar 2020"'
    ),
    "What factors need to be considered when configuring a solar power system?": (
        "¿Qué factores deben tenerse en cuenta al configurar un sistema de energía solar?"
    ),
    "Design of off-grid photovoltaic power generation system": (
        "Diseño del sistema de generación de energía fotovoltaica fuera de la red"
    ),
    "Pure sine wave inverter applications": (
        "Aplicaciones de inversores de onda sinusoidal pura"
    ),
}

ALT_OVERRIDES = {
    "Which is better, PWM or MPPT solar controller?": (
        "¿Qué es mejor, un controlador solar PWM o MPPT?"
    ),
    "Xindun power adward": "Premio Xindun Power",
    "Design of off grid photovoltaic power generation system": (
        "Diseño del sistema de generación de energía fotovoltaica fuera de la red"
    ),
    "Design of off-grid photovoltaic power generation system": (
        "Diseño del sistema de generación de energía fotovoltaica fuera de la red"
    ),
    "pure sine wave inverter applications": (
        "Aplicaciones de inversores de onda sinusoidal pura"
    ),
}

_MYMEMORY: MyMemoryTranslator | None = None


def _mymemory() -> MyMemoryTranslator:
    global _MYMEMORY
    if _MYMEMORY is None:
        _MYMEMORY = MyMemoryTranslator(source="en-GB", target="es-ES")
    return _MYMEMORY


def already_published_strict(title_es: str, title_en: str) -> str | None:
    """Stricter duplicate check: require slug or exact title, or nearly full token overlap."""
    import requests

    s = requests.Session()
    s.headers["User-Agent"] = base.UA

    def title_match(query: str, rendered: str) -> bool:
        ql = base.normalize_title(query)
        rt = base.normalize_title(rendered)
        if not ql or not rt:
            return False
        if rt == ql or rt.rstrip("?") == ql.rstrip("?"):
            return True
        stop = {
            "cual", "cuál", "para", "como", "cómo", "que", "qué", "esta", "este",
            "from", "with", "what", "when", "where", "mejor", "best", "solar",
            "paneles", "panels", "sistema", "system", "energia", "energía", "power",
            "the", "and", "for", "inversor", "inverter", "inversores", "phase", "fase",
        }

        def tokens(text: str) -> set[str]:
            return {
                t
                for t in re.split(r"[^a-z0-9áéíóúñü]+", text.lower())
                if len(t) > 3 and t not in stop
            }

        q_tok = tokens(query)
        if len(q_tok) < 2:
            return False
        shared = tokens(rendered) & q_tok
        return len(shared) >= len(q_tok)

    if title_es:
        try:
            r = s.get(
                f"{base.WP}/wp-json/wp/v2/posts",
                params={
                    "slug": base.slugify(title_es),
                    "categories": base.CAT,
                    "per_page": 5,
                    "status": "publish",
                },
                timeout=30,
            )
            if r.ok and r.json():
                return r.json()[0].get("link")
        except Exception:  # noqa: BLE001
            pass

    for q in (title_es, title_en):
        if not q or len(q.strip()) < 8:
            continue
        try:
            r = s.get(
                f"{base.WP}/wp-json/wp/v2/posts",
                params={"search": q, "categories": base.CAT, "per_page": 10, "status": "publish"},
                timeout=30,
            )
            if not r.ok:
                continue
            for post in r.json():
                rendered = (post.get("title") or {}).get("rendered") or ""
                if title_match(q, rendered):
                    return post.get("link")
        except Exception:  # noqa: BLE001
            continue
    return None


def _fit_crop_to_ratio(im, target_ratio: float):
    from PIL import Image

    w, h = im.size
    current_ratio = w / h if h else 1.0
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(w / target_ratio)
    top = (h - new_h) // 2
    return im.crop((0, top, w, top + new_h))


def _image_mean_diff_cropped(orig_path: Path, candidate_path: Path, tw: int, th: int) -> float:
    from PIL import Image, ImageChops, ImageStat

    target_ratio = tw / th if th else 1.0
    with Image.open(orig_path) as im1, Image.open(candidate_path) as im2:
        a = im1.convert("RGB").resize((tw, th), Image.Resampling.BICUBIC)
        b = _fit_crop_to_ratio(im2.convert("RGB"), target_ratio).resize(
            (tw, th), Image.Resampling.BICUBIC
        )
    diff = ImageChops.difference(a, b)
    mean_rgb = ImageStat.Stat(diff).mean
    return float(sum(mean_rgb) / len(mean_rgb))


DUOMI_DIFF_OVERRIDES: dict[tuple[int, int], float] = {
    # Hexagon infographic: label translation raises pixel diff but layout stays intact.
    (4, 0): 38.0,
}


def run_duomi_relaxed_ratio(
    image_url: str,
    extra_prompt: str,
    stem: str,
    size: str,
    orig_wh: tuple[int, int],
    orig_path: Path,
    attempts: int = 8,
    article_idx: int = -1,
    img_idx: int = -1,
):
    """Allow Duomi 3:2 output when original is slightly off-ratio (e.g. 600x400)."""
    import json
    import subprocess

    prompt = f"{base.PROMPT_BASE} {extra_prompt}"
    final = base.OUT / f"{stem}.jpg"
    orig_ratio = orig_wh[0] / orig_wh[1] if orig_wh[1] else 1.0
    override = DUOMI_DIFF_OVERRIDES.get((article_idx, img_idx))
    if override is not None:
        diff_limit = override
    elif orig_ratio > 2.0:
        diff_limit = 50.0
    elif orig_ratio > 1.7:
        diff_limit = 55.0
    else:
        diff_limit = 28.0
    best: tuple[float, Path] | None = None

    for attempt in range(attempts):
        out_name = f"{stem}-try{attempt + 1}"
        print(f"[duomi] {stem} attempt={attempt + 1} size={size}", flush=True)
        cmd = [
            "python3",
            str(base.REPO / "scripts" / "duomi_image.py"),
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
            "600",
        ]
        p = subprocess.run(cmd, cwd=base.REPO, capture_output=True, text=True)
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
            time.sleep(5)
            continue

        raw = Path(files[0])
        if not raw.exists():
            print(f"[duomi] output missing: {raw}", flush=True)
            time.sleep(3)
            continue

        try:
            with __import__("PIL").Image.open(raw) as chk:
                cw, ch = chk.size
            ratio_delta = abs((cw / ch) - orig_ratio)
            if ratio_delta > 0.15:
                print(
                    f"[duomi] ratio drift {cw}x{ch} vs {orig_wh} (delta={ratio_delta:.3f}); "
                    "validating with aspect crop",
                    flush=True,
                )

            diff_score = _image_mean_diff_cropped(orig_path, raw, orig_wh[0], orig_wh[1])
            print(f"[duomi] diff={diff_score:.2f} limit={diff_limit}", flush=True)
            if diff_score <= diff_limit and (best is None or diff_score < best[0]):
                best = (diff_score, raw)
        except Exception as exc:  # noqa: BLE001
            print(f"[duomi] layout check failed: {exc}", flush=True)
            time.sleep(3)
            continue

    if best is None:
        return None

    try:
        raw = best[1]
        cropped = base.OUT / f"{stem}-cropped.png"
        from PIL import Image

        with Image.open(raw) as im:
            fitted = _fit_crop_to_ratio(im.convert("RGB"), orig_ratio)
            fitted.save(cropped)
        base.encode_jpeg(cropped, final, orig_wh[0], orig_wh[1], 100)
    except Exception as exc:  # noqa: BLE001
        print(f"[duomi] final encode failed: {exc}", flush=True)
        return None

    if final.exists() and final.stat().st_size > 0:
        return final
    return None


def translate_text_resilient(text: str, retries: int = 3) -> str:
    text = base.clean_spaces(text.replace("\\'", "'"))
    if not text:
        return text
    if text in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[text]
    if text in ALT_OVERRIDES:
        return ALT_OVERRIDES[text]
    if not re.search(r"[A-Za-zÀ-ÿ]", text):
        return text

    normalized = text
    if "-" in text and " " not in text and re.search(r"[A-Za-z]-[A-Za-z]", text):
        normalized = text.replace("-", " ")

    for attempt in range(retries):
        try:
            out = GoogleTranslator(source="en", target="es").translate(normalized)
            out = base.clean_spaces(out)
            if out and not re.search(r"Error\s*500|Server Error", out, re.I):
                return out
        except Exception as exc:  # noqa: BLE001
            print(f"[translate-google] retry {attempt + 1}: {exc}", flush=True)
        time.sleep(1.6 * (attempt + 1))

    try:
        out = base.clean_spaces(_mymemory().translate(normalized))
        if out and not re.search(r"Error\s*500|Server Error", out, re.I):
            return out
    except Exception as exc:  # noqa: BLE001
        print(f"[translate-mymemory] failed: {exc}", flush=True)

    print(f"[translate] fallback keep original: {text[:80]!r}", flush=True)
    return text


def translate_html_resilient(html: str) -> str:
    from bs4 import BeautifulSoup, NavigableString

    soup = BeautifulSoup(html, "lxml")
    body = soup.body or soup
    for node in list(body.descendants):
        if not isinstance(node, NavigableString):
            continue
        parent = node.parent
        if parent is None or parent.name in {"script", "style"}:
            continue
        raw = str(node)
        if not raw.strip() or not re.search(r"[A-Za-z]", raw):
            continue
        node.replace_with(translate_text_resilient(raw))
        time.sleep(0.15)

    for a in body.find_all("a"):
        a.unwrap()

    if body.name == "body":
        return "".join(str(c) for c in body.children)
    return str(body)


_CURRENT_DUOMI_IDX: tuple[int, int] = (-1, -1)


def run_duomi_bound(
    image_url: str,
    extra_prompt: str,
    stem: str,
    size: str,
    orig_wh: tuple[int, int],
    orig_path: Path,
    attempts: int = 8,
):
    a, i = _CURRENT_DUOMI_IDX
    return run_duomi_relaxed_ratio(
        image_url, extra_prompt, stem, size, orig_wh, orig_path, attempts, a, i
    )


def prepare_images_with_idx(article_idx: int, images: list[dict]) -> list[dict]:
    global _CURRENT_DUOMI_IDX
    prepared: list[dict] = []
    for img_idx, im in enumerate(images):
        _CURRENT_DUOMI_IDX = (article_idx, img_idx)
        alt_en = im["alt"] or f"imagen-{article_idx}-{img_idx}"
        alt_es = translate_text_resilient(alt_en)
        title_es = translate_text_resilient(im.get("title") or alt_en)
        stem = base.unique_stem(base.slugify(alt_es))

        ext = Path(im["src"]).suffix.lower() or ".jpg"
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
            ext = ".jpg"
        local = base.OUT / f"_src_a{article_idx}_i{img_idx}{ext}"
        if not local.exists() or local.stat().st_size == 0:
            rr = __import__("requests").get(im["src"], timeout=60, headers={"User-Agent": base.UA})
            rr.raise_for_status()
            local.write_bytes(rr.content)

        from PIL import Image

        with Image.open(local) as pil:
            orig_wh = pil.size

        tagged = base.OUT / f"{stem}.jpg"
        method = "duomi" if (article_idx, img_idx) in base.DUOMI_MAP else "compress"
        duomi_path = None
        if tagged.exists() and tagged.stat().st_size > 0:
            method += "-reuse"
            final = tagged
            if "duomi" in method:
                duomi_path = str(tagged)
        elif (article_idx, img_idx) in base.DUOMI_MAP:
            size = base.size_for(*orig_wh)
            result = run_duomi_bound(
                im["src"],
                base.DUOMI_MAP[(article_idx, img_idx)],
                stem,
                size,
                orig_wh,
                local,
            )
            if result is None:
                raise RuntimeError(f"duomi failed for required overlay image a{article_idx}_i{img_idx}")
            final = result
            duomi_path = str(result)
        else:
            final = base.compress_only(local, stem, orig_wh)

        if final.stat().st_size > 100 * 1024:
            raise RuntimeError(f"image exceeds 100KB: {final}")
        with Image.open(final) as chk:
            if chk.size != orig_wh:
                raise RuntimeError(f"image dimensions changed for {final}: {chk.size} vs {orig_wh}")

        entry = {
            "local": final,
            "alt_es": alt_es,
            "title_es": title_es,
            "src_orig": im["src"],
            "method": method,
            "duomi_path": duomi_path,
            "orig_wh": orig_wh,
        }
        base.IMAGE_LOG.append(
            {
                "article": article_idx,
                "img": img_idx,
                **{k: (str(v) if k == "local" else v) for k, v in entry.items()},
            }
        )
        prepared.append(entry)
        print(
            f"[img] a{article_idx}_i{img_idx} method={method} -> {final.name} {final.stat().st_size}b",
            flush=True,
        )
    _CURRENT_DUOMI_IDX = (-1, -1)
    return prepared


base.translate_text = translate_text_resilient
base.translate_html = translate_html_resilient
base.run_duomi = run_duomi_bound
base.prepare_images = prepare_images_with_idx
base.already_published = already_published_strict
base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    base.main()
