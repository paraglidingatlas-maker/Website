"""Kenya Rift corridor as an aeronautical chart.

Vector throughout apart from a very faint terrain tint, which is how an ICAO
1:500,000 handles relief anyway. Cropped to the operating area rather than the
whole country: at 300 px per degree the three Rift sites sit 39px apart instead
of 15, which is the difference between a cluster and a readable group.

Bearings and distances on every leg are computed great circle from the real
coordinates. Nothing on this chart is decorative invention.
"""
import json, math, base64
from PIL import Image, ImageFilter
Image.MAX_IMAGE_PIXELS = None

LON0, LON1 = 33.80, 39.80
LAT0, LAT1 = -3.20, 1.60
W = 1800
S = W / (LON1 - LON0)
H = int((LAT1 - LAT0) * S)
M = 54                                   # neat-line margin

# Night palette. Not a fudge: Jeppesen and ForeFlight both ship a night chart,
# and pilots fly off it. Ground sits a touch above the site background so the
# sheet reads as a sheet rather than as a hole in the page.
INK = "#e8e4d8"
RULE = "#6b6557"
WATER_F = "#16262e"
WATER_S = "#43707f"
ORANGE = "#ff7517"
GROUND = "#191a1f"

# dx, dy is where the label sits relative to the symbol. The three Rift sites
# are 15 to 31 km apart, so their labels are fanned onto leader lines the way a
# chart handles any dense group. Everything else takes the default to the right.
SITES = [
    ("KERIO VALLEY",   35.65,  0.72,  26,  -4, "start"),
    ("RIFT VALLEY NP", 36.30, -0.90, -66, -96, "end"),
    ("MT LONGONOT",    36.45, -0.91,  96, -78, "start"),
    ("KIJABE HILL",    36.58, -0.93, -104, 104, "end"),
    ("MACHAKOS HILLS", 37.26, -1.52,  26,  -4, "start"),
    ("CHYULU HILLS",   37.88, -2.68, -26,  -4, "end"),
]


def xy(lon, lat):
    return ((lon - LON0) * S, (LAT1 - lat) * S)


def gc(a, b):
    """Great circle distance in km and initial true bearing in degrees."""
    lo1, la1 = a[1], a[2]
    lo2, la2 = b[1], b[2]
    p1, p2 = math.radians(la1), math.radians(la2)
    dl = math.radians(lo2 - lo1)
    d = math.acos(min(1, math.sin(p1) * math.sin(p2) +
                      math.cos(p1) * math.cos(p2) * math.cos(dl))) * 6371.0
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return d, (math.degrees(math.atan2(y, x)) + 360) % 360


def rings(g):
    if g["type"] == "Polygon":
        return g["coordinates"]
    return [r for poly in g["coordinates"] for r in poly]


def clip_path(geom, tol=0.0):
    out = []
    for r in rings(geom):
        pts = [xy(x, y) for x, y in r]
        if max(p[0] for p in pts) < -200 or min(p[0] for p in pts) > W + 200:
            continue
        if max(p[1] for p in pts) < -200 or min(p[1] for p in pts) > H + 200:
            continue
        out.append("M" + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + "Z")
    return "".join(out)


o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
     f'font-family="DM Sans, sans-serif">']
o.append('<defs>')
o.append(f'<clipPath id="neat"><rect x="{M}" y="{M}" width="{W-2*M}" height="{H-2*M}"/></clipPath>')
o.append('</defs>')
o.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

# ---- terrain tint ---------------------------------------------------------
src = Image.open("/tmp/bm/shadedrelief.jpg")
ppd = src.size[0] / 360
tile = src.crop((int((LON0 + 180) * ppd), int((90 - LAT1) * ppd),
                 int((LON1 + 180) * ppd), int((90 - LAT0) * ppd)))
tile = tile.resize((W, H), Image.LANCZOS).convert("L")
# Night terrain has to be built, not just re-blended. Flat ground must fall to
# near black or a screen blend floods the whole sheet; only the escarpments and
# the volcanoes should lift.
import numpy as _np
_t = _np.asarray(tile).astype(_np.float32) / 255.0
_lo, _hi = _np.percentile(_t, 4), _np.percentile(_t, 99)
_t = _np.clip((_t - _lo) / (_hi - _lo), 0, 1) ** 2.9
tile = Image.fromarray((_t * 64).astype("uint8"), "L")
# The source is 30 px per degree, so this crop is only 180x144 before a 10x
# upscale. Left sharp it reads as moon craters. Blurring past the sample grid
# turns it back into landform, which is all a chart terrain tint should be.
tile = tile.filter(ImageFilter.GaussianBlur(7))
tile.save("chart-terrain.png")
b64 = base64.b64encode(open("chart-terrain.png", "rb").read()).decode()
o.append(f'<g clip-path="url(#neat)"><image href="data:image/png;base64,{b64}" '
         f'x="0" y="0" width="{W}" height="{H}" opacity="0.95" '
         f'style="mix-blend-mode:screen"/></g>')

