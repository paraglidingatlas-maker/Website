#!/usr/bin/env python3
"""
A globe turned to one place, drawn at build time as inline SVG (no d3 on the
page). The episode page's opening moment: where the story is from.

Data
  land      Natural Earth 1:110m land (public domain), tools/data/ne_110m_land.geojson,
            the same source the podcast globe draws (world-atlas land-110m).
  the pin   the episode's own pin on the site's globe (globe-episodes.js, from
            globe.js). Episodes whose pin is only the home default (home: true)
            get no globe: the place is not in the data.
  range     great circle distance and bearing from Oslo, the coordinate in the
            site's navigation, as the podcast globe's popup already prints them.

    import v4_globe as G
    svg = G.globe(lat, lon, ident, title, desc, label="Colombia")
"""
import html
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAND = os.path.join(ROOT, "tools", "data", "ne_110m_land.geojson")
OSLO = (59.9139, 10.7522)
_land = None


def land():
    global _land
    if _land is None:
        gj = json.load(open(LAND, encoding="utf-8"))
        rings = []
        for ft in gj["features"]:
            g = ft["geometry"]
            polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
            for poly in polys:
                rings.append(poly[0])            # outer rings only at this scale
        _land = rings
    return _land


def xyz(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def rot(p, lat0, lon0):
    """Rotate the sphere so (lat0, lon0) faces the viewer: returns (x right, y up, z towards)."""
    x, y, z = p
    lo = math.radians(lon0)
    x, y = x * math.cos(lo) + y * math.sin(lo), -x * math.sin(lo) + y * math.cos(lo)
    la = math.radians(lat0)
    x, z = x * math.cos(la) + z * math.sin(la), -x * math.sin(la) + z * math.cos(la)
    return (y, z, x)


def densify(ring, step=3.0):
    out = []
    for (a, b) in zip(ring, ring[1:]):
        n = max(1, int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) / step))
        for i in range(n):
            out.append((a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n))
    out.append(ring[-1])
    return out


def clip_ring(pts3):
    """Sutherland-Hodgman against the visible hemisphere (z >= 0); crossing
    points land on the horizon; a gap along the horizon is walked as an arc."""
    out = []
    n = len(pts3)
    for i in range(n):
        a, b = pts3[i - 1], pts3[i]
        ina, inb = a[2] >= 0, b[2] >= 0
        if ina != inb:
            t = a[2] / (a[2] - b[2])
            c = [a[k] + (b[k] - a[k]) * t for k in range(3)]
            L = math.hypot(c[0], c[1]) or 1
            out.append(("h", (c[0] / L, c[1] / L, 0.0)))
        if inb:
            out.append(("p", b))
    if not out:
        return []
    # walk the horizon between an exit and the next entry
    res = []
    for i, (kind, p) in enumerate(out):
        res.append(p)
        nk, np_ = out[(i + 1) % len(out)]
        if kind == "h" and nk == "h":
            a0 = math.atan2(p[1], p[0])
            a1 = math.atan2(np_[1], np_[0])
            d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
            steps = int(abs(d) / math.radians(4))
            for s in range(1, steps):
                a = a0 + d * s / steps
                res.append((math.cos(a), math.sin(a), 0.0))
    return res


def f(v):
    return "%d" % round(v)


def thin(xy, tol=1.6):
    """Drop points closer than tol px to the last one kept."""
    out = [xy[0]]
    for p in xy[1:]:
        if abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) >= tol:
            out.append(p)
    return out


