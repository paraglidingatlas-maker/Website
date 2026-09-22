"""Figure: rotor downwash near a downed pilot. A helicopter above a slope,
the downwash column spreading along the ground, and a paraglider still
connected to its pilot reinflating in that flow and dragging downhill.
Schematic. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
# slope
sl = np.array([[300, 330], [2200, 560]]); L(ax, sl, GR, 1.2, .6)
for x in range(320, 2200, 60):
    y = 330+(x-300)*(230/1900); L(ax, [[x, y], [x-12, y+14]], GR, .6, .2)
def gy(x): return 330+(x-300)*(230/1900)
# helicopter
hx, hy = 900, 110
ax.add_patch(FancyBboxPatch((hx-90, hy-26), 180, 52, boxstyle="round,pad=0,rounding_size=24", fc=FILL, ec=WH, lw=1.4, zorder=5))
L(ax, [[hx+90, hy-4], [hx+230, hy-12]], WH, 1.4, .9, z=5); L(ax, [[hx-230, hy-44], [hx+230, hy-44]], WH, 2, .9, z=5); L(ax, [[hx, hy-44], [hx, hy-26]], WH, 1.4, .9, z=5)
# downwash column
for dx in (-160, -80, 0, 80, 160):
    AR(ax, (hx+dx, hy+40), (hx+dx*1.2, gy(hx+dx*1.2)-18), OR, 1.4, 12, 5, .8)
for s in (1, -1):
    for k in range(3):
        x0 = hx+s*(230+k*120); AR(ax, (x0, gy(x0)-16-k*4), (x0+s*110, gy(x0+s*110)-12-k*4), OR, 1.2, 10, 4, .6-.12*k)
# pilot and reinflating wing downhill
px = 1500; py = gy(px)
ax.add_patch(Circle((px, py-14), 11, fc=FILL, ec=WH, lw=1.2, zorder=6))
arc = np.array([[px+220+160*np.cos(t), py-70-80*np.sin(t)] for t in np.linspace(.2, 2.9, 80)])
ax.add_patch(Polygon(np.r_[arc, arc[::-1]+[0, 16]], closed=True, fc=FILL, ec=GR, lw=1.1, zorder=4))
for k in range(0, 80, 14): L(ax, [arc[k]+[0, 16], [px+6, py-18]], GR, .6, .4, z=3)
AR(ax, (px+40, py+30), (px+240, gy(px+240)+30), WH, 1.6, 12, 5, .8)
T(ax, px+140, gy(px+140)+62, "a wing still attached can refill and drag", GR, 13, "center")
T(ax, hx, 560, "rotor downwash spreads along the ground", GR, 13, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "downwash.jpg", bloom=.3)
print("ok")
