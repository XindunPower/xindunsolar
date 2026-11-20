#!/usr/bin/env python3
"""Prepare page 23 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for marketing headlines and diagram labels.
Product photos, factory shots, installations and plain collages are compressed only.
Product casing text, logos, certificates and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 23

_KEEP = (
    "Keep arrows, wires, icons, colors and the background. Do not move products. "
    "Do not add objects or labels that are not already in the image. Do not redesign. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, product casing text, "
    "model numbers, CE marks, display readings, button silkscreen, terminal letters N L PE, "
    "or words printed on the product such as HYBRID SOLAR INVERTER, Low Frequency Inverter, "
    "Low Frequency PV Inverter, Pure Sine Wave, ENERGY STORAGE SYSTEM, "
    "ALL IN ONE SOLAR GENERATOR, or SOLAR POWER SYSTEM."
)

_LF_WALL = (
    "Wiring diagram of a white wall inverter. Translate only the English overlay labels. "
    "'PV Input' → 'Вход PV'. "
    "'AC Input' → 'Вход AC'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Lead Acid/Lithium Battery' → 'Свинцовый/литиевый аккумулятор'. "
    "'Computer/TV' → 'Компьютер/ТВ'. "
    "'Pure sine wave' → 'Чистая синусоида'. "
    "'High-power Appliances' → 'Мощные приборы'. "
    "'Household Appliances' → 'Бытовые приборы'. "
    "Do NOT change 'Low Frequency PV Inverter' printed on the unit. " + _KEEP
)

_DF = (
    "Wiring diagram of a white wall inverter with solar panels at the top. "
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

_HDSX = (
    "Wiring diagram of a tall black three-phase inverter cabinet. "
    "Translate only the English caption labels, not silkscreen on the terminal block. "
    "'INVERTER' above the cabinet → 'ИНВЕРТОР'. "
    "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
    "'PV COMBINER' under the white box → 'КОМБАЙНЕР PV'. "
    "'SOLAR CONTROLLER' → 'СОЛНЕЧНЫЙ КОНТРОЛЛЕР'. "
    "'12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч' wherever it appears. "
    "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
    "'3-PHASE LOADS' → 'ТРЁХФАЗНЫЕ НАГРУЗКИ'. "
    "'1-PHASE LOADS' → 'ОДНОФАЗНЫЕ НАГРУЗКИ'. "
    "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
    "'BREAKER' → 'АВТОМАТ'. "
    "'Earth Wire (GND)' → 'Заземление (GND)'. "
    "'A Phase' → 'Фаза A'. 'B Phase' → 'Фаза B'. 'C Phase' → 'Фаза C'. "
    "Keep the single letter N. Do not change BATTERY, AC INPUT or AC OUTPUT printed on the terminal block, "
    "or text printed on the white combiner and the orange controller. " + _KEEP
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

_HFP_TITLE = (
    "Same hybrid-inverter wiring diagram, with a large title at the top. "
    "Translate 'ON-OFF GRID MODE' → 'РЕЖИМ СЕТЬ И АВТОНОМИЯ'. "
    "Then translate the diagram labels: "
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

_WD_BASE = (
    "Rear wiring diagram of a white floor inverter with an orange controller. "
    "Translate only the English overlay labels. "
    "'RS232 (Optional)' → 'RS232 (опция)'. "
    "'RS485 (Optional)' → 'RS485 (опция)'. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Solar Controller' → 'Солнечный контроллер'. "
    "'Ground Line' → 'Заземление'. "
    "'Batteries' → 'Аккумуляторы'. "
    "Do not change text on the orange controller or terminal silkscreen. "
)

_WD_RICE = (
    _WD_BASE
    + "'Rice cooker' → 'Рисоварка'. "
    "'Water dispenser' → 'Кулер'. "
    "'Electromagnetic furnace' → 'Индукционная плита'. "
    "'Refrigerator' → 'Холодильник'. "
    "'AIR CONDITIONER' → 'КОНДИЦИОНЕР'. "
    + _KEEP
)

_WD_HAMMER = (
    _WD_BASE
    + "'Water dispenser' → 'Кулер'. "
    "'Refrigerator' → 'Холодильник'. "
    "'Electric hammer' → 'Электромолоток'. "
    "'Electromagnetic furnace' → 'Индукционная плита'. "
    "'Air conditioner' → 'Кондиционер'. "
    + _KEEP
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

_ZRS = (
    "Wiring diagram of a tall white-and-black hybrid inverter on wheels. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Off-Grid Hybrid Solar Inverter' → 'Автономный гибридный солнечный инвертор'. "
    "'(Can work without battery)' → '(может работать без аккумулятора)'. "
    "'Batteries (Optional)' → 'Аккумуляторы (опция)'. "
    "'Power Grid' → 'Электросеть'. "
    "'Generator' → 'Генератор'. "
    "'or' → 'или'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Do not change text printed on the inverter. " + _KEEP
)

_ESS_CABINET = (
    "Wiring diagram of a black-and-white all-in-one cabinet. Translate only the English labels. "
    "'DC LOADS' → 'НАГРУЗКИ DC'. "
    "'Refrigerator' → 'Холодильник'. "
    "'Electromagnetic furnace' → 'Индукционная плита'. "
    "'Electric hammer' → 'Электромолоток'. "
    "'Air conditioner' → 'Кондиционер'. "
    "'AC LOADS' → 'НАГРУЗКИ AC'. "
    "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
    "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
    "'or' → 'или'. "
    "'GENERATOR' → 'ГЕНЕРАТОР'. "
    "'12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
    "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
    "'INVERTER' under the cabinet → 'ИНВЕРТОР'. "
    "Keep the letters N and L. Do NOT change 'ALL IN ONE SOLAR GENERATOR' printed on the door. " + _KEEP
)

_HP_HOME = (
    "Simple wiring diagram of one white wall inverter. Translate only the English labels. "
    "'Solar Panel' → 'Солнечная панель'. "
    "'Power Grid' → 'Электросеть'. "
    "'Generator' → 'Генератор'. "
    "'Inverter' under the unit → 'Инвертор'. "
    "'Battery' → 'Аккумулятор'. "
    "'WiFi / GPRS' → 'WiFi / GPRS'. "
    "'Internet' → 'Интернет'. "
    "'Supply Power to Home/Office/School' → 'Питание дома, офиса и школы'. "
    "Keep WiFi and GPRS as those abbreviations. Do not change the xindun logo. " + _KEEP
)

_PARALLEL3 = (
    "Parallel wiring of three wall inverters, with rear views below. "
    "Translate only the English labels. "
    "'Battery' → 'Аккумулятор'. "
    "'Utility Grid' → 'Электросеть'. "
    "'Loads' → 'Нагрузки'. "
    "Keep the letters N and L. Do not change the xindun logo or port silkscreen on the rear views. " + _KEEP
)

_UNITS = (
    "Parallel wiring of three white inverters. Translate only the English labels. "
    "'Unit 1' → 'Блок 1'. 'Unit 2' → 'Блок 2'. 'Unit 3' → 'Блок 3'. "
    "'Battery' → 'Аккумулятор'. "
    "'Utility Grid' → 'Электросеть'. "
    "'Loads' → 'Нагрузки'. "
    "Keep the letters N and L and the xindun logo. " + _KEEP
)

_P123 = (
    "Three-phase parallel diagram with nine white inverters in groups P1, P2 and P3. "
    "Keep P1, P2 and P3 unchanged. Translate only: "
    "'Battery' → 'Аккумулятор'. "
    "'Utility Grid' → 'Электросеть'. "
    "'Loads' → 'Нагрузки'. "
    "Do not move the colored wires. " + _KEEP
)

_HPPROT = (
    "Wiring diagram titled Solar Inverter, with a white hybrid unit in the center. "
    "Translate only the English labels. "
    "'Solar Inverter' → 'Солнечный инвертор'. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Generator' → 'Генератор'. "
    "'or' → 'или'. "
    "'Power Grid' → 'Электросеть'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "'Household Device' → 'Бытовые приборы'. "
    "'Office Equipment' → 'Офисная техника'. "
    "'Industrial Equipment' → 'Промышленное оборудование'. "
    "Do NOT change 'HYBRID SOLAR INVERTER' on the casing or the xindun GREENPOWER logo. " + _KEEP
)

_HP_REAR = (
    "Rear view of a wide inverter with two solar arrays. Translate only the English labels. "
    "'Solar Panels 2' → 'Солнечные панели 2'. "
    "'Solar Panels 1' → 'Солнечные панели 1'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'AC Input' → 'Вход AC'. "
    "'AC Output' → 'Выход AC'. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Keep N, L and PE. Do not change the xindun GREENPOWER logo or battery model text. " + _KEEP
)

_LS_BLUE = (
    "Open view of a blue wall inverter. Translate only the English labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'DC Loads' → 'Нагрузки DC'. "
    "'AC Input' → 'Вход AC'. "
    "'AC Output' → 'Выход AC'. "
    "'Battery' → 'Аккумулятор'. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Keep N, L and PE. Do not change text printed on the blue cover. " + _KEEP
)

_CT = (
    "Wiring diagram of a small white-and-yellow inverter. Translate only the English labels. "
    "'DC Loads (DC 12V Output)' → 'Нагрузки DC (выход 12 В DC)'. "
    "'USB 5V Loads (DC 5V Output)' → 'Нагрузки USB 5 В (выход 5 В DC)'. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'DC Loads' → 'Нагрузки DC'. "
    "'Battery' → 'Аккумулятор'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Do not change silkscreen on the inverter such as SOLAR INVERTER, BATTERY, AC INPUT or AC OUTPUT. " + _KEEP
)

_WD_YELLOW = (
    "Wiring diagram of a yellow floor inverter. Translate only the English labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Solar Inverter' → 'Солнечный инвертор'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'Power Grid' → 'Электросеть'. "
    "'Generator' → 'Генератор'. "
    "'or' → 'или'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Do not change the xindun logo on the yellow cabinet. " + _KEEP
)

_WF_LOADS = (
    "Wiring diagram of a white wall inverter with heavy loads on the right. "
    "Translate only the English labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Utility Grid' → 'Электросеть'. "
    "'OR' → 'ИЛИ'. "
    "'Generator' → 'Генератор'. "
    "'Battery' → 'Аккумулятор'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "'Freezer' → 'Морозильник'. "
    "'Air conditioner' → 'Кондиционер'. "
    "'Motor' → 'Двигатель'. "
    "'Water pump' → 'Водяной насос'. "
    "'Percussion drill' → 'Перфоратор'. "
    "Do NOT change 'Low Frequency Inverter' or 'Pure Sine Wave' printed on the unit. " + _KEEP
)

_ESS_NOTES = (
    "Annotated photo of two solar-generator cabinets with many small English notes. "
    "Translate every English note. Keep 4mm², the colors of the wires, and the photos. "
    "'4pcs 330W solar panel connect in parallel' → '4 панели по 330 Вт параллельно'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "'Solar Generntor: Built-in 3KW 24V inverter +24V 60A MPPT+2pcs 12V 200Ah Gel battery' → "
    "'Солнечный генератор: встроенный инвертор 3 кВт 24 В + MPPT 24 В 60 А + 2 гелевых аккумулятора 12 В 200 А·ч'. "
    "'USB 5V Loads (DC 5V Output)' → 'Нагрузки USB 5 В (выход 5 В DC)'. "
    "'DC Loads (DC 12V Output)' → 'Нагрузки DC (выход 12 В DC)'. "
    "'12V Battery' → 'Аккумулятор 12 В'. "
    "'Spare Battery' → 'Запасной аккумулятор'. "
    "'Live Wire(L)' → 'Фаза (L)'. "
    "'Neutral Wire(N)' → 'Ноль (N)'. "
    "'Power Grid' → 'Электросеть'. "
    "'Breaker' → 'Автомат'. "
    "'OR' → 'ИЛИ'. "
    "'Diesel generators' → 'Дизельные генераторы'. "
    "'Battery positive (connected to the red wire)' → 'Плюс аккумулятора (к красному проводу)'. "
    "'Battery negative (connected to the black wire)' → 'Минус аккумулятора (к чёрному проводу)'. "
    "'12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
    "Do not change the xindun logo. " + _KEEP
)

_HDSX_SIMPLE = (
    "Wiring diagram of a black three-phase cabinet. Translate only the English labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'3 Phase Solar Inverter' → 'Трёхфазный солнечный инвертор'. "
    "'Power Grid' → 'Электросеть'. "
    "'Generator' → 'Генератор'. "
    "'or' → 'или'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "Do not change the xindun logo on the cabinet. " + _KEEP
)

_BANNER_DE = (
    "Marketing banner of solar panels and several inverters on a dark background. "
    "The only overlay headline is German, not English: 'Solar Wechselrichter'. "
    "Translate that headline to Russian: 'Солнечный инвертор'. Keep it one centered line. "
    "Do NOT change the xindun GREENPOWER logo, product casing text, panels or the units. Do not redesign. "
    + _KEEP
)

_COLLAGE1 = (
    "Factory photo collage with a green number 1. "
    "The headline is German: 'CHINA SOLARFABRIK SEIT 2007' → 'КИТАЙСКИЙ СОЛНЕЧНЫЙ ЗАВОД С 2007'. "
    "Translate the green English captions: 'Reception' → 'Ресепшен', 'Sample Room' → 'Образцы', "
    "'Office' → 'Офис', 'Workshop' → 'Цех' on both workshop captions. "
    "Do NOT change the green number, the photos, the xindun logo, or Chinese characters on the wall."
)

_COLLAGE2 = (
    "Factory photo collage with a green number 2. "
    "Translate only the German headline 'STRENGE QUALITÄTSKONTROLLE UND PROZESSKONTROLLE' "
    "to 'СТРОГИЙ КОНТРОЛЬ КАЧЕСТВА И ПРОЦЕССОВ'. Keep the two-line layout and the number 2. "
    "Do not change the photographs."
)

_COLLAGE3 = (
    "Customer photo collage with a green number 3. "
    "Translate only the German headline 'MIT UNSEREN RESPEKTIERTEN KUNDEN' "
    "to 'С НАШИМИ УВАЖАЕМЫМИ КЛИЕНТАМИ'. Keep two lines and the number 3. "
    "Do NOT change photos, the booth sign Hall E5-113-115, Chinese or English company names "
    "on walls and banners, the xindun logo, or certificates people are holding."
)

_CERTS = (
    "Certificate collage with a green number 4. "
    "Translate only the German headline 'DAS DRITTANBIETER-ZERTIFIKAT BEWEIST ZUVERLÄSSIGKEIT' "
    "to 'СЕРТИФИКАТ НЕЗАВИСИМОЙ СТОРОНЫ ПОДТВЕРЖДАЕТ НАДЁЖНОСТЬ'. Keep two lines and the number 4. "
    "Do NOT change CE, FC, IEC, ISO, RoHS or TÜV marks, and do not change any text, seals or layout "
    "of the certificate documents."
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "hero4": "https://www.xindun-power.com/uploadfile/2024/10/31/20241031101056dLbA4u.jpg",
    "hero15": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311120003Jxgu6.jpg",
    "hero6": "https://www.xindun-power.com/uploadfile/2024/10/31/20241031105124mIOct9.jpg",
    "hero20": "https://www.xindun-power.com/uploadfile/2024/11/06/20241106085141a2m58P.jpg",
    "hero_de": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/OffGridPVWechselrichterSolar.jpg",
    "lf_wall": "https://www.xindun-power.com/uploadfile/2024/08/28/202408281504199926.jpg",
    "df": "https://www.xindun-power.com/uploadfile/2023/11/25/20231125171345fMB3JT.jpg",
    "df2": "https://www.xindun-power.com/uploadfile/2024/10/31/202410310953097995.jpg",
    "ls": "https://www.xindun-power.com/uploadfile/2024/10/31/202410310954245812.jpg",
    "hdsx": "https://www.xindun-power.com/uploadfile/2024/10/31/202410310955287320.jpg",
    "essli": "https://www.xindun-power.com/uploadfile/2024/10/31/202410310956586221.jpg",
    "hfp": "https://www.xindun-power.com/uploadfile/2024/10/31/202410310959575831.jpg",
    "use4": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311002144914.jpg",
    "office": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311005334006.jpg",
    "factory": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311006334774.jpg",
    "wd_prod": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311059275619.jpg",
    "wd": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311101142137.jpg",
    "hdsx_prod": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311102497132.jpg",
    "hdsx3": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311106275402.jpg",
    "wf_prod": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311107565138.jpg",
    "wf": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311109218818.jpg",
    "zrs_prod": "https://www.xindun-power.com/uploadfile/2024/11/02/202411021750389111.jpg",
    "zrs": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311112463795.jpg",
    "use15": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311114264978.jpg",
    "wd6": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311033015214.jpg",
    "ess": "https://www.xindun-power.com/uploadfile/2024/11/04/202411040850296527.jpg",
    "hf": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311042065073.jpg",
    "use6": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311045037511.jpg",
    "app_wf": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311141272327.jpg",
    "app_wd": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311146594129.jpg",
    "app_hdsx": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311408582533.jpg",
    "zrs20": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311153216355.jpg",
    "app_zrs": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311154556121.jpg",
    "hq": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311156589541.png",
    "shop": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311159546513.png",
    "banner_de": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/OffGridSolarPVWechselrichter.jpg",
    "hpplus": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/HPPLUSSolarWechselrichter.jpg",
    "hpplus_1": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/HPPLUSSolarWechselrichterohneparallel.jpg",
    "hpplus_p": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/HPPLUSSolarWechselrichterParallel.jpg",
    "hpplus2": "https://www.xindun-power.com/uploadfile/2024/08/27/202408271436547689.jpg",
    "units": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151138082598.jpg",
    "p123": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151159558052.jpg",
    "hfp_prod": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151151307876.jpg",
    "hfp_title": "https://www.xindun-power.com/uploadfile/2024/09/29/202409291438062189.jpg",
    "hpprot_prod": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151203438188.jpg",
    "hpprot": "https://www.xindun-power.com/uploadfile/2024/08/27/202408271420161484.jpg",
    "hp_prod": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/HPSolarWechselrichter.jpg",
    "hp_rear": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/WieManSolarWechselrichterVerwendetHP.jpg",
    "ls_prod": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/LSSolarWechselrichter.jpg",
    "ls_blue": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/WieManSolarWechselrichterVerwendetLS.jpg",
    "ct_prod": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/CTSolarWechselrichter.jpg",
    "ct": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/WieManSolarWechselrichterVerwendetCT.jpg",
    "wd_family": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/WDSolarWechselrichter.jpg",
    "wd_yellow": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/WieManSolarWechselrichterVerwendetWD.jpg",
    "df_prod": "https://www.xindun-power.com/uploadfile/2024/03/04/20240304162327ASPtyF.jpg",
    "lf_prod": "https://www.xindun-power.com/uploadfile/2024/08/28/202408281503204754.jpg",
    "wf_family": "https://www.xindun-power.com/uploadfile/2024/08/28/202408281528217092.jpg",
    "wf_loads": "https://www.xindun-power.com/uploadfile/2024/08/28/202408281730337751.jpg",
    "ess_prod": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/ESSSolarWechselrichter.jpg",
    "ess_notes": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/WieManSolarWechselrichterVerwendetESS.jpg",
    "essli_prod": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151150396319.jpg",
    "zrs_family": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/ZRSSolarWechselrichter-00a7a.jpg",
    "zrs_old": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/WieManSolarWechselrichterVerwendetZRS-9939e.jpg",
    "hdsx_family": "https://www.xindun-power.com/uploadfile/upload/2022-08/04/HDSXSolarWechselrichter.jpg",
    "hdsx_simple": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/WieManSolarWechselrichterVerwendetHDSX.jpg",
    "c1": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/xindunoffgridsolarwechselrichter_01.jpg",
    "c2": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/xindunoffgridsolarwechselrichter_02.jpg",
    "c3": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/xindunoffgridsolarwechselrichter_03.jpg",
    "c4": "https://www.xindun-power.com/uploadfile/upload/2022-08/05/xindunoffgridsolarwechselrichter_04.jpg",
}

DUOMI_BY_URL = {
    U["hero_de"]: _BANNER_DE,
    U["lf_wall"]: _LF_WALL,
    U["df"]: _DF,
    U["df2"]: _DF,
    U["ls"]: _LS_LOADS,
    U["hdsx"]: _HDSX,
    U["essli"]: _ESS_WHITE,
    U["hfp"]: _HFP,
    U["wd"]: _WD_RICE,
    U["hdsx3"]: _HDSX,
    U["wf"]: _WF,
    U["zrs"]: _ZRS,
    U["wd6"]: _WD_HAMMER,
    U["ess"]: _ESS_CABINET,
    U["hf"]: _HF,
    U["zrs20"]: _ZRS,
    U["banner_de"]: _BANNER_DE,
    U["hpplus_1"]: _HP_HOME,
    U["hpplus_p"]: _PARALLEL3,
    U["units"]: _UNITS,
    U["p123"]: _P123,
    U["hfp_title"]: _HFP_TITLE,
    U["hpprot"]: _HPPROT,
    U["hp_rear"]: _HP_REAR,
    U["ls_blue"]: _LS_BLUE,
    U["ct"]: _CT,
    U["wd_yellow"]: _WD_YELLOW,
    U["wf_loads"]: _WF_LOADS,
    U["ess_notes"]: _ESS_NOTES,
    U["zrs_old"]: _ZRS,
    U["hdsx_simple"]: _HDSX_SIMPLE,
    U["c1"]: _COLLAGE1,
    U["c2"]: _COLLAGE2,
    U["c3"]: _COLLAGE3,
    U["c4"]: _CERTS,
}

IMAGE_SOURCES = [
    [
        _im(U["hero4"], "Что может питать солнечный инвертор на 4 кВт"),
        _im(U["lf_wall"], "Солнечный инвертор LF на 4 кВт"),
        _im(U["df"], "Схема подключения солнечного инвертора DF на 4 кВт"),
        _im(U["df2"], "Солнечный инвертор WF на 4 кВт от Xindun"),
        _im(U["ls"], "Солнечный инвертор LS на 4 кВт с разделённой фазой"),
        _im(U["hdsx"], "Трёхфазный солнечный инвертор HDSX на 4 кВт"),
        _im(U["essli"], "Портативный солнечный генератор ESS-Li на 4 кВт"),
        _im(U["hfp"], "Гибридный солнечный инвертор HFP на 4 кВт"),
        _im(U["use4"], "Где применяют солнечный инвертор на 4 кВт"),
        _im(U["office"], "Офис компании Xindun Power"),
        _im(U["factory"], "Завод инверторов в Китае"),
    ],
    [
        _im(U["hero15"], "Что может питать солнечный инвертор на 15 кВт"),
        _im(U["wd_prod"], "Инвертор WD на 15 кВт"),
        _im(U["wd"], "Низкочастотный солнечный инвертор WD на 15 кВт"),
        _im(U["hdsx_prod"], "Трёхфазный солнечный инвертор на 15 кВт"),
        _im(U["hdsx3"], "Как подключить трёхфазный инвертор на 15 кВт"),
        _im(U["wf_prod"], "Низкочастотный инвертор на 15 кВт"),
        _im(U["wf"], "Схема подключения инвертора на 15 кВт"),
        _im(U["zrs_prod"], "Инвертор серии ZRS на 15 кВт"),
        _im(U["zrs"], "Схема подключения инвертора ZRS на 15 кВт"),
        _im(U["use15"], "Куда ставят солнечный инвертор на 15 кВт"),
        _im(U["office"], "Китайская компания солнечных инверторов"),
        _im(U["factory"], "Производитель инверторов"),
    ],
    [
        _im(U["hero6"], "Как выбрать лучший солнечный инвертор на 6 кВт"),
        _im(U["lf_wall"], "Солнечный инвертор LF на 6 кВт из Китая"),
        _im(U["df"], "Низкочастотный солнечный инвертор DF на 6 кВт"),
        _im(U["df2"], "Силовой инвертор WF на 6 кВт"),
        _im(U["ls"], "Низкочастотный инвертор LS на 6 кВт"),
        _im(U["wd6"], "Инвертор для солнечных панелей WD на 6 кВт"),
        _im(U["essli"], "Солнечный генератор ESS-Li на 6 кВт с китайского завода"),
        _im(U["ess"], "Солнечный генератор ESS всё в одном"),
        _im(U["hf"], "Гибридный инвертор HF"),
        _im(U["hfp"], "Гибридный солнечный инвертор HFP"),
        _im(U["use6"], "Установка солнечного инвертора на 6 кВт"),
        _im(U["office"], "Офис Xindun Power в Китае"),
        _im(U["factory"], "Завод по производству солнечных инверторов на 6 кВт"),
    ],
    [
        _im(U["hero20"], "Почему инвертор на 20 кВт подходит для автономной системы"),
        _im(U["wf"], "Схема подключения солнечного инвертора на 20 кВт"),
        _im(U["app_wf"], "Установка солнечного инвертора на 20 кВт"),
        _im(U["wd"], "Как работает солнечный инвертор"),
        _im(U["app_wd"], "Где уместен солнечный инвертор на 20 кВт"),
        _im(U["hdsx3"], "Как работает инвертор на 20 кВт"),
        _im(U["app_hdsx"], "Установка трёхфазного инвертора на 20 кВт"),
        _im(U["zrs20"], "Преобразование постоянного тока в переменный на 20 кВт"),
        _im(U["app_zrs"], "Применение инвертора Xindun на 20 кВт"),
        _im(U["hq"], "Штаб-квартира Xindun в Фошане, провинция Гуандун, Китай"),
        _im(U["shop"], "OEM-завод инверторов"),
    ],
    [
        _im(U["hero_de"], "Автономный солнечный PV-инвертор — XINDUN Китай"),
        _im(U["banner_de"], "Автономный солнечный PV-инвертор XINDUN Китай"),
        _im(U["hpplus"], "Автономный солнечный инвертор HP PLUS"),
        _im(U["hpplus_1"], "Как пользоваться автономным PV-инвертором без параллели"),
        _im(U["hpplus_p"], "Параллельное подключение автономного PV-инвертора"),
        _im(U["hpplus2"], "Автономный солнечный инвертор HP PLUS+"),
        _im(U["units"], "Параллельная работа с однофазным выходом"),
        _im(U["p123"], "Параллельная работа с трёхфазным выходом"),
        _im(U["hfp_prod"], "Автономный солнечный инвертор HFP"),
        _im(U["hfp_title"], "Как пользоваться PV-инвертором HFP"),
        _im(U["hpprot_prod"], "Автономный солнечный инвертор HP PRO-T"),
        _im(U["hpprot"], "Как пользоваться PV-инвертором HP PRO-T"),
        _im(U["hp_prod"], "Автономный солнечный инвертор HP"),
        _im(U["hp_rear"], "Как пользоваться инвертором HP"),
        _im(U["ls_prod"], "Автономный солнечный инвертор LS"),
        _im(U["ls_blue"], "Как пользоваться инвертором LS"),
        _im(U["ct_prod"], "Автономный солнечный инвертор CT"),
        _im(U["ct"], "Как пользоваться инвертором CT"),
        _im(U["wd_family"], "Автономный солнечный инвертор WD"),
        _im(U["wd_yellow"], "Как пользоваться инвертором WD"),
        _im(U["df_prod"], "Автономный солнечный инвертор DF"),
        _im(U["df"], "Как пользоваться инвертором DF"),
        _im(U["lf_prod"], "Автономный солнечный инвертор LF"),
        _im(U["lf_wall"], "Как пользоваться инвертором LF"),
        _im(U["wf_family"], "Автономный солнечный инвертор WF"),
        _im(U["wf_loads"], "Как пользоваться инвертором WF"),
        _im(U["ess_prod"], "Автономный солнечный инвертор ESS"),
        _im(U["ess_notes"], "Как пользоваться инвертором ESS"),
        _im(U["essli_prod"], "Автономный солнечный инвертор ESS-Li"),
        _im(U["essli"], "Как пользоваться инвертором ESS-Li"),
        _im(U["zrs_family"], "Автономный солнечный инвертор ZRS"),
        _im(U["zrs_old"], "Как пользоваться инвертором ZRS"),
        _im(U["hdsx_family"], "Автономный солнечный инвертор HDSX"),
        _im(U["hdsx_simple"], "Как пользоваться трёхфазным PV-инвертором"),
        _im(U["c1"], "Завод солнечных инверторов Xindun в Китае"),
        _im(U["c2"], "Контроль качества на заводе Xindun"),
        _im(U["c3"], "Клиенты производителя автономных инверторов Xindun"),
        _im(U["c4"], "Сертификаты автономных солнечных инверторов Xindun"),
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
