#!/usr/bin/env python3
"""
v4 figures, drawn with the kit (tools/v4_draw.py). One function per figure;
each returns inline SVG for a wide layout (desktop) and a tall one (phone).

Every label, number and dimension here is traced to a sentence on the page
the figure sits on (the source is noted beside each one). Shapes are drawn
from geometry (curves, arcs), never to look measured: the title block says
"Not to scale".
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402


# ---------------------------------------------------------------- geometry
def naca(c, t=0.15):
    """Half thickness of a symmetric 4-digit section at chord fraction c."""
    return 5 * t * (0.2969 * math.sqrt(c) - 0.1260 * c - 0.3516 * c ** 2 + 0.2843 * c ** 3 - 0.1036 * c ** 4)


def camber(c, m=0.035, p=0.35):
    return m / p ** 2 * (2 * p * c - c * c) if c < p else m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * c - c * c)


def profile(le, chord, aoa_deg, n=34):
    """Upper and lower surface points of a cambered profile, nose at le,
    pitched nose-up by aoa (screen: y down)."""
    a = math.radians(aoa_deg)
    d = (math.cos(a), math.sin(a))          # along the chord, towards the trailing edge (down-right when pitched)
    nn = (d[1], -d[0])                       # up from the chord
    cs = [(1 - math.cos(math.pi * i / n)) / 2 for i in range(n + 1)]
    def at(c, s):
        y = camber(c) + s * naca(c)
        return (le[0] + d[0] * c * chord + nn[0] * y * chord, le[1] + d[1] * c * chord + nn[1] * y * chord)
    up = [at(c, 1) for c in cs]
    lo = [at(c, -1) for c in cs]
    return up, lo, at, d, nn


# ---------------------------------------------------------------- the views
def side_view(d, o, s=1.0, labels=True, narrow=False):
    """Side view, flying to the left: the profile, the lines, the pilot
    facing forward, the speed bar at the feet. o = top-left, s = scale."""
    X = lambda x, y: (o[0] + x * s, o[1] + y * s)
    chord = 250 * s
    aoa = 12.0
    le = X(150, 118)
    up, lo, at, dv, nv = profile(le, chord, aoa)
    d.path(K.catmull(up + lo[::-1][1:], closed=True, tension=.35), "outline", fill="card")
    te = at(1, 0)
    # the chord line, extended forward past the nose (a centre line)
    fwd = (-dv[0], -dv[1])
    d.line(K.add(le, fwd, 176 * s), K.add(te, dv, 26 * s), "centre")
    # the air meeting the wing: level, from ahead
    for k, dy in enumerate((0, 18, 36)):
        a = K.add(le, (-176 * s, dy * s))
        b = K.add(le, (-(24 if k == 0 else 120) * s, dy * s))
        d.line(a, b, "ghost")
        d.head(b if k else K.add(le, (-130 * s, 0)), (1, 0), 7)
    # pilot, seated, facing the direction of flight (left)
    C = X(316, 452)
    head = K.add(C, (6 * s, -40 * s))
    P = lambda x, y: K.add(C, (x * s, y * s))
    # the harness: back protector and seat board, drawn behind the pilot
    d.spline([P(24, -30), P(30, 4), P(26, 38), P(4, 48), P(-30, 46), P(-34, 38), P(-4, 36), P(14, 14), P(14, -28)],
             "detail", closed=True, fill="card", tension=.5)
    # the pilot: one silhouette, torso reclined a little, thighs forward, shins down to the bar
    d.spline([P(12, -28), P(16, -6), P(16, 20), P(6, 32), P(-30, 34), P(-40, 40), P(-44, 58), P(-40, 68),
              P(-52, 70), P(-52, 64), P(-54, 46), P(-42, 26), P(-12, 22), P(2, 10), P(0, -20), P(4, -28)],
             "outline", closed=True, fill="card", tension=.42)
    d.circle(head, 10.5 * s, "outline", fill="card")
    feet = P(-50, 70)
    # the risers: A to the front of the carabiner, the rear risers behind
    ra, rb = K.add(C, (-6 * s, -4 * s)), K.add(C, (4 * s, -4 * s))
    tops = {}
    for c, r in ((0.05, ra), (0.30, ra), (0.58, rb)):
        tops[c] = at(c, -1)
        d.line(tops[c], r, "detail")
    # brake line: trailing edge to the handle on the rear riser, hands fully up
    tip = at(1, 0)
    hand = K.add(C, (14 * s, -28 * s))
    d.line(tip, hand, "detail")
    d.poly([K.add(hand, (-4 * s, -1 * s)), K.add(hand, (4 * s, -1 * s)), K.add(hand, (4 * s, 9 * s)),
            K.add(hand, (-4 * s, 9 * s))], "outline", closed=True, fill="card")
    d.spline([P(8, -18), P(14, -10), K.add(hand, (0, 7 * s))], "outline", tension=.4)
    # speed bar: at the feet, on lines up to the A risers
    bar = K.add(feet, (-10 * s, 4 * s))
    d.line(K.add(bar, (-9 * s, 2 * s)), K.add(bar, (9 * s, -2 * s)), "outline")
    d.spline([ra, K.add(C, (-24 * s, 10 * s)), bar], "hair", tension=.4)
    # the lift resultant (orange), up from about a quarter of the chord, and its shift forward
    lp = at(0.28, 0)
    top = K.add(lp, nv, 74 * s)
    d.arrow(K.add(lp, nv, 6 * s), top, "accent", 10)
    sh0 = K.add(lp, nv, 50 * s)
    d.arrow(sh0, K.add(sh0, fwd, 30 * s), "accent", 7)
    # angle of attack: from the level air to the chord line, at the nose
    a_ch = math.degrees(math.atan2(fwd[1], fwd[0])) % 360
    RA = 150 * s
    d.arc(le, RA, RA, 180, a_ch, "accent")
    for ang, dirn in ((180, 1), (a_ch, -1)):
        pt = (le[0] + RA * math.cos(math.radians(ang)), le[1] + RA * math.sin(math.radians(ang)))
        tang = (-math.sin(math.radians(ang)) * dirn, math.cos(math.radians(ang)) * dirn)
        d.head(pt, tang, 7, accent=True)
    ret = dict(C=C, le=le, te=te, hand=hand, lp=lp, top=top, sh0=sh0, fwd=fwd, dv=dv, nv=nv, bar=bar,
               tops=tops, ra=ra, rb=rb, tip=tip, at=at)
    if not labels:
        return ret
    # ---- labels: the page's own words ---------------------------------------
    d.callout(at(0.74, 1), K.add(at(0.74, 1), (40 * s, -30 * s)), "Profile")
    d.callout(le, K.add(le, (-24 * s, 44 * s)), "Nose", anchor="end")
    d.callout(te, K.add(te, (8, 30)) if narrow else K.add(te, (14 * s, 40 * s)), "Trailing edge")
    ma = K.lerp(tops[0.05], ra, .42)
    d.callout(ma, K.add(ma, (-44 * s, 0)), "A lines", anchor="end")
    mb = K.lerp(tops[0.58], rb, .55)
    d.callout(mb, K.add(mb, (-34 * s, 34 * s)), "B lines", anchor="end")
    mk = K.lerp(tip, hand, .5)
    d.callout(mk, K.add(mk, (40 * s, 0)), "Brake line")
    d.callout(bar, K.add(bar, (-30 * s, 30 * s)), "Speed bar", anchor="end")
    d.text(K.add(top, (10, 2)), "Lift resultant", "lab")
    d.text(K.add(top, (10, 18)), "moves forward as the", "sub")
    d.text(K.add(top, (10, 32)), "angle of attack falls", "sub")
    mid_a = math.radians((180 + a_ch) / 2)
    ap = (le[0] + (RA + 4 * s) * math.cos(mid_a), le[1] + (RA + 4 * s) * math.sin(mid_a))
    d.text(K.add(ap, (-2 * s, -30 * s)), "Angle of attack", "val", "start")
    d.line(K.add(ap, (0, -4 * s)), K.add(ap, (0, -24 * s)), "hair")
    return ret


def detail_brake(d, c, r, s=1.0, text_out=False):
    """Detail D: the brake handle, magnified. Hands fully up, then the first
    tension, at least 7 cm lower (Tom Lolies, Episode 66, chapter 12)."""
    d.circle(c, r, "hair")
    x = c[0] - (14 if text_out else 44) * s
    # the rear riser, a strap
    d.poly([(x - 3 * s, c[1] - r * .92), (x - 3 * s, c[1] + r * .92)], "outline")
    # the pulley on it, and the brake line coming down from the wing through it
    pul = (x + 6 * s, c[1] - 34 * s)
    d.circle(pul, 5 * s, "outline", fill="card")
    d.line((x + 11 * s, c[1] - r * .9), (x + 11 * s, pul[1]), "detail")
    # the handle, hands fully up: just under the pulley
    def toggle(top, w):
        d.path(K.catmull([K.add(top, (-6 * s, 0)), K.add(top, (6 * s, 0)), K.add(top, (9 * s, 12 * s)),
                          K.add(top, (6 * s, 26 * s)), K.add(top, (-6 * s, 26 * s)), K.add(top, (-9 * s, 12 * s))],
                         closed=True, tension=.45), w, fill="card" if w == "outline" else None)
    up = (x + 11 * s, pul[1] + 12 * s)
    d.line((x + 11 * s, pul[1] + 5 * s), up, "detail")
    toggle(up, "outline")
    low = (up[0], up[1] + 40 * s)
    d.line(K.add(up, (0, 26 * s)), low, "ghost")
    toggle(low, "ghost")
    d.dim((up[0] + 9 * s, up[1]), (low[0] + 9 * s, low[1]), -18 * s, "", ext=True, gap=2)
    lx = c[0] + r + 14 if text_out else up[0] + 36 * s
    lines = ["hands fully up", "to the first tension"] if text_out else ["hands fully up", "to the first", "tension"]
    d.text((lx, up[1] + 16 * s), "\u2265 7 cm", "val")
    for i, t in enumerate(lines):
        d.text((lx, up[1] + 16 * s + 16 + 14 * i), t, "sub")


def front_view(d, o, s=1.0):
    """Front view: the canopy's arc (an ellipse, thinning to the tips), the
    lines fanning to the two risers, the pilot between them."""
    cx, cy = o[0] + 190 * s, o[1] + 210 * s
    A, B = 170 * s, 128 * s
    TM = 74
    def mid(t):
        t = math.radians(t)
        return (cx + A * math.sin(t), cy - B * math.cos(t))
    def nrm(t):
        t = math.radians(t)
        v = (B * math.sin(t), -A * math.cos(t))
        return K.unit(v)
    def thick(t):
        return 16 * s * max(0.0, 1 - (t / TM) ** 2) ** 0.4 + 1.2 * s
    ts = [-TM + i * (2 * TM) / 60 for i in range(61)]
    outer = [K.add(mid(t), nrm(t), thick(t) / 2) for t in ts]
    inner = [K.add(mid(t), nrm(t), -thick(t) / 2) for t in ts[::-1]]
    d.path(K.catmull(outer + inner, closed=True, tension=.3), "outline", fill="card")
    for t in [-TM + 6 + i * (2 * TM - 12) / 22 for i in range(23)]:
        d.line(K.add(mid(t), nrm(t), -thick(t) * .42), K.add(mid(t), nrm(t), thick(t) * .42), "hair")
    riser = {-1: (cx - 10 * s, cy + 208 * s), 1: (cx + 10 * s, cy + 208 * s)}
    for i, t in enumerate([-TM + 8 + k * (2 * TM - 16) / 17 for k in range(18)]):
        side = -1 if t < 0 else 1
        p = K.add(mid(t), nrm(t), -thick(t) / 2)
        d.line(p, riser[side], "detail" if i % 3 == 0 else "hair")
    Cc = (cx, cy + 222 * s)
    d.line((cx, cy - B - 26 * s), (cx, cy + 270 * s), "centre")
    d.circle((cx, cy + 196 * s), 9 * s, "outline", fill="card")
    d.spline([(cx - 16 * s, cy + 212 * s), (cx - 20 * s, cy + 240 * s), (cx, cy + 250 * s),
              (cx + 20 * s, cy + 240 * s), (cx + 16 * s, cy + 212 * s)], "outline", closed=True, fill="card", tension=.5)
    for side in (-1, 1):
        d.line(riser[side], (cx + side * 14 * s, cy + 214 * s), "detail")
    return dict(top=mid(0), C=Cc)


def plan_view(d, o, s=1.0, labels=True, te_right=False):
    """Plan view from above, nose up: a nearly straight leading edge swept back
    at the tips, a curved trailing edge, the chord falling off elliptically."""
    cx, cy = o[0] + 190 * s, o[1] + 40 * s
    HS, CM = 178 * s, 70 * s
    n = 40
    ys = [math.sin(math.pi / 2 * (-1 + 2 * i / n)) for i in range(n + 1)]     # denser at the tips
    def chord(y):
        return CM * max(0.0, 1 - y * y) ** 0.5
    lead = [(cx + HS * y, cy + 26 * s * abs(y) ** 3) for y in ys]
    trail = [(lead[i][0], lead[i][1] + chord(y)) for i, y in enumerate(ys)]
    d.path(K.catmull(lead + trail[::-1][1:-1], closed=True, tension=.35), "outline", fill="card")
    # the cell walls: a hairline at each rib, spaced evenly along the span
    for k in range(1, 26):
        y = -1 + 2 * k / 26
        x = cx + HS * y
        ly = cy + 26 * s * abs(y) ** 3
        d.line((x, ly + 2.5 * s), (x, ly + chord(y) - 2.5 * s), "hair")
    d.line((cx, cy - 22 * s), (cx, cy + CM + 22 * s), "centre")
    ret = dict(lead=lead, trail=trail, cx=cx, cy=cy)
    if labels:
        p = lead[29]
        d.callout(p, K.add(p, (30 * s, -26 * s)), "Nose")
        q = trail[14]
        if te_right:
            q = trail[18]
            d.callout(q, K.add(q, (20 * s, 30 * s)), "Trailing edge", anchor="start")
        else:
            d.callout(q, K.add(q, (-26 * s, 30 * s)), "Trailing edge", anchor="end")
    return ret


def detail_mark(d, c, r, letter):
    """The circle on a view that a detail view magnifies, with its letter."""
    d.circle(c, r, "ghost")
    d.text((c[0] + r * .74 + 4, c[1] - r * .74), letter, "vn")


# ---------------------------------------------------------------- the figure
TITLE = "A paraglider in three views"
DESC = ("Technical drawing of a paraglider in three views. Side view: the profile with its nose and "
        "trailing edge, the A lines, B lines and brake line to the pilot, the speed bar, the angle of "
        "attack, and the lift resultant, which moves forward as the angle of attack falls. The brake "
        "handle is shown hands fully up and again at the first tension, at least 7 cm lower. Front "
        "view: the canopy's arc and the lines to the risers. Plan view: the planform from above. "
        "Not to scale.")
SOURCE = ("Tom Lolies", "Episode 66, chapter 12")


def three_view(layout="wide"):
    if layout == "wide":
        d = K.Drawing(1200, 660, "tv", TITLE, DESC)
        d.frame()
        sv = side_view(d, (70, 40), 1.0)
        d.backdrop(glow=sv["lp"], glow_r=330)
        detail_mark(d, K.add(sv["hand"], (0, 4)), 26, "D")
        d.view((60, 628), "A", "Side view")
        plan_view(d, (700, 26), 1.12)
        d.view((740, 210), "C", "Plan view")
        front_view(d, (604, 206), 0.8)
        d.view((640, 628), "B", "Front view")
        detail_brake(d, (1034, 352), 92, 1.3)
        d.view((980, 472), "D", "Detail, brake handle")
        d.title_block(930, 508, 242, "Paraglider, three views", [
            ("Brake", "Tom Lolies, Ep. 66, ch. 12"),
            ("Profile", "Luc Armant, Tom Lolies"),
            ("Scale", "Not to scale")])
    else:
        d = K.Drawing(390, 1250, "tvn", TITLE, DESC, compact=True)
        d.frame(4)
        sv = side_view(d, (22, 4), 0.62, narrow=True)
        d.backdrop(glow=sv["lp"], glow_r=240, grid=30)
        detail_mark(d, K.add(sv["hand"], (0, 3)), 17, "D")
        d.view((20, 392), "A", "Side view")
        detail_brake(d, (118, 504), 84, 1.05, text_out=True)
        d.view((20, 616), "D", "Detail, brake handle")
        front_view(d, (77, 616), 0.62)
        d.view((20, 944), "B", "Front view")
        plan_view(d, (24, 975), 0.9, te_right=True)
        d.view((20, 1134), "C", "Plan view")
        d.title_block(16, 1158, 358, "Paraglider, three views", [
            ("Brake", "Tom Lolies, Episode 66, chapter 12"),
            ("Profile", "Luc Armant, Tom Lolies"),
            ("Scale", "Not to scale")])
    return d.svg()


if __name__ == "__main__":
    print(len(three_view("wide")), len(three_view("narrow")))
