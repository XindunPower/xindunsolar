#!/usr/bin/env python3
"""Publish xindun-power news page 86 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import re
import time
from pathlib import Path

from argostranslate import translate as argos_translate
from deep_translator import GoogleTranslator, MyMemoryTranslator

import publish_page55 as base

base.PAGE_NUM = 86
base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
base.RESULTS_PATH = Path(f"/tmp/page{base.PAGE_NUM}_results.json")

# Product/installation photos without English marketing/diagram overlays — compress only.
base.DUOMI_MAP = {}

TITLE_OVERRIDES = {
    "How about the inverters of Xindun Power?": "¿Qué tal los inversores de Xindun Power?",
    "What are the differences between single phase inverter and three phase inverter?": (
        "¿Cuáles son las diferencias entre un inversor monofásico y un inversor trifásico?"
    ),
    "What is an off-grid inverter?": "¿Qué es un inversor off-grid?",
    "The difference between off-grid power system and on-grid power system": (
        "La diferencia entre un sistema off-grid y un sistema on-grid"
    ),
    "Which inverter manufacturer is better for custom processing?": (
        "¿Qué fabricante de inversores es mejor para el procesamiento personalizado?"
    ),
}

ALT_OVERRIDES = {
    "xindun power inverter": "inversor Xindun Power",
    "single phase inverter": "inversor monofásico",
    "three phase inverter": "inversor trifásico",
    "off grid inverter": "inversor off-grid",
    "on-off-grid-photovoltaic-power-system": "sistema fotovoltaico on-grid y off-grid",
    "Custom-inverter-manufacturers": "fabricantes de inversores personalizados",
}

_MYMEMORY: MyMemoryTranslator | None = None
_ARGOS_TR = None


def _mymemory() -> MyMemoryTranslator:
    global _MYMEMORY
    if _MYMEMORY is None:
        _MYMEMORY = MyMemoryTranslator(source="en-GB", target="es-ES")
    return _MYMEMORY


def _argos_en_es():
    global _ARGOS_TR
    if _ARGOS_TR is not None:
        return _ARGOS_TR
    langs = argos_translate.get_installed_languages()
    lang_en = next((x for x in langs if x.code == "en"), None)
    lang_es = next((x for x in langs if x.code == "es"), None)
    if not lang_en or not lang_es:
        raise RuntimeError("Argos en->es model is not installed")
    _ARGOS_TR = lang_en.get_translation(lang_es)
    return _ARGOS_TR


def _mymemory_chunked(text: str, chunk_size: int = 450) -> str:
    if len(text) <= chunk_size:
        return _mymemory().translate(text)
    parts: list[str] = []
    buf = ""
    for piece in re.split(r"(\s+)", text):
        if len(buf) + len(piece) > chunk_size and buf.strip():
            parts.append(_mymemory().translate(buf))
            buf = piece
        else:
            buf += piece
    if buf.strip():
        parts.append(_mymemory().translate(buf))
    return "".join(parts)


def already_published_strict(title_es: str, title_en: str) -> str | None:
    """Stricter duplicate check: require slug or exact title, or nearly full token overlap."""
    import requests

    s = requests.Session()
    s.headers["User-Agent"] = base.UA

    def title_match(query: str, rendered: str) -> bool:
        ql = base.normalize_title(query)
        rt = base.normalize_title(rendered)
        if not ql or not rt:
            return False
        if rt == ql or rt.rstrip("?") == ql.rstrip("?"):
            return True
        stop = {
            "cual", "cuál", "para", "como", "cómo", "que", "qué", "esta", "este",
            "from", "with", "what", "when", "where", "mejor", "best", "solar",
            "paneles", "panels", "sistema", "system", "energia", "energía", "power",
            "the", "and", "for", "inversor", "inverter", "inversores", "phase", "fase",
        }

        def tokens(text: str) -> set[str]:
            return {
                t
                for t in re.split(r"[^a-z0-9áéíóúñü]+", text.lower())
                if len(t) > 3 and t not in stop
            }

        q_tok = tokens(query)
        if len(q_tok) < 2:
            return False
        shared = tokens(rendered) & q_tok
        return len(shared) >= len(q_tok)

    if title_es:
        try:
            r = s.get(
                f"{base.WP}/wp-json/wp/v2/posts",
                params={
                    "slug": base.slugify(title_es),
                    "categories": base.CAT,
                    "per_page": 5,
                    "status": "publish",
                },
                timeout=30,
            )
            if r.ok and r.json():
                return r.json()[0].get("link")
        except Exception:  # noqa: BLE001
            pass

    for q in (title_es, title_en):
        if not q or len(q.strip()) < 8:
            continue
        try:
            r = s.get(
                f"{base.WP}/wp-json/wp/v2/posts",
                params={"search": q, "categories": base.CAT, "per_page": 10, "status": "publish"},
                timeout=30,
            )
            if not r.ok:
                continue
            for post in r.json():
                rendered = (post.get("title") or {}).get("rendered") or ""
                if title_match(q, rendered):
                    return post.get("link")
        except Exception:  # noqa: BLE001
            continue
    return None


def translate_text_resilient(text: str, retries: int = 1) -> str:
    text = base.clean_spaces(text.replace("\\'", "'"))
    if not text:
        return text
    if text in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[text]
    if text in ALT_OVERRIDES:
        return ALT_OVERRIDES[text]
    if not re.search(r"[A-Za-zÀ-ÿ]", text):
        return text

    normalized = text
    if "-" in text and " " not in text and re.search(r"[A-Za-z]-[A-Za-z]", text):
        normalized = text.replace("-", " ")

    try:
        out = base.clean_spaces(_argos_en_es().translate(normalized))
        if out and not re.search(r"Error\s*500|Server Error", out, re.I):
            return out
    except Exception as exc:  # noqa: BLE001
        print(f"[translate-argos] failed: {exc}", flush=True)

    for attempt in range(retries):
        try:
            out = GoogleTranslator(source="en", target="es").translate(normalized)
            out = base.clean_spaces(out)
            if out and not re.search(r"Error\s*500|Server Error", out, re.I):
                return out
        except Exception as exc:  # noqa: BLE001
            print(f"[translate-google] retry {attempt + 1}: {exc}", flush=True)
        time.sleep(1.6 * (attempt + 1))

    try:
        out = base.clean_spaces(_mymemory_chunked(normalized))
        if out and not re.search(r"Error\s*500|Server Error", out, re.I):
            return out
    except Exception as exc:  # noqa: BLE001
        print(f"[translate-mymemory] failed: {exc}", flush=True)

    print(f"[translate] fallback keep original: {text[:80]!r}", flush=True)
    return text


def translate_html_resilient(html: str) -> str:
    from bs4 import BeautifulSoup, NavigableString

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
        node.replace_with(translate_text_resilient(raw))
        time.sleep(0.15)

    for a in body.find_all("a"):
        a.unwrap()

    if body.name == "body":
        return "".join(str(c) for c in body.children)
    return str(body)


def prepare_images_with_idx(article_idx: int, images: list[dict]) -> list[dict]:
    prepared: list[dict] = []
    for img_idx, im in enumerate(images):
        alt_en = im["alt"] or f"imagen-{article_idx}-{img_idx}"
        alt_es = translate_text_resilient(alt_en)
        title_es = translate_text_resilient(im.get("title") or alt_en)
        stem = base.unique_stem(base.slugify(alt_es))

        ext = Path(im["src"]).suffix.lower() or ".jpg"
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
            ext = ".jpg"
        local = base.OUT / f"_src_a{article_idx}_i{img_idx}{ext}"
        if not local.exists() or local.stat().st_size == 0:
            rr = __import__("requests").get(im["src"], timeout=60, headers={"User-Agent": base.UA})
            rr.raise_for_status()
            local.write_bytes(rr.content)

        from PIL import Image

        with Image.open(local) as pil:
            orig_wh = pil.size

        tagged = base.OUT / f"{stem}.jpg"
        method = "compress"
        duomi_path = None
        if tagged.exists() and tagged.stat().st_size > 0:
            method += "-reuse"
            final = tagged
        else:
            final = base.compress_only(local, stem, orig_wh)

        if final.stat().st_size > 100 * 1024:
            raise RuntimeError(f"image exceeds 100KB: {final}")
        with Image.open(final) as chk:
            if chk.size != orig_wh:
                raise RuntimeError(f"image dimensions changed for {final}: {chk.size} vs {orig_wh}")

        entry = {
            "local": final,
            "alt_es": alt_es,
            "title_es": title_es,
            "src_orig": im["src"],
            "method": method,
            "duomi_path": duomi_path,
            "orig_wh": orig_wh,
        }
        base.IMAGE_LOG.append(
            {
                "article": article_idx,
                "img": img_idx,
                **{k: (str(v) if k == "local" else v) for k, v in entry.items()},
            }
        )
        prepared.append(entry)
        print(
            f"[img] a{article_idx}_i{img_idx} method={method} -> {final.name} {final.stat().st_size}b",
            flush=True,
        )
    return prepared


def main_with_update() -> None:
    import os

    if base.page_already_completed(base.PAGE_NUM) and os.environ.get("FORCE_PUBLISH") != "1":
        print(
            f"[skip] page {base.PAGE_NUM} already completed per progress.json "
            f"(set FORCE_PUBLISH=1 to override)",
            flush=True,
        )
        return

    wp = base.WPClient()
    wp.login()

    articles = base.fetch_page_articles(base.PAGE_NUM)
    print(f"[page] {base.PAGE_NUM} -> {len(articles)} articles from {base.NEWS_URL}", flush=True)

    results: list[dict] = []
    only = os.environ.get("ONLY_ARTICLE")
    only_idxs = {int(x) for x in only.split(",")} if only else None

    for article_idx, art in enumerate(articles):
        if only_idxs is not None and article_idx not in only_idxs:
            continue

        print("=" * 70, flush=True)
        print(f"ARTICLE {article_idx}: {art['title_en']}", flush=True)

        raw = base.fetch_article(art["url"])
        title_en = base.clean_spaces(raw["title_en"] or art["title_en"])
        seo_title_en = base.clean_spaces(raw["seo_title_en"] or title_en)
        desc_en = base.clean_spaces(raw["description_en"] or title_en)

        title_es = translate_text_resilient(title_en)
        seo_title_es = translate_text_resilient(seo_title_en)
        desc_es = translate_text_resilient(desc_en)

        existing = already_published_strict(title_es, title_en)
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
            base.save_results(results)
            continue

        prepared = prepare_images_with_idx(article_idx, raw["images"])
        content_es = translate_html_resilient(raw["content_html"])
        if re.search(r"Error\s*500|Server Error", content_es, re.I):
            print("[translate] Error 500 in content; retrying full translate", flush=True)
            time.sleep(5)
            content_es = translate_html_resilient(raw["content_html"])
            if re.search(r"Error\s*500|Server Error", content_es, re.I):
                raise RuntimeError("Translate Error 500 persists in content")

        content_es = base.prepend_18pt_title(content_es, title_es)

        media_list: list[dict] = []
        for p in prepared:
            media = wp.upload_media(p["local"], p["alt_es"], p["title_es"])
            media_list.append(media)

        content_es = base.replace_images_in_html(content_es, prepared, media_list)
        featured = media_list[0]["id"] if media_list else 0
        featured_url = media_list[0].get("source_url", "") if media_list else ""

        post = wp.create_post(title_es, desc_es, content_es, featured)
        print(f"[post] created id={post['id']} {post.get('link')}", flush=True)

        wp.set_yoast(post["id"], seo_title_es, desc_es, content_es, featured, featured_url)

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
        base.save_results(results)

    base.save_results(results)
    print("DONE", __import__("json").dumps(results, ensure_ascii=False, indent=2), flush=True)
    print("IMAGE_LOG", __import__("json").dumps(base.IMAGE_LOG, ensure_ascii=False, indent=2), flush=True)


base.translate_text = translate_text_resilient
base.translate_html = translate_html_resilient
base.prepare_images = prepare_images_with_idx
base.already_published = already_published_strict
base.IMAGE_LOG.clear()
base.USED_FILE_STEMS.clear()

if __name__ == "__main__":
    main_with_update()
