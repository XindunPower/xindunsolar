#!/usr/bin/env python3
"""Prepare page 10 Japanese images.

Duomi gpt-image-2 for marketing banners and wiring diagrams that carry English
overlay labels. Studio product shots and the installation collage stay compressed
and renamed only. Outputs stay in output/duomi/ja/.
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
PAGE_NUM = 10

KEEP_CASE = (
    " Do NOT change product casing text, the xindun logo, CE, ISO, displays, "
    "or model markings. Do not add or remove products. Do not redesign."
)

DUOMI_MAP: dict[tuple[int, int], str] = {
    (0, 0): (
        "This is a light-gray marketing banner: one white wall inverter in the center "
        "and four orange rounded icons (bug, water drop, dust filter, sun). "
        "Translate only the top headline to Japanese, keep it on one line: "
        "'INVERTER PROTECTION LEVEL' → 'インバーターの保護等級'. "
        "Keep the second line of rating codes exactly: IP20 IP21 IP54 IP65 IP66. "
        "Keep the inverter, icons, gray background and spacing."
        + KEEP_CASE
    ),
    (1, 0): (
        "This is a light-gray marketing banner: a white hybrid inverter in the center, "
        "an orange rounded panel on the left and a pale-gray rounded panel on the right. "
        "Translate only the overlay text to Japanese and keep the same line breaks. "
        "Headline line 1: 'DC COUPLING VS' → 'DCカップリングと'. "
        "Headline line 2: 'AC COUPLING OF INVERTER' → 'ACカップリングの比較'. "
        "Left orange panel, two lines: 'DC' stays 'DC'; 'COUPLING' → 'カップリング'. "
        "Right panel, three lines: 'AC' stays 'AC'; 'COUPLING OF' → 'カップリング'; "
        "'INVERTER' → 'インバーター'. "
        "Keep DC and AC abbreviations. Do not change the casing line HYBRID SOLAR INVERTER, "
        "the xindun GREEN POWER logo, the display, buttons or CE mark."
        + KEEP_CASE
    ),
    (2, 0): (
        "This is a portrait marketing banner: a log cabin in a forest, solar panels "
        "and two power units in the foreground. Translate only the white two-line headline "
        "to Japanese: 'What Is Pay As You Go' → '従量課金型とは'; "
        "'Solar Home System?' → 'ソーラーホームシステム？'. "
        "Keep the cabin, forest, panels, both units and the question mark. "
        "Do not change product casing text such as ENERGY STORAGE SYSTEM or SOLAR GENERATOR."
        + KEEP_CASE
    ),
    (2, 2): (
        "This is a wiring diagram on a white background. Translate only the English labels "
        "around the diagram to Japanese. Keep every wire, arrow, icon and the central inverter. "
        "'Solar Panel' → '太陽光パネル'; 'AC Output' → 'AC出力'; 'Laptop' → 'ノートPC'; "
        "'Refrigerator' → '冷蔵庫'; 'Air-conditioning' → 'エアコン'; "
        "'Hair drier' → 'ドライヤー'; 'Water dispenser' → '給水器'; "
        "'AC Input' → 'AC入力'; 'or' → 'または'; 'Generator' → '発電機'; "
        "'DC Output' → 'DC出力'; 'Lamp' → 'ランプ'; 'Mobile Phone' → '携帯電話'; "
        "'Wireless Earphone' → 'ワイヤレスイヤホン'. "
        "Do NOT change text printed on the inverter body, including ENERGY STORAGE SYSTEM, "
        "LiFePO4+MPPT+INVERTER, the xindun logo, the display, or side-panel port names. "
        "Do not add or remove appliances. Do not redesign."
    ),
    (2, 4): (
        "This is a wiring diagram on a white background with two solar-generator units. "
        "Translate only the English diagram labels to Japanese. Keep wire colors, N and L, "
        "arrows, breakers and every appliance icon. "
        "'INVERTER' → 'インバーター'; 'SOLAR PANELS' → '太陽光パネル'; "
        "'POWER GRID' → '電力系統'; 'GENERATOR' → '発電機'; 'or' → 'または'; "
        "'Fan' → '扇風機'; 'Notebook Computer' → 'ノートPC'; 'Hair Drier' → 'ドライヤー'; "
        "'Electric kettle' → '電気ケトル'; 'AC LOADS' → 'AC負荷'; "
        "'DC LOADS' → 'DC負荷'. Keep the letters N and L exactly. "
        "Do NOT change SOLAR GENERATOR printed on the casing, the xindun logo, "
        "the display, or port labels on the black panel. Do not redesign."
    ),
    (2, 6): (
        "This is a wiring diagram on a white background with one blue portable unit. "
        "Translate only the labels outside the product to Japanese. "
        "'Solar Panels' → '太陽光パネル'; 'or' → 'または'; "
        "'Adapter Input' → 'アダプター入力'; 'Mains' → '商用電源'; "
        "'Mini Fan' → 'ミニ扇風機'; 'Wireless Earphone' → 'ワイヤレスイヤホン'; "
        "'Mobile Phone' → '携帯電話'; 'Lamp' → 'ランプ'. "
        "Do NOT change text printed on the blue unit: SOLAR POWER LIGHTING SYSTEM, "
        "POWER, ON/OFF, DC 5V, DC 12V, USB, SOLAR INPUT or ADAPTER INPUT. "
        "Keep the adapter photo, pylons, panel and arrows. Do not redesign."
    ),
    (3, 0): (
        "This is a beige comparison banner: a black inverter on a green panel at left, "
        "a gray VFD on a brown panel at right, and a yellow VS bolt in the middle. "
        "Translate only the overlay text to Japanese. Keep two headline lines and the green "
        "color of the second line: 'What Is the Difference Between' → '違いは何か'; "
        "'VFD And Inverter?' → 'VFDとインバーター？'. "
        "Bottom-left label 'INVERTER' → 'インバーター'. Keep the bottom-right label 'VFD' as VFD. "
        "Keep the yellow VS. Do not change either product, warning stickers, the display "
        "or the logo."
        + KEEP_CASE
    ),
    (4, 0): (
        "This is a dark marketing banner of several white inverters on black steps. "
        "Keep the green badge text '2 in 1' exactly, because it is the product name. "
        "Translate only the white words 'Solar Inverter' → 'ソーラーインバーター'. "
        "Keep every inverter, the RGB ring, the steps, the dark background, CE marks "
        "and HYBRID SOLAR INVERTER printed on the casings."
        + KEEP_CASE
    ),
}

IMAGE_SOURCES = [
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/09/202510091145502608.jpg",
            "alt_ja": "インバーターの保護等級IP20 IP21 IP54 IP65 IP66",
            "title_ja": "インバーターの保護等級IP20 IP21 IP54 IP65 IP66",
            "stem": "インバーターの保護等級",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/10/09/202510091143529756.jpg",
            "alt_ja": "DCカップリングとACカップリングのインバーター",
            "title_ja": "DCカップリングとACカップリングのインバーター",
            "stem": "DCとACのカップリング",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/09/06/202509061456418096.jpg",
            "alt_ja": "従量課金型ソーラーホームシステム",
            "title_ja": "従量課金型ソーラーホームシステム",
            "stem": "従量課金型ソーラーホームシステム",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/11/01/202411011540107215.jpg",
            "alt_ja": "ESS-LiのPAYGOソーラーシステム",
            "title_ja": "ESS-LiのPAYGOソーラーシステム",
            "stem": "ESS-LiのPAYGOソーラーシステム",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/31/202410310956586221.jpg",
            "alt_ja": "PAYGOソーラーシステムの配線図",
            "title_ja": "PAYGOソーラーシステムの配線図",
            "stem": "PAYGOソーラーシステムの配線図",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/21/202507211052554816.jpg",
            "alt_ja": "ESSの従量課金型ソーラーシステム",
            "title_ja": "ESSの従量課金型ソーラーシステム",
            "stem": "ESSの従量課金型ソーラーシステム",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2024/10/31/202410311726521839.jpg",
            "alt_ja": "従量課金型ソーラーシステムの接続",
            "title_ja": "従量課金型ソーラーシステムの接続",
            "stem": "従量課金型ソーラーシステムの接続",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/09/06/202509061505127925.jpg",
            "alt_ja": "XD-TのPAYGOソーラーシステム",
            "title_ja": "XD-TのPAYGOソーラーシステム",
            "stem": "XD-TのPAYGOソーラーシステム",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/09/06/202509061506114178.jpg",
            "alt_ja": "PAYGOソーラーホームシステムの配線",
            "title_ja": "PAYGOソーラーホームシステムの配線",
            "stem": "PAYGOソーラーホームシステムの配線",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/09/06/202509061455511845.jpg",
            "alt_ja": "使用中のPAYGOソーラーホームシステム",
            "title_ja": "使用中のPAYGOソーラーホームシステム",
            "stem": "使用中のPAYGOソーラーホームシステム",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/30/202508301049129940.jpg",
            "alt_ja": "VFDとインバーターの違い",
            "title_ja": "VFDとインバーターの違い",
            "stem": "VFDとインバーターの違い",
        },
    ],
    [
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/08/30/202508301553448160.jpg",
            "alt_ja": "2 in 1ソーラーインバーター",
            "title_ja": "2 in 1ソーラーインバーター",
            "stem": "2in1ソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211756314825.png",
            "alt_ja": "HFPの2 in 1ソーラーインバーター",
            "title_ja": "HFPの2 in 1ソーラーインバーター",
            "stem": "HFPの2in1ソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141550028678.jpg",
            "alt_ja": "HFP-Sハイブリッドソーラーインバーター",
            "title_ja": "HFP-Sハイブリッドソーラーインバーター",
            "stem": "HFP-Sハイブリッドソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/06/21/202506211757093016.png",
            "alt_ja": "HFP-Cの2 in 1ソーラーインバーター",
            "title_ja": "HFP-Cの2 in 1ソーラーインバーター",
            "stem": "HFP-Cの2in1ソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141551587220.jpg",
            "alt_ja": "HFP-Eソーラーインバーター",
            "title_ja": "HFP-Eソーラーインバーター",
            "stem": "HFP-Eソーラーインバーター",
        },
        {
            "src": "https://www.xindun-power.com/uploadfile/2025/07/14/202507141552243253.jpg",
            "alt_ja": "HP PLUS+の2 in 1インバーター",
            "title_ja": "HP PLUS+の2 in 1インバーター",
            "stem": "HP-PLUS+の2in1インバーター",
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
