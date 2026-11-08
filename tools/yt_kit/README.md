# YouTube kit for comp highlights (chat 20, Tapalpa, 8 Nov 2026)

Owner: CapCut, 4K 60 fps; look = thumbnail style "A" (big italic TASK n, Mexican tricolour stripes) with a subtle
pine-green shade on the left (from style D). Event logo = SRS mark + Advance arch symbol + "ADVANCE EDITION" in the
kit's own type (Advance's wordmark is not available as a file; never redraw it).

- `plate.tpl`: one lower-third; set(p) fills name, flag, IOC, glider; rendered 3840x2160 transparent, one PNG per
  confirmed pilot (airtribune srs-2026-6/info embeds the pilot list as JSON; status "confirmed"; flags from
  airtribune /static/flags-svg/). Glider names are as each pilot typed them on airtribune (not corrected).
- `anim.tpl` + `make_anim.py N "8 Nov" "Mon 9 Nov"`: the opener (green-screen MP4 for CapCut's Chroma key, and a
  transparent PNG-codec MOV, ~470 MB for 4 s, too big to send) and the end card (animates in, holds 15 s).
  Web Animations with per-keyframe easing; the effect's own easing must stay linear (it compressed the timeline).
- Needs in the same folder: src/srs-w.png (prototypes/v4/img/media/logo-srs.png), src/advance-white.svg
  (cdn.advance.swiss .../Images/logo-white.svg), src/atlas.png (assets/logo/atlas-logo-white.png), src/flags/.
- Still to make each evening: task card, results boards (airtribune results), Google Earth KML (tracks), 2D replay,
  YouTube text, the thumbnail from the day's photo. Follow srs.live for the day's story (owner, 8 Nov).
- Templates are .tpl, not .html: the site's audit treats every .html in the repo as a page (8 Nov lesson).
- `board.tpl`: the results boards and winner cards (rows from SRS scores, api.airtribune.com/srs/scores/, the
  task's Sports, Female and Team tables). `make_kml.py t1 1 10`: the Google Earth file from SRS's task KMZ and IGC zip.
