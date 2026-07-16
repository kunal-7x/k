# system/ — the workspace hub

This is the "one door, many threads" you asked for. The main chat is the hub;
the actual work lives here and in `content/`, committed so nothing is ever lost
when a session ends.

## Files

- **`DASHBOARD.md`** — the board. Every idea/feature/product/reel you submit is a
  thread with a status (`in-progress` / `blocked` / `inbox` / `done` / `dropped`),
  priority, next action, and links to its artifacts. **Read this first** to see
  where everything stands. Auto-generated — don't hand-edit.
- **`registry.json`** — the machine-readable source of truth behind the board.
- **`track.py`** — add/update/list items and re-render the board.
- **`crews.md`** — the org chart: skills grouped into crews (departments), the
  "run Claude Code like a company" model. What's built vs. planned.

## Everyday use

```bash
# see the board
cat system/DASHBOARD.md

# add a new idea (I do this automatically whenever you send one)
python3 system/track.py add --title "..." --source "<link>" --type idea \
    --status inbox --priority high --next "first step"

# move it forward
python3 system/track.py update --id T-00X --status in-progress
python3 system/track.py update --id T-00X --status done --add-artifact path/to/output
```

## The workflow (what happens when you drop a link or idea)

1. It's logged as a thread here (nothing skipped — past, present, future).
2. `visual-content` reads it if it's a post/reel/video.
3. It gets worked (research / build / content) — artifacts saved under
   `content/` or a project dir.
4. Its thread is moved to `done` with links to what was produced.
5. The main chat stays a clean hub; the detail lives in files you can revisit.

See `crews.md` for how the skills are organized and what to build next.
