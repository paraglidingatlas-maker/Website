"""Figure: the size of the weight problem. A pilot all-up weight axis from 40
to 125 kg; the band drag noodles address (100 to 125 kg, about 5% difference
in performance) against the gap between an extra small and an extra large
(65 to 125 kg, about 20%). 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
x = lambda kg: 300 + (kg-40)*(1800/85)
L(ax, [[x(40), 360], [x(125), 360]], GR, 1.2, .7)
for kg in range(40, 130, 10):
    L(ax, [[x(kg), 352], [x(kg), 368]], GR, 1, .6); T(ax, x(kg), 392, f"{kg}", GR, 13, "center")
T(ax, x(125)+20, 392, "kg", GR, 13, "left")
ax.add_patch(Rectangle((x(100), 250), x(125)-x(100), 60, fc=GR, ec="none", alpha=.25, zorder=2))
T(ax, (x(100)+x(125))/2, 280, "about 5%", WH, 18, "center", fw="bold"); T(ax, (x(100)+x(125))/2, 228, "what drag noodles can adjust", GR, 13, "center")
ax.add_patch(Rectangle((x(65), 150), x(125)-x(65), 60, fc=OR, ec="none", alpha=.22, zorder=2))
L(ax, [[x(65), 150], [x(65), 360]], OR, 1, .5, ls=(0, (5, 5))); L(ax, [[x(125), 150], [x(125), 360]], OR, 1, .5, ls=(0, (5, 5)))
T(ax, (x(65)+x(125))/2, 180, "about 20%", OR, 20, "center", fw="bold"); T(ax, (x(65)+x(125))/2, 128, "extra small against extra large", GR, 13, "center")
T(ax, x(40), 470, "Performance gap by pilot weight", WH, 20, "left", fw="bold"); T(ax, x(40), 502, "Bruce Goldsmith's figures; MRT is aimed at the whole range, down to 40 kg pilots", GR, 14, "left")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "weight.jpg", bloom=.3)
print("ok")
