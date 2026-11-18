#!/usr/bin/env python3
"""Prepare page 3 Japanese images.

Duomi gpt-image-2 only for English marketing/diagram overlays.
Product photos and the home-install collage are compressed and renamed only.
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
PAGE_NUM = 3

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a daylight marketing banner: wind turbine and house at left, solar panels, "
        "six power products in a row, transmission tower at right, green hills. "
        "Translate only the three-line English headline to Japanese, keeping the same three-line layout "
        "and the large middle emphasis: "
        "'What Can Run Off a' → '5000ワットの'; "
        "'5000 Watt' → 'パワーコンバーターで'; "
        "'Power Converter?' → '何が動くか？'. "
        "Keep the question mark, products, panels, turbine, tower, and landscape. "
        "Do NOT change product casing text, the xindun logo, CE marks, or model markings. "
        "Do not add or remove objects. Do not redesign the poster."
    ),
    (1, 0): (
        "This is a four-scene diagram banner with a white inverter in the center, "
        "solar panel at top left, city and power lines at top right, a daytime house at bottom left, "
        "a night house at bottom right, a battery below the inverter, and yellow arrows. "
        "Translate only the headline and the three white labels to Japanese: "
        "'Can inverter run only on sun panel?' → 'インバーターは太陽光パネルだけで動くか？'; "
        "'Sun Panel' → '太陽光パネル'; "
        "'Grid' → '電力系統'; "
        "'Battery' → 'バッテリー'. "
        "Keep the question mark, arrows, products, scenes, and layout. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo, display readings, or CE marks. Do not redesign."
    ),
    (2, 0): (
        "This is a diagram banner over a solar-farm path: a line chart on the left, a bar chart on the right, "
        "one round-display inverter and one lithium battery in front. "
        "Translate only the English overlay headline and chart titles to Japanese. "
        "Keep every number and unit exactly (10kW, 5kWh, 10kWh, 15kWh) and keep the three-line headline: "
        "'How to do' → 'インバーター用'; "
        "'Inverter Battery Size Calculation' → 'バッテリー容量の計算'; "
        "'to Choose the Right Lithium Battery?' → '適切なリチウム電池の選び方は？'; "
        "'Inverter Output Power' → 'インバーター出力'; "
        "'Battery Capacity in kWh' → 'バッテリー容量（kWh）'. "
        "Keep the curve, bars, arrows, colors, products, and solar field. "
        "Do NOT change product casing text or the xindun logo. Do not redesign."
    ),
    (3, 0): (
        "This is a daylight marketing banner: solar array and mountains on the left, "
        "a white hybrid inverter and a white lithium battery on a dirt path, power lines on the right. "
        "Translate only the two-line English headline to Japanese, keeping the line break: "
        "'What Is a' → 'スプリットフェーズ並列'; "
        "'Split Phase Parallel Hybrid Inverter?' → 'ハイブリッドインバーターとは？'. "
        "Keep the question mark, products, panels, mountains, and sky. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo, or CE marks. Do not redesign."
    ),
    (4, 0): (
        "This is a dusk-to-night marketing banner of a house with rooftop solar, "
        "a wall-mounted inverter, a lithium battery, a bulb, a TV, and a refrigerator. "
        "Translate only the two English overlay lines to Japanese, keeping two lines: "
        "'Solar Inverter and Battery for Home' → '家庭用ソーラーインバーターとバッテリー'; "
        "'Stable Power, Day & Night' → '昼夜を問わない安定電力'. "
        "Keep the moon, arrows, house, products, and lighting. "
        "Do NOT change product casing text, the xindun logo, or CE marks. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241659115926.jpg",
            "alt_ja": "5000ワットパワーコンバーター",
            "title_ja": "5000ワットパワーコンバーター",
            "stem": "5000w-power-converter",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241700361463.jpg",
            "alt_ja": "HFP 5000Wコンバーター",
            "title_ja": "HFP 5000Wコンバーター",
            "stem": "hfp-5000w-converter",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241701207934.jpg",
            "alt_ja": "LUスプリットフェーズパワーコンバーター",
            "title_ja": "LUスプリットフェーズパワーコンバーター",
            "stem": "lu-split-phase-power-converter",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241702338686.jpg",
            "alt_ja": "WF 5000Wパワーコンバーター",
            "title_ja": "WF 5000Wパワーコンバーター",
            "stem": "wf-5000w-power-converter",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241704337778.jpg",
            "alt_ja": "LF 5000Wコンバーター",
            "title_ja": "LF 5000Wコンバーター",
            "stem": "lf-5000w-converter",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241712586945.jpg",
            "alt_ja": "ESS-Li一体型5000Wパワーコンバーター",
            "title_ja": "ESS-Li一体型5000Wパワーコンバーター",
            "stem": "ess-li-all-in-one-5000w",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241715091918.jpg",
            "alt_ja": "ESS 5000Wソーラーパワーコンバーター",
            "title_ja": "ESS 5000Wソーラーパワーコンバーター",
            "stem": "ess-5000w-solar-power-converter",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/24/202601241649054608.jpg",
            "alt_ja": "太陽光パネル用インバーター",
            "title_ja": "太陽光パネル用インバーター",
            "stem": "sun-panel-inverter",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/23/202601231503001875.jpg",
            "alt_ja": "インバーターのバッテリー容量計算",
            "title_ja": "インバーターのバッテリー容量計算",
            "stem": "inverter-battery-size-calculation",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/22/202601221743309376.jpg",
            "alt_ja": "スプリットフェーズ並列ハイブリッドインバーター",
            "title_ja": "スプリットフェーズ並列ハイブリッドインバーター",
            "stem": "parallel-hybrid-inverter-split-phase",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161559208083.jpg",
            "alt_ja": "家庭用ソーラーインバーターとバッテリー",
            "title_ja": "家庭用ソーラーインバーターとバッテリー",
            "stem": "solar-inverter-battery-for-home",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161601195480.jpg",
            "alt_ja": "家庭用ソーラーインバーターとバッテリーの導入事例",
            "title_ja": "家庭用ソーラーインバーターとバッテリーの導入事例",
            "stem": "solar-inverter-battery-home-case",
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
