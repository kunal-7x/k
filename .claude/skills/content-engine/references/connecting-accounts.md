# Connecting accounts for publishing

I can produce everything up to the publish tap. To actually post to a **live**
account, that account must be connected once. This is a platform requirement,
not a permission I'm withholding — the keys belong to the user.

## Instagram (via Meta)

Instagram publishing goes through the **Meta Graph API**, which needs:
1. An Instagram **Business** or **Creator** account, linked to a Facebook Page.
2. A Meta app with the `instagram_content_publish` permission.
3. A long-lived access token.

In this environment there is a **Meta connector** (`meta_MCP`) that is currently
**unauthorized**. Authorize it from an interactive session:
- claude.ai connectors: enable/authorize the Meta connector in connector settings.
- Claude Code CLI: `/mcp` (interactive) to run the OAuth flow.

Once authorized, its posting tools become available (find them with ToolSearch).
Until then, deliver "ready-to-post" caption + media and hand off the copy-paste.

## X / Twitter

Needs X API access (a paid tier for write/post) with OAuth 1.0a or OAuth 2.0
user context credentials: API key/secret + access token/secret. Provide these as
environment variables or a connected connector; then posting can be scripted.

## LinkedIn

Needs a LinkedIn app with the `w_member_social` scope and a user OAuth token.
Company-page posting needs the organization admin scopes. Provide the token via
a connector or env var.

## The safe default

Even after connecting, keep a **light review before the first posts** — posting
under someone's identity is public and hard to reverse. Switch to full-auto
publishing only when the user explicitly asks. Never post anything that
impersonates a real person/brand or makes claims the user hasn't approved.

## What to tell the user

Be concrete: name the single step that unblocks publishing (e.g. "authorize the
Meta connector in your claude.ai settings, then I can publish IG directly"), and
keep delivering ready-to-post work in the meantime so nothing is blocked.
