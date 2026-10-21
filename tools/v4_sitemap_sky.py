#!/usr/bin/env python3
"""
The v4 sitemap's night sky from real stars (owner's queue, 20 Oct 2026, item 1;
the motion asked for by the owner the same day).

The sitemap (prototypes/v4/sitemap.html) used to load the LIVE sitemap-sky.js,
which is never edited here. That script draws its background field on the
.sky-stars canvas from a seeded random number generator, now and then lets a
shooting star cross on its own, and the episode stars twinkle (sitemap.html's
.sky-core animation). The episode stars and the series constellations are the
site's data and stay as they are.

This writes prototypes/v4/v4-sitemap-sky.js, a copy of the live script with
only its background field changed, and the v4 page loads it in place of the
live one:

  - the field is the real sky: every star of STARS in tools/v4_record.py that
    falls in it (the record page's data: positions and magnitudes from the npm
    package d3-celestial 0.7.35, data/stars.6.json, whose star data is XHIP:
    An Extended Hipparcos Compilation, Anderson and Francis 2012, VizieR
    V/137D, converted by Olaf Frohn; BSD-3-Clause, its notice is STAR_NOTE and
    goes at the head of the file with the data). The field is centred on
    Sirius's part of the sky (RA 95, Dec -25: Orion, Canis Major, Puppis and
    Carina), drawn looking up (east to the left) in a stereographic
    projection; each star is sized and lit by its magnitude, in --white;
  - depth: the brighter a star, the nearer it is drawn, so the field moves in
    layers. The sky zooms in slowly and back out (about 80 s each way, the
    nearer stars further), follows the camera's pan and zoom at a fraction of
    its pace, and leans a little towards the mouse pointer, eased;
  - the shooting star and the episode stars' twinkle are the live script's and
    page's own, unchanged (the owner asked for both, 20 Oct 2026);
  - with reduced motion the field is drawn once and moves only with the
    camera; the zoom stops while the sky is off screen or the tab is hidden.

The live file is checked each run: if a patched line has changed there, this
stops rather than lose the change. The page keeps the credit in a comment
between <!--v4sky--> and <!--/v4sky--> right before <!-- site-schema --> (v4_pwa
puts its app block before </head> after this runs), and the script tag between
<!--v4sky:js--> marks; both are rewritten whole each run, so the pass is
idempotent. It runs in tools/v4_build.py after v4_ux.

The ground under the sky (owner, 21 Oct: the sitemap "only navigates the episodes, but now the site has
increased substantially"; of the two ways, the full list): the live script writes its four short groups
into .sky-ground when the page runs, where no search engine reads them. Here the ground is written into
the page itself, between <!--v4map--> marks, as a map of every page that is not an episode: Trips (the
expeditions page and the four trips, from the page's own SITEMAP_SKY tree), Listen, Learn (the knowledge
base and its five levels, the encyclopedia's Atlas and A to Z), About (with the speed record), Legal,
then rows of the 13 series, the topics and the ten answers in depth. The script leaves a ground it
finds written (one patched line). The encyclopedia and the record page are prototype-only, so their
links sit between v4:needs marks and the switch-over leaves them out until the owner's go.

The landmarks (owner, 21 Oct, of the two ways to show the rest of the site in the sky: "A. Landmarks in the
same sky"): the episode constellations stay as they are, and the main parts of the site join them as named,
clickable bodies in a frame that stays still while the sky moves, as a planetarium's horizon does: Home as
the moon and the encyclopedia's Atlas as a small globe, top right; the knowledge base's five levels as an
altitude scale up the left edge (600 m to 4,000 m, as on its page); and under the sky a horizon where the
four trips rise as planets over the mountain line, each with its own photograph, and About, Mission,
Partners and the Speed Record shine as named stars. Every word, picture and link is the page's own data
(the SITEMAP_SKY tree, the knowledge base's levels, the A to Z's count). Hover only; still with reduced
motion. Between <!--v4marks:...--> marks, written whole each run.
"""
import hashlib
import html as H_
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
PAGE = os.path.join(V4, "sitemap.html")
OUT = os.path.join(V4, "v4-sitemap-sky.js")
OLD_SVG = os.path.join(V4, "img", "sitemap-stars.svg")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from v4_record import STARS, STAR_NOTE   # noqa: E402

