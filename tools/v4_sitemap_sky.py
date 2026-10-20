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
"""
import hashlib
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
    with open(PAGE, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("v4_sitemap_sky: %d real stars, in depth, behind the sitemap" % len(field()))


if __name__ == "__main__":
    main()
