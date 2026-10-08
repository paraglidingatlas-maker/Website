"""Figure: one profile at three angles of attack, on one scale. Too low and the
nose is pushed in and the wing collapses; the flying range between; too high and
the flow breaks away from the top surface and the wing stalls. The oncoming air
is horizontal in all three panels. 2400x700."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 700; fig, ax = canvas(W, H)
def foil(t=.17, m=.04, p=.32, n=200):
    x = (1 - np.cos(np.linspace(0, np.pi, n))) / 2
    yt = 5 * t * (.2969 * np.sqrt(x) - .126 * x - .3516 * x**2 + .2843 * x**3 - .1036 * x**4)
    yc = np.where(x < p, m / p**2 * (2 * p * x - x**2), m / (1 - p)**2 * ((1 - 2 * p) + 2 * p * x - x**2))
    return x, yc + yt, yc - yt
x, yu, yl = foil()
def shape(cx, cy, C, deg, fold=0.0):
    """Chord along +x from the nose; deg > 0 raises the nose (positive angle of attack).
    fold > 0 deflates the front of the profile: the top surface sags onto the bottom."""
    yuu, yll = yu.copy(), yl.copy()
    if fold:
        k = x < fold
        w = (x[k] / fold) ** 1.4
        yuu[k] = yll[k] + (yu[k] - yll[k]) * w
        sag = ((fold - x[k]) / fold) ** 2 * .07
        yuu[k] -= sag; yll[k] -= sag
    a = np.radians(-deg)            # screen y points down, so a nose-up angle is negative here
    pts = lambda yy: np.c_[(x - .3) * C, -yy * C]
    R = np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
    return pts(yuu) @ R.T + [cx, cy], pts(yll) @ R.T + [cx, cy]
def wind(x0, y0, n=5, gap=46, length=170):
    for i in range(n):
        y = y0 + (i - (n - 1) / 2) * gap
        AR(ax, (x0, y), (x0 + length, y), GR, 1.2, 10, 4, .45)
C = 430
panels = [(500, -7, .32), (1240, 5, 0), (1950, 21, 0)]
for i, (cx, deg, fold) in enumerate(panels):
    cy = 300
    U, Lo = shape(cx, cy, C, deg, fold)
    ax.add_patch(Polygon(np.r_[U, Lo[::-1]], closed=True, fc=FILL, ec=WH, lw=1.6, zorder=3))
    wind(cx - 420, cy, 5, 40, 120)
    # chord line and the angle against the oncoming air
    nose = (U[0] + Lo[0]) / 2; tail = (U[-1] + Lo[-1]) / 2
    L(ax, [nose, tail], OR, 1, .55, ls=(0, (4, 4)), z=4)
    L(ax, [nose, nose + [C * .55, 0]], GR, 1, .4, ls=(0, (2, 4)), z=4)
    if i == 0:
        # sinking air on the nose and the folded leading edge
        tip = U[40]
        AR(ax, (tip[0], tip[1] - 140), (tip[0], tip[1] - 14), OR, 2.2, 14, 6, .95)
        T(ax, tip[0] + 16, tip[1] - 130, "sinking air", OR, 13, "left")
        ax.add_patch(Circle(tuple(U[22]), 46, fc="none", ec=OR, lw=1.4, ls=(0, (4, 3)), zorder=6, alpha=.9))
        T(ax, U[22][0] - 40, U[22][1] + 70, "nose folds in", OR, 12, "center")
    if i == 1:
        mid = (U[60] + Lo[60]) / 2
        AR(ax, tuple(mid), (mid[0], mid[1] - 150), OR, 2.4, 16, 7, 1)
        for j in range(3):          # smooth flow over the top
            P = U[::8] + [0, -26 - 22 * j]
            L(ax, np.r_[[P[0] - [140, 0]], P, [P[-1] + [160, 25 + 8 * j]]], GR, 1, .28, z=2)
    if i == 2:
        mid = (U[60] + Lo[60]) / 2
        AR(ax, tuple(mid), (mid[0], mid[1] - 55), OR, 2, 12, 5, .6)
        AR(ax, tuple(tail), (tail[0] + 90, tail[1]), GR, 2, 12, 5, .8)
        for j in range(5):           # the flow breaks away from the top surface and tumbles
            c = U[70 + j * 25] + [10 + j * 14, -34 - j * 10]
            ax.add_patch(Arc(tuple(c), 54 + j * 10, 30 + j * 6, angle=0, theta1=30, theta2=330, color=GR, lw=1, alpha=.38, zorder=2))
T(ax, 500, 560, "Too low", WH, 20, "center", fw="bold"); T(ax, 500, 592, "collapse", OR, 15, "center")
T(ax, 1240, 560, "Flying", WH, 20, "center", fw="bold"); T(ax, 1240, 592, "pressurised, making lift", GR, 15, "center")
T(ax, 1950, 560, "Too high", WH, 20, "center", fw="bold"); T(ax, 1950, 592, "stall", OR, 15, "center")
AR(ax, (700, 640), (1790, 640), DIM, 1.2, 12, 5, .7); AR(ax, (1790, 640), (700, 640), DIM, 1.2, 12, 5, .7)
T(ax, 1245, 668, "angle of attack: the angle between the chord (orange dashes) and the oncoming air", DIM, 12, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "aoa.jpg", bloom=.3)
print("ok")
