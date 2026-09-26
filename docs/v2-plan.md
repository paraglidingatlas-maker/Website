# v2: the plan to finish (26 Sep 2026, overnight run)

The owner asked for every remaining step to be done without their input
while they sleep: freeze the design rules, finish every page type, the quality
pass, and the switch-over preparation. The content pass (text trim, supplying
facts) is out, by the owner's word. This file is the list, the checks, and the
schedule; `docs/v2-report.md` is what was actually done.

## Ground rules (unchanged)

- Nothing invented. Only what the site already says. Missing facts stay
  `[to supply]`.
- The live site is not changed. v2 lives in `prototypes/v2/`, noindex, never
  linked from live. `rss-feed.js` is not modified.
- **The switch-over itself is prepared, not performed.** Replacing the live
  site is the one step that can hurt search visibility and cannot be quietly
  undone once search engines have re-crawled; it waits for the owner's go.
- Every push: `./build.sh`, `python3 tools/audit.py --drift` (0 FAIL),
  `python3 tools/smoke.py` (0 FAIL; the pinch test can flake, rerun once),
  plus the new `python3 tools/v2_check.py` (0 FAIL). Push to `main` and
  `claude/v2-prototype`.

## The tasks, in order

### 0. Baseline
- 0.1 Preview server, Python deps (fonttools, brotli, pillow, playwright 1.56
  for the pre-installed Chromium).
- 0.2 All gates green before starting; note the page and check counts.

### 1. The checker first (`tools/v2_check.py`)
Written before the pages, so each new page is checked as it lands. For every
v2 page, headless Chromium at 390, 768 and 1440 wide:
- **Breakage:** uncaught page errors; console errors from our own files;
  sideways overflow; local links, images, scripts and styles that 404 on the
  preview server; images that fail to load (external stills excepted, the
  sandbox blocks YouTube).
- **Structure:** exactly one `<h1>`; no skipped heading levels inside `main`;
  every `<img>` has an `alt`; buttons and links have an accessible name; the
  page has `lang`.
- **Robots:** `noindex` present (v2 must never be indexed while it is a
  prototype).
- **SEO/GEO parity with the live twin** (the page that will be replaced):
  same `<title>`, meta description, canonical, `og:title`,
  `og:description`, `og:image`, `twitter:card`, the same JSON-LD `@type`s
  (and, for episodes, the same PodcastEpisode name, date and duration), the
  same `<h1>` text, and no less body text and no fewer transcript chapters
  than live (answer engines and search read the words, so v2 must not hide
  or lose any). A v2-only page (styleguide, fly-options) is exempt.
- **Tap targets:** interactive elements at least 40px in both directions on
  the phone width (report only; the kit uses 44px).
- Output: a table per page, a JSON file for the report, and screenshots at
  the three widths in the scratchpad for eyeballing.

### 2. Freeze the design rules (`docs/v2-design-rules.md`)
The tokens and patterns the pages already use, written down so new work is
checked against them: colour tokens, type scale, spacing, the two button
kinds, kicker / title / intro head, panel and card, photo grade and shade over
photos, motion rules (only on scroll or pointer, respect reduced motion),
phone rules (16px gutters, 44px targets, no sideways scroll). The styleguide
page gains the two new pieces: the fly-through and the episode hero.

