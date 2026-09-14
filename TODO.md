# Open items

Findings from the site health review on 14 September 2026. Ordered by what costs
most to leave alone. Anything fixed should be struck out or deleted here rather
than left to rot, or this file stops being trusted.

## Blocked on Aninder

- [ ] **index.html says "Placeholder" nine times** in the Himalayas, Peru and
      Kazakhstan fact blocks. Needs real figures. Most damaging thing on the site:
      it is the homepage and every visitor sees it.
- [ ] **Six Kenya site cards are text only.** Kerio Valley, Rift Valley NP,
      Kijabe Hill, Mount Longonot, Machakos Hills, Chyulu Hills. Photos exist but
      nobody has identified which frame is which site. Ask before assigning any.
- [ ] **No price anywhere on Kenya.** Says "Enquire for prices" twice. Deposit
      and Klarna were discussed and deferred.
- [ ] **India, Peru and Kazakhstan destination pages not built.** Old site copy
      is garbled; do not copy it without asking.
- [ ] **Verify library.html renders its episode list in a real browser.** It
      renders nothing in the sandbox: all 86 episodes load into LIB_EPISODES and
      LIB_MODAL, no page errors, but no grid appears. Could be the blocked
      Cloudflare worker, except the fetch has a catch and the page is written to
      work without it. If it is blank on the live site, this is a whole page of
      the archive down and jumps to the top of this list.

## Process, highest leverage

- [ ] **The audit never clicks anything.** 104 checks, all of them reading files.
      That is why the rail popup bug survived since f2a5381 and needed a user to
      report it. A smoke test that opens the homepage, clicks a tile, asserts the
      popup opened, opens the phone menu, asserts four links are reachable, would
      have caught it the day it shipped. Roughly 40 lines with Playwright.

## Content and SEO

- [ ] **Dead link.** "Open the episode &rarr;" points at `href="#"`. Users click
      it and nothing happens.
- [ ] **Two episode pages have an empty description:**
      `can-we-steer-a-round-reserve-parachute-urs-haari-answers`,
      `touch-the-sky-with-glory`.
- [ ] **Two pairs of pages share a title:** the Oslo bird's eye view pair, and
      Touch The Sky With Glory.
- [ ] **Fourteen PodcastEpisode blocks missing a date or description**, including
      the SRS Piedrahita and BGD edition highlights.
- [ ] One description under 70 characters.

## Layout and housekeeping

- [ ] **Three content widths on wide screens.** 1300px is used 35 times, one page
      uses 1500, some pages have no cap at all and run to the gutters. Three
      different left edges. Standardising on 1300 is small and visible.
- [ ] **Kenya gutter** is `clamp(1.2rem,5vw,5.5rem)` where most pages use
      `clamp(1.5rem,5vw,4rem)`. Not only Kenya and enquire: the same value is in
      tags.css (145 pages), policies.css (7 pages), 404.html and the 404 template.
- [ ] **Footer column heads are h2 at 12px.** Nav groups marked up as page
      sections. The CSS already styles h2, h3 and h4 identically, so moving to h3
      changes nothing visually.
- [ ] **Eight unreferenced asset files**, including `assets/footer/mountains.png`
      and `assets/podcast/guest-urs-haari.jpg`.
- [ ] **Two classes with no CSS rule and no JS reference:** `dst` on
      destinations/kenya.html, `enq` on enquire.html.
- [ ] `assets/images/himalayas-1.jpg` is 402KB, 2KB over the ceiling.
- [ ] **404.html has 17px links.** Genuinely small tap targets, but it is a page
      nobody spends time on. Low priority.

## Known and deliberate, not bugs

- Every build rewrites `dateModified` on ~176 pages, because the date is read
  from git before the commit exists. Each catch-up itself touches those files, so
  it never settles. Every fix trades the churn for permanently stale dates, so it
  stays. Review diffs with `git diff -I'"dateModified"'`, which collapsed 177
  changed files to 1 real one.
- 11px of horizontal overflow at 320px viewport width, on index.html and
  about.html. Narrower than an iPhone SE. Left alone deliberately.
- library.html depends on a Cloudflare worker proxying the anchor.fm RSS feed for
  episode durations. The fetch has a catch and the page is meant to work without
  it.

## Verified healthy as of 14 September 2026

Checked 37 pages at 390px: zero horizontal overflow anywhere, exactly one h1 per
page, no images missing alt text, no page errors. 187 pages, 104 checks, 0 FAIL,
9 warn. Assets 6.8MB total.
