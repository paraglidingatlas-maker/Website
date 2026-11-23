# SRS 2027 race calendar: put it online (owner's ask, 23 Nov 2026)

From the calendar design chat (session_018Da7i8GvmpTqQuksKDnhdU). The owner is making a downloadable SRS 2027
race calendar, one page at a time, from his own SRS 2026 Tapalpa photos. His words on 23 Nov: "put this online
and put the lable in the place next instead of srs lvie" and, earlier, "a digital calendar for download like a
luxry immersive experiecne to go on the webnsite".

## The job
1. A calendar page on the site showing the pages finished so far (cover, January to August today; September to
   December follow, then wallpapers and the complete PDF). Each page viewable large and downloadable; "Add to
   calendar" with srs-2027.ics. Dark, immersive, the site's own look. Say plainly that the remaining months are
   on their way.
2. The nav slot that carried "Live from SRS" (tools/v4_nav_live.py; its window ended 17 Nov, but the committed
   pages and the live owned pages, media* and others, still show it) now carries a link to the calendar page
   instead. Suggested label "SRS 2027 Calendar", short "Calendar"; no pulsing "live" dot, since nothing is live.
   The phone menu (src/v4-menu.js) follows the header. Mind the translated pages: a new English string in the
   nav must not make /de/ /fr/ /es/ /zh/ stale.

## What is in this folder
- pages/NN-name-2400.webp and -1200.webp: the nine finished pages (A4 landscape, 2400 and 1200 px wide).
- srs-2027.ics: the five rounds as all-day events (St Jean Montclar marked tentative).
- source/: how the pages are made (build.js with Playwright; fx.py, grade.py, dusk.py, depth.py for the photo
  treatments). The design chat keeps the working copies and will push new pages to this branch.
- Photos used (all from media-srs-tapalpa-2026): cover SRS_6_T6_138, Jan T6_66, Feb T6_100, Mar T4_54,
  Apr T4_94, May T4_152, Jun T4_118, Jul T3_45, Aug T3_57. Credit: Aninder Singh / Paragliding Atlas.

## Facts (sportsracingseries.org/events, read 23 Nov 2026)
R01 Lijak, Slovenia, 15-21 Mar 2027 (confirmed) · R02 St Jean Montclar, France, 20-27 Jun (provisional) ·
R03 Gemona, Italy, 17-24 Jul (confirmed) · R04 Krushevo, North Macedonia, 22-29 Aug (confirmed) ·
R05 St Andre, France, 12-19 Sep (confirmed; the SRS page spells it "St Ande").

## Not decided by the owner (use judgement, tell him what you chose)
- The exact nav label and the page's address.
- Whether the draft PDF goes up now or only when all twelve months exist (the design chat suggests: only when
  complete; until then each page downloads as an image).
