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
judges asked to graft from B and C:
  - the opening: the masked three-line title (the page's one typographic
    entrance), and on the first screen the two numbers (the mark to beat and
    his best, "about", "not a record course") beside the window, with one way
    straight down to the offer (B). On phones the photograph sits above the
    words so the type is on dark ground;
  - a chapter bar with every chapter's name, a reading line per chapter and a
    solid Partner button (B, C): along the top on wide screens, along the
    bottom on phones (the chapters' numbers there, with the name of the one
    being read beside them, so no name is ever cut), one bar at a time (it
    steps away while the site menu is back, and the menu never slides across
    it);
  - 01 the mark: 35.94 in solid grey against a solid orange "about 36", the
    sources beside the numbers (B), "The time to beat" line and a fold with
    the detail behind the numbers (C);
  - 02 the course: pinned and flown kilometre by kilometre with the scroll, as
    a hairpin out and back with a position dot, Leg, Flown and two clocks counting
    the same way (B), watch-face figures (C), a 100 / 200 km switch that works
    without JavaScript (two radio buttons and :has, B);
  - 03 Kerio Valley: the name in solid type, the full-bleed valley plate
    dissolving into the sky, the facts under it, the thermals as a vario
    gauge (B);
  - 04 the window: the 26 days as two continuous expedition bars with the
    two days between as a dashed hairline, "During" once across both (B, C),
    and the before and after as four steps in a grid (one row on wide
    screens, two by two on phones: nothing slides sideways, nothing is cut);
  - 05 the audience and 06 the offer: the counts, the portrait, the tiers
    with small 01 02 03 labels and an orange edge on the Title Partner (C).
    Photographs of people are crisp frames with a hairline edge and a caption
    under them (never half dissolved).

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
    Every number is true from the first frame (nothing counts up).

Motion only answers the visitor (scroll, pointer, tap, key); nothing loops or
runs on a timer. Reduced motion shows every finished state, unpinned; with
JavaScript off everything is readable and the switch still works; phones get
the simplest version. No libraries, no video.

The backgrounds (owner, 18 to 19 Oct 2026: "The background of the winning
page looks quite bland"; he chose option 2, "be creative, and use something
from online as well if needed"). No photographs of pilots, people or stock
paragliding: the page makes its own atmosphere, one record day over Kerio
Valley from first light to night, moved on by the scroll, told by light
alone. Third pass (19 Oct), after the owner's "the animations seem to give a
cheap rip-off feeling rather than a premium one, along with the graphics"
(he circled the clouds, and the hard seam where the Kerio photograph
begins) and two directors' audits: less, but better. The drawn clouds, the
drawn hills and acacias, the sun's disc and rays, the thermals, the ticker,
the count-ups, the ring cursor, the magnetic buttons, the outlined numerals,
the photograph inside the letters, the word-by-word headlines and the
sideways strip are gone; every photograph dissolves into the sky over a long
eased mask; the course and the day follow the scroll with weight (eased
toward it in one loop that stops when settled). Fourth pass (19 Oct, two
judges on the third): no fixed stripe anywhere in the sky (the horizon is the
bottom edge of the screen, so its light only falls off upward, and midday is
deep overhead and lighter toward the horizon, never darker in the middle);
the Kerio photograph's top is tinted with the very colour the sky has behind
it (sampled from the painted sky), so it meets no band; the footer's drawn
ridge gives way to a soft horizon of light; the headings simply stand (only
the opening title rises); one easing curve (the site's --ease); the stars
turn and fade on the compositor (redrawn only every few degrees), and no
photograph is scaled or drifted, so the scroll stays smooth.
  - the brightness limit: no pixel of the sky, and nothing drawn on it, is
    let past SKY_CAP (relative luminance 0.044, with a soft knee), which
    keeps 4.5:1 for the muted small words (--wr-dim, 4.5:1 up to 0.050) and
    for --gray-light body text (up to 0.0624). So light comes from contrast,
    not level: deep, saturated skies, and the light gathered where it falls;
  - the sky: one fixed canvas pair behind the page. The sky itself is painted
    small (one pixel for every seven to fourteen on screen) in linear light
    from the design tokens (the site's --sky-cool follows the visitor's clock,
    so the page's blues do too) and stretched by the browser; over it one
    canvas draws the stars, composed again only when they have moved.
    Pre-dawn under the stars; dawn cool overhead with a pale line of light
    rising from the bottom edge on the LEFT, where the sun comes up; a deep
    blue morning; midday deep and saturated overhead, lighter toward the
    horizon, darker at the sides; a warm afternoon; dusk on the RIGHT as an
    ember light rising from the bottom edge under a deep blue-violet sky (the
    warmth only at the horizon, never a band across the screen); then night.
    No objects: no disc, no clouds, no hills;
  - the sun: where it really is that day (6 Feb 2027, in the window, at the
    page's 0.72N 35.65E: declination -15.6, solar noon 12:51 EAT, up about
    06:52, down about 18:51), seen looking south down the valley; shown only
    as the light it puts on the horizon, under it;
  - the stars: the real sky over Kerio Valley that day, at 05:30 for the
    opening and 19:00 for the close, turning about the south celestial pole
    as the scroll moves the clock on (15 degrees an hour), coming out as the
    opening photograph dissolves away. No lines between them, no names. Positions and
    magnitudes (STARS) are from the npm package d3-celestial 0.7.35 (see its
    notice below), whose star data is XHIP: An Extended Hipparcos
    Compilation (Anderson and Francis 2012, VizieR V/137D), converted to
    GeoJSON at J2000 by Olaf Frohn. The Milky Way is not taken from the
    package: it is drawn here (img/record/mw-dawn.webp, mw-night.webp) from
    the galactic plane, in the stars' own projection (see make_images): an
    impression;
  - the close: on this page the footer's drawn ridge (img/ridge.svg) is
    replaced by a soft horizon: the night sky dissolving into the ground
    under a faint last light, with the page's grain carried over it;
  - 02 the course: Kenya's ground under the line, as form lines traced
    (marching squares) from the chart sheet's shaded relief
    (assets/destinations/kenya/map/kenya-sheet-terrain.webp), so lines of
    equal shade, smoothed into curves: form lines, not surveyed contours.
    Cut round Kerio Valley and turned a quarter so the Rift runs along the
    course, four levels, each faintly filling the land above it (terraces);
    vector, crisp at every width (img/record/ground.svg), seen only round the
    course drawing (a soft oval), sliding under the position out and back
    with the same eased progress. The position is a plain orange dot, as a
    live tracker shows it;
  - the page's still grain lies in the page itself, over the sky (it dithers
    the gradients, so no banding).
Without JavaScript, and with reduced motion, the same day is one still
gradient down the whole page (its stops in STILL; every stop under the same
limit with each of the site's four skies), with the night's stars over the
close. Nothing moves.
Muted small words (the markers, chapter numbers, sources) are lifted from
--gray to a mix of --gray-light and --gray, so they keep 4.5:1 on a sky. The
partner cards are solid, so the sky does not show through the offer.
The image files are made by `python3 tools/v4_record.py --images` (numpy,
Pillow and contourpy), from the site's own files and the geometry here;
nothing in them comes from online. Files in img/record/: ground.svg and
mw-dawn, mw-night (the earlier passes' relief, contour and cloud masks are
gone).

The page takes the v4 shell (head, menu, footer) from partners.html and is
prototype-only (tools/v2_site.py PROTO_ONLY) until the owner approves it.

    python3 tools/v4_record.py
"""
import datetime
import math
import os
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
    """A headline: it arrives whole (see the CSS), so the words stay plain text."""
    return text


def ease_stops(p0, p1, a0, a1, n=8, col="var(--bg)"):
    """Gradient stops for a smoothstep from opacity a0 at p0% to a1 at p1%: no knee at either end, so
    no edge can be found where a photograph or a shade dissolves into the sky."""
    out = []
    for i in range(n + 1):
        t = i / float(n)
        a = a0 + (a1 - a0) * t * t * (3 - 2 * t)
        p = "%g%%" % round(p0 + (p1 - p0) * t, 2)
        if a <= 0.0005:
            out.append("transparent " + p)
        elif a >= 0.9995:
            out.append(col + " " + p)
        else:
            out.append("color-mix(in srgb,%s %g%%,transparent) %s" % (col, round(a * 100, 1), p))
    return ",".join(out)


def mask(*parts):
    """A vertical mask from runs of stops (see ease_stops), written once and given to both the -webkit- and the
    standard property."""
    return "--wr-m:linear-gradient(180deg,%s);-webkit-mask-image:var(--wr-m);mask-image:var(--wr-m);" % ",".join(parts)


def mask2(vert, horiz):
    """Vertical and horizontal runs of stops intersected: an edge that dissolves on all four sides."""
    return ("--wr-m:linear-gradient(180deg,%s),linear-gradient(90deg,%s);-webkit-mask-image:var(--wr-m);"
            "-webkit-mask-composite:source-in;mask-image:var(--wr-m);mask-composite:intersect;" % (vert, horiz))


def rmask(shape, stops):
    """A radial mask (an ellipse from its centre outward, from runs of stops), with the -webkit- copy."""
    return "--wr-m:radial-gradient(%s,%s);-webkit-mask-image:var(--wr-m);mask-image:var(--wr-m);" % (shape, stops)


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


def defs():
    """The Milky Way's grey-to-alpha filter (in a rendered, empty SVG) and the two skies' stars (in a hidden
    one, read by the script and used by the still page's night): one copy of each in the page."""
    flt = '<filter id="wrLumA" color-interpolation-filters="sRGB"><feColorMatrix type="luminanceToAlpha"/></filter>'
    stars = "".join('<g id="%s">%s</g>' % (gid, stars_g(key)) for key, gid in (("dawn", "wrStarsDawn"), ("night", "wrStarsNight")))
    return ('<svg class="wr-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>' + flt + "</defs></svg>"
            '<div class="wr-data" hidden><svg aria-hidden="true" focusable="false"><defs>' + STAR_NOTE + stars + "</defs></svg></div>\n")


def sky_html():
    """The fixed sky behind the whole page: the sky itself, painted small and stretched by the browser, and over
    it one canvas for everything drawn on the sky (see SCRIPT, part 7)."""
    return '<div class="wr-sky" aria-hidden="true"><canvas class="wr-sky-c" width="16" height="16"></canvas><canvas class="wr-sky-o" width="16" height="16"></canvas></div>\n'


def night_static():
    """The close's stars for a still page (no script, or reduced motion): the night sky's own dots."""
    return ('<div class="wr-night" aria-hidden="true"><svg viewBox="-1500 -2250 3000 2350" preserveAspectRatio="xMidYMax slice" focusable="false">'
            '<use href="#wrStarsNight"/></svg></div>')


def make_images():
    """Write the background images into prototypes/v4/img/record/ (see the docstring), all from the
    site's own files or from geometry: the Milky Way and the ground's form lines."""
    import gzip
    import contourpy
    import numpy as np
    from PIL import Image, ImageFilter
    out = os.path.join(V4, REC_IMG)
    os.makedirs(out, exist_ok=True)
    kenya = os.path.join(ROOT, "assets", "destinations", "kenya")
    # the earlier passes' files: relief and contours, then the clouds (cut in the third pass: flat masks
    # under the brightness limit read as cardboard, so the sky keeps only its light)
    for old in (("relief-w.webp", "relief-p.webp", "contours-p.webp") + tuple("cloud-%d-%s.webp" % (n, t) for n in (1, 3, 4) for t in "ls")
                + tuple("%s-%s.webp" % (n, t) for n in ("street", "cu", "dusk") for t in "ls")):
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

    # 2. the ground: form lines traced from the chart sheet's relief (kenya-sheet-terrain.webp, a shaded
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
    # four levels (every second of eight), each line a closed quadratic B-spline: the simplified points are
    # the control points and the curve runs through their midpoints (M, one q, then t after t, each t's control
    # the mirror of the last), so the lines are smooth curves with no corners or stair-steps, at the size of the
    # polylines they replace
    S4, paths = 4, []
    for lv in np.percentile(f, np.linspace(34, 93, 8))[::2]:
        d = []
        for ln in gen.lines(lv):
            ln = ln - 1
            if len(ln) < 6 or np.sum(np.hypot(*np.diff(ln, axis=0).T)) * 2 < 60:
                continue
            q = np.round(dp(ln, 0.7) * S4).astype(int)
            q = q[np.r_[True, np.any(np.diff(q, axis=0) != 0, axis=1)]]
            if len(q) > 1 and np.all(q[0] == q[-1]):
                q = q[:-1]
            if len(q) < 4:
                continue
            # in half units: every midpoint (the sum of two neighbours) and every control point (twice a point) is whole
            mid, ctl = q + np.roll(q, -1, axis=0), q * 2
            u = lambda v: "%g" % (v / 2.0)
            st = mid[-1]
            seg = "M%s %sq%s %s %s %s" % (u(st[0]), u(st[1]), u(ctl[0][0] - st[0]), u(ctl[0][1] - st[1]),
                                         u(mid[0][0] - st[0]), u(mid[0][1] - st[1]))
            rel = np.diff(mid, axis=0)
            d.append(seg + "t" + " ".join("%s %s" % (u(dx), u(dy)) for dx, dy in rel) + "z")
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
  /* one easing curve for every motion on the page: the site's own --ease, long and decelerating (no snap, no overshoot) */
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

/* the opening title: each line rises inside its own mask, once */
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
.wr-hero{position:relative;min-height:calc(100svh - var(--wr-top));display:flex;flex-direction:column;justify-content:flex-end;overflow:clip;background:var(--bg);}
.wr-hero-pic{position:absolute;inset:0;z-index:-2;overflow:clip;}
.wr-hero-pic img{display:block;width:100%;height:100%;object-fit:cover;object-position:66% 46%;}
.wr-hero::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:
  linear-gradient(90deg,color-mix(in srgb,var(--bg) 80%,transparent) 0%,color-mix(in srgb,var(--bg) 38%,transparent) 46%,transparent 72%),
  linear-gradient(180deg,color-mix(in srgb,var(--bg) 45%,transparent) 0%,transparent 24%,transparent 46%,color-mix(in srgb,var(--bg) 70%,transparent) 78%,var(--bg) 100%);}
.wr-hero-in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,16.5rem);align-items:end;gap:var(--sp-5);padding-block:var(--sp-5) calc(var(--sp-section) * 1.15);}
.wr-kick{margin:0 0 var(--sp-3);text-wrap:balance;font-size:var(--fs-micro);font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--orange);
  text-shadow:0 1px 2px color-mix(in srgb,var(--bg) 85%,transparent);}
