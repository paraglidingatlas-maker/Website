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
  - Left out entirely: every death mentioned (a fatal accident at Mount Borah, a fatal crash at the 2019 Panchgani pre-World Cup, fatal accidents mentioned in Colombia and Bir), and everything about John Silvester's own flying decisions, including the Barabangal story; only Eddie Colfox's lesson from it is kept, and not on the page. Also left out: Vistasp Kharas deliberately climbing through a cloud, Godfrey's account of deliberately flying in a dust devil, Nikolay Yotov's arrests, the Isiolo incident and his marriage story, and remarks about crime in named countries.
  - Jigish Gohil's statistics (deaths per season in Bir) are not on the page; his pilot numbers are ("about 800 solo pilots in autumn 2023, about 200 when he arrived").
  - Godfrey Wenness is called a former world record holder and an Advance test pilot only by the host. The page uses what Godfrey says himself: the world record in November 1998, landing in Queensland 335 km from Manilla.
  - Speaker labels are wrong in many places in the Eddie Colfox and Nikolay Yotov transcripts (host and guest swapped). Judged by content. "Many accidents happen because of the cloud" turned out to be the host's line, so it is not attributed to Eddie; the page only credits him with "be very careful of cloud, and don't follow others into it". "Don't spoil the system" on retrieve fares is labelled as the host but reads as the end of Vistasp Kharas' answer (the labels lag by a few words there); credited to Kharas.
  - Place spellings: "Piedechinche" (the episode page and captions say "Pidecinche"; the village in Valle del Cauca is Piedechinche). "Mount Borah" (captions: Bora, Borat) and "Manilla" (captions: Manila). "Aberdares" (captions: Abardere, Bardere). "Kerio Valley" (captions: Kereo). "Rohtang" (captions: Rotang). Please confirm Piedechinche in particular, since it differs from the episode page.
  - Guest names checked against episode-meta.json: captions say "Paul Tuckerts", "Godfrey Venice/Willis", "Jagish", "Nikolai"; kept Pal Takats, Godfrey Wenness, Jigish Gohil, Nikolay Yotov as in the metadata.
  - The Cauca Valley figure puts Roldanillo and Piedechinche on one cross-section; they are about 100 km apart. Marked schematic in the figure and its source line.
  - FAQ "Is it safe to land out in Colombia" and the security lines are Pal Takats' own experience, stated as such.

## Sky Gods

- Commit a7fdffe, deploy: pages build and deployment success (build, deploy jobs success).
- H1: How Do the Best Paragliding Pilots Train and Think?
- Bands:
  1. Beginnings: Maxime Pinot's early start and the Pyrenees school; Honorin Hamard's father and his first 200-hour years; Antoine Girard from climbing's 8,000 metre peaks; Robbie Whittall from hang gliding to Ozone.
  2. Volume: ground handling and hours (figure: hours a year).
  3. Moving up: Hamard's too-early jump to a demanding wing; keeping a wing longer; stepping down a class for expeditions.
  4. Limits: flying at altitude (figure: trim speed at 2,000 to 8,000 m) and Girard's Peru cloud; Hamard stopping a record attempt (quote band); Pinot on the X-Alps and fatigue; Whittall over Zanskar.
  5. Race craft: Hamard's and Pinot's competition habits and rules; Whittall on leaving the gaggle.
- Editorial calls to check:
  - Titles: the host calls Honorin Hamard the world number one and a multiple record holder; the page only uses what the guests say themselves (both Hamard and Pinot say "when I was world champion"; Girard describes his 2016 flight as the first above 8,000 m, which the page does not repeat as a claim).
  - Antoine Girard says a normal reserve would descend at 11 to 13 m/s at 5,000 m. That looks wrong (thin air raises a 5.5 m/s descent to roughly 7), so the numbers are left out; the page only says a reserve was not an option in that storm. His airspeed figures (about 40, 50 and 60 km/h at 2,000, mid and 8,000 m) do match the true-airspeed change and are used.
  - Maxime Pinot says the 2023 X-Alps left him with something that "looks a lot like post-traumatic stress" and that he works with psychologists. The page says only that he has felt fear where he had none and works on it with a psychologist; no diagnosis wording. The falling-asleep flight could be 2021 or 2023 (he is not sure), so the page does not date it.
  - Robbie Whittall: left out his views on vaccines, the food and pharmaceutical industries, one meal a day, football, wars and technology, his parting with a named co-founder, and every mention of John Silvester. Ozone partners spelled "Mike Cavanagh" (captions: Kavanagh) and "Dave Pilkington". The Zanskar flight's launch point is unclear in the transcript, so the page says only "over Zanskar".
  - Left out: the fatal accident of a local pilot in Karimabad, Maxime Pinot's criticism of beer at goal in official races, the storm incident of another X-Alps pilot, product names and product-behaviour claims (e.g. about specific two-liner models), and Honorin Hamard's name for the pilot who broke his triangle record.
  - Speaker labels in the Honorin Hamard transcript are largely swapped (his label is mostly the host). Judged by content.

