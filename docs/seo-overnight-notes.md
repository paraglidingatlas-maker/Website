# SEO and GEO overnight notes

Summary goes here at the end of the job (F1).

## Checklist

- [x] 7.1 AI index file (llms.txt): done, 4baf0d9, deploy success
- [x] 7.2 Episode to series links: done, f56e9b4, deploy success
- [x] 7.3 Structured data: done, 9ccfadb, deploy success
- [x] 7.4 Titles and meta descriptions: done, 4c85528, deploy success
- [x] 7.5 Social preview tags: done, 914062a, deploy success
- [x] 7.6 Images and speed: done, see log
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

**Live checks (C7) could not be run from this machine.** The network policy
here blocks paraglidingatlas.com and paraglidingatlas-maker.github.io (curl and
WebFetch both refused), and the Pages artifact download is blocked too. For
every commit I instead confirmed the "pages build and deployment" run for that
exact commit concluded success, on top of the full local gate. Please open the
home page, one episode page and one knowledge base page in the morning.

### 7.1 AI index file: done (4baf0d9, deploy run 431 success)

llms.txt had no knowledge base entries at all: no series page and no landing
page was listed. `generate_llms_txt.py` now writes a "Knowledge base" section:
the five landing pages, each followed by its series pages, every entry with the
page's own H1 as link text and its lead as the description. The text is read
from `kb_landing.LANDING` and `kb_editorial.EDITORIAL` (read only), the same
data the pages render from, so it cannot drift; which series sits under which
landing page is read from the built landing page's links. Verified all 18
entries match the built pages' H1 and lead exactly. Only llms.txt changed.

### 7.2 Episode to series links: done (f56e9b4, deploy run 432 success)

No episode page linked to its knowledge base series page. Each of the 93
episode pages now has a "Knowledge base" box in the sidebar, directly under
Related episodes, built from the existing `cd-box` and `cd-link` classes, with
the series page's H1 as the link text (read from `kb_editorial.EDITORIAL`).
The episode's `series` field maps to the series slug; all 13 series resolve.

**Deviation from the brief, on purpose:** the brief said to add it in
`generate_episode_pages.py`, but that file is dead code (PROJECT_HANDOFF.md
says so, and `build.sh` never runs it). The live episode pages come from
`generate_chapter_deck.py` and `templates/episode-template.html`, so the change
is there. The only page without the box is
`episodes/new-technologies-5-frantisek-pavlousek-2.html`, which is a noindex
redirect stub, not an episode.

### 7.3 Structured data: done (9ccfadb, deploy run 433 success)

What was already right: every indexable page has Organization and WebSite
(from `tools/inject_site_schema.py`); every episode has PodcastEpisode with
name, description, datePublished, partOfSeries and url, and the guest as a
Person (`actor`). 404.html has no schema, which is correct for a noindex page.

Changed, JSON-LD only (checked: no page differs outside its JSON-LD blocks):

- Episodes: `duration` added (PT96M style, from the feed's `duration_label`,
  80 episodes). A nested `video` VideoObject on the 85 episodes whose id is in
  `youtube_video_ids.json` (name, description, thumbnailUrl, embedUrl, url).
  **No `uploadDate` on the VideoObject**: the only dates stored are the podcast
  feed's, and the YouTube upload date may differ. Google's video rich results
  want uploadDate, so Search Console may flag these as missing it; add the
  real upload dates to the data if you want those results.
- Episodes: description is now the full summary; it was cut at 280 characters,
  mid-word. Empty `datePublished` (13 reels) and empty `description` (2) are
  now omitted instead of written as "".
- Duplicates: 84 pages declared their own page node (tag and KB
  CollectionPages, policy and About WebPages, the enquire ContactPage) with no
  `@id`, and the injector then added a second WebPage for the same address;
  the homepage had two WebSite nodes. The injector now gives the page's own
  node the shared `#webpage` (or `#website`) id and the site facts, and skips
  its extra WebPage there. After: no page has two entities of the same type,
  and no shared `@id` has two types. Hand-maintained pages (index, about,
  podcast, library, enquire, knowledge-base.html) had their own JSON-LD block
  rewritten once by the injector; later builds leave them alone (verified: a
  second build changes nothing).

Left for you: episodes with two guests carry one Person named "A & B"
(7 entries, e.g. "Tilen Ceglar & Stan Radzikowski"). Two of those are not
two people ("Finsterwalder & Charly", "Shams & Ouka"), so I did not split them
automatically. Also: the summary-based meta description (7.4) is still cut at
155 characters mid-word on most episodes; I left that alone because it was
outside the brief, but cutting at a word boundary would read better.

