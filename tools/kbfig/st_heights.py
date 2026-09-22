"""Figure: Marko Milutinovic's two mid-air collisions on one height scale.
France, 2023: hit at about 600 m above the ground; the wing stayed open but
had no brake pressure, and he went down to land. Spain, 2024: hit more than
1,000 m up, tangled and spinning, a slow backflip, the reserve thrown at 400
to 600 m, and a landing between olive trees. 2400x700."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 700; fig, ax = canvas(W, H)
Y0, Y1 = 610, 110
def Y(m): return Y0 - m / 1200 * (Y0 - Y1)
for m in range(0, 1201, 200):
    L(ax, [(420, Y(m)), (2280, Y(m))], GR, .6, .25 if m == 0 else .08, z=1)
    T(ax, 400, Y(m), "{:,} m".format(m), GR, 12, "right", a=.7)
T(ax, 400, Y(1200) - 40, "above the ground", GR, 12, "right", a=.7)
# France
xf = 800
T(ax, xf, 70, "FRANCE, 2023 WORLDS", WH, 14, "center", fw="bold")
L(ax, [(xf, Y(600)), (xf, Y(0))], OR, 2.2, .85, ls=(0, (5, 4)))
ax.add_patch(Circle((xf, Y(600)), 13, fc=OR, ec="none", zorder=5))
T(ax, xf + 30, Y(600) - 12, "hit at about 600 m", WH, 15, "left", fw="bold")
T(ax, xf + 30, Y(600) + 14, "felt like ten seconds, lasted three", GR, 12)
T(ax, xf + 30, Y(350), "wing open but no brake pressure:", GR, 13)
T(ax, xf + 30, Y(350) + 24, "he went down to land", GR, 13)
# Spain
xs = 1650
T(ax, xs, 70, "SPAIN, 2024 EUROPEANS", WH, 14, "center", fw="bold")
ax.add_patch(Circle((xs, Y(1050)), 13, fc=OR, ec="none", zorder=5))
T(ax, xs + 30, Y(1050) - 12, "hit at more than 1,000 m", WH, 15, "left", fw="bold")
T(ax, xs + 30, Y(1050) + 14, "tangled, spinning, a slow backflip", GR, 12)
t = np.linspace(0, 1, 120); zz = 1050 - 550 * t
L(ax, np.c_[xs + 18 * np.sin(t * 40), [Y(z) for z in zz]], OR, 1.6, .7)
ax.add_patch(Rectangle((xs - 60, Y(600)), 120, Y(400) - Y(600), fc=OR, ec="none", alpha=.18, zorder=2))
T(ax, xs + 80, Y(500) - 12, "reserve thrown at 400 to 600 m", WH, 15, "left", fw="bold")
T(ax, xs + 80, Y(500) + 14, "the landing was a gamble either way", GR, 12)
L(ax, [(xs, Y(450)), (xs + 40, Y(0))], GR, 1.4, .7, ls=(0, (3, 4)))
T(ax, xs + 60, Y(0) - 22, "between two olive trees", GR, 12)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "heights.jpg", bloom=.25)
print("ok")
