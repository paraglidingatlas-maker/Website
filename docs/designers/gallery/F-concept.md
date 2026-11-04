# F, Turnpoint: "Fly the Comp" (round 1, concept only, 4 Nov 2026)

**In one line.** The home opening's season line, shrunk to one comp: the task days on one line at their real dates, the newest day open under it, so a pilot taps their day and is looking at their photos in two taps.

**Why this angle.** The brief's pilot comes "on the evening of the task" from a WhatsApp link. Their first question is "is my day up yet", their second "am I in it". The page answers the first with the line and the second with the day's photos in flight order, and nothing sells until a photo is open.

## The flow, a pilot on a phone, the evening of Task 4
1. The WhatsApp link is `media-srs-tapalpa-2026.html#task-4` (or no hash: the page opens on the newest day with photos). First screen at 390x683: the comp's name, the task line, the day's head and the first row of photos.
2. The line: one turnpoint per date, 8 to 14 Nov. States, honest about dates and counted in the comp's own time zone (America/Mexico_City), not the viewer's: flown with photos (solid, "Task 3 · 48 photos"), today (orange tally, "Today · photos tonight"), passed without photos yet ("Photos coming", never a stale "tonight"), not flown (hollow, "No task", reason [to supply]), to come (dashed, date only). Task numbers come from the owner's list, not the date: a day lost to weather shifts them.
3. Find yourself: the day's photos in the order they were shot, in justified rows (time order kept, no masonry shuffle). Over the grid one row of wing colour chips (Orange, Red, Yellow, Blue, White, Green, and so on) filters the day; gaggle shots stay under All. Optional, and only if the owner wants it: one "where" label per batch (Launch, Start, Goal), cheap because the photographer stands in one place per batch.
4. Tap a photo: the existing viewer, the day as its set (swipe through all 50), 1600 px on a phone, 2400 px only on zoom or Save. At the thumb, a readout bar: "Task 4 · 11 Nov · SRS_5_T2_133-2" (the owner's file name; Tapalpa's naming is [to supply], so the Piedrahita name stands in here), then two buttons: **Save, free** (btn-lines) and **Original, EUR 1** (btn-solid).
5. Save: one tap. Phones with file sharing get the share sheet (Save Image goes to Photos, or straight to Instagram or WhatsApp); desktop gets a download named `SRS_5_T2_133-2.webp`. The copies are on GitHub Pages with `access-control-allow-origin: *` (checked), so a fetch to a file works; a plain `download` link would not across origins. No JS: Save is a link to the 2400 px copy. Under it, one quiet line: "Free web copy. Use: [to supply]. Photo: Aninder Singh, Paragliding Atlas."
6. Original: a small sheet rises inside the viewer: the photo's name with Copy, "Full size, sent by hand to the email you pay with, within [to supply]. Licence: [to supply]." and **Pay EUR 1** to the payment link [to supply], with the file name added to the link as its reference, so the owner builds one link per comp, not 350. The email comes from the checkout itself. If the provider cannot carry a reference, the sheet says "Paste the photo's name in the payment note".
7. Back from paying (if the provider returns): "Paid. SRS_5_T2_133-2 goes to the email you paid with, within [to supply]." Every photo also has its own link (`#SRS_5_T2_133-2`) so a pilot can send "this is me" to a friend.

## Layout
**390.** Nav; a short lead band (the day's best shot, about 300 px, the name "Tapalpa" in Poppins over its foot, "SRS Advance Edition · 8 to 14 Nov 2026"); the task line, sticky under the nav, 7 turnpoints of about 50 px each (date over, task under, the small glider on the open day); the day head ("Task 4 · 11 Nov · 52 photos", the video if there is one as the first, wider tile); colour chips in one row; rows about 150 px tall, two or three photos a row; at the foot "Next: Task 5, 12 Nov" to fly the next leg. No sideways photo rails (today's page has one at 390).
**1440.** The lead photo full-bleed at about 62vh, the giant name bottom left as on the home opening, the task line along the photo's foot at the opening's edges (72 to 1368 px) with each day's readout under its turnpoint; once scrolled, it slims to a sticky line of dots and dates. Day head left, chips right, rows about 300 px tall, the viewer's bar along the bottom with the buttons at the right.
**After the days.** The comp's videos (as today), then the organiser band, quiet and last (the page is proof for organisers), then the newsletter line.

