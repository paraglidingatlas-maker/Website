# PARAGLIDING ATLAS — PROJECT HANDOFF

> **READ THIS PAGE FIRST, THEN THE TO DO LIST AT THE BOTTOM OF THIS FILE.**
> Everything else in this document is background you can read as it becomes
> relevant. Do not start work until the two setup steps below are done.

## Setup, before anything else

1. **Ask the user for a GitHub personal access token** if one was not supplied.
   Push access never carries over between chats. Fine-grained, Contents = read
   and write, scoped to the `Website` repo only. Then:
   `git remote set-url origin https://x-access-token:TOKEN@github.com/paraglidingatlas-maker/Website.git`
   Commit as `Atlas Site Build <build@paraglidingatlas.com>` to match history.

2. **Test network egress.** The user has already allowlisted `anchor.fm` and
   `transcript-files.spotifycdn.com` at claude.ai/settings/capabilities, but a
   sandbox only picks that up if it was created AFTER the change.
   `curl -sS -o /dev/null -w "%{http_code}\n" https://anchor.fm/s/ed1344d8/podcast/rss`
   200 means the RSS feed is reachable, which unlocks show notes and full
   episode titles. 403 means it is not; say so rather than working around it.

## How this project is verified. Do not skip this.

Three checks exist because three separate runtime bugs reached the live site
while narrower checks passed. Run them before every push that touches
`sitemap-graph.js`:
- `node --check` on the script (syntax only, catches very little).
- A static scan asserting nothing inside the translated node group uses absolute
  `n.x` / `n.y`. The group is already translated; absolute coordinates apply the
  offset twice and throw labels off screen.
- A headless render that stubs the DOM, actually runs `draw()`, and asserts it
  does not throw and that no `x` attribute inside a node exceeds 200.

**Verify the DEPLOYED page, not the pushed commit.** This sandbox can check the
repo and the Pages build; it cannot see what the user sees.
`GET /repos/paraglidingatlas-maker/Website/pages/builds/latest` must report
`status: built` with a matching commit sha. Then say "this should be fixed, tell
me what you see" rather than "this is fixed". Claiming otherwise cost real trust
in the previous session. If the user reports no change, suspect the browser
cache and tell them to add `?x=1` to the URL.

## The three rules that must not be broken

1. **Transcripts are clipped by CSS only.** The full text is always in the served
   HTML; the button toggles a `max-height`. Search engines run JavaScript, most
   AI crawlers do not. Turning this into a lazy fetch would silently destroy the
   site's visibility to answer engines. `display:none` is deliberately avoided.
2. **Never invent a URL, an ID, or content.** A fabricated YouTube id once
   shipped as a real episode's embed. Every id is validated against
   `youtube_video_ids.json`.
3. **Never summarise an episode from its title alone**, and never write FAQ
   content. Both produce plausible, subtly wrong text under a real person's name.

## Working style

The user tests on the live GitHub Pages site in their own browser. Edit, commit,
push. Build downloadable prototypes to `/mnt/user-data/outputs` for design
decisions rather than in-chat previews. Feedback comes as small iterative
corrections; that is normal. When an instruction could mean "adjust this" or
"replace this", ASK. Reading "make it top to bottom" as "replace the graph with
a list" cost two rounds and deleted working design.

---

# Paragliding Atlas Website — Project Handoff

Last updated: 2026-09-10 (third update)

**If you are a new chat, jump to "START HERE IF THIS IS A NEW CHAT" near the
bottom of this file first.** It covers the two setup steps needed before any
work can continue, and the current state of the library and episode pages.

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

## ⚠️ START HERE IF THIS IS A NEW CHAT (written 2026-09-10, third update)
Two things must happen before work continues:
1. **Ask the user for a fresh GitHub personal access token.** Push access never
   carries over. Fine-grained token, Contents = read and write, scoped to the
   `Website` repo only. Then set it as the remote:
   `git remote set-url origin https://x-access-token:TOKEN@github.com/paraglidingatlas-maker/Website.git`
   Commit as `Atlas Site Build <build@paraglidingatlas.com>` to match history.
2. **Verify network egress.** The user has already added
   `transcript-files.spotifycdn.com` and `anchor.fm` to the account-level
   allowlist at claude.ai/settings/capabilities (Code execution and file
   creation → Allow network egress → package managers plus specific domains).
   The previous chat's sandbox could not pick this up because its permissions
   were issued at session start, which is the ONLY reason this handoff exists.
   Test it immediately:
   `curl -sS -o /dev/null -w "%{http_code}\n" https://anchor.fm/s/ed1344d8/podcast/rss`
   200 means everything below is unblocked. 403 with `x-deny-reason:
   host_not_allowed` means it still has not propagated.

## Library page: REBUILT (this session, live)
`library.html` is no longer the A-to-Z functional pass. It is now a topic-first
page in a "stone portal" style, arrived at over five prototype rounds.

**Files:** `library.html` (markup and page CSS), `library.js` (behaviour, glyph
drawing, RSS enrichment), `library-data.js` (episode to series mapping).

**How it works:**
- Landing page shows the 13 Knowledge Base series as carved granite slabs, 3
  featured large and 10 smaller. No episode thumbnails on the landing page.
- Each slab is generated in the browser: two `feTurbulence` + `feDiffuseLighting`
  filters make the granite grain, and each series has its own embossed
  instrument glyph (compass rose for Navigators, balance beam for Risk vs
  Reward, iris for Storytellers, eclipse for The Dark Side, isobars for Weather
  Patterns, wing section for Flight Mechanics, carabiner for Know Your
  Equipment, and so on). No image files at all.
- Emboss = three stacked copies of each glyph: dark cut offset down-right,
  light catch offset up-left, stone face on top.
- Hover leaks orange light in from different edges per tile, cycling through
  four patterns (`edge-lb`, `edge-tr`, `edge-b`, `edge-l`) so the grid does not
  pulse in unison. Glyph warms to orange with a soft bloom.
- Click runs a portal: the slab grows to fill the viewport, a seam of light
  cracks across the middle, the two halves part like doors, and the episode
  grid rises behind. ~1.2s, skipped entirely under prefers-reduced-motion.
- Inside a series: filter pills (length, sort) plus a thumbnail grid.
- Routing is hash based (`#s=Risk%20vs%20Reward`, `#all`) so a series is
  linkable and survives refresh. **These should eventually become real pages**
  (`library/risk-vs-reward.html`) for search traffic; hash routes were the cheap
  way to test the idea.

**Data sourcing, deliberately robust:**
- Episode thumbnails come from YouTube (`i.ytimg.com/vi/ID/hqdefault.jpg`), so
  the grid never depends on the Cloudflare Worker being up.
- Durations are enriched at runtime from the podcast RSS through the existing
  Worker, matched to YouTube titles by normalised exact match then by word
  overlap at a 0.7 threshold. If that fetch fails the length filter simply does
  not render and the page still works.

**Placement provenance (important):** 61 of 79 episodes take the series they
already sit on in the Knowledge Base pages, read directly out of those pages'
`data-yt-id` attributes. Only the 18 that appear on NO Knowledge Base page were
newly assigned, each against that series' own stated description, and every one
is marked `// ** review` in `library-data.js`. Six items are excluded as
non-episodes (show trailer, "A Note of Thanks", four cinematic Oslo/Norway
reels), listed with reasons at the top of the file.

**Rejected prototypes, do not resurrect:** shelves/carousel rows; a light
background variant; and a version where the slabs protrude with a 3D edge,
cursor tilt and haptic vibration. The user explicitly chose the flat v4 stone
look over the protruding v5 one.

## Episode pages: AGREED APPROACH, not yet built
Format is `prototypes/episode-page-chapter-deck-FINAL.html` ("Chapter Deck":
sticky chapter rail, player, scrollspy, full transcript, FAQ, guest box,
resources, related episodes, tags). Note the ONE existing page,
`episodes/watch-this-before-you-buy-a-paragliding-harness.html`, uses the OLD
`ep-*` layout, not this format, and its transcript is a "coming soon"
placeholder. There is no real transcript text anywhere on the site yet.

