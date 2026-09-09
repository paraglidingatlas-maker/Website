# Paragliding Atlas Website — Project Handoff

Last updated: 2026-09-09 (end of first major build session)

This document exists so a new Claude conversation (or anyone else picking up
this project) can get full context quickly, without having to re-explain
everything from scratch. Read this first, then look at the actual files —
this repo is the single source of truth for what currently exists.

## Live links
- **Live site:** https://paraglidingatlas-maker.github.io/Website/
- **Repo:** https://github.com/paraglidingatlas-maker/Website
- Real domain (paraglidingatlas.com) is NOT yet connected to this — still on
  the default GitHub Pages URL.

## People
- Owner: Aninder Singh, aninder@paraglidingatlas.com
- WhatsApp: +4796757456

## Design system (locked — do not invent new colors/fonts)
```
--bg: #141519       (main dark background)
--card: #202127      (slightly lighter card/section background)
--orange: #ff7517    (the ONLY accent color — used sparingly, not everywhere)
--white: #f6f4f4
--gray: #737373
--gray-light: #b4b4b4
Fonts: Poppins (display/headlines) + DM Sans (body) only
No em-dashes anywhere in copy (was flagged early as an AI tell)
```
Visual language: dark HUD/dossier aesthetic — corner brackets (small L-shaped
orange accents on card corners), coordinate-stamp nav, skewed parallelogram
buttons (`transform:skewX(-10deg); transform-origin:left top` — the
`transform-origin:left top` part matters, see Lessons Learned below).

## File structure
```
index.html              Homepage
about.html              About Us
podcast.html            Podcast page (most iterated-on page by far)
knowledge-base.html     Knowledge Base PORTAL (just 5 category cards)
knowledge-base/         Category pages + sub-series pages (see below)
episodes/               Individual SEO episode pages (only 1 built so far)
styles.css              Shared global styles (nav, footer, buttons, etc.)
script.js               Shared global JS (scroll reveals, nav interactions)
globe.js                Homepage interactive episode globe (D3.js)
hero-canvas.js           WebGL particle hero background (Three.js) — pauses when off-screen
rss-feed.js             Podcast RSS live feed — ⚠️ CONFIRMED WORKING, see below
youtube-feed.js         YouTube channel live feed (featured + playlist UI)
episode-modal.js        Shared popup modal for Knowledge Base episode tiles
kinetic-type.js         Word-cascade animation for podcast pull-quote
cloudflare-worker.js    Dedicated CORS proxy Worker (deployed by user, see below)
generate_kb_pages.py    Script that generated the Knowledge Base sub-pages
generate_episode_pages.py  Script for individual episode pages (template + generator)
kb_yt_mapping.json      Episode title → real YouTube video ID mapping
youtube_video_ids.json  Full bulk export of channel's videos (85 entries)
```

## Knowledge Base structure (3-level hierarchy, NOT one long page)
```
knowledge-base.html (portal: 5 category cards)
  └─ knowledge-base/core-series.html
       ├─ navigators.html
       ├─ sky-gods.html
       └─ living-the-dream.html
  └─ knowledge-base/competitions.html
       ├─ world-cups.html
       ├─ risk-vs-reward.html
       └─ resources-tools-tips.html
  └─ knowledge-base/meteorology.html
       └─ weather-patterns.html
  └─ knowledge-base/industry.html
       ├─ brand-stories.html
       ├─ storytellers.html
       └─ the-dark-side.html
  └─ knowledge-base/technical.html
       ├─ flight-mechanics.html
       ├─ new-technologies.html
       └─ know-your-equipment.html
```
Episode tiles on sub-series pages open a popup modal (episode-modal.js) —
NOT a direct link out. The modal shows a video/thumbnail, description, and
a Read More button. Clicking play either embeds real YouTube video (if a
confirmed video ID exists), opens a real Spotify link (if one was found), or
falls back to the general show page (honest fallback, not a guess).

## Live feed infrastructure (podcast page)
Both the podcast RSS feed and the YouTube channel feed need a CORS proxy
since browsers can't fetch cross-origin XML directly. History:
1. Started with `allorigins.win` — free, no uptime SLA, started failing.
2. Switched to `corsproxy.io` — also free, also started failing at certain
   times of day (rate limiting on the shared free tier, confirmed via
   research — this is a known pattern with free shared proxies).
3. **Current solution:** a dedicated Cloudflare Worker the user deployed
   themselves (`https://restless-king-e534.aninder.workers.dev/`), running
   `cloudflare-worker.js`. This is NOT shared with other sites, so no more
   time-of-day rate limiting. Both `rss-feed.js` and `youtube-feed.js` point
   to this Worker now.

