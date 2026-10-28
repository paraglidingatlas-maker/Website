#!/usr/bin/env python3
"""
A trip page, less but better (owner, 19 Oct 2026). The record page's pass
(tools/v4_record.py; docs/v4-design-rules.md, Motion) carried to the trip
pages, one page at a time; India first. The owner called the record page's
first version "a cheap rip-off feeling rather than a premium one"; what fixed
it was one easing curve, motion with weight (an eased glide that settles, never
a loop), no drawn stand-ins for nature, typography and real photographs as the
graphics, and photographs that never meet the page at a hard edge.

What this does to the page, in place (the markup side; the look is
prototypes/v4/src/v4-calm.css and the motion prototypes/v4/src/v4-calm.js,
which this links from the page with their version hashes and which only this
page loads, so Kenya, which shares every trip class, and every other v4 page
carry none of it, and v2.css and v2-immersive.js are as they were):

  - <html class="v4-calm">: the page opts in, and links v4-calm.css and
    v4-calm.js.
  - The hero is one plate: the snowline photograph and the owner's footage.
    The other four photographs, their tabs, the "Scroll" cue and the slideshow
    script go; the four photographs move to the gallery, their tab names as
    their captions. The parallax moves to the one eased loop.
  - The facts row: four big facts (next departure, length, level, price),
    then the old row's other four (base, launch, guiding, season) in a
    quieter row under them; every label and value is the old row's own.
  - The gauge in the Overview fold is drawn finished (3.6 km, the front
    ridge's cloudbase, the site's own figure); its sweep and drift and the
    sign-off's word-by-word lighting leave the Overview script.
  - The fly-through: slides 2 to 5 get the <noscript> twin slide 1 already
    had, so without JavaScript every step shows its photograph. Every
    readout row stays (the cloudbase scene keeps all three of its figures).
  - The route: the real-geography fall now ends on the whole of India with
    Bir Billing's marker clear of the bar (it ended on an empty field), and
    the schematic's drawn hills become two straight lines, their names set
    on them. The lit lines are masked so the eased loop can draw them with
    the scroll. The section is .tm-calm, not .tm, so v2-immersive.js's trip
    map (part 15) leaves it to v4-calm.js. The map's land is cut to the
    widest frame the camera ever shows (nothing on screen changes; a third
    of the map's weight goes) and its finer graticule, never shown, goes.
  - The departures: each tour's dates under its bar, and "Guaranteed to run"
    a status line beside "6 places" (.v2-status.is-go, its green in the dot).
  - The page's own rules for the schematic's ranges and type and for the
    guides, India's alone, take the calmed look in place.
  - The gallery is the owner's pinned fly-through again on a wide screen
    (his choice of 1 Oct, option A; the blind judges of 20 Oct missed it),
    flown by v4-calm.js's one loop, and a column of clean full-width plates
    on a phone, with reduced motion and without the script. Thirteen
    photographs, none shown twice on the page: the four that repeated the
    hero or the fly-through go, the hero's four come in, and Last light
    (the pushed page's closer, its caption and alt as they were there);
    it opens on the back ranges from the air and closes on Last light.
    Each figure carries its place in the run (01 / 13) in its own caption,
    and the point its crop keeps (--fx, --fy); one markup serves every
    screen (a track, a pin, the figures, the progress marks). The section
    is .v4c-g, not .gxa, so v2-immersive.js's pinned gallery (part 14)
    finds nothing to run.
  - The phone's booking bar also steps aside while the departures' cards
    (which carry their own Hold a place) are on screen, and leaves for the
    call only once its buttons are in view.
  - Flying Etiquette is a list to read at every width (no sideways pin, no
    page-wide scroll listener). The FAQ's height transition takes the one
    curve. The dead "Routes sheet" script and its styles go.
  - This pass's own small scripts (the booking bar, the fly-through's step
    swap, Flying Etiquette's button) live in v4-calm.js, not inline in the
    page; their marks stay, empty. The fly-through's first words wait for
    their photograph, and the route's schematic comes in on its pool before
    its names (v4-calm.css and v4-calm.js).
  - Weight on arrival (the speed rule: no heavier than before): the parts of
    the usability pass's blocks (tools/v4_ux.py) that have nothing left to
    act on here go (the hero slideshow's waker, the pinned gallery's phone
    rules), and the fly-through's photographs wake from the screen's foot,
    since the fly-through now begins behind the Overview heading. Last,
    the page is written compactly (compact(): no indentation at the start
    of a line, inline scripts as tools/v4_min.py writes the served ones,
    the JSON-LD without its pretty-printing, the inline styles' notes out
    but this tool's v4c marks), which pays for the gallery's run: nothing
    on screen changes.

Every change sits between <!--v4c:NAME--> and <!--/v4c:NAME--> marks, or is
an exact replace that first checks for its applied form, and every match is
asserted, so a changed upstream page fails loudly instead of half patching.
Running it twice leaves the page byte-identical. Nothing is invented: every
word, number, place and photograph is one the page or the site already has.

Run it last in the trip chain, after tools/v4_trip.py, v4_flythrough.py,
v4_tripmap.py, v4_award.py, v4_footage.py, v4_phone_media.py, v4_pass.py and
v4_ux.py (tools/v4_build.py runs v4_ux on the trips, so it needs this right
after), then write the served CSS and script:

    python3 tools/v4_trip_calm.py india
    python3 tools/v4_min.py

It takes the trip's name and accepts only india this round (Kenya can join
by adding its name and its own data). The version hash on each link is that
of the copy tools/v4_min.py writes from the source (the hash
tools/version_assets.py would give it), so the order above leaves it right.
It never touches prototypes/v2/, the live pages or root files
(destinations.css, styles.css, script.js, rss-feed.js), Kenya, the other v4
tools, src/v2.css, src/v2-immersive.js or src/v4-ux.css.
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_min  # noqa: E402  (the minifier, for the served copies' version hashes)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
TRIPS = {"india": "destinations/india.html"}
A = "../../../assets/destinations/india/"


def fail(msg):
    raise SystemExit("v4_trip_calm: " + msg + " (the page has changed upstream; check it before patching)")


def marked(src, name, new, find):
    """Put `new` between <!--v4c:NAME--> marks: in place of what the marks hold when the page already has
    them (so a second run writes the same bytes), or the first time in place of `find`, a pattern that must
    match exactly once."""
    a, b = "<!--v4c:%s-->" % name, "<!--/v4c:%s-->" % name
    if src.count(a) == 1 and src.count(b) == 1:
        i, j = src.index(a), src.index(b) + len(b)
        return src[:i] + a + new + b + src[j:]
    if a in src or b in src:
        fail("the marks for %s are not a pair" % name)
    ms = list(re.finditer(find, src, re.S))
    if len(ms) != 1:
        fail("%s: expected one match, found %d" % (name, len(ms)))
    return src[:ms[0].start()] + a + new + b + src[ms[0].end():]


def squash(t):
    """Markup as compact() leaves it: no indentation at the start of a line."""
    return re.sub(r"\n[ \t]+", "\n", t)


def compact(src):
    """The page written compactly, for its weight on arrival (the speed rule: no heavier than the pushed page),
    with nothing on screen changed: no indentation at the start of a line of markup or style (a line break is
    still there, so the words wrap and space exactly as before); each inline script as tools/v4_min.py writes
    the served scripts (no comments, no indentation, no empty lines); the structured data (JSON-LD) without its
    pretty-printing; the inline styles without their notes, except this tool's own v4c marks. A second pass
    changes nothing."""
    out = []
    for part in re.split(r"(<script\b[^>]*>.*?</script>)", src, flags=re.S):
        m = re.match(r"(<script\b([^>]*)>)(.*?)(</script>)$", part, re.S)
        if not m:
            part = re.sub(r"(<style[^>]*>)(.*?)(</style>)", lambda t: t.group(1) + re.sub(r"/\*(?! v4c).*?\*/\n?", "", t.group(2), flags=re.S)
                          + t.group(3), part, flags=re.S)
            out.append(squash(part))
            continue
        attrs, body = m.group(2), m.group(3)
        if "src=" in attrs:
            out.append(part)
        elif "ld+json" in attrs:
            out.append(m.group(1) + json.dumps(json.loads(body), ensure_ascii=False, separators=(",", ":")) + m.group(4))
        else:
            out.append(m.group(1) + "\n" + v4_min.js(body) + m.group(4))
    return "".join(out)


def swap(src, name, old, new, n=1):
    """An exact replace that first checks for its applied form (as compact() leaves it)."""
    if src.count(squash(new)) == n and old not in src and squash(old) not in src:
        return src
    if src.count(old) != n:
        fail("%s: expected %d of %r, found %d" % (name, n, old[:60], src.count(old)))
    return src.replace(old, new)


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


# ---------- the facts row: four big facts, then the old row's other four, quieter ----------
# Every label and value is the old row's own (or the booking bar's next departure; India in 2027, tools/v4_india_2027.py); a value's
# small words ("or equivalent", "per pilot") sit beside its big ones, so no label is reworded.
BIG = [("Next departure", "15 Apr 2027", ""), ("Duration", "10 days", ""), ("Pilot rating", "IPPI 2", "or equivalent"),
       ("Price", "£1,100", "per pilot")]
QUIET = [("Base", "Bir, Himachal Pradesh"), ("Launch", "Billing, about 2,400m"), ("Guiding", "1 guide to 3 pilots"),
         ("Season", "April to May, October to November")]


def facts():
    big = "".join('\n    <div><dt>%s</dt><dd><b>%s</b>%s</dd></div>' % (esc(l), esc(v), " <small>%s</small>" % esc(s) if s else "")
                  for l, v, s in BIG)
    quiet = "".join('\n    <div><dt>%s</dt><dd>%s</dd></div>' % (esc(l), esc(v)) for l, v in QUIET)
    return ('<section class="dst-spec v4t-spec">\n  <dl class="v4c-facts">%s\n  </dl>\n  <dl class="v4c-facts is-quiet">%s\n  </dl>\n'
            '</section>' % (big, quiet))


# ---------- the fly-through's slides 2 to 5, each with the <noscript> twin slide 1 has ----------
FLY = [("front-range", "A pilot flying along the forested front range, snow peaks behind"),
       ("last-light-pair", "Two paragliders silhouetted against the sunset"),
       ("ridge-cumulus", "The forested front range under building cumulus"),
       ("sky-of-wings", "Dozens of paragliders thermalling together under grey cloud")]


def fly_slides():
    out = []
    for name, alt in FLY:
        g = A + "gallery/" + name
        out.append('<div class="kfly-slide"><picture><source data-v4-srcset="%s.webp" type="image/webp"><img data-v4-src="%s.jpg" '
                   'width="1400" height="933" loading="lazy" draggable="false" alt="%s"></picture><noscript><picture>'
                   '<source srcset="%s.webp" type="image/webp"><img src="%s.jpg" width="1400" height="933" loading="lazy" '
                   'draggable="false" alt="%s"></picture></noscript></div>' % (g, g, esc(alt), g, g, esc(alt)))
    return "\n      ".join(out)


# ---------- the route: the fall ends on India's outline, Bir Billing at its centre ----------
# India's outline (the map's .tm-hl) spans x 3527 to 4694 and y 180 to 1330 in the map's units; the marker
# is at 3868.8, 318. The fall ends on the country, a little wider than the old country frame and a little
# higher (1897 wide, centred at 4110.2, 720), so India's outline is whole on a wide screen and the marker with
# its name sits clear under the chapter bar and the heading, at 1440 and at 390; the cards then come in on
# the country frame's old width (1458.9) centred on the marker (docs/v4-report.md).
KEYS_OLD = ('data-keys="{&quot;world&quot;: [3840.0, 640.0, 3840.0], &quot;country&quot;: [4110.16, 755.1, 1458.8999999999999], '
            '&quot;region&quot;: [3984.8, 328.0000000000001, 400.0], &quot;focus&quot;: [[3984.8, 328.0], [3984.8, 328.0], '
            '[3984.8, 328.0], [3984.8, 328.0]], &quot;zoom&quot;: 1}"')
KEYS_NEW = ('data-keys="{&quot;world&quot;: [3840.0, 640.0, 3840.0], &quot;country&quot;: [4110.2, 720.0, 1897.0], '
            '&quot;region&quot;: [3868.8, 318.0, 1458.9], &quot;focus&quot;: [[3868.8, 318.0], [3868.8, 318.0], '
            '[3868.8, 318.0], [3868.8, 318.0]], &quot;zoom&quot;: 1}"')
# the still map (reduced motion, no script) frames the same: 1458.9 wide, 8:5, centred on the marker; the
# marks' size (--u) comes from v4-calm.css until the script measures it
MAP_OLD = 'viewBox="3781.8 218 406 200" style="--u:0.3172;--fine:1;--ter:.85"'
MAP_NEW = 'viewBox="3139.35 -137.81 1458.9 911.81" style="--fine:1;--ter:.85"'

# The land, cut to the widest frame the camera ever shows (the fall's first, the whole continent: x 1632 to
# 6048 and y -1568 to 2848 at any screen's shape, tools/v4_trip_calm.py's KEYS_NEW and v4-calm.js), with a
# margin: what lies beyond it (the Americas, most of Africa) is never on screen, and its coastline was a third
# of the page's weight in this map. Every point inside keeps its place to the tenth of a unit, as written. The
# finer graticule (.tm-g2) goes too: the calmed route never shows it.
CLIP = (1400, -1800, 6300, 3100)


def rings(d):
    """The closed outlines of a path written in M, L, H, V and their relative forms, as absolute points."""
    toks = re.findall(r"[MmLlHhVvZz]|-?\d*\.?\d+", d)
    x = y = sx = sy = 0.0
    out, cmd, i = [], None, 0
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                x, y = sx, sy
                continue
        n = 1 if cmd in "HhVv" else 2
        v = [float(t) for t in toks[i:i + n]]
        i += n
        if cmd in "Mm":
            x, y = (v[0], v[1]) if cmd == "M" else (x + v[0], y + v[1])
            sx, sy = x, y
            out.append([(x, y)])
            cmd = "L" if cmd == "M" else "l"
            continue
        if cmd == "L": x, y = v
        elif cmd == "l": x, y = x + v[0], y + v[1]
        elif cmd == "H": x = v[0]
        elif cmd == "h": x += v[0]
        elif cmd == "V": y = v[0]
        elif cmd == "v": y += v[0]
        else: fail("land: a path command the cut does not read (%s)" % cmd)
        out[-1].append((x, y))
    return out


def cut(ring):
    """One outline cut to CLIP, a side at a time (Sutherland and Hodgman): what is inside keeps its points."""
    x0, y0, x1, y1 = CLIP
    sides = ((lambda q: q[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
             (lambda q: q[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
             (lambda q: q[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
             (lambda q: q[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1)))
    for inside, cross in sides:
        pts, ring = ring, []
        for k in range(len(pts)):
            a, b = pts[k - 1], pts[k]
            if inside(b):
                if not inside(a):
                    ring.append(cross(a, b))
                ring.append(b)
            elif inside(a):
                ring.append(cross(a, b))
        if not ring:
            break
    return ring


def num(v):
    t = ("%.1f" % v).rstrip("0").rstrip(".")
    t = t.replace("-0.", "-.") if t.startswith("-0.") else (t[1:] if t.startswith("0.") else t)
    return "0" if t in ("", "-0") else t


def outline(ring):
    """An outline written as the map writes its own: a move, then relative steps to the tenth, closed."""
    pts = [(round(x, 1), round(y, 1)) for x, y in ring]
    y = num(pts[0][1])
    out, prev = "M%s%s%sl" % (num(pts[0][0]), "" if y.startswith("-") else " ", y), pts[0]
    first = True
    for q in pts[1:]:
        dx, dy = q[0] - prev[0], q[1] - prev[1]
        if abs(dx) < .05 and abs(dy) < .05:
            continue
        a, b = num(dx), num(dy)
        out += ("" if first or a.startswith("-") else " ") + a + ("" if b.startswith("-") else " ") + b
        first, prev = False, q
    return out + "z"


def land(src):
    m = re.search(r'<g class="tm-land">(.*?)</g>', src, re.S)
    if not m:
        fail("land: no .tm-land")
    paths = []
    for d in re.findall(r'<path d="([^"]*)"/>', m.group(1)):
        kept = [r for r in (cut(r) for r in rings(d)) if len(r) > 2]
        if kept:
            paths.append('<path d="%s"/>' % "".join(outline(r) for r in kept))
    if not paths:
        fail("land: nothing left inside the frame")
    return src[:m.start(1)] + "".join(paths) + src[m.end(1):]


# The schematic, without drawn hills: the two ranges are straight hairlines with their names set on them,
# every dot, route curve, label and the span bar (513 units for about 70 km, 367 for about 50 km) as they
# were. Each lit line has a mask of the same curve, which the eased loop draws with the scroll (v4-calm.js);
# without the script, or with reduced motion, the masks are whole and the lines show in full.
SCHEM = """<svg class="iroute-svg" viewBox="0 0 1000 400" role="img" aria-labelledby="irT irD">
  <title id="irT">The Dhauladhar front range above Bir, drawn as a schematic</title>
  <desc id="irD">Billing launch sits on the front range above the Bir landing field. The standard day runs west to Dharamshala and back, a bigger day adds 360 to the east, and the back ranges rise behind.</desc>
  <defs>
    <mask id="irmW" class="ir-m" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="400"><path class="ir-mk" d="M573 164c-120-44-173-44-293-14"/><path class="ir-mk" d="M280 158c120-12 173-12 287 8"/></mask>
    <mask id="irmE" class="ir-m" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="400"><path class="ir-mk" d="M573 164c70-32 137-36 197-14"/></mask>
    <mask id="irmO" class="ir-m" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="400"><path class="ir-mk" d="M573 164c10-44 40-68 70-104"/></mask>
  </defs>
  <path class="ir-back" d="M60 96H940"/>
  <text class="ir-k" x="60" y="86">Back ranges, towards Barabangal and Manali</text>
  <path class="ir-front" d="M60 196H940"/>
  <text class="ir-k" x="60" y="186">The Dhauladhar front range</text>
  <line class="ir-valley" x1="60" y1="318" x2="940" y2="318"/>
  <text class="ir-k" x="940" y="340" text-anchor="end">Kangra valley</text>
  <line class="ir-drop" x1="573" y1="172" x2="573" y2="318"/>
  <path class="ir-west" mask="url(#irmW)" d="M573 164c-120-44-173-44-293-14"/>
  <path class="ir-west" mask="url(#irmW)" d="M280 158c120-12 173-12 287 8"/>
  <path class="ir-east" mask="url(#irmE)" d="M573 164c70-32 137-36 197-14"/>
  <path class="ir-over" mask="url(#irmO)" d="M573 164c10-44 40-68 70-104"/>
  <circle class="ir-dot" cx="280" cy="160" r="6"/>
  <text class="ir-l is-strong" x="280" y="126" text-anchor="middle">Dharamshala</text>
  <circle class="ir-dot" cx="770" cy="160" r="6"/>
  <text class="ir-l is-strong" x="770" y="126" text-anchor="middle">360</text>
  <circle class="ir-dot ir-home" cx="573" cy="168" r="7"/>
  <text class="ir-l is-strong" x="587" y="226">Billing launch</text>
  <text class="ir-k" x="587" y="252">about 2,400m</text>
  <circle class="ir-dot" cx="573" cy="318" r="6"/>
  <text class="ir-l is-strong" x="587" y="306">Bir landing</text>
  <text class="ir-k" x="657" y="72">Over the back</text>
  <line class="ir-span" x1="60" y1="372" x2="573" y2="372"/>
  <line class="ir-span" x1="60" y1="366" x2="60" y2="378"/><line class="ir-span" x1="573" y1="366" x2="573" y2="378"/>
  <text class="ir-k" x="316" y="394" text-anchor="middle">about 70 km of front range to the west</text>
  <line class="ir-span" x1="573" y1="372" x2="940" y2="372"/>
  <line class="ir-span" x1="940" y1="366" x2="940" y2="378"/>
  <text class="ir-k" x="756" y="394" text-anchor="middle">about 50 km to the east</text>
