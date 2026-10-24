#!/usr/bin/env python3
"""
The expeditions page, option C, "The atlas" (owner, 19 Oct 2026: "expeditions
standalone tab needs to be a redesigned page, it's just an off copy of
leftover material at homepage, I want it to be a bit different").

    prototypes/v4/expeditions-c.html   (canonical /expeditions.html)

For pilots choosing a trip, and plainly not the home page's #destinations
section (its four cards over one held picture, its dates-and-prices table and
its book-a-call band stay on the home page; none of them is repeated here).
Place-first and cartographic, with the lessons of the record page ("robotic,
too much text, hard to navigate", then "a cheap rip-off rather than
premium"): few words, typography and real photography as the graphics, one
signature, calm motion only in answer to the visitor.

  - the signature is one large map, drawn here from geometry in the site's
    map language (the trip pages' route maps: land a shade above the page,
    hairline coasts, a faint graticule, the equator dashed, places as small
    rings with spaced capitals): the world in the Equal Earth projection
    (Savric, Patterson and Jenny, 2018), the four places marked, filled where
    departures are set and open where the trip is planned. No tiles, no
    library;
  - on wide screens it is the page: the stage holds still while the scroll
    flies the atlas from the whole world to each place in the order they fly
    (India, Kenya, Kazakhstan, Peru) and back out; each move is the
    van Wijk and Nuij smooth zoom (out, across, in), eased toward where the
    scroll has put it in one loop that stops when it arrives. At a place with
    a photograph the photograph comes up out of the map from the place's own
    ring (a soft round reveal inside long eased masks, so it has no edge);
    the place's words stand at the left: its name, its one line, its facts as
    a map key, one way to book and one to read the trip. Choosing a place on
    the map or in the index along the foot flies straight to it; tabbing into
    a place's words takes you there too;
  - on phones and tablets the map becomes a vertical journey: the whole world
    first, as the index (each place a link), then the four places down the
    page, each opening on its own plate of the same map (the same drawing,
    framed on the place), its photograph rising out of the plate, then its
    words. Nothing is pinned, nothing slides sideways;
  - reduced motion and JavaScript off: the phone layout at every width (on
    wide screens each place's words beside its plate and photograph), all of
    it visible, nothing moving;
  - two quiet layers that answer the visitor: pointing at a place in the list
    lights it on the map and the other way round; and, drawn once when the
    page opens (never animated), the real night on the map at that moment,
    deepening from sunset to the end of astronomical twilight (a
    low-precision solar position), with "Night, now" in the map's key.

Nothing on the page is unknown, so nothing shows as [to supply]: the planned
trips show only what the home page gives them.

Facts, each from the site (nothing here is new):
  - the home page's #destinations section (prototypes/v4/index.html): India
    "Bir Billing, Himalaya", four departures in 2027 (15 to 24 Apr, 25 Apr to 4 May, 21 to 30 Oct, 3 to 12 Nov), 10 days,
    6 places, £1,100, "Guaranteed to run"; Kenya "Kerio Valley, Rift Valley",
    18 to 29 Jan 2027 and 1 to 12 Feb 2027, 12 days, 8 places, US$2,100,
    "Booking open"; Kazakhstan "The steppe", "Beyond Roads, Beyond Maps",
    planned June 2027, 10 days, small group, €2,100; Peru "Lima and the
    Andes", "Soar The Land Of The Incas", planned November 2027, 14 days,
    small group, €1,850; both planned trips "Register interest"
    (enquire.html?trip=kazakhstan, ?trip=peru);
  - destinations/india.html: "Ten days on the Dhauladhar, the wall of the
    Himalaya above Bir"; £1,100 per pilot; pilot rating IPPI 2 or equivalent;
    season October to November; cloudbase 3 to 3.6 km on the front range;
    Bir's place, 32.0500°N 76.7200°E (the page's own coordinates, shown as
    32.05°N · 76.72°E); "Hold a place" sends an enquiry (enquire.html?trip=india);
  - destinations/kenya.html: Kerio Valley "is the base", "the site where the
    world speed records are chased", 0.72°N · 35.65°E; "Starting from
    US$2,100"; pilot rating IPPI 2 or equivalent; season December to March;
    thermals 4 to 6 m/s at the midday peaks;
  - the call: the home page's free 30-minute call (the calendar link the
    site uses) and the enquiry page;
  - photographs: only the trip pages' own, each with the alt its page gives
    it, and named only as its page names it ("The Dhauladhar", "Kerio
    Valley", the trip pages' hero labels). Kazakhstan and Peru have no
    photographs on the site, so their plates are the map alone. No video
    (owner, 8 Oct: footage only on trip pages and the home page).
  - the map: country outlines from prototypes/workspace/atlas/data/world.json
    (Natural Earth 1:110m countries, public domain; read here, never edited),
    Antarctica left out. Coasts are the edges no two countries share, borders
    the edges two countries share. The markers for Kazakhstan and Peru stand
    for "The steppe" and "Lima and the Andes"; no coordinates are given for
    them because the site gives none.

The page takes the v4 shell (head, menu, footer) from partners.html and is
prototype-only until the owner approves it.

    python3 tools/v4_expeditions_c.py
"""
import html
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "partners.html")
OUT = os.path.join(V4, "expeditions-c.html")
WORLD = os.path.join(ROOT, "prototypes", "workspace", "atlas", "data", "world.json")

TITLE = "Expeditions"
DESC = ("Four places to fly with Paragliding Atlas, on one map: Bir Billing in India and Kerio Valley "
        "in Kenya with dates set, Kazakhstan and Peru being planned.")
URL = "https://paraglidingatlas.com/expeditions.html"
OG_IMG = "https://paraglidingatlas.com/assets/destinations/kenya/hero/kerio-valley.jpg"
CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"

A = "../../assets/"

# ---------- the projection: Equal Earth (Savric, Patterson, Jenny 2018), 200 units to the radius ----------
EA1, EA2, EA3, EA4 = 1.340264, -0.081106, 0.000893, 0.003796
EM = math.sqrt(3) / 2
SCALE = 200.0


def ee(lon, lat):
    """Longitude and latitude in degrees to the drawing's x and y (y down)."""
    lam = math.radians(lon)
    th = math.asin(EM * math.sin(math.radians(lat)))
    t2 = th * th
    t6 = t2 * t2 * t2
    x = 2 * math.sqrt(3) * lam * math.cos(th) / (3 * (9 * EA4 * t6 * t2 + 7 * EA3 * t6 + 3 * EA2 * t2 + EA1))
    y = th * (EA1 + EA2 * t2 + t6 * (EA3 + EA4 * t2))
    return SCALE * x, -SCALE * y


def num(v):
    s = "%.1f" % v
    if s in ("-0.0", "0.0"):
        return "0"
    s = s.rstrip("0").rstrip(".")
    if s.startswith("0."):
        s = s[1:]
    elif s.startswith("-0."):
        s = "-" + s[2:]
    return s


def rel_path(pts, close=False):
    """Points to a compact path: one absolute move, then relative lines at a tenth of a unit."""
    q = []
    for x, y in pts:
        p = (round(x * 10), round(y * 10))
        if not q or p != q[-1]:
            q.append(p)
    if close and len(q) > 1 and q[0] == q[-1]:
        q.pop()
    if len(q) < 2:
        return ""
    out = "M%s %s" % (num(q[0][0] / 10.0), num(q[0][1] / 10.0))
    seq = []
    for (ax, ay), (bx, by) in zip(q, q[1:]):
        dx, dy = num((bx - ax) / 10.0), num((by - ay) / 10.0)
        seq.append(dx + ("" if dy.startswith("-") else " ") + dy)
    body = ""
    for s in seq:
        if body and not s.startswith("-"):
            body += " "
        body += s
    return out + "l" + body + ("z" if close else "")


def _fmt_pairs(pairs):
    body = ""
    for dx, dy in pairs:
        for v in (dx, dy):
            t = num(v / 10.0)
            if body and not t.startswith("-"):
                body += " "
            body += t
    return body


def smooth_path(pts, closed):
    """A quadratic B-spline through the polyline (Chaikin's limit curve): the outline's own vertices become the
    control points and the curve runs through the middles of its sides, so a coarse outline reads as drawn,
    not plotted. An open run (a border) starts and ends at the middles of its end sides, which lie on the
    curves of the two countries it divides."""
    q = []
    for x, y in pts:
        p = (round(x * 10), round(y * 10))
        if not q or p != q[-1]:
            q.append(p)
    if closed and len(q) > 1 and q[0] == q[-1]:
        q.pop()
    if len(q) < (3 if closed else 3):
        return rel_path([(a / 10.0, b / 10.0) for a, b in q], close=closed) if len(q) > 1 else ""
    n = len(q)
    mid = lambda a, b: ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
    if closed:
        start = mid(q[-1], q[0])
        verts = [(q[i], mid(q[i], q[(i + 1) % n])) for i in range(n)]
    else:
        start = mid(q[0], q[1])
        verts = [(q[i], mid(q[i], q[i + 1])) for i in range(1, n - 1)]
    out = "M%s %s" % (num(start[0] / 10.0), num(start[1] / 10.0))
    cur, pairs = start, []
    for c, e in verts:
        pairs.append((c[0] - cur[0], c[1] - cur[1]))
        pairs.append((e[0] - cur[0], e[1] - cur[1]))
        cur = e
    return out + "q" + _fmt_pairs(pairs) + ("z" if closed else "")


