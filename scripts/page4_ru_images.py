#!/usr/bin/env python3
"""Prepare page 4 Russian images.

Duomi gpt-image-2 only for English marketing banners and diagram callouts.
Studio product shots (casing text, logos, model numbers) are compressed and renamed only.
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
PAGE_NUM = 4

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a blue-sky marketing banner: a solar panel and sun on the left, a tall white "
        "all-in-one cabinet in the center, a battery, a light bulb, appliances, a grid tower and a generator. "
        "Translate only the English overlay text to Russian: "
        "'What Is All In One Hybrid Solar Inverter?' → 'Что такое моноблочный гибридный солнечный инвертор?'; "
        "'Inverter+Solar Controller+Battery in One System' → 'Инвертор + солнечный контроллер + аккумулятор в одной системе'; "
        "'Grid' → 'Сеть'; "
        "'Generator' → 'Генератор'. "
        "Keep the question mark. Keep the sun, clouds, grass, arrows, panel, cabinet, battery, appliances, tower and generator unchanged. "
        "Do NOT change product casing text (ENERGY STORAGE SYSTEM and any small print on the cabinet), "
        "the xindun logo, CE marks or the display. Do not add or remove objects. Do not redesign the poster. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original text area."
    ),
    (0, 2): (
        "This is a two-part technical diagram of one white-and-black cabinet, front view on top and rear view below, "
        "with green leader lines and English callout labels. Translate only those callout labels to Russian: "
        "'LED Indicator' → 'Светодиодный индикатор'; "
        "'LCD Display' → 'Дисплей LCD'; "
        "'12VDC Output' → 'Выход 12 В DC'; "
        "'USB 5VDC Output' → 'Выход USB 5 В DC'; "
        "'AC Output Socket' → 'Розетка выхода AC'; "
        "'DC Output Switch' → 'Выключатель выхода DC'; "
        "'AC INPUT/OUTPUT' and 'SOLAR INPUT' and 'Terminal Block' → 'Клеммная колодка входа/выхода AC и входа PV'; "
        "'AC Input / Output Switch' → 'Выключатель входа/выхода AC'; "
        "'Battery Switch' → 'Выключатель аккумулятора'; "
        "'Spare Battery' → 'Запасной аккумулятор'; "
        "'RS232 Communication Interface' → 'Интерфейс связи RS232'; "
        "'RS485 Communication Interface' → 'Интерфейс связи RS485'. "
        "Keep both product views, green lines, fan, sockets and switches in the same places. "
        "Do NOT change the xindun GREEN POWER logo, silkscreen printed on the hardware, or model markings. "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so each label stays beside its original leader line."
    ),
    (0, 3): (
        "This is a cutaway product diagram: a white cabinet with a blue battery and circuit boards visible, "
        "and three English callouts on the right. Translate only the callout text to Russian: "
        "'Solar Controller' → 'Солнечный контроллер'; "
        "'Built-in MPPT' → 'Встроенный MPPT'; "
        "'Inverter' → 'Инвертор'; "
        "'Pure Sine Wave' → 'Чистая синусоида'; "
        "'LiFePO4 Battery' → 'Аккумулятор LiFePO4'; "
        "'Longer Lifespan' → 'Больший срок службы'. "
        "Keep the cabinet, cutaway, boards, blue battery and green leader lines unchanged. "
        "Do NOT change casing text (ENERGY STORAGE SYSTEM, LiFePO4+MPPT+INVERTER), "
        "the xindun GREEN POWER logo, or the display. Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays in the original callout area."
    ),
    (0, 4): (
        "This is a three-view technical diagram inside two green frames: front panel on top, "
        "rear panel and side panel below, with green leader lines and English callouts. "
        "Translate only the callout labels to Russian: "
        "'LCD Display' → 'Дисплей LCD'; "
        "'Function keys' → 'Функциональные кнопки'; "
        "'Up keys' → 'Кнопки «вверх»'; "
        "'Down keys' → 'Кнопки «вниз»'; "
        "'Inverter Switch' → 'Выключатель инвертора'; "
        "'Handle' → 'Ручка'; "
        "'Battery Switch' → 'Выключатель аккумулятора'; "
        "'DC Output Switch' → 'Выключатель выхода DC'; "
        "'WiFi/GPRS' → 'WiFi/GPRS'; "
        "'RS485' → 'RS485'. "
        "Keep all three product views, frames and leader lines unchanged. "
        "Do NOT change the xindun GREEN POWER logo, button silkscreen (FUNCTION, UP, DOWN), "
        "breaker text (BATTERY ON/OFF) or port markings printed on the hardware. "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so each label stays beside its leader line."
    ),
    (0, 5): (
        "This is a rear-panel diagram titled Multiple Output, with a magnified inset of the ports, "
        "four icons along the bottom, and a full rear view on the right. Translate only the overlay headline and icon captions to Russian: "
        "'Multiple Output' → 'Несколько выходов'; "
        "'4*DC 12V 、 4*USB 、 AC Output Socket and Terminal Strip' → '4×DC 12 В, 4×USB, розетка выхода AC и клеммная колодка'; "
        "the four bottom captions 'DC OUTPUT' → 'Выход DC', 'USB' → 'USB', "
        "'AC Output Socket' → 'Розетка выхода AC', 'Terminal Strip' → 'Клеммная колодка'. "
        "Keep the product, magnified inset, green outline, icons and connector photo unchanged. "
        "Do NOT change silkscreen printed on the panel (USB 5V, 12V, ON/OFF, AC OUTPUT, AC INPUT, N, L, SOLAR, BATTERY ON, CAUTION). "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original headline and caption areas."
    ),
    (1, 0): (
        "This is a green infographic banner split into a left power-sources scene and a right parallel-system scene. "
        "Translate only the English overlay text to Russian, keeping the same boxes and colors: "
        "'Can Parallel Hybrid Inverter Use Batteryless Operation Mode?' → 'Может ли параллельный гибридный инвертор работать без аккумулятора?'; "
        "'POWER SOURCES' → 'ИСТОЧНИКИ ПИТАНИЯ'; "
        "'Solar Power' → 'Солнечная энергия'; "
        "'Mains Power' → 'Сеть'; "
        "'NO BATTERY REQUIRED' → 'АККУМУЛЯТОР НЕ НУЖЕН'; "
        "'RUNS WITHOUT BATTERY' → 'РАБОТАЕТ БЕЗ АККУМУЛЯТОРА'; "
        "'PARALLEL SYSTEM' → 'ПАРАЛЛЕЛЬНАЯ СИСТЕМА'; "
        "'BATTERY REQUIRED FOR PARALLEL OPERATION' → 'ДЛЯ ПАРАЛЛЕЛЬНОЙ РАБОТЫ НУЖЕН АККУМУЛЯТОР'; "
        "'NO BATTERYLESS MODE' → 'РЕЖИМ БЕЗ АККУМУЛЯТОРА НЕДОСТУПЕН'; "
        "'NO BACKUP POWER' → 'НЕТ РЕЗЕРВНОГО ПИТАНИЯ'; "
        "'NO ENERGY STORAGE' → 'НЕТ НАКОПЛЕНИЯ ЭНЕРГИИ'; "
        "'GRID FAILURE' → 'ОТКАЗ СЕТИ'; "
        "'DIRECT POWER USE ONLY' → 'ТОЛЬКО ПРЯМОЕ ПОТРЕБЛЕНИЕ'. "
        "Keep the panel, sun, towers, houses, meter, check mark, red arrow and all three inverters unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER), the xindun logo, CE marks or displays. "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so every label stays inside its original box."
    ),
    (2, 0): (
        "This is a green marketing diagram with one white inverter in the center and four colored callout cards. "
        "Translate only the English overlay text to Russian: "
        "'Parallel Hybrid Inverter' → 'Параллельный гибридный инвертор'; "
        "'Fault Codes & Protection Functions' → 'Коды неисправностей и функции защиты'; "
        "'Battery Fault Codes' → 'Коды неисправностей аккумулятора'; "
        "'Battery Undervoltage' → 'Пониженное напряжение аккумулятора'; "
        "'Overcurrent' → 'Сверхток'; "
        "'Connection Error' → 'Ошибка подключения'; "
        "'Solar Protection' → 'Защита солнечного входа'; "
        "'Overvoltage Shield' → 'Защита от перенапряжения'; "
        "'Current Limiting' → 'Ограничение тока'; "
        "'Reverse Charging Protection' → 'Защита от обратного заряда'; "
        "'Inverter Circuit Protection' → 'Защита цепи инвертора'; "
        "'Overload Safety' → 'Защита от перегрузки'; "
        "'Short Circuit Protection' → 'Защита от короткого замыкания'; "
        "'Overheat Defense' → 'Защита от перегрева'; "
        "'Output Protection' → 'Защита выхода'; "
        "'Short Circuit Guard' → 'Защита от КЗ'; "
        "'Overload Control' → 'Контроль перегрузки'; "
        "'AC Reverse Protection' → 'Защита от обратного тока AC'; "
        "'FAULT ALARM' → 'АВАРИЙНЫЙ СИГНАЛ'. "
        "Keep the inverter, sun, panel, alarm lamp, checklist, magnifier and card colors unchanged. "
        "Do NOT change the xindun logo or HYBRID SOLAR INVERTER printed on the casing. "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so every line stays inside its original card."
    ),
    (3, 0): (
        "This is a sunset marketing banner with autumn leaves, solar panels, a house, a power tower and two white inverters. "
        "Translate only the English headline and the two bottom captions to Russian, keeping the stacked headline: "
        "'Why the Best' → 'Почему лучший'; "
        "'Split Phase' → 'с расщеплённой фазой'; "
        "'Solar Inverter' → 'солнечный инвертор'; "
        "'Matters for Solar System?' → 'важен для солнечной системы?'; "
        "'Day/Night Smart Scheduling' → 'Умное расписание день/ночь'; "
        "'Up to 6x Parallel Connection' → 'До 6 аппаратов параллельно'. "
        "Keep the question mark, the gold emphasis on the middle line, leaves, sun, panels, house, tower and both products. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), the xindun logo, CE marks or displays. "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so it stays inside the original headline and footer bands."
    ),
    (4, 0): (
        "This is a three-column diagram under a green headline: too many panels, a proper ratio, and too few panels, "
        "each with one white inverter. Translate only the English overlay text to Russian: "
        "'What Happens If You Connect Too Many Solar Panels to Inverter?' → "
        "'Что будет, если подключить к инвертору слишком много солнечных панелей?'; "
        "'Too Many' → 'Слишком много'; "
        "'Proper Ratio' → 'Правильное соотношение'; "
        "'Too Few' → 'Слишком мало'; "
        "'Clipping' → 'Ограничение мощности'; "
        "'Power Wasted' → 'Потери мощности'; "
        "'Best Efficiency' → 'Лучший КПД'; "
        "'Grid Support' → 'Поддержка от сети'; "
        "'Battery Backup' → 'Резерв от аккумулятора'. "
        "Keep the question mark, red X marks, green check, panels, three inverters, warning icon and column dividers. "
        "Do NOT change text on the product displays, the xindun logo or CE marks. "
        "Do not add or remove objects. Do not redesign. "
        "If Russian is longer, use a slightly smaller font so every label stays inside its original area."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161544446666.jpg",
            "alt_ru": "Моноблочный гибридный инвертор",
            "title_ru": "Моноблочный гибридный инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161545443780.jpg",
            "alt_ru": "Моноблочный инвертор",
            "title_ru": "Моноблочный инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161546138528.jpg",
            "alt_ru": "Моноблочный гибридный солнечный инвертор",
            "title_ru": "Моноблочный гибридный солнечный инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161547032380.jpg",
            "alt_ru": "Солнечный инвертор всё в одном",
            "title_ru": "Солнечный инвертор всё в одном",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161547371441.jpg",
            "alt_ru": "Гибридный инвертор",
            "title_ru": "Гибридный инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161548072528.jpg",
            "alt_ru": "Инвертор всё в одном",
            "title_ru": "Инвертор всё в одном",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/13/202601131758599588.jpg",
            "alt_ru": "Параллельный гибридный инвертор",
            "title_ru": "Параллельный гибридный инвертор",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ru": "Гибридный инвертор HFP без аккумулятора",
            "title_ru": "Гибридный инвертор HFP без аккумулятора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ru": "Гибридный инвертор HFP-C без аккумулятора",
            "title_ru": "Гибридный инвертор HFP-C без аккумулятора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141550028678.jpg",
            "alt_ru": "Гибридный инвертор HFP-S",
            "title_ru": "Гибридный инвертор HFP-S",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ru": "Инвертор HFP-E без аккумулятора",
            "title_ru": "Инвертор HFP-E без аккумулятора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg",
            "alt_ru": "Параллельный гибридный инвертор HU",
            "title_ru": "Параллельный гибридный инвертор HU",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg",
            "alt_ru": "Параллельный гибридный инвертор HP Plus+",
            "title_ru": "Параллельный гибридный инвертор HP Plus+",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/13/20260113173404LoDdKT.jpg",
            "alt_ru": "Неисправности и защита параллельного гибридного инвертора",
            "title_ru": "Неисправности и защита параллельного гибридного инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg",
            "alt_ru": "Неисправность инвертора",
            "title_ru": "Неисправность инвертора",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg",
            "alt_ru": "Защита инвертора",
            "title_ru": "Защита инвертора",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/27/202512271351579370.jpg",
            "alt_ru": "Лучший инвертор с расщеплённой фазой",
            "title_ru": "Лучший инвертор с расщеплённой фазой",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/26/202512261546573452.jpg",
            "alt_ru": "Солнечные панели и инвертор",
            "title_ru": "Солнечные панели и инвертор",
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
