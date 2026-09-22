"""Brand Stories hero: a design sheet. A paraglider planform with tubercles
along the central 60% of the leading edge (the wave leading edge Gin Seok Song
describes), and below it a pod harness in section with its crushable protector
and the carabiner it hangs from. Right 60%; left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 900; fig, ax = canvas(W, H)
# ---------- sheet grid, faint, right side only ----------
for x in range(1000, 2400, 80): L(ax, [[x, 60], [x, 860]], GR, .5, .05, z=1)
for y in range(60, 900, 80): L(ax, [[1000, y], [2400, y]], GR, .5, .05, z=1)
# ---------- planform ----------
CX, TE0, SPAN, CH = 1690, 330, 1180, 250
xs = np.linspace(-1, 1, 900)
c = CH*np.clip(1-xs**2, 0, 1)**.42
te = TE0 + 0.40*c + 26*xs**2
le = te - c
bump = np.where(np.abs(xs) <= .6, 7*np.clip(np.sin(xs*np.pi*34), 0, 1)**.8, 0)
le_w = le - bump
X = CX + SPAN/2*xs
pl = np.r_[np.c_[X, le_w], np.c_[X, te][::-1]]
ax.add_patch(Polygon(pl, closed=True, fc=FILL, ec=GR, lw=1.2, alpha=.95, zorder=3))
for k in range(0, 900, 30): L(ax, [[X[k], le[k]], [X[k], te[k]]], GR, .5, .22, z=4)
m = np.abs(xs) <= .6
L(ax, np.c_[X[m], le_w[m]], OR, 2.0, .95, z=5)
# 60% dimension line
y0 = le.min() - 60
L(ax, [[CX-SPAN/2*.6, y0], [CX+SPAN/2*.6, y0]], OR, 1.0, .7, z=5)
for s in (-1, 1): L(ax, [[CX+s*SPAN/2*.6, y0-10], [CX+s*SPAN/2*.6, y0+10]], OR, 1.0, .7, z=5)
T(ax, CX, y0-24, "tubercles on the central 60% of the span", OR, 14, "center")
T(ax, CX+SPAN/2*.86, le[int(900*.93)]-40, "plain tips", GR, 12, "center", a=.75)
# ---------- harness in section ----------
HX, HY = 1500, 690
body = [(HX-260, HY-40), (HX-150, HY-78), (HX+40, HY-70), (HX+330, HY-40), (HX+470, HY-6), (HX+330, HY+30), (HX+40, HY+44), (HX-160, HY+40), (HX-250, HY+14)]
ax.add_patch(Polygon(body, closed=True, fc=FILL, ec=WH, lw=1.3, alpha=.95, zorder=3))
# protector block: crushable tubes, drawn as a hex-ish grid under the seat
px0, py0 = HX-200, HY+44
for i in range(14):
    for j in range(3):
        cx = px0 + i*22 + (11 if j % 2 else 0); cy = py0 + 10 + j*17
        ax.add_patch(Circle((cx, cy), 9, fc="none", ec=OR if j == 0 else GR, lw=.9, alpha=.8 if j == 0 else .5, zorder=4))
L(ax, [[px0-14, py0], [px0+310, py0], [px0+320, py0+56], [px0-4, py0+56], [px0-14, py0]], GR, .8, .5, z=4)
T(ax, px0+400, py0+30, "a protector that crushes", GR, 13, "left", a=.85)
T(ax, px0+400, py0+52, "rather than springs back", GR, 12, "left", a=.7)
# carabiner detail
KX, KY = 1240, 560
ax.add_patch(FancyBboxPatch((KX-24, KY-52), 48, 104, boxstyle="round,pad=0,rounding_size=24", fc="none", ec=WH, lw=1.6, zorder=5))
L(ax, [[KX+24, KY-30], [KX+24, KY+12]], BG, 4, 1, z=6)
L(ax, [[KX+20, KY-34], [KX+30, KY+8]], WH, 1.4, .9, z=7)
T(ax, KX, KY+82, "carabiner", GR, 12, "center", a=.8)
L(ax, [[KX, KY+52], [HX-230, HY-30]], GR, .6, .3, ls=(0, (4, 4)), z=2)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.72, .35, .35))
print("ok")