### 3. Every page type in v2
- 3.1 **Episodes (94).** `tools/v2_episode.py`: the player-beside-title hero
  for every episode (the owner's decision; the portrait layout is dropped),
  guest card without a face. Build every slug. Edge cases to check: audio
  only, no artwork, no chapters, snippets and trailers, the AMA and the note
  of thanks (host only), two guests, very long titles.
- 3.2 **Knowledge base categories (18 more).** New `tools/v2_twin.py`: copy
  the live page, mark the body `data-v2="kb"` (the flight-mechanics sample's
  treatment), localize. `knowledge-base/index.html` is checked for what it is
  (redirect or page) and handled to match.
- 3.3 **Topic (tag) pages (49 more).** Same tool: the tag hero becomes the kit
  hero exactly as on `tags/safety.html`.
- 3.4 **Text pages (7):** mission, partners, corrections,
  safety-and-disclosure, cookie-policy, terms, participant-agreement. Same
  tool: the policy hero becomes the kit page hero exactly as on
  `privacy-policy.html`; partners' own hero checked by eye.
- 3.5 `v2_localize.py` over everything, so every internal link in v2 now
  reaches a v2 twin, and v2 becomes a whole, walkable site.
- 3.6 Styles: any page type whose live CSS clashes with the kit is fixed in
  `v2.css` under its `data-v2` marker, never in the live CSS.

### 4. Responsive and immersive pass
- 4.1 Screenshots of every page type at 390 / 768 / 1440 and a look at each.
  The tablet width has never been checked; do it now.
- 4.2 Known issues: the home "Because We Care to Share" panel squeezes its
  words on a phone; long episode titles; anything the checker's tap-target
  report finds.
- 4.3 The immersive layer (darkening scroll, contour backdrop, image
  fade-in, footer ridge) reaches every new page via `v2_localize.py`; verify
  it runs on each type and never on print or reduced motion.

### 5. Quality pass
- 5.1 **Speed:** oversized images (the audit names `himalayas-1.jpg`, 402 KB)
  get a leaner copy for v2 only; hero images keep `fetchpriority`, the rest
  stay lazy; videos stay `preload="none"`.
- 5.2 **Accessibility:** keyboard focus visible on the new pieces
  (fly-through buttons, board tabs, episode hero); contrast of small orange
  text on photos; the fly-through works with no script and with reduced
  motion.
- 5.3 **SEO/GEO:** the parity check at zero differences; the 14 episodes the
  audit flags for a PodcastEpisode without date or description are listed in
  the report with the fix to make at switch-over (they are live data).
- 5.4 **Debugging:** every FAIL and warning from the checker, the audit and the
  smoke run is fixed or explained in the report.

### 6. Switch-over, prepared (not performed)
- 6.1 `tools/v2_switch.py --dry-run`: builds the would-be live site into a
  staging folder in the scratchpad: v2 pages moved to their live paths,
  links and asset paths rewritten back, noindex removed, v2.css / v2.js
  loaded from their new place, the prototype-only pages left out.
- 6.2 The live audit and the v2 checker run against the staging copy:
  every live URL still exists, canonicals and JSON-LD unchanged, sitemap
  unchanged, no page lost.
- 6.3 A runbook in the report: what the one real run does, the order,
  how to roll back (one git revert), and what to watch in Search Console
  afterwards.

### 7. Wrap-up
- The report (`docs/v2-report.md`): what was done, numbers, what was checked,
  what is left and why, and anything that needs the owner.
- Handoff updated; everything pushed; push notification.

## What could be missed, and the check that catches it

| Risk | Check |
|---|---|
| A v2 page silently loses its title, description, canonical or schema | parity check in `v2_check.py` |
| A transcript or chapter list shorter in v2 than live | body-text and chapter counts in the parity check |
| A v2 page indexed by search engines | noindex check on every page |
| A link inside v2 lands on a 404 | local link check on the preview server |
| A page type looks fine at 390 and 1440 but breaks at tablet width | the 768 pass |
| Sideways scroll on a phone | overflow check at all three widths |
| A script error on one page type only | page-error check on every page |
| A generator change breaks the samples the owner already approved | rebuild the samples and compare screenshots |
| Live pages touched by accident | `git diff --stat` shows only `prototypes/`, `tools/`, `docs/` before each push |
| The switch-over drops a URL | staging copy compared with the live file list and sitemap |
| Something works headless but not on an iPhone | listed for the owner to check on a real phone (cannot be tested here) |

## Schedule (overnight)

| Step | Work | Push |
|---|---|---|
| 0-1 | baseline, checker | yes |
| 2 | design rules, styleguide | yes |
| 3.1 | all episodes | yes |
| 3.2-3.6 | knowledge base, topics, text pages, links | yes |
| 4 | responsive and immersive pass | yes |
| 5 | speed, access, SEO/GEO, debugging | yes |
| 6 | switch-over dry run and runbook | yes |
| 7 | report, handoff, notification | yes |

Check-ins are scheduled into this session in case the run is interrupted; on
each one the next unfinished step in this table is picked up.
