#!/usr/bin/env python3
"""
Kenya's page takes the immersion chat's map (owner, 28 Oct 2026: "push the immersion handoff"; that chat's note the
same day: Kenya goes live through the live-site chat). That chat's finished page is
prototypes/v4/destinations/kenya-e.html ("Rift Immersive": the sites down the Rift flown by the scroll over live
terrain drawn by fly.js, the figures, the chapter rail). As with India (tools/v4_india_immersive.py), the page
itself is not copied: the current Kenya page keeps every fact it has and its own gallery, and takes from kenya-e
only

  - its section #flight, in place of the old route (#route);
  - the style block that section uses (kenya-e's "option D" style);
  - the terrain engine (../fly.js, a module) and the flight's own small script (its chapter rail);
  - its jump link for the flight (Rift Immersive), in place of Routes.

The page keeps #v4-kenya-own, so its FAQ stays out of the reading light (src/v2.css GRAIN). Run in
tools/v4_build.py after tools/v4_india_immersive.py. Idempotent: the parts sit between v4ke marks and a second run
writes the same bytes.

    python3 tools/v4_kenya_immersive.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "prototypes", "v4", "destinations")
SRC = os.path.join(DST, "kenya-e.html")
OUT = os.path.join(DST, "kenya.html")


def fail(msg):
    raise SystemExit("v4_kenya_immersive: " + msg)


def section(s, ident):
    m = re.search(r'<section[^>]*\sid="%s"' % ident, s)
    if not m:
        return None
    j = s.find("</section>", m.start())
    if s.find("<section", m.start() + 1, j) != -1:
        fail("#%s holds another section" % ident)
    return m.start(), j + len("</section>")


def mark(name, body):
    return "<!--v4ke:%s-->%s<!--/v4ke:%s-->" % (name, body, name)


def main():
    e = open(SRC, encoding="utf-8").read()
    s = open(OUT, encoding="utf-8").read()
    span = section(e, "flight")
    if not span:
        fail("kenya-e.html has no #flight")
    styles = re.findall(r"<style>\s*/\* v4 India option D\b.*?</style>", e, re.S)
    if len(styles) != 1:
        fail("kenya-e.html's flight style not found (%d)" % len(styles))
    fly = re.search(r'<script type="module" src="\.\./fly\.js[^"]*"></script>', e)
    if not fly:
        fail("the fly.js module tag not found")
    rail = [m.group(0) for m in re.finditer(r"<script>.*?</script>", e, re.S) if 'getElementById("flight")' in m.group(0)]
    if len(rail) != 1:
        fail("the flight's own script not found (%d)" % len(rail))
    jump = re.search(r'<a [^>]*href="#flight"[^>]*>.*?</a>', e, re.S)
    if not jump:
        fail("kenya-e.html's jump link to #flight not found")
    blocks = {"sections": e[span[0]:span[1]], "jump": jump.group(0), "css": styles[0], "js": fly.group(0) + "\n" + rail[0]}

    if "<!--v4ke:" in s:
        for name, body in blocks.items():
            s, n = re.subn(r"<!--v4ke:%s-->.*?<!--/v4ke:%s-->" % (name, name), lambda _: mark(name, body), s, flags=re.S)
            if n != 1:
                fail("the v4ke marks for %s: found %d" % (name, n))
        open(OUT, "w", encoding="utf-8").write(s)
        print("v4 Kenya immersive: refreshed from kenya-e.html")
        return

    r = section(s, "route")
    if not r:
        fail("kenya.html has no #route")
    s = s[:r[0]] + mark("sections", blocks["sections"]) + s[r[1]:]
    ro = re.search(r'<a [^>]*href="#route"[^>]*>.*?</a>', s, re.S)
    if not ro:
        fail("kenya.html's jump link to #route not found")
    s = s[:ro.start()] + mark("jump", blocks["jump"]) + s[ro.end():]
    if 'href="#route"' in s:
        fail("a link to #route is left on the page")
    if 'id="v4-kenya-own"' not in s:
        fail("#v4-kenya-own is gone (it keeps the FAQ out of the reading light)")
    s = s.replace("</head>", mark("css", blocks["css"]) + "\n</head>", 1)
    s = s.replace("</body>", mark("js", blocks["js"]) + "\n</body>", 1)
    open(OUT, "w", encoding="utf-8").write(s)
    print("v4 Kenya immersive: the flight in place of the route")


if __name__ == "__main__":
    main()
