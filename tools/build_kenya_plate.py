"""Kenya as an extruded chart plate, axonometric.

The projection matters. The earlier 3D terrain render was perspective with
relief, so a summit was drawn displaced from the ground under it and no pin
could be trusted. This is a parallel projection of a flat plate: screen position
is an exact linear function of longitude and latitude, invertible, with the
extrusion only ever a constant offset in screen y. Every site sits exactly where
its coordinate says.

Sites stand on stems rather than lying flat. On an extruded plate a flat dot
reads as a smudge, and the stem base is the true coordinate, so the height is
decoration that costs no accuracy.
"""
import json, math

THETA = math.radians(0.0)      # plate rotation
SQUASH = 0.74                    # vertical foreshortening
DEPTH = 46                       # extrusion thickness, screen px
W, H = 1900, 1500
LONC, LATC = 37.9, 0.2
S = 132                          # px per degree on the plate

PAGE = "#141519"
TOP = "#272a33"
WALL = "#0e0f12"
EDGE = "#565a66"
PROV = "#3a3d47"
INK = "#e8e4d8"
DIM = "#8f95a3"
WATER = "#1d3440"
ORANGE = "#ff7517"
GOLD = "#c9a86a"

SITES = [
    ("KERIO VALLEY",   35.65,  0.72, -26,  -30, "end"),
    ("RIFT VALLEY NP", 36.30, -0.90, -120,  14, "end"),
    ("MT LONGONOT",    36.45, -0.91,  -4,  -84, "middle"),
    ("KIJABE HILL",    36.58, -0.93,  124, -34, "start"),
    ("MACHAKOS HILLS", 37.26, -1.52,  32,   40, "start"),
    ("CHYULU HILLS",   37.88, -2.68,  32,   -4, "start"),
]
CX, CY = W / 2 - 40, H / 2 - 30


def plate(lon, lat):
    """lon/lat to screen, on the top face of the plate."""
    u = (lon - LONC) * S
    v = (LATC - lat) * S
    x = CX + (u * math.cos(THETA) - v * math.sin(THETA))
    y = CY + (u * math.sin(THETA) + v * math.cos(THETA)) * SQUASH
    return x, y


def rings(g):
    if g["type"] == "Polygon":
        return g["coordinates"]
    return [r for poly in g["coordinates"] for r in poly]


def gc(a, b):
    lo1, la1, lo2, la2 = a[1], a[2], b[1], b[2]
    p1, p2 = math.radians(la1), math.radians(la2)
    dl = math.radians(lo2 - lo1)
    d = math.acos(min(1, math.sin(p1) * math.sin(p2) +
                      math.cos(p1) * math.cos(p2) * math.cos(dl))) * 6371.0
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return d, (math.degrees(math.atan2(y, x)) + 360) % 360


def _perp(p, a, b):
    if a == b:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    n = abs((b[0] - a[0]) * (a[1] - p[1]) - (a[0] - p[0]) * (b[1] - a[1]))
    return n / math.hypot(b[0] - a[0], b[1] - a[1])


