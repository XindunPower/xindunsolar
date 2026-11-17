#!/usr/bin/env python3
"""Prepare page 15 Russian images.

Duomi gpt-image-2 only for English marketing headlines and diagram labels.
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
PAGE_NUM = 15

_KEEP = (
    "Do NOT change the xindun logo, Xindun GREEN POWER, product casing text, "
    "model numbers, CE marks, display readings, terminal silkscreen "
    "(SOLAR, BATTERY, DC LOAD, RS485, TEMP.SENSOR, SET, MENU), "
    "or the words printed on the product face such as MPPT Solar Charge Controller, "
    "HYBRID SOLAR INVERTER and INVERTER. Do not move products, arrows, wires or icons. "
    "Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a 3:2 industrial banner: a black UPS cabinet and battery cabinet on a factory road. "
        "Translate only the four-line white headline on the left green band. "
        "Line 1: 'How to Choose the' → 'Как выбрать лучшую'. "
        "Line 2: 'Best UPS Backup' → 'систему резервного'. "
        "Line 3: 'Power System for' → 'питания ИБП для'. "
        "Line 4: 'Industrial?' → 'промышленности?'. "
        "Keep the factory, sky, cabinets and screen. " + _KEEP
    ),
    (1, 0): (
        "This is a 3:2 studio banner of orange and white MPPT charge controllers on a pale blue stage. "
        "Translate only the two-line blue headline. Keep MPPT in Latin letters. "
        "Line 1: 'How to Properly Size MPPT' → 'Как правильно подобрать MPPT'. "
        "Line 2: 'Solar Charge Controller?' → 'контроллер заряда?'. "
        "Do not change text printed on the orange and white products. " + _KEEP
    ),
    (2, 0): (
        "This is a 3:2 studio banner of four white hybrid inverters. "
        "Translate only the large outlined headline. "
        "'HIGHBREED INVERTER' → 'ГИБРИДНЫЙ ИНВЕРТОР'. "
        "Do not change the circular INVERTER badge, the xindun logo or casing print. " + _KEEP
    ),
    (2, 1): (
        "This is a wiring diagram of one white hybrid inverter. Translate only the English diagram labels. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор сети и автономии'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Battery' → 'Аккумулятор'. "
        "'Power Grid' → 'Электросеть'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "Both 'AC Loads' → 'Нагрузка AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. " + _KEEP
    ),
    (2, 2): (
        "This is a wiring diagram of a white hybrid inverter with two AC outputs. "
        "Translate only the English diagram labels. "
        "'On&Off Grid Hybrid Solar Inverter' → 'Гибридный инвертор сети и автономии'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'Power Grid' → 'Электросеть'. "
        "'Electric Meter' → 'Электросчётчик'. "
        "'AC Loads' → 'Нагрузка AC'. "
        "'or' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'Uninterrupted Power Supply(Main output)' → 'Бесперебойное питание (основной выход)'. "
        "'Uninterrupted Power Supply(Second output)' → 'Бесперебойное питание (второй выход)'. " + _KEEP
    ),
    (2, 3): (
        "This is a wiring diagram of a white inverter with a green ring. "
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
        "'Uninterrupted Power Supply(Second Output)' → 'Бесперебойное питание (второй выход)'. " + _KEEP
    ),
    (2, 4): (
        "This is a wiring diagram of a white inverter with a green INVERTER handle. "
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
        "Do not change the INVERTER word on the product handle. " + _KEEP
    ),
    (3, 0): (
        "This is a 3:2 diagram: solar panels, a white hybrid inverter, a battery and a power pole. "
        "Translate only the English headline and the four diagram labels. "
        "Headline line 1: 'How Many Charging Modes Does Hybrid Inverter Have?' → "
        "'Сколько режимов заряда у гибридного инвертора?'. "
        "Headline line 2: 'How To Use Charging Priority?' → 'Как пользоваться приоритетом заряда?'. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Power Grid' → 'Электросеть'. "
        "'Battery' → 'Аккумулятор'. "
        "'Inverter' under the unit → 'Инвертор'. "
        "Keep the colored wires, sun and products. " + _KEEP
    ),
    (4, 0): (
        "This is a house cross-section diagram with solar panels, an orange controller, a battery, "
        "a white inverter and a utility pole. Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Solar Controller' → 'Солнечный контроллер'. "
        "'Battery' → 'Аккумулятор'. "
        "'Inverter' → 'Инвертор'. "
        "'AC Loads' → 'Нагрузка AC'. "
        "'Power Grid' → 'Электросеть'. "
        "Keep the letters N and L, the xindun GREENPOWER logo, wires and the house. " + _KEEP
    ),
    (4, 1): (
        "This is a square wiring diagram of an orange MPPT controller, four batteries, panels and a blue inverter. "
        "Translate only the captions under the drawings, not the text printed on the controller. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'Inverter' → 'Инвертор'. "
        "'DC Load' → 'Нагрузка DC'. "
        "On each small battery, '12V200Ah Battery' → 'Аккумулятор 12V200Ah'. "
        "Do not change SOLAR, BATTERY, DC LOAD, RS485 or TEMP.SENSOR on the product. " + _KEEP
    ),
    (4, 2): (
        "This is a square wiring diagram of a white MPPT controller, two batteries, panels and a blue inverter. "
        "Translate only the captions under the drawings, not the text printed on the controller. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Batteries' → 'Аккумуляторы'. "
        "'Inverter' → 'Инвертор'. "
        "'DC Load' → 'Нагрузка DC'. "
        "'12V200Ah Battery' → 'Аккумулятор 12V200Ah'. "
        "Do not change MPPT Solar Charge Controller, SET, MENU or the terminal labels. " + _KEEP
    ),
    (4, 3): (
        "This is a square diagram of a black PWM controller above a blue inverter and three load photos. "
        "Translate only the English diagram captions. "
        "'Solar Panel' → 'Солнечная панель'. "
        "'Battery' → 'Аккумулятор'. "
        "'Dc Load' → 'Нагрузка DC'. "
        "'Inverter' → 'Инвертор'. "
        "'House Loads' → 'Домашняя нагрузка'. "
        "'Office Equipment' → 'Офисная техника'. "
        "'Industrial equipment' → 'Промышленное оборудование'. "
        "Do not change text printed on the black controller or the blue inverter. " + _KEEP
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/20/202506201409218862.jpg",
            "alt_ru": "Лучший промышленный ИБП",
            "title_ru": "Лучший промышленный ИБП",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/20/202506201407508434.jpg",
            "alt_ru": "Подбор контроллера заряда MPPT",
            "title_ru": "Подбор контроллера заряда MPPT",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/11/202506111429238620.jpg",
            "alt_ru": "Гибридный инвертор highbreed",
            "title_ru": "Гибридный инвертор highbreed",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/12/16/202412161348304040.png",
            "alt_ru": "Гибридный инвертор HFP",
            "title_ru": "Гибридный инвертор HFP",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/11/202506111433272766.png",
            "alt_ru": "Гибридный инвертор HFP-S",
            "title_ru": "Гибридный инвертор HFP-S",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/20/202505201734324427.png",
            "alt_ru": "Солнечный гибридный инвертор HFP-C",
            "title_ru": "Солнечный гибридный инвертор HFP-C",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/02/20/202502201531002662.png",
            "alt_ru": "Гибридный инвертор HFP-E",
            "title_ru": "Гибридный инвертор HFP-E",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/02/202506021144221391.jpg",
            "alt_ru": "Режим заряда солнечного инвертора",
            "title_ru": "Режим заряда солнечного инвертора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/28/202505281034426fU0XN.jpg",
            "alt_ru": "Как работает контроллер заряда",
            "title_ru": "Как работает контроллер заряда",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/27/202505271638331976.jpg",
            "alt_ru": "Схема работы солнечного контроллера заряда",
            "title_ru": "Схема работы солнечного контроллера заряда",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/27/202505271639203692.jpg",
            "alt_ru": "Как работает солнечный контроллер",
            "title_ru": "Как работает солнечный контроллер",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/27/202505271640059587.jpg",
            "alt_ru": "Схема подключения контроллера заряда",
            "title_ru": "Схема подключения контроллера заряда",
        },
    ],
]

IMAGE_LOG: list[dict] = []


def api_size(w: int, h: int) -> str:
    """Named ratios the API accepts, or a pixel size divisible by 16.

    Duomi rejects any side above 3840, so the search stays inside that limit
    and prefers the smaller canvas when ratios are equally close.
    """
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
