#!/usr/bin/env bash
# Installs the tools the visual-content skill needs.
# Everything comes from PyPI, which is reachable directly (whitelisted through
# the agent proxy), so this is reliable even when apt mirrors are not.
#
#   yt-dlp          -> download videos + metadata + subtitles from 1000+ sites
#   gallery-dl      -> download image posts / carousels (Instagram, X, etc.)
#   imageio-ffmpeg  -> ships a static ffmpeg binary (no apt / sudo needed)
#
# Idempotent: safe to run repeatedly. Prints where ffmpeg ended up.
set -euo pipefail

log() { printf '[visual-content:setup] %s\n' "$*" >&2; }

PIP=(python3 -m pip install --quiet --disable-pip-version-check)

need() { command -v "$1" >/dev/null 2>&1; }

# 1) yt-dlp -------------------------------------------------------------------
if need yt-dlp; then
  log "yt-dlp present ($(yt-dlp --version 2>/dev/null))"
else
  log "installing yt-dlp ..."
  "${PIP[@]}" --upgrade yt-dlp || "${PIP[@]}" --user --upgrade yt-dlp
fi

# 2) gallery-dl ---------------------------------------------------------------
if need gallery-dl; then
  log "gallery-dl present ($(gallery-dl --version 2>/dev/null))"
else
  log "installing gallery-dl ..."
  "${PIP[@]}" --upgrade gallery-dl || "${PIP[@]}" --user --upgrade gallery-dl
fi

# 3) ffmpeg (system, else pip-provided static binary) -------------------------
if need ffmpeg; then
  log "ffmpeg present ($(command -v ffmpeg))"
else
  log "system ffmpeg missing; installing imageio-ffmpeg (bundled binary) ..."
  "${PIP[@]}" --upgrade imageio-ffmpeg || "${PIP[@]}" --user --upgrade imageio-ffmpeg
  FF="$(python3 -c 'import imageio_ffmpeg,sys; sys.stdout.write(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null || true)"
  if [ -n "${FF:-}" ] && [ -x "$FF" ]; then
    log "ffmpeg binary at: $FF"
  else
    log "WARNING: could not obtain ffmpeg. Video frame extraction will be skipped."
  fi
fi

log "setup complete."
