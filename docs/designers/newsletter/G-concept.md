# Designer G (inbox): newsletter concept, contest round 1 (12 Nov 2026)

Mock: `prototypes/v4/samples/newsletter-g/index.html` (shots: `shot-390.png`, `shot-1440.png`, and
`shot-390-images-off.png`, the same email with every image blocked).

## The idea in one line
**"The Letter From the Field":** a short letter from the owner at Tapalpa, then the week as live text you can read
with images off: one photo, a scoreboard built as an HTML table, three film rows, one talk, the season list, Patreon.

What I rely on in the brief (`docs/designers/newsletter-brief.md`, Design rules): "One column, Gmail on a phone first;
real text, not text in pictures; images with alt text and the email still readable with images off." And the voice:
"a short personal opener in the owner's first person (Aninder Singh), then brand-style sections (Paragliding Atlas)."

## Subject and preview (two each, no em dashes)
| | Subject | Preview line |
|---|---|---|
| **A (recommended)** | From the media team at Tapalpa | Rain stopped one task, 88 pilots made goal the next. Photos, films and results from my week on the media team. |
| B | Tapalpa so far: 4 tasks, 4 winners | My first letter to the list: the race in photos, films and results, plus a talk on flying Tapalpa. |

Why A: it is the first email the list has ever had, so it should read like a person, not a bulletin (Gmail on a phone
shows about 30 to 40 characters of subject: A fits whole). The preview carries the numbers. If the send is after
14 Nov, B becomes "Tapalpa: the final results" and the preview names the winner.

## The email, top to bottom
1. **Preview line** (hidden, with filler so Gmail does not pull body text in after it).
2. **Masthead.** A 3 px orange rule; the white Atlas logo (alt text "PARAGLIDING ATLAS", styled, so it reads as a
   wordmark with images off); dateline "TAPALPA · MEXICO" in live text, the welcome letter's "OSLO · NORWAY" habit.
3. **The opener, live text** (draft words; the owner rewrites them): "Hey fellow pilot," / "I'm writing from Tapalpa,
   Mexico, where I'm on the media team for the SRS Advance Edition, 8 to 14 November. Every evening the day's photos
   go up, free to save, and a highlights film goes up on YouTube." / "This is the first newsletter I've sent to the
   list, so here is the week in one place." / "Aninder". The greeting is the welcome letter's own.
4. **The photo.** One picture, full width: SRS_6_T1_62, the gallery's own cover (the owner's pick, COMPS lead),
   alt "A yellow and blue wing high over the white greenhouses and the lake bed at Tapalpa, Task 1"; live caption
   "Task 1, 8 Nov. Photo: Aninder Singh". THE PHOTOS / "Every task, every photo, free to save" / "The Tapalpa page
   fills up each night by task. If you flew, look for your wing." Button: **See the Tapalpa photos**
   (media-srs-tapalpa-2026.html).
5. **The race so far** (a table, never an image). "Four tasks, four winners", "Sports class, provisional results
   from SRS on 12 Nov." Task 1, Sun 8 Nov, 59.1 km: Matthijs Groeneveld NLD, 26 in goal. Task 2, Mon 9 Nov, 41.3 km:
   Arnold Castro ARG, stopped by rain at 14:40, the only pilot in goal. Task 3, Tue 10 Nov, 58.7 km: Abel Varga HUN,
   88 in goal. Task 4, Wed 11 Nov, 82.4 km: Brian Duffy USA, nobody in goal, furthest at 65.6 km. A lit panel with an
   orange left edge: overall 1 Andrés Tello Alvarado MEX 3137.6, 2 Bill Belcourt USA 2953.5, 3 Chaeden Luebberke USA
   2897.0; first woman Lynsey Haynes CAN, 5th overall. Link: **Full results on SRS scores**.
