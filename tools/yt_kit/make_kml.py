"""Google Earth file for one task: the top N tracks animated in time, 3D turnpoint cylinders, a camera tour.

    python3 make_kml.py t1 1 [N]

Reads t1/results.json (SRS provisional scores), t1/kmz/doc.kml (SRS's task KMZ: the cylinders) and t1/igc/*.igc
(SRS's IGC zip, named by competition ID). Writes out/earth/Tapalpa_TaskN_GoogleEarth.kmz.
Open in Google Earth Pro: the time slider plays the race; Tour "Fly the race" flies it (Tools > Movie Maker records it).
"""
import json, math, os, re, sys, zipfile, datetime as dt
from xml.sax.saxutils import escape

K = os.path.dirname(os.path.abspath(__file__))
D, TASK = os.path.join(K, sys.argv[1]), int(sys.argv[2])
N = int(sys.argv[3]) if len(sys.argv) > 3 else 10
COLS = ["ff1775ff", "ff4700ce", "ff478600", "ffffffff", "ff00d7ff", "ffff9e1e", "ffb469ff", "ff5ce1e6", "ff7fbf7f", "ff8080ff"]  # aabbggrr


def igc_points(path):
    date, pts = None, []
    for line in open(path, encoding="latin-1"):
        if line.startswith("HFDTE"):
            m = re.search(r"(\d{6})", line); d = m.group(1); date = dt.date(2000 + int(d[4:]), int(d[2:4]), int(d[:2]))
        elif line.startswith("B") and len(line) >= 35:
            t = line[1:7]; lat = int(line[7:9]) + int(line[9:14]) / 60000.0; lat = -lat if line[14] == "S" else lat
            lon = int(line[15:18]) + int(line[18:23]) / 60000.0; lon = -lon if line[23] == "W" else lon
            alt = int(line[30:35])
            pts.append((dt.datetime.combine(date, dt.time(int(t[:2]), int(t[2:4]), int(t[4:6]))), lon, lat, alt))
    return pts


def cylinders():
    kml = open(os.path.join(D, "kmz", "doc.kml"), encoding="utf-8").read()
    seg = kml.split("<name>2d Cylinders</name>", 1)[1]
    out = []
    for m in re.finditer(r"<Placemark>\s*<name>([^<]+)</name>.*?<coordinates>([^<]+)</coordinates>", seg, re.S):
        name, co = m.group(1), [tuple(map(float, c.split(",")[:2])) for c in m.group(2).split()]
        if out and name == out[0][0]:      # the list starts again (SRS's 3D set): the task is complete
            break
        out.append((name, co))
    return out


