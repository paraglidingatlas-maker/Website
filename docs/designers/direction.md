# The home page's design direction (the three standing designers read this first)

The owner's site: Paragliding Atlas, a paragliding podcast, knowledge base and
guided expeditions. v4 is the prototype (`prototypes/v4/`, live at
https://paraglidingatlas.com/prototypes/v4/). The designers are
`.claude/agents/designer-d.md`, `designer-e.md` and `designer-f.md`; each keeps
a notebook here (`D.md`, `E.md`, `F.md`). Chats record the owner's decisions in
this file, newest at the top of the log, in the owner's own words.

## The brief (unchanged since round 1, 23 Oct 2026)
The home opening must be awwwards worthy and true to the owner: their own
photos and footage only, the site's look (dark ground, one orange, Poppins and
DM Sans, design tokens), nothing invented. Motion answers the visitor, with the
owner's exceptions below. Reduced motion and no JavaScript show the finished
page. Work lean: at most two options, one preview for a big change.

## Where it stands (24 Oct 2026)
The winner is F, "Fly the Season", built on as F2: the review page
https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG (F2/index.html) and the
prototype copy `prototypes/v4/samples/opening/`. A giant place name, the wing
cut out in front of it with its shadow on the letters, depth from the photo in
WebGL; the season line Oct 2026 to Nov 2027 with each tour at its real dates
and a readout under the photo. The owner said "do it" to building it into the
v4 home page (chat 10's job).

## Decision log (newest first)
- 25 Oct (chat 14): "yes Poster strip into home": samples/listen-c is the home page's podcast section
  (tools/v4_home_listen.py now copies it). The contour lines must run on unbroken from the section's map into
  each poster ("the contour strips do not match ... with those above") and fade out sooner on the posters (by
  about a quarter of their height). Fixed: the posters' resting tilt hid the section's lines above the cards.
- 25 Oct (chat 13): one width across the site, "go with 1": on screens wider than 1440px every page uses
  the opening's margin, 72px from each screen edge (src/v2.css "ONE WIDTH ACROSS THE SITE": --gutter 72px,
  --measure 100% minus 144px, plus overrides for the pages with their own containers: partners, the record,
  the knowledge base hub and topic pages, episodes). Up to 1440px nothing changes. Left as designed: the
  knowledge base climb's staircase, the partners journey's spine, full-bleed photos, maps and rails.
  The listen-c preview: the posters back with faint contour lines that run on into the section and fade;
  the strip drifts on its own again. No compass (the owner: the dial and the rose "look odd").
- 25 Oct (chat 13): the call band kept and made to arrive (glow opens in the middle, settles top-left; words
  rise), built and pushed. Then the owner on the "More conversations" strip: "I really like the previous
  design ... agency quality". All three now say bring the poster back (the grey calm look was their own
  over-reach): live Poppins type on the art, warmth, the lean with a soft light, arrows in the heading row, a
  thin progress line under the strip, a peeking swipe on the phone. They differ on colour: each guest's own
  art, darker at rest (F); one warm orange duotone (E); the face cut out on an ember ground (D). D adds a line
  per card true to its length and chapters; E a short scroll-held sideways pass. Flags: "Newest first" is
  not true of the 15 (D); "Enzo 3" breaks alone; the lead's pictures still grey. Waiting on the owner.
- 25 Oct (chat 13): the owner saw the flat call band built and said "i like the current one really".
  Asked why simpler, all three agreed: keep the current band (a lit panel like .kit-panel, the page's one warm
  spot where it asks for action; "no glow" was the podcast cards' rule, not the site's). Small fixes offered:
  the gap to the spacing scale (D 48px, E 24px), the words on the rows' left edge (D), the buttons centred on
  the title (F), the glow colour as a token (D), the phone's season line run down to the band (E).
- 25 Oct (chat 13): the owner said "ok" to building listen-b into the home page; built in place of #listen
  and #map by tools/v4_home_listen.py. Then asked all three about the step from the departures into the call
  band, "the only one which hasn't been updated as per the new site rules". All three agree: no box, no
  orange glow or fading orange line; the call becomes the last row on the departures grid (words under
  "Expedition", Book a Call and WhatsApp under Status, level with the title), one hairline above it, a
  token gap (--sp-3 or --sp-4); on a phone the orange season line runs past Peru to the call. They differ only
  on the hairline (plain, D; with the heads' short orange lead, F; Peru's own rule, E) and on whether the other
  four places follow. Waiting on the owner.
