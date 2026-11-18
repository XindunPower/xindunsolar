#!/usr/bin/env python3
"""Prepare page 21 Russian images.

Duomi gpt-image-2 only for English marketing headlines and diagram labels.
Factory collages, exhibition photos and plain product shots are compressed only.
Product casing text, logos and wall company names stay unchanged.
"""

from __future__ import annotations

import hashlib
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from page1_ru_images import (  # noqa: E402
    OUT,
    USED_FILE_STEMS,
    compress_only,
    encode_jpeg,
    run_duomi,
    slugify,
    unique_stem,
)

UA = "Mozilla/5.0 (compatible; XindunRussianBot/1.0)"
PAGE_NUM = 21

_KEEP = (
    "Keep arrows, wires, icons and the background. Do not move products. "
    "Do not add objects or labels that are not already in the image. Do not redesign. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, product casing text, "
    "model numbers, CE marks, display readings, or words printed on the product "
    "such as HYBRID SOLAR INVERTER, Low Frequency PV Inverter, Low Frequency Inverter, "
    "Pure Sine Wave, ENERGY STORAGE SYSTEM, ALL IN ONE SOLAR GENERATOR, "
    "or MPPT Solar Charge Controller."
)

# Exact English overlay → Russian, keyed by public image URL.
DUOMI_BY_URL: dict[str, str] = {
    "https://www.xindun-power.com/uploadfile/2025/01/20/202501201346338EVQLh.jpg": (
        "This is a marketing banner: a black inverter cabinet on grass in front of a farm shed. "
        "Translate only the white headline on the blue-green panel: "
        "'What is Solar Farm Inverter?' → 'Что такое инвертор для солнечной фермы?'. "
        "Keep the question mark and the two-line layout. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2025/01/20/202501201346573960.jpg": (
        "This is a wider marketing banner of the same farm scene and black inverter cabinet. "
        "Translate only the white headline on the blue-green panel: "
        "'What is Solar Farm Inverter?' → 'Что такое инвертор для солнечной фермы?'. "
        "Keep the question mark and the panel shape. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/25/20241225134840hj0yxN.jpg": (
        "This is a blue product banner of several inverters and solar panels. "
        "Translate only the white headline: "
        "'Inverter PSW Low Frequency' → 'Низкочастотный инвертор PSW'. "
        "Keep it one line. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/25/202412251201224105.jpg": (
        "This is a wider blue product banner of several inverters and solar panels. "
        "Translate only the white headline: "
        "'Inverter PSW Low Frequency' → 'Низкочастотный инвертор PSW'. "
        "Keep it one line. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/25/20241225115242pTCPhj.jpg": (
        "This is a white marketing banner of black three-phase inverter cabinets. "
        "Translate only the green headline: "
        "'Off Grid 3 Phase Solar Inverter' → 'Автономный трёхфазный солнечный инвертор'. "
        "Keep the green badge '3KW-160KW' unchanged. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/25/202412251156069539.jpg": (
        "This is a wider white marketing banner of black three-phase inverter cabinets. "
        "Translate only the green headline: "
        "'Off Grid 3 Phase Solar Inverter' → 'Автономный трёхфазный солнечный инвертор'. "
        "Keep the green badge '3KW-160KW' unchanged. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2025/01/20/202501201350187271.jpg": (
        "This is a wiring diagram of an open black inverter cabinet. Translate only the English diagram labels. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'PV COMBINER' → 'КОМБАЙНЕР PV'. "
        "'SOLAR CONTROLLER' → 'СОЛНЕЧНЫЙ КОНТРОЛЛЕР'. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
        "Each '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
        "'INVERTER' → 'ИНВЕРТОР'. "
        "'3-PHASE LOADS' → 'НАГРУЗКА 3 ФАЗЫ'. "
        "'1-PHASE LOADS' → 'НАГРУЗКА 1 ФАЗЫ'. "
        "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
        "'BREAKER' → 'АВТОМАТ'. "
        "'Earth Wire (GND)' → 'Заземление (GND)'. "
        "'A Phase' → 'Фаза A'. 'B Phase' → 'Фаза B'. 'C Phase' → 'Фаза C'. "
        "Keep the letter N. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161152117945.png": (
        "This is a wiring diagram titled Solar Inverter, with a white wall inverter in the center. "
        "Translate only the English diagram labels. "
        "Title 'Solar Inverter' → 'Солнечный инвертор'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Generator' → 'Генератор'. 'or' → 'или'. 'Power Grid' → 'Электросеть'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'AC Loads' → 'Нагрузка AC'. "
        "'Household Device' → 'Бытовые приборы'. "
        "'Office Equipment' → 'Офисная техника'. "
        "'Industrial Equipment' → 'Промышленное оборудование'. "
        "Do NOT change 'HYBRID SOLAR INVERTER' printed on the white unit. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161155415614.png": (
        "This is a wiring diagram of a white low-frequency inverter. Translate only the English diagram labels. "
        "'PV Input' → 'Вход PV'. "
        "'AC Input' → 'Вход AC'. 'or' → 'или'. 'Generator' → 'Генератор'. "
        "'Lead Acid/Lithium Battery' → 'Свинцовый/литиевый аккумулятор'. "
        "'Pure sine wave' → 'Чистая синусоида'. "
        "'Computer/TV' → 'Компьютер/ТВ'. "
        "'High-power Appliances' → 'Мощные приборы'. "
        "'Household Appliances' → 'Бытовые приборы'. "
        "Do NOT change 'Low Frequency PV Inverter' printed on the white unit. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161157491917.png": (
        "This is a wiring diagram of a white low-frequency inverter with four panel strings. "
        "Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'AC Output' → 'Выход AC'. "
        "'Refrigerator' → 'Холодильник'. "
        "'Fan heater' → 'Тепловентилятор'. "
        "'Air conditioner' → 'Кондиционер'. "
        "'Heater' → 'Нагреватель'. "
        "'Percussion drill' → 'Перфоратор'. "
        "'AC Input' → 'Вход AC'. 'or' → 'или'. "
        "'Generator' → 'Генератор'. 'Battery' → 'Аккумулятор'. "
        "Do NOT change 'Low Frequency PV Inverter' printed on the white unit. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/24/202412241739404082.png": (
        "This is a wiring diagram of a tall white low-frequency inverter and a rack battery. "
        "Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'AC Output' → 'Выход AC'. "
        "'Refrigerator' → 'Холодильник'. "
        "'Fan heater' → 'Тепловентилятор'. "
        "'Air conditioner' → 'Кондиционер'. "
        "'Heater' → 'Нагреватель'. "
        "'Percussion drill' → 'Перфоратор'. "
        "'AC Input' → 'Вход AC'. 'or' → 'или'. "
        "'Generator' → 'Генератор'. 'Battery' → 'Аккумулятор'. "
        "Do NOT change text printed on the white unit. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161201017261.png": (
        "This is a wiring diagram of a blue wall inverter. Translate only the English diagram labels. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'AC INPUT' → 'ВХОД AC'. "
        "'Generator' → 'Генератор'. "
        "'AC OUTPUT' → 'ВЫХОД AC'. "
        "'LAPTOP' → 'НОУТБУК'. 'LAMP' → 'ЛАМПА'. 'PRINTER' → 'ПРИНТЕР'. "
        "'TV' → 'ТЕЛЕВИЗОР'. 'FAN' → 'ВЕНТИЛЯТОР'. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/25/202412251054422376.png": (
        "This is a rear wiring diagram of a white tower inverter. Translate only the English diagram labels. "
        "'Power Grid' → 'Электросеть'. 'or' → 'или'. 'Generator' → 'Генератор'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Solar Controller' → 'Солнечный контроллер'. "
        "'RS232 (Optional)' → 'RS232 (опция)'. "
        "'RS485 (Optional)' → 'RS485 (опция)'. "
        "'Ground Line' → 'Заземление'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'Rice cooker' → 'Рисоварка'. "
        "'Water dispenser' → 'Кулер'. "
        "'Electromagnetic furnace' → 'Индукционная плита'. "
        "'Refrigerator' → 'Холодильник'. "
        "'AIR CONDITIONER' → 'КОНДИЦИОНЕР'. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/25/202412251058171415.png": (
        "This is a wiring diagram of a closed black inverter cabinet. Translate only the English diagram labels. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'PV COMBINER' → 'КОМБАЙНЕР PV'. "
        "'SOLAR CONTROLLER' → 'СОЛНЕЧНЫЙ КОНТРОЛЛЕР'. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
        "Each '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
        "'INVERTER' → 'ИНВЕРТОР'. "
        "'3-PHASE LOADS' → 'НАГРУЗКА 3 ФАЗЫ'. "
        "'1-PHASE LOADS' → 'НАГРУЗКА 1 ФАЗЫ'. "
        "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
        "'BREAKER' → 'АВТОМАТ'. "
        "'Earth Wire (GND)' → 'Заземление (GND)'. "
        "'A Phase' → 'Фаза A'. 'B Phase' → 'Фаза B'. 'C Phase' → 'Фаза C'. "
        "Keep the letter N. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161340176595.png": (
        "This is a wiring diagram of a closed black inverter cabinet. Translate only the English diagram labels. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'PV COMBINER' → 'КОМБАЙНЕР PV'. "
        "'SOLAR CONTROLLER' → 'СОЛНЕЧНЫЙ КОНТРОЛЛЕР'. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
        "Each '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
        "'INVERTER' → 'ИНВЕРТОР'. "
        "'3-PHASE LOADS' → 'НАГРУЗКА 3 ФАЗЫ'. "
        "'1-PHASE LOADS' → 'НАГРУЗКА 1 ФАЗЫ'. "
        "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
        "'BREAKER' → 'АВТОМАТ'. "
        "'Earth Wire (GND)' → 'Заземление (GND)'. "
        "'A Phase' → 'Фаза A'. 'B Phase' → 'Фаза B'. 'C Phase' → 'Фаза C'. "
        "Keep the letter N. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/25/202412251102379323.png": (
        "This is a wiring diagram of a white energy-storage inverter. Translate only the English diagram labels. "
        "'Solar Panel' → 'Солнечная панель'. "
        "'AC Input' → 'Вход AC'. 'or' → 'или'. 'Generator' → 'Генератор'. "
        "'AC Output' → 'Выход AC'. "
        "'Laptop' → 'Ноутбук'. 'Refrigerator' → 'Холодильник'. "
        "'Air-conditioning' → 'Кондиционер'. "
        "'Hair drier' → 'Фен'. 'Water dispenser' → 'Кулер'. "
        "'DC Output' → 'Выход DC'. "
        "'Lamp' → 'Лампа'. 'Mobile Phone' → 'Телефон'. "
        "'Wireless Earphone' → 'Беспроводные наушники'. "
        "Do NOT change 'ENERGY STORAGE SYSTEM' printed on the white unit. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161342456267.png": (
        "This is a wiring diagram of an all-in-one solar generator cabinet. Translate only the English diagram labels. "
        "'DC LOADS' → 'НАГРУЗКА DC'. "
        "'AC LOADS' → 'НАГРУЗКА AC'. "
        "'Refrigerator' → 'Холодильник'. "
        "'Electromagnetic furnace' → 'Индукционная плита'. "
        "'Electric hammer' → 'Электромолоток'. "
        "'Air conditioner' → 'Кондиционер'. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. 'or' → 'или'. 'GENERATOR' → 'ГЕНЕРАТОР'. "
        "'INVERTER' → 'ИНВЕРТОР'. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
        "Each '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
        "Keep the letters L and N. "
        "Do NOT change 'ALL IN ONE SOLAR GENERATOR' printed on the cabinet. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161348304040.png": (
        "This is a system diagram of an on-and-off-grid hybrid inverter. Translate only the English diagram labels. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Battery' → 'Аккумулятор'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или' only if that word is printed. "
        "'Generator' → 'Генератор' only if that word is printed. "
        "Both 'AC Loads' labels → 'Нагрузка AC'. "
        "Do NOT change 'HYBRID SOLAR INVERTER' on the white unit. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161153535797.png": (
        "This is a parallel-wiring diagram of three inverters. Translate only the English labels. "
        "Headline: 'Parallel operation support single phase output' → 'Параллельная работа, однофазный выход'. "
        "'Unit 1' → 'Блок 1'. 'Unit 2' → 'Блок 2'. 'Unit 3' → 'Блок 3'. "
        "'Battery' → 'Аккумулятор'. 'Utility Grid' → 'Электросеть'. 'Loads' → 'Нагрузка'. "
        "Keep N and L. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161154299998.png": (
        "This is a parallel-wiring diagram of nine inverters in three phases. Translate only the English labels. "
        "Headline: 'Parallel operation support three phase output' → 'Параллельная работа, трёхфазный выход'. "
        "Keep P1, P2 and P3. "
        "'Battery' → 'Аккумулятор'. 'Utility Grid' → 'Электросеть'. 'Loads' → 'Нагрузка'. "
        "Keep N, L1, L2 and L3. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161159218612.png": (
        "This is a wiring diagram of a tall white low-frequency inverter. Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'AC Input' → 'Вход AC'. 'or' → 'или'. 'Generator' → 'Генератор'. "
        "'AC Output' → 'Выход AC'. "
        "'Laptop' → 'Ноутбук'. 'Printer' → 'Принтер'. 'TV' → 'Телевизор'. "
        "'Fans' → 'Вентиляторы'. 'Water pump' → 'Водяной насос'. "
        "'Battery' → 'Аккумулятор'. "
        "Do NOT change text printed on the white unit. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161337527724.jpg": (
        "This is a rear wiring diagram of a white tower inverter. Translate only the English diagram labels. "
        "'Power Grid' → 'Электросеть'. 'or' → 'или'. 'Generator' → 'Генератор'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Solar Controller' → 'Солнечный контроллер'. "
        "'RS232 (Optional)' → 'RS232 (опция)'. "
        "'RS485 (Optional)' → 'RS485 (опция)'. "
        "'Ground Line' → 'Заземление'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'Water dispenser' → 'Кулер'. "
        "'Refrigerator' → 'Холодильник'. "
        "'Electric hammer' → 'Электромолоток'. "
        "'Electromagnetic furnace' → 'Индукционная плита'. "
        "'Air conditioner' → 'Кондиционер'. " + _KEEP
    ),
    "https://www.xindun-power.com/uploadfile/2024/12/16/202412161344261233.png": (
        "This is a system diagram of an on-and-off-grid hybrid inverter, wider than tall. "
        "Translate only the English diagram labels that are actually printed. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Battery' → 'Аккумулятор'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "'Power Grid' → 'Электросеть'. "
        "Both 'AC Loads' labels → 'Нагрузка AC'. "
        "Do NOT change 'HYBRID SOLAR INVERTER' on the white unit. " + _KEEP
    ),
}


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


IMAGE_SOURCES: list[list[dict]] = [
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/01/20/202501201346338EVQLh.jpg",
            "Как выбрать инвертор для солнечной фермы на 100 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/01/20/202501201346573960.jpg",
            "Что такое инвертор для солнечной фермы",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/01/20/202501201349589278.jpg",
            "Трёхфазный инвертор 100 кВт для фермы",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/01/20/202501201350187271.jpg",
            "Схема трёхфазного инвертора для фермы на 100 кВт",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/20241225134840hj0yxN.jpg",
            "Что такое низкочастотный инвертор PSW",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251201224105.jpg",
            "Низкочастотный инвертор чистой синусоиды Xindun Power",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/28/202412281456587560.jpg",
            "Низкочастотный инвертор чистой синусоиды серии LS",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/28/202412281457159132.jpg",
            "Инвертор PSW серии LF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/28/202412281457335013.jpg",
            "Низкочастотный инвертор PSW серии DF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/28/202412281457537249.jpg",
            "Инвертор PSW серии WD",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/28/202412281458114315.jpg",
            "Низкочастотный инвертор PSW серии HDSX",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/28/202412281458365283.jpg",
            "Низкочастотный инвертор PSW серии WF",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/24/20241224171614bhHyBt.jpg",
            "Как правильно выбрать инвертор MPPT на 3 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161152117945.png",
            "Схема инвертора MPPT 3 кВт серии HP PRO-T",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/24/202412241731067479.png",
            "Применение инвертора MPPT 3 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161155415614.png",
            "Схема солнечного инвертора MPPT 3 кВт серии LF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/24/202412241734159173.png",
            "Инвертор MPPT 3 кВт Xindun Power на стене",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161157491917.png",
            "Схема инвертора MPPT 3 кВт серии DF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/24/202412241736544787.png",
            "Применение инвертора MPPT 3 кВт серии DF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/24/202412241739404082.png",
            "Схема инвертора MPPT 3 кВт серии WF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251048449693.png",
            "Инвертор MPPT 3 кВт у солнечных панелей",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161201017261.png",
            "Схема солнечного инвертора MPPT 3 кВт серии LS",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251053191763.png",
            "Инвертор MPPT 3 кВт для дома",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251054422376.png",
            "Схема инвертора MPPT 3 кВт серии WD",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251056291316.png",
            "Настенный инвертор MPPT 3 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251058171415.png",
            "Схема трёхфазного инвертора MPPT 3 кВт серии HDSX",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251059472676.png",
            "Аккумуляторная стойка с инвертором MPPT 3 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251102379323.png",
            "Схема инвертора MPPT 3 кВт серии ESS-Li",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251104122085.png",
            "Монтаж солнечной панели для инвертора MPPT 3 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161342456267.png",
            "Схема солнечного генератора 3 кВт серии ESS",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251106454825.png",
            "Настенная установка солнечного генератора 3 кВт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161348304040.png",
            "Схема гибридного солнечного инвертора MPPT 3 кВт серии HFP",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251111063938.png",
            "Гибридный инвертор MPPT 3 кВт на стене",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251118174421.jpg",
            "Завод производителя инверторов MPPT 3 кВт в Китае",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251120367207.png",
            "Цех солнечных инверторов MPPT",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251122291487.jpg",
            "Команда и сотрудничество Xindun Power",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/20241225115242pTCPhj.jpg",
            "Автономный трёхфазный солнечный инвертор",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251156069539.jpg",
            "Что такое трёхфазный солнечный инвертор",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/25/202412251151388118.jpg",
            "Шоурум автономного трёхфазного солнечного инвертора",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/20241216113030ktQw2s.jpg",
            "Зарядное устройство-инвертор чистой синусоиды на 48 вольт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161152117945.png",
            "Схема зарядного инвертора 48 В серии HP PRO-T",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161153535797.png",
            "Параллельная работа с однофазным выходом",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161154299998.png",
            "Параллельная работа с трёхфазным выходом",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161155415614.png",
            "Инвертор чистой синусоиды 48 В серии LF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161157491917.png",
            "Инвертор синусоиды 48 В серии DF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161159218612.png",
            "Схема зарядного инвертора 48 В серии WF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161201017261.png",
            "Зарядный инвертор 48 В серии LS",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161337527724.jpg",
            "Инвертор чистой синусоиды 48 В серии WD",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161340176595.png",
            "Трёхфазный зарядный инвертор 48 В серии HDSX",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161342456267.png",
            "Инвертор синусоиды 48 В серии ESS",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161344261233.png",
            "Инвертор чистой синусоиды 48 В серии HF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161348304040.png",
            "Гибридный солнечный инвертор 48 В для сети и автономии серии HFP",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161349448460.png",
            "Применение зарядного инвертора чистой синусоиды на 48 вольт",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/12/16/202412161351503972.png",
            "Производитель зарядных инверторов 48 В",
        ),
    ],
]

IMAGE_LOG: list[dict] = []
DUOMI_MAP = {
    (a, i): im["src"]
    for a, group in enumerate(IMAGE_SOURCES)
    for i, im in enumerate(group)
    if im["src"] in DUOMI_BY_URL
}


def candidate_sizes(w: int, h: int) -> list[str]:
    """Sizes Duomi accepts: 1:1, 3:2, 2:3, or widthxheight divisible by 16."""
    ratio = w / h if h else 1.0
    named = [("1:1", 1.0), ("3:2", 1.5), ("2:3", 2 / 3)]
    sizes: list[str] = []
    name, nr = min(named, key=lambda kv: abs(kv[1] - ratio))
    if abs(nr - ratio) <= 0.045:
        sizes.append(name)

    def r16(x: float) -> int:
        return max(256, int(round(x / 16.0)) * 16)

    custom: list[str] = []
    for target in (1_400_000, 2_200_000):
        tw = r16((target * ratio) ** 0.5)
        th = r16(tw / ratio)
        for _ in range(12):
            pix = tw * th
            if pix < 655360:
                tw += 16
                th = r16(tw / ratio)
            elif pix > 8_000_000:
                tw -= 16
                th = r16(tw / ratio)
            else:
                break
        best = (tw, th, abs((tw / th) - ratio))
        for dw in range(-80, 96, 16):
            for dh in range(-80, 96, 16):
                cw, ch = tw + dw, th + dh
                if cw < 256 or ch < 256:
                    continue
                if not (655360 <= cw * ch <= 8294400):
                    continue
                delta = abs((cw / ch) - ratio)
                if delta < best[2]:
                    best = (cw, ch, delta)
        custom.append(f"{best[0]}x{best[1]}")
    for item in custom:
        if item not in sizes:
            sizes.append(item)
    if not sizes:
        sizes.append("1:1")
    return sizes


def _download(src: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    rr = requests.get(src, timeout=90, headers={"User-Agent": UA})
    rr.raise_for_status()
    dest.write_bytes(rr.content)


def _translate_url(src: str, orig_wh: tuple[int, int], orig_path: Path) -> Path | None:
    prompt = DUOMI_BY_URL[src]
    digest = hashlib.sha1(src.encode()).hexdigest()[:10]
    sizes = candidate_sizes(*orig_wh)
    for i, size in enumerate(sizes):
        stem = f"p21cache-{digest}-s{i}"
        print(f"[duomi] {digest} size-try {i + 1}/{len(sizes)} {size} {orig_wh}", flush=True)
        result = run_duomi(src, prompt, stem, size, orig_wh, orig_path, attempts=2 if i == 0 else 1)
        if result is not None:
            return result
    return None


def _final_ready(stem: str, orig_wh: tuple[int, int]) -> Path | None:
    final = OUT / f"{stem}.jpg"
    if not final.exists() or final.stat().st_size == 0 or final.stat().st_size > 100 * 1024:
        return None
    with Image.open(final) as im:
        if im.size != orig_wh:
            return None
    return final


def prepare_all() -> list[list[dict]]:
    specs: list[dict] = []
    for article_idx, images in enumerate(IMAGE_SOURCES):
        for img_idx, im in enumerate(images):
            stem = unique_stem(slugify(im["alt_ru"]))
            ext = Path(im["src"]).suffix.lower() or ".jpg"
            if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
                ext = ".jpg"
            local = OUT / f"_src_ru_p{PAGE_NUM}_a{article_idx}_i{img_idx}{ext}"
            ready = _final_ready(stem, (0, 0))
            # Dimensions are known only after the source is opened. Download when reuse is not yet proven.
            if ready is None and not local.exists():
                _download(im["src"], local)
            if local.exists():
                with Image.open(local) as pil:
                    orig_wh = pil.size
            else:
                # Reused output still needs the original pixel size. Read it from the finished JPEG.
                with Image.open(ready) as pil:  # type: ignore[arg-type]
                    orig_wh = pil.size
            ready = _final_ready(stem, orig_wh)
            specs.append(
                {
                    "article": article_idx,
                    "img": img_idx,
                    "im": im,
                    "stem": stem,
                    "local": local,
                    "orig_wh": orig_wh,
                    "need": im["src"] in DUOMI_BY_URL,
                    "ready": ready,
                }
            )

    translated: dict[str, Path | None] = {}
    pending_urls = {spec["im"]["src"] for spec in specs if spec["need"] and spec["ready"] is None}
    unique = []
    seen = set()
    for spec in specs:
        src = spec["im"]["src"]
        if src in pending_urls and src not in seen:
            seen.add(src)
            unique.append(spec)
    if not unique:
        print("[img] reusing prepared JPEGs, no new Duomi calls", flush=True)

    lock = threading.Lock()

    def _job(spec: dict) -> tuple[str, Path | None]:
        src = spec["im"]["src"]
        try:
            path = _translate_url(src, spec["orig_wh"], spec["local"])
        except Exception as exc:  # noqa: BLE001
            print(f"[duomi] failed {src}: {exc}", flush=True)
            path = None
        with lock:
            print(f"[duomi] done {Path(src).name} -> {path}", flush=True)
        return src, path

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(_job, spec) for spec in unique]
        for fut in as_completed(futures):
            src, path = fut.result()
            translated[src] = path

    prepared_all: list[list[dict]] = [[] for _ in IMAGE_SOURCES]
    for spec in specs:
        im = spec["im"]
        stem = spec["stem"]
        orig_wh = spec["orig_wh"]
        final = OUT / f"{stem}.jpg"
        method = "compress"
        duomi_path = None
        if spec["ready"] is not None:
            final = spec["ready"]
            method = "duomi" if spec["need"] else "compress"
            duomi_path = str(final) if spec["need"] else None
        elif spec["need"]:
            got = translated.get(im["src"])
            if got is not None and got.exists():
                encode_jpeg(got, final, orig_wh[0], orig_wh[1], 100)
                method = "duomi"
                duomi_path = str(got)
            else:
                print(f"[duomi] fallback original a{spec['article']}_i{spec['img']}", flush=True)
                final = compress_only(spec["local"], stem, orig_wh)
                method = "duomi-fallback-original"
        else:
            final = compress_only(spec["local"], stem, orig_wh)

        if final.stat().st_size > 100 * 1024:
            raise RuntimeError(f"image exceeds 100KB: {final}")
        with Image.open(final) as chk:
            if chk.size != orig_wh:
                raise RuntimeError(f"image dimensions changed for {final}: {chk.size} vs {orig_wh}")

        entry = {
            "local": final,
            "alt_ru": im["alt_ru"],
            "title_ru": im["title_ru"],
            "src_orig": im["src"],
            "method": method,
            "duomi_path": duomi_path,
            "orig_wh": orig_wh,
        }
        IMAGE_LOG.append(
            {
                "article": spec["article"],
                "img": spec["img"],
                **{k: (str(v) if k == "local" else v) for k, v in entry.items()},
            }
        )
        prepared_all[spec["article"]].append(entry)
        print(
            f"[img] a{spec['article']}_i{spec['img']} method={method} -> {final.name} "
            f"{final.stat().st_size}b {orig_wh}",
            flush=True,
        )

    Path(f"/tmp/page{PAGE_NUM}_ru_image_log.json").write_text(
        json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return prepared_all


if __name__ == "__main__":
    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
