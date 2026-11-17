#!/usr/bin/env python3
"""Prepare page 10 Russian images.

Duomi gpt-image-2 only for English marketing headlines and wiring-diagram labels.
Studio product shots, panel close-ups and installation photos stay compressed and renamed.
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
PAGE_NUM = 10

KEEP_CASE = (
    " Do NOT change product casing text, the xindun logo, CE, ISO, displays, "
    "or model markings. Do not add or remove products. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a light-gray marketing banner: one white wall inverter in the center "
        "and four orange rounded icons (bug, water drop, dust filter, sun). "
        "Translate only the top headline to Russian, keep it on one line: "
        "'INVERTER PROTECTION LEVEL' → 'СТЕПЕНЬ ЗАЩИТЫ ИНВЕРТОРА'. "
        "Keep the second line of rating codes exactly: IP20 IP21 IP54 IP65 IP66. "
        "Keep the inverter, icons, gray background and spacing."
        + KEEP_CASE
    ),
    (1, 0): (
        "This is a light-gray marketing banner: a white hybrid inverter in the center, "
        "an orange rounded panel on the left and a pale-gray rounded panel on the right. "
        "Translate only the overlay text to Russian and keep the same line breaks. "
        "Headline line 1: 'DC COUPLING VS' → 'СВЯЗЬ ПО DC ИЛИ'. "
        "Headline line 2: 'AC COUPLING OF INVERTER' → 'СВЯЗЬ ПО AC ИНВЕРТОРА'. "
        "Left orange panel, two lines: 'DC' stays 'DC'; 'COUPLING' → 'СВЯЗЬ'. "
        "Right panel, three lines: 'AC' stays 'AC'; 'COUPLING OF' → 'СВЯЗЬ'; "
        "'INVERTER' → 'ИНВЕРТОРА'. "
        "Keep DC and AC abbreviations. Do not change the casing line HYBRID SOLAR INVERTER, "
        "the xindun GREEN POWER logo, the display, buttons or CE mark."
        + KEEP_CASE
    ),
    (2, 0): (
        "This is a portrait marketing banner: a log cabin in a forest, solar panels "
        "and two power units in the foreground. Translate only the white two-line headline "
        "to Russian: 'What Is Pay As You Go' → 'Что такое Pay-As-You-Go'; "
        "'Solar Home System?' → 'солнечная система для дома?'. "
        "Keep the cabin, forest, panels, both units and the question mark. "
        "Do not change product casing text such as ENERGY STORAGE SYSTEM or SOLAR GENERATOR."
        + KEEP_CASE
    ),
    (2, 2): (
        "This is a wiring diagram on a white background. Translate only the English labels "
        "around the diagram to Russian. Keep every wire, arrow, icon and the central inverter. "
        "'Solar Panel' → 'Солнечная панель'; 'AC Output' → 'Выход AC'; 'Laptop' → 'Ноутбук'; "
        "'Refrigerator' → 'Холодильник'; 'Air-conditioning' → 'Кондиционер'; "
        "'Hair drier' → 'Фен'; 'Water dispenser' → 'Кулер'; 'AC Input' → 'Вход AC'; "
        "'or' → 'или'; 'Generator' → 'Генератор'; 'DC Output' → 'Выход DC'; "
        "'Lamp' → 'Лампа'; 'Mobile Phone' → 'Телефон'; 'Wireless Earphone' → 'Наушники'. "
        "Do NOT change text printed on the inverter body, including ENERGY STORAGE SYSTEM, "
        "LiFePO4+MPPT+INVERTER, the xindun logo, the display, or side-panel port names. "
        "Do not add or remove appliances. Do not redesign."
    ),
    (2, 4): (
        "This is a wiring diagram on a white background with two solar-generator units. "
        "Translate only the English diagram labels to Russian. Keep wire colors, N and L, "
        "arrows, breakers and every appliance icon. "
        "'INVERTER' → 'ИНВЕРТОР'; 'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'; "
        "'POWER GRID' → 'СЕТЬ'; 'GENERATOR' → 'ГЕНЕРАТОР'; 'or' → 'или'; "
        "'Fan' → 'Вентилятор'; 'Notebook Computer' → 'Ноутбук'; 'Hair Drier' → 'Фен'; "
        "'Electric kettle' → 'Электрочайник'; 'AC LOADS' → 'НАГРУЗКА AC'; "
        "'DC LOADS' → 'НАГРУЗКА DC'. Keep the letters N and L exactly. "
        "Do NOT change SOLAR GENERATOR printed on the casing, the xindun logo, "
        "the display, or port labels on the black panel. Do not redesign."
    ),
    (2, 6): (
        "This is a wiring diagram on a white background with one blue portable unit. "
        "Translate only the labels outside the product to Russian. "
        "'Solar Panels' → 'Солнечные панели'; 'or' → 'или'; "
        "'Adapter Input' → 'Вход адаптера'; 'Mains' → 'Сеть'; "
        "'Mini Fan' → 'Мини-вентилятор'; 'Wireless Earphone' → 'Наушники'; "
        "'Mobile Phone' → 'Телефон'; 'Lamp' → 'Лампа'. "
        "Do NOT change text printed on the blue unit: SOLAR POWER LIGHTING SYSTEM, "
        "POWER, ON/OFF, DC 5V, DC 12V, USB, SOLAR INPUT or ADAPTER INPUT. "
        "Keep the adapter photo, pylons, panel and arrows. Do not redesign."
    ),
    (3, 0): (
        "This is a beige comparison banner: a black inverter on a green panel at left, "
        "a gray VFD on a brown panel at right, and a yellow VS bolt in the middle. "
        "Translate only the overlay text to Russian. Keep two headline lines and the green "
        "color of the second line: 'What Is the Difference Between' → 'В чём разница между'; "
        "'VFD And Inverter?' → 'VFD и инвертором?'. "
        "Bottom-left label 'INVERTER' → 'ИНВЕРТОР'. Keep the bottom-right label 'VFD' as VFD. "
        "Keep the yellow VS. Do not change either product, warning stickers, the display "
        "or the logo."
        + KEEP_CASE
    ),
    (4, 0): (
        "This is a dark marketing banner of several white inverters on black steps. "
        "Translate only the headline. The green badge '2 in 1' → '2 в 1'. "
        "The white words 'Solar Inverter' → 'Солнечный инвертор'. "
        "Keep every inverter, the RGB ring, the steps, the dark background, CE marks "
        "and HYBRID SOLAR INVERTER printed on the casings."
        + KEEP_CASE
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/09/202510091145502608.jpg",
            "alt_ru": "Степень защиты инвертора IP20 IP21 IP54 IP65 IP66",
            "title_ru": "Степень защиты инвертора IP20 IP21 IP54 IP65 IP66",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/09/202510091143529756.jpg",
            "alt_ru": "Инвертор со связью по постоянному и переменному току",
            "title_ru": "Инвертор со связью по постоянному и переменному току",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/09/06/202509061456418096.jpg",
            "alt_ru": "Домашняя солнечная система Pay-As-You-Go",
            "title_ru": "Домашняя солнечная система Pay-As-You-Go",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/11/01/202411011540107215.jpg",
            "alt_ru": "Солнечная система PAYG серии ESS-Li",
            "title_ru": "Солнечная система PAYG серии ESS-Li",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/31/202410310956586221.jpg",
            "alt_ru": "Схема подключения солнечной системы PAYGO",
            "title_ru": "Схема подключения солнечной системы PAYGO",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211052554816.jpg",
            "alt_ru": "Солнечная система ESS с оплатой по мере использования",
            "title_ru": "Солнечная система ESS с оплатой по мере использования",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311726521839.jpg",
            "alt_ru": "Подключение солнечной системы с оплатой по мере использования",
            "title_ru": "Подключение солнечной системы с оплатой по мере использования",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/09/06/202509061505127925.jpg",
            "alt_ru": "Солнечная система PAYGO серии XD-T",
            "title_ru": "Солнечная система PAYGO серии XD-T",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/09/06/202509061506114178.jpg",
            "alt_ru": "Проводка домашней солнечной системы PAYGO",
            "title_ru": "Проводка домашней солнечной системы PAYGO",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/09/06/202509061455511845.jpg",
            "alt_ru": "Домашняя солнечная система PAYGO в работе",
            "title_ru": "Домашняя солнечная система PAYGO в работе",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/30/202508301049129940.jpg",
            "alt_ru": "Разница между VFD и инвертором",
            "title_ru": "Разница между VFD и инвертором",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/30/202508301553448160.jpg",
            "alt_ru": "Солнечный инвертор 2 в 1",
            "title_ru": "Солнечный инвертор 2 в 1",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ru": "Солнечный инвертор HFP 2 в 1",
            "title_ru": "Солнечный инвертор HFP 2 в 1",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141550028678.jpg",
            "alt_ru": "Гибридный солнечный инвертор HFP-S",
            "title_ru": "Гибридный солнечный инвертор HFP-S",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ru": "Солнечный инвертор HFP-C 2 в 1",
            "title_ru": "Солнечный инвертор HFP-C 2 в 1",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ru": "Солнечный инвертор HFP-E",
            "title_ru": "Солнечный инвертор HFP-E",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141552243253.jpg",
            "alt_ru": "Инвертор HP PLUS+ 2 в 1",
            "title_ru": "Инвертор HP PLUS+ 2 в 1",
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
                    **{k: (str(v) if k == "local" else list(v) if k == "orig_wh" else v) for k, v in entry.items()},
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