o.append(f'<g clip-path="url(#neat)">')

# ---- graticule ------------------------------------------------------------
o.append(f'<g stroke="{RULE}" stroke-opacity=".38" stroke-width="0.8">')
lo = math.ceil(LON0)
while lo <= LON1:
    x, _ = xy(lo, 0)
    o.append(f'<line x1="{x:.0f}" y1="{M}" x2="{x:.0f}" y2="{H-M}"/>')
    lo += 1
la = math.ceil(LAT0)
while la <= LAT1:
    _, y = xy(0, la)
    o.append(f'<line x1="{M}" y1="{y:.0f}" x2="{W-M}" y2="{y:.0f}"/>')
    la += 1
o.append('</g>')

# equator, which the route actually crosses
_, yeq = xy(0, 0)
o.append(f'<line x1="{M}" y1="{yeq:.0f}" x2="{W-M}" y2="{yeq:.0f}" stroke="{INK}" '
         f'stroke-opacity=".55" stroke-width="1.6" stroke-dasharray="14 6 3 6"/>')
o.append(f'<text x="{M+14}" y="{yeq-11:.0f}" font-size="15" letter-spacing="4" '
         f'fill="{INK}" fill-opacity=".72">EQUATOR  00°00\'00"</text>')

# ---- water ----------------------------------------------------------------
lakes = json.load(open("ne_10m_lakes.json"))["features"]
for f in lakes:
    d = clip_path(f["geometry"])
    if d:
        o.append(f'<path d="{d}" fill="{WATER_F}" stroke="{WATER_S}" stroke-width="1.1"/>')
rv = json.load(open("rivers.json"))["features"]
for f in rv:
    g = f.get("geometry")
    if not g:
        continue
    ls = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
    for line in ls:
        pts = [xy(x, y) for x, y in line]
        if not any(-200 < a < W + 200 and -200 < b < H + 200 for a, b in pts):
            continue
        o.append('<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) +
                 f'" fill="none" stroke="{WATER_S}" stroke-width="1.5" stroke-opacity=".8"/>')

# ---- international boundary, chain dash ----------------------------------
feats = json.load(open("ne_10m_admin_0_countries.json"))["features"]
kenya = next(f for f in feats if f["properties"].get("ADMIN") == "Kenya")
o.append(f'<path d="{clip_path(kenya["geometry"])}" fill="none" stroke="{INK}" '
         f'stroke-opacity=".42" stroke-width="2.2" stroke-dasharray="22 7 5 7"/>')

# ---- towns ----------------------------------------------------------------
places = json.load(open("pp.json"))["features"]
for f in places:
    lo_, la_ = f["geometry"]["coordinates"]
    if not (LON0 < lo_ < LON1 and LAT0 < la_ < LAT1):
        continue
    pop = f["properties"].get("POP_MAX") or 0
    if pop < 40000:
        continue
    x, y = xy(lo_, la_)
    big = pop > 500000
    r = 6 if big else 3.4
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    if big:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{INK}"/>')
    nm = (f["properties"].get("NAME") or "").upper()
    fs = 15 if big else 12.5
    o.append(f'<rect x="{x+r+3:.1f}" y="{y-9:.1f}" width="{len(nm)*(fs*0.78)+8:.0f}" height="18" '
             f'fill="{GROUND}" fill-opacity=".8"/>')
    o.append(f'<text x="{x+r+7:.1f}" y="{y+4:.1f}" font-size="{fs}" '
             f'letter-spacing="{2.4 if big else 1.6}" fill="{INK}" fill-opacity=".85">{nm}</text>')

# ---- route ----------------------------------------------------------------
pts = [xy(t[1], t[2]) for t in SITES]
o.append('<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) +
         f'" fill="none" stroke="{ORANGE}" stroke-width="3.4" stroke-opacity=".9" '
         f'stroke-linejoin="round"/>')
