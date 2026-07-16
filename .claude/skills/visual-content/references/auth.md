# Login-gated content & full transcripts

## Private / login-gated / age-restricted posts

Public posts download with no auth. For content that requires being logged in
(private accounts, age-restricted videos, some carousels), supply cookies:

```bash
python3 .claude/skills/visual-content/scripts/grab.py "<url>" \
  --out <dir> --cookies /path/to/cookies.txt
```

`cookies.txt` must be in **Netscape format**. Two common ways to get one:

1. **Browser extension** — "Get cookies.txt LOCALLY" (Chrome/Firefox) exports
   the current site's cookies in the right format. Export while logged in.
2. **yt-dlp from your browser** (on a machine with the browser installed):
   ```bash
   yt-dlp --cookies-from-browser chrome --cookies cookies.txt --skip-download "<url>"
   ```

Then hand the file path to `--cookies`. Never commit cookies to the repo — they
are credentials. Keep them in a scratch/temp location.

If a download fails for lack of auth, the manifest `errors` field will show a
message like "login required" / "private" — pass cookies and retry.

## Full spoken transcript when there are no captions

`grab.py` already pulls subtitles / auto-captions when a platform provides them
(YouTube usually does; Instagram/TikTok often don't). Combined with the video
frames, that is normally enough to understand a clip.

When you truly need a verbatim transcript of the **audio** and no captions
exist, transcribe the downloaded audio locally with Whisper:

```bash
python3 -m pip install --quiet faster-whisper
python3 - <<'PY'
from faster_whisper import WhisperModel
m = WhisperModel("base")               # or "small"/"medium" for accuracy
segments, info = m.transcribe("<path-to-video-or-audio>")
print("".join(s.text for s in segments))
PY
```

This is opt-in because the model download is large; skip it unless a full audio
transcript is specifically required.
