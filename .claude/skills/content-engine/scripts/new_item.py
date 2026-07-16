#!/usr/bin/env python3
"""
new_item.py — scaffold a content-pipeline item with consistent naming.

Creates a brief file under content/briefs/ from a template and appends an entry
to content/ideas-inbox.md so the item is tracked. Filenames use a caller-passed
sequence prefix (the script does not use wall-clock time, so it is deterministic).

Usage:
  python3 new_item.py --slug "hook-teardown" --source "<url-or-desc>" \
      [--seq 007] [--root .]

Prints the created brief path.
"""
import argparse
import re
from pathlib import Path

BRIEF_TEMPLATE = """# Brief: {title}

- **Source:** {source}
- **Status:** new
- **Deliverables:** (fill: reel / carousel / thread / linkedin / automation)

## The play
- **Format:**
- **Hook (verbatim):**
- **Why it works:**
- **Structure (beats):**
- **CTA / engagement driver:**

## Adapted to our brand
- **Our angle:**
- **Our hook:**

## Deliverables produced
- (link each finished file in content/drafts/)

## Un-asked extras
- (repurposes, follow-up ideas, timing, series arc)

## Publish status
- ready-to-post: yes/no — what's needed to publish
"""


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s[:48] or "item"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="short name for the item")
    ap.add_argument("--source", default="", help="source URL or description")
    ap.add_argument("--seq", default="000", help="sequence prefix, e.g. 007")
    ap.add_argument("--root", default=".", help="repo root")
    args = ap.parse_args()

    root = Path(args.root)
    briefs = root / "content" / "briefs"
    inbox = root / "content" / "ideas-inbox.md"
    briefs.mkdir(parents=True, exist_ok=True)

    slug = slugify(args.slug)
    seq = re.sub(r"[^0-9]", "", args.seq) or "000"
    name = f"{seq}-{slug}.md"
    brief_path = briefs / name

    title = args.slug.strip().title()
    brief_path.write_text(
        BRIEF_TEMPLATE.format(title=title, source=args.source or "(none)"),
        encoding="utf-8",
    )

    # Append to inbox (create with header if missing).
    if not inbox.exists():
        inbox.write_text(
            "# Ideas inbox\n\n"
            "Drop links/ideas here. `content-engine` processes anything marked "
            "`new`.\n\n"
            "| seq | item | source | status | brief |\n"
            "|-----|------|--------|--------|-------|\n",
            encoding="utf-8",
        )
    with inbox.open("a", encoding="utf-8") as f:
        f.write(f"| {seq} | {slug} | {args.source or '-'} | new | "
                f"content/briefs/{name} |\n")

    print(str(brief_path))


if __name__ == "__main__":
    main()
