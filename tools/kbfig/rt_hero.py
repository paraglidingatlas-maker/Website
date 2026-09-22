"""Resources, Tools & Tips hero: a breathing trace drawn as an instrument
line. Short inhales, longer exhales, the amplitude settling as it runs to the
right, with a small paraglider silhouette riding the calmer end. Right 60%;
left 40% empty. 2400x900."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 900; fig, ax = canvas(W, H)
x = np.linspace(1000, 2340, 1400)
def breath(u):
    ph = u % 1.0                     # 35% of each cycle in, 65% out
    return np.where(ph < .35, np.sin(ph/.35*np.pi/2), np.cos((ph-.35)/.65*np.pi/2))
per = 170 + (x-1000)*0.14
cyc = np.cumsum(np.gradient(x)/per)
amp = 170*np.exp(-(x-1000)/900) + 45
y = 520 - amp*breath(cyc)
L(ax, np.c_[x, y], OR, 2.0, .9, z=4)
for k in range(1, 7):
    L(ax, [[1000, 520-k*40], [2340, 520-k*40]], GR, .5, .08, z=1)
L(ax, [[1000, 520], [2340, 520]], GR, .8, .3, z=1)
T(ax, 1030, 300, "in", GR, 13, "center"); T(ax, 1130, 300, "longer out", GR, 13, "center")
# paraglider silhouette above the calm end
px, py = 2140, 330
arc = np.array([[px+95*np.cos(t), py-40*np.sin(t)] for t in np.linspace(.15, 2.99, 60)])
ax.add_patch(Polygon(np.r_[arc, arc[::-1]+[0, 10]], closed=True, fc=FILL, ec=WH, lw=1.3, zorder=5))
for k in range(0, 60, 10): L(ax, [arc[k]+[0, 10], [px, py+90]], GR, .6, .5, z=4)
ax.add_patch(Circle((px, py+96), 7, fc=FILL, ec=WH, lw=1.1, zorder=5))
T(ax, 2340, 820, "slow the breath, and the thinking comes back", GR, 12, "right", a=.75)
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", bloom=.35, glow=(.02, 1.1, .45))
print("ok")
