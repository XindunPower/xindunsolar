#!/usr/bin/env python3
"""Publish xindun-power news page from progress.json to Spanish WordPress."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator
from PIL import Image, ImageChops, ImageStat

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "output" / "duomi"
OUT.mkdir(parents=True, exist_ok=True)
PROGRESS_PATH = REPO / "progress.json"

WP = "https://www.xindunsolar.com"
SOURCE_HOST = "https://www.xindun-power.com"
CAT = 89
UA = "Mozilla/5.0 (compatible; XindunSpanishBot/1.0)"

PROMPT_BASE = (
    "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. "
    "Only translate English marketing/diagram overlay text to Spanish. "
    "Do NOT change product casing text, logos, model numbers, certificates, "
    "Chinese exhibition signs, or wall company names "
    "(Xindun / Xindun GREEN POWER / XINDUN POWER)."
)

# Page-49-specific overlay translation instructions (URL -> {image_index: prompt}).
DUOMI_RULES_BY_URL = {
    "https://www.xindun-power.com/faq/what-means-off-grid-solar-system.html": {
        0: (
            "Translate only diagram labels to Spanish: "
            "'Solar Panels' -> 'Paneles solares'; "
            "'Solar Generator' -> 'Generador solar'; "
            "'Power grid' -> 'Red eléctrica'. "
            "Keep house illustration, product photo, logo, wiring colors, layout and background unchanged. "
            "Do not redesign."
        )
    }
}

IMAGE_LOG: list[dict] = []


def normalize_source_url(url: str) -> str:
    parsed = urlparse(url.strip())
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc or "www.xindun-power.com"
    path = parsed.path or "/"
    return f"{scheme}://{netloc}{path}"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:90] or "imagen"


def clean_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\xa0", " ").replace("Â", "")).strip()


def translate_text(text: str, retries: int = 5) -> str:
    text = clean_spaces(text)
    if not text:
        return text
    if not re.search(r"[A-Za-zÀ-ÿ]", text):
        return text
    for attempt in range(retries):
        try:
            translated = GoogleTranslator(source="en", target="es").translate(text)
            if translated and not re.search(r"Error\s*500|Server Error", translated, re.I):
                return translated
        except Exception as exc:  # noqa: BLE001
            print(f"[translate] retry {attempt + 1}/{retries}: {exc}", flush=True)
        time.sleep(2 * (attempt + 1))
    print(f"[translate] fallback to original: {text[:80]!r}", flush=True)
    return text


def translate_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    body = soup.body or soup
    for node in list(body.descendants):
        if not isinstance(node, NavigableString):
            continue
        parent = node.parent
        if parent is None or parent.name in {"script", "style"}:
            continue
        raw = str(node)
        if not raw.strip() or not re.search(r"[A-Za-z]", raw):
            continue
        node.replace_with(translate_text(raw))
        time.sleep(0.08)
    for a in body.find_all("a"):
        a.unwrap()
    if body.name == "body":
        return "".join(str(c) for c in body.children)
    return str(body)


def prepend_18pt_title(content_html: str, title_es: str) -> str:
    return f'<p><span style="font-size: 18pt;">{title_es}</span></p>{content_html}'


def size_for(w: int, h: int) -> str:
    ratio = w / h if h else 1.0
    candidates = {
        "1:1": 1.0,
        "3:2": 1.5,
        "2:3": 2 / 3,
        "16:9": 16 / 9,
        "9:16": 9 / 16,
        "4:3": 4 / 3,
        "3:4": 3 / 4,
    }
    return min(candidates.items(), key=lambda kv: abs(kv[1] - ratio))[0]


def save_jpeg_under_100kb(
    img_or_bytes: Path | bytes,
    dest: Path,
    target_wh: tuple[int, int],
    max_kb: int = 100,
) -> None:
    if isinstance(img_or_bytes, bytes):
        img = Image.open(BytesIO(img_or_bytes)).convert("RGB")
    else:
        img = Image.open(img_or_bytes).convert("RGB")
    if img.size != target_wh:
        img = img.resize(target_wh, Image.Resampling.LANCZOS)
    for quality in (92, 88, 84, 80, 76, 72, 68, 64, 60, 56, 52, 48, 44, 40, 36, 32, 28, 24, 20):
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
        if len(buf.getvalue()) <= max_kb * 1024:
            dest.write_bytes(buf.getvalue())
            return
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=16, optimize=True, progressive=True)
    dest.write_bytes(buf.getvalue())
    if dest.stat().st_size > max_kb * 1024:
        raise RuntimeError(f"Cannot compress {dest.name} under {max_kb}KB without resizing")


def visual_delta_score(orig: Path, candidate: Path, target_wh: tuple[int, int]) -> float:
    with Image.open(orig).convert("RGB") as orig_img, Image.open(candidate).convert("RGB") as cand_img:
        if orig_img.size != target_wh:
            orig_img = orig_img.resize(target_wh, Image.Resampling.LANCZOS)
        if cand_img.size != target_wh:
            cand_img = cand_img.resize(target_wh, Image.Resampling.LANCZOS)
        diff = ImageChops.difference(orig_img, cand_img)
        stat = ImageStat.Stat(diff)
        mean = sum(stat.mean) / max(1, len(stat.mean))
        return float(mean)


def run_duomi(
    image_url: str,
    extra_prompt: str,
    output_name: str,
    size: str,
    orig_path: Path,
    orig_wh: tuple[int, int],
    attempts: int = 4,
) -> Path:
    prompt = f"{PROMPT_BASE} {extra_prompt}"
    final = OUT / f"{output_name}.jpg"
    for attempt in range(1, attempts + 1):
        duomi_name = f"{output_name}-duomi-try{attempt}"
        cmd = [
            "python3",
            str(REPO / "scripts" / "duomi_image.py"),
            "--image-url",
            image_url,
            "--prompt",
            prompt,
            "--size",
            size,
            "--output-name",
            duomi_name,
            "--max-kb",
            "100",
            "--print-json",
            "--timeout",
            "600",
        ]
        print(f"[duomi] {output_name} attempt={attempt} size={size}", flush=True)
        proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
        files: list[str] = []
        for line in (proc.stdout or "").splitlines()[::-1]:
            line = line.strip()
            if line.startswith("{"):
                try:
                    files = json.loads(line).get("files") or []
                    if files:
                        break
                except Exception:  # noqa: BLE001
                    pass
            if line.startswith("SUCCESS:"):
                files = [line.split("SUCCESS:", 1)[1].strip()]
                break
        if not files:
            stderr = (proc.stderr or "")[-500:]
            print(f"[duomi] no output file, stderr={stderr}", flush=True)
            time.sleep(5)
            continue
        raw = Path(files[0])
        if not raw.exists() or raw.stat().st_size == 0:
            print(f"[duomi] output path missing: {raw}", flush=True)
            time.sleep(3)
            continue
        with Image.open(raw) as test_img:
            cw, ch = test_img.size
        src_ratio = orig_wh[0] / orig_wh[1]
        out_ratio = cw / ch if ch else 1.0
        if abs(src_ratio - out_ratio) > 0.06:
            print(f"[duomi] reject aspect {cw}x{ch} vs original {orig_wh}", flush=True)
            time.sleep(3)
            continue
        delta = visual_delta_score(orig_path, raw, orig_wh)
        # Text-only edits should be close to source; high delta indicates redesign.
        if delta > 45.0:
            print(f"[duomi] reject redesign-like delta={delta:.2f}", flush=True)
            time.sleep(3)
            continue
        save_jpeg_under_100kb(raw, final, orig_wh, max_kb=100)
        print(f"[duomi] accepted delta={delta:.2f} -> {final}", flush=True)
        if final.stat().st_size > 100 * 1024:
            raise RuntimeError(f"Duomi output still exceeds 100KB: {final}")
        return final
    raise RuntimeError(f"Duomi failed to produce valid layout-preserving output for {output_name}")


def download_source_image(src: str, article_idx: int, img_idx: int) -> Path:
    ext = Path(urlparse(src).path).suffix.lower() or ".jpg"
    local = OUT / f"_src_a{article_idx}_i{img_idx}{ext}"
    if local.exists() and local.stat().st_size > 0:
        return local
    r = requests.get(src, timeout=60, headers={"User-Agent": UA})
    r.raise_for_status()
    local.write_bytes(r.content)
    return local


def parse_news_page(page_no: int) -> list[dict]:
    url = f"{SOURCE_HOST}/news/{page_no}.html"
    r = requests.get(url, timeout=60, headers={"User-Agent": UA})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    items: list[dict] = []
    for div in soup.select("div.title.clearfix"):
        a = div.find("a")
        if not a:
            continue
        title = clean_spaces(a.get("title") or a.get_text(" ", strip=True))
        href = (a.get("href") or "").strip()
        if not href:
            continue
        if href.startswith("//"):
            href = "https:" + href
        elif href.startswith("/"):
            href = urljoin(SOURCE_HOST, href)
        elif not href.startswith("http"):
            href = urljoin(SOURCE_HOST + "/", href.lstrip("./"))
        items.append({"title_en": title, "url": normalize_source_url(href)})
    if len(items) < 5:
        raise RuntimeError(f"News page {page_no} has only {len(items)} items")
    return items[:5]


def fetch_article(url: str) -> dict:
    html = requests.get(url, timeout=60, headers={"User-Agent": UA}).text
    soup = BeautifulSoup(html, "lxml")
    title = clean_spaces((soup.find("h1") or soup.find("title")).get_text(" ", strip=True))
    md = soup.find("meta", attrs={"name": "description"})
    desc = clean_spaces(md.get("content", "") if md else "")
    box = soup.select_one(".pageNewsDetailsBox") or soup.select_one("#pageNewsDetailsBox")
    if not box:
        for selector in [".news-detail", ".content", ".detail", ".article"]:
            box = soup.select_one(selector)
            if box:
                break
    if box:
        for marker in box.find_all(string=re.compile(r"Related\s+posts", re.I)):
            parent = marker.parent
            for sib in list(parent.next_siblings):
                if getattr(sib, "decompose", None):
                    sib.decompose()
            parent.decompose()
            break
        for rel in box.find_all(class_=re.compile(r"related", re.I)):
            rel.decompose()
    images: list[dict] = []
    if box:
        for img in box.find_all("img"):
            src = (img.get("src") or img.get("data-src") or "").strip()
            if src.startswith("//"):
                src = "https:" + src
            elif src.startswith("/"):
                src = urljoin(SOURCE_HOST, src)
            elif src and not src.startswith("http"):
                src = urljoin(SOURCE_HOST + "/", src.lstrip("./"))
            images.append(
                {
                    "src": normalize_source_url(src),
                    "alt": clean_spaces(img.get("alt") or ""),
                    "title": clean_spaces(img.get("title") or img.get("alt") or ""),
                }
            )
    return {
        "url": normalize_source_url(url),
        "title": title,
        "description": desc,
        "images": images,
        "content_html": str(box) if box else "",
    }


class WPClient:
    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.nonce = ""

    def login(self) -> None:
        user = os.environ.get("WP_USER", "").strip()
        pw = os.environ.get("WP_PASSWORD", "").strip() or os.environ.get("WP_APP_PASSWORD", "").strip()
        if not user or not pw:
            raise RuntimeError("Missing WP_USER or WP_PASSWORD/WP_APP_PASSWORD in environment")
        last_error = ""
        for attempt in range(8):
            try:
                self.s.cookies.clear()
                login_get = self.s.get(f"{WP}/wp-login.php", timeout=30)
                if login_get.status_code >= 500:
                    raise RuntimeError(f"wp-login GET {login_get.status_code}")
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
                match = re.search(r"wpApiSettings\s*=\s*(\{.*?\});", admin.text)
                if not match:
                    raise RuntimeError("wpApiSettings nonce not found")
                self.nonce = json.loads(match.group(1))["nonce"]
                self.s.headers["X-WP-Nonce"] = self.nonce
                print("[wp] logged in and nonce acquired", flush=True)
                return
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
                print(f"[wp] login retry {attempt + 1}/8: {last_error}", flush=True)
                time.sleep(5 * (attempt + 1))
        raise RuntimeError(f"WP login failed: {last_error}")

    def upload_media(self, path: Path, alt: str, title: str) -> dict:
        last_error = ""
        for attempt in range(6):
            resp = self.s.post(
                f"{WP}/wp-json/wp/v2/media",
                headers={
                    "Content-Disposition": f'attachment; filename="{path.name}"',
                    "Content-Type": "image/jpeg",
                    "X-WP-Nonce": self.nonce,
                },
                data=path.read_bytes(),
                timeout=120,
            )
            if resp.status_code < 400:
                media = resp.json()
                media_id = media["id"]
                upd = self.s.post(
                    f"{WP}/wp-json/wp/v2/media/{media_id}",
                    headers={"X-WP-Nonce": self.nonce},
                    json={"alt_text": alt, "title": title},
                    timeout=60,
                )
                if upd.ok:
                    media = upd.json()
                return media
            last_error = f"{resp.status_code}: {resp.text[:300]}"
            if resp.status_code in {401, 403}:
                self.login()
            print(f"[wp] media upload retry {attempt + 1}/6: {last_error}", flush=True)
            time.sleep(3 * (attempt + 1))
        raise RuntimeError(f"media upload failed: {last_error}")

    def create_post(self, title: str, content: str, featured_media: int) -> dict:
        last_error = ""
        for attempt in range(6):
            resp = self.s.post(
                f"{WP}/wp-json/wp/v2/posts",
                headers={"X-WP-Nonce": self.nonce},
                json={
                    "title": title,
                    "content": content,
                    "status": "publish",
                    "categories": [CAT],
                    "featured_media": featured_media,
                },
                timeout=120,
            )
            if resp.status_code < 400:
                return resp.json()
            last_error = f"{resp.status_code}: {resp.text[:500]}"
            if resp.status_code in {401, 403}:
                self.login()
            print(f"[wp] create post retry {attempt + 1}/6: {last_error}", flush=True)
            time.sleep(3 * (attempt + 1))
        raise RuntimeError(f"create post failed: {last_error}")

    def set_yoast(
        self,
        post_id: int,
        title: str,
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
        nonce_match = re.search(r'name="yoast_free_metabox_nonce"\s+value="([^"]+)"', edit.text) or re.search(
            r'id="yoast_free_metabox_nonce"[^>]*value="([^"]+)"', edit.text
        )
        if nonce_match:
            yoast_field = "yoast_free_metabox_nonce"
            yoast_nonce = nonce_match.group(1)
        else:
            fallback = re.search(r'name="([^"]*yoast[^"]*nonce[^"]*)"\s+value="([^"]+)"', edit.text, re.I)
            yoast_field = fallback.group(1) if fallback else "yoast_free_metabox_nonce"
            yoast_nonce = fallback.group(2) if fallback else ""
        wpnonce = re.search(r'name="_wpnonce"\s+value="([^"]+)"', edit.text)
        payload = {
            "_wpnonce": wpnonce.group(1) if wpnonce else "",
            "_wp_http_referer": f"/wp-admin/post.php?post={post_id}&action=edit",
            "post_ID": str(post_id),
            "post_title": title,
            "content": content,
            "post_status": "publish",
            "post_type": "post",
            "save": "Update",
            "action": "editpost",
            yoast_field: yoast_nonce,
            "yoast_wpseo_title": title,
            "yoast_wpseo_metadesc": metadesc,
            "yoast_wpseo_opengraph-title": title,
            "yoast_wpseo_opengraph-description": metadesc,
            "yoast_wpseo_opengraph-image": image_url,
            "yoast_wpseo_twitter-title": title,
            "yoast_wpseo_twitter-description": metadesc,
            "yoast_wpseo_twitter-image": image_url,
        }
        update_resp = self.s.post(f"{WP}/wp-admin/post.php", data=payload, timeout=120, allow_redirects=True)
        print(f"[yoast] post.php status={update_resp.status_code}", flush=True)
        rest = self.s.post(
            f"{WP}/wp-json/wp/v2/posts/{post_id}",
            headers={"X-WP-Nonce": self.nonce},
            json={"content": content, "featured_media": featured_media, "status": "publish"},
            timeout=120,
        )
        if rest.status_code >= 400:
            print(f"[yoast] warn rest post update {rest.status_code}: {rest.text[:200]}", flush=True)
            return {}
        return rest.json()


def replace_images_in_html(content_html_es: str, prepared: list[dict], media_list: list[dict]) -> str:
    soup = BeautifulSoup(content_html_es, "lxml")
    body = soup.body or soup
    imgs = body.find_all("img")
    for idx, img in enumerate(imgs):
        if idx >= len(media_list):
            break
        media = media_list[idx]
        img["src"] = media.get("source_url", img.get("src", ""))
        img["alt"] = prepared[idx]["alt_es"]
        img["title"] = prepared[idx]["title_es"]
        for attr in ("width", "height", "srcset", "sizes"):
            if attr in img.attrs:
                del img.attrs[attr]
    if body.name == "body":
        return "".join(str(c) for c in body.children)
    return str(body)


def prepare_images(article_idx: int, article_url: str, imgs: list[dict]) -> list[dict]:
    prepared: list[dict] = []
    used_names: set[str] = set()
    duomi_rules = DUOMI_RULES_BY_URL.get(normalize_source_url(article_url), {})
    for img_idx, img in enumerate(imgs):
        alt_en = img["alt"] or f"imagen-{article_idx}-{img_idx}"
        alt_es = translate_text(alt_en)
        title_es = translate_text(img.get("title") or alt_en)
        base = slugify(alt_es)
        filename = base
        suffix = 2
        while filename in used_names:
            filename = f"{base}-{suffix}"
            suffix += 1
        used_names.add(filename)

        local_src = download_source_image(img["src"], article_idx, img_idx)
        with Image.open(local_src) as src_img:
            orig_wh = src_img.size

        final = OUT / f"{filename}.jpg"
        method = "compress"
        duomi_output = None
        if img_idx in duomi_rules:
            method = "duomi"
            duomi_output = run_duomi(
                image_url=img["src"],
                extra_prompt=duomi_rules[img_idx],
                output_name=filename,
                size=size_for(*orig_wh),
                orig_path=local_src,
                orig_wh=orig_wh,
            )
            final = duomi_output
        else:
            save_jpeg_under_100kb(local_src, final, orig_wh, max_kb=100)

        if final.stat().st_size > 100 * 1024:
            raise RuntimeError(f"Image over 100KB: {final}")
        with Image.open(final) as chk:
            if chk.size != orig_wh:
                raise RuntimeError(f"Image dimensions changed for {final.name}: {chk.size} != {orig_wh}")

        info = {
            "local": final,
            "alt_es": alt_es,
            "title_es": title_es,
            "src_orig": img["src"],
            "method": method,
            "duomi_path": str(duomi_output) if duomi_output else None,
            "orig_wh": orig_wh,
            "bytes": final.stat().st_size,
        }
        prepared.append(info)
        IMAGE_LOG.append(
            {
                "article_index": article_idx,
                "image_index": img_idx,
                "article_url": article_url,
                "src_orig": img["src"],
                "method": method,
                "local": str(final),
                "duomi_path": str(duomi_output) if duomi_output else None,
                "orig_wh": list(orig_wh),
                "bytes": final.stat().st_size,
                "alt_es": alt_es,
                "title_es": title_es,
            }
        )
        print(
            f"[img] article={article_idx} img={img_idx} method={method} file={final.name} bytes={final.stat().st_size}",
            flush=True,
        )
    return prepared


def already_published(title_es: str, title_en: str) -> str | None:
    stopwords = {
        "cual",
        "cuál",
        "para",
        "como",
        "cómo",
        "que",
        "qué",
        "esta",
        "este",
        "from",
        "with",
        "what",
        "when",
        "where",
        "mejor",
        "best",
        "solar",
        "paneles",
        "panels",
        "sistema",
        "system",
        "energia",
        "energía",
        "power",
        "the",
        "and",
        "for",
        "inversor",
        "inverter",
        "inversores",
        "phase",
        "fase",
        "company",
        "empresa",
        "famous",
        "famosa",
        "wholesale",
        "mayorista",
        "suitable",
        "adecuado",
        "which",
        "find",
        "encontrar",
    }

    def tokens(text: str) -> set[str]:
        return {
            tok
            for tok in re.split(r"[^a-z0-9áéíóúñü]+", text.lower())
            if len(tok) > 3 and tok not in stopwords
        }

    session = requests.Session()
    session.headers["User-Agent"] = UA
    for query in {title_es, title_en}:
        q = clean_spaces(query)
        if len(q) < 8:
            continue
        try:
            resp = session.get(
                f"{WP}/wp-json/wp/v2/posts",
                params={"search": q, "categories": CAT, "per_page": 10, "status": "publish"},
                timeout=30,
            )
            if not resp.ok:
                continue
            q_tokens = tokens(q)
            for post in resp.json():
                rendered = re.sub(r"<[^>]+>", "", (post.get("title") or {}).get("rendered") or "")
                rendered = clean_spaces(rendered.lower())
                ql = q.lower()
                if rendered == ql or rendered.rstrip("?") == ql.rstrip("?"):
                    return post.get("link")
                shared = tokens(rendered) & q_tokens
                if len(q_tokens) >= 2 and len(shared) >= max(2, len(q_tokens) - 1):
                    if abs(len(rendered) - len(ql)) <= 12:
                        return post.get("link")
        except Exception:  # noqa: BLE001
            continue
    return None


def load_progress() -> dict:
    if PROGRESS_PATH.exists():
        return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    progress = {"page": 27}
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    return progress


def save_results(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def process_page() -> tuple[int, list[dict], Path]:
    progress = load_progress()
    page_no = int(progress.get("page", 27))
    if page_no <= 26:
        raise RuntimeError(f"Refusing to redo page {page_no}; expected page >= 27")

    source_page = f"{SOURCE_HOST}/news/{page_no}.html"
    articles = parse_news_page(page_no)
    print(f"[source] page={page_no} articles={len(articles)} from {source_page}", flush=True)

    wp = WPClient()
    wp.login()

    results: list[dict] = []
    only = os.environ.get("ONLY_ARTICLE")
    only_idxs = {int(x) for x in only.split(",")} if only else None

    for idx, article in enumerate(articles):
        if only_idxs is not None and idx not in only_idxs:
            continue
        print("=" * 72, flush=True)
        print(f"ARTICLE {idx}: {article['title_en']} | {article['url']}", flush=True)
        try:
            raw = fetch_article(article["url"])
            title_en = article["title_en"] or raw["title"]
            title_es = translate_text(title_en)
            desc_source = raw.get("description") or title_en
            desc_es = translate_text(desc_source)

            existing = already_published(title_es, title_en)
            if existing and os.environ.get("FORCE_PUBLISH") != "1":
                print(f"[skip] already published: {existing}", flush=True)
                results.append(
                    {
                        "title_en": title_en,
                        "title_es": title_es,
                        "url": existing,
                        "status": "already_published",
                        "source_url": article["url"],
                    }
                )
                continue

            prepared = prepare_images(idx, article["url"], raw["images"])
            content_es = translate_html(raw["content_html"])
            if re.search(r"Error\s*500|Server Error", content_es, re.I):
                print("[translate] found Error 500 marker; retrying", flush=True)
                time.sleep(5)
                content_es = translate_html(raw["content_html"])
                if re.search(r"Error\s*500|Server Error", content_es, re.I):
                    raise RuntimeError("Google Translate Error 500 marker persists in article body")
            content_es = prepend_18pt_title(content_es, title_es)

            media_list: list[dict] = []
            for prepared_img in prepared:
                media = wp.upload_media(prepared_img["local"], prepared_img["alt_es"], prepared_img["title_es"])
                media_list.append(media)
            content_es = replace_images_in_html(content_es, prepared, media_list)
            featured_id = media_list[0]["id"] if media_list else 0
            featured_url = media_list[0].get("source_url", "") if media_list else ""

            post = wp.create_post(title_es, content_es, featured_id)
            print(f"[post] id={post['id']} link={post.get('link')}", flush=True)
            wp.set_yoast(
                post_id=post["id"],
                title=title_es,
                metadesc=desc_es,
                content=content_es,
                featured_media=featured_id,
                image_url=featured_url,
            )
            results.append(
                {
                    "title_en": title_en,
                    "title_es": title_es,
                    "url": post.get("link"),
                    "status": "published",
                    "post_id": post["id"],
                    "source_url": article["url"],
                }
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[error] article {idx} failed: {exc}", flush=True)
            results.append(
                {
                    "title_en": article["title_en"],
                    "title_es": "",
                    "url": "",
                    "status": "failed",
                    "source_url": article["url"],
                    "reason": str(exc),
                }
            )

    results_path = Path(f"/tmp/page{page_no}_results.json")
    save_results(
        results_path,
        {
            "page": page_no,
            "source": source_page,
            "results": results,
            "images": IMAGE_LOG,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    failures = [r for r in results if r["status"] == "failed"]
    if failures:
        raise RuntimeError(f"Page {page_no} has failures; not updating progress.json")
    if len(results) != 5:
        raise RuntimeError(f"Expected 5 results, got {len(results)}; not updating progress.json")

    today = datetime.now(timezone.utc).date().isoformat()
    progress["page"] = page_no + 1
    progress["last_completed_page"] = page_no
    progress["note"] = f"page {page_no} completed {today}; next pending page is {page_no + 1}"
    progress["last_run"] = {
        "date": today,
        "source": source_page,
        "published": [
            {
                "title_en": row["title_en"],
                "title_es": row["title_es"],
                "url": row["url"],
                "status": row["status"],
            }
            for row in results
        ],
    }
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    return page_no, results, results_path


def main() -> None:
    page_no, results, results_path = process_page()
    print(
        json.dumps(
            {"ok": True, "page": page_no, "results_path": str(results_path), "results": results},
            ensure_ascii=False,
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", file=sys.stderr)
        sys.exit(1)
