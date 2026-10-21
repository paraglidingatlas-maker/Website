#!/usr/bin/env python3
"""v4 Kenya, option E: the six sites down the Rift flown over live terrain.

    python3 tools/v4_kenya_e.py

Reads prototypes/v4/destinations/kenya.html and writes kenya-e.html beside it. The
route section (#route) becomes the flight: the same engine as India (prototypes/v4/fly.js)
over a two-layer ground, a coarse journey layer for the whole Rift and a finer inset per
site loaded as the camera nears it (tools/data/kenya-dem.json). The six route cards are
the chapters, the owner's own flights are the tracks, the towns come from GeoNames. No
photographs are placed yet: that is stage four, once the owner places them. v4 itself is
untouched: this writes an option page only."""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import v4_india_e as I  # noqa: E402  the CSS and the escapes are shared

SRC = os.path.join(V4, "destinations", "kenya.html")
OUT = os.path.join(V4, "destinations", "kenya-e.html")
DEM = os.path.join(ROOT, "tools", "data", "kenya-dem.json")
TRACKS = os.path.join(ROOT, "tools", "data", "kenya-tracks.json")
TOWNS = os.path.join(ROOT, "tools", "data", "kenya-towns.json")
DEMBIN = os.environ.get("KENYA_DEM_BIN", "")      # the journey heights, to read elevations for the pins at build time

# the camera path: lon, lat, metres; the sun as azimuth and elevation, east in the morning over Kerio, west by afternoon down the Rift
KEYS = [
    ("opening",        (37.10, -2.75, 72000), (36.30, -0.30, 1500), 46, [70000, 300000], [255, 22]),
    ("kerio-approach", (35.95,  0.15, 26000), (35.55,  0.64, 1900), 48, [30000, 170000], [155, 30]),
    ("kerio-launch",   (35.575, 0.595, 3300), (35.512, 0.655, 2150), 50, [14000, 100000], [160, 26]),
    ("kerio-north",    (35.60,  0.98,  3600), (35.545, 1.19, 2150), 50, [14000, 100000], [160, 28]),
    ("transit-1",      (35.75, -0.05, 65000), (36.30, -0.80, 1700), 46, [50000, 260000], [170, 42]),
    ("hells-gate",     (36.22, -0.80,  3600), (36.31, -0.90, 1950), 50, [14000, 100000], [225, 28]),
    ("longonot",       (36.39, -0.84,  4800), (36.455, -0.915, 2500), 50, [14000, 100000], [230, 27]),
    ("kijabe",         (36.49, -0.985, 3900), (36.56, -0.925, 2350), 50, [14000, 100000], [235, 28]),
    ("transit-2",      (36.75, -1.15, 48000), (37.22, -1.50, 1700), 46, [45000, 240000], [230, 40]),
    ("machakos",       (37.17, -1.44,  3600), (37.265, -1.52, 1800), 50, [14000, 100000], [235, 28]),
    ("site-13-feb",    (37.33, -1.99,  3300), (37.395, -2.07, 1600), 50, [14000, 100000], [235, 27]),
    ("transit-3",      (37.55, -2.25, 42000), (37.87, -2.66, 1500), 46, [45000, 240000], [240, 38]),
    ("chyulu",         (37.77, -2.58,  4200), (37.885, -2.68, 1750), 50, [14000, 100000], [240, 26]),
    ("kilimanjaro",    (37.62, -2.72,  9000), (37.35, -3.07, 4500), 48, [40000, 220000], [250, 22]),
]
PER_LEG = [22, 14, 16, 18, 16, 10, 14, 12, 16, 12, 14, 16, 14]
LEG_CHAPTER = [0, 0, 0, 0, 1, 1, 2, 3, 4, 4, 4, 5, 5]
# the pins, in priority order: the owner's launches from his tracks, the six sites from the page, then the towns
LAUNCHES = [("L01", "Kerio launch", 35.5141, 0.639, 2226), ("L02", "Rift wall launch, 8 Feb", 36.5461, -0.9109, 2656), ("L03", "Launch, 13 Feb", 37.392, -2.0681, 1614)]
PHONE_PINS = 6
CREDIT = ("The ground is open terrain data (AWS Terrain Tiles, Mapzen Terrarium, from SRTM and other open sources), a coarse layer for the whole "
          "Rift and a finer one over each site, drawn live as relief, flown by the scroll or moved by hand. The sites are the six of the tour, the "
          "launches are read from the owner's own tracklogs and the towns are placed from GeoNames (CC BY 4.0). The flights drawn are the owner's, "
          "scored by the XContest rules: the distance is the scored route, the dashed line is that route, and the average speed is the scored "
          "distance over the time in the air.")


