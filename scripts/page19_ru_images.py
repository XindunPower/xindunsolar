#!/usr/bin/env python3
"""Prepare page 19 Russian images.

Listing heroes differ from the in-article pictures. Index 0 of each article is
the listing hero and is uploaded only as featured_media.
Duomi gpt-image-2 only for English marketing headlines and diagram labels.
The factory collage and the installation photo have no English marketing overlay
and are compressed only.
"""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from page1_ru_images import (  # noqa: E402
    OUT,
    USED_FILE_STEMS,
    compress_only,
    run_duomi,
    slugify,
)

UA = "Mozilla/5.0 (compatible; XindunRussianBot/1.0)"
PAGE_NUM = 19

_KEEP = (
    "Do NOT change the xindun logo, Xindun GREEN POWER, product casing text, "
    "model numbers, CE marks, display readings, button labels, terminal letters "
    "N L A B C, wire colors, or words printed on the product such as "
    "HYBRID SOLAR INVERTER, Low Frequency PV Inverter, MPPT Solar Charge Controller, "
    "or SOLAR GENERATOR. Do not move products, arrows, wires or icons. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "Wide green marketing banner of four white hybrid inverters. "
        "Translate only the green headline '3.3 KW INVERTER?' → 'ИНВЕРТОР 3,3 КВТ?'. "
        "Keep it one line at the top. " + _KEEP
    ),
    (0, 1): (
        "Portrait marketing poster, green background, four white inverters, red NEW badge. "
        "Translate only the overlay text. "
        "'NEW' → 'НОВИНКА'. "
        "'WHAT IS' → 'КАКОЙ'. "
        "'THE BEST' → 'ЛУЧШИЙ'. "
        "'3.3 KW INVERTER?' → 'ИНВЕРТОР 3,3 КВТ?'. "
        "Keep the three-line headline and the red badge. " + _KEEP
    ),
    (0, 2): (
        "Wiring diagram of an HFP hybrid inverter. Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Battery' → 'Аккумулятор'. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "'AC Loads' → 'Нагрузки AC' (both occurrences). "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "The gold line on the inverter must stay 'HYBRID SOLAR INVERTER'. " + _KEEP
    ),
    (0, 3): (
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
        "Keep red dotted arrows and icons. " + _KEEP
    ),
    (0, 4): (
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
        "'Uninterrupted Power Supply(Main Output)' → 'Бесперебойное питание (основной выход)'. "
        "'Uninterrupted Power Supply(Second Output)' → 'Бесперебойное питание (второй выход)'. "
        "Keep the green ring and red dotted arrows. " + _KEEP
    ),
    (0, 5): (
        "Wiring diagram of an HFP-E hybrid inverter with a detachable panel. "
        "Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор для сети и автономии'. "
        "'Power Grid' → 'Электросеть'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'AC Loads' → 'Нагрузки AC'. "
        "'Uninterrupted Power Supply(Main Output)' → 'Бесперебойное питание (основной выход)'. "
        "'Uninterrupted Power Supply(Second Output)' → 'Бесперебойное питание (второй выход)'. "
        "Do not change the word INVERTER on the green circle of the unit. " + _KEEP
    ),
    (0, 6): (
        "Green collage poster of hybrid inverter installations. "
        "Translate only the white and yellow overlay text. "
        "'HYBRID INVERTER' → 'ГИБРИДНЫЙ ИНВЕРТОР'. "
        "'Remote Area / Home Office / Farm Agriculture' → 'Удалённый район / Домашний офис / Сельское хозяйство'. "
        "'Emergency Backup Power /' → 'Аварийный резерв /'. "
        "'RV Campervan' → 'Автодом'. "
        "Keep the photo circles and the green background. " + _KEEP
    ),
    (1, 0): (
        "Wide banner: white, black and yellow inverters in front of solar panels. "
        "Translate only the headline and the two orange badges. "
        "'INVERTER' → 'ИНВЕРТОР'. "
        "'10kva 96v inverter' → 'инвертор 10 кВА 96 В'. "
        "'15kva 96v inverter' → 'инвертор 15 кВА 96 В'. "
        "Keep the two orange pills. " + _KEEP
    ),
    (1, 1): (
        "Wide banner, same three inverters. Translate only the white headline and the two orange badges. "
        "'LOW FREQUENCY' → 'НИЗКОЧАСТОТНЫЙ'. "
        "'INVERTER' → 'ИНВЕРТОР'. "
        "'10kva 96v inverter' → 'инвертор 10 кВА 96 В'. "
        "'15kva 96v inverter' → 'инвертор 15 кВА 96 В'. "
        "Keep the two-line headline and both orange pills. " + _KEEP
    ),
    (1, 2): (
        "Three-phase cabinet wiring diagram. Translate only the English diagram labels. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'PV COMBINER' → 'КОМБАЙНЕР PV'. "
        "'SOLAR CONTROLLER' → 'СОЛНЕЧНЫЙ КОНТРОЛЛЕР'. "
        "'12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч' on every battery. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
        "'INVERTER' → 'ИНВЕРТОР'. "
        "'3-PHASE LOADS' → 'ТРЁХФАЗНЫЕ НАГРУЗКИ'. "
        "'1-PHASE LOADS' → 'ОДНОФАЗНЫЕ НАГРУЗКИ'. "
        "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
        "'BREAKER' → 'АВТОМАТ'. "
        "'Earth Wire (GND)' → 'Заземление (GND)'. "
        "Keep A Phase, B Phase, C Phase, N and the colored wires. "
        "Do not change text printed on the orange controller. " + _KEEP
    ),
    (1, 3): (
        "WD low-frequency inverter wiring diagram. Translate only the English diagram labels. "
        "'RS232 (Optional)' → 'RS232 (опция)'. "
        "'RS485 (Optional)' → 'RS485 (опция)'. "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Solar Controller' → 'Солнечный контроллер'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'Ground Line' → 'Заземление'. "
        "'Rice cooker' → 'Рисоварка'. "
        "'Water dispenser' → 'Кулер'. "
        "'Electromagnetic furnace' → 'Индукционная плита'. "
        "'Refrigerator' → 'Холодильник'. "
        "'AIR CONDITIONER' → 'КОНДИЦИОНЕР'. "
        "Do not change text printed on the white inverter or the orange controller. " + _KEEP
    ),
    (1, 4): (
        "WF inverter wiring diagram. Translate only the English diagram labels. "
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
    ),
    (2, 0): (
        "Wide product banner of a black three-phase cabinet between solar panels. "
        "Translate only the white headline 'Solar Power System' → 'Солнечная энергосистема'. "
        "Keep it one line. Do not change the cabinet, panels or sky. " + _KEEP
    ),
    (2, 1): (
        "Square product banner, blue background, black cabinet and solar panels. "
        "Translate only the two headline lines on the green and white bars. "
        "'Three Phase Inverter' → 'Трёхфазный инвертор'. "
        "'Solar Power System' → 'Солнечная энергосистема'. "
        "Keep the two bars. Do not change the cabinet. " + _KEEP
    ),
    (3, 0): (
        "Banner of a black cabinet in a greenhouse with irrigation sprinklers. "
        "Translate only the white headline. "
        "'What Solar System' → 'Какая солнечная система'. "
        "'Suitable For Irrigation?' → 'подходит для полива?'. "
        "Keep the two-line layout. " + _KEEP
    ),
    (3, 1): (
        "Same greenhouse banner as the listing hero, used again in the article. "
        "Translate only the white headline. "
        "'What Solar System' → 'Какая солнечная система'. "
        "'Suitable For Irrigation?' → 'подходит для полива?'. "
        "Keep the two-line layout. " + _KEEP
    ),
    (3, 2): (
        "WD irrigation wiring diagram. Translate only the English diagram labels. "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'RS232 (Optional)' → 'RS232 (опция)'. "
        "'RS485 (Optional)' → 'RS485 (опция)'. "
        "'Water Pump' → 'Водяной насос'. "
        "'Percussion Drill' → 'Перфоратор'. "
        "'Irrigator' → 'Поливная установка'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Solar Controller' → 'Солнечный контроллер'. "
        "'Ground Line' → 'Заземление'. "
        "'Battery' → 'Аккумулятор'. "
        "Do not change text printed on the products. " + _KEEP
    ),
    (3, 3): (
        "WF irrigation wiring diagram, black cabinet. Translate only the English diagram labels. "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'RS232 (Optional)' → 'RS232 (опция)'. "
        "'RS485-1 (Optional)' → 'RS485-1 (опция)'. "
        "'RS485-2 (Optional)' → 'RS485-2 (опция)'. "
        "'Water Pump' → 'Водяной насос'. "
        "'Percussion Drill' → 'Перфоратор'. "
        "'Irrigator' → 'Поливная установка'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Ground Line' → 'Заземление'. "
        "'Battery' → 'Аккумулятор'. "
        "Do not change text printed on the cabinet. " + _KEEP
    ),
    (3, 4): (
        "HDSX irrigation cabinet diagram. Translate only the English diagram labels. "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'AC Loads' → 'Нагрузки AC'. "
        "'Water Pump' → 'Водяной насос'. "
        "'Percussion Drill' → 'Перфоратор'. "
        "'Irrigator' → 'Поливная установка'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Solar Controller' → 'Солнечный контроллер'. "
        "'Ground Line' → 'Заземление'. "
        "'Battery' → 'Аккумулятор'. "
        "'A Phase' → 'Фаза A'. "
        "'B Phase' → 'Фаза B'. "
        "'C Phase' → 'Фаза C'. "
        "Keep the letter N. Do not change MPPT printed on the orange controller. " + _KEEP
    ),
    (4, 0): (
        "Banner of a small boat with solar panels. Translate only the two-line headline. "
        "'How To Choose' → 'Как выбрать'. "
        "'The Boat Solar Panel System?' → 'солнечную систему для лодки?'. "
        "Keep the two-line layout, white and yellow type, the boat and the sky. " + _KEEP
    ),
    (4, 1): (
        "Same boat banner as the listing hero, used again in the article. "
        "Translate only the two-line headline. "
        "'How To Choose' → 'Как выбрать'. "
        "'The Boat Solar Panel System?' → 'солнечную систему для лодки?'. "
        "Keep the boat, panels and sky. " + _KEEP
    ),
    (4, 2): (
        "DF boat inverter wiring diagram. Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'AC Output' → 'Выход AC'. "
        "'Refrigerator' → 'Холодильник'. "
        "'Fan heater' → 'Тепловентилятор'. "
        "'Air conditioner' → 'Кондиционер'. "
        "'Heater' → 'Нагреватель'. "
        "'Percussion drill' → 'Перфоратор'. "
        "'AC Input' → 'Вход AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'Battery' → 'Аккумулятор'. "
        "Do not change text printed on the white inverter. " + _KEEP
    ),
    (4, 3): (
        "ESS portable solar generator wiring diagram. Translate only the English diagram labels. "
        "Top title, including the misspelling: "
        "'Solar Generrtor: Built-in 500W 12V inverter' → 'Солнечный генератор: встроенный инвертор 500 Вт 12 В'. "
        "'+12V 20A PWM+1pc 12V 50Ah Gel battery' → '+ ШИМ 12 В 20 А + 1 шт. гелевый аккумулятор 12 В 50 А·ч'. "
        "'Diesel generators' → 'Дизельные генераторы'. "
        "'Power Grid' → 'Электросеть'. "
        "'OR' → 'или'. "
        "'Breaker' → 'Автомат'. "
        "'1pcs 160W solar panel' → '1 шт. панель 160 Вт'. "
        "'Live Wire(L)' → 'Фаза (L)' everywhere. "
        "'Neutral Wire(N)' → 'Ноль (N)' everywhere. "
        "'USB 5V Loads (DC 5V Output)' → 'Нагрузки USB 5 В (выход DC 5 В)'. "
        "'DC Loads (DC 12V Output)' → 'Нагрузки DC (выход DC 12 В)'. "
        "'AC Loads' → 'Нагрузки AC'. "
        "'Battery negative (connected to the black wire)' → 'Минус аккумулятора (чёрный провод)'. "
        "'Battery positive (connected to the red wire)' → 'Плюс аккумулятора (красный провод)'. "
        "'12V50Ah Battery' → 'Аккумулятор 12 В 50 А·ч'. "
        "Keep 4mm². Do NOT change 'SOLAR GENERATOR' printed on the black unit. " + _KEEP
    ),
    (4, 4): (
        "WD boat system wiring diagram. Translate only the English diagram labels. "
        "'Battery' → 'Аккумулятор'. "
        "'12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч' on every battery. "
        "'Power Grid' → 'Электросеть'. "
        "'Breaker' → 'Автомат'. "
        "'Solar Inverter' → 'Солнечный инвертор'. "
        "'solar panel' → 'солнечная панель'. "
        "'3 in 1 out PV combiner' → 'Комбайнер PV, 3 входа / 1 выход'. "
        "'Neutral Wire(N)' → 'Ноль (N)' everywhere. "
        "'Line Wire (L)' → 'Фаза (L)' everywhere. "
        "'Earth Wire(GND)' → 'Заземление (GND)'. "
        "'AC loads' → 'Нагрузки AC'. "
        "Do not change text printed on the white inverter or the combiner box. " + _KEEP
    ),
}


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


