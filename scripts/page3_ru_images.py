#!/usr/bin/env python3
"""Prepare page 3 Russian images.

Duomi gpt-image-2 only for English marketing/diagram overlays.
Product studio shots and the installation collage have no marketing overlay
and are compressed and renamed only.
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
PAGE_NUM = 3

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a wide marketing banner: wind turbine, solar roof, six power products, "
        "a transmission tower and green hills. Translate only the three-line English headline "
        "overlay to Russian, keeping the huge middle line and the question mark: "
        "'What Can Run Off a' → 'Что может питать'; "
        "'5000 Watt' → '5000 ватт'; "
        "'Power Converter?' → 'преобразователь мощности?'. "
        "Keep the digits 5000 large and on the center line. Keep the question mark. "
        "Keep every product, the panels, turbine, tower, sun, grass and sky unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, SPLIT PHASE INVERTER, "
        "Low Frequency Inverter, ENERGY STORAGE SYSTEM, ALL IN ONE SOLAR GENERATOR, SOLAR GENERATOR), "
        "the xindun logo, CE marks or displays. Do not add or remove objects. Do not redesign the poster. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original headline area."
    ),
    (1, 0): (
        "This is a four-scene diagram banner with a central white inverter, yellow arrows, "
        "a solar panel, a city power grid, a battery and day/night houses. Translate only the "
        "English overlay text to Russian: "
        "'Can inverter run only on sun panel?' → 'Может ли инвертор работать только от солнечной панели?'; "
        "'Sun Panel' → 'Солнечная панель'; "
        "'Grid' → 'Сеть'; "
        "'Battery' → 'Аккумулятор'. "
        "Keep the question mark, yellow arrows, sun, moon, panels, houses, towers and both products unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo, CE marks or displays. Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original text area."
    ),
    (2, 0): (
        "This is a diagram banner over a solar field: a power curve on the left, three capacity bars "
        "on the right, one inverter and one battery in front. Translate only the English overlay text "
        "to Russian, keeping the three-line headline: "
        "'How to do' → 'Как выполнить'; "
        "'Inverter Battery Size Calculation' → 'расчёт ёмкости аккумулятора инвертора'; "
        "'to Choose the Right Lithium Battery?' → 'и выбрать подходящую литиевую батарею?'; "
        "'Inverter Output Power' → 'Выходная мощность инвертора'; "
        "'Battery Capacity in kWh' → 'Ёмкость аккумулятора, кВт·ч'. "
        "Keep the figures 10kW, 5kWh, 10kWh and 15kWh exactly, including kW and kWh. "
        "Keep the curve, bars, arrow, sun, panels, grass and both products unchanged. "
        "Do NOT change product casing text (LiFePO4 Lithium Battery), the xindun logo, CE marks or the display. "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original text area."
    ),
    (3, 0): (
        "This is a landscape marketing banner: a solar array, mountains, two white units on a dirt road "
        "and power lines. Translate only the two-line English headline to Russian: "
        "'What Is a' → 'Что такое'; "
        "'Split Phase Parallel Hybrid Inverter?' → 'параллельный гибридный инвертор с расщеплённой фазой?'. "
        "Keep the question mark. Keep the sun, mountains, palms, panels, road, towers and both products unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo, CE marks or the battery screen. Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original headline area."
    ),
    (4, 0): (
        "This is a dusk-to-night house banner with rooftop solar, an inverter, a battery, a light bulb, "
        "a television and a refrigerator. Translate only the English overlay text to Russian, keeping two lines: "
        "'Solar Inverter and Battery for Home' → 'Солнечный инвертор и аккумулятор для дома'; "
        "'Stable Power, Day & Night' → 'Стабильное питание днём и ночью'. "
        "Keep the moon, house, panels, arrows, bulb, television, refrigerator and both products unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo, CE marks or displays. Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original text area."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241659115926.jpg",
            "alt_ru": "Преобразователь мощности на 5000 ватт",
            "title_ru": "Преобразователь мощности на 5000 ватт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241700361463.jpg",
            "alt_ru": "Преобразователь HFP на 5000 ватт",
            "title_ru": "Преобразователь HFP на 5000 ватт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241701207934.jpg",
            "alt_ru": "Преобразователь мощности LU с расщеплённой фазой",
            "title_ru": "Преобразователь мощности LU с расщеплённой фазой",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241702338686.jpg",
            "alt_ru": "Преобразователь мощности WF на 5000 ватт",
            "title_ru": "Преобразователь мощности WF на 5000 ватт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241704337778.jpg",
            "alt_ru": "Преобразователь LF на 5000 ватт",
            "title_ru": "Преобразователь LF на 5000 ватт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241712586945.jpg",
            "alt_ru": "Моноблочный преобразователь мощности ESS-Li на 5000 ватт",
            "title_ru": "Моноблочный преобразователь мощности ESS-Li на 5000 ватт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241715091918.jpg",
            "alt_ru": "Солнечный преобразователь мощности ESS на 5000 ватт",
            "title_ru": "Солнечный преобразователь мощности ESS на 5000 ватт",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241649054608.jpg",
            "alt_ru": "Инвертор солнечной панели",
            "title_ru": "Инвертор солнечной панели",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/23/202601231503001875.jpg",
            "alt_ru": "Расчёт ёмкости аккумулятора для инвертора",
            "title_ru": "Расчёт ёмкости аккумулятора для инвертора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/22/202601221743309376.jpg",
            "alt_ru": "Параллельный гибридный инвертор с расщеплённой фазой",
            "title_ru": "Параллельный гибридный инвертор с расщеплённой фазой",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161559208083.jpg",
            "alt_ru": "Солнечный инвертор и аккумулятор для дома",
            "title_ru": "Солнечный инвертор и аккумулятор для дома",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161601195480.jpg",
            "alt_ru": "Пример установки солнечного инвертора и аккумулятора для дома",
            "title_ru": "Пример установки солнечного инвертора и аккумулятора для дома",
        },
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
