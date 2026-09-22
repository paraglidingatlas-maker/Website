"""World Cups hero: forty tracklogs from a race start converging on one
turnpoint cylinder, tagging its edge and bending away, one leading track a
little ahead in orange. Right 60%; left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 900; fig, ax = canvas(W, H)
C = np.array([1700., 440.]); R = 170
ax.add_patch(Circle(C, R, fc=OR, ec="none", alpha=.05, zorder=1)); ax.add_patch(Circle(C, R, fc="none", ec=GR, lw=1.2, alpha=.7, zorder=2))
ax.add_patch(Circle(C, 4, fc=WH, ec="none", zorder=3)); T(ax, C[0], C[1]-R-18, "turnpoint", GR, 13, "center")
rng = np.random.default_rng(11)
tan = C + np.array([-R*.2, -R*.98])          # tag point near the top of the cylinder
for k in range(40):
    y0 = 520 + rng.normal(0, 90); x0 = 1080 + rng.normal(0, 20)
    pts = [np.array([x0, y0])]
    tgt = tan + rng.normal(0, 14, 2)
    for t in np.linspace(0, 1, 30)[1:]:
        p = pts[0]*(1-t) + tgt*t + np.array([0, 60*np.sin(t*np.pi)*rng.normal(0, .5)]) + rng.normal(0, 3, 2)
        pts.append(p)
    ex = tgt + np.array([420, 180]) + rng.normal(0, 40, 2)
    for t in np.linspace(0, 1, 20)[1:]:
        pts.append(tgt*(1-t) + ex*t + rng.normal(0, 3, 2))
    P = np.array(pts); lead = k == 0
    if lead: P = P + np.array([60, -6])
    L(ax, P, OR if lead else GR, 1.8 if lead else .7, .95 if lead else .28, z=4 if lead else 3)
T(ax, 2330, 820, "one thermal ahead is what leading points pay for", GR, 12, "right", a=.75)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.02, 1.1, .45))
print("ok")
