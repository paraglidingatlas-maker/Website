# Newsletter, contest round 1: designer F (Turnpoint), "The Task Line"

Mock: `prototypes/v4/samples/newsletter-f/index.html` (shots `shot-390.png`, `shot-1440.png` beside it).
Facts checked on 12 Nov 2026, about 06:00 UTC: SRS scores (api.airtribune.com/srs/scores, Tapalpa = meet 93,
tasks T6.1 to T6.4, all PROVISIONAL), the owner's YouTube (vidIQ), photos.json of the Tapalpa gallery, the repo.

## The idea in one line
The email reads like a task board: the 2026 season line with Tapalpa lit, then Tapalpa task by task (date, distance,
what happened, who won, one film, one photo link), so a reader on a phone sees where I have been and taps the day
they want.

Why this angle: it is the site's own grammar (the home page's season line, the event pages' task line), so the first
email looks like it came from the same hand. And a list of days is the fastest thing to scan on a phone.

## Subject and preview (two each)
- Subject A: **Four tasks into Tapalpa** (recommended: plain, true, and it names the place readers saw on YouTube)
- Subject B: From the media team at SRS Tapalpa
- Preview A: **82.4 km and nobody in goal. The photos, the films and the rest of my season.** (recommended)
- Preview B: 484 photos free to save, three highlight films and a talk with Miguel Gutiérrez.

Both are dated: if the send is after 14 Nov, "Four tasks" becomes the final count and the numbers update (brief).

## The email, top to bottom
Dark, like the welcome email (#0e0f12 ground, #141519 card, one orange: #ff7517 for text and lines, #e5600a for the
one filled button). Poppins headings, DM Sans text, Arial fallback. 600 px, one column, tables, inline styles.

1. **Masthead.** The 3 px orange rule (welcome email), the white Atlas logo, "Field notes, 12 Nov 2026" on the right
   (the welcome email promised "field notes from the sites I fly").
2. **The photo.** SRS_6_T1_62, the owner's Tapalpa cover (yellow wing over the lake and greenhouses), full width,
   links to the photos page. Alt: "A yellow race wing over the lake and the greenhouses below Tapalpa, Task 1".
3. **The heading and readout.** Kicker "On now, SRS Advance Edition, Tapalpa, Mexico"; H1 "Four Tasks Into Tapalpa";
   a four-fact readout on one rule, like the home opening: 8 to 14 Nov 2026 | 4 of 7 tasks flown | 116 pilots |
   484 photos.
4. **The owner's opener** (first person, portrait from assets/email/portrait.png): "Hello from Tapalpa, I am in Mexico
   on the media team of the SRS Advance Edition. Every evening the day's photos go online, free to save, and a
   highlights film of the task follows. Four tasks are flown, three to go. Here is each day, and the rest of my 2026
   season, one tap each. Aninder". The owner should read it and put it in their own words.
5. **The 2026 Season.** A thin line, 1 May to 1 Dec at scale, each event a mark at its real dates, Tapalpa orange;
   months under it. Then four rows, dates on the left, one link each: PWC Super Final (May, Pegalajar, 5 highlight
   films, "Films"); SRS Bassano (24 to 30 May, Monte Grappa, live commentary, 5 broadcasts, "Broadcasts"); SRS
   Piedrahita (22 to 29 Aug, 325 photos and 3 films, "Photos and films"); SRS Tapalpa (8 to 14 Nov, orange edge,
   "On now", "every task, below"). Under it: "All four on one page: Media".
