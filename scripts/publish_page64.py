#!/usr/bin/env python3
"""Publish xindun-power news page 64 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

import publish_page55 as base

base.PAGE_NUM = 64
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 0-1: product photos (inverter + battery) without English marketing overlays.
# Article 2: VS comparison poster with "Inverter" / "DC solar system" labels.
# Article 3: MPPT vs PMW category labels on product showcase.
# Article 4: peak vs average power diagram with English axis/legend labels.
base.DUOMI_MAP = {
    (2, 0): (
        "Translate the bottom labels to Spanish: Inverter, DC solar system. "
        "Keep the VS graphic, hand-drawn borders, products, and layout unchanged."
    ),
    (3, 0): (
        "Translate the bottom category labels to Spanish: MPPT(10A-100A), PMW(10A-200A). "
        "Keep all solar controllers, solar farm background, and composition unchanged."
    ),
    (4, 0): (
        "Translate diagram labels to Spanish: Power (W), Average Power, Peak Power, t (s). "
        "Keep the graph lines, axis numbers, inverter product photo, and layout unchanged."
    ),
}

TITLE_OVERRIDES = {
    "what can a off grid solar power inverter do?": (
        "¿Qué puede hacer un inversor de energía solar fuera de la red?"
    ),
    "How long can a fully charged 12 volt battery and 12 volt inverter last?": (
        "¿Cuánto tiempo pueden durar una batería de 12 voltios y un inversor de 12 voltios "
        "completamente cargados?"
    ),
    "What do DC inverter and AC inverter mean?": (
        "¿Qué significan inversor de CC e inversor de CA?"
    ),
    "Is mppt solar controller really better than pwm solar controller?": (
        "¿Es el controlador solar MPPT realmente mejor que el controlador solar PWM?"
    ),
    "What does the peak power of the power inverter mean and what is the difference between it and the rated power": (
        "¿Qué significa la potencia pico del inversor de corriente y cuál es la diferencia "
        "entre ella y la potencia nominal?"
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
