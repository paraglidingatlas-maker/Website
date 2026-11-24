# The glider alone, lit as a studio object for a black page: wing, lines, pod; plus its mirror reflection and the orange light.
import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
D, O = sys.argv[1], sys.argv[2]
src = np.asarray(Image.open(D + '/src.jpg').convert('RGB')).astype(np.float32) / 255
H, W = src.shape[:2]
ld = lambda n: np.asarray(Image.open(D + '/work/' + n)).astype(np.float32)[..., None] / 255
wing, pod, lines = ld('mask_wing.png'), ld('mask_pod.png'), ld('mask_lines.png')
# real lines run almost vertically: keep only line pixels that continue up and down (a 31px vertical run), not flecks of field
cs = np.cumsum(np.pad(lines[..., 0], ((16, 16), (0, 0))), axis=0)
vrun = (cs[31:31 + H] - cs[:H]) / 31
lines = lines * (np.clip((vrun - .18) / .2, 0, 1))[..., None]
def blur(a, r): return np.asarray(Image.fromarray((np.clip(a[..., 0], 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32)[..., None] / 255
def erode(a, k): return np.asarray(Image.fromarray((np.clip(a[..., 0], 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(k))).astype(np.float32)[..., None] / 255
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); X, Y = xx[..., None] / W, yy[..., None] / H
# the wing: key light from the upper left, rim on the right (leading) edge, highlights held back
key = np.clip(1.12 - ((X - .36) * 1.6 + (Y - .3) * 1.1), .8, 1.15)
wc = src * key; wc = np.where(wc > .64, .64 + (wc - .64) * .55, wc)
gx = np.gradient(blur(wing, 6)[..., 0], axis=1)[..., None]
rim = blur(np.clip(wing - erode(wing, 9), 0, 1) * np.clip(-gx * 60, 0, 1), 1.5)
wc = 1 - (1 - wc) * (1 - rim * np.array([1.0, .93, .82], np.float32) * .8)
# the pod: lifted from near-black so it reads on black, its top edge lit
pc = src * 1.25 + .05
pin = np.clip(pod - erode(pod, 7), 0, 1)
top = blur(pin * (np.gradient(blur(pod, 4)[..., 0], axis=0)[..., None] > 0), 1.2)
pc = 1 - (1 - np.clip(pc, 0, 1)) * (1 - top * .7)
# the lines, exactly where they are in the photo, lit pale against the black
lc = np.ones_like(src) * np.array([.86, .84, .8], np.float32)
la = np.clip(lines * 1.4, 0, 1) * .85
rgb = np.zeros_like(src); a = np.zeros_like(lines)
rgb = rgb * (1 - la) + lc * la; a = np.maximum(a, la)
# clean edges: tighten each mask a little and give its rim the colour from just inside, so no haze shows on black
def clean(col, m, grow=6):
    core = (erode(m, 9) > .5).astype(np.float32)
    num = np.concatenate([blur(col[..., i:i + 1] * core, grow) for i in range(3)], 2)
    den = blur(core, grow)
    ext = np.where(den > .02, num / np.maximum(den, 1e-3), col)
    col2 = col * core + ext * (1 - core)
    tight = blur((erode(m, 3) > .5).astype(np.float32), 1.0)
    return np.clip(col2, 0, 1), tight
pc, pod = clean(np.clip(pc, 0, 1), pod)
wc, wing = clean(np.clip(wc, 0, 1), wing)
rgb = rgb * (1 - pod) + pc * pod; a = np.maximum(a, pod)
rgb = rgb * (1 - wing) + wc * wing; a = np.maximum(a, wing)
rgb = np.where(a > 1e-3, rgb, 0)
# canvas taller than the photo, for the reflection below the pod
EXTRA = 400; L = 1452                                                    # the mirror line, just under the pod
can = np.zeros((H + EXTRA, W, 4), np.float32)
can[:H, :, :3] = rgb; can[:H, :, 3:] = a
ref = np.zeros_like(can)
for y in range(L, L + EXTRA):
    sy = 2 * L - y
    if 0 <= sy < H:
        f = max(0.0, 1 - (y - L) / 230) ** 1.6 * .38
        ref[y, :, :3] = can[sy, :, :3]; ref[y, :, 3] = can[sy, :, 3] * f
ref[..., :3] *= .8
refi = Image.fromarray((np.clip(ref, 0, 1) * 255).astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(1.5))
Image.fromarray((np.clip(can, 0, 1) * 255).astype(np.uint8), 'RGBA').save(O + '/glider.png')
refi.save(O + '/reflection.png')
# orange light: a bundle of fine streaks falling from the top right, and a faint warm haze
SW, SH = 2246, 1588
st = Image.new('L', (SW, SH), 0); d = ImageDraw.Draw(st); rng = np.random.default_rng(14)
for i in range(260):
    x0 = rng.normal(SW * .83, SW * .055); bend = rng.normal(-SW * .05, SW * .03); ln = rng.uniform(.35, .85) * SH
    pts = [(x0 + bend * (t ** 1.8) + rng.normal(0, .6), t * ln) for t in np.linspace(0, 1, 40)]
    for j in range(len(pts) - 1):
        fade = (1 - j / len(pts)) ** 1.2
        d.line([pts[j], pts[j + 1]], fill=int(rng.uniform(30, 150) * fade), width=int(rng.choice([1, 1, 2, 3])))
st = np.asarray(st).astype(np.float32) / 255
soft = np.asarray(Image.fromarray((st * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255
lightm = np.clip(st * .9 + soft * 1.6, 0, 1)[..., None]
col = np.array([1.0, .42, .1], np.float32)
img = np.concatenate([np.broadcast_to(col, (SH, SW, 3)), lightm], 2)
Image.fromarray((img * 255).astype(np.uint8), 'RGBA').save(O + '/streaks.png')
print('ok', can.shape)
