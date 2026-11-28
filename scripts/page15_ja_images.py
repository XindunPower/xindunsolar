#!/usr/bin/env python3
"""Prepare page 15 Japanese images.

Duomi gpt-image-2 only for English marketing headlines and diagram captions.
Listing crops are the WordPress featured images. Product casing text stays
unchanged. Outputs stay in output/duomi/ja/.
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
PAGE_NUM = 15

NO_INV = (
    " Use Japanese characters for the translated overlay. Do not use Chinese characters. "
    "Do not write the katakana インバータ or インバーター. "
    "Do not leave the original English overlay. Do not add or remove objects. Do not redesign."
)

KEEP_CASE = (
    " Do NOT change product casing text, the xindun logo, CE marks, displays, buttons, "
    "terminal silkscreen (SOLAR, BATTERY, DC LOAD, TEMP SENSOR, RS485, PV), "
    "model numbers, voltage numbers, 12V/250Ah, or the words HYBRID SOLAR INVERTER, "
    "MPPT SOLAR CONTROLLER, MPPT Solar Charge Controller, PWM Solar Controller, "
    "LiFePO4 Lithium Battery, and INVERTER printed inside a round display. "
    "Do not translate the company name xindun or GREENPOWER."
    + NO_INV
)

UPS_HEAD = (
    "Translate only the white headline on the translucent green bar at the left. Keep four lines. "
    "Line 1: 'How to Choose the' → '産業用に最適な'. "
    "Line 2: 'Best UPS Backup' → 'UPSバックアップ'. "
    "Line 3: 'Power System for' → '電源システムの'. "
    "Line 4: 'Industrial?' → '選び方は？'. "
    "Keep UPS in Latin letters. Do not move the cabinets, display, plant, sky or ground."
    + NO_INV
)

MPPT_HEAD = (
    "Translate only the blue two-line headline. Keep MPPT in Latin letters. "
    "Line 1: 'How to Properly Size MPPT' → 'MPPTの容量選定'. "
    "Line 2: 'Solar Charge Controller?' → '充電コントローラ'. "
    "Do NOT change text printed on the orange and white products, including "
    "MPPT Solar Charge Controller, displays, the xindun logo, fans or terminals. "
    "Do not move the products or the platform."
    + NO_INV
)

HYBRID_HEAD = (
    "Translate only the large one-line headline. "
    "'HIGHBREED INVERTER' → 'ハイブリッド電源'. "
    "Do NOT change text on the four white products, including INVERTER inside the round display, "
    "HYBRID SOLAR INVERTER, the xindun logo, CE marks, or model numbers such as 1.2 and 10. "
    "Do not move the products or the blue blocks."
    + NO_INV
)

CHARGE_HEAD = (
    "Translate only the two-line green headline and the English diagram labels. "
    "Line 1: 'How Many Charging Modes Does Hybrid Inverter Have?' → '充電モードはいくつある？'. "
    "Line 2: 'How To Use Charging Priority?' → '充電優先の使い方は？'. "
    "'Solar Panels' → '太陽光パネル'. "
    "'Power Grid' → '電力系統'. "
    "'Inverter' under the unit → '変換装置'. "
    "'Battery' → 'バッテリー'. "
    "Keep the blue, red and yellow arrows, the sun, panels, utility pole and battery drawing. "
    "Do NOT change HYBRID SOLAR INVERTER or the xindun logo printed on the white unit."
    + NO_INV
)

HFP_LABELS = (
    "Translate only the English diagram labels. Keep arrows, colors and the drawing. "
    "'Solar Panels' → '太陽光パネル'. "
    "'Battery' or 'Batteries' → 'バッテリー'. "
    "The caption above the white unit, 'On&Off Grid Hybrid Solar Inverter' → '系統連系・オフグリッド両用'. "
    "'Power Grid' → '電力系統'. "
    "'Electric Meter' → '電力量計'. "
    "The small word 'or' → 'または'. "
    "'Generator' → '発電機'. "
    "'AC Loads' → '交流負荷'. "
    "'Uninterrupted Power Supply(Main output)' and 'Uninterrupted Power Supply(Main Output)' → '無停電（主出力）'. "
    "'Uninterrupted Power Supply(Second output)' and 'Uninterrupted Power Supply(Second Output)' → '無停電（副出力）'. "
    "Do NOT change HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery, INVERTER on the round display, "
    "the xindun logo, CE marks, or the display screen."
    + NO_INV
)

HOUSE_LABELS = (
    "This is a house cutaway wiring diagram. Translate only the English labels. "
    "Keep the sun, roof panels, rooms, sofa, television, washing machine, utility pole and colored wires. "
    "'Solar Panels' → '太陽光パネル'. "
    "'Solar Controller' → 'ソーラーコントローラ'. "
    "'Battery' → 'バッテリー'. "
    "'Inverter' → '変換装置'. "
    "'AC Loads' → '交流負荷'. "
    "'Power Grid' → '電力系統'. "
    "Keep the letters N and L. Do not translate the xindun logo or GREENPOWER."
    + NO_INV
)

WONDER_LABELS = (
    "This is a wiring photo of an MPPT charge controller. Translate only the callout labels under the drawings. "
    "'DC Load' → '直流負荷'. "
    "'Solar Panels' → '太陽光パネル'. "
    "'Batteries' → 'バッテリー'. "
    "'Inverter' → '変換装置'. "
    "On each battery, keep the numerals 12V/250Ah and translate only the word Battery to バッテリー. "
    "Do NOT change silkscreen on the controller: MPPT SOLAR CONTROLLER, MPPT Solar Charge Controller, "
    "SOLAR, BATTERY, DC LOAD, TEMP SENSOR, RS485, PV, SET, MENU, the xindun logo, or the display digits."
    + NO_INV
)

KY1_LABELS = (
    "This is a wiring diagram of a black PWM controller above a blue inverter. "
    "Translate only the English callout labels. "
    "'Solar Panel' → '太陽光パネル'. "
    "'Battery' → 'バッテリー'. "
    "'Dc Load' → '直流負荷'. "
    "'Inverter' → '変換装置'. "
    "'House Loads' → '家庭負荷'. "
    "'Office Equipment' → '事務機器'. "
    "'Industrial equipment' → '産業機器'. "
    "Do NOT change text printed on the black controller, including PWM Solar Controller, "
    "or text on the blue inverter. Keep the red wires and the three small photos."
    + NO_INV
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a 4:3 crop of a marketing photo: a black UPS cabinet and a battery cabinet "
        "on wheels, in an industrial plant yard. " + UPS_HEAD
    ),
    (0, 1): (
        "This is a wide marketing photo: a black UPS cabinet and a battery cabinet "
        "on wheels, in an industrial plant yard. " + UPS_HEAD
    ),
    (1, 0): (
        "This is a 4:3 crop of a studio banner: orange and white MPPT charge controllers "
        "on a pale blue platform under a cloudy sky. " + MPPT_HEAD
    ),
    (1, 1): (
        "This is a wide studio banner: orange and white MPPT charge controllers "
        "on a pale blue platform under a cloudy sky. " + MPPT_HEAD
    ),
    (2, 0): (
        "This is a 4:3 crop of a studio banner: four white inverters on blue blocks. " + HYBRID_HEAD
    ),
    (2, 1): (
        "This is a wide studio banner: four white inverters on blue blocks. " + HYBRID_HEAD
    ),
    (2, 2): (
        "This is a white-background wiring diagram. A large white hybrid inverter is in the center, "
        "solar panels and a battery on the left, a power grid, meter, generator and AC loads on the right. "
        + HFP_LABELS
    ),
    (2, 3): (
        "This is a white-background wiring diagram of a dual-output hybrid inverter. "
        "Solar panels and batteries are on the left. The right side has a power grid, meter, generator, "
        "AC loads, and two uninterrupted-power labels for the main and second outputs. " + HFP_LABELS
    ),
    (2, 4): (
        "This is a white-background wiring diagram. The center inverter has a large black circle "
        "with a green ring. Solar panels and a battery are on the left. The right side has a power grid, "
        "meter, generator, AC loads, and main/second output labels. " + HFP_LABELS
    ),
    (2, 5): (
        "This is a white-background wiring diagram. The center inverter has a black vertical handle "
        "and the word INVERTER on its round display. Solar panels and a battery are on the left. "
        "The right side has a power grid, meter, generator, AC loads, and main/second output labels. "
        + HFP_LABELS
    ),
    (3, 0): (
        "This is a 4:3 crop of a pale-green diagram: solar panels, a utility pole, a white inverter "
        "with a green ring, a sun, and a red battery, joined by colored arrows. " + CHARGE_HEAD
    ),
    (3, 1): (
        "This is a wide pale-green diagram: solar panels, a utility pole, a white inverter "
        "with a green ring, a sun, and a red battery, joined by colored arrows. " + CHARGE_HEAD
    ),
    (4, 0): (
        "This is a 4:3 crop of a house cutaway: solar panels on the roof, an orange controller, "
        "a battery, a white inverter, and appliances inside, with a utility pole on the right. " + HOUSE_LABELS
    ),
    (4, 1): (
        "This is a wide house cutaway: solar panels on the roof, an orange controller, "
        "a battery, a white inverter, and appliances inside, with a utility pole on the right. " + HOUSE_LABELS
    ),
    (4, 2): (
        "An orange and black MPPT controller is wired to solar panels, four batteries, a light bulb "
        "and a blue inverter. " + WONDER_LABELS
    ),
    (4, 3): (
        "A white MPPT controller is wired to solar panels, four batteries, a light bulb and a blue inverter. "
        + WONDER_LABELS
    ),
    (4, 4): (
        "A black PWM controller is wired to a solar panel, a battery and a light bulb, then down to a blue "
        "inverter and three small photos of house, office and industrial loads. " + KY1_LABELS
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/20/20250620140958alUhBO.jpg",
            "alt_ja": "産業用に最適なUPSバックアップ電源システムの選び方",
            "title_ja": "産業用に最適なUPSバックアップ電源システムの選び方",
            "stem": "産業用に最適なUPSバックアップ電源システムの選び方",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/20/202506201409218862.jpg",
            "alt_ja": "産業用に最適なUPS",
            "title_ja": "産業用に最適なUPS",
            "stem": "産業用に最適なUPS",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/20/20250620140820q9HpxF.jpg",
            "alt_ja": "MPPTソーラー充電コントローラの容量選定",
            "title_ja": "MPPTソーラー充電コントローラの容量選定",
            "stem": "MPPTソーラー充電コントローラの容量選定",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/20/202506201407508434.jpg",
            "alt_ja": "MPPTソーラー充電コントローラの容量",
            "title_ja": "MPPTソーラー充電コントローラの容量",
            "stem": "MPPTソーラー充電コントローラの容量",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/11/20250611142901QRCcjP.jpg",
            "alt_ja": "ハイブリッドインバーターとは",
            "title_ja": "ハイブリッドインバーターとは",
            "stem": "ハイブリッドインバーターとは",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/11/202506111429238620.jpg",
            "alt_ja": "ハイブリッドインバーター",
            "title_ja": "ハイブリッドインバーター",
            "stem": "ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/12/16/202412161348304040.png",
            "alt_ja": "HFPハイブリッドインバーターの構成",
            "title_ja": "HFPハイブリッドインバーターの構成",
            "stem": "HFPハイブリッドインバーターの構成",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/11/202506111433272766.png",
            "alt_ja": "HFP-Sハイブリッドインバーターの構成",
            "title_ja": "HFP-Sハイブリッドインバーターの構成",
            "stem": "HFP-Sハイブリッドインバーターの構成",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/20/202505201734324427.png",
            "alt_ja": "HFP-Cソーラーハイブリッドインバーターの構成",
            "title_ja": "HFP-Cソーラーハイブリッドインバーターの構成",
            "stem": "HFP-Cソーラーハイブリッドインバーターの構成",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/02/20/202502201531002662.png",
            "alt_ja": "HFP-Eハイブリッドインバーターの構成",
            "title_ja": "HFP-Eハイブリッドインバーターの構成",
            "stem": "HFP-Eハイブリッドインバーターの構成",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/02/20250602114542Nz5HYA.jpg",
            "alt_ja": "ハイブリッドソーラーインバーターの充電モード",
            "title_ja": "ハイブリッドソーラーインバーターの充電モード",
            "stem": "ハイブリッドソーラーインバーターの充電モード",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/02/202506021144221391.jpg",
            "alt_ja": "ソーラーインバーターの充電モード",
            "title_ja": "ソーラーインバーターの充電モード",
            "stem": "ソーラーインバーターの充電モード",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/30/20250530170800WRqQ4J.jpg",
            "alt_ja": "ソーラー充電コントローラの働き",
            "title_ja": "ソーラー充電コントローラの働き",
            "stem": "ソーラー充電コントローラの働き",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/28/202505281034426fU0XN.jpg",
            "alt_ja": "充電コントローラの家屋配線",
            "title_ja": "充電コントローラの家屋配線",
            "stem": "充電コントローラの家屋配線",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/27/202505271638331976.jpg",
            "alt_ja": "Wonder1のMPPTソーラーコントローラ配線",
            "title_ja": "Wonder1のMPPTソーラーコントローラ配線",
            "stem": "Wonder1のMPPTソーラーコントローラ配線",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/27/202505271639203692.jpg",
            "alt_ja": "Wonder2のMPPTソーラーコントローラ配線",
            "title_ja": "Wonder2のMPPTソーラーコントローラ配線",
            "stem": "Wonder2のMPPTソーラーコントローラ配線",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/05/27/202505271640059587.jpg",
            "alt_ja": "KY1のPWMソーラーコントローラ配線",
            "title_ja": "KY1のPWMソーラーコントローラ配線",
            "stem": "KY1のPWMソーラーコントローラ配線",
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
