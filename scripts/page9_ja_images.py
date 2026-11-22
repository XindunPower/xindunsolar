#!/usr/bin/env python3
"""Prepare page 9 Japanese images.

Duomi gpt-image-2 for marketing banners and wiring diagrams that carry English
overlay labels. Studio product shots of HP PLUS+ and HU stay compressed and
renamed only. Outputs stay in output/duomi/ja/.
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
PAGE_NUM = 9

WIRE = (
    "This is a wiring diagram on a white background. Translate only the English labels to Japanese. "
    "Keep every wire, color, arrow, breaker, DB9 plug, solar panel, house icon and battery icon. "
    "Keep the exact inverter count and which units share a bracket labeled P1, P2 or P3. "
    "Keep electrical symbols exactly: P1, P2, P3, N, L1, L2, L3, PV1+, PV1-. "
    "Do NOT change product faces, the xindun logo, or displays. Do not add or remove inverters. "
    "Do not redesign. Keep any small red annotation mark exactly where it is."
)
LABELS = (
    " Labels: 'Battery' → 'バッテリー'; 'Utility Grid' → '電力系統'; "
    "'Loads' → '負荷'; 'PV array' → 'PVアレイ'."
)
KEEP_CASE = (
    " Do NOT change product casing text (HYBRID SOLAR INVERTER, HYBRID INVERTER, "
    "LiFePO4 Lithium Battery), the xindun logo, CE, ISO, or the display."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a dark-blue marketing banner: a white clock ring, an alarm-clock icon, "
        "a gear icon, a lithium battery on the left and a hybrid inverter on the right. "
        "Translate only the white headline to Japanese, keeping two lines: "
        "'Does The Scheduled Charge And Discharge Function of Off Grid Hybrid Inverter "
        "Affect Battery Life?' → "
        "'オフグリッドハイブリッドインバーターの充放電スケジュール機能はバッテリー寿命に影響するか？'. "
        "Keep the ring, icons, products and blue background unchanged."
        + KEEP_CASE
        + " Do not redesign."
    ),
    (1, 0): (
        "This is a dark marketing banner: a hybrid inverter on the left, a lithium battery "
        "on the right, an orange clock and two white arrows between them. "
        "Translate only the headline to Japanese and keep the second line orange: "
        "'Can The Off Grid Hybrid Inverter Be Set To' → "
        "'オフグリッドハイブリッドインバーターは'; "
        "'Timed Charging And Discharging?' → '時刻指定の充放電を設定できるか？'. "
        "Keep the clock, arrows, products and background unchanged."
        + KEEP_CASE
        + " Do not redesign."
    ),
    (2, 0): (
        "This is a blue-gray marketing banner: a hybrid inverter on the left, a lithium "
        "battery on the right, a dashed double arrow, and the large word BMS in the center. "
        "Translate only the white headline to Japanese. Keep the large center letters BMS unchanged: "
        "'What Are The Function of The Communication Connection Between Inverter And "
        "Lithium Battery BMS?' → "
        "'インバーターとリチウムバッテリーBMSの通信接続にはどんな機能があるか？'. "
        "Keep the center BMS, the arrow, the rounded frame, products and background unchanged."
        + KEEP_CASE
        + " Do not redesign."
    ),
    (3, 0): (
        "This is a daylight marketing diagram: solar panels, a power pylon, AC loads, "
        "three white inverters and a lithium battery, with mountains and a solar farm behind. "
        "Translate only the headline and the diagram labels to Japanese: "
        "'Can Single Phase Hybrid Inverter Output Three Phase AC Power?' → "
        "'単相ハイブリッドインバーターは三相交流を出力できるか？'; "
        "'Three phase parallel operation' → '三相並列運転'; "
        "'Solar Panels' → '太陽光パネル'; 'Power Grid' → '電力系統'; "
        "'AC Loads' → '交流負荷'; 'Battery' → 'バッテリー'. "
        "Keep L1, L2, L3, N and 380V exactly. Keep three inverters, one battery, arrows and background."
        + KEEP_CASE
        + " Do not redesign."
    ),
    (3, 1): (
        WIRE + LABELS
        + " Three inverters in one row. Top labels are P1, P2 and P3, one inverter each. "
        "This is the 1+1+1 three-phase diagram. Six PV array labels along the bottom."
    ),
    (3, 2): (
        WIRE + LABELS
        + " Four inverters. The P1 bracket covers the first two inverters. "
        "P2 and P3 are one inverter each. This is the 2+1+1 diagram."
    ),
    (3, 3): (
        WIRE + LABELS
        + " Five inverters. P1 covers two, P2 covers two, P3 is one. "
        "This is the 2+2+1 diagram. Keep the small red mark in the middle of the wires."
    ),
    (3, 4): (
        WIRE + LABELS
        + " Five inverters. P1 covers the first three. P2 and P3 are one inverter each. "
        "This is the 3+1+1 diagram."
    ),
    (3, 5): (
        WIRE + LABELS
        + " Six inverters. P1, P2 and P3 each cover two inverters. "
        "This is the 2+2+2 diagram."
    ),
    (3, 6): (
        WIRE + LABELS
        + " Six inverters. P1 covers the first three, P2 covers the next two, P3 is the last one. "
        "This is the 3+2+1 diagram. Keep the small red mark near the bottom-left plugs."
    ),
    (3, 7): (
        WIRE + LABELS
        + " Six inverters. The P1 bracket covers the first four. "
        "P2 and P3 are one inverter each. This is the 4+1+1 diagram."
    ),
    (4, 0): (
        "This is a sunset marketing diagram over a solar farm: panels, a pylon, AC loads, "
        "three white inverters and a lithium battery. "
        "Translate only the headline and the diagram labels to Japanese: "
        "'Can Hybrid Inverter Support Parallel Operation?' → "
        "'ハイブリッドインバーターは並列運転に対応できるか？'; "
        "'Inverter Parallel Operation' → 'インバーターの並列運転'; "
        "'Solar Panels' → '太陽光パネル'; 'Power Grid' → '電力系統'; "
        "'AC Loads' → '交流負荷'; 'Battery' → 'バッテリー'. "
        "Keep three inverters, one battery, arrows, sunset and solar-farm background."
        + KEEP_CASE
        + " Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/20251015141934Q1iFl3.jpg",
            "alt_ja": "インバーターのバッテリー寿命",
            "title_ja": "インバーターのバッテリー寿命",
            "stem": "インバーターのバッテリー寿命",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/20251015135824gYTtGy.jpg",
            "alt_ja": "オフグリッドハイブリッドインバーター",
            "title_ja": "オフグリッドハイブリッドインバーター",
            "stem": "オフグリッドハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg",
            "alt_ja": "HP PLUS+オフグリッドハイブリッドソーラーインバーター",
            "title_ja": "HP PLUS+オフグリッドハイブリッドソーラーインバーター",
            "stem": "HP-PLUS+オフグリッドハイブリッドソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151404306156.jpg",
            "alt_ja": "HUシリーズのオフグリッドハイブリッドインバーター",
            "title_ja": "HUシリーズのオフグリッドハイブリッドインバーター",
            "stem": "HUシリーズのオフグリッドハイブリッドインバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151351572844.jpg",
            "alt_ja": "インバーターとリチウムバッテリーBMS",
            "title_ja": "インバーターとリチウムバッテリーBMS",
            "stem": "インバーターとリチウムバッテリーBMS",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141455215992.jpg",
            "alt_ja": "単相ハイブリッドインバーターの出力",
            "title_ja": "単相ハイブリッドインバーターの出力",
            "stem": "単相ハイブリッドインバーターの出力",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141439441653.jpg",
            "alt_ja": "単相から三相へのハイブリッドインバーター",
            "title_ja": "単相から三相へのハイブリッドインバーター",
            "stem": "単相から三相へのハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141441107491.jpg",
            "alt_ja": "4台のインバーターによる三相ハイブリッド出力",
            "title_ja": "4台のインバーターによる三相ハイブリッド出力",
            "stem": "4台のインバーターによる三相ハイブリッド出力",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141441527553.jpg",
            "alt_ja": "5台のインバーターによる三相ハイブリッド出力",
            "title_ja": "5台のインバーターによる三相ハイブリッド出力",
            "stem": "5台のインバーターによる三相ハイブリッド出力",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141443026342.jpg",
            "alt_ja": "三相ハイブリッドインバーター",
            "title_ja": "三相ハイブリッドインバーター",
            "stem": "三相ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141447436781.jpg",
            "alt_ja": "6台のインバーターによる三相ハイブリッド出力",
            "title_ja": "6台のインバーターによる三相ハイブリッド出力",
            "stem": "6台のインバーターによる三相ハイブリッド出力",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141448025033.jpg",
            "alt_ja": "ハイブリッドインバーターの並列構成",
            "title_ja": "ハイブリッドインバーターの並列構成",
            "stem": "ハイブリッドインバーターの並列構成",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141448369932.jpg",
            "alt_ja": "単相ハイブリッドインバーターは三相交流を出力できるか",
            "title_ja": "単相ハイブリッドインバーターは三相交流を出力できるか",
            "stem": "単相ハイブリッドインバーターは三相交流を出力できるか",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/14/202510141520491752.jpg",
            "alt_ja": "並列ハイブリッドインバーター",
            "title_ja": "並列ハイブリッドインバーター",
            "stem": "並列ハイブリッドインバーター",
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
