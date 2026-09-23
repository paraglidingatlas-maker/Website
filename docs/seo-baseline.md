# SEO baseline, 23 September 2026

Written by the overnight SEO job (task 7.8). Report only: nothing in this file
changed the site. Numbers are from the repository as built on the night of
22 to 23 September 2026, after tasks 7.1 to 7.7.

## (a) Links, images and the judgement calls from 7.7

### Internal links

- **Broken internal links: none.** Every `<a href>` on the 206 non-stub pages
  that points inside the site resolves to a file.
- **Links into redirect stubs:** six "Related episodes" links on five episode
  pages pointed at `episodes/new-technologies-5-frantisek-pavlousek-2.html`, a
  noindex stub. Fixed in 7.7 (c18fe95); none remain.
- **Missing images: none.** Every local `img src`, `source srcset` and inline
  CSS `url()` resolves to a file.

### External links: not checked, and why

This machine's network policy blocks outbound requests to every outside site
(curl and WebFetch were both refused, including for paraglidingatlas.com
itself), so no external link could be tested. There are 337 distinct external
links:

| Domain | Links |
|---|---|
| www.youtube.com | 86 |
| podcasts.apple.com | 81 |
| podcasters.spotify.com | 80 |
| anchor.fm | 80 |
| calendar.app.google, wa.me, open.spotify.com, castbox.fm, www.podbean.com, www.patreon.com, www.instagram.com, music.amazon.com, a typeform, www.allaboutcookies.org | 1 each |

Worth checking first: the 80 `podcasters.spotify.com` links. That is Spotify's
old name for Spotify for Creators, and it now answers at
`creators.spotify.com` (the address that appeared in the search results in
part c). The old links probably still redirect, but through an extra hop. A
link checker run from a normal connection (for example `lychee` or
`linkchecker` over the built site) would settle all 337 in a few minutes.

### Judgement calls, deliberately not changed

1. **sitemap.xml `lastmod` is the file's modification time**
   (`generate_robots_sitemap.py`), not the last real change. On a fresh
   checkout every page claims to have changed that day, and every build
   rewrites all 177 dates. `tools/inject_site_schema.py` already takes
   dateModified from `git log`; using the same source for `lastmod` would make
   the two agree and stop the daily churn. Search engines discount a lastmod
   that is always today.
2. **Thin tag pages.** 13 of the 50 tag pages list only 3 episodes: ccc,
   free-flight, impact-protection, materials, mountaineering, open-class, oslo,
   piedrahita, safety-training, spain, srs, visualization, x-alps. A further 9
   list 4. They are indexable and in the sitemap. Options: leave them (they
   are real hubs with unique text), or merge the smallest into broader tags,
   or noindex them. Your call.
3. **noindex.** Only 404.html and the 28 redirect stubs are noindex. That looks
   right; nothing indexable is hidden.
4. **Related-episode data.** Ziad Bassil's entry lists New Technologies 5 twice,
   and New Technologies 5 lists itself. Not changed, because task 7.11 says
   existing related entries must not be edited.
5. **Homepage "Links are not crawlable"** (the one Lighthouse SEO failure on the
   home page): `<a class="popup-link" data-hover>` has no `href`. A `<button>`
   or a real href would clear it; index.html is hand-maintained, so it was
   not edited.
6. **Episode meta descriptions are the summary cut at 155 characters,
   mid-word**, on most episodes. Cutting at the last whole word would read
   better in results.

## (b) Lighthouse, from 7.6

Lighthouse 12, mobile, local server of the built site (no CDN or
compression, third-party embeds blocked), median of three runs.

| Page | Performance | SEO | LCP | CLS |
|---|---|---|---|---|
| Home (index.html) | 78 | 92 | 5.9 s | 0.014 |
| Episode (maxime-pinot-the-journey-within) | 84 (was 79) | 100 | 3.1 s | 0.155 (was 0.225) |
| Knowledge base (sky-gods) | 92 | 100 | 3.1 s | 0.006 |
| Tag (accidents) | 96 | 100 | 2.4 s | 0.066 |
| Destination (kenya) | 68 | 100 | 11.3 s | 0.007 |

Biggest remaining opportunities: Kenya LCP (a large hero plus three gallery
JPGs whose WebP versions exist but are not used), the home page's
`himalayas-1.webp` served much larger than displayed, and render-blocking
`styles.css` and `fonts.css` on every page.

## (c) Twenty questions the knowledge base answers, searched

Each question is taken from a knowledge base page's FAQ and was searched on
23 September 2026 with a US web search. **paraglidingatlas.com appeared in
none of the 20.** The brand did appear twice, through its own podcast pages on
Spotify for Creators (and once YouTube), which suggests the episode audio
ranks while the site itself is not yet indexed or trusted for these queries.
Worth checking in Search Console whether the knowledge base pages are indexed
at all yet; they only went live in the new layout this week.