</svg>"""

# ---------- the gallery: an edited sequence, opened and closed on a strong photograph ----------
# (file, folder, caption, alt, width, height, --fx, --fy); the hero's four keep their alt text and take their tab
# names, Last light its caption and alt from the pushed page. It opens on the strongest aerial that is not the
# hero's photograph (the back ranges from the air), runs as a day (the launch, the flying, the valley, the
# landing, the monastery) and closes on Last light, the one sunset. --fx is the point its crop keeps across on
# an upright screen, --fy the point it keeps down on a wide one (the green wing at Billing, the peak under the
# wing, the two hikers, the monastery's roof, the wing in the sun). No two near-identical scenes sit together.
# Thirteen: the twelve the page had (their words stay on the page) and Last light.
GALLERY = [
    ("back-ranges", "hero", "The back ranges", "Snow-covered back ranges seen from the air", 1920, 848, "50%", "50%"),
    ("billing-launch", "hero", "Billing launch", "Pilots laying out and launching on the grass at Billing", 2000, 1333, "74%", "42%"),
    ("over-the-peaks", "gallery", "Over the peaks", "A single wing high above a snow-streaked peak", 1400, 933, "44%", "72%"),
    ("dhauladhar", "hero", "The Dhauladhar", "The Dhauladhar range under building cumulus, above the Kangra valley", 2400, 1600, "50%", "56%"),
    ("hike-and-fly", "gallery", "Hike and fly", "Two pilots with paraglider rucksacks climbing a forest trail", 1400, 933, "44%", "58%"),
    ("valley-river", "gallery", "The valley floor", "Terraced fields, a river and villages seen from the air", 1400, 933, "62%", "50%"),
    ("cloud-range", "gallery", "Cloud on the range", "A snow-dusted rock peak half hidden in cloud", 1400, 933, "46%", "45%"),
    ("kangra-valley", "gallery", "Kangra valley", "The Kangra valley from the air, villages and fields below the hills", 1400, 933, "40%", "60%"),
    ("meadows", "gallery", "Meadows below the range", "A meadow of white flowers below the snow-covered Dhauladhar", 1400, 933, "56%", "55%"),
    ("bir-landing", "hero", "Bir landing", "Bir's landing field among terraced fields, seen from the air", 1600, 899, "50%", "50%"),
    ("landing-field", "gallery", "The landing field", "The Bir landing field under big cumulus, snow peaks behind, one wing coming in", 1400, 933, "62%", "50%"),
    ("monastery", "gallery", "Tibetan monastery", "A Tibetan monastery with prayer flags against a blue sky", 1400, 933, "64%", "35%"),
    ("last-light", "gallery", "Last light", "A paraglider silhouetted against a burning sunset", 1400, 933, "47%", "45%"),
]
# the hero's photograph and the fly-through's five: none of them is shown twice on the page
GONE = ("snowline", "red-wing", "launch-day", "front-range", "last-light-pair", "ridge-cumulus", "sky-of-wings")


def gallery():
    """The run's markup, one for every screen: v4-calm.css lays it out as a column of plates (a phone, reduced
    motion, no script) or, once v4-calm.js marks the section .is-pin on a wide screen, as one pinned frame the
    photographs dissolve through, with the progress marks under it; each caption carries its own place in the
    run (01 / 13), so the count and the caption showing are always the same photograph's."""
    figs = []
    for k, (name, folder, title, alt, wd, ht, fx, fy) in enumerate(GALLERY):
        g = A + folder + "/" + name
        # the hero's four keep their JPEG under a WebP source; the gallery's own photographs are WebP only, as
        # before, so their <img> needs no source beside it
        webp = '<source srcset="%s.webp" type="image/webp">' % g if folder == "hero" else ""
        src = g + (".jpg" if folder == "hero" else ".webp")
        figs.append('<figure class="v4c-g-f" style="--fx:%s;--fy:%s"><picture>%s<img src="%s" alt="%s" width="%d" height="%d" '
                    'loading="lazy" decoding="async"></picture><figcaption><span class="v4c-g-n">%02d / %02d</span><b>%s</b>'
                    '<span class="v4c-g-alt">%s</span></figcaption></figure>'
                    % (fx, fy, webp, src, esc(alt), wd, ht, k + 1, len(GALLERY), esc(title), esc(alt)))
    # the progress marks are drawn by v4-calm.css on the one empty rail (a tick a photograph, from --n)
    return ('<section class="dst-sec v4c-g" id="gallery" aria-labelledby="gallery-h" style="--n:%d">\n'
            '  <div class="v4c-g-head"><span class="kicker">The pictures</span><h2 id="gallery-h">Bir Billing In Pictures</h2></div>\n'
            '  <div class="v4c-g-track"><div class="v4c-g-pin">\n'
            '  <a class="v4c-g-skip" href="#guides">Skip the pictures <i aria-hidden="true">&darr;</i></a>\n'
            '  %s\n'
            '  <div class="v4c-g-rail" aria-hidden="true"></div>\n'
            '  </div></div>\n</section>' % (len(GALLERY), "\n  ".join(figs)))


