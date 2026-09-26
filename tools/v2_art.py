#!/usr/bin/env python3
"""
Draw the v2 prototype's line art (prototypes/v2/img/), pure Python, no deps.

  contours.svg  topographic contour lines, traced with marching squares over a
                made-up terrain (a few hills and a ridge), every fifth line
                heavier like an index contour on a survey map. Sits faintly
                behind text-heavy sections (.v2-topo in v2.css).
  ridge.svg     three layers of mountain ridge for the footer horizon; the
                sky glow behind it is CSS, so it follows the time-of-day sky.

Deterministic (fixed seed), so re-running gives the same files.

    python3 tools/v2_art.py          # contours.svg, ridge.svg
    python3 tools/v2_art.py icons    # the panel icons, into the v2 pages
"""
import math
import os
import random
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "prototypes", "v2", "img")


def terrain(w, h, seed):
    rnd = random.Random(seed)
    hills = [(rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(0.35, 1.0), rnd.uniform(w * .08, w * .22)) for _ in range(9)]
    waves = [(rnd.uniform(.5, 2.2) * math.pi / w, rnd.uniform(.5, 2.2) * math.pi / h, rnd.uniform(0, 6.3), rnd.uniform(.04, .1)) for _ in range(5)]
    def z(x, y):
        v = 0.0
        for cx, cy, a, s in hills:
            v += a * math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s * s))
        for fx, fy, ph, a in waves:
            v += a * math.sin(fx * x * 3 + ph) * math.cos(fy * y * 3 - ph)
        return v
    return z


def march(z, w, h, step, level):
    """Marching squares: segments where the field crosses `level`."""
    nx, ny = int(w / step) + 1, int(h / step) + 1
    g = [[z(i * step, j * step) for i in range(nx)] for j in range(ny)]
    segs = []
    def lerp(p, q, a, b):
        t = (level - a) / (b - a) if b != a else .5
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    for j in range(ny - 1):
        for i in range(nx - 1):
            a, b, c, d = g[j][i], g[j][i + 1], g[j + 1][i + 1], g[j + 1][i]
            P = [(i * step, j * step), ((i + 1) * step, j * step), ((i + 1) * step, (j + 1) * step), (i * step, (j + 1) * step)]
            v = [a, b, c, d]
            e = []
            for k in range(4):
                p, q = k, (k + 1) % 4
                if (v[p] >= level) != (v[q] >= level):
                    e.append(lerp(P[p], P[q], v[p], v[q]))
            if len(e) == 2:
                segs.append((e[0], e[1]))
            elif len(e) == 4:
                segs.append((e[0], e[1]))
                segs.append((e[2], e[3]))
    return segs


def join(segs):
    key = lambda p: (round(p[0], 3), round(p[1], 3))
    ends = {}
    for s in segs:
        for p in s:
            ends.setdefault(key(p), []).append(s)
    used, lines = set(), []
    for s in segs:
        if id(s) in used:
            continue
        used.add(id(s))
        line = [s[0], s[1]]
        for direction in (0, 1):
            while True:
                tip = line[-1] if direction == 0 else line[0]
                nxt = None
                for t in ends.get(key(tip), []):
                    if id(t) not in used:
                        nxt = t
                        break
                if not nxt:
                    break
                used.add(id(nxt))
                other = nxt[1] if key(nxt[0]) == key(tip) else nxt[0]
                if direction == 0:
                    line.append(other)
                else:
                    line.insert(0, other)
        lines.append(line)
    return lines


def smooth_path(pts):
    if len(pts) < 3:
        return "M%.1f %.1f L%.1f %.1f" % (pts[0][0], pts[0][1], pts[-1][0], pts[-1][1])
    d = "M%.0f %.0f" % pts[0]
    for k in range(1, len(pts) - 1):
        mx, my = (pts[k][0] + pts[k + 1][0]) / 2, (pts[k][1] + pts[k + 1][1]) / 2
        d += " Q%.0f %.0f %.0f %.0f" % (pts[k][0], pts[k][1], mx, my)
    d += " L%.0f %.0f" % pts[-1]
    return d


def contours():
    w, h, step = 1600, 1000, 12
    z = terrain(w, h, 7)
    paths = []
    levels = [0.06 + k * 0.075 for k in range(22)]
    for n, lv in enumerate(levels):
        heavy = n % 5 == 0
        for line in join(march(z, w, h, step, lv)):
            if len(line) < 4:
                continue
            paths.append('<path d="%s"%s/>' % (smooth_path(line), ' stroke-width="1.6"' if heavy else ""))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">'
           '<g fill="none" stroke="#b4b4b4" stroke-width=".8" stroke-linejoin="round" stroke-linecap="round">%s</g></svg>\n') % (w, h, "".join(paths))
    open(os.path.join(OUT, "contours.svg"), "w").write(svg)
    return len(paths)