**Chapters, decision made this session:** Spotify's auto-chapters are not in the
RSS feed and are not reachable by any tool. The user chose NOT to export them
manually. Instead: **derive chapter titles from the user's own show notes**
(most episode descriptions already contain their own bullet list of topics
covered, e.g. "We talk about:", "In This Episode You'll Learn:"), then find each
chapter's timestamp by matching those phrases against the transcript. The
chapter titles are therefore the user's words, not invented.

**Transcripts:** `<podcast:transcript>` tags in the RSS point at real `.srt`
files on `transcript-files.spotifycdn.com`, present for most but not all
episodes. With the allowlist now in place these can be curled and parsed
directly in the sandbox. Unknown until one is actually read: whether the `.srt`
carries speaker labels. The Chapter Deck design shows "Aninder:" / "Zsolt:" per
line, and subtitle files usually have no speaker attribution, so that part of
the design may need to change once the real data is seen.

**Still needs the user's input:** the FAQ block content, guest roles (the feed
has guest links but no structured role), whether related episodes are automatic
by series or hand picked, and whether the primary player is YouTube or Spotify.

## Lessons learned, added this session
11. **Do not make content decisions to make a page look finished.** The library
    was shipped with all 83 episodes assigned to series by guessing at titles,
    flagged only as "needs review" in a code comment. The user pushed back, and
    correctly: the design was agreed, the placement was not. Worse, 61 correct
    placements already existed in the Knowledge Base pages, so several guesses
    contradicted decisions the user had already made. **Before assigning,
    categorising or labelling the user's own content, look for where they have
    already done it, and ask when they have not.**
12. **Prototype in downloadable files, not in-chat previews.** Five rounds of
    library design were done as standalone HTML files written to outputs and
    opened in the user's own browser. This worked well and matches how they
    test everything else.
13. **The sandbox allowlist is fixed at session start.** Adding domains at
    claude.ai/settings/capabilities does not affect a conversation already in
    progress. A new chat is required.

## Episode pages: BUILT AND WORKING (fourth update, 2026-09-10)

### The transcripts
The user has 52 real transcripts in a Google Drive folder:
`https://drive.google.com/drive/folders/1Vx4cPOOJZZhAS47upZhx4UMtEMxuInxM`
They are PDF conversions of WebVTT files produced by Autotekst using Whisper V3.
**They carry real timestamps AND speaker diarisation tags** (`[SPEAKER_00]`,
`[SPEAKER_01]`), so the per-line timestamps and speaker attribution in the
Chapter Deck design both work with real data. This answers the open question
from the previous handoff.

**Getting them into the sandbox. Three routes, in order of preference:**
1. **Ask the user to upload a single ZIP of all 52 files.** A zip lands only on
   disk at `/mnt/user-data/uploads`, so nothing passes through the conversation.
   `unzip` and `pdftotext` are both present, and `pypdf` is installed. This works
   in any session with no settings change and is by far the cheapest route.
2. Allowlist `drive.google.com` and `googleusercontent.com` at
   claude.ai/settings/capabilities, set the folder to "anyone with the link",
   then curl each file id. Remember the allowlist only applies to a session
   started AFTER the change.
3. The Google Drive connector (`read_file_content`) works and needs no setup, but
   each transcript is 4,000 to 15,000 words, so pulling 52 through the
   conversation will blow the context many times over. Use it for one or two
   files only.

### The generator
`generate_chapter_deck.py` reads `transcripts/<slug>.vtt` plus `episode-meta.json`
and writes `episodes/<slug>.html`. Run `python3 generate_chapter_deck.py` for all,
or pass slugs to build a subset. It parses VTT, merges cues into paragraphs on
speaker change or a pause, and places chapters.

`episodes/episode.css` is lifted verbatim from the agreed prototype so the design
is single sourced. `episode-template.html` is the page shell. Nav, footer and
design tokens come from `../styles.css`.

**Chapters** come from the user's own show notes. Each chapter in
`episode-meta.json` carries a `cue`: a short phrase actually spoken in the
episode. The generator finds that phrase in the transcript by fuzzy word match
(0.7 threshold) and takes its real timestamp. A chapter can carry an explicit
`at` instead. Unplaceable cues print a warning and are skipped, so bad chapter
data fails loudly rather than silently inventing timings.

One page is built and live as a working reference:
`episodes/carabiner-fatigue.html`, from `transcripts/carabiner-fatigue.vtt`.
Its chapter titles and summary are marked `** review` in `episode-meta.json`
because that episode's show notes have no bullet list.

### Episode numbering (user's instruction, not yet implemented)
The "Episode 47" line in the design is currently blank. The user wants real
numbers: the show began around November 2023, so number episodes chronologically
from 1 by `pubDate` in the RSS feed, oldest first. Confirm the first episode's
actual pubDate from the feed rather than assuming, then write the number into
each `episode-meta.json` entry as `epno` (e.g. "Episode 12").

### Still open on episode pages
- **The FAQ block is deliberately unbuilt.** `.cd-faq` exists in the CSS and in
  the prototype. The user has something specific in mind for it and wants to
  handle it before the project wraps. Do not invent FAQ content.
- **Guest roles**: the line under the guest's name in the sidebar. The RSS has
  guest names and links but no job titles. Needs either a line per guest from the
  user, or extraction from how they are introduced in the transcript.
- **Related episodes**: proposal on the table is to fill automatically from the
  same series, overridable per episode in `episode-meta.json`. Awaiting a decision.
- The prototype's custom play button (`.cd-play`) is unused; the page embeds
  YouTube directly instead.

## Lesson learned, added this session
14. **Diff generated markup against the prototype's class list BEFORE pushing.**
    The first generated episode page was visibly broken: `.cd-line` is a two
    column grid whose first cell is a per-line timestamp, and the text cell must
    be a `<p>` because `.cd-line p` carries the font size. The generator put the
    speaker span in the timestamp cell, omitted that cell entirely on unlabelled
    paragraphs (collapsing text into a 64px column), used `h3` for chapter
    headings where only `.cd-block h2` is styled, and invented a `cd-box-title`
    class that nothing styles. All four would have been caught in seconds by
    comparing the classes used against the classes the CSS defines. That check is
    now part of the routine and comes back clean.

## Sitemap page (fifth update, 2026-09-10)
`sitemap.html`, linked in the nav next to Podcast on all 72 pages. Generated by
`generate_sitemap.py` from `library-data.js`, `episode-meta.json` and the
`knowledge-base/` folder, using `templates/sitemap-template.html` and
`sitemap-graph.js`. Nothing on it is hand written.

The page is a network graph and nothing else. The text index survives inside a
`<noscript>` block for crawlers. Decisions the user made, in order:
- Graph only. No section cards, no visible accordion.
- Opens as exactly the nav bar: Home, About Us, Knowledge Base, Podcast.
  Episode Library is depth 2 because it sits under Podcast.
- Collapsed branches trail faint hint lines, one per child up to five.
- Orange is down to three visible uses: the frame brackets, the hovered node's
  outline and label, and the "Open this page" link.
- Nodes are instrument glyphs, not circles: root is a ringed reticle with
  crosshair ticks, sections hexagons, categories diamonds, series chips,
  episodes small rotated squares, on a faint grid with a vignette.
- Clicking NEVER navigates. It opens or folds a branch and describes the node in
  the bar below, which offers the page as an explicit link.
- Three tiers of dimming: what just opened and its children at full strength,
  the path back to home at 46 percent, everything else at 17.
- **Layout is a left to right tidy tree**, not a force directed radial. Radial
  put generations on top of each other. Column per depth (215px), leaves take
  the next free row, parents centre on their children, 430ms eased transitions,
  new nodes slide out from their parent.
- Wheel zooms over the map like the globe on the home page, BUT releases the
  wheel at either zoom limit so the page scrolls on past instead of trapping the
  reader. Zoom anchors on the cursor. Buttons for minus, plus and reset.

### OPEN REQUEST, not yet built
The user wants this to feel like an award winning lateral scroll experience:
the columns should read as a horizontal journey rather than a static tree, using
the empty space on the left properly. Think Awwwards style horizontal scroll
where moving through the site structure feels like travelling across a canvas.
This is a design piece, not a bug fix. Ask what they want before building.

