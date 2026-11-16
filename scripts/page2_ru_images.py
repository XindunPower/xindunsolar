#!/usr/bin/env python3
"""Prepare page 2 Russian images.

Duomi gpt-image-2 only for English marketing/diagram overlays.
The installation photo has no marketing overlay and is compressed and renamed only.
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
PAGE_NUM = 2

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a green marketing banner: solar panel and two white inverters, a green shield, "
        "and three circular badges. Translate only the English overlay text to Russian, keeping the same "
        "two-line headline and the three badges: "
        "'How to Prevent' → 'Как предотвратить'; "
        "'INVERTER DAMAGE?' → 'ПОВРЕЖДЕНИЕ ИНВЕРТОРА?'; "
        "'Overvoltage' → 'Перенапряжение'; "
        "'Overcurrent' → 'Сверхток'; "
        "'Load Surge' → 'Бросок нагрузки'. "
        "Keep the question mark, lightning badge, gauge badge, pump badge, shield, solar panel, "
        "both inverters, grass, and forest unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo, CE marks, or the display. Do not add or remove objects. Do not redesign the poster. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original text area."
    ),
    (1, 0): (
        "This is a dusk marketing banner with two white inverters, a battery, a clock, a light bulb, "
        "and two speech bubbles. Translate only the English overlay text to Russian, keeping the two-line headline: "
        "'Should I Leave My' → 'Нужно ли оставлять'; "
        "'Inverter On All The Time?' → 'инвертор включённым постоянно?'; "
        "'Keep ON?' → 'Держать ВКЛ?'; "
        "'Turn OFF?' → 'Выключить?'. "
        "Keep the question mark in the sky, check mark, power icon, warning triangle, clock, battery, "
        "light bulb, solar panels, houses, wind turbine, power lines, and both inverters unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER), the xindun logo, CE marks, or displays. "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original text area."
    ),
    (2, 0): (
        "This is a light-green diagram banner: one white inverter, solar panels, a wind turbine, "
        "and three gauges with arrows. Translate only the English overlay text to Russian: "
        "'How Many Amps of Current Does a' → 'Сколько ампер тока потребляет'; "
        "'2000 Watt Inverter Consume?' → 'инвертор на 2000 ватт?'; "
        "'12V DC INPUT' → 'ВХОД 12 В DC'; "
        "'24V DC INPUT' → 'ВХОД 24 В DC'; "
        "'48V DC INPUT' → 'ВХОД 48 В DC'; "
        "'HIGH' → 'ВЫСОКИЙ'; "
        "'MEDIUM' → 'СРЕДНИЙ'; "
        "'LOW' → 'НИЗКИЙ'. "
        "Keep the figures 185.2A, 92.6A and 46.3A exactly, including the letter A and the decimal point. "
        "Keep the arrows, gauges, waveform lines, panels, turbine, and inverter unchanged. "
        "Do NOT change product casing text (Low Frequency PV Inverter), the xindun logo, CE mark, "
        "or the numbers on the inverter display. Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original text area."
    ),
    (3, 0): (
        "This is a day-and-night marketing banner: house with rooftop solar, two white units, "
        "an orange MPPT controller, and three icons. Translate only the English overlay text to Russian: "
        "'What Is' → 'Что такое'; "
        "'SHS Solar Home System?' → 'домашняя солнечная система SHS?'; "
        "'Reliable Off-Grid Power Solution for Your Home.' → 'Надёжное автономное питание для дома.'; "
        "'Reduce Electricity Costs' → 'Меньше плата за свет'; "
        "'24/7 Energy Security' → 'Энергия 24/7'; "
        "'Green & Sustainable' → 'Экологично'. "
        "Keep SHS and 24/7 in Latin characters. Keep the sun, moon, house, panels, wooden table, "
        "icons, and all three products unchanged. "
        "Do NOT change product casing text (LiFePO4 Lithium Battery, MPPT Solar Charge Controller), "
        "the xindun logo, CE marks, or the controller screen. Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original text area."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/03/31/202603311201351097.jpg",
            "alt_ru": "Повреждение инвертора",
            "title_ru": "Повреждение инвертора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/03/28/202603281528155286.jpg",
            "alt_ru": "Нужно ли оставлять инвертор включённым постоянно",
            "title_ru": "Нужно ли оставлять инвертор включённым постоянно",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/30/202601301718427091.jpg",
            "alt_ru": "Ток инвертора 2000 ватт в амперах",
            "title_ru": "Ток инвертора 2000 ватт в амперах",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/27/202601271623259348.jpg",
            "alt_ru": "Солнечные решения SHS",
            "title_ru": "Солнечные решения SHS",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/27/202601271622219263.jpg",
            "alt_ru": "Примеры установки домашней солнечной системы SHS",
            "title_ru": "Примеры установки домашней солнечной системы SHS",
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
