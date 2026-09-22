"""Figure: Will Gadd's three hazard levels, as a ladder. Consequence on the
left, what you do about it on the right; probability drawn as a thin scale so
the point lands: the row decides, not the odds. 2400x640."""
import sys, os; sys.path.insert(0, "os.path.dirname(os.path.abspath(__file__))"); from common import *
W, H = 2400, 640; fig, ax = canvas(W, H)
rows = [("Bumps and bruises", "Play. Pay attention, nothing more.", .22, GR),
        ("Hospital", "Slow down, keep a hand on the wall, choose the inside of the trail.", .55, ORL),
        ("Death", "Find the line that removes this row before you look at the odds.", 1.0, OR)]
y0, dy = 120, 175
for i, (name, act, w, c) in enumerate(rows):
    y = y0 + i*dy
    ax.add_patch(Rectangle((300, y-40), 1800, 128, fc="#1b1c22", ec=GR, lw=.8, alpha=.9, zorder=2))
    ax.add_patch(Rectangle((300, y-40), 14, 128, fc=c, ec="none", zorder=3))
    T(ax, 350, y-4, name, WH, 30, fw="bold")
    T(ax, 350, y+44, act, GR, 19)
    # consequence bar: length is the weight of the row
    ax.add_patch(Rectangle((1440, y-6), 560*w, 12, fc=c, ec="none", alpha=.9, zorder=4))
    L(ax, [[1440, y+22], [2000, y+22]], GR, .6, .25)
    T(ax, 1440, y+42, "consequence", DIM, 14)
# probability as a small dial off to the side, deliberately minor
cx, cy = 2210, 330
for r in (110, 80):
    ax.add_patch(Arc((cx, cy), 2*r, 2*r, theta1=180, theta2=360, color=GR, lw=.9, alpha=.35, zorder=3))
for k in range(0, 181, 30):
    a = np.radians(k); L(ax, [[cx+80*np.cos(a), cy-80*np.sin(a)], [cx+110*np.cos(a), cy-110*np.sin(a)]], GR, .8, .35)
AR(ax, (cx, cy), (cx+95*np.cos(np.radians(140)), cy-95*np.sin(np.radians(140))), DIM, 1.6)
T(ax, cx, cy+38, "probability", DIM, 15, "center")
T(ax, cx, cy+64, "the second question", DIM, 13, "center", a=.7)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "ladder.jpg", bloom=.35)
print("ok")
