"""Figure: a long glide managed in thirds. Arriving in the top third of the
height band, look at the clouds; in the middle third, clouds and ground; in the
bottom third, only ground triggers, with three or four options ahead. After
Godfrey Wenness. Schematic. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
G, TOP = 540, 110
third = (G - TOP) / 3
for i, (lab, sub) in enumerate([("Top third", "look at the clouds"), ("Middle third", "clouds and the ground"), ("Bottom third", "ground triggers only, three or four options ahead")]):
    y0 = TOP + i*third
    ax.add_patch(Rectangle((150, y0), 2150, third, fc=OR if i == 2 else GR, ec="none", alpha=.06 if i == 2 else .025, zorder=1))
    L(ax, [(150, y0), (2300, y0)], GR, .7, .25, ls=(0, (6, 6)), z=2)
    T(ax, 170, y0+third/2-12, lab, OR if i == 2 else WH, 15, "left", fw="bold"); T(ax, 170, y0+third/2+12, sub, GR, 12, "left")
L(ax, [(150, G), (2300, G)], GR, 1.2, .7, z=3)
for xx in range(170, 2300, 70): L(ax, [(xx, G), (xx-12, G+14)], GR, .6, .2, z=2)
# cloud row and the glide
for cx in (620, 1250, 1900):
    for k, (dx, dy, r) in enumerate([(0, 0, 38), (40, 8, 30), (-38, 10, 28), (18, -18, 26)]):
        ax.add_patch(Circle((cx+dx, 70+dy), r, fc=FILL, ec=GR, lw=.9, alpha=.9, zorder=3))
path = np.array([(560, 130), (1000, 250), (1400, 360), (1760, 470)])
L(ax, path, WH, 1.8, .9, z=5)
AR(ax, tuple(path[-2]), tuple(path[-1]), WH, 1.8)
for i, (tx, lab) in enumerate([(1880, "field on the upslope"), (2060, "tree line"), (2210, "creek bend")]):
    ax.add_patch(Circle((tx, G-6), 7, fc=OR, ec="none", zorder=6)); T(ax, tx, G+34, lab, GR, 11, "center", a=.8)
T(ax, 1760, 500, "options, not a single hope", OR, 12, "right")
T(ax, 2300, 600, "schematic, height above ground", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "thirds.jpg", bloom=.3)
print("ok")
