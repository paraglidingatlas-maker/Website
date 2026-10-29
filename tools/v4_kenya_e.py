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

SRC = os.environ.get("KENYA_SRC") or os.path.join(V4, "destinations", "kenya.html")   # the live page before tools/v4_kenya_immersive.py puts this flight in it
OUT = os.path.join(V4, "destinations", "kenya-e.html")
DEM = os.path.join(ROOT, "tools", "data", "kenya-dem.json")
TRACKS = os.path.join(ROOT, "tools", "data", "kenya-tracks.json")
TOWNS = os.path.join(ROOT, "tools", "data", "kenya-towns.json")
PLACES = os.path.join(ROOT, "tools", "data", "kenya-places.json")
BORDERS = os.path.join(ROOT, "tools", "data", "kenya-borders.json")   # Natural Earth admin-0 boundary lines inside the box
COUNTRIES = [("C01", "Kenya", 36.1, -1.25), ("C02", "Tanzania", 36.35, -2.75)]   # one word each, on their own soil, for orientation   # wildlife, peoples, origins and landmarks along the way, each with a story
EMOJI = os.path.join(ROOT, "tools", "data", "emoji")                     # the figures: Noto Emoji (Apache 2.0) and a baobab drawn to match
LIFE_KINDS = ("elephant", "giraffe", "zebra", "rhino", "hippo", "buffalo", "lion", "flamingo", "runner", "cattle", "walker", "crocodile", "baobab")
DEMBIN = os.environ.get("KENYA_DEM_BIN", "")      # the journey heights, to read elevations for the pins at build time

# the camera path: lon, lat, metres; the sun as azimuth and elevation, east in the morning over Kerio, west by afternoon down the Rift
KEYS = [
    ("opening",        (37.10, -2.75, 72000), (36.43, -0.69, 1500), 46, [100000, 400000], [255, 22]),   # halfway down (owner, 28 Oct): up the Rift and the ground below, the far edge against the page black
    ("kerio-approach", (35.95,  0.15, 26000), (35.55,  0.64, 1900), 48, [60000, 260000], [155, 30]),
    ("kerio-launch",   (35.575, 0.595, 3300), (35.512, 0.655, 2150), 50, [14000, 100000], [160, 26]),
    ("kerio-north",    (35.60,  0.98,  3600), (35.545, 1.19, 2150), 50, [14000, 100000], [160, 28]),
    ("transit-1",      (35.75, -0.05, 65000), (36.30, -0.80, 1700), 46, [120000, 430000], [170, 42]),
    ("hells-gate",     (36.22, -0.80,  3600), (36.31, -0.90, 1950), 50, [14000, 100000], [225, 28]),
    ("longonot",       (36.39, -0.84,  4800), (36.455, -0.915, 2500), 50, [14000, 100000], [230, 27]),
    ("kijabe",         (36.49, -0.985, 3900), (36.56, -0.925, 2350), 50, [14000, 100000], [235, 28]),
    ("transit-2",      (36.92, -1.24, 12000), (37.25, -1.52, 1800), 48, [60000, 260000], [230, 34]),   # from here on low and continuous (owner, 29 Oct: "smoothened out with flying sites in focus")
    ("machakos",       (37.17, -1.44,  3600), (37.265, -1.52, 1800), 50, [14000, 100000], [235, 28]),
    ("site-13-feb",    (37.33, -1.99,  3300), (37.395, -2.07, 1600), 50, [14000, 100000], [235, 27]),
    ("transit-3",      (37.60, -2.36,  9000), (37.87, -2.66, 1600), 48, [50000, 240000], [240, 32]),
    ("chyulu",         (37.77, -2.58,  4200), (37.885, -2.68, 1750), 50, [14000, 100000], [240, 26]),
    ("glide",          (37.74, -2.66,  6500), (37.38, -3.04, 4600), 48, [40000, 220000], [248, 24]),   # the glide out: the summit held in view, no turn to the sea
    ("kilimanjaro",    (37.60, -2.76,  8500), (37.355, -3.067, 4800), 46, [60000, 300000], [250, 22]),
]
PORTRAIT_TGT = {"opening": (36.70, -1.525, 1500)}   # a tall screen stands further back with a wider lens: it looks steeper down so the ground still fills the frame
PER_LEG = [22, 14, 16, 18, 16, 10, 14, 12, 16, 12, 14, 16, 12, 20]
LEG_CHAPTER = [0, 0, 0, 0, 1, 1, 2, 3, 4, 4, 4, 5, 5, 5]
# the pins, in priority order: the owner's launches from his tracks, the six sites from the page, then the towns
LAUNCHES = [("L01", "Kerio launch", 35.5141, 0.639, 2226), ("L02", "Rift wall launch, 8 Feb", 36.5461, -0.9109, 2656), ("L03", "Launch, 13 Feb", 37.392, -2.0681, 1614)]
PHONE_PINS = 6
LIFE_SIZE = {"min": 22, "max": 52, "cap": 62, "near": 2500, "far": 160000, "few": 3}   # a figure's height on the screen, px: far overview to close by
SKY = {"haze": "#2e2f36", "zenith": "#141519", "lo": -0.12, "hi": 0.42}     # haze at the ground's far edge, the page's dark overhead: no flat black behind the first frame
CREDIT = ("The ground is open terrain data (AWS Terrain Tiles, Mapzen Terrarium, from SRTM and other open sources), a coarse layer for the whole "
          "Rift and a finer one over each site, drawn live as relief, flown by the scroll or moved by hand. The sites are the six of the tour, the "
          "launches are read from the owner's own tracklogs and the towns are placed from GeoNames (CC BY 4.0); the parks, peoples, prehistoric sites and landmarks "
          "along the way are placed by hand at the centre of each area, with a few lines each from published sources; the border is Natural Earth's. The flights drawn are the owner's, "
          "scored by the XContest rules: the distance is the scored route, the dashed line is that route, and the average speed is the scored "
          "distance over the time in the air. The figures are Noto Emoji (Google, Apache 2.0): they stand on ground placed by hand near each park, lake or town, in view at any distance, "
          "for the animals and people of a place, not for sightings.")


