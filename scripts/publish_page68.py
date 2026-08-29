#!/usr/bin/env python3
"""Publish xindun-power news page 68 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

import publish_page55 as base

base.PAGE_NUM = 68
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 1: installation collage with "Controller" and "Inverter" diagram labels.
# Article 3: marketing poster with "700w-12kw low frequency pure sine wave inverter".
# Articles 0, 2, and 4 are product/installation photos — compress/rename only.
base.DUOMI_MAP = {
    (1, 0): (
        "Translate diagram overlay labels to Spanish: Controller, Inverter. "
        "Keep solar panels, building exterior, electrical cabinets, wiring, "
        "and three-panel collage layout unchanged."
    ),
    (3, 0): (
        "Translate the orange marketing overlay text to Spanish: "
        "700w-12kw low frequency pure sine wave inverter. "
        "Keep yellow inverter products, city skyline background, and composition unchanged."
    ),
}

TITLE_OVERRIDES = {
    "Does it matter if car's 12V battery is connected to 2000w solar power inverter?": (
        "¿Importa si la batería de 12 V del automóvil está conectada a un inversor solar de 2000 W?"
    ),
    "Can an off grid solar inverter charger replace the solar controller?": (
        "¿Puede un cargador de inversor solar off-grid reemplazar al controlador solar?"
    ),
    "Xindun power assists China's Shanxi Provincial Government to build a new 5G+ smart tourism business in Dazhai": (
        "Xindun Power ayuda al Gobierno Provincial de Shanxi de China a construir un nuevo negocio de turismo inteligente 5G+ en Dazhai"
    ),
    "Which power inverter kit is better": (
        "¿Qué kit de inversor de potencia es mejor?"
    ),
    "How to match the photovoltaic power inverter and photovoltaic power generation system?": (
        "¿Cómo emparejar el inversor de energía fotovoltaica y el sistema de generación de energía fotovoltaica?"
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
