import numpy as np
from PIL import Image, ImageFilter
src = np.asarray(Image.open('src.jpg').convert('RGB')).astype(np.float32) / 255
H, W = src.shape[:2]
lum = (src @ np.array([.299, .587, .114], np.float32))[..., None]
mx, mn = src.max(2, keepdims=True), src.min(2, keepdims=True)
sat = (mx - mn) / np.maximum(mx, 1e-4)
r, g, b = src[..., 0:1], src[..., 1:2], src[..., 2:3]
# the wing and harness: lime/yellow/red, strongly saturated, and warmer than the blue-green hills
box = np.zeros((H, W, 1), np.float32)
box[110:950, 1300:1790] = 1      # the wing (2400 x 1600 frame)
box[1370:1560, 1260:1790] = 1    # the pilot and harness
hue = (sat > .3) & (g > b * 1.55) & (lum > .16)          # lime and yellow, sunlit or shaded
red = (r > g * 1.35) & (r > .4) & (sat > .4)             # the red stripes
pil = (lum > .55) & (sat < .25)                          # the helmet
wing = ((hue | red) * box[..., 0:1] > 0) | ((pil * box[..., 0:1]) > 0) & (yy0 := 0) == 0
wing = (((hue | red) | (pil & (np.arange(H)[:, None, None] > 1370))) * box).astype(np.float32)
# above the ridge the wing stands against sky only: there, anything not sky is wing (its shaded leading edge too),
# filled across each row between the wing's outer edges
rows = np.arange(H)[:, None, None] < 800
sky = (b >= g * .97) | ((lum > .62) & (sat < .2))
loose = (~sky & (lum > .06) & rows & (box > 0)).astype(np.float32)
wing = np.maximum(wing, loose)
wa = wing[..., 0] > .5
for y in range(110, 800):
    xs = np.nonzero(wa[y, 1300:1790])[0]
    if len(xs) > 1:
        wa[y, 1300 + xs[0]:1300 + xs[-1] + 1] = True
wing = np.maximum(wing, wa[..., None].astype(np.float32))
m = Image.fromarray((wing[..., 0] * 255).astype(np.uint8))
m = m.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.MinFilter(21))   # close the black logo and seams
from PIL import ImageDraw
b = m.point(lambda v: 255 if v > 127 else 0)
f = b.copy(); ImageDraw.floodfill(f, (0, 0), 128)                       # the outside
m = f.point(lambda v: 0 if v == 128 else 255)                            # everything not reached from outside: wing + holes
m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(2))
wing = np.asarray(m).astype(np.float32)[..., None] / 255
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def vig(cx, cy, k=.8, lo=.55):
    rr = np.sqrt(((xx - W * cx) / W) ** 2 + ((yy - H * cy) / H) ** 2)
    return np.clip(1.12 - k * rr ** 1.5, lo, 1)[..., None]
def save(x, n):
    x = np.clip(x + np.random.default_rng(3).normal(0, .008, (H, W, 1)).astype(np.float32), 0, 1)
    Image.fromarray((x * 255 + .5).astype(np.uint8)).save(n, quality=94, subsampling=0)
def s(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
# 1 natural: gentle S curve, a little less saturation in the land, vignette
x = s(src) * .5 + src * .5
l2 = (x @ np.array([.299, .587, .114], np.float32))[..., None]
x = l2 + (x - l2) * (.9 + .25 * wing)
save(x * vig(.6, .45), 'o_nat.jpg')
# 2 dusk: land and sky pulled down and cooled, the wing kept bright
d = src * np.array([.78, .86, 1.0], np.float32) * .62
d = s(d) * .4 + d * .6
d = d * (1 - wing) + np.clip(src * 1.05, 0, 1) * wing
save(d * vig(.6, .4, 1.0, .35), 'o_dusk.jpg')
# 3 colour pop: everything but the wing and harness in black and white
m = s(lum * 1.05) * .6 + lum * .4
p = np.repeat(m, 3, 2) * np.array([.97, .99, 1.03], np.float32)
p = p * (1 - wing) + np.clip(src * 1.04, 0, 1) * wing
save(p * vig(.6, .45), 'o_pop.jpg')
# cutout for the depth layout (the word behind the wing): the wing and harness alone
cut = np.concatenate([np.asarray(Image.open('o_nat.jpg')).astype(np.float32) / 255, wing], 2)
Image.fromarray((cut * 255).astype(np.uint8), 'RGBA').save('o_cut.png')
print('done', round(float(wing.mean()), 4))
# 4 speed: the hills and sky streak past (a slanted motion blur), the wing and pilot stay sharp
bg = 1 - wing; acc = np.zeros_like(src); wt = np.zeros_like(bg); n = 48
for k in range(n):
    dx, dy = int(k * 2.2), int(k * .7)
    acc += np.roll(np.roll(src * bg, dx, 1), dy, 0); wt += np.roll(np.roll(bg, dx, 1), dy, 0)
blur = acc / np.maximum(wt, 1e-3)          # the background streaks; the wing's colour never smears into it
x = blur * (1 - wing) + src * wing
x = s(x) * .45 + x * .55
save(x * np.array([.97, .99, 1.02], np.float32) * vig(.62, .5, .9, .45), 'o_fx.jpg')
