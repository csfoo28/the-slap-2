# The Slap 2 — Slap Along

A mobile web mini game: watch the sketch and swing your phone like a slap when each slap lands.
Plain HTML/CSS/JS, no build step.

- `index.html` — the whole game (video, motion detection, scoring, slap-marking mode)
- `media/the-slap-2-360p.mp4` — the video (360p, ~2.6 MB, fully preloaded before play)
- `serve_https.py` — optional local server (`python serve_https.py` for HTTPS on the LAN with a self-signed cert in `certs/`, or `python serve_https.py 8090 --http` for local HTTP)

## Deploy

Static site — deploy the repo root as-is (e.g. Vercel with no framework preset and no build command).
Phone motion sensors only work over HTTPS, which Vercel provides.

## Slap timings

Set in `DEFAULT_CUES` near the top of the script in `index.html` (seconds into the video).
"Mark slap moments" in the game lets you re-time them and share via `?cues=...`.