.wr-mega{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wr-mega);line-height:.9;letter-spacing:-.045em;color:var(--white);}
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
/* the way down: one hairline at the foot of the opening (a link to the first chapter, 44px wide to the touch) */
.wr-cue{position:absolute;left:50%;bottom:0;z-index:5;display:block;width:44px;height:clamp(3rem,9vh,5rem);margin-left:-22px;}
.wr-cue::before{content:"";position:absolute;left:50%;top:0;bottom:0;width:1px;background:linear-gradient(180deg,transparent,var(--edge-hi));}
.wr-cue:hover::before,.wr-cue:focus-visible::before{background:linear-gradient(180deg,transparent,var(--orange));}

/* ---------- the chapter bar: every chapter named, a reading line under each ---------- */
.wr-bar{z-index:55;}
.wr-bar-in{display:flex;align-items:center;gap:var(--sp-2);}
.wr-bar ol{position:relative;list-style:none;margin:0;padding:0;display:flex;}
.wr-bar ol a{position:relative;display:flex;align-items:center;gap:.5rem;min-height:44px;padding:0 .8rem;white-space:nowrap;text-decoration:none;
  font-size:var(--fs-small);font-weight:500;color:var(--gray-light);transition:color .3s var(--ease);}
.wr-bar ol a span{font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--wr-dim);transition:color .3s var(--ease);}
.wr-bar ol a b{font-weight:inherit;}
.wr-bar ol a i{position:absolute;left:.8rem;right:.8rem;bottom:6px;height:1px;background:var(--edge);overflow:hidden;}
.wr-bar ol a i::after{content:"";position:absolute;inset:0;background:var(--orange);transform:scaleX(var(--p,0));transform-origin:0 50%;}
.wr-bar ol a:hover,.wr-bar ol a[aria-current]{color:var(--white);}
.wr-bar ol a[aria-current] span{color:var(--white);}
.wr-bar .wr-btn{flex:none;margin-left:auto;}
@media (min-width:900px){
  .wr-bar{border-block:1px solid var(--line);background:var(--wr-solid);}
  .wr-bar-in{height:var(--wr-bar);}
  .wr-bar ol{margin-left:-.8rem;}
  .wr-js .wr-bar{position:fixed;left:0;right:0;top:0;transform:translateY(-104%);transition:transform .45s var(--ease);}
  .wr-js .wr-bar.is-on{transform:none;transition-delay:.24s;}
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
  html.v2-nav-up.wr-js .wr-bar.is-on{transform:translateY(110%);}
}
/* while the site menu is back at the top, it does the navigating: one bar at a time, and nothing under it shifts.
   The bar steps away at once and comes back only after the menu has gone (the delay above), so they never cross */
@media (min-width:900px){html.v2-nav-up.wr-js .wr-bar.is-on{transform:translateY(-104%);transition-delay:0s;}}
/* a phone: the chapters' numbers, and beside them the name of the one being read (from the script), so no
   name is ever cut by the screen's edge or by the button; every name stays in the links for screen readers */
@media (max-width:560px){
  .wr-js .wr-bar-in::before{content:attr(data-cur);flex:0 0 5.2rem;min-width:0;overflow:hidden;white-space:nowrap;
    font-size:var(--fs-small);font-weight:500;color:var(--white);}
  .wr-js .wr-bar ol{flex:0 1 auto;overflow:visible;margin-left:0;padding-left:0;-webkit-mask-image:none;mask-image:none;}
  .wr-js .wr-bar ol a{padding:0 .42rem;}
  .wr-js .wr-bar ol a span{display:inline;font-size:var(--fs-small);}
  .wr-js .wr-bar ol a b{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
  .wr-js .wr-bar ol a i{left:.42rem;right:.42rem;}
  .wr-js .wr-bar-in{padding-left:var(--wr-x);}
}
/* a key that reaches the bar always finds it on screen */
.wr-js .wr-bar:focus-within,html.v2-nav-up.wr-js .wr-bar:focus-within{transform:none;}

/* ---------- 01 the mark to beat: theirs in neutral, mine in orange, both solid ---------- */
.wr-mark{padding-block:var(--wr-pad) calc(var(--wr-pad) * .55);}
.wr-duel{display:grid;margin-top:var(--sp-5);}
.wr-big{min-width:0;}
.wr-big.is-mine{justify-self:end;text-align:right;margin-top:calc(var(--wr-giga) * -.2);}
.wr-cap{margin:0 0 .4rem;font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-giga{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wr-giga);line-height:.84;letter-spacing:-.055em;color:var(--white);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.is-theirs .wr-giga{color:var(--gray-light);}
.is-mine .wr-giga{color:var(--orange);}
.wr-giga small{font-size:.15em;font-weight:600;letter-spacing:0;margin-left:.35em;color:var(--gray-light);}
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
/* the flown line: one clean orange stroke, no bloom */
.wr-flown{fill:none;stroke:var(--orange);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;}
.wr-gate{stroke:var(--white);stroke-width:2;vector-effect:non-scaling-stroke;}
.wr-tk{stroke:var(--edge-hi);stroke-width:1;vector-effect:non-scaling-stroke;}
.wr-pl{position:absolute;bottom:calc(100% + .7rem);left:0;white-space:nowrap;font-size:var(--fs-small);line-height:1.3;color:var(--white);}
.wr-pl i{display:block;font-style:normal;font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-tp{position:absolute;top:0;bottom:0;width:0;}
.wr-tp .wr-pl{transform:translateX(-50%);text-align:center;}
.wr-tp.v200 .wr-pl{transform:translateX(-100%);text-align:right;}
.wr-ring{position:absolute;left:0;top:50%;width:2.8rem;height:2.8rem;margin:-1.4rem 0 0 -1.4rem;box-sizing:border-box;border-radius:50%;border:1px dashed var(--gray-light);}
.wr-ring::after{content:"";position:absolute;left:50%;top:50%;width:7px;height:7px;margin:-3.5px 0 0 -3.5px;border-radius:50%;background:var(--white);}
/* the position: a plain orange dot in a hairline ring, as a live tracker draws it (no pictogram, nothing turning) */
.wr-gl{position:absolute;left:3%;top:75%;width:22px;height:22px;margin:-11px 0 0 -11px;pointer-events:none;}
.wr-gl::before{content:"";position:absolute;inset:0;border-radius:50%;border:1px solid color-mix(in srgb,var(--orange) 55%,transparent);
  background:color-mix(in srgb,var(--orange) 10%,transparent);}
.wr-gl::after{content:"";position:absolute;left:50%;top:50%;width:8px;height:8px;margin:-4px 0 0 -4px;border-radius:50%;background:var(--orange);}
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
/* a counting kilometre figure keeps three digits of room, so nothing beside it moves */
#wrKm{display:inline-block;min-width:3ch;text-align:right;}

/* ---------- 03 Kerio Valley: the name in solid type, then the valley ---------- */
.wr-place{padding-top:var(--wr-pad);}
.wr-cut{width:fit-content;max-width:100%;margin:0;font-family:var(--font-display);font-weight:700;font-size:min(calc(var(--fs-display) * 3),22vw);
  line-height:.86;letter-spacing:-.05em;color:var(--white);}
.wr-cut span{display:block;}
.wr-plate{position:relative;margin:var(--sp-5) 0 0;}
/* the photograph, still and at its own scale: up and down it dissolves through its own long mask, so no box edge
   can show; past 1440px it stops growing (the file is 1152px wide) and dissolves at the sides as well */
.wr-plate-img{position:relative;height:min(96svh,62rem);overflow-x:clip;}
.wr-par{position:absolute;inset:0;max-width:1440px;margin:0 auto;pointer-events:none;}
.wr-par img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 72%;}
/* its pale haze is tinted toward the very sky behind it (the script samples the painted sky into --wr-plate-sky;
   the still day's own colour there otherwise), so the photograph meets the sky without a band */
.wr-par::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,@@PAR_GRADE@@);}
.wr-facts{position:relative;z-index:2;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-4);
  box-sizing:border-box;max-width:var(--measure);margin:0 auto;padding:var(--sp-4) var(--wr-x) 0;}
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
.wr-win .wr-h2{max-width:11ch;}
.wr-nw{white-space:nowrap;}
.wr-win .wr-lede{margin-top:var(--sp-2);}
/* the 26 days: each expedition one continuous bar, the two days between them a dashed hairline, the days as ticks
   over their numbers */