RA0, DEC0 = 95.0, -25.0      # the field's centre: Sirius's part of the sky
HW, HH = 1.75, 1.0           # half the field, in stereographic units (about 164 by 106 degrees across)


def fail(msg):
    raise SystemExit("v4_sitemap_sky: " + msg)


def project(ra, dec):
    """Oblique stereographic, looking up: east to the left, north up."""
    a, d, d0 = math.radians(ra - RA0), math.radians(dec), math.radians(DEC0)
    cosc = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a)
    if cosc < -0.2:
        return None
    k = 2 / (1 + cosc)
    x = -k * math.cos(d) * math.sin(a)
    y = -k * (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a))
    return x, y


def field():
    out = []
    for row in STARS.split():
        ra, dec, mag, _bv = (float(v) for v in row.split(","))
        p = project(ra, dec)
        if p and abs(p[0]) <= HW + 0.15 and abs(p[1]) <= HH + 0.15:
            out.append([round(p[0], 3), round(p[1], 3), mag])
    return out


# What the copy adds: the real field, its depth, its slow zoom and its parallax. Inserted after the
# script's own state (the line that declares vw, vh, bg and the shooting star).
SKY_JS = r"""
  /* v4: the background is the real sky (tools/v4_sitemap_sky.py; the data's credit is at the head of this
     file). REAL is [x, y, magnitude] in stereographic units about RA 95, Dec -25, looking up; the field is
     3.5 by 2 units, drawn to cover the view with room to move. Brighter stars are nearer: they move and
     zoom more. */
  var REAL = %s;
  var WHITE = (getComputedStyle(document.documentElement).getPropertyValue('--white') || '').trim() || '#f6f4f4';
  var skyOn = true, mx = 0, my = 0, mxE = 0, myE = 0, home = null;
  function realSky() {
    var s = Math.max(vw / 3.5, vh / 2) * 1.2, rk = Math.max(0.75, Math.min(1.3, s / 492));
    bg = REAL.map(function (st) {
      var t = Math.max(0, Math.min(1, (st[2] + 1.5) / 6.1));
      return [st[0] * s, st[1] * s, (1.7 - 1.15 * t) * rk, 0.85 - 0.6 * t, 1 - t];
    });
  }
  function sky(now) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, vw, vh);
    ctx.fillStyle = WHITE;
    if (!home) home = { x: cam.x, y: cam.y, k: cam.k };
    var breathe = reduce ? 0 : (1 - Math.cos(now / 1000 * 6.2832 / 160)) / 2;
    var ck = Math.pow(cam.k / home.k, 0.15);
    var px0 = Math.max(-1, Math.min(1, (cam.x - home.x) / 1500)) * -vw * 0.07;
    var py0 = Math.max(-1, Math.min(1, (cam.y - home.y) / 900)) * -vh * 0.07;
    if (!reduce) { mxE += (mx - mxE) * 0.04; myE += (my - myE) * 0.04; }
    var cx = vw / 2, cy = vh / 2;
    for (var i = 0; i < bg.length; i++) {
      var st = bg[i], d = 0.35 + 0.65 * st[4];
      var z = (1 + 0.12 * breathe * (0.4 + d)) * (1 + (ck - 1) * d);
      var x = cx + st[0] * z + (px0 - mxE * 22) * d, y = cy + st[1] * z + (py0 - myE * 14) * d;
      if (x < -4 || x > vw + 4 || y < -4 || y > vh + 4) continue;
      ctx.globalAlpha = st[3];
      ctx.beginPath(); ctx.arc(x, y, st[2], 0, 6.2832); ctx.fill();
    }
  }
  view.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse') return;
    var r = view.getBoundingClientRect();
    mx = (e.clientX - r.left) / r.width * 2 - 1; my = (e.clientY - r.top) / r.height * 2 - 1;
  });
  view.addEventListener('pointerleave', function () { mx = 0; my = 0; });
  if (window.IntersectionObserver) new IntersectionObserver(function (en) { skyOn = en[0].isIntersecting; }).observe(view);
"""

