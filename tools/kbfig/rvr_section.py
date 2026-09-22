"""Quote-band image: a paraglider mid asymmetric collapse, drawn as the same
wireframe family, with the reserve handle marked. It sits beside Will Gadd's
line about capacity. 2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, "os.path.dirname(os.path.abspath(__file__))"); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
O = np.array([1720., 420.]); EA, EB, TM, T0 = 420, 300, 80, 34
def mid(t): t = np.radians(t); return O + np.array([EA*np.sin(t), -EB*np.cos(t)])
def nrm(t): t = np.radians(t); v = np.array([EB*np.sin(t), -EA*np.cos(t)]); return v/np.linalg.norm(v)
def thk(t): return T0*np.clip(1-(t/TM)**2, 0, 1)**.38 + .6
# left 55% flying, right 45% folded under: the folded part hangs as a tucked flap
ts = np.linspace(-TM, 22, 260)
outer = [mid(t)+nrm(t)*thk(t)/2 for t in ts]; inner = [mid(t)-nrm(t)*thk(t)/2 for t in ts[::-1]]
ax.add_patch(Polygon(outer+inner, closed=True, fc=FILL, ec=GR, lw=1.3, alpha=.95, zorder=3))
for t in np.linspace(-TM+4, 20, 30): L(ax, [mid(t)-nrm(t)*thk(t)*.42, mid(t)+nrm(t)*thk(t)*.42], GR, .5, .28, z=4)
# collapsed tip: the right 40% folds under the leading edge and hangs as a tucked flap
def bez(P0, P1, P2, P3, n=200):
    tt = np.linspace(0, 1, n)[:, None]; P0, P1, P2, P3 = map(np.array, (P0, P1, P2, P3))
    return (1-tt)**3*P0 + 3*(1-tt)**2*tt*P1 + 3*(1-tt)*tt**2*P2 + tt**3*P3
a0 = mid(22)+nrm(22)*thk(22)/2; b0 = mid(22)-nrm(22)*thk(22)/2
edge = bez(a0, a0+np.array([160, 90]), a0+np.array([120, 300]), b0+np.array([-140, 250]))
back = bez(b0+np.array([-140, 250]), b0+np.array([-120, 150]), b0+np.array([-10, 60]), b0)
fold = np.r_[edge, back]
ax.add_patch(Polygon(fold, closed=True, fc=FILL, ec=GR, lw=1.2, alpha=.9, zorder=3))
for k in range(8, 190, 16): L(ax, [edge[k], back[len(back)-1-int(k*len(back)/200)]], GR, .5, .25, z=4)
# lines: flying side taut to the risers, collapsed side slack
rs = {-1: np.array([1700., 700.]), 1: np.array([1740., 700.])}
for t in np.linspace(-TM+7, 18, 14):
    p = mid(t)-nrm(t)*thk(t)/2; L(ax, [p, rs[-1 if t < 0 else 1]], GR, .7, .5)
for k in range(10, 190, 24):
    p = edge[k]; q = rs[1]; m_ = (p+q)/2 + np.array([30, 40]); L(ax, [p, m_, q], GR, .6, .3)
# pilot in pod harness, rolled towards the collapse
Hh = np.array([1735., 760.])
ax.add_patch(Circle(Hh, 30, fc=FILL, ec=GR, lw=1.2, zorder=5)); ax.add_patch(Circle(Hh+np.array([0, -44]), 11, fc=FILL, ec=GR, lw=1.1, zorder=5))
for sd in (-1, 1): L(ax, [rs[sd], Hh+np.array([sd*12, -20])], GR, 1.0, .8)
# reserve handle, marked
hd = Hh + np.array([-30, 6]); ax.add_patch(Circle(hd, 7, fc=OR, ec=BG, lw=1.4, zorder=8)); ax.add_patch(Circle(hd, 16, fc="none", ec=OR, lw=1, alpha=.55, zorder=8))
# the weight-shift arrow toward the collapsed side, and the pendulum
AR(ax, Hh+np.array([0, 60]), Hh+np.array([70, 60]), OR, 1.8)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.35, glow=(.62, .55, .3))
print("ok")
