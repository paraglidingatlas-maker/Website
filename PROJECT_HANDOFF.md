# Paragliding Atlas Website — Project Handoff

Last updated: 2026-09-10 (mid-session handoff, second update)

This document exists so a new Claude conversation (or anyone else picking up
this project) can get full context quickly, without having to re-explain
everything from scratch. Read this first, then look at the actual files —
this repo is the single source of truth for what currently exists.

## ⚠️ CRITICAL: git push access does NOT carry over between chats
The previous chat's sandbox has a GitHub token embedded directly in its git
remote URL (`https://x-access-token:TOKEN@github.com/paraglidingatlas-maker/Website.git`).
This lives ONLY in that conversation's sandbox filesystem and is NOT
retained by Anthropic or carried into any new chat automatically — every
new conversation gets a completely fresh, empty sandbox. **The user must
provide a GitHub personal access token (repo write scope) again at the
start of this conversation before any push will work.** Cloning and reading
the repo needs no credentials since it's public — only pushing does.

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
index.html              Homepage (now includes a real episode search section)
about.html              About Us
podcast.html            Podcast page (most iterated-on page by far)
knowledge-base.html     Knowledge Base PORTAL (just 5 category cards)
knowledge-base/         Category pages + sub-series pages (see below)
episodes/               Individual SEO episode pages (only 1 built so far)
library.html            NEW: all-episodes archive, functional pass only —
                        real visual layout still needs to be designed (see
                        Known pending items)
styles.css              Shared global styles (nav, footer, buttons, etc.)
script.js               Shared global JS (scroll reveals, nav interactions)
globe.js                Homepage interactive episode globe (D3.js)
hero-canvas.js          WebGL particle hero background (Three.js) — pauses when off-screen
rss-feed.js             Podcast RSS live feed — ⚠️ CONFIRMED WORKING, see below
youtube-feed.js         YouTube channel live feed (featured + playlist UI)
episode-modal.js        Shared popup modal for Knowledge Base episode tiles
episode-search.js       NEW: homepage live episode search (filters as you type)
episode-search-data.js  NEW: 85 real episode titles + YouTube video IDs, powers
                        both the homepage search and library.html
kinetic-type.js         Word-cascade animation for podcast pull-quote
cloudflare-worker.js    Dedicated CORS proxy Worker (deployed by user, see below)
generate_kb_pages.py    Script that generated the Knowledge Base sub-pages
generate_episode_pages.py  Script for individual episode pages (template + generator)
kb_yt_mapping.json      Episode title → real YouTube video ID mapping
youtube_video_ids.json  Full bulk export of channel's videos (85 entries)
prototypes/episode-page-chapter-deck-FINAL.html  The AGREED final format for
                        individual episode pages ("Chapter Deck" — sticky
                        chapter rail + player + scrollspy). Generator not
                        built yet, see Known pending items.
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

## Homepage episode search + Library (NEW this session)
- A real, working search section sits between the "handpicked episodes"
  ticker and the interactive globe map. Searches all 85 real episode titles
  live as you type (episode-search.js + episode-search-data.js), each result
  links straight to the real YouTube video. Not a placeholder — genuinely
  functional.
- The word "Library" in that section's heading is clickable, styled with
  white text, small pulsating orange corner brackets on opposite corners
  (top-left/bottom-right), and 3 faint floating orange sparkle dots behind
  it — opens `library.html` in a new tab.
- `library.html` currently lists all 85 episodes with basic title A-Z/Z-A
  sorting. This is explicitly a **functional first pass only** — the user
  wants to design the real visual layout for this page as a separate next
  step. Don't over-invest in styling it further until that conversation
  happens.

## Real data available for episodes (investigated this session)
This came from directly fetching the live Spotify RSS feed
(`https://anchor.fm/s/ed1344d8/podcast/rss`) and checking it carefully:
- **Real per-episode metadata IS fully fetchable**: title, full show notes/
  description, guest links, publish date, duration, and a real per-episode
  thumbnail image URL — for all ~71 published Spotify episodes. Just
  web_fetch the RSS URL directly.
- **Real transcripts exist** — Spotify auto-generates them, and the RSS feed
  has a `<podcast:transcript url="...">` tag pointing to a real `.srt` file
  on Spotify's CDN for most (not all) episodes. Confirmed these files
  genuinely exist and are fetchable. BUT: web_fetch returns them as raw
  binary, not parsed text — extracting readable transcript text needs
  Claude Code (real curl/requests access) to download and parse them
  properly. This hasn't been done yet.
- **No chapters exist anywhere accessible.** The RSS feed declares the
  Podlove chapters namespace but never actually uses a `<psc:chapters>` or
  `<podcast:chapters>` tag on any episode — checked this thoroughly across
  ~20 episodes. Spotify's auto-chapters feature (the user confirmed it
  exists and generates chapters for every episode) appears to live only
  inside the Spotify app / Spotify for Podcasters creator dashboard UI and
  is NOT published through public RSS syndication. There is also no MCP
  connector that can reach it — the "Spotify" connector in the registry is
  for the consumer listening app (playlists, search, currently playing),
  not the Podcasters/Creator dashboard, so it's the wrong tool for this.
  **The only way to get chapters is for the user to manually check/export
  them from creators.spotify.com per episode.**