# (what the live file has, exactly once) -> (what the copy has)
PATCHES = [
    ("  var vw = 0, vh = 0, dpr = 1, bg = [], raf = 0, t0 = 0, shoot = null, shootT = 0, ambient = 0;\n",
     None),   # SKY_JS goes after this line
    ("""    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, vw, vh);
    ctx.fillStyle = 'rgb(180,180,180)';
    var ox = -cam.x * 0.14, oy = -cam.y * 0.14;
    for (var i = 0; i < bg.length; i++) {
      var s = bg[i];
      var px = ((s[0] + ox * s[4]) % vw + vw) % vw, py = ((s[1] + oy * s[4]) % vh + vh) % vh;
      ctx.globalAlpha = s[3];
      ctx.beginPath(); ctx.arc(px, py, s[2], 0, 6.2832); ctx.fill();
    }
""", "    sky(now);\n"),
    ("""    bg = [];
    var s0 = seed; seed = 77;
    for (var i = 0, n = Math.round(w * h / 2600); i < n; i++) bg.push([rnd() * w, rnd() * h, 0.3 + rnd() * 0.8, 0.06 + rnd() * rnd() * 0.5, 0.3 + rnd() * 1.3]);
    seed = s0;
""", "    realSky();\n"),
    ("    if (shoot) draw(now);\n",
     "    if (shoot) draw(now);\n    else if (!reduce && skyOn && !document.hidden) sky(now);\n"),
    # the ground is written into the page (ground() below): keep it
    ("    ground.innerHTML = h + '</div>';\n",
     "    if (!ground.querySelector('.sky-g')) ground.innerHTML = h + '</div>';\n"),
]


def script():
    src = open(os.path.join(ROOT, "sitemap-sky.js"), encoding="utf-8").read()
    for old, new in PATCHES:
        if src.count(old) != 1:
            fail("sitemap-sky.js changed: %r is not there once" % old.strip().split("\n")[0])
        if new is None:
            new = old + SKY_JS % json.dumps(field(), separators=(",", ":"))
        src = src.replace(old, new)
    head = ("/* v4-sitemap-sky.js: written by tools/v4_sitemap_sky.py from the live sitemap-sky.js, with its random\n"
            "   background field replaced by the real sky, in depth, zooming slowly and moving with the camera and the\n"
            "   pointer. Do not edit; change sitemap-sky.js or the tool and run it.\n"
            + STAR_NOTE.replace("<!-- ", "   ").replace(" -->", "") + " */\n")
    return head + src


MAP = ("<!--v4map-->", "<!--/v4map-->")
RIDGE = ('<svg class="sky-ridge" viewBox="0 0 1200 40" preserveAspectRatio="none" aria-hidden="true"><path d="M0,34 L70,28 '
         'L130,14 L180,6 L225,12 L300,27 L380,32 L470,24 L540,30 L640,21 L720,31 L820,18 L900,29 L1010,23 L1100,31 L1200,26"/></svg>')
MAP_CSS = (
    "@media (min-width:901px){.sky-ground .sky-ground-in{grid-template-columns:1.35fr repeat(4,minmax(0,1fr))}}"
    ".sky-row{grid-column:1/-1;padding-top:var(--sp-3);border-top:1px solid var(--edge)}"
    ".sky-row ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:row;flex-wrap:wrap;gap:.15rem 1.15rem}"
    ".sky-row a{display:inline-flex;align-items:center;min-height:34px;color:var(--gray-light);font-size:.9rem;transition:color .15s ease}"
    ".sky-row a:hover{color:var(--orange)}"
    ".sky-g a small.sky-alt{display:inline;margin-left:.45rem;letter-spacing:.06em}"
)


def _need(page, inner):
    return "<!-- v4:needs %s -->%s<!-- /v4:needs -->" % (page, inner)


