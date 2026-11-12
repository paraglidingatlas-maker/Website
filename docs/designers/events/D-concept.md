# Event landing pages: designer D (Trim), "Final Cut, the event"

**The direction in one line.** The gallery page, finished: a cover that cuts once through the event's days like a
film edit, on a letterbox bar that is both the cut's progress line and, once you scroll, the page's day-by-day bar.

Sample: `prototypes/v4/samples/event-d/index.html` (SRS Piedrahita) and `pwc.html` (PWC Super Final), shared
`event-d.css` and `event-d.js`, screenshots `shot-390.png`, `shot-1440.png` (plus `shot-pwc-390.png`,
`shot-pwc-1440.png`). Both pages are built from one template by a generator (chat 22 scratchpad, `gen_event_d.py`):
the event's data is the only thing that differs.

## The answers

**Landing page = the gallery, or a page above it?** The gallery page, made right. Same URL, no page above it.
Why: people arrive from a WhatsApp or Instagram link to see the photos and the films; a page above the gallery puts
one more tap between them and the photo they came for, and splits one event across two URLs. What the gallery lacks is
not a new page, it is a cover and a way round the days. So the opening of the gallery becomes the landing.

**Films only (PWC, Bassano), so it does not feel empty.** The same template with the photo sheet left out: each day
is its film, large, playing in place, with two more frames from the same film under it. The cover cuts through
frames of the owner's own films (the flags through Pegalajar, launch, the pilots), not the YouTube thumbnail art
(baked text, purple and green, faces in a row). One craft rule makes it hold: **a film frame is shown as a film frame.**
A 1280 frame cropped to a 390x683 portrait is soft and reads as a fault, so on a phone the PWC cover is a 16:9 screen
with the title on the dark ground under it (all on the first screen at 683). On 1440 it fills the screen.
The facts line counts what is there: "5 films by Aninder Singh, 37 min 49 s, 21,690 views on YouTube by 3 Nov 2026".
What is not known shows as `[to supply]` (pilots, tasks flown, the official event link, what happened on Task 3).

**Easy to navigate (phone, one or two taps).**
- A day or task: one tap on the bar (Day 1, Task 1, 2, 3). The bar sticks under the header all the way down and
  lights the day in view; on PWC's six days it fits (the word small, the number large).
- The films: they sit in their own day, first thing under its title; one tap on the bar, one tap on Play.
- The photos: each task's sheet follows its film; one tap on a photo opens the viewer (swipe, Save free, Patreon).
- Back to the season, the next or previous event: the bar's first item "&larr; 2026" jumps to the season block at the
  page's foot (one tap), where the four events of 2026 stand as rows marked Before, Here, Next (second tap).
  The Media page is one more link there. Nothing leaves the page by surprise.

**Immersive: the signature moment.** "The cut". The cover holds each task's best frame for 5.5 s and cuts straight
to the next (no fade, no zoom: a cut, like an edit), while that task's segment of the line fills along the photo's
foot. One forward pass, then it rests on the cover frame and stops; the line becomes the page's day bar as you scroll.
It is the home opening's approved grammar (one forward pass, a progress line you can tap) told in an event's days.
A tap on a day, or scrolling into the days, ends it. Pause sits at the line's end. Off screen and in a hidden tab it
holds; it never cuts to a frame that has not arrived (the line waits full until it has).

**What it costs on a mid-range phone.** Almost nothing. Three (Piedrahita) to five (PWC) images, the phone's 800 or
1600 copy, about 0.4 MB in all; the cut is one opacity switch every 5.5 s; the line is a CSS animation of `scaleX`
on a 2 px bar (compositor only). No WebGL, no scroll-linked transforms, no per-frame JavaScript. Compare the Media
page's pull-back (a day to make smooth): this has nothing to smooth.

