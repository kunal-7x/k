# How to turn a real space or object into a navigable 3D scene you can share as a link (like the reel)

**What the reel actually shows, decoded.** A real-estate agent walks an apartment holding a phone; a capture app overlays a reticle + "Finish" button; the output is a smooth *first-person* 3D walkthrough you steer with an on-screen **joystick**, delivered as a **secure, trackable link tied to a property address.** Three separate things are bundled in that pitch, and it matters which tool gives you which:

1. **The continuous 3D look** (not a slideshow of photos) = **3D Gaussian Splatting (3DGS)** — millions of tiny colored 3D blobs reconstructed from overlapping phone frames, drawn by the browser GPU in real time.
2. **The joystick / first-person "walk"** = a **viewer feature.** No capture app produces the joystick by itself. You capture the splat with one tool, then load it into a walk-enabled viewer.
3. **The trackable, address-tied link** = a **hosting + analytics layer** you either buy (a real-estate tour platform) or self-host (your domain + an analytics script + per-recipient slugs).

> **Reality check on the reel's own product.** 20sec.video (promoted by @thesaar.ai) is an **AI marketing-video generator**: it ingests uploaded photos / a floor plan / a short clip (or auto-pulls MLS photos by address) and renders a promo video. The on-screen "scanning" reticle is UI dressing, not live photogrammetry. The tracks below reproduce the *actual capability* you asked for — a genuinely navigable 3D scene with a shareable link.

The guide is organized as four tracks — **A** (easiest phone app), **B** (real-estate tour workflow), **C** (single object), **D** (DIY open-source, the exact reel joystick) — plus a joystick deep-dive, a trackable-link recipe, a comparison table, and a weekend plan.

---

## The single most important split: capture vs. walk-viewer

| The reel feature | Who gives it to you |
|---|---|
| Photoreal continuous 3D | Any splat capture app (Scaniverse, Luma, Polycam, KIRI, RealityScan, Postshot…) |
| **On-screen joystick / first-person walk** | A **walk-mode viewer**: PlayCanvas SuperSplat Viewer (free, built-in Walk Mode), Luma's viewer (WASD), or a custom Three.js viewer + nipplejs |
| **Branded, trackable, per-address link** | A tour platform's analytics tier **or** your own domain + analytics script + per-recipient links |

Almost every "easy" app hands you a share link whose default navigation is **drag-to-orbit**, on the **vendor's domain**. Getting the *joystick* and the *branded trackable URL* is a deliberate second step. That step is the whole point of Track D and the two sections right after the tracks — do not skip them if matching the reel exactly is the goal.

---

## Track A — EASIEST: one phone app, live link today

**Best single pick: Scaniverse** (Niantic) — free, unlimited, on-device Gaussian splatting, hands you a browser link. <https://scaniverse.com>
*Runner-up for the cleanest embed story: **Luma AI** — <https://lumalabs.ai/interactive-scenes> (see the caveat below).*

**Steps:**
1. Install Scaniverse (iOS/Android, free). Choose **Splat** mode.
2. Hold the phone at chest height. Move **slowly and smoothly** through the room (for an object, orbit it in 2–3 rings at different heights). Keep the on-screen coverage guide filled, overlap heavily, avoid fast pans and motion blur. Even lighting matters.
3. Tap **Finish**. It processes **on-device** — no internet required.
4. Tap **Share / Upload** → you get a public web link anyone opens and interacts with in a browser (WebXR-capable too).

- **Cost:** Free, unlimited (capture, processing, sharing).
- **Output:** Gaussian splat, in-app + browser; exports `.SPZ`, `.PLY`, `.USDZ`, mesh.
- **Share link:** Yes — native public web link, **on scaniverse.com** (not your domain).
- **Gap vs. the reel:** the shared viewer defaults to **drag-to-orbit**, not a joystick walk. To get the walk, export the `.PLY`/`.SPZ` and load it into a walk-mode viewer (see "Reproducing the joystick" below). That is the *only* piece the easy path doesn't hand you.

