"""Figure: four paraglider planforms of the same area, drawn from their flat
aspect ratios, so the spans are to scale against each other. Elliptical chord
distribution with a straight quarter-chord line; shape schematic, span to scale.
EN A 4.26 (Ozone Atom 3), EN B 5.3 (Niviuk Hook 6), EN C 6.0 (Ozone Delta 4),
CCC 7.55 (Ozone Enzo 3). 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
S = 24.0                       # m2, the same flat area for all four
PX = 38.0                      # px per metre
wings = [("EN A", 4.26, 40, "4.26"), ("EN B", 5.3, 50, "5.3"), ("EN C", 6.0, 60, "6.0"), ("CCC", 7.55, 100, "7.55")]
for i, (lab, ar, cells, shown) in enumerate(wings):
    cx = 300 + i * 600; cy = 150
    b = np.sqrt(ar * S); cr = 4 * S / (np.pi * b)
    eta = np.linspace(-1, 1, 401); c = cr * np.sqrt(np.clip(1 - eta**2, 0, None))
    c = np.maximum(c, cr * .14)                      # blunt tips, as on a real wing
    y = eta * b / 2 * PX; le = cy + .25 * (cr - c) * PX; te = le + c * PX   # straight quarter-chord, flight direction up
    ax.add_patch(Polygon(np.r_[np.c_[cx + y, le], np.c_[cx + y[::-1], te[::-1]]], closed=True, fc=FILL, ec=WH, lw=1.5, zorder=3))
    for e in np.linspace(-1, 1, cells + 1)[1:-1]:
        j = int((e + 1) / 2 * 400); L(ax, [[cx + y[j], le[j]], [cx + y[j], te[j]]], GR, .5, .18, z=4)
    yb = cy + cr * PX + 40
    L(ax, [[cx - b / 2 * PX, yb], [cx + b / 2 * PX, yb]], OR, 1.6, .9, z=5)
    for s in (-1, 1): L(ax, [[cx + s * b / 2 * PX, yb - 9], [cx + s * b / 2 * PX, yb + 9]], OR, 1.6, .9, z=5)
    T(ax, cx, yb + 28, "span %.1f m" % b, OR, 13, "center")
    T(ax, cx, 470, lab, WH, 20, "center", fw="bold"); T(ax, cx, 502, "flat aspect ratio " + shown, GR, 15, "center")
T(ax, 1200, 575, "All four drawn at the same flat area, 24 m², at one scale. Planform shape schematic.", DIM, 12, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "aspect.jpg", bloom=.3)
print("ok")
