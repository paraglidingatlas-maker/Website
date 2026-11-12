# F, Turnpoint: "The Season Opens Here" (event landing pages, round 1, 12 Nov 2026)

**In one line.** Every event page opens on its place, and at the photo's foot the 2026 season line opens, down an orange fan, into that event's own task line: one line takes you between events, the next takes you to the day, and the day is already on screen.

Sample: `prototypes/v4/samples/event-f/index.html` (SRS Piedrahita) and `pwc.html` (PWC Super Final, films only), with `event-f.css`, `event-f.js` and the generator `build_f.py`. Screenshots: `shot-390.png`, `shot-1440.png` (Piedrahita), `shot-pwc-390.png`, `shot-pwc-1440.png`.

## Why this angle
The people who arrive (a pilot from a WhatsApp link, a friend, an organiser shown the page) all ask the same three things in the same order: which event is this and when, where is my day, and what else is there. The home opening already answers "where and when" with a giant place name and a line of real dates. So the event page uses the same grammar, one scale down, and it adds no new navigation to learn: the season line is the event menu, the task line is the day menu.

## The questions

**Landing page = the gallery, or a page above it?** The gallery, made the landing. Same URL, same page, a new opening on top. A page above it costs every pilot one more tap to the only thing they came for (their photos), and splits the share links in two. The two URLs on WhatsApp and Instagram (`media-srs-piedrahita-2026.html`, `media-srs-tapalpa-2026.html`) keep working because they ARE the landing pages. The sample proves it: `index.html` is today's Piedrahita page (same markup, same `v4-gallery.css/js`, same viewer, same 325 photos), with only the opening changed, the season strip added above the task line and the season added at the foot.

