"""Quote-band image: a collapse and two ways back. A wing seen from in front,
flying; the same wing with one side folded; then two outcomes: a damped,
gradual reopening, and an impulsive one that surges and folds the other
side. After Gin Seok Song. 2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
def front(cx, cy, w=360, cut_r=0., cut_l=0., col=WH, a=.85):
    t = np.linspace(.1*np.pi, .9*np.pi, 160)
    P = np.c_[cx+w/2*np.cos(t)/np.cos(.1*np.pi), cy-.36*w*np.sin(t)]
    n = len(P); r0 = int(n*cut_r); l0 = n-int(n*cut_l)
    keep = P[r0:l0]
    L(ax, keep, GR, 8, .45, z=3); L(ax, keep, col, 1.4, a, z=4)
    if r0:   # folded right side (t small = right)
        f = P[:r0][::-1]; fold = np.c_[2*P[r0][0]-f[:, 0]*1+0*f[:, 0], f[:, 1]]
        fold = P[r0] + (f-P[r0])*np.array([-.55, 1.05]) + np.array([0, 18])
        L(ax, fold, col, 1.2, a*.7, ls=(0, (5, 4)), z=4)
    if l0 < n:
        f = P[l0-1:]; fold = P[l0-1] + (f-P[l0-1])*np.array([-.55, 1.05]) + np.array([0, 18])
        L(ax, fold, col, 1.2, a*.7, ls=(0, (5, 4)), z=4)
    for k in range(10, len(P)-10, 20):
        if r0 <= k < l0: L(ax, [P[k], (cx, cy+.62*w)], GR, .6, .28, z=2)
    ax.add_patch(Circle((cx, cy+.62*w+8), 9, fc=FILL, ec=WH, lw=1.1, zorder=5))
front(1140, 470)
T(ax, 1140, 780, "flying", GR, 14, "center")
AR(ax, (1360, 420), (1440, 420), GR, 1.4)
front(1660, 470, cut_r=.42)
T(ax, 1660, 780, "a big asymmetric collapse", GR, 14, "center")
AR(ax, (1860, 330), (1980, 260), WH, 1.6); AR(ax, (1860, 540), (1980, 610), OR, 1.6)
front(2150, 230, w=260)
T(ax, 2150, 432, "reopens gradually, damped", WH, 14, "center")
front(2150, 640, w=260, cut_l=.4, col=OR, a=.95)
T(ax, 2150, 850, "reopens violently: the other side goes", OR, 14, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.32, glow=(.7, .5, .3))
print("ok")
