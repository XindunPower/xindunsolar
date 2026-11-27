#!/usr/bin/env python3
"""Prepare page 14 Japanese images.

Duomi gpt-image-2 only for English marketing headlines and diagram captions.
Listing crops are the WordPress featured images. Voltage labels, installation
collages, and product studio shots are compressed and renamed. Product casing
text stays unchanged. Outputs stay in output/duomi/ja/.
"""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
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
PAGE_NUM = 14

KEEP_CASE = (
    " Do NOT change product casing text, the xindun logo, CE marks, ISO marks, displays, "
    "buttons, or model markings. Do not add or remove products. Do not redesign. "
    "Use Japanese characters for the translated overlay. Do not use Chinese characters. "
    "Do not leave the original English headline. "
    "Do not write the katakana word インバータ or インバーター on this image."
)

MC4_HEAD = (
    "Translate only the two-line blue headline. Keep MC4 and PV in Latin letters. "
    "Line 1: 'What Is MC4 PV Connector' → 'MC4 PVコネクタとは'. "
    "Line 2: 'for Solar Inverters?' → 'ソーラー用？'. "
    "Shrink the type only enough to stay on those two lines. "
    "Do NOT change the xindun logo, HYBRID SOLAR INVERTER, the display, buttons, CE marks, "
    "or text printed on the product. Do not move the panels, inverter, cables or connectors."
    + KEEP_CASE
)

COMP_HEAD = (
    "Translate only the headline. Keep the green pill behind the middle phrase. "
    "Line 1, black: 'What Is the Inverter' → '出力を補う'. "
    "Green pill: 'Output Compensation' → '出力補償'. "
    "Black text after the pill: 'Function?' → '機能とは？'. "
    "If a word is cut off by the crop, translate only the fully visible words and do not invent the rest. "
    "Do NOT change the xindun logo, HYBRID SOLAR INVERTER, the display, RGB ring, buttons or CE marks. "
    "Do not move the inverter, wall, floor, mountains or panels."
    + KEEP_CASE
)

OVER_HEAD = (
    "Translate only the one-line headline. Keep '過負荷保護' in green and the rest in white. "
    "White 'What Is' → '機器の'. "
    "Green 'Overload Protection' → '過負荷保護'. "
    "White 'for Inverter?' → 'とは？'. "
    "Do NOT change the xindun logo, HYBRID SOLAR INVERTER, the display, buttons or CE marks. "
    "Do not move the inverter or the shield."
    + KEEP_CASE
)

MODE_HEAD = (
    "Translate only the three-line headline. Keep the middle line green. "
    "Line 1, black: 'What Are the' → 'ハイブリッドの'. "
    "Line 2, green: 'Three Working Modes' → '3つの動作モード'. "
    "Line 3, black: 'of Hibrid Invertor?' → 'とは？'. "
    "Keep three lines. Shrink the type so each line stays on its own line. "
    "Do NOT change the xindun logo, HYBRID SOLAR INVERTER, displays, buttons, RGB ring or CE marks. "
    "Do not move the three inverters or the pedestals."
    + KEEP_CASE
)

