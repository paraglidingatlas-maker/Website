# Paragliding Atlas v2: where we are and what is next (27 Sep 2026)

## Done
- **Every page in v2** (182, every sitemap URL), hidden and noindex until the
  switch. All 93 episodes in the chosen layout (player beside the title).
- **Homepage:** hero video, the fly-through for the four trips ("See where we
  fly" as its first frame), dates table, readable over the video.
- **Look:** soft surfaces instead of hard boxes; no red tint; no tracers;
  the map card as soft glass; the ALT / HDG readout only over moving footage,
  flying with it.
- **Phone, tablet, desktop** checked; touch sizes; reduced motion and no-JS
  safe; home 2.5 MB on arrival (was 4.1).
- **Checks:** tools/v2_check.py (every page, three widths, SEO/GEO parity
  with live) and tools/v2_switch.py (the switch-over, rehearsed, 0 FAIL).
  Design rules frozen in docs/v2-design-rules.md.

## Next, in order
1. **Trip pages rebuilt** (India first): fly-through style, about 800 words on
   first read instead of 3,300 to 4,200, every word kept folded away.
2. **Grammar fixes** (safe, make nothing duller): Arial on buttons and fields
   (patch ready), three page-title sizes and one weight, one section-head
   pattern, fewer button and chip styles, no empty voids before the footer,
   Partners brought into the site's scale.
3. **One signature moment per page** (added to the rules): the library as a
   flight log or a poster wall; topic pages with a featured row and rhythm;
   an episode page opening on a globe turned to where the story is from;
   episode cards that open into the page; a full-screen menu with photos;
   an altimeter progress marker on long pages; full-screen footage breathers.
4. **Generated images redrawn to technical-drawing standard:** one drawing kit
   (engineering line weights, the site's type, callouts, dimensions, hatching,
   title blocks citing the episode and timestamp, vector output, real curves).
   About 57 knowledge base figures, the Kenya map and plates, the trip dials,
   the poster frame, series and panel icons, contours and ridge. A before and
   after on the paraglider three-view first.
5. **An instrument font** (monospaced) for the readout, coordinates, stats and
   timestamps, as a sample first.
6. **Navigation and wayfinding:** Expeditions in the main menu (Sitemap moves
   to the footer); the current section marked in the menu; one search in the
   header across episodes, knowledge base and trips; every page ends on one
   clear next step; bridges between the halves ("from the show" on trip pages,
   "fly it yourself" on relevant episodes, real links only); the wind-sound
   button says what it is; the same sticky phone action bar on every trip
   page (and Play / Next on episodes).
7. **Business machinery:** a booking path (deposit or place-hold per
   departure, places left shown); proof from past clients on each trip page;
   a "why you can trust us" strip from the terms and agreement; an automatic
   reply and a reminder after an enquiry.

## Needs the owner
- **Footage and data:** IGC track logs for the filmed flights (real ALT / HDG
  and the real flight line on the maps), 5 to 10 s clips per destination and
  site, a wind or vario recording (optional sound), photos from past trips.
- **Business:** how to take deposits (a payment link per departure is enough
  to start), client quotes and photos with permission, the trust strip facts.
- **Facts:** Peru and Kazakhstan details, 14 episode dates and 2
  descriptions, the one episode count, one currency or both (India is in £,
  Kenya in US$).
- **The go:** an iPhone check, then the switch-over (runbook in
  docs/v2-report.md).

## Dropped on purpose (they would flatten the site)
One header style for every page, one icon style everywhere, one neutral grade
on the episode stills.
