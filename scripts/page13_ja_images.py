#!/usr/bin/env python3
"""Prepare page 13 Japanese images.

Duomi gpt-image-2 only for English marketing headlines and diagram captions.
Listing crops are the WordPress featured images. Product studio shots, the
factory/application collage, and the installation photo collage are compressed
and renamed. Product casing text stays unchanged. Outputs stay in output/duomi/ja/.
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
from page7_ja_images import SIZE_RATIOS, run_duomi_fit  # noqa: E402

UA = "Mozilla/5.0 (compatible; XindunJapaneseBot/1.0)"
PAGE_NUM = 13

KEEP_CASE = (
    " Do NOT change product casing text, the xindun logo, CE marks, displays, "
    "buttons, or model markings. Do not add or remove products. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a 4:3 crop of a dark-blue diagram. A warning triangle, sun, battery icon, "
        "house, red power tower, lightning, arrows, and a white wall inverter remain. "
        "The top headline is cropped by the frame. Do NOT invent, restore, or enlarge any headline. "
        "Do not add lines and do not change the canvas. "
        "Translate only the fully visible white caption at the bottom: "
        "'Overvoltage, frequent outages, surges – all threaten your inverter system.' "
        "→ '過電圧、頻繁な停電、サージは、インバーターを脅かします。'. "
        "Keep the warning triangle yellow. Keep every icon, arrow, tower, and the inverter in place."
        + KEEP_CASE
    ),
    (0, 1): (
        "This is a square dark-blue diagram with a three-line white headline, icons, and a white inverter. "
        "Translate only the overlay headline and the bottom caption. Keep three headline lines. "
        "Line 1: 'UNSTABLE MAINS POWER' → '不安定な商用電源は'. "
        "Line 2: 'MAY DAMAGE YOUR' → 'オフグリッドインバーターを'. "
        "Line 3: 'OFF GRID INVERTER' → '損なうことがある'. "
        "Bottom caption: 'Overvoltage, frequent outages, surges – all threaten your inverter system.' "
        "→ '過電圧、頻繁な停電、サージは、インバーターを脅かします。'. "
        "Keep the sun, battery icon, house, red tower, lightning, arrows, and warning triangle. "
        "Do not move them."
        + KEEP_CASE
    ),
    (1, 0): (
        "This is a cropped product banner: an RV behind five inverters on pale-blue blocks. "
        "Translate only the green headline. Keep it as one green line: "
        "'Solar Power Inverter For Vehicle' → '車両用ソーラーパワーインバーター'. "
        "Shrink the type only enough to stay on that one line. "
        "Do NOT change text printed on the products, including ENERGY STORAGE SYSTEM, "
        "LiFePO4 Lithium Battery, DC-AC, SOLAR GENERATOR, the xindun logo, displays, or terminals. "
        "Do not move the RV, products, or blocks. Do not redesign."
    ),
    (1, 1): (
        "This is a wide product banner: an RV behind five inverters on pale-blue blocks. "
        "Translate only the green headline. Keep it as one green line: "
        "'Solar Power Inverter For Vehicle' → '車両用ソーラーパワーインバーター'. "
        "Shrink the type only enough to stay on that one line. "
        "Do NOT change text printed on the products, including ENERGY STORAGE SYSTEM, "
        "LiFePO4 Lithium Battery, DC-AC, SOLAR GENERATOR, the xindun logo, displays, or terminals. "
        "Do not move the RV, products, or blocks. Do not redesign."
    ),
    (3, 0): (
        "This is a cropped comparison banner on a pale-blue background: two white inverters and a blue VS badge. "
        "Translate only the two-line headline. Keep two lines. "
        "Line 1: 'Why Is the Max Charging Current of High Frequency Inverter' → '高周波インバーターの最大充電電流は'. "
        "Line 2: 'Higher Than That of Low Frequency Inverter?' → 'なぜ低周波より大きいのか？'. "
        "Keep the labels HFP and LF in Latin letters. Keep the blue VS badge as VS. "
        "Do NOT change HYBRID SOLAR INVERTER or Low Frequency PV Inverter on the casings, "
        "the xindun logo, displays, buttons, or CE marks. Do not move the inverters or the badge. Do not redesign."
    ),
    (3, 1): (
        "This is a wide comparison banner on a pale-blue background: two white inverters and a blue VS badge. "
        "Translate only the two-line headline. Keep two lines. "
        "Line 1: 'Why Is the Max Charging Current of High Frequency Inverter' → '高周波インバーターの最大充電電流は'. "
        "Line 2: 'Higher Than That of Low Frequency Inverter?' → 'なぜ低周波より大きいのか？'. "
        "Keep the labels HFP and LF in Latin letters. Keep the blue VS badge as VS. "
        "Do NOT change HYBRID SOLAR INVERTER or Low Frequency PV Inverter on the casings, "
        "the xindun logo, displays, buttons, or CE marks. Do not move the inverters or the badge. Do not redesign."
    ),
    (4, 0): (
        "This is a cropped dark banner: a white inverter inside a shield, with two round shield icons. "
        "Translate only the headline and the two captions. Keep the headline as two lines. "
        "Line 1: 'What Are the Low Voltage Protection' → 'インバーターの低電圧保護と'. "
        "Line 2: 'And High Voltage Protection of Inverters?' → '高電圧保護とは？'. "
        "Left caption under the H shield: 'High Voltage Protection' → '高電圧保護'. "
        "Right caption under the L shield: 'Low Voltage Protection' → '低電圧保護'. "
        "Keep the letters H and L inside the shields. Keep the shield outlines. "
        "Do NOT change text on the inverter casing, the xindun logo, the display, or CE marks. "
        "Do not move the inverter or the shields. Do not redesign."
    ),
    (4, 1): (
        "This is a wide dark banner: a white inverter inside a shield, with two round shield icons. "
        "Translate only the headline and the two captions. Keep the headline as two lines. "
        "Line 1: 'What Are the Low Voltage Protection' → 'インバーターの低電圧保護と'. "
        "Line 2: 'And High Voltage Protection of Inverters?' → '高電圧保護とは？'. "
        "Left caption under the H shield: 'High Voltage Protection' → '高電圧保護'. "
        "Right caption under the L shield: 'Low Voltage Protection' → '低電圧保護'. "
        "Keep the letters H and L inside the shields. Keep the shield outlines. "
        "Do NOT change text on the inverter casing, the xindun logo, the display, or CE marks. "
        "Do not move the inverter or the shields. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/23/20250723141340KlhTOw.jpg",
            "alt_ja": "オフグリッドインバーターの商用電源モード",
            "title_ja": "オフグリッドインバーターの商用電源モード",
            "stem": "オフグリッドインバーターの商用電源モード",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/23/202507231412502496.jpg",
            "alt_ja": "不安定な商用電源はインバーターを損なう",
            "title_ja": "不安定な商用電源はインバーターを損なう",
            "stem": "不安定な商用電源はインバーターを損なう",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211010548954.jpg",
            "alt_ja": "車両用ソーラーパワーインバーター",
            "title_ja": "車両用ソーラーパワーインバーター",
            "stem": "車両用ソーラーパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211011296067.jpg",
            "alt_ja": "車両用パワーインバーター",
            "title_ja": "車両用パワーインバーター",
            "stem": "車両用パワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211051145263.jpg",
            "alt_ja": "車両用パワーインバーター製品",
            "title_ja": "車両用パワーインバーター製品",
            "stem": "車両用パワーインバーター製品",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151710038307.jpg",
            "alt_ja": "車両用インバーターシステム",
            "title_ja": "車両用インバーターシステム",
            "stem": "車両用インバーターシステム",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211353482657.jpg",
            "alt_ja": "車両用インバーター",
            "title_ja": "車両用インバーター",
            "stem": "車両用インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211107597731.jpg",
            "alt_ja": "車両用パワーインバーターの筐体",
            "title_ja": "車両用パワーインバーターの筐体",
            "stem": "車両用パワーインバーターの筐体",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/19/202507191512123FdpYG.jpg",
            "alt_ja": "高負荷インバーター",
            "title_ja": "高負荷インバーター",
            "stem": "高負荷インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/19/202507191503015862.jpg",
            "alt_ja": "高負荷対応インバーター",
            "title_ja": "高負荷対応インバーター",
            "stem": "高負荷対応インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/19/202507191504176168.jpg",
            "alt_ja": "高負荷インバーターの設置",
            "title_ja": "高負荷インバーターの設置",
            "stem": "高負荷インバーターの設置",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/20250702104318jxV2iD.jpg",
            "alt_ja": "インバーターの充電電流",
            "title_ja": "インバーターの充電電流",
            "stem": "インバーターの充電電流",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/202507021055145558.jpg",
            "alt_ja": "高周波と低周波の充電電流",
            "title_ja": "高周波と低周波の充電電流",
            "stem": "高周波と低周波の充電電流",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/20250702104338SAcMNt.jpg",
            "alt_ja": "低電圧保護と高電圧保護",
            "title_ja": "低電圧保護と高電圧保護",
            "stem": "低電圧保護と高電圧保護",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/202507021044418741.jpg",
            "alt_ja": "インバーターの低電圧保護と高電圧保護",
            "title_ja": "インバーターの低電圧保護と高電圧保護",
            "stem": "インバーターの低電圧保護と高電圧保護",
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
                orig_ratio = orig_wh[0] / orig_wh[1] if orig_wh[1] else 1.0
                gap = abs(SIZE_RATIOS[size] - orig_ratio)
                runner = run_duomi_fit if gap > 0.105 else run_duomi
                print(
                    f"[img] a{article_idx}_i{img_idx} size={size} gap={gap:.3f} "
                    f"runner={runner.__name__}",
                    flush=True,
                )
                result = runner(
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

            stored_method = "duomi" if str(method).startswith("duomi") else "compress"
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
