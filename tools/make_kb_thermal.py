# Knowledge base figure generator (Flight Mechanics). Usage: python3 tools/make_kb_thermal.py <out.jpg> [background hex]
"""Knowledge base figure: reading a thermal (Brett Janaway). Left, from above:
the core sits upwind; turning into wind finds it, turning downwind falls out
the back. Right, from the side: the column leans downwind, strongest air at the
upwind front. 2400x760, two panels, no text (captions are HTML)."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Ellipse
from PIL import Image, ImageFilter

W, H = 2400, 760
BG = sys.argv[2] if len(sys.argv) > 2 else "#202127"
OR = "#ff7517"; GR = "#b4b4b4"; DIM = "#737373"; FILL = "#2a2b33"
fig = plt.figure(figsize=(W/100, H/100), dpi=100); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off"); fig.patch.set_facecolor(BG)
def arrow(p, q, c, lw=2.0, hl=14, hw=6, a=1.0, z=6, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"-|>,head_length={hl},head_width={hw}", color=c, lw=lw, alpha=a, mutation_scale=1, zorder=z, linestyle=ls))
def glider(p, ang, c=GR, s=15):
    t = np.radians(ang); d = np.array([np.cos(t), np.sin(t)]); n = np.array([-d[1], d[0]])
    tri = [p + d*s, p - d*s*0.6 + n*s*0.75, p - d*s*0.3, p - d*s*0.6 - n*s*0.75]
    ax.add_patch(Polygon(tri, closed=True, fc=c, ec="none", zorder=8))

# ---------- left: top view ----------
C = np.array([640., 390.]); CORE = C + np.array([-120., 0.])      # wind blows left -> right, core upwind (left)
yy, xx = np.mgrid[0:H, 0:W]
field = np.exp(-(((xx - C[0])/300)**2 + ((yy - C[1])/250)**2))*0.55 + np.exp(-(((xx - CORE[0])/115)**2 + ((yy - CORE[1])/105)**2))*0.8
field[:, 1180:] = 0
for r, a in [(1.0, 0.18), (0.78, 0.22), (0.56, 0.28)]:
    ax.add_patch(Ellipse(C + np.array([-120*(1 - r), 0]), 600*r, 500*r, fc="none", ec=GR, lw=0.8, alpha=a, ls=(0, (4, 4)), zorder=3))
# approach path from below, hits lift at the back-left edge area
E = C + np.array([30., 120.])
ax.plot([E[0] + 10, E[0]], [E[1] + 230, E[1]], color=GR, lw=1.4, alpha=0.6, ls=(0, (6, 5)), zorder=5)
glider(E + np.array([4, 140]), -90, GR)
# into wind (left turn): circles whose centre slides from beside the entry point onto the core
t = np.linspace(0, 1, 700); r0 = 95
th_ = t*2*np.pi*2.3; blend = np.clip(t*2.2, 0, 1)**0.8
cen = (E + np.array([-r0, 0]))*(1 - blend)[:, None] + CORE*blend[:, None]; rad = r0*(1 - blend) + 62*blend
path = np.c_[cen[:, 0] + rad*np.cos(th_), cen[:, 1] - rad*np.sin(th_)]
ax.plot(path[:, 0], path[:, 1], color=OR, lw=2.2, alpha=0.95, zorder=6, solid_capstyle="round")
arrow(path[-8], path[-1], OR, lw=2.2, hl=14, hw=6)
# downwind (right turn): circles that drift out of the back of the thermal
t2 = np.linspace(0, 1, 500); th2 = t2*2*np.pi*1.7; r2 = 70
cen2 = E + np.array([r2, 0]) + np.c_[t2*420, -t2*10]
path2 = np.c_[cen2[:, 0] - r2*np.cos(th2), cen2[:, 1] - r2*np.sin(th2)]
ax.plot(path2[:, 0], path2[:, 1], color=GR, lw=1.6, alpha=0.55, ls=(0, (5, 4)), zorder=5)
arrow(path2[-8], path2[-1], GR, lw=1.6, hl=12, hw=5, a=0.6)
ax.add_patch(Ellipse(CORE, 16, 16, fc=OR, ec="none", zorder=7))
# wind arrows
for y in (95, 140):
    arrow(np.array([200., y]), np.array([330., y]), GR, lw=1.4, hl=12, hw=5, a=0.55)

# ---------- right: side view ----------
G = 690.; S = np.array([1560., G])                                 # ground source
ax.plot([1260, 2330], [G, G], color=GR, lw=1.0, alpha=0.4, zorder=3)
for k in range(9):
    ax.plot([1300 + k*120, 1285 + k*120], [G, G + 14], color=GR, lw=0.8, alpha=0.25)
h = np.linspace(0, 1, 60)
lean = 330*h**1.1                                                  # drifts downwind with height
front = np.c_[S[0] - 60 - 40*h + lean, G - 560*h]
back = np.c_[S[0] + 60 + 170*h + lean, G - 560*h*0.92]
ax.add_patch(Polygon(np.r_[front, back[::-1]], closed=True, fc=OR, ec="none", alpha=0.07, zorder=2))
ax.plot(front[:, 0], front[:, 1], color=GR, lw=1.0, alpha=0.45, zorder=3); ax.plot(back[:, 0], back[:, 1], color=GR, lw=1.0, alpha=0.3, ls=(0, (4, 4)), zorder=3)
core = np.c_[S[0] - 20 + lean*1.0 - 10*h, G - 560*h]
ax.plot(core[:, 0], core[:, 1], color=OR, lw=3.0, alpha=0.9, zorder=4, solid_capstyle="round")
for f in (0.2, 0.45, 0.85):
    j = int(f*59); arrow(core[j] + np.array([0, 20]), core[j] + np.array([10, -40]), OR, lw=1.8, hl=12, hw=5)
# cloud
cb = core[-1] + np.array([60, -30])
for dx, dy, w, hh in [(-80, 10, 220, 90), (40, -10, 260, 120), (160, 12, 200, 90)]:
    ax.add_patch(Ellipse(cb + np.array([dx, dy]), w, hh, fc=FILL, ec=GR, lw=0.9, alpha=0.9, zorder=5))
# gliders: one climbing in the core, one fallen out of the back
glider(core[40] + np.array([26, 4]), -30, OR, 16)
glider(back[22] + np.array([60, 70]), 20, GR, 14)
arrow(back[22] + np.array([40, 40]), back[22] + np.array([100, 110]), GR, lw=1.4, hl=11, hw=5, a=0.55, ls=(0, (4, 3)))
for y in (110, 155):
    arrow(np.array([1300., y]), np.array([1430., y]), GR, lw=1.4, hl=12, hw=5, a=0.55)
ax.plot([1200, 1200], [60, H - 60], color=GR, lw=0.6, alpha=0.12)
fig.savefig("/tmp/thermal_raw.png", facecolor=BG); plt.close(fig)

img = np.asarray(Image.open("/tmp/thermal_raw.png").convert("RGB").resize((W, H))).astype(np.float32)/255
orange = np.array([1.0, .459, .09])
img = img + field[..., None]*orange*0.12
o = np.clip((img[..., 0] - img[..., 2])*1.6, 0, 1)
bl = np.asarray(Image.fromarray((o*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))).astype(np.float32)/255
img = np.clip(img + bl[..., None]*orange*0.3, 0, 1)
Image.fromarray((img*255).astype(np.uint8)).save(sys.argv[1] if len(sys.argv) > 1 else "thermal.jpg", quality=88, optimize=True, progressive=True)
print("ok")
