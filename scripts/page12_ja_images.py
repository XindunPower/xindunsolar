#!/usr/bin/env python3
"""Prepare page 12 Japanese images.

Duomi gpt-image-2 only for English marketing headlines and the portable-unit
diagram callouts. Listing crops are the WordPress featured images. Studio
product shots, the camping photo, the lifestyle collage, and the factory
collage are compressed and renamed. Product casing text and the Chinese wall
sign stay unchanged. Outputs stay in output/duomi/ja/.
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
PAGE_NUM = 12

KEEP_CASE = (
    " Do NOT change product casing text, the xindun logo, CE, ISO, displays, "
    "or model markings. Do not add or remove products. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a cropped comparison banner on a beige background: a white wall inverter "
        "in a rounded card on the left and a black floor cabinet on the right, with an orange VS badge. "
        "Translate only the overlay headline and the two captions under the cards. Keep two headline lines. "
        "Line 1, black: 'What Is the Difference Between' → '単相と三相の'. "
        "Line 2, orange: 'Single Phase and 3 Phase Inverter ?' → 'インバーターの違いは？'. "
        "Left caption: 'LF SINGLE PHASE INVERTER' → 'LF単相インバーター'. "
        "Right caption: 'HDSX 3 PHASE INVERTER' → 'HDSX三相インバーター'. "
        "Keep the orange VS badge as VS. Keep the orange circles 1 and 2. "
        "Keep LF and HDSX in Latin letters. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the products, cards or badge. Do not redesign."
        + KEEP_CASE
    ),
    (0, 1): (
        "This is a wide comparison banner on a beige background: a white wall inverter "
        "in a rounded card on the left and a black floor cabinet on the right, with an orange VS badge. "
        "Translate only the overlay headline and the two captions under the cards. Keep two headline lines. "
        "Line 1, black: 'What Is the Difference Between' → '単相と三相の'. "
        "Line 2, orange: 'Single Phase and 3 Phase Inverter ?' → 'インバーターの違いは？'. "
        "Left caption: 'LF SINGLE PHASE INVERTER' → 'LF単相インバーター'. "
        "Right caption: 'HDSX 3 PHASE INVERTER' → 'HDSX三相インバーター'. "
        "Keep the orange VS badge as VS. Keep the orange circles 1 and 2. "
        "Keep LF and HDSX in Latin letters. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the products, cards or badge. Do not redesign."
        + KEEP_CASE
    ),
    (1, 0): (
        "This is a cropped night banner: a lit house, a candle, lightning, and a white hybrid inverter. "
        "Translate only the overlay headline and the green pill. Keep two white headline lines. "
        "Line 1: 'Reliable Power Inverter' → '頼れるパワーインバーター'. "
        "Line 2: 'for Power Outages' → '停電に備える'. "
        "Green pill: 'Backup Energy Solution' → 'バックアップ電源'. "
        "Do NOT change HYBRID SOLAR INVERTER on the casing, the xindun logo, the display, buttons or CE marks. "
        "Do not move the house, candle, inverter or lightning. Do not redesign."
        + KEEP_CASE
    ),
    (1, 1): (
        "This is a wide night banner: a lit house, a candle, lightning, and a white hybrid inverter. "
        "Translate only the overlay headline and the green pill. Keep two white headline lines. "
        "Line 1: 'Reliable Power Inverter' → '頼れるパワーインバーター'. "
        "Line 2: 'for Power Outages' → '停電に備える'. "
        "Green pill: 'Backup Energy Solution' → 'バックアップ電源'. "
        "Do NOT change HYBRID SOLAR INVERTER on the casing, the xindun logo, the display, buttons or CE marks. "
        "Do not move the house, candle, inverter or lightning. Do not redesign."
        + KEEP_CASE
    ),
    (2, 3): (
        "This is a tall product diagram on white: a cutaway energy-storage cabinet on top, "
        "a rear-panel close-up at bottom left, the real rear panel at bottom right, and four icons. "
        "Translate ONLY the callout labels on the white background and the four captions under the icons. "
        "'Solar Controller' → 'ソーラーコントローラ'. 'Built-in MPPT' → '内蔵MPPT'. "
        "'Inverter' → 'インバーター'. 'Pure Sine Wave' → '純正弦波'. "
        "'LiFePO4 Battery' → 'LiFePO4バッテリー'. 'Longer Lifespan' → '長寿命'. "
        "Under the icons: 'DC OUTPUT' → 'DC出力'. Keep 'USB' as USB. "
        "'AC Output Socket' → 'AC出力コンセント'. 'Terminal Strip' → '端子台'. "
        "Do NOT change any text printed on the product itself: ENERGY STORAGE SYSTEM, "
        "LiFePO4+MPPT+INVERTER, the xindun logo, the display numbers, USB 5V, 12V, ON, OFF, "
        "AC OUTPUT, AC INPUT, N, L, PV, SOLAR, BATTERY, CAUTION, or the terminal markings. "
        "Keep the green leader lines, the cutaway, the circuit boards, the blue battery and both rear views. "
        "Do not add or remove parts. Do not redesign."
    ),
    (3, 0): (
        "This is a sunset banner with five inverters in front of a house and rooftop solar panels. "
        "Translate only the two-line pale headline. Keep the pale green color. "
        "Line 1: 'What Is the Best 11KW' → '最良の11kW'. "
        "Line 2: 'Solar Inverter?' → 'ソーラーインバーターは？'. "
        "Keep 11kW in Latin digits. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the inverters, house, sky or panels. Do not redesign."
        + KEEP_CASE
    ),
    (4, 0): (
        "This is a cropped pale-blue product banner: five white inverters on round podiums. "
        "Translate only the green headline: "
        "'Utility Interconnected Photovoltaic Inverters' → '系統連系型太陽光発電インバーター'. "
        "Keep it as one green line. Shrink the type only enough to stay on that one line. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the inverters, podiums or arch. Do not redesign."
        + KEEP_CASE
    ),
    (4, 1): (
        "This is a wide pale-blue product banner: five white inverters on round podiums. "
        "Translate only the green headline: "
        "'Utility Interconnected Photovoltaic Inverters' → '系統連系型太陽光発電インバーター'. "
        "Keep it as one green line. Shrink the type only enough to stay on that one line. "
        "Do NOT change text printed on the product casings, the xindun logo, displays, buttons or CE marks. "
        "Do not move the inverters, podiums or arch. Do not redesign."
        + KEEP_CASE
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/20250821144527GjQcba.jpg",
            "alt_ja": "単相と三相インバーターの違い",
            "title_ja": "単相と三相インバーターの違い",
            "stem": "単相と三相インバーターの違い",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211444307681.jpg",
            "alt_ja": "単相インバーターと三相インバーターの比較",
            "title_ja": "単相インバーターと三相インバーターの比較",
            "stem": "単相インバーターと三相インバーターの比較",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/20250821140345oVrWhz.jpg",
            "alt_ja": "停電用パワーインバーター",
            "title_ja": "停電用パワーインバーター",
            "stem": "停電用パワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211408039800.jpg",
            "alt_ja": "停電時のバックアップ電源",
            "title_ja": "停電時のバックアップ電源",
            "stem": "停電時のバックアップ電源",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg",
            "alt_ja": "HFPハイブリッドパワーインバーター",
            "title_ja": "HFPハイブリッドパワーインバーター",
            "stem": "HFPハイブリッドパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151501334463.jpg",
            "alt_ja": "HFP-Cハイブリッドパワーインバーター",
            "title_ja": "HFP-Cハイブリッドパワーインバーター",
            "stem": "HFP-Cハイブリッドパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg",
            "alt_ja": "HP PLUS+並列ハイブリッドインバーター",
            "title_ja": "HP PLUS+並列ハイブリッドインバーター",
            "stem": "HP-PLUS並列ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151505009158.jpg",
            "alt_ja": "HDSX三相パワーインバーター",
            "title_ja": "HDSX三相パワーインバーター",
            "stem": "HDSX三相パワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211416117011.jpg",
            "alt_ja": "LUスプリットフェーズパワーインバーター",
            "title_ja": "LUスプリットフェーズパワーインバーター",
            "stem": "LUスプリットフェーズパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211051145263.jpg",
            "alt_ja": "GP-Cソーラーパワーインバーター",
            "title_ja": "GP-Cソーラーパワーインバーター",
            "stem": "GP-Cソーラーパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151710038307.jpg",
            "alt_ja": "DFソーラーパワーインバーター",
            "title_ja": "DFソーラーパワーインバーター",
            "stem": "DFソーラーパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211107597731.jpg",
            "alt_ja": "ESS-Li一体型ソーラー発電機",
            "title_ja": "ESS-Li一体型ソーラー発電機",
            "stem": "ESS-Li一体型ソーラー発電機",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211353482657.jpg",
            "alt_ja": "ESS一体型ソーラー発電機",
            "title_ja": "ESS一体型ソーラー発電機",
            "stem": "ESS一体型ソーラー発電機",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/18/2025081815123669Mvi1.jpg",
            "alt_ja": "バッテリー付きポータブルパワーインバーター",
            "title_ja": "バッテリー付きポータブルパワーインバーター",
            "stem": "バッテリー付きポータブルパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/18/202508181513067423.jpg",
            "alt_ja": "ポータブル電源の利用シーン",
            "title_ja": "ポータブル電源の利用シーン",
            "stem": "ポータブル電源の利用シーン",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/18/202508181513505996.jpg",
            "alt_ja": "キャンプと救助のポータブル電源",
            "title_ja": "キャンプと救助のポータブル電源",
            "stem": "キャンプと救助のポータブル電源",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/18/202508181514415005.jpg",
            "alt_ja": "ポータブルパワーインバーターの内部構成",
            "title_ja": "ポータブルパワーインバーターの内部構成",
            "stem": "ポータブルパワーインバーターの内部構成",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/20250715151325yn7r9j.jpg",
            "alt_ja": "最良の11kWソーラーインバーター",
            "title_ja": "最良の11kWソーラーインバーター",
            "stem": "最良の11kWソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg",
            "alt_ja": "HFPシリーズ11kWインバーター",
            "title_ja": "HFPシリーズ11kWインバーター",
            "stem": "HFPシリーズ11kWインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/06/202508061014537483.jpg",
            "alt_ja": "HFP-Cシリーズ11kWソーラーインバーター",
            "title_ja": "HFP-Cシリーズ11kWソーラーインバーター",
            "stem": "HFP-Cシリーズ11kWソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151502199748.jpg",
            "alt_ja": "HFP-Eシリーズ11kWソーラーインバーター",
            "title_ja": "HFP-Eシリーズ11kWソーラーインバーター",
            "stem": "HFP-Eシリーズ11kWソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151709439605.jpg",
            "alt_ja": "LFシリーズ11kWインバーター",
            "title_ja": "LFシリーズ11kWインバーター",
            "stem": "LFシリーズ11kWインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/06/202508061015172459.jpg",
            "alt_ja": "WFシリーズ11kWインバーター",
            "title_ja": "WFシリーズ11kWインバーター",
            "stem": "WFシリーズ11kWインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151505009158.jpg",
            "alt_ja": "HDSXシリーズ11kW三相インバーター",
            "title_ja": "HDSXシリーズ11kW三相インバーター",
            "stem": "HDSXシリーズ11kW三相インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151710038307.jpg",
            "alt_ja": "DFシリーズ11kWソーラーパワーインバーター",
            "title_ja": "DFシリーズ11kWソーラーパワーインバーター",
            "stem": "DFシリーズ11kWソーラーパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151510427948.jpg",
            "alt_ja": "HFシリーズ11kWハイブリッドインバーター",
            "title_ja": "HFシリーズ11kWハイブリッドインバーター",
            "stem": "HFシリーズ11kWハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/06/202508061015336199.jpg",
            "alt_ja": "11kWソーラーインバーターメーカー",
            "title_ja": "11kWソーラーインバーターメーカー",
            "stem": "11kWソーラーインバーターメーカー",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/20250714155319IH3g8f.jpg",
            "alt_ja": "系統連系型太陽光発電インバーター",
            "title_ja": "系統連系型太陽光発電インバーター",
            "stem": "系統連系型太陽光発電インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141543223443.jpg",
            "alt_ja": "系統連系インバーターの製品群",
            "title_ja": "系統連系インバーターの製品群",
            "stem": "系統連系インバーターの製品群",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ja": "HFP系統連系インバーター",
            "title_ja": "HFP系統連系インバーター",
            "stem": "HFP系統連系インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141550028678.jpg",
            "alt_ja": "HFP-S系統連系インバーター",
            "title_ja": "HFP-S系統連系インバーター",
            "stem": "HFP-S系統連系インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ja": "HFP-C系統連系インバーター",
            "title_ja": "HFP-C系統連系インバーター",
            "stem": "HFP-C系統連系インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ja": "HFP-E系統連系インバーター",
            "title_ja": "HFP-E系統連系インバーター",
            "stem": "HFP-E系統連系インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141552243253.jpg",
            "alt_ja": "HP PLUS+系統連系インバーター",
            "title_ja": "HP PLUS+系統連系インバーター",
            "stem": "HP-PLUS系統連系インバーター",
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
