#!/usr/bin/env python3
"""Prepare page 22 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for English marketing headlines and diagram labels.
Product photos, factory and exhibition shots, and certificates are compressed only.
Product casing text, logos and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 22

_KEEP = (
    "Keep arrows, wires, icons, colors and the background. Do not move products. "
    "Do not add objects or labels that are not already in the image. Do not redesign. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, product casing text, "
    "model numbers, CE marks, display readings, button silkscreen, terminal letters, "
    "or words printed on the product such as HYBRID SOLAR INVERTER, Low Frequency Inverter, "
    "Low Frequency PV Inverter, Pure Sine Wave, ENERGY STORAGE SYSTEM, "
    "ALL IN ONE SOLAR GENERATOR, STORAGE Power Inverter, LifePo4 Lithium Battery, "
    "or Pv Combiner."
)

_HFP = (
    "Wiring diagram of a white hybrid inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Battery' → 'Аккумулятор'. "
    "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
    "'Electric Meter' → 'Электросчётчик'. "
    "'AC Loads' → 'Нагрузки AC' wherever it appears. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "The gold line on the inverter must stay 'HYBRID SOLAR INVERTER'. " + _KEEP
)

_HFP_S = (
    "Wiring diagram of an HFP-S hybrid inverter with two AC outputs. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
    "'Power Grid' → 'Электросеть'. "
    "'Electric Meter' → 'Электросчётчик'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "'Uninterrupted Power Supply(Main output)' → 'Бесперебойное питание (основной выход)'. "
    "'Uninterrupted Power Supply(Second output)' → 'Бесперебойное питание (второй выход)'. "
    "Also translate the same phrases if the parentheses say Main Output or Second Output. "
    "Keep red dotted arrows and icons. " + _KEEP
)

_HFP_C = (
    "Wiring diagram of an HFP-C hybrid inverter with a green RGB ring. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
    "'Power Grid' → 'Электросеть'. "
    "'Electric Meter' → 'Электросчётчик'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "If present, 'Uninterrupted Power Supply(Main output)' → 'Бесперебойное питание (основной выход)' "
    "and 'Uninterrupted Power Supply(Second output)' → 'Бесперебойное питание (второй выход)'. "
    "Keep the green ring and red dotted arrows. " + _KEEP
)

_HF = (
    "Wide wiring diagram of a blue hybrid inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
    "'Battery' → 'Аккумулятор'. "
    "'Electric Meter' → 'Электросчётчик'. "
    "'Power Grid' → 'Электросеть'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Do not change text printed on the blue unit. " + _KEEP
)

_ES = (
    "Wiring diagram of a white storage inverter with solar panels on the left. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Solar On/Off Grid Inverter' → 'Сетевой и автономный солнечный инвертор'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'Power Grid' → 'Электросеть'. "
    "'Electric Meter' → 'Электросчётчик'. "
    "'AC loads' → 'Нагрузки AC'. "
    "'Generator' → 'Генератор'. "
    "'Uninterrupted Power Supply' → 'Бесперебойное питание'. "
    "Do NOT change the word STORAGE printed on the inverter. " + _KEEP
)

_BANNER = (
    "Marketing banner of several white hybrid inverters on a pale background with a green circle. "
    "Translate only the white headline on the green ribbon: "
    "'Top Hybrid Solar Inverter Manufacturer In The World' → "
    "'Ведущий производитель гибридных солнечных инверторов в мире'. "
    "Keep the two-line ribbon. Keep the green badge '1~25KW' unchanged, including the arrow. "
    "Do NOT change 'STORAGE Power Inverter' on the tall cabinet or gold text on the smaller units. "
    + _KEEP
)

_LF_PUMP = (
    "Wiring diagram of a white wall inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Utility Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Battery' → 'Аккумулятор'. "
    "'AC Output' → 'Выход AC'. "
    "'Laptop' → 'Ноутбук'. "
    "'Printer' → 'Принтер'. "
    "'TV' → 'Телевизор'. "
    "'Fans' → 'Вентиляторы'. "
    "'Water pump' → 'Водяной насос'. "
    "Do not change text printed on the white unit. " + _KEEP
)

_LF_LIGHT = (
    "Wiring diagram of a white wall inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Utility Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Battery' → 'Аккумулятор'. "
    "'AC Output' → 'Выход AC'. "
    "'Laptop' → 'Ноутбук'. "
    "'Printer' → 'Принтер'. "
    "'TV' → 'Телевизор'. "
    "'Fans' → 'Вентиляторы'. "
    "'Light' → 'Свет'. "
    "Do not change text printed on the white unit. " + _KEEP
)

_DF = (
    "Wiring diagram of a white wall inverter with solar panels at the upper left. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'AC Output' → 'Выход AC'. "
    "'Refrigerator' → 'Холодильник'. "
    "'Fan heater' → 'Тепловентилятор'. "
    "'Air conditioner' → 'Кондиционер'. "
    "'Heater' → 'Обогреватель'. "
    "'Percussion drill' → 'Перфоратор'. "
    "'AC Input' → 'Вход AC'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Battery' → 'Аккумулятор'. "
    "Do not change text printed on the inverter. " + _KEEP
)

_WF = (
    "Wiring diagram of a white wall inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'AC Output' → 'Выход AC'. "
    "'Laptop' → 'Ноутбук'. "
    "'Printer' → 'Принтер'. "
    "'TV' → 'Телевизор'. "
    "'Fans' → 'Вентиляторы'. "
    "'Water pump' → 'Водяной насос'. "
    "'AC Input' → 'Вход AC'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Battery' → 'Аккумулятор'. "
    "Do not change text printed on the white unit. " + _KEEP
)

_LS_BLUE = (
    "Wiring diagram of a blue wall inverter. Translate only the English diagram labels. "
    "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
    "'AC INPUT' → 'ВХОД AC'. "
    "'Generator' → 'Генератор'. "
    "'AC OUTPUT' → 'ВЫХОД AC'. "
    "'Laptop' → 'Ноутбук'. "
    "'Printer' → 'Принтер'. "
    "'LAMP' → 'ЛАМПА'. "
    "'PHONE' → 'ТЕЛЕФОН'. "
    "'FAN' → 'ВЕНТИЛЯТОР'. "
    "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
    "Also translate the same words if they are in title case. "
    "Do not change text printed on the blue inverter. " + _KEEP
)

_LS_LOADS = (
    "Wiring diagram of a blue wall inverter with icons of loads. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'DC Loads' → 'Нагрузки DC'. "
    "'AC Input' → 'Вход AC'. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Battery' → 'Аккумулятор'. "
    "'AC Output' → 'Выход AC'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Do not change text printed on the blue unit. " + _KEEP
)

_WD = (
    "Wiring diagram of a white low-frequency inverter with an orange solar controller. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Solar Controller' → 'Солнечный контроллер'. "
    "'Battery' → 'Аккумулятор'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Do not change text printed on the inverter or the orange controller. " + _KEEP
)

_ESS_PORTS = (
    "Annotated photo of a white all-in-one generator, front and back, with green callout lines. "
    "Translate only the English callout labels. "
    "'LED Indicator' → 'Светодиод'. "
    "'LCD Display' → 'Дисплей'. "
    "'12VDC Output' → 'Выход 12 В DC'. "
    "'USB 5VDC Output' → 'Выход USB 5 В DC'. "
    "'AC Output Socket' → 'Розетка AC'. "
    "'DC Output Switch' → 'Выключатель выхода DC'. "
    "'AC Input / Output Switch' → 'Переключатель входа/выхода AC'. "
    "'AC INPUT/OUTPUT SOLAR INPUT Terminal Block' → 'Клеммы входа/выхода AC и входа от солнца'. "
    "'Battery Switch' → 'Выключатель аккумулятора'. "
    "'RS232 Communication Interface' → 'Интерфейс связи RS232'. "
    "'RS485 Communication Interface' → 'Интерфейс связи RS485'. "
    "'Spare Battery' → 'Запасной аккумулятор'. "
    "Keep the green lines and the xindun logo. " + _KEEP
)

_ESS_FRONT = (
    "Front view of a white lithium unit with green callout lines. "
    "Translate only the English callout labels. "
    "'LCD Display' → 'Дисплей'. "
    "'Function keys' → 'Функциональные кнопки'. "
    "'Inverter Switch' → 'Выключатель инвертора'. "
    "'Up keys' → 'Кнопка вверх'. "
    "'Down keys' → 'Кнопка вниз'. "
    "Do not change the xindun GREENPOWER logo or the numbers on the screen. " + _KEEP
)

_ESS_SIDE = (
    "Rear views of a tall white-and-black unit with green callout lines. "
    "Translate only the English callout labels. "
    "'Handle' → 'Ручка'. "
    "'Battery Switch' → 'Выключатель аккумулятора'. "
    "'DC Output Switch' → 'Выключатель выхода DC'. "
    "'WiFi/GPRS' → 'WiFi/GPRS'. "
    "'RS485' → 'RS485'. "
    "Keep WiFi/GPRS and RS485 as those abbreviations. "
    "Do not change silkscreen on the terminals. " + _KEEP
)

_WF_TROLLEY = (
    "Wiring diagram of a tall wheeled inverter. Translate only the English overlay labels. "
    "'PV Input' → 'Вход PV'. "
    "'AC Input' → 'Вход AC'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Pure sine wave' → 'Чистая синусоида'. "
    "'Computer/TV' → 'Компьютер/ТВ'. "
    "'High-power Appliances' → 'Мощные приборы'. "
    "'Household Appliances' → 'Бытовые приборы'. "
    "'Lead Acid/Lithium Batteries' → 'Свинцовые/литиевые аккумуляторы'. "
    "Do NOT change 'Low Frequency Inverter' printed on the cabinet. " + _KEEP
)

_ESS_WHITE = (
    "Wiring diagram of a white all-in-one unit. Translate only the English diagram labels. "
    "'Solar Panel' → 'Солнечная панель'. "
    "'AC Output' → 'Выход AC'. "
    "'Laptop' → 'Ноутбук'. "
    "'Refrigerator' → 'Холодильник'. "
    "'Air-conditioning' → 'Кондиционер'. "
    "'Hair dryer' → 'Фен'. "
    "'Water dispenser' → 'Кулер'. "
    "'AC Input' → 'Вход AC'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'DC Output' → 'Выход DC'. "
    "'Lamp' → 'Лампа'. "
    "'Mobile Phone' → 'Телефон'. "
    "'Wireless Earphone' → 'Беспроводные наушники'. "
    "Do not change text printed on the unit. " + _KEEP
)

_ESS_ICON = (
    "Wiring diagram titled around a black all-in-one inverter. Translate only the English diagram labels. "
    "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
    "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
    "'OR' → 'ИЛИ'. "
    "'GENERATOR' → 'ГЕНЕРАТОР'. "
    "'INVERTER' → 'ИНВЕРТОР' only if it is a caption above the unit, not text on the casing. "
    "'Fan' → 'Вентилятор'. "
    "'Notebook Computer' → 'Ноутбук'. "
    "'Hair Drier' → 'Фен'. "
    "'Electric kettle' → 'Электрочайник'. "
    "'AC LOADS' → 'НАГРУЗКИ AC'. "
    "'DC LOADS' → 'НАГРУЗКИ DC'. "
    "Keep the letters N and L. Do not change text printed on the black unit. " + _KEEP
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


DUOMI_BY_URL = {
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161133047764.jpg": (
        "Green marketing banner with appliance icons, solar panels and two white units. "
        "Translate only the headline: "
        "'What Can A 5KW Inverter Run?' → 'Что может питать инвертор на 5 кВт?'. "
        "Keep it one line. Do NOT change 'Pv Combiner' on the small box or text on the battery and inverter. "
        + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/11/30/202411301129064894.jpg": _ESS_PORTS,
    "https://www.xindun-power.com/uploadfile/2024/11/30/202411301131268998.jpg": _ESS_FRONT,
    "https://www.xindun-power.com/uploadfile/2024/11/30/202411301132089938.jpg": _ESS_SIDE,
    "https://www.xindun-power.com/uploadfile/2024/11/30/202411301134157727.jpg": _WF_TROLLEY,
    "https://www.xindun-power.com/uploadfile/2024/11/30/202411301340046968.jpg": _BANNER,
    "https://www.xindun-power.com/uploadfile/2024/12/02/20241202155014XoHPwI.jpg": _BANNER,
    "https://www.xindun-power.com/uploadfile/2024/11/01/202411011553297878.jpg": _HFP,
    "https://www.xindun-power.com/uploadfile/2024/11/30/202411301350466108.jpg": _HFP_S,
    "https://www.xindun-power.com/uploadfile/2024/11/30/202411301352218756.jpg": _HFP_C,
    "https://www.xindun-power.com/uploadfile/2024/10/31/202410311042065073.jpg": _HF,
    "https://www.xindun-power.com/uploadfile/2024/11/30/202411301357213095.jpg": _ES,
    "https://www.xindun-power.com/uploadfile/2024/11/09/202411091600108703.jpg": _LF_PUMP,
    "https://www.xindun-power.com/uploadfile/2023/11/25/20231125171345fMB3JT.jpg": _DF,
    "https://www.xindun-power.com/uploadfile/2024/11/09/202411091606366102.jpg": _WF,
    "https://www.xindun-power.com/uploadfile/2024/11/09/202411091612538718.jpg": _LS_BLUE,
    "https://www.xindun-power.com/uploadfile/2024/11/09/202411091618106694.jpg": _WD,
    "https://www.xindun-power.com/uploadfile/2024/10/15/202410151145295923.jpg": _ESS_WHITE,
    "https://www.xindun-power.com/uploadfile/2024/11/02/202411021801555154.jpg": _LF_LIGHT,
    "https://www.xindun-power.com/uploadfile/2024/10/31/202410310954245812.jpg": _LS_LOADS,
    "https://www.xindun-power.com/uploadfile/2024/10/31/202410311716193727.jpg": _WD,
    "https://www.xindun-power.com/uploadfile/2024/10/31/202410310956586221.jpg": _ESS_WHITE,
    "https://www.xindun-power.com/uploadfile/2024/10/31/202410311726521839.jpg": _ESS_ICON,
}

IMAGE_SOURCES = [
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/20241216115007pZoEed.jpg",
            "Что может питать инвертор на 5 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161133047764.jpg",
            "Какую технику тянет инвертор на 5 кВт",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/20241130114153OtgrQF.jpg",
            "Как выбрать мобильную инверторную тележку",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301127445921.jpg",
            "Инверторная тележка 2 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301129064894.jpg",
            "Инверторная тележка 1 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301130267605.jpg",
            "Инверторная тележка 3 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301131268998.jpg",
            "Инверторная тележка 5 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301132089938.jpg",
            "Мобильная инверторная тележка",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301133127710.png",
            "Цена мобильной инверторной тележки 5 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301134157727.jpg",
            "Мобильная инверторная тележка Xindun Power",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301135533195.jpg",
            "Где применяют мобильную инверторную тележку",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091713509183.jpg",
            "Почему выбирают завод инверторов Xindun Power",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301138492150.jpg",
            "Солнечная выставка и сотрудничество",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301140514172.png",
            "Испытание мобильной инверторной тележки",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/02/20241202155014XoHPwI.jpg",
            "Что такое гибридный солнечный инвертор",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301340046968.jpg",
            "Гибридный солнечный инвертор для сети и автономии",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/01/202411011553297878.jpg",
            "Подключение гибридного солнечного инвертора",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301350466108.jpg",
            "Гибридный солнечный инвертор",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301352218756.jpg",
            "Гибридный инвертор для сети и автономии",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311042065073.jpg",
            "Сетевой и автономный гибридный инвертор",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/30/202411301357213095.jpg",
            "Гибридный инвертор Xindun",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091725472ZqaHI.jpg",
            "Автономный солнечный инвертор 2 кВт с литиевым аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091558044596.jpg",
            "Солнечный инвертор LF 2 кВт с аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091600108703.jpg",
            "Схема солнечного инвертора LF 2 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091601354846.jpg",
            "Инвертор DF 2 кВт с литиевым аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2023/11/25/20231125171345fMB3JT.jpg",
            "Схема инвертора DF 2 кВт с аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091605046325.jpg",
            "Низкочастотный инвертор WF 2 кВт с литиевым аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091606366102.jpg",
            "Схема солнечного инвертора 2 кВт с аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091614325993.jpg",
            "Инвертор LS 2 кВт с литиевым аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091612538718.jpg",
            "Схема автономного солнечного инвертора 2 кВт с аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091616437825.jpg",
            "Автономный инвертор WD 2 кВт и аккумулятор",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091618106694.jpg",
            "Солнечный инвертор 2 кВт с аккумулятором Xindun",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091620196540.jpg",
            "Солнечный генератор ESS-Li 2 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/15/202410151145295923.jpg",
            "Солнечный генератор 2 кВт с литиевым аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091625331922.jpg",
            "Гибридный солнечный инвертор HFP 2 кВт с аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/01/202411011553297878.jpg",
            "Гибридный инвертор 2 кВт для сети и автономии с аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091725298562.jpg",
            "Где применяют солнечный инвертор 2 кВт с аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091713509183.jpg",
            "Компания солнечных инверторов 2 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091716289725.jpg",
            "Поставщик солнечного инвертора 2 кВт с аккумулятором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/09/202411091718423810.jpg",
            "Завод по производству солнечных инверторов",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/07/20241107165056i5I3Fz.jpg",
            "Почему стоит выбрать гибридный солнечный инвертор на 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/01/202411011519069489.jpg",
            "Низкочастотный солнечный инвертор LF 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/02/202411021801555154.jpg",
            "Схема подключения солнечного инвертора",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311707579406.jpg",
            "Внешний вид солнечного инвертора DF 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2023/11/25/20231125171345fMB3JT.jpg",
            "Как работает инвертор DF 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311701456285.jpg",
            "Солнечный инвертор LS 1 кВА с завода",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410310954245812.jpg",
            "Как соединить панели, аккумулятор и инвертор 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/06/202411060933119523.jpg",
            "Поставщик низкочастотных инверторов Xindun",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311716193727.jpg",
            "Как пользоваться солнечным инвертором 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/01/202411011540107215.jpg",
            "Автономный солнечный генератор 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410310956586221.jpg",
            "Солнечный генератор 1 кВА с китайского завода",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311724127549.jpg",
            "Солнечный генератор всё в одном на 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311726521839.jpg",
            "Солнечный генератор 1 кВА снижает счета за электричество",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311729041319.jpg",
            "Популярный высокочастотный инвертор 1 кВА",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/01/202411011553297878.jpg",
            "Как гибридный инвертор 1 кВА питает нагрузку",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311732342833.jpg",
            "Куда ставят гибридный солнечный инвертор 1 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/01/202411011601476811.jpg",
            "Xindun на выставке солнечной энергетики",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/01/202411011607059009.jpg",
            "Производитель бытовых солнечных инверторов",
        ),
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
