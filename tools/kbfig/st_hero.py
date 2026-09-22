"""Storytellers hero: the places in the two stories, drawn as a technical
sheet from the south coast of England to India. West Dorset, where Eddie
Colfox learned; the French Alps and Pegalajar, where Marko Milutinovic was
hit in the 2023 and 2024 championships; Hunza, Bir, Pune and Goa, where
Colfox flew and guided. Equirectangular, Natural Earth 1:110m land.
Right 60%; left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
import nav_land
W, H = 2400, 900; fig, ax = canvas(W, H)
LON0, LON1, LAT0, LAT1 = -12, 84, 58, 10
X0, X1, Y0 = 970, 2390, 105
K = (X1 - X0) / (LON1 - LON0)
def P(lat, lon): return (X0 + (lon - LON0) * K, Y0 + (LAT0 - lat) * K)
YB = P(LAT1, 0)[1]
for lon in range(-10, 81, 10): L(ax, [(P(0, lon)[0], Y0), (P(0, lon)[0], YB)], GR, .5, .08, z=1)
for lat in range(10, 58, 10): L(ax, [(X0, P(lat, 0)[1]), (X1, P(lat, 0)[1])], GR, .5, .08, z=1)
for ring in nav_land.rings():
    lons = [lo for lo, la in ring]
    if max(lons) - min(lons) > 180: continue
    if max(lons) < LON0 - 5 or min(lons) > LON1 + 5: continue
    pts = [P(la, lo) for lo, la in ring]
    if len(pts) > 2:
        ax.add_patch(Polygon(np.clip(pts, [X0, Y0], [X1, YB]), closed=True, fc=FILL, ec=GR, lw=.7, alpha=.9, zorder=2))
places = [("West Dorset", "where Eddie Colfox learned", 50.73, -2.75, (-10, -70), "left", WH),
          ("French Alps", "2023 World Championship", 44.9, 6.2, (70, -60), "left", OR),
          ("Pegalajar", "2024 European Championship", 37.73, -3.65, (-20, 70), "left", OR),
          ("Hunza", "a 200 km out-and-return, 2001", 36.32, 74.65, (-40, -75), "right", WH),
          ("Bir", "flying safaris from 2006", 32.05, 76.72, (-30, 60), "right", WH),
          ("Pune and Goa", "winter seasons", 17.0, 73.9, (-50, 20), "right", WH)]
for name, sub, la, lo, (dx, dy), ha, c in places:
    x, y = P(la, lo)
    ax.add_patch(Circle((x, y), 15, fc=c, ec="none", alpha=.16, zorder=4))
    ax.add_patch(Circle((x, y), 5.5, fc=c, ec="none", zorder=5))
    tx, ty = x + dx, y + dy
    L(ax, [(x, y), (tx + (-8 if ha == "left" else 8), ty)], c, .8, .5, z=4)
    T(ax, tx, ty - 9, name, WH, 16, ha, fw="bold"); T(ax, tx, ty + 14, sub, GR, 12, ha, a=.75)
bx, by = X0, YB + 34
ax.add_patch(Circle((bx + 6, by), 5.5, fc=OR, ec="none")); T(ax, bx + 20, by, "Marko Milutinovic's collisions", GR, 11)
ax.add_patch(Circle((bx + 280, by), 5.5, fc=WH, ec="none")); T(ax, bx + 294, by, "Eddie Colfox's stories", GR, 11)
T(ax, X1, by, "schematic: places named in the conversations", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.72, .45, .35))
print("ok")