.wr-days{grid-area:days;min-width:0;}
.wr-days-k,.wr-days-bar,.wr-days-n{display:grid;grid-template-columns:repeat(26,minmax(0,1fr));gap:2px;}
.wr-days-k{margin-bottom:.9rem;}
.wr-days-k>span{display:flex;flex-direction:column;gap:.2rem;padding-left:.7rem;border-left:1px solid var(--orange);font-size:var(--fs-body-s);line-height:1.3;color:var(--gray-light);}
.wr-days-k>span:first-child{grid-column:1/13;}
.wr-days-k>span:last-child{grid-column:15/27;}
.wr-days-k a{display:inline-flex;align-items:center;min-height:44px;margin:-.5rem 0 -.4rem;width:fit-content;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);color:var(--white);}
.wr-days-bar{align-items:center;}
.wr-days-bar i{display:block;height:4px;background:var(--orange);}
.wr-days-bar i.is-off{height:1px;margin-inline:3px;background:linear-gradient(90deg,var(--edge-hi) 50%,transparent 0) 0 0/6px 1px repeat-x;}
.wr-days-n{margin-top:.5rem;font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--gray);text-align:center;}
.wr-days-n span{position:relative;min-width:0;padding-top:.6rem;}
.wr-days-n span::before{content:"";position:absolute;left:50%;top:0;width:1px;height:5px;background:var(--edge-hi);}
.wr-days-dur{display:flex;flex-wrap:wrap;align-items:baseline;gap:.4rem 1rem;margin:var(--sp-3) 0 0;padding-top:.9rem;border-top:1px solid var(--live);font-size:var(--fs-body);line-height:1.45;color:var(--white);}
.wr-days-dur b{font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gray-light);}
/* before and after: four steps */
.wr-vp{grid-area:vp;min-width:0;}
.wr-track{display:flex;align-items:stretch;}
.wr-steps{list-style:none;margin:0;padding:0;display:flex;}
.wr-step{position:relative;flex:0 0 min(19rem,76vw);box-sizing:border-box;padding:var(--sp-4) var(--sp-5) var(--sp-2) 0;border-top:1px solid var(--edge);}
.wr-step::before{content:"";position:absolute;left:0;top:-5px;width:9px;height:9px;box-sizing:border-box;border-radius:50%;background:var(--bg);border:1px solid var(--gray-light);}
.wr-when{display:block;margin:0 0 var(--sp-2);font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-step h3{margin:0;font-family:var(--font-display);font-weight:600;font-size:calc(var(--fs-h3) * 1.15);line-height:1.15;color:var(--white);}
.wr-step p{margin:.7rem 0 0;max-width:16rem;font-size:var(--fs-body);line-height:1.5;color:var(--gray-light);}
.wr-step p a{display:inline-flex;align-items:center;min-height:44px;}

/* ---------- 05 the audience ---------- */
.wr-aud{padding-block:var(--wr-pad);}
.wr-aud-in{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,.85fr);grid-template-areas:"copy pic" "stats pic";column-gap:clamp(2rem,6vw,6rem);}
.wr-aud-copy{grid-area:copy;}
/* the portrait: a crisp frame in the page's light (its bright sky graded down from the top), the name under it */
.wr-portrait{grid-area:pic;position:relative;margin:calc(var(--sp-5) * 1.6) 0 0;align-self:start;}
.wr-portrait picture{position:relative;display:block;aspect-ratio:4/5;overflow:clip;outline:1px solid var(--line);outline-offset:-1px;}
.wr-portrait picture::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,@@PORTRAIT_GRADE@@);}
.wr-portrait figcaption{margin-top:.8rem;font-family:var(--font-mono);font-size:var(--fs-small);color:var(--wr-dim);}
.wr-stats{grid-area:stats;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-5) var(--sp-4);margin:var(--sp-5) 0 0;}
.wr-stats div{display:flex;flex-direction:column-reverse;justify-content:flex-end;padding-top:var(--sp-3);border-top:1px solid var(--edge);}
.wr-stats dd{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-display) * .95);line-height:1;letter-spacing:-.04em;color:var(--white);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.wr-stats dt{margin-top:.6rem;font-size:var(--fs-body-s);color:var(--gray-light);}

/* ---------- 06 the offer ---------- */
.wr-offer{padding-block:var(--wr-pad) var(--sp-section);background:radial-gradient(70% 60% at 85% 0%,var(--sky-warm),transparent 70%);}
.wr-offer-head{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(2rem,6vw,6rem);align-items:end;}
/* photographs of people: crisp frames with a hairline edge (never half dissolved), graded to the page's light */
.wr-offer-pic{position:relative;margin:0;aspect-ratio:4/3;overflow:clip;outline:1px solid var(--line);outline-offset:-1px;}
.wr-tiers{display:grid;grid-template-columns:minmax(0,1.2fr) repeat(2,minmax(0,1fr));gap:var(--sp-3);margin-top:var(--sp-5);}
.wr-tier{position:relative;padding:var(--sp-4);border-top:1px solid var(--edge-hi);}
.wr-tier.is-lead{border-top:2px solid var(--orange);}
/* the tier's number: a small label, so the card leads with its name */
.wr-tier-n{margin:0 0 var(--sp-2);font-family:var(--font-mono);font-size:var(--fs-small);line-height:1.4;letter-spacing:.08em;color:var(--wr-dim);}
.wr-tier-k{position:absolute;top:var(--sp-4);right:var(--sp-4);margin:0;padding:.2rem .5rem;border:1px solid var(--live);font-family:var(--font-mono);font-size:var(--fs-micro);line-height:1.4;color:var(--gray-light);}
.wr-tier h3{margin:0 0 var(--sp-3);font-family:var(--font-display);font-weight:700;font-size:var(--fs-h3);line-height:1.1;color:var(--white);}
.wr-tier ul{list-style:none;margin:0;padding:0;display:grid;gap:.15rem;}
.wr-tier li{position:relative;padding:.5rem 0 .5rem 1.2rem;border-top:1px solid var(--line);font-size:var(--fs-body);line-height:1.45;color:color-mix(in srgb,var(--white) 88%,var(--gray-light));}
.wr-tier li::before{content:"";position:absolute;left:0;top:1.2em;width:.5rem;height:2px;background:var(--orange);}
.wr-cta{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-3) var(--sp-5);margin-top:var(--sp-5);}
.wr-cta .btn-solid{margin:0;font-size:var(--fs-lead);padding:1.05rem 2.3rem;}
.wr-cta .btn-lines{display:inline-flex;align-items:center;min-height:48px;box-sizing:border-box;font-size:var(--fs-lead);}
.wr-cta .btn-lines:hover{color:var(--orange);border-color:var(--orange);}
.wr-src{margin:var(--sp-5) 0 0;font-size:var(--fs-small);line-height:1.8;color:var(--gray);}

/* ---------- photographs in frames: graded to the page's light ---------- */
.wr-offer-pic img,.wr-portrait img{display:block;width:100%;height:100%;object-fit:cover;filter:saturate(.72) brightness(.74);}

/* ---------- motion: only in answer to the visitor, and none of it when they ask for stillness ---------- */
@media (prefers-reduced-motion:no-preference){
  /* two entrances on the whole page, both on the site's one curve. The opening title: three lines rising once,
     after the face has loaded, then its lines under it */
  .wr-js .wr-mega .wr-ln>span{transform:translateY(104%);transition:transform 1.2s var(--ease);transition-delay:calc(var(--i,0) * 90ms);}
  .wr-js .wr-mega.is-in .wr-ln>span{transform:none;}
  .wr-js .wr-hero .wr-fade{opacity:0;transform:translateY(14px);transition:opacity 1s var(--ease) .35s,transform 1.1s var(--ease) .35s;}
  .wr-js .wr-hero .wr-fade.is-in{opacity:1;transform:none;}
  /* and the window's days, drawn once left to right, as time passing. Everything else simply stands; the
     photographs stay still (no drift, no zoom), so the scroll is the only thing moving the page */
  .wr-js .wr-days-bar{clip-path:inset(0 100% 0 0);transition:clip-path 1.6s var(--ease) .1s;}
  .wr-js .wr-days.is-in .wr-days-bar{clip-path:inset(0);}
  html{scroll-behavior:smooth;}
}
@media (prefers-reduced-motion:reduce){
  .wr *,.wr *::before,.wr *::after{transition:none!important;}
}

/* ---------- the pinned course (set before the first paint by the script at the top of main) ---------- */
.wr-pin .wr-course{height:250vh;}
.wr-pin .wr-course .wr-stage{position:sticky;top:0;box-sizing:border-box;height:100svh;padding-block:calc(var(--wr-bar) + var(--sp-3)) var(--sp-3);display:flex;align-items:center;overflow:hidden;}