# ---------- the page's own sheet and script: linked here alone, with the hash of the copy v4_min writes ----------
def stamp(name):
    src = open(os.path.join(V4, "src", name), encoding="utf-8").read()
    out = v4_min.HEAD % name + (v4_min.css if name.endswith(".css") else v4_min.js)(src)
    return hashlib.sha256(out.encode("utf-8")).hexdigest()[:8]


# ---------- the page's own styles: the old routes sheet's rules go with its script ----------
# (the drawing now lives in the trip map's schematic; .iroute-svg and the .ir-* rules stay)
SHEET_CSS_OLD = """.iroute-fig{margin:2.2rem 0 0;}
.iroute-scroll{overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;}
.iroute-svg{display:block;width:100%;min-width:760px;height:auto;}
@media (min-width:860px){.iroute-svg{min-width:0;}}
.iroute-fig figcaption{margin-top:.8rem;color:var(--gray);font-size:.82rem;line-height:1.6;max-width:70ch;}
.iroute-hint{display:none;}
@media (max-width:859px){.iroute-hint{display:inline;}}
"""
SHEET_CSS_NEW = """.iroute-svg{display:block;width:100%;min-width:760px;height:auto;}
@media (min-width:860px){.iroute-svg{min-width:0;}}
"""
LIST_CSS_OLD = """.iroute-list{list-style:none;margin:2.4rem 0 0;padding:0;display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));gap:2rem;}
@media (max-width:900px){.iroute-list{grid-template-columns:1fr;gap:1.6rem;}}
.iroute-item{padding-top:1rem;border-top:2px solid var(--orange);}
.iroute-item.is-east{border-top-style:dashed;}
.iroute-item.is-over{border-top:2px dotted var(--gray-light);}
.iroute-item h3{font-family:var(--font-display);font-weight:600;font-size:1.16rem;color:var(--white);
  margin:0 0 .3rem;}
.iroute-km{display:block;color:var(--gray);font-size:.82rem;margin-bottom:.8rem;}
.iroute-item p{margin:0;color:var(--gray-light);font-size:.95rem;line-height:1.75;}
.iroute-item a{color:var(--gray-light);}
"""
LIST_CSS_NEW = "/* v4c: the routes sheet's list, scroller and hint are gone with it (tools/v4_trip_calm.py) */\n"

