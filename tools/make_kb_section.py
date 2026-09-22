# Draws the knowledge base mid-page band: wing cutaway at a rib plus a Joukowski potential-flow field.
# Usage: python3 tools/make_kb_section.py assets/images/kb-flight-mechanics-section.jpg
"""Mid-page band: cutaway of a paraglider wing at a rib, with cross-ports, and a
potential-flow (Joukowski) field around the section: streamlines coloured by
speed, surface-pressure glow. Wide 2400x1000; drawing in the left ~58%."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image, ImageFilter

W, H = 2400, 1000
BG = "#141519"; OR = "#ff7517"; GR = "#b4b4b4"; FILL = "#1e1f25"
cm = LinearSegmentedColormap.from_list("atlas", ["#1b1c22", "#3b3b44", "#8a8a92", "#ffb27a", "#ff7517"])

# ---- Joukowski section + exact potential flow with Kutta condition ----
MU = complex(-0.19, 0.12); A = abs(1 - MU); ALPHA = np.radians(7); U = 1.0
BETA = -np.angle(1 - MU); GAM = 4*np.pi*U*A*np.sin(ALPHA + BETA)
th = np.linspace(0, 2*np.pi, 900)
zeta = MU + A*np.exp(1j*th); zf = zeta + 1/zeta                     # section outline
def vel(z):
    s = np.sqrt(z*z - 4 + 0j); z1, z2 = (z + s)/2, (z - s)/2
    zt = np.where(abs(z1 - MU) >= abs(z2 - MU), z1, z2)
    d = zt - MU
    dw = U*(np.exp(-1j*ALPHA) - A*A*np.exp(1j*ALPHA)/d**2) + 1j*GAM/(2*np.pi*d)
    q = dw/(1 - 1/zt**2); inside = abs(d) < A*1.0005
    return np.conj(q), inside                                       # u + iv

# section frame -> pixels (flight to the left: flip x so leading edge is on the left)
xmin, xmax = zf.real.min(), zf.real.max(); CH = xmax - xmin
SC = 980/CH; X0, Y0 = 230, 430
def P(x, y): return np.c_[X0 + (xmax - np.asarray(x) - 0)*SC*0 + (np.asarray(x) - xmin)*SC, Y0 - np.asarray(y)*SC]
# x as-is puts LE (Joukowski LE is at x=-2) on the left; flow comes from the left
sec = P(zf.real, zf.imag)

fig = plt.figure(figsize=(W/100, H/100), dpi=100); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off"); fig.patch.set_facecolor(BG)

# ---- the rest of the half-wing, receding down-left behind the cut ----
def sec_at(k):
    s = 1 - 0.86*k**1.15; dx = -470*k**1.25; dy = 440*k**1.9
    c = sec.mean(0); return (sec - c)*s + c + np.array([dx, dy])
ks = np.linspace(0, 1, 40)
secs = [sec_at(k) for k in ks]
le_i = np.argmin(sec[:, 0]); te_i = np.argmax(sec[:, 0]); top_i = np.argmin(sec[:, 1])
LEc = np.array([q[le_i] for q in secs]); TEc = np.array([q[te_i] for q in secs]); TPc = np.array([q[top_i] for q in secs])
lo_i = np.argmax(sec[:, 1])
LOc = np.array([q[lo_i] for q in secs])
skin = np.r_[TPc, LEc[::-1]]
ax.add_patch(Polygon(np.r_[TEc, TPc[::-1]], closed=True, fc="#23242b", ec="none", alpha=0.85, zorder=1))
ax.add_patch(Polygon(np.r_[TPc, LEc[::-1]], closed=True, fc="#2b2c34", ec="none", alpha=0.9, zorder=1))
ax.add_patch(Polygon(np.r_[LEc, LOc[::-1]], closed=True, fc="#1d1e24", ec="none", alpha=0.9, zorder=1))
for k, q in zip(ks[1::2], secs[1::2]):
    a = 0.22*(1 - k) + 0.06
    ax.plot(q[:, 0], q[:, 1], color=GR, lw=0.6, alpha=a, zorder=1)
for c_, a_ in [(LEc, 0.8), (TEc, 0.55), (TPc, 0.35), (LOc, 0.3)]:
    ax.plot(c_[:, 0], c_[:, 1], color=GR, lw=1.0, alpha=a_, zorder=1)

# ---- flow field: speed heat-map near the section ----
gx, gy = np.meshgrid(np.linspace(-3.2, 3.2, 700), np.linspace(-1.6, 1.8, 380))
V, ins = vel(gx + 1j*gy); spd = np.abs(V); spd[ins] = np.nan
dist = np.hypot(gx/2.6, gy/1.3); fade = np.clip(1.25 - dist, 0, 1)**1.2
ext = [X0 + (-3.2 - xmin)*SC, X0 + (3.2 - xmin)*SC, Y0 + 1.6*SC, Y0 - 1.8*SC]
rgba = cm(np.clip((spd - 0.3)/1.5, 0, 1)); rgba[..., 3] = np.nan_to_num(fade*0.55)
ax.imshow(rgba, extent=[ext[0], ext[1], ext[2], ext[3]], origin="lower", zorder=2, interpolation="bilinear")

# ---- streamlines (RK4 in the section plane), coloured by speed ----
def trace(z0, n=900, h=0.012):
    pts, sp = [z0], []
    z = z0
    for _ in range(n):
        def f(zz):
            v, i = vel(np.array([zz])); return v[0], i[0]
        k1, i1 = f(z)
        if i1: break
        k2, _ = f(z + h/2*k1/abs(k1)); k3, _ = f(z + h/2*k2/abs(k2)); k4, _ = f(z + h*k3/abs(k3))
        d = (k1/abs(k1) + 2*k2/abs(k2) + 2*k3/abs(k3) + k4/abs(k4))/6
        sp.append(abs(k1)); z = z + h*d; pts.append(z)
        if z.real > 3.25 or abs(z.imag) > 2.2: break
    sp.append(sp[-1] if sp else 1); return np.array(pts), np.array(sp)
seeds = np.r_[np.linspace(-0.9, -0.2, 6), np.linspace(-0.12, 0.35, 9), np.linspace(0.45, 1.45, 10)]
for y0 in seeds:
    z0 = complex(-3.2, y0 - 0.25)
    pts, sp = trace(z0)
    xy = P(pts.real, pts.imag)
    segs = np.stack([xy[:-1], xy[1:]], 1)
    near = np.clip(1.3 - np.hypot(pts.real[:-1]/2.7, pts.imag[:-1]/1.2), 0, 1)
    endf = np.clip((3.2 - pts.real[:-1])/0.9, 0, 1)*np.clip((pts.real[:-1] + 3.2)/0.6, 0, 1)
    cols = cm(np.clip((sp[:-1] - 0.3)/1.5, 0, 1)); cols[:, 3] = (0.12 + 0.78*near)*endf
    ax.add_collection(LineCollection(segs, colors=cols, linewidths=1.1 + 0.6*near, zorder=3, capstyle="round"))

# ---- the cut rib, with cross-ports ----
ax.add_patch(Polygon(sec, closed=True, fc=FILL, ec="#d8d6d6", lw=1.5, zorder=5, joinstyle="round"))
up = sec[:len(sec)//2]; lo = sec[len(sec)//2:]
def surf(x):
    ys = sec[np.abs(sec[:, 0] - x) < 3][:, 1]
    return ys.min(), ys.max()
x_le, x_te = sec[:, 0].min(), sec[:, 0].max()
for f in np.linspace(0.1, 0.78, 12):
    x = x_le + f*(x_te - x_le); t, b = surf(x); hgt = (b - t)*0.62; w = 26 - 12*f
    if hgt < 14: continue
    cy = (t + b)/2 + (b - t)*0.02
    ax.add_patch(FancyBboxPatch((x - w/2, cy - hgt/2), w, hgt, boxstyle="round,pad=0,rounding_size=%.1f" % (w/2),
                                fc="#101115", ec=GR, lw=0.8, alpha=0.95, zorder=6))
# small LE opening and chord line
ax.plot([x_le + 4, x_te], [sec[le_i, 1], sec[te_i, 1]], color=OR, lw=0.9, alpha=0.55, ls=(0, (5, 4)), zorder=6)
fig.savefig("/tmp/mid_raw.png", facecolor=BG); plt.close(fig)

img = np.asarray(Image.open("/tmp/mid_raw.png").convert("RGB").resize((W, H))).astype(np.float32)/255
o = np.clip((img[..., 0] - img[..., 2])*1.6, 0, 1)
bl = np.asarray(Image.fromarray((o*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(np.float32)/255
yy, xx = np.mgrid[0:H, 0:W]; orange = np.array([1.0, 0.459, 0.09])
img = img + bl[..., None]*orange*0.35
img = img + np.exp(-(((xx - 0.3*W)/(0.35*W))**2 + ((yy - 0.35*H)/(0.4*H))**2))[..., None]*orange*0.04
img = np.clip(img, 0, 1)
Image.fromarray((img*255).astype(np.uint8)).save(sys.argv[1] if len(sys.argv) > 1 else "mid.jpg", quality=86, optimize=True, progressive=True)
print("ok")