6. **Task By Task** ("Results provisional, from SRS scores on 12 Nov"). One row a task: a square photo of that day
   (the film posters the owner's page uses: T1_55, T2_44, T3_141; Task 4: T4_54), then "Task 1, Sun 8 Nov, 59.1 km",
   one line, the winner, then "Watch 4:48 | 99 photos".
   - Task 1: An opener that started low and ended with a long glide into the wind. Won by Matthijs Groeneveld, 26 in goal.
   - Task 2: Raced under a storm clock, stopped by rain at 14:40. Arnold Castro won, the only pilot in goal.
   - Task 3: The ridge, the lake bed into the wind and a cloud street home. Won by Abel Varga, 88 in goal.
   - Task 4: The longest task yet, and nobody made goal. Brian Duffy flew furthest, 65.6 km, and won the day.
     Film [to supply], 168 photos.
   - Tasks 5 to 7, to 14 Nov, to come (a dashed row, like the line's days to come).
   The lines come from the films' own descriptions (COMPS["tapalpa"]["films"]); every figure from SRS. "Watch" opens
   the film on the photos page (#film-task-N: the theatre, whose end card sends people to the photos), not YouTube.
7. **Overall after four tasks (provisional).** 1 Andrés Tello Alvarado MEX 3,137.6; 2 Bill Belcourt USA 2,953.5;
   3 Chaeden Luebberke USA 2,897.0. Then: "Bill Belcourt was on the podcast last year: the safety paradox" (his
   episode page; YouTube 29 Oct 2025). A free link from the race to the archive.
8. **Find Yourself In The Photos** (the gallery's own end-card words). SRS_6_T4_67 full width (orange wing over green
   hills); "484 photos from the practice day and Tasks 1 to 4, by task, free to save. The practice day's are by Paco
   Peciado." The one filled orange button: See the photos.
9. **Listen, 53 min: Miguel Gutiérrez on Flying Tapalpa.** A frame from the talk (the owner's video, no baked text);
   "Miguel talks about flying in Tapalpa: the airspace, local flying, the thermals, and what you need to know to fly
   here." (from the video's description). "Watch the talk" (YouTube yhHoRUJtyOY).
10. **Patreon.** "Like what you see? Join me on Patreon", an outline button (second to the photos), the brief's link.
11. **Sign-off.** "See you up there, Aninder" (welcome email) and "A question for the show? aninder@paraglidingatlas.com".
12. **Footer.** "Touch The Sky With Glory"; "You get this because you joined the Atlas list at paraglidingatlas.com.
    Not for you any more? Unsubscribe in one tap." ({$unsubscribe}); "Paragliding Atlas, postal address [to supply]".

Images off: every picture has alt text and a grey ground; the text alone tells the whole story (checked).
Pictures for the draft: JPEGs made from the owner's web copies (in the mock's img/), to be copied to a new folder
`assets/email/newsletter-2026-11/` with absolute URLs. Nothing in assets/email/ moves.

## Why it gets read and clicked
- The first screen on a phone has the place, the photo, the headline and four numbers: you know what this is in two seconds.
- Every row ends in a link, and every link is the next thing a reader wants ("Watch 4:48", "99 photos"). Lengths and
  counts set expectations, so taps are not wasted.
- One filled button (See the photos): a pilot's first question is "am I in it". Patreon is second, an outline.
- Honest dates: real task dates, "provisional", "to come", "[to supply]". Readers trust a list that says what it does not know.
- The season rows show the owner's whole year in four lines, so a reader who missed Bassano or Piedrahita finds them.

## What I would steal from the others
I have not seen D, E or G's concepts (we work at the same time). What I would look for: from G, the inbox craft
(Gmail dark-mode inversion, Outlook buttons, the preview text length); from D, one exact line per task that teaches
something; from E, a bigger single photo moment.

## Flags (near the newsletter, found while checking)
- **The Miguel Gutiérrez talk is not in the repo** (no episode page, not in episode-titles.json). It is on YouTube only
  (yhHoRUJtyOY, 53:23, out 10 Nov 03:08 UTC). Its YouTube title says "Maxico" (typo). Its description's newsletter link
  is a Google Form (forms.gle/PN3LGt8L589cmugT7), not the MailerLite list.
- **Task 4 film:** not on the channel at 06:00 UTC 12 Nov: [to supply].
- **PWC and Bassano pages** (media-pwc-pegalajar-2026.html, media-srs-bassano-2026.html) are on branch
  claude/chat22-events, not live yet: they must be live before the send.
- **Countries:** I left them out ("116 pilots"): the site says 44 countries, the handover says the 116 confirmed pilots
  come from 25. Owner to settle.
- **Bassano dates:** 24 to 30 May are SRS's task dates (T2.1 Sun 24 May to T2.6 Sat 30 May). PWC's comp dates are
  [to supply]; the mock says "May".
- **MailerLite needs a postal address** in the footer: [to supply].
- Dark emails: Gmail on iPhone may invert colours; G should test the draft there.
