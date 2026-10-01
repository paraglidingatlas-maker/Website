#!/usr/bin/env python3
"""
Series tiles, second round (owner, 1 Oct 2026: "more vibrant and elegant
samples"). The same four series in four looks, so a direction can be picked:

  ember       luminous lines on deep night blue, the subject glowing
  dusk        painted: a sky running to a warm horizon, ridges in layers
  gold line   fine gradient lines, white into orange, and a lot of space
  colour      a colour field per category, white line art on top

Each tile shows the same idea as its series' knowledge base drawing. Geometry
is shared; only the treatment changes.

    python3 tools/v4_series_icons2.py   # writes prototypes/v4/samples/series-icons-2.html
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_samples as SM  # noqa: E402
from v4_computed import naca  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
W, H = 200, 138
SERIES = [("Risk vs Reward", "Competitions", 12), ("Sky Gods", "Core series", 4),
          ("Weather Patterns", "Meteorology", 1), ("Flight Mechanics", "Technical", 7)]


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def path(pts, close=False):
    return "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts) + (" Z" if close else "")


def smooth(pts, close=False, t=.5):
    """Catmull-Rom through the points, as cubic Beziers."""
    n = len(pts)
    p = [pts[-1]] + pts + [pts[0], pts[1]] if close else [pts[0]] + pts + [pts[-1]]
    d = "M%s,%s" % (f(pts[0][0]), f(pts[0][1]))
    for i in range(1, n if close else n):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += " C%s,%s %s,%s %s,%s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    if close:
        p0, p1, p2, p3 = p[n - 1], p[n], p[n + 1], p[n + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += " C%s,%s %s,%s %s,%s Z" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return d


# ---------------------------------------------------------------- the four ideas, as geometry
def risk():
    g = lambda x: (100 - 30 * math.exp(-((x - 26) / 16) ** 2) - 46 * math.exp(-((x - 190) / 22) ** 2)
                   + 20 * max(0, math.sin((x - 70) / 14)) ** 3 * math.exp(-((x - 96) / 22) ** 2))
    ground = [(x, g(x)) for x in range(0, 201, 4)]
    L = (26, g(26) - 4)
    climb = [(32 + i * .12 + 5 * math.sin(i / 7), L[1] - 4 - i * .34) for i in range(70)]
    top = climb[-1]
    safe = [top, (78, top[1] - 6), (126, top[1] + 2), (166, 46), (188, g(188) - 5)]
    fast = [(L[0] + i, L[1] + 7 * math.sin(i / 72 * math.pi / 2) + i * .13) for i in range(73)]
    fields = [((44, 62), g(53)), ((122, 140), g(131)), ((150, 166), g(158))]
    gorge = (96, g(96))
    return dict(ground=ground, climb=climb, safe=safe, fast=fast, fields=fields, decision=(L[0] + 6, L[1] - 7), gorge=gorge)


def sky():
    far = [(0, 92), (28, 70), (52, 80), (78, 54), (104, 66), (132, 48), (160, 70), (186, 58), (200, 66)]
    near = [(0, 108), (30, 84), (50, 94), (84, 52), (106, 76), (126, 64), (152, 92), (178, 74), (200, 88)]
    cx = 96
    spiral = [(cx + 9 * math.sin(t * 2 * math.pi * 6) * (1 - .3 * t), 84 - 48 * t) for t in [i / 180 for i in range(181)]]
    wave = [(cx, 36), (cx + 2, 24), (cx + 5, 12)]
    return dict(far=far, near=near, spiral=spiral, wave=wave, stop=36, cx=cx)


def weather():
    x0, x1, y0, y1 = 34, 178, 112, 16
    T = lambda t, z: (x0 + (t + 2) / 32 * (x1 - x0), y0 - z / 3500 * (y0 - y1))
    mid = [T(*p) for p in [(27.5, 0), (21, 700), (14.5, 1400), (8.3, 2100), (5.3, 2550), (5.8, 2800), (2.5, 3500)]]
    dew = [T(*p) for p in [(12, 0), (10.3, 1000), (8.8, 1700), (5.4, 2250), (2.0, 2650), (-1.5, 3100), (-2, 3500)]]
    adiab = [((x0 + 24 + k * 30, y0), (x0 + 24 + k * 30 - 58, y1)) for k in range(5)]
    return dict(mid=mid, dew=dew, kink=T(5.3, 2550), cloud=T(19, 2250), adiab=adiab, axes=(x0, x1, y0, y1))


def flight():
    up, lo = naca(.14, .045, .35, 70)
    x0, y0, c = 46, 74, 112
    U = [(x0 + c * x, y0 - c * y) for x, y in up]
    L = [(x0 + c * x, y0 - c * y) for x, y in lo]
    streams = []
    for dy in (-38, -24, -12, 16, 30):
        bump = -15 if dy < 0 else -5
        streams.append([(4 + i * 4.8, y0 + dy + bump * math.exp(-((4 + i * 4.8 - 86) / 44) ** 2) * (1.3 if dy == -12 else 1))
                        for i in range(41)])
    cp = (x0 + c * .37, y0 - c * .078)
    return dict(foil=U + L[::-1], streams=streams, cp=cp, lift=(cp[0], cp[1] - 36))


GEO = {"Risk vs Reward": risk, "Sky Gods": sky, "Weather Patterns": weather, "Flight Mechanics": flight}


# ---------------------------------------------------------------- treatments
def svg(ident, title, defs, body):
    return ('<svg class="kbd dk si2" viewBox="0 0 %d %d" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">'
            '<defs>%s</defs>%s</svg>' % (W, H, title, defs, body))


def S(d, stroke, w=1.4, op=1, extra=""):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-opacity="%s" stroke-linecap="round" '
            'stroke-linejoin="round" vector-effect="non-scaling-stroke"%s/>' % (d, stroke, w, op, extra))


def F(d, fill, op=1):
    return '<path d="%s" fill="%s" fill-opacity="%s"/>' % (d, fill, op)


def FL(d, stroke="#fff", op=.7, slow=True):
    return ('<path class="fl%s" d="%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="1.2" stroke-linecap="round" '
            'vector-effect="non-scaling-stroke"/>' % (" fl-slow" if slow else "", d, stroke, op))


def subject(name, g, stroke, sw, accent, glowid=None, base="#f6f4f4", soft=.55, fill=None):
    """The idea of each series, in a given palette: base lines, the accent, an optional glow filter on the accent."""
    gf = ' filter="url(#%s)"' % glowid if glowid else ""
    o = ""
    if name == "Risk vs Reward":
        o += S(smooth(g["climb"]), base, 1, soft) + S(smooth(g["safe"]), base, sw, .9)
        o += "".join(S(path([(a, y - 1), (b, y - 1)]), base, 2.2, .85) for (a, b), y in g["fields"])
        o += '<g%s>%s<circle cx="%s" cy="%s" r="4.5" fill="none" stroke="%s" stroke-width="1.4" vector-effect="non-scaling-stroke"/>' \
             '<circle cx="%s" cy="%s" r="1.8" fill="%s"/></g>' % (
                 gf, S(smooth(g["fast"]), accent, sw + .6), f(g["decision"][0]), f(g["decision"][1]), accent,
                 f(g["decision"][0]), f(g["decision"][1]), accent)
        o += FL(smooth(g["fast"]))
    elif name == "Sky Gods":
        o += S(smooth(g["spiral"], t=.6), base, 1.1, .9)
        o += S("M%s,%s H%s" % (f(g["cx"] - 28), f(g["stop"]), f(g["cx"] + 44)), accent, 1, .7, ' stroke-dasharray="2 3"')
        o += '<g%s>%s</g>' % (gf, S(smooth(g["wave"]), accent, sw + .8))
        o += FL(smooth(g["wave"]))
    elif name == "Weather Patterns":
        o += S(smooth(g["dew"]), base, sw, .9)
        o += '<g%s>%s<circle cx="%s" cy="%s" r="4" fill="none" stroke="%s" stroke-width="1.3" vector-effect="non-scaling-stroke"/></g>' % (
            gf, S(path(g["mid"]), accent, sw + .5), f(g["kink"][0]), f(g["kink"][1]), accent)
        o += FL(path(g["mid"]), op=.5)
    else:
        for k, st in enumerate(g["streams"]):
            o += S(smooth(st), base, .9, .35 if k in (0, 4) else .6)
        o += FL(smooth(g["streams"][2]), op=.6)
        o += F(path(g["foil"], True), fill or "none") if fill else ""
        o += S(path(g["foil"], True), base, sw + .2, 1)
        cp, lt = g["cp"], g["lift"]
        o += '<g%s>%s<path d="M%s,%s l-3.5,7 h7 Z" fill="%s"/><circle cx="%s" cy="%s" r="2.4" fill="%s"/></g>' % (
            gf, S(path([cp, (lt[0], lt[1] + 5)]), accent, sw + .4), f(lt[0]), f(lt[1]), accent, f(cp[0]), f(cp[1]), accent)
    return o


def glow(ident, std=2.2):
    return ('<filter id="%s" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="%s" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' % (ident, std))


def ember(name):
    g = GEO[name]()
    k = "em-" + name.split()[0].lower()
    defs = ('<radialGradient id="%s-bg" cx="62%%" cy="30%%" r="85%%"><stop offset="0" stop-color="#1d2233"/>'
            '<stop offset="1" stop-color="#0b0d14"/></radialGradient>'
            '<linearGradient id="%s-ac" gradientUnits="userSpaceOnUse" x1="0" y1="138" x2="200" y2="0"><stop offset="0" stop-color="#ff5a1f"/>'
            '<stop offset="1" stop-color="#ffc06b"/></linearGradient>'
            '<linearGradient id="%s-gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b3247"/>'
            '<stop offset="1" stop-color="#0b0d14"/></linearGradient>' % (k, k, k)) + glow(k + "-gl")
    body = '<rect width="%d" height="%d" fill="url(#%s-bg)"/>' % (W, H, k)
    for i in range(18):                                       # a few stars
        x, y = (37 * i * 7) % 200, (23 * i * 5) % 70
        body += '<circle cx="%d" cy="%d" r="%s" fill="#fff" fill-opacity="%s"/>' % (x, y, ".5" if i % 3 else ".8", ".25" if i % 2 else ".45")
    if name == "Risk vs Reward":
        body += F(path(g["ground"] + [(200, 138), (0, 138)], True), "url(#%s-gr)" % k)
        body += S(path(g["ground"]), "#8fa0c8", 1, .55)
        body += '<ellipse cx="%s" cy="%s" rx="14" ry="5" fill="#ff7517" fill-opacity=".22" filter="url(#%s-gl)"/>' % (f(g["gorge"][0]), f(g["gorge"][1] - 2), k)
    elif name == "Sky Gods":
        body += F(smooth(g["far"]) + " L200,138 L0,138 Z", "#1a2033")
        body += F(smooth(g["near"]) + " L200,138 L0,138 Z", "url(#%s-gr)" % k) + S(smooth(g["near"]), "#8fa0c8", 1, .55)
    elif name == "Weather Patterns":
        x0, x1, y0, y1 = g["axes"]
        body += S(path([(x0, y1), (x0, y0), (x1, y0)]), "#8fa0c8", .8, .5)
        body += "".join(S(path(list(a)), "#8fa0c8", .7, .2) for a in g["adiab"])
        c = g["cloud"]
        body += '<g filter="url(#%s-gl)">%s</g>' % (k, "".join('<circle cx="%s" cy="%s" r="%s" fill="#cfe0ff" fill-opacity=".14"/>' % (
            f(c[0] + dx), f(c[1] + dy), r) for dx, dy, r in ((0, -6, 9), (-10, -2, 7), (10, -3, 7.5))))
    body += subject(name, g, "#fff", 1.4, "url(#%s-ac)" % k, k + "-gl", base="#e8eeff", fill="#151a28")
    return svg(k, name, defs, body)


def dusk(name):
    g = GEO[name]()
    k = "du-" + name.split()[0].lower()
    defs = ('<linearGradient id="%s-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141a33"/>'
            '<stop offset=".55" stop-color="#5a2a3a"/><stop offset=".82" stop-color="#ff7a2e"/><stop offset="1" stop-color="#ffc27a"/></linearGradient>'
            '<radialGradient id="%s-sun" cx="50%%" cy="50%%" r="50%%"><stop offset="0" stop-color="#fff2d6"/>'
            '<stop offset=".35" stop-color="#ffb04a" stop-opacity=".8"/><stop offset="1" stop-color="#ff7517" stop-opacity="0"/></radialGradient>'
            % (k, k)) + glow(k + "-gl", 1.6)
    body = '<rect width="%d" height="%d" fill="url(#%s-sky)"/>' % (W, H, k)
    body += '<circle cx="150" cy="96" r="38" fill="url(#%s-sun)"/>' % k
    hills = {"Risk vs Reward": None, "Sky Gods": None}
    layers = [([(0, 96), (40, 84), (80, 92), (120, 80), (160, 90), (200, 82)], "#3a2236", .9),
              ([(0, 108), (36, 98), (70, 106), (110, 96), (150, 104), (200, 98)], "#24172a", 1)]
    if name == "Sky Gods":
        layers = [(g["far"], "#4a2a3e", .85), (g["near"], "#1d1424", 1)]
    if name == "Risk vs Reward":
        layers = [([(0, 86), (50, 78), (100, 84), (150, 74), (200, 80)], "#4a2a3e", .8), (g["ground"], "#1d1424", 1)]
    for pts, col, op in layers:
        body += F(smooth(pts) + " L200,138 L0,138 Z", col, op)
    if name == "Weather Patterns":
        x0, x1, y0, y1 = g["axes"]
        body += S(path([(x0, y1), (x0, y0), (x1, y0)]), "#ffe6c8", .8, .45)
    body += subject(name, g, "#fff", 1.5, "#ffd08a", k + "-gl", base="#fff6ea", soft=.6, fill="#1d1424")
    return svg(k, name, defs, body)


def goldline(name):
    g = GEO[name]()
    k = "gl-" + name.split()[0].lower()
    defs = ('<linearGradient id="%s-ln" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="200" y2="0"><stop offset="0" stop-color="#f6f4f4"/>'
            '<stop offset="1" stop-color="#ffb35c"/></linearGradient>'
            '<linearGradient id="%s-ac" gradientUnits="userSpaceOnUse" x1="0" y1="138" x2="200" y2="0"><stop offset="0" stop-color="#ff7517"/>'
            '<stop offset="1" stop-color="#ffd27a"/></linearGradient>' % (k, k))
    body = '<rect width="%d" height="%d" fill="#121318"/>' % (W, H)
    body += '<circle cx="100" cy="69" r="58" fill="none" stroke="#ffffff" stroke-opacity=".05" vector-effect="non-scaling-stroke"/>'
    if name == "Risk vs Reward":
        body += S(smooth(g["ground"]), "url(#%s-ln)" % k, .9, .7)
    elif name == "Sky Gods":
        body += S(smooth(g["far"]), "url(#%s-ln)" % k, .7, .35) + S(smooth(g["near"]), "url(#%s-ln)" % k, .9, .75)
    elif name == "Weather Patterns":
        x0, x1, y0, y1 = g["axes"]
        body += S(path([(x0, y1), (x0, y0), (x1, y0)]), "#f6f4f4", .6, .4)
    body += subject(name, g, "url(#%s-ln)" % k, 1, "url(#%s-ac)" % k, None, base="url(#%s-ln)" % k, soft=.5)
    return svg(k, name, defs, body)


CAT = {"Competitions": ("#ff6a2b", "#b8241c"), "Core series": ("#ffb648", "#d4561b"),
       "Meteorology": ("#3fa7ff", "#1d3f9e"), "Technical": ("#2fd4c0", "#14667a")}


def colour(name, cat):
    g = GEO[name]()
    k = "co-" + name.split()[0].lower()
    a, b = CAT[cat]
    defs = ('<linearGradient id="%s-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient>'
            '<radialGradient id="%s-hi" cx="78%%" cy="18%%" r="70%%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>' % (k, a, b, k)) + glow(k + "-gl", 1.4)
    body = '<rect width="%d" height="%d" fill="url(#%s-bg)"/><rect width="%d" height="%d" fill="url(#%s-hi)"/>' % (W, H, k, W, H, k)
    if name == "Risk vs Reward":
        body += F(smooth(g["ground"]) + " L200,138 L0,138 Z", "#000", .18)
    elif name == "Sky Gods":
        body += F(smooth(g["far"]) + " L200,138 L0,138 Z", "#000", .12) + F(smooth(g["near"]) + " L200,138 L0,138 Z", "#000", .2)
    elif name == "Weather Patterns":
        x0, x1, y0, y1 = g["axes"]
        body += S(path([(x0, y1), (x0, y0), (x1, y0)]), "#fff", .8, .5)
    body += subject(name, g, "#fff", 1.5, "#fff", k + "-gl", base="#fff", soft=.55, fill="#000")
    return svg(k, name, defs, body).replace('fill="#000" fill-opacity="1"', 'fill="#000" fill-opacity=".15"')


LOOKS = [
    ("Ember", "Luminous lines on deep night blue; the thing the series is about glows, white into gold.", ember),
    ("Dusk", "Painted: a sky running down to a warm horizon, ridges in layers, the subject in pale gold light.", dusk),
    ("Gold line", "Fine lines that run from white into gold, a lot of empty space, nothing heavy.", goldline),
    ("Colour field", "A colour per category (competitions, core series, meteorology, technical), white line art on top.", colour),
]

CSS = SM.SPEC_CSS + """
.si-sec{padding:var(--sp-5) var(--gutter) var(--sp-3);max-width:1240px;margin:0 auto;}
.si-sec h2{font-family:var(--font-display);font-size:var(--fs-h2);color:var(--white);margin:0 0 var(--sp-1);}
.si-sec>p{color:var(--gray-light);max-width:70ch;line-height:1.7;margin:0 0 var(--sp-3);}
.si-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-3);}
@media (max-width:900px){.si-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
.si-tile h3{font-family:var(--font-display);font-size:var(--fs-h4);color:var(--white);margin:.7rem 0 .2rem;}
.si-tile .meta{font-size:var(--fs-small);color:var(--gray);}
.si-shot{aspect-ratio:200/138;border-radius:10px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.35);transition:transform .4s ease,box-shadow .4s ease;}
.si-tile:hover .si-shot{transform:translateY(-4px);box-shadow:0 16px 40px rgba(0,0,0,.5);}
.si-shot svg{display:block;width:100%;height:100%;}
.si-n{display:inline-block;font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);margin-bottom:var(--sp-2);}
@media (prefers-reduced-motion:reduce){.si-shot{transition:none;}}
"""


def page():
    body = ('<header class="kit-hero is-sky v2-page-hero"><div class="kit-hero-copy"><span class="kit-kicker">Sample, not live</span>'
            '<h1>Series tiles: four looks</h1><p class="kit-intro">The same four series in four treatments, from glowing to '
            'painted to fine line to bold colour. Each tile shows the idea of its series: the decision over the gorge, the '
            'climb into wave, the sounding\'s kink, the wing and its lift. Pick one (or mix two) and the other nine follow.</p>'
            '</div></header>')
    for i, (name, why, fn) in enumerate(LOOKS):
        tiles = ""
        for s, cat, n in SERIES:
            art = fn(s, cat) if fn is colour else fn(s)
            tiles += ('<div class="si-tile"><div class="si-shot">%s</div><h3>%s</h3><div class="meta">%d episode%s in %s</div></div>'
                      % (art, s, n, "" if n == 1 else "s", cat))
        body += ('<section class="si-sec"><span class="si-n">%s</span><h2>%s</h2><p>%s</p><div class="si-grid">%s</div></section>'
                 % ("Look %d" % (i + 1), name, why, tiles))
    body += '<div style="height:var(--sp-5)"></div>'
    return SM.shell("Series tiles: four looks", "Four looks for the library's series tiles, for the owner to choose from.", body, CSS)


def main():
    out = os.path.join(V4, "samples", "series-icons-2.html")
    open(out, "w", encoding="utf-8").write(page())
    print("v4 series icons 2: samples/series-icons-2.html")


if __name__ == "__main__":
    main()
