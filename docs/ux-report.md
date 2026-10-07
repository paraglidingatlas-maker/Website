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
| 4 | Hold a place in context | generic heading; first field at y=840; message required; header Enquire Now shown | the departure's trip, dates, length and price under the title; first field at y=774 on a phone; message optional; header Enquire Now hidden on the enquiry page; mailto and the worker hook unchanged | see git log |
