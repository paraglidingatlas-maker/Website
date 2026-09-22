"""Quote-band image: turning back. A ridge with the wind coming over it, the
rough air in its lee, a pilot's track arriving downwind of it, three frontal
collapses marked, and the track turning away to land. After Honorin Hamard
calling off a record attempt. Schematic. 2400x1000, subject on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
x = np.linspace(900, 2400, 500)
g = 880 - 430*np.exp(-((x-1500)/260)**2) - 180*np.exp(-((x-2150)/300)**2)
ax.add_patch(Polygon(np.r_[np.c_[x, g], [[2400, 1000], [900, 1000]]], closed=True, fc=FILL, ec=GR, lw=1.1, zorder=2))
for yy in (240, 300, 360):
    AR(ax, (960, yy), (1380, yy + 40), GR, 1.4, a=.6)
T(ax, 960, 205, "wind", GR, 13, "left", a=.8)
# rotor in the lee
for r, a in ((70, .5), (110, .35), (150, .22)):
    t = np.linspace(0, 1.7*np.pi, 80)
    L(ax, np.c_[1760 + r*np.cos(t), 560 + .6*r*np.sin(t)], GR, 1, a, z=3)
T(ax, 1700, 790, "rough air downwind of the ridge", GR, 12, "center", a=.8)
# the track
trk = np.array([(2300, 250), (2080, 330), (1900, 430), (1790, 500)])
L(ax, trk, WH, 1.6, .85, z=5)
for k, (px, py) in enumerate([(2020, 360), (1930, 410), (1840, 470)]):
    ax.add_patch(Circle((px, py), 13, fc="none", ec=OR, lw=1.6, zorder=6)); T(ax, px + 18, py - 20, str(k + 1), OR, 12, "left", fw="bold")
back = np.array([(1790, 500), (1860, 560), (1990, 610), (2120, 660), (2230, 700)])
L(ax, back, OR, 2.2, .95, z=6); AR(ax, tuple(back[-2]), tuple(back[-1]), OR, 2.2)
T(ax, 2230, 740, "turn away, land,", OR, 14, "right", fw="bold"); T(ax, 2230, 766, "try another day", OR, 14, "right", fw="bold")
T(ax, 2060, 290, "three frontals", OR, 13, "left")
T(ax, 2380, 975, "schematic", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.3, glow=(.75, .5, .3))
print("ok")
