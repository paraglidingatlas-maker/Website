#!/usr/bin/env python3
"""
The painted lens (tools/v4_lens.py): the knowledge base's scenes composed as
pictures. Ridges stand in layers that pale with distance (aerial
perspective), one light falls across each scene, and orange is kept for the
one thing the scene is about. The facts, labels and geometry are those of the
drawing each replaces (tools/kbfig/*.py); nothing is added but light.

  heroes   kb-sky-gods (the record climb), kb-risk-vs-reward (the decision)
  sides    kb-sky-gods-section (the lee), kb-storytellers-section (the dusk),
           kb-weather-patterns-section (the Keepit blue hole),
           kb-navigators-section (a launch for every wind)
  band     kb-navigators-cauca (the Cauca Valley), with a phone version

One computed drawing sits here too, since it is a hero: the weather-patterns
sounding, drawn over dry adiabats worked out at 9.8 degrees per 1,000 m.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402
from v4_computed import P, rect  # noqa: E402
from v4_phone import lines  # noqa: E402

f = K.f
BG = "#141519"


def defs(d, s):
    d.defs_extra = getattr(d, "defs_extra", "") + s


def vgrad(d, ident, stops, x1=0, y1=0, x2=0, y2=1):
    defs(d, '<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>' % (
        ident, x1, y1, x2, y2, "".join('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>' % s for s in stops)))


def rgrad(d, ident, cx, cy, r, color, op, mid=.4):
    defs(d, '<radialGradient id="%s" gradientUnits="userSpaceOnUse" cx="%s" cy="%s" r="%s">'
            '<stop offset="0" stop-color="%s" stop-opacity="%s"/><stop offset="%s" stop-color="%s" stop-opacity="%s"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (
                ident, f(cx), f(cy), f(r), color, op, mid, color, op * .35, color))
    return 'url(#%s)' % ident


def fill_path(d, pts, fill, extra=""):
    d.raw('<path d="M%s Z" fill="%s"%s/>' % (" L".join("%s,%s" % (f(x), f(y)) for x, y in pts), fill, extra))


def stroke_path(d, pts, color, width, op, dash=None):
    d.raw('<path d="M%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="%s" stroke-linejoin="round" '
          'stroke-linecap="round" vector-effect="non-scaling-stroke"%s/>' % (
              " L".join("%s,%s" % (f(x), f(y)) for x, y in pts), color, op, width,
              ' stroke-dasharray="%s"' % dash if dash else ""))


def glow(d, ident, cx, cy, r, color="#ff7517", op=.18):
    d.raw('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), rgrad(d, ident, cx, cy, r, color, op)))


def noise(seed):
    """A small deterministic 1D value noise, for ridgelines."""
    import random
    rnd = random.Random(seed)
    knots = [rnd.uniform(-1, 1) for _ in range(400)]

    def n(x):
        i = int(math.floor(x)) % 399
        t = x - math.floor(x)
        t = t * t * (3 - 2 * t)
        return knots[i] * (1 - t) + knots[i + 1] * t
    return lambda x: n(x) * .6 + n(x * 2.3 + 17) * .3 + n(x * 5.1 + 41) * .1


def ridge_layer(d, ident, xs, ys, bottom, top_col, bot_col, op_top, op_bot, rim=None):
    """A silhouette filled with a vertical gradient (lit at the top), optionally rim-lit along its crest."""
    vgrad(d, ident, [(0, top_col, op_top), (1, bot_col, op_bot)])
    fill_path(d, list(zip(xs, ys)) + [(xs[-1], bottom), (xs[0], bottom)], "url(#%s)" % ident)
    if rim:
        stroke_path(d, list(zip(xs, ys)), rim[0], rim[1], rim[2])


# ---------------------------------------------------------------- sky gods hero: the record climb
SG_DESC = ("How the highest flights are made: a range of big mountains, generic rather than a named peak, an altitude scale, "
           "and one climb: circling in thermals to 7,600 m, then straight up in wave to 8,400 m, as Antoine Girard "
           "describes his record flight. Painted: ranges paling with distance, a low sun behind the climb.")


def sky_hero():
    W, H = 1600, 600
    s = W / 2400
    d = K.Drawing(W, H, "pt-sg", "The record climb: thermals, then wave", SG_DESC, inline_css=False)
    Y = lambda m: (840 - (m - 2000) / 7000 * 720) * s
    glow(d, "pt-sg-sun", 1180, 120, 420, "#ff7517", .16)
    # three ranges, far to near
    for k, (seed, base, amp, top, bot, opt, opb, rim) in enumerate((
            (7, 6600, 700, "#8d8d8d", BG, .2, 0, ("#c9ccd3", .8, .2)),
            (3, 5700, 900, "#50525c", BG, .45, .1, ("#e9e7e7", .9, .3)),
            (11, 3300, 1100, "#2a2b33", "#141519", .97, 1, ("#f6f4f4", 1.2, .55)))):
        n = noise(seed)
        xs = [640 + i * 4 for i in range(241)]
        peaks = [(1180, 4800, 90), (1400, 6100, 110), (1880, 6900, 120), (2160, 6000, 120), (2300, 4300, 100)]
        ys = []
        for x in xs:
            X = x / s
            h = 2000 + min(1, max(0, (X - 960) / 300)) * 1800
            if k == 2:
                for c, t, w in peaks:
                    h = max(h, t - (abs(X - c) / w) ** 1.15 * 900)
            else:
                h = base + amp * n(X / 420 + k * 3)
            ys.append(Y(h) + (k == 2) * 0)
        ridge_layer(d, "pt-sg-r%d" % k, xs, ys, H, top, bot, opt, opb, rim)
    # snow light on the near range: short strokes down the sunlit faces
    # altitude scale
    for m in (2000, 5000, 7600, 8000, 8400):
        acc = m in (7600, 8400)
        d.line((1553, Y(m)), (1580, Y(m)), "accent" if acc else "hair")
        d.text((1546, Y(m) + 4), "{:,} m".format(m), "val" if m == 8400 else ("tb" if not acc else "val"), "end")
    d.line((1580, Y(2000)), (1580, Y(8600)), "hair")
    # the climb
    cx = 1630 * s
    pts = []
    for i in range(900):
        t = i / 899
        a = 5000 + t * 2600
        pts.append((cx + 40 * math.sin(t * 2 * math.pi * 11) * (1 - .3 * t), Y(a)))
    stroke_path(d, pts, "#f6f4f4", 1.1, .8)
    d.path("M%s,%s L%s,%s" % (f(cx - 80), f(Y(7600)), f(cx + 280), f(Y(7600))), "accent", extra=' style="stroke-dasharray:6 6;stroke-opacity:.6"')
    glow(d, "pt-sg-wave", cx + 14, Y(8000), 60, "#ff7517", .35)
    d.line((cx, Y(7600)), (cx + 27, Y(8400) + 8), "accent")
    d.head((cx + 27, Y(8400)), (27, Y(8400) - Y(7600)), 10, True)
    d.text((cx - 60, Y(6200)), "thermals", "tv", "end")
    d.text((cx + 46, Y(8150)), "wave", "val")
    d.text((cx + 280, Y(7600) + 16), "where the thermals stopped", "val", "end")
    return d


# ---------------------------------------------------------------- risk vs reward hero: the decision
RVR_DESC = ("A valley in section. Launch on the left; one line climbs first and crosses high, keeping landing options; the "
            "other goes straight across, low, over a gorge where a collapse has nowhere to go. A small marker where they "
            "diverge: the decision. Painted: the gorge lit from inside in orange, the landable fields catching the light.")


def rvr_hero():
    W, H = 1600, 600
    s = W / 2400
    d = K.Drawing(W, H, "pt-rvr", "The decision: climb first, or straight across", RVR_DESC, inline_css=False)

    def ground(x):
        y = 640
        y -= 210 * math.exp(-((x - 1060) / 110) ** 2)
        y += 120 * max(0, math.sin((x - 1380) / 95)) ** 3 * math.exp(-((x - 1560) / 160) ** 2)
        y -= 60 * math.exp(-((x - 1860) / 70) ** 2)
        y -= 320 * math.exp(-((x - 2360) / 150) ** 2)
        return y
    G = lambda X: ground(X) * s
    glow(d, "pt-rvr-sky", 1450 * s, 180 * s, 700 * s, "#ff7517", .09)
    # far ranges behind, pale
    for k, (seed, lvl, op) in enumerate(((5, 420, .16), (9, 480, .3))):
        n = noise(seed)
        xs = [660 + i * 5 for i in range(189)]
        ys = [(lvl - 40 + 60 * n(x / 320 + k)) * s for x in [x_ / s for x_ in xs]]
        ridge_layer(d, "pt-rvr-f%d" % k, xs, ys, H, "#737373", BG, op * .7, 0, ("#c9ccd3", .8, op * .7))
    xs = [1000 * s + i * 2 for i in range(int((2400 - 1000) * s / 2) + 1)]
    gs = [G(x / s) for x in xs]
    vgrad(d, "pt-rvr-g", [(0, "#2a2b33", 1), (1, BG, 1)])
    fill_path(d, list(zip(xs, gs)) + [(xs[-1], H), (xs[0], H)], "url(#pt-rvr-g)")
    # the gorge, lit from inside
    gx = [x for x in xs if 1390 * s <= x <= 1730 * s]
    glow(d, "pt-rvr-gorge", 1560 * s, G(1560) - 10, 120, "#ff7517", .35)
    stroke_path(d, list(zip(gx, [G(x / s) for x in gx])), "#ff7517", 1.4, .8)
    stroke_path(d, list(zip(xs, gs)), "#e9e7e7", 1.2, .7)
    # landable fields catching the light
    for x0, x1 in ((1180, 1330), (1740, 1840), (1960, 2120)):
        yy = G((x0 + x1) / 2)
        stroke_path(d, [(x0 * s, yy + 1), (x1 * s, yy + 1)], "#f6f4f4", 2.2, .75)
        d.text(((x0 + x1) / 2 * s, yy + 30), "landable", "sub", "middle")
    d.text((1560 * s, G(1560) + 58), "no landing", "val", "middle")
    lx, ly = 1060 * s, G(1060) - 4
    d.dot((lx, ly), 3.5, False)

    def bez(p0, p1, p2, p3, n=120):
        out = []
        for i in range(n + 1):
            t = i / n
            out.append(tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * e
                             for a, b, c, e in zip(p0, p1, p2, p3)))
        return out
    helix = []
    for i in range(301):
        th = i / 300 * 8 * math.pi
        helix.append(((1140 + th * 6 + 30 * math.sin(th)) * s, (ground(1060) - 30 - th * 11 + 9 * math.cos(th)) * s))
    stroke_path(d, [(lx, ly)] + helix, "#c9ccd3", 1.1, .8)
    top = helix[-1]
    safe = bez(top, (1500 * s, top[1] - 7), (1900 * s, G(1900) - 173), (2300 * s, G(2300) - 9))
    fast = bez((lx, ly), (1350 * s, ly + 27), (1650 * s, G(1650) - 100), (1790 * s, G(1790) - 47))
    stroke_path(d, safe, "#e9e7e7", 1.6, .9)
    d.head(safe[-1], (safe[-1][0] - safe[-4][0], safe[-1][1] - safe[-4][1]), 9)
    stroke_path(d, fast, "#ff7517", 2, 1)
    d.head(fast[-1], (fast[-1][0] - fast[-4][0], fast[-1][1] - fast[-4][1]), 10, True)
    D = (lx + 17, ly - 12)
    d.dot(D, 4.5, True)
    d.circle(D, 11, "accent")
    d.text((top[0] + 26, top[1] - 4), "climb first, cross high", "tv")
    d.text((fast[50][0] + 4, fast[50][1] + 26), "straight across, low", "val")
    d.text((D[0] + 16, D[1] - 6), "the decision", "lab")
    d.text((2300 * s, G(2300) - 26), "goal", "lab", "middle")
    return d


# ---------------------------------------------------------------- sky gods side: the lee
SGS_DESC = ("Turning back, after Honorin Hamard calling off a record attempt. A ridge with the wind coming over it, the rough "
            "air in its lee, a pilot's track arriving downwind of it, three frontal collapses marked, and the track "
            "turning away to land. Schematic.")


def sky_section():
    W, H = 1600, 667
    s = W / 2400
    d = K.Drawing(W, H, "pt-sgs", "Turning back in the lee", SGS_DESC, inline_css=False)
    glow(d, "pt-sgs-l", 1000 * s, 260 * s, 600 * s, "#8d8d8d", .12)
    n = noise(21)
    xs = [600 + i * 4 for i in range(251)]
    far = [(600 + 50 * n(x / 330)) * s for x in [x_ / s for x_ in xs]]
    ridge_layer(d, "pt-sgs-f", xs, far, H, "#737373", BG, .22, 0, ("#c9ccd3", .8, .2))
    g = [(880 - 430 * math.exp(-((X - 1500) / 260) ** 2) - 180 * math.exp(-((X - 2150) / 300) ** 2)) * s for X in [x / s for x in xs]]
    vgrad(d, "pt-sgs-g", [(0, "#2a2b33", 1), (1, BG, 1)])
    fill_path(d, list(zip(xs, g)) + [(xs[-1], H), (xs[0], H)], "url(#pt-sgs-g)")
    # the windward face lit, the lee in shadow
    wind_face = [(x, y) for x, y in zip(xs, g) if x <= 1500 * s]
    stroke_path(d, wind_face, "#e9e7e7", 1.4, .7)
    stroke_path(d, [(x, y) for x, y in zip(xs, g) if x > 1500 * s], "#8d8d8d", 1, .45)
    for yy in (240, 300, 360):
        d.arrow((960 * s, yy * s), (1380 * s, (yy + 40) * s), "detail", 8)
    d.text((960 * s, 215 * s), "wind", "sub")
    # the rotor: painted as a dim, churning bruise in the lee
    glow(d, "pt-sgs-rot", 1760 * s, 560 * s, 170 * s, "#8d8d8d", .22)
    for r, op in ((70, .5), (110, .35), (150, .22)):
        pts = [(1760 * s + r * s * math.cos(t), 560 * s + .6 * r * s * math.sin(t)) for t in [1.7 * math.pi * k / 60 for k in range(61)]]
        stroke_path(d, pts, "#c9ccd3", 1, op)
    d.text((1700 * s, 790 * s), "rough air downwind of the ridge", "sub", "middle")
    trk = [(2300, 250), (2080, 330), (1900, 430), (1790, 500)]
    stroke_path(d, [(x * s, y * s) for x, y in trk], "#e9e7e7", 1.4, .85)
    for k, (px, py) in enumerate(((2020, 360), (1930, 410), (1840, 470))):
        d.circle((px * s, py * s), 9, "accent")
        d.text((px * s + 12, py * s - 12), str(k + 1), "vn")
    back = [(1790, 500), (1860, 560), (1990, 610), (2120, 660), (2230, 700)]
    glow(d, "pt-sgs-b", 2230 * s, 700 * s, 90, "#ff7517", .3)
    stroke_path(d, [(x * s, y * s) for x, y in back], "#ff7517", 2, 1)
    d.head((2230 * s, 700 * s), (110, 40), 10, True)
    d.text((2230 * s, 740 * s), "turn away, land,", "val", "end")
    d.text((2230 * s, 758 * s), "try another day", "val", "end")
    d.text((2060 * s, 290 * s), "three frontals", "val")
    d.text((2380 * s, 985 * s), "schematic", "tb", "end")
    return d


# ---------------------------------------------------------------- storytellers side: caught by the dusk
STS_DESC = ("Caught by the dusk, after Eddie Colfox's 2001 flight in Hunza. A section through deep Karakoram valleys late in "
            "the day: the pilot still high in sunlight, the valleys below already in shadow, the known landing beach by the "
            "river out of reach, and the narrow strip above a gully where he had to land: a four-metre strip, by a stone "
            "wall. Schematic.")


def story_section():
    W, H = 1600, 667
    s = W / 2400
    d = K.Drawing(W, H, "pt-sts", "Caught by the dusk", STS_DESC, inline_css=False)
    # the sky: warm and bright high, falling to dark
    vgrad(d, "pt-sts-sky", [(0, "#ff7517", .16), (.45, "#ff7517", .05), (1, BG, 0)])
    d.raw('<rect x="%s" y="0" width="%s" height="%s" fill="url(#pt-sts-sky)"/>' % (f(560), f(W - 560), f(H)))
    glow(d, "pt-sts-sun", 620, 90, 380, "#ff7517", .22)
    xs = [600 + i * 4 for i in range(251)]
    X = [x / s for x in xs]
    for k, (seed, lvl, amp, op) in enumerate(((13, 330, 90, .22), (17, 430, 110, .4))):
        n = noise(seed)
        ys = [(lvl + amp * n(x / 110 + k)) * s for x in X]
        ridge_layer(d, "pt-sts-f%d" % k, xs, ys, H, "#737373", BG, op, 0, ("#ff7517", .8, .25 + .15 * k))
    g = [(930 - 620 * math.exp(-((x - 1180) / 150) ** 2) - 520 * math.exp(-((x - 1850) / 170) ** 2)
          - 430 * math.exp(-((x - 2330) / 160) ** 2) - 40 * math.sin(x / 37)) * s for x in X]
    vgrad(d, "pt-sts-g", [(0, "#2a2b33", 1), (1, "#0e0f12", 1)])
    fill_path(d, list(zip(xs, g)) + [(xs[-1], H), (xs[0], H)], "url(#pt-sts-g)")
    # the shadow line: above it the peaks catch the last sun, below it the valleys go dark
    shade = [(x, (360 + (xx - 900) * .12) * s) for x, xx in zip(xs, X)]
    vgrad(d, "pt-sts-sh", [(0, "#000", 0), (.2, "#000", .35), (1, "#000", .55)])
    fill_path(d, shade + [(xs[-1], H), (xs[0], H)], "url(#pt-sts-sh)")
    lit = [(x, y) for x, y, (_, sy) in zip(xs, g, shade) if y < sy]
    run = []
    for x, y, (_, sy) in zip(xs, g, shade):
        if y < sy:
            run.append((x, y))
        elif run:
            stroke_path(d, run, "#ff7517", 1.6, .7)
            run = []
    if run:
        stroke_path(d, run, "#ff7517", 1.6, .7)
    stroke_path(d, shade, "#ff7517", 1, .25, "6 6")
    d.text((930 * s, 120 * s), "low sun", "val")
    for k in range(4):
        d.arrow((930 * s, (150 + k * 45) * s), (1080 * s, (168 + k * 45) * s), "accent", 7)
    d.text((2380 * s, 330 * s), "still sunlit up high", "sub", "end")
    d.text((2380 * s, 700 * s), "valleys already in shadow", "sub", "end")
    Gi = lambda xx: (930 - 620 * math.exp(-((xx - 1180) / 150) ** 2) - 520 * math.exp(-((xx - 1850) / 170) ** 2)
                     - 430 * math.exp(-((xx - 2330) / 160) ** 2) - 40 * math.sin(xx / 37)) * s
    lx, ly = 1615, Gi(1615) - 4
    tr = [(2200, 230), (2020, 245), (1860, 300), (1760, 420), (1700, 560), (1650, 700)]
    glow(d, "pt-sts-p", 2200 * s, 230 * s, 70, "#ff7517", .4)
    stroke_path(d, [(x * s, y * s) for x, y in tr] + [(lx * s, ly)], "#ff7517", 2.2, 1)
    d.dot((2200 * s, 230 * s), 5, True)
    bx = 1515
    stroke_path(d, [((bx - 45) * s, Gi(bx) - 2), ((bx + 45) * s, Gi(bx) - 2)], "#f6f4f4", 2.4, .5)
    d.text((bx * s - 14, Gi(bx) + 28), "known landing: a beach by the river", "sub", "middle")
    d.circle((lx * s, ly), 7, "accent")
    d.line((lx * s + 9, ly - 3), (1760 * s, 800 * s - 4), "hair")
    d.text((1770 * s, 800 * s), "landed short, on a four-metre strip", "lab")
    d.text((1770 * s, 800 * s + 16), "above a gully, by a stone wall", "sub")
    d.text((2380 * s, 985 * s), "schematic", "tb", "end")
    return d


# ---------------------------------------------------------------- weather patterns side: the Keepit blue hole
WPS_DESC = ("The Keepit blue hole: a plan of the valley in front of Manilla's launch on Mount Borah, with Lake Keepit to the "
            "southwest. When the wind blows off the lake, from about one o'clock it spills cool air across the valley and "
            "breaks up the thermals. Only the places named in the conversation are labelled. Schematic.")


def wp_section():
    W, H = 1600, 667
    s = W / 2400
    d = K.Drawing(W, H, "pt-wps", "The Keepit blue hole", WPS_DESC, inline_css=False)
    glow(d, "pt-wps-sun", 2000 * s, 420 * s, 520 * s, "#ff7517", .12)
    for k, op in enumerate((.35, .25, .18)):
        pts = [((xx) * s, (260 + k * 45 - 60 * math.sin((xx - 1500) / 170) - (xx - 1500) * .12) * s) for xx in range(1500, 2351, 10)]
        stroke_path(d, pts, "#c9ccd3", 1, op)
    # the lake, deep and cool
    lake = [((1180 + 150 * math.cos(t) + 25 * math.sin(3 * t)) * s, (780 + 80 * math.sin(t) + 18 * math.cos(4 * t)) * s)
            for t in [2 * math.pi * k / 120 for k in range(120)]]
    defs(d, '<radialGradient id="pt-wps-lk" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#3d4a5a"/><stop offset="1" stop-color="#1e252e"/></radialGradient>')
    fill_path(d, lake, "url(#pt-wps-lk)")
    stroke_path(d, lake + [lake[0]], "#c9ccd3", 1, .5)
    d.text((1180 * s, 785 * s + 4), "Lake Keepit", "lab", "middle")
    for k in range(4):
        d.arrow(((1010 + k * 30) * s, (930 - k * 40) * s), ((1100 + k * 30) * s, (860 - k * 40) * s), "detail", 7)
    d.text((960 * s, 960 * s), "wind off the lake", "sub")
    # the cool tongue: a pale, cold wash spreading across the valley
    tongue = [(1300, 740), (1480, 640), (1700, 560), (1880, 560), (1960, 620), (1850, 700), (1640, 760), (1420, 820)]
    defs(d, '<radialGradient id="pt-wps-t" gradientUnits="userSpaceOnUse" cx="%s" cy="%s" r="%s"><stop offset="0" stop-color="#9fb4c8" stop-opacity=".22"/>'
            '<stop offset="1" stop-color="#9fb4c8" stop-opacity=".04"/></radialGradient>' % (f(1650 * s), f(660 * s), f(380 * s)))
    d.path(K.catmull([(x * s, y * s) for x, y in tongue], closed=True), "ghost")
    d.raw('<path d="%s" fill="url(#pt-wps-t)"/>' % K.catmull([(x * s, y * s) for x, y in tongue], closed=True))
    for k in range(3):
        d.arrow(((1420 + k * 130) * s, (740 - k * 45) * s), ((1500 + k * 130) * s, (700 - k * 45) * s), "hair", 7)
    for x, y in ((1640, 660), (1780, 620), (1540, 720)):
        d.path(K.catmull([(x * s + 11 * math.cos(t), y * s + 11 * math.sin(t)) for t in [2 * math.pi * k / 8 for k in range(8)]], True), "ghost")
    for x, y in ((2100, 520), (2200, 700), (1420, 480)):
        glow(d, "pt-wps-th%d" % x, x * s, (y - 20) * s, 34, "#ff7517", .3)
        d.circle((x * s, y * s), 11, "accent")
        d.arrow((x * s, (y - 18) * s), (x * s, (y - 70) * s), "accent", 8)
    d.dot((1760 * s, 820 * s), 4.5, False)
    d.text((1776 * s, 820 * s + 4), "Manilla", "lab")
    d.raw('<path class="fa" d="M%s,%s L%s,%s L%s,%s Z"/>' % (f(1880 * s), f(380 * s), f(1900 * s), f(350 * s), f(1920 * s), f(380 * s)))
    d.text((1935 * s, 368 * s + 4), "Mount Borah launch", "lab")
    d.text((1720 * s, 520 * s), "the Keepit blue hole", "lab", "middle")
    d.text((1720 * s, 544 * s), "cool air, broken thermals from about 1 pm", "sub", "middle")
    d.arrow((2300 * s, 950 * s), (2300 * s, 880 * s), "detail", 8)
    d.text((2300 * s, 862 * s), "N", "sub", "middle")
    d.text((2380 * s, 985 * s), "schematic", "tb", "end")
    return d


# ---------------------------------------------------------------- navigators side: a launch for every wind
NVS_DESC = ("An isolated plateau with a launch on each of its four sides, one for every wind direction, drawn as contours, "
            "with the flat country all round and a climb lifting off near the landing paddock rather than on the face of "
            "the hill. After Godfrey Wenness on Mount Borah. Schematic.")


def nav_section():
    W, H = 1600, 667
    s = W / 2400
    d = K.Drawing(W, H, "pt-nvs", "A launch for every wind", NVS_DESC, inline_css=False)
    C = (1600 * s, 500 * s)

    def shape(r, k):
        pts = []
        for i in range(120):
            th = 2 * math.pi * i / 120
            rr = r * (1 + .10 * math.sin(3 * th + .6) + .06 * math.cos(5 * th + 1.1) + .03 * math.sin(9 * th + k))
            pts.append((C[0] + 1.25 * rr * s * math.cos(th), C[1] + .95 * rr * s * math.sin(th)))
        return pts
    # hill shading: each contour band a step lighter towards the top, lit from the north-west
    rings = [330, 285, 240, 200, 165, 135]
    for i, r in enumerate(rings):
        tone = 26 + i * 6
        fill_path(d, shape(r, i * .3), "#%02x%02x%02x" % (tone, tone + 1, tone + 7))
    glow(d, "pt-nvs-lit", C[0] - 60, C[1] - 60, 180, "#f6f4f4", .08)
    for i, r in enumerate(rings):
        stroke_path(d, shape(r, i * .3) + [shape(r, i * .3)[0]], "#c9ccd3", 1 if i == 5 else .8, .5 if i == 5 else .3 - .03 * i)
    d.text(C, "plateau", "sub", "middle")
    for ang, lab in ((-math.pi / 2, "north launch"), (0, "east launch"), (math.pi / 2, "south launch"), (math.pi, "west launch")):
        dx, dy = math.cos(ang), math.sin(ang)
        p = (C[0] + dx * 1.25 * 150 * s, C[1] + dy * .95 * 150 * s)
        q = (p[0] + dx * 100, p[1] + dy * 80)
        d.dot(p, 5, True)
        d.arrow((p[0] + dx * 9, p[1] + dy * 9), q, "accent", 9)
        anc = "middle" if abs(dx) < .1 else ("start" if dx > 0 else "end")
        d.text((q[0] + dx * 10, q[1] + dy * 18 + (4 if abs(dx) > .1 else 0)), lab, "lab", anc)
    LP = (2060 * s, 880 * s)
    d.path("M%s,%s h80 v35 h-80 Z" % (f(LP[0] - 40), f(LP[1] - 17)), "detail")
    d.text((LP[0] - 52, LP[1] + 4), "landing paddock", "sub", "end")
    glow(d, "pt-nvs-c", LP[0] + 20, LP[1] - 110, 110, "#ff7517", .22)
    for k in range(5):
        d.raw('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#ff7517" stroke-opacity="%s" vector-effect="non-scaling-stroke"/>' % (
            f(LP[0] + 20), f(LP[1] - 47 - k * 25), f((16 + k * 7) * s), .55 - .08 * k))
    d.text((LP[0] + 20, LP[1] - 200), "the climb is often out here,", "val", "middle")
    d.text((LP[0] + 20, LP[1] - 184), "not on the face of the hill", "val", "middle")
    d.text((2380 * s, 975 * s), "schematic", "tb", "end")
    return d


# ---------------------------------------------------------------- navigators band: the Cauca Valley
CAUCA_DESC = ("Colombia's Cauca Valley in one schematic section, after Pal Takats. Left, the western Cordillera with "
              "Roldanillo's east-facing launch, flying from about 9 am, and high-voltage lines along the foot of the range; "
              "right, the central Cordillera with Piedechinche's west-facing launch, thermals from about 10 or 11. The "
              "Pacific breeze arrives over the western range from late morning: a gusty backwind at Roldanillo, a headwind "
              "at Piedechinche, where you can fly on into the evening. The two sites are about 100 km apart; they share one "
              "section here.")


def cauca_ground(x):
    ridge = lambda c, w, h: h * math.exp(-((x - c) / w) ** 2)
    return 600 - ridge(300, 330, 360) - ridge(2140, 360, 330) - 12 * math.sin(x / 37) * math.exp(-((x - 1220) / 500) ** 2)


def cauca_scene(d, W, H, s, oy=0):
    """The valley painted: the Pacific side in morning light, far ranges paling, the valley floor in haze."""
    glow(d, "%s-sun" % d.id, 120 * s, 90 * s + oy, 520 * s, "#ff7517", .14)
    xs = [i * 4 * s * 2400 / 2400 for i in range(int(2400 / 4) + 1)]
    X = [x / s for x in xs]
    n = noise(31)
    far = [(440 + 45 * n(x / 380)) * s + oy for x in X]
    ridge_layer(d, "%s-far" % d.id, xs, far, H, "#737373", BG, .18, 0, ("#c9ccd3", .8, .18))
    g = [cauca_ground(x) * s + oy for x in X]
    vgrad(d, "%s-g" % d.id, [(0, "#2a2b33", 1), (1, BG, 1)])
    fill_path(d, list(zip(xs, g)) + [(xs[-1], H), (xs[0], H)], "url(#%s-g)" % d.id)
    defs(d, '<radialGradient id="%s-haze" gradientUnits="userSpaceOnUse" cx="%s" cy="%s" r="%s" gradientTransform="translate(0 %s) scale(1 .25) translate(0 -%s)">'
            '<stop offset="0" stop-color="#c9ccd3" stop-opacity=".09"/><stop offset="1" stop-color="#c9ccd3" stop-opacity="0"/></radialGradient>' % (
                d.id, f(1220 * s), f(560 * s + oy), f(560 * s), f(560 * s + oy), f(560 * s + oy)))
    d.raw('<rect x="0" y="%s" width="%s" height="%s" fill="url(#%s-haze)"/>' % (f(400 * s + oy), f(2400 * s), f(260 * s), d.id))
    # the western range lit from the Pacific side, the central range from the valley
    stroke_path(d, [(x, y) for x, y, xx in zip(xs, g, X) if xx < 560], "#e9e7e7", 1.4, .75)
    stroke_path(d, [(x, y) for x, y, xx in zip(xs, g, X) if 560 <= xx < 1860], "#8d8d8d", 1, .5)
    stroke_path(d, [(x, y) for x, y, xx in zip(xs, g, X) if xx >= 1860], "#e9e7e7", 1.2, .6)
    G = lambda xx: cauca_ground(xx) * s + oy
    for px in (560, 1860):
        y = G(px)
        d.raw('<path class="fa" d="M%s,%s L%s,%s L%s,%s Z"/>' % (f(px * s - 6), f(y - 1), f(px * s + 6), f(y - 1), f(px * s), f(y - 13)))
    for px in (700, 760):
        y = G(px)
        d.line((px * s, y), (px * s, y - 41 * s * 1.5), "detail")
        d.line((px * s - 8 * s * 1.5, y - 37 * s * 1.5), (px * s + 8 * s * 1.5, y - 37 * s * 1.5), "detail")
    wire = [(xx * s, G(xx) - 33 * s * 1.5 - 7 * math.sin((xx - 640) / 180 * math.pi)) for xx in range(640, 821, 6)]
    stroke_path(d, wire, "#b4b4b4", .9, .6)
    # the Pacific breeze, pouring over the western range
    for yy, op in ((150, .95), (190, .6)):
        d.arrow((60 * s, yy * s + oy), (430 * s, (yy + 40) * s + oy), "accent", 9)
    d.path("M%s,%s L%s,%s" % (f(430 * s), f(190 * s + oy), f(620 * s), f(330 * s + oy)), "accent", extra=' style="stroke-dasharray:6 5"')
    d.head((640 * s, 350 * s + oy), (40, 32), 9, True)
    d.arrow((1380 * s, 480 * s + oy), (1640 * s, 480 * s + oy), "accent", 9)
    return G


def cauca():
    W, H = 1200, 350
    s = W / 2400
    d = K.Drawing(W, H, "pt-cauca", "The Cauca Valley in one section", CAUCA_DESC, inline_css=False)
    G = cauca_scene(d, W, H, s)
    d.text((170 * s, 300 * s), "western Cordillera", "sub", "middle")
    d.text((2250 * s, 320 * s), "central Cordillera", "sub", "middle")
    d.text((1220 * s, 640 * s), "Cauca Valley", "sub", "middle")
    d.text((586 * s, G(560) - 34), "Roldanillo", "lab")
    d.text((586 * s, G(560) - 20), "east-facing launch, flying from about 9 am", "sub")
    d.text((1834 * s, G(1860) - 34), "Piedechinche", "lab", "end")
    d.text((1834 * s, G(1860) - 20), "west-facing, thermals from about 10 or 11", "sub", "end")
    d.text((845 * s, G(760) - 20), "high-voltage lines along the range", "sub")
    d.text((60 * s, 110 * s), "Pacific breeze, arriving from late morning", "val")
    d.text((640 * s, 250 * s), "a gusty backwind on this launch", "val")
    d.text((1330 * s, 520 * s), "a headwind on this one: fly on into the evening", "val")
    d.text((W - 10, H - 8), "schematic: the two sites are about 100 km apart", "tb", "end")
    return d


def cauca_p():
    W, H = 360, 560
    s = W / 2400
    d = K.Drawing(W, H, "pt-cauca-p", "The Cauca Valley in one section", CAUCA_DESC, inline_css=False)
    G = cauca_scene(d, W, 150, s, 30)
    marks = [((560 * s), G(560) - 18, "1"), ((1860 * s), G(1860) - 18, "2"), ((700 * s), G(700) + 24, "3"), ((250 * s), 40, "4")]
    for x, y, t in marks:
        d.text((x, y), t, "vn", "middle")
    rows = [("1", "Roldanillo", "east-facing launch, flying from about 9 am; the Pacific breeze is a gusty backwind here"),
            ("2", "Piedechinche", "west-facing, thermals from about 10 or 11; the same breeze is a headwind: fly on into the evening"),
            ("3", "High-voltage lines", "along the foot of the western range"),
            ("4", "Pacific breeze", "arriving over the western Cordillera from late morning")]
    y = 196
    for n_, a, b in rows:
        d.text((16, y), n_, "vn")
        d.text((36, y), a, "lab")
        y = lines(d, 36, y + 17, b, 44) + 16
    d.text((16, y + 8), "Schematic: the two sites are about 100 km apart.", "tb")
    return d


# ---------------------------------------------------------------- weather patterns hero: the sounding, over dry adiabats
WPH_DESC = ("A sounding read the simple way, after Ivelin Kalushkov's Manilla example: temperature against height. The early "
            "morning line bends back on itself near the ground: warmer above than below, an inversion, the thermal killer. "
            "The midday line leans over steadily until a kink where climbs stop; the dew point line comes within three or "
            "four degrees of it at cloud base. Behind them, the dry adiabats, worked out at 9.8 degrees per 1,000 m: the "
            "rate at which rising dry air cools. Schematic.")


def wp_hero():
    W, H = 1600, 600
    s = W / 2400
    d = K.Drawing(W, H, "pt-wph", "A sounding, read the simple way", WPH_DESC, inline_css=False)
    X0, X1, Y0, Y1 = 1060 * s, 2300 * s, 800 * s, 110 * s
    T0, T1, Z1 = -2, 30, 3500
    Pt = lambda t, z: (X0 + (t - T0) / (T1 - T0) * (X1 - X0), Y0 - z / Z1 * (Y0 - Y1))
    glow(d, "pt-wph-g", Pt(19, 2250)[0], Pt(19, 2250)[1], 300, "#ff7517", .12)
    d.raw('<clipPath id="pt-wph-c"><rect x="%s" y="%s" width="%s" height="%s"/></clipPath>' % (f(X0), f(Y1), f(X1 - X0), f(Y0 - Y1)))
    for t in range(0, 31, 5):
        d.line(Pt(t, 0), Pt(t, Z1), "ghost")
        d.text((Pt(t, 0)[0], Y0 + 18), "%d°" % t, "tb", "middle")
    for z in range(0, 3501, 500):
        d.line(Pt(T0, z), Pt(T1, z), "hair" if z == 0 else "ghost")
        if z:
            d.text((X0 - 10, Pt(0, z)[1] + 4), "{:,} m".format(z), "tb", "end")
    d.text((X1, Y0 + 38), "temperature", "tb", "end")
    # the dry adiabats: a parcel cools 9.8 degrees for every 1,000 m it rises
    d.raw('<g clip-path="url(#pt-wph-c)">')
    for t0 in range(0, 71, 5):
        a, b = Pt(t0, 0), Pt(t0 - 9.8 * Z1 / 1000, Z1)
        d.raw('<path d="M%s,%s L%s,%s" fill="none" stroke="#ff7517" stroke-opacity=".14" stroke-width=".75" vector-effect="non-scaling-stroke"/>' % (
            f(a[0]), f(a[1]), f(b[0]), f(b[1])))
    d.raw('</g>')
    p = Pt(29.5, 3100)
    d.text((p[0], p[1]), "dry adiabats: 9.8° per 1,000 m", "sub", "end")
    morn = [(16, 0), (13, 800), (14, 1050), (11.8, 1700)]
    d.path("M" + " L".join("%s,%s" % tuple(f(v) for v in Pt(t, z)) for t, z in morn), "detail", extra=' style="stroke-dasharray:5 4"')
    q0, q1 = Pt(14, 1050), Pt(21, 1150)
    d.line((q0[0] + 5, q0[1]), (q1[0] - 5, q1[1]), "hair")
    d.text((q1[0], q1[1] - 2), "8 am: warmer above than below", "tv")
    d.text((q1[0], q1[1] + 14), "an inversion, the thermal killer", "sub")
    mid = [(27.5, 0), (21, 700), (14.5, 1400), (8.3, 2100), (5.3, 2550), (5.8, 2800), (2.5, 3500)]
    stroke_path(d, [Pt(t, z) for t, z in mid], "#ff7517", 2.6, 1)
    dew = [(12, 0), (10.3, 1000), (8.8, 1700), (5.4, 2250), (2.0, 2650), (-1.5, 3100), (-2, 3500)]
    stroke_path(d, [Pt(t, z) for t, z in dew], "#f6f4f4", 1.8, .85)
    zb = 2250
    d.path("M%s,%s L%s,%s" % tuple(f(v) for v in Pt(T0, zb) + Pt(T1, zb)), "hair", extra=' style="stroke-dasharray:2 5"')
    cx, cy = Pt(19, zb)
    for dx, dy, r in ((0, -23, 31), (-33, -12, 23), (33, -13, 25), (-13, -39, 23), (19, -35, 20)):
        d.raw('<circle cx="%s" cy="%s" r="%s" fill="#f6f4f4" fill-opacity=".1"/>' % (f(cx + dx), f(cy + dy), f(r)))
    d.text((cx + 60, cy - 20), "cloud base", "lab")
    d.text((cx + 60, cy - 4), "lines within 3 to 4 degrees", "sub")
    kx, ky = Pt(5.3, 2550)
    d.circle((kx, ky), 8, "accent")
    d.line((kx + 9, ky - 4), (kx + 80, ky - 47), "hair")
    d.text((kx + 86, ky - 52), "the kink: climbs stop here", "val")
    p = Pt(17, 1800)
    d.text(p, "midday: the more it leans,", "tv")
    d.text((p[0], p[1] + 15), "the better the thermals", "sub")
    p = Pt(10.3, 1000)
    d.text((p[0] - 10, p[1] + 4), "dew point", "tv", "end")
    d.text((X1, Y1 - 20), "schematic: after the Manilla forecast in the conversation", "tb", "end")
    return d


def registry():
    return {
        "kb-sky-gods": (sky_hero, None),
        "kb-risk-vs-reward": (rvr_hero, None),
        "kb-sky-gods-section": (sky_section, None),
        "kb-storytellers-section": (story_section, None),
        "kb-weather-patterns-section": (wp_section, None),
        "kb-navigators-section": (nav_section, None),
        "kb-navigators-cauca": (cauca, cauca_p),
        "kb-weather-patterns": (wp_hero, None),
    }
