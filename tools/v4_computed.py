#!/usr/bin/env python3
"""
The computed lens (tools/v4_lens.py): drawings whose subject is physics the
page states, worked out rather than sketched. Each keeps the page's own
numbers as the labels and draws the computation beside them:

  kb-sky-gods-speed               trim speed with height: Antoine Girard's
                                  figures on the curve that thin air alone
                                  gives (ISA density, true airspeed)
  kb-weather-patterns-millibars   the rule of thumb (every 100 mb about
                                  1,000 m) on the standard atmosphere's
                                  pressure-height curve
  kb-weather-patterns-resolution  the three model resolutions as areas to
                                  scale, one kilometre the same everywhere
  kb-new-technologies-airfoil     the two sections as real four-digit
                                  profiles at the thicknesses the page gives

Each has a phone version (stacked, at reading size).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402

f = K.f


def P(pts):
    return " ".join("%s,%s" % (f(x), f(y)) for x, y in pts)


def flow(d, pts, color="#f6f4f4", op=.75, slow=False):
    """A moving dash laid over a line (class fl, animated by the page's CSS; still when motion is reduced)."""
    d.raw('<path class="fl%s" d="M%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="1.4" stroke-linecap="round" '
          'vector-effect="non-scaling-stroke"/>' % (" fl-slow" if slow else "", " L".join("%s,%s" % (K.f(x), K.f(y)) for x, y in pts),
                                                   color, op))


def rect(d, x, y, w, h, cls="fa", op=None):
    d.raw('<rect class="%s" x="%s" y="%s" width="%s" height="%s"%s/>' % (
        cls, f(x), f(y), f(w), f(h), ' style="fill-opacity:%s"' % op if op is not None else ""))


# ---------------------------------------------------------------- the standard atmosphere (ICAO, troposphere)
def isa(h):
    """(pressure hPa, density kg/m3) at geopotential height h metres."""
    T = 288.15 - 0.0065 * h
    p = 101325 * (T / 288.15) ** 5.25588
    return p / 100, p / (287.053 * T)


def isa_height(hpa):
    return (1 - (hpa / 1013.25) ** (1 / 5.25588)) * 288.15 / 0.0065


def tas(h, v0=40.0, h0=2000.0):
    """True airspeed at h for a wing that flies v0 at h0: the same indicated speed, thinner air."""
    return v0 * math.sqrt(isa(h0)[1] / isa(h)[1])


# ---------------------------------------------------------------- sky gods: trim speed with height
GIRARD = [(2000, 40, "2,000 m", "the speed you are used to"),
          (5000, 50, "about 5,000 m", "landing, you touch down at 25 to 30 km/h: hard to run it out"),
          (8000, 60, "8,000 m", "collapses and reactions come faster, and less oxygen slows the pilot")]
SPEED_DESC = ("Trim speed of the same wing against height. Antoine Girard's figures: about 40 km/h at 2,000 m, about 50 "
              "in the middle, about 60 at 8,000 m. The line is what thinner air alone gives, from the standard "
              "atmosphere: about 47 km/h at 5,000 m and 55 at 8,000 m. His figures run a little above it.")


def speed_chart(d, x0, y0, w, h, compact=False):
    """Height up the side (0 to 9,000 m), speed along the bottom (30 to 70 km/h)."""
    X = lambda v: x0 + (v - 30) / 40 * w
    Y = lambda m: y0 + h - m / 9000 * h
    for m in range(0, 9001, 1000):
        d.line((x0, Y(m)), (x0 + w, Y(m)), "ghost" if m % 2000 else "hair")
        if m % 2000 == 0:
            d.text((x0 - 8, Y(m) + 4), "{:,} m".format(m) if m else "0", "tb", "end")
    for v in range(30, 71, 10):
        d.line((X(v), y0 + h), (X(v), y0 + h + 5), "hair")
        d.text((X(v), y0 + h + 20), str(v), "tb", "middle")
    d.text((x0 + w, y0 + h + 38), "trim speed, km/h", "tb", "end")
    curve = [(X(tas(m)), Y(m)) for m in range(0, 9001, 150)]
    d.poly(curve, "detail")
    lx, ly = curve[-1]
    d.text((lx + 8, ly + 4 if not compact else ly - 10), "thin air alone", "sub", "start" if not compact else "end")
    for m, v, _, _ in GIRARD:
        if abs(X(v) - X(tas(m))) > 3:
            d.line((X(tas(m)), Y(m)), (X(v), Y(m)), "accent")
        d.dot((X(v), Y(m)), 5, True)
    return X, Y


def sky_speed():
    d = K.Drawing(1200, 400, "cs-speed", "The same wing, faster in thin air", SPEED_DESC, inline_css=False)
    d.backdrop(glow=(330, 160), glow_r=260, sheet=False)
    X, Y = speed_chart(d, 110, 40, 420, 300)
    for i, (m, v, alt, note) in enumerate(GIRARD[::-1]):
        y = 78 + 104 * i
        d.text((640, y), alt, "lab")
        d.text((640, y + 22), "about %d km/h" % v, "val")
        d.text((640, y + 42), note, "sub")
        d.poly([(X(v) + 8, Y(m)), (620, Y(m)), (630, y - 4)], "hair")
    d.text((1180, 388), "his figures, orange · the line: standard atmosphere, same wing", "tb", "end")
    return d


def sky_speed_p():
    d = K.Drawing(360, 660, "cs-speed-p", "The same wing, faster in thin air", SPEED_DESC, inline_css=False)
    speed_chart(d, 70, 30, 250, 300, compact=True)
    for i, (m, v, alt, note) in enumerate(GIRARD[::-1]):
        y = 420 + 86 * i
        d.dot((22, y - 4), 5, True)
        d.text((36, y), alt, "lab")
        d.text((36, y + 20), "about %d km/h" % v, "val")
        words, line, out = note.split(), "", []
        for wd in words:
            if len(line) + len(wd) > 44:
                out.append(line)
                line = wd
            else:
                line = (line + " " + wd).strip()
        out.append(line)
        for k, ln in enumerate(out):
            d.text((36, y + 38 + 14 * k), ln, "sub")
    d.text((344, 652), "the line: standard atmosphere", "tb", "end")
    return d


# ---------------------------------------------------------------- weather patterns: millibars to metres
MB = [(1000, "sea level"), (900, "about 1,000 m"), (800, "about 2,000 m"), (700, "about 3,000 m")]
MB_DESC = ("Millibars to metres, the rule of thumb: start at 1,000 millibars at sea level; every 100 millibars less is "
           "about 1,000 metres higher: 900 is about 1,000 m, 800 about 2,000 m and 700 about 3,000 m. Beside each, the "
           "standard atmosphere's height for that pressure: about 110, 990, 1,950 and 3,010 m. Forecasts give the wind "
           "at a pressure, because that is how balloons report it.")


def millibars():
    d = K.Drawing(1200, 330, "cs-mb", "Millibars to metres", MB_DESC, inline_css=False)
    d.backdrop(glow=(700, 160), glow_r=300, sheet=False)
    x0, x1 = 170, 1100
    X = lambda mb: x0 + (1000 - mb) / 300 * (x1 - x0)
    ya, yb = 110, 200
    d.line((x0 - 20, ya), (x1 + 20, ya), "hair")
    d.line((x0 - 20, yb), (x1 + 20, yb), "hair")
    d.text((x0 - 34, ya + 4), "pressure", "tb", "end")
    d.text((x0 - 34, yb + 4), "height", "tb", "end")
    # the standard atmosphere, drawn as a scale under the rule: where each height really falls
    Hs = lambda m: x0 + m / 3000 * (x1 - x0)
    for mb, lab in MB:
        x = X(mb)
        d.line((x, ya), (Hs(isa_height(mb)), yb), "accent")
        d.dot((x, ya), 5, True)
        d.dot((Hs(isa_height(mb)), yb), 4.5, False)
        d.text((x, ya - 20), "%d mb" % mb, "lab", "middle")
        d.text((Hs(isa_height(mb)), yb + 26), lab, "tv" if mb == 1000 else "val", "middle")
        d.text((Hs(isa_height(mb)), yb + 44), "standard: {:,} m".format(int(round(isa_height(mb), -1))), "sub", "middle")
    d.text(((x0 + x1) / 2, 50), "every 100 millibars less is about 1,000 metres higher", "sub", "middle")
    rect(d, X(900), 272, X(700) - X(900), 6, "fa", .35)
    d.text(((X(900) + X(700)) / 2, 298), "the range most flying forecasts need", "sub", "middle")
    d.text((1180, 322), "the slant: the standard atmosphere puts each pressure a little off the round number", "tb", "end")
    return d


def millibars_p():
    d = K.Drawing(360, 470, "cs-mb-p", "Millibars to metres", MB_DESC, inline_css=False)
    d.text((16, 24), "every 100 mb less", "vw")
    d.text((16, 40), "is about 1,000 m higher", "vw")
    y0, y1 = 400, 90                              # height runs up the screen
    Y = lambda m: y0 - m / 3000 * (y0 - y1)
    d.line((110, y0 + 10), (110, y1 - 20), "hair")
    d.head((110, y1 - 26), (0, -1), 8)
    for mb, lab in MB:
        y = Y(isa_height(mb))
        d.dot((110, y), 4.5, mb != 1000)
        d.text((96, y + 4), "%d mb" % mb, "lab", "end")
        d.text((126, y), lab, "tv" if mb == 1000 else "val")
        d.text((126, y + 16), "standard: {:,} m".format(int(round(isa_height(mb), -1))), "sub")
    rect(d, 104, Y(isa_height(700)), 3, Y(isa_height(900)) - Y(isa_height(700)), "fa", .5)
    d.text((16, 440), "900 to 700 mb: the range most", "sub")
    d.text((16, 456), "flying forecasts need", "sub")
    return d


# ---------------------------------------------------------------- weather patterns: model resolution, to scale
RES = [("GFS", 22, "about 22 km"), ("ECMWF", 9, "about 9 km"), ("NEMS", 4, "down to 4 km")]
RES_DESC = ("What a model's resolution means, as Ivelin Kalushkov explains it: the forecast for a point covers the area "
            "around it; if rain falls anywhere inside, the model counts itself right. His figures: GFS about 22 km, "
            "ECMWF about 9 km, NEMS down to 4 km. Each circle is that many kilometres across, all to one scale.")


def shower(d, x, y):
    for dx, dy, r in ((0, 0, 11), (-10, 5, 8), (10, 5, 8.5)):
        d.circle((x + dx, y + dy), r, "hair", fill="card")
    for k in range(4):
        d.line((x - 9 + k * 6, y + 16), (x - 11 + k * 6, y + 25), "hair")


def resolution():
    d = K.Drawing(1200, 360, "cs-res", "What a model's resolution means", RES_DESC, inline_css=False)
    d.backdrop(glow=(300, 170), glow_r=260, sheet=False)
    S = 10.0                                        # px per km, the same for all three: each circle is km across
    cy = 160
    for (name, km, lab), cx in zip(RES, (300, 700, 960)):
        r = km * S / 2
        d.raw('<circle cx="%s" cy="%s" r="%s" class="fa" style="fill-opacity:.08"/>' % (f(cx), f(cy), f(r)))
        d.circle((cx, cy), r, "accent")
        d.dot((cx, cy), 3.5, False)
        d.text((cx, cy + max(r, 30) + 26), name, "lab", "middle")
        d.text((cx, cy + max(r, 30) + 44), lab, "val", "middle")
    sx, sy = 300 + 11 * S * .7, cy - 11 * S * .6
    shower(d, sx, sy)
    d.poly([(sx + 16, sy - 6), (sx + 70, sy - 36), (sx + 84, sy - 36)], "hair")
    d.text((sx + 90, sy - 38), "rain here still counts", "lab")
    d.text((sx + 90, sy - 22), "as a correct forecast for the centre", "sub")
    d.line((1080, 300), (1080 + 10 * S, 300), "outline")
    d.text((1080 + 5 * S, 320), "10 km", "tb", "middle")
    d.text((1180, 350), "his figures, as he gives them · one scale", "tb", "end")
    return d


def resolution_p():
    d = K.Drawing(360, 560, "cs-res-p", "What a model's resolution means", RES_DESC, inline_css=False)
    S = 9.0
    cy, cx = 150, 150
    r = 22 * S / 2
    for (name, km, lab), (x, y) in zip(RES, ((cx, cy), (90, 330), (250, 330))):
        rr = km * S / 2
        d.raw('<circle cx="%s" cy="%s" r="%s" class="fa" style="fill-opacity:.08"/>' % (f(x), f(y), f(rr)))
        d.circle((x, y), rr, "accent")
        d.dot((x, y), 3.2, False)
        yl = y + max(rr, 24) + 22
        d.text((x, yl), name, "lab", "middle")
        d.text((x, yl + 18), lab, "val", "middle")
    sx, sy = cx + r * .72, cy - r * .62
    shower(d, sx, sy)
    d.text((16, 470), "Rain anywhere inside the circle still", "sub")
    d.text((16, 486), "counts as a correct forecast for the centre.", "sub")
    d.line((16, 520), (16 + 10 * S, 520), "outline")
    d.text((16 + 10 * S + 8, 524), "10 km · circles are km across", "tb")
    return d


# ---------------------------------------------------------------- new technologies: two sections, real profiles
def naca(t, m=.03, p=.35, n=120):
    """A cambered four-digit section: thickness t, camber m at p; upper and lower surfaces, nose to tail."""
    xs = [(1 - math.cos(math.pi * i / (n - 1))) / 2 for i in range(n)]
    up, lo = [], []
    for x in xs:
        yt = 5 * t * (.2969 * math.sqrt(x) - .126 * x - .3516 * x ** 2 + .2843 * x ** 3 - .1036 * x ** 4)
        yc = m / p ** 2 * (2 * p * x - x * x) if x < p else m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x * x)
        up.append((x, yc + yt))
        lo.append((x, yc - yt))
    return up, lo


