#!/usr/bin/env python3
"""Publish xindun-power news page 67 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

import publish_page55 as base

base.PAGE_NUM = 67
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 1: off-grid inverter diagram (Grid, Generator, Solar panels, Batteries, AC loads).
# Article 2: 50kW price list diagram (Price tiers, BATTERY, AC INPUT, AC OUTPUT).
# Article 3: 350W hybrid function diagram (AC/DC loads, Solar Panels, Battery, warning text).
# Articles 0 and 4 are installation/product photos — compress/rename only.
base.DUOMI_MAP = {
    (1, 0): (
        "Translate diagram labels to Spanish: Grid, Generator, Solar panels, "
        "Batteries, (Optional), AC loads. Keep inverter product, arrows, icons, "
        "appliance images, and overall layout unchanged."
    ),
    (2, 0): (
        "Translate overlay text to Spanish: Price pricing tiers (keep dollar amounts), "
        "BATTERY, AC INPUT, AC OUTPUT. Keep product cabinet views, dimensions in cm, "
        "breakers, and layout unchanged."
    ),
    (3, 0): (
        "Translate diagram labels and warning text to Spanish: AC Loads, Generator, or, "
        "Power Grid, Solar Panels, DC Loads, Battery, and the red warning about total load "
        "power vs rated inverter power. Keep inverter rear panel, connection lines, "
        "appliance icons, and composition unchanged."
    ),
}

TITLE_OVERRIDES = {
    "Characteristics of off-grid photovoltaic power generation system": (
        "Características del sistema de generación de energía fotovoltaica off-grid"
    ),
    "Can photovoltaic off-grid inverters without batteries?": (
        "¿Pueden los inversores fotovoltaicos off-grid funcionar sin baterías?"
    ),
    "Off grid home use solar inverter 50kw price list": (
        "Lista de precios de inversor solar off-grid de 50 kW para uso doméstico"
    ),
    "350w pure sine wave hybrid energy inverter function": (
        "Función del inversor híbrido de energía de onda sinusoidal pura de 350 W"
    ),
    "What is the life span of the 20kw off grid photovoltaic inverter": (
        "¿Cuál es la vida útil del inversor fotovoltaico off-grid de 20 kW?"
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


def translate_text_resilient(text: str, retries: int = 3) -> str:
    text = base.clean_spaces(text)
    if not text:
        return text
    if text in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[text]
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
base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    base.main()
