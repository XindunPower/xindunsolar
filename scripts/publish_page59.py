#!/usr/bin/env python3
"""Publish xindun-power news page 59 articles to Spanish WordPress (cat 89)."""

from pathlib import Path

import publish_page55 as base

base.PAGE_NUM = 59
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Only images with English marketing/diagram overlay text.
base.DUOMI_MAP = {
    (0, 0): (
        "Translate diagram labels '12V DC' and '220V AC' to Spanish (12V CC, 220V CA). "
        "Keep battery, inverter, air conditioner, arrows, xindun GREEN POWER logo, and layout unchanged."
    ),
    (0, 1): (
        "Translate all technical flow overlay text to Spanish, including "
        "'12V DC', 'high frequency boost', '220V DC', 'full bridge rectification', "
        "'inverter bridge converter', and '220V AC'. "
        "Keep inverter product, arrows, and background unchanged."
    ),
    (1, 0): (
        "Translate marketing poster text to Spanish: title 'Xindun 3000 watt power inverter', "
        "bullet points 'High-Quality Construction', 'High Performance', 'Advanced Technology', "
        "and specification labels (Battery Voltage, Size, Packing Size, N.W.). "
        "Keep Xindun brand name, xindun GREEN POWER logo, product, and layout unchanged."
    ),
    (3, 0): (
        "Translate diagram labels to Spanish: 'High Frequency Inverter', 'Gel Batteries', "
        "'Lithium Batteries', 'AC Loads', 'DC Loads', and 'or'. "
        "Keep product casing text (SOLAR INVERTER, LFP-48100), arrows, icons, and layout unchanged."
    ),
    (4, 0): (
        "Translate marketing overlay text '30000 hours of trouble-free operation inverter manufacturers' "
        "to Spanish. Keep xindun GREEN POWER logo, calculator, desk scene, and layout unchanged."
    ),
}

base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    base.main()
