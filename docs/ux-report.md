# v4 usability pass (7 Oct 2026)

The owner's brief: fix measured usability problems on v4, re-measure, report.
Not a redesign: the look stays. Live site, `prototypes/v2/`, `rss-feed.js`,
`prototypes/v4/samples/` and `episode-meta.json` untouched; no switch-over.
All 27 items are done, each measured before and after (`tools/ux_measure.py`;
`docs/ux-measure/before.json` and `after.json`), the gates passed before every
push.

## What changed

**Trips.** The phone bar leads with the price (£1,100 per pilot, From
US$2,100), 69 to 75 px tall from 320 px up. The dates come at screens 10.6 and
11.5 on a phone (were 19.3 and 20.0): the gallery's pinned run is under three screens and
shows every photograph whole. Every question is in view; Flying Etiquette is a
band of its own. On a wide screen the section bar carries the price and Hold a
place. Hold a place opens the enquiry on that departure (trip, dates, length,
price), the form on screen one, the message optional. The hero's words keep a
darker shade over bright snow.

**Episodes.** The transcript uses the whole column on a phone (43 characters a
line, was 33), chapters are a list, not a sideways row. No card or link is
labelled with only a series name or repeats itself. Nothing jumps as the page
loads (podcast CLS 0.55 to 0.00, episode title 35 px to 1 px).

**Knowledge base.** The first idea within a screen and a half on a phone (was
3.3 to 4.2), the conversations one row to swipe. Every series page has the
trips' jump row. The hub says what each series is about (its own page's
question), has the site search at the top, no text under 12 px on a phone and
46 px altitude bands. Running text is in one size (secondary text in one
other), at most 82 characters a line (was up to 230).

**Search, podcast, topics.** The library's search sits under its title and
also finds topics, chapter titles and summaries ("collapse": 11 results, was
0). The site search puts trips first for trip words, shows the matching line,
and offers Topics, Library, India and Kenya when nothing is found. The podcast
opens with its newest episode and a play button that works when the feeds do
not. Topics: SRS and CCC, a box to narrow the 50 tiles, a caption for the
traces.

**Every page.** One main landmark, where the skip link lands. No text under
12 px on a phone. A Pause beside Wind sound wherever footage plays. Tap, not
Click, in the helper lines on touch screens. Bigger star targets on the
sitemap. Width and height on all 1,565 images. The enquiry form says under
each field what it needs.

**Weight.** Home 2.71 to 1.37 MB on a phone, India 4.19 to 1.46, Kenya 1.63 to
0.79, podcast 2.04 to 1.36, the hub, About and Flight Mechanics lighter too.
Of the ten pages measured, none is heavier as the preview server sends them;
as GitHub Pages sends them, the library is 0.7 KB (0.3%) heavier. Pages with no
photographs or footage to trim (the topic pages, the legal pages, 21 episodes
without a globe) carry about half a kilobyte more as sent: the main landmark,
image sizes and the rules every page now shares.

## What to check on your phone

1. India and Kenya: the bar at the bottom shows the price and clears the home
   indicator; scroll to Dates (about screen 11); the gallery shows each
   photograph whole; Hold a place opens the enquiry with the trip, dates and
   price at the top.
2. The India hero and the home page: the footage is the upright cut and loops
   (Safari plays the MP4 versions); turn the phone sideways and back.
3. Podcast: the newest episode under the two buttons; press play, then pause.
4. Any page with footage: Pause in the footer stops it, and it stays paused on
   the next page (not remembered in a Private tab).
5. An episode: the transcript reads full width, chapters are a list, the
   Listening mode button is there from the start.
6. A knowledge base series page: the jump row stays at the top while you
   scroll; the film strip's still arrives as you come to it.
7. Library: type "collapse"; the results appear under the field. Then type
   nonsense: it offers Topics.
8. Enquire: press Send with the form empty; a message under each field, the
   first one in view. The words are Safari's own.
9. Sitemap: the stars are easier to tap; the helper line says Tap.
10. Topics: type in Search topics; the tiles narrow.

