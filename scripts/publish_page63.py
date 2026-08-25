#!/usr/bin/env python3
"""Publish xindun-power news page 63 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator

import publish_page55 as base

base.PAGE_NUM = 63
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Article 4 diagram has English labels (Grid, Generator, Solar panels, Batteries, AC loads).
# Articles 0-3 are product/factory photos without English marketing overlays.
base.DUOMI_MAP = {
    (4, 0): (
        "Translate diagram labels to Spanish: Grid, Generator, Solar panels, "
        "Batteries (Optional), AC loads. Keep the solar inverter product, red arrows, "
        "appliance icons, and overall layout unchanged. Do not change SOLAR INVERTER "
        "text on the product casing."
    ),
}

TITLE_OVERRIDES = {
    "Xindun house power inverter charger 12v to 220v": (
        "Cargador inversor de energía doméstica Xindun de 12 V a 220 V"
    ),
    "Photovoltaic inverter OEM - Xindun Power Technology Co., Ltd.": (
        "OEM de inversor fotovoltaico - Xindun Power Technology Co., Ltd."
    ),
    "How about pure sine wave inverters sold online": (
        "¿Qué tal los inversores de onda sinusoidal pura vendidos en línea?"
    ),
    "How much power inverter can drive the induction cooker": (
        "¿Cuánta potencia necesita un inversor para accionar la cocina de inducción?"
    ),
    "Can I Use Solar Inverter Without Battery?": (
        "¿Puedo usar un inversor solar sin batería?"
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
