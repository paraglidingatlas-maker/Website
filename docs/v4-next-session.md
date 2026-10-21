# v4: handoff to the next session (21 Oct 2026)

Start here, then read `docs/v4-plan.md` (the brief and the owner's rules) and
the progress table in `docs/v4-report.md` (rows 0 to 43). Everything below is
the owner's current queue and what the last session learnt doing it.

## The owner's rules (unchanged)
- Only `prototypes/v4/`, `tools/` and `docs/` change. Never `prototypes/v2/`,
  never a live page, never `rss-feed.js`. The switch-over is the owner's.
- Nothing invented: a missing fact shows as `[to supply]` (`.v2-tbd`).
- Design tokens only; no em dashes in copy; cache-bust changed CSS and JS.
- Motion only in answer to the visitor; nothing loops or runs on its own (the
  owner's footage while on screen is the one exception; they were asked on
  20 Oct to confirm it still stands). Reduced motion and no JavaScript show the
  finished page.
- Push only `git push origin HEAD:main` and `git push origin HEAD:claude/v2-prototype`,
  after `python3 tools/v4_gates.py` passes (about 25 minutes; `--quick` while
  iterating). Never forced, no pull requests.
- Never store a token or key in the repository or the chat; GitHub access comes
  from the connected account.
- Episode counts are the RSS feed's (owner, 21 Oct: "whatever the RSS feed
  shows, it's the correct count"; never ask again): the episodes in
  episode-meta.json with a publish date (80 on 21 Oct); tools/v4_polish.py
  feed_count() writes it on the sitemap and Mission.
- No photograph is used twice on the site unless it really must be (faces,
  portraits); a repeat is replaced with a different picture, not dropped
  (owner, 21 Oct).
- Work lean (owner, 21 Oct: "we're spending a lot of time discussing"): at
  most two options for a decision, one preview only for a large visual
  change, small fixes built straight away and shown after.

## Where the queue stands (21 Oct)
Items 1 to 3 below are done and pushed: the sitemap's real sky (row 35, with
the motion the owner asked for), Partners (row 34) and the site-wide pass on
home, podcast, library, knowledge base, topics, About and Mission (rows 36 to
43). The owner chose every look from side-by-side previews; the episode
reader fix the switch-over needed is done too (the report's switch-over
section). What is open:
- **The record page photo**: built on 21 Oct (report row 44) as the owner
  chose from mock-ups, `docs/record-photo/README.md` and `tools/v4_record.py`
  01 the mark. A full-size export of DSC06347 would let it fly larger.
- **The review of every page type** (21 Oct): screenshots of 17 page types
  on desktop and phone sent to the owner, with what the review found (below,
  under "Found in the 21 Oct review").
- Done on 21 Oct from the review (row 45): the four small fixes and the
  corrections v4 can make. Left for the owner: the same
  corrections in the live site's own sources (generate_tag_pages.py lines
  331 and 363, episode-meta.json, destinations/kenya.html).
- Photographs used twice on v4 (owner's rule), each waiting for a new
  photograph from the owner: About's Kenya, Peru and Kazakhstan cards (the
  home page's), Expeditions' India and Kenya photographs (the trip pages'),
  and the record page's Kerio Valley, Kenya hero and Coupe Icare photographs
  (the Kenya page's and Partners'). Episode cover art repeats by design.
- The home page (roadmap step 6): built on 21 Oct, both directions the
  owner chose ("both A&B", report row 46): figures under the opening that
  count up, every departure on one line of months, the held photographs that
  come closer, the episode cards that lean gently towards the mouse (a
  stronger lean was tried and turned back by the owner; the trip list's
  orange fill was taken out, "remove this"). All in `tools/v4_polish.py` (HOME_CSS, HOME_JS, `home_markup`,
  read from the site at each build).
- **The encyclopedia** (21 Oct, report row 47): the A to Z and the ten
  Flight Mechanics answers are v4 pages under the knowledge base
  (`tools/v4_encyclopedia.py`, rebuilt from the review copy in
  `prototypes/workspace/drafts/` on every build), reached from the knowledge
  base page, Flight Mechanics and the FAQ answers the A to Z links to.
  Prototype-only until the owner has reviewed the ten drafts. A change to an
  answer is made on the encyclopedia-pilot branch (`kb_answers.py`) and the
  review copy built again (`ENC_SHOW_DRAFTS=1`). That branch's A to Z filter
  changes only the count (fixed in v4 only).
- **The Atlas** (21 Oct, report row 48): the knowledge base's button opens
  the globe (`knowledge-base/encyclopedia/atlas.html`, `tools/v4_atlas.py`),
  and its pins and questions lead into the encyclopedia. Built from the
  site's own data (globe-episodes.js, the FAQ answers, the ten answers),
  not from the workspace's Flying Atlas, whose 450 entries were never
  checked. On the home page too, later, if the owner wants it there.
- From the 20 Oct roadmap, still open: icons to photographs (step 7,
  waiting for the owner's photographs; on About the owner chose to keep the
  icons).
- The switch-over stays the owner's.

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
3. **The site-wide pass, only on**: home, podcast, library, knowledge base,
   topics, about pages. Episode pages are off the list for now (owner, 20 Oct).
   One page type at a time, screenshots to the owner after each, the way India
   was done (report: "India, less but better"). Topic pages are a template
   over about 50 pages: build the change in a tool, check a sample of pages,
   and prove the rebuild.

Then, before any switch-over: `tools/v2_episode.py` must read the live episode
header of 2 Oct. Done on 20 Oct (commit 19f4707f): a new episode builds again. Kenya's pass is paused by the owner; the
cheap option offered was removing only what breaks the motion rule (its hero
slideshow timer and the slow zooms).

## Found in the 21 Oct review
17 page types on desktop (1440) and phone (390), captured by scrolling a real
window one screen at a time and joining the screens (one tall full-page shot
breaks the pinned and scroll-driven parts), read by two agents and every
finding checked again by hand; sent to the owner as a page
(https://claude.ai/artifact/5oA3E1CrreKHtYgbopMXW3). No script errors.
- Fixed (a regression of row 36): the library's opening chart drifted over
  "Start here / All Series" on a phone; its drift now stops at the room left
  in the opening (`tools/v4_polish.py` LIB_JS).
- For the owner (content, also on the live site): topic pages promise a full
  transcript for every episode (`generate_tag_pages.py`, lines 331 and 363)
  while Safety has 29 of 30; the "New Technologies 3: Stephan Stiegler"
  description lacks a name ("the innovative designer from .",
  `episode-meta.json`; probably AirDesign); 80 episodes on some pages, 93 on
  others (both true: 80 in the feed, 93 with the 13 YouTube-only videos);
  Kenya's "Took It's First Steps".
- Proposed v4 fixes, waiting for a yes: the podcast feed's failure message
  ("the saved archive is below instead", from `rss-feed.js`, with nothing
  below; v4 can replace it with a link to the library); a soft shadow behind
  the home opening's small orange line over bright snow; "carabiner" under
  the harness outline in the Brand Stories drawing; the topic pages' chart
  labels about 5 px on a phone.
- Not problems: Kenya's gallery and Expeditions' panels need a continuous
  scroll to load and show (a capture that jumps a screen at a time misses
  them); nine topics have no trend line because none of their episodes is
  dated; YouTube pictures are blank only where YouTube cannot be reached.

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
