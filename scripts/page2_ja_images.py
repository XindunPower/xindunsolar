#!/usr/bin/env python3
"""Prepare page 2 Japanese images.

Duomi gpt-image-2 only for English marketing/diagram overlays.
The SHS install collage is a field photo and is compressed and renamed only.
Outputs stay in output/duomi/ja/ so they do not collide with the Russian task.
Marketing edits that fail layout checks are discarded and retried.
They are not replaced by drawing text onto the original.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from page1_ja_images import (  # noqa: E402
    OUT,
    assert_ja_progress_current,
    compress_only,
    run_duomi,
    size_for,
    unique_stem,
)

UA = "Mozilla/5.0 (compatible; XindunJapaneseBot/1.0)"
PAGE_NUM = 2

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a daylight marketing banner: solar panel and white hybrid inverter on the left, "
        "a green shield in the center, a white lithium battery on the right, jungle background. "
        "Translate only the English overlay headline and the three circular badge labels to Japanese, "
        "keeping the same two-line headline layout and short badge labels: "
        "'How to Prevent' → 'インバーターの'; "
        "'INVERTER DAMAGE?' → '損傷を防ぐには？'; "
        "'Overvoltage' → '過電圧'; "
        "'Overcurrent' → '過電流'; "
        "'Load Surge' → '負荷急変'. "
        "Keep the question mark, lightning icon, gauge, pump icon, shield, products, solar panel, and jungle. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo, CE marks, or model markings. Do not add or remove objects. Do not redesign the poster."
    ),
    (1, 0): (
        "This is a dusk-to-night marketing banner with two white inverters, a clock, a battery gauge, "
        "a light bulb, solar panels, houses, and power lines. "
        "Translate only the English overlay headline and the two speech-bubble labels to Japanese, "
        "keeping the two-line headline and the short bubble labels: "
        "'Should I Leave My' → 'インバーターは'; "
        "'Inverter On All The Time?' → '常時オンにすべきか？'; "
        "'Keep ON?' → 'オンのまま？'; "
        "'Turn OFF?' → 'オフにする？'. "
        "Keep the question-mark graphic, green check mark, red power icon, yellow warning triangle, clock, battery gauge, light bulb, products, and landscape exactly. "
        "The smaller left inverter must keep its green LCD and buttons. "
        "The larger right inverter must keep its black rounded front display panel; do not replace that panel with ventilation slots or remove the display. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER), the xindun logo, or CE marks. "
        "Do not add or remove objects. Do not redesign the poster."
    ),
    (2, 0): (
        "This is a diagram banner on a green background: wind turbine and solar panels at left, "
        "one white inverter at right, and three gauges along the bottom. "
        "Translate only the English overlay text to Japanese, keeping every number unchanged "
        "and keeping the two-line headline: "
        "'How Many Amps of Current Does a' → '2000Wインバーターは'; "
        "'2000 Watt Inverter Consume?' → '何アンペア消費するか？'; "
        "'12V DC INPUT' → '12V直流入力'; "
        "'24V DC INPUT' → '24V直流入力'; "
        "'48V DC INPUT' → '48V直流入力'; "
        "'HIGH' → '高'; "
        "'MEDIUM' → '中'; "
        "'LOW' → '低'. "
        "Keep 185.2A, 92.6A, and 46.3A exactly, and keep the arrows and gauge colors. "
        "Do NOT change product casing text (Low Frequency PV Inverter), the xindun logo, or CE marks. "
        "Do not redesign."
    ),
    (3, 0): (
        "This is a day-and-night marketing banner: sun and moon, a house with rooftop panels, "
        "a white battery, an orange MPPT controller, and a white inverter on a wooden table. "
        "Translate only the English overlay headline, subtitle, and three icon captions to Japanese, "
        "keeping the two-line headline and one short subtitle line: "
        "'What Is' → 'SHSソーラー'; "
        "'SHS Solar Home System?' → 'ホームシステムとは？'; "
        "'Reliable Off-Grid Power Solution for Your Home.' → '家庭向けの信頼できるオフグリッド電源'; "
        "'Reduce Electricity Costs' → '電気代を削減'; "
        "'24/7 Energy Security' → '24時間の電力確保'; "
        "'Green & Sustainable' → '環境に優しく持続可能'. "
        "Keep the dollar, shield, and leaf icons, the house, sun, moon, and products. "
        "Do NOT change product casing text (LiFePO4 Lithium Battery, MPPT Solar Charge Controller), "
        "the xindun logo, the controller display readings, or CE marks. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/03/31/202603311201351097.jpg",
            "alt_ja": "インバーターの損傷",
            "title_ja": "インバーターの損傷",
            "stem": "inverter-no-songai",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/03/28/202603281528155286.jpg",
            "alt_ja": "インバーターは常時オンのままにすべきか",
            "title_ja": "インバーターは常時オンのままにすべきか",
            "stem": "inverter-wa-joji-on",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/30/202601301718427091.jpg",
            "alt_ja": "2000Wインバーターの消費電流",
            "title_ja": "2000Wインバーターの消費電流",
            "stem": "2000w-inverter-no-shohi-denryu",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/27/202601271623259348.jpg",
            "alt_ja": "SHSソーラーソリューション",
            "title_ja": "SHSソーラーソリューション",
            "stem": "shs-solar-solutions",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/27/202601271622219263.jpg",
            "alt_ja": "SHSソーラーホームシステムの設置事例",
            "title_ja": "SHSソーラーホームシステムの設置事例",
            "stem": "shs-solar-home-system-secchi-jirei",
        },
    ],
]

IMAGE_LOG: list[dict] = []


def prepare_all() -> list[list[dict]]:
    assert_ja_progress_current()
    prepared_all: list[list[dict]] = []
    for article_idx, images in enumerate(IMAGE_SOURCES):
        prepared: list[dict] = []
        for img_idx, im in enumerate(images):
            stem = unique_stem(im["stem"])
            ext = Path(im["src"]).suffix.lower() or ".jpg"
            if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
                ext = ".jpg"
            local = OUT / f"_src_ja_p{PAGE_NUM}_a{article_idx}_i{img_idx}{ext}"
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
                    raise RuntimeError(
                        f"Duomi edit failed layout checks for a{article_idx}_i{img_idx}; "
                        "not publishing the untranslated original"
                    )
                final = result
                duomi_path = str(result)
            else:
                final = compress_only(local, stem, orig_wh)

            if final.stat().st_size > 100 * 1024:
                raise RuntimeError(f"image exceeds 100KB: {final}")
            with Image.open(final) as chk:
                if chk.size != orig_wh:
                    raise RuntimeError(f"image dimensions changed for {final}: {chk.size} vs {orig_wh}")

            stored_method = "duomi" if method.startswith("duomi") else "compress"
            marker.write_text(
                json.dumps(
                    {"method": stored_method, "src": im["src"], "duomi_path": duomi_path},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            entry = {
                "local": final,
                "alt_ja": im["alt_ja"],
                "title_ja": im["title_ja"],
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
    Path(f"/tmp/page{PAGE_NUM}_ja_image_log.json").write_text(
        json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return prepared_all


if __name__ == "__main__":
    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
