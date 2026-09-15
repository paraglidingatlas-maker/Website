"""Prepare the gallery photographs and find the canopy in each.

The carousel crops 3:2 photographs into 2:3 portrait cards, which keeps 44% of
each frame. That is only acceptable because the crop is centred on the wing
rather than on the middle of the picture.

The wing is findable without any kind of model: terrain here is green, brown and
haze, so the canopy is the only strongly saturated thing in frame. The first
version ranked candidate blobs by AREA and picked sunlit ground on two of the
eleven. Ranking by mean score instead found the canopy every time. Verified
against every photograph by eye before shipping.
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = [("longonot", "assets/destinations/kenya/hero/longonot.jpg", "Mount Longonot"),
       ("kerio-valley", "assets/destinations/kenya/hero/kerio-valley.jpg", "Kerio Valley"),
       ("equator", "assets/destinations/kenya/hero/equator.jpg", "The Equator"),
       ("north-kenya", "assets/destinations/kenya/hero/north-kenya.jpg", "Northern Kenya"),
       ("chyulu-hills", "assets/destinations/kenya/hero/chyulu-hills.jpg", "Chyulu Hills"),
       ("kenya-hero", "assets/images/kenya-hero.jpg", ""),
       ("kenya-high", "assets/images/kenya-high.jpg", ""),
       ("kenya-launch", "assets/images/kenya-launch.jpg", ""),
       ("kenya-ridge", "assets/images/kenya-ridge.jpg", ""),
       ("kenya-slope", "assets/images/kenya-slope.jpg", ""),
       ("kenya-3", "assets/images/kenya-3.jpg", "")]
OUT = "assets/destinations/kenya/gallery"


def wing(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((600, 600))
    a = np.asarray(im).astype(np.float32) / 255.0
    mx, mn = a.max(2), a.min(2)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    notgreen = np.clip(1.0 - (g - np.maximum(r, b)) * 3.0, 0, 1)
    score = sat * notgreen * np.clip(mx, 0, 1)
    m = ndimage.binary_closing(score >= np.percentile(score, 99.0), np.ones((3, 3)))
    lab, n = ndimage.label(m)
    best = []
    for i in range(1, n + 1):
        sel = lab == i
        if sel.sum() < 10:
            continue
        best.append((float(score[sel].mean()), sel.sum(),
                     np.nonzero(sel)[1].mean() / a.shape[1] * 100,
                     np.nonzero(sel)[0].mean() / a.shape[0] * 100))
    best.sort(reverse=True)
    top = best[:3]
    if not top:
        return 50.0, 50.0
    w = sum(s * z for s, z, _, _ in top) or 1
    return (sum(s * z * x for s, z, x, _ in top) / w,
            sum(s * z * y for s, z, _, y in top) / w)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    meta = []
    for slug, path, title in SRC:
        im = Image.open(path).convert("RGB")
        im.thumbnail((1400, 1400), Image.LANCZOS)
        clean = Image.new("RGB", im.size)
        clean.putdata(list(im.getdata()))            # drops EXIF
        clean.save(f"{OUT}/{slug}.webp", "WEBP", quality=80, method=6)
        clean.save(f"{OUT}/{slug}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
        x, y = wing(path)
        meta.append({"slug": slug, "title": title, "w": clean.size[0], "h": clean.size[1],
                     "x": round(min(85, max(15, x)), 1), "y": round(min(85, max(15, y)), 1)})
        print(f"  {slug:14s} wing at {meta[-1]['x']:5.1f}% {meta[-1]['y']:5.1f}%")
    json.dump(meta, open("/tmp/gallery.json", "w"), indent=1)
