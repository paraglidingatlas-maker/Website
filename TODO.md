# Open items

Findings from the site health review on 14 September 2026. Ordered by what costs
most to leave alone. Anything fixed should be struck out or deleted here rather
than left to rot, or this file stops being trusted.

## Parked, revisit after 21 September

- [ ] **Google Search Console and Bing Webmaster Tools.** Add
      `paraglidingatlas.com` as a Domain property in Search Console, verify by
      TXT in Cloudflare, submit `https://paraglidingatlas.com/sitemap.xml`. Then
      Bing Webmaster Tools offers "Import from Google Search Console", which
      carries the property and verification across and skips doing the DNS step
      twice. Bing matters because ChatGPT search and Copilot run on its index.
      Note: a `google-site-verification` TXT record already exists on the domain,
      so a Search Console property may already be there. Check the property
      dropdown before adding a new one.
- [ ] **Cancel the old cPanel hosting.** Nothing serves the main site from it
      any more. Still pointing at it: blog, staging, mail, admin, cpanel, whm and
      webdisk subdomains. Open blog and staging first and confirm nothing there
      is wanted, and check no mail client is configured against
      mail.paraglidingatlas.com, since Google Workspace uses imap.gmail.com and
      smtp.gmail.com. Take a backup before cancelling.

## Blocked on Aninder

- [ ] **Real figures for Himalayas, Peru and Kazakhstan.** Duration, Group Size
      and Best Season, nine values across the three homepage fact blocks. They
      now read "Coming soon" instead of "Placeholder", which is honest rather
      than unfinished, but they are still not numbers. Skill Level is already set
      on all three and does not need anything.
- [ ] **Six Kenya site cards are text only.** Kerio Valley, Rift Valley NP,
      Kijabe Hill, Mount Longonot, Machakos Hills, Chyulu Hills. Photos exist but
      nobody has identified which frame is which site. Ask before assigning any.
- [ ] **No price anywhere on Kenya.** Says "Enquire for prices" twice. Deposit
      and Klarna were discussed and deferred.
- [ ] **India, Peru and Kazakhstan destination pages not built.** Old site copy
      is garbled; do not copy it without asking.
- [x] **library.html was never broken.** It opens on a landing screen by design:
      #eps is empty and hidden until you choose All or a series, and then it
      fills with all 86. Clicking a card opens the popup. Now covered by
      smoke.py so nobody rediscovers this as a bug.

## Process

- [x] **The audit never clicks anything.** Done: `python3 tools/smoke.py` drives a
      real browser over the rail popup, the phone menu, the audio player,
      sideways scroll at 390px and uncaught script errors. 14 checks. It was
      validated by putting the setPointerCapture bug back, which made it fail and
      exit 1, then taking it out again. It skips cleanly where Playwright is not
      installed.
- [x] **One command before pushing: `./check.sh`.** Runs build, then
      `audit.py --drift`, then `smoke.py`, stops at the first real failure and
      exits non-zero. Prints the warnings, and the real diff with the
      dateModified churn filtered out. Verified against three failure modes: a
      build failure stops everything, a JS syntax error fails at the audit, and a
      silently broken pinch passes the audit with 0 FAIL and fails at the smoke
      stage, which is the whole reason the smoke stage exists.
- [ ] **Widen smoke.py further.** 31 checks now, covering the rail, the phone
      menu, the audio player, the globe and its gestures, the library, the
      homepage search, the Kenya accordions, the enquiry form and sideways
      scroll. Still nothing on the podcast page, the knowledge base indexes, the
      tag pages or the episode transcript clipping. The rule that has worked:
      when something reaches Aninder that this missed, add a check for it.

## Content and SEO

- [x] **Dead link.** Was the globe popup's empty template state; globe.js sets a
      real href when a pin is clicked. The placeholder href is gone, so the
      keyboard cannot land on a link to nowhere while the popup is empty.
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
      and `assets/podcast/guest-urs-haari.jpg`. Not deleted: `atlas-favicon-source.png`
      reads like a source file worth keeping, and the guest-urs-haari pair may be
      waiting to be used. Needs a yes or no rather than a guess.
- [ ] **Two classes with no CSS rule and no JS reference:** `dst` on
      destinations/kenya.html, `enq` on enquire.html.
- [ ] `assets/images/himalayas-1.jpg` is 402KB, 2KB over the ceiling. Left alone
      on purpose: re-encoding at quality 80 came out at 417KB, so the file is
      already efficient at 1600x1200, and most visitors get the 374KB webp
      instead. Either widen the ceiling by a few KB or accept the warning.
- [ ] **404.html has 17px links.** Genuinely small tap targets, but it is a page
      nobody spends time on. Low priority.

## Also known

- [ ] **`generate_episode_pages.py` emits a stray duplicate**,
      `episodes/watch-this-before-you-buy-a-paragliding-harness.html`, alongside
      the committed `-a-talk` version. Running the generator otherwise changes
      nothing, so this is a slug mismatch rather than drift. The stray file is
      deleted rather than committed each time, which will keep happening until
      the slug is reconciled.

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