## Living The Dream

- Commit fdc1ded, deploy: pages build and deployment success (build, deploy jobs success).
- H1: How Do Pilots Build a Life Around Paragliding?
- Bands:
  1. Beginnings: Benjamin Jordan's 2003 goal boiled down to a skateboard trip, then a powered flight, then Mexico to Canada (figure: one idea, three projects); Sandrine Roy's ten-year-old idea; Damien Lacaze's eBay wing and competition "revelation"; Chris Garcia's Cuba roots and first tour.
  2. What it costs: Jordan's school-bus decade and "adjust the lock"; Roy's five years of saving; Lacaze training 10 to 12 hours a week around a family and a job; Shams working as little as possible for his family.
  3. Travelling light: Roy's human-powered route and under-3 kg kit (figure: kit weights); Lacaze's X-Alps second place and 7,960 m in Pakistan.
  4. Who you fly with: Lacaze's team of nine (figure); Garcia's local pilots in Cuba and village permission in Socotra; Shams training Ouka to fly. Quote band after this band: Jordan's "awkward lines" (drawing: a ski slope and a gap in birch trees).
  5. Highs and lows: Jordan's lows after each high and "at least one"; Roy's "avance"; Lacaze on risk, focus and landing too late in a storm; Garcia's bigger margins in remote places.
- Hero: Sandrine Roy's route as a Pacific-centred world map (seam in the Atlantic, where she sailed). Only the countries she names are used, in her order; the planned leg home is dashed. The route points inside each country (and the exact US and China points) are schematic.
- Editorial calls to check:
  - Personal detail kept to what serves the page: Sandrine Roy's family losses, Benjamin Jordan's drinking and sobriety, and Shams's depression are all stated by the guests themselves but left out; the page says only that Jordan had long low periods, and that Roy's mantra on hard days is avance.
  - Chris Garcia runs a tour company, so the page uses only what he says about his own tours. Left out: all Cuban and US politics, fuel and regime talk, the Emirati and Saudi influence on Socotra, his account of why other countries closed their airspace, another operator's opinion of helicopters, the unplanned landing after a Cuban flight restriction, and the claimed Cuban distance record by a third pilot. His company is not named on the page.
  - Shams: the dog's name is spelled Ouka, as on the episode page (captions: Hookah, Uka, Luca). Left out: the harness maker and designer names (unclear in captions), the glider model, the Dean Potter story, another pilot flying acro with a dog, and castration. The "Samoyed" comes from his mention that a friend's dog was the same breed.
  - Damien Lacaze: the other X-Alps pilot's storm incident (chapter 11) is left out; only Lacaze's general point about storms is used. Rivals who train 20 to 25 hours a week are not named. The 7,960 m flight is by GPS; he says the barometer read 7,700. Its year is not stated, so it is not dated. "Sherpa" is his word for the supporter who walks with him.
  - Benjamin Jordan says the Mexico to Canada flight "still stands" as a free-flying vol-biv world record; the page attributes that to him. He gives both 2008 and 2009 for the powered flight across Canada, so it is not dated.
  - Sandrine Roy's wing, harness and reserve models are left out (caption spellings unreliable), and so is the pilot who told her flying at Rinjani was forbidden. The Pakistan leg of her planned route comes from chapter 5.
  - The "Touch The Sky With Glory" tile has no transcript and is not quoted. The From Cuba to Socotra tile still shows no guest name (the generator's tile data leaves it blank); not changed.

## Storytellers

- Commit c36cfd8, deploy: pages build and deployment success (build, deploy jobs success).
- H1: What Can Pilots Learn From Other Pilots' Close Calls?
- A short page, as the brief asked: four bands instead of five, two figures, ten FAQ answers.
- Bands:
  1. Then and now: Eddie Colfox's first flight and the early 1990s against today (figure: then and now); Marko Milutinovic on 140-pilot gaggles, pod harness reserve pockets and score discards.
  2. Collisions: Milutinovic's two mid-airs, France 2023 and Spain 2024 (figure: both on one height scale), and steering a reserve with the wing in his lap.
  3. Decisions: Colfox's launch into a gust front and "one bad decision, then two or three more"; his 2001 Hunza flight racing the dusk. Quote band after this band (drawing: sunlit heights, shadowed valleys, a landing short of the beach).
  4. Why keep going: Milutinovic weighing smaller competitions and joy; Colfox on guiding, tandems, the Bir season and tandem rescue.
- Hero: a map from England to India with the places named in both stories. The French Alps marker is schematic; the transcript says only that the 2023 World Championship was in the Alps in France.
- Editorial calls to check:
  - Everything about John Silvester is left out (he has died), including his flights, his launch habits and chapter 9 as a whole, apart from Eddie Colfox's own view in that chapter on risk management and abandoning the goal. Also left out: Colfox's cousin's death, Milutinovic's account of a pilot who died wanting to stay in a race, other pilots' injuries and fundraising, and a named team-mate's back injury.
  - The two pilots who hit Milutinovic are not named or described; his remark that one was flying aggressively and that some pilots dip in and out of cloud is left out. His view that that year's new pod harness fairings limited visibility is kept, as his own assumption ("no forensics"), with no brand named.
  - It is unclear from the transcript whether Milutinovic threw his reserve in France. The page says only that his wing kept flying without brake pressure and that he went down to land. He says he had never thrown a reserve before that first collision.
  - His explanation of score discards (FTV) gives numbers that do not add up (25% per day, "one full and three quarters" days over ten), so the page describes it without numbers.
  - Colfox's numbers are his own memory and flagged as such: first flight 1991 or 1992, glide ratios of 6.5 to 7, the Hunza flight "in 2001, I think". His claim to have run the first genuine flying safaris is attributed as "what he believes". Brand names (sponsors, wing models, Ozone's founding) are left out.
  - Speaker labels in the Milutinovic transcript lag; his speech is mostly labelled SPK03/SPK04 and the host's under his name. Judged by content.

