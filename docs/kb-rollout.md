# Knowledge base rollout: handoff

Read this first in any new chat that continues the knowledge base work. It is
the whole brief: what the pages are, how one is made, how to check it, how to
ship it, and how to do it without burning the session.

## What we are doing

Each knowledge base series page (`knowledge-base/<slug>.html`) is being turned
from a thin link hub (~300 words) into a full article built from the episode
transcripts: a drawn hero, five editorial bands with drawings, a quote band, a
practical callout, grouped takeaways, ten FAQ answers and a closing strip.
Every claim links to the chapter of the episode where the guest says it.

Why: SEO and GEO. These pages were nav with no answers on them. Now each one
is a citable article that ranks on its own and links down into the episodes.

## Status

| Series page | Episodes | Status |
|---|---|---|
| flight-mechanics | 8 | done |
| risk-vs-reward | 12 | done |
| know-your-equipment | 8 | done |
| new-technologies | 7 | done |
| the-dark-side | 5 | done |
| world-cups | 7 | done |
| resources-tools-tips | 11 | done |
| brand-stories | 4 | done |
| navigators | 6 | done |
| sky-gods | 4 | done |
| living-the-dream | 6 | done |
| storytellers | 2 | done |
| weather-patterns | 1 | done |

| Landing page | Series | Status |
|---|---|---|
| core-series | 3 | done |
| competitions | 3 | done |
| meteorology | 1 | done |
| industry | 3 | next (landing layout) |
| technical | 3 | to do (landing layout) |

The five category landing pages use the lighter landing layout described under
"Landing pages" below. Update these tables when a page ships.

## Landing pages

The five category pages (`core-series`, `competitions`, `meteorology`,
`industry`, `technical`) are built by `category_page()` in
`generate_kb_pages.py`. When the slug has an entry in `kb_landing.py`, it hands
over to `landing_page()`, which renders `kb_layout.landing()`: a hero (kicker,
H1, lead, sub, series count), the series cards (each showing the H1 of its
series page), and a five-question FAQ. The stylesheet and script are the same
`templates/kb/category.css` and `category.js` as the series pages; the only extra
CSS is the card rules taken from `CATEGORY_CSS`. A slug without an entry keeps
the old plain card page.

- Content: `kb_landing.py`, one entry per category. Everything comes from the
  published series pages and the chapters they cite; no FAQ question repeats a
  series page FAQ. Answers may cite several chapters (`src` is a list), and the
  links are validated at build time.
- Hero: `assets/images/kb-<slug>.jpg` (2400x900) plus `.webp`, drawn by
  `tools/kbfig/landing_hero.py <slug> <out>`: an abstract motif per category.
  The image also becomes the page's og:image, so add it only when the page
  itself switches over.
- Checks: as for a series page, with 5 JSON-LD questions and the series card
  count. The change must leave every other knowledge base and episode page
  byte-identical apart from `dateModified`: snapshot them before, diff after.

## Where things live

- `kb_editorial.py`: the content. One entry per series slug. **Copy the shape
  of the `know-your-equipment` entry exactly**; it is the cleanest example.
  `"layout": 2` switches a slug to the new design.
- `kb_layout.py`: renders an entry into the page body. Validates every
  `(episode, chapter)` reference at build time; a wrong chapter fails the build.
- `templates/kb/category.css`, `category.js`: the design and the immersive
  layer (canvas, reveal, parallax). Do not fork per page.
- `generate_kb_pages.py`: picks up the entry, supplies the episode grid,
  stats, head, nav, footer.
- `tools/kbfig/`: the drawings. `common.py` has the palette and helpers;
  `rvr_*.py` and `kye_*.py` are working examples of a hero, a quote-band image
  and figures. Copy one, change the subject.
- `assets/images/kb-<slug>.jpg` (hero, 2400x900), `kb-<slug>-section.jpg`
  (quote band, 2400x1000), `kb-<slug>-<figure>.jpg` (figures, 2400 wide).
  Each needs a `.webp` beside it (PIL, quality 84, method 6).

