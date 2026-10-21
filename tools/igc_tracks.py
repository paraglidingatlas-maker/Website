#!/usr/bin/env python3
"""Tracklogs for the India flight (option E): IGC files in, tools/data/india-tracks.json out.

    python3 tools/igc_tracks.py NAME=path/to/file.igc [NAME=path ...] [--out tools/data/india-tracks.json] [--dem tools/data/kenya-dem.json]

Each track keeps: the name given on the command line, the date from the file, the
flight scored the way XContest scores it (tools/xc_score.py: the route type, whether
it closed, the scored distance, the points, the legs and the closing gap), the
average speed as that scored distance over the time in the air, the duration from
first to last fix in the air, the length of the track over the ground (the fixes
summed, km), the furthest the flight got from its first airborne fix, the highest GPS altitude, and the track simplified to a few hundred points in the
terrain grid's pixels (tools/data/india-dem.json). The line is drawn only where it
lies inside the terrain box: a flight that leaves the box comes back as several
segments, and the kilometres flown outside it are counted and named by side so
the page can say so. A file with fewer than half its fixes in the box is refused.
The pilot's name and the glider are kept in this file for the record and are not
put on the page. Nothing is estimated: every number is read or summed from the file."""
import json, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from xc_score import score as xc_score
DEM_PATH = sys.argv[sys.argv.index("--dem") + 1] if "--dem" in sys.argv else os.path.join(ROOT, "tools", "data", "india-dem.json")   # --dem for another site's grid
DEM = json.load(open(DEM_PATH))


def grid_px(lon, lat, meta):
    n = 2 ** meta["z"]; x = (lon + 180) / 360 * n; k = meta.get("down", 2)
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return (x - meta["tx0"]) * 256 / k, (y - meta["ty0"]) * 256 / k


def parse(path):
    date, fixes, pilot, glider = None, [], "", ""
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("HFDTE"):
            m = re.search(r"(\d{2})(\d{2})(\d{2})", line)
            if m:
                date = "20%s-%s-%s" % (m.group(3), m.group(2), m.group(1))
        elif line.startswith("HFPLT"):
            pilot = line.split(":", 1)[-1].strip()
        elif line.startswith("HFGTY"):
            glider = line.split(":", 1)[-1].strip()
        elif line.startswith("B") and len(line) >= 35:
            try:
                t = int(line[1:3]) * 3600 + int(line[3:5]) * 60 + int(line[5:7])
                lat = int(line[7:9]) + int(line[9:14]) / 60000.0
                if line[14] == "S": lat = -lat
                lon = int(line[15:18]) + int(line[18:23]) / 60000.0
                if line[23] == "W": lon = -lon
                galt = int(line[30:35])
            except ValueError:
                continue
            fixes.append((t, lat, lon, galt))
    return date, fixes, pilot, glider


def hav(a, b):
    R = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[2], b[1], b[2]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def simplify(pts, eps):
    """Douglas-Peucker on (x, y) with z carried along."""
    if len(pts) < 3:
        return pts
    def d(p, a, b):
        ax, ay, bx, by = a[0], a[1], b[0], b[1]
        L = (bx - ax) ** 2 + (by - ay) ** 2
        if L == 0: return math.hypot(p[0] - ax, p[1] - ay)
        t = max(0, min(1, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / L))
        return math.hypot(p[0] - (ax + t * (bx - ax)), p[1] - (ay + t * (by - ay)))
    idx, dm = 0, 0
    for i in range(1, len(pts) - 1):
        dd = d(pts[i], pts[0], pts[-1])
        if dd > dm: idx, dm = i, dd
    if dm > eps:
        return simplify(pts[:idx + 1], eps)[:-1] + simplify(pts[idx:], eps)
    return [pts[0], pts[-1]]


