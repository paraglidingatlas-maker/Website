# Designer F, "Fly the Season": notebook (newest first)

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