| # | Question (KB page) | paraglidingatlas.com? | What ranks instead |
|---|---|---|---|
| 1 | What is pitch-up tendency in a paraglider? (flight-mechanics) | No | flybgd.com, paraglidingequipment.com, xcmag.com, templepilots.com, Wikipedia, passionparagliding.com |
| 2 | Does EN certification tell me how likely a wing is to collapse? (flight-mechanics) | No | flybubble.com, adventuro.com, bhpa.co.uk, xcmag.com, paramotorplanet.com |
| 3 | When should I do my first SIV course? (risk-vs-reward) | No | riseparagliding.com, flywithbehrooz.com, paraglidenewengland.com, paraglidingunlimited.com, bhpa.co.uk |
| 4 | What is intermediate syndrome in paragliding? (risk-vs-reward) | No | xcmag.com, paragliding-lessons.com, ushpa.org, cloudbasemayhem.com, paraoz.com.au |
| 5 | How big should my reserve parachute be? (know-your-equipment) | No | paraglidingequipment.com, flyozone.com, flybubble.com, airetaventure.com |
| 6 | Round, square or Rogallo: which reserve is safest? (know-your-equipment) | No | paraglidingequipment.com, xcmag.com (two), flybubble.com, flyspain.co.uk |
| 7 | Is a two-liner paraglider safe for a B pilot? (new-technologies) | No | niviuk.com, xcmag.com, fly2base.com, schnellcraft.com, ziadbassil.blogspot.com |
| 8 | What is the Supair Skymate smart harness? (new-technologies) | No; the Atlas Sky Gods episode on creators.spotify.com ranked first | skymate.supair.com, flybubble.com, xcmag.com, supair.com |
| 9 | What is CIVLRESIGN? (the-dark-side) | No; the Atlas episode ranked 2nd (creators.spotify.com) and 3rd (YouTube) | hyperpilot.substack.com, xcmag.com, sahpa.co.za |
| 10 | How are paragliding competitions scored? (world-cups) | No | fai.org, onlinecontest.org, xcmag.com, xcontest.org, Wikipedia |
| 11 | What is the Sports Racing Series in paragliding? (world-cups) | No | facebook.com, xcmag.com, youtube.com, airtribune.com, cloudbasemayhem.com, sportsracingseries.org |
| 12 | What is a good pre-flight routine for paragliding? (resources-tools-tips) | No | flybubble.com, paragliding-lessons.com, paraglidingshop.com.au, paragliding24.ch |
| 13 | What is the wave leading edge on a paraglider? (brand-stories) | No | gingliders.com, xcmag.com, youtube.com, ojovolador.com |
| 14 | When is the paragliding season in Bir Billing? (navigators) | No | thehosteller.com, stayvista.com, makemytrip.com, traveltriangle.com, birbillingparagliding.com |
| 15 | Where can you go paragliding in Kenya? (navigators) | No | paraglidingmap.com, getyourguide.com, tripadvisor.com, wildsprings.co.ke, convergenceparagliding.com |
| 16 | Can you paraglide at 8,000 metres? (sky-gods) | No | quora.com, Wikipedia, 8000paragliding.com, outuro.com |
| 17 | Can you fly a paraglider with your dog? (living-the-dream) | No | emmenetonchien.com, pethelpful.com, airetaventure.com, wilderdog.com |
| 18 | What should you do right after a mid-air collision? (storytellers) | No | news sites (nbcnews.com, foxnews.com), youtube.com, researchgate.net |
| 19 | How do you spot an inversion on a sounding? (weather-patterns) | No | flyDrama (Google Sites), xcmag.com, portugalparagliding.com, pataga.net, windy.com |
| 20 | What should you do when your paraglider collapses? (technical) | No | xcmag.com (two), flybubble.com, skynomad.com, paragliding-lessons.com, footflyer.com |

Patterns: xcmag.com ranks for 12 of the 20, and flybubble.com for 6. Where the
Atlas has something no one else has (Skymate, CIVLRESIGN), the episode already
ranks through Spotify; linking those Spotify and YouTube listings back to the
matching site page would help the site inherit that.

## (d) Destination and tour pages: suggestions only

The only destination page is `destinations/kenya.html` (hand-maintained);
`enquire.html` is the booking page. Nothing here was changed.

### destinations/kenya.html

- **Title** ("Kenya: Paragliding in the Cradle of Humankind | Paragliding
  Atlas", 66 characters): strong brand line, but it has no word a pilot
  searches for. Something like "Kenya Paragliding Tour: 12 Days in Kerio
  Valley | Paragliding Atlas" (67) matches "paragliding tour Kenya" and
  "Kerio Valley paragliding".
- **H1** is just "Kenya". A pilot-facing H1 such as "Paragliding in Kenya:
  a 12-day guided XC tour from Kerio Valley" says what the page is. Keep the
  "Cradle of Humankind" line as the kicker.
- **Headings**: several H2s are evocative rather than descriptive ("The
  practical country", "A Flight of Human Genesis", "Eleven frames from the
  Rift"). Answer-engine extraction favours headings that name the topic, for
  example "Flying conditions in Kenya", "Kenya flying sites" (the "Six sites
  down the Rift" section), "Tour dates 2027".
- **FAQ**: six questions, marked up as FAQPage. Questions people search that
  the page could answer: "When is the best time to paraglide in Kenya?" (the
  page says peak season is December to March), "How strong are the thermals
  in Kerio Valley?" (6 m/s is on the page), "What rating do I need?" (IPPI 2
  is in the schema), "Where do I fly into?" and "What does the tour cost?".
  The Navigators KB page already has "Where can you go paragliding in
  Kenya?"; link the two both ways.
- **Structured data**: the TouristTrip is minimal. It could carry the two
  departures as `offers` or as an `Event` each (18 to 29 January 2027,
  1 to 12 February 2027, both on the page), `duration` (P12D),
  `touristType` is already there, `image` (the hero), and
  `provider` as `{"@id": "https://paraglidingatlas.com/#organization"}`
  instead of a second, unlinked Organization. No price is published, so no
  price should go in the schema.
- **Speed**: see (b). LCP is 11.3 s on a simulated phone; the page is 350 KB of
  HTML and loads about 3 MB in total.

### enquire.html

- Title "Enquire | Paragliding Atlas" names no activity; "Enquire About a
  Guided Paragliding Trip | Paragliding Atlas" would say what it is.
- Its ContactPage markup is now linked to the site graph (7.3).
