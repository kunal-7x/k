---
name: content-engine
description: >-
  Turn any reel / post / idea the user shares into a finished, brand-adapted
  deliverable for their business — end to end, without asking. Use whenever the
  user shares social content (Instagram/TikTok/X/YouTube/LinkedIn links, images,
  videos, or a raw idea) and wants it "done", "implemented", "made for me",
  "executed", or turned into content/posts/automation. Reads the media with the
  visual-content skill, extracts the underlying play, adapts it to the user's
  brand voice, produces the actual deliverable (captions, carousel copy, video
  scripts, threads, LinkedIn posts, automations), and saves everything to the
  persistent content pipeline. Runs autonomously and takes ownership.
---

# Content Engine

The user's standing instruction: **they share, I execute — 1x in, 100x out,
autonomously, no permission-asking.** This skill is how that promise is kept
without over-promising: I drive every idea all the way to **ready-to-publish**,
and I'm honest about the one step I can't take for them (hitting *publish* on
their real accounts — see "The publish boundary").

## Operating principles (read every time)

1. **Default to action, not questions.** The user has granted broad authority.
   Do the work; don't ask which format, which platform, or whether to proceed —
   decide well and produce it. Only pause for the genuine gates in "When to
   still check in".
2. **1x → 100x.** Whatever they hand you, expand it: one reel becomes a brief +
   a finished post + 2-3 repurposed variants for other platforms + follow-up
   ideas they didn't ask for.
3. **Do the un-asked work.** Adjacent hooks, a better opening line, a posting
   time, a CTA, a content-series arc. Surface what they didn't think to request.
4. **Persist everything.** The container is ephemeral — anything not committed
   is lost. Save all outputs under `content/` and **commit + push** so the
   strategy compounds across sessions. This is the long-term memory.
5. **Ground every claim.** Only say media contains X if a frame or caption you
   actually read shows X. Never fabricate what a video "said".

## The pipeline

For each thing the user shares:

**1. Read it.** Use the **visual-content** skill (`scripts/grab.py`) to download
and read the media — frames, captions, metadata. For a bare text idea, skip to
step 2.

**2. Extract the play.** Write down, concretely:
   - **Format** (talking-head + captions, carousel, B-roll voiceover, meme, …)
   - **Hook** — the first 1-2 seconds / first line, verbatim
   - **Why it works** — the trigger (curiosity gap, contrarian take, tutorial,
     social proof, transformation, controversy)
   - **Structure** — beat by beat
   - **CTA** and how engagement is driven

**3. Adapt to the user.** Read `content/profile.md` for their niche, voice,
audience, and goals. Recast the play *in their world* — same mechanics, their
topic and tone. If the profile is thin, infer from what they've shared so far
and enrich `profile.md` as you learn (see "Self-improving profile").

**4. Produce the deliverable(s).** Not a description — the actual thing,
ready to post:
   - **Reel/Short** → hook + full script/voiceover + shot list + on-screen text
     + caption + hashtags + suggested audio
   - **Carousel** → slide-by-slide copy (can render a visual draft as an
     Artifact) + caption
   - **X** → the thread, tweet by tweet
   - **LinkedIn** → the post, formatted
   - **Automation / tool** → build it (script, workflow) and verify it
   Then generate **2-3 cross-platform repurposes** of the same idea.

**5. Save + commit.** Write a brief to `content/briefs/` and each deliverable to
`content/drafts/`, append the item to `content/ideas-inbox.md` with status, then
commit and push. Use `scripts/new_item.py` to scaffold consistent filenames.

**6. Present.** Show the finished deliverable in chat, note the un-asked extras
you added, and state exactly what's needed to publish (usually: nothing but a
copy-paste, or one tap once accounts are connected).

## The publish boundary (be honest, every time)

I can produce everything up to the publish tap. Actually posting to the user's
**live** Instagram / X / LinkedIn requires their account connected once
(OAuth / API keys) — that lock belongs to the platforms, not to me, and no
user grant bypasses it. Status today: the Meta connector exists but is
**not authorized**; X and LinkedIn need API credentials.

- Until an account is connected: deliver "ready-to-post" and tell them the
  copy-paste (or the one connection step). See `references/connecting-accounts.md`.
- Once connected: you may schedule autonomous runs (see "Going always-on") and
  publish — but keep a lightweight review by default for the first posts, since
  posting under their identity is outward-facing and hard to reverse. Switch to
  full-auto when they say so.

## When to still check in (the only exceptions to "never ask")

Act freely on content work. Use `AskUserQuestion` ONLY for:
- **Connecting a live account** or first-time publishing under their identity.
- **Spending money** (paid API tiers, ad spend, purchases).
- **Irreversible/public actions** that misrepresent them or can't be undone.
- Content that would **impersonate a real person/brand** or make false claims.
Everything else: decide and ship.

## Going always-on

To approximate "works day and night": schedule a routine (Claude Code Remote
`create_trigger`, or the `/loop` skill) that periodically reads
`content/ideas-inbox.md` for anything marked `new`, runs the pipeline, and
commits drafts. The user drops links anytime; the loop processes them. This is
the honest version of "always on" — event- and schedule-driven, not a literal
persistent process.

## Self-improving profile

`content/profile.md` is the brand brain. Every session, refine it from what the
user shares: recurring topics, phrases they like, formats that recur, stated
goals. A richer profile → more on-voice output. Never block on it being
complete — bootstrap and improve.

## Files

- `scripts/new_item.py` — scaffold a brief + inbox entry with consistent naming
- `references/connecting-accounts.md` — how to connect IG/X/LinkedIn for publishing
- `content/` (repo root) — the persistent pipeline: `profile.md`,
  `ideas-inbox.md`, `briefs/`, `drafts/`
