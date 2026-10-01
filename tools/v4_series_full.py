#!/usr/bin/env python3
"""
Looks 3 (gold line) and 4 (colour field) on the whole library page (owner,
1 Oct 2026: "show me 3 & 4 in full page config"). All 13 series tiles drawn
in each look, placed on a copy of library.html:

    prototypes/v4/samples/library-gold.html
    prototypes/v4/samples/library-colour.html

The four from the first sample keep their drawings (tools/v4_series_icons2.py);
the other nine are drawn here from the idea of each series' knowledge base
drawing. library.js still draws its stone slabs first; a short script after it
puts these in their place, so everything else on the page works as it does.

    python3 tools/v4_series_full.py
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_samples as SM  # noqa: E402
import v4_series_icons2 as A  # noqa: E402
from v4_computed import naca  # noqa: E402

f, path, smooth = A.f, A.path, A.smooth
ROOT = A.ROOT
V4 = A.V4
CATS = {"Risk vs Reward": "Competitions", "Know Your Equipment": "Technical", "Sky Gods": "Core series",
        "Navigators": "Core series", "Living the Dream": "Core series", "World Cups": "Competitions",
        "Resources, Tools and Tips": "Competitions", "Weather Patterns": "Meteorology", "Brand Stories": "Industry",
        "Storytellers": "Industry", "The Dark Side": "Industry", "Flight Mechanics": "Technical",
        "New Technologies": "Technical"}
A.CAT["Industry"] = ("#a07bff", "#3d2a8f")


# ---------------------------------------------------------------- the nine other ideas, as drawing parts
# each part: ("line", d, width, opacity) | ("accent", d, width) | ("fill", d, opacity) | ("dot", x, y, r) | ("flow", d)
def kye():
    O, R = (78, 46), 44
    dome = [(O[0] + R * math.cos(t), O[1] - 26 * math.sin(t)) for t in [math.pi * k / 30 for k in range(31)]]
    p = (70, 108)
    parts = [("fill", path(dome, True), .2), ("line", path(dome, True), 1.3, 1)]
    for k in range(0, 31, 5):
        parts.append(("line", path([dome[k], p]), .7, .45))
    parts += [("dot", p[0], p[1] + 4, 3.2, False)]
    V, L = (136, 44), 48
    parts += [("line", path([V, (V[0], V[1] + L)]), 1.2, .8), ("line", path([V, (V[0] + L, V[1])]), 1.2, .8),
              ("accent", path([V, (V[0] + L, V[1] + L)]), 1.8), ("flow", path([V, (V[0] + L, V[1] + L)]))]
    return parts


def navigators():
    cx, cy, rx, ry = 100, 66, 74, 44
    ell = lambda a, b: [(cx + a * math.cos(t), cy + b * math.sin(t)) for t in [2 * math.pi * k / 60 for k in range(61)]]
    parts = [("line", path(ell(rx, ry)), 1.2, .9)]
    for fr in (.33, .66):
        parts.append(("line", path(ell(rx * fr, ry)), .7, .35))
    for y in (-.5, 0, .5):
        w = rx * math.sqrt(1 - y * y)
        parts.append(("line", path([(cx - w, cy + y * ry), (cx + w, cy + y * ry)]), .7, .35))
    pins = [(52, 70), (112, 74), (140, 48), (138, 58), (166, 92)]          # Colombia, Kenya, Bir, Panchgani, Manilla (schematic)
    parts += [("accent", path([pins[0], (80, 52), pins[1], pins[2]]), 1.2)]
    parts += [("dot", x, y, 2.6, True) for x, y in pins]
    return parts


def living():
    arc = [(x, 100 - 26 * math.sin(math.pi * (x - 10) / 180)) for x in range(10, 191, 6)]
    route = [(24, 88), (52, 70), (80, 60), (104, 66), (128, 52), (156, 58), (178, 44)]
    parts = [("fill", path(arc + [(190, 138), (10, 138)], True), .18), ("line", path(arc), 1.2, .9),
             ("accent", smooth(route), 1.8), ("flow", smooth(route))]
    parts += [("dot", x, y, 2.4, True) for x, y in route[1:-1]]
    parts += [("dot", 178, 44, 3.4, False)]
    return parts


def worldcups():
    C, R = (120, 64), 32
    circ = [(C[0] + R * math.cos(t), C[1] + R * math.sin(t)) for t in [2 * math.pi * k / 60 for k in range(61)]]
    parts = [("line", path(circ), 1.2, .9), ("dot", C[0], C[1], 2, False)]
    tag = (C[0] - 6, C[1] - R + 1)
    for k in range(9):
        y0 = 70 + (k - 4) * 9
        pts = [(14, y0), (60, y0 - 14 + k), (tag[0] - 2 + k * .5, tag[1] + k * .4), (184, 96 + (k - 4) * 4)]
        parts.append(("line", smooth(pts), .7, .35))
    lead = [(22, 66), (66, 46), (tag[0] + 4, tag[1] - 2), (186, 84)]
    parts += [("accent", smooth(lead), 1.8), ("flow", smooth(lead))]
    return parts


def resources():
    pts, cyc, x = [], 0.0, 14.0
    while x <= 186:
        per = 30 + (x - 14) * .1
        ph = cyc % 1
        b = math.sin(ph / .35 * math.pi / 2) if ph < .35 else math.cos((ph - .35) / .65 * math.pi / 2)
        amp = 34 * math.exp(-(x - 14) / 130) + 8
        pts.append((x, 92 - amp * b))
        cyc += 1.0 / per
        x += 1.0
    return [("line", path([(14, 92), (186, 92)]), .8, .5), ("accent", path(pts), 1.6), ("flow", path(pts))]


def brand():
    n = 80
    xs = [-1 + 2 * i / (n - 1) for i in range(n)]
    c = [44 * max(0, 1 - x * x) ** .42 for x in xs]
    te = [86 + .4 * ci + 6 * x * x for x, ci in zip(xs, c)]
    le = [t - ci - (2.6 * max(0, math.sin(x * math.pi * 26)) ** .8 if abs(x) <= .6 else 0) for x, ci, t in zip(xs, c, te)]
    X = [100 + 84 * x for x in xs]
    parts = [("fill", path(list(zip(X, le)) + list(zip(X, te))[::-1], True), .18),
             ("line", path(list(zip(X, le)) + list(zip(X, te))[::-1], True), 1.2, 1)]
    for k in range(0, n, 6):
        parts.append(("line", path([(X[k], le[k]), (X[k], te[k])]), .6, .3))
    parts.append(("accent", path([(X[i], le[i]) for i in range(n) if abs(xs[i]) <= .6]), 1.8))
    parts.append(("line", path([(100 - 84 * .6, 30), (100 + 84 * .6, 30)]), .8, .6))
    return parts


def storytellers():
    ridge = lambda y0, a, s: [(x, y0 - a * math.exp(-((x - 60) / 26) ** 2) - a * .8 * math.exp(-((x - 140) / 30) ** 2) - 6 * math.sin(x / s))
                               for x in range(0, 201, 5)]
    far, near = ridge(90, 30, 9), ridge(112, 44, 13)
    track = [(176, 22), (150, 26), (126, 36), (112, 58), (104, 82), (98, 100)]
    return [("fill", path(far + [(200, 138), (0, 138)], True), .12), ("line", path(far), .8, .45),
            ("fill", path(near + [(200, 138), (0, 138)], True), .24), ("line", path(near), 1.2, .9),
            ("line", path([(0, 60), (200, 30)]), .7, .35),
            ("accent", smooth(track), 1.8), ("flow", smooth(track)), ("dot", 176, 22, 3.2, True)]


def darkside():
    y = 60
    parts = [("line", path([(16, y), (70, y)]), 1.2, .9), ("line", path([(76, y + 5), (82, y - 5)]), 1, .8),
             ("line", path([(84, y + 5), (90, y - 5)]), 1, .8), ("line", path([(96, y), (176, y)]), 1.2, .9),
             ("dot", 36, y, 3, False), ("dot", 128, y, 3, False), ("dot", 160, y, 4.2, True),
             ("line", path([(16, 100), (110, 100)]), .8, .5)]
    parts += [("dot", x, 100, 2.2, False) for x in (36, 56, 76)]
    parts += [("accent", path([(84, 100), (140, 100)]), 1.6), ("dot", 146, 100, 2.4, True)]
    return parts


def newtech():
    up, lo = naca(.18, .035, .35, 60)
    x0, y0, c = 40, 46, 120
    U = [(x0 + c * x, y0 - c * y) for x, y in up]
    L = [(x0 + c * x, y0 - c * y) for x, y in lo]
    lp = lambda fr: min(L, key=lambda q: abs((q[0] - x0) / c - fr))
    R = (96, 118)
    aa, bb, old = lp(.30), lp(.62), lp(.10)
    return [("fill", path(U + L[::-1], True), .2), ("line", path(U + L[::-1], True), 1.3, 1),
            ("line", path([old, R]), .7, .4),
            ("accent", path([aa, (R[0] - 3, R[1])]), 1.6), ("accent", path([bb, (R[0] + 3, R[1])]), 1.6),
            ("dot", aa[0], aa[1], 2.6, True), ("dot", bb[0], bb[1], 2.6, True)]


NINE = {"Know Your Equipment": kye, "Navigators": navigators, "Living the Dream": living, "World Cups": worldcups,
        "Resources, Tools and Tips": resources, "Brand Stories": brand, "Storytellers": storytellers,
        "The Dark Side": darkside, "New Technologies": newtech}


def render(parts, base, accent, fillc, glowid=None, fscale=1.0):
    gf = ' filter="url(#%s)"' % glowid if glowid else ""
    o = ""
    for p in parts:
        if p[0] == "fill":
            o += A.F(p[1], fillc, round(p[2] * fscale, 3))
    for p in parts:
        if p[0] == "line":
            o += A.S(p[1], base, p[2], p[3])
    acc = ""
    for p in parts:
        if p[0] == "accent":
            acc += A.S(p[1], accent, p[2])
        elif p[0] == "dot":
            acc += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(p[1]), f(p[2]), f(p[3]), accent if p[4] else base)
    o += "<g%s>%s</g>" % (gf, acc)
    for p in parts:
        if p[0] == "flow":
            o += A.FL(p[1])
    return o


def gold(name):
    if name not in NINE:
        return A.goldline(name)
    k = "gl-" + re.sub(r"\W", "", name.lower())
    defs = ('<linearGradient id="%s-ln" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="200" y2="0"><stop offset="0" stop-color="#f6f4f4"/>'
            '<stop offset="1" stop-color="#ffb35c"/></linearGradient>'
            '<linearGradient id="%s-ac" gradientUnits="userSpaceOnUse" x1="0" y1="138" x2="200" y2="0"><stop offset="0" stop-color="#ff7517"/>'
            '<stop offset="1" stop-color="#ffd27a"/></linearGradient>' % (k, k))
    body = '<rect width="%d" height="%d" fill="#121318"/>' % (A.W, A.H)
    body += '<circle cx="100" cy="69" r="58" fill="none" stroke="#ffffff" stroke-opacity=".05" vector-effect="non-scaling-stroke"/>'
    body += render(NINE[name](), "url(#%s-ln)" % k, "url(#%s-ac)" % k, "#ffb35c", fscale=.25)
    return A.svg(k, name, defs, body)


def colour(name):
    cat = CATS[name]
    if name not in NINE:
        return A.colour(name, cat)
    k = "co-" + re.sub(r"\W", "", name.lower())
    a, b = A.CAT[cat]
    defs = ('<linearGradient id="%s-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient>'
            '<radialGradient id="%s-hi" cx="78%%" cy="18%%" r="70%%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>' % (k, a, b, k)) + A.glow(k + "-gl", 1.4)
    body = '<rect width="%d" height="%d" fill="url(#%s-bg)"/><rect width="%d" height="%d" fill="url(#%s-hi)"/>' % (A.W, A.H, k, A.W, A.H, k)
    body += render(NINE[name](), "#fff", "#fff", "#000", k + "-gl")
    return A.svg(k, name, defs, body)


SWAP = """<script>
/* sample only: the series tiles in this look, in place of the stone slabs library.js drew */
(function () {
  var art = %s;
  document.querySelectorAll('.v2-tiles .tile').forEach(function (t) {
    var s = art[t.getAttribute('data-t')];
    if (s) t.querySelector('.shot').innerHTML = s;
  });
})();
</script>
"""
CSS = """<style>
/* sample: tiles as cards with the drawing filling them */
.v2-tiles .tile .shot{border-radius:10px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.35);transition:transform .4s ease,box-shadow .4s ease;background:none;}
.v2-tiles .tile:hover .shot{transform:translateY(-4px);box-shadow:0 16px 40px rgba(0,0,0,.5);}
.v2-tiles .tile .shot svg{display:block;width:100%;height:100%;}
.v2-tiles .tile .shot::before,.v2-tiles .tile .shot::after{display:none;}
@media (prefers-reduced-motion:reduce){.v2-tiles .tile .shot{transition:none;}}
.v4s-banner{position:relative;z-index:5;background:#ff7517;color:#141519;font-weight:600;text-align:center;padding:.5rem 1rem;font-size:.85rem;}
.v4s-banner a{color:#141519;text-decoration:underline;}
</style>
"""


def build(look, fn, label):
    src = open(os.path.join(V4, "library.html"), encoding="utf-8").read()
    art = {n: fn(n) for n in CATS}
    src = re.sub(r"<title>(.*?)</title>", lambda m: "<title>%s (sample: %s)</title>" % (m.group(1), label), src, 1, flags=re.S)
    src = src.replace("</head>", CSS + "</head>", 1)
    src = re.sub(r'(<body[^>]*>)', r'\1<div class="v4s-banner">Sample, not live: the library with the series tiles in the "%s" look. '
                 r'<a href="series-icons-2.html">All four looks</a></div>' % label, src, 1)
    i = src.index('v2-library.js')
    j = src.index("</script>", i) + len("</script>")
    src = src[:j] + "\n" + SWAP % json.dumps(art) + src[j:]
    src = SM.deeper(src).replace('href="../series-icons-2.html"', 'href="series-icons-2.html"')
    out = os.path.join(V4, "samples", "library-%s.html" % look)
    open(out, "w", encoding="utf-8").write(src)
    print("v4 series full: samples/library-%s.html" % look)


def main():
    build("gold", gold, "Gold line")
    build("colour", colour, "Colour field")


if __name__ == "__main__":
    main()