SECTIONS = [(.105, [("A", .10), ("B", .33), ("C", .58), ("D", .82)], "Forty years ago", "profile about 9 to 12% of chord",
             "thin section, four rows to hold its shape"),
            (.18, [("AA", .30), ("BB", .62)], "Today", "profile about 18% of chord", "more volume, more pressure, fewer points")]
FOIL_DESC = ("Why two lines became possible. Two sections to the same chord: a profile of forty years ago, about 9 to 12% "
             "thick, with four rows of attachment points, and a modern profile near 18% with only two groups, AA pushed "
             "back. The shapes are four-digit profiles at those thicknesses.")


def section(d, x0, y0, C, t, pts, lab, sub, note, ty):
    up, lo = naca(t)
    U = [(x0 + C * x, y0 - C * y) for x, y in up]
    L = [(x0 + C * x, y0 - C * y) for x, y in lo]
    d.path("M" + " L".join("%s,%s" % (f(a), f(b)) for a, b in U + L[::-1]) + " Z", "outline", fill="card")
    for k in range(1, 12):                              # the ribs' stations, faint
        i = int(k / 12 * (len(U) - 1))
        d.line(U[i], L[i], "ghost")
    i_max = max(range(len(U)), key=lambda i: U[i][1] * -1 - L[i][1] * -1)
    d.dim(L[i_max], U[i_max], -16 if C < 300 else -22, "9–12%" if t < .15 else "%d%%" % round(t * 100))
    for name, fx in pts:
        i = min(range(len(L)), key=lambda i: abs(up[i][0] - fx))
        q = L[i]
        d.line(q, (q[0], q[1] + 44), "detail")
        d.dot(q, 4, True)
        d.text((q[0], q[1] + 62), name, "val", "middle")
    d.text((x0, ty), lab, "lab")
    d.text((x0, ty + 18), sub, "tv")
    d.text((x0, ty + 34), note, "sub")


