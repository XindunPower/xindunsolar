#!/usr/bin/env python3
"""Prepare page 18 Russian images.

Duomi gpt-image-2 only for English marketing headlines and diagram labels.
Product photos and the Nigeria scene (no English marketing overlay) are compressed only.
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
PAGE_NUM = 18

_KEEP = (
    "Do NOT change the xindun logo, Xindun GREEN POWER, product casing text, "
    "model numbers, CE marks, display readings, button labels, or words printed "
    "on the product such as HYBRID SOLAR INVERTER, Low Frequency PV Inverter, "
    "Low Frequency Inverter, Pure Sine Wave, MPPT Solar Charge Controller, "
    "ENERGY STORAGE SYSTEM, or SOLAR Charge Controller. "
    "Do not move products, arrows, wires or icons. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a wide product banner. Translate only the two headline bars. "
        "Green bar: 'HIGH FREQUENCY INVERTER' → 'ВЫСОКОЧАСТОТНЫЙ ИНВЕРТОР'. "
        "Gold bar: 'LOW FREQUENCY INVERTER' → 'НИЗКОЧАСТОТНЫЙ ИНВЕРТОР'. "
        "Keep the golden VS emblem between the bars exactly as drawn. "
        "Keep every inverter, the grey studio background and the two-bar layout. " + _KEEP
    ),
    (0, 1): (
        "This is a studio banner with two white hybrid inverters on stone pedestals. "
        "Translate only the white headline above the products. "
        "'High Frequency Hybrid Inverter' → 'Высокочастотный гибридный инвертор'. "
        "Keep it one line, white, and centered. "
        "The gold line on both inverter bodies must stay exactly 'HYBRID SOLAR INVERTER' in Latin letters. "
        + _KEEP
    ),
    (1, 0): (
        "This is a wide studio banner with four inverters on round pedestals. "
        "Translate only the three-line white headline. "
        "Line 1: 'HIGH FREQUENCY INVERTER' stays on the first line, translate to 'ВЫСОКОЧАСТОТНЫЙ ИНВЕРТОР', "
        "and keep the black VS badge on that same line. "
        "Line 2: 'LOW FREQUENCY INVERTER' → 'НИЗКОЧАСТОТНЫЙ ИНВЕРТОР'. "
        "Line 3: 'BUILT IN MPPT' → 'ВСТРОЕННЫЙ MPPT'. "
        "Keep the three-line layout, white type and the black VS badge. "
        "Do not change 'Low Frequency PV Inverter' or 'HYBRID SOLAR INVERTER' printed on the white units, "
        "or 'MPPT Solar Charge Controller' printed on the orange unit. " + _KEEP
    ),
    (3, 0): (
        "This is a black marketing banner of orange and white solar regulators. "
        "Translate only the two white headlines. "
        "'MPPT Solar Regulator' → 'Солнечный регулятор MPPT'. "
        "'PWM Solar Regulator' → 'Солнечный регулятор PWM'. "
        "Keep the yellow slash and the black-and-gold VS badge exactly as drawn. "
        "Keep the xindun logo and the words GREEN POWER. "
        "Do NOT change text printed on the product casings. "
        "Do not move products. Do not redesign the poster. " + _KEEP
    ),
    (4, 0): (
        "This is a dark marketing banner with three inverters on the right. "
        "Translate only the English headline and the two red badges. "
        "Line 1, large white: 'LOW FREQUENCY' → 'НИЗКОЧАСТОТНЫЙ'. "
        "Line 2, large red: 'HYBRID INVERTER' → 'ГИБРИДНЫЙ ИНВЕРТОР'. "
        "Upper red badge: '24VDC TO 120VAC INVERTER' → 'ИНВЕРТОР 24 В DC НА 120 В AC'. "
        "Lower red badge: '24VDC TO 110VAC INVERTER' → 'ИНВЕРТОР 24 В DC НА 110 В AC'. "
        "Keep the two-line headline, both red pills, the red arc, and the black background. "
        "Keep the xindun logo and the words GREEN POWER exactly. "
        "Do NOT change text printed on the product casings. "
        "Do not move the three inverters. Do not redesign. " + _KEEP
    ),
    (4, 1): (
        "This is a wiring diagram of an LF low-frequency inverter. Translate only the English diagram labels. "
        "'Solar Panels' → 'Солнечные панели'. "
        "'Utility Grid' → 'Электросеть'. "
        "'OR' → 'или'. "
        "'Generator' → 'Генератор'. "
        "'Battery' → 'Аккумулятор'. "
        "'Laptop' → 'Ноутбук'. "
        "'Printer' → 'Принтер'. "
        "'TV' → 'Телевизор'. "
        "'Fans' → 'Вентиляторы'. "
        "'Light' → 'Лампа'. "
        "Do not change 'Low Frequency PV Inverter' printed on the white unit. "
        "Keep arrows, icons and the white background. " + _KEEP
    ),
    (4, 2): (
        "This is a wiring diagram of a DF low-frequency inverter. Translate only the English diagram labels. "
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
        "Do not change 'Low Frequency PV Inverter' printed on the white unit. "
        "Keep arrows, icons and the white background. " + _KEEP
    ),
    (4, 3): (
        "This is a wiring diagram of a WF low-frequency inverter. Translate only the English diagram labels. "
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
        "Do not change 'Low Frequency Inverter' or 'Pure Sine Wave' printed on the white unit. "
        "Keep arrows, icons and the white background. " + _KEEP
    ),
    (4, 4): (
        "This is a wiring diagram of a blue LS inverter. Translate only the English diagram labels. "
        "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
        "'AC INPUT' → 'ВХОД AC'. "
        "'Generator' → 'Генератор'. "
        "'AC OUTPUT' → 'ВЫХОД AC'. "
        "'LAPTOP' → 'НОУТБУК'. "
        "'LAMP' → 'ЛАМПА'. "
        "'PRINTER' → 'ПРИНТЕР'. "
        "'TV' → 'ТЕЛЕВИЗОР'. "
        "'FAN' → 'ВЕНТИЛЯТОР'. "
        "'Battery' → 'Аккумулятор'. "
        "Keep arrows, icons and the white background. " + _KEEP
    ),
    (4, 5): (
        "This is a wiring diagram of a yellow WD inverter. Translate only the English diagram labels. "
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
        "Keep arrows, icons and the white background. " + _KEEP
    ),
}


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


IMAGE_SOURCES: list[list[dict]] = [
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/28/20250428104831zFosif.jpg",
            "Высокочастотный и низкочастотный инвертор",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/30/20250430190547Sig1Ko.jpg",
            "Высокочастотный гибридный инвертор",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/27/202504271604474704.jpg",
            "Высокочастотный и низкочастотный инвертор со встроенным MPPT",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251609283224.jpg",
            "Гибридный солнечный инвертор HFP",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/27/202504271556532553.jpg",
            "Гибридный инвертор HFP-C с MPPT",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251608565115.jpg",
            "Низкочастотный солнечный инвертор LF",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/27/202504271557577862.jpg",
            "Инвертор LS с расщеплённой фазой",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251728474711.jpg",
            "Лучший солнечный инвертор для Нигерии",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251605475197.jpg",
            "Трёхфазный инвертор HDSX для Нигерии",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251606458128.jpg",
            "Солнечный генератор ESS-Li",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251607372220.jpg",
            "Низкочастотный инвертор WD",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251608565115.jpg",
            "Низкочастотный инвертор LF для Нигерии",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251609283224.jpg",
            "Гибридный инвертор HFP для Нигерии",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/19/20250419092007PxYuaS.jpg",
            "Разница между солнечными регуляторами PWM и MPPT",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/18/202504181719461485.jpg",
            "Солнечный регулятор MPPT Wonder1",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/18/202504181720014942.jpg",
            "Солнечный регулятор MPPT Wonder2",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/18/202504181720193337.jpg",
            "Солнечный регулятор PWM KY1",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/19/202504191456263173.jpg",
            "Как выбрать инвертор 24 В DC на 120 В AC или 110 В AC",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/19/202504191503471831.png",
            "Схема инвертора LF 24 В в 110 В",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/19/202504191512076247.jpg",
            "Схема инвертора DF 24 В",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/19/202504191506054728.png",
            "Схема инвертора WF 120 В",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/19/202504191507024517.jpg",
            "Схема инвертора LS 110 В",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/19/202504191507527479.jpg",
            "Схема инвертора WD 24 В в 110 В",
        ),
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
