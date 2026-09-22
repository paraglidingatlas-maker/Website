"""Quote-band image: a wing planform marked up the way a test lab marks it.
The big asymmetric collapse field: 50% of the trailing edge, a fold line at
45 degrees to the open side, stickers on the bottom surface, and a folding
line to pull it. 2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
cx, span, chord = 1600., 1180., 300.
xs = np.linspace(-1, 1, 400); c = chord*np.clip(1-xs**2, 0, 1)**.42; le = 330+10*xs**2 - .15*c; te = le + c
X = cx+span/2*xs
ax.add_patch(Polygon(np.r_[np.c_[X, le], np.c_[X, te][::-1]], closed=True, fc=FILL, ec=WH, lw=1.5, zorder=3))
for k in range(0, 400, 16): L(ax, [[X[k], le[k]], [X[k], te[k]]], GR, .5, .22, z=4)
# collapse field on the right half: TE from tip to 50% of TE length, fold running at 45 deg forward to the LE
xte = cx+span/2*0.0         # 50% of the trailing edge from the right tip = centre of the span
i0 = int(np.argmin(abs(X-xte))); p_te = np.array([X[i0], te[i0]])
# walk 45 deg forward-right until LE
t = np.linspace(0, 1, 400); line = p_te + np.c_[t*600, -t*600]
j = next(k for k, q in enumerate(line) if q[1] <= le[int(np.argmin(abs(X-q[0])))])
p_le = line[j]
iL = int(np.argmin(abs(X-p_le[0])))
field = np.r_[[p_te], [p_le], np.c_[X[iL:], le[iL:]], np.c_[X[i0:], te[i0:]][::-1]]
ax.add_patch(Polygon(field, closed=True, fc=OR, ec="none", alpha=.14, zorder=4))
L(ax, [p_te, p_le], OR, 2.2, .95, z=6)
# stickers along the fold
for f in np.linspace(.12, .88, 5):
    q = p_te+(p_le-p_te)*f; ax.add_patch(Rectangle(q-[9, 9], 18, 18, fc=OR, ec="none", alpha=.85, zorder=7))
# 45 deg arc
ax.add_patch(Arc(p_te, 120, 120, theta1=-45, theta2=0, color=OR, lw=1.3, zorder=6))
T(ax, p_te[0]+72, p_te[1]-16, "45°", OR, 16, "left", fw="bold")
# 50% dimension along TE
y = te.max()+70
L(ax, [[X[i0], y], [X[-1], y]], GR, 1, .7); L(ax, [[X[i0], y-10], [X[i0], y+10]], GR, 1, .7); L(ax, [[X[-1], y-10], [X[-1], y+10]], GR, 1, .7)
T(ax, (X[i0]+X[-1])/2, y+26, "50% of the trailing edge, ±2.5", GR, 14, "center")
# folding line to the riser
L(ax, [p_le+[20, 6], [cx+120, 880]], OR, 1.2, .7, ls=(0, (6, 5)), z=5)
T(ax, cx+140, 900, "folding line: pulls the fold where the norm wants it", GR, 13, "left")
T(ax, cx-span/2+40, le.min()-40, "open side", GR, 13, "left", a=.8)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.3, glow=(.62, .6, .32))
print("ok")
