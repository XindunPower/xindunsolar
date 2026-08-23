#!/usr/bin/env python3
"""Publish xindun-power news page 58 articles to Spanish WordPress (cat 89)."""

from pathlib import Path

import publish_page55 as base

base.PAGE_NUM = 58
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Only these images contain English marketing/diagram overlay text.
# All other images are product/factory shots and should use original image
# (compress+rename only) per publishing rules.
base.DUOMI_MAP = {
    (0, 1): (
        "Translate the diagram label 'AC Loads' to Spanish. "
        "Keep arrows, truck, battery, appliance icons, inverter product, and layout unchanged."
    ),
    (1, 1): (
        "Translate all overlay labels to Spanish: "
        "'Internet', 'GPRS/WIFI module', 'Monitoring APP', and 'Monitoring web'. "
        "Keep cloud icon, phone, laptop, inverter, arrows, and composition unchanged."
    ),
    (2, 0): (
        "Translate the overlay text 'ups' to Spanish ('SAI'). "
        "Keep monitor, UPS product, background, and composition unchanged."
    ),
    (3, 0): (
        "Translate overlay bullet text to Spanish: "
        "'Excellent Mute', 'High Efficiency', and 'Electronic protect'. "
        "Keep icons, inverter product, and background layout unchanged."
    ),
    (3, 1): (
        "Translate all instructional overlay text to Spanish, including heading and captions. "
        "Keep product images, symbols, arrows, hazard icons, and layout unchanged."
    ),
    (4, 0): (
        "Translate the label 'Suggestion' to Spanish. "
        "Keep 2500W/3000W numbers, check/cross marks, products, and layout unchanged."
    ),
    (4, 1): (
        "Translate the label 'Voltage' to Spanish ('Voltaje'). "
        "Keep battery label text, product casing text, blue bars, background, and layout unchanged."
    ),
}

# Ensure per-run state is fresh.
base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    base.main()