def dp(pts, tol):
    """Douglas-Peucker, on projected points."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1e-9
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            dd = abs(dy * px - dx * py + bx * ay - by * ax) / L if (dx or dy) else math.hypot(px - ax, py - ay)
            if dd > best:
                best, bi = dd, i
        if best > tol and bi > 0:
            keep[bi] = True
            stack.append((a, bi))
            stack.append((bi, b))
    return [p for p, k in zip(pts, keep) if k]


TOL = 0.45         # simplification, in drawing units (at the closest plate about 2 px)
MIN_AREA = 6.0    # islands smaller than this (square units, a few pixels at the whole world) are left out,
NEAR_DEG = 22     # except within this many degrees of a place, where the plates come close

# ---------- the places, in the order they fly ----------
PLACES = [
    dict(id="india", n="01", name="India", region="Bir Billing, Himalaya", country="India",
         lon=76.72, lat=32.05, co="32.05°N · 76.72°E", status="set", side="r",
         line="Ten days on the Dhauladhar, the wall of the Himalaya above Bir.",
         dates=["15 to 24 Apr 2027", "25 Apr to 4 May 2027", "21 to 30 Oct 2027", "3 to 12 Nov 2027"], state="Guaranteed to run",
         facts=[("Length", "10 days"), ("Group", "6 places"), ("Price", "£1,100 per pilot"),
                ("Rating", "IPPI 2 or equivalent"), ("Season", "April to May, October to November"),
                ("Cloudbase", "3 to 3.6 km on the front range")],
         book=("Hold a place", "enquire.html?trip=india"), more=("The full trip", "destinations/india.html"),
         photo=(A + "destinations/india/hero/dhauladhar", 2400, 1600,
                "The Dhauladhar range under building cumulus, above the Kangra valley", "The Dhauladhar", "50% 62%"),
         month="Oct 2026", near=7.0),
    dict(id="kenya", n="02", name="Kenya", region="Kerio Valley, Rift Valley", country="Kenya",
         lon=35.65, lat=0.72, co="0.72°N · 35.65°E", status="set", side="r",
         line="Kerio Valley is the base, and the site where the world speed records are chased.",
         dates=["18 to 29 Jan 2027", "1 to 12 Feb 2027"], state="Booking open",
         facts=[("Length", "12 days"), ("Group", "8 places"), ("Price", "From US$2,100"),
                ("Rating", "IPPI 2 or equivalent"), ("Season", "December to March"),
                ("Thermals", "4 to 6 m/s at the midday peaks")],
         book=("Hold a place", "enquire.html?trip=kenya"), more=("The full trip", "destinations/kenya.html"),
         photo=(A + "destinations/kenya/hero/kerio-valley", 1152, 768,
                "Three paragliders soaring along a hazy green ridge above terraced fields in the Kerio Valley",
                "Kerio Valley", "55% 60%"),
         month="Jan 2027", near=7.0),
    dict(id="kazakhstan", n="03", name="Kazakhstan", region="The steppe", country="Kazakhstan",
         lon=67.0, lat=48.0, co="", status="planned", side="l",
         line="Beyond roads, beyond maps.",
         dates=[], state="",
         facts=[("Planned", "June 2027"), ("Length", "10 days"), ("Group", "Small group"), ("Price", "From €2,100")],
         book=("Register interest", "enquire.html?trip=kazakhstan"), more=None, photo=None,
         month="Jun 2027", near=0),
    dict(id="peru", n="04", name="Peru", region="Lima and the Andes", country="Peru",
         lon=-77.04, lat=-12.05, co="", status="planned", side="l",
         line="Soar the land of the Incas.",
         dates=[], state="",
         facts=[("Planned", "November 2027"), ("Length", "14 days"), ("Group", "Small group"), ("Price", "From €1,850")],
         book=("Register interest", "enquire.html?trip=peru"), more=None, photo=None,
         month="Nov 2027", near=0),
]
for _p in PLACES:
    _p["x"], _p["y"] = ee(_p["lon"], _p["lat"])

ARROW = ('<svg class="ex-arr" viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M2 7h10M8 3l4 4-4 4" '
         'fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')

def esc(s):
    return html.escape(s, quote=True)


# ---------- the geometry ----------
def load_world():
    world = json.load(open(WORLD, encoding="utf-8"))
    out = []
    for c in world:
        if c["n"] == "Antarctica":
            continue
        rings = []
        for r in c["p"]:
            lon = [r[0][0]]
            for p in r[1:]:
                v = p[0]
                while v - lon[-1] > 180:
                    v -= 360
                while v - lon[-1] < -180:
                    v += 360
                lon.append(v)
            mean = sum(lon) / len(lon)
            if mean > 180:
                lon = [v - 360 for v in lon]
            elif mean < -180:
                lon = [v + 360 for v in lon]
            rings.append([(max(-180.0, min(180.0, a)), p[1], (p[0], p[1])) for a, p in zip(lon, r)])
        out.append((c["n"], rings))
    return out


def area(pts):
    return abs(sum(ax * by - bx * ay for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]))) / 2


def geometry():
    """The countries as filled shapes (their edges stroked as coast), and the borders: the edges two countries
    share, each drawn once. Islands smaller than a pixel at the whole world's scale are left out."""
    world = load_world()
    seg = {}
    for _, rings in world:
        for r in rings:
            for a, b in zip(r, r[1:] + r[:1]):
                k = tuple(sorted((a[2], b[2])))
                seg[k] = seg.get(k, 0) + 1
    land, hl, borders = [], {}, []
    done = set()
    # one path per country (and per country's share of the borders), so the browser can skip what is off the plate
    trip = [p["country"] for p in PLACES]
    for name, rings in world:
        dpath, bpath = "", ""
        for r in rings:
            pts = [ee(a, b) for a, b, _ in r]
            if area(pts) < MIN_AREA and name not in trip:
                lo = sum(a for a, _, _ in r) / len(r)
                la = sum(b for _, b, _ in r) / len(r)
                if not any(abs(lo - p["lon"]) < NEAR_DEG and abs(la - p["lat"]) < NEAR_DEG for p in PLACES):
                    continue
            dpath += smooth_path(dp(pts + [pts[0]], TOL), True)
            n = len(r)
            run = []
            for j in range(n + 1):
                i = j % n
                a, b = r[i], r[(i + 1) % n]
                k = tuple(sorted((a[2], b[2])))
                shared = j < n and seg.get(k, 0) >= 2 and k not in done
                if shared:
                    done.add(k)
                    if not run:
                        run = [i]
                    run.append((i + 1) % n)
                elif run:
                    bpath += smooth_path(dp([ee(r[q][0], r[q][1]) for q in run], TOL), False)
                    run = []
        if bpath:
            borders.append(bpath)
        if name in trip:
            hl[name] = dpath
        elif dpath:
            land.append(dpath)
    return land, hl, borders


def graticule():
    """Every 30 degrees across the world; every 5 degrees (seen only on the close plates) where the places are."""
    major, minor = [], []
    for lon in range(-150, 151, 30):
        major.append(rel_path([ee(lon, lat) for lat in range(-85, 86, 5)]))
    for lat in (-60, -30, 30, 60):
        major.append(rel_path([ee(-180, lat), ee(180, lat)]))
    for lon in range(-110, 111, 5):
        if lon % 30:
            minor.append(rel_path([ee(lon, lat) for lat in range(-50, 71, 10)]))
    for lat in range(-50, 71, 5):
        if lat % 30:
            minor.append(rel_path([ee(-110, lat), ee(110, lat)]))
    edge = [ee(-180, lat / 2.0) for lat in range(-180, 181, 3)] + [ee(180, lat / 2.0) for lat in range(180, -181, -3)]
    eq = rel_path([ee(-180, 0), ee(180, 0)])
    return "".join(major), "".join(minor), rel_path(edge, close=True), eq


def bbox_of(country):
    world = json.load(open(WORLD, encoding="utf-8"))
    c = [x for x in world if x["n"] == country][0]
    pts = [ee(p[0], p[1]) for r in c["p"] for p in r]
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]


def r1(v):
    return round(v, 1)


# the overview: the whole world but Antarctica, with a little sea round it
_top = ee(0, 84.5)[1]
_bot = ee(0, -58.0)[1]
_xw = ee(180, 0)[0]
OVER = [r1(-_xw - 6), r1(_top - 6), r1(2 * _xw + 12), r1(_bot - _top + 12)]


def frames():
    """The stage's stops: what to fit (a box in drawing units) and where on the stage to fit it (fractions)."""
    world = [r1(-_xw), r1(_top), r1(_xw), r1(_bot)]
    out = [dict(id="intro", box=world, reg=[.35, 1.05, .12, .92])]
    for p in PLACES:
        if p["photo"]:
            k = p["near"] * 3.0          # about 3 units a degree near the equator
            box = [p["x"] - k, p["y"] - k, p["x"] + k, p["y"] + k]
            reg = [.43, .6, .3, .74]
        else:
            b = bbox_of(p["country"])
            m = 8
            box = [b[0] - m, b[1] - m, b[2] + m, b[3] + m]
            reg = [.47, .93, .18, .86]
        out.append(dict(id=p["id"], box=[r1(v) for v in box], reg=reg, x=r1(p["x"]), y=r1(p["y"]),
                        photo=bool(p["photo"])))
    out.append(dict(id="outro", box=world, reg=[.35, 1.05, .12, .92]))
    return out


