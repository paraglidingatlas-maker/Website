"""Figure: hours in the air a year. Honorin Hamard now flies about 500 hours a
year; Maxime Pinot has flown between 250 and 450 a year for two decades;
pilots building towards the World Cup from scratch fly 400 to 500; and in an
X-Alps season Pinot trained about 450 hours in the air and 450 on foot.
2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
X0, X1 = 760, 2200
def X(h): return X0 + h / 1000 * (X1 - X0)
for h in range(0, 1001, 100):
    L(ax, [(X(h), 90), (X(h), 540)], GR, .6, .12 if h % 500 else .3, z=1)
    T(ax, X(h), 570, "{:,}".format(h), GR, 12, "center", a=.7)
T(ax, X1, 600, "hours a year", GR, 12, "right", a=.7)
rows = [("Honorin Hamard, now", "about 500", [(0, 500, OR, .9)]),
        ("Maxime Pinot, over 20 years", "250 to 450", [(0, 250, OR, .9), (250, 450, OR, .35)]),
        ("Pilots building towards the World Cup", "400 to 500", [(0, 400, WH, .6), (400, 500, WH, .25)]),
        ("Pinot in an X-Alps season", "450 flying + 450 on foot", [(0, 450, OR, .9), (450, 900, GR, .35)])]
for i, (lab, val, segs) in enumerate(rows):
    y = 130 + i * 105
    T(ax, X0 - 30, y, lab, WH, 15, "right", fw="bold"); T(ax, X0 - 30, y + 24, val, GR, 12, "right")
    for a, b, c, al in segs:
        ax.add_patch(Rectangle((X(a), y - 16), X(b) - X(a), 32, fc=c, ec="none", alpha=al, zorder=3))
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hours.jpg", bloom=.25)
print("ok")
