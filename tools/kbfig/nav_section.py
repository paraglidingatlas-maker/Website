"""Quote-band image: an isolated plateau with a launch on each of its four
sides, one for every wind direction, drawn as schematic contours, with the flat
country all round and a climb lifting off near the landing paddock rather than
on the face of the hill. After Godfrey Wenness on Mount Borah. Schematic.
2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
C = np.array([1600., 500.])
th = np.linspace(0, 2*np.pi, 400)
def shape(r, k):
    rr = r*(1 + .10*np.sin(3*th+.6) + .06*np.cos(5*th+1.1) + .03*np.sin(9*th+k))
    return np.c_[C[0]+1.25*rr*np.cos(th), C[1]+.95*rr*np.sin(th)]
for i, r in enumerate([330, 285, 240, 200, 165, 135]):
    P = shape(r, i*.3)
    ax.add_patch(Polygon(P, closed=True, fc=FILL if i == 5 else "none", ec=GR, lw=1.0 if i == 5 else .8, alpha=.9 if i == 5 else .45 - .04*i, zorder=2+i))
T(ax, C[0], C[1], "plateau", GR, 13, "center", a=.7)
# four launches on the rim, each facing out
for ang, lab in [(-np.pi/2, "north launch"), (0, "east launch"), (np.pi/2, "south launch"), (np.pi, "west launch")]:
    d = np.array([np.cos(ang), np.sin(ang)]); p = C + d*np.array([1.25*150, .95*150])
    ax.add_patch(Circle(tuple(p), 9, fc=OR, ec="none", zorder=9))
    q = p + d*np.array([150, 120]); AR(ax, tuple(p + d*14), tuple(q), OR, 1.8)
    T(ax, q[0] + d[0]*14, q[1] + d[1]*26 + (0 if d[1] else -2), lab, WH, 14, "center" if d[0] == 0 else ("left" if d[0] > 0 else "right"))
# landing paddock and a flatland climb
LP = np.array([2060., 880.])
ax.add_patch(Rectangle((LP[0]-60, LP[1]-26), 120, 52, fc="none", ec=GR, lw=1, alpha=.7, zorder=4))
T(ax, LP[0]-80, LP[1], "landing paddock", GR, 12, "right", a=.8)
for k in range(5):
    ax.add_patch(Circle((LP[0]+30, LP[1]-70-k*38), 16+k*7, fc="none", ec=OR, lw=1, alpha=.55-.08*k, zorder=4))
T(ax, LP[0]+30, LP[1]-300, "the climb is often out here,", OR, 13, "center"); T(ax, LP[0]+30, LP[1]-276, "not on the face of the hill", OR, 13, "center")
T(ax, 2380, 975, "schematic", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.3, glow=(.68, .5, .3))
print("ok")