## Making one page: the lean process

Budget: aim for roughly 12 to 15 tool calls per page. The expensive things
are reading, images and long outputs. Keep all three small.

1. **Episodes and chapter map.** One call: list the episode slugs linked from
   the current `knowledge-base/<slug>.html`, and for each, print the guest,
   duration and chapter titles with word counts (not the text). Save the
   chapter text per episode to `/tmp/<slug>/<episode>.txt`.
2. **Read selectively.** Do not print whole chapters. Use `grep -i -n` or a
   small Python search over the saved text for the claims you need (numbers,
   named techniques, strong opinions), printing ~600 characters around each
   hit. Chapter titles tell you where to look. Two or three calls, not ten.
3. **Plan five bands.** Group by idea, not by episode. Each band: kicker,
   heading, a two-sentence summary, two paragraphs, 3 to 5 bold terms, chips
   for the guests it draws on, and optionally a figure. Pick two or three
   bands that deserve a drawing.
4. **Drawings.** Copy the nearest `tools/kbfig/*.py`, change the subject,
   render once, view once at reduced size. Fix only real problems (overlap,
   clipping, wrong physics). One revision at most; the user will ask for more
   if they want it. Hero: subject in the right 60%, left 40% dark and empty.
5. **Write the entry** into `kb_editorial.py` (append before the final `}`,
   put slug constants above `EDITORIAL = {`). Rules below.
6. **Build and check.** `./build.sh` then `./check.sh` must say "All three
   gates clean". Also confirm: 10 FAQ questions in the page's JSON-LD, the
   right tile count, and phone `scrollWidth` 390 (a two-line Playwright check;
   no full-page screenshot needed).
7. **Ship.** Commit only the files you changed (`kb_editorial.py`,
   `knowledge-base/`, the new `assets/images/kb-<slug>*`, `tools/kbfig/`),
   push, then `git checkout -- .` to drop build-only `dateModified` churn.
   **Wait ~100 s and confirm the "pages build and deployment" run for that
   commit concluded `success`** via the GitHub API. A failed deploy has
   happened once (upload step); re-run it with
   `POST /repos/.../actions/runs/<id>/rerun`.
8. **Update the status table above** in the same commit or the next.

## Writing rules

- Paraphrase; never quote the transcripts, which are automatic captions. The
  quote band is a paraphrase and says so.
- Every takeaway, FAQ answer, callout and figure source links to a real
  chapter. If you cannot find the chapter, drop the claim.
- Attribute carefully. Captions often mislabel speakers; when a two-guest
  episode makes it unclear who said something, credit both or leave it out.
  Do not upgrade a claim (e.g. calling someone a world champion when the
  transcript does not say so).
- FAQ: questions end in `?` (and takeaway titles must not, or the schema
  picks them up as extra questions), answers 55 to 70 words, phrased the way a pilot
  would search.
- `seo_title` 70 characters or fewer; `seo_desc` 70 to 165.
- No em-dashes anywhere. Orange accents stay as designed.
- H1 is the question a pilot would type; the series name is the kicker. The
  URL never changes.

## Narrative series (Navigators, Sky Gods, Living The Dream, Storytellers)

These are people and places, not physics. Same layout, different drawings:
a route or region map drawn as a technical sheet (coastline, ridge lines, a
track with waypoints), a topo contour of a famous site, or a typographic
hero. Bands follow themes across guests (how they started, what it cost, the
decision that mattered, what they would tell a new pilot), not one band per
guest.

## Standing preferences

- Do not narrate mid-task; give the result.
- No downloadable files or screenshots in replies unless asked.
- Show name is not changing. Hero coordinates (Oslo) stay.
- Repo pushes are allowed with the GitHub token the user supplies; ask for it
  in the new chat, never write it into the repo.
- Reminder in the user's calendar for Tue 20 Oct 2026: Search Console query
  export for flight-mechanics, to tune its headings and FAQ wording.