def inset_box(p):
    """A place's plate on phones: the place a little above the middle, its country round it."""
    if p["photo"]:
        k = 26.0
        w, h = 2 * k * 1.6, 2 * k
        return [r1(p["x"] - w / 2), r1(p["y"] - h * .42), r1(w), r1(h)]
    b = bbox_of(p["country"])
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    w = max(b[2] - b[0], (b[3] - b[1]) * 1.25) * 1.5
    h = w / 1.25
    return [r1(cx - w / 2), r1(cy - h / 2), r1(w), r1(h)]


# ---------- the markup ----------
def pct(v, a, n):
    return "%.2f%%" % ((v - a) / n * 100)


def pin(p, i):
    kind = "is-set" if p["status"] == "set" else "is-planned"
    when = ("next " + p["dates"][0]) if p["dates"] else ("planned " + [f[1] for f in p["facts"] if f[0] == "Planned"][0])
    return ('<a class="ex-pin %s is-%s" href="#%s" data-i="%d" style="--x:%s;--y:%s" aria-label="%s, %s, %s">'
            '<i class="ex-dot" aria-hidden="true"></i><span class="ex-pl" aria-hidden="true">%s</span></a>'
            % (kind, p["side"], p["id"], i + 1, pct(p["x"], OVER[0], OVER[2]), pct(p["y"], OVER[1], OVER[3]),
               esc(p["name"]), esc(p["region"]), esc(when), esc(p["name"])))


def map_svg():
    land, hl, borders = geometry()
    major, minor, edge, eq = graticule()
    hlp = "".join('<path class="ex-c ex-c-%s" d="%s"/>' % (p["id"], hl[p["country"]]) for p in PLACES)
    hlo = "".join('<path class="ex-o ex-o-%s" d="%s"/>' % (p["id"], hl[p["country"]]) for p in PLACES)
    # the borders twice: once in the land's own colour over the coast strokes the two countries' edges leave
    # there, once as the border itself
    return ('<svg class="ex-map" viewBox="%s" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">'
            '<g id="ex-geo"><path class="ex-sea" d="%s"/><path class="ex-g5" d="%s"/><path class="ex-g30" d="%s"/>'
            '<path class="ex-eq" d="%s"/><g class="ex-land">%s</g>%s<g class="ex-bd" id="ex-bd">%s</g>'
            '<use class="ex-bdu" href="#ex-bd"/><g class="ex-night" clip-path="url(#ex-clip)"></g>%s'
            '<path class="ex-edge" d="%s"/></g><defs><clipPath id="ex-clip"><path d="%s"/></clipPath></defs></svg>'
            % (" ".join(num(v) for v in OVER), edge, minor, major, eq,
               "".join('<path class="ex-l" d="%s"/>' % d for d in land), hlp,
               "".join('<path class="ex-b" d="%s"/>' % d for d in borders), hlo, edge, edge))


def legend_key():
    return ('<p class="ex-key" aria-hidden="true"><span><i class="ex-dot is-set"></i>Dates set</span>'
            '<span><i class="ex-dot is-planned"></i>Planned</span>'
            '<span class="ex-key-night"><i class="ex-nsw"></i>Night, now</span></p>')


def intro():
    idx = "".join('<li><a href="#%s"><span class="ex-ix-n">%s</span> <span class="ex-ix-t">%s</span> '
                  '<span class="ex-ix-m">%s</span></a></li>' % (p["id"], p["n"], esc(p["name"]), esc(p["month"]))
                  for p in PLACES)
    return ('<div class="ex-stop ex-intro is-on" data-i="0"><div class="ex-panel">'
            '<p class="ex-kicker">Expeditions</p>'
            '<h1 class="ex-h1">Choose Your Sky</h1>'
            '<p class="ex-lead">Two expeditions with dates set and two being planned. Pick a place on the map.</p>'
            '<nav class="ex-ix" aria-label="The four places"><ol>%s</ol></nav>'
            '</div></div>' % idx)


def plate():
    pins = "".join(pin(p, i) for i, p in enumerate(PLACES))
    return ('<figure class="ex-plate" aria-label="Map of the four places">%s<div class="ex-pins">%s</div>'
            '<div class="ex-photos"></div>'
            '<figcaption class="ex-cap">%s<span class="ex-credit">Equal Earth projection, Natural Earth outlines</span>'
            '</figcaption></figure>' % (map_svg(), pins, legend_key()))


def picture(p, lazy=True):
    base, w, h, alt, cap, pos = p["photo"]
    return ('<figure class="ex-photo" style="--pos:%s"><picture><source srcset="%s.webp" type="image/webp">'
            '<img src="%s.jpg" width="%d" height="%d" alt="%s"%s></picture><figcaption>%s</figcaption></figure>'
            % (pos, base, base, w, h, esc(alt), ' loading="lazy" decoding="async"' if lazy else "", esc(cap)))


def inset(p):
    vb = inset_box(p)
    kind = "is-set" if p["status"] == "set" else "is-planned"
    x, y = pct(p["x"], vb[0], vb[2]), pct(p["y"], vb[1], vb[3])
    co = '<span class="ex-ico">%s</span>' % esc(p["co"] or "Planned")
    return ('<div class="ex-inset%s" style="--ar:%s;--av:%s">'
            '<svg viewBox="%s" preserveAspectRatio="xMidYMid slice" data-on="%s" aria-hidden="true" focusable="false">'
            '<use href="#ex-geo"/></svg>'
            '<span class="ex-imark %s" style="--x:%s;--y:%s" aria-hidden="true"><i class="ex-dot %s"></i>%s</span></div>'
            % (" has-photo" if p["photo"] else "", "%g / %g" % (vb[2], vb[3]), "%.4f" % (vb[2] / vb[3]),
               " ".join(num(v) for v in vb), p["id"],
               kind, x, y, kind, co))


def stop(p, i):
    if p["dates"]:
        when = ('<div class="ex-when"><span class="ex-l">Departures</span><p>%s</p>'
                '<p class="ex-state"><i aria-hidden="true"></i>%s</p></div>'
                % ("".join('<span>%s</span>' % esc(d) for d in p["dates"]), esc(p["state"])))
    else:
        when = ""
    facts = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(k), esc(v)) for k, v in p["facts"])
    acts = '<a class="btn-solid ex-book" href="%s"><span>%s</span></a>' % (p["book"][1], esc(p["book"][0]))
    if p["more"]:
        acts += '<a class="ex-more" href="%s">%s%s</a>' % (p["more"][1], esc(p["more"][0]), ARROW)
    media = inset(p) + (picture(p) if p["photo"] else "")
    return ('<article class="ex-stop ex-place is-%s" id="%s" data-i="%d" aria-labelledby="%s-h">'
            '<div class="ex-media">%s</div>'
            '<div class="ex-panel">'
            '<p class="ex-label"><span>%s</span> %s</p>'
            '<h2 class="ex-name" id="%s-h">%s</h2>'
            '%s'
            '<p class="ex-line">%s</p>'
            '%s<dl class="ex-facts">%s</dl>'
            '<div class="ex-acts">%s</div>'
            '</div></article>'
            % (p["status"], p["id"], i + 1, p["id"], media, p["n"], esc(p["region"]), p["id"], esc(p["name"]),
               ('<p class="ex-co">%s</p>' % esc(p["co"])) if p["co"] else "",
               esc(p["line"]), when, facts, acts))


def outro():
    return ('<div class="ex-stop ex-outro" data-i="%d"><div class="ex-panel">'
            '<h2 class="ex-h2">Still Choosing?</h2>'
            '<p class="ex-lead">Book a free 30-minute call, or send an enquiry.</p>'
            '<div class="ex-acts"><a class="btn-solid" href="%s" target="_blank" rel="noopener"><span>Book a call</span></a>'
            '<a class="ex-more" href="enquire.html">Enquire%s</a></div>'
            '</div></div>' % (len(PLACES) + 1, CALL, ARROW))


def index_bar():
    items = "".join('<a href="#%s" data-i="%d"><span>%s</span> %s</a>' % (p["id"], i + 1, p["n"], esc(p["name"]))
                    for i, p in enumerate(PLACES))
    return '<nav class="ex-bar" aria-label="Places on the map">%s</nav>' % items


EARLY = ('<script>(function(r,m){r.classList.add("ex-js");'
         'if(m("(min-width: 1000px) and (min-height: 620px)").matches&&!m("(prefers-reduced-motion: reduce)").matches)'
         'r.classList.add("ex-fly");'
         'var s=r.style,o=s.setProperty;s.setProperty=function(k){if(k!=="--v2-gust")return o.apply(s,arguments);};'
         '})(document.documentElement,function(q){return window.matchMedia(q);});</script>')


