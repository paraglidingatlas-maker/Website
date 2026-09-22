"""Figure: what a model's resolution means, as Ivelin Kalushkov explains it.
The forecast for a point covers the area around it; if rain falls anywhere
inside, the model counts itself right. His figures: GFS about 22 km, ECMWF
about 9 km, NEMS down to 4 km. Circles drawn to scale. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
S = 11.0     # px per km
rows = [("GFS", 22, 560), ("ECMWF", 9, 1260), ("NEMS", 4, 1760)]
cy = 300
for name, km, cx in rows:
    r = km * S
    ax.add_patch(Circle((cx, cy), r, fc=OR, ec=OR, lw=1.4, alpha=.10, zorder=2))
    ax.add_patch(Circle((cx, cy), r, fc="none", ec=OR, lw=1.4, alpha=.8, zorder=3))
    ax.add_patch(Circle((cx, cy), 6, fc=WH, ec="none", zorder=5))
    T(ax, cx, cy + r + 34 if km > 5 else cy + 90, name, WH, 17, "center", fw="bold")
    T(ax, cx, (cy + r + 60) if km > 5 else cy + 116, "about %d km" % km if km != 4 else "down to 4 km", GR, 13, "center")
# a shower at the edge of the GFS circle still counts as a hit
sx, sy = 560 + 22 * S * .72, cy - 22 * S * .55
for dx, dy, rr in ((0, 0, 20), (-18, 8, 14), (18, 8, 15)):
    ax.add_patch(Circle((sx + dx, sy + dy), rr, fc=WH, ec="none", alpha=.35, zorder=4))
for k in range(4): L(ax, [(sx - 16 + k * 11, sy + 24), (sx - 20 + k * 11, sy + 40)], WH, 1.2, .6, z=4)
L(ax, [(sx + 30, sy - 10), (sx + 170, sy - 60)], GR, .8, .5)
T(ax, sx + 180, sy - 70, "rain here still counts", WH, 13, "left", fw="bold")
T(ax, sx + 180, sy - 46, "as a correct forecast for the centre", GR, 12, "left")
L(ax, [(2040, 520), (2040 + 10 * S, 520)], GR, 2, .7); T(ax, 2040 + 5 * S, 548, "10 km", GR, 12, "center")
T(ax, 2240, 590, "his figures, as he gives them", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "res.jpg", bloom=.25)
print("ok")
