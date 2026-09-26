# v4: report of the autonomous build (from 26 Sep 2026)

The brief is `docs/v4-plan.md`. v4 lives in `prototypes/v4/` (hidden,
noindex), previewed at https://paraglidingatlas.com/prototypes/v4/. v2 and
the live site are not changed. v4's rules: `docs/v4-design-rules.md`.

## Progress
A check-in reads this table to know where to resume: the first row not
marked done is the next step.

| Step | State | Commit | Gates |
|---|---|---|---|
| 0. Setup: v4 copy, `--site`, v2 byte-identical | done | (step 0 commit) | v4 check 182 pages 0 FAIL; switch v4 180 pages 0 FAIL; audit 0 FAIL; smoke 172 / 0 FAIL; v2 rerun byte-identical |
| 1. Basics: the grammar | done | (step 1 commit) | all gates PASS (v4 182 pages 0 FAIL, switch 0 FAIL, smoke 0 FAIL, v2 untouched) |
| 2. Drawing kit and the three-view | | | |
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