/* ---------- wide screens: the window's four steps in one calm row ---------- */
@media (min-width:900px){
  .wr-win-in{grid-template-columns:minmax(0,20rem) minmax(0,1fr);grid-template-areas:"head days" "vp vp";column-gap:var(--sp-5);align-items:end;}
  .wr-track{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-4);}
  .wr-steps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-4);}
  .wr-step{padding-right:0;}
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
  .wr-hero-sub{margin-top:var(--sp-3);}
  .wr-hero-meta{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:var(--sp-3);margin-top:var(--sp-4);border-left:0;padding:var(--sp-3) 0 0;border-top:1px solid var(--edge-hi);}
  .wr-cue{display:none;}
  .wr-big.is-mine{margin-top:var(--sp-5);}
  .wr-read{grid-template-columns:minmax(0,1fr);gap:0;}
  .wr-read div{display:flex;align-items:baseline;justify-content:space-between;gap:var(--sp-2);padding:.6rem 0;border-bottom:1px solid var(--line);}
  .wr-read dd,.wr-read .is-leg dd{margin:0;font-size:calc(var(--fs-h2) * 1.05);}
  .wr-pin .wr-course{height:220vh;}
  .wr-pin .wr-course .wr-stage{padding-block:var(--sp-3) calc(var(--sp-3) + var(--wr-dock));}
  .wr-facts{grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-3);padding-top:var(--sp-3);}
  .wr-plate-img{height:70svh;}
  /* the four steps two by two: nothing slides sideways and nothing is cut by the screen's edge */
  .wr-track{display:grid;grid-template-columns:minmax(0,1fr);row-gap:var(--sp-2);}
  .wr-steps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:var(--sp-3);}
  .wr-step{padding:var(--sp-3) 0 var(--sp-2);}
  .wr-step p{max-width:none;}
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
  .wr-course-head .wr-h2{font-size:calc(var(--fs-h1) * 1.05);}
  .wr-ring{width:2rem;height:2rem;margin:-1rem 0 0 -1rem;}
  .wr-scale span:nth-child(even){display:none;}
  .wr-facts{grid-template-columns:minmax(0,1fr);}
  .wr-days-n{display:none;}
  .wr-days-bar i{height:5px;}
  .wr-days-bar i.is-off{height:1px;}
  .wr-days-k a{font-size:var(--fs-body);}
  .wr-stats{gap:var(--sp-4) var(--sp-3);}
  .wr-stats dd{font-size:calc(var(--fs-display) * .82);}
  .wr-tiers{grid-template-columns:minmax(0,1fr);}
  .wr-cta{flex-direction:column;align-items:flex-start;}
}
/* ---------- the record day: the backgrounds (see the docstring) ---------- */
/* small muted words sit on a sky now, not flat black: lifted enough to keep 4.5:1 on its brightest */
.wr{--wr-dim:color-mix(in srgb,var(--gray-light) 84%,var(--gray));}
.wr-tbd,.wr-no,.wr-src,.wr-days-n{color:var(--wr-dim);}
.wr-mark,.wr-offer{position:relative;isolation:isolate;}
.wr-sky,.wr-night{display:none;}
.wr-defs{position:absolute;width:0;height:0;overflow:hidden;}
/* the partner cards are solid: the sky does not show through the offer */
.wr .wr-tier{background:linear-gradient(180deg,color-mix(in srgb,var(--white) 6%,transparent),color-mix(in srgb,var(--white) 1.5%,transparent) 70%),color-mix(in srgb,var(--card) 94%,var(--bg));}
.wr .wr-tier.is-lead{background:linear-gradient(180deg,color-mix(in srgb,var(--orange) 9%,transparent),color-mix(in srgb,var(--white) 2%,transparent) 70%),color-mix(in srgb,var(--card) 94%,var(--bg));}
/* the course's grain fades at both ends, so no line marks its edges (with the moving sky the page's own grain is there instead) */
.wr-sky-on .wr-course.wr-grain::after{display:none;}
.wr-course.wr-grain::after{@@M_COURSE_GRAIN@@}

/* ----- the still day (no script, or reduced motion): one gradient down the whole page, every stop under the
   moving sky's brightness limit (checked with each of the site's four skies); cool everywhere, the warmth of
   dusk held to one low stop; the night's stars at the close, settling onto the footer's soft horizon ----- */
.wr,footer{--wr-s0:color-mix(in srgb,var(--bg) 62%,var(--sky-cool));
  --wr-s1:color-mix(in srgb,color-mix(in srgb,var(--bg) 58%,var(--sky-cool)) 92%,var(--white));
  --wr-s2:color-mix(in srgb,color-mix(in srgb,var(--bg) 54%,var(--sky-cool)) 91%,color-mix(in srgb,var(--white) 86%,var(--orange)));
  --wr-s3:color-mix(in srgb,color-mix(in srgb,var(--bg) 50%,var(--sky-cool)) 94%,var(--white));
  --wr-s4:color-mix(in srgb,color-mix(in srgb,var(--bg) 46%,var(--sky-cool)) 93%,var(--white));
  --wr-s5:color-mix(in srgb,color-mix(in srgb,var(--bg) 56%,var(--sky-cool)) 95%,var(--white));
  --wr-s6:color-mix(in srgb,color-mix(in srgb,var(--bg) 64%,var(--sky-cool)) 95%,var(--orange));
  --wr-s7:color-mix(in srgb,var(--bg) 62%,var(--sky-cool));
  --wr-s8:color-mix(in srgb,var(--bg) 66%,var(--sky-cool));}
:root:not(.wr-sky-on) .wr{background:linear-gradient(180deg,var(--bg) 0,var(--bg) @@S0@@%,var(--wr-s0) @@S1@@%,var(--wr-s1) @@S2@@%,var(--wr-s2) @@S3@@%,
  var(--wr-s3) @@S4@@%,var(--wr-s4) @@S5@@%,var(--wr-s3) @@S6@@%,var(--wr-s5) @@S7@@%,var(--wr-s6) @@S8@@%,var(--wr-s7) @@S9@@%,var(--wr-s8) @@S10@@%,var(--wr-s8));}
:root:not(.wr-sky-on) .wr-course,:root:not(.wr-sky-on) .wr-offer{background:none;}
:root:not(.wr-sky-on) .wr-night{display:block;position:absolute;left:0;right:0;bottom:0;z-index:-1;height:min(110vh,80%);pointer-events:none;@@M_NIGHT@@}
.wr-night svg{display:block;width:100%;height:100%;}
/* ----- the close: the night dissolves into the ground over a long eased band, under a faint last light (on
   this page the footer's drawn ridge gives way to this soft horizon: no outline, no flat cut-out) ----- */
footer{--wr-fh:clamp(110px,13vw,200px);padding-top:var(--wr-fh);
  background:linear-gradient(180deg,@@FOOT_SKY@@) top/100% var(--wr-fh) no-repeat,linear-gradient(var(--bg),var(--bg)) bottom/100% calc(100% - var(--wr-fh) + 1px) no-repeat;}
:root:not(.wr-sky-on) footer{background:linear-gradient(180deg,@@FOOT_STILL@@) top/100% var(--wr-fh) no-repeat,linear-gradient(var(--bg),var(--bg)) bottom/100% calc(100% - var(--wr-fh) + 1px) no-repeat;}
footer::after{background:radial-gradient(58% 40% at 68% 36%,color-mix(in srgb,var(--sky-horizon) 55%,transparent),transparent 74%);}

/* ----- the moving sky (with the script and motion): one canvas, fixed behind everything ----- */
.wr-sky-on .wr-sky{display:block;position:fixed;left:0;top:0;z-index:-1;width:100%;height:100vh;height:100lvh;overflow:hidden;pointer-events:none;contain:strict;background:var(--wr-s0);}
.wr-sky-c,.wr-sky-o{position:absolute;left:0;top:0;width:100%;height:100%;display:block;}
.wr-sky-o{opacity:0;will-change:transform,opacity;}
/* the page's still grain, in the page itself (no layer of its own): film texture on every chapter, and no banding in the sky's gradients */
.wr-sky-on .wr{background-image:__GRAIN2__;background-size:220px 220px;}
/* and carried over the footer, whose soft horizon closes the page, so no line marks where the page ends */
.wr-sky-on footer::before{display:block;content:"";position:absolute;inset:0;height:auto;pointer-events:none;background:__GRAIN2__ 0 0/220px 220px;}
/* the star dots, as the still page's night uses them (sizes in the drawing's units) */
.wr .z0,.wr .z1,.wr .z2,.wr .z3,.wr .z4{fill:none;stroke-linecap:round;}
.wr .z0{stroke-width:9.5;}.wr .z1{stroke-width:7.5;}.wr .z2{stroke-width:5.8;}.wr .z3{stroke-width:4.6;opacity:.82;}.wr .z4{stroke-width:3.6;opacity:.55;}
.wr .tw,.wr .tb{stroke:var(--white);}.wr .ty{stroke:color-mix(in srgb,var(--white) 80%,var(--orange));}.wr .tr{stroke:color-mix(in srgb,var(--white) 58%,var(--orange));}

/* the chapters let the sky through */
.wr-sky-on .wr-hero,.wr-sky-on .wr-course,.wr-sky-on .wr-offer{background:none;}
.wr-sky-on .wr-hero.wr-grain::after{@@M_HERO_GRAIN@@}
/* the opening photograph dissolves into the sky over its lower half, on a long eased mask that stays put while
   the page scrolls; its shade for the words fades with it, so no band marks where it ends */
.wr-sky-on .wr-hero::before{background:linear-gradient(180deg,color-mix(in srgb,var(--bg) 45%,transparent) 0%,transparent 24%);}
.wr-sky-on .wr-hero-pic{@@M_HERO@@}
.wr-sky-on .wr-hero-pic::after{content:"";position:absolute;inset:0;pointer-events:none;background:
  linear-gradient(90deg,color-mix(in srgb,var(--bg) 80%,transparent) 0%,color-mix(in srgb,var(--bg) 38%,transparent) 46%,transparent 72%),
  linear-gradient(180deg,@@HERO_SHADE@@);}
/* the Kerio photograph fades into whatever sky is behind it (moving or still), at both ends, on long eased masks */
.wr-par{@@M_PLATE@@}
@media (min-width:1500px){.wr-par{@@M_PLATE_W@@}}
@media (max-width:899.98px){
  .wr-sky-on .wr-hero::before{background:linear-gradient(180deg,color-mix(in srgb,var(--bg) 30%,transparent) 0%,transparent 18%);}
  .wr-sky-on .wr-hero-pic{@@M_HERO_P@@}
  .wr-sky-on .wr-hero-pic::after{background:linear-gradient(180deg,@@HERO_SHADE_P@@);}
  .wr-par{@@M_PLATE_P@@}
}

/* ----- 02: Kenya's ground under the course: form lines traced from the relief, crisp at every width ----- */
/* no shade and no slab: the chapter is the same sky as its neighbours, and the ground is seen only in a soft oval
   round the course drawing (eased to nothing well before the heading and the readouts) */
.wr-ground{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none;@@M_GROUND@@}
.wr-topo{position:absolute;left:-7%;top:-4%;width:114%;height:108%;display:none;opacity:.14;}
:root:not(.wr-js) .wr-topo,.wr-ground.is-near .wr-topo{display:block;background:url(@@IMG@@ground.svg) 50% 50%/cover no-repeat;}
.wr-pin .wr-topo{will-change:transform;}

