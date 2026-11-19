#!/usr/bin/env python3
"""Prepare page 6 Japanese images.

Duomi gpt-image-2 only for the five marketing banners that carry English headlines.
Product studio shots and the installation photo collage are compressed only.
Outputs stay in output/duomi/ja/ so they do not collide with the Russian task.
Marketing edits that fail layout checks are discarded and retried from the original.
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
PAGE_NUM = 6

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a marketing banner: eight inverter and all-in-one units on a gold platform "
        "against a pale desert sky. Translate only the two-line English headline to Japanese, "
        "keeping the two-line layout: "
        "'What You Should Know About' → '構築する前に知っておきたい'; "
        "'Hybrid Inverter Before Building Solar System?' → 'ハイブリッドインバーター'. "
        "Keep every product, the platform and the background unchanged. "
        "Do NOT change product casing text (HYBRID SOLAR INVERTER, SPLIT PHASE INVERTER, "
        "ALL IN ONE SOLAR GENERATOR, Low Frequency), the xindun logo, CE marks or displays. "
        "Do not redesign."
    ),
    (1, 0): (
        "This is a night banner with a clock, a white hybrid inverter and a lithium battery. "
        "Translate only the headline to Japanese. Keep the orange highlight on the first words: "
        "'24 Hours' → '24時間'; 'Backup Inverter' → 'バックアップインバーター'. "
        "Keep both products, the clock and the starry background unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo, CE marks, 51.2V or the display. Do not redesign."
    ),
    (2, 0): (
        "This is a pale-blue product lineup on a white round podium. "
        "Translate only the two-line headline to Japanese, keeping 48 large and blue: "
        "'48 Volt' → '48ボルト'; 'Off Grid Inverter' → 'オフグリッドインバーター'. "
        "Keep every product and the podium unchanged. "
        "Do NOT change product casing text (ALL IN ONE SOLAR GENERATOR and other model labels), "
        "the xindun logo or displays. Do not redesign."
    ),
    (3, 0): (
        "This is a daylight banner: a house with rooftop solar and a row of inverters on grass. "
        "Translate only the headline to Japanese. Keep the orange pill around the product name: "
        "'What Can' and 'Do?' become the Japanese question around the pill, "
        "and the orange pill text '8KW Solar Hybrid Inverter' → '8KW太陽光ハイブリッドインバーター'. "
        "The full headline should read '8KW太陽光ハイブリッドインバーターにできることは？'. "
        "Keep the house, panels, lawn and every product unchanged. "
        "Do NOT change product casing text, the xindun logo or displays. Do not redesign."
    ),
    (4, 0): (
        "This is a night scene: a lit house, moon, solar panels, an inverter and a lithium battery. "
        "Translate only the two-line headline to Japanese. Keep the first line white and the second line red: "
        "'DOES THE SOLAR INVERTER' → 'ソーラーインバーターは'; "
        "'TURN OFF AT NIGHT?' → '夜間に停止するか？'. "
        "Keep the house, car, plug graphic, panels and both products unchanged. "
        "Do NOT change casing text (HYBRID SOLAR INVERTER, LiFePO4 Lithium Battery), "
        "the xindun logo or the display. Do not redesign."
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181628389949.jpg",
            "alt_ja": "ハイブリッドインバーターについて",
            "title_ja": "ハイブリッドインバーターについて",
            "stem": "ハイブリッドインバーターについて",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg",
            "alt_ja": "HFPハイブリッドインバーター",
            "title_ja": "HFPハイブリッドインバーター",
            "stem": "HFPハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151404306156.jpg",
            "alt_ja": "HUスプリットフェーズハイブリッドインバーター",
            "title_ja": "HUスプリットフェーズハイブリッドインバーター",
            "stem": "HUスプリットフェーズハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg",
            "alt_ja": "HP PLUS+並列ハイブリッドインバーター",
            "title_ja": "HP PLUS+並列ハイブリッドインバーター",
            "stem": "HP-PLUS並列ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211416117011.jpg",
            "alt_ja": "LUハイブリッドインバーター",
            "title_ja": "LUハイブリッドインバーター",
            "stem": "LUハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151505009158.jpg",
            "alt_ja": "HDSX三相ハイブリッドインバーター",
            "title_ja": "HDSX三相ハイブリッドインバーター",
            "stem": "HDSX三相ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151709439605.jpg",
            "alt_ja": "LFハイブリッドインバーター",
            "title_ja": "LFハイブリッドインバーター",
            "stem": "LFハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211353482657.jpg",
            "alt_ja": "ESSオールインワンソーラー発電機",
            "title_ja": "ESSオールインワンソーラー発電機",
            "stem": "ESSオールインワンソーラー発電機",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211107597731.jpg",
            "alt_ja": "ESS-Liソーラー発電機",
            "title_ja": "ESS-Liソーラー発電機",
            "stem": "ESS-Liソーラー発電機",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091544188167.jpg",
            "alt_ja": "24時間バックアップインバーター",
            "title_ja": "24時間バックアップインバーター",
            "stem": "24時間バックアップインバーター",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181609357954.jpg",
            "alt_ja": "48ボルトオフグリッドインバーター",
            "title_ja": "48ボルトオフグリッドインバーター",
            "stem": "48ボルトオフグリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124155414.jpg",
            "alt_ja": "HU 48ボルトスプリットフェーズインバーター",
            "title_ja": "HU 48ボルトスプリットフェーズインバーター",
            "stem": "HU-48ボルトスプリットフェーズインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091124506499.jpg",
            "alt_ja": "HP PLUS+ 48ボルト並列インバーター",
            "title_ja": "HP PLUS+ 48ボルト並列インバーター",
            "stem": "HP-PLUS-48ボルト並列インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ja": "HFP 48ボルトオフグリッドインバーター",
            "title_ja": "HFP 48ボルトオフグリッドインバーター",
            "stem": "HFP-48ボルトオフグリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ja": "HFP-E 48ボルトオフグリッドインバーター",
            "title_ja": "HFP-E 48ボルトオフグリッドインバーター",
            "stem": "HFP-E-48ボルトオフグリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181614417438.jpg",
            "alt_ja": "HDSX 48ボルト三相インバーター",
            "title_ja": "HDSX 48ボルト三相インバーター",
            "stem": "HDSX-48ボルト三相インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091125237036.jpg",
            "alt_ja": "LU 48ボルトスプリットフェーズインバーター",
            "title_ja": "LU 48ボルトスプリットフェーズインバーター",
            "stem": "LU-48ボルトスプリットフェーズインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181616085997.jpg",
            "alt_ja": "WF 48ボルトインバーター",
            "title_ja": "WF 48ボルトインバーター",
            "stem": "WF-48ボルトインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/18/202512181616422042.jpg",
            "alt_ja": "ESS 48ボルトソーラー発電機",
            "title_ja": "ESS 48ボルトソーラー発電機",
            "stem": "ESS-48ボルトソーラー発電機",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091013036397.jpg",
            "alt_ja": "8KW太陽光ハイブリッドインバーター",
            "title_ja": "8KW太陽光ハイブリッドインバーター",
            "stem": "8KW太陽光ハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151500223519.jpg",
            "alt_ja": "8KWハイブリッドインバーター",
            "title_ja": "8KWハイブリッドインバーター",
            "stem": "8KWハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091015453907.jpg",
            "alt_ja": "8KWソーラーインバーター",
            "title_ja": "8KWソーラーインバーター",
            "stem": "8KWソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151505009158.jpg",
            "alt_ja": "8KW三相インバーター",
            "title_ja": "8KW三相インバーター",
            "stem": "8KW三相インバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211416117011.jpg",
            "alt_ja": "8KWスプリットフェーズハイブリッドインバーター",
            "title_ja": "8KWスプリットフェーズハイブリッドインバーター",
            "stem": "8KWスプリットフェーズハイブリッドインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091019088117.jpg",
            "alt_ja": "ソーラーインバーター8KW",
            "title_ja": "ソーラーインバーター8KW",
            "stem": "ソーラーインバーター8KW",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091020017762.jpg",
            "alt_ja": "ソーラーインバーター",
            "title_ja": "ソーラーインバーター",
            "stem": "ソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/15/202507151709439605.jpg",
            "alt_ja": "インバーターソーラー8KW",
            "title_ja": "インバーターソーラー8KW",
            "stem": "インバーターソーラー8KW",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091529333216.jpg",
            "alt_ja": "8KWインバーター",
            "title_ja": "8KWインバーター",
            "stem": "8KWインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091038043837.jpg",
            "alt_ja": "8KW太陽光ハイブリッドインバーターの導入事例",
            "title_ja": "8KW太陽光ハイブリッドインバーターの導入事例",
            "stem": "8KW太陽光ハイブリッドインバーターの導入事例",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/12/09/202512091057481969.jpg",
            "alt_ja": "夜間のソーラーインバーター",
            "title_ja": "夜間のソーラーインバーター",
            "stem": "夜間のソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/15/202510151404306156.jpg",
            "alt_ja": "スプリットフェーズソーラーインバーター",
            "title_ja": "スプリットフェーズソーラーインバーター",
            "stem": "スプリットフェーズソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/21/202508211412417185.jpg",
            "alt_ja": "並列ソーラーインバーター",
            "title_ja": "並列ソーラーインバーター",
            "stem": "並列ソーラーインバーター",
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
