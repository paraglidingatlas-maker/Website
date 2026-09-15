"""Cloud layers for the Kenya gallery.

Four transparent layers of fractal noise, drifting at different rates against
the page scroll. Two copies are rendered in the page from these same four
files: a front copy with the middle cut out, and a back copy showing only the
middle, so the part of the sky over the cards passes behind them.

The blur is applied here, not in CSS, which means sharpness cannot be adjusted
without regenerating. BLUR is the only knob that matters for that; everything
else controls shape and density.

The vertical taper is a true sine rather than a clipped one. Clipped, each layer
ended in a hard horizontal seam, which was invisible while they were inside a
clipped frame and very visible once they ran across the page.
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

OUT = "assets/destinations/kenya/clouds"

# Blur solved for, not guessed. Cutting the radius by 30% only lifted measured
# edge detail by 12%, because the noise is band-limited and most of the radius
# is spent on frequencies that are not there. These values were found by
# bisection against a 30% detail target from the previous set (13, 9, 6, 10).
# More octaves does not help: their amplitude is negligible and the blur
# removes them anyway, tested at 6, 7, 8 and 9.
#        seed  cut   blur  alpha  height
LAYERS = [(3,  0.54,  5.59, 0.92, 1000),
          (11, 0.60,  3.19, 0.70,  880),
          (23, 0.65,  2.25, 0.55,  760),
          (41, 0.57,  4.32, 0.80,  920)]
WIDTH = 2400


def fbm(h, w, octaves, seed):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, freq = 1.0, 2
    for _ in range(octaves):
        small = rng.random((max(2, h * freq // 360), max(2, w * freq // 360)))
        up = np.asarray(Image.fromarray((small * 255).astype(np.uint8))
                        .resize((w, h), Image.BICUBIC), np.float32) / 255.0
        out += up * amp
        amp *= 0.55
        freq *= 2
    return out / out.max()


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, (seed, cut, blur, alpha, H) in enumerate(LAYERS, 1):
        n = fbm(H, WIDTH, 6, seed)
        a = np.clip((n - cut) / (1 - cut), 0, 1) ** 1.2
        yy = np.linspace(0, 1, H)[:, None]
        a *= np.sin(yy * np.pi) ** 0.75          # reaches zero at both edges
        a = ndimage.gaussian_filter(a, blur) * alpha
        rgb = np.dstack([np.full((H, WIDTH), 218, np.uint8),
                         np.full((H, WIDTH), 223, np.uint8),
                         np.full((H, WIDTH), 232, np.uint8),
                         (np.clip(a, 0, 1) * 255).astype(np.uint8)])
        path = f"{OUT}/cloud-{i}.webp"
        Image.fromarray(rgb, "RGBA").save(path, "WEBP", quality=76, method=6)
        detail = np.abs(np.diff(a, axis=1)).mean() * 1000
        print(f"  cloud-{i}  blur {blur:4.1f}  detail {detail:5.2f}  "
              f"{os.path.getsize(path)//1024}KB")