### 7.4 Titles and meta descriptions: done (4c85528, deploy run 434 success)

Audit of all 177 indexable pages: no missing title or description, no title
over 70 characters. Problems found, all on episode pages:

- Duplicate title: `episodes/touch-the-sky-with-glory.html` had the same title
  as `mission.html`. Now "Touch The Sky With Glory: Channel Trailer".
- Duplicate title: Oslo part 2 lost ": Part 2" when shortened, so it matched
  part 1. Now "Bird's-Eye View of Oslo: Part 2".
- Empty description: touch-the-sky-with-glory and
  can-we-steer-a-round-reserve-parachute-urs-haari-answers (both have no
  summary). Descriptions written only from each entry's own title, guest,
  series and notes.
- Description under 70: art-of-flight-in-norwegian-skies (65). Added
  ", a cinematic clip", from its own `_not_an_episode` note.

How: two new optional fields in `episode-meta.json`, `seo_title` and
`seo_desc`, each with a `_source` note, used by `generate_chapter_deck.py` for
`<title>`, meta description and og:description only. H1, og:title and the
visible summary are unchanged. Knowledge base pages were not touched.

### 7.5 Social preview tags: done (914062a, deploy run 435 success)

Every indexable page (177) already had og:title, og:description and og:image.
The 93 episode pages had no og:url and no twitter:card; every other page had
both. Added to `templates/episode-template.html`: og:url (the same address as
the page's canonical, checked on all 93) and
`twitter:card = summary_large_image`, the value every other page uses. Twitter
falls back to the og tags for title, description and image, as it already does
on the other pages. Head tags only.

Not verified: episode og:image points at YouTube's `maxresdefault.jpg`, which
YouTube does not generate for every upload (it serves a small grey
placeholder instead). I could not fetch i.ytimg.com from here to check which.

### 7.6 Images and speed

Lighthouse 12, mobile, performance and SEO only, run against a local server of
the built site (so no CDN, compression or third-party embeds; compare the two
columns with each other, not with the live site). Median of three runs each.

| Page | Perf before | Perf after | SEO before | SEO after | CLS before | CLS after |
|---|---|---|---|---|---|---|
| index.html | 75 | 78 | 92 | 92 | 0.006 | 0.014 |
| episodes/maxime-pinot-the-journey-within.html | 79 | 84 | 100 | 100 | 0.225 | 0.155 |
| knowledge-base/sky-gods.html | 93 | 92 | 100 | 100 | 0.006 | 0.006 |
| tags/accidents.html | 96 | 96 | 100 | 100 | 0.066 | 0.066 |
| destinations/kenya.html | 68 | 68 | 100 | 100 | 0.007 | 0.007 |

The home, KB, tag and Kenya changes are run-to-run noise (index.html and
kenya.html were not changed at all). Screenshots of all five pages at 390 and
1440 wide, full page, before and after: **pixel-identical** (0.000% of pixels
differ on all ten). Two before runs were also identical, so the comparison is
exact, not within a tolerance.

Audit first: every `<img>` on the site already has an alt attribute (580
images), so no alt text was needed. Changed:

- Logo width="480" height="100" (its real size) on the header and footer logo
  in every generator and template: episodes, tags, KB, policies, sitemap, 404.
  The CSS always fixes one dimension and sets the other to auto, so the size
  on screen is unchanged. 172 pages.
- Episode artwork (the 8 audio-only episodes): width and height read from the
  file. The CSS already fixes its box at 16:9.
- KB episode tiles for those 8 audio-only episodes served the artwork .jpg
  (about 100 KB) although a .webp (about half) sits beside it: now a
  `<picture>` with the webp, as the episode page already does.
- loading="lazy": every image below the first screen on generated pages was
  already lazy; nothing to add there.

Not changed, left for you (hand-maintained pages, which this job does not edit
by hand, or pages the brief said not to touch):

- The logo on the seven hand-maintained pages (index, about, podcast, library,
  enquire, knowledge-base.html, destinations/kenya.html) still has no
  width/height; same one-line change as above if you want it.
- index.html: `assets/podcast/plate.webp` is below the first screen and not
  lazy (Lighthouse: 89 KiB). himalayas-1.webp (302 KB) is served far larger
  than it displays.
- destinations/kenya.html: LCP 11.3s on the simulated phone; three gallery
  images (longonot, equator, kerio-valley) are served as .jpg although .webp
  versions exist (about 135 KiB).
- Home SEO 92: Lighthouse "Links are not crawlable" (an anchor without a real
  href on the homepage).
- The remaining episode layout shift (0.15, `.cd-main`) is not from images.
