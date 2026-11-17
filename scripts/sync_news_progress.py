#!/usr/bin/env python3
"""Refresh local news progress from origin/main.

Cloud agents boot from a snapshot, so progress_ru.json in the working tree can
be behind main. Compare the page field and, when main is ahead, replace the
local file. Never downgrade a newer local file.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROGRESS_FILES = ("progress_ru.json", "progress.json", "progress_fr.json")
_fetched = False


def _run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )


def fetch_main() -> None:
    global _fetched
    if _fetched:
        return
    last_err = ""
    for attempt in range(4):
        result = _run_git(["fetch", "origin", "main"])
        if result.returncode == 0:
            _fetched = True
            return
        last_err = (result.stderr or result.stdout or "").strip()
        if attempt < 3:
            import time

            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"git fetch origin main failed: {last_err[:400]}")


def _page(data: dict) -> int | None:
    try:
        return int(data["page"])
    except (KeyError, TypeError, ValueError):
        return None


def remote_progress(name: str) -> dict | None:
    fetch_main()
    result = _run_git(["show", f"origin/main:{name}"])
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def sync_file(name: str) -> bool:
    """Update one progress file when origin/main is on a later page.

    Returns True when the local file was behind and has been replaced.
    """
    remote = remote_progress(name)
    if remote is None:
        return False
    remote_page = _page(remote)
    if remote_page is None:
        return False
    path = REPO / name
    local_page = None
    if path.is_file():
        try:
            local_page = _page(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            local_page = None
    if local_page is not None and local_page >= remote_page:
        print(f"[progress] {name} local page {local_page} matches origin/main", flush=True)
        return False
    path.write_text(json.dumps(remote, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[progress] {name} was page {local_page}; origin/main is page {remote_page}. "
        "Local file updated. Stop this page and read the file again.",
        flush=True,
    )
    return True


def ensure_current(names: tuple[str, ...] = PROGRESS_FILES) -> list[str]:
    updated = [name for name in names if sync_file(name)]
    return updated


def main() -> None:
    names = tuple(sys.argv[1:]) or PROGRESS_FILES
    updated = ensure_current(names)
    if updated:
        print("STALE " + " ".join(updated), flush=True)
        sys.exit(3)
    print("FRESH", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"[progress] sync failed: {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