**Luma caveat (important, 2026):** Luma still offers phone 3D capture with interactive-scene embeds (and its web viewer supports **WASD/keyboard walk**, a near-zero-effort partial match to the reel). But Luma has pivoted hard to its **Dream Machine** video product; the standalone 3D-capture line gets less attention, the free tier **watermarks exports and forbids commercial use**, and **commercial use requires the Plus plan (~$30/mo)**. Great for a quick embeddable demo — do **not** build a paid real-estate workflow on the free tier.

**Also worth knowing — RealityScan (Epic Games), free:** the app formerly seeded by RealityCapture is now **RealityScan Mobile** (iOS/Android), **free including for commercial use**, with AR-guidance capture and automated background removal. It's photogrammetry/mesh-focused (excellent for objects) rather than a one-tap splat-link tool, but it's a legitimate $0 capture option many guides drop.

---

## Track B — REAL-ESTATE virtual-tour workflow (shareable + trackable link)

Use this when the point is the *business workflow*: a per-listing link you send to buyers and can see who viewed. Pick by how close to the reel you need to look.

### B1 — Cheapest working shareable link (plain phone, $0)
**Zillow 3D Home** — free app. <https://www.zillow.com/3d-home/>
1. Install the free Zillow 3D Home app.
2. Shoot each room by slowly rotating the phone (a 360 camera is faster/cleaner).
3. It stitches → publishes to the Zillow listing **and** gives a shareable link.
- **Cost:** Free. **Nav:** click-hotspot between panoramas (**not** a joystick walk). **Track:** minimal.

### B2 — Shareable AND trackable (the reel's "secure trackable link")
- **CloudPano** — <https://www.cloudpano.com> — **Free** (3 tours, expire in 120 days); **Pro ~$27/mo** (≈$19/mo billed annually, unlimited tours); **Pro Plus ~$33/mo annual** (white-label branding, 8K uploads, lead capture, **analytics**); **Teams ~$199/mo annual** (5 users, agency analytics); Business custom. → **Analytics/lead-capture live on Pro Plus and up — budget $33/mo, not $19/mo, if "trackable" is the requirement.**
- **Ricoh360 Tours** — <https://www.ricoh360.com/tours/> — **~$45/mo (Pro; ~$39/mo annual)**, with **visitor analytics included** in the paid tier, plus optional AI staging / floor plans.

**Steps (either):** shoot with the app (plain phone) or a 360 camera (Ricoh Theta / Insta360 — faster, higher quality) → build the tour, add room-to-room paths → **publish** for a shareable/embeddable link → gate per-buyer with a password or unique link and tie it to the address. **Analytics = who viewed / how often = the "trackable" part**, and it is a **higher-tier feature on CloudPano** (Pro Plus) though **included on Ricoh360 Pro** — confirm the tier before promising it.

### B3 — True joystick first-person walkthrough (closest visual match)
- **Matterport** — <https://matterport.com/plans> — **Free** (1 space, includes analytics), **Starter ~$9.99/mo** (5 spaces), **Professional ~$69/mo** (25 spaces, MatterPak, custom branding), **Business ~$309/mo** (100 spaces); plus **~$20/mo per active space** hosting. **Analytics (walk-through heatmaps, dwell time, click-to-showing) are available on all plans, free included.** Gives a guided-path "digital twin" with dollhouse view + link — polished, but the nav is **guided waypoints**, not free joystick roaming.
- **For the exact game-like joystick free-movement:** a **Gaussian-splat real-estate platform** fed a phone video is the true match:
  - **Splat Labs** — <https://www.splatlabs.ai/solutions/real-estate> — quote-based (expect a **monthly SaaS / per-scene** commercial contract, typically **low-hundreds $/mo territory** for small teams; get a written quote — they don't publish a public price).
  - **Realsee** — enterprise 3D/VR tour platform (contact-sales pricing) with splat-quality walkthroughs.
  - **Gracia** — Gaussian-splat volumetric capture, VR-leaning.
- **The portals are doing this now, too:** **Zillow SkyTour** (launched mid-2025) and **Realtor.com FlyAround** (late 2025) are splat-based walkthrough features — evidence the reel's look is becoming table-stakes, and a distribution channel worth watching.

