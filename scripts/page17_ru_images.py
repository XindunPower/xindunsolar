#!/usr/bin/env python3
"""Prepare page 17 Russian images.

Duomi gpt-image-2 only for English marketing headlines and diagram labels.
Product photos, installation collages and lifestyle shots are compressed only.
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
PAGE_NUM = 17

_KEEP = (
    "Do NOT change the xindun logo, Xindun GREEN POWER, product casing text, "
    "model numbers, CE marks, display readings, button labels, terminal marks "
    "N and L, LiFePO4 text, HYBRID SOLAR INVERTER, ENERGY STORAGE SYSTEM, "
    "Low Frequency PV Inverter, MPPT Solar Charge Controller, or the word INVERTER "
    "printed on the product. Do not move products, arrows, wires or icons. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a square marketing banner: a white hybrid inverter in front of a round collage "
        "of a living room, a farm, a server room and a factory. Translate only the two-line green headline. "
        "Line 1: 'Where Are Dual Output' → 'Где уместны солнечные'. "
        "Line 2: 'Solar Inverters Suitable?' → 'инверторы с двумя выходами?'. "
        "Keep the green color and the two-line layout. " + _KEEP
    ),
    (0, 1): (
        "This is a product composite: two views of a white hybrid inverter and a circular inset of the AC terminals. "
        "Translate only the two English labels inside that circular inset. "
        "'MAIN AC OUT' → 'Основной выход AC'. "
        "'SECOND AC OUT' → 'Второй выход AC'. "
        "Keep the letters N and L under the terminals. Do not change the inverter body, display, buttons, "
        "logo or the red corner. " + _KEEP
    ),
    (0, 2): (
        "This is a wiring diagram of an HFP-S hybrid inverter. Translate only the English diagram labels. "
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
        "Keep red dotted arrows, icons and the white background. " + _KEEP
    ),
    (0, 3): (
        "This is a wiring diagram of an HFP-C hybrid inverter with a green RGB ring. "
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
        "Keep the green ring, red dotted arrows, icons and the white background. " + _KEEP
    ),
    (0, 4): (
        "This is a wiring diagram of an HFP-E hybrid inverter with a detachable panel. "
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
        "Keep red dotted arrows, icons and the white background. Do not change the word INVERTER on the green circle of the unit. "
        + _KEEP
    ),
    (1, 0): (
        "This is a wide marketing banner: two white hybrid inverters on stone pedestals against a dark green wall. "
        "Translate only the three-line white headline on the left. "
        "Line 1: 'Hot Sale' → 'Хит продаж'. "
        "Line 2: 'Hybrid Solar' → 'Гибридный солнечный'. "
        "Line 3: 'Inverter' → 'инвертор'. "
        "Keep the three-line layout and white type. " + _KEEP
    ),
    (3, 0): (
        "This is a wide marketing banner in a factory: solar panels, a black cabinet, an orange MPPT controller, "
        "cable coils and a battery rack. Translate only the white headline on the green translucent panel. "
        "Line 1: 'Large Off Grid' → 'Крупная автономная'. "
        "Line 2: 'Solar Power System' → 'солнечная система'. "
        "Do not change 'MPPT Solar Charge Controller' printed on the orange unit. " + _KEEP
    ),
    (4, 0): (
        "This is a studio banner with four inverter and storage units on a round pedestal. "
        "Translate only the green headline 'UPS vs Inverter' → 'ИБП и инвертор'. "
        "Keep it one line and green. Do not change text printed on the product casings. " + _KEEP
    ),
}


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


IMAGE_SOURCES: list[list[dict]] = [
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201525268839.jpg",
            "Где уместны солнечные инверторы с двумя выходами",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/21/202502211109144813.jpg",
            "Два выхода инвертора основной и второй",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201527344688.jpg",
            "Схема подключения инвертора HFP-S с двумя выходами",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201629492750.jpg",
            "Гибридный инвертор HFP-C с двумя выходами",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/02/20/202502201531002662.png",
            "Схема подключения инвертора HFP-E с двумя выходами",
        ),
    ],
    [
        _im(
            "https://www.xinduninverter.com/uploadfile/2025/04/30/202504301645036608.jpg",
            "Самый продаваемый гибридный солнечный инвертор",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/05/17/202505171639152797.jpg",
            "Портативный солнечный генератор для дома",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/05/17/202505171654575983.jpg",
            "Крупная автономная солнечная система",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/05/17/202505171655554450.jpg",
            "Примеры установки крупной автономной солнечной системы",
        ),
    ],
    [
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/29/20250429112627h64puG.jpg",
            "Сравнение ИБП и инвертора",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251609283224.jpg",
            "Гибридный инвертор HFP и ИБП",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/28/202504281609489599.jpg",
            "Низкочастотный инвертор LF и ИБП",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/28/202504281610369777.jpg",
            "Трёхфазный инвертор HDSX и ИБП",
        ),
        _im(
            "https://www.xindun-power.com/uploadfile/2025/04/25/202504251606458128.jpg",
            "Солнечный генератор ESS-Li и ИБП",
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