def main():
    R = json.load(open(os.path.join(D, "results.json")))["sports"]
    top = R[:N]
    tracks = []
    for i, r in enumerate(top):
        f = os.path.join(D, "igc", "%s.igc" % r["ID"])
        if not os.path.exists(f):
            continue
        pts = igc_points(f)[::4]                      # every 4th fix is plenty for the replay
        tracks.append((i, r, pts))
    # the race: from the start gate to the last of the top N in goal (UTC; Tapalpa is UTC-6)
    t0 = min(p[0][0] for _, _, p in tracks)
    # the start gate from SRS's own Start column (local, UTC-6); 12:30 if no pilot has one
    st = next((r["Start"] for r in R if r.get("Start")), "12:30:00")
    h, m, _ = map(int, st.split(":"))
    start = dt.datetime.combine(t0.date(), dt.time(h, m)) + dt.timedelta(hours=6)
    ends = []
    for _, r, pts in tracks:
        fin = r.get("Finish")
        ends.append(dt.datetime.combine(t0.date(), dt.time(*map(int, fin.split(":")))) + dt.timedelta(hours=6) if fin else pts[-1][0])
    end = max(ends) + dt.timedelta(minutes=2)

    def iso(t): return t.strftime("%Y-%m-%dT%H:%M:%SZ")
    pm = []
    # cylinders: the task's turnpoints as see-through walls 2,400 m to 3,400 m above sea level
    cyl = cylinders()
    for k, (name, ring) in enumerate(cyl):
        col = "6600d7ff" if k in (0, len(cyl) - 1) else "551775ff"
        coords = " ".join("%.6f,%.6f,3400" % c for c in ring)
        pm.append('<Placemark><name>%s</name><Style><LineStyle><color>ccffffff</color><width>2</width></LineStyle><PolyStyle><color>%s</color></PolyStyle></Style>'
                  '<Polygon><extrude>1</extrude><altitudeMode>absolute</altitudeMode><outerBoundaryIs><LinearRing><coordinates>%s</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
                  % (escape(name), col, coords))
    # the tracks
    for i, r, pts in tracks:
        col = COLS[i % len(COLS)]
        name = "%s. %s" % (r["Rank"], r["Name"])
        when = "".join("<when>%s</when>" % iso(p[0]) for p in pts if start - dt.timedelta(minutes=20) <= p[0] <= end)
        coord = "".join("<gx:coord>%.6f %.6f %d</gx:coord>" % (p[1], p[2], p[3]) for p in pts if start - dt.timedelta(minutes=20) <= p[0] <= end)
        pm.append('<Placemark><name>%s</name><Style><IconStyle><color>%s</color><scale>1.1</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/arrow.png</href></Icon></IconStyle>'
                  '<LabelStyle><color>%s</color><scale>1.1</scale></LabelStyle><LineStyle><color>%s</color><width>4</width></LineStyle></Style>'
                  '<gx:Track><altitudeMode>absolute</altitudeMode>%s%s</gx:Track></Placemark>' % (escape(name), col, col, col, when, coord))
    # the tour: the camera follows the leader on points, 3 s of film for every 4 min of race, the time slider in step
    lead = tracks[0][2]
    tour, t, step = [], start, dt.timedelta(minutes=4)
    def at(ts):
        best = min(lead, key=lambda p: abs((p[0] - ts).total_seconds())); return best
    prev = at(start)
    while t <= end:
        p = at(t); hd = math.degrees(math.atan2(p[1] - prev[1], p[2] - prev[2])) % 360 if p != prev else 0
        tour.append('<gx:FlyTo><gx:duration>3</gx:duration><gx:flyToMode>smooth</gx:flyToMode><LookAt><gx:TimeSpan><begin>%s</begin><end>%s</end></gx:TimeSpan>'
                    '<longitude>%.6f</longitude><latitude>%.6f</latitude><altitude>%d</altitude><heading>%.1f</heading><tilt>68</tilt><range>9000</range>'
                    '<altitudeMode>absolute</altitudeMode></LookAt></gx:FlyTo>' % (iso(start - dt.timedelta(minutes=20)), iso(t), p[1], p[2], p[3], hd))
        prev, t = p, t + step
    doc = ('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2"><Document>'
           '<name>SRS Advance Edition, Tapalpa: Task %d (top %d, provisional)</name><open>1</open>'
           '<Folder><name>Turnpoints</name>%s</Folder><Folder><name>Top %d tracks</name><open>1</open>%s</Folder>'
           '<gx:Tour><name>Fly the race</name><gx:Playlist>%s</gx:Playlist></gx:Tour></Document></kml>'
           % (TASK, N, "".join(pm[:len(cyl)]), N, "".join(pm[len(cyl):]), "".join(tour)))
    out = os.path.join(K, "out", "earth"); os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, "Tapalpa_Task%d_GoogleEarth.kmz" % TASK)
    with zipfile.ZipFile(fn, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("doc.kml", doc)
    print(fn, len(tracks), "tracks,", len(cyl), "cylinders,", len(tour), "tour stops", os.path.getsize(fn) // 1024, "KB")


if __name__ == "__main__":
    main()