# The page's own rules for the schematic's two ranges and its type, and for the guides, are India's alone
# (no other page has them), so they take the calmed look here rather than being overruled from v4-calm.css:
# the ranges two straight lines (the front solid, the back ranges dashed behind it), the type at a size that
# reads; each guide under a hairline (the facts' figures), the name large, the role in the page's label type
# (no orange: the section keeps one), the one strong line under them.
IR_OLD = """.ir-back{fill:none;stroke:var(--gray);stroke-width:1.3;stroke-dasharray:5 6;}
.ir-front{fill:none;stroke:var(--gray-light);stroke-width:2;stroke-linejoin:round;}
"""
IR_NEW = """.ir-back{fill:none;stroke:var(--edge-hi);stroke-width:1;stroke-dasharray:5 7;vector-effect:non-scaling-stroke;}
.ir-front{fill:none;stroke:var(--gray);stroke-width:1;vector-effect:non-scaling-stroke;}
"""
IRT_OLD = """.ir-l{font-family:var(--font-body);font-size:15px;fill:var(--gray-light);}
.ir-l.is-strong{fill:var(--white);font-weight:500;}
.ir-k{font-family:var(--font-body);font-size:12.5px;fill:var(--gray);}
"""
IRT_NEW = """.ir-l{font-family:var(--font-body);font-size:20px;fill:var(--gray-light);}
.ir-l.is-strong{fill:var(--white);font-weight:500;}
.ir-k{font-family:var(--font-body);font-size:18px;fill:var(--gray-light);}
"""
GUIDES_OLD = """.kguides-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--rule);
  border:1px solid var(--rule);margin-top:1rem;}
@media (max-width:820px){.kguides-grid{grid-template-columns:1fr;}}
.kguide{background:var(--bg);padding:clamp(1.2rem,2.4vw,1.8rem);}
.kguide h3{font-family:var(--font-display);font-weight:600;font-size:1.2rem;color:var(--white);margin:0;}
.kguide-role{display:block;color:var(--orange);font-size:.78rem;letter-spacing:.04em;margin:.3rem 0 .9rem;}
.kguide p{margin:0;color:var(--gray-light);font-size:.95rem;line-height:1.75;}
.kguides-note{margin:.9rem 0 0;color:var(--gray);font-size:.86rem;}
"""
GUIDES_NEW = """.kguides-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-4) var(--sp-5);margin-top:var(--sp-3);}
@media (max-width:820px){.kguides-grid{grid-template-columns:1fr;}}
.kguide{position:relative;padding:var(--sp-3) 0 0;}
.kguide::before{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:var(--edge);}
.kguide h3{font-family:var(--font-display);font-weight:600;font-size:var(--fs-h3);color:var(--white);margin:0;}
.kguide-role{display:block;color:var(--gray-light);font-size:var(--fs-micro);font-weight:600;letter-spacing:.14em;line-height:1.5;text-transform:uppercase;margin:.5rem 0 .7rem;}
.kguide p{margin:0;color:var(--gray-light);font-size:.95rem;line-height:1.75;}
.kguides-note{margin:var(--sp-4) 0 0;color:var(--white);font-size:var(--fs-lead);}
"""

