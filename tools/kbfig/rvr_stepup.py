"""Figure: the speed range of a wing as one bar, from minimum sink through trim
to full bar. Subir Sidhu's rule: you are ready to move up when you are
comfortable across all of it, not just at trim. 2400x520."""
import sys, os; sys.path.insert(0, "os.path.dirname(os.path.abspath(__file__))"); from common import *
W, H = 2400, 520; fig, ax = canvas(W, H)
x0, x1, y = 300, 2100, 250
ax.add_patch(Rectangle((x0, y-16), x1-x0, 32, fc="#1b1c22", ec=GR, lw=.9, zorder=2))
segs = [(0, .18, "min sink", "stall point behind you"), (.18, .42, "trim", "where everyone is comfortable"), (.42, 1.0, "speed bar", "half bar to full bar")]
for a, b, lab, sub in segs:
    xa, xb = x0+(x1-x0)*a, x0+(x1-x0)*b
    ax.add_patch(Rectangle((xa, y-16), xb-xa, 32, fc=OR if lab == "speed bar" else ("#3a3b44" if lab == "trim" else "#2c2d35"), ec="none", alpha=.85 if lab == "speed bar" else 1, zorder=3))
    L(ax, [[xa, y-30], [xa, y+30]], GR, .8, .5, z=4)
    T(ax, (xa+xb)/2, y+66, lab, WH, 24, "center", fw="bold")
    T(ax, (xa+xb)/2, y+100, sub, DIM, 16, "center")
L(ax, [[x1, y-30], [x1, y+30]], GR, .8, .5, z=4)
# the comfortable range of a pilot who is not ready: covers min sink to a bit past trim
ax.add_patch(Rectangle((x0+(x1-x0)*.06, y-52), (x1-x0)*.5, 10, fc=GR, ec="none", alpha=.55, zorder=4))
T(ax, x0+(x1-x0)*.31, y-72, "comfortable today", GR, 17, "center")
# the part still missing, hatched
for xh in np.arange(x0+(x1-x0)*.56, x1, 22):
    L(ax, [[xh, y-52], [xh+10, y-42]], OR, 1.0, .7, z=4)
T(ax, x0+(x1-x0)*.78, y-72, "not yet: learn this first", OR, 17, "center")
# the rule, as a bracket under the whole bar
L(ax, [[x0, y+130], [x0, y+142], [x1, y+142], [x1, y+130]], GR, .9, .6, z=4)
T(ax, (x0+x1)/2, y+178, "Ready to step up when all of this is comfortable in the air you fly in", GR, 19, "center")
# trim speed note: every class is about the same at trim
T(ax, x0+(x1-x0)*.30, y-140, "38 to 40 km/h at trim, from a low B to a CCC. The class shows on the bar.", DIM, 16, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "stepup.jpg", bloom=.3)
print("ok")
