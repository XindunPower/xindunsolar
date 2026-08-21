#!/usr/bin/env python3
"""Normalize page 54 featured images to consistent 600x400 height."""

from __future__ import annotations

import json
import os
import re
import sys
import time
from io import BytesIO
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "output" / "duomi"
WP = "https://www.xindunsolar.com"
UA = "Mozilla/5.0 (compatible; XindunSpanishBot/1.0)"
TARGET_W, TARGET_H = 600, 400

POSTS = [
    {
        "post_id": 14364,
        "local": OUT / "a0_i0_expo-de-energia-fotovoltaica-snec-xindun-2020.webp",
        "out": OUT / "a0_i0_expo-de-energia-fotovoltaica-snec-xindun-2020-h400.webp",
    },
    {
        "post_id": 14367,
        "local": OUT / "a1_i0_exposicion-mundial-de-energia-solar-fotovoltaica-2020-en-guangzhou-xindun.webp",
        "out": OUT / "a1_i0_exposicion-mundial-de-energia-solar-fotovoltaica-2020-en-guangzhou-xindun-h400.webp",
    },
    {
        "post_id": 14370,
        "local": OUT / "a2_i0_carta-de-invitacion-de-xindun-para-la-exposicion-en-linea-de-la-industria-de-equipos-elect.webp",
        "out": OUT / "a2_i0_carta-de-invitacion-de-xindun-para-la-exposicion-en-linea-de-la-industria-de-equipos-elect-h400.webp",
    },
    {
        "post_id": 14373,
        "local": OUT / "a3_i0_fabricante-oem-del-inversor.webp",
        "out": OUT / "a3_i0_fabricante-oem-del-inversor-h400.webp",
    },
    {
        "post_id": 14376,
        "local": OUT / "a4_i0_inversor-de-potencia-total-wd.webp",
        "out": OUT / "a4_i0_inversor-de-potencia-total-wd-h400.webp",
    },
]


def encode_webp(img: Image.Image, dest: Path, max_kb: int = 100) -> None:
    quality = 90
    while quality >= 20:
        buf = BytesIO()
        img.save(buf, format="WEBP", quality=quality, method=6)
        data = buf.getvalue()
        if len(data) <= max_kb * 1024:
            dest.write_bytes(data)
            return
        quality -= 8
    buf = BytesIO()
    img.save(buf, format="WEBP", quality=16, method=6)
    dest.write_bytes(buf.getvalue())


