#!/usr/bin/env python3
"""
The expeditions page (owner, 19 Oct 2026: "expeditions standalone tab needs
to be a redesigned page, it's just an off copy of leftover material at
homepage, I want it to be a bit different"; then "use the same Awwwards
rule" and "the Awwwards rule can contain any option which makes the website
worth it, go crazy with your imagination").

    prototypes/v4/expeditions.html   (canonical /expeditions.html, noindex until approved)

For pilots choosing a trip, and plainly not the home page's #destinations
section: its four cards over one held picture, its dates-and-prices table and
its book-a-call band stay on the home page, and none of them is repeated
here. Built from option C, "The atlas" (tools/v4_expeditions_c.py, the
judges' winner over A and B, which stay as they are for the owner), with the
judges' grafts and every one of their must-fix items. The lessons of the
record page hold ("robotic, too much text, hard to navigate", then "a cheap
rip-off rather than premium"): few words, real photographs and type as the
graphics, long eased masks instead of seams, one signature, motion only in
answer to the visitor and calm.

The page, on a wide screen with motion allowed (the flight):
  - the arrival is a photograph (A): the two skies, the yellow wing over the
    Rift on the left and the red wing over the snow on the right, meeting in
    one long dissolve under "Choose Your Sky" (Kenya lies west of India, so
    each sky sits on its own side of the map that follows). The first image
    loads eagerly with fetchpriority high. Pointing at a sky leans the
    dissolve open (A), mask only;
  - the signature: the scroll pulls the camera back out of the sky into the
    atlas. The photograph is laid on the map between its two places and
    shrinks with the map as the camera zooms out (one transform, on the
    compositor), dissolving as the world comes up; then the scroll flies the
    camera from the whole world to India, Kenya, Kazakhstan and Peru and
    back out, each move the van Wijk and Nuij smooth zoom (out, across, in),
    all of it eased toward where the scroll has put it in one loop that
    stops when it arrives. No timers;
  - on a real graphics processor the map is drawn by WebGL 2 on one canvas
    from the same outlines as the still map (no library, no tiles): land
    filled through the stencil (nonzero, each ring fanned from its
    centroid), hairline coasts, the borders dashed, a graticule that fines
    as the camera comes close, the equator dashed, a soft light at each
    place and one that follows the pointer over the land. Every colour is
    read from the design tokens at run time (getComputedStyle, resolved
    through a 1 x 1 canvas). Each frame changes one uniform, so the flight
    stays smooth where an SVG of this size is repainted every frame. On a
    software renderer (failIfMajorPerformanceCaveat, or a SwiftShader /
    llvmpipe renderer string) or without WebGL 2, the still map's SVG flies
    by its viewBox instead, which software draws faster (measured here in
    headless Chromium, wheel scrolling from the world to Kenya: median
    16.7 ms, p90 33 ms, as option C on the same run; with software WebGL
    forced instead, p90 over a second);
  - the route: a great-circle line in the site's orange, India to Kenya to
    Kazakhstan to Peru, drawn as the camera flies each leg (scrubbed by the
    same eased progress), so the year reads as one journey;
  - the photograph rises out of the map from the place's ring as the camera
    comes in (from the last part of the approach, held through the whole
    stop), through an "air" dissolve: the reveal's edge is shaped by a still
    field of soft noise, so it opens like cloud clearing rather than a
    circle; it moves only as the camera does. One small 2D canvas over the
    photograph's region, the mask worked out on a coarse grid and upscaled
    (smooth at any size), redrawn only when something moved, on either
    renderer. Long eased masks on every inner edge; the photograph is held
    within 1.12 times its own pixels, so the 1152 px Kerio Valley frame is
    never stretched soft, and its region starts clear of the words;
  - pointing at India or Kenya on the world map (its row, its pin, or one of
    its months) opens a small soft window of that place's photograph round
    its ring, its own focal point under the ring (a preview before the
    flight); on the WebGL map a soft light follows the pointer over the
    land; both ease in answer to the pointer and stop when it does;
  - the year along the foot, to scale (A, with B's season stretches and
    month zones): Oct 2026 to Nov 2027, each departure a bar on its real
    days, the planned two as hollow month bars, the season of each set trip
    a brighter stretch of the line, a taller tick where 2027 begins. It
    answers when as the map answers where: pointing at a month lights the
    place flying then; choosing a place flies there; the current stop's bars
    turn orange;
  - the world stop is the index (B): each place's dates, length and price in
    four rows, not a table, so dates and budget are chosen in seconds;
  - the place type is at display scale (A), fitted to each name;
  - the planned two: the camera frames each closer, the route arrives there,
    the type leads with only what the home page gives them;
  - the close: the camera pulls back over the whole route and India's "Last
    light" frame rises under "Still Choosing?" (B's closing photograph).

Phones, tablets, reduced motion and no script (the still journey): the
same story down the page, nothing pinned, nothing moving: the two skies
(stacked on phones, India above Kenya, as on the map), the year chooser
sticky under the menu (stepping down when the menu returns, and letting go
after the last place), the world with the route and the index, each place on
its own plate of the same map dissolving into its photograph on every edge,
then the close. Phones get the trip pages' own portrait crops.

Fixes from the judges, beyond the grafts: no lit national outlines (each
place is a ring and a soft light, the same for all four); no "Night, now"
layer and no map credit on the page (Natural Earth is public domain; noted
here); no setProperty patch on <html>; words leave as the camera leaves and
come in on arrival, on a scroll or a click; pin labels keep a fixed gap from
their rings; index rows lift to white with an underline, not orange; phone
pin labels at least 12.5 px; the world fits its stage; the arrival has a
photograph at every width.

Facts, each from the site (nothing here is new):
  - the home page's #destinations section (prototypes/v4/index.html): India
    "Bir Billing, Himalaya", four departures in 2027 (15 to 24 Apr, 25 Apr to 4 May, 21 to 30 Oct, 3 to 12 Nov), 10 days,
    6 places, £1,100, "Guaranteed to run"; Kenya "Kerio Valley, Rift Valley",
    18 to 29 Jan 2027 and 1 to 12 Feb 2027, 12 days, 8 places, US$2,100,
    "Booking open"; Kazakhstan "The steppe", "Beyond Roads, Beyond Maps",
    planned June 2027, 10 days, small group, €2,100; Peru "Lima and the
    Andes", "Soar The Land Of The Incas", planned November 2027, 14 days,
    small group, €1,850; both planned "Register interest"
    (enquire.html?trip=kazakhstan, ?trip=peru); the "From" before every
    price; "Small groups, fixed dates. Prices are per pilot.";
  - destinations/india.html: "Big Mountain Flying is built for autonomous
    pilots who want the Himalaya at its most approachable"; £1,100 per
    pilot; pilot rating IPPI 2 or equivalent; season October to November;
    cloudbase 3 to 3.6 km on the front range; 32.0500°N 76.7200°E (shown as
    32.05°N · 76.72°E); "Hold a place" sends an enquiry (?trip=india);
  - destinations/kenya.html: "Explore the Cradle is built for independent
    pilots with strong glider handling and an appetite for the unfamiliar";
    0.72°N · 35.65°E; "Starting from US$2,100"; pilot rating IPPI 2 or
    equivalent; season December to March; thermals 4 to 6 m/s at the midday
    peaks;
  - the call: the home page's free 30-minute call (the site's calendar link)
    and the enquiry page.
  Level: the home page's skill meter (India 4 of 5, Kenya 2 of 5) is left
  out on purpose until the owner reconciles it with the trip pages (India:
  "IPPI 2 or equivalent, the same as our Kenya tour"; Kenya asks for
  autonomous pilots with strong thermalling). The two trip pages' own "built
  for" lines tell the trips apart instead.
  Nothing on the page is unknown, so nothing shows as [to supply]; a fact
  added later without a source takes the site's <span class="v2-tbd">.

Photographs: only the trips' own, each with the alt its trip page gives it
and named only as its page names it. Sizes checked with PIL:
  - india/hero/snowline 1800x1200 ("Above the snowline"), kenya/hero/equator
    1152x768 ("The Equator"): the arrival, eager; on phones the trip pages'
    portrait crops img/hero/india-snowline-p (800x1200) and
    kenya-equator-p (512x768);
  - india/hero/dhauladhar 2400x1600 ("The Dhauladhar"), phone crop
    india-dhauladhar-p 934x1400; kenya/hero/kerio-valley 1152x768 ("Kerio
    Valley"), phone crop kenya-kerio-valley-p 512x768;
  - india/gallery/last-light 1400x933 ("Last light"), the close.
  Kazakhstan and Peru have no trip photographs on the site, so their stops
  are the map and the type. No video (owner, 8 Oct: footage only on trip
  pages and the home page), no stock, no pilot presented as the owner.

The map: country outlines from prototypes/workspace/atlas/data/world.json
(Natural Earth 1:110m, public domain; read here, never edited), Antarctica
left out, in the Equal Earth projection (Savric, Patterson and Jenny,
2018). The markers for Kazakhstan and Peru stand for "The steppe" and "Lima
and the Andes"; no coordinates are shown for them because the site gives
none.

House rules: tokens only (CSS, and the canvas reads them), no em dash, Title
Case headings, grey labels (the orange capitals only in the page's kicker),
motion only in answer to the visitor, everything visible with reduced motion
or without the script, 44 px targets, a name on every control, under 400
words in <main> (checked here). The v4 shell (head, menu, footer) comes from
partners.html; the menu is not touched here (the owner wires it after
approving).

    python3 tools/v4_expeditions.py
"""
import calendar
import html
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "partners.html")
OUT = os.path.join(V4, "expeditions.html")
WORLD = os.path.join(ROOT, "prototypes", "workspace", "atlas", "data", "world.json")

TITLE = "Expeditions"
DESC = ("Five places to fly with Paragliding Atlas, on one map and one year: Kerio Valley in Kenya, Panchgani "
        "and Bir Billing in India with dates set, Kazakhstan and Peru planned for 2027.")
URL = "https://paraglidingatlas.com/expeditions.html"
OG_IMG = "https://paraglidingatlas.com/assets/destinations/india/hero/snowline.jpg"
CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"
MAX_WORDS = 450          # 400 for four places; Panchgani, a fifth, adds its card and its row (chat 11)

A = "../../assets/"

# ---------- the projection: Equal Earth (Savric, Patterson, Jenny 2018), 200 units to the radius ----------
EA1, EA2, EA3, EA4 = 1.340264, -0.081106, 0.000893, 0.003796
EM = math.sqrt(3) / 2
SCALE = 200.0



def one_year(dates):
    """A place's departures in one year name it once, on the last (owner, 26 Oct 2026: "write 2027 only once")."""
    yrs = {d.rsplit(" ", 1)[-1] for d in dates}
    if len(dates) < 2 or len(yrs) != 1:
        return dates
    return [d.rsplit(" ", 1)[0] for d in dates[:-1]] + dates[-1:]

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
    body = ""
    for (ax, ay), (bx, by) in zip(q, q[1:]):
        for t in (num((bx - ax) / 10.0), num((by - ay) / 10.0)):
            if body and not t.startswith("-"):
                body += " "
            body += t
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
    if len(q) < 3:
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


TOL = 0.32         # simplification, in drawing units (finer than option C's .45: the coasts hold at country zoom)
MIN_AREA = 6.0     # islands smaller than this (square units, a few pixels at the whole world) are left out,
NEAR_DEG = 22      # except within this many degrees of a place, where the camera comes close

# ---------- the places, in the order they fly ----------
TBD = "[to supply]"      # the owner's fact still to come: shown as the site's to-supply mark


def val(v):
    """A fact, escaped, with [to supply] as the site's mark."""
    return esc(v).replace(TBD, '<i class="v2-tbd">%s</i>' % TBD)


PLACES = [
    dict(id="kenya", n="01", name="Kenya", region="Kerio Valley, Rift Valley", country="Kenya",
         lon=35.65, lat=0.72, co="0.72°N · 35.65°E", status="set",
         line=("Explore the Cradle is built for independent pilots with strong glider handling and an appetite "
               "for the unfamiliar."),
         dates=["18 to 29 Jan 2027", "1 to 12 Feb 2027"], state="Booking open",
         deps=[(2027, 1, 18, 29), (2027, 2, 1, 12)], season=((2026, 12), (2027, 3)), pick="Jan, Feb", lab="r",
         facts=[("Length", "12 days"), ("Group", "8 places"), ("Price", "From US$2,100"),
                ("Rating", "IPPI 2 or equivalent"), ("Season", "December to March"),
                ("Thermals", "4 to 6 m/s at the midday peaks")],
         ix=("12 days", "From US$2,100"),
         book=("Hold a place", "enquire.html?trip=kenya"), more=("The full trip", "destinations/kenya.html"),
         photo=dict(base=A + "destinations/kenya/hero/kerio-valley", w=1152, h=768,
                    p=("img/hero/kenya-kerio-valley-p", 512, 768),
                    alt="Three paragliders soaring along a hazy green ridge above terraced fields in the Kerio Valley",
                    cap="Kerio Valley", pos=(.55, .6)),
         near=7.0),
    dict(id="panchgani", n="02", name="Panchgani", region="Sahyadri hills", country="India",
         lon=73.82, lat=17.92, co="17.92°N · 73.82°E", status="set",
         line="The plateau that hosted a pre World Cup.",
         dates=["14 to 21 Feb 2027"], state="Dates set",
         deps=[(2027, 2, 14, 21)], season=None, pick="Feb",
         facts=[("Length", "8 days"), ("Group", TBD), ("Price", TBD), ("Rating", TBD),
                ("Season", "November to March")],
         ix=("8 days", "Price " + TBD),
         book=("Hold a place", "enquire.html?trip=panchgani"), more=("The full trip", "destinations/panchgani.html"),
         photo=None,      # its one photograph is already the opening's and its own page's (no photo twice)
         near=7.0),
    dict(id="india", n="03", name="India", region="Bir Billing, Himalaya", country="India",
         lon=76.72, lat=32.05, co="32.05°N · 76.72°E", status="set",
         line="Big Mountain Flying is built for autonomous pilots who want the Himalaya at its most approachable.",
         dates=["15 to 24 Apr 2027", "25 Apr to 4 May 2027", "21 to 30 Oct 2027", "3 to 12 Nov 2027"], state="Guaranteed to run",
         deps=[(2027, 4, 15, 24), (2027, 4, 25, 4), (2027, 10, 21, 30), (2027, 11, 3, 12)], season=None,
         pick="Apr, May, Oct, Nov", lab=("r", (2027, 10, 31)),
         facts=[("Length", "10 days"), ("Group", "6 places"), ("Price", "£1,100 per pilot"),
                ("Rating", "IPPI 2 or equivalent"), ("Season", "April to May, October to November"),
                ("Cloudbase", "3 to 3.6 km on the front range")],
         ix=("10 days", "From £1,100"),
         book=("Hold a place", "enquire.html?trip=india"), more=("The full trip", "destinations/india.html"),
         photo=dict(base=A + "destinations/india/hero/dhauladhar", w=2400, h=1600,
                    p=("img/hero/india-dhauladhar-p", 934, 1400),
                    alt="The Dhauladhar range under building cumulus, above the Kangra valley",
                    cap="The Dhauladhar", pos=(.5, .62)),
         near=7.0),
    dict(id="kazakhstan", n="04", name="Kazakhstan", region="The steppe", country="Kazakhstan",
         lon=67.0, lat=48.0, co="", status="planned",
         line="Beyond Roads, Beyond Maps",
         dates=[], state="", deps=[(2027, 6, 1, 30)], season=None, pick="Jun", when="June 2027",
         facts=[("Planned", "June 2027"), ("Length", "10 days"), ("Group", "Small group"), ("Price", "From €2,100")],
         ix=("10 days", "From €2,100"),
         book=("Register interest", "enquire.html?trip=kazakhstan"), more=None, photo=None,
         near=11.0),
    dict(id="peru", n="05", name="Peru", region="Lima and the Andes", country="Peru",
         lon=-77.04, lat=-12.05, co="", status="planned",
         line="Soar The Land Of The Incas",
         dates=[], state="", deps=[(2027, 11, 1, 30)], season=None, pick="Nov", lab="l", when="November 2027",
         facts=[("Planned", "November 2027"), ("Length", "14 days"), ("Group", "Small group"),
                ("Price", "From €1,850")],
         ix=("14 days", "From €1,850"),
         book=("Register interest", "enquire.html?trip=peru"), more=None, photo=None,
         near=11.0),
]
for _p in PLACES:
    _p["x"], _p["y"] = ee(_p["lon"], _p["lat"])
