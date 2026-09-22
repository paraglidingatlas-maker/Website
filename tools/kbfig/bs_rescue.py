"""Figure: the mirror effect and the stand-up alternative. Left, the reserve
bridled to the shoulders pulls one way while the paraglider, still on the main
carabiners, pulls the other: the pilot is stretched between them on their
back. Right, reserve and wing join at the same point and the pilot sits
upright, able to reach the risers. After Eric Roussel. Schematic. 2400x700."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 700; fig, ax = canvas(W, H)
def reserve(cx, cy, r=120):
    th = np.linspace(np.pi, 2*np.pi, 80)
    top = np.c_[cx+r*np.cos(th), cy+.55*r*np.sin(th)]
    ax.add_patch(Polygon(np.r_[top, [[cx+r, cy], [cx-r, cy]]], closed=True, fc=FILL, ec=WH, lw=1.3, zorder=3))
    return [(cx-r, cy), (cx-r/2, cy), (cx+r/2, cy), (cx+r, cy)]
def wing(cx, cy, w=300, tilt=0):
    t = np.linspace(.12*np.pi, .88*np.pi, 80)
    P = np.c_[cx+w/2*np.cos(t)/np.cos(.12*np.pi), cy-.28*w*np.sin(t)]
    a = np.radians(tilt); R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    P = (P-[cx, cy]) @ R.T + [cx, cy]
    L(ax, P, GR, 7, .55, z=3); L(ax, P, WH, 1.2, .8, z=4)
    return [P[5], P[40], P[75]]
def pilot(hx, hy, ang):
    a = np.radians(ang); d = np.array([np.cos(a), np.sin(a)])
    head = np.array([hx, hy]); hip = head + 70*d
    ax.add_patch(Circle(head, 13, fc=FILL, ec=WH, lw=1.3, zorder=6))
    L(ax, [head+14*d, hip], WH, 2.4, .9, z=6)
    return head+22*d, hip
# ---------------- left: shoulder bridle, mirror effect ----------------
T(ax, 600, 60, "Reserve on the shoulders", WH, 17, "center", fw="bold")
T(ax, 600, 88, "the two canopies pull apart and the pilot ends up on their back", GR, 13, "center")
sh, hip = pilot(520, 470, 8)
feet = hip + np.array([70, 18]); L(ax, [hip, feet], WH, 2.4, .9, z=6)
for p in reserve(300, 250): L(ax, [p, sh], GR, .8, .5, z=2)
for p in wing(880, 250, tilt=10): L(ax, [p, hip], GR, .8, .5, z=2)
AR(ax, (430, 400), (330, 330), OR, 2.0); AR(ax, (720, 400), (820, 320), OR, 2.0)
T(ax, 300, 160, "reserve", GR, 13, "center"); T(ax, 900, 130, "paraglider", GR, 13, "center")
T(ax, 600, 600, "mirror effect", OR, 15, "center", fw="bold")
# ---------------- right: same point, stand up ----------------
T(ax, 1800, 60, "Reserve and wing at the same point", WH, 17, "center", fw="bold")
T(ax, 1800, 88, "the pilot sits upright, legs free, hands on the risers", GR, 13, "center")
J = np.array([1800., 420.])
head = J + np.array([0, 20]); ax.add_patch(Circle(head, 13, fc=FILL, ec=WH, lw=1.3, zorder=6))
seat = head + np.array([0, 90]); L(ax, [head+[0, 14], seat], WH, 2.4, .9, z=6)
knee = seat + np.array([46, 8]); L(ax, [seat, knee, knee+[4, 62]], WH, 2.4, .9, z=6)
for p in reserve(1560, 250): L(ax, [p, J], GR, .8, .5, z=2)
for p in wing(2050, 250, tilt=8): L(ax, [p, J], GR, .8, .5, z=2)
ax.add_patch(Circle(J, 6, fc=OR, ec="none", zorder=7))
T(ax, J[0]+20, J[1]-4, "one attachment point", OR, 13, "left")
T(ax, 1560, 160, "reserve", GR, 13, "center"); T(ax, 2060, 130, "paraglider", GR, 13, "center")
L(ax, [[1200, 120], [1200, 640]], GR, .8, .2, z=1)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "rescue.jpg", bloom=.3)
print("ok")