@media print{
  .wr-sky,.wr-ground,.wr-night{display:none!important;}
  .wr-pin .wr-course{height:auto!important;}
  .wr .wr-stage{position:static!important;height:auto!important;}
  .wr-bar,.wr-cue{display:none!important;}
}
""".replace("__GRAIN2__", GRAIN2).replace("__GRAIN__", GRAIN).replace("@@IMG@@", REC_IMG)
for _i, _v in enumerate(STILL):
    CSS = CSS.replace("@@S%d@@" % _i, "%g" % _v)
# the long, eased masks and shades (smoothstep, sampled finely: no knee where a photograph or a shade meets the sky)
for _k, _v in {
        "M_PLATE": mask(ease_stops(0, 56, 0, 1, 12), ease_stops(64, 98, 1, 0, 10)),
        "M_PLATE_P": mask(ease_stops(0, 50, 0, 1, 12), ease_stops(60, 96, 1, 0, 10)),
        "M_PLATE_W": mask2(",".join((ease_stops(0, 56, 0, 1, 12), ease_stops(64, 98, 1, 0, 10))),
                           ",".join((ease_stops(0, 12, 0, 1, 8), ease_stops(88, 100, 1, 0, 8)))),
        "PAR_GRADE": ease_stops(0, 58, .9, 0, 10, "var(--wr-plate-sky,color-mix(in srgb,var(--bg) 50%,var(--sky-cool)))"),
        "M_HERO": mask(ease_stops(50, 100, 1, 0, 10)),
        "M_HERO_P": mask(ease_stops(44, 100, 1, 0, 10)),
        "HERO_SHADE": ",".join((ease_stops(36, 70, 0, .5, 6), ease_stops(70, 100, .5, 0, 6))),
        "HERO_SHADE_P": ",".join((ease_stops(30, 66, 0, .45, 6), ease_stops(66, 100, .45, 0, 6))),
        "M_HERO_GRAIN": mask(ease_stops(50, 100, 1, 0, 6)),
        "M_COURSE_GRAIN": mask(ease_stops(0, 16, 0, 1, 6), ease_stops(84, 100, 1, 0, 6)),
        "PORTRAIT_GRADE": ease_stops(0, 62, .42, 0, 8),
        "M_NIGHT": mask(ease_stops(0, 60, 0, 1, 8)),
        "FOOT_SKY": ease_stops(0, 100, 0, 1, 12),
        "FOOT_STILL": ",".join("color-mix(in srgb,var(--bg) %g%%,var(--wr-s8)) %g%%" % (round(100 * t * t * (3 - 2 * t), 1), round(100 * t, 2))
                               for t in (i / 12.0 for i in range(13))),
        "M_GROUND": rmask("64% 32% at 50% 57%", ease_stops(0, 100, 1, 0, 10)),
}.items():
    CSS = CSS.replace("@@%s@@" % _k, _v)


def hero():
    best = '<span class="wr-v">36<small>km/h</small></span>'
    mark = '<span class="wr-v">35.94<small>km/h</small></span>'
    return """
<header class="wr-hero wr-grain" id="wr-goal">
  """ + pic("hero", "wr-hero-pic", lazy=False, fetch=True) + """
  <div class="wr-in wr-hero-in">
    <div>
      <p class="wr-kick"><span>World Record Attempt</span> <span class="wr-sep" aria-hidden="true">&middot;</span> <span>Kerio Valley, Kenya</span></p>
      <h1 class="wr-mega wr-k"><span class="wr-ln"><span style="--i:0">The Speed</span></span> <span class="wr-ln"><span style="--i:1">Record</span></span> <span class="wr-ln"><span style="--i:2">Attempt</span></span></h1>
      <p class="wr-hero-sub wr-fade">Two world records for speed: 100 km and 200 km, out and return.</p>
      <a class="wr-go wr-fade" href="#wr-partner">Partner on the attempt """ + DOWN + """</a>
    </div>
    <dl class="wr-hero-meta wr-fade">
      <div><dt>To beat, 100 km</dt><dd>""" + mark + """</dd><dd class="wr-s">""" + TBC + """</dd></div>
      <div class="is-me"><dt>My best, about</dt><dd>""" + best + """</dd><dd class="wr-s">Over 198.86 km, not a record course</dd></div>
      <div class="is-win"><dt>Window</dt><dd>18 Jan to 12 Feb 2027</dd></div>
    </dl>
  </div>
  <a class="wr-cue" href="#wr-mark" aria-label="Go to the mark to beat"></a>
</header>
"""


def bar():
    lis = "".join('<li><a href="#%s"><span>%s</span><b>%s</b><i aria-hidden="true"></i></a></li>' % (cid, n, name)
                  for cid, n, name in CHAPTERS)
    return ('\n<nav class="wr-bar" aria-label="Chapters"><div class="wr-in wr-bar-in"><ol>' + lis + '</ol>'
            '<a class="wr-btn" href="#wr-partner">Partner</a></div></nav>\n')


def mark():
    return """
<section class="wr-mark" id="wr-mark" aria-labelledby="wr-mark-h">
  <div class="wr-in">
    <p class="wr-no">01</p>
    <h2 class="wr-h2" id="wr-mark-h">""" + kin("The Mark To Beat") + """</h2>
    <div class="wr-duel">
      <div class="wr-big is-theirs">
        <p class="wr-cap">100 km mark, class O-3</p>
        <p class="wr-giga">35.94<small>km/h</small></p>
        <ul class="wr-meta"><li><b>Michel Macquet (FRA)</b></li><li>23 Jan 2025</li><li>Status&nbsp;""" + TBC + """</li><li>""" + ext(FAI_LIST, "FAI records") + """</li></ul>
      </div>
      <div class="wr-big is-mine">
        <p class="wr-cap">My best average, about</p>
        <p class="wr-giga">36<small>km/h</small></p>
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
        + '<path class="wr-flown v100" id="wrF100" d="%s"/>' % lane(100)
        + '<path class="wr-flown v200" id="wrF200" d="%s"/>' % lane(200)
        + "".join(ticks)
        + '<path class="wr-gate" d="M%g 28V172"/>' % X0
        + "</svg>"
    )




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
        <div><p class="wr-no">02</p><h2 class="wr-h2" id="wr-course-h">""" + kin("Out And Back, To Scale") + """</h2></div>
        <fieldset class="wr-seg"><legend>Course length</legend>
          <input type="radio" name="wrk" id="wrk100" value="100" checked><label for="wrk100">100 km</label>
          <input type="radio" name="wrk" id="wrk200" value="200"><label for="wrk200">200 km</label>
        </fieldset>
      </div>
      <div class="wr-map">
        <div class="wr-box">
          """ + course_svg() + """
          <span class="wr-pl" style="left:0">Start, finish</span>
          """ + tp(100, "v100") + tp(200, "v200") + """
          <span class="wr-gl" id="wrGl" aria-hidden="true"></span>
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
    <p class="wr-lede">The base of my <a class="wr-u" href="destinations/kenya.html">Kenya expeditions</a>, and the site where the world speed records are chased.</p>
  </div>
  <figure class="wr-plate">
    <div class="wr-plate-img"><div class="wr-par"><picture><source media="(max-width: 560px)" srcset=\"""" + IMG["kerio_p"][0] + """.webp" type="image/webp"><source srcset=\"""" + IMG["kerio"][0] + """.webp" type="image/webp"><img src=\"""" + IMG["kerio"][0] + """.jpg" width="1152" height="768" alt="Paragliding at Kerio Valley, Kenya" loading="lazy" decoding="async"></picture></div></div>
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
    # 18 Jan to 12 Feb 2027 on a grid of 26 days: Expedition One (18 to 29 Jan) and Expedition Two (1 to 12 Feb) each one
    # continuous bar, the two days between a dashed hairline; the days themselves as ticks over the numbers under it
    cells = ['<i class="is-on" style="grid-column:1/13"></i>', '<i class="is-off" style="grid-column:13/15"></i>',
             '<i class="is-on" style="grid-column:15/27"></i>']
    nums = ["<span>%d</span>" % (18 + i if i < 14 else i - 13) for i in range(26)]
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
        <h2 class="wr-h2" id="wr-win-h"><span class="wr-nw">18 Jan</span> To <span class="wr-nw">12 Feb</span> 2027</h2>
        <p class="wr-lede">Alongside my two Kenya expeditions.</p>
      </div>""" + days() + """
      <div class="wr-vp">
        <div class="wr-track">
          <ol class="wr-steps">
            <li class="wr-step"><span class="wr-when">Before</span><h3>Preparation</h3><p>Wing, instruments, team, FAI observer """ + TBD + """</p></li>
            <li class="wr-step"><span class="wr-when">Before</span><h3>Build-Up Episodes</h3><p>And the newsletter</p></li>
          </ol>
          <ol class="wr-steps" start="3">
            <li class="wr-step"><span class="wr-when">After</span><h3>The Claim</h3><p><a class="wr-u" href=\"""" + FAI_CODE + """\" target="_blank" rel="noopener">FAI Sporting Code, Section 7D</a></p></li>
            <li class="wr-step"><span class="wr-when">After</span><h3>The Film</h3><p>A debrief episode and the flight data</p></li>
          </ol>
        </div>
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
      <h2 class="wr-h2" id="wr-aud-h">""" + kin("Who Flies It With You") + """</h2>
      <p class="wr-lede">Podcast, YouTube and a newsletter about four times a month.</p>
    </div>
    <figure class="wr-portrait">""" + pic("aninder") + """<figcaption>Aninder Singh</figcaption></figure>
    <dl class="wr-stats">
      <div><dt>Podcast streams</dt><dd>100,000+</dd></div>
      <div><dt>Countries reached</dt><dd>130+</dd></div>
      <div><dt>Long-form interviews</dt><dd>80</dd></div>
      <div><dt>Years flying</dt><dd>10+</dd></div>
    </dl>
  </div>
</section>
"""


def offer():
    return """
<section class="wr-offer" id="wr-partner" aria-labelledby="wr-offer-h">
  """ + night_static() + """
  <div class="wr-in">
    <div class="wr-offer-head">
      <div>
        <p class="wr-no">06</p>
        <h2 class="wr-h2" id="wr-offer-h">""" + kin("Put Your Name On The Attempt") + """</h2>
        <p class="wr-lede">Prices in the media kit, on request. Every sponsorship is <a class="wr-u" href="safety-and-disclosure.html">clearly marked as sponsored</a>.</p>
      </div>
      <figure class="wr-offer-pic">""" + pic("icare") + """</figure>
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
      <a class="btn-solid" href=\"""" + MAIL + """\"><span>Partner on the attempt</span></a>
      <a class="btn-lines" href="partners.html#pwForm">Other ways to work together</a>
    </div>
    <p class="wr-src">Sources: <a class="wr-u" href=\"""" + UP_NEWS + """\" target="_blank" rel="noopener">UP Paragliders</a>, <a class="wr-u" href=\"""" + FAI_LIST + """\" target="_blank" rel="noopener">FAI records</a>, <a class="wr-u" href=\"""" + FAI_CODE + """\" target="_blank" rel="noopener">Sporting Code 7D</a>, <a class="wr-u" href="destinations/kenya.html">the Kenya expedition</a></p>
  </div>
</section>
"""


