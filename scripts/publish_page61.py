#!/usr/bin/env python3
"""Publish xindun-power news page 61 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

import publish_page55 as base

base.PAGE_NUM = 61
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Only images with English marketing/diagram overlay text should use duomi.
# Other images are product photos or product casing text and must keep original
# composition (compress + Spanish alt filename only).
base.DUOMI_MAP = {
    (0, 0): (
        "Translate the labels 'Low frequency converter' and 'High frequency converter' to Spanish. "
        "Keep inverter products, VS mark style, and layout unchanged."
    ),
    (1, 0): (
        "Translate visible English marketing overlay text in the laptop screen area to Spanish, "
        "including the heading 'PRODUCTS'. Keep shopping cart, money, laptop, logos, product images, "
        "and composition unchanged."
    ),
    (2, 0): (
        "Translate diagram labels 'Toroidal transformer' and 'EI square transformer' to Spanish. "
        "Keep internal components, VS artwork, arrows, and layout unchanged."
    ),
}

TITLE_OVERRIDES = {
    "Difference between Low frequency converter and High frequency converter": (
        "Diferencia entre convertidor de baja frecuencia y convertidor de alta frecuencia"
    ),
    "Buy a pure sine wave inverter solar charger online": (
        "Comprar en línea un cargador solar con inversor de onda sinusoidal pura"
    ),
    "Toroidal transformer or EI square transformer? Which one is better for inverter": (
        "¿Transformador toroidal o transformador cuadrado EI? ¿Cuál es mejor para el inversor?"
    ),
    "What is the advantages of solar inverter battery charging and discharging voltage can be adjusted?": (
        "¿Cuáles son las ventajas de que se pueda ajustar el voltaje de carga y descarga de la batería del inversor solar?"
    ),
    "What is on off grid inverter?": "¿Qué es un inversor on-grid/off-grid?",
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
