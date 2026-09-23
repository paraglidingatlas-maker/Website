"""Heroes for the knowledge base category landing pages: abstract drawings, one
motif per category, in the right 60% with the left 40% dark and empty.
  core-series   contour lines with a single pilot's track looping up in thermals
  competitions  task cylinders and the optimised line through them
  meteorology   isobars round a low with a cold front
  industry      a paraglider planform drawn as a pattern of cells and panels
  technical     an aerofoil section with streamlines and pressure arrows
usage: landing_hero.py <slug> <out.jpg>. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
slug, out = sys.argv[1], sys.argv[2]
W, H = 2400, 900; fig, ax = canvas(W, H)
rng = np.random.default_rng(11)
xs = np.linspace(960, 2400, 360); ys = np.linspace(0, 900, 180); X, Y = np.meshgrid(xs, ys)

def field(n=7, seed=5):
    r = np.random.default_rng(seed); Z = np.zeros_like(X)
    for _ in range(n):
        cx, cy, s, a = r.uniform(1000, 2400), r.uniform(0, 900), r.uniform(150, 380), r.uniform(-1, 1)
        Z += a * np.exp(-(((X - cx) / s) ** 2 + ((Y - cy) / s) ** 2))
    return Z

def fade(alpha):  # soften the left edge of the drawing
    return alpha

if slug == "core-series":
    ax.contour(X, Y, field(9, 3), levels=16, colors=GR, linewidths=.7, alpha=.22, zorder=1)
    t = np.linspace(0, 1, 900)
    base = np.c_[1080 + 1220 * t, 640 - 380 * t + 60 * np.sin(t * 7)]
    loops = np.zeros_like(base)
    for c in (.18, .43, .68, .9):
        w = np.exp(-((t - c) / .035) ** 2)
        loops[:, 0] += 38 * w * np.cos((t - c) * 260); loops[:, 1] += 38 * w * np.sin((t - c) * 260) - 90 * w
    L(ax, base + loops, OR, 2.4, .95, z=4)
    for c in (.18, .43, .68, .9):
        i = int(c * 899); ax.add_patch(Circle(tuple(base[i] + loops[i]), 70, fc=OR, ec="none", alpha=.05, zorder=2))
    ax.add_patch(Circle(tuple(base[0]), 8, fc=OR, ec="none", zorder=5))
elif slug == "competitions":
    ax.contour(X, Y, field(6, 8), levels=10, colors=GR, linewidths=.6, alpha=.12, zorder=1)
    tps = [(1200, 650, 150), (1650, 250, 110), (2050, 560, 90), (2280, 220, 60)]
    for i, (x, y, r) in enumerate(tps):
        ax.add_patch(Circle((x, y), r, fc="none", ec=GR if i else WH, lw=1.3, alpha=.5, ls="-" if i else (0, (6, 5)), zorder=2))
        ax.add_patch(Circle((x, y), 5, fc=GR, ec="none", alpha=.7, zorder=3))
    pts = [(1080, 820), (1290, 530), (1690, 355), (1985, 505), (2242, 262)]
    L(ax, pts, OR, 2.6, .95, z=5)
    for x, y in pts[1:]: ax.add_patch(Circle((x, y), 7, fc=OR, ec="none", zorder=6))
    L(ax, [(2230, 180), (2330, 265)], OR, 3.5, .9, z=6)
elif slug == "meteorology":
    Z = -1.2 * np.exp(-(((X - 1750) / 330) ** 2 + ((Y - 430) / 260) ** 2)) + field(4, 21) * .5
    ax.contour(X, Y, Z, levels=18, colors=GR, linewidths=1, alpha=.3, zorder=1)
    t = np.linspace(0, 1, 300); fx = 1735 - 420 * t + 50 * np.sin(t * 3); fy = 470 + 400 * t ** 1.1   # trailing from the low
    L(ax, np.c_[fx, fy], OR, 2.6, .95, z=4)
    for k in np.linspace(.08, .92, 9):
        i = int(k * 299); dx, dy = fx[i + 1] - fx[i - 1], fy[i + 1] - fy[i - 1]; n = np.hypot(dx, dy); ux, uy = dx / n, dy / n
        tri = [(fx[i] - ux * 14, fy[i] - uy * 14), (fx[i] + ux * 14, fy[i] + uy * 14), (fx[i] + uy * 22, fy[i] - ux * 22)]
        ax.add_patch(Polygon(tri, closed=True, fc=OR, ec="none", alpha=.9, zorder=5))
    T(ax, 1750, 430, "L", WH, 30, "center", fw="bold", a=.6)
elif slug == "industry":
    n = 38; span = 1300; cx0 = 1060; cy0 = 330
    for i in range(n + 1):
        u = i / n; x = cx0 + span * u; ch = 170 * np.sqrt(max(0, 1 - (2 * u - 1) ** 2)) + 20
        ytop = cy0 - 55 * (2 * u - 1) ** 2; L(ax, [(x, ytop), (x, ytop + ch)], GR, .8, .35, z=2)
    u = np.linspace(0, 1, 300); x = cx0 + span * u; ch = 170 * np.sqrt(np.clip(1 - (2 * u - 1) ** 2, 0, 1)) + 20; ytop = cy0 - 55 * (2 * u - 1) ** 2
    L(ax, np.c_[x, ytop], WH, 1.6, .7, z=3); L(ax, np.c_[x, ytop + ch], WH, 1.6, .7, z=3)
    L(ax, np.c_[x, ytop + ch * .22], OR, 1.8, .85, z=4)
    for k in range(0, n + 1, 3):
        uu = k / n; xx = cx0 + span * uu; yb = cy0 - 55 * (2 * uu - 1) ** 2 + 170 * np.sqrt(max(0, 1 - (2 * uu - 1) ** 2)) + 20
        L(ax, [(xx, yb), (1710, 830)], GR, .6, .18, z=1)
    ax.add_patch(Rectangle((1660, 820), 100, 36, fc=FILL, ec=GR, lw=1, alpha=.8, zorder=3))
elif slug == "technical":
    c = 1150; x0, y0 = 1150, 470
    t = np.linspace(0, 1, 200); yt = .15 * 5 * (0.2969 * np.sqrt(t) - 0.126 * t - 0.3516 * t ** 2 + 0.2843 * t ** 3 - 0.1015 * t ** 4)
    camber = .05 * np.where(t < .4, (2 * .4 * t - t ** 2) / .16, ((1 - 2 * .4) + 2 * .4 * t - t ** 2) / .36)
    up = np.c_[x0 + c * t, y0 - c * (camber + yt)]; lo = np.c_[x0 + c * t, y0 - c * (camber - yt)]
    ax.add_patch(Polygon(np.r_[up, lo[::-1]], closed=True, fc=FILL, ec=WH, lw=1.6, alpha=.95, zorder=4))
    for k in range(-6, 7):
        yy = y0 + k * 55; xx = np.linspace(960, 2400, 400)
        bump = -np.sign(k + .01) * 0 + (-70 if k <= 0 else -25) * np.exp(-((xx - (x0 + c * .3)) / 330) ** 2) * np.exp(-abs(k) / 4)
        L(ax, np.c_[xx, yy + bump], GR, .9, .28, z=2)
    for tt in np.linspace(.05, .85, 10):
        i = int(tt * 199); px, py = up[i]; L_ = 80 * (1 - tt) ** 1.5 + 12
        AR(ax, (px, py - 6), (px, py - 6 - L_), OR, 1.6, a=.85, z=5)
else:
    raise SystemExit("unknown slug " + slug)
finish(fig, W, H, out, bloom=.35, glow=(.72, .45, .35))
print("ok")