def normalize_canvas(src: Path, dest: Path) -> tuple[int, int]:
    with Image.open(src) as im:
        img = im.convert("RGB")
    scale = min(TARGET_W / img.width, TARGET_H / img.height)
    nw = max(1, int(img.width * scale))
    nh = max(1, int(img.height * scale))
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), (255, 255, 255))
    canvas.paste(resized, ((TARGET_W - nw) // 2, (TARGET_H - nh) // 2))
    encode_webp(canvas, dest, 100)
    return canvas.size


class WPClient:
    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.nonce = ""

    def login(self) -> None:
        user = os.environ["WP_USER"]
        pw = os.environ["WP_APP_PASSWORD"]
        last_err = ""
        for attempt in range(8):
            try:
                self.s.cookies.clear()
                self.s.get(f"{WP}/wp-login.php", timeout=30)
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
                m = re.search(r"wpApiSettings\s*=\s*(\{.*?\});", admin.text)
                if not m:
                    raise RuntimeError("wpApiSettings nonce not found")
                self.nonce = json.loads(m.group(1))["nonce"]
                self.s.headers["X-WP-Nonce"] = self.nonce
                print("[wp] logged in", flush=True)
                return
            except Exception as exc:  # noqa: BLE001
                last_err = str(exc)
                time.sleep(5 * (attempt + 1))
        raise RuntimeError(f"WP login failed: {last_err}")

    def upload_media(self, path: Path, alt: str, title: str) -> dict:
        data = path.read_bytes()
        r = self.s.post(
            f"{WP}/wp-json/wp/v2/media",
            headers={
                "Content-Disposition": f'attachment; filename="{path.name}"',
                "Content-Type": "image/webp",
                "X-WP-Nonce": self.nonce,
            },
            data=data,
            timeout=120,
        )
        r.raise_for_status()
        media = r.json()
        r2 = self.s.post(
            f"{WP}/wp-json/wp/v2/media/{media['id']}",
            headers={"X-WP-Nonce": self.nonce},
            json={"alt_text": alt, "title": title},
            timeout=60,
        )
        return r2.json() if r2.ok else media

    def set_yoast(
        self,
        post_id: int,
        title: str,
        metadesc: str,
        content: str,
        featured_media: int,
        image_url: str,
    ) -> None:
        edit = self.s.get(
            f"{WP}/wp-admin/post.php",
            params={"post": post_id, "action": "edit"},
            timeout=60,
        )
        edit.raise_for_status()
        m = re.search(r'name="yoast_free_metabox_nonce"\s+value="([^"]+)"', edit.text)
        yoast_nonce = m.group(1) if m else ""
        wpnonce = re.search(r'name="_wpnonce"\s+value="([^"]+)"', edit.text)
        data = {
            "_wpnonce": wpnonce.group(1) if wpnonce else "",
            "_wp_http_referer": f"/wp-admin/post.php?post={post_id}&action=edit",
            "post_ID": str(post_id),
            "post_title": title,
            "content": content,
            "post_status": "publish",
            "post_type": "post",
            "save": "Update",
            "action": "editpost",
            "yoast_free_metabox_nonce": yoast_nonce,
            "yoast_wpseo_title": title,
            "yoast_wpseo_metadesc": metadesc,
            "yoast_wpseo_opengraph-title": title,
            "yoast_wpseo_opengraph-description": metadesc,
            "yoast_wpseo_opengraph-image": image_url,
            "yoast_wpseo_twitter-title": title,
            "yoast_wpseo_twitter-description": metadesc,
            "yoast_wpseo_twitter-image": image_url,
        }
        self.s.post(f"{WP}/wp-admin/post.php", data=data, timeout=120, allow_redirects=True)
        self.s.post(
            f"{WP}/wp-json/wp/v2/posts/{post_id}",
            headers={"X-WP-Nonce": self.nonce},
            json={"content": content, "featured_media": featured_media, "status": "publish"},
            timeout=120,
        )


def replace_first_img(content_html: str, new_url: str) -> str:
    soup = BeautifulSoup(content_html, "lxml")
    body = soup.body or soup
    img = body.find("img")
    if img:
        img["src"] = new_url
        for attr in ("width", "height", "srcset", "sizes"):
            img.attrs.pop(attr, None)
    if body.name == "body":
        return "".join(str(c) for c in body.children)
    return str(body)


def main() -> None:
    wp = WPClient()
    wp.login()
    results = []

    for item in POSTS:
        src = item["local"]
        dest = item["out"]
        if not src.exists():
            raise FileNotFoundError(src)

        wh = normalize_canvas(src, dest)
        print(f"[canvas] {src.name} -> {dest.name} {wh} {dest.stat().st_size}b", flush=True)

        post_id = item["post_id"]
        pr = wp.s.get(f"{WP}/wp-json/wp/v2/posts/{post_id}", timeout=60)
        pr.raise_for_status()
        post = pr.json()
        title = re.sub(r"<[^>]+>", "", post["title"]["rendered"])
        content = post["content"]["rendered"]

        old_media_id = post.get("featured_media")
        alt = title
        title_attr = title
        if old_media_id:
            mr = wp.s.get(f"{WP}/wp-json/wp/v2/media/{old_media_id}", timeout=30)
            if mr.ok:
                md = mr.json()
                alt = md.get("alt_text") or alt
                title_attr = md.get("title", {}).get("rendered") or alt

        media = wp.upload_media(dest, alt, title_attr)
        new_url = media["source_url"]
        new_content = replace_first_img(content, new_url)

        wp.set_yoast(
            post_id,
            title,
            title,
            new_content,
            media["id"],
            new_url,
        )

        verify = wp.s.get(f"{WP}/wp-json/wp/v2/media/{media['id']}", timeout=30).json()
        vw = verify.get("media_details", {}).get("width")
        vh = verify.get("media_details", {}).get("height")
        results.append(
            {
                "post_id": post_id,
                "title": title,
                "media_id": media["id"],
                "url": new_url,
                "size": f"{vw}x{vh}",
            }
        )
        print(f"[ok] post={post_id} media={media['id']} {vw}x{vh} {new_url}", flush=True)

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