def _h1(rel):
    s = open(os.path.join(V4, rel), encoding="utf-8").read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    return H_.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else None


def ground(page):
    """The map of every page that is not an episode, written into .sky-ground (see the docstring)."""
    m = re.search(r"window\.SITEMAP_SKY = (\{.*?\});?\s*</script>", page, re.S)
    if not m:
        fail("no SITEMAP_SKY tree in sitemap.html")
    tree = json.loads(m.group(1))["tree"]
    by = {c["label"]: c for c in tree["children"]}
    E = lambda t: H_.escape(t, quote=True)

    def li(url, label, img=None, sub=None, alt=None):
        pic = '<img src="%s" alt="">' % E(img) if img else ""
        small = "<small>%s</small>" % E(sub) if sub else ""
        a = '<small class="sky-alt">%s</small>' % E(alt) if alt else ""
        return '<li><a href="%s">%s<span>%s%s%s</span></a></li>' % (E(url), pic, E(label), a, small)

    def group(title, items):
        return '<div class="sky-g"><h2>%s</h2><ul>%s</ul></div>' % (E(title), "".join(items))

    trips = [li("expeditions.html", "Expeditions", sub=by["Trips"].get("sub"))]
    trips += [li(c["url"], c["label"], c.get("img"), c.get("sub") if c.get("kind") == "trip" else None)
              for c in by["Trips"]["children"]]
    listen = [li("index.html", "Home"), li("podcast.html", "Podcast"), li("library.html", "Episode Library"),
              li("tags.html", "Topics")]
    kb = open(os.path.join(V4, "knowledge-base.html"), encoding="utf-8").read()
    learn = [li("knowledge-base.html", "Knowledge Base")]
    stations = re.findall(r'<section class="clb-station" id="lvl-\d" data-alt="([^"]+)"', kb)
    cats = [c for c in by["Knowledge Base"]["children"] if c.get("kind") == "category"]
    for i, c in enumerate(cats):
        learn.append(li(c["url"], c["label"], alt=("%s m" % stations[i]) if i < len(stations) else None))
    learn.append(_need("knowledge-base/encyclopedia/atlas.html", li("knowledge-base/encyclopedia/atlas.html", "The Atlas")))
    learn.append(_need("knowledge-base/encyclopedia/index.html", li("knowledge-base/encyclopedia/index.html", "Encyclopedia, A to Z")))
    about = [li(by["About Me"]["url"], "About Me")] + [li(c["url"], c["label"]) for c in by["About Me"]["children"]]
    about.insert(3, _need("record-attempt.html", li("record-attempt.html", "Speed Record")))
    legal = [li(c["url"], c["label"]) for c in by["Legal"]["children"]]
    series = [s for c in cats for s in c.get("children", [])]
    row_series = ('<div class="sky-row sky-g"><h2>The %d series</h2><ul>%s</ul></div>'
                  % (len(series), "".join(li(s["url"], s["label"]) for s in series)))
    topics = []
    for f in sorted(os.listdir(os.path.join(V4, "tags"))):
        if f.endswith(".html"):
            t = _h1("tags/" + f)
            if t:
                topics.append((t.lstrip("#").strip(), "tags/" + f))
    topics.sort(key=lambda t: t[0].lower())
    row_topics = ('<div class="sky-row sky-g"><h2>%d topics</h2><ul>%s</ul></div>'
                  % (len(topics), "".join(li(u, t) for t, u in topics)))
    enc = os.path.join(V4, "knowledge-base", "encyclopedia")
    deep = []
    if os.path.isdir(enc):
        fm = open(os.path.join(V4, "knowledge-base", "flight-mechanics.html"), encoding="utf-8").read()
        deep = re.findall(r'<a class="nx-card" href="(encyclopedia/[a-z0-9-]+\.html)"><span class="kicker">[^<]*</span><strong>([^<]*)</strong>', fm)
    row_deep = _need("knowledge-base/encyclopedia/index.html", '<div class="sky-row sky-g"><h2>Answered in depth</h2><ul>%s</ul></div>'
                     % "".join(li("knowledge-base/" + u, H_.unescape(q)) for u, q in deep)) if deep else ""
    inner = (RIDGE + '<div class="sky-ground-in">' + group("Trips", trips) + group("Listen", listen) + group("Learn", learn)
             + group("About", about) + group("Legal", legal) + row_series + row_topics + row_deep + "</div>")
    out = re.sub(re.escape(MAP[0]) + r".*?" + re.escape(MAP[1]), "", page, flags=re.S)
    nav = '<nav class="sky-ground" aria-label="Every other page on the site">'
    if out.count(nav) != 1:
        fail("the sitemap's ground is not there once")
    i = out.index(nav) + len(nav)
    j = out.index("</nav>", i)
    out = out[:i] + MAP[0] + "<style>%s</style>" % MAP_CSS + inner + MAP[1] + out[j:]
    return out