# The script that runs before the first paint: the page's modes, and one guard. The site's shell
# (v2-immersive.js) still writes --v2-gust on the root at every scroll frame for an instrument that v4 no longer
# has; nothing reads it, but each write restyles the whole page and repaints every layer drawn from a token
# (measured: 2.5 s of raster in ten wheel notches, against 0.17 s without it). On this page that one write is
# dropped (every other property passes through); the real fix belongs in the shell.
EARLY = ('<script>(function(r,m){r.classList.add("wr-js");if(!m("(prefers-reduced-motion: reduce)").matches)'
         'r.classList.add("wr-pin","wr-sky-on");'
         'var s=r.style,o=s.setProperty;s.setProperty=function(k){if(k!=="--v2-gust")return o.apply(s,arguments);};'
         '})(document.documentElement,function(q){return window.matchMedia(q);});</script>')


def main_html():
    return ('<main id="v4-main" class="wr">\n' + EARLY + defs() + sky_html() + hero() + bar() + mark() + course()
            + place() + window() + audience() + offer() + "\n</main>")


SCRIPT = r"""<script>
/* The speed record attempt (tools/v4_record.py). Every frame here is caused
   by a scroll, a tap or a key, and stops when they do: what the scroll moves
   (the position on its course, the ground under it, the day behind the page)
   eases toward where the scroll has put it, in one loop that stops as soon as
   it has arrived. Reduced motion: the finished state, nothing pinned. Without
   this script the page is complete and the course switch still works. */
(function () {
  var d = document, w = window, root = d.documentElement;
  var main = d.getElementById("v4-main");
  if (!main || !main.classList.contains("wr")) return;
  var mq = function (q) { return w.matchMedia(q); };
  var still = mq("(prefers-reduced-motion: reduce)").matches;
  var IO = "IntersectionObserver" in w;
  var REC = @@REC@@, BEST = @@BEST@@, TBD = '<span class="wr-tbd">[to supply]</span>';
  var X0 = @@X0@@, PX = @@PX@@, YO = @@YO@@, YB = @@YB@@, RX = @@RX@@, RY = @@RY@@, CY = @@CY@@;
  var ARRIVE = ".wr-k,.wr-fade,.wr-days";
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function absTop(el) { return el.getBoundingClientRect().top + w.scrollY; }
  function clock(h) { var m = Math.round(h * 60), mm = m % 60; return "<b>" + Math.floor(m / 60) + "</b><small>h</small> <b>" + (mm < 10 ? "0" : "") + mm + "</b><small>min</small>"; }
  function all(s, r) { return [].slice.call((r || d).querySelectorAll(s)); }
  function showAll() { all(ARRIVE).forEach(function (el) { el.classList.add("is-in"); }); }

  try {
  /* 1. two entrances only: the opening's title rises (with its lines after it), once the display face has
     loaded so the swap never lands mid-rise; and the window's days draw across, as time passing, once they are
     well in view. Every other heading, line and photograph simply stands */
  var hero = d.getElementById("wr-goal");
  if (still || !IO) showAll();
  else {
    var first = hero ? all(ARRIVE, hero) : [];
    var ro = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { ro.unobserve(e.target); e.target.classList.add("is-in"); } });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0 });
    all(ARRIVE).forEach(function (el) { if (first.indexOf(el) < 0) ro.observe(el); });
    var open = function () { first.forEach(function (el) { el.classList.add("is-in"); }); };
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(open, open); else open();
  }

  /* 2. the course: 100 or 200 km on one scale, a hairpin flown by the scroll */
  var C = d.getElementById("wr-course"), Cst = C.querySelector(".wr-stage"), map = C.querySelector(".wr-map");
  var box = C.querySelector(".wr-box svg"), gl = d.getElementById("wrGl"), topo = C.querySelector(".wr-topo");
  var kmEl = d.getElementById("wrKm"), legEl = d.getElementById("wrLeg");
  var t1 = d.getElementById("wrT1"), t2 = d.getElementById("wrT2");
  var paths = { 100: d.getElementById("wrF100"), 200: d.getElementById("wrF200") };
  var r200 = d.getElementById("wrk200");
  var K = r200 && r200.checked ? 200 : 100, F = 1, lastKm = -1, lastT = "", lastLeg = "";
  var geo = { mapW: 1, mapH: 1, vh: w.innerHeight, tops: [], ends: [], clipH: 1 };
  function X(km) { return X0 + km * PX; }
  function render(f) {
    F = f;
    var sx = geo.mapW / 1000, sy = geo.mapH / 200, xs = X(0), xa = X(K / 2) - RX;
    /* the turn takes its true share of the line on screen, so the position keeps one speed all the way round */
    var a = RX * sx, b = RY * sy, arc = Math.PI / 2 * (3 * (a + b) - Math.sqrt((3 * a + b) * (a + 3 * b))), run = Math.max(1, (xa - xs) * sx);
    var ts = arc / (2 * run + arc), half = (1 - ts) / 2, x, y, km, dd, leg;
    if (f <= half) {
      var u = f / half; x = xs + (xa - xs) * u; y = YO; km = K / 2 * u; leg = "Out";
      dd = "M" + xs + " " + YO + "H" + x.toFixed(1);
    } else if (f <= half + ts) {
      var v = (f - half) / ts, th = -Math.PI / 2 + v * Math.PI;
      x = xa + RX * Math.cos(th); y = CY + RY * Math.sin(th); km = K / 2; leg = "Turnpoint";
      dd = "M" + xs + " " + YO + "H" + xa + "A" + RX + " " + RY + " 0 0 1 " + x.toFixed(1) + " " + y.toFixed(1);
    } else {
      var u2 = f >= 1 ? 1 : Math.min(1, (f - half - ts) / half); x = xa - (xa - xs) * u2; y = YB; km = K / 2 + K / 2 * u2;
      leg = u2 >= 1 ? "Finish" : "Home";
      dd = "M" + xs + " " + YO + "H" + xa + "A" + RX + " " + RY + " 0 0 1 " + xa + " " + YB + "H" + x.toFixed(1);
    }
    paths[K].setAttribute("d", dd);
    gl.style.transform = "translate(" + (x * sx).toFixed(1) + "px," + (y * sy).toFixed(1) + "px)";
    /* the ground slides under the position out and back, on the same eased progress, so the two move as one */
    if (topo && geo.pin) topo.style.transform = "translate3d(" + (-5 * Math.sin(Math.PI * f)).toFixed(2) + "%,0,0)";
    /* the distance flown, in whole kilometres actually flown (the full course shows only at the finish), and
       both clocks read from that same figure, so they always agree with it */
    var k = Math.floor(km + 1e-6);
    if (k !== lastKm) { lastKm = k; kmEl.textContent = k; }
    if (leg !== lastLeg) { lastLeg = leg; legEl.textContent = leg; }
    var tk = K + "|" + k;
    if (tk !== lastT) { lastT = tk; t1.innerHTML = clock(k / BEST); t2.innerHTML = K === 100 ? clock(k / REC) : TBD; }
  }
  function setK(k) {
    K = k; lastKm = -1; lastT = ""; lastLeg = "";
    /* the other course is shown whole, so a change of mind finds it drawn */
    var o = k === 100 ? 200 : 100, xo = X(o / 2) - RX;
    paths[o].setAttribute("d", "M" + X(0) + " " + YO + "H" + xo + "A" + RX + " " + RY + " 0 0 1 " + xo + " " + YB + "H" + X(0));
    render(F);
  }
  all('input[name="wrk"]').forEach(function (r) { r.addEventListener("change", function () { if (r.checked) setK(+r.value); }); });
  map.classList.add("is-live");

  /* 3. the site menu: when it first leaves the page's flow to wait above the screen, it goes there at once
     rather than sliding away across the chapter bar (so there is never a moment with two bars) */
  var Wn = d.getElementById("wr-window"), siteNav = d.querySelector(".page-wrap > nav");
  if (siteNav && "MutationObserver" in w) {
    var wasPinned = siteNav.classList.contains("v2-nav-pinned");
    new MutationObserver(function () {
      var p = siteNav.classList.contains("v2-nav-pinned");
      if (p && !wasPinned && !siteNav.classList.contains("v2-nav-shown")) {
        siteNav.style.transition = "none"; void siteNav.offsetWidth;
        requestAnimationFrame(function () { requestAnimationFrame(function () { siteNav.style.transition = ""; }); });
      }
      wasPinned = p;
    }).observe(siteNav, { attributes: true, attributeFilter: ["class"] });
  }

  /* 4. the chapter bar: the chapter being read, a reading line under each; over the offer, the Partner button.
     On a phone the bar shows the chapters' numbers, with the name of the one being read beside them */
  var barEl = d.querySelector(".wr-bar"), barOl = barEl && barEl.querySelector("ol"), barBtn = barEl && barEl.querySelector(".wr-btn");
  var barIn = barEl && barEl.querySelector(".wr-bar-in");
  var links = barEl ? all("ol a", barEl) : [], lines = links.map(function (a) { return a.querySelector("i"); });
  var chaps = links.map(function (a) { return d.getElementById(a.getAttribute("href").slice(1)); });
  var lastP = links.map(function () { return -1; });
  var foot = d.querySelector("footer"), partner = d.getElementById("wr-partner"), cur = -2;
  function bars(y, vh) {
    if (!barEl) return;
    var line = y + vh * 0.4, i = -1;
    for (var n = 0; n < geo.tops.length; n++) {
      if (geo.tops[n] <= line && line < geo.ends[n]) i = n;
      var p = clamp((line - geo.tops[n]) / Math.max(1, geo.ends[n] - geo.tops[n]));
      if (Math.abs(p - lastP[n]) > 0.002) { lastP[n] = p; lines[n].style.setProperty("--p", p.toFixed(3)); }
    }
    if (i < 0 && line >= geo.partner) i = links.length;
    if (i !== cur) {
      cur = i;
      links.forEach(function (a, k) { if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      if (barBtn) { if (i === links.length) barBtn.setAttribute("aria-current", "true"); else barBtn.removeAttribute("aria-current"); }
      if (barIn) barIn.setAttribute("data-cur", i >= 0 && i < links.length ? links[i].querySelector("b").textContent : "");
      if (i >= 0 && i < links.length && barOl && barOl.scrollWidth > barOl.clientWidth) {
        var li = links[i].parentNode;
        barOl.scrollTo({ left: Math.max(0, li.offsetLeft - barOl.clientWidth * 0.3), behavior: still ? "auto" : "smooth" });
      }
    }
    barEl.classList.toggle("is-on", y > geo.heroEnd - vh * 0.55 && y + vh < geo.foot + 2);
  }

  /* 5. the record day behind the page: from first light to night as the visitor scrolls, told by light alone.
     Two canvases, fixed behind everything: the sky, painted small from the design tokens in linear light and
     never past a set brightness (so the words keep their contrast), stretched by the browser; and over it the
     real stars and Milky Way of a night in the window, drawn a little larger than the screen and only every
     few degrees of their turn: between those, the browser's compositor turns and fades the drawing (no
     repaint while the page scrolls) */
  var skyEl = root.classList.contains("wr-sky-on") ? d.querySelector(".wr-sky") : null;
  var dayEls = [hero, d.getElementById("wr-mark"), C, d.getElementById("wr-kerio"), Wn, d.getElementById("wr-audience"), partner, foot];
  var SKY = null;
  /* a sky that cannot be painted leaves the still day in its place, and every other effect running */
  if (skyEl) { try { SKY = daySky(skyEl); } catch (e) { SKY = null; root.classList.remove("wr-sky-on"); } }
  function daySky(el) {
    var sk = el.querySelector(".wr-sky-c"), sg = sk.getContext("2d", { alpha: false }), cv = el.querySelector(".wr-sky-o"), g = cv.getContext("2d");
    if (!g || !sg) throw new Error("no sky");
    var IMGS = "@@IMG@@";
    var CAP = @@CAP@@, KNEE = CAP * 0.7, YH = 0.86, SUNR = 1.519, T = {}, P = [], img = null, Cc = {}, Cs = {};
    var Wd = 1, Hd = 1, dpr = 0, W2 = 1, H2 = 1, cw = 1, ch = 1, kx = 1, ky = 1, lastQ = -1;
    /* the star drawing: which sky it holds, the turn it was drawn at, its margin past the screen, and what the
       compositor was last told (turn, opacity); MAXR is how far it may be turned before it is drawn again */
    var ov = { set: "", base: 0, m: 0, tf: "", op: "", dirty: true }, MAXR = 2.5 * Math.PI / 180, plate = { c: "" };
    var ENC = new Uint8ClampedArray(4096), HX = [], VX = [];
    var i;
    for (i = 0; i < 4096; i++) { var e = i / 4095; ENC[i] = Math.round(e <= 0.0031308 ? 3294.6 * e : 269.025 * Math.pow(e, 1 / 2.4) - 14.025); }
    function lin(v) { v = v < 0 ? 0 : v > 255 ? 1 : v / 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    function sm(t) { return t * t * (3 - 2 * t); }
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
      Cc = { sw: T.white, sy: mx("var(--white)", 80, "var(--orange)"), sr: mx("var(--white)", 58, "var(--orange)"), mw: mx("var(--white)", 82, "var(--sky-cool)") };
      Cs = { tw: css(Cc.sw, 1), tb: css(Cc.sw, 1), ty: css(Cc.sy, 1), tr: css(Cc.sr, 1) };
      build();
      ["mwd", "mwn"].forEach(function (k) { if (CL[k].img && CL[k].img.complete) CL[k].tint = tint(CL[k]); });
      ov.dirty = true;
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
       Valley, 4 the window, 5 the audience, 6 the offer, 7 the footer) the clock; the sky from the top of the
       screen to its bottom edge, which is the horizon (z, mi, h, in linear light at a set luminance, never darker
       lower down, so no stripe can form); the light the low sun puts on the horizon, rising from the bottom edge
       under the sun (hc ha, hh tall, hw wide); the deep sides of midday (vg); the stars before dawn (sa) and at
       night (sb). Overhead the sky stays in one cool family all day; the warmth of dawn and dusk lives only at
       the horizon */
    function build() {
      function unit(c) { var l = [lin(c[0]), lin(c[1]), lin(c[2])], L = 0.2126 * l[0] + 0.7152 * l[1] + 0.0722 * l[2]; return [l[0] / L, l[1] / L, l[2] / L]; }
      /* the horizon's lights: first light pale and cool; the afternoon's amber and dusk's ember leaning to rose
         (some of the sky's blue in them) and kept saturated, so that held under the brightness limit they read
         as light, not as brown */
      var first = unit(m("white", .62, "sky-cool", .28, "orange", .1)), amber = unit(m("orange", .62, "white", .2, "sky-cool", .18)),
        ember = unit(m("orange", .76, "sky-cool", .24));
      function blue(L) { return tone(L, "sky-cool", .92, "white", .08); }
      function deep(L) { return tone(L, "sky-cool", 1.3, "white", -.3); }
      function S(dd, hr, z, mi, h, o) {
        var s = { d: dd, hr: hr, z: z, mi: mi, h: h, hc: first, ha: 0, hh: .14, hw: .42, vg: 0, sa: 0, sb: 0 };
        for (var k in o) s[k] = o[k];
        return s;
      }
      var n0 = blue(.0055), n1 = tone(.0072, "sky-cool", .9, "white", .1), n2 = tone(.0092, "sky-cool", .84, "white", .14, "orange", .02);
      P = [
        S(0, 5.2, n0, n1, n2, { sa: .25 }),
        S(.45, 5.85, blue(.006), tone(.008, "sky-cool", .9, "white", .1), tone(.0115, "sky-cool", .78, "white", .2, "orange", .02), { sa: .4, ha: .15, hh: .12 }),
        S(.75, 6.45, blue(.0072), tone(.0098, "sky-cool", .86, "white", .14), tone(.0145, "sky-cool", .7, "white", .27, "orange", .03), { sa: .75, ha: .5, hh: .12, hw: .38 }),
        S(1.05, 6.87, blue(.0085), tone(.0115, "sky-cool", .82, "white", .18), tone(.0175, "sky-cool", .64, "white", .33, "orange", .03), { sa: .2, ha: .85, hh: .13, hw: .36 }),
        S(1.45, 7.6, blue(.0098), tone(.0135, "sky-cool", .78, "white", .22), tone(.0205, "sky-cool", .6, "white", .37, "orange", .03), { ha: .5, hh: .15, hw: .4 }),
        S(1.75, 8.2, deep(.0108), tone(.0148, "sky-cool", .82, "white", .18), tone(.0225, "sky-cool", .58, "white", .4, "orange", .02), { ha: .18, hh: .17, hw: .44 }),
        S(2.2, 9.2, deep(.0108), deep(.0145), tone(.0235, "sky-cool", .64, "white", .36), { vg: .35 }),
        S(2.7, 10.6, deep(.0105), deep(.0145), tone(.0245, "sky-cool", .62, "white", .38), { vg: .6 }),
        S(3.2, 12.1, deep(.0102), deep(.0145), tone(.025, "sky-cool", .6, "white", .4), { vg: .7 }),
        S(3.7, 13.3, deep(.0102), deep(.0145), tone(.025, "sky-cool", .6, "white", .39, "orange", .01), { vg: .7 }),
        S(4.2, 14.5, deep(.0105), tone(.014, "sky-cool", 1.1, "white", -.1), tone(.023, "sky-cool", .6, "white", .36, "orange", .04), { vg: .55 }),
        S(4.65, 15.6, tone(.0105, "sky-cool", .98, "orange", .02), tone(.0135, "sky-cool", .9, "white", .08, "orange", .02), tone(.0185, "sky-cool", .72, "white", .22, "orange", .06), { vg: .35, hc: amber, ha: .25, hh: .14, hw: .42 }),
        S(5.15, 16.8, tone(.0098, "sky-cool", .97, "orange", .03), tone(.0125, "sky-cool", .93, "orange", .05, "white", .02), tone(.0145, "sky-cool", .84, "orange", .1, "white", .06), { vg: .15, hc: amber, ha: .55, hh: .15, hw: .44 }),
        S(5.55, 17.9, tone(.009, "sky-cool", .95, "orange", .05), tone(.0112, "sky-cool", .92, "orange", .08), tone(.0122, "sky-cool", .86, "orange", .14), { hc: ember, ha: .85, hh: .16, hw: .46 }),
        S(5.8, 18.55, tone(.0085, "sky-cool", .95, "orange", .05), tone(.0105, "sky-cool", .92, "orange", .08), tone(.0115, "sky-cool", .86, "orange", .14), { hc: ember, ha: .95, hh: .15, hw: .46 }),
        S(6.1, 18.95, blue(.0072), tone(.0092, "sky-cool", .93, "orange", .07), tone(.0105, "sky-cool", .86, "orange", .14), { hc: ember, ha: .55, hh: .13, hw: .48, sb: .35 }),
        S(6.45, 19.3, n0, tone(.0082, "sky-cool", .94, "orange", .04), tone(.0098, "sky-cool", .86, "white", .08, "orange", .06), { hc: ember, ha: .22, hh: .12, hw: .5, sb: .85 }),
        S(6.8, 19.6, n0, n1, n2, { hc: ember, ha: .07, hh: .12, hw: .5, sb: 1 }),
        S(8, 20.4, n0, n1, n2, { hc: ember, hh: .12, hw: .5, sb: 1 })
      ];
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
    /* sizes are taken from the sky box (100lvh), so a phone's toolbar sliding in or out changes nothing here */
    function size() {
      var W = Math.max(1, el.clientWidth), H = Math.max(1, el.clientHeight), r = Math.min(w.devicePixelRatio || 1, 2);
      if (W === Wd && H === Hd && r === dpr) return;
      Wd = W; Hd = H; dpr = r;
      cw = Wd < 600 ? 56 : Wd < 1100 ? 80 : 104; ch = Math.max(8, Math.round(cw * Hd / Wd));
      sk.width = cw; sk.height = ch; img = sg.createImageData(cw, ch);
      ky = YH * Hd / 2.1; kx = Math.min(ky, (Wd / 2 - 14) / 1.6);
      /* the star drawing reaches past the screen by as much as a turn of MAXR moves its farthest corner */
      ov.m = Math.ceil(Math.sqrt(Wd * Wd / 4 + YH * Hd * YH * Hd) * Math.sin(MAXR + 0.003)) + 4;
      W2 = Math.round((Wd + 2 * ov.m) * dpr); H2 = Math.round((Hd + 2 * ov.m) * dpr);
      cv.width = W2; cv.height = H2;
      cv.style.left = cv.style.top = -ov.m + "px";
      cv.style.width = Wd + 2 * ov.m + "px"; cv.style.height = Hd + 2 * ov.m + "px";
      cv.style.transformOrigin = (ov.m + Wd / 2) + "px " + (ov.m + YH * Hd) + "px";
      lastQ = -1; ov.dirty = true; plate.c = "";
    }
    /* the Milky Ways: greyscale masks, each fetched only as its hour comes near, then given its colour from the tokens */
    var CL = { mwd: { f: "mw-dawn", c: "mw", a: 0.09 }, mwn: { f: "mw-night", c: "mw", a: 0.09 } };
    function want(k) {
      var c = CL[k];
      if (c.img) return c.tint;
      c.img = new Image(); c.img.decoding = "async";
      c.img.onload = function () { c.tint = tint(c); ov.dirty = true; if (SKY) onScroll(); };
      c.img.src = IMGS + c.f + ".webp";
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
    /* every pixel of the sky, in linear light: the gradient (eased between its three heights, so it has no
       knee, and never darker lower down), the deep sides, the light on the horizon (the bottom edge) under the
       sun, falling off upward only; then held under CAP (a soft knee) and encoded */
    function paint(s, sx) {
      var px = img.data, syh = Hd / ch, hx = s.hw * Wd, hy = s.hh * Hd;
      var hc = s.hc, n = 0, x, u;
      var z = s.z, mi = s.mi, h = s.h;
      for (x = 0; x < cw; x++) {
        u = (x + 0.5) / cw; var dx = (u * Wd - sx) / hx;
        HX[x] = Math.exp(-dx * dx);
        VX[x] = 1 - s.vg * (Wd < 600 ? 0.2 : 0.45) * (2 * u - 1) * (2 * u - 1);
      }
      for (var y = 0; y < ch; y++) {
        var py = (y + 0.5) * syh, t = py / Hd;
        var base = t < 0.5 ? mix(z, mi, sm(t / 0.5)) : mix(mi, h, sm((t - 0.5) / 0.5));
        var hv = (Hd - py) / hy, hrow = s.ha * 0.026 * Math.exp(-hv * hv);
        for (x = 0; x < cw; x++, n += 4) {
          var v = VX[x], h2 = hrow * HX[x];
          var r = base[0] * v + hc[0] * h2, gg = base[1] * v + hc[1] * h2, b = base[2] * v + hc[2] * h2;
          var L = 0.2126 * r + 0.7152 * gg + 0.0722 * b;
          if (L > KNEE) { var f = (KNEE + (CAP - KNEE) * (1 - Math.exp(-(L - KNEE) / (CAP - KNEE)))) / L; r *= f; gg *= f; b *= f; }
          px[n] = ENC[r > 1 ? 4095 : (r * 4095) | 0]; px[n + 1] = ENC[gg > 1 ? 4095 : (gg * 4095) | 0]; px[n + 2] = ENC[b > 1 ? 4095 : (b * 4095) | 0]; px[n + 3] = 255;
        }
      }
      sg.putImageData(img, 0, 0);
    }
    /* the sun that day: hour angle from solar noon; looking south it comes up on the left and goes down on the
       right; only the light it puts on the horizon under it is drawn */
    function sunX(hr) { return Wd / 2 + SUNR * Math.sin((hr - @@NOON@@) * 15 * Math.PI / 180) * kx; }
    /* the real sky, drawn turned by rot about the south pole, which sits on the horizon below the screen's
       middle (the drawing's margin past the screen keeps every corner covered while the compositor turns it) */
    function draw(list, mw, rot) {
      var cx = (ov.m + Wd / 2) * dpr, cy = (ov.m + YH * Hd) * dpr, u = ky * dpr, c = Math.cos(rot), s = Math.sin(rot), j;
      g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.clearRect(0, 0, W2, H2);
      if (mw) { g.save(); g.translate(cx, cy); g.rotate(rot); g.drawImage(mw, -3 * u, -2.25 * u, 6 * u, 3 * u); g.restore(); }
      for (var k = 0; k < list.length; k++) {
        var q = list[k], r = Math.max(0.35, SZ[q.z] / 2000 * u), p = q.p;
        g.globalAlpha = SO[q.z]; g.fillStyle = Cs[q.t] || Cs.tw; g.beginPath();
        for (j = 0; j < p.length; j += 2) {
          var X = cx + (p[j] * c - p[j + 1] * s) * u, Y = cy + (p[j] * s + p[j + 1] * c) * u;
          if (X < -3 || X > W2 + 3 || Y < -3 || Y > H2 + 3) continue;
          g.moveTo(X + r, Y); g.arc(X, Y, r, 0, 6.2832);
        }
        g.fill();
      }
      g.globalAlpha = 1;
    }
    /* the sky's own colour at a height on the screen (the middle of the row, as painted) */
    function skyAt(py) {
      var row = Math.max(0, Math.min(ch - 1, Math.floor(py / Hd * ch))), p = img.data, x0 = Math.floor(cw * 0.25), x1 = Math.ceil(cw * 0.75), o = [0, 0, 0];
      for (var x = x0; x < x1; x++) { var n = (row * cw + x) * 4; o[0] += p[n]; o[1] += p[n + 1]; o[2] += p[n + 2]; }
      return o.map(function (v) { return Math.round(v / (x1 - x0)); });
    }
    function at(D, y, vh, geo) {
      var q = Math.round(D * 160);
      if (q !== lastQ) { lastQ = q; var sq = state(q / 160); paint(sq, sunX(sq.hr)); plate.c = ""; }
      var s = state(D), set = s.sa > 0.004 ? "d" : s.sb > 0.004 ? "n" : "", a = set === "d" ? s.sa : set === "n" ? s.sb : 0;
      /* the stars: turned and faded by the compositor; drawn again only past MAXR of turn, or when what they
         hold has changed (the other sky, a Milky Way just loaded, new tokens, a new size) */
      if (set) {
        var rot = (s.hr - (set === "d" ? 5.5 : 19)) * 15.04 * Math.PI / 180, mw = set === "d" ? want("mwd") : D > 5 ? want("mwn") : null;
        if (ov.dirty || set !== ov.set || Math.abs(rot - ov.base) > MAXR || !!mw !== !!ov.mw) {
          draw(set === "d" ? STARS.d : STARS.n, mw, rot); ov.set = set; ov.base = rot; ov.mw = mw; ov.dirty = false;
        }
        var tf = "rotate(" + (rot - ov.base).toFixed(5) + "rad)";
        if (tf !== ov.tf) { ov.tf = tf; cv.style.transform = tf; }
      }
      var op = a > 0.004 ? a.toFixed(3) : "0";
      if (op !== ov.op) { ov.op = op; cv.style.opacity = op; }
      /* the Kerio photograph's top is tinted with the very sky behind it, so it meets no band */
      if (geo.plateEl) {
        var py = geo.plateTop - y;
        if (py > -Hd && py < Hd * 1.2) {
          var c = skyAt(Math.max(0, Math.min(Hd - 1, py))), cs = "rgb(" + c.join(",") + ")";
          if (cs !== plate.c) { plate.c = cs; geo.plateEl.style.setProperty("--wr-plate-sky", cs); }
        }
      }
    }
    tokens(); size();
    /* the site's sky tokens ease to the visitor's hour over two seconds after the page opens */
    root.addEventListener("transitionend", function (e) { if (e.target === root && e.propertyName === "--sky-cool") { tokens(); lastQ = -1; onScroll(); } });
    return { size: size, at: at };
  }
  function dayAt(line) {
    var t = geo.dT, n = t.length, i = 0;
    if (line <= t[0]) return 0;
    while (i < n - 1 && line >= t[i + 1]) i++;
    var end = i < n - 1 ? t[i + 1] : geo.docH;
    return Math.min(8, i + clamp((line - t[i]) / Math.max(1, end - t[i])));
  }

  /* the ground under the course loads once, as it comes near */
  var nearEls = all(".wr-ground");
  if (IO) {
    var nio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-near"); nio.unobserve(e.target); } }); }, { rootMargin: "60% 0px 60% 0px" });
    nearEls.forEach(function (el) { nio.observe(el); });
  } else nearEls.forEach(function (el) { el.classList.add("is-near"); });

  function measure() {
    var vh = w.innerHeight, r = box.getBoundingClientRect();
    geo.mapW = r.width; geo.mapH = r.height; geo.vh = vh;
    geo.pin = root.classList.contains("wr-pin");
    geo.cStart = absTop(C); geo.cLen = Math.max(1, C.offsetHeight - Cst.offsetHeight);
    geo.tops = chaps.map(function (c) { return c ? absTop(c) : 0; });
    geo.ends = chaps.map(function (c, i) { return i + 1 < chaps.length ? geo.tops[i + 1] : (partner ? absTop(partner) : geo.tops[i] + 1); });
    geo.partner = partner ? absTop(partner) : 1e9;
    geo.foot = foot ? absTop(foot) : 1e9;
    geo.heroEnd = hero ? absTop(hero) + hero.offsetHeight : 0;
    if (SKY) {
      SKY.size(); geo.dT = dayEls.map(function (e) { return e ? absTop(e) : 0; }); geo.docH = root.scrollHeight;
      geo.plateEl = d.querySelector(".wr-par"); geo.plateTop = geo.plateEl ? absTop(geo.plateEl) : 0;
    }
  }

  /* 6. one loop for all that the scroll moves. The position's progress and the day's hour ease toward where the
     scroll has put them (each frame closes a share of the gap, by the time passed: a spring-like lerp), so a
     flick of the wheel becomes a glide with weight that settles; the loop stops once both have arrived (the
     position within half a pixel), and the next scroll starts it again */
  var now = { f: -1, D: -1 }, raf = 0, last = 0;
  function toward(v, to, dt, tau, eps) { return v < 0 || Math.abs(to - v) < eps ? to : v + (to - v) * (1 - Math.exp(-dt / tau)); }
  function frame(t) {
    raf = 0;
    var dt = last ? Math.min(64, Math.max(1, t - last)) : 16; last = t;
    var y = w.scrollY, vh = geo.vh;
    var ft = geo.pin ? clamp((clamp((y - geo.cStart) / geo.cLen) - 0.05) / 0.77) : 1, Dt = SKY ? dayAt(y + vh * 0.5) : 0;
    var f = toward(now.f, ft, dt, 140, 0.0004), D = toward(now.D, Dt, dt, 320, 0.002);
    if (f !== now.f) { now.f = f; render(f); }
    now.D = D;
    bars(y, vh);
    if (SKY) SKY.at(D, y, vh, geo);
    if (f !== ft || D !== Dt) raf = requestAnimationFrame(frame); else last = 0;
  }
  function onScroll() { if (!raf) raf = requestAnimationFrame(frame); }
  /* measure again (a resize, a phone's toolbar, the fonts, the images): the position and the day go on easing from
     where they are toward the new targets; only the first frame starts them in place */
  function refresh(first) {
    measure(); if (first) { now.f = -1; now.D = -1; } else if (now.f >= 0) render(now.f);
    last = 0; if (raf) { cancelAnimationFrame(raf); raf = 0; } frame(performance.now());
  }

  refresh(true);
  w.addEventListener("scroll", onScroll, { passive: true });
  var rz = 0;
  w.addEventListener("resize", function () { cancelAnimationFrame(rz); rz = requestAnimationFrame(function () { refresh(false); }); }, { passive: true });
  w.addEventListener("load", function () { refresh(false); });
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(function () { refresh(false); });
  } catch (err) {
    root.classList.remove("wr-pin", "wr-sky-on");
    showAll();
  }
})();
</script>"""


def script():
    s = SCRIPT
    for k, v in (("REC", REC100), ("BEST", BEST), ("X0", X0), ("PX", PX_PER_KM), ("YO", YO), ("YB", YB),
                 ("RX", RX), ("RY", RY), ("CY", CY), ("CAP", SKY_CAP), ("NOON", SUN_NOON)):
        s = s.replace("@@%s@@" % k, repr(v))
    s = s.replace("@@IMG@@", REC_IMG)
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
