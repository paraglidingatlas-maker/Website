# v4: the brief for the autonomous build (27 Sep 2026)

Read this first in the v4 session. The owner gave the go for everything
below and is away: work without asking, decide by this brief and the design
rules, and put anything that needs the owner in `docs/v4-report.md`. Then
read `docs/v2-roadmap.md` (the list this brief turns into work),
`docs/v2-design-rules.md` (the rules), `docs/v2-handoff.md` (tools, history)
and `docs/v2-report.md` (checks, the switch-over).

## The owner's decisions (the go, 27 Sep)
1. **All work in `prototypes/v4/`**, a copy of `prototypes/v2/`, hidden and
   noindex like v2. `prototypes/v2/` and the live site are never changed: v2
   stays the fallback the owner compares against.
2. **The tools take a site.** Every `tools/v2_*.py` hardcodes
   `prototypes/v2`. Give them one setting (default v2) so the same tools build
   and check v4. Prove v2 is untouched: rerun the v2 tools after the change
   and `git status --short prototypes/v2` stays empty.
3. **Push after every step that passes the gates** (below), to main and to
   `claude/v2-prototype`. The owner previews at
   https://paraglidingatlas.com/prototypes/v4/.
4. **The Arial fix goes in** (the rule is at the end).
5. **Menu:** Expeditions, Podcast, Knowledge Base, About, then Enquire.
   Sitemap moves to the footer.
6. **Library:** build a flight log and a poster wall. The stronger becomes the
   library; the other stays as a hidden sample page.
7. **Text:** cut, fold or reorder without asking. Nothing new written; SEO/GEO
   parity kept (folded text stays in the HTML).
8. **India, then Kenya**, no review in between.
9. **Drawings:** the drawing kit and the paraglider three-view first, before
   and after side by side. If clearly better, redraw them all (the originals
   stay in v2). No Midjourney, no generated pictures: drawn from geometry.
10. **Trust strip** only from facts in the terms and the participant agreement.
11. **Fallback check-ins** so the run survives a stop (below).
12. **At the end:** `docs/v4-report.md`, before/after screenshots, a push
    notification.
13. **Order:** setup, basics, three-view and drawing kit, India then Kenya,
    signature moments, navigation, speed, the remaining redraws.

The principle agreed with the owner: **consistent in the grammar, distinctive
in the moments.** One signature moment per page. The look the owner wants is
immersive and cinematic, dark with the orange accent, trustworthy without
being boring. Uniformity must never flatten it.

## The work, in order (estimates at full effort, about 45 to 55 h in all)

### 0. Setup (about 1 h)
- Copy `prototypes/v2/` to `prototypes/v4/`. Keep the file names inside it
  (v2.css, v2.js, v2-immersive.js...) so the tools need only the folder.
- One setting for the tools: a small shared helper (for example
  `tools/v2_site.py`) that reads `--site v4` (or `PA_SITE`), default `v2`,
  and gives the folder. Prefer the `--site` flag: commands then start with
  `python3 tools/...`, which the allow rules in `.claude/settings.json` match.
  The places that hardcode `prototypes/v2`: v2_localize (4), v2_check (3),
  v2_switch (5), v2_episode (2), v2_twin (1), v2_fly_options (4), v2_art (3),
  v2_library_cards (3). v2_switch's assets folder follows the site
  (`assets/v4`), and so do its stage folder and its prototype-only pages
  (styleguide, fly-options, and any v4 sample pages).
- The page scripts look for the folder: `v2.js` lines 17 and 20 and
  `v2-immersive.js` line 39 match `/prototypes/v2/`. In the v4 copy, match
  `/prototypes/v\d+/`.
- Byte-identical proof for v2: run v2_episode `--all`, v2_twin, v2_localize
  (and the one-off generators) with the default site; `git status --short
  prototypes/v2` must be empty. If a tool was never deterministic, compare
  against a run made before the change instead.
- v4 checks as its own site: `v2_check.py --site v4` and
  `v2_switch.py --site v4 --dry-run` at 0 FAIL; no v4 page links into
  `prototypes/v2/`.
- Start `docs/v4-design-rules.md` (a copy of the v2 rules; v4 changes go
  there, the v2 file stays as it is) and `docs/v4-report.md` with a
  progress table (step, commit, gates). Update the table after every step:
  a check-in reads it to know where to resume.

### 1. Basics: the grammar (2 to 3 h)
- The Arial fix.
- Three page-title sizes and one weight (h1 today: 152, 74, 70, 61, 50 and
  48 px in two weights).
- One section-head pattern: kicker, title, rule, right-aligned note.
- Buttons: `.btn-solid` and `.btn-lines` only (the listen buttons join them).
  One chip: a soft fill, the chosen one orange.
- Partners into the scale: its 61px extra-bold section titles and 56
  outlined tiles become the kit's titles and soft surfaces.
- No empty voids before the footer (library, topics).
- Shorter on-screen episode titles: the long part smaller, every word still
  in the h1.
