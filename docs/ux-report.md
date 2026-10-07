# v4 usability pass (from 7 Oct 2026)

The owner's brief: fix measured usability problems on v4, re-measure, report.
Not a redesign: the look stays. Live site, `prototypes/v2/` and `rss-feed.js`
untouched; no switch-over.

Every number here comes from `python3 tools/ux_measure.py` (headless
Chromium: phone 390 x 844 touch, tablet 768 x 1024, desktop 1440 x 900). The
numbers before any change are in `docs/ux-measure/before.json`, after in
`docs/ux-measure/after.json`.

## Progress
A check-in reads this table to know where to resume: the first item not
marked done or blocked is the next one.

| # | Item | Before | After | Commit |
|---|---|---|---|---|
| 0 | Measurement tool and baselines | the brief's numbers reproduced | `docs/ux-measure/before.json` | 9f490edf |
| 1 | Price in the phone action bar | "10 days, Next departure 21 Oct 2026" | "£1,100 per pilot, 10 days, Next departure 21 Oct 2026" (Kenya "From US$2,100"); 320 to 414 px, 69 to 75 px tall | ccb03bb5 |
| 2 | Dates sooner | Dates at screen 19.3 (India), 20.0 (Kenya) of 26; gallery 7.6 / 7.0 screens | Dates at 10.6 / 11.5 of 20; gallery 2.8 / 2.7 screens; route 3.2 / 4.2 | see git log |
| 3 | Gallery framing | 30% of each photo shown on average (least 20%), up to 4.7x enlarged on a 3x phone | every photo whole in a landscape frame on an upright phone or tablet (100% shown, at most 1.1x) | f8f677de |
| 4 | Hold a place in context | generic heading; first field at y=840; message required; header Enquire Now shown | the departure's trip, dates, length and price under the title; first field at y=774 on a phone; message optional; header Enquire Now hidden on the enquiry page; mailto and the worker hook unchanged | a8f9bd93 |
| 5 | Nothing important folded away | India 5 of 10 questions in view, Kenya 5 of 6 (cancellation folded); Flying Etiquette one collapsed row at the end | every question in view on both; Flying Etiquette its own band after Before You Book, heading and first two paragraphs in view (510 / 494 characters), in the jump row | 602c47e4 |
| 6 | Weight on a phone | own-host bytes on arrival (3x phone): India 4.19 MB, home 2.71 MB, Kenya 1.63 MB | India 1.45 MB, home 1.37 MB, Kenya 0.79 MB; no measured page heavier. Phone cuts of the hero photos and clips (2:3, the same framing), only the first hero slide on arrival, gallery and the home fly-through photos when near | 95066dd7 |
| 7 | Desktop sub-navigation | the bar ends on a small "Enquire" | "Enquire", then the from price ("£1,100 per pilot", "From US$2,100") and Hold a place, held at the bar's right end while the links scroll (821 px and up) | 5c8064cd |
| 12 | aria-controls before the target exists | 2 dangling (v4-open -> v4Menu, v4-ls-open -> v4Listen) | 0: each button names its menu or screen once it exists | 5c8064cd |
| 8 | Transcript on phones | 264 px column, 33 characters a line | the time above each paragraph: 342 px, 43 characters a line | see git log |
| 9 | Chapters on phones | 13 cards of 220 px in a sideways row; ticks 5 to 19 px; axe target-size: 10 nodes here, 36 on three more episodes | a vertical list (44 px rows); the timeline ticks and the audio player's chapter marks left out on touch screens; axe target-size passes on all four | 438a6891 |
| 10 | Titles that say nothing | 613 labels on 93 episode pages: 36 equal a series name ("Sky Gods"), 34 repeats in a block (the guest twice on a card) | 0 and 0: guest plus the descriptive part of the title ("Antoine Girard: Flying 8000ers"; cards "Flying to Win" over "Honorin Hamard, 108 min") | 406d1edd |
| 11 | Layout jumps at 1440 | podcast CLS 0.55; episode 0.06, hero title moves 35 px | podcast 0.00, episode 0.01 (title moves 1 px) | 406d1edd |
| 13 | Ideas first | first idea at screen 3.3 (Flight Mechanics), 4.2 (Risk vs Reward); tiles 2.3 / 3.2 screens | 1.4 and 1.4 (Sky Gods 1.5); the conversations are one row to swipe (0.3 screens) | see git log |
| 14 | Series pages: a jump row | 13 series pages of 17 to 20 phone screens, no way to jump | the trips' jump row on all 13: each idea by its kicker, Worth Remembering, FAQ, the conversations; it stays at the top | see git log |
