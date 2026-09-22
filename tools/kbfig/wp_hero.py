"""Weather Patterns hero: a sounding read the simple way. Temperature against
height: the early-morning line bends back on itself near the ground (an
inversion, the thermal killer); the midday line leans over steadily until a
kink where climbs stop; the dew point line comes within three or four
degrees of it where cloud base will be. Schematic, after Ivelin Kalushkov's
Manilla example. Right 60%; left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 900; fig, ax = canvas(W, H)
X0, X1, Y0, Y1 = 1060, 2300, 800, 110          # plot box: x = temperature, y = height
T0, T1, Z1 = -2, 30, 3500
def P(t, z): return (X0 + (t - T0) / (T1 - T0) * (X1 - X0), Y0 - z / Z1 * (Y0 - Y1))
for t in range(0, 31, 5):
    L(ax, [P(t, 0), P(t, Z1)], GR, .5, .08, z=1); T(ax, P(t, 0)[0], Y0 + 26, "%d°" % t, GR, 12, "center", a=.6)
for z in range(0, 3501, 500):
    L(ax, [P(T0, z), P(T1, z)], GR, .5, .08 if z else .3, z=1)
    if z: T(ax, X0 - 16, P(0, z)[1], "{:,} m".format(z), GR, 12, "right", a=.6)
T(ax, X1, Y0 + 56, "temperature", GR, 12, "right", a=.6)
# early morning: inversion near the ground (cold air pooled overnight)
morn = [(16, 0), (13, 800), (14, 1050), (11.8, 1700)]
L(ax, [P(t, z) for t, z in morn], GR, 1.6, .55, ls=(0, (5, 4)), z=4)
L(ax, [(P(14, 1050)[0] + 8, P(14, 1050)[1]), (P(21, 1150)[0] - 8, P(21, 1150)[1])], GR, .8, .5, z=4)
T(ax, P(21, 1150)[0], P(21, 1150)[1] - 4, "8 am: warmer above than below", GR, 13, "left", a=.85)
T(ax, P(21, 1150)[0], P(21, 1150)[1] + 20, "an inversion, the thermal killer", GR, 12, "left", a=.7)
# midday temperature: leaning over steadily, then a kink where climbs stop
mid = [(27.5, 0), (21, 700), (14.5, 1400), (8.3, 2100), (5.3, 2550), (5.8, 2800), (2.5, 3500)]
L(ax, [P(t, z) for t, z in mid], OR, 3, .95, z=6)
# dew point: dry low down, closing in near cloud base, then dropping away
dew = [(12, 0), (10.3, 1000), (8.8, 1700), (5.4, 2250), (2.0, 2650), (-1.5, 3100), (-2, 3500)]
L(ax, [P(t, z) for t, z in dew], WH, 2.2, .85, z=5)
# cloud base and the top of the climbs
zb = 2250
L(ax, [P(T0, zb), P(T1, zb)], WH, 1, .35, ls=(0, (2, 5)), z=3)
cx, cy = P(19, zb)
for dx, dy, r in ((0, -34, 46), (-50, -18, 34), (50, -20, 38), (-20, -58, 34), (28, -52, 30)):
    ax.add_patch(Circle((cx + dx, cy + dy), r, fc=WH, ec="none", alpha=.14, zorder=3))
T(ax, P(19, zb)[0] + 90, P(19, zb)[1] - 30, "cloud base", WH, 15, "left", fw="bold")
T(ax, P(19, zb)[0] + 90, P(19, zb)[1] - 6, "lines within 3 to 4 degrees", GR, 12, "left")
kx, ky = P(5.3, 2550)
ax.add_patch(Circle((kx, ky), 12, fc="none", ec=OR, lw=1.4, zorder=7))
L(ax, [(kx + 14, ky - 6), (kx + 120, ky - 70)], OR, .9, .6, z=6)
T(ax, kx + 130, ky - 80, "the kink: climbs stop here", OR, 14, "left", fw="bold")
T(ax, P(17, 1800)[0], P(17, 1800)[1], "midday: the more it leans,", WH, 13, "left")
T(ax, P(17, 1800)[0], P(17, 1800)[1] + 22, "the better the thermals", GR, 12, "left")
T(ax, P(10.3, 1000)[0] - 16, P(10.3, 1000)[1], "dew point", WH, 13, "right")
T(ax, X1, Y1 - 30, "schematic: after the Manilla forecast in the conversation", GR, 11, "right", a=.55)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.72, .45, .35))
print("ok")
