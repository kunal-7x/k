#!/usr/bin/env python3
"""
ingest_saved.py — extract Instagram post/reel URLs from an Instagram
"Download Your Information" export.

This is the SAFE way to hand Claude your saved posts: no password, no login,
no ToS violation. In the Instagram app:
  Settings -> Accounts Center -> Your information and permissions ->
  Download your information -> request "Saved posts" (JSON or HTML).
Instagram emails you a file; point this script at it.

It handles both the JSON export (e.g. saved_posts.json, with the
`saved_saved_media` structure) and the HTML export, and as a last resort
regex-scrapes any Instagram post/reel/tv URLs from the file. Works on a single
file or a directory (walks it).

Usage:
  python3 ingest_saved.py <file-or-dir> [--out urls.txt]

Prints one URL per line (also to --out if given) plus a count on stderr.
Feed the result to grab.py in batches to read + understand each post:
  python3 grab.py $(cat urls.txt) --out ./work
"""
import argparse
import json
import re
import sys
from pathlib import Path

URL_RE = re.compile(
    r"https?://(?:www\.)?instagram\.com/(?:p|reel|reels|tv)/[A-Za-z0-9_-]+/?",
    re.IGNORECASE,
)


def log(*a):
    print("[visual-content:ingest]", *a, file=sys.stderr, flush=True)


def norm(u: str) -> str:
    u = u.split("?")[0].rstrip("/")
    return u + "/"


def walk_json(obj, out):
    """Recursively collect any Instagram URLs found in JSON values."""
    if isinstance(obj, dict):
        for v in obj.values():
            walk_json(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk_json(v, out)
    elif isinstance(obj, str):
        for m in URL_RE.findall(obj):
            out.append(m)


def extract_from_text(text, out):
    for m in URL_RE.findall(text):
        out.append(m)


def process_file(path: Path, out):
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        log(f"skip {path}: {e}")
        return
    # Try structured JSON first (most reliable for the official export).
    if path.suffix.lower() == ".json" or raw.lstrip()[:1] in "{[":
        try:
            walk_json(json.loads(raw), out)
            return
        except Exception:
            pass  # fall through to regex
    # HTML / text / malformed JSON: regex scrape.
    extract_from_text(raw, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="export file or directory")
    ap.add_argument("--out", default=None, help="also write URLs here")
    args = ap.parse_args()

    root = Path(args.path)
    found = []
    if root.is_dir():
        for p in sorted(root.rglob("*")):
            if p.is_file() and p.suffix.lower() in {".json", ".html", ".htm", ".txt"}:
                process_file(p, found)
    elif root.is_file():
        process_file(root, found)
    else:
        log(f"not found: {root}")
        sys.exit(1)

    # Dedupe, preserve order.
    seen, urls = set(), []
    for u in found:
        n = norm(u)
        if n not in seen:
            seen.add(n)
            urls.append(n)

    for u in urls:
        print(u)
    if args.out:
        Path(args.out).write_text("\n".join(urls) + ("\n" if urls else ""),
                                  encoding="utf-8")
    log(f"extracted {len(urls)} unique Instagram URLs"
        + (f" -> {args.out}" if args.out else ""))


if __name__ == "__main__":
    main()
