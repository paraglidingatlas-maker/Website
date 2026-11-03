#!/usr/bin/env python3
"""The four product posters of the Media page (chat 17, 3 Nov 2026; owner: "DIY", their Canva "SRS TV" board as
the model: Pre-Race Show, Daily Highlights, Aftermovie, Race Behind The Race as tall posters).

Each poster is a 3:4 crop of the owner's own material: a still from the Piedrahita "Chosen Few" folder, or a frame
of their own YouTube video (YouTube's maxres1 frame of that video). Written as WebP at 600x800 and 900x1200 where
the source is large enough (video frames are 720 px tall, so they stay at 540x720).

    python3 tools/v4_media_posters.py PHOTOS_DIR OUT_DIR

PHOTOS_DIR holds the stills' 2400 px web copies (STEM-2400.webp); frames are fetched from i.ytimg.com.
"""
import io
import os
import sys
import urllib.request

from PIL import Image

# key: (source, horizontal centre of the crop 0..1)
POSTERS = {
    "pre-race-show": ("host", .5),                  # the podcast host cut-out (assets/podcast), on the podcast's warm dark
    "daily-highlights": ("SRS_5_T2_133-2", .5),
    "aftermovie": ("SRS_5_T3_63", .52),
    "race-behind-the-race": ("yt:BRAX1XMU390", .28),  # launch at the Super Final, from the Task 1 video
}


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def host():
    """the host cut-out on a warm dark ground, the podcast page's colours (bg #141519, orange #ff7517)"""
    W, H = 900, 1200
    from PIL import ImageDraw, ImageFilter
    bg = Image.new("RGB", (W, H), (20, 21, 25))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((W * .05, H * .12, W * 1.05, H * .78), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    bg = Image.composite(Image.new("RGB", (W, H), (150, 62, 14)), bg, glow.point(lambda v: v * .75))
    cut = Image.open(os.path.join(ROOT, "assets", "podcast", "host-aninder-soft.png")).convert("RGBA")
    cw = int(W * 1.08)
    cut = cut.resize((cw, round(cut.height * cw / cut.width)), Image.LANCZOS)
    bg.paste(cut, ((W - cw) // 2, H - cut.height + 40), cut)
    return bg


def load(src, photos):
    if src == "host":
        return host()
    if src.startswith("yt:"):
        with urllib.request.urlopen("https://i.ytimg.com/vi/%s/maxres1.jpg" % src[3:]) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    return Image.open(os.path.join(photos, src + "-2400.webp")).convert("RGB")


def crop34(im, cx):
    w, h = im.size
    if w / h > .75:
        nw = round(h * .75)
        x = min(max(0, round(cx * w - nw / 2)), w - nw)
        return im.crop((x, 0, x + nw, h))
    nh = round(w / .75)
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def main(photos, out):
    os.makedirs(out, exist_ok=True)
    for key, (src, cx) in POSTERS.items():
        im = crop34(load(src, photos), cx)
        for w in (600, 900):
            if im.width < w * .95 and w != 600:
                continue
            c = im.resize((w, round(w / .75)), Image.LANCZOS) if im.width >= w else im
            c.save(os.path.join(out, "poster-%s-%d.webp" % (key, w)), "WEBP", quality=82, method=6)
        print(key, im.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
