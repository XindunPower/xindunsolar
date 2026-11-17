#!/usr/bin/env python3
"""Prepare page 16 Russian images.

Duomi gpt-image-2 only for English marketing headlines and diagram labels.
Product photos, installation photos and factory shots are compressed only.
Product casing text, logos and model marks stay unchanged.
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
PAGE_NUM = 16

_KEEP = (
    "Do NOT change the xindun logo, Xindun GREEN POWER, product casing text, "
    "model numbers, CE marks, display readings, button labels, terminal marks "
    "N L PE, or Chinese characters on walls. Do not move products, arrows, wires or icons. "
    "Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a 3:2 marketing banner: five inverters in front of a house with rooftop solar at sunset. "
        "Translate only the two-line green outlined headline. "
        "Line 1: 'How To Choose' → 'Как выбрать'. "
        "Line 2: 'Solar Inverter For Home?' → 'солнечный инвертор для дома?'. "
        "Keep the house, sunset, solar roof and the five products. " + _KEEP
    ),
    (0, 1): (
        "This is a wiring diagram of one white hybrid inverter. Translate only the English diagram labels. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор сети и автономии'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Battery' → 'Аккумулятор'. "
        "'Power Grid' → 'Электросеть'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "Both 'AC Loads' → 'Нагрузка AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "Do not change HYBRID SOLAR INVERTER printed on the product. " + _KEEP
    ),
    (0, 2): (
        "This is a wiring diagram of a white hybrid inverter with a green ring and two AC outputs. "
        "Translate only the English diagram labels. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор сети и автономии'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'Power Grid' → 'Электросеть'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "'AC Loads' → 'Нагрузка AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'Uninterrupted Power Supply(Main Output)' → 'Бесперебойное питание (основной выход)'. "
        "'Uninterrupted Power Supply(Second Output)' → 'Бесперебойное питание (второй выход)'. "
        "Do not change text printed on the product. " + _KEEP
    ),
    (0, 3): (
        "This is a square wiring diagram of a white low-frequency inverter. Translate only the English labels "
        "around the unit, not the gold text on the casing. "
        "'PV Input' → 'Вход PV'. "
        "'AC Input' → 'Вход AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'Lead Acid/Lithium Battery' → 'Свинцовый / литиевый аккумулятор'. "
        "'Pure sine wave' → 'Чистая синусоида'. "
        "'Computer/TV' → 'Компьютер / ТВ'. "
        "'High-power Appliances' → 'Мощная техника'. "
        "'Household Appliances' → 'Бытовые приборы'. "
        "Do not change 'Low Frequency PV Inverter', FUNCTION, UP, DOWN, the display or the xindun logo. " + _KEEP
    ),
    (0, 4): (
        "This is a near-square wiring diagram of a blue inverter. Translate only the English diagram labels. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'AC INPUT' → 'ВХОД AC'. "
        "'Generator' → 'Генератор'. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
        "'AC OUTPUT' → 'ВЫХОД AC'. "
        "'LAPTOP' → 'НОУТБУК'. "
        "'LAMP' → 'ЛАМПА'. "
        "'PRINTER' → 'ПРИНТЕР'. "
        "'TV' → 'ТВ'. "
        "'FAN' → 'ВЕНТИЛЯТОР'. "
        "Do not change text on the blue product face or the battery cases. " + _KEEP
    ),
    (0, 5): (
        "This is a near-square wiring diagram of a white all-in-one unit. Translate only the English labels "
        "around the unit. "
        "'Solar Panel' → 'Солнечная панель'. "
        "'AC Input' → 'Вход AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'DC Output' → 'Выход DC'. "
        "'Lamp' → 'Лампа'. "
        "'Mobile Phone' → 'Телефон'. "
        "'Wireless Earphone' → 'Наушники'. "
        "'AC Output' → 'Выход AC'. "
        "'Laptop' → 'Ноутбук'. "
        "'Refrigerator' → 'Холодильник'. "
        "'Air-conditioning' → 'Кондиционер'. "
        "'Hair drier' → 'Фен'. "
        "'Water dispenser' → 'Кулер'. "
        "Do not change ENERGY STORAGE SYSTEM or LiFePO4 text on the casing. " + _KEEP
    ),
    (1, 0): (
        "This is a 3:2 banner: a black three-phase cabinet beside rooftop solar panels. "
        "Translate only the three-line headline and keep the green bar behind the middle line. "
        "Line 1: 'What Is A' → 'Что такое'. "
        "Line 2 on the green bar: 'Three Phase' → 'трёхфазный'. "
        "Line 3: 'Solar Inverter ?' → 'солнечный инвертор?'. "
        "Keep the cabinet, sky and solar panels. " + _KEEP
    ),
    (2, 0): (
        "This is a 3:2 studio banner with a wall battery, a gel battery and a battery rack. "
        "Translate only the three-line white headline on the left. "
        "Line 1: 'How to prevent' → 'Как не допустить'. "
        "Line 2: 'battery voltage' → 'слишком высокого'. "
        "Line 3: 'from being too high?' → 'напряжения аккумулятора?'. "
        "Keep the products and the blue background. Do not change LiFePO4 text on the products. " + _KEEP
    ),
    (3, 0): (
        "This is a 3:2 banner split between a red headline panel and a wall-mounted inverter. "
        "Translate only the red headline and the four icon captions. "
        "'WHY INVERTER NOT WORKING?' → 'ПОЧЕМУ ИНВЕРТОР НЕ РАБОТАЕТ?'. "
        "'Overload' → 'Перегрузка'. "
        "'Dust' → 'Пыль'. "
        "'Insect' → 'Насекомые'. "
        "'Reverse connection' → 'Переполюсовка'. "
        "Keep the red panel, icons, screwdriver, warning sign and the inverter. "
        "Do not change Low Frequency PV Inverter on the casing. " + _KEEP
    ),
    (4, 0): (
        "This is a square wiring diagram of a blue inverter seen from the terminal side. "
        "Translate only the English captions. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'DC Loads' → 'Нагрузка DC'. "
        "'AC Input' → 'Вход AC'. "
        "'AC Output' → 'Выход AC'. "
        "'Battery' → 'Аккумулятор'. "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'AC Loads' → 'Нагрузка AC'. "
        "Keep N, L, PE, plus and minus marks, and text on the product panel. " + _KEEP
    ),
    (4, 2): (
        "This is a wiring diagram with panels, a tower, a generator, an orange controller, a battery and a white inverter. "
        "Translate only the English captions. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Power Grid' → 'Электросеть'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'Solar Controller' → 'Солнечный контроллер'. "
        "'Battery' → 'Аккумулятор'. "
        "'AC Loads' → 'Нагрузка AC'. " + _KEEP
    ),
    (4, 4): (
        "This is a square wiring diagram of a white low-frequency inverter, the same layout as a home PV diagram. "
        "Translate only the English labels around the unit, not the gold text on the casing. "
        "'PV Input' → 'Вход PV'. "
        "'AC Input' → 'Вход AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'Lead Acid/Lithium Battery' → 'Свинцовый / литиевый аккумулятор'. "
        "'Pure sine wave' → 'Чистая синусоида'. "
        "'Computer/TV' → 'Компьютер / ТВ'. "
        "'High-power Appliances' → 'Мощная техника'. "
        "'Household Appliances' → 'Бытовые приборы'. "
        "Do not change 'Low Frequency PV Inverter', FUNCTION, UP, DOWN or the display. " + _KEEP
    ),
    (4, 6): (
        "This is a wiring diagram of a white low-frequency inverter with four solar panels and a battery. "
        "Translate only the English captions. "
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
        "Do not change Low Frequency PV Inverter on the product. " + _KEEP
    ),
    (4, 8): (
        "This is a wiring diagram of a white all-in-one unit. Translate only the English labels around the unit. "
        "'Solar Panel' → 'Солнечная панель'. "
        "'AC Input' → 'Вход AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'DC Output' → 'Выход DC'. "
        "'Lamp' → 'Лампа'. "
        "'Mobile Phone' → 'Телефон'. "
        "'Wireless Earphone' → 'Наушники'. "
        "'AC Output' → 'Выход AC'. "
        "'Laptop' → 'Ноутбук'. "
        "'Refrigerator' → 'Холодильник'. "
        "'Air-conditioning' → 'Кондиционер'. "
        "'Hair drier' → 'Фен'. "
        "'Water dispenser' → 'Кулер'. "
        "Do not change ENERGY STORAGE SYSTEM or LiFePO4 text on the casing. " + _KEEP
    ),
    (4, 10): (
        "This is a wiring diagram of a wheeled all-in-one solar generator. Translate only the surrounding captions. "
        "'DC LOADS' → 'НАГРУЗКА DC'. "
        "'Refrigerator' → 'Холодильник'. "
        "'Electromagnetic furnace' → 'Индукционная плита'. "
        "'Electric hammer' → 'Электромолоток'. "
        "'Air conditioner' → 'Кондиционер'. "
        "'AC LOADS' → 'НАГРУЗКА AC'. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
        "'or' → 'или'. "
        "'GENERATOR' → 'ГЕНЕРАТОР'. "
        "Both '12V200Ah Battery' → 'Аккумулятор 12V200Ah'. "
        "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
        "The caption 'INVERTER' under the cabinet → 'ИНВЕРТОР'. "
        "Do not change ALL IN ONE SOLAR GENERATOR printed on the cabinet, or the letters N and L. " + _KEEP
    ),
    (4, 12): (
        "This is a wiring diagram of one white hybrid inverter. Translate only the English diagram labels. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор сети и автономии'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Battery' → 'Аккумулятор'. "
        "'Power Grid' → 'Электросеть'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "Both 'AC Loads' → 'Нагрузка AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "Do not change HYBRID SOLAR INVERTER printed on the product. " + _KEEP
    ),
    (4, 14): (
        "This is a five-photo factory collage with green caption bars. Translate only those five English captions. "
        "'Reception' → 'Приёмная'. "
        "'Sample Room' → 'Образцы'. "
        "'Office' → 'Офис'. "
        "Both 'Workshop' captions → 'Цех'. "
        "Do not change the Chinese company name on the reception wall or the xindun logo. " + _KEEP
    ),
}


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


IMAGE_SOURCES: list[list[dict]] = [
    [
        _im("https://www.xindun-power.com/uploadfile/2025/05/20/202505201727431491.jpg", "Как выбрать домашний инвертор"),
        _im("https://www.xindun-power.com/uploadfile/2024/12/16/202412161348304040.png", "Как выбрать солнечный инвертор для дома"),
        _im("https://www.xindun-power.com/uploadfile/2025/05/20/202505201734324427.png", "Гибридный солнечный инвертор для дома"),
        _im("https://www.xindun-power.com/uploadfile/2024/12/16/202412161155415614.png", "Домашний солнечный инвертор"),
        _im("https://www.xindun-power.com/uploadfile/2024/12/16/202412161201017261.png", "Домашний инвертор"),
        _im("https://www.xindun-power.com/uploadfile/2024/12/25/202412251102379323.png", "Инвертор для дома: как выбрать"),
    ],
    [
        _im("https://www.xindun-power.com/uploadfile/2025/05/27/202505271728158953.jpg", "Что такое трёхфазный солнечный инвертор"),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/27/202504271633315115.jpg",
            "Как не допустить слишком высокого напряжения аккумулятора",
        ),
        _im("https://www.xindun-power.com/uploadfile/2025/04/27/202504271628351642.jpg", "Аккумулятор MPPT"),
        _im("https://www.xindun-power.com/uploadfile/2025/04/27/202504271641281907.jpg", "Защита аккумулятора инвертора"),
        _im("https://www.xindun-power.com/uploadfile/2025/04/27/202504271630584195.jpg", "Напряжение гелевого аккумулятора"),
    ],
    [
        _im(
            "https://www.xinduninverter.com/uploadfile/2025/04/30/202504301706025477.jpg",
            "Почему не работает мой солнечный инвертор",
        ),
    ],
    [
        _im("https://www.xindun-power.com/uploadfile/2024/10/31/202410310954245812.jpg", "Двухвыходной солнечный инвертор 2 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011622015367.jpg", "Установка двухфазного инвертора 2 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011624005684.png", "Инвертор 2 кВА даёт стабильное питание"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011728522856.jpg", "Применение гибридного инвертора Xindun 2 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2024/08/28/202408281504199926.jpg", "Инвертор 2 кВА держит освещение дома"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011631079516.jpg", "Солнечный инвертор какой мощности купить"),
        _im("https://www.xindun-power.com/uploadfile/2023/11/25/20231125171345fMB3JT.jpg", "Инверторы 2 кВА для мобильной техники"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011637587921.jpg", "Гибридный инвертор 2 кВА установлен дома"),
        _im(
            "https://www.xindun-power.com/uploadfile/2024/10/31/202410310956586221.jpg",
            "Как подключить аккумуляторы и нагрузку к инвертору 2 кВА",
        ),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011646254552.jpg", "Где лучше установить солнечный инвертор 2 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011658394281.jpg", "Стабильно ли выходное напряжение солнечного инвертора"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011700106747.jpg", "Какие функции у инвертора 2 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011553297878.jpg", "Оптовая цена солнечной системы 2 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011707482947.jpg", "Как спроектировать и установить солнечную PV-систему"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/01/202411011715278472.jpg", "Бренд гибридного инвертора Xindun Power 2 кВА"),
        _im("https://www.xindun-power.com/uploadfile/2024/11/04/202411040919122658.jpg", "Контроль качества солнечного инвертора"),
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