- 85 real YouTube video IDs + titles are already saved in
  `youtube_video_ids.json` / `episode-search-data.js` from an earlier bulk
  export the user ran via Claude Code + yt-dlp.

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

## Podcast page polish (this session — many small deliberate fixes)
After a full redesign attempt was tried and reverted (see Lessons Learned),
the approach shifted to small, targeted, one-thing-at-a-time fixes:
- Fixed real alignment/spacing bugs: "What You Can Expect" was the only
  content section using center-align (now left-aligned like the rest);
  pull-quote had different padding than every other section (now matches).
- Fixed abrupt background transitions: every section's gradient was
  flat-color-then-sudden-fade, causing hard visible bands especially on
  mobile. Converted all 10 gradients to smooth continuous transitions
  across each section's full height.
- Testimonials: removed the flat orange top bar, added a subtle background
  quote-mark decoration. Avatar initial badges were added then REMOVED per
  request. Auto-scroll was added then REMOVED — it conflicted with
  `scroll-snap-type: mandatory` and caused visible shaking (see Lessons
  Learned #3).
- Question form ("Got a Question For The Show?"): removed glassmorphism +
  rotating conic-gradient border (was the most decoratively "busy" thing on
  the page), replaced with the same flat corner-bracket card style used
  elsewhere. Inputs changed from plain boxes to the top/bottom-line style
  matching the newsletter input. Widened to match the testimonials
  container (was narrower, looked misaligned). Left border accent removed
  per request — now a fully flat card.
- Stat counter numbers switched from chunky Poppins bold to DM Sans with a
  subtle glow (chunky Poppins numerals looked "toy-like" at large size).
- Episode popup play button (episode-modal.js / styles.css) changed from a
  plain circle to an oval/ellipse shape with a soft shadow and inset
  highlight for more depth.

## Kinetic typography (each headline has ITS OWN distinct treatment —
explicit feedback was to never repeat the same animation everywhere)
- Hero headline: cinematic mask/wipe reveal on page load (CSS only).
- Pull-quote: word-by-word cascade reveal on scroll into view
  (kinetic-type.js, IntersectionObserver-based, deliberately simple after
  the Lenis experience).
- "Fly Better, Every Week": punchy scale-in with a slight overshoot bounce
  on scroll into view.

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
   design direction has already been approved once. This lesson was
   reinforced successfully this session — the follow-up round of podcast
   page fixes was done as many small isolated changes and went well.
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
9. **web_fetch can confirm a file exists but can't always parse it as
   text** — binary formats like `.srt` come back as raw binary. Confirming
   a URL is real is not the same as being able to extract its content;
   that distinction matters when telling the user what's actually usable.
10. **Don't assume a data field doesn't exist without checking the actual
    raw source carefully.** The chapters question required literally
    re-fetching the RSS XML and checking for the specific tag by name
    before giving a confident answer — first instinct guesses were nearly
    given as fact without verification.

## Known pending items
- **`library.html` needs its real visual layout designed** — explicitly
  deferred by the user to a separate conversation. Currently just a
  functional grid with basic sorting.
- **Chapter data for episodes** — doesn't exist anywhere accessible to
  Claude (see "Real data available" section above). User needs to manually
  pull it from the Spotify for Podcasters dashboard if they want it.
- **Real transcripts need extracting** — the `.srt` files are confirmed to
  exist and are fetchable, but need Claude Code (real curl access) to
  actually download and convert them to plain text. Not done yet.
- **The Chapter Deck episode page generator hasn't been built yet** — the
  format is agreed and saved (see file structure above), but no script
  exists yet to generate all ~79 real episode pages from it. This needs the
  transcript extraction above done first to be genuinely useful.
- **Safety Information & Disclosure Statements section is MISSING.** It
  existed on the original single-page Knowledge Base draft but was dropped
  when the page was restructured into the portal → category → sub-series
  hierarchy. Needs to be re-added somewhere (probably the portal page).
- **7 episode tiles still lack a specific real link** (fall back to the
  general show page): Anatomy of a Dream, Demystifying Parakites, Legacy
  and Lifetimes, Mastering the Unknown, New Technologies 3, PWCA, Science
  Backed Pre Flight Rituals.
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
- The user gives design feedback iteratively and often in small follow-up
  corrections (e.g. "keep the color white but add corner brackets instead",
  then "remove the underline, reduce spacing, add sparkles"). Expect to
  refine visual details across several quick back-and-forth turns rather
  than getting it exactly right in one shot — that's the normal working
  style here, not a sign something went wrong.


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