IMAGE_SOURCES: list[list[dict]] = [
    [
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/20250317134924a4YP5f.jpg", "Инвертор 3,3 кВт"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/202503171200505916.jpg", "Какой инвертор 3,3 кВт лучший"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011553297878.jpg", "Схема подключения гибридного инвертора HFP 3,3 кВт"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/20/202502201527344688.jpg", "Схема подключения инвертора HFP-S 3,3 кВт"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/20/202502201629492750.jpg", "Схема подключения инвертора HFP-C 3,3 кВт"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/20/202502201531002662.png", "Схема подключения инвертора HFP-E 3,3 кВт"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/202503171344466372.jpg", "Применение гибридного инвертора 3,3 кВт"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/202503171345521368.jpg", "Завод инверторов Xindun"),
    ],
    [
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/20250317142020aSFqKh.jpg", "Инвертор 10 кВА 96 В и 15 кВА 96 В"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/202503171406329737.jpg", "Низкочастотный инвертор 10 кВА и 15 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/202503171407583585.png", "Схема подключения инвертора HDSX 10 кВА 96 В"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/202503171409154714.png", "Схема подключения инвертора WD 15 кВА 96 В"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/202503171410401386.png", "Схема подключения инвертора WF 10 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/17/202503171415559538.jpg", "Пример установки инвертора 10 кВА и 15 кВА"),
    ],
    [
        _im("https://www.xindun-power.com/uploadfile/2025/03/07/20250307160659PfWKTD.jpg", "Солнечная энергосистема 50 кВт"),
        _im("https://www.xindun-power.com/uploadfile/2025/03/07/202503071607263911.jpg", "Трёхфазная солнечная система"),
    ],
    [
        _im("https://www.xindun-power.com/uploadfile/2025/02/15/20250215151912J2oQfT.jpg", "Солнечная система для полива"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/15/202502151505543762.jpg", "Какая солнечная система подходит для полива"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/15/202502151507402887.jpg", "Схема автономной системы WD для полива"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/15/202502151510308833.jpg", "Схема автономной системы WF для полива"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/15/202502151511409964.jpg", "Схема автономной системы HDSX для полива"),
    ],
    [
        _im("https://www.xindun-power.com/uploadfile/2025/02/20/202502201420508Ry4iQ.jpg", "Как выбрать солнечную систему для лодки"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/20/202502201421199136.jpg", "Комплект солнечных панелей для небольшой лодки"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/20/202502201739564872.jpg", "Схема подключения судового комплекта DF"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/20/202502201746394219.jpg", "Схема подключения судового комплекта ESS"),
        _im("https://www.xindun-power.com/uploadfile/2025/02/20/202502201747339324.jpg", "Схема подключения судового комплекта WD"),
    ],
]

