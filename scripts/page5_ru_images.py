#!/usr/bin/env python3
"""Prepare page 5 Russian images.

Duomi gpt-image-2 only for English marketing headlines and wiring-diagram labels.
Product studio shots and the installation photo collage are compressed only.
"""

from __future__ import annotations

import json
import sys
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
PAGE_NUM = 5

WIRE = (
    "This is a wiring diagram. Translate only the English diagram labels to Russian. "
    "Keep every wire, color, arrow, icon, product photo and terminal mark. "
    "Keep electrical symbols exactly: L, N, L1, L2, P1, P2, +, −, and the figures 12V, 120V, 240V. "
    "Do NOT change product casing text (HYBRID SOLAR INVERTER, SPLIT PHASE INVERTER, "
    "Low Frequency Inverter, LiFePO4), the xindun logo, or displays. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a 3:2 marketing banner: a house with rooftop solar, a field of panels, turbines, "
        "and eight white or black power products on grass. Translate only the English headline to Russian: "
        "'How to Choose the Right' → 'Как выбрать подходящий'; "
        "'Photovoltaic Power Converter' → 'фотоэлектрический преобразователь мощности'; "
        "'For Residential, Commercial & Industrial Applications' → 'Для дома, коммерции и промышленности'. "
        "Keep products, house, panels, sky and grass unchanged. "
        "Do NOT change product casing text, the xindun logo or displays. Do not redesign."
    ),
    (1, 0): (
        "This is a 3:2 product banner on a pale blue background: three white units on a round podium. "
        "Translate only the headline to Russian: "
        "'10KW Split Phase Inverter' → 'Инвертор 10 кВт с расщеплённой фазой'. "
        "Keep 10 кВт readable. Keep the three products, podium and background unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, Low Frequency Inverter, SPLIT PHASE INVERTER), "
        "the xindun logo or displays. Do not redesign."
    ),
    (1, 1): (
        WIRE + " Labels: 'Battery' → 'Аккумулятор'; 'Power Grid' → 'Сеть'; "
        "'AC Loads' → 'Нагрузка AC'; 'PV Array' → 'Массив PV'. "
        "Three inverters in one row. This is single-phase parallel wiring."
    ),
    (1, 2): (
        WIRE + " Labels: 'Battery' → 'Аккумулятор'; 'Power Grid' → 'Сеть'; "
        "'AC Loads' → 'Нагрузка AC'; 'PV Array' → 'Массив PV'. "
        "Three inverters. This is split-phase parallel wiring."
    ),
    (1, 3): (
        WIRE + " Labels: 'Battery' → 'Аккумулятор'; 'Power Grid' → 'Сеть'; "
        "'AC Loads' → 'Нагрузка AC'; 'PV Array' → 'Массив PV'. "
        "Keep the top labels P1 and P2. This is two-phase split-phase parallel wiring."
    ),
    (1, 4): (
        WIRE + " Labels: 'Battery' → 'Аккумулятор'; 'Power Grid' → 'Сеть'; "
        "'AC Loads' → 'Нагрузка AC'; 'PV Array' → 'Массив PV'. "
        "Three inverters with green, red and blue phase wires. This is three-phase parallel wiring."
    ),
    (1, 5): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'Battery' → 'Аккумулятор'; "
        "'Power Grid' → 'Сеть'; 'AC Loads' → 'Нагрузка AC'. "
        "One inverter, grid at 120V L1-N, loads at 240V and 120V. Single-phase system."
    ),
    (1, 6): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'Battery' → 'Аккумулятор'; "
        "'Power Grid' → 'Сеть'; 'AC Loads' → 'Нагрузка AC'. "
        "Grid shows L1 L2 N with 120V and 240V. Split-phase system."
    ),
    (1, 7): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'AC Input' → 'Вход AC'; "
        "'or' → 'или'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'; "
        "'AC Output' → 'Выход AC'; 'Laptop' → 'Ноутбук'; 'Printer' → 'Принтер'; "
        "'TV' → 'Телевизор'; 'Fans' → 'Вентиляторы'; 'Water pump' → 'Насос'."
    ),
    (1, 8): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'Utility Grid' → 'Сеть'; "
        "'OR' → 'ИЛИ'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'; "
        "'AC OUTPUT' → 'Выход AC'; 'AC Loads' → 'Нагрузка AC'. "
        "Keep 12V, 240V, L1, L2 and N."
    ),
    (2, 0): (
        "This is a night marketing banner: a white inverter on the left and a cutaway house on the right. "
        "Translate only the two-line headline to Russian, keeping 3000 large: "
        "'Will 3000 Watt Pure Sine Wave Inverter' → 'Потянет ли инвертор чистой синусоиды на 3000 ватт'; "
        "'Run a House?' → 'целый дом?'. "
        "Keep the question mark, inverter, house, fridge, AC, TV and sine wave unchanged. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, CE, ISO or the display. Do not redesign."
    ),
    (3, 0): (
        "This is a dusk banner of two white units on a lawn in front of a house. "
        "Translate only the headline to Russian: "
        "'Solar Battery Backup Inverter' → 'Солнечный инвертор резерва с аккумулятором'. "
        "Keep both products, house, grass and sky unchanged. "
        "Do NOT change casing text (LiFePO4 Lithium Battery, HYBRID SOLAR INVERTER), "
        "the xindun logo or displays. Do not redesign."
    ),
    (4, 0): (
        "This is a pale-blue product lineup banner with eight units. "
        "Translate only the stacked headline to Russian: "
        "'12 Volt' → '12 вольт'; '220 Volt' → '220 вольт'; 'INVERTER' → 'ИНВЕРТОР'. "
        "Keep the orange and blue headline blocks and every product unchanged. "
        "Do NOT change product casing text, the xindun logo or displays. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/26/202512261347465141.jpg", "alt_ru": "Фотоэлектрический преобразователь мощности", "title_ru": "Фотоэлектрический преобразователь мощности"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/26/202512261348523657.jpg", "alt_ru": "Примеры применения фотоэлектрического преобразователя", "title_ru": "Примеры применения фотоэлектрического преобразователя"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png", "alt_ru": "Гибридный фотоэлектрический преобразователь мощности", "title_ru": "Гибридный фотоэлектрический преобразователь мощности"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg", "alt_ru": "Солнечный преобразователь мощности", "title_ru": "Солнечный преобразователь мощности"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png", "alt_ru": "Фотоэлектрический преобразователь", "title_ru": "Фотоэлектрический преобразователь"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125487765.jpg", "alt_ru": "Трёхфазный фотоэлектрический преобразователь мощности", "title_ru": "Трёхфазный фотоэлектрический преобразователь мощности"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125237036.jpg", "alt_ru": "Фотоэлектрический преобразователь с расщеплённой фазой", "title_ru": "Фотоэлектрический преобразователь с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181616085997.jpg", "alt_ru": "Фотоэлектрический преобразователь PV", "title_ru": "Фотоэлектрический преобразователь PV"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757379506.jpg", "alt_ru": "Преобразователь для фотоэлектричества", "title_ru": "Преобразователь для фотоэлектричества"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091126518485.jpg", "alt_ru": "Моноблочный фотоэлектрический генератор", "title_ru": "Моноблочный фотоэлектрический генератор"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/23/202512231811267150.jpg", "alt_ru": "Инвертор 10 кВт с расщеплённой фазой", "title_ru": "Инвертор 10 кВт с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141154031704.jpg", "alt_ru": "Однофазная параллельная работа HU", "title_ru": "Однофазная параллельная работа HU"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155069284.jpg", "alt_ru": "Параллельная работа HU с расщеплённой фазой", "title_ru": "Параллельная работа HU с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141157382346.jpg", "alt_ru": "Двухфазная параллельная работа с расщеплением", "title_ru": "Двухфазная параллельная работа с расщеплением"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155496791.jpg", "alt_ru": "Трёхфазная параллельная работа инвертора", "title_ru": "Трёхфазная параллельная работа инвертора"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/23/202512231759127889.jpg", "alt_ru": "Инвертор с расщеплённой фазой", "title_ru": "Инвертор с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141426036849.jpg", "alt_ru": "Инвертор 10 кВт с расщеплённой фазой, схема", "title_ru": "Инвертор 10 кВт с расщеплённой фазой, схема"},
        {"src": "https://www.xindun-power.com/uploadfile/2024/11/09/202411091606366102.jpg", "alt_ru": "Однофазная схема инвертора с расщеплённой фазой", "title_ru": "Однофазная схема инвертора с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141432533866.jpg", "alt_ru": "Инвертор на 10 кВт", "title_ru": "Инвертор на 10 кВт"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/23/202512231745238361.jpg", "alt_ru": "Инвертор чистой синусоиды на 3000 ватт", "title_ru": "Инвертор чистой синусоиды на 3000 ватт"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201713589748.jpg", "alt_ru": "Солнечный инвертор резервного питания с аккумулятором", "title_ru": "Солнечный инвертор резервного питания с аккумулятором"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201646268458.jpg", "alt_ru": "Инвертор 12 вольт 220 вольт", "title_ru": "Инвертор 12 вольт 220 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201649052138.jpg", "alt_ru": "Инвертор HFP 12 вольт 220 вольт", "title_ru": "Инвертор HFP 12 вольт 220 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201650119960.jpg", "alt_ru": "Низкочастотный инвертор LF 12 вольт 220 вольт", "title_ru": "Низкочастотный инвертор LF 12 вольт 220 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201650488303.jpg", "alt_ru": "Солнечный инвертор DF 220 вольт", "title_ru": "Солнечный инвертор DF 220 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201651201692.jpg", "alt_ru": "Инвертор LS 12 вольт", "title_ru": "Инвертор LS 12 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201652418130.jpg", "alt_ru": "Солнечный инвертор WF 220 вольт", "title_ru": "Солнечный инвертор WF 220 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201653434694.jpg", "alt_ru": "Инвертор WD 12 вольт 220 вольт", "title_ru": "Инвертор WD 12 вольт 220 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201655539810.jpg", "alt_ru": "Солнечный генератор ESS-Li 220 вольт", "title_ru": "Солнечный генератор ESS-Li 220 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201656447609.jpg", "alt_ru": "Солнечный генератор 12 вольт 220 вольт", "title_ru": "Солнечный генератор 12 вольт 220 вольт"},
    ],
]

