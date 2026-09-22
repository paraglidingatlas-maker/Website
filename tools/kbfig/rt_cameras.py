"""Figure: where the footage comes from. A pilot in flight with the camera
positions the filmmakers describe: helmet mount, selfie stick or gimbal, a
drone flown by a partner, and a compact camera on a tripod on the ground.
Schematic. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
# ground
L(ax, [[120, 520], [2280, 520]], GR, 1, .4)
# pilot and wing, centre
px, py = 1150, 300
arc = np.array([[px+220*np.cos(t), py-150-70*np.sin(t)] for t in np.linspace(.15, 2.99, 80)])
ax.add_patch(Polygon(np.r_[arc, arc[::-1]+[0, 14]], closed=True, fc=FILL, ec=WH, lw=1.3, zorder=4))
for k in range(0, 80, 13): L(ax, [arc[k]+[0, 14], [px, py]], GR, .6, .4, z=3)
ax.add_patch(Circle((px, py+8), 12, fc=FILL, ec=WH, lw=1.2, zorder=5))
ax.add_patch(Polygon([(px-14, py+20), (px+40, py+26), (px+60, py+56), (px-10, py+52)], closed=True, fc=FILL, ec=WH, lw=1.2, zorder=5))
# helmet cam
ax.add_patch(Rectangle((px-6, py-12), 12, 9, fc=OR, ec="none", zorder=6))
T(ax, px-40, py-30, "helmet mount", OR, 14, "right", fw="bold"); T(ax, px-40, py-8, "easy, but a line can catch it", GR, 12, "right")
# selfie stick
L(ax, [[px+30, py+30], [px+190, py-40]], GR, 1.2, .8, z=5); ax.add_patch(Rectangle((px+186, py-50), 14, 12, fc=OR, ec="none", zorder=6))
T(ax, px+215, py-44, "stick or gimbal", OR, 14, "left", fw="bold"); T(ax, px+215, py-22, "the pilot in frame", GR, 12, "left")
# drone
dx, dy = 1850, 170
ax.add_patch(Rectangle((dx-16, dy-6), 32, 12, fc=OR, ec="none", zorder=6))
for s in (-1, 1): L(ax, [[dx+s*16, dy], [dx+s*40, dy-10]], GR, 1, .8); L(ax, [[dx+s*52, dy-12], [dx+s*28, dy-12]], WH, 1.4, .8)
L(ax, [[dx-20, dy+10], [px+120, py-60]], OR, 1, .45, ls=(0, (5, 6)))
T(ax, dx, dy+40, "drone", OR, 14, "center", fw="bold"); T(ax, dx, dy+62, "flown by someone else", GR, 12, "center")
# tripod on the ground
tx = 420
for s in (-1, 0, 1): L(ax, [[tx, 440], [tx+s*34, 520]], WH, 1.3, .8)
ax.add_patch(Rectangle((tx-20, 424), 40, 22, fc=OR, ec="none", zorder=6))
L(ax, [[tx+20, 430], [px-60, py+40]], OR, 1, .4, ls=(0, (5, 6)))
T(ax, tx, 555, "compact camera on a tripod", OR, 14, "center", fw="bold"); T(ax, tx, 578, "most of the ground story", GR, 12, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "cameras.jpg", bloom=.3)
print("ok")
