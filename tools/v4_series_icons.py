#!/usr/bin/env python3
"""
The library's series tiles redrawn as drawing sheets (owner, 1 Oct 2026: "yes"
to a before/after sample). In place of an embossed glyph on a grained stone:
a miniature of the series' own knowledge base drawing, in the kit's lines, on
a faint drafting grid, one orange element for what the series is about, and a
title block naming the sheet, the category and the episode count.

Sample first (four tiles), the rest once the owner picks:

    python3 tools/v4_series_icons.py      # writes prototypes/v4/samples/series-icons.html

The "before" pictures are the live v4 tiles, captured from library.html.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402
import v4_samples as SM  # noqa: E402
from v4_computed import P, naca, flow  # noqa: E402

f = K.f
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
W, H = 200, 138

# name, sheet number (the library's order), category, episodes: as the library page states them
SERIES = {
    "Flight Mechanics": ("12", "Technical", 7),
    "Sky Gods": ("03", "Core series", 4),
    "Weather Patterns": ("08", "Meteorology", 1),
    "Risk vs Reward": ("01", "Competitions", 12),
}


def sheet(name, desc):
    """The tile: grid, corner ticks and the title block; the drawing goes in between."""
    no, cat, n = SERIES[name]
    d = K.Drawing(W, H, "si-" + name.lower().replace(" ", "-"), name, desc, inline_css=False)
    d.backdrop(glow=(140, 50), glow_r=90, grid=10)
    for (x, y, dx, dy) in ((6, 6, 1, 1), (W - 6, 6, -1, 1), (6, H - 6, 1, -1), (W - 6, H - 6, -1, -1)):
        d.poly([(x + dx * 9, y), (x, y), (x, y + dy * 9)], "hair")
    d.line((6, H - 22), (W - 6, H - 22), "hair")
    lab = ('<text x="%s" y="%s"%s style="font-size:6.2px;font-weight:600;letter-spacing:.14em;fill:#8d8d8d">%s</text>')
    d.raw(lab % (10, H - 11, "", "SHEET " + no))
    d.raw(lab % (W - 10, H - 11, ' text-anchor="end"', "%s · %d EP" % (cat.upper(), n)))
    return d


def flight_mechanics():
    d = sheet("Flight Mechanics", "A wing section with the air flowing round it and the lift arrow where the lift acts.")
    up, lo = naca(.14, .045, .35, 80)
    x0, y0, c = 46, 70, 112
    U = [(x0 + c * x, y0 - c * y) for x, y in up]
    L = [(x0 + c * x, y0 - c * y) for x, y in lo]
    for k, dy in enumerate((-34, -20, 16, 30)):
        bump = -14 if dy < 0 else -5
        pts = [(8 + i * 4.6, y0 + dy + bump * math.exp(-((8 + i * 4.6 - (x0 + c * .35)) / 46) ** 2) * (1 if dy < 0 else .6))
               for i in range(41)]
        d.poly(pts, "ghost" if abs(dy) > 25 else "detail")
        if dy == -20:
            flow(d, pts, "#f6f4f4", .55, slow=True)
    d.path("M" + " L".join("%s,%s" % (f(a), f(b)) for a, b in U + L[::-1]) + " Z", "outline", fill="card")
    cp = (x0 + c * .37, y0 - c * .075)
    d.dot(cp, 2.6, True)
    d.arrow(cp, (cp[0], cp[1] - 34), "accent", 7)
    return d


def sky_gods():
    d = sheet("Sky Gods", "Big mountains, a pilot circling up in thermals to where they stop, then straight up in wave.")
    ridge = [(6, 104), (34, 78), (52, 90), (82, 46), (104, 72), (124, 58), (150, 86), (178, 64), (194, 80)]
    d.poly(ridge + [(194, 116), (6, 116)], "detail", True, "card")
    cx = 96
    spiral = [(cx + 9 * math.sin(t * 2 * math.pi * 6) * (1 - .25 * t), 86 - 50 * t) for t in [i / 160 for i in range(161)]]
    d.poly(spiral, "outline")
    d.path("M%s,36 H%s" % (f(cx - 26), f(cx + 46)), "accent", extra=' style="stroke-dasharray:3 3"')
    d.line((cx, 36), (cx + 4, 14), "accent")
    d.head((cx + 4.6, 10), (1, -7), 6, True)
    flow(d, [(cx, 36), (cx + 4, 14)], "#f6f4f4", .7)
    return d


def weather_patterns():
    d = sheet("Weather Patterns", "A sounding: temperature against height, leaning over until a kink where climbs stop, the dew point close below cloud base.")
    x0, x1, y0, y1 = 30, 182, 108, 14
    d.line((x0, y0), (x1, y0), "hair")
    d.line((x0, y0), (x0, y1), "hair")
    for k in range(5):
        a = x0 + 30 + k * 34
        d.path("M%s,%s L%s,%s" % (f(a), f(y0), f(a - 60), f(y1)), "ghost")
    T = lambda t, z: (x0 + (t + 2) / 32 * (x1 - x0), y0 - z / 3500 * (y0 - y1))
    mid = [(27.5, 0), (21, 700), (14.5, 1400), (8.3, 2100), (5.3, 2550), (5.8, 2800), (2.5, 3500)]
    dew = [(12, 0), (10.3, 1000), (8.8, 1700), (5.4, 2250), (2.0, 2650), (-1.5, 3100), (-2, 3500)]
    d.poly([T(*p) for p in dew], "outline")
    d.poly([T(*p) for p in mid], "accent")
    flow(d, [T(*p) for p in mid], "#f6f4f4", .5, slow=True)
    k = T(5.3, 2550)
    d.circle(k, 4, "accent")
    zb = T(19, 2250)
    for dx, dy, r in ((0, -6, 8), (-9, -3, 6), (9, -3, 6.5)):
        d.raw('<circle cx="%s" cy="%s" r="%s" fill="#f6f4f4" fill-opacity=".1"/>' % (f(zb[0] + dx), f(zb[1] + dy), f(r)))
    return d


def risk_vs_reward():
    d = sheet("Risk vs Reward", "A valley in section: one line climbs first and crosses high over landable fields; the other goes straight across, low, over a gorge.")

    def g(x):
        y = 104 - 30 * math.exp(-((x - 24) / 16) ** 2) - 44 * math.exp(-((x - 192) / 22) ** 2)
        y += 18 * max(0, math.sin((x - 70) / 14)) ** 3 * math.exp(-((x - 96) / 22) ** 2)
        return y
    xs = [6 + i * 2 for i in range(95)]
    d.poly([(x, g(x)) for x in xs] + [(194, 116), (6, 116)], "detail", True, "card")
    for a, b in ((44, 64), (122, 142), (150, 168)):
        d.line((a, g((a + b) / 2) - 1), (b, g((a + b) / 2) - 1), "outline")
    L = (24, g(24) - 3)
    helix = [(30 + i * .1 + 5 * math.sin(i / 8), L[1] - 4 - i * .32) for i in range(80)]
    d.poly(helix, "detail")
    top = helix[-1]
    d.spline([top, (70, top[1] - 5), (120, top[1] + 4), (160, 48), (186, g(186) - 4)], "outline", tension=.45)
    d.head((186, g(186) - 4), (1, 1.2), 6)
    fast = [(L[0] + i * 1.0, L[1] + 8 * math.sin(i / 70 * math.pi / 2) + i * .12) for i in range(71)]
    d.poly(fast, "accent")
    flow(d, fast, "#f6f4f4", .6)
    d.head(fast[-1], (1, .4), 6, True)
    d.circle((L[0] + 6, L[1] - 6), 5, "accent")
    d.dot((L[0] + 6, L[1] - 6), 1.8, True)
    return d


DRAW = {"Flight Mechanics": flight_mechanics, "Sky Gods": sky_gods, "Weather Patterns": weather_patterns,
        "Risk vs Reward": risk_vs_reward}

CSS = SM.SPEC_CSS + """
.si-sec{padding:var(--sp-5) var(--gutter);max-width:1240px;margin:0 auto;}
.si-sec h2{font-family:var(--font-display);font-size:var(--fs-h2);color:var(--white);margin:0 0 var(--sp-1);}
.si-sec>p{color:var(--gray-light);max-width:70ch;line-height:1.7;margin:0 0 var(--sp-3);}
.si-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-3);}
@media (max-width:900px){.si-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
.si-tile h3{font-family:var(--font-display);font-size:var(--fs-h4);color:var(--white);margin:.7rem 0 .2rem;}
.si-tile .meta{font-size:var(--fs-small);color:var(--gray);}
.si-shot{aspect-ratio:200/138;background:#141519;border:1px solid var(--line);overflow:hidden;}
.si-shot img,.si-shot svg{display:block;width:100%;height:100%;}
.si-lab{display:inline-block;font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gray);margin-bottom:var(--sp-2);}
.si-lab.is-new{color:var(--orange);}
"""


def tile(name, shot):
    no, cat, n = SERIES[name]
    return ('<div class="si-tile"><div class="si-shot">%s</div><h3>%s</h3><div class="meta">%d episode%s in %s</div></div>'
            % (shot, name, n, "" if n == 1 else "s", cat))


def page():
    order = ["Risk vs Reward", "Sky Gods", "Weather Patterns", "Flight Mechanics"]
    before = "".join(tile(n, '<img src="samples/img/series-before-%s.jpg" alt="" width="336" height="230">'
                          % n.lower().replace(" ", "-")) for n in order)
    after = "".join(tile(n, DRAW[n]().svg().replace('<svg class="dk ', '<svg class="kbd dk ', 1)) for n in order)
    body = ('<header class="kit-hero is-sky v2-page-hero"><div class="kit-hero-copy"><span class="kit-kicker">Sample, not live</span>'
            '<h1>Series tiles, redrawn</h1><p class="kit-intro">Four of the library\'s thirteen series tiles, as they are and '
            'as drawing sheets: a miniature of each series\' own knowledge base drawing, one orange element for what the '
            'series is about, and a title block. Pick a direction before the rest are redrawn.</p></div></header>'
            '<section class="si-sec"><span class="si-lab">Today</span><h2>Embossed glyphs on stone</h2>'
            '<p>Generic symbols (scales, a target, arcs), the same grey on every tile, on a grained stone with orange corner brackets.</p>'
            '<div class="si-grid">%s</div></section>'
            '<section class="si-sec"><span class="si-lab is-new">Redrawn</span><h2>Drawing sheets</h2>'
            '<p>Risk vs Reward: the decision, climb first or straight across over the gorge. Sky Gods: thermals to 7,600 m, '
            'then the wave. Weather Patterns: the sounding with its kink. Flight Mechanics: the wing section and its lift. '
            'Each draws itself in as it comes into view, with the air, the wave or the line still moving; still under reduced '
            'motion.</p><div class="si-grid">%s</div></section>') % (before, after)
    return SM.shell("Series tiles, redrawn", "Four library series tiles as drawing sheets: a before and after sample.", body, CSS)


def main():
    out = os.path.join(V4, "samples", "series-icons.html")
    open(out, "w", encoding="utf-8").write(page())
    print("v4 series icons: samples/series-icons.html")


if __name__ == "__main__":
    main()
