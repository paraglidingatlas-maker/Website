# Event landing pages, round 1: designer E (Cloudbase), "Pull Back to the Race"

Sample: `prototypes/v4/samples/event-e/` (index.html = SRS Piedrahita, pwc.html = PWC Super Final, shot-390.png,
shot-1440.png; `make.py` writes both pages from the live Piedrahita page's shell).

## The direction in one line
The page opens on one moment of the race; one screen of scroll pulls the camera back until that moment sits in its
place on the race, task by task; a tap flies you into a task; at the foot the camera pulls back once more, to the
season, and flies you into the next comp.

## The answers
**Gallery or a page above it?** The gallery page, made immersive, at the same URL. A link from WhatsApp, the
organiser or the Media page lands on the whole event, and a pilot is one tap from their task's photos. A page above
the gallery adds a tap between a pilot and their photo, and splits one event across two URLs. The two shared URLs
(`media-srs-piedrahita-2026.html`, `media-srs-tapalpa-2026.html`) stay, and so do their `#task-2` and `#SRS_5_T2_44`
links: the shared gallery still handles them.

**Films only (PWC, Bassano).** The same template; the race line is made of films instead of photo tasks. Each film
opens on a frame from its own footage (YouTube's own stills of the owner's video, not the designed covers with faces
and lettering), so the page is full of real pictures with no photos in the repo. Each chapter: the day, its film
playing in place, three frames from that film (a tap plays it), its length, views, YouTube date and the episode page.
The totals carry the weight: 5 films, 38 minutes, 21,690 views. A missing film shows as a quiet dashed slot
("Task 3, Film [to supply]") so the jump from Task 2 to Task 4 is not a mystery.

**Easy to navigate (phone).**
- A task: the race line (one scroll down) or the sticky task line; one tap.
- The films: Piedrahita's films lead each task (as the owner asked on 9 Nov); PWC is all films, one tap from the bar.
- The photos: "Find your photos" drives the move to the race line; one more tap opens a task.
- Back to the season: "The 2026 season" on the opening, and "2026 Season" at the right end of the sticky line, from
  anywhere on the page; one tap.
- Next or previous comp: the season at the foot shows all four, this one ringed, and Before / Next; two taps from
  anywhere (Season, then the comp).

**Immersive: the signature moment.** The pull-back. The opening photo (Piedrahita: the gaggle, SRS_5_T3_63) shrinks,
as one camera move, into its own frame on the race line, so the visitor learns without words that this is one
moment of Task 3, and that the race has three tasks. The picture never stretches: its box scales and the picture
inside is counter-scaled so it always covers it, and the race line is revealed under the shot as it pulls away (no
fades over the ground). Scroll drives it both ways; nothing moves on its own. The foot repeats the move outwards: the
season, and a tap on another comp grows its frame to fill the screen before that comp's page opens on the same
picture.

**Its cost on a mid-range phone.** Per scroll frame: two transforms and three opacities on composited layers, no
layout, no paint of the photo (it is decoded once at 1600 px). Far less than the Media page's pull-back, which moves
four posters and the board. Measured only in desktop Chromium (no frame drops, no sideways scroll at 390x683,
390x844, 1440x900); a real Android check is still to do. Under reduced motion, without JavaScript, or on a screen too
short for the race line, there is no move: the opening and the race line stand one after the other.

**One template.** Per event the chat fills one entry (beside COMPS in tools/v4_comp_gallery.py): edition, place,
dates, facts, the lead photo (or the lead film), one photo per task, the task lines, films per task, and the season
row (the Media page's SEASON and UPCOMING already hold it). Shared code: one event stylesheet and script (the
opening, the move, the race line, the films chapters, the season), plus the existing gallery, viewer and play in
place. Photo counts come from photos.json; views and lengths from V.

**File names.** Keep `media-<series>-<place>-<year>.html`: the two live ones stay, new ones follow
(`media-pwc-superfinal-2026.html`, `media-srs-bassano-2026.html`). Season rows on the Media page link to them.

## The page from top to bottom, on a phone
1. The opening: the lead photo full height (a film's frame across the top, words below, for films only), "The 2026
   season" link, edition and place, the giant name and year, dates, category, pilots and countries, "325 photos,
   3 films by Aninder Singh", Find your photos (orange) and Watch the films, "Scroll to pull back to the race". The
   nav's Enquire Now hides on phones over the opening, so one orange.
2. The pull-back (0.9 of a screen), then the race line: a vertical orange line, one row per task (its photo, the
   task's line, its counts).
3. The sticky task line (the gallery's, F's glider and all) with 2026 Season at its right end; one task at a time;
   the films, then the photos; the viewer as today.
4. The gallery's media enquiry band, as today.
5. The season: four frames (PWC, Bassano, Piedrahita ringed "You are here", Tapalpa "On now" in its own time zone),
   Before and Next, the Media page link. Footer.

PWC: the same, with the bar (Day 1, Task 1, 2, 4, 5) and the films chapters in place of the gallery.

## What it costs to build
About a day: the event script and stylesheet are written; the work is moving them into the generator, an EVENTS entry
per comp, the Media page's rows linked to the pages, and a real phone check. Bassano needs its page (five broadcasts,
the same films template).

## Flags (found on the way)
- The PWC Day 1 cover on YouTube reads "12.05.2027 - 23.05.2027" (2027 for a 2026 event). The comp's own dates are
  still [to supply], as are its pilots and countries and official event link.
- YouTube's frame stills (maxres1 to 3) are not a documented address and could vanish; for the build, grab the
  frames from the owner's footage and host them in media-2026 like the photos.
- Piedrahita's Day 1 film sits under Task 1 (no Day 1 photos); Task 3 has no film.
- Bassano's broadcast frames carry the stream's LIVE overlay: honest, but busier than the others.
- Desktop: the race line uses about half of a 900 px screen; bigger frames would help.

## What I would steal from the other two if I lose
I worked alone and have not seen their rounds. From their past work: Trim's contact sheet of true-ratio frames for
"find yourself", and Turnpoint's task line with the glider (already in the shared gallery, kept here as the sticky
bar). If either has a stronger answer for films-only events, I would take it in place of mine and keep the pull-back
as the opening.
