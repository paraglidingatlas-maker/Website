# v4 design rules (from the v2 rules, 26 Sep 2026)

v4 (`prototypes/v4/`) starts as a copy of v2 and its rules. The v2 file
(`docs/v2-design-rules.md`) stays as it was; every v4 change is written here.
The principle agreed with the owner: **consistent in the grammar, distinctive
in the moments.**

The rules the v2 pages already follow, written down so new work is checked
against them instead of judged by eye each time. The values live in
`styles.css` (`:root`) and `prototypes/v4/v2.css` (the kit); this file says
how to use them. The living examples are on `prototypes/v4/styleguide.html`.

## Words
- Short. The owner's rule: the site already has too much text. A section is a
  kicker, a title, at most one line of intro, then the thing itself.
- Nothing invented. Only what the site already says or the owner supplies.
  A missing fact shows as `[to supply]` (`.v2-tbd`), never a guess.
- Every heading keeps the words of the live page's heading (search reads
  them); layout may split it into lines, never drop words.

## Colour
| Token | Use |
|---|---|
| `--bg` #141519 | the page; every section sits on it |
| `--card` #202127 | a solid surface (form fields, chips) |
| `--orange` #ff7517 | one accent: kickers, prices, the primary button, a lit edge. Never large areas of text |
| `--orange-lite` #ff8a3d | orange on top of a photo, where plain orange is too dark |
| `--white` #f6f4f4 | titles and key values |
| `--gray-light` #b4b4b4 | running text |
| `--gray` #737373 | captions, labels, muted meta |
| `--line` / `--edge` / `--edge-hi` | hairlines: inside a card / a card's edge / a rule meant to be seen |
| `--live` / `--wash` | focus or hover border / orange hover fill |
| green #5fd08a | only for "Guaranteed to run" |

## Type
**Page titles (v4): three sizes, one weight (700).** `--fs-display` for a
hero over a photo or film (home, podcast, about, partners, trips);
`--fs-h1` for a hero on the sky (library, topics, text pages, the knowledge
base door); `--fs-title-s` for long titles (episodes, knowledge base
articles). An episode's on-screen title is its short part; the rest sits
under it, smaller, and every word stays in the `<h1>` (`tools/v4_pass.py`).

**The instrument font (v4):** DM Mono (`--font-mono`, OFL, self-hosted in
`prototypes/v4/fonts/`) only for what an instrument would print: the
readout, coordinates, timestamps and chapter times, durations, the trip
readouts, the stats rows. The outlined stat numerals stay.

Poppins (`--font-display`) for titles and numbers, DM Sans (`--font-body`)
for everything else. Sizes only from the scale: `--fs-micro` (kickers,
labels), `--fs-small` (meta, chips), `--fs-body-s` (card text), `--fs-body`,
`--fs-lead` (intros), `--fs-h4` (card titles), `--fs-h3`, `--fs-h2`
(section titles), `--fs-h1`, `--fs-display` (heroes). Kickers are uppercase,
600, letter-spacing .16em, orange. Stat numerals are outlined.

## Space and layout
- A section is a band: `.kit-band` (vertical `--sp-section`, sides
  `--gutter`), content in `.kit-in` (max `--measure`, 1300px).
- Head: `.kit-head` = `.kit-kicker` + `.kit-title` + optional `.kit-intro`,
  then the rule (a hairline with a short orange lead, drawn by the head
  itself) and, optionally, `.kit-note` on the right (a count, a link, a
  caption; under the title on a phone). One pattern for every section head.
- **Folded text (v4):** words the first read does not need go in a
  `<details>` (`.v4-fold`, or a panel that is a `<details>` whose title is the
  summary). Never loaded by a script, so search and answer engines read them.
- **No void before the footer:** the footer's ridge is the page's ending; the
  last band keeps a short gap.
- Gaps only from `--sp-1` to `--sp-5`.
- Grids: `.kit-grid` (auto-fill 17rem), `.is-2`, `.is-3`. Never three narrow
  columns on a tablet: two to a row between 561 and 1024px.

## Pieces
- **Buttons:** two kinds only. `.btn-solid` (orange, skewed, one per group)
  and `.btn-lines` (a hairline above and below). The listen buttons and the
  episode's listen links are these two as well (v4). A status (`.v2-status`)
  may sit after them. Buttons and fields take the page's type (the Arial fix).
