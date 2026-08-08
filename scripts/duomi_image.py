#!/usr/bin/env python3
"""Cloud-safe Duomi gpt-image-2 helper for XindunPower/xindunsolar Automations.

Uses only the public HTTPS Duomi API (same as the local /image skill).
Does NOT depend on Cursor local skills or slash commands.

Auth (first match wins):
  1) --api-key
  2) env DUOMI_API_KEY  (set this in Cursor Cloud Agents secrets)
  3) repo-root .env     (local only; never commit real keys)
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://duomiapi.com"
TERMINAL_FAILURES = {"failed", "error", "cancelled", "canceled"}
REPO_ROOT = Path(__file__).resolve().parent.parent


def load_env_file(path: Path) -> None:
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value[:1] == value[-1:] and value[:1] in {"'", '"'}:
            value = value[1:-1]
        if key:
            os.environ.setdefault(key, value)


def request_json(url, api_key, data=None, method=None, timeout=60):
    headers = {"Authorization": api_key}
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API HTTP {exc.code}: {body}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"API request failed: {exc}") from exc


def download(url, destination: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "xindunsolar-duomi/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        destination.write_bytes(response.read())


def extension_for(image) -> str:
    name = image.get("file_name") or urllib.parse.urlparse(image["url"]).path
    suffix = Path(name).suffix
    if suffix and len(suffix) <= 6:
        return suffix
    content_type, _ = mimetypes.guess_type(image["url"])
    return mimetypes.guess_extension(content_type or "image/jpeg") or ".jpg"


def wait_for_task(task_id, api_key, interval, timeout):
    deadline = time.monotonic() + timeout
    url = f"{BASE_URL}/v1/tasks/{urllib.parse.quote(task_id, safe='')}"
    while True:
        result = request_json(url, api_key)
        state = str(result.get("state", "")).lower()
        progress = result.get("progress")
        print(f"Task {task_id}: state={state or 'unknown'}, progress={progress}", file=sys.stderr)
        if state == "succeeded":
            return result
        if state in TERMINAL_FAILURES:
            raise RuntimeError(
                f"Task {task_id} ended with state={state}: {json.dumps(result, ensure_ascii=False)}"
            )
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Task {task_id} did not finish within {timeout} seconds")
        time.sleep(interval)


def compress_under_kb(path: Path, max_kb: int) -> Path:
    """Re-encode to JPEG under max_kb when possible. Requires Pillow."""
    if max_kb <= 0 or path.stat().st_size <= max_kb * 1024:
        return path
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "Image exceeds --max-kb but Pillow is not installed. "
            "Run: pip install -r requirements.txt"
        ) from exc

    out = path.with_suffix(".jpg")
    img = Image.open(path).convert("RGB")
    quality = 88
    while quality >= 20:
        img.save(out, format="JPEG", quality=quality, optimize=True)
        if out.stat().st_size <= max_kb * 1024:
            if out.resolve() != path.resolve() and path.suffix.lower() != ".jpg":
                path.unlink(missing_ok=True)
            return out
        quality -= 8
    # Last resort: slight downscale then re-encode (keeps composition)
    w, h = img.size
    for scale in (0.92, 0.85, 0.78, 0.7):
        resized = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
        resized.save(out, format="JPEG", quality=40, optimize=True)
        if out.stat().st_size <= max_kb * 1024:
            if out.resolve() != path.resolve() and path.suffix.lower() != ".jpg":
                path.unlink(missing_ok=True)
            return out
    raise RuntimeError(f"Could not compress {path.name} under {max_kb}KB")


def main() -> None:
    load_env_file(REPO_ROOT / ".env")
    parser = argparse.ArgumentParser(
        description="Generate/edit images via Duomi gpt-image-2 (cloud Automation compatible)"
    )
    parser.add_argument("--api-key", help="Duomi API key")
    parser.add_argument("--prompt", "-p", required=True)
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="3:2", help="Prefer 3:2 to match existing Xindun Spanish assets")
    parser.add_argument(
        "--image-url",
        action="append",
        default=[],
        help="Public HTTPS source/reference image URL; repeatable",
    )
    parser.add_argument("--oversea", action="store_true")
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--poll-interval", type=float, default=5.0)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument(
        "--output-dir",
        default="output/duomi",
        help="Relative to repo root unless absolute",
    )
    parser.add_argument("--output-name", help="Filename stem, e.g. spanish-alt-slug")
    parser.add_argument("--max-kb", type=int, default=100, help="Compress result under this size; 0 disables")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Print a machine-readable JSON summary on stdout",
    )
    args = parser.parse_args()

    if args.n < 1:
        parser.error("--n must be at least 1")
    for url in args.image_url:
        if urllib.parse.urlparse(url).scheme not in {"http", "https"}:
            parser.error("--image-url must be a public HTTP(S) URL; local files are not supported")

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "oversea": bool(args.oversea),
    }
    if args.image_url:
        payload["image"] = args.image_url

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    api_key = args.api_key or os.environ.get("DUOMI_API_KEY")
    if not api_key:
        parser.error("Set DUOMI_API_KEY in Cloud Agents secrets, or pass --api-key")

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = REPO_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    prefix = args.output_name or f"duomi_{stamp}"
    saved = []

    for task_number in range(1, args.n + 1):
        created = request_json(f"{BASE_URL}/v1/images/generations", api_key, payload, method="POST")
        task_id = created.get("id")
        if not task_id:
            raise RuntimeError(f"Create response has no id: {json.dumps(created, ensure_ascii=False)}")
        result = wait_for_task(str(task_id), api_key, args.poll_interval, args.timeout)
        images = result.get("data", {}).get("images", [])
        if not images:
            raise RuntimeError(f"Task {task_id} succeeded without images")
        for image_number, image in enumerate(images, 1):
            url = image.get("url")
            if not url:
                continue
            suffix = extension_for(image)
            serial = f"_{task_number}" if args.n > 1 else ""
            if len(images) > 1:
                serial += f"_{image_number}"
            destination = output_dir / f"{prefix}{serial}{suffix}"
            download(url, destination)
            destination = compress_under_kb(destination, args.max_kb)
            saved.append(destination)
            print(f"SUCCESS:{destination}")

    if not saved:
        raise RuntimeError("No downloadable images returned")

    if args.print_json:
        print(
            json.dumps(
                {
                    "ok": True,
                    "files": [str(p) for p in saved],
                    "bytes": [p.stat().st_size for p in saved],
                    "payload": {
                        "model": payload["model"],
                        "size": payload["size"],
                        "has_reference": bool(args.image_url),
                    },
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, TimeoutError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
