# V2: the hidden prototype site. Brief for the session that builds it

Written 2026-09-25 by the session that did the Horizon work (PROJECT_HANDOFF.md
sections 67 to 81). Read PROJECT_HANDOFF.md from section 67 on as well; this brief
does not repeat it.

## What Aninder asked for, in his words and decisions

- The whole site lacks consistency: the homepage "feels off", About is "totally
  off", Podcast "not far behind", the episode library "completely off".
- Build **a complete new version of the site, hidden**, in one go, so he can review
  it thoroughly before anything changes on the live site.
- **He has said GO and does not want to be asked for approval again until the
  end.** Give short progress notes after each page (informational, never waiting
  for an answer). Only stop to ask if something would break the live site or
  remove existing content.
- Model: Opus at xhigh effort (his choice).

## Where it lives and how it stays hidden

- `prototypes/v2/` on main, URL `https://paraglidingatlas.com/prototypes/v2/`.
  The build tools already skip `prototypes/` (audit, IndexNow, nav injector,
  sitemap).
- Every v2 page: `<meta name="robots" content="noindex, nofollow">` AND
  `<link rel="canonical" href="https://paraglidingatlas.com/<live equivalent>">`.
- **Do NOT block v2 in robots.txt**: a crawler that cannot fetch the page cannot
  see its noindex, and the bare URL can then be listed.
- Never link to v2 from any live page, sitemap or IndexNow.
- v2 pages link to each other, so it can be clicked through like the real site.
- **All v2 styles in their own stylesheet** (`prototypes/v2/v2.css`, loaded after
  `../../styles.css`). The live site must not change while v2 is built.

## State you inherit

- Main is at `8000e06` (plus whatever the other session pushed since; see below).
- Branch `claude/wizardly-davinci-0khbe4` has one extra, unmerged commit
  `ff2fb1c` ("Draft, not live"): the kit appended to the end of `styles.css`
  (section "THE KIT", `.kit-*` classes, plus `.kit-card`/`.kit-panel` added to two
  Feedback `:where()` lists and `> .kit-hero.is-sky` added to the ambient sky
  selector) and a style guide at `prototypes/styleguide.html`.
  **Take the kit into `prototypes/v2/v2.css` and the style guide into
  `prototypes/v2/styleguide.html`; do not merge `styles.css` changes to main.**
  Get them with `git fetch origin claude/wizardly-davinci-0khbe4` and
  `git show ff2fb1c:styles.css` / `git show ff2fb1c:prototypes/styleguide.html`.

## Scope (in this order; a short note to Aninder after each)

| # | Page | What |
|---|---|---|
| 1 | Style guide | the kit, as the reference (draft exists, see above) |
| 2 | Homepage | rebuild as a three part story: Fly, Listen, Join |
| 3 | Podcast | rebuild; the globe moves here as a "map of stories" |
| 4 | Episode library | a real browser: search and series filters at the top, one card style, paging on screen (all 93 episodes stay as real links in the HTML for crawlers); stone tiles kept as the series entrance; episode popup kept |
| 5 | About | rebuild |
| 6 | Kenya, India | align to the kit; keep the hero slideshow, the pinned photo sequence, the booking bar |
| 7 | Episode page | 2 samples: a video episode (urs-haari-the-real-truth-about-reserve-parachutes-a) and an audio one (anatomy-of-a-dream-with-damien-lacaze) |
| 8 | Knowledge base | the door kept as is; 1 category page (flight-mechanics) on the kit |
| 9 | Topics | the index and 1 topic page (safety) |
| 10 | Enquire, one policy page, 404, sitemap | on the kit |

Generated pages (93 episodes, 50 topics, 20 KB categories) get samples only; at
switch-over the generators produce all of them in the new style.

### Homepage defaults (Aninder did not override them)
- Hero: the video (assets/video/hero-*), one line under the headline, two
  buttons ("Find your expedition", "Listen to the podcast"), stats inside the
  hero; no separate stats strip; no particles; nothing floating over the video.