- **Panel:** `.kit-panel`, lit from its top-left corner, words only.
- **Card:** `.kit-card`, a picture and words.
- **Soft surfaces, not boxes:** cards (episode tiles, topic and knowledge base
  cards, side boxes, Up next) have no outline and no inner rules: a faint fill
  lit from the top. The orange corner shows only under the pointer or keyboard
  focus. Chips and filters are soft fills; the chosen one is orange. Search
  boxes are a soft field with a line underneath.
- **Facts:** a row of label (micro, orange, uppercase) over value (white).
  Trips show next date, length, level, price; group size lives in the
  departures table. On a calmed trip page (India) the row is four big
  facts: the value large over a grey label in sentence case, a hairline over
  each (the record page's figures), no orange; the old row's other four
  (base, launch, guiding, season) sit under them on the same columns,
  quieter, and the trust strip keeps its four columns.
- **Words on a photo:** no box. A shade (gradient) behind them, darker on the
  side the words sit; small orange text on a photo gets `--orange-lite` and a
  tight dark text-shadow.
- **Fly-through** (home, `.v2-flyby`): one picture held on screen, each trip's
  details passing over it; the section heading is its first frame.
- **Episode page:** the player beside the title (every episode, owner's
  choice); quote and guest card in one row below; chapters, transcript,
  "Fly with us", "Up next". Host-only episodes say "Hosted by".

## One signature moment per page (v4)
Consistent in the grammar, distinctive in the moments. Each page has one
moment, and everything around it stays quiet (kit heads, soft surfaces,
short text). A second moment on the same page is a sign one should go.

| Page | Its moment |
|---|---|
| Home | the fly-through of the four trips |
| India, Kenya | the fly-through: five full screens, the photograph behind |
| India (less but better, 19 Oct 2026; the gallery, 20 Oct) | the fly-through stays the moment: the hero is one plate with the footage, the route a schematic flown with the same weighted glide; the gallery is the owner's pinned run again on a wide screen (his choice of 1 Oct; the blind judges missed it), kept quiet beside the fly-through: one photograph at a time at full brightness, a scroll-led dissolve and no zoom, one caption at a time; on a phone a column of clean full-width plates |
| Kenya (second half) | the route map stays (it is the route section's own piece) |
| Podcast | the globe (its footage breather taken out, owner, 8 Oct 2026; its line stands on the page) |
| Library | the flight log (every episode a line in the log, the library drawn as a log) |
| Episode | the opening globe turned to where the story is from (72 episodes); the others open on the player |
| Topic | the topic's log drawing and the newest three |
| Knowledge base | its own drawings (it stays different on purpose) |
| Partners | the flight line down the page |
| Record attempt | the course drawn to scale, pinned and flown kilometre by kilometre as the visitor scrolls, the clocks counting alongside (prototype-only until the owner's go, 17 Oct 2026) |
| Expeditions | the map flown with the scroll from the world to each trip, each place's own photograph rising out of the map (owner, 19 Oct 2026: its own page, not the home page's section again) |
| Text pages | none: they are for reading |

Shared, not moments: the altimeter on long pages (decoration), cards that
open into the episode (a transition), the instrument font.

## Motion
- Only in answer to the visitor: scroll, pointer, tap, key. Nothing loops or
  moves on its own except a looping flight video, and that only while on
  screen.
- **Footage (owner, 8 Oct 2026):** only on the trip pages and the home
  page, only footage the site has, playing only while on screen. No footage
  bands on the podcast or knowledge base pages; their immersion is to come
  from what the site makes itself (drawings, animation).
- Page darkens as it descends; images fade up from a blur; contour backdrop
  behind text sections. No tracers (removed at the owner's request).
- **Less but better (the record page, 19 Oct 2026):** the owner called the
  first record page's flat clouds, drawn hills, count-ups, ring cursor and
  word-by-word reveals "a cheap rip-off". What replaced them: one easing
  curve; motion with weight (an eased glide that stops when it settles,
  never a loop); no drawn stand-ins for nature (clouds, hills, trees,
  thermals); typography and real photographs as the graphics; a
  photograph never meets the page at a hard edge (its edge takes the colour
  behind it).
- **Trips, less but better (India first, 19 Oct 2026;
  `tools/v4_trip_calm.py`, `html.v4-calm`, with its own `v4-calm.css` and
  `v4-calm.js`, which only a calmed page loads):** the record page's lesson
  on a trip page, one page at a time. One eased loop (the record page's):
  each frame reads the scroll, every value glides toward it and the loop
  stops when all have settled; it moves the hero at 0.3 of the scroll, the
  hairline under the chapter being read, the route's camera and lit line and
  the gallery's dissolves, captions and marks.
  The hero is one plate with the owner's footage (no slideshow, no tabs, no
  cue); the facts under it are four big facts (next departure, length,
  level, price) over the old row's other four. In the fly-through each
  photograph dissolves in over the last, which stays whole beneath it (no
  frame is two photographs half gone over the dark), and settles once per
  step instead of a slow zoom; its words come in at the foot of the screen
  once their photograph has come (the first step's once the heading has
  passed), hold there, and leave before the next arrive and before the
  chapter bar. The gallery opens on a strong photograph and closes on one
  (the back ranges from the air, Last light), none shown twice on the page.
  On a wide screen it is pinned: one photograph at a time fills the screen
  at full brightness once settled; the scroll picks the photograph and the
  loop dissolves the next in over the last, which stays whole beneath it, so
  no frame is ever empty, even in a flick; one caption at a time, the one
  whose photograph is more than half in, the last gone before the next comes
  and none resting half faded, its count (01 / 13) in the caption so the two
  always agree; marks that fill and a skip link along the foot. On a phone,
  and with reduced motion or no script, it is a column of full-width
  plates, clean nearly edge to edge: a short soft edge and a small gap of
  the page between plates, a breath and not a dark band, each caption on its
  own photograph's lower third on an eased shade. The route stays a
  schematic (the page gives no positions to draw to scale) with straight
  lines for the ranges, the back ranges dashed; its
  fall ends on the whole of India with Bir Billing's name on a halo (no
  border through it), every card gets an equal share of the pin, and the
  schematic and the cards' words sit on pools of the page's dark, so no line
  of the map runs through them, while Bir Billing stays lit on the dimmed
  map beside them; as it comes in, the pool comes before the schematic's
  names, so none sits on a border. "Guaranteed to run" is a status line,
  its green only in the dot; the guides sit under hairlines, their roles in
  label type; the
  footer follows the call closely, with no drawn ridge and no glow alone in
  an empty band. The gauge, the season ring, the tour bars and the day line
  are drawn finished; no reveals on headings or the call card, which keeps
  its card without the corner bracket; every transition in the page on
  `--ease`. Each dissolve is a smoothstep from clear to the page's dark (the
  `--v4c-1` to `--v4c-7` steps).
- `prefers-reduced-motion`: transitions off, everything visible. With
  JavaScript off, everything readable (the fly-through shows every trip).

## Phone and touch
- 16px gutters at the phone width, no sideways scroll at 390, 768 or 1440.
- On touch screens every tap target is at least 44px tall
  (`@media (pointer:coarse)`), with the compact look kept under a mouse.
- Order on a phone: the words first, then the buttons, then the media.

## Drawings (v4)
Every drawing is made with the kit (`tools/v4_draw.py`): hairlines that keep
their width at any size, the site's type, orange for what matters. The
knowledge base figures come from their original scripts through
`tools/v4_kbsvg.py`; placed by `tools/v4_pass.py` (inline when small or
labelled, a lazy image when large and wordless). Keep the alt text as the
drawing's title and never touch og:image.

## Files (v4)
Edit the readable sources in `prototypes/v4/src/` (`v2.css`,
`v2-immersive.js`, `v4-menu.js`), then `python3 tools/v4_min.py` writes the
served copies without comments. The menu's code loads on first use.
Speed rule: no v4 page heavier on arrival than its v2 twin
(`python3 tools/v4_weight.py`, compressed as served).

## Checks before any push
`./build.sh`, `python3 tools/audit.py --drift`, `python3 tools/smoke.py`,
`python3 tools/v2_check.py --site v4` (0 FAIL: links, noindex, headings, alt,
SEO/GEO parity with live, errors, overflow, names, tap targets, no link into
another prototype), `python3 tools/v2_switch.py --site v4 --dry-run` (0 FAIL),
`python3 tools/v2_check.py --static` (v2 still 0 FAIL) and
`git status --short prototypes/v2` (empty).
