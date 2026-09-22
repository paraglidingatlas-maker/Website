"""Navigators hero: a world map drawn as a technical sheet, with the five
places the six conversations are about marked in orange: the Cauca Valley in
Colombia, Manilla in Australia, Bir and Panchgani in India, and Kijabe in
Kenya. Equirectangular, Natural Earth 1:110m land. Right 60%; left 40% empty.
2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
import nav_land
W, H = 2400, 900; fig, ax = canvas(W, H)
X0, X1, LAT0, LAT1, Y0 = 970, 2390, 72, -56, 190
K = (X1 - X0) / 360.0
def P(lat, lon): return (X0 + (lon + 180) * K, Y0 + (LAT0 - lat) * K)
# graticule
for lon in range(-180, 181, 30): L(ax, [P(LAT0, lon), P(LAT1, lon)], GR, .5, .07, z=1)
for lat in range(-45, 76, 15): L(ax, [P(lat, -180), P(lat, 180)], GR, .5, .07 if lat else .16, z=1)
for ring in nav_land.rings():
    lons = [lo for lo, la in ring]
    if max(lons) - min(lons) > 180:
        continue   # rings drawn across the antimeridian would smear across the map
    pts = [P(la, lo) for lo, la in ring if LAT1 - 5 <= la <= LAT0 + 5]
    if len(pts) > 2:
        ax.add_patch(Polygon(np.clip(pts, [X0, Y0 - 20], [X1, 9999]), closed=True, fc=FILL, ec=GR, lw=.7, alpha=.9, zorder=2))
places = [("Cauca Valley", "Colombia", 4.0, -76.2, (-30, 60), "right"),
          ("Kijabe", "Kenya", -0.93, 36.6, (40, 95), "left"),
          ("Bir", "India", 32.05, 76.72, (-40, -60), "right"),
          ("Panchgani", "India", 17.9, 73.8, (60, 55), "left"),
          ("Manilla", "Australia", -30.75, 150.7, (-60, 70), "right")]
for name, country, la, lo, (dx, dy), ha in places:
    x, y = P(la, lo)
    ax.add_patch(Circle((x, y), 16, fc=OR, ec="none", alpha=.18, zorder=4))
    ax.add_patch(Circle((x, y), 5.5, fc=OR, ec="none", zorder=5))
    tx, ty = x + dx, y + dy
    L(ax, [(x, y), (tx + (8 if ha == "right" else -8), ty)], OR, .9, .6, z=4)
    T(ax, tx, ty - 9, name, WH, 16, ha, fw="bold"); T(ax, tx, ty + 14, country, GR, 12, ha, a=.75)
T(ax, X1, Y0 + (LAT0 - LAT1) * K + 34, "schematic: places named in the conversations", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.75, .5, .35))
print("ok")
