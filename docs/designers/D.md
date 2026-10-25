# Designer D, "Final Cut": notebook (newest first)

## 25 Oct 2026: the "More conversations" strip, agency quality

**Asked.** The owner "really like[s] the previous design" (poster cards at
fa877a47: hook and guest name set on the art, colour, the lean with a soft
light) and wants the strip and its cards award level. **Found.** The calm
look came largely from my own list (portraits greyscale, drop tilt and
shine); "no glow" was the podcast cards' rule, never the site's. I was
right about the compass and the raw YouTube red, wrong to take the poster
and the warmth with them: today's strip reads as a contact sheet, grey on
grey. Its hover floods the raw red and blue shirts in (worst of both).
Also: "Newest first" is untrue (F noted the 15 are not the 15 newest);
the phone heading sits at 24 px against the 16 px gutter; one-line titles
leave a hole; "Enzo 3" orphan; the expand icon is unexplained; the rule
runs past the container.
**Proposed, "The Plate, Finished".** Keep the poster. Key the flat red
backdrop out (clean cut, no red rim), lay each guest on an ember ground
from the one orange to the dark at the foot; face in true colour. Live
plate: hook in Poppins caps, short orange rule, guest name large; series
and number one line on top. Meta: each episode's chapter line drawn to its
real length (episode-meta.json), the lead player's twin; no expand icon.
Hover: 2 degree lean, white light 8%, the rule draws; no overlay. Strip:
hairline to container, arrows in the heading row, edge fade not a hard
crop, token gap after the globe; phone: 82% cards with a peek, swipe and
snap, no arrows, gutters fixed. Reduced motion and no JS: the still plate.
**Recommended** it. Why: it gives back what the owner liked and fixes
the two faults that made us drop it (the second red, the compass).

## 25 Oct 2026: the globe leads the lead trip (B, "Hear Where We Fly")

**Asked.** The owner: the lead trip shows "too big of an episode thumbnail"
(560 px face); they want the globe to dominate this section; the globe will
likely be swapped later, so only its position, size and look. Need a change?
**Found.** Yes: the face is the largest thing in the section, the globe
(about 480 px) floats right with dead space under it, legend above and zoom
buttons sitting on the ring.
**Proposed.** 1440: swap the weights. Globe column about 60% (ring about 720
px, globe about 640), top aligned with "Kenya", sticky. Left 40%: name 112
px, dates, a small 16:9 picture (240x135) with play over it, chapter line the
full column width under it, title, guest, See the trip; Hear another trip as
two rows with 96x54 pictures under it. 390: name and dates, then the globe
full width inside the 16 px gutters, then picture (96x54) plus title in one
row, chapter line, See the trip, other trips as rows. Fix: one hairline ring
(--line), no glow, the route the only orange; legend, caption and the three
buttons in one row under the globe, off the ring.
**Recommended** side by side, not text over the globe. Why: text over a
turning globe fights it, and the globe is going to be swapped; a fixed
column survives the swap.

## 25 Oct 2026: making the lead trip right (B, "Hear Where We Fly")

