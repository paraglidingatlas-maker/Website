# Knowledge base overnight run: notes

<!-- SUMMARY: written at the end of the run -->

## Start of run

- Lock taken on main. Fresh environment needed extra Python packages before
  `./build.sh` would run: fonttools, matplotlib, numpy, scipy, pillow. Playwright
  pinned to 1.56.0 to match the preinstalled Chromium (build 1194); the newer
  Playwright wanted a browser that is not installed. No repo files changed for this.
- Health check on untouched main: `./check.sh` said "All three gates clean".
- **Smoke gate caveat (pre-existing, not knowledge base):** `tools/smoke.py` crashes
  part way through, in `kenya()`: clicking `.kkit-item` on destinations/kenya.html
  times out because the collapsed packing-kit group header intercepts the click.
  `check.sh` only greps for `FAIL` lines, so a crash still reports "All three gates
  clean" and the checks after `kenya()` never run. I did not touch the Kenya page or
  the smoke test. Instead, for every page this run I ran the checks after the crash
  point separately (kenya_hero through overflow, globe, touch, pinch, errors): 133
  checks, 0 FAIL each time. Worth fixing the smoke test or check.sh.
- **Live site check not possible from this environment:** the session's egress proxy
  blocks paraglidingatlas.com and paraglidingatlas-maker.github.io (403), and
  WebFetch is blocked too. For each commit I confirmed instead that the "pages build
  and deployment" run concluded success with its build and deploy jobs both
  succeeding, and that the committed page on main carries the new H1 (via the GitHub
  API). Please open the pages in a browser in the morning.

## Brand Stories

- Commit 8797eac, deploy: pages build and deployment success (build, deploy jobs success).
- H1: How Are Paragliders and Harnesses Designed and Made?
- Bands:
  1. Beginnings: Gin Seok Song's Boomerang and Gin Gliders; Eric Roussel's String harness and Neo.
  2. Making it: Neo's cost arithmetic of sewing in France; Gin paying a Korean mill to develop fabric.
  3. Research: university and government funded R&D, the wave leading edge (figure: tubercles on the central 60%); Neo's 80 simulated harness shapes.
  4. Safety by design: why a wing must be able to collapse (quote band); Koroyd crush versus rebound; the mirror effect and Neo's stand-up reserve system (figure).
  5. The racing world: Pal Takats on culture, event grading, top speed and the submarine harness framework; Goran Dimiskovski on the PWCA and pilot quality.
- Editorial calls to check:
  - The PWCA episode (Goran Dimiskovski) is filed under "World Cups" in episode-meta.json but is one of the four tiles on this page. Kept the four tiles as they were. The library card links to `#s=Brand%20Stories`, which shows three episodes, so the card says "The Brand Stories episodes" with no count.
  - Pal Takats' episode is about competition safety culture, not a brand. Used only his general views. Left out: his account of a China World Cup and what its organisers knew, the X-Alps censorship discussion (named people and a media company), every named death, the petition and federation details, and what a named designer told him second hand.
  - Goran Dimiskovski: left out the early Owens Valley fatality, the 2013 Superfinal disqualification story and the 2019 Worlds wing ban (claims about named companies' products), his view of X-Alps as a marketing product, his criticism of a named pilot in Colombia, and his claims about national aero clubs and other licence schemes. Dropped "flew his first World Cup in 1999": he says he was accepted and then refused because it was overbooked, so it is unclear whether he flew.
  - Gin Seok Song: left out his remarks on a rival's wing in a China incident, on another fabric maker, on a tandem brand that closed, on a rival designer's EN B wing, on market leadership, and "no one has aspect ratio 6 on a B". Claims about his own products are attributed ("he says").
  - Eric Roussel: left out his comparison with another brand's protector (including G figures), his comment that Gin is "not the best in business", his ranking of other brands, and "the only workshop in France able to do that". Added one line saying other guests on the site are more sceptical of crumple protectors (Zsolt Ero on Know Your Equipment, the Niviuk engineers on New Technologies). The captions place Neo's workshop in "Nancy"; I left the town out because I could not confirm it.
  - Spellings: "Pal Takats" (captions say Paul Takats / Tuckertz), "Gin Seok Song" and "Gin Gliders" (captions Jin, Gene, Jingle), "Myeongjin" for the fabric maker (captions vary: Myeongjin, Myungjin; the episode page's chapter title says "Munjin"). Please confirm the fabric maker's spelling.
  - Speaker labels are wrong in places: Gin's "flying since 1977" and Pal's "started flying at 16" are labelled as the host. Judged by content.
  - Carabiner test: captions are garbled ("85,000 times after 880 * 1000 cycles"), so the page says "tens of thousands of load cycles".
  - FAQ "Do I need a licence to fly in the Paragliding World Cup?" is framed "at the time of this conversation" (February 2024); rules may have changed.