PWM_HEAD = (
    "Translate only the two-line black headline. Keep PWM and MPPT in Latin letters. "
    "Line 1: 'PWM vs MPPT Inverter' → 'PWMとMPPT'. "
    "Line 2: 'What's the Difference?' → '違いは何か？'. "
    "Do NOT change text printed on the product casings, including MPPT Solar Charge Controller, SOLAR, "
    "HYBRID SOLAR INVERTER, Low Frequency PV Inverter, the xindun logo, displays, buttons or CE marks. "
    "Do not move the products or the pedestal."
    + KEEP_CASE
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a 4:3 crop of a marketing banner: two solar panels, a white hybrid inverter, "
        "coils of blue and red cable, and four black MC4 connectors, over a pale blue snowy background. "
        + MC4_HEAD
    ),
    (0, 1): (
        "This is a wide marketing banner: two solar panels on the left, a white hybrid inverter, "
        "coils of blue and red cable, and four black MC4 connectors on the right, over a pale blue snowy background. "
        + MC4_HEAD
    ),
    (0, 3): (
        "This is a white exploded-view diagram of a black MC4 connector. Translate only the English labels. "
        "Keep the connector parts, red dots, leader lines and white background. "
        "Title: 'Product Explanation' → '製品の説明'. "
        "The subtitle repeats 'High quality' by mistake. Render one short subtitle: "
        "'High quality High quality High density' → '高品質・高密度'. Do not repeat 高品質. "
        "'Self locking design' → '自己ロック構造'. "
        "'Inner core (female)' → '内部コア（メス）'. "
        "'Inner core (male)' → '内部コア（オス）'. "
        "'Locking teeth' → 'ロック爪'. "
        "'Tighten the cap' → 'キャップを締める'. "
        "'Male plug' → 'オスプラグ'. "
        "Both 'Female plug' labels → 'メスプラグ'. "
        "'Waterproof pad' → '防水パッキン'. "
        "Do not move any part. Do not redesign. Use Japanese characters. Do not use Chinese characters."
    ),
    (0, 4): (
        "This is a close-up photo of a grey connector heated by a lighter flame, held in white gloves. "
        "Translate only the English overlay. Keep the photo, flame, gloves, and any molded text on the connector, "
        "including 'Do not disconnect under load'. "
        "Headline: 'Product real shot demonstration effect' → '製品の実写デモ'. "
        "Caption line 1: 'Flame retardant material, no fear of high' → '難燃材料で、'. "
        "Caption line 2: 'temperature generated by the ammeter' → '電流計の高温も恐れない'. "
        "Do not move the connector or the flame. Do not redesign. Use Japanese characters. Do not use Chinese characters."
    ),
    (1, 0): (
        "This is a 4:3 crop of a banner: a white inverter on a beige wall at left, "
        "an open view of mountains and solar panels at right. " + COMP_HEAD
    ),
    (1, 1): (
        "This is a wide banner: a white inverter on a beige wall at left, "
        "an open view of mountains and solar panels at right. " + COMP_HEAD
    ),
    (2, 0): (
        "This is a 4:3 crop of a dark-blue banner: a white hybrid inverter centered on a glowing blue shield. "
        + OVER_HEAD
    ),
    (2, 1): (
        "This is a dark-blue banner: a white hybrid inverter centered on a glowing blue shield. "
        + OVER_HEAD
    ),
    (3, 0): (
        "This is a 4:3 crop of a pale studio banner with three white inverters on round pedestals. "
        + MODE_HEAD
    ),
    (3, 1): (
        "This is a pale studio banner with three white inverters on round pedestals. "
        + MODE_HEAD
    ),
    (4, 0): (
        "This is a 4:3 crop of a pale studio banner with a row of inverters and a black cabinet on the right. "
        + PWM_HEAD
    ),
    (4, 1): (
        "This is a pale studio banner with a row of inverters and a black cabinet on the right. "
        + PWM_HEAD
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/20250702105258ub1UGY.jpg",
            "alt_ja": "ソーラーインバーター用MC4 PVコネクタ",
            "title_ja": "ソーラーインバーター用MC4 PVコネクタ",
            "stem": "ソーラーインバーター用MC4-PVコネクタ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/202507021053327737.jpg",
            "alt_ja": "ソーラーインバーター用MC4 PVコネクタの全体",
            "title_ja": "ソーラーインバーター用MC4 PVコネクタの全体",
            "stem": "ソーラーインバーター用MC4-PVコネクタの全体",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/30/202506301451375218.jpg",
            "alt_ja": "直流1000Vと1500VのMC4コネクタ",
            "title_ja": "直流1000Vと1500VのMC4コネクタ",
            "stem": "直流1000Vと1500VのMC4コネクタ",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/30/202506301454595150.jpg",
            "alt_ja": "MC4 PVコネクタの構造",
            "title_ja": "MC4 PVコネクタの構造",
            "stem": "MC4-PVコネクタの構造",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/30/202506301455514391.jpg",
            "alt_ja": "インバーターコネクタの難燃材料",
            "title_ja": "インバーターコネクタの難燃材料",
            "stem": "インバーターコネクタの難燃材料",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/30/202506301456493159.jpg",
            "alt_ja": "MC4 PVコネクタの接続",
            "title_ja": "MC4 PVコネクタの接続",
            "stem": "MC4-PVコネクタの接続",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/20250702105126A4d1lO.jpg",
            "alt_ja": "インバーターの出力補償機能",
            "title_ja": "インバーターの出力補償機能",
            "stem": "インバーターの出力補償機能",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/202507021051418037.jpg",
            "alt_ja": "インバーター出力補償の全体",
            "title_ja": "インバーター出力補償の全体",
            "stem": "インバーター出力補償の全体",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/20250702104930Th3YWm.jpg",
            "alt_ja": "インバーターの過負荷保護",
            "title_ja": "インバーターの過負荷保護",
            "stem": "インバーターの過負荷保護",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/202507021049481089.jpg",
            "alt_ja": "インバーター過負荷保護の全体",
            "title_ja": "インバーター過負荷保護の全体",
            "stem": "インバーター過負荷保護の全体",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/20250702104637g2hq6K.jpg",
            "alt_ja": "ハイブリッドインバーターの3つの動作モード",
            "title_ja": "ハイブリッドインバーターの3つの動作モード",
            "stem": "ハイブリッドインバーターの3つの動作モード",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/02/202507021046541869.jpg",
            "alt_ja": "ハイブリッドインバーターの動作モード全体",
            "title_ja": "ハイブリッドインバーターの動作モード全体",
            "stem": "ハイブリッドインバーターの動作モード全体",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/16/20250616161657hCbjYp.jpg",
            "alt_ja": "PWMとMPPTインバーターの違い",
            "title_ja": "PWMとMPPTインバーターの違い",
            "stem": "PWMとMPPTインバーターの違い",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/16/202506161616217751.jpg",
            "alt_ja": "PWMとMPPTインバーターの比較",
            "title_ja": "PWMとMPPTインバーターの比較",
            "stem": "PWMとMPPTインバーターの比較",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ja": "HFPのMPPTハイブリッドインバーター",
            "title_ja": "HFPのMPPTハイブリッドインバーター",
            "stem": "HFPのMPPTハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ja": "HFP-CのMPPTハイブリッドインバーター",
            "title_ja": "HFP-CのMPPTハイブリッドインバーター",
            "stem": "HFP-CのMPPTハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757379506.jpg",
            "alt_ja": "MPPT付きLF低周波ソーラーインバーター",
            "title_ja": "MPPT付きLF低周波ソーラーインバーター",
            "stem": "MPPT付きLF低周波ソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211758136722.jpg",
            "alt_ja": "ESS-LiのMPPTソーラー発電機",
            "title_ja": "ESS-LiのMPPTソーラー発電機",
            "stem": "ESS-LiのMPPTソーラー発電機",
        },
    ],
]

