#!/usr/bin/env python3
"""Publish xindun-power news page 60 articles to Spanish WordPress (cat 89)."""

from pathlib import Path

import publish_page55 as base

base.PAGE_NUM = 60
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Only image (article index 2, image index 0) has translatable English diagram overlays.
# Other images are photo/product shots or brand-only marks and must stay original
# (compress + Spanish alt filename only).
base.DUOMI_MAP = {
    (2, 0): (
        "Translate all English diagram labels and control-panel instruction overlays to Spanish, "
        "including heading text such as 'SOLAR POWER SYSTEM' and button/help labels. "
        "Keep product casing text, logos, model numbers, hardware layout, wiring, and composition unchanged."
    ),
}

base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    base.main()
