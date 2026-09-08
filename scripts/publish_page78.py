#!/usr/bin/env python3
"""Publish xindun-power news page 78 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

from PIL import Image, ImageChops, ImageStat

import publish_page55 as base

base.PAGE_NUM = 78
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 0: product photo (inverter + washing machine) — compress only.
# Article 1: DC/AC waveform diagram with DC, AC labels.
# Article 2: product grid with English marketing captions and prices.
# Article 3: VS comparison graphic (Power inverter vs Inverter generator).
# Article 4: marketing banner with overlay title text.
base.DUOMI_MAP = {
    (1, 0): (
        "Translate diagram labels to Spanish: DC and AC. "
        "Keep waveform graphs, axes u and t, inverter product photo, "
        "and black background layout unchanged."
    ),
    (2, 0): (
        "Translate the English product description captions and price labels below each "
        "product to Spanish (e.g. on/off grid inverter, solar inverter, power inverter, "
        "pure sine wave inverter, PV inverter, 3 phase inverter, UPS). "
        "Keep product photos, casing text like STORAGE Power Inverter, layout, "
        "white frames, and grid composition unchanged."
    ),
    (3, 0): (
        "Translate overlay labels to Spanish: Power inverter and Inverter generator. "
        "Keep VS logo, product photos, gray/blue backgrounds, and composition unchanged."
    ),
    (4, 0): (
        "Translate the green banner overlay text to Spanish: "
        "Various types of residential solar inverters. "
        "Keep product lineup, city background, STORAGE casing text on products, "
        "and layout unchanged."
    ),
}

TITLE_OVERRIDES = {
    "Can the 1500w hybrid solar inverter drive a 240w washing machine?": (
        "¿Puede el inversor solar híbrido de 1500 W accionar una lavadora de 240 W?"
    ),
    "Can an inverter convert DC into AC?": (
        "¿Puede un inversor convertir CC en CA?"
    ),
    "Xindun solar inverters ranking! Top 6 best solar inverters prices in south africa": (
        "¡Ranking de inversores solares Xindun! Top 6 mejores precios de inversores solares en Sudáfrica"
    ),
    "Which one is better, power inverter vs inverter generator?": (
        "¿Cuál es mejor, inversor de corriente o generador inversor?"
    ),
    "Types of residential solar inverters": (
        "Tipos de inversores solares residenciales"
    ),
}

ALT_OVERRIDES = {
    "Can the 1500w hybrid solar inverter drive a 240w washing machine?": (
        "¿Puede el inversor solar híbrido de 1500 W accionar una lavadora de 240 W?"
    ),
    "Can an inverter convert dc into ac?": (
        "¿Puede un inversor convertir CC en CA?"
    ),
    "price": (
        "Precio"
    ),
    "vs": (
        "Inversor de corriente frente a generador inversor"
    ),
    "Various types of residential solar inverters": (
        "Varios tipos de inversores solares residenciales"
    ),
}

_ARGOS_TR = None


def _argos_en_es():
    global _ARGOS_TR
    if _ARGOS_TR is not None:
        return _ARGOS_TR
    langs = argos_translate.get_installed_languages()
    lang_en = next((x for x in langs if x.code == "en"), None)
    lang_es = next((x for x in langs if x.code == "es"), None)
    if not lang_en or not lang_es:
        raise RuntimeError("Argos en->es model is not installed")
    _ARGOS_TR = lang_en.get_translation(lang_es)
    return _ARGOS_TR


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


def _fit_crop_to_ratio(im: Image.Image, target_ratio: float) -> Image.Image:
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
    target_ratio = tw / th if th else 1.0
    with Image.open(orig_path) as im1, Image.open(candidate_path) as im2:
        a = im1.convert("RGB").resize((tw, th), Image.Resampling.BICUBIC)
        b = _fit_crop_to_ratio(im2.convert("RGB"), target_ratio).resize((tw, th), Image.Resampling.BICUBIC)
    diff = ImageChops.difference(a, b)
    mean_rgb = ImageStat.Stat(diff).mean
    return float(sum(mean_rgb) / len(mean_rgb))


def run_duomi_relaxed_ratio(
    image_url: str,
    extra_prompt: str,
    stem: str,
    size: str,
    orig_wh: tuple[int, int],
    orig_path: Path,
    attempts: int = 8,
):
    """Allow Duomi 3:2 output when original is slightly off-ratio (e.g. 600x400)."""
    import json
    import subprocess

    prompt = f"{base.PROMPT_BASE} {extra_prompt}"
    final = base.OUT / f"{stem}.jpg"
    orig_ratio = orig_wh[0] / orig_wh[1] if orig_wh[1] else 1.0
    diff_limit = 50.0 if orig_ratio > 2.0 else 28.0
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
            with Image.open(raw) as chk:
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
        out = base.clean_spaces(_argos_en_es().translate(normalized))
        if out and not re.search(r"Error\s*500|Server Error", out, re.I):
            return out
    except Exception as exc:  # noqa: BLE001
        print(f"[translate-argos] failed: {exc}", flush=True)

    print(f"[translate] fallback keep original: {text[:80]!r}", flush=True)
    return text


base.translate_text = translate_text_resilient
base.run_duomi = run_duomi_relaxed_ratio
base.already_published = already_published_strict
base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    base.main()
