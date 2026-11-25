#!/usr/bin/env python3
"""Publish xindun-power news page 28 in Russian (tag Русский, category id 125)."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from page28_ru_content import ARTICLES, assert_article, assert_no_translate_error
from page28_ru_images import IMAGE_LOG, IMAGE_SOURCES, prepare_all
from wp_ru import CATEGORY_ID, WP, WPClient

REPO = Path(__file__).resolve().parent.parent
PAGE_NUM = 28
RESULTS_PATH = Path(f"/tmp/page{PAGE_NUM}_ru_results.json")
PROGRESS_PATH = REPO / "progress_ru.json"
SOURCE_LIST = "https://www.xindun-power.com/news/28.html"


def img_tag(src: str, alt: str, title: str) -> str:
    return (
        f'<img src="{html.escape(src, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}" '
        f'title="{html.escape(title, quote=True)}" />'
    )


def remote_page() -> int:
    fetch = subprocess.run(
        ["git", "fetch", "origin", "main"],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    if fetch.returncode != 0:
        raise RuntimeError(f"git fetch origin main failed: {(fetch.stderr or fetch.stdout)[:400]}")
    show = subprocess.run(
        ["git", "show", "origin/main:progress_ru.json"],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if show.returncode != 0:
        raise RuntimeError("origin/main:progress_ru.json is missing; not advancing")
    return int(json.loads(show.stdout)["page"])


def find_same_title(wp: WPClient, title: str) -> dict | None:
    r = wp.s.get(
        f"{WP}/wp-json/wp/v2/posts",
        params={"search": title, "per_page": 20, "status": "publish"},
        timeout=60,
    )
    if not r.ok:
        return None
    for post in r.json():
        rendered = html.unescape((post.get("title") or {}).get("rendered") or "").strip()
        if rendered != title.strip():
            continue
        if CATEGORY_ID in (post.get("categories") or []):
            return post
    return None


def publish_new(wp: WPClient, art: dict, prepared: list[dict]) -> dict:
    body = art["body_html"]
    assert_no_translate_error(body)
    placeholders = [int(x) for x in re.findall(r"\{img(\d+)\}", body)]
    expected = list(range(1, len(prepared)))
    if sorted(placeholders) != expected or 0 in placeholders:
        raise RuntimeError(
            f"{art['title_en']} body placeholders {placeholders}; "
            f"expected {expected} (featured image stays out of the body)"
        )

    media_list = []
    for p in prepared:
        media = wp.upload_media(p["local"], p["alt_ru"], p["title_ru"])
        media_list.append(media)

    filled = body
    for i, media in enumerate(media_list):
        if i == 0:
            continue
        filled = filled.replace(
            "{img" + str(i) + "}",
            img_tag(media.get("source_url", ""), prepared[i]["alt_ru"], prepared[i]["title_ru"]),
        )
    if re.search(r"\{img\d+\}", filled):
        raise RuntimeError(f"unreplaced image placeholder in {art['title_en']}")
    if "<a " in filled.lower() or "</a>" in filled.lower():
        raise RuntimeError(f"hyperlink remains in {art['title_en']}")
    assert_no_translate_error(filled)
    if re.search(r"font-size:\s*18pt", filled, re.I):
        raise RuntimeError("duplicate 18pt title is still in the body")

    featured = media_list[0]["id"] if media_list else 0
    featured_url = media_list[0].get("source_url", "") if media_list else ""

    existing = find_same_title(wp, art["title_ru"])
    if existing:
        print(f"[post] reuse existing id={existing['id']} {existing.get('link')}", flush=True)
        r = wp.s.post(
            f"{WP}/wp-json/wp/v2/posts/{existing['id']}",
            headers={"X-WP-Nonce": wp.nonce},
            json={
                "title": art["title_ru"],
                "content": filled,
                "excerpt": art["description_ru"],
                "status": "publish",
                "tags": [wp.tag_id],
                "categories": [CATEGORY_ID],
                "featured_media": featured,
            },
            timeout=120,
        )
        r.raise_for_status()
        post = r.json()
    else:
        post = wp.create_post(art["title_ru"], art["description_ru"], filled, featured)
        print(f"[post] created id={post['id']} {post.get('link')}", flush=True)

    updated = wp.set_yoast(
        post["id"],
        art["seo_title_ru"],
        art["description_ru"],
        art["focuskw_ru"],
        filled,
        featured,
        featured_url,
    )
    final_post = updated or post
    tags = final_post.get("tags") or []
    cats = final_post.get("categories") or []
    tag_ok = wp.tag_id in tags
    cat_ok = CATEGORY_ID in cats and all(int(c) == CATEGORY_ID for c in cats)
    if not tag_ok or not cat_ok:
        raise RuntimeError(f"{art['title_en']} tag/category mismatch tags={tags} cats={cats}")

    return {
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
                "src_orig": p["src_orig"],
            }
            for p in prepared
        ],
    }


def main() -> None:
    if len(ARTICLES) != 5:
        raise RuntimeError(f"expected 5 articles, got {len(ARTICLES)}")
    if len(IMAGE_SOURCES) != 5:
        raise RuntimeError("image groups must match 5 articles")
    for art in ARTICLES:
        assert_article(art)

    ahead = remote_page()
    if ahead != PAGE_NUM:
        raise RuntimeError(
            f"origin/main progress_ru.json page is {ahead}, expected {PAGE_NUM}. "
            "Not translating or publishing this snapshot."
        )

    prepared_all = prepare_all()
    if len(prepared_all) != 5:
        raise RuntimeError("image prepare did not return 5 articles")
    for group in prepared_all:
        for img in group:
            if img.get("method") == "duomi-fallback-original":
                raise RuntimeError(
                    f"Duomi did not translate {img.get('src_orig')}; "
                    "not publishing an English marketing image"
                )

    wp = WPClient()
    wp.login()

    results = []
    for article_idx, art in enumerate(ARTICLES):
        print("=" * 70, flush=True)
        print(f"ARTICLE {article_idx}: {art['title_en']}", flush=True)
        results.append(publish_new(wp, art, prepared_all[article_idx]))
        RESULTS_PATH.write_text(
            json.dumps({"page": PAGE_NUM, "results": results, "images": IMAGE_LOG}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    if len(results) != 5 or any(r["status"] != "published" for r in results):
        raise RuntimeError("not all 5 page articles are published; not advancing progress_ru.json")

    latest = remote_page()
    if latest > PAGE_NUM:
        raise RuntimeError(
            f"origin/main is already page {latest}; not overwriting progress_ru.json with page {PAGE_NUM}"
        )

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    progress = {
        "page": PAGE_NUM + 1,
        "note": (
            f"page {PAGE_NUM} completed {now}; next pending page is {PAGE_NUM + 1}. "
            "Listing page 1 is https://www.xindun-power.com/news/index.html "
            "(news/1.html returns 404). Featured image is featured_media only and must not "
            "be inserted into the post body. The post title is already the page H1; do not "
            "prepend another title inside the body. Do not duplicate a source URL already "
            "recorded in progress_ru.json. Page 2 repeated is-battery-necessary-for-inverter.html "
            "as post 20192."
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
