#!/usr/bin/env python3
"""
The site-wide pass, less but better (owner's queue, 20 Oct 2026, item 3): the
record page's pass, India's and Partners' carried to the home, podcast,
library, knowledge base, topics and about pages, one page type at a time.
Episode pages are off the list for now (owner, 20 Oct 2026).

The look is prototypes/v4/src/v4-quiet.css (written to v4-quiet.css by
tools/v4_min.py), which this links from the pass's pages alone; every rule is
under html.v4-quiet or a page type's own class (q-home, ...), so no other v4
page, and neither v2.css nor v2-immersive.js, changes. What it holds to is
said at the top of the sheet.

What this does to each page of a type, in place (each change between
<!--v4q:NAME--> marks or on the <html> tag; a second run changes nothing):

  - <html class="v4-quiet q-TYPE">;
  - links v4-quiet.css, with its version hash, after v2.css;
  - no rail drifts on its own (a .v2-rail's data-auto goes);
  - home and podcast: the globe no longer moves on its own. The live
    globe.js (never edited) turns the globe slowly whenever it is on screen
    and nothing is open, again three seconds after every touch, and widens
    and fades a ring round every pin for ever. This writes a v4 copy,
    prototypes/v4/v4-globe.js, from the live file with those two starts and
    the rings' animation taken out (each ring holds still as a halo), and the
    pages load it in place of the live one: drag, zoom, the pins and the
    flight to a pin are as they were. The copy is checked against the live
    file each run, so a change there stops this rather than being lost.

    python3 tools/v4_quiet.py home     # one type; with no argument, every type done so far

It runs in tools/v4_build.py after v4_ux.
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import v4_min   # noqa: E402

TYPES = {
    "home": ["index.html"],
    "podcast": ["podcast.html"],
}
GLOBE_PAGES = {"index.html", "podcast.html"}
# Rails that drift on their own (v2-immersive.js part 1 moves a .v2-rail[data-auto] whenever it is on screen and
# untouched): on every page of the pass the attribute goes, so a rail moves only by the visitor's swipe, drag or
# its arrows.
RAIL_AUTO = re.compile(r'(<div class="v2-rail[^"]*") data-auto\b')


def fail(msg):
    raise SystemExit("v4_quiet: " + msg)


def stamp(name):
    src = open(os.path.join(V4, "src", name), encoding="utf-8").read()
    out = v4_min.HEAD % name + v4_min.css(src)
    return hashlib.sha256(out.encode("utf-8")).hexdigest()[:8]


# The live globe's two starts of its spin: on load (when nothing is asked for in the address) and three
# seconds after the last touch. Both go; the timer that would run the spin is then never started. And the
# pins' rings, which widen and fade for ever (two SMIL <animate>s a pin): each holds still as a quiet halo.
GLOBE_CUTS = [
    ("""    if (!reduceMotion) {
      ring.append('animate').attr('attributeName', 'r').attr('values', '4;13')
        .attr('dur', '2.2s').attr('repeatCount', 'indefinite');
      ring.append('animate').attr('attributeName', 'opacity').attr('values', '0.7;0')
        .attr('dur', '2.2s').attr('repeatCount', 'indefinite');
    }
""", "    /* v4: the ring holds still */\n"),
    ("      if (!reduceMotion) startAutoRotate();\n", "      /* v4: no spin on its own */\n"),
    ("  if (!reduceMotion && !findPin(pinSlugFromHash())) startAutoRotate();\n", "  /* v4: no spin on its own */\n"),
]


def still_globe():
    src = open(os.path.join(ROOT, "globe.js"), encoding="utf-8").read()
    for old, new in GLOBE_CUTS:
        if src.count(old) != 1:
            fail("globe.js changed: %r is not there once" % old.strip())
        src = src.replace(old, new)
    head = ("/* v4-globe.js: written by tools/v4_quiet.py from the live globe.js, with its slow spin taken out (nothing\n"
            "   moves on its own). Do not edit; change globe.js and run the tool. */\n")
    out = head + src
    p = os.path.join(V4, "v4-globe.js")
    if not os.path.exists(p) or open(p, encoding="utf-8").read() != out:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
    return hashlib.sha256(out.encode("utf-8")).hexdigest()[:8]


def marked(src, name, new, find, page):
    a, b = "<!--v4q:%s-->" % name, "<!--/v4q:%s-->" % name
    if src.count(a) == 1 and src.count(b) == 1:
        i, j = src.index(a), src.index(b) + len(b)
        return src[:i] + a + new + b + src[j:]
    if a in src or b in src:
        fail("%s: the marks for %s are not a pair" % (page, name))
    ms = list(re.finditer(find, src, re.S))
    if len(ms) != 1:
        fail("%s: %s: expected one match, found %d" % (page, name, len(ms)))
    m = ms[0]
    return src[:m.start()] + a + new + b + src[m.end():]


def one(rel, kind, globe):
    p = os.path.join(V4, rel)
    src = open(p, encoding="utf-8").read()
    up = "../" * rel.count("/")
    # the classes on <html>
    m = re.search(r"<html([^>]*)>", src)
    attrs = m.group(1)
    want = "v4-quiet q-" + kind
    cm = re.search(r'\sclass="([^"]*)"', attrs)
    if cm:
        cls = [c for c in cm.group(1).split() if c != "v4-quiet" and not c.startswith("q-")]
        attrs2 = attrs.replace(cm.group(0), ' class="%s"' % " ".join(cls + want.split()))
    else:
        attrs2 = attrs + ' class="%s"' % want
    src = src[:m.start()] + "<html%s>" % attrs2 + src[m.end():]
    # the sheet, right after v2.css
    src = marked(src, "css", '<link rel="stylesheet" href="%sv4-quiet.css?v=%s">' % (up, stamp("v4-quiet.css")),
                 r'(?<=<link rel="stylesheet" href="%sv2\.css\?v=[0-9a-f]{8}">)' % re.escape(up), rel)
    # the still rails
    src = RAIL_AUTO.sub(r"\1", src)
    # the still globe
    if rel in GLOBE_PAGES:
        src = marked(src, "globe", '<script src="%sv4-globe.js?v=%s"></script>' % (up, globe),
                     r'<script src="(?:\.\./)+globe\.js\?v=[0-9a-f]{8}"></script>', rel)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)


def main():
    kinds = sys.argv[1:] or list(TYPES)
    for k in kinds:
        if k not in TYPES:
            fail("no page type %r (have: %s)" % (k, ", ".join(TYPES)))
    globe = still_globe()
    for k in kinds:
        for rel in TYPES[k]:
            one(rel, k, globe)
        print("v4_quiet: %s (%d page%s)" % (k, len(TYPES[k]), "" if len(TYPES[k]) == 1 else "s"))


if __name__ == "__main__":
    main()
