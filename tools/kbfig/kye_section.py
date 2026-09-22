"""Quote-band image: reserve size against the wing it has to dominate. Three
reserve outlines to scale (20 m2, 30 m2, 40 m2) beside a 25 m2 paraglider
planform, with the wing loading each implies for an 80 kg system. 2400x1000,
subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
SC = 34.0   # px per metre, areas true to scale
# paraglider planform, 25 m2, flat span ~11.5 m, chord ~2.3 m, span horizontal
span, chord = 11.5*SC, 2.3*SC
xs = np.linspace(-1, 1, 300); c = chord*np.clip(1-xs**2, 0, 1)**.42; te = 300 + 0.42*c + 10*xs**2
pl = np.r_[np.c_[1560+span/2*xs, te-c], np.c_[1560+span/2*xs, te][::-1]]
ax.add_patch(Polygon(pl, closed=True, fc=FILL, ec=GR, lw=1.2, alpha=.9, zorder=3))
for k in range(0, 300, 15): L(ax, [pl[k], pl[599-k]], GR, .5, .25, z=4)
T(ax, 1560, 385, "the wing it has to dominate: 25 m²", GR, 14, "center")
# reserves as circles of equal area, to the same scale
for i, (a, lab, note) in enumerate([(20, "20 m²", "passes certification"), (30, "30 m²", "starts to dominate"), (40, "40 m²", "or carry two")]):
    r = np.sqrt(a/np.pi)*SC; cx = 1290 + i*300; cyy = 640
    ax.add_patch(Circle((cx, cyy), r, fc=OR, ec="none", alpha=.06+.08*i, zorder=3))
    ax.add_patch(Circle((cx, cyy), r, fc="none", ec=WH if i == 0 else OR, lw=1.4, zorder=5))
    T(ax, cx, cyy+r+30, lab, WH, 17, "center", fw="bold"); T(ax, cx, cyy+r+54, note, GR, 12, "center", a=.8)
T(ax, 1290, 490, "reserves, same scale", GR, 13, "left", a=.8)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.3, glow=(.62, .6, .32))
print("ok")
