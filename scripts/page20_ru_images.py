#!/usr/bin/env python3
"""Prepare page 20 Russian images.

Duomi gpt-image-2 only for English marketing headlines and diagram labels.
Product photos whose only English is casing, logo or model text are compressed.
The red «New» ribbon is a marketing overlay and is translated. Product casing text stays.
"""

from __future__ import annotations

import page18_ru_images as base

PAGE_NUM = 20

_KEEP = (
    "Do NOT change the xindun logo, Xindun GREEN POWER, product casing text, "
    "model numbers, CE or ISO marks, display readings, button labels, ports, "
    "wire colors, arrows or icons. Do not move products. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a marketing banner: a sailboat on the left and a white-and-black inverter on a white curve at the right, with a green panel. "
        "Translate only the two-line white headline on the green panel. "
        "Line 1: 'Sailboat' → 'Парусная'. Line 2: 'Inverter' → 'яхта: инвертор'. "
        "Keep two lines, white type, and the green panel. " + _KEEP
    ),
    (0, 1): (
        "This is a square marketing banner: a sailboat on the left and an inverter on a white curve, with a green panel. "
        "Translate only the three-line white headline. "
        "Line 1: 'What is' → 'Что такое'. "
        "Line 2: 'Sailboat' → 'инвертор'. "
        "Line 3: 'Inverter?' → 'для яхты?'. "
        "Keep three lines and the green panel. " + _KEEP
    ),
    (1, 0): (
        "This is a wide marketing banner of three white inverters in front of solar panels and a blue sky. "
        "Translate only the yellow headline. "
        "'Can Single Phase Inverter Output 380V AC?' → 'Может ли однофазный инвертор выдавать 380 В AC?'. "
        "Keep it one yellow line in the same place. Keep the xindun logo and GREEN POWER. "
        "Do NOT change 'HYBRID SOLAR INVERTER' on the units. " + _KEEP
    ),
    (1, 1): (
        "This is the same wide marketing banner of three white inverters, a slightly taller crop. "
        "Translate only the yellow headline. "
        "'Can Single Phase Inverter Output 380V AC?' → 'Может ли однофазный инвертор выдавать 380 В AC?'. "
        "Keep it one yellow line. Keep the xindun logo and GREEN POWER. "
        "Do NOT change 'HYBRID SOLAR INVERTER' on the units. " + _KEEP
    ),
    (1, 2): (
        "This image has a product photo on the left and a wiring diagram on the right. "
        "Translate only the English diagram labels on the right. "
        "'solar panel' → 'солнечная панель'. "
        "'mains' → 'сеть'. 'OR' → 'ИЛИ'. "
        "'Diesel/gasoline generator' → 'дизельный/бензиновый генератор'. "
        "'battery' → 'аккумулятор'. "
        "'fridge' → 'холодильник'. "
        "'washing machine' → 'стиральная машина'. "
        "'air conditioner' → 'кондиционер'. "
        "'water heater' → 'водонагреватель'. "
        "'water pump' → 'водяной насос'. "
        "Do NOT change 'HYBRID SOLAR INVERTER' printed on either white unit. " + _KEEP
    ),
    (1, 3): (
        "This is a wiring diagram of three inverters with a three-phase parallel output. "
        "Translate only the English overlay labels. "
        "Headline: 'Single phase inverter with three phase output in parallel' → "
        "'Однофазный инвертор с трёхфазным выходом в параллели'. "
        "'battery' → 'аккумулятор'. 'mains' → 'сеть'. 'loads' → 'нагрузка'. "
        "Keep N, L1, L2, L3, plus and minus signs. "
        "Do NOT change 'HYBRID SOLAR INVERTER' on the units. " + _KEEP
    ),
    (1, 4): (
        "This is a wiring diagram of three inverters paralleled to expand power. "
        "Translate only the English overlay labels. "
        "Headline: 'Single phase inverter with power expansion in parallel' → "
        "'Однофазный инвертор с наращиванием мощности в параллели'. "
        "'battery' → 'аккумулятор'. 'mains' → 'сеть'. 'loads' → 'нагрузка'. "
        "Keep N and L. Do NOT change 'HYBRID SOLAR INVERTER' on the units. " + _KEEP
    ),
    (2, 0): (
        "This is a marketing banner of two white inverters in front of solar panels. "
        "Translate only the two-line yellow headline at the bottom. "
        "Line 1: 'Can The Inverter Be' → 'Можно ли инвертор'. "
        "Line 2: 'Operated With Overload?' → 'эксплуатировать с перегрузкой?'. "
        "Keep the translucent bar and the yellow type. Keep the xindun logo and GREEN POWER. "
        "Do NOT change 'HYBRID SOLAR INVERTER' on the units. " + _KEEP
    ),
    (2, 1): (
        "This is a taller crop of the same two-inverter marketing banner. "
        "Translate only the two-line yellow headline. "
        "Line 1: 'Can The Inverter Be' → 'Можно ли инвертор'. "
        "Line 2: 'Operated With Overload?' → 'эксплуатировать с перегрузкой?'. "
        "Keep the xindun logo and GREEN POWER. "
        "Do NOT change 'HYBRID SOLAR INVERTER' on the units. " + _KEEP
    ),
    (2, 2): (
        "This is a studio photo of one white hybrid inverter. "
        "The only marketing overlay is the red corner ribbon that says 'New'. "
        "Translate that single word to 'Новинка' and keep the red ribbon in the same corner. "
        "Do NOT change 'HYBRID SOLAR INVERTER', the xindun logo, GREEN POWER, CE or ISO. " + _KEEP
    ),
    (2, 3): (
        "This is a studio photo of one white hybrid inverter with a dark display. "
        "The only marketing overlay is the red corner ribbon that says 'New'. "
        "Translate that single word to 'Новинка' and keep the red ribbon in the same corner. "
        "Do NOT change 'HYBRID SOLAR INVERTER', the xindun logo, GREEN POWER, CE or ISO. " + _KEEP
    ),
    (3, 0): (
        "This is a marketing banner of many orange and white solar charge controllers. "
        "Translate only the two-line headline. "
        "Line 1, green: 'PWM & MPPT' → 'PWM и MPPT'. "
        "Line 2, black: 'Solar Charge Controller' → 'Солнечный контроллер заряда'. "
        "Do NOT change text printed on the product casings, including MPPT, Solar Charge Controller and Solar controller. " + _KEEP
    ),
    (3, 1): (
        "This is a taller marketing banner of the same controller family. "
        "Translate only the two-line headline. "
        "Line 1, green: 'PWM & MPPT' → 'PWM и MPPT'. "
        "Line 2: 'Solar Charge Controller' → 'Солнечный контроллер заряда'. "
        "Do NOT change text printed on the product casings. " + _KEEP
    ),
    (3, 2): (
        "This is a wiring diagram of a black PWM solar controller. "
        "Translate only the three captions under the icons. "
        "'SOLAR PANEL' → 'СОЛНЕЧНАЯ ПАНЕЛЬ'. "
        "'BATTERY' → 'АККУМУЛЯТОР'. "
        "'DC LOAD' → 'НАГРУЗКА DC'. "
        "Do NOT change 'PWM Solar Controller' printed on the device, the SET button, or the display. " + _KEEP
    ),
    (3, 3): (
        "This is a diagram of a blue inverter feeding three load groups. "
        "Translate only the English labels. "
        "'INVERTER' → 'ИНВЕРТОР'. "
        "'AC LOAD' → 'НАГРУЗКА AC'. "
        "'Household Electric Appliances' → 'Бытовые электроприборы'. "
        "'Office Equipment' → 'Офисная техника'. "
        "'Industrial Equipment' → 'Промышленное оборудование'. " + _KEEP
    ),
    (3, 4): (
        "This is a wiring diagram of an orange MPPT controller. "
        "Translate only the captions outside the product. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'DC Load' → 'Нагрузка DC'. "
        "'Inverter' → 'Инвертор'. "
        "On each of the four battery icons, '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
        "Do NOT change text printed on the orange controller: MPPT SOLAR CONTROLLER, "
        "MPPT Solar Charge Controller, SOLAR, BATTERY, DC LOAD, TEMP SENSOR, RS485, or the display. " + _KEEP
    ),
    (3, 5): (
        "This is a wiring diagram of a white MPPT controller. "
        "Translate only the captions outside the product. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'DC Load' → 'Нагрузка DC'. "
        "On each battery icon, '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
        "Do NOT change 'MPPT Solar Charge Controller' on the casing, terminal words SOLAR, BATTERY, DC LOAD, PE, MENU, SET, or the display. " + _KEEP
    ),
    (4, 0): (
        "This is a marketing banner of five inverters on grass under solar panels. "
        "Translate only the white headline inside the green rounded banner. "
        "Line 1: 'What's The Difference Between' → 'В чём разница между'. "
        "Line 2: 'Solar Charge Controller And Inverter?' → 'контроллером заряда и инвертором?'. "
        "Keep the green pill shape. Do NOT change text on the product casings. " + _KEEP
    ),
    (4, 1): (
        "This is a wider crop of the same five-inverter banner. "
        "Translate only the white headline inside the green rounded banner. "
        "Line 1: 'What's The Difference Between' → 'В чём разница между'. "
        "Line 2: 'Solar Charge Controller And Inverter?' → 'контроллером заряда и инвертором?'. "
        "Do NOT change text on the product casings. " + _KEEP
    ),
    (4, 2): (
        "This is a wiring diagram under a white MPPT controller. "
        "Translate only the captions outside the product. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'DC Load' → 'Нагрузка DC'. "
        "On each battery icon, '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
        "Do NOT change 'MPPT Solar Charge Controller' or the terminal words SOLAR, BATTERY, DC LOAD, PE. " + _KEEP
    ),
    (4, 3): (
        "This is a system diagram around a white hybrid inverter. "
        "Translate only the English diagram labels. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Battery' → 'Аккумулятор'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "Both 'AC Loads' labels → 'Нагрузка AC'. "
        "Do NOT change 'HYBRID SOLAR INVERTER' on the white unit or text on the small battery unit. " + _KEEP
    ),
    (4, 4): (
        "This is a parallel-wiring diagram of three inverters. "
        "Translate only the English labels. "
        "Headline: 'Parallel operation support single phase output' → 'Параллельная работа, однофазный выход'. "
        "'Unit 1' → 'Блок 1'. 'Unit 2' → 'Блок 2'. 'Unit 3' → 'Блок 3'. "
        "'Battery' → 'Аккумулятор'. 'Utility Grid' → 'Электросеть'. 'Loads' → 'Нагрузка'. "
        "Keep N and L. Do NOT change text on the inverter casings. " + _KEEP
    ),
    (4, 5): (
        "This is a parallel-wiring diagram of nine inverters in three phases. "
        "Translate only the English labels. "
        "Headline: 'Parallel operation support three phase output' → 'Параллельная работа, трёхфазный выход'. "
        "Keep P1, P2 and P3 as they are. "
        "'Battery' → 'Аккумулятор'. 'Utility Grid' → 'Электросеть'. 'Loads' → 'Нагрузка'. "
        "Keep N, L1, L2 and L3. Do NOT change text on the inverter casings. " + _KEEP
    ),
    (4, 6): (
        "This is a wiring diagram of a blue LS inverter. "
        "Translate only the English diagram labels. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'AC INPUT' → 'ВХОД AC'. "
        "'Generator' → 'Генератор'. "
        "'AC OUTPUT' → 'ВЫХОД AC'. "
        "'LAPTOP' → 'НОУТБУК'. 'LAMP' → 'ЛАМПА'. 'PRINTER' → 'ПРИНТЕР'. "
        "'TV' → 'ТЕЛЕВИЗОР'. 'FAN' → 'ВЕНТИЛЯТОР'. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
        "Do NOT change text printed on the blue inverter. " + _KEEP
    ),
    (4, 7): (
        "This is a wiring diagram of a white low-frequency inverter. "
        "Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'AC Input' → 'Вход AC'. 'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'AC Output' → 'Выход AC'. "
        "'Laptop' → 'Ноутбук'. 'Printer' → 'Принтер'. 'TV' → 'Телевизор'. "
        "'Fans' → 'Вентиляторы'. 'Water pump' → 'Водяной насос'. "
        "'Battery' → 'Аккумулятор'. "
        "Do NOT change 'Low Frequency Inverter' or 'Pure Sine Wave' printed on the white unit. " + _KEEP
    ),
}


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


