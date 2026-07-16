#!/usr/bin/env python3
"""
grab.py — fetch visual media from a URL (or local file) and prepare it so an
agent with image vision can actually "see" it.

What it does
------------
1. Figures out whether the target is a video site, an image/social post, or a
   plain media URL / local file.
2. Downloads the media:
     - videos  -> yt-dlp (also grabs metadata + subtitles/auto-captions)
     - posts   -> gallery-dl (Instagram carousels, X image tweets, etc.)
     - direct  -> plain download
3. For every video, extracts evenly-spaced JPEG frames (so they can be read as
   images) plus first/last frames, and copies any subtitle track to .txt.
4. Prints a JSON manifest to stdout listing every readable artifact:
     images (post pictures + video frames), text (captions/subs/metadata).

The agent then Reads the listed image files (native vision) and text files to
understand the visual content — images AND video.

Usage
-----
  python3 grab.py <url-or-path> [--out DIR] [--frames N] [--cookies FILE]

Exit code is always 0 when a manifest is produced (even partial); the manifest
carries per-item errors so the caller can see what failed.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


def log(*a):
    print("[visual-content:grab]", *a, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# tool discovery
# ---------------------------------------------------------------------------
def which(name):
    return shutil.which(name)


def ffmpeg_path():
    p = which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg  # type: ignore
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


VIDEO_HOST_HINTS = (
    "youtube.com", "youtu.be", "tiktok.com", "vimeo.com", "dailymotion.com",
    "twitch.tv", "streamable.com", "facebook.com/watch", "/video/", "/reel/",
    "/reels/", "/shorts/",
)
IMAGE_POST_HINTS = ("instagram.com", "twitter.com", "x.com", "threads.net", "pinterest.")
VIDEO_EXT = {".mp4", ".mkv", ".webm", ".mov", ".avi", ".m4v", ".gif"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".heic"}


def classify(target: str) -> str:
    low = target.lower()
    if os.path.exists(target):
        if os.path.isdir(target):
            return "local_directory"
        ext = Path(target).suffix.lower()
        if ext in VIDEO_EXT:
            return "local_video"
        if ext in IMAGE_EXT:
            return "local_image"
        return "local_other"
    if any(h in low for h in VIDEO_HOST_HINTS):
        return "video_site"
    ext = Path(low.split("?")[0]).suffix
    if ext in VIDEO_EXT:
        return "direct_video"
    if ext in IMAGE_EXT:
        return "direct_image"
    if any(h in low for h in IMAGE_POST_HINTS):
        return "image_post"
    # Unknown web URL: try video tooling first (yt-dlp handles most media),
    # fall back to gallery-dl handled by caller.
    return "unknown_url"


# ---------------------------------------------------------------------------
# downloaders
# ---------------------------------------------------------------------------
def run(cmd, **kw):
    log("$", " ".join(str(c) for c in cmd))
    return subprocess.run(cmd, **kw)


def ytdlp_download(url, outdir, cookies, want_subs=True):
    if not which("yt-dlp"):
        return None, "yt-dlp not installed (run setup.sh)"
    tmpl = str(outdir / "%(title).80s-%(id)s.%(ext)s")
    cmd = [
        "yt-dlp", "--no-playlist", "--no-warnings",
        "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
        "--merge-output-format", "mp4",
        "--write-info-json",
        "-o", tmpl,
    ]
    if want_subs:
        cmd += ["--write-subs", "--write-auto-subs", "--sub-langs", "en.*,en",
                "--convert-subs", "srt"]
    if cookies:
        cmd += ["--cookies", cookies]
    cmd.append(url)
    r = run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return None, (r.stderr or r.stdout or "yt-dlp failed").strip()[-800:]
    return True, None


def gallerydl_download(url, outdir, cookies):
    if not which("gallery-dl"):
        return None, "gallery-dl not installed (run setup.sh)"
    cmd = ["gallery-dl", "-D", str(outdir)]
    if cookies:
        cmd += ["--cookies", cookies]
    cmd.append(url)
    r = run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return None, (r.stderr or r.stdout or "gallery-dl failed").strip()[-800:]
    return True, None


def plain_download(url, outdir):
    name = Path(url.split("?")[0]).name or "download"
    dest = outdir / name
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(dest, "wb") as f:
            shutil.copyfileobj(resp, f)
        return dest, None
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# video frame extraction (no ffprobe dependency)
# ---------------------------------------------------------------------------
def video_duration(ff, path):
    # Parse "Duration: HH:MM:SS.xx" from ffmpeg stderr.
    r = subprocess.run([ff, "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", r.stderr or "")
    if not m:
        return None
    h, mm, ss = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h * 3600 + mm * 60 + ss


def extract_frames(ff, video, outdir, n_frames):
    dur = video_duration(ff, video)
    stem = Path(video).stem
    frames = []
    if not dur or dur <= 0:
        # Unknown duration: sample by scene changes, capped at n_frames.
        pat = str(outdir / f"{stem}-frame-%03d.jpg")
        run([ff, "-y", "-i", str(video), "-vf",
             "select='eq(n,0)+gt(scene,0.25)',scale=1024:-1",
             "-vsync", "vfr", "-frames:v", str(n_frames), "-q:v", "3", pat],
            capture_output=True, text=True)
        frames = sorted(str(p) for p in outdir.glob(f"{stem}-frame-*.jpg"))
        return frames, dur
    # Evenly spaced timestamps across the clip (skip the very edges).
    n = max(1, n_frames)
    for i in range(n):
        t = dur * (i + 0.5) / n
        out = outdir / f"{stem}-frame-{i:03d}.jpg"
        run([ff, "-y", "-ss", f"{t:.2f}", "-i", str(video),
             "-frames:v", "1", "-vf", "scale=1024:-1", "-q:v", "3", str(out)],
            capture_output=True, text=True)
        if out.exists():
            frames.append(str(out))
    return frames, dur


# ---------------------------------------------------------------------------
# subtitle / metadata flattening
# ---------------------------------------------------------------------------
def srt_to_text(srt_path, txt_path):
    try:
        raw = Path(srt_path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    lines = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln or ln.isdigit() or "-->" in ln:
            continue
        ln = re.sub(r"<[^>]+>", "", ln)
        if ln and (not lines or lines[-1] != ln):
            lines.append(ln)
    if not lines:
        return None
    Path(txt_path).write_text("\n".join(lines), encoding="utf-8")
    return txt_path


def info_json_to_text(info_path, txt_path):
    try:
        d = json.loads(Path(info_path).read_text(encoding="utf-8"))
    except Exception:
        return None
    parts = []
    for k in ("title", "uploader", "channel", "upload_date", "duration",
              "view_count", "like_count", "description"):
        if d.get(k) not in (None, "", []):
            parts.append(f"{k}: {d[k]}")
    if not parts:
        return None
    Path(txt_path).write_text("\n".join(str(p) for p in parts), encoding="utf-8")
    return txt_path


# ---------------------------------------------------------------------------
def collect(outdir):
    imgs, vids, texts = [], [], []
    for p in sorted(outdir.rglob("*")):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in IMAGE_EXT:
            imgs.append(p)
        elif ext in VIDEO_EXT:
            vids.append(p)
        elif ext in {".txt"}:
            texts.append(p)
    return imgs, vids, texts


def process(target, base_out, frames, cookies):
    kind = classify(target)
    log("classified as:", kind)

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", target.split("?")[0])[-48:].strip("-") or "media"
    outdir = Path(base_out) / slug if base_out else Path.cwd() / ".visual-cache" / slug
    outdir.mkdir(parents=True, exist_ok=True)

    errors = []

    # --- acquire media --------------------------------------------------
    if kind == "local_directory":
        errors.append(f"local directories are not supported: {target}")
    elif kind in ("local_video", "local_image", "local_other"):
        dst = outdir / Path(target).name
        if Path(target).resolve() != dst.resolve():
            shutil.copy2(target, dst)
    elif kind in ("video_site", "direct_video", "unknown_url"):
        ok, err = ytdlp_download(target, outdir, cookies)
        if not ok:
            errors.append(f"yt-dlp: {err}")
            # fall back to gallery-dl for unknown/image-ish URLs
            ok2, err2 = gallerydl_download(target, outdir, cookies)
            if not ok2:
                errors.append(f"gallery-dl: {err2}")
    elif kind == "image_post":
        ok, err = gallerydl_download(target, outdir, cookies)
        if not ok:
            errors.append(f"gallery-dl: {err}")
            ok2, err2 = ytdlp_download(target, outdir, cookies)
            if not ok2:
                errors.append(f"yt-dlp: {err2}")
    elif kind == "direct_image":
        dst, err = plain_download(target, outdir)
        if err:
            errors.append(f"download: {err}")

    # --- flatten subtitles + metadata to .txt ---------------------------
    for srt in list(outdir.rglob("*.srt")) + list(outdir.rglob("*.vtt")):
        srt_to_text(srt, srt.with_suffix(".txt"))
    for ij in outdir.rglob("*.info.json"):
        info_json_to_text(ij, ij.with_suffix("").with_suffix(".meta.txt"))

    # --- extract frames from every downloaded video ---------------------
    ff = ffmpeg_path()
    _, vids, _ = collect(outdir)
    frame_files = []
    if vids and not ff:
        errors.append("ffmpeg unavailable: cannot extract video frames (run setup.sh)")
    for v in vids:
        if ff:
            fr, dur = extract_frames(ff, v, outdir, frames)
            frame_files += fr
            log(f"extracted {len(fr)} frames from {v.name} (duration={dur})")

    # --- build manifest -------------------------------------------------
    imgs, vids, texts = collect(outdir)
    frame_set = set(frame_files)
    post_images = [str(p) for p in imgs if str(p) not in frame_set]

    manifest = {
        "target": target,
        "kind": kind,
        "out_dir": str(outdir),
        "images_to_read": sorted(post_images) + sorted(frame_files),
        "post_images": sorted(post_images),
        "video_frames": sorted(frame_files),
        "videos": [str(v) for v in vids],
        "text_to_read": [str(t) for t in texts],
        "errors": errors,
        "counts": {
            "post_images": len(post_images),
            "video_frames": len(frame_files),
            "videos": len(vids),
            "text_files": len(texts),
        },
    }
    return manifest


def main():
    ap = argparse.ArgumentParser(description="Fetch + prepare visual media for reading.")
    ap.add_argument("targets", nargs="+", help="one or more URLs or local paths")
    ap.add_argument("--out", default=None, help="base output dir (default ./.visual-cache)")
    ap.add_argument("--frames", type=int, default=12, help="frames to extract per video")
    ap.add_argument("--cookies", default=None,
                    help="cookies.txt for login-gated / private content")
    args = ap.parse_args()

    items = []
    for t in args.targets:
        try:
            items.append(process(t, args.out, args.frames, args.cookies))
        except Exception as e:
            items.append({"target": t, "kind": "error", "out_dir": "",
                          "images_to_read": [], "post_images": [],
                          "video_frames": [], "videos": [], "text_to_read": [],
                          "errors": [repr(e)],
                          "counts": {"post_images": 0, "video_frames": 0,
                                     "videos": 0, "text_files": 0}})

    # Merge convenience lists so the caller can read everything in one pass.
    all_images, all_text = [], []
    for it in items:
        all_images += it.get("images_to_read", [])
        all_text += it.get("text_to_read", [])

    out = {
        "items": items,
        "all_images_to_read": all_images,
        "all_text_to_read": all_text,
        "summary": {
            "targets": len(items),
            "total_images": len(all_images),
            "total_text_files": len(all_text),
        },
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