# this page's own rules, after the shared flight CSS: the hand mode kept clean
KCSS = (
    # the flights flown: one compact row under the title, never a block over the map
    ".v4i-fl-tks{flex-wrap:nowrap;align-items:center;max-width:calc(100% - 2 * var(--gutter));top:clamp(9.2rem,18vh,10.6rem)}"
    ".v4i-fl-tks .kicker{width:auto;margin:0 .5rem 0 0;white-space:nowrap}"
    ".v4i-fl-tk{white-space:nowrap;flex:none}"
    # the hint: along the foot, where the chapters were, clear of the title
    ".v4i-fl.is-free .v4i-fl-hint{top:auto;bottom:clamp(2.6rem,6vh,3.6rem);left:var(--gutter);right:auto;text-align:left;max-width:min(44rem,calc(100% - 2 * var(--gutter) - 17rem));border-radius:.9rem}"
    # the chapter index: a slim mono rail on the right edge, in flight only
    ".v4i-fl-jump{display:none}"
    ".v4i-fl.is-live .v4i-fl-jump{display:block;position:absolute;z-index:4;right:calc(var(--gutter) - .6rem);top:50%;transform:translateY(-50%);transition:opacity .3s var(--ease)}"
    ".v4i-fl-jump ol{list-style:none;margin:0;padding:0;display:grid}"
    ".v4i-fl-jump button{position:relative;display:flex;align-items:center;justify-content:flex-end;gap:.55rem;min-height:2.25rem;min-width:2.75rem;padding:0 .6rem;margin:0;background:none;border:0;border-radius:999px;cursor:pointer;"
    "font:400 var(--fs-micro)/1 var(--font-mono);letter-spacing:.06em;color:var(--gray-light);text-shadow:0 0 4px rgba(20,21,25,.95),0 0 2px rgba(20,21,25,.95)}"
    ".v4i-fl-jump .t{display:block;width:.8rem;height:2px;border-radius:1px;background:currentColor;opacity:.7;transition:width .25s var(--ease)}"
    ".v4i-fl-jump .l{position:absolute;right:100%;top:50%;transform:translateY(-50%);opacity:0;white-space:nowrap;color:var(--white);background:rgba(20,21,25,.78);border-radius:999px;padding:.35rem .6rem;text-shadow:none;transition:opacity .2s var(--ease);pointer-events:none}"
    ".v4i-fl-jump button:hover,.v4i-fl-jump button:focus-visible{color:var(--white);outline:none}"
    ".v4i-fl-jump button:hover .l,.v4i-fl-jump button:focus-visible .l{opacity:1}"
    ".v4i-fl-jump button:focus-visible .n{outline:1px solid var(--orange);outline-offset:3px;border-radius:2px}"
    ".v4i-fl-jump button[aria-current]{color:var(--orange)}"
    ".v4i-fl-jump button[aria-current] .t{width:1.4rem;opacity:1}"
    ".v4i-fl.is-free .v4i-fl-jump,.v4i-fl.is-tracked .v4i-fl-jump{opacity:0;visibility:hidden;pointer-events:none}"
    "@media (prefers-reduced-motion:reduce){.v4i-fl-jump .t,.v4i-fl-jump .l{transition:none}}"
    "@media (max-width:700px){"
    ".v4i-fl.is-live .v4i-fl-jump{right:0;top:47%}"
    ".v4i-fl-jump button{min-height:44px;min-width:44px;padding:0 .7rem 0 .4rem;gap:.4rem}"
    ".v4i-fl-jump .l{display:none}"
    # a phone: the row scrolls sideways under the title, the top third stays the map's
    ".v4i-fl-tks{top:8.9rem;left:0;right:0;max-width:none;padding:0 var(--gutter) .2rem;overflow-x:auto;overscroll-behavior-x:contain;scrollbar-width:none;-webkit-overflow-scrolling:touch}"
    ".v4i-fl-tks::-webkit-scrollbar{display:none}"
    ".v4i-fl-tk{padding:.5rem .75rem}"
    ".v4i-fl.is-free .v4i-fl-hint{display:none}"
    "}"
)