# the usability pass's phone heights for the gallery's and the route's pins, and its framing of the pinned
# gallery on an upright screen (tools/v4_ux.py), have nothing left to act on here: the gallery is a still
# column and the route's pin has its own length (v4-calm.css); they go, for the page's weight on arrival
UX_PINS = ("@media (max-width:760px){html .gxa-track{height:calc(var(--n) * 15vh + 100vh);height:calc(var(--n) * 15svh + 100svh)}"
           "html .tm-track{height:calc(var(--n) * 50vh + 120vh);height:calc(var(--n) * 50svh + 120svh)}}"
           "@media (max-width:1100px) and (orientation:portrait){html .gxa-f{display:flex;flex-direction:column;justify-content:center}"
           "html .gxa-f picture{height:auto;flex:none}html .gxa-f img{height:auto;max-height:56vh;max-height:56svh;object-fit:contain;"
           "transform:scale(calc(1.03 - .03 * var(--t,0)));transform-origin:50% 50%}html .gxa-f::after{display:none}"
           "html .gxa-f figcaption{position:static;margin:var(--sp-3) var(--edge-x) 0;max-width:none}}")
UX_NEXT = "html .v4u-etq{"

# the usability pass's media script (tools/v4_ux.py) also woke the hero's later slides and the home page's
# fly-by stage; with one plate and no fly-by here, only its footage sizing stays
MEDIA_OLD = 'function wake(el) {\nif (!el) return;\n[].forEach.call(el.querySelectorAll ? el.querySelectorAll("[data-v4-src],[data-v4-srcset]") : [], function (x) {\nif (x.dataset.v4Srcset) { x.srcset = x.dataset.v4Srcset; x.removeAttribute("data-v4-srcset"); }\nif (x.dataset.v4Src) { x.src = x.dataset.v4Src; x.removeAttribute("data-v4-src"); }\n});\n}\nfunction init() {\nif (mo) { mo.disconnect(); [].forEach.call(d.querySelectorAll("video[data-loop]"), fit); }\nvar slides = [].slice.call(d.querySelectorAll(".khero-slide"));\nif (slides.length > 1) {\nvar next = function () {\nvar i = slides.findIndex(function (s) { return s.classList.contains("is-on"); });\nwake(slides[i]); wake(slides[(i + 1) % slides.length]);\n};\nslides.forEach(function (s) { new MutationObserver(next).observe(s, { attributes: true, attributeFilter: ["class"] }); });\nvar soon = function () { setTimeout(function () { wake(slides[1]); }, 4500); };\nif (d.readyState === "complete") soon(); else w.addEventListener("load", soon, { once: true });\n}\nvar fb = d.querySelector(".v2-fb-stage");\nif (fb && fb.querySelector("[data-v4-src]")) {\nvar go = function () { w.removeEventListener("scroll", go); if (io) io.disconnect(); wake(fb); }, io = null;\nw.addEventListener("scroll", go, { passive: true });\nif ("IntersectionObserver" in w) { io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.intersectionRatio > 0; })) go(); }); io.observe(fb.closest(".v2-flyby") || fb); }\nelse go();\n}\n}\n'
MEDIA_NEW = """function init() {
if (mo) { mo.disconnect(); [].forEach.call(d.querySelectorAll("video[data-loop]"), fit); }
}
"""