> **Why classic 360 tours can't give the joystick:** Zillow 3D Home, CloudPano, Kuula, Ricoh360, Asteroom navigate by **clicking hotspots** between fixed panoramas. Smooth free-roam "walking" is a **splat / true-3D** feature only. (Also note: **Kuula's** analytics are **Business-tier only** — the "trackable" gate varies by vendor.)

---

## Track C — a SINGLE OBJECT

Two **non-interchangeable** pipelines. Choose by whether you have the physical object and need it *dimensionally faithful*.

### C1 — Photo-scan a REAL object (dimensionally faithful)
**Best value: KIRI Engine** — <https://www.kiriengine.app> — handles shiny/featureless items; **Free tier gives unlimited *photogrammetry/mesh* exports, but 3D Gaussian-Splatting mode is a paid feature** — **Pro ~$17.99/mo or ~$99.99/yr** (some regions/older plans show $14.99/$59.99). **Flag this: KIRI is "free" for mesh scans, not for splats.**
**Alternative: Polycam** — <https://poly.cam/object-capture> — **Free** tier (up to 150 images/capture, GLTF export). **Gaussian Splatting + `.PLY` export require a paid plan: Basic ~$12.50/mo billed annually** is the cheapest tier that unlocks splats; higher Pro/Business tiers (~$26.99/mo up to $199.99/yr) add all 15+ export formats, unlimited scans, watermark-free. (Polycam retired the standalone "Pro" name — legacy Pro users keep their price.)
**Free heavy-duty option:** **RealityScan Mobile** (Epic, free, commercial-OK) for high-detail photogrammetry meshes.

**Capture technique (this is what separates a clean scan from mush):**
1. Choose **Object / Photo Scan** mode.
2. Walk a **full 360° orbit** taking **40–150 overlapping photos**, then a **second higher ring** (for tops) and a **third lower ring** (for undersides). Consistent, diffuse lighting.
3. **Shiny / transparent / thin objects break photogrammetry.** Use a **matte dulling spray** (or talc/dry shampoo) on reflective surfaces, put the object on a **turntable** against a plain matte backdrop, or switch to KIRI's **Featureless Object Scan** — or generate it instead (C2).
4. Process (~2 min in KIRI) → export `GLB`/`USDZ`.
5. **Link:** Polycam gives a hosted viewer page directly; KIRI one-click publishes to Sketchfab; or self-host (see the object-embed recipe below).

### C2 — AI-generate an object from TEXT or ONE IMAGE (seconds, no physical object)
Current generation (the older tools are a version behind — use these):
- **Microsoft TRELLIS-2** — <https://microsoft.github.io/TRELLIS.2/> — **open-source, MIT, free**, 4B-param image/text-to-3D with PBR materials and clean meshes; free web demos, GLB/OBJ/PLY export, no signup. **The strongest free single-object generator right now.**
- **Tencent Hunyuan3D (2.5 / 3.0)** — open-weights, self-hostable/free; hosted tiers up to ~$99/mo.
- **Tripo (v3 / P-series)** — <https://www.tripo3d.ai> — **Free** ~2,000 signup credits + monthly free credits (non-commercial); **Pro from ~$13.93/mo annual (~$19.90/mo monthly)** for commercial.
- **Meshy (5/6)** — <https://www.meshy.ai> — **Free** ~200 credits/mo; **Pro ~$20/mo**, Studio ~$60/mo.
- **Rodin / Hyper3D Gen-2 (2.5)** — <https://hyper3d.ai> — highest fidelity; **Creator ~$30/mo**, Business ~$120/mo, or ~$0.50+/model pay-per-download.

**Steps:** sign up → **Text-to-3D** or **Image-to-3D** → prompt or upload one reference image → wait ~30–60s → download `GLB` (also FBX/OBJ/USDZ/STL).

- **Link:** upload the GLB to **Sketchfab** for an orbitable embed (see note), to **Reflct** for a guided ecommerce-style viewer, or self-host with `<model-viewer>` (recipe below).
- **Warning:** generative AI **hallucinates unseen sides** and is **not dimensionally accurate** — never claim the output is "the actual product." Free tiers usually forbid commercial use and make models public.

