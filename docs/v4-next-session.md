# v4: handoff to the next session (21 Oct 2026)

Start here, then read `docs/v4-plan.md` (the brief and the owner's rules) and
the progress table in `docs/v4-report.md` (rows 0 to 43). Everything below is
the owner's current queue and what the last session learnt doing it.

## The owner's rules (unchanged)
- Only `prototypes/v4/`, `tools/` and `docs/` change. Never `prototypes/v2/`,
  never a live page, never `rss-feed.js`. The switch-over is the owner's.
- Nothing invented: a missing fact shows as `[to supply]` (`.v2-tbd`).
- Design tokens only; no em dashes in copy; cache-bust changed CSS and JS.
- Motion only in answer to the visitor; nothing loops or runs on its own (the
  owner's footage while on screen is the one exception; they were asked on
  20 Oct to confirm it still stands). Reduced motion and no JavaScript show the
  finished page.
- Push only `git push origin HEAD:main` and `git push origin HEAD:claude/v2-prototype`,
  after `python3 tools/v4_gates.py` passes (about 25 minutes; `--quick` while
  iterating). Never forced, no pull requests.
- Never store a token or key in the repository or the chat; GitHub access comes
  from the connected account.
- Episode counts are the RSS feed's (owner, 21 Oct: "whatever the RSS feed
  shows, it's the correct count"; never ask again): the episodes in
  episode-meta.json with a publish date (80 on 21 Oct); tools/v4_polish.py
  feed_count() writes it on the sitemap and Mission.
- No photograph is used twice on the site unless it really must be (faces,
  portraits); a repeat is replaced with a different picture, not dropped
  (owner, 21 Oct).
- Work lean (owner, 21 Oct: "we're spending a lot of time discussing"): at
  most two options for a decision, one preview only for a large visual
  change, small fixes built straight away and shown after.

## Where chat 9 left it (24 Oct): the route plays on, Panchgani is a fifth tour, India moves to 2027, the opening is on the prototype
Chat 9 added one v4 page, the opening sample (`prototypes/v4/samples/opening/`); the rest is docs. Its work is in the review page
https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG (newest at the top; F2's
code is its published file `F2/index.html`, the Panchgani layers are
`F2/panchgani-*`).
- **No restart, the route moves on** (owner: "the transition in kenya is
  making the gliders abruptly switch positions ... instead move on the next
  slide and maybe we can make this as a progress bar ... make the line a bit
  sleek"). The cloud restart is gone: each place plays one forward pass
  (14 s, `push.ms`; 14 s for a place without a move), then the route goes to
  the next place in `ORDER`, round again after the last. During the wipe the
  old pass keeps flying forward (z runs on past 1, capped at 1.3). The short
  orange line on top of the trip readout (`.deck::before`) is now a progress
  bar: full width, 1 px, a soft glow, `scaleX(var(--prog))`; it drains as the
  next place wipes in. Code: `playOn()` and `dwell` in F2/index.html; it
  pauses off screen, in a hidden tab and mid swipe, and restarts when the
  visitor picks a place. Reduced motion: no autoplay, the line stays 48 px.
- **Panchgani** (owner: first "Add Panchgani to F2 as option A", a podcast
  stop apart from the season; then "it has dates, 2 days after the last kenya
  tour and runs for 8 days"; then "yes, it is a proper tour which will need
  to have all its necessities like other destination pages in the site, for
  now do this and then we proceed"). Now a dated tour on the season line:
  14 to 21 Feb 2027, 8 days (Kenya's last ends 12 Feb), bar at left 31.89%,
  width 2.04%, marker 32.91%; `ORDER` is India, Kenya, Panchgani, Kazakhstan,
  Peru. Its name reads to the right of its marker (`.tp.lt`), and on a phone
  sits a row above Kenya's. Readout: launch and price `[to supply]`; "You fly:
  The plateau that hosted a pre World Cup" (episode summary); photo credit
  under the place name, "Photo by Michael Gebert / @flywithandy_paragliding"
  (owner's words; the handle links to Instagram); the button is still
  "Listen: Navigating Panchgani" (`episodes/navigating-panchgani-vistasp-kharas.html`)
  until a Panchgani tour page exists. The `.season` box and the route-%
  glider positions read from each marker in `layout()` stay (with `--s:1`).
  Photo: the review page's `src/panchgani.webp` (1500 x 756). The wing keeps
  its real size and place (`box`, mapped through the ground's cover rect);
  PANCHGANI is at Kazakhstan's size (`sizeAs`) with its middle on the
  plateau's flat top (`rim: 0.285`). Motion (owner: "a left circle with a
  very shallow angle while moving forward ... ensure this does not become
  nauseating"): over each 14 s pass the land comes 4% nearer (`g` 0.04 about
  `far` [0.47, 0.4], depth `k` 0.04), slides 2.5% of the width right
  (`pan[0]`, centred) and turns 1.6 degrees clockwise about the frame's middle
  (`push.rot`, new uniform `uGRot`); name and wing hold still. The wing was cut
  by hand (low saturation inside its box, the pilot in a tight box: about
  110 px of wing, too small for the line tools), then `scene.py` with
  place-named outputs, `groundw` 1500, `wingw` 240.
- **India's dates** (owner, 24 Oct: "move dates of india to 15th april for
  the first tour and then 1 day later the next one", then "keep the older
  india dates for 2027 so make that tour visible as well accordingly
  everywhere needed"). In F2 India now has four departures, 10 days each:
  15 to 24 Apr 2027, 25 Apr to 4 May 2027 (one day after the first ends,
  read like Panchgani's "2 days after"), 21 to 30 Oct 2027, 3 to 12 Nov 2027.
  Bars at 46.19/2.38, 48.57/2.35, 90.32/2.3, 93.33/2.38 (%), marker 48.56%;
  `ORDER` is Kenya, Panchgani, India, Kazakhstan, Peru; on a phone
  Kazakhstan's name reads right of its marker (`.tp.lt-m`) to clear India's;
  the dates are one a line (`dd.four`). The Oct and Nov 2027 bars sit inside
  Peru's dashed "planned Nov 2027" box. **Not done, chat 10's first job:**
  the same dates "everywhere needed" in v4 (only v4; live pages are the
  owner's). India's 2026 dates are written in many generators: grep
  `21 to 30 Oct 2026`, `2026-10-21`, `3 to 12 Nov 2026` in tools/ (v4_expeditions*.py,
  v4_trip_calm.py, v4_pass.py TRIPS, v2_episode.py, v2_fly_options.py,
  v3_directions.py, ux_measure.py, smoke.py) and prototypes/v4 (index,
  expeditions*, destinations/india, enquire, about, fly-options, styleguide,
  v4-sitemap-sky.js); some v4 pages are localized from the live pages, so
  change the v4 generator or polish step, never the live page.
- **The opening is on the prototype** (owner: "make this page live on proto
  and give me the link"): `prototypes/v4/samples/opening/` (index.html plus
  its 47 files, about 6.7 MB), a standalone review page (noindex, links to
  the v4 pages with `../../`, its own styles: a comment names why it links
  neither styles.css nor v2.css, which v2_localize looks for). Live at
  https://paraglidingatlas.com/prototypes/v4/samples/opening/?kenya=9492
  once deployed. It is a copy of the review page's F2: change both, or
  rebuild this one from F2 (rewrite the page links to `../../`).
- **The library is another chat's** (owner, 24 Oct: "forget about library
  here, I'm working on it on another chat ... which needs to be connected to
  chat 10"): the owner's chat https://claude.ai/code/cshk_014sbQF9W1CqGXbH3oHgNsEBPkibnHiMxcAso6rNZN4e7y
  (session_014sbQF9W1CqGXbH3oHgNsEB, "Website immersion capabilities
  assessment"). Do not change `library.html`, `tools/v4_library.py` or the
  library chart from this chain; before touching anything the library
  shares (the build, `tools/v4_polish.py`, the nav), check with the owner.
  That session can be found with list_sessions and sent a message
  (SendMessage to its name), but a cloud session cannot answer back, so
  anything it needs to know goes through the owner too.
- **Next (owner):** Panchgani needs everything the other destinations have
  in the site (its own destination page and the rest); the owner said "then
  we proceed", so ask what comes first only if it is not clear from them.
- **Waiting on the owner (do not push):** how the autoplay and the Panchgani
  turn look live; Panchgani's launch and price; and everything still
  listed under chat 8 below.

## Where chat 8 left it (24 Oct): F2's Kenya photo and DSC_9492's move, nothing half-built in the repo
Chat 8 changed nothing in v4 (docs only: this section, `docs/home-opening`
README and `scripts/sheet.py`, the contact-sheet maker). All its work is in
the review page https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG (newest at
the top; F2's code is its published file `F2/index.html`).
- **Big-wing search** (owner: "stunning photos only where the wing is
  visible largely"). Went through the Drive's "Kenya Feb 2025" (62 JPGs and 6
  NEFs; 58 JPGs downloaded) and "Go Pro Photos" (10 frames, all Norway and a
  sea coast, nothing for Kenya or India). Shortlist sent to the owner, no
  answer yet: **DSC_9473** (orange wing against the sky, lines clear; the
  pick), **DSC_9489** (orange and blue over red earth), **DSC_9792** (biggest
  wing, over grass); runners-up DSC_9814, DSC_9763. Not reachable through the
  connector: IMG_2073, IMG_2074, IMG_2132 (8.5 to 9.7 MB, the connector drops
  on them) and IMG_2111 (over 10 MB). India: still no originals; the owner
  was asked once for full-size India JPGs under 10 MB.
- **Wing liveries** (owner asked to see the wing in a Kenyan pattern, then
  said "forget it"). Three F1-style looks were shown in chat only (shuka
  slash, bead line, Maasai shield). Dropped; do not raise.
- **DSC_9492 now moves** (owner: "the gliders have to go away from the viewer
  and background is correct, but this has to be done slowly"; three designers
  D, E, F were asked; the owner said "ok" to option A, D's and F's): a follow
  shot that starts when WebGL takes over (about 1.55 s), 12 s each way. The valley grows 1 to 1.08 about its far point (uv 0.42, 0.18 of the
  ground) with a depth dolly 0.10; the gliders shrink 1 to 0.9 about their
  own centre and drift 2% of the width toward that point; their shadow gap on
  the letters shrinks to 0.6 and darkens 14%; the mouse pull shrinks with
  them; scroll works on top. The arrival glide for this photo starts at
  scale 1.05 from lower right (`glide-away`), so the gliders only ever move
  away. Code: F2/index.html `PHOTOS.kenya['9492'].push`, `pushZ`, `drawDest`,
  uniforms `uDolly` and `uShK`. Option B (E's: scroll drives the move, bigger)
  was not chosen.
- **Then (owner, 24 Oct):** "the shadows become too prominent upon scroll,
  reduce that by 50%": on every place the gliders' shadow strength now falls
  to half as the page scrolls (`uShK` times `1 - 0.5p`) and its scroll gap
  grows half as much (`lift` 1.4 to 0.7). "Do the same with India": the
  snowline photo drifts, the ground 2.2% of the width right plus a depth
  shift 0.03 (near rock moves more) under a 5% zoom that hides the edges,
  the wing 3.5% left, 14 s each way (`DESTS.india.push`); "red wing" and
  "launch day" stay still. (A first, smaller drift, 1.2%, was too small to
  see: the owner said "the india animation isn't working".)
- **The owner changed the motion rule for these (24 Oct):** "for both kenya
  and india add this as a infinity loop, as long as the viewer stays the
  immersion stays"; then "the gliders start reversing after a bit, that
  defeats the purpose, they should only go in one direction, and that is
  forward" (Kenya, then "do the same for india"), and "make sure your
  restart is awwwards worthy". So both moves only ever go forward, forever:
  each pass runs 14 s at an even pace (the first starts from rest); the next
  pass starts 9.1 s in (`fade` 0.35). The restart is hidden in a cloud we fly
  through: in Kenya a ring of cloud streams out from the valley's far point,
  in India a bank of cloud drifts across with the snow; the next pass is
  drawn over the last only where the cloud has already passed (shader
  `cloud()`, uniforms `uMist`, `uMistB`, `uRev`; per place `push.mist` =
  [mode, colour, peak]; India's colour is above 1 because its grade is dim).
  A faint wisp (0.08) always drifts. Time runs only while that place is
  drawn, so it pauses off screen, in a hidden tab and on other places.
  Reduced motion: still. This is the owner's exception to "nothing loops on
  its own" for these two opening moves only. Testing note: headless
  Chromium draws slowly, so the scene clock (capped at 50 ms a frame) runs
  at about half speed there; capture by the clock, not by wall time.
- **Waiting on the owner (do not push):** which Kenya big-wing photo (if any)
  to build into F2 the same way (grade, cut-out with real lines, filled
  ground, shadow, depth: `docs/home-opening/README.md`); India originals;
  everything still listed under chat 7 and chat 6 below.
- Testing WebGL in this container: serve the folder over http on any port
  but 8765 (the gates use 8765 and will use, and fail on, any server already
  there), not file:// (textures from file:// are
  cross-origin and the WebGL scene never starts); headless Chromium has WebGL.

## Where chat 7 left it (24 Oct): the home opening is down to photo choices, nothing half-built in the repo
Chat 7 changed nothing in v4. It ran a second round of three designers on
C2 (the owner, 23 Oct: "C2 is really nice", asked for a competition to
improve it). All live in https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG,
newest at the top, each with its files under its letter:
- **D. Final Cut** (craft: drawn lines, a light per place, film-cut switch),
  **E. Pull Back to the Route** (scroll pulls back into a four-place route
  that replaces the destinations section), **F. Fly the Season** (the list
  becomes a season line Oct 2026 to Nov 2027 with each trip's readout and a
  button to its page; `[to supply]` for Kenya, Peru and Kazakhstan launch
  heights and the Peru and Kazakhstan dates).
- The owner looked at **F** and asked for the wing's "original lineset" back,
  then chose photos: DSC_9522, DSC_9492 and DSC_6210 for Kenya, and "similar
  examples for India". Built as **F2** (same page, `F2/`): a review-only pill
  switches Kenya (now DSC_9452, DSC_9522 with its real lines traced from the
  photo, DSC_9492 three gliders) and India (now snowline, red wing, launch
  day; no lines, only 1400 px copies exist). How the layers are made, and the
  scripts: `docs/home-opening/README.md`.
- **Waiting on the owner:** which design (F2 is the one they are working
  in) and which photo per place; a JPG export of DSC_6210 (the NEF is over
  the Drive connector's 10 MB limit); full-size India originals if India
  should get real lines. Still open from chat 6, not raised again in chat 7:
  the live episode chart (finish or drop) and the five Kenya repeat photos
  (both below, unchanged).
- On a yes: build the chosen design into `tools/v4_polish.py` `home_markup`
  and HOME_CSS/HOME_JS, layers into `prototypes/v4/img/`, drop the pill.
  Note DSC_9452 is also the record page's new Kenya photo (chat 6), and the
  India choices are in the India gallery: "no photo twice" needs a call.
- Container (24 Oct): the preinstalled Chromium is now build 1243, so the
  gates' browser needs `pip install "playwright==1.63.0"` (1.56.0 no longer
  launches; check `/opt/node-tools/node_modules/playwright-core/browsers.json`
  if it moves again). Still `git fetch --unshallow origin claude/v2-prototype`
  and `pip install contourpy fonttools brotli` first.

## Where chat 6 left it (23 Oct): three things wait on the owner, nothing half-built in the repo
Chat 6 changed nothing in v4. Its work lives in two private review pages the
owner has; their published files are the hand-over (read them with the
Artifact tool, `action: "read"`, `path`).
- **The live episode chart** (owner, 22 Oct: "make this live and real
  clickable to episode pages"). Built and tested in chat 5; screenshots in
  the review page https://claude.ai/artifact/H3xMx4aW6teybonm5aYpvY. The
  owner has not said "finish it" or "drop it". The change is that page's
  published file `chart.patch` (tools/v4_pass.py topic_log and topic_page,
  tools/v4_library.py, tools/v4_polish.py LOG_CSS and LOG_JS, report row 54).
  To finish: `git apply` it, `python3 tools/v4_build.py` twice (the second
  changes nothing), `git checkout -- sitemap.xml`, commit, gates, clean
  rebuild, push. To drop: nothing to undo.
- **Five new Kenya photographs for the repeats** (owner, 22 Oct: find them
  in the Drive, "impactful and captivating", edited to match the site).
  From the owner's Drive folder "Kenya Feb 2025" (Paragliding Atlas > PG
  Atlas Photos > Photos by Self): DSC_9840 for About's Kenya card, DSC_9842
  and DSC_9541 for Expeditions' Kenya and Kerio Valley photographs (with 2:3
  phone crops), DSC_9452 and DSC_9537 for the record page's Kenya and Kerio
  Valley photographs. Graded warmer and deeper with a soft vignette, framed
  on the wing. The finished files (jpg and webp, `edit/` in the same review
  page) await the owner's yes; the review page shows each against the photo
  it replaces. Where each is set: Expeditions in `tools/v4_expeditions.py`
  (about lines 337 and 366), the record page in `tools/v4_record*.py`,
  About's card comes through the v2 About build (find `kenya-3` in the
  About source). Put them in `prototypes/v4/img/`, never in `assets/`.
  Still uncovered: India, Peru and Kazakhstan (no photographs of them in the
  Drive), Coupe Icare (the Drive's "Coupe Icare Asset Sheet" folder is not
  yet looked at). The Drive connector refuses files over 10 MB and dropped
  the connection on them; the owner's "Hi Res Camera" folder needs smaller
  exports.
- **The home page opening** (owner, 23 Oct: the hero "is a joke"; asked for a
  competition between three designers). Three mock-ups (A footage, B atlas
  chart, C still photograph with the wing cut out over a giant KENYA); the
  owner liked C, asked whether dropping video lost awwwards ground, and said
  "ok" to both upgrades: C2 adds depth-map parallax (Depth Anything) in
  WebGL, the wing's shadow on the letters, a pointer light, static grain, a
  one-time arrival (about 1.5 s, approved), footage inside the letters on
  point or tap (India: the Bir clip; the others a second photograph, since
  footage must come from the named place) and a four-destination switcher.
  All four live, with their files, at
  https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG (C2 first). Waiting for
  the owner's verdict on C2. C2's open points: Peru and Kazakhstan reuse
  peru-1 and kazakhstan-1 (already lower on the home page; kazakhstan-1 may
  be a composite, ask); the wing cut-outs lose the lines; not yet tried on a
  real iPhone. New headline in C and C2: "Paragliding expeditions, run by a
  pilot." Building the winner into v4 means `tools/v4_polish.py`
  `home_markup` and HOME_CSS/HOME_JS, the assets into `prototypes/v4/img/`.
- Parked by the owner (23 Oct, "I'll take my own time, don't disturb me"):
  the Encarta concept for the globe and the encyclopedia home. Do not ask.
- Small, not yet offered again: on a phone the library chart's year labels
  and "166 min" are tiny (the topic pages' chart got larger ones in row 45).
- The build needs `contourpy` (`pip install contourpy`; v4_expert.py's
  meteo drawing). A fresh container may lack it: `v4_build.py` then fails at
  `v4_pass.py`.

## Where the queue stands (21 Oct)
Items 1 to 3 below are done and pushed: the sitemap's real sky (row 35, with
the motion the owner asked for), Partners (row 34) and the site-wide pass on
home, podcast, library, knowledge base, topics, About and Mission (rows 36 to
43). The owner chose every look from side-by-side previews; the episode
reader fix the switch-over needed is done too (the report's switch-over
section). What is open:
- **The record page photo**: built on 21 Oct (report row 44) as the owner
  chose from mock-ups, `docs/record-photo/README.md` and `tools/v4_record.py`
  01 the mark. A full-size export of DSC06347 would let it fly larger.
- **The review of every page type** (21 Oct): screenshots of 17 page types
  on desktop and phone sent to the owner, with what the review found (below,
  under "Found in the 21 Oct review").
- Done on 21 Oct from the review (row 45): the four small fixes and the
  corrections v4 can make. Left for the owner: the same
  corrections in the live site's own sources (generate_tag_pages.py lines
  331 and 363, episode-meta.json, destinations/kenya.html).
- Photographs used twice on v4 (owner's rule), each waiting for a new
  photograph from the owner: About's Kenya, Peru and Kazakhstan cards (the
  home page's), Expeditions' India and Kenya photographs (the trip pages'),
  and the record page's Kerio Valley, Kenya hero and Coupe Icare photographs
  (the Kenya page's and Partners'). Episode cover art repeats by design.
- The home page (roadmap step 6): built on 21 Oct, both directions the
  owner chose ("both A&B", report row 46): figures under the opening that
  count up, every departure on one line of months, the held photographs that
  come closer, the episode cards that lean gently towards the mouse (a
  stronger lean was tried and turned back by the owner; the trip list's
  orange fill was taken out, "remove this"). All in `tools/v4_polish.py` (HOME_CSS, HOME_JS, `home_markup`,
  read from the site at each build).
- **The encyclopedia** (21 Oct, report row 47): the A to Z and the ten
  Flight Mechanics answers are v4 pages under the knowledge base
  (`tools/v4_encyclopedia.py`, rebuilt from the review copy in
  `prototypes/workspace/drafts/` on every build), reached from the knowledge
  base page, Flight Mechanics and the FAQ answers the A to Z links to.
  Prototype-only until the owner has reviewed the ten drafts. A change to an
  answer is made on the encyclopedia-pilot branch (`kb_answers.py`) and the
  review copy built again (`ENC_SHOW_DRAFTS=1`). That branch's A to Z filter
  changes only the count (fixed in v4 only).
- **The Encarta pieces** (21 Oct, report row 50, `tools/v4_enc_lab.py`): the
  seven worlds and the featured article on the A to Z, the moving wing on
  Collapse, the angle-of-attack lab on Collapse and Stall. Next, if the owner
  wants more: Active flying with the same lab, the Encarta build's kinds of
  collapse and step-by-step pictures, and a picture for each other answer.
- **The Atlas** (21 Oct, report row 48): the knowledge base's button opens
  the globe (`knowledge-base/encyclopedia/atlas.html`, `tools/v4_atlas.py`),
  and its pins and questions lead into the encyclopedia. Built from the
  site's own data (globe-episodes.js, the FAQ answers, the ten answers),
  not from the workspace's Flying Atlas, whose 450 entries were never
  checked. On the home page too, later, if the owner wants it there.
- **The sitemap's ground** (21 Oct, report row 49): every page that is not an
  episode, one click away under the sky (`tools/v4_sitemap_sky.py` ground()).
  The landmarks followed (row 52): Home as the moon, the Atlas, the
  knowledge base's altitude scale, the trips as planets over the ridge and
  the named stars. Not built: the topics as a Milky Way.
- From the 20 Oct roadmap, still open: icons to photographs (step 7,
  waiting for the owner's photographs; on About the owner chose to keep the
  icons).
- The switch-over stays the owner's.

## The queue, in the owner's order (20 Oct)
1. **The sitemap's night sky from real stars.** The v4 sitemap
   (`prototypes/v4/sitemap.html`, built by `tools/v4_catchup.py`
   `sitemap_sky()`) loads the LIVE `sitemap-sky.js`, which must never be
   edited. Its background field is seeded random (`rnd()`, seed 20261002, about
   line 47) drawn on the `.sky-stars` canvas; the episode stars and the series
   constellations are data and stay. Real positions and magnitudes are already
   in the repo: `tools/v4_record.py` `STARS` (d3-celestial 0.7.35,
   `data/stars.6.json`, BSD-3-Clause, XHIP; the credit and notice are its
   `STAR_NOTE`, which must go with the data). Way in: a v4-only background
   layer under the sky (or a v4 copy of the script, `prototypes/v4/`), loaded
   only by the v4 sitemap, credited, still (no twinkle), drawn once; then add
   its tool step to `tools/v4_build.py` after `v4_ux` if it patches the page.
2. **Partners** (`prototypes/v4/partners.html`): the formats laid out like the
   record page's offer, the audience numbers big and still with an "About
   these numbers" fold (80 from the feed; 130+ countries confirmed by the
   owner on 20 Oct; 100,000+ streams and 10+ years have no stated source, so
   `[to supply]`), and a link to the record attempt inside
   `<!-- v4:needs record-attempt.html -->` marks that `tools/v2_switch.py` drops
   while the record page is prototype-only. Run in the previous session as a
   workflow; if row 34 of the report is not there and nothing is pushed for it,
   start it again from this brief. `partners.html` is the shell (head, menu,
   footer) that the record, Expeditions and feed-option generators copy:
   leave those parts alone and prove their pages unchanged.
3. **The site-wide pass, only on**: home, podcast, library, knowledge base,
   topics, about pages. Episode pages are off the list for now (owner, 20 Oct).
   One page type at a time, screenshots to the owner after each, the way India
   was done (report: "India, less but better"). Topic pages are a template
   over about 50 pages: build the change in a tool, check a sample of pages,
   and prove the rebuild.

Then, before any switch-over: `tools/v2_episode.py` must read the live episode
header of 2 Oct. Done on 20 Oct (commit 19f4707f): a new episode builds again. Kenya's pass is paused by the owner; the
cheap option offered was removing only what breaks the motion rule (its hero
slideshow timer and the slow zooms).

## Found in the 21 Oct review
17 page types on desktop (1440) and phone (390), captured by scrolling a real
window one screen at a time and joining the screens (one tall full-page shot
breaks the pinned and scroll-driven parts), read by two agents and every
finding checked again by hand; sent to the owner as a page
(https://claude.ai/artifact/5oA3E1CrreKHtYgbopMXW3). No script errors.
- Fixed (a regression of row 36): the library's opening chart drifted over
  "Start here / All Series" on a phone; its drift now stops at the room left
  in the opening (`tools/v4_polish.py` LIB_JS).
- For the owner (content, also on the live site): topic pages promise a full
  transcript for every episode (`generate_tag_pages.py`, lines 331 and 363)
  while Safety has 29 of 30; the "New Technologies 3: Stephan Stiegler"
  description lacks a name ("the innovative designer from .",
  `episode-meta.json`; probably AirDesign); 80 episodes on some pages, 93 on
  others (both true: 80 in the feed, 93 with the 13 YouTube-only videos);
  Kenya's "Took It's First Steps".
- Proposed v4 fixes, built the same day (report row 45, commit e7398530; checked again in the browser on 21 Oct, all four in place): the podcast feed's failure message
  ("the saved archive is below instead", from `rss-feed.js`, with nothing
  below; v4 can replace it with a link to the library); a soft shadow behind
  the home opening's small orange line over bright snow; "carabiner" under
  the harness outline in the Brand Stories drawing; the topic pages' chart
  labels about 5 px on a phone.
- Not problems: Kenya's gallery and Expeditions' panels need a continuous
  scroll to load and show (a capture that jumps a screen at a time misses
  them); nine topics have no trend line because none of their episodes is
  dated; YouTube pictures are blank only where YouTube cannot be reached.

## Keeping the cost down (the owner asked, 20 Oct)
India took about 25 agents and three workflows for a 7.5-to-6 win. Most of
that was checking, not building. Next time:
- **Screenshot once, judge many.** Each blind judge re-walked both pages at two
  widths (about 150 tool calls and 180k tokens per judge). Instead, one cheap
  agent takes the screenshot set and the frame sequences once, for old and new,
  into labelled folders; the judges only look at them.
- **One judge for a small page, two only for a big one**, and never more than
  one fix round; a small fix after judging is made directly, without judging
  again.
- **Let the gates check what they already check.** Parity, links, words,
  overflow, tap targets and weight are in `v4_gates.py` and `v4_weight.py`; the
  checker agent only does what they cannot: the facts diff, the booking links,
  the motion rule.
- **One audit agent, not two**, and no per-frame probes, CPU throttling runs or
  thousands of frames unless something is actually janky.
- **Smaller models for mechanical work**: screenshots, diffs and measurements
  on a smaller model (the Workflow tool's `model` option); the planner, the
  builder and the judges on the main one.
- **Full gates once before a push**, `--quick` while iterating.
- **Content before polish**: the judges' main limits on India were the visible
  "From past pilots [to supply]", soft or repetitive photographs and a route
  that is only a diagram. The owner's quotes, best photographs, IGC logs and a
  sharp hero clip would lift the trip pages more than another round.

## How to work here
- Preview server: `python3 -m http.server 8765 --bind 127.0.0.1` from the repo
  root. For old-versus-new comparisons, a git worktree of the last pushed
  commit in `/tmp/claude-0/wt-old`, served on port 8766.
- `tools/v4_build.py` must keep reproducing the committed v4 byte for byte:
  in a clean worktree of the new commit, `./build.sh && python3 tools/v4_build.py`
  twice, then `git status --short prototypes/v4` is empty. Every new in-place
  pass (like `tools/v4_trip_calm.py`) goes in it after `v4_ux`. This check found
  a real bug on 20 Oct (the enquiry page's trip length).
- A page-only look goes in its own sheet and script loaded by that page alone
  (as `v4-calm.css` and `v4-calm.js` for India), so no other page's bytes or
  version hashes change.
- A new page with no live twin goes in `tools/v2_site.py` `NEW_PAGES`.

## Waiting on the owner
Photographs (a Google Drive folder works; Terabox is blocked), client quotes
for "From past pilots", the record page's FAI figures, wing and team, the
sponsor tiers and promises, the source and date of the 100,000+ streams, the
India and Kenya skill levels, whether the hero footage may loop, the iPhone
check and the switch-over.
