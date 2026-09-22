"""Figure: why a slower top class still means full bar. Two panels of speed
ranges, trim to full bar, as horizontal bars. Before 2011: open-class wings
with a lot of speed that was rarely all used. Today: CCC wings about 20 km/h
slower at the top and used most of the time, while slower wings in the same
gaggle sit pinned at their limit. Schematic, no scale. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
def bar(x0, y, a, b, used, lab, pegged=False, tag_x=None):
    L(ax, [[x0+a, y], [x0+b, y]], GR, 12, .14, z=2)
    L(ax, [[x0+a, y], [x0+used, y]], OR, 12, .9 if pegged or used >= b-2 else .55, z=3)
    ax.add_patch(Rectangle((x0+b-2, y-14), 4, 28, fc=WH, ec="none", zorder=4))
    T(ax, x0+a-18, y, lab, GR, 14, "right")
    if pegged: T(ax, tag_x if tag_x else x0+b+16, y, "pinned at full bar", OR, 13, "left", fw="bold")
# panel 1
x0 = 380
bar(x0, 200, 0, 700, 430, "Open class")
L(ax, [[x0+430, 170], [x0+430, 230]], WH, 1.2, .7, z=5); T(ax, x0+430, 150, "what was usually used", GR, 12, "center")
T(ax, x0+350, 400, "Before 2011", WH, 20, "center", fw="bold"); T(ax, x0+350, 432, "lots of speed, rarely all of it", GR, 14, "center")
# panel 2
x0 = 1500
pace = 520
bar(x0, 150, 0, 560, 520, "CCC")
bar(x0, 215, 0, 470, 470, "EN D", True, x0+pace+24)
bar(x0, 280, 0, 400, 400, "EN C", True, x0+pace+24)
L(ax, [[x0+pace, 115], [x0+pace, 310]], OR, 1.2, .8, ls=(0, (5, 5)), z=5); T(ax, x0+pace, 100, "pace of the lead gaggle", OR, 12, "center")
T(ax, x0+280, 400, "Today", WH, 20, "center", fw="bold"); T(ax, x0+280, 432, "a slower top class, used most of the time", GR, 14, "center")
T(ax, 1200, 560, "Schematic: bar length is speed range from trim to full bar, not to scale", DIM, 12, "center")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "speed.jpg", bloom=.3)
print("ok")
