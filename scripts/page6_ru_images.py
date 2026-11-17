#!/usr/bin/env python3
"""Prepare page 6 Russian images.

Duomi gpt-image-2 only for the five English marketing banners.
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
    USED_FILE_STEMS,
    compress_only,
    run_duomi,
    size_for,
    slugify,
)

UA = "Mozilla/5.0 (compatible; XindunRussianBot/1.0)"
PAGE_NUM = 6

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a 3:2 marketing banner: eight white and black inverters on a gold podium, desert dunes behind. "
        "Translate only the two-line English headline to Russian: "
        "'What You Should Know About' → 'Что нужно знать о'; "
        "'Hybrid Inverter Before Building Solar System?' → 'гибридном инверторе перед сборкой солнечной системы?'. "
        "Keep the question mark, gold type color, products, podium and desert unchanged. "
        "Do NOT change product casing text (ALL IN ONE SOLAR GENERATOR, SPLIT PHASE INVERTER, HYBRID SOLAR INVERTER), "
        "the xindun logo, CE marks or displays. Do not redesign."
    ),
    (1, 0): (
        "This is a 3:2 night banner: a white hybrid inverter and a white LiFePO4 battery on a clock-face background. "
        "Translate only the headline to Russian, keeping the orange pill on the first words: "
        "'24 Hours' → '24 часа'; 'Backup Inverter' → 'Инвертор резерва'. "
        "Keep both products, clock, stars and the orange/white headline layout unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery, xindun GREEN POWER), "
        "the logo, CE marks or the displays. Do not redesign."
    ),
    (2, 0): (
        "This is a 3:2 product banner on a pale blue background: eight units on a white round podium. "
        "Translate only the two-line headline to Russian, keeping 48 large and blue: "
        "'48 Volt' → '48 вольт'; 'Off Grid Inverter' → 'Автономный инвертор'. "
        "Keep every product, podium and background unchanged. "
        "Do NOT change casing text (ALL IN ONE SOLAR GENERATOR and other product labels), "
        "the xindun logo or displays. Do not redesign."
    ),
    (3, 0): (
        "This is a 3:2 daylight banner: a house with rooftop solar panels and eight inverters on the lawn. "
        "Translate only the headline to Russian, keeping the orange highlight on the middle phrase and 8 кВт readable: "
        "'What Can' → 'Что может'; "
        "'8KW Solar Hybrid Inverter' → 'солнечный гибридный инвертор 8 кВт'; "
        "'Do?' → 'сделать?'. "
        "Keep the question mark, house, panels, sky, grass and every product unchanged. "
        "Do NOT change product casing text, the xindun logo or displays. Do not redesign."
    ),
    (4, 0): (
        "This is a 3:2 night banner: a lit house, moon, a plug with lightning, an inverter, a LiFePO4 battery and solar panels. "
        "Translate only the two-line headline to Russian, keeping the first line white and the second line red: "
        "'DOES THE SOLAR INVERTER' → 'ОТКЛЮЧАЕТСЯ ЛИ СОЛНЕЧНЫЙ ИНВЕРТОР'; "
        "'TURN OFF AT NIGHT?' → 'НОЧЬЮ?'. "
        "Keep the question mark, house, moon, car, plug, products and panels unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), the xindun logo or displays. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181628389949.jpg", "alt_ru": "О гибридном инверторе", "title_ru": "О гибридном инверторе"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg", "alt_ru": "Гибридный инвертор HFP", "title_ru": "Гибридный инвертор HFP"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151404306156.jpg", "alt_ru": "Гибридный инвертор HU с расщеплённой фазой", "title_ru": "Гибридный инвертор HU с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg", "alt_ru": "Параллельный гибридный инвертор HP PLUS+", "title_ru": "Параллельный гибридный инвертор HP PLUS+"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211416117011.jpg", "alt_ru": "Гибридный инвертор LU", "title_ru": "Гибридный инвертор LU"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151505009158.jpg", "alt_ru": "Трёхфазный гибридный инвертор HDSX", "title_ru": "Трёхфазный гибридный инвертор HDSX"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151709439605.jpg", "alt_ru": "Гибридный инвертор LF", "title_ru": "Гибридный инвертор LF"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211353482657.jpg", "alt_ru": "Моноблочный солнечный генератор ESS", "title_ru": "Моноблочный солнечный генератор ESS"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211107597731.jpg", "alt_ru": "Солнечный генератор ESS-Li", "title_ru": "Солнечный генератор ESS-Li"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091544188167.jpg", "alt_ru": "Инвертор с резервом на 24 часа", "title_ru": "Инвертор с резервом на 24 часа"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181609357954.jpg", "alt_ru": "Автономный инвертор 48 вольт", "title_ru": "Автономный инвертор 48 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg", "alt_ru": "Инвертор HU 48 вольт с расщеплённой фазой", "title_ru": "Инвертор HU 48 вольт с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg", "alt_ru": "Параллельный инвертор HP Plus+ 48 вольт", "title_ru": "Параллельный инвертор HP Plus+ 48 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png", "alt_ru": "Автономный инвертор HFP 48 вольт", "title_ru": "Автономный инвертор HFP 48 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg", "alt_ru": "Автономный инвертор HFP-E 48 вольт", "title_ru": "Автономный инвертор HFP-E 48 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181614417438.jpg", "alt_ru": "Трёхфазный инвертор HDSX 48 вольт", "title_ru": "Трёхфазный инвертор HDSX 48 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125237036.jpg", "alt_ru": "Инвертор LU 48 вольт с расщеплённой фазой", "title_ru": "Инвертор LU 48 вольт с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181616085997.jpg", "alt_ru": "Инвертор WF 48 вольт", "title_ru": "Инвертор WF 48 вольт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181616422042.jpg", "alt_ru": "Солнечный генератор ESS 48 вольт", "title_ru": "Солнечный генератор ESS 48 вольт"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091013036397.jpg", "alt_ru": "Солнечный гибридный инвертор 8 кВт", "title_ru": "Солнечный гибридный инвертор 8 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg", "alt_ru": "Гибридный инвертор 8 кВт", "title_ru": "Гибридный инвертор 8 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091015453907.jpg", "alt_ru": "Солнечный инвертор HFP-C 8 кВт", "title_ru": "Солнечный инвертор HFP-C 8 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151505009158.jpg", "alt_ru": "Трёхфазный инвертор 8 кВт", "title_ru": "Трёхфазный инвертор 8 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211416117011.jpg", "alt_ru": "Гибридный инвертор 8 кВт с расщеплённой фазой", "title_ru": "Гибридный инвертор 8 кВт с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091019088117.jpg", "alt_ru": "Солнечный инвертор WF 8 кВт", "title_ru": "Солнечный инвертор WF 8 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091020017762.jpg", "alt_ru": "Солнечный инвертор WD 8 кВт", "title_ru": "Солнечный инвертор WD 8 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151709439605.jpg", "alt_ru": "Солнечный инвертор LF 8 кВт", "title_ru": "Солнечный инвертор LF 8 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091529333216.jpg", "alt_ru": "Инвертор DF 8 кВт", "title_ru": "Инвертор DF 8 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091038043837.jpg", "alt_ru": "Пример установки солнечного инвертора 8 кВт", "title_ru": "Пример установки солнечного инвертора 8 кВт"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091057481969.jpg", "alt_ru": "Отключается ли солнечный инвертор ночью", "title_ru": "Отключается ли солнечный инвертор ночью"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151404306156.jpg", "alt_ru": "Солнечный инвертор с расщеплённой фазой", "title_ru": "Солнечный инвертор с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg", "alt_ru": "Параллельный солнечный инвертор", "title_ru": "Параллельный солнечный инвертор"},
    ],
]

IMAGE_LOG: list[dict] = []


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


def prepare_all() -> list[list[dict]]:
    prepared_all: list[list[dict]] = []
    for article_idx, images in enumerate(IMAGE_SOURCES):
        prepared: list[dict] = []
        for img_idx, im in enumerate(images):
            stem = stem_for(im["alt_ru"], im["src"])
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
