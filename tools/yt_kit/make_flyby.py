"""A Google Earth fly-by of one task's route (owner, 11 Nov 2026: "a task file I can play in Google Earth and
create some animations ... of the route, like a fly-by").

    python3 make_flyby.py N          (after make_day.py N has fetched tN/kmz/doc.kml from SRS)

Writes out/earth/Tapalpa_TaskN_FlyBy.kmz: the optimised route SRS publishes (its "Route" folder) as an orange
curtain over the ground, the turnpoint cylinders as see-through walls with their names, and three tours:
"1 Fly-by" (overview, swoop to the start, follow the route at low level, orbit goal, pull back),
"2 Overview orbit" (one slow turn around the whole task) and "3 Turnpoints" (a still at each turnpoint).
In Google Earth Pro: open the file, double-click a tour in Places to play it; Tools > Movie Maker records it
(choose the tour, 3840x2160, 60 fps). Nothing here is invented: every point is SRS's own.
"""
import math, os, re, sys, zipfile
from xml.sax.saxutils import escape

K = os.path.dirname(os.path.abspath(__file__))
N = int(sys.argv[1])
KML = open(os.path.join(K, "t%d" % N, "kmz", "doc.kml"), encoding="utf-8").read()
R_EARTH = 6371000.0


def coords(s):
    return [tuple(map(float, c.split(",")[:2])) for c in s.split()]


def dist(a, b):
    lo1, la1, lo2, la2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R_EARTH * math.asin(math.sqrt(h))


def bearing(a, b):
    lo1, la1, lo2, la2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return math.degrees(math.atan2(y, x)) % 360


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# the route: SRS's "Route" folder, leg by leg (each leg lists its two tag points twice, at 10 m and 0 m)
seg = KML.split("<name>Route</name>", 1)[1]
legs = re.findall(r"<Placemark>\s*<name>([^<]+)</name>.*?<coordinates>([^<]+)</coordinates>", seg, re.S)
pts, names = [], []
for nm, co in legs:
    c = coords(co)
    a, b = c[0], c[-1]
    if not pts:
        pts.append(a)
    if dist(pts[-1], b) > 1:
        pts.append(b)
    names.append(nm.strip())
total = sum(dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))

# the cylinders: SRS's 2d set, until the list starts again
seg = KML.split("<name>2d Cylinders</name>", 1)[1].split("<name>3d Cylinders</name>", 1)[0]
cyl = []
for m in re.finditer(r"<Placemark>\s*<name>([^<]+)</name>.*?<coordinates>([^<]+)</coordinates>", seg, re.S):
    cyl.append((m.group(1), coords(m.group(2))))
title = re.search(r"<name>(T\d+\.\d+\.[^<]*)</name>", KML)
title = title.group(1).strip() if title else "Task %d" % N

