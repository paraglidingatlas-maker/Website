# Option D, F1 style: the world streaks past, light trails stream off the wing and the pod, the wing stays sharp
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
rng = np.random.default_rng(7)
src = np.asarray(Image.open('src.jpg').convert('RGB')).astype(np.float32) / 255
H, W = src.shape[:2]
cut = np.asarray(Image.open('o_cut.png')).astype(np.float32) / 255
wing = cut[..., 3:4]
lum = (src @ np.array([.299, .587, .114], np.float32))[..., None]
# the lines: thin and darker than what is just around them, in the band between the wing and the pod
lu = Image.fromarray((lum[..., 0] * 255).astype(np.uint8))
med = np.asarray(lu.filter(ImageFilter.MedianFilter(11))).astype(np.float32) / 255
dark = np.clip((med - lum[..., 0] - .025) / .05, 0, 1)
band = Image.new('L', (W, H), 0); ImageDraw.Draw(band).polygon([(1340, 880), (1640, 880), (1560, 1400), (1430, 1400)], fill=255)
band = np.asarray(band.filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
lines = (dark * band)[..., None]
wing = np.maximum(wing, lines)
# the pilot in the cockpit: helmet, body and hands, from the original photo
pm = Image.new('L', (W, H), 0); pd = ImageDraw.Draw(pm)
pd.ellipse((1494, 1343, 1550, 1390), fill=255)
pd.polygon([(1446, 1338), (1498, 1372), (1548, 1380), (1540, 1422), (1448, 1424)], fill=255)
pd.rectangle((1440, 1300, 1486, 1398), fill=255)
pm = np.asarray(pm).astype(np.float32)[..., None] / 255
mx, mn = src.max(2, keepdims=True), src.min(2, keepdims=True); sat = (mx - mn) / np.maximum(mx, 1e-4)
hill = (src[..., 2:3] > src[..., 0:1] + .06) & (sat < .5) & (lum > .18) & (lum < .6)
upper = (np.arange(H)[:, None, None] < 1384)
pm = pm * (1 - (hill & upper))
pm = Image.fromarray((pm[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(1))
pm = np.asarray(pm).astype(np.float32)[..., None] / 255
wing = np.maximum(wing, pm)

# 1. the background: black and white, darker, cooled, streaked hard to the right (the glider flies left)
bg = 1 - wing
mono = np.repeat(lum, 3, 2) * np.array([.86, .92, 1.05], np.float32)
acc = np.zeros_like(src); wt = np.zeros_like(bg); n = 90
for k in range(n):
    dx = int(k * 4.2)
    acc += np.roll(mono * bg, dx, 1); wt += np.roll(bg, dx, 1)
streak = acc / np.maximum(wt, 1e-3)
x = streak * .42
x = x * x * (3 - 2 * x) * .5 + x * .5

# 2. speed lines: thin bright streaks, long and soft, mostly in the middle band
L = Image.new('L', (W, H), 0); d = ImageDraw.Draw(L)
for _ in range(260):
    y = int(rng.normal(H * .5, H * .26)); x0 = int(rng.uniform(-W * .2, W)); ln = int(rng.uniform(W * .08, W * .55))
    d.line([(x0, y), (x0 + ln, y)], fill=int(rng.uniform(25, 120)), width=int(rng.choice([1, 1, 2, 3])))
L = L.filter(ImageFilter.GaussianBlur(1.2))
sl = np.asarray(L).astype(np.float32)[..., None] / 255
x = x + sl * np.array([.75, .82, 1.0], np.float32) * .55

# 3. light trails: from the wing tips, the trailing edge and the pod, out behind to the right edge
T = [Image.new('RGB', (W, H), 0) for _ in range(3)]
def trail(p0, colour, width, bend, layer=0):
    xs = np.linspace(p0[0], W + 60, 120)
    t = (xs - p0[0]) / (W + 60 - p0[0])
    ys = p0[1] + bend * t ** 1.6
    dd = ImageDraw.Draw(T[layer])
    for i in range(len(xs) - 1):
        fade = (1 - t[i]) ** .6
        c = tuple(int(v * fade) for v in colour)
        dd.line([(xs[i], ys[i]), (xs[i + 1], ys[i + 1])], fill=c, width=max(1, int(width * (1 - .5 * t[i]))))
RED, WHITE, LIME = (232, 17, 45), (255, 246, 236), (214, 255, 60)
# wing: upper tip, mid trailing edge, lower tip (2400 x 1600 frame)
trail((1745, 160), RED, 14, -60); trail((1755, 300), WHITE, 5, 40); trail((1700, 420), RED, 9, 70)
trail((1610, 520), LIME, 8, 90); trail((1590, 640), RED, 6, 120)
trail((1480, 930), WHITE, 4, 160)
# the pod: its tail and fin
trail((1775, 1470), RED, 16, 30); trail((1775, 1505), WHITE, 6, 50); trail((1720, 1545), RED, 8, 70)
tr = np.asarray(T[0]).astype(np.float32) / 255
glow = sum(np.asarray(T[0].filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255 * k for r, k in ((4, 1.2), (14, 1.0), (40, .9)))
x = 1 - (1 - np.clip(x, 0, 1)) * (1 - np.clip(tr + glow, 0, 1))     # screen: light adds

# 4. a little warm bloom off the wing, then the wing itself, sharp and full colour
wb = Image.fromarray((wing[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))
bloom = np.asarray(wb).astype(np.float32)[..., None] / 255 * np.array([.55, .7, .15], np.float32) * .55
x = 1 - (1 - x) * (1 - bloom)
x = x * (1 - wing) + np.clip(src * 1.06, 0, 1) * wing
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
v = np.clip(1.15 - .9 * np.sqrt(((xx - W * .62) / W) ** 2 + ((yy - H * .5) / H) ** 2) ** 1.4, .35, 1)[..., None]
x = np.clip(x * v + rng.normal(0, .01, (H, W, 1)).astype(np.float32), 0, 1)
Image.fromarray((x * 255 + .5).astype(np.uint8)).save('o_f1.jpg', quality=94, subsampling=0)
# the cutout for the word behind the wing, from this version
c = np.concatenate([x, wing], 2)
Image.fromarray((c * 255).astype(np.uint8), 'RGBA').save('o_f1cut.png')
print('ok')