MARKS_SKY = ("<!--v4marks:sky-->", "<!--/v4marks:sky-->")
MARKS_BAND = ("<!--v4marks:band-->", "<!--/v4marks:band-->")
MARKS_CSS = (
    ".sky-mk{position:absolute;z-index:4;display:flex;gap:clamp(1rem,2.4vw,2rem);align-items:flex-start;"
    "top:clamp(1.2rem,2.4vw,2rem);right:clamp(1.5rem,5vw,4rem)}"
    ".sky-mk a,.sky-hz a,.sky-alt-sc a{color:inherit;text-decoration:none}"
    ".sky-mk a{display:flex;flex-direction:column;align-items:center;gap:.5rem;text-align:center}"
    ".sky-mk b,.sky-hz b{font-family:var(--font-display);font-weight:600;font-size:.95rem;color:var(--white);line-height:1.2}"
    ".sky-mk small,.sky-hz small{display:block;font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gray-light);margin-top:.15rem}"
    ".sky-moon-o{width:84px;height:84px;border-radius:50%;position:relative;"
    "background:radial-gradient(circle at 36% 32%,var(--white) 0,color-mix(in srgb,var(--white) 82%,var(--gray)) 46%,color-mix(in srgb,var(--gray) 80%,var(--bg)) 100%);"
    "box-shadow:0 0 46px 10px color-mix(in srgb,var(--white) 16%,transparent),inset -12px -9px 24px color-mix(in srgb,var(--bg) 42%,transparent);"
    "transition:transform .45s var(--ease),box-shadow .45s var(--ease)}"
    ".sky-moon-o::before,.sky-moon-o::after{content:\"\";position:absolute;border-radius:50%;background:color-mix(in srgb,var(--gray) 45%,transparent)}"
    ".sky-moon-o::before{width:16px;height:16px;left:46px;top:20px}.sky-moon-o::after{width:10px;height:10px;left:24px;top:50px}"
    ".sky-atlas-o{width:62px;height:62px;margin-top:11px;transition:transform .45s var(--ease)}"
    ".sky-atlas-o circle.g{fill:var(--bg);stroke:var(--edge-hi)}.sky-atlas-o .m{fill:none;stroke:var(--edge);stroke-width:1}"
    ".sky-atlas-o .p{fill:var(--orange)}"
    ".sky-mk a:is(:hover,:focus-visible) .sky-moon-o{transform:scale(1.06);box-shadow:0 0 64px 16px color-mix(in srgb,var(--white) 24%,transparent),inset -12px -9px 24px color-mix(in srgb,var(--bg) 42%,transparent)}"
    ".sky-mk a:is(:hover,:focus-visible) .sky-atlas-o{transform:scale(1.1) rotate(-8deg)}"
    ".sky-mk a:is(:hover,:focus-visible) b,.sky-hz a:is(:hover,:focus-visible) b,.sky-alt-sc a:is(:hover,:focus-visible) b{color:var(--orange)}"
    # the knowledge base's levels, an altitude scale up the left edge
    ".sky-alt-sc{position:absolute;z-index:4;left:clamp(.6rem,1.6vw,1.4rem);top:30%;bottom:16%}"
    ".sky-alt-sc ol{height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:0 0 0 .8rem;"
    "border-left:1px solid var(--edge-hi);margin:0;list-style:none}"
    ".sky-alt-sc li{position:relative}.sky-alt-sc li::before{content:\"\";position:absolute;left:-.8rem;top:.55rem;width:.5rem;height:1px;background:var(--edge-hi)}"
    ".sky-alt-sc a{display:block;line-height:1.2}"
    ".sky-alt-sc i{display:block;font-style:normal;font-size:.68rem;letter-spacing:.08em;color:var(--orange);font-variant-numeric:tabular-nums}"
    ".sky-alt-sc b{font-size:.78rem;font-weight:500;color:var(--gray-light)}"
    ".sky-alt-sc .top{position:absolute;top:-1.6rem;left:0;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gray);white-space:nowrap}"
    # the horizon: the trips rising over the mountain line, and the named stars
    ".sky-hz{position:relative;z-index:1;height:clamp(200px,20vw,250px);overflow:hidden;background:"
    "radial-gradient(1px 1px at 12% 22%,color-mix(in srgb,var(--white) 55%,transparent),transparent),"
    "radial-gradient(1px 1px at 31% 48%,color-mix(in srgb,var(--white) 40%,transparent),transparent),"
    "radial-gradient(1px 1px at 57% 26%,color-mix(in srgb,var(--white) 50%,transparent),transparent),"
    "radial-gradient(1px 1px at 79% 52%,color-mix(in srgb,var(--white) 35%,transparent),transparent),"
    "radial-gradient(1px 1px at 92% 18%,color-mix(in srgb,var(--white) 45%,transparent),transparent),"
    # the sky's glow (.sky-view: --card at the middle of its foot, --bg to the sides) goes on, mirrored, and warms towards the mountains
    "linear-gradient(180deg,transparent 35%,color-mix(in srgb,var(--orange) 7%,transparent) 82%,color-mix(in srgb,var(--orange) 11%,transparent)),"
    "radial-gradient(120% 90% at 50% 0%,var(--card) 0%,var(--bg) 62%)}"
    ".sky-hz .sky-hz-k{position:absolute;z-index:2;left:50%;bottom:46px;transform:translateX(-50%);font-size:.7rem;letter-spacing:.16em;"
    "text-transform:uppercase;color:var(--orange);white-space:nowrap}"
    ".sky-hz ul{list-style:none;margin:0;padding:0}"
    ".sky-pl li{position:absolute;left:var(--x);bottom:0;transform:translateX(-50%)}"
    ".sky-pl a{display:flex;flex-direction:column;align-items:center;gap:.6rem;text-align:center}"
    ".sky-pl .o{display:block;width:var(--r);height:var(--r);border-radius:50%;overflow:hidden;margin-bottom:calc(var(--r) * -.32);"
    "box-shadow:0 0 0 1px color-mix(in srgb,var(--orange) 45%,transparent),0 0 34px 6px color-mix(in srgb,var(--orange) 22%,transparent);"
    "transition:transform .5s var(--ease),box-shadow .5s var(--ease)}"
    ".sky-pl .o img{width:100%;height:100%;object-fit:cover;filter:saturate(.85) brightness(.9);display:block}"
    ".sky-pl a:is(:hover,:focus-visible) .o{transform:translateY(-10px);box-shadow:0 0 0 1px var(--orange),0 0 46px 10px color-mix(in srgb,var(--orange) 34%,transparent)}"
    ".sky-st li{position:absolute;left:var(--x);top:var(--y)}"
    ".sky-st a{display:flex;align-items:center;gap:.55rem}"
    ".sky-st i{display:block;width:16px;height:16px;flex:none;background:var(--white);"
    "clip-path:polygon(50% 0,60% 40%,100% 50%,60% 60%,50% 100%,40% 60%,0 50%,40% 40%);"
    "filter:drop-shadow(0 0 6px color-mix(in srgb,var(--white) 70%,transparent));transition:transform .4s var(--ease)}"
    ".sky-st b{font-size:.85rem;font-weight:500}"
    ".sky-st a:is(:hover,:focus-visible) i{transform:scale(1.5) rotate(45deg);background:var(--orange)}"
    "@media (max-width:759px){.sky-mk{top:.8rem;left:.8rem;right:auto;gap:1rem}.sky-moon-o{width:52px;height:52px}"
    ".sky-moon-o::before{width:10px;height:10px;left:28px;top:12px}.sky-moon-o::after{width:6px;height:6px;left:14px;top:30px}"
    ".sky-atlas-o{width:40px;height:40px;margin-top:6px}.sky-mk b{font-size:.8rem}.sky-mk small{display:none}"
    ".sky-alt-sc{display:none}.sky-hz{height:300px}.sky-pl li{--r:58px!important}.sky-pl small{display:none}"
    ".sky-st li{left:var(--xs)!important;top:var(--ys)!important}"
    ".sky-hz .sky-hz-k{left:clamp(1.25rem,5vw,2rem);bottom:104px;transform:none}}"
    "@media (prefers-reduced-motion:reduce){.sky-moon-o,.sky-atlas-o,.sky-pl .o,.sky-st i{transition:none}}"
)