## Lessons learned, added this session
15. **Check the deployed page, not the pushed commit.** GitHub Pages had been
    failing silently for several commits because the repo had no `.nojekyll` and
    `episode-template.html` at the root contained `{{ }}` sequences that Jekyll
    parses as Liquid. A failed Pages build keeps serving the last good one, so
    `main` looked correct while the live site was frozen. Verify with
    `GET /repos/{owner}/{repo}/pages/builds/latest` and look for `status: built`
    plus a matching commit sha. Templates now live in `templates/`.
16. **Cache bust any script that changes.** The user twice saw an old version
    after a successful deploy because the browser held a stale
    `sitemap-graph.js`. The generator now appends a hash of the file's own
    contents to the src.
17. **Never invent a URL or an ID.** A YouTube id fabricated for a hand written
    "related episodes" link in the first prototype survived into generated
    metadata and shipped as a real episode's embed. Every id is now validated
    against `youtube_video_ids.json`.

## Sitemap: FINAL STATE and the 3D detour (sixth update, 2026-09-10)

### Where it landed
`sitemap.html` is the **2D left to right tidy tree**, restored from commit
`ea26925` after a long experiment with a 3D landscape was abandoned. Live and
building green. Files: `sitemap.html` (generated), `generate_sitemap.py`,
`templates/sitemap-template.html`, `sitemap-graph.js`.

What it does, all of it decided with the user over many rounds:
- Opens as exactly the nav bar: Home, About Us, Knowledge Base, Podcast.
  Episode Library is depth 2 because it sits under Podcast.
- Column per depth (215px), leaves take the next free row, parents centre on
  their children. Generations can never overlap, which a radial layout could not
  guarantee.
- Three tiers of dimming: what just opened and its children at full strength,
  the path back to home at 50 percent, everything else at 20.
- Camera pans at **constant zoom**, keeping the focused node a third in from the
  left. Zoom never changes by itself; that was what made it lurch.
- Collapsing retraces the route you actually took. Series have two parents (a KB
  category and the Library), so each node stores `via`, the parent that revealed
  it. Falling back to `parents[0]` sends people somewhere they have never been.
- Wheel zooms over the map but **releases at either zoom limit** so the page
  scrolls on past instead of trapping the reader. Buttons for minus, plus, reset.
- Clicking NEVER navigates. It opens or folds a branch and describes the node in
  the bar below, which offers the page as an explicit link.
- Nodes are instrument glyphs: root a ringed reticle with crosshair ticks,
  sections hexagons, categories diamonds, series chips, episodes small rotated
  squares, on a faint grid with a vignette.
- Orange only on the frame brackets, the hovered node and the "Open this page"
  link. Everything else greys.
- Collapsed branches trail faint hint lines, one per child up to five.
- The text index survives inside `<noscript>` for crawlers. Do not remove it.

### The 3D landscape, tried and rejected. DO NOT REBUILD WITHOUT ASKING.
Between `d9c050f` and `59d57a4` the map was a true ground plane projection: real
perspective, undulating terrain height field, horizon, parallaxing star field and
ridgeline, drifting dust, distance haze, depth of field blur, markers standing on
tethers above the ground, and a camera that flew between branches. It looked
genuinely good in the prototype (`formation-landscape-v2.html`) and the user
liked the look. It failed in use, and every fix surfaced another problem:
- `setPointerCapture` on the svg for dragging **stole the click** from markers,
  so nothing was clickable. A guard for exactly this existed in the 2D version
  and was lost in the rewrite.
- Drag converted cursor pixels through a world scale that stopped matching once
  the canvas cropped rather than fitted, so dragging drifted.
- The camera parked a fixed offset from the focused node, so wide branches ran
  off the frame. Fixed by framing the whole focused group, then it was too small.
- The canvas was a fixed 1180x660 letterboxed inside a much wider frame, leaving
  most of the screen dead.
- A hard horizontal seam appeared at the horizon once it was raised, because the
  sky gradient resolved lighter than the ground fill.
- Redrawing terrain polylines plus a Gaussian blur every animation frame was
  jerky; a coarse pass while moving helped but did not solve it.
The prototypes are worth keeping for reference:
`sitemap-visual-treatments.html` (four treatments: survey map, formation,
schematic, depth field) and `formation-landscape-v2.html`. The user chose
Formation, then asked for the landscape, then reverted to 2D.

### A misread worth not repeating
The user said "make this a top to bottom navigation". That meant **rotate the
travel direction**, not replace the graph with a list. It was read as the latter,
the whole visual was deleted and rebuilt as an indented accordion, which was the
thing deliberately removed several updates earlier. Two rounds were lost.
**When an instruction could mean "adjust" or "replace", ask.**

## Lessons learned, added this session
18. **Never remove a working visual to fix an interaction bug.** The clicks and
    drag were broken by the camera, not by the graph. Diagnose the actual
    component at fault.
19. **A prototype that feels good is not proof the interaction works.** The
    landscape prototype was convincing; the same design on the live page needed
    six rounds of fixes and still was not dependable. Prototype the interaction
    on the real page before committing to a direction.
20. **Keep the `<noscript>` index on the sitemap.** A canvas or a graph is
    invisible to search engines. That block is the only thing making 79 episodes
    and 13 series crawlable from this page.

## Sitemap: current state (seventh update, 2026-09-10) — DONE, do not redesign
2D left to right tree. Settled after a long detour through a 3D landscape that
was tried and rejected (see the previous update). Live, build green.

**Marker pack, chosen by the user from `blade-marker-variations.html`:**
- root and section -> `warden()`, hexagonal shield around a blade, in its two
  lighter treatments (the lighter one drops alternate walls of the shield)
- category, series, episode -> `interceptor()`, swept delta with a spine cut,
  in its three fuller treatments (outriggers, then nose spark, shed by level)
- Detail is fixed PER TIER, not by size, so a category always reads as a
  category. This was a deliberate change from the prototype.

**Spacing:** "Roomier". `COLW = 268`, `ROWH = 62`.

**Labels:** never shortened. `wrap()` breaks at `MAXCH = 44` on word boundaries,
splitting inside a word only when a single word exceeds the limit. Each line is a
`<tspan>`; the block is centred on its marker. Longest label needs three lines.

**Hit area:** a rect spanning the marker AND the whole wrapped label, so hovering
or clicking anywhere on the row works and lights marker plus text orange.

**Edges** start beyond the parent's label (`labelInfo().end + 10`), otherwise the
connector draws straight through the parent's own text.

### Nine titles are cut in the SOURCE DATA, not by the page
`youtube_video_ids.json` holds them already truncated at exactly 100 characters
ending in a literal "...", because that is YouTube's own title limit. Affected:
Sandrine Roy, Shane Tighe, Kinga Masztalerz, Ashutosh Chopra, Meteorology 101,
Eddie Colfox, Aljaž Valič, Alain Zoller, Helmut Schrempf.
**Fix:** `TITLE_FIX` at the top of `generate_sitemap.py` maps a truncated title to
the real one. It is empty with a worked example commented out. The full titles are
in the RSS feed, which has no such limit, so a session with `anchor.fm` reachable
can fill all nine automatically. That domain is already on the user's allowlist;
it only needs a session created after that change.

### Checks that now run before any sitemap push. KEEP THESE.
1. `node --check` on the script (syntax only, catches little).
2. **Static scan**: assert nothing inside the translated node group uses absolute
   `n.x` / `n.y`. The group is already translated, so absolute coordinates apply
   the offset twice and fling labels off screen.
3. **Headless render**: stub the DOM, actually run `draw()`, assert it does not
   throw and that no `x` attribute inside a node exceeds 200 (an absolute
   coordinate would).
These exist because three separate runtime bugs reached the live page while
narrower checks passed.

## Lessons learned, added this session
21. **Syntax checks prove almost nothing.** A missing helper, a lost guard and a
    wrong coordinate space all passed `node --check` and all broke the live page.
    Run the code, do not just parse it.
22. **`git checkout <old-sha> -- <files>` silently reverts unrelated fixes.** A 60
    character title cap that had already been removed came back this way and cut
    titles again. After any partial restore, re-check the fixes that file carried.
