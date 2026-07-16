# Supported platforms

`grab.py` routes each target to the right downloader automatically:

| Target                                   | Tool used   | Notes                                   |
|------------------------------------------|-------------|-----------------------------------------|
| YouTube / Shorts, TikTok, Vimeo, Twitch  | `yt-dlp`    | video + metadata + subtitles/auto-caps  |
| Instagram reels & video posts            | `yt-dlp`    | frames extracted from the video         |
| Instagram photo posts & carousels        | `gallery-dl`| every image in the carousel             |
| X / Twitter posts (image or video)       | `gallery-dl`→`yt-dlp` fallback | images, else the video   |
| Threads, Pinterest, Reddit, Tumblr, etc. | `gallery-dl`| image posts                             |
| Direct `.jpg/.png/.mp4/...` URLs         | plain / `yt-dlp` | downloaded as-is                   |
| Local image/video files                  | (copied)    | frames extracted from local videos      |

## How routing works

`classify()` in `grab.py` inspects the URL/host and file extension:

- Known **video hosts** or `/reel/`, `/shorts/`, `/video/` paths → `yt-dlp`
  first, with `gallery-dl` as fallback.
- Known **image-post hosts** (instagram, x/twitter, threads, pinterest) →
  `gallery-dl` first, with `yt-dlp` as fallback (covers IG reels posted under
  a `/p/` URL, video tweets, etc.).
- **Direct media** extensions → downloaded directly.
- **Local paths** → copied in; videos get frame extraction.

Because each path has a fallback, a misclassified URL still usually succeeds.

## Full site list

`yt-dlp` alone supports 1000+ sites. To check a specific one:

```bash
yt-dlp --list-extractors | grep -i <site>
```

If neither tool supports a site, the manifest's `errors` will say so — report
that to the user instead of guessing at the content.
