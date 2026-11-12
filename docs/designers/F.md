# Designer F, "Fly the Season": notebook (newest first)

## 12 Nov 2026: the phone photo viewer's controls, "The Task Line" (chat 23)
**Asked.** Brief `docs/designers/viewer-controls-brief.md`: the gallery viewer's controls one-handed and Awwwards level, sleek and
futuristic, not boxes and not chat 23's glass capsule ("the buttons still look odd to me"). One sample each from D, E, F.
**Proposed** `prototypes/v4/samples/viewer-f/` (index.html, phone.png, desktop.png). The controls are the task line itself: one
line of ticks, one per photo in the task, a fisheye swell round the site's glider (the gallery's gf-line grammar), "21 of 144"
riding above it; prev and next are the line's two arrow ends; drag the line to scrub to any photo (a light 800 copy follows the
thumb, the 1600 on release; role="slider", Home/End). Under it plain lit type, no fills: Download (orange arrow onto a base, the
readout "1600 x 2400 px · 891 KB", real fetch progress as a glowing underline, then a check and the file name), Share (the
site's icon, share sheet else link copied), "Like what you see? Join me on Patreon" with an orange arrow. Pressed = a soft orange
light pool under the glyph and the glyph nudges (no shape appears). Name, task, date, close in the row above; the licence line
under. All in the bottom 240 px of 844, beside the photo, not over it. Tap the photo hides the controls; swipe sideways steps,
down closes. Desktop: the same line centred in one low bar, id and licence left, actions right, close top right, the photo's
sides click to step. A States board (behind Close) shows Download ready / getting it / saved and the pressed states.
**Recommended** it because stepping, "where you are" and progress through the task are one control the thumb can slide, and it
is the gallery's own line, so the viewer reads as the same site rather than a widget.
**Checked** 390x844 and 1440x900 (file://): no console errors, no sideways scroll (two found and fixed: the panel grid's 1fr
and the specimen light pools), Download fetched and saved SRS_6_T4_54.jpg, scrub lands on the real photo, reduced motion
(no glides or pools) and no JS (the line and actions still drawn).
**Flagged.** Real sizes after the site's JPEG step are smaller than the brief's example (T3_21 891 KB, T4_54 826 KB). Pinch
zoom is not in the sample (the site's v4-gallery.js keeps it). The sample's prev/next joins the two brief photos; on the site
they step through the task.

## 12 Nov 2026: the first newsletter, contest round 1, "The Task Line" (chat 22)
**Asked.** Brief `docs/designers/newsletter-brief.md`: the first email to all subscribers (28), a mix of the owner's
first-person opener and brand sections; concept `docs/designers/newsletter/F-concept.md`, a static email-safe mock
`prototypes/v4/samples/newsletter-f/` (index.html, img/, shot-390.png, shot-1440.png). No MailerLite writes.
**Proposed.** The email as a task board in the site's grammar: masthead (welcome email's orange rule), the owner's
cover photo SRS_6_T1_62, "Four Tasks Into Tapalpa" with a four-fact readout, the opener with the portrait, the 2026
season line at scale (Tapalpa orange) and four season rows with one link each, then Tapalpa task by task (square
poster, date, km, the film's own line, winner and goal count from SRS, "Watch m:ss | N photos" to the site's film
theatre), the provisional top 3 (with a link to Bill Belcourt's episode, he is second), "Find Yourself In The Photos"
with the one filled button, the Miguel Gutierrez talk (frame from the owner's video), Patreon as an outline button,
sign-off, honest footer. Subjects: "Four tasks into Tapalpa" / "From the media team at SRS Tapalpa"; previews:
"82.4 km and nobody in goal. The photos, the films and the rest of my season." / "484 photos free to save, three
highlight films and a talk with Miguel Gutierrez."
**Recommended** subject A and preview A, because they are true, short and name the place readers know.
**Checked.** SRS scores T6.1 to T6.4 (goal counts 26, 1, 88, 0; Duffy 65.6 km), overall top 3, photos.json (484:
P 19, T1 99, T2 54, T3 144, T4 168), YouTube (Miguel yhHoRUJtyOY 53:23; no Task 4 film yet). 390 and 1440: no errors,
no sideways scroll; images off still reads.
**Flagged.** Miguel talk not in the repo and "Maxico" in its YouTube title, its description links a Google Form for the
newsletter; Task 4 film [to supply]; PWC and Bassano pages not live yet; countries 44 vs 25 (left out); postal address
for the footer [to supply]; Gmail iPhone dark-mode inversion for G to test.

## 12 Nov 2026: event landing pages, the winner built for real (chat 22, branch claude/chat22-events)
**Asked.** Build "The Season Opens Here" (won round 1) in the site's tools, with E's films-only chapter rows and season-foot pictures and D's two rules (a 16:9 film frame stays 16:9 on a phone; Piedrahita's Day 1 film is not Task 1's, posters are photos of the same task). No commit, no build or gates (the chat runs them).
**Built.** `tools/v4_comp_gallery.py`: per-comp switch `COMPS[c]["landing"]` (absent = off; the name `event` was taken by the official-event link, and chat 21 asked that the tapalpa dict stay untouched). On: `landing()` swaps the gallery's lead for `opening()` (giant place name, readout, "325 photos, 3 films", official link), puts `season_strip()` (2026 line, this event lit, fan into the task line, phone prev/next row) over the task line and `season_foot()` (every event a row with its picture, dates on its rule, one link) before the organiser band. Films-only comps (`stops` instead of photos): `render_films()` / `page_films()`, each stop its films as `chapter()`s (16:9 frame playing in place via v4-media.js, kicker, title, length, views, date out, episode, YouTube), a missing film a dashed 16:9 slot with `[to supply]`. Piedrahita: Day 1 its own stop (state "film", "1 film, no photos this day"), films as Tapalpa's bands with photo posters (my pick: SRS_5_T1_10, SRS_5_T2_99; Day 1 a frame of its own film). New pages `media-pwc-pegalajar-2026.html`, `media-srs-bassano-2026.html` (NEW_PAGES; owned()/OWNED_GIT already take media*.html). Season from ONE place: `tools/v4_media.py season()` over SEASON + UPCOMING (new keys page, go, nick, pic). Media page rows now open the event pages. Shared code in new `v4-event.css/js` (not v4-gallery.css/js: Tapalpa's page carries their ?v= hashes, so touching them would change its bytes).
**Checked.** Tapalpa regenerated before and after: byte-identical. 390x683, 390x844, 1440x900 on the three event pages and Media: no console errors, no 4xx (served from the repo root: the pages reach ../../ files), no sideways scroll (one found and fixed: page() still counted days the old way, --n was 3 for 4 stops); reduced motion and no JS finished. Stop switching, #task-2 hash, play in place, a left stop's film stops, Day 1 state "film", "3 films" opens Day 1.
**Recommended / flagged.** Owner to pick posters and frames (PWC frame grabs, Bassano YouTube thumbnails with baked text and one reads "TASK CANCELLED" for Task 4 part 1, Piedrahita Day 1 frame, my two Piedrahita posters); PWC and Bassano comp dates, pilots, countries, official links; PWC Task 3 and Bassano Task 1 (flown? film?); the PWC film-frame opening is soft at 1440 (a 1280 frame): a 2400 still from the footage would fix it.

## 12 Nov 2026: event landing pages, contest round 1, built `samples/event-f/`
**Asked.** Chat 22, brief `docs/designers/event-brief.md`: each event on the Media page gets its own immersive, easy landing page; one full direction each (D, E, F), a working sample (Piedrahita `index.html`, PWC films only `pwc.html`), screenshots, concept `docs/designers/events/F-concept.md`.
**Proposed: "The Season Opens Here".** The landing page IS the gallery page (same URL, same `v4-gallery.css/js`, viewer and photos), with a taller opening (giant place name, readout, "325 photos, 3 films"), the 2026 season line at its foot (four events at their real dates, this one lit orange, the others links; on a phone a prev/next row), and an orange fan with a soft light from the lit dates down to the ends of the task line. Foot: "The 2026 Season" rows, each event's dates on its row rule, "You are here". Films only (PWC): the same template, the line is the film line (Day 1, Tasks 1, 2, 4, 5 with length and date out; Task 3 hollow, "No film", `[to supply]`), one 16:9 screen per stop playing in place (`md-frame`, v4-media.js); opening on a frame of the owner's film (Task 4's relief map with the task in red, darkened). Signature: on arrival the lit dates open into the task line (fan, track grows out of the bar, turnpoints drop in, glider appears), once, about 1.2 s, WAAPI transform and opacity; frame count at 4x throttle same as the page without it. Generator `samples/event-f/build_f.py` (from today's Piedrahita page, paths +../../).
**Recommended** that, because a pilot gets their photos with no extra tap and the shared URLs keep working, and the season line is the event menu in the site's own grammar.
**Checked** 390x683, 390x844, 1440x900: no console errors, no sideways scroll; stop switching, play in place, a hidden stop's film stops (both pages), hash opens a stop, no JS (stacked, finished), reduced motion (no animations).
**Flagged.** PWC Day 1 thumbnail reads "12.05.2027 - 23.05.2027" (year?); PWC comp dates and Task 3 `[to supply]`; posters are YouTube frame grabs, owner to pick stills; Piedrahita task dates unknown and its films still on designed thumbnails; v4-gallery.js would say "Photos coming" on a films-only page (needs a "film" state); Bassano has no page.

## 4 Nov 2026: the comp photo gallery, round 2, built `samples/gallery-f/`
**Asked.** Read D's "Proof Sheet" and E's "Pull Back to the Comp", answer them, steal with credit, build a Tapalpa sample with Piedrahita stand-ins. **Built** `prototypes/v4/samples/gallery-f/` (index.html, gallery-f.css, gallery-f.js; generator scratchpad `gallery/build_f.py`, shell from the Piedrahita page, ALT lines fixed in the generator because that page changed at 17:30). Shown as 11 Nov (`data-on`; `?on=` for other days; `?paid=` for the return from paying). Line sticky under the nav (transform only, once stuck); glider by the Web Animations API on transform; one day at a time (no JS: all stacked); justified rows, no crop, mean-colour cells; viewer from v4-media.js viewer() with the day as its set, 1600 on open, 2400 on zoom; Save fetches the 2400 copy (share sheet on touch, named download on desktop, "Tap again" if the share times out); Original sheet with Copy name and Pay [to supply]. Taken from D: dim never hide, colours from alts, mean colour, back to the last cell. **Checked** 390x683, 390x844, 1440x900: no console errors, no sideways scroll (the glider rail and the chips row overflowed at first; fixed). Reduced motion: no moves of mine (the 4 left are the site's v2-img-in). **Not proven:** glider smoothness on a real phone (a 4x throttled Playwright video drops frames, so it could not tell).

## 4 Nov 2026: the comp photo gallery, round 1 (concept only, nothing built)
**Asked.** Chat 19, brief `docs/designers/gallery-brief.md`: one gallery page per comp (Tapalpa first, then rebuild `media-srs-piedrahita-2026.html`), browse by day, find yourself, open big, free download of the 2400 px web copy, EUR 1 original by a per-photo payment link ([to supply]), delivered by hand. Owner away 4 h, asked the three to brainstorm. Wrote `docs/designers/gallery/F-concept.md`.
**Proposed: "Fly the Comp".** The season line shrunk to one comp: the task days at their real dates (8 to 14 Nov), states counted in the comp's time zone (flown, today "photos tonight", passed "photos coming", not flown, to come), task numbers from the owner's list, not the date. The newest day open under it, one day at a time (no JS: all days stacked). Photos in shot order, justified rows, wing colour chips (one keyword per photo at the cull, about 3 minutes a night), optional "where" label per batch. Viewer: the day as its set, 1600 on a phone, readout bar with the file name, Save, free (share sheet on phones, fetch to a named file; GitHub Pages sends ACAO *, checked) and Original, EUR 1 (a sheet; one payment link per comp with the file name as its reference). Signature: the opening's glider flies the task line to the day you tap.
**Recommended** that, because the pilot's two questions are "is my day up" and "am I in it", and the line answers the first in the site's own grammar.
**Flagged** on today's Piedrahita page: "a highlight video each day" (three videos, Task 3 none); task dates missing, video publish dates shown unlabelled; hero photos repeated in the grid; captions carry no file name; "A free 30-minute call" not in the facts. The 20 web copies carry no EXIF, so capture times must come from the originals at export.

## 3 Nov 2026: the Media page as a broadcast media kit, built "On Air" in `samples/media-f/`
**Asked.** Rebuild Media to sell comp coverage to organisers and sponsors only (owner: it has the vibe but "doesn't scream buy my services", a portfolio not an offer). Brief: `docs/designers/media-brief.md` (agreed order, the only facts, EXAMPLE and `[to supply]`). Own angle on the broadcast media kit; no prices; one primary action, Check dates for your event.
**My angle.** An event director's first two questions are "what do I get" and "can you do my dates". So the page is a season rundown, and orange is the LIVE tally: the next comp's dot, the lit package, the button.
**Built** `prototypes/v4/samples/media-f/index.html`, self-contained (copy of media.html; reel, stills and viewer kept, v4-media.js unedited; build script scratchpad `f/build.py`). Paths are two folders below v4: repo-root files need `../../../../` (the brief's "../../ becomes ../../../" was one level short; listen-c does the same).
1. First screen: SRS_5_T1_9 full-bleed (orange race wing under heavy cloud); a broadcast bug "Next, SRS Tapalpa, Mexico, Tasks 8 to 14 Nov 2026, In 5 days" (counted by script, dates without it; "Now" during, "Latest" after); "Your Comp, On Air"; the result line (sponsors seen, pilots back); Check dates + Book a Call; a lower third: Covered for SRS and PWCA (dashed text lockups marked Logo slot), 31,250 views, 21 h 42 min live, 136 countries.
2. Line-up: the four posters at 2:3 on the event's own line, a turnpoint over each (Before the race, Every task day, After the race, Mid-season), one short line each, and which package holds it.
3. Packages: Daily, Full Event (orange edge, "Most chosen" tab marked Example), Season; a bar shows which part of the event each covers; "Priced per event"; Check dates picks the package in the form.
4. Reach: the gaggle full-bleed with 31,250 (counted 3 Nov); then the 2026 season line May to Nov, each comp at its real dates with its readout, Tapalpa lit, today marked; phone: the upright spine.
5. Proof: quote marked Example, the 13-video reel (meta in DM Sans, not DM Mono), nine stills with zoom.
6. Spec sheet: you get / I need from you. 7. FAQ as details. 8. Check Dates in the cta-band: 2027 months (Example; an open month fills the dates), the six-field form, GET to enquire.html?trip=media, Book a Call and WhatsApp second. 9. One newsletter line.
**Checked.** 1440x900, 390x683, 390x844 (plus 1024, 768, 1920): no sideways scroll, no errors or 404s. The owner's 683 phone shows bug, wing, promise, both buttons and Covered for on the first screen. Reduced motion and no JS show the finished page. Picks, poster play, reel filter, viewer and submit tested. Shots: `/tmp/claude-0/media-design/f/`.
**Recommended.** This, because it answers both questions on the first screen and every section ends in the same one action, with nothing invented.
**Flagged.** (1) enquire.html does not know trip=media: it keeps only the dates and drops event, place, package, name, email; GET also puts name and email in the address bar (POST once the enquiry worker is on). (2) The nav's Enquire Now goes to the trip form; on Media it could read Check Dates. (3) media.html's "free 30-minute call" is not in the brief's facts; media.html still uses DM Mono for labels. (4) After 14 Nov the next comp is `[to supply]`. (5) To supply: logo files, the quote, the 2027 calendar, travel, rights, lead time, footage access.

## 28 Oct 2026: a loading screen (advice, nothing built)
**Asked.** One concept for a loader shown only on slow loads (over 0.5 s, once per visit), after the owner called version 2 (scratchpad `loader.html`, stills `l2sheet.jpg`) "a cheap build"; back or kill horizon line, focus pull, ASCII terrain.
**Found.** Cheap because: clip-art glider and stock speed lines; a percentage counter (fake precision, dashboard talk); six things at once; a canopy wipe to a hero that is not our opening; demo chrome. Flagged: "Â·" mojibake in the readouts; "93 conversations" on the podcast screen where the fact is 86.
**Proposed: "The line is already there."** The loader is the opening's own first frame without the photo: the place name in Poppins, dim, and the season line drawing as real progress at its own place; when loaded, the photo rises behind the name and the line simply carries on as the season line. No exit, no wipe. Phone: same at the phone line's place. Reduced motion: name and line still, then a cut.
**Recommended.** That, with the horizon line kept only for destination pages (their ridge as the line); kill focus pull (needs the photo it waits for) and ASCII terrain for the loader (heavy three.js to cover a slow load; borrowed signature). Why: the best loader is the page arriving, not a separate show.

## 28 Oct 2026: a grain map for every page type (advice, nothing built in the repo)
**Asked.** Where D's film grain (sd about 2) should be on, off, lighter or faded, so it merges into the site. Looked at the staged site (scratchpad `_site5`) at 1440 with the contrast stretched (scratchpad `gmap/`).
**Found.** Grain is already off on photos, video, globe, posters and cards (they sit above the body). Gaps: (1) the home opening's own shader grain (sd 3.3, fine) stops on a hard line at the canvas foot against the CSS grain (sd 2.0); (2) the destination page's `.tm` (#route) and `.gxa` (#gallery) are opaque #0d0e11, about 12,000 px with no grain and a hard on/off edge; (3) the sticky `.v4u-jump` bar (destinations, KB topics, atlas) is flat (blur, 94% fill), the same fault `.v2-tools` had; also the footer ridge fill and the sitemap `.sky-ground` are flat.
**Proposed and tested.** Mask `.gl-canvas,.veil` to transparent over their last 200 px: the two grains cross-fade, no step (`gmap/seam_before_after.png`). Grain layer on `.tm,.gxa` and on `html body .v4u-jump`.
**Recommended.** Those three; keep cards, photos, globe, posters, buttons, fields and the orange clean; no "lighter grain" behind transcripts (2 levels is already below what text notices); no grain over photos.

## 25 Oct 2026: a compass or emblem on the listen-c posters (brainstorm, nothing built)
**Asked.** The owner wants a shape "like I had, a compass or something, which invokes a sense of adventure".
**Old compass, honestly.** Baked into plate.webp: large, grey on red so muddy, across the faces, the same on all 15 (wallpaper), it said nothing true, and it could not move.
**Ideas.** (1) bearing compass: thin ring in the top corner, needle at the episode's real bearing from the Oslo studio (globe-episodes.js `brg`, `card`, `km`; globe.js already swings an index this way), readout "229° SW, 1,133 km", needle swings on hover; (2) the wing arc of the Atlas mark over the head; (3) XC turnpoint cylinder, dashed ring with a cross; (4) contour rings behind the head; (5) curved graticule in the red ground.
**Picked.** (1): the same adventure sign, but true and different on each card, and it ties the strip to the globe above.

## 25 Oct 2026: overlays on the listen-c posters (brainstorm, nothing built)
**Asked.** The owner: "how will overlays affect the look, what kind, types etc". Looked at `samples/listen-c/` at 1440 and 390 (scratchpad `f-rail/c-*.png`): the foot gradient reads navy, not the page ground; hover change is barely visible.
**Ideas.** (1) foot fade into the page's own ground; (2) faint site topo lines in the red ground; (3) fine static grain over all 15; (4) duotone at rest, colour on hover; (5) hover light tinted orange; (6) the pin's real place on the art: lat, lon and bearing from globe-episodes.js (e.g. Ogden 52.5 N 1.9 W), "Find it on the globe" on hover.
**Picked.** (6), on top of (1): it ties the strip to the globe above with real data, the site's "where" thread; risk is small type on red, so it sits on the fade.

## 25 Oct 2026: the "More conversations" strip, award level (advice, nothing built)
**Asked.** The owner likes the previous home rail (fa877a47: red poster art, hook and name on the plate, lean with a soft light) more than today's calm grey cards; what can make the cards and the strip agency quality. Shots: scratchpad `f-rail/` (old and current, 1440 and 390, hover).
**Found.** The calm look came from my own chat 12 refinement ("calm cards ... no compass, plate, tilt or glint", to make orange the only colour). What I missed: the red ground and the plate are the podcast's own cover art, its identity and the strip's warmth; grey cards read as a stock gallery after the lit Kenya stage. Kept from today: live, readable series, number and length; no baked compass or tiny baked text.
**Proposed.** Posters again: guest art in its own colour held a step down at rest (lifted to full on hover or focus), hook and name in live Poppins caps on the art with CSS rules in place of plate.webp (no compass), series and number as a stamp above, under the art only "52 min / 12 chapters", no expand icon. The lean and soft light back on the one card under a fine pointer only. Strip: heading row "More Conversations" with the arrows and "All episodes in the Library" on its right, hairline with a short orange lead, a 15 tick progress line under the rail in the opening's line style, poster ratio, next card peeking; phone cards about 72vw, swipe, line visible.
**Recommended.** That one, because the art is the owner's and colour plus live type is what lifts it from tidy. Flagged: the lead's grey stills next to warm posters; the orphan "3" in Armant's title.

## 25 Oct 2026: built B4, the globe leads the stage, in `samples/listen-b/`
**Asked.** Build the three designers' merged spec. **Built** (script `scratchpad/b4/build_b4.py`): 1440, left 5/12 (Kenya and India 112 px, Panchgani shrinks to fit; dates; 240x135 picture with our play on it, series, title, guest beside; chapter line at column width; See the trip; Hear another trip as 96x54 rows at the column foot), right 7/12 the globe, ring 720 px, top level with the name, not sticky. Play grows the frame to the column width into the space above the rows; the globe and name never move; the end or another pick brings it back small. Globe: compass, second ring and orange rim off, one ring in the line token; legend and caption one grey line under it; zoom 28 px inside the square's corner (phone: at the end of that line). globe.js fits the sphere to 0.74 of its box, so the box is drawn larger and a square clips it (clicks too); the card stays inside the square; a resize closes an open card. 390: name, dates, globe 352 px, picture row, line, See the trip, other trips. **Checked:** no console errors, no sideways scroll at 390, pins click at 1440, 1100, 800 and 390, reduced motion and no JS.

## 25 Oct 2026: the globe leads the top of the podcast section (advice, nothing built)
**Asked.** The owner on B3: the episode picture is too big; they want the globe to dominate this section (the globe itself will later be swapped, likely for the Encarta concept), so only its position, size and look. Keep the lead trip, play in place, chapter line, See the trip, the globe turning to the pick, Hear another trip, More conversations.
**Found.** The 560 px grey face is the biggest thing in the section; the globe ring is about 480 px in a 40% column with empty space under it.
**Proposed.** 1440: flip the stage, globe about 760 px square on the right (no sticky), text column about 440 px on the left, centred to it: Kenya 112 px, dates, then a 240 px 16:9 picture beside play with the chapter line under, series, title, guest, See the trip. On play the same frame opens to the column width for the video. Hear another trip moves under the stage as one full-width row. 390: name and dates, then the globe full width (square, not 4:5), then the small picture with play, chapter line, title, See the trip, then the other trips. Appearance: quiet the chrome, drop the degree ticks and N E S W, keep one thin ring, legend and caption as one line under the globe, zoom buttons small inside its bottom-right corner, so a new globe drops into a clean square.
**Recommended.** Yes, change it: the place on the globe is the answer to "where", the face is not. Easy: the grid, sizes and moves (CSS). Risky: the globe canvas resizing (hit areas, redraw on resize) and the play frame growing without shifting the globe. Text over the globe not proposed (contrast, fights drag).

## 25 Oct 2026: built B3, the lead trip in `samples/listen-b/`
**Asked.** Build the chat's merged spec: the lit trip leads (Kenya default), plays in place with Trim's chapter line, the globe answers. **Built** (generator `scratchpad/b3/build_b3.py`): heading row with a one-line intro and search; lead about 60% (112 px name, dates, 16:9 face crop at 560 px, play + chapter line + readout, series, title, guest, See the trip), globe 40% beside it and sticky; other trips as radio labels under it; India's Gohil as a second line that swaps into the player. Play loads the nocookie embed only on tap; another pick removes it. Globe: no idle spin, 0.9 s shortest turn then the route lights in 0.5 s; phone turns as it scrolls in; reduced motion jumps. No JS: CSS picks, links, trip list with the lead orange. **Said:** the frame stays 560 px because the face crop is about 530 to 540 px of the 1280 still (larger is soft); chapter titles carry no "** review" text, but episode-meta.json says they were written by Claude and marked for review; the exact length comes only from the player (the timelines are whole minutes).

## 25 Oct 2026: how I will build the lead in B (advice, nothing built)
**Asked.** As the builder, plan the owner's choice for `samples/listen-b/`: the lit trip leads large (Kenya by default), the others small beside it, the episode plays in place with Trim's chapter line, the globe turns to the lead trip with the route lit to it. Not the footage.
**Checked.** No audio file exists: the episode pages embed YouTube (`youtube-nocookie.com/embed/<id>?enablejsapi=1`) and their chapter ticks jump to transcript anchors, not the player. episode-meta.json has only `duration_label` ("52 min", whole minutes) and chapter starts in seconds; Yotov's last chapter starts 35:09 of 52 min. `.sl[data-lit]` follows the opening, so it changes on its own.
**Proposed.** Lead: picture (the episode's own YouTube still, face crop, about 60% wide so it stays sharp), place name large in Poppins, real dates from the season rows, "See the trip", guest, series and number, title, length, one play button, the chapter line. Play swaps the still for the nocookie embed in the same frame (loaded on tap only); the line reads the time over YouTube's postMessage (no extra script) and a tap seeks to that chapter. Switch: tap a small trip; the lead reads `data-lit` only as the section scrolls in, never while seen or playing; one sound at a time. Kazakhstan, Peru lit: Kenya leads; no card for them (as before). India leads with Colfox, Gohil small. Phone: frame full width, then text, then the three small trips as a row; the chapter line taps to the nearest chapter, name shown under it. No JS: still, links and a plain chapter list.
**Recommended.** The lead as one block of trip plus episode: the dates and "See the trip" sit beside play, so hearing Kenya and choosing Kenya are the same place on the page.

## 25 Oct 2026: "something missing" in B2 (review, nothing built)
**Asked.** The owner on B2 "Hear Where We Fly": "There's something missing. Is it the size, the feel, the appearance, what?" Judged in context at 1440 and 390 (opening, departures, then the section; shots in scratchpad `fresh/`).
**Found:** no hero moment. The opening is a 260 px place name on a full photo; the departures are precise data; then this section drops to a 35 px heading (same as "Every Departure") and a row of equal grey portrait cards. Nothing leads, nothing is big, and a section called "Hear" has nothing to hear on the page.
**Proposed:** one stage before the rail for the lit trip (Kenya now): full content width, about 560 to 640 px tall on desktop and about 60 vh on a phone, a clean frame from that episode's own video (`[to supply]` if none without baked words), the place name large in Poppins, guest and title, one play button that plays the episode in place on tap (its YouTube embed, no autoplay). Yotov's card leaves the rail so no art shows twice. Smaller: crop the cards to head and shoulders (the phone crop is eyes to chin); shorten the intro to one line with the search on the heading row so the stage reaches the first screen.
**Recommended:** the stage, because scale and one clear lead are what the opening taught the eye to expect, and play is the section's promise.

## 25 Oct 2026: built B2, the agreed refinements to "Hear Where We Fly"
Built into `prototypes/v4/samples/listen-b/index.html` (generator `scratchpad/lb/build_b2.py`): calm cards (grey grade, colour on hover or focus, live title and guest, no compass, plate, tilt or glint); trip cards on each episode's own art cropped to the face (YouTube still, words cropped out; no local portraits exist for Yotov, Kharas, Colfox, Gohil); one heading per trip, India's four dates once; "More conversations, Newest first" in the same row, grey rule, sticky; globe popups on the rail's picture, coordinates to one decimal in DM Sans; season route line and hollow Kazakhstan and Peru pins (Expeditions atlas coordinates); "Find it on the globe" uses the globe's own #pin deep link; phone ring fits with N E S W inside it, zoom buttons under the caption. Said "Newest first" rather than "Latest conversations": the 15 are not the 15 newest episodes.

## 25 Oct 2026: refining "Hear Where We Fly" for Awwwards (review, nothing built)
**Asked.** The owner chose B and asked to refine it with Awwwards in mind; fix trip photos reused from the opening, compass rose and red YouTube art fighting the orange, phone globe ring cut off, sideways "More conversations", unsourced "most streamed".
**Proposed, ranked:** (1) one art system: trip cards on owner photos not on the home (Kenya `img/hero/kenya-chyulu-hills-p`, India Billing launch for Colfox and Bir landing for Gohil), Panchgani `[to supply]` (its only photo is the opening's), compass and tiny baked text off, all art in one dark grade, colour back on hover or focus; (2) pin popups use that art, not YouTube thumbnails; (3) one India head over both India cards with all four 2027 dates; (4) "More conversations" as a flat head in the trip-head row, split line gone; (5) phone globe: dial fits 358 px or loses its degree ring, zoom buttons in a row under it; (6) a "Find it on the globe" link in each trip head turns the globe to its pin and opens it (the only new motion, on tap); (7) no order claim for the 15 unless sourced ("Newest first" if sorted by date).
**Recommended:** (1) matters most: it ends the rule breach and makes orange the only colour, the biggest Design lift.

## 25 Oct 2026: built "Hear Where We Fly" as preview B
Built `prototypes/v4/samples/listen-b/` (home copy, #listen and #map merged): trip cards first (Kenya, Panchgani, India x2, next date and "See the trip" above each), then the 15 cards, no self-scroll; globe below with trip pins orange, others grey, trip popup adds dates from the rows. No JS or reduced motion: list of the pinned trip episodes. Flagged: trip photos repeat the opening's (owner's rule).

## 25 Oct 2026: round 1 on #listen (the podcast section) and #map

**Asked.** One concept for `#listen` (search, most-streamed rail), what
follows the season line and leads to `#map`; should the two merge?
**Proposed: "Hear Where We Fly".** One section, one heading: head and search,
then the rail, then the globe straight under it (its own kicker and title
become the caption). The rail opens with the episodes recorded at our trip
places, in season order (Kenya: Nikolay Yotov, Navigators 10; Panchgani:
Vistasp Kharas, 9; India: Eddie Colfox, 3, Jigish Gohil, 4), the trip lit
above first, on the owner's own trip photos (no guest art exists for them);
then the 15 most streamed. One interaction, the existing pin tap: trip pins
orange, and their popup adds the trip's dates from the season rows and "See
the trip". Remove the rail's self-scroll (moves unasked, clones all 15
cards) and the "Click A Pin" link. **Recommended** merging: both halves are
episodes, and the trips stay the thread from the season line to the map.
**Flagged:** "80 conversations" vs 93 entries in episode-meta.json and 78
pins; Kazakhstan and Peru have no episode (no card, no placeholder); the
intro's "most streamed" copy is the owner's to change; without JS the globe
box is empty (needs a plain list of pinned episodes).

## 25 Oct 2026: a cursor shine on the departure rows?

**Asked.** Is a soft light that follows the mouse across the departure rows
(like the episode cards' radial light, `html.v4-tilt` in tools/v4_polish.py)
a good idea, on top of the 4% wash, orange bar and glider flight?
**Answered: No.** The rows already answer the pointer three times; the one
answer that matters is the orange bar at the real dates, and a moving light
pulls the eye off it. The shine suits pictures (episode cards, tiles), not
wide rows of text and prices, where it reads as a smear over the facts. Phone
and reduced motion would not see it anyway. **Recommended** keeping the rows
as built; if the section needs more life, make the existing wash a touch
stronger rather than adding a fourth effect.

## 24 Oct 2026: whole-site study for Awwwards, from the destinations

**Asked.** Study the whole v4 site against Awwwards (Design 40, Usability 30,
Creativity 20, Content 10) and say how far it has come since v4 at 48bfc475
(the owner: "I'm talking about V4"). **Found:** the home now opens on the
trips (KENYA, real dates, "Next one in 86 days", one button, season line);
India's 2027 dates match everywhere; Panchgani is a tour with its own page and
the episode links to it. One step back: on a phone the opening's trip button
sits at 824 to 871 px on an 844 px screen (was 560 px). **Gaps, ranked:**
(1) trip pages tell the trip differently from the opening (no dates or price
on Kenya's or Panchgani's first phone screen; US$, GBP, EUR unexplained);
(2) phone button below the fold; (3) the home says the trips three times
(fly-by, sideways timeline, table); (4) trust thins at the last step (pilot
quotes and eight Panchgani facts `[to supply]`, Send opens the visitor's own
email app); (5) Kenya's route stops in reduced motion are a 150 px column with
labels overlapping, DM Mono in Kenya's season facts, empty maps for
Panchgani, Kazakhstan, Peru on expeditions, Panchgani's only photo borrowed.
**Recommended, and why:** "one trip, one readout, everywhere": the opening's
readout and season line as the trip component on home, expeditions, every
trip page's top and the enquiry summary, so the same facts follow the visitor
to Send. Scratch: /tmp/claude-0/-home-user-website/33175f8f-65f7-5e00-a8e5-f43c2657942f/scratchpad/designers/study-F.md

## 24 Oct 2026: built the one preview of the merged departures section

**Asked.** Build option A, the three designers' merge, as one preview in
context. **Built:** `prototypes/v4/samples/departures/index.html`, a copy of
the v4 home with only `#destinations` replaced. Desktop: the opening's season
line (edges matched to the pixel, 72 to 1368 px at 1440), today marked, Kenya
lit; nine rows (today's table facts, `[to supply]` kept), each with its bar at
real dates as a line under the row (bars above the row read as belonging to
the row before, so I moved them under). Pointing or focus flies the glider
along the line to that bar with the opening's lift and bank, orange track
from today. Phone: upright spine, one card per departure, Nov, Dec and Jul,
Aug, Sep shown as gaps, scroll-drawn track with the glider on its tip. Reduced
motion and no JS: whole list, glider at today. Call band kept. **Recommend**
showing the owner this as is; the call band's "Kenya, India, or Peru" is still
the owner's words to change. Shots: scratchpad `designers/preview-*.png`.

## 24 Oct 2026: round 2 on the section after the opening

**Asked.** Weigh D's and E's round 1 against mine, name one concept and a
second. **Proposed and recommended:** "One Line, Two Postures": D's line
across on desktop with nine rows and bars at real dates, E's glider flying to
the row you point at, my upright spine and scroll track on the phone; no
filters, thumbnails or morph. Why: the opening's line carries on unchanged on
desktop, and the phone gets the clearest one-tap list. Second: D with my phone
spine. Scratch: /tmp/claude-0/-home-user-website/33175f8f-65f7-5e00-a8e5-f43c2657942f/scratchpad/designers/round2-F.md

## 24 Oct 2026: round 1 on the section after the opening

**Asked.** How the next v4 home section (today `#destinations`: the fly-by
"See Where We Fly", "Every Departure" with its sideways timeline and table,
then the call band) should look and move, judged on the Awwwards criteria,
given that the opening already shows the season, places and dates.

**Proposed: "The Flight Log".** The opening picks a place; this section picks
a departure. All nine departures in date order on the opening's season line
turned upright (Oct 2026 top, Nov 2027 bottom), one row or phone card each:
name, tour, dates, length, places, price, status, level, arrow to the trip
page. Planned trips dashed, empty months shown as gaps, missing facts
`[to supply]`. On scroll an orange track draws down the spine and the
opening's small glider rides its tip (CSS scroll timeline; reduced motion and
no JS show it finished). The trip chosen in the opening arrives marked.
Drop the fly-by (older photos, four trips not five, repeats the opening) and
the sideways timeline (labels collide, repeats the season line). Keep the
departures data, level meter and call band.

**Recommended, and why.** This one only: it stops the repeat by giving the
section a new job (which departure, can I go) and makes the two sections read
as one flight. Lighter page (four photos and a video fewer).

**Flagged.** The call band copy names "Kenya, India, or Peru" only (owner's
words to change). Levels for Panchgani, Kazakhstan, Peru are not on file.
Scratch: /tmp/claude-0/-home-user-website/33175f8f-65f7-5e00-a8e5-f43c2657942f/scratchpad/designers/round1-F.md

## 24 Oct 2026: my own entry

**My angle.** The trips are the main act. People come to pick a trip, so the
opening must make that easy: where, when, how long, how much, and one button
to the trip page. The photo sets the mood; the readout and the button must
win. I keep the season line honest (real dates, nothing made up), the opening
calm, and switching places clean and quick on a phone.

**What I proposed, and why.**
- Round 3 (23 Oct), "Fly the Season": the corner list became a flight line
  across the season, one turnpoint per trip at its real dates, with a
  readout and one button under the photo. Why: it answers "when can I go?"
  at a glance. It won.
- DSC_9492 (24 Oct): the valley pushes in about 8% over 14 s while the
  gliders get a little smaller and drift away, one way only, starting after
  the arrival so nothing turns back. Why: the owner's "away from the
  viewer" without fighting the arrival.
- Panchgani (24 Oct): I said keep it off the line until it had dates, a page
  and a price, and never put it under India's Bir Billing trip. No big
  cut-out (the wing is tiny and would go soft), the name at Kazakhstan's
  size, a slow, gentle move. The owner then gave it dates (14 to 21 Feb
  2027), so it now sits on the line.

**What I would do next.** Build F2 into the v4 home, then check it on a real
phone: the readout and button easy to read over every photo, and "Next one in
N days" using all four of India's 2027 departures.

**The next transition.** It should feel like flying the next leg, not
changing a slide. About 1.1 s:
- When the progress line is full, the small glider flies to the next
  turnpoint, always left to right.
- The new place comes in from the right behind the orange edge; the old one
  slides 3% left and dims. The new wing glides in 0.3 s later, so the name
  and readout read first.
- The name settles in, 70 ms per letter. The readout changes in place; the
  button stays put and only its words change.
- From Peru back to Kenya the glider must not fly back across the line (today
  it does): it flies off the right end and comes in from the left, so the
  season only moves forward.
- A tap mid-move goes straight to that place; reduced motion changes at once.

## Starter (24 Oct 2026, from docs/v4-next-session.md)
- Round 3 (23 Oct): the corner list became a flight line across the season,
  each trip at its real dates; picking one flies a small glider along the leg
  while the new place sweeps in; a readout gives dates, length, launch, price,
  what you fly, "Next one in N days" and one button. Won; became F2.
- 24 Oct, DSC_9492: the owner chose option A, the slow follow shot (D's pick
  and mine).
