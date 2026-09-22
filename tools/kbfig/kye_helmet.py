"""Figure: what EN 966 tests, in three panels: the 1.5 m drop with the 250 G
limit, the penetration test with its 5 mm gap, and the 5 mm rule for
anything on the shell. 2400x600."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 600; fig, ax = canvas(W, H)
def helmet(cx, cy, r=110, open_face=True):
    th = np.linspace(np.pi*1.02, np.pi*2.05, 80)
    ax.add_patch(Polygon(np.c_[cx+r*np.cos(th), cy+r*0.92*np.sin(th)], closed=True, fc=FILL, ec=WH, lw=1.6, zorder=4))
    th2 = np.linspace(np.pi*1.06, np.pi*2.0, 60)
    L(ax, np.c_[cx+(r-22)*np.cos(th2), cy+(r-22)*0.92*np.sin(th2)], GR, .8, .4, z=5)     # liner
    ax.add_patch(Circle((cx, cy+8), r-44, fc="#1b1c22", ec=GR, lw=.8, zorder=3))         # head form
# 1: drop
cx = 420; helmet(cx, 330)
AR(ax, (cx-200, 90), (cx-200, 210), OR, 2.0)
L(ax, [[cx-230, 90], [cx-170, 90]], GR, 1, .6); L(ax, [[cx-230, 240], [cx-170, 240]], GR, 1, .6)
T(ax, cx-215, 165, "1.5 m", OR, 18, "right", fw="bold")
T(ax, cx, 470, "Drop test", WH, 20, "center", fw="bold"); T(ax, cx, 500, "head form must see under 250 G", GR, 14, "center")
T(ax, cx, 526, "a good new helmet: 170 to 180 G", DIM, 12, "center")
# 2: penetration
cx = 1200; helmet(cx, 330)
ax.add_patch(Polygon([(cx, 226), (cx-16, 160), (cx+16, 160)], closed=True, fc=OR, ec="none", zorder=6))
L(ax, [[cx, 160], [cx, 100]], OR, 2, .9, z=6); AR(ax, (cx, 40), (cx, 90), OR, 1.6, 10, 4)
L(ax, [[cx+130, 236], [cx+130, 248]], OR, 1.4, .9, z=6); T(ax, cx+142, 242, "5 mm gap", OR, 14, "left", fw="bold")
T(ax, cx, 470, "Penetration", WH, 20, "center", fw="bold"); T(ax, cx, 500, "a falling point must stop 5 mm short of the head", GR, 14, "center")
T(ax, cx, 526, "vented bike and climbing shells fail here", DIM, 12, "center")
# 3: nothing sticks out
cx = 1980; helmet(cx, 330)
ax.add_patch(Rectangle((cx-14, 214), 28, 26, fc="#2a2b33", ec=OR, lw=1.4, zorder=6))
L(ax, [[cx+40, 214], [cx+40, 236]], OR, 1.2, .9, z=6); T(ax, cx+50, 225, "5 mm max", OR, 14, "left", fw="bold")
# a line that could snag
L(ax, [[cx-300, 120], [cx-20, 214]], GR, .8, .4, ls=(0, (4, 4)))
T(ax, cx, 470, "Nothing to snag", WH, 20, "center", fw="bold"); T(ax, cx, 500, "shell parts, mounts and cameras: 5 mm or less", GR, 14, "center")
T(ax, cx, 526, "a line round a camera is the failure mode", DIM, 12, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "helmet.jpg", bloom=.3)
print("ok")
