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
| 0 | Measurement tool and baselines | | | |