Safari-only things the Chromium checks here could not see: the bar's
safe-area padding; the upright pictures chosen by `<source media>`; the MP4
clips; audio play on a tap (iOS); the larger star rings (CSS `r` on SVG: if
Safari ignores it, the old rings stay and taps still go to the nearest star);
sticky rows with a blurred background; the hidden clear button in search
fields; the names wall waiting for its font (`document.fonts`); the
smooth scroll to the first empty field.

## For you to decide

Nothing was changed for these; one screenshot each.

1. **Level bars.** The home page's trip cards show Level as bars: India 4 of
   5, Kenya 2 of 5, with no scale, which reads as the opposite of the copy.
   Keep, give them a scale, or drop them? `docs/ux-shots/q1-levels.jpg`
2. **About opening.** About opens on the glacier picture, not your portrait.
   Swap them? `docs/ux-shots/q2-about-opening.jpg`
3. **Countries.** Partners says 130+ countries reached; Podcast and About say
   136. Which one? `docs/ux-shots/q3-countries.jpg`
4. **Episode count.** Topics and the home page say 80 conversations, the
   library 86 episodes, the sitemap 93. Which count, and of what?
   `docs/ux-shots/q4-episode-count.jpg`
5. **Route length.** Kenya's route heading says 451 km end to end; the counter
   beside the map ends at 472 km (the legs add up to 194 + 17 + 15 + 100 + 146).
   Which? `docs/ux-shots/q5-route-km.jpg`
6. **From the work: "Srs" and "Ccc".** The pages now show SRS and CCC, but the
   two topic names are "Srs" and "Ccc" in episode-meta.json, so the topic
   pages' titles and structured data still say so (they must match the live
   site). Correct them at the source?

## How it is built

Run after the other v4 passes, in this order: `python3 tools/v4_phone_media.py`
(the phone pictures and clips, only what is missing), `python3 tools/v4_search.py`
(search-index.js, library-find.js), `python3 tools/v4_ux.py` (last; `--check`
says whether anything would change), `python3 tools/v4_min.py`. The pass's
rules for one kind of page are in `prototypes/v4/src/v4-ux.css` (each `@page`
section goes into those pages only, right after v2.css); the rules every page
needs are at the end of `src/v2.css`, with the few page rules the live audit
must not find inside a page (a hidden element on an episode, v2.css's own
tokens); its scripts are `src/v4-ux-*.js`.
`tools/v2_switch.py` now also carries `.webm` and `.mp4`.

An independent read-only check at the end confirmed nothing outside v4, tools
and docs changed, no em dashes were added, not one word of the Kenya copy
changed (only the fold button "One more question" went, with the fold), and
traced every new wording to the site. It doubted three: "Each topic's
conversations by date" (now "Conversations by date"), the library's "Every
topic" / "Browse the topics" (now "Topics"), and "Search topics" (kept: the
site's own "Search episodes" with its own "Topics").

## Item by item