def data_attr():
    d = dict(over=OVER, stops=frames(), k=SCALE)
    return esc(json.dumps(d, separators=(",", ":")))


def main_html():
    return ('<main id="v4-main" class="ex">\n' + EARLY
            + '<div class="ex-atlas" data-ex="%s" style="--n:%d">' % (data_attr(), len(PLACES) + 2)
            + '<div class="ex-stage">' + intro() + plate()
            + "".join(stop(p, i) for i, p in enumerate(PLACES)) + outro() + index_bar()
            + '</div></div>\n</main>')


# ---------- the styles ----------
def ease_stops(p0, p1, a0, a1, n=8, col="var(--bg)"):
    """Gradient stops for a smoothstep from opacity a0 at p0% to a1 at p1% (no knee at either end)."""
    out = []
    for i in range(n + 1):
        t = i / float(n)
        a = a0 + (a1 - a0) * t * t * (3 - 2 * t)
        p = "%g%%" % round(p0 + (p1 - p0) * t, 2)
        if a <= 0.0005:
            out.append("transparent " + p)
        elif a >= 0.9995:
            out.append(col + " " + p)
        else:
            out.append("color-mix(in srgb,%s %g%%,transparent) %s" % (col, round(a * 100, 1), p))
    return ",".join(out)


def mask_v(*parts):
    return "linear-gradient(180deg,%s)" % ",".join(parts)


def mask_h(*parts):
    return "linear-gradient(90deg,%s)" % ",".join(parts)


K = "var(--ink)"   # a mask only reads alpha; any opaque token will do
# the stage photograph: in from the left over most of its width, out at the top and the foot
PH_H = mask_h(ease_stops(0, 52, 0, 1, 10, K), "%s 100%%" % K)
PH_V = mask_v(ease_stops(0, 26, 0, 1, 8, K), ease_stops(70, 100, 1, 0, 8, K))
# the phone photograph: rising out of the plate above it, settling into the page below
PP_V = mask_v(ease_stops(0, 42, 0, 1, 10, K), ease_stops(72, 100, 1, 0, 8, K))
# the plate: dissolving at its foot into the photograph (or the page), and softly at its top
PL_V = mask_v(ease_stops(0, 16, 0, 1, 6, K), ease_stops(58, 100, 1, 0, 10, K))
PL_V2 = mask_v(ease_stops(0, 14, 0, 1, 6, K), ease_stops(76, 100, 1, 0, 8, K))
# the stage's left shade, for the words
SHADE = mask_h(ease_stops(0, 46, .9, 0, 10, "var(--bg)"))
SHADE_FOOT = mask_v("transparent 0%", ease_stops(72, 100, 0, .85, 8, "var(--bg)"))