# the chapter index: each tick scrolls to where its chapter begins on the flight; the one on screen is orange
JUMP_JS = """(function () {
  var s = document.getElementById("flight"), nav = s && s.querySelector(".v4i-fl-jump"), el = document.getElementById("v4i-fl-data"); if (!nav || !el) return;
  var D; try { D = JSON.parse(el.textContent); } catch (e) { return; }
  var n = 0, at = [], acc = 0; D.per_leg.forEach(function (k) { n += k; }); n += 1;
  D.per_leg.forEach(function (k, leg) { var c = D.chapter[leg]; if (at[c] === undefined) at[c] = acc; acc += k; });
  var bs = [].slice.call(nav.querySelectorAll("button")), chs = [].slice.call(s.querySelectorAll(".v4i-fl-c"));
  function mark() { var on = -1; chs.forEach(function (c, k) { if (c.classList.contains("is-on")) on = k; }); bs.forEach(function (b, k) { if (k === on) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current"); }); }
  bs.forEach(function (b) { b.addEventListener("click", function () {
    var k = +b.getAttribute("data-k"), f = Math.min(n - 1, (at[k] || 0) + (k ? 1.5 : 0)), r = s.getBoundingClientRect(), h = r.height - window.innerHeight;
    var y = window.scrollY + r.top + f / (n - 1) * h, calm = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({ top: Math.round(y), behavior: calm ? "auto" : "smooth" }); }); });
  if ("MutationObserver" in window) new MutationObserver(mark).observe(s.querySelector(".v4i-fl-ch"), { subtree: true, attributes: true, attributeFilter: ["class"] });
  mark();
})();"""


