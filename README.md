# visual-content skill

A Claude Code skill that lets Claude **read and understand any visual content**
you share — not just its text.

Drop in one or many:

- **Instagram** posts, reels, carousels
- **X / Twitter** posts (image or video)
- **TikTok**, **YouTube** (incl. Shorts), **Vimeo**, **Facebook**, and 1000+
  other sites
- Standalone **image** or **video** URLs, or **local** image/video files

…and Claude will download the media, turn videos into readable frames, pull in
captions/subtitles/metadata, and then actually *see* it — describing the
visuals, transcribing on-screen/spoken text, and answering whatever you asked.
Multiple posts / images / videos at once are handled in a single pass.

## How it works

1. **Download** — `yt-dlp` for videos (+ metadata + subtitles), `gallery-dl`
   for image posts/carousels, plain download for direct URLs.
2. **Make videos readable** — `ffmpeg` samples evenly-spaced JPEG frames, so a
   video becomes a sequence of images Claude can read with native vision.
3. **Flatten text** — subtitles/auto-captions and post metadata become `.txt`.
4. **Read + report** — Claude reads every frame/image/text file and tells you
   what's in the media.

No system packages or `sudo` required — all tools install from PyPI, including
a bundled `ffmpeg`.

## Usage

The skill activates on its own when you share visual content. To drive it
manually:

```bash
# one-time per session
bash .claude/skills/visual-content/scripts/setup.sh

# fetch + prepare one or more targets
python3 .claude/skills/visual-content/scripts/grab.py \
  "<url-or-path>" ["<url2>" ...] --out ./work --frames 12
```

`grab.py` prints a JSON manifest listing the image files to read
(`all_images_to_read`) and text files to read (`all_text_to_read`).

See [`.claude/skills/visual-content/SKILL.md`](.claude/skills/visual-content/SKILL.md)
for the full workflow, and `references/` for supported platforms and handling
login-gated content.

## Layout

```
.claude/skills/visual-content/
├── SKILL.md                 # workflow Claude follows
├── scripts/
│   ├── setup.sh             # installs yt-dlp, gallery-dl, ffmpeg (via pip)
│   └── grab.py              # download + frame extraction + manifest
└── references/
    ├── platforms.md         # what's supported and how routing works
    └── auth.md              # cookies for private content; full transcripts
```