def landmarks(page):
    """The landmarks (see the docstring): the frame inside .sky-view and the horizon under it."""
    m = re.search(r"window\.SITEMAP_SKY = (\{.*?\});?\s*</script>", page, re.S)
    tree = json.loads(m.group(1))["tree"]
    by = {c["label"]: c for c in tree["children"]}
    E = lambda t: H_.escape(t, quote=True)
    kb = open(os.path.join(V4, "knowledge-base.html"), encoding="utf-8").read()
    alts = re.findall(r'<section class="clb-station" id="lvl-\d" data-alt="([^"]+)"', kb)
    cats = [c for c in by["Knowledge Base"]["children"] if c.get("kind") == "category"]
    az = os.path.join(V4, "knowledge-base", "encyclopedia", "index.html")
    n_q = None
    if os.path.exists(az):
        mm = re.search(r'<span><b>(\d+)</b>questions</span>', open(az, encoding="utf-8").read())
        n_q = mm.group(1) if mm else None
    globe = ('<svg class="sky-atlas-o" viewBox="0 0 64 64" aria-hidden="true"><circle class="g" cx="32" cy="32" r="30"/>'
             '<ellipse class="m" cx="32" cy="32" rx="12" ry="30"/><ellipse class="m" cx="32" cy="32" rx="24" ry="30"/>'
             '<path class="m" d="M2 32h60M7 17h50M7 47h50"/><circle class="p" cx="36" cy="18" r="2.4"/>'
             '<circle class="p" cx="26" cy="27" r="2"/><circle class="p" cx="40" cy="33" r="2"/><circle class="p" cx="30" cy="42" r="2.4"/></svg>')
    top = ('<div class="sky-mk"><!-- v4:needs knowledge-base/encyclopedia/atlas.html --><a href="knowledge-base/encyclopedia/atlas.html">%s'
           '<span><b>The Atlas</b><small>%s</small></span></a><!-- /v4:needs -->'
           '<a href="index.html"><span class="sky-moon-o" aria-hidden="true"></span><span><b>Home</b><small>Back to the start</small></span></a></div>'
           % (globe, ("%s questions, A to Z" % n_q) if n_q else "The encyclopedia"))
    lv = "".join('<li><a href="%s"><i>%s m</i><b>%s</b></a></li>' % (E(c["url"]), E(alts[i]) if i < len(alts) else "", E(c["label"]))
                 for i, c in reversed(list(enumerate(cats))))
    scale = ('<div class="sky-alt-sc"><a class="top" href="knowledge-base.html">Knowledge Base</a>'
             '<ol aria-label="The knowledge base, by level">%s</ol></div>' % lv)
    trips = [c for c in by["Trips"]["children"] if c.get("kind") == "trip"]
    xs, rs = ["16%", "38%", "62%", "84%"], ["104px", "124px", "112px", "96px"]
    pl = "".join('<li style="--x:%s;--r:%s"><a href="%s"><span><b>%s</b><small>%s</small></span><span class="o"><img src="%s" alt="" loading="lazy" decoding="async"></span></a></li>'
                 % (xs[i % 4], rs[i % 4], E(c["url"]), E(c["label"]), E(c.get("sub", "")), E(c.get("img", ""))) for i, c in enumerate(trips))
    named = [("about.html", "About Me", "4%", "12%", "6%", "8%"), ("mission.html", "Mission Statement", "26%", "26%", "52%", "8%"),
             ("partners.html", "Partner With Me", "49%", "10%", "6%", "22%"), ("record-attempt.html", "Speed Record", "72%", "24%", "52%", "22%")]
    st = ""
    for u, label, x, y, xs_, ys_ in named:
        li = '<li style="--x:%s;--y:%s;--xs:%s;--ys:%s"><a href="%s"><i aria-hidden="true"></i><b>%s</b></a></li>' % (x, y, xs_, ys_, u, E(label))
        st += ("<!-- v4:needs %s -->%s<!-- /v4:needs -->" % (u, li)) if u == "record-attempt.html" else li
    band = ('<div class="sky-hz"><a class="sky-hz-k" href="expeditions.html">Expeditions</a><ul class="sky-st">%s</ul>'
            '<ul class="sky-pl">%s</ul></div>' % (st, pl))
    out = re.sub(re.escape(MARKS_SKY[0]) + r".*?" + re.escape(MARKS_SKY[1]), "", page, flags=re.S)
    out = re.sub(re.escape(MARKS_BAND[0]) + r".*?" + re.escape(MARKS_BAND[1]), "", out, flags=re.S)
    view = '<div class="sky-view">'
    nav = '<nav class="sky-ground"'
    if out.count(view) != 1 or out.count(nav) != 1:
        fail("the sky's view or its ground is not there once")
    i = out.index(view) + len(view)
    out = out[:i] + MARKS_SKY[0] + "<style>%s</style>" % MARKS_CSS + top + scale + MARKS_SKY[1] + out[i:]
    j = out.index(nav)
    return out[:j] + MARKS_BAND[0] + band + MARKS_BAND[1] + out[j:]


