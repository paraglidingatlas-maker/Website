#!/usr/bin/env python3
"""
Phone sizes of the trips' hero photographs and of the two hero clips (the
usability pass, item 6; docs/ux-report.md).

On a phone held upright a landscape hero shows only its middle third, scaled
up to fill a tall screen, yet the whole 1600 to 2400 px photograph was sent.
The phone versions are the same photographs cut to what an upright screen
shows (2:3, at the page's own object-position, so the same part is seen) and
no taller than 1400 px; the clips likewise (the 1080p file cut to 2:3, 480 x
720). Nothing is redrawn or retouched. The live files in assets/ are read,
never written.

    python3 tools/v4_phone_media.py              # write what is missing
    python3 tools/v4_phone_media.py --force      # write everything again
    python3 tools/v4_phone_media.py --out DIR    # write elsewhere (a dry run)

Also the home page's four expedition photographs (home-<name>-p), and the
stills under the knowledge base's film strips (film-<name>-p.webp, the usability
pass's weight check: the strip now sits within a phone's first screens, where the
browser fetches a lazy picture at once, and the 1600 px still was 87 to 309 KB).

Writes prototypes/v4/img/hero/<trip>-<name>-p.webp|jpg, film-<name>-p.webp, img/art/<episode>-s.webp,
img/clouds/cloud-<n>-s.webp and
prototypes/v4/img/clips/<name>-p-720.webm|mp4. Needs Pillow and ffmpeg
(libvpx-vp9, libx264).
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
ASPECT = 2 / 3           # width / height of the phone cut: covers any screen narrower than 2:3
MAX_H = 1400
CLIPS = {"bir": 50, "hero": 50}     # clip name -> its object-position x (%) on the page


def heroes(trip):
    """(name, jpg path, object-position x %) for each hero slide of a trip page, in order."""
    src = open(os.path.join(V4, "destinations", trip + ".html"), encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<div class="khero-slide[^"]*">\s*<picture>(.*?)</picture>', src, re.S):
        jpg = re.search(r'(?:data-v4-src|\bsrc)="([^"]+\.jpg)"', m.group(1)).group(1)
        x = re.search(r"object-position:\s*(\d+(?:\.\d+)?)%", m.group(1))
        out.append((os.path.basename(jpg)[:-4], os.path.normpath(os.path.join(V4, "destinations", jpg)), float(x.group(1)) if x else 50.0))
    return out


def flyby():
    """(name, jpg path, 50) for the home page's four expedition photographs."""
    src = open(os.path.join(V4, "index.html"), encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<div class="v2-fb-shot[^"]*"><picture>(.*?)</picture>', src, re.S):
        jpg = re.search(r'(?:data-v4-src|\bsrc)="([^"]+\.jpg)"', m.group(1)).group(1)
        out.append((os.path.basename(jpg)[:-4], os.path.normpath(os.path.join(V4, jpg)), 50.0))
    return out


def films():
    """(name, jpg path, 50) for each still under a knowledge base film strip (centred, as the page shows it)."""
    seen, out = set(), []
    kb = os.path.join(V4, "knowledge-base")
    for f in sorted(os.listdir(kb)):
        if not f.endswith(".html"):
            continue
        src = open(os.path.join(kb, f), encoding="utf-8").read()
        for m in re.finditer(r'<section class="v4-breather v4-film"[^>]*>\s*<div class="v4-br-media">.*?<img\b[^>]*\ssrc="([^"]+\.jpg)"', src, re.S):
            path = os.path.normpath(os.path.join(kb, m.group(1)))
            if path not in seen:
                seen.add(path)
                out.append((os.path.basename(path)[:-4], path, 50.0))
    return out


