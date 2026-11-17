#!/usr/bin/env python3
"""Prepare page 11 Russian images.

Duomi gpt-image-2 only for English marketing headlines and wiring-diagram labels.
Listing crops and studio product shots without overlay copy stay compressed and renamed.
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
    compress_only,
    run_duomi,
    size_for,
    slugify,
    unique_stem,
)

UA = "Mozilla/5.0 (compatible; XindunRussianBot/1.0)"
PAGE_NUM = 11

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 1): (
        "This is a kitchen scene: a dark refrigerator on the left, a white wall inverter "
        "and a white battery on the right, with red, blue and green wires marked N, L and +. "
        "Translate only the three-line beige headline at the top to Russian. Keep three lines. "
        "Line 1: 'CAN I RUN A REFRIGERATOR' → 'МОЖНО ЛИ ПИТАТЬ ХОЛОДИЛЬНИК'. "
        "Line 2: 'ON A 1500W PURE SINE WAVE' → 'ОТ ИНВЕРТОРА ЧИСТОЙ СИНУСОИДЫ'. "
        "Line 3: 'INVERTER?' → 'НА 1500 ВТ?'. "
        "Keep the letters N, L and the plus sign exactly. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, LiFePO4 Lithium Battery, "
        "CE marks, the display or buttons. Do not move the refrigerator, inverter, battery, "
        "wires or window. Do not redesign."
    ),
    (1, 0): (
        "This is a dark wiring diagram, slightly cropped. Translate only the English overlay "
        "text to Russian. Keep the green banner, white headline, arrows, wire colors, "
        "voltage tags and every icon. "
        "Headline line 1, white: 'What Is the Best' → 'Какой лучше'. "
        "Headline line 2, green banner: 'Split Phase Solar Inverter?' → 'инвертор split phase?'. "
        "'Solar Panels' → 'Солнечные панели'. 'Battery' → 'Аккумулятор'. "
        "'Power Grid' → 'Сеть'. 'AC Loads' → 'Нагрузка AC'. "
        "Keep 120V, 240V, L1, L2 and N exactly, including the colored boxes. "
        "Do NOT change SPLIT PHASE INVERTER on the casing, the xindun logo, the display, "
        "or LiFePO4 Lithium Battery on the battery unit. "
        "Do not add or remove products, wires or icons. Do not redesign."
    ),
    (1, 1): (
        "This is a dark wiring diagram on a wide canvas. Translate only the English overlay "
        "text to Russian. Keep the green banner, white headline, arrows, wire colors, "
        "voltage tags and every icon. "
        "Headline line 1, white: 'What Is the Best' → 'Какой лучше'. "
        "Headline line 2, green banner: 'Split Phase Solar Inverter?' → 'инвертор split phase?'. "
        "'Solar Panels' → 'Солнечные панели'. 'Battery' → 'Аккумулятор'. "
        "'Power Grid' → 'Сеть'. 'AC Loads' → 'Нагрузка AC'. "
        "Keep 120V, 240V, L1, L2 and N exactly, including the colored boxes. "
        "Do NOT change SPLIT PHASE INVERTER on the casing, the xindun logo, the display, "
        "or LiFePO4 Lithium Battery on the battery unit. "
        "Do not add or remove products, wires or icons. Do not redesign."
    ),
    (2, 1): (
        "This is a product lineup on grass under a blue sky, with solar panels behind the units. "
        "Translate only the two-line headline. Keep the green emphasis on the middle words. "
        "Line 1: 'Can Low Frequency Solar Inverter' → 'Можно ли низкочастотный солнечный инвертор'. "
        "Line 2: 'Be Used Directly Without Battery?' → 'включить напрямую без аккумулятора?'. "
        "Do NOT change any text printed on the product casings, including a partial 'Low Fre', "
        "SPLIT PHASE INVERTER, LiFePO4 Lithium Battery, the xindun logo, displays, CE or ISO marks. "
        "Do not add or remove products or panels. Do not redesign."
    ),
    (3, 0): (
        "This is a cropped beach scene with solar panels and two white low-frequency inverters. "
        "Translate only the headline. Line 1 stays blue on the sky: "
        "'Why Does the Low Frequency Inverter' → 'Почему у низкочастотного инвертора'. "
        "Line 2 stays inside the blue rounded banner: "
        "'Have No Bypass Output?' → 'нет байпасного выхода?'. "
        "Do NOT change 'Low Frequency PV Inverter' printed on the casings, the xindun logo, "
        "displays, buttons or CE marks. Do not move the inverters, sand, sky or panels. Do not redesign."
    ),
    (3, 1): (
        "This is a wide beach scene with solar panels and two white low-frequency inverters. "
        "Translate only the headline. Line 1 stays blue on the sky: "
        "'Why Does the Low Frequency Inverter' → 'Почему у низкочастотного инвертора'. "
        "Line 2 stays inside the blue rounded banner: "
        "'Have No Bypass Output?' → 'нет байпасного выхода?'. "
        "Do NOT change 'Low Frequency PV Inverter' printed on the casings, the xindun logo, "
        "displays, buttons or CE marks. Do not move the inverters, sand, sky or panels. Do not redesign."
    ),
    (4, 0): (
        "This is a wide studio banner: a white hybrid inverter on a round pedestal, "
        "a blue lightning badge on the left and a blue waveform badge on the right. "
        "Translate only the overlay text. Keep two headline lines. "
        "Line 1: \"WHAT IS THE ROLE OF THE INVERTER'S\" → 'КАКОВА РОЛЬ ВХОДНОГО ТОКА СЕТИ'. "
        "Line 2: 'MAINS INPUT CURRENT AND INPUT POWER?' → 'И ВХОДНОЙ МОЩНОСТИ ИНВЕРТОРА?'. "
        "Left caption 'INPUT CURRENT' → 'ВХОДНОЙ ТОК'. "
        "Right caption 'INPUT POWER' → 'ВХОДНАЯ МОЩНОСТЬ'. "
        "Keep the letter A inside the lightning badge. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, the display, buttons, CE or ISO marks. "
        "Do not move the inverter, badges or pedestal. Do not redesign."
    ),
    (4, 1): (
        "This is a studio banner, slightly tighter crop: a white hybrid inverter on a round pedestal, "
        "a blue lightning badge on the left and a blue waveform badge on the right. "
        "Translate only the overlay text. Keep two headline lines. "
        "Line 1: \"WHAT IS THE ROLE OF THE INVERTER'S\" → 'КАКОВА РОЛЬ ВХОДНОГО ТОКА СЕТИ'. "
        "Line 2: 'MAINS INPUT CURRENT AND INPUT POWER?' → 'И ВХОДНОЙ МОЩНОСТИ ИНВЕРТОРА?'. "
        "Left caption 'INPUT CURRENT' → 'ВХОДНОЙ ТОК'. "
        "Right caption 'INPUT POWER' → 'ВХОДНАЯ МОЩНОСТЬ'. "
        "Keep the letter A inside the lightning badge. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, the display, buttons, CE or ISO marks. "
        "Do not move the inverter, badges or pedestal. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/30/20250830172038NOZbGE.jpg",
            "alt_ru": "Холодильник и инвертор чистой синусоиды 1500 Вт",
            "title_ru": "Холодильник и инвертор чистой синусоиды 1500 Вт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/30/202508301716567704.jpg",
            "alt_ru": "Можно ли питать холодильник от инвертора чистой синусоиды 1500 Вт",
            "title_ru": "Можно ли питать холодильник от инвертора чистой синусоиды 1500 Вт",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/2025082511504221Xqsy.jpg",
            "alt_ru": "Схема солнечного инвертора с расщеплённой фазой",
            "title_ru": "Схема солнечного инвертора с расщеплённой фазой",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/202508251151214665.jpg",
            "alt_ru": "Солнечный инвертор с расщеплённой фазой в Южной Америке",
            "title_ru": "Солнечный инвертор с расщеплённой фазой в Южной Америке",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/202508251458058bBEVr.jpg",
            "alt_ru": "Линейка низкочастотных солнечных инверторов",
            "title_ru": "Линейка низкочастотных солнечных инверторов",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/202508251457528554.jpg",
            "alt_ru": "Низкочастотный солнечный инвертор без аккумулятора",
            "title_ru": "Низкочастотный солнечный инвертор без аккумулятора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/20250825114541Ygv2ol.jpg",
            "alt_ru": "Почему у низкочастотного инвертора нет байпасного выхода",
            "title_ru": "Почему у низкочастотного инвертора нет байпасного выхода",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/202508251146107503.jpg",
            "alt_ru": "Выход низкочастотного инвертора",
            "title_ru": "Выход низкочастотного инвертора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/20250821145039S0bGDw.jpg",
            "alt_ru": "Входной ток сети и входная мощность инвертора",
            "title_ru": "Входной ток сети и входная мощность инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211455008206.jpg",
            "alt_ru": "Показания входного тока и входной мощности инвертора",
            "title_ru": "Показания входного тока и входной мощности инвертора",
        },
    ],
]

IMAGE_LOG: list[dict] = []


def api_size(w: int, h: int) -> str:
    """Use a named ratio when it is close; otherwise a pixel size the API accepts.

    gpt-image-2 rejects odd ratios such as 3:4 for this portrait banner and requires
    width and height divisible by 16, with a pixel budget of at least 655360.
    """
    preset = size_for(w, h)
    a, b = (int(x) for x in preset.split(":"))
    if h and abs((a / b) - (w / h)) <= 0.08:
        return preset
    target = w / h if h else 1.0
    best = None
    for height in range(800, 2200, 16):
        width = int(round((target * height) / 16.0)) * 16
        if width < 16:
            continue
        pixels = width * height
        if pixels < 655360 or pixels > 8294400:
            continue
        delta = abs((width / height) - target)
        if best is None or delta < best[0]:
            best = (delta, f"{width}x{height}")
    if best is None:
        return preset
    return best[1]


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
            stem = unique_stem(slugify(im["alt_ru"]))
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
