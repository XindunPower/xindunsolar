#!/usr/bin/env python3
"""Publish xindun-power news page 72 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

from PIL import Image

import publish_page55 as base

base.PAGE_NUM = 72
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 0: waveform diagram labels; article 3: "Pure sine wave output" banner overlay.
base.DUOMI_MAP = {
    (0, 0): (
        "Translate the oscilloscope diagram labels to Spanish: Modified Sine Wave and Pure Sine Wave. "
        "Keep both waveform screens, the car background, and the white inverter product unchanged."
    ),
    (3, 0): (
        "Translate the top banner overlay text 'Pure sine wave output' to Spanish. "
        "Keep all inverter products, floor, sky background, and product casing labels unchanged."
    ),
}

TITLE_OVERRIDES = {
    "Buy dc to ac power inverters for cars, choose pure sine wave or modified sine wave?": (
        "¿Comprar inversores de CC a CA para automóviles: onda sinusoidal pura o modificada?"
    ),
    "Solar photovoltaic inverters for solar power systems": (
        "Inversores solares fotovoltaicos para sistemas de energía solar"
    ),
    "What brand of inverters for home is better": (
        "¿Qué marca de inversores para el hogar es mejor?"
    ),
    "How to choose a pure sine wave inverter charger or converter charger?": (
        "¿Cómo elegir un cargador inversor de onda sinusoidal pura o un cargador convertidor?"
    ),
    "What can 12v 1000w pure sine wave inverter charger do?": (
        "¿Qué puede hacer el cargador inversor de onda sinusoidal pura de 12 V y 1000 W?"
    ),
}

ALT_OVERRIDES = {
    "Buy dc to ac power inverters for cars, choose pure sine wave or modified sine wave?": (
        "¿Comprar inversores de CC a CA para automóviles: onda sinusoidal pura o modificada?"
    ),
    "Solar photovoltaic inverters for solar power systems": (
        "Inversores solares fotovoltaicos para sistemas de energía solar"
    ),
    "What brand of inverters for home is better": (
        "¿Qué marca de inversores para el hogar es mejor?"
    ),
    "How to choose a pure sine wave inverter charger or converter charger?": (
        "¿Cómo elegir un cargador inversor de onda sinusoidal pura o un cargador convertidor?"
    ),
    "What can 12v 1000w pure sine wave inverter charger do?": (
        "¿Qué puede hacer el cargador inversor de onda sinusoidal pura de 12 V y 1000 W?"
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


def run_duomi_relaxed_ratio(
    image_url: str,
    extra_prompt: str,
    stem: str,
    size: str,
    orig_wh: tuple[int, int],
    orig_path: Path,
    attempts: int = 5,
):
    """Allow Duomi 3:2 output when original is slightly off-ratio (e.g. 600x400)."""
    import json
    import subprocess

    import publish_page55 as mod

    prompt = f"{mod.PROMPT_BASE} {extra_prompt}"
    final = mod.OUT / f"{stem}.jpg"
    for attempt in range(attempts):
        out_name = f"{stem}-try{attempt + 1}"
        print(f"[duomi] {stem} attempt={attempt + 1} size={size}", flush=True)
        cmd = [
            "python3",
            str(mod.REPO / "scripts" / "duomi_image.py"),
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
        p = subprocess.run(cmd, cwd=mod.REPO, capture_output=True, text=True)
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
            ratio_delta = abs((cw / ch) - (orig_wh[0] / orig_wh[1]))
            if ratio_delta > 0.15:
                print(f"[duomi] reject ratio {cw}x{ch} vs {orig_wh}", flush=True)
                time.sleep(3)
                continue

            diff_score = mod.image_mean_diff(orig_path, raw, orig_wh[0], orig_wh[1])
            if diff_score > 28.0:
                print(f"[duomi] reject redesign diff={diff_score:.2f}", flush=True)
                time.sleep(3)
                continue

            mod.encode_jpeg(raw, final, orig_wh[0], orig_wh[1], 100)
        except Exception as exc:  # noqa: BLE001
            print(f"[duomi] layout/compress failed: {exc}", flush=True)
            time.sleep(3)
            continue

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
