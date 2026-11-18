#!/usr/bin/env python3
"""Prepare page 4 Japanese images.

Duomi gpt-image-2 only for English marketing/diagram overlays.
Plain product photos are compressed and renamed only.
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
PAGE_NUM = 4

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a blue-sky marketing diagram: sun and solar panel on the left, "
        "a tall white-and-black all-in-one cabinet in the center, a portable battery at lower left, "
        "appliances on the right, a power tower labeled Grid, and a generator. "
        "Translate only the English overlay headline, subtitle, and two labels to Japanese: "
        "'What Is All In One Hybrid Solar Inverter?' → 'オールインワン・ハイブリッドソーラーインバーターとは？'; "
        "'Inverter+Solar Controller+Battery in One System' → 'インバーター＋ソーラーコントローラ＋バッテリーを一台に'; "
        "'Grid' → '電力系統'; 'Generator' → '発電機'. "
        "Keep the xindun logo, ENERGY STORAGE SYSTEM casing text, display digits, CE marks, "
        "arrows, products, clouds, grass, and layout. Do not add or remove objects. Do not redesign."
    ),
    (0, 2): (
        "This is a two-panel product diagram on white: front view on top, rear view below, "
        "with green callout lines. Translate only the English callout labels to Japanese. "
        "Front: 'LED Indicator' → 'LED表示灯'; 'LCD Display' → 'LCD表示'; "
        "'12VDC Output' → 'DC12V出力'; 'USB 5VDC Output' → 'USB 5VDC出力'; "
        "'AC Output Socket' → 'AC出力コンセント'; 'DC Output Switch' → 'DC出力スイッチ'. "
        "Rear title 'AC INPUT/OUTPUT SOLAR INPUT Terminal Block' → 'AC入力/出力・太陽光入力 端子台'; "
        "'AC Input / Output Switch' → 'AC入力/出力スイッチ'; 'Battery Switch' → 'バッテリースイッチ'; "
        "'Spare Battery' → '予備バッテリー'; 'RS232 Communication Interface' → 'RS232通信端子'; "
        "'RS485 Communication Interface' → 'RS485通信端子'. "
        "Keep the xindun GREEN POWER logo, display readings, fan, sockets, breakers, green lines, "
        "and the two-panel layout. Do not redesign."
    ),
    (0, 3): (
        "This is a cutaway diagram of a white energy-storage cabinet with three green callouts on the right. "
        "Translate only those callout headings and sublines to Japanese: "
        "'Solar Controller' → 'ソーラーコントローラ'; 'Built-in MPPT' → 'MPPT内蔵'; "
        "'Inverter' → 'インバーター'; 'Pure Sine Wave' → '純正弦波'; "
        "'LiFePO4 Battery' → 'LiFePO4バッテリー'; 'Longer Lifespan' → 'より長い寿命'. "
        "Do NOT change product casing text (ENERGY STORAGE SYSTEM, LiFePO4+MPPT+INVERTER), "
        "the xindun logo, display digits, or marks on the blue battery. Do not redesign."
    ),
    (0, 4): (
        "This is a three-view diagram inside a green frame: front on top, two rear views below, "
        "with green callout lines. Translate only the English callout labels to Japanese: "
        "'LCD Display' → 'LCD表示'; 'Function keys' → '機能キー'; 'Up keys' → '上キー'; "
        "'Down keys' → '下キー'; 'Inverter Switch' → 'インバータースイッチ'; 'Handle' → '取っ手'; "
        "'Battery Switch' → 'バッテリースイッチ'; 'DC Output Switch' → 'DC出力スイッチ'. "
        "Keep 'WiFi/GPRS' and 'RS485' as they are. "
        "Do NOT change the xindun logo, port silkscreen on the product (USB, 12V, AC), "
        "display digits, or the green frame. Do not redesign."
    ),
    (0, 5): (
        "This is a white marketing diagram titled Multiple Output, with a magnified rear panel, "
        "the full unit, and four icons along the bottom. "
        "Translate only the headline, the subtitle, and the four bottom icon captions to Japanese: "
        "'Multiple Output' → '複数出力'; "
        "'4*DC 12V 、 4*USB 、 AC Output Socket and Terminal Strip' → 'DC12V×4、USB×4、AC出力コンセントと端子台'; "
        "'DC OUTPUT' → 'DC出力'; 'USB' stays 'USB'; "
        "'AC Output Socket' → 'AC出力コンセント'; 'Terminal Strip' → '端子台'. "
        "Do NOT change silkscreen printed on the product panel "
        "(USB 5V, 12V, ON/OFF, AC OUTPUT, AC INPUT, SOLAR, N, L, BATTERY). "
        "Keep the green magnifier, products, and layout. Do not redesign."
    ),
    (1, 0): (
        "This is a green infographic comparing a single inverter without a battery and a three-unit parallel system. "
        "Translate only the English overlay text to Japanese, keeping each label in its own box: "
        "headline 'Can Parallel Hybrid Inverter Use Batteryless Operation Mode?' → "
        "'並列ハイブリッドインバーターはバッテリーなし運転ができるか？'; "
        "'POWER SOURCES' → '電源'; 'Solar Power' → '太陽光発電'; 'Mains Power' → '商用電源'; "
        "'NO BATTERY REQUIRED' → 'バッテリー不要'; 'RUNS WITHOUT BATTERY' → 'バッテリーなしで運転'; "
        "'PARALLEL SYSTEM' → '並列システム'; "
        "'BATTERY REQUIRED FOR PARALLEL OPERATION' → '並列運転にはバッテリーが必要'; "
        "'NO BATTERYLESS MODE' → 'バッテリーなしモード不可'; "
        "'NO BACKUP POWER' → 'バックアップ電源なし'; 'GRID FAILURE' → '系統停電'; "
        "'NO ENERGY STORAGE' → '蓄電なし'; 'DIRECT POWER USE ONLY' → '発電のその場利用のみ'. "
        "Keep the xindun logo, CE marks, products, icons, colors, arrows, and two-column layout. "
        "Do not redesign."
    ),
    (2, 0): (
        "This is a dark-green marketing banner with a white hybrid inverter in the center and four labeled panels. "
        "Translate only the English overlay text to Japanese: "
        "'Parallel Hybrid Inverter' → '並列ハイブリッドインバーター'; "
        "'Fault Codes & Protection Functions' → '故障コードと保護機能'; "
        "'Battery Fault Codes' → 'バッテリー故障コード'; "
        "'Battery Undervoltage' → 'バッテリー低電圧'; 'Overcurrent' → '過電流'; "
        "'Connection Error' → '接続異常'; "
        "'Solar Protection' → '太陽光保護'; 'Overvoltage Shield' → '過電圧保護'; "
        "'Current Limiting' → '電流制限'; 'Reverse Charging Protection' → '逆充電保護'; "
        "'Inverter Circuit Protection' → 'インバーター回路保護'; "
        "'Overload Safety' → '過負荷安全'; 'Short Circuit Protection' → '短絡保護'; "
        "'Overheat Defense' → '過熱防御'; "
        "'Output Protection' → '出力保護'; 'Short Circuit Guard' → '短絡ガード'; "
        "'Overload Control' → '過負荷制御'; 'AC Reverse Protection' → '交流逆流保護'; "
        "'FAULT ALARM' → '故障警報'. "
        "Do NOT change the xindun logo or HYBRID SOLAR INVERTER casing text. "
        "Keep the alarm light, checklist, magnifier, sun, panels, and layout. Do not redesign."
    ),
    (3, 0): (
        "This is a sunset marketing banner with maple leaves, two white inverters, solar panels, a house, and a power tower. "
        "Translate only the English headline and the two bottom captions to Japanese, keeping the stacked headline: "
        "'Why the Best' → '最高の'; 'Split Phase' → 'スプリットフェーズ'; "
        "'Solar Inverter' → 'ソーラーインバーター'; "
        "'Matters for Solar System?' → 'が太陽光発電に重要な理由'; "
        "'Day/Night Smart Scheduling' → '昼夜のスマートスケジュール'; "
        "'Up to 6x Parallel Connection' → '最大6台の並列接続'. "
        "Do NOT change LiFePO4 Lithium Battery casing text, the xindun logo, or CE marks. "
        "Keep the products, leaves, house, panels, and sunset. Do not redesign."
    ),
    (4, 0): (
        "This is a three-column diagram under a green headline bar: too many panels, a proper ratio, and too few panels. "
        "Translate only the English overlay text to Japanese: "
        "'What Happens If You Connect Too Many Solar Panels to Inverter?' → "
        "'太陽光パネルをインバーターに接続しすぎるとどうなるか？'; "
        "'Too Many' → '多すぎる'; 'Proper Ratio' → '適切な比率'; 'Too Few' → '少なすぎる'; "
        "'Clipping' → '出力制限'; 'Power Wasted' → '電力の無駄'; "
        "'Best Efficiency' → '最高効率'; 'Grid Support' → '系統で補う'; 'Battery Backup' → 'バッテリーで補う'. "
        "Keep the xindun logos, CE marks, panel counts, check and cross icons, and three columns. "
        "Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161544446666.jpg",
            "alt_ja": "オールインワンハイブリッドインバーター",
            "title_ja": "オールインワンハイブリッドインバーター",
            "stem": "オールインワンハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161545443780.jpg",
            "alt_ja": "オールインワンインバーター",
            "title_ja": "オールインワンインバーター",
            "stem": "オールインワンインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161546138528.jpg",
            "alt_ja": "オールインワンハイブリッドソーラーインバーター",
            "title_ja": "オールインワンハイブリッドソーラーインバーター",
            "stem": "オールインワンハイブリッドソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161547032380.jpg",
            "alt_ja": "オールインワンソーラーインバーター",
            "title_ja": "オールインワンソーラーインバーター",
            "stem": "オールインワンソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161547371441.jpg",
            "alt_ja": "ハイブリッドインバーター",
            "title_ja": "ハイブリッドインバーター",
            "stem": "ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/16/202601161548072528.jpg",
            "alt_ja": "インバーターオールインワン",
            "title_ja": "インバーターオールインワン",
            "stem": "インバーターオールインワン",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/13/202601131758599588.jpg",
            "alt_ja": "ハイブリッドインバーターの並列",
            "title_ja": "ハイブリッドインバーターの並列",
            "stem": "ハイブリッドインバーターの並列",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ja": "HFPバッテリーなしハイブリッドインバーター",
            "title_ja": "HFPバッテリーなしハイブリッドインバーター",
            "stem": "HFPバッテリーなしハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ja": "HFP-Cバッテリーなしハイブリッドインバーター",
            "title_ja": "HFP-Cバッテリーなしハイブリッドインバーター",
            "stem": "HFP-Cバッテリーなしハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141550028678.jpg",
            "alt_ja": "HFP-Sハイブリッドインバーター",
            "title_ja": "HFP-Sハイブリッドインバーター",
            "stem": "HFP-Sハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ja": "HFP-Eバッテリーなしインバーター",
            "title_ja": "HFP-Eバッテリーなしインバーター",
            "stem": "HFP-Eバッテリーなしインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg",
            "alt_ja": "HU並列ハイブリッドインバーター",
            "title_ja": "HU並列ハイブリッドインバーター",
            "stem": "HU並列ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg",
            "alt_ja": "HP Plus+ハイブリッドインバーター並列",
            "title_ja": "HP Plus+ハイブリッドインバーター並列",
            "stem": "HP-Plus-ハイブリッドインバーター並列",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2026/01/13/20260113173404LoDdKT.jpg",
            "alt_ja": "並列ハイブリッドインバーターの故障と保護",
            "title_ja": "並列ハイブリッドインバーターの故障と保護",
            "stem": "並列ハイブリッドインバーターの故障と保護",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg",
            "alt_ja": "インバーターの故障",
            "title_ja": "インバーターの故障",
            "stem": "インバーターの故障",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg",
            "alt_ja": "インバーターの保護",
            "title_ja": "インバーターの保護",
            "stem": "インバーターの保護",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/27/202512271351579370.jpg",
            "alt_ja": "最適なスプリットフェーズインバーター",
            "title_ja": "最適なスプリットフェーズインバーター",
            "stem": "最適なスプリットフェーズインバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/26/202512261546573452.jpg",
            "alt_ja": "太陽光パネルとインバーター",
            "title_ja": "太陽光パネルとインバーター",
            "stem": "太陽光パネルとインバーター",
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
