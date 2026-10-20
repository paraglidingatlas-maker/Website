# v4: handoff to the next session (20 Oct 2026)

Start here, then read `docs/v4-plan.md` (the brief and the owner's rules) and
the progress table in `docs/v4-report.md` (rows 0 to 34). Everything below is
the owner's current queue and what the last session learnt doing it.

## The owner's rules (unchanged)
- Only `prototypes/v4/`, `tools/` and `docs/` change. Never `prototypes/v2/`,
  never a live page, never `rss-feed.js`. The switch-over is the owner's.
- Nothing invented: a missing fact shows as `[to supply]` (`.v2-tbd`).
- Design tokens only; no em dashes in copy; cache-bust changed CSS and JS.
- Motion only in answer to the visitor; nothing loops or runs on its own (the
  owner's footage while on screen is the one exception; he was asked on
  20 Oct to confirm it still stands). Reduced motion and no JavaScript show the
  finished page.
- Push only `git push origin HEAD:main` and `git push origin HEAD:claude/v2-prototype`,
  after `python3 tools/v4_gates.py` passes (about 25 minutes; `--quick` while
  iterating). Never forced, no pull requests.
- Never store a token or key in the repository or the chat; GitHub access comes
  from the connected account.

## The queue, in the owner's order (20 Oct)
1. **The sitemap's night sky from real stars.** The v4 sitemap
   (`prototypes/v4/sitemap.html`, built by `tools/v4_catchup.py`
   `sitemap_sky()`) loads the LIVE `sitemap-sky.js`, which must never be
   edited. Its background field is seeded random (`rnd()`, seed 20261002, about
   line 47) drawn on the `.sky-stars` canvas; the episode stars and the series
   constellations are data and stay. Real positions and magnitudes are already
   in the repo: `tools/v4_record.py` `STARS` (d3-celestial 0.7.35,
   `data/stars.6.json`, BSD-3-Clause, XHIP; the credit and notice are its
   `STAR_NOTE`, which must go with the data). Way in: a v4-only background
   layer under the sky (or a v4 copy of the script, `prototypes/v4/`), loaded
   only by the v4 sitemap, credited, still (no twinkle), drawn once; then add
   its tool step to `tools/v4_build.py` after `v4_ux` if it patches the page.
2. **Partners** (`prototypes/v4/partners.html`): the formats laid out like the
   record page's offer, the audience numbers big and still with an "About
   these numbers" fold (80 from the feed; 130+ countries confirmed by the
   owner on 20 Oct; 100,000+ streams and 10+ years have no stated source, so
   `[to supply]`), and a link to the record attempt inside
   `<!-- v4:needs record-attempt.html -->` marks that `tools/v2_switch.py` drops
   while the record page is prototype-only. Run in the previous session as a
   workflow; if row 34 of the report is not there and nothing is pushed for it,
   start it again from this brief. `partners.html` is the shell (head, menu,
   footer) that the record, Expeditions and feed-option generators copy:
   leave those parts alone and prove their pages unchanged.
3. **The site-wide pass, only on**: home, podcast, library, episode pages,
   knowledge base, topics, about pages. One page type at a time, screenshots
   to the owner after each, the way India was done (report: "India, less but
   better"). Episode and topic pages are templates over about 140 pages: build
   the change in a tool, check a sample of pages, and prove the rebuild.

Then, before any switch-over: `tools/v2_episode.py` must read the live episode
header of 2 Oct (a new episode stops `tools/v4_build.py` until then; see the
report's switch-over section). Kenya's pass is paused by the owner; the
cheap option offered was removing only what breaks the motion rule (its hero
slideshow timer and the slow zooms).

## Keeping the cost down (the owner asked, 20 Oct)
India took about 25 agents and three workflows for a 7.5-to-6 win. Most of
that was checking, not building. Next time:
- **Screenshot once, judge many.** Each blind judge re-walked both pages at two
  widths (about 150 tool calls and 180k tokens per judge). Instead, one cheap
  agent takes the screenshot set and the frame sequences once, for old and new,
  into labelled folders; the judges only look at them.
- **One judge for a small page, two only for a big one**, and never more than
  one fix round; a small fix after judging is made directly, without judging
  again.
- **Let the gates check what they already check.** Parity, links, words,
  overflow, tap targets and weight are in `v4_gates.py` and `v4_weight.py`; the
  checker agent only does what they cannot: the facts diff, the booking links,
  the motion rule.
- **One audit agent, not two**, and no per-frame probes, CPU throttling runs or
  thousands of frames unless something is actually janky.
- **Smaller models for mechanical work**: screenshots, diffs and measurements
  on a smaller model (the Workflow tool's `model` option); the planner, the
  builder and the judges on the main one.
- **Full gates once before a push**, `--quick` while iterating.
- **Content before polish**: the judges' main limits on India were the visible
  "From past pilots [to supply]", soft or repetitive photographs and a route
  that is only a diagram. The owner's quotes, best photographs, IGC logs and a
  sharp hero clip would lift the trip pages more than another round.

## How to work here
- Preview server: `python3 -m http.server 8765 --bind 127.0.0.1` from the repo
  root. For old-versus-new comparisons, a git worktree of the last pushed
  commit in `/tmp/claude-0/wt-old`, served on port 8766.
- `tools/v4_build.py` must keep reproducing the committed v4 byte for byte:
  in a clean worktree of the new commit, `./build.sh && python3 tools/v4_build.py`
  twice, then `git status --short prototypes/v4` is empty. Every new in-place
  pass (like `tools/v4_trip_calm.py`) goes in it after `v4_ux`. This check found
  a real bug on 20 Oct (the enquiry page's trip length).
- A page-only look goes in its own sheet and script loaded by that page alone
  (as `v4-calm.css` and `v4-calm.js` for India), so no other page's bytes or
  version hashes change.
- A new page with no live twin goes in `tools/v2_site.py` `NEW_PAGES`.

## Waiting on the owner
Photographs (a Google Drive folder works; Terabox is blocked), client quotes
for "From past pilots", the record page's FAI figures, wing and team, the
sponsor tiers and promises, the source and date of the 100,000+ streams, the
India and Kenya skill levels, whether the hero footage may loop, the iPhone
check and the switch-over.
