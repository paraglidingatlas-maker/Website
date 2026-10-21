#!/usr/bin/env python3
"""A height grid from Mapzen Terrarium tiles (AWS Terrain Tiles, open data) for any box.

    python3 tools/dem_fetch.py --bbox W S E N --zoom 13 --down 2 --out DIR [--tiles CACHE]

Writes DIR/dem.bin (float32 rows north first) and DIR/dem.json with the grid metadata
the page and the track pipeline share: w, h, metres per pixel at the box's middle
latitude, zoom, the first tile column and row, the downsample factor, min and max.
Grid pixel = (tile coordinate - first tile) * 256 / down. Tiles are cached by zoom so a
second run over a bigger box only fetches what is new; a cut-off download is retried."""
import argparse, io, json, math, os, sys, time, urllib.request
import numpy as np
from PIL import Image

URL = "https://elevation-tiles-prod.s3.amazonaws.com/terrarium/%d/%d/%d.png"


def tile(lon, lat, z):
    n = 2 ** z; x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def fetch(url, path):
    for attempt in range(5):
        try:
            data = urllib.request.urlopen(url, timeout=60).read()
            Image.open(io.BytesIO(data)).verify()
            open(path, "wb").write(data); return
        except Exception as e:
            if attempt == 4: raise
            time.sleep(2 * (attempt + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bbox", nargs=4, type=float, required=True, metavar=("W", "S", "E", "N"))
    ap.add_argument("--zoom", type=int, default=13)
    ap.add_argument("--down", type=int, default=2)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tiles", default=None, help="tile cache directory (default OUT/tiles)")
    a = ap.parse_args()
    W_, S_, E_, N_ = a.bbox; z = a.zoom
    x0, y1 = tile(W_, S_, z); x1, y0 = tile(E_, N_, z)
    tx0, tx1, ty0, ty1 = int(x0), int(x1), int(y0), int(y1)
    cache = a.tiles or os.path.join(a.out, "tiles"); os.makedirs(os.path.join(cache, str(z)), exist_ok=True); os.makedirs(a.out, exist_ok=True)
    Wpx, Hpx = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    grid = np.zeros((Hpx, Wpx), np.float32); n = 0
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            f = os.path.join(cache, str(z), "%d_%d.png" % (tx, ty))
            if not os.path.exists(f) or os.path.getsize(f) == 0:
                fetch(URL % (z, tx, ty), f); n += 1
            arr = np.asarray(Image.open(f).convert("RGB"), np.float32)
            grid[(ty - ty0) * 256:(ty - ty0 + 1) * 256, (tx - tx0) * 256:(tx - tx0 + 1) * 256] = arr[..., 0] * 256 + arr[..., 1] + arr[..., 2] / 256 - 32768
    k = a.down
    g = grid.reshape(Hpx // k, k, Wpx // k, k).mean(axis=(1, 3)).astype(np.float32) if k > 1 else grid
    g.tofile(os.path.join(a.out, "dem.bin"))
    lat_mid = (S_ + N_) / 2
    mpp = 156543.03 * math.cos(math.radians(lat_mid)) / 2 ** z * k
    meta = dict(w=int(g.shape[1]), h=int(g.shape[0]), mpp=mpp, z=z, down=k, tx0=tx0, ty0=ty0, tiles_w=tx1 - tx0 + 1, tiles_h=ty1 - ty0 + 1,
                bbox=[W_, S_, E_, N_], min=float(g.min()), max=float(g.max()))
    json.dump(meta, open(os.path.join(a.out, "dem.json"), "w"), indent=1)
    print("fetched %d new tiles; grid %dx%d at %.1f m/px; %.0f to %.0f m" % (n, meta["w"], meta["h"], mpp, meta["min"], meta["max"]))


if __name__ == "__main__":
    main()
