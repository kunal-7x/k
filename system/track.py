#!/usr/bin/env python3
"""
track.py — the idea/feature/product tracker for this workspace.

One hub, many threads. Every idea, feature, product, reel, or task you submit
becomes a tracked ITEM with a status, so nothing (past, present, or future)
gets lost in the chat. This is the source of truth; DASHBOARD.md is a rendered,
human-readable view regenerated from registry.json on every change.

Commands:
  add     --title T [--source URL] [--type TYPE] [--status S] [--priority P]
          [--next "next action"] [--notes "..."] [--artifact PATH ...]
  update  --id T-003 [--status S] [--priority P] [--next "..."] [--notes "..."]
          [--title T] [--add-artifact PATH ...]
  list    [--status S] [--type TYPE]
  render  (regenerate DASHBOARD.md)

TYPE:     content | feature | product | research | idea   (free-form allowed)
STATUS:   inbox | in-progress | blocked | done | dropped
PRIORITY: high | med | low

Examples:
  python3 system/track.py add --title "3D walk-viewer" --type feature \
      --source "ig reel DakwVRrp3tb" --status in-progress --priority high \
      --next "wire nipplejs joystick"
  python3 system/track.py update --id T-004 --status done --add-artifact viewer/index.html
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "registry.json"
DASHBOARD = ROOT / "DASHBOARD.md"

STATUS_ORDER = ["in-progress", "blocked", "inbox", "done", "dropped"]
STATUS_EMOJI = {
    "in-progress": "🔨", "blocked": "⛔", "inbox": "📥",
    "done": "✅", "dropped": "🗑️",
}


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def load():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {"items": []}


def save(data):
    REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    render(data)


def next_id(data):
    n = 0
    for it in data["items"]:
        try:
            n = max(n, int(str(it["id"]).split("-")[1]))
        except (IndexError, ValueError):
            pass
    return f"T-{n + 1:03d}"


def cmd_add(args, data):
    item = {
        "id": next_id(data),
        "title": args.title,
        "source": args.source or "",
        "type": args.type or "idea",
        "status": args.status or "inbox",
        "priority": args.priority or "med",
        "created": now(),
        "updated": now(),
        "next_action": args.next or "",
        "notes": args.notes or "",
        "artifacts": list(args.artifact or []),
    }
    data["items"].append(item)
    save(data)
    print(f"added {item['id']}: {item['title']} [{item['status']}]")


def cmd_update(args, data):
    for it in data["items"]:
        if it["id"] == args.id:
            if args.status:   it["status"] = args.status
            if args.priority: it["priority"] = args.priority
            if args.next is not None:   it["next_action"] = args.next
            if args.notes is not None:  it["notes"] = args.notes
            if args.title:    it["title"] = args.title
            if args.source:   it["source"] = args.source
            for a in (args.add_artifact or []):
                if a not in it["artifacts"]:
                    it["artifacts"].append(a)
            it["updated"] = now()
            save(data)
            print(f"updated {it['id']}: {it['title']} [{it['status']}]")
            return
    print(f"no item with id {args.id}")


def cmd_list(args, data):
    for it in data["items"]:
        if args.status and it["status"] != args.status:
            continue
        if args.type and it["type"] != args.type:
            continue
        print(f"{it['id']} [{it['status']}/{it['priority']}] {it['title']}"
              + (f"  <- {it['source']}" if it["source"] else ""))


def render(data):
    items = data["items"]
    counts = {s: 0 for s in STATUS_ORDER}
    for it in items:
        counts[it.get("status", "inbox")] = counts.get(it.get("status", "inbox"), 0) + 1
    lines = []
    lines.append("# 📋 Dashboard — idea & project tracker")
    lines.append("")
    lines.append("> One hub, many threads. Auto-generated from `registry.json` "
                 "by `track.py` — do not edit by hand.")
    lines.append("")
    summary = " · ".join(f"{STATUS_EMOJI[s]} {counts[s]} {s}"
                         for s in STATUS_ORDER if counts.get(s))
    lines.append(f"**{len(items)} items** — {summary}")
    lines.append("")
    for s in STATUS_ORDER:
        group = [it for it in items if it.get("status") == s]
        if not group:
            continue
        lines.append(f"## {STATUS_EMOJI[s]} {s.title()} ({len(group)})")
        lines.append("")
        lines.append("| ID | Pri | Item | Type | Next action / notes | Artifacts | Source |")
        lines.append("|----|-----|------|------|---------------------|-----------|--------|")
        pri_rank = {"high": 0, "med": 1, "low": 2}
        for it in sorted(group, key=lambda x: pri_rank.get(x.get("priority"), 1)):
            arts = "<br>".join(f"`{a}`" for a in it.get("artifacts", [])) or "—"
            nxt = it.get("next_action") or it.get("notes") or "—"
            src = it.get("source") or "—"
            lines.append(
                f"| {it['id']} | {it.get('priority','')} | {it['title']} | "
                f"{it.get('type','')} | {nxt} | {arts} | {src} |")
        lines.append("")
    lines.append("---")
    lines.append(f"_Last rendered: {now()}_")
    DASHBOARD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="idea/project tracker")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--source"); a.add_argument("--type"); a.add_argument("--status")
    a.add_argument("--priority"); a.add_argument("--next"); a.add_argument("--notes")
    a.add_argument("--artifact", action="append")

    u = sub.add_parser("update")
    u.add_argument("--id", required=True)
    u.add_argument("--status"); u.add_argument("--priority"); u.add_argument("--next")
    u.add_argument("--notes"); u.add_argument("--title"); u.add_argument("--source")
    u.add_argument("--add-artifact", action="append")

    l = sub.add_parser("list")
    l.add_argument("--status"); l.add_argument("--type")

    sub.add_parser("render")

    args = ap.parse_args()
    data = load()
    if args.cmd == "add":
        cmd_add(args, data)
    elif args.cmd == "update":
        cmd_update(args, data)
    elif args.cmd == "list":
        cmd_list(args, data)
    elif args.cmd == "render":
        render(data)
        print("rendered DASHBOARD.md")


if __name__ == "__main__":
    main()