- A shorter homepage (4 to 5 sections) and less text on the knowledge base
  categories (about 2,400 words), the homepage and the podcast (about 950).
  Fold rather than delete.
- The knowledge base stays different on purpose. Other fonts are welcome
  where they add to the look.

### 2. The drawing kit and the three-view
- The kit: a Python module writing SVG. Engineering line weights (a thick
  outline, thin detail, hairline dimensions), the site's type, callouts with
  leaders, dimension lines, hatching, real curves (splines, arcs), a title
  block citing the episode and timestamp where the page cites one, the
  site's colours on dark. One look for every figure.
- First the paraglider three-view (plan, front, side), before and after on a
  v4 sample page. If clearly better, carry on (step 7).
- Every label, number and dimension comes from the page's own text or the
  episode it cites. What the source does not give is left out, never drawn
  to look precise (no scale bar without a real scale). Keep the alt text and
  the captions.

### 3. India, then Kenya (3 to 4 h, then 2 to 3 h)
- The fly-through style: one screen per idea with the photo or footage
  behind it, facts instead of paragraphs, about 800 words on first read
  (from 4,214 and 3,353). Every word kept: the FAQ, packing and practical
  parts folded (`<details>`), so the body words stay at 95% of live or more.
- Keep exactly: dates, prices (India in £, Kenya in US$, as the site states
  them), places, the departures table, the enquiry links, the structured
  data, and every anchor other pages link to.
- The sticky phone action bar; the trust strip (decision 10); "Hold a place"
  on each departure, opening the enquiry with that departure filled in (it
  stays mailto; payment and places left wait for the owner).
- Proof from past clients: only quotes the site already has, as written.

### 4. Signature moments (about 12 h)
- The rule "one signature moment per page" goes into the v4 design rules.
- The library as a flight log and as a poster wall (decision 6).
- Topic pages: a featured row and rhythm; the knowledge base's header
  pattern (a drawing, the stats row).
- The episode page opening on a globe turned to where the story is from,
  only where the place is in the data; otherwise the usual hero.
- Episode cards that open into the page (cross-document view transitions;
  plain navigation where not supported; off under reduced motion).
- A full-screen menu with photos (focus kept inside, Escape closes, photos
  load only when it opens).
- An altimeter progress marker on long pages (decoration, hidden from
  screen readers).
- Full-screen footage breathers: only footage the site has, at most one a
  page.
- An instrument font (monospaced) for the readout, coordinates, timestamps
  and chapter times: an OFL font, self-hosted and subset like DM Sans, kept
  inside `prototypes/v4/` (the system monospace stack if none can be
  fetched). A
  style guide specimen first, then applied in v4. The outlined stat numerals
  stay unless the mono version is clearly better.
- Knowledge base cards and figures in the new design (the KB stays itself).

### 5. Navigation and wayfinding (5 to 7 h)
- The menu (decision 5), with the current section marked.
- One search in the header across episodes, knowledge base and trips, from
  an index of the pages' own titles and descriptions (no new text).
- Every page ends on one clear next step.
- Bridges between the halves: "from the show" on trip pages, "fly it
  yourself" on relevant episodes (real links only).
- The wind-sound button says what it is.
- The same sticky phone action bar on every trip page; Play / Next on
  episodes.

### 6. Speed
- Home 2.5 MB on arrival (v2) or less; the podcast globe's d3 (273 KB) loads
  only when the globe comes near. No v4 page heavier on arrival than its v2
  twin.

### 7. The remaining redraws (most of the 20 h the drawings need)
- About 57 knowledge base figures, the Kenya map and plates, the trip dials,
  the poster frame, the series and panel icons, the contours and the ridge,
  all with the kit. Each page keeps its og:image as it is (parity).

### 8. The report
- `docs/v4-report.md`: what was done, the gates, before/after screenshots (a
  few key pairs as JPG in `docs/v4-shots/`, under 5 MB in all; also sent to
  the owner with SendUserFile), what needs the owner, and a note on the
  switch: if the owner picks v4, the deploy workflow draft runs the same
  steps with `--site v4`.
- Then the push notification.

## Needs the owner (collect in the report, never wait for it)
- Booking: how to take deposits (a payment link per departure is enough to
  start); places left per departure.