IMAGE_LOG: list[dict] = []


def prepare_all() -> list[list[dict]]:
    prepared_all: list[list[dict]] = []
    for article_idx, images in enumerate(IMAGE_SOURCES):
        prepared: list[dict] = []
        for img_idx, im in enumerate(images):
            stem = unique_stem(slugify(im["alt_ru"]))
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
                if size_ok and meta.get("method") == expected and meta.get("src") == im["src"]:
                    final = tagged
                    method = "duomi-reuse" if need_duomi else "compress-reuse"
                    duomi_path = meta.get("duomi_path")
                    reused = True
                    print(f"[img] reuse {tagged.name} method={method}", flush=True)
            if reused:
                pass
            elif need_duomi:
                size = size_for(*orig_wh)
                result = run_duomi(
                    im["src"],
                    DUOMI_MAP[(article_idx, img_idx)],
                    stem,
                    size,
                    orig_wh,
                    local,
                    attempts=3,
                )
                if result is None:
                    print(
                        f"[duomi] fallback original compress for a{article_idx}_i{img_idx}",
                        flush=True,
                    )
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
                json.dumps(
                    {"method": stored, "src": im["src"], "duomi_path": duomi_path},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            entry = {
                "local": final,
                "alt_ru": im["alt_ru"],
                "title_ru": im["title_ru"],
                "src_orig": im["src"],
                "method": method,
                "duomi_path": duomi_path,
                "orig_wh": orig_wh,
            }
            IMAGE_LOG.append(
                {
                    "article": article_idx,
                    "img": img_idx,
                    **{k: (str(v) if k == "local" else v) for k, v in entry.items()},
                }
            )
            prepared.append(entry)
            print(
                f"[img] a{article_idx}_i{img_idx} method={method} -> {final.name} "
                f"{final.stat().st_size}b {orig_wh}",
                flush=True,
            )
        prepared_all.append(prepared)
    Path(f"/tmp/page{PAGE_NUM}_ru_image_log.json").write_text(
        json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return prepared_all


if __name__ == "__main__":
    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
