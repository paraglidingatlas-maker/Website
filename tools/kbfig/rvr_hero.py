"""Risk vs Reward hero: a valley in section. Launch on the left, three glide
lines fanning out over terrain shaded by consequence. The safe line (grey) keeps
landing options; the fast line (orange) crosses a gorge where a collapse has
nowhere to go. A small marker where they diverge. 2400x900, left 40% empty."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Circle
from PIL import Image, ImageFilter
plt.rcParams["mathtext.fontset"] = "cm"
W, H = 2400, 900; BG = "#141519"; OR = "#ff7517"; GR = "#b4b4b4"; DIM = "#737373"; WH = "#e9e7e7"; FILL = "#24252c"
fig = plt.figure(figsize=(W/100, H/100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off"); fig.patch.set_facecolor(BG)
def L(P, c=GR, lw=1, a=.8, ls="-", z=2): P = np.asarray(P, float); ax.plot(P[:, 0], P[:, 1], color=c, lw=lw, alpha=a, ls=ls, zorder=z, solid_capstyle="round")
def AR(p, q, c, lw=1.6, hl=12, hw=5, a=1, z=6): ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"-|>,head_length={hl},head_width={hw}", color=c, lw=lw, alpha=a, mutation_scale=1, zorder=z))
def T(x, y, s, c=GR, fs=14, ha="left", va="center", fw="normal", a=.9, z=7, fam="DejaVu Sans"): ax.text(x, y, s, color=c, fontsize=fs, ha=ha, va=va, fontweight=fw, alpha=a, zorder=z, family=fam)
# terrain profile: launch ridge left, valley floor with fields, gorge, far ridge right
xs = np.linspace(1000, 2400, 700)
def ground(x):
    y = 640 + 0*x
    y = y - 210*np.exp(-((x-1060)/110)**2)                     # launch ridge
    y = y + 120*np.clip(np.sin((x-1380)/95), 0, 1)**3*np.exp(-((x-1560)/160)**2)   # gorge (deeper)
    y = y - 60*np.exp(-((x-1860)/70)**2)                        # spur
    y = y - 320*np.exp(-((x-2360)/150)**2)                      # far ridge
    return y
g = ground(xs)
ax.add_patch(Polygon(np.r_[np.c_[xs, g], [[2400, 900], [1000, 900]]], closed=True, fc="#1b1c22", ec="none", zorder=1))
L(np.c_[xs, g], WH, 1.4, .85, z=3)
for k in range(1, 5):  # strata
    L(np.c_[xs, g + 26*k + 6*np.sin(xs/60)], GR, .5, .16 - .03*k, z=2)
# consequence wash under the surface of the gorge, fading with depth
m = (xs >= 1390) & (xs <= 1730)
for k in range(8):
    ax.add_patch(Polygon(np.r_[np.c_[xs[m], g[m]+8*k], np.c_[xs[m][::-1], g[m][::-1]+8*k+10]], closed=True, fc=OR, ec="none", alpha=.11*(1-k/8), zorder=2))
# gorge hatching
for x in range(1420, 1700, 18):
    y0 = ground(np.array([x]))[0]; L([[x, y0-2], [x-14, y0-38]], OR, .7, .35, z=3)
# landing fields (safe options)
for x0, x1 in [(1180, 1330), (1740, 1840), (1960, 2120)]:
    yy = ground(np.array([(x0+x1)/2]))[0]
    for x in range(x0, x1, 12): L([[x, yy-3], [x+6, yy-10]], GR, .6, .35, z=3)
    L([[x0, yy+2], [x1, yy+2]], WH, 1.2, .6, z=4)
# launch marker and pilot
lx, ly = 1060, ground(np.array([1060]))[0]
ax.add_patch(Circle((lx, ly-6), 5, fc=WH, ec=BG, lw=1.4, zorder=8))
# two lines from launch. Grey: climb in the house thermal first, cross high with a landing in reach.
# Orange: straight across, arriving low over the gorge with nothing below.
start = np.array([lx, ly-6])
t = np.linspace(0, 1, 300)
def bez(P0, P1, P2, P3):
    P0, P1, P2, P3 = map(np.array, (P0, P1, P2, P3)); tt = t[:, None]
    return (1-tt)**3*P0 + 3*(1-tt)**2*tt*P1 + 3*(1-tt)*tt**2*P2 + tt**3*P3
# climb: a rising helix drawn as a slanted spiral
th = np.linspace(0, 4*2*np.pi, 500); cz = 1140 + th*6; cy = ly - 30 - th*11
climb = np.c_[cz + 30*np.sin(th), cy + 9*np.cos(th)]
L(np.c_[[lx, climb[0][0]], [ly-6, climb[0][1]]], GR, 1.6, .8, z=5)
L(climb, GR, 1.5, .75, z=5)
top = climb[-1]
safe = bez(top, (1500, top[1]-10), (1900, ground(np.array([1900]))[0]-260), (2300, ground(np.array([2300]))[0]-14))
fast = bez(start, (1350, ly+40), (1650, ground(np.array([1650]))[0]-150), (1790, ground(np.array([1790]))[0]-70))
L(safe, GR, 2.0, .9, z=5); AR(safe[-6], safe[-1], GR, 2.0)
L(fast, OR, 2.2, .95, z=5); AR(fast[-6], fast[-1], OR, 2.2)
D = start + np.array([26, -18])
ax.add_patch(Circle(D, 7, fc=OR, ec=BG, lw=1.6, zorder=9)); ax.add_patch(Circle(D, 16, fc="none", ec=OR, lw=1, alpha=.5, zorder=9))
c1 = fast[150]
L([[c1[0], c1[1]+12], [c1[0]-10, ground(np.array([c1[0]-10]))[0]-8]], OR, 1.0, .5, ls=(0, (3, 3)), z=5)
T(top[0]+40, top[1]-6, "climb first, cross high", GR, 13, "left")
T(fast[95][0]+6, fast[95][1]+34, "straight across, low", OR, 13, "left")
T(D[0]+24, D[1]-4, "the decision", WH, 13, "left", fw="bold")
T(1560, ground(np.array([1560]))[0]+92, "no landing", OR, 11, "center", a=.85)
T(1255, ground(np.array([1250]))[0]+48, "landable", GR, 11, "center", a=.7)
T(1790, ground(np.array([1790]))[0]+48, "landable", GR, 11, "center", a=.7)
T(2040, ground(np.array([2040]))[0]+48, "landable", GR, 11, "center", a=.7)
T(2300, ground(np.array([2300]))[0]-40, "goal", WH, 11, "center", a=.8)
# altitude ticks on the right edge
for k, yv in enumerate(range(200, 700, 100)):
    L([[2372, yv], [2384, yv]], GR, .8, .35, z=3)
fig.savefig("/tmp/rvr_hero_raw.png", facecolor=BG); plt.close(fig)
img = np.asarray(Image.open("/tmp/rvr_hero_raw.png").convert("RGB").resize((W, H))).astype(np.float32)/255
yy, xx = np.mgrid[0:H, 0:W]; orange = np.array([1, .459, .09])
grid = (((xx % 60) == 0) | ((yy % 60) == 0)).astype(np.float32)*np.clip((xx-.36*W)/(.3*W), 0, 1)*np.clip(yy/(.18*H), 0, 1)*np.clip((H-yy)/(.18*H), 0, 1)*np.clip((W-xx)/(.06*W), 0, 1)*.045
img = img + grid[..., None]
img = img + np.exp(-(((xx-.02*W)/(.45*W))**2 + ((yy-1.1*H)/(.7*H))**2))[..., None]*orange*.11
o = np.clip((img[..., 0]-img[..., 2])*2, 0, 1); bl = np.asarray(Image.fromarray((o*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))).astype(np.float32)/255
img = np.clip(img + bl[..., None]*orange*.4, 0, 1)
Image.fromarray((img*255).astype(np.uint8)).save(sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", quality=87, optimize=True, progressive=True); print("ok")
