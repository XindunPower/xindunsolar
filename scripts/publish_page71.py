#!/usr/bin/env python3
"""Publish xindun-power news page 71 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

from PIL import Image

import publish_page55 as base

base.PAGE_NUM = 71
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Articles 0-2 have English diagram/marketing overlay text; 3-4 are product photos only.
base.DUOMI_MAP = {
    (0, 0): (
        "Translate the diagram legend labels to Spanish: powering, free-wheeling, recovery diode. "
        "Keep the three-phase bridge circuit schematic, colored arrows, Q/D transistor labels, "
        "and the two inverter product photos unchanged."
    ),
    (1, 0): (
        "Translate the device labels around the circle to Spanish: TV, iphone, ipad, camera, "
        "notebook, speaker, camcorder, shaver. Keep the three yellow inverters, circular layout, "
        "and product casing text unchanged."
    ),
    (2, 0): (
        "Translate the bottom banner overlay labels to Spanish: MPPT(10A-100A) and PMW(10A-200A). "
        "Keep SOLAR Charge Controller product casing text, all controller units, forest background, "
        "and product lineup layout unchanged."
    ),
}

TITLE_OVERRIDES = {
    "A pure sine wave solar inverter charger how does it work": (
        "¿Cómo funciona un cargador de inversor solar de onda sinusoidal pura?"
    ),
    "Use of off grid power house inverter": (
        "Uso del inversor off-grid para vivienda"
    ),
    "Pwm and mppt solar controller selection": (
        "Selección de controlador solar PWM y MPPT"
    ),
    "How much AH battery is needed for the inverter": (
        "¿Cuántos Ah de batería se necesitan para el inversor?"
    ),
    "Off grid 100kw inverter parameters": (
        "Parámetros del inversor off-grid de 100 kW"
    ),
}

ALT_OVERRIDES = {
    "A pure sine wave solar inverter charger how does it work": (
        "¿Cómo funciona un cargador de inversor solar de onda sinusoidal pura?"
    ),
    "Use of off grid power house inverter": (
        "Uso del inversor off-grid para vivienda"
    ),
    "Pwm and mppt solar controller selection": (
        "Selección de controlador solar PWM y MPPT"
    ),
    "How much AH battery is needed for the inverter": (
        "¿Cuántos Ah de batería se necesitan para el inversor?"
    ),
    "Off grid 100kw inverter parameters": (
        "Parámetros del inversor off-grid de 100 kW"
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
base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    base.main()
