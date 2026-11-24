#!/usr/bin/env python3
"""Prepare page 11 Japanese images.

All five heroes carry English marketing or diagram overlay text, so each one
goes through Duomi gpt-image-2. Outputs stay in output/duomi/ja/.
Marketing edits that fail layout checks are discarded and retried from the
original. They are not replaced by drawing text onto the original.
The 750x868 refrigerator banner is farther than 0.11 from the nearest Duomi
ratio, so it uses run_duomi_fit and is written back to the original pixel size.
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
PAGE_NUM = 11

KEEP_CASE = (
    " Do NOT change product casing text, the xindun logo, CE, ISO, displays, "
    "or model markings. Do not add or remove products. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a portrait kitchen scene: a dark four-door refrigerator on the left, "
        "a white wall inverter and a white floor battery on the right, wood slat wall, "
        "and colored wires marked N and L. Translate only the three-line beige headline "
        "at the top to Japanese, keeping three centered lines and the same beige color. "
        "Line 1: 'CAN I RUN A REFRIGERATOR' → '冷蔵庫は'. "
        "Line 2: 'ON A 1500W PURE SINE WAVE' → '1500W純正弦波インバーターで'. "
        "Line 3: 'INVERTER?' → '動かせるか？'. "
        "Keep 1500W as Latin digits. Keep the letters N and L, the plus and minus marks, "
        "and every wire color. Do NOT change HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery, "
        "51.2V / 280Ah / 14.3kWh, the xindun logo, or the CE mark. "
        "Do not move the refrigerator, inverter, battery, cabinets, or window."
        + KEEP_CASE
    ),
    (1, 0): (
        "This is a dark wiring diagram with one white split-phase inverter in the center. "
        "Translate only the overlay labels to Japanese. Keep the green title bar. "
        "White headline: 'What Is the Best' → '最も適したのは'. "
        "Green bar: 'Split Phase Solar Inverter?' → 'スプリットフェーズソーラーインバーターは？'. "
        "Shrink the green-bar type only enough to stay inside the existing bar. "
        "'Solar Panels' → '太陽光パネル'; 'Battery' → 'バッテリー'; "
        "'Power Grid' → '電力系統'; 'AC Loads' → 'AC負荷'. "
        "Keep L1, L2, N, 120V, 240V, every arrow, wire color, solar panel, pylon, "
        "appliance icons, and the small battery photo. "
        "Do NOT change SPLIT PHASE INVERTER or LiFePO4 Lithium Battery printed on the casings, "
        "the xindun logo, or the display. Do not redesign."
    ),
    (2, 0): (
        "This is a product lineup on grass under a blue sky, with solar panels behind the units. "
        "Translate only the two-line headline. Keep the green emphasis on the product name "
        "and the black color of the remaining words. "
        "Line 1: 'Can Low Frequency Solar Inverter' → '低周波ソーラーインバーターは', "
        "with '低周波ソーラーインバーター' in green and 'は' in black. "
        "Line 2: 'Be Used Directly Without Battery?' → 'バッテリーなしで直接使えるか？' in black. "
        "Keep every inverter, battery, solar panel, the grass, sky, and flowers. "
        "Do NOT change casing text such as SPLIT PHASE INVERTER, Low Frequency, "
        "LiFePO4 Lithium Battery, or the xindun logo. Do not redesign."
        + KEEP_CASE
    ),
    (3, 0): (
        "This is a daylight banner: two white low-frequency inverters in front of a solar field. "
        "Translate only the headline. Keep line 1 in white and line 2 inside the existing blue pill. "
        "Line 1: 'Why Does the Low Frequency Inverter' → '低周波インバーターに'. "
        "Line 2, white text in the blue pill: 'Have No Bypass Output?' → 'バイパス出力がないのはなぜ？'. "
        "Widen the pill only enough for the Japanese line. Do not move either inverter. "
        "Do NOT change 'Low Frequency PV Inverter' printed on the casings, the xindun logo, "
        "CE marks, displays, or the solar panels, sky, and sand. Do not redesign."
        + KEEP_CASE
    ),
    (4, 0): (
        "This is a light-gray studio banner: one white hybrid inverter on a round pedestal, "
        "a blue current icon on the left and a blue waveform icon on the right. "
        "Translate only the overlay text to Japanese. Keep the two-line headline, "
        "the blue letters, and the white outline. "
        "Line 1: 'WHAT IS THE ROLE OF THE INVERTER'S' → 'インバーターの商用入力電流と'. "
        "Line 2: 'MAINS INPUT CURRENT AND INPUT POWER?' → '入力電力の役割とは？'. "
        "Left label: 'INPUT CURRENT' → '入力電流'. Right label: 'INPUT POWER' → '入力電力'. "
        "Keep the letter A inside the left icon and the waveform graphic. "
        "Do NOT change HYBRID SOLAR INVERTER, the xindun logo, CE, ISO, the display, "
        "or the pedestal. Do not redesign."
        + KEEP_CASE
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/30/202508301716567704.jpg",
            "alt_ja": "1500W純正弦波インバーター",
            "title_ja": "1500W純正弦波インバーター",
            "stem": "1500W純正弦波インバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/202508251151214665.jpg",
            "alt_ja": "南米のスプリットフェーズソーラーインバーター",
            "title_ja": "南米のスプリットフェーズソーラーインバーター",
            "stem": "南米のスプリットフェーズソーラーインバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/202508251457528554.jpg",
            "alt_ja": "バッテリーなしの低周波ソーラーインバーター",
            "title_ja": "バッテリーなしの低周波ソーラーインバーター",
            "stem": "バッテリーなしの低周波ソーラーインバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/25/202508251146107503.jpg",
            "alt_ja": "低周波インバーターの出力",
            "title_ja": "低周波インバーターの出力",
            "stem": "低周波インバーターの出力",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211455008206.jpg",
            "alt_ja": "インバーターの入力電流と入力電力",
            "title_ja": "インバーターの入力電流と入力電力",
            "stem": "インバーターの入力電流と入力電力",
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
