# v2 prototype: handoff (26 Sep 2026)

Read this first in a new session. It picks up the v2 redesign exactly where the
previous session stopped.

## Where things are

- **v2 prototype**: `prototypes/v2/` (hidden, noindex, never linked from live).
  Live URL: https://paraglidingatlas.com/prototypes/v2/
- **Live site is untouched** while v2 is built. Do not change live pages unless
  the owner asks.
- `prototypes/v3/` holds the abandoned direction experiments (A/B/C/D). The owner
  chose to stay with v2 and borrow D's booking pieces into it. Ignore v3.
- Branches: work on `claude/v2-prototype`; push to main with
  `git push origin HEAD:main` (allowed by `.claude/settings.local.json`) and also
  `git push -q origin HEAD:claude/v2-prototype`.

## Tools (all under `tools/`)

| Tool | What it does |
|---|---|
| `v2_localize.py` | Run after editing any v2 page: rewrites links to v2 twins or live files, adds noindex, v2.css, v2.js, v2-immersive.js, updates the page list in v2.js. |
| `v2_episode.py` | Builds a v2 episode page from the live `episodes/<slug>.html` plus `episode-meta.json`. `--samples` rebuilds the samples; or pass slugs. Then run `v2_localize.py`. |
| `v2_art.py` | Draws `prototypes/v2/img/contours.svg` and `ridge.svg`, writes the contour-tracer paths into `v2-immersive.js`. `python3 tools/v2_art.py icons` writes the panel icons into pages. |
| `v3_directions.py` | Generator for the abandoned v3 directions. |

Gates before every push: `./build.sh`, `python3 tools/audit.py --drift`
(0 FAIL), `python3 tools/smoke.py` (0 FAIL; a pinch test can flake, rerun once).
Preview: any static server at the repo root (the old one was
`python3 /tmp/claude-0/serve.py` on 127.0.0.1:8765; recreate if needed).

## Rules the owner set

- Nothing invented. Only facts the site already states or the owner gives.
  Missing facts show as a visible `[to supply]` mark.
- `rss-feed.js` is DO NOT MODIFY (styles only).
- Owner dislikes back-and-forth: do the work, verify with screenshots
  (desktop 1440 and phone 390, no horizontal overflow, no page errors), push,
  then report. Send a push notification when a long piece of work finishes.
- Keep text short; the owner feels the site has too much text.

## Done in v2 so far (highlights)

- Homepage: clear nav over brighter hero video; next date, group and price on
  India and Kenya; "Every departure" dates table; nav returns on scroll up
  (plain dark glass, no blue tint), not on trip pages.
- Site-wide: page darkens as it descends; contour backdrop behind text sections
  with random orange tracers moving with scroll; footer ridge horizon; image
  fade-in; instrument icons on panels; orange accent phrase in a few titles;
  outlined stat numerals; library stills in brand red; testimonial faces.
- Kenya/India trip pages: back as they were (no photo breaks), but keep the
  fade-in and the darkening background.
- Episode pages: redesign built by `tools/v2_episode.py` on three samples:
  Urs Haari (video), Damien Lacaze (audio), Zsolt Ero harness episode. Short
  title, guest portrait (only if a real portrait exists), player first, quote and
  guest card, chapter timeline (video), Fly with us panel, Up next (episode's own
  16:9 thumbnail). Owner has not yet approved rolling it out to all episodes.
- About: Mission Control removed; short story + timeline; "Meet the founder"
  (Aninder only; the owner asked to remove Gurpreet and Nikolay); facts row;
  "Discover the World From Above" now shows four tour tabs (India, Kenya, Peru,
  Kazakhstan) with dates and prices; book-a-call card.
- Facts supplied by the owner: Kenya US$2,100, 8 places; 136 countries.
- Enquiry form: `enquiry-worker.js` exists, but the owner will not pay for
  Workers, so the form stays mailto. A free alternative (Google Apps Script in
  their Workspace) was offered, not built.

## Open items / next steps

1. Owner to review the three v2 episode samples, then roll the design out to
   all episodes (`tools/v2_episode.py` over every slug, then fold it into
   `generate_chapter_deck.py` before switch-over).
2. Text trimming pass across the site (show before/after word counts).
3. Put 136 countries and the Kenya price on the LIVE site (offered, not yet
   approved).
4. Episode count: check the Spotify/Anchor feed (anchor.fm is blocked by the
   environment network policy; the owner must allow it, or give the number).
   Pages currently say 71, 86, 93 and 90+.
5. Peru and Kazakhstan details: owner will send later.
6. Guest portraits: only a few guests have one (`assets/podcast/guest-*.jpg`);
   more would improve episode heroes.
7. Switch-over of v2 to live only when the owner asks.
