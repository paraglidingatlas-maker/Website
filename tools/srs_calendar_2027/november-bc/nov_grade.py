import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
D = sys.argv[1]
src = np.asarray(Image.open(D + '/src.jpg').convert('RGB')).astype(np.float32) / 255
H, W = src.shape[:2]
r, g, b = src[..., 0:1], src[..., 1:2], src[..., 2:3]
lum = (src @ np.array([.299, .587, .114], np.float32))[..., None]
box = np.zeros((H, W, 1), np.float32)
box[450:850, 1090:2080] = 1          # the wing (2400 x 1600 frame)
box[990:1220, 1490:1660] = 1         # the pod and pilot
yellow = ((r > .5) & (g > .38) & (b < g * .62) & (r > b * 1.8)) | ((r > .62) & (g > .56) & (b < g * .86) & (r > b * 1.22))
m = Image.fromarray(((yellow * box)[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
f = m.point(lambda v: 255 if v > 127 else 0); ImageDraw.floodfill(f, (0, 0), 128)
m = f.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.4))
wing = np.asarray(m).astype(np.float32)[..., None] / 255
# the pilot's dark body and arms on the pod
pil = np.zeros((H, W, 1), np.float32); pil[1010:1110, 1505:1615] = 1
wing = np.maximum(wing, ((lum < .3) * pil).astype(np.float32))
# broadcast grade: steel teal by brightness, deep navy shadows, crushed towards the edges
lo, hi = np.array([.015, .03, .05], np.float32), np.array([.36, .52, .60], np.float32)
t = np.clip(lum, 0, 1) ** 1.6
bg = lo + (hi - lo) * t
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vig = np.clip(1.2 - 1.0 * np.sqrt(((xx - W * .62) / W) ** 2 + ((yy - H * .5) / H) ** 2) ** 1.4, .28, 1)[..., None]
bg = bg * vig
gs = Image.fromarray((wing[..., 0] * 255).astype(np.uint8))
glow = sum(np.asarray(gs.filter(ImageFilter.GaussianBlur(rr))).astype(np.float32)[..., None] / 255 * k for rr, k in ((10, .16), (50, .16), (140, .14)))
glow = glow * np.array([1.0, .78, .1], np.float32)
x = 1 - (1 - np.clip(bg, 0, 1)) * (1 - np.clip(glow, 0, 1))
w2 = src + (src - lum) * .12
w2 = np.clip(w2, 0, 1) * .86
w2 = np.where(w2 > .55, .55 + (w2 - .55) * .62, w2)          # roll the highlights off: the panels and seams show
x = x * (1 - wing) + w2 * wing
x = np.clip(x + np.random.default_rng(6).normal(0, .009, (H, W, 1)).astype(np.float32), 0, 1)
Image.fromarray((x * 255 + .5).astype(np.uint8)).save(D + '/work/nov_bc.jpg', quality=95, subsampling=0)
print('ok', round(float(wing.mean()), 4))