**`rss-feed.js` is marked as confirmed-working and isolated in its own file
on purpose** — it took several failed attempts to get right. Don't modify
it casually; if it needs changes, be deliberate.

## Lessons learned (avoid repeating these mistakes)
1. **GitHub Pages hosts project repos under a subfolder**, not the domain
   root. Absolute links like `/about.html` break — always use relative
   paths (`about.html`, `../about.html` from subfolders).
2. **`skewX()` transform-origin bug:** the horizontal component of
   `transform-origin` does NOT affect skew shear at all — only the vertical
   component does. To keep a skewed button's top-left corner flush with
   adjacent elements, use `transform-origin: left top`, not `left center`.
3. **`scroll-snap-type: mandatory` conflicts with continuous JS
   auto-scroll** — the browser fights the script trying to snap back,
   causing visible shaking. Don't combine them.
4. **A full page redesign was attempted once (podcast page) and reverted**
   — the user found it didn't match their vision despite "improving"
   consistency/typography. Lesson: make small, reviewable, one-thing-at-a-
   time changes rather than large restructures, especially after the
   design direction has already been approved once.
5. **Lenis smooth-scroll was tried and removed** — caused uneven scroll
   feel (possibly WebGL hero competing for frame budget, possibly the
   easing curve) that couldn't be fixed blind after two attempts. Removed
   rather than keep guessing. The WebGL pause-when-offscreen fix from that
   attempt was kept since it's a good optimization on its own.
6. **Kinetic typography:** give each major headline its OWN distinct
   animation treatment, not the same one repeated everywhere — that was
   explicit feedback. Hero = mask/wipe reveal on load. Pull-quote = word
   cascade on scroll. "Fly Better" = scale-in overshoot bounce on scroll.
7. **I have no way to take real screenshots** — tried Puppeteer (blocked,
   can't download Chrome), tried installing Chromium via apt (needs snapd,
   unavailable), tried the old wkhtmltoimage tool (renders but has real
   layout bugs with modern CSS). For before/after comparisons, the reliable
   method is publishing both versions live and having the user compare in
   their own browser.
8. **Background color alternation:** sections should alternate `--bg` and
   `--card`, using smooth full-height gradients (not flat-color-then-
   sudden-fade) to avoid hard visible bands, especially on mobile where
   sections are shorter.

## Known pending items
- **Safety Information & Disclosure Statements section is MISSING.** It
  existed on the original single-page Knowledge Base draft but was dropped
  when the page was restructured into the portal → category → sub-series
  hierarchy. Needs to be re-added somewhere (probably the portal page).
- **7 episode tiles still lack a specific real link** (fall back to the
  general show page): Anatomy of a Dream, Demystifying Parakites, Legacy
  and Lifetimes, Mastering the Unknown, New Technologies 3, PWCA, Science
  Backed Pre Flight Rituals.
- **Individual SEO episode pages** (the `/episodes/` folder with
  transcripts, JSON-LD structured data, keywords) — only 1 of ~79 episodes
  has one built (Zsolt Ero's harness episode). Scaling this needs real
  transcripts, which requires a bulk export via Claude Code + yt-dlp (the
  workflow was set up once for a different purpose but transcript data was
  never actually delivered back).
- **Destination pages** (Kenya/Himalayas/Peru/Kazakhstan individual pages)
  don't exist — only homepage teaser sections.
- **Real trip facts** (duration, group size, season) on homepage
  destinations are still placeholder text.
- **Host photo** on podcast page uses a real photo now (fixed), but About
  Us page still has no founder photo.
- Icons used throughout Knowledge Base cards are Claude's own
  interpretation of appropriate icons per topic — NOT a pixel-perfect
  match to the original Canva source icons (those were too small/blurry to
  read precisely when checked).

## Workflow notes
- The user tests almost everything by checking the live GitHub Pages site
  directly in their own browser — NOT by reviewing in-chat previews. This
  is genuinely more efficient (zero token cost, and in-chat previews can't
  even test real multi-page navigation properly). Default to editing +
  committing + pushing directly without building an in-chat preview first,
  unless there's a specific reason to sanity-check something before it
  goes live (e.g. presenting multiple design options to choose between).
- "Nothing changed" after a push is very often a browser/CDN caching issue,
  not a code bug — verify the code is actually correct in the pushed commit
  first before assuming something is broken, then suggest a hard refresh.
- The user has a Cloudflare account and has successfully deployed a Worker
  before (see live feed infrastructure above) — comfortable with basic
  copy-paste deployment steps when given clear instructions.
