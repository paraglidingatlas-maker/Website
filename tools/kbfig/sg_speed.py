"""Figure: the same wing, faster in thin air. Antoine Girard's figures for trim
speed: about 40 km/h at 2,000 m, about 50 in the middle, about 60 at 8,000 m,
so collapses, reactions and landings all happen faster up high. The numbers
follow true airspeed rising as air density falls. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
X0 = 600
def X(v): return X0 + v * 16
rows = [("8,000 m", 60, "collapses and reactions come faster, and less oxygen slows the pilot"),
        ("about 5,000 m", 50, "landing, you touch down at 25 to 30 km/h: hard to run it out"),
        ("2,000 m", 40, "the speed you are used to")]
for i, (alt, v, note) in enumerate(rows):
    y = 150 + i * 150
    T(ax, X0 - 40, y, alt, WH, 17, "right", fw="bold")
    ax.add_patch(Rectangle((X0, y - 20), X(v) - X0, 40, fc=OR if i == 0 else (ORL if i == 1 else GR), ec="none", alpha=.9 if i == 0 else .6, zorder=3))
    T(ax, X(v) + 20, y - 8, "about %d km/h" % v, WH, 15, "left", fw="bold")
    T(ax, X(v) + 20, y + 18, note, GR, 12, "left")
L(ax, [(X0, 100), (X0, 500)], GR, 1, .5, z=2)
T(ax, X0, 560, "trim speed, same wing", GR, 12, "left", a=.7)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "speed.jpg", bloom=.25)
print("ok")