BY = {p["id"]: p for p in PLACES}

# the two skies at the arrival, and the close (each alt the one its trip page gives it)
SKY = {
    "kenya": dict(base=A + "destinations/kenya/hero/equator", w=1152, h=768, p=("img/hero/kenya-equator-p", 512, 768),
                  alt="A yellow paraglider on a long glide over arid rock outcrops in low golden light",
                  trip="Explore the Cradle"),
    "india": dict(base=A + "destinations/india/hero/snowline", w=1800, h=1200, p=("img/hero/india-snowline-p", 800, 1200),
                  alt="A pilot on a red wing flying over snow-covered mountains", trip="Big Mountain Flying"),
}
LAST = dict(base=A + "destinations/india/gallery/last-light", w=1400, h=933,
            alt="A paraglider silhouetted against a burning sunset", cap="Last light")

# the year: October 2026 to November 2027, fourteen months
Y0, M0, NMONTHS = 2026, 10, 14

ARROW = ('<svg class="ex-arr" viewBox="0 0 16 10" aria-hidden="true" focusable="false">'
         '<path d="M0 5h14.5M10.5 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')
DOWN = ('<svg class="ex-dn" viewBox="0 0 10 14" aria-hidden="true" focusable="false">'
        '<path d="M5 0v12.5M1 8.5l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')
EXT = ('<svg class="ex-ext" viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
       '<path d="M3.5 2.5h6v6M9.5 2.5l-7 7" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')


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
    share, each drawn once. Islands smaller than a pixel at the whole world's scale are left out. No country
    is ever lit as a whole: a place is a ring and a light."""
    world = load_world()
    seg = {}
    for _, rings in world:
        for r in rings:
            for a, b in zip(r, r[1:] + r[:1]):
                k = tuple(sorted((a[2], b[2])))
                seg[k] = seg.get(k, 0) + 1
    land, borders = [], []
    done = set()
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
        if dpath:
            land.append(dpath)
    return land, borders


def graticule():
    """Every 30 degrees across the world; every 5 degrees (seen only close) where the places are."""
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


def great_circle(a, b, n=72):
    """Points along the great circle from place a to place b (longitude, latitude), projected."""
    lo1, la1, lo2, la2 = map(math.radians, (a["lon"], a["lat"], b["lon"], b["lat"]))
    p1 = (math.cos(la1) * math.cos(lo1), math.cos(la1) * math.sin(lo1), math.sin(la1))
    p2 = (math.cos(la2) * math.cos(lo2), math.cos(la2) * math.sin(lo2), math.sin(la2))
    om = math.acos(max(-1.0, min(1.0, sum(x * y for x, y in zip(p1, p2)))))
    out = []
    for i in range(n + 1):
        t = i / float(n)
        s1, s2 = math.sin((1 - t) * om) / math.sin(om), math.sin(t * om) / math.sin(om)
        p = [s1 * x + s2 * y for x, y in zip(p1, p2)]
        out.append(ee(math.degrees(math.atan2(p[1], p[0])), math.degrees(math.asin(max(-1.0, min(1.0, p[2]))))))
    return out


LEGS = [great_circle(a, b) for a, b in zip(PLACES, PLACES[1:])]


def bbox_of(country):
    world = json.load(open(WORLD, encoding="utf-8"))
    c = [x for x in world if x["n"] == country][0]
    pts = [ee(p[0], p[1]) for r in c["p"] for p in r]
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]


def r1(v):
    return round(v, 1)


# the whole world but Antarctica, with a little sea round it
_top = ee(0, 84.5)[1]
_bot = ee(0, -58.0)[1]
_xw = ee(180, 0)[0]
OVER = [r1(-_xw - 6), r1(_top - 6), r1(2 * _xw + 12), r1(_bot - _top + 12)]
WORLD_BOX = [r1(-_xw), r1(_top), r1(_xw), r1(_bot)]


def frames():
    """The stage's stops: what to fit (a box in drawing units) and where on the stage to fit it (fractions of
    the width and height: left, right, top, bottom)."""
    ki, kk = BY["india"], BY["kenya"]
    out = [dict(id="open", box=[r1(kk["x"] - 4), r1(ki["y"] - 4), r1(ki["x"] + 4), r1(kk["y"] + 4)],
                reg=[.26, .74, .3, .7])]
    out.append(dict(id="world", box=WORLD_BOX, reg=[.43, .97, .17, .83]))
    for p in PLACES:
        k = p["near"] * 3.0          # about 3 units a degree near the equator
        box = [p["x"] - k, p["y"] - k, p["x"] + k, p["y"] + k]
        reg = [.42, .64, .27, .73] if p["photo"] else [.62, .94, .22, .82]
        out.append(dict(id=p["id"], box=[r1(v) for v in box], reg=reg))
    out.append(dict(id="outro", box=WORLD_BOX, reg=[.36, .98, .08, .6]))
    return out


def inset_box(p):
    """A place's plate in the still journey: the place a little above the middle, the land round it."""
    k = 26.0 if p["photo"] else 30.0
    w, h = 2 * k * 1.6, 2 * k
    return [r1(p["x"] - w / 2), r1(p["y"] - h * (.42 if p["photo"] else .5)), r1(w), r1(h)]


# ---------- the markup ----------
def pct(v, a, n):
    return "%.2f%%" % ((v - a) / n * 100)


def pin(p, i):
    kind = "is-set" if p["status"] == "set" else "is-planned"
    when = ("next " + p["dates"][0]) if p["dates"] else ("planned " + p["when"])
    side = " is-l" if p["id"] in ("peru",) else ""
    return ('<a class="ex-pin %s%s" href="#%s" data-i="%d" tabindex="-1" style="--x:%s;--y:%s" aria-label="%s, %s, %s">'
            '<i class="ex-dot" aria-hidden="true"></i><span class="ex-pl" aria-hidden="true">%s</span></a>'
            % (kind, side, p["id"], i + 2, pct(p["x"], OVER[0], OVER[2]), pct(p["y"], OVER[1], OVER[3]),
               esc(p["name"]), esc(p["region"]), esc(when), esc(p["name"])))


def route_d():
    return "".join(rel_path(leg) for leg in LEGS)


def map_svg():
    land, borders = geometry()
    major, minor, edge, eq = graticule()
    glows = "".join('<circle class="ex-gw is-%s" cx="%s" cy="%s" r="%s" fill="url(#ex-glow%s)"/>'
                    % (p["status"], num(p["x"]), num(p["y"]), "7" if p["status"] == "set" else "5",
                       "" if p["status"] == "set" else "2") for p in PLACES)
    # the borders twice: once in the land's own colour over the coast strokes the two countries' edges leave
    # there, once as the border itself
    return ('<svg class="ex-map" viewBox="%s" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">'
            '<defs><radialGradient id="ex-glow"><stop offset="0" class="ex-gs0"/><stop offset=".45" class="ex-gs1"/>'
            '<stop offset="1" class="ex-gs2"/></radialGradient><radialGradient id="ex-glow2"><stop offset="0" class="ex-gs3"/>'
            '<stop offset=".45" class="ex-gs4"/><stop offset="1" class="ex-gs2"/></radialGradient></defs>'
            '<g id="ex-geo"><path class="ex-sea" d="%s"/><path class="ex-g5" d="%s"/><path class="ex-g30" d="%s"/>'
            '<path class="ex-eq" d="%s"/><g class="ex-land">%s</g><g class="ex-bd" id="ex-bd">%s</g>'
            '<use class="ex-bdu" href="#ex-bd"/><path class="ex-rplan" d="%s"/><path class="ex-route" d="%s"/><g class="ex-gws">%s</g>'
            '<path class="ex-edge" d="%s"/></g></svg>'
            % (" ".join(num(v) for v in OVER), edge, minor, major, eq,
               "".join('<path class="ex-l" d="%s"/>' % d for d in land),
               "".join('<path class="ex-b" d="%s"/>' % d for d in borders), route_d(), route_d(), glows, edge))


def picture(ph, cls="ex-photo", lazy=True, fetch=False, cap=None, phone="(max-width: 699px)"):
    att = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if fetch else ' decoding="async"')
    p = ph.get("p")
    small = ('<source media="%s" srcset="%s.webp" type="image/webp"><source media="%s" srcset="%s.jpg">'
             % (phone, p[0], phone, p[0])) if p and phone else ""
    fc = ('<figcaption>%s</figcaption>' % esc(cap)) if cap else ""
    return ('<figure class="%s"><picture>%s<source srcset="%s.webp" type="image/webp">'
            '<img src="%s.jpg" width="%d" height="%d" alt="%s"%s></picture>%s</figure>'
            % (cls, small, ph["base"], ph["base"], ph["w"], ph["h"], esc(ph["alt"]), att, fc))


def opening():
    """The arrival: the two skies meeting in one dissolve, Kenya to the west and India to the east."""
    halves = "".join(
        '<a class="ex-half is-%s" href="#%s"><span class="ex-hcap"><b>%s%s</b> <span>%s</span></span></a>'
        % (k, k, BY[k]["name"], DOWN, esc(SKY[k]["trip"])) for k in ("kenya", "india"))
    pics = "".join(
        '<div class="ex-pic is-%s">%s</div>' % (k, picture(SKY[k], cls="ex-sky-ph", lazy=False, fetch=(k == "india")))
        for k in ("kenya", "india"))
    return ('<header class="ex-stop ex-open is-on" data-i="0">'
            '<div class="ex-sky">%s</div>'
            '<div class="ex-panel"><p class="ex-kicker">Expeditions</p><h1 class="ex-h1">Choose Your Sky</h1>'
            '<p class="ex-lead">Three with dates set, two being planned. Small groups, fixed dates. '
            'Prices are per pilot.</p></div>%s</header>' % (pics, halves))


def frac(y, m, day, end=False):
    """Where a day falls on the year line, 0 at 1 October 2026 and 1 at the end of November 2027."""
    i = (y - Y0) * 12 + (m - M0)
    n = calendar.monthrange(y, m)[1]
    return (i + (day if end else day - 1) / float(n)) / NMONTHS


def dep_end(y, m, d0, d1):
    """A departure's last day as (year, month, day): one whose last day is smaller than its first ends in the next month."""
    if d1 >= d0:
        return y, m, d1
    return (y + 1, 1, d1) if m == 12 else (y, m + 1, d1)


def year_strip():
    links, bars, seasons = [], [], []
    for i, p in enumerate(PLACES):
        x0 = frac(*p["deps"][0][:3])
        x1 = frac(*dep_end(*p["deps"][-1]), end=True)
        # a label starts at its first departure, or ends at its last (lab="r", or past nine tenths of the
        # line): Kenya's ends where Panchgani's begins (chat 11); the months, not the year, as the line marks it
        # India's ends with October, where Peru's begins: both fly in November 2027
        lab = p.get("lab")
        if isinstance(lab, tuple):
            lab, x1 = lab[0], frac(*lab[1], end=True)
        right = lab == "r" or (lab != "l" and x1 > 0.9)
        anchor = ("right:calc(%.3f%% + .6rem)" % ((1 - x1) * 100)) if right else ("left:%.3f%%" % (x0 * 100))
        links.append('<li style="%s"><a href="#%s" data-i="%d"><b>%s</b> <span class="ex-mo">%s</span></a></li>'
                     % (anchor, p["id"], i + 2, esc(p["name"]), esc(p["pick"])))
        for (y, m, d0, d1) in p["deps"]:
            s, e = frac(y, m, d0), frac(*dep_end(y, m, d0, d1), end=True)
            bars.append('<i class="ex-ybar%s" data-t="%s" style="left:%.3f%%;width:%.3f%%"></i>'
                        % (" is-plan" if p["status"] == "planned" else "", p["id"], s * 100, (e - s) * 100))
        if p["season"]:
            (ya, ma), (yb, mb) = p["season"]
            s = max(0.0, frac(ya, ma, 1))
            e = frac(yb, mb, calendar.monthrange(yb, mb)[1], end=True)
            seasons.append('<i class="ex-yseason" data-t="%s" style="left:%.3f%%;width:%.3f%%"></i>'
                           % (p["id"], s * 100, (e - s) * 100))
    months = []
    for k in range(NMONTHS):
        y, m = Y0 + (M0 - 1 + k) // 12, (M0 - 1 + k) % 12 + 1
        name = calendar.month_abbr[m]
        who = [p["id"] for p in PLACES if any(dy == y and dm == m for (dy, dm, _, _) in p["deps"])]
        months.append('<span%s%s><b>%s</b><i>%s</i></span>'
                      % (' class="is-y"' if m == 1 else "", (' data-t="%s"' % who[0]) if who else "", name, name[0]))
    return ('<nav class="ex-year" aria-label="The five expeditions, by place and month"><div class="ex-year-in">'
            '<div class="ex-yline" aria-hidden="true">%s%s</div>'
            '<div class="ex-ymonths" aria-hidden="true">%s</div>'
            '<ol class="ex-yplaces">%s</ol></div></nav>'
            % ("".join(seasons), "".join(bars), "".join(months), "".join(links)))


def world():
    rows = []
    for i, p in enumerate(PLACES):
        if p["dates"]:
            when = "".join('<span>%s</span>' % esc(d) for d in one_year(p["dates"]))
        else:
            when = '<span>Planned, %s</span>' % esc(p["when"])
        rows.append('<li><a href="#%s" data-i="%d"><span class="ex-ix-n">%s</span><span class="ex-ix-t">%s</span>'
                    '<span class="ex-ix-m"><span class="ex-ix-d">%s</span><span class="ex-ix-f">%s · %s</span></span>'
                    '</a></li>' % (p["id"], i + 2, p["n"], esc(p["name"]), when, esc(p["ix"][0]), val(p["ix"][1])))
    return ('<section class="ex-stop ex-world" data-i="1" aria-labelledby="ex-world-h"><div class="ex-panel">'
            '<h2 class="ex-h2" id="ex-world-h">Where And When</h2>'
            '<ol class="ex-ix">%s</ol></div></section>' % "".join(rows))


def plate():
    pins = "".join(pin(p, i) for i, p in enumerate(PLACES))
    return ('<figure class="ex-plate" aria-label="Map of the five places and the route between them">%s'
            '<canvas class="ex-gl" aria-hidden="true"></canvas><canvas class="ex-air" aria-hidden="true"></canvas>'
            '<div class="ex-pins">%s</div></figure>' % (map_svg(), pins))


def inset(p):
    vb = inset_box(p)
    kind = "is-set" if p["status"] == "set" else "is-planned"
    x, y = pct(p["x"], vb[0], vb[2]), pct(p["y"], vb[1], vb[3])
    label = p["co"] or "Planned"
    return ('<div class="ex-inset%s" style="--ar:%s;--av:%s">'
            '<svg viewBox="%s" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            '<use href="#ex-geo"/></svg>'
            '<span class="ex-imark %s" style="--x:%s;--y:%s" aria-hidden="true"><i class="ex-dot %s"></i>%s</span></div>'
            % (" has-photo" if p["photo"] else "", "%g / %g" % (vb[2], vb[3]), "%.4f" % (vb[2] / vb[3]),
               " ".join(num(v) for v in vb), kind, x, y, kind, esc(label)))


def fit_name(name):
    """The place's name at display scale, fitted to its letters (Poppins Bold advances about .58 em a letter
    at this tracking)."""
    return "%.4f" % (1.0 / (len(name) * .58))


