"""Figure: where the tubercles go. Two planforms. Left, the first try, with
tubercles across the whole leading edge: good glide, but the tips stalled
quickly and the wing spun early. Right, tubercles on the central 60% of the
span, plain leading edge at the tips. After Gin Seok Song. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
def wing(CX, frac, col):
    SPAN, CH, TE0 = 980, 190, 330
    xs = np.linspace(-1, 1, 800); c = CH*np.clip(1-xs**2, 0, 1)**.42
    te = TE0 + .40*c + 20*xs**2; le = te - c
    bump = np.where(np.abs(xs) <= frac, 6*np.clip(np.sin(xs*np.pi*30), 0, 1)**.8, 0)
    X = CX + SPAN/2*xs
    ax.add_patch(Polygon(np.r_[np.c_[X, le-bump], np.c_[X, te][::-1]], closed=True, fc=FILL, ec=GR, lw=1.1, zorder=3))
    for k in range(0, 800, 32): L(ax, [[X[k], le[k]], [X[k], te[k]]], GR, .5, .2, z=4)
    m = np.abs(xs) <= frac; L(ax, np.c_[X[m], (le-bump)[m]], col, 1.8, .95, z=5)
    return X, le, te
X, le, te = wing(640, 1.0, WH)
for s in (0, -1):
    k = 40 if s == 0 else 759
    ax.add_patch(Circle((X[k], le[k]+16), 34, fc=OR, ec=OR, lw=1.2, alpha=.12, zorder=2))
    ax.add_patch(Circle((X[k], le[k]+16), 34, fc="none", ec=OR, lw=1.2, alpha=.8, zorder=6))
T(ax, 640, 90, "Tubercles along the whole span", WH, 17, "center", fw="bold")
T(ax, 640, 118, "good glide, but the tips stall early", GR, 13, "center")
X, le, te = wing(1760, .6, OR)
y0 = 150
L(ax, [[1760-490*.6, y0+30], [1760+490*.6, y0+30]], OR, 1.0, .75, z=5)
for s in (-1, 1): L(ax, [[1760+s*490*.6, y0+20], [1760+s*490*.6, y0+40]], OR, 1.0, .75, z=5)
T(ax, 1760, 90, "Tubercles on the central 60%", WH, 17, "center", fw="bold")
T(ax, 1760, 118, "the tips keep a plain leading edge", GR, 13, "center")
T(ax, 1200, 560, "planforms, leading edge at the top", GR, 12, "center", a=.6)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "tub.jpg", bloom=.3)
print("ok")
