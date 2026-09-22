"""Figure: why two lines became possible. Two sections to the same chord: a
profile of 40 years ago at about 10% thickness with four rows of attachment
points, and a modern profile near 18% with only two groups, AA pushed back.
2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
def foil(t, m=.03, p=.35, n=240):
    x = (1-np.cos(np.linspace(0, np.pi, n)))/2
    yt = 5*t*(.2969*np.sqrt(x)-.126*x-.3516*x**2+.2843*x**3-.1036*x**4)
    yc = np.where(x < p, m/p**2*(2*p*x-x**2), m/(1-p)**2*((1-2*p)+2*p*x-x**2))
    return x, yc+yt, yc-yt
def panel(x0, t, pts, lab, sub, note):
    C, y0 = 820, 220
    x, yu, yl = foil(t); U = np.c_[x0+C*x, y0-C*yu]; Lo = np.c_[x0+C*x, y0-C*yl]
    ax.add_patch(Polygon(np.r_[U, Lo[::-1]], closed=True, fc=FILL, ec=WH, lw=1.5, zorder=3))
    for f in np.linspace(.06, .94, 12):
        i = int(np.argmin(abs(x-f))); L(ax, [U[i], Lo[i]], GR, .5, .22, z=4)
    for name, f in pts:
        i = int(np.argmin(abs(x-f))); q = Lo[i]
        L(ax, [q, q+[0, 70]], WH, 1.3, .8, z=2); ax.add_patch(Circle(q, 5, fc=OR, ec="none", zorder=6))
        T(ax, q[0], q[1]+90, name, OR, 15, "center", fw="bold")
    T(ax, x0+C/2, 470, lab, WH, 20, "center", fw="bold"); T(ax, x0+C/2, 502, sub, GR, 14, "center"); T(ax, x0+C/2, 528, note, DIM, 12, "center")
panel(200, .105, [("A", .10), ("B", .33), ("C", .58), ("D", .82)], "Forty years ago", "profile about 9 to 12% of chord", "thin section, four rows to hold its shape")
panel(1320, .18, [("AA", .30), ("BB", .62)], "Today", "profile about 18% of chord", "more volume, more pressure, fewer points")
AR(ax, (1070, 220), (1250, 220), GR, 1.4, 12, 5, .6)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "airfoil.jpg", bloom=.3)
print("ok")
