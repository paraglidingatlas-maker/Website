import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
D = sys.argv[1]
src = np.asarray(Image.open(D + '/src.jpg').convert('RGB')).astype(np.float32) / 255
H, W = src.shape[:2]
r, g, b = src[..., 0:1], src[..., 1:2], src[..., 2:3]
lum = (src @ np.array([.299, .587, .114], np.float32))[..., None]
mx, mn = src.max(2, keepdims=True), src.min(2, keepdims=True); sat = (mx - mn) / np.maximum(mx, 1e-4)
box = np.zeros((H, W, 1), np.float32); box[180:870, 1140:1920] = 1            # the wing (2400 x 1600 frame)
lime = (g > b * 1.35) & (g > .35) & (sat > .3)
red = (r > g * 1.4) & (r > .35) & (sat > .4)
notsky = ~((b > r * 1.12) & (b > g * 1.02)) & (sat > .16)
m = Image.fromarray((((lime | red | notsky) * box)[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(27)).filter(ImageFilter.MinFilter(27))
f = m.point(lambda v: 255 if v > 127 else 0); ImageDraw.floodfill(f, (0, 0), 128)
m = f.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.4))
wing = np.asarray(m).astype(np.float32)[..., None] / 255
# dusk: every pixel outside the wing is re-lit by its brightness, along a sky that runs indigo (top) to amber (low)
y = (np.arange(H, dtype=np.float32) / H)[:, None, None]
def ramp(stops, t):
    out = np.zeros(t.shape[:2] + (3,), np.float32)
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        k = np.clip((t - t0) / (t1 - t0), 0, 1)
        sel = (t >= t0) & (t <= t1)
        out = np.where(sel, np.array(c0, np.float32) + (np.array(c1, np.float32) - np.array(c0, np.float32)) * k, out)
    return out
yy = np.repeat(y, W, 1)
sky = ramp([(0, (.07, .06, .19)), (.45, (.36, .13, .30)), (.8, (.80, .33, .25)), (1.0, (.96, .55, .28))], yy)
sky = sky * (.75 + .5 * np.clip((lum - .45) / .4, 0, 1))          # the sky keeps its own gentle shading
cloud = np.clip(1 - sat * 2.4, 0, 1) ** 1.2                         # white and grey: the clouds (and the dark pod)
shade, lit = np.array([.16, .10, .22], np.float32), np.array([1.0, .80, .62], np.float32)
cl = shade + (lit - shade) * np.clip((lum - .3) / .6, 0, 1) ** 1.1
bg = sky * (1 - cloud) + cl * cloud
xx = np.arange(W, dtype=np.float32)[None, :, None] / W
bg *= np.clip(1.1 - .6 * ((xx - .72) ** 2 + (y - .62) ** 2) ** .8, .45, 1)
sil = np.clip((.34 - lum) / .16, 0, 1)                                # the pod, the pilot and the lines: silhouettes
bg = bg * (1 - sil) + (np.array([.05, .03, .07], np.float32) + lum * .15) * sil
# the wing: its own colours, a touch warmer, highlights held back (never over-exposed)
w2 = src * np.array([1.0, .95, .86], np.float32) * .9
w2 = np.where(w2 > .55, .55 + (w2 - .55) * .6, w2)
gs = Image.fromarray((wing[..., 0] * 255).astype(np.uint8))
glow = sum(np.asarray(gs.filter(ImageFilter.GaussianBlur(rr))).astype(np.float32)[..., None] / 255 * k for rr, k in ((30, .10), (110, .10)))
x = 1 - (1 - np.clip(bg, 0, 1)) * (1 - glow * np.array([1, .75, .3], np.float32))
x = x * (1 - wing) + w2 * wing
x = np.clip(x + np.random.default_rng(12).normal(0, .009, (H, W, 1)).astype(np.float32), 0, 1)
Image.fromarray((x * 255 + .5).astype(np.uint8)).save(D + '/work/dec.jpg', quality=95, subsampling=0)
print('ok', round(float(wing.mean()), 4))