CSS = r"""
/* ===== Expeditions, option C: the atlas (tools/v4_expeditions_c.py) ===== */
@property --ex-r{syntax:"<percentage>";inherits:false;initial-value:0%;}
.ex{--ex-x:var(--edge-x,var(--gutter));
  --ex-land:color-mix(in srgb,var(--white) 3%,var(--card));
  --ex-land-hi:color-mix(in srgb,var(--white) 9%,var(--card));
  --ex-sea:color-mix(in srgb,var(--sky-cool) 45%,var(--bg));
  --ex-coast:color-mix(in srgb,var(--white) 30%,transparent);
  --ex-border:color-mix(in srgb,var(--white) 13%,transparent);
  --ex-grat:color-mix(in srgb,var(--white) 7%,transparent);
  --ex-rim:color-mix(in srgb,var(--orange) 60%,transparent);
  --ex-muted:color-mix(in srgb,var(--gray-light) 40%,var(--gray));
  --ex-name:min(6vw,6.6rem);
  position:relative;overflow-x:clip;}
@media (max-width:560px){.ex{--ex-x:var(--sp-2);}}
.ex-atlas{position:relative;}

/* ---- the map's drawing (the trip pages' route map language) ---- */
.ex-map{display:block;width:100%;height:100%;overflow:visible;}
.ex-sea,.ex-edge,.ex-g30,.ex-g5,.ex-eq,.ex-land,.ex-c,.ex-bd,.ex-o{vector-effect:non-scaling-stroke;}
.ex-sea{fill:var(--ex-sea);stroke:none;}
.ex-edge{fill:none;stroke:var(--ex-grat);stroke-width:1;}
.ex-g30{fill:none;stroke:var(--ex-grat);stroke-width:.8;}
.ex-g5{fill:none;stroke:color-mix(in srgb,var(--white) 4%,transparent);stroke-width:.6;opacity:var(--ex-fine,0);transition:opacity .9s var(--ease);}
.ex-eq{fill:none;stroke:color-mix(in srgb,var(--white) 16%,transparent);stroke-width:.8;stroke-dasharray:5 5;}
.ex-land{fill:var(--ex-land);stroke:var(--ex-coast);stroke-width:.8;stroke-linejoin:round;}
.ex-l,.ex-b{vector-effect:non-scaling-stroke;}
.ex-c{fill:var(--ex-land);stroke:var(--ex-coast);stroke-width:.8;stroke-linejoin:round;transition:fill .9s var(--ease);}
.ex-bd{fill:none;stroke:var(--ex-bdc,var(--ex-land));stroke-width:var(--ex-bdw,1.6);stroke-dasharray:var(--ex-bdd,none);stroke-linecap:round;}
.ex-bdu{--ex-bdc:var(--ex-border);--ex-bdw:.7;--ex-bdd:2 3;}
.ex-o{fill:none;stroke:transparent;stroke-width:1;stroke-linejoin:round;transition:stroke .9s var(--ease);}
/* inside a plate (an svg <use>), the place's country is lit through inherited properties */
.ex-c-india{fill:var(--ex-hl-india,var(--ex-land));}.ex-o-india{stroke:var(--ex-ol-india,transparent);}
.ex-c-kenya{fill:var(--ex-hl-kenya,var(--ex-land));}.ex-o-kenya{stroke:var(--ex-ol-kenya,transparent);}
.ex-c-kazakhstan{fill:var(--ex-hl-kazakhstan,var(--ex-land));}.ex-o-kazakhstan{stroke:var(--ex-ol-kazakhstan,transparent);}
.ex-c-peru{fill:var(--ex-hl-peru,var(--ex-land));}.ex-o-peru{stroke:var(--ex-ol-peru,transparent);}
.ex-map[data-hint="india"],.ex-map[data-on="india"],.ex-inset svg[data-on="india"]{--ex-hl-india:var(--ex-land-hi);--ex-ol-india:var(--ex-rim);}
.ex-map[data-hint="kenya"],.ex-map[data-on="kenya"],.ex-inset svg[data-on="kenya"]{--ex-hl-kenya:var(--ex-land-hi);--ex-ol-kenya:var(--ex-rim);}
.ex-map[data-hint="kazakhstan"],.ex-map[data-on="kazakhstan"],.ex-inset svg[data-on="kazakhstan"]{--ex-hl-kazakhstan:var(--ex-land-hi);--ex-ol-kazakhstan:var(--ex-rim);}
.ex-map[data-hint="peru"],.ex-map[data-on="peru"],.ex-inset svg[data-on="peru"]{--ex-hl-peru:var(--ex-land-hi);--ex-ol-peru:var(--ex-rim);}
.ex-inset svg{--ex-fine:1;}

/* ---- markers: a small ring, filled where the dates are set, open where the trip is planned ---- */
.ex-dot{display:block;flex:none;width:9px;height:9px;border-radius:50%;box-sizing:border-box;
  background:var(--orange);border:1.5px solid var(--orange);}
.ex-dot.is-planned,.is-planned>.ex-dot{background:var(--bg);border-color:var(--white);}
.ex-pins{position:absolute;inset:0;pointer-events:none;}
.ex-pin{position:absolute;left:var(--x);top:var(--y);display:flex;align-items:center;gap:.55rem;min-height:44px;
  padding:0 .6rem;margin:-22px 0 0 calc(-.6rem - 4.5px);color:var(--gray-light);text-decoration:none;pointer-events:auto;
  font:600 var(--fs-micro)/1 var(--font-body);letter-spacing:.16em;text-transform:uppercase;white-space:nowrap;}
.ex-pin.is-l{flex-direction:row-reverse;margin-left:calc(.6rem + 4.5px);transform:translateX(-100%);}
.ex-pin .ex-dot{position:relative;}
.ex-pin .ex-dot::after{content:"";position:absolute;inset:-9px;border-radius:50%;border:1px solid var(--orange);
  opacity:0;scale:.6;transition:opacity .6s var(--ease),scale .6s var(--ease);}
.ex-pin:is(:hover,:focus-visible){color:var(--white);}
.ex-pin:is(:hover,:focus-visible) .ex-dot::after,.ex-pin:is(.is-on,.is-hint) .ex-dot::after{opacity:1;scale:1;}
.ex-pin.is-hint{color:var(--white);}
.ex-ix a.is-hint .ex-ix-t{color:var(--orange);}
.ex-pin.is-on{color:var(--white);}
.ex-pin:focus-visible{outline:none;}
.ex-pin:focus-visible .ex-pl{outline:2px solid var(--orange);outline-offset:4px;}
.ex-pl{text-shadow:0 0 6px var(--bg),0 0 2px var(--bg);}

/* ---- the words ---- */
.ex-kicker{margin:0 0 var(--sp-2);font:600 var(--fs-micro)/1.2 var(--font-body);letter-spacing:.18em;text-transform:uppercase;color:var(--orange);}
.ex-h1{margin:0;font:700 min(calc(var(--fs-display) * 1.45),15vw)/.98 var(--font-display);letter-spacing:-.035em;color:var(--white);text-wrap:balance;}
.ex-h2{margin:0;font:700 var(--fs-h1)/1.04 var(--font-display);letter-spacing:-.025em;color:var(--white);}
.ex-lead{margin:var(--sp-3) 0 0;max-width:34ch;font-size:calc(var(--fs-lead) * 1.1);line-height:1.6;color:var(--gray-light);}
.ex-label{display:flex;gap:.8rem;align-items:baseline;margin:0 0 var(--sp-1);font:600 var(--fs-micro)/1.3 var(--font-body);
  letter-spacing:.16em;text-transform:uppercase;color:var(--gray);}
.ex-label span{font-variant-numeric:tabular-nums;color:var(--ex-muted);}
.ex-name{margin:0;font:700 var(--ex-name)/.95 var(--font-display);letter-spacing:-.04em;color:var(--white);}
.ex-co{margin:var(--sp-1) 0 0;font:500 var(--fs-small)/1.4 var(--font-body);letter-spacing:.08em;color:var(--gray);font-variant-numeric:tabular-nums;}
.ex-line{margin:var(--sp-3) 0 0;max-width:30ch;font-size:calc(var(--fs-lead) * 1.12);line-height:1.55;color:var(--gray-light);text-wrap:pretty;}
.ex-l,.ex-facts dt{display:block;font:600 var(--fs-micro)/1.3 var(--font-body);letter-spacing:.14em;text-transform:uppercase;color:var(--gray);}
.ex-when{margin:var(--sp-4) 0 0;padding:var(--sp-2) 0 0;border-top:1px solid var(--line);}
.ex-when p{margin:.35rem 0 0;display:flex;flex-wrap:wrap;gap:.2rem 1.4rem;font:600 var(--fs-h4)/1.4 var(--font-display);color:var(--white);font-variant-numeric:tabular-nums;}
.ex-when .ex-state{gap:.55rem;align-items:center;font:500 var(--fs-small)/1.4 var(--font-body);color:var(--gray-light);}
.ex-state i{width:6px;height:6px;border-radius:50%;background:var(--orange);}
.ex-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 var(--sp-3);margin:var(--sp-2) 0 0;}
.ex-facts div{padding:.7rem 0;border-top:1px solid var(--line);min-width:0;}
.ex-facts dd{margin:.25rem 0 0;font-size:var(--fs-body-s);line-height:1.4;color:var(--white);font-variant-numeric:tabular-nums;}
.is-planned .ex-facts{margin-top:var(--sp-4);}
.ex-acts{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-2) var(--sp-4);margin:var(--sp-4) 0 0;}
.ex-acts .btn-solid{min-height:44px;box-sizing:border-box;display:inline-flex;align-items:center;}
.ex-more{display:inline-flex;align-items:center;gap:.5rem;min-height:44px;color:var(--white);text-decoration:none;font-weight:500;
  border-bottom:1px solid var(--edge-hi);transition:border-color .3s var(--ease),color .3s var(--ease);}
.ex-more:is(:hover,:focus-visible){border-color:var(--orange);}
.ex-arr{width:14px;height:14px;flex:none;transition:translate .3s var(--ease);}
.ex-more:is(:hover,:focus-visible) .ex-arr{translate:3px 0;}
.ex-key{display:flex;flex-wrap:wrap;gap:.3rem var(--sp-3);margin:0;font:500 var(--fs-micro)/1.3 var(--font-body);letter-spacing:.06em;color:var(--ex-muted);text-shadow:0 0 6px var(--bg);}
.ex-key span{display:inline-flex;align-items:center;gap:.5rem;}
.ex-key .ex-dot{width:8px;height:8px;}
.ex-credit{font:400 var(--fs-micro)/1.3 var(--font-body);color:var(--ex-muted);text-shadow:0 0 6px var(--bg);}
/* night, now: the real night on the map at the moment the page is opened, deepening in seven steps of three
   degrees from sunset to the end of astronomical twilight, drawn once by the script */
.ex-night path{fill:color-mix(in srgb,var(--bg) 7%,transparent);stroke:none;}
.ex-key-night{display:none !important;}
.ex-has-night .ex-key-night{display:inline-flex !important;}
.ex-nsw{display:block;width:12px;height:8px;border-radius:2px;background:linear-gradient(90deg,var(--ex-land) 0 50%,color-mix(in srgb,var(--bg) 55%,var(--ex-land)) 50% 100%);box-shadow:inset 0 0 0 1px var(--line);}

/* the index of places */
.ex-ix{margin:var(--sp-4) 0 0;}
.ex-ix ol{list-style:none;margin:0;padding:0;border-top:1px solid var(--line);max-width:24rem;}
.ex-ix li{border-bottom:1px solid var(--line);}
.ex-ix a{display:grid;grid-template-columns:2.2rem 1fr auto;align-items:center;min-height:48px;color:var(--white);text-decoration:none;
  transition:color .3s var(--ease);}
.ex-ix-n{font:600 var(--fs-micro)/1 var(--font-body);letter-spacing:.14em;color:var(--gray);font-variant-numeric:tabular-nums;}
.ex-ix-t{font:600 var(--fs-body)/1.2 var(--font-display);}
.ex-ix-m{font-size:var(--fs-small);color:var(--gray);font-variant-numeric:tabular-nums;}
.ex-ix a:is(:hover,:focus-visible) .ex-ix-t{color:var(--orange);}

/* ---- the photographs ---- */
.ex-photo{margin:0;position:relative;}
.ex-photo img{display:block;width:100%;height:100%;object-fit:cover;object-position:var(--pos,50% 50%);}
.ex-photo figcaption{position:absolute;right:var(--ex-x);bottom:var(--sp-2);font:500 var(--fs-micro)/1.3 var(--font-body);
  letter-spacing:.12em;text-transform:uppercase;color:var(--white);text-shadow:0 0 3px var(--bg),0 0 10px var(--bg),0 0 18px var(--bg);}

/* ======== the vertical journey: phones, tablets, reduced motion and no script ======== */
.ex-stage{display:flex;flex-direction:column;}
.ex-intro{order:0;padding:clamp(1.5rem,6vw,4rem) var(--ex-x) 0;}
/* the opening on the journey: the words, then the map, then the places as a list */
html:not(.ex-fly) .ex-intro,html:not(.ex-fly) .ex-intro .ex-panel{display:contents;}
html:not(.ex-fly) .ex-intro .ex-kicker{order:0;margin:clamp(1.5rem,6vw,4rem) var(--ex-x) var(--sp-2);}
html:not(.ex-fly) .ex-intro .ex-h1{order:0;margin:0 var(--ex-x);}
html:not(.ex-fly) .ex-intro .ex-lead{order:0;margin:var(--sp-3) var(--ex-x) 0;}
html:not(.ex-fly) .ex-intro .ex-ix{order:2;margin:calc(var(--sp-5) + var(--sp-3)) var(--ex-x) 0;}
html:not(.ex-fly) .ex-co{display:none;}
.ex-plate{order:1;position:relative;margin:var(--sp-4) 0 0;aspect-ratio:@@OVER_AR@@;max-width:1400px;width:100%;align-self:center;}
.ex-plate .ex-map{position:absolute;inset:0;}
.ex-cap{position:absolute;left:var(--ex-x);right:var(--ex-x);bottom:calc(-1 * var(--sp-4));display:flex;flex-wrap:wrap;justify-content:space-between;gap:.4rem var(--sp-3);}
.ex-photos{display:none;}
.ex-place{order:3;margin:clamp(4.5rem,12vw,8rem) 0 0;}
.ex-outro{order:4;padding:clamp(4.5rem,12vw,8rem) var(--ex-x) var(--sp-section);}
.ex-bar{display:none;}
.ex-media{position:relative;}
.ex-inset{position:relative;aspect-ratio:var(--ar);-webkit-mask-image:@@PL_V2@@;mask-image:@@PL_V2@@;}
.ex-inset.has-photo{-webkit-mask-image:@@PL_V@@;mask-image:@@PL_V@@;}
.ex-inset svg{position:absolute;inset:0;width:100%;height:100%;}
.ex-imark{position:absolute;left:var(--x);top:calc(50% + (var(--y) - 50%) * var(--ac,var(--av)) / var(--av));display:flex;align-items:center;gap:.6rem;margin:-4.5px 0 0 -4.5px;
  font:500 var(--fs-micro)/1 var(--font-body);letter-spacing:.1em;color:var(--gray-light);white-space:nowrap;font-variant-numeric:tabular-nums;}
.ex-imark .ex-dot{box-shadow:0 0 0 9px color-mix(in srgb,var(--orange) 14%,transparent);}
.ex-imark.is-planned .ex-dot{box-shadow:0 0 0 9px color-mix(in srgb,var(--white) 8%,transparent);}
.ex-media .ex-photo{margin-top:-24%;aspect-ratio:3 / 2;-webkit-mask-image:@@PP_V@@;mask-image:@@PP_V@@;}
.ex-media .ex-photo figcaption{bottom:22%;}
.ex-place .ex-panel{padding:0 var(--ex-x);margin-top:var(--sp-3);}
.ex-place.is-planned .ex-panel{margin-top:0;}
@media (max-width:999px){
  .ex-plate{margin-top:var(--sp-5);}
  .ex-pin{font-size:calc(var(--fs-micro) * .92);letter-spacing:.12em;}
}
@media (max-width:560px){
  .ex-pin{padding:0 .45rem;margin-left:calc(-.45rem - 4.5px);gap:.4rem;letter-spacing:.1em;}
  .ex-pin.is-l{margin-left:calc(.45rem + 4.5px);}
  .ex-cap{bottom:calc(-1 * var(--sp-5));}
  .ex-credit{display:none;}
  .ex-name{--ex-name:min(14.5vw,4.6rem);}
  .ex-place .ex-panel{margin-top:var(--sp-2);}
}
@media (min-width:700px) and (max-width:999px){
  .ex-place .ex-panel{max-width:40rem;}
  .ex-inset{--ac:2.2;aspect-ratio:2.2;}
  .ex-inset:not(.has-photo){--ac:1.9;aspect-ratio:1.9;}
  .ex-media .ex-photo{aspect-ratio:16 / 9;margin-top:-16%;}
}
/* wide screens without the pinned atlas: each place's words beside its plate and photograph */
@media (min-width:1000px){
  html:not(.ex-fly) .ex-place{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:center;gap:var(--sp-5);
    padding-left:var(--ex-x);}
  html:not(.ex-fly) .ex-place .ex-media{order:2;}
  html:not(.ex-fly) .ex-place .ex-panel{order:1;padding:0;margin:0;}
  html:not(.ex-fly) .ex-intro .ex-panel{max-width:44rem;}
}

/* ======== the pinned atlas: wide screens, with the script, without reduced motion ======== */
.ex-fly .ex-atlas{height:calc(100svh + (var(--n) - 1) * 88svh);}
.ex-fly .ex-stage{display:block;position:sticky;top:0;height:100svh;overflow:hidden;}
.ex-fly:not(.ex-ready) :is(.ex-map,.ex-pins,.ex-cap){visibility:hidden;}
.ex-fly .ex-plate{position:absolute;inset:0;margin:0;aspect-ratio:auto;max-width:none;align-self:stretch;width:auto;}
.ex-fly .ex-plate::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
  background:@@SHADE@@,@@SHADE_FOOT@@;}
.ex-fly .ex-pins{z-index:3;}
.ex-fly .ex-pin{left:0;top:0;opacity:0;transition:opacity .5s var(--ease),color .3s var(--ease);will-change:transform;}
.ex-fly.ex-ready .ex-pin{opacity:1;}
.ex-fly .ex-pin.is-off{opacity:0;pointer-events:none;}
.ex-fly .ex-cap{left:auto;right:var(--ex-x);bottom:var(--sp-3);z-index:4;flex-direction:column;align-items:flex-end;gap:.5rem;}
.ex-fly .ex-photos{display:block;position:absolute;inset:0 0 0 40%;z-index:1;pointer-events:none;}
.ex-fly .ex-photos .ex-photo{position:absolute;inset:0;opacity:0;
  -webkit-mask-image:@@PH_H@@,@@PH_V@@;-webkit-mask-composite:source-in;
  mask-image:@@PH_H@@,@@PH_V@@;mask-composite:intersect;
  transition:opacity .7s var(--ease),visibility 0s linear .7s;visibility:hidden;}
.ex-fly .ex-photos .ex-photo picture{position:absolute;inset:0;display:block;
  -webkit-mask-image:radial-gradient(circle farthest-corner at var(--mx,20%) var(--my,50%),var(--ink) calc(var(--ex-r) * .55),transparent var(--ex-r));
  mask-image:radial-gradient(circle farthest-corner at var(--mx,20%) var(--my,50%),var(--ink) calc(var(--ex-r) * .55),transparent var(--ex-r));
  --ex-r:18%;transition:--ex-r 1.6s var(--ease);}
.ex-fly .ex-photos .ex-photo.is-on{opacity:1;visibility:visible;transition:opacity 1.1s var(--ease),visibility 0s;}
.ex-fly .ex-photos .ex-photo.is-on picture{--ex-r:150%;}
.ex-fly .ex-photos figcaption{right:var(--ex-x);bottom:33%;}
.ex-fly .ex-media{display:none;}
.ex-fly .ex-stop{position:absolute;left:0;top:0;bottom:0;z-index:5;display:flex;align-items:center;
  width:calc(var(--ex-x) + min(30rem,36vw));padding:96px 0 88px var(--ex-x);box-sizing:border-box;margin:0;
  opacity:0;pointer-events:none;transition:opacity .3s var(--ease);}
.ex-fly .ex-stop.is-on{opacity:1;pointer-events:auto;transition:opacity .7s var(--ease) .28s;}
.ex-fly .ex-intro{width:calc(var(--ex-x) + min(36rem,40vw));}
.ex-fly .ex-panel{width:100%;margin:0;padding:0;}
.ex-fly .ex-name{font-size:var(--ex-name);}
.ex-fly .ex-bar{display:flex;gap:0 var(--sp-3);position:absolute;left:var(--ex-x);bottom:var(--sp-2);z-index:6;}
.ex-bar a{display:inline-flex;align-items:center;gap:.5rem;min-height:44px;padding:0 .1rem;color:var(--gray);text-decoration:none;
  font:500 var(--fs-small)/1 var(--font-body);border-bottom:1px solid transparent;transition:color .3s var(--ease),border-color .3s var(--ease);}
.ex-bar a span{font:600 var(--fs-micro)/1 var(--font-body);letter-spacing:.12em;font-variant-numeric:tabular-nums;color:var(--ex-muted);}
.ex-bar a:is(:hover,:focus-visible){color:var(--white);}
.ex-bar a.is-on{color:var(--white);border-bottom-color:var(--orange);}
.ex-fly .ex-bar.is-quiet:not(:focus-within){opacity:0;pointer-events:none;}
.ex-fly .ex-bar{transition:opacity .6s var(--ease);}

@media (prefers-reduced-motion:reduce){
  .ex *{transition:none !important;}
}
"""


