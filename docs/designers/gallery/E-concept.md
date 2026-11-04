# Comp gallery, designer E (Cloudbase): "Pull Back to the Comp"

**The idea.** One camera, three distances: the photo, the day, and the whole comp as a contact sheet. A tap flies in, a swipe down (or Back) pulls back, so a pilot sees every frame at once, spots their own wing and lands on it.

## The flow, on a phone
1. **Land.** A link with #task-3 lands on that day. The bare link opens on the newest day's lead frame, full bleed: "Tapalpa 2026", "SRS Advance Edition · Tapalpa, Mexico", "Task 3 · 52 photos" (counts from the build; numbers here are examples). The first scroll (half a screen, not pinned) pulls back: the frame shrinks into its place on the comp line, one frame per day in date order. A day with no photos yet is an empty hairline frame with its name and "Photos after the task" ("Photos tonight" when the owner marks it as flying).
2. **By day.** A slim day bar sticks under the nav: D1 T1 T2 ... T7, lit where you are, dim when empty, Scan at its end. Each day: name, date, count; its highlight video as one slim row that plays in place ("Watch Task 2 Highlights, 13:46"); then the wall in justified rows, in the order shot.
3. **Find yourself.** Scan pulls the camera back to the contact sheet: every frame of the comp, small, under thin day labels (phone 7 a row, about 48 px). The frame you were on stays put and lit while the rest shrink in around it. A pilot knows their wing, and at 48 px a wing is still its colours. Days flies back in.
4. **Open.** Tap a frame and it grows into the viewer from where it sat (today's viewer: pinch, drag, arrows, plus swipe sideways). Its foot: the photo's name, SRS_5_T2_133-2 (always shown: it is the order reference), "12 of 52 · Task 2", **Save free** (btn-lines), **Original · EUR 1** (btn-solid). The address becomes #SRS_5_T2_133-2, so a pilot can send a friend that exact photo.
5. **Save free.** One tap, and only now does the 2400 copy load. On a phone it opens the share sheet (Save Image to Photos, or straight into Instagram or WhatsApp); on a computer it downloads. Checked: the photo host sends access-control-allow-origin *, so the site may fetch it. Under the button: "How you may use it: [to supply]".
6. **Buy.** Original opens a small sheet inside the viewer: the frame, its name, "Full-size original, EUR 1, sent by email within [to supply]", one email field, **Pay EUR 1** to the payment link [to supply], carrying the name and the email in the link where the provider allows it; where it cannot, a Copy name button and "paste it in the payment note". Back from payment: "Paid for SRS_5_T2_133-2. Your original comes by email within [to supply]", on the same photo, so the next one is one swipe away.
7. **Pull back.** Swipe down, Back or Esc: the photo flies home into its own frame, lit orange for a beat, in whichever view you came from.

No JavaScript: the comp line and day bar are links, each frame opens its own #name target with the same two links (the 2400 file and the payment link), loaded only when opened. Reduced motion: every move is a cut.

## Layout
- **390.** Opening 72% of the screen, words on its foot; the comp line a 4 by 2 grid of day frames (cover, name, date, count). Day bar 44 px under the nav. Walls inside the 16 px gutter, rows about 150 px (2 to 3 frames), 4 px gaps. Contact sheet 7 a row. Viewer foot in two rows, both buttons side by side at thumb height.
- **1440.** Opening full bleed; the pull back lands in one row of day frames across the measure. Then a sticky left rail (3 of 12 columns): the days upright with date and count, the lit one with the season line's orange tick, Scan at its foot; the walls in the other 9, rows about 300 px. Contact sheet 16 a row, a whole comp in about a screen and a half. Viewer: the photo as big as the screen allows, one foot bar (name and position left, the two buttons right).

## The signature moment
The pull back. Drag a photo down and it shrinks under your finger, the day (or the whole comp) opens behind it, and it lands in its own frame, lit. It is the opening's move and the Media page's pull back into the four posters, so the site keeps one camera; and the contact sheet tells an organiser "every day, covered" without a word.

## What scales (350 photos, many comps)
- One data file per comp (name, place, dates; days with date, state, video, photo names and sizes). A day is added by adding its list; the empty day is the default state, not a special case.
- Walls load 800 px copies only near the screen, with sizes that never pick 1600 on a phone. The contact sheet needs a small copy: a 240 px size in the export (about 8 KB each, 3 MB a comp) or one contact-sheet image per day made by tools/. With only the 800 copies (62 KB on average, measured), Scan would pull about 22 MB.
- The pull back animates only the frames on screen (60 at most); the rest cut into place.
- The gallery index is the same camera pulled back once more: each comp as one small contact sheet (season, comp, day, photo), linked from the Media page and each event page.
- "Photos of me": I believe in it, as the contact sheet, which costs nothing to run. Colour tags (one keyword at the cull, about 2 s a photo, 2 minutes a night, by the owner) could later add colour chips that dim the other frames; I would wait until pilots ask. Pilot numbers and names: no, rarely readable in the air, and someone would tag 350 a comp.

## What I would not do
Masonry columns (they scramble the order and the pilot loses their place). A buy button or a price on the wall (it turns a gallery into a shop; you buy after seeing it big). A watermark across the free copy (the stock-shop look; the terms say it in words). A long pinned scroll move (half a screen, unpinned, and a #task link skips it). Any 2400 px copy before Save or zoom. A carousel of days, a slideshow, face or bib recognition.

## Honest risk
The pull back is premium only if it is smooth on a mid-range Android over hotel wifi, and the Media page's moves needed three fix passes after the owner called them "patchy". So: transform and opacity only, 60 frames at most, the small copy; if the sample stutters, it becomes a plain cut and nothing else depends on it.

## Flags on today's Piedrahita page (measured at 390x844 3x and 1440x900)
- The viewer caption says "Piedrahita 2026, Task 1": no photo name, so a buyer cannot say which photo.
- sizes="(max-width:700px) 70vw": on a 3x phone all 20 tiles load the 1600 copy; at 1440, 8 of 21 do.
- Phone: Task 2's four photos share one row 96 px tall (portraits 64 px wide) and start 3.3 screens down, under a full-width video cover. Too small to find yourself.
- 1440: the walls stop at 992 px, leaving the right third of the screen empty.
- The YouTube covers (SRS purple and red art) lead every day and fight the one orange; a slim row keeps the video and lets the photos lead.
- Day 1 has a video and no photos, Task 3 photos and no video: the template must make both look intended.

## For Trim and Turnpoint
1. Both: per photo at EUR 1 means a pilot with six photos pays six times. Inside the owner's "per photo", how does your flow make the sixth as quick as the first?
2. Turnpoint: should the day bar take the season line's grammar (each day at its real date on one line, today marked) or stay plain chips, faster to tap? I lean chips on the phone, the line on the rail at 1440.
3. Trim: if you propose colour tags or a pilot finder, who tags 350 photos, and at what hour after a task? If nobody can, is the contact sheet enough?

## Round 2 (after reading Trim's "Proof Sheet" and Turnpoint's "Fly the Comp")
**Answers.** Trim 1: nothing of mine needs a time or a place; order is the file number within each day. Trim 2: from the WhatsApp link, three taps (photo, Save, free, Save Image), and a photo is on the first screen at 390x683 (the opening is the newest day's lead frame and opens as that frame). Trim 3: I tag nothing; Scan shows every frame, so nobody can be missed. Turnpoint 1: date order, agreed, with the opening and the tally on the newest day. Turnpoint 2: you were right, and I dropped the opening's scroll pull-back. Nothing on my page moves when you scroll; the camera moves only on a tap (Scan all, Days, open, close). Turnpoint 3: zero owner minutes a night. The build needs one small copy per photo (below).
**Stolen, with credit.** Trim: true-ratio frames everywhere, the contact sheet too (a cropped thumb cannot grow into the photo without a jump); each frame painted in its photo's mean colour before it loads; no form and no email on our page (the payment page takes the email). Turnpoint: honest day states ("photos tonight" only on the day), counted in the comp's time zone in the real page; one payment link per comp with the file name as the reference, not 350 links (Trim too).
**My view of theirs.** Proof Sheet is closest to mine and its lift-out is the right viewer move. But 50 frames a day at 150 px is about 7 phone screens, so a whole comp is about 49 screens to search for one wing; my Scan exists for that. Fly the Comp has the best day line. Showing one day at a time keeps the page light, but it hides the other six from a pilot who flew them all and from Find in page. Its chips filter photos out, where Trim's dim the rest and hide none, which is safer.
**Sharpened.** Three clear choices for the owner: Trim, one day at a time at true size; Turnpoint, the day picked on the comp's line; mine, the camera pulls back to the whole comp on one screen. Small copy needed: 320 px on the long edge (about 10 KB on average, 3.5 MB a comp); the sample uses the 800 px copies.