def px_of(lon, lat, g):
    n = 2 ** g["z"]; x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return [round((x - g["tx0"]) * 256 / g["down"], 1), round((y - g["ty0"]) * 256 / g["down"], 1)]


def build():
    t = open(SRC, encoding="utf-8").read()
    dem = json.load(open(DEM)); g = dem["grid"]
    tracks = json.load(open(TRACKS))["tracks"]
    towns = json.load(open(TOWNS))["towns"]
    heights = None
    if DEMBIN and os.path.exists(DEMBIN):
        import numpy as np
        heights = np.fromfile(DEMBIN, np.float32).reshape(g["h"], g["w"])
    def elev(px):
        if heights is None: return g["base_m"]
        x, y = int(min(max(px[0], 0), g["w"] - 1)), int(min(max(px[1], 0), g["h"] - 1)); return float(round(heights[y, x]))

    # the route section: its six cards are the chapters and the sites
    m = re.search(r'<section class="dst-sec tm" id="route"(.*?)</section>\n', t, re.S)
    assert m, "route section"
    route = m.group(0)
    sites = json.loads(re.search(r'data-v4-sites="([^"]+)"', route).group(1).replace("&quot;", '"'))
    assert len(sites) == 6, len(sites)
    cards = re.findall(r'<div class="tm-card-t">(.*?)</div></article>', route, re.S)
    assert len(cards) == 6, len(cards)
    h2 = re.search(r'<h2 id="route-h">(.*?)</h2>', route).group(1)
    t = t[:m.start()] + "@@FLIGHT@@" + t[m.end():]

    # the pins
    wp = {}
    for code, label, lon, lat, alt in LAUNCHES:
        wp[code] = dict(label=label, px=px_of(lon, lat, g), elev=alt, kind="launch")
    for i, s in enumerate(sites):
        px = px_of(s["lon"], s["lat"], g); wp["S%02d" % (i + 1)] = dict(label=s["name"], px=px, elev=elev(px), kind="site")
    for code, tw in towns.items():
        px = px_of(tw["lon"], tw["lat"], g); wp[code] = dict(label=tw["label"], px=px, elev=elev(px), kind="town")
    pins = [("L01", "Kerio launch")] + [("S%02d" % (i + 1), s["name"]) for i, s in enumerate(sites)] + [(c, l) for c, l, _, _, _ in LAUNCHES[1:]] + [(c, tw["label"]) for c, tw in towns.items()]

    keys = [dict(name=n, cam=px_of(c[0], c[1], g) + [c[2]], tgt=px_of(tg[0], tg[1], g) + [tg[2]], fov=fov, fog=fog, sun=sun) for n, c, tg, fov, fog, sun in KEYS]
    assert len(PER_LEG) == len(keys) - 1 == len(LEG_CHAPTER)
    data = {"grid": g, "textures": dem["textures"], "layers": dem["layers"], "edge_fade": 0.04, "keys": keys, "per_leg": PER_LEG, "bounds": dem["bounds"],
            "light": dem["light"], "waypoints": wp, "chapter": LEG_CHAPTER, "cards": [], "farKm": 50, "phonePins": PHONE_PINS,
            "tracks": [{"name": x["name"], "date": x["date"], "distance_km": x["distance_km"], "duration_min": x["duration_min"], "avg_kmh": x["avg_kmh"],
                        "max_alt_m": x["max_alt_m"], "type": x["type"], "closed": x["closed"], "points": x["points"], "ground_km": x["ground_km"],
                        "off_map": x["off_map"], "route": x["route"], "segs": x["segs"]} for x in tracks]}
    data_js = json.dumps(data, separators=(",", ":"))

    esc = I.esc
    place_svg = []
    for code, label in pins:
        if wp[code]["kind"] == "town":
            place_svg.append('<g class="v4i-fl-pl is-town" data-c="%s" data-l="%s" style="display:none"><rect x="-2.5" y="-2.5" width="5" height="5"/><text x="7" y="4">%s</text></g>' % (code, esc(label), esc(label)))
        else:
            place_svg.append('<g class="v4i-fl-pl" data-c="%s" data-l="%s" style="display:none"><circle r="2.6"/><text x="7" y="4">%s</text></g>' % (code, esc(label), esc(label)))
    marks = "".join('<span class="v4i-fl-tp" hidden></span>' for _ in tracks)
    ico = {"in": '<svg viewBox="0 0 16 16"><path d="M8 3v10M3 8h10"/></svg>', "out": '<svg viewBox="0 0 16 16"><path d="M3 8h10"/></svg>',
           "left": '<svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg>', "right": '<svg viewBox="0 0 16 16"><path d="m6 3 5 5-5 5"/></svg>',
           "up": '<svg viewBox="0 0 16 16"><path d="M3 10 8 5l5 5"/></svg>', "down": '<svg viewBox="0 0 16 16"><path d="m3 6 5 5 5-5"/></svg>'}
    btn_labels = {"in": "Closer", "out": "Further", "left": "Turn left", "right": "Turn right", "up": "Tilt flatter", "down": "Tilt steeper"}
    btns = '<div class="v4i-fl-btns" aria-label="Map controls">' + "".join('<button class="v4i-fl-btn" type="button" data-do="%s" aria-label="%s" title="%s">%s</button>' % (k, btn_labels[k], btn_labels[k], ico[k]) for k in ("in", "out", "left", "right", "up", "down")) + '</div>'
    chips = ('<div class="v4i-fl-tks" hidden><span class="kicker">Flights flown here</span>' + "".join(
        '<button class="v4i-fl-tk" type="button" aria-pressed="false">%s<b>%s km</b></button>' % (esc(x["name"]), format(x["distance_km"], ".0f")) for x in tracks) + '</div>') if tracks else ""
    tcard = ('<div class="v4i-fl-tcard" hidden><div class="v4i-fl-th"><span class="v4i-fl-tn"></span><span class="v4i-fl-td"></span></div>'
             '<div class="v4i-fl-tg"><div class="v4i-fl-tkm"><b></b><span>km</span></div><div class="v4i-fl-tsp"><b></b><span>km/h over the route</span></div>'
             '<div class="v4i-fl-tal"><b></b><span>m highest</span></div><div class="v4i-fl-tdu"><b></b><span>in the air</span></div></div>'
             '<p class="v4i-fl-tnote"></p><button class="v4i-fl-tx" type="button">Close</button></div>') if tracks else ""
    dialog = ('<dialog class="v4i-fl-dlg" id="v4i-fl-dlg" aria-labelledby="v4i-fl-dt"><div class="v4i-fl-dh"><span class="kicker v4i-fl-dt" id="v4i-fl-dt"></span>'
              '<button class="v4i-fl-dx" type="button">Close</button></div></dialog>'
              '<dialog class="v4i-fl-lb" id="v4i-fl-lb" aria-label="The photograph, enlarged"><div class="v4i-fl-lbs"><img alt="" draggable="false"></div>'
              '<button class="v4i-fl-lbx" type="button" aria-label="Close the photograph"></button><span class="v4i-fl-lbc"></span>'
              '<button class="v4i-fl-lbn v4i-fl-lbp" type="button" hidden aria-label="Previous photograph"><svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg></button>'
              '<button class="v4i-fl-lbn v4i-fl-lbnx" type="button" hidden aria-label="Next photograph"><svg viewBox="0 0 16 16"><path d="m6 3 5 5-5 5"/></svg></button>'
              '<span class="v4i-fl-lbh" aria-hidden="true">click to come closer &middot; scroll or pinch for more &middot; drag to move &middot; arrows for the next &middot; click outside to close</span></dialog>')
    chapters = "".join('<li class="v4i-fl-c" data-i="%d"><div class="tm-card-t">%s</div></li>' % (i, c) for i, c in enumerate(cards))
    still = ('<img src="../../../assets/destinations/kenya/gallery/kerio-valley.webp" width="1152" height="768" alt="The Kerio Valley from the air" loading="lazy" decoding="async">')
    flight = "\n".join([
        '<section class="dst-sec is-loud v4i-fl" id="flight" aria-labelledby="flight-h" data-src="">',
        '<script type="application/json" id="v4i-fl-data">%s</script>' % data_js,
        '<div class="v4i-fl-track"><div class="v4i-fl-pin">',
        '<div class="v4i-fl-map">' + still + '<canvas class="v4i-fl-canvas" aria-hidden="true"></canvas><div class="v4i-fl-scrim" aria-hidden="true"></div>',
        '<svg class="v4i-fl-ov" viewBox="0 0 1600 900" aria-hidden="true">' + "".join(place_svg) + '</svg>',
        '<div class="v4i-fl-mks">' + marks + '</div></div>',
        '<div class="v4i-fl-head"><span class="kicker">Rift Immersive</span><h2 id="flight-h">%s</h2>' % h2 +
        '<p>From the Elgeyo escarpment at Kerio in the north to the Chyulu Hills in the south, the scroll flies the six sites in order, 451 km end to end. Or take the controls and go where you like.</p></div>',
        '<button class="v4i-fl-ctl" type="button" data-take="Take the controls" data-back="Back to the flight">Take the controls</button>',
        btns, chips, tcard,
        '<span class="v4i-fl-hint" aria-hidden="true"><span class="is-long">drag the ground &middot; scroll to come closer &middot; right button to turn and tilt</span><span class="is-short">drag the ground &middot; pinch to come closer &middot; twist to turn, two fingers up or down to tilt</span></span>',
        '<ol class="v4i-fl-ch">' + chapters + '</ol>',
        '<div class="v4i-fl-cards"></div>',
        '<svg class="v4i-fl-lead" viewBox="0 0 1600 900" aria-hidden="true"><line class="v4i-fl-tie"/><circle class="v4i-fl-halo" r="9"/><circle class="v4i-fl-dot" r="4"/></svg>',
        '<div class="v4i-fl-read" aria-hidden="true"><span class="v4i-fl-km"><b>160</b>km wide</span><span class="v4i-fl-at"><i>over</i> the Rift</span><span class="v4i-fl-alt">camera <b>95,000</b> m</span></div>',
        '<a class="v4i-fl-skip" href="#dates">Skip the flight <i aria-hidden="true">&darr;</i></a>',
        '</div></div>',
        '<p class="v4i-fl-cred">%s</p>' % CREDIT,
        dialog,
        '</section>',
    ])
    t = t.replace("@@FLIGHT@@", flight + "\n", 1)

    j = '<a href="#route">Routes</a>\n'
    assert t.count(j) == 1
    t = t.replace(j, '<a href="#flight">Rift Immersive</a>\n', 1)
    assert 'href="#route"' not in t

    assert t.count("<title>Kenya: ") == 1
    t = t.replace("<title>Kenya: ", "<title>Option E: Kenya: ", 1)
    t = t.replace("</head>", "<style>" + I.CSS + "</style>\n</head>", 1)
    t = t.replace("</body>", '<script type="module" src="../fly.js"></script>\n</body>', 1)
    open(OUT, "w", encoding="utf-8").write(t)
    print("wrote %s %d bytes; data %d bytes; %d pins, %d tracks, %d layers" % (os.path.relpath(OUT, ROOT), len(t), len(data_js), len(pins), len(tracks), len(dem["layers"])))


if __name__ == "__main__":
    build()