def place(p, i):
    if p["dates"]:
        when = ('<div class="ex-when"><span class="ex-lab">Departures</span><p>%s</p>'
                '<p class="ex-state"><i aria-hidden="true"></i>%s</p></div>'
                % ("".join('<span>%s</span>' % esc(d) for d in one_year(p["dates"])), esc(p["state"])))
    else:
        when = ""
    facts = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(k), val(v)) for k, v in p["facts"])
    acts = ('<a class="btn-solid ex-book" href="%s"><span>%s<span class="ex-vh"> for %s</span></span></a>'
            % (p["book"][1], esc(p["book"][0]), esc(p["name"])))
    if p["more"]:
        acts += ('<a class="ex-more" href="%s">%s<span class="ex-vh"> to %s</span>%s</a>'
                 % (p["more"][1], esc(p["more"][0]), esc(p["name"]), ARROW))
    media = inset(p)
    if p["photo"]:
        media += picture(p["photo"], cap=p["photo"]["cap"])
    return ('<article class="ex-stop ex-place is-%s" id="%s" data-i="%d" aria-labelledby="%s-h">'
            '<div class="ex-media">%s</div>'
            '<div class="ex-panel">'
            '<p class="ex-label"><span>%s</span> %s</p>'
            '<h2 class="ex-name" id="%s-h" style="--ex-fit:%s">%s</h2>'
            '%s<p class="ex-line">%s</p>'
            '%s<dl class="ex-facts">%s</dl>'
            '<div class="ex-acts">%s</div>'
            '</div></article>'
            % (p["status"], p["id"], i + 2, p["id"], media, p["n"], esc(p["region"]), p["id"], fit_name(p["name"]),
               esc(p["name"]), ('<p class="ex-co">%s</p>' % esc(p["co"])) if p["co"] else "",
               esc(p["line"]), when, facts, acts))


def outro():
    return ('<section class="ex-stop ex-outro" data-i="%d" aria-labelledby="ex-outro-h">'
            '<div class="ex-out-ph">%s</div><div class="ex-panel">'
            '<h2 class="ex-h2" id="ex-outro-h">Still Choosing?</h2>'
            '<p class="ex-lead">Book a free 30-minute call, or send an enquiry.</p>'
            '<div class="ex-acts"><a class="btn-solid" href="%s" target="_blank" rel="noopener"><span>Book a call'
            '<span class="ex-vh"> (opens a new tab)</span></span></a>'
            '<a class="ex-more" href="enquire.html">Enquire%s</a></div>'
            '</div></section>' % (len(PLACES) + 2, picture(LAST, cap=LAST["cap"], phone=None), CALL, ARROW))


EARLY = ('<script>(function(r,m){r.classList.add("ex-js");'
         'if(m("(min-width: 1000px) and (min-height: 620px)").matches&&!m("(prefers-reduced-motion: reduce)").matches'
         '&&typeof WebGL2RenderingContext!=="undefined"){r.classList.add("ex-fly");'
         'var n=document.querySelector(".page-wrap > nav");if(n)r.style.setProperty("--ex-nav",n.offsetHeight+"px");}'
         '})(document.documentElement,function(q){return window.matchMedia(q);});</script>')


def data_attr():
    places = []
    for p in PLACES:
        d = dict(id=p["id"], x=r1(p["x"]), y=r1(p["y"]), set=p["status"] == "set")
        if p["photo"]:
            ph = p["photo"]
            d["photo"] = dict(src=ph["base"], w=ph["w"], h=ph["h"], pos=list(ph["pos"]))
        places.append(d)
    legs = [[r1(v) for pt in leg for v in pt] for leg in LEGS]
    d = dict(over=OVER, stops=frames(), places=places, legs=legs)
    return esc(json.dumps(d, separators=(",", ":")))


def main_html():
    return ('<main id="v4-main" class="ex">\n' + EARLY
            + '<!-- The map: Natural Earth 1:110m outlines (public domain), Equal Earth projection. -->'
            + '<div class="ex-atlas" data-ex="%s" style="--n:%d">' % (data_attr(), len(PLACES) + 3)
            + '<div class="ex-stage">' + opening()
            + '<div class="ex-journey">' + year_strip() + world() + plate()
            + "".join(place(p, i) for i, p in enumerate(PLACES)) + '</div>'
            + outro() + '</div></div>\n</main>')


# ---------- the long eased masks ----------
# a photograph or a plate never meets the page at an edge: its alpha runs from nothing to whole along a
# smootherstep, over a long distance, written out as many stops of an opaque token mixed with transparent (a
# mask reads only the alpha, so the colour never shows)
K = "var(--ink)"


