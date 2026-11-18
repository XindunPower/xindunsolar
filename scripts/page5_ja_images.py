#!/usr/bin/env python3
"""Prepare page 5 Japanese images.

Duomi gpt-image-2 only for English marketing headlines and wiring-diagram labels.
Product studio shots and the installation photo collage are compressed only.
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
PAGE_NUM = 5

WIRE = (
    "This is a wiring diagram. Translate only the English diagram labels to Japanese. "
    "Keep every wire, color, arrow, icon, product photo and terminal mark. "
    "Keep electrical symbols exactly: L, N, L1, L2, L3, P1, P2, +, −, and the figures 12V, 120V, 240V. "
    "Do NOT change product casing text (HYBRID SOLAR INVERTER, SPLIT PHASE INVERTER, "
    "Low Frequency Inverter, LiFePO4 Lithium Battery), the xindun logo, or displays. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a 3:2 marketing banner: a house with rooftop solar, a field of panels, wind turbines, "
        "and eight white or black power products on grass. Translate only the English headline to Japanese: "
        "'How to Choose the Right' → '適切な選び方'; "
        "'Photovoltaic Power Converter' → '太陽光パワーコンバータ'; "
        "'For Residential, Commercial & Industrial Applications' → '住宅・商業・産業用途向け'. "
        "Keep products, house, panels, sky and grass unchanged. "
        "Do NOT change product casing text, the xindun logo or displays. Do not redesign."
    ),
    (1, 0): (
        "This is a 3:2 product banner on a pale blue background: three white units on a round podium. "
        "Translate only the headline to Japanese: "
        "'10KW Split Phase Inverter' → '10KWスプリットフェーズインバーター'. "
        "Keep 10KW readable. Keep the three products, podium and background unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, Low Frequency Inverter, SPLIT PHASE INVERTER), "
        "the xindun logo or displays. Do not redesign."
    ),
    (1, 1): (
        WIRE + " Labels: 'Battery' → 'バッテリー'; 'Power Grid' → '電力系統'; "
        "'AC Loads' → '交流負荷'; 'PV Array' → 'PVアレイ' (every occurrence). "
        "Three inverters in one row. This is single-phase parallel wiring."
    ),
    (1, 2): (
        WIRE + " Labels: 'Battery' → 'バッテリー'; 'Power Grid' → '電力系統'; "
        "'AC Loads' → '交流負荷'; 'PV Array' → 'PVアレイ' (every occurrence). "
        "Three inverters. This is split-phase parallel wiring."
    ),
    (1, 3): (
        WIRE + " Labels: 'Battery' → 'バッテリー'; 'Power Grid' → '電力系統'; "
        "'AC Loads' → '交流負荷'; 'PV Array' → 'PVアレイ' (every occurrence). "
        "Keep the top labels P1 and P2. This is two-phase split-phase parallel wiring."
    ),
    (1, 4): (
        WIRE + " Labels: 'Battery' → 'バッテリー'; 'Power Grid' → '電力系統'; "
        "'AC Loads' → '交流負荷'; 'PV Array' → 'PVアレイ' (every occurrence). "
        "Three inverters with green, red and blue phase wires. This is three-phase parallel wiring. "
        "Keep L1, L2, L3 and N."
    ),
    (1, 5): (
        WIRE + " Labels: 'Solar Panels' → '太陽光パネル'; 'Battery' → 'バッテリー'; "
        "'Power Grid' → '電力系統'; 'AC Loads' → '交流負荷'. "
        "One inverter. Grid is 120V between L1 and N. Loads show 240V and 120V. Single-phase system."
    ),
    (1, 6): (
        WIRE + " Labels: 'Solar Panels' → '太陽光パネル'; 'Battery' → 'バッテリー'; "
        "'Power Grid' → '電力系統'; 'AC Loads' → '交流負荷'. "
        "Grid shows L1, L2, N with 120V and 240V. Split-phase system."
    ),
    (1, 7): (
        WIRE + " Labels: 'Solar Panels' → '太陽光パネル'; 'AC Input' → '交流入力'; "
        "'or' → 'または'; 'Generator' → '発電機'; 'Battery' → 'バッテリー'; "
        "'AC Output' → '交流出力'; 'Laptop' → 'ノートパソコン'; 'Printer' → 'プリンター'; "
        "'TV' → 'テレビ'; 'Fans' → '扇風機'; 'Water pump' → 'ポンプ'."
    ),
    (1, 8): (
        WIRE + " Labels: 'Solar Panels' → '太陽光パネル'; 'Utility Grid' → '商用系統'; "
        "'OR' → 'または'; 'Generator' → '発電機'; 'Battery' → 'バッテリー'; "
        "'AC OUTPUT' → '交流出力'; 'AC Loads' → '交流負荷' (both occurrences). "
        "Keep 12V, 240V, L1, L2 and N."
    ),
    (2, 0): (
        "This is a night marketing banner: a white inverter on the left and a cutaway house on the right. "
        "Translate only the two-line headline to Japanese, keeping 3000 large and green: "
        "'Will 3000 Watt Pure Sine Wave Inverter' → '3000ワット純正弦波インバーターで'; "
        "'Run a House?' → '家は動くか？'. "
        "Keep the question mark, inverter, house, fridge, air conditioner, TV and sine wave unchanged. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, CE, ISO or the display. Do not redesign."
    ),
    (3, 0): (
        "This is a dusk banner of two white units on a lawn in front of a house. "
        "Translate only the headline to Japanese: "
        "'Solar Battery Backup Inverter' → '太陽光バッテリーバックアップインバーター'. "
        "Keep both products, house, grass and sky unchanged. "
        "Do NOT change casing text (LiFePO4 Lithium Battery, HYBRID SOLAR INVERTER), "
        "the xindun logo or displays. Do not redesign."
    ),
    (4, 0): (
        "This is a pale-blue product lineup banner with eight units. "
        "Translate only the stacked headline to Japanese, keeping the orange and blue blocks: "
        "'12 Volt' → '12ボルト'; '220 Volt' → '220ボルト'; 'INVERTER' → 'インバーター'. "
        "Keep every product unchanged. "
        "Do NOT change product casing text, the xindun logo or displays. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/26/202512261347465141.jpg",
            "alt_ja": "太陽光パワーコンバータ",
            "title_ja": "太陽光パワーコンバータ",
            "stem": "太陽光パワーコンバータ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/26/202512261348523657.jpg",
            "alt_ja": "太陽光パワーコンバータの導入事例",
            "title_ja": "太陽光パワーコンバータの導入事例",
            "stem": "太陽光パワーコンバータの導入事例",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ja": "ハイブリッド太陽光パワーコンバータ",
            "title_ja": "ハイブリッド太陽光パワーコンバータ",
            "stem": "ハイブリッド太陽光パワーコンバータ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg",
            "alt_ja": "ソーラーパワーコンバータ",
            "title_ja": "ソーラーパワーコンバータ",
            "stem": "ソーラーパワーコンバータ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ja": "太陽光コンバータ",
            "title_ja": "太陽光コンバータ",
            "stem": "太陽光コンバータ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125487765.jpg",
            "alt_ja": "三相太陽光パワーコンバータ",
            "title_ja": "三相太陽光パワーコンバータ",
            "stem": "三相太陽光パワーコンバータ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125237036.jpg",
            "alt_ja": "スプリットフェーズ太陽光コンバータ",
            "title_ja": "スプリットフェーズ太陽光コンバータ",
            "stem": "スプリットフェーズ太陽光コンバータ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181616085997.jpg",
            "alt_ja": "PVパワーコンバータ",
            "title_ja": "PVパワーコンバータ",
            "stem": "PVパワーコンバータ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757379506.jpg",
            "alt_ja": "太陽光発電用コンバータ",
            "title_ja": "太陽光発電用コンバータ",
            "stem": "太陽光発電用コンバータ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091126518485.jpg",
            "alt_ja": "オールインワン太陽光パワー発電機",
            "title_ja": "オールインワン太陽光パワー発電機",
            "stem": "オールインワン太陽光パワー発電機",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/23/202512231811267150.jpg",
            "alt_ja": "10kWスプリットフェーズインバーター",
            "title_ja": "10kWスプリットフェーズインバーター",
            "stem": "10kWスプリットフェーズインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141154031704.jpg",
            "alt_ja": "HU単相並列",
            "title_ja": "HU単相並列",
            "stem": "HU単相並列",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155069284.jpg",
            "alt_ja": "HUスプリットフェーズ並列インバーター",
            "title_ja": "HUスプリットフェーズ並列インバーター",
            "stem": "HUスプリットフェーズ並列インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141157382346.jpg",
            "alt_ja": "二相スプリットフェーズ並列インバーター",
            "title_ja": "二相スプリットフェーズ並列インバーター",
            "stem": "二相スプリットフェーズ並列インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155496791.jpg",
            "alt_ja": "スプリットフェーズインバーターの三相並列",
            "title_ja": "スプリットフェーズインバーターの三相並列",
            "stem": "スプリットフェーズインバーターの三相並列",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/23/202512231759127889.jpg",
            "alt_ja": "スプリットフェーズインバーター単相系統",
            "title_ja": "スプリットフェーズインバーター単相系統",
            "stem": "スプリットフェーズインバーター単相系統",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141426036849.jpg",
            "alt_ja": "10kWスプリットフェーズインバーターの配線",
            "title_ja": "10kWスプリットフェーズインバーターの配線",
            "stem": "10kWスプリットフェーズインバーターの配線",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/11/09/202411091606366102.jpg",
            "alt_ja": "スプリットフェーズインバーターの単相配線",
            "title_ja": "スプリットフェーズインバーターの単相配線",
            "stem": "スプリットフェーズインバーターの単相配線",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141432533866.jpg",
            "alt_ja": "10kWインバーター",
            "title_ja": "10kWインバーター",
            "stem": "10kWインバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/23/202512231745238361.jpg",
            "alt_ja": "3000ワット純正弦波インバーター",
            "title_ja": "3000ワット純正弦波インバーター",
            "stem": "3000ワット純正弦波インバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201713589748.jpg",
            "alt_ja": "太陽光バッテリーバックアップインバーター",
            "title_ja": "太陽光バッテリーバックアップインバーター",
            "stem": "太陽光バッテリーバックアップインバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201646268458.jpg",
            "alt_ja": "12ボルト220ボルトインバーター",
            "title_ja": "12ボルト220ボルトインバーター",
            "stem": "12ボルト220ボルトインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201649052138.jpg",
            "alt_ja": "HFP 12ボルト220ボルトインバーター",
            "title_ja": "HFP 12ボルト220ボルトインバーター",
            "stem": "HFP-12ボルト220ボルトインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201650119960.jpg",
            "alt_ja": "LF 12ボルト220ボルトインバーター",
            "title_ja": "LF 12ボルト220ボルトインバーター",
            "stem": "LF-12ボルト220ボルトインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201650488303.jpg",
            "alt_ja": "DF 220ボルトインバーター",
            "title_ja": "DF 220ボルトインバーター",
            "stem": "DF-220ボルトインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201651201692.jpg",
            "alt_ja": "LS 12ボルトインバーター",
            "title_ja": "LS 12ボルトインバーター",
            "stem": "LS-12ボルトインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201652418130.jpg",
            "alt_ja": "WF 220ボルトインバーター",
            "title_ja": "WF 220ボルトインバーター",
            "stem": "WF-220ボルトインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201653434694.jpg",
            "alt_ja": "WD 12ボルト220ボルトインバーター",
            "title_ja": "WD 12ボルト220ボルトインバーター",
            "stem": "WD-12ボルト220ボルトインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201655539810.jpg",
            "alt_ja": "ESS-Li 220ボルトソーラー発電機",
            "title_ja": "ESS-Li 220ボルトソーラー発電機",
            "stem": "ESS-Li-220ボルトソーラー発電機",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/20/202512201656447609.jpg",
            "alt_ja": "12ボルト220ボルトソーラー発電機",
            "title_ja": "12ボルト220ボルトソーラー発電機",
            "stem": "12ボルト220ボルトソーラー発電機",
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
