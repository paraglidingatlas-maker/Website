"""The Dark Side hero: a competition task drawn as a briefing sheet. Start
cylinder, turnpoint cylinders, the optimised course line, a goal line, a
sea-breeze arrow field low down and a gradient wind above, and one course
leg left unfinished. Right 60%; left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 900; fig, ax = canvas(W, H)
# terrain contours, faint
rng = np.random.default_rng(7)
for k in range(9):
    xs = np.linspace(980, 2380, 300); y = 620 + k*26 + 30*np.sin(xs/140+k) + 18*np.sin(xs/57+k*2)
    L(ax, np.c_[xs, y], GR, .6, .12, z=1)
cyl = [((1180, 300), 120, "start"), ((1640, 180), 90, "TP1"), ((2120, 360), 110, "TP2"), ((1760, 560), 80, "TP3")]
for (c, r, lab) in cyl:
    ax.add_patch(Circle(c, r, fc=OR, ec="none", alpha=.05, zorder=2)); ax.add_patch(Circle(c, r, fc="none", ec=GR, lw=1.1, alpha=.7, zorder=3))
    ax.add_patch(Circle(c, 4, fc=WH, ec="none", zorder=4)); T(ax, c[0], c[1]-r-16, lab, GR, 13, "center")
# optimised course: tangent-ish points on cylinders
pts = np.array([[1260, 230], [1600, 262], [2020, 380], [1830, 600]])
L(ax, pts, OR, 2.0, .95, z=5)
for p, q in zip(pts[:-1], pts[1:]):
    m = (p+q)/2; d = (q-p)/np.linalg.norm(q-p); AR(ax, m-d*10, m+d*14, OR, 1.6, 12, 5)
# goal line, unfinished leg
g = np.array([1420, 700]); L(ax, [g+[-70, 0], g+[70, 0]], WH, 2.4, .9, z=5); T(ax, g[0], g[1]+24, "goal", GR, 13, "center")
L(ax, [pts[-1], g+[0, -4]], OR, 1.4, .5, ls=(0, (6, 6)), z=5)
# wind: gradient aloft, sea breeze low
for y, n, lab in [(110, 6, "gradient wind aloft"), (790, 8, "sea breeze, strongest low down")]:
    for i in range(n):
        x0 = 1080 + i*(1200/n); AR(ax, (x0+60, y), (x0, y+(10 if y > 400 else -6)), GR, 1.1, 10, 4, .55)
    T(ax, 2340, y+(30 if y > 400 else -28), lab, GR, 12, "right", a=.7)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.02, 1.1, .45))
print("ok")
