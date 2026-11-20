#!/usr/bin/env python3
"""Prepare page 7 Japanese images.

Duomi gpt-image-2 for marketing banners and wiring diagrams that carry English
overlay labels. Product studio shots, installation collages, and the factory
floor collage are compressed only.
Outputs stay in output/duomi/ja/ so they do not collide with the Russian task.
Marketing or diagram edits that fail layout checks are discarded and retried
from the original. They are not replaced by drawing text onto the original.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from page1_ja_images import (  # noqa: E402
    OUT,
    PROMPT_BASE,
    REPO,
    assert_ja_progress_current,
    compress_only,
    image_mean_diff,
    run_duomi,
    size_for,
    unique_stem,
)

SIZE_RATIOS = {
    "1:1": 1.0,
    "3:2": 1.5,
    "2:3": 2 / 3,
    "16:9": 16 / 9,
    "9:16": 9 / 16,
    "4:3": 4 / 3,
    "3:4": 3 / 4,
    "21:9": 21 / 9,
    "2:1": 2.0,
    "3:1": 3.0,
}

UA = "Mozilla/5.0 (compatible; XindunJapaneseBot/1.0)"
PAGE_NUM = 7

KEEP = (
    "Keep wiring colors, arrows, icons, products, background and layout unchanged. "
    "Do NOT change product casing text, the xindun logo, CE or ISO marks, displays, "
    "model numbers, phase marks L1 L2 L3 N, or voltage numbers such as 120V and 240V. "
    "Do not add or remove objects. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a daylight marketing banner: inverters on a lawn, mountains and rooftop solar. "
        "Translate only the headline. Keep the red rounded pill on the second phrase: "
        "'Pure Sine Wave' → '純正弦波'; the red pill 'Off Grid Solar Inverter' → 'オフグリッドソーラーインバーター'. "
        "Keep every product, the grass, mountains and panels unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, SPLIT PHASE INVERTER, Low Frequency), "
        "the xindun logo, CE marks or displays. Do not redesign."
    ),
    (1, 0): (
        "This is a night banner: a clock, two white inverters on a round platform, solar panels at right. "
        "Translate only the headline. Keep the red pill: "
        "'Solar Inverter' → 'ソーラーインバーター'; the red pill 'Time Setting' → '時間設定'. "
        "Keep both products, the clock, mountains and panels. "
        "Do NOT change casing text (SPLIT PHASE INVERTER, HYBRID SOLAR INVERTER), the xindun logo or displays. "
        "Do not redesign."
    ),
    (1, 1): (
        "Wiring diagram of three hybrid inverters. Translate only these labels: "
        "Battery→バッテリー, Power Grid→電力系統, AC Loads→交流負荷, PV Array→太陽光アレイ. "
        + KEEP
    ),
    (1, 2): (
        "Wiring diagram of three hybrid inverters in split phase. Translate only these labels: "
        "Battery→バッテリー, Power Grid→電力系統, AC Loads→交流負荷, PV Array→太陽光アレイ. "
        + KEEP
    ),
    (1, 3): (
        "Three-phase parallel wiring diagram of three hybrid inverters. Translate only these labels: "
        "Battery→バッテリー, Power Grid→電力系統, AC Loads→交流負荷, PV Array→太陽光アレイ. "
        + KEEP
    ),
    (1, 4): (
        "Two-group split-phase parallel diagram marked P1 and P2. Translate only these labels: "
        "Battery→バッテリー, Power Grid→電力系統, AC Loads→交流負荷, PV Array→太陽光アレイ. "
        "Keep the P1 and P2 marks. " + KEEP
    ),
    (1, 5): (
        "Parallel wiring diagram of three inverters on a pale green background. Translate only these labels: "
        "Battery→バッテリー, Utility Grid→商用電源, Loads→負荷, PV Array→太陽光アレイ. "
        + KEEP
    ),
    (1, 6): (
        "Three-phase output parallel diagram. Translate only these labels: "
        "Battery→バッテリー, Utility Grid→商用電源, Loads→負荷, PV Array→太陽光アレイ. "
        + KEEP
    ),
    (2, 0): (
        "Studio banner of four inverters on pale blue blocks. Translate only the headline. "
        "Keep the green pill in the middle: 'Inverter' → 'インバーター'; "
        "the green pill 'Split Phase' → 'スプリットフェーズ'; 'Power Supply' → '電源'. "
        "Keep every product and the blocks. Do NOT change casing text "
        "(SPLIT PHASE INVERTER, HYBRID SOLAR INVERTER, Low Frequency Inverter Pure Sine Wave), "
        "the xindun logo or displays. Do not redesign."
    ),
    (2, 1): (
        "Single-inverter split-phase wiring diagram. Translate only these labels: "
        "Solar Panels→太陽光パネル, Battery→バッテリー, Power Grid→電力系統, AC Loads→交流負荷. "
        + KEEP
    ),
    (2, 2): (
        "Split-phase parallel wiring diagram of three hybrid inverters. Translate only these labels: "
        "Battery→バッテリー, Power Grid→電力系統, AC Loads→交流負荷, PV Array→太陽光アレイ. "
        + KEEP
    ),
    (2, 3): (
        "Blue inverter system diagram. Translate only these labels: "
        "Solar Panels→太陽光パネル, Utility Grid→商用電源, OR→または, Generator→発電機, "
        "Battery→バッテリー, AC OUTPUT→交流出力, AC Loads→交流負荷. "
        + KEEP
    ),
    (2, 4): (
        "Tower inverter system diagram. Translate only these labels: "
        "Solar Panels→太陽光パネル, Utility Grid→商用電源, OR→または, Generator→発電機, "
        "Battery→バッテリー, AC OUTPUT→交流出力, AC Loads→交流負荷. "
        "Do NOT change the casing line 'Low Frequency Inverter Pure Sine Wave'. " + KEEP
    ),
    (3, 0): (
        "Daylight banner of six inverters in front of a house with rooftop solar. "
        "Translate only the headline 'Sun Hybrid Inverter' → '太陽光ハイブリッドインバーター'. "
        "Keep every product, the house and the panels. Do NOT change casing text, "
        "the word INVERTER inside the green circle on the right-hand unit, the xindun logo, CE marks or displays. "
        "Do not redesign."
    ),
    (3, 1): (
        "System diagram around one round-display inverter. Translate only these labels: "
        "Solar Panels→太陽光パネル, Utility Grid→商用電源, OR→または, Generator→発電機, "
        "Uninterrupted Power Supply(Main output)→無停電電源（主出力）, "
        "Uninterrupted Power Supply(Second output)→無停電電源（副出力）, Battery→バッテリー. "
        "Do NOT change LiFePO4 Lithium Battery on the battery drawing. " + KEEP
    ),
    (3, 2): (
        "System diagram around an inverter with a green ring. Translate only these labels: "
        "Solar Panels→太陽光パネル, Utility Grid→商用電源, OR→または, Generator→発電機, "
        "Uninterrupted Power Supply(Main output)→無停電電源（主出力）, "
        "Uninterrupted Power Supply(Second output)→無停電電源（副出力）, Battery→バッテリー. "
        "Do NOT change LiFePO4 Lithium Battery on the battery drawing. " + KEEP
    ),
    (3, 3): (
        "System diagram around an inverter with a detachable panel. Translate only the outside labels: "
        "Solar Panels→太陽光パネル, Utility Grid→商用電源, OR→または, Generator→発電機, "
        "Uninterrupted Power Supply(Main output)→無停電電源（主出力）, "
        "Uninterrupted Power Supply(Second output)→無停電電源（副出力）, Battery→バッテリー. "
        "Do NOT change the word INVERTER on the green product circle or LiFePO4 Lithium Battery. " + KEEP
    ),
    (3, 4): (
        "Single-phase parallel diagram labeled Unit 1, Unit 2 and Unit 3. Translate only: "
        "Unit 1→ユニット1, Unit 2→ユニット2, Unit 3→ユニット3, "
        "Battery→バッテリー, Utility Grid→商用電源, Loads→負荷. " + KEEP
    ),
    (3, 5): (
        "Nine-inverter parallel diagram grouped as P1, P2 and P3. Translate only: "
        "Battery→バッテリー, Utility Grid→商用電源, Loads→負荷. Keep P1 P2 P3. " + KEEP
    ),
    (3, 6): (
        "Parallel expansion wiring diagram. Translate only: "
        "Battery→バッテリー, Utility Grid→商用電源, Loads→負荷, PV Array→太陽光アレイ. " + KEEP
    ),
    (3, 7): (
        "Split-phase output parallel diagram. Translate only: "
        "Battery→バッテリー, Utility Grid→商用電源, Loads→負荷, PV Array→太陽光アレイ. "
        "The small casing line under each xindun logo must stay exactly as printed "
        "(HYBRID SOLAR INVERTER or XINDUN SOLAR INVERTER). Do not replace it with XINDUN POWER. "
        + KEEP
    ),
    (3, 8): (
        "Three-phase output parallel diagram. Translate only: "
        "Battery→バッテリー, Utility Grid→商用電源, Loads→負荷, PV Array→太陽光アレイ. "
        "The small casing line under each xindun logo must stay exactly as printed. "
        "Do not replace it with XINDUN POWER. " + KEEP
    ),
    (4, 0): (
        "Factory banner with three tall inverters. Translate only the headline "
        "'What Can a 25KW Inverter Run?' → '25kWインバーターは何を動かせるか？'. "
        "Keep 25KW emphasized in orange as 25kW. Keep the three products and the factory interior. "
        "Do NOT change casing text (Low Frequency Inverter Pure Sine Wave), the xindun logo or displays. "
        "Do not redesign."
    ),
    (4, 1): (
        "Rear-view system diagram of a white tower inverter. Translate only the callout labels: "
        "Power Grid→電力系統, or→または, Generator→発電機, Solar Panels→太陽光パネル, "
        "Solar Controller→ソーラーコントローラ, RS232 (Optional)→RS232（オプション）, "
        "RS485 (Optional)→RS485（オプション）, Ground Line→アース線, Batteries→バッテリー, "
        "Rice cooker→炊飯器, Water dispenser→ウォーターサーバー, Electromagnetic furnace→電磁調理器, "
        "Refrigerator→冷蔵庫, AIR CONDITIONER→エアコン. " + KEEP
    ),
    (4, 2): (
        "System diagram of a low-frequency inverter feeding household loads. Translate only: "
        "Solar Panels→太陽光パネル, AC Input→交流入力, or→または, Generator→発電機, "
        "Battery→バッテリー, AC Output→交流出力, Laptop→ノートパソコン, Printer→プリンター, "
        "TV→テレビ, Fans→扇風機, Water pump→水ポンプ. "
        "Do NOT change casing text 'Low Frequency Inverter Pure Sine Wave'. " + KEEP
    ),
    (4, 3): (
        "Black three-phase inverter system diagram. Translate only the external callouts, not text printed on the metal chassis: "
        "INVERTER→インバーター, SOLAR PANELS→太陽光パネル, PV COMBINER→PV接続箱, "
        "SOLAR CONTROLLER→ソーラーコントローラ, 12V200Ah Battery→12V200Ahバッテリー, "
        "BATTERIES→バッテリー, A Phase→A相, B Phase→B相, C Phase→C相, "
        "3-PHASE LOADS→三相負荷, 1-PHASE LOADS→単相負荷, POWER GRID→電力系統, "
        "Earth Wire (GND)→アース線（GND）, BREAKER→ブレーカー. "
        "Leave BATTERY, AC INPUT, AC OUTPUT and PV INPUT printed on the chassis unchanged. " + KEEP
    ),
    (4, 5): (
        "Office photo collage with three green caption bars. Translate only those bars: "
        "Office→オフィス, Laboratory→実験室, Exhibition hall→展示ホール. "
        "Do NOT change the wall company name xindun GREEN POWER, the Chinese company name, "
        "Guangdong Xindun Power Technology Co., LTD, certificates, or any other sign. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091120331497.jpg",
            "alt_ja": "純正弦波オフグリッドソーラーインバーター",
            "title_ja": "純正弦波オフグリッドソーラーインバーター",
            "stem": "純正弦波オフグリッドソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ja": "純正弦波インバーター",
            "title_ja": "純正弦波インバーター",
            "stem": "純正弦波インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ja": "オフグリッドソーラーインバーター",
            "title_ja": "オフグリッドソーラーインバーター",
            "stem": "オフグリッドソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg",
            "alt_ja": "純正弦波インバーターHU",
            "title_ja": "純正弦波インバーターHU",
            "stem": "純正弦波インバーターHU",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg",
            "alt_ja": "オフグリッドインバーターHP",
            "title_ja": "オフグリッドインバーターHP",
            "stem": "オフグリッドインバーターHP",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125237036.jpg",
            "alt_ja": "オフグリッドインバーターLU",
            "title_ja": "オフグリッドインバーターLU",
            "stem": "オフグリッドインバーターLU",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125487765.jpg",
            "alt_ja": "純正弦波三相インバーター",
            "title_ja": "純正弦波三相インバーター",
            "stem": "純正弦波三相インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091126518485.jpg",
            "alt_ja": "オフグリッドソーラー発電機",
            "title_ja": "オフグリッドソーラー発電機",
            "stem": "オフグリッドソーラー発電機",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/15/202511150928484456.jpg",
            "alt_ja": "ソーラーインバーターの時間設定",
            "title_ja": "ソーラーインバーターの時間設定",
            "stem": "ソーラーインバーターの時間設定",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141154031704.jpg",
            "alt_ja": "単相並列のソーラーインバーター",
            "title_ja": "単相並列のソーラーインバーター",
            "stem": "単相並列のソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155069284.jpg",
            "alt_ja": "スプリットフェーズ並列インバーター",
            "title_ja": "スプリットフェーズ並列インバーター",
            "stem": "スプリットフェーズ並列インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155496791.jpg",
            "alt_ja": "三相並列インバーター",
            "title_ja": "三相並列インバーター",
            "stem": "三相並列インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141157382346.jpg",
            "alt_ja": "二相スプリットフェーズ並列インバーター",
            "title_ja": "二相スプリットフェーズ並列インバーター",
            "stem": "二相スプリットフェーズ並列インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141159513423.jpg",
            "alt_ja": "時間設定対応インバーターの並列",
            "title_ja": "時間設定対応インバーターの並列",
            "stem": "時間設定対応インバーターの並列",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141200562922.jpg",
            "alt_ja": "三相出力の並列ソーラーインバーター",
            "title_ja": "三相出力の並列ソーラーインバーター",
            "stem": "三相出力の並列ソーラーインバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/20251114142133mHRDbI.jpg",
            "alt_ja": "スプリットフェーズ電源",
            "title_ja": "スプリットフェーズ電源",
            "stem": "スプリットフェーズ電源",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141426036849.jpg",
            "alt_ja": "スプリットフェーズ電源インバーター",
            "title_ja": "スプリットフェーズ電源インバーター",
            "stem": "スプリットフェーズ電源インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141155069284.jpg",
            "alt_ja": "ハイブリッドインバーターのスプリットフェーズ電源",
            "title_ja": "ハイブリッドインバーターのスプリットフェーズ電源",
            "stem": "ハイブリッドインバーターのスプリットフェーズ電源",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141427125780.jpg",
            "alt_ja": "LSスプリットフェーズ電源インバーター",
            "title_ja": "LSスプリットフェーズ電源インバーター",
            "stem": "LSスプリットフェーズ電源インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141432533866.jpg",
            "alt_ja": "WFスプリットフェーズ給電インバーター",
            "title_ja": "WFスプリットフェーズ給電インバーター",
            "stem": "WFスプリットフェーズ給電インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/11/14/202511141433559083.jpg",
            "alt_ja": "スプリットフェーズ給電の導入事例",
            "title_ja": "スプリットフェーズ給電の導入事例",
            "stem": "スプリットフェーズ給電の導入事例",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301436325219.jpg",
            "alt_ja": "太陽光ハイブリッドインバーター",
            "title_ja": "太陽光ハイブリッドインバーター",
            "stem": "太陽光ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301437478088.jpg",
            "alt_ja": "太陽光パワーインバーター",
            "title_ja": "太陽光パワーインバーター",
            "stem": "太陽光パワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301438298106.jpg",
            "alt_ja": "太陽光インバーターHFP-C",
            "title_ja": "太陽光インバーターHFP-C",
            "stem": "太陽光インバーターHFP-C",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301439085755.jpg",
            "alt_ja": "太陽光ハイブリッドパワーインバーター",
            "title_ja": "太陽光ハイブリッドパワーインバーター",
            "stem": "太陽光ハイブリッドパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151138082598.jpg",
            "alt_ja": "並列の太陽光パワーインバーター",
            "title_ja": "並列の太陽光パワーインバーター",
            "stem": "並列の太陽光パワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/15/202410151159558052.jpg",
            "alt_ja": "三相出力の太陽光ハイブリッドインバーター",
            "title_ja": "三相出力の太陽光ハイブリッドインバーター",
            "stem": "三相出力の太陽光ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301453378424.jpg",
            "alt_ja": "並列太陽光インバーター",
            "title_ja": "並列太陽光インバーター",
            "stem": "並列太陽光インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301453241476.jpg",
            "alt_ja": "スプリットフェーズ出力の太陽光パワーインバーター",
            "title_ja": "スプリットフェーズ出力の太陽光パワーインバーター",
            "stem": "スプリットフェーズ出力の太陽光パワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301452362924.jpg",
            "alt_ja": "三相出力のハイブリッド太陽光インバーター",
            "title_ja": "三相出力のハイブリッド太陽光インバーター",
            "stem": "三相出力のハイブリッド太陽光インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301455232457.jpg",
            "alt_ja": "ハイブリッド太陽光インバーターの導入事例",
            "title_ja": "ハイブリッド太陽光インバーターの導入事例",
            "stem": "ハイブリッド太陽光インバーターの導入事例",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301415354090.jpg",
            "alt_ja": "25kWソーラーインバーター",
            "title_ja": "25kWソーラーインバーター",
            "stem": "25kWソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301418405169.jpg",
            "alt_ja": "WDシリーズ25kWインバーター",
            "title_ja": "WDシリーズ25kWインバーター",
            "stem": "WDシリーズ25kWインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311109218818.jpg",
            "alt_ja": "WFシリーズ25kWソーラーインバーター",
            "title_ja": "WFシリーズ25kWソーラーインバーター",
            "stem": "WFシリーズ25kWソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301419552617.jpg",
            "alt_ja": "HDSXシリーズ25kWソーラーパワーインバーター",
            "title_ja": "HDSXシリーズ25kWソーラーパワーインバーター",
            "stem": "HDSXシリーズ25kWソーラーパワーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301420539336.jpg",
            "alt_ja": "25kWインバーターの用途",
            "title_ja": "25kWインバーターの用途",
            "stem": "25kWインバーターの用途",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301421321541.jpg",
            "alt_ja": "インバーターメーカー",
            "title_ja": "インバーターメーカー",
            "stem": "インバーターメーカー",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/30/202510301422247905.jpg",
            "alt_ja": "インバーター充電器の工場",
            "title_ja": "インバーター充電器の工場",
            "stem": "インバーター充電器の工場",
        },
    ],
]

IMAGE_LOG: list[dict] = []


def run_duomi_fit(
    image_url: str,
    extra_prompt: str,
    stem: str,
    size: str,
    orig_wh: tuple[int, int],
    orig_path: Path,
    attempts: int = 3,
) -> Path | None:
    """Same Duomi edit as run_duomi, for originals whose nearest supported size is slightly off.

    Duomi only offers discrete ratios. A 750x851 diagram is 0.119 away from 1:1, so the
    strict 0.11 gate rejects every successful edit. Accept the nearest supported ratio when
    the picture still matches the original, then encode back to the original pixel size.
    """
    assert_ja_progress_current()
    prompt = f"{PROMPT_BASE} {extra_prompt}"
    final = OUT / f"{stem}.jpg"
    timeouts = [240, 600]
    requested = SIZE_RATIOS[size]
    for attempt in range(attempts):
        out_name = f"{stem}-try{attempt + 1}"
        timeout = str(timeouts[min(attempt, len(timeouts) - 1)])
        print(f"[duomi-fit] {stem} attempt={attempt + 1} size={size} timeout={timeout}", flush=True)
        cmd = [
            "python3",
            str(REPO / "scripts" / "duomi_image.py"),
            "--image-url",
            image_url,
            "--prompt",
            prompt,
            "--size",
            size,
            "--output-name",
            out_name,
            "--output-dir",
            "output/duomi/ja",
            "--max-kb",
            "0",
            "--print-json",
            "--timeout",
            timeout,
        ]
        p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
        combined_err = (p.stderr or "") + "\n" + (p.stdout or "")
        if "余额不足" in combined_err or "没有权限" in combined_err:
            print(f"[duomi-fit] API no balance/permission: {combined_err[-300:]}", flush=True)
            return None
        files: list[str] = []
        for line in (p.stdout or "").splitlines()[::-1]:
            line = line.strip()
            if line.startswith("{"):
                try:
                    files = json.loads(line).get("files") or []
                    break
                except Exception:  # noqa: BLE001
                    pass
            if line.startswith("SUCCESS:"):
                files = [line.split("SUCCESS:", 1)[1].strip()]
                break
        if not files:
            print(f"[duomi-fit] no files stderr={(p.stderr or '')[-400:]}", flush=True)
            time.sleep(3)
            continue
        raw = Path(files[0])
        if not raw.exists():
            print(f"[duomi-fit] output missing: {raw}", flush=True)
            time.sleep(3)
            continue
        try:
            with Image.open(raw) as chk:
                cw, ch = chk.size
            got = cw / ch if ch else 1.0
            if abs(got - requested) > 0.08:
                print(f"[duomi-fit] reject unexpected size {cw}x{ch} vs requested {size}", flush=True)
                time.sleep(3)
                continue
            orig_ratio = orig_wh[0] / orig_wh[1]
            if abs(got - orig_ratio) > 0.2:
                print(f"[duomi-fit] reject ratio {cw}x{ch} vs {orig_wh}", flush=True)
                time.sleep(3)
                continue
            diff_score = image_mean_diff(orig_path, raw, orig_wh[0], orig_wh[1])
            if diff_score > 42.0:
                print(f"[duomi-fit] reject redesign diff={diff_score:.2f}", flush=True)
                time.sleep(3)
                continue
            print(
                f"[duomi-fit] accept {cw}x{ch} diff={diff_score:.2f} "
                f"orig_delta={abs(got - orig_ratio):.3f}",
                flush=True,
            )
            from page1_ja_images import encode_jpeg

            encode_jpeg(raw, final, orig_wh[0], orig_wh[1], 100)
        except Exception as exc:  # noqa: BLE001
            print(f"[duomi-fit] layout/compress failed: {exc}", flush=True)
            time.sleep(3)
            continue
        if final.exists() and final.stat().st_size > 0:
            return final
    return None


def prepare_all() -> list[list[dict]]:
    assert_ja_progress_current()
    prepared_all: list[list[dict]] = []
    src_cache: dict[str, dict] = {}
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
            if (not reused) and need_duomi and im["src"] in src_cache:
                cached = src_cache[im["src"]]
                if tuple(cached["orig_wh"]) == tuple(orig_wh):
                    final = tagged
                    final.write_bytes(Path(cached["final"]).read_bytes())
                    method = "duomi-src-reuse"
                    duomi_path = cached.get("duomi_path")
                    reused = True
                    print(f"[img] src-reuse {tagged.name}", flush=True)
            if reused:
                pass
            elif need_duomi:
                size = size_for(*orig_wh)
                orig_ratio = orig_wh[0] / orig_wh[1] if orig_wh[1] else 1.0
                gap = abs(SIZE_RATIOS[size] - orig_ratio)
                runner = run_duomi_fit if gap > 0.105 else run_duomi
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
            if need_duomi:
                src_cache[im["src"]] = {
                    "final": str(final),
                    "duomi_path": duomi_path,
                    "orig_wh": orig_wh,
                }
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
