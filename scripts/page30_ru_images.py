#!/usr/bin/env python3
"""Prepare page 30 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for English marketing headlines, product-card captions
and wiring-diagram labels. Factory floors, certificates, installation photos
and plain product shots are compressed only. Product casing text, logos,
port silkscreen and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 30

_KEEP = (
    "Keep arrows, icons, colors, people, products and the background. "
    "Do not move products or people. Do not add objects or labels that are not already in the image. "
    "Do not redesign the poster. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, "
    "product casing text, model numbers, display readings, port silkscreen, CE marks, "
    "Chinese characters, certificates, exhibition booth signs, or the URL xindun-power.com. "
    "Do not change words printed on the product such as ALL IN ONE SOLAR GENERATOR, "
    "SOLAR GENERATOR, HYBRID SOLAR INVERTER, PURE SINE WAVE INVERTER, SOLAR POWER SYSTEM, "
    "or SOLAR POWER INVERTER."
)

_SPEC = (
    "Product sheet with a product photograph on the left and a caption block on the right. "
    "Do not change the photograph, the two-column layout, the green title underline or the bullet dots. "
    "Keep the power-range line of watts or kVA exactly as printed. "
    "Translate only the product title and the bullet lines. "
)


def _card(title_en: str, title_ru: str, extra_lines: list[tuple[str, str]], bullets: list[tuple[str, str]], extra: str = "") -> str:
    lines = [
        _SPEC,
        f"Title '{title_en}' → '{title_ru}'.",
    ]
    for src, dst in extra_lines:
        lines.append(f"Line '{src}' → '{dst}'.")
    for src, dst in bullets:
        lines.append(f"Bullet '{src}' → '{dst}'.")
    if extra:
        lines.append(extra)
    lines.append(_KEEP)
    return " ".join(lines)


_VS = (
    "Three rounded comparison cards on a dark green background. Translate only the three white titles. "
    "'Power Inverter' → 'Силовой инвертор'. "
    "'Solar Inverter' → 'Солнечный инвертор'. "
    "'UPS' → 'ИБП'. "
    "Keep the red VS letters in Latin. "
    "Do NOT change any text printed on the three units. " + _KEEP
)

_MOTOR = (
    "A black cabinet on the left and three callout photos on the right, joined by yellow lines. "
    "Translate only the three green labels. "
    "'Three Phase Motor' → 'Трёхфазный двигатель'. "
    "'Blender' → 'Блендер'. "
    "'Conveyor' → 'Конвейер'. "
    "Keep three labels and the yellow lines. " + _KEEP
)

_HPT = _card(
    "HP PRO-T SOLAR INVERTER",
    "Солнечный инвертор HP PRO-T",
    [("best inverter for home", "лучший инвертор для дома")],
    [
        ("High frequency pure sine wave", "Высокочастотная чистая синусоида"),
        ("Inverter built-in mppt solar charge", "Встроенный солнечный заряд MPPT"),
        ("Compatible with lithium batteries", "Совместим с литиевыми аккумуляторами"),
        ("Can work without/with batteries", "Работает с аккумулятором и без него"),
        ("RS485/WIFI remote monitoring", "Удалённый контроль RS485/WIFI"),
    ],
    "Keep '1KW-8KW' unchanged. Keep MPPT, RS485 and WIFI in Latin letters. "
    "Do NOT change HYBRID SOLAR INVERTER printed on the unit.",
)

_HP = _card(
    "HP PRO SOLAR INVERTER",
    "Солнечный инвертор HP PRO",
    [],
    [
        ("Combines solar energy and grid power", "Объединяет солнечную и сетевую энергию"),
        ("Reduce your reliance on the grid", "Снижает зависимость от сети"),
        ("Battery storage for backup power", "Накопление в аккумуляторе как резерв"),
        ("Intelligent energy management,optimizing the utilization of solar power", "Умное управление энергией и лучшее использование солнца"),
    ],
    "Keep '1kw-8kw' unchanged.",
)

_DP = _card(
    "DP POWER INVERTER",
    "Силовой инвертор DP",
    [],
    [
        ("Pure sine wave output", "Чистая синусоида на выходе"),
        ("Toroidal transformer high efficiency", "Высокий КПД тороидального трансформатора"),
        ("One-button start with an external display screen", "Пуск одной кнопкой с внешним дисплеем"),
        ("Monitor the operation condition in real time", "Контроль работы в реальном времени"),
        ("RS485 communication port/ APP", "Порт связи RS485/APP"),
    ],
    "Keep '1kw-7kw' unchanged. Keep RS485 and APP in Latin letters. "
    "Do NOT change text printed on the inverter or on the external display.",
)

_DA = _card(
    "DA POWER INVERTER",
    "Силовой инвертор DA",
    [],
    [
        ("Optimal power conversion and high efficiency", "Оптимальное преобразование и высокий КПД"),
        ("Wide range of applications, from residential to RV", "Широкий круг задач: от дома до автодома"),
        ("Stable and uninterrupted power supply", "Стабильное бесперебойное питание"),
        ("Easy installation, operation, and monitoring", "Простые установка, работа и контроль"),
    ],
    "Keep '1kw-6kw' unchanged. Do NOT change SOLAR INVERTER printed on the blue panel.",
)

_HDSX = _card(
    "HDSX UPS INVERTER",
    "Инвертор ИБП HDSX",
    [("DC to 3 Phase AC", "Постоянный ток в трёхфазный AC")],
    [
        ("Off grid convert 3 phase to single phase/three phase.", "Автономия: три фазы в одну или в три фазы."),
        ("Built-in pwm or mppt controller", "Встроенный контроллер PWM или MPPT"),
        ("Battery charger,stable voltage, UPS backup power", "Заряд аккумулятора, стабильное напряжение, резерв ИБП"),
        ("Solar charger/AC charger/ generator charger in one.", "Солнечный заряд, заряд от сети и от генератора в одном."),
    ],
    "Keep '4kVA-200kVA' unchanged. Keep PWM, MPPT and AC in Latin letters.",
)

_WD = _card(
    "WD UPS INVERTER",
    "Инвертор ИБП WD",
    [],
    [
        ("Uninterrupted power supply during outages.", "Бесперебойное питание при отключении сети."),
        ("Suitable for various electronic devices.", "Подходит для разной электроники."),
        ("High conversion efficiency for optimal power.", "Высокий КПД для оптимальной мощности."),
        ("Safeguards against voltage fluctuations and power surges.", "Защита от скачков и колебаний напряжения."),
    ],
    "Keep '700w-40kw' unchanged.",
)

_HOUSE = (
    "A house diagram with rooftop panels, a white cabinet and a power pole. "
    "Translate only the three callout labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Solar Generator' → 'Солнечный генератор'. "
    "'Power grid' → 'Электросеть'. "
    "Do NOT change text printed on the white cabinet. " + _KEEP
)

_ESS = (
    "Two all-in-one cabinets in front of an RV, with three icon captions along the bottom. "
    "Translate only the six bottom caption lines. Keep three columns and the plus signs. "
    "'Battery' → 'Аккумулятор'. "
    "'Lithium or Lead-acid Optional' → 'Литий или свинец, по выбору'. "
    "'Solar controller' → 'Солнечный контроллер'. "
    "'MPPT or PWM Optional' → 'MPPT или PWM, по выбору'. "
    "'Inverter' → 'Инвертор'. "
    "'Convert DC to AC' → 'Преобразование DC в AC'. "
    "Keep MPPT, PWM, DC and AC in Latin letters. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR or SOLAR GENERATOR printed on the cabinets. " + _KEEP
)

_WIRE_S = (
    "A compact wiring diagram of two black cabinets. Translate only the English diagram labels. "
    "'INVERTER' → 'ИНВЕРТОР'. "
    "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
    "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
    "'GENERATOR' → 'ГЕНЕРАТОР'. "
    "'AC LOADS' → 'НАГРУЗКА AC'. "
    "'DC LOADS' → 'НАГРУЗКА DC'. "
    "'Fan' → 'Вентилятор'. "
    "'Notebook Computer' → 'Ноутбук'. "
    "'Hair Drier' → 'Фен'. "
    "'Electric kettle' → 'Электрочайник'. "
    "Keep N, L and the plus and minus signs. Keep AC and DC in Latin letters. "
    "Do NOT change SOLAR GENERATOR printed on the right cabinet. " + _KEEP
)

_WIRE_L = (
    "A larger wiring diagram of one white-and-black cabinet. Translate only the English diagram labels. "
    "'DC LOADS' → 'НАГРУЗКА DC'. "
    "'Refrigerator' → 'Холодильник'. "
    "'Electromagnetic furnace' → 'Индукционная плита'. "
    "'Electric hammer' → 'Электромолоток'. "
    "'Air conditioner' → 'Кондиционер'. "
    "'AC LOADS' → 'НАГРУЗКА AC'. "
    "'INVERTER' → 'ИНВЕРТОР'. "
    "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
    "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
    "'GENERATOR' → 'ГЕНЕРАТОР'. "
    "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
    "Each '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
    "The small word 'or' → 'или'. "
    "Keep N, L and the plus and minus signs. Keep AC and DC in Latin letters. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR printed on the cabinet. " + _KEEP
)

_COMPANY = (
    "A factory photo with a green curved band and a white headline. "
    "Translate only the two-line headline. Keep two lines and the question mark. "
    "Line 1 'How To Find The World Best' → 'Как найти лучшую в мире'. "
    "Line 2 'Solar Inverter Company?' → 'компанию солнечных инверторов?'. "
    "Keep the logo and the URL www.xindun-power.com. " + _KEEP
)

_CHARGER = (
    "A marketing banner: five inverter cabinets in front of a house with rooftop panels. "
    "Translate only the blue and black overlay lines. Keep XINDUN in Latin letters. "
    "'XINDUN Inverter plus battery charger' → 'XINDUN: инвертор с зарядным устройством'. "
    "'high frequency and low frequency' → 'высокая и низкая частота'. "
    "'Solar/mains/generator charging' → 'заряд от солнца, сети и генератора'. "
    "Keep the black URL badge www.xindun-power.com and the logo. "
    "Do NOT change text printed on the cabinets. " + _KEEP
)

_DP_WIRE = (
    "A wiring diagram of a silver low-frequency inverter. Translate only the English diagram labels. "
    "The misspelled label 'SoarI Panels' → 'Солнечные панели'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'DC Loads' → 'Нагрузка DC'. "
    "'Neutral Wire' → 'Нейтраль' in both places. "
    "'Live Wire' → 'Фаза' in both places. "
    "'Ground Wire' → 'Заземление'. "
    "'Power Grid or Generator' → 'Сеть или генератор'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "'Loads for each AC output socket should not exceed 1KW' → 'Нагрузка каждой розетки AC не более 1 кВт'. "
    "Keep DC, AC and 1KW numerals readable. "
    "Do NOT change PURE SINE WAVE INVERTER or other text printed on the unit. " + _KEEP
)

_DA_WIRE = (
    "A block wiring diagram of a blue inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Power Grid' → 'Электросеть'. "
    "'Generator' → 'Генератор'. "
    "'or' → 'или'. "
    "'Solar Controller' → 'Солнечный контроллер'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "Keep AC in Latin letters. Do NOT change text printed on the blue inverter. " + _KEEP
)

_LS_WIRE = (
    "A wiring diagram of a blue wall inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'DC Loads' → 'Нагрузка DC'. "
    "'AC Input' → 'Вход AC'. "
    "'AC Output' → 'Выход AC'. "
    "'Battery' → 'Аккумулятор'. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "Keep N, L, PE, AC and DC in Latin letters. "
    "Do NOT change SOLAR POWER SYSTEM printed on the unit or the text printed on the battery. " + _KEEP
)

_HP_WIRE = (
    "A wiring diagram of a white hybrid inverter. Translate only the English diagram labels. "
    "'Power Grid' → 'Электросеть'. "
    "'OR' → 'ИЛИ'. "
    "'Generator' → 'Генератор'. "
    "'AC INPUT' → 'ВХОД AC'. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Battery' → 'Аккумулятор'. "
    "'AC OUTPUT' → 'ВЫХОД AC'. "
    "'Refrigerator' → 'Холодильник'. "
    "'Air conditioner' → 'Кондиционер'. "
    "'Washing machine' → 'Стиральная машина'. "
    "'TV' → 'ТВ'. "
    "'Rice cooker' → 'Рисоварка'. "
    "Keep AC in Latin letters. "
    "Do NOT change HYBRID SOLAR INVERTER printed on the unit. " + _KEEP
)

_WD_WIRE = (
    "A rear-view wiring diagram of a yellow-and-white cabinet. Translate only the English diagram labels. "
    "'DC Load' → 'Нагрузка DC'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Battery' → 'Аккумулятор'. "
    "'Utility Power' → 'Сеть'. "
    "'Ground Line' → 'Заземление'. "
    "Keep N, L, DC and AC in Latin letters. "
    "Do NOT change the model text printed on the batteries. " + _KEEP
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "vs": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202102920l6AYm7.jpg",
    "room": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202103019nSosPC.jpg",
    "motor": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202103104p6IiG5.jpg",
    "family": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202103137NOGi6v.jpg",
    "hpt": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202103229IGhVMw.jpg",
    "hp": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202103228GUspD9.jpg",
    "dp": "https://www.xindun-power.com/uploadfile/2023/12/02/202312021032522gSNnj.jpg",
    "da": "https://www.xindun-power.com/uploadfile/2023/12/02/2023120210325272luFi.jpg",
    "hdsx": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202103316mp9bSU.jpg",
    "wd": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202103316jzAC34.jpg",
    "factory1": "https://www.xindun-power.com/uploadfile/2023/12/02/202312021034313aRLQZ.jpg",
    "factory2": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202103449JZPGKx.jpg",
    "pp_hero": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202094457UJs1xO.jpg",
    "pp1": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202094911bEUQ3K.jpg",
    "pp2": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202094937u8BkEU.jpg",
    "pp3": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202095152bvlTCI.jpg",
    "pp4": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202095153yYpTEO.jpg",
    "house": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202095254W4rR9C.jpg",
    "ess": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202095322C4rutY.jpg",
    "wire_s": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202095356J82W9O.jpg",
    "wire_l": "https://www.xindun-power.com/uploadfile/2023/12/02/202312020954086bjUxX.jpg",
    "office": "https://www.xindun-power.com/uploadfile/2023/12/02/202312020955204Tt2yl.jpg",
    "pp_fac1": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202095550rwHEbo.jpg",
    "pp_fac2": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202095603Bo7Mcl.jpg",
    "pump": "https://www.xindun-power.com/uploadfile/2023/07/01/202307011059343904.jpg",
    "ls": "https://www.xindun-power.com/uploadfile/2023/07/01/202307011122198647.jpg",
    "hpplus": "https://www.xindun-power.com/uploadfile/2023/07/01/202307011352406489.jpg",
    "wd_p": "https://www.xindun-power.com/uploadfile/2023/07/01/202307011135548953.jpg",
    "ess_p": "https://www.xindun-power.com/uploadfile/2023/07/01/202307011141166086.jpg",
    "pump_fac": "https://www.xindun-power.com/uploadfile/2023/07/01/202307011358212842.jpg",
    "field": "https://www.xindun-power.com/uploadfile/2023/07/01/202307011359446625.jpg",
    "install": "https://www.xindun-power.com/uploadfile/2023/07/10/202307101647443367.jpg",
    "best": "https://www.xindun-power.com/uploadfile/2023/06/17/202306171635328433.jpg",
    "showroom": "https://www.xindun-power.com/uploadfile/2023/06/17/202306171636144952.jpg",
    "best_fac": "https://www.xindun-power.com/uploadfile/2023/06/17/202306171637132852.jpg",
    "certs": "https://www.xindun-power.com/uploadfile/2023/06/17/202306171637469191.jpg",
    "lineup": "https://www.xindun-power.com/uploadfile/2023/06/20/202306200906244066.jpg",
    "team": "https://www.xindun-power.com/uploadfile/2023/06/17/202306171638563493.jpg",
    "chg": "https://www.xindun-power.com/uploadfile/2023/07/03/20230703163423MVhDTs.jpg",
    "dp_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031540377111.jpg",
    "dp_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031540555074.jpg",
    "da_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031637472291.jpg",
    "da_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031423013770.jpg",
    "ls_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031538551338.jpg",
    "ls_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031539161266.jpg",
    "hpt_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031535554192.jpg",
    "hpt_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031536142680.jpg",
    "wd_c": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031641324405.jpg",
    "wd_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031641501794.jpg",
    "chg_off": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031542354449.jpg",
    "chg_fac": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031651008641.jpg",
}

DUOMI_BY_URL = {
    U["vs"]: _VS,
    U["motor"]: _MOTOR,
    U["hpt"]: _HPT,
    U["hp"]: _HP,
    U["dp"]: _DP,
    U["da"]: _DA,
    U["hdsx"]: _HDSX,
    U["wd"]: _WD,
    U["house"]: _HOUSE,
    U["ess"]: _ESS,
    U["wire_s"]: _WIRE_S,
    U["wire_l"]: _WIRE_L,
    U["best"]: _COMPANY,
    U["chg"]: _CHARGER,
    U["dp_w"]: _DP_WIRE,
    U["da_w"]: _DA_WIRE,
    U["ls_w"]: _LS_WIRE,
    U["hpt_w"]: _HP_WIRE,
    U["wd_w"]: _WD_WIRE,
}

IMAGE_SOURCES = [
    [
        _im(U["vs"], "Силовой инвертор, солнечный инвертор и ИБП"),
        _im(U["room"], "Разница между солнечным и электрическим инвертором"),
        _im(U["motor"], "Разница между солнечным инвертором и ИБП"),
        _im(U["family"], "Разница между силовым инвертором и ИБП"),
        _im(U["hpt"], "Солнечный инвертор Xindun HP PRO-T"),
        _im(U["hp"], "Солнечный инвертор Xindun HP PRO"),
        _im(U["dp"], "Силовой инвертор Xindun DP"),
        _im(U["da"], "Силовой инвертор Xindun DA"),
        _im(U["hdsx"], "ИБП Xindun HDSX"),
        _im(U["wd"], "ИБП Xindun WD"),
        _im(U["factory1"], "Завод электрических инверторов Xindun"),
        _im(U["factory2"], "Китайский производитель электрических инверторов Xindun Power"),
    ],
    [
        _im(U["pp_hero"], "Готовое решение: автономная солнечная система «подключи и работай»"),
        _im(U["pp1"], "Солнечная система «подключи и работай»"),
        _im(U["pp2"], "Комплект «подключи и работай»"),
        _im(U["pp3"], "Лучшие комплекты солнечных панелей «подключи и работай»"),
        _im(U["pp4"], "Солнечные системы «подключи и работай»"),
        _im(U["house"], "Солнечные энергосистемы «подключи и работай»"),
        _im(U["ess"], "Солнечный генератор «подключи и работай»"),
        _im(U["wire_s"], "Инверторная система «подключи и работай»"),
        _im(U["wire_l"], "Фотоэлектрическая система «подключи и работай»"),
        _im(U["office"], "Компания автономных солнечных систем «подключи и работай» Xindun Power"),
        _im(U["pp_fac1"], "Завод солнечных систем «подключи и работай» Xindun"),
        _im(U["pp_fac2"], "Завод солнечных систем «подключи и работай» Xindun Power"),
    ],
    [
        _im(U["pump"], "Инвертор солнечного насоса и солнечный инвертор для водяного насоса"),
        _im(U["ls"], "Инвертор солнечного насоса LS"),
        _im(U["hpplus"], "Инвертор солнечного насоса HP PLUS"),
        _im(U["wd_p"], "Солнечный инвертор для водяного насоса WD"),
        _im(U["ess_p"], "Солнечный инвертор для водяного насоса ESS"),
        _im(U["pump_fac"], "Производитель инверторов солнечного насоса"),
        _im(U["field"], "Пример солнечного инвертора для водяного насоса"),
        _im(U["install"], "Монтаж солнечного инвертора для водяного насоса"),
    ],
    [
        _im(U["best"], "Как найти лучшую в мире компанию солнечных инверторов"),
        _im(U["showroom"], "Лучшая в мире компания солнечных инверторов Xindun"),
        _im(U["best_fac"], "Лучшая в мире инверторная компания Xindun"),
        _im(U["certs"], "Технические сертификаты лучшего солнечного инвертора"),
        _im(U["lineup"], "Лучший в мире солнечный инвертор Xindun"),
        _im(U["team"], "Сотрудничество с лучшей компанией солнечных инверторов Xindun"),
    ],
    [
        _im(U["chg"], "Инвертор Xindun с зарядным устройством аккумулятора"),
        _im(U["dp_p"], "Инвертор DP Xindun с зарядным устройством аккумулятора"),
        _im(U["dp_w"], "Схема подключения инвертора DP Xindun с зарядным устройством"),
        _im(U["da_p"], "Инвертор DA Xindun с зарядным устройством аккумулятора"),
        _im(U["da_w"], "Схема подключения инвертора DA Xindun с зарядным устройством"),
        _im(U["ls_p"], "Инвертор LS Xindun с зарядным устройством аккумулятора"),
        _im(U["ls_w"], "Схема подключения инвертора LS Xindun с зарядным устройством"),
        _im(U["hpt_p"], "Инвертор HP PRO-T Xindun с зарядным устройством аккумулятора"),
        _im(U["hpt_w"], "Схема подключения инвертора HP PRO-T Xindun с зарядным устройством"),
        _im(U["wd_c"], "Инвертор WD Xindun с зарядным устройством аккумулятора"),
        _im(U["wd_w"], "Схема подключения инвертора WD Xindun с зарядным устройством"),
        _im(U["chg_off"], "Производитель инверторов Xindun с зарядным устройством аккумулятора"),
        _im(U["chg_fac"], "Поставщик инверторов Xindun с зарядным устройством аккумулятора"),
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
