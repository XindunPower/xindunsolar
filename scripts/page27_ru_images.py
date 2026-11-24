#!/usr/bin/env python3
"""Prepare page 27 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for marketing headlines and diagram captions.
Exhibition photos, factory floors and product studio shots are compressed only.
Product casing text, logos, Chinese booth signs and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 27

_KEEP = (
    "Keep arrows, icons, colors, people, products and the background. "
    "Do not move products or people. Do not add objects or labels that are not already in the image. "
    "Do not redesign the poster. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, product casing text, "
    "model numbers, display readings, Chinese characters on photos, certificates or walls, "
    "or the URL www.xindun-power.com / xindun-power.com. "
    "Do not change words printed on the product such as ALL IN ONE SOLAR GENERATOR, "
    "PV COMBINER BOX, XD200-12, SOLAR INVERTER, or POWER."
)

_CRISIS = (
    "Marketing banner: hands holding a glowing Earth. "
    "Translate only the two white headline lines. "
    "'Energy Crisis' → 'Энергетический кризис'. "
    "'is coming' → 'наступает'. "
    "Keep exactly two lines. Keep the logo. " + _KEEP
)

_SOLAR = (
    "Marketing banner: solar panels, a city skyline and a dark blue ribbon. "
    "Translate only the English marketing lines. "
    "On the blue ribbon, 'Solar Energy' → 'Солнечная энергия' and "
    "'renewable energy' → 'возобновляемая энергия'. Keep the vertical bar between them. "
    "On the small orange badge, 'Bright future' → 'Светлое будущее'. "
    "Keep the logo and the white, blue and orange colors. " + _KEEP
)

_REASONS = (
    "Marketing banner: four green and orange headline lines on the left, a hexagon icon on the right. "
    "Translate only those four lines and keep four lines. "
    "Line 1 '5 reasons why' → '5 причин выбрать'. "
    "Line 2 'choose Chinese' → 'китайского'. "
    "Line 3 'power inverter' → 'производителя'. "
    "Line 4 'manufactory' → 'инверторов'. "
    "Keep the green and orange colors, the hexagon, the sun and the panels. Keep the logo. " + _KEEP
)

_BEST = (
    "Marketing banner: a house with rooftop solar and two inverter cabinets. "
    "Translate only the three white headline lines on the blue panel. Keep three lines. "
    "Line 1 'Best All In One' → 'Лучшая «всё в одном»'. "
    "Line 2 'Off Grid' → 'автономная'. "
    "Line 3 'Solar Power System' → 'солнечная энергосистема'. "
    "Do NOT change 'ALL IN ONE SOLAR GENERATOR' or any text printed on the cabinets. "
    "Keep the logo, the house and the products. " + _KEEP
)

_CAMPING = (
    "Marketing photo: a couple camping, batteries and an all-in-one cabinet. "
    "Translate only the white headline across the top. Keep it one line. "
    "'All In One Off Grid Solar System' → 'Автономная солнечная система «всё в одном»'. "
    "Do NOT change text on the batteries or the cabinet, including XD200-12 and "
    "ALL IN ONE SOLAR GENERATOR. Keep the green arrows, people, tent and logo. " + _KEEP
)

_IRAN = (
    "Marketing banner: a solar farm with a green caption band. "
    "Translate only the caption. Keep it one line. "
    "'Iran abundant solar energy' → 'Обильная солнечная энергия Ирана'. "
    "Keep 'солнечная энергия' in the bolder white style of the original 'solar energy'. "
    "Keep www.xindun-power.com exactly. Keep the logo and the solar farm. " + _KEEP
)

_OFFGRID = (
    "Marketing banner: a house with rooftop solar on the left and a dark blue panel on the right. "
    "Translate only the English marketing lines. Do not move the house, car or panels. "
    "On the blue panel keep three stacked lines: "
    "'Design' → 'Проектирование', 'Install' → 'Монтаж', 'Commissioning' → 'Пусконаладка'. "
    "'Residential & Commercial' → 'Для дома и бизнеса'. "
    "The question over the house stays three lines: "
    "'Will an off grid solar system worthwhile' → 'Стоит ли автономная солнечная', "
    "'investment for your home,business,and' → 'система вложений для дома,', "
    "'factories?' → 'бизнеса и заводов?'. "
    "The white badge 'off grid solar backup' → 'автономный солнечный резерв'. "
    "The bottom strip 'Off grid solar system-solar inverter,solar panel,solar controller,battery,etc' → "
    "'Автономная солнечная система: инвертор, панель, контроллер, аккумулятор и др.'. "
    "Keep the logo. " + _KEEP
)

_COUNTRIES = (
    "Photo collage with a beige caption bar. "
    "Translate only the two orange caption lines. Keep two lines. "
    "'XINDUN power off grid solar backup system' → 'Автономная резервная солнечная система XINDUN Power'. "
    "'for more than 63 countries' → 'более чем для 63 стран'. "
    "Keep 'XINDUN Power' in Latin letters. "
    "Do NOT change 'PV COMBINER BOX' or any text on the equipment. "
    "Keep the photographs, people, batteries and the logo. " + _KEEP
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "crisis": "https://www.xindun-power.com/uploadfile/2023/03/09/202303091456432974.jpg",
    "solar": "https://www.xindun-power.com/uploadfile/2023/03/09/202303091457493080.jpg",
    "reasons": "https://www.xindun-power.com/uploadfile/2023/04/08/202304081521582714.jpg",
    "exhibition": "https://www.xindun-power.com/uploadfile/2023/04/08/202304081522575888.jpg",
    "factory_walk": "https://www.xindun-power.com/uploadfile/2023/04/08/202304081525386347.jpg",
    "best": "https://www.xindun-power.com/uploadfile/2023/03/15/202303151442212927.jpg",
    "camping": "https://www.xindun-power.com/uploadfile/2023/03/15/202303151444069978.jpg",
    "iran": "https://www.xindun-power.com/uploadfile/2023/04/14/202304141138506751.jpg",
    "inverters": "https://www.xindun-power.com/uploadfile/2023/04/14/202304141141479252.jpg",
    "factory_line": "https://www.xindun-power.com/uploadfile/2023/04/14/202304141142282288.jpg",
    "offgrid": "https://www.xindun-power.com/uploadfile/2023/03/07/202303071604239993.jpg",
    "countries": "https://www.xindun-power.com/uploadfile/2023/03/07/202303071605468886.jpg",
}

DUOMI_BY_URL = {
    U["crisis"]: _CRISIS,
    U["solar"]: _SOLAR,
    U["reasons"]: _REASONS,
    U["best"]: _BEST,
    U["camping"]: _CAMPING,
    U["iran"]: _IRAN,
    U["offgrid"]: _OFFGRID,
    U["countries"]: _COUNTRIES,
}

IMAGE_SOURCES = [
    [
        _im(U["solar"], "Солнечная энергия — как решить энергетический кризис 2022"),
        _im(U["crisis"], "Как решить энергетический кризис 2022"),
    ],
    [
        _im(U["reasons"], "5 причин выбрать китайского производителя инверторов"),
        _im(U["exhibition"], "Выставка китайских инверторов Xindun Power"),
        _im(U["factory_walk"], "Китайское производство инверторов"),
    ],
    [
        _im(U["best"], "Лучшая автономная система питания всё в одном"),
        _im(U["camping"], "Автономная солнечная система всё в одном"),
    ],
    [
        _im(U["iran"], "Обильная солнечная энергия Ирана"),
        _im(U["inverters"], "Солнечный инвертор Xindun Power"),
        _im(U["factory_line"], "Производственный завод Xindun Power"),
    ],
    [
        _im(U["offgrid"], "Автономная солнечная система с резервным аккумулятором"),
        _im(U["countries"], "Резервная автономная солнечная система Xindun"),
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
