#!/usr/bin/env python3
"""
The speed record attempt page, for sponsors (owner, 17 Oct 2026): "a page for
the WR attempt I'll be doing ... avg speed over a course for 100 km and 200 km
out and return ... professional and elegant so that sponsors find it
interesting". On the first build he said "The design feels very robotic, too
much text, difficult to navigate, make it stunning", and then "Add elements
which awwwards worthy websites use".

    prototypes/v4/record-attempt.html

The design is option A, "Cinematic story" (tools/v4_record_a.py, the judges'
winner over B and C, which stay as options for the owner), with what the
judges asked to graft from B and C and every fix they listed:
  - the opening: the masked three-line title, and on the first screen the two
    numbers (the mark to beat and his best, "about", "not a record course")
    beside the window, with one way straight down to the offer (B). On phones
    the photograph sits above the words so the type is on dark ground;
  - a chapter bar with every chapter's name, a reading line per chapter and a
    solid Partner button (B, C): along the top on wide screens (below the
    site menu when it comes back), along the bottom on phones;
  - 01 the mark: an outlined 35.94 against a solid orange "about 36", the
    sources beside the numbers (B), "The time to beat" line and a fold with
    the detail behind the numbers (C);
  - 02 the course: pinned and flown kilometre by kilometre with the scroll, as
    a hairpin out and back with a glider, Leg, Flown and two clocks counting
    the same way (B), watch-face figures and a giant outlined kilometre
    count behind (C), a 100 / 200 km switch that works without JavaScript
    (two radio buttons and :has, B);
  - 03 Kerio Valley: the photograph seen through its name (with a plain
    fallback fill, so the name never vanishes), the full-bleed valley plate,
    the thermals as a vario gauge (B);
  - 04 the window: the 26 days drawn as two expedition blocks with the gap,
    "During" once across both (B, C), and the before and after as a strip
    moved sideways by the scroll on wide screens, a swipe row on phones;
  - 05 the audience and 06 the offer: the counts, the portrait, the tiers with
    outlined 01 02 03 numerals and an orange edge on the Title Partner (C).

Facts only, each from a source named on the page or already on the site:
  - the owner's flight: UP Paragliders news, "Almost 200km with an average of
    36kph": 6 Feb 2025, Kenya, 198.86 km on XContest, about 36 km/h, on a UP
    Trango X (EN C). The page never calls it a record or a record course.
  - the marks to beat: FAI CIVL records list (class O-3, speed over an
    out-and-return course of 100 km: 35.94 km/h, Michel Macquet, FRA, 23 Jan
    2025, shown in one FAI listing as a claim under review and in another as
    the record, so its status is "[to confirm]"; 200 km: not found, so
    "[to supply]"). The FAI pages cannot be opened from the build machine:
    check them before the page goes out. The claim goes to the FAI under the
    Sporting Code, Section 7D.
  - times are distance over speed: 100 km at 35.94 or at 36 km/h, 2 h 47 min;
    200 km at 36 km/h, 5 h 33 min.
  - Kerio Valley, its place, season, thermals and flights: the Kenya page.
    The window, 18 Jan to 12 Feb 2027, is flown alongside the two Kenya
    expeditions (18 to 29 Jan, 1 to 12 Feb 2027).
  - audience: the v4 partners page (100,000+ streams, 130+ countries, 80
    interviews, 10+ years, a newsletter about four times a month).
  - the partnership options are the owner's offer, drafted as asked; prices
    stay in the media kit.
  - still to supply: the wing and instruments, the team and the FAI
    observer, the preparation.
  - photographs: only the site's own; each alt is the one the Kenya or
    partners page gives it, and only kerio-valley is shown as Kerio Valley.

Motion only answers the visitor (scroll, pointer, tap, key); nothing loops or
runs on a timer. Reduced motion shows every finished state, unpinned; with
JavaScript off everything is readable and the switch still works; phones get
the simplest version. No libraries, no video.

The backgrounds (owner, 18 to 19 Oct 2026: "The background of the winning
page looks quite bland"; he chose option 2, "be creative, and use something
from online as well if needed"). No photographs of pilots, people or stock
paragliding: the page makes its own atmosphere, one record day over Kerio
Valley from first light to night, moved on by the scroll. Second pass (19
Oct), after two reviews of the first: midday read as a flat slate and its sun
as a stain, the clouds as smoke, morning and dusk alike, the relief as blur,
the escarpment as steps, and the scroll was much slower than before.
  - the brightness limit: no pixel of the sky, and nothing drawn on it, is
    let past SKY_CAP (relative luminance 0.044, with a soft knee), which
    keeps 4.5:1 for the muted small words (--wr-dim, 4.5:1 up to 0.050) and
    for --gray-light body text (up to 0.0624). So light comes from contrast,
    not level: deep, saturated skies, and the light gathered where it falls;
  - the sky: one fixed canvas pair behind the page. The sky itself is painted
    small (one pixel for every seven to fourteen on screen) in linear light
    from the design tokens (the site's --sky-cool follows the visitor's clock,
    so the page's blues do too) and stretched by the browser; over it one
    canvas draws everything else on the sky, composed again only when
    something on it has moved. Pre-dawn under the stars; dawn cool overhead
    with a rose band and the Earth's shadow to the right and a narrow pale
    line of light low on the LEFT, where the sun comes up behind the Tugen
    Hills and lights the escarpment's east face (right); a deep blue
    morning; midday deep and saturated, darker at the sides, its light
    falling from the top edge with the sun overhead and out of sight (no
    disc between about 09:00 and 15:00), a pale haze along the horizon; a
    warm afternoon; dusk on the RIGHT, saturated orange behind the
    escarpment, its edge rimmed, its face in shadow, violet above, the Tugen
    Hills' west slopes in the afterglow; then night;
  - the sun: where it really is that day (6 Feb 2027, in the window, at the
    page's 0.72N 35.65E: declination -15.6, solar noon 12:51 EAT, up about
    06:52, down about 18:51), seen looking south down the valley; a hazy
    disc only when low, rising and setting half behind the hills' own line;
  - the stars: the real sky over Kerio Valley that day, at 05:30 for the
    opening and 19:00 for the close, turning about the south celestial pole
    as the scroll moves the clock on (15 degrees an hour), beginning under
    the opening photograph (nothing of the sky shows through the pilot).
    No lines between them, no names. Positions and magnitudes (STARS) are
    from the npm package d3-celestial 0.7.35 (see its notice below), whose
    star data is XHIP: An Extended Hipparcos Compilation (Anderson and
    Francis 2012, VizieR V/137D), converted to GeoJSON at J2000 by Olaf
    Frohn. The Milky Way is not taken from the package: it is drawn here
    (img/record/mw-dawn.webp, mw-night.webp) from the galactic plane, in
    the stars' own projection (see make_images): an impression;
  - the horizon: the Elgeyo escarpment (right) as a fault scarp, a long,
    nearly level plateau edge running away to the valley's end with 1/f
    roughness, a steep face with gullies of uneven width and spacing; the
    rounder Tugen Hills (left) by 1/f midpoint displacement; a farther range
    and the far hills lighter; the phone has its own drawing with fewer,
    larger features. Seeded geometry, not a survey. It steps aside while the
    course is flown on its map, stands in midday's haze, keeps clear of the
    opening photograph and the partner cards (and half steps down for the
    01 numerals), and on tablets and phones stands on the chapter bar;
  - clouds, at three depths, each fetched only as it comes near (phones get
    copies half the size): far, a midday cloud street along the escarpment
    (fair-weather cumulus with their bases at one height, so in perspective
    they fall in line toward the valley's end), drifting slower than the
    page; between, a dusk cloud passing from 05 into 06, lit from below by
    the set sun and behind the hills; near, a cumulus passing from 02 into
    03 faster than the page, in front of them. All are drawn with one colour
    held at the brightness limit through a greyscale mask, so a cloud can
    only lighten its sky, never darken it into a smudge. The cumulus are
    built here (make_images) from seeded lobes, broken and textured by the
    Kenya page's own cloud layer (assets/destinations/kenya/clouds/
    cloud-1.webp); the dusk cloud is a band of cloud-4.webp, its edges
    sharpened and its undersides lit (img/record/street-*, cu-*, dusk-*);
  - 01 the mark: two thermals in the gutters, soft sinuous streamlines and
    at most two bubbles each, leaning with the wind, of different heights,
    faded through their own strokes; each rises faster than the page as one
    layer (phones keep the right-hand one);
  - 02 the course: Kenya's ground under the line, as form lines traced
    (marching squares) from the chart sheet's shaded relief
    (assets/destinations/kenya/map/kenya-sheet-terrain.webp), so lines of
    equal shade, smoothed: form lines, not surveyed contours. Cut round
    Kerio Valley and turned a quarter so the Rift runs along the course,
    each level faintly filling the land above it (terraces); vector, crisp
    at every width (img/record/ground.svg), sliding under the glider out and
    back, with the glider's shadow on it;
  - the page's still grain lies in the page itself, over the sky.
Without JavaScript, and with reduced motion, the same day is one still
gradient down the whole page (its stops in STILL; every stop under the same
limit with each of the site's four skies), the horizon drawn at the start of
01, the start of 06 and the close (from the same paths), with the night's
stars over the last. Nothing moves.
Muted small words (the markers, chapter numbers, sources) are lifted from
--gray to a mix of --gray-light and --gray, so they keep 4.5:1 on a sky. The
partner cards are solid, so neither sky nor hills show through the offer.
The image files are made by `python3 tools/v4_record.py --images` (numpy,
Pillow and contourpy), from the site's own files and the geometry here;
nothing in them comes from online. Second-pass files in img/record/: ground.svg,
street-l/-s, cu-l/-s, dusk-l/-s and mw-dawn, mw-night (the first pass's
relief, contour and cloud-N masks are gone).

The page takes the v4 shell (head, menu, footer) from partners.html and is
prototype-only (tools/v2_site.py PROTO_ONLY) until the owner approves it.

    python3 tools/v4_record.py
"""
import datetime
import json
import math
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "partners.html")
OUT = os.path.join(V4, "record-attempt.html")

TITLE = "The Speed Record Attempt"
DESC = ("Aninder Singh's attempt on two paragliding world records for speed, over a 100 km "
        "and a 200 km out-and-return course, from Kerio Valley, Kenya, between 18 January "
        "and 12 February 2027, and how to partner on it.")
URL = "https://paraglidingatlas.com/record-attempt.html"
OG_IMG = "https://paraglidingatlas.com/assets/destinations/kenya/gallery/kenya-hero.jpg"

# the marks (see the docstring for where each comes from)
REC100 = 35.94      # km/h, the 100 km mark to beat, status to confirm
BEST = 36           # km/h, about, over 198.86 km (not a record course)

MAIL = "mailto:aninder@paraglidingatlas.com?subject=Partnering%20on%20the%20speed%20record%20attempt"
UP_NEWS = "https://www.up-paragliders.com/news/almost-200km-with-an-average-of-36kph"
FAI_LIST = "https://www.fai.org/page/civl-records"
FAI_CODE = "https://www.fai.org/sites/default/files/civl/documents/sporting_code_s7_d_-_records_and_badges_2025.pdf"

A = "../../assets/"
IMG = {
    "hero": (A + "destinations/kenya/gallery/kenya-hero", 1400, 788, "Paragliding in Kenya"),
    "kerio": (A + "destinations/kenya/hero/kerio-valley", 1152, 768, "Paragliding at Kerio Valley, Kenya"),
    "kerio_p": ("img/hero/kenya-kerio-valley-p", 512, 768, "Paragliding at Kerio Valley, Kenya"),
    "high": (A + "destinations/kenya/gallery/kenya-high", 1400, 933, "Paragliding in Kenya"),
    "aninder": (A + "images/partners-aninder", 720, 900, "Aninder Singh"),
    "icare": (A + "images/partners-coupe-icare-wide", 1920, 1372,
              "Aninder shaking hands with a brand representative at a harness test stand, "
              "camera in hand, at Coupe Icare"),
}

TBD = '<span class="wr-tbd">[to supply]</span>'
TBC = '<span class="wr-tbd">[to confirm]</span>'

# the course drawing, in a 1000 x 200 box stretched to the width: km out from
# the start to x; the out leg on YO, home on YB, the turn a half ellipse whose
# far point is the turnpoint itself (so the drawing stays to scale)
X0, PX_PER_KM = 30, 9.5
YO, YB, RX = 50, 150, 40
RY = (YB - YO) / 2
CY = (YO + YB) / 2

# the chapters: (id, number, name in the bar)
CHAPTERS = [("wr-mark", "01", "Mark"), ("wr-course", "02", "Course"), ("wr-kerio", "03", "Kerio"),
            ("wr-window", "04", "Window"), ("wr-audience", "05", "Audience")]

EXT = ('<svg class="wr-ext" viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
       '<path d="M3.5 2.5h6v6M9.5 2.5l-7 7" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')
DOWN = ('<svg viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M7 1v11M2.5 7.5 7 12l4.5-4.5" '
        'fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')


def X(km):
    return X0 + km * PX_PER_KM


def pct(km):
    return "%g%%" % (X(km) / 10)


def mins(km, kmh):
    return int(round(km / kmh * 60))