def _simplify(pts, tol):
    """Douglas-Peucker, iterative so a 3000 point ring cannot blow the stack."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        dmax, idx = 0.0, 0
        for m in range(i + 1, j):
            d = _perp(pts[m], pts[i], pts[j])
            if d > dmax:
                dmax, idx = d, m
        if dmax > tol:
            keep[idx] = True
            stack.append((i, idx))
            stack.append((idx, j))
    return [p for p, k in zip(pts, keep) if k]


def path(ringlist, tol=3.0):
    """Coordinates go out at one decimal and rings are simplified first. The
    source is 10m Natural Earth, which at this display size carries detail far
    below a pixel: unsimplified the plate was 195KB of path data alone."""
    out = []
    for r in ringlist:
        pts = _simplify([plate(x, y) for x, y in r], tol)
        if len(pts) < 3:
            continue
        out.append("M" + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + "Z")
    return "".join(out)


feats = json.load(open("ne_10m_admin_0_countries.json"))["features"]
kenya = next(f for f in feats if f["properties"].get("ADMIN") == "Kenya")
kr = [r for r in rings(kenya["geometry"]) if len(r) > 20]
outer = max(kr, key=len)

o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
     f'font-family="DM Sans, sans-serif">']
o.append('<defs>'
         f'<clipPath id="plate"><path d="{path([outer])}"/></clipPath>'
         '<filter id="sh" x="-30%" y="-30%" width="180%" height="180%">'
         '<feGaussianBlur stdDeviation="26"/></filter>'
         '</defs>')
o.append(f'<rect width="{W}" height="{H}" fill="{PAGE}"/>')

# ---- cast shadow ----------------------------------------------------------
sp = [plate(x, y) for x, y in outer]
o.append('<path filter="url(#sh)" opacity=".75" fill="#000" d="M' +
         " ".join(f"{a+16:.1f},{b+DEPTH+30:.1f}" for a, b in sp) + 'Z"/>')

# ---- extrusion ------------------------------------------------------------
o.append(f'<path d="M' + " ".join(f"{a:.1f},{b+DEPTH:.1f}" for a, b in sp) +
         f'Z" fill="{WALL}"/>')
for i in range(len(sp)):
    x1, y1 = sp[i]
    x2, y2 = sp[(i + 1) % len(sp)]
    o.append(f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} '
             f'L{x2:.1f},{y2+DEPTH:.1f} L{x1:.1f},{y1+DEPTH:.1f}Z" fill="{WALL}"/>')
o.append(f'<path d="M' + " ".join(f"{a:.1f},{b+DEPTH:.1f}" for a, b in sp) +
         f'Z" fill="none" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1.4"/>')

# ---- top face -------------------------------------------------------------
o.append(f'<path d="{path(kr)}" fill="{TOP}"/>')
o.append('<g clip-path="url(#plate)">')

# graticule on the surface
o.append(f'<g stroke="{EDGE}" stroke-opacity=".26" stroke-width="1">')
for lo in range(34, 42):
    a = plate(lo, -5.2)
    b = plate(lo, 5.6)
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
for la in range(-5, 6):
    if la == 0:
        continue
    a = plate(33.4, la)
    b = plate(42.4, la)
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
o.append('</g>')
a, b = plate(33.4, 0), plate(42.4, 0)
o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
         f'stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.8" stroke-dasharray="16 6 4 6"/>')

# provinces
adm = json.load(open("adm1.json"))["features"]
o.append(f'<g fill="none" stroke="{PROV}" stroke-width="1.3">')
for f in adm:
    if f["properties"].get("admin") != "Kenya":
        continue
    o.append(f'<path d="{path(rings(f["geometry"]))}"/>')
o.append('</g>')

# water
for f in json.load(open("ne_10m_lakes.json"))["features"]:
    nm = str(f["properties"].get("name"))
    if nm not in ("Lake Victoria", "Lake Turkana", "Lake Natron", "Masinga Res."):
        continue
    o.append(f'<path d="{path(rings(f["geometry"]))}" fill="{WATER}" '
             f'stroke="#4d7d90" stroke-width="1.2"/>')

# route on the surface
pts = [plate(t[1], t[2]) for t in SITES]
o.append('<polyline class="kmap-course" points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) +
         f'" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-opacity=".85" '
         f'stroke-linejoin="round" stroke-linecap="round"/>')
o.append('</g>')
o.append(f'<path d="{path([outer])}" fill="none" stroke="{EDGE}" stroke-width="2"/>')

# ---- standing site pins ---------------------------------------------------
MARKS = False   # site marks are real HTML buttons now, see kenya-map.js

# No stems. They lifted every marker 58px, which is 49km at this scale, and the
# route then ended below the mark the eye was reading. Depth is not worth an
# apparent error on a map whose whole claim is that it is accurate.
for (n, lo, la, dx, dy, anc), (x, y) in zip(SITES, pts):
    if not MARKS:
        continue
    tx, ty = x, y
    o.append(f'<ellipse cx="{x:.1f}" cy="{y+9:.1f}" rx="13" ry="5" fill="#000" fill-opacity=".38"/>')
    o.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="11" fill="{PAGE}" stroke="{ORANGE}" stroke-width="2.4"/>')
    o.append(f'<path d="M{tx-5.5:.1f},{ty+2.5:.1f} L{tx:.1f},{ty-5:.1f} L{tx+5.5:.1f},{ty+2.5:.1f}" '
             f'fill="none" stroke="{ORANGE}" stroke-width="2" stroke-linejoin="round"/>')
    lx, ly = tx + dx, ty + dy
    if abs(dx) > 40 or abs(dy) > 40:
        o.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{lx:.1f}" y2="{ly+5:.1f}" '
                 f'stroke="{DIM}" stroke-opacity=".55" stroke-width="1"/>')
    lat_s = f'{abs(la):.2f}°{"N" if la >= 0 else "S"}'
    lw = len(n) * 10.4 + 16
    ox = -lw if anc == "end" else (-lw / 2 if anc == "middle" else 0)
    o.append('<g class="lbl">')
    o.append(f'<rect x="{lx+ox:.1f}" y="{ly-19:.1f}" width="{lw:.0f}" height="42" rx="0" '
             f'fill="{PAGE}" fill-opacity=".82"/>')
    o.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="17" font-weight="600" '
             f'letter-spacing="1.5" fill="{INK}" text-anchor="{anc}">{n}</text>')
    o.append(f'<text x="{lx:.1f}" y="{ly+18:.1f}" font-size="12.5" letter-spacing="1.8" '
             f'fill="{DIM}" text-anchor="{anc}">{lat_s}  {lo:.2f}°E</text>')
    o.append('</g>')

# ---- furniture ------------------------------------------------------------
o.append('<g id="furn">')
o.append(f'<g><text x="58" y="{H-104}" font-size="14" letter-spacing="5" fill="{GOLD}" '
         f'fill-opacity=".85">PARAGLIDING ATLAS</text>'
         f'<text x="58" y="{H-70}" font-size="25" font-weight="600" letter-spacing="1.4" '
         f'fill="{INK}">KENYA  ·  RIFT VALLEY CORRIDOR</text>'
         f'<text x="58" y="{H-44}" font-size="12.5" letter-spacing="2.6" fill="{DIM}">'
         f'WGS 84   ·   SIX SITES   ·   BEARINGS TRUE   ·   451 KM TOTAL</text></g>')

legs = []
for i in range(len(SITES) - 1):
    d, brg = gc(SITES[i], SITES[i + 1])
    legs.append(f"{brg:03.0f}°T / {d:.0f} KM")
o.append(f'<g><text x="{W-58}" y="{H-146}" font-size="12" letter-spacing="4" fill="{GOLD}" '
         f'fill-opacity=".8" text-anchor="end">LEGS</text>')
for i, t in enumerate(legs):
    o.append(f'<text x="{W-58}" y="{H-118+i*21}" font-size="13" letter-spacing="1.6" '
             f'fill="{DIM}" text-anchor="end">{t}</text>')
o.append('</g>')

# north arrow, rotated with the plate
nx, ny = 150, 150
na = THETA
o.append(f'<g stroke="{INK}" stroke-opacity=".7" fill="{INK}" fill-opacity=".7">'
         f'<line x1="{nx:.0f}" y1="{ny:.0f}" '
         f'x2="{nx+math.sin(na)*54:.0f}" y2="{ny-math.cos(na)*54*SQUASH:.0f}" stroke-width="1.6"/>'
         f'<circle cx="{nx+math.sin(na)*54:.0f}" cy="{ny-math.cos(na)*54*SQUASH:.0f}" r="4"/>'
         f'<text x="{nx+math.sin(na)*74:.0f}" y="{ny-math.cos(na)*74*SQUASH+5:.0f}" '
         f'font-size="15" letter-spacing="3" text-anchor="middle">N</text></g>')

o.append('</g>')
o.append('</svg>')
open("chart-iso.svg", "w").write("\n".join(o))
json.dump({n: {"x": round(plate(lo, la)[0] / W * 100, 3),
               "y": round(plate(lo, la)[1] / H * 100, 3)}
           for n, lo, la, *_ in SITES}, open("pos-plate.json", "w"), indent=1)
print(f"iso chart {W}x{H}  {len(''.join(o))//1024} KB")