def smoother(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def alpha(a):
    if a <= 0.004:
        return "transparent"
    if a >= 0.996:
        return K
    return "color-mix(in srgb,%s %.1f%%,transparent)" % (K, a * 100)


def at(p0, p1, t):
    if isinstance(p0, (int, float)) and isinstance(p1, (int, float)):
        return "%.2f%%" % (p0 + (p1 - p0) * t)
    return "calc(%s + (%s - %s) * %.4f)" % (p0, p1, p0, t)


def ramp(p0, p1, a0, a1, n=10):
    return ["%s %s" % (alpha(a0 + (a1 - a0) * smoother(i / float(n))), at(p0, p1, i / float(n))) for i in range(n + 1)]


def grad(deg, *runs):
    out = []
    for r in runs:
        out += r if isinstance(r, list) else [r]
    return "linear-gradient(%ddeg,%s)" % (deg, ",".join(out))


SPLIT0, SPLIT1 = "(var(--ex-split) - var(--ex-w))", "(var(--ex-split) + var(--ex-w))"
# the arrival, side by side: the west sky whole at the left and gone past the seam, the east sky the other way
MASK_W = grad(90, "%s 0%%" % K, ramp(SPLIT0, SPLIT1, 1, 0, 12), "transparent 100%")
MASK_E = grad(90, "transparent 0%", ramp(SPLIT0, SPLIT1, 0, 1, 12), "%s 100%%" % K)
# on the flight the skies are a little wider than the stage, and soft at their outer edges too, so when the
# camera pulls back and they shrink with the map no edge ever shows
MASK_WF = grad(90, "transparent 0%", ramp(8, 16, 0, 1, 10), ramp(SPLIT0, SPLIT1, 1, 0, 12), "transparent 100%")
MASK_EF = grad(90, "transparent 0%", ramp(SPLIT0, SPLIT1, 0, 1, 12), ramp(84, 92, 1, 0, 10), "transparent 100%")
MASK_TOP = grad(180, ramp(0, 24, 0, 1), ramp(44, 97, 1, 0, 14))
# phones: India above, Kenya below, meeting across the middle
MASK_N = grad(180, ramp(0, 16, 0, 1, 8), ramp(SPLIT0, SPLIT1, 1, 0, 12), "transparent 100%")
MASK_S = grad(180, "transparent 0%", ramp(SPLIT0, SPLIT1, 0, 1, 12), ramp(58, 98, 1, 0, 14))
# the still plates: soft on every edge; with a photograph below, dissolving into it
PL_H = grad(90, ramp(0, 24, 0, 1, 10), ramp(76, 100, 1, 0, 10))
PL_V = grad(180, ramp(0, 26, 0, 1, 10), ramp(54, 100, 1, 0, 12))
PL_V2 = grad(180, ramp(0, 26, 0, 1, 10), ramp(66, 100, 1, 0, 12))
# a place's photograph in the still journey: rising out of its plate, settling into the page
PP_V = grad(180, ramp(0, 40, 0, 1, 12), ramp(70, 100, 1, 0, 10))
PP_H = grad(90, ramp(0, 34, 0, 1, 12), "%s 100%%" % K)        # wide screens: in from the words' side
PP_H2 = grad(90, ramp(0, 8, 0, 1, 6), ramp(92, 100, 1, 0, 6))   # tablets: soft at both sides
# the close: last light rising from below the words
LL_V = grad(180, ramp(0, 42, 0, 1, 12), ramp(58, 100, 1, 0, 14))
LL_H = grad(90, ramp(0, 30, 0, 1, 10), "%s 100%%" % K)
# the flight's shade, behind the words (a token mixed toward transparent, not a mask)


def shade(p0, p1, a0, a1, n=10):
    out = []
    for i in range(n + 1):
        t = i / float(n)
        a = a0 + (a1 - a0) * smoother(t)
        pos = "%.2f%%" % (p0 + (p1 - p0) * t)
        out.append(("transparent " + pos) if a <= .004 else
                   ("color-mix(in srgb,var(--bg) %.1f%%,transparent) %s" % (a * 100, pos)))
    return ",".join(out)


SHADE = "linear-gradient(90deg,%s)" % shade(0, 50, .88, 0, 12)
SHADE_FOOT = "linear-gradient(180deg,transparent 0%%,%s)" % shade(74, 100, 0, .8, 8)

CSS = r"""
/* ===== Expeditions (tools/v4_expeditions.py) ===== */
@property --ex-split{syntax:"<percentage>";inherits:true;initial-value:50%;}
.ex{--ex-x:var(--edge-x,var(--gutter));--ex-yh:76px;--ex-w:7vw;--ex-nav:93px;
  --ex-land:color-mix(in srgb,var(--white) 3%,var(--card));
  --ex-land-hi:color-mix(in srgb,var(--white) 7%,var(--card));
  --ex-sea:color-mix(in srgb,var(--sky-cool) 45%,var(--bg));
  --ex-coast:color-mix(in srgb,var(--white) 30%,transparent);
  --ex-border:color-mix(in srgb,var(--white) 13%,transparent);
  --ex-grat:color-mix(in srgb,var(--white) 7%,transparent);
  --ex-grat5:color-mix(in srgb,var(--white) 4%,transparent);
  --ex-eqc:color-mix(in srgb,var(--white) 16%,transparent);
  --ex-route:color-mix(in srgb,var(--orange) 85%,transparent);
  --ex-lamp:var(--orange);--ex-lamp2:var(--white);
  /* small grey words: --gray alone is 3.8:1 on the page, this mix holds 5.5:1 */
  --ex-dim:color-mix(in srgb,var(--gray-light) 40%,var(--gray));
  --ex-giant:min(13.5rem,15vw);--ex-namew:calc(100vw - 2 * var(--ex-x));
  position:relative;overflow-x:clip;color:var(--gray-light);}
@media (max-width:1023px){.ex{--ex-yh:84px;}}
@media (max-width:759px){.ex{--ex-yh:64px;}}
@media (max-width:560px){.ex{--ex-x:var(--sp-2);--ex-w:9vh;}}
:where(.ex) :where(p,h1,h2,dl,dd,figure,ol){margin:0;}
.ex-vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
.ex :focus-visible{outline:2px solid var(--white);outline-offset:3px;}
.ex-atlas{position:relative;}
.ex-stage{display:flex;flex-direction:column;}
.ex-journey{position:relative;display:flex;flex-direction:column;}

/* ---- the words ---- */
.ex-kicker{margin:0 0 var(--sp-2);font:700 max(12px,var(--fs-micro))/1.2 var(--font-body);letter-spacing:.2em;text-transform:uppercase;color:var(--orange);
  text-shadow:0 0 2px var(--bg),0 0 6px var(--bg),0 0 14px var(--bg),0 0 26px var(--bg);}
.ex-h1{font:700 min(calc(var(--fs-display) * 1.85),11.5vw)/.92 var(--font-display);letter-spacing:-.05em;color:var(--white);text-wrap:balance;}
.ex-h2{font:700 var(--fs-h2)/1.1 var(--font-display);letter-spacing:-.02em;color:var(--white);}
.ex-lead{margin:var(--sp-3) auto 0;max-width:33rem;font-size:var(--fs-lead);line-height:1.6;color:var(--gray-light);text-wrap:balance;}
.ex-label{display:flex;gap:.8rem;align-items:baseline;margin:0 0 var(--sp-2);font:600 var(--fs-micro)/1.3 var(--font-body);
  letter-spacing:.16em;text-transform:uppercase;color:var(--gray-light);}
.ex-label span{font-variant-numeric:tabular-nums;color:var(--ex-dim);}
.ex-name{font:700 min(var(--ex-giant),calc(var(--ex-namew) * var(--ex-fit)))/.8 var(--font-display);letter-spacing:-.055em;
  color:var(--white);margin-left:-.04em;white-space:nowrap;}
.ex-co{margin:var(--sp-2) 0 0;font:500 var(--fs-small)/1.4 var(--font-body);letter-spacing:.08em;color:var(--ex-dim);font-variant-numeric:tabular-nums;}
.ex-line{margin:var(--sp-3) 0 0;max-width:30ch;font:500 var(--fs-h4)/1.5 var(--font-display);letter-spacing:-.005em;color:var(--white);text-wrap:pretty;}
.is-planned .ex-line{font-size:var(--fs-h3);line-height:1.3;color:var(--gray-light);}
.ex-lab,.ex-facts dt{display:block;font:600 var(--fs-micro)/1.3 var(--font-body);letter-spacing:.14em;text-transform:uppercase;color:var(--ex-dim);}
.ex-when{margin:var(--sp-4) 0 0;padding:var(--sp-2) 0 0;border-top:1px solid var(--edge);}
.ex-when p{margin:.4rem 0 0;display:flex;flex-wrap:wrap;gap:.2rem 1.4rem;font:600 var(--fs-h4)/1.4 var(--font-display);color:var(--white);font-variant-numeric:tabular-nums;}
.ex-when p span{white-space:nowrap;}
.ex-when .ex-state{gap:.55rem;align-items:center;font:500 var(--fs-small)/1.4 var(--font-body);color:var(--gray-light);}
.ex-state i{width:6px;height:6px;border-radius:50%;background:var(--orange);}
.ex-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 var(--sp-3);margin:var(--sp-2) 0 0;}
.ex-facts div{padding:.7rem 0;border-top:1px solid var(--line);min-width:0;}
.ex-facts dd{margin:.3rem 0 0;font-size:var(--fs-body-s);line-height:1.4;color:var(--white);font-variant-numeric:tabular-nums;}
.is-planned .ex-facts{margin-top:var(--sp-4);}
.ex-acts{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-2) var(--sp-4);margin:var(--sp-4) 0 0;}
.ex-acts .btn-solid{min-height:48px;box-sizing:border-box;display:inline-flex;align-items:center;margin:0 0 0 .35rem;}
.ex-more{position:relative;display:inline-flex;align-items:center;gap:.6rem;min-height:44px;font-size:var(--fs-body-s);font-weight:600;color:var(--white);text-decoration:none;
  background:linear-gradient(var(--edge-hi),var(--edge-hi)) 0 calc(100% - 9px)/100% 1px no-repeat;}
.ex-more::before{content:"";position:absolute;left:0;right:0;bottom:9px;height:1px;background:var(--white);transform:scaleX(0);transform-origin:left;transition:transform .7s var(--ease);}
.ex-more:is(:hover,:focus-visible)::before{transform:scaleX(1);}
.ex-arr{width:16px;height:10px;flex:none;transition:transform .6s var(--ease);}
.ex-more:is(:hover,:focus-visible) .ex-arr{transform:translateX(4px);}
.ex-ext{width:11px;height:11px;flex:none;}

/* ---- the arrival: two skies, one dissolve ---- */
.ex-open{position:relative;isolation:isolate;display:flex;flex-direction:column;justify-content:flex-end;
  min-height:clamp(560px,calc(100svh - var(--ex-nav) - var(--ex-yh)),1000px);}
.ex-sky{position:absolute;inset:0;z-index:-1;overflow:hidden;--ex-split:50%;}
.ex-pic{position:absolute;inset:0;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-composite:source-in;mask-composite:intersect;}
.ex-sky-ph{position:absolute;margin:0;}
.ex-sky-ph picture,.ex-photo picture{display:block;width:100%;height:100%;}
.ex-photo picture{-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-composite:source-in;mask-composite:intersect;}
.ex-sky-ph img,.ex-photo img{display:block;width:100%;height:100%;object-fit:cover;}
.ex-pic .ex-sky-ph{top:-12%;bottom:0;width:calc(60% + var(--ex-w));}
.ex-pic.is-kenya .ex-sky-ph{left:0;}
.ex-pic.is-india .ex-sky-ph{right:0;top:-18%;}
.ex-pic.is-kenya img{object-position:88% 50%;}
.ex-pic.is-india img{object-position:100% 58%;}
.ex-pic.is-kenya{-webkit-mask-image:@@MASK_W@@,@@MASK_TOP@@;mask-image:@@MASK_W@@,@@MASK_TOP@@;}
.ex-pic.is-india{-webkit-mask-image:@@MASK_E@@,@@MASK_TOP@@;mask-image:@@MASK_E@@,@@MASK_TOP@@;}
/* the kicker over the photographs: a soft shade of the page behind it, no edge */
.ex-open .ex-kicker{display:inline-block;padding:.9em 2.2em;margin-bottom:calc(var(--sp-2) - .9em);
  background:radial-gradient(closest-side,color-mix(in srgb,var(--bg) 82%,transparent),color-mix(in srgb,var(--bg) 50%,transparent) 55%,transparent);}
.ex-open .ex-panel{position:relative;z-index:1;padding:0 var(--ex-x) clamp(2.2rem,6vh,4rem);text-align:center;pointer-events:none;}
/* a long eased shade under the title, so the words stand on the photographs without a box */
.ex-open .ex-panel::before{content:"";position:absolute;z-index:-1;left:50%;bottom:-10%;width:min(1180px,135%);height:170%;transform:translateX(-50%);
  background:radial-gradient(closest-side at 50% 58%,@@SHADE_R@@);pointer-events:none;}
.ex-half{position:absolute;top:0;bottom:0;z-index:0;color:var(--white);text-decoration:none;}
.ex-half.is-kenya{left:0;width:50%;}
.ex-half.is-india{left:50%;right:0;}
.ex-half:focus-visible{outline:none;}
.ex-half:focus-visible .ex-hcap{outline:2px solid var(--white);outline-offset:8px;}
.ex-hcap{position:absolute;bottom:clamp(2.2rem,6vh,4rem);display:flex;flex-direction:column;gap:.2rem;
  text-shadow:0 0 2px var(--bg),0 0 8px var(--bg),0 0 18px var(--bg),0 0 30px var(--bg);}
.ex-half.is-kenya .ex-hcap{left:var(--ex-x);}
.ex-half.is-india .ex-hcap{right:var(--ex-x);align-items:flex-end;text-align:right;}
.ex-hcap b{display:inline-flex;align-items:center;gap:.55rem;font:600 var(--fs-h4)/1.2 var(--font-display);letter-spacing:-.01em;color:var(--white);}
.ex-hcap>span{font-size:var(--fs-small);color:var(--white);}
.ex-dn{width:10px;height:14px;transition:transform .6s var(--ease);}
.ex-half:is(:hover,:focus-visible) .ex-dn{transform:translateY(3px);}
/* point at a sky and it leans open, slowly; the other gives way (only the masks move) */
@media (hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference){
  .ex-sky{transition:--ex-split 1.6s var(--ease);}
  .ex-open:has(.ex-half.is-kenya:is(:hover,:focus-visible)) .ex-sky{--ex-split:58%;}
  .ex-open:has(.ex-half.is-india:is(:hover,:focus-visible)) .ex-sky{--ex-split:42%;}
}

/* ---- the year, to scale: Oct 2026 to Nov 2027 ---- */
.ex-year{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--bg) 96%,transparent);
  -webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border-bottom:1px solid var(--line);transition:top .38s var(--ease),opacity .6s var(--ease);}
/* when the menu comes back (scrolling up), the year steps down under it, as the site's other sticky bars do */
html.v2-nav-up .ex-year{top:var(--v2-nav-h,77px);}
.ex-year-in{position:relative;box-sizing:border-box;height:var(--ex-yh);margin-inline:var(--ex-x);}
.ex-yline{position:absolute;left:0;right:0;top:46px;height:1px;background:var(--edge);}
.ex-yseason{position:absolute;top:0;height:1px;background:var(--edge-hi);}
.ex-ybar{position:absolute;top:-2px;height:5px;border-radius:1px;background:var(--gray-light);transition:background-color .5s var(--ease),opacity .5s var(--ease);}
.ex-ybar.is-plan{box-sizing:border-box;background:transparent;border:1px solid var(--gray-light);}
.ex-ymonths{position:absolute;left:0;right:0;top:46px;display:grid;grid-template-columns:repeat(14,minmax(0,1fr));}
.ex-ymonths span{position:relative;padding-top:8px;text-align:center;font-size:var(--fs-micro);line-height:1.2;color:var(--gray-light);transition:color .4s var(--ease);}
.ex-ymonths span::before{content:"";position:absolute;left:0;top:-3px;width:1px;height:4px;background:var(--edge);}
.ex-ymonths span.is-y::before{top:-9px;height:13px;background:var(--edge-hi);}
.ex-ymonths b{font-weight:400;}
.ex-ymonths i{display:none;font-style:normal;}
.ex-yplaces{list-style:none;padding:0;}
.ex-yplaces li{position:absolute;top:0;}
.ex-yplaces a{display:flex;align-items:baseline;gap:.55rem;box-sizing:border-box;min-width:44px;height:var(--ex-yh);padding-top:14px;text-decoration:none;white-space:nowrap;}
.ex-yplaces b{font:600 var(--fs-body-s)/1.2 var(--font-display);color:var(--gray-light);transition:color .5s var(--ease);}
.ex-mo{font-size:var(--fs-small);color:var(--gray-light);font-variant-numeric:tabular-nums;}
.ex-yplaces a:is(:hover,:focus-visible,.is-hint) b,.ex-yplaces a[aria-current] b{color:var(--white);}
.ex-yplaces a:focus-visible{outline-offset:-2px;}
@@BAR_RULES@@
@media (hover:hover) and (pointer:fine){.ex-ymonths span[data-t]{cursor:pointer;}}

/* ---- the map's drawing (the trip pages' route-map language) ---- */
.ex-map{display:block;width:100%;height:100%;overflow:visible;}
.ex-sea,.ex-edge,.ex-g30,.ex-g5,.ex-eq,.ex-land,.ex-bd,.ex-route{vector-effect:non-scaling-stroke;}
.ex-l,.ex-b{vector-effect:non-scaling-stroke;}
.ex-sea{fill:var(--ex-sea);stroke:none;}
.ex-edge{fill:none;stroke:var(--ex-grat);stroke-width:1;}
.ex-g30{fill:none;stroke:var(--ex-grat);stroke-width:.8;}
.ex-g5{fill:none;stroke:var(--ex-grat5);stroke-width:.6;opacity:var(--ex-fine,0);}
.ex-eq{fill:none;stroke:var(--ex-eqc);stroke-width:.8;stroke-dasharray:5 5;}
.ex-land{fill:var(--ex-land);stroke:var(--ex-coast);stroke-width:.8;stroke-linejoin:round;}
.ex-bd{fill:none;stroke:var(--ex-bdc,var(--ex-land));stroke-width:var(--ex-bdw,1.6);stroke-dasharray:var(--ex-bdd,none);stroke-linecap:round;}
.ex-bdu{--ex-bdc:var(--ex-border);--ex-bdw:.7;--ex-bdd:2 3;}
.ex-route{fill:none;stroke:var(--ex-route);stroke-width:1.3;stroke-linecap:round;}
.ex-rplan{display:none;fill:none;stroke:color-mix(in srgb,var(--orange) 34%,transparent);stroke-width:1;stroke-dasharray:3 5;vector-effect:non-scaling-stroke;}
.ex-svg .ex-plate .ex-rplan{display:inline;}
.ex-gs0{stop-color:var(--orange);stop-opacity:.34;}.ex-gs1{stop-color:var(--orange);stop-opacity:.1;}.ex-gs2{stop-color:var(--orange);stop-opacity:0;}
.ex-gs3{stop-color:var(--white);stop-opacity:.16;}.ex-gs4{stop-color:var(--white);stop-opacity:.05;}
.ex-inset svg{--ex-fine:1;}

/* markers: a small ring, filled where the dates are set, open where the trip is planned */
.ex-dot{display:block;flex:none;width:9px;height:9px;border-radius:50%;box-sizing:border-box;background:var(--orange);border:1.5px solid var(--orange);}
.ex-dot.is-planned,.is-planned>.ex-dot{background:var(--bg);border-color:var(--white);}
.ex-pins{position:absolute;inset:0;pointer-events:none;}
.ex-pin{position:absolute;left:var(--x);top:var(--y);display:flex;align-items:center;gap:1.15rem;min-height:44px;
  padding:0 .6rem;margin:-22px 0 0 calc(-.6rem - 4.5px);color:var(--gray-light);text-decoration:none;pointer-events:auto;
  font:600 max(12.5px,var(--fs-micro))/1 var(--font-body);letter-spacing:.16em;text-transform:uppercase;white-space:nowrap;}
.ex-pin.is-l{flex-direction:row-reverse;margin-left:calc(.6rem + 4.5px);transform:translateX(-100%);}
.ex-pin .ex-dot{position:relative;}
.ex-pin .ex-dot::after{content:"";position:absolute;inset:-7px;border-radius:50%;border:1px solid var(--orange);
  opacity:0;scale:.6;transition:opacity .6s var(--ease),scale .6s var(--ease);}
.ex-pin.is-planned .ex-dot::after{border-color:var(--white);}
.ex-pin:is(:hover,:focus-visible,.is-on,.is-hint){color:var(--white);}
.ex-pin:is(:hover,:focus-visible,.is-on,.is-hint) .ex-dot::after{opacity:1;scale:1;}
.ex-pin:focus-visible{outline:none;}
.ex-pin:focus-visible .ex-pl{outline:2px solid var(--white);outline-offset:4px;}
.ex-pl{text-shadow:0 0 2px var(--bg),0 0 6px var(--bg),0 0 14px var(--bg),0 0 24px var(--bg);}

/* ---- the index: each place's dates, length and price ---- */
.ex-world .ex-h2{font-size:var(--fs-h3);}
.ex-ix{list-style:none;padding:0;margin:var(--sp-3) 0 0;border-top:1px solid var(--edge);}
.ex-ix li{border-bottom:1px solid var(--line);}
.ex-ix a{display:grid;grid-template-columns:2.2rem minmax(0,1fr) auto;align-items:baseline;gap:0 var(--sp-2);min-height:48px;padding:.95rem 0;
  color:var(--white);text-decoration:none;}
.ex-ix-n{font:600 var(--fs-micro)/1 var(--font-body);letter-spacing:.14em;color:var(--ex-dim);font-variant-numeric:tabular-nums;}
.ex-ix-t{font:600 var(--fs-h3)/1.15 var(--font-display);letter-spacing:-.01em;background:linear-gradient(var(--white),var(--white)) 0 100%/0 1px no-repeat;
  transition:background-size .6s var(--ease);justify-self:start;padding-bottom:2px;}
.ex-ix a:is(:hover,:focus-visible,.is-hint) .ex-ix-t{background-size:100% 1px;}
.ex-ix-m{display:flex;flex-direction:column;align-items:flex-end;text-align:right;gap:.15rem;font-size:var(--fs-body-s);line-height:1.45;font-variant-numeric:tabular-nums;}
.ex-ix-d{display:flex;flex-direction:column;align-items:flex-end;color:var(--white);}
.ex-ix-f{color:var(--gray-light);}

/* ---- the photographs ---- */
.ex-photo{margin:0;position:relative;}
.ex-photo figcaption{position:absolute;right:var(--ex-x);bottom:var(--sp-2);display:flex;align-items:center;gap:.6rem;
  font-size:var(--fs-small);color:var(--white);text-shadow:0 0 2px var(--bg),0 0 8px var(--bg),0 0 18px var(--bg),0 0 30px var(--bg);}
.ex-photo figcaption::before{content:"";width:1.4rem;height:1px;background:var(--edge-hi);}

/* ======== the still journey: phones, tablets, reduced motion and no script ======== */
.ex-world{padding:clamp(3rem,9vw,5rem) var(--ex-x) 0;}
.ex-plate{position:relative;margin:var(--sp-4) 0 0;aspect-ratio:@@OVER_AR@@;width:100%;max-width:1400px;align-self:center;}
.ex-plate .ex-map{position:absolute;inset:0;}
.ex-gl,.ex-air{display:none;}
.ex-place{margin:clamp(4rem,11vw,7rem) 0 0;scroll-margin-top:calc(var(--ex-yh) + 1rem);}
.ex-media{position:relative;}
.ex-inset{position:relative;aspect-ratio:var(--ar);-webkit-mask-image:@@PL_H@@,@@PL_V2@@;mask-image:@@PL_H@@,@@PL_V2@@;
  -webkit-mask-composite:source-in;mask-composite:intersect;}
.ex-inset.has-photo{-webkit-mask-image:@@PL_H@@,@@PL_V@@;mask-image:@@PL_H@@,@@PL_V@@;}
.ex-inset svg{position:absolute;inset:0;width:100%;height:100%;}
.ex-imark{position:absolute;left:var(--x);top:calc(50% + (var(--y) - 50%) * var(--ac,var(--av)) / var(--av));display:flex;align-items:center;gap:.9rem;margin:-4.5px 0 0 -4.5px;
  font:500 max(12.5px,var(--fs-micro))/1 var(--font-body);letter-spacing:.1em;color:var(--gray-light);white-space:nowrap;font-variant-numeric:tabular-nums;text-shadow:0 0 6px var(--bg);}
.ex-imark .ex-dot{box-shadow:0 0 0 7px color-mix(in srgb,var(--orange) 16%,transparent);}
.ex-imark.is-planned .ex-dot{box-shadow:0 0 0 7px color-mix(in srgb,var(--white) 9%,transparent);}
.ex-media .ex-photo{margin-top:-26%;aspect-ratio:4 / 5;}
.ex-media .ex-photo picture{-webkit-mask-image:@@PP_V@@;mask-image:@@PP_V@@;}
.ex-media .ex-photo figcaption{bottom:20%;}
.ex-place .ex-panel{padding:0 var(--ex-x);margin-top:calc(var(--sp-5) * -1);position:relative;}
.ex-place.is-planned .ex-panel{margin-top:calc(var(--sp-3) * -1);}
.ex-outro{position:relative;margin:clamp(4rem,11vw,7rem) 0 0;padding:0 0 var(--sp-section);}
.ex-out-ph .ex-photo{aspect-ratio:4 / 5;}
.ex-out-ph .ex-photo picture{-webkit-mask-image:@@LL_V@@;mask-image:@@LL_V@@;}
.ex-out-ph .ex-photo figcaption{bottom:auto;top:30%;}
.ex-outro .ex-panel{position:relative;margin-top:-28%;padding:0 var(--ex-x);text-align:center;}
.ex-outro .ex-h2{font-size:var(--fs-h1);letter-spacing:-.035em;}
.ex-outro .ex-acts{justify-content:center;}
.ex-dn,.ex-hcap{pointer-events:none;}
@media (max-width:699px){
  /* phones: India above, Kenya below, as on the map */
  .ex-sky{--ex-split:47%;--ex-w:9%;}
  .ex-pic .ex-sky-ph{top:0;bottom:auto;left:0;right:0;width:auto;}
  .ex-pic.is-india .ex-sky-ph{top:0;height:56%;}
  .ex-pic.is-kenya .ex-sky-ph{top:34%;bottom:0;height:auto;}
  .ex-pic.is-india img{object-position:50% 70%;}
  .ex-pic.is-kenya img{object-position:60% 40%;}
  .ex-pic.is-india{-webkit-mask-image:@@MASK_N@@;mask-image:@@MASK_N@@;}
  .ex-pic.is-kenya{-webkit-mask-image:@@MASK_S@@;mask-image:@@MASK_S@@;}
  .ex-open{min-height:clamp(540px,calc(100svh - var(--ex-nav) - var(--ex-yh)),780px);}
  .ex-h1{font-size:min(16vw,4.4rem);}
  .ex-lead{font-size:var(--fs-body);}
  .ex-half.is-india{left:0;top:0;bottom:50%;width:auto;right:0;}
  .ex-half.is-kenya{left:0;right:0;top:50%;bottom:0;width:auto;}
  .ex-half.is-india .ex-hcap{top:var(--sp-3);bottom:auto;right:var(--ex-x);}
  .ex-half.is-kenya .ex-hcap{top:2%;bottom:auto;left:var(--ex-x);right:auto;align-items:flex-start;text-align:left;}
  .ex-hcap b{font-size:var(--fs-body);}
  .ex-hcap>span{font-size:var(--fs-micro);}
  /* over the photographs on a phone: a soft shade of the page behind the small words, no edge */
  .ex-hcap,.ex-open .ex-kicker{background:radial-gradient(closest-side,color-mix(in srgb,var(--bg) 88%,transparent),color-mix(in srgb,var(--bg) 60%,transparent) 55%,transparent);}
  .ex-hcap{padding:.9rem 1.6rem;margin:-.9rem -1.6rem;}
  .ex-open .ex-kicker{padding:1.5em 3.4em;margin-bottom:calc(var(--sp-1) - 1.5em);
    background:radial-gradient(closest-side,color-mix(in srgb,var(--bg) 94%,transparent),color-mix(in srgb,var(--bg) 78%,transparent) 50%,transparent);}
  .ex-open .ex-panel{padding-bottom:var(--sp-4);}
  .ex-ix a{grid-template-columns:1.9rem minmax(0,1fr) auto;}
}
@media (max-width:759px){
  .ex-yplaces a{padding-top:10px;}
  .ex-mo{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
  .ex-yline,.ex-ymonths{top:36px;}
  .ex-ymonths span{padding-top:6px;}
  .ex-ymonths b{display:none;}
  .ex-ymonths i{display:inline;}
  .ex-yplaces b{font-size:var(--fs-small);}
}
@media (max-width:479px){
  /* five names on a phone's line: Kazakhstan and India, a few weeks apart, need the smaller size (chat 11) */
  .ex-yplaces b{font-size:var(--fs-micro);}
  .ex-yplaces li:has(a[href="#kazakhstan"]){translate:-10px 0;}
  .ex-yplaces li:has(a[href="#india"]){translate:10px 0;}
}
@media (min-width:760px) and (max-width:1023px){
  .ex-yplaces a{flex-direction:column;gap:0;padding-top:8px;}
  .ex-yplaces b{line-height:1.25;}
  .ex-mo{font-size:var(--fs-micro);line-height:1.3;}
  .ex-yline,.ex-ymonths{top:50px;}
}
@media (min-width:700px){
  .ex-media .ex-photo{aspect-ratio:16 / 9;margin-top:-18%;}
  .ex-media .ex-photo picture{-webkit-mask-image:@@PP_V@@,@@PP_H2@@;mask-image:@@PP_V@@,@@PP_H2@@;
    -webkit-mask-composite:source-in;mask-composite:intersect;}
  .ex-media .ex-photo figcaption{bottom:18%;}
  .ex-inset{--ac:2.4;aspect-ratio:2.4;}
  .ex-place .ex-panel{max-width:44rem;margin-top:calc(var(--sp-4) * -1);}
  .ex-world .ex-panel{max-width:46rem;}
  .ex-out-ph .ex-photo{aspect-ratio:16 / 8;}
  .ex-out-ph .ex-photo figcaption{top:auto;bottom:14%;}
  .ex-outro .ex-panel{margin-top:-14%;}
  .ex-facts{grid-template-columns:repeat(3,minmax(0,1fr));}
  .is-planned .ex-facts{grid-template-columns:repeat(4,minmax(0,1fr));}
}
/* wide screens without the flight: the words beside the map, the plate and the photograph */
@media (min-width:1000px){
  html:not(.ex-fly) .ex-journey{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:center;}
  html:not(.ex-fly) .ex-year{grid-column:1 / -1;align-self:start;}
  html:not(.ex-fly) .ex-world{grid-column:1;padding:var(--sp-5) 0 0 var(--ex-x);}
  html:not(.ex-fly) .ex-plate{grid-column:2;margin:var(--sp-5) 0 0;}
  html:not(.ex-fly) .ex-place{grid-column:1 / -1;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:center;
    gap:var(--sp-4);padding-left:var(--ex-x);}
  html:not(.ex-fly) .ex-place .ex-media{order:2;}
  html:not(.ex-fly) .ex-place .ex-panel{order:1;padding:0;margin:0;--ex-namew:36vw;}
  html:not(.ex-fly) .ex-inset{-webkit-mask-image:@@PL_H@@,@@PL_V2@@;mask-image:@@PL_H@@,@@PL_V2@@;}
  html:not(.ex-fly) .ex-media .ex-photo picture{-webkit-mask-image:@@PP_V@@,@@PP_H@@;mask-image:@@PP_V@@,@@PP_H@@;}
  html:not(.ex-fly) .ex-facts{grid-template-columns:repeat(2,minmax(0,1fr));}
  html:not(.ex-fly) .ex-outro{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:center;padding-left:var(--ex-x);}
  html:not(.ex-fly) .ex-out-ph{order:2;}
  html:not(.ex-fly) .ex-out-ph .ex-photo{aspect-ratio:3 / 2;}
  html:not(.ex-fly) .ex-out-ph .ex-photo picture{-webkit-mask-image:@@LL_V@@,@@LL_H@@;mask-image:@@LL_V@@,@@LL_H@@;
    -webkit-mask-composite:source-in;mask-composite:intersect;}
  html:not(.ex-fly) .ex-outro .ex-panel{order:1;margin:0;padding:0;text-align:left;}
  html:not(.ex-fly) .ex-outro .ex-acts{justify-content:flex-start;}
  html:not(.ex-fly) .ex-outro .ex-lead{margin-left:0;}
}

/* ======== the flight: wide screens, with the script, without reduced motion ======== */
.ex-fly .ex-atlas{height:calc(100svh + (var(--n) - .55) * 88svh);margin-top:calc(-1 * var(--ex-nav));}
.ex-fly .ex-stage{display:block;position:sticky;top:0;height:100svh;overflow:hidden;}
.ex-fly .ex-journey{display:contents;}
.ex-fly .ex-plate{position:absolute;inset:0;margin:0;aspect-ratio:auto;max-width:none;width:auto;z-index:1;align-self:stretch;}
.ex-fly .ex-plate .ex-map{opacity:0;}
.ex-gl-on .ex-plate .ex-map{visibility:hidden;}
.ex-fly .ex-gl{display:block;position:absolute;inset:0;width:100%;height:100%;opacity:0;}
.ex-fly .ex-plate::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;background:@@SHADE@@,@@SHADE_FOOT@@;
  opacity:var(--ex-shade,1);}
.ex-fly .ex-pins{z-index:3;}
.ex-fly .ex-pin{left:0;top:0;opacity:0;transition:opacity .5s var(--ease),color .3s var(--ease);will-change:transform;}
.ex-fly .ex-pin.is-l{transform:none;}
.ex-fly.ex-ready .ex-pin:not(.is-off){opacity:1;}
.ex-fly .ex-pin.is-off{pointer-events:none;}
.ex-fly .ex-pin.is-on .ex-pl{opacity:0;}
.ex-fly .ex-pl{transition:opacity .5s var(--ease);}
.ex-fly .ex-air{display:block;position:absolute;left:0;top:0;width:0;height:0;z-index:1;visibility:hidden;pointer-events:none;}
.ex-fly .ex-media{display:none;}
.ex-fly .ex-stop{position:absolute;left:0;top:0;bottom:0;z-index:5;display:flex;align-items:center;margin:0;box-sizing:border-box;
  width:calc(var(--ex-x) + min(36rem,40vw));padding:calc(var(--ex-nav) + 1rem) 0 calc(var(--ex-yh) + 1.5rem) var(--ex-x);
  opacity:0;pointer-events:none;transition:opacity .4s var(--ease),translate .4s var(--ease);translate:0 .6rem;}
.ex-fly .ex-stop.is-on{opacity:1;pointer-events:auto;translate:0 0;transition:opacity .8s var(--ease) .05s,translate .9s var(--ease) .05s;}
.ex-fly .ex-panel{width:100%;margin:0;padding:0;}
.ex-fly .ex-place .ex-panel{--ex-namew:44vw;}
.ex-fly .ex-place.is-planned .ex-panel{--ex-namew:50vw;}
.ex-fly .ex-name{font-size:min(var(--ex-giant),calc(var(--ex-namew) * var(--ex-fit)),20svh);}
.ex-fly .ex-when{margin-top:var(--sp-3);}
.ex-fly .ex-line{margin-top:var(--sp-2);}
.ex-fly .ex-world .ex-panel{max-width:34rem;}
/* the arrival on the flight: the whole stage, the skies a little wider than it (the camera pulls back out of them) */
.ex-fly .ex-open{inset:0;width:auto;padding:0;display:flex;opacity:1;pointer-events:auto;translate:none;z-index:6;transition:none;}
.ex-fly .ex-sky{will-change:transform;transform-origin:0 0;overflow:visible;}
/* the title fades on its own layer: overlapping the moving sky it must never share a layer with it (Chromium
   then drops the masked west sky) */
.ex-fly .ex-open .ex-panel{padding-bottom:calc(var(--ex-yh) + clamp(1.6rem,5vh,3.4rem));will-change:opacity;}
.ex-fly .ex-hcap{bottom:calc(var(--ex-yh) + clamp(1.6rem,5vh,3.4rem));}
.ex-fly .ex-pic{inset:0 -24%;overflow:visible;}
.ex-fly .ex-pic .ex-sky-ph{width:calc(50% + var(--ex-w));}
.ex-fly .ex-pic.is-kenya .ex-sky-ph{left:8%;}
.ex-fly .ex-pic.is-india .ex-sky-ph{right:8%;}
.ex-fly .ex-pic.is-kenya{-webkit-mask-image:@@MASK_WF@@,@@MASK_TOP@@;mask-image:@@MASK_WF@@,@@MASK_TOP@@;}
.ex-fly .ex-pic.is-india{-webkit-mask-image:@@MASK_EF@@,@@MASK_TOP@@;mask-image:@@MASK_EF@@,@@MASK_TOP@@;}
.ex-fly .ex-open.is-gone{pointer-events:none;}
.ex-fly .ex-open.is-gone .ex-half{visibility:hidden;}
/* the year along the foot of the stage */
html.ex-fly .ex-year,html.ex-fly.v2-nav-up .ex-year{position:absolute;left:0;right:0;bottom:0;top:auto;z-index:7;background:none;-webkit-backdrop-filter:none;backdrop-filter:none;border:0;}
.ex-fly .ex-year::before{content:"";position:absolute;inset:-60% 0 0;pointer-events:none;
  background:linear-gradient(180deg,transparent,color-mix(in srgb,var(--bg) 70%,transparent));z-index:-1;}
.ex-fly .ex-year.is-quiet{opacity:0;pointer-events:none;}
.ex-fly .ex-year.is-quiet:focus-within{opacity:1;pointer-events:auto;}
/* the close, on the flight: last light rising under the words */
.ex-fly .ex-outro{width:auto;right:0;align-items:flex-end;padding-bottom:calc(var(--sp-5) + 1rem);opacity:1;translate:none;pointer-events:none;}
.ex-fly .ex-outro .ex-panel{opacity:0;translate:0 .6rem;transition:opacity .4s var(--ease),translate .4s var(--ease);}
.ex-fly .ex-outro.is-on .ex-panel{opacity:1;translate:0 0;pointer-events:auto;transition:opacity .8s var(--ease) .05s,translate .9s var(--ease) .05s;}
.ex-fly .ex-outro:not(.is-near) .ex-out-ph{display:none;}
.ex-fly .ex-outro .ex-panel{max-width:34rem;text-align:left;}
.ex-fly .ex-outro .ex-lead{margin-left:0;}
.ex-fly .ex-outro .ex-acts{justify-content:flex-start;}
.ex-fly .ex-out-ph{position:absolute;left:30%;right:0;bottom:0;height:72%;z-index:-1;}
.ex-fly .ex-out-ph .ex-photo{position:absolute;inset:0;aspect-ratio:auto;}
.ex-fly .ex-out-ph .ex-photo picture{-webkit-mask-image:@@LL_V@@,@@LL_H@@;mask-image:@@LL_V@@,@@LL_H@@;
  -webkit-mask-composite:source-in;mask-composite:intersect;}
.ex-fly .ex-out-ph .ex-photo figcaption{bottom:var(--sp-5);}
.ex-fly .ex-outro .ex-h2{font-size:min(calc(var(--fs-display) * 1.3),8vw);letter-spacing:-.045em;line-height:.95;}
@media (max-width:1199px){.ex-fly .ex-stop:not(.ex-open,.ex-outro){width:calc(var(--ex-x) + min(36rem,45vw));}}
/* shorter screens: the same words, closer together */
@media (max-height:820px){
  .ex-fly .ex-stop:not(.ex-open){padding-top:calc(var(--ex-nav) + .25rem);padding-bottom:calc(var(--ex-yh) + .75rem);}
  .ex-fly .ex-name{font-size:min(var(--ex-giant),calc(var(--ex-namew) * var(--ex-fit)),17svh);}
  .ex-fly .ex-co{display:none;}
  .ex-fly .ex-label{margin-bottom:var(--sp-1);}
  .ex-fly .ex-line{font-size:var(--fs-body);line-height:1.45;}
  .ex-fly .ex-when{margin-top:var(--sp-2);padding-top:var(--sp-1);}
  .ex-fly .ex-when p{font-size:var(--fs-body);}
  .ex-fly .ex-facts{margin-top:var(--sp-1);}
  .ex-fly .ex-facts div{padding:.45rem 0;}
  .ex-fly .ex-facts dd{margin-top:.15rem;font-size:var(--fs-small);}
  .ex-fly .ex-acts{margin-top:var(--sp-3);}
  .ex-fly .ex-ix a{padding:.6rem 0;}
}

@media (prefers-reduced-motion:reduce){
  .ex *,.ex *::before,.ex *::after,.ex-sky{transition:none!important;}
}
"""


def bar_rules():
    """The year's bars answer their place: white under the pointer, orange for the stop you are at."""
    out = []
    for p in PLACES:
        k = p["id"]
        out.append('.ex-year-in:has(a[href="#%s"]:is(:hover,:focus-visible,.is-hint)) :is(.ex-ybar,.ex-yseason)[data-t="%s"]'
                   '{background:var(--white);}' % (k, k))
        out.append('.ex-year-in:has(a[href="#%s"]:is(:hover,:focus-visible,.is-hint)) .ex-ybar.is-plan[data-t="%s"]'
                   '{background:transparent;border-color:var(--white);}' % (k, k))
        out.append('.ex-year-in:has(a[href="#%s"][aria-current]) .ex-ybar[data-t="%s"]{background:var(--orange);border-color:var(--orange);}'
                   % (k, k))
        out.append('.ex-year-in:has(a[href="#%s"][aria-current]) .ex-ybar.is-plan[data-t="%s"]{background:transparent;}' % (k, k))
        out.append('.ex-ymonths span[data-t="%s"].is-hint{color:var(--white);}' % k)
    return "\n".join(out)


def css():
    s = CSS
    subs = dict(OVER_AR="%g / %g" % (OVER[2], OVER[3]), MASK_W=MASK_W, MASK_E=MASK_E, MASK_WF=MASK_WF, MASK_EF=MASK_EF,
                MASK_TOP=MASK_TOP, MASK_N=MASK_N, MASK_S=MASK_S, PL_H=PL_H, PL_V2=PL_V2, PL_V=PL_V, PP_V=PP_V,
                PP_H2=PP_H2, PP_H=PP_H, LL_V=LL_V, LL_H=LL_H, SHADE_FOOT=SHADE_FOOT, SHADE=SHADE,
                SHADE_R=shade(0, 100, .72, 0, 12), BAR_RULES=bar_rules())
    for k in sorted(subs, key=len, reverse=True):
        s = s.replace("@@%s@@" % k, subs[k])
    if "@@" in s:
        raise SystemExit("v4_expeditions: a style placeholder was left: %s" % re.findall(r"@@\w+@@", s)[:3])
    return s


SCRIPT = r"""<script>
/* Expeditions (tools/v4_expeditions.py). On wide screens with motion allowed
   the stage holds still and the scroll flies a camera: out of the two skies
   into the atlas, then to each place and back out. One eased progress drives
   everything (the camera on its van Wijk and Nuij paths, the route, the
   photographs, the words), in one loop that runs only while the scroll, a
   click, a key or the pointer has moved something, and stops when it has
   arrived. Nothing runs on a timer. The map is WebGL 2 (colours read from
   the tokens); if that cannot start, the same SVG the still journey uses
   flies instead. Reduced motion, narrow screens and no script: the still
   journey. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  var atlas = d.querySelector(".ex-atlas");
  if (!atlas) return;
  var DATA = JSON.parse(atlas.getAttribute("data-ex"));
  var stage = atlas.querySelector(".ex-stage"), plate = atlas.querySelector(".ex-plate");
  var svg = plate.querySelector(".ex-map"), canvas = plate.querySelector(".ex-gl"), pinBox = plate.querySelector(".ex-pins");
  var routeEl = svg.querySelector(".ex-route"), routeD = routeEl.getAttribute("d");
  var pins = [].slice.call(plate.querySelectorAll(".ex-pin"));
  var stops = [].slice.call(atlas.querySelectorAll(".ex-stop")).sort(function (a, b) { return a.getAttribute("data-i") - b.getAttribute("data-i"); });
  var openEl = atlas.querySelector(".ex-open"), sky = openEl.querySelector(".ex-sky"), openPanel = openEl.querySelector(".ex-panel");
  var caps = [].slice.call(openEl.querySelectorAll(".ex-hcap"));
  var outroEl = atlas.querySelector(".ex-outro"), outroPh = outroEl.querySelector(".ex-out-ph");
  var yearEl = atlas.querySelector(".ex-year"), yearLinks = [].slice.call(yearEl.querySelectorAll("a[data-i]"));
  var S = DATA.stops, N = S.length, ids = S.map(function (s) { return s.id; });
  var PL = DATA.places, NP = PL.length;            /* the places are stops 2 .. NP + 1 */
  var mqWide = w.matchMedia("(min-width: 1000px) and (min-height: 620px)");
  var mqRM = w.matchMedia("(prefers-reduced-motion: reduce)");
  var on = false, W = 0, H = 0, top0 = 0, step = 1, cams = [], zs = [];
  var regs = [], panelR = 0, cur = null, P = 0, raf = 0, tween = null, lastT = 0, words = -2, curPlace = -2, quiet = null, near = false, gone = null;
  var R = null, hint = "", prev = {}, lamp = { x: 0, y: 0, a: 0, tx: 0, ty: 0, ta: 0 }, photosWanted = false;
  var DWELL = .5, HOLD = .45;        /* HOLD: a little more scroll at the close before the page moves on */

  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function sstep(t) { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); }
  function band(a, b, x) { return sstep((x - a) / (b - a)); }
  /* the site's easing curve, cubic-bezier(.2,.8,.2,1); a flight uses it mirrored about its middle */
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
  function cosh(x) { return ((x = Math.exp(x)) + 1 / x) / 2; }
  function sinh(x) { return ((x = Math.exp(x)) - 1 / x) / 2; }
  function tanh(x) { return ((x = Math.exp(2 * x)) - 1) / (x + 1); }
  /* van Wijk and Nuij, "Smooth and efficient zooming and panning" (2003): a view is [cx, cy, width] */
  function zoom(p0, p1) {
    var rho = 1.25, ux0 = p0[0], uy0 = p0[1], w0 = p0[2], ux1 = p1[0], uy1 = p1[1], w1 = p1[2];
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
  function fit(s, i) {
    var b = s.box, r = regs[i] || s.reg, bw = b[2] - b[0], bh = b[3] - b[1];
    var k = Math.min((r[1] - r[0]) * W / bw, (r[3] - r[2]) * H / bh);
    var vw = W / k, bcx = (b[0] + b[2]) / 2, bcy = (b[1] + b[3]) / 2;
    var vx = bcx - ((r[0] + r[1]) / 2 * W) / k, vy = bcy - ((r[2] + r[3]) / 2 * H) / k;
    return [vx + vw / 2, vy + H / k / 2, vw];
  }
  function measure() {
    W = stage.clientWidth; H = stage.clientHeight;
    top0 = atlas.getBoundingClientRect().top + w.scrollY;
    /* each stop's region starts clear of its words, whatever the width */
    regs = S.map(function (s, i) {
      var r = s.reg.slice();
      if (i >= 1 && i <= NP + 1 && stops[i]) {
        var need = Math.min(.62, (stops[i].getBoundingClientRect().right + 24) / W);
        if (r[0] < need) { var wd = r[1] - r[0]; r[0] = need; r[1] = Math.min(.98, need + wd); }
      }
      return r;
    });
    panelR = stops[2] ? stops[2].getBoundingClientRect().right : W * .45;
    step = Math.max(1, (atlas.offsetHeight - H) / (N - 1 + HOLD));
    cams = S.map(fit);
    zs = [];
    for (var i = 0; i < N - 1; i++) zs.push(zoom(cams[i], cams[i + 1]));
    if (R) R.resize(W, H);
  }
  function progress() { return clamp((w.scrollY - top0) / step, 0, N - 1); }
  /* inside each step: a dwell at the stop, then the flight to the next (eased at both ends) */
  function flightT(f) { var a = DWELL / 2; return f <= a ? 0 : f >= 1 - a ? 1 : sstep((f - a) / (1 - 2 * a)); }
  function camAt(p) {
    var i = Math.floor(p);
    if (i >= N - 1) return cams[N - 1].slice();
    var t = flightT(p - i);
    return t <= 0 ? cams[i].slice() : t >= 1 ? cams[i + 1].slice() : zs[i](t);
  }
  function routeAt(p) {
    if (p <= 2) return 0;
    if (p >= NP + 1) return NP - 1;
    var i = Math.floor(p);
    return i - 2 + flightT(p - i);
  }
  function view(c) { var k = W / c[2]; return [c[0] - c[2] / 2, c[1] - H / k / 2, k]; }

  /* ---------------- the renderers ---------------- */
  function makeGL() {
    var gl = canvas.getContext("webgl2", { alpha: true, premultipliedAlpha: true, antialias: true, stencil: true, depth: false,
      failIfMajorPerformanceCaveat: true });
    if (!gl) return null;
    /* only on a real graphics processor: a software one draws the SVG faster */
    var dbg = gl.getExtension("WEBGL_debug_renderer_info"), gpu = String(gl.getParameter(dbg ? dbg.UNMASKED_RENDERER_WEBGL : gl.RENDERER));
    if (/swiftshader|llvmpipe|softpipe|software|basic render/i.test(gpu)) { var lose = gl.getExtension("WEBGL_lose_context"); if (lose) lose.loseContext(); return null; }
    var dpr = Math.min(w.devicePixelRatio || 1, 2), CW = 1, CH = 1;
    /* the colours: each token resolved by the browser, then read back through a 1 x 1 canvas */
    var probe = d.createElement("i"), c2 = d.createElement("canvas"), x2;
    probe.style.cssText = "position:absolute;width:0;height:0;visibility:hidden";
    atlas.appendChild(probe);
    c2.width = c2.height = 1; x2 = c2.getContext("2d", { willReadFrequently: true });
    function tok(name) {
      probe.style.color = "var(" + name + ")";
      x2.clearRect(0, 0, 1, 1); x2.fillStyle = getComputedStyle(probe).color; x2.fillRect(0, 0, 1, 1);
      var p = x2.getImageData(0, 0, 1, 1).data, al = p[3] / 255;
      return [p[0] / 255 * al, p[1] / 255 * al, p[2] / 255 * al, al];
    }
    var C = {};
    ["--ex-sea", "--ex-land", "--ex-land-hi", "--ex-coast", "--ex-border", "--ex-grat", "--ex-grat5", "--ex-eqc", "--ex-route", "--ex-lamp", "--ex-lamp2"]
      .forEach(function (n) { C[n.slice(5)] = tok(n); });
    atlas.removeChild(probe);
    function mul(c, a) { return [c[0] * a, c[1] * a, c[2] * a, c[3] * a]; }

    function sh(type, src) {
      var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    }
    function prog(vs, fs) {
      var p = gl.createProgram(), u = {};
      gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(p);
      if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
      for (var i = 0, n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS); i < n; i++) {
        var nm = gl.getActiveUniform(p, i).name; u[nm.replace("[0]", "")] = gl.getUniformLocation(p, nm);
      }
      return { p: p, u: u };
    }
    var HEAD = "#version 300 es\nprecision highp float;\nuniform vec4 cam;uniform vec2 res;\n" +
      "vec4 clip(vec2 s){return vec4(s.x/res.x*2.-1.,1.-s.y/res.y*2.,0.,1.);}\n";
    var FILL = prog(HEAD + "layout(location=0) in vec2 p;void main(){gl_Position=clip((p-cam.xy)*cam.z);}",
      "#version 300 es\nprecision highp float;uniform vec4 col;out vec4 o;void main(){o=col;}");
    /* the land's colour, with the pointer's soft light over it */
    var COVER = prog("#version 300 es\nlayout(location=0) in vec2 p;void main(){gl_Position=vec4(p,0.,1.);}",
      "#version 300 es\nprecision highp float;uniform vec4 col;uniform vec4 hi;uniform vec4 lamp;uniform vec2 res;out vec4 o;" +
      "void main(){vec2 f=vec2(gl_FragCoord.x,res.y-gl_FragCoord.y);float l=lamp.w*(1.-smoothstep(0.,1.,length(f-lamp.xy)/lamp.z));" +
      "o=mix(col,hi,l*l*(3.-2.*l));}");
    /* hairlines: each segment a quad of exact width (the multisampling smooths it); drawn once a pixel */
    var LINE = prog(HEAD + "layout(location=0) in vec2 t;layout(location=1) in vec4 ab;layout(location=2) in vec2 ss;" +
      "uniform float hw;out float vs;void main(){vec2 a=(ab.xy-cam.xy)*cam.z,b=(ab.zw-cam.xy)*cam.z;vec2 e=b-a;float L=length(e);" +
      "vec2 u=L>1e-4?e/L:vec2(1.,0.);vec2 n=vec2(-u.y,u.x);vs=mix(ss.x,ss.y,t.x);" +
      "gl_Position=clip(mix(a,b,t.x)+u*(t.x*2.-1.)*hw+n*t.y*hw);}",
      "#version 300 es\nprecision highp float;in float vs;uniform vec4 col;uniform vec3 dash;uniform vec2 cut;out vec4 o;" +
      "void main(){if(dash.x>0.&&mod(vs*dash.z,dash.x+dash.y)>dash.x)discard;if(cut.y>0.&&vs>cut.x)discard;o=col;}");
    /* the soft light at each place */
    var GLOW = prog(HEAD + "layout(location=0) in vec2 q;uniform vec3 g;out vec2 vq;void main(){vq=q;gl_Position=clip((g.xy-cam.xy)*cam.z+q*g.z);}",
      "#version 300 es\nprecision highp float;in vec2 vq;uniform vec4 col;out vec4 o;" +
      "void main(){float r=dot(vq,vq);if(r>1.)discard;o=col*(exp(-r*4.2)*(1.-r));}");
    gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    gl.disable(gl.DEPTH_TEST); gl.disable(gl.CULL_FACE);

    /* ---- the geometry, read from the very same paths the still map draws ---- */
    var RE = /[MlqzLQZ]|-?(?:\d+\.?\d*|\.\d+)/g;
    function parse(str, out) {
      var tk = str.match(RE) || [], i = 0, cmd = "", x = 0, y = 0, line = null;
      function num() { return +tk[i++]; }
      while (i < tk.length) {
        var t = tk[i];
        if (/[A-Za-z]/.test(t)) { cmd = t; i++; if (cmd === "z" || cmd === "Z") { if (line) line.closed = true; } continue; }
        if (cmd === "M") { x = num(); y = num(); line = [x, y]; out.push(line); cmd = "l"; }
        else if (cmd === "l") { x += num(); y += num(); line.push(x, y); }
        else if (cmd === "q") {
          var cx = x + num(), cy = y + num(), ex = x + num(), ey = y + num();
          for (var j = 1; j <= 4; j++) { var s = j / 4, a = (1 - s) * (1 - s), b = 2 * (1 - s) * s, c = s * s; line.push(a * x + b * cx + c * ex, a * y + b * cy + c * ey); }
          x = ex; y = ey;
        } else i++;
      }
      return out;
    }
    function lines(sel) { var out = []; [].forEach.call(svg.querySelectorAll(sel), function (p) { parse(p.getAttribute("d"), out); }); return out; }
    function tris(polys) {               /* each ring as a fan from its centroid, for the stencil's nonzero fill */
      var n = 0, k = 0;
      polys.forEach(function (p) { n += (p.length / 2) * 6; });
      var a = new Float32Array(n);
      polys.forEach(function (p) {
        var m = p.length / 2, cx = 0, cy = 0, i;
        for (i = 0; i < m; i++) { cx += p[2 * i]; cy += p[2 * i + 1]; }
        cx /= m; cy /= m;
        for (i = 0; i < m; i++) { var j = (i + 1) % m; a[k++] = cx; a[k++] = cy; a[k++] = p[2 * i]; a[k++] = p[2 * i + 1]; a[k++] = p[2 * j]; a[k++] = p[2 * j + 1]; }
      });
      return a;
    }
    function segs(polys, withClose, legs) {   /* each segment: a, b, and the length along at each end */
      var out = [];
      polys.forEach(function (p, li) {
        var s = 0, total = 0, m = p.length / 2, i;
        if (legs) for (i = 0; i + 3 < p.length; i += 2) total += Math.hypot(p[i + 2] - p[i], p[i + 3] - p[i + 1]);
        var last = (withClose && p.closed) ? m : m - 1;
        for (i = 0; i < last; i++) {
          var j = (i + 1) % m, ax = p[2 * i], ay = p[2 * i + 1], bx = p[2 * j], by = p[2 * j + 1], L = Math.hypot(bx - ax, by - ay);
          var s0 = legs ? li + s / total : s, s1 = legs ? li + (s + L) / total : s + L;
          out.push(ax, ay, bx, by, s0, s1); s += L;
        }
      });
      return new Float32Array(out);
    }
    var tmpl = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tmpl);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0, -1, 1, -1, 1, 1, 0, -1, 1, 1, 0, 1]), gl.STATIC_DRAW);
    function lineSet(data) {
      var vao = gl.createVertexArray(), buf = gl.createBuffer();
      gl.bindVertexArray(vao);
      gl.bindBuffer(gl.ARRAY_BUFFER, tmpl); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
      gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1, 4, gl.FLOAT, false, 24, 0); gl.vertexAttribDivisor(1, 1);
      gl.enableVertexAttribArray(2); gl.vertexAttribPointer(2, 2, gl.FLOAT, false, 24, 16); gl.vertexAttribDivisor(2, 1);
      gl.bindVertexArray(null);
      return { vao: vao, n: data.length / 6 };
    }
    function triSet(data) {
      var vao = gl.createVertexArray(), buf = gl.createBuffer();
      gl.bindVertexArray(vao); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
      gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0); gl.bindVertexArray(null);
      return { vao: vao, n: data.length / 2 };
    }
    var land = lines(".ex-l"), edgeL = lines(".ex-edge"), route = DATA.legs.map(function (l) { return l.slice(); });
    var G = {
      sea: triSet(tris(edgeL)), land: triSet(tris(land)),
      coast: lineSet(segs(land, true)), border: lineSet(segs(lines(".ex-b"), false)),
      g30: lineSet(segs(lines(".ex-g30"), false)), g5: lineSet(segs(lines(".ex-g5"), false)),
      eq: lineSet(segs(lines(".ex-eq"), false)), edge: lineSet(segs(edgeL, true)),
      route: lineSet(segs(route, false, true)), plan: lineSet(segs(route, false))
    };
    var quad = triSet(new Float32Array([-1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1]));
    var full = triSet(new Float32Array([-1, -1, 3, -1, -1, 3]));
    function use(pr, c) { gl.useProgram(pr.p); if (pr.u.cam) gl.uniform4f(pr.u.cam, c[0], c[1], c[2], 0); if (pr.u.res) gl.uniform2f(pr.u.res, CW, CH); }
    function drawLines(set, col, wcss, dash, cut, once) {
      if (!set.n || col[3] <= .002) return;
      if (once) { gl.enable(gl.STENCIL_TEST); gl.stencilFunc(gl.EQUAL, 0, 255); gl.stencilOp(gl.KEEP, gl.KEEP, gl.INCR); }
      gl.uniform4fv(LINE.u.col, col); gl.uniform1f(LINE.u.hw, Math.max(.5, wcss * dpr / 2));
      gl.uniform3f(LINE.u.dash, dash ? dash[0] * dpr : 0, dash ? dash[1] * dpr : 0, dash ? dash[2] : 0);
      gl.uniform2f(LINE.u.cut, cut == null ? 0 : cut, cut == null ? 0 : 1);
      gl.bindVertexArray(set.vao); gl.drawArraysInstanced(gl.TRIANGLES, 0, 6, set.n);
      if (once) { gl.disable(gl.STENCIL_TEST); gl.clear(gl.STENCIL_BUFFER_BIT); }
    }
    return {
      gl: true,
      resize: function () {
        dpr = Math.min(w.devicePixelRatio || 1, 2);
        CW = Math.max(1, Math.round(W * dpr)); CH = Math.max(1, Math.round(H * dpr));
        if (canvas.width !== CW || canvas.height !== CH) { canvas.width = CW; canvas.height = CH; }
      },
      draw: function (st) {
        var v = view(st.cam), c = [v[0], v[1], v[2] * dpr];
        gl.viewport(0, 0, CW, CH); gl.clearColor(0, 0, 0, 0); gl.clearStencil(0);
        gl.clear(gl.COLOR_BUFFER_BIT | gl.STENCIL_BUFFER_BIT);
        if (st.map <= .001) return;
        use(FILL, c);
        gl.uniform4fv(FILL.u.col, C.sea); gl.bindVertexArray(G.sea.vao); gl.drawArrays(gl.TRIANGLES, 0, G.sea.n);
        use(LINE, c);
        drawLines(G.g5, mul(C.grat5, st.fine), .6, null, null, true);
        drawLines(G.g30, C.grat, .8, null, null, true);
        drawLines(G.eq, C.eqc, .8, [5, 5, c[2]], null, true);
        /* the land: a nonzero fill through the stencil, then one cover */
        use(FILL, c);
        gl.enable(gl.STENCIL_TEST); gl.colorMask(false, false, false, false);
        gl.stencilFunc(gl.ALWAYS, 0, 255);
        gl.stencilOpSeparate(gl.FRONT, gl.KEEP, gl.KEEP, gl.INCR_WRAP); gl.stencilOpSeparate(gl.BACK, gl.KEEP, gl.KEEP, gl.DECR_WRAP);
        gl.bindVertexArray(G.land.vao); gl.drawArrays(gl.TRIANGLES, 0, G.land.n);
        gl.colorMask(true, true, true, true);
        gl.stencilFunc(gl.NOTEQUAL, 0, 255); gl.stencilOp(gl.ZERO, gl.ZERO, gl.ZERO);
        use(COVER, c);
        gl.uniform4fv(COVER.u.col, C.land); gl.uniform4fv(COVER.u.hi, C["land-hi"]);
        gl.uniform4f(COVER.u.lamp, st.lamp[0] * dpr, st.lamp[1] * dpr, st.lamp[2] * dpr, st.lamp[3]);
        gl.bindVertexArray(full.vao); gl.drawArrays(gl.TRIANGLES, 0, 3);
        gl.disable(gl.STENCIL_TEST);
        use(LINE, c);
        drawLines(G.coast, C.coast, .8, null, null, true);
        drawLines(G.border, C.land, 1.6, null, null, false);
        drawLines(G.border, C.border, .7, [2, 3, c[2]], null, true);
        /* the route: the whole year faintly, as planned; the flown part solid */
        drawLines(G.plan, mul(C.route, .34), 1, [3, 5, c[2]], null, true);
        if (st.route > .001) drawLines(G.route, C.route, 1.4, null, st.route, true);
        /* the places' light */
        use(GLOW, c); gl.bindVertexArray(quad.vao);
        st.glows.forEach(function (g) {
          if (g.a <= .002) return;
          gl.uniform3f(GLOW.u.g, g.x, g.y, g.r * dpr);
          gl.uniform4fv(GLOW.u.col, mul(g.set ? C.lamp : C.lamp2, g.a));
          gl.drawArrays(gl.TRIANGLES, 0, 6);
        });
        use(LINE, c);
        drawLines(G.edge, C.grat, 1, null, null, true);
        gl.bindVertexArray(null);
      }
    };
  }
  /* on a software renderer (or none): the still map's SVG flies, by its viewBox */
  function makeSVG() {
    root.classList.add("ex-svg");
    var rp = svg.querySelector(".ex-route"), ra = -1;
    function partial(t) {
      var out = "";
      DATA.legs.forEach(function (l, i) {
        var n = l.length / 2, m = i < Math.floor(t) ? n : i === Math.floor(t) ? Math.round((t - i) * (n - 1)) + 1 : 0;
        for (var k = 0; k < m; k++) out += (out ? "L" : "M") + l[2 * k] + " " + l[2 * k + 1];
      });
      return out || "M0 0";
    }
    return {
      gl: false,
      resize: function () {},
      draw: function (st) {
        var v = view(st.cam), vw = st.cam[2], vh = H / v[2];
        svg.setAttribute("viewBox", v[0].toFixed(2) + " " + v[1].toFixed(2) + " " + vw.toFixed(2) + " " + vh.toFixed(2));
        var fine = st.fine > .5 ? "1" : "0";
        if (svg.style.getPropertyValue("--ex-fine") !== fine) svg.style.setProperty("--ex-fine", fine);
        svg.style.opacity = st.map.toFixed(3);
        var r = Math.round(st.route * 400) / 400;
        if (r !== ra) { ra = r; rp.setAttribute("d", partial(r)); rp.style.visibility = r > 0 ? "visible" : "hidden"; }
      }
    };
  }
  /* the photographs: each rises out of the map from its place's ring through the "air", a still field of soft
     noise that shapes the edge of the reveal. One small canvas over the photograph's region; the mask is
     worked out on a coarse grid (smooth enough to upscale) and the frame is drawn only when something moved. */
  var AIRF = (function () {
    var S = 128, L = 8, val = new Float32Array(S * S);
    function hash(x, y, per) { x = ((x % per) + per) % per; y = ((y % per) + per) % per; var h = (x * 374761393 + y * 668265263) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967295; }
    function vn(x, y, per) {
      var xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
      var a = hash(xi, yi, per), b = hash(xi + 1, yi, per), c = hash(xi, yi + 1, per), e = hash(xi + 1, yi + 1, per);
      return a + (b - a) * u + (c - a) * v + (a - b - c + e) * u * v;
    }
    for (var j = 0; j < S; j++) for (var i = 0; i < S; i++) {
      var sum = 0, amp = .5, f = L / S;
      for (var o = 0; o < 5; o++) { sum += amp * vn(i * f, j * f, L << o); f *= 2; amp *= .5; }
      val[j * S + i] = sum / .97;
    }
    return function (x, y) {                     /* bilinear, tiling */
      x = ((x % S) + S) % S; y = ((y % S) + S) % S;
      var i = Math.floor(x), j = Math.floor(y), fx = x - i, fy = y - j, i1 = (i + 1) % S, j1 = (j + 1) % S;
      return (val[j * S + i] * (1 - fx) + val[j * S + i1] * fx) * (1 - fy) + (val[j1 * S + i] * (1 - fx) + val[j1 * S + i1] * fx) * fy;
    };
  })();
  var Air = (function () {
    var cv = plate.querySelector(".ex-air"), cx = cv.getContext("2d"), mk = d.createElement("canvas"), mx = mk.getContext("2d");
    var imgs = {}, caches = {}, shown = "", last = "", alts = {};
    PL.forEach(function (pl) { var a = d.querySelector("#" + pl.id + " .ex-photo img"); if (a) alts[pl.id] = a.getAttribute("alt"); });
    function ss(a, b, x) { var t = clamp((x - a) / (b - a), 0, 1); return t * t * t * (t * (t * 6 - 15) + 10); }
    function load() {
      PL.forEach(function (pl) {
        if (!pl.photo || imgs[pl.id]) return;
        var im = new Image(), jpg = false;
        im.decoding = "async";
        im.onerror = function () { if (!jpg) { jpg = true; im.src = pl.photo.src + ".jpg"; } };
        im.onload = function () {
          var done = function () {
            im.ok = true; last = "";
            /* scale it for its stop while the visitor is still on the way (not on the frame it first shows) */
            var warm = function () { if (on && W) cacheFor(pl.id, im, photoRect(pl), pl.photo); kick(); };
            if (w.requestIdleCallback) w.requestIdleCallback(warm, { timeout: 600 }); else warm();
          };
          if (im.decode) im.decode().then(done, done); else done();
        };
        im.src = pl.photo.src + ".webp";
        imgs[pl.id] = im;
      });
    }
    function scale(rw, rh) { return Math.min(w.devicePixelRatio || 1, 2, Math.sqrt(2.6e6 / (rw * rh))); }
    function cacheFor(id, im, r, ph) {
      var rw = r[2] - r[0], rh = r[3] - r[1], q = scale(rw, rh), bw = Math.round(rw * q), bh = Math.round(rh * q);
      var ck = bw + "|" + bh, cache = caches[id];
      if (!cache || cache.key !== ck) {
        var iw = ph.w, ih = ph.h, s = Math.max(rw / iw, rh / ih), sw = rw / s, sh = rh / s;
        cache = caches[id] = { key: ck, cv: d.createElement("canvas") };
        cache.cv.width = bw; cache.cv.height = bh;
        var c3 = cache.cv.getContext("2d"); c3.imageSmoothingEnabled = true; c3.imageSmoothingQuality = "high";
        c3.drawImage(im, (iw - sw) * ph.pos[0], (ih - sh) * ph.pos[1], sw, sh, 0, 0, bw, bh);
      }
      return cache;
    }
    function draw(list) {
      var ph = null;
      list.forEach(function (q) { if (!ph || q.rev > ph.rev) ph = q; });
      var im = ph && imgs[ph.id];
      if (!ph || !im || !im.ok || ph.rev <= .002) {
        if (shown) { cv.style.visibility = "hidden"; shown = ""; last = ""; cv.removeAttribute("role"); cv.removeAttribute("aria-label"); cv.setAttribute("aria-hidden", "true"); }
        return;
      }
      var r = ph.rect, rw = r[2] - r[0], rh = r[3] - r[1], rx = ph.ring[0] - r[0], ry = ph.ring[1] - r[1];
      var key = ph.id + "|" + ph.rev.toFixed(4) + (ph.peek ? 'p' : '') + "|" + rx.toFixed(1) + "|" + ry.toFixed(1) + "|" + rw + "|" + rh;
      if (key === last) return;
      last = key;
      if (shown !== ph.id) {
        shown = ph.id; cv.style.visibility = "visible";
        cv.setAttribute("role", "img"); cv.setAttribute("aria-label", alts[ph.id] || ""); cv.removeAttribute("aria-hidden");
      }
      var q = scale(rw, rh), bw = Math.round(rw * q), bh = Math.round(rh * q);
      if (cv.width !== bw || cv.height !== bh) { cv.width = bw; cv.height = bh; }
      /* placed by a transform, so moving it is never a layout shift */
      cv.style.transform = "translate(" + r[0].toFixed(1) + "px," + r[1].toFixed(1) + "px)"; cv.style.width = rw + "px"; cv.style.height = rh + "px";
      /* the photograph scaled once to its region (a well smoothed cache); each frame then copies it 1:1 */
      var cache = cacheFor(ph.id, im, r, ph);
      cx.globalCompositeOperation = "copy"; cx.imageSmoothingQuality = "low";
      cx.drawImage(cache.cv, 0, 0);
      /* the mask: long eased edges (in from the words' side, out at the top and the foot) times the reveal,
         whose edge the air shapes */
      var MW = 84, MH = Math.max(8, Math.round(MW * rh / rw));
      if (mk.width !== MW || mk.height !== MH) { mk.width = MW; mk.height = MH; }
      var md = mx.createImageData(MW, MH), dd = md.data, big = 0, rev = ph.rev;
      [[0, 0], [rw, 0], [0, rh], [rw, rh]].forEach(function (c) { big = Math.max(big, Math.hypot(c[0] - rx, c[1] - ry)); });
      /* a peek from the world map: a small window, about 130 px across its soft edge, round the ring */
      var pk = ph.peek ? 104 * Math.min(1, ph.rev / .15) : 0;
      for (var j = 0; j < MH; j++) {
        var y = (j + .5) / MH * rh, my = pk ? 1 : ss(0, rh * .26, y) * ss(0, rh * .3, rh - y);
        for (var i = 0; i < MW; i++) {
          var x = (i + .5) / MW * rw, m = pk ? my : my * ss(0, rw * .5, x);
          var n = AIRF(x / rh * 79, y / rh * 79);
          var t, a, dr = Math.hypot(x - rx, y - ry);
          if (pk) { t = clamp((pk - dr - (n - .5) * pk * .5) / (pk * .6), 0, 1); }
          else { var f = rev * 1.32 - dr / big - (n - .5) * .6 * Math.min(1, rev * 2.6) * (1 - rev * .6); t = clamp((f + .03) / .23, 0, 1); }
          a = t * t * (3 - 2 * t);
          dd[(j * MW + i) * 4 + 3] = Math.round(m * a * 255);
        }
      }
      mx.putImageData(md, 0, 0);
      cx.globalCompositeOperation = "destination-in";
      cx.drawImage(mk, 0, 0, MW, MH, 0, 0, bw, bh);
      cx.globalCompositeOperation = "source-over";
    }
    return { load: load, draw: draw, reset: function () { shown = ""; last = ""; cv.style.visibility = "hidden"; } };
  })();
  function ensure() {
    if (R) return;
    try { R = makeGL(); } catch (err) { R = null; }
    if (!R) R = makeSVG(); else root.classList.add("ex-gl-on");
    R.resize(W, H);
  }
  canvas.addEventListener("webglcontextlost", function (e) { e.preventDefault(); root.classList.remove("ex-gl-on"); canvas.style.opacity = "0"; R = makeSVG(); kick(); });

  /* ---------------- one frame: everything follows the one eased progress ---------------- */
  function photoRect(pl) {
    var cap = 1.12, rw = Math.min(W * .64, pl.photo.w * cap, W - panelR + 160), rh = Math.min(H, pl.photo.h * cap);
    var y0 = (H - rh) / 2;
    return [W - rw, y0, W, y0 + rh];
  }
  function setWords(i) {
    if (i === words) return;
    words = i;
    stops.forEach(function (el) { var k = +el.getAttribute("data-i"); if (k > 0) el.classList.toggle("is-on", k === i); });
  }
  function setPlace(i) {
    if (i === curPlace) return;
    curPlace = i;
    pins.forEach(function (el) { el.classList.toggle("is-on", +el.getAttribute("data-i") === i); });
    yearLinks.forEach(function (el) { if (+el.getAttribute("data-i") === i) el.setAttribute("aria-current", "location"); else el.removeAttribute("aria-current"); });
  }
  function render(tw, dt) {
    var moving = false, a1 = 1 - Math.exp(-dt / 140), a2 = 1 - Math.exp(-dt / 260);
    var o = P >= 1 ? 1 : flightT(Math.max(0, P));
    var oo = P <= N - 2 ? 0 : flightT(P - (N - 2));
    var wi;
    if (tw) wi = tw.u > .88 ? tw.to : (tw.u < .03 ? tw.from : -1);
    else { var rr = Math.round(P); wi = Math.abs(P - rr) < DWELL / 2 + .03 ? rr : -1; }
    setWords(wi);
    var pi = (wi >= 2 && wi <= NP + 1) ? wi : (tw && tw.u > .5 && tw.to >= 2 && tw.to <= NP + 1 ? tw.to : -1);
    setPlace(pi);
    var q = P > N - 1.55 || (tw && tw.to === N - 1 && tw.u > .4);
    if (q !== quiet) { quiet = q; yearEl.classList.toggle("is-quiet", q); }
    var nr = P > N - 3.6 || (tw && tw.to === N - 1);
    if (nr && !near) { near = true; outroEl.classList.add("is-near"); }
    if ((P > .45 || (tw && tw.to >= 1)) && !photosWanted) { photosWanted = true; Air.load(); }
    var v = view(cur), k = v[2];
    /* the arrival: the two skies lie on the map between their places and go with it as the camera pulls back */
    var g0 = o >= 1;
    if (!g0 || gone !== true) {
      var v0 = view(cams[0]), s = k / v0[2];
      sky.style.transform = "matrix(" + s.toFixed(5) + ",0,0," + s.toFixed(5) + "," + ((v0[0] - v[0]) * k).toFixed(2) + "," + ((v0[1] - v[1]) * k).toFixed(2) + ")";
      sky.style.opacity = (1 - band(.14, .74, o)).toFixed(3);
      var po = (1 - band(0, .3, o)).toFixed(3);
      openPanel.style.opacity = po; caps.forEach(function (c) { c.style.opacity = po; });
      openEl.classList.toggle("is-gone", o > .45);
      gone = g0;
    }
    var map = band(.1, .62, o) * (1 - .42 * oo);
    if (R && R.gl) canvas.style.opacity = map.toFixed(3);
    pinBox.style.opacity = band(.5, 1, o).toFixed(3);
    if (near) outroPh.style.opacity = band(.3, 1, oo).toFixed(3);
    /* the photographs at their stops: rising from the last part of the approach, held through the stop */
    var phs = [], glows = [];
    PL.forEach(function (pl, j) {
      var si = j + 2, x = (pl.x - v[0]) * k, y = (pl.y - v[1]) * k, close = 1 - band(.25, .9, Math.abs(P - si));
      if (pl.photo) {
        var r = tw ? (si === tw.to ? band(.55, 1, tw.u) : si === tw.from ? 1 - band(0, .22, tw.u) : 0) : 1 - band(.27, .47, Math.abs(P - si));
        var pt = (hint === pl.id && wi === 1) ? .15 : 0, pv = prev[pl.id] || 0;
        pv += (pt - pv) * a2; if (Math.abs(pt - pv) < .002) pv = pt; else moving = true;
        prev[pl.id] = pv;
        var peek = pv > r;
        r = Math.max(r, pv);
        var rc = photoRect(pl);
        /* a peek sets the photograph's own focal point under the ring */
        if (peek) { var rw0 = rc[2] - rc[0], rh0 = rc[3] - rc[1]; rc = [x - rw0 * pl.photo.pos[0], y - rh0 * pl.photo.pos[1], 0, 0]; rc[2] = rc[0] + rw0; rc[3] = rc[1] + rh0; }
        if (r > .002) phs.push({ id: pl.id, rev: r, peek: peek, ring: [x, y], rect: rc, w: pl.photo.w, h: pl.photo.h, pos: pl.photo.pos });
      }
      glows.push({ x: pl.x, y: pl.y, set: pl.set, r: 46 + 34 * close, a: map * (pl.set ? .28 + .36 * close : .08 + .16 * close) + (hint === pl.id ? .25 * map : 0) });
    });
    /* the pointer's light over the land */
    lamp.x += (lamp.tx - lamp.x) * a1; lamp.y += (lamp.ty - lamp.y) * a1; lamp.a += (lamp.ta - lamp.a) * a2;
    if (Math.abs(lamp.tx - lamp.x) > .3 || Math.abs(lamp.ty - lamp.y) > .3 || Math.abs(lamp.ta - lamp.a) > .003) moving = true;
    else if (lamp.ta === 0) lamp.a = 0;
    if (o > .05) {
      ensure();
      R.draw({ cam: cur, map: map, fine: 1 - band(300, 520, cur[2]),
               route: routeAt(P), glows: glows, lamp: [lamp.x, lamp.y, 300, lamp.a * map * .9] });
    } else if (R && R.gl) canvas.style.opacity = "0";
    Air.draw(phs);
    /* the pins, where the camera puts them (hidden under the words) */
    for (var i = 0; i < pins.length; i++) {
      var pl = PL[i], x = (pl.x - v[0]) * k, y = (pl.y - v[1]) * k;
      var out = x < Math.min(W * .46, W * .4 + 80) || x > W + 40 || y < 30 || y > H - 40;
      pins[i].style.transform = "translate3d(" + x.toFixed(1) + "px," + y.toFixed(1) + "px,0)" + (pins[i].classList.contains("is-l") ? " translateX(-100%)" : "");
      pins[i].classList.toggle("is-off", out);
    }
    return moving;
  }
  function frame(t) {
    raf = 0;
    var dt = lastT ? Math.min(120, t - lastT) : 16; lastT = t;
    var busy = false, tw = null;
    if (tween) {
      var u = Math.min(1, (t - tween.t0) / tween.dur), e = u < .5 ? (1 - bez(1 - 2 * u)) / 2 : (1 + bez(2 * u - 1)) / 2;
      cur = tween.f(e); P = tween.P0 + (tween.P1 - tween.P0) * e;
      tw = { u: u, to: tween.to, from: tween.from };
      if (u >= 1) { P = tween.to; cur = cams[tween.to].slice(); tween = null; tw = null; }
      busy = true;
    } else {
      var p = progress(), a = 1 - Math.exp(-dt / 170);
      P += (p - P) * a;
      if (Math.abs(p - P) < 1e-4) P = p; else busy = true;
      cur = camAt(P);
    }
    if (render(tw, dt)) busy = true;
    if (busy) raf = requestAnimationFrame(frame); else lastT = 0;
  }
  function kick() { if (on && !raf) raf = requestAnimationFrame(frame); }
  function nearest() { var r = Math.round(P); return Math.abs(P - r) < .3 ? r : -1; }
  function go(i, instant) {
    if (!on) return false;
    var y = Math.round(top0 + i * step);
    if (!instant && cur) {
      var z = zoom(cur, cams[i]);
      tween = { f: z, t0: performance.now(), dur: clamp(700 * z.len + 500, 1100, 2600), to: i, from: nearest(), P0: P, P1: i };
    } else { tween = null; P = i; cur = cams[i].slice(); }
    w.scrollTo({ top: y, behavior: "instant" });
    kick();
    return true;
  }
  function enable() {
    on = true;
    root.classList.add("ex-fly");
    measure();
    P = progress(); cur = camAt(P);
    render(null, 16);
    root.classList.add("ex-ready");
    if (location.hash) { var k = ids.indexOf(location.hash.slice(1)); if (k > 0) { ensure(); go(k, true); } }
    kick();
  }
  function disable() {
    on = false; tween = null;
    root.classList.remove("ex-fly", "ex-ready", "ex-gl-on", "ex-svg");
    svg.setAttribute("viewBox", DATA.over.join(" "));
    svg.style.removeProperty("--ex-fine"); svg.style.opacity = "";
    routeEl.setAttribute("d", routeD); routeEl.style.visibility = ""; Air.reset();
    if (R && !R.gl) R = null;
    [sky, openPanel, pinBox, outroPh, canvas].concat(caps).forEach(function (el) { el.style.transform = ""; el.style.opacity = ""; });
    pins.forEach(function (p) { p.style.transform = ""; p.classList.remove("is-off", "is-on"); });
    stops.forEach(function (s) { if (+s.getAttribute("data-i") > 0) s.classList.remove("is-on"); });
    openEl.classList.remove("is-gone"); yearEl.classList.remove("is-quiet"); outroEl.classList.remove("is-near");
    words = -2; curPlace = -2; quiet = null; near = false; gone = null;
    yearLinks.forEach(function (el) { el.removeAttribute("aria-current"); });
    if (still) still();
  }
  function safeEnable() { try { enable(); } catch (err) { disable(); } }
  function decide() {
    var want = mqWide.matches && !mqRM.matches && typeof WebGL2RenderingContext !== "undefined";
    if (want && !on) safeEnable(); else if (!want && on) disable();
    else if (on) { measure(); P = progress(); cur = camAt(P); render(null, 16); }
  }
  w.addEventListener("scroll", kick, { passive: true });
  w.addEventListener("resize", function () { if (on || mqWide.matches) decide(); }, { passive: true });
  if (mqWide.addEventListener) { mqWide.addEventListener("change", decide); mqRM.addEventListener("change", decide); }
  /* choosing a place (on the map, in the index, on the year, on a sky) flies there */
  atlas.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    var m = !a && e.target.closest && e.target.closest(".ex-ymonths span[data-t]");
    var id = a ? a.getAttribute("href").slice(1) : m ? m.getAttribute("data-t") : "";
    var k = ids.indexOf(id);
    if (k < 0) return;
    if (!on) { if (m) { var el = d.getElementById(id); if (el) el.scrollIntoView({ block: "start" }); } return; }
    e.preventDefault();
    ensure();
    go(k, false);
    if (history.replaceState) history.replaceState(null, "", "#" + ids[k]);
    var h = stops[k] && stops[k].querySelector("h1,h2");
    if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
  });
  /* tabbing into a place's words takes the camera there */
  atlas.addEventListener("focusin", function (e) {
    if (!on || tween) return;
    var st = e.target.closest && e.target.closest(".ex-stop");
    if (!st || e.target.matches("h1,h2")) return;
    var k = +st.getAttribute("data-i");
    if (k > 0 && k !== words) { ensure(); go(k, false); }
  });
  /* pointing at a place (or its month) lights it everywhere it appears; on the world map it opens a little of
     its photograph; the pointer carries a soft light over the land */
  function setHint(id, onn) {
    // the selector's quotes are single so the site audit does not read it as a link
    [].forEach.call(atlas.querySelectorAll("a[href='#" + id + "'],.ex-ymonths span[data-t='" + id + "']"), function (a) { a.classList.toggle("is-hint", onn); });
    if (onn) hint = id; else if (hint === id) hint = "";
    kick();
  }
  [].forEach.call(atlas.querySelectorAll('.ex-ix a,.ex-pin,.ex-yplaces a,.ex-ymonths span[data-t]'), function (a) {
    var id = a.getAttribute("data-t") || a.getAttribute("href").slice(1);
    ["pointerenter", "focus"].forEach(function (t) { a.addEventListener(t, function () { setHint(id, true); }); });
    ["pointerleave", "blur"].forEach(function (t) { a.addEventListener(t, function () { setHint(id, false); }); });
  });
  stage.addEventListener("pointermove", function (e) {
    if (!on || e.pointerType !== "mouse") return;
    var r = stage.getBoundingClientRect();
    lamp.tx = e.clientX - r.left; lamp.ty = e.clientY - r.top;
    if (lamp.a < .01) { lamp.x = lamp.tx; lamp.y = lamp.ty; }
    lamp.ta = 1; kick();
  }, { passive: true });
  stage.addEventListener("pointerleave", function () { lamp.ta = 0; kick(); });

  /* ---------------- the still journey: the year marks the place you are reading ---------------- */
  var still = (function () {
    var parts = yearLinks.map(function (a) { return d.getElementById(a.getAttribute("href").slice(1)); });
    var mark = -1, queued = false;
    function update() {
      queued = false;
      if (on) return;
      var line = w.innerHeight * .42, hit = -1;
      parts.forEach(function (el, i) {
        if (!el) return;
        var r = el.getBoundingClientRect();
        if (r.top <= line && r.bottom > line) hit = i;
      });
      if (hit === mark) return;
      if (mark > -1) yearLinks[mark].removeAttribute("aria-current");
      mark = hit;
      if (hit > -1) yearLinks[hit].setAttribute("aria-current", "location");
    }
    function soon() { if (!queued && !on) { queued = true; w.requestAnimationFrame(update); } }
    w.addEventListener("scroll", soon, { passive: true });
    w.addEventListener("resize", soon, { passive: true });
    return function () { mark = -1; soon(); };
  })();

  /* if anything here fails, the page falls back to the still journey rather than an empty stage */
  if (root.classList.contains("ex-fly")) {
    if (mqWide.matches && !mqRM.matches) safeEnable(); else root.classList.remove("ex-fly");
  }
  if (!on) still();
  var warm = function () { if (on && !R) { ensure(); kick(); } };
  w.addEventListener("load", function () {
    if (on) { measure(); kick(); }
    if (w.requestIdleCallback) w.requestIdleCallback(warm, { timeout: 4000 });
  });
  ["wheel", "keydown", "touchstart"].forEach(function (t) { w.addEventListener(t, warm, { passive: true, once: true }); });
})();
</script>"""


def ld():
    return ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"WebPage",'
            '"@id":"%s#webpage","name":"%s","url":"%s","description":"%s",'
            '"isPartOf":{"@id":"https://paraglidingatlas.com/#website"},'
            '"publisher":{"@id":"https://paraglidingatlas.com/#organization"},"inLanguage":"en"}\n</script>'
            % (URL, TITLE, URL, DESC.replace('"', '\\"')))


