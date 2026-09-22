# Knowledge base figure generator (Flight Mechanics). Usage: python3 tools/make_kb_brakes.py <out.jpg> [background hex]
"""Knowledge base figure: the small-brake problem. One profile, three brake
positions. Orange arrow = where the lift acts; curved arrow = what the profile
does in a gust; grey arrow = drag. 2400x640, three equal panels, no text (the
captions are HTML so they use the site fonts)."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Arc
from PIL import Image, ImageFilter

W, H = 2400, 640
BG = sys.argv[2] if len(sys.argv) > 2 else "#141519"
OR = "#ff7517"; GR = "#b4b4b4"; DIM = "#737373"; FILL = "#24252c"
fig = plt.figure(figsize=(W/100, H/100), dpi=100); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off"); fig.patch.set_facecolor(BG)

def thick(c): return 0.17*(2.969*np.sqrt(c) - 1.26*c - 3.516*c**2 + 2.843*c**3 - 1.015*c**4)
def camb(c): return 0.05*np.sin(np.pi*c)
CH = 500; cs = np.linspace(0, 1, 160)

def profile(cx, cy, defl):
    x = cx - CH/2 + cs*CH
    tail = np.clip((cs - 0.68)/0.32, 0, 1)**2*defl
    yu = cy - CH*(camb(cs) + thick(cs)/2) + tail
    yl = cy - CH*(camb(cs) - thick(cs)/2) + tail
    return x, yu, yl

def arrow(p, q, c, lw=2.0, hl=14, hw=6, a=1.0, z=6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"-|>,head_length={hl},head_width={hw}", color=c, lw=lw, alpha=a, mutation_scale=1, zorder=z))

def curl(cx, cy, r, a0, a1, c, a=1.0):
    ax.add_patch(Arc((cx, cy), 2*r, 2*r, theta1=min(a0, a1), theta2=max(a0, a1), color=c, lw=1.8, alpha=a, zorder=6))
    end = np.radians(a1); tip = np.array([cx + r*np.cos(end), cy + r*np.sin(end)])
    d = np.array([-np.sin(end), np.cos(end)])*(1 if a1 > a0 else -1)
    arrow(tip - d*2, tip + d*12, c, lw=1.8, hl=12, hw=5, a=a)

panels = [  # defl px, centre of lift (chord fraction), lift len, pitch sense, drag len
    dict(defl=0,  cp=0.22, L=150, pitch=+1, drag=44),
    dict(defl=26, cp=0.36, L=150, pitch=-1, drag=52),
    dict(defl=64, cp=0.40, L=205, pitch=0,  drag=130),
]
for i, pnl in enumerate(panels):
    cx, cy = 360 + i*800, 330
    x, yu, yl = profile(cx, cy, pnl["defl"])
    # airflow: smooth streamlines that bow over the top and ease under the bottom
    xs = np.linspace(cx - 390, cx + 390, 300)
    for k, off in enumerate((62, 112, 170)):
        bump = 34*np.exp(-((xs - (cx - CH*0.18))/(CH*0.42))**2)*(1 - 0.35*k)
        ys = cy - off - bump + np.clip((xs - (cx + CH/2 - 40))/400, 0, 1)*pnl["defl"]*0.5
        ax.plot(xs, ys, color=GR, lw=0.8, alpha=0.2 - 0.05*k, zorder=2)
    for k, off in enumerate((40, 92)):
        ys = cy + off + 6*np.exp(-((xs - cx)/(CH*0.5))**2) + np.clip((xs - (cx + CH/2 - 80))/300, 0, 1)*pnl["defl"]*(0.9 - 0.3*k)
        ax.plot(xs, ys, color=GR, lw=0.8, alpha=0.16 - 0.05*k, zorder=2)
    ax.add_patch(Polygon(np.r_[np.c_[x, yu], np.c_[x[::-1], yl[::-1]]], closed=True, fc=FILL, ec="#d8d6d6", lw=1.4, zorder=4, joinstyle="round"))
    # chord line
    ax.plot([x[0], x[-1]], [cy, cy + pnl["defl"]], color=OR, lw=0.8, alpha=0.4, ls=(0, (5, 4)), zorder=5)
    # brake line from the trailing edge
    te = np.array([x[-1], (yu[-1] + yl[-1])/2]); pull = 60 + pnl["defl"]*1.6
    ax.plot([te[0], te[0] - 30], [te[1], te[1] + pull], color=GR, lw=1.0, alpha=0.55, zorder=3)
    # lift at the centre of pressure
    j = int(pnl["cp"]*(len(cs) - 1)); base = np.array([x[j], yu[j] - 4])
    ax.plot([x[j], x[j]], [yu[j], yl[j]], color=OR, lw=1.0, alpha=0.6, zorder=5)
    arrow(base, base + np.array([0, -pnl["L"]]), OR, lw=2.2, hl=16, hw=7)
    # drag
    d0 = te + np.array([26, 0])
    arrow(d0, d0 + np.array([pnl["drag"], 0]), DIM, lw=2.0, hl=13, hw=6)
    # pitch tendency at the nose
    if pnl["pitch"] == +1: curl(x[0] + 30, cy - 12, 58, 110, 200, OR)
    elif pnl["pitch"] == -1: curl(x[0] + 30, cy - 12, 58, 200, 110, GR, a=0.8)
    # panel divider
    if i < 2: ax.plot([800*(i + 1)]*2, [70, H - 70], color=GR, lw=0.6, alpha=0.12)
fig.savefig("/tmp/brakes_raw.png", facecolor=BG); plt.close(fig)
img = np.asarray(Image.open("/tmp/brakes_raw.png").convert("RGB").resize((W, H))).astype(np.float32)/255
o = np.clip((img[..., 0] - img[..., 2])*1.8, 0, 1)
bl = np.asarray(Image.fromarray((o*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))).astype(np.float32)/255
img = np.clip(img + bl[..., None]*np.array([1.0, .459, .09])*0.4, 0, 1)
Image.fromarray((img*255).astype(np.uint8)).save(sys.argv[1] if len(sys.argv) > 1 else "brakes.jpg", quality=88, optimize=True, progressive=True)
print("ok")
