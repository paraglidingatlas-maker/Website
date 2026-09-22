"""Quote-band image: who is responsible after a competition accident. Four
bodies drawn as boxes, organiser, CIVL, FAI and the pilot, with the lines
between them dashed and a question mark where the workflow should be.
2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
B = {"FAI": (1640, 200), "CIVL": (1640, 420), "Organiser": (1260, 660), "Pilot": (2020, 660)}
sub = {"FAI": "the federation", "CIVL": "the commission", "Organiser": "the event", "Pilot": "the one who launches"}
for k, (x, y) in B.items():
    ax.add_patch(FancyBboxPatch((x-150, y-50), 300, 100, boxstyle="round,pad=0,rounding_size=10", fc=FILL, ec=WH if k != "Pilot" else OR, lw=1.5, zorder=4))
    T(ax, x, y-10, k, WH if k != "Pilot" else OR, 20, "center", fw="bold"); T(ax, x, y+22, sub[k], GR, 12, "center", a=.8)
for a, b in [("FAI", "CIVL"), ("CIVL", "Organiser"), ("CIVL", "Pilot"), ("Organiser", "Pilot")]:
    p, q = np.array(B[a], float), np.array(B[b], float); d = (q-p)/np.linalg.norm(q-p)
    L(ax, [p+d*70, q-d*70], GR, 1.2, .55, ls=(0, (6, 6)), z=3)
ax.add_patch(Circle((1640, 600), 44, fc=BG, ec=OR, lw=1.8, zorder=5)); T(ax, 1640, 600, "?", OR, 34, "center", fw="bold")
T(ax, 1640, 820, "after an accident: who communicates, who decides, who answers", GR, 14, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.3, glow=(.62, .6, .32))
print("ok")