- 25 Oct (chat 12): option B's missing piece is scale (all three). The owner chose option 1, the lit trip
  leads as a large block, with two of the chat's ideas: play the episode in place with Trim's chapter line
  under it, and the globe answers the lead trip (turns to it, the route lit to it). Not the footage behind
  the lead trip ("Except 2, 1 & 3 are good concepts"). Globe-led option 2 (Cloudbase) not chosen.
- 25 Oct (chat 12): the podcast section after the departures: option B, Turnpoint's "Hear Where We Fly"
  ("i like option B"; A was Trim's "Told From Here"), #listen and #map merged, the rail opening with
  the trip places' episodes. The owner asked the three to refine it "keeping awwwards in mind".
  Preview: prototypes/v4/samples/listen-b/. The cursor shine on the departure rows: not added (all three said no).
- 25 Oct (chat 12): option A "One Line, Two Postures" is built into the v4 home page in place of
  the fly-by and table ("do what you can yourself"); on a phone the opening's headline and trip
  button sit on the first screen and the trip panel no longer fades.
- 24 Oct (chat 11): a fourth agent, the Juror, scores built previews blind on
  the Awwwards criteria; "use only after checking with me the prediction of
  time and turn expenses".
- 24 Oct (chat 11): the designers have names: D is Trim, E is Cloudbase, F is
  Turnpoint ("give these designers some cool names"; chosen by the chat).
- 24 Oct (chat 10): the move between places is E's, "through the cloud" (the
  owner saw three built versions: D "Contour Cut", the orange line bending
  round the land; E, the camera flies into cloud and out over the next place;
  F "Opens at the Turnpoint", a window rising from the next marker; and said
  "build E only"). The review-only photo switch is removed ("remove the photo
  changing option widget from the centre of the page"); Kenya opens on
  DSC_9492. A click on the progress line skips to the next place ("let the
  progress bar be clickable ... rather than waiting for long"). From Peru back
  to Kenya the season glider flies on forward (off the right end, in from the
  left), as designer F's notebook asked.
- 24 Oct: progress line toned down by a quarter; play/pause has no ring, is dim
  until hovered, and stands in a small gap at the line's end ("remove the
  round circle around the pause button ... even more subtle, only highlight it
  to the current brightness upon hover"; "a bit of a gap from the progress
  line"; "tone down the progress bar by 25%").
- 24 Oct: a play/pause button at the end of the progress line, "subtle yet
  elegant and sleek ... for those who want to stay on the image". Pause holds
  the place and its move still.
- 24 Oct: India in 2027: 15 to 24 Apr, 25 Apr to 4 May, 21 to 30 Oct, 3 to 12
  Nov. Panchgani a proper tour, 14 to 21 Feb 2027, on the season line.
- 24 Oct: Panchgani's motion: "a left circle with a very shallow angle while
  moving forward ... ensure this does not become nauseating". Built: 4% nearer,
  2.5% slide right, 1.6 degrees clockwise per 14 s pass; name and wing still.
- 24 Oct: Panchgani added as option A ("the designers' pick, which I chose"):
  wing at its real small size, the name at Kazakhstan's size across the flat top.
- 24 Oct: no restart in a loop: "the gliders abruptly switch positions ...
  instead move on the next slide ... make this as a progress bar ... make the
  line a bit sleek". Each place plays one forward pass, then the route moves on.
- 24 Oct (rejected after trying): the cloud restart of a looping move.
- 24 Oct: DSC_9492's follow shot, option A (D's and F's pick): "the gliders
  have to go away from the viewer ... slowly". E's option B (scroll drives it)
  not chosen. Shadow on the letters half as strong on scroll.
- 24 Oct: "forget it" to Kenyan wing liveries (do not raise).
- 23 Oct: round 3, D Final Cut, E Pull Back to the Route, F Fly the Season;
  F won. Round 2: C2 (C plus depth, shadow, light, footage in the letters).
  Round 1: A footage, B atlas chart, C the held moment; the owner liked C.
- Parked by the owner: the Encarta concept (do not raise).

## Open now
- 25 Oct (chat 13): the call band stays; the small fixes wait on the owner's yes.
- Nothing open in design. Chat 10 builds the opening (with E's cloud move) into
  the v4 home page.