def css():
    s = CSS
    for k, v in (("OVER_AR", "%g / %g" % (OVER[2], OVER[3])), ("PH_H", PH_H), ("PH_V", PH_V), ("PP_V", PP_V),
                 ("PL_V2", PL_V2), ("PL_V", PL_V), ("SHADE_FOOT", SHADE_FOOT), ("SHADE", SHADE)):
        s = s.replace("@@%s@@" % k, v)
    return s


SCRIPT = r"""<script>
/* Expeditions, option C (tools/v4_expeditions_c.py). On wide screens the
   stage holds still and the scroll flies the atlas between the places: each
   move is the van Wijk and Nuij smooth zoom (out, across, in), eased toward
   where the scroll has put it in one loop that stops when it arrives.
   Choosing a place (on the map, in the index, or tabbing into its words)
   flies straight there. Nothing runs on a timer. Reduced motion, narrow
   screens and no script: the vertical journey, still. */
(function () {
  var d = document, w = window, root = d.documentElement;
  var atlas = d.querySelector(".ex-atlas");
  if (!atlas) return;
  var DATA = JSON.parse(atlas.getAttribute("data-ex"));
  var stage = atlas.querySelector(".ex-stage"), svg = atlas.querySelector(".ex-map");
  var pins = [].slice.call(atlas.querySelectorAll(".ex-pin"));
  var stops = [].slice.call(atlas.querySelectorAll(".ex-stop"));
  var bar = [].slice.call(atlas.querySelectorAll(".ex-bar a")), barEl = atlas.querySelector(".ex-bar");
  var photoLayer = atlas.querySelector(".ex-photos");
  var S = DATA.stops, N = S.length, ids = S.map(function (s) { return s.id; });
  var mqWide = w.matchMedia("(min-width: 1000px) and (min-height: 620px)");
  var mqRM = w.matchMedia("(prefers-reduced-motion: reduce)");
  var on = false, W = 0, H = 0, top0 = 0, step = 1, cams = [], zs = [], photos = {};
  var cur = null, tgt = null, raf = 0, tween = null, active = -1, lastT = 0, photoOn = "";

  /* the site's easing curve, cubic-bezier(.2,.8,.2,1); a flight uses it mirrored about its middle, so it
     leaves as gently as it arrives */
  function bez(t) {
    var x1 = .2, y1 = .8, x2 = .2, y2 = 1, u = t;
    for (var k = 0; k < 8; k++) {
      var cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
      var x = ((ax * u + bx) * u + cx) * u - t, dx = (3 * ax * u + 2 * bx) * u + cx;
      if (Math.abs(x) < 1e-5 || !dx) break;
      u -= x / dx;
    }
    var cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    return ((ay * u + by) * u + cy) * u;
  }
  function sstep(t) { return t * t * (3 - 2 * t); }
  function cosh(x) { return ((x = Math.exp(x)) + 1 / x) / 2; }
  function sinh(x) { return ((x = Math.exp(x)) - 1 / x) / 2; }
  function tanh(x) { return ((x = Math.exp(2 * x)) - 1) / (x + 1); }
  /* van Wijk and Nuij, "Smooth and efficient zooming and panning" (2003): a view is [cx, cy, width] */
  function zoom(p0, p1) {
    var rho = Math.SQRT2, ux0 = p0[0], uy0 = p0[1], w0 = p0[2], ux1 = p1[0], uy1 = p1[1], w1 = p1[2];
    var dx = ux1 - ux0, dy = uy1 - uy0, d2 = dx * dx + dy * dy, f, Sx;
    if (d2 < 1e-9) {
      Sx = Math.log(w1 / w0) / rho;
      f = function (t) { return [ux0 + t * dx, uy0 + t * dy, w0 * Math.exp(rho * t * Sx)]; };
    } else {
      var d1 = Math.sqrt(d2), b0 = (w1 * w1 - w0 * w0 + 4 * d2) / (2 * w0 * 2 * d1),
          b1 = (w1 * w1 - w0 * w0 - 4 * d2) / (2 * w1 * 2 * d1),
          r0 = Math.log(Math.sqrt(b0 * b0 + 1) - b0), r1 = Math.log(Math.sqrt(b1 * b1 + 1) - b1);
      Sx = (r1 - r0) / rho;
      f = function (t) {
        var s = t * Sx, c0 = cosh(r0), u = w0 / (2 * d1) * (c0 * tanh(rho * s + r0) - sinh(r0));
        return [ux0 + u * dx, uy0 + u * dy, w0 * c0 / cosh(rho * s + r0)];
      };
    }
    f.len = Math.abs(Sx);
    return f;
  }
  /* a stop's view: its box fitted into its region of the stage */
  function fit(s) {
    var b = s.box, r = s.reg, bw = b[2] - b[0], bh = b[3] - b[1];
    var k = Math.min((r[1] - r[0]) * W / bw, (r[3] - r[2]) * H / bh);
    var vw = W / k, vh = H / k, bcx = (b[0] + b[2]) / 2, bcy = (b[1] + b[3]) / 2;
    var vx = bcx - ((r[0] + r[1]) / 2 * W) / k, vy = bcy - ((r[2] + r[3]) / 2 * H) / k;
    return [vx + vw / 2, vy + vh / 2, vw];
  }
  function measure() {
    W = stage.clientWidth; H = stage.clientHeight;
    top0 = atlas.getBoundingClientRect().top + w.scrollY;
    step = (atlas.offsetHeight - H) / (N - 1);
    cams = S.map(fit);
    zs = [];
    for (var i = 0; i < N - 1; i++) zs.push(zoom(cams[i], cams[i + 1]));
    S.forEach(function (s, i) {
      var ph = photos[s.id];
      if (!ph) return;
      var c = cams[i], vw = c[2], vh = vw * H / W, px = (s.x - (c[0] - vw / 2)) / vw * W, py = (s.y - (c[1] - vh / 2)) / vh * H;
      var L = W * .4, PW = W - L;
      ph.style.setProperty("--mx", ((px - L) / PW * 100).toFixed(1) + "%");
      ph.style.setProperty("--my", (py / H * 100).toFixed(1) + "%");
    });
  }
  /* where the scroll has put the camera: a dwell at each stop, then a smooth zoom to the next */
  var DWELL = .5;
  function progress() { return Math.max(0, Math.min(N - 1, (w.scrollY - top0) / step)); }
  function target(p) {
    var i = Math.floor(p), f = p - i;
    if (i >= N - 1) return { cam: cams[N - 1].slice(), stop: N - 1, settled: true };
    var a = DWELL / 2;
    if (f <= a) return { cam: cams[i].slice(), stop: i, settled: true };
    if (f >= 1 - a) return { cam: cams[i + 1].slice(), stop: i + 1, settled: true };
    var t = sstep((f - a) / (1 - 2 * a));
    return { cam: zs[i](t), stop: f < .5 ? i : i + 1, settled: false };
  }
  function apply(c) {
    var vw = c[2], vh = vw * H / W, vx = c[0] - vw / 2, vy = c[1] - vh / 2;
    svg.setAttribute("viewBox", vx.toFixed(2) + " " + vy.toFixed(2) + " " + vw.toFixed(2) + " " + vh.toFixed(2));
    for (var i = 0; i < pins.length; i++) {
      var s = S[i + 1], x = (s.x - vx) / vw * W, y = (s.y - vy) / vh * H;
      var out = x < W * .42 || x > W + 40 || y < -40 || y > H + 40;
      pins[i].style.transform = "translate3d(" + x.toFixed(1) + "px," + y.toFixed(1) + "px,0)" + (pins[i].classList.contains("is-l") ? " translateX(-100%)" : "");
      pins[i].classList.toggle("is-off", out);
    }
    var fine = vw < 700 ? "1" : "0";
    if (svg.style.getPropertyValue("--ex-fine") !== fine) svg.style.setProperty("--ex-fine", fine);
  }
  function setActive(i) {
    if (i === active) return;
    active = i;
    stops.forEach(function (el) { el.classList.toggle("is-on", +el.getAttribute("data-i") === i); });
    pins.forEach(function (el) { el.classList.toggle("is-on", +el.getAttribute("data-i") === i); });
    bar.forEach(function (el) { el.classList.toggle("is-on", +el.getAttribute("data-i") === i); if (+el.getAttribute("data-i") === i) el.setAttribute("aria-current", "location"); else el.removeAttribute("aria-current"); });
    svg.setAttribute("data-on", i > 0 && i < N - 1 ? ids[i] : "");
    if (barEl) barEl.classList.toggle("is-quiet", i === 0 || i === N - 1);
  }
  function setPhoto(id) {
    if (id === photoOn) return;
    if (photos[photoOn]) photos[photoOn].classList.remove("is-on");
    photoOn = id;
    if (photos[id]) photos[id].classList.add("is-on");
  }
  function near(a, b) { return Math.abs(Math.log(a[2] / b[2])) < .02 && Math.hypot(a[0] - b[0], a[1] - b[1]) < b[2] * .006; }
  function frame(t) {
    raf = 0;
    var dt = lastT ? Math.min(64, t - lastT) : 16; lastT = t;
    var g = target(progress());
    tgt = g.cam;
    if (tween) {
      var u = Math.min(1, (t - tween.t0) / tween.dur);
      cur = tween.f(u < .5 ? (1 - bez(1 - 2 * u)) / 2 : (1 + bez(2 * u - 1)) / 2);
      if (u >= 1) tween = null;          /* from here the camera eases on toward wherever the scroll now is */
    } else {
      /* ease toward the target with weight: the centre in drawing units, the width in log */
      var a = 1 - Math.exp(-dt / 140);
      cur[0] += (tgt[0] - cur[0]) * a; cur[1] += (tgt[1] - cur[1]) * a;
      cur[2] = Math.exp(Math.log(cur[2]) + (Math.log(tgt[2]) - Math.log(cur[2])) * a);
    }
    apply(cur);
    setActive(tween ? tween.stop : g.stop);
    var here = !tween && g.settled && near(cur, tgt);
    var s = S[g.stop];
    setPhoto(here && s.photo ? s.id : "");
    if (tween || !near(cur, tgt)) raf = requestAnimationFrame(frame);
    else { lastT = 0; cur = tgt.slice(); apply(cur); }
  }
  function kick() { if (on && !raf) raf = requestAnimationFrame(frame); }
  function go(i, instant) {
    if (!on) return false;
    var y = Math.round(top0 + i * step);
    var to = cams[i];
    if (!instant && cur) {
      var z = zoom(cur, to);
      tween = { f: z, t0: performance.now(), dur: Math.max(1100, Math.min(2600, 700 * z.len + 500)), stop: i };
      setPhoto("");
    }
    w.scrollTo({ top: y, behavior: "instant" });
    if (instant || !cur) { cur = to.slice(); apply(cur); }
    setActive(i);
    kick();
    return true;
  }
  function build() {
    stops.forEach(function (st) {
      var fig = st.querySelector(".ex-photo");
      if (!fig || photos[st.id]) return;
      var c = fig.cloneNode(true);
      c.setAttribute("data-id", st.id);
      var img = c.querySelector("img");
      if (img) img.setAttribute("loading", "lazy");
      photoLayer.appendChild(c);
      photos[st.id] = c;
    });
  }
  function enable() {
    on = true;
    root.classList.add("ex-fly");
    build();
    measure();
    var g = target(progress());
    cur = g.cam.slice(); tgt = g.cam.slice();
    apply(cur); setActive(g.stop);
    root.classList.add("ex-ready");
    if (location.hash) { var k = ids.indexOf(location.hash.slice(1)); if (k > 0) go(k, true); }
    kick();
  }
  function disable() {
    on = false;
    root.classList.remove("ex-fly", "ex-ready");
    svg.setAttribute("viewBox", DATA.over.join(" "));
    svg.removeAttribute("data-on");
    svg.style.removeProperty("--ex-fine");
    pins.forEach(function (p) { p.style.transform = ""; p.classList.remove("is-off", "is-on"); });
    stops.forEach(function (s) { s.classList.remove("is-on"); });
    setPhoto(""); active = -1; tween = null;
  }
  function decide() {
    var want = mqWide.matches && !mqRM.matches;
    if (want && !on) safeEnable(); else if (!want && on) disable();
    else if (on) { measure(); cur = target(progress()).cam; apply(cur); }
  }
  w.addEventListener("scroll", kick, { passive: true });
  w.addEventListener("resize", function () { if (on || mqWide.matches) decide(); }, { passive: true });
  if (mqWide.addEventListener) { mqWide.addEventListener("change", decide); mqRM.addEventListener("change", decide); }
  /* choosing a place: the pins, the index and the bar fly there on the pinned atlas */
  atlas.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a || !on) return;
    var k = ids.indexOf(a.getAttribute("href").slice(1));
    if (k < 0) return;
    e.preventDefault();
    go(k, false);
    if (history.replaceState) history.replaceState(null, "", "#" + ids[k]);
    var st = stops[k], h = st && st.querySelector("h1,h2");
    if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
  });
  /* tabbing into a place's words takes the atlas there */
  atlas.addEventListener("focusin", function (e) {
    if (!on) return;
    var st = e.target.closest && e.target.closest(".ex-stop");
    if (!st) return;
    var k = +st.getAttribute("data-i");
    if (k !== active) go(k, false);
  });
  /* if anything here fails, the page falls back to the still journey rather than an empty stage */
  function safeEnable() { try { enable(); } catch (err) { disable(); } }
  if (root.classList.contains("ex-fly")) { if (mqWide.matches && !mqRM.matches) safeEnable(); else root.classList.remove("ex-fly"); }
  w.addEventListener("load", function () { if (on) { measure(); kick(); } });
})();
/* Night, now: the sun's place for this moment (a low-precision solar position, good to a fraction of a
   degree), and the night as seven small circles round the point opposite it, from sunset to the sun 18
   degrees down (the end of astronomical twilight) in steps of three, projected like the map (Equal Earth)
   and clipped to the world. Drawn once, on load. */
(function () {
  var d = document, atlas = d.querySelector(".ex-atlas"), g = atlas && atlas.querySelector(".ex-night");
  if (!g) return;
  var K = JSON.parse(atlas.getAttribute("data-ex")).k, R = Math.PI / 180;
  var A1 = 1.340264, A2 = -0.081106, A3 = 0.000893, A4 = 0.003796, M = Math.sqrt(3) / 2;
  function ee(lon, lat) {
    var th = Math.asin(M * Math.sin(lat * R)), t2 = th * th, t6 = t2 * t2 * t2;
    return [K * 2 * Math.sqrt(3) * lon * R * Math.cos(th) / (3 * (9 * A4 * t6 * t2 + 7 * A3 * t6 + 3 * A2 * t2 + A1)),
            -K * th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))];
  }
  var n = Date.now() / 86400000 + 2440587.5 - 2451545.0;
  var gm = (357.529 + 0.98560028 * n) * R, q = 280.459 + 0.98564736 * n;
  var L = (q + 1.915 * Math.sin(gm) + 0.020 * Math.sin(2 * gm)) * R, e = (23.439 - 0.00000036 * n) * R;
  var dec = Math.asin(Math.sin(e) * Math.sin(L)), ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L)) / R;
  var gmst = (280.46061837 + 360.98564736629 * n) % 360;
  var sunLon = ((ra - gmst) % 360 + 540) % 360 - 180;
  var aLat = -dec, aLon = sunLon + 180;                   /* the point opposite the sun */
  var html = "";
  [0, 3, 6, 9, 12, 15, 18].forEach(function (below) {
    var r = (90 - below) * R, p1 = aLat, l1 = aLon * R, pts = [], lon = null, total = 0;
    for (var b = 0; b <= 360; b += 2) {
      var th = b * R, la = Math.asin(Math.sin(p1) * Math.cos(r) + Math.cos(p1) * Math.sin(r) * Math.cos(th));
      var lo = (l1 + Math.atan2(Math.sin(th) * Math.sin(r) * Math.cos(p1), Math.cos(r) - Math.sin(p1) * Math.sin(la))) / R;
      if (lon !== null) { while (lo - lon > 180) lo -= 360; while (lo - lon < -180) lo += 360; total += lo - lon; }
      lon = lo; pts.push([lo, la / R]);
    }
    if (Math.abs(total) > 180) {                          /* it holds a pole: close the shape along it */
      var pole = aLat > 0 ? 90 : -90, last = pts[pts.length - 1][0], first = pts[0][0];
      pts.push([last, pole], [first, pole]);
    }
    for (var s = -360; s <= 360; s += 360) {
      var dd = "";
      pts.forEach(function (p, i) { var xy = ee(p[0] + s, p[1]); dd += (i ? "L" : "M") + xy[0].toFixed(1) + " " + xy[1].toFixed(1); });
      html += '<path d="' + dd + 'Z"/>';
    }
  });
  g.innerHTML = html;
  d.documentElement.classList.add("ex-has-night");
})();

/* Pointing at a place in the list lights it on the map, and pointing at it on the map lights it in the list. */
(function () {
  var d = document, atlas = d.querySelector(".ex-atlas");
  if (!atlas) return;
  var svg = atlas.querySelector(".ex-map");
  function links(id) { return atlas.querySelectorAll('a[href="#' + id + '"]'); }
  function hint(id, on) {
    [].forEach.call(links(id), function (a) { a.classList.toggle("is-hint", on); });
    if (on) svg.setAttribute("data-hint", id); else if (svg.getAttribute("data-hint") === id) svg.removeAttribute("data-hint");
  }
  [].forEach.call(atlas.querySelectorAll('.ex-ix a,.ex-pin,.ex-bar a'), function (a) {
    var id = a.getAttribute("href").slice(1);
    ["pointerenter", "focus"].forEach(function (t) { a.addEventListener(t, function () { hint(id, true); }); });
    ["pointerleave", "blur"].forEach(function (t) { a.addEventListener(t, function () { hint(id, false); }); });
  });
})();
</script>"""


