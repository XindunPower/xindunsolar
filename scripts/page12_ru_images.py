#!/usr/bin/env python3
"""Prepare page 12 Russian images.

Duomi gpt-image-2 only for English marketing headlines and diagram callouts.
Studio product shots, lifestyle photos and the factory collage are compressed
and renamed. Product casing text and the Chinese wall sign stay unchanged.
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
PAGE_NUM = 12

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a cropped comparison banner on a beige background: a white wall inverter "
        "in a rounded card on the left and a black floor cabinet on the right, with an orange VS badge. "
        "Translate only the overlay headline and the two captions under the cards. Keep two headline lines. "
        "Line 1, black: 'What Is the Difference Between' → 'В чём разница между'. "
        "Line 2, orange: 'Single Phase and 3 Phase Inverter ?' → 'однофазным и трёхфазным инвертором?'. "
        "Left caption: 'LF SINGLE PHASE INVERTER' → 'ОДНОФАЗНЫЙ ИНВЕРТОР LF'. "
        "Right caption: 'HDSX 3 PHASE INVERTER' → 'ТРЁХФАЗНЫЙ ИНВЕРТОР HDSX'. "
        "Keep the orange VS badge as VS. Keep the orange circles 1 and 2. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the products, cards or badge. Do not redesign."
    ),
    (0, 1): (
        "This is a wide comparison banner on a beige background: a white wall inverter "
        "in a rounded card on the left and a black floor cabinet on the right, with an orange VS badge. "
        "Translate only the overlay headline and the two captions under the cards. Keep two headline lines. "
        "Line 1, black: 'What Is the Difference Between' → 'В чём разница между'. "
        "Line 2, orange: 'Single Phase and 3 Phase Inverter ?' → 'однофазным и трёхфазным инвертором?'. "
        "Left caption: 'LF SINGLE PHASE INVERTER' → 'ОДНОФАЗНЫЙ ИНВЕРТОР LF'. "
        "Right caption: 'HDSX 3 PHASE INVERTER' → 'ТРЁХФАЗНЫЙ ИНВЕРТОР HDSX'. "
        "Keep the orange VS badge as VS. Keep the orange circles 1 and 2. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the products, cards or badge. Do not redesign."
    ),
    (1, 0): (
        "This is a cropped night banner: a lit house, a candle, lightning, and a white hybrid inverter. "
        "Translate only the overlay headline and the green pill. Keep two white headline lines. "
        "Line 1: 'Reliable Power Inverter' → 'Надёжный инвертор'. "
        "Line 2: 'for Power Outages' → 'на случай отключения'. "
        "Green pill: 'Backup Energy Solution' → 'Резервное энергоснабжение'. "
        "Do NOT change HYBRID SOLAR INVERTER on the casing, the xindun logo, the display, buttons or CE marks. "
        "Do not move the house, candle, inverter or lightning. Do not redesign."
    ),
    (1, 1): (
        "This is a wide night banner: a lit house, a candle, lightning, and a white hybrid inverter. "
        "Translate only the overlay headline and the green pill. Keep two white headline lines. "
        "Line 1: 'Reliable Power Inverter' → 'Надёжный инвертор'. "
        "Line 2: 'for Power Outages' → 'на случай отключения'. "
        "Green pill: 'Backup Energy Solution' → 'Резервное энергоснабжение'. "
        "Do NOT change HYBRID SOLAR INVERTER on the casing, the xindun logo, the display, buttons or CE marks. "
        "Do not move the house, candle, inverter or lightning. Do not redesign."
    ),
    (2, 3): (
        "This is a tall product diagram on white: a cutaway energy-storage cabinet on top, "
        "a rear-panel close-up at bottom left, the real rear panel at bottom right, and four icons. "
        "Translate ONLY the callout labels on the white background and the four captions under the icons. "
        "'Solar Controller' → 'Солнечный контроллер'. 'Built-in MPPT' → 'Встроенный MPPT'. "
        "'Inverter' → 'Инвертор'. 'Pure Sine Wave' → 'Чистая синусоида'. "
        "'LiFePO4 Battery' → 'Батарея LiFePO4'. 'Longer Lifespan' → 'Дольше служит'. "
        "Under the icons: 'DC OUTPUT' → 'ВЫХОД DC'. Keep 'USB' as USB. "
        "'AC Output Socket' → 'Розетка выхода AC'. 'Terminal Strip' → 'Клеммник'. "
        "Do NOT change any text printed on the product itself: ENERGY STORAGE SYSTEM, "
        "LiFePO4+MPPT+INVERTER, the xindun logo, the display numbers, USB 5V, 12V, ON, OFF, "
        "AC OUTPUT, AC INPUT, N, L, PV, SOLAR, BATTERY, CAUTION, or the terminal markings. "
        "Keep the green leader lines, the cutaway, the circuit boards, the blue battery and both rear views. "
        "Do not add or remove parts. Do not redesign."
    ),
    (3, 0): (
        "This is a sunset banner with five inverters in front of a house and rooftop solar panels. "
        "Translate only the two-line pale headline. "
        "Line 1: 'What Is the Best 11KW' → 'Какой солнечный инвертор'. "
        "Line 2: 'Solar Inverter?' → 'на 11 кВт лучше?'. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the inverters, house, sky or panels. Do not redesign."
    ),
    (4, 0): (
        "This is a cropped pale-blue product banner: five white inverters on round podiums. "
        "Translate only the green headline: "
        "'Utility Interconnected Photovoltaic Inverters' → "
        "'Фотоэлектрические инверторы с подключением к сети'. "
        "Keep it as one green line. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the inverters, podiums or arch. Do not redesign."
    ),
    (4, 1): (
        "This is a wide pale-blue product banner: five white inverters on round podiums. "
        "Translate only the green headline: "
        "'Utility Interconnected Photovoltaic Inverters' → "
        "'Фотоэлектрические инверторы с подключением к сети'. "
        "Keep it as one green line. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the inverters, podiums or arch. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/20250821144527GjQcba.jpg",
            "alt_ru": "Разница между однофазным и трёхфазным инвертором",
            "title_ru": "Разница между однофазным и трёхфазным инвертором",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211444307681.jpg",
            "alt_ru": "Сравнение однофазного инвертора LF и трёхфазного HDSX",
            "title_ru": "Сравнение однофазного инвертора LF и трёхфазного HDSX",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/20250821140345oVrWhz.jpg",
            "alt_ru": "Надёжный инвертор на случай отключения электричества",
            "title_ru": "Надёжный инвертор на случай отключения электричества",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211408039800.jpg",
            "alt_ru": "Инвертор резервного питания при отключении",
            "title_ru": "Инвертор резервного питания при отключении",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg",
            "alt_ru": "Гибридный инвертор HFP",
            "title_ru": "Гибридный инвертор HFP",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151501334463.jpg",
            "alt_ru": "Гибридный инвертор HFP-C",
            "title_ru": "Гибридный инвертор HFP-C",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg",
            "alt_ru": "Параллельный гибридный инвертор HP PLUS+",
            "title_ru": "Параллельный гибридный инвертор HP PLUS+",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151505009158.jpg",
            "alt_ru": "Трёхфазный автономный инвертор HDSX",
            "title_ru": "Трёхфазный автономный инвертор HDSX",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211416117011.jpg",
            "alt_ru": "Инвертор LU с расщеплённой фазой",
            "title_ru": "Инвертор LU с расщеплённой фазой",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211051145263.jpg",
            "alt_ru": "Солнечный инвертор GP-C",
            "title_ru": "Солнечный инвертор GP-C",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151710038307.jpg",
            "alt_ru": "Автономный инвертор DF",
            "title_ru": "Автономный инвертор DF",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211107597731.jpg",
            "alt_ru": "Моноблочный солнечный генератор ESS-Li",
            "title_ru": "Моноблочный солнечный генератор ESS-Li",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211353482657.jpg",
            "alt_ru": "Солнечный генератор ESS при отключении",
            "title_ru": "Солнечный генератор ESS при отключении",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/18/2025081815123669Mvi1.jpg",
            "alt_ru": "Портативный инвертор с аккумулятором",
            "title_ru": "Портативный инвертор с аккумулятором",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/18/202508181513067423.jpg",
            "alt_ru": "Портативная электростанция для кемпинга и спасения",
            "title_ru": "Портативная электростанция для кемпинга и спасения",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/18/202508181513505996.jpg",
            "alt_ru": "Применение портативного инвертора на природе",
            "title_ru": "Применение портативного инвертора на природе",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/18/202508181514415005.jpg",
            "alt_ru": "Устройство портативного инвертора с аккумулятором",
            "title_ru": "Устройство портативного инвертора с аккумулятором",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/20250715151325yn7r9j.jpg",
            "alt_ru": "Лучший солнечный инвертор на 11 кВт",
            "title_ru": "Лучший солнечный инвертор на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg",
            "alt_ru": "Инвертор HFP на 11 кВт",
            "title_ru": "Инвертор HFP на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/06/202508061014537483.jpg",
            "alt_ru": "Солнечный инвертор HFP-C на 11 кВт",
            "title_ru": "Солнечный инвертор HFP-C на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151502199748.jpg",
            "alt_ru": "Солнечный инвертор HFP-E на 11 кВт",
            "title_ru": "Солнечный инвертор HFP-E на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151709439605.jpg",
            "alt_ru": "Инвертор LF на 11 кВт",
            "title_ru": "Инвертор LF на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/06/202508061015172459.jpg",
            "alt_ru": "Инвертор WF на 11 кВт",
            "title_ru": "Инвертор WF на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151505009158.jpg",
            "alt_ru": "Трёхфазный инвертор HDSX на 11 кВт",
            "title_ru": "Трёхфазный инвертор HDSX на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151710038307.jpg",
            "alt_ru": "Солнечный инвертор DF на 11 кВт",
            "title_ru": "Солнечный инвертор DF на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151510427948.jpg",
            "alt_ru": "Гибридный инвертор HF на 11 кВт",
            "title_ru": "Гибридный инвертор HF на 11 кВт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/06/202508061015336199.jpg",
            "alt_ru": "Производитель солнечных инверторов на 11 кВт",
            "title_ru": "Производитель солнечных инверторов на 11 кВт",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/20250714155319IH3g8f.jpg",
            "alt_ru": "Фотоэлектрические инверторы с подключением к сети",
            "title_ru": "Фотоэлектрические инверторы с подключением к сети",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141543223443.jpg",
            "alt_ru": "Линейка инверторов с подключением к сети",
            "title_ru": "Линейка инверторов с подключением к сети",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ru": "Инвертор HFP с подключением к сети",
            "title_ru": "Инвертор HFP с подключением к сети",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141550028678.jpg",
            "alt_ru": "Инвертор HFP-S с подключением к сети",
            "title_ru": "Инвертор HFP-S с подключением к сети",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ru": "Инвертор HFP-C с подключением к сети",
            "title_ru": "Инвертор HFP-C с подключением к сети",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ru": "Инвертор HFP-E с подключением к сети",
            "title_ru": "Инвертор HFP-E с подключением к сети",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141552243253.jpg",
            "alt_ru": "Инвертор HP PLUS+ с подключением к сети",
            "title_ru": "Инвертор HP PLUS+ с подключением к сети",
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
