"""Quote-band image: caught by the dusk. A schematic section through deep
Karakoram valleys late in the day: the pilot still high in sunlight, the
valleys below already in shadow, the known landing beach by the river out of
reach, and the narrow strip above a gully where Eddie Colfox had to land.
After his 2001 flight in Hunza. 2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
x = np.linspace(900, 2400, 600)
g = 930 - 620*np.exp(-((x-1180)/150)**2) - 520*np.exp(-((x-1850)/170)**2) - 430*np.exp(-((x-2330)/160)**2) - 40*np.sin(x/37)
ax.add_patch(Polygon(np.r_[np.c_[x, g], [[2400, 1000], [900, 1000]]], closed=True, fc=FILL, ec="none", zorder=3))
L(ax, np.c_[x, g], GR, 1.1, .8, z=3)
# sunlight from the left, low: a line above which the air is lit
xf = np.linspace(0, 2400, 200); yf = 360 + (xf - 900) * .12
fade = np.clip((xf - 300) / 600, 0, 1)          # fade the light and shadow in from the left, so no hard edge
for i in range(len(xf) - 1):
    ax.fill_between(xf[i:i + 2], 0, yf[i:i + 2], color=OR, alpha=.07 * fade[i], zorder=1, lw=0)
    ax.fill_between(xf[i:i + 2], yf[i:i + 2], 1000, color="#000000", alpha=.28 * fade[i], zorder=2, lw=0)
ys = 360 + (x - 900) * .12
L(ax, np.c_[x, ys], OR, 1, .35, ls=(0, (6, 6)), z=2)
for k in range(5): AR(ax, (930, 150 + k * 45), (1080, 168 + k * 45), OR, 1.2, a=.5)
T(ax, 930, 120, "low sun", OR, 13, "left", a=.8)
T(ax, 2380, 330, "still sunlit up high", GR, 13, "right", a=.8)
T(ax, 2380, 700, "valleys already in shadow", GR, 13, "right", a=.8)
def G(xx): return float(np.interp(xx, x, g))
# pilot track: coming back high in the light from the right, then a fast glide down into the valley towards the beach
lx = 1615; ly = G(lx) - 6
tr = np.array([[2200, 230], [2020, 245], [1860, 300], [1760, 420], [1700, 560], [1650, 700], [lx, ly]])
L(ax, tr, OR, 3, .95, z=6)
ax.add_patch(Circle(tuple(tr[0]), 9, fc=OR, ec="none", zorder=7))
# the known landing: a beach by the river on the valley floor
bx = 1515; by = G(bx)
ax.add_patch(Rectangle((bx - 45, by - 6), 90, 8, fc=WH, ec="none", alpha=.4, zorder=4))
T(ax, bx - 20, by + 40, "known landing: a beach by the river", GR, 12, "center", a=.8)
ax.add_patch(Circle((lx, ly), 11, fc="none", ec=OR, lw=1.4, zorder=7))
L(ax, [(lx + 14, ly - 4), (1760, 800)], OR, .8, .6, z=6)
T(ax, 1770, 800, "landed short, on a four-metre strip", WH, 13, "left", fw="bold")
T(ax, 1770, 824, "above a gully, by a stone wall", GR, 12, "left")
T(ax, 2380, 975, "schematic", GR, 11, "right", a=.5)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.35, glow=(.35, .2, .3))
print("ok")
