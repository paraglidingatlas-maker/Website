"""Figure: Sandrine Roy's whole flying kit, as she gives it. A wing of about
1.8 kg with unsheathed lines, a 300 g harness and a reserve of about 800 g:
under 3 kg in all, packed with her shoes and waterproof in one 24-litre bike
bag. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
X0, X1 = 520, 2180
def X(kg): return X0 + kg / 3.0 * (X1 - X0)
for g in range(0, 3001, 250):
    kg = g / 1000
    L(ax, [(X(kg), 150), (X(kg), 470)], GR, .6, .3 if g % 1000 == 0 else .1, z=1)
    if g % 500 == 0: T(ax, X(kg), 500, ("{:g} kg".format(kg)), GR, 12, "center", a=.7)
segs = [("Wing", "about 1.8 kg, lines unsheathed", 0, 1.8, OR, .9),
        ("Harness", "300 g", 1.8, 2.1, OR, .55),
        ("Reserve", "about 800 g", 2.1, 2.9, WH, .55)]
y = 300
for name, note, a, b, c, al in segs:
    ax.add_patch(Rectangle((X(a), y - 45), X(b) - X(a) - 4, 90, fc=c, ec="none", alpha=al, zorder=3))
for name, note, a, b, c, al in segs:
    xm = (X(a) + X(b)) / 2
    if name == "Harness":
        L(ax, [(xm, y - 50), (xm, y - 110)], GR, .8, .6); T(ax, xm, y - 140, name, WH, 15, "center", fw="bold"); T(ax, xm, y - 116, note, GR, 12, "center")
    else:
        T(ax, xm, y - 12, name, BG if c == OR else BG, 16, "center", fw="bold", a=.95); T(ax, xm, y + 18, note, BG, 12, "center", a=.9)
L(ax, [(X(3.0), 180), (X(3.0), 440)], OR, 1.6, .9, ls=(0, (6, 4)))
T(ax, X(3.0) + 18, 250, "under 3 kg", OR, 16, "left", fw="bold")
T(ax, X(3.0) + 18, 278, "the whole setup", GR, 12, "left")
T(ax, X0 - 30, y - 12, "Sandrine Roy's", WH, 15, "right", fw="bold"); T(ax, X0 - 30, y + 14, "flying kit", GR, 13, "right")
T(ax, (X0 + X1) / 2, 575, "all of it, with shoes and a waterproof, fits in one 24-litre bike bag; every piece is more than six years old", GR, 13, "center", a=.75)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "kit.jpg", bloom=.25)
print("ok")
