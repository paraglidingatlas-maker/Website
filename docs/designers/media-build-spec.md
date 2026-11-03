# Media page: the build spec (chat 17, 3 Nov 2026)

The design round (docs/designers/media-brief.md) is over. Three judges (a race director, a sponsor's brand manager
and an Awwwards critic) tried all three mocks at 1440x900, 390x683 and 390x844 and **all three picked E,
"Pull Back To The Coverage"** (Cloudbase): scores E 24.2, F 22.1, D 19.3. This file is the one list the build
works from: E's mock, plus what the judges said to take from F and D, plus what they said must be fixed.
The brief's rules all still hold: organisers and sponsors only, no prices, nothing invented ([to supply], class
v2-tbd), EXAMPLE marked on the quote, "Most chosen" and the 2027 months, no em dashes, the site's two fonts and one
orange, btn-solid (inner span) and btn-lines with data-hover, reduced motion and no JS show the finished page.

Mocks (kept as they are, do not edit): prototypes/v4/samples/media-e/ (the winner: index.html, media-e.css,
media-e.js), prototypes/v4/samples/media-f/index.html, prototypes/v4/samples/media-d/index.html.

## Where it is built
- A1. The page comes from the generator, not by hand: tools/v4_media.py writes prototypes/v4/media.html (and
  media-srs-piedrahita-2026.html). Port E's markup into media_page(). E's CSS goes into one shared file
  prototypes/v4/v4-media.css (linked from both media pages with ?v=), and E's script is merged into
  prototypes/v4/v4-media.js, keeping everything that file already does (play in place, the reel list, chips,
  the justified rows, the photo viewer copied from fly.js, data-md-out for the preview).
- A2. Photos come from the MEDIA base (default the future media-2026 repo, `--media img/media-tmp/` for the
  preview). The opening photo SRS_5_T2_133-2 has a 2400 px copy in img/media-tmp/: use it in srcset for retina.
- A3. tools/v4_media_preview.py packs the new CSS file, and packs prototypes/v4/enquire.html too, so the preview's
  dates form lands on the preview's own enquiry page in its media mode (not the live pilot form).
- A4. The shell (about.html) brings the About page's polish block (a count-up on hero figures, the trips' tilt):
  drop it from the media pages.
- A5. The Piedrahita event page (speaks to pilots) keeps working with the shared CSS and JS. No redesign now:
  its photo pick is still with the owner.