23. **Cache-bust the HTML, not only the scripts.** The graph data lives in
    `sitemap.html`; versioning `sitemap-graph.js` alone meant a fresh script
    rendering stale data. Appending `?x=1` to the page URL is the quickest way for
    the user to rule cache in or out.
24. **Say "this should be fixed, tell me what you see."** This sandbox can verify
    the repo and the Pages build status. It cannot see the rendered page. Claiming
    something is fixed on the strength of a repo check burned real trust here.

## Where the project actually stands
Done: library page, 46 episode pages from real transcripts, sitemap, nav link on
all 72 pages, Pages build fixed and green.
Open, roughly in order of value:
1. **`enquire.html` does not exist** but every page's nav CTA points at it, on all
   72 pages, and has since before this work started. A dead button site wide.
2. **The FAQ block** on episode pages is deliberately unbuilt. The user has a plan
   for it and wants it done before the project wraps.
3. **Six transcripts have no page** because those episodes are not in the YouTube
   export: Damien Lacaze, Gin Seok Song, Maxime Pinot, the parakites episode,
   Mastering the Unknown, the pre-flight rituals one. They need a series and a
   video id, or podcast-only handling.
4. **Guest roles**: 2 of 46 could be extracted from transcripts. Either the user
   supplies a line per guest or the field is dropped from the design.
5. **The nine titles** above. DONE, see the eighth update.
6. **Library and Knowledge Base still link episodes to YouTube**, not to the new
   episode pages. Pointing them at the local pages is a small change.
7. Thin series: Weather Patterns has 1 episode, Storytellers 2, Sky Gods 3.

# ============================================================
# TO DO LIST — carry this into every new chat, keep it updated
# ============================================================
# Mark items DONE rather than deleting them, so nothing gets redone.

## PENDING, in rough priority order

1. **enquire.html does not exist.** Every page's nav CTA points at it, on all
   ~90 pages, and has since before any of this work. A dead button site wide.
   Needs a real page written, not invented copy.

2. **Episode summaries. COMPLETE for every episode that has a transcript.
   71 of 86 written; the remaining 15 have no transcript and mostly should not
   have a summary at all.**
   Written across seven batches, all in one session. Every one came from the
   episode's OWN transcript, read directly, cross checked against the show notes
   in the feed. None from a title. Two sentences each, no em-dashes, and every
   entry carries `_summary_source`.
   **Why this mattered more than its size:** the summary populates the page's
   `<meta name="description">` as well as the visible `.cd-summary` block, and
   that description is what answer engines read when deciding whether an episode
   answers a question. The field was empty on all 86 pages before this session.

   **Method, reuse it if more transcripts arrive:** take the longest transcripts
   first, read each episode's own opening (roughly 200 to 400 words, where the
   host almost always states the topic outright) alongside the feed's show notes
   with the boilerplate links stripped, then write two sentences carrying at
   least one specific, checkable detail rather than generic praise. Ten per batch
   is comfortable. Verify afterwards that every page renders `.cd-summary`, has a
   populated meta description, keeps the transcript clip with no `display:none`,
   and uses no undefined classes.

   **The 15 without summaries, and what they are.** Do NOT write summaries for
   these from titles. 12 are not really episodes: 8 competition highlight reels
   (SRS Piedrahita, PWC Super Final tasks), and 4 Oslo and Norway cinematics.
   They have little or no speech and are fine as player-only pages.
   The other 3 could be summarised if a transcript ever appears: `ama-1`,
   `touch-the-sky-with-glory` and
   `can-we-steer-a-round-reserve-parachute-urs-haari-answers`. The first two are
   the last of the eight Spotify episodes with no RSS transcript tag; the third
   is YouTube only and has real content, so it is the one worth transcribing.

3. **Eric Roussel transcript. DONE (eighth update), by a route that was not on
   this list.** With `anchor.fm` reachable, the RSS turned out to carry a
   `podcast:transcript` `.srt` for this episode on Spotify's CDN. It was checked
   before use (1,374 English stopwords, zero French), so it is a transcript of
   the real English audio, not a back-translation. Converted to WebVTT, 1,197
   cues, 11,918 words, at `transcripts/brand-stories-neo-eric-roussel.vtt`. The
   French file is removed. Chapters left empty: this episode's show notes are
   prose with no topic list, so there was nothing to derive them from.
   **Two caveats recorded in `episode-meta.json` under `_transcript_source`:**
   Spotify transcripts carry NO speaker diarisation, so this page has no per
   line speaker attribution where the other 46 do; and machine transcription
   drifts on technical vocabulary (the opening line reads "with the choroid"
   where the word is almost certainly "shroud"). **Still open: the other 46
   pages carry an inline "[Automatic captions by Autotekst...]" note that comes
   from inside the Autotekst VTT itself. This page has no such note, so it
   currently reads as MORE authoritative than the pages that are actually
   better sourced. Decide where provenance should live: in the VTT, or emitted
   by the generator for every page.**
   **Speaker labels on this page are INFERRED, not diarised (ninth update).**
   The user asked for them and agreed the page must say so. Spotify supplies no
   diarisation, so `tools/infer_speakers_eric.py` anchors 58 turn boundaries to
   exact phrases where the speaker changes, read off the text of a two person
   interview, and splits cues at those points. A missing anchor is a hard error,
   never a silent mislabel. Result: 59 turns, 25 percent host and 75 percent
   guest by word count, and the transcript word count is unchanged at 11,919.
   The page's provenance note says the speakers were inferred and may be wrong.
   **If a real Autotekst transcript is ever produced for this episode it should
   replace all of this**, since that carries diarisation from the audio.
   **Standing instruction unchanged: scan any new batch of transcripts for
   language before publishing them.**

4. **Transcripts: 71 of 86 pages now have one, up from 46 (ninth update).**
   19 were pulled from Spotify's own `podcast:transcript` tags in the RSS feed,
   converted from SRT, and verified before writing: English by stopword count,
   plausible length, and for the three fuzzy title matches the pairing was
   confirmed against the globe's OWN existing slug mapping rather than trusted
   from a similarity score. None were skipped.
   **These 19 have no speaker labels** and their pages say so. Do not hand label
   them the way the Eric Roussel page was done; that was a one off the user
   asked for on a single episode and it took reading the whole transcript.
   **21 pages still have no transcript**, and the feed cannot fill them:
   - 8 match a feed episode that carries no `.srt` at all.
   - 13 have no feed match, so they are YouTube-only videos (tutorials, reels,
     the Oslo cinematics) rather than podcast episodes.
   The only routes left for those are Autotekst, or leaving them as player-only
   pages, which is a perfectly good outcome for a cinematic reel.

   **DO NOT retry the Spotify CDN trick on the missing ones. It was tested and it
   fails.** The transcript URL is
   `transcript-files.spotifycdn.com/{showID}/{publicEpisodeID}/transcript.srt`,
   the show ID is `16jBM3RfjVERukNHJrIRec`, and the episode segment is confirmed
   to be the public Spotify episode ID. Even so, an episode with no
   `podcast:transcript` tag in the RSS has NO public file: Robbie Whittall's real
   episode ID was tested against seven path variants with a known-good control
   alongside it, and every one returned 404 while the control returned 200.
   Spotify only writes a public copy when it also writes the RSS tag. The
   in-app transcript comes from an authenticated endpoint that is not reachable.
   This is the same wall as the auto-chapters.

   **Why syndication stopped is worth chasing with Spotify.** Every episode up to
   27 Apr 2026 published a transcript tag; nothing from 29 Jun 2026 onwards has.
   There is a two month publishing gap between those dates. If that is fixed at
   source it back-fills six episodes and every future one automatically.

   **The manual route works and is cheap, and has now cleared six of the eight.**
   The user downloaded them from the Spotify app and uploaded the .srt files.
   Done this way: Robbie Whittall, Russell Ogden, Metacognition, Brett Janaway's
   Technical Masterclass, Luc Armant, How to Thermal Like a Pro. Each was matched
   to its page by title overlap (five at 1.00, Russell Ogden at 0.83 because the
   feed title differs), then language checked and length checked before writing.
   Every one ends within seconds of the duration the feed states, so none are
   truncated: Luc Armant's really is a 20 minute episode.
   **Only two of the eight remain: AMA #1 and Touch The Sky With Glory**, both
   from the 2023 to 2024 era before Spotify transcription existed, so they may
   have nothing in the app either.