def hm(km, kmh):
    m = mins(km, kmh)
    return "%d h %02d min" % (m // 60, m % 60)


def clock(km, kmh):
    """The watch-face figures: large numerals, a small h and min."""
    m = mins(km, kmh)
    return "<b>%d</b><small>h</small> <b>%02d</b><small>min</small>" % (m // 60, m % 60)


def pic(key, cls="", lazy=True, fetch=False):
    base, w, h, alt = IMG[key]
    att = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if fetch else "")
    return ('<picture%s><source srcset="%s.webp" type="image/webp"><img src="%s.jpg" width="%d" height="%d" alt="%s"%s></picture>'
            % (' class="%s"' % cls if cls else "", base, base, w, h, alt, att))


def kin(text):
    """A headline that rises word by word: each word in its own mask."""
    out = []
    for i, w in enumerate(text.split(" ")):
        out.append('<span class="wr-w"><span style="--i:%d">%s</span></span>' % (i, w))
    return " ".join(out)


def count(final, to, dec=0, comma=False, suf=""):
    return ('<span class="wr-count" data-final="%s" data-count="%s" data-dec="%d"%s%s><span>%s</span></span>'
            % (final, to, dec, ' data-comma="1"' if comma else "", ' data-suf="%s"' % suf if suf else "", final))


def ext(href, text, hidden=""):
    return ('<a class="wr-u" href="%s" target="_blank" rel="noopener">%s%s%s</a>'
            % (href, text, '<span class="wr-vh">%s</span>' % hidden if hidden else "", EXT))


# ---------- the record day's sky (see the docstring) ----------
SKY_LON, SKY_LAT = 35.65, 0.72          # Kerio Valley, as the page gives it
SKY_AT = {"dawn": datetime.datetime(2027, 2, 6, 2, 30),    # UTC: 05:30 in Kenya (UTC+3)
          "night": datetime.datetime(2027, 2, 6, 16, 0)}   # UTC: 19:00 in Kenya
SUN_DEC, SUN_NOON = -15.6, 12.86        # that day: the sun's declination, and solar noon at Kerio Valley (EAT, hours)
SKY_CAP = 0.044                         # no pixel of the painted sky brighter than this relative luminance
BOX = (-3.0, 3.0, -2.25, 0.75)          # the drawn sky in projection units: the horizon at y 0, the zenith near y -2
REC_IMG = "img/record/"
# Stars to magnitude 4.6 that can show in BOX at either time, as "ra,dec,mag,b-v" (degrees, J2000), taken
# from data/stars.6.json of the npm package d3-celestial 0.7.35 (npm pack d3-celestial@0.7.35; tarball SHA-1
# bee03f337ac1ae3d32de2c3bd7d7ae4dd27e1e21; its package.json gives "license": "BSD-3-Clause"). Its readme
# credits the star data to XHIP: An Extended Hipparcos Compilation, Anderson E., Francis C. (2012), VizieR
# V/137D, converted to GeoJSON at J2000 by Olaf Frohn. The package's notice, as its LICENSE gives it:
#
#   Copyright (c) 2015, Olaf Frohn
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without modification, are permitted provided
#   that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#   following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
#   the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
#   promote products derived from this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
#   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#   PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
#   DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#   HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#   POSSIBILITY OF SUCH DAMAGE.
#
# The page carries the same credit and notice in an HTML comment beside the star data (STAR_NOTE).
STARS = """
101.29,-16.72,-1.44,0.01 95.99,-52.70,-0.62,0.16 219.90,-60.83,-0.01,0.71 78.63,-8.20,0.18,-0.03
114.83,5.22,0.40,0.43 24.43,-57.24,0.45,-0.16 88.79,7.41,0.45,1.50 210.96,-60.37,0.61,-0.23
297.70,8.87,0.76,0.22 186.65,-63.10,0.77,-0.24 201.30,-11.16,0.98,-0.23 247.35,-26.43,1.06,1.86
116.33,28.03,1.16,0.99 344.41,-29.62,1.17,0.14 191.93,-59.69,1.25,-0.24 219.90,-60.84,1.35,0.90
152.09,11.97,1.36,-0.09 104.66,-28.97,1.50,-0.21 187.79,-57.11,1.59,1.60 263.40,-37.10,1.62,-0.23
81.28,6.35,1.64,-0.22 138.30,-69.72,1.67,0.07 84.05,-1.20,1.69,-0.18 332.06,-46.96,1.73,-0.07
85.19,-1.94,1.74,-0.20 122.38,-47.34,1.75,-0.14 276.04,-34.38,1.79,-0.03 107.10,-26.39,1.83,0.67
125.63,-59.51,1.86,1.20 264.33,-43.00,1.86,0.41 252.17,-69.03,1.91,1.45 99.43,16.40,1.93,0.00
131.18,-54.71,1.93,0.04 306.41,-56.74,1.94,-0.12 95.67,-17.96,1.98,-0.24 141.90,-8.66,1.99,1.44
154.99,19.84,2.01,1.13 10.90,-17.99,2.04,1.02 283.82,-26.30,2.05,-0.13 211.67,-36.37,2.06,1.01
86.94,-9.67,2.07,-0.17 340.67,-46.88,2.07,1.61 2.10,29.09,2.07,-0.04 263.73,12.56,2.08,0.15
177.26,14.57,2.14,0.09 190.38,-48.96,2.20,-0.02 120.90,-40.00,2.21,-0.27 139.27,-59.28,2.21,0.19
137.00,-43.43,2.23,1.67 83.00,-0.30,2.25,-0.17 204.97,-53.47,2.29,-0.17 240.08,-22.62,2.29,-0.12
252.54,-34.29,2.29,1.14 220.48,-47.39,2.30,-0.15 218.88,-42.16,2.33,-0.16 326.05,9.88,2.38,1.52
265.62,-39.03,2.39,-0.17 6.57,-42.31,2.40,1.08 257.59,-15.72,2.43,0.06 345.94,28.08,2.44,1.66
111.02,-29.30,2.45,-0.08 140.53,-55.01,2.47,-0.14 346.19,15.21,2.49,-0.00 249.29,-10.57,2.54,0.04
45.57,4.09,2.54,1.63 208.88,-47.29,2.55,-0.18 168.53,20.52,2.56,0.13 241.36,-19.81,2.56,-0.07
83.18,-17.82,2.58,0.21 182.09,-50.72,2.58,-0.13 183.95,-17.54,2.58,-0.11 285.65,-29.88,2.60,0.06
229.25,-9.38,2.61,-0.07 236.07,6.43,2.63,1.17 84.91,-34.07,2.65,-0.12 188.60,-23.40,2.65,0.89
224.63,-43.13,2.68,-0.18 161.69,-49.42,2.69,0.90 189.30,-69.14,2.69,-0.18 262.69,-37.30,2.70,-0.18
109.29,-37.10,2.71,1.62 275.25,-29.83,2.72,1.38 296.56,10.61,2.72,1.51 243.59,-3.69,2.73,1.58
160.74,-64.39,2.74,-0.22 190.42,-1.45,2.74,0.37 83.86,-5.91,2.75,-0.21 200.15,-36.71,2.75,0.07
222.72,-16.04,2.75,0.15 265.87,4.57,2.76,1.17 258.66,14.39,2.78,1.16 76.96,-5.09,2.78,0.16
183.79,-58.75,2.79,-0.19 233.79,-41.17,2.80,-0.22 82.06,-20.76,2.81,0.81 6.44,-77.25,2.82,0.62
248.97,-28.22,2.82,-0.21 276.99,-25.42,2.82,1.02 121.89,-24.30,2.83,0.46 238.79,-63.43,2.83,0.32
3.31,15.18,2.83,-0.19 261.32,-55.53,2.84,1.48 262.96,-49.88,2.84,-0.14 326.76,-16.13,2.85,0.18
29.69,-61.57,2.86,0.29 229.73,-68.68,2.87,0.01 334.63,-60.26,2.87,1.39 95.74,22.51,2.87,1.62
44.57,-40.30,2.88,0.13 287.44,-21.02,2.88,0.38 111.79,8.29,2.89,-0.10 239.71,-26.11,2.89,-0.18
245.30,-25.59,2.90,0.30 322.89,-5.57,2.90,0.83 146.78,-65.07,2.92,0.27 102.48,-50.61,2.94,1.21
187.47,-16.52,2.94,-0.01 331.45,-0.32,2.95,0.97 146.46,23.77,2.97,0.81 59.51,-13.51,2.97,1.59
271.45,-30.42,2.98,0.98 199.73,-23.17,2.99,0.92 266.90,-40.13,2.99,0.51 286.35,13.86,2.99,0.01
252.97,-38.05,3.00,-0.20 328.48,-37.36,3.00,-0.08 95.08,-30.06,3.02,-0.16 105.76,-23.83,3.02,-0.08
182.53,-22.62,3.02,1.33 191.57,-68.11,3.04,-0.18 305.25,-14.78,3.05,0.79 100.98,25.13,3.06,1.38
274.41,-36.76,3.10,1.58 133.85,5.95,3.11,0.98 162.41,-16.19,3.11,1.23 173.95,-63.02,3.11,-0.04
309.39,-47.29,3.11,1.00 87.74,-35.77,3.12,1.15 254.66,-55.99,3.12,1.55 258.76,24.84,3.12,0.08
224.79,-42.10,3.13,-0.21 142.81,-57.03,3.16,1.54 99.44,-43.20,3.17,-0.10 281.41,-26.99,3.17,-0.11
220.63,-64.98,3.18,0.26 76.37,-22.37,3.19,1.46 254.42,9.38,3.19,1.16 267.46,-37.04,3.19,1.19
72.46,6.96,3.19,0.48 230.34,-40.65,3.22,-0.23 244.58,-4.69,3.23,0.97 275.33,-2.90,3.23,0.94
102.05,-61.94,3.24,0.23 302.83,-0.82,3.24,-0.07 112.31,-43.30,3.25,1.51 211.59,-26.68,3.25,1.09
226.02,-25.28,3.25,1.67 56.81,-74.24,3.26,1.59 260.50,-25.00,3.27,-0.19 343.66,-15.82,3.27,0.07
78.23,-16.21,3.29,-0.11 153.43,-70.04,3.29,-0.07 68.50,-55.05,3.30,-0.08 158.01,-61.69,3.30,-0.09
261.35,-56.38,3.31,-0.15 93.72,22.51,3.31,1.60 16.52,-46.72,3.32,0.89 258.04,-43.24,3.32,0.44
269.76,-9.77,3.32,0.99 286.74,-27.67,3.32,1.17 63.61,-62.47,3.33,0.92 168.56,15.43,3.33,-0.00
117.32,-24.86,3.34,1.22 101.32,12.90,3.35,0.44 81.12,-2.40,3.35,-0.24 291.37,3.11,3.36,0.32
230.67,-44.69,3.37,-0.19 131.69,6.42,3.38,0.69 203.67,-0.60,3.38,0.11 154.27,-61.33,3.39,1.54
193.90,3.40,3.39,1.57 83.78,9.93,3.39,-0.16 22.09,-43.32,3.41,1.54 207.38,-41.69,3.41,-0.23
228.07,-52.10,3.41,0.92 340.37,10.83,3.41,-0.09 240.03,-38.40,3.42,-0.21 266.61,27.72,3.42,0.75
311.24,-66.20,3.42,0.16 137.74,-58.97,3.43,-0.19 154.17,23.42,3.43,0.31 286.56,-4.88,3.43,-0.10
119.19,-52.98,3.46,-0.18 17.15,-10.18,3.46,1.16 207.40,-42.47,3.47,-0.17 40.83,3.24,3.47,0.09
151.83,16.76,3.48,-0.03 105.43,-27.93,3.49,1.73 276.74,-45.97,3.49,-0.18 342.14,-51.32,3.49,0.08
26.02,-15.94,3.49,0.73 102.46,-32.51,3.50,-0.12 110.03,21.98,3.50,0.37 299.69,19.49,3.51,1.57
342.50,24.60,3.51,0.93 145.29,9.89,3.52,0.52 149.22,-54.57,3.52,-0.07 284.43,-21.11,3.52,1.15
55.81,-9.76,3.52,0.92 332.55,6.20,3.52,0.09 124.13,9.19,3.53,1.48 173.25,-31.86,3.54,0.95
237.41,-3.43,3.54,-0.04 264.40,-15.40,3.54,0.26 64.47,-33.80,3.55,-0.11 86.74,-14.82,3.55,0.10
214.85,-46.06,3.55,-0.18 302.18,-66.18,3.55,0.75 34.13,-51.51,3.56,-0.12 169.84,-14.78,3.56,1.11
253.08,-38.02,3.56,-0.21 4.86,-8.82,3.56,1.21 116.11,24.40,3.57,0.93 230.45,-36.26,3.57,1.53
109.52,16.54,3.58,0.11 304.51,-12.54,3.58,0.88 86.12,-22.45,3.59,0.48 177.67,1.76,3.59,0.52
185.34,-60.40,3.59,1.39 79.40,-6.84,3.59,-0.12 130.07,-52.92,3.60,-0.17 142.68,-40.47,3.60,0.37
234.26,-28.14,3.60,1.36 262.77,-60.68,3.60,-0.10 21.01,-8.18,3.60,1.06 152.65,-12.35,3.61,1.01
195.57,-71.55,3.61,1.19 266.43,-64.72,3.61,1.16 116.31,-37.97,3.62,1.71 253.65,-42.36,3.62,1.39
176.40,-66.73,3.63,0.16 309.39,14.60,3.64,0.42 271.66,-50.09,3.65,-0.10 337.21,-0.02,3.65,0.41
234.66,-29.78,3.66,-0.18 313.70,-58.45,3.67,1.25 130.90,-33.19,3.68,-0.18 296.85,18.53,3.68,1.31
347.36,-21.17,3.68,1.20 72.80,5.61,3.68,-0.16 28.99,-51.61,3.69,0.84 146.31,-62.51,3.69,1.01
325.02,-16.66,3.69,0.32 269.44,29.25,3.70,0.94 49.88,-21.76,3.70,1.61 349.29,3.28,3.70,0.92
89.10,-14.17,3.71,0.34 118.05,-40.58,3.71,1.01 237.70,4.48,3.71,0.15 271.84,9.56,3.71,0.16 298.83,6.41,3.71,0.85
73.56,2.44,3.71,-0.18 53.23,-9.46,3.72,0.88 221.56,1.89,3.73,-0.01 325.37,-77.39,3.73,1.01
343.15,-7.58,3.73,1.63 27.87,-10.34,3.74,1.14 136.04,-47.10,3.75,1.17 266.97,2.71,3.75,0.04
83.41,-62.49,3.76,0.64 87.83,-20.88,3.76,0.98 97.20,-7.03,3.76,-0.11 286.17,-21.74,3.76,1.01
84.69,-2.60,3.77,-0.19 126.43,-66.14,3.77,1.13 130.16,-46.65,3.77,0.67 252.45,-59.04,3.77,1.56
309.91,15.91,3.77,-0.06 321.67,-22.41,3.77,1.00 107.19,-70.50,3.78,1.01 163.37,-58.85,3.78,0.94
311.92,-9.50,3.78,0.00 111.43,27.80,3.78,1.02 114.71,-26.80,3.80,-0.16 233.70,10.54,3.80,0.27
48.02,-28.99,3.80,0.54 68.89,-30.56,3.81,0.96 156.97,-58.74,3.81,0.32 247.73,1.98,3.82,0.02 30.51,2.76,3.82,0.02
156.52,-16.84,3.83,1.46 209.57,-42.10,3.83,-0.22 221.97,-79.04,3.83,1.43 56.05,-64.81,3.84,1.13
133.76,-60.64,3.84,-0.10 158.20,9.31,3.84,-0.15 159.33,-48.23,3.84,0.30 188.12,-72.13,3.84,-0.16
271.89,28.76,3.84,-0.02 273.44,-21.06,3.84,0.20 63.50,-42.29,3.85,1.08 86.82,-51.07,3.85,0.17
95.53,-33.44,3.85,0.86 153.68,-42.12,3.85,0.05 189.43,-48.54,3.85,0.05 275.92,21.77,3.85,1.17
278.80,-8.24,3.85,1.32 82.80,-35.47,3.86,1.13 243.86,-63.69,3.86,1.10 248.36,-78.90,3.86,0.92
69.55,-14.30,3.86,1.08 335.41,-1.39,3.86,-0.06 131.51,-46.04,3.87,0.01 209.67,-44.80,3.87,-0.21
220.77,-5.66,3.87,0.39 239.22,-29.21,3.87,-0.20 298.12,1.01,3.87,0.63 2.35,-45.75,3.88,1.01
148.19,26.01,3.88,1.22 227.98,-48.74,3.88,-0.03 347.59,-45.25,3.88,1.00 103.53,-24.18,3.89,1.74
138.59,2.31,3.89,-0.06 184.98,-0.67,3.89,0.03 44.11,-8.90,3.89,1.09 144.96,-1.14,3.90,1.31
170.25,-54.49,3.90,-0.16 202.76,-39.41,3.90,1.19 126.42,-3.91,3.91,-0.01 187.01,-50.23,3.91,-0.19
226.28,-47.05,3.91,-0.14 233.88,-14.79,3.91,1.01 60.79,5.99,3.91,0.03 290.42,-17.85,3.92,0.23
318.96,5.25,3.92,0.55 6.55,-43.68,3.93,0.17 22.81,-49.07,3.93,0.97 115.46,-72.61,3.93,1.03
167.15,-58.98,3.93,1.23 241.70,-20.67,3.93,-0.05 270.16,2.93,3.93,0.03 69.08,-3.35,3.93,-0.21
17.10,-55.25,3.94,-0.12 115.31,-9.55,3.94,1.02 115.95,-28.95,3.94,0.16 131.17,18.15,3.94,1.08
99.17,-19.26,3.95,1.04 89.79,-42.82,3.96,1.15 137.82,-62.32,3.96,-0.18 290.66,-44.46,3.96,-0.09
290.97,-40.62,3.96,-0.10 350.74,-20.10,3.96,1.08 66.01,-34.02,3.97,1.47 109.21,-67.96,3.97,0.76
130.03,-35.31,3.97,0.94 182.91,-52.37,3.97,-0.16 237.74,-33.63,3.97,-0.04 300.15,-72.91,3.97,-0.03
337.32,-43.50,3.97,1.02 341.63,23.57,3.97,1.07 93.71,-6.27,3.99,1.32 156.10,-74.03,3.99,0.37
349.36,-58.24,3.99,0.41 30.00,-21.08,3.99,1.55 135.61,-66.40,4.00,0.14 170.98,10.53,4.00,0.42
243.00,-19.46,4.00,0.08 106.03,20.57,4.01,0.90 108.70,-26.77,4.01,-0.15 220.49,-37.79,4.01,-0.16
244.96,-50.16,4.01,1.08 280.76,-71.43,4.01,1.13 71.38,-3.25,4.01,-0.15 132.63,-27.71,4.02,1.27
182.10,-24.73,4.02,0.33 284.91,15.07,4.02,1.08 285.42,-5.74,4.02,1.08 193.65,-57.18,4.03,-0.18
271.36,2.50,4.03,0.86 308.30,11.30,4.03,-0.12 359.83,6.86,4.03,0.42 176.46,6.53,4.04,1.50 62.97,-6.84,4.04,0.33
338.84,-0.12,4.04,-0.08 124.63,-76.92,4.05,0.41 131.10,-42.65,4.05,0.87 170.28,6.03,4.05,-0.06
215.14,-37.89,4.05,-0.03 219.47,-49.43,4.05,-0.15 342.40,-13.59,4.05,1.57 171.22,-17.68,4.06,0.22
184.39,-67.96,4.06,1.60 184.61,-64.00,4.06,-0.17 220.91,-35.17,4.06,1.36 254.90,-53.16,4.06,1.45
113.98,26.90,4.06,1.54 214.00,-6.00,4.07,0.51 227.21,-45.28,4.07,-0.16 229.38,-58.80,4.07,0.09
35.44,-68.66,4.08,0.03 103.55,-12.04,4.08,1.42 143.61,-59.23,4.08,-0.01 164.94,-18.30,4.08,1.08
316.49,-17.23,4.08,-0.01 320.52,19.80,4.08,1.11 39.87,0.33,4.08,-0.21 45.60,-23.62,4.08,0.16
84.23,9.29,4.09,0.95 117.31,-46.37,4.10,-0.16 277.21,-49.07,4.10,0.99 287.51,-39.34,4.10,1.16
40.17,-39.86,4.11,1.01 105.94,-15.63,4.11,-0.11 129.41,-42.99,4.11,0.11 147.87,-14.85,4.11,0.92
158.87,-78.61,4.11,1.58 176.63,-61.18,4.11,0.90 234.18,-66.32,4.11,1.16 287.37,-37.90,4.11,0.04
345.22,-52.75,4.11,0.96 39.90,-68.27,4.12,-0.06 181.30,8.73,4.12,0.97 298.82,-41.87,4.12,1.06
312.96,-26.92,4.12,1.63 337.44,-43.75,4.12,1.57 90.60,9.65,4.12,0.17 80.99,-7.81,4.13,0.94
97.24,20.21,4.13,-0.12 238.46,-16.73,4.13,1.00 311.52,-25.27,4.13,0.43 341.51,-81.38,4.13,0.21
354.99,5.63,4.13,0.51 129.41,5.70,4.14,0.00 181.72,-64.61,4.14,0.35 107.97,-0.49,4.15,-0.01
241.09,-11.37,4.16,0.46 261.59,-24.18,4.16,0.28 57.36,-36.20,4.17,0.93 334.21,-7.78,4.17,0.98
213.22,-10.27,4.18,1.32 249.09,-35.26,4.18,1.53 340.16,-27.04,4.18,-0.10 207.36,-34.45,4.19,1.52
281.42,20.55,4.19,0.48 119.21,-22.88,4.20,0.72 343.99,-32.54,4.20,0.95 82.70,5.95,4.20,-0.14
341.67,12.17,4.20,0.50 321.61,-65.37,4.21,0.49 118.33,-48.10,4.22,-0.13 241.65,-36.80,4.22,-0.18
246.76,-18.46,4.22,0.22 281.79,-4.75,4.22,1.09 283.05,-62.19,4.22,-0.15 56.71,-23.25,4.22,0.43
348.58,-6.05,4.22,1.54 5.02,-64.87,4.23,0.58 206.42,-33.04,4.23,0.39 210.41,1.54,4.23,0.12
250.77,-77.52,4.23,1.06 286.60,-37.06,4.23,0.52 115.83,28.88,4.23,1.12 36.75,-47.70,4.24,-0.14
184.59,-79.31,4.24,-0.12 247.85,-34.70,4.24,-0.17 265.35,-12.88,4.24,0.09 41.03,-13.86,4.24,-0.12
348.97,-9.09,4.24,1.11 18.94,-68.88,4.25,0.48 193.36,-40.18,4.25,0.22 77.29,-8.75,4.25,-0.19
49.98,-43.07,4.26,0.71 64.01,-51.49,4.26,0.31 134.62,11.86,4.26,0.14 264.14,-38.64,4.26,1.07
270.38,21.60,4.26,0.41 26.35,9.16,4.26,0.94 53.45,-21.63,4.26,-0.11 196.73,-49.91,4.27,-0.18
229.63,-47.88,4.27,-0.09 290.80,-44.80,4.27,0.35 311.66,16.12,4.27,1.04 15.74,7.89,4.27,0.95
351.99,6.38,4.27,1.06 156.79,-31.07,4.28,1.43 261.84,-29.87,4.28,0.40 320.56,-16.83,4.28,0.89
346.72,-43.52,4.28,0.42 79.89,-13.18,4.29,-0.23 159.83,-55.60,4.29,1.02 178.23,-33.91,4.29,-0.10
247.78,-16.61,4.29,0.92 331.61,-13.87,4.29,-0.07 337.88,-32.35,4.29,0.01 54.22,0.40,4.29,0.57
57.15,-37.62,4.30,-0.04 130.81,3.40,4.30,-0.19 163.90,24.75,4.30,0.02 174.24,-0.82,4.30,0.98
177.42,-63.79,4.30,-0.15 188.02,-16.20,4.30,0.39 215.08,-56.39,4.30,0.08 304.41,-12.51,4.30,0.93
14.65,-29.36,4.30,-0.15 37.04,8.46,4.30,-0.05 130.15,-59.76,4.31,-0.12 216.73,-83.67,4.31,1.30
241.85,-20.87,4.31,0.83 309.58,-1.11,4.31,0.95 70.11,-19.67,4.32,1.60 131.59,-13.55,4.32,0.90
142.93,22.97,4.32,1.54 180.76,-63.31,4.32,0.28 207.96,-32.99,4.32,-0.15 222.91,-43.58,4.32,-0.15
260.21,-12.85,4.32,0.04 112.04,8.93,4.33,1.43 193.28,-48.94,4.33,1.34 216.55,-45.38,4.33,0.43
258.84,-26.60,4.33,0.85 272.15,-63.67,4.33,0.23 86.19,-65.74,4.34,0.22 97.96,-23.42,4.34,-0.24
125.16,-77.48,4.34,1.16 139.05,-57.54,4.34,1.60 144.21,-49.35,4.34,0.17 210.43,-45.60,4.34,0.60
234.51,-42.57,4.34,1.41 261.63,4.14,4.34,1.48 281.76,18.18,4.34,0.15 326.13,17.35,4.34,1.16
98.74,-52.98,4.35,-0.02 121.98,-68.62,4.35,-0.11 132.11,5.84,4.35,-0.04 229.46,-30.15,4.35,1.10
275.81,-61.49,4.35,1.46 326.24,-33.03,4.35,-0.05 72.65,8.90,4.35,0.01 7.89,-62.96,4.36,-0.06
10.84,-57.46,4.36,0.02 78.31,-12.94,4.36,-0.09 89.38,-35.28,4.36,-0.17 104.03,-17.05,4.36,-0.06
122.15,-2.98,4.36,0.97 211.51,-41.18,4.36,-0.20 294.18,-1.29,4.36,-0.08 33.25,8.85,4.36,0.88
73.22,-5.45,4.36,0.26 94.14,-35.14,4.37,0.98 109.68,-24.95,4.37,-0.13 165.04,-42.23,4.37,0.12
272.19,20.81,4.37,-0.16 299.93,-35.28,4.37,-0.15 0.49,-6.01,4.37,1.63 197.49,-5.54,4.38,-0.01
351.51,-20.64,4.38,1.46 353.24,-37.82,4.38,-0.10 28.41,-46.30,4.39,1.60 95.94,4.59,4.39,0.21
120.57,2.33,4.39,1.25 151.98,10.00,4.39,1.45 225.73,2.09,4.39,1.03 253.50,10.17,4.39,-0.09
260.25,-21.11,4.39,0.39 295.02,18.01,4.39,0.78 295.26,17.48,4.39,1.04 319.97,-53.45,4.39,0.19
83.71,9.49,4.39,-0.16 117.02,-25.94,4.40,-0.07 122.26,-19.25,4.40,-0.16 284.24,-67.23,4.40,0.53
329.48,-54.99,4.40,0.30 102.46,-53.62,4.41,0.90 215.76,-39.51,4.41,-0.18 262.68,26.11,4.41,1.43
269.63,30.19,4.41,0.38 349.71,-32.53,4.41,1.11 107.78,30.25,4.41,1.26 349.48,-9.18,4.41,-0.14
99.47,-18.24,4.42,1.14 108.38,-44.64,4.42,1.33 108.56,-26.35,4.42,-0.17 123.51,-40.35,4.42,1.17
165.58,20.18,4.42,0.05 222.57,-27.96,4.42,1.37 236.61,7.35,4.42,0.60 270.44,1.31,4.42,0.05
91.89,14.77,4.42,-0.16 351.34,23.40,4.42,0.62 300.66,-27.71,4.43,1.64 310.86,15.07,4.43,0.30
311.93,-5.03,4.43,1.64 56.54,-12.10,4.43,1.60 63.82,-7.65,4.43,0.82 64.12,-59.30,4.44,1.08
70.14,-41.86,4.44,0.34 113.51,-22.30,4.44,0.52 122.84,-39.62,4.44,1.59 124.64,-36.66,4.44,0.22
218.15,-50.46,4.44,-0.18 292.18,24.66,4.44,1.50 3.66,-18.93,4.44,1.64 12.17,7.59,4.44,1.50
42.27,-32.41,4.45,0.98 78.07,-11.87,4.45,-0.10 129.69,3.34,4.45,1.22 135.02,-41.25,4.45,0.65
158.90,-57.56,4.45,1.60 161.45,-80.54,4.45,-0.19 169.17,-3.65,4.45,0.21 248.03,-21.47,4.45,0.13
293.52,7.38,4.45,1.18 25.36,5.49,4.45,1.35 92.98,14.21,4.45,-0.18 167.91,-22.83,4.46,0.03
182.02,-50.66,4.46,-0.16 246.80,-47.55,4.46,-0.07 343.13,-32.88,4.46,-0.04 58.57,-2.95,4.46,0.67
78.32,2.86,4.46,1.17 97.04,-32.58,4.47,-0.17 98.23,7.33,4.47,0.02 119.56,-49.24,4.47,-0.18
136.29,-72.60,4.47,0.61 141.16,26.18,4.47,1.22 177.79,-45.17,4.47,1.28 224.30,-4.35,4.47,0.32
318.62,10.01,4.47,0.53 331.53,-39.54,4.47,1.35 41.28,-18.57,4.47,0.48 74.64,1.71,4.47,1.37
60.22,-62.16,4.48,1.50 101.97,2.41,4.48,1.10 151.98,-0.37,4.48,-0.03 230.84,-59.32,4.48,0.17
246.03,-20.04,4.48,1.00 346.67,-23.74,4.48,0.89 345.97,3.82,4.48,-0.12 68.38,-29.77,4.49,0.97
101.00,13.23,4.49,1.17 108.14,-46.76,4.49,0.32 118.16,-38.86,4.49,-0.19 316.78,-25.01,4.49,1.60
359.98,-65.58,4.49,-0.07 355.51,1.78,4.49,0.20 355.68,-14.54,4.49,-0.03 87.46,-56.17,4.50,1.07
131.68,-56.77,4.50,-0.17 155.23,-56.04,4.50,-0.10 317.40,-11.37,4.50,0.93 322.18,-21.81,4.50,0.89
332.10,-32.99,4.50,0.05 84.80,4.12,4.50,-0.10 142.31,-35.95,4.51,1.41 144.84,-61.33,4.51,-0.07
311.01,-51.92,4.51,0.28 324.27,-19.47,4.51,-0.18 336.83,-64.97,4.51,-0.03 200.66,-60.99,4.52,-0.14
201.00,-64.54,4.52,0.82 214.78,-13.37,4.52,0.13 272.81,-45.95,4.52,1.01 290.43,-15.96,4.52,0.08
322.49,23.64,4.52,1.62 7.89,-62.97,4.53,0.15 90.01,-3.07,4.53,1.20 114.34,-34.97,4.53,-0.08
261.66,-5.09,4.53,0.39 266.89,-27.83,4.53,0.60 98.76,-22.96,4.54,-0.04 143.00,-1.18,4.54,0.11
228.06,-19.79,4.54,-0.07 230.79,-36.86,4.54,-0.15 299.24,-27.17,4.54,1.46 346.75,9.41,4.54,1.56
352.29,12.76,4.54,0.94 76.10,-35.48,4.55,1.18 112.45,12.01,4.55,1.28 233.97,-44.96,4.55,-0.17
245.16,-24.17,4.55,0.76 272.02,-28.46,4.55,0.94 0.94,-17.34,4.55,-0.05 59.69,-61.40,4.56,1.59
216.53,-45.22,4.56,-0.15 263.92,-46.51,4.56,-0.02 54.27,-40.27,4.57,1.02 246.35,14.03,4.57,0.00
246.40,-23.45,4.57,0.23 283.69,22.65,4.57,0.78 287.09,-40.50,4.57,1.07 298.37,24.08,4.57,-0.05
83.85,-4.84,4.58,-0.18 147.92,-46.55,4.58,1.17 160.88,-60.57,4.58,1.70 198.07,-59.92,4.58,-0.07
243.08,-27.93,4.58,-0.17 264.46,-8.12,4.58,0.13 350.16,23.74,4.58,0.18 10.33,-46.09,4.59,0.95
55.71,-37.31,4.59,1.19 142.29,-2.77,4.59,0.41 154.90,-55.03,4.59,1.60 168.15,-60.32,4.59,0.54
238.40,-25.33,4.59,-0.07 294.18,-24.88,4.59,-0.07 357.23,-28.13,4.59,0.00 81.71,3.10,4.59,-0.20
151.28,-13.06,4.60,-0.09 164.18,-37.14,4.60,1.01 231.33,-38.73,4.60,0.00
"""


STAR_NOTE = ("<!-- Star positions and magnitudes: d3-celestial 0.7.35 (npm), data/stars.6.json; star data XHIP: An Extended "
             "Hipparcos Compilation, Anderson E., Francis C. (2012), VizieR V/137D, converted by Olaf Frohn. "
             "Copyright (c) 2015, Olaf Frohn. All rights reserved. Redistribution and use in source and binary forms, with or "
             "without modification, are permitted provided that the following conditions are met: 1. Redistributions of source "
             "code must retain the above copyright notice, this list of conditions and the following disclaimer. 2. "
             "Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following "
             "disclaimer in the documentation and/or other materials provided with the distribution. 3. Neither the name of the "
             "copyright holder nor the names of its contributors may be used to endorse or promote products derived from this "
             "software without specific prior written permission. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND "
             "CONTRIBUTORS \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES "
             "OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR "
             "CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, "
             "BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS "
             "INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT "
             "(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE "
             "POSSIBILITY OF SUCH DAMAGE. -->")


def sidereal(t):
    """Local sidereal time at Kerio Valley, degrees."""
    days = (t - datetime.datetime(2000, 1, 1, 12, 0)).total_seconds() / 86400.0
    return (280.46061837 + 360.98564736629 * days + SKY_LON) % 360


def stereo(ra, dec, lst):
    """The sky looking south, drawn about the south celestial pole (0, 0), which sits on the horizon
    (0.72 degrees under it): the zenith near (0, -2), east to the left. As the night goes on every
    star turns clockwise about the pole, so the page turns the drawing rather than redrawing it."""
    h = math.radians((lst - ra) % 360)
    r = 2 * math.tan(math.radians(min(90 + dec, 175)) / 2)
    return r * math.sin(h), -r * math.cos(h)


def stars_g(key):
    """One sky's stars as a few paths of dots (a zero-length line with round ends is a dot), grouped
    by size (magnitude) and tint (b-v colour index)."""
    lst = sidereal(SKY_AT[key])
    groups = {}
    for row in STARS.split():
        ra, dec, mag, bv = (float(v) for v in row.split(","))
        x, y = stereo(ra, dec, lst)
        if not (BOX[0] <= x <= BOX[1] and BOX[2] <= y <= BOX[3]):
            continue
        z = 0 if mag < 0.5 else 1 if mag < 1.5 else 2 if mag < 2.5 else 3 if mag < 3.5 else 4
        t = "b" if bv < 0 else "w" if bv < 0.8 else "y" if bv < 1.3 else "r"
        groups.setdefault((z, t), []).append("M%d %dh0" % (round(x * 1000), round(y * 1000)))
    return "".join('<path class="z%d t%s" d="%s"/>' % (z, t, "".join(v)) for (z, t), v in sorted(groups.items()))


def mdp(n, amp, rough, rnd):
    """1/f midpoint displacement: 2**n + 1 values from 0 to 0, each level's kick `rough` times the last."""
    N = 2 ** n
    v = [0.0] * (N + 1)
    step, a = N, amp
    while step > 1:
        h = step // 2
        for i in range(h, N, step):
            v[i] = (v[i - h] + v[i + h]) / 2 + rnd.uniform(-a, a)
        step, a = h, a * rough
    return v


def series(v, t):
    x = min(max(t, 0.0), 1.0) * (len(v) - 1)
    i = min(int(x), len(v) - 2)
    return v[i] + (v[i + 1] - v[i]) * (x - i)


# the horizon's two drawings: (width, height, vanishing point x, its y); the phone's is the right-hand part,
# drawn with fewer and larger features, not a scaled-down copy of the wide one
RIDGE_BOX = {"w": (1600, 400, 700, 332), "p": (800, 400, 150, 336)}


def ridge(kind):
    """The horizon looking south down Kerio Valley, from seeded geometry (an impression, not a survey).
    The Elgeyo escarpment on the right is a fault scarp: a long, nearly level plateau edge running away to
    the vanishing point (so in perspective a near-straight line falling toward it), with 1/f roughness and
    small dips where gullies cut back; its steep face carries the gullies (curved, unevenly spaced, wider
    near). The Tugen Hills on the left are rounder, with two summits, 1/f midpoint displacement for their
    line; a farther range shows behind them and low hills where the valley ends, each farther layer
    lighter. The valley floor near, with two flat-topped acacias. Returns the paths, and the skyline (the
    highest land at 33 points across) for the sun to rise and set behind."""
    W, H, vx, vy = RIDGE_BOX[kind]
    phone = kind == "p"
    rnd = random.Random(1907 if not phone else 2207)
    zf = 7.0                                    # the wall runs from z=1 (the right edge) to z=7, near the vanishing point

    def wx(z):
        return vx + (W - vx) * (1 / z - 1 / zf) / (1 - 1 / zf)
    tall = 205 if not phone else 196
    plate = mdp(6 if phone else 8, 1.0, 0.5, rnd)
    bend = mdp(3, 1.0, 0.6, rnd)
    gul, z = [], 1.0 + rnd.uniform(0.05, 0.3)
    while z < zf - 0.2:
        gw = rnd.uniform(0.04, 0.16) * (1.7 if phone else 1)
        gul.append((z, gw, rnd.uniform(0.25, 0.75)))
        z += rnd.expovariate(1 / (0.55 if not phone else 1.1)) + gw * 1.4

    def crest(x):
        t = (x - vx) / float(W - vx)
        if t <= 0:
            return vy
        z = 1 / (1 / zf + t * (1 - 1 / zf))
        hgt = tall / z
        y = vy - hgt * (1 - 0.9 * math.exp(-t / 0.03)) + series(plate, t) * (1.2 + 6 * t) + series(bend, t) * 9 * t
        for gz, gw, gd in gul:
            dz = abs(z - gz) / gw
            if dz < 1:
                y += gd * hgt * 0.035 * (1 - dz * dz)
        return y

    def foot(x):
        return vy + (x - vx) / float(W - vx) * (H - vy + 30)
    xs = sorted(set([vx + i * (W - vx) / (90.0 if phone else 170.0) for i in range(91 if phone else 171)] + [wx(g[0]) for g in gul]))
    cr = [(x, crest(x)) for x in xs]
    gl = []
    for gz, gw, gd in gul:
        x = wx(gz)
        y0, y1 = crest(x), foot(x)
        ln = (y1 - y0) * rnd.uniform(0.55, 0.9)
        x1 = x + (W - x) * 0.015 * rnd.uniform(-0.5, 1.5) - (y1 - y0) * rnd.uniform(0.1, 0.35)
        gl.append((x, y0 + 1, x1, y0 + ln))
    tp = mdp(5 if phone else 7, 1.0, 0.56, rnd)
    top_l = 236 if not phone else 262

    def tug(x):
        t = x / float(vx)
        return (top_l + (vy - top_l) * t ** 1.6 + series(tp, t) * (44 * (1 - t) + 6)
                - 18 * math.exp(-((t - 0.22) / 0.12) ** 2) - 9 * math.exp(-((t - 0.58) / 0.08) ** 2))
    tg = [(x, min(tug(min(x, vx)), vy + 1)) for x in [i * vx / (40.0 if phone else 110.0) for i in range(41 if phone else 111)] + [vx + 20]]
    fp = mdp(4 if phone else 6, 1.0, 0.5, rnd)
    fw = vx + 120
    far2 = [(x, top_l - 22 + (vy - 6 - top_l + 22) * (x / fw) ** 1.3 + series(fp, x / fw) * 14) for x in [i * fw / 80.0 for i in range(81)]]
    hp = mdp(5, 1.0, 0.55, rnd)
    farh = [(x, vy - 3 - 9 * math.exp(-((x - (vx - 60)) / 70.0) ** 2) - 6 * math.exp(-((x - (vx + 150)) / 60.0) ** 2) + series(hp, (x - vx + 260) / 600.0) * 3)
            for x in [vx - 260 + i * 10.0 for i in range(61)]]
    npr = mdp(5, 1.0, 0.5, rnd)
    near = [(x, 372 + series(npr, x / float(W)) * 9) for x in [i * W / 64.0 for i in range(65)]]

    def pts(p):
        """a polyline as its first point and relative steps: "x y l dx dy dx dy ..." """
        q = [(int(round(x)), int(round(y))) for x, y in p]
        q = [q[0]] + [b for a, b in zip(q, q[1:]) if b != a]
        return "%d %d" % q[0] + ("l" + " ".join("%d %d" % (b[0] - a[0], b[1] - a[1]) for a, b in zip(q, q[1:])) if len(q) > 1 else "")

    def acacia(cx, base, h, w):
        t0 = base - h
        return ("M%d %dL%d %dL%d %dL%d %dZ" % (cx - 3, base, cx + 3, base, cx + 2, t0 + 4, cx - 1, t0 + 4)
                + "M%d %dQ%d %d %d %dQ%d %d %d %dQ%d %d %d %dQ%d %d %d %dZ"
                % (cx - w / 2, t0 + 3, cx - w / 2 + 6, t0 - 5, cx - w / 6, t0 - 7, cx + 2, t0 - 10, cx + w / 4, t0 - 7,
                   cx + w / 2 - 4, t0 - 6, cx + w / 2, t0 + 2, cx, t0 + 7, cx - w / 2, t0 + 3))
    sky = []
    for i in range(33):
        x = i * W / 32.0
        y = min(tug(min(x, vx)) if x <= vx + 20 else 999, crest(x) if x >= vx else 999, vy)
        sky.append(round(y, 1))
    return {
        "far2": "M0 %dL" % H + pts(far2) + "L%d %dZ" % (fw, H),
        "farh": "M%d %dL" % (vx - 260, H) + pts(farh) + "L%d %dZ" % (vx + 340, H),
        "tug": "M0 %dL" % H + pts(tg) + "L%d %dL%d %dZ" % (vx + 20, vy + 1, vx + 230, H),
        "esc": "M%d %dL" % (vx - 4, vy + 1) + pts(cr) + "L%d %dL%d %dZ" % (W, H, vx - 220, H),
        "near": "M0 %dL" % (H + 240) + pts(near) + "L%d %dZ" % (W, H + 240),
        "trees": acacia(214, 372, 44, 92) + acacia(1196, 376, 30, 64) if not phone else acacia(560, 374, 34, 70),
        "face": "M" + pts(cr + [(W, foot(W)), (vx, vy)]) + "Z",
        "tface": "M" + pts([p for p in tg if p[0] <= vx] + [(vx, vy + 1), (0, vy + 26)]) + "Z",
        "gul": "".join("M%.0f %.0fQ%.0f %.0f %.0f %.0f" % (a, b, a + (c - a) * 0.2, b + (d - b) * 0.55, c, d) for a, b, c, d in gl),
        "rim": "M" + pts(cr),
        "trim": "M" + pts([p for p in tg if 4 < p[0] < vx - 10]),
        "sky": sky,
        # each gradient-filled shape's top and bottom (the gradients run over the shape, as in SVG)
        "bb": {"tug": [round(min(y for x, y in tg)), H], "esc": [round(min(y for x, y in cr)), H],
               "face": [round(min(y for x, y in cr)), round(foot(W))], "tface": [round(min(y for x, y in tg)), vy + 26]},
    }


RIDGES = {k: ridge(k) for k in RIDGE_BOX}


def ridge_defs():
    """Paths, stars and gradients shared by the moving sky and the still page's horizons and night (one copy of
    each in the page)."""
    out = []
    for k, r in RIDGES.items():
        for name in ("far2", "farh", "tug", "esc", "near", "trees", "face", "tface", "gul", "rim", "trim"):
            out.append('<path id="wrR%s-%s" d="%s"/>' % (k, name, r[name]))
    grads = ('<linearGradient id="wrThF" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1000"><stop class="f0" offset="0"/><stop class="f1" offset=".3"/>'
             '<stop class="f1" offset=".74"/><stop class="f0" offset="1"/></linearGradient>'
             '<filter id="wrLumA" color-interpolation-filters="sRGB"><feColorMatrix type="luminanceToAlpha"/></filter>'
             '<linearGradient id="wrThR" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1000"><stop class="q0" offset="0"/><stop class="q1" offset=".32"/>'
             '<stop class="q1" offset=".7"/><stop class="q0" offset="1"/></linearGradient>')
    stars = "".join('<g id="%s">%s</g>' % (gid, stars_g(key)) for key, gid in (("dawn", "wrStarsDawn"), ("night", "wrStarsNight")))
    # the gradients in a rendered (empty) SVG; the shapes and the stars, which are only ever used by reference or
    # read by the script, in a hidden one, so the browser keeps no style for them while the page scrolls
    return ('<svg class="wr-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>' + grads + "</defs></svg>"
            '<div class="wr-data" hidden><svg aria-hidden="true" focusable="false"><defs>' + "".join(out) + STAR_NOTE + stars + "</defs></svg></div>\n")


# the hills' gradients, needed only where the still page draws its horizons (the canvas makes its own): they live
# in the first still horizon, so the moving page, where it is hidden, keeps no style for them
RIDGE_GRADS = ('<defs><linearGradient id="wrHaze" x1="0" y1="0" x2="0" y2="1"><stop class="h1" offset="0"/><stop class="h2" offset=".7"/></linearGradient>'
               '<linearGradient id="wrWall" x1="0" y1="0" x2="0" y2="1"><stop class="w1" offset="0"/><stop class="w2" offset=".55"/></linearGradient>'
               '<linearGradient id="wrLit" x1="0" y1="0" x2="0" y2="1"><stop class="g1" offset="0"/><stop class="g2" offset=".42"/><stop class="g3" offset="1"/></linearGradient>'
               '<linearGradient id="wrGlow" x1="0" y1="0" x2="0" y2="1"><stop class="p1" offset="0"/><stop class="p2" offset="1"/></linearGradient></defs>')


def horizon(layer, kinds="wp", defs=""):
    """One layer of the horizon, wide and phone drawings (CSS shows one): the land, the morning light
    (the escarpment's east face lit, its gullies in shadow, the Tugen crest backlit) or the dusk light
    (the escarpment rimmed, the Tugen Hills' west slopes in the afterglow)."""
    parts = {
        "land": (("far2", "r-far2"), ("farh", "r-far"), ("tug", "r-tug"), ("esc", "r-esc"), ("near", "r-near"), ("trees", "r-near")),
        "morn": (("face", "r-face"), ("gul", "r-gul"), ("trim", "r-trim")),
        "dusk": (("tface", "r-tface"), ("rim", "r-rim")),
    }[layer]
    out = []
    for k in kinds:
        W, H = RIDGE_BOX[k][:2]
        out.append('<svg class="is-%s" viewBox="0 0 %d %d" preserveAspectRatio="xMaxYMax slice" focusable="false">%s%s</svg>'
                   % (k, W, H, defs if k == "w" else "", "".join('<use href="#wrR%s-%s" class="%s"/>' % (k, n, c) for n, c in parts)))
    return "".join(out)


def thermal(seed, lean, height, width, rings):
    """One thermal column in a 240 x 1000 box, as a pilot pictures it: a few soft, sinuous streamlines of
    air drawn in low down, rising through a core that leans with the wind and spreading at the top; at
    most two bubbles (rings), widening as they rise. Faded top and bottom by its stroke (no mask)."""
    rnd = random.Random(seed)
    top = 1000 - 1000 * height
    lines = []
    for k in (-1, -0.35, 0.3, 0.95)[:4 if width > 0.8 else 3]:
        ph, am = rnd.uniform(0, 6.3), rnd.uniform(4, 10)
        p = []
        for i in range(15):
            u = i / 14.0                              # 0 at the ground, 1 at the top
            y = 1000 - u * (1000 - top)
            spread = 1 - 0.78 * math.sin(math.pi * min(u, 0.85) / 0.85 * 0.5) if u < 0.85 else 0.22 + (u - 0.85) / 0.15 * 0.55
            x = 120 + lean * u ** 1.4 + k * 92 * width * spread + am * math.sin(u * 7.5 + ph) * (0.4 + u)
            p.append((x, y))
        d = "M%.0f %.0f" % p[0]
        for i in range(1, len(p) - 1):           # smooth: through the midpoints, each point a control
            d += "Q%.0f %.0f %.0f %.0f" % (p[i][0], p[i][1], (p[i][0] + p[i + 1][0]) / 2, (p[i][1] + p[i + 1][1]) / 2)
        d += "L%.0f %.0f" % p[-1]
        lines.append('<path d="%s"/>' % d)
    rs = []
    for j, (u, rx) in enumerate(rings):
        y = 1000 - u * (1000 - top)
        rs.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f"/>' % (120 + lean * u ** 1.4, y, rx * width, rx * width * 0.24))
    return "".join(lines) + "".join(rs)


def thermals_html():
    """Two thermals behind the mark, in the gutters: a tall one leaning right at the right-hand edge, a
    lower, narrower one leaning left at the left-hand edge (wide screens only; phones keep the right one)."""
    cols = ((thermal(5, 34, 0.92, 1.0, ((0.42, 26), (0.7, 44))), "n0"), (thermal(17, -26, 0.66, 0.72, ((0.55, 30),)), "n1"))
    return ('<div class="wr-thermals" aria-hidden="true">' + "".join(
        '<svg class="wr-th %s" viewBox="0 0 240 1000" preserveAspectRatio="xMidYMax meet" focusable="false">%s</svg>' % (c, s)
        for s, c in cols) + "</div>")


def sky_html():
    """The fixed sky behind the whole page: the sky itself, painted small and stretched by the browser, and over
    it one canvas for everything drawn on the sky (see SCRIPT, part 7)."""
    return '<div class="wr-sky" aria-hidden="true"><canvas class="wr-sky-c" width="16" height="16"></canvas><canvas class="wr-sky-o" width="16" height="16"></canvas></div>\n'


def still_ridge(where, light=""):
    """The horizon on a still page (no script, or reduced motion): drawn in the flow at a chapter's edge."""
    return ('<div class="wr-still-rg %s" aria-hidden="true"><div class="wr-rg is-land">%s</div>%s</div>'
            % (where, horizon("land", defs=RIDGE_GRADS if where == "at-01" else ""), '<div class="wr-rg is-%s">%s</div>' % (light, horizon(light)) if light else ""))


def night_static():
    """The close's stars for a still page (no script, or reduced motion): the night sky's own dots."""
    return ('<div class="wr-night" aria-hidden="true"><svg viewBox="-1500 -2250 3000 2350" preserveAspectRatio="xMidYMax slice" focusable="false">'
            '<use href="#wrStarsNight"/></svg></div>')


# the cloud masks (see make_images): file, width, height
CLOUDS = {"street-l": (1600, 640), "street-s": (800, 680), "cu-l": (1200, 700), "cu-s": (600, 350), "dusk-l": (1600, 520), "dusk-s": (800, 260)}


def make_images():
    """Write the background images into prototypes/v4/img/record/ (see the docstring), all from the
    site's own files or from geometry: the Milky Way, the cloud masks and the ground's form lines."""
    import gzip
    import contourpy
    import numpy as np
    from PIL import Image, ImageFilter
    out = os.path.join(V4, REC_IMG)
    os.makedirs(out, exist_ok=True)
    kenya = os.path.join(ROOT, "assets", "destinations", "kenya")
    for old in ("relief-w.webp", "relief-p.webp", "contours-p.webp") + tuple("cloud-%d-%s.webp" % (n, t) for n in (1, 3, 4) for t in "ls"):
        if os.path.exists(os.path.join(out, old)):
            os.remove(os.path.join(out, old))

    def save(a, name, q=60):
        """a mask as a greyscale image (white: the shape); the page turns it into alpha and colours it from the tokens"""
        Image.fromarray(np.clip(a * 255 + .5, 0, 255).astype("uint8")).save(os.path.join(out, name), "WEBP", quality=q, method=6)

    # 1. the Milky Way at the two times, in the stars' projection (160 px a unit): the galactic plane from the
    # IAU galactic pole (RA 192.85948, Dec 27.12825, J2000; the north celestial pole at l 122.93192), a band
    # wider and brighter toward the centre in Sagittarius, the star clouds of Cygnus, Carina and Scutum, the
    # Great Rift's dark lane and the Coalsack, mottled by a seeded 1/f noise: an impression, drawn here
    def noise3(v, octaves, seed):
        rs = np.random.RandomState(seed)
        acc, amp, tot, f = np.zeros(v.shape[0]), 1.0, 0.0, 5.0
        for _ in range(octaves):
            n = int(f * 2) + 3
            lat = rs.rand(n, n, n)
            q = (v * 0.5 + 0.5) * f + 1.0
            i = np.floor(q).astype(int)
            t = q - i
            t = t * t * (3 - 2 * t)
            c = 0
            for dx in (0, 1):
                for dy in (0, 1):
                    for dz in (0, 1):
                        wgt = (t[:, 0] if dx else 1 - t[:, 0]) * (t[:, 1] if dy else 1 - t[:, 1]) * (t[:, 2] if dz else 1 - t[:, 2])
                        c = c + wgt * lat[i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz]
            acc += amp * c
            tot += amp
            amp *= 0.55
            f *= 2.1
        acc /= tot
        return (acc - acc.min()) / (acc.max() - acc.min())
    s = 160
    w, h = round((BOX[1] - BOX[0]) * s), round((BOX[3] - BOX[2]) * s)
    X, Y = np.meshgrid(BOX[0] + (np.arange(w) + .5) / s, BOX[2] + (np.arange(h) + .5) / s)
    dec = np.degrees(2 * np.arctan(np.hypot(X, Y) / 2)) - 90
    for key in ("dawn", "night"):
        ra = (sidereal(SKY_AT[key]) - np.degrees(np.arctan2(X, -Y))) % 360
        a, d = np.radians(ra), np.radians(dec)
        aG, dG = math.radians(192.85948), math.radians(27.12825)
        b = np.degrees(np.arcsin(np.clip(np.sin(d) * math.sin(dG) + np.cos(d) * math.cos(dG) * np.cos(a - aG), -1, 1)))
        l = (122.93192 - np.degrees(np.arctan2(np.cos(d) * np.sin(a - aG), np.sin(d) * math.cos(dG) - np.cos(d) * math.sin(dG) * np.cos(a - aG)))) % 360
        L = np.where(l > 180, l - 360, l)
        cen = (1 + np.cos(np.radians(L))) / 2
        band = (0.22 + 0.78 * cen ** 1.6 + 0.35 * np.exp(-((L - 80) / 12) ** 2) + 0.3 * np.exp(-((L + 73) / 14) ** 2)
                + 0.25 * np.exp(-((L - 27) / 8) ** 2)) * np.exp(-(b / (4.0 + 6.5 * cen ** 1.5)) ** 2)
        bulge = 0.9 * np.exp(-(L / 14) ** 2 - ((b + 2) / 9) ** 2)
        rift = 1 - 0.62 * np.exp(-((b - 1.2 - 0.03 * L) / (1.6 + 0.02 * np.abs(L))) ** 2) * np.exp(-((L - 38) / 36) ** 4)
        coal = 1 - 0.5 * np.exp(-(((L + 59) / 5) ** 2 + ((b + 0.8) / 4) ** 2))
        v = np.stack([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)], -1).reshape(-1, 3)
        I = (band + bulge) * rift * coal * (0.2 + 1.6 * noise3(v, 5, 7).reshape(h, w) ** 2)
        I = np.clip(I / np.percentile(I, 99.7), 0, 1) ** 1.15
        img = Image.fromarray((I * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
        save(np.asarray(img, dtype="float32") / 255, "mw-%s.webp" % key, 50)

    # 2. the clouds, as greyscale luminance masks (white: the lit cloud; black: clear sky). Their texture is the
    # Kenya page's own cloud layer (cloud-1's alpha, a fractal field): it warps each cumulus' lobes and breaks
    # its edge, so no two lobes are round
    T = np.asarray(Image.open(os.path.join(kenya, "clouds", "cloud-1.webp")).getchannel("A"), dtype="float32")
    T /= T.max()

    def tex(x, y):
        return T[np.abs(y).astype(int) % T.shape[0], np.abs(x).astype(int) % T.shape[1]]

    def blur(a, sg):
        r = int(3 * sg) + 1
        k = np.exp(-(np.arange(-r, r + 1) / sg) ** 2 / 2)
        k /= k.sum()
        a = np.apply_along_axis(lambda q: np.convolve(np.pad(q, r, mode="edge"), k, "valid"), 0, a)
        return np.apply_along_axis(lambda q: np.convolve(np.pad(q, r, mode="edge"), k, "valid"), 1, a)

    def cumulus(W, H, cx, base, cw, ch, seed):
        """One fair-weather cumulus with a flat base at y=base: a seeded heap of lobes on a flat lens,
        lit from above (lobe tops bright, a silver edge where the surface faces the sun), its base
        dimmer but never darker than the sky behind (it is a mask: dark means clear)."""
        rnd = random.Random(seed)
        x0, x1 = int(max(0, cx - cw)), int(min(W, cx + cw))
        y0, y1 = int(max(0, base - ch * 1.9)), int(min(H, base + 4))
        yy, xx = np.mgrid[y0:y1, x0:x1].astype("float32")
        k = 900.0 / cw
        wx_ = xx + (tex(xx * k + 37 * seed, yy * k + 53 * seed) - 0.45) * ch * 0.32
        wy_ = yy + (tex(xx * k + 37 * seed + 511, yy * k + 53 * seed + 233) - 0.45) * ch * 0.26
        F = np.full(xx.shape, -1.0, "float32")
        for _ in range(rnd.randint(16, 22)):
            u = rnd.uniform(-1, 1)
            dome = math.sqrt(max(0, 1 - u * u))
            r = ch * (0.13 + 0.12 * rnd.random()) * (0.7 + 0.6 * dome)
            F = np.maximum(F, 1 - np.hypot(wx_ - (cx + u * cw * 0.40), wy_ - (base - r * 0.4 - dome * ch * rnd.uniform(0.35, 0.78))) / r)
        F = np.maximum(F, 1 - np.hypot((wx_ - cx) / (cw * 0.43), (wy_ - (base - ch * 0.12)) / (ch * 0.3)))
        G = F + 0.07 * (tex(xx * 2.9 * k + 97, yy * 2.9 * k + 41) - 0.5)
        A = np.clip(G / 0.05, 0, 1) * np.clip((base - yy) / 1.5, 0, 1)
        S = blur(np.clip(G, 0, 0.6), max(1.0, ch * 0.05))
        gy = np.zeros_like(S)
        gy[1:-1] = (S[2:] - S[:-2]) / 2
        up = np.clip(gy / (np.abs(gy).max() + 1e-6) * 3.0, -1, 1)
        lum = (0.5 + 0.36 * np.clip((base - yy) / ch, 0, 1) ** 0.5) * (0.86 + 0.14 * up)
        lum = np.clip(lum + 0.55 * np.clip(1 - np.abs(G - 0.035) / 0.05, 0, 1) * np.clip(up + 0.25, 0, 1), 0, 1)
        o = np.zeros((H, W), "float32")
        o[y0:y1, x0:x1] = A * lum
        return o

    def street(W, H, vx, vy, nx, ny, cw, ch, scales, seeds):
        """A cloud street along the escarpment: cumulus with their bases at one height, so in perspective
        the bases fall along one line toward the valley's vanishing point; the nearest is the largest."""
        acc = np.zeros((H, W), "float32")
        for sc, sd in zip(scales, seeds):
            acc = np.maximum(acc, cumulus(W, H, vx + (nx - vx) * sc, vy + (ny - vy) * sc, cw * sc, ch * sc, sd))
        return acc
    save(street(1600, 640, 700, 628, 1380, 250, 400, 236, (1.0, 0.63, 0.41, 0.27, 0.18, 0.12), (3, 5, 8, 13, 21, 34)), "street-l.webp")
    save(street(800, 680, 250, 668, 590, 240, 290, 175, (1.0, 0.6, 0.38, 0.24), (3, 5, 8, 13)), "street-s.webp")
    save(cumulus(1200, 700, 640, 640, 470, 330, 55), "cu-l.webp")
    save(cumulus(600, 350, 320, 320, 235, 165, 55), "cu-s.webp")
    # the dusk cloud: a band of the Kenya page's cloud-4, its edges sharpened, lit from below by the set sun
    # (bright where the cloud's underside faces down)
    c4 = Image.open(os.path.join(kenya, "clouds", "cloud-4.webp")).getchannel("A")
    for name, (W, H) in (("dusk-l.webp", CLOUDS["dusk-l"]), ("dusk-s.webp", CLOUDS["dusk-s"])):
        a = np.asarray(c4.crop((0, 240, 2400, 1020)).resize((W, round(W * 780 / 2400)), Image.LANCZOS), dtype="float32")[:H] / 255.0
        a = a / np.percentile(a, 99.5)
        A = np.clip((a - 0.28) / 0.3, 0, 1)
        A = A * A * (3 - 2 * A)
        S = blur(A, W / 400.0)
        gy = np.zeros_like(S)
        gy[1:-1] = S[:-2] - S[2:]                 # > 0 on an underside
        under = np.clip(gy / (np.abs(gy).max() + 1e-6) * 4, 0, 1)
        fade = np.clip(np.minimum(np.arange(W) / (0.12 * W), (W - np.arange(W)) / (0.12 * W)), 0, 1)[None, :]
        save(A * (0.06 + 0.94 * under ** 0.8) * fade, name)

    # 3. the ground: form lines traced from the chart sheet's relief (kenya-sheet-terrain.webp, a shaded
    # relief, so these are lines of equal shade, smoothed: form lines, not surveyed contours), cut round Kerio
    # Valley and turned a quarter so the Rift runs along the course; each level's lines also fill the land
    # above them faintly, so the ground reads in terraces. Vector, crisp at every width, faded top and bottom
    # inside the drawing, far enough in that the widest screens' crop never reaches a line at full strength (no CSS
    # mask on the moving layer; the strokes scale with the drawing, which is shown at about its own size, because a
    # mask does not reach non-scaling strokes)
    ter = Image.open(os.path.join(kenya, "map", "kenya-sheet-terrain.webp")).convert("L").crop((255, 0, 855, 780))
    ter = ter.filter(ImageFilter.GaussianBlur(7))
    ter = ter.resize((ter.size[0] // 2, ter.size[1] // 2), Image.LANCZOS)
    f = np.rot90(np.asarray(ter, dtype="float64"), 1)
    fh, fw = f.shape
    gen = contourpy.contour_generator(z=np.pad(f, 1, constant_values=f.min() - 1))

    def dp(p, tol):
        keep = np.zeros(len(p), bool)
        keep[0] = keep[-1] = True
        st = [(0, len(p) - 1)]
        while st:
            i, j = st.pop()
            if j <= i + 1:
                continue
            a_, d_ = p[i], p[j] - p[i]
            n = math.hypot(*d_)
            seg = p[i + 1:j]
            dist = np.hypot(*(seg - a_).T) if n == 0 else np.abs(d_[0] * (seg[:, 1] - a_[1]) - d_[1] * (seg[:, 0] - a_[0])) / n
            m = int(np.argmax(dist))
            if dist[m] > tol:
                keep[i + 1 + m] = True
                st += [(i, i + 1 + m), (i + 1 + m, j)]
        return p[keep]
    S4, paths = 4, []
    for lv in np.percentile(f, np.linspace(34, 93, 8)):
        d = []
        for ln in gen.lines(lv):
            ln = ln - 1
            if len(ln) < 6 or np.sum(np.hypot(*np.diff(ln, axis=0).T)) * 2 < 60:
                continue
            q = np.round(dp(ln, 0.45) * S4).astype(int)
            q = q[np.r_[True, np.any(np.diff(q, axis=0) != 0, axis=1)]]
            if len(q) < 4:
                continue
            rel = np.diff(q, axis=0)
            d.append("M%d %d" % tuple(q[0]) + "l" + " ".join("%d %d" % (dx, dy) for dx, dy in rel[:-1]) + "z")
        paths.append("".join(d))
    W, H = fw * S4, fh * S4
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">'
           '<defs><linearGradient id="f" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="%d"><stop offset=".18" stop-color="white" stop-opacity="0"/>'
           '<stop offset=".38" stop-color="white"/><stop offset=".62" stop-color="white"/><stop offset=".82" stop-color="white" stop-opacity="0"/></linearGradient>'
           '<mask id="m" maskUnits="userSpaceOnUse" x="-20" y="-20" width="%d" height="%d"><rect x="-20" y="0" width="%d" height="%d" fill="url(#f)"/></mask></defs>'
           '<g mask="url(#m)" fill="white" fill-rule="evenodd" stroke="white" stroke-width="1">' % (W, H, H, W + 40, H + 40, W + 40, H)
           + "".join('<path d="%s" fill-opacity=".032" stroke-opacity=".7"/>' % p for p in paths)
           + "</g></svg>\n")
    open(os.path.join(out, "ground.svg"), "w").write(svg)
    print("  ground.svg: %d bytes, %d gzipped" % (len(svg), len(gzip.compress(svg.encode(), 9))))
    for fn in sorted(os.listdir(out)):
        print("  %s %d bytes" % (fn, os.path.getsize(os.path.join(out, fn))))


GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='g'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E"
         "%3CfeColorMatrix type='saturate' values='0'/%3E%3CfeComponentTransfer%3E%3CfeFuncA type='linear' slope='.55'/%3E"
         "%3C/feComponentTransfer%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23g)'/%3E%3C/svg%3E\")")

# the still day's gradient: where each stop sits, in percent of the page (the chapters measured with no script
# and with reduced motion at 390, 768 and 1440 px, then averaged): the opening's end, then pre-dawn, dawn, the
# morning, the course's midmorning and the course, Kerio Valley at midday, the afternoon, dusk at the start of
# 06, late dusk, night
STILL = (11, 13, 17, 23, 29, 33, 45, 63, 77, 85, 92)

# the same grain, faint enough to lie over the sky from the page itself (as the old overlay did at 7%)
GRAIN2 = GRAIN.replace("slope='.55'", "slope='.04'")

CSS = r"""
/* ===== The speed record attempt (tools/v4_record.py) ===== */
.wr{--wr-top:92px;--wr-bar:56px;--wr-dock:58px;
  --wr-deep:color-mix(in srgb,var(--bg) 58%,var(--ink));
  --wr-shade:color-mix(in srgb,var(--bg) 84%,transparent);
  --wr-solid:color-mix(in srgb,var(--bg) 92%,var(--card));
  --wr-mega:min(calc(var(--fs-display) * 2.1),14.6vw);
  --wr-giga:min(calc(var(--fs-display) * 3.3),23vw);
  --wr-h2:calc(var(--fs-h1) * 1.2);
  --wr-pad:calc(var(--sp-section) * 1.5);
  --wr-x:var(--gutter);
  position:relative;overflow-x:clip;}
@media (max-width:560px){.wr{--wr-x:var(--sp-2);}}
.wr-in{box-sizing:border-box;width:100%;max-width:var(--measure);margin:0 auto;padding-inline:var(--wr-x);}
.wr-tbd{font-style:italic;font-weight:400;color:var(--gray);white-space:nowrap;letter-spacing:0;text-transform:none;font-family:var(--font-body);}
.wr-vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}

/* the chapter number, the headline, the one line under it */
.wr-no{display:flex;align-items:center;gap:var(--sp-2);margin:0 0 var(--sp-3);font-family:var(--font-mono);font-size:var(--fs-small);letter-spacing:.08em;color:var(--gray);}
.wr-no::after{content:"";flex:0 0 clamp(2.5rem,6vw,5rem);height:1px;background:var(--edge-hi);}
.wr-h2{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wr-h2);line-height:1.02;letter-spacing:-.035em;color:var(--white);text-wrap:balance;max-width:14ch;}
.wr-lede{margin:var(--sp-3) 0 0;max-width:31rem;font-size:var(--fs-lead);line-height:1.55;color:var(--gray-light);text-wrap:pretty;}

/* kinetic type: each word (or line) rises inside its own mask, once */
.wr-w{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.12em;margin-bottom:-.12em;}
.wr-w>span,.wr-ln>span{display:inline-block;}
.wr-ln{display:block;overflow:hidden;padding-bottom:.07em;margin-bottom:-.07em;}
.wr-ln>span{display:block;}

/* links: the underline draws in under the pointer */
.wr-u{color:inherit;text-decoration:underline;text-decoration-color:var(--edge-hi);text-underline-offset:.22em;text-decoration-thickness:1px;
  background:linear-gradient(var(--orange),var(--orange)) 0 100%/0 1px no-repeat;padding-bottom:1px;
  transition:background-size .6s var(--ease),color .3s var(--ease),text-decoration-color .3s var(--ease);}
.wr-u:hover,.wr-u:focus-visible{color:var(--white);text-decoration-color:transparent;background-size:100% 1px;}
.wr-ext{display:inline-block;width:.62em;height:.62em;margin-left:.28em;vertical-align:.08em;}
.wr :focus-visible{outline:2px solid var(--white);outline-offset:3px;}

/* still film grain over the dark chapters (an SVG noise, never animated) */
.wr-grain{position:relative;isolation:isolate;}
.wr-grain::after{content:"";position:absolute;inset:0;z-index:4;pointer-events:none;opacity:.32;mix-blend-mode:overlay;
  background-image:__GRAIN__;background-size:220px 220px;}

/* the button: the site's orange, skewed */
.wr-btn{position:relative;isolation:isolate;display:inline-flex;align-items:center;justify-content:center;gap:.55rem;min-height:44px;padding:0 1.3rem;
  font-family:var(--font-body);font-size:var(--fs-small);font-weight:700;letter-spacing:.01em;text-decoration:none;white-space:nowrap;color:var(--ink);}
.wr-btn::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--orange);transform:skewX(-10deg);transition:transform .45s var(--ease),filter .3s var(--ease);}
.wr-btn:hover::before{transform:skewX(-10deg) scaleX(1.05);filter:brightness(1.08);}

/* ---------- the opening ---------- */
.wr-hero{position:relative;min-height:calc(100svh - var(--wr-top));display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;background:var(--bg);}
.wr-hero-pic{position:absolute;inset:0;z-index:-2;}
.wr-hero-pic img{display:block;width:100%;height:100%;object-fit:cover;object-position:66% 46%;}
.wr-hero::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:
  linear-gradient(90deg,color-mix(in srgb,var(--bg) 80%,transparent) 0%,color-mix(in srgb,var(--bg) 38%,transparent) 46%,transparent 72%),
  linear-gradient(180deg,color-mix(in srgb,var(--bg) 45%,transparent) 0%,transparent 24%,transparent 46%,color-mix(in srgb,var(--bg) 70%,transparent) 78%,var(--bg) 100%);}
.wr-hero-in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,16.5rem);align-items:end;gap:var(--sp-5);padding-block:var(--sp-5) calc(var(--sp-section) * 1.15);}
.wr-kick{margin:0 0 var(--sp-3);text-wrap:balance;font-size:var(--fs-micro);font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--orange);
  text-shadow:0 1px 2px color-mix(in srgb,var(--bg) 85%,transparent);}
.wr-mega{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wr-mega);line-height:.9;letter-spacing:-.045em;color:var(--white);}
.wr-mega .is-hollow{color:transparent;-webkit-text-stroke:max(1px,.011em) var(--white);}
.wr-hero-sub{margin:var(--sp-4) 0 0;max-width:27rem;font-size:var(--fs-lead);line-height:1.5;color:var(--gray-light);}
.wr-go{display:inline-flex;align-items:center;gap:.6rem;min-height:44px;margin-top:var(--sp-2);font-size:var(--fs-body);font-weight:600;color:var(--white);text-decoration:none;
  background:linear-gradient(var(--orange),var(--orange)) 0 calc(100% - 6px)/100% 1px no-repeat;transition:background-size .6s var(--ease),color .3s var(--ease);}
.wr-go svg{width:13px;height:13px;transition:transform .5s var(--ease);}
.wr-go:hover{color:var(--orange);}
.wr-go:hover svg{transform:translateY(3px);}
.wr-hero-meta{margin:0;display:grid;gap:var(--sp-3);padding:0 0 .3rem var(--sp-3);border-left:1px solid var(--edge-hi);}
.wr-hero-meta dt{font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray-light);}
.wr-hero-meta dd{margin:.35rem 0 0;font-family:var(--font-mono);font-size:var(--fs-body-s);color:var(--white);}
.wr-hero-meta .wr-v{font-family:var(--font-display);font-weight:600;font-size:var(--fs-h2);line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums;}
.wr-hero-meta .wr-v small{font-family:var(--font-mono);font-size:var(--fs-small);font-weight:400;letter-spacing:0;color:var(--gray-light);margin-left:.4em;}
.wr-hero-meta .is-me .wr-v{color:var(--orange);}
.wr-hero-meta .wr-s{margin-top:.35rem;font-family:var(--font-body);font-size:var(--fs-small);line-height:1.4;color:var(--gray-light);}
.wr-cue{position:absolute;left:50%;bottom:var(--sp-3);z-index:5;display:grid;place-items:center;width:44px;height:44px;margin-left:-22px;border-radius:50%;
  border:1px solid var(--edge-hi);color:var(--white);transition:border-color .4s var(--ease),background-color .4s var(--ease);}
.wr-cue:hover{border-color:var(--orange);background:var(--wash);}
.wr-cue svg{width:14px;height:14px;}

/* ---------- the chapter bar: every chapter named, a reading line under each ---------- */
.wr-bar{z-index:55;}
.wr-bar-in{display:flex;align-items:center;gap:var(--sp-2);}
.wr-bar ol{position:relative;list-style:none;margin:0;padding:0;display:flex;}
.wr-bar ol a{position:relative;display:flex;align-items:center;gap:.5rem;min-height:44px;padding:0 .8rem;white-space:nowrap;text-decoration:none;
  font-size:var(--fs-small);font-weight:500;color:var(--gray-light);transition:color .3s var(--ease);}
.wr-bar ol a span{font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--gray);transition:color .3s var(--ease);}
.wr-bar ol a i{position:absolute;left:.8rem;right:.8rem;bottom:6px;height:1px;background:var(--edge);overflow:hidden;}
.wr-bar ol a i::after{content:"";position:absolute;inset:0;background:var(--orange);transform:scaleX(var(--p,0));transform-origin:0 50%;}
.wr-bar ol a:hover,.wr-bar ol a[aria-current]{color:var(--white);}
.wr-bar ol a[aria-current] span{color:var(--white);}
.wr-bar .wr-btn{flex:none;margin-left:auto;}
@media (min-width:900px){
  .wr-bar{border-block:1px solid var(--line);background:var(--wr-solid);}
  .wr-bar-in{height:var(--wr-bar);}
  .wr-bar ol{margin-left:-.8rem;}
  .wr-js .wr-bar{position:fixed;left:0;right:0;top:0;transform:translateY(-104%);transition:transform .45s var(--ease),translate .38s var(--ease);}
  .wr-js .wr-bar.is-on{transform:none;}
  html.v2-nav-up .wr-bar{translate:0 var(--v2-nav-h,77px);}
  html{scroll-padding-top:calc(var(--wr-bar,56px) + .5rem);}
}
@media (max-width:899.98px){
  .wr-bar{background:var(--wr-shade);border-top:1px solid var(--edge);}
  @supports (backdrop-filter:blur(2px)){.wr-bar{-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);}}
  .wr-bar-in{gap:.4rem;padding-block:6px calc(6px + env(safe-area-inset-bottom,0px));padding-right:calc(var(--wr-x) + 4px);}
  .wr-bar ol{flex:1 1 auto;min-width:0;overflow-x:auto;scrollbar-width:none;margin-left:calc(var(--wr-x) * -1);padding-left:calc(var(--wr-x) - .7rem);
    -webkit-mask-image:linear-gradient(90deg,transparent,var(--bg) 1rem,var(--bg) calc(100% - 1.5rem),transparent);mask-image:linear-gradient(90deg,transparent,var(--bg) 1rem,var(--bg) calc(100% - 1.5rem),transparent);}
  .wr-bar ol::-webkit-scrollbar{display:none;}
  .wr-bar ol a{padding:0 .7rem;}
  .wr-bar ol a span{display:none;}
  .wr-bar ol a i{left:.7rem;right:.7rem;bottom:4px;}
  .wr-js .wr-bar{position:fixed;left:0;right:0;bottom:0;transform:translateY(110%);transition:transform .45s var(--ease);}
  .wr-js .wr-bar.is-on{transform:none;}
  /* while the site menu is back at the top, it does the navigating: one bar at a time on a small screen */
  html.v2-nav-up.wr-js .wr-bar.is-on{transform:translateY(110%);}
}
/* a key that reaches the bar always finds it on screen */
.wr-js .wr-bar:focus-within,html.v2-nav-up.wr-js .wr-bar:focus-within{transform:none;}

/* ---------- the ticker: moves only while the page scrolls ---------- */
.wr-tick{overflow:hidden;padding-block:clamp(1.1rem,2.6vw,2.2rem);border-block:1px solid var(--line);}
.wr-tick-in{display:flex;width:max-content;}
.wr-tick-in>span{display:flex;align-items:center;flex:none;white-space:nowrap;font-family:var(--font-display);font-weight:700;
  font-size:min(calc(var(--fs-display) * 1.45),15vw);line-height:1.02;letter-spacing:-.035em;color:transparent;-webkit-text-stroke:1px var(--edge-hi);}
.wr-tick em{font-style:normal;color:var(--white);-webkit-text-stroke:0;}
.wr-tick i{flex:none;width:.14em;height:.14em;margin:0 .5em;border-radius:50%;background:var(--orange);}

/* ---------- 01 the mark to beat ---------- */
.wr-mark{padding-block:var(--wr-pad) calc(var(--wr-pad) * .55);}
.wr-duel{display:grid;margin-top:var(--sp-5);}
.wr-big{min-width:0;}
.wr-big.is-mine{justify-self:end;text-align:right;margin-top:calc(var(--wr-giga) * -.2);}
.wr-cap{margin:0 0 .4rem;font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-giga{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wr-giga);line-height:.84;letter-spacing:-.055em;color:var(--white);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.is-theirs .wr-giga{color:transparent;-webkit-text-stroke:max(1px,.005em) color-mix(in srgb,var(--white) 78%,transparent);}
.is-mine .wr-giga{color:var(--orange);}
.wr-giga small{font-size:.15em;font-weight:600;letter-spacing:0;margin-left:.35em;color:var(--gray-light);-webkit-text-stroke:0;}
.wr-meta{list-style:none;margin:var(--sp-3) 0 0;padding:0;display:flex;flex-wrap:wrap;gap:.35rem 0;font-size:var(--fs-body-s);color:var(--gray-light);}
.wr-meta li{display:flex;align-items:center;}
.wr-meta li+li::before{content:"";width:4px;height:4px;border-radius:50%;background:var(--gray);margin:0 .75rem;}
.is-mine .wr-meta{justify-content:flex-end;}
.wr-meta b{font-weight:500;color:var(--white);}
.wr-say{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:var(--sp-2) var(--sp-5);margin:var(--sp-5) 0 0;padding-top:var(--sp-3);border-top:1px solid var(--line);}
.wr-say p{margin:0;}
.wr-say .wr-t{font-family:var(--font-display);font-weight:500;font-size:var(--fs-h2);line-height:1.2;letter-spacing:-.02em;color:var(--white);}
.wr-say .wr-t b{font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;}
.wr-also{font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-more{margin-top:var(--sp-3);border-bottom:1px solid var(--line);max-width:46rem;}
.wr-more summary{display:flex;align-items:center;gap:.9rem;min-height:52px;cursor:pointer;list-style:none;width:fit-content;
  color:var(--gray-light);font-size:var(--fs-small);font-weight:600;letter-spacing:.14em;text-transform:uppercase;transition:color .3s var(--ease);}
.wr-more summary::-webkit-details-marker{display:none;}
.wr-more summary::after{content:"";width:11px;height:11px;flex:none;transition:transform .45s var(--ease);
  background:linear-gradient(currentColor,currentColor) 50% 50%/100% 1px no-repeat,linear-gradient(currentColor,currentColor) 50% 50%/1px 100% no-repeat;}
.wr-more[open] summary::after{transform:rotate(45deg);}
.wr-more summary:hover{color:var(--white);}
.wr-more p{margin:0 0 1rem;font-size:var(--fs-body-s);line-height:1.65;color:var(--gray-light);max-width:44rem;}
/* a number that counts keeps the width of its final value */
.wr-count{display:inline-grid;}
.wr-count>span,.wr-count::after{grid-area:1/1;}
.wr-count::after{content:attr(data-final);visibility:hidden;}
.is-mine .wr-count>span{text-align:right;}

/* ---------- 02 the course, pinned and flown ---------- */
.wr-course{position:relative;background:var(--wr-deep);}
.wr-course .wr-stage{position:relative;padding-block:var(--wr-pad);}
.wr-course-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:var(--sp-3) var(--sp-4);}
.wr-seg{position:relative;display:inline-flex;gap:3px;margin:0;padding:3px;min-width:0;border:1px solid var(--edge);}
.wr-seg legend{position:absolute;width:1px;height:1px;padding:0;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
.wr-seg input{position:absolute;opacity:0;width:1px;height:1px;margin:0;}
.wr-seg label{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:5.6rem;padding:0 1rem;cursor:pointer;
  font:600 var(--fs-body-s)/1 var(--font-body);color:var(--gray-light);transition:background-color .35s var(--ease),color .35s var(--ease);}
.wr-seg label:hover{color:var(--white);}
.wr-seg input:checked+label{background:var(--white);color:var(--bg);}
.wr-seg input:focus-visible+label{outline:2px solid var(--white);outline-offset:2px;}
/* the switch without a script: two radio buttons and :has */
.wr-course:not(:has(#wrk200:checked)) .v200,.wr-course:has(#wrk200:checked) .v100{display:none;}
.wr-map{position:relative;isolation:isolate;margin:clamp(2.6rem,7vh,4.6rem) 0 clamp(1.6rem,4vh,2.8rem);}
.wr-box{position:relative;}
.wr-box svg{display:block;width:100%;height:clamp(120px,21vh,200px);overflow:visible;}
.wr-lane{fill:none;stroke:var(--edge-hi);stroke-width:1.5;vector-effect:non-scaling-stroke;}
.wr-lane.is-200{stroke:var(--edge);stroke-dasharray:3 7;}
.wr-course:has(#wrk200:checked) .wr-lane.is-200{stroke:var(--edge-hi);stroke-dasharray:none;}
.wr-glow{fill:none;stroke:color-mix(in srgb,var(--orange) 26%,transparent);stroke-width:13;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;}
.wr-flown{fill:none;stroke:var(--orange);stroke-width:4;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;}
.wr-gate{stroke:var(--white);stroke-width:2;vector-effect:non-scaling-stroke;}
.wr-tk{stroke:var(--edge-hi);stroke-width:1;vector-effect:non-scaling-stroke;}
.wr-pl{position:absolute;bottom:calc(100% + .7rem);left:0;white-space:nowrap;font-size:var(--fs-small);line-height:1.3;color:var(--white);}
.wr-pl i{display:block;font-style:normal;font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-tp{position:absolute;top:0;bottom:0;width:0;}
.wr-tp .wr-pl{transform:translateX(-50%);text-align:center;}
.wr-tp.v200 .wr-pl{transform:translateX(-100%);text-align:right;}
.wr-ring{position:absolute;left:0;top:50%;width:2.8rem;height:2.8rem;margin:-1.4rem 0 0 -1.4rem;box-sizing:border-box;border-radius:50%;border:1px dashed var(--gray-light);}
.wr-ring::after{content:"";position:absolute;left:50%;top:50%;width:7px;height:7px;margin:-3.5px 0 0 -3.5px;border-radius:50%;background:var(--white);}
.wr-gl{position:absolute;left:3%;top:75%;width:34px;height:34px;margin:-17px 0 0 -17px;transform:rotate(180deg);pointer-events:none;}
.wr-gl::before{content:"";position:absolute;inset:-16px;border-radius:50%;
  background:radial-gradient(circle,color-mix(in srgb,var(--orange) 46%,transparent) 0%,color-mix(in srgb,var(--orange) 14%,transparent) 42%,transparent 70%);}
.wr-gl svg{position:relative;display:block;width:100%;height:100%;overflow:visible;}
.wr-gl .g-w{fill:none;stroke:var(--orange);stroke-width:3.6;stroke-linecap:round;}
.wr-gl .g-l{fill:none;stroke:var(--white);stroke-width:.9;opacity:.75;}
.wr-gl .g-p{fill:var(--white);}
.wr-map.is-live .wr-gl{left:0;top:0;will-change:transform;}
.wr-scale{position:relative;height:1.6em;margin-top:.8rem;font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-scale span{position:absolute;top:0;transform:translateX(-50%);white-space:nowrap;}
.wr-scale span:first-child{transform:translateX(-30%);}
.wr-scale span:last-child{transform:translateX(-80%);}
.wr-read{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1fr) minmax(0,1.15fr) minmax(0,1.15fr);gap:var(--sp-4);margin:0;padding-top:var(--sp-3);border-top:1px solid var(--edge);}
.wr-read dt{font-family:var(--font-mono);font-size:var(--fs-small);line-height:1.35;color:var(--gray-light);}
.wr-read dd{margin:.6rem 0 0;font-family:var(--font-display);font-weight:500;font-size:calc(var(--fs-h2) * 1.45);line-height:1;letter-spacing:-.035em;color:var(--white);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.wr-read dd b{font-weight:500;}
.wr-read dd small{font-size:.36em;font-weight:500;letter-spacing:.02em;color:var(--gray-light);margin:0 .5em 0 .18em;}
.wr-read dd small:last-child{margin-right:0;}
.wr-read dd .wr-tbd{font-size:.42em;letter-spacing:0;}
.wr-read .is-leg dd{font-size:calc(var(--fs-h2) * 1.2);}
.wr-read .is-me dd{color:var(--orange);}
.wr-read .is-me dt::before{content:"";display:inline-block;width:7px;height:7px;margin-right:.45rem;border-radius:50%;background:var(--orange);vertical-align:.05em;}
.wr-km{display:none;}
/* a counting kilometre figure keeps three digits of room, so nothing beside it moves */
#wrKm,#wrKmBig{display:inline-block;min-width:3ch;text-align:right;}

/* ---------- 03 Kerio Valley ---------- */
.wr-place{padding-top:var(--wr-pad);}
.wr-cut{width:fit-content;max-width:100%;margin:0;font-family:var(--font-display);font-weight:700;font-size:min(calc(var(--fs-display) * 3),22vw);
  line-height:.86;letter-spacing:-.05em;color:var(--white);}
.wr-cut span{display:block;}
@supports ((-webkit-background-clip:text) or (background-clip:text)){
  /* the photograph inside the letters, over a plain fill, so the name shows before the photograph arrives */
  .wr-cut{color:transparent;background:url("__KERIO__.webp") 50% 58%/cover no-repeat,var(--gray-light);
    -webkit-background-clip:text;background-clip:text;filter:saturate(1.15) brightness(1.2);}
  .wr-js .wr-cut:not(.is-near){background:var(--gray-light);-webkit-background-clip:text;background-clip:text;}
}
.wr-plate{position:relative;margin:var(--sp-5) 0 0;}
.wr-plate-img{position:relative;height:min(80svh,54rem);overflow:hidden;}
.wr-par{position:absolute;inset:0;}
.wr-par img{width:100%;height:100%;object-fit:cover;}
.wr-plate-img::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,var(--bg) 0%,transparent 22%,transparent 46%,color-mix(in srgb,var(--bg) 94%,transparent) 100%);}
.wr-facts{position:absolute;left:0;right:0;bottom:0;z-index:2;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-4);
  box-sizing:border-box;max-width:var(--measure);margin:0 auto;padding:0 var(--wr-x) var(--sp-5);}
.wr-facts div{padding-top:var(--sp-2);border-top:1px solid var(--edge-hi);}
.wr-facts dt{font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--gray-light);}
.wr-facts dd{margin:.45rem 0 0;font-size:var(--fs-body);line-height:1.35;color:var(--white);}
.wr-vario{display:block;width:100%;max-width:14rem;height:auto;margin:.7rem 0 0;overflow:visible;}
.wr-vario .v-base,.wr-vario .v-tk{stroke:var(--gray-light);stroke-width:1;}
.wr-vario .v-n{fill:var(--gray-light);font-family:var(--font-mono);font-size:11px;text-anchor:middle;}
.wr-vario .v-pk{fill:var(--orange);}
.wr-vario .v-rr{fill:url(#wrHatch);stroke:var(--orange);stroke-width:1;}
.wr-vario .v-ht{stroke:var(--orange);stroke-width:1.4;}

/* ---------- 04 the window ---------- */
.wr-win .wr-stage{padding-block:var(--wr-pad);}
.wr-win-in{display:grid;grid-template-columns:minmax(0,1fr);grid-template-areas:"head" "days" "vp";gap:var(--sp-5);}
.wr-win-head{grid-area:head;}
.wr-win .wr-h2{max-width:9ch;}
.wr-win .wr-lede{margin-top:var(--sp-2);}
/* the 26 days: two expeditions and the two days between */
.wr-days{grid-area:days;min-width:0;}
.wr-days-k,.wr-days-bar,.wr-days-n{display:grid;grid-template-columns:repeat(26,minmax(0,1fr));gap:3px;}
.wr-days-k{margin-bottom:.8rem;}
.wr-days-k>span{display:flex;flex-direction:column;gap:.2rem;padding-left:.7rem;border-left:1px solid var(--orange);font-size:var(--fs-body-s);line-height:1.3;color:var(--gray-light);}
.wr-days-k>span:first-child{grid-column:1/13;}
.wr-days-k>span:last-child{grid-column:15/27;}
.wr-days-k a{display:inline-flex;align-items:center;min-height:44px;margin:-.5rem 0 -.4rem;width:fit-content;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);color:var(--white);}
.wr-days-bar i{display:block;height:2.6rem;background:var(--orange);transform-origin:50% 100%;}
.wr-days-bar i.is-off{background:none;border:1px dashed var(--edge-hi);}
.wr-days-n{margin-top:.5rem;font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--gray);text-align:center;}
.wr-days-n span{min-width:0;}
.wr-days-dur{display:flex;flex-wrap:wrap;align-items:baseline;gap:.4rem 1rem;margin:var(--sp-3) 0 0;padding-top:.9rem;border-top:1px solid var(--live);font-size:var(--fs-body);line-height:1.45;color:var(--white);}
.wr-days-dur b{font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gray-light);}
/* before and after: a strip */
.wr-vp{grid-area:vp;min-width:0;}
.wr-track{display:flex;align-items:stretch;}
.wr-steps{list-style:none;margin:0;padding:0;display:flex;}
.wr-step{position:relative;flex:0 0 min(19rem,76vw);box-sizing:border-box;padding:var(--sp-4) var(--sp-5) var(--sp-2) 0;border-top:1px solid var(--edge);}
.wr-step::before{content:"";position:absolute;left:0;top:-5px;width:9px;height:9px;box-sizing:border-box;border-radius:50%;background:var(--bg);border:1px solid var(--gray-light);}
.wr-when{display:block;margin:0 0 var(--sp-2);font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-step h3{margin:0;font-family:var(--font-display);font-weight:600;font-size:calc(var(--fs-h3) * 1.15);line-height:1.15;color:var(--white);}
.wr-step p{margin:.7rem 0 0;max-width:16rem;font-size:var(--fs-body);line-height:1.5;color:var(--gray-light);}
.wr-step p a{display:inline-flex;align-items:center;min-height:44px;}
.wr-fig{position:relative;flex:0 0 min(18rem,60vw);margin:0 var(--sp-5) 0 0;overflow:hidden;align-self:stretch;}
.wr-fig img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:56% 50%;transition:transform 1.4s var(--ease);}
.wr-fig:hover img{transform:scale(1.05);}
.wr-swipe{display:none;}

/* ---------- 05 the audience ---------- */
.wr-aud{padding-block:var(--wr-pad);}
.wr-aud-in{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,.85fr);grid-template-areas:"copy pic" "stats pic";column-gap:clamp(2rem,6vw,6rem);}
.wr-aud-copy{grid-area:copy;}
.wr-portrait{grid-area:pic;position:relative;margin:calc(var(--sp-5) * 1.6) 0 0;align-self:start;aspect-ratio:4/5;overflow:hidden;}
.wr-portrait figcaption{position:absolute;left:var(--sp-3);bottom:var(--sp-3);z-index:1;font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--white);
  text-shadow:0 1px 3px color-mix(in srgb,var(--bg) 90%,transparent);}
.wr-portrait::after{content:"";position:absolute;inset:55% 0 0;background:linear-gradient(180deg,transparent,color-mix(in srgb,var(--bg) 70%,transparent));pointer-events:none;}
.wr-stats{grid-area:stats;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-5) var(--sp-4);margin:var(--sp-5) 0 0;}
.wr-stats div{display:flex;flex-direction:column-reverse;justify-content:flex-end;padding-top:var(--sp-3);border-top:1px solid var(--edge);}
.wr-stats dd{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-display) * .95);line-height:1;letter-spacing:-.04em;color:var(--white);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.wr-stats dt{margin-top:.6rem;font-size:var(--fs-body-s);color:var(--gray-light);}

/* ---------- 06 the offer ---------- */
.wr-offer{padding-block:var(--wr-pad) var(--sp-section);background:radial-gradient(70% 60% at 85% 0%,var(--sky-warm),transparent 70%);}
.wr-offer-head{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(2rem,6vw,6rem);align-items:end;}
.wr-offer-pic{position:relative;margin:0;aspect-ratio:4/3;overflow:hidden;}
.wr-offer-pic img{transition:transform 1.4s var(--ease);}
.wr-offer-pic:hover img{transform:scale(1.04);}
.wr-tiers{display:grid;grid-template-columns:minmax(0,1.2fr) repeat(2,minmax(0,1fr));gap:var(--sp-3);margin-top:var(--sp-5);}
.wr-tier{position:relative;padding:var(--sp-4);border-top:1px solid var(--edge-hi);
  background:linear-gradient(180deg,color-mix(in srgb,var(--white) 6%,transparent),color-mix(in srgb,var(--white) 1.5%,transparent) 70%);}
.wr-tier.is-lead{border-top:2px solid var(--orange);background:linear-gradient(180deg,color-mix(in srgb,var(--orange) 9%,transparent),color-mix(in srgb,var(--white) 2%,transparent) 70%);}
.wr-tier::after{content:"";position:absolute;left:0;top:0;width:2px;height:0;background:var(--orange);transition:height .6s var(--ease);}
.wr-tier:hover::after,.wr-tier:focus-within::after{height:3.5rem;}
.wr-tier-n{margin:0 0 var(--sp-3);font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-display) * 1.05);line-height:.9;letter-spacing:-.04em;
  color:transparent;-webkit-text-stroke:1px var(--edge-hi);}
.wr-tier.is-lead .wr-tier-n{-webkit-text-stroke-color:var(--orange);}
.wr-tier-k{position:absolute;top:var(--sp-4);right:var(--sp-4);margin:0;padding:.2rem .5rem;border:1px solid var(--live);font-family:var(--font-mono);font-size:var(--fs-micro);line-height:1.4;color:var(--gray-light);}
.wr-tier h3{margin:0 0 var(--sp-3);font-family:var(--font-display);font-weight:700;font-size:var(--fs-h3);line-height:1.1;color:var(--white);}
.wr-tier ul{list-style:none;margin:0;padding:0;display:grid;gap:.15rem;}
.wr-tier li{position:relative;padding:.5rem 0 .5rem 1.2rem;border-top:1px solid var(--line);font-size:var(--fs-body);line-height:1.45;color:color-mix(in srgb,var(--white) 88%,var(--gray-light));}
.wr-tier li::before{content:"";position:absolute;left:0;top:1.2em;width:.5rem;height:2px;background:var(--orange);}
.wr-cta{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-3) var(--sp-5);margin-top:var(--sp-5);}
.wr-mag{display:inline-block;padding:16px;margin:-16px;transition:transform .7s var(--ease);}
.wr-cta .btn-solid{margin:0;font-size:var(--fs-lead);padding:1.05rem 2.3rem;}
.wr-cta .btn-lines{display:inline-flex;align-items:center;min-height:48px;box-sizing:border-box;font-size:var(--fs-lead);}
.wr-cta .btn-lines:hover{color:var(--orange);border-color:var(--orange);}
.wr-src{margin:var(--sp-5) 0 0;font-size:var(--fs-small);line-height:1.8;color:var(--gray);}

/* ---------- image reveals and depth ---------- */
.wr-rv{clip-path:inset(0);}
.wr-par img,.wr-offer-pic img,.wr-portrait img{display:block;width:100%;height:100%;object-fit:cover;}

/* ---------- the ring cursor (fine pointers only; made by the script) ---------- */
.wr-cursor{position:fixed;left:0;top:0;z-index:250;width:0;height:0;pointer-events:none;opacity:0;transition:opacity .3s var(--ease);}
.wr-cursor.is-on{opacity:1;}
.wr-cursor i{position:absolute;left:-17px;top:-17px;width:34px;height:34px;box-sizing:border-box;border-radius:50%;border:1px solid color-mix(in srgb,var(--white) 55%,transparent);
  transition:transform .5s var(--ease),background-color .5s var(--ease),border-color .5s var(--ease);}
.wr-cursor.is-big i{transform:scale(1.75);background:color-mix(in srgb,var(--orange) 12%,transparent);border-color:var(--live);}
.wr-cursor.is-map i{transform:scale(2.5);background:transparent;border-color:color-mix(in srgb,var(--orange) 70%,transparent);}

/* ---------- motion: only in answer to the visitor, and none of it when they ask for stillness ---------- */
@media (prefers-reduced-motion:no-preference){
  .wr-js .wr-k :is(.wr-w,.wr-ln)>span{transform:translateY(112%);transition:transform 1.05s var(--ease);transition-delay:calc(var(--i,0) * 70ms);}
  .wr-js .wr-k.is-in :is(.wr-w,.wr-ln)>span{transform:none;}
  .wr-js .wr-fade{opacity:0;transform:translateY(1.4rem);transition:opacity 1s var(--ease) .3s,transform 1s var(--ease) .3s;}
  .wr-js .wr-fade.is-in{opacity:1;transform:none;}
  .wr-js .wr-cut{transition:clip-path 1.3s var(--ease),transform 1.3s var(--ease);}
  .wr-js .wr-cut:not(.is-in){clip-path:inset(0 0 100% 0);transform:translateY(10%);}
  .wr-js .wr-rv{transition:clip-path 1.5s var(--ease);}
  .wr-js .wr-rv:not(.is-in){clip-path:inset(14% 9% 14% 9%);}
  .wr-js .wr-rv img{transition:transform 1.8s var(--ease);}
  .wr-js .wr-rv:not(.is-in) img{transform:scale(1.18);}
  .wr-js .wr-days-bar i{transition:transform .9s var(--ease) calc(var(--d) * 32ms);}
  .wr-js .wr-days:not(.is-in) .wr-days-bar i{transform:scaleY(.06);}
  .wr-pin .wr-stage>.wr-in{transition:translate .38s var(--ease);}
  html{scroll-behavior:smooth;}
}
@supports (animation-timeline:view()){
  @media (prefers-reduced-motion:no-preference){
    .wr-hero-pic{animation:wr-sink linear both;animation-timeline:view();animation-range:exit 0% exit 100%;}
    .wr-hero-in{animation:wr-lift linear both;animation-timeline:view();animation-range:exit 0% exit 100%;}
    @keyframes wr-sink{to{transform:translateY(16%) scale(1.06);}}
    @keyframes wr-lift{to{transform:translateY(-12vh);opacity:0;}}
    .wr-par{animation:wr-drift linear both;animation-timeline:view();animation-range:cover 0% cover 100%;}
    @keyframes wr-drift{from{transform:translateY(-7%) scale(1.15);}to{transform:translateY(7%) scale(1.15);}}
  }
}
@media (prefers-reduced-motion:reduce){
  .wr *,.wr *::before,.wr *::after{transition:none!important;}
}

/* ---------- pinned chapters (set before the first paint by the script at the top of main) ---------- */
.wr-pin .wr-course{height:200vh;}
.wr-pin .wr-course .wr-stage{position:sticky;top:0;box-sizing:border-box;height:100svh;padding-block:calc(var(--wr-bar) + var(--sp-3)) var(--sp-3);display:flex;align-items:center;overflow:hidden;}
.wr-pin .wr-km{display:block;position:absolute;z-index:-1;right:-.04em;top:50%;transform:translateY(-54%);margin:0;pointer-events:none;white-space:nowrap;
  font-family:var(--font-display);font-weight:700;font-size:min(32vh,19vw);line-height:.8;letter-spacing:-.06em;color:transparent;
  -webkit-text-stroke:1px color-mix(in srgb,var(--white) 14%,transparent);font-variant-numeric:tabular-nums;}
.wr-pin .wr-km small{font-size:.22em;letter-spacing:0;margin-left:.12em;}
html.v2-nav-up.wr-pin .wr-stage>.wr-in{translate:0 calc(var(--v2-nav-h,77px) * .8);}
.wr-hz .wr-win .wr-stage{position:sticky;top:0;box-sizing:border-box;height:100svh;padding-block:calc(var(--wr-bar) + var(--sp-3)) var(--sp-3);display:flex;align-items:center;overflow:hidden;}

/* ---------- wide screens: the window's title and days hold while the strip passes ---------- */
@media (min-width:900px){
  .wr-win-in{grid-template-columns:minmax(0,20rem) minmax(0,1fr);grid-template-areas:"head days" "vp vp";column-gap:var(--sp-5);align-items:end;}
  :root:not(.wr-hz) .wr-track{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-4);}
  :root:not(.wr-hz) .wr-steps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-4);}
  :root:not(.wr-hz) .wr-step{padding-right:0;}
  :root:not(.wr-hz) .wr-fig{display:none;}
  .wr-hz .wr-win-in{grid-template-areas:"head vp" "days days";row-gap:clamp(2rem,6vh,4rem);align-items:center;}
  .wr-hz .wr-vp{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,var(--bg) 9%,var(--bg) 90%,transparent);mask-image:linear-gradient(90deg,transparent,var(--bg) 9%,var(--bg) 90%,transparent);}
  .wr-hz .wr-track{padding:var(--sp-3) 0 0 var(--sp-3);width:max-content;will-change:transform;}
  .wr-hz .wr-fig{height:auto;min-height:15rem;}
}

/* ---------- tablets and phones ---------- */
@media (max-width:899.98px){
  /* the photograph above the words, so the type sits on dark ground */
  .wr-hero{--wr-ph:clamp(17rem,40svh,30rem);min-height:0;display:block;padding-top:calc(var(--wr-ph) - 3.4rem);}
  .wr-hero-pic{inset:0 0 auto 0;height:var(--wr-ph);}
  .wr-hero-pic img{object-position:81% 44%;}
  .wr-hero::before{background:linear-gradient(180deg,color-mix(in srgb,var(--bg) 30%,transparent) 0%,transparent 18%,transparent calc(var(--wr-ph) - 7rem),var(--bg) calc(var(--wr-ph) - .5rem));}
  /* the title, then the numbers, then the line and the way down: what, why and when on the first screen */
  .wr-hero-in{grid-template-columns:minmax(0,1fr);gap:0;padding-block:0 calc(var(--sp-5) + 1rem);}
  .wr-hero-in>div:first-child{display:contents;}
  .wr-kick{order:1;}
  .wr-mega{order:2;}
  .wr-hero-meta{order:3;}
  .wr-hero-sub{order:4;}
  .wr-go{order:5;justify-self:start;}
  .wr-mega .is-hollow{-webkit-text-stroke-width:max(1.5px,.016em);}
  .wr-hero-sub{margin-top:var(--sp-3);}
  .wr-hero-meta{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:var(--sp-3);margin-top:var(--sp-4);border-left:0;padding:var(--sp-3) 0 0;border-top:1px solid var(--edge-hi);}
  .wr-cue{display:none;}
  .wr-big.is-mine{margin-top:var(--sp-5);}
  .wr-read{grid-template-columns:minmax(0,1fr);gap:0;}
  .wr-read div{display:flex;align-items:baseline;justify-content:space-between;gap:var(--sp-2);padding:.6rem 0;border-bottom:1px solid var(--line);}
  .wr-read dd,.wr-read .is-leg dd{margin:0;font-size:calc(var(--fs-h2) * 1.05);}
  .wr-pin .wr-course .wr-stage{padding-block:var(--sp-3) calc(var(--sp-3) + var(--wr-dock));}
  .wr-facts{position:static;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-3);padding-top:var(--sp-3);padding-bottom:0;}
  .wr-plate-img{height:62svh;}
  .wr-plate-img::after{background:linear-gradient(180deg,var(--bg) 0%,transparent 18%,transparent 75%,var(--bg) 100%);}
  .wr-vp{margin-inline:calc(var(--wr-x) * -1);}
  .wr-track{overflow-x:auto;scroll-snap-type:x mandatory;overscroll-behavior-x:contain;scrollbar-width:none;padding:var(--sp-3) var(--wr-x) var(--sp-2);scroll-padding-inline:var(--wr-x);}
  .wr-track::-webkit-scrollbar{display:none;}
  .wr-step{scroll-snap-align:start;padding-right:var(--sp-4);}
  .wr-fig{display:none;}
  .wr-swipe{display:block;position:relative;height:2px;margin:var(--sp-2) var(--wr-x) 0;background:var(--line);}
  .wr-swipe i{position:absolute;inset:0;background:var(--orange);transform:scaleX(var(--p,.25));transform-origin:0 50%;}
  .wr-aud-in{grid-template-columns:minmax(0,1fr);grid-template-areas:"copy" "pic" "stats";}
  .wr-portrait{justify-self:end;width:min(62%,20rem);margin-top:var(--sp-4);}
  .wr-offer{padding-bottom:calc(var(--sp-section) + var(--wr-dock));}
  .wr-offer-head{grid-template-columns:minmax(0,1fr);}
  .wr-tiers{grid-template-columns:repeat(2,minmax(0,1fr));}
  .wr-tier.is-lead{grid-column:1/-1;}
}
@media (max-width:560px){
  .wr-kick span{display:block;}
  .wr-kick .wr-sep{display:none;}
  .wr-hero-meta{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:var(--sp-2);}
  .wr-hero-meta .is-win{grid-column:1/-1;display:flex;align-items:baseline;gap:.8rem;}
  .wr-hero-meta .is-win dd{margin:0;}
  .wr-hero-meta .wr-v{font-size:calc(var(--fs-h2) * 1.15);}
  .wr-meta{flex-direction:column;gap:.25rem;}
  .wr-meta li+li::before{display:none;}
  .wr-meta a{display:inline-flex;align-items:center;min-height:44px;}
  .is-mine .wr-meta{align-items:flex-end;}
  .wr-say .wr-t{font-size:var(--fs-h3);}
  .wr-map{margin:var(--sp-5) 0 var(--sp-3);}
  .wr-pin .wr-course{height:190vh;}
  .wr-pin .wr-km{display:none;}
  .wr-course-head .wr-h2{font-size:calc(var(--fs-h1) * 1.05);}
  .wr-ring{width:2rem;height:2rem;margin:-1rem 0 0 -1rem;}
  .wr-scale span:nth-child(even){display:none;}
  .wr-facts{grid-template-columns:minmax(0,1fr);}
  .wr-days-n{display:none;}
  .wr-days-bar i{height:2.2rem;}
  .wr-days-k a{font-size:var(--fs-body);}
  .wr-stats{gap:var(--sp-4) var(--sp-3);}
  .wr-stats dd{font-size:calc(var(--fs-display) * .82);}
  .wr-tiers{grid-template-columns:minmax(0,1fr);}
  .wr-cta{flex-direction:column;align-items:flex-start;}
}
/* ---------- the record day: the backgrounds (see the docstring) ---------- */
/* small muted words sit on a sky now, not flat black: lifted enough to keep 4.5:1 on its brightest */
.wr{--wr-dim:color-mix(in srgb,var(--gray-light) 84%,var(--gray));
  --wr-land:color-mix(in srgb,var(--ink) 72%,var(--bg));
  /* a cloud's lit colour: a warm white held at the sky's brightness limit, so a cloud lightens the sky and never lifts it past what the words need */
  --wr-cloud:color-mix(in srgb,var(--white) 18.5%,var(--bg));
  --wr-cloud-dusk:color-mix(in srgb,color-mix(in srgb,var(--orange) 80%,var(--white)) 26%,var(--bg));}
.wr-tbd,.wr-no,.wr-src,.wr-days-n{color:var(--wr-dim);}
.wr-mark,.wr-offer{position:relative;isolation:isolate;}
.wr-sky,.wr-night,.wr-still-rg{display:none;}
.wr-defs{position:absolute;width:0;height:0;overflow:hidden;}
/* the partner cards are solid: neither the sky nor the hills show through the offer */
.wr .wr-tier{background:linear-gradient(180deg,color-mix(in srgb,var(--white) 6%,transparent),color-mix(in srgb,var(--white) 1.5%,transparent) 70%),color-mix(in srgb,var(--card) 94%,var(--bg));}
.wr .wr-tier.is-lead{background:linear-gradient(180deg,color-mix(in srgb,var(--orange) 9%,transparent),color-mix(in srgb,var(--white) 2%,transparent) 70%),color-mix(in srgb,var(--card) 94%,var(--bg));}
/* the course's grain fades at both ends, so no line marks its edges (with the moving sky the page's own grain is there instead) */
.wr-sky-on .wr-course.wr-grain::after{display:none;}
.wr-course.wr-grain::after{-webkit-mask-image:linear-gradient(180deg,transparent,var(--bg) 16%,var(--bg) 84%,transparent);mask-image:linear-gradient(180deg,transparent,var(--bg) 16%,var(--bg) 84%,transparent);}

/* ----- the horizon: the escarpment and the hills (drawn once in .wr-defs, used by the moving and the still page) ----- */
.wr-rg{position:absolute;inset:0;}
.wr-rg svg{position:absolute;left:0;top:0;display:block;width:100%;height:100%;overflow:visible;}
.wr-rg .is-p{display:none;}
@media (max-width:560px){.wr-rg .is-w{display:none;}.wr-rg .is-p{display:block;}}
.r-far2{fill:var(--bg);fill-opacity:.26;}
.r-far{fill:var(--bg);fill-opacity:.44;}
.r-tug{fill:url(#wrHaze);}
.r-esc{fill:url(#wrWall);}
.r-near{fill:var(--wr-land);}
.wr-still-rg .h1{stop-color:color-mix(in srgb,var(--bg) 86%,var(--gray-light));}
.wr-still-rg .h2{stop-color:color-mix(in srgb,var(--bg) 70%,var(--ink));}
.wr-still-rg .w1{stop-color:color-mix(in srgb,var(--bg) 93%,var(--gray-light));}
.wr-still-rg .w2{stop-color:color-mix(in srgb,var(--bg) 60%,var(--ink));}
/* morning: the sun comes up behind the Tugen Hills (left), lights the escarpment's east face (right) */
.r-face{fill:url(#wrLit);}
.wr-still-rg .g1{stop-color:color-mix(in srgb,var(--orange) 62%,var(--white));stop-opacity:.24;}
.wr-still-rg .g2{stop-color:color-mix(in srgb,var(--orange) 70%,var(--white));stop-opacity:.08;}
.wr-still-rg .g3{stop-color:var(--orange);stop-opacity:0;}
.r-gul{fill:none;stroke:var(--bg);stroke-opacity:.6;stroke-width:1.3;stroke-linecap:round;vector-effect:non-scaling-stroke;}
.r-trim{fill:none;stroke:color-mix(in srgb,var(--orange) 55%,var(--white));stroke-opacity:.7;stroke-width:1.2;stroke-linejoin:round;vector-effect:non-scaling-stroke;}
/* dusk: the sun goes down behind the escarpment (right), rims its edge, and the Tugen Hills' west slopes glow */
.r-tface{fill:url(#wrGlow);}
.wr-still-rg .p1{stop-color:color-mix(in srgb,var(--orange) 70%,var(--sky-cool));stop-opacity:.2;}
.wr-still-rg .p2{stop-color:var(--orange);stop-opacity:0;}
.r-rim{fill:none;stroke:var(--orange);stroke-width:1.5;stroke-linejoin:round;vector-effect:non-scaling-stroke;}
/* the thermals' streamlines and bubbles fade at both ends through their own stroke */
.wr-defs .f0{stop-color:var(--gray-light);stop-opacity:0;}
.wr-defs .f1{stop-color:var(--gray-light);stop-opacity:1;}
.wr-defs .q0{stop-color:color-mix(in srgb,var(--orange) 50%,var(--white));stop-opacity:0;}
.wr-defs .q1{stop-color:color-mix(in srgb,var(--orange) 50%,var(--white));stop-opacity:1;}

/* ----- the still day (no script, or reduced motion): one gradient down the whole page, every stop under the
   moving sky's brightness limit (checked with each of the site's four skies), the horizon drawn at three edges ----- */
.wr{--wr-s0:color-mix(in srgb,var(--bg) 62%,var(--sky-cool));
  --wr-s1:color-mix(in srgb,color-mix(in srgb,var(--bg) 84%,color-mix(in srgb,var(--white) 62%,var(--orange))) 88%,var(--sky-cool));
  --wr-s2:color-mix(in srgb,var(--bg) 82%,color-mix(in srgb,var(--orange) 38%,var(--white)));
  --wr-s3:color-mix(in srgb,color-mix(in srgb,var(--bg) 50%,var(--sky-cool)) 94%,var(--white));
  --wr-s4:color-mix(in srgb,color-mix(in srgb,var(--bg) 46%,var(--sky-cool)) 93%,var(--white));
  --wr-s5:color-mix(in srgb,color-mix(in srgb,var(--bg) 66%,var(--sky-cool)) 90%,color-mix(in srgb,var(--orange) 40%,var(--white)));
  --wr-s6:color-mix(in srgb,color-mix(in srgb,var(--bg) 80%,color-mix(in srgb,var(--orange) 62%,var(--white))) 86%,var(--sky-cool));
  --wr-s7:color-mix(in srgb,color-mix(in srgb,var(--bg) 70%,var(--sky-cool)) 94%,color-mix(in srgb,var(--orange) 50%,var(--white)));
  --wr-s8:color-mix(in srgb,var(--bg) 66%,var(--sky-cool));}
:root:not(.wr-sky-on) .wr{background:linear-gradient(180deg,var(--bg) 0,var(--bg) @@S0@@%,var(--wr-s0) @@S1@@%,var(--wr-s1) @@S2@@%,var(--wr-s2) @@S3@@%,
  var(--wr-s3) @@S4@@%,var(--wr-s4) @@S5@@%,var(--wr-s3) @@S6@@%,var(--wr-s5) @@S7@@%,var(--wr-s6) @@S8@@%,var(--wr-s7) @@S9@@%,var(--wr-s8) @@S10@@%,var(--wr-s8));}
:root:not(.wr-sky-on) .wr-course,:root:not(.wr-sky-on) .wr-offer{background:none;}
:root:not(.wr-sky-on) .wr-still-rg{display:block;position:absolute;left:0;right:0;z-index:-1;height:clamp(120px,21vw,300px);pointer-events:none;
  -webkit-mask-image:linear-gradient(180deg,var(--bg) 62%,transparent);mask-image:linear-gradient(180deg,var(--bg) 62%,transparent);}
.wr-still-rg.at-01,.wr-still-rg.at-06{top:0;}
.wr-still-rg.at-end{bottom:0;-webkit-mask-image:none;mask-image:none;}
:root:not(.wr-sky-on) .wr-night{display:block;position:absolute;left:0;right:0;bottom:clamp(60px,9vw,150px);z-index:-1;height:min(110vh,80%);pointer-events:none;
  -webkit-mask-image:linear-gradient(180deg,transparent,var(--bg) 60%);mask-image:linear-gradient(180deg,transparent,var(--bg) 60%);}
.wr-night svg{display:block;width:100%;height:100%;}
@media (max-width:899.98px){:root:not(.wr-sky-on) .wr-still-rg.at-end{bottom:var(--wr-dock);}}

/* ----- the moving sky (with the script and motion): one canvas, fixed behind everything ----- */
.wr-sky-on .wr-sky{display:block;position:fixed;left:0;top:0;z-index:-1;width:100%;height:100vh;height:100lvh;overflow:hidden;pointer-events:none;contain:strict;background:var(--wr-s0);}
.wr-sky-c,.wr-sky-o{position:absolute;left:0;top:0;width:100%;height:100%;display:block;}
/* the page's still grain, in the page itself (no layer of its own): film texture on every chapter, and no banding in the sky's gradients */
.wr-sky-on .wr{background-image:__GRAIN2__;background-size:220px 220px;}
/* the star dots, as the still page's night uses them (sizes in the drawing's units) */
.wr .z0,.wr .z1,.wr .z2,.wr .z3,.wr .z4{fill:none;stroke-linecap:round;}
.wr .z0{stroke-width:9.5;}.wr .z1{stroke-width:7.5;}.wr .z2{stroke-width:5.8;}.wr .z3{stroke-width:4.6;opacity:.82;}.wr .z4{stroke-width:3.6;opacity:.55;}
.wr .tw,.wr .tb{stroke:var(--white);}.wr .ty{stroke:color-mix(in srgb,var(--white) 80%,var(--orange));}.wr .tr{stroke:color-mix(in srgb,var(--white) 58%,var(--orange));}

/* the chapters let the sky through */
.wr-sky-on .wr-hero,.wr-sky-on .wr-course,.wr-sky-on .wr-offer{background:none;}
.wr-sky-on .wr-hero.wr-grain::after{-webkit-mask-image:linear-gradient(180deg,var(--bg) 60%,transparent);mask-image:linear-gradient(180deg,var(--bg) 60%,transparent);}
/* the opening photograph: whole until its last seventh, its own shade fading with it, so nothing of the
   sky shows through the pilot and no band marks where the photograph ends */
.wr-sky-on .wr-hero::before{background:
  linear-gradient(90deg,color-mix(in srgb,var(--bg) 80%,transparent) 0%,color-mix(in srgb,var(--bg) 38%,transparent) 46%,transparent 72%),
  linear-gradient(180deg,color-mix(in srgb,var(--bg) 45%,transparent) 0%,transparent 24%);}
.wr-sky-on .wr-hero-pic{-webkit-mask-image:linear-gradient(180deg,var(--bg) 86%,transparent);mask-image:linear-gradient(180deg,var(--bg) 86%,transparent);}
.wr-sky-on .wr-hero-pic::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 46%,color-mix(in srgb,var(--bg) 70%,transparent) 78%,var(--bg) 100%);}
/* the Kerio photograph fades into whatever sky is behind it (moving or still), at both ends: the fade rides
   on the drifting photograph itself (its stops allow for the drift), so no mask is laid over a moving layer */
.wr-par{-webkit-mask-image:linear-gradient(180deg,transparent 13%,var(--bg) 31%,var(--bg) 55%,transparent 87%);
  mask-image:linear-gradient(180deg,transparent 13%,var(--bg) 31%,var(--bg) 55%,transparent 87%);}
.wr-portrait .wr-par{-webkit-mask-image:none;mask-image:none;}
/* the facts on it (wide screens): its shade starts well above them, so they keep 4.5:1 wherever the photograph
   drifts, and lets go below them, where the photograph has already faded into the sky */
.wr-plate-img::after{background:linear-gradient(180deg,transparent 40%,color-mix(in srgb,var(--bg) 80%,transparent) 70%,color-mix(in srgb,var(--bg) 92%,transparent) 87%,transparent 100%);}
@media (max-width:899.98px){
  .wr-sky-on .wr-hero::before{background:linear-gradient(180deg,color-mix(in srgb,var(--bg) 30%,transparent) 0%,transparent 18%);}
  .wr-sky-on .wr-hero-pic{-webkit-mask-image:linear-gradient(180deg,var(--bg) 62%,transparent);mask-image:linear-gradient(180deg,var(--bg) 62%,transparent);}
  .wr-sky-on .wr-hero-pic::after{background:linear-gradient(180deg,transparent 40%,color-mix(in srgb,var(--bg) 60%,transparent) 80%,var(--bg) 100%);}
  .wr-plate .wr-par{-webkit-mask-image:linear-gradient(180deg,transparent 13%,var(--bg) 27%,var(--bg) 70%,transparent 87%);
    mask-image:linear-gradient(180deg,transparent 13%,var(--bg) 27%,var(--bg) 70%,transparent 87%);}
  .wr .wr-plate-img::after{background:none;}
}

/* ----- 01: two thermals in the gutters, rising faster than the page (one layer each, no mask) ----- */
.wr-thermals{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none;}
.wr-th{position:absolute;bottom:0;width:auto;aspect-ratio:240/1000;overflow:visible;opacity:.62;}
.wr-th.n0{height:86%;right:max(-8rem,calc((100% - var(--measure)) / 2 - 12.5rem));}
.wr-th.n1{height:58%;left:max(-6.5rem,calc((100% - var(--measure)) / 2 - 10rem));}
.wr-th path{fill:none;stroke:url(#wrThF);stroke-width:.6;stroke-linecap:round;vector-effect:non-scaling-stroke;}
.wr-th ellipse{fill:none;stroke:url(#wrThR);stroke-width:.8;vector-effect:non-scaling-stroke;}
@media (max-width:899.98px){.wr-th.n1{display:none;}.wr-th.n0{height:62%;right:-26%;}}

/* ----- 02: Kenya's ground under the course: form lines traced from the relief, crisp at every width ----- */
.wr-ground{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none;}
/* a shade under the course for the words, fading into the sky above and below (a gradient, not a mask) */
.wr-ground{background:linear-gradient(180deg,transparent,color-mix(in srgb,var(--bg) 72%,transparent) 18%,color-mix(in srgb,var(--bg) 72%,transparent) 82%,transparent);}
.wr-topo{position:absolute;left:-7%;top:-4%;width:114%;height:108%;display:none;opacity:.2;}
:root:not(.wr-js) .wr-topo,.wr-ground.is-near .wr-topo{display:block;background:url(@@IMG@@ground.svg) 50% 50%/cover no-repeat;}
/* the glider's shadow on the ground, cast away from the morning sun */
.wr-gs{position:absolute;left:3%;top:75%;width:34px;height:34px;margin:-17px 0 0 -17px;pointer-events:none;transform:translate(9px,13px) rotate(180deg);
  background:radial-gradient(50% 50% at 50% 50%,color-mix(in srgb,var(--ink) 80%,transparent),transparent 72%);clip-path:ellipse(22% 50% at 56% 50%);}
.wr-map.is-live .wr-gs{left:0;top:0;will-change:transform;}

/* all of it moves only with the scroll, and only where the browser ties it to the scroll itself */
@supports (animation-timeline:view()){
  @media (prefers-reduced-motion:no-preference){
    .wr-mark{view-timeline:--wr-mk block;}
    .wr-course{view-timeline:--wr-co block;}
    .is-live .wr-th.n0{animation:wr-rise linear both;animation-timeline:--wr-mk;animation-range:cover 0% cover 100%;}
    .is-live .wr-th.n1{animation:wr-rise2 linear both;animation-timeline:--wr-mk;animation-range:cover 0% cover 100%;}
    @keyframes wr-rise{from{transform:translate3d(0,18%,0);}to{transform:translate3d(0,-22%,0);}}
    @keyframes wr-rise2{from{transform:translate3d(0,12%,0);}to{transform:translate3d(0,-14%,0);}}
    .wr-pin .is-live .wr-topo{animation:wr-gt linear both;animation-timeline:--wr-co;animation-range:contain 0% contain 100%;}
    @keyframes wr-gt{0%,5%{transform:translate3d(0,2.5%,0);}47%,53%{transform:translate3d(-5.5%,0,0);}90%,100%{transform:translate3d(0,-2.5%,0);}}
  }
}

@media print{
  .wr-sky,.wr-thermals,.wr-ground,.wr-night,.wr-still-rg,.wr-gs{display:none!important;}
  .wr-pin .wr-course,.wr-hz .wr-win{height:auto!important;}
  .wr .wr-stage{position:static!important;height:auto!important;}
  .wr-bar,.wr-tick,.wr-cursor,.wr-cue,.wr-km{display:none!important;}
  .wr-track{transform:none!important;flex-wrap:wrap;}
  .wr-cut{color:var(--white)!important;background:none!important;filter:none!important;}
}
""".replace("__GRAIN2__", GRAIN2).replace("__GRAIN__", GRAIN).replace("__KERIO__", IMG["kerio"][0]).replace("@@IMG@@", REC_IMG)
for _i, _v in enumerate(STILL):
    CSS = CSS.replace("@@S%d@@" % _i, "%g" % _v)


def hero():
    best = '<span class="wr-v">36<small>km/h</small></span>'
    mark = '<span class="wr-v">35.94<small>km/h</small></span>'
    return """
<header class="wr-hero wr-grain" id="wr-goal">
  """ + pic("hero", "wr-hero-pic", lazy=False, fetch=True) + """
  <div class="wr-in wr-hero-in">
    <div>
      <p class="wr-kick"><span>World Record Attempt</span> <span class="wr-sep" aria-hidden="true">&middot;</span> <span>Kerio Valley, Kenya</span></p>
      <h1 class="wr-mega wr-k"><span class="wr-ln"><span style="--i:0">The Speed</span></span> <span class="wr-ln"><span class="is-hollow" style="--i:1">Record</span></span> <span class="wr-ln"><span style="--i:2">Attempt</span></span></h1>
      <p class="wr-hero-sub wr-fade">Two world records for speed: 100 km and 200 km, out and return.</p>
      <a class="wr-go wr-fade" href="#wr-partner">Partner on the attempt """ + DOWN + """</a>
    </div>
    <dl class="wr-hero-meta wr-fade">
      <div><dt>To beat, 100 km</dt><dd>""" + mark + """</dd><dd class="wr-s">""" + TBC + """</dd></div>
      <div class="is-me"><dt>My best, about</dt><dd>""" + best + """</dd><dd class="wr-s">Over 198.86 km, not a record course</dd></div>
      <div class="is-win"><dt>Window</dt><dd>18 Jan to 12 Feb 2027</dd></div>
    </dl>
  </div>
  <a class="wr-cue" href="#wr-mark" aria-label="Go to the mark to beat">""" + DOWN + """</a>
</header>
"""


def bar():
    lis = "".join('<li><a href="#%s"><span>%s</span>%s<i aria-hidden="true"></i></a></li>' % (cid, n, name)
                  for cid, n, name in CHAPTERS)
    return ('\n<nav class="wr-bar" aria-label="Chapters"><div class="wr-in wr-bar-in"><ol>' + lis + '</ol>'
            '<a class="wr-btn" href="#wr-partner">Partner</a></div></nav>\n')


def ticker():
    one = '<span>100 km<i></i>200 km<i></i><em>Kerio Valley</em><i></i>2027<i></i></span>'
    return '\n<div class="wr-tick" aria-hidden="true"><div class="wr-tick-in">' + one + one + '</div></div>\n'


def mark():
    return """
<section class="wr-mark" id="wr-mark" aria-labelledby="wr-mark-h">
  """ + thermals_html() + still_ridge("at-01", "morn") + """
  <div class="wr-in">
    <p class="wr-no">01</p>
    <h2 class="wr-h2 wr-k" id="wr-mark-h">""" + kin("The Mark To Beat") + """</h2>
    <div class="wr-duel">
      <div class="wr-big is-theirs">
        <p class="wr-cap">100 km mark, class O-3</p>
        <p class="wr-giga">""" + count("35.94", REC100, 2) + """<small>km/h</small></p>
        <ul class="wr-meta"><li><b>Michel Macquet (FRA)</b></li><li>23 Jan 2025</li><li>Status&nbsp;""" + TBC + """</li><li>""" + ext(FAI_LIST, "FAI records") + """</li></ul>
      </div>
      <div class="wr-big is-mine">
        <p class="wr-cap">My best average, about</p>
        <p class="wr-giga">""" + count("36", BEST) + """<small>km/h</small></p>
        <ul class="wr-meta"><li><b>198.86 km</b></li><li>Kenya, 6 Feb 2025</li><li>UP Trango X (EN C)</li><li><b>Not a record course</b></li><li>""" + ext(UP_NEWS, "Source", ": UP Paragliders news") + """</li></ul>
      </div>
    </div>
    <div class="wr-say">
      <p class="wr-t">The time to beat: 100&nbsp;km in <b>""" + hm(100, REC100).replace(" ", "&nbsp;") + """</b>.</p>
      <p class="wr-also">200 km mark """ + TBD + """</p>
    </div>
    <details class="wr-more"><summary>About these numbers</summary>
      <p>Class O-3 is paragliders. Speed is the course distance over the time.</p>
      <p>One FAI listing shows the 100&nbsp;km mark as a claim under review, another as the record: <a class="wr-u" href=\"""" + FAI_LIST + """\" target="_blank" rel="noopener">FAI CIVL records</a>.</p>
      <p>My 198.86&nbsp;km flight, about 36&nbsp;km/h on a UP Trango X (EN C), was logged on XContest. It was not a record course: <a class="wr-u" href=\"""" + UP_NEWS + """\" target="_blank" rel="noopener">UP Paragliders</a>.</p>
      <p>The claim goes to the FAI under the <a class="wr-u" href=\"""" + FAI_CODE + """\" target="_blank" rel="noopener">Sporting Code, Section 7D</a>.</p>
    </details>
  </div>
</section>
"""


def lane(k):
    xa = X(k / 2) - RX
    return "M%g %gH%gA%g %g 0 0 1 %g %gH%g" % (X0, YO, xa, RX, RY, xa, YB, X0)


def course_svg():
    ticks = []
    for k in range(0, 101, 10):
        big = k % 50 == 0
        ticks.append('<line class="wr-tk" x1="%g" y1="%d" x2="%g" y2="200"/>' % (X(k), 184 if big else 191, X(k)))
    return (
        '<svg viewBox="0 0 1000 200" preserveAspectRatio="none" role="img" aria-labelledby="wrMapT">'
        '<title id="wrMapT">The 100 km and 200 km out-and-return courses drawn to one scale: out from the start '
        'to a turnpoint at half the distance, round it, and straight back</title>'
        '<path class="wr-lane is-200" d="%s"/>' % lane(200)
        + '<path class="wr-lane v100" d="%s"/>' % lane(100)
        + '<path class="wr-glow v100" id="wrG100" d="%s"/><path class="wr-flown v100" id="wrF100" d="%s"/>' % (lane(100), lane(100))
        + '<path class="wr-glow v200" id="wrG200" d="%s"/><path class="wr-flown v200" id="wrF200" d="%s"/>' % (lane(200), lane(200))
        + "".join(ticks)
        + '<path class="wr-gate" d="M%g 28V172"/>' % X0
        + "</svg>"
    )


GLIDER = ('<svg viewBox="-16 -16 32 32" aria-hidden="true" focusable="false">'
          '<path class="g-l" d="M5 -13 L-8 0 L5 13"/><path class="g-w" d="M5 -13 Q15 0 5 13"/><circle class="g-p" cx="-8" cy="0" r="2.6"/></svg>')


def course():
    tp = lambda k, cls: ('<span class="wr-tp %s" style="left:%s"><span class="wr-ring" aria-hidden="true"></span>'
                         '<span class="wr-pl">Turnpoint<i>%d km out</i></span></span>' % (cls, pct(k / 2), k // 2))
    scale = "".join('<span style="left:%s">%s</span>' % (pct(k), "%d km" % k if k == 100 else k) for k in (0, 25, 50, 75, 100))
    return """
<section class="wr-course wr-grain" id="wr-course" aria-labelledby="wr-course-h">
  <div class="wr-stage">
    <div class="wr-ground" aria-hidden="true"><i class="wr-topo"></i></div>
    <div class="wr-in">
      <div class="wr-course-head">
        <div><p class="wr-no">02</p><h2 class="wr-h2 wr-k" id="wr-course-h">""" + kin("Out And Back, To Scale") + """</h2></div>
        <fieldset class="wr-seg"><legend>Course length</legend>
          <input type="radio" name="wrk" id="wrk100" value="100" checked><label for="wrk100">100 km</label>
          <input type="radio" name="wrk" id="wrk200" value="200"><label for="wrk200">200 km</label>
        </fieldset>
      </div>
      <div class="wr-map" data-cursor="map">
        <p class="wr-km" aria-hidden="true"><span id="wrKmBig"><span class="v100">100</span><span class="v200">200</span></span><small>km</small></p>
        <div class="wr-box">
          """ + course_svg() + """
          <span class="wr-pl" style="left:0">Start, finish</span>
          """ + tp(100, "v100") + tp(200, "v200") + """
          <span class="wr-gs" id="wrGs" aria-hidden="true"></span><span class="wr-gl" id="wrGl">""" + GLIDER + """</span>
        </div>
        <div class="wr-scale" aria-hidden="true">""" + scale + """</div>
      </div>
      <dl class="wr-read">
        <div><dt>Flown</dt><dd><span id="wrKm"><span class="v100">100</span><span class="v200">200</span></span><small>km</small></dd></div>
        <div class="is-leg"><dt>Leg</dt><dd id="wrLeg">Finish</dd></div>
        <div class="is-me"><dt>At about 36 km/h, my best average</dt><dd id="wrT1"><span class="v100">""" + clock(100, BEST) + """</span><span class="v200">""" + clock(200, BEST) + """</span></dd></div>
        <div class="is-mark"><dt>At the mark, """ + ("%.2f" % REC100) + """ km/h</dt><dd id="wrT2"><span class="v100">""" + clock(100, REC100) + """</span><span class="v200">""" + TBD + """</span></dd></div>
      </dl>
    </div>
  </div>
</section>
"""


def vario_svg():
    # 0 to 8 m/s: the midday peaks 4 to 6 filled, the rare surges 6 to 7 hatched
    x0, x1, y = 6, 224, 16
    u = (x1 - x0) / 8.0
    p = ['<defs><pattern id="wrHatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line class="v-ht" x1="0" y1="0" x2="0" y2="4"/></pattern></defs>',
         '<line class="v-base" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x0, y, x1, y)]
    for v in range(9):
        x = x0 + v * u
        t = 5 if v % 2 == 0 else 3
        p.append('<line class="v-tk" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x, y - t, x, y + t))
        if v in (0, 2, 4, 6, 8):
            p.append('<text class="v-n" x="%.1f" y="%d">%d</text>' % (x, y + 20, v))
    p.append('<rect class="v-pk" x="%.1f" y="%d" width="%.1f" height="9"/>' % (x0 + 4 * u, y - 4.5, 2 * u))
    p.append('<rect class="v-rr" x="%.1f" y="%d" width="%.1f" height="9"/>' % (x0 + 6 * u, y - 4.5, u))
    return '<svg class="wr-vario" viewBox="0 0 230 40" aria-hidden="true" focusable="false">%s</svg>' % "".join(p)


def place():
    return """
<section class="wr-place" id="wr-kerio" aria-labelledby="wr-kerio-h">
  <div class="wr-in">
    <p class="wr-no">03</p>
    <h2 class="wr-cut" id="wr-kerio-h"><span>Kerio</span> <span>Valley</span></h2>
    <p class="wr-lede wr-fade">The base of my <a class="wr-u" href="destinations/kenya.html">Kenya expeditions</a>, and the site where the world speed records are chased.</p>
  </div>
  <figure class="wr-plate">
    <div class="wr-plate-img wr-rv"><div class="wr-par"><picture><source media="(max-width: 560px)" srcset=\"""" + IMG["kerio_p"][0] + """.webp" type="image/webp"><source srcset=\"""" + IMG["kerio"][0] + """.webp" type="image/webp"><img src=\"""" + IMG["kerio"][0] + """.jpg" width="1152" height="768" alt="Paragliding at Kerio Valley, Kenya" loading="lazy" decoding="async"></picture></div></div>
    <dl class="wr-facts">
      <div><dt>Where</dt><dd>0.72&deg;N 35.65&deg;E</dd></div>
      <div><dt>Season</dt><dd>December to March</dd></div>
      <div><dt>Thermals</dt><dd>4 to 6 m/s at the midday peaks, rare surges 6 to 7""" + vario_svg() + """</dd></div>
      <div><dt>Flights</dt><dd>2 to 7 hours over the Rift Valley</dd></div>
    </dl>
  </figure>
</section>
"""


def days():
    # 18 Jan to 12 Feb 2027, a cell a day: Expedition One (18 to 29 Jan), the two days between, Expedition Two (1 to 12 Feb)
    cells, nums = [], []
    for i in range(26):
        on = i < 12 or i >= 14
        cells.append('<i class="%s" style="--d:%d"></i>' % ("is-on" if on else "is-off", i))
        nums.append("<span>%d</span>" % (18 + i if i < 14 else i - 13))
    return """
      <div class="wr-days">
        <div class="wr-days-k">
          <span><a class="wr-u" href="destinations/kenya.html">Expedition One</a>18 to 29 Jan</span>
          <span><a class="wr-u" href="destinations/kenya.html">Expedition Two</a>1 to 12 Feb</span>
        </div>
        <div class="wr-days-bar" role="img" aria-label="The window, 26 days from 18 January to 12 February 2027: Expedition One, 18 to 29 January, two days between, then Expedition Two, 1 to 12 February">""" + "".join(cells) + """</div>
        <div class="wr-days-n" aria-hidden="true">""" + "".join(nums) + """</div>
        <p class="wr-days-dur"><b>During</b>Live tracking from Kerio Valley on attempt days, daily updates</p>
      </div>"""


def window():
    return """
<section class="wr-win" id="wr-window" aria-labelledby="wr-win-h">
  <div class="wr-stage">
    <div class="wr-in wr-win-in">
      <div class="wr-win-head">
        <p class="wr-no">04</p>
        <h2 class="wr-h2 wr-k" id="wr-win-h">""" + kin("18 Jan To 12 Feb 2027") + """</h2>
        <p class="wr-lede wr-fade">Alongside my two Kenya expeditions.</p>
      </div>""" + days() + """
      <div class="wr-vp">
        <div class="wr-track">
          <ol class="wr-steps">
            <li class="wr-step"><span class="wr-when">Before</span><h3>Preparation</h3><p>Wing, instruments, team, FAI observer """ + TBD + """</p></li>
            <li class="wr-step"><span class="wr-when">Before</span><h3>Build-Up Episodes</h3><p>And the newsletter</p></li>
          </ol>
          <figure class="wr-fig">""" + pic("high") + """</figure>
          <ol class="wr-steps" start="3">
            <li class="wr-step"><span class="wr-when">After</span><h3>The Claim</h3><p><a class="wr-u" href=\"""" + FAI_CODE + """\" target="_blank" rel="noopener">FAI Sporting Code, Section 7D</a></p></li>
            <li class="wr-step"><span class="wr-when">After</span><h3>The Film</h3><p>A debrief episode and the flight data</p></li>
          </ol>
        </div>
        <div class="wr-swipe" aria-hidden="true"><i></i></div>
      </div>
    </div>
  </div>
</section>
"""


def audience():
    return """
<section class="wr-aud" id="wr-audience" aria-labelledby="wr-aud-h">
  <div class="wr-in wr-aud-in">
    <div class="wr-aud-copy">
      <p class="wr-no">05</p>
      <h2 class="wr-h2 wr-k" id="wr-aud-h">""" + kin("Who Flies It With You") + """</h2>
      <p class="wr-lede wr-fade">Podcast, YouTube and a newsletter about four times a month.</p>
    </div>
    <figure class="wr-portrait wr-rv"><div class="wr-par">""" + pic("aninder") + """</div><figcaption>Aninder Singh</figcaption></figure>
    <dl class="wr-stats">
      <div><dt>Podcast streams</dt><dd>""" + count("100,000+", 100000, comma=True, suf="+") + """</dd></div>
      <div><dt>Countries reached</dt><dd>""" + count("130+", 130, suf="+") + """</dd></div>
      <div><dt>Long-form interviews</dt><dd>""" + count("80", 80) + """</dd></div>
      <div><dt>Years flying</dt><dd>""" + count("10+", 10, suf="+") + """</dd></div>
    </dl>
  </div>
</section>
"""


def offer():
    return """
<section class="wr-offer" id="wr-partner" aria-labelledby="wr-offer-h">
  """ + still_ridge("at-06", "dusk") + night_static() + still_ridge("at-end") + """
  <div class="wr-in">
    <div class="wr-offer-head">
      <div>
        <p class="wr-no">06</p>
        <h2 class="wr-h2 wr-k" id="wr-offer-h">""" + kin("Put Your Name On The Attempt") + """</h2>
        <p class="wr-lede wr-fade">Prices in the media kit, on request. Every sponsorship is <a class="wr-u" href="safety-and-disclosure.html">clearly marked as sponsored</a>.</p>
      </div>
      <figure class="wr-offer-pic wr-rv">""" + pic("icare") + """</figure>
    </div>
    <div class="wr-tiers">
      <article class="wr-tier is-lead">
        <p class="wr-tier-n" aria-hidden="true">01</p>
        <p class="wr-tier-k">One only</p>
        <h3>Title Partner</h3>
        <ul><li>Your name in the attempt's title</li><li>Your mark on kit and on camera</li><li>Sponsored segments in the build-up and debrief episodes</li><li>First credit in the film</li><li>Your logo on the live tracking page</li></ul>
      </article>
      <article class="wr-tier">
        <p class="wr-tier-n" aria-hidden="true">02</p>
        <h3>Equipment Partner</h3>
        <ul><li>Your product used and shown</li><li>An honest, disclosed review</li><li>In the hands of my Kenya expedition pilots</li><li>Credits</li></ul>
      </article>
      <article class="wr-tier">
        <p class="wr-tier-n" aria-hidden="true">03</p>
        <h3>Supporter</h3>
        <ul><li>Your name on this page</li><li>Newsletter and debrief thanks</li><li>Film credit</li></ul>
      </article>
    </div>
    <div class="wr-cta">
      <span class="wr-mag"><a class="btn-solid" href=\"""" + MAIL + """\"><span>Partner on the attempt</span></a></span>
      <span class="wr-mag"><a class="btn-lines" href="partners.html#pwForm">Other ways to work together</a></span>
    </div>
    <p class="wr-src">Sources: <a class="wr-u" href=\"""" + UP_NEWS + """\" target="_blank" rel="noopener">UP Paragliders</a>, <a class="wr-u" href=\"""" + FAI_LIST + """\" target="_blank" rel="noopener">FAI records</a>, <a class="wr-u" href=\"""" + FAI_CODE + """\" target="_blank" rel="noopener">Sporting Code 7D</a>, <a class="wr-u" href="destinations/kenya.html">the Kenya expedition</a></p>
  </div>
</section>
"""


EARLY = ('<script>(function(r,m){r.classList.add("wr-js");if(!m("(prefers-reduced-motion: reduce)").matches)'
         '{r.classList.add("wr-pin","wr-sky-on");if(m("(min-width: 900px)").matches)r.classList.add("wr-hz");}})'
         '(document.documentElement,function(q){return window.matchMedia(q);});</script>')


def main_html():
    return ('<main id="v4-main" class="wr">\n' + EARLY + ridge_defs() + sky_html() + hero() + bar() + ticker() + mark() + course()
            + place() + window() + audience() + offer() + "\n</main>")


SCRIPT = r"""<script>
/* The speed record attempt (tools/v4_record.py). Every frame here is caused
   by a scroll, a pointer, a tap or a key, and stops when they do. Reduced
   motion: the finished state, nothing pinned, nothing counting. Without this
   script the page is complete and the course switch still works. */
(function () {
  var d = document, w = window, root = d.documentElement;
  var main = d.getElementById("v4-main");
  if (!main || !main.classList.contains("wr")) return;
  var mq = function (q) { return w.matchMedia(q); };
  var still = mq("(prefers-reduced-motion: reduce)").matches;
  var IO = "IntersectionObserver" in w;
  var REC = @@REC@@, BEST = @@BEST@@, TBD = '<span class="wr-tbd">[to supply]</span>';
  var X0 = @@X0@@, PX = @@PX@@, YO = @@YO@@, YB = @@YB@@, RX = @@RX@@, RY = @@RY@@, CY = @@CY@@;
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function absTop(el) { return el.getBoundingClientRect().top + w.scrollY; }
  function clock(h) { var m = Math.round(h * 60), mm = m % 60; return "<b>" + Math.floor(m / 60) + "</b><small>h</small> <b>" + (mm < 10 ? "0" : "") + mm + "</b><small>min</small>"; }
  function all(s, r) { return [].slice.call((r || d).querySelectorAll(s)); }
  function showAll() { all(".wr-k,.wr-fade,.wr-rv,.wr-cut,.wr-days").forEach(function (el) { el.classList.add("is-in", "is-near"); }); }

  try {
  /* 1. headlines, lines, photographs and the window's days arrive once, as they come into view */
  var rv = all(".wr-k,.wr-fade,.wr-rv,.wr-cut,.wr-days");
  if (still || !IO) showAll();
  else {
    /* an element clipped shut to begin with has no area to intersect, so its parent is watched for it */
    var hosts = [];
    var ro = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        ro.unobserve(e.target);
        hosts.forEach(function (h) { if (h[0] === e.target) h[1].classList.add("is-in"); });
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    rv.forEach(function (el) {
      var host = el.classList.contains("wr-cut") ? el.parentNode : el;
      hosts.push([host, el]); ro.observe(host);
    });
  }
  /* the photograph inside the letters loads only when its chapter is near (the letters show a plain fill until then) */
  var cut = d.querySelector(".wr-cut");
  if (cut && IO) {
    var no = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { cut.classList.add("is-near"); no.disconnect(); } }, { rootMargin: "120% 0px 120% 0px" });
    no.observe(cut);
  } else if (cut) cut.classList.add("is-near");

  /* 2. the numbers count up once, in the display face, at their final width */
  function fmt(el, v) {
    var dec = +el.getAttribute("data-dec") || 0, s = v.toFixed(dec);
    if (el.hasAttribute("data-comma")) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return s + (el.getAttribute("data-suf") || "");
  }
  if (!still && IO) {
    var counts = all("[data-count]");
    counts.forEach(function (el) { el.firstElementChild.textContent = fmt(el, 0); });
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        co.unobserve(e.target);
        var el = e.target, to = +el.getAttribute("data-count"), t = el.firstElementChild, t0 = performance.now(), dur = 1700;
        (function step(now) {
          var p = Math.min(1, (now - t0) / dur), k = 1 - Math.pow(1 - p, 4);
          t.textContent = p < 1 ? fmt(el, to * k) : el.getAttribute("data-final");
          if (p < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: 0.6 });
    counts.forEach(function (el) { co.observe(el); });
  }

  /* 3. the course: 100 or 200 km on one scale, a hairpin flown by the scroll */
  var C = d.getElementById("wr-course"), Cst = C.querySelector(".wr-stage"), map = C.querySelector(".wr-map");
  var box = C.querySelector(".wr-box svg"), gl = d.getElementById("wrGl"), gs = d.getElementById("wrGs");
  var kmEl = d.getElementById("wrKm"), kmBig = d.getElementById("wrKmBig"), legEl = d.getElementById("wrLeg");
  var t1 = d.getElementById("wrT1"), t2 = d.getElementById("wrT2");
  var paths = { 100: [d.getElementById("wrF100"), d.getElementById("wrG100")], 200: [d.getElementById("wrF200"), d.getElementById("wrG200")] };
  var r200 = d.getElementById("wrk200");
  var K = r200 && r200.checked ? 200 : 100, F = 1, lastKm = -1, lastT = "", lastLeg = "";
  function X(km) { return X0 + km * PX; }
  var geo = { mapW: 1, mapH: 1 };
  function render(f) {
    F = f;
    var xs = X(0), xa = X(K / 2) - RX, ts = 0.06, half = (1 - ts) / 2, sx = geo.mapW / 1000, sy = geo.mapH / 200;
    var x, y, km, rot, dd, leg;
    if (f <= half) {
      var u = f / half; x = xs + (xa - xs) * u; y = YO; km = K / 2 * u; rot = 0; leg = "Out";
      dd = "M" + xs + " " + YO + "H" + x.toFixed(1);
    } else if (f <= half + ts) {
      var v = (f - half) / ts, th = -Math.PI / 2 + v * Math.PI;
      x = xa + RX * Math.cos(th); y = CY + RY * Math.sin(th); km = K / 2; leg = "Turnpoint";
      rot = Math.atan2(RY * Math.cos(th) * sy, -RX * Math.sin(th) * sx) * 180 / Math.PI;
      dd = "M" + xs + " " + YO + "H" + xa + "A" + RX + " " + RY + " 0 0 1 " + x.toFixed(1) + " " + y.toFixed(1);
    } else {
      var u2 = Math.min(1, (f - half - ts) / half); x = xa - (xa - xs) * u2; y = YB; km = K / 2 + K / 2 * u2; rot = 180;
      leg = u2 >= 1 ? "Finish" : "Home";
      dd = "M" + xs + " " + YO + "H" + xa + "A" + RX + " " + RY + " 0 0 1 " + xa + " " + YB + "H" + x.toFixed(1);
    }
    paths[K][0].setAttribute("d", dd); paths[K][1].setAttribute("d", dd);
    gl.style.transform = "translate(" + (x * sx).toFixed(1) + "px," + (y * sy).toFixed(1) + "px) rotate(" + rot.toFixed(1) + "deg)";
    if (gs) gs.style.transform = "translate(" + (x * sx + 9).toFixed(1) + "px," + (y * sy + 13).toFixed(1) + "px) rotate(" + rot.toFixed(1) + "deg)";
    var k = Math.round(km);
    if (k !== lastKm) { lastKm = k; kmEl.textContent = k; if (kmBig) kmBig.textContent = k; }
    if (leg !== lastLeg) { lastLeg = leg; legEl.textContent = leg; }
    var s1 = clock(km / BEST);
    if (s1 !== lastT) { lastT = s1; t1.innerHTML = s1; t2.innerHTML = K === 100 ? clock(km / REC) : TBD; }
  }
  function setK(k) {
    K = k; lastKm = -1; lastT = ""; lastLeg = "";
    /* the other course is shown whole, so a change of mind finds it drawn */
    var o = k === 100 ? 200 : 100, full = "M" + X(0) + " " + YO + "H" + (X(o / 2) - RX) + "A" + RX + " " + RY + " 0 0 1 " + (X(o / 2) - RX) + " " + YB + "H" + X(0);
    paths[o][0].setAttribute("d", full); paths[o][1].setAttribute("d", full);
    render(F);
  }
  all('input[name="wrk"]').forEach(function (r) { r.addEventListener("change", function () { if (r.checked) setK(+r.value); }); });
  map.classList.add("is-live");

  /* 4. the window: a strip moved sideways by the vertical scroll (wide screens), a swipe row with a line under it (phones) */
  var W = d.getElementById("wr-window"), Wst = W.querySelector(".wr-stage"), Wvp = W.querySelector(".wr-vp"), Wtr = W.querySelector(".wr-track");
  var swipe = W.querySelector(".wr-swipe");
  var hzMq = mq("(min-width: 900px)");
  function hzOn() { return root.classList.contains("wr-hz"); }
  function swiped() {
    if (!swipe || hzOn()) return;
    var m = Wtr.scrollWidth - Wtr.clientWidth;
    swipe.style.setProperty("--p", (0.25 + 0.75 * (m > 0 ? Wtr.scrollLeft / m : 1)).toFixed(3));
  }
  Wtr.addEventListener("scroll", swiped, { passive: true });

  /* 5. the ticker and the chapter bar */
  var tick = d.querySelector(".wr-tick-in"), tickBox = d.querySelector(".wr-tick");
  var barEl = d.querySelector(".wr-bar"), barOl = barEl && barEl.querySelector("ol");
  var links = barEl ? all("ol a", barEl) : [], lines = links.map(function (a) { return a.querySelector("i"); });
  var chaps = links.map(function (a) { return d.getElementById(a.getAttribute("href").slice(1)); });
  var lastP = links.map(function () { return -1; });
  var foot = d.querySelector("footer"), hero = d.getElementById("wr-goal"), partner = d.getElementById("wr-partner"), cur = -2;

  /* 7. the record day behind the page: from first light to night as the visitor scrolls. Two canvases,
     fixed behind everything: the sky, painted small from the design tokens in linear light and never past a
     set brightness (so the words keep their contrast), stretched by the browser; and over it everything on
     the sky (the real stars and Milky Way of a night in the window, the low sun, the clouds, the hills),
     composed again only when something on it has moved. Each change follows the scroll and stops with it. */
  var skyEl = root.classList.contains("wr-sky-on") ? d.querySelector(".wr-sky") : null;
  var dayEls = [hero, d.getElementById("wr-mark"), C, d.getElementById("wr-kerio"), W, d.getElementById("wr-audience"), partner, foot];
  var SKY = null;
  /* a sky that cannot be painted leaves the still day in its place, and every other effect running */
  if (skyEl) { try { SKY = daySky(skyEl); } catch (e) { SKY = null; root.classList.remove("wr-sky-on"); } }
  function daySky(el) {
    var sk = el.querySelector(".wr-sky-c"), sg = sk.getContext("2d", { alpha: false }), cv = el.querySelector(".wr-sky-o"), g = cv.getContext("2d");
    if (!g || !sg || typeof Path2D === "undefined") throw new Error("no sky");
    var INFO = @@SKYINFO@@, IMGS = "@@IMG@@";
    var CAP = @@CAP@@, KNEE = CAP * 0.7, YH = 0.86, SUNR = 1.519, T = {}, P = [], img = null, Cc = {}, Cs = {};
    var Wd = 1, Hd = 1, dpr = 1, W2 = 1, H2 = 1, cw = 1, ch = 1, kx = 1, ky = 1, lastQ = -1, hzH = 1, hzB = 0, kind = "w", lay = {}, sig = "", dirty = [0, 0];
    var ENC = new Uint8ClampedArray(4096), GX = [], HX = [], BX = [], VX = [], OX = [], DX = [];
    var i;
    for (i = 0; i < 4096; i++) { var e = i / 4095; ENC[i] = Math.round(e <= 0.0031308 ? 3294.6 * e : 269.025 * Math.pow(e, 1 / 2.4) - 14.025); }
    function lin(v) { v = v < 0 ? 0 : v > 255 ? 1 : v / 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    /* a token or a mix of tokens, as the page computes it now: [r, g, b, a] */
    function rgba(expr) {
      cv.style.color = expr;
      var s = getComputedStyle(cv).color, n = (s.match(/-?[\d.]+(?:e-?\d+)?/g) || [0, 0, 0]).map(Number);
      cv.style.color = "";
      if (s.indexOf("color(") === 0) { n[0] *= 255; n[1] *= 255; n[2] *= 255; }
      return [n[0], n[1], n[2], n.length > 3 ? n[3] : 1];
    }
    function css(c, a) { return "rgba(" + Math.round(c[0]) + "," + Math.round(c[1]) + "," + Math.round(c[2]) + "," + (a === undefined ? c[3] : a) + ")"; }
    /* the tokens (the site's own sky tokens follow the visitor's clock), and every colour drawn from them */
    function tokens() {
      ["bg", "ink", "orange", "white", "sky-cool"].forEach(function (k) { T[k] = rgba("var(--" + k + ")"); });
      var mx = function (a, p, b) { return rgba("color-mix(in srgb," + a + " " + p + "%," + b + ")"); };
      Cc = { bg: T.bg, land: mx("var(--ink)", 72, "var(--bg)"), h1: mx("var(--bg)", 86, "var(--gray-light)"), h2: mx("var(--bg)", 70, "var(--ink)"),
        w1: mx("var(--bg)", 93, "var(--gray-light)"), w2: mx("var(--bg)", 60, "var(--ink)"), gold: mx("var(--orange)", 62, "var(--white)"),
        gold2: mx("var(--orange)", 70, "var(--white)"), trim: mx("var(--orange)", 55, "var(--white)"), glow: mx("var(--orange)", 70, "var(--sky-cool)"),
        orange: T.orange, cloud: rgba("var(--wr-cloud)"), dusk: rgba("var(--wr-cloud-dusk)"), sun: mx("var(--orange)", 30, "var(--bg)"),
        sw: T.white, sy: mx("var(--white)", 80, "var(--orange)"), sr: mx("var(--white)", 58, "var(--orange)"), mw: mx("var(--white)", 82, "var(--sky-cool)") };
      Cs = { tw: css(Cc.sw, 1), tb: css(Cc.sw, 1), ty: css(Cc.sy, 1), tr: css(Cc.sr, 1) };
      build();
      if (lay.k) ridges();
      ["street", "near", "dusk", "mwd", "mwn"].forEach(function (k) { if (CL[k].img && CL[k].img.complete) CL[k].tint = tint(CL[k]); });
      sig = "";
    }
    function m() {
      var o = [0, 0, 0];
      for (var i = 0; i < arguments.length; i += 2) { var t = T[arguments[i]], k = arguments[i + 1]; o[0] += t[0] * k; o[1] += t[1] * k; o[2] += t[2] * k; }
      return o;
    }
    /* a colour from the tokens (a mix, as pairs) brought to a set relative luminance, in linear light: the
       hue comes from the palette, the brightness from the day */
    function tone(Lt) {
      var c = m.apply(null, [].slice.call(arguments, 1)), l = [lin(c[0]), lin(c[1]), lin(c[2])];
      var L = 0.2126 * l[0] + 0.7152 * l[1] + 0.0722 * l[2], f = L > 0 ? Lt / L : 0;
      return [l[0] * f, l[1] * f, l[2] * f];
    }
    /* the day: at each point (in chapters from the top: 0 the opening, 1 the mark, 2 the course, 3 Kerio
       Valley, 4 the window, 5 the audience, 6 the offer, 7 the footer) the clock; the sky from the top down
       (z, mi, h, in linear light at a set luminance); the low sun's glow (gc ga gr); the glow along the
       horizon under it (hc ha, hh tall); its rays (ra); the rose band and the Earth's shadow on the side away
       from the sun (b); midday's light falling from the top (bl, centred at bx) and its deep sides (vg); the
       stars before dawn (sa) and at night (sb); the hills' sinking (rg) and haze (lo), the morning light on
       the escarpment's face (fm), the dusk light (fd); the sun's disc (sd); the cloud street (cs) */
    function build() {
      function unit(c) { var l = [lin(c[0]), lin(c[1]), lin(c[2])], L = 0.2126 * l[0] + 0.7152 * l[1] + 0.0722 * l[2]; return [l[0] / L, l[1] / L, l[2] / L]; }
      var gold = unit(m("orange", .36, "white", .64)), pale = unit(m("orange", .22, "white", .78)), warm = unit(m("white", .66, "orange", .34)),
        amber = unit(m("orange", .72, "white", .28)), ember = unit(m("orange", .92, "white", .08));
      function blue(L) { return tone(L, "sky-cool", .92, "white", .08); }
      function deep(L) { return tone(L, "sky-cool", 1.3, "white", -.3); }
      function S(dd, hr, z, mi, h, o) {
        var s = { d: dd, hr: hr, z: z, mi: mi, h: h, gc: gold, ga: 0, gr: .3, hc: gold, ha: 0, hh: .12, hw: .5, ra: 0, b: 0, bl: 0, bx: .5, vg: 0, sa: 0, sb: 0, lo: 1, fm: 0, fd: 0, sd: 0, cs: 0 };
        for (var k in o) s[k] = o[k];
        return s;
      }
      var n0 = blue(.0055), n1 = tone(.007, "sky-cool", .9, "white", .1), n2 = tone(.0095, "sky-cool", .8, "orange", .06, "white", .14);
      P = [
        S(0, 5.2, n0, n1, n2, { sa: 1 }),
        S(.45, 5.85, blue(.0065), tone(.009, "sky-cool", .86, "white", .1, "orange", .04), tone(.014, "sky-cool", .62, "white", .26, "orange", .12), { sa: 1, b: .4, hc: pale, ha: .25, hh: .05 }),
        S(.75, 6.45, blue(.008), tone(.011, "sky-cool", .8, "white", .16, "orange", .04), tone(.016, "sky-cool", .56, "white", .34, "orange", .1), { sa: .55, b: .9, hc: pale, ha: .75, hh: .05, hw: .3, fm: .25 }),
        S(1.05, 6.87, blue(.009), tone(.0125, "sky-cool", .74, "white", .22, "orange", .04), tone(.017, "sky-cool", .55, "white", .35, "orange", .1), { sa: .12, b: .55, ha: 1, hh: .06, hw: .3, ga: 1, gr: .14, ra: .3, fm: .9, sd: 1 }),
        S(1.45, 7.6, blue(.0105), tone(.015, "sky-cool", .72, "white", .24, "orange", .04), tone(.02, "white", .5, "sky-cool", .4, "orange", .1), { b: .15, ha: .75, hh: .08, hw: .34, ga: 1, gr: .17, ra: .4, fm: 1, sd: .4 }),
        S(1.75, 8.2, deep(.012), tone(.017, "sky-cool", .8, "white", .2), tone(.027, "white", .58, "sky-cool", .34, "orange", .08), { hc: pale, ha: .3, hh: .1, ga: .5, gr: .3, ra: .2, fm: .7, bl: .25, bx: .2 }),
        S(2.2, 9.2, deep(.012), deep(.015), tone(.024, "sky-cool", .7, "white", .3), { bl: .5, bx: .2, vg: .4, fm: .3, cs: .25, lo: .85 }),
        S(2.7, 10.6, deep(.0115), deep(.0145), tone(.025, "sky-cool", .66, "white", .34), { bl: .8, bx: .28, vg: .8, cs: .8, lo: .6 }),
        S(3.2, 12.1, deep(.011), deep(.014), tone(.026, "sky-cool", .62, "white", .38), { bl: 1, bx: .36, vg: 1, cs: 1, lo: .5 }),
        S(3.7, 13.3, deep(.011), deep(.014), tone(.026, "sky-cool", .62, "white", .34, "orange", .04), { bl: .95, bx: .44, vg: 1, cs: 1, lo: .5 }),
        S(4.2, 14.5, deep(.0115), tone(.0145, "sky-cool", 1.15, "white", -.15), tone(.026, "sky-cool", .5, "white", .38, "orange", .12), { bl: .7, bx: .56, vg: .8, cs: .7, lo: .65 }),
        S(4.65, 15.6, tone(.0115, "sky-cool", .95, "orange", .05), tone(.016, "sky-cool", .6, "white", .25, "orange", .15), tone(.027, "orange", .3, "white", .5, "sky-cool", .2), { bl: .3, bx: .85, gc: warm, ga: .45, gr: .3, hc: amber, ha: .3, hh: .12, cs: .3, fd: .15, lo: .85 }),
        S(5.15, 16.8, tone(.0105, "sky-cool", .88, "orange", .12), tone(.015, "sky-cool", .45, "orange", .35, "white", .2), tone(.03, "orange", .62, "white", .3, "sky-cool", .08), { gc: amber, ga: .7, gr: .28, hc: amber, ha: .65, hh: .16, ra: .45, fd: .5 }),
        S(5.55, 17.9, tone(.0095, "sky-cool", .85, "orange", .15), tone(.013, "sky-cool", .55, "orange", .45), tone(.032, "orange", .85, "white", .15), { gc: ember, ga: .7, gr: .24, hc: ember, ha: .9, hh: .2, ra: .4, fd: .8, sd: 1, b: .3 }),
        S(5.8, 18.55, tone(.009, "sky-cool", .88, "orange", .12), tone(.012, "sky-cool", .6, "orange", .4), tone(.031, "orange", .92, "white", .08), { gc: ember, ga: .45, gr: .22, hc: ember, ha: 1, hh: .22, ra: .25, fd: 1, sd: .8, b: .5 }),
        S(6.1, 18.95, blue(.0075), tone(.0105, "sky-cool", .7, "orange", .3), tone(.02, "orange", .8, "sky-cool", .2), { gc: ember, hc: ember, ha: .55, hh: .2, fd: .6, sb: .35, b: .3 }),
        S(6.45, 19.3, n0, tone(.0085, "sky-cool", .82, "orange", .18), tone(.012, "orange", .5, "sky-cool", .5), { gc: ember, hc: ember, ha: .2, hh: .18, fd: .2, sb: .85 }),
        S(6.8, 19.6, n0, n1, n2, { gc: ember, hc: ember, ha: .06, hh: .16, sb: 1 }),
        S(8, 20.4, n0, n1, n2, { gc: ember, hc: ember, hh: .16, sb: 1 })
      ];
      P.rose = tone(.022, "orange", .45, "white", .3, "sky-cool", .25);
      P.shade = tone(.0075, "sky-cool", 1);
      P.hot = unit(m("white", .74, "orange", .08, "sky-cool", .18));
      P.rays = amber;
      lastQ = -1;
    }
    function mix(a, b, f) { return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f]; }
    function state(D) {
      var i = 0;
      while (i < P.length - 2 && D > P[i + 1].d) i++;
      var a = P[i], b = P[i + 1], f = clamp((D - a.d) / (b.d - a.d)), s = {};
      for (var k in a) s[k] = typeof a[k] === "number" ? a[k] + (b[k] - a[k]) * f : mix(a[k], b[k], f);
      return s;
    }
    function size() {
      Wd = Math.max(1, el.clientWidth); Hd = Math.max(1, el.clientHeight); dpr = Math.min(w.devicePixelRatio || 1, 2);
      W2 = Math.round(Wd * dpr); H2 = Math.round(Hd * dpr);
      if (cv.width !== W2 || cv.height !== H2) { cv.width = W2; cv.height = H2; }
      dirty = [0, H2];
      cw = Wd < 600 ? 56 : Wd < 1100 ? 80 : 104; ch = Math.max(8, Math.round(cw * Hd / Wd));
      sk.width = cw; sk.height = ch; img = sg.createImageData(cw, ch);
      ky = YH * Hd / 2.1; kx = Math.min(ky, (Wd / 2 - 14) / 1.6);
      /* the hills: the phone's own drawing under 560 px; on tablets and phones they stand on the chapter bar */
      var vh = w.innerHeight;
      kind = Wd <= 560 ? "p" : "w"; hzB = Wd < 900 ? 58 : 0; hzH = Math.round(vh * (Wd <= 560 ? 0.2 : Wd < 900 ? 0.26 : 0.3));
      ridges(); lastQ = -1; sig = "";
    }
    /* the three layers of the hills, drawn once per size from the shared paths (the still page uses the same) */
    function ridges() {
      var R = INFO[kind], s = Math.max(Wd / R.w, hzH / R.h), ox = Wd - R.w * s, oy = hzH - R.h * s, hh = Math.round(hzH * dpr);
      function layer() { var c = d.createElement("canvas"); c.width = W2; c.height = hh; var x = c.getContext("2d"); x.setTransform(dpr * s, 0, 0, dpr * s, dpr * ox, dpr * oy); return x; }
      function p2(n) { return new Path2D(d.getElementById("wrR" + kind + "-" + n).getAttribute("d")); }
      function grad(x, n, st) { var b = R.bb[n], gr = x.createLinearGradient(0, b[0], 0, b[1]); st.forEach(function (q) { gr.addColorStop(q[0], q[1]); }); return gr; }
      var x = layer();
      x.fillStyle = css(Cc.bg, 0.26); x.fill(p2("far2"));
      x.fillStyle = css(Cc.bg, 0.44); x.fill(p2("farh"));
      x.fillStyle = grad(x, "tug", [[0, css(Cc.h1)], [0.7, css(Cc.h2)], [1, css(Cc.h2)]]); x.fill(p2("tug"));
      x.fillStyle = grad(x, "esc", [[0, css(Cc.w1)], [0.55, css(Cc.w2)], [1, css(Cc.w2)]]); x.fill(p2("esc"));
      x.fillStyle = css(Cc.land); x.fill(p2("near")); x.fill(p2("trees"));
      lay.land = x.canvas;
      x = layer(); x.lineCap = "round"; x.lineJoin = "round";
      x.fillStyle = grad(x, "face", [[0, css(Cc.gold, 0.24)], [0.42, css(Cc.gold2, 0.08)], [1, css(Cc.gold2, 0)]]); x.fill(p2("face"));
      x.strokeStyle = css(Cc.bg, 0.6); x.lineWidth = 1.3 / s; x.stroke(p2("gul"));
      x.strokeStyle = css(Cc.trim, 0.7); x.lineWidth = 1.2 / s; x.stroke(p2("trim"));
      lay.morn = x.canvas;
      x = layer(); x.lineJoin = "round";
      x.fillStyle = grad(x, "tface", [[0, css(Cc.glow, 0.2)], [1, css(Cc.glow, 0)]]); x.fill(p2("tface"));
      x.strokeStyle = css(Cc.orange, 1); x.lineWidth = 1.5 / s; x.stroke(p2("rim"));
      lay.dusk = x.canvas; lay.k = kind; lay.s = s; lay.ox = ox; lay.oy = oy; lay.hk = "";
    }
    /* the hills as they stand at this hour (their haze, the morning light, the dusk light), composed once per step */
    function hills(lo, fm, fd) {
      var k = [Math.round(lo * 25), Math.round(fm * 25), Math.round(fd * 25), lay.k, W2].join();
      if (lay.hk === k) return lay.h;
      if (!lay.h || lay.h.width !== W2 || lay.h.height !== lay.land.height) { lay.h = d.createElement("canvas"); lay.h.width = W2; lay.h.height = lay.land.height; }
      var x = lay.h.getContext("2d");
      x.clearRect(0, 0, W2, lay.h.height);
      x.globalAlpha = Math.round(lo * 25) / 25; x.drawImage(lay.land, 0, 0);
      if (fm > 0.02) { x.globalAlpha = Math.round(fm * 25) / 25; x.drawImage(lay.morn, 0, 0); }
      if (fd > 0.02) { x.globalAlpha = Math.round(fd * 25) / 25; x.drawImage(lay.dusk, 0, 0); }
      lay.hk = k;
      return lay.h;
    }
    /* where the hills' top line is on screen at x */
    function skyline(x, vh) {
      var b = INFO[kind], X = (x - lay.ox) / lay.s / b.w * 32;
      var i = Math.max(0, Math.min(31, Math.floor(X))), f = clamp(X - i);
      return vh - hzB - hzH + lay.oy + (b.y[i] + (b.y[i + 1] - b.y[i]) * f) * lay.s;
    }
    /* the clouds (the far cloud street, the near cumulus, the dusk cloud) and the two Milky Ways: greyscale
       masks, each fetched only as its hour comes near, then given its colour from the tokens */
    var CL = {
      street: { f: function () { return Wd <= 700 ? "street-s" : "street-l"; }, c: "cloud" },
      near: { f: function () { return Wd <= 700 ? "cu-s" : "cu-l"; }, c: "cloud" },
      dusk: { f: function () { return Wd <= 700 ? "dusk-s" : "dusk-l"; }, c: "dusk" },
      mwd: { f: function () { return "mw-dawn"; }, c: "mw", a: 0.09 }, mwn: { f: function () { return "mw-night"; }, c: "mw", a: 0.09 }
    };
    function want(k) {
      var c = CL[k];
      if (c.img) return c.tint;
      c.img = new Image(); c.img.decoding = "async";
      c.img.onload = function () { c.tint = tint(c); sig = ""; if (SKY) onScroll(); };
      c.img.src = IMGS + c.f() + ".webp";
      return null;
    }
    function tint(c) {
      var im = c.img, t = d.createElement("canvas"), W = t.width = im.naturalWidth, H = t.height = im.naturalHeight, x = t.getContext("2d");
      /* grey to alpha: through the page's own filter where the canvas takes filters, else pixel by pixel (once) */
      if ("filter" in x && d.getElementById("wrLumA")) { x.filter = "url(#wrLumA)"; x.drawImage(im, 0, 0); x.filter = "none"; }
      else { x.drawImage(im, 0, 0); var id = x.getImageData(0, 0, W, H), p = id.data; for (var i = 0; i < p.length; i += 4) p[i + 3] = p[i]; x.putImageData(id, 0, 0); }
      if (c.a) { x.globalCompositeOperation = "destination-in"; x.globalAlpha = c.a; x.fillRect(0, 0, W, H); x.globalAlpha = 1; }
      x.globalCompositeOperation = "source-in"; x.fillStyle = css(Cc[c.c], 1); x.fillRect(0, 0, W, H);
      return t;
    }
    var STARS = { d: parseStars("wrStarsDawn"), n: parseStars("wrStarsNight") }, SZ = [9.5, 7.5, 5.8, 4.6, 3.6], SO = [1, 1, 1, 0.82, 0.55];
    function parseStars(id) {
      return [].map.call(d.querySelectorAll("#" + id + " path"), function (p) {
        var cl = (p.getAttribute("class") || "z4 tw").split(" "), pts = [];
        (p.getAttribute("d") || "").replace(/M(-?\d+) (-?\d+)h0/g, function (_, x, y) { pts.push(+x / 1000, +y / 1000); return ""; });
        return { z: +cl[0].charAt(1), t: cl[1], p: pts };
      });
    }
    /* every pixel of the sky, in linear light: the gradient, the rose band and the Earth's shadow away from
       the sun, the low sun's glow, the glow on the horizon under it, its rays, midday's light from above;
       then held under CAP (a soft knee) and encoded */
    function paint(s, sx, sy) {
      var px = img.data, sxw = Wd / cw, syh = Hd / ch, yhp = YH * Hd, R = s.gr * Math.max(Wd, Hd);
      var bx = s.bx * Wd, by = -0.1 * Hd, BRX = Math.max(0.17 * Wd + 0.1 * Hd, 0.5 * Wd), BRY = 0.38 * Hd, hx = s.hw * Wd, hy = s.hh * Hd;
      var gc = s.gc, hc = s.hc, rc = P.rays, hot = P.hot, n = 0, glow = s.ga > 0.004, rays = s.ra > 0.004, bloom = s.bl > 0.004, belt = s.b > 0.005, x, dx, u;
      var away = sx < Wd / 2 ? 1 : -1, z = s.z, mi = s.mi, h = s.h, ro = P.rose, sh = P.shade;
      for (x = 0; x < cw; x++) {
        u = (x + 0.5) / cw; dx = u * Wd - sx; DX[x] = dx;
        GX[x] = Math.exp(-dx * dx / (R * R)); HX[x] = Math.exp(-(dx / hx) * (dx / hx));
        var bd = (u * Wd - bx) / BRX; BX[x] = Math.exp(-bd * bd);
        VX[x] = 1 - s.vg * (Wd < 600 ? 0.2 : 0.45) * (2 * u - 1) * (2 * u - 1);
        OX[x] = s.b * (0.25 + 0.75 * clamp(0.5 + away * (u - 0.5) * 1.6));
      }
      for (var y = 0; y < ch; y++) {
        var py = (y + 0.5) * syh, t = py / Hd;
        var base = t < 0.5 ? mix(z, mi, t / 0.5) : t < YH ? mix(mi, h, (t - 0.5) / (YH - 0.5)) : h;
        var bt = (t - (YH - 0.09)) / 0.045, et = (t - (YH - 0.015)) / 0.03, rb = belt ? 0.55 * Math.exp(-bt * bt) : 0, eb = belt ? 0.5 * Math.exp(-et * et) : 0;
        var dy = py - sy, hv = (py - yhp) / hy, hrow = s.ha * 0.026 * Math.exp(-hv * hv), above = py < sy + 0.02 * Hd;
        var gy = glow ? 0.03 * s.ga * Math.exp(-dy * dy / (R * R)) : 0, bv = (py - by) / BRY, by2 = bloom ? s.bl * 0.06 * Math.exp(-bv * bv) : 0;
        for (x = 0; x < cw; x++, n += 4) {
          var r = base[0], gg = base[1], b = base[2], v = VX[x];
          if (belt) {
            var wr = rb * OX[x], we = eb * OX[x];
            r += (ro[0] - r) * wr; gg += (ro[1] - gg) * wr; b += (ro[2] - b) * wr;
            r += (sh[0] - r) * we; gg += (sh[1] - gg) * we; b += (sh[2] - b) * we;
          }
          var k = gy * GX[x], h2 = hrow * HX[x], k2 = by2 * BX[x];
          r = r * v + gc[0] * k + hc[0] * h2 + hot[0] * k2; gg = gg * v + gc[1] * k + hc[1] * h2 + hot[1] * k2; b = b * v + gc[2] * k + hc[2] * h2 + hot[2] * k2;
          if (rays && above) {
            dx = DX[x];
            var d2 = dx * dx + dy * dy, a = Math.atan2(dy, dx), q = 0.5 + 0.5 * Math.cos(a * 23 + 0.6) * Math.cos(a * 9 - 1.1);
            k = s.ra * 0.009 * q * q * Math.exp(-Math.sqrt(d2) / (0.8 * Wd)) * (1 - Math.exp(-d2 / (0.004 * Wd * Wd)));
            r += rc[0] * k; gg += rc[1] * k; b += rc[2] * k;
          }
          var L = 0.2126 * r + 0.7152 * gg + 0.0722 * b;
          if (L > KNEE) { var f = (KNEE + (CAP - KNEE) * (1 - Math.exp(-(L - KNEE) / (CAP - KNEE)))) / L; r *= f; gg *= f; b *= f; }
          px[n] = ENC[r > 1 ? 4095 : (r * 4095) | 0]; px[n + 1] = ENC[gg > 1 ? 4095 : (gg * 4095) | 0]; px[n + 2] = ENC[b > 1 ? 4095 : (b * 4095) | 0]; px[n + 3] = 255;
        }
      }
      sg.putImageData(img, 0, 0);
    }
    function sunAt(hr, vh) {
      /* the sun that day: hour angle from solar noon; looking south it climbs from the left, stands high,
         goes down right; its height over the true horizon is measured up from the hills' line */
      var H = (hr - @@NOON@@) * 15 * Math.PI / 180, x = Wd / 2 + SUNR * Math.sin(H) * kx;
      return [x, skyline(x, vh) - SUNR * Math.cos(H) * ky];
    }
    /* the real sky turned about the south pole (15 degrees an hour), cut off above the opening photograph */
    function stars(list, mw, a, rot, clip) {
      var cx = Wd / 2 * dpr, cy = YH * Hd * dpr, u = ky * dpr, c = Math.cos(rot), s = Math.sin(rot), top = clip * dpr;
      g.save(); g.beginPath(); g.rect(0, top, W2, H2 - top); g.clip();
      if (mw) { g.save(); g.translate(cx, cy); g.rotate(rot); g.globalAlpha = a * clamp(1 - clip / (0.5 * Hd)); g.drawImage(mw, -3 * u, -2.25 * u, 6 * u, 3 * u); g.restore(); }
      for (var k = 0; k < list.length; k++) {
        var q = list[k], r = Math.max(0.35, SZ[q.z] / 2000 * u), p = q.p;
        g.globalAlpha = a * SO[q.z]; g.fillStyle = Cs[q.t] || Cs.tw; g.beginPath();
        for (var j = 0; j < p.length; j += 2) {
          var X = cx + (p[j] * c - p[j + 1] * s) * u, Y = cy + (p[j] * s + p[j + 1] * c) * u;
          if (X < -3 || X > W2 + 3 || Y < top - 3 || Y > H2 + 3) continue;
          g.moveTo(X + r, Y); g.arc(X, Y, r, 0, 6.2832);
        }
        g.fill();
      }
      g.restore(); g.globalAlpha = 1;
    }
    function cloudAt(t, x, y, wd, ht, a, mark) { if (t && a > 0.004 && y < Hd && y + ht > 0) { g.globalAlpha = a; g.drawImage(t, x * dpr, y * dpr, wd * dpr, ht * dpr); g.globalAlpha = 1; mark(y, y + ht); } }
    function at(D, y, vh, geo) {
      var q = Math.round(D * 40);
      if (q !== lastQ) { lastQ = q; var sq = state(q / 40), sp = sunAt(sq.hr, vh); paint(sq, sp[0], sp[1]); }
      var s = state(D), sp2 = sunAt(s.hr, vh);
      /* the hills step aside while the course is flown on its map and stand in midday's haze; they keep out of
         the way of the opening photograph and the cards, and half step down for the 01 numerals */
      var rg = D < 1.8 ? 0 : D < 2.08 ? (D - 1.8) / 0.28 : D < 2.88 ? 1 : D < 3.15 ? 1 - 0.6 * (D - 2.88) / 0.27 : D < 4.4 ? 0.4 : D < 4.7 ? 0.4 * (4.7 - D) / 0.3 : 0;
      var band = vh - hzB - hzH, full = hzH + hzB + 4, sink = rg * full, clr = geo.clear;
      for (var i = 0; i < clr.length; i++) {
        var t = clr[i][0] - y, b = clr[i][1] - y;
        if (b <= band || t >= vh + hzH) continue;
        sink = Math.max(sink, Math.min(b - band, full * clr[i][2]) * clamp((vh + hzH - t) / hzH));
      }
      sink = Math.round(sink);
      var clip = Math.round(Math.max(0, Math.min(Hd, geo.clip - y))), up = sink < full - 1;
      /* the clouds' places: the street drifts slower than the page (far); the dusk cloud passes 05 into 06 a
         little slower than the page (between); the near cumulus passes 02 into 03 faster than the page */
      var sw = Wd <= 700 ? Wd : Math.min(Wd, 1.7 * Hd), sh = sw * (Wd <= 700 ? 680 / 800 : 640 / 1600);
      var stx = Wd - sw + (2.6 - D) * 0.04 * sw, sty = (Wd <= 700 ? 0.02 : 0.01) * Hd + (3.2 - D) * 0.025 * Hd;
      var nw = Wd <= 700 ? 0.96 * Wd : Math.min(0.54 * Wd, 840), nh = nw * 700 / 1200, nrel = geo.near - y, np = clamp((vh - nrel) / (vh + nh));
      var nx = Wd - nw + (Wd <= 700 ? 0.34 * Wd : 0.05 * Wd) + (0.04 - 0.08 * np) * nw, ny = nrel - (Wd <= 700 ? 0.02 : 0.04) * vh + (0.3 - 0.6 * np) * vh;
      var dw = Wd <= 700 ? 1.8 * Wd : Math.max(1.12 * Wd, 900), dh = dw * (Wd <= 700 ? 260 / 800 : 520 / 1600), drel = geo.dusk - y, dp = clamp((vh - drel) / (vh + dh));
      var dx = (Wd <= 700 ? -0.4 * Wd : -0.06 * Wd) + (-0.02 + 0.04 * dp) * dw, dy = drel - (Wd <= 700 ? 0.12 : 0.22) * vh + (-0.09 + 0.18 * dp) * vh, da = (dp < 0.45 ? 1 : 1 - (dp - 0.45) / 0.55) * clamp((6.7 - D) / 0.5);
      var nearOn = Math.abs(nrel - vh / 2) < 2 * vh, duskOn = Math.abs(drel - vh / 2) < 2 * vh;
      /* the canvas is composed again only when something on it has moved: a still stretch of sky costs nothing */
      var sees = function (top, ht) { return top < Hd && top + ht > 0; }, starsOn = s.sa > 0.004 || s.sb > 0.004;
      var key = [kind, up ? sink : -1, starsOn ? Math.round(D * 900) + "," + clip : "", s.sd > 0.004 ? Math.round(sp2[0]) + "," + Math.round(sp2[1]) : "",
        D > 1.7 && D < 5 && s.cs > 0.004 ? Math.round(stx / 2) + "," + Math.round(sty / 2) + "," + Math.round(s.cs * 50) : "",
        nearOn && sees(ny, nh) ? Math.round(ny) : "", duskOn && sees(dy, dh) ? Math.round(dy) + "," + Math.round(da * 50) : "", Math.round(s.lo * 25), Math.round(s.fm * 25), Math.round(s.fd * 25)].join("|");
      if (key === sig) return;
      sig = key;
      /* only the band drawn last time is cleared, and this frame's band noted */
      g.globalAlpha = 1; if (dirty[1] > dirty[0]) g.clearRect(0, dirty[0], W2, dirty[1] - dirty[0]);
      var y0 = H2, y1 = 0, mark = function (a, b) { a = Math.max(0, Math.floor(a * dpr) - 2); b = Math.min(H2, Math.ceil(b * dpr) + 2); if (b > a) { y0 = Math.min(y0, a); y1 = Math.max(y1, b); } };
      if (s.sa > 0.004 && clip < Hd) { stars(STARS.d, want("mwd"), s.sa, (s.hr - 5.5) * 15.04 * Math.PI / 180, clip); mark(clip, Hd); }
      if (s.sb > 0.004) { stars(STARS.n, D > 5 ? want("mwn") : null, s.sb, (s.hr - 19) * 15.04 * Math.PI / 180, 0); mark(0, Hd); }
      if (s.sd > 0.004 && up) {
        var r = Math.max(9, Math.min(15, 0.0135 * Math.min(Wd, Hd))), sx = sp2[0] * dpr, sy = (sp2[1] + sink) * dpr;
        g.globalAlpha = s.sd; g.fillStyle = css(Cc.sun, 1); g.beginPath(); g.arc(sx, sy, r * dpr, 0, 6.2832); g.fill(); g.globalAlpha = 1; mark(sy / dpr - r, sy / dpr + r);
      }
      if (duskOn) cloudAt(want("dusk"), dx, dy, dw, dh, da, mark);
      if (D > 1.7 && D < 5) cloudAt(want("street"), stx, sty, sw, sh, s.cs, mark);
      if (up) {
        var top = (band + sink) * dpr;
        g.drawImage(hills(s.lo, s.fm, s.fd), 0, top);
        if (hzB) { g.globalAlpha = s.lo; g.fillStyle = css(Cc.land, 1); g.fillRect(0, top + hzH * dpr - 1, W2, (hzB + 8) * dpr); g.globalAlpha = 1; }
        mark(band + sink, vh + 8);
      }
      if (nearOn) cloudAt(want("near"), nx, ny, nw, nh, 1, mark);
      dirty = [y0, y1];
    }
    tokens(); size();
    /* the site's sky tokens ease to the visitor's hour over two seconds after the page opens */
    root.addEventListener("transitionend", function (e) { if (e.target === root && e.propertyName === "--sky-cool") { tokens(); onScroll(); } });
    return { size: size, at: at };
  }
  function dayAt(line) {
    var t = geo.dT, n = t.length, i = 0;
    if (line <= t[0]) return 0;
    while (i < n - 1 && line >= t[i + 1]) i++;
    var end = i < n - 1 ? t[i + 1] : geo.docH;
    return Math.min(8, i + clamp((line - t[i]) / Math.max(1, end - t[i])));
  }

  /* the clouds and the ground under the course load once, as they come near; they, and the thermals,
     move only while they are close to the screen, so nothing off screen costs a frame */
  var nearEls = all(".wr-ground"), liveEls = all(".wr-ground,.wr-mark");
  if (IO) {
    var nio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-near"); nio.unobserve(e.target); } }); }, { rootMargin: "60% 0px 60% 0px" });
    nearEls.forEach(function (el) { nio.observe(el); });
    var lio = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle("is-live", e.isIntersecting); }); }, { rootMargin: "60% 0px 60% 0px" });
    liveEls.forEach(function (el) { lio.observe(el); });
  } else liveEls.forEach(function (el) { el.classList.add("is-near", "is-live"); });

  function measure() {
    var vh = w.innerHeight;
    var r = box.getBoundingClientRect(); geo.mapW = r.width; geo.mapH = r.height;
    geo.pin = root.classList.contains("wr-pin");
    geo.cStart = absTop(C); geo.cLen = Math.max(1, C.offsetHeight - Cst.offsetHeight);
    if (hzOn()) {
      W.style.height = ""; Wtr.style.transform = "";
      geo.over = Math.max(0, Wtr.scrollWidth - Wvp.clientWidth);
      W.style.height = Math.round(Wst.offsetHeight + geo.over * 1.05 + vh * 0.15) + "px";
      geo.wStart = absTop(W);
      geo.wLen = Math.max(1, W.offsetHeight - Wst.offsetHeight);
    } else { W.style.height = ""; Wtr.style.transform = ""; geo.over = 0; }
    geo.seg = tick ? tick.firstElementChild.offsetWidth : 0;
    geo.tickTop = tickBox ? absTop(tickBox) : 0;
    geo.tops = chaps.map(function (c) { return c ? absTop(c) : 0; });
    geo.ends = chaps.map(function (c, i) { return i + 1 < chaps.length ? geo.tops[i + 1] : (partner ? absTop(partner) : geo.tops[i] + 1); });
    geo.partner = partner ? absTop(partner) : 1e9;
    geo.foot = foot ? absTop(foot) : 1e9;
    geo.heroEnd = hero ? absTop(hero) + hero.offsetHeight : 0;
    geo.vh = vh;
    if (SKY) {
      SKY.size(); geo.dT = dayEls.map(function (e) { return e ? absTop(e) : 0; }); geo.docH = root.scrollHeight;
      /* the stars begin under the opening photograph (its parallax can carry it a sixth lower); the hills keep clear of it, the 01 numerals and the cards */
      var pic = hero && hero.querySelector(".wr-hero-pic"), hb = hero ? absTop(hero) + hero.offsetHeight : 0;
      geo.clip = pic ? Math.min(hb, absTop(pic) + pic.offsetHeight * 1.16) : hb;
      /* (the hills only half step down for the 01 numerals: sunrise is behind them) */
      geo.near = absTop(d.getElementById("wr-kerio")); geo.dusk = partner ? absTop(partner) : 1e9;
      geo.clear = [[0, geo.clip, 1]].concat(all(".is-theirs .wr-giga,.wr-tiers").map(function (e) { var t = absTop(e); return [t, t + e.offsetHeight, e.classList.contains("wr-giga") ? 0.55 : 1]; }));
    }
    swiped();
  }

  var queued = false;
  function frame() {
    queued = false;
    var y = w.scrollY, vh = geo.vh;
    if (geo.pin) render(clamp((clamp((y - geo.cStart) / geo.cLen) - 0.05) / 0.85));
    if (hzOn() && geo.over) {
      var q = clamp((y - geo.wStart) / geo.wLen);
      Wtr.style.transform = "translate3d(" + (-q * geo.over).toFixed(1) + "px,0,0)";
    }
    if (tick && !still && geo.seg && y + vh > geo.tickTop - 200 && y < geo.tickTop + 600) {
      tick.style.transform = "translate3d(" + (-((y * 0.55) % geo.seg)).toFixed(1) + "px,0,0)";
    }
    if (barEl) {
      var line = y + vh * 0.4, i = -1;
      for (var n = 0; n < geo.tops.length; n++) {
        if (geo.tops[n] <= line && line < geo.ends[n]) i = n;
        var p = clamp((line - geo.tops[n]) / Math.max(1, geo.ends[n] - geo.tops[n]));
        if (Math.abs(p - lastP[n]) > 0.002) { lastP[n] = p; lines[n].style.setProperty("--p", p.toFixed(3)); }
      }
      if (i !== cur) {
        cur = i;
        links.forEach(function (a, k) { if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
        if (i >= 0 && barOl && barOl.scrollWidth > barOl.clientWidth) {
          var li = links[i].parentNode;
          barOl.scrollTo({ left: Math.max(0, li.offsetLeft - barOl.clientWidth * 0.3), behavior: still ? "auto" : "smooth" });
        }
      }
      barEl.classList.toggle("is-on", y > geo.heroEnd - vh * 0.55 && y + vh < geo.foot + 2);
    }
    if (SKY) SKY.at(dayAt(y + vh * 0.5), y, vh, geo);
  }
  function onScroll() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
  function refresh() { measure(); if (!geo.pin) render(1); frame(); }

  measure();
  if (!geo.pin) render(1);
  frame();
  w.addEventListener("scroll", onScroll, { passive: true });
  var rz = 0;
  w.addEventListener("resize", function () { cancelAnimationFrame(rz); rz = requestAnimationFrame(refresh); }, { passive: true });
  w.addEventListener("load", refresh);
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(refresh);
  if (hzMq.addEventListener) hzMq.addEventListener("change", function (e) { if (!still) root.classList.toggle("wr-hz", e.matches); refresh(); });
  /* a key that moves into the strip brings its step on screen */
  Wtr.addEventListener("focusin", function (e) {
    if (!hzOn() || !geo.over) return;
    var item = e.target.closest(".wr-step,.wr-fig") || e.target;
    var q = clamp((item.offsetLeft - Wvp.clientWidth * 0.3) / geo.over);
    w.scrollTo(0, geo.wStart + q * geo.wLen);
  });

  /* 6. a ring cursor and magnetic buttons, under a fine pointer only */
  if (!still && mq("(hover: hover) and (pointer: fine)").matches) {
    var ring = d.createElement("div"); ring.className = "wr-cursor"; ring.setAttribute("aria-hidden", "true"); ring.innerHTML = "<i></i>";
    d.body.appendChild(ring);
    var cx = 0, cy = 0, craf = 0;
    function paint() { craf = 0; ring.style.transform = "translate3d(" + cx + "px," + cy + "px,0)"; }
    d.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      cx = e.clientX; cy = e.clientY; if (!craf) craf = requestAnimationFrame(paint);
      ring.classList.add("is-on");
      var t = e.target.closest ? e.target.closest("a,button,label,summary,[data-cursor]") : null;
      ring.classList.toggle("is-big", !!t && !t.hasAttribute("data-cursor"));
      ring.classList.toggle("is-map", !!t && t.hasAttribute("data-cursor"));
    }, { passive: true });
    d.addEventListener("pointerleave", function () { ring.classList.remove("is-on"); });
    w.addEventListener("blur", function () { ring.classList.remove("is-on"); });
    all(".wr-mag").forEach(function (m) {
      m.addEventListener("pointermove", function (e) {
        var r = m.getBoundingClientRect();
        var dx = Math.max(-10, Math.min(10, (e.clientX - (r.left + r.width / 2)) * 0.12)), dy = Math.max(-6, Math.min(6, (e.clientY - (r.top + r.height / 2)) * 0.2));
        m.style.transform = "translate3d(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px,0)";
      });
      m.addEventListener("pointerleave", function () { m.style.transform = ""; });
    });
  }
  } catch (err) {
    root.classList.remove("wr-pin", "wr-hz", "wr-sky-on");
    showAll();
  }
})();
</script>"""


def script():
    s = SCRIPT
    for k, v in (("REC", REC100), ("BEST", BEST), ("X0", X0), ("PX", PX_PER_KM), ("YO", YO), ("YB", YB),
                 ("RX", RX), ("RY", RY), ("CY", CY), ("CAP", SKY_CAP), ("NOON", SUN_NOON)):
        s = s.replace("@@%s@@" % k, repr(v))
    s = s.replace("@@SKYINFO@@", json.dumps({k: {"w": RIDGE_BOX[k][0], "h": RIDGE_BOX[k][1], "y": RIDGES[k]["sky"], "bb": RIDGES[k]["bb"]}
                                             for k in RIDGE_BOX}, separators=(",", ":"))).replace("@@IMG@@", REC_IMG)
    return s


def ld():
    return ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"WebPage",'
            '"@id":"%s#webpage","name":"%s","url":"%s","description":"%s",'
            '"isPartOf":{"@id":"https://paraglidingatlas.com/#website"},'
            '"publisher":{"@id":"https://paraglidingatlas.com/#organization"},"inLanguage":"en"}\n</script>'
            % (URL, TITLE, URL, DESC.replace('"', '\\"')))


def main():
    s = open(SHELL, encoding="utf-8").read()
    head, rest = s.split('<main id="v4-main">', 1)
    tail = rest.split("</main>", 1)[1]
    # the page's own title, description, address and picture
    head = re.sub(r"<title>.*?</title>", "<title>%s: Paragliding Atlas</title>" % TITLE, head, 1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + DESC, head, 1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, head, 1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + TITLE, head, 1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + DESC, head, 1)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + OG_IMG, head, 1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + URL, head, 1)
    # the partners page's own structured data and styles go; this page's come in
    head = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "WebPage".*?</script>',
                  lambda m: ld(), head, 1, flags=re.S)
    head = re.sub(r"<!--v4u-css-->.*?<!--/v4u-css-->", "", head, 1, flags=re.S)
    head = re.sub(r"\n<style>.*?</style>\n(?=<!-- site-schema -->)", lambda m: "\n<style>" + CSS + "</style>\n", head, 1, flags=re.S)
    head = head.replace(' aria-current="page" class="is-here"', "")
    if ".wr-hero" not in head or "Partner With Me" in head.split("<body")[0] or URL not in head:
        raise SystemExit("v4_record: the partners shell has changed; check the head")
    page = head + main_html() + tail.replace("</body>", script() + "\n</body>", 1)
    if "\u2014" in page:
        raise SystemExit("v4_record: an em dash crept in")
    # no colour written out anywhere: the styles and markup use only the tokens; the script's canvas formats
    # colours it has just read from the tokens (rgba( + numbers it computed), never a written-out value
    if re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", CSS + main_html()) or re.search(r"#[0-9a-fA-F]{6}\b|(rgba?|hsla?)\(\s*[\d.]", script()):
        raise SystemExit("v4_record: a raw colour crept in; use the design tokens")
    open(OUT, "w", encoding="utf-8").write(page)
    print("v4_record: %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    if "--images" in sys.argv:
        make_images()
    main()
