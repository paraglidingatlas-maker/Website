"""Figure: one idea, and the projects it grew. Benjamin Jordan's 2003 goal as
a novice, to fly from Mexico to Canada, was out of reach, so he boiled it
down to what was left: skateboarding across Canada, then a powered paraglider
across Canada, and finally the free-flying vol-biv from Mexico to Canada,
during COVID. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
nodes = [("The idea, 2003", "a novice's goal:", "fly Mexico to Canada", WH, .5),
         ("What was left", "he could walk and skateboard:", "skateboard across Canada", OR, .9),
         ("The next step", "motor on his back:", "powered paraglider across Canada", OR, .9),
         ("The original idea", "during COVID, free flight:", "Mexico to Canada, vol-biv", OR, .9)]
xs = [330, 900, 1470, 2040]; y = 300
for i, (k, a, b, c, al) in enumerate(nodes):
    x = xs[i]
    ax.add_patch(FancyBboxPatch((x - 250, y - 95), 500, 190, boxstyle="round,pad=0,rounding_size=14", fc=FILL, ec=c, lw=1.4, alpha=1, zorder=3))
    ax.add_patch(FancyBboxPatch((x - 250, y - 95), 500, 190, boxstyle="round,pad=0,rounding_size=14", fc="none", ec=c, lw=1.4, alpha=al, zorder=4))
    T(ax, x, y - 50, k.upper(), c, 13, "center", fw="bold", a=.95)
    T(ax, x, y + 5, a, GR, 14, "center")
    T(ax, x, y + 40, b, WH, 16, "center", fw="bold")
    if i < 3:
        AR(ax, (x + 262, y), (xs[i + 1] - 262, y), OR, 2, a=.9)
# the goal loops back: the last box is the first idea, realised
L(ax, [(xs[3], y + 100), (xs[3], y + 165), (xs[0], y + 165)], GR, 1.2, .45, ls=(0, (5, 5)), z=2)
AR(ax, (xs[0], y + 165), (xs[0], y + 104), GR, 1.2, a=.5, z=2)
T(ax, (xs[0] + xs[3]) / 2, y + 205, "each project taught the skills for the next; the last one was the first idea", GR, 13, "center", a=.75)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "chain.jpg", bloom=.25)
print("ok")