**Reduced motion and no JavaScript.** The cover rests on its last frame (Piedrahita: the gaggle, SRS_5_T3_63), the
bar's days are anchors, films link to YouTube, photos open full size. Tested.

**One template for every event (a comp a month).** The chat fills in per event, in `tools/v4_comp_gallery.py`
COMPS (Piedrahita and Tapalpa are already there): title, kicker, the facts, the official link, the photo folder (or
none), and the days: id, name, the story line (from the film's own description), its films, a poster photo of the
same task per film (the owner's 9 Nov Tapalpa rule), and one cover frame with its crop. Prev/next comes by itself
from the Media page's SEASON and UPCOMING. Shared code: the cover, the bar and the days go into `v4-gallery.css/js`;
the viewer stays the gallery's (Save free, Patreon, the originals link); play in place as on the Media page.
A live event (Tapalpa) works the same: the cut runs through the tasks so far and rests on the newest.

**File names and URLs.** The two shared URLs stay and become the landing pages: `media-srs-piedrahita-2026.html`,
`media-srs-tapalpa-2026.html`. New ones follow them: `media-pwc-pegalajar-2026.html`, `media-srs-bassano-2026.html`.
The Media page's season rows link to these instead of opening the Watch sheet.

## The page, top to bottom, on a phone (390x683)
1. The site header.
2. The cover, the rest of the first screen: the photo full height, no scrim on the subject (a foot gradient for the
   words). Kicker "SRS BGD Edition &middot; Piedrahita, &Aacute;vila, Spain"; "Piedrahita 2026"; 22 to 29 Aug 2026,
   FAI Category 2, 120 pilots, 54 countries; the official event link.
3. The bar, a letterbox on the photo's foot: &larr; 2026 | Day 1 | Task 1 | Task 2 | Task 3 | pause. On the first screen.
4. Day 1: "1 film, no photos this day", the line, the film (its own frame as poster), plays in place.
5. Task 1, Task 2: count, the line, the film (a photo of that task as poster), then every photo in shot order,
   true ratios, nothing cropped, each cell in its photo's colour while it loads.
6. Task 3: 146 photos.
7. The 2026 season: four rows, Before / Here / Next, each a tap to that event; the Media page link.
8. "Coverage Like This For Your Event" (the organisers' proof, as today), the footer.
On 1440 the day's title sits in a sticky left quarter, film and photos in the other three.

## What I would steal if I lose
I worked alone and have not seen E's or F's. By their angles: from E (Cloudbase), a camera move only where the owner
has real footage to move through (not a zoom on a still); from F (Turnpoint), the season as a line with each event
at its real dates, in place of my four rows. I would keep my two rules in any winner: film frames never cropped to
a portrait, and the cut instead of a crossfade.

## Found on the way (not asked)
- The PWC Day 1 thumbnail on YouTube reads "12.05.2027 - 23.05.2027": the year is wrong (the films came out in May 2026).
- The live Piedrahita gallery puts the Day 1 film under Task 1; it is a different day (registration). Here it is its own day.
- The live Piedrahita gallery uses the purple SRS thumbnail art as film posters; Tapalpa uses a photo of the same task
  (owner, 9 Nov). Piedrahita was never brought up to that rule.
- PWC has no stills in the repo: the sample uses YouTube's own 1280 frames of the owner's films. For the build, the
  owner's frame grabs from the film files (2400 wide, on the media host) would make the cover sharp.
- Bassano: the broadcast frames carry the live overlay (clock, chat, paraglidinglive.com). Its page needs the
  owner's own frames or stills, and whether that footage is the owner's to use: `[to supply]`.

## What it costs to build
About one chat day: the cover, bar and days into `v4-gallery.css/js` (about 250 lines CSS, 150 JS), the generator in
`tools/v4_comp_gallery.py` (films-only events, the season rows), PWC and Bassano entries, the Media page's rows
pointed at the pages; then the gates at 390x683, 390x844, 1440x900, reduced motion and no JS.