def airfoil():
    d = K.Drawing(1200, 330, "cs-foil", "Two sections to the same chord", FOIL_DESC, inline_css=False)
    d.backdrop(glow=(860, 130), glow_r=280, sheet=False)
    for k, s in enumerate(SECTIONS):
        section(d, 80 + 580 * k, 120, 460, *s, ty=236)
    d.arrow((565, 120), (620, 120), "hair", 8)
    d.text((1180, 322), "four-digit profiles at the page's thicknesses · attachment points as the page gives them", "tb", "end")
    return d


def airfoil_p():
    d = K.Drawing(360, 470, "cs-foil-p", "Two sections to the same chord", FOIL_DESC, inline_css=False)
    for k, s in enumerate(SECTIONS):
        section(d, 30, 70 + 250 * k, 300, *s, ty=160 + 250 * k)
    return d


def registry():
    return {
        "kb-sky-gods-speed": (sky_speed, sky_speed_p),
        "kb-weather-patterns-millibars": (millibars, millibars_p),
        "kb-weather-patterns-resolution": (resolution, resolution_p),
        "kb-new-technologies-airfoil": (airfoil, airfoil_p),
    }


if __name__ == "__main__":
    for h in (2000, 5000, 8000):
        print(h, "m", round(tas(h), 1), "km/h")
    for mb in (1000, 900, 800, 700):
        print(mb, "mb", round(isa_height(mb)), "m")
