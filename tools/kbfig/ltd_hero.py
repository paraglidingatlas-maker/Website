"""Living The Dream hero: Sandrine Roy's human-powered route around the world,
drawn as a technical sheet. A Pacific-centred map (seam in the mid-Atlantic,
where she sailed across) with the countries she names, in her order: from the
south of France west by bike and boat through Central America, across the
Pacific, through Australia and Asia to India, then the planned way home
(dashed). Natural Earth 1:110m land. Right 60%; left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
import nav_land
W, H = 2400, 900; fig, ax = canvas(W, H)
X0, X1, LAT0, LAT1, Y0 = 970, 2390, 72, -56, 190
SEAM = -30.0
K = (X1 - X0) / 360.0
def wrap(lon): return lon + 360 if lon < SEAM else lon
def P(lat, lon): return (X0 + (wrap(lon) - SEAM) * K, Y0 + (LAT0 - lat) * K)
for lon in range(-30, 331, 30): L(ax, [(X0 + (lon - SEAM) * K, Y0), (X0 + (lon - SEAM) * K, Y0 + (LAT0 - LAT1) * K)], GR, .5, .07, z=1)
for lat in range(-45, 76, 15): L(ax, [(X0, P(lat, 0)[1]), (X1, P(lat, 0)[1])], GR, .5, .07 if lat else .16, z=1)
for ring in nav_land.rings():
    lons = np.array([lo for lo, la in ring])
    shift = 360 if (lons < SEAM).mean() > .5 else 0
    pts = [(X0 + ((lo + shift) - SEAM) * K,
            Y0 + (LAT0 - la) * K) for lo, la in ring if LAT1 - 5 <= la <= LAT0 + 5]
    if len(pts) > 2:
        ax.add_patch(Polygon(np.clip(pts, [X0, Y0 - 20], [X1, 9999]), closed=True, fc=FILL, ec=GR, lw=.7, alpha=.9, zorder=2))
done = [(43.6, 3.9), (39.6, 2.9), (36.1, -5.35), (28.3, -15.5)]
americas = [(9.0, -79.5), (10.0, -84.1), (12.1, -86.3), (14.1, -87.2), (13.7, -89.2), (14.6, -90.5), (19.4, -99.1), (33.5, -117.5),
            (-9.0, -139.5), (-17.6, -149.4), (-21.2, -159.8), (-13.8, -171.8), (-17.8, 178.0), (-30.75, 150.7), (-12.46, 130.84),
            (-8.41, 116.46), (3.1, 101.7), (13.75, 100.5), (18.0, 102.6), (25.0, 102.7), (29.65, 91.1), (28.2, 85.6), (32.05, 76.72)]
planned = [(32.05, 76.72), (33.7, 73.0), (32.6, 51.7), (33.3, 44.4), (29.4, 47.9), (24.7, 46.7), (30.0, 31.2), (38.0, 23.7), (41.3, 19.8),
           (40.6, 17.0), (42.0, 12.5), (45.9, 6.9), (43.6, 3.9)]
def pl(seq): return [P(a, b) for a, b in seq]
d = pl(done); am = pl(americas); pn = pl(planned)
yseam = Y0 + (LAT0 - 19) * K
L(ax, d + [(X0 + 4, yseam)], OR, 2.2, .95, z=5)            # Canaries, out over the Atlantic
L(ax, [(X1 - 4, yseam)] + am, OR, 2.2, .95, z=5)         # back in, to Panama and on
L(ax, pn, OR, 1.8, .7, ls=(0, (4, 4)), z=5)
T(ax, X0 + 10, yseam - 22, "sailed across", GR, 11, "left", a=.7)
T(ax, X1 - 10, yseam - 22, "the Atlantic", GR, 11, "right", a=.7)
for x, y in d + am[:-1] + pn[1:-1]:
    ax.add_patch(Circle((x, y), 3.2, fc=WH, ec="none", alpha=.8, zorder=6))
for x, y in (d[0], am[-1]):
    ax.add_patch(Circle((x, y), 15, fc=OR, ec="none", alpha=.18, zorder=6))
    ax.add_patch(Circle((x, y), 6, fc=OR, ec="none", zorder=7))
labels = [("Home", "south of France", 43.6, 3.9, (-10, -125), "left"),
          ("Canary Islands", "", 28.3, -15.5, (-20, 75), "left"),
          ("Panama", "", 9.0, -79.5, (40, 55), "left"),
          ("Marquesas", "", -9.0, -139.5, (-40, -10), "right"),
          ("Fiji", "", -17.8, 178.0, (20, 60), "left"),
          ("Australia", "", -30.75, 150.7, (-40, 45), "right"),
          ("Indonesia", "", -8.41, 116.46, (-45, 50), "right"),
          ("Nepal", "", 28.2, 85.6, (-60, 90), "right"),
          ("Bir, India", "", 32.05, 76.72, (60, -70), "left")]
for name, sub, la, lo, (dx, dy), ha in labels:
    x, y = P(la, lo); tx, ty = x + dx, y + dy
    L(ax, [(x, y), (tx + (-6 if ha == "left" else 6), ty)], GR, .7, .45, z=4)
    T(ax, tx, ty, name, WH, 14, ha, fw="bold")
    if sub: T(ax, tx, ty + 20, sub, GR, 11, ha, a=.7)
bx, by = X0 + 10, Y0 + (LAT0 - LAT1) * K + 34
L(ax, [(bx, by), (bx + 40, by)], OR, 2.2, .95); T(ax, bx + 50, by, "so far", GR, 11)
L(ax, [(bx + 130, by), (bx + 170, by)], OR, 1.8, .7, ls=(0, (4, 4))); T(ax, bx + 180, by, "planned: Pakistan to Egypt, by boat to Greece, then Italy and the Alps", GR, 11)
T(ax, X1, by, "schematic: countries named in the conversation, in her order", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.72, .5, .35))
print("ok")