IMAGE_LOG: list[dict] = []


def prepare_one(article_idx: int, img_idx: int, im: dict, stem: str) -> dict:
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
            f"[img] a{article_idx}_i{img_idx} size={size} gap={gap:.3f} runner={runner.__name__}",
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
        "article": article_idx,
        "img": img_idx,
        "local": final,
        "alt_ja": im["alt_ja"],
        "title_ja": im["title_ja"],
        "src_orig": im["src"],
        "method": method,
        "duomi_path": duomi_path,
        "orig_wh": orig_wh,
    }
    print(
        f"[img] a{article_idx}_i{img_idx} method={method} -> {final.name} "
        f"{final.stat().st_size}b {orig_wh}",
        flush=True,
    )
    return entry


def prepare_all() -> list[list[dict]]:
    assert_ja_progress_current()
    jobs = []
    for article_idx, images in enumerate(IMAGE_SOURCES):
        for img_idx, im in enumerate(images):
            stem = unique_stem(im["stem"])
            jobs.append((article_idx, img_idx, im, stem))

    prepared_map: dict[tuple[int, int], dict] = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(prepare_one, article_idx, img_idx, im, stem): (article_idx, img_idx)
            for article_idx, img_idx, im, stem in jobs
        }
        for fut in as_completed(futures):
            entry = fut.result()
            prepared_map[(entry["article"], entry["img"])] = entry

    prepared_all: list[list[dict]] = []
    IMAGE_LOG.clear()
    for article_idx, images in enumerate(IMAGE_SOURCES):
        prepared = []
        for img_idx, _im in enumerate(images):
            entry = prepared_map[(article_idx, img_idx)]
            IMAGE_LOG.append(
                {
                    "article": article_idx,
                    "img": img_idx,
                    **{
                        k: (str(v) if k == "local" else list(v) if k == "orig_wh" else v)
                        for k, v in entry.items()
                        if k not in {"article", "img"}
                    },
                }
            )
            prepared.append(entry)
        prepared_all.append(prepared)
    Path(f"/tmp/page{PAGE_NUM}_ja_image_log.json").write_text(
        json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return prepared_all


if __name__ == "__main__":
    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