# ---------- the inline scripts ----------
# The page's three small scripts of this pass (the booking bar that rises after the hero and steps aside for
# the departures' cards, the call and the footer; the fly-through's step and photograph swap; Flying
# Etiquette's open and close) live in v4-calm.js now (its chores()), written there once without the inline
# copies' comments and indentation, for the page's weight on arrival; their marks here stay, empty, so the
# old scripts are found and taken out on a fresh page and a second run changes nothing.


def patch(src):
    # the page opts in, and loads its own sheet (after destinations.css) and script (after v2-immersive.js)
    src = swap(src, "html", '<html lang="en">', '<html lang="en" class="v4-calm">')
    src = marked(src, "calm-css", '<link rel="stylesheet" href="../v4-calm.css?v=%s">' % stamp("v4-calm.css"),
                 r'(?<=<link rel="stylesheet" href="\.\./\.\./\.\./destinations\.css\?v=[0-9a-f]{8}">)')
    src = marked(src, "calm-js", '<script src="../v4-calm.js?v=%s"></script>' % stamp("v4-calm.js"),
                 r'(?<=<script src="\.\./v2-immersive\.js\?v=[0-9a-f]{8}"></script>)')
    # the departures' flag keeps the green of .v2-status.is-go (the page's own orange chip rule would win)
    src = swap(src, "flag-css", ".kdates-flags span.is-go{color:var(--orange);border-color:var(--orange);}",
               "/* v4c: the departures' flag is .v2-status.is-go, in its own green (tools/v4_trip_calm.py) */")

    src = swap(src, "sheet-css", SHEET_CSS_OLD, SHEET_CSS_NEW)
    src = swap(src, "ux-pins", UX_PINS + UX_NEXT, UX_NEXT)
    src = swap(src, "ux-media", MEDIA_OLD, MEDIA_NEW)
    src = swap(src, "list-css", LIST_CSS_OLD, LIST_CSS_NEW)
    src = swap(src, "ir-css", IR_OLD, IR_NEW)
    src = swap(src, "ir-type", IRT_OLD, IRT_NEW)
    src = swap(src, "guides-css", GUIDES_OLD, GUIDES_NEW)

    # the hero: one plate (slide 1, its poster and footage, keeps is-on); no tabs, no cue
    src = marked(src, "hero-slides", "",
                 r'<div class="khero-slide">\n        <picture>\n[^\n]*india-billing-launch-p\.webp.*?back-ranges\.jpg.*?</picture>\n      </div>')
    src = marked(src, "hero-rail", "", r'<div class="khero-rail" role="group" aria-label="Choose a photograph">.*?</div>\n  <a class="khero-cue" href="#overview"><span>Scroll</span><i></i></a>')
    if src.count('class="khero-slide') != 1 or "khero-tab" in src.split("</header>", 1)[0]:
        fail("hero: more than one plate left")

    # four big facts
    src = marked(src, "facts", facts(), r'<section class="dst-spec v4t-spec">\n  <div class="dst-spec-grid">.*?</section>')

    # the fly-through: slides 2 to 5 with their no-script twins (every readout row stays)
    src = marked(src, "fly-slides", fly_slides(),
                 r'<div class="kfly-slide"><picture><source data-v4-srcset="[^"]*gallery/front-range\.webp".*?gallery/sky-of-wings\.jpg"[^>]*></picture></div>')

    # the gauge, finished: 3.6 of 6 km is 108 degrees about the needle's own pivot
    src = swap(src, "needle", '<line class="needle" x1="120" y1="120" x2="32.0" y2="120.0"/>',
               '<line class="needle" x1="120" y1="120" x2="32.0" y2="120.0" style="transform:rotate(108deg)"/>')
    src = swap(src, "read", '<text class="read" x="120" y="160">0.0</text>', '<text class="read" x="120" y="160">3.6</text>')

    # the route and the gallery gave way to the immersion chat's map (tools/v4_india_immersive.py, 28 Oct):
    # once its marks are on the page, this pass leaves those two parts alone
    ie = "<!--v4ie:" in src
    if not ie:
        src = swap(src, "route", '<section class="dst-sec tm" id="route"', '<section class="dst-sec tm-calm" id="route"')
        src = swap(src, "keys", KEYS_OLD, KEYS_NEW)
        src = land(src)
        g2 = len(re.findall(r'<path class="tm-g2" d="[^"]*"/>', src))
        if g2 not in (0, 12):
            fail("map: expected the 12 lines of the finer graticule, found %d" % g2)
        src = re.sub(r'<path class="tm-g2" d="[^"]*"/>', "", src)
        src = swap(src, "map", MAP_OLD, MAP_NEW)
        src = marked(src, "schem", SCHEM, r'<svg class="iroute-svg" viewBox="0 0 1000 400" role="img" aria-labelledby="irT irD">.*?</svg>')

    # the departures: each tour's dates under its bar; the flag in green, the count plain
    # (India's 2027 bands carry their dates already, tools/v4_india_2027.py; these label the 2026 tours if they come back)
    if '<i class="kdates-tour" style="--a:32.79;--w:16.39;--i:0"><b>01</b></i>' in src:
        src = swap(src, "tour1", '<i class="kdates-tour" style="--a:32.79;--w:16.39;--i:0"><b>01</b></i>',
                   '<i class="kdates-tour" style="--a:32.79;--w:16.39;--i:0"><b>01</b><span>21 to 30 Oct</span></i>')
        src = swap(src, "tour2", '<i class="kdates-tour" style="--a:54.10;--w:16.39;--i:1"><b>02</b></i>',
                   '<i class="kdates-tour" style="--a:54.10;--w:16.39;--i:1"><b>02</b><span>3 to 12 Nov</span></i>')
    src = swap(src, "flags", '<p class="kdates-flags"><span class="is-go">Guaranteed to run</span><span>6 places</span></p>',
               '<p class="kdates-flags"><span class="v2-status is-go">Guaranteed to run</span><span>6 places</span></p>',
               n=4)   # India's four 2027 departures (tools/v4_india_2027.py)

    # the gallery: a pinned run on a wide screen, a column of plates on a phone (v4-calm.css, v4-calm.js)
    if not ie:
        src = marked(src, "gallery", gallery(), r'<section class="dst-sec gxa" id="gallery".*?</section>')
        gal = src.split('id="gallery"', 1)[1].split("</section>", 1)[0]
        for g in GONE:
            if g + "." in gal:
                fail("gallery: %s is still there" % g)
        rest = src.replace(gal, "")
        for name, folder, *_ in GALLERY:
            if "/%s/%s." % (folder, name) in rest:
                fail("gallery: %s is shown elsewhere on the page too" % name)

    # the scripts
    src = marked(src, "mobar", "", r'<script>\n\(function\(\)\{\n  /\* The booking bar rises.*?</script>')
    src = marked(src, "hero-script", "", r'<script>\n/\* Hero\. Five photographs, crossfaded, drifting\..*?</script>')
    src = marked(src, "routes-sheet", "", r'<script>\n/\* Routes sheet\..*?</script>')
    src = marked(src, "overview", "", r'<script>\n/\* Overview prototype\..*?</script>')
    # the fly-through's photographs wake as it comes near: it now begins behind the Overview heading, so
    # "near" is measured from the screen's foot, or the five would load on arrival (the page's weight rule)
    src = swap(src, "fly-wake", "{ rootMargin: '60% 0px' }", "{ rootMargin: '0px 0px 25% 0px' }")
    src = swap(src, "faq-curve", "body.style.transition='height .32s ease';", "body.style.transition='height .32s var(--ease)';", n=2)
    src = marked(src, "etiquette", "", r'<script>\n/\* Flying Etiquette: vertical scroll drives the sideways run of rules\. \*/.*?</script>')

    # last, the page written compactly (its weight on arrival)
    src = compact(src)
    if "\u2014" in src:
        fail("an em dash crept in")
    if "iroute-scroll" in re.sub(r"<style>.*?</style>", "", src, flags=re.S):
        fail("a script still looks for .iroute-scroll")
    return src


def main():
    trip = sys.argv[1] if len(sys.argv) > 1 else "india"
    if trip not in TRIPS:
        raise SystemExit("v4_trip_calm: only %s this round (got %r)" % (", ".join(sorted(TRIPS)), trip))
    p = os.path.join(V4, TRIPS[trip])
    src = open(p, encoding="utf-8").read()
    out = patch(src)
    if out != src:
        open(p, "w", encoding="utf-8").write(out)
    print("v4_trip_calm: %s %s, sha256 %s" % (TRIPS[trip], "patched" if out != src else "unchanged",
                                             hashlib.sha256(out.encode("utf-8")).hexdigest()[:16]))


if __name__ == "__main__":
    main()
