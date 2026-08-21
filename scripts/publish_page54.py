#!/usr/bin/env python3
"""Publish xindun-power news page 54 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
import unicodedata
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator
from PIL import Image, ImageChops, ImageStat

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "output" / "duomi"
OUT.mkdir(parents=True, exist_ok=True)
WP = "https://www.xindunsolar.com"
CAT = 89
UA = "Mozilla/5.0 (compatible; XindunSpanishBot/1.0)"
PAGE_NUM = 54
NEWS_URL = f"https://www.xindun-power.com/news/{PAGE_NUM}.html"
RESULTS_PATH = Path(f"/tmp/page{PAGE_NUM}_results.json")

PROMPT_BASE = (
    "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. "
    "Only translate English marketing/diagram overlay text to Spanish. "
    "Do NOT change product casing text, logos, model numbers, certificates, "
    "Chinese exhibition signs, or wall company names "
    "(Xindun / Xindun GREEN POWER / XINDUN POWER)."
)

# Only images with English marketing/diagram overlays use Duomi.
DUOMI_MAP = {
    (0, 0): (
        "Translate exhibition invitation poster English text to Spanish. "
        "Keep Xindun/XINDUN company name, SNEC logo, dates, booth/hall numbers, "
        "and overall poster layout unchanged. Do not redesign."
    ),
    (1, 0): (
        "Translate Guangzhou Solar PV World Expo invitation poster English text to Spanish. "
        "Keep Xindun/XINDUN company name, logos, dates, booth numbers, "
        "and poster layout unchanged. Do not redesign."
    ),
    (2, 0): (
        "Translate online expo invitation letter English text to Spanish. "
        "Keep Xindun company name, logos, dates, URLs, and letter layout unchanged. "
        "Do not redesign or add products."
    ),
}

IMAGE_LOG: list[dict] = []


def clean_spaces(text: str) -> str:
    text = (text or "").replace("\xa0", " ").replace("Â", " ").strip()
    return re.sub(r"\s+", " ", text).strip()


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:90] or "imagen"


def translate_text(text: str, retries: int = 5) -> str:
    text = clean_spaces(text)
    if not text:
        return text
    if not re.search(r"[A-Za-zÀ-ÿ]", text):
        return text
    for attempt in range(retries):
        try:
            out = GoogleTranslator(source="en", target="es").translate(text)
            if out and not re.search(r"Error\s*500|Server Error", out, re.I):
                return clean_spaces(out)
        except Exception as exc:  # noqa: BLE001
            print(f"[translate] retry {attempt + 1}: {exc}", flush=True)
        time.sleep(2 * (attempt + 1))
    print(f"[translate] fallback keep original: {text[:60]!r}", flush=True)
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
        time.sleep(0.12)
    # Remove all links in body per publishing rule.
    for a in body.find_all("a"):
        a.unwrap()
    if body.name == "body":
        return "".join(str(c) for c in body.children)
    return str(body)


def prepend_18pt_title(content_html: str, title_es: str) -> str:
    return f'<p><span style="font-size: 18pt;">{title_es}</span></p>' + content_html


def size_for(w: int, h: int) -> str:
    r = w / h if h else 1.0
    candidates = {
        "1:1": 1.0,
        "3:2": 1.5,
        "2:3": 2 / 3,
        "16:9": 16 / 9,
        "9:16": 9 / 16,
        "4:3": 4 / 3,
        "3:4": 3 / 4,
    }
    return min(candidates.items(), key=lambda kv: abs(kv[1] - r))[0]


def encode_webp(src: Path, dest: Path, tw: int, th: int, max_kb: int = 100) -> None:
    with Image.open(src) as im:
        img = im.convert("RGB")
    if img.size != (tw, th):
        img = img.resize((tw, th), Image.Resampling.LANCZOS)
    quality = 90
    while quality >= 20:
        buf = BytesIO()
        img.save(buf, format="WEBP", quality=quality, method=6)
        data = buf.getvalue()
        if len(data) <= max_kb * 1024:
            dest.write_bytes(data)
            return
        quality -= 8
    # Last resort keeps dimensions unchanged and prioritizes size cap.
    buf = BytesIO()
    img.save(buf, format="WEBP", quality=16, method=6)
    dest.write_bytes(buf.getvalue())


def image_mean_diff(orig: Path, candidate: Path, tw: int, th: int) -> float:
    with Image.open(orig) as im1, Image.open(candidate) as im2:
        a = im1.convert("RGB").resize((tw, th), Image.Resampling.BICUBIC)
        b = im2.convert("RGB").resize((tw, th), Image.Resampling.BICUBIC)
    diff = ImageChops.difference(a, b)
    mean_rgb = ImageStat.Stat(diff).mean
    return float(sum(mean_rgb) / len(mean_rgb))


def compress_only(local: Path, name: str, orig_wh: tuple[int, int]) -> Path:
    dest = OUT / f"{name}.webp"
    encode_webp(local, dest, orig_wh[0], orig_wh[1], 100)
    return dest


def run_duomi(
    image_url: str,
    extra_prompt: str,
    name: str,
    size: str,
    orig_wh: tuple[int, int],
    orig_path: Path,
    attempts: int = 4,
) -> Path | None:
    prompt = f"{PROMPT_BASE} {extra_prompt}"
    final = OUT / f"{name}.webp"
    for attempt in range(attempts):
        out_name = f"{name}-try{attempt}"
        print(f"[duomi] {name} attempt={attempt + 1} size={size}", flush=True)
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
            out_name,
            "--max-kb",
            "0",
            "--print-json",
            "--timeout",
            "600",
        ]
        p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
        files: list[str] = []
        for line in (p.stdout or "").splitlines()[::-1]:
            line = line.strip()
            if line.startswith("{"):
                try:
                    files = json.loads(line).get("files") or []
                    break
                except Exception:  # noqa: BLE001
                    pass
            if line.startswith("SUCCESS:"):
                files = [line.split("SUCCESS:", 1)[1].strip()]
                break
        if not files:
            print(f"[duomi] no files stderr={(p.stderr or '')[-400:]}", flush=True)
            time.sleep(5)
            continue

        raw = Path(files[0])
        if not raw.exists():
            print(f"[duomi] output missing: {raw}", flush=True)
            time.sleep(3)
            continue

        try:
            with Image.open(raw) as chk:
                cw, ch = chk.size
            ratio_delta = abs((cw / ch) - (orig_wh[0] / orig_wh[1]))
            if ratio_delta > 0.05:
                print(f"[duomi] reject ratio {cw}x{ch} vs {orig_wh}", flush=True)
                time.sleep(3)
                continue
            diff_score = image_mean_diff(orig_path, raw, orig_wh[0], orig_wh[1])
            # Large visual drift usually means redesign; reject and retry.
            if diff_score > 28.0:
                print(f"[duomi] reject redesign diff={diff_score:.2f}", flush=True)
                time.sleep(3)
                continue
            encode_webp(raw, final, orig_wh[0], orig_wh[1], 100)
        except Exception as exc:  # noqa: BLE001
            print(f"[duomi] layout/compress failed: {exc}", flush=True)
            time.sleep(3)
            continue
        if final.exists() and final.stat().st_size > 0:
            return final
    return None


def fetch_page_articles(page_num: int) -> list[dict]:
    url = f"https://www.xindun-power.com/news/{page_num}.html"
    s = requests.Session()
    s.headers["User-Agent"] = UA
    r = s.get(url, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    out: list[dict] = []
    seen: set[str] = set()
    for div in soup.select("div.title.clearfix"):
        a = div.find("a")
        if not a:
            continue
        href = (a.get("href") or "").strip()
        if not href:
            continue
        link = urljoin("https://www.xindun-power.com/", href)
        if link in seen:
            continue
        seen.add(link)
        title_en = clean_spaces(a.get("title") or a.get_text(" ", strip=True))
        out.append({"title_en": title_en, "url": link})
        if len(out) == 5:
            break
    if len(out) != 5:
        raise RuntimeError(f"Expected 5 articles on {url}, got {len(out)}")
    return out


def fetch_article(url: str) -> dict:
    s = requests.Session()
    s.headers["User-Agent"] = UA
    html = s.get(url, timeout=60).text
    soup = BeautifulSoup(html, "lxml")
    title = clean_spaces((soup.find("h1") or soup.find("title")).get_text(" ", strip=True))
    md = soup.find("meta", attrs={"name": "description"})
    desc = clean_spaces(md.get("content", "") if md else "")

    box = soup.select_one(".pageNewsDetailsBox") or soup.select_one("#pageNewsDetailsBox")
    if not box:
        for sel in [".news-detail", ".content", ".detail", ".article"]:
            box = soup.select_one(sel)
            if box:
                break
    if box:
        for el in box.find_all(string=re.compile(r"Related\s+posts", re.I)):
            p = el.parent
            for sib in list(p.next_siblings):
                if getattr(sib, "decompose", None):
                    sib.decompose()
            p.decompose()
            break
        for el in box.find_all(class_=re.compile(r"related", re.I)):
            el.decompose()

    imgs = []
    if box:
        for img in box.find_all("img"):
            src = (img.get("src") or img.get("data-src") or "").strip()
            src = urljoin("https://www.xindun-power.com/", src)
            imgs.append(
                {
                    "src": src,
                    "alt": clean_spaces(img.get("alt") or ""),
                    "title": clean_spaces(img.get("title") or img.get("alt") or ""),
                }
            )
    return {
        "url": url,
        "title": title,
        "description": desc,
        "images": imgs,
        "content_html": str(box) if box else "",
    }


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
                return
            except Exception as exc:  # noqa: BLE001
                last_err = str(exc)
                print(f"[wp] login retry {attempt + 1}/8: {last_err}", flush=True)
                time.sleep(5 * (attempt + 1))
        raise RuntimeError(f"WP login failed: {last_err}")

    def upload_media(self, path: Path, alt: str, title: str) -> dict:
        last_err = ""
        mime = "image/webp" if path.suffix.lower() == ".webp" else "image/jpeg"
        for attempt in range(6):
            data = path.read_bytes()
            r = self.s.post(
                f"{WP}/wp-json/wp/v2/media",
                headers={
                    "Content-Disposition": f'attachment; filename="{path.name}"',
                    "Content-Type": mime,
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

    def create_post(self, title: str, content: str, featured_media: int) -> dict:
        last_err = ""
        for attempt in range(6):
            r = self.s.post(
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
            json={"content": content, "featured_media": featured_media, "status": "publish"},
            timeout=120,
        )
        if r2.status_code >= 400:
            print(f"[yoast] warn REST re-post {r2.status_code}: {r2.text[:200]}", flush=True)
            return {}
        return r2.json()


def save_results(results: list[dict]) -> None:
    RESULTS_PATH.write_text(
        json.dumps({"page": PAGE_NUM, "results": results, "images": IMAGE_LOG}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def prepare_images(article_idx: int, imgs: list[dict]) -> list[dict]:
    prepared = []
    used_names: set[str] = set()
    for ii, im in enumerate(imgs):
        alt_en = im["alt"] or f"imagen-{article_idx}-{ii}"
        alt_es = translate_text(alt_en)
        title_es = translate_text(im.get("title") or alt_en)

        base = slugify(alt_es)
        stem = base
        n = 2
        while stem in used_names:
            stem = f"{base}-{n}"
            n += 1
        used_names.add(stem)

        ext = Path(im["src"]).suffix.lower() or ".jpg"
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
            ext = ".jpg"
        local = OUT / f"_src_a{article_idx}_i{ii}{ext}"
        if not local.exists() or local.stat().st_size == 0:
            rr = requests.get(im["src"], timeout=60, headers={"User-Agent": UA})
            rr.raise_for_status()
            local.write_bytes(rr.content)

        with Image.open(local) as pil:
            orig_wh = pil.size

        tagged_stem = f"a{article_idx}_i{ii}_{stem}"
        tagged = OUT / f"{tagged_stem}.webp"

        method = "duomi" if (article_idx, ii) in DUOMI_MAP else "compress"
        duomi_path = None
        if tagged.exists() and tagged.stat().st_size > 0:
            method += "-reuse"
            final = tagged
            if "duomi" in method:
                duomi_path = str(tagged)
        elif (article_idx, ii) in DUOMI_MAP:
            size = size_for(*orig_wh)
            result = run_duomi(
                im["src"],
                DUOMI_MAP[(article_idx, ii)],
                tagged_stem,
                size,
                orig_wh,
                local,
            )
            if result is None:
                raise RuntimeError(f"duomi failed for required overlay image a{article_idx}_i{ii}")
            final = result
            duomi_path = str(result)
        else:
            final = compress_only(local, tagged_stem, orig_wh)

        if final.stat().st_size > 100 * 1024:
            raise RuntimeError(f"image exceeds 100KB: {final}")

        entry = {
            "local": final,
            "alt_es": alt_es,
            "title_es": title_es,
            "src_orig": im["src"],
            "method": method,
            "duomi_path": duomi_path,
            "orig_wh": orig_wh,
        }
        IMAGE_LOG.append(
            {
                "article": article_idx,
                "img": ii,
                **{k: (str(v) if k == "local" else v) for k, v in entry.items()},
            }
        )
        prepared.append(entry)
        print(
            f"[img] a{article_idx}_i{ii} method={method} -> {final.name} {final.stat().st_size}b",
            flush=True,
        )

    return prepared


def replace_images_in_html(content_html_es: str, prepared: list[dict], media_list: list[dict]) -> str:
    soup = BeautifulSoup(content_html_es, "lxml")
    body = soup.body or soup
    imgs = body.find_all("img")
    for idx, img in enumerate(imgs):
        if idx >= len(media_list):
            break
        m = media_list[idx]
        img["src"] = m.get("source_url")
        img["alt"] = prepared[idx]["alt_es"]
        img["title"] = prepared[idx]["title_es"]
        for attr in ("width", "height", "srcset", "sizes"):
            if attr in img.attrs:
                del img.attrs[attr]
    if body.name == "body":
        return "".join(str(c) for c in body.children)
    return str(body)


def already_published(title_es: str, title_en: str) -> str | None:
    """Strict duplicate check to avoid false positives on generic words."""
    s = requests.Session()
    s.headers["User-Agent"] = UA
    stop = {
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
        "difference",
        "diferencia",
        "hybrid",
        "hibrido",
        "híbrido",
        "batteries",
        "baterias",
        "baterías",
    }

    def tokens(text: str) -> set[str]:
        return {
            t
            for t in re.split(r"[^a-z0-9áéíóúñü]+", text.lower())
            if len(t) > 3 and t not in stop
        }

    for q in {title_es, title_en}:
        if not q or len(q.strip()) < 8:
            continue
        try:
            r = s.get(
                f"{WP}/wp-json/wp/v2/posts",
                params={"search": q, "categories": CAT, "per_page": 10, "status": "publish"},
                timeout=30,
            )
            if not r.ok:
                continue
            q_tok = tokens(q)
            for p in r.json():
                rendered = re.sub(r"<[^>]+>", "", (p.get("title") or {}).get("rendered") or "")
                rt = rendered.lower().strip()
                ql = q.lower().strip()
                if rt == ql or rt.rstrip("?") == ql.rstrip("?"):
                    return p.get("link")
                shared = tokens(rt) & q_tok
                if len(q_tok) >= 2 and len(shared) >= max(2, len(q_tok) - 1):
                    if abs(len(rt) - len(ql)) <= 12:
                        return p.get("link")
        except Exception:  # noqa: BLE001
            continue
    return None


def main() -> None:
    wp = WPClient()
    wp.login()

    articles = fetch_page_articles(PAGE_NUM)
    print(f"[page] {PAGE_NUM} -> {len(articles)} articles from {NEWS_URL}", flush=True)

    results: list[dict] = []
    only = os.environ.get("ONLY_ARTICLE")
    only_idxs = {int(x) for x in only.split(",")} if only else None

    for article_idx, art in enumerate(articles):
        if only_idxs is not None and article_idx not in only_idxs:
            continue

        print("=" * 70, flush=True)
        print(f"ARTICLE {article_idx}: {art['title_en']}", flush=True)

        raw = fetch_article(art["url"])
        title_en = clean_spaces(art["title_en"] or raw["title"])
        title_es = translate_text(title_en)
        desc_es = translate_text(raw.get("description") or title_en)

        existing = already_published(title_es, title_en)
        if existing and os.environ.get("FORCE_PUBLISH") != "1":
            print(f"[skip] already published: {existing}", flush=True)
            results.append(
                {
                    "title_en": title_en,
                    "title_es": title_es,
                    "url": existing,
                    "status": "already_published",
                    "post_id": None,
                    "source_url": art["url"],
                }
            )
            save_results(results)
            continue

        prepared = prepare_images(article_idx, raw["images"])
        content_es = translate_html(raw["content_html"])
        if re.search(r"Error\s*500|Server Error", content_es, re.I):
            print("[translate] Error 500 in content; retrying full translate", flush=True)
            time.sleep(5)
            content_es = translate_html(raw["content_html"])
            if re.search(r"Error\s*500|Server Error", content_es, re.I):
                raise RuntimeError("Google Translate Error 500 persists in content")

        content_es = prepend_18pt_title(content_es, title_es)

        media_list: list[dict] = []
        for p in prepared:
            media = wp.upload_media(p["local"], p["alt_es"], p["title_es"])
            media_list.append(media)

        content_es = replace_images_in_html(content_es, prepared, media_list)
        featured = media_list[0]["id"] if media_list else 0
        featured_url = media_list[0].get("source_url", "") if media_list else ""

        post = wp.create_post(title_es, content_es, featured)
        print(f"[post] created id={post['id']} {post.get('link')}", flush=True)

        wp.set_yoast(post["id"], title_es, desc_es, content_es, featured, featured_url)

        results.append(
            {
                "title_en": title_en,
                "title_es": title_es,
                "url": post.get("link"),
                "status": "published",
                "post_id": post["id"],
                "source_url": art["url"],
            }
        )
        save_results(results)

    save_results(results)
    print("DONE", json.dumps(results, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
