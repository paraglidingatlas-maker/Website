# v4: the owner's photographs, where they go and how (9 Oct 2026)

The owner, 9 Oct: a set of their own photographs (a Terabox share), to be
used on pages such as the knowledge base and the episodes, where the footage
was taken out on 8 Oct (commit 299d254, `docs/ux-report.md` "footage only on
the trips and the home page"). The pages "have to remain immersive".

**Status: waiting on the photos.** The environment's network policy blocks
`1024terabox.com` (403 at the proxy), and the owner's Google Drive (connected)
holds only three unrelated screenshots. Ways in: a Google Drive folder (read
through the connector), the repository (for example `incoming/photos/` on
`claude/v2-prototype`), or `1024terabox.com` added to the environment's
allowed domains (Terabox often needs a sign-in and serves files from other
hosts, so this may still fail).

Nothing below assumes what any photograph shows. Every photo is looked at
before it is placed: faces, and names on helmets, wings and harnesses (an
About frame was dropped for a helmet reading "ANDY", 4 Oct).

This plan came from three surveys of the repository (where photos could go;
the rules; the image pipeline), a planner, and a skeptic who measured the
pages and found fourteen problems in the first draft. The fixes are folded in.

## What the owner's message decides, and what it leaves open

- Decided (9 Oct): photographs on the knowledge base and episode pages. This
  amends the 8 Oct footage rule (`docs/v4-design-rules.md`, "Footage"), which
  sent those pages' immersion to drawings and animation; the rule and the
  moments table should record it when the first band is built. Still
  photographs only: no video returns to these pages, and no cloud climb.
- Open: the podcast. On 8 Oct the owner removed a photo backdrop behind the
  podcast's line together with its clip, and a still-only strip on Weather
  Patterns. A photo in either spot rebuilds what was just removed, minus the
  video. Both are listed below as "ask first".

## The slots, in order

One photograph band per page, never in a header, never on top of a page's
moment (the drawings on the knowledge base, the globe or the player on an
episode). The band carries no words, so no shade and no contrast risk. It
moves only with the scroll (the existing `v4-drift`, still under reduced
motion), and its photo waits until the reader comes near.

| # | Page | Where | Photos | Notes |
|---|---|---|---|---|
| 1 | Knowledge base: Flight Mechanics, Risk vs Reward | where the film strip was, between sections 01 and 02 | 2 | Flight Mechanics: section 01 is text only, a good spot. Risk vs Reward: section 01 ends with the hazard-ladder drawing, so the band moves one section later. |
| 2 | Knowledge base: the other 10 series pages | between two text-only sections, chosen page by page | 10 | On 8 of the 13 series pages a full-width drawing sits right before the obvious anchor; the band goes where at least one text-only section separates it from any drawing. The anchor table is measured at build time. |
| 3 | Episode pages | at the foot, just before "Up next" | 0 new | Each episode shows its series' photo (the same file as the series page, cached once). Not on the short film and highlight episodes (the Oslo and Norway films, World Cups and SRS highlights), where "Up next" is less than a screen below the player. |
| 4 | Knowledge base: the five level pages | after the questions, not before | 5 (optional) | Before the questions, Meteorology's band would load on arrival (28 KB headroom against its v2 twin). After them it waits. |
| ask first | Weather Patterns | where the still-only strip was | (1) | Removed by the owner on 8 Oct; a photo elsewhere on the page instead, unless the owner wants that spot back. |
| ask first | Podcast | behind the line "Intimate, deep and often thought provoking..." | (1) | This is the 8 Oct breather without its video. If wanted: a centred shade (the line is centred, 24 to 76% of the width), the photo waits, at most 180 KB. |

Totals: 13 photos for the knowledge base series (Weather Patterns' among
them, wherever it goes; the episodes reuse 12 of them), up to 5 for the
level pages, and 1 more if the podcast gets one. Five are enough to start (the four pages that lost a strip and one
more series page). Landscape files, at least 1600 px wide (ideally 2400),
with the subject across the middle (the band shows about a 3:1 slice on a
computer, a 4:5 cut on a phone).

What suits each page, if the set allows (never assumed): the wing from
below or overhead (Flight Mechanics), terrain close to the wing (Risk vs
Reward; nothing that reads as an incident), sky and cloud (Weather Patterns,
Meteorology, two different photos), a wide view with distance (Navigators),
gear on launch (Know Your Equipment), several wings sharing the air (World
Cups, without implying a competition), a heavy sky with no person in it (The
Dark Side). Otherwise any calm flying landscape.

Left as they are: every header and every page's moment, the trips (full of
photos already, the fly-through their moment), Enquire and the home Why band
(they carry forms), the library and topics, the knowledge base hub, text and
legal pages, and the stills behind the Mission and About headers.

