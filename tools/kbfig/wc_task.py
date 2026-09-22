"""Figure: how a race task is scored. A course from launch through the start
cylinder (SSS), turnpoints, the end of speed section (ESS) and goal, with the
three games marked: distance along the whole course, time only between SSS
and ESS, leading across the same stretch. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
P = {"launch": (200, 300), "SSS": (520, 300), "TP1": (1000, 180), "TP2": (1480, 330), "ESS": (1900, 250), "goal": (2160, 250)}
rad = {"SSS": 150, "TP1": 90, "TP2": 90, "ESS": 110}
for k, r in rad.items():
    ax.add_patch(Circle(P[k], r, fc=OR if k in ("SSS", "ESS") else "none", ec=GR, lw=1.1, alpha=.08 if k in ("SSS", "ESS") else .7, zorder=2))
    ax.add_patch(Circle(P[k], r, fc="none", ec=GR, lw=1.1, alpha=.7, zorder=2))
route = [P["launch"], (P["SSS"][0]+150, 300), (P["TP1"][0], 270), (P["TP2"][0]-60, 260), (P["ESS"][0]-110, 250), P["goal"]]
L(ax, route, WH, 1.6, .8, z=4)
for k, p in P.items():
    ax.add_patch(Circle(p, 5, fc=OR if k in ("SSS", "ESS", "goal") else WH, ec="none", zorder=5)); T(ax, p[0], p[1]-(rad.get(k, 30))-18, k, WH if k in ("SSS", "ESS", "goal") else GR, 15, "center", fw="bold" if k in ("SSS", "ESS", "goal") else "normal")
L(ax, [[2160, 215], [2160, 285]], WH, 2.6, .9, z=5)
def span(x1, x2, y, lab, sub, c):
    L(ax, [[x1, y], [x2, y]], c, 6, .85, z=3); T(ax, x1, y+30, lab, c, 16, "left", fw="bold"); T(ax, x1, y+54, sub, GR, 13, "left")
span(200, 2160, 450, "Distance", "how far along the course you got, launch to goal", WH)
span(670, 1790, 520 - 10, "Time and leading", "only between the start of speed (SSS) and its end (ESS): how fast, and how far in front", OR)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "task.jpg", bloom=.3)
print("ok")
