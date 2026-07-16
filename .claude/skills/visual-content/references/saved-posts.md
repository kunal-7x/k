# Reading a user's saved Instagram posts (safely)

The safe, no-password, ToS-compliant way to hand Claude every post the user has
saved. No login or credentials are shared.

## Step 1 — user exports their saved posts

In the Instagram app (or instagram.com):

1. **Settings and privacy** → **Accounts Center**
2. **Your information and permissions** → **Download your information**
3. **Download or transfer information** → choose the account
4. Select **Some of your information** → tick **Saved** (a.k.a. "Saved posts")
5. Format: **JSON** (preferred) or HTML · Date range: **All time**
6. Submit. Instagram emails a download link (minutes to a few hours). It's a zip.

## Step 2 — extract the URLs

Point `ingest_saved.py` at the unzipped export (a file or the whole folder):

```bash
python3 .claude/skills/visual-content/scripts/ingest_saved.py \
  <export-file-or-dir> --out saved_urls.txt
```

Handles the JSON export (`saved_saved_media`), the HTML export, or any file with
Instagram URLs in it; dedupes and normalizes.

## Step 3 — read + understand each post

Batch the URLs through `grab.py` (do it in chunks of ~10-20 to keep runs light):

```bash
python3 .claude/skills/visual-content/scripts/grab.py \
  $(head -n 15 saved_urls.txt) --out ./work --frames 10
```

Then read the manifest's images/text and, if desired, run each through the
**content-engine** skill to brief them and produce content.

## Alternative — live cookie access (risky, opt-in only)

Only when the user has **explicitly accepted the ban risk**. Uses Instagram's
unofficial API via their session cookies — never their password.

1. User exports **cookies** from a browser logged into Instagram:
   - Extension "Get cookies.txt LOCALLY" (Chrome/Firefox) → save `cookies.txt`, or
   - `gallery-dl --cookies-from-browser chrome --cookies-export cookies.txt`
   Keep `cookies.txt` in a scratch/temp dir — it is a live credential and is
   gitignored; never commit it.
2. List saved posts:
   ```bash
   python3 .claude/skills/visual-content/scripts/saved_live.py \
     --cookies cookies.txt --user <username> --limit 30 --out saved_urls.txt
   ```
3. Read them with `grab.py` in batches (same as the export flow).

If gallery-dl errors on auth/rate-limit, the script reports it — surface that,
don't retry aggressively (hammering the private API is what triggers blocks).
Never ask for or store the password; cookies only.

## Notes & limits

- Some saved posts may be from **private accounts** or since **deleted** — those
  can fail to download; the manifest's `errors` will show it. Report honestly.
- The export lists what's saved at export time; it's a **snapshot**, not live.
  For an ongoing feed the user must re-export (safe) or connect live access
  (see the risk note in the content-engine `connecting-accounts.md`).
- Never ask for or store the user's Instagram password. The export needs none.