def build(name, path, meta):
    date, fixes, pilot, glider = parse(path)
    if not fixes:
        raise SystemExit("%s: no fixes" % path)
    # the flight: from the first fix moving faster than 8 km/h to the last
    def spd(i):
        if i == 0: return 0
        dt = max(1, fixes[i][0] - fixes[i - 1][0]); return hav(fixes[i - 1], fixes[i]) / dt * 3600
    a = next((i for i in range(1, len(fixes)) if spd(i) > 8), 0)
    b = len(fixes) - 1
    while b > a and spd(b) < 2: b -= 1
    fl = fixes[a:b + 1]
    dist = sum(hav(fl[i - 1], fl[i]) for i in range(1, len(fl)))
    dur = fl[-1][0] - fl[0][0]
    if dur <= 0:
        raise SystemExit("%s: no duration" % path)
    hi = max(f[3] for f in fl)
    xc = xc_score(fl)
    avg = xc["distance_km"] / (dur / 3600.0)
    far = max(hav(fl[0], f) for f in fl)                 # the furthest the flight got from where it left the ground
    # the fixes in the box, as runs; the kilometres outside it, by the side they lie on
    segs, run, inside, off_km, sides = [], [], 0, 0.0, {"south": 0.0, "north": 0.0, "east": 0.0, "west": 0.0}
    for i, (t, lat, lon, galt) in enumerate(fl):
        x, y = grid_px(lon, lat, meta)
        if 0 <= x < meta["w"] and 0 <= y < meta["h"]:
            run.append((round(x, 1), round(y, 1), galt)); inside += 1
        else:
            if run: segs.append(run); run = []
            if i:
                d = hav(fl[i - 1], fl[i]); off_km += d
                dx, dy = (x - meta["w"] / 2) / meta["w"], (y - meta["h"] / 2) / meta["h"]
                sides[("south" if dy > 0 else "north") if abs(dy) > abs(dx) else ("east" if dx > 0 else "west")] += d
    if run: segs.append(run)
    if inside < len(fl) * 0.5:
        raise SystemExit("%s: %d of %d fixes outside the terrain box; not a Bir flight" % (path, len(fl) - inside, len(fl)))
    out = []
    for seg in segs:
        if len(seg) < 2: continue
        eps = 100.0 / DEM["grid"]["mpp"]                  # a hundred metres of tolerance, whatever the grid's resolution
        simp = simplify(seg, eps)
        if len(simp) > 600:
            simp = simplify(seg, eps * 2.7)
        out.append([[p[0], p[1], p[2]] for p in simp])
    off = {"km": round(off_km, 1), "side": max(sides, key=sides.get)} if off_km >= 1 else None
    def rpx(i):
        x, y = grid_px(fl[i][2], fl[i][1], meta); return [round(x, 1), round(y, 1), fl[i][3]]
    return dict(name=name, date=date, pilot=pilot, glider=glider, type=xc["type"], closed=xc["closed"], distance_km=round(xc["distance_km"], 1),
                points=round(xc["points"], 1), legs_km=xc["legs_km"], gap_km=xc["gap_km"], ground_km=round(dist, 1), duration_min=int(round(dur / 60)),
                avg_kmh=round(avg, 1), max_alt_m=int(hi), far_km=round(far, 1), fixes=len(fl), off_map=off, route=[rpx(i) for i in xc["route"]], segs=out)


def main():
    args = [a for a in sys.argv[1:] if "=" in a and not a.startswith("--")]
    out = os.path.join(ROOT, "tools", "data", "india-tracks.json")
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    g = DEM["grid"]
    meta = dict(z=g["z"], tx0=g["tx0"], ty0=g["ty0"], w=g["w"], h=g["h"], down=g.get("down", 2))
    tracks = [build(a.split("=", 1)[0], a.split("=", 1)[1], meta) for a in args]
    json.dump(dict(source="IGC tracklogs supplied by the owner, scored with the XContest rules (tools/xc_score.py); average speed is the scored distance over the time in the air", tracks=tracks), open(out, "w"), indent=0)
    for t in tracks:
        print("%-28s %s  %s%s %6.1f km (%.1f pts)  %4d min  %5.1f km/h  track %5.1f km  max %5d m  %d pts in %d segments, off the map: %s" % (
            t["name"], t["date"], "closed " if t["closed"] else "", t["type"], t["distance_km"], t["points"], t["duration_min"], t["avg_kmh"], t["ground_km"], t["max_alt_m"], sum(len(s) for s in t["segs"]), len(t["segs"]), t["off_map"]))


if __name__ == "__main__":
    main()
