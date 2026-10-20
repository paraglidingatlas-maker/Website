#!/usr/bin/env python3
"""
The v4 sitemap's night sky from real stars (owner's queue, 20 Oct 2026, item 1).

The sitemap (prototypes/v4/sitemap.html) loads the LIVE sitemap-sky.js, which
is never edited here. That script draws its background field on the
.sky-stars canvas from a seeded random number generator, lets a shooting star
cross now and then on its own, and the episode stars twinkle on a loop
(sitemap.html's .sky-core animation). The episode stars and the series
constellations are the site's data and stay as they are.

This pass, on the v4 page only:

  - writes img/sitemap-stars.svg: the real sky, every star of STARS in
    tools/v4_record.py (the record page's data: positions and magnitudes from
    the npm package d3-celestial 0.7.35, data/stars.6.json, whose star data is
    XHIP: An Extended Hipparcos Compilation, Anderson and Francis 2012, VizieR
    V/137D, converted by Olaf Frohn; BSD-3-Clause, its notice is STAR_NOTE and
    goes inside the file with the data). The field is centred on Sirius's part
    of the sky (RA 95, Dec -25: Orion, Canis Major, Puppis and Carina), drawn
    looking up (east to the left) in a stereographic projection, each star a
    dot sized and lit by its magnitude. No lines, no names, no colour: a
    background, dimmer than the episode stars so they still lead;
  - shows it as a mask over the page's --white on a layer under the sky
    (.sky-view::before), so the colour is a token and the file stays a shape;
    it is drawn once by the browser and never moves;
  - hides the .sky-stars canvas, which takes the random field and the
    shooting star with it (the script still runs as it does live);
  - stops the episode stars' twinkle (.sky-core's loop): nothing moves on its
    own; the camera still glides in answer to the visitor.

The look is one <style> between <!--v4sky--> and <!--/v4sky--> right before
<!-- site-schema --> (v4_pwa puts its app block before </head> after this
runs), with the credit comment; rewritten whole each run, so the pass is
idempotent. It runs in tools/v4_build.py after v4_ux.
"""
import hashlib
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
PAGE = os.path.join(V4, "sitemap.html")
SVG = os.path.join(V4, "img", "sitemap-stars.svg")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from v4_record import STARS, STAR_NOTE   # noqa: E402

RA0, DEC0 = 95.0, -25.0      # the field's centre: Sirius's part of the sky
HW, HH = 1.75, 1.0           # half the field, in stereographic units (about 164 by 106 degrees across)
U = 1000                     # file units per stereographic unit
PX = 0.41                    # screen pixels per file unit at 1440 by 750, the sky's usual desktop size (cover)


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


def look(mag):
    """Radius (screen px at desktop) and opacity by magnitude: -1.4 is 1.7 px at 0.8, 4.6 is 0.55 px at 0.22."""
    t = max(0.0, min(1.0, (mag + 1.5) / 6.1))
    return 1.7 - 1.15 * t, 0.8 - 0.58 * t


def svg():
    groups = {}
    for row in STARS.split():
        ra, dec, mag, _bv = (float(v) for v in row.split(","))
        p = project(ra, dec)
        if not p or abs(p[0]) > HW + 0.02 or abs(p[1]) > HH + 0.02:
            continue
        r, o = look(mag)
        key = (round(r * 2 / PX), round(o, 2))     # stroke width in file units (a dot is a round-capped zero-length line)
        groups.setdefault(key, []).append("M%d %dh0" % (round(p[0] * U), round(p[1] * U)))
    body = "".join('<path stroke-width="%d" stroke-opacity="%s" d="%s"/>' % (w, ("%.2f" % o).lstrip("0"), "".join(v))
                   for (w, o), v in sorted(groups.items()))
    n = sum(len(v) for v in groups.values())
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%d %d %d %d" width="%d" height="%d">\n'
            % (-HW * U, -HH * U, 2 * HW * U, 2 * HH * U, HW * U, HH * U)
            + STAR_NOTE.replace("<!-- ", "<!-- The real sky behind the v4 sitemap (tools/v4_sitemap_sky.py): %d stars "
                                "to magnitude 4.6 about RA 95, Dec -25, looking up. " % n) + "\n"
            + '<g fill="none" stroke="#fff" stroke-linecap="round">' + body + "</g>\n</svg>\n"), n


def main():
    data, n = svg()
    with open(SVG, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)
    v = hashlib.md5(data.encode()).hexdigest()[:8]
    block = ("<!--v4sky--><!-- The background stars are real (img/sitemap-stars.svg, its credit inside): d3-celestial "
             "0.7.35, data/stars.6.json; star data XHIP (Anderson and Francis 2012, VizieR V/137D), converted by Olaf Frohn; "
             "BSD-3-Clause. --><style>"
             ".sky-view::before{content:\"\";position:absolute;inset:0;pointer-events:none;background:var(--white);"
             "-webkit-mask:url(img/sitemap-stars.svg?v=%s) center/cover no-repeat;mask:url(img/sitemap-stars.svg?v=%s) center/cover no-repeat;}"
             ".sky-stars{display:none;}"
             ".sky-core{animation:none;}"
             "</style><!--/v4sky-->" % (v, v))
    html = open(PAGE, encoding="utf-8").read()
    html = re.sub(r"<!--v4sky-->.*?<!--/v4sky-->\n", "", html, flags=re.S)
    if html.count("<!-- site-schema -->") != 1:
        raise SystemExit("v4_sitemap_sky: no single <!-- site-schema --> in sitemap.html")
    html = html.replace("<!-- site-schema -->", block + "\n<!-- site-schema -->", 1)
    with open(PAGE, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("v4_sitemap_sky: %d real stars behind the sitemap" % n)


if __name__ == "__main__":
    main()