- Proof: client quotes and photos, with permission.
- Enquiry follow-up: an automatic reply and a reminder need a mail service
  (free: Google Apps Script in the owner's Workspace). The form stays mailto.
- Footage and data: IGC logs of the filmed flights (real ALT / HDG and the
  real flight line), 5 to 10 s clips per destination, a wind or vario
  recording, photos from past trips.
- Facts: Peru and Kazakhstan (length, group size, price), 14 episode dates
  and 2 descriptions (list in `docs/v2-report.md`), one episode count (pages
  say 71, 86, 93 and 90+), one currency or both.
- The go: an iPhone check, then the switch-over (v2 or v4).

## Dropped on purpose (they would flatten the site)
One header style for every page, one icon style everywhere, one neutral
grade on the episode stills.

## Gates before every push
```
./build.sh                                        # then: git status shows no live page changed
python3 tools/audit.py --drift                    # 0 FAIL
python3 tools/smoke.py                            # 0 FAIL (the pinch test can flake: rerun once; twice is real)
python3 tools/v2_check.py --site v4               # 0 FAIL (Chromium at 390 as a touch phone, 768, 1440)
python3 tools/v2_switch.py --site v4 --dry-run    # 0 FAIL
python3 tools/v2_check.py --static                # v2 still 0 FAIL
git status --short prototypes/v2                  # empty: v2 untouched
```
And screenshots of every changed page at 390 (touch) and 1440, looked at
before pushing. Walk the page with viewport shots; full-page shots miss the
fade-ins and the sticky parts.

## What could be missed (check at every step)
| Risk | Check |
|---|---|
| v2 or a live page changed | `git diff --name-only origin/main` lists only `prototypes/v4/`, `tools/`, `docs/` |
| a v4 link into v2 | no `prototypes/v2` in `prototypes/v4/` outside comments |
| search / answer-engine loss | the checker's parity: title, description, canonical, Open Graph, Twitter, JSON-LD, episode data, h1 words, 95% of body words, chapters |
| words lost in a fold | folded text sits in the HTML (`<details>`), never loaded by a script |
| an invented fact | every new label, number, callout and trust line traced to a sentence on the site; otherwise `[to supply]` or left out |
| a drawing that looks precise but is not | dimensions only from the source text |
| phone | 390 touch: 44px targets, no sideways scroll; words, then buttons, then media |
| motion | reduced motion: everything visible and still; JavaScript off: everything readable |
| weight | bytes on arrival not above the v2 twin |
| the switch | the dry run for v4: pages, sitemap, robots, links, the live audit |
| fonts | a licence that allows the web (OFL); self-hosted; subset |
| Safari | view transitions and blur have fallbacks; list what the iPhone check should look at |

## Environment (every new container, every check-in)
```
mkdir -p /tmp/claude-0
python3 -c "import fontTools, brotli, PIL, playwright" || pip install fonttools brotli pillow
(setsid nohup python3 -m http.server 8765 --bind 127.0.0.1 >/tmp/claude-0/serve.log 2>&1 &)
curl -sI http://127.0.0.1:8765/prototypes/v2/ | head -1
```
- Playwright 1.56 comes with the image and matches the Chromium in
  `/opt/pw-browsers`. Never run `playwright install`. New scripts launch with
  `executable_path="/opt/pw-browsers/chromium"`. Phone: 390 x 844, touch,
  mobile, scale 2. Desktop: 1440 x 900.
- The preview server stops between turns: start it again each turn.
- Blocked here: YouTube and its stills, anchor.fm, paraglidingatlas.com.
  Grey boxes there in screenshots are expected.
- Permissions: `.claude/settings.json` pre-approves the commands this run
  uses (the tools, git, the pushes, the preview server) and refuses force
  pushes, `reset --hard`, and edits to `prototypes/v2/` and `rss-feed.js`.
  Anything else goes to the auto-mode classifier, which allows ordinary work
  and pushes to main and this branch. A denied command is denied, not held
  for a person: find another way (a script you run often is best saved in
  `tools/` and run as `python3 tools/<name>.py`, which is pre-approved), and
  note it in the report if it blocks a step.

## Fallback check-ins
Before each long step, arm one check-in about 90 minutes out with
`send_later`: "v4 check-in: read docs/v4-plan.md and the progress table in
docs/v4-report.md, start the preview server, carry on with the next
unfinished step, and re-arm this check-in." Keep one pending at a time
(list_triggers; delete the old one when arming a new one). Delete it when
everything is done.

## The rules (the owner's words)
- "Nothing invented. Only facts the site already states or the owner gives.
  Missing facts show as a visible `[to supply]` mark."
- "`rss-feed.js` is DO NOT MODIFY (styles only)."
- "Live site is untouched while v2 is built. Do not change live pages unless
  the owner asks."
- "Switch-over of v2 to live only when the owner asks." The same holds for v4.
- "I don't want to touch version two ... try that on version four and not
  risk messing up version two."
- Keep text short. Verify with desktop and phone screenshots before pushing.
  Push to main with `git push origin HEAD:main` and to `claude/v2-prototype`.
  Send a push notification when a long piece of work finishes.
- The enquiry form stays mailto (no paid Workers).
- No pull requests. Work on `claude/v2-prototype`.

## The Arial fix
Was `arial-fix.patch` in the v2 session's scratchpad. Add to the v4 copy of
v2.css:
```css
/* buttons and form fields take the page's type (browsers do not pass it down
   on their own, so a <button> or an <input> was drawing in Arial) */
:where(button, input, select, textarea, optgroup){font-family:inherit;}
```