IMAGE_SOURCES: list[list[dict]] = [
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/20250220140645A2Kmfi.jpg",
            "Инвертор для парусной яхты",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201407132217.jpg",
            "Что такое инвертор для парусной яхты",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/21/202502211406445760.jpg",
            "Солнечный инвертор DF для парусной яхты",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/21/202502211400109163.jpg",
            "Инвертор ESS для парусной яхты",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/21/202502211355045562.jpg",
            "Цена инвертора ESS-Li для парусной яхты",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/21/202502211400321862.jpg",
            "Лучший инвертор GP-C для парусной яхты",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/21/202502211401448412.jpg",
            "Инвертор WD для парусной яхты",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/20250220145402Tr8AIi.jpg",
            "Может ли однофазный инвертор выдавать 380 В AC",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201441287335.jpg",
            "Солнечный инвертор 380 В",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201442206592.jpg",
            "Схема однофазного солнечного инвертора 380 В",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201703528517.png",
            "Параллель однофазного инвертора с трёхфазным выходом",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201701056468.jpg",
            "Параллельное наращивание мощности однофазного инвертора",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/20250220150231xStX8w.jpg",
            "Можно ли эксплуатировать инвертор с перегрузкой",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201503382289.jpg",
            "Перегрузка инвертора",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201506263090.jpg",
            "Гибридный инвертор HFP и перегрузка",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201505107818.jpg",
            "Инвертор HP PLUS+ и перегрузка",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201646229701.jpg",
            "Низкочастотный инвертор LF при перегрузке",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201646361956.jpg",
            "Трёхфазный инвертор HDSX при перегрузке",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/13/20250213171114Sz8upr.jpg",
            "Солнечный контроллер заряда PWM и MPPT",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/13/202502131711445211.jpg",
            "Контроллер заряда аккумулятора для инвертора",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/13/202502131713281425.jpg",
            "Схема ШИМ-контроллера KY1",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/13/202502131714067401.jpg",
            "Схема нагрузки инвертора",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/13/202502131716331967.jpg",
            "Схема контроллера MPPT Wonder1",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/13/202502131717295641.jpg",
            "Схема контроллера MPPT Wonder2",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/01/20/20250120144429omHfsk.jpg",
            "Разница между контроллером заряда и инвертором",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/01/20/202501201445547101.jpg",
            "Контроллер заряда солнечной панели и инвертор",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/01/20/202501201447162694.jpg",
            "Контроллер заряда Wonder2 всё в одном",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/11/01/202411011553297878.jpg",
            "Гибридный солнечный инвертор HFP чистой синусоиды",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/09/29/202409291439493192.jpg",
            "Параллельная работа с однофазным выходом",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/09/29/202409291440508234.jpg",
            "Параллельная работа с трёхфазным выходом",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/01/20/202501201454429424.jpg",
            "Автономный инвертор чистой синусоиды LS",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410311109218818.jpg",
            "Инвертор WF чистой синусоиды и контроллер заряда",
        ),
    ],
]

IMAGE_LOG = base.IMAGE_LOG


def prepare_all():
    base.PAGE_NUM = PAGE_NUM
    base.DUOMI_MAP = DUOMI_MAP
    base.IMAGE_SOURCES = IMAGE_SOURCES
    base.IMAGE_LOG.clear()
    return base.prepare_all()


if __name__ == "__main__":
    import json

    prepare_all()
    print(json.dumps(base.IMAGE_LOG, ensure_ascii=False, indent=2))
