#!/usr/bin/env python3
"""
The India page, option E: the flight over live 3D terrain, with the controls in the visitor's hands.

    prototypes/v4/destinations/india-e.html

Built from prototypes/v4/destinations/india-c.html (option C stays as it is).
The route section (#route) and the pinned gallery (#gallery) go; in their
place comes one section, #flight, "The flight":

  A pinned stage filled by the Dhauladhar as live 3D terrain (three.js,
  prototypes/v4/lib/, the heights and tint from open 19 m terrain data under
  prototypes/v4/img/india/dem/, the scene in tools/data/india-dem.json;
  the module is prototypes/v4/india-fly.js). The scroll flies the same path
  as option D: in high over the Kangra valley, down to Billing launch, west
  along the front to a close pass over Dharamshala, back east past Billing
  to 360, and a climb out with the back ranges behind. At any point the
  visitor can take the controls: drag moves the ground, wheel or pinch comes
  closer, a second button or a two-finger twist turns, all inside the range
  and the angles set in the data; scrolling on hands the camera back to the
  flight. Places with photographs carry a tappable marker that opens the
  pictures in a dialog. Nothing moves on its own. The four route cards' own
  words are the four chapters, one lit at a time at the foot of the stage,
  the readouts (width of view, the place under the camera, camera height)
  at the other side. The pilots' own Bir waypoints (tools/data/
  bir-waypoints.json, the XC League's BirIndia.cup) are pinned where the 3D
  camera puts them in every frame, so they sit on the ground in perspective.
  Nine of the owner's photographs rise as plates anchored to their waypoint
  as the camera passes, one at a time, the leader line drawn in a layer above
  everything so it can never hide. Frames load only once the section is
  within a screen and a half of view, never on arrival. Reduced motion and
  no JavaScript get a still of the Billing frame, the four chapters and the
  nine photographs, laid out plainly.

  The other four photographs sit in a quiet captioned row after it under the
  gallery's own heading. Every photograph is on the page once.

    python3 tools/v4_india_d.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "destinations", "india-c.html")
OUT = os.path.join(V4, "destinations", "india-e.html")
FLY = os.path.join(ROOT, "tools", "data", "india-fly.json")       # the plate windows and the still are read from the rendered path
DEM = os.path.join(ROOT, "tools", "data", "india-dem.json")
TRACKS = os.environ.get("V4_TRACKS") or os.path.join(ROOT, "tools", "data", "india-tracks.json")   # V4_TRACKS=... for a harness fixture
PHOTOS = os.path.join(ROOT, "tools", "data", "india-flight.json")   # titles, files, captions
WAYPOINTS = os.path.join(ROOT, "tools", "data", "bir-waypoints.json")
TOWNS = os.path.join(ROOT, "tools", "data", "india-towns.json")         # the towns named on the map (GeoNames)
LANDMARKS = os.path.join(ROOT, "tools", "data", "india-landmarks.json")   # the places with a story: a description and open-source photographs
LM_CREDITS = os.path.join(ROOT, "tools", "data", "india-landmarks-credits.json")   # written by tools/fetch_landmarks.py
LM_DIR = os.path.join(V4, "img", "india", "landmarks")

# the eight photographs on the stage, each anchored to a waypoint (code in bir-waypoints.json) and
# up between two frames (0-based) chosen from where the waypoint sits well inside the view (see
# card_windows for the check); "near" where the spot is read from the caption rather than a fix.
PLACED = [
    ("Bir landing", "A01", False, 2, 10),
    ("The valley floor", "B47", True, 12, 18),          # Baijnath
    ("Billing launch", "D01", False, 21, 29),
    ("Kangra valley", "B46", True, 33, 41),             # Palampur, on the run west
    ("The Dhauladhar", "B10", True, 74, 78),            # the big face, on the way home
    ("Over the peaks", "B07", True, 102, 106),          # Waldo peak, climbing out
    ("Meadows below the range", "B06", True, 108, 112),  # Thatwal Thati
    ("The back ranges", "B09", True, 114, 118),         # Mills peak
]
ROW = ["The landing field", "Tibetan monastery", "Hike and fly", "Last light", "Cloud on the range"]
# every photograph's place on the ground (waypoint code), for the markers and the dialog
PHOTO_AT = {"Kangra valley": "B46", "The Dhauladhar": "B10", "Billing launch": "D01", "Hike and fly": "D01", "Bir landing": "A01",
            "The landing field": "A01", "Last light": "A01", "Over the peaks": "B07", "Meadows below the range": "B06",
            "The valley floor": "B47", "Cloud on the range": "B11", "The back ranges": "B09", "Tibetan monastery": "B29"}
# the legs of the path -> the chapter (route card) lit while it runs
LEG_CHAPTER = [0, 1, 1, 2, 3]
# the places pinned, in priority order, with their label
PINS = [("D01", "Billing launch"), ("A01", "Bir landing"), ("B23", "Dharamsala"), ("B38", "360"), ("B22", "Triund"),
        ("B46", "Palampur"), ("B07", "Waldo peak"), ("B09", "Mills peak"), ("B10", "Big face"),
        ("T01", "Mandi"), ("T02", "Kangra"), ("T03", "Kullu"), ("T04", "Jogindernagar"), ("T05", "Manali"), ("T06", "Chamba"),
        ("B19", "Chamunda Devi temple"), ("B40", "Barot pass"), ("B36", "Mandi ridge"), ("B47", "Baijnath"), ("B29", "Chauntra monastery"), ("B06", "Thatwal Thati"),
        ("T07", "Bhuntar"), ("T08", "Nagrota Bagwan"), ("T09", "Sujanpur Tira"), ("T10", "Jawalamukhi"), ("T11", "Nadaun"), ("T12", "Naggar"),
        ("B02", "First ridge"), ("B01", "Billing upper ridge"), ("B30", "1st spur east"), ("B31", "2nd spur east"),
        ("B14", "Palampur ridge"), ("B11", "Top of big face"), ("B26", "DH cricket stadium"), ("B34", "Train station")]
PHONE_PINS = 6          # how many of the priority list a phone shows
CREDIT = ("The ground is open 19 m terrain data (AWS Terrain Tiles, Mapzen Terrarium, from SRTM and other open sources) "
          "drawn live as relief, flown by the scroll or moved by hand; the pins are the Bir waypoints pilots fly with "
          "(Indian XC League) and the towns are placed from GeoNames (CC BY 4.0). A photograph marked near is placed from its caption, not from a fix. The flights drawn are real "
          "tracklogs scored by the XContest rules: the distance is the scored route, the dashed line is that route, and the average "
          "speed is the scored distance over the time in the air.")
LM_CREDIT = " The landmark photographs are from Wikimedia Commons, each named with its author and licence where it appears."

CSS = r"""
/* v4 India option D, the flight over real terrain (tools/v4_india_d.py) */
.dst-sec.v4i-fl{padding:0;border-top:0;background:var(--bg)}
.v4i-fl *{box-sizing:border-box}
.v4i-fl-track{position:relative}
.v4i-fl-pin{position:relative;background:var(--bg)}
.v4i-fl-map{position:relative;overflow:hidden;background:var(--bg);isolation:isolate}
.v4i-fl-map>picture,.v4i-fl-map>picture img,.v4i-fl-canvas{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.v4i-fl-canvas{opacity:0;transition:opacity .6s var(--ease)}
.v4i-fl.is-ready .v4i-fl-canvas{opacity:1}
.v4i-fl-scrim{position:absolute;inset:0}
.v4i-fl-ov,.v4i-fl-lead{position:absolute;inset:0;width:100%;height:100%;display:block;overflow:visible;pointer-events:none}
.v4i-fl-ov text{font-family:var(--font-mono);font-size:12px;letter-spacing:.06em;fill:var(--white);paint-order:stroke;stroke:rgba(20,21,25,.9);stroke-width:3px;stroke-linejoin:round}
.v4i-fl-ov .v4i-fl-pl{transition:opacity .35s var(--ease)}
.v4i-fl-ov .v4i-fl-pl circle{fill:var(--white)}
.v4i-fl-ov .v4i-fl-pl.is-far text{fill:var(--gray-light)}
.v4i-fl-ov .v4i-fl-pl.is-far circle{opacity:.55}
.v4i-fl-ov .v4i-fl-pl text.is-l{text-anchor:end}
.v4i-fl-ov .v4i-fl-pl.is-town rect{fill:var(--white);opacity:.85}
.v4i-fl-ov .v4i-fl-pl.is-country text{font-size:12px;letter-spacing:.42em;fill:var(--gray);stroke:none;opacity:.8}
.v4i-fl-ov .v4i-fl-pl.is-story path{fill:var(--white);opacity:.9}.v4i-fl-ov .v4i-fl-pl.is-story .is-hollow{fill:none;stroke:var(--white);stroke-width:1.2}
.v4i-fl-ov .v4i-fl-pl.is-story.is-far path,.v4i-fl-ov .v4i-fl-pl.is-story.is-far .is-hollow{opacity:.55}
.v4i-fl-dg .v4i-fl-dk{grid-column:1/-1;margin:0 0 -.4rem;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;color:var(--orange)}
.v4i-fl-ov .v4i-fl-pl.is-town text{font-size:11px;letter-spacing:.14em;text-transform:uppercase;fill:var(--gray-light)}
.v4i-fl-ov .v4i-fl-pl.is-town.is-far text{fill:var(--gray)}.v4i-fl-ov .v4i-fl-pl.is-town.is-far rect{opacity:.5}
.v4i-fl-lead .v4i-fl-tie{stroke:var(--orange);stroke-width:1.25;opacity:0}
.v4i-fl-lead .v4i-fl-dot{fill:var(--orange);opacity:0}
.v4i-fl-lead .v4i-fl-halo{fill:none;stroke:var(--orange);stroke-width:1;opacity:0}
.v4i-fl-lead .v4i-fl-halo.is-near{fill:var(--orange);stroke:none}
.v4i-fl-head{position:relative;z-index:2;max-width:38rem}
.v4i-fl-head .kicker{display:flex;align-items:center;gap:.6rem;margin:0}
.v4i-fl-head h2{margin:.5rem 0 .6rem;color:var(--white);font-size:var(--fs-h2);text-wrap:balance}
.v4i-fl-head p{margin:0;color:var(--gray-light);font-size:var(--fs-body);max-width:31rem}
.v4i-fl-read{font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);letter-spacing:.04em;font-variant-numeric:tabular-nums;display:grid;gap:.35rem;text-align:right}
.v4i-fl-read b{font-weight:400;color:var(--white);font-size:1.6rem;letter-spacing:0;margin-right:.35rem;line-height:1}
.v4i-fl-read .v4i-fl-at i{font-style:normal;color:var(--gray)}
.v4i-fl-read .v4i-fl-alt{color:var(--gray)}
.v4i-fl-ch{list-style:none;margin:0;padding:0;display:grid;gap:var(--sp-3)}
.v4i-fl-c{position:relative;padding-left:1.1rem;opacity:.42;transition:opacity .5s var(--ease)}
.v4i-fl-c::before{content:"";position:absolute;left:0;top:.35rem;bottom:.2rem;width:2px;background:var(--line);transition:background .5s var(--ease)}
.v4i-fl-c.is-on{opacity:1}
.v4i-fl-c.is-on::before{background:var(--orange)}
.v4i-fl-c h3{margin:.25rem 0 .2rem;font-size:var(--fs-h4);color:var(--white)}
.v4i-fl-c p{margin:.3rem 0 0;color:var(--gray-light);font-size:var(--fs-body-s)}
.v4i-fl-c p a{color:var(--white)}
.v4i-fl-c .tm-leg{margin-top:.5rem}
.v4i-fl-cards{display:grid;gap:var(--sp-3)}
.v4i-fl-card{margin:0;width:100%;background:var(--card);box-shadow:0 24px 60px rgba(0,0,0,.55)}
.v4i-fl-card picture,.v4i-fl-card img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover}
.v4i-fl-card figcaption{padding:.75rem .9rem .9rem;font-size:var(--fs-small);color:var(--gray-light);line-height:1.4}
.v4i-fl-card figcaption b{display:block;font-family:var(--font-display);font-weight:600;color:var(--white);font-size:var(--fs-body-s);margin-bottom:.15rem}
.v4i-fl-card .v4i-fl-where{display:block;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--orange);margin-top:.45rem}
.v4i-fl-skip{display:inline-flex;align-items:center;gap:.4rem;color:var(--gray);font-size:var(--fs-small);text-decoration:none;letter-spacing:.04em}
.v4i-fl-skip:hover,.v4i-fl-skip:focus-visible{color:var(--white)}
.v4i-fl-cred{margin:var(--sp-3) var(--edge-x) 0;max-width:46rem;color:var(--gray);font-size:var(--fs-small);line-height:1.5}
/* the still page: no script, or reduced motion */
.v4i-fl:not(.is-live) .v4i-fl-pin{padding:var(--sp-section) var(--edge-x) 0;display:grid;gap:var(--sp-4)}
.v4i-fl:not(.is-live) .v4i-fl-map{aspect-ratio:16/9;max-height:70vh;order:2}
.v4i-fl:not(.is-live) .v4i-fl-head{order:1}
.v4i-fl:not(.is-live) .v4i-fl-read,.v4i-fl:not(.is-live) .v4i-fl-skip,.v4i-fl:not(.is-live) .v4i-fl-ov,.v4i-fl:not(.is-live) .v4i-fl-lead{display:none}
.v4i-fl:not(.is-live) .v4i-fl-ch{order:3;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-4)}
.v4i-fl:not(.is-live) .v4i-fl-c{opacity:1}
.v4i-fl:not(.is-live) .v4i-fl-cards{order:5;grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:1024px){.v4i-fl:not(.is-live) .v4i-fl-ch{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:700px){.v4i-fl:not(.is-live) .v4i-fl-ch,.v4i-fl:not(.is-live) .v4i-fl-cards{grid-template-columns:minmax(0,1fr)}}
/* the live page: pinned, flown by the scroll */
.v4i-fl.is-live .v4i-fl-track{height:900vh}
.v4i-fl.is-live .v4i-fl-pin{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;will-change:transform;transform:translateZ(0)}
.v4i-fl.is-live .v4i-fl-map{position:absolute;inset:0}
.v4i-fl.is-live .v4i-fl-scrim{background:linear-gradient(180deg,rgba(20,21,25,.72) 0,rgba(20,21,25,.12) 22%,rgba(20,21,25,0) 45%,rgba(20,21,25,.1) 68%,rgba(20,21,25,.86) 100%)}
.v4i-fl.is-live .v4i-fl-head{position:absolute;left:var(--gutter);top:clamp(5.4rem,10vh,6.4rem);right:auto;max-width:34rem;pointer-events:none}
.v4i-fl.is-live .v4i-fl-head h2{font-size:var(--fs-h3)}
.v4i-fl.is-live .v4i-fl-head p{font-size:var(--fs-body-s);max-width:28rem}
.v4i-fl.is-live .v4i-fl-ch{position:absolute;left:var(--gutter);bottom:clamp(2.6rem,6vh,3.6rem);width:min(30rem,44vw);z-index:3;display:block}
.v4i-fl.is-live .v4i-fl-c{position:absolute;left:0;bottom:0;width:100%;opacity:0;transition:opacity .5s var(--ease)}
.v4i-fl.is-live .v4i-fl-c.is-on{opacity:1}
.v4i-fl.is-live .v4i-fl-c p:not(.tm-leg){max-width:28rem}
.v4i-fl.is-live .v4i-fl-read{position:absolute;right:var(--gutter);bottom:clamp(2.6rem,6vh,3.6rem);z-index:3}
.v4i-fl.is-live .v4i-fl-cards{position:absolute;inset:0;display:block;pointer-events:none;z-index:2}
.v4i-fl.is-live .v4i-fl-card{position:absolute;left:0;top:0;width:19rem;opacity:0;transform:translate3d(var(--x,0px),calc(var(--y,0px) + (1 - var(--w,0)) * 22px),0);opacity:var(--w,0);will-change:transform,opacity}
.v4i-fl.is-live .v4i-fl-lead{z-index:4}
.v4i-fl.is-live .v4i-fl-skip{position:absolute;right:var(--gutter);top:clamp(5.6rem,10vh,6.6rem);z-index:3}
.v4i-fl.is-live .v4i-fl-cred{margin-top:var(--sp-4)}
@media (max-width:700px){
.v4i-fl.is-live .v4i-fl-track{height:700vh}
.v4i-fl.is-live .v4i-fl-map{inset:0;height:auto}
.v4i-fl.is-live .v4i-fl-scrim{background:linear-gradient(180deg,rgba(20,21,25,.86) 0,rgba(20,21,25,.3) 22%,rgba(20,21,25,0) 40%,rgba(20,21,25,0) 58%,rgba(20,21,25,.55) 74%,rgba(20,21,25,.92) 100%)}
.v4i-fl.is-live .v4i-fl-head{top:4.3rem;left:var(--gutter);right:var(--gutter);max-width:calc(100% - 2 * var(--gutter));padding-right:8.4rem}
.v4i-fl.is-live .v4i-fl-head h2{font-size:1.05rem;margin:.3rem 0 0;line-height:1.25}
.v4i-fl.is-live .v4i-fl-head p{display:none}
.v4i-fl.is-live .v4i-fl-ch{top:auto;right:var(--gutter);left:var(--gutter);width:auto;bottom:8.9rem}
.v4i-fl.is-live .v4i-fl-c{padding-left:.9rem}
.v4i-fl.is-live .v4i-fl-c h3{font-size:1.05rem;margin:.2rem 0 0}
.v4i-fl.is-live .v4i-fl-c p:not(.tm-leg){display:none}
.v4i-fl.is-live .v4i-fl-c .tm-leg{margin-top:.25rem}
.v4i-fl.is-live .v4i-fl-read{bottom:5.4rem;left:var(--gutter);right:var(--gutter);font-size:var(--fs-micro);display:flex;gap:1.1rem;text-align:left;align-items:baseline}
.v4i-fl.is-live .v4i-fl-read b{font-size:1.15rem}
.v4i-fl.is-live .v4i-fl-read .v4i-fl-alt{display:none}
.v4i-fl.is-live .v4i-fl-card{width:min(14rem,54vw)}
.v4i-fl.is-live .v4i-fl-card figcaption{padding:.5rem .65rem .6rem;font-size:var(--fs-micro)}
.v4i-fl.is-live .v4i-fl-skip{display:none}
}
/* the controls, the markers and the dialog */
.v4i-fl-ctl{position:absolute;z-index:5;right:var(--gutter);top:clamp(5.6rem,10vh,6.6rem);font:600 var(--fs-small)/1 var(--font-display);color:var(--white);background:rgba(20,21,25,.72);border:1px solid rgba(246,244,244,.28);border-radius:999px;padding:.6rem 1rem;cursor:pointer;letter-spacing:.02em;backdrop-filter:blur(6px)}
.v4i-fl-ctl:hover,.v4i-fl-ctl:focus-visible{border-color:var(--orange);color:var(--white)}
.v4i-fl.is-free .v4i-fl-ctl{background:var(--orange);color:var(--bg);border-color:var(--orange)}
.v4i-fl-hint{position:absolute;z-index:5;left:50%;transform:translateX(-50%);bottom:clamp(2.6rem,6vh,3.6rem);font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray-light);background:rgba(20,21,25,.7);border-radius:999px;padding:.45rem .9rem;opacity:0;transition:opacity .4s var(--ease);pointer-events:none;white-space:nowrap}
.v4i-fl.is-free .v4i-fl-hint{opacity:1}
.v4i-fl.is-live .v4i-fl-map{cursor:grab}
.v4i-fl.is-free .v4i-fl-map{touch-action:none;cursor:grabbing}
.v4i-fl.is-free .v4i-fl-skip{display:none}
.v4i-fl-btns{position:absolute;z-index:5;right:var(--gutter);top:50%;transform:translateY(-50%);display:grid;gap:.35rem;opacity:0;pointer-events:none;transition:opacity .35s var(--ease)}
.v4i-fl.is-free .v4i-fl-btns{opacity:1;pointer-events:auto}
.v4i-fl-btn{width:2.5rem;height:2.5rem;border-radius:50%;border:1px solid rgba(246,244,244,.28);background:rgba(20,21,25,.72);color:var(--white);font:600 1rem/1 var(--font-display);cursor:pointer;display:grid;place-items:center;backdrop-filter:blur(6px);padding:0}
.v4i-fl-btn:hover,.v4i-fl-btn:focus-visible{border-color:var(--orange);outline:none}
.v4i-fl-btn svg{width:1rem;height:1rem;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.v4i-fl-tks{position:absolute;z-index:5;left:var(--gutter);top:clamp(9.6rem,19vh,11.6rem);display:flex;flex-wrap:wrap;gap:.4rem;max-width:min(34rem,60vw)}
.v4i-fl-tks[hidden]{display:none}
.v4i-fl-tks .kicker{width:100%;margin:0 0 .1rem}
.v4i-fl-tk{font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.05em;color:var(--white);background:rgba(20,21,25,.72);border:1px solid rgba(246,244,244,.28);border-radius:999px;padding:.45rem .8rem;cursor:pointer;backdrop-filter:blur(6px)}
.v4i-fl-tk b{font-weight:400;color:var(--orange);margin-left:.45rem}
.v4i-fl-tk:hover,.v4i-fl-tk:focus-visible,.v4i-fl-tk.is-on{border-color:var(--orange);outline:none}
.v4i-fl-tk.is-on{background:var(--orange);color:var(--bg)}.v4i-fl-tk.is-on b{color:var(--bg)}
.v4i-fl-tp{position:absolute;left:0;top:0;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:var(--orange);box-shadow:0 0 0 4px rgba(255,117,23,.25);pointer-events:none}
.v4i-fl-tp[hidden]{display:none}
.v4i-fl-tcard{position:absolute;z-index:5;left:var(--gutter);bottom:clamp(2.6rem,6vh,3.6rem);width:min(25rem,calc(100% - 2 * var(--gutter)));background:var(--card);border-radius:4px;box-shadow:0 24px 60px rgba(0,0,0,.55);padding:1rem 1.1rem 1.1rem}
.v4i-fl-tcard[hidden]{display:none}
.v4i-fl-tcard .v4i-fl-th{display:block;padding-right:4.4rem}
.v4i-fl-tcard .v4i-fl-tn{font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);color:var(--white)}
.v4i-fl-tcard .v4i-fl-td{display:block;margin-top:.25rem;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray)}
.v4i-fl-tcard .v4i-fl-tg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.6rem;margin-top:.7rem}
.v4i-fl-tcard .v4i-fl-tkm{grid-column:1/-1;display:flex;align-items:baseline;gap:.6rem;flex-wrap:wrap;padding-bottom:.2rem;border-bottom:1px solid var(--line);margin-bottom:.2rem}
.v4i-fl-tcard .v4i-fl-tkm b{font-size:2.1rem;margin:0}.v4i-fl-tcard .v4i-fl-tkm span{color:var(--orange);font-size:var(--fs-small);letter-spacing:.04em}
.v4i-fl-tcard .v4i-fl-tnote{margin:.7rem 0 0;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray);line-height:1.5}
.v4i-fl-tcard .v4i-fl-tg span{display:block;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray-light)}
.v4i-fl-tcard .v4i-fl-tg b{display:block;font-weight:400;font-size:1.35rem;color:var(--white);font-variant-numeric:tabular-nums;line-height:1.1;margin-bottom:.2rem}
.v4i-fl-tcard .v4i-fl-tx{position:absolute;right:.6rem;top:.55rem;font:600 var(--fs-micro)/1 var(--font-display);color:var(--gray-light);background:none;border:1px solid var(--line);border-radius:999px;padding:.35rem .6rem;cursor:pointer}
.v4i-fl.is-free .v4i-fl-ch,.v4i-fl.is-free .v4i-fl-c{opacity:0;pointer-events:none;transition:opacity .3s var(--ease)}
.v4i-fl.is-free .v4i-fl-head p{display:none}
.v4i-fl.is-free .v4i-fl-hint{bottom:auto;top:clamp(5.6rem,10vh,6.6rem);left:auto;right:calc(var(--gutter) + 11.5rem);transform:none;white-space:normal;text-align:right;max-width:min(44rem,calc(100% - 2 * var(--gutter) - 38rem));line-height:1.6}
.v4i-fl-mks{position:absolute;inset:0;pointer-events:none;z-index:3}
.v4i-fl-mk{position:absolute;left:0;top:0;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;border:1.5px solid var(--orange);background:rgba(20,21,25,.55);pointer-events:auto;cursor:pointer;padding:0;display:grid;place-items:center;transition:background .25s var(--ease)}
.v4i-fl-mk::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--orange);box-shadow:0 0 0 3px rgba(255,117,23,.25)}
.v4i-fl-mk:hover,.v4i-fl-mk:focus-visible{background:rgba(255,117,23,.28);outline:none}
.v4i-fl-mk[hidden]{display:none}
/* a landmark: no ring, a dotted line under its name, the name itself the button */
.v4i-fl-ov .v4i-fl-ul{stroke:var(--gray-light);stroke-width:1;stroke-dasharray:1 3;stroke-linecap:round;opacity:.75}
.v4i-fl-ov .v4i-fl-pl.is-far .v4i-fl-ul{opacity:.45}
.v4i-fl-ov .v4i-fl-pl.is-hot text{fill:var(--orange)}.v4i-fl-ov .v4i-fl-pl.is-hot .v4i-fl-ul{stroke:var(--orange);stroke-dasharray:none;opacity:1}
.v4i-fl-lm{position:absolute;left:0;top:0;height:26px;margin-top:-13px;background:none;border:0;padding:0;border-radius:3px;pointer-events:auto;cursor:pointer}
.v4i-fl-lm:focus-visible{outline:1px solid var(--orange);outline-offset:1px}
.v4i-fl-lm[hidden]{display:none}
.v4i-fl:not(.is-live) .v4i-fl-ctl,.v4i-fl:not(.is-live) .v4i-fl-mks,.v4i-fl:not(.is-live) .v4i-fl-hint{display:none}
.v4i-fl-dlg{border:0;padding:0;margin:auto;background:var(--card);color:var(--white);max-width:min(56rem,calc(100vw - 2rem));width:auto;min-width:min(26rem,calc(100vw - 2rem));border-radius:4px;box-shadow:0 30px 80px rgba(0,0,0,.6)}
.v4i-fl-dlg.is-text{max-width:min(36rem,calc(100vw - 2rem))}
.v4i-fl-dlg::backdrop{background:rgba(20,21,25,.86)}
.v4i-fl-dh{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.25rem .6rem}
.v4i-fl-dh .kicker{margin:0}
.v4i-fl-dx{font:600 var(--fs-small)/1 var(--font-display);color:var(--gray-light);background:none;border:1px solid var(--line);border-radius:999px;padding:.5rem .9rem;cursor:pointer}
.v4i-fl-dx:hover,.v4i-fl-dx:focus-visible{color:var(--white);border-color:var(--orange)}
.v4i-fl-dg{display:grid;gap:1rem;padding:0 1.25rem 1.25rem;max-height:min(78vh,60rem);overflow:auto}
.v4i-fl-dg[hidden]{display:none}
.v4i-fl-dg figure{margin:0}
.v4i-fl-dg picture{display:block}.v4i-fl-dg img{display:block;width:auto;max-width:100%;height:auto;max-height:min(62vh,46rem);margin:0 auto}
.v4i-fl-dg figcaption{padding:.6rem 0 0;font-size:var(--fs-small);color:var(--gray-light);line-height:1.4}
.v4i-fl-dg figcaption b{display:block;font-family:var(--font-display);font-weight:600;color:var(--white);font-size:var(--fs-body-s);margin-bottom:.1rem}
.v4i-fl-dg.is-two{grid-template-columns:repeat(2,minmax(0,1fr))}
.v4i-fl-dg.is-two figure img{width:100%;max-height:none;aspect-ratio:3/2;object-fit:cover}
.v4i-fl-dg .v4i-fl-dp{grid-column:1/-1;margin:0;max-width:64ch;font-size:var(--fs-body-s);color:var(--gray-light);line-height:1.6}
.v4i-fl-dg .v4i-fl-dc{grid-column:1/-1;margin:-.4rem 0 0;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray);line-height:1.5}
.v4i-fl-dg figure img{cursor:zoom-in}
.v4i-fl.is-live .v4i-fl-card.is-on picture{pointer-events:auto;cursor:zoom-in}
.v4i-fl-row-g figure img{cursor:zoom-in}
@media (max-width:700px){.v4i-fl-dg.is-two{grid-template-columns:minmax(0,1fr)}}
/* a photograph, enlarged: floating on a dimmed page, zoom by wheel or pinch, drag to move, click outside or the cross to close */
.v4i-fl-lb{border:0;padding:0;margin:0;max-width:none;max-height:none;width:100vw;height:100vh;background:transparent;overflow:hidden;opacity:0;transition:opacity .22s var(--ease)}
.v4i-fl-lb.is-in{opacity:1}
.v4i-fl-lb::backdrop{background:rgba(20,21,25,.9);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
.v4i-fl-lbs{position:absolute;inset:0;display:grid;place-items:center;touch-action:none}
.v4i-fl-lb img{max-width:min(92vw,1800px);max-height:86vh;width:auto;height:auto;display:block;box-shadow:0 40px 120px rgba(0,0,0,.7);border-radius:3px;cursor:zoom-in;transform-origin:center center;transition:transform .18s var(--ease),opacity .22s var(--ease);user-select:none;-webkit-user-drag:none;transform:scale(.96)}
.v4i-fl-lb.is-in img{transform:none}
.v4i-fl-lb.is-zoomed img{cursor:grab}.v4i-fl-lb.is-drag img{cursor:grabbing;transition:opacity .22s var(--ease)}
.v4i-fl-lbx{position:absolute;top:1rem;right:1rem;width:2.6rem;height:2.6rem;border-radius:50%;border:1px solid rgba(246,244,244,.3);background:rgba(20,21,25,.5);cursor:pointer;z-index:2;padding:0;transition:border-color .2s var(--ease),transform .2s var(--ease)}
.v4i-fl-lbx::before,.v4i-fl-lbx::after{content:"";position:absolute;left:50%;top:50%;width:14px;height:1px;margin:0 0 0 -7px;background:var(--white);transform:rotate(45deg)}.v4i-fl-lbx::after{transform:rotate(-45deg)}
.v4i-fl-lbx:hover,.v4i-fl-lbx:focus-visible{border-color:var(--orange);outline:none;transform:rotate(90deg)}
.v4i-fl-lbc{position:absolute;left:1.25rem;bottom:1.1rem;max-width:50vw;display:flex;align-items:baseline;gap:.8rem;font-family:var(--font-display);font-weight:600;font-size:var(--fs-small);color:var(--white);pointer-events:none}
.v4i-fl-lbc .v4i-fl-lbi{font-family:var(--font-mono);font-weight:400;font-size:var(--fs-micro);letter-spacing:.08em;color:var(--gray)}
.v4i-fl-lbn{position:absolute;top:50%;transform:translateY(-50%);width:2.8rem;height:2.8rem;border-radius:50%;border:1px solid rgba(246,244,244,.3);background:rgba(20,21,25,.5);color:var(--white);cursor:pointer;z-index:2;display:grid;place-items:center;padding:0;transition:border-color .2s var(--ease),background .2s var(--ease)}
.v4i-fl-lbn svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.v4i-fl-lbn:hover,.v4i-fl-lbn:focus-visible{border-color:var(--orange);background:rgba(255,117,23,.18);outline:none}
.v4i-fl-lbn[hidden]{display:none}.v4i-fl-lbp{left:1rem}.v4i-fl-lbnx{right:1rem}
.v4i-fl-lbh{position:absolute;right:1.25rem;bottom:1.2rem;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray);white-space:nowrap;pointer-events:none}
@media (max-width:700px){.v4i-fl-lbh{display:none}.v4i-fl-lb img{max-width:100vw;max-height:78vh;border-radius:0}.v4i-fl-lbc{bottom:1rem;max-width:calc(100vw - 2.5rem)}.v4i-fl-lbn{width:2.4rem;height:2.4rem;top:auto;bottom:4rem;transform:none}.v4i-fl-lbp{left:auto;right:4.2rem}.v4i-fl-lbnx{right:1rem}}
.v4i-fl-ov .v4i-fl-an use{transition:opacity .3s var(--ease)}
.v4i-fl-ov .v4i-fl-an.is-hot use{filter:drop-shadow(0 0 2px rgba(255,117,23,.95)) drop-shadow(0 0 6px rgba(255,117,23,.6))}
.v4i-fl-ab{position:absolute;left:0;top:0;width:30px;height:30px;margin:-15px 0 0 -15px;background:none;border:0;padding:0;border-radius:50%;pointer-events:auto;cursor:pointer}
.v4i-fl-ab:focus-visible{outline:1px solid var(--orange);outline-offset:2px}
.v4i-fl-ab[hidden]{display:none}
.v4i-fl .v4i-fl-map.is-hand,.v4i-fl.is-free .v4i-fl-map.is-hand{cursor:pointer}
.v4i-fl.is-tracked .v4i-fl-ab{opacity:0;pointer-events:none}
.v4i-fl-dg .v4i-fl-dl{grid-column:1/-1;margin:.3rem 0 0;max-width:64ch;padding-top:.9rem;border-top:1px solid rgba(255,255,255,.08);font-size:var(--fs-body-s);color:var(--gray-light);line-height:1.6}
.v4i-fl-dg .v4i-fl-dl b{display:flex;align-items:center;gap:.45rem;margin:0 0 .35rem;font-family:var(--font-mono);font-weight:400;font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;color:var(--white)}
.v4i-fl-dg .v4i-fl-dl b svg{width:1.3rem;height:1.3rem;flex:none}
@media (prefers-reduced-motion:reduce){.v4i-fl-ov .v4i-fl-an use{transition:none}}
@media (prefers-reduced-motion:reduce){.v4i-fl-lb,.v4i-fl-lb img,.v4i-fl-lbx{transition:none}}
.v4i-fl-hint .is-short{display:none}
@media (max-width:700px){.v4i-fl-ctl{top:4.6rem;right:var(--gutter);padding:.55rem .8rem;font-size:var(--fs-micro)}.v4i-fl-hint{bottom:13.6rem;left:var(--gutter);right:var(--gutter);transform:none;white-space:normal;text-align:center;font-size:10px;line-height:1.5}.v4i-fl.is-free .v4i-fl-hint{top:auto;bottom:13.6rem;left:var(--gutter);transform:none}.v4i-fl-hint .is-long{display:none}.v4i-fl-hint .is-short{display:inline}.v4i-fl-mk{width:34px;height:34px;margin:-17px 0 0 -17px}
.v4i-fl-btns{right:.5rem;top:46%;transform:translateY(-50%);grid-template-columns:repeat(2,1fr)}.v4i-fl-btn{width:2.2rem;height:2.2rem}
.v4i-fl-tks{top:9.8rem;left:var(--gutter);right:3.2rem;max-width:none}
.v4i-fl.is-free .v4i-fl-hint{top:auto;bottom:auto;left:var(--gutter);right:3.2rem;transform:none;display:none}
.v4i-fl-tcard{bottom:5.2rem;width:calc(100% - 2 * var(--gutter));padding:.8rem .9rem .9rem}.v4i-fl-tcard .v4i-fl-tg{gap:.45rem}.v4i-fl-tcard .v4i-fl-tg b{font-size:1.1rem}.v4i-fl-tcard .v4i-fl-tkm b{font-size:1.7rem}.v4i-fl-tcard .v4i-fl-tg span{font-size:9px;letter-spacing:.04em}.v4i-fl-tcard .v4i-fl-td{display:none}.v4i-fl-lm{height:32px;margin-top:-16px}}
/* a flight chosen: the ground, the line and its figures, nothing else; the figures as a strip along the bottom */
.v4i-fl.is-tracked .v4i-fl-head,.v4i-fl.is-tracked .v4i-fl-tks,.v4i-fl.is-tracked .v4i-fl-btns,.v4i-fl.is-tracked .v4i-fl-hint,.v4i-fl.is-tracked .v4i-fl-read,.v4i-fl.is-tracked .v4i-fl-ov,.v4i-fl.is-tracked .v4i-fl-ctl,.v4i-fl.is-tracked .v4i-fl-mk,.v4i-fl.is-tracked .v4i-fl-lm,.v4i-fl.is-tracked .v4i-fl-skip,.v4i-fl.is-tracked .v4i-fl-lead{opacity:0;pointer-events:none;transition:opacity .35s var(--ease)}
.v4i-fl.is-tracked .v4i-fl-tp:not(.is-on){display:none}
.v4i-fl.is-tracked .v4i-fl-tcard{left:0;right:0;bottom:0;width:auto;max-width:none;background:linear-gradient(to top,rgba(20,21,25,.94) 55%,rgba(20,21,25,0));box-shadow:none;border-radius:0;padding:2.4rem var(--gutter) 1.2rem;display:flex;align-items:baseline;gap:1.4rem 2rem;flex-wrap:wrap}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-th{display:flex;align-items:baseline;gap:.8rem;padding:0}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-td{display:inline;margin:0}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tg{display:flex;flex-wrap:wrap;gap:.6rem 1.8rem;margin:0}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tg > div{display:flex;align-items:baseline;gap:.45rem}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tkm{border:0;padding:0;margin:0}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tg b,.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tkm b{font-size:1.3rem;margin:0;line-height:1}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tg span{display:inline;white-space:nowrap}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tnote{flex-basis:100%;margin:0;opacity:.8;order:5}
.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tx{position:static;margin-left:auto;align-self:center;order:4}
@media (max-width:700px){.v4i-fl.is-tracked .v4i-fl-tcard{bottom:4.9rem;padding:1.6rem var(--gutter) .6rem;gap:.7rem 1.2rem}.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tg{gap:.5rem 1.1rem}.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tg b,.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tkm b{font-size:1.1rem}.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-td{display:inline}.v4i-fl.is-tracked .v4i-fl-tcard .v4i-fl-tnote{display:none}}
/* the quiet row after it */
.dst-sec.v4i-fl-row{padding-top:var(--sp-section);padding-bottom:var(--sp-section)}
.v4i-fl-row .dst-head{margin-bottom:var(--sp-4)}
.v4i-fl-row .dst-head .kicker{display:flex;align-items:center;gap:.6rem}
.v4i-fl-row-g{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:var(--sp-3)}
.v4i-fl-row-g figure{margin:0}
.v4i-fl-row-g picture,.v4i-fl-row-g img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover}
.v4i-fl-row-g figcaption{padding:.6rem 0 0;font-size:var(--fs-small);color:var(--gray);line-height:1.4}
.v4i-fl-row-g figcaption b{display:block;font-family:var(--font-display);font-weight:600;color:var(--white);font-size:var(--fs-body-s);margin-bottom:.1rem}
@media (max-width:1024px){.v4i-fl-row-g{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:700px){.v4i-fl-row-g{gap:var(--sp-2)}.v4i-fl-row-g figcaption{font-size:var(--fs-micro)}}
"""

SCRIPT = '<script type="module" src="../fly.js"></script>'


def th(v):
    return int(round(v * 1000))


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def card_windows(F, n, pins_by_code):
    """The plates' windows from PLACED, checked: the waypoint sits well inside the view and within
    38 km for every frame of the window, and the windows never overlap."""
    out, end = [], -2
    for nm, code, near, a, b in PLACED:
        label = pins_by_code[code]
        for i in range(a, b + 1):
            p = F[i]["places"][label]
            assert p[2] and 0.08 < p[0] < 0.92 and 0.14 < p[1] < 0.84 and p[3] < 38000, (nm, i, p)
        assert a > end + 1, nm
        out.append({"n": nm, "p": label, "a": a, "b": b, "near": near})
        end = b
    return out


def build():
    t = open(SRC, encoding="utf-8").read()
    fly = json.load(open(FLY))
    dem = json.load(open(DEM))
    tracks = json.load(open(TRACKS))["tracks"]
    pd = json.load(open(PHOTOS))
    wp = {p["code"]: p for p in json.load(open(WAYPOINTS))["points"]}
    towns = json.load(open(TOWNS))["towns"]
    wp.update({code: dict(code=code, name=tw["label"], lat=tw["lat"], lon=tw["lon"], elev=tw["elev"]) for code, tw in towns.items()})
    LM = json.load(open(LANDMARKS))["places"]
    lm_credits = json.load(open(LM_CREDITS)) if os.path.exists(LM_CREDITS) else {}
    assert all(code in dict(PINS) for code in LM), "every landmark is a pin"
    n0 = len(t)
    F = fly["frames"]
    n = len(F)
    photos = {p["title"]: p for p in pd["photos"]}
    pins_by_code = dict(PINS)
    assert all(code in wp for code, _ in PINS)
    # frames.json keys places by the label used in the render; three differ from the pin labels
    render_name = {"360": "360 (Xaviers)", "Waldo peak": "Waldo peak 3,470 m", "Mills peak": "Mills peak 4,140 m"}
    for fr in F:
        fr["places"] = {label: fr["places"].get(render_name.get(label, label), [0, 0, 0, 0]) for _, label in PINS}

    # the pieces of the page we keep the words of
    m = re.search(r'<section class="dst-sec tm-calm" id="route".*?</section>\n', t, re.S)
    assert m, "route section"
    route = m.group(0)
    cards = re.findall(r'<article class="tm-card" data-i="\d"><div class="tm-card-t">(.*?)</div></article>', route, re.S)
    assert len(cards) == 4, cards
    h2 = re.search(r'<h2 id="route-h">(.*?)</h2>', route).group(1)
    t = t[:m.start()] + "@@FLIGHT@@" + t[m.end():]
    m = re.search(r'<!--v4c:gallery--><section class="dst-sec v4c-g" id="gallery".*?</section><!--/v4c:gallery-->\n', t, re.S)
    assert m, "gallery section"
    gallery = m.group(0)
    figs = {}
    for pic, cap in re.findall(r'<figure class="v4c-g-f"[^>]*>(<picture>.*?</picture>)<figcaption>.*?<b>(.*?)</b>', gallery, re.S):
        figs[cap] = pic
    assert len(figs) == 13, len(figs)
    gh2 = re.search(r'<h2 id="gallery-h">(.*?)</h2>', gallery).group(1)
    t = t[:m.start()] + t[m.end():]

    # the data the script flies: per place, x and y in thousandths and distance in km, every frame
    places = {}
    for _, label in PINS:
        arr = []
        for fr in F:
            x, y, vis, dist = fr["places"][label]
            if vis and -0.2 < x < 1.2 and -0.2 < y < 1.2:
                arr += [th(x), th(y), int(round(dist / 1000))]
            else:
                arr += [-1, -1, 0]
        places[label] = arr
    card_data = card_windows(F, n, pins_by_code)
    chapter = [LEG_CHAPTER[fr["leg"]] for fr in F]
    for cd in card_data:
        cd["c"] = [code for code, label in PINS if label == cd["p"]][0]
    data = {"grid": dem["grid"], "textures": dem["textures"], "keys": dem["keys"], "per_leg": dem["per_leg"], "bounds": dem["bounds"],
            "light": dem["light"], "waypoints": dem["waypoints"], "chapter": LEG_CHAPTER, "cards": card_data, "farKm": 42, "phonePins": PHONE_PINS, "edge_fade": 0.04,
            "tracks": [{"name": t["name"], "date": t["date"], "distance_km": t["distance_km"], "duration_min": t["duration_min"], "avg_kmh": t["avg_kmh"],
                        "max_alt_m": t["max_alt_m"], "type": t["type"], "closed": t["closed"], "points": t["points"], "ground_km": t["ground_km"],
                        "off_map": t["off_map"], "route": t["route"], "segs": t["segs"]} for t in tracks]}
    data_js = json.dumps(data, separators=(",", ":"))

    # the markup
    place_svg = []
    for code, label in PINS:
        mk = code in PHOTO_AT.values()
        if code in towns:                                  # a town: a small square and its name in capitals
            place_svg.append('<g class="v4i-fl-pl is-town" data-c="%s" data-l="%s" style="display:none"><rect x="-2.5" y="-2.5" width="5" height="5"/><text x="7" y="4">%s</text></g>' % (code, esc(label), esc(label)))
            continue
        place_svg.append('<g class="v4i-fl-pl" data-c="%s" data-l="%s"%s%s style="display:none"><circle r="2.6"%s/><text x="%d" y="4">%s</text></g>'
                         % (code, esc(label), ' data-mk=""' if mk else "", ' data-lm=""' if code in LM else "", ' style="display:none"' if mk else "", 19 if mk else 7, esc(label)))
    by_code = {}
    for title, code in PHOTO_AT.items():
        by_code.setdefault(code, []).append(title)
    marks = "".join('<button class="v4i-fl-mk" type="button" data-c="%s" hidden aria-label="Photographs at %s"></button>' % (code, esc(dict(PINS)[code])) for code in by_code)
    marks += "".join('<button class="v4i-fl-lm" type="button" data-c="%s" hidden aria-label="About %s"></button>' % (code, esc(LM[code]["title"])) for code, _ in PINS if code in LM)
    marks += "".join('<span class="v4i-fl-tp" hidden></span>' for _ in tracks)
    ico = {"in": '<svg viewBox="0 0 16 16"><path d="M8 3v10M3 8h10"/></svg>', "out": '<svg viewBox="0 0 16 16"><path d="M3 8h10"/></svg>',
           "left": '<svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg>', "right": '<svg viewBox="0 0 16 16"><path d="m6 3 5 5-5 5"/></svg>',
           "up": '<svg viewBox="0 0 16 16"><path d="M3 10 8 5l5 5"/></svg>', "down": '<svg viewBox="0 0 16 16"><path d="m3 6 5 5 5-5"/></svg>'}
    btn_labels = {"in": "Closer", "out": "Further", "left": "Turn left", "right": "Turn right", "up": "Tilt flatter", "down": "Tilt steeper"}
    btns = '<div class="v4i-fl-btns" aria-label="Map controls">' + "".join('<button class="v4i-fl-btn" type="button" data-do="%s" aria-label="%s" title="%s">%s</button>' % (k, btn_labels[k], btn_labels[k], ico[k]) for k in ("in", "out", "left", "right", "up", "down")) + '</div>'
    chips = ('<div class="v4i-fl-tks" hidden><span class="kicker">Flights flown here</span>' + "".join(
        '<button class="v4i-fl-tk" type="button" aria-pressed="false">%s<b>%s km</b></button>' % (esc(t["name"]), format(t["distance_km"], ".0f")) for t in tracks) + '</div>') if tracks else ""
    tcard = ('<div class="v4i-fl-tcard" hidden><div class="v4i-fl-th"><span class="v4i-fl-tn"></span><span class="v4i-fl-td"></span></div>'
             '<div class="v4i-fl-tg"><div class="v4i-fl-tkm"><b></b><span>km</span></div><div class="v4i-fl-tsp"><b></b><span>km/h over the route</span></div>'
             '<div class="v4i-fl-tal"><b></b><span>m highest</span></div><div class="v4i-fl-tdu"><b></b><span>in the air</span></div></div>'
             '<p class="v4i-fl-tnote"></p><button class="v4i-fl-tx" type="button">Close</button></div>') if tracks else ""
    def lm_html(code):
        """the open-source pictures that exist on disk, then the description, then who took the pictures"""
        lm, pics, names = LM[code], [], []
        for cr in lm_credits.get(code, []):
            f = os.path.join(LM_DIR, "1400", "%s-%d.webp" % (code, cr["n"]))
            if not os.path.exists(f):
                continue
            h = max(1, round(cr["h"] * 1400 / cr["w"]))
            pics.append('<figure class="v4i-fl-lf"><picture><source media="(max-width: 700px)" srcset="../img/india/landmarks/700/%s-%d.webp" type="image/webp">'
                        '<img src="../img/india/landmarks/1400/%s-%d.webp" width="1400" height="%d" alt="%s" loading="lazy" decoding="async"></picture></figure>'
                        % (code, cr["n"], code, cr["n"], h, esc(lm["title"] + (", photographed by " + cr["author"] if cr.get("author") else ""))))
            if cr.get("licence"):                              # the owner's own photographs carry no credit line
                names.append("%s (%s)" % (esc(cr["author"] or "unnamed"), esc(cr["licence"])))
        html = "".join(pics) + '<p class="v4i-fl-dp">%s</p>' % esc(lm["blurb"])
        if names:
            html += '<p class="v4i-fl-dc">Photographs: %s, via Wikimedia Commons</p>' % ", ".join(names)
        return html, len(pics)
    groups, lm_pics = [], 0
    for code, titles in by_code.items():
        figs_html = "".join('<figure>%s<figcaption><b>%s</b>%s</figcaption></figure>' % (figs[t], esc(t), esc(photos[t]["caption"])) for t in titles)
        extra, npics = lm_html(code) if code in LM else ("", 0)
        lm_pics += npics
        groups.append('<div class="v4i-fl-dg" data-c="%s" data-t="%s" hidden>%s%s</div>' % (code, esc(LM[code]["title"] if code in LM else dict(PINS)[code]), figs_html, extra))
    for code in LM:
        if code in by_code:
            continue
        extra, npics = lm_html(code)
        lm_pics += npics
        groups.append('<div class="v4i-fl-dg%s" data-c="%s" data-t="%s" hidden>%s</div>' % (" is-two" if npics in (2, 4) else "", code, esc(LM[code]["title"]), extra))
    dialog = ('<dialog class="v4i-fl-dlg" id="v4i-fl-dlg" aria-labelledby="v4i-fl-dt"><div class="v4i-fl-dh"><span class="kicker v4i-fl-dt" id="v4i-fl-dt"></span>'
              '<button class="v4i-fl-dx" type="button">Close</button></div>' + "".join(groups) + '</dialog>'
              '<dialog class="v4i-fl-lb" id="v4i-fl-lb" aria-label="The photograph, enlarged"><div class="v4i-fl-lbs"><img alt="" draggable="false"></div>'
              '<button class="v4i-fl-lbx" type="button" aria-label="Close the photograph"></button><span class="v4i-fl-lbc"></span>'
              '<button class="v4i-fl-lbn v4i-fl-lbp" type="button" hidden aria-label="Previous photograph"><svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg></button>'
              '<button class="v4i-fl-lbn v4i-fl-lbnx" type="button" hidden aria-label="Next photograph"><svg viewBox="0 0 16 16"><path d="m6 3 5 5-5 5"/></svg></button>'
              '<span class="v4i-fl-lbh" aria-hidden="true">click to come closer &middot; scroll or pinch for more &middot; drag to move &middot; arrows for the next &middot; click outside to close</span></dialog>')
    chapters = "".join('<li class="v4i-fl-c" data-i="%d"><div class="tm-card-t">%s</div></li>' % (i, c) for i, c in enumerate(cards))
    card_html = []
    placed_titles = [cd["n"] for cd in card_data]
    for cd in card_data:
        p = photos[cd["n"]]
        where = ("near " if cd["near"] else "at ") + cd["p"]
        card_html.append('<figure class="v4i-fl-card" data-k="%s">%s<figcaption><b>%s</b>%s<span class="v4i-fl-where">%s</span></figcaption></figure>'
                         % (esc(cd["n"]), figs[cd["n"]], esc(cd["n"]), esc(p["caption"]), esc(where)))
    row_titles = ROW + [nm for nm, _, _, _, _ in PLACED if nm not in placed_titles]
    row_html = []
    for nm in row_titles:
        p = photos[nm]
        row_html.append('<figure>%s<figcaption><b>%s</b>%s</figcaption></figure>' % (figs[nm], esc(nm), esc(p["caption"])))
    km0 = round(F[0]["width_km"])
    bil = fly["per_leg"][0] + 1
    still = ('<picture><source media="(max-width: 700px)" srcset="../img/india/fly/800/f%03d.webp" type="image/webp">'
             '<img src="../img/india/fly/1600/f%03d.webp" width="1600" height="900" alt="The Dhauladhar from above Bir: the launch at Billing on its ridge, the snow of the back ranges behind, rendered from open terrain data" loading="lazy" decoding="async"></picture>' % (bil, bil))
    flight = "\n".join([
        '<section class="dst-sec is-loud v4i-fl" id="flight" aria-labelledby="flight-h" data-src="">',
        '<script type="application/json" id="v4i-fl-data">%s</script>' % data_js,
        '<div class="v4i-fl-track"><div class="v4i-fl-pin">',
        '<div class="v4i-fl-map">' + still + '<canvas class="v4i-fl-canvas" aria-hidden="true"></canvas><div class="v4i-fl-scrim" aria-hidden="true"></div>',
        '<svg class="v4i-fl-ov" viewBox="0 0 1600 900" aria-hidden="true">' + "".join(place_svg) + '</svg>',
        '<div class="v4i-fl-mks">' + marks + '</div></div>',
        '<div class="v4i-fl-head"><span class="kicker">Bir Immersive</span><h2 id="flight-h">%s</h2>' % h2 +
        '<p>In from %d km wide over the Kangra valley, down to Billing, west along the front to Dharamshala, back east to 360, and up over the back. The scroll flies it, or take the controls and go where you like.</p></div>' % km0,
        '<button class="v4i-fl-ctl" type="button" data-take="Take the controls" data-back="Back to the flight">Take the controls</button>',
        btns, chips, tcard,
        '<span class="v4i-fl-hint" aria-hidden="true"><span class="is-long">drag the ground &middot; scroll to come closer &middot; right button to turn and tilt &middot; a ring opens the photographs &middot; a dotted name tells its story</span><span class="is-short">drag the ground &middot; pinch to come closer &middot; twist to turn, two fingers up or down to tilt &middot; a ring opens the photographs, a dotted name its story</span></span>',
        '<ol class="v4i-fl-ch">' + chapters + '</ol>',
        '<div class="v4i-fl-cards">' + "".join(card_html) + '</div>',
        '<svg class="v4i-fl-lead" viewBox="0 0 1600 900" aria-hidden="true"><line class="v4i-fl-tie"/><circle class="v4i-fl-halo" r="9"/><circle class="v4i-fl-dot" r="4"/></svg>',
        '<div class="v4i-fl-read" aria-hidden="true"><span class="v4i-fl-km"><b>%d</b>km wide</span><span class="v4i-fl-at"><i>over</i> Billing launch</span><span class="v4i-fl-alt">camera <b>3,600</b> m</span></div>' % round(F[bil - 1]["width_km"]),
        '<a class="v4i-fl-skip" href="#dates">Skip the flight <i aria-hidden="true">&darr;</i></a>',
        '</div></div>',
        '<p class="v4i-fl-cred">%s</p>' % (CREDIT + (LM_CREDIT if lm_pics else "")),
        dialog,
        '</section>',
        '',
        '<section class="dst-sec v4i-fl-row" id="pictures" aria-labelledby="pictures-h">',
        '<div class="dst-head"><span class="kicker">The pictures</span><h2 id="pictures-h">%s</h2></div>' % gh2,
        '<div class="v4i-fl-row-g">' + "".join(row_html) + '</div>',
        '</section>',
    ])
    t = t.replace("@@FLIGHT@@", flight + "\n", 1)

    # the jump bar: one entry for the two
    j = '<a href="#route">Routes</a>\n'
    assert t.count(j) == 1
    t = t.replace(j, '<a href="#flight">Bir Immersive</a>\n', 1)
    g = '<a href="#gallery">Gallery</a>\n'
    assert t.count(g) == 1
    t = t.replace(g, "", 1)
    assert 'href="#route"' not in t and 'href="#gallery"' not in t

    # page identity, style and script
    assert t.count("<title>Option C: ") == 1
    t = t.replace("<title>Option C: ", "<title>Option E: ", 1)
    t = t.replace("</head>", "<style>" + CSS + "</style>\n</head>", 1)
    t = t.replace("</body>", SCRIPT + "\n</body>", 1)

    # every photograph once on the page; the dialog holds the same picture again, unseen until its marker is tapped
    for nm in photos:
        f = photos[nm]["file"].split("/")[-1]
        c = len(re.findall(r'/%s\.(?:webp|jpg)' % re.escape(f), t))
        assert c in (2, 4), (nm, c)
    open(OUT, "w", encoding="utf-8").write(t)
    print("wrote", os.path.relpath(OUT, ROOT), n0, "->", len(t), "bytes; data", len(data_js), "bytes; plates", [(c["n"], c["a"], c["b"]) for c in card_data])


if __name__ == "__main__":
    build()
