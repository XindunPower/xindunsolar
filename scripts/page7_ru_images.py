#!/usr/bin/env python3
"""Prepare page 7 Russian images.

Duomi gpt-image-2 only for English marketing headlines and wiring-diagram labels.
Product studio shots, installation collages, and the factory floor photo are compressed only.
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
PAGE_NUM = 7

WIRE = (
    "This is a wiring diagram. Translate only the English diagram labels to Russian. "
    "Keep every wire, color, arrow, icon, product photo and terminal mark. "
    "Keep electrical symbols exactly: L, N, L1, L2, L3, P1, P2, P3, U, +, −, "
    "and the voltage figures such as 12V, 120V, 240V. "
    "Do NOT change product casing text (HYBRID SOLAR INVERTER, SPLIT PHASE INVERTER, "
    "Low Frequency Inverter, LiFePO4, INVERTER), the xindun logo, CE, ISO, or displays. "
    "Do not redesign."
)
COMMON = (
    " Labels: 'Battery' → 'Аккумулятор'; 'Batteries' → 'Аккумуляторы'; "
    "'Utility Grid' → 'Сеть'; 'Power Grid' → 'Сеть'; 'POWER GRID' → 'Сеть'; "
    "'Loads' → 'Нагрузка'; 'AC Loads' → 'Нагрузка AC'; "
    "'PV Array' → 'Массив PV'; 'Solar Panels' → 'Солнечные панели'; "
    "'SOLAR PANELS' → 'Солнечные панели'; 'Generator' → 'Генератор'; "
    "'OR' → 'ИЛИ'; 'or' → 'или'."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a daylight marketing banner: seven white or black inverters on a lawn, "
        "mountains and rooftop solar behind them. Translate only the headline to Russian: "
        "'Pure Sine Wave' → 'Чистая синусоида'; "
        "'Off Grid Solar Inverter' → 'Автономный солнечный инвертор'. "
        "Keep the red banner shape, products, grass, mountains and panels unchanged. "
        "Do NOT change product casing text, the xindun logo or displays. Do not redesign."
    ),
    (1, 0): (
        "This is a dusk marketing banner: two white inverters on a round podium, a clock, "
        "mountains and solar panels. Translate only the headline to Russian: "
        "'Solar Inverter' → 'Солнечный инвертор'; 'Time Setting' → 'Настройка времени'. "
        "Keep the red block, clock, products, podium and background unchanged. "
        "Do NOT change casing text (SPLIT PHASE INVERTER, HYBRID SOLAR INVERTER), "
        "the xindun logo or displays. Do not redesign."
    ),
    (1, 1): (
        WIRE + COMMON + " Three inverters in one row. This is single-phase parallel wiring. "
        "The grid label reads 'Power Grid'."
    ),
    (1, 2): (
        WIRE + COMMON + " Three inverters. This is split-phase parallel wiring. "
        "The grid label reads 'Power Grid'."
    ),
    (1, 3): (
        WIRE + COMMON + " Three inverters with green, red and blue phase wires. "
        "This is three-phase parallel wiring. The grid label reads 'Power Grid'."
    ),
    (1, 4): (
        WIRE + COMMON + " Keep the top labels P1 and P2. "
        "This is two-phase split-phase parallel wiring. The grid label reads 'Power Grid'."
    ),
    (1, 5): (
        WIRE + COMMON + " Three hybrid inverters. Several 'PV Array' labels. "
        "Grid and loads show N and L. This diagram expands power in parallel."
    ),
    (1, 6): (
        WIRE + COMMON + " Three hybrid inverters. Grid and loads show N, L1, L2 and L3. "
        "This is three-phase parallel output. Keep L1, L2, L3 and N."
    ),
    (2, 0): (
        "This is a pale-blue product banner with four inverters on blocks. "
        "Translate only the headline to Russian: "
        "'Inverter' → 'Инвертор'; 'Split Phase' → 'Расщеплённая фаза'; "
        "'Power Supply' → 'Электроснабжение'. "
        "Keep the green highlight, products and background unchanged. "
        "Do NOT change casing text, the xindun logo or displays. Do not redesign."
    ),
    (2, 1): (
        WIRE + COMMON + " One split-phase inverter. Grid on the left shows L1 N L2 "
        "with 120V and 240V. Loads on the right show L1 N L2. Keep those symbols and voltages."
    ),
    (2, 2): (
        WIRE + COMMON + " Three inverters. This is split-phase parallel wiring. "
        "The grid label reads 'Power Grid'."
    ),
    (2, 3): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'Utility Grid' → 'Сеть'; "
        "'OR' → 'ИЛИ'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'; "
        "'AC OUTPUT' → 'Выход AC'; 'AC Loads' → 'Нагрузка AC'. "
        "Keep 120V, 240V, L1, L2 and N. One blue inverter and a battery below it."
    ),
    (2, 4): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'Utility Grid' → 'Сеть'; "
        "'OR' → 'ИЛИ'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'; "
        "'AC OUTPUT' → 'Выход AC'; 'AC Loads' → 'Нагрузка AC'. "
        "Keep 12V, 120V, 240V, L1, L2 and N. One white tower inverter."
    ),
    (3, 0): (
        "This is a daylight lineup banner of six white hybrid inverters in front of a house "
        "with rooftop solar. Translate only the headline to Russian: "
        "'Sun Hybrid Inverter' → 'Гибридный солнечный инвертор'. "
        "Keep every product, the house, panels and sky unchanged. "
        "Do NOT change casing text, the xindun logo, the word INVERTER on the round display, "
        "or CE marks. Do not redesign."
    ),
    (3, 1): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'Utility Grid' → 'Сеть'; "
        "'OR' → 'ИЛИ'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'; "
        "'Uninterrupted Power Supply(Main output)' → 'Бесперебойное питание (основной выход)'; "
        "'Uninterrupted Power Supply(Second output)' → 'Бесперебойное питание (второй выход)'. "
        "One white inverter with a round green display."
    ),
    (3, 2): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'Utility Grid' → 'Сеть'; "
        "'OR' → 'ИЛИ'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'; "
        "'Uninterrupted Power Supply(Main output)' → 'Бесперебойное питание (основной выход)'; "
        "'Uninterrupted Power Supply(Second output)' → 'Бесперебойное питание (второй выход)'. "
        "One white inverter with an RGB ring."
    ),
    (3, 3): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'Utility Grid' → 'Сеть'; "
        "'OR' → 'ИЛИ'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'; "
        "'Uninterrupted Power Supply(Main output)' → 'Бесперебойное питание (основной выход)'; "
        "'Uninterrupted Power Supply(Second output)' → 'Бесперебойное питание (второй выход)'. "
        "One white inverter with a detachable-style panel and a green INVERTER badge. "
        "Keep the badge word only if it is printed on the product; do not redesign the badge."
    ),
    (3, 4): (
        WIRE + " Labels: 'Unit 1' → 'Блок 1'; 'Unit 2' → 'Блок 2'; 'Unit 3' → 'Блок 3'; "
        "'Battery' → 'Аккумулятор'; 'Utility Grid' → 'Сеть'; 'Loads' → 'Нагрузка'. "
        "Keep N and L. Three inverters in one row. Single-phase parallel output."
    ),
    (3, 5): (
        WIRE + " Labels: 'Battery' → 'Аккумулятор'; 'Utility Grid' → 'Сеть'; 'Loads' → 'Нагрузка'. "
        "Keep the top labels P1, P2 and P3. Nine inverters. Three-phase parallel output."
    ),
    (3, 6): (
        WIRE + COMMON + " Three hybrid inverters with a black-and-red panel. "
        "Grid and loads show N and L. Several 'PV Array' labels. Parallel power expansion."
    ),
    (3, 7): (
        WIRE + COMMON + " Three hybrid inverters. Grid and loads show L1, N and L2. "
        "Split-phase parallel output. Keep L1, L2 and N."
    ),
    (3, 8): (
        WIRE + COMMON + " Three hybrid inverters. Grid and loads show L1, L2, L3 and N. "
        "Three-phase parallel output. Keep L1, L2, L3 and N."
    ),
    (4, 0): (
        "This is a factory marketing banner: three tall inverters, white, yellow and black, "
        "standing in a workshop. Translate only the headline to Russian, keeping 25 кВт large: "
        "'What Can a 25KW Inverter Run?' → 'Что может питать инвертор на 25 кВт?'. "
        "Keep the three products, the workshop, cranes and floor unchanged. "
        "Do NOT change casing text (Low Frequency Inverter, Pure Sine Wave), "
        "the xindun logo or displays. Do not redesign."
    ),
    (4, 1): (
        WIRE + " Labels: 'Power Grid' → 'Сеть'; 'or' → 'или'; 'Generator' → 'Генератор'; "
        "'Solar Panels' → 'Солнечные панели'; 'Solar Controller' → 'Солнечный контроллер'; "
        "'RS232 (Optional)' → 'RS232 (опция)'; 'RS485 (Optional)' → 'RS485 (опция)'; "
        "'Ground Line' → 'Заземление'; 'Batteries' → 'Аккумуляторы'; "
        "'Rice cooker' → 'Рисоварка'; 'Water dispenser' → 'Кулер'; "
        "'Electromagnetic furnace' → 'Индукционная плита'; 'Refrigerator' → 'Холодильник'; "
        "'AIR CONDITIONER' → 'КОНДИЦИОНЕР'. "
        "Keep RS232 and RS485. Rear view of a white tower inverter."
    ),
    (4, 2): (
        WIRE + " Labels: 'Solar Panels' → 'Солнечные панели'; 'AC Input' → 'Вход AC'; "
        "'or' → 'или'; 'Generator' → 'Генератор'; 'Battery' → 'Аккумулятор'; "
        "'AC Output' → 'Выход AC'; 'Laptop' → 'Ноутбук'; 'Printer' → 'Принтер'; "
        "'TV' → 'Телевизор'; 'Fans' → 'Вентиляторы'; 'Water pump' → 'Насос'. "
        "One white low-frequency inverter in the center."
    ),
    (4, 3): (
        WIRE + " Labels: 'INVERTER' → 'ИНВЕРТОР'; 'SOLAR PANELS' → 'Солнечные панели'; "
        "'PV COMBINER' → 'Сумматор PV'; 'SOLAR CONTROLLER' → 'Солнечный контроллер'; "
        "'BATTERIES' → 'Аккумуляторы'; '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'; "
        "'A Phase' → 'Фаза A'; 'B Phase' → 'Фаза B'; 'C Phase' → 'Фаза C'; "
        "'3-PHASE LOADS' → 'Нагрузка 3 фазы'; '1-PHASE LOADS' → 'Нагрузка 1 фазы'; "
        "'POWER GRID' → 'Сеть'; 'Earth Wire (GND)' → 'Заземление (GND)'; "
        "'BREAKER' → 'Автомат'. "
        "Keep N, GND, 12V and 200Ah. Black cabinet inverter. Do not change terminal silk-screen inside the chassis."
    ),
    (4, 5): (
        "This is a company photo collage: reception desk above, three small photos below "
        "with green caption bars. Translate only those three green captions to Russian: "
        "'Office' → 'Офис'; 'Laboratory' → 'Лаборатория'; 'Exhibition hall' → 'Выставочный зал'. "
        "Do NOT change the wall company name xindun GREEN POWER, the Chinese company name, "
        "certificates, people, furniture, plants, or the building. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091120331497.jpg", "alt_ru": "Автономный солнечный инвертор чистой синусоиды", "title_ru": "Автономный солнечный инвертор чистой синусоиды"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png", "alt_ru": "Инвертор чистой синусоиды HFP", "title_ru": "Инвертор чистой синусоиды HFP"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png", "alt_ru": "Автономный солнечный инвертор HFP-C", "title_ru": "Автономный солнечный инвертор HFP-C"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg", "alt_ru": "Инвертор чистой синусоиды HU", "title_ru": "Инвертор чистой синусоиды HU"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg", "alt_ru": "Автономный инвертор HP PLUS+", "title_ru": "Автономный инвертор HP PLUS+"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125237036.jpg", "alt_ru": "Автономный инвертор LU", "title_ru": "Автономный инвертор LU"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125487765.jpg", "alt_ru": "Трёхфазный инвертор чистой синусоиды", "title_ru": "Трёхфазный инвертор чистой синусоиды"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091126518485.jpg", "alt_ru": "Автономный солнечный генератор ESS-Li", "title_ru": "Автономный солнечный генератор ESS-Li"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/15/202511150928484456.jpg", "alt_ru": "Настройка времени солнечного инвертора", "title_ru": "Настройка времени солнечного инвертора"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141154031704.jpg", "alt_ru": "Однофазная параллельная схема солнечного инвертора", "title_ru": "Однофазная параллельная схема солнечного инвертора"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155069284.jpg", "alt_ru": "Параллельная схема с расщеплённой фазой", "title_ru": "Параллельная схема с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155496791.jpg", "alt_ru": "Трёхфазная параллельная схема инвертора", "title_ru": "Трёхфазная параллельная схема инвертора"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141157382346.jpg", "alt_ru": "Двухфазная параллельная схема с расщеплением", "title_ru": "Двухфазная параллельная схема с расщеплением"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141159513423.jpg", "alt_ru": "Параллельное расширение мощности инвертора", "title_ru": "Параллельное расширение мощности инвертора"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141200562922.jpg", "alt_ru": "Параллельный трёхфазный выход солнечного инвертора", "title_ru": "Параллельный трёхфазный выход солнечного инвертора"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/20251114142133mHRDbI.jpg", "alt_ru": "Электроснабжение с расщеплённой фазой", "title_ru": "Электроснабжение с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141426036849.jpg", "alt_ru": "Схема инвертора LU с расщеплённой фазой", "title_ru": "Схема инвертора LU с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155069284.jpg", "alt_ru": "Гибридный инвертор HU с расщеплённой фазой", "title_ru": "Гибридный инвертор HU с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141427125780.jpg", "alt_ru": "Схема инвертора LS с расщеплённой фазой", "title_ru": "Схема инвертора LS с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141432533866.jpg", "alt_ru": "Схема инвертора WF с расщеплённой фазой", "title_ru": "Схема инвертора WF с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141433559083.jpg", "alt_ru": "Примеры электроснабжения с расщеплённой фазой", "title_ru": "Примеры электроснабжения с расщеплённой фазой"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301436325219.jpg", "alt_ru": "Гибридный солнечный инвертор", "title_ru": "Гибридный солнечный инвертор"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301437478088.jpg", "alt_ru": "Солнечный инвертор HFP-S", "title_ru": "Солнечный инвертор HFP-S"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301438298106.jpg", "alt_ru": "Солнечный инвертор HFP-C", "title_ru": "Солнечный инвертор HFP-C"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301439085755.jpg", "alt_ru": "Гибридный солнечный инвертор HFP-E", "title_ru": "Гибридный солнечный инвертор HFP-E"},
        {"src": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151138082598.jpg", "alt_ru": "Параллельная работа солнечного инвертора", "title_ru": "Параллельная работа солнечного инвертора"},
        {"src": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151159558052.jpg", "alt_ru": "Трёхфазный выход гибридного инвертора", "title_ru": "Трёхфазный выход гибридного инвертора"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301453378424.jpg", "alt_ru": "Параллельное расширение мощности", "title_ru": "Параллельное расширение мощности"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301453241476.jpg", "alt_ru": "Выход с расщеплённой фазой", "title_ru": "Выход с расщеплённой фазой"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301452362924.jpg", "alt_ru": "Трёхфазный параллельный выход", "title_ru": "Трёхфазный параллельный выход"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301455232457.jpg", "alt_ru": "Примеры гибридного солнечного инвертора", "title_ru": "Примеры гибридного солнечного инвертора"},
    ],
    [
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301415354090.jpg", "alt_ru": "Солнечный инвертор 25 кВт", "title_ru": "Солнечный инвертор 25 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301418405169.jpg", "alt_ru": "Инвертор WD 25 кВт", "title_ru": "Инвертор WD 25 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311109218818.jpg", "alt_ru": "Солнечный инвертор WF 25 кВт", "title_ru": "Солнечный инвертор WF 25 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301419552617.jpg", "alt_ru": "Солнечный инвертор HDSX 25 кВт", "title_ru": "Солнечный инвертор HDSX 25 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301420539336.jpg", "alt_ru": "Применение инвертора 25 кВт", "title_ru": "Применение инвертора 25 кВт"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301421321541.jpg", "alt_ru": "Производитель инверторов Xindun", "title_ru": "Производитель инверторов Xindun"},
        {"src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301422247905.jpg", "alt_ru": "Цех зарядных инверторов", "title_ru": "Цех зарядных инверторов"},
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
