# The studio scene for the cover, at print size (3369 x 2382, A4 landscape at 3x): a slate backdrop under a top spotlight,
# a floor, the glider's motion smear behind it, the glider lit from above, a soft shadow on the floor.
import sys, numpy as np
from PIL import Image, ImageFilter
O = sys.argv[1]
PW, PH = 3369, 2382
m = Image.open(O + '/matte.png'); wingm = Image.open(O + '/wing.png')
k = 1.455; ox, oy = 254, -304                                   # the photo frame on the page (glider centred, top at y 380)
gw, gh = int(2400 * k), int(1600 * k)
g = m.resize((gw, gh), Image.LANCZOS); wm = wingm.resize((gw, gh), Image.LANCZOS)
G = np.zeros((PH, PW, 4), np.float32); WM = np.zeros((PH, PW, 1), np.float32)
x0, y0 = max(0, ox), max(0, oy); sx, sy = x0 - ox, y0 - oy
w_, h_ = min(gw - sx, PW - x0), min(gh - sy, PH - y0)
G[y0:y0 + h_, x0:x0 + w_] = np.asarray(g).astype(np.float32)[sy:sy + h_, sx:sx + w_] / 255
WM[y0:y0 + h_, x0:x0 + w_, 0] = np.asarray(wm).astype(np.float32)[sy:sy + h_, sx:sx + w_] / 255
rgb, a = G[..., :3], G[..., 3:]
yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32); X, Y = xx[..., None] / PW, yy[..., None] / PH
def blur(arr, r):
    return np.asarray(Image.fromarray((np.clip(arr[..., 0], 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32)[..., None] / 255
# backdrop: slate, a soft spotlight from above on the glider, the corners falling to near black
base = np.array([.055, .065, .075], np.float32)
spot = np.exp(-(((X - .5) / .34) ** 2 + ((Y - .42) / .5) ** 2))
top = np.exp(-(((X - .5) / .16) ** 2 + ((Y + .05) / .35) ** 2))          # the light's own glow at the top
bd = base + np.array([.24, .27, .30], np.float32) * spot ** 1.3 + np.array([.10, .11, .12], np.float32) * top
# the floor: from about two thirds down, a little lighter under the glider, fading out
fl = np.clip((Y - .74) / .06, 0, 1) * np.exp(-(((X - .5) / .32) ** 2)) * np.clip(1.1 - (Y - .74) * 2.2, 0, 1)
bd = bd + np.array([.05, .055, .06], np.float32) * fl
# speed: the glider's silhouette smeared to the left (it flies right) as a dark trail, and soft horizontal light streaks
sil = a.copy()
acc = np.zeros_like(sil)
for i in range(1, 70):
    acc += np.roll(sil, -int(i * 11), 1) * (1 - i / 70)
trail = np.clip(blur(acc / 22, 6), 0, 1)
bd = bd * (1 - trail * .55)
rng = np.random.default_rng(31); st = np.zeros((PH, PW), np.float32)
for _ in range(90):
    y = int(np.clip(rng.normal(.5, .16), .2, .8) * PH); x1 = int(rng.uniform(.0, .55) * PW); ln = int(rng.uniform(.15, .5) * PW)
    st[y:y + rng.integers(2, 7), x1:min(PW, x1 + ln)] += rng.uniform(.02, .07)
st = np.asarray(Image.fromarray((np.clip(st, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))).astype(np.float32)[..., None] / 255
bd = bd + st * spot * np.array([.9, .95, 1.0], np.float32)
# the shadow on the floor beneath the pod
sh = np.exp(-(((X - .502) / .11) ** 2 + ((Y - .805) / .016) ** 2))
bd = bd * (1 - sh[..., :1] * .55)
bd = np.clip(bd + rng.normal(0, .006, (PH, PW, 1)).astype(np.float32), 0, 1)
Image.fromarray((bd * 255 + .5).astype(np.uint8)).save(O + '/backdrop.png')
# the glider, lit from above: the wing a touch brighter at the top, everything a little cooler in the shadows like the room
lift = np.clip(1.08 - (Y - .2) * .35, .9, 1.1)
rgb2 = rgb * lift
rgb2 = np.where(rgb2 > .66, .66 + (rgb2 - .66) * .55, rgb2)
rgb2 = rgb2 * (1 - WM * 0) + 0
cool = np.array([.97, .99, 1.03], np.float32)
rgb2 = rgb2 * (1 - (1 - np.clip(rgb2.mean(2, keepdims=True) * 2, 0, 1)) * (1 - cool))
Image.fromarray(np.concatenate([(np.clip(rgb2, 0, 1) * 255 + .5).astype(np.uint8), (np.clip(a, 0, 1) * 255 + .5).astype(np.uint8)], 2), 'RGBA').save(O + '/glider_layer.png')
comp = bd * (1 - a) + rgb2 * a
Image.fromarray((np.clip(comp, 0, 1) * 255 + .5).astype(np.uint8)).resize((1200, 848), Image.LANCZOS).save(O + '/scene_prev.jpg', quality=88)
print('ok')