## Weather Patterns

- Commit 63c9eee, deploy: pages build and deployment success (build, deploy jobs success).
- H1: How Do You Read a Weather Forecast for Paragliding?
- A short page for a single episode: four bands, two figures, ten FAQ answers. It is a technique page, so the drawings are technical rather than a map: the hero is a schematic sounding.
- Bands:
  1. Models: why apps disagree, resolution (figure: 22, 9 and 4 km circles), the 72-hour limit, update times, the multimodel average, paid services.
  2. Wind: wind at flying height, the millibar rule (figure), wind barbs, windgrams, shear.
  3. The sounding: inversions, the kink where climbs stop, dew point spread and cloud base, dry layers. Quote band after this band: the Keepit blue hole (drawing: a schematic plan of Lake Keepit, Manilla and the Mount Borah launch).
  4. Local knowledge: the Keepit blue hole and Sopot in a northerly; live radar, convergence lines, and keep learning.
- Callout: what rain radar colours mean for pilots (12 and about 48 mm an hour).
- Editorial calls to check:
  - Model details are given as his figures and flagged as such: GFS about 22 km, ECMWF about 9, NEMS down to 4. He was unsure about several agency details (which agency runs ICON, whether GFS support has stopped), so those are left out, as is his aside that Windy acquired part of Meteoblue (a company claim he was unsure of). SkySight's founder is not named; the page says only that it was built for gliding.
  - Left out as wrong or unverifiable: the claim that the Perlan sailplane reached "almost 40 km" (the real record is about 23 km), and the cost of running a model ("$40,000").
  - The millibar rule (900, 800 and 700 mb at about 1,000, 2,000 and 3,000 m) checks out against the standard atmosphere (about 990, 1,950 and 3,010 m), so it is used as given.
  - On a sounding he says a vertical temperature line means "no temperature difference between the thermal and the surrounding air". That is a simplification; the page paraphrases it as a thermal gaining nothing on the air around it.
  - Spellings: Ivelin Kalushkov (from the episode metadata; the host calls him Ivo), Sky Nomad (as on the episode page; captions: Kainomat, Scanomat), Manilla, Mount Borah, Lake Keepit (captions: Kipit), Sopot.

## Landing pages: how they are built (code changes)

