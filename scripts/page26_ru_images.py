#!/usr/bin/env python3
"""Prepare page 26 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for marketing headlines and diagram captions.
Product casing text, logos, Chinese photo captions and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 26

_KEEP = (
    "Keep arrows, icons, colors, people, products and the background. "
    "Do not move products or people. Do not add objects or labels that are not already in the image. "
    "Do not redesign the poster. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, product casing text, "
    "model numbers, display readings, Chinese characters on photos, certificates or walls, "
    "or the URL www.xindun-power.com / xindun-power.com. "
    "Do not change words printed on the product such as SOLAR INVERTER, ALL IN ONE SOLAR GENERATOR, "
    "PV COMBINER BOX, DC-AC, or POWER."
)

_WHOLESALE = (
    "Marketing banner: several inverter cabinets and a solar array in front of Earth. "
    "Translate only the green headline. "
    "'Solar inverter wholesale suppliers - Xindun China' → "
    "'Оптовые поставщики солнечных инверторов — Xindun China'. "
    "Keep it one line. Keep 'Xindun China' exactly. " + _KEEP
)

_COOP = (
    "Marketing collage: a dark blue text panel on the left and customer photos on the right. "
    "Translate only the English marketing lines on the blue and white panels. "
    "'Cooperation with global customers' → 'Сотрудничество с клиентами по всему миру'. "
    "'-Solar inverter manufacturer' → '-Производитель солнечных инверторов'. "
    "Keep 'Xindun China' exactly, including the line break. "
    "Do not change the photographs, Chinese signs, certificates or the logo. " + _KEEP
)

_UPS_HERO = (
    "Marketing banner: black UPS cabinets in a blue server aisle. "
    "Translate only the white headline. Keep 'XINDUN Power' exactly. "
    "'UPS system' → 'система ИБП'. "
    "The line must read 'XINDUN Power система ИБП' and stay one line. " + _KEEP
)

_UPS_BACKUP = (
    "Marketing banner: a control-room photo on the left and a pale text panel on the right. "
    "Translate only the three black headline lines. "
    "'UPS system' → 'Система ИБП'. "
    "'for backup' → 'для резервного'. "
    "'power' → 'питания'. "
    "Keep the three-line layout. Keep xindun-power.com and the logo exactly. " + _KEEP
)

_STANDALONE_DIAGRAM = (
    "Two wiring diagrams under one black headline on a white background. "
    "Translate only the headline and the English diagram labels. "
    "Headline 'What is Standalone Solar Electric System?' → "
    "'Что такое автономная солнечная электросистема?'. Keep the question mark and two lines. "
    "'Solar Array' → 'Солнечная батарея'. 'DC Current' → 'Постоянный ток'. "
    "'Charge Controller' → 'Контроллер заряда'. 'Battery' → 'Аккумулятор'. "
    "'Inverter' → 'Инвертор'. 'AC loads in home' → 'Нагрузка AC дома'. "
    "'Solar Irradiance' → 'Солнечное излучение'. 'Module' → 'Модуль'. "
    "'AC Loads' → 'Нагрузка AC'. 'DC Loads' → 'Нагрузка DC'. "
    "Keep the house, sun, arrows, panels and both circuit layouts. " + _KEEP
)

_HOW_TO = (
    "Marketing banner: orange headline on a white panel, a house with rooftop solar on the right. "
    "Translate only the orange headline and keep five short lines plus the question mark. "
    "'HOW TO USE' → 'КАК ПОЛЬЗОВАТЬСЯ'. "
    "'STAND ALONE' → 'АВТОНОМНОЙ'. "
    "'SOLAR' → 'СОЛНЕЧНОЙ'. "
    "'PHOTOVOLTAIC' → 'ФОТОЭЛЕКТРИЧЕСКОЙ'. "
    "'SYSTEM?' → 'СИСТЕМОЙ?'. "
    "Together: 'КАК ПОЛЬЗОВАТЬСЯ АВТОНОМНОЙ СОЛНЕЧНОЙ ФОТОЭЛЕКТРИЧЕСКОЙ СИСТЕМОЙ?'. "
    "Keep the orange color, the green diagonal bars, the family, the logo and xindun-power.com. " + _KEEP
)

_HOME_WHAT = (
    "Illustrated banner: green headline on the left, battery, panels, wind turbine and an electric car on the right. "
    "Translate only the green headline and keep the lowercase style and the question mark. "
    "'what is the home solar battery system?' → 'что такое домашняя солнечная аккумуляторная система?'. "
    "Keep it four lines. Keep the logo and xindun-power.com. " + _KEEP
)

_HOME_HERO = (
    "Marketing photo: a house at dusk with inverters in the foreground. "
    "Translate only the gold headline. "
    "'Home solar battery storage system' → 'Домашняя солнечная аккумуляторная система'. "
    "Keep it one line. Keep the house, people, products and the logo. " + _KEEP
)

_OFFGRID_DIAGRAM = (
    "Wide diagram: blue headline and three bullets on the left, a house section on the right. "
    "Translate only the English marketing and diagram labels. "
    "'OFF-GRID' → 'АВТОНОМНАЯ'. 'SOLAR SYSTEM' → 'СОЛНЕЧНАЯ СИСТЕМА'. "
    "'No access to the utility grid' → 'Нет доступа к электросети'. "
    "'Become energy self-sufficient' → 'Энергетическая независимость'. "
    "'Uninterrupted Power Supply' → 'Бесперебойное питание'. "
    "Keep the leading dashes. "
    "'Smart module' → 'Умный модуль'. 'Controller' → 'Контроллер'. "
    "'Battery' → 'Аккумулятор'. 'Inverter' → 'Инвертор'. "
    "'Netmeter' → 'Счётчик'. Keep the short badge 'EV' unchanged. "
    "Keep the house, appliances, orange wires and the logo. " + _KEEP
)

_PACKAGES = (
    "Marketing banner: solar panels and inverters on the left, a four-line headline on the right. "
    "Translate only that headline and keep four lines. "
    "Line 1 'Off-grid' → 'Автономные'. "
    "Line 2 'solar system' stays on the green highlight → 'солнечные системы'. "
    "Line 3 'packages with' → 'комплекты с'. "
    "Line 4 'Batteries' → 'аккумуляторами'. "
    "Keep the orange and green highlight colors. "
    "Do NOT change 'PV COMBINER BOX' or any text printed on the products. "
    "Keep the logo and xindun-power.com. " + _KEEP
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "wholesale": "https://www.xindun-power.com/uploadfile/2023/02/21/202302210857066018.jpg",
    "coop": "https://www.xindun-power.com/uploadfile/2023/02/21/202302210900061382.jpg",
    "ups_hero": "https://www.xindun-power.com/uploadfile/2023/03/01/202303010956132791.jpg",
    "ups_backup": "https://www.xindun-power.com/uploadfile/2023/03/01/202303010952503720.jpg",
    "standalone_diagram": "https://www.xindun-power.com/uploadfile/2023/02/06/202302061413004734.jpg",
    "how_to": "https://www.xindun-power.com/uploadfile/2023/02/06/202302061416066189.jpg",
    "home_what": "https://www.xindun-power.com/uploadfile/2023/02/28/202302281418456709.jpg",
    "home_hero": "https://www.xindun-power.com/uploadfile/2023/02/28/202302281421485337.jpg",
    "offgrid_diagram": "https://www.xindun-power.com/uploadfile/2023/02/07/202302071735314236.jpg",
    "packages": "https://www.xindun-power.com/uploadfile/2023/02/07/202302071729424YiI6s.jpg",
}

DUOMI_BY_URL = {
    U["wholesale"]: _WHOLESALE,
    U["coop"]: _COOP,
    U["ups_hero"]: _UPS_HERO,
    U["ups_backup"]: _UPS_BACKUP,
    U["standalone_diagram"]: _STANDALONE_DIAGRAM,
    U["how_to"]: _HOW_TO,
    U["home_what"]: _HOME_WHAT,
    U["home_hero"]: _HOME_HERO,
    U["offgrid_diagram"]: _OFFGRID_DIAGRAM,
    U["packages"]: _PACKAGES,
}

IMAGE_SOURCES = [
    [
        _im(U["coop"], "Поставщики солнечных инверторов Xindun"),
        _im(U["wholesale"], "Оптовые поставщики солнечных инверторов"),
    ],
    [
        _im(U["ups_hero"], "Разница между ИБП и инвертором"),
        _im(U["ups_backup"], "Система ИБП для резервного питания"),
    ],
    [
        _im(U["how_to"], "Как пользоваться автономной солнечной фотоэлектрической системой"),
        _im(U["standalone_diagram"], "Автономная фотоэлектрическая система"),
    ],
    [
        _im(U["home_hero"], "Домашняя солнечная система накопления"),
        _im(U["home_what"], "Домашняя солнечная аккумуляторная система"),
    ],
    [
        _im(U["packages"], "Комплекты автономных солнечных систем с аккумуляторами"),
        _im(U["offgrid_diagram"], "Автономная солнечная система с аккумуляторами"),
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