def textures(dem):
    """the ground's images, lighter and on phones sharper: heights as lossless WebP (the same metres as the PNGs, a third fewer
    bytes), the colour at 2k as WebP for every screen; a phone gets the journey heights at 1k, the sites at three quarters
    of the 2k, and the 2k colour and water (all written beside the originals by the fix pass, nothing removed)"""
    def web(path, old, new): return path.replace(old, new) if path else path
    tex = json.loads(json.dumps(dem["textures"])); layers = json.loads(json.dumps(dem["layers"]))
    d, ph = tex["desktop"], tex["phone"]
    d["h"] = web(d["h"], ".png", ".webp"); d["c"] = web(d["c"], ".jpg", ".webp")
    ph["h"] = web(ph["h"], ".png", ".webp"); ph["c"] = d["c"]; ph["w"] = d.get("w") or ph.get("w")
    for L in layers:
        d, ph = L["textures"]["desktop"], L["textures"]["phone"]
        d["h"] = web(d["h"], ".png", ".webp"); d["c"] = web(d["c"], ".jpg", ".webp")
        ph["h"] = d["h"].replace("-2k.webp", "-1k5.webp"); ph["c"] = d["c"]
        if d.get("w"): ph["w"] = d["w"]
        ph["seg"] = [v * 3 // 4 for v in d["seg"]]
    for t in [tex["desktop"], tex["phone"]] + [L["textures"][k] for L in layers for k in ("desktop", "phone")]:
        for k in ("h", "c", "w"):
            if t.get(k): assert os.path.exists(os.path.join(V4, "destinations", t[k])), t[k]
    return tex, layers


def symbols():
    """the figures as SVG symbols, ids made unique per file, for <use> from the overlay and the dialog"""
    out = []
    for kind in LIFE_KINDS:
        s = open(os.path.join(EMOJI, kind + ".svg"), encoding="utf-8").read()
        s = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", s, flags=re.S)
        m = re.search(r"<svg\b[^>]*>(.*)</svg>", s, re.S); assert m, kind
        inner = m.group(1)
        for i in sorted(set(re.findall(r'\bid="([^"]+)"', inner)), key=len, reverse=True):
            inner = inner.replace('id="%s"' % i, 'id="em-%s-%s"' % (kind, i)).replace("url(#%s)" % i, "url(#em-%s-%s)" % (kind, i)).replace('href="#%s"' % i, 'href="#em-%s-%s"' % (kind, i))
        inner = re.sub(r"\s+", " ", inner).strip()
        out.append('<symbol id="v4i-em-%s" viewBox="0 0 128 128">%s</symbol>' % (kind, inner))
    return "<defs>" + "".join(out) + "</defs>"


def px_of(lon, lat, g):
    n = 2 ** g["z"]; x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return [round((x - g["tx0"]) * 256 / g["down"], 1), round((y - g["ty0"]) * 256 / g["down"], 1)]


def build():
    t = open(SRC, encoding="utf-8").read()
    dem = json.load(open(DEM)); g = dem["grid"]
    tracks = json.load(open(TRACKS))["tracks"]
    towns = json.load(open(TOWNS))["towns"]
    places = json.load(open(PLACES))["places"]
    borders = []
    for ln in json.load(open(BORDERS))["lines"]:               # only the runs of points that lie on the terrain
        run = []
        for lon, lat in ln["pts"]:
            px = px_of(lon, lat, g)
            if 0 <= px[0] < g["w"] and 0 <= px[1] < g["h"]: run.append(px)
            else:
                if len(run) > 1: borders.append(dict(name=ln["right_name"], pts=run))
                run = []
        if len(run) > 1: borders.append(dict(name=ln["right_name"], pts=run))
    stories = {pl["code"]: pl for pl in places}                      # by code: S-codes attach to the route cards, P-codes are their own pins
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
    for pl in places:
        if pl.get("site"): continue
        px = px_of(pl["lon"], pl["lat"], g); wp[pl["code"]] = dict(label=pl["label"], px=px, elev=elev(px), kind=pl["kind"])
    for code, tw in towns.items():
        px = px_of(tw["lon"], tw["lat"], g); wp[code] = dict(label=tw["label"], px=px, elev=elev(px), kind="town")
    for code, name, lon, lat in COUNTRIES:
        px = px_of(lon, lat, g); wp[code] = dict(label=name, px=px, elev=elev(px), kind="country")
    pins = ([("L01", "Kerio launch")] + [("S%02d" % (i + 1), s["name"]) for i, s in enumerate(sites)] + [(c, l) for c, l, _, _, _ in LAUNCHES[1:]]
            + [(c, n) for c, n, _, _ in COUNTRIES] + [(pl["code"], pl["label"]) for pl in places if not pl.get("site")] + [(c, tw["label"]) for c, tw in towns.items()])
    for code in stories: assert code in wp, code
    life = []                                                        # the figures: where they stand, how many, how they move
    for code, pl in stories.items():
        for e in pl.get("life", []):
            assert e["kind"] in LIFE_KINDS, e["kind"]
            at = e.get("at") or [pl["lat"], pl["lon"]]
            g1 = dict(c=code, kind=e["kind"], name=e["name"], n=e["n"], mode=e["mode"], km=e["km"], px=px_of(at[1], at[0], g))
            if e.get("to"): g1["to"] = px_of(e["to"][1], e["to"][0], g)
            life.append(g1)

    keys = [dict(name=n, cam=px_of(c[0], c[1], g) + [c[2]], tgt=px_of(tg[0], tg[1], g) + [tg[2]], fov=fov, fog=fog, sun=sun) for n, c, tg, fov, fog, sun in KEYS]
    for k in keys:
        if k["name"] in PORTRAIT_TGT: pt = PORTRAIT_TGT[k["name"]]; k["ptgt"] = px_of(pt[0], pt[1], g) + [pt[2]]
    assert len(PER_LEG) == len(keys) - 1 == len(LEG_CHAPTER)
    tex, layers = textures(dem)
    data = {"grid": g, "textures": tex, "layers": layers, "dprMax": 2, "edge_fade": 0.04, "keys": keys, "per_leg": PER_LEG, "flow": [k[0] for k in KEYS].index("transit-2"), "bounds": dem["bounds"],
            "light": dem["light"], "waypoints": wp, "chapter": LEG_CHAPTER, "cards": [], "farKm": 50, "phonePins": PHONE_PINS, "maxPins": 12, "borders": borders, "life": life,
            "lifeSize": LIFE_SIZE, "keepFree": [".v4i-fl-tks", ".v4i-fl-btns", ".v4i-fl-hint"], "keepFlight": [".v4i-fl-jump"], "flipLabels": True, "tracks": [{"name": x["name"], "date": x["date"], "distance_km": x["distance_km"], "duration_min": x["duration_min"], "avg_kmh": x["avg_kmh"],
                        "max_alt_m": x["max_alt_m"], "type": x["type"], "closed": x["closed"], "points": x["points"], "ground_km": x["ground_km"],
                        "off_map": x["off_map"], "route": x["route"], "segs": x["segs"]} for x in tracks]}
    data_js = json.dumps(data, separators=(",", ":"))

    esc = I.esc
    GLYPH = {"wildlife": '<path d="M0 -3.4 3.4 0 0 3.4 -3.4 0z"/>', "people": '<path d="M0 -3.6 3.4 2.6 -3.4 2.6z"/>', "origins": '<circle class="is-hollow" r="2.9"/>', "landmark": '<circle r="2.6"/>'}
    place_svg = []
    for code, label in pins:
        kind = stories[code]["kind"] if code in stories else wp[code]["kind"]
        if kind == "town":
            place_svg.append('<g class="v4i-fl-pl is-town" data-c="%s" data-l="%s" style="display:none"><rect x="-2.5" y="-2.5" width="5" height="5"/><text x="7" y="4">%s</text></g>' % (code, esc(label), esc(label)))
        elif kind == "country":                            # a country's name, wide and quiet, no mark
            place_svg.append('<g class="v4i-fl-pl is-town is-country" data-c="%s" data-l="%s" style="display:none"><text x="0" y="4">%s</text></g>' % (code, esc(label), esc(label)))
        elif code in stories:                              # a story: its own glyph by kind, a dotted line under the name, the name the button
            place_svg.append('<g class="v4i-fl-pl is-story is-%s" data-c="%s" data-l="%s" data-lm="" style="display:none">%s<text x="8" y="4">%s</text></g>' % (kind if kind in GLYPH else "landmark", code, esc(label), GLYPH.get(kind, GLYPH["landmark"]), esc(label)))
        else:
            place_svg.append('<g class="v4i-fl-pl" data-c="%s" data-l="%s" style="display:none"><circle r="2.6"/><text x="7" y="4">%s</text></g>' % (code, esc(label), esc(label)))
    marks = "".join('<button class="v4i-fl-lm" type="button" data-c="%s" hidden aria-label="About %s"></button>' % (code, esc(stories[code]["title"])) for code, _ in pins if code in stories)
    marks += "".join('<span class="v4i-fl-tp" hidden></span>' for _ in tracks)
    KIND = {"wildlife": "Wildlife", "people": "People", "origins": "Origins", "landmark": "Landmark"}
    def notes(pl):                                                  # what moves here, under the story
        return "".join('<p class="v4i-fl-dl"><b><svg aria-hidden="true"><use href="#v4i-em-%s"/></svg>%s</b>%s</p>' % (e["kind"], esc(e["name"]), esc(e["note"]))
                       for e in pl.get("life", []) if e.get("note"))
    groups = "".join('<div class="v4i-fl-dg" data-c="%s" data-t="%s" hidden><span class="v4i-fl-dk">%s</span><p class="v4i-fl-dp">%s</p>%s</div>'
                     % (code, esc(pl["title"]), KIND.get(pl["kind"], "Place"), esc(pl["blurb"]), notes(pl)) for code, pl in stories.items())
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
              '<button class="v4i-fl-dx" type="button">Close</button></div>' + groups + '</dialog>'
              '<dialog class="v4i-fl-lb" id="v4i-fl-lb" aria-label="The photograph, enlarged"><div class="v4i-fl-lbs"><img alt="" draggable="false"></div>'
              '<button class="v4i-fl-lbx" type="button" aria-label="Close the photograph"></button><span class="v4i-fl-lbc"></span>'
              '<button class="v4i-fl-lbn v4i-fl-lbp" type="button" hidden aria-label="Previous photograph"><svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg></button>'
              '<button class="v4i-fl-lbn v4i-fl-lbnx" type="button" hidden aria-label="Next photograph"><svg viewBox="0 0 16 16"><path d="m6 3 5 5-5 5"/></svg></button>'
              '<span class="v4i-fl-lbh" aria-hidden="true">click to come closer &middot; scroll or pinch for more &middot; drag to move &middot; arrows for the next &middot; click outside to close</span></dialog>')
    names = [re.sub(r"<[^>]+>", "", re.search(r"<h3[^>]*>(.*?)</h3>", c, re.S).group(1)).strip() for c in cards]
    jump = ('<nav class="v4i-fl-jump" aria-label="Chapters of the flight"><ol>' + "".join(
        '<li><button type="button" data-k="%d" aria-label="Chapter %d of 6: %s"><span class="l" aria-hidden="true">%s</span><span class="n" aria-hidden="true">%02d</span><span class="t" aria-hidden="true"></span></button></li>'
        % (i, i + 1, n, n, i + 1) for i, n in enumerate(names)) + '</ol></nav>')
    chapters = "".join('<li class="v4i-fl-c" data-i="%d"><div class="tm-card-t">%s</div></li>' % (i, c) for i, c in enumerate(cards))
    still = ('<img src="../../../assets/destinations/kenya/gallery/kerio-valley.webp" width="1152" height="768" alt="The Kerio Valley from the air" loading="lazy" decoding="async">')
    flight = "\n".join([
        '<section class="dst-sec is-loud v4i-fl" id="flight" aria-labelledby="flight-h" data-src="">',
        '<script type="application/json" id="v4i-fl-data">%s</script>' % data_js,
        '<div class="v4i-fl-track"><div class="v4i-fl-pin">',
        '<div class="v4i-fl-map">' + still + '<canvas class="v4i-fl-canvas" aria-hidden="true"></canvas><div class="v4i-fl-scrim" aria-hidden="true"></div>',
        '<svg class="v4i-fl-ov" viewBox="0 0 1600 900" aria-hidden="true">' + symbols() + "".join(place_svg) + '</svg>',
        '<div class="v4i-fl-mks">' + marks + '</div></div>',
        '<div class="v4i-fl-head"><span class="kicker">Rift Immersive</span><h2 id="flight-h">%s</h2>' % h2 +
        '<p>From the Elgeyo escarpment at Kerio in the north to the Chyulu Hills in the south, the scroll flies the six sites in order, 451 km end to end. Or take the controls and go where you like.</p></div>',
        '<button class="v4i-fl-ctl" type="button" data-take="Take the controls" data-back="Back to the flight">Take the controls</button>',
        btns, chips, tcard,
        '<span class="v4i-fl-hint" aria-hidden="true"><span class="is-long">drag the ground &middot; scroll to come closer &middot; right button to turn and tilt &middot; a dotted name or an animal tells its story</span><span class="is-short">drag the ground &middot; pinch to come closer &middot; twist to turn, two fingers up or down to tilt &middot; a dotted name or an animal tells its story</span></span>',
        '<ol class="v4i-fl-ch">' + chapters + '</ol>', jump,
        '<div class="v4i-fl-cards"></div>',
        '<svg class="v4i-fl-lead" viewBox="0 0 1600 900" aria-hidden="true"><line class="v4i-fl-tie"/><circle class="v4i-fl-halo" r="9"/><circle class="v4i-fl-dot" r="4"/></svg>',
        '<div class="v4i-fl-read" aria-hidden="true"><span class="v4i-fl-km"><b>160</b>km wide</span><span class="v4i-fl-at"><i>over</i> the Rift</span><span class="v4i-fl-alt">camera <b>95,000</b> m</span></div>',
        '<a class="v4i-fl-skip" href="#dates">Skip the flight <i aria-hidden="true">&darr;</i></a>',
        '</div></div>',
        '<p class="v4i-fl-cred">%s</p>' % CREDIT,
        dialog,
        '<script>%s</script>' % JUMP_JS,
        '</section>',
    ])
    t = t.replace("@@FLIGHT@@", flight + "\n", 1)

    # the fly-in slides show the same three photographs the gallery loads: point them at the gallery's copies, one download each
    for nm in ("slope", "high", "ridge"):
        assert os.path.exists(os.path.join(ROOT, "assets", "destinations", "kenya", "gallery", "kenya-%s.webp" % nm)), nm
        t = t.replace("../../../assets/images/kenya-%s.webp" % nm, "../../../assets/destinations/kenya/gallery/kenya-%s.webp" % nm)

    j = '<a href="#route">Routes</a>\n'
    assert t.count(j) == 1
    t = t.replace(j, '<a href="#flight">Rift Immersive</a>\n', 1)
    assert 'href="#route"' not in t

    assert t.count("<title>Kenya: ") == 1
    t = t.replace("<title>Kenya: ", "<title>Option E: Kenya: ", 1)
    t = t.replace("</head>", "<style>" + I.CSS + KCSS + "</style>\n</head>", 1)
    t = t.replace("</body>", '<script type="module" src="../fly.js"></script>\n</body>', 1)
    open(OUT, "w", encoding="utf-8").write(t)
    print("wrote %s %d bytes; data %d bytes; %d pins, %d tracks, %d layers" % (os.path.relpath(OUT, ROOT), len(t), len(data_js), len(pins), len(tracks), len(dem["layers"])))


if __name__ == "__main__":
    build()
