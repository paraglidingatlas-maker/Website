"""Figure: how far each kind of glider gets from 1,000 m in still air. Glide
paths drawn from one start height to the ground, horizontal distance to scale,
height exaggerated. Paraglider 8 to 11 km, hang glider 16 to 20 km, sailplane
38 to 60 km with the largest open-class ships past 70. 2400x700."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 700; fig, ax = canvas(W, H)
X0, Y0, YG = 230, 140, 470          # start point (1,000 m) and the ground line
K = 2050 / 75.0                      # px per km, 0 to 75 km
gx = lambda km: X0 + km * K
# ground and distance ticks
L(ax, [[X0 - 40, YG], [gx(75), YG]], GR, 1.2, .55)
for km in range(0, 76, 10):
    L(ax, [[gx(km), YG], [gx(km), YG + 10]], GR, 1, .5)
    T(ax, gx(km), YG + 30, "%d km" % km if km else "0", DIM, 12, "center")
# the start height
L(ax, [[X0, Y0], [X0, YG]], GR, 1, .45, ls=(0, (4, 5)))
T(ax, X0 - 18, Y0, "1,000 m", WH, 15, "right", fw="bold")
ax.add_patch(Circle((X0, Y0), 6, fc=WH, ec="none", zorder=6))
def wedge(a, b, fc, ec, alpha, lab, sub, ly, bold=False):
    ax.add_patch(Polygon([[X0, Y0], [gx(a), YG], [gx(b), YG]], closed=True, fc=fc, ec="none", alpha=alpha, zorder=2))
    L(ax, [[X0, Y0], [gx(a), YG]], ec, 1.3, .85, z=3); L(ax, [[X0, Y0], [gx(b), YG]], ec, 1.3, .85, z=3)
    L(ax, [[gx(a), ly], [gx(b), ly]], ec, 2.2, .9, z=4)
    for k in (a, b): L(ax, [[gx(k), ly - 7], [gx(k), ly + 7]], ec, 1.6, .9, z=4)
    T(ax, (gx(a) + gx(b)) / 2, ly + 30, lab, ec, 16, "center", fw="bold")
    T(ax, (gx(a) + gx(b)) / 2, ly + 56, sub, GR, 13, "center")
wedge(38, 60, WH, GR, .06, "Sailplane", "38 to 60 km", 545)
L(ax, [[X0, Y0], [gx(70), YG]], GR, 1, .5, ls=(0, (3, 6)), z=3)
T(ax, gx(70) + 12, YG - 14, "70+ km, the largest", DIM, 12, "left")
wedge(16, 20, WH, WH, .08, "Hang glider", "16 to 20 km", 545)
wedge(8, 11, OR, OR, .22, "Paraglider", "8 to 11 km", 545, True)
T(ax, 1200, 660, "Still air. Horizontal distance to scale; height exaggerated about 12 times.", DIM, 12, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "glide.jpg", bloom=.35)
print("ok")
