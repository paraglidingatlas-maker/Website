"""Quote-band image: the Keepit blue hole. A schematic plan of the valley in
front of Manilla's launch on Mount Borah, with Lake Keepit to the southwest.
When the wind blows off the lake, from about one o'clock it spills cool air
across the valley and breaks up the thermals. Only the places named in the
conversation are labelled. 2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
rng = np.random.default_rng(3)
# contour-ish ridges of the range behind launch (north-east)
for k, a in enumerate((.35, .25, .18)):
    xx = np.linspace(1500, 2350, 200); yy = 260 + k * 45 - 60 * np.sin((xx - 1500) / 170) - (xx - 1500) * .12
    L(ax, np.c_[xx, yy], GR, 1, a, z=2)
# the lake, south-west
t = np.linspace(0, 2 * np.pi, 200)
lx, ly = 1180 + 150 * np.cos(t) + 25 * np.sin(3 * t), 780 + 80 * np.sin(t) + 18 * np.cos(4 * t)
ax.add_patch(Polygon(np.c_[lx, ly], closed=True, fc="#2b3440", ec=GR, lw=1, alpha=.9, zorder=3))
T(ax, 1180, 785, "Lake Keepit", WH, 16, "center", fw="bold")
# wind off the lake, then a tongue of cool air spreading across the valley
for k in range(4):
    AR(ax, (1010 + k * 30, 930 - k * 40), (1100 + k * 30, 860 - k * 40), GR, 1.3, a=.55)
T(ax, 960, 960, "wind off the lake", GR, 12, "left", a=.8)
tongue = np.array([[1300, 740], [1480, 640], [1700, 560], [1880, 560], [1960, 620], [1850, 700], [1640, 760], [1420, 820]])
ax.add_patch(Polygon(tongue, closed=True, fc=WH, ec="none", alpha=.07, zorder=2))
for x0, y0 in tongue[1:6]:
    pass
xs = rng.uniform(1350, 1950, 260); ys = rng.uniform(560, 800, 260)
from matplotlib.path import Path
inside = Path(tongue).contains_points(np.c_[xs, ys])
ax.scatter(xs[inside], ys[inside], s=3, c=WH, alpha=.25, lw=0, zorder=3)
for k in range(3): AR(ax, (1420 + k * 130, 740 - k * 45), (1500 + k * 130, 700 - k * 45), WH, 1.2, a=.45)
# broken thermals: small crossed-out circles in the tongue, healthy ones outside
for x, y in ((1640, 660), (1780, 620), (1540, 720)):
    ax.add_patch(Circle((x, y), 16, fc="none", ec=GR, lw=1, alpha=.6, ls=(0, (2, 3)), zorder=4))
for x, y in ((2100, 520), (2200, 700), (1420, 480)):
    ax.add_patch(Circle((x, y), 16, fc="none", ec=OR, lw=1.3, alpha=.8, zorder=4))
    AR(ax, (x, y - 18), (x, y - 70), OR, 1.4, a=.8)
# Manilla and the launch
ax.add_patch(Circle((1760, 820), 7, fc=WH, ec="none", zorder=5)); T(ax, 1776, 820, "Manilla", WH, 15, "left", fw="bold")
ax.add_patch(Polygon([[1880, 380], [1900, 350], [1920, 380]], closed=True, fc=OR, ec="none", zorder=5))
T(ax, 1935, 368, "Mount Borah launch", WH, 15, "left", fw="bold")
T(ax, 1720, 560 - 40, "the Keepit blue hole", WH, 15, "center", fw="bold")
T(ax, 1720, 560 - 16, "cool air, broken thermals from about 1 pm", GR, 12, "center")
# north arrow
AR(ax, (2300, 950), (2300, 880), GR, 1.4, a=.7); T(ax, 2300, 862, "N", GR, 13, "center")
T(ax, 2380, 985, "schematic", GR, 11, "right", a=.5)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.35, glow=(.75, .5, .3))
print("ok")
