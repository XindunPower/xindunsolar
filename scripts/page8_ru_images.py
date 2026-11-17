#!/usr/bin/env python3
"""Prepare page 8 Russian images.

Duomi gpt-image-2 only for English marketing headlines and wiring-diagram labels.
Product studio shots, system collages, and the house installation photo are compressed only.
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
PAGE_NUM = 8

WIRE = (
    "This is a wiring diagram. Translate only the English diagram labels to Russian. "
    "Keep every wire, color, arrow, icon, product photo and terminal mark. "
    "Keep electrical symbols exactly: L, N, and any voltage figures. "
    "Do NOT change product casing text (ENERGY STORAGE SYSTEM, SOLAR GENERATOR, "
    "Low Frequency PV Inverter, LiFePO4, HYBRID SOLAR INVERTER, INVERTER), "
    "the xindun logo, CE, ISO, or displays. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a pale studio marketing banner: four inverter units on white podiums. "
        "Translate only the headline to Russian: "
        "'Pure Sine Wave' → 'Чистая синусоида'; "
        "'Combined Inverter & Charger' → 'Инвертор и зарядное устройство'. "
        "Keep the two-line layout, products, podiums and background unchanged. "
        "Do NOT change casing text (ENERGY STORAGE SYSTEM, SOLAR GENERATOR), "
        "the xindun logo or displays. Do not redesign."
    ),
    (0, 1): (
        WIRE
        + " One white low-frequency inverter in the center, four panels above, a battery below, "
        "a generator and grid at lower left, appliances at the right. "
        "Labels: 'Solar Panels' → 'Солнечные панели'; 'AC Output' → 'Выход AC'; "
        "'Refrigerator' → 'Холодильник'; 'Fan heater' → 'Тепловентилятор'; "
        "'Air conditioner' → 'Кондиционер'; 'Heater' → 'Обогреватель'; "
        "'Percussion drill' → 'Перфоратор'; 'AC Input' → 'Вход AC'; "
        "'or' → 'или'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'."
    ),
    (0, 2): (
        WIRE
        + " One blue wall inverter, panels at upper left, generator and grid at lower left, "
        "four batteries below, five loads on the right. "
        "Labels: 'SOLAR PANELS' → 'Солнечные панели'; 'AC INPUT' → 'Вход AC'; "
        "'Generator' → 'Генератор'; 'AC OUTPUT' → 'Выход AC'; "
        "'LAPTOP' → 'Ноутбук'; 'LAMP' → 'Лампа'; 'PRINTER' → 'Принтер'; "
        "'TV' → 'Телевизор'; 'FAN' → 'Вентилятор'; 'BATTERIES' → 'Аккумуляторы'."
    ),
    (0, 3): (
        WIRE
        + " One tall white energy-storage unit. Panel at upper left, generator and grid at lower left, "
        "AC loads on the right, DC loads along the bottom. "
        "Labels: 'Solar Panel' → 'Солнечная панель'; 'AC Output' → 'Выход AC'; "
        "'Laptop' → 'Ноутбук'; 'Refrigerator' → 'Холодильник'; "
        "'Air-conditioning' → 'Кондиционер'; 'Hair drier' → 'Фен'; "
        "'Water dispenser' → 'Кулер'; 'AC Input' → 'Вход AC'; 'or' → 'или'; "
        "'Generator' → 'Генератор'; 'DC Output' → 'Выход DC'; 'Lamp' → 'Лампа'; "
        "'Mobile Phone' → 'Телефон'; 'Wireless Earphone' → 'Наушники'."
    ),
    (0, 4): (
        WIRE
        + " Two tower units on the right, panels at upper left, grid and generator at mid left, "
        "a boxed row of AC loads and a small box of DC loads. Keep the letters N and L on the wires. "
        "Labels: 'INVERTER' → 'Инвертор'; 'SOLAR PANELS' → 'Солнечные панели'; "
        "'or' → 'или'; 'POWER GRID' → 'Сеть'; 'GENERATOR' → 'Генератор'; "
        "'Fan' → 'Вентилятор'; 'Notebook Computer' → 'Ноутбук'; "
        "'Hair Drier' → 'Фен'; 'Electric kettle' → 'Электрочайник'; "
        "'AC LOADS' → 'Нагрузка AC'; 'DC LOADS' → 'Нагрузка DC'."
    ),
    (1, 0): (
        "This is a daylight marketing banner: two solar panels, an arrow, and one white inverter "
        "in front of a house with rooftop solar. Translate only the headline to Russian: "
        "'Solar Panel Direct To Inverter' → 'Солнечная панель напрямую к инвертору'. "
        "Keep panels, arrow, inverter, house and sky unchanged. "
        "Do NOT change casing text (SPLIT PHASE INVERTER), the xindun logo or the display. "
        "Do not redesign."
    ),
    (2, 0): (
        "This is a pale-blue marketing banner: a closed white inverter and an open chassis on a podium. "
        "Translate only the headline to Russian: "
        "'Solar Charge Controller' → 'Контроллер заряда'; "
        "'Inverter Combination' → 'и инвертор'. "
        "Keep the letters MPPT on the blue badge exactly. "
        "Keep products, podium and background unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER), the xindun logo, CE or the display. "
        "Do not redesign."
    ),
    (3, 0): (
        "This is a diagram banner inside a white rounded card: a solar panel, a small controller, "
        "a battery and a tall inverter, with black arrows. Translate only the overlay labels to Russian: "
        "'How Does Solar Panel to Battery' → 'Как работают панель, аккумулятор'; "
        "'to Inverter Work?' → 'и инвертор?'; "
        "'Solar Controller' → 'Солнечный контроллер'; "
        "'Solar Panels' → 'Солнечные панели'; "
        "'Battery' → 'Аккумулятор'; "
        "'Solar Inverter' → 'Солнечный инвертор'. "
        "Keep arrows, products, house and sky unchanged. "
        "Do NOT change casing text (LiFePO4, Low Frequency), the xindun logo, CE or displays. "
        "Do not redesign."
    ),
    (4, 0): (
        "This is a pale studio marketing banner: five white inverters on blocks and a round podium. "
        "Translate only the headline and the green badge to Russian: "
        "'Inverter Solar To 220 Volts' → 'Инвертор: солнце в 220 вольт'; "
        "'Without Battery' → 'Без аккумулятора'. "
        "Keep the green badge shape, products, spheres, pyramid and background unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, the word INVERTER on the round button), "
        "the xindun logo, CE or displays. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/29/20251029110530nAzTrq.jpg",
            "alt_ru": "Чистая синусоида, инвертор и зарядное устройство",
            "title_ru": "Чистая синусоида, инвертор и зарядное устройство",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2023/11/25/20231125171345fMB3JT.jpg",
            "alt_ru": "Инвертор-зарядное устройство DF с синусоидой",
            "title_ru": "Инвертор-зарядное устройство DF с синусоидой",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/01/20/202501201454429424.jpg",
            "alt_ru": "Инвертор-зарядное устройство LS",
            "title_ru": "Инвертор-зарядное устройство LS",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/03/19/20240319180514Fw1B02.jpg",
            "alt_ru": "Инвертор-зарядное устройство ESS-Li с чистой синусоидой",
            "title_ru": "Инвертор-зарядное устройство ESS-Li с чистой синусоидой",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311726521839.jpg",
            "alt_ru": "Инвертор-зарядное устройство ESS с чистой синусоидой",
            "title_ru": "Инвертор-зарядное устройство ESS с чистой синусоидой",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241506246986.jpg",
            "alt_ru": "Солнечная панель напрямую к инвертору",
            "title_ru": "Солнечная панель напрямую к инвертору",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241448493461.jpg",
            "alt_ru": "Комбинация солнечного контроллера заряда и инвертора",
            "title_ru": "Комбинация солнечного контроллера заряда и инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151404306156.jpg",
            "alt_ru": "Комбинация HU: контроллер заряда и инвертор",
            "title_ru": "Комбинация HU: контроллер заряда и инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg",
            "alt_ru": "Солнечный инвертор HFP с контроллером заряда",
            "title_ru": "Солнечный инвертор HFP с контроллером заряда",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241453376522.jpg",
            "alt_ru": "Инвертор HFP-S с солнечным контроллером заряда",
            "title_ru": "Инвертор HFP-S с солнечным контроллером заряда",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151501334463.jpg",
            "alt_ru": "Комбинация контроллера и инвертора HFP-C",
            "title_ru": "Комбинация контроллера и инвертора HFP-C",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151502199748.jpg",
            "alt_ru": "Солнечный инвертор HFP-E с контроллером",
            "title_ru": "Солнечный инвертор HFP-E с контроллером",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg",
            "alt_ru": "Комбинация инвертора HP PLUS+ и контроллера заряда",
            "title_ru": "Комбинация инвертора HP PLUS+ и контроллера заряда",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/20251022162327Mp17mX.jpg",
            "alt_ru": "Солнечная панель, аккумулятор и инвертор",
            "title_ru": "Солнечная панель, аккумулятор и инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221626318952.jpg",
            "alt_ru": "Система HFP: панель, аккумулятор, инвертор",
            "title_ru": "Система HFP: панель, аккумулятор, инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221627174500.jpg",
            "alt_ru": "Система HDSX: панель, аккумулятор, инвертор",
            "title_ru": "Система HDSX: панель, аккумулятор, инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221628024529.jpg",
            "alt_ru": "Солнечная инверторная система WF",
            "title_ru": "Солнечная инверторная система WF",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221628358086.jpg",
            "alt_ru": "Моноблочная солнечная станция ESS",
            "title_ru": "Моноблочная солнечная станция ESS",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221629169116.jpg",
            "alt_ru": "Солнечная станция ESS-Li",
            "title_ru": "Солнечная станция ESS-Li",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241514554488.jpg",
            "alt_ru": "Солнечная энергия в 220 вольт без аккумулятора",
            "title_ru": "Солнечная энергия в 220 вольт без аккумулятора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241516254008.jpg",
            "alt_ru": "Применение преобразования солнца в 220 вольт",
            "title_ru": "Применение преобразования солнца в 220 вольт",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141552243253.jpg",
            "alt_ru": "Солнечный инвертор без аккумулятора",
            "title_ru": "Солнечный инвертор без аккумулятора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ru": "Инвертор без аккумулятора",
            "title_ru": "Инвертор без аккумулятора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141550028678.jpg",
            "alt_ru": "Гибридный инвертор без аккумулятора",
            "title_ru": "Гибридный инвертор без аккумулятора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ru": "Инвертор: солнце в 220 вольт без аккумулятора",
            "title_ru": "Инвертор: солнце в 220 вольт без аккумулятора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ru": "Гибридный солнечный инвертор без аккумулятора",
            "title_ru": "Гибридный солнечный инвертор без аккумулятора",
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
                method_ok = stored == expected or (
                    need_duomi and stored == "duomi-fallback-original"
                )
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
