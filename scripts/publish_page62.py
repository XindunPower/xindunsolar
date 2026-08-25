#!/usr/bin/env python3
"""Publish xindun-power news page 62 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

import publish_page55 as base

base.PAGE_NUM = 62
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 0 has English marketing question overlay on product photo.
# Articles 1-4 are product lineup, factory, festive logo graphic, or event photo.
base.DUOMI_MAP = {
    (0, 0): (
        "Translate the English question overlay at the top to Spanish: "
        "'Can I use a 2000 watts inverter, if my appliances just equal to 2000 watts'. "
        "Keep the inverter product, SOLAR POWER SYSTEM casing text, background kitchen, "
        "and layout unchanged."
    ),
}

TITLE_OVERRIDES = {
    "Can I use a 2000 watts inverter, if my appliances just equal to 2000 watts?": (
        "¿Puedo usar un inversor de 2000 vatios si mis electrodomésticos tienen solo 2000 vatios?"
    ),
    "What should you get know before purchase your inverter?": (
        "¿Qué debes saber antes de comprar tu inversor?"
    ),
    "Which is the best photovoltaic solar inverter manufacturer?": (
        "¿Cuál es el mejor fabricante de inversores solares fotovoltaicos?"
    ),
    "Xindun Power 2020 Mid-Autumn Festival National Day holiday schedule": (
        "Calendario de vacaciones del Festival del Medio Otoño y Día Nacional 2020 de Xindun Power"
    ),
    "Celebrate the Mid-Autumn Festival-Xindun Power Company provides benefits for employees": (
        "Celebre el Festival del Medio Otoño: Xindun Power Company ofrece beneficios a los empleados"
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