## The opening (hero)
- H1. Every hero number names its source at every size, phone too: "21,690 views, PWC Super Final",
  "7,342 views, one task day film", "21 h 42 min live, SRS Bassano" (D's crediting). No "Views of one event".
- H2. Phone: Book a Call sits beside Check dates for your event on one row, not alone underneath. A stronger scrim
  under the copy where it runs over the wing and the white cloud (deck text at least 4.5:1).
- H3. The slate is fed by one list of upcoming events in the generator (today: SRS Tapalpa, Mexico, tasks 8 to 14
  Nov 2026). With JS: "Next ... in N days" before, a lit "On air now" during the task days, and after the last
  task the slate drops the countdown (and the next event is [to supply] until the list has one). Without JS it
  shows the dates. A real tally light is steady: it never blinks.
- H4. Logo slots carry the full names under the lockups (SRS: Sports-Class Racing Series; PWCA: Paragliding World
  Cup Association) and stay marked as logo slots until the files arrive.
- H5. On this page the header's Enquire Now goes to #dates (the dates form), not to the pilots' trip enquiry.

## The four posters (the pull-back)
- P1. No dead taps: once the pull-back starts the hero layer takes no pointer events, and the shot itself is the
  Daily Highlights link at every stage.
- P2. No messy middle frames: the Daily Highlights label rides on the shot as soon as the other three start to
  slide in; the cards are opaque during the move; the heading "Four Pieces Of Coverage" is never covered.
- P3. Phone: the move ends on large tall posters (a swipe rail of cards about 280 px wide, or full width), on F's
  numbered line (01 Before the race, 02 Every task day, 03 After the race, 04 Mid-season), never 165 px
  thumbnails. Desktop keeps the row of four. The shot lands at a readable size.
- P4. Phone: the scrub finishes within about 0.8 of a screen of scrolling, and a stop or fast flick never leaves
  the visitor on a half-scaled frame.
- P5. Each poster names the package it is in, from the packages below (for example "In Daily and Full Event").
- P6. Every poster leads somewhere (Pre-Race Show to the Kenya episode, Daily Highlights plays the most watched
  video in place, Aftermovie and Race Behind The Race light their package and pick it in the form).

## Packages
- K1. Each card shows what it covers as a bar (F): Before / Task days / After; Season as every stop of a series.
- K2. Every Check dates (each package card, each poster that names a package) picks that package in the form.
- K3. Daily: the number of social clips per task day is [to supply].
- K4. A short "Where your sponsors appear" block (the sponsor's first question): the joint posts on both channels
  (a fact), and the rest (in the films, in live commentary, in the results newsletter) each marked [to supply]
  until the owner confirms. Nothing invented.

## Reach
- R1. E's cropped-wing "One joint post" card goes. In its place F's reach: a giant 31,250 ("views on 13 comp videos
  in 2026, counted 3 Nov") over a photo band of the gaggle, then the 2026 season on its real dates (May to Nov), a
  TODAY marker, Tapalpa lit as Next, the views per event, a Watch link on every event (plays in place or opens the
  showreel on that comp), and "Your comp next? Check dates".
- R2. D's line under the total: "Most watched: Task 1 Highlights, PWC Super Final, 7,342 views for 6:53 of an
  86.5 km sprint".
- R3. One joint post, two audiences, said plainly and legibly (your channels and Paragliding Atlas), no wireframe
  boxes and no tiny overlay labels.
- R4. The base audience row is on the page: channel subscribers and followers, [to supply]. The podcast's
  136 countries drops to a secondary line. Counts keep their source stamp (YouTube, 3 Nov 2026).

## Proof
- Q1. The quote's EXAMPLE mark stays visible at phone width.
- Q2. DM Mono only on the slate and the tally. The video meta and the reel list are set in DM Sans and never wrap
  into ragged two or three line stacks on the phone.

## Delivery, FAQ
- D1. The "We need" list numbered 01 / 02 / 03, and the delivery caveat set as its own line (same day or end of the
  week, subject to internet on site, the task finish time and access to footage), like a production rider.
- F1. The FAQ heading: "What Organisers Ask First".

## The dates form
- S1. The 2027 season (EXAMPLE) reads Open / Held / Booked (booked months struck through); tapping an open month
  fills the dates field.
- S2. Fields have a scroll-margin-top larger than the fixed header, so validation bubbles never land under the nav.
- S3. The hand-off to enquire.html (the contract with its media mode):
  GET enquire.html?trip=media&event=...&when=...&place=...&package=daily|full|season|unsure
  (package is never empty: "Not sure yet" is unsure). Name and email inputs carry no name attribute, so they
  never go into the address bar; on submit the script saves them as JSON {"name":..,"email":..} in
  sessionStorage key "v4-media-enq" and enquire.html reads it once and removes it.
- S4. The phone booking bar is slim, and is hidden while the opening, the pull-back, any in-section Check dates,
  the form or the footer is on screen: never two orange buttons at once.

## enquire.html, media mode (prototypes/v4/enquire.html)
- N1. A "Media coverage" option in the Destination list (value media), always there; choosing it, or arriving with
  ?trip=media, switches the form to its media mode.
- N2. Media mode: copy speaks to organisers; "Your flying" is hidden and none of its fields is required; an "Your
  event" fieldset shows Event (required), Dates, Place and Package (Daily, Full Event, Season, Not sure yet),
  prefilled from the URL and from sessionStorage "v4-media-enq"; the message is optional ("Anything else").
  Switching back to a trip restores the pilot fields and their required marks.
- N3. The mailto subject is "Media enquiry: <event>" and the body carries event, dates, place and package; the
  Worker POST (when ENDPOINT is set) carries them in its FormData. The "Hold a place" arrival (?trip=..&when=..)
  never fires for trip=media. Book a Call and WhatsApp stay.

## Everywhere
- G1. No horizontal scroll at 360, 390, 768, 820, 1024, 1440 and 1920 wide. No console errors.
- G2. Reduced motion and no JS show the finished page; ambient motion pauses off screen.
- G3. Tested at 390x683 (the owner's phone in the Claude app), 390x844 and 1440x900 before the owner sees it.
