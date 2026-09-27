#!/usr/bin/env python3
"""
The last knowledge base drawings taken by a lens (tools/v4_lens.py), redrawn
with the kit from the scripts they replace (tools/kbfig/*.py): the same
geometry, labels and numbers, at two thirds of the old 2400-wide coordinates.

  computed   kb-know-your-equipment (5.5 m/s down, 5.5 forward: the 1:1
             glide as a true vector triangle), kb-new-technologies (a
             four-digit section at 18%), kb-resources-tools-tips (the
             breathing trace, generated), kb-know-your-equipment-section
             (reserve areas to one scale)
  painted    kb-living-the-dream-section (fresh snow), kb-world-cups (forty
             tracklogs and a leader)
  kit        kb-brand-stories, kb-brand-stories-section,
             kb-new-technologies-section, kb-resources-tools-tips-section,
             kb-world-cups-section

Heroes are 1600 x 600 with the left 40% empty; side drawings 1600 x 667 with
the subject on the right, as before.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402
from v4_computed import P, rect, flow, naca  # noqa: E402
from v4_painted import glow, stroke_path, fill_path, fade_left, vgrad, BG  # noqa: E402

f = K.f
S = 2 / 3


def T(x, y):
    return (x * S, y * S)


def TP(pts):
    return [T(x, y) for x, y in pts]


# ---------------------------------------------------------------- know your equipment hero: a reserve in use
KYE_DESC = ("A reserve in use: a round canopy above, the pilot under it, the neutralised paraglider hanging alongside, and "
            "the two speeds that certification allows to be equal: 5.5 m/s down and 5.5 m/s forward, a 1:1 glide. "
            "Big enough to dominate the wing, or it does not work.")


def kye_hero():
    d = K.Drawing(1600, 600, "rs-kye", "A reserve in use, and the 1:1 glide", KYE_DESC, inline_css=False)
    glow(d, "rs-kye-g", *T(1560, 260), 300, "#ff7517", .12)
    O, RX, RY, tilt = (1560, 250), 330, 150, math.radians(-8)

    def rot(p):
        x, y = p[0] - O[0], p[1] - O[1]
        c, s = math.cos(tilt), math.sin(tilt)
        return T(O[0] + x * c - y * s, O[1] + x * s + y * c)
    ths = [math.pi + math.pi * k / 60 for k in range(61)]
    top = [rot((O[0] + RX * math.cos(t), O[1] + RY * math.sin(t))) for t in ths]
    skirt = [rot((O[0] + RX * math.cos(t), O[1] + 26 * (1 - math.cos(t) ** 2))) for t in ths]
    d.poly(top + skirt[::-1], "outline", True, "card")
    for k in range(13):
        fr = -1 + 2 * k / 12
        x, y = O[0] + RX * fr, O[1] - RY * math.sqrt(max(0, 1 - fr * fr))
        d.line(rot((x, O[1])), rot((x, y)), "ghost")
    d.poly(skirt, "detail")
    Pp = (1470, 620)
    for k in range(15):
        fr = -1 + 2 * k / 14
        d.line(rot((O[0] + RX * fr, O[1])), T(Pp[0], Pp[1] - 18), "ghost")
    d.circle(T(Pp[0], Pp[1] - 52), 12 * S, "outline", fill="card")
    d.poly(TP([(Pp[0] - 16, Pp[1] - 38), (Pp[0] + 20, Pp[1] - 34), (Pp[0] + 34, Pp[1] + 6), (Pp[0] + 2, Pp[1] + 24),
               (Pp[0] - 30, Pp[1] + 12)]), "outline", True, "card")
    Q = (1150, 430)
    arc = [(Q[0] + 117 * math.cos(t) + 6 * math.sin(3 * t), Q[1] - 70 * math.sin(t)) for t in [.15 + 2.75 * k / 40 for k in range(41)]]
    d.poly(TP(arc + [(x, y + 22) for x, y in arc[::-1]]), "detail", True, "card")
    for k in range(2, 41, 6):
        p = (arc[k][0], arc[k][1] + 22)
        m = ((p[0] + Pp[0]) / 2 - 30, (p[1] + Pp[1]) / 2 + 60)
        d.poly(TP([p, m, (Pp[0] - 14, Pp[1] - 20)]), "ghost")
    d.text(T(Q[0], Q[1] + 62), "the paraglider, neutralised", "sub", "middle")
    # the vectors: equal legs, so the resultant is at 45 degrees, a 1:1 glide
    V = T(1980, 330)
    L = 300 * S
    d.raw('<path class="fa" style="fill-opacity:.08" d="M%s,%s L%s,%s L%s,%s Z"/>' % (f(V[0]), f(V[1]), f(V[0] + L), f(V[1]), f(V[0] + L), f(V[1] + L)))
    d.arrow(V, (V[0], V[1] + L), "accent", 10)
    d.arrow(V, (V[0] + L, V[1]), "accent", 10)
    d.path("M%s,%s L%s,%s" % (f(V[0]), f(V[1]), f(V[0] + L), f(V[1] + L)), "accent", extra=' style="stroke-dasharray:6 5"')
    flow(d, [V, (V[0] + L, V[1] + L)], "#f6f4f4", .6)
    d.angle((V[0], V[1]), 46, 0, 45, "45°")
    d.text((V[0] - 10, V[1] + L / 2), "5.5 m/s down", "val", "end")
    d.text((V[0] + L / 2, V[1] - 12), "5.5 m/s forward", "val", "middle")
    d.text((V[0] + L, V[1] + L + 20), "a 1:1 glide is allowed", "tv", "end")
    d.text((V[0] + L, V[1] + L + 36), "certified, and still gliding", "sub", "end")
    d.text(T(O[0] + RX + 40, O[1] - 70), "big enough to dominate the wing,", "sub")
    d.text(T(O[0] + RX + 40, O[1] - 48), "or it does not work", "sub")
    d.line(T(960, 820), T(2400, 820), "hair")
    fade_left(d, 640, 120)
    return d


# ---------------------------------------------------------------- know your equipment side: reserve sizes, to scale
KYES_DESC = ("Reserve size against the wing it has to dominate: three reserves drawn as circles of equal area to one scale, "
             "20 m² (passes certification), 30 m² (starts to dominate) and 40 m² (or carry two), beside a 25 m² paraglider "
             "planform.")


def kye_section():
    d = K.Drawing(1600, 667, "rs-kyes", "Reserve size against the wing", KYES_DESC, inline_css=False)
    glow(d, "rs-kyes-g", *T(1500, 600), 330, "#ff7517", .12)
    SC = 34.0 * S                                       # px per metre, one scale for areas
    span, chord = 11.5 * SC, 2.3 * SC
    n = 120
    xs = [-1 + 2 * i / (n - 1) for i in range(n)]
    c = [chord * max(0, 1 - x * x) ** .42 for x in xs]
    X = [1560 * S + span / 2 * x for x in xs]
    te = [300 * S + .42 * ci + 10 * S * x * x for x, ci in zip(xs, c)]
    le = [t - ci for t, ci in zip(te, c)]
    d.poly(list(zip(X, le)) + list(zip(X, te))[::-1], "detail", True, "card")
    for k in range(0, n, 6):
        d.line((X[k], le[k]), (X[k], te[k]), "ghost")
    d.text(T(1560, 385), "the wing it has to dominate: 25 m²", "sub", "middle")
    for i, (a, lab, note) in enumerate(((20, "20 m²", "passes certification"), (30, "30 m²", "starts to dominate"),
                                        (40, "40 m²", "or carry two"))):
        r = math.sqrt(a / math.pi) * SC
        cx, cy = T(1290 + i * 300, 640)
        d.raw('<circle class="fa" cx="%s" cy="%s" r="%s" style="fill-opacity:%s"/>' % (f(cx), f(cy), f(r), .06 + .08 * i))
        d.circle((cx, cy), r, "outline" if i == 0 else "accent")
        d.text((cx, cy + r + 20), lab, "lab", "middle")
        d.text((cx, cy + r + 36), note, "sub", "middle")
    d.text(T(1290, 490), "reserves, same scale", "sub")
    return d


# ---------------------------------------------------------------- new technologies hero: a two-liner section
NTH_DESC = ("A two-liner section drawn as a technical sheet: a thick modern airfoil, about 18% of chord, with its two "
            "load-bearing line groups (AA set far back, BB behind), the old A point kept as an unloaded line for launching, "
            "the nose ahead of AA drawn flexing (the wing pitches and speeds up), and a sensor trace underneath standing "
            "for the harness that watches the wing: 100 readings a second.")


def nt_hero():
    d = K.Drawing(1600, 600, "rs-nth", "A two-liner section", NTH_DESC, inline_css=False)
    glow(d, "rs-nth-g", *T(1640, 300), 380, "#ff7517", .1)
    X0, Y0, C = 1080, 300, 1120
    up, lo = naca(.18, .035, .35, 200)
    U = [T(X0 + C * x, Y0 - C * y) for x, y in up]
    Lo = [T(X0 + C * x, Y0 - C * y) for x, y in lo]
    d.path("M" + " L".join("%s,%s" % (f(a), f(b)) for a, b in U + Lo[::-1]) + " Z", "outline", fill="card")
    for k in range(1, 16):
        i = int(k / 16 * (len(U) - 1))
        d.line(U[i], Lo[i], "ghost")
    xa = .30
    idx = [i for i, (x, _) in enumerate(up) if x < xa]
    for surf, dy in ((U, 22), (Lo, 16)):
        pts = []
        for i in idx:
            dd = (1 - up[i][0] / xa) ** 1.6
            pts.append((surf[i][0] + dd * 6 * S, surf[i][1] + dd * dy * S))
        d.path("M" + " L".join("%s,%s" % (f(a), f(b)) for a, b in pts), "accent", extra=' style="stroke-dasharray:6 5"')
    d.text(T(X0 - 10, Y0 - 200), "the nose may flex:", "val")
    d.text(T(X0 - 10, Y0 - 178), "the wing pitches and speeds up", "val")
    d.line(T(X0 + 10, Y0 - 166), T(X0 + 40, Y0 - 70), "hair")

    def lp(fr):
        return min(Lo, key=lambda q: abs((q[0] / S - X0) / C - fr))
    R = T(1560, 800)
    aa, bb, old = lp(.30), lp(.62), lp(.10)
    d.line(aa, (R[0] - 9, R[1]), "outline")
    d.line(bb, (R[0] + 9, R[1]), "outline")
    d.path("M%s,%s L%s,%s" % (f(old[0]), f(old[1]), f(R[0] - 13), f(R[1])), "detail", extra=' style="stroke-dasharray:3 5"')
    d.dot(aa, 4, True)
    d.dot(bb, 4, True)
    d.circle(old, 3.5, "detail", fill="card")
    d.text((aa[0] + 10, aa[1] + 24), "AA", "vn")
    d.text((bb[0] + 10, bb[1] + 24), "BB", "vn")
    d.text((old[0] - 10, old[1] + 26), "old A point:", "sub", "end")
    d.text((old[0] - 10, old[1] + 40), "no load, kept for launch", "sub", "end")
    d.text((R[0] + 20, R[1] + 4), "two load-bearing groups", "sub")
    it = min(range(len(up)), key=lambda i: abs(up[i][0] - .30))
    d.dim(Lo[it], U[it], -18, "about 18% of chord")
    rnd = random.Random(3)
    tr = []
    for i in range(500):
        x = 1020 + 1300 * i / 499
        sig = 12 * math.sin(x / 37) + 5 * math.sin(x / 11) + rnd.gauss(0, 1.4)
        if 2020 < x < 2200:
            sig += 55 * math.sin((x - 2020) / 180 * math.pi) * math.sin((x - 2020) / 9)
        tr.append(T(x, 860 + sig * .6))
    stroke_path(d, tr, "#ff7517", 1, .8)
    d.text(T(2320, 828), "100 readings a second", "tb", "end")
    fade_left(d, 660, 60)
    return d


# ---------------------------------------------------------------- new technologies side: the collapse field
NTS_DESC = ("A wing planform marked up the way a test lab marks it for the big asymmetric collapse: 50% of the trailing "
            "edge (±2.5), a fold line at 45 degrees to the open side, stickers on the bottom surface, and a folding line "
            "that pulls the fold where the norm wants it.")


def nt_section():
    d = K.Drawing(1600, 667, "rs-nts", "The big asymmetric collapse, as a lab marks it", NTS_DESC, inline_css=False)
    cx, span, chord = 1600, 1180, 300
    n = 200
    xs = [-1 + 2 * i / (n - 1) for i in range(n)]
    c = [chord * max(0, 1 - x * x) ** .42 for x in xs]
    le = [330 + 10 * x * x - .15 * ci for x, ci in zip(xs, c)]
    te = [l + ci for l, ci in zip(le, c)]
    X = [cx + span / 2 * x for x in xs]
    d.poly(TP(list(zip(X, le)) + list(zip(X, te))[::-1]), "outline", True, "card")
    for k in range(0, n, 8):
        d.line(T(X[k], le[k]), T(X[k], te[k]), "ghost")
    i0 = min(range(n), key=lambda i: abs(X[i] - cx))
    p_te = (X[i0], te[i0])
    p_le = None
    for k in range(1, 1200):
        q = (p_te[0] + k * .5, p_te[1] - k * .5)
        j = min(range(n), key=lambda i: abs(X[i] - q[0]))
        if q[1] <= le[j]:
            p_le = q
            iL = j
            break
    field = [p_te, p_le] + list(zip(X[iL:], le[iL:])) + list(zip(X[i0:], te[i0:]))[::-1]
    glow(d, "rs-nts-g", *T((p_te[0] + p_le[0]) / 2, (p_te[1] + p_le[1]) / 2), 200, "#ff7517", .22)
    d.raw('<path class="fa" style="fill-opacity:.14" d="M%s Z"/>' % " L".join("%s,%s" % (f(a), f(b)) for a, b in TP(field)))
    d.line(T(*p_te), T(*p_le), "accent")
    for fr in (.12, .31, .5, .69, .88):
        q = T(p_te[0] + (p_le[0] - p_te[0]) * fr, p_te[1] + (p_le[1] - p_te[1]) * fr)
        rect(d, q[0] - 6, q[1] - 6, 12, 12, "fa", .85)
    d.angle(T(*p_te), 40, -45, 0, "45°")
    y = max(te) + 70
    d.dim(T(X[i0], y), T(X[-1], y), 0, "50% of the trailing edge, ±2.5")
    d.path("M%s,%s L%s,%s" % tuple(f(v) for v in T(p_le[0] + 20, p_le[1] + 6) + T(cx + 120, 880)), "accent",
           extra=' style="stroke-dasharray:6 5"')
    d.text(T(cx + 140, 900), "folding line: pulls the fold where the norm wants it", "sub")
    d.text(T(cx - span / 2 + 40, min(le) - 40), "open side", "sub")
    return d


# ---------------------------------------------------------------- brand stories hero: a design sheet
BSH_DESC = ("Brand stories as a design sheet: a paraglider planform with tubercles along the central 60% of the leading edge "
            "(the wave leading edge Gin Seok Song describes) and plain tips, and below it a pod harness in section with its "
            "crushable protector (a protector that crushes rather than springs back) and the carabiner it hangs from.")


def bs_hero():
    d = K.Drawing(1600, 600, "rs-bsh", "A design sheet: tubercles and a crushable protector", BSH_DESC, inline_css=False)
    glow(d, "rs-bsh-g", *T(1690, 260), 360, "#ff7517", .1)
    for x in range(1000, 2400, 80):
        d.raw('<path d="M%s,%s V%s" stroke="#fff" stroke-opacity=".05" vector-effect="non-scaling-stroke"/>' % (f(x * S), f(60 * S), f(860 * S)))
    CX, TE0, SPAN, CH = 1690, 330, 1180, 250
    n = 360
    xs = [-1 + 2 * i / (n - 1) for i in range(n)]
    c = [CH * max(0, 1 - x * x) ** .42 for x in xs]
    te = [TE0 + .4 * ci + 26 * x * x for x, ci in zip(xs, c)]
    le = [t - ci for t, ci in zip(te, c)]
    bump = [7 * max(0, math.sin(x * math.pi * 34)) ** .8 if abs(x) <= .6 else 0 for x in xs]
    X = [CX + SPAN / 2 * x for x in xs]
    lew = [l - b for l, b in zip(le, bump)]
    d.poly(TP(list(zip(X, lew)) + list(zip(X, te))[::-1]), "detail", True, "card")
    for k in range(0, n, 12):
        d.line(T(X[k], le[k]), T(X[k], te[k]), "ghost")
    d.poly(TP([(X[i], lew[i]) for i in range(n) if abs(xs[i]) <= .6]), "accent")
    y0 = min(le) - 60
    d.dim(T(CX - SPAN / 2 * .6, y0), T(CX + SPAN / 2 * .6, y0), 0, "tubercles on the central 60% of the span")
    d.text(T(CX + SPAN / 2 * .86, le[int(n * .93)] - 40), "plain tips", "sub", "middle")
    HX, HY = 1500, 690
    body = [(HX - 260, HY - 40), (HX - 150, HY - 78), (HX + 40, HY - 70), (HX + 330, HY - 40), (HX + 470, HY - 6),
            (HX + 330, HY + 30), (HX + 40, HY + 44), (HX - 160, HY + 40), (HX - 250, HY + 14)]
    d.spline(TP(body), "outline", True, "card", .3)
    px0, py0 = HX - 200, HY + 44
    for i in range(14):
        for j in range(3):
            d.circle(T(px0 + i * 22 + (11 if j % 2 else 0), py0 + 10 + j * 17), 9 * S, "accent" if j == 0 else "ghost")
    d.poly(TP([(px0 - 14, py0), (px0 + 310, py0), (px0 + 320, py0 + 56), (px0 - 4, py0 + 56)]), "hair", True)
    d.text(T(px0 + 400, py0 + 30), "a protector that crushes", "tv")
    d.text(T(px0 + 400, py0 + 52), "rather than springs back", "sub")
    KX, KY = 1240, 560
    kx, ky = T(KX, KY)
    d.path("M%s,%s a%s,%s 0 0 1 %s,0 v%s a%s,%s 0 0 1 -%s,0 Z" % (
        f(kx - 16), f(ky - 18), f(16), f(16), f(32), f(36), f(16), f(16), f(32)), "outline")
    d.text((kx, ky + 54), "carabiner", "sub", "middle")
    d.path("M%s,%s L%s,%s" % tuple(f(v) for v in (kx, ky + 34) + T(HX - 230, HY - 30)), "ghost")
    fade_left(d, 660, 60)
    return d


# ---------------------------------------------------------------- brand stories side: a collapse and two ways back
BSS_DESC = ("A collapse and two ways back, after Gin Seok Song: a wing seen from in front, flying; the same wing with one side "
            "folded, a big asymmetric collapse; then two outcomes: it reopens gradually, damped, or it reopens violently and "
            "the other side goes.")


def front(d, cx, cy, w, cut_r=0., cut_l=0., accent=False):
    n = 80
    pts = [(cx + w / 2 * math.cos(t) / math.cos(.1 * math.pi), cy - .36 * w * math.sin(t))
           for t in [.1 * math.pi + .8 * math.pi * k / (n - 1) for k in range(n)]]
    r0, l0 = int(n * cut_r), n - int(n * cut_l)
    d.poly(TP(pts[r0:l0]), "accent" if accent else "outline")
    for a, b in ((r0, None), (None, l0)):
        if a:
            fl = pts[:r0][::-1]
            fold = [(pts[r0][0] + (x - pts[r0][0]) * -.55, pts[r0][1] + (y - pts[r0][1]) * 1.05 + 18) for x, y in fl]
            d.path("M" + " L".join("%s,%s" % (f(p[0]), f(p[1])) for p in TP(fold)), "accent" if accent else "detail",
                   extra=' style="stroke-dasharray:5 4"')
        if b is not None and b < n:
            fl = pts[b - 1:]
            fold = [(pts[b - 1][0] + (x - pts[b - 1][0]) * -.55, pts[b - 1][1] + (y - pts[b - 1][1]) * 1.05 + 18) for x, y in fl]
            d.path("M" + " L".join("%s,%s" % (f(p[0]), f(p[1])) for p in TP(fold)), "accent" if accent else "detail",
                   extra=' style="stroke-dasharray:5 4"')
    for k in range(5, n - 5, 10):
        if r0 <= k < l0:
            d.line(T(*pts[k]), T(cx, cy + .62 * w), "ghost")
    d.circle(T(cx, cy + .62 * w + 8), 6, "outline", fill="card")


def bs_section():
    d = K.Drawing(1600, 667, "rs-bss", "A collapse and two ways back", BSS_DESC, inline_css=False)
    glow(d, "rs-bss-g", *T(2150, 640), 180, "#ff7517", .2)
    front(d, 1140, 470, 360)
    d.text(T(1140, 780), "flying", "sub", "middle")
    d.arrow(T(1360, 420), T(1440, 420), "detail", 8)
    front(d, 1660, 470, 360, cut_r=.42)
    d.text(T(1660, 780), "a big asymmetric collapse", "sub", "middle")
    d.arrow(T(1860, 330), T(1980, 260), "outline", 9)
    d.arrow(T(1860, 540), T(1980, 610), "accent", 9)
    front(d, 2150, 230, 260)
    d.text(T(2150, 432), "reopens gradually, damped", "tv", "middle")
    front(d, 2150, 640, 260, cut_l=.4, accent=True)
    d.text(T(2150, 850), "reopens violently: the other side goes", "val", "middle")
    return d


# ---------------------------------------------------------------- resources hero: the breathing trace
RTH_DESC = ("A breathing trace drawn as an instrument line: short inhales, longer exhales (35% of each breath in, 65% out), "
            "the amplitude settling as it runs to the right, with a small paraglider riding the calmer end. Slow the breath, "
            "and the thinking comes back.")


def rt_hero():
    d = K.Drawing(1600, 600, "rs-rth", "Slow the breath", RTH_DESC, inline_css=False)
    glow(d, "rs-rth-g", *T(2140, 400), 260, "#ff7517", .12)
    for k in range(1, 7):
        d.line(T(1000, 520 - k * 40), T(2340, 520 - k * 40), "ghost")
    d.line(T(1000, 520), T(2340, 520), "hair")
    pts, cyc, x = [], 0.0, 1000.0
    dx = 1340 / 900
    for i in range(901):
        per = 170 + (x - 1000) * .14
        ph = cyc % 1
        b = math.sin(ph / .35 * math.pi / 2) if ph < .35 else math.cos((ph - .35) / .65 * math.pi / 2)
        amp = 170 * math.exp(-(x - 1000) / 900) + 45
        pts.append(T(x, 520 - amp * b))
        cyc += dx / per
        x += dx
    stroke_path(d, pts, "#ff7517", 2, .95)
    flow(d, pts, "#f6f4f4", .55, slow=True)
    d.text(T(1030, 300), "in", "sub", "middle")
    d.text(T(1130, 300), "longer out", "sub", "middle")
    px, py = 2140, 330
    arc = [(px + 95 * math.cos(t), py - 40 * math.sin(t)) for t in [.15 + 2.84 * k / 30 for k in range(31)]]
    d.poly(TP(arc + [(x_, y_ + 10) for x_, y_ in arc[::-1]]), "outline", True, "card")
    for k in range(0, 31, 5):
        d.line(T(arc[k][0], arc[k][1] + 10), T(px, py + 90), "ghost")
    d.circle(T(px, py + 96), 5, "outline", fill="card")
    d.text(T(2340, 820), "slow the breath, and the thinking comes back", "sub", "end")
    fade_left(d, 660, 60)
    return d


# ---------------------------------------------------------------- resources side: two thoughts
RTS_DESC = ("Fighting a thought against letting it be there: two curves of how loud an unhelpful thought gets over time in "
            "the air. Pushed against, it grows; noticed and let be, it rises and passes.")


def rt_section():
    d = K.Drawing(1600, 667, "rs-rts", "Pushed against, or let be", RTS_DESC, inline_css=False)
    glow(d, "rs-rts-g", *T(1400, 600), 260, "#ff7517", .12)
    x0, x1, yb = 1100, 2280, 780
    d.line(T(x0, yb), T(x1, yb), "detail")
    d.line(T(x0, yb), T(x0, 260), "detail")
    d.text(T(x1, yb + 34), "time in the air", "tb", "end")
    d.text(T(x0 - 16, 270), "how loud the thought is", "tb", "end")
    fight, allow = [], []
    for i in range(201):
        t = i / 200
        X = x0 + t * (x1 - x0)
        fight.append(T(X, yb - (120 + 380 * t ** 1.3 + 18 * math.sin(t * 40))))
        a = 260 * math.exp(-((t - .18) / (.2 if t < .18 else .28)) ** 2)
        allow.append(T(X, yb - (120 + a)))
    stroke_path(d, fight, "#f6f4f4", 1.6, .8)
    stroke_path(d, allow, "#ff7517", 2, 1)
    d.text((fight[-1][0] - 6, fight[-1][1] - 16), "pushed against: it grows", "lab", "end")
    d.text((allow[-1][0] - 6, allow[-1][1] - 14), "noticed and let be: it passes", "val", "end")
    return d


# ---------------------------------------------------------------- world cups hero: forty tracklogs
WCH_DESC = ("Forty tracklogs from a race start converging on one turnpoint cylinder, tagging its edge and bending away, one "
            "leading track a little ahead in orange: one thermal ahead is what leading points pay for.")


def wc_hero():
    d = K.Drawing(1600, 600, "rs-wch", "Forty tracks, one turnpoint", WCH_DESC, inline_css=False)
    C, R = (1700, 440), 170
    glow(d, "rs-wch-g", *T(*C), R * S * 1.8, "#ff7517", .14)
    d.raw('<circle class="fa" cx="%s" cy="%s" r="%s" style="fill-opacity:.05"/>' % (f(C[0] * S), f(C[1] * S), f(R * S)))
    d.circle(T(*C), R * S, "detail")
    d.dot(T(*C), 3, False)
    d.text(T(C[0], C[1] - R - 18), "turnpoint", "sub", "middle")
    rnd = random.Random(11)
    tan = (C[0] - R * .2, C[1] - R * .98)
    lead = None
    for k in range(40):
        y0, x0 = 520 + rnd.gauss(0, 90), 1080 + rnd.gauss(0, 20)
        tgt = (tan[0] + rnd.gauss(0, 14), tan[1] + rnd.gauss(0, 14))
        s = rnd.gauss(0, .5)
        pts = [(x0, y0)]
        for i in range(1, 30):
            t = i / 29
            pts.append((x0 * (1 - t) + tgt[0] * t + rnd.gauss(0, 3), y0 * (1 - t) + tgt[1] * t + 60 * math.sin(t * math.pi) * s + rnd.gauss(0, 3)))
        ex = (tgt[0] + 420 + rnd.gauss(0, 40), tgt[1] + 180 + rnd.gauss(0, 40))
        for i in range(1, 20):
            t = i / 19
            pts.append((tgt[0] * (1 - t) + ex[0] * t + rnd.gauss(0, 3), tgt[1] * (1 - t) + ex[1] * t + rnd.gauss(0, 3)))
        if k == 0:
            lead = [(x + 60, y - 6) for x, y in pts]
        else:
            stroke_path(d, TP(pts), "#b4b4b4", .7, .3)
    stroke_path(d, TP(lead), "#ff7517", 1.8, 1)
    flow(d, TP(lead), "#f6f4f4", .7)
    d.text(T(2330, 820), "one thermal ahead is what leading points pay for", "sub", "end")
    fade_left(d, 700, 60)
    return d


# ---------------------------------------------------------------- world cups side: multi radius turnpoints
WCS_DESC = ("Multi radius turnpoints: one turnpoint with three concentric cylinders, the smallest for the heaviest class and "
            "the largest for the lightest, and the course line each class flies from the last turnpoint to the next, tagging "
            "its own edge where the line bends.")


def wc_section():
    d = K.Drawing(1600, 667, "rs-wcs", "Multi radius turnpoints", WCS_DESC, inline_css=False)
    C, start, nxt = (1720, 500), (1060, 820), (2300, 780)
    glow(d, "rs-wcs-g", *T(*C), 220, "#ff7517", .12)

    def unit(a, b):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    dd, ee = unit(C, start), unit(C, nxt)
    m = (dd[0] + ee[0], dd[1] + ee[1])
    mL = math.hypot(*m)
    m = (m[0] / mL, m[1] / mL)
    for r, cls in ((300, "accent"), (210, "detail"), (120, "outline")):
        tag = (C[0] + m[0] * r, C[1] + m[1] * r)
        d.circle(T(*C), r * S, cls)
        d.poly(TP([start, tag, nxt]), cls)
        d.dot(T(*tag), 3.5, cls == "accent")
    d.dot(T(*C), 3, False)
    d.text(T(C[0] + 320, C[1] - 240), "lightest pilots: biggest cylinder", "val")
    d.text(T(C[0] + 240, C[1] - 150), "middle", "sub")
    d.text(T(C[0] + 140, C[1] - 60), "heaviest: smallest", "lab")
    d.text(T(start[0], start[1] + 34), "from the last turnpoint", "sub", "middle")
    d.text(T(nxt[0], nxt[1] + 34), "to the next", "sub", "middle")
    return d


# ---------------------------------------------------------------- living the dream side: the awkward line, painted
LTS_DESC = ("Awkward lines, after Benjamin Jordan's story of skiing with a friend: a ski slope seen from above, the worn "
            "tracks everyone follows (same snow, already tracked), a stand of birch trees with a tight gap, and one line "
            "squeezing through it into fresh snow, even taking the easy way down from there. Schematic.")


def ltd_section():
    d = K.Drawing(1600, 667, "rs-lts", "The awkward line", LTS_DESC, inline_css=False)
    rnd = random.Random(7)
    # the snow: cool light on the untouched side
    glow(d, "rs-lts-snow", *T(2000, 700), 360, "#e9eef5", .1)
    for _ in range(700):
        x, y = rnd.uniform(1650, 2330), rnd.uniform(430, 930)
        d.raw('<circle cx="%s" cy="%s" r="%s" fill="#f6f4f4" fill-opacity=".16"/>' % (f(x * S), f(y * S), f(rnd.uniform(.4, 1.3))))
    for i in range(16):
        off, ph, amp = rnd.gauss(0, 38), rnd.uniform(0, 6), rnd.uniform(20, 45)
        pts = [(1300 + off + amp * math.sin(yy / 70 + ph) + (yy - 110) * .08, yy) for yy in [110 + 830 * k / 100 for k in range(101)]]
        stroke_path(d, TP(pts), "#b4b4b4", 1, .16)
    d.text(T(1225, 80), "the way everyone goes", "sub", "middle")
    d.text(T(1225, 104), "same snow, already tracked", "tb", "middle")
    for x, y in ((1600, 300), (1690, 330), (1745, 262), (1560, 390), (1830, 300), (1905, 360), (1640, 205), (1980, 280),
                 (1520, 250), (2050, 350)):
        d.raw('<circle cx="%s" cy="%s" r="%s" fill="#2b2d33" fill-opacity=".6"/>' % (f(x * S), f(y * S), f(34 * S)))
        d.circle(T(x, y), 34 * S, "hair")
        d.raw('<circle cx="%s" cy="%s" r="%s" fill="#f6f4f4" fill-opacity=".85"/>' % (f(x * S), f(y * S), f(8 * S)))
        rect(d, (x - 5) * S, (y - 2) * S, 10 * S, 3 * S, "f", .9)
    p0 = [(1330 + 330 * t ** 1.3, 120 + 140 * t) for t in [k / 40 for k in range(41)]]
    gap = [(1660, 260), (1718, 296), (1760, 350)]
    low = [(1760 + 150 * math.sin((yy - 350) / 95) * math.exp(-(yy - 350) / 900) + (yy - 350) * .22, yy)
           for yy in [350 + 580 * k / 100 for k in range(101)]]
    track = TP(p0 + gap + low)
    glow(d, "rs-lts-gap", *T(1718, 296), 50, "#ff7517", .35)
    stroke_path(d, track, "#ff7517", 2.4, 1)
    flow(d, track, "#f6f4f4", .7)
    d.head(track[-1], (track[-1][0] - track[-3][0], track[-1][1] - track[-3][1]), 10, True)
    d.path("M%s,%s a%s,%s 0 1,0 %s,0 a%s,%s 0 1,0 %s,0" % (f(1718 * S - 17), f(296 * S), 17, 17, 34, 17, 17, -34), "accent",
           extra=' style="stroke-dasharray:3 3"')
    d.line(T(1745, 296), T(2090, 180), "hair")
    d.text(T(2100, 170), "the awkward line", "val")
    d.text(T(2100, 196), "a gap between birch trees", "sub")
    d.text(T(2100, 216), "you barely fit through", "sub")
    d.text(T(2150, 640), "fresh snow from there,", "lab", "middle")
    d.text(T(2150, 664), "even taking the easy way down", "sub", "middle")
    d.text(T(2330, 975), "schematic", "tb", "end")
    return d


def registry():
    return {
        "kb-know-your-equipment": (kye_hero, None),
        "kb-know-your-equipment-section": (kye_section, None),
        "kb-new-technologies": (nt_hero, None),
        "kb-new-technologies-section": (nt_section, None),
        "kb-brand-stories": (bs_hero, None),
        "kb-brand-stories-section": (bs_section, None),
        "kb-resources-tools-tips": (rt_hero, None),
        "kb-resources-tools-tips-section": (rt_section, None),
        "kb-world-cups": (wc_hero, None),
        "kb-world-cups-section": (wc_section, None),
        "kb-living-the-dream-section": (ltd_section, None),
    }
