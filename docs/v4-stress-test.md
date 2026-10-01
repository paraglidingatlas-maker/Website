# v4 stress test (1 Oct 2026)

The same stress test as the live site's (docs/live-stress-test.md), run on
`prototypes/v4/`: 186 pages, seven dimensions (viewport and zoom, network,
interaction abuse, degraded modes, accessibility, data integrity, hostile
input), each finding re-run by a second, sceptical pass. The performance pass
and the final critic did not complete (the run stopped during the performance
pass); performance is covered only by the network dimension's measurements.

**48 confirmed findings: 3 high, 21 medium, 24 low** (plus 9 info). None
critical. The repro scripts are in the session's scratchpad
(`stress-v4/<dimension>/`), not in the repo.

**Fixed: 29. Partly fixed: 3. Open: 16.** Commits 6a40bc9 and a117e46, every
gate passing (v4 191 pages 0 FAIL, switch dry run 0 FAIL, smoke 0 FAIL, v2
untouched, no live page changed).

## Fixed
| Id | Severity | Finding | Fix |
|---|---|---|---|
| DG-1 | high | Print: cards below the first screen print blank on 164 of 186 pages because of the CSS scroll-driven 'v2-surface' entrance (v4 only) | print stylesheet: entrances off, everything shown |
| VP-1 | high | Phone menu button is off screen at 280px and half off at 320px on every v4 page: the added Wind-sound button widens the header row to 341px (v4 only) | wind button, then Enquire, give way at 22.5em / 20em; menu holds Enquire |
| VP-2 | high | At 200% text the header pushes Enquire and the menu off screen on all 17 templates, even on a 1280px desktop, and header plus footer force a 460-670px layout on phones (same as live: header Enquire/menu at 200% text + footer 12.86rem; v4 makes it worse) | header and footer breakpoints repeated in em, so they follow the reader's text size |
| A11Y-V4-1 | medium | KB series hero drawings never draw on 320-390px phones: lines and words stay invisible (v4 only) | drawings wider than the screen draw on any overlap |
| A11Y-V4-2 | medium | Fixed phone bottom bars (#v4Epbar on episodes, #dstMobar on trips) take Tab focus while hidden and cover focused controls once shown | phone bars hidden from Tab while off screen |
| A11Y-V4-3 | medium | KB door (#iris) is aria-modal, but Tab goes straight to the page underneath (same as live: KB door dialog lets Tab escape) | Tab kept inside any open aria-modal dialog |
| A11Y-V4-4 | medium | Kenya photo lightbox and KB episode popup do not contain focus (same as live: lightbox focus not contained / episode popup focus not contained) | same (Kenya lightbox verified: 0 escapes in 12 Tabs) |
| A11Y-V4-5 | medium | KB 'Read more' and FAQ questions stay at opacity 0 when reached by Tab (same as live: KB FAQ questions opacity 0 on focus) | revealed blocks show on focus-within |
| ABUSE-2 | medium | Homepage episode rail arrows barely move the rail: the auto-drift loop cancels their smooth scroll (v4 only) | rail arrows pause the drift; three presses move about 2.4 screens |
| ABUSE-3 | medium | The full-screen menu stays open over the homepage after choosing 'Expeditions' (same-page link), with scroll locked and focus outside the dialog (v4 only) | same-page links in the menu close it |
| DG-10 | medium | Print truncates the episode transcript to the collapsed 620px clip | print shows the whole transcript |
| DG-3 | medium | Printed knowledge base drawings vanish: light kit strokes and labels on white paper, and below-the-fold drawings still hidden by kd-h and the kr reveal | drawings finished before print (beforeprint) and turned for paper |
| DG-4 | medium | Forced colors (light theme): the white labels and lines in the kit drawings disappear on the forced white canvas (v4 only) | forced-colors rules map the kit's lines and words to system colours |
| DG-7 | medium | No-JS: the knowledge base landing's category stations are invisible (72% of the page's visible text) | noscript override shows the KB stations |
| INT-1 | medium | KB landing: the drifting episode wall behind the hero shifts by about 104px twice during load, giving CLS 0.11-0.17 on desktop and 0.18-0.25 on phone (also on live, intermittently; not in the live list) | KB wall fills from the top |
| NET-1 | medium | Phone menu, header Search and the 404 search link do nothing when the on-demand v4-menu.js fails or is slow, and the tap is swallowed (v4 only) | if v4-menu.js fails or takes 6 s: toggle opens the small panel, search goes to the sitemap |
| NET-3 | medium | India hero slideshow advances and pulls in every full-size hero photo before load: over 2 MB own-host before load and LCP 44 s on Slow 3G | India and Kenya slideshows wait for load; save-data and 2G keep the first photo |
| VP-3 | medium | Knowledge base band drawings render their labels at 5-9px between 761 and about 1300px, because the phone version switches in only at 760px (v4 only) | phone versions of band drawings hold to 1000px |
| VP-5 | medium | Knowledge base grids have 320px and 278px minimum columns, so series cards run to 344px on 280 and 320 screens (same as live: KB grids wider than 280px) | KB grids use min(100%, …) |
| VP-8 | medium | On 2560/3840 screens, an undrawn knowledge base drawing's large circle (overflow:visible) is the hit target over READ MORE and the guest chips above it (v4 only) | drawings take no pointer events |
| A11Y-V4-8 | low | Scrollable regions that cannot be reached by keyboard (axe scrollable-region-focusable) | scroll boxes get tabindex, role=region and a name |
| ABUSE-1 | low | A knowledge base band drawing whose draw-in is cut short by the wide/phone swap stays partly drawn for good (v4 only) | same as DG-2 |
| ABUSE-5 | low | Menu search adds one search-index.js <script> per keystroke while the index loads, and shows nothing (forever if the index fails) (v4 only) | one index script; a message and the sitemap link if it fails |
| DG-2 | low | Knowledge base drawings stop short for good after the window is narrowed below 760px while one is drawing (part 11 leaves a stale inline dash; v4 only) | draw-in also ends on transitioncancel |
| DG-6 | low | Reduced motion: collapsing an episode transcript still smooth-scrolls (v4 dropped live's reduced-motion check) | transcript collapse respects reduced motion |
| HOST-1 | low | A malformed percent-escape in the URL hash throws an uncaught URIError: it breaks the podcast globe and leaves the library unpaginated (same as live: URIError on malformed hash / library hash router URIError) | decodeURIComponent in try/catch |
| NET-6 | low | Knowledge-base landing eager-loads 220 YouTube thumbnails for the decorative tile wall | wall thumbnails lazy |
| VP-6 | low | Home and podcast listen sections have a min-content wider than a 280/320 screen (home 352px) (v4 only) | min-width:0 on the listen and search columns; 280px has no sideways scroll |
| VP-4 | medium | At 200% text the knowledge base band-figure quotes are cut off (same as live) | the quote's 900px rule repeated in em, so with large text it moves under the picture (1280px at 200%: 0px clipped) |

## Partly fixed
| Id | Severity | Finding | What changed, what is left |
|---|---|---|---|
| A11Y-V4-6 | medium | No main landmark on many pages and no skip link on any page (same as live: no skip link / no main landmark) | skip link added on every page; the main landmark is still missing (wrapping the content would break the page-wrap > section rules) |
| A11Y-V4-7 | medium | Interactive content nested inside role=slider and role=img (axe nested-interactive, serious) | the sitemap graph is now a group; the audio player's seek bar is in the shared episode-audio.js, not changed |
| A11Y-V4-11 | low | Minor axe and SVG naming items | icons inside labelled links and buttons hidden; the podcast globe not changed |

## Open
Left for a later round or for the owner. Most are low; the one medium is
DG-5 (text spacing pushes Enquire off at 1280-1366px). Letting the header row
wrap was tried and dropped: at the default spacing the row only fits at
1280-1366px by shrinking, so it wrapped there for everyone.

| Id | Severity | Finding | Cause (from the finding) |
|---|---|---|---|
| DG-5 | medium | Text spacing (WCAG 1.4.12) pushes the header's Enquire Now button off screen at common desktop widths (v4 only at these widths) | prototypes/v4/src/v2.css:1777 '.page-wrap > nav .v4-nav a{white-space:nowrap}' plus the extra header controls v4 adds (wind sound and search |
| A11Y-V4-10 | low | fly-options trip tabs: Tab to tabs 02-04 leaves the focused tab 226px above the viewport (v4 only, sample page) | fly-options.js: the panel opens on focus and re-lays out after the browser has scrolled the focused tab into view |
| A11Y-V4-9 | low | Contrast: the only axe failures are buttons inside dimmed fly-through slides; real only on the fly-options sample (v4 only) | fly-options.html fo3 slide styling: a focused slide is not raised to full opacity (no :focus-within rule) |
| ABUSE-4 | low | fly-options swipe strip: a mouse drag that starts on a picture or link gets stuck, and the strip then follows the mouse with no button held (v4 only) | prototypes/v4/fly-options.js:74-90 (generator tools/v2_fly_options.py). It listens for pointerdown, pointermove and pointerup only. There is |
| ABUSE-6 | low | fly-options swipe strip drops arrow and key presses made while the previous slide is still scrolling (v4 only) | prototypes/v4/fly-options.js:53-62 and 67-69. go(cur + 1) uses cur, which mark() updates only when the scroll position's nearest slide chang |
| ABUSE-7 | low | Enquire form: 20 rapid submits fire 20 mailto navigations, and a long (10 kB) message is refused by the 1900-char mailto cap (same as live: no double-submit guard; mailto 1900-char cap) | prototypes/v4/enquire.html inline script (sendByMail and the submit handler): no in-flight flag in mailto mode, and href.length > 1900 is re |
| ABUSE-8 | low | Kenya gallery: 6 of 16 photo cards have an empty data-title, so the live region and the lightbox caption announce nothing for them (same as live: not in the list) | prototypes/v4/destinations/kenya.html card markup (data-title=""), read by prototypes/v4/kenya-gallery.js:69 and :94 (live.textContent and l |
| DG-8 | low | Forced colors: dots and bars drawn with background colours vanish (gallery dots, season date bars, live dot, chapter dots) | background-color-only indicators with no forced-colors fallback (border or forced-color-adjust) in prototypes/v4/src/v2.css and the shared s |
| DG-9 | low | No-JS phone header shows only Enquire Now; the section links are reachable only through the footer | the .nav-toggle / v4 menu button is created by prototypes/v4/src/v4-menu.js:135 and v2-immersive.js:592; the .v4-nav links are display:none  |
| INT-3 | low | Sitemap graph: 8 audio-only episodes share the node id "ep:", so they collapse into one node (same as live: sitemap graph shared id) | The SITEMAP_GRAPH data inlined in prototypes/v4/sitemap.html:440 builds the episode id from the YouTube id, which is empty for audio-only ep |
| INT-4 | low | og:image is relative on 8 audio-only episode pages (same as live: og:image relative on 8 audio-only episodes) | The v4 episode pages were copied from the live audio-only episode heads, which carry the relative path. |
| NET-2 | low | Render-blocking head chain on every template: styles.css + v2.css + page CSS + 2 synchronous head scripts (v4 adds v2.css and the head scripts) | tools/v2_localize.py:112-115 inserts <script src=v2.js> and <script src=v2-immersive.js> before </head> without defer; v2.css is loaded in f |
| NET-7 | low | Very heavy HTML on KB articles and the drawings sample delays DOMContentLoaded (and everything that waits for it) by 16-38 s on Slow 3G | inline band drawings emitted into the page HTML by the v4 KB generators (tools/v2_*.py / tools/kbfig); the end-of-body synchronous <script s |
| NET-8 | low | Podcast feed status stuck on 'Connecting to YouTube feed...' / 'Connecting to RSS feed...' when JS fails | static 'Connecting...' placeholder text in prototypes/v4/podcast.html, replaced only by rss-feed.js / the YouTube glimpse script |
| NET-9 | low | Audio-only episode Play when offline: unhandled rejection and no message | /home/user/Website/episode-audio.js:90 and :142 (audio.play() with no .catch and no error UI); prototypes/v4/src/v2-immersive.js:626-631 jus |
| VP-7 | low | Episode chapter tap targets collapse at narrow widths: the new chapter track has ticks 2-27px wide; the audio-only player's chapter markers overlap each other | prototypes/v4/src/v2.css:953: .ep2-tick width calc(var(--w)*1%), proportional to chapter length with no minimum. Audio markers: episode-audi |

## Information
| Id | Severity | Finding | Note |
|---|---|---|---|
| A11Y-V4-12 | info | Checked and working: v4 menu/search dialog, focus indicators incl. forced colors, drawing twins, drawing names | n/a |
| HOST-2 | info | No DOM XSS reachable in v4: every flow from an attacker-controllable source was traced and fuzzed, and none executed (v4 only, info) | n/a (no defect). Hardening only: prototypes/v4/src/v4-menu.js:37-46 and :91 build hrefs and data-bg from BASE (taken from location.pathname) |
| HOST-3 | info | Third-party, link and secret surface is clean; header-level hardening is absent (v4 only, info) | Hardening advice: add a <meta http-equiv=Content-Security-Policy> (script-src 'self'; frame-src https://www.youtube-nocookie.com; media-src  |
| INT-2 | info | The Search/menu button's aria-controls="v4Menu" points to an id that does not exist until the menu is first opened (v4 only) | prototypes/v4/src/v2-immersive.js:595 `b.setAttribute("aria-controls", "v4Menu")` in mount(), while the element is only created in src/v4-me |
| INT-5 | info | HTML parse errors: stray </p></p> in 2 episode transcripts (same markup as live) | The episode transcript note template doubles the closing </p> for these two episodes. |
| INT-6 | info | Sample and styleguide pages: canonical points at the homepage or library, and drawings-all.html is 1.46 MB with 5,396 DOM nodes (v4 only, prototype pages) | The sample and option pages copied the home or library head. Their size comes from tools/v4_samples.py, which inlines every drawing. |
| NET-10 | info | Measurements: resource-failure injection and own-host 404 sweep found nothing else | n/a |
| NET-5 | info | Homepage LCP 21.9 s on Slow 3G: the LCP is a decorative cloud overlay (CSS ::before background) that arrives behind 1 MB of below-the-fold photos | prototypes/v4/src/v2.css:556-561 (.kit-hero:not(.is-sky)::before background:url(cloud-3.webp)), together with the lazy .v2-fb-shot photos at |
| VP-9 | info | Large-screen typography: no body text under 14px and line length mostly fine; several 11.8-13.9px secondary text styles and 2 paragraphs over 120 characters per line | Fixed rem/px font sizes for captions and notes in prototypes/v4/src/v2.css and the KB inline styles |

## Coverage
- **network**: 17 v4 templates on Slow 3G (400/400 kbit/s, 400 ms) and Fast 3G (1.6 Mbit/s / 750 kbit/s, 150 ms). Cache was disabled through CDP, on a 390x844 phone at DPR 2. Measured: FCP, LCP plus the LCP element, DCL, load, CLS, own-host bytes and requests before load, largest resources, render-blocking resources (renderBlockingStatus) and external hosts.  Resource-failure injection ran 6 modes (normal, fonts, JS, CSS, images, every non-local host blocked) on all 17 templates at 390, and normal/JS/external also at 1280. Each run checked h1 visibility, visible main-text characters vs normal, uncaught error
- **viewport**: Covered everything the viewport task asked for.  **Main sweep.** All 186 v4 pages at 5 sizes: 280x653, 320x568 and 844x390 (is_mobile + has_touch), plus 2560x1440 and 3840x2160. That is 930 loads with 0 errors. For each one I scrolled the page through to fire the reveals, then measured: - horizontal overflow, using the visual viewport rather than innerWidth (mobile emulation widens the layout viewport) and naming the culprit elements; - text clipped inside overflow:hidden boxes; - fixed/sticky elements covering more than 35% of the height at 844x390, at the top and mid-page; - elementFromPoint
- **degraded**: All five degraded modes ran against the v4 prototype on port 8914, using the repo root as the server root.  (1) JS off against JS on: all 186 pages at 1280, plus the 390 phone header and footer on every page. Text, images, script-filled containers, and script-built forms and controls were diffed.  (1b) KB drawings without JS: all 18 svg.kbd pages, plus knowledge-base.html, samples/drawings-all.html and tags/safety.html, at 1280 and 390. Checked: hidden strokes and text, and the has-p/kbd-p phone swap.  (2) Reduced motion on the 17 templates. Checked: getAnimations, the rAF rate, frame diffs at
- **abuse**: Port 8913, Chromium headless. External hosts were aborted in the browser context (they are blocked by the environment anyway). Sections, with results in out/*.json: (1) Menu on all 17 templates at 1440 and 390. Per template: 50 open/close cycles by click (alternating close button and Escape), 50 by keyboard (Enter/Space on the button, then Escape), 60 Tab plus 60 Shift+Tab inside the menu, and a click into the search field. End state on every template: menu hidden, html not locked, 1 menu, 1 v4-menu.js script, focus back on the opener, page scrolls 600 px after closing. Focus never left the me
- **integrity**: I covered all 186 v4 pages statically: html5lib parse plus BeautifulSoup. The checks were: - every href/src/srcset/poster/data-src/data-bg/inline style url() resolves to an existing file, including ../../ links to the live shared files, and every #fragment resolves to an id or name in its target - duplicate ids per page - url(#x), <use>/<image> href=#x and aria-*/for IDREFs point to existing ids - JSON-LD parses and has @context/@type, and its site URLs exist - images without width/height or an inline aspect-ratio - HTML size, element count, h1 count, main, lang - canonical and og:url, og:imag
- **hostile**: Static review: every JS file the 186 v4 pages load. That is the 10 files under prototypes/v4/ (v2.js, v2-immersive.js and its src, v4-menu.js and its src, v2-home.js, v2-library.js, kenya-gallery.js, fly-options.js, search-index.js) plus the shared root scripts v4 references: script.js, nav-menu.js, episode-sync.js, episode-modal.js, episode-audio.js, waveforms.js, tags-sort.js, newsletter.js, home-episodes.js, library-episodes.js, youtube-feed.js, sitemap-graph.js, rss-feed.js (referenced once in the HTML but not executed on the v4 pages tested), kenya-map.js, episode-search.js, globe.js and 
- **a11y**: Ran axe-core (wcag2a, wcag2aa, wcag21a, wcag21aa, best-practice) on all 186 v4 pages at 390x844 and on the 17 templates at 1440x900. Each page was scrolled top to bottom first and given 2.6 s so reveals and drawings had run; external hosts were aborted; 0 page errors; 428 s. The same pass audited every inline SVG: accessible name, labelledby targets, decorative or hidden, the .has-p/.kbd-p twins, and drawings left undrawn. Keyboard walk (up to 300 Tabs) on the 17 templates at 1440 and at 390, plus a forced-colors walk at 1440. For each focus stop it checked whether the element was hidden or of