- `generate_kb_pages.py`: `category_page()` now checks `LANDING` (from the new `kb_landing.py`). A slug with an entry goes to the new `landing_page()`; a slug without one renders exactly as before. `landing_page()` builds the series cards (the existing card markup, now with the series page's H1 under each name) and wraps `kb_layout.landing()` in the usual head, nav and footer. `LANDING_CSS` is the card part of the existing `CATEGORY_CSS` plus three small rules. Nothing in `templates/kb/` was changed or forked.
- `kb_layout.py`: new `landing()` renders the hero, the series section and a five-question FAQ, reusing `pic()` and `src()` (so every chapter link is validated at build time, as on the series pages). FAQ answers can cite several chapters.
- `kb_landing.py`: one entry per category, with the rules in its docstring.
- `tools/kbfig/landing_hero.py`: one abstract hero per category (contours and a thermal track; task cylinders; isobars and a cold front; a wing and its lines; an aerofoil with streamlines).
- Byte-identical guard: before the change, every `knowledge-base/*.html` and `episodes/*.html` was built and saved; after each landing page, each file was diffed ignoring `dateModified`. Only the landing page being shipped differed. One catch: a hero image also becomes the page's og:image, so the other four heroes were held back until their own page shipped.
- `docs/kb-rollout.md` now has a "Landing pages" section and a status table for them.

## Core Series (landing)

- Commit 81e717f (with the code above), deploy: pages build and deployment success (build, deploy jobs success).
- H1: How Do Experienced Pilots Travel, Train and Live for Flying?
- FAQ: hiring a local guide abroad (Eddie Colfox, Chris Garcia); oxygen at altitude, where the guests differ (Antoine Girard, Damien Lacaze); hours a year (Maxime Pinot, Honorin Hamard); making a living (Hamard, Benjamin Jordan, Shams, Chris Garcia); deciding not to fly (Pinot, Hamard, Lacaze).
- Editorial calls: the old intro sentence is kept as the sub line. The oxygen answer presents both views rather than choosing. Every fact is one already on the Navigators, Sky Gods or Living The Dream page, with the same chapters.

## Competitions & Performance (landing)

- Commit 56c9460, deploy: pages build and deployment success (build, deploy jobs success).
- H1: How Do You Race, Judge Risk and Keep a Clear Head in Paragliding?
- FAQ: racing in your first competitions (Joerg Ewald, Manfred Ruhmer); SIV or active flying (Subir Sidhu, Beni Kälin); knowing when you are pushing too hard (Grant Smith, Beni Kälin); how a review should test a wing (Ziad Bassil); learning from a flight that went wrong (Subir Sidhu, Will Gadd).
- Editorial calls: Beni Kälin is spelled with the umlaut here and on New Technologies, but "Beni Kalin" on the Risk vs Reward page (not changed; one of them should be made consistent). Answers keep to the wording already published on World Cups, Risk vs Reward and Resources, Tools & Tips.

## Meteorology & Weather Analysis (landing)

- Commit 746cee1, deploy: pages build and deployment success (build, deploy jobs success).
- H1: What Do Paragliding Pilots Need to Know About Weather?
- FAQ: can a cloud suck you in (Will Gadd, Eddie Colfox); spotting overdevelopment (Eddie Colfox, Ivelin Kalushkov); gust fronts (Eddie Colfox, Ivelin Kalushkov); when the wind is strongest (Ivelin Kalushkov, Pal Takats); why locals read the weather better than a forecast (Ivelin Kalushkov).
- Editorial calls: this category has one series, so four of the five answers draw on weather advice published in other series (Risk vs Reward, Navigators, Storytellers). The single series card stretches across the grid on desktop, as it did on the old page.

## Industry & Community (landing)

- Commit 5fdadd4, deploy: pages build and deployment success (build, deploy jobs success).
- H1: What Happens Behind the Scenes of Paragliding?
- FAQ: choosing a competition (Pal Takats, Marko Milutinovic, Stan Radzikowski); how high reserves are thrown (Eric Roussel, Marko Milutinovic); starting a brand (Eric Roussel, Gin Seok Song); why share accident stories (Julien Garcia, Bill Hughes, Eddie Colfox); what makes a competition safer (Goran Dimiskovski, Stan Radzikowski, Bill Belcourt).
- Editorial calls: brand facts are only what the guests say about their own companies (Neo's reserve system, Gin's fabric), as on Brand Stories. The Dark Side FAQ on reducing fatalities already covers Bill Belcourt's "training comes first", so this page uses his other point instead (pilots who own their decisions).
