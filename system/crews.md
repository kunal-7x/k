# 🏢 The Workspace, run like a company

Inspired by @leadgenman / Norbert Bezzina: *don't treat Claude Code like one
assistant — run it like a company.* Skills are **employees**, grouped into
**crews** (departments). This file is the org chart. The tracker
(`system/DASHBOARD.md`) is the project board; `content/` is the output; each
crew's skills are threads.

Legend: ✅ built · 🔨 in progress · 🗓️ planned

## 🎥 Content Crew — read the world, make the content
| Skill | Status | Does |
|-------|--------|------|
| `visual-content` | ✅ | Reads any reel/post/image/video (frames + captions). |
| `content-engine` | ✅ | Turns anything read into brand-adapted deliverables. |
| `saved-posts ingest` (`ingest_saved.py` / `saved_live.py`) | ✅ tool | Pulls IG saved posts (export = safe; cookies = live). |
| `publisher` (IG/X/LinkedIn) | 🗓️ | Auto-publish once accounts are connected. |

## 🧭 Operations Crew — nothing gets dropped
| Skill | Status | Does |
|-------|--------|------|
| `tracker` (`system/track.py`) | ✅ | One hub, many threads; the dashboard. |
| `session-start-hook` (built-in) | 🗓️ | Bootstrap the workspace each web session. |
| `scheduler` (routines / `/loop`) | 🗓️ | Run the inbox + PR check-ins on a timer. |

## 🔬 Research Crew — find out how, with proof
| Skill | Status | Does |
|-------|--------|------|
| `deep-research` (built-in) | ✅ | Multi-source, fact-checked reports. |
| `ultracode workflows` | ✅ | Parallel multi-agent research/build (e.g. the 3D guide). |

## 🛠️ Build Crew — ship the actual thing
| Skill | Status | Does |
|-------|--------|------|
| `3D walk-viewer` (`viewer/`) | ✅ | Joystick Gaussian-splat walkthrough, self-host. |
| `run` / `verify` (built-in) | ✅ | Launch + verify changes in the real app. |
| `automation builder` | 🗓️ | Turn a manual task from a reel into a working script. |

## 📣 Growth Crew — turn output into audience
| Skill | Status | Does |
|-------|--------|------|
| `content-engine` (repurpose) | ✅ | Cross-platform variants of one idea. |
| `keyword-DM automation` | 🗓️ | "Comment WORD" → auto-DM (ManyChat / Meta API). |
| `analytics` | 🗓️ | Track link/tour/post performance. |

## 💼 Business Crew — the money + the fine print
| Skill | Status | Does |
|-------|--------|------|
| `finance/modeling` | 🗓️ | Pricing, ROI, unit economics for offers. |
| `legal/review` | 🗓️ | Read the fine print (ToS, contracts) — flag, don't advise. |

## 🔌 Connectors Crew — reach outside
| Connector | Status | Does |
|-----------|--------|------|
| GitHub (MCP) | ✅ | PRs, reviews, CI. |
| Meta (MCP) | 🔨 needs auth | Instagram publishing once authorized. |
| Apollo / Shopify (MCP) | ✅ available | Leads / store ops when a task needs them. |

---

## How a new idea flows through the company
1. You drop a link/idea → **Content Crew** reads it (`visual-content`).
2. **Operations** logs it as a thread (`track.py` → DASHBOARD).
3. **Research** figures out how (if needed); **Build** ships it.
4. **Content/Growth** turn the result into a post; **Connectors** publish it.
5. Every step is a tracked thread — the main chat stays the hub, the work lives
   in files.

## Next hires (build order)
1. `scheduler` — make the inbox + check-ins run on a timer (always-on).
2. `publisher` + Meta auth — close the loop to live posting.
3. `keyword-DM automation` — the "Comment WORD" engine every top post uses.
