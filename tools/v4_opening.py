#!/usr/bin/env python3
"""
The home page's opening (owner, 1 Oct 2026: "go", the Awwwards list): over the
hero footage, the ground drawn in the Gold line: two ranges, the
far one faint, the near one solid in the page's own colour so the hero runs
into the page, engraved shading on the slopes, and one orange line, a flight
leaving a launch on the middle range and climbing out of the picture.

It draws itself in as the page opens (v2-immersive.js part 11), and as the
page scrolls the ground drops away under the reader, the near range fastest
(v2.css, scroll-driven, nothing for reduced motion). No words, no facts: a
drawing of ridges and a climb.

    python3 tools/v4_opening.py     # writes the drawing into prototypes/v4/index.html
"""
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "prototypes", "v4", "index.html")
W, H = 1600, 700
MARK = ("<!-- v4-opening: tools/v4_opening.py -->", "<!-- /v4-opening -->")


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def P(pts, close=False):
    return "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts) + (" Z" if close else "")


def smooth(pts, t=.5):
    n = len(pts)
    p = [pts[0]] + pts + [pts[-1]]
    d = "M%s,%s" % (f(pts[0][0]), f(pts[0][1]))
    for i in range(1, n):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += " C%s,%s %s,%s %s,%s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return d


def ridge(anchors, rough, seed, levels=5):
    """A ridgeline by midpoint displacement between hand-set anchors (peaks and
    saddles): jagged like rock at every scale, the same every build."""
    import random
    rnd = random.Random(seed)
    pts = list(anchors)
    amp = rough
    for _ in range(levels):
        nxt = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            m = ((x0 + x1) / 2, (y0 + y1) / 2 + rnd.uniform(-amp, amp) * (x1 - x0) / 100)
            nxt += [m, (x1, y1)]
        pts = nxt
        amp *= .56
    return pts


def hatch(cid, clip, ang, gap, op, box):
    """Engraving: parallel hairlines inside a shape (clipped, and cut to its box to keep the file small)."""
    a = math.radians(ang)
    dx, dy, nx, ny = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = math.hypot(x1 - x0, y1 - y0) / 2 + 2
    d, o = "", -R
    while o <= R:
        px, py = cx + nx * o, cy + ny * o
        seg = cut((px - dx * R, py - dy * R), (px + dx * R, py + dy * R), box)
        if seg:
            d += "M%s,%s L%s,%s " % (f(seg[0][0]), f(seg[0][1]), f(seg[1][0]), f(seg[1][1]))
        o += gap
    return ('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, clip),
            '<path clip-path="url(#%s)" d="%s" fill="none" stroke="#f6f4f4" stroke-opacity="%s" stroke-width=".6" '
            'vector-effect="non-scaling-stroke"/>' % (cid, d.strip(), op))


def cut(a, b, box):
    x0, y0, x1, y1 = box
    ddx, ddy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-ddx, a[0] - x0), (ddx, x1 - a[0]), (-ddy, a[1] - y0), (ddy, y1 - a[1])):
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
    return (a[0] + t0 * ddx, a[1] + t0 * ddy), (a[0] + t1 * ddx, a[1] + t1 * ddy)


def line(d, stroke, w, op=1, cls=""):
    return ('<path%s d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-opacity="%s" stroke-linecap="round" '
            'stroke-linejoin="round" vector-effect="non-scaling-stroke"/>' % (' class="%s"' % cls if cls else "", d, stroke, w, op))


