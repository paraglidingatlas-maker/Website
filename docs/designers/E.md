# Designer E, "Pull Back to the Route": notebook (newest first)

## 4 Nov 2026: the review's defects on the built Media page (fix pass 1, chat 17)
**Asked.** Fix the 27 defects three reviewers (a race director and a sponsor's brand manager, QA, an Awwwards critic) found on media.html and enquire.html's media mode: every blocker and major, the minors where cheap and safe.
**Did.**
- The move (critic-1-1, qa-1-1). Nothing moves until the stage is pinned (the first scroll is a plain one, the nav leaving). Then the words cut out within 3.5% of the move, before the shot starts to scale; the Daily Highlights label rides on the shot next; the other three stay unseen until it is on, then come in as pictures, never from beyond the screen's edge; every word of the board comes last, and only where the shot has cleared it. A tap on the shot plays Daily Highlights from the first pixel.
- The phone opening (critic-1-5, -3, -4). The shot as wide as the screen, lifted so the wing sits under the nav and feathered into the ground, the words on the ground below it, so the owner's photo reads instead of a dim smear. The deck is two factual lines: "Your pilots back next season" was an outcome the facts do not give (my mock's line; dropped with "Your sponsors seen"). Every label 11 px or more, the credits 12 px on two deliberate lines. On a phone up to 799 tall the three numbers sit just below the fold, and the first scroll brings them up before the move.
- One orange. On phones the top nav leaves the orange to the opening's Check dates; a chosen chip is white; the film on air has a white title and the one tally dot (critic-1-2, -10).
- The booking path (buyer-1-3 to -5, -9, critic-1-11, qa-1-2, qa-1-3). On narrow screens the form comes straight after the heading, so every Check dates lands with the Event field in view; "Step 1 of 2" under the button, "(optional)" on Dates and Place; a month tap brings the Dates field into view and flashes it; keyboard focus never lands under the bar. enquire.html: the organiser's label, consent and aside, no lit nav, step 2 brought into view. Media enquiries go by mail even with ENDPOINT set, because the Worker would refuse them (buyer-1-1; the change waits on the owner).
- Smaller fixes: "we" for the offer on both pages (the brief's production house), device-neutral verbs, the reel title over its comp, separated season pills, place lines without a leading middot, a centred "+", one source stamp under 31,250, Season as one bar with ticks (no invented count), sub-lines from the facts, a shorter and brighter quote band, a 72 px ringed play button, words only on rail posters in view.
**Kept, and why.** On desktop the header keeps its Enquire Now: there it sits far from the opening's button, hiding it unbalances the nav or makes Search jump when the nav unpins, and the home page shows the same pair. The call band's single corner bracket stays: it is the site's call band (styles.css: "the recess, the sheen and the corner bracket"), which the owner chose to keep on 25 Oct; only its floating tag moved into the kicker.
**Recommended** the order of the move above, because one clean pull-back (words out, shot back, pieces in, words last) is what makes it read as a camera and not a collage, and a director needs the move to explain the four pieces without words.
**Flags.** The Worker's media branch and the facts to supply are first in docs/v4-next-session.md. Desktop's two orange buttons on the first frame are a deliberate exception the owner may want to rule on.

## 4 Nov 2026: "Pull Back To The Coverage" built into the generator (chat 17)
**Asked.** Build my winning Media mock into the real generator from docs/designers/media-build-spec.md (A, H, P, K, R, Q, D, F, S, G items; enquire.html's media mode was another agent's).
**Built.** tools/v4_media.py writes the page (an UPCOMING list feeds the slate and the season's Next); one shared prototypes/v4/v4-media.css and v4-media.js for both media pages, linked with ?v= hashes; the About polish block dropped; Enquire Now goes to #dates on media.html only; tools/v4_media_preview.py packs the CSS and enquire.html.
**What changed from the mock, and why.**
- The move (the judges' "messy middle"): the shot now flies in front of the board, the other three slide in under it fully opaque, the Daily Highlights label rides on the shot (its dark foot across the shot's full width, never a box edge), and the heading and the shot's own labels show only where the shot no longer covers them. The shot is the Daily Highlights link at every stage; the opening's words stop taking taps once half faded.
- Phone: a swipe rail of 280 px posters on a numbered line (01 Before the race to 04 Mid-season), the shot's poster in the middle with both neighbours peeking. The move takes 0.8 of a screen; on touch, a stop between the ends finishes it the way it was going. Desktop keeps the row of four and free scrolling (its middle frames are clean now).
- The opening: each number names its source; both buttons on one row; the scrim measured to 4.5:1 or better at every size (the mock failed on tablets and the lower deck at 1440); logo slots with full names; the slate counts down, lights a steady "On air now" during task days, then shows [to supply]. The headline is always two lines, and the words compact on short screens, so the move runs from 360x640 to 1920x1080 (the owner's 390x683 had no room to spare before).
- Taken from F: coverage bars on the packages, the reach band (31,250 over the gaggle, the 2026 season on its dates with Today and Tapalpa lit), Open/Held/Booked months that fill the dates. From D: the season rows with a Watch on each, the "Most watched" line, the numbered "need" list as a production rider. My cropped-wing joint-post card went; "one joint post, two audiences" is now said in plain large type.
- Fixed on the way: the Piedrahita page's opening was broken by the old poster-shelf grid; portrait photos were listed at the wrong widths in srcset.
**Flags.** [to supply]: subscribers and followers, clips per task day, where sponsors appear beyond the joint posts, travel, rights, booking lead time, what an event provides, the quote's organiser, the 2027 calendar (EXAMPLE). Logo files still to come. After 14 Nov the slate needs the next comp in UPCOMING, and Tapalpa's views in V. PWC and Bassano sit on the season line at their films' and broadcasts' dates (the comps' own dates are not in the facts). The Race Behind The Race poster exists only at 540 px.

## 3 Nov 2026: the Media page as a broadcast media kit (built a mock, chat 17)
**Asked.** Rebuild the Media page to sell comp coverage to organisers and sponsors only, in the order of `docs/designers/media-brief.md`, as a broadcast media kit (calm, expensive, cinematic, orange like a LIVE tally light). A complete working mock at `prototypes/v4/samples/media-e/`, my own angle, not an average of D and F.
**Proposed: "Pull Back To The Coverage".** The first screen is one shot of a race as the audience sees it (the orange wing between clouds, SRS_5_T2_133-2, full bleed): a slate with a steady tally light ("Next: SRS Tapalpa, Mexico, 8 to 14 Nov 2026"), "Media · For organisers and sponsors", the promise "Your Comp, Seen.", a deck with the three results (comp seen, sponsors seen, pilots back), Check dates for your event and Book a Call, Covered for SRS and PWCA (logo slots), three numbers as a score bug (21,690 views of one event, 7,342 of one task day, 21h 42m live). Scrolling pulls the camera back until that shot is the Daily Highlights poster and the other three slide in, in event order, on a line through the four; scrolling up flies back in. The tally lamp marks the poster on air and moves to the one you point at. Then: packages as broadcast rundowns (Daily, Full Event with "Most chosen" EXAMPLE, Season; "Priced per event"; each Check dates picks itself in the form), reach (a joint post shown as a post, 31,250 views, 136 countries, a views-by-event board with Tapalpa as Next), the quote full bleed over the race (EXAMPLE), the 13 videos playing in place and 10 stills in the viewer, the three formats drawn to scale beside what I need, the FAQ, the dates form inside the site's call band with the 2027 season (EXAMPLE), the newsletter in one line. Phone: one bar with Check dates once the opening is gone; the nav's Enquire Now goes to the form.
**Recommended it** because one move tells an event director what they buy without words: the shot of their race is one of four pieces around their event, and every exit on the page leads to the same action. Reduced motion and no JS show the finished page (the opening, then the four).
**Tried and dropped.** "Seen." in the site's orange accent: white instead, so the button and the tally are the only orange beside the wing.
**Flags.** enquire.html has no media mode (it reads only trip and when, and asks pilot questions as required); media-srs-piedrahita-2026.html is still in the old dress; subscribers and followers [to supply]; the Tapalpa "Next" lines go stale after 14 Nov; a larger export of SRS_5_T2_133-2 for retina desktops; the owner turned down scroll-driven moves on the home opening (24 Oct), so the static order is the fallback.

## 28 Oct 2026: a loading screen (advice only)
**Asked.** Critique the second loader (scratchpad loader.html: drawn glider, speed lines, filled ridge, big per cent counter, canopy wipe; owner: "cheap build"), give one concept, back or kill horizon line, focus pull, ASCII terrain.
**Found.** Seven things at once; the glider is clip art of our own subject; speed lines are a stock trope; the counter and mono kicker are dashboard language; the ridge is a filled chart. Flags: the podcast state says 93 conversations (the owner's fact is 86); the meta lines show a broken "Â·"; on a phone the counter collides with the meta.
**Proposed: "The line becomes the horizon."** Nothing for 0.5 s; then a faint full ridge hairline traced from the hero photo's own skyline, an orange stroke drawing over it as real progress (critical assets done), the place in small spaced capitals; on load the dark above the line lifts, the photo is placed so its skyline sits on the line, a slow 1.04 to 1 push in hands over to the opening's giant name. Phone: same line full width, central part of the ridge. Reduced motion: no draw, a 200 ms crossfade. No JS: no loader.
**Back / kill.** Back horizon line (it is the concept). Kill focus pull as a loader (it needs the photo, which is what is slow). Kill ASCII terrain for the loader (needs three.js and the DEM, the heaviest things, and it is good-fella's signature); worth a look for the footer, where the owner saw it.
**Recommended** the horizon line, because one line that turns into the photo's real horizon explains the arrival without words and costs almost nothing to load.

## 28 Oct 2026: a grain map for every page type (advice; built by the chat)
**Asked.** Where the live film grain should be on, off, lighter or faded so it merges into the site.
**Found.** Ground sd 1.9, zero on a few surfaces: the opening's foot (finer shader grain, sd 3.3, meets the page's on a line), the footer ridge band, the destination route map and fly-through, the sitemap sky.
**Proposed.** Fix the opening seam (smoothstep over the bottom 22% plus a fading CSS grain band); grain as the footer's top layer over the ridge; grain on the route map (0.8) and on the fly-through's top and bottom edges; leave glass nav, photos, cards and text alone.
**Built (by the chat, agreed by D, E and F).** The opening crossfade, grain on the destination pinned layers, the sticky section menu. Not built: the footer ridge and the sitemap sky (F wanted the sky clean; a footer top layer doubles the grain above the ridge).

## 25 Oct 2026: a compass-like emblem on the listen-c posters (review only)

**Asked.** The owner wants a shape overlay "like I had, a compass or something", for a sense of adventure. Old plate (assets/podcast/plate.webp): a large distressed compass rose at eye level, identical on every card.

**Old fault.** Same big rose, same place, across every face: it read as a stamp or watermark, the grunge texture was clip art next to the site's fine lines, and it said nothing about the episode.

**Proposed.** (1) Bearing ring, cropped off the top right corner, its orange needle pointing to the guest's place from the lead trip, swinging as the strip pans; (2) coordinates set up the card edge; (3) the logo's wing arc over the head, drawn on hover; (4) contour lines with a summit mark; (5) a dotted flight track drawn on scroll, only from the owner's real tracks; (6) map graticule corner ticks.

**Does a shape help?** Yes, if it carries a real fact (the bearing to the guest's place) and moves with the strip; a fixed decorative stamp would not.

**Picked (1)** because it keeps the compass the owner liked but makes it true to each card and gives it a move the visitor drives; it needs a place per guest (globe-episodes.js), else `[to supply]`.

## 25 Oct 2026: overlay brainstorm for the listen-c posters (review only)

**Asked.** The owner on listen-c (posters back: live type on colour art, dark foot gradient, lean and light, length line): "how will overlays affect the look, what kind, types etc, just brainstorm."

**Proposed.** (1) Orange ember tint pulling the red toward the site orange; (2) the site's topo contours as hairlines on the art, drifting slower than the photo as the strip moves; (3) film grain; (4) the foot gradient into the page ground, not slate; (5) one light sweep as each card enters; (6) the title in outline that fills on hover. Flag: the foot gradient reads blue-grey, not the page ground.

**Picked (2) contours,** because they give depth through parallax and say "place" without words, tying the cards to the topo ground below the section.

## 25 Oct 2026: the "More conversations" strip, awwwards level (review only)

**Asked.** The owner, on the home rail in #listen (built today from listen-b): "I really like the previous design", wants agency-quality cards and strip. Compared fa877a47 (poster cards: red guest art, compass stamp, hook and name plate on the art, lean with a soft light) with today's grey portrait cards, title and meta under the photo, boxed arrows.

**Found.** Old did better: one poster per episode, type on the art, warmth, the card answered the hand. New does better: no compass, readable titles, honest meta, calm. Lost: warmth and depth; the grey row reads as mugshots, and hover brings back the red YouTube ground that fights the orange. I recommended the grey earlier; I was partly wrong, the fault was the red and the compass, not the colour or the plate.

**Proposed.** Cards: poster ratio, guest art as one warm duotone (ink shadows to the site orange in the light, CSS only), the plate back (hook in Poppins on the art, guest name under it), series and episode number as a small line above, meta under the card; the lean and soft light back, the light in the duotone's orange, no colour flip. Strip: heading "More conversations" at the section's second size, the strip is a scroll-driven pan on desktop (sticky, about 1.5 screens, vertical scroll moves the cards sideways, the art drifts inside its frame for depth), a thin readout line under it with episode numbers and an orange tick where you are, echoing the season line; arrows sit at the line's end. Phone: native swipe with snap, card about 78vw, same readout. Reduced motion / no JS: a plain swipe rail.

**Recommended** the duotone plate cards with the scroll-driven pan, because it gives back the warmth the owner liked in one on-brand colour, and the pan turns a list into a camera move the visitor drives.

## 25 Oct 2026: shrink the episode picture, let the globe lead (review only)

**Asked.** On listen-b's lead block the owner said the 560 px episode face is too big and wants the globe to dominate the section; the globe itself will later be swapped for the Encarta one, so only its place, size and look in the layout matter. Keep the lead trip (name, dates, play in place, chapter line, See the trip), the turn to the picked trip with the route lit, Hear another trip, More conversations.

**Proposed.** Yes, change: the face is the biggest thing and says "a man", not "where we fly". 1440: two columns, text 5 of 12 on the left, the globe 7 of 12 on the right, ring about 720 px (fits a 900 px tall screen), its top level with the KENYA name. Left column: KENYA, dates, then one row: a 160 x 90 picture, play, episode title and guest; the chapter line under it at column width; See the trip; Hear another trip as two text rows with a small play, no pictures. Search moves out of the header into the More conversations row. Legend and "Click a pin" become one grey caption line under the ring; zoom buttons sit quiet inside the ring's lower right. 390: heading, KENYA and dates, the globe full width (ring inside 358 px) straight after the dates, then the small picture row, chapter line, See the trip, the two other trips. The globe turns to the lead as it scrolls in from the departures, nothing else moves. Appearance fix: drop the compass bezel (ticks, N S E W, second ring); one hairline ring in the line token, orange only on the route and pins. Option 2 (not recommended): my earlier globe-first full-width hero.

**Recommended the side by side,** because the pick and the globe's answer must be on one screen, and a plain frame survives the Encarta swap unchanged.

## 25 Oct 2026: motion and flow for B with a lead trip (review only)

**Asked.** The owner chose the lead block for B (`prototypes/v4/samples/listen-b/`): the trip lit in the departures leads large (Kenya by default), the others small; the episode plays in place with Trim's chapter line (real length, real chapter starts from episode-meta.json); the globe turns to the lead trip and the orange route lights to it. My globe-led option was not chosen. Advise motion and flow only, do not build.

**Proposed.** Turn: one move, 0.9 s (`--dur-l`), ease in-out, then the route draws in season order from Kenya to the picked trip in 0.5 s (`--dur-m`, `--ease`); the rest of the route stays dim; picking an earlier trip pulls the lit part back; a new pick mid-move retargets, never queues. No idle spin. While audio plays only the playhead moves (linear, real time); chapter jumps cut, no glide; picking another trip pauses and keeps the place. Flow: no entrance motion; the departures' lit row already picks the lead, so the orange hands over; cut the dead dark after the call band to the normal section gap. 1440: lead block and globe side by side on one screen, the small trips under the lead, so the answer is seen when you pick. 390: lead, small trips as a swipe row, globe under; the globe makes its turn as it scrolls into view. Reduced motion: cut to the place, route shown lit; the playhead still moves. No JS: Kenya lead as plain HTML, play is a link to the episode page, the chapter line static with ticks linking to the chapters, no globe box. Data: the episode JSON has only "52 min", so the exact length comes from the player once loaded; trips with no episode (Kazakhstan, Peru) show no play button, not an invented one.

**Strongest point.** The route lit in season order up to the picked trip: it tells "this trip is stop N of one season" without words, the same story the opening's season line tells, so it must sit on the same screen as the pick.

## 25 Oct 2026: "something is missing" in B2, "Hear Where We Fly" (review only)

**Asked.** The owner, on refined B (`prototypes/v4/samples/listen-b/`): "There's something missing. Is it the size, the feel, the appearance, what?" Judged in the whole page flow at 1440 and 390 (opening, departures, call band, this section).

**Found: a hero moment, which is a scale problem.** The page goes cinema (KENYA about 260 px tall over a full photo), then timetable, then this section opens at the same size as the call band above it (a 36 px heading, a paragraph, a search box). Its only big thing, the globe, sits about 1000 px down, after the cards. So it reads as one more block, not a new chapter, and the page never climbs back up after the opening.

**Proposed.** Make the globe the section's first screen: full width, about 85 to 90 vh (phone: full width, ring inside 358 px), "Hear Where We Fly" set big over its top (about 120 to 140 px desktop, 52 px phone, one step under the opening's name), the place rail sitting on the globe's lower edge, search moved under the rail. The move: as it scrolls in, the globe turns once to Kenya, the route pulls back to the planet. Smaller: (1) nothing plays; a podcast section with no visible "listen" on a card; (2) about 190 px of dead dark between the call band and the kicker, plus the band's empty right half; tighten so the globe follows the call.

**Recommended the globe-first hero,** because the opening's grammar is one huge thing per screen and this section breaks it; one big round world answers "where we fly" without words.

## 25 Oct 2026: refine option B, "Hear Where We Fly" (review only)

**Asked.** The owner chose B for the home podcast section and asked whether it can be refined "keeping awwwards in mind". Review `prototypes/v4/samples/listen-b/`, do not build. Known faults: trip cards reuse the opening's photos; a compass rose over every card and red YouTube art fight the orange; the globe ring is cut off on a 390 phone; "More conversations" stands sideways; "most streamed" has no source.

**Proposed, ranked.** (1) One calm card art: no compass, guest art in grey with colour back only on the card pointed at, the globe popup uses the card art, not the YouTube thumbnail. (2) New owner photos for the trip cards from `img/hero/` (Kenya Kerio Valley; India Billing launch and Dhauladhar, one each), Panchgani a type card until a second photo is `[to supply]`. (3) One India header over both India cards. (4) "More conversations" flat in the header row with a grey rule: orange = our trips, grey = the rest, same key as the globe legend. (5) Name the 15 honestly: "Latest conversations", newest first from episode-meta.json, unless the owner gives a source. (6) Phone: shrink the globe so its ring fits inside 358 px. (7) The globe draws the route: a thin orange arc joining the trip places in season order, Kazakhstan and Peru as hollow orange pins with dates and "See the trip". (8) My round 1 turn, adapted: the globe is below the fold while you point at cards, so instead it turns once, as it scrolls into view, to the last card pointed at (Kenya by default).

**Recommended (1) most,** because Design is 40% of the score and today the cards read as YouTube thumbnails with a stamp on top; one quiet art system lets the single orange (trip lines, pins) carry the meaning.

## 25 Oct 2026: round 1, the #listen section (podcast rail and search)

**Asked.** One concept for `#listen` (search plus the most-streamed rail), how it follows the season line and leads into `#map`, and whether the two should merge.

**Proposed: "Turn to the Voice", and merge #listen with #map.** Desktop: heading and search top left, the existing globe top right (about 560px, still), the rail full width under both. Phone: heading, search, globe at full width, rail swiping under it. One interaction: point at or focus a card (on a phone, the card that snaps into place) and the globe turns to that guest's place, lights its pin and reads out e.g. "Honorin Hamard, 1588 km SSW". Same grammar as the departures (point at a row, the season line answers), but time becomes place. Data: episode-meta.json and globe-episodes.js only (all 15 rail episodes have a place). Remove: the map's own heading and kicker, the "Click A Pin" link to podcast.html#map, the globe's idle spin, the card tilt light, the card hover overlay that repeats the plate; platform buttons become one quiet line. No JS: rail full width, no globe box. Reduced motion: the globe cuts to the place.

**Recommended it, because** the globe stops being a second section that repeats the episodes and becomes the rail's answer, so the visitor sees "these voices come from all over" without words. Honest limit: most top guests sit in the Alps, so most turns are small; Everest (Girard) and Canada (Gadd) give the big swings. Flagged: the intro says 80 conversations; episode-meta.json has 93 entries and the latest is Episode 80.

## 25 Oct 2026: a cursor shine on the departure rows?

**Asked.** Should the departure rows (option A, built) get a soft light that follows the mouse, like the episode cards' `v4-tilt` light, on top of the 4% wash, the orange bar and the glider flight.

**Answered: No.** The row already answers three ways, and the glider flying along the line is the move that tells "this row is these dates". A light sliding sideways under the cursor would be a second thing travelling sideways at the same moment and pull the eye off the glider. The card light suits photo cards; these rows are a timetable.

**Fallback offered (not recommended).** If the owner wants the link to the cards, swap the flat wash for the light, never add it: white at 6%, about 240px wide, full row height, following the cursor left to right only, mouse only (`hover: hover` and `pointer: fine`). Phone, keyboard focus and reduced motion keep the flat 4% wash.

## 24 Oct 2026: whole-site study, v4 at 48bfc475 against v4 now

**Asked.** How the whole site can reach Awwwards level, and how far v4 has come since 48bfc475, from my angle (scroll as story, hand-offs, navigation).

**Found.** The gains are the home opening and true route data (India 2027, Panchgani everywhere, a new Panchgani page). The other pages barely changed. The five gaps, in order:
1. Home tells the places three times (opening, fly-by without Panchgani, departures).
2. The opening does not fly into its place: "into the picture" is only wired to the old fly-by, and Kenya opens on a different photo.
3. With no JS, home hides its departure rows, three fly-by photos and the list signup.
4. Place pages are dead ends; Panchgani's page is flat, and the episode sidebar and About cards miss it.
5. The route line is drawn four different ways, and the Expeditions atlas has empty map between stops.
Flagged: Panchgani's hero is credited to Michael Gebert.

**Recommended: make the route the navigation.** Tap a place and fly into its page; the end of each page flies on to the next leg. Why: one move shows the site is a season of trips without words, and the parts already exist (v2-immersive.js depth transitions, the season line, the cloud move).
File: the chat's scratchpad `designers/study-E.md`.

## 24 Oct 2026: round 2, the section after the opening

Read D's and F's round 1. Dropped my photo shrink (WebGL risk, varies with
the auto-advance); took D's pixel-matched line, per-row bars and lit last
place, and F's scroll-drawn spine and glider for phone only. Held my ground:
on desktop the line stays across and the rows unfold out of their bars as you
scroll, both ways. Voted for this merge; second F (scroll still tells it).
File: the chat's scratchpad `designers/round2-E.md`.

## 24 Oct 2026: round 1, the section after the opening

**Asked.** What the section after the opening (#destinations: the "See
Where We Fly" fly-by, "Every Departure" timeline and table, the call band)
should do and look like, judged on the Awwwards criteria, since the opening
already tells the season, places and dates.

**Proposed: "The Line Unfolds".** Give the section a new job: the opening
is the dream (one place at a time), this is the decision (every departure
side by side). The opening's season line is the thread. Scroll out of the
opening and the current photo shrinks into its marker on the line; the line
rises to the top of the section and the nine departure rows drop out of
their bars in date order (photo frame, dates, length, group, level, price,
status). Pointing at a row lights its bar and the glider flies to it. The
call band is the last row. Phone: the line stands upright down the left,
cards hang off their months, the glider moves down as you scroll. Scroll up
folds it all back. Reduced motion and no JS: line above the finished list.
Drop the fly-by (a second carousel repeating the opening), the separate Jan
to Nov timeline and the "See dates" buttons.

**Recommended it, because** one move turns the opening's progress line into
the timetable, so the visitor sees "these are all the dates" without words,
and comparing beats waiting for a carousel. Risks: do the shrink with the
still photo, not the WebGL canvas; rows under bars need width (plain stagger
from 861 to 1200 px); the auto-advance means the shrinking photo varies.
Proposal file: the chat's scratchpad `designers/round1-E.md`.

## 24 Oct 2026: my own entry

**My angle.** I think in camera moves the visitor drives. Scroll tells the
story: pull back from one place to the whole route, then fly back in. If a
move explains the site without words, it is the right move.

**What I proposed, and why.**
- Round 3, "Pull Back to the Route" (23 Oct). Scrolling pulled the camera
  back from C2 until the photo was one of four frames; the other places slid
  in, in flying order, and an orange line joined them into a route with dates
  and prices. Scrolling up flew back in. Why: one move shows the site is a
  route of trips, not one photo. F won.
- DSC_9492 (24 Oct). Option B: one move, started by time, finished by scroll.
  A 4 s start went 30% of the way; scroll took it on and back. The valley
  grew to 1.20, the gliders shrank to 0.84 and only ever went away. Why:
  motion should answer the visitor. Not chosen; the owner took D's and F's
  slow timed follow shot.
- Panchgani (24 Oct). It had no dates then, so: set apart from the dated
  line, facts [to supply], not under India (that trip is Bir Billing). The
  wing at its real small size, to show how big the land is. I said no push.
  The owner chose this, then gave it dates and a shallow left circle, which
  beats my still frame.

**What I would do next.** Give scroll one job: as the visitor scrolls past
the opening, the photo shrinks into its marker on the season line, so the
route is the last thing they see. Ask for a larger Panchgani original; it is
1500 px wide and goes soft on big screens.

**The next transition.** A small pull back and fly in, not a wipe. About
1.6 s, soft start and stop. First 0.5 s: the old place keeps flying forward
while its frame shrinks to 94% and dims. Next 0.6 s: it slides out the way
the route goes, while the small glider on the season line flies the leg.
Last 0.5 s: the new place comes in at 104% and settles to 100% as its pass
starts, so nothing turns back. The new letters settle, then the wing glides
in. A drag scrubs it; reduced motion is a plain cut. It plays every 14 s, so
it must stay small.

## Starter (24 Oct 2026, from docs/v4-next-session.md)
- Round 3 (23 Oct): the first screen is C2; scrolling pulls the camera back
  until the photo is one of four frames, the other places slide in in flying
  order and an orange line joins them into a route with dates and prices;
  scrolling up flies back in.
- 24 Oct, DSC_9492: proposed option B (scroll drives a bigger move); not chosen.