def trails():
    """A pool of the backdrop's longer contour lines (img/contours.svg is the
    same drawing), thinned to every third point to stay small. The page picks
    a few at random for each section and sends a short orange glow along them
    from a random point as it scrolls (v2-immersive.js); the paths are written
    into that file between markers."""
    w, h, step = 1600, 1000, 12
    z = terrain(w, h, 7)
    pool = []
    for n in range(22):
        lv = 0.06 + n * 0.075
        for line in join(march(z, w, h, step, lv)):
            L = sum(math.dist(line[i], line[i + 1]) for i in range(len(line) - 1))
            if L > 900:
                pool.append((L, line))
    pool.sort(key=lambda t: -t[0])
    out = []
    for L, line in pool[:12]:
        pts = line[::3] + ([line[-1]] if (len(line) - 1) % 3 else [])
        out.append(smooth_path(pts))
    js = os.path.join(ROOT, "prototypes", "v2", "v2-immersive.js")
    src = open(js, encoding="utf-8").read()
    lst = ",".join('"%s"' % d for d in out)
    src = re.sub(r"/\*v2-trails\*/.*?/\*/v2-trails\*/", lambda m: "/*v2-trails*/" + lst + "/*/v2-trails*/", src, flags=re.S)
    open(js, "w", encoding="utf-8").write(src)
    return len(out)


def ridge():
    """Midpoint displacement, one profile per layer: far and high to near and low."""
    w, h = 1600, 260
    rnd = random.Random(11)

    def profile(top, bottom, rough):
        n = 128
        ys = [0.0] * (n + 1)
        ys[0], ys[n] = rnd.uniform(0, 1), rnd.uniform(0, 1)
        size, amp = n, 1.0
        while size > 1:
            half = size // 2
            for i in range(half, n, size):
                ys[i] = (ys[i - half] + ys[i + half]) / 2 + rnd.uniform(-amp, amp)
            size, amp = half, amp * rough
        lo, hi = min(ys), max(ys)
        return [(w * i / n, bottom - (y - lo) / (hi - lo) * (bottom - top)) for i, y in enumerate(ys)]

    layers = []
    for n, (top, bottom, rough, fill) in enumerate([(24, 170, .58, "#1b1d23"), (90, 205, .55, "#15161b"), (150, 235, .5, "#101115")]):
        pts = profile(top, bottom, rough)
        line = " L".join("%.0f %.0f" % p for p in pts)
        layers.append('<path d="M0 %d L%s L%d %d Z" fill="%s"/>' % (h, line, w, h, fill))
        # a lit rim on the far ridge only, the last of the sun on it
        if n == 0:
            layers.append('<path d="M%s" fill="none" stroke="#ff7517" stroke-opacity=".3" stroke-width="1.2"/>' % line)
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="none">%s</svg>\n' % (w, h, "".join(layers))
    open(os.path.join(OUT, "ridge.svg"), "w").write(svg)




# ---------------------------------------------------------------------------
# Icons: one instrument-style set for every panel that used to carry a numeral.
# A faint gauge bezel with four ticks, the symbol inside in the accent colour.
# Inline SVG (currentColor), written into the pages by `python3 tools/v2_art.py icons`.

def _flags():
    """Prayer flags: two poles, a sagging line, four pennants."""
    out = ['<path d="M8 8v16.5M24 8v16.5M8 9.5Q16 16.5 24 9.5"/>']
    for t in (.2, .4, .6, .8):
        x = (1 - t) ** 2 * 8 + 2 * (1 - t) * t * 16 + t * t * 24
        y = (1 - t) ** 2 * 9.5 + 2 * (1 - t) * t * 16.5 + t * t * 9.5
        out.append('<path d="M%.1f %.1f h3.4 l-1.7 4.8z"/>' % (x - 1.7, y))
    return "".join(out)