**Asked.** How to build the owner's choice: the lit trip leads big (Kenya by
default), others small beside it; play in place with my chapter line; the
globe turns to the lead and the route lights to it. Not the footage.
**Found.** All four trip episodes are YouTube only (8 of 93 episodes have
their own audio, none of these); episode pages use the youtube-nocookie
embed with enablejsapi, and v4-listen.js seeks through it. Trip cards show
YouTube maxresdefault art (baked text). episode-meta.json gives chapter
starts but length only to the minute; the episode page timeline holds the
exact length (Kenya 52:05).
**Proposed.** 1440: lead 2/3 (about 856 px): name Poppins 112 px, dates,
16:9 picture (owner's unused place photo; Panchgani [photo to supply]),
under it play plus chapter line in one row, then title 32 px. The other two
trips stacked in the last third, 160x90 picture, today's 1.05rem names.
390: name 64 px (fits "Panchgani"), picture full width, play and line under,
title 24 px, other trips as two rows under. Pick by a radio group in the
section (labels on the small rows); CSS hides the picked trip's small row;
the switch is a cut. Play: no iframe until pressed, then the nocookie embed
in the same frame, controls off, our line the only control; another pick
stops it. Globe: 0.8 s shortest turn, route orange up to the lead, the rest
dim; reduced motion jumps. No JS: Kenya leads, picks still work, play and
ticks link to the episode page and its chapters.
**Recommended** the player as the picture. Why: nothing jumps on play and
YouTube's art never shows, so play in place reads as ours, not an embed.

## 25 Oct 2026: "something missing" in B, "Hear Where We Fly"

**Asked.** The owner: "There's something missing. Is it the size, the feel,
the appearance, what?" Judged in the page, opening down to #listen, 1440 and
390. **Found.** Scale. The opening is a 260 px place name on a photo; the
section is all one size: a 35 px heading (same as every h2), 19 px place
names, five equal grey faces, then a globe under its own rule and kicker.
No lead, so it reads as a podcast catalogue, and faces, not places, lead.
**Proposed.** One hero: the place lit above (#destinations data-lit, Kenya by
default) leads as a block about half the width: place name in Poppins at
about 110 px desktop, 64 px phone (a step down from the opening, not a copy),
dates under it, its episode portrait at about twice the card size, title 32
px. The other groups stay at today's size beside it: one big, then small.
Smaller: cut the dead 170 px gap after the call band; fold the globe into the
section (no second kicker or rule; legend into the trip headers).
**Recommended** the hero. Why: the eye needs one place to land, and it makes
"places first" visible.

## 25 Oct 2026: refining B, "Hear Where We Fly" (the owner chose it over my A)

**Asked.** How B can be refined for Awwwards, keeping its idea (trip places
first, globe under the rail, orange trip pins with dates and "See the trip").
Review only. **Found.** Compass rose over every photo; guest portraits on red;
popups show YouTube thumbnails with baked text; trip cards reuse the opening's
photos; two identical "India" headers (reads as a bug); "More conversations"
sideways; phone ring cut and zoom buttons on the globe; popup coordinates at
four decimals in a mono face; 3D tilt and shine on cards.
**Proposed, ranked.** (1) Clean card faces: no compass, portraits greyscale,
title and guest in live type below the photo, popup uses the same image, never
the YouTube art. (2) Unused owner photos for trip cards: kenya-kerio-valley-p,
india-billing-launch-p, india-dhauladhar-p (img/hero); Panchgani has only one
photo, so its card waits on `[photo to supply]`. (3) One India header over both
cards. (4) "More conversations" as a flat header in the trip headers' grammar,
grey rule. (5) Phone: ring fits inside the gutters, N/E/S/W only, zoom buttons
under the caption. (6) No "most streamed"; order by date or no label; popup
coordinates to one decimal, DM Sans. (7) Drop tilt and shine; hover brightens
the photo and turns the title rule orange. (8) Sentence case on kicker and
labels. **Recommended** (1) as the one that matters most. Why: it is what the
eye meets first, and it gives the one orange back to the trips.

## 25 Oct 2026: round 1, the podcast section (#listen) and the map

**Asked.** One concept for #listen (search box plus a rail of most streamed
episode cards), and whether #listen and #map should merge.
**Found.** The cards are guest portraits on red YouTube backgrounds with a
compass rose over the face: a second warm colour fighting the one orange. The
rail hides most cards off the right edge. The intro says "80 conversations";
episode-meta.json lists 93 entries and the globe 78 (owner to confirm).
**Proposed: "Told From Here".** Merge #listen and #map into one band. Left:
heading, search, six to eight rows from homepage-cards.json in the departure
rows' grammar (series and number, hook, guest, minutes, chapters), each with a
quiet line drawn to its real length in minutes with ticks at its real chapter
times (episode-meta.json), the season line's twin. Small greyscale portrait.
Right: the globe, sticky. One interaction: point at or focus a row and the
globe turns to that guest's pin (0.6 s), the pin lights orange, a readout gives
range and bearing from Oslo (globe-episodes.js), as the glider flies to a
departure row. Phone: stacked rows, globe below, drag only. Reduced motion: the
globe cuts. No JS: the full list, readouts as text. Removed: red cards, compass
overlay, rail and arrows, "Click A Pin" link, the map's own heading.
**Recommended** the merge. Why: two bands about episodes with a link from one
to the other is one band; the same gesture as the rows above makes the page
read as one hand.

## 25 Oct 2026: a cursor shine on the departure rows?

