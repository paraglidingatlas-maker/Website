"""Figure: Colombia's Cauca Valley in one schematic section. Left, the western
Cordillera with Roldanillo's east-facing launch and the power lines along the
foot of the range; right, the central Cordillera with Piedechinche's
west-facing launch. The Pacific breeze arrives over the western range: a
backwind at Roldanillo, a headwind at Piedechinche. The two sites are about
100 km apart; they share one section here. After Pal Takats. 2400x700."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 700; fig, ax = canvas(W, H)
x = np.linspace(0, W, 600)
def ridge(c, w, h): return h*np.exp(-((x-c)/w)**2)
g = 600 - ridge(300, 330, 360) - ridge(2140, 360, 330) - 12*np.sin(x/37)*np.exp(-((x-1220)/500)**2)
ax.add_patch(Polygon(np.r_[np.c_[x, g], [[W, H], [0, H]]], closed=True, fc=FILL, ec=GR, lw=1.2, zorder=3))
T(ax, 170, 300, "western Cordillera", GR, 13, "center", a=.8)
T(ax, 2250, 320, "central Cordillera", GR, 13, "center", a=.8)
T(ax, 1220, 640, "Cauca Valley", GR, 14, "center", a=.8)
# launches
def launch(xi, lab1, lab2, ha, dx):
    y = np.interp(xi, x, g)
    ax.add_patch(Polygon([(xi-9, y-2), (xi+9, y-2), (xi, y-20)], closed=True, fc=OR, ec="none", zorder=6))
    T(ax, xi+dx, y-60, lab1, WH, 15, ha, fw="bold"); T(ax, xi+dx, y-36, lab2, GR, 12, ha)
launch(560, "Roldanillo", "east-facing launch, flying from about 9 am", "left", 26)
launch(1860, "Piedechinche", "west-facing, thermals from about 10 or 11", "right", -26)
# power lines at the foot of the western range
for px in (700, 760):
    y = np.interp(px, x, g)
    L(ax, [(px, y), (px, y-62)], GR, 1.1, .8, z=5); L(ax, [(px-12, y-56), (px+12, y-56)], GR, 1.1, .8, z=5)
xs = np.linspace(640, 820, 50); L(ax, np.c_[xs, np.interp(xs, x, g)-50-10*np.sin((xs-640)/180*np.pi)], GR, .9, .6, z=5)
T(ax, 845, np.interp(760, x, g)-40, "high-voltage lines along the range", GR, 12, "left", a=.85)
# Pacific breeze
for yy, a in ((150, .95), (190, .6)):
    AR(ax, (60, yy), (430, yy+40), OR, 2.0, a=a)
L(ax, [(430, 190), (620, 330)], OR, 1.6, .7, ls=(0, (6, 5)), z=5)
AR(ax, (600, 318), (640, 350), OR, 1.6, a=.8)
T(ax, 60, 110, "Pacific breeze, arriving from late morning", OR, 14, "left", fw="bold")
T(ax, 640, 250, "a gusty backwind on this launch", OR, 12, "left")
AR(ax, (1380, 480), (1640, 480), OR, 1.8, a=.8)
T(ax, 1330, 510, "a headwind on this one: fly on into the evening", OR, 12, "left")
T(ax, W-20, 680, "schematic: the two sites are about 100 km apart", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "cauca.jpg", bloom=.3)
print("ok")