def globe(lat, lon, ident, title, desc, label="", size=420, tilt=14.0):
    """The globe centred a little below the place (tilt), so the place sits
    above the middle, where the eye goes first."""
    R = size * 0.42
    cx = cy = size / 2
    c_lat = max(-70.0, min(70.0, lat - tilt))
    P = lambda p: (cx + R * p[0], cy - R * p[1])
    paths = []
    for ring in land():
        pts = [rot(xyz(la, lo), c_lat, lon) for lo, la in densify(ring)]
        vis = clip_ring(pts)
        if len(vis) < 3:
            continue
        xy = thin([P(p) for p in vis])
        if len(xy) < 3:
            continue
        paths.append("M" + "L".join("%s,%s" % (f(x), f(y)) for x, y in xy) + "Z")
    # graticule: every 15 degrees, only the front
    grat = []
    for la in range(-75, 90, 15):
        seg = []
        for lo in range(-180, 181, 3):
            p = rot(xyz(la, lo), c_lat, lon)
            if p[2] >= 0:
                seg.append(P(p))
            elif seg:
                grat.append(seg)
                seg = []
        if seg:
            grat.append(seg)
    for lo in range(-180, 180, 15):
        seg = []
        for la in range(-90, 91, 3):
            p = rot(xyz(la, lo), c_lat, lon)
            if p[2] >= 0:
                seg.append(P(p))
            elif seg:
                grat.append(seg)
                seg = []
        if seg:
            grat.append(seg)
    gd = "".join("M" + "L".join("%s,%s" % (f(x), f(y)) for x, y in thin(s, 3)) for s in grat if len(s) > 1)
    # the great circle from Oslo, the front half only
    arc = []
    a, b = xyz(*OSLO), xyz(lat, lon)
    dot = max(-1.0, min(1.0, sum(i * j for i, j in zip(a, b))))
    om = math.acos(dot)
    if om > 1e-3:
        seg = []
        for i in range(61):
            t = i / 60
            s1, s2 = math.sin((1 - t) * om) / math.sin(om), math.sin(t * om) / math.sin(om)
            p = rot(tuple(s1 * a[k] + s2 * b[k] for k in range(3)), c_lat, lon)
            if p[2] >= 0:
                seg.append(P(p))
            elif seg:
                arc.append(seg)
                seg = []
        if seg:
            arc.append(seg)
    ad = "".join("M" + "L".join("%s,%s" % (f(x), f(y)) for x, y in s) for s in arc if len(s) > 1)
    pin = P(rot(xyz(lat, lon), c_lat, lon))
    oslo = rot(xyz(*OSLO), c_lat, lon)
    op = P(oslo) if oslo[2] >= 0 and om > 0.02 else None
    p = "gl-" + ident
    parts = [
        '<svg class="v4-globe %s" viewBox="0 0 %s %s" role="img" aria-labelledby="%s-t %s-d" xmlns="http://www.w3.org/2000/svg">' % (p, size, size, p, p),
        '<title id="%s-t">%s</title><desc id="%s-d">%s</desc>' % (p, html.escape(title), p, html.escape(desc)),
        '<defs><radialGradient id="%s-sea" cx="42%%" cy="36%%" r="70%%"><stop offset="0" stop-color="#23252d"/>'
        '<stop offset="1" stop-color="#15161b"/></radialGradient>'
        '<radialGradient id="%s-glow"><stop offset="0" stop-color="#ff7517" stop-opacity=".35"/>'
        '<stop offset="1" stop-color="#ff7517" stop-opacity="0"/></radialGradient></defs>' % (p, p),
        '<circle cx="%s" cy="%s" r="%s" fill="url(#%s-sea)"/>' % (f(cx), f(cy), f(R), p),
        '<path class="gl-grat" d="%s"/>' % gd,
        '<path class="gl-land" d="%s"/>' % "".join(paths),
        '<circle class="gl-rim" cx="%s" cy="%s" r="%s"/>' % (f(cx), f(cy), f(R)),
    ]
    if ad:
        parts.append('<path class="gl-arc" d="%s"/>' % ad)
    if op:
        parts.append('<circle class="gl-home" cx="%s" cy="%s" r="2.6"/>' % (f(op[0]), f(op[1])))
    parts += [
        '<circle cx="%s" cy="%s" r="46" fill="url(#%s-glow)"/>' % (f(pin[0]), f(pin[1]), p),
        '<circle class="gl-ring" cx="%s" cy="%s" r="9"/>' % (f(pin[0]), f(pin[1])),
        '<circle class="gl-pin" cx="%s" cy="%s" r="4"/>' % (f(pin[0]), f(pin[1])),
        "</svg>",
    ]
    return "".join(parts)


def range_bearing(lat, lon):
    a, b = OSLO, (lat, lon)
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    km = 6371.0 * 2 * math.asin(math.sqrt(h))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return km, (math.degrees(math.atan2(y, x)) + 360) % 360
