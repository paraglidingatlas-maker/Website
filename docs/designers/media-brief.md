# Media page brief (chat 17, 3 Nov 2026)

## The job, in the owner's words
"This is my face to asking people to trust my site ... where I convert eyeballs into customers ... in an elegant and
effective way." On the second preview: "it does have the vibe of the site, but it's far from being a premium offering
page, this is where I sell my services." On the third: "this page still doesn't scream buy my services to the viewer."

## Who it speaks to: organisers and sponsors, exclusively (owner, 3 Nov)
Comp organisers (SRS, the Paragliding World Cup Association, national series, Coupe Icare) and the brands that sponsor
them. They are buying coverage of their event. Pilots and fans are served by the event pages (media-srs-piedrahita-2026.html),
not by this page; on this page they get at most the newsletter at the very foot.

## Owner decisions
- Prices are agreed in discussion: never shown. Packages show what is delivered, never a price ("Priced per event").
- Photos only, no showreel video yet. Videos are YouTube embeds that play in place on a tap (youtube-nocookie).
- Logos: the owner has SRS's and PWCA's OK to show their logos. Until the files arrive, draw a clean text lockup
  placeholder ("SRS", "PWCA") clearly marked as a logo slot.
- Organiser quote: coming. Meanwhile a generic placeholder, visibly marked EXAMPLE (it never goes live as is).
- Slots / availability for the 2027 season: example data, visibly marked EXAMPLE.
- The four posters (Pre-Race Show, Daily Highlights, Aftermovie, Race Behind The Race) stay as the signature moment,
  after the owner's Canva "SRS TV" board (four tall poster cards on dark, "Scan to Watch").
- No em dashes in copy. Nothing invented: a missing fact is [to supply] (class v2-tbd).
- Site look fixed: dark ground, one orange, Poppins display, DM Sans text, the tokens in prototypes/v4/v2.css. Buttons
  only btn-solid (with inner span) and btn-lines, data-hover. Reuse kit-head (kit-kicker, kit-title, kit-intro), kit-stats,
  cta-band, v2-chip, v2-nl. Reduced motion and no JavaScript show the finished page. Motion rules: ambient motion only
  subtle, slow, stops under reduce motion, pauses off screen, never behind reading text or beside the booking button.
- Tested at 390x683 (the owner's phone inside the Claude app), 390x844 and 1440x900. No horizontal scroll.

## The direction agreed (chat 17): a broadcast media kit
The pack a sports channel sends to rights holders: the production house behind a world cup, not a freelancer's
portfolio. Dark and cinematic, the owner's photos full-bleed, big confident type that states the result, numbers set
like broadcast graphics, orange used sparingly like a LIVE tally light, calm and expensive, never loud.

## The order the page should sell in (chat 17 plan, owner agreed)
1. The promise (a headline that states the result for the organiser), who hired him (logo lockups), three proof numbers,
   one primary action ("Check dates for your event") and Book a Call.
2. What every event gets: the four posters.
3. Packages, no prices: Daily (Daily Highlights + social clips + results newsletter), Full Event (Pre-Race Show + Daily
   Highlights + Aftermovie, "Most chosen" as EXAMPLE), Season (every event of a series + Race Behind The Race). Each with
   "Check dates".
4. Your audience, not just your video: the reach an organiser buys (joint posts on both channels, the numbers below).
5. Proof: the quote (EXAMPLE), the work (stills, the showreel of 13 videos that play in place).
6. What you get / what we need: delivery formats (16:9 videos, 9:16 social clips, web and full-size stills), delivery
   the same day or at the end of the week as needed, subject to internet on site, task finish time and access to footage;
   what the organiser provides: [to supply] beyond "internet on site" and "access to footage" (from the pitch).
7. FAQ for organisers (cost: priced per event after a call; travel: [to supply]; rights: [to supply]; how far ahead: [to supply]).
8. A dates form (event, dates, place, package, name, email) going to enquire.html?trip=media, with Book a Call and WhatsApp
   as the second options.
9. Newsletter at the very foot (one line), for the rest.

## Facts (only these; checked 3 Nov 2026)
- Hired by SRS (Sports-Class Racing Series, sportsracingseries.org) and the Paragliding World Cup Association. Wording: "covered for".
- 2026 comps: PWC Super Final, Pegalajar, Spain (15th Paragliding World Cup Super Final), May 2026: 5 highlight videos,
  21,690 views. SRS Skywalk Bassano Edition, Monte Grappa, Italy, May 2026: live commentary, 5 broadcasts, 21 h 42 min on
  air, 4,081 views. SRS BGD Edition, Piedrahita, Avila, Spain, 22 to 29 Aug 2026, FAI CAT 2, 120 pilots from 54 countries:
  stills and 3 highlight videos, 5,479 views. Next: SRS Advance Edition, Tapalpa, Mexico, tasks 8 to 14 Nov 2026, 7 tasks,
  up to 120 pilots, 44 countries.
- 13 comp videos, 31,250 views in all. Most watched: Task 1 Highlights, PWC Super Final (BRAX1XMU390), 7,342 views, 6:53,
  an 86.5 km sprint.
- The podcast: about 80 episodes, listened to in 136 countries (the site's About page). Pre-Race Show example: the episode
  "Pre PWC Kenya" with Nikolay Yotov (episodes/pre-pwc-kenya-nikolay-yotov.html).
- The four products (the owner's Canva pitches): Pre-Race Show, a Paragliding Atlas podcast preview episode to build
  anticipation with audiences and pilots who would like to know the venue and conditions; Daily Highlights, a long-form
  video each task day plus social clips and a results newsletter, showing task, results, race dynamics and what made each
  day special; Aftermovie, a highlights compilation: task details, racing strategies, leaderboard standings, fun factor;
  Race Behind The Race, BTS and athlete showreel, mid-season or as available, to explain what it takes to organise a comp
  and create a deeper emotional connection between audiences, athletes and organisers. Everything published as
  collaborative posts on both Paragliding Atlas and the organiser's channels. Start with the resources available and grow
  the deliverables as budget allows. Season coverage is possible (the SRS roadmap runs Q3 2026 to Q2 2027).
- Also offered: live commentary (as at Bassano), stills (as at Piedrahita).
- Book a Call: https://calendar.app.google/HaJMYuiomt5Db9eh8 . WhatsApp: https://wa.me/4796757456

## Material on disk (serve with the preview server on http://127.0.0.1:8765, site root = repo root)
- The current built page: prototypes/v4/media.html (generator tools/v4_media.py, script prototypes/v4/v4-media.js with the
  zoom viewer and play-in-place video). Its photos: prototypes/v4/img/media-tmp/ (STEM-800/1600/2400.webp for the 20
  Piedrahita stills SRS_5_T*_*, and poster-<key>-600/900.webp for the four posters).
- Screenshot helper: node with NODE_PATH=$(npm root -g) and require('playwright'); chromium.launch() needs no options.
  Set sessionStorage v4ld=1 in an init script to skip the site loader.
