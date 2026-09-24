#!/usr/bin/env python3
"""Web versions of the India page photographs.

The originals (12 to 23 MB each, some AVIF) stay out of the repo. Point this at
the folder that holds them and it writes the page's photos into
assets/destinations/india/, each as a JPEG and a WebP sibling:

  hero/     full-screen slides. Native aspect, never upscaled, because the
            slides are cropped by the viewport. 2400 px wide where the file
            fits under the limit at a decent quality; busier photos (snow,
            terraced fields) step down through 2200, 2000, 1800 and 1600 px,
            the width Kenya uses, instead of
            dropping below quality 68.
  gallery/  the gallery and the overview sequence. 3:2, 1400 x 933, cropped
            around the focus point given below.
  india-og.jpg  the 1200 x 630 social share image.

Every file is kept under 400 KB (the audit's limit) by stepping the quality
down from 82, and all camera metadata is stripped.

Run: python3 tools/build_india_photos.py /path/to/originals
Needs: Pillow 11.2+ (AVIF support)
"""
import os
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets/destinations/india")
LIMIT = 400 * 1024 - 8 * 1024          # a little headroom under the audit's 400 KB

# (source file, output name, kind, focus x, focus y). Focus is where a crop
# centres, 0 to 1 across and down; it only matters when the aspect changes.
PHOTOS = [
    ("Bir_1.jpg",               "snowline",        "hero",    0.5, 0.5),
    ("bir_takeoff__1_.jpg",     "billing-launch",  "hero",    0.5, 0.5),
    ("Bir_landing.jpg",         "bir-landing",     "hero",    0.5, 0.5),
    ("bir_valley__1_.jpg",      "dhauladhar",      "hero",    0.5, 0.5),
    ("Bir_Hero.jpg",            "back-ranges",     "hero",    0.5, 0.5),
    ("Bir_Takeoff.jpg",         "launch-day",      "gallery", 0.5, 0.5),
    ("bir_ridge__1_.jpg",       "front-range",     "gallery", 0.4, 0.5),
    ("bir_sunsset__2_.jpg",     "last-light-pair", "gallery", 0.5, 0.45),
    ("bir_2.jpg",               "red-wing",        "gallery", 0.45, 0.5),
    ("Bir_4.jpg",               "over-the-peaks",  "gallery", 0.4, 0.55),
    ("bir_ridge__2_.jpg",       "ridge-cumulus",   "gallery", 0.5, 0.5),
    ("bir_vilage_view__2_.jpg", "sky-of-wings",    "gallery", 0.55, 0.4),
    ("bir_landing_2.jpg",       "landing-field",   "gallery", 0.6, 0.5),
    ("bir_hike_n_fly__3_.jpg",  "hike-and-fly",    "gallery", 0.45, 0.55),
    ("bir_valley__4_.jpg",      "kangra-valley",   "gallery", 0.5, 0.5),
    ("bir_monastry.png",        "monastery",       "gallery", 0.45, 0.5),
    ("Bir_meadows.avif",        "meadows",         "gallery", 0.5, 0.5),
    ("bir_valley__3_.jpg",      "valley-river",    "gallery", 0.5, 0.5),
    ("bir_clouds.jpg",          "cloud-range",     "gallery", 0.62, 0.5),
    ("bir_sunsset__1_.jpg",     "last-light",      "gallery", 0.5, 0.45),
]
OG = ("Bir_1.jpg", 0.55, 0.45)


def crop_to(im, ratio, fx, fy):
    w, h = im.size
    if w / h > ratio:                           # too wide: trim the sides
        nw = round(h * ratio)
        x = min(max(round(fx * w - nw / 2), 0), w - nw)
        return im.crop((x, 0, x + nw, h))
    nh = round(w / ratio)                       # too tall: trim top and bottom
    y = min(max(round(fy * h - nh / 2), 0), h - nh)
    return im.crop((0, y, w, y + nh))


def save_under(im, path, fmt, floor=60):
    for q in range(82, floor - 1, -3):
        kw = dict(quality=q, optimize=True, progressive=True) if fmt == "JPEG" else dict(quality=q, method=6)
        im.save(path, fmt, **kw)
        if os.path.getsize(path) <= LIMIT:
            return q, os.path.getsize(path) // 1024, True
    return q, os.path.getsize(path) // 1024, False


def save_hero(im, base):
    """Largest width that fits the limit at quality 68 or better, in both formats."""
    for width in (2400, 2200, 2000, 1800, 1600):
        w = min(width, im.width)
        cur = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        qj, kj, okj = save_under(cur, base + ".jpg", "JPEG", floor=68)
        qw, kw, okw = save_under(cur, base + ".webp", "WEBP", floor=68)
        if (okj and okw) or w == im.width or width == 1600:
            return cur, (qj, kj, qw, kw)


def load(src_dir, name):
    im = Image.open(os.path.join(src_dir, name))
    im = ImageOps.exif_transpose(im).convert("RGB")
    im.info.pop("exif", None)
    return im


def build(src_dir):
    rows = []
    for src, name, kind, fx, fy in PHOTOS:
        im = load(src_dir, src)
        os.makedirs(os.path.join(OUT, kind), exist_ok=True)
        base = os.path.join(OUT, kind, name)
        if kind == "hero":
            im, (qj, kj, qw, kw) = save_hero(im, base)
        else:
            im = crop_to(im, 3 / 2, fx, fy)
            im = im.resize((1400, 933), Image.LANCZOS) if im.width >= 1400 else im
            qj, kj, _ = save_under(im, base + ".jpg", "JPEG")
            qw, kw, _ = save_under(im, base + ".webp", "WEBP")
        rows.append((kind + "/" + name, im.width, im.height, kj, qj, kw, qw))
    src, fx, fy = OG
    im = crop_to(load(src_dir, src), 1200 / 630, fx, fy).resize((1200, 630), Image.LANCZOS)
    q, k, _ = save_under(im, os.path.join(OUT, "india-og.jpg"), "JPEG")
    rows.append(("india-og", 1200, 630, k, q, 0, 0))
    for r in rows:
        print("%-26s %4dx%-4d  jpg %3d KB q%d   webp %3d KB q%d" % r)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    build(sys.argv[1])
