"""New Technologies hero: a two-liner section drawn as a technical sheet. A
thick modern airfoil with its two load-bearing line groups (AA set far back,
BB behind), the old A point kept as an unloaded line for launching, the nose
ahead of AA drawn flexing (dashed), and a sensor trace underneath standing for
the harness that watches the wing. Right 60%; left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 900; fig, ax = canvas(W, H)
X0, Y0, C = 1080., 300., 1120.            # leading edge and chord in px
def foil(t=.18, m=.035, p=.35, n=300):
    x = (1-np.cos(np.linspace(0, np.pi, n)))/2
    yt = 5*t*(.2969*np.sqrt(x)-.126*x-.3516*x**2+.2843*x**3-.1036*x**4)
    yc = np.where(x < p, m/p**2*(2*p*x-x**2), m/(1-p)**2*((1-2*p)+2*p*x-x**2))
    return x, yc+yt, yc-yt
x, yu, yl = foil()
U = np.c_[X0+C*x, Y0-C*yu]; Lo = np.c_[X0+C*x, Y0-C*yl]
ax.add_patch(Polygon(np.r_[U, Lo[::-1]], closed=True, fc=FILL, ec=WH, lw=1.7, zorder=3))
# ribs / cell hatching
for f in np.linspace(.06, .94, 16):
    i = int(np.argmin(abs(x-f))); L(ax, [U[i], Lo[i]], GR, .6, .22, z=4)
# flexing nose ahead of AA: a dashed, slightly dropped leading edge
xa = .30
m = x < xa
nose_u = U[m].copy(); nose_l = Lo[m].copy()
d = (1-x[m]/xa)**1.6
L(ax, nose_u+np.c_[d*6, d*22], OR, 1.3, .8, ls=(0, (6, 5)), z=5)
L(ax, nose_l+np.c_[d*6, d*16], OR, 1.3, .8, ls=(0, (6, 5)), z=5)
T(ax, X0-10, Y0-200, "the nose may flex:", OR, 13, "left"); T(ax, X0-10, Y0-178, "the wing pitches and speeds up", OR, 13, "left")
L(ax, [[X0+10, Y0-166], [X0+40, Y0-70]], OR, .8, .5)
# attachment points on the lower surface
def lp(f): i = int(np.argmin(abs(x-f))); return Lo[i]
R = np.array([1560., 800.])                  # riser / pilot
aa, bb, old = lp(.30), lp(.62), lp(.10)
L(ax, [aa, R+[-14, 0]], WH, 1.6, .9, z=2); L(ax, [bb, R+[14, 0]], WH, 1.6, .9, z=2)
L(ax, [old, R+[-20, 0]], GR, .9, .5, ls=(0, (3, 5)), z=2)
for p in (aa, bb): ax.add_patch(Circle(p, 6, fc=OR, ec="none", zorder=6))
ax.add_patch(Circle(old, 5, fc=BG, ec=GR, lw=1.2, zorder=6))
T(ax, aa[0]+14, aa[1]+34, "AA", OR, 17, "left", fw="bold"); T(ax, bb[0]+14, bb[1]+34, "BB", OR, 17, "left", fw="bold")
T(ax, old[0]-16, old[1]+40, "old A point:", GR, 12, "right"); T(ax, old[0]-16, old[1]+60, "no load, kept for launch", GR, 12, "right")
T(ax, R[0]+30, R[1]+4, "two load-bearing groups", GR, 13, "left")
# thickness dimension
it = int(np.argmin(abs(x-.30)))
xt = U[it][0]
L(ax, [[xt, U[it][1]], [xt, Lo[it][1]]], WH, 1.2, .8, z=5); L(ax, [[xt-10, U[it][1]], [xt+10, U[it][1]]], WH, 1.2, .8, z=5)
T(ax, xt+22, (U[it][1]+Lo[it][1])/2-10, "about 18% of chord", GR, 13, "left")
# sensor trace strip along the bottom
tx = np.linspace(1020, 2320, 700); rng = np.random.default_rng(3)
sig = 12*np.sin(tx/37)+5*np.sin(tx/11)+rng.normal(0, 1.4, tx.size)
spike = (tx > 2020)&(tx < 2200); sig[spike] += 55*np.sin((tx[spike]-2020)/180*np.pi)*np.sin((tx[spike]-2020)/9)
L(ax, np.c_[tx, 860+sig*.6], OR, 1.0, .75, z=3)
T(ax, 2320, 828, "100 readings a second", GR, 12, "right", a=.75)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.02, 1.1, .45))
print("ok")
