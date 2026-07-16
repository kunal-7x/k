# Content pipeline

Persistent memory + working area for the `content-engine` skill. Because the
runtime container is ephemeral, everything here is **committed to the repo** so
the strategy compounds across sessions.

## How it flows

```
you share a reel/post/idea
        │
        ▼
  [visual-content]  read the media (frames, captions, metadata)
        │
        ▼
  [content-engine]  extract the play → adapt to profile.md → produce deliverables
        │
        ▼
  briefs/<seq>-<slug>.md     the analysis + plan
  drafts/<seq>-<slug>-*.md   the finished, ready-to-post deliverables
  ideas-inbox.md             the tracker (status: new → done)
```

## Files

- **`profile.md`** — the brand brain (voice, niche, audience, goals). Self-improving.
- **`ideas-inbox.md`** — everything shared, with status. Items marked `new` are
  the work queue; an always-on routine can process them.
- **`briefs/`** — one brief per idea: the play, why it works, our adaptation.
- **`drafts/`** — the actual deliverables (captions, carousels, threads, scripts).

## Publishing

Drafts are **ready-to-post**. Actually posting to live accounts needs those
accounts connected once — see
`.claude/skills/content-engine/references/connecting-accounts.md`. Until then,
publishing is copy-paste; after connecting, it can be automated.