**Sketchfab status (verify before you rely on it):** Epic **closed the Sketchfab Store/marketplace in 2025** (no more sales). **But** free/public uploading, the 3D viewer, glTF/USDZ conversion, and **embeds still work** and remain free — so it's still a valid *free host for an embed URL*, just no longer a store. For clean **single-object product embeds**, **Reflct** (<https://reflct.app>) is purpose-built: you set predefined viewpoints + orbit limits and get a website-ready 3DGS embed.

---

## Track D — DIY / open-source Gaussian splatting (full control, free, the reel's exact joystick)

This is the track that gives you the reel's **custom joystick viewer + branded, trackable, per-address link**, at **$0 in software**.

**1. Capture:** slow, steady phone video walking each room (or a full multi-ring orbit of an object). Even lighting, heavy overlap, no motion blur.

**2. Train the splat** — pick by hardware:
- **Jawset Postshot** (easiest; **Windows + NVIDIA**; point it at the video, it does frame-extraction + alignment) — free tier — <https://www.jawset.com>
- **Nerfstudio `splatfacto`** (most flexible; NVIDIA; `ns-process-data` runs COLMAP for you) — <https://docs.nerf.studio>
- **Brush** (Mac / AMD / no-CUDA / even in-browser) — <https://github.com/ArthurBrussee/brush>

Output: a `.ply` splat.

**3. Clean it:** open the `.ply` in **SuperSplat** (free, in-browser) — crop the outside world, delete floaters, optionally author a camera path. <https://superspl.at/editor>

**4. Compress for mobile (do not skip — see the size section):** convert the `.ply` to **`.sog` / SOGS** (Self-Organizing / Spatially-Ordered Gaussians) with **SplatTransform** (PlayCanvas, open source). SOG is the current best mobile-delivery format — **~15–20× smaller** than PLY (a 1 GB / 4 M-splat scene → **~55 MB**), GPU-ready, streams on load. This is what makes it usable over cellular; `.ksplat`/`.spz` are older fallbacks.

**5. Publish (get the link) — two options:**
- **No-code, fastest:** **SuperSplat → File ▸ Publish** → public `superspl.at/scene/<hash>` URL + iframe embed (set "unlisted" if needed). **Its viewer now has a built-in Walk Mode** (WASD/FPS + click-to-walk) — so you already get a first-person walk without writing code, just not an on-screen thumb-joystick or your own domain by default.
- **The reel's exact joystick + branded, trackable, per-address URL:** self-host a walk-mode viewer on your own domain (next section).

- **Cost:** free software; you pay only hosting (GitHub Pages / Netlify / Vercel = free) + dev time.
- **Gotchas:** COLMAP pose alignment is the usual failure point; Postshot is Windows-only; splats smear on glass/mirrors/blank walls; **raw `.ply` is heavy → always ship `.sog`** and test on a real mid-range phone over cellular.

---

## Reproducing the joystick (the headline feature — here's how, concretely)

Three ways, cheapest first. **Options 1–2 need no custom code.**

