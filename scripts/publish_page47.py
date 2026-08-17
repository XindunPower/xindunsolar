#!/usr/bin/env python3
"""Publish xindun-power news page 47 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import unicodedata
from io import BytesIO
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "output" / "duomi"
OUT.mkdir(parents=True, exist_ok=True)
WP = "https://www.xindunsolar.com"
CAT = 89
UA = "Mozilla/5.0 (compatible; XindunSpanishBot/1.0)"
RESULTS_PATH = Path("/tmp/page47_results.json")

PROMPT_BASE = (
    "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. "
    "Only translate English marketing/diagram overlay text to Spanish. "
    "Do NOT change product casing text, logos, model numbers, certificates, "
    "Chinese exhibition signs, or wall company names "
    "(Xindun / Xindun GREEN POWER / XINDUN POWER)."
)

# Duomi only where English marketing/diagram overlays exist.
# Compress-only: factory photo (0,0); product showcase casing+URL (0,1);
# product lineup casing-only (4,0).
DUOMI_MAP = {
    (1, 0): (
        "Translate diagram overlay labels only to Spanish: "
        "'AC output switch'→'Interruptor de salida CA'; "
        "'AC input switch'→'Interruptor de entrada CA'; "
        "'Battery switch'→'Interruptor de batería'; "
        "'Battery'→'Batería'; "
        "'Grid or generator'→'Red o generador'; "
        "'Three phase loads'→'Cargas trifásicas'. "
        "Keep white background, open black cabinet, wiring colors, "
        "A/B/C/N phase letters, motor photos, ON/OFF casing labels, "
        "and xindun GREEN POWER logo unchanged. Do not redesign."
    ),
    (2, 0): (
        "Translate red diagram overlay text only to Spanish: "
        "'10KVA power inverter'→'Inversor de potencia 10KVA'; "
        "'10KVA pure resistive loads'→'Cargas resistivas puras 10KVA'; "
        "'>25kva solar power inverter'→'>25kva inversor de energía solar'; "
        "'10KVA inductive load'→'Carga inductiva 10KVA'. "
        "Keep white background, both black tower inverters, blue arrows, "
        "and all appliance icons unchanged. Do not redesign."
    ),
    (2, 1): (
        "Translate diagram overlay labels only to Spanish: "
        "'Power Grid'→'Red eléctrica'; "
        "'or'→'o'; "
        "'Generator'→'Generador'; "
        "'Solar Panels'→'Paneles solares'; "
        "'Three Phase Hybrid Solar Inverter'→'Inversor solar híbrido trifásico'; "
        "'Batteries'→'Baterías'; "
        "'Single Phase Loads'→'Cargas monofásicas'; "
        "'Household Device'→'Dispositivos domésticos'; "
        "'Office Equipment'→'Equipos de oficina'; "
        "'Industrial Equipment'→'Equipos industriales'; "
        "'Three-phase loads'→'Cargas trifásicas'. "
        "Keep white background, red dashed arrows, product photos, "
        "and Xindun GREEN POWER on battery unchanged. Do not redesign."
    ),
    (3, 0): (
        "Translate the three red numbered guideline lines only to Spanish: "
        "'1.The total power of the solar panels in the system should not exceed 80% of the inverter power.'→"
        "'1.La potencia total de los paneles solares del sistema no debe exceder el 80% de la potencia del inversor.'; "
        "'2.The total power of the load connected to the inverter does not exceed 80% of power of the inverter.'→"
        "'2.La potencia total de la carga conectada al inversor no excede el 80% de la potencia del inversor.'; "
        "'3.The inverter needs to be selected according to the type of load,'→"
        "'3.El inversor debe seleccionarse según el tipo de carga,'. "
        "Keep blue sky, solar panels, black inverter, silver refrigerator, "
        "power cable, and xindun logo unchanged. Do not redesign."
    ),
}

ARTICLES = [
    {
        "url": "https://www.xindun-power.com/faq/find-a-famous-inverter-company-to-buy-power-inverter.html",
        "title_en": "Find a famous inverter company to buy power inverter",
    },
    {
        "url": "https://www.xindun-power.com/faq/Which-solar-inverter-can-power-3-phase.html",
        "title_en": "Which solar inverter can power 3 phase？",
    },
    {
        "url": "https://www.xindun-power.com/faq/what-can-10Kva-inverter-power.html",
        "title_en": "What can 10Kva inverter power?",
    },
    {
        "url": "https://www.xindun-power.com/faq/suitable-inverter-for-150KW-solar-power-system.html",
        "title_en": "Suitable Inverter for 150KW Solar Power System",
    },
    {
        "url": "https://www.xindun-power.com/faq/how-much-is-the-Inverte-wholesale-in-south-Africa.html",
        "title_en": "How much is the Inverte wholesale in south Africa",
    },
]

IMAGE_LOG: list[dict] = []


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:90] or "imagen"


def translate_text(text: str, retries: int = 5) -> str:
    text = (text or "").strip()
    if not text:
        return text
    if not re.search(r"[A-Za-zÀ-ÿ]", text):
        return text
    for attempt in range(retries):
        try:
            out = GoogleTranslator(source="en", target="es").translate(text)
            if out and not re.search(r"Error\s*500|Server Error", out, re.I):
                return out
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


def to_webp(src: Path | bytes, dest: Path, tw: int, th: int, max_kb: int = 100) -> None:
    if isinstance(src, bytes):
        img = Image.open(BytesIO(src)).convert("RGB")
    else:
        img = Image.open(src).convert("RGB")
    sw, sh = img.size
    ta, sa = tw / th, sw / sh
    if abs(sa - ta) > 0.08:
        print(f"[img] aspect adjust {sw}x{sh} -> {tw}x{th}", flush=True)
        if sa > ta:
            nw = int(sh * ta)
            left = (sw - nw) // 2
            img = img.crop((left, 0, left + nw, sh))
        else:
            nh = int(sw / ta)
            top = (sh - nh) // 2
            img = img.crop((0, top, sw, top + nh))
    img = img.resize((tw, th), Image.Resampling.LANCZOS)
    q = 82
    while q >= 20:
        buf = BytesIO()
        img.save(buf, format="WEBP", quality=q, method=6)
        if len(buf.getvalue()) <= max_kb * 1024:
            dest.write_bytes(buf.getvalue())
            return
        q -= 8
    buf = BytesIO()
    img.save(buf, format="WEBP", quality=15, method=6)
    dest.write_bytes(buf.getvalue())


def compress_only(local: Path, name: str, orig_wh: tuple[int, int]) -> Path:
    dest = OUT / f"{name}.webp"
    to_webp(local, dest, orig_wh[0], orig_wh[1], 100)
    return dest


def run_duomi(
    image_url: str,
    extra_prompt: str,
    name: str,
    size: str,
    orig_wh: tuple[int, int],
    attempts: int = 3,
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
        try:
            with Image.open(raw) as chk:
                cw, ch = chk.size
            # Reject extreme redesign aspect; still force to original WxH afterward.
            if abs((cw / ch) - (orig_wh[0] / orig_wh[1])) > 0.35:
                print(f"[duomi] reject bad aspect {cw}x{ch} vs {orig_wh}", flush=True)
                time.sleep(3)
                continue
            to_webp(raw, final, orig_wh[0], orig_wh[1], 100)
        except Exception as exc:  # noqa: BLE001
            print(f"[duomi] layout/compress failed: {exc}", flush=True)
            time.sleep(3)
            continue
        if final.exists() and final.stat().st_size > 0:
            return final
    return None


def fetch_article(url: str) -> dict:
    s = requests.Session()
    s.headers["User-Agent"] = UA
    html = s.get(url, timeout=60).text
    soup = BeautifulSoup(html, "lxml")
    title = (soup.find("h1") or soup.find("title")).get_text(strip=True)
    md = soup.find("meta", attrs={"name": "description"})
    desc = md.get("content", "") if md else ""
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
            src = img.get("src") or img.get("data-src") or ""
            if src.startswith("//"):
                src = "https:" + src
            elif src.startswith("/"):
                src = "https://www.xindun-power.com" + src
            imgs.append(
                {
                    "src": src,
                    "alt": img.get("alt") or "",
                    "title": img.get("title") or img.get("alt") or "",
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
        mime = "image/webp" if path.suffix.lower() == ".webp" else "image/jpeg"
        last_err = ""
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
            print(f"[wp] warn alt update {r2.status_code}", flush=True)
        media = r2.json() if r2.ok else media
        src = media.get("source_url") or ""
        try:
            chk = requests.head(src, timeout=30, allow_redirects=True, headers={"User-Agent": UA})
            if chk.status_code == 404:
                print(f"[wp] WARN media 404 at {src}", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[wp] warn head {exc}", flush=True)
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
            m2 = re.search(
                r'name="([^"]*yoast[^"]*nonce[^"]*)"\s+value="([^"]+)"', edit.text, re.I
            )
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
            json={
                "content": content,
                "featured_media": featured_media,
                "status": "publish",
            },
            timeout=120,
        )
        if r2.status_code >= 400:
            print(f"[yoast] warn REST re-post {r2.status_code}: {r2.text[:200]}", flush=True)
            return {}
        return r2.json()


def save_results(results: list[dict]) -> None:
    RESULTS_PATH.write_text(
        json.dumps({"results": results, "images": IMAGE_LOG}, ensure_ascii=False, indent=2),
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
        name = base
        n = 2
        while name in used_names:
            name = f"{base}-{n}"
            n += 1
        used_names.add(name)

        local = OUT / f"_src_a{article_idx}_i{ii}{Path(im['src']).suffix or '.jpg'}"
        if not local.exists() or local.stat().st_size == 0:
            rr = requests.get(im["src"], timeout=60, headers={"User-Agent": UA})
            rr.raise_for_status()
            local.write_bytes(rr.content)
        with Image.open(local) as pil:
            orig_wh = pil.size

        method = "duomi" if (article_idx, ii) in DUOMI_MAP else "compress"
        duomi_path = None
        final = OUT / f"{name}.webp"
        # Prefer unique tag reuse for resume.
        tagged = OUT / f"a{article_idx}_i{ii}_{name}.webp"
        if tagged.exists() and tagged.stat().st_size > 0:
            final = tagged
            method = f"{method}-reuse"
            if "duomi" in method:
                duomi_path = str(final)
        elif final.exists() and final.stat().st_size > 0:
            method = f"{method}-reuse"
            if "duomi" in method:
                duomi_path = str(final)
        elif method == "duomi":
            size = size_for(*orig_wh)
            result = run_duomi(im["src"], DUOMI_MAP[(article_idx, ii)], name, size, orig_wh)
            if result is None:
                print(f"[img] duomi failed; fallback compress-only for {name}", flush=True)
                method = "compress-fallback"
                final = compress_only(local, name, orig_wh)
            else:
                # Copy to tagged path for resume clarity.
                tagged.write_bytes(result.read_bytes())
                final = tagged
                duomi_path = str(result)
        else:
            final = compress_only(local, name, orig_wh)
            tagged.write_bytes(final.read_bytes())
            final = tagged

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


def replace_images_in_html(
    content_html_es: str, prepared: list[dict], media_list: list[dict]
) -> str:
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
    """Strict duplicate check — avoid false positives on shared stopwords."""
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
    }

    def tokens(text: str) -> set[str]:
        return {
            t
            for t in re.split(r"[^a-z0-9áéíóúñü]+", text.lower())
            if len(t) > 3 and t not in stop
        }

    queries = {title_es, title_en}
    for q in queries:
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
                # Exact / near-exact title only.
                if rt == ql or rt.rstrip("?") == ql.rstrip("?"):
                    return p.get("link")
                # High-signal content tokens must largely match (no generic words).
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
    results: list[dict] = []
    only = os.environ.get("ONLY_ARTICLE")
    only_idxs = {int(x) for x in only.split(",")} if only else None

    for article_idx, art in enumerate(ARTICLES):
        if only_idxs is not None and article_idx not in only_idxs:
            continue
        print("=" * 70, flush=True)
        print(f"ARTICLE {article_idx}: {art['title_en']}", flush=True)
        raw = fetch_article(art["url"])
        title_es = translate_text(art["title_en"])
        desc_es = translate_text(raw.get("description") or art["title_en"])

        existing = already_published(title_es, art["title_en"])
        if existing and os.environ.get("FORCE_PUBLISH") != "1":
            print(f"[skip] already published: {existing}", flush=True)
            results.append(
                {
                    "title_en": art["title_en"],
                    "title_es": title_es,
                    "url": existing,
                    "status": "already_published",
                    "post_id": None,
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
                "title_en": art["title_en"],
                "title_es": title_es,
                "url": post.get("link"),
                "status": "published",
                "post_id": post["id"],
            }
        )
        save_results(results)

    save_results(results)
    print("DONE", json.dumps(results, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
