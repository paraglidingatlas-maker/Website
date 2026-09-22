"""Sky Gods hero: how the highest flights are made. A range of big mountains
in silhouette (generic, not a named peak), an altitude scale, and one climb:
circling in thermals to 7,600 m, then straight up in wave to 8,400 m, as
Antoine Girard describes his record flight. Right 60%; left 40% empty.
2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 900; fig, ax = canvas(W, H)
def Y(m): return 840 - (m - 2000) / 7000 * 720          # 2,000 m at the bottom, 9,000 m at the top
x = np.linspace(960, 2400, 700)
rng = np.random.default_rng(3)
peaks = [(1180, 4800, 90), (1400, 6100, 110), (1880, 6900, 120), (2160, 6000, 120), (2300, 4300, 100)]
h = np.full_like(x, 2000.) + np.clip((x - 960) / 300, 0, 1) * 1800
for c, top, w in peaks:
    h = np.maximum(h, top - (np.abs(x - c) / w) ** 1.15 * 900)
h += rng.normal(0, 40, len(x)).cumsum() * .02
ax.add_patch(Polygon(np.r_[np.c_[x, [Y(v) for v in h]], [[2400, 900], [960, 900]]], closed=True, fc=FILL, ec=GR, lw=1.0, zorder=2))
for k in range(0, 700, 40):
    L(ax, [(x[k], Y(h[k])), (x[k] + 25, Y(h[k]) + 60)], GR, .5, .15, z=3)
# altitude scale
for m in (2000, 5000, 7600, 8000, 8400):
    L(ax, [(2330, Y(m)), (2370, Y(m))], OR if m in (7600, 8400) else GR, 1, .8, z=5)
    T(ax, 2320, Y(m), "{:,} m".format(m), OR if m in (7600, 8400) else GR, 13, "right", fw="bold" if m == 8400 else "normal")
L(ax, [(2370, Y(2000)), (2370, Y(8600))], GR, .8, .4, z=4)
# the climb: circles in thermals, then a straight rise in wave
cx = 1630
ts = np.linspace(0, 1, 900)
alt = 5000 + ts * (7600 - 5000)
xs = cx + 60 * np.sin(ts * 2 * np.pi * 11) * (1 - .3 * ts)
L(ax, np.c_[xs, [Y(a) for a in alt]], WH, 1.3, .75, z=6)
L(ax, [(cx, Y(7600)), (cx + 40, Y(8400))], OR, 2.4, .95, z=6)
AR(ax, (cx + 34, Y(8250)), (cx + 40, Y(8400)), OR, 2.4)
L(ax, [(cx - 120, Y(7600)), (cx + 420, Y(7600))], OR, .9, .6, ls=(0, (6, 6)), z=5)
T(ax, cx - 90, Y(6200), "thermals", WH, 14, "right")
T(ax, cx + 70, Y(8150), "wave", OR, 14, "left", fw="bold")
T(ax, cx + 420, Y(7600) + 20, "where the thermals stopped", OR, 12, "right")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.65, .25, .35))
print("ok")