def film_stills(out, force):
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    for name, path, x in films():
        stem = os.path.join(out, "film-%s-p" % name)
        if not force and os.path.exists(stem + ".webp"):
            continue
        im = Image.open(path).convert("RGB")
        im = im.crop(cut(im, x))
        im.save(stem + ".webp", "WEBP", quality=74, method=6)
        print("phone still film-%s: %dx%d, %d KB webp" % (name, im.width, im.height, os.path.getsize(stem + ".webp") // 1024))


STILLS = (("about", "img/alps-11-still.jpg", 62.0, 0.8),)    # (name, v4 path, object-position x %, the phone box's width / height)


def page_stills(out, force):
    """The About opening's still: on a phone it fills a 342 x 428 box (cover, at 62%), so it gets that window of
    the 1920 x 1080 file (864 x 1080), not the whole of it (the weight check at the end of the pass)."""
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    for name, rel, x, aspect in STILLS:
        stem = os.path.join(out, "%s-%s-p" % (name, os.path.basename(rel)[:-4]))
        if not force and os.path.exists(stem + ".webp"):
            continue
        im = Image.open(os.path.join(V4, rel)).convert("RGB")
        w, h = im.size
        cw = min(w, round(h * aspect))
        left = round((x / 100.0) * (w - cw))
        im = im.crop((left, 0, left + cw, h))
        im.save(stem + ".webp", "WEBP", quality=74, method=6)
        print("phone still %s: %dx%d, %d KB webp" % (os.path.basename(stem), im.width, im.height, os.path.getsize(stem + ".webp") // 1024))


def art_thumbs(out, force):
    """The episodes' own artwork (assets/podcast/artwork, 1280 x 720) at 400 px wide, for the knowledge base's
    conversation tiles on a phone, which show it 120 px wide (the weight check at the end of the pass)."""
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    art = os.path.join(ROOT, "assets", "podcast", "artwork")
    for f in sorted(os.listdir(art)):
        if not f.endswith(".webp"):
            continue
        dst = os.path.join(out, f[:-5] + "-s.webp")
        if not force and os.path.exists(dst):
            continue
        im = Image.open(os.path.join(art, f)).convert("RGB")
        im = im.resize((400, round(im.height * 400 / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=76, method=6)
        print("tile art %s: %dx%d, %d KB" % (os.path.basename(dst), im.width, im.height, os.path.getsize(dst) // 1024))


def cloud_copies(out, force):
    """The Kenya page's own cloud layers (assets/destinations/kenya/clouds, 2400 px wide, transparent) at 1000 px
    for a phone, for the climb into the footage bands (src/v4-ux-ascent.js): the same clouds at 1000 px."""
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    src = os.path.join(ROOT, "assets", "destinations", "kenya", "clouds")
    for f in sorted(os.listdir(src)):
        if not f.endswith(".webp"):
            continue
        dst = os.path.join(out, f[:-5] + "-s.webp")
        if not force and os.path.exists(dst):
            continue
        im = Image.open(os.path.join(src, f)).convert("RGBA")
        im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=60, method=6, alpha_quality=60)     # soft edges: 21 to 33 KB a layer
        print("cloud %s: %dx%d, %d KB" % (os.path.basename(dst), im.width, im.height, os.path.getsize(dst) // 1024))


def cut(im, x):
    """The 2:3 window an upright screen shows at object-position x%, as a box in the image."""
    w, h = im.size
    cw = min(w, round(h * ASPECT))
    left = round((x / 100.0) * (w - cw))
    return (left, 0, left + cw, h)


def photos(out, force):
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    for trip in ("india", "kenya", "home"):
        for name, path, x in (flyby() if trip == "home" else heroes(trip)):
            stem = os.path.join(out, "%s-%s-p" % (trip, name))
            if not force and os.path.exists(stem + ".webp") and os.path.exists(stem + ".jpg"):
                continue
            im = Image.open(path).convert("RGB")
            im = im.crop(cut(im, x))
            if im.height > MAX_H:
                im = im.resize((round(im.width * MAX_H / im.height), MAX_H), Image.LANCZOS)
            im.save(stem + ".webp", "WEBP", quality=74, method=6)
            im.save(stem + ".jpg", "JPEG", quality=80, optimize=True, progressive=True)
            print("phone photo %s-%s: %dx%d, %d KB webp, %d KB jpg" % (trip, name, im.width, im.height,
                  os.path.getsize(stem + ".webp") // 1024, os.path.getsize(stem + ".jpg") // 1024))


def clips(out, force):
    os.makedirs(out, exist_ok=True)
    for name, x in CLIPS.items():
        src = os.path.join(ROOT, "assets", "video", name + "-1080.mp4")
        stem = os.path.join(out, name + "-p-720")
        # 2:3 out of 1920 x 1080 is 720 x 1080, placed at x%, then 480 x 720
        crop = "crop=720:1080:(in_w-720)*%.3f:0,scale=480:720:flags=lanczos" % (x / 100.0)
        log = os.path.join("/tmp", "v4pm-" + name)
        if force or not os.path.exists(stem + ".webm"):
            # the same bits a pixel as the 720p files (about 650 kbit/s for 1280 x 720): 250 kbit/s, two passes
            for ps, dst in (("1", os.devnull), ("2", stem + ".webm")):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", crop, "-an", "-c:v", "libvpx-vp9", "-b:v", "250k",
                                "-row-mt", "1", "-deadline", "good", "-cpu-used", "2", "-pass", ps, "-passlogfile", log,
                                "-f", "webm", dst], check=True)
        if force or not os.path.exists(stem + ".mp4"):
            for ps, dst in (("1", os.devnull), ("2", stem + ".mp4")):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", crop, "-an", "-c:v", "libx264", "-preset", "slow",
                                "-b:v", "300k", "-pass", ps, "-passlogfile", log, "-pix_fmt", "yuv420p", "-profile:v", "high",
                                "-movflags", "+faststart", "-f", "mp4", dst], check=True)
        print("phone clip %s: %d KB webm, %d KB mp4" % (name, os.path.getsize(stem + ".webm") // 1024, os.path.getsize(stem + ".mp4") // 1024))


def main(args):
    force = "--force" in args
    out = args[args.index("--out") + 1] if "--out" in args else None
    photos(os.path.join(out, "hero") if out else os.path.join(V4, "img", "hero"), force)
    film_stills(os.path.join(out, "hero") if out else os.path.join(V4, "img", "hero"), force)
    page_stills(os.path.join(out, "hero") if out else os.path.join(V4, "img", "hero"), force)
    art_thumbs(os.path.join(out, "art") if out else os.path.join(V4, "img", "art"), force)
    cloud_copies(os.path.join(out, "clouds") if out else os.path.join(V4, "img", "clouds"), force)
    clips(os.path.join(out, "clips") if out else os.path.join(V4, "img", "clips"), force)


if __name__ == "__main__":
    main(sys.argv[1:])