for i in range(len(SITES) - 1):
    d, brg = gc(SITES[i], SITES[i + 1])
    if d < 45:                      # inside the cluster; the panel carries these
        continue
    (x1, y1), (x2, y2) = pts[i], pts[i + 1]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if ang > 90 or ang < -90:
        ang += 180
    o.append(f'<g transform="translate({mx:.1f},{my:.1f}) rotate({ang:.1f})">'
             f'<rect x="-74" y="-27" width="148" height="21" fill="{GROUND}" fill-opacity=".9"/>'
             f'<text x="0" y="-12" font-size="14.5" letter-spacing="2.2" fill="{ORANGE}" '
             f'text-anchor="middle">{brg:03.0f}°T   {d:.0f} KM   {d*0.53996:.0f} NM</text></g>')

# ---- sites ----------------------------------------------------------------
SHEET_MARKS = False    # HTML buttons instead, so one label shows at a time
for (n, lo_, la_, dx, dy, anc), (x, y) in zip(SITES, pts):
    if not SHEET_MARKS:
        continue
    lx, ly = x + dx, y + dy
    if abs(dy) > 40:                       # fanned out, so it needs a leader
        o.append(f'<polyline points="{x:.1f},{y:.1f} {lx:.1f},{ly+6:.1f}" fill="none" '
                 f'stroke="{INK}" stroke-opacity=".5" stroke-width="1.2"/>')
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{GROUND}" fill-opacity=".6"/>')
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="none" stroke="{ORANGE}" stroke-width="2.4"/>')
    o.append(f'<path d="M{x-7:.1f},{y+3:.1f} L{x:.1f},{y-6:.1f} L{x+7:.1f},{y+3:.1f}" '
             f'fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-linejoin="round"/>')
    lat_s = f'{abs(la_):.2f}°{"N" if la_>=0 else "S"}'
    w = len(n) * 10 + 20
    ox = -w if anc == "end" else 0
    o.append(f'<rect x="{lx+ox-8:.1f}" y="{ly-19:.1f}" width="{w}" height="40" '
             f'fill="{GROUND}" fill-opacity=".82"/>')
    o.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="17" font-weight="600" '
             f'letter-spacing="1.6" fill="{INK}" text-anchor="{anc}">{n}</text>')
    o.append(f'<text x="{lx:.1f}" y="{ly+18:.1f}" font-size="13" letter-spacing="1.8" '
             f'fill="{INK}" fill-opacity=".62" text-anchor="{anc}">{lat_s}  {lo_:.2f}°E</text>')

o.append('</g>')

# ---- neat line and minute ticks ------------------------------------------
o.append(f'<rect x="{M}" y="{M}" width="{W-2*M}" height="{H-2*M}" fill="none" '
         f'stroke="{INK}" stroke-width="2.2"/>')
o.append(f'<rect x="{M-9}" y="{M-9}" width="{W-2*M+18}" height="{H-2*M+18}" fill="none" '
         f'stroke="{INK}" stroke-width="1"/>')
tick = []
lo = LON0
while lo <= LON1:
    x, _ = xy(lo, 0)
    if M < x < W - M:
        long_ = abs(lo - round(lo)) < 1e-6
        L = 11 if long_ else 6
        tick.append(f'<line x1="{x:.1f}" y1="{M}" x2="{x:.1f}" y2="{M+L}"/>')
        tick.append(f'<line x1="{x:.1f}" y1="{H-M}" x2="{x:.1f}" y2="{H-M-L}"/>')
    lo += 1 / 6
la = LAT0
while la <= LAT1:
    _, y = xy(0, la)
    if M < y < H - M:
        long_ = abs(la - round(la)) < 1e-6
        L = 11 if long_ else 6
        tick.append(f'<line x1="{M}" y1="{y:.1f}" x2="{M+L}" y2="{y:.1f}"/>')
        tick.append(f'<line x1="{W-M}" y1="{y:.1f}" x2="{W-M-L}" y2="{y:.1f}"/>')
    la += 1 / 6
o.append(f'<g stroke="{INK}" stroke-width="1.3">' + "".join(tick) + '</g>')

lo = math.ceil(LON0)
while lo <= LON1:
    x, _ = xy(lo, 0)
    if M + 30 < x < W - M - 30:
        o.append(f'<text x="{x:.0f}" y="{M-17}" font-size="14" letter-spacing="2" '
                 f'fill="{INK}" text-anchor="middle">{lo:.0f}°E</text>')
    lo += 1