5. **Chapters. DONE for all 26 episodes that had a summary and a transcript but
   no chapters.** 259 chapters written, 27 of them the user's own words from
   show note topic lists, 232 written from the transcript and marked
   `src: "claude"` with `_chapters_source` explaining it. Every chapter records
   which it is, so provenance is visible in the data.
   **Placement method, this is the part that matters.** Matching a topic phrase
   against the transcript by keyword was tried first and FAILED: on the Robbie
   Whittall episode only one of eight show note topics placed with confidence,
   and the acro episode put "the hard truth on drugs and performance" onto a
   passage about reserve handles. That is why the generator had left these empty.
   `tools/chapter_candidates.py` instead extracts real boundaries from the
   transcript: the subject changes when the HOST speaks, so it takes host turns
   where speaker labels exist and question shaped cues where they do not. Every
   candidate carries the timestamp of the cue it came from, so a chapter cannot
   drift. Verified afterwards that no chapter timestamp falls past the end of its
   transcript and that no title is a fragment.

6. **FAQ block on episode pages.** `.cd-faq` exists in the CSS and the prototype
   but is deliberately unbuilt. The user has a specific plan for it and wants it
   done before the project wraps. DO NOT invent FAQ content.

7. **Guest roles.** Only 2 of 46 could be extracted from transcripts. Either the
   user supplies one line per guest, or the field is dropped from the design.

7. **Six podcast-only episodes have no page** because they are not in the
   YouTube export: Damien Lacaze, Gin Seok Song, Maxime Pinot, the parakites
   episode, Mastering the Unknown, the pre-flight rituals one. Nine globe pins
   also still point at the generic Spotify show link for the same reason.

8. **Thin series.** Weather Patterns has 1 episode, Storytellers 2, Sky Gods 3.
   Opening one of those on the sitemap or library feels empty.

9. **Site-wide chrome treatment.** Three full page mockups were produced:
   `full-page-treatment-comparison.html` (A rounded soft, B machined HUD,
   C flat HUD as live). The recommendation was B: the same tactile depth as A
   but expressed in the site's existing square-cornered bracket language, so the
   site does not end up with a fourth visual dialect. NOT YET APPLIED. Would be
   nav bar first, then buttons and pills, content surfaces left flat.

## NEW OPEN ITEMS (eighth update, 2026-09-10) — read these before picking work

A. **`library.html` has no content of its own for crawlers.** See PENDING item
   10 below for the full write up and the decision waiting on the user.

B. **`globe.js` pin labels are rewritten, not the user's titles.** See PENDING
   item 11 below. Ready to run, just needs a go ahead.

C. **Doc versus behaviour mismatch on the sitemap.** This file says twice that
   "clicking NEVER navigates", but `sitemap-graph.js` line 553 navigates on leaf
   nodes that carry a url (`window.location.href = n.url`, or `window.open` for
   external). Either the behaviour changed deliberately and the doc was not
   updated, or the guard was lost. Confirm which before touching it.

D. **Episode numbering (`epno`) is now unblocked and still empty.** The feed's
   oldest `pubDate` is confirmed as Wed 15 Nov 2023, so chronological numbering
   from 1 is computable. `published` / `published_label` are also empty on at
   least some entries and the feed has real dates for all 80.

## What the RSS feed actually gives you (verified, eighth update)
`curl https://anchor.fm/s/ed1344d8/podcast/rss` returned **200** in this session,
and `transcript-files.spotifycdn.com` is reachable too. Measured, not assumed:
- **80 episodes**, all 80 with non-empty show notes, a per-episode image and a
  duration. Oldest pubDate Wed 15 Nov 2023, newest Tue 08 Sep 2026.
- **63 carry a `<podcast:transcript>` `.srt`.** All six podcast-only episodes
  that have no page, and the Eric Roussel episode, are among them.
- **15 titles exceed YouTube's 100 character cap**, which is why the export cuts
  nine of them.
- **Spotify's `.srt` files carry real timestamps but NO speaker labels.** This
  answers the open question from an earlier handoff. The Chapter Deck design
  shows "Aninder:" / "Zsolt:" per line; transcripts sourced from Spotify cannot
  fill that field, only the Autotekst ones can.

10. **`library.html` serves no episode content to crawlers. DECISION NEEDED: A or
    B.** The page serves 614 characters of text and zero episode titles. There is
    no `<noscript>` block and every tile is injected by JavaScript, so a crawler
    that does not run scripts sees an empty page.
    **Do not overstate this.** The episodes are NOT undiscoverable: `sitemap.html`
    already lists all 79 episodes and 13 series in its own `<noscript>` index, so
    every episode page is reachable. The narrower and real problem is that the
    library page itself has no content, so it cannot rank or be cited despite
    being the main archive.
    Measured: 79 episodes across 13 series in `library-data.js`, and all 79 have
    a local episode page, so every row in an index can link internally.
    - **Option A, a `<noscript>` index.** Same pattern the sitemap already uses
      and that lesson 20 calls essential. Generated from `library-data.js` by a
      script writing between markers so it cannot drift. Zero visual change for
      anyone with JavaScript. **This is the recommendation.**
    - **Option B, render the tiles as real HTML** and let JS enhance them. Search
      engines weight real markup above `<noscript>`, but it is a restructure of a
      page that took five prototype rounds to settle and risks the stone slab
      rendering. Do not do this without the user asking for it by name.

