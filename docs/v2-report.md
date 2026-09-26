# v2: overnight report (26 to 27 Sep 2026)

The plan was `docs/v2-plan.md`. Everything in it is done, except the one step
kept for the owner on purpose: the live switch-over is prepared and
rehearsed, not performed.

## In one paragraph
Every page of the site now exists in v2: **182 pages** (was 20), covering
every URL in `sitemap.xml`. All 93 episodes use the layout the owner chose
(player beside the title). A new checker tests every page for broken links,
errors, sideways scroll, headings, labels, tap sizes and **search / answer-
engine parity with the live page it replaces**: 0 FAIL. The switch-over has a
tool, a rehearsal on a full staging copy (0 FAIL, including the live site's
own audit) and a one-page runbook below.

## What was done
| Step | Result |
|---|---|
| Checker | `tools/v2_check.py`: static checks on every page, Chromium at 390 (as a touch phone), 768 and 1440. Found and fixed: episode headings dropping the guest's name (it is in the live heading, so search reads it there), "Snippet" dropped from one heading, a canonical on the v2 404 that live does not have. |
| Episodes (93) | Built with `tools/v2_episode.py --all`. Host-only episodes (AMA, notes) say "Hosted by" with a host card; race highlights and films with no guest have no guest card; no stray dot where there is no episode number. |
| Knowledge base (18), topics (50), text pages (8) | `tools/v2_twin.py`: the live page in the kit's frame, reproducing the three hand-made samples byte for byte. Redirect stubs stay live as they are. |
| Responsive (390 / 768 / 1440) | Touch sizes 44px on the v2 pieces (chips, sources, trip tabs, timeline, logo, Enquire, contents lists). Home: "Why fly with us" panels no longer squeeze on a phone; hero label readable over snow; departures two to a row on a tablet. Podcast: "What You Can Expect" two to a row on a tablet. Reduced motion and JavaScript-off: nothing hidden, no errors. |
| Speed | Home loads **2.5 MB** on arrival instead of 4.1 MB: the India flight video starts only when the fly-through is on screen (pauses after India); leaner copies of the four trip photos for v2 only. |
| Accessibility | Focus rings on the new pieces; no heading level skipped that live does not skip (the 404 was fixed); the podcast question form's fields have explicit labels. |
| Design rules | `docs/v2-design-rules.md`, and the style guide gains the words-on-a-photo specimen. |
| Switch-over | `tools/v2_switch.py`, rehearsed end to end (below). The rehearsal found and fixed: the library's portal element twice, the 404 needing root-absolute links, the audit misreading `#s=` / `#pin=` as anchors. |

## Checks (last run)
- `./build.sh`: ok. `tools/audit.py --drift`: 0 FAIL, 5 warn (all on the
  live site, unchanged: unreferenced assets, a 402 KB image, CSS classes,
  radii, and the episode data below).
- `tools/smoke.py`: 172 checks, 0 FAIL.
- `tools/v2_check.py`: 182 pages, 0 FAIL, 80 warn. The warnings are 79 tap
  targets that are 44px tall but narrower than 40px by design (episode
  timeline ticks sized by chapter length, the trip photo dots, the knowledge
  base's title links, two sitemap buttons), and the homepage having fewer
  words than live, which was the owner's decision.
- `tools/v2_switch.py --dry-run --build`: 180 pages, 0 FAIL.

## SEO / GEO (search and answer engines)
- Every v2 page keeps the live page's title, description, canonical, Open
  Graph, Twitter card, structured data types, episode name / date / duration,
  every meaningful word of its `<h1>`, at least 95% of its body text and all
  transcript chapters. Checked on every page, every run.
- Transcripts stay in the HTML, readable without JavaScript, as `robots.txt`
  promises. `robots.txt`, `sitemap.xml`, `llms.txt` and the redirect stubs are
  untouched by the switch.
- v2 stays `noindex` with a canonical to live until the switch, so it cannot
  compete with the live pages in search.
- **Needs the owner (data, not design):** 14 episodes have no publish date in
  their data, 2 of them no description either, so their search data is
  incomplete on the live site today: art-of-flight-in-norwegian-skies,
  birds-eye-view-of-oslo (both parts), can-we-steer-a-round-reserve-parachute
  (date and description), highlights-day-1-pwca-superfinal-2026,
  just-another-day-in-paradise-oslo, the three SRS Piedrahita videos, the four
  World Cup Super Final task highlights, touch-the-sky-with-glory
  (description). Dates can come from YouTube; send them and they go in.

## The switch-over runbook (for when the owner says go)
Switching the repo in place does not hold: the next `build.sh` rewrites the
generated pages in the old design and stops at the library's markers. So the
repo keeps its pages as the generators' sources, and the deploy publishes a
built folder with the v2 pages laid over it.

1. Copy `docs/v2-deploy-workflow.yml` to `.github/workflows/deploy.yml`.
2. GitHub: Settings > Pages > Source: **GitHub Actions** (owner only).
3. Push. The workflow runs `build.sh`, rebuilds the v2 pages from that fresh
   output, runs the gates, runs `tools/v2_switch.py --apply --out _site` and
   publishes `_site`.
4. Check: home, an episode, a topic, the 404 (any missing address), on a
   real iPhone and a desktop.
5. Search Console: submit `sitemap.xml` again; watch Coverage and Core Web
   Vitals for two weeks. Nothing changes address, so no redirects are needed.

**Roll back:** set the Pages source back to "Deploy from a branch" (main, /)
and delete `deploy.yml`. The repo is exactly the live site, so this restores
it at once.

Differences the switch makes beyond the pages: the published site stops
serving the repo's working files (`tools/`, `docs/`, `prototypes/`,
`templates/`, the `.py` scripts). None of them is in the sitemap.

## Could not be done here
- **A real iPhone and Safari.** Everything was checked in Chromium,
  including touch emulation. The fly-through's held picture and the blurred
  glass are the parts most worth a look on a phone.
- **YouTube stills and players, the live podcast feed:** blocked in this
  environment, so screenshots show grey boxes there; the live pages load them.

## Left for the owner
- Say go for the switch-over (runbook above).
- The 14 episode dates / 2 descriptions.
- Peru and Kazakhstan: length, group size, price (still `[to supply]`).
- The episode count: pages still say 71, 86, 93 and 90+. The library counts
  86 listed episodes and there are 93 episode pages.
- Content pass (text trim) was out of scope, by the owner's word.
