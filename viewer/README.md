# 3D Walk-Viewer — the reel's joystick walkthrough, on your own domain

A self-contained web viewer that reproduces the @thesaar.ai reel: an **on-screen
joystick** to walk through a **3D Gaussian-splat** scene, first-person, on a URL
you own and can track. No build step — it's one `index.html`.

This is Track D from `content/guides/001-3d-from-phone-howto.md`, made real.

## Quick start

1. **Capture a scene** with Scaniverse (free) → export a splat as `.ply`
   (or `.ksplat` / `.splat`).
2. **(Recommended) clean + shrink** it in SuperSplat (<https://superspl.at/editor>):
   crop the room, delete floaters, export. For best mobile performance convert
   to `.ksplat` (mkkellogg's compact format) — the viewer loads `.ply`,
   `.ksplat`, and `.splat`.
3. **Drop the file** next to `index.html` as `scene.ksplat` (or pass `?src=`).
4. **Serve it** (the ES-module imports need http, not `file://`):
   ```bash
   cd viewer && python3 -m http.server 8000
   # open http://localhost:8000/?src=scene.ksplat
   ```
5. **Deploy** the folder to Netlify / Vercel / GitHub Pages (all free) → you get
   your branded link, e.g. `tours.youragency.com`.

## Controls

- **Left joystick** (touch) or **WASD** (desktop) — walk.
- **Drag the right side of the screen** (touch) or **drag the mouse** — look around.
- Camera is pinned to eye height (1.6 m) and clamped to the room bounds, so you
  walk the floor instead of flying through walls.

## Tune per scene (top of `index.html`, `CONFIG`)

| Field | What it does |
|-------|--------------|
| `src` | splat file to load (or `?src=` in the URL) |
| `eyeHeight` | standing camera height, metres |
| `speed` | walk speed, m/s |
| `bounds` | room bounding box `{minX,maxX,minZ,maxZ}` — get from SuperSplat |
| `start` | initial camera position |

## Make the link trackable + per-address (the reel's "secure link")

Follow the recipe in the guide's "trackable, address-tied link" section:
- host per-listing paths (`/123-main-st`), append a per-recipient slug,
- add Plausible / Umami / Vercel Analytics to see who viewed and how often,
- optionally gate with a signed, expiring URL.

## Notes / gotchas

- **CORS:** if `scene.ksplat` is served from a different origin than the page,
  that origin must send `Access-Control-Allow-Origin`, or the load fails with a
  blank canvas. Simplest: keep the splat next to `index.html`.
- **File size:** raw `.ply` can be hundreds of MB. Convert to `.ksplat` and test
  on a real mid-range phone over cellular; target well under ~80 MB.
- **Dependencies** load from jsDelivr (three, @mkkellogg/gaussian-splats3d,
  nipplejs) via an import map. For a fully offline/self-contained deploy, vendor
  those three files locally and update the import map to relative paths.
- For real wall collision (not just a box clamp), export a low-poly collision
  mesh from your capture and raycast the move direction against it.