11. **`globe.js` pin labels were rewritten by an earlier session and carry
    invented em-dashes.** Ready to run, needs only a go ahead.
    Measured, not assumed: 73 pins, **25 labels contain an em-dash, and ZERO of
    the 25 match the real episode title.** The user's own titles use `|` as the
    separator and the rewrite replaced it. The same rewrite altered the user's
    capitalisation ("If you fly in the Himalayas" became "If You Fly in the
    Himalayas") and misspelled a guest: the globe says "Dr Matt Wikes" where the
    real title says "Wilkes".
    **The user's rule on dashes, given this session: a dash is fine if it came
    from them or from source text that was picked up. A dash in anything newly
    written is not.** These are newly written, so they go.
    **Fix:** every pin already carries its episode page URL, so the real title
    can be read out of `episode-meta.json` by slug. No matching heuristic and no
    guessing. Three pins have no local page; two of those carry em-dashes and
    their real titles should come from the RSS feed instead.
    **Layout is not a risk here, this was checked:** labels go into a popup via
    `popupTitle.textContent`, and swapping to real titles moves the average label
    from 70 to 71 characters and the longest from 144 to 143.

## 12. CHAPTER TITLES: 18 OF 38 REWRITTEN, 20 STILL TO GO
45 episodes carry chapters, and 38 of them had titles cut off mid sentence,
generated from host questions and never rewritten. Examples of what was there:
"Look for when choosing a reserve?", "Community where even the top of the line
pilots are paying the…". They are the navigation rail on the site's longest
pages, so they read as broken rather than merely absent.

**The timestamps were already correct**, taken from real host questions, so only
the titles need work. `python3 tools/chapter_context.py <slug> [words]` prints
the transcript at each existing chapter mark, which turns rewriting a title into
reading about fifty words rather than re-choosing a boundary. Roughly six
episodes per batch is comfortable.

**Done (18):** Urs Haari, Gabriel Orsini, Andreas Lattner, Alain Zoller, Aljaz
Valic, Goran Dimiskovski, Beni Kalin, Will Gadd, Eddie Colfox (Storytime), The
Silent Mind, Christian Ciech, Helmut Schrempf, Godfrey Wenness, Pal Takats
(Colombia), Meteorology 101, Antoine Girard, Michael Nesler (RAST), Ziad Bassil.

**Still to do (20):** ashutosh-chopra, carabiner-fatigue-finsterwalder-charly,
what-is-civlresign-with-julien-garcia, flying-filming-1-benjamin-jordan,
flying-filming-2-benjamin-kellet, insights-from-the-gaggle-with-tilen-ceglar-stan,
living-the-dream-benjamin-jordan, navigating-india-eddie-colfox,
navigating-india-jigish-gohil, navigating-panchgani-vistasp-kharas,
new-technologies-2-guillem-batlle-adria-grau, new-technologies-5-frantisek-pavlousek,
new-technologies-4-veselin-ovcharov, pal-takats-on-challenges-change-the-future,
risk-vs-reward-3-manfred-ruhmer, risk-vs-reward-4-raul-rodriguez,
sandrine-roy-vol-biv, shane-tighes-road-to-x-alps,
the-resilience-equation-erlend-ukvitnes, understanding-skymate.
A one line check finds them: any chapter title ending in an ellipsis or starting
with a lower case letter.

## 13. SMALL REMAINING GLITCH IN THE LIBRARY SEARCH
The library search was badly broken and is fixed: the only box lived inside
#landing, which show() hides, and the handler cleared the value on every
keystroke, so a query could never exceed one character. There are now two boxes,
one per view, kept in sync. The user reports a SMALL remaining glitch, not yet
described. Get the specifics before changing anything.
**Note honestly:** that fix was verified by reading the code and by static checks,
NOT by execution. A headless harness was attempted and abandoned, because top
level `const` in separate `vm` scripts does not share a lexical scope the way two
script tags do in a browser, and stubbing around it grew past what the fix was
worth. If this is revisited, build the harness by concatenating library-data.js
and library.js into ONE script, which is what actually made the data visible.

## 14. POLICY PAGES ARE LIVE BUT NEED A LAWYER, AND TWO THINGS NEED THE USER
terms.html, privacy-policy.html and cookie-policy.html are built and linked from
the footer of all 113 pages. They are generated by `generate_policies.py`, so
edit the bodies in that file and re-run rather than editing the HTML.

**Sources.** The Drive Policies folder held a tailored Privacy Policy and Cookie
Policy, an EMPTY Terms document, Trek Travel's participant waiver as a reference,
and a 3.2 MB Policies.pdf that could NOT be read: Drive returns no text for it and
the content snippet is empty, so it is a scan with no text layer. If it matters,
it needs uploading to chat for OCR.

**The drafts described a website that does not exist.** They listed Klarna,
GoDaddy, Cookiebot, Google Analytics 4 and Leaflet Maps. The site uses none of
them. It is on GitHub Pages, has no analytics, no consent platform and no payment
processor, and NO code anywhere on it writes a cookie or uses browser storage.
Publishing those drafts unchanged would have described cookies that are never set.
The published versions were rewritten against what the code actually loads:
GitHub Pages, Google Fonts, YouTube in nocookie mode, cdnjs, unpkg, and the user's
own Cloudflare Worker RSS proxy.

**The Trek waiver was used for structure, NOT for its legal mechanism.** It is a
Wisconsin document in which the participant releases the operator from its own
negligence. That is void in Norway and across the EEA: liability for death or
personal injury caused by negligence cannot be excluded by agreement. The terms
therefore use assumption of inherent risk plus participant responsibilities,
which is enforceable, and say plainly that no negligence waiver is being sought.

**Commercial terms are now filled with defaults, and they are LIVE.** The user
asked for a decision rather than another question, so the terms now carry a 25
per cent deposit, balance at 60 days, and a 90/60/30 day cancellation scale.
That is the standard shape for small group adventure operators. It is binding on
new bookings from publication, so if the operator disagrees it must be changed
rather than merely noted.

**A fourth document was added: participant-agreement.html.** This is the
equivalent of the Trek waiver, rewritten for the EEA. It records risk
acknowledgement, pilot in command, licence and experience, equipment, insurance,
health and emergency contact, conduct and image consent. It is published rather
than kept private so a pilot reads it before booking instead of a week before
departure. Sections 3 to 6 and 8 carry italic "to complete" lines, because the
page doubles as the form.

**STILL NEEDS AN ANSWER: is this a package under the Package Travel Act?** If so,
Norwegian law requires insolvency protection, in practice Reisegarantifondet
registration, and the prescribed standard information form must be given before
booking. This is the only open item with a consequence for trading legally.

**LEGAL-REVIEW.md in the repo root is a brief for a lawyer.** It states what was
drafted, the five decisions already taken and why, and the six questions actually
worth paying for. It exists so a review costs one focused hour rather than
several exploratory ones. Hand it over with the four URLs.

**Also flagged:** Google Fonts loads from Google on every page, which transfers
the visitor IP to a US company. Self hosting the two font files removes that
entirely and is the cleanest GDPR improvement available on this site.

## 15. FONTS ARE SELF HOSTED NOW. DO NOT REINTRODUCE GOOGLE FONTS.
Poppins and DM Sans were loaded from fonts.googleapis.com on every page, which
sent every visitor's IP to Google before a word was read. The ten weights the
site uses are now in `assets/fonts/` (124 KB total, latin subset, woff2) and
declared in `fonts.css` at the root. Zero references to Google Fonts remain.
`fonts.css` lives at the root next to `assets/`, so its relative `url()` calls
resolve correctly from any page depth. Pages at depth link `../fonts.css`.
**Five generators and two templates also had the Google link and were patched.**
If a new page is added, link `fonts.css`, never the Google stylesheet.

**BOTH subsets are shipped, and that was a bug on the first attempt.** Google's
stylesheet served latin AND latin-ext, each with a `unicode-range`, so a browser
fetched latin-ext only on pages that needed it. The first self hosting pass
shipped latin only, which silently broke real guest names: Aljaz Valic, Frantisek
Pavlousek and Goran Dimiskovski carry carons and an acute that live in latin-ext,
and those letters would have dropped to a fallback face mid word. 23 occurrences
across the site. `fonts.css` now declares both subsets with the same
unicode-ranges Google used, so the behaviour matches the old setup and latin-ext
is still only downloaded when required. Total 204 KB for 20 files.
**If a weight is ever added, add BOTH the latin and the latin-ext file.**

**Four faces are preloaded on every page**: Poppins 600 and 700, DM Sans 400 and
500, latin only. Those draw the first screen. Do NOT preload more; extra
preloads compete for bandwidth with the fonts they are meant to accelerate.

**`fonts.css` also declares two matched fallback faces**, "Poppins Fallback" and
"DM Sans Fallback". They borrow a local system font and override its vertical
metrics to match the real ones exactly, 105/35/10 for Poppins and 99.2/31/0 for
DM Sans, computed from the font files rather than estimated. This means the line
boxes are the same height before and after the swap, so the page does not jump.
The stacks in `styles.css` are Poppins then Poppins Fallback then Arial.
`size-adjust` is deliberately NOT set: it needs the fallback's average character
width, and `xAvgCharWidth` is defined inconsistently between fonts, so any value
derived from it is a guess wearing the costume of precision.

## 16. enquire.html EXISTS. The site-wide dead CTA is gone.
It has no backend and no form service: submitting composes a message and hands it
to the visitor's own mail client, so nothing is posted anywhere and no processor
sits between a pilot and the inbox, which is exactly what the privacy policy
promises. If a real backend is ever wanted, that is a decision with a data
processing consequence and the privacy policy must be updated with it.
General and Contact Us in the footer now point here too.

**Path lesson worth keeping.** Patching footers across templates and generators
introduced THREE separate depth bugs in one pass: the episode template renders
into `episodes/` and needs `../`, the kb generator renders into `knowledge-base/`
and needs `../`, and the sitemap template renders to the ROOT and must not have
`../` at all. Each was caught only by auditing every relative href and src, not
just the .html ones. When touching shared chrome, always re-run that audit.

## 17. PERFORMANCE: WHAT WAS DONE, AND WHAT IS LEFT
**Images.** Every photo was resized to how it is actually used, allowing for a 2x
display, and re-encoded. WebP versions sit alongside the JPEGs and every photo
`<img>` is wrapped in a `<picture>` with a WebP `<source>`. The `<img>` is kept
untouched as the fallback, so existing CSS that targets `img` still applies and
nothing breaks without WebP support.
**The two biggest wins were site chrome, not photographs.** The logo was a 800px
wide 90 KB PNG, now 480px and 8 KB. The footer mountain graphic was 243 KB, now
31 KB. Both load on EVERY page, so that alone is about 294 KB off every single
page view. If either is ever re-exported, re-quantise it: `Image.quantize(256,
method=Image.FASTOCTREE)` for anything with alpha, MEDIANCUT fails on RGBA.
**Preconnects** were added per page, only to origins that page actually uses.
Do not make this a blanket list: each preconnect costs a connection and a
site-wide list would make pages slower.

**three.js is GONE. Do not reintroduce it for the hero.**
`hero-canvas.js` used exactly nine three.js symbols to draw a field of soft
glowing dots: WebGLRenderer, Scene, PerspectiveCamera, BufferGeometry,
BufferAttribute, Points, PointsMaterial, CanvasTexture and AdditiveBlending. The
library cost 654 KB, nearly all of it WebGLRenderer pulling in three's shader and
material system. A tree-shaken bundle of just those nine still came to 454 KB,
which is what made the decision obvious.
It is now plain 2D canvas with no dependency, and **every constant was carried
across unchanged**: 500 particles under 700px wide and 1200 above, a 24 x 14 x 16
box, rise speed 0.15 to 0.35 scaled by 0.008 a frame, wrap from y > 7 to -7, the
same white to ember gradient sprite, 0.55 opacity, a 55 degree field of view from
z = 12, and a 0.04 lerp toward a cursor target scaled by 1.4. Additive blending is
the `lighter` composite operation. The IntersectionObserver pause is kept, and it
matters: without it the loop competes with the page's scroll smoothing and makes
scrolling feel heavy further down.
The old WebGL version is in git history if the look ever needs comparing.
d3, topojson, gsap and ScrollTrigger are still needed, and are self hosted in
`assets/js/`. **The homepage now contacts no third party origin at all.**

## 18. THE STIEGLER / PAVLOUSEK MIX-UP IS RESOLVED, EXCEPT FOR ONE PAGE
The user uploaded the AirDesign transcript, which turned out to be byte-for-byte
the file already live on `new-technologies-5-frantisek-pavlousek`. The feed
settles it: New Technologies 3 : Stephan Stiegler (AirDesign Paragliders),
15 Aug 2024, duration 01:22:22, and that transcript runs to 01:22:11.

**What was done.** The real Frantisek transcript, which was sitting on the
duplicate `-2` page, now serves the Frantisek page. That page reads Franta five
times and Stefan zero. Its summary and chapters were replaced, since both had
been written against the wrong guest's words. The `-2` entry is deleted, its URL
is a noindex redirect stub rather than a 404, and the duplicate video_id is gone.
Stiegler's transcript is parked at
`transcripts/_unpublished/new-technologies-3-stephan-stiegler.vtt`.

**What is NOT done, and why.** Stephan Stiegler has no page. He has no YouTube
video, so the page would be podcast-only, and `templates/episode-template.html`
hardcodes YouTube in four places: og:image, the iframe, and the watch link. A
video-less episode would render a broken player. Building that path also unlocks
the five OTHER podcast-only episodes that currently have no page, so it is worth
doing properly rather than hacking one page.
**Being offline under his own name is better than being online under someone
else's, which is why it was done this way round.**

## 19. AUDIO-ONLY EPISODES ARE SUPPORTED. EIGHT NEW PAGES EXIST.
`templates/episode-template.html` hardcoded YouTube in four places, so an episode
without a video rendered an empty iframe. The player and og:image are now built
by `player_html()` in `generate_chapter_deck.py`. Video episodes are unchanged.
Episodes with no `video_id` get the artwork slot, a line saying it was never
filmed, and the listen buttons, styled by `.cd-player-audio` in episode.css.

Built on that: Stephan Stiegler, Damien Lacaze, Bryan Van Ostheim, Gin Seok Song,
Maxime Pinot, the pre flight rituals episode, Mastering the Unknown, and the Urs
Haari snippet. Seven had a transcript sitting in the RSS feed that nothing had
fetched. All eight are wired into library-data.js, episode-search-data.js and
globe.js, where **zero pins now use showUrl**.

**Artwork is a local placeholder on those eight.** Real episode art is on a
Spotify CDN unreachable from the sandbox, and linking it would add a third party
request to pages the rest of this work removed third parties from. If the user
supplies images, set `artwork` in episode-meta.

**Two generator bugs, same root cause: the assumption that every episode has a
YouTube id.** `generate_sitemap.py` required a non-empty `id` in library-data
rows and silently dropped rows without one, and keyed page lookup on video id.
Both now fall back to the page slug. If another id-keyed lookup is ever added,
give it the same fallback.

## 20. GUEST NAME EXTRACTION WAS TRIED AND MOSTLY ABANDONED. DO NOT RETRY NAIVELY.
`guest` is empty on most entries. Pulling the name from the episode title looks
easy and is not: matching capitalised words before a colon produced "Consequence
Over Probability" and "Understanding Skymate" as people, two wrong out of five,
even with a stop word list and a check that the surname appears in the
transcript. Those were reverted. Only names confirmed both by title pattern AND
by the surname being spoken were kept.
**The field needs the user, or a per-episode read. A 40 per cent error rate puts
invented people on pages under a real brand.**

## 21. AUDIT FINDINGS, AND THE RULE THAT CAUGHT THEM
A full re-audit after the session's changes found four real bugs. Three were
caused by the same mistake: **editing generated HTML directly instead of the
generator, then regenerating and wiping the edit.** It has now happened three
times, to sitemap.html, to the thin episode descriptions, and to all 17
knowledge-base pages, which silently lost their canonical, og tags and JSON-LD.
**If a page is produced by a generator, edit the generator.** Nothing else.

1. **Transcript content was being dropped.** `render_transcript` grouped
   paragraphs into chapters using the chapter times as boundaries, so anything
   starting before the FIRST chapter fell outside every bucket and never
   rendered. A first chapter at 00:04 silently deleted the opening seconds of
   the transcript on seven pages. The first boundary is now clamped to zero.
2. **The rail linked to blocks that were never emitted**, leaving dead `#c1`
   anchors. `chapters_with_content()` now filters the rail and the transcript
   with the same rule so they cannot disagree.
3. **A noindex redirect stub was listed in sitemap.xml**, which is a
   contradiction. `generate_robots_sitemap.py` now skips anything carrying
   noindex.
4. **Six Autotekst transcripts WITH speaker diarisation were sitting unused**
   under long auto-generated filenames that matched no slug, so every generator
   was blind to them. Weaker Spotify caption files had been fetched for the same
   episodes. The Autotekst files are now in place with speaker maps derived by
   finding the speaker who asks the most questions, verified independently by
   checking who says the welcome line.
   **If a transcript exists but a page shows none, check for a long filename
   before fetching a replacement.**

## 22. SECOND-PASS AUDIT: THE CATEGORIES THE FIRST ONE NEVER LOOKED AT
The first audit was structural. A second pass over the things it never checked
found six more real gaps, all now fixed.
- **`404.html` did not exist.** GitHub Pages serves it for a missing URL at ANY
  depth, so it uses ABSOLUTE `/Website/...` paths throughout. A relative path
  there resolves against the missing URL and breaks. Do not "tidy" them.
- **No `<link rel="alternate" type="application/rss+xml">` anywhere.** On a
  podcast site that is a genuine discovery gap; feed readers and crawlers look
  for it. Now on all 124 indexable pages.
- **No `apple-touch-icon` and no `theme-color`.** Both added; the touch icon is
  flattened onto the site background because iOS ignores transparency.
- **Placeholder text was doing the job of a label** on podcast.html. Placeholders
  are not reliably announced and vanish on typing. `aria-label` added.
- **38 pages skipped a heading level.** Footer columns were `h4` under an `h2`,
  knowledge-base series cards and episode sidebars were `h3` under an `h1`.
  Footer columns are now `h2`, series cards `h2`, episode sidebar sections `h2`.
  CSS selectors were widened rather than swapped, so old and new both style.
- **`knowledge-base/core-series.html` is NOT generated.** It is hand maintained
  and was missed by every generator patch this session. Check it by hand.

**Two checker flaws worth knowing, both of which produced false alarms:**
`grep -r --include=*.html . | grep -v prototypes` does NOT exclude prototypes,
because the filtered lines are bare URLs. And a link checker must resolve
`/Website/...` against the repo root, since the site is served from that path;
otherwise every absolute link on 404.html looks broken.

## 23. RUN `python3 tools/audit.py --drift` BEFORE EVERY PUSH. IT REPLACES THE
## MANUAL AUDITS.
Four hand-run audits each found a category the previous one had not thought of.
Relying on remembering to look was the actual bug. **80 checks now run from one
command**, and every one of them is a fault class that already bit this project.

`python3 tools/audit.py` report, `--quiet` failures only, `--drift` also verifies
generated files are in sync. Non-zero exit on any FAIL, so it can gate a push.

**`--drift` is the most valuable flag.** It regenerates everything and fails if a
generated file changes, which catches somebody editing generated HTML by hand.
That exact mistake silently reverted work THREE times in one session, including
all 17 knowledge-base pages losing their canonical and JSON-LD.

**When the audit reports something, suspect the audit first.** On its first deep
runs, five of the eight findings were faults in the checker, not the site:
a redirect stub legitimately canonicalises to its destination; title comparison
tripped over an emoji surrogate pair and over a bracketed suffix the generators
strip by design; the drift check flagged any uncommitted file including itself;
and `.left` and `.right` on podcast.html are JavaScript hooks with no CSS, which
is correct. **A check that cries wolf is worse than no check, because it teaches
people to skip it.** Fix the tool, never edit the data to silence it.

**The 11 remaining warnings are all known and mostly need the user**, so a clean
run means 0 FAIL and roughly 11 warn, not 0 warn:
FAQs/Passion/Mission Statement pages do not exist; two episodes have no honest
description source; the homepage still says Placeholder for trip facts; four
Oslo cinematics are unlinked; 67 episode titles are longer than a search result
shows; 13 YouTube-only videos have no publish date because they are not in the
podcast feed; one unused favicon source file; one 402 KB image.

## 24. THE DRIVE FOLDER THE USER POINTED AT HAD MOST OF WHAT WAS "MISSING"
Folder `1y9QWZa6gZ3SBOT20zqqFTxFWomnUtJ41` holds the Kenya tour's real FAQ,
Cancellation, Insurance, Requirements and packing list, Payment terms, and the
"A Flight of Human Genesis" marketing copy. A separate doc holds the Safety
Information and Disclosure Statements. **Check Drive before concluding content
does not exist.** Several items sat on the "needs the user" list for this whole
project while the answers were already written.

**A correction that matters.** The terms briefly carried INVENTED commercial
defaults: 25 per cent deposit, balance at 60 days, a 90/60/30 sliding refund
scale. The real policy is deposit with registration, **balance 120 days before
departure, and NO refunds at all**, including where the tour misses its flight
objectives and including pilots who leave early. Wrong, binding terms were live
for part of a day. Filling a commercial gap with a sensible-looking guess is not
a neutral act, and the lesson is to leave the gap visible instead.

**The legal tension is now question 1 in LEGAL-REVIEW.md.** A blanket no-refund
term sits badly against the Package Travel Act, which gives a right to terminate
against a *reasonable* fee and to terminate free of charge for unavoidable and
extraordinary circumstances. The page states the policy then says statutory
rights cannot be contracted away. Both are true and they are in visible tension,
which is a lawyer's question, not a writer's.

**Still not read: the `Unpublished` subfolder** inside that Drive folder.

**Nikolay Yotov's Africa field guide** is now the "On the Ground" section of the
Kenya page: local perceptions, how to approach people, pricing and tipping, being
asked for money, landing protocol, staying and moving, permissions, and the
ambassador point. It is attributed to him and cross linked to his episode, which
the page already carried, so the advice has a voice and a source rather than
floating as anonymous house wisdom.
**Two passages were deliberately rephrased rather than reproduced.** The source
says some warrior tribes refuse physical work; the page says that in some
communities men will not take portering work and that offering a guiding or
security role is the respectful move. The source says avoid talking to the wife
or daughter; the page says follow your host's lead on who it is appropriate to
address. Same practical guidance, without inviting a reader to generalise about
people.

## DONE (do not redo)
- **Nine truncated titles, recovered properly (eighth update).** They now live in
  `episode-titles.json`, verbatim from the RSS feed and **keyed by YouTube video
  ID**, and are applied to the sitemap, `library-data.js`,
  `episode-search-data.js` and `episode-meta.json`. The old `TITLE_FIX` map in
  `generate_sitemap.py` is gone: it only protected the sitemap, and keying on the
  exact truncated string meant one character of drift would silently restore the
  cut. `youtube_video_ids.json` is deliberately NOT rewritten; it is the raw
  export and the file every video ID is validated against.
  Side effect worth watching: `wrap()` breaks at 44 characters, so three sitemap
  labels now need FOUR lines where the longest previously needed three. At font
  size 11 that is about 51px against a `ROWH` of 62, so rows do not collide, but
  the deliberately roomier spacing is tighter for those three.
- **The three mandated sitemap checks are now real scripts**, run together by
  `./tools/check_sitemap.sh`. See lesson 25 for why two of them were worthless
  as originally written.
- Library page rebuilt (stone slab tiles, topic first).
- 86 episode pages, one for every video on the channel, transcript or not.
- Sitemap: 2D tree, Warden + Interceptor marker pack, Roomier spacing.
- Sitemap signal interaction: tail only, no head, node warms on arrival.
- Cross linking: every reference to a video anywhere on the site resolves to the
  same page. Library, Knowledge Base modal, related links, globe pins, sitemap.
- Nine titles truncated by YouTube's 100 character limit recovered in full from
  the globe's Spotify titles.
- GitHub Pages build fixed (.nojekyll) after failing silently for many commits.
- Transcript clipping, see below.

## Lessons learned, added this session
25. **A check that runs but exercises nothing is worse than no check, because it
    buys false confidence.** Both of the non-syntax sitemap checks were written
    out properly this session and both were initially useless. The static scan
    for absolute `n.x`/`n.y` flagged sixteen false positives when written as a
    whole-file grep, because edges, the camera and the layout all use absolute
    coordinates legitimately; it has to read only the block between the node
    group's `translate` and its `appendChild`. The headless render was worse: it
    stubbed the DOM, ran the script, passed, and had rendered nothing but the
    four collapsed nav nodes, because episode labels only draw when their branch
    is the focused one. It now renders three times, collapsed, fully expanded,
    and focused on the series holding the longest title, and it FAILS if the
    expanded pass produces too few node groups or no multi line label, so it
    cannot go quiet again.
26. **Check where a fix actually surfaces before calling it an SEO fix.** The
    nine truncated titles reached ZERO served HTML: episode pages already
    carried full titles and the sitemap `<noscript>` was already clean. The fix
    was still worth doing for correctness and to stop future generators
    reintroducing the cut, but it moved crawler visibility by nothing. The thing
    that would actually move it is item A above.
27. **A "recovered" value is not automatically the user's own.** The nine full
    titles already in `TITLE_FIX` had been quietly prettified at some earlier
    point: colons swapped for em-dashes, curly apostrophes straightened,
    capitalisation altered. Seven of those em-dashes had reached
    `episode-meta.json` and were being served in episode titles, h1s and JSON-LD,
    against a design rule stated at the top of this file. Always diff a
    "recovered" string against the authoritative source rather than trusting it.

## Transcript clipping: THE RULE THAT MUST NOT BE BROKEN
Episode transcripts are clipped to 620px with a fade and a "Continue reading"
button. **The full text is always in the served HTML.** The button only toggles
a `max-height`. This is deliberate and non-negotiable:
- Search engines render JavaScript. **Most AI crawlers do not** (GPTBot,
  ClaudeBot, PerplexityBot read the HTML they are served).
- If the transcript were fetched on click, those crawlers would see an empty
  page and the episodes would stop being answerable. That is the GEO risk and it
  is larger than the SEO one.
- `display:none` is deliberately avoided; a height clip is used instead.
- A `.no-js` class removes the clip entirely so text is never trapped.
If anyone later "optimises" this into a lazy-loaded fetch, it will silently
destroy the site's visibility to answer engines.