**Asked.** Is a soft light that follows the mouse across the departure rows
(like the episode cards' radial light, `html.v4-tilt`) a good idea, on top of
the 4% wash, the orange bar and the glider flight? **Answered: No.** Why: the
row already answers hover three ways; a fourth thing moving splits the eye from
the glider, the one thing that should travel. The card shine is light on a
picture; on rows of text and dates it reads as a smudge. **Fallback if the
owner still wants it:** white only (no orange), 6% at the centre, a 220 px
circle, inside the hovered row only, 0.3 s fade, mouse only; none on phone,
reduced motion or no JS.

## 24 Oct 2026: whole-site study to Awwwards standard

**Asked.** Study the whole v4 site (home, expeditions, Kenya, Panchgani,
podcast, knowledge base, one episode, about) on the Awwwards criteria, and
say how far it has come since v4 at 48bfc475 (the owner: "I'm talking about
V4"). **Found.** The home opening is the big step (the place as the page,
readout, season line); Panchgani is new; the other pages are unchanged and
now lag. **Ranked gaps:** (1) one trip, one name, one list: home shows each
tour three times under three names, four time scales, "Touch The Sky With
Glory" left in footer and call band; (2) the opening's finish: grey rim on
the pilot in the A, no lines, the dashed [to supply] box, 9 px phone months;
(3) red YouTube episode cards; (4) type and token drift: six body sizes, DM
Mono, pure white and #FF8A3D on Kenya, mixed button case; (5) Kenya's fly
chapters black without JS, 21 phone screens. **Recommended:** the opening's
season line as the site's one ruler, fed from one list of names, dates and
prices. Why: it closes the biggest gap and adds nothing new. Full text: the
chat's scratchpad `designers/study-D.md`.

## 24 Oct 2026: round 2, the section after the opening

**Asked.** Weigh E's and F's round 1 against mine and vote. **Voted** a merge:
my across-line on desktop (the opening's own line, edges matched), F's upright
spine and cards on phone (my per-row strip is too small), E's glider gliding to
a hovered row. Rejected E's photo shrink (a big move on a still, chance photo)
and F's scroll-drawn track (motion nobody asked for). Second: F whole, minus
the track. Full text: the chat's scratchpad `designers/round2-D.md`.

## 24 Oct 2026: round 1, the section after the opening (#destinations)

**Asked.** How the next home section should look and move, judged on the
Awwwards criteria, since the opening already tells season, places and dates.

**What I found.** The fly-by repeats the opening with other photos and other
trip names ("The Majestic Himalayas" against the opening's "Big Mountain
Flying"; "A Journey Over The Cradle Of Humankind" against "Explore The
Cradle"). The "Every Departure" timeline runs Jan to Nov 2027, the opening's
line Oct 2026 to Nov 2027: two scales for one season. The call band names
only "Kenya, India, or Peru" (owner to confirm). The level meter (India 4 of
5, Kenya 2 of 5) is the one fact the opening lacks.

**Proposed: "The Season, Opened Up".** Drop the fly-by and the second
timeline. The section opens with the opening's own season line, same 14
months and edges (a match cut by layout, no morph), and under it nine
departure rows with dates, length, group, level, price, status, button and a
bar at real dates on that line. Five place filters; the place last shown in
the opening arrives lit in orange. Phone: stacked rows, each with a 14-month
strip. Motion: bars draw once (0.6 s), hover lights a row's months, filters
dim, never reorder. Reduced motion and no JS: full list, nothing lit.

**Why.** Craft first: one name per trip, one scale per season, one line
through the page. Usability and content gain most; creativity is modest,
which is the risk, along with the edges having to match at every width.
Full text: the chat's scratchpad `designers/round1-D.md`.

## 24 Oct 2026: my own entry

**My angle.** Craft and finish. I make what is there right before adding
anything. Every layer obeys one physics, like one camera on one real scene:
when the gliders go further away they get smaller, their shadow sits
closer on the letters and the mouse moves them less, all from one number. I
distrust any move that could read as a bug.

**What I proposed, and why.**
- Round 3, "Final Cut" (23 Oct): C2 finished, nothing new: each glider's
  real lines drawn back, cut-outs with no rims, a light for each place, a
  switch that cuts like film, a phone layout of its own with swipe. Why: C2
  needed finish, not ideas. The owner chose F.
- DSC_9492 (24 Oct): a follow shot. We follow the gliders into the
  valley; they are faster and pull away: the valley grows to 1.08,
  the gliders shrink to 0.9 and drift toward its far point, their shadow gap
  shrinks to 0.6. Why: only this makes "the valley comes in, the gliders go
  away" true. I warned of a bounce at the start (the arrival grew them,
  the move shrank them); the arrival now starts at 1.05. The owner chose
  it.
- Panchgani (24 Oct): the wing at its real size (110 px of wing turns to
  mush enlarged), the name at Kazakhstan's size, a slow slide, no push (no
  horizon). With no dates then, I kept it off the dated line. The owner then gave dates and
  their own shallow left turn.

**Next for the opening.**
1. An invisible hand-over at 1.55 s: the first WebGL frame matches the
   still.
2. Check every place against the one-number rule.
3. Real lines for India once full-size originals come.
4. Test the phone layout and swipe on a real phone.

**The next transition: a cut on motion, 1.2 s.**
- Everything moves the route's way: right to a later place, left to an
  earlier one.
- 0 to 0.5 s: the old wing speeds up and leaves the frame; its shadow lifts
  off the letters and fades. The old name sinks, letter by letter.
- At 0.5 s: the photo changes in a 0.2 s dissolve, the next pass already
  moving, so the eye carries across.
- 0.5 to 1.2 s: the new wing sweeps in and slows; its shadow lands on the
  letters as it arrives. The new name rises letter by letter.
- The season line's small glider flies the leg in the same 1.2 s; the
  orange diagonal wipe goes, so one orange thing moves.
- A swipe holds the old wing under the finger. Reduced motion: a plain cut.

## Starter (24 Oct 2026, from docs/v4-next-session.md)
- Round 3 (23 Oct): C2 finished, nothing new to learn: each glider's lines
  drawn back, cut-outs without rims, a light per place (late sun Kenya, cold
  India, warm haze Peru, rust Kazakhstan), a switch that cuts like film (one
  glider flies off, the name sinks, the next sweeps in, its name rising letter
  by letter), a phone layout of its own with swipe.
- 24 Oct, DSC_9492: proposed option A, the slow follow shot (chosen);
  warned of a bounce where the arrival hands over to the move.