def ld():
    return ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"WebPage",'
            '"@id":"%s#webpage","name":"%s","url":"%s","description":"%s",'
            '"isPartOf":{"@id":"https://paraglidingatlas.com/#website"},'
            '"publisher":{"@id":"https://paraglidingatlas.com/#organization"},"inLanguage":"en"}\n</script>'
            % (URL, TITLE, URL, DESC.replace('"', '\\"')))


def main():
    s = open(SHELL, encoding="utf-8").read()
    head, rest = s.split('<main id="v4-main">', 1)
    tail = rest.split("</main>", 1)[1]
    head = re.sub(r"<title>.*?</title>", "<title>%s: Paragliding Atlas</title>" % TITLE, head, 1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + DESC, head, 1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, head, 1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + TITLE, head, 1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + DESC, head, 1)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + OG_IMG, head, 1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + URL, head, 1)
    head = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "WebPage".*?</script>',
                  lambda m: ld(), head, 1, flags=re.S)
    head = re.sub(r"<!--v4u-css-->.*?<!--/v4u-css-->", "", head, 1, flags=re.S)
    head = re.sub(r"\n<style>.*?</style>\n(?=<!-- site-schema -->)", lambda m: "\n<style>" + css() + "</style>\n", head, 1, flags=re.S)
    head = head.replace(' aria-current="page" class="is-here"', "")
    # the header's Expeditions tab leads here (owner, 19 Oct): marked as the page you are on
    head = head.replace('<a href="expeditions.html">Expeditions</a>',
                        '<a href="expeditions.html" aria-current="page" class="is-here">Expeditions</a>', 1)
    if 'aria-current="page" class="is-here">Expeditions</a>' not in head:
        raise SystemExit("v4_expeditions_c: the header has no Expeditions tab to mark")
    if ".ex-atlas" not in head or "Partner With Me" in head.split("<body")[0] or URL not in head:
        raise SystemExit("v4_expeditions_c: the partners shell has changed; check the head")
    if 'content="noindex' not in head:
        raise SystemExit("v4_expeditions_c: the shell lost its noindex")
    body = main_html()
    page = head + body + tail.replace("</body>", SCRIPT + "\n</body>", 1)
    if "—" in page:
        raise SystemExit("v4_expeditions_c: an em dash crept in")
    if re.search(r"#[0-9a-fA-F]{3,8}\b(?![\w-])|rgba?\(|hsla?\(", css() + re.sub(r'href="#[\w-]+"|#ex-geo', "", body)) \
            or re.search(r"#[0-9a-fA-F]{6}\b|(rgba?|hsla?)\(", SCRIPT):
        raise SystemExit("v4_expeditions_c: a raw colour crept in; use the design tokens")
    open(OUT, "w", encoding="utf-8").write(page)
    print("v4_expeditions_c: %s (%d KB, main %d KB)" % (os.path.relpath(OUT, ROOT), len(page.encode()) // 1024,
                                                     len(body.encode()) // 1024))


if __name__ == "__main__":
    main()
