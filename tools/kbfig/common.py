import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Circle, Rectangle, Arc, FancyBboxPatch
from PIL import Image, ImageFilter
BG = "#141519"; OR = "#ff7517"; ORL = "#ff9a52"; GR = "#b4b4b4"; DIM = "#737373"; WH = "#e9e7e7"; FILL = "#24252c"
def canvas(W, H, bg=BG):
    fig = plt.figure(figsize=(W/100, H/100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off"); fig.patch.set_facecolor(bg); return fig, ax
def L(ax, P, c=GR, lw=1, a=.8, ls="-", z=2): P = np.asarray(P, float); ax.plot(P[:, 0], P[:, 1], color=c, lw=lw, alpha=a, ls=ls, zorder=z, solid_capstyle="round")
def AR(ax, p, q, c, lw=1.6, hl=12, hw=5, a=1, z=6): ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"-|>,head_length={hl},head_width={hw}", color=c, lw=lw, alpha=a, mutation_scale=1, zorder=z))
def T(ax, x, y, s, c=GR, fs=14, ha="left", va="center", fw="normal", a=.9, z=7): ax.text(x, y, s, color=c, fontsize=fs, ha=ha, va=va, fontweight=fw, alpha=a, zorder=z, family="DejaVu Sans")
def finish(fig, W, H, out, bloom=.4, glow=None):
    fig.savefig("/tmp/_raw.png", facecolor=fig.get_facecolor()); plt.close(fig)
    img = np.asarray(Image.open("/tmp/_raw.png").convert("RGB").resize((W, H))).astype(np.float32)/255
    orange = np.array([1, .459, .09])
    if glow:
        yy, xx = np.mgrid[0:H, 0:W]; gx, gy, s = glow
        img = img + np.exp(-(((xx-gx*W)/(s*W))**2 + ((yy-gy*H)/(s*H*1.4))**2))[..., None]*orange*.10
    o = np.clip((img[..., 0]-img[..., 2])*1.8, 0, 1); bl = np.asarray(Image.fromarray((o*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))).astype(np.float32)/255
    img = np.clip(img + bl[..., None]*orange*bloom, 0, 1)
    Image.fromarray((img*255).astype(np.uint8)).save(out, quality=88, optimize=True, progressive=True)
