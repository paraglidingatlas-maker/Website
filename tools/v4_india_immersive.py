#!/usr/bin/env python3
"""
India's page takes the immersion chat's map (owner, 28 Oct 2026: "replace the current india page with the one
finalised in immersion chat"). That chat's finished page is prototypes/v4/destinations/india-e.html ("Bir
Immersive": the ridge flown by the scroll, the live Dhauladhar terrain drawn by fly.js, the pictures row). Its
other sections carry the facts of the day it was built (two 2026 departures), so the page itself is not copied:
the current India page keeps every fact it has (four 2027 departures, guides, FAQ) and takes from india-e only

  - its sections #ridge, #flight and #pictures, in place of the old route (#route) and gallery (#gallery); the
    ridge's 60 frames are cut again from the Bir clip by tools/v4_india_ridge_frames.py (that chat's were all
    the clip's first picture);
  - the two style blocks those sections use (india-e's "option C" and "option D" styles);
  - the terrain engine (../fly.js, a module) and the ridge's frame script;
  - its jump link for the flight (Bir Immersive), in place of Routes and Gallery.

Run in tools/v4_build.py after tools/v4_trip_calm.py india. Idempotent: the parts sit between v4ie marks and a
second run writes the same bytes.

    python3 tools/v4_india_immersive.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "prototypes", "v4", "destinations")
SRC = os.path.join(DST, "india-e.html")
OUT = os.path.join(DST, "india.html")


def fail(msg):
    raise SystemExit("v4_india_immersive: " + msg)


def section(s, ident):
    m = re.search(r'<section[^>]*\sid="%s"' % ident, s)
    if not m:
        return None
    j = s.find("</section>", m.start())
    if s.find("<section", m.start() + 1, j) != -1:
        fail("#%s holds another section" % ident)
    return m.start(), j + len("</section>")


def mark(name, body):
    return "<!--v4ie:%s-->%s<!--/v4ie:%s-->" % (name, body, name)


def main():
    e = open(SRC, encoding="utf-8").read()
    s = open(OUT, encoding="utf-8").read()
    secs = []
    for ident in ("ridge", "flight", "pictures"):
        span = section(e, ident)
        if not span:
            fail("india-e.html has no #%s" % ident)
        secs.append(e[span[0]:span[1]])
    styles = re.findall(r"<style>\s*/\* v4 India option [CD]\b.*?</style>", e, re.S)
    if len(styles) != 2:
        fail("india-e.html's two section styles not found (%d)" % len(styles))
    fly = re.search(r'<script type="module" src="\.\./fly\.js[^"]*"></script>', e)
    if not fly:
        fail("the fly.js module tag not found")
    jumps = {}
    for ident in ("flight",):
        m = re.search(r'<a [^>]*href="#%s"[^>]*>.*?</a>' % ident, e, re.S)
        if not m:
            fail("india-e.html's jump link to #%s not found" % ident)
        jumps[ident] = m.group(0)

    ridge = [m.group(0) for m in re.finditer(r"<script>.*?</script>", e, re.S) if 'getElementById("ridge")' in m.group(0)]
    if len(ridge) != 1:
        fail("the ridge's frame script not found (%d)" % len(ridge))
    blocks = {"sections": "\n".join(secs), "jump": jumps["flight"], "css": "\n".join(styles),
              "js": fly.group(0) + "\n" + ridge[0]}
    if "<!--v4ie:" in s:
        # a later run: each marked part refreshed from india-e.html
        for name, body in blocks.items():
            s, n = re.subn(r"<!--v4ie:%s-->.*?<!--/v4ie:%s-->" % (name, name), lambda _: mark(name, body), s, flags=re.S)
            if n != 1:
                fail("the v4ie marks for %s: found %d" % (name, n))
        open(OUT, "w", encoding="utf-8").write(s)
        print("v4 India immersive: refreshed from india-e.html")
        return

    # the sections: the two in place of the route, the gallery gone (the pictures row takes its place)
    r = section(s, "route")
    if not r:
        fail("india.html has no #route")
    s = s[:r[0]] + mark("sections", blocks["sections"]) + s[r[1]:]
    g = section(s, "gallery")
    if not g:
        fail("india.html has no #gallery")
    s = s[:g[0]].rstrip(" \n") + "\n" + s[g[1]:].lstrip("\n")

    # the jump row: Bir Immersive in place of Routes; Gallery gone
    ro = re.search(r'<a [^>]*href="#route"[^>]*>.*?</a>', s, re.S)
    ga = re.search(r'\s*<a [^>]*href="#gallery"[^>]*>.*?</a>', s, re.S)
    if not ro or not ga:
        fail("india.html's jump links to #route and #gallery not found")
    s = s[:ga.start()] + s[ga.end():]
    ro = re.search(r'<a [^>]*href="#route"[^>]*>.*?</a>', s, re.S)
    s = s[:ro.start()] + mark("jump", blocks["jump"]) + s[ro.end():]
    if 'href="#route"' in s or 'href="#gallery"' in s:
        fail("a link to #route or #gallery is left on the page")

    # their styles and scripts
    s = s.replace("</head>", mark("css", blocks["css"]) + "\n</head>", 1)
    s = s.replace("</body>", mark("js", blocks["js"]) + "\n</body>", 1)
    open(OUT, "w", encoding="utf-8").write(s)
    print("v4 India immersive: the flight and the pictures in place of the route and the gallery")


if __name__ == "__main__":
    main()