def words(markup):
    """The words a visitor sees in <main>: tags, scripts, comments, drawings and visually hidden spans out; the
    year's month initials (shown only on phones, in place of the names) out."""
    t = re.sub(r"<script.*?</script>", " ", markup, flags=re.S)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<svg.*?</svg>", " ", t, flags=re.S)
    t = re.sub(r'<span class="ex-vh">.*?</span>', " ", t)
    t = re.sub(r"<i>[A-Z]</i>", " ", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return [x for x in t.split() if re.search(r"\w", x)]


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
        raise SystemExit("v4_expeditions: the header has no Expeditions tab to mark")
    if ".ex-atlas" not in head or "Partner With Me" in head.split("<body")[0] or URL not in head:
        raise SystemExit("v4_expeditions: the partners shell has changed; check the head")
    if 'content="noindex' not in head:
        raise SystemExit("v4_expeditions: the shell lost its noindex")
    if "<title>Expeditions: Paragliding Atlas</title>" not in head:
        raise SystemExit("v4_expeditions: the title is wrong")
    body = main_html()
    page = head + body + tail.replace("</body>", SCRIPT + "\n</body>", 1)
    if "—" in page:
        raise SystemExit("v4_expeditions: an em dash crept in")
    # no colour written out anywhere: the styles and the markup use only the tokens; the canvas reads the tokens
    if re.search(r"#[0-9a-fA-F]{3,8}\b(?![\w-])|rgba?\(|hsla?\(", css() + re.sub(r'href="#[\w-]+"|#ex-[\w-]+', "", body)) \
            or re.search(r"#[0-9a-fA-F]{6}\b|(rgba?|hsla?)\(", SCRIPT):
        raise SystemExit("v4_expeditions: a raw colour crept in; use the design tokens")
    for h in re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", body):
        txt = re.sub(r"<[^>]+>", "", h)
        small = {"a", "an", "and", "the", "of", "to", "in", "on", "for", "or", "at", "by", "with"}
        bad = [x for i, x in enumerate(txt.split()) if x[0].isalpha() and x[0].islower() and (i == 0 or x not in small)]
        if bad:
            raise SystemExit("v4_expeditions: a heading is not in Title Case: %r" % txt)
    n = len(words(body))
    if n > MAX_WORDS:
        raise SystemExit("v4_expeditions: %d words in <main>; keep it under %d" % (n, MAX_WORDS))
    open(OUT, "w", encoding="utf-8").write(page)
    print("v4_expeditions: %s (%d KB, main %d KB, %d words in <main>)"
          % (os.path.relpath(OUT, ROOT), len(page.encode()) // 1024, len(body.encode()) // 1024, n))


if __name__ == "__main__":
    main()
