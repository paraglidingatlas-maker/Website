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

## Navigators

- Commit 6fde74e, deploy: pages build and deployment success (build, deploy jobs success).
- H1: What Should I Know Before a Paragliding Trip Abroad?
- Bands:
  1. Putting down roots: Pal Takats buying a hill with a takeoff in Colombia; Godfrey Wenness building Mount Borah; Eddie Colfox and Jigish Gohil in Bir.
  2. When to go: seasons in Colombia, Bir, Panchgani and East Africa; Australia's unreliable months and the synoptic pattern; two guests' impression that seasons run later.
  3. The local air: Roldanillo versus Piedechinche and the Pacific breeze (figure: Cauca Valley section); Panchgani's sea wind and shear layers; Bir's back ranges; Kijabe's afternoon easterlies.
  4. Launch and climb: leaving Mount Borah for the flats (quote band: schematic plateau with four launches); Bir's nil-wind launch; Kijabe's cone; Godfrey's glide in thirds (figure).
  5. Coming down: power lines, terraces, crops, fences and water; retrieves and security in each region.
- Hero: world map from Natural Earth 1:110m (public domain). The usual map CDNs are blocked here, so `tools/kbfig/nav_land.py` reads the copy bundled in the geopandas 0.14.4 wheel (fetched with pip on first use). Places marked: only those named in the episodes.
- Editorial calls to check:
  - Left out entirely: every death mentioned (a fatal accident at Mount Borah, a fatal crash at the 2019 Panchgani pre-World Cup, fatal accidents mentioned in Colombia and Bir, a Pakistani pilot who died), and everything about John Silvester's own flying decisions, including the Barabangal story; only Eddie Colfox's lesson from it is kept, and not on the page. Also left out: Vistasp Kharas deliberately climbing through a cloud, Godfrey's account of deliberately flying in a dust devil, Nikolay Yotov's arrests, the Isiolo incident and his marriage story, and remarks about crime in named countries.
  - Jigish Gohil's statistics (deaths per season in Bir) are not on the page; his pilot numbers are ("about 800 solo pilots in autumn 2023, about 200 when he arrived").
  - Godfrey Wenness is called a former world record holder and an Advance test pilot only by the host. The page uses what Godfrey says himself: the world record in November 1998, landing in Queensland 335 km from Manilla.
  - Speaker labels are wrong in many places in the Eddie Colfox and Nikolay Yotov transcripts (host and guest swapped). Judged by content. "Many accidents happen because of the cloud" turned out to be the host's line, so it is not attributed to Eddie; the page only credits him with "be very careful of cloud, and don't follow others into it". "Don't spoil the system" on retrieve fares is labelled as the host but reads as the end of Vistasp Kharas' answer (the labels lag by a few words there); credited to Kharas.
  - Place spellings: "Piedechinche" (the episode page and captions say "Pidecinche"; the village in Valle del Cauca is Piedechinche). "Mount Borah" (captions: Bora, Borat) and "Manilla" (captions: Manila). "Aberdares" (captions: Abardere, Bardere). "Kerio Valley" (captions: Kereo). "Rohtang" (captions: Rotang). Please confirm Piedechinche in particular, since it differs from the episode page.
  - Guest names checked against episode-meta.json: captions say "Paul Tuckerts", "Godfrey Venice/Willis", "Jagish", "Nikolai"; kept Pal Takats, Godfrey Wenness, Jigish Gohil, Nikolay Yotov as in the metadata.
  - The Cauca Valley figure puts Roldanillo and Piedechinche on one cross-section; they are about 100 km apart. Marked schematic in the figure and its source line.
  - FAQ "Is it safe to land out in Colombia" and the security lines are Pal Takats' own experience, stated as such.
