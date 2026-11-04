# Comp gallery page brief (chat 19, 4 Nov 2026)

## The job
Every comp the owner (Aninder Singh, Paragliding Atlas) covers gets its own photo gallery page. Tapalpa first (SRS
Advance Edition, Tapalpa, Mexico, tasks 8 to 14 Nov 2026, 7 tasks), then the Piedrahita page
(prototypes/v4/media-srs-piedrahita-2026.html, today about 20 photos with zoom and the task videos) is rebuilt the
same way. The owner asked the three designers to "brainstorm amongst themselves and do their magic".

## Who it is for
Pilots who flew the comp, their friends and family, and fans. A pilot lands from a link (the organiser's post, a
WhatsApp group, Instagram) usually on a phone, often on the evening of the task, wanting to find photos of themselves,
download them for free to post, and maybe buy the full-size original. The page is also proof for organisers that the
coverage is professional (the Media page sells to them), so it must feel premium, not like a stock-photo shop.

## What the page must do (owner decisions, 4 Nov)
- Browse photos by day (task). About 50 new photos a day during the comp, so up to ~350 per comp. Days are added one
  at a time while the comp runs (a day with no photos yet must look intentional: "Task 4 photos tonight" or similar).
- Tap a photo: see it big (the site already has a zoom viewer in prototypes/v4/v4-media.js, viewer()).
- Free download of the web copy (the 2400 px WebP), one tap.
- Buy the original: EUR 1 per photo, a payment link per photo (owner chose "per photo" over a basket). The payment
  provider is not chosen yet: the link is [to supply]. After payment the owner sends the original by hand (a Drive link
  by email). The buyer must be able to tell the owner which photo (the file name, e.g. SRS_5_T2_133-2) and their email.
  Show the delivery time as [to supply].
- Licence/usage terms of the free copy and the original: [to supply] (the media repo says "All rights reserved").
- Optional idea, the owner has NOT decided: helping a pilot find "photos of me" (by glider colours, pilot number,
  name tags). Propose it if you believe in it, with what it costs to run (who tags 350 photos a comp, and when).
- Must scale to many comps: one page per comp, same template, a gallery index link from the Media page and the event.

## Facts (only these; never invent)
- Piedrahita: SRS BGD Edition, Piedrahita, Avila, Spain, 22 to 29 Aug 2026, FAI CAT 2, 120 pilots from 54 countries.
  Task videos: Day 1 cuGs7Lk6Dt4, Task 1 uCEfssE40u8, Task 2 NXUEyPQ3V4E. Photos by Aninder Singh.
- Tapalpa: SRS Advance Edition, Tapalpa, Mexico, tasks 8 to 14 Nov 2026, 7 tasks, up to 120 pilots, 44 countries.
  No Tapalpa photos exist yet: use the Piedrahita photos as stand-ins in the sample and say so.
- Photos available now (web copies only, never originals): 20 Piedrahita stills on
  https://paraglidingatlas-maker.github.io/media-2026/srs-piedrahita/STEM-800.webp, -1600.webp, -2400.webp for STEM in:
  SRS_5_T1_9, SRS_5_T2_133-2, SRS_5_T2_64, SRS_5_T2_76, SRS_5_T2_83, SRS_5_T3_121, SRS_5_T3_127, SRS_5_T3_150,
  SRS_5_T3_166, SRS_5_T3_172, SRS_5_T3_21, SRS_5_T3_27, SRS_5_T3_38, SRS_5_T3_47, SRS_5_T3_57, SRS_5_T3_63,
  SRS_5_T3_64, SRS_5_T3_66, SRS_5_T3_86, SRS_5_T3_92 (T1/T2/T3 = task). A local copy is in /home/user/media-2026/.
  Do not use a photo twice on one page unless you say why.

## The site's rules (unchanged, from media-brief.md)
Dark ground, one orange, Poppins display, DM Sans text, tokens in prototypes/v4/v2.css. Buttons only btn-solid (with
inner span) and btn-lines. No em dashes in copy. A missing fact is [to supply] (class v2-tbd). Reduced motion and no
JavaScript show a usable page. Ambient motion only subtle, slow, stops under reduce motion, pauses off screen. Tested at
390x683 (the owner's phone in the Claude app), 390x844 and 1440x900, no horizontal scroll. Fast on a phone over hotel
wifi: lazy-load, 800 px thumbs, never load 2400 px until asked. Lessons from the Media page (chat 18, the owner called
its animations "patchy"): never animate clip-path, masks or big box-shadows per scroll frame; move things with
transform and opacity only.

## Working rules for this round
- Never run ./build.sh, tools/v4_build.py, tools/v4_gates.py or any build; never commit or push. The chat does that.
- Preview server: http://127.0.0.1:8765/ is already running with the repo root as site root (do not stop it).
  Screenshots: node with NODE_PATH=$(npm root -g), require('playwright'); set sessionStorage v4ld=1 to skip the loader.
- Write only inside your own folder (named below) and your own notebook.
