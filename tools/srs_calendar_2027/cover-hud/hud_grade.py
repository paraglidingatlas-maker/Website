import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
D = sys.argv[1]
src = np.asarray(Image.open(D + '/src.jpg').convert('RGB')).astype(np.float32) / 255
H, W = src.shape[:2]
r, g, b = src[..., 0:1], src[..., 1:2], src[..., 2:3]
lum = (src @ np.array([.299, .587, .114], np.float32))[..., None]
mx, mn = src.max(2, keepdims=True), src.min(2, keepdims=True); sat = (mx - mn) / np.maximum(mx, 1e-4)
box = np.zeros((H, W, 1), np.float32); box[470:995, 830:1120] = 1            # the wing (2400 x 1600 frame)
orange = (r > g * 1.3) & (sat > .4)
wingish = orange | (lum < .36) | ((lum > .8) & (sat < .25))
m = Image.fromarray(((wingish * box)[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))
f = m.point(lambda v: 255 if v > 127 else 0); ImageDraw.floodfill(f, (0, 0), 128)
m = f.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.3))
wing = np.asarray(m).astype(np.float32)[..., None] / 255
pod = np.zeros((H, W, 1), np.float32); pod[1280:1440, 800:1150] = 1
glove = np.zeros((H, W, 1), bool); glove[1330:1410, 950:1020] = True
podm = (((lum < .36) | (r > g * 1.3) & (sat > .4) | ((lum > .75) & glove)) * pod).astype(np.float32)   # the pod, the orange helmet, the white glove
podm = np.asarray(Image.fromarray((podm[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(1))).astype(np.float32)[..., None] / 255
# lines: thin, darker than their surroundings, between the wing and the pod
lu = Image.fromarray((lum[..., 0] * 255).astype(np.uint8))
med = np.asarray(lu.filter(ImageFilter.MedianFilter(9))).astype(np.float32) / 255
bi = Image.new('L', (W, H), 0); ImageDraw.Draw(bi).polygon([(900, 960), (1060, 900), (1030, 1300), (990, 1300)], fill=255)
band = np.asarray(bi.filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
lines = (np.clip((med - lum[..., 0] - .015) / .04, 0, 1) * band)[..., None]
subj = np.maximum(np.maximum(wing, podm), lines)
# background: dark, cold, streaked to the left (the glider flies right)
mono = np.repeat(lum, 3, 2)
bgw = 1 - subj; acc = np.zeros_like(src); wt = np.zeros_like(bgw)
for k in range(60):
    dx = -int(k * 3.5)
    acc += np.roll(mono * bgw, dx, 1); wt += np.roll(bgw, dx, 1)
st = acc / np.maximum(wt, 1e-3)
t = np.clip((st - .35) / .55, 0, 1) ** 1.4
x = np.array([.01, .025, .035], np.float32) + np.array([.10, .30, .36], np.float32) * t
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
x *= np.clip(1.25 - 1.0 * np.sqrt(((xx - W * .42) / W) ** 2 + ((yy - H * .5) / H) ** 2) ** 1.2, .3, 1)[..., None]
gs = Image.fromarray((wing[..., 0] * 255).astype(np.uint8))
glow = sum(np.asarray(gs.filter(ImageFilter.GaussianBlur(rr))).astype(np.float32)[..., None] / 255 * k for rr, k in ((12, .22), (60, .2)))
x = 1 - (1 - x) * (1 - glow * np.array([1, .45, .1], np.float32))
wc = src * .94; wc = np.where(wc > .6, .6 + (wc - .6) * .6, wc)
x = x * (1 - lines) + src * .5 * lines
x = x * (1 - podm) + src * podm
x = x * (1 - wing) + wc * wing
x = np.clip(x + np.random.default_rng(3).normal(0, .01, (H, W, 1)).astype(np.float32), 0, 1)
Image.fromarray((x * 255 + .5).astype(np.uint8)).save(D + '/work/hud.jpg', quality=95, subsampling=0)
print('ok', round(float(wing.mean()), 4))
Image.fromarray(np.concatenate([(x * 255 + .5).astype(np.uint8), (wing * 255).astype(np.uint8)], 2), 'RGBA').save(D + '/work/hud_cut.png')
