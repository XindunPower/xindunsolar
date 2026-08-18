#!/usr/bin/env python3
"""Normalize featured image height to 600x400 for existing Spanish posts."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from publish_page50 import (  # noqa: E402
    FEATURED_WH,
    OUT,
    UA,
    WP,
    WPClient,
    make_featured_variant,
    slugify,
)

CAT = 89


def posts_with_tall_featured(limit: int = 100) -> list[dict]:
    s = requests.Session()
    s.headers["User-Agent"] = UA
    found: list[dict] = []
    page = 1
    while len(found) < limit:
        r = s.get(
            f"{WP}/wp-json/wp/v2/posts",
            params={
                "categories": CAT,
                "per_page": 50,
                "page": page,
                "status": "publish",
                "_embed": "1",
            },
            timeout=60,
        )
        if not r.ok or not r.json():
            break
        for post in r.json():
            media = post.get("_embedded", {}).get("wp:featuredmedia", [{}])[0]
            url = media.get("source_url") or ""
            if not url:
                continue
            try:
                rr = s.get(url, timeout=60)
                rr.raise_for_status()
                with Image.open(__import__("io").BytesIO(rr.content)) as img:
                    w, h = img.size
            except Exception:
                continue
            if h != FEATURED_WH[1] or w != FEATURED_WH[0]:
                found.append(
                    {
                        "post_id": post["id"],
                        "media_id": media.get("id"),
                        "link": post.get("link"),
                        "title": re.sub(
                            r"<[^>]+>",
                            "",
                            (post.get("title") or {}).get("rendered") or "",
                        ),
                        "size": (w, h),
                        "source_url": url,
                    }
                )
        page += 1
    return found


def fix_post(wp: WPClient, post_id: int, source_path: Path | None = None) -> dict:
    edit = wp.s.get(
        f"{WP}/wp-json/wp/v2/posts/{post_id}",
        params={"context": "edit", "_embed": "1"},
        headers={"X-WP-Nonce": wp.nonce},
        timeout=60,
    )
    edit.raise_for_status()
    post = edit.json()
    title = re.sub(r"<[^>]+>", "", (post.get("title") or {}).get("rendered") or "")
    content = post.get("content", {}).get("raw") or post.get("content", {}).get("rendered") or ""
    desc = post.get("excerpt", {}).get("raw") or post.get("excerpt", {}).get("rendered") or title
    featured_media = post.get("featured_media")
    media = post.get("_embedded", {}).get("wp:featuredmedia", [{}])[0]
    media_url = media.get("source_url") or ""

    if source_path is None:
        local = OUT / f"_fix_src_post_{post_id}.webp"
        rr = wp.s.get(media_url, timeout=60)
        rr.raise_for_status()
        local.write_bytes(rr.content)
        source_path = local

    alt = media.get("alt_text") or title
    feat_path = make_featured_variant(source_path, slugify(alt))
    feat_media = wp.upload_media(feat_path, alt, alt)
    featured = feat_media["id"]
    featured_url = feat_media.get("source_url", "")

    r = wp.s.post(
        f"{WP}/wp-json/wp/v2/posts/{post_id}",
        headers={"X-WP-Nonce": wp.nonce},
        json={"featured_media": featured},
        timeout=120,
    )
    r.raise_for_status()
    wp.set_yoast(post_id, title, desc, content, featured, featured_url)
    return {
        "post_id": post_id,
        "old_media_id": featured_media,
        "new_media_id": featured,
        "old_size": media.get("media_details", {}).get("width"),  # may be absent
        "new_url": featured_url,
        "featured_path": str(feat_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post-id", type=int, action="append", default=[])
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--all-tall", action="store_true")
    args = parser.parse_args()

    wp = WPClient()
    wp.login()

    targets: list[int] = list(args.post_id)
    if args.scan:
        tall = posts_with_tall_featured()
        print(json.dumps(tall, ensure_ascii=False, indent=2))
        if not args.all_tall and not targets:
            return
        if args.all_tall:
            targets.extend(p["post_id"] for p in tall)

    if not targets:
        targets = [14158]

    results = []
    for pid in dict.fromkeys(targets):
        print(f"[fix] post {pid}", flush=True)
        try:
            result = fix_post(wp, pid)
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[fix] failed post {pid}: {exc}", flush=True)
            time.sleep(2)
    print("DONE", json.dumps(results, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
