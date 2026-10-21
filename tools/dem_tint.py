#!/usr/bin/env python3
"""Colour for a height grid, in the site's tones, and the four textures the live page loads.

    python3 tools/dem_tint.py --dem DIR --out OUTDIR --name journey --palette kenya [--water] [--k2 2 --k1 4]

Reads DIR/dem.bin and DIR/dem.json (from tools/dem_fetch.py). Writes OUTDIR/h-<name>-2k.png
(heights as R*256+G metres, rows north first; the page flips them), OUTDIR/c-<name>-2k.jpg
and the same at 1k for phones. --k2 and --k1 are the downsample factors of the 2k and 1k
textures from the grid (India used 2 and 4). --water paints perfectly flat ground of
some size as water: on these open tiles lakes are filled flat, plains are not.

Palettes are hypsometric stops (metres -> rgb) in the family of the site's dark pages,
with slope rules: rock shows through on steep high faces, snow stays on gentle ground
above the snow line where a palette has one."""
import argparse, json, os
import numpy as np
from PIL import Image

PALETTES = {
    # the Dhauladhar: valley greens, grey rock, snow above 4,100 m
    "india": dict(stops=[(450, (70, 74, 64)), (1200, (62, 70, 58)), (2000, (70, 70, 62)), (2800, (104, 98, 90)), (3500, (140, 134, 128)),
                         (4100, (196, 196, 198)), (4800, (236, 238, 240)), (6200, (248, 249, 250))], rock_above=4300, snow=None),
    # the Rift: ochre floors, dry savanna, green highlands, dark forest, grey rock; Mount Kenya's top the only white
    "kenya": dict(stops=[(300, (132, 98, 64)), (800, (122, 98, 62)), (1200, (106, 94, 58)), (1600, (84, 88, 54)), (2000, (62, 80, 50)),
                         (2500, (50, 70, 46)), (3000, (76, 82, 70)), (3800, (112, 110, 104)), (4600, (150, 148, 146)), (5200, (226, 228, 230))],
                  rock_above=3600, snow=None),
}
WATER = (26, 36, 48)


def blur3(a):
    k = np.array([1, 2, 1], np.float32) / 4
    b = np.pad(a, 1, mode="edge")
    b = b[:, :-2] * k[0] + b[:, 1:-1] * k[1] + b[:, 2:] * k[2]
    return b[:-2] * k[0] + b[1:-1] * k[1] + b[2:] * k[2]


def tint(g, mpp, pal, water=False):
    gs = blur3(g); gy, gx = np.gradient(gs, mpp); slope = np.degrees(np.arctan(np.hypot(gx, gy)))
    stops = pal["stops"]; e = np.clip(g, stops[0][0], stops[-1][0]); col = np.zeros(g.shape + (3,), np.float32)
    col[...] = np.array(stops[0][1])
    for (e0, c0), (e1, c1) in zip(stops, stops[1:]):
        t = np.clip((e - e0) / (e1 - e0), 0, 1)[..., None]; m = ((e >= e0) & (e <= e1))[..., None]
        col = np.where(m, np.array(c0) * (1 - t) + np.array(c1) * t, col)
    # steep high faces show rock
    steep = (g > pal["rock_above"])[..., None] * np.clip((slope - 35) / 20, 0, 1)[..., None]
    col = col * (1 - steep) + np.array((96, 92, 88), np.float32) * steep
    # steep faces anywhere are a touch darker, so escarpments read
    col = col * (1 - 0.22 * np.clip((slope - 14) / 22, 0, 1))[..., None]
    if water:
        # perfectly flat ground of some size: the local range of heights is under half a metre across 5 cells
        from numpy.lib.stride_tricks import sliding_window_view
        p = np.pad(g, 2, mode="edge"); win = sliding_window_view(p, (5, 5))
        flat = (win.max(axis=(2, 3)) - win.min(axis=(2, 3))) < 0.5
        # drop specks: a cell stays water only if its 3x3 neighbourhood is all flat, twice
        for _ in range(2):
            q = np.pad(flat, 1, mode="edge"); flat = np.ones_like(flat)
            for dy in (0, 1, 2):
                for dx in (0, 1, 2): flat &= q[dy:dy + flat.shape[0], dx:dx + flat.shape[1]]
        col = np.where(flat[..., None], np.array(WATER, np.float32), col)
    return np.clip(col, 0, 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dem", required=True); ap.add_argument("--out", required=True); ap.add_argument("--name", required=True)
    ap.add_argument("--palette", default="kenya"); ap.add_argument("--water", action="store_true")
    ap.add_argument("--k2", type=int, default=2); ap.add_argument("--k1", type=int, default=4)
    a = ap.parse_args()
    m = json.load(open(os.path.join(a.dem, "dem.json"))); W, H = m["w"], m["h"]
    g = np.fromfile(os.path.join(a.dem, "dem.bin"), np.float32).reshape(H, W)
    col = Image.fromarray(tint(g, m["mpp"], PALETTES[a.palette], a.water))
    os.makedirs(a.out, exist_ok=True)
    for tag, k, q in (("2k", a.k2, 82), ("1k", a.k1, 78)):
        w, h = W // k, H // k
        gg = g[:h * k, :w * k].reshape(h, k, w, k).mean(axis=(1, 3)) if k > 1 else g
        hm = np.clip(np.rint(gg), 0, 65535).astype(np.int32)
        png = np.zeros((h, w, 3), np.uint8); png[..., 0] = hm >> 8; png[..., 1] = hm & 255
        Image.fromarray(png).save(os.path.join(a.out, "h-%s-%s.png" % (a.name, tag)), optimize=True)
        col.resize((w, h), Image.LANCZOS).save(os.path.join(a.out, "c-%s-%s.jpg" % (a.name, tag)), quality=q, optimize=True, progressive=True)
        print(a.name, tag, w, h)
    col.save(os.path.join(a.dem, "color.png"))


if __name__ == "__main__":
    main()