- Part 1 Expeditions first: India and Kenya as big feature blocks (India may use
  the Bir Billing loop assets/video/bir-*; Aninder removed it from the current
  homepage card "for now", so keep India's homepage block a photo unless the
  whole v2 homepage clearly benefits, and say so in the notes), Peru and
  Kazakhstan as one compact "coming 2027, register interest" row
  (enquire.html?trip=peru / ?trip=kazakhstan), then the booking card.
- Part 2 Listen: one section: episode rail with the search built into its
  header. The globe goes to the podcast page.
- Part 3 Join: "why us" as three short proof points beside the newsletter.

## Rules

- **Structure is shared, character is not.** Keep the signature pieces as they
  are: knowledge base door, Kenya/India photo sequences, library stone tiles,
  booking card, globe, the episode pages' Horizon look, the video heroes,
  transcript sync, time of day sky, page transitions and feedback.
- The kit: one section header (kicker, title, intro), one spacing rhythm
  (`--sp-section`, `--gutter`, `--measure`), three hero types (media, sky,
  episode), four card types (lit panel, media card, list row, feature block),
  one solid button per group, 44px touch targets, no text under 11px, Horizon
  rules (light never cut, lines fade at their ends, panels lit not boxed).
- **Nothing invented.** Same words, same facts. Where text is shortened or moved,
  list it in the final notes. No placeholder figures.
- Keep for SEO at switch-over: URLs, titles, meta descriptions, H1 wording,
  structured data, internal links. Keep a per-page checklist.
- Every page checked at 390px and 1440px: no sideways scroll, no broken links,
  fast (the homepage used to block the main thread; do not regress: no always
  running animations off screen).
- Reduced motion: nothing moves. Save-Data / 2G / 3G: no video.

## Finish line

One message with: links to every v2 page, before/after screenshots, the SEO
checklist, text shortened or moved, content gaps needing Aninder (photos,
prices, dates, figures), and anything you chose that he should look at.
Then stop. Switching pages over is a separate, later step he will ask for.

## Working setup (container is fresh each session)

```
pip install brotli fonttools pillow imageio-ffmpeg --break-system-packages -q
pip install "playwright==1.56.0" --break-system-packages -q   # chromium at /opt/pw-browsers, do not run playwright install
ln -sf "$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')" /usr/local/bin/ffmpeg   # only if video work
```
- Gates, run separately with timeouts: `./build.sh`, `python3 tools/audit.py --drift`
  (if the only FAIL is drift on sitemap.xml, build once more), `python3 tools/smoke.py`
  (about 4 to 5 minutes). 0 FAIL required before any push to main.
- Preview server for screenshots: a threaded one (a single threaded server stalls
  on video). `python3 -m http.server` died repeatedly in background; a small
  `socketserver.ThreadingTCPServer` script run with run_in_background works.
- The playwright Chromium cannot play H.264 (MP4); WebM plays. YouTube and
  i.ytimg.com are blocked in the container: route them to stand-ins when testing.
- Commits: author `Atlas Site Build <build@paraglidingatlas.com>`. Push to main
  and to your session branch. **Another session edits main at the same time**
  (Partners page, email forms): fetch before every push; if main moved, rebase
  on it; conflicts are almost always only `?v=` hashes and `dateModified`
  (take either side), then rebuild and rerun the gates before pushing.
- Usage: when a usage window runs out, schedule your own resume with
  `send_later` (claude-code-remote MCP) and tell Aninder in one line when you
  will continue.

## Gotchas already paid for (details in PROJECT_HANDOFF.md 67 to 81)

- A mask on a scaled element scales with it; put fades on an unscaled frame.
- `overflow:hidden` makes a scroll container; view timelines then sit at 50%. Use `clip`.
- `display:contents` elements never intersect; observe the element itself.
- The audit reads tokens only from the main `:root` in styles.css.
- The audit's border check rejects raw `rgba(180,180,180,x)` / `rgba(255,117,23,x)` in borders; use tokens or `transparent`.
- `scrollbar-gutter:stable` on all pages made full bleed heroes 10px short; only while a popup locks the page.
- Speculation rules prerender the next page; the knowledge base is prefetch only.
