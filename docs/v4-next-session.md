# v4: handoff to the next session (25 Oct 2026)

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

## Chat 14 (25 Oct): the poster strip is in the home page
- The owner said "yes Poster strip into home": tools/v4_home_listen.py copies samples/listen-c (not listen-b).
- Contour lines fixed on the owner's screenshot: the map behind the strip has its own layer (will-change), since
  the posters' resting 3D tilt hid it above the cards; it peaks where the posters start; poster lines fade out by
  26% of the height. Known, left alone: img/contours.svg is not a seamless tile, so faint straight joins show.

## Chat 14 starts here (25 Oct): put the poster strip (listen-c) into the home page when the owner says yes
Chat 13 (all pushed, last 43eefad8, gates PASS):
- **The podcast section is in the home page** (`tools/v4_home_listen.py` copies PART 2 of
  `samples/listen-b/index.html` in place of #listen and #map; run it by hand after a change to the sample, then
  commit both). `tools/v4_polish.py` no longer leans the home rail's cards. The sample sets `--hf`/`--nf` once
  (styles.css still sizes the old plate's words by them; without it the switch dry run fails its token check).
  The globe box keeps `id="map"`. Play still needs checking on the owner's device.
- **The call band stays and arrives** (samples/departures, copied by tools/v4_home_departures.py): the glow opens
  in the middle and settles top-left, the line draws, the words rise; words on the rows' edge, buttons level with
  the title, an --sp-4 gap; on a phone the season line runs to a ring at the call.
- **The poster strip, preview only:** `samples/listen-c/index.html` (live at
  https://paraglidingatlas.com/prototypes/v4/samples/listen-c/), listen-b with the "More conversations" cards as
  posters again: each guest's own art in colour (a step darker at rest), hook and name in live type on the art
  (no plate image, no compass), a deep fade into the page dark, the lean with a soft light, a line per card to
  its real length with chapter ticks, arrows in the heading row, a progress line under the strip, the strip
  drifting on its own again (v2-immersive.js data-auto), faint contour lines (img/contours.svg) on the red above
  each head, lined up with one map behind the strip that fades out into the section; the lead trip's pictures in
  colour; "15 guests, newest first". The owner tried and rejected a small compass dial and a big compass rose
  ("looks odd"). Chat 13's generator was in its scratchpad (gone); the sample itself is the source now.
  **Next:** when the owner says yes, copy listen-c into the home page (point tools/v4_home_listen.py at
  samples/listen-c, rerun, build, gates).
- **One width across the site** (owner: "go with 1"): above 1440px every page uses the opening's 72px edge
  (src/v2.css "ONE WIDTH ACROSS THE SITE"). Up to 1440px nothing changed. Left as designed: the knowledge base
  climb's staircase, the partners journey's spine, full-bleed photos, maps and rails. The library page follows
  through the shared stylesheet only (its files are the other chat's; nothing in them was edited).
- **Designers:** their definitions now carry the owner's "professional standard" (homework first, no rule
  stretched past its section, weigh immersion before simplifying, own the whole site).
- **Build note:** a change to src/v2.css changes the ?v= stamp on every page; build once, commit the rebuilt
  pages, then the clean double rebuild.

## Chat 13 starts here (25 Oct): build the podcast section into the v4 home page
Chat 12 did the seven steps (below) and then, with the owner and the three designers, designed the
section after the departures. The owner's choices, in order (also in docs/designers/direction.md):
no cursor shine on the departure rows; option B, Turnpoint's "Hear Where We Fly", #listen and #map
merged into one section; refined (one calm card look: grey pictures, colour on hover, no compass, no
YouTube red; one India heading; "More conversations, Newest first", no "most streamed" claim; the phone
globe fits; "Find it on the globe"; a still orange route on the globe in season order, hollow pins for
Kazakhstan and Peru); then a lead: the lit trip leads with its big name, dates, play in place (the
youtube-nocookie embed loads only on tap) and Trim's chapter line, the globe turns to a picked trip and
lights the route to it; no footage ("Except 2, 1 & 3"); last, the globe leads the stage (about 720px on the
right, one plain ring, legend and caption one line under it, zoom inside its square), the episode picture
small (240px) and growing on play. The owner: the globe "will most likely be replaced by the Encarta
concept globe later on", so only its place and look matter now.
- **The preview:** `prototypes/v4/samples/listen-b/index.html` (live at
  https://paraglidingatlas.com/prototypes/v4/samples/listen-b/), last at bfb126d9, gates PASS. Turnpoint's
  rebuild scripts were in chat 12's scratchpad (gone with the container); the sample itself is the source.
- **Next (not yet asked):** the owner had not yet said "build it into the home page". Ask once, then do it
  like `tools/v4_home_departures.py`: a tool copying the merged section from the sample into
  prototypes/v4/index.html in place of `<section id="listen">` and `<section id="map">`, with the chain
  checked (v4_ux, v4_polish, v2-home.js rail code, the globe scripts, smoke tests on #listen or #map).
- **To check with the owner:** play on a real device (YouTube is blocked in the container, so the playhead
  and the exact length from the player are untested); the chapter titles in episode-meta.json were written
  from transcripts and marked for review; sharper guest portraits would help (the face crops come from each
  episode's YouTube art, to keep "no photo used twice"); the source of "most streamed" if it is to come back.
- **Worktree note:** a designer run with `isolation: worktree` leaves full copies under
  `.claude/worktrees/`; the audit and the switch dry run then scan them and FAIL. Remove them
  (`git worktree remove --force`) before gates. Chat 12 put `.claude/worktrees/` in `.git/info/exclude`.

## Where chat 12 left it (25 Oct): the seven steps are done and pushed
- **Step 1 (301b80d1): option A is the home departures.** `tools/v4_home_departures.py`
  (run by hand after a change to `samples/departures/index.html`; the build
  keeps what it wrote) copies the sample's `<style>` into the head and its
  `<section id="destinations">` (season line, nine rows, call band, small
  script) in place of the fly-by, line of months and table, between
  `v4-home-departures` marks. `tools/v4_polish.py` counts the Destinations
  from the `.sl-row` rows and no longer draws the old line (`v4p:tl`);
  `v4_ux` home_flyby_weight and `v4_phone_media` flyby() find no fly-by and
  do nothing; the fly-by's phone cuts (`img/hero/home-*-p`) are deleted. The
  home page has no video now, so v4_footage drops its pause script there.
  No JavaScript shows the whole list (checked at 1440 and 390); the phone
  card's "Today" reads the sample's 24 Oct 2026 until the script sets it.
- **Step 2: the phone opening.** On a phone (sample, then
  `tools/v4_home_opening.py`) the headline comes up under the route, the
  trip panel follows with its button, "You fly" moves under the button, the
  kicker and "Listen to the podcast" go last; the panel no longer fades as
  the page scrolls (`.dock{opacity:1}` on phones) and the trips' grid no
  longer stretches to India's height. At 390x844: headline 456 to 510 px,
  the trip button 723 to 811 px for every place (was 842 to 957).
- **Step 3: text and targets.** Readout labels, month letters (desktop and
  phone), route names on a phone, the swipe hint and hints 11.2 to 12.5 px
  (route names lose their letter spacing under 360 px, so KAZAKHSTAN clears
  PERU at 320); the pause button is a 44 px target, still dim, no ring. The
  departures' small labels went up the same way.
- **Step 4: the call band** reads "(Kenya, Panchgani, India, Kazakhstan or
  Peru)" on home and the three trip pages (tell the owner).
- **Step 5: Panchgani.** Vistasp Kharas's episode lists Panchgani first in
  Fly With Us (price `[to supply]`); About has a fifth card ("Panchgani ·
  Sahyadri hills", "The Sahyadri Tablelands", from the page's own title)
  with the contour pattern instead of a photo (its one photo is used three
  times already), five cards in a row from 1101 px.
- **Step 6: no JavaScript.** Kenya's five fly chapters each show their own
  photo under their words (noscript copies, India's v4-calm way, in the
  page's own `<style id="v4-kenya-own">`). The home rows and "Join The Atlas
  List" show without JS at 1440 and 390 (the old hidden rows went with step 1).
- **Step 7: Kenya's drift.** On Kenya `--font-mono` is the body font and
  `--orange-lite` the one orange (page-only, so the library's mono stays);
  `src/v2.css` gallery, route, 404 and altitude whites are `var(--white)`.
- **Listed, not done:** the pilot cut-out's grey rim and the shadow blobs in
  the opening need image work (re-cut masks); not tried, to keep it clean.
- **Next:** offer the owner a new Juror review with its estimate (one page at
  two widths about 3 to 6 min and 60k to 120k tokens; site-wide about 20 min
  and 150k). The scheduled task "Chat 12: carry on the v4 plan" is disabled.

## Chat 12 starts here (25 Oct): the owner said "do what you can yourself"
After the steps below the owner had the three designers (now named Trim = D,
Cloudbase = E, Turnpoint = F; `docs/designers/README.md`) and a new fourth
agent, the Juror (`.claude/agents/awwwards-juror.md`), look at the home page
and the whole site. Their write-ups are in the designers' notebooks
(`docs/designers/D.md`, `E.md`, `F.md`, `juror.md`, newest at the top).
- **The Juror's rule (owner):** "use only after checking with me the
  prediction of time and turn expenses". Tell the owner the estimate first
  (one page at two widths about 3 to 6 min and 60k to 120k tokens; the
  site-wide review took 19 min and 150k) and wait for their yes.
- **The Juror's scores** (v4 at 48bfc475 before the opening went in, against
  v4 now): 7.14 then, 7.83 now out of 10 (Design 8.2, Usability 7.3,
  Creativity 8.3, Content 7.0). About 8 usually wins Site of the Day.
- **The next home section, option A "One Line, Two Postures"** (the
  designers' majority pick after two rounds): the opening's season line
  carried down across the top, matched to the pixel; the nine departures as
  rows under it, each with a thin bar at its real dates (planned dashed), the
  place last shown in the opening lit orange; pointing at a row flies the
  glider to its bar. Phone: the line upright in the left margin, one card per
  departure, the orange track drawn by scroll (CSS scroll timeline) with the
  glider on its tip. The fly-by and the sideways line of months go; the call
  band stays. Preview built by Turnpoint as a full copy of the home page:
  `prototypes/v4/samples/departures/index.html` (live at
  https://paraglidingatlas.com/prototypes/v4/samples/departures/#destinations).
  Option B (Cloudbase's: rows unfold out of their bars as you scroll) was not
  chosen by the majority.
- **"Do what you can yourself" (owner, 25 Oct)**, chat 12, in this order,
  each step with gates and a push:
  1. **Build option A into the v4 home page** in place of
     `<section id="destinations">` (the fly-by, the line of months and the
     table). Make it a tool like `tools/v4_home_opening.py` that copies the
     section from the sample. Watch the chain: `tools/v4_polish.py` reads the
     departures (`a.v2-dep` rows) for the home line of months and the
     Destinations figure and stops if they are gone; `tools/v4_ux.py`
     home_flyby_weight and `tools/v4_phone_media.py` flyby() read the fly-by
     (the phone cuts `img/hero/home-*-p`). Keep the departures' data (one
     list, the rows) so the passes and v4_polish can read it, or move them to
     read the new rows. No-JS must show the finished list.
  2. **The phone opening** (all four found it): on a 390x844 phone the
     opening's trip button sits at 824 to 871 px (was 560 px), the headline
     "Paragliding Expeditions, Run By A Pilot." starts about 964 px down, and
     the trip panel fades to black after about 200 px of scroll. Put the
     headline and button inside the first screen, hold the fade until the
     panel has scrolled past (sample, then `tools/v4_home_opening.py`, then
     the build).
  3. **Small text and targets** (Juror): readout labels 9.9 px, phone month
     letters 9 px, the route hint 11 px: none under 11 to 12 px; the pause
     button a 44 px touch area (it can stay dim).
  4. **The call band** says "Ideal tour match ... (Kenya, India, or Peru)" on
     the home page and the trip pages: make it the five places (Kenya,
     Panchgani, India, Kazakhstan or Peru); tell the owner.
  5. **Panchgani where it is still missing** (Cloudbase): the Panchgani
     episode's "Fly With Us" box and About's place cards.
  6. **No JavaScript** (Cloudbase, Trim): on the home page the departure rows
     and "Join The Atlas List" are hidden without JS (the fly-by goes with
     step 1); on Kenya's page the five chapter sections are black without JS.
  7. **Kenya's page drift** (Trim): DM Mono as a third font, an off-token
     white and a second orange; use the tokens and the two fonts.
  Then ask the owner (with the estimate) whether the Juror should score again.
  Not decided by the chats: keep `[to supply]` visible (the owner's standing
  rule: a missing fact shows as `[to supply]`; the Juror would hide empty
  fields: put that to the owner, do not change it). The pilot cut-out's grey
  rim and the shadow blobs in the opening (Juror, Trim) need image work: try
  only if it can be done cleanly, otherwise list it.
- **Still waiting on the owner:** Panchgani's and Kenya's launch heights and
  prices, Panchgani's group and rating; "Guaranteed to run, 6 places" for all
  four India 2027 departures; Peru and Kazakhstan dates; a second Panchgani
  photo; the big-wing Kenya photo, if any; India JPGs under 10 MB; a JPG of
  DSC_6210; the live episode chart and the five Kenya repeat photos; the
  switch-over (it changes the live home h1).

## Where chat 11 left it (24 Oct): Panchgani has its page and is across v4, the phone fixes and the review are done
- **Step 4 done (01505966, gates PASS): Panchgani's page**
  https://paraglidingatlas.com/prototypes/v4/destinations/panchgani.html, by
  `tools/v4_panchgani.py` (run by hand, then the build; it writes the page from
  the v4 Kenya page's frame, and `img/panchgani/plateau.jpg|webp`, the
  opening's ground with its wing put back). Hero (one photo, no rail, the
  credit on it), jump row, facts (launch, rating, group, price `[to supply]`),
  overview and six questions from Vistasp Kharas's episode (each fact his, or
  the owner's dates), one departure card (Hold a place with
  `?trip=panchgani&when=14+to+21+February+2027`), the episode, the call band,
  the booking bar. A small script lights the dates band (Kenya's overview
  script does it there). `tools/v4_ux.py` TRIPS and `tools/v4_phone_media.py`
  take Panchgani as a third trip (the phone cut `img/hero/panchgani-plateau-p`);
  v4_ux's trip_dates_first skips a page with no route or gallery, its price
  regexes allow `<b class="v2-tbd">`. `tools/v2_site.py` NEW_PAGES lists
  `destinations/panchgani.html` (no live twin: the switch writes it, indexable,
  into the sitemap); its canonical and og:image are the addresses it will have
  (`/destinations/panchgani.html`, `/assets/v4/img/panchgani/plateau.jpg`).
  The opening's Panchgani button is "See the Panchgani trip" (sample, then
  `tools/v4_home_opening.py`, then the build; the build title-cases the home
  headings, so commit its output).
- **Step 5 done: Panchgani across v4.** `python3 tools/v4_panchgani.py links`
  puts "Panchgani Tour" after Kenya in every footer (not samples, not
  library.html: the library is the other chat's); v4_build runs it after the
  encyclopedia's pages, which are rebuilt from a source without it. Phone menu
  (`src/v4-menu.js`), enquire's trip list, the sitemap (a fifth trip in its
  SITEMAP_SKY tree, thumbnail `img/panchgani/plateau-thumb.webp`, five
  positions in `tools/v4_sitemap_sky.py`; India's line now "April to May,
  October to November"), the home departures (a row after Kenya, "Dates set",
  group and price `[to supply]`; v4_polish draws it on the line of months),
  the expeditions page (`tools/v4_expeditions.py`: five places in the
  season's order, Panchgani 02 without a photo, words cap 450; year labels
  carry months only, Kenya's ends at its last departure, India's ends with
  October where Peru's begins, and on a phone Kazakhstan's and India's are
  nudged apart), and Fly it yourself on the Panchgani episode
  (`tools/v4_pass.py` TRIPS).
- **Decided without the owner (tell them):** Panchgani's only photo appears on
  the opening, its page hero and the sitemap thumbnail; the home fly-by and the
  expeditions page leave it out rather than repeat it again. A second
  Panchgani photo would fill both. Panchgani's status reads "Dates set" (not
  "Booking open", which the owner has not said).
- **Step 6 done: the opening's two phone faults.** (1) The route's label
  boxes (`.tp`, 4.6rem wide on a phone) overlapped: Panchgani's took taps on
  Kenya's marker, a neighbour's took the end of India's and Kazakhstan's
  names. Now `.tp{pointer-events:none}` and only `.tp-n` (its own width,
  padded 8px 4px, placed as before) and `.tp-r` (a 7px tap ring) take taps;
  checked by elementFromPoint at 320 to 1440 px (one ambiguous 4px edge at
  320, where the two markers are 13px apart). (2) The swipe: the old code let
  every slow short swipe through (before the next photo was ready, any 40px).
  Now the speed is over the last 60 ms (`drag.hist`), zero if the finger
  rested 90 ms before lifting, a flick needs 0.45 px/ms and 8% of the way,
  and the no-photo path needs the same third (W * 0.62 * 0.3) or a flick.
  Tested by in-page PointerEvents on a timer (CDP touches arrive ~100 ms
  apart, too slow to flick): slow short, twitch and rest spring back; flick
  and long go. Headless frames lag once WebGL runs, so the ready path reads
  every swipe as slow there; check it by hand on a phone.
- **Step 11 done: the final review pass.** 19 main pages at 1440 and 390 px
  (home, expeditions, the three trips, podcast, knowledge base, library,
  the Panchgani episode, enquire, about, sitemap, mission, record, topics,
  the Atlas, partners, 404, terms): no script errors, no sideways scroll, no
  broken image, no failed request. Hold a place from Panchgani opens enquire
  on its departure; its price now shows as the to-supply mark
  (`tools/v4_ux.py` HOLD_JS). The only new check warning is Panchgani's "no
  live twin", expected. The scheduled task "Chat 11: carry on the v4 plan" is
  disabled: every step that does not wait on the owner is done.
- **Waiting on the owner:** Panchgani's and Kenya's launch heights and
  prices, Panchgani's group size and pilot rating; whether "Guaranteed to
  run, 6 places" applies to all four India 2027 departures; Peru and
  Kazakhstan dates; a second Panchgani photo (for the home fly-by and the
  expeditions page); which big-wing Kenya photo, if any; full-size India JPGs
  under 10 MB; a JPG of DSC_6210; the live episode chart and the five Kenya
  repeat photos; the switch-over (it changes the live home h1 to
  "Paragliding expeditions, run by a pilot.").

## Where chat 10 left it (24 Oct): the opening is the v4 home hero, India is in 2027 everywhere; chat 11 builds Panchgani's page
Live (17f53b72, gates PASS): https://paraglidingatlas.com/prototypes/v4/samples/opening/
- **The move between places is E's** (owner: "build E only"): the camera flies
  forward into a cloud and out of it over the next place (`flight()`,
  `flyCSS()` for no WebGL with the `.veil`, shader `flyAt`/`flyCover`, uniforms
  `uFly`, `uFlyB`, `uCloud`, `uFlyO`, `uWordS`; 1.4 s, `easeFly`); the season
  glider lifts a few px on the leg (`--ga`). The orange wipe is gone. D and F
  were built (scratch only, never pushed) and dropped.
- **Skip** (owner): a click on the progress line fills it in 0.32 s and the
  next place flies in, paused or not (`.skip` button over the line, `skipping`).
- **Peru back to Kenya** on autoplay: forward round the season (`autoWrap`,
  `trans.wrap`, glider fades at the ends, `--go`).
- **No photo switch** (owner): `.kpick` and the `#india` jump removed; Kenya
  defaults to DSC_9492 (`pick` default map; `?kenya=9452|9522`,
  `?india=redwing|launch` still reach the others). No-JS still shows the 9452
  layers: hard-wire 9492 when building into the home page.
- The owner's other chat (session_01DCHUF6z6Tm2mvyLyj9PbTP) pushed the play
  button without a ring and three standing designers (`.claude/agents/designer-*.md`,
  `docs/designers/`); the owner: "those pushes have to stay". Record design
  decisions in `docs/designers/direction.md`.
- **The owner said "go autonomous"** at extra high effort: carry on without
  asking, through usage resets (a scheduled task in this session wakes it),
  steps in this order, each ending with gates and a push:
  2. **Done (f47d960e, gates PASS): the opening is the v4 home page's hero.**
     `tools/v4_home_opening.py` (run by hand after any change to the sample,
     then the build) copies `samples/opening/` into `index.html`: photo layers
     to `img/opening/`, the hero between `<!-- v4-home-opening -->` marks
     (replacing the old kit-hero, its footage and the ridge drawing; so
     `tools/v4_opening.py` has no place any more), styles fenced to `#held`
     (classes on <html> renamed `op-*`, keyframes `op-*`, the kicker
     `op-kicker` because the site greys every `.kicker`, the site's slanted
     `.btn-solid` box undone), the site's nav lying over the photo, the script
     loading from `img/opening/`. The build title-cases the headings. v4_polish
     skips its figures when the old hero is gone. `tools/v2_check.py` EXEMPT
     now lists the home h1 ("Paragliding expeditions, run by a pilot.") as
     the owner's deliberate change from the live "Touch The Sky With Glory":
     **tell the owner this changes the live h1 at the switch-over.**
     The sample is the single source; Kenya is fixed to DSC_9492 there.
  3. **Done: India's 2027 dates everywhere in v4** (four departures, 15 to
     24 Apr, 25 Apr to 4 May, 21 to 30 Oct, 3 to 12 Nov 2027).
     `tools/v4_india_2027.py` (idempotent, run by hand) moved the pages: the
     India page (two season bands, spring and autumn; four cards; strap, FAQ,
     terms, structured data; "Next departure 15 Apr 2027"), the home
     departures (by month, dated before planned) and fly-by, every episode's
     Fly With Us (Kenya first now), the Fly it yourself links, About. The
     generators carry the dates (v4_expeditions*.py with a cross-month
     departure, v2_fly_options, v2_episode, v4_pass TRIPS, v4_trip_calm
     BIG/QUIET, which now expects four flags). v4_polish's line of months
     reads a departure that crosses a month. The India search description is
     the owner's fact (`tools/data/v4_facts.json` india_2027), accepted by
     v2_check's parity. Carried over, not confirmed by the owner: "Guaranteed
     to run" and "6 places" for all four (as the opening already says), and
     the booking terms line now just points to the terms (the 120-day rule
     no longer fits). Never run `tools/v2_fly_options.py` without `--site v4`:
     it writes prototypes/v2 (reverted once in chat 10).
  4. **Next (chat 11 starts here): Panchgani's destination page**, then its
     button in the opening points there (edit `samples/opening/index.html`,
     run `tools/v4_home_opening.py`, then the build). Only India and Kenya
     have pages (live and v4); Panchgani's has no live twin (v2_check warns
     "no live twin", fine). Plan scoped in chat 10: a generator
     (`tools/v4_panchgani.py`) that takes the v4 Kenya page's shell (head,
     nav, footer, the dst-* section classes) and writes
     `destinations/panchgani.html` with: hero (the opening's Panchgani layers
     in `img/opening/`, credit "Photo by Michael Gebert /
     @flywithandy_paragliding"; the only Panchgani photo, so it repeats the
     opening's: note it to the owner), facts (14 to 21 Feb 2027, 8 days,
     17.92°N 73.82°E, Sahyadri hills; launch, price, group, rating
     `[to supply]`), overview and FAQ from the episode
     `episodes/navigating-panchgani-vistasp-kharas.html` with Vistasp Kharas
     named (take-off about 1,100 to 1,200 m; 3,000 to 4,000 m in peak season;
     two hours from Pune, four and a half to five from Mumbai; volcanic
     plateaus of the Deccan, sharp cliffs, flat tops; evening coastal winds
     time the window; season November to March, the wind turning from
     north-northeast to southeast; strong, punchy thermals, SIV advised, EN-B
     fine; Panchgani to Kamshet about 100 km; the pre World Cup), one dates
     card (Hold a place, `enquire.html?trip=panchgani&when=14+to+21+February+2027`),
     the episode as "from the show", the call band. Keep the facts row's
     launch `[to supply]` (the owner's number), quote the episode elsewhere.
  5. Panchgani in the rest of v4 (expeditions pages, the home departures and
     fly-by, enquire's trips and v4_ux `TRIPS` for hold data, sitemap, map,
     nav where destinations are listed). Reorder the expeditions generators'
     PLACES to the season (Kenya, Panchgani, India, Kazakhstan, Peru) then.
  6. Small fixes: on a phone India's label covers the Panchgani marker; a
     short swipe on a phone went through as a flick (check it springs back
     below a third when slow).
  11. A final review pass of v4 on phone and desktop.
  Skip what waits on the owner (facts, photos, the episode chart, the
  switch-over) and list it at the end. Never touch the library's files.
- Testing tip: headless screenshots are too slow to catch a 1.4 s move; slow
  the page clock (`performance.now` scaled after load) to take frames.

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
- **The three standing designers** (owner, 24 Oct: "how can we have access
  to 3 master designers all the time so it doesn't get confusing, because
  every time we switch I think it's a loss of direction"): `designer-d`,
  `designer-e`, `designer-f` in `.claude/agents/`, their memory in
  `docs/designers/` (`direction.md`: the brief and the owner's decisions, keep
  it current; `D.md`, `E.md`, `F.md`: their notebooks). Use them for every
  design question. The owner was given a prompt for chat 8 so the original
  three write their own notebook entries; if chat 8 has pushed them, read
  them first.
- **The play button and the line** (24 Oct): no ring, dim until hovered, a
  small gap before it; the progress line at 75%.
- **Chat 10 starts here, in this order** (owner, 24 Oct, asked whether the
  opening should replace the v4 home page's own opening: "do it"):
  1. **Build F2 into the v4 home page** (`prototypes/v4/index.html`), in
     place of its current opening: the source is
     `prototypes/v4/samples/opening/index.html` (the same as the review page's
     F2/index.html; its page links carry `../../`). The home opening is made
     by `tools/v4_polish.py` (`home_markup`, HOME_CSS, HOME_JS); the assets
     go into `prototypes/v4/img/` (never `assets/`). Keep F2 as it stands:
     the season route with Panchgani and India's four 2027 departures, one
     pass then the next place, the progress line with play and pause, the
     real-size Panchgani wing and its left turn, the DSC_9492 follow shot
     (`?kenya=9492` picks it in the sample; in v4 make 9492 Kenya's photo, as
     the owner chose option A for it) and drop the review-only photo switch
     (`.kpick`). The rest of the home page stays. Use the site's own fonts
     (`prototypes/v4/fonts/`), not Google Fonts, and the design tokens.
  2. **India's 2027 dates everywhere in v4** (next point).
  3. Then Panchgani's own destination page and the rest it needs (owner:
     "it is a proper tour which will need to have all its necessities like
     other destination pages"), and its button changes from the episode to
     that page.
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
- **Play and pause** (owner: "give a subtle yet elegant and sleek play pause
  button for those who want to stay on the image"): a 30 px ring at the right
  end of the progress line (`.play`, shown only with `.auto`), the line stops
  46 px short of it. Pause holds the place and its move still (`paused` stops
  both `dwell` and `pushClock`); play goes on from there. Both copies (F2 and
  `samples/opening/`).
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
