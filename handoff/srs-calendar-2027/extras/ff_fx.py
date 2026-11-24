# Five "street racing / open-world game" concepts for December, from SRS_6_T6_106. Original looks; no film or game marks.
import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageOps
D, O = sys.argv[1], sys.argv[2]
src = np.asarray(Image.open(D + '/src.jpg').convert('RGB')).astype(np.float32) / 255
H, W = src.shape[:2]
r, g, b = src[..., 0:1], src[..., 1:2], src[..., 2:3]
lum = (src @ np.array([.299, .587, .114], np.float32))[..., None]
mx, mn = src.max(2, keepdims=True), src.min(2, keepdims=True); sat = (mx - mn) / np.maximum(mx, 1e-4)
# the wing (as dec_grade.py) and the dark parts (pod, pilot, lines)
box = np.zeros((H, W, 1), np.float32); box[180:870, 1140:1920] = 1
lime = (g > b * 1.35) & (g > .35) & (sat > .3); red = (r > g * 1.4) & (r > .35) & (sat > .4)
notsky = ~((b > r * 1.12) & (b > g * 1.02)) & (sat > .16)
m = Image.fromarray((((lime | red | notsky) * box)[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(27)).filter(ImageFilter.MinFilter(27))
f = m.point(lambda v: 255 if v > 127 else 0); ImageDraw.floodfill(f, (0, 0), 128)
wm = f.point(lambda v: 0 if v == 128 else 255)
wing = np.asarray(wm.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.4))).astype(np.float32)[..., None] / 255
sil = np.clip((.34 - lum) / .16, 0, 1)
lu = Image.fromarray((lum[..., 0] * 255).astype(np.uint8))
med = np.asarray(lu.filter(ImageFilter.MedianFilter(9))).astype(np.float32) / 255
bandi = Image.new('L', (W, H), 0); ImageDraw.Draw(bandi).polygon([(1300, 700), (1900, 420), (1800, 1250), (1660, 1260)], fill=255)
bandm = np.asarray(bandi.filter(ImageFilter.GaussianBlur(8))).astype(np.float32) / 255
lines = (np.clip((med - lum[..., 0] - .02) / .05, 0, 1) * bandm)[..., None]
subj = np.maximum(wing, sil)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); Y, X = yy[..., None] / H, xx[..., None] / W
def save(x, n): Image.fromarray((np.clip(x, 0, 1) * 255 + .5).astype(np.uint8)).save(f'{O}/{n}.jpg', quality=94, subsampling=0)
def blur(a, rad):
    return np.asarray(Image.fromarray((np.clip(a[..., 0], 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(rad))).astype(np.float32)[..., None] / 255
def screen(a, b_): return 1 - (1 - np.clip(a, 0, 1)) * (1 - np.clip(b_, 0, 1))
cloud = np.clip(1 - sat * 2.4, 0, 1) ** 1.2 * (1 - sil)
rng = np.random.default_rng(21)
def grain(x, k=.012): return x + rng.normal(0, k, (H, W, 1)).astype(np.float32)
wingc = np.where(src * .92 > .55, .55 + (src * .92 - .55) * .6, src * .92)       # the wing, never blown out
# rim: a band just outside the wing and the pod
outer = np.asarray(Image.fromarray((subj[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))).astype(np.float32)[..., None] / 255
rim = np.clip(outer - subj, 0, 1)

# 1 NEON: night city sky, magenta and cyan, the wing and pod rimmed in neon
sky = np.array([.02, .02, .06], np.float32) + (np.array([.20, .03, .22], np.float32) - .0) * Y ** 1.6
cl = (np.array([.05, .35, .45], np.float32) * (1 - X) + np.array([.55, .08, .45], np.float32) * X) * np.clip((lum - .35) / .6, 0, 1) ** 1.3
x = sky * (1 - cloud) + (sky + cl) * cloud
x = x * (1 - sil) + np.array([.01, .01, .03], np.float32) * sil
neon = blur(rim, 3) * 1.6 * np.array([1.0, .15, .75], np.float32) + blur(rim, 18) * 1.2 * np.array([.15, .85, 1.0], np.float32)
x = screen(x, neon)
x = screen(x, lines * np.array([.35, .9, 1.0], np.float32) * .9 + blur(lines, 4) * np.array([.2, .6, 1.0], np.float32) * .6)
x = x * (1 - wing) + wingc * .95 * wing
save(grain(x), 'c1_neon')

# 2 NITRO: a zoom burst behind the glider, teal shadows, orange light, flares off the wing tips
cx, cy = .66, .42
acc = np.zeros_like(src); wt = np.zeros_like(lum)
bgsrc = src * (1 - subj)
for k in np.linspace(0, .38, 34):
    s = 1 + k
    im = Image.fromarray((bgsrc * 255).astype(np.uint8)).resize((int(W * s), int(H * s)), Image.BILINEAR)
    ox, oy = int(cx * W * k), int(cy * H * k)
    a = np.asarray(im.crop((ox, oy, ox + W, oy + H))).astype(np.float32) / 255
    mm = Image.fromarray(((1 - subj[..., 0]) * 255).astype(np.uint8)).resize((int(W * s), int(H * s)), Image.BILINEAR)
    mw = np.asarray(mm.crop((ox, oy, ox + W, oy + H))).astype(np.float32)[..., None] / 255
    acc += a; wt += mw
z = acc / np.maximum(wt, 1e-3)
zl = (z @ np.array([.299, .587, .114], np.float32))[..., None]
tealorange = np.array([.02, .16, .2], np.float32) + (np.array([1.0, .62, .3], np.float32) - np.array([.02, .16, .2], np.float32)) * np.clip((zl - .3) / .62, 0, 1) ** 1.5
x = tealorange * (1 - sil) + np.array([.02, .03, .04], np.float32) * sil
x = x * (1 - lines * .8)
d = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
x = screen(x, np.clip(.5 - d, 0, 1) ** 2 * np.array([1.0, .55, .2], np.float32) * 1.4)
fl = Image.new('L', (W, H), 0); dd = ImageDraw.Draw(fl)
for (px, py) in ((1170, 520), (1890, 470)):
    dd.line([(px - 900, py), (px + 900, py)], fill=255, width=3)
fl = np.asarray(fl.filter(ImageFilter.GaussianBlur(4))).astype(np.float32)[..., None] / 255
x = screen(x, (fl + blur(fl, 30) * 2) * np.array([1.0, .7, .4], np.float32))
x = x * (1 - wing) + wingc * wing
save(grain(x), 'c2_nitro')

# 3 COLLAGE: an illustrated, inked look (flat colour, black outlines) under a warm late sky; panels are built on the page
q = Image.fromarray((src * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9))
q = ImageOps.posterize(q, 3)
qa = np.asarray(q).astype(np.float32) / 255
ql = (qa @ np.array([.299, .587, .114], np.float32))[..., None]
skyc = np.array([.16, .30, .62], np.float32) * (1 - Y) + np.array([.98, .55, .32], np.float32) * Y
x = np.where(cloud > .5, np.array([1.0, .93, .82], np.float32) * (.75 + .25 * ql), skyc * (.8 + .3 * ql))
x = x * (1 - sil) + np.array([.06, .05, .08], np.float32) * sil
edges = np.asarray(Image.fromarray((src * 255).astype(np.uint8)).convert('L').filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))).astype(np.float32)[..., None] / 255
ink = np.clip((edges - .12) / .2, 0, 1)
wq = np.where(wing > .5, qa, x)
x = x * (1 - wing) + wq * 1.02 * wing
x = x * (1 - ink * .85)
save(x, 'c3_collage')

# 4 BLOCKBUSTER: heavy teal and orange, an anamorphic flare across the sky, deep contrast
base = src.copy()
tl = np.clip((lum - .25) / .65, 0, 1)
tealsky = np.array([.01, .10, .14], np.float32) + np.array([.10, .42, .50], np.float32) * tl ** 1.2
gold = np.array([.20, .10, .05], np.float32) + np.array([.95, .70, .42], np.float32) * tl ** 1.1
x = tealsky * (1 - cloud) + gold * cloud
x = x * x * (3 - 2 * x) * .5 + x * .5
x = x * (1 - sil) + np.array([.01, .02, .03], np.float32) * sil
x = x * (1 - lines * .7)
fl = Image.new('L', (W, H), 0); ImageDraw.Draw(fl).line([(0, 330), (W, 330)], fill=255, width=4)
flr = np.asarray(fl.filter(ImageFilter.GaussianBlur(3))).astype(np.float32)[..., None] / 255
spot = np.exp(-(((X - .79) * 6) ** 2 + ((Y - .2) * 9) ** 2))
x = screen(x, (flr * (.4 + 1.2 * np.exp(-((X - .79) * 2.5) ** 2)) + spot * .7) * np.array([.55, .85, 1.0], np.float32))
x = x * (1 - wing) + wingc * np.array([1.02, .98, .9], np.float32) * wing
v = np.clip(1.15 - .8 * np.sqrt((X - .6) ** 2 + (Y - .45) ** 2) ** 1.4, .35, 1)
save(grain(x * v), 'c4_blockbuster')

# 5 RETRO SUNSET: a striped sun behind the glider, magenta to orange sky, the clouds as dark violet shapes
sky = np.array([.10, .03, .22], np.float32) * (1 - Y) + np.array([1.0, .36, .38], np.float32) * Y ** .9
sx, sy, sr = .68 * W, .5 * H, .3 * H
dsun = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2)[..., None]
sunc = np.array([1.0, .86, .34], np.float32) * (1 - (yy[..., None] - (sy - sr)) / (2 * sr)) + np.array([1.0, .22, .52], np.float32) * ((yy[..., None] - (sy - sr)) / (2 * sr))
band = ((yy[..., None] - sy) > 0) & ((((yy[..., None] - sy) / 26).astype(int) % 2) == 0) & ((yy[..., None] - sy) / sr > (((yy[..., None] - sy) / 26).astype(int) * 26 / sr) * 0)
stripe = ((yy[..., None] > sy) & (((yy[..., None] - sy) % 46) < (6 + 28 * (yy[..., None] - sy) / sr)))
sun = (dsun < sr) & ~stripe
x = np.where(sun, np.clip(sunc, 0, 1), sky)
x = x * (1 - cloud * .9) + np.array([.18, .05, .22], np.float32) * (.6 + .6 * lum) * cloud * .9
x = x * (1 - sil) + np.array([.05, .01, .08], np.float32) * sil
x = x * (1 - wing) + wingc * wing
save(grain(x, .01), 'c5_retro')
Image.fromarray((wing[..., 0] * 255).astype(np.uint8)).save(f'{O}/wingmask.png')
print('ok')
