#!/usr/bin/env python3
"""WordPress cookie+nonce helper for Xindun French news (tag Français, no categories)."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

import requests

WP = "https://www.xindunsolar.com"
UA = "Mozilla/5.0 (compatible; XindunFrenchBot/1.0)"
TAG_NAME = "Français"
TAG_SLUG = "francais"
FORBIDDEN_TAG_ID = 60  # existing "FR" tag — never use


class WPClient:
    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.nonce = ""
        self.tag_id = 0

    def login(self) -> None:
        user = os.environ["WP_USER"]
        pw = os.environ["WP_APP_PASSWORD"]
        last_err = ""
        for attempt in range(8):
            try:
                self.s.cookies.clear()
                lr = self.s.get(f"{WP}/wp-login.php", timeout=30)
                if lr.status_code >= 500:
                    raise RuntimeError(f"wp-login GET {lr.status_code}")
                self.s.post(
                    f"{WP}/wp-login.php",
                    data={
                        "log": user,
                        "pwd": pw,
                        "wp-submit": "Log In",
                        "redirect_to": f"{WP}/wp-admin/",
                        "testcookie": "1",
                    },
                    timeout=30,
                    allow_redirects=True,
                )
                admin = self.s.get(f"{WP}/wp-admin/", timeout=30)
                if admin.status_code >= 500:
                    raise RuntimeError(f"wp-admin GET {admin.status_code}")
                m = re.search(r"wpApiSettings\s*=\s*(\{.*?\});", admin.text)
                if not m:
                    raise RuntimeError("wpApiSettings nonce not found")
                self.nonce = json.loads(m.group(1))["nonce"]
                self.s.headers["X-WP-Nonce"] = self.nonce
                print("[wp] logged in, nonce ok", flush=True)
                self.tag_id = self.ensure_francais_tag()
                return
            except Exception as exc:  # noqa: BLE001
                last_err = str(exc)
                print(f"[wp] login retry {attempt + 1}/8: {last_err}", flush=True)
                time.sleep(5 * (attempt + 1))
        raise RuntimeError(f"WP login failed: {last_err}")

    def ensure_francais_tag(self) -> int:
        r = self.s.get(
            f"{WP}/wp-json/wp/v2/tags",
            params={"search": TAG_NAME, "per_page": 50},
            timeout=30,
        )
        r.raise_for_status()
        exact = [
            t
            for t in r.json()
            if t.get("name") == TAG_NAME and int(t.get("id") or 0) != FORBIDDEN_TAG_ID
        ]
        if not exact:
            r2 = self.s.get(
                f"{WP}/wp-json/wp/v2/tags",
                params={"slug": TAG_SLUG, "per_page": 20},
                timeout=30,
            )
            if r2.ok:
                exact = [
                    t
                    for t in r2.json()
                    if t.get("name") == TAG_NAME and int(t.get("id") or 0) != FORBIDDEN_TAG_ID
                ]
        if exact:
            tag_id = int(exact[0]["id"])
            print(f"[wp] tag {TAG_NAME} id={tag_id} count={exact[0].get('count')}", flush=True)
            return tag_id

        r3 = self.s.post(
            f"{WP}/wp-json/wp/v2/tags",
            headers={"X-WP-Nonce": self.nonce},
            json={"name": TAG_NAME, "slug": TAG_SLUG},
            timeout=30,
        )
        if r3.status_code >= 400:
            raise RuntimeError(f"create tag failed {r3.status_code}: {r3.text[:400]}")
        created = r3.json()
        tag_id = int(created["id"])
        if tag_id == FORBIDDEN_TAG_ID:
            raise RuntimeError("refusing to use FR tag id=60")
        print(f"[wp] created tag {TAG_NAME} id={tag_id}", flush=True)
        return tag_id

    def francais_count(self) -> int:
        r = self.s.get(f"{WP}/wp-json/wp/v2/tags/{self.tag_id}", timeout=30)
        r.raise_for_status()
        return int(r.json().get("count") or 0)

    def upload_media(self, path: Path, alt: str, title: str) -> dict:
        last_err = ""
        for attempt in range(6):
            data = path.read_bytes()
            r = self.s.post(
                f"{WP}/wp-json/wp/v2/media",
                headers={
                    "Content-Disposition": f'attachment; filename="{path.name}"',
                    "Content-Type": "image/jpeg",
                    "X-WP-Nonce": self.nonce,
                },
                data=data,
                timeout=120,
            )
            if r.status_code < 400:
                break
            last_err = f"{r.status_code}: {r.text[:400]}"
            if r.status_code in {401, 403}:
                self.login()
            print(f"[wp] media upload retry {attempt + 1}/6: {last_err[:120]}", flush=True)
            time.sleep(3 * (attempt + 1))
        else:
            raise RuntimeError(f"media upload failed {last_err}")

        media = r.json()
        mid = media["id"]
        r2 = self.s.post(
            f"{WP}/wp-json/wp/v2/media/{mid}",
            headers={"X-WP-Nonce": self.nonce},
            json={"alt_text": alt, "title": title},
            timeout=60,
        )
        if r2.status_code >= 400:
            print(f"[wp] warn alt/title update {r2.status_code}", flush=True)
        media = r2.json() if r2.ok else media
        print(f"[media] id={media['id']} {media.get('source_url')}", flush=True)
        return media

    def create_post(self, title: str, description: str, content: str, featured_media: int) -> dict:
        last_err = ""
        payload = {
            "title": title,
            "content": content,
            "excerpt": description,
            "status": "publish",
            "tags": [self.tag_id],
            "featured_media": featured_media,
        }
        for attempt in range(6):
            r = self.s.post(
                f"{WP}/wp-json/wp/v2/posts",
                headers={"X-WP-Nonce": self.nonce},
                json=payload,
                timeout=120,
            )
            if r.status_code < 400:
                return r.json()
            last_err = f"{r.status_code}: {r.text[:500]}"
            if r.status_code in {401, 403}:
                self.login()
            print(f"[wp] create post retry {attempt + 1}/6: {last_err[:120]}", flush=True)
            time.sleep(3 * (attempt + 1))
        raise RuntimeError(f"create post failed {last_err}")

    def set_yoast(
        self,
        post_id: int,
        seo_title: str,
        metadesc: str,
        content: str,
        featured_media: int,
        image_url: str,
    ) -> dict:
        edit = self.s.get(
            f"{WP}/wp-admin/post.php",
            params={"post": post_id, "action": "edit"},
            timeout=60,
        )
        edit.raise_for_status()

        m = re.search(r'name="yoast_free_metabox_nonce"\s+value="([^"]+)"', edit.text) or re.search(
            r'id="yoast_free_metabox_nonce"[^>]*value="([^"]+)"', edit.text
        )
        if not m:
            m2 = re.search(r'name="([^"]*yoast[^"]*nonce[^"]*)"\s+value="([^"]+)"', edit.text, re.I)
            yoast_nonce = m2.group(2) if m2 else ""
            yoast_field = m2.group(1) if m2 else "yoast_free_metabox_nonce"
        else:
            yoast_nonce = m.group(1)
            yoast_field = "yoast_free_metabox_nonce"

        wpnonce = re.search(r'name="_wpnonce"\s+value="([^"]+)"', edit.text)
        data = {
            "_wpnonce": wpnonce.group(1) if wpnonce else "",
            "_wp_http_referer": f"/wp-admin/post.php?post={post_id}&action=edit",
            "post_ID": str(post_id),
            "post_title": seo_title,
            "content": content,
            "post_status": "publish",
            "post_type": "post",
            "save": "Update",
            "action": "editpost",
            yoast_field: yoast_nonce,
            "yoast_wpseo_title": seo_title,
            "yoast_wpseo_metadesc": metadesc,
            "yoast_wpseo_opengraph-title": seo_title,
            "yoast_wpseo_opengraph-description": metadesc,
            "yoast_wpseo_opengraph-image": image_url,
            "yoast_wpseo_twitter-title": seo_title,
            "yoast_wpseo_twitter-description": metadesc,
            "yoast_wpseo_twitter-image": image_url,
        }
        r = self.s.post(
            f"{WP}/wp-admin/post.php",
            data=data,
            timeout=120,
            allow_redirects=True,
        )
        print(f"[yoast] post.php status={r.status_code} url={r.url}", flush=True)

        r2 = self.s.post(
            f"{WP}/wp-json/wp/v2/posts/{post_id}",
            headers={"X-WP-Nonce": self.nonce},
            json={
                "content": content,
                "featured_media": featured_media,
                "status": "publish",
                "excerpt": metadesc,
                "tags": [self.tag_id],
            },
            timeout=120,
        )
        if r2.status_code >= 400:
            print(f"[yoast] warn REST re-post {r2.status_code}: {r2.text[:200]}", flush=True)
            return {}
        return r2.json()
