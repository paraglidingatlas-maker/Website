# SEO and GEO overnight notes

Summary goes here at the end of the job (F1).

## Checklist

- [ ] 7.1 AI index file (llms.txt)
- [ ] 7.2 Episode to series links
- [ ] 7.3 Structured data
- [ ] 7.4 Titles and meta descriptions
- [ ] 7.5 Social preview tags
- [ ] 7.6 Images and speed
- [ ] 7.7 Crawl hygiene
- [ ] 7.8 Report (docs/seo-baseline.md)
- [ ] 7.9 Episode summary fixes (progress: none yet)
- [ ] 7.10 Headings and accessibility
- [ ] 7.11 Related episodes (progress: none yet)

## Run log

### Run 1 (started 2026-09-23 01:01 UTC)

Setup, before any site change:

- The pages job finished (every series and landing page marked done) and
  released its lock at 01:00 UTC. Lock "B" taken at 01:01 UTC.
- The build needs `fontTools`, which this machine did not have. Installed it
  with pip. No repo change.
- `pip install playwright` pulled 1.63, which does not match the Chromium
  preinstalled on this machine, so the smoke gate silently skipped the browser.
  Pinned playwright 1.56 locally to match. No repo change.
- **Pre-existing, not caused by this job:** `tools/smoke.py` crashes on the
  Kenya packing kit (`pg.click(".kkit-item")` times out because
  `.kkit-groups` intercepts the click; the kit was collapsed on 16 Sep). The
  crash is a Python exception, not a `FAIL` line, so `check.sh` still prints
  "All three gates clean" while every smoke check after Kenya is skipped.
  For this job I ran every smoke check through a wrapper that records a crash
  per check instead of stopping: baseline is 154 checks, 0 FAIL, the Kenya
  click as the only crash. That is the bar each change below had to meet.
  Worth fixing the test (open the collapsed group first) in the morning.
- `sitemap.xml` `lastmod` comes from file modification times, so a checkout
  whose files carry different mtimes than the last build drifts on the first
  build and settles on the second. Seen once during the health check; the
  second run was clean. Not changed (judgement call, see 7.8 report).