## The signature moment
The glider flies the comp. Tap another day and the opening's small glider flies the leg along the task line to that turnpoint (0.6 s, a little lift and bank, transform only), while the new day's rows rise in the same direction behind it. It is the home page's own grammar, so the gallery reads as part of the Atlas, not a photo shop. Reduced motion and no JS: the day simply changes (no JS: all days stacked in date order, the turnpoints as anchor links).

## What scales (350 photos, many comps)
- One data file per comp written by a tool from the owner's export folder (file names, sizes, capture time from the originals, colour, where), one template, rendered to static HTML so no JS still works. A new day is a folder and one line.
- Only the open day is shown: about 50 thumbs at 800 px, lazy; first screen under about 0.6 MB (lead at 1600 plus six thumbs, measured sizes 213 KB and 60 KB average).
- Many comps: the Media page's season rows each get "Photos" (Piedrahita already has "All 20 from Piedrahita, by task"); a galleries index is the same season line of comps, newest lit.
- Owner cost per night for "find yourself": one colour keyword per photo at the cull, about 3 s each, so about 3 minutes for 50; a script can suggest the colour first. Not pilot numbers (not readable at these distances in the 20 stills), not faces (privacy, cost).

## What I would not do
No basket and no price on the thumbnails (the price shows once, in the open photo). No infinite scroll of all 350. No auto slideshow, no hover-only actions. No watermark across the photo (pilots crop it; the credit sits in the caption and file name; a corner mark is the owner's call). No second accent: the tally and Original are the only orange.

## One honest risk
Delivery by hand on the worst night: the owner edits Daily Highlights the same evening, and 30 EUR 1 orders after Task 1 are 30 Drive links by email. If the payment cannot carry the file name, each order also needs a reply to ask "which photo". So the delivery time must be honest ([to supply], perhaps "after the comp"), and the provider is chosen for carrying a reference.

## For Trim and Cloudbase
1. Newest day first, or date order? I keep date order on the line with the newest day open under it. Argue me out of it.
2. Cloudbase: if the scroll drives a move, show it never slows a pilot thumbing fast through 50 thumbs looking for one orange wing.
3. Both: say your "find yourself" in owner minutes per night during the comp. Mine is about 3, plus one label per batch.

## Flags on today's Piedrahita page (found on the way)
- "a highlight video each day": there are three (Day 1, Task 1, Task 2), Task 3 has none.
- The task dates are not on the page; the dates shown are the videos' publish dates (Task 2: 6 Sep) with no label. The line needs the real task dates: [to supply].
- The hero photos (SRS_5_T3_63, phone SRS_5_T2_133-2) appear again in the grid, so twice on one page.
- Every caption is "Piedrahita 2026, Task N": no file name, so nobody can name a photo to buy.
- The foot's "A free 30-minute call" is still not in the facts (flagged 3 Nov).

## Round 2 (after reading Trim's "Proof Sheet" and Cloudbase's "Pull Back to the Comp")
**Answers.** Trim 1: I place days, not photos, on the line; the days' dates come from the comp's schedule (8 to 14 Nov), not from EXIF. Photos keep file-number order; no clock, no map, no "where" label in the sample (no facts for it). Trim 2: yes, a photo row is on the first screen at 390x683; three taps from the link to Photos (photo, Save free, Save Image). Trim 3: a missed tag hides nothing; I took your dim, never hide. Cloudbase 1: the sixth photo is a swipe and two taps (Original, Pay), and a return from paying lands on the same photo; a basket stays out (the owner's call). Cloudbase 2: the line on both widths, because the days are back to back, so the line costs nothing in tap speed (each day a 50 px column, 44 px tall or more), and it says "today" and "to come" where chips cannot.
**Taken, with credit.** Trim: dim, never hide; the colour words read from the alt lines; the mean colour under each cell before it loads; back to the last photo's cell on close. Both: no YouTube art leading a day (a slim row when a video exists); uncropped justified rows. Cloudbase: back from paying on the same photo.
**Where I differ.** Trim stacks all days on one page: 350 photos is about 50 phone screens; I show one day, the line is the way between days, and no JS still stacks them. Cloudbase's contact sheet is a good "find yourself" but needs an extra export size and a big move on a phone; mine is a day you already chose plus an optional colour row.
**The three choices for the owner.** Trim: the sheet (every day, one scroll). Cloudbase: the camera (pull back to the whole comp). Turnpoint: the line (today, by date, one day at a time).
