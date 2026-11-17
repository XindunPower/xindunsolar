#!/usr/bin/env python3
"""Prepare page 9 Russian images.

Duomi gpt-image-2 only for English marketing headlines and wiring-diagram labels.
Studio product shots of HP PLUS+ and HU stay compressed and renamed only.
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
PAGE_NUM = 9

WIRE = (
    "This is a wiring diagram on a white background. Translate only the English labels to Russian. "
    "Keep every wire, color, arrow, breaker, DB9 plug, solar panel, house icon and battery icon. "
    "Keep the exact inverter count and which units share a bracket labeled P1, P2 or P3. "
    "Keep electrical symbols exactly: P1, P2, P3, N, L1, L2, L3, PV1+, PV1-. "
    "Do NOT change product faces, the xindun logo, or displays. Do not add or remove inverters. "
    "Do not redesign. Keep any small red annotation mark exactly where it is."
)
LABELS = (
    " Labels: 'Battery' → 'Аккумулятор'; 'Utility Grid' → 'Сеть'; "
    "'Loads' → 'Нагрузка'; 'PV array' → 'Массив PV'."
)
KEEP_CASE = (
    " Do NOT change product casing text (HYBRID SOLAR INVERTER, HYBRID INVERTER, "
    "LiFePO4 Lithium Battery), the xindun logo, CE, ISO, or the display."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a dark-blue marketing banner: a white clock ring, an alarm-clock icon, "
        "a gear icon, a lithium battery on the left and a hybrid inverter on the right. "
        "Translate only the white headline to Russian, keeping two lines: "
        "'Does The Scheduled Charge And Discharge Function of Off Grid Hybrid Inverter "
        "Affect Battery Life?' → "
        "'Влияет ли заряд и разряд по расписанию автономного гибридного инвертора "
        "на срок службы аккумулятора?'. "
        "Keep the ring, icons, products and blue background unchanged."
        + KEEP_CASE
        + " Do not redesign."
    ),
    (1, 0): (
        "This is a dark marketing banner: a hybrid inverter on the left, a lithium battery "
        "on the right, an orange clock and two white arrows between them. "
        "Translate only the headline to Russian and keep the second line orange: "
        "'Can The Off Grid Hybrid Inverter Be Set To' → "
        "'Можно ли задать у автономного гибридного инвертора'; "
        "'Timed Charging And Discharging?' → 'заряд и разряд по времени?'. "
        "Keep the clock, arrows, products and background unchanged."
        + KEEP_CASE
        + " Do not redesign."
    ),
    (2, 0): (
        "This is a blue-gray marketing banner: a hybrid inverter on the left, a lithium "
        "battery on the right, a dashed double arrow, and the large word BMS in the center. "
        "Translate only the white headline to Russian. Keep the letters BMS unchanged: "
        "'What Are The Function of The Communication Connection Between Inverter And "
        "Lithium Battery BMS?' → "
        "'Какие функции даёт связь инвертора с BMS литиевого аккумулятора?'. "
        "Keep BMS, the arrow, the rounded frame, products and background unchanged."
        + KEEP_CASE
        + " Do not redesign."
    ),
    (3, 0): (
        "This is a daylight marketing diagram: solar panels, a power pylon, AC loads, "
        "three white inverters and a lithium battery, with mountains and a solar farm behind. "
        "Translate only the headline and the diagram labels to Russian: "
        "'Can Single Phase Hybrid Inverter Output Three Phase AC Power?' → "
        "'Может ли однофазный гибридный инвертор выдавать трёхфазный переменный ток?'; "
        "'Three phase parallel operation' → 'Трёхфазная параллельная работа'; "
        "'Solar Panels' → 'Солнечные панели'; 'Power Grid' → 'Сеть'; "
        "'AC Loads' → 'Нагрузка AC'; 'Battery' → 'Аккумулятор'. "
        "Keep L1, L2, L3, N and 380V exactly. Keep three inverters, one battery, arrows and background."
        + KEEP_CASE
        + " Do not redesign."
    ),
    (3, 1): (
        WIRE + LABELS
        + " Three inverters in one row. Top labels are P1, P2 and P3, one inverter each. "
        "This is the 1+1+1 three-phase diagram. Six PV array labels along the bottom."
    ),
    (3, 2): (
        WIRE + LABELS
        + " Four inverters. The P1 bracket covers the first two inverters. "
        "P2 and P3 are one inverter each. This is the 2+1+1 diagram."
    ),
    (3, 3): (
        WIRE + LABELS
        + " Five inverters. P1 covers two, P2 covers two, P3 is one. "
        "This is the 2+2+1 diagram. Keep the small red mark in the middle of the wires."
    ),
    (3, 4): (
        WIRE + LABELS
        + " Five inverters. P1 covers the first three. P2 and P3 are one inverter each. "
        "This is the 3+1+1 diagram."
    ),
    (3, 5): (
        WIRE + LABELS
        + " Six inverters. P1, P2 and P3 each cover two inverters. "
        "This is the 2+2+2 diagram."
    ),
    (3, 6): (
        WIRE + LABELS
        + " Six inverters. P1 covers the first three, P2 covers the next two, P3 is the last one. "
        "This is the 3+2+1 diagram. Keep the small red mark near the bottom-left plugs."
    ),
    (3, 7): (
        WIRE + LABELS
        + " Six inverters. The P1 bracket covers the first four. "
        "P2 and P3 are one inverter each. This is the 4+1+1 diagram."
    ),
    (4, 0): (
        "This is a sunset marketing diagram over a solar farm: panels, a pylon, AC loads, "
        "three white inverters and a lithium battery. "
        "Translate only the headline and the diagram labels to Russian: "
        "'Can Hybrid Inverter Support Parallel Operation?' → "
        "'Поддерживает ли гибридный инвертор параллельную работу?'; "
        "'Inverter Parallel Operation' → 'Параллельная работа инверторов'; "
        "'Solar Panels' → 'Солнечные панели'; 'Power Grid' → 'Сеть'; "
        "'AC Loads' → 'Нагрузка AC'; 'Battery' → 'Аккумулятор'. "
        "Keep three inverters, one battery, arrows, sunset and solar-farm background."
        + KEEP_CASE
        + " Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/20251015141934Q1iFl3.jpg",
            "alt_ru": "Срок службы аккумулятора инвертора",
            "title_ru": "Срок службы аккумулятора инвертора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/20251015135824gYTtGy.jpg",
            "alt_ru": "Автономный гибридный инвертор",
            "title_ru": "Автономный гибридный инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg",
            "alt_ru": "Автономный гибридный солнечный инвертор HP PLUS+",
            "title_ru": "Автономный гибридный солнечный инвертор HP PLUS+",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151404306156.jpg",
            "alt_ru": "Автономный гибридный инвертор серии HU",
            "title_ru": "Автономный гибридный инвертор серии HU",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151351572844.jpg",
            "alt_ru": "Связь инвертора с BMS литиевого аккумулятора",
            "title_ru": "Связь инвертора с BMS литиевого аккумулятора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141455215992.jpg",
            "alt_ru": "Трёхфазный выход однофазного гибридного инвертора",
            "title_ru": "Трёхфазный выход однофазного гибридного инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141439441653.jpg",
            "alt_ru": "Однофазный гибридный инвертор в трёхфазной схеме",
            "title_ru": "Однофазный гибридный инвертор в трёхфазной схеме",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141441107491.jpg",
            "alt_ru": "Четыре инвертора на трёхфазный выход",
            "title_ru": "Четыре инвертора на трёхфазный выход",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141441527553.jpg",
            "alt_ru": "Пять инверторов на трёхфазный выход",
            "title_ru": "Пять инверторов на трёхфазный выход",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141443026342.jpg",
            "alt_ru": "Трёхфазный гибридный инвертор",
            "title_ru": "Трёхфазный гибридный инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141447436781.jpg",
            "alt_ru": "Шесть инверторов на трёхфазный выход",
            "title_ru": "Шесть инверторов на трёхфазный выход",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141448025033.jpg",
            "alt_ru": "Гибридный инвертор",
            "title_ru": "Гибридный инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141448369932.jpg",
            "alt_ru": "Может ли однофазный гибридный инвертор выдать трёхфазный ток",
            "title_ru": "Может ли однофазный гибридный инвертор выдать трёхфазный ток",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141520491752.jpg",
            "alt_ru": "Параллельный гибридный инвертор",
            "title_ru": "Параллельный гибридный инвертор",
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
                size = size_for(*orig_wh)
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
