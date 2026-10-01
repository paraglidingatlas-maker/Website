#!/usr/bin/env python3
"""
Series tiles, Gold line, three drawing options per series (owner, 1 Oct 2026:
"we go with gold line, but can i get some options for the symbols/drawings
for icons, i want them to be of higher quality").

Finer than the first Gold line tiles: engraving hatching for shade and volume,
a weight for every line (hairline, detail, outline, accent), a soft gold light
behind the subject, and still one gold element per tile for what the series
is about. Each series gets a row: today's Gold line tile, then options A, B, C.

    python3 tools/v4_series_options.py   # writes prototypes/v4/samples/series-options.html
                                         # and puts PICK on the v4 library (v2-library.js)

The owner picked B for every series (1 Oct 2026: "b"). install() writes those
drawings into prototypes/v4/v2-library.js between the series-art markers; the
tile loop there uses them in place of the stone slabs.
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_samples as SM  # noqa: E402
import v4_series_icons2 as A  # noqa: E402
import v4_series_full as FULL  # noqa: E402
from v4_computed import naca  # noqa: E402

f, path, smooth = A.f, A.path, A.smooth
W, H = A.W, A.H
PI = math.pi


def bbox(d):
    """The box a clip path sits in (whole tile when the path has arcs, whose flags are not coordinates)."""
    if re.search(r"[AaQqCcHhVv]", re.sub(r"[eE]", "", d)) and re.search(r"[Aa]", d):
        return (0, 0, W, H)
    n = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", d)]
    xs, ys = n[0::2], n[1::2]
    return (max(0, min(xs) - 2), max(0, min(ys) - 2), min(W, max(xs) + 2), min(H, max(ys) + 2))


def cut(a, b, box):
    """Liang-Barsky: the part of segment a-b inside the box, or None."""
    x0, y0, x1, y1 = box
    dx, dy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if p == 0:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy)


# ---------------------------------------------------------------- the pen
class G:
    """One tile: back (fills, hatching), mid (lines), top (the gold), flow."""

    def __init__(self, k):
        self.k, self.defs, self.back, self.mid, self.top, self.fl, self.n = k, [], [], [], [], [], 0
        self.ln_ = "url(#%s-ln)" % k
        self.ac_ = "url(#%s-ac)" % k

    def ln(self, d, w=1.1, op=1, dash=None):
        self.mid.append(A.S(d, self.ln_, w, op, ' stroke-dasharray="%s"' % dash if dash else ""))

    def hair(self, d, op=.3, dash=None):
        self.mid.append(A.S(d, "#f6f4f4", .55, op, ' stroke-dasharray="%s"' % dash if dash else ""))

    def ac(self, d, w=1.7, op=1, dash=None):
        self.top.append(A.S(d, self.ac_, w, op, ' stroke-dasharray="%s"' % dash if dash else ""))

    def fill(self, d, op=.05, c="#ffb35c"):
        self.back.append(A.F(d, c, op))

    def ink(self, d):
        """Knock the background colour back in behind a shape (for overlaps)."""
        self.mid.append(A.F(d, "#121318", 1))

    def dot(self, x, y, r=2.2, acc=True):
        self.top.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x), f(y), f(r), self.ac_ if acc else "#f6f4f4"))

    def ring(self, x, y, r, acc=True, w=1.2):
        d = "M%s,%s a%s,%s 0 1,0 %s,0 a%s,%s 0 1,0 %s,0" % (f(x - r), f(y), f(r), f(r), f(2 * r), f(r), f(r), f(-2 * r))
        (self.ac if acc else self.ln)(d, w)

    def flow(self, d, op=.6):
        self.fl.append(A.FL(d, op=op))

    def hatch(self, clip, ang=45, gap=3.0, op=.22, w=.5, top=False):
        self.n += 1
        cid = "%s-h%d" % (self.k, self.n)
        self.defs.append('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, clip))
        a = math.radians(ang)
        dx, dy, nx, ny = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        box = bbox(clip)
        d = ""
        o = -130.0
        while o <= 130:
            cx, cy = 100 + nx * o, 69 + ny * o
            seg = cut((cx - dx * 140, cy - dy * 140), (cx + dx * 140, cy + dy * 140), box)
            if seg:
                d += "M%s,%s L%s,%s " % (f(seg[0][0]), f(seg[0][1]), f(seg[1][0]), f(seg[1][1]))
            o += gap
        if not d:
            return
        el = ('<g clip-path="url(#%s)"><path d="%s" fill="none" stroke="#f6f4f4" stroke-opacity="%s" stroke-width="%s" '
              'vector-effect="non-scaling-stroke"/></g>' % (cid, d.strip(), round(min(.6, op * 1.4), 3), w))
        (self.mid if top else self.back).append(el)

    def light(self, x, y, r, op=.13):
        self.n += 1
        gid = "%s-l%d" % (self.k, self.n)
        self.defs.append('<radialGradient id="%s" gradientUnits="userSpaceOnUse" cx="%s" cy="%s" r="%s">'
                         '<stop offset="0" stop-color="#ffb35c" stop-opacity="%s"/><stop offset="1" stop-color="#ffb35c" stop-opacity="0"/>'
                         '</radialGradient>' % (gid, f(x), f(y), f(r), op))
        self.back.insert(0, '<rect width="%d" height="%d" fill="url(#%s)"/>' % (W, H, gid))

    def head(self, tip, vec, s=6, acc=True):
        L = math.hypot(*vec) or 1
        ux, uy = vec[0] / L, vec[1] / L
        b = (tip[0] - ux * s, tip[1] - uy * s)
        p = [tip, (b[0] - uy * s * .45, b[1] + ux * s * .45), (b[0] + uy * s * .45, b[1] - ux * s * .45)]
        self.top.append('<path d="%s" fill="%s"/>' % (path(p, True), self.ac_ if acc else "#f6f4f4"))

    def arrow(self, a, b, acc=True, w=1.5, s=6):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        e = (b[0] - ux * s * .8, b[1] - uy * s * .8)
        (self.ac if acc else self.ln)(path([a, e]), w)
        self.head(b, (ux, uy), s, acc)

    def svg(self, title):
        defs = ('<linearGradient id="%s-ln" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="200" y2="0"><stop offset="0" stop-color="#f6f4f4"/>'
                '<stop offset="1" stop-color="#ffcf94"/></linearGradient>'
                '<linearGradient id="%s-ac" gradientUnits="userSpaceOnUse" x1="0" y1="138" x2="200" y2="0"><stop offset="0" stop-color="#ff7517"/>'
                '<stop offset="1" stop-color="#ffd27a"/></linearGradient>' % (self.k, self.k)) + "".join(self.defs)
        body = '<rect width="%d" height="%d" fill="#121318"/>' % (W, H)
        body += "".join(self.back) + "".join(self.mid) + "".join(self.top) + "".join(self.fl)
        return A.svg(self.k, title, defs, body)


def ell(cx, cy, rx, ry, a0=0, a1=2 * PI, n=60, rot=0):
    out = []
    for i in range(n + 1):
        t = a0 + (a1 - a0) * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
    return out


def blob(cx, cy, R, ph, n=72, k=(.12, .07)):
    return [(cx + R * (1 + k[0] * math.sin(3 * t + ph) + k[1] * math.sin(5 * t + 2 * ph)) * math.cos(t),
             cy + R * .62 * (1 + k[0] * math.sin(3 * t + ph) + k[1] * math.sin(5 * t + 2 * ph)) * math.sin(t))
            for t in [2 * PI * i / n for i in range(n)]]


def wing(g, cx, cy, s, acc=False, lines=True):
    """A paraglider seen from in front: the arched canopy, its lines, the pilot."""
    top = ell(cx, cy, s, s * .42, PI, 2 * PI, 30)
    bot = ell(cx, cy + s * .1, s * .93, s * .3, 2 * PI, PI, 30)
    shape = path(top + bot, True)
    g.ink(shape)
    g.fill(shape, .12)
    (g.ac if acc else g.ln)(shape, 1.1)
    p = (cx, cy + s * .95)
    if lines:
        for q in (bot[0], bot[8], bot[15], bot[22], bot[30]):
            g.hair(path([q, p]), .45)
    g.dot(p[0], p[1], max(1.2, s * .08), acc)


# ---------------------------------------------------------------- Risk vs Reward
def risk_a(g):
    r = A.risk()
    gr = r["ground"]
    land = smooth(gr) + " L200,138 L0,138 Z"
    g.light(70, 40, 90)
    g.hatch(land, 62, 2.6, .2)
    g.ln(smooth(gr), .9, .8)
    for dy in (10, 20):
        g.hair(smooth([(x, y + dy) for x, y in gr]), .16)
    g.hair(smooth(r["climb"]), .55)
    g.ln(smooth(r["safe"]), 1.1, .9)
    for (a, b), y in r["fields"]:
        g.ln(path([(a, y - 1), (b, y - 1)]), 2.2, .85)
    g.ac(smooth(r["fast"]), 1.9)
    g.flow(smooth(r["fast"]))
    x, y = r["decision"]
    g.ring(x, y, 4.6)
    g.dot(x, y, 1.8)


def risk_b(g):
    c, R = (100, 112), 74
    g.light(100, 100, 90)
    g.ln(path(ell(c[0], c[1], R, R, PI, 2 * PI, 80)), 1.1, .9)
    g.hair(path(ell(c[0], c[1], R - 14, R - 14, PI, 2 * PI, 80)), .3)
    zone = ell(c[0], c[1], R - 4, R - 4, PI * 1.72, 2 * PI, 30)
    band = path(ell(c[0], c[1], R - 1, R - 1, PI * 1.72, 2 * PI, 30) + ell(c[0], c[1], R - 12, R - 12, 2 * PI, PI * 1.72, 30), True)
    g.hatch(band, -50, 1.8, .45)
    g.ac(path(zone), 2.4)
    for i in range(41):
        t = PI + PI * i / 40
        l = 10 if i % 5 == 0 else 5
        g.hair(path([(c[0] + R * math.cos(t), c[1] + R * math.sin(t)), (c[0] + (R - l) * math.cos(t), c[1] + (R - l) * math.sin(t))]),
               .7 if i % 5 == 0 else .4)
    t0 = PI * 1.42
    g.hair(path([c, (c[0] + (R - 20) * math.cos(t0), c[1] + (R - 20) * math.sin(t0))]), .3, "2 3")
    t = PI * 1.76
    tip = (c[0] + (R - 8) * math.cos(t), c[1] + (R - 8) * math.sin(t))
    g.ln(path([(c[0] - 8 * math.cos(t), c[1] - 8 * math.sin(t)), tip]), 1.6)
    g.ac(path(ell(c[0], c[1], 30, 30, t0, t, 20)), 1, .7)
    g.ring(c[0], c[1], 5, False, 1.2)
    g.dot(c[0], c[1], 2)


def risk_c(g):
    def cliff(x0, x1, top, face):
        pts = [(x0, top)]
        for i in range(13):
            y = top + i * (128 - top) / 12
            pts.append((face + (2.6 * math.sin(i * .9) + 1.4 * math.sin(i * 2.3)) * (1 if x1 > x0 else -1), y))
        return pts + [(face, 138), (x0, 138)]
    L = cliff(0, 1, 50, 72)
    Rt = cliff(200, -1, 62, 134)
    g.light(104, 40, 80)
    for P, ang in ((L, 70), (Rt, 110)):
        d = path(P, True)
        g.hatch(d, ang, 2.4, .22)
        g.ln(path(P[:2]) + " " + smooth(P[1:-2]), 1.1, .9)
    g.hair(smooth([(70 + i * 3.4, 128 + 2 * math.sin(i)) for i in range(20)]), .4)
    g.hair(smooth([(72 + i * 3.3, 132 + 1.6 * math.sin(i + 1)) for i in range(19)]), .25)
    safe = [(60, 46), (80, 20), (120, 16), (150, 30), (176, 56)]
    g.ln(smooth(safe), 1, .55, "3 3")
    fast = [(64, 50), (100, 60), (138, 60)]
    g.ac(smooth(fast), 1.8)
    g.flow(smooth(fast))
    wing(g, 100, 42, 13, True)
    g.dot(64, 50, 2.2)


# ---------------------------------------------------------------- Know Your Equipment
def kye_a(g):
    cx, cy = 100, 50
    out = ell(cx, cy + 4, 82, 40, PI, 2 * PI, 48)
    inn = ell(cx, cy + 10, 76, 30, PI, 2 * PI, 48)
    g.light(100, 40, 90)
    band = path(out + inn[::-1], True)
    g.ink(band)
    g.hatch(path(out[24:] + inn[24:][::-1], True), 80, 1.6, .3)
    g.fill(band, .1)
    for i in range(0, 49, 2):
        g.hair(path([out[i], inn[i]]), .5)
    g.ln(path(out + inn[::-1], True), 1.3)
    rL, rR = (88, 122), (112, 122)
    for side, r in ((range(2, 24, 3), rL), (range(26, 47, 3), rR)):
        nodes = []
        idx = list(side)
        for j in range(0, len(idx), 2):
            grp = [inn[k] for k in idx[j:j + 2]]
            m = (sum(p[0] for p in grp) / len(grp) * .6 + r[0] * .4, sum(p[1] for p in grp) / len(grp) * .55 + r[1] * .45)
            for q in grp:
                g.hair(path([q, m]), .45)
            nodes.append(m)
        for m in nodes:
            g.hair(path([m, r]), .55)
    g.ac(path([inn[0], (inn[0][0] + 20, inn[0][1] + 36), rL]), 1.3)
    g.ac(path([inn[-1], (inn[-1][0] - 20, inn[-1][1] + 36), rR]), 1.3)
    g.ln("M86,122 h28 v8 q-14,6 -28,0 Z", 1.1)
    g.dot(rL[0], rL[1], 1.8)
    g.dot(rR[0], rR[1], 1.8)


def kye_b(g):
    g.light(90, 90, 80)
    outer = [(60, 96), (60, 120), (70, 132), (96, 132), (106, 120), (110, 88), (100, 78), (74, 78)]
    inner = [(68, 98), (68, 118), (74, 125), (92, 125), (99, 117), (102, 90), (96, 85), (78, 85)]
    metal = smooth(outer, True, .6) + " " + smooth(inner[::-1], True, .6)
    g.hatch(smooth(outer, True, .6), 30, 1.8, .3)
    g.ink(smooth(inner, True, .6))
    g.ln(smooth(outer, True, .6), 1.3)
    g.ln(smooth(inner, True, .6), .9, .8)
    g.ac(path([(62, 102), (70, 80)]), 2.2)
    for x0 in (80, 94):
        strap = [(x0, 84), (x0 + 6, 84), (x0 + 10 + (x0 - 87) * 1.2, 34), (x0 + 4 + (x0 - 87) * 1.2, 34)]
        g.ink(path(strap, True))
        g.ln(path(strap, True), 1)
        g.hair(path([((strap[0][0] + strap[1][0]) / 2, 80), ((strap[2][0] + strap[3][0]) / 2, 38)]), .6, "1.5 2")
    tops = [(83 + (80 - 87) * 1.2 + 4, 30), (97 + (94 - 87) * 1.2 + 4, 30)]
    for (x, y) in tops:
        g.ln(smooth(ell(x, y, 3.2, 4.4, 0, 2 * PI, 20), True), 1)
        for k in range(5):
            g.hair(path([(x, y - 4), (x - 26 + k * 13 + (x - 90) * .6, 4)]), .4)
    g.arrow((150, 112), (150, 64), True, 1.2, 5)
    g.hair(path([(140, 112), (160, 112)]), .4)
    g.hair(path([(140, 64), (160, 64)]), .4)


def kye_c(g):
    n = 34
    xs = [-1 + 2 * i / (n - 1) for i in range(n)]
    LE = [(100 + 90 * x, 44 + 26 * x ** 2) for x in xs]
    TE = [(100 + 90 * x, 98 - 8 * x ** 2 - 20 * max(0, abs(x) - .8) / .2) for x in xs]
    g.light(100, 70, 100)
    wingd = smooth(LE) + " L" + " L".join("%s,%s" % (f(x), f(y)) for x, y in TE[::-1]) + " Z"
    g.ink(wingd)
    g.fill(wingd, .08)
    g.hatch(path(LE[n // 2:] + TE[n // 2:][::-1], True), 0, 2.2, .2)
    for a, b in zip(LE[1:-1], TE[1:-1]):
        g.hair(path([a, b]), .4)
    for a in LE[2:-2:2]:
        g.hair(smooth(ell(a[0], a[1] + 2.5, 1.6, 1.1, 0, 2 * PI, 10), True), .6)
    g.ln(smooth(LE), 1.3)
    g.ln(smooth(TE[8:-8]), 1)
    g.ac(smooth(TE[:9]), 1.9)
    g.ac(smooth(TE[-9:]), 1.9)


# ---------------------------------------------------------------- Sky Gods
def sky_a(g):
    s = A.sky()
    far, near = s["far"], s["near"]
    g.light(96, 30, 80)
    g.fill(smooth(far) + " L200,138 L0,138 Z", .05)
    g.ln(smooth(far), .7, .35)
    nd = smooth(near) + " L200,138 L0,138 Z"
    g.ink(nd)
    g.hatch(nd, 120, 2.4, .2)
    for (x0, y0) in near[1:-1]:
        g.hair(path([(x0, y0), (x0 + 8, y0 + 30)]), .25)
    g.ln(smooth(near), 1.1, .85)
    g.ln(smooth(s["spiral"], t=.6), 1, .9)
    g.ac("M%s,%s H%s" % (f(s["cx"] - 28), f(s["stop"]), f(s["cx"] + 44)), 1, .7, "2 3")
    g.ac(smooth(s["wave"]), 2.2)
    g.flow(smooth(s["wave"]))
    lens = ell(140, 20, 26, 4.5, 0, 2 * PI, 30)
    g.hair(smooth(lens, True), .5)


def sky_b(g):
    peak = (108, 18)
    left = [(0, 128), (30, 110), (52, 86), (70, 70), (86, 44), peak]
    right = [peak, (124, 40), (136, 52), (152, 64), (170, 92), (200, 112)]
    g.light(108, 26, 80)
    mtn = path(left + right[1:] + [(200, 138), (0, 138)], True)
    g.ink(mtn)
    shadow = path([peak] + right[1:] + [(200, 138), (120, 138), (114, 90), (112, 54)], True)
    g.hatch(shadow, 100, 1.8, .3)
    g.hatch(path([peak, (86, 44), (98, 46), (104, 34)], True), 60, 1.6, .35)
    g.ln(path(left), 1.2)
    g.ln(path(right), 1.2)
    g.hair(path([peak, (112, 54), (114, 90), (120, 138)]), .5)
    g.hair(path([(70, 70), (78, 92), (74, 120)]), .3)
    g.hair(path([(152, 64), (146, 92)]), .3)
    x = 18
    g.hair(path([(x, 120), (x, 14)]), .4)
    for i in range(12):
        y = 120 - i * 9
        g.hair(path([(x, y), (x + (6 if i % 3 == 0 else 3), y)]), .5)
    g.ac(path([(x - 4, 18), (x + 10, 18)]), 1.6)
    g.hair(path([(x + 12, 18), (peak[0] - 6, 18)]), .3, "1 3")
    wing(g, 146, 26, 9, True)
    g.ac(smooth([(140, 50), (146, 44), (142, 38), (146, 34)]), 1, .8)


def sky_c(g):
    g.light(100, 50, 100)
    ridge = [(0, 122), (24, 112), (44, 96), (58, 90), (72, 100), (96, 118), (200, 126)]
    rd = smooth(ridge) + " L200,138 L0,138 Z"
    g.ink(rd)
    g.hatch(rd, 60, 2.2, .25)
    g.ln(smooth(ridge), 1.2)
    for k in range(6):
        y0 = 84 - k * 13
        amp = 9 + k * 1.5
        pts = [(x, y0 - amp * math.exp(-((x - 58) / 22) ** 2)) if x < 58 else
               (x, y0 - amp * math.cos((x - 58) / 46 * 2 * PI) * math.exp(-(x - 58) / 240)) for x in range(0, 201, 4)]
        g.hair(smooth(pts), .45 if k % 2 else .3)
    for cx, cy, rx in ((106, 36, 18), (106, 30, 13), (154, 34, 14)):
        lens = [(cx + rx * math.cos(t), cy - 3.4 * math.sin(t) * (1 if math.sin(t) > 0 else .5)) for t in [2 * PI * i / 40 for i in range(40)]]
        g.ink(smooth(lens, True))
        g.ln(smooth(lens, True), .9, .9)
    climb = [(100, 70), (103, 58), (106, 46)]
    g.ac(smooth(climb), 1.8)
    g.flow(smooth(climb))
    wing(g, 100, 74, 7, True, False)


# ---------------------------------------------------------------- Navigators
def nav_a(g):
    c, R = (100, 69), 56
    g.light(86, 50, 90)
    disc = smooth(ell(c[0], c[1], R, R, 0, 2 * PI, 60), True)
    g.ink(disc)
    g.hatch("M100,13 A56,56 0 0 1 100,125 A30,56 0 0 0 100,13 Z", 45, 1.8, .3)
    for fr in (.25, .55, .82):
        g.hair(path(ell(c[0], c[1], R * fr, R, -PI / 2, PI / 2, 40)), .3)
        g.hair(path(ell(c[0], c[1], R * fr, R, PI / 2, 3 * PI / 2, 40)), .3)
    for lat in (-.6, -.3, 0, .3, .6):
        w = R * math.sqrt(1 - lat * lat)
        g.hair(path(ell(c[0], c[1] + lat * R, w, w * .18, 0, PI, 30)), .3)
    g.ln(disc, 1.3)
    pins = [(66, 82), (112, 78), (140, 54), (126, 100)]
    for a, b in zip(pins, pins[1:]):
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 16)
        g.ac("M%s,%s Q%s,%s %s,%s" % (f(a[0]), f(a[1]), f(m[0]), f(m[1]), f(b[0]), f(b[1])), 1.4)
    for x, y in pins:
        g.ring(x, y, 3.4, True, 1)
        g.dot(x, y, 1.3)


def nav_b(g):
    c = (100, 69)
    g.light(100, 69, 70)
    for r, op in ((60, .9), (52, .4), (30, .3)):
        (g.ln if op > .5 else g.hair)(smooth(ell(c[0], c[1], r, r, 0, 2 * PI, 60), True), *((1.1, op) if op > .5 else (op,)))
    for i in range(72):
        t = 2 * PI * i / 72
        l = 7 if i % 9 == 0 else 3.5
        g.hair(path([(c[0] + 60 * math.cos(t), c[1] + 60 * math.sin(t)), (c[0] + (60 - l) * math.cos(t), c[1] + (60 - l) * math.sin(t))]),
               .7 if i % 9 == 0 else .4)
    for i in range(8):
        t = -PI / 2 + i * PI / 4
        L = 48 if i % 2 == 0 else 26
        w = 7 if i % 2 == 0 else 5
        tip = (c[0] + L * math.cos(t), c[1] + L * math.sin(t))
        lft = (c[0] + w * math.cos(t - PI / 2), c[1] + w * math.sin(t - PI / 2))
        rgt = (c[0] + w * math.cos(t + PI / 2), c[1] + w * math.sin(t + PI / 2))
        half = path([c, tip, rgt], True)
        g.ink(path([c, lft, tip, rgt], True))
        g.hatch(half, t * 180 / PI + 90, 1.4, .45, top=True)
        if i == 0:
            g.ac(path([c, lft, tip, rgt], True), 1.5)
        else:
            g.ln(path([c, lft, tip, rgt], True), .9 if i % 2 == 0 else .7, .9)
    g.ring(c[0], c[1], 3, True, 1)


def nav_c(g):
    g.light(100, 69, 90)
    for i, (cx, cy, R, ph) in enumerate(((66, 76, 46, .4), (148, 56, 34, 1.7))):
        for k in range(6):
            r = R * (1 - k * .16)
            g.hair(smooth(blob(cx, cy, r, ph + k * .2), True), .45 if k % 2 == 0 else .25)
    g.hatch(smooth(blob(66, 76, 46 * .2, .4 + 1), True), 45, 1.4, .4)
    tp = [(30, 112), (70, 40), (150, 56), (172, 112)]
    for (x, y), r in zip(tp[1:-1], (12, 10)):
        g.ln(smooth(ell(x, y, r, r, 0, 2 * PI, 40), True), .9, .6, "2 2.5")
    g.ln(path(ell(tp[-1][0], tp[-1][1], 7, 7, 0, 2 * PI, 30)), 1, .8)
    route = [tp[0], (70, 52), (140, 59), (168, 106)]
    g.ac(path(route), 1.7)
    g.flow(path(route))
    for p in route[1:-1]:
        g.dot(p[0], p[1], 1.8)
    g.dot(tp[0][0], tp[0][1], 2.8)


# ---------------------------------------------------------------- Living the Dream
def live_a(g):
    hy = 92
    g.light(100, hy, 90, .2)
    sun = ell(100, hy, 22, 22, PI, 2 * PI, 40)
    for i in range(1, 24):
        t = PI + PI * i / 24
        g.hair(path([(100 + 27 * math.cos(t), hy + 27 * math.sin(t)), (100 + (34 + 6 * (i % 2)) * math.cos(t), hy + (34 + 6 * (i % 2)) * math.sin(t))]), .45)
    g.hatch(path(sun, True), 0, 2, .35)
    g.ac(path(sun), 1.8)
    g.ln(path([(10, hy), (190, hy)]), .9, .6)
    for k, y in enumerate((100, 110, 122)):
        pts = [(x, y + (2.5 + k) * math.sin(x / (9 + k * 3) + k)) for x in range(0, 201, 5)]
        cloud = smooth(pts) + " L200,138 L0,138 Z"
        g.ink(cloud)
        g.hatch(cloud, 0, 2.6 + k * .4, .12)
        g.ln(smooth(pts), .8, .7 - k * .15)
    wing(g, 150, 38, 12)
    g.hair(smooth([(60, 52), (100, 44), (138, 42)]), .3, "2 3")


def live_b(g):
    g.light(70, 40, 90)
    cliff = [(120, 138), (122, 108), (130, 96), (126, 82), (136, 70), (150, 62), (200, 58), (200, 138)]
    cd = smooth(cliff[:-1]) + " L200,138 Z"
    g.ink(cd)
    g.hatch(cd, 100, 2, .3)
    g.ln(smooth(cliff[:-1]), 1.2)
    for k in range(7):
        y = 108 + k * 4.4
        g.hair(path([(4 + k * 3, y), (118 - k * 1, y)]), .45 - k * .05, "%s %s" % (6 + k, 3 + k % 3))
    for k, y in enumerate((64, 78, 92)):
        pts = [(x, y + (0 if x < 80 else -(x - 80) ** 2 / (220 + k * 60))) for x in range(0, 141, 6)]
        g.hair(smooth(pts), .35)
        if k == 1:
            g.flow(smooth(pts), .4)
    beat = ell(132, 46, 30, 7, 0, 2 * PI, 40, -.12)
    g.ac(smooth(beat, True), 1.2, .8, "4 3")
    wing(g, 104, 44, 11, True)


def live_c(g):
    arc = [(x, 104 - 28 * math.sin(math.pi * (x - 4) / 192)) for x in range(4, 197, 6)]
    route = [(24, 92), (52, 72), (80, 60), (104, 66), (128, 52), (156, 58), (178, 42)]
    land = path(arc + [(196, 138), (4, 138)], True)
    g.light(140, 40, 90)
    g.hatch(land, 0, 2.4, .2)
    for dy in (8, 16, 24):
        g.hair(smooth([(x, y + dy) for x, y in arc]), .2)
    g.ln(smooth(arc), 1.2, .9)
    for x, y in route[1:-1]:
        g.hair(path([(x, y + 3), (x, y + 14)]), .35)
    g.ac(smooth(route), 1.8)
    g.flow(smooth(route))
    for x, y in route[1:-1]:
        g.ring(x, y, 2.6, True, 1)
    g.dot(178, 42, 3.2)
    g.ring(178, 42, 6.5, True, .8)


# ---------------------------------------------------------------- World Cups
def wc_a(g):
    C, rx, ry, h = (120, 92), 30, 9, 58
    g.light(120, 60, 80)
    side = path(ell(C[0], C[1], rx, ry, 0, PI, 30) + ell(C[0], C[1] - h, rx, ry, PI, 0, 30), True)
    g.ink(side)
    g.hatch(path(ell(C[0], C[1], rx, ry, 0, PI * .45, 15) + ell(C[0], C[1] - h, rx, ry, PI * .45, 0, 15), True), 90, 1.8, .3)
    g.ln(path(ell(C[0], C[1] - h, rx, ry, 0, 2 * PI, 50)), 1, .9)
    g.ln(path(ell(C[0], C[1], rx, ry, 0, PI, 30)), 1.1)
    g.hair(path(ell(C[0], C[1], rx, ry, PI, 2 * PI, 30)), .35, "2 2")
    g.ln(path([(C[0] - rx, C[1]), (C[0] - rx, C[1] - h)]), 1)
    g.ln(path([(C[0] + rx, C[1]), (C[0] + rx, C[1] - h)]), 1)
    tag = (C[0] - 12, C[1] - h - 8)
    for k in range(7):
        pts = [(8, 54 + k * 8), (54, 42 + k * 4), (tag[0] + k * 2, tag[1] - 2 + k * .8), (196, 30 + k * 6)]
        g.hair(smooth(pts), .35)
    lead = [(10, 46), (56, 34), (tag[0] - 2, tag[1] - 4), (196, 22)]
    g.ac(smooth(lead), 1.8)
    g.flow(smooth(lead))
    for x, y in ((40, 39), (74, 30)):
        wing(g, x, y - 6, 7, True, False)


def wc_b(g):
    g.light(100, 50, 80)
    bowl = [(68, 22), (70, 46), (80, 64), (94, 72), (106, 72), (120, 64), (130, 46), (132, 22)]
    bd = smooth(bowl) + " Z"
    g.ink(bd)
    g.hatch(path(bowl[3:] + [(132, 22), (112, 22)], True), 75, 1.6, .32)
    g.ln(smooth(bowl), 1.3)
    g.ac(smooth(ell(100, 22, 32, 4.5, 0, 2 * PI, 40), True), 1.4)
    for s in (-1, 1):
        x = 100 + s * 31
        g.ln(smooth([(x, 30), (x + s * 18, 30), (x + s * 18, 46), (x + s * 2, 56)]), 1.1, .9)
    g.ln(path([(96, 72), (96, 96), (104, 96), (104, 72)]), 1.1)
    g.ln(smooth([(96, 84), (92, 88), (96, 92)]), .8, .7)
    for y0, w0, hh in ((96, 18, 8), (104, 26, 10)):
        r = [(100 - w0, y0), (100 + w0, y0), (100 + w0 + 2, y0 + hh), (100 - w0 - 2, y0 + hh)]
        g.ink(path(r, True))
        g.hatch(path([(100 + w0 * .3, y0), (100 + w0, y0), (100 + w0 + 2, y0 + hh), (100 + w0 * .3, y0 + hh)], True), 90, 1.6, .3)
        g.ln(path(r, True), 1.1)
    wing(g, 100, 38, 13, True, True)
    for s in (-1, 1):
        stem = [(100 + s * (40 + 30 * math.sin(t * PI * .5)), 122 - 70 * t) for t in [i / 20 for i in range(21)]]
        g.ln(smooth(stem), .8, .6)
        for i in range(2, 20, 3):
            (x, y), (x2, y2) = stem[i], stem[i + 1]
            ang = math.atan2(y2 - y, x2 - x)
            for side in (-1, 1):
                a = ang + side * .7
                cx, cy = x + 5 * math.cos(a), y + 5 * math.sin(a)
                leaf = smooth(ell(cx, cy, 5, 2, 0, 2 * PI, 14, a), True)
                g.ink(leaf)
                g.ln(leaf, .8, .75)


def wc_c(g):
    c, R = (100, 76), 48
    g.light(100, 70, 80)
    g.ln("M94,18 h12 v8 h-12 Z", 1)
    g.ln(path([(100, 26), (100, c[1] - R)]), 1.2)
    g.ln("M%s,%s l8,-8" % (f(c[0] + R * .72), f(c[1] - R * .72)), 1.2)
    disc = smooth(ell(c[0], c[1], R, R, 0, 2 * PI, 60), True)
    g.ink(disc)
    g.ln(disc, 1.3)
    g.hair(smooth(ell(c[0], c[1], R - 5, R - 5, 0, 2 * PI, 60), True), .3)
    for i in range(60):
        t = -PI / 2 + 2 * PI * i / 60
        l = 6 if i % 5 == 0 else 3
        g.hair(path([(c[0] + (R - 5) * math.cos(t), c[1] + (R - 5) * math.sin(t)), (c[0] + (R - 5 - l) * math.cos(t), c[1] + (R - 5 - l) * math.sin(t))]),
               .75 if i % 5 == 0 else .35)
    t1 = -PI / 2 + 2 * PI * .3
    sec = path([c] + ell(c[0], c[1], R - 14, R - 14, -PI / 2, t1, 30), True)
    g.hatch(sec, 30, 1.8, .4)
    g.ac(path(ell(c[0], c[1], R - 14, R - 14, -PI / 2, t1, 30)), 1.4, .9)
    g.ac(path([c, (c[0] + (R - 9) * math.cos(t1), c[1] + (R - 9) * math.sin(t1))]), 1.8)
    g.ln(path([c, (c[0] + 22 * math.cos(-PI * .85), c[1] + 22 * math.sin(-PI * .85))]), 1.3)
    g.hair(smooth(ell(c[0], c[1] + 20, 9, 9, 0, 2 * PI, 30), True), .5)
    g.ring(c[0], c[1], 3, True, 1.2)


# ---------------------------------------------------------------- Resources, Tools and Tips
def res_a(g):
    fr = (22, 22, 156, 94)
    g.light(100, 60, 90)
    x0, y0, w, h = fr
    g.ln("M%s,%s h%s a6,6 0 0 1 6,6 v%s a6,6 0 0 1 -6,6 h-%s a6,6 0 0 1 -6,-6 v-%s a6,6 0 0 1 6,-6 Z" % (
        f(x0 + 6), f(y0), f(w - 12), f(h - 12), f(w - 12), f(h - 12)), 1.2)
    for i in range(1, 8):
        g.hair(path([(x0 + i * w / 8, y0 + 8), (x0 + i * w / 8, y0 + h - 8)]), .12)
    for j in range(1, 5):
        g.hair(path([(x0 + 8, y0 + j * h / 5), (x0 + w - 8, y0 + j * h / 5)]), .12)
    base = y0 + h * .7
    g.hair(path([(x0 + 8, base), (x0 + w - 8, base)]), .4)
    pts, cyc, x = [], 0.0, x0 + 10.0
    while x <= x0 + w - 10:
        per = 22 + (x - x0) * .08
        ph = cyc % 1
        b = math.sin(ph / .35 * PI / 2) if ph < .35 else math.cos((ph - .35) / .65 * PI / 2)
        amp = 40 * math.exp(-(x - x0) / 120) + 6
        pts.append((x, base - amp * b))
        cyc += 1.0 / per
        x += 1.0
    fill = path(pts + [(pts[-1][0], base), (pts[0][0], base)], True)
    g.hatch(fill, 90, 1.6, .3)
    g.ac(path(pts), 1.6)
    g.flow(path(pts))
    for k in range(6):
        g.ln(path([(x0 + w - 18, y0 + h - 14 - k * 5), (x0 + w - 12, y0 + h - 14 - k * 5)]), 2, .9 - k * .12)


def res_b(g):
    g.light(100, 60, 90)
    Lp = [(100, 34), (64, 26), (24, 30), (24, 112), (64, 108), (100, 116)]
    Rp = [(100, 34), (136, 26), (176, 30), (176, 112), (136, 108), (100, 116)]
    for P in (Lp, Rp):
        d = "M%s,%s Q%s,%s %s,%s L%s,%s Q%s,%s %s,%s Z" % (f(P[0][0]), f(P[0][1]), f(P[1][0]), f(P[1][1]), f(P[2][0]), f(P[2][1]),
                                                       f(P[3][0]), f(P[3][1]), f(P[4][0]), f(P[4][1]), f(P[5][0]), f(P[5][1]))
        g.ink(d)
        g.ln(d, 1.2)
    for k in range(3):
        g.hair("M%s,%s Q%s,%s %s,%s" % (f(100 - 2 - k * 2), f(118 + k * 2), f(64), f(110 + k * 2), f(24 + k), f(114 + k * 2)), .35)
        g.hair("M%s,%s Q%s,%s %s,%s" % (f(100 + 2 + k * 2), f(118 + k * 2), f(136), f(110 + k * 2), f(176 - k), f(114 + k * 2)), .35)
    g.hatch(path([(94, 36), (100, 34), (100, 116), (94, 113)], True), 0, 1.6, .4)
    for i in range(9):
        y = 42 + i * 7.6
        w = 56 if i % 4 != 3 else 34
        g.hair("M%s,%s q%s,-3 %s,-1" % (f(34), f(y + 1), f(w / 2), f(w)), .45)
    wing(g, 138, 56, 18)
    g.hair(smooth([(116, 92), (134, 86), (150, 92), (166, 84)]), .6, "2 2")
    rib = [(104, 112), (110, 112), (110, 134), (107, 130), (104, 134)]
    g.hatch(path(rib, True), 90, 1, .6)
    g.ac(path(rib, True), 1.3)


def res_c(g):
    g.light(80, 50, 90)
    g.ln(path([(42, 128), (42, 30)]), 1.4)
    g.hatch(path([(40, 128), (44, 128), (44, 30), (40, 30)], True), 90, 1, .5)
    g.ln("M30,128 h24", 1.1)
    g.ring(42, 30, 2.4, False, 1)
    cone = lambda u, s: (46 + u * 112, 38 + u * 12 + s * (14 - 9 * u) + 6 * u * u * math.sin(u * 5))
    segs = 5
    for i in range(segs):
        u0, u1 = i / segs, (i + 1) / segs
        poly = [cone(u0, -1), cone(u1, -1), cone(u1, 1), cone(u0, 1)]
        d = path(poly, True)
        g.ink(d)
        if i % 2 == 0:
            g.hatch(d, 80, 1.5, .5)
        g.ln(d, 1, .9)
    g.ac(smooth([cone(u / 20, -1) for u in range(21)]), 1.6)
    g.ac(path([cone(1, -1), cone(1, 1)]), 1.6)
    for k, y in enumerate((70, 86, 102)):
        pts = [(x, y + 4 * math.sin(x / 20 + k)) for x in range(56, 196, 6)]
        g.hair(smooth(pts), .35)
        if k == 1:
            g.flow(smooth(pts), .4)


# ---------------------------------------------------------------- Weather Patterns
def wx_a(g):
    w = A.weather()
    x0, x1, y0, y1 = w["axes"]
    g.light(110, 60, 90)
    for i in range(1, 7):
        y = y0 - i * (y0 - y1) / 7
        g.hair(path([(x0, y), (x1, y)]), .1)
    for a, b in w["adiab"]:
        g.hair(path([a, b]), .22)
    g.hair(path([(x0, y1), (x0, y0), (x1, y0)]), .5)
    for i in range(8):
        y = y0 - i * (y0 - y1) / 7
        g.hair(path([(x0 - 3, y), (x0, y)]), .5)
    mid, dew = w["mid"], w["dew"]
    band = path(mid + dew[::-1], True)
    g.hatch(band, 135, 2.2, .2)
    g.ln(smooth(dew), 1.1, .9)
    g.ac(path(mid), 1.9)
    g.flow(path(mid), .5)
    kx, ky = w["kink"]
    g.ring(kx, ky, 4.4)
    g.hair(path([(x0, ky), (kx - 6, ky)]), .5, "1.5 2.5")
    cx, cy = w["cloud"]
    cl = [(cx - 16, cy), (cx - 14, cy - 7), (cx - 6, cy - 12), (cx + 2, cy - 15), (cx + 10, cy - 10), (cx + 16, cy - 5), (cx + 17, cy)]
    g.ink(smooth(cl) + " Z")
    g.ln(smooth(cl) + " Z", .9, .8)


def wx_b(g):
    g.light(100, 40, 90)
    base = 54
    top = [(44, base), (46, 42), (56, 34), (62, 24), (74, 18), (84, 10), (98, 8), (110, 12), (120, 8), (134, 14), (142, 26),
           (152, 32), (158, 44), (156, base)]
    cd = smooth(top) + " Z"
    g.ink(cd)
    g.hatch(path([(44, base), (156, base), (157, 42), (150, 36), (44, 44)], True), 0, 1.6, .35)
    g.hatch(path([(120, 8), (134, 14), (142, 26), (152, 32), (158, 44), (156, base), (128, base), (124, 24)], True), 60, 2, .25)
    g.ln(smooth(top) + " Z", 1.3)
    for a, b, c in (((70, 30), (78, 24), (86, 22)), ((100, 22), (110, 18), (118, 22)), ((126, 32), (136, 30), (140, 38))):
        g.hair(smooth([a, b, c]), .45)
    g.ac(path([(14, base), (40, base)]), 1.2, .8, "3 3")
    g.ac(path([(160, base), (190, base)]), 1.2, .8, "3 3")
    gnd = [(0, 124), (40, 122), (80, 126), (120, 124), (160, 127), (200, 124)]
    g.ln(smooth(gnd), 1)
    g.hatch(path([(76, 125), (124, 124), (124, 138), (76, 138)], True), 45, 1.6, .4)
    for k, dx in enumerate((-22, -11, 0, 11, 22)):
        pts = [(100 + dx * (1 - .5 * t) + 3 * math.sin(t * 6 + k), 122 - t * 66) for t in [i / 20 for i in range(21)]]
        if dx == 0:
            g.ac(smooth(pts), 1.8)
            g.flow(smooth(pts))
            g.head((pts[-1][0], pts[-1][1] - 2), (0, -1), 5)
        else:
            g.hair(smooth(pts), .45)


def wx_c(g):
    g.light(70, 70, 90)
    c = (70, 72)
    for k in range(6):
        r = 16 + k * 15
        g.hair(smooth(blob(c[0], c[1], r, .6 + k * .15, 72, (.08, .05)), True), .5 if k % 2 == 0 else .3)
    g.hatch(smooth(blob(c[0], c[1], 12, .6, 40, (.08, .05)), True), 45, 1.4, .5)
    g.ln(path([(c[0] - 4, c[1] - 4), (c[0] - 4, c[1] + 4), (c[0] + 3, c[1] + 4)]), 1.4)
    front = [(c[0] + 8, c[1] - 2), (110, 62), (140, 70), (168, 92), (186, 122)]
    sp = smooth(front)
    g.ac(sp, 1.8)
    pts = []
    for i in range(len(front) - 1):
        a, b = front[i], front[i + 1]
        for t in [j / 6 for j in range(6)]:
            pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    for j, p in enumerate(pts[3::3]):
        i = pts.index(p)
        q = pts[min(i + 1, len(pts) - 1)]
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        if j % 2 == 0:
            tri = [(p[0] - ux * 4, p[1] - uy * 4), (p[0] + ux * 4, p[1] + uy * 4), (p[0] + uy * 6, p[1] - ux * 6)]
            g.top.append('<path d="%s" fill="%s"/>' % (path(tri, True), g.ac_))
        else:
            semi = ell(p[0], p[1], 4, 4, math.atan2(uy, ux) + PI, math.atan2(uy, ux) + 2 * PI, 12)
            g.top.append('<path d="%s" fill="%s"/>' % (path([(p[0] - ux * 4, p[1] - uy * 4)] + [(2 * p[0] - x, 2 * p[1] - y) for x, y in semi[::-1]], True), g.ac_))
    for k, y in enumerate((24, 112)):
        g.hair(smooth([(x, y + 6 * math.sin(x / 30 + k)) for x in range(110, 201, 6)]), .25)


# ---------------------------------------------------------------- Brand Stories
def brand_a(g):
    g.light(100, 60, 100)
    base = 112
    g.hair(path([(14, base), (186, base)]), .45)
    for k, (cx, sz) in enumerate(((44, 18), (98, 24), (156, 30))):
        wing(g, cx, base - sz * 1.05 - 10, sz, k == 2)
        g.hair(path([(cx, base - 2), (cx, base + 4)]), .6)
        y = base + 12
        g.hair(path([(cx - sz, y), (cx + sz, y)]), .45)
        g.hair(path([(cx - sz, y - 3), (cx - sz, y + 3)]), .45)
        g.hair(path([(cx + sz, y - 3), (cx + sz, y + 3)]), .45)
    g.ac(path([(156 - 30, base + 12), (156 + 30, base + 12)]), 1.4)


def brand_b(g):
    up, lo = naca(.16, .04, .32, 70)
    x0, y0, c = 24, 74, 152
    U = [(x0 + c * x, y0 - c * y) for x, y in up]
    L = [(x0 + c * x, y0 - c * y) for x, y in lo]
    foil = U + L[::-1]
    g.light(90, 60, 100)
    g.ink(path(foil, True))
    g.fill(path(foil, True), .06)
    g.ln(path(foil, True), 1.3)
    off = [(x, y - 5) for x, y in U] + [(x, y + 5) for x, y in L[::-1]]
    g.hair(smooth(off, True), .4, "3 2")
    for fr, r in ((.2, 6), (.36, 7), (.52, 6), (.68, 4.6)):
        i = int(fr * (len(U) - 1))
        cx = (U[i][0] + L[i][0]) / 2
        cy = (U[i][1] + L[i][1]) / 2
        hh = (L[i][1] - U[i][1]) * .3
        e = ell(cx, cy, r, max(2.4, hh), 0, 2 * PI, 30)
        g.hatch(smooth(e, True), 45, 1.2, .5)
        g.ac(smooth(e, True), 1.2)
    for fr in (.1, .5, .9):
        i = int(fr * (len(U) - 1))
        g.hair(path([(U[i][0], U[i][1] - 7), (U[i][0], U[i][1] - 2)]), .7)
        g.hair(path([(L[i][0], L[i][1] + 2), (L[i][0], L[i][1] + 7)]), .7)
    g.arrow((60, 120), (140, 120), False, .7, 4)
    g.head((60, 120), (-1, 0), 4, False)
    g.hair(path([(150, 28), (170, 28), (170, 40)]), .5)
    g.hair(path([(30, 28), (30, 40)]), .3)


def brand_c(g):
    c = (100, 69)
    g.light(100, 69, 70)
    g.ac(smooth(ell(c[0], c[1], 60, 60, 0, 2 * PI, 80), True), 1.4)
    g.ln(smooth(ell(c[0], c[1], 55, 55, 0, 2 * PI, 80), True), .8, .7)
    for i in range(48):
        t = 2 * PI * i / 48
        g.dot(c[0] + 50 * math.cos(t), c[1] + 50 * math.sin(t), .9, False)
    inner = ell(c[0], c[1], 44, 44, 0, 2 * PI, 60)
    g.ln(smooth(inner, True), 1, .9)
    mt = [(56, 96), (74, 78), (86, 86), (104, 62), (120, 80), (132, 72), (144, 96)]
    g.hatch(path(mt + [(144, 104), (56, 104)], True), 120, 1.7, .35)
    g.ln(path(mt), 1.1)
    g.hair(path([(58, 104), (142, 104)]), .5)
    wing(g, 100, 46, 20, True)
    for s in (-1, 1):
        for k in range(4):
            g.hair(smooth(ell(c[0] + s * (36 - k * 2), c[1] + 24 + k * 5, 3, 1.5, 0, 2 * PI, 10, s * .6), True), .4)


# ---------------------------------------------------------------- Storytellers
def story_a(g):
    ridge = lambda y0, a, s: [(x, y0 - a * math.exp(-((x - 60) / 26) ** 2) - a * .8 * math.exp(-((x - 140) / 30) ** 2) - 6 * math.sin(x / s))
                               for x in range(0, 201, 5)]
    far, near = ridge(90, 30, 9), ridge(114, 44, 13)
    g.light(170, 24, 90, .18)
    g.fill(smooth(far) + " L200,138 L0,138 Z", .05)
    g.ln(smooth(far), .8, .45)
    nd = smooth(near) + " L200,138 L0,138 Z"
    g.ink(nd)
    g.hatch(nd, 70, 2.2, .22)
    g.ln(smooth(near), 1.2, .9)
    for k in range(4):
        g.hair(path([(0, 56 - k * 9), (200, 26 - k * 9)]), .12)
    track = [(176, 22), (150, 26), (126, 36), (112, 58), (104, 82), (98, 100)]
    g.ac(smooth(track), 1.8)
    g.flow(smooth(track))
    g.ring(176, 22, 6, True, .8)
    g.dot(176, 22, 2.6)


def story_b(g):
    g.light(100, 50, 80)
    cap = "M84,22 a16,16 0 0 1 32,0 v34 a16,16 0 0 1 -32,0 Z"
    g.ink(cap)
    g.hatch(cap, 45, 2.2, .35)
    g.hatch(cap, -45, 2.2, .35)
    g.ln(cap, 1.3)
    g.hair(path([(84, 40), (116, 40)]), .6)
    g.ln("M74,46 v10 a26,26 0 0 0 52,0 v-10", 1.1)
    g.ln(path([(100, 82), (100, 112)]), 1.2)
    g.ln("M80,118 q20,-8 40,0", 1.2)
    for s in (-1, 1):
        for k, r in enumerate((30, 44, 58)):
            a0, a1 = (-PI * .22, PI * .22) if s > 0 else (PI * .78, PI * 1.22)
            g.ac(path(ell(100, 40, r, r * .9, a0, a1, 20)), 1.6 - k * .35, 1 - k * .25)
    g.hair(path([(10, 126), (190, 126)]), .3)


def story_c(g):
    g.light(100, 70, 100)
    mid = 92
    prof = lambda x: 10 + 38 * math.exp(-((x - 62) / 24) ** 2) + 30 * math.exp(-((x - 138) / 30) ** 2) + 6 * math.sin(x / 7)
    for i, x in enumerate(range(12, 190, 4)):
        h = prof(x) * (.75 + .25 * math.sin(i * 2.3) ** 2)
        g.ln(path([(x, mid), (x, mid - h)]), 1.4, .9)
        g.hair(path([(x, mid + 3), (x, mid + 3 + h * .28)]), .3)
    g.hair(path([(8, mid + 1.5), (192, mid + 1.5)]), .4)
    track = [(20, 30), (60, 18), (100, 32), (140, 20), (180, 28)]
    g.ac(smooth(track), 1.6)
    g.flow(smooth(track))
    wing(g, 180, 22, 6, True, False)


# ---------------------------------------------------------------- The Dark Side
def dark_a(g):
    g.light(100, 30, 90, .1)
    cb = [(44, 92), (40, 80), (46, 70), (44, 58), (54, 48), (56, 36), (66, 28), (40, 24), (22, 18), (60, 10), (110, 7), (160, 9),
          (192, 14), (170, 20), (142, 26), (150, 36), (148, 48), (158, 58), (156, 72), (162, 82), (156, 92)]
    cd = smooth(cb) + " Z"
    g.ink(cd)
    g.hatch(path([(48, 92), (152, 92), (152, 72), (48, 72)], True), 0, 1.4, .4)
    g.hatch(cd, 115, 2.4, .2)
    g.ln(cd, 1.3)
    for a in ((68, 52), (84, 40), (110, 36), (128, 52)):
        g.hair(smooth([a, (a[0] + 8, a[1] - 6), (a[0] + 16, a[1] - 2)]), .4)
    for i in range(16):
        x = 58 + i * 5.6
        g.hair(path([(x, 96), (x - 8, 128)]), .3 - (i % 3) * .05)
    bolt = [(112, 92), (104, 108), (112, 108), (100, 128)]
    g.ac(path(bolt), 1.8)
    g.hair(path([(0, 132), (200, 132)]), .3)
    wing(g, 178, 70, 7)
    g.hair(smooth([(176, 76), (164, 70), (154, 62)]), .5, "2 2")


def dark_b(g):
    g.light(100, 50, 90)
    cx, cy, s = 100, 54, 70
    top = ell(cx, cy, s, s * .4, PI * 1.3, 2 * PI, 30)
    bot = ell(cx, cy + 7, s * .93, s * .28, 2 * PI, PI * 1.3, 30)
    shape = path(top + bot, True)
    g.ink(shape)
    g.fill(shape, .1)
    g.hatch(shape, 80, 2, .2)
    g.ln(shape, 1.3)
    a = top[0]
    fold = [a, (a[0] - 18, a[1] + 16), (a[0] - 8, a[1] + 30), (a[0] + 10, a[1] + 22)]
    fd = smooth(fold) + " Z"
    g.ink(fd)
    g.hatch(fd, 30, 1.4, .45)
    g.ac(smooth(fold) + " Z", 1.6)
    p = (cx, 124)
    for q in bot[::6]:
        g.hair(path([q, p]), .45)
    for k in range(3):
        g.hair(smooth([fold[2], (fold[2][0] + 8 + k * 6, 90 + k * 4), (p[0] - 10, 112), p]), .45, "2 2")
    g.dot(p[0], p[1], 2.4, False)
    g.ac(path(ell(cx, cy + 34, 52, 16, PI * .15, PI * .65, 20)), 1.2, .8)
    g.head(ell(cx, cy + 34, 52, 16, PI * .65, PI * .65, 1)[0], (-1, -.2), 5)


def dark_c(g):
    g.light(100, 40, 90)
    c, R = (100, 50), 48
    dome = ell(c[0], c[1], R, R * .62, PI, 2 * PI, 40)
    rim = ell(c[0], c[1], R, R * .16, 0, PI, 30)
    shape = path(dome + rim, True)
    g.ink(shape)
    for i in range(0, 41, 5):
        if i in (0, 40):
            continue
        g.hair(smooth([dome[i], (c[0] + (dome[i][0] - c[0]) * .2, c[1] - R * .6)]), .45)
    g.hatch(path(dome[20:] + rim[:15], True), 75, 1.8, .3)
    g.ln(path(dome), 1.3)
    g.ac(path(rim), 1.8)
    g.ac(path(ell(c[0], c[1], R, R * .16, PI, 2 * PI, 30)), 1, .5)
    conf = (100, 104)
    for t in [i / 8 for i in range(9)]:
        q = rim[int(t * 30)]
        g.hair(path([q, conf]), .5)
    g.ln(path([conf, (100, 116)]), 1.1)
    g.dot(100, 118, 2.6, False)
    g.ln(smooth([(100, 118), (118, 126), (132, 120), (150, 130)]), .8, .5, "2 2")
    g.ln(smooth([(150, 130), (160, 122), (170, 132), (156, 134)], True), .9, .6)


# ---------------------------------------------------------------- Flight Mechanics
def fm_a(g):
    fl = A.flight()
    g.light(96, 60, 90)
    for k, st in enumerate(fl["streams"]):
        g.hair(smooth(st), .3 if k in (0, 4) else .55)
    g.flow(smooth(fl["streams"][2]), .6)
    foil = path(fl["foil"], True)
    g.ink(foil)
    g.hatch(foil, 20, 1.5, .4)
    g.ln(foil, 1.3)
    cp, lt = fl["cp"], fl["lift"]
    g.arrow(cp, lt, True, 1.8, 7)
    g.dot(cp[0], cp[1], 2.4)
    g.arrow((cp[0] + 4, cp[1] + 2), (cp[0] + 26, cp[1] + 6), False, .8, 4)


def fm_b(g):
    g.light(100, 60, 90)
    a = math.radians(12)
    ux, uy = math.cos(a), math.sin(a)
    P = (100, 62)
    g.hair(path([(P[0] - ux * 96, P[1] - uy * 96), (P[0] + ux * 96, P[1] + uy * 96)]), .45, "3 3")
    g.hair(path([(P[0] - 90, P[1]), (P[0] + 90, P[1])]), .25)
    g.ln(path(ell(P[0], P[1], 54, 54, 0, a, 12)), .8, .7)
    g.arrow(P, (P[0] + math.sin(a) * 46, P[1] - math.cos(a) * 46), False, 1.3, 6)
    g.arrow(P, (P[0] - ux * 30, P[1] - uy * 30), False, 1.1, 5)
    g.arrow(P, (P[0], P[1] + 54), True, 1.8, 7)
    wing(g, P[0] - 30, P[1] - 30, 10)
    res = (P[0] + math.sin(a) * 46 - ux * 30, P[1] - math.cos(a) * 46 - uy * 30)
    g.hair(path([(P[0] + math.sin(a) * 46, P[1] - math.cos(a) * 46), res, (P[0] - ux * 30, P[1] - uy * 30)]), .3, "2 2")


def fm_c(g):
    x0, y0, x1, y1 = 26, 26, 186, 126
    g.light(110, 70, 100)
    for i in range(1, 8):
        g.hair(path([(x0 + i * 20, y0), (x0 + i * 20, y1)]), .1)
    for j in range(1, 5):
        g.hair(path([(x0, y0 + j * 20), (x1, y0 + j * 20)]), .1)
    g.hair(path([(x0, y1), (x0, y0), (x1, y0)]), .55)
    for i in range(9):
        g.hair(path([(x0 + i * 20, y0 - 3), (x0 + i * 20, y0)]), .5)
    sink = lambda v: y0 + 20 + .004 * (v - 70) ** 2 + .00002 * (v - 70) ** 3
    curve = [(x, sink(x)) for x in range(50, 178, 3)]
    g.hatch(path(curve + [(curve[-1][0], y0), (curve[0][0], y0)], True), 90, 2.2, .2)
    g.ln(smooth(curve), 1.4)
    best = min(curve, key=lambda p: (p[1] - y0) / (p[0] - x0))
    k = (best[1] - y0) / (best[0] - x0)
    g.ac(path([(x0, y0), (x1, y0 + k * (x1 - x0))]), 1.6)
    g.ring(best[0], best[1], 4, True, 1.2)
    g.dot(best[0], best[1], 1.6)
    mn = min(curve, key=lambda p: p[1])
    g.ln(path([(mn[0], y0), (mn[0], mn[1])]), .8, .5, "2 2")
    g.dot(mn[0], mn[1], 2, False)


# ---------------------------------------------------------------- New Technologies
def nt_a(g):
    up, lo = naca(.18, .035, .35, 60)
    x0, y0, c = 34, 50, 132
    U = [(x0 + c * x, y0 - c * y) for x, y in up]
    L = [(x0 + c * x, y0 - c * y) for x, y in lo]
    lp = lambda fr: min(L, key=lambda q: abs((q[0] - x0) / c - fr))
    R = (96, 124)
    aa, bb, old = lp(.30), lp(.62), lp(.10)
    foil = path(U + L[::-1], True)
    g.light(96, 60, 100)
    g.ink(foil)
    g.hatch(foil, 20, 1.5, .35)
    g.ln(foil, 1.3)
    for fr in (.1, .2, .45, .8):
        q = lp(fr)
        g.hair(path([q, R]), .2, "2 2")
    g.ac(path([aa, (R[0] - 3, R[1])]), 1.7)
    g.ac(path([bb, (R[0] + 3, R[1])]), 1.7)
    g.ring(aa[0], aa[1], 2.8, True, 1)
    g.ring(bb[0], bb[1], 2.8, True, 1)
    g.ln("M88,124 h16 v6 q-8,4 -16,0 Z", 1)
    for k in range(4):
        y = 24 - k * 3
        g.hair(smooth([(10, y + 26), (60, y + 4 - k), (120, y), (196, y + 8)]), .25)


def nt_b(g):
    g.light(100, 60, 100)

    def P(u, v):
        th = u * 1.05
        cu = 1 - .45 * u * u
        x = 100 + 80 * math.sin(th) * (1 - .1 * v) + 24 * v * cu
        y = 90 - 62 * math.cos(th) + 34 * v * cu - 7 * math.sin(v * PI) * cu
        return (x, y)
    us = [-1 + i / 12 for i in range(25)]
    vs = [i / 8 for i in range(9)]
    skin = path([P(u, 0) for u in us] + [P(u, 1) for u in us[::-1]], True)
    g.ink(skin)
    g.hatch(path([P(u, 0) for u in us[12:]] + [P(u, 1) for u in us[12:][::-1]], True), 100, 1.8, .2)
    for v in vs:
        g.hair(smooth([P(u, v) for u in us]), .45 if v in (0, 1) else .3)
    for u in us:
        g.hair(smooth([P(u, v) for v in vs]), .3)
    g.ln(smooth([P(u, 1) for u in us]), 1)
    g.ac(smooth([P(u, 0) for u in us]), 1.9)
    g.flow(smooth([P(u, 0) for u in us]), .5)


def nt_c(g):
    g.light(70, 40, 90)
    c = (64, 38)
    a = math.radians(-20)

    def rot(x, y):
        return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))
    body = [rot(-8, -8), rot(8, -8), rot(8, 8), rot(-8, 8)]
    g.ink(path(body, True))
    g.hatch(path(body, True), 70, 1.4, .5)
    g.ln(path(body, True), 1.2)
    for s in (-1, 1):
        x0, x1 = (s * 12, s * 46)
        panel = [rot(x0, -6), rot(x1, -6), rot(x1, 6), rot(x0, 6)]
        g.ink(path(panel, True))
        g.ln(path(panel, True), 1)
        for k in range(1, 5):
            xx = x0 + (x1 - x0) * k / 5
            g.hair(path([rot(xx, -6), rot(xx, 6)]), .5)
        g.hair(path([rot(x0, 0), rot(x1, 0)]), .5)
        g.ln(path([rot(s * 8, 0), rot(x0, 0)]), .9)
    dish = rot(0, 12)
    g.ln(path([rot(0, 8), dish]), 1)
    g.ring(dish[0], dish[1], 2.4, False, 1)
    g.hair(path(ell(100, 150, 150, 120, PI * 1.12, PI * 1.6, 40)), .25, "2 3")
    tgt = (150, 104)
    ang = math.atan2(tgt[1] - dish[1], tgt[0] - dish[0])
    for k, r in enumerate((22, 40, 58, 76)):
        g.ac(path(ell(dish[0], dish[1], r, r, ang - .22, ang + .22, 10)), 1.5 - k * .2, 1 - k * .18)
    wing(g, tgt[0], tgt[1], 12, True)


OPTIONS = [
    ("Risk vs Reward", [("Valley lines", risk_a, "The two lines over the valley, the land engraved."),
                        ("The dial", risk_b, "An instrument dial, its needle at the edge of the gold."),
                        ("The gorge", risk_c, "Straight across the gorge, or the long way round.")]),
    ("Know Your Equipment", [("Canopy and lines", kye_a, "The wing from in front: cells, the line cascade, the brakes in gold."),
                             ("Carabiner and riser", kye_b, "The hardware up close: carabiner, risers, maillons, the speed bar travel."),
                             ("Planform", kye_c, "The wing from above, ribs and cell openings, the trailing edge in gold.")]),
    ("Sky Gods", [("Spiral and wave", sky_a, "Thermals to the top of the climb, then straight up in the wave."),
                  ("The big peak", sky_b, "A high summit, the height scale beside it, a wing above the ridge."),
                  ("Wave over the ridge", sky_c, "Air over a ridge in waves, lenticular clouds, the climb in gold.")]),
    ("Navigators", [("The globe", nav_a, "A shaded globe, routes arcing between places."),
                    ("Compass rose", nav_b, "An engraved compass rose, north in gold."),
                    ("Topo and task", nav_c, "Contour lines, turnpoint cylinders and the route through them.")]),
    ("Living the Dream", [("Above the clouds", live_a, "A wing over a sea of cloud, the sun on the horizon."),
                          ("Coastal soaring", live_b, "Beating along a sea cliff in the ridge lift."),
                          ("The road", live_c, "A long route across the land, stop after stop.")]),
    ("World Cups", [("The cylinder", wc_a, "The gaggle racing to a turnpoint cylinder."),
                    ("The trophy", wc_b, "A cup, engraved with a wing, between laurels."),
                    ("Start gate", wc_c, "A stopwatch, the race clock running in gold.")]),
    ("Resources, Tools and Tips", [("Vario trace", res_a, "An instrument screen with the climb trace and the climb bars."),
                                   ("The handbook", res_b, "An open notebook, notes on one page, a wing sketched on the other."),
                                   ("Windsock", res_c, "A striped windsock in the breeze.")]),
    ("Weather Patterns", [("The sounding", wx_a, "Temperature against height, the kink where climbs stop."),
                          ("Thermal and cumulus", wx_b, "A thermal rising from a sunny field to a cumulus, cloud base in gold."),
                          ("Isobars and front", wx_c, "A low, its isobars, and a front in gold.")]),
    ("Brand Stories", [("The line-up", brand_a, "One wing in three sizes, side by side, the largest in gold."),
                       ("Pattern piece", brand_b, "A rib as a cutting pattern: seam allowance, notches, the cross ports in gold."),
                       ("The seal", brand_c, "A maker's mark: a wing over mountains in a beaded ring.")]),
    ("Storytellers", [("The ridges", story_a, "Ranges in layers, a flight track coming down out of the light."),
                      ("The microphone", story_b, "An engraved microphone, the sound going out in gold."),
                      ("Voice into mountains", story_c, "A voice waveform that is also a mountain range.")]),
    ("The Dark Side", [("The storm", dark_a, "A cumulonimbus, rain and lightning, a wing at its edge."),
                       ("Collapse", dark_b, "A wing with one side folded under, starting to turn."),
                       ("The reserve", dark_c, "A reserve open, the wing below it in a tangle.")]),
    ("Flight Mechanics", [("Section and lift", fm_a, "The wing section in the airflow, the lift in gold."),
                          ("The forces", fm_b, "Lift, drag and weight on a wing on its glide path."),
                          ("The polar", fm_c, "The speed polar, the best glide tangent in gold.")]),
    ("New Technologies", [("Two-line wing", nt_a, "The section with the line attachments down to two."),
                          ("The mesh", nt_b, "A wing as a computer mesh, the leading edge in gold."),
                          ("Satellite", nt_c, "A navigation satellite, its signal reaching a wing.")]),
]


def slug(s):
    return re.sub(r"\W+", "", s.lower())


CSS = """
.so-sec{padding:var(--sp-4) var(--gutter);max-width:1320px;margin:0 auto;border-top:1px solid var(--line);}
.so-sec h2{font-family:var(--font-display);font-size:var(--fs-h3);color:var(--white);margin:0 0 var(--sp-3);}
.so-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-3);}
@media (max-width:900px){.so-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
.so-tile .shot{aspect-ratio:200/138;border-radius:10px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.35);}
.so-tile .shot svg{display:block;width:100%;height:100%;}
.so-tile.is-now .shot{opacity:.75;}
.so-tile h3{font-family:var(--font-display);font-size:var(--fs-body);color:var(--white);margin:.7rem 0 .2rem;}
.so-tile h3 b{color:var(--orange);font-weight:700;margin-right:.35rem;}
.so-tile p{font-size:var(--fs-small);color:var(--gray);line-height:1.55;margin:0;}
.so-intro{padding:var(--sp-4) var(--gutter) var(--sp-2);max-width:1320px;margin:0 auto;color:var(--gray-light);line-height:1.7;}
"""


def page():
    rows = ""
    for name, opts in OPTIONS:
        tiles = ('<div class="so-tile is-now"><div class="shot">%s</div><h3><b>Now</b>Today\'s Gold line</h3>'
                 '<p>As on the sample library page.</p></div>' % FULL.gold(name))
        for letter, (title, fn, cap) in zip("ABC", opts):
            g = G("so-%s-%s" % (slug(name)[:10], letter.lower()))
            fn(g)
            tiles += ('<div class="so-tile"><div class="shot">%s</div><h3><b>%s</b>%s</h3><p>%s</p></div>'
                      % (g.svg(name), letter, title, cap))
        rows += '<section class="so-sec"><h2>%s</h2><div class="so-grid">%s</div></section>' % (name, tiles)
    body = ('<header class="kit-hero is-sky v2-page-hero"><div class="kit-hero-copy"><span class="kit-kicker">Sample, not live</span>'
            '<h1>Series tiles: three drawings each</h1><p class="kit-intro">Gold line, finer: engraved shading, a weight for '
            'every line, one gold element for what the series is about. For each series, today\'s tile and three options. '
            'Pick a letter per series (for example "Risk B, Sky Gods A ...") and those go on the library page.</p></div></header>'
            + rows)
    return SM.shell("Series tiles: three drawings each", "Gold line series tiles, three drawing options for each of the 13 series.",
                    body, SM.SPEC_CSS + CSS)


PICK = {name: "B" for name, _ in OPTIONS}
LIB = os.path.join(A.V4, "v2-library.js")
MARK = ("  /* series-art: written by tools/v4_series_options.py */\n", "  /* /series-art */\n")


def install():
    art = {}
    for name, opts in OPTIONS:
        i = "ABC".index(PICK[name])
        g = G("st-%s" % slug(name)[:12])
        opts[i][1](g)
        art[name] = g.svg(name).replace('role="img" aria-label="%s"' % name, 'aria-hidden="true"', 1)
    src = open(LIB, encoding="utf-8").read()
    block = MARK[0] + "  var ART = " + json.dumps(art, separators=(",", ":")) + ";\n" + MARK[1]
    if MARK[0] in src:
        src = src[:src.index(MARK[0])] + block + src[src.index(MARK[1]) + len(MARK[1]):]
    else:
        anchor = "  function emboss(p) {"
        src = src.replace(anchor, block + "\n" + anchor, 1)
    old = 't.querySelector(".shot").innerHTML = slab(t.getAttribute("data-t"), 200, 138);'
    new = 'var k = t.getAttribute("data-t");\n    t.querySelector(".shot").innerHTML = ART[k] || slab(k, 200, 138);'
    src = src.replace(old, new, 1)
    open(LIB, "w", encoding="utf-8").write(src)
    print("v4 series options: %s on the library" % ", ".join("%s %s" % (PICK[n], n) for n, _ in OPTIONS[:2]) + " ...")


def main():
    out = os.path.join(A.V4, "samples", "series-options.html")
    open(out, "w", encoding="utf-8").write(page())
    print("v4 series options: samples/series-options.html")
    install()


if __name__ == "__main__":
    main()