def build():
    defs, far_g, near_g, sky_g = [], [], [], []
    defs.append('<linearGradient id="op-ln" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="%d" y2="0">'
                '<stop offset="0" stop-color="#f6f4f4" stop-opacity=".35"/><stop offset=".55" stop-color="#f6f4f4"/>'
                '<stop offset="1" stop-color="#ffcf94"/></linearGradient>' % W)
    defs.append('<radialGradient id="op-glow" gradientUnits="userSpaceOnUse" cx="1250" cy="480" r="430">'
                '<stop offset="0" stop-color="#ff7517" stop-opacity=".16"/><stop offset="1" stop-color="#ff7517" stop-opacity="0"/></radialGradient>')

    # low on the left, where the words sit; the ranges rise to the right
    far = ridge([(0, 560), (260, 520), (520, 420), (700, 470), (930, 300), (1120, 380), (1330, 250), (1480, 330), (1600, 300)], 14, 7)
    near = ridge([(0, 690), (380, 660), (700, 600), (900, 560), (1060, 470), (1180, 500), (1300, 380), (1420, 455), (1600, 420)], 11, 3)

    # far: a faint line and two contours below it, the sky showing through
    far_g.append('<path d="%s L%d,%d L0,%d Z" fill="#141519" fill-opacity=".35"/>' % (P(far), W, H, H))
    for k in (1, 2):
        far_g.append(line(P([(x, y + 22 * k) for x, y in far]), "#f6f4f4", .5, .12 / k))
    far_g.append(line(P(far), "url(#op-ln)", 1, .8))

    # the launch and the climb: off the middle range, out of the picture
    li = min(range(len(near)), key=lambda i: abs(near[i][0] - 1300))
    L = near[li]
    # off the launch, round in a thermal four times, tightening as it climbs, then away to the left
    climb = [L]
    cx = L[0] - 70
    for i in range(1, 4 * 24 + 1):                          # four turns, every 15 degrees, narrowing as it climbs
        t = i / 24.0
        r = 44 * (1 - .14 * t)
        a = -math.pi / 2 + t * 2 * math.pi
        climb.append((cx + r * math.cos(a) * 1.0, L[1] - 40 - 62 * t + r * .28 * math.sin(a)))
    top = climb[-1]
    climb += [(top[0] - 120, top[1] - 40), (top[0] - 360, top[1] - 120), (top[0] - 640, -30)]
    sky_g.append(line(smooth(climb, .5), "#ff7517", 1.6, 1))
    sky_g.append('<path class="fl fl-slow" d="%s" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.2" '
                 'stroke-linecap="round" vector-effect="non-scaling-stroke"/>' % smooth(climb, .5))
    sky_g.append('<circle cx="%s" cy="%s" r="5" fill="#ff7517"/>' % (f(L[0]), f(L[1] - 2)))
    sky_g.append('<circle cx="%s" cy="%s" r="11" fill="none" stroke="#ff7517" stroke-opacity=".6" stroke-width="1" '
                 'vector-effect="non-scaling-stroke"/>' % (f(L[0]), f(L[1] - 2)))

    # near: solid in the page's colour, so the hero runs into the page below it
    nd = P(near) + " L%d,%d L0,%d Z" % (W, H, H)
    near_g.append('<path d="%s" fill="#141519"/>' % nd)
    top = min(y for _, y in near)
    c, h = hatch("op-h2", nd, 112, 6, .13, (0, top, W, H))
    defs.append(c)
    near_g.append(h)
    for (x0, y0), (x1, y1) in zip(near[::8], near[8::8]):     # gullies down the faces
        if y1 > y0 + 8:
            near_g.append(line(P([(x1, y1), (x1 + 14, y1 + 60), (x1 + 6, y1 + 120)]), "#f6f4f4", .5, .16))
    near_g.append(line(P(near), "url(#op-ln)", 1.6, 1))

    svg = ('<svg class="kbd dk v4-ridge" viewBox="0 0 %d %d" preserveAspectRatio="xMaxYMax slice" aria-hidden="true" '
           'focusable="false" xmlns="http://www.w3.org/2000/svg"><defs>%s</defs>'
           '<rect width="%d" height="%d" fill="url(#op-glow)"/>'
           '<g class="op-far">%s</g><g class="op-sky">%s</g><g class="op-near">%s</g></svg>'
           % (W, H, "".join(defs), W, H, "".join(far_g), "".join(sky_g), "".join(near_g)))
    return svg


def main():
    src = open(PAGE, encoding="utf-8").read()
    block = MARK[0] + "\n  " + build() + "\n  " + MARK[1]
    if MARK[0] in src:
        src = src[:src.index(MARK[0])] + block + src[src.index(MARK[1]) + len(MARK[1]):]
    else:
        anchor = '<header class="kit-hero v2-home-hero">'
        i = src.index(anchor)
        j = src.index("</div>", src.index('<div class="kit-hero-media">', i)) + len("</div>")
        src = src[:j] + "\n  " + block + src[j:]
    open(PAGE, "w", encoding="utf-8").write(src)
    print("v4 opening: %d bytes in index.html" % len(block))


if __name__ == "__main__":
    main()
