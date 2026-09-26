# v4: report of the autonomous build (from 26 Sep 2026)

The brief is `docs/v4-plan.md`. v4 lives in `prototypes/v4/` (hidden,
noindex), previewed at https://paraglidingatlas.com/prototypes/v4/. v2 and
the live site are not changed. v4's rules: `docs/v4-design-rules.md`.

## Progress
A check-in reads this table to know where to resume: the first row not
marked done is the next step.

| Step | State | Commit | Gates |
|---|---|---|---|
| 0. Setup: v4 copy, `--site`, v2 byte-identical | done | c649f29 | v4 check 182 pages 0 FAIL; switch v4 180 pages 0 FAIL; audit 0 FAIL; smoke 172 / 0 FAIL; v2 rerun byte-identical |
| 1. Basics: the grammar | done | b0310c7 | all gates PASS (v4 182 pages 0 FAIL, switch 0 FAIL, smoke 0 FAIL, v2 untouched) |
| 2. Drawing kit and the three-view | done (redraws go ahead: step 7) | (step 2 commit) | all gates PASS (v4 183 pages 0 FAIL) |
| 3. India, then Kenya | | | |
| 4. Signature moments | | | |
| 5. Navigation and wayfinding | | | |
| 6. Speed | | | |
| 7. The remaining redraws | | | |
| 8. The report | | | |

## How to build and check v4
Every `tools/v2_*.py` takes `--site v4` (or `PA_SITE=v4`); without it they
build and check v2 exactly as before (`tools/v2_site.py`).

```
python3 tools/v2_localize.py --site v4        # after editing any v4 page
python3 tools/v2_check.py --site v4           # every v4 page, 390 / 768 / 1440
python3 tools/v2_switch.py --site v4 --dry-run
```

## Needs the owner
(collected as the run goes; nothing here blocks the build)

## Step 0: setup
- `prototypes/v4/` is a copy of v2 (same file names inside). Its scripts find
  their folder with `/prototypes/v\d+/`, so the same files work in v2 and v4.
- `tools/v2_site.py`: `--site v4` (or `PA_SITE=v4`), default v2. Every
  `tools/v2_*.py` uses it for its folder; `v2_switch` also for its assets
  folder (`assets/v4`), its staging copy (`/tmp/claude-0/v4-stage`) and the
  prototype-only pages (styleguide, fly-options, anything under `samples/`).
- The checker now also fails a page that links into another prototype's
  folder, and a v4 script or style sheet that names `prototypes/v2`.
- Proof that v2 is untouched: every v2 generator (episodes `--all`, twins,
  art, icons, fly options, library cards, localize) and `build.sh` rerun with
  the default site; `git status --short prototypes/v2` is empty. The same
  run before the change was also clean, so the tools are deterministic.
- `tools/v4_shots.py`: viewport screenshots walking down a page at 390
  (touch) and 1440, with a contact sheet (`--sheet`).

## Step 1: the grammar
- **Arial fix** in the v4 v2.css: buttons and fields take the page's type (0
  of 72 controls on India still in Arial; were 32).
- **Page titles: three sizes, one weight (700)**, measured on 17 page kinds:
  73.6 px (display, photo heroes), 60.8 px (sky heroes, and the knowledge base
  door, was 70.4), 48 px (episodes and knowledge base articles, was 50.4 and
  48 at 800). Partners, the trip pages and the episodes lose the 800 weight;
  the trip pages' 152 px wordmark is display size until step 3 rebuilds them.
- **One section head**: kicker, title, a hairline with a short orange lead,
  and an optional note on the right (`.kit-note`; the departures' "Small
  groups, fixed dates. Prices are per pilot." is the first).
- **Buttons**: the listen buttons (home, podcast, the call) and the episodes'
  listen links now read as `.btn-solid` / `.btn-lines`.
- **One chip**: the episode topic tags, the partners' interests, the knowledge
  base series tags: soft fill, the chosen one orange.
- **Partners** in the site's scale: section titles 61 px extra-bold -> the
  kit's section size, kickers the kit's, reel tiles and fields soft surfaces.
- **No void before the footer**: the library's and topics' last band keeps a
  short gap; the topics grid is soft tiles (its short last row left a grey slab).
- **Episode titles**: `tools/v4_pass.py` splits 13 long on-screen titles at a
  natural break (the speaker line above, the rest under the title, smaller);
  every word stays in the `<h1>`.
- **Shorter homepage**: five bands (hero, where we fly and every departure,
  the podcast, why and the list); the call moved into the departures band as
  one row, its pitch and list folded; the "why" panels are titles that open.
  Desktop height 9,403 -> 8,865 px; phone 12,366 -> 11,016 px.
- **Less text on first read, every word kept (in `<details>`)**: knowledge base
  sections show title, summary and sources, the long paragraphs under "Read
  more" (62 sections; e.g. Navigators 1,745 words folded); the podcast's
  "What you can expect" panels open from their titles and the two
  collaborate / sponsor panels fold after their first sentence.

## Step 2: the drawing kit and the three-view
- `tools/v4_draw.py`, the kit: inline SVG in the site's type (the drawing
  inherits the page's DM Sans and Poppins); a 2 px outline, 1 px detail,
  0.75 px hairlines and centre lines that keep their width on a phone
  (non-scaling strokes); callouts with leaders, dimension lines with extension
  lines and arrowheads, angle arcs, hatching, Catmull-Rom splines and true
  arcs, view labels, detail circles, a title block, a drawing-sheet frame, and
  a backdrop (a drafting grid that fades out, a soft orange light on the
  subject). A compact mode sets the labels a size smaller for phone layouts.
- `tools/v4_figs.py`, the paraglider three-view: side view (the profile, the
  lines, the pilot facing forward, the speed bar, the angle of attack, the
  lift resultant), front view (the arc and the lines), plan view, and detail D
  (the brake handle, hands fully up and at the first tension). A wide layout
  and a tall phone layout.
- **Nothing invented.** Every label is a word the Flight Mechanics page uses
  (profile, nose, trailing edge, A lines, B lines, brake line, speed bar,
  angle of attack, lift resultant "moves forward as the angle of attack
  falls"). The one number is the page's own: at least 7 cm of brake travel
  from hands fully up to the first tension, Tom Lolies, Episode 66, chapter 12
  (in the title block). No scale: the title block says "Not to scale". The
  old figure's flight-dynamics symbols (K, P, B, AM, x_b, theta_b...) are not
  on the page, so they are gone.
- Before and after: `prototypes/v4/samples/three-view.html` (a v4 sample
  page: hidden, noindex, never switched). **Verdict: clearly better**
  (vector and sharp at any size, legible on a phone, true labels, the site's
  type), so the remaining figures are redrawn in step 7; the originals stay in
  v2.