6. **The films.** Three rows, newest first, each a 16:9 photo of the same task as its poster (D's rule) at 128 x 72,
   the title, the length and the film's own line from COMPS: Task 3 Highlights 6:41, Task 2 4:36, Task 1 4:48.
   Link: **Watch the newest film**. Task 4's film joins when it is on YouTube.
7. **The talk.** No picture. "Miguel Gutiérrez explains flying in Tapalpa", "53 minutes on how this place flies,
   recorded here during the comp. [to supply: one line on who Miguel is.]" Link: **Watch the talk on YouTube**
   (yhHoRUJtyOY).
8. **The 2026 season.** "Every event now has its own page": four text rows, each a link: PWC Super Final (Pegalajar,
   Spain, May, 5 highlight films), SRS Bassano (Monte Grappa, Italy, May, 5 live broadcasts), SRS Piedrahita (Spain,
   22 to 29 Aug, 325 photos and the task films), SRS Tapalpa (Mexico, 8 to 14 Nov). Link: **The whole season on the
   Media page**.
9. **Patreon.** A quiet panel, the owner's own line "Like what you see? Join me on Patreon", button **Join on Patreon**.
10. **Honest footer.** "Touch The Sky With Glory"; "You get this because you joined the Atlas list at
    paraglidingatlas.com." The owner's address for questions; **Unsubscribe** in one click; Open in your browser;
    "Paragliding Atlas · [to supply: postal address]".

Two orange buttons in the whole email (photos, Patreon); every other section has one text link. That is the "one
clear action per section" rule, and it keeps orange the single live light the site uses it for.

## Why it gets read and clicked
- **It survives the inbox.** Gmail, Outlook and many work accounts block images until asked. With images off this
  email still reads top to bottom (see shot-390-images-off.png): the letter, the results, the film titles, every
  link. A newsletter set as pictures would show grey boxes.
- **The numbers are the hook.** Results are the thing a pilot opens a comp email for; as live text they are
  searchable, copyable, readable by screen readers and never blurry.
- **One photo, chosen.** One strong picture leads to the gallery that holds hundreds; more photos in the email would
  make it heavier and give fewer reasons to click.
- **Small and safe.** 22 KB of HTML (Gmail clips at about 102 KB), tables and inline styles, fluid without media
  queries (Gmail with non-Google accounts ignores them), buttons as table cells so Outlook draws them, a ghost table
  for Outlook's width.

## Where email cannot match the site (said plainly)
- **Fonts:** Poppins and DM Sans load only in Apple Mail and iOS Mail. Gmail and Outlook show Segoe UI, Helvetica or
  Arial. The sizes and weights are set so it still looks like the site.
- **Buttons:** the site's skewed buttons need CSS transforms that Gmail strips: square buttons here. Dark text on
  #ff7517 (about 7:1) instead of white (under 3:1 on that orange), so the label reads at any size.
- **Dark ground:** dark is kept, as in the welcome email. Gmail's app and Outlook may still shift colours a little in
  their own dark modes; the ground and panels use `bgcolor` as well as CSS so Outlook keeps them.
- **No motion, no grain, no season line drawing.** Email cannot run them safely.

## What I would steal from the others
I have not seen their entries (we work alone this round). I would take any photo choice or headline from D, E or F
that is stronger than mine, and the scoreboard should stay a table whoever wins.

## Flags for the chat (near the job, not yet right)
1. **Two season links are dead today:** media-pwc-pegalajar-2026.html and media-srs-bassano-2026.html return 404 on
   paraglidingatlas.com (12 Nov); they are built on the branch but not live. Push them before the send, or drop the
   two rows.
2. **The live welcome email is a picture of a letter** (assets/email/welcome/v1/letter.jpg, 1200 x 1760). With images
   off a new subscriber sees nothing of it, and screen readers read only its alt text. Worth a live-text version
   later (not this round; the owner decides).
3. **The YouTube title of the talk says "Maxico"**: "Miguel Gutiérrez Explains Flying in Tapalpa, Maxico during SRS -
   Advance Edition 2026". The owner may want to fix it before the email points 28 people at it.
4. **Postal address:** MailerLite needs one in the footer; the account's address still reads "M 46" per the
   handover. [to supply].
5. **Images for the real draft** go to `assets/email/newsletter-2026-11/` (new folder; the chat copies the JPEGs from
   `prototypes/v4/samples/newsletter-g/img/`) or MailerLite's file storage. Never the .webp copies.
6. **The welcome promised "about four emails a month"** (old welcome copy); this is the first. Not an issue for this
   email, but the cadence promise should match what the owner will really send.