def main():
    js = script()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    v = hashlib.sha256(js.encode("utf-8")).hexdigest()[:8]
    if os.path.exists(OLD_SVG):
        os.remove(OLD_SVG)     # the still layer of the first version
    html = open(PAGE, encoding="utf-8").read()
    # the credit, before the site schema
    block = ("<!--v4sky--><!-- The background stars are real (v4-sitemap-sky.js, its credit at its head): d3-celestial "
             "0.7.35, data/stars.6.json; star data XHIP (Anderson and Francis 2012, VizieR V/137D), converted by Olaf Frohn; "
             "BSD-3-Clause. --><!--/v4sky-->")
    html = re.sub(r"<!--v4sky-->.*?<!--/v4sky-->\n", "", html, flags=re.S)
    if html.count("<!-- site-schema -->") != 1:
        fail("no single <!-- site-schema --> in sitemap.html")
    html = html.replace("<!-- site-schema -->", block + "\n<!-- site-schema -->", 1)
    # the script: the v4 copy in place of the live one
    tag = '<script src="v4-sitemap-sky.js?v=%s"></script>' % v
    a, b = "<!--v4sky:js-->", "<!--/v4sky:js-->"
    if a in html:
        html = re.sub(re.escape(a) + ".*?" + re.escape(b), lambda m: a + tag + b, html, count=1, flags=re.S)
    else:
        html, n = re.subn(r'<script src="\.\./\.\./sitemap-sky\.js\?v=[0-9a-f]{8}"></script>', lambda m: a + tag + b, html)
        if n != 1:
            fail("the live sky script's tag is not in sitemap.html once")
    html = landmarks(ground(html))
    with open(PAGE, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("v4_sitemap_sky: %d real stars, in depth, behind the sitemap, and every page under it" % len(field()))


if __name__ == "__main__":
    main()