# the camera path: a point every 250 m along the route
STEP = 250.0
path = []
for i in range(len(pts) - 1):
    d = dist(pts[i], pts[i + 1])
    n = max(1, int(d // STEP))
    for k in range(n):
        path.append(lerp(pts[i], pts[i + 1], k / n))
path.append(pts[-1])


def heading_at(i, ahead=1500.0):
    """the bearing to a point ~1.5 km further on, so the camera turns before each turnpoint, not at it"""
    j, d = i, 0.0
    while j < len(path) - 1 and d < ahead:
        d += dist(path[j], path[j + 1]); j += 1
    return bearing(path[i], path[j]) if j > i else bearing(path[i - 1], path[i])


hs, prev = [], None
for i in range(len(path)):
    h = heading_at(i)
    if prev is not None:                       # low-pass the heading (shortest way round) for a smooth glide
        dh = (h - prev + 540) % 360 - 180
        h = (prev + 0.35 * dh) % 360
    hs.append(h); prev = h

cen = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
span = max(dist(cen, p) for p in pts) * 2.6 + 8000


def lookat(p, heading, tilt, rng, alt=0, mode="relativeToGround"):
    return ("<LookAt><longitude>%.6f</longitude><latitude>%.6f</latitude><altitude>%d</altitude><heading>%.1f</heading>"
            "<tilt>%.1f</tilt><range>%d</range><gx:altitudeMode>%s</gx:altitudeMode></LookAt>"
            % (p[0], p[1], alt, heading, tilt, rng, mode))


def fly(p, heading, tilt, rng, dur, mode="smooth"):
    return "<gx:FlyTo><gx:duration>%.2f</gx:duration><gx:flyToMode>%s</gx:flyToMode>%s</gx:FlyTo>" % (dur, mode, lookat(p, heading, tilt, rng))


def wait(s):
    return "<gx:Wait><gx:duration>%.1f</gx:duration></gx:Wait>" % s


# tour 1: the fly-by. Overview, swoop to the start, follow the route (about 70 s of film for the whole task,
# whatever its length), orbit goal, pull back.
SPEED = total / 70.0                           # metres of route per second of film
t1 = [fly(cen, hs[0], 35, span, 0.1, "bounce"), wait(2.5),
      fly(path[0], hs[0], 72, 2600, 5.0, "bounce")]
for i in range(1, len(path)):
    t1.append(fly(path[i], hs[i], 72, 2600, dist(path[i - 1], path[i]) / SPEED))
g = pts[-1]
for k in range(1, 13):                         # one turn around goal in 9 s
    t1.append(fly(g, (hs[-1] + k * 30) % 360, 62, 1800, 0.75))
t1 += [wait(1.0), fly(cen, hs[-1], 35, span, 6.0, "bounce"), wait(2.0)]

# tour 2: one slow orbit of the whole task (36 s)
t2 = [fly(cen, 0, 50, span * 0.8, 0.1, "bounce"), wait(1.0)]
for k in range(1, 37):
    t2.append(fly(cen, k * 10 % 360, 50, span * 0.8, 1.0))

# tour 3: a still at each turnpoint, 4 s each, looking along the next leg
t3 = [fly(cen, 0, 35, span, 0.1, "bounce"), wait(2.0)]
for i, p in enumerate(pts):
    h = bearing(p, pts[i + 1]) if i + 1 < len(pts) else bearing(pts[i - 1], p)
    t3 += [fly(p, h, 65, 3500, 4.0, "bounce"), wait(4.0)]


def tour(name, items):
    return "<gx:Tour><name>%s</name><gx:Playlist>%s</gx:Playlist></gx:Tour>" % (escape(name), "".join(items))


# the route as an orange curtain 150 m over the ground, and a bright line on top
line = " ".join("%.6f,%.6f,150" % p for p in path)
route = ('<Placemark><name>Route, %.1f km</name><Style><LineStyle><color>ff1775ff</color><width>5</width></LineStyle>'
         '<PolyStyle><color>661775ff</color></PolyStyle></Style><LineString><extrude>1</extrude><tessellate>1</tessellate>'
         '<altitudeMode>relativeToGround</altitudeMode><coordinates>%s</coordinates></LineString></Placemark>' % (total / 1000, line))
walls, seen = [], set()
for k, (nm, ring) in enumerate(cyl):
    first, last = k == 0, k == len(cyl) - 1
    col = "5500d7ff" if (first or last) else "441775ff"
    walls.append('<Placemark><name>%s</name><Style><LineStyle><color>ccffffff</color><width>2</width></LineStyle>'
                 '<PolyStyle><color>%s</color></PolyStyle></Style><Polygon><extrude>1</extrude><altitudeMode>relativeToGround</altitudeMode>'
                 '<outerBoundaryIs><LinearRing><coordinates>%s</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
                 % (escape(nm), col, " ".join("%.6f,%.6f,600" % c for c in ring)))
labels = []
for i, p in enumerate(pts):
    nm = names[i - 1].split(" - ")[1].split(":")[0].strip() if i else names[0].split(" - ")[0].strip()
    labels.append('<Placemark><name>%s</name><Style><IconStyle><scale>0</scale></IconStyle><LabelStyle><scale>1.3</scale></LabelStyle></Style>'
                  '<Point><altitudeMode>relativeToGround</altitudeMode><coordinates>%.6f,%.6f,700</coordinates></Point></Placemark>' % (escape(nm), p[0], p[1]))

doc = ('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">'
       '<Document><name>SRS Advance Edition, Tapalpa: Task %d fly-by (%s)</name><open>1</open>'
       '<Folder><name>Course</name><open>1</open>%s<Folder><name>Turnpoints</name>%s%s</Folder></Folder>'
       '<Folder><name>Tours (double-click to play)</name><open>1</open>%s%s%s</Folder></Document></kml>'
       % (N, escape(title), route, "".join(walls), "".join(labels),
          tour("1 Fly-by: Task %d, %.1f km" % (N, total / 1000), t1), tour("2 Overview orbit", t2), tour("3 Turnpoints", t3)))
out = os.path.join(K, "out", "earth"); os.makedirs(out, exist_ok=True)
fn = os.path.join(out, "Tapalpa_Task%d_FlyBy.kmz" % N)
with zipfile.ZipFile(fn, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("doc.kml", doc)
dur = sum(float(x) for x in re.findall(r"<gx:duration>([\d.]+)</gx:duration>", "".join(t1)))
print("%s: route %.1f km, %d turnpoints, %d cylinders, fly-by %.0f s, %d KB"
      % (os.path.basename(fn), total / 1000, len(pts), len(cyl), dur, os.path.getsize(fn) // 1024))
