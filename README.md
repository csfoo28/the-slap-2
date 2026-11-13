# The Slap 2 — Slap Along

A mobile web mini game built around the comedy sketch *The Slap 2* (Adam Rozenbachs, *Open Slather*, 2015).
Watch the video and **swing your phone like a slap** every time a slap lands on screen.
Hit it on time and hard for big points.

Plain HTML/CSS/JS in a single page: no framework, no build step.

## How to play

1. Open the site on your phone (it has to be served over HTTPS for the motion sensor).
2. Tap **Enable motion & test swing**, allow motion access, and try a swing. Adjust **Sensitivity** if needed.
3. Wait for the video to finish loading, then tap **PLAY**. On iPhone, the first tap asks for motion permission and the second tap starts the game.
4. When the ring closes in on the hand, swing. **Skip intro** jumps ahead to just before the first slap.

> Grip your phone tight (or use a wrist strap) and keep clear of people and furniture.

## Features

- **Swing detection** from the phone's accelerometer and gyroscope, with adjustable sensitivity
- **Rhythm-style scoring:** Perfect / Great / Good / Miss by timing, bonus points for harder swings, combo multiplier, letter grade and personal best
- **Fullscreen landscape play:** if the phone is held upright, the game rotates itself sideways; on Android it also goes fullscreen and locks to landscape
- **Full video preload** with a progress bar (percentage, MB, speed, time left), so playback never stalls mid-game
- **Skip intro** button until 00:29
- **Slap sound effects, screen flash/shake and vibration** (vibration on Android only)
- **Mark slap moments** mode to re-time the slaps by tapping along, with a share link (`?cues=...`)
- **Desktop fallback:** press Space or click to slap

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole game: markup, styles and script, plus SEO meta tags, social cards, JSON-LD and the About/FAQ panel |
| `media/the-slap-2-720p.mp4` | The sketch video (720p, ~10 MB) |
| `og-image.jpg` | 1200×630 social share image |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `icon-*.png` | Browser, home-screen and app icons |
| `site.webmanifest` | Install-to-home-screen settings (fullscreen, landscape) |
| `robots.txt`, `sitemap.xml` | Crawler rules (search engines and AI crawlers allowed) and sitemap |
| `llms.txt` | Plain-text summary of the game for AI search and answer engines |

## SEO and AI search

- **Search engines:** descriptive title and meta description, canonical URL, `robots` meta, `sitemap.xml`
- **Social sharing:** Open Graph and X (Twitter) card tags with `og-image.jpg`
- **Structured data:** JSON-LD `VideoGame` / `WebApplication` and `FAQPage`
- **AI search (GEO):** an About / FAQ panel in the page's HTML (readable without running JavaScript), `llms.txt`, and `robots.txt` that explicitly allows GPTBot, ClaudeBot, PerplexityBot, Google-Extended and other AI crawlers

The site URL `https://the-slap-2.vercel.app/` is written into `index.html`, `robots.txt`, `sitemap.xml` and `llms.txt`. Update all four if the domain changes.

## Run locally

```bash
python -m http.server 8095
```

Open http://localhost:8095. On a computer, press Space or click to slap. To test the motion sensor on a phone, use the HTTPS deployment.

## Deploy

Deploy the repo root as a static site. On Vercel, set **Framework Preset** to **Other**, with no build command and the root as the output directory.
HTTPS is required for phone motion sensors; Vercel provides it.

## Customizing

Settings live near the top of the `<script>` in `index.html`:

- `DEFAULT_CUES`: seconds into the video where each slap lands (from MM:SS:frames timecodes at 25 fps)
- `INTRO_END`: where **Skip intro** jumps to (29.0 s)
- `WIN` / `PTS`: timing windows and points per rating
- `BASE_ACC` / `BASE_ROT`: how hard a swing must be at 1.0× sensitivity
