#!/usr/bin/env python3
"""Publish xindun-power news page 1 in Russian (tag Русский, category id 125)."""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from page1_ru_content import ARTICLES, assert_article, assert_no_translate_error, prepend_18pt_title
from page1_ru_images import IMAGE_LOG, IMAGE_SOURCES, prepare_all
from wp_ru import CATEGORY_ID, WPClient

REPO = Path(__file__).resolve().parent.parent
PAGE_NUM = 1
RESULTS_PATH = Path(f"/tmp/page{PAGE_NUM}_ru_results.json")
PROGRESS_PATH = REPO / "progress_ru.json"
SOURCE_LIST = "https://www.xindun-power.com/news/index.html"


def img_tag(src: str, alt: str, title: str) -> str:
    return (
        f'<img src="{html.escape(src, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}" '
        f'title="{html.escape(title, quote=True)}" />'
    )


def main() -> None:
    if len(ARTICLES) != 5:
        raise RuntimeError(f"expected 5 articles, got {len(ARTICLES)}")
    if len(IMAGE_SOURCES) != 5:
        raise RuntimeError("image groups must match 5 articles")
    for art in ARTICLES:
        assert_article(art)
        n_ph = len(re.findall(r"\{img\d+\}", art["body_html"]))
        # placeholder count checked after we know image counts

    prepared_all = prepare_all()
    if len(prepared_all) != 5:
        raise RuntimeError("image prepare did not return 5 articles")

    wp = WPClient()
    wp.login()

    results: list[dict] = []
    for article_idx, art in enumerate(ARTICLES):
        print("=" * 70, flush=True)
        print(f"ARTICLE {article_idx}: {art['title_en']}", flush=True)

        body = art["body_html"]
        assert_no_translate_error(body)
        assert_no_translate_error(art["title_ru"])
        assert_no_translate_error(art["description_ru"])

        prepared = prepared_all[article_idx]
        placeholders = re.findall(r"\{img(\d+)\}", body)
        if sorted(int(x) for x in placeholders) != list(range(len(prepared))):
            raise RuntimeError(
                f"article {article_idx} placeholders {placeholders} vs {len(prepared)} images"
            )

        media_list = []
        for p in prepared:
            media = wp.upload_media(p["local"], p["alt_ru"], p["title_ru"])
            media_list.append(media)

        filled = body
        for i, media in enumerate(media_list):
            filled = filled.replace(
                "{img" + str(i) + "}",
                img_tag(media.get("source_url", ""), prepared[i]["alt_ru"], prepared[i]["title_ru"]),
            )
        if re.search(r"\{img\d+\}", filled):
            raise RuntimeError(f"unreplaced image placeholder in article {article_idx}")
        if "<a " in filled.lower() or "</a>" in filled.lower():
            raise RuntimeError(f"hyperlink remains in article {article_idx}")

        content = prepend_18pt_title(filled, art["title_ru"])
        assert_no_translate_error(content)
        if 'font-size: 18pt' not in content:
            raise RuntimeError("18pt title missing")

        featured = media_list[0]["id"] if media_list else 0
        featured_url = media_list[0].get("source_url", "") if media_list else ""

        post = wp.create_post(art["title_ru"], art["description_ru"], content, featured)
        print(f"[post] created id={post['id']} {post.get('link')}", flush=True)

        updated = wp.set_yoast(
            post["id"],
            art["seo_title_ru"],
            art["description_ru"],
            art["focuskw_ru"],
            content,
            featured,
            featured_url,
        )
        final_post = updated or post
        tags = final_post.get("tags") or []
        cats = final_post.get("categories") or []
        tag_ok = wp.tag_id in tags
        cat_ok = CATEGORY_ID in cats
        if not tag_ok or not cat_ok:
            raise RuntimeError(
                f"article {article_idx} tag/category mismatch tags={tags} cats={cats}"
            )

        results.append(
            {
                "title_en": art["title_en"],
                "title_ru": art["title_ru"],
                "url": art["source_url"],
                "status": "published",
                "published_url": final_post.get("link") or post.get("link"),
                "post_id": final_post.get("id") or post["id"],
                "russkiy_tag": tag_ok,
                "tag_id": wp.tag_id,
                "category_id": CATEGORY_ID,
                "category_ok": cat_ok,
                "images": [
                    {
                        "method": p["method"],
                        "duomi_path": p["duomi_path"],
                        "local": str(p["local"]),
                        "orig_wh": list(p["orig_wh"]),
                        "alt_ru": p["alt_ru"],
                    }
                    for p in prepared
                ],
            }
        )
        RESULTS_PATH.write_text(
            json.dumps({"page": PAGE_NUM, "results": results, "images": IMAGE_LOG}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    if len(results) != len(ARTICLES) or any(r["status"] != "published" for r in results):
        raise RuntimeError(
            f"not all {len(ARTICLES)} articles published; not advancing progress_ru.json"
        )

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    progress = {
        "page": PAGE_NUM + 1,
        "note": (
            f"page {PAGE_NUM} completed {now}; next pending page is {PAGE_NUM + 1}. "
            "Listing page 1 is https://www.xindun-power.com/news/index.html "
            "(news/1.html returns 404)."
        ),
        "last_completed_page": PAGE_NUM,
        "last_run": {
            "date": now,
            "source": SOURCE_LIST,
            "published": [
                {
                    "title_en": r["title_en"],
                    "title_ru": r["title_ru"],
                    "url": r["url"],
                    "status": r["status"],
                    "published_url": r["published_url"],
                    "post_id": r["post_id"],
                    "russkiy_tag": r["russkiy_tag"],
                    "category_id": r["category_id"],
                }
                for r in results
            ],
        },
    }
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("DONE", json.dumps(results, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
