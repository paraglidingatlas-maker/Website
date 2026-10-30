#!/usr/bin/env python3
"""
Prepare the data behind the Speed Record hero (prototypes/v4/record-attempt.html,
drawn by prototypes/v4/record-hero.js). Not part of the build: the outputs are
committed under prototypes/v4/img/record/hero/, and the page is edited directly.

    python3 tools/v4_record_hero_prep.py terrain --cache DIR
    python3 tools/v4_record_hero_prep.py path    --cache DIR --igc FLIGHT.igc
    python3 tools/v4_record_hero_prep.py depth   --horizon HZ.npy

terrain  The ground is heights only: open terrain data (AWS Terrain Tiles,
         Mapzen Terrarium, from SRTM and other open sources), fetched into DIR
         when missing. No colour imagery is fetched or shipped. Near the course,
         z14 tiles are joined into 3 x 3 squares (7.34 km a side) and written as
         t/hm<i>_<j>.webp at 384 px (desktop) and t/p/hm<i>_<j>.webp at 192 px
         (phone); the whole valley, from z12, as t/far-h.webp and t/p/far-h.webp.
         Heights are packed lossless in red and green: (R * 256 + G) / 16 + 500 m.
         Prints the square list and the far box that record-hero.js carries as
         CHUNKS and FAR.
path     The line of flight from the IGC log (6 Feb 2025): the fixes only (no
         header, so no name leaves the log), north into Turn 2 from 21 km before
         it and back to land, smoothed (tight round the turn, wide on the legs),
         resampled every 30 m, held 40 m over the crest it follows, with local
         time (EAT) and ground speed. Writes path.json: step, turn (its sample),
         x, y, z (metres, the squares' frame), t (seconds of the day), v (km/h).
depth    The photograph's depth for the parallax: 0 for the sky, rising to 1 at
         its foot from the horizon line (a 1920-value .npy traced from the photo),
         eased off over the hazy valley on the right; written as depth.png,
         480 x 270, softened. The photograph (plate.jpg, the glider taken out) and
         the wing cut from it (wing.webp) are committed as prepared by hand.

Needs numpy and Pillow; terrain needs the network unless DIR already holds the
tiles.
"""
import argparse, concurrent.futures as cf, json, math, os, sys, urllib.request
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "prototypes", "v4", "img", "record", "hero")
Z, CH, BASE = 14, 3, 500.0
MPP = 40075016.686 / 2 ** Z / 256
TILE = "https://elevation-tiles-prod.s3.amazonaws.com/terrarium/%d/%d/%d.png"
FAR_BOX = (35.25, 1.40, 35.95, 0.15)          # lon, lat of the valley's NW and SE corners


