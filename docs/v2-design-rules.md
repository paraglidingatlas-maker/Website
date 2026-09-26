# v2 design rules (frozen 26 Sep 2026)

The rules the v2 pages already follow, written down so new work is checked
against them instead of judged by eye each time. The values live in
`styles.css` (`:root`) and `prototypes/v2/v2.css` (the kit); this file says
how to use them. The living examples are on `prototypes/v2/styleguide.html`.

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
Poppins (`--font-display`) for titles and numbers, DM Sans (`--font-body`)
for everything else. Sizes only from the scale: `--fs-micro` (kickers,
labels), `--fs-small` (meta, chips), `--fs-body-s` (card text), `--fs-body`,
`--fs-lead` (intros), `--fs-h4` (card titles), `--fs-h3`, `--fs-h2`
(section titles), `--fs-h1`, `--fs-display` (heroes). Kickers are uppercase,
600, letter-spacing .16em, orange. Stat numerals are outlined.

## Space and layout
- A section is a band: `.kit-band` (vertical `--sp-section`, sides
  `--gutter`), content in `.kit-in` (max `--measure`, 1300px).
- Head: `.kit-head` = `.kit-kicker` + `.kit-title` + optional `.kit-intro`.
- Gaps only from `--sp-1` to `--sp-5`.
- Grids: `.kit-grid` (auto-fill 17rem), `.is-2`, `.is-3`. Never three narrow
  columns on a tablet: two to a row between 561 and 1024px.

## Pieces
- **Buttons:** two kinds only. `.btn-solid` (orange, skewed, one per group)
  and `.btn-lines` (outlined). A status (`.v2-status`) may sit after them.
- **Panel:** `.kit-panel`, lit from its top-left corner, words only.
- **Card:** `.kit-card`, a picture and words.
- **Soft surfaces, not boxes:** cards (episode tiles, topic and knowledge base
  cards, side boxes, Up next) have no outline and no inner rules: a faint fill
  lit from the top. The orange corner shows only under the pointer or keyboard
  focus. Chips and filters are soft fills; the chosen one is orange. Search
  boxes are a soft field with a line underneath.
- **Facts:** a row of label (micro, orange, uppercase) over value (white).
  Trips show next date, length, level, price; group size lives in the
  departures table.
- **Words on a photo:** no box. A shade (gradient) behind them, darker on the
  side the words sit; small orange text on a photo gets `--orange-lite` and a
  tight dark text-shadow.
- **Fly-through** (home, `.v2-flyby`): one picture held on screen, each trip's
  details passing over it; the section heading is its first frame.
- **Episode page:** the player beside the title (every episode, owner's
  choice); quote and guest card in one row below; chapters, transcript,
  "Fly with us", "Up next". Host-only episodes say "Hosted by".

## Motion
- Only in answer to the visitor: scroll, pointer, tap, key. Nothing loops or
  moves on its own except a looping flight video, and that only while on
  screen.
- Page darkens as it descends; images fade up from a blur; contour backdrop
  behind text sections. No tracers (removed at the owner's request).
- `prefers-reduced-motion`: transitions off, everything visible. With
  JavaScript off, everything readable (the fly-through shows every trip).

## Phone and touch
- 16px gutters at the phone width, no sideways scroll at 390, 768 or 1440.
- On touch screens every tap target is at least 44px tall
  (`@media (pointer:coarse)`), with the compact look kept under a mouse.
- Order on a phone: the words first, then the buttons, then the media.

## Checks before any push
`./build.sh`, `python3 tools/audit.py --drift`, `python3 tools/smoke.py`,
`python3 tools/v2_check.py` (0 FAIL: links, noindex, headings, alt, SEO/GEO
parity with live, errors, overflow, names, tap targets) and
`python3 tools/v2_switch.py --dry-run` (0 FAIL).
