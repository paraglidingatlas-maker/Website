# Designer F, "Fly the Season": notebook (newest first)

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