la = math.ceil(LAT0)
while la <= LAT1:
    _, y = xy(0, la)
    if M + 24 < y < H - M - 24:
        s = f'{abs(la):.0f}°{"N" if la>0 else ("S" if la<0 else "")}' if la else "0°"
        o.append(f'<text x="{M-16}" y="{y+5:.0f}" font-size="14" letter-spacing="2" '
                 f'fill="{INK}" text-anchor="end">{s}</text>')
    la += 1

# ---- compass rose ---------------------------------------------------------
cx, cy, R = W - M - 132, M + 132, 74
o.append(f'<g><circle cx="{cx}" cy="{cy}" r="{R}" fill="{GROUND}" fill-opacity=".8" '
         f'stroke="{INK}" stroke-width="1.6"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{R-13}" fill="none" stroke="{INK}" '
         f'stroke-width="0.8" stroke-opacity=".5"/>')
for deg in range(0, 360, 10):
    a = math.radians(deg - 90)
    L = 13 if deg % 30 == 0 else 7
    o.append(f'<line x1="{cx+math.cos(a)*R:.1f}" y1="{cy+math.sin(a)*R:.1f}" '
             f'x2="{cx+math.cos(a)*(R-L):.1f}" y2="{cy+math.sin(a)*(R-L):.1f}" '
             f'stroke="{INK}" stroke-width="{1.4 if deg%30==0 else 0.8}"/>')
o.append(f'<path d="M{cx},{cy-R+20} L{cx-9},{cy+10} L{cx},{cy+2} L{cx+9},{cy+10} Z" '
         f'fill="{INK}"/>')
o.append(f'<text x="{cx}" y="{cy+R-22}" font-size="13" letter-spacing="3" fill="{INK}" '
         f'text-anchor="middle">TRUE</text></g>')

# ---- scale bar ------------------------------------------------------------
kmpx = 111.32 / S
bx, by = M + 34, H - M - 46
seg = 50 / kmpx
o.append(f'<g><rect x="{bx-14}" y="{by-40}" width="{seg*4+28}" height="60" fill="{GROUND}" '
         f'fill-opacity=".85" stroke="{INK}" stroke-width="0.8"/>')
for i in range(4):
    o.append(f'<rect x="{bx+i*seg:.1f}" y="{by-14}" width="{seg:.1f}" height="9" '
             f'fill="{INK if i%2==0 else GROUND}" stroke="{INK}" stroke-width="1"/>')
for i in range(5):
    o.append(f'<text x="{bx+i*seg:.1f}" y="{by-20}" font-size="12.5" fill="{INK}" '
             f'text-anchor="middle">{i*50}</text>')
o.append(f'<text x="{bx+seg*4+6:.1f}" y="{by+1}" font-size="12.5" letter-spacing="2" fill="{INK}">KM</text>')
o.append('</g>')

# ---- title block ----------------------------------------------------------
tw, th = 430, 104
tx, ty = M + 14, M + 14
o.append(f'<g><rect x="{tx}" y="{ty}" width="{tw}" height="{th}" fill="{GROUND}" '
         f'fill-opacity=".92" stroke="{INK}" stroke-width="1.6"/>'
         f'<line x1="{tx}" y1="{ty+34}" x2="{tx+tw}" y2="{ty+34}" stroke="{INK}" stroke-width="0.9"/>'
         f'<text x="{tx+16}" y="{ty+23}" font-size="15" letter-spacing="4.5" fill="{INK}">'
         f'PARAGLIDING ATLAS</text>'
         f'<text x="{tx+16}" y="{ty+58}" font-size="19" font-weight="600" letter-spacing="1.6" '
         f'fill="{INK}">KENYA  ·  RIFT VALLEY CORRIDOR</text>'
         f'<text x="{tx+16}" y="{ty+82}" font-size="12.5" letter-spacing="2.4" fill="{INK}" '
         f'fill-opacity=".68">WGS 84   ·   SIX SITES   ·   BEARINGS TRUE</text></g>')

o.append('</svg>')
json.dump({n: {"x": round(xy(lo_, la_)[0] / W * 100, 3),
               "y": round(xy(lo_, la_)[1] / H * 100, 3)}
           for n, lo_, la_, *_ in SITES}, open("pos-sheet.json", "w"), indent=1)
open("chart-dark.svg", "w").write("\n".join(o))
print(f"chart {W}x{H}, {len('\n'.join(o))//1024} KB")
for i in range(len(SITES) - 1):
    d, b = gc(SITES[i], SITES[i + 1])
    print(f"   {SITES[i][0]:16s} -> {SITES[i+1][0]:16s} {b:05.1f}°T  {d:6.1f} km")
