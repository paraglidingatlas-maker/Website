# Event landing pages brief (chat 22, 12 Nov 2026)

## The job, in the owner's words (12 Nov)
"Every event page to have its own landing page which is immersive and easy to navigate; feel free to apply 3 designers
to run a contest between them to make a most viable page." A contest: each designer brings one full direction, the
chat judges (the Juror only with the owner's yes), then the winner is built with the best of the others.

## The events (the Media page's "The 2026 season", tools/v4_media.py SEASON and UPCOMING)
1. PWC Super Final: 15th Paragliding World Cup Super Final, Pegalajar, Spain, May 2026. 5 highlight videos
   (V in tools/v4_media.py: Day 1, Tasks 1, 2, 4, 5; titles, views, lengths, dates are there). No photos in the repo.
2. SRS Bassano: SRS Skywalk Bassano Edition, Monte Grappa, Italy, May 2026. Live commentary: 5 broadcasts,
   21 h 42 min on air (Task 2, Task 3, Task 4 parts 1 and 2, Task 5 the final day). No photos in the repo.
3. SRS Piedrahita: SRS BGD Edition, Piedrahita, Avila, Spain, 22 to 29 Aug 2026, FAI Category 2, 120 pilots from 54
   countries. 325 photos (T1 48, T2 131, T3 146) and 3 videos (Day 1, Task 1, Task 2); task lines in
   tools/v4_comp_gallery.py COMPS["piedrahita"]. Gallery page today: prototypes/v4/media-srs-piedrahita-2026.html.
4. SRS Tapalpa: SRS Advance Edition, Tapalpa, Mexico, 8 to 14 Nov 2026, on air NOW (Task 5 is 12 Nov). Practice and
   Tasks 1 to 4 photos so far, task films T1 to T3 with their lines (COMPS["tapalpa"]["films"]). Gallery page:
   prototypes/v4/media-srs-tapalpa-2026.html. Chat 21 updates it every evening: do not touch its files.

Today each season row on the Media page (prototypes/v4/media.html, "The 2026 season") opens a "Watch" sheet; the owner
wants each event to open its own landing page.

## Who it is for
Pilots who flew the event, their friends and family, fans; and the organisers and sponsors who are shown the page as
proof (the Media page sells coverage to them). Most arrive on a phone from a link (WhatsApp, Instagram, the
organiser's post, the Media page).

## The questions each direction must answer
- Is the landing page the gallery page made more immersive (Piedrahita, Tapalpa), or a page above it? And what does
  an event with films only and no photos (PWC, Bassano) look like so it does not feel empty?
- "Easy to navigate": how does a visitor get to a day/task, to the films, to the photos, back to the season, and to
  the next/previous event, in one or two taps on a phone?
- "Immersive": what is the one signature moment, and what does it cost on a mid-range phone (the Media page's
  pull-back took chat 19 a day to make smooth)?
- One template for every future event (a comp a month): what does the chat fill in per event, what is shared code.
- File names / URLs (keep the two existing gallery URLs working: they are shared on WhatsApp and Instagram).

## Rules (all from the site's standing direction, docs/designers/direction.md)
- Nothing invented. Facts only from the repo (tools/v4_media.py, tools/v4_comp_gallery.py), SRS/airtribune and the
  owner's YouTube. A missing fact is [to supply] (class v2-tbd). No em dashes in copy.
- Site look fixed: dark ground, one orange, Poppins display, DM Sans text, tokens in prototypes/v4/v2.css; buttons
  btn-solid (with inner span) and btn-lines. Reuse the gallery's shared files (assets/v4 v4-gallery.css/js) and the
  Media page's viewer where they fit. Videos are youtube-nocookie embeds that play in place on a tap.
- Reduced motion and no JavaScript show the finished page. Ambient motion subtle, pauses off screen.
- Tested at 390x683 (the owner's phone in the Claude app), 390x844 and 1440x900. No horizontal scroll.
- Photos: web copies only (https://paraglidingatlas-maker.github.io/media-2026/<folder>/STEM-800|1600|2400.webp,
  photos.json lists them). Never a Drive link or id.

## What each designer delivers (contest round 1)
1. docs/designers/events/<D|E|F>-concept.md: the direction in one line, the answers to the questions above, the
   page from top to bottom on a phone, the signature moment, what it costs to build, and what you would steal from
   the other two if you lose.
2. A working sample, prototypes/v4/samples/event-<d|e|f>/index.html (plus its own css/js beside it), showing
   SRS Piedrahita (photos and films) AND, as a second file pwc.html, the PWC Super Final (films only), with real
   facts and real photos/films. Self-contained: open it from a static server at the repo root.
3. Screenshots of your sample at 390x844 and 1440x900 in the same folder (shot-390.png, shot-1440.png).

Do NOT run ./build.sh, tools/v4_build.py, tools/v4_gates.py, git commit or git push (the chat runs one build at a time
and owns git). Do not edit files outside docs/designers/events/, your sample folder and your own notebook.
