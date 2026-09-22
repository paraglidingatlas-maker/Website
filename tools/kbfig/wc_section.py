"""Quote-band image: multi radius turnpoints. One turnpoint with three
concentric cylinders, the smallest for the heaviest class and the largest for
the lightest, and the course lines each class flies to tag its own edge.
2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
C = np.array([1720., 500.])
start = np.array([1060., 820.]); nxt = np.array([2300., 780.])
for r, lab, col in [(300, "lightest pilots: biggest cylinder", OR), (210, "middle", ORL), (120, "heaviest pilots: smallest cylinder", WH)]:
    ax.add_patch(Circle(C, r, fc="none", ec=col, lw=1.4, alpha=.85, zorder=3))
    d = (start-C)/np.linalg.norm(start-C); e = (nxt-C)/np.linalg.norm(nxt-C); m = (d+e)/np.linalg.norm(d+e)
    tag = C + m*r
    L(ax, [start, tag, nxt], col, 1.4, .7, z=4); ax.add_patch(Circle(tag, 6, fc=col, ec="none", zorder=5))
ax.add_patch(Circle(C, 4, fc=WH, ec="none", zorder=5))
T(ax, C[0]+320, C[1]-240, "lightest pilots: biggest cylinder", OR, 14, "left")
T(ax, C[0]+240, C[1]-150, "middle", ORL, 14, "left")
T(ax, C[0]+140, C[1]-60, "heaviest: smallest", WH, 14, "left")
T(ax, start[0], start[1]+34, "from the last turnpoint", GR, 12, "center"); T(ax, nxt[0], nxt[1]+34, "to the next", GR, 12, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.3, glow=(.62, .6, .32))
print("ok")