### Option 1 — PlayCanvas **SuperSplat Viewer** (free, MIT, self-hostable) — *the cheapest joystick path*
The open-source **supersplat-viewer** (<https://github.com/playcanvas/supersplat-viewer>, on npm as `@playcanvas/supersplat-viewer`) has a **built-in Walk Mode**: **WASD/FPS controls on desktop**, **click/tap-to-walk** (camera glides where you tap) on mobile, plus streamed LOD. Export it straight from the SuperSplat Editor, or `npm i` it, and **self-host the static build on your own domain** (Netlify/Vercel/GitHub Pages). This alone reproduces the reel's first-person walk **without writing a viewer from scratch** — Track D's earlier framing that custom dev is the "only" $0 joystick path was wrong; this is the shortcut.

### Option 2 — Luma's viewer WASD walk
Luma's interactive-scene viewer already supports **keyboard/WASD walking**. If you captured with Luma, that's a near-zero-effort partial match (desktop keyboard, not a mobile thumb-stick).

### Option 3 — Custom Three.js viewer + **nipplejs** (full control: on-screen thumb-joystick, your UI, your domain)
Use **mkkellogg/GaussianSplats3D** (<https://github.com/mkkellogg/GaussianSplats3D>) or **Spark** (Three.js, <https://sparkjs.dev>) to render the splat, and **nipplejs** (<https://github.com/yoannmoinet/nipplejs>) for the on-screen mobile joystick. The core is: **map the joystick vector to camera translation in the camera's facing plane, then pin the camera to eye height** so viewers can't fly through the ceiling or sink through the floor:

```js
import nipplejs from 'nipplejs';
// three.js scene + GaussianSplats3D viewer already set up; `camera` is your THREE.PerspectiveCamera
const EYE_HEIGHT = 1.6;          // metres — pin camera to standing eye level
const SPEED = 2.0;               // metres / second
const move = { x: 0, y: 0 };     // joystick output, -1..1

const stick = nipplejs.create({
  zone: document.getElementById('joystick'),  // a fixed-position div, bottom-left
  mode: 'static', position: { left: '80px', bottom: '80px' }, size: 110,
});
stick.on('move', (_, d) => {           // d.vector.y = forward/back, d.vector.x = strafe
  move.x = d.vector.x; move.y = d.vector.y;
});
stick.on('end', () => { move.x = 0; move.y = 0; });

const fwd = new THREE.Vector3(), right = new THREE.Vector3(), up = new THREE.Vector3(0,1,0);
function update(dt) {
  camera.getWorldDirection(fwd); fwd.y = 0; fwd.normalize();     // flatten so you walk, not fly
  right.crossVectors(fwd, up).normalize();
  camera.position.addScaledVector(fwd,   move.y * SPEED * dt);
  camera.position.addScaledVector(right, move.x * SPEED * dt);
  camera.position.y = EYE_HEIGHT;        // gravity/eye-height clamp — no passing through floors
  // bounds clamp: keep inside the room's AABB so you can't walk into the void
  camera.position.x = THREE.MathUtils.clamp(camera.position.x, ROOM.minX, ROOM.maxX);
  camera.position.z = THREE.MathUtils.clamp(camera.position.z, ROOM.minZ, ROOM.maxZ);
}
// look-around: drag on the rest of the screen → yaw/pitch the camera (PointerLock or a second touch zone)
```

**The three things every real walkthrough needs that a raw "fly camera" lacks:**
- **Eye-height pin** (`camera.position.y = EYE_HEIGHT`) so you walk at ~1.6 m, not float.
- **Flattened forward vector** (`fwd.y = 0`) so pushing the stick walks along the floor instead of nose-diving.
- **Bounds / collision** — at minimum clamp to the room's bounding box; for real wall collision, raycast the stick direction against a cheap invisible collision mesh (export a low-poly mesh from your capture) and stop movement on hit. Without this, viewers phase through walls — the #1 thing that makes a DIY walk feel broken.

**Point the yaw at look-around, translation at the joystick.** A second (right-side) nipplejs stick or drag-to-look on the rest of the screen handles turning; the left stick handles walking — exactly the reel's control scheme.

---

## The "trackable, address-tied link" — concretely, not hand-waved

"Wrap it with your own analytics" needs a real recipe. Minimal $0–cheap path:

1. **Host the viewer** (SuperSplat Viewer build, or your Three.js app) on **Vercel or Netlify** (free tier) under **your own domain** — e.g. `tours.youragency.com`. This is the branded part the vendor share-links (`scaniverse.com/...`, `superspl.at/...`) never give you.
2. **Per-address route:** make each listing a path — `tours.youragency.com/123-main-st` — so the URL *is* the address. In Next.js this is a dynamic route; as static files it's one folder per listing.
3. **Per-recipient tracking:** append a unique slug per buyer — `/123-main-st?to=buyer-jane` or a signed token. Log the hit.
4. **Analytics:** drop in a lightweight, privacy-friendly script — **Plausible** (~$9/mo, or self-host free), **Umami** (open-source, free self-host), or **Vercel Web Analytics** (free tier). You now see views, unique visitors, referrer, and (with the slug) *which buyer* opened it and how often — the reel's "who viewed" claim.
5. **Gating / expiry (optional):** put the viewer behind a **signed, expiring URL** (a short-lived JWT/HMAC token in the query string, verified by a Vercel/Netlify edge function) or a simple password. That's the "secure, trackable" combination.

**Which tier of the buy-it platforms actually unlocks analytics** (so you don't over-promise): **Ricoh360** — included in Pro (~$45/mo). **CloudPano** — Pro Plus (~$33/mo) and up. **Matterport** — all plans incl. free (heatmaps/dwell time). **Kuula** — Business only. **Zillow 3D Home** — minimal. When the client just needs tracking without building anything, buy one of these; when they need a *branded* per-address URL, self-host (steps above).

---

## Sharing / hosting reality (the traps)

- **File size is the make-or-break.** Raw splat `.ply` files are **tens to hundreds of MB** (a detailed room can top **500 MB–1 GB**), which is unusable over cellular. **Always convert to `.sog`/SOGS** (SplatTransform) → **~15–20× smaller**; target **under ~50–80 MB** per scene for a mid-range phone on LTE. Test on a real phone, not desktop wifi.
- **CORS (silent-failure trap):** a self-hosted viewer fetching a `.sog`/`.ply`/`.glb` from a **different origin** (e.g. a CDN or S3 bucket) needs `Access-Control-Allow-Origin` headers on that asset, or the load **fails silently** with a blank canvas. Either serve the asset from the same origin as the viewer, or set the CORS header on your bucket/CDN.
- **Vendor domain vs. branded URL:** every free hosted share link (Scaniverse, Luma, SuperSplat Publish, Sketchfab) lives on **the vendor's domain** and carries their branding — it is **not** the reel's `youragency.com/123-main-st`. That branded, address-tied URL is exactly the differentiator, and it only comes from self-hosting.
- **Site-builder embeds fail on some hosts:** **Wix and Squarespace** frequently block third-party `<iframe>`/`<script>` embeds or their **CSP** strips them, so a splat/`<model-viewer>` embed can render blank. Use their official "embed/HTML" block, host the viewer yourself and iframe your own domain, or use a builder (Framer, plain HTML, Webflow with custom-code) that allows it.

### Single-object web embed the simplest way — Google `<model-viewer>`
For a GLB from Track C, the lowest-effort self-hosted embed is Google's web component — no build step, works in any HTML page:
```html
<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>
<model-viewer src="chair.glb" camera-controls auto-rotate ar
              alt="Product" style="width:100%;height:480px"></model-viewer>
```
Drag-to-orbit + AR out of the box. (Watch CORS if `chair.glb` is on another domain.)

---

## Comparison table

| Tool | Input | Output | Cost (2025–26) | Share link | Nav | Best for |
|---|---|---|---|---|---|---|
| **Scaniverse** <br><https://scaniverse.com> | Phone video/photos (on-device) | Splat; `.SPZ`/`.PLY`/`.USDZ`/mesh | **Free, unlimited** | Yes — vendor domain | Orbit | Fastest free capture→link (space + object) |
| **Luma AI** <br><https://lumalabs.ai/interactive-scenes> | Phone video (cloud) | Interactive scene; PLY; embed | Free (watermark, non-commercial); **commercial = Plus ~$30/mo** | Yes — link + iframe | Orbit + **WASD walk** | Easy embed; keyboard walk; *pivoting to video* |
| **RealityScan (Epic)** <br><https://www.realityscan.com> | Phone photos | Mesh/photogrammetry (GLB/OBJ) | **Free, commercial OK** | Via export/host | — | Free high-detail object meshes |
| **Polycam** <br><https://poly.cam> | Photos/LiDAR/video | Splat, mesh, floor plans; hosted page | Free (mesh); **splats+PLY = Basic ~$12.50/mo annual**; Pro to ~$27/mo | Yes — hosted page | Orbit | Real-estate rooms + object scans |
| **KIRI Engine** <br><https://www.kiriengine.app> | Photos/video/LiDAR | Mesh (free) / **3DGS = Pro** | Free mesh; **splat = Pro ~$17.99/mo** | Publish to Sketchfab | Orbit | Cheapest photogrammetry incl. shiny objects |
| **CloudPano** <br><https://www.cloudpano.com> | Phone / 360 cam | 360 tour | Free (3 tours); Pro ~$27; **Pro Plus ~$33 (analytics)**; Teams ~$199 | Yes + **analytics (Pro Plus)** | Hotspot | Real-estate tours w/ lead capture |
| **Ricoh360 Tours** <br><https://www.ricoh360.com/tours> | Phone / Theta 360 | 360 tour + AI staging | ~$45/mo (Pro; ~$39 annual) | Yes + **analytics incl.** | Hotspot | Real estate with built-in tracking |
| **Matterport** <br><https://matterport.com> | Phone / 360 / Pro cam | Digital twin + dollhouse | Free (1 space) → Pro ~$69 → ~$309; **+~$20/mo/space**; analytics all tiers | Yes + link + **analytics** | Guided waypoints | Whole-property guided walkthrough |
| **Splat Labs** <br><https://www.splatlabs.ai> | Phone video | Real-estate splat walk | Quote (commercial SaaS/per-scene) | Yes (branded) | **Joystick / free-roam** | Closest real-estate match to reel |
| **TRELLIS-2** <br><https://microsoft.github.io/TRELLIS.2/> | Text or 1 image | GLB/OBJ/PLY (+PBR) | **Free, MIT** | Via host/Sketchfab | Orbit | Best free AI single-object generator |
| **Tripo / Meshy / Rodin** | Text or 1 image | GLB/USDZ/FBX/OBJ | Free tiers; Pro ~$13.93–$30/mo | Via Sketchfab/model-viewer | Orbit | Commercial AI object generation |
| **SuperSplat + Viewer** <br><https://superspl.at/editor> | `.ply`/`.sog` | Cleaned splat; hosted scene; self-host viewer | **Free (MIT)** | Yes — one-click Publish **or self-host** | **Built-in Walk Mode (WASD/tap)** | The clean/publish/**walk** layer of DIY |
| **Reflct** <br><https://reflct.app> | `.ply` splat | Guided object embed | Free tier + paid | Website embed | Guided viewpoints | Clean single-object 3DGS on a site |

---

## Start here this weekend (real estate AND objects, $0)

1. **Today — one live 3D scene for $0.** Install **Scaniverse**, capture one **room** *and* one **object** in Splat mode, tap Share. Two live browser links = proof the whole thing works.
2. **Get the walk, still free.** Export the room's `.PLY`, open **SuperSplat**, clean it, convert to **`.sog`** for mobile, then either **Publish** (instant link, Walk Mode built in) or export the **SuperSplat Viewer** and drop it on **Netlify/Vercel under your own domain** — that's the reel's first-person walk on a branded URL, no custom code.
3. **Add the on-screen thumb-joystick + tracking** only if you need the exact reel UI: host the same `.sog` with **mkkellogg/GaussianSplats3D + nipplejs** (eye-height pin + bounds, code above), add **Plausible/Umami** and a per-recipient slug for the trackable, per-address link.
4. **For AI objects:** run **TRELLIS-2** (free) or **Tripo** — prompt or one image → `GLB` → embed with **`<model-viewer>`** or **Reflct**.
5. **When it becomes a paying real-estate workflow:** add **Ricoh360** (~$45/mo, analytics included) or **CloudPano Pro Plus** (~$33/mo) for turnkey trackable, address-gated tours — the one thing free capture apps don't hand you — or **Splat Labs / Realsee** (get a quote) if the client demands the exact splat joystick walk without you building it.

**Total to be fully operational this weekend: $0** (Scaniverse + SuperSplat + SplatTransform/SOG + TRELLIS-2 + self-hosted walk viewer on free Vercel/Netlify). Add **~$9–45/mo** only when you need per-buyer analytics or a turnkey tour platform.