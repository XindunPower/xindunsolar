#!/usr/bin/env python3
"""Publish xindun-power news page 57 articles to Spanish WordPress (cat 89)."""

from pathlib import Path

import publish_page55 as base

base.PAGE_NUM = 57
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Only this infographic contains English overlay labels on page 57.
base.DUOMI_MAP = {
    (3, 0): (
        "Translate waveform legend labels to Spanish: "
        "'Pure sine wave' and 'Modified sine wave'. "
        "Keep the inverter product, curves, chart lines, axes, and layout unchanged."
    )
}

# Ensure per-run state is fresh.
base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    base.main()
