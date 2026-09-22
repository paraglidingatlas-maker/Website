"""Figure: the altitude scale where hypoxia starts to matter, with the two
multipliers that shrink your margin (cold, time) and the hangover after
descending. From Dr Matt Wilkes. 2400x760."""
import sys, os; sys.path.insert(0, "os.path.dirname(os.path.abspath(__file__))"); from common import *
W, H = 2400, 760; fig, ax = canvas(W, H)
# vertical altitude axis on the left third
x = 520; top, bot = 80, 680
def Y(m): return bot - (bot-top)*(m/6000)
L(ax, [[x, top], [x, bot]], GR, 1.2, .7, z=3)
for m in range(0, 6001, 1000):
    L(ax, [[x-14, Y(m)], [x+14, Y(m)]], GR, .9, .6, z=3); T(ax, x-30, Y(m), f"{m:,} m", GR, 16, "right")
# bands
ax.add_patch(Rectangle((x+20, Y(3500)), 560, Y(3000)-Y(3500), fc=OR, ec="none", alpha=.22, zorder=2))
ax.add_patch(Rectangle((x+20, Y(6000)), 560, Y(3500)-Y(6000), fc=OR, ec="none", alpha=.38, zorder=2))
T(ax, x+40, Y(3250), "most pilots start to be affected", WH, 18)
T(ax, x+40, Y(4700), "impaired, and not aware of it", WH, 18)
T(ax, x+40, Y(1500), "fine", GR, 18)
L(ax, [[x+20, Y(2600)], [x+580, Y(2600)]], GR, .8, .5, ls=(0, (4, 4)), z=3)
T(ax, x+40, Y(2600)-16, "general aviation: 30 min above 3,000 m, or any time above 4,000 m", DIM, 14)
# the multipliers, as three cards on the right
cards = [("Cold", "Shivering multiplies the oxygen your body burns by about five. Staying warm is margin.", "x5"),
         ("Time", "Each hour up high draws down bandwidth, and repeated days stack the fatigue.", "hrs"),
         ("After", "Back down low you feel better, but you are not back to full for up to 90 minutes.", "90 min")]
for i, (h, b, big) in enumerate(cards):
    cx = 1280 + i*370; cy = 150
    ax.add_patch(Rectangle((cx, cy), 330, 420, fc="#1b1c22", ec=GR, lw=.8, alpha=.9, zorder=2))
    ax.add_patch(Rectangle((cx, cy), 330, 4, fc=OR, ec="none", zorder=3))
    T(ax, cx+165, cy+90, big, OR, 58, "center", fw="bold")
    T(ax, cx+24, cy+165, h, WH, 24, fw="bold")
    import textwrap
    for k, line in enumerate(textwrap.wrap(b, 26)):
        T(ax, cx+24, cy+210+k*32, line, GR, 17)
# the self-check: a note on the cockpit
T(ax, 1280, 630, "The check: a note on the cockpit asking what you are thinking.", DIM, 15)
T(ax, 1280, 660, "Mood, thermalling precision and speech change first.", DIM, 15)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "altitude.jpg", bloom=.3)
print("ok")
