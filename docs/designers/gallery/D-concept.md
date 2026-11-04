# Trim (D): the comp gallery, round 1 concept (4 Nov 2026)

**"Proof Sheet".** A photographer's proof sheet, finished: every frame uncropped at its own ratio, in shot order by day, no shop on the grid. The shop appears only when you lift a frame out, in one line under it.

**Why.** The brief: "it must feel premium, not like a stock-photo shop". A stock shop puts prices, carts and marks on every thumbnail; a gallery keeps them off and lets the photo lead. Tapalpa's Task 1 is 8 Nov, four days away, so this builds on parts that already work (kit-hero, the CSS justified grid in v4-media.css, viewer()). The sample uses the Piedrahita photos as Tapalpa stand-ins, labelled so. I wrote this without reading E's or F's concepts.

## The flow on a phone (390x683, from a WhatsApp link)
1. **Land.** The organiser's post links one day (`...#task-3`); the comp link lands on the hero. Either way, a row of photos is on the first screen.
2. **Browse by day.** A sticky day strip under the header (`Task 1 · [n]`, `Task 2 · [n]` ...). A tap jumps to that day. Days are stacked on one page: no tabs hiding days, Find in page works, no JS shows the same page. On task days the live day carries one steady orange tally (media-brief.md: "orange used sparingly like a LIVE tally light"); it is gone after the comp. A day with no photos yet shows one empty hairline frame, "Task 4 photos tonight"; later days show only their name, and their date once the owner gives it.
3. **Find yourself.** Rows of true-ratio frames, 2 or 3 to a row, never under 150 px tall, in file-number (shot) order. 50 a day is about 7 phone screens, scanned by eye for your wing's colours.
4. **Open.** Tap and the frame lifts out (the signature, below). Swipe for the next photo of the day, pinch to zoom, swipe down to close.
5. **Save free.** One button, "Save photo" (btn-lines): it fetches the 2400 WebP and hands it to the phone's share sheet (Save Image, or straight to Instagram or WhatsApp). The file keeps its name, `SRS_5_T2_133-2`, so a pilot who comes back to buy can name the photo. On desktop it is a plain download.
6. **Buy the original.** "Original, EUR 1" (btn-solid) opens one line under the photo: "The full-size original of SRS_5_T2_133-2, sent by email as a Drive link within [to supply]. Pay with the email it should go to." Then "Pay EUR 1" opens the photo's payment link [to supply]. Our page holds no form and no email: the link names the frame, the payment page takes the email. The licence for both copies is [to supply], in one small line.
7. **Back.** Close, and the frame settles into the cell of the last photo you saw, the sheet scrolled to it, so you never lose your place among 50.

## Layout
- **390.** The hero cut to about 55% of the screen: the comp's lead frame (not repeated in the sheet), with title and dates on its foot and the stats below it. Then the sticky strip and the stacked days. Each day: kicker, title, one video row (a small 16:9 still, title and length; it plays in place), then the sheet edge to edge inside the gutters with 4 px gaps. Viewer: the photo above, a bar in the thumb zone under it (frame number, "12 of 52", Save photo, Original, EUR 1). Nothing sits on the photo.
- **1440.** The hero at about 72vh, the cinematic open the organiser judges us by; the stats are counted by the build (`[n] photos · 7 tasks · up to 120 pilots · 44 countries`). The strip is sticky under the header. Each day in two columns: a sticky quarter (task, title, count, the video playing in place) and three quarters of sheet at about 240 px rows, out to the gutter (today the grid stops at 62rem and leaves a dead third). Viewer: the photo at its own ratio up to 86vh, with one line under it: frame number and task on the left, the two buttons on the right; the hint line cut to "Arrows · scroll to zoom · Esc". The foot keeps the call band for organisers.

## The signature moment: the frame lifts out
Tap a cell. The photo rises from its exact place to the screen (transform and opacity only, 0.3 s), the sheet dims behind it, and only when it lands does the one line appear under it: frame number, Save photo, Original. Close, and it goes back into its cell. It only works because the sheet never crops: a cropped thumbnail cannot grow into the true photo without a jump. The 800 file makes the flight; the 1600 (phone) or 2400 (desktop) swaps in under it after landing, in the same frame with no visible change. Reduced motion: a cut. No JS: each cell links to its 2400 file.

## What scales to 350 photos and many comps
- One list per comp (tasks: title, date, video; photos: file, task, size, alt). The build makes every page from one template. Adding a day means 50 files and 50 lines.
- Each cell is painted in its photo's mean colour (one hex from the build), so on hotel wifi the sheet reads as the day's sky before the images arrive.
- The CSS justified rows already work without JS; JS only trues the edges. Each day uses `content-visibility:auto`; thumbs are lazy at 800 px (the 20 Piedrahita thumbs average 65 KB, so about 3.3 MB a day; an optional 480 px phone copy would halve that).
- Each day has its own link for the organiser's post. One gallery index (newest comp first, the live one with its tally) is linked from Media and from the event.

## Photos of me: highlight, never hide (optional, I believe in this version only)
Wing colour chips per day (orange, red, blue, yellow, green, white), read from the colour words in the alt text every photo needs anyway. Tap a colour and the other photos dim; nothing disappears, so a missed tag never hides a pilot's photo. The cost is the alt lines: about 10 minutes a night for 50 photos (the owner, or a drafted list the owner checks). No names or pilot numbers: they cannot be read reliably, and naming people in photos for sale is personal data. Not needed for 8 Nov; switch it on for a day once its alts exist.

## What I would not do
- No prices, carts, badges or marks on the cells, and no watermark across a photo.
- No square crops, and no hover zoom (today's scale 1.03 on the cells and 1.02 on the video art go: a zoom on a still reads as a fault).
- No filter that hides photos. No route map or clock of photos: the web copies carry no time or place (checked: none of the 20 has EXIF or XMP).
- No 2400 file on a phone until Save or a deep zoom (viewer() loads it on every open today).
- No YouTube art leading a day: the photos lead, the video is a row.

## The honest risk
Saving on an iPhone. The photos live on github.io and the page on paraglidingatlas.com, and browsers ignore `download` for a file on another domain. So Save must fetch the file (CORS is open, I checked: `access-control-allow-origin: *`) and hand it to the share sheet; older phones fall back to opening the image for a long-press. A saved WebP must also be tested posting to Instagram and WhatsApp on a real phone before 8 Nov. If that fails, the free copy needs a JPEG beside it.

## Flags on today's Piedrahita page
- "Stills and a highlight video each day" is not true: Task 3 has no video and Day 1 has no stills.
- The hero photo is also in the grid (T3_63 at 1440, T2_133-2 on the phone), and the page does not say why.
- On the phone, Task 2 packs four photos into one 96 px row (the portrait cells are 64 px wide), too small to find yourself in.
- The viewer's caption has no frame number, and "20 Chosen stills" is typed in, not counted.
- A link per photo means 350 payment links a comp. If the provider takes a reference in the address, one link serves them all [to supply].

## For Cloudbase (E) and Turnpoint (F)
1. The web copies carry no time and no GPS. If your idea places photos on a route, a clock or a map, where do 350 times a comp come from by 8 Nov, and where does a photo with none go?
2. On 390x683, from the WhatsApp link to "it is in my Photos": how many taps, and is a photo on the first screen? Mine: yes, and three taps (photo, Save photo, Save Image).
3. If you tag "photos of me", what does a pilot see when their photo was missed? Mine dims the others and never hides one.
