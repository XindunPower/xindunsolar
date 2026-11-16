#!/usr/bin/env python3
"""Publish xindun-power news page 80 to French WordPress (tag Français, no categories)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from page80_fr_content import ARTICLES, assert_no_translate_error, prepend_18pt_title
from page80_fr_images import IMAGE_LOG, prepare_all
from wp_fr import WPClient

REPO = Path(__file__).resolve().parent.parent
PAGE_NUM = 80
RESULTS_PATH = Path(f"/tmp/page{PAGE_NUM}_fr_results.json")
PROGRESS_PATH = REPO / "progress_fr.json"


def img_tag(src: str, alt: str, title: str) -> str:
    return f'<img src="{src}" alt="{alt}" title="{title}" />'


def main() -> None:
    prepared_all = prepare_all()
    wp = WPClient()
    wp.login()
    print(f"[wp] Français count before publish: {wp.francais_count()}", flush=True)

    results: list[dict] = []
    for article_idx, art in enumerate(ARTICLES):
        print("=" * 70, flush=True)
        print(f"ARTICLE {article_idx}: {art['title_en']}", flush=True)

        body = art["body_html"]
        assert_no_translate_error(body)
        assert_no_translate_error(art["title_fr"])
        assert_no_translate_error(art["description_fr"])

        prepared = prepared_all[article_idx]
        media_list = []
        for p in prepared:
            media = wp.upload_media(p["local"], p["alt_fr"], p["title_fr"])
            media_list.append(media)

        filled = body
        for i, media in enumerate(media_list):
            filled = filled.replace(
                "{img" + str(i) + "}",
                img_tag(media.get("source_url", ""), prepared[i]["alt_fr"], prepared[i]["title_fr"]),
            )
        if re.search(r"\{img\d+\}", filled):
            raise RuntimeError(f"unreplaced image placeholder in article {article_idx}")
        if "<a " in filled.lower():
            raise RuntimeError(f"hyperlink remains in article {article_idx}")

        content = prepend_18pt_title(filled, art["title_fr"])
        assert_no_translate_error(content)

        featured = media_list[0]["id"] if media_list else 0
        featured_url = media_list[0].get("source_url", "") if media_list else ""

        post = wp.create_post(art["title_fr"], art["description_fr"], content, featured)
        print(f"[post] created id={post['id']} {post.get('link')}", flush=True)
        tags = post.get("tags") or []
        if wp.tag_id not in tags:
            print(f"[warn] Français tag missing on create, tags={tags}", flush=True)

        updated = wp.set_yoast(
            post["id"],
            art["seo_title_fr"],
            art["description_fr"],
            content,
            featured,
            featured_url,
        )
        final_post = updated or post
        tag_ok = wp.tag_id in (final_post.get("tags") or tags or [])
        results.append(
            {
                "title_en": art["title_en"],
                "title_fr": art["title_fr"],
                "url": art["source_url"],
                "status": "published",
                "published_url": final_post.get("link") or post.get("link"),
                "post_id": final_post.get("id") or post["id"],
                "francais_tag": tag_ok,
                "images": [
                    {
                        "method": p["method"],
                        "duomi_path": p["duomi_path"],
                        "local": str(p["local"]),
                        "orig_wh": list(p["orig_wh"]),
                    }
                    for p in prepared
                ],
            }
        )
        RESULTS_PATH.write_text(
            json.dumps({"page": PAGE_NUM, "results": results, "images": IMAGE_LOG}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    if len(results) != 5 or any(r["status"] != "published" for r in results):
        raise RuntimeError("not all 5 articles published; not advancing progress_fr.json")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    progress = {
        "page": PAGE_NUM + 1,
        "note": f"page {PAGE_NUM} completed {now}; next pending page is {PAGE_NUM + 1}",
        "last_completed_page": PAGE_NUM,
        "last_run": {
            "date": now,
            "source": f"https://www.xindun-power.com/news/{PAGE_NUM}.html",
            "published": [
                {
                    "title_en": r["title_en"],
                    "title_fr": r["title_fr"],
                    "url": r["published_url"],
                    "status": r["status"],
                    "published_url": r["published_url"],
                    "post_id": r["post_id"],
                    "francais_tag": r["francais_tag"],
                }
                for r in results
            ],
        },
    }
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("DONE", json.dumps(results, ensure_ascii=False, indent=2), flush=True)
    print(f"[wp] Français count after publish: {wp.francais_count()}", flush=True)


if __name__ == "__main__":
    main()
