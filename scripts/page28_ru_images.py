#!/usr/bin/env python3
"""Prepare page 28 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for English marketing headlines and diagram labels.
Factory floors, installation photos and plain product shots are compressed only.
Product casing text, logos and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 28

_KEEP = (
    "Keep arrows, icons, colors, people, products and the background. "
    "Do not move products or people. Do not add objects or labels that are not already in the image. "
    "Do not redesign the poster. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, ZAMDON logo, "
    "product casing text, model numbers, display readings, Chinese characters, certificates, "
    "or the URL www.xindun-power.com. "
    "Do not change words printed on the product such as ALL IN ONE SOLAR GENERATOR, "
    "MPPT Solar Charge Controller, XD65-12, 12V-150Ah, or POWER."
)

_UPS = (
    "Marketing comparison banner: black left side, red right side, a white cabinet and a black cabinet, "
    "large white VS in the center. Translate only the two black rounded labels. "
    "Left label 'UPS single phase' → 'Однофазный ИБП'. "
    "Right label 'UPS three phase' → 'Трёхфазный ИБП'. "
    "Keep the word VS in Latin letters. Keep exactly those two labels and do not add a third headline. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR or any text on the cabinets. Keep the logo. " + _KEEP
)

_BATT = (
    "Blue infographic with two batteries on the left and a numbered list on the right. "
    "Translate only the white overlay text. Keep the title on exactly two lines: "
    "'Difference between lithium ion battery' → 'Разница между литий-ионным' and "
    "'and lead acid battery' → 'и свинцово-кислотным аккумулятором'. "
    "The caption under the upper battery 'LEAD ACID' → 'СВИНЦОВЫЙ'. "
    "The caption under the lower battery 'LITHIUM ION' → 'ЛИТИЙ-ИОННЫЙ'. "
    "Keep the six numbered lines and do not merge or drop any line: "
    "'1)Service life,cost and efficiency' → '1) Срок службы, цена и КПД'. "
    "'2)Safety' → '2) Безопасность'. "
    "'3)Different energy densities' → '3) Разная плотность энергии'. "
    "'4)Cycle life' → '4) Циклический ресурс'. "
    "'5)Battery capacity' → '5) Ёмкость аккумулятора'. "
    "'6)Environmental protection' → '6) Экологичность'. "
    "Do NOT change text printed on the batteries, including XD65-12, 12V-150Ah, ZAMDON, CE, "
    "or the xindun and ZAMDON logos. " + _KEEP
)

_ESS_HOME = (
    "Living-room marketing banner with a white cabinet on the right. "
    "Translate only the three white headline lines. Keep three lines. "
    "Line 1 'ESS Portable' → 'Портативный ESS'. "
    "Line 2 'solar generator' → 'солнечный генератор'. "
    "Line 3 'for off-grid living' → 'для автономной жизни'. "
    "Keep the blue badge '1500W-7000W' unchanged. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR on the cabinet. Keep the logo, sofa, plant and cabinet. " + _KEEP
)

_ESS_CAMP = (
    "Camping marketing banner with people, a tent, a fire and a white cabinet. "
    "Translate only the three white headline lines. Keep three lines. "
    "Line 1 'ESS Portable' → 'Портативный ESS'. "
    "Line 2 'solar generator' → 'солнечный генератор'. "
    "Line 3 'off-grid' → 'автономный'. "
    "Keep the blue badge '300W-1000W' unchanged. "
    "Do NOT change text printed on the cabinet. Keep the people, tent, fire, lights and logo. " + _KEEP
)

_LEBANON = (
    "Photo collage with a green band across the middle. "
    "Translate only the text on the green band. Keep it one line. "
    "'Hybrid Solar Inverter Lebanon for Varied Uses' → 'Гибридный солнечный инвертор для Ливана'. "
    "Keep the four photographs, the yellow inverters, the robot arm, the living room, the towers "
    "and the industrial walkway. Do NOT change text printed on the inverters. Keep the logo. " + _KEEP
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "ups": "https://www.xindun-power.com/uploadfile/2023/03/29/202303291724252716.jpg",
    "factory3": "https://www.xindun-power.com/uploadfile/2023/03/29/202303291726007719.jpg",
    "batt_chart": "https://www.xindun-power.com/uploadfile/2023/02/16/202302161356386983.jpg",
    "batt_photo": "https://www.xindun-power.com/uploadfile/2023/02/16/202302161358441154.jpg",
    "ess_home": "https://www.xindun-power.com/uploadfile/2023/02/11/202302111559127364.jpg",
    "ess_camp": "https://www.xindun-power.com/uploadfile/2023/02/11/202302111601173337.jpg",
    "lebanon": "https://www.xindun-power.com/uploadfile/2023/04/15/202304151024367704.jpg",
    "lebanon_roof": "https://www.xindun-power.com/uploadfile/2023/04/15/202304151026002002.jpg",
    "lebanon_case": "https://www.xindun-power.com/uploadfile/2023/04/15/202304151028414576.jpg",
    "yemen": "https://www.xindun-power.com/uploadfile/2023/04/06/202304061553474771.jpg",
    "yemen_rd": "https://www.xindun-power.com/uploadfile/2023/04/06/202304061557224540.jpg",
    "yemen_factory": "https://www.xindun-power.com/uploadfile/2023/04/06/202304061638362038.jpg",
}

DUOMI_BY_URL = {
    U["ups"]: _UPS,
    U["batt_chart"]: _BATT,
    U["ess_home"]: _ESS_HOME,
    U["ess_camp"]: _ESS_CAMP,
    U["lebanon"]: _LEBANON,
}

IMAGE_SOURCES = [
    [
        _im(U["ups"], "Однофазный и трёхфазный ИБП"),
        _im(U["factory3"], "Завод трёхфазных инверторов Xindun"),
    ],
    [
        _im(U["batt_photo"], "Разница между солнечным литий-ионным и свинцово-кислотным аккумулятором"),
        _im(U["batt_chart"], "Разница между литий-ионным и свинцово-кислотным аккумулятором"),
    ],
    [
        _im(U["ess_camp"], "Автономный солнечный генератор"),
        _im(U["ess_home"], "Лучший солнечный генератор для автономной жизни"),
    ],
    [
        _im(U["lebanon"], "Гибридный солнечный инвертор для Ливана"),
        _im(U["lebanon_roof"], "Пример гибридной солнечной системы Xindun Power"),
        _im(U["lebanon_case"], "Пример гибридной солнечной системы Xindun Power"),
    ],
    [
        _im(U["yemen"], "Рынок домашних солнечных инверторов Йемена"),
        _im(U["yemen_rd"], "Разработка и проектирование китайского солнечного инвертора"),
        _im(U["yemen_factory"], "Завод китайских солнечных и домашних инверторов"),
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
