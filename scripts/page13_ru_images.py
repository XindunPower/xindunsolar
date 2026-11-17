#!/usr/bin/env python3
"""Prepare page 13 Russian images.

Duomi gpt-image-2 only for English marketing headlines.
Product studio shots, installation photos and collages without overlay copy
are compressed and renamed. Product casing text stays unchanged.
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
PAGE_NUM = 13

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a cropped dark-blue diagram: sun, battery, house and a red power tower on the left, "
        "a white hybrid inverter on the right, a yellow warning triangle at the bottom left. "
        "The top headline is cut off by the crop. Translate only the English overlay that is actually visible. "
        "Do not invent a new headline and do not expand the canvas. "
        "Bottom caption, three lines: "
        "'Overvoltage, frequent outages,' → 'Перенапряжение, частые отключения,'. "
        "'surges – all threaten your' → 'скачки — всё это угрожает'. "
        "'inverter system.' → 'вашей инверторной системе.'. "
        "If a fragment of the headline remains at the top edge, translate only that fragment and keep it cropped. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, the display, buttons or CE marks. "
        "Do not move the icons, tower, inverter or warning sign. Do not redesign."
    ),
    (0, 1): (
        "This is a square dark-blue diagram. Translate only the English overlay. "
        "Keep the three-line white headline and the three-line caption. "
        "Headline line 1: 'UNSTABLE MAINS POWER' → 'НЕСТАБИЛЬНАЯ СЕТЬ'. "
        "Headline line 2: 'MAY DAMAGE YOUR' → 'МОЖЕТ ПОВРЕДИТЬ'. "
        "Headline line 3: 'OFF GRID INVERTER' → 'АВТОНОМНЫЙ ИНВЕРТОР'. "
        "Caption line 1: 'Overvoltage, frequent outages,' → 'Перенапряжение, частые отключения,'. "
        "Caption line 2: 'surges – all threaten your' → 'скачки — всё это угрожает'. "
        "Caption line 3: 'inverter system.' → 'вашей инверторной системе.'. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, the display, buttons or CE marks. "
        "Do not move the sun, battery, house, red tower, arrows, inverter or warning sign. Do not redesign."
    ),
    (1, 0): (
        "This is a cropped product banner in front of an RV. Translate only the green headline: "
        "'Solar Power Inverter For Vehicle' → 'Солнечный инвертор для транспорта'. "
        "Keep it as one green line. "
        "Do NOT change text printed on the product casings, including DC-AC, 1000W, "
        "ENERGY STORAGE SYSTEM, LiFePO4 Lithium Battery, SOLAR GENERATOR, the xindun logo, "
        "displays, buttons or CE marks. Do not move the five products, the RV or the blue platforms. Do not redesign."
    ),
    (1, 1): (
        "This is a wide product banner in front of an RV. Translate only the green headline: "
        "'Solar Power Inverter For Vehicle' → 'Солнечный инвертор для транспорта'. "
        "Keep it as one green line. "
        "Do NOT change text printed on the product casings, including DC-AC, 1000W, "
        "ENERGY STORAGE SYSTEM, LiFePO4 Lithium Battery, SOLAR GENERATOR, the xindun logo, "
        "displays, buttons or CE marks. Do not move the five products, the RV or the blue platforms. Do not redesign."
    ),
    (3, 0): (
        "This is a cropped comparison banner on a pale blue background: a white HFP inverter on the left, "
        "a white LF inverter on the right, and a blue VS badge. "
        "Translate only the two-line headline. Keep HFP, LF and VS exactly. "
        "Line 1: 'Why Is the Max Charging Current of High Frequency Inverter' → "
        "'Почему максимальный ток заряда высокочастотного инвертора'. "
        "Line 2: 'Higher Than That of Low Frequency Inverter?' → 'выше, чем у низкочастотного?'. "
        "Do NOT change text on the casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the inverters, cards or VS badge. Do not redesign."
    ),
    (3, 1): (
        "This is a wide comparison banner on a pale blue background: a white HFP inverter on the left, "
        "a white LF inverter on the right, and a blue VS badge. "
        "Translate only the two-line headline. Keep HFP, LF and VS exactly. "
        "Line 1: 'Why Is the Max Charging Current of High Frequency Inverter' → "
        "'Почему максимальный ток заряда высокочастотного инвертора'. "
        "Line 2: 'Higher Than That of Low Frequency Inverter?' → 'выше, чем у низкочастотного?'. "
        "Do NOT change text on the casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the inverters, cards or VS badge. Do not redesign."
    ),
    (4, 0): (
        "This is a cropped dark banner: a white hybrid inverter in the center, a shield marked H on the left "
        "and a shield marked L on the right. Translate only the overlay text. Keep the letters H and L. "
        "Headline line 1: 'What Are the Low Voltage Protection' → 'Что такое защита инвертора'. "
        "Headline line 2: 'And High Voltage Protection of Inverters?' → 'по низкому и высокому напряжению?'. "
        "Left caption: 'High Voltage Protection' → 'Защита по высокому напряжению'. "
        "Right caption: 'Low Voltage Protection' → 'Защита по низкому напряжению'. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, the display, buttons or CE marks. "
        "Do not move the inverter or the shields. Do not redesign."
    ),
    (4, 1): (
        "This is a wide dark banner: a white hybrid inverter in the center, a shield marked H on the left "
        "and a shield marked L on the right. Translate only the overlay text. Keep the letters H and L. "
        "Headline line 1: 'What Are the Low Voltage Protection' → 'Что такое защита инвертора'. "
        "Headline line 2: 'And High Voltage Protection of Inverters?' → 'по низкому и высокому напряжению?'. "
        "Left caption: 'High Voltage Protection' → 'Защита по высокому напряжению'. "
        "Right caption: 'Low Voltage Protection' → 'Защита по низкому напряжению'. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, the display, buttons or CE marks. "
        "Do not move the inverter or the shields. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/23/20250723141340KlhTOw.jpg",
            "alt_ru": "Недостатки сетевого режима автономного инвертора",
            "title_ru": "Недостатки сетевого режима автономного инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/23/202507231412502496.jpg",
            "alt_ru": "Нестабильная сеть может повредить автономный инвертор",
            "title_ru": "Нестабильная сеть может повредить автономный инвертор",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211010548954.jpg",
            "alt_ru": "Солнечный инвертор для транспорта",
            "title_ru": "Солнечный инвертор для транспорта",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211011296067.jpg",
            "alt_ru": "Инвертор для дома на колёсах и спецтранспорта",
            "title_ru": "Инвертор для дома на колёсах и спецтранспорта",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211051145263.jpg",
            "alt_ru": "Силовой инвертор GP-C для транспорта",
            "title_ru": "Силовой инвертор GP-C для транспорта",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151710038307.jpg",
            "alt_ru": "Инвертор DF для транспортной системы",
            "title_ru": "Инвертор DF для транспортной системы",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211353482657.jpg",
            "alt_ru": "Моноблочный солнечный генератор ESS для транспорта",
            "title_ru": "Моноблочный солнечный генератор ESS для транспорта",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211107597731.jpg",
            "alt_ru": "Инвертор ESS-Li с литиевой батареей для транспорта",
            "title_ru": "Инвертор ESS-Li с литиевой батареей для транспорта",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/19/202507191512123FdpYG.jpg",
            "alt_ru": "Инвертор для тяжёлой нагрузки на производстве",
            "title_ru": "Инвертор для тяжёлой нагрузки на производстве",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/19/202507191503015862.jpg",
            "alt_ru": "Где применяют инвертор для тяжёлой нагрузки",
            "title_ru": "Где применяют инвертор для тяжёлой нагрузки",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/19/202507191504176168.jpg",
            "alt_ru": "Установка инвертора для тяжёлой нагрузки",
            "title_ru": "Установка инвертора для тяжёлой нагрузки",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/20250702104318jxV2iD.jpg",
            "alt_ru": "Ток заряда высокочастотного и низкочастотного инвертора",
            "title_ru": "Ток заряда высокочастотного и низкочастотного инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/202507021055145558.jpg",
            "alt_ru": "Сравнение тока заряда инверторов HFP и LF",
            "title_ru": "Сравнение тока заряда инверторов HFP и LF",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/20250702104338SAcMNt.jpg",
            "alt_ru": "Защита инвертора по низкому и высокому напряжению",
            "title_ru": "Защита инвертора по низкому и высокому напряжению",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/202507021044418741.jpg",
            "alt_ru": "Защита аккумулятора по низкому и высокому напряжению",
            "title_ru": "Защита аккумулятора по низкому и высокому напряжению",
        },
    ],
]

IMAGE_LOG: list[dict] = []


def api_size(w: int, h: int) -> str:
    """Named ratios the API accepts, or a pixel size divisible by 16."""
    ratio = w / h if h else 1.0
    named = {"1:1": 1.0, "3:2": 1.5, "2:3": 2 / 3}
    best_name, best_ratio = min(named.items(), key=lambda kv: abs(kv[1] - ratio))
    if abs(best_ratio - ratio) <= 0.03:
        return best_name
    best = None
    for height in range(640, 2200, 16):
        width = int(round((ratio * height) / 16.0)) * 16
        if width < 16:
            continue
        pixels = width * height
        if pixels < 655360 or pixels > 8294400:
            continue
        delta = abs((width / height) - ratio)
        if best is None or delta < best[0]:
            best = (delta, f"{width}x{height}")
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
