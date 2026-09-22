"""Flight Mechanics hero: three-view technical drawing (side, front, top) with
reference frames, in the site palette. Wide format, left 42% left empty."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Arc, Ellipse, Circle
from PIL import Image, ImageFilter
plt.rcParams["mathtext.fontset"] = "cm"

W, H = 2400, 900
BG = "#141519"; OR = "#ff7517"; ORL = "#ff9a52"; GR = "#b4b4b4"; DIM = "#737373"; WH = "#e9e7e7"; FILL = "#24252c"
fig = plt.figure(figsize=(W/100, H/100), dpi=100); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off"); fig.patch.set_facecolor(BG)

def L(P, c=GR, lw=1.0, a=0.8, ls="-", z=2):
    P = np.asarray(P, float); ax.plot(P[:, 0], P[:, 1], color=c, lw=lw, alpha=a, ls=ls, zorder=z, solid_capstyle="round")
def AR(p, v, c, lab=None, off=(0, 0), lw=1.6, fs=21, a=1.0):
    p = np.asarray(p, float); q = p + np.asarray(v, float)
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=11,head_width=4.5", color=c, lw=lw, alpha=a, mutation_scale=1, zorder=5))
    if lab: ax.text(q[0]+off[0], q[1]+off[1], lab, color=c, fontsize=fs, ha="center", va="center", zorder=6, alpha=a)
def ANG(p, r, a0, a1, c, lab, loff=16, fs=18):   # degrees, screen angles measured CCW from +x with y down flipped
    ax.add_patch(Arc(p, 2*r, 2*r, angle=0, theta1=min(a0, a1), theta2=max(a0, a1), color=c, lw=0.9, alpha=0.8, zorder=4))
    m = np.radians((a0+a1)/2); ax.text(p[0]+(r+loff)*np.cos(m), p[1]+(r+loff)*np.sin(m), lab, color=c, fontsize=fs, ha="center", va="center", alpha=0.9)
def DOT(p, lab=None, off=(18, -14), fs=17):
    ax.add_patch(Circle(p, 5.5, fc=WH, ec=BG, lw=1.5, zorder=7))
    if lab: ax.text(p[0]+off[0], p[1]+off[1], lab, color=GR, fontsize=fs, fontweight="bold", ha="center", va="center", zorder=7, family="DejaVu Sans")
def rot(v, deg):  # screen-space rotation, positive = counter-clockwise on screen
    t = np.radians(deg); x, y = v; return np.array([x*np.cos(t) + y*np.sin(t), -x*np.sin(t) + y*np.cos(t)])

def thick(c): return 0.17*(2.969*np.sqrt(c) - 1.26*c - 3.516*c**2 + 2.843*c**3 - 1.015*c**4)
def camb(c): return 0.045*np.sin(np.pi*c)

# ================= SIDE VIEW =================
LE = np.array([1000., 150.]); CH = 350; AOA = 5.5
d = np.array([np.cos(np.radians(AOA)), np.sin(np.radians(AOA))]); n = np.array([d[1], -d[0]])
def af(c, s): return LE + d*c*CH + n*CH*(camb(c) + s*thick(c)/2)
cs = np.linspace(0, 1, 80)
up = [af(c, 1) for c in cs]; lo = [af(c, -1) for c in cs]
ax.add_patch(Polygon(up + lo[::-1], closed=True, fc=FILL, ec=GR, lw=1.3, alpha=0.95, zorder=3))
C = np.array([1178., 640.])
nodes = [(C + (af(0.10, -1) + af(0.30, -1))/2 - C) * 0.72 + C*0.0, None]
n1 = C + ((af(0.10, -1) + af(0.30, -1))/2 - C)*0.72; n2 = C + ((af(0.55, -1) + af(0.80, -1))/2 - C)*0.72
for a_, nd in [(0.10, n1), (0.30, n1), (0.55, n2), (0.80, n2)]: L([af(a_, -1), nd], lw=0.8, a=0.55)
L([n1, C], lw=0.9, a=0.6); L([n2, C], lw=0.9, a=0.6)
L([af(1.0, 0), C + np.array([22, 18])], c=DIM, lw=1.0, a=0.7, ls=(0, (3, 4)))
# pod harness
pod = C + np.array([[-120, 40], [-95, 22], [-20, 14], [0, 8], [40, 6], [95, 8], [118, -12], [178, -12], [178, 52], [120, 52], [95, 62], [-40, 70], [-110, 62]])
ax.add_patch(Polygon(pod, closed=True, fc=FILL, ec=GR, lw=1.2, alpha=0.95, zorder=3))
ax.add_patch(Circle(C + np.array([44, -3]), 12, fc=FILL, ec=GR, lw=1.1, zorder=3))
Hh = C + np.array([30, 38])
# frames
K = LE; P = af(0.33, 1); B = np.array([1158., 405.]); AM = np.array([1095., 300.])
AR(K, rot((0, -95), 0), GR, r"$z_k$", (18, 4)); AR(K, d*62, GR, r"$x_k$", (10, 20))
AR(P, -d*95, OR, r"$x_c$", (-6, -20)); AR(P, -n*105, OR, r"$z_c$", (20, 10))
AR(B, (-135, 0), WH, None, lw=1.3, a=0.75); AR(B, (0, 170), WH, None, lw=1.3, a=0.75)
AR(B, rot((-135, 0), 7), OR, r"$x_b$", (-20, 6)); AR(B, rot((0, 170), 7), OR, r"$z_b$", (22, 2))
gd = rot((-150, 0), 19); L([B, B + gd], c=DIM, lw=1.2, a=0.7, ls=(0, (4, 3)))
ANG(B, 112, 173, 180, OR, r"$\theta_b$", 22); ANG(B, 70, 161, 180, DIM, r"$\gamma$", 15)
AR(Hh, (-120, 0), OR, r"$x_h$", (-20, -2), lw=1.3); AR(Hh, (0, 95), OR, r"$z_h$", (20, 2), lw=1.3)
for p_, l_, o_ in [(K, "K", (-20, -2)), (P, "P", (14, -22)), (B, "B", (22, -16)), (AM, "AM", (26, -12)), (C, "C", (-20, -14)), (Hh, "H", (20, -14))]: DOT(p_, l_, o_)
# small inertial glyph
g0 = np.array([1290., 520.]); AR(g0, (-55, 0), WH, r"$x_I$", (-14, -16), lw=1.1, fs=17, a=0.7); AR(g0, (0, 60), WH, r"$z_I$", (18, 6), lw=1.1, fs=17, a=0.7)

# ================= FRONT VIEW =================
O = np.array([1660., 490.]); R1, R2 = 305, 277; TM = 64
def arcpt(t, r): t = np.radians(t); return O + r*np.array([np.sin(t), -np.cos(t)])
ts = np.linspace(-TM, TM, 200)
outer = [arcpt(t, R1) for t in ts]; inner = [arcpt(t, R2) for t in ts[::-1]]
ax.add_patch(Polygon(outer + inner, closed=True, fc=FILL, ec=GR, lw=1.3, alpha=0.95, zorder=3))
for t in np.linspace(-TM + 3, TM - 3, 45): L([arcpt(t, R2 + 2), arcpt(t, R1 - 2)], lw=0.5, a=0.28, z=4)
for sgn in (-1, 1):   # stabilo curl at the tips
    a0 = arcpt(sgn*TM, R1); a1 = arcpt(sgn*TM, R2)
    L([a0, a0 + np.array([sgn*6, 26]), a1 + np.array([sgn*2, 22]), a1], lw=1.2, a=0.9, z=4)
rs = {-1: np.array([1640., 712.]), 1: np.array([1680., 712.])}
att = np.linspace(-TM + 4, TM - 4, 27)
for g in range(0, 27, 3):
    grp = att[g:g+3]; sd = 1 if grp.mean() > 0 else -1
    pts = [arcpt(t, R2) for t in grp]; mid = rs[sd] + (np.mean(pts, 0) - rs[sd])*0.66
    for p_ in pts: L([p_, mid], lw=0.7, a=0.5)
    L([mid, rs[sd]], lw=0.85, a=0.6)
Cf = np.array([1660., 718.]); Hf = np.array([1660., 755.])
ax.add_patch(Circle(Hf, 32, fc=FILL, ec=GR, lw=1.2, zorder=3)); ax.add_patch(Circle(Cf + np.array([0, -12]), 11, fc=FILL, ec=GR, lw=1.1, zorder=3))
for sd in (-1, 1): L([rs[sd], Cf + np.array([sd*12, 2])], lw=1.0, a=0.8)
Bf = np.array([1660., 505.]); PHI = 9
AR(Bf, (-130, 0), WH, None, lw=1.3, a=0.75); AR(Bf, (0, 150), WH, None, lw=1.3, a=0.75)
AR(Bf, rot((-130, 0), -PHI), OR, r"$y_b$", (-22, -8)); AR(Bf, rot((0, 150), -PHI), OR, r"$z_b$", (20, 4))
ANG(Bf, 92, 180, 180 + PHI, OR, r"$\phi_b$", 26)
top = arcpt(0, R1 + 4); AR(top, (0, -120), GR, r"$z_k$", (20, 6)); AR(top, (-120, 0), GR, r"$y_k$", (0, -18))
AR(arcpt(0, R2), (0, 120), OR, r"$z_c$", (20, 4), lw=1.3)
AR(Hf, (-105, 18), OR, r"$y_h$", (-16, -14), lw=1.3); AR(Hf, (14, 105), OR, r"$z_h$", (22, 2), lw=1.3)
for p_, l_, o_ in [(Bf, "B", (22, -16)), (Cf, "C", (24, -10)), (Hf, "H", (22, -18))]: DOT(p_, l_, o_)

# ================= TOP VIEW =================
Q = np.array([2190., 450.]); HS = 360; CMX = 160
ys = np.linspace(-1, 1, 400)
cy = CMX*np.clip(1 - ys**2, 0, 1)**0.42; le = Q[0] - 0.42*cy - 26*ys**2
tev = le + cy; yy = Q[1] + HS*ys
ax.add_patch(Polygon(np.r_[np.c_[le, yy], np.c_[tev, yy][::-1]], closed=True, fc=FILL, ec=GR, lw=1.3, alpha=0.95, zorder=3))
for k in np.linspace(-0.98, 0.98, 46):
    j = np.argmin(abs(ys - k)); L([[le[j] + 1, yy[j]], [tev[j] - 1, yy[j]]], lw=0.45, a=0.22, z=4)
for k in np.linspace(-0.85, 0.85, 12):
    j = np.argmin(abs(ys - k))
    for f_ in (0.2, 0.5, 0.78):
        x0 = le[j] + f_*cy[j]; y0 = yy[j]; s_ = 9
        L([[x0, y0], [x0 - s_, y0 - s_]], lw=0.7, a=0.5, z=4); L([[x0, y0], [x0 + s_, y0 - s_]], lw=0.7, a=0.5, z=4); L([[x0, y0], [x0, y0 + s_*1.3]], lw=0.7, a=0.5, z=4)
PSI = 12
ax.add_patch(Ellipse(Q, 150, 38, angle=PSI*1.6, fc=FILL, ec=GR, lw=1.2, alpha=0.95, zorder=5))
AR(Q, (-150, 0), WH, r"$x_I$", (-20, -2), lw=1.3, a=0.75); AR(Q, (0, 130), WH, r"$y_I$", (22, 8), lw=1.3, a=0.75)
AR(Q, rot((-150, 0), -PSI*1.6), OR, r"$x_b$", (-18, -14)); AR(Q, rot((0, 130), -PSI*1.6), OR, r"$y_b$", (-24, 6))
AR(Q, rot((-130, 0), -8), DIM, None, lw=1.2)
ANG(Q, 132, 180, 180 + PSI*1.6, OR, r"$\psi_b$", 20); ANG(Q, 78, 180, 188, DIM, r"$\beta$", 18)
DOT(Q)

# view labels
for x_, t_ in [(1000, "SIDE"), (1356, "FRONT"), (2010, "TOP")]:
    ax.text(x_, 862, t_, color=DIM, fontsize=12, family="DejaVu Sans", fontweight="bold", alpha=0.8)
fig.savefig("/tmp/kb_hero_raw.png", facecolor=BG); plt.close(fig)

# ================= atmosphere =================
img = Image.open("/tmp/kb_hero_raw.png").convert("RGB").resize((W, H)); a = np.asarray(img).astype(np.float32)/255
o = np.clip((a[..., 0] - a[..., 2])*2.0, 0, 1)
bl = np.asarray(Image.fromarray((o*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))).astype(np.float32)/255
yy_, xx_ = np.mgrid[0:H, 0:W]
grid = (((xx_ % 60) == 0) | ((yy_ % 60) == 0)).astype(np.float32)
gm = np.clip((xx_ - 0.36*W)/(0.3*W), 0, 1) * np.clip(yy_/(0.18*H), 0, 1) * np.clip((H - yy_)/(0.18*H), 0, 1) * np.clip((W - xx_)/(0.06*W), 0, 1) * 0.045
a = a + grid[..., None]*gm[..., None]
orange = np.array([1.0, 0.459, 0.09])
a = a + np.exp(-(((xx_ - 0.02*W)/(0.45*W))**2 + ((yy_ - 1.1*H)/(0.7*H))**2))[..., None]*orange*0.11
a = a + bl[..., None]*orange*0.45
a = np.clip(a, 0, 1)
Image.fromarray((a*255).astype(np.uint8)).save(sys.argv[1] if len(sys.argv) > 1 else "assets/images/kb-flight-mechanics.jpg", quality=87, optimize=True, progressive=True)
print("ok")