GLYPHS = {
    "globe": '<circle cx="16" cy="16" r="8"/><ellipse cx="16" cy="16" rx="3.4" ry="8"/><path d="M8 16h16M9.1 12h13.8M9.1 20h13.8"/>',
    "mic": '<rect x="13" y="7.5" width="6" height="10.5" rx="3"/><path d="M10 15a6 6 0 0 0 12 0M16 21v3M13 24h6"/>',
    "shield": '<path d="M16 7l7 3v5.2c0 4.8-3 8.3-7 9.8-4-1.5-7-5-7-9.8V10z"/><path d="M12.8 16.1l2.3 2.3 4.3-4.6"/>',
    "flags": _flags(),
    "series": '<path d="M13 7.5h6M11 10h10"/><rect x="9" y="12.5" width="14" height="10" rx="1.5"/><path d="M14.8 15v5l4.2-2.5z" fill="currentColor"/>',
    "people": '<circle cx="12" cy="12.2" r="2.6"/><circle cx="20" cy="12.2" r="2.6"/><path d="M7.4 23c.3-3.1 2.2-5.2 4.6-5.2s4.3 2.1 4.6 5.2M15.4 23c.3-3.1 2.2-5.2 4.6-5.2s4.3 2.1 4.6 5.2"/>',
    "compass": '<path d="M16 8l2.7 8-2.7 8-2.7-8z"/><path d="M16 8l2.7 8h-5.4z" fill="currentColor"/><circle cx="16" cy="16" r=".9" fill="currentColor"/>',
    "canopy": '<path d="M6.5 13.2C9.5 8.3 22.5 8.3 25.5 13.2 22.3 11.6 9.7 11.6 6.5 13.2z"/><path d="M7.5 13 16 22.2M11.8 11.7 16 22.2M20.2 11.7 16 22.2M24.5 13 16 22.2"/><circle cx="16" cy="23.4" r="1.2" fill="currentColor"/>',
    "talk": '<path d="M9 9.5h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-8l-4 3.5v-3.5H9a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z"/><circle cx="12.5" cy="15" r=".9" fill="currentColor"/><circle cx="16" cy="15" r=".9" fill="currentColor"/><circle cx="19.5" cy="15" r=".9" fill="currentColor"/>',
}


def icon(name):
    return ('<span class="v2-ic" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round">'
            '<g class="v2-ic-bezel"><circle cx="16" cy="16" r="15"/><path d="M16 1v2.6M16 28.4V31M1 16h2.6M28.4 16H31"/></g>'
            '<g class="v2-ic-glyph">%s</g></svg></span>') % GLYPHS[name]


ICON_SWAPS = {
    "podcast.html": [('<span class="kit-kicker">%s</span><h3>%s' % (n, t), g) for n, t, g in (
        ("I", "Global Destinations", "globe"), ("II", "Expert Insights", "mic"), ("III", "Safety First", "shield"),
        ("IV", "Cultural Immersion", "flags"), ("V", "Thematic Mini-Series", "series"))],
    "index.html": [('<span class="kit-kicker">%s</span><h3>%s' % (n, t), g) for n, t, g in (
        ("01", "Because We Care to Share", "people"), ("02", "Flight Safety, First and Always", "shield"), ("03", "Exclusive Journeys", "compass"))],
}
# one icon span and nothing past it: the svg holds no nested </svg>
ONE_ICON = r'<span class="%s" aria-hidden="true"><svg[^>]*>(?:(?!</svg>).)*</svg></span>'
ABOUT = (("Experience", "canopy"), ("Service", "talk"), ("Community Empowerment", "people"), ("Security", "shield"))


def icons():
    import re
    v2 = os.path.join(ROOT, "prototypes", "v2")
    n = 0
    for page, swaps in ICON_SWAPS.items():
        fp = os.path.join(v2, page)
        html = open(fp, encoding="utf-8").read()
        for old, g in swaps:
            head = old.split("<h3>")[1]
            # first run replaces the numeral; later runs refresh the drawn icon
            pat = re.compile(r'(?:<span class="kit-kicker">[IVX0-9]+</span>|' + ONE_ICON % "v2-ic" + ')<h3>' + re.escape(head))
            html, k = pat.subn(lambda m: icon(g) + "<h3>" + head, html, count=1)
            n += k
        open(fp, "w", encoding="utf-8").write(html)
    fp = os.path.join(v2, "about.html")
    html = open(fp, encoding="utf-8").read()
    for title, g in ABOUT:
        pat = re.compile("(?:" + ONE_ICON % "v2-promise-ic" + "|" + ONE_ICON % "v2-ic" + ")<h3>" + re.escape(title) + "</h3>")
        html, k = pat.subn(lambda m: icon(g) + "<h3>" + title + "</h3>", html, count=1)
        n += k
    open(fp, "w", encoding="utf-8").write(html)
    return n


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["icons"]:
        print("v2 icons: %d panels" % icons())
    else:
        os.makedirs(OUT, exist_ok=True)
        n = contours()
        ridge()
        t = trails()
        print("v2 art: contours.svg (%d lines), ridge.svg, %d glow trails" % (n, t))
