#!/usr/bin/env python3
"""Stills for the library from the podcast's own YouTube thumbnails.

    python3 tools/library_stills.py --raw DIR [--sheet PATH]

DIR holds <video_id>.jpg (the maxresdefault thumbnail, 1280x720). For every episode in episode-meta.json with a
video the biggest face is found (OpenCV's Haar cascade); the still is a square around the head and shoulders, and
a 4:3 crop around the head, a little wider than the square, for backgrounds. No face found: the right half, where the guest
usually stands on these thumbnails. tools/data/library-stills.json records what was done and takes overrides:
  {"slug": {"box": [x, y, side]}} sets the square by hand (thumbnail pixels); the 4:3 crop follows it.
Written: prototypes/v4/img/library/stills/s/<slug>.webp (640 square) and w/<slug>.webp (960x720).
The grade is the same for all: colour eased, a touch darker and warmer, so 85 thumbnails read as one set."""
import argparse, json, os
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(ROOT, "episode-meta.json")
REC = os.path.join(ROOT, "tools", "data", "library-stills.json")
OUT = os.path.join(ROOT, "prototypes", "v4", "img", "library", "stills")


def grade(pil):
    pil = ImageEnhance.Color(pil).enhance(0.82); pil = ImageEnhance.Brightness(pil).enhance(0.92)
    r, g, b = pil.split(); r = r.point(lambda p: min(255, int(p * 1.04))); b = b.point(lambda p: int(p * 0.95))
    return Image.merge("RGB", (r, g, b))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--raw", required=True); ap.add_argument("--sheet", default="")
    a = ap.parse_args()
    rec = json.load(open(REC)) if os.path.exists(REC) else {}
    cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eps = [e for e in json.load(open(META)) if e.get("video_id")]
    os.makedirs(os.path.join(OUT, "s"), exist_ok=True); os.makedirs(os.path.join(OUT, "w"), exist_ok=True)
    tiles = []
    for e in eps:
        p = os.path.join(a.raw, e["video_id"] + ".jpg")
        if not os.path.exists(p): print("missing", e["slug"]); continue
        img = cv2.imread(p); H, W = img.shape[:2]
        r = rec.get(e["slug"], {})
        if r.get("box"):
            x0, y0, s = r["box"]; how = "by hand"
        else:
            g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); faces = list(cas.detectMultiScale(g, 1.08, 5, minSize=(70, 70)))
            if faces:
                x, y, w, h = max(faces, key=lambda f: f[2] * f[3]); cx, cy = x + w / 2, y + h * 0.62; s = int(min(W, H, w * 1.8))
                x0 = int(np.clip(cx - s / 2, 0, W - s)); y0 = int(np.clip(cy - s / 2, 0, H - s)); how = "face"
            else:
                s = H; x0, y0 = W - H, 0; how = "no face: right side"
        rec[e["slug"]] = dict(r, video_id=e["video_id"], how=how, used=[int(x0), int(y0), int(s)])
        sq = Image.fromarray(cv2.cvtColor(img[y0:y0 + s, x0:x0 + s], cv2.COLOR_BGR2RGB)).resize((640, 640), Image.LANCZOS)
        grade(sq).save(os.path.join(OUT, "s", e["slug"] + ".webp"), quality=84)
        wh = int(min(H, s * 1.15)); ww = int(wh * 4 / 3); cx = x0 + s / 2; cy = y0 + s / 2
        wx0 = int(np.clip(cx - ww / 2, 0, W - ww)); wy0 = int(np.clip(cy - wh / 2, 0, H - wh))
        wd = Image.fromarray(cv2.cvtColor(img[wy0:wy0 + wh, wx0:wx0 + ww], cv2.COLOR_BGR2RGB)).resize((960, 720), Image.LANCZOS)
        grade(wd).save(os.path.join(OUT, "w", e["slug"] + ".webp"), quality=82)
        tiles.append((e["slug"], e.get("guest", ""), how, sq.resize((150, 150))))
    json.dump(rec, open(REC, "w"), indent=1, sort_keys=True)
    if a.sheet:
        cols = 9; rows = (len(tiles) + cols - 1) // cols; S = Image.new("RGB", (cols * 160 + 10, rows * 190 + 10), (20, 21, 25)); d = ImageDraw.Draw(S)
        for i, (slug, guest, how, t) in enumerate(tiles):
            x = 10 + (i % cols) * 160; y = 10 + (i // cols) * 190; S.paste(t, (x, y))
            d.text((x, y + 153), (guest or slug)[:22], fill=(246, 244, 244)); d.text((x, y + 166), ("%d " % (i + 1)) + how[:20], fill=(255, 117, 23) if "no face" in how else (154, 154, 163))
        S.save(a.sheet); print("sheet", S.size)
    print("stills", len(tiles), "no face:", sum(1 for t in tiles if "no face" in t[2]))


if __name__ == "__main__":
    main()
