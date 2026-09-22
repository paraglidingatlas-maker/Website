"""Draws a knowledge base hero as a technical wing diagram (Flight Mechanics).
Usage: python3 tools/make_kb_hero.py assets/images/kb-flight-mechanics.jpg
Pure matplotlib + PIL, no AI image model: geometry, lift vectors and lines are
plotted, so the drawing is accurate and repeatable. Layout keeps the left 40%
empty for the headline."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon
from PIL import Image, ImageFilter
import sys

W, H = 2400, 1350
BG = "#141519"; OR = "#ff7517"; GR = "#b4b4b4"

# ---------- geometry (metres; x forward, y left, z up; pilot near origin) ----------
R, TH = 6.0, np.radians(64)          # arc radius, half arc angle
ZC = 8.2 - R                          # arc centre height
C0 = 2.7                              # root chord
NR = 49                               # ribs
th = np.linspace(-TH, TH, NR)
s = th / TH
chord = C0 * np.sqrt(np.clip(1 - 0.82 * s**2, 0.05, 1))
xle = 0.35 * C0 * (s**2)              # slight sweep of the leading edge

def airfoil(c):                       # thickness/chord, 0..1
    return 0.16 * (2.969*np.sqrt(c) - 1.26*c - 3.516*c**2 + 2.843*c**3 - 1.015*c**4)
def camber(c): return 0.035 * np.sin(np.pi * c)

def pt(i, c, side):                   # side +1 upper, -1 lower, 0 camber line
    t = th[i]; n = np.array([0, np.sin(t), np.cos(t)])
    base = np.array([xle[i] + chord[i]*(0.5 - c) * 1.0, R*np.sin(t), ZC + R*np.cos(t)])
    base[0] = xle[i] + chord[i]*(1 - c) - chord[i]   # leading edge at x = xle, trailing edge behind
    base[0] = -(xle[i] + chord[i]*c) + C0*0.5
    off = chord[i]*(camber(c) + side*airfoil(c)/2)
    return base + n*off

# ---------- camera ----------
cam = np.array([-15.5, -8.5, 11.5]); tgt = np.array([0.4, 0.0, 4.6]); up = np.array([0, 0, 1.0])
f = tgt - cam; f /= np.linalg.norm(f); r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
FOV = 1.25
def proj(P):
    P = np.atleast_2d(P); d = P - cam
    z = d @ f; return np.c_[(d @ r) / z * FOV, (d @ u) / z * FOV]

# collect primitives: (kind, points3d, style)
prims = []
def line(P, **k): prims.append(("l", np.array(P), k))
def arrow(a, b, **k): prims.append(("a", np.array([a, b]), k))

cs = np.linspace(0, 1, 40)
wire = dict(color=GR, lw=0.55, alpha=0.30)
for i in range(NR):                                   # ribs (airfoil sections)
    up_ = [pt(i, c, 1) for c in cs]; lo = [pt(i, c, -1) for c in cs[::-1]]
    line(up_ + lo + [up_[0]], **(dict(color=GR, lw=0.75, alpha=0.55) if i % 6 == 0 else wire))
for c, a in [(0.0, 0.9), (0.08, 0.35), (0.25, 0.22), (0.5, 0.22), (0.75, 0.22), (1.0, 0.8)]:  # spanwise
    line([pt(i, c, 1) for i in range(NR)], color=GR, lw=0.9 if a > 0.5 else 0.55, alpha=a)
line([pt(i, 0.0, -1) for i in range(NR)], color=GR, lw=0.6, alpha=0.35)
line([pt(i, 1.0, -1) for i in range(NR)], color=GR, lw=0.6, alpha=0.35)

# suspension lines: attachment -> cascade -> riser
ris = {+1: np.array([0.25, 0.28, 1.35]), -1: np.array([0.25, -0.28, 1.35])}
for i in range(1, NR - 1, 3):
    side = 1 if th[i] > 0 else -1
    for c in (0.12, 0.42, 0.72):
        a = pt(i, c, -1); k = a + (ris[side] - a) * 0.28
        line([a, k, ris[side]], color=GR, lw=0.45, alpha=0.22)
# brake lines
for i in range(2, NR - 2, 4):
    side = 1 if th[i] > 0 else -1
    a = pt(i, 1.0, 0); line([a, ris[side] + np.array([-0.35, 0, -0.1])], color=GR, lw=0.4, alpha=0.14)

# lift vectors from quarter chord, along local normal, elliptical distribution
for i in range(2, NR - 2, 3):
    t = th[i]; n = np.array([0, np.sin(t), np.cos(t)])
    L = 2.7 * max(0.0, 1 - (t/TH)**2)**0.8 + 0.12
    a = pt(i, 0.25, 1); arrow(a, a + n*L, color=OR, lw=1.3, alpha=0.95)

# centre-section chord line (dashed orange) and resultant arrow
ic = NR // 2
line([pt(ic, 0, 0) + np.array([0.9, 0, 0.05]), pt(ic, 1, 0) + np.array([-1.0, 0, -0.05])], color=OR, lw=0.9, alpha=0.7, ls=(0, (5, 4)))

# streamlines
rng = np.random.default_rng(7)
for k in range(46):
    y = rng.uniform(-8, 8); z0 = rng.uniform(1.0, 11.5)
    xs = np.linspace(-9, 7, 140)
    near = np.exp(-(((y/7.0)**2) + ((z0 - (ZC + R*np.cos(np.clip(y/R, -1, 1))))/1.4)**2))
    zs = z0 + 0.55*near*np.exp(-((xs - 0.5)/1.6)**2) - 0.25*near*np.tanh(xs)
    line(np.c_[xs, np.full_like(xs, y), zs], color=GR, lw=0.4, alpha=0.08 + 0.10*near)

# floor grid
for g in np.arange(-14, 15, 2.0):
    line([[g, -14, -3.5], [g, 14, -3.5]], color=GR, lw=0.4, alpha=0.05)
    line([[-14, g, -3.5], [14, g, -3.5]], color=GR, lw=0.4, alpha=0.05)

# ---------- framing: fit wing + pilot into the right-hand box ----------
key = np.vstack([p for kind, p, k in prims if k.get("color") == OR or k.get("alpha", 0) >= 0.3] + [[[0, 0, 0.0]]])
kp = proj(key); lo_, hi_ = kp.min(0), kp.max(0)
box = np.array([0.40*W, 0.07*H, 0.965*W, 0.95*H])     # x0, y0, x1, y1 in pixels (y down)
sc = min((box[2]-box[0])/(hi_[0]-lo_[0]), (box[3]-box[1])/(hi_[1]-lo_[1]))
def px(P):
    q = proj(P); x = box[2] - (hi_[0] - q[:, 0])*sc; y = box[1] + (hi_[1] - q[:, 1])*sc
    return np.c_[x, y]

fig = plt.figure(figsize=(W/100, H/100), dpi=100); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off"); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
for kind, P, k in prims:
    q = px(P)
    if kind == "l":
        ax.plot(q[:, 0], q[:, 1], color=k["color"], lw=k["lw"], alpha=k["alpha"], ls=k.get("ls", "-"), solid_capstyle="round")
    else:
        ax.add_patch(FancyArrowPatch(q[0], q[1], arrowstyle="-|>,head_length=9,head_width=4", color=k["color"], lw=k["lw"], alpha=k["alpha"], mutation_scale=1))

# pilot: seated in a pod harness, drawn in screen space under the risers
rl, rr = px(ris[-1][None])[0], px(ris[1][None])[0]
m = (rl + rr) / 2; k = 1.0
sh = m + np.array([4, 34])*k
for r0 in (rl, rr): ax.plot([r0[0], sh[0]], [r0[1], sh[1]], color=GR, lw=0.9, alpha=0.8)
ax.add_patch(plt.Circle(sh + np.array([-4, -12]), 7.5, fc="#23242b", ec=GR, lw=0.9, alpha=0.95))
pod = np.array([[-14, -2], [10, 0], [44, 10], [70, 26], [62, 36], [26, 34], [-8, 28], [-18, 14]])*k + sh
ax.add_patch(Polygon(pod, closed=True, fc="#23242b", ec=GR, lw=0.9, alpha=0.95))
fig.savefig("raw.png", facecolor=BG); plt.close(fig)

# ---------- atmosphere: warm glow bottom-left, cool vignette ----------
img = Image.open("raw.png").convert("RGB").resize((W, H))
a = np.asarray(img).astype(np.float32) / 255
o = np.clip((a[...,0] - a[...,2]) * 2.2, 0, 1)
bl = np.asarray(Image.fromarray((o*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(np.float32)/255
yy, xx = np.mgrid[0:H, 0:W]
glow = np.exp(-(((xx - 0.05*W)/(0.55*W))**2 + ((yy - 1.05*H)/(0.55*H))**2))
orange = np.array([1.0, 0.459, 0.09])
a = a + glow[..., None] * orange * 0.12
glow2 = np.exp(-(((xx - 0.72*W)/(0.35*W))**2 + ((yy - 0.25*H)/(0.35*H))**2))
a = a + glow2[..., None] * orange * 0.035
vig = 1 - 0.35*np.clip(((xx - 0.6*W)/(0.9*W))**2 + ((yy - 0.45*H)/(0.8*H))**2, 0, 1)
a = np.clip(a * vig[..., None], 0, 1)
a = np.clip(a + bl[..., None]*orange*0.5, 0, 1)
out = Image.fromarray((a*255).astype(np.uint8))
out.save(sys.argv[1] if len(sys.argv) > 1 else "hero.jpg", quality=86, optimize=True, progressive=True)
print("ok")
