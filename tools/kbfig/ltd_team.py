"""Figure: Damien Lacaze's X-Alps team. The first time there were three of
them; in 2025 there were nine: six supporters in two vans, three in each, the
athlete, his coach Julien at home on the radio and live tracking, and his
mental coach Delphine on the phone. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
def dot(x, y, c, al=.9, r=17): ax.add_patch(Circle((x, y), r, fc=c, ec="none", alpha=al, zorder=4))
# first time: three
T(ax, 330, 150, "THE FIRST TIME", GR, 13, "center", fw="bold")
for i in range(3): dot(270 + i * 60, 300, WH, .75)
T(ax, 330, 370, "a team of three", WH, 16, "center", fw="bold")
L(ax, [(620, 110), (620, 520)], GR, .8, .2)
# 2025: nine
T(ax, 1450, 110, "2025: NINE", OR, 13, "center", fw="bold")
dot(1450, 300, OR, 1, 24); T(ax, 1450, 355, "Damien", WH, 15, "center", fw="bold"); T(ax, 1450, 380, "racing", GR, 12, "center")
for vx, lab in ((900, "van one"), (1150, "van two")):
    ax.add_patch(FancyBboxPatch((vx - 105, 220), 210, 110, boxstyle="round,pad=0,rounding_size=12", fc=FILL, ec=GR, lw=1, alpha=.9, zorder=3))
    for i in range(3): dot(vx - 60 + i * 60, 270, WH, .8)
    T(ax, vx, 360, lab, GR, 12, "center")
T(ax, 1025, 190, "six supporters on the road", WH, 14, "center", fw="bold")
L(ax, [(1260, 275), (1420, 295)], GR, 1, .45, ls=(0, (4, 4)))
for (x, name, role1, role2) in ((1800, "Julien", "coach, at home", "radio and live tracking"), (2120, "Delphine", "mental coach", "by phone when needed")):
    dot(x, 300, WH, .6)
    L(ax, [(1480, 300), (x - 22, 300)], OR, 1, .45, ls=(0, (2, 5)))
    T(ax, x, 355, name, WH, 15, "center", fw="bold"); T(ax, x, 380, role1, GR, 12, "center"); T(ax, x, 402, role2, GR, 12, "center")
T(ax, 1450, 540, "among the supporters, the Sherpa walks with him, carries his non-mandatory kit and flies down: fit, and a good pilot", GR, 13, "center", a=.75)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "team.jpg", bloom=.25)
print("ok")
