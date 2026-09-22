"""Figure: two impact curves from a harness drop test. Left: foam or airbag,
a smooth rise to the peak. Right: a crumple protector, flat until it yields,
then a step. Same peak G; very different jerk. 2400x640, two panels."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 640; fig, ax = canvas(W, H)
def panel(x0, kind):
    y0, w, h = 520, 900, 380
    L(ax, [[x0, y0], [x0+w, y0]], GR, 1, .5, z=3); L(ax, [[x0, y0], [x0, y0-h]], GR, 1, .5, z=3)
    T(ax, x0+w, y0+26, "time", DIM, 13, "right"); T(ax, x0-14, y0-h, "G", DIM, 13, "right")
    t = np.linspace(0, 1, 400)
    if kind == "foam":
        g = 1-np.exp(-((t-0.45)/0.16)**2)*0 ; g = np.exp(-((t-0.5)/0.17)**2)      # bell
    else:
        g = np.where(t < 0.36, 0.02+0.06*t, np.exp(-((t-0.52)/0.16)**2)); g[(t >= 0.36) & (t < 0.4)] = np.linspace(0.05, 1.0, ((t >= 0.36) & (t < 0.4)).sum())
    pts = np.c_[x0+40+t*(w-80), y0-20-g*(h-70)]
    L(ax, pts, OR if kind == "foam" else WH, 2.4, .95, z=5)
    # peak marker
    j = np.argmax(g); L(ax, [[x0, pts[j][1]], [pts[j][0], pts[j][1]]], GR, .7, .35, ls=(0, (4, 4)), z=4)
    T(ax, x0-14, pts[j][1], "same peak", DIM, 12, "right")
    return pts
p1 = panel(200, "foam"); p2 = panel(1300, "crumple")
# the slope: mark the rise segment on both
T(ax, 640, 120, "Foam or airbag", WH, 22, "center", fw="bold"); T(ax, 640, 152, "the rise is gradual: low jerk", GR, 14, "center")
T(ax, 1740, 120, "Crumple honeycomb", WH, 22, "center", fw="bold"); T(ax, 1740, 152, "nothing, then a step: high jerk", GR, 14, "center")
# highlight the step
i0 = int(0.36*399); i1 = int(0.40*399)
ax.add_patch(Rectangle((p2[i0][0]-14, p2[i1][1]-10), 40, p2[i0][1]-p2[i1][1]+20, fc="none", ec=OR, lw=1.4, ls=(0, (3, 3)), zorder=6))
AR(ax, (p2[i1][0]+80, p2[i1][1]+60), (p2[i1][0]+30, p2[i1][1]+14), OR, 1.4, 10, 4)
T(ax, p2[i1][0]+92, p2[i1][1]+62, "the corner that breaks vertebrae", OR, 13, "left")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "jerk.jpg", bloom=.35)
print("ok")