IMAGE_LOG: list[dict] = []
def api_size(w: int, h: int) -> str:
    ratio = w / h if h else 1.0
    named = {"1:1": 1.0, "3:2": 1.5, "2:3": 2 / 3, "2:1": 2.0, "16:9": 16 / 9}
    best_name, best_ratio = min(named.items(), key=lambda kv: abs(kv[1] - ratio))
    if abs(best_ratio - ratio) <= 0.03:
        return best_name
    best = None
    for height in range(640, 2048, 16):
        width = int(round((ratio * height) / 16.0)) * 16
        if width < 16 or width > 3840 or height > 3840:
            continue
        pixels = width * height
        if pixels < 655360 or pixels > 8294400:
            continue
        delta = abs((width / height) - ratio)
        if best is None or delta < best[0] - 1e-9 or (abs(delta - best[0]) <= 1e-9 and pixels < best[2]):
            best = (delta, f"{width}x{height}", pixels)
    if best is None:
        return best_name
    return best[1]


def stem_for(alt: str, src: str) -> str:
    base = slugify(alt)
    stem = base
    n = 2
    while True:
        marker = OUT / f"{stem}.method.json"
        jpg = OUT / f"{stem}.jpg"
        clash = stem in USED_FILE_STEMS
        if not clash and jpg.exists() and marker.exists():
            try:
                meta = json.loads(marker.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                meta = {}
            if meta.get("src") not in {None, src}:
                clash = True
        if not clash:
            USED_FILE_STEMS.add(stem)
            return stem
        stem = f"{base}-{n}"
        n += 1


def prepare_one(article_idx: int, img_idx: int, im: dict, stem: str) -> dict:
    ext = Path(im["src"]).suffix.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
        ext = ".jpg"
    local = OUT / f"_src_ru_p{PAGE_NUM}_a{article_idx}_i{img_idx}{ext}"
    if not local.exists() or local.stat().st_size == 0:
        rr = requests.get(im["src"], timeout=60, headers={"User-Agent": UA})
        rr.raise_for_status()
        local.write_bytes(rr.content)
    with Image.open(local) as pil:
        orig_wh = pil.size

    need_duomi = (article_idx, img_idx) in DUOMI_MAP
    method = "duomi" if need_duomi else "compress"
    duomi_path = None
    final: Path
    tagged = OUT / f"{stem}.jpg"
    marker = OUT / f"{stem}.method.json"
    reused = False
    if tagged.exists() and tagged.stat().st_size > 0 and tagged.stat().st_size <= 100 * 1024 and marker.exists():
        meta = json.loads(marker.read_text(encoding="utf-8"))
        with Image.open(tagged) as chk:
            size_ok = chk.size == orig_wh
        expected = "duomi" if need_duomi else "compress"
        stored = meta.get("method")
        method_ok = stored == expected or (need_duomi and stored == "duomi-fallback-original")
        if size_ok and method_ok and meta.get("src") == im["src"]:
            final = tagged
            if stored == "duomi-fallback-original":
                method = "duomi-fallback-original"
            else:
                method = "duomi-reuse" if need_duomi else "compress-reuse"
            duomi_path = meta.get("duomi_path")
            reused = True
            print(f"[img] reuse {tagged.name} method={method}", flush=True)
    if reused:
        pass
    elif need_duomi:
        size = api_size(*orig_wh)
        result = run_duomi(
            im["src"],
            DUOMI_MAP[(article_idx, img_idx)],
            stem,
            size,
            orig_wh,
            local,
            attempts=2,
        )
        if result is None:
            print(f"[duomi] fallback original compress for a{article_idx}_i{img_idx}", flush=True)
            final = compress_only(local, stem, orig_wh)
            method = "duomi-fallback-original"
        else:
            final = result
            duomi_path = str(result)
    else:
        final = compress_only(local, stem, orig_wh)

    if final.stat().st_size > 100 * 1024:
        raise RuntimeError(f"image exceeds 100KB: {final}")
    with Image.open(final) as chk:
        if chk.size != orig_wh:
            raise RuntimeError(f"image dimensions changed for {final}: {chk.size} vs {orig_wh}")

    stored = "compress"
    if method.startswith("duomi") and method != "duomi-fallback-original":
        stored = "duomi"
    if method == "duomi-fallback-original":
        stored = "duomi-fallback-original"
    marker.write_text(
        json.dumps({"method": stored, "src": im["src"], "duomi_path": duomi_path}, ensure_ascii=False),
        encoding="utf-8",
    )
    entry = {
        "article": article_idx,
        "img": img_idx,
        "local": final,
        "alt_ru": im["alt_ru"],
        "title_ru": im["title_ru"],
        "src_orig": im["src"],
        "method": method,
        "duomi_path": duomi_path,
        "orig_wh": orig_wh,
    }
    print(
        f"[img] a{article_idx}_i{img_idx} method={method} -> {final.name} "
        f"{final.stat().st_size}b {orig_wh}",
        flush=True,
    )
    return entry


def prepare_all() -> list[list[dict]]:
    jobs = []
    for article_idx, images in enumerate(IMAGE_SOURCES):
        for img_idx, im in enumerate(images):
            stem = stem_for(im["alt_ru"], im["src"])
            jobs.append((article_idx, img_idx, im, stem))

    prepared_map: dict[tuple[int, int], dict] = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(prepare_one, article_idx, img_idx, im, stem): (article_idx, img_idx)
            for article_idx, img_idx, im, stem in jobs
        }
        for fut in as_completed(futures):
            entry = fut.result()
            prepared_map[(entry["article"], entry["img"])] = entry

    prepared_all: list[list[dict]] = []
    IMAGE_LOG.clear()
    for article_idx, images in enumerate(IMAGE_SOURCES):
        prepared = []
        for img_idx, _im in enumerate(images):
            entry = prepared_map[(article_idx, img_idx)]
            IMAGE_LOG.append(
                {
                    "article": article_idx,
                    "img": img_idx,
                    **{
                        k: (str(v) if k == "local" else list(v) if k == "orig_wh" else v)
                        for k, v in entry.items()
                        if k not in {"article", "img"}
                    },
                }
            )
            prepared.append(entry)
        prepared_all.append(prepared)
    Path(f"/tmp/page{PAGE_NUM}_ru_image_log.json").write_text(
        json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return prepared_all


if __name__ == "__main__":
    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
