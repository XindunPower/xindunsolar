#!/usr/bin/env python3
"""Publish xindun-power news page 3 in Japanese (tag 日本語, category id 123)."""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from page3_ja_content import ARTICLES, assert_article, assert_no_translate_error, prepend_18pt_title
from page3_ja_images import IMAGE_LOG, IMAGE_SOURCES, prepare_all
from wp_ja import CATEGORY_ID, FORBIDDEN_TAG_ID, WPClient

REPO = Path(__file__).resolve().parent.parent
PAGE_NUM = 3
RESULTS_PATH = Path(f"/tmp/page{PAGE_NUM}_ja_results.json")
PROGRESS_PATH = REPO / "progress_ja.json"
SOURCE_LIST = "https://www.xindun-power.com/news/3.html"


def img_tag(src: str, alt: str, title: str) -> str:
    return (
        f'<img src="{html.escape(src, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}" '
        f'title="{html.escape(title, quote=True)}" />'
    )


def main() -> None:
    progress = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    if int(progress.get("page") or 0) != PAGE_NUM:
        raise RuntimeError(
            f"progress_ja.json page is {progress.get('page')}, expected {PAGE_NUM}; not publishing"
        )
    if int(progress.get("last_completed_page") or 0) >= PAGE_NUM:
        raise RuntimeError(
            f"last_completed_page is {progress.get('last_completed_page')}; not redoing page {PAGE_NUM}"
        )
    if len(ARTICLES) != 5:
        raise RuntimeError(f"expected 5 articles, got {len(ARTICLES)}")
    if len(IMAGE_SOURCES) != 5:
        raise RuntimeError("image groups must match 5 articles")
    for art in ARTICLES:
        assert_article(art)

    wp = WPClient()
    wp.login()
    if wp.tag_id == FORBIDDEN_TAG_ID:
        raise RuntimeError("refusing JP tag id 70")

    prepared_all = prepare_all()
    if len(prepared_all) != 5:
        raise RuntimeError("image prepare did not return 5 articles")

    results: list[dict] = []
    for article_idx, art in enumerate(ARTICLES):
        print("=" * 70, flush=True)
        print(f"ARTICLE {article_idx}: {art['title_en']}", flush=True)

        body = art["body_html"]
        assert_no_translate_error(body)
        assert_no_translate_error(art["title_ja"])
        assert_no_translate_error(art["description_ja"])

        prepared = prepared_all[article_idx]
        placeholders = [int(x) for x in re.findall(r"\{img(\d+)\}", body)]
        expected = list(range(1, len(prepared)))
        if sorted(placeholders) != expected or 0 in placeholders:
            raise RuntimeError(
                f"article {article_idx} body placeholders {placeholders}; "
                f"expected {expected} (featured image stays out of the body)"
            )

        media_list = []
        for p in prepared:
            media = wp.upload_media(p["local"], p["alt_ja"], p["title_ja"])
            media_list.append(media)

        filled = body
        for i, media in enumerate(media_list):
            if i == 0:
                continue
            filled = filled.replace(
                "{img" + str(i) + "}",
                img_tag(media.get("source_url", ""), prepared[i]["alt_ja"], prepared[i]["title_ja"]),
            )
        if re.search(r"\{img\d+\}", filled):
            raise RuntimeError(f"unreplaced image placeholder in article {article_idx}")
        if "<a " in filled.lower() or "</a>" in filled.lower():
            raise RuntimeError(f"hyperlink remains in article {article_idx}")

        content = prepend_18pt_title(filled, art["title_ja"])
        assert_no_translate_error(content)
        if len(re.findall(r"font-size:\s*18pt", content, re.I)) != 1:
            raise RuntimeError("Japanese body must start with exactly one 18pt title")

        featured = media_list[0]["id"] if media_list else 0
        featured_url = media_list[0].get("source_url", "") if media_list else ""

        post = wp.create_post(art["title_ja"], art["description_ja"], content, featured)
        print(f"[post] created id={post['id']} {post.get('link')}", flush=True)

        updated = wp.set_yoast(
            post["id"],
            art["seo_title_ja"],
            art["description_ja"],
            art["focuskw_ja"],
            content,
            featured,
            featured_url,
        )
        final_post = updated or post
        tags = [int(t) for t in (final_post.get("tags") or [])]
        cats = [int(c) for c in (final_post.get("categories") or [])]
        tag_ok = wp.tag_id in tags
        cat_ok = cats == [CATEGORY_ID]
        if not tag_ok or not cat_ok:
            raise RuntimeError(
                f"article {article_idx} tag/category mismatch tags={tags} cats={cats}"
            )

        results.append(
            {
                "title_en": art["title_en"],
                "title_ja": art["title_ja"],
                "url": art["source_url"],
                "status": "published",
                "published_url": final_post.get("link") or post.get("link"),
                "post_id": final_post.get("id") or post["id"],
                "nihongo_tag": tag_ok,
                "tag_id": wp.tag_id,
                "category_id": CATEGORY_ID,
                "category_ok": cat_ok,
                "images": [
                    {
                        "method": p["method"],
                        "duomi_path": p["duomi_path"],
                        "local": str(p["local"]),
                        "orig_wh": list(p["orig_wh"]),
                        "alt_ja": p["alt_ja"],
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
            f"not all {len(ARTICLES)} articles published; not advancing progress_ja.json"
        )

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    progress_out = {
        "page": PAGE_NUM + 1,
        "note": (
            f"page {PAGE_NUM} completed {now}; next pending page is {PAGE_NUM + 1}. "
            "Listing page 1 is https://www.xindun-power.com/news/index.html "
            "(news/1.html returns 404). "
            "Do not redo pages 1-3. Page 2 skipped republishing "
            "Is Battery Necessary for Inverter? because it was already published on page 1."
        ),
        "last_completed_page": PAGE_NUM,
        "last_run": {
            "date": now,
            "source": SOURCE_LIST,
            "published": [
                {
                    "title_en": r["title_en"],
                    "title_ja": r["title_ja"],
                    "url": r["url"],
                    "status": r["status"],
                    "published_url": r["published_url"],
                    "post_id": r["post_id"],
                    "nihongo_tag": r["nihongo_tag"],
                    "category_id": r["category_id"],
                }
                for r in results
            ],
        },
    }
    PROGRESS_PATH.write_text(json.dumps(progress_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("DONE", json.dumps(results, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
