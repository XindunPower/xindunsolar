#!/usr/bin/env python3
"""Publish xindun-power news page 65 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

import publish_page55 as base

base.PAGE_NUM = 65
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 0: product photo (industrial inverter cabinets) — no English marketing overlays.
# Article 1: residential solar diagram (Solar panel, Battery, Single phase inverter, 1 phase AC).
# Article 2: battery-inverter-refrigerator diagram (DC / AC arrow labels).
# Article 3: Venn diagram (Low frequency / Pure sine wave / overlap label).
# Article 4: waveform diagram (DC / AC on sine wave chart).
base.DUOMI_MAP = {
    (1, 0): (
        "Translate diagram labels to Spanish: Solar panel, Battery, Single phase inverter, "
        "1 phase AC. Keep house icon, solar panels, batteries, inverter product, arrows, "
        "and layout unchanged."
    ),
    (2, 0): (
        "Translate the DC and AC arrow labels to Spanish (CC and CA). "
        "Keep battery, inverter, refrigerator products, arrows, and layout unchanged."
    ),
    (3, 0): (
        "Translate Venn diagram labels to Spanish: Low frequency inverter, "
        "Pure sine wave inverter, Low frequency pure sine wave inverter. "
        "Keep circles, colors, inverter products, and layout unchanged."
    ),
    (4, 0): (
        "Translate diagram labels DC and AC to Spanish (CC and CA). "
        "Keep waveform graph, axes u/t, inverter products, and layout unchanged."
    ),
}

TITLE_OVERRIDES = {
    "How much is the 380V AC output current of a 3 phase 50kw photovoltaic inverter": (
        "¿Cuál es la corriente de salida de 380 V CA de un inversor fotovoltaico trifásico de 50 kW?"
    ),
    "Is the home inverter single-phase or three-phase": (
        "¿El inversor doméstico es monofásico o trifásico?"
    ),
    "How long can a 12V 75A battery with a 3000W pure sine wave power inverter drive a 40W refrigerator?": (
        "¿Cuánto tiempo puede una batería de 12 V 75 A con un inversor de onda sinusoidal pura "
        "de 3000 W alimentar un refrigerador de 40 W?"
    ),
    "What is the difference between a low frequency inverter and a pure sine wave inverter": (
        "¿Cuál es la diferencia entre un inversor de baja frecuencia y un inversor de onda sinusoidal pura?"
    ),
    "Can the inverter convert AC to DC?": (
        "¿Puede el inversor convertir CA a CC?"
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
