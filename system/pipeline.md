# 🔁 The Insta-automation pipeline (target architecture)

Executed from @ai_with_paawan's reel (DX1pGpBSjwo), which whiteboards a
"full-time social media manager" built on Claude. It maps almost 1:1 onto the
crews we're already building — this doc is our target pipeline and build order.

## What the reel showed (transcribed from the whiteboard)

```
                              Reviews          VM / "Claude Dispatch"
                                 │                    │
   Topic (AI) ──► Claude Code ──► creates ───► posting MCP ──► POST
                       │          carousel,    ("Zernio MCP")
                       │          caption
             ┌─────────┴─────────┐
        search new           skills
          trends           (pptx, ppt/resume)
```

Caption's claim: automated Instagram pipeline from **ideation → scheduling**,
"saves 10+ hours/week," built on Claude's API + custom scripts.

> Reading note: "Zernio MCP" is our best read of the whiteboard label for the
> posting MCP; the exact product name is unverified. The *role* (an MCP that
> publishes to Instagram) is what matters and is what we build to.

## Map to our system (what exists vs. what's missing)

| Reel stage | Our component | Status |
|------------|---------------|--------|
| Topic (AI) | ideas-inbox + `track.py` | ✅ built |
| Search new trends | Research crew (`deep-research`, ultracode) | ✅ built |
| Claude Code creates carousel + caption | `content-engine` | ✅ built |
| Skills (pptx, decks, etc.) | skill library (add as needed) | 🗓️ add per task |
| Reviews | light human/agent review gate | ✅ policy (draft-first) |
| Posting MCP ("Zernio MCP") → POST | **publisher** (Meta MCP / posting API) | 🔨 needs account auth |
| VM / "Claude Dispatch" | **scheduler** (routines / cron) | 🗓️ next build |

**Conclusion:** we already have the whole left half (ideate → research → create).
The two missing pieces to close the loop are exactly the two on the right:
**a scheduler** and **a publisher**. Neither is a mystery; both are scoped below.

## The two builds that close the loop

### 1. Scheduler — the "Claude Dispatch / VM" equivalent
A recurring trigger that wakes on a cadence, reads `content/ideas-inbox.md` for
anything `new`, runs the content-engine, and saves drafts — the "always-on"
worker. Implemented with a **Claude Code Remote Routine** (fresh session per
fire) or the `/loop` skill. No VM to rent — the routine is the dispatcher.
- **Safe default:** draft-only (produces ready-to-post content, does not publish).
- **One decision before enabling:** cadence (daily / weekly) — a recurring
  routine consumes compute each fire, so it's opt-in, one word to turn on.

### 2. Publisher — the posting MCP ("Zernio MCP") equivalent
The step that actually posts to Instagram. Options, cheapest-risk first:
- **Meta Graph API** via the Meta connector (already present, **needs auth**) —
  official IG publishing for Business/Creator accounts.
- A third-party scheduling API (Buffer/Later/Publer) with a token.
- The unofficial route (cookies) — works but ToS/ban risk (already scoped in
  `references/connecting-accounts.md`).
Until one is connected, the pipeline stops at "ready-to-post" and hands off.

## The end-to-end loop, once both are built
```
scheduler wakes ─► reads inbox ─► content-engine drafts carousel+caption
      ─► review gate ─► publisher posts (or hands you the ready draft)
      ─► track.py marks the thread done
```

That is the reel's pipeline, on our stack, with an honest gate at the one place
that touches your live audience.

## Next hire (build order, from `crews.md`)
1. **Scheduler** (this doc §1) — biggest leverage, buildable now, draft-safe.
2. **Publisher** (§2) — needs one account connection to go live.
3. Keyword-DM automation ("Comment WORD") — the engagement CTA every top post uses.
