#!/usr/bin/env python3
"""
saved_live.py — pull a user's Instagram *saved* posts live, using their session
cookies (NOT their password), via gallery-dl's InstagramSavedExtractor.

RISK: this uses Instagram's unofficial/private API. It can get an account
flagged or banned and violates Instagram's ToS. Only run it when the user has
explicitly accepted that risk. The safe alternative is the data-export flow
(see references/saved-posts.md).

Auth: pass a Netscape cookies.txt exported from a browser where the user is
logged in to Instagram (extension "Get cookies.txt LOCALLY", or
`gallery-dl --cookies-from-browser <browser> --cookies-export cookies.txt`).
Never accept or store the user's password. Keep cookies.txt in a scratch/temp
dir — it is a live credential and must never be committed (it is gitignored).

What it does: asks gallery-dl for the saved feed's metadata, extracts each
post's permalink, dedupes, and writes a URL list. Feed that list to grab.py to
actually download + read each post (frames, captions), same as every other path.

Usage:
  python3 saved_live.py --cookies cookies.txt --user <your_username> \
      [--limit N] [--url <explicit saved/collection url>] [--out saved_urls.txt]

  # then:
  python3 grab.py $(head -n 15 saved_urls.txt) --out ./work
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SHORTCODE_KEYS = {"shortcode", "post_shortcode", "code"}
PERMALINK_RE = re.compile(
    r"https?://(?:www\.)?instagram\.com/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)",
    re.IGNORECASE,
)
SHORTCODE_RE = re.compile(r"^[A-Za-z0-9_-]{5,20}$")


def log(*a):
    print("[visual-content:saved_live]", *a, file=sys.stderr, flush=True)


def walk(obj, shortcodes):
    """Collect shortcodes from gallery-dl JSON: explicit shortcode keys and any
    Instagram permalinks embedded in string values."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in SHORTCODE_KEYS and isinstance(v, str) and SHORTCODE_RE.match(v):
                shortcodes.append(v)
            else:
                walk(v, shortcodes)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, shortcodes)
    elif isinstance(obj, str):
        for m in PERMALINK_RE.findall(obj):
            shortcodes.append(m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookies", required=True, help="Netscape cookies.txt (NOT a password)")
    ap.add_argument("--user", default=None, help="your Instagram username")
    ap.add_argument("--url", default=None,
                    help="explicit saved/collection URL (overrides --user)")
    ap.add_argument("--limit", type=int, default=None, help="max posts to list")
    ap.add_argument("--out", default=None, help="write URL list here")
    args = ap.parse_args()

    if not Path(args.cookies).is_file():
        log(f"cookies file not found: {args.cookies}")
        sys.exit(1)

    url = args.url or (f"https://www.instagram.com/{args.user}/saved/"
                       if args.user else None)
    if not url:
        log("provide --user or --url")
        sys.exit(1)

    cmd = ["gallery-dl", "--cookies", args.cookies, "--dump-json"]
    if args.limit:
        cmd += ["--post-range", f"1-{args.limit}"]
    cmd.append(url)
    log("$", " ".join(cmd[:3]), "... ", url)

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 and not r.stdout.strip():
        msg = (r.stderr or "gallery-dl failed").strip()[-800:]
        log("gallery-dl error (auth/cookies/rate-limit?):")
        log(msg)
        sys.exit(2)

    shortcodes = []
    try:
        walk(json.loads(r.stdout), shortcodes)
    except Exception:
        # Fall back to scraping permalinks straight from the raw output.
        for m in PERMALINK_RE.findall(r.stdout):
            shortcodes.append(m)

    seen, urls = set(), []
    for sc in shortcodes:
        u = f"https://www.instagram.com/p/{sc}/"
        if u not in seen:
            seen.add(u)
            urls.append(u)

    for u in urls:
        print(u)
    if args.out:
        Path(args.out).write_text("\n".join(urls) + ("\n" if urls else ""),
                                  encoding="utf-8")
    log(f"found {len(urls)} saved posts"
        + (f" -> {args.out}" if args.out else ""))
    if not urls:
        log("nothing extracted — check that cookies are valid and the account "
            "actually has saved posts, or pass --url with a specific collection.")


if __name__ == "__main__":
    main()
