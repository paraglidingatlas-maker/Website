"""Know Your Equipment hero: a reserve in use. A round canopy above, the
pilot under it, the neutralised paraglider hanging alongside, and the two
speeds that certification allows to be equal: 5.5 m/s down and 5.5 m/s
forward, a 1:1 glide. Right two thirds; left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 900; fig, ax = canvas(W, H)
# ---------- reserve canopy: round, seen side-on, slightly gliding (tilted) ----------
O = np.array([1560., 250.]); RX, RY = 330, 150; tilt = np.radians(-8)
def rot(p): p = np.asarray(p)-O; c, s = np.cos(tilt), np.sin(tilt); return O + np.array([p[0]*c-p[1]*s, p[0]*s+p[1]*c])
th = np.linspace(np.pi, 2*np.pi, 200)
top = np.array([rot((O[0]+RX*np.cos(t), O[1]+RY*np.sin(t))) for t in th])
skirt = np.array([rot((O[0]+RX*np.cos(t), O[1]+26*(1-np.cos(t)**2))) for t in th])   # skirt sags between the gores
# gores
ax.add_patch(Polygon(np.r_[top, skirt[::-1]], closed=True, fc=FILL, ec=WH, lw=1.5, zorder=3))
for f in np.linspace(-1, 1, 13):
    x = O[0]+RX*f; y = O[1]-RY*np.sqrt(max(0, 1-f*f))
    L(ax, [rot((x, O[1])), rot((x, y))], GR, .7, .28, z=4)
L(ax, skirt, GR, 1.0, .6, z=4)
# apex vent
L(ax, [rot((O[0]-22, O[1]-RY)), rot((O[0]+22, O[1]-RY))], BG, 3.5, 1, z=5)
# ---------- pilot ----------
P = np.array([1470., 620.])
for f in np.linspace(-1, 1, 15):
    L(ax, [rot((O[0]+RX*f, O[1])), P+np.array([0, -18])], GR, .7, .5, z=3)
ax.add_patch(Circle(P+np.array([0, -52]), 12, fc=FILL, ec=WH, lw=1.3, zorder=6))
ax.add_patch(Polygon([P+np.array([-16, -38]), P+np.array([20, -34]), P+np.array([34, 6]), P+np.array([2, 24]), P+np.array([-30, 12])], closed=True, fc=FILL, ec=WH, lw=1.3, zorder=6))
# ---------- neutralised paraglider hanging to the left, B-stalled: a crumpled arc with slack lines ----------
Q = np.array([1150., 430.])
arc = np.array([[Q[0]+130*np.cos(t)*0.9+40*np.sin(3*t)*0.15, Q[1]-70*np.sin(t)] for t in np.linspace(0.15, 2.9, 120)])
ax.add_patch(Polygon(np.r_[arc, [arc[-1]+[0, 22], arc[0]+[0, 22]]], closed=True, fc=FILL, ec=GR, lw=1.1, alpha=.9, zorder=3))
for k in range(0, 120, 12): L(ax, [arc[k], arc[k]+[0, 22]], GR, .5, .3, z=4)
for k in range(6, 120, 18):
    p = arc[k]+[0, 22]; m = (p+P)/2 + np.array([-30, 60]); L(ax, np.array([p, m, P+np.array([-14, -20])]), GR, .6, .32, z=2)
# ---------- the vectors ----------
V = np.array([1980., 330.])
AR(ax, V, V+np.array([0, 300]), OR, 2.2)                       # sink
AR(ax, V, V+np.array([300, 0]), OR, 2.2)                       # forward
L(ax, [V, V+np.array([300, 300])], OR, 1.2, .55, ls=(0, (6, 5)), z=5)
ax.add_patch(Polygon([V, V+np.array([300, 0]), V+np.array([300, 300])], closed=True, fc=OR, ec="none", alpha=.07, zorder=2))
T(ax, V[0]-14, V[1]+150, "5.5 m/s down", OR, 15, "right")
T(ax, V[0]+150, V[1]-18, "5.5 m/s forward", OR, 15, "center")
T(ax, V[0]+250, V[1]+255, "a 1:1 glide is allowed", GR, 13, "right")
T(ax, V[0]+250, V[1]+278, "certified, and still gliding", GR, 11, "right", a=.7)
# ---------- labels ----------
T(ax, O[0]+RX+40, O[1]-70, "big enough to dominate the wing,", GR, 13, "left"); T(ax, O[0]+RX+40, O[1]-48, "or it does not work", GR, 13, "left")
T(ax, Q[0], Q[1]+62, "the paraglider, neutralised", GR, 12, "center", a=.8)
# ground reference
L(ax, [[960, 820], [2400, 820]], GR, .8, .25, z=1)
for x in range(980, 2400, 60): L(ax, [[x, 820], [x-12, 834]], GR, .6, .18, z=1)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.02, 1.1, .45))
print("ok")