## How a band is built

- Markup between its own marks, `<!-- v4-photo -->` and `<!-- /v4-photo -->`.
  Never the `v4-footage` marks or the `v4u-film`, `v4u-breather` or
  `v4u-ascent` marks: `tools/v4_footage.py` and `tools/v4_ux.py` delete those
  blocks on every build.
- Knowledge base: a full-width band, 52vh, capped at 640px, its top and
  bottom faded into the page with the knowledge base figures' own mask; plus
  `.v4-pband + .k-sec` so section 02 keeps its hairline. Never inside the
  drawings' slot (`.bf-media` blends with `lighten`, so a photo would come
  out ghosted) and never the unused `.band-img` rule (its caption is a box
  on the photo, against the rules).
- Episodes: the band breaks out of `main.cd-wrap` (1400px, padded) to full
  width, checked for overflow at 390, 768 and 1440.
- The photo waits: the 8 Oct waker (in 299d254^ `tools/v4_ux.py`, film
  stills) comes back under a new mark, and adds the blur-up classes itself
  (the blur-up scan skips images with no source yet). A `<noscript>` copy
  keeps it visible without script.
- CSS in a `/* @page photo */` section of `src/v4-ux.css`, loaded only on
  pages with a band. Design tokens only.
- Decorative: `alt=""`, `aria-hidden`, no caption, no place named, unless
  the owner says where and when each was taken and who is in it.

## From the owner's files to the site

A new v4-only tool, `tools/v4_photos.py`:

1. `--ingest <folder>`: originals stay outside the repository. Each file is
   opened, turned upright from its EXIF orientation, converted from its colour
   profile (Display P3, Adobe RGB) to sRGB, and saved with no EXIF, GPS, ICC
   or XMP. Under 1600 px wide is refused. HEIC cannot be read here (no
   pillow-heif): JPEG please, or convert first.
2. Desktop copies at 1200, 1800 and 2400 px (never enlarged), WebP and
   progressive JPEG, quality stepped down until each file meets its slot's
   budget; the tool fails rather than warns when one cannot. They land in
   `prototypes/v4/img/photo/<slot>-<hash>.webp|jpg`, the hash taken from the
   original, so a replaced photo gets a new address (the service worker
   serves images cache-first).
3. Phone cuts (4:5 for the bands, 2:3 for the podcast if wanted) with
   `tools/v4_phone_media.py`, given a 1400 px height cap and a byte budget.
4. A table filled in by hand once the photos have been seen: source file,
   slot, focus x and y, phone x.
5. Run order: `tools/v4_pass.py`'s generators (v2_episode --all, v2_twin,
   v4_pass), then v4_footage, v4_photos, v4_phone_media, v4_search, v4_ux,
   v4_min, and v2_localize last.

Checks before any push, besides the usual gates: a metadata scan of every
new image (0 EXIF, 0 GPS, 0 ICC, 0 XMP); `tools/v4_weight.py` and
`--phone` on every page that gets a band (no v4 page heavier on arrival than
its v2 twin; the episode template is already 1 KB over on one page, so
bytes come off elsewhere first or the owner grants an exception);
`python3 tools/ux_measure.py 6 --compare after`; layout shift under 0.05;
the wake position of each band at 1280x800, 1440x900, 1920x1080 and 390x844;
and `git status --short prototypes/v2` empty.

## Questions for the owner

1. The podcast's line and Weather Patterns' old strip: photos there (what
   was removed on 8 Oct, without the video), or elsewhere on those pages?
2. Episodes: reuse each series' photo (no extra photos), their own photos,
   or none?
3. The five knowledge base level pages: a photo each too?
4. Does any photo show a person other than you? If so, did they agree (the
   participant agreement's image-use box)? Any names on gear?
5. Decorative (no captions), or captions? Captions need where, when and who.
6. The site's landscape grade (a little more contrast, warmer), or as shot?
7. All taken by you, or does anyone need a credit?
8. Any from the India or Kenya trips with the place known? Those could serve
   the trip pages too.