def txy(lon, lat, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n


def gpx(lon, lat):
    n = 2 ** Z * 256
    lat = np.radians(lat)
    return (np.asarray(lon) + 180) / 360 * n, (1 - np.log(np.tan(lat) + 1 / np.cos(lat)) / np.pi) / 2 * n


def fetch(cache, jobs):
    def get(j):
        z, x, y = j
        p = os.path.join(cache, "h%d_%d_%d.png" % (z, x, y))
        if os.path.exists(p) and os.path.getsize(p) > 0:
            return 0
        for _ in range(4):
            try:
                r = urllib.request.urlopen(urllib.request.Request(TILE % (z, x, y), headers={"User-Agent": "paraglidingatlas-build"}), timeout=40)
                open(p, "wb").write(r.read())
                return 0
            except Exception as e:      # noqa: BLE001  (retried, then reported)
                err = e
        print("FAIL", TILE % (z, x, y), err)
        return 1
    with cf.ThreadPoolExecutor(12) as ex:
        if sum(ex.map(get, sorted(jobs))):
            sys.exit("some tiles could not be fetched")


def tile_h(cache, z, x, y):
    a = np.asarray(Image.open(os.path.join(cache, "h%d_%d_%d.png" % (z, x, y))).convert("RGB")).astype(np.float64)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


def enc(A, path):
    v = np.clip(np.round((A - BASE) * 16), 0, 65535).astype(np.uint32)
    im = np.zeros(A.shape + (3,), np.uint8)
    im[..., 0] = v >> 8
    im[..., 1] = v & 255
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(im).save(path, lossless=True, quality=100, method=1)


def down(A, k):
    return A.reshape(A.shape[0] // k, k, A.shape[1] // k, k).mean((1, 3))


def read_igc(path):
    """The B records only: time, latitude, longitude, GPS altitude."""
    rows = []
    for l in open(path, errors="ignore"):
        if l.startswith("B") and len(l) > 35 and l[24] == "A":
            t = int(l[1:3]) * 3600 + int(l[3:5]) * 60 + int(l[5:7])
            la = (int(l[7:9]) + int(l[9:14]) / 60000) * (-1 if l[14] == "S" else 1)
            lo = (int(l[15:18]) + int(l[18:23]) / 60000) * (-1 if l[23] == "W" else 1)
            rows.append((t, la, lo, int(l[30:35])))
    return np.array(rows, float)


def course_squares(la, lo):
    px, py = gpx(lo, la)
    cx0, cx1 = int(px.min() // 256 // CH) - 3, int(px.max() // 256 // CH) + 3
    cy0, cy1 = int(py.min() // 256 // CH) - 3, int(py.max() // 256 // CH) + 3
    out = []
    for cy in range(cy0, cy1 + 1):
        for cx in range(cx0, cx1 + 1):
            x0, y0 = cx * CH * 256, cy * CH * 256
            dx = np.maximum(0, np.maximum(x0 - px, px - x0 - CH * 256))
            dy = np.maximum(0, np.maximum(y0 - py, py - y0 - CH * 256))
            if np.hypot(dx, dy).min() * MPP <= 6000:
                out.append((cx, cy))
    return out


def cmd_terrain(a):
    os.makedirs(a.cache, exist_ok=True)
    P = read_igc(a.igc)[::20]
    sq = course_squares(P[:, 1], P[:, 2])
    fx0, fy0 = txy(FAR_BOX[0], FAR_BOX[1], 12)
    fx1, fy1 = txy(FAR_BOX[2], FAR_BOX[3], 12)
    far = (int(fx0), int(fy0), int(fx1), int(fy1))
    jobs = {(14, cx * CH + i, cy * CH + j) for cx, cy in sq for i in range(CH) for j in range(CH)}
    jobs |= {(12, x, y) for x in range(far[0], far[2] + 1) for y in range(far[1], far[3] + 1)}
    fetch(a.cache, jobs)
    cx0, cy0 = min(c[0] for c in sq), min(c[1] for c in sq)
    for cx, cy in sq:
        H = np.zeros((CH * 256, CH * 256))
        for i in range(CH):
            for j in range(CH):
                H[j * 256:(j + 1) * 256, i * 256:(i + 1) * 256] = tile_h(a.cache, 14, cx * CH + i, cy * CH + j)
        k = "%d_%d" % (cx - cx0, cy - cy0)
        enc(down(H, 2), os.path.join(OUT, "t", "hm%s.webp" % k))
        enc(down(H, 4), os.path.join(OUT, "t", "p", "hm%s.webp" % k))
    xs, ys = range(far[0], far[2] + 1), range(far[1], far[3] + 1)
    H = np.zeros((len(ys) * 256, len(xs) * 256))
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            H[j * 256:(j + 1) * 256, i * 256:(i + 1) * 256] = tile_h(a.cache, 12, x, y)
    enc(down(H, 2), os.path.join(OUT, "t", "far-h.webp"))
    enc(down(H, 4), os.path.join(OUT, "t", "p", "far-h.webp"))
    m12 = 40075016.686 / 2 ** 12 / 256
    ox, oy = cx0 * CH * 256, cy0 * CH * 256           # the squares' frame, z14 pixels
    box = {"x0": round((far[0] * 1024 - ox) * MPP, 2), "z0": round((far[1] * 1024 - oy) * MPP, 2),
           "w": round(len(xs) * 256 * m12, 2), "h": round(len(ys) * 256 * m12, 2)}
    print("CHUNKS =", json.dumps([[cx - cx0, cy - cy0] for cx, cy in sq], separators=(",", ":")))
    print("FAR =", json.dumps(box, separators=(",", ":")))
    json.dump({"cx0": cx0, "cy0": cy0}, open(os.path.join(a.cache, "frame.json"), "w"))


class Ground:
    """Heights from the cached z14 tiles, bilinear, in global z14 pixels."""
    def __init__(self, cache):
        self.cache, self.t = cache, {}

    def tile(self, x, y):
        if (x, y) not in self.t:
            p = os.path.join(self.cache, "h14_%d_%d.png" % (x, y))
            self.t[(x, y)] = tile_h(self.cache, 14, x, y) if os.path.exists(p) else None
        return self.t[(x, y)]

    def __call__(self, px, py):
        px, py = np.atleast_1d(np.asarray(px, float)), np.atleast_1d(np.asarray(py, float))
        x0, y0 = np.floor(px - .5), np.floor(py - .5)
        fx, fy = px - .5 - x0, py - .5 - y0

        def g(X, Y):
            r = np.full(X.shape, np.nan)
            tx, ty = (X // 256).astype(int), (Y // 256).astype(int)
            for u, v in set(zip(tx.ravel(), ty.ravel())):
                T = self.tile(u, v)
                if T is not None:
                    m = (tx == u) & (ty == v)
                    r[m] = T[(Y[m] - v * 256).astype(int), (X[m] - u * 256).astype(int)]
            return r
        return g(x0, y0) * (1 - fx) * (1 - fy) + g(x0 + 1, y0) * fx * (1 - fy) + g(x0, y0 + 1) * (1 - fx) * fy + g(x0 + 1, y0 + 1) * fx * fy


def gs(a, sig, mode="edge"):
    k = np.arange(-4 * sig, 4 * sig + 1)
    w = np.exp(-.5 * (k / sig) ** 2)
    return np.convolve(np.pad(a, 4 * sig, mode=mode), w / w.sum(), "valid")


def cmd_path(a):
    fr = json.load(open(os.path.join(a.cache, "frame.json")))
    OXp, OYp = fr["cx0"] * CH * 256, fr["cy0"] * CH * 256
    H = Ground(a.cache)
    P = read_igc(a.igc)
    t, la, lo = P[:, 0], P[:, 1], P[:, 2]
    R = 6371008.8
    a1, o1, a2, o2 = map(np.radians, (la[:-1], lo[:-1], la[1:], lo[1:]))
    cs = np.r_[0, np.cumsum(2 * R * np.arcsin(np.sqrt(np.sin((a2 - a1) / 2) ** 2 + np.cos(a1) * np.cos(a2) * np.sin((o2 - o1) / 2) ** 2)))]
    v = np.array([(cs[min(len(t) - 1, i + 20)] - cs[max(0, i - 20)]) / max(t[min(len(t) - 1, i + 20)] - t[max(0, i - 20)], 1) * 3.6 for i in range(len(t))])
    iN = int(np.argmax(la))                       # Turn 2, the northern turn
    px, py = gpx(lo, la)
    sx, sy = gs(px, 25), gs(py, 25)               # the plan line, by time
    X, Zz = (sx - OXp) * MPP, (sy - OYp) * MPP
    sl = np.r_[0, np.cumsum(np.hypot(np.diff(X), np.diff(Zz)))]
    s = np.arange(0, sl[-1], 30.0)
    idx = np.interp(s, sl, np.arange(len(sl)))
    x, z = np.interp(idx, np.arange(len(X)), X), np.interp(idx, np.arange(len(Zz)), Zz)
    xr, zr = x.copy(), z.copy()
    ts = np.interp(idx, np.arange(len(t)), t) + 3 * 3600            # EAT
    vs = np.interp(idx, np.arange(len(v)), v)
    kN = int(np.argmin(np.abs(ts - (t[iN] + 3 * 3600))))
    lo_, hi_ = kN - 700, len(x) - 1                                  # 21 km into Turn 2, then back to land
    x, z, ts, vs, xr, zr = (q[lo_:hi_ + 1] for q in (x, z, ts, vs, xr, zr))
    kt = kN - lo_
    d = np.abs(np.arange(len(x)) - kt)
    sig = 4 + 36 * (1 - np.exp(-.5 * (d / 60.) ** 2))                # tight round the turn, wide on the legs
    ii = np.arange(len(x))

    def gsv(arr):
        out = np.empty_like(arr)
        for i in range(len(arr)):
            w = np.exp(-.5 * ((ii - i) / sig[i]) ** 2)
            out[i] = (w * arr).sum() / w.sum()
        return out
    xs, zs = gsv(x), gsv(z)
    sl = np.r_[0, np.cumsum(np.hypot(np.diff(xs), np.diff(zs)))]
    S = np.arange(0, sl[-1], 30.0)
    j = np.interp(S, sl, np.arange(len(sl)))
    X, Zz = np.interp(j, ii, xs), np.interp(j, ii, zs)
    T, V = np.interp(j, ii, ts), np.interp(j, ii, vs)
    Xr, Zr = np.interp(j, ii, xr), np.interp(j, ii, zr)
    KT = int(np.argmin(np.abs(j - kt)))
    gp = lambda X_, Z_: (X_ / MPP + OXp, Z_ / MPP + OYp)
    best = np.fmax(H(*gp(X, Zz)), H(*gp(Xr, Zr)))                    # the crest he follows
    for r in (60, 120, 200):
        for ang in np.linspace(0, 2 * np.pi, 16, endpoint=False):
            best = np.fmax(best, H(*gp(Xr + r * np.cos(ang), Zr + r * np.sin(ang))))
    alt = gs(best, 40, "reflect") + 40
    ring = ((0, 0), (60, 0), (-60, 0), (0, 60), (0, -60))
    for _ in range(5):
        g = np.fmax.reduce([H(*gp(X + ox, Zz + oz)) for ox, oz in ring])
        alt = alt + gs(np.maximum(0, g + 30 - alt), 16, "reflect") * 1.3
    alt = gs(alt, 10, "reflect")
    for _ in range(4):
        g = np.fmax.reduce([H(*gp(X + ox, Zz + oz)) for ox, oz in ring])
        alt = alt + gs(np.maximum(0, g + 28 - alt), 8, "reflect") * 1.4
    out = {"step": 30, "turn": KT, "x": [round(q, 1) for q in X], "y": [round(q, 1) for q in alt],
           "z": [round(q, 1) for q in Zz], "t": [int(q) for q in T], "v": [round(q, 1) for q in V]}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "path.json"), "w"), separators=(",", ":"))
    print("samples", len(S), "turn at", KT)


def cmd_depth(a):
    hz = np.load(a.horizon).astype(np.float32)
    W, Hh = 1920, 1080
    k = np.exp(-.5 * (np.arange(-48, 49) / 12.) ** 2)
    hz = np.convolve(np.pad(hz, 48, mode="edge"), k / k.sum(), "valid")
    yy, xx = np.mgrid[0:Hh, 0:W].astype(np.float32)
    t = np.clip((yy - hz[None, :]) / (Hh - hz[None, :]), 0, 1)
    z = t ** 1.15
    v = np.clip((xx - 1250) / 550, 0, 1)
    v = v * v * (3 - 2 * v)
    z = z * (1 - .45 * v * (1 - t ** 2))           # the valley floor on the right lies far below, in haze
    im = Image.fromarray(np.clip(z * 255 + .5, 0, 255).astype(np.uint8)).resize((480, 270), Image.BOX)
    from PIL import ImageFilter
    im.filter(ImageFilter.GaussianBlur(3)).save(os.path.join(OUT, "depth.png"), optimize=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("terrain"); p.add_argument("--cache", required=True); p.add_argument("--igc", required=True)
    p = sub.add_parser("path"); p.add_argument("--cache", required=True); p.add_argument("--igc", required=True)
    p = sub.add_parser("depth"); p.add_argument("--horizon", required=True)
    a = ap.parse_args()
    {"terrain": cmd_terrain, "path": cmd_path, "depth": cmd_depth}[a.cmd](a)


if __name__ == "__main__":
    main()
