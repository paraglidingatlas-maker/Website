"""Figure: harness drag measured by Supair, three silhouettes side-on with a
bar each: chair about 23 N, foil-faired pod about 12 N, submarine about 8 N.
2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
def pilot(cx, cy, kind):
    ax.add_patch(Circle((cx-70, cy-52), 20, fc=FILL, ec=WH, lw=1.3, zorder=5))
    if kind == "chair":
        body = [(-95, -30), (-40, -38), (10, 0), (70, 10), (80, 60), (40, 70), (-10, 40), (-80, 30)]
        legs = [(40, 10), (100, 30), (106, 88), (90, 90), (80, 46)]
        ax.add_patch(Polygon(np.array(legs)+[cx, cy], closed=True, fc=FILL, ec=GR, lw=1.1, zorder=4))
    elif kind == "pod":
        body = [(-100, -30), (-30, -40), (80, -18), (230, 5), (250, 22), (220, 40), (60, 50), (-60, 40), (-100, 20)]
    else:
        body = [(-110, -44), (-20, -58), (120, -30), (270, 0), (300, 20), (270, 34), (100, 44), (-60, 38), (-112, 10)]
    ax.add_patch(Polygon(np.array(body)+[cx, cy], closed=True, fc=FILL, ec=WH, lw=1.4, zorder=4))
    L(ax, [[cx-60, cy-40], [cx-40, cy-240]], GR, .8, .4, z=3)
items = [("chair", "Chair", "about 23 N", 23), ("pod", "Pod with a fairing", "about 12 N", 12), ("sub", "Submarine", "about 8 N", 8)]
for i, (k, lab, val, n) in enumerate(items):
    cx = 360 + i*800; pilot(cx, 300, k)
    y = 420; L(ax, [[cx-160, y], [cx-160+23*20, y]], GR, 10, .12, z=2); L(ax, [[cx-160, y], [cx-160+n*20, y]], OR, 10, .9, z=3)
    T(ax, cx-160, 470, lab, WH, 20, "left", fw="bold"); T(ax, cx-160, 502, val + " of drag", GR, 14, "left")
T(ax, 360-160, 540, "Supair's drag figures for pilot and harness; drawings schematic", DIM, 12, "left")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "drag.jpg", bloom=.3)
print("ok")
