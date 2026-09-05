#!/usr/bin/env python3
"""Publish xindun-power news page 75 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

from PIL import Image, ImageChops, ImageStat

import publish_page55 as base

base.PAGE_NUM = 75
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 2: transformer type diagram with English labels (Toroidal/Square/Strip transformer).
# All other images are product/factory photos (compress+rename only).
base.DUOMI_MAP = {
    (2, 0): (
        "Translate diagram labels to Spanish: Toroidal transformer, Square transformer, "
        "Strip transformer. Keep all internal chassis photos, external inverter products, "
        "red highlight boxes, blue background, and layout unchanged."
    ),
}

TITLE_OVERRIDES = {
    "How many batteries do I need for a 3000 watt power inverter charger?": (
        "¿Cuántas baterías necesito para un cargador inversor de corriente de 3000 vatios?"
    ),
    "How long will a 12v pure sine wave inverter battery last with a pure sine wave power generator inverter?": (
        "¿Cuánto tiempo durará una batería de inversor de onda sinusoidal pura de 12 V "
        "con un inversor generador de energía de onda sinusoidal pura?"
    ),
    "Which type of transformer is used in DC to AC converter and inverter?": (
        "¿Qué tipo de transformador se utiliza en el convertidor e inversor de CC a CA?"
    ),
    "What is the role of solar energy storage inverter in solar energy storage system?": (
        "¿Cuál es el papel del inversor de almacenamiento de energía solar en el sistema "
        "de almacenamiento de energía solar?"
    ),
    "Professional off grid energy storage power inverter charger manufacturers": (
        "Fabricantes profesionales de cargadores inversores de potencia de almacenamiento "
        "de energía fuera de red"
    ),
}

ALT_OVERRIDES = {
    "How many batteries do I need for a 3000 watt power inverter charger?": (
        "¿Cuántas baterías necesito para un cargador inversor de corriente de 3000 vatios?"
    ),
    "How long will a 12v pure sine wave inverter battery last with a pure sine wave power generator inverter?": (
        "¿Cuánto tiempo durará una batería de inversor de onda sinusoidal pura de 12 V "
        "con un inversor generador de energía de onda sinusoidal pura?"
    ),
    "Which type of transformer is used in DC to AC converter and inverter?": (
        "¿Qué tipo de transformador se utiliza en el convertidor e inversor de CC a CA?"
    ),
    "What is the role of solar energy storage inverter in solar energy storage system?": (
        "¿Cuál es el papel del inversor de almacenamiento de energía solar en el sistema "
        "de almacenamiento de energía solar?"
    ),
    "Professional off grid energy storage power inverter charger manufacturers": (
        "Fabricantes profesionales de cargadores inversores de potencia de almacenamiento "
        "de energía fuera de red"
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
