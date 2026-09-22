"""Figure: millibars to metres, the rule of thumb. Start at 1,000 millibars
at sea level; every 100 millibars less is about 1,000 metres higher: 900 is
about 1,000 m, 800 about 2,000 m and 700 about 3,000 m. Forecasts give the
wind at a pressure, because that is how balloons report it. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
X0, X1 = 420, 2140
def X(mb): return X0 + (1000 - mb) / 300 * (X1 - X0)
ya, yb = 250, 400
L(ax, [(X0 - 40, ya), (X1 + 40, ya)], GR, 1.2, .5)
L(ax, [(X0 - 40, yb), (X1 + 40, yb)], GR, 1.2, .5)
T(ax, X0 - 70, ya, "pressure", GR, 13, "right"); T(ax, X0 - 70, yb, "height", GR, 13, "right")
for mb, m in ((1000, "sea level"), (900, "about 1,000 m"), (800, "about 2,000 m"), (700, "about 3,000 m")):
    x = X(mb)
    L(ax, [(x, ya), (x, yb)], OR, 1.6, .75, ls=(0, (4, 4)))
    ax.add_patch(Circle((x, ya), 8, fc=OR, ec="none", zorder=5)); ax.add_patch(Circle((x, yb), 8, fc=WH, ec="none", zorder=5))
    T(ax, x, ya - 38, "%d mb" % mb, WH, 18, "center", fw="bold")
    T(ax, x, yb + 38, m, WH if mb != 1000 else GR, 16, "center", fw="bold" if mb != 1000 else "normal")
ax.add_patch(Rectangle((X(900), 470), X(700) - X(900), 16, fc=OR, ec="none", alpha=.35, zorder=3))
T(ax, (X(900) + X(700)) / 2, 510, "the range most flying forecasts need", GR, 13, "center")
T(ax, X(850), 150, "every 100 millibars less is about 1,000 metres higher", GR, 14, "center", a=.8)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "mb.jpg", bloom=.2)
print("ok")