**Films only (PWC, Bassano), so it does not feel empty?** The same template, with films in the stops instead of photos. The task line becomes the film line: Day 1, Task 1, Task 2, Task 3, Task 4, Task 5, each turnpoint with its length and the day it came out ("6:53, Out 14 May"). Task 3 has no film in the repo, so it stays on the line as a hollow, dashed turnpoint, "No film", and its stop says so with `[to supply]`: an honest gap reads as a record, not as emptiness. Each stop is one full-width 16:9 screen that plays in place on a tap (youtube-nocookie, the Media page's own `md-frame` and `v4-media.js`), with the title, length, views, date out, "Read the episode" and "Watch on YouTube". The opening is a frame from the event's own footage (in the sample, Task 4's relief map with the task drawn in red, darkened), the giant place name "Pegalajar", and the readout "5 highlight films, 21,690 views on YouTube, 3 Nov 2026". It never looks like a gallery with the photos missing, because nothing on it is shaped like a photo grid.
Bassano: the same, five broadcasts as five stops (Task 2, Task 3, Task 4 part 1, Task 4 part 2, Task 5), "21 h 42 min on air" in the readout. Not built in the sample.

**Easy to navigate, in one or two taps on a phone.**
- To a day or task: one tap on the task line, which is on the first screen at 390x683 and sticks under the nav after.
- To the films: one tap ("3 films" in the opening's readout goes to the first task with a film; each film sits in its own task, where a pilot looks for it).
- To the photos: none: the newest task with photos is open under the line on arrival ("325 photos" in the readout).
- Back to the season: one tap, "The 2026 season" over the strip (desktop) or the season list at the foot.
- Next / previous event: one tap. On a phone, the row above the strip: "<- SRS Bassano, May" and "SRS Tapalpa, Now ->". On a desktop, every event's name sits over its dates on the strip and is a link.

**Immersive: the one signature moment, and its phone cost.** See below. Cost: four to nine Web Animations on transform and opacity, once, about 1.2 s, no scroll handler, no WebGL, no layout. Measured at 4x CPU throttle on a 390 phone: the page's frame count during load is the same with and without the move (the gallery's own load dominates). It is not the Media page's scroll-driven pull-back, so it cannot stutter under a thumb.

**One template for a comp a month.** See "What the chat fills in".

**URLs.** `media-<comp>-<year>.html` in `prototypes/v4/`, as today: Piedrahita and Tapalpa unchanged; new `media-pwc-superfinal-2026.html` and `media-srs-bassano-2026.html`. A day keeps its hash (`#task-2`), a film stop too (`pwc...html#task-4`), so a link can open a day.

## The page, top to bottom, on a phone (Piedrahita)
1. The nav over the photo (as on the gallery and the home).
2. The opening, about 60% of the screen: SRS_5_T3_63, the kicker "SRS BGD Edition, Piedrahita, Avila, Spain", the giant name "Piedrahita 2026", the readout "22 to 29 Aug 2026, 120 pilots, 54 countries", then "325 photos, 3 films".
3. The season: "<- SRS Bassano, May" and "SRS Tapalpa, Now ->"; the 2026 line with the four events at their real dates (Piedrahita lit orange, Tapalpa white for now, the two May events grey), "Piedrahita, 22 to 29 Aug" over its bar; from the bar, a thin orange fan with a soft orange light inside it runs down to the ends of the task line.
4. The task line (today's, sticky): Task 1, 48 photos; Task 2, 131 photos; Task 3, 146 photos; the glider on the open task. At 390x683 all of this is on the first screen.
5. The open task: today's gallery (the day head and its line, its films, the photos in justified rows, the viewer with Save and Patreon, "Next leg").
6. "The 2026 Season": the four events as rows (dates, name, edition and place, what is there, one link), each event's dates marked on its row's own rule where the season line has them; "You are here" on this one in orange.
7. The organiser band ("Coverage like this for your event"), the newsletter and the footer, as today.

PWC is the same, with the films opening (2), the film line (4) and one screen per stop (5).

## The signature moment: "the season opens here"
On arrival, the event's orange dates on the season line open into its task line: the fan unfolds from the bar, the task line's track grows out of the lit dates to its full width, then the turnpoints drop into place left to right and the glider appears on the open day. About 1.2 s, once, only when the line is on screen at load and the page is not scrolled; nothing loops. Its finished state is the page itself (the fan, the light and the line stay), so reduced motion and no JavaScript show exactly that, still. It says, in the site's own grammar, "this event is one stretch of the season, and here it is up close", and it is the same move on every event page, so the season feels like one journey across pages.

## What it costs to build
- `tools/v4_comp_gallery.py`: the opening (taller lead, readout, "N photos, N films" links), the season strip from one list, the season rows at the foot, and a films-only mode (stops with a film, no photo grid). About half a day.
- `prototypes/v4/v4-gallery.js`: one rule: a stop with a film and no photos is state "film", not "Photos coming" (and "none" when it has neither, after the comp). Today a films-only page would say "Photos coming" on every task, which is untrue. In the sample `event-f.js` does this for PWC so the shared file stays untouched.
- `event-f.css` (about 10 KB) and `event-f.js` (about 7 KB) become part of `v4-gallery.css/js`.
- `tools/v4_media.py`: each SEASON row's "Watch" opens the event's page instead of the sheet (the "page" key, as UPCOMING already has).
- Checks at 390x683, 390x844, 1440x900, reduced motion, no JS. About a day in all, with the films-only pages for PWC and Bassano.

## What the chat fills in per event (the rest is shared code)
One entry: name, edition, place, dates (or the month and `[to supply]`), facts, official link, lead photo (or a film frame), the stops (name, date if known, photos from photos.json, film ids with title, length, views, date out, episode page), and the season list gets one row (its span on the line). A new night is a folder of photos and, if there is one, a film id.

## What I would steal from the other two if I lose
I have not seen their directions this round, so from what Trim and Cloudbase showed on the gallery (docs/designers/gallery/): from Trim, dim never hide and the every-day contact sheet as the no-JS view; from Cloudbase, the camera pull-back as the way OUT of an event to the season (the reverse of my zoom). I keep, whatever wins: the season line as the event menu with every event at its real dates, and the existing URLs as the landing pages.

## Flags (found on the way, not fixed)
1. PWC's "Day 1 Highlights" YouTube thumbnail reads "12.05.2027 - 23.05.2027". The year looks wrong (the comp was May 2026), and the dates are not in the repo, so the page shows "Comp dates [to supply]". Please check the thumbnail and give the comp dates.
2. PWC Task 3: there is no film in the repo. Was it flown, and is there a film? The stop says `[to supply]`.
3. The PWC opening and the film posters are YouTube's own frame grabs of the owner's films (i.ytimg maxres1, 2, 3), not stills the owner picked. For the build: a still from the footage, chosen by the owner, `[to supply]`.
4. Piedrahita task dates are still not known (`dates={}` in COMPS), so its task line shows no dates; the comp's own dates are on the strip.
5. Piedrahita's films still show their designed thumbnails (big baked words such as "TASK 1 - SUPERFINAL"); Tapalpa's film bands already use a photo of the same task as the poster. The build should give Piedrahita the same.
6. Bassano has no page yet; its row and its strip name go to the Media page's season until it has one.
7. The "Watch" sheet on the Media page and these pages would both show the films: once the pages exist, the sheet can go (one place per film).