| # | Item | Before | After | Commit |
|---|---|---|---|---|
| 0 | Measurement tool and baselines | the brief's numbers reproduced | `docs/ux-measure/before.json` | 9f490edf |
| 1 | Price in the phone action bar | "10 days, Next departure 21 Oct 2026" | "£1,100 per pilot, 10 days, Next departure 21 Oct 2026" (Kenya "From US$2,100"); 320 to 414 px, 69 to 75 px tall | ccb03bb5 |
| 2 | Dates sooner | Dates at screen 19.3 (India), 20.0 (Kenya) of 26; gallery 7.6 / 7.0 screens | Dates at 10.6 / 11.5 of 20; gallery 2.8 / 2.7 screens; route 3.2 / 4.2 | 685325b4 |
| 3 | Gallery framing | 30% of each photo shown on average (least 20%), up to 4.7x enlarged on a 3x phone | every photo whole in a landscape frame on an upright phone or tablet (100% shown, at most 1.1x) | f8f677de |
| 4 | Hold a place in context | generic heading; first field at y=840; message required; header Enquire Now shown | the departure's trip, dates, length and price under the title; first field at y=774 on a phone; message optional; header Enquire Now hidden on the enquiry page; mailto and the worker hook unchanged | a8f9bd93 |
| 5 | Nothing important folded away | India 5 of 10 questions in view, Kenya 5 of 6 (cancellation folded); Flying Etiquette one collapsed row at the end | every question in view on both; Flying Etiquette its own band after Before You Book, heading and first two paragraphs in view (510 / 494 characters), in the jump row | 602c47e4 |
| 6 | Weight on a phone | own-host bytes on arrival (3x phone): India 4.19 MB, home 2.71 MB, Kenya 1.63 MB | India 1.45 MB, home 1.37 MB, Kenya 0.79 MB. Phone cuts of the hero photos and clips (2:3, the same framing), only the first hero slide on arrival, gallery and the home fly-through photos when near. At the end of the pass, all ten measured pages again (see "6, at the end") | 95066dd7 |
| 7 | Desktop sub-navigation | the bar ends on a small "Enquire" | "Enquire", then the from price ("£1,100 per pilot", "From US$2,100") and Hold a place, held at the bar's right end while the links scroll (821 px and up) | 5c8064cd |
| 12 | aria-controls before the target exists | 2 dangling (v4-open -> v4Menu, v4-ls-open -> v4Listen) | 0: each button names its menu or screen once it exists | 5c8064cd |
| 8 | Transcript on phones | 264 px column, 33 characters a line | the time above each paragraph: 342 px, 43 characters a line | 438a6891 |
| 9 | Chapters on phones | 13 cards of 220 px in a sideways row; ticks 5 to 19 px; axe target-size: 10 nodes here, 36 on three more episodes | a vertical list (44 px rows); the timeline ticks and the audio player's chapter marks left out on touch screens; axe target-size passes on all four | 438a6891 |
| 10 | Titles that say nothing | 613 labels on 93 episode pages: 36 equal a series name ("Sky Gods"), 34 repeats in a block (the guest twice on a card) | 0 and 0: guest plus the descriptive part of the title ("Antoine Girard: Flying 8000ers"; cards "Flying to Win" over "Honorin Hamard, 108 min") | 406d1edd |
| 11 | Layout jumps at 1440 | podcast CLS 0.55; episode 0.06, hero title moves 35 px | podcast 0.00, episode 0.01 (title moves 1 px) | 406d1edd |
| 13 | Ideas first | first idea at screen 3.3 (Flight Mechanics), 4.2 (Risk vs Reward); tiles 2.3 / 3.2 screens | 1.4 and 1.4 (Sky Gods 1.5); the conversations are one row to swipe (0.3 screens) | b4490a64 |
| 14 | Series pages: a jump row | 13 series pages of 17 to 20 phone screens, no way to jump | the trips' jump row on all 13: each idea by its kicker, Worth Remembering, FAQ, the conversations; it stays at the top | b4490a64 |
| 15 | The knowledge base hub | 43% of characters under 12 px on a phone; altitude links 18 px tall; series names alone; no search on the page | 0% under 12 px; altitude links 46 px; each of the 13 series with its own page's question under its name; the site search at the top, under the introduction (screen 0.67) | b5639588 |
| 16 | Reading measure | at 1440 the longest lines: knowledge base 120 to 230 characters (folds, FAQ answers, a caption), Kenya 143, India 143; 8 sizes for running text (14.1 to 17.3 px) | longest lines 79, 82 and 74 characters (31 rem); 2 sizes, --fs-body for running text and --fs-body-s for secondary | 64abaed2 |
| 17 | Library search | the search 3.1 phone screens down, under the series; titles and guests only: "collapse" 0 results, "reserve" 3, "thermal" 1; nothing offered when nothing matches | under the title (screen 0.48), its first results right under the field; also matches each episode's topics, chapter titles and summary: "collapse" 11, "reserve" 9, "thermal" 5; when nothing matches, the matching topics, or a link to Topics | f2cb2d28 |
| 18 | Site search | "how much does kenya cost": the Kenya trip 4th; titles only; "Nothing found" | the Kenya trip 1st (trip words put trips first); each result with its matching line; "Nothing found" offers Topics, Library, India and Kenya | f2cb2d28 |
| 19 | Podcast: the newest episode | first episode link 5.85 phone screens down; no listen control anywhere when the feeds fail | the newest episode (Episode 80, its length, date, title and guest) under the two buttons, link at screen 0.86, its play button at 0.83; plays from the saved archive (episode-meta.json, mp3-map.json) whether or not the feeds answer, one player at a time with the feed's rows | e7b253c2 |
| 20 | Topics | "Srs" and "Ccc" on the tiles, chips, headings and search; 50 tiles and no way to narrow them; the traces on the tiles unexplained | SRS and CCC as the site writes them wherever they are shown (the page title and structured data stay as the live page has them, for the parity gate; the name is "Srs" in episode-meta.json, see the questions); a Search topics box under the introduction (Nothing found offers the library); a caption with a sample trace: Conversations by date, 2023 to 2026 | 35e03f66 |
| 21 | One main landmark | axe landmark-one-main failed on 33 of 60 views (20 templates at 390, 768, 1440); the skip link landed on a header outside any main on 18 templates | 0 of 60; every page has one main and the skip link lands on it (an episode's main is now the whole episode, not only its centre column); before-and-after screenshots of 21 templates at 390 and 1440 match | 35e03f66 |
| 22 | Small text on phones | under 12 px at 390: home 40% of characters, hub 43%, library 17%, sitemap 14%, flight options 14%, About 11%; smallest 8.3 px | 0% on all twelve pages measured; smallest 12 px (the last labels, from the episode rail to the trip's packing list, take the micro size on phones). Text drawn at 0 px, the trip hero's tab names that only a screen reader reads, is not counted | 8ea75c8e |
| 23 | Footage | no way to stop the moving footage; the trip hero's words over bright snow (India at 1440, the brightest frame behind the title: 124 of 255); at 1920 the 720p clip in a 1968 px box | Pause beside Wind sound in the footer of every page with footage (reads Play once paused, remembered from page to page); the shade behind the trip hero's words reaches further in (brightest frame behind the title 92, behind the sub-line 82); the clip is chosen by the box it fills (item 6), so 1920 gets the 1080p file | 8ea75c8e |
| 24 | Touch wording | 3 helper lines say Click on a phone | on a touch screen they say Tap, the site's own word ("Tap the centre to come inside"); with a mouse, Click; the headings are unchanged | 8ea75c8e |
| 25 | Sitemap stars | 93 stars with 17 px hit areas | 25.6 px; a tap goes to the nearest star within 30 px rather than to an overlapping ring; axe target-size passes | 8ea75c8e |
| 26 | Image width and height | missing: partners 56 of 63, hub 33 of 36, flight options 20 of 22, home 6 of 23, About 4 of 8, podcast 2 of 16 | 0 of 1,565 images on every v4 page (the file's own size; YouTube's fixed sizes for its stills); screenshots of 21 templates unchanged | 8ea75c8e |
| 27 | Enquiry form messages | an empty send: the browser's bubble on the first field only | a message under each of the 7 fields, in the browser's own words and the form's orange, the field's edge with it; the first brought into view and focused; each message goes as its field is put right; without script, the browser's checks as before | 8ea75c8e |
| 6, at the end | Weight, every measured page | the pass had made the pages without media to trim 1 to 3% heavier (its rules and scripts in the shared v2.css and v2-immersive.js), the Flight Mechanics page 32% (its film strip's 309 KB still now fetched on arrival) | home -49%, India -65%, Kenya -52%, podcast -33%, hub -21%, About -7%, Flight Mechanics -3%, enquiry -1%, episode -0.2%, library -0.3% (as the preview server sends them; as GitHub Pages sends them the library is +0.3%, 0.7 KB, all others lighter). How: each page carries only its own rules and scripts (src/v4-ux.css, src/v4-ux-*.js); the podcast's footage and the film strips' stills cut for an upright phone and fetched when near; the hub's drawings fetched when near; About's opening still, the tiles' artwork at the size shown; the episode globe written as relative steps (the same drawing, 3.5 KB lighter); the library's duplicated search words gone and its search extras fetched on first use | 6fb85495 |
