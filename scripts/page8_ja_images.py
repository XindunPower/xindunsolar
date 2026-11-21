#!/usr/bin/env python3
"""Prepare page 8 Japanese images.

Duomi gpt-image-2 for marketing banners and wiring diagrams that carry English
overlay labels. Product studio shots and the house installation photo are
compressed only. Outputs stay in output/duomi/ja/.
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
PAGE_NUM = 8

KEEP = (
    "Keep wiring colors, arrows, icons, products, background and layout unchanged. "
    "Do NOT change product casing text, the xindun logo, CE or ISO marks, displays, "
    "model numbers, or the wire marks N and L. Do not add or remove objects. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a pale studio marketing banner: four inverter units on white podiums. "
        "Translate only the two-line headline: "
        "'Pure Sine Wave' → '純正弦波'; "
        "'Combined Inverter & Charger' → '一体型インバーター充電器'. "
        "Keep the two-line layout, products, podiums and background unchanged. "
        "Do NOT change casing text (ENERGY STORAGE SYSTEM, SOLAR GENERATOR), "
        "the xindun logo or displays. Do not redesign."
    ),
    (0, 1): (
        "Wiring diagram of one white low-frequency inverter, four panels above, a battery below, "
        "a generator and grid at lower left, appliances at the right. Translate only these labels: "
        "Solar Panels→太陽光パネル, AC Output→交流出力, Refrigerator→冷蔵庫, "
        "Fan heater→ファンヒーター, Air conditioner→エアコン, Heater→ヒーター, "
        "Percussion drill→ハンマードリル, AC Input→交流入力, or→または, "
        "Generator→発電機, Battery→バッテリー. "
        "Do NOT change the casing line 'Low Frequency PV Inverter'. " + KEEP
    ),
    (0, 2): (
        "Wiring diagram of one blue wall inverter, panels at upper left, generator and grid at lower left, "
        "four batteries below, five loads on the right. Translate only these labels: "
        "SOLAR PANELS→太陽光パネル, AC INPUT→交流入力, Generator→発電機, "
        "AC OUTPUT→交流出力, LAPTOP→ノートパソコン, LAMP→ランプ, PRINTER→プリンター, "
        "TV→テレビ, FAN→扇風機, BATTERIES→バッテリー. " + KEEP
    ),
    (0, 3): (
        "Wiring diagram of one tall white energy-storage unit. Panel at upper left, generator and grid "
        "at lower left, AC loads on the right, DC loads along the bottom. Translate only these labels: "
        "Solar Panel→太陽光パネル, AC Output→交流出力, Laptop→ノートパソコン, "
        "Refrigerator→冷蔵庫, Air-conditioning→エアコン, Hair drier→ヘアドライヤー, "
        "Water dispenser→ウォーターサーバー, AC Input→交流入力, or→または, "
        "Generator→発電機, DC Output→直流出力, Lamp→ランプ, "
        "Mobile Phone→携帯電話, Wireless Earphone→ワイヤレスイヤホン. "
        "Do NOT change the casing line 'ENERGY STORAGE SYSTEM' or 'LiFePO4+MPPT+INVERTER'. " + KEEP
    ),
    (0, 4): (
        "Wiring diagram of two tower units on the right, panels at upper left, grid and generator at mid left, "
        "a boxed row of AC loads and a small box of DC loads. Keep the letters N and L on the wires. "
        "Translate only these labels: "
        "INVERTER→インバーター, SOLAR PANELS→太陽光パネル, or→または, "
        "POWER GRID→電力系統, GENERATOR→発電機, Fan→扇風機, "
        "Notebook Computer→ノートパソコン, Hair Drier→ヘアドライヤー, "
        "Electric kettle→電気ケトル, AC LOADS→交流負荷, DC LOADS→直流負荷. "
        "Do NOT change the casing line 'SOLAR GENERATOR'. " + KEEP
    ),
    (1, 0): (
        "Daylight marketing banner: two solar panels, an arrow, and one white inverter "
        "in front of a house with rooftop solar. Translate only the headline: "
        "'Solar Panel Direct To Inverter' → '太陽光パネルをインバーターへ直接接続'. "
        "Keep panels, arrow, inverter, house and sky unchanged. "
        "Do NOT change casing text (SPLIT PHASE INVERTER), the xindun logo or the display. "
        "Do not redesign."
    ),
    (2, 0): (
        "Pale-blue marketing banner: a closed white inverter and an open chassis on a podium. "
        "Translate only the two-line headline, keeping the line break. "
        "Line 1 must read exactly ソーラー充電コントローラ. "
        "Line 2 must read exactly インバーター組合せ. "
        "After ター write the kanji 組 immediately. Do not insert a long-vowel dash, and do not write 一体 or ー体. "
        "Keep the letters MPPT on the blue badge exactly. "
        "Keep products, podium and background unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER), the xindun logo, CE or the display. "
        "Do not redesign."
    ),
    (3, 0): (
        "Diagram banner inside a white rounded card: a solar panel, a small controller, "
        "a battery and a tall inverter, with black arrows. Translate only the overlay labels: "
        "'How Does Solar Panel to Battery' → '太陽光パネルからバッテリー、'; "
        "'to Inverter Work?' → 'インバーターはどう動くか？'; "
        "'Solar Controller' → 'ソーラーコントローラー'; "
        "'Solar Panels' → '太陽光パネル'; "
        "'Battery' → 'バッテリー'; "
        "'Solar Inverter' → 'ソーラーインバーター'. "
        "Keep arrows, products, house and sky unchanged. "
        "Do NOT change casing text (LiFePO4 Lithium Battery, Low Frequency PV Inverter), "
        "the xindun logo, CE or displays. Do not redesign."
    ),
    (4, 0): (
        "Pale studio marketing banner: five white inverters on blocks and a round podium. "
        "Translate only the headline and the green badge: "
        "'Inverter Solar To 220 Volts' → '太陽光を220Vにするインバーター'; "
        "'Without Battery' → 'バッテリーなし'. "
        "Keep the green badge shape, products, spheres, pyramid and background unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, the word INVERTER on the round button), "
        "the xindun logo, CE or displays. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/29/20251029110530nAzTrq.jpg",
            "alt_ja": "純正弦波一体型インバーター充電器",
            "title_ja": "純正弦波一体型インバーター充電器",
            "stem": "純正弦波一体型インバーター充電器",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2023/11/25/20231125171345fMB3JT.jpg",
            "alt_ja": "DF純正弦波一体型インバーター充電器",
            "title_ja": "DF純正弦波一体型インバーター充電器",
            "stem": "DF純正弦波一体型インバーター充電器",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/01/20/202501201454429424.jpg",
            "alt_ja": "LSインバーター充電器",
            "title_ja": "LSインバーター充電器",
            "stem": "LSインバーター充電器",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/03/19/20240319180514Fw1B02.jpg",
            "alt_ja": "ESS-Li純正弦波一体型インバーター充電器",
            "title_ja": "ESS-Li純正弦波一体型インバーター充電器",
            "stem": "ESS-Li純正弦波一体型インバーター充電器",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311726521839.jpg",
            "alt_ja": "ESS純正弦波インバーター充電器",
            "title_ja": "ESS純正弦波インバーター充電器",
            "stem": "ESS純正弦波インバーター充電器",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241506246986.jpg",
            "alt_ja": "太陽光パネルをインバーターへ直接接続",
            "title_ja": "太陽光パネルをインバーターへ直接接続",
            "stem": "太陽光パネルをインバーターへ直接接続",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241448493461.jpg",
            "alt_ja": "ソーラーチャージコントローラー一体型インバーター",
            "title_ja": "ソーラーチャージコントローラー一体型インバーター",
            "stem": "ソーラーチャージコントローラー一体型インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151404306156.jpg",
            "alt_ja": "HUソーラーチャージコントローラー一体型インバーター",
            "title_ja": "HUソーラーチャージコントローラー一体型インバーター",
            "stem": "HUソーラーチャージコントローラー一体型インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg",
            "alt_ja": "HFPソーラーチャージコントローラー一体型インバーター",
            "title_ja": "HFPソーラーチャージコントローラー一体型インバーター",
            "stem": "HFPソーラーチャージコントローラー一体型インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241453376522.jpg",
            "alt_ja": "ソーラーチャージコントローラー付きHFP-Sインバーター",
            "title_ja": "ソーラーチャージコントローラー付きHFP-Sインバーター",
            "stem": "ソーラーチャージコントローラー付きHFP-Sインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151501334463.jpg",
            "alt_ja": "HFP-Cソーラーコントローラー一体型インバーター",
            "title_ja": "HFP-Cソーラーコントローラー一体型インバーター",
            "stem": "HFP-Cソーラーコントローラー一体型インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151502199748.jpg",
            "alt_ja": "HFP-Eソーラーコントローラーインバーター",
            "title_ja": "HFP-Eソーラーコントローラーインバーター",
            "stem": "HFP-Eソーラーコントローラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg",
            "alt_ja": "HP PLUS+ソーラーインバーターとチャージコントローラーの一体型",
            "title_ja": "HP PLUS+ソーラーインバーターとチャージコントローラーの一体型",
            "stem": "HP-PLUS+ソーラーインバーターとチャージコントローラーの一体型",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/20251022162327Mp17mX.jpg",
            "alt_ja": "太陽光パネルからバッテリー、インバーターへ",
            "title_ja": "太陽光パネルからバッテリー、インバーターへ",
            "stem": "太陽光パネルからバッテリー、インバーターへ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221626318952.jpg",
            "alt_ja": "HFPのパネル・バッテリー・インバーター",
            "title_ja": "HFPのパネル・バッテリー・インバーター",
            "stem": "HFPのパネル・バッテリー・インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221627174500.jpg",
            "alt_ja": "HDSXのパネル・バッテリー・インバーター",
            "title_ja": "HDSXのパネル・バッテリー・インバーター",
            "stem": "HDSXのパネル・バッテリー・インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221628024529.jpg",
            "alt_ja": "WFソーラーインバーターシステム",
            "title_ja": "WFソーラーインバーターシステム",
            "stem": "WFソーラーインバーターシステム",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221628358086.jpg",
            "alt_ja": "ESS一体型ソーラー発電機",
            "title_ja": "ESS一体型ソーラー発電機",
            "stem": "ESS一体型ソーラー発電機",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/22/202510221629169116.jpg",
            "alt_ja": "ESS-Liソーラー発電機",
            "title_ja": "ESS-Liソーラー発電機",
            "stem": "ESS-Liソーラー発電機",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241514554488.jpg",
            "alt_ja": "バッテリーなしで太陽光を220Vへ",
            "title_ja": "バッテリーなしで太陽光を220Vへ",
            "stem": "バッテリーなしで太陽光を220Vへ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/24/202510241516254008.jpg",
            "alt_ja": "太陽光220V変換の設置例",
            "title_ja": "太陽光220V変換の設置例",
            "stem": "太陽光220V変換の設置例",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141552243253.jpg",
            "alt_ja": "バッテリーなしのソーラーインバーター",
            "title_ja": "バッテリーなしのソーラーインバーター",
            "stem": "バッテリーなしのソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ja": "バッテリーなしのインバーター",
            "title_ja": "バッテリーなしのインバーター",
            "stem": "バッテリーなしのインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141550028678.jpg",
            "alt_ja": "バッテリーなしのハイブリッドインバーター",
            "title_ja": "バッテリーなしのハイブリッドインバーター",
            "stem": "バッテリーなしのハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ja": "バッテリーなしで太陽光を220Vにするインバーター",
            "title_ja": "バッテリーなしで太陽光を220Vにするインバーター",
            "stem": "バッテリーなしで太陽光を220Vにするインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ja": "バッテリーなしのハイブリッドソーラーインバーター",
            "title_ja": "バッテリーなしのハイブリッドソーラーインバーター",
            "stem": "バッテリーなしのハイブリッドソーラーインバーター",
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

            stored_method = "compress"
            if method.startswith("duomi") and method != "duomi-fallback-original":
                stored_method = "duomi"
            if method == "duomi-fallback-original":
                stored_method = "duomi-fallback-original"
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
