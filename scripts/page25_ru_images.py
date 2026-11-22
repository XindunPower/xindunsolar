#!/usr/bin/env python3
"""Prepare page 25 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for marketing headlines and diagram captions.
Product studio shots are compressed only.
Product casing text, logos and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 25

_KEEP = (
    "Keep arrows, icons, colors, flags and the background. Do not move products or people. "
    "Do not add objects or labels that are not already in the image. Do not redesign. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, product casing text, "
    "model numbers, display readings, Chinese characters in the logo, "
    "or the URL www.xindun-power.com / xindun-power.com. "
    "Do not change words printed on the product such as SOLAR INVERTER, DC-AC, or POWER."
)

_TOROID = (
    "Close-up diagram of an inverter interior and a magnified toroidal transformer on a blue background. "
    "Translate only the white caption beside the pointer. "
    "'Inverter toroidal transformer' → 'Тороидальный трансформатор инвертора'. "
    "Keep the white pointer triangle, the magnified circle, the wires and the blue background. " + _KEEP
)

_UZ_CRISIS = (
    "Marketing banner: a tiled mosque and minaret on the left, a pale text panel on the right. "
    "Translate only the three black headline lines. "
    "'uzbekistan' → 'узбекистан'. "
    "'energy crisis' → 'энергетический кризис'. "
    "'analyse 2022' → 'анализ 2022'. "
    "Keep the three-line layout and similar letter size. "
    "Keep the xindun GREENPOWER logo and www.xindun-power.com exactly. " + _KEEP
)

_UZ_CHINA = (
    "Marketing banner: solar panels on the left, a white text panel, and the flags of Uzbekistan and China. "
    "Translate only the black headline. "
    "'LEADING CHINESE SOLAR ENERGY MANUFACTURER' → 'ВЕДУЩИЙ КИТАЙСКИЙ ПРОИЗВОДИТЕЛЬ СОЛНЕЧНОЙ ЭНЕРГИИ'. "
    "Keep '-XinDun Power' exactly, including the hyphen and that brand spelling. "
    "Keep the xindun GREENPOWER logo, both flags and the orange shapes. " + _KEEP
)

_OUTLOOK = (
    "Marketing banner: two solar trackers against a sunset. "
    "Translate only the yellow headline on the dark band. "
    "'Solar Energy Industry Outlook 2022' → 'Перспективы солнечной энергетики 2022'. "
    "Keep it one line. Keep the xindun GREENPOWER logo and xindun-power.com exactly. " + _KEEP
)

_WIND = (
    "Green illustrated banner with wind turbines, a light bulb, solar panels and three inverters. "
    "Translate only the yellow headline. "
    "'Xindun Power's solar inverters can be used for wind or solar power system' → "
    "'Солнечные инверторы Xindun Power подходят для ветровой или солнечной системы'. "
    "Keep Xindun Power as the company name. Keep the logo, including the Chinese characters under it. "
    "Do not move the inverters, turbines or icons. " + _KEEP
)

_CHOOSE = (
    "Marketing banner: a solar array on the right and a white text panel on the left. "
    "Translate only the orange three-line headline. "
    "Line 1 'HOW TO CHOOSE' → 'КАК ВЫБРАТЬ'. "
    "Line 2 'SOLAR POWER' → 'КОМПАНИЮ СОЛНЕЧНЫХ'. "
    "Line 3 'SYSTEM COMPANY?' → 'СИСТЕМ?'. "
    "Together the lines read 'КАК ВЫБРАТЬ КОМПАНИЮ СОЛНЕЧНЫХ СИСТЕМ?'. "
    "Keep the question mark and the three-line layout. "
    "Keep the xindun GREENPOWER logo and xindun-power.com exactly. " + _KEEP
)

_FACTORY = (
    "Factory photo collage of workers and inverter production lines. "
    "Translate only the white caption across the photo. "
    "Keep 'XINDUN' unchanged. "
    "'China solar power system company' → 'китайская компания солнечных энергосистем'. "
    "The caption must stay one line and read 'XINDUN китайская компания солнечных энергосистем'. "
    "Keep the xindun GREENPOWER logo. Do not change people, products or the factory. " + _KEEP
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "hf_hero": "https://www.xindun-power.com/uploadfile/upload/2020-10/27/whatishighfrequencyinverter.jpg",
    "hf_hp": "https://www.xindun-power.com/uploadfile/upload/2021-09/08/Highfrequencyinverter.jpg",
    "hf_ct_small": "https://www.xindun-power.com/uploadfile/upload/2021-03/06/GPCTSolarInverter300600W3.jpg",
    "hf_ct_large": "https://www.xindun-power.com/uploadfile/upload/2021-03/06/GPCTSolarInverter1KW2KW3.jpg",
    "hf_gpc": "https://www.xindun-power.com/uploadfile/upload/2021-09/08/Highfrequencyinverter2.jpg",
    "toroid": "https://www.xindun-power.com/uploadfile/upload/2021-06/02/Theadvantagesofusingtoroidaltransformerforinverters.jpg",
    "uz_crisis": "https://www.xindun-power.com/uploadfile/2023/03/02/202303020925178373.jpg",
    "uz_china": "https://www.xindun-power.com/uploadfile/2023/03/02/202303020927037984.jpg",
    "outlook_body": "https://www.xindun-power.com/uploadfile/2023/02/08/202302081512535165.jpg",
    "outlook_hero": "https://www.xindun-power.com/uploadfile/2023/02/08/20230208150949nWENK0.jpg",
    "choose_hero": "https://www.xindun-power.com/uploadfile/2023/02/16/202302161550153129.jpg",
    "choose_factory": "https://www.xindun-power.com/uploadfile/2023/02/16/202302161552166221.jpg",
}

DUOMI_BY_URL = {
    U["toroid"]: _TOROID,
    U["uz_crisis"]: _UZ_CRISIS,
    U["uz_china"]: _UZ_CHINA,
    U["outlook_body"]: _WIND,
    U["outlook_hero"]: _OUTLOOK,
    U["choose_hero"]: _CHOOSE,
    U["choose_factory"]: _FACTORY,
}

IMAGE_SOURCES = [
    [
        _im(U["hf_hero"], "Что такое высокочастотный солнечный инвертор"),
        _im(U["hf_hp"], "Высокочастотный солнечный инвертор серии HP"),
        _im(U["hf_ct_small"], "Высокочастотный солнечный инвертор серии CT"),
        _im(U["hf_ct_large"], "Высокочастотный солнечный инвертор серии CT"),
        _im(U["hf_gpc"], "Высокочастотный солнечный инвертор серии GP-C"),
    ],
    [
        _im(U["toroid"], "Преимущества тороидального трансформатора для инверторов"),
    ],
    [
        _im(U["uz_crisis"], "Энергетический кризис Узбекистана и солнечная энергетика"),
        _im(U["uz_china"], "Солнечная энергетика Узбекистана вместе с Китаем"),
    ],
    [
        _im(U["outlook_hero"], "Перспективы солнечной отрасли на 2022 год"),
        _im(U["outlook_body"], "Перспективы солнечной энергетики"),
    ],
    [
        _im(U["choose_hero"], "Компания солнечных систем как выбрать солнечную систему"),
        _im(U["choose_factory"], "Компания солнечных энергосистем как выбрать солнечную систему"),
    ],
]

IMAGE_LOG = engine.IMAGE_LOG


def prepare_all():
    engine.PAGE_NUM = PAGE_NUM
    engine.DUOMI_BY_URL = DUOMI_BY_URL
    engine.IMAGE_SOURCES = IMAGE_SOURCES
    engine.IMAGE_LOG.clear()
    return engine.prepare_all()


if __name__ == "__main__":
    import json

    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
