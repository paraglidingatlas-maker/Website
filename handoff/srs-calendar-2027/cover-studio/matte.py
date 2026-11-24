# A difference matte for SRS_6_T1_51: the haze behind the glider is estimated and the glider separated from it pixel by
# pixel, so its outline (and every line) keeps its natural soft edge instead of a hard cut.
import sys, numpy as np
from PIL import Image, ImageFilter
D, O = sys.argv[1], sys.argv[2]
src = np.asarray(Image.open(D + '/src.jpg').convert('RGB')).astype(np.float32) / 255
H, W = src.shape[:2]
ld = lambda n: np.asarray(Image.open(D + '/work/' + n)).astype(np.float32)[..., None] / 255
wing, pod, lines = ld('mask_wing.png'), ld('mask_pod.png'), ld('mask_lines.png')
def f(a, flt): return np.asarray(Image.fromarray((np.clip(a[..., 0], 0, 1) * 255).astype(np.uint8)).filter(flt)).astype(np.float32)[..., None] / 255
def blur(a, r): return f(a, ImageFilter.GaussianBlur(r))
def blur3(c, r): return np.concatenate([blur(c[..., i:i + 1], r) for i in range(3)], 2)
solid = np.maximum(wing, pod)
cs = np.cumsum(np.pad(lines[..., 0], ((16, 16), (0, 0))), axis=0); vrun = (cs[31:31 + H] - cs[:H]) / 31
lines = lines * np.clip((vrun - .18) / .2, 0, 1)[..., None]
# where to look for the subject: the solid parts grown a little, and the line band
near = np.clip(f((solid > .5).astype(np.float32), ImageFilter.MaxFilter(13)) + f((lines > .2).astype(np.float32), ImageFilter.MaxFilter(5)), 0, 1)
# the background behind it: the haze around, carried in by a masked blur (twice, wide then tighter)
bgm = 1 - f(near, ImageFilter.MaxFilter(15))
B = blur3(src * bgm, 30) / np.maximum(blur(bgm, 30), 1e-3)
B2 = blur3(src * bgm, 12) / np.maximum(blur(bgm, 12), 1e-3)
B = np.where(blur(bgm, 12) > .15, B2, B)
d = np.sqrt(((src - B) ** 2).sum(2, keepdims=True))
# alpha: solid inside (the masks, pulled in), the difference from the haze at the edges and along the lines
core = (f(solid, ImageFilter.MinFilter(7)) > .5).astype(np.float32)
near_solid = f((wing > .5).astype(np.float32), ImageFilter.MaxFilter(13))      # the wing's edge against clean haze; the pod's is done from inside (fields behind it)
on_line = f((lines > .15).astype(np.float32), ImageFilter.MaxFilter(3))
alpha_edge = np.clip((d - .035) / .20, 0, 1) * np.clip(near_solid + on_line, 0, 1)   # away from the wing and pod, only on the lines
alpha = np.maximum(core, alpha_edge)
alpha = np.where(near > 0, alpha, 0)
alpha = np.maximum(alpha, blur(core, 1.2))
# the subject's own colour, with the haze taken out of each edge pixel
F = np.where(alpha > .02, B + (src - B) / np.maximum(alpha, .08), 0)
F = np.where(core > .5, src, np.clip(F, 0, 1))
# the pod: a tight edge, its rim coloured from just inside (no fields, no haze)
pcore = (f(pod, ImageFilter.MinFilter(9)) > .5).astype(np.float32)
num = blur3(src * pcore, 6); den = blur(pcore, 6)
pext = np.where(den > .02, num / np.maximum(den, 1e-3), src)
pa = blur((f(pod, ImageFilter.MinFilter(3)) > .5).astype(np.float32), 1.0)
podzone = f((pod > .5).astype(np.float32), ImageFilter.MaxFilter(11)) * (1 - near_solid)
F = np.where(podzone > .5, src * pcore + pext * (1 - pcore), F)
alpha = np.where(podzone > .5, np.maximum(pa, alpha_edge * on_line), alpha)
# lone flecks: drop alpha islands smaller than a line segment
isl = f((alpha > .25).astype(np.float32), ImageFilter.MedianFilter(5))
alpha = alpha * np.clip(isl + core + on_line * (vrun[..., None] > .3), 0, 1)
Image.fromarray(np.concatenate([(F * 255 + .5).astype(np.uint8), (np.clip(alpha, 0, 1) * 255 + .5).astype(np.uint8)], 2), 'RGBA').save(O + '/matte.png')
Image.fromarray((wing[..., 0] * 255).astype(np.uint8)).save(O + '/wing.png')
print('ok', round(float(alpha.mean()), 4))
