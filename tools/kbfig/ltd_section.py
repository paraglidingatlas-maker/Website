"""Quote-band image: awkward lines. A ski slope seen from above: the worn
tracks everyone follows from the top of the lift, a stand of birch trees
with a tight gap, and one orange line squeezing through it into untouched
snow, then taking the easy way down from there. After Benjamin Jordan's
story of skiing with a friend. Schematic. 2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
rng = np.random.default_rng(7)
# fresh snow field (stipple) on the right
fx = rng.uniform(1650, 2330, 900); fy = rng.uniform(430, 930, 900)
ax.scatter(fx, fy, s=rng.uniform(1, 5, 900), c=WH, alpha=.18, lw=0, zorder=1)
# the herd: worn tracks down the obvious way
yy = np.linspace(110, 940, 200)
for i in range(16):
    off = rng.normal(0, 38); ph = rng.uniform(0, 6); amp = rng.uniform(20, 45)
    xx = 1300 + off + amp * np.sin(yy / 70 + ph) + (yy - 110) * .08
    L(ax, np.c_[xx, yy], GR, 1.1, .16, z=2)
T(ax, 1225, 80, "the way everyone goes", GR, 14, "center", a=.8)
T(ax, 1225, 104, "same snow, already tracked", GR, 12, "center", a=.6)
# birch trees seen from above: pale trunks with dark marks and faint crowns
trees = [(1600, 300), (1690, 330), (1745, 262), (1560, 390), (1830, 300), (1905, 360), (1640, 205), (1980, 280), (1520, 250), (2050, 350)]
for x, y in trees:
    ax.add_patch(Circle((x, y), 34, fc="#2b2d33", ec=GR, lw=.6, alpha=.55, zorder=3))
    ax.add_patch(Circle((x, y), 8, fc=WH, ec="none", alpha=.85, zorder=4))
    ax.add_patch(Rectangle((x - 5, y - 2), 10, 3, fc=BG, ec="none", alpha=.9, zorder=5))
# the awkward line: from the top, through the gap between (1690, 330) and (1745, 262), then easy turns in fresh snow
t = np.linspace(0, 1, 60)
p0 = np.c_[1330 + 330 * t ** 1.3, 120 + 140 * t]                       # peel off the herd
gap = np.array([[1660, 260], [1718, 296], [1760, 350]])                # squeeze through
yy2 = np.linspace(350, 930, 160)
low = np.c_[1760 + 150 * np.sin((yy2 - 350) / 95) * np.exp(-(yy2 - 350) / 900) + (yy2 - 350) * .22, yy2]
track = np.r_[p0, gap, low]
L(ax, track, OR, 3, .95, z=6)
AR(ax, tuple(track[-3]), tuple(track[-1] + [2, 12]), OR, 2.4, a=.95, z=7)
ax.add_patch(Circle((1718, 296), 26, fc="none", ec=OR, lw=1.2, alpha=.7, ls=(0, (3, 3)), zorder=6))
L(ax, [(1745, 296), (2090, 180)], OR, .8, .5, z=5)
T(ax, 2100, 170, "the awkward line", OR, 16, "left", fw="bold")
T(ax, 2100, 196, "a gap between birch trees", GR, 12, "left")
T(ax, 2100, 216, "you barely fit through", GR, 12, "left")
T(ax, 2150, 640, "fresh snow from there,", WH, 14, "center", fw="bold", a=.85)
T(ax, 2150, 664, "even taking the easy way down", GR, 12, "center", a=.75)
T(ax, 2330, 975, "schematic", GR, 11, "right", a=.5)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.35, glow=(.72, .45, .3))
print("ok")
