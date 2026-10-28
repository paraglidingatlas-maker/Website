#!/usr/bin/env python3
"""
The library, option E1: "the ridge and the voices on one screen" (owner, 28 Oct 2026: "here is the final design
that goes in library page", https://claude.ai/artifact/1PmqmchoF6Pr3Hig8LSQFk). The immersion chat published it
as a preview only (no patch), so this takes the preview's page and fits it to the v4 tree:

  - the shell (head, menu, footer) is prototypes/v4/library-e.html's, as option E had it;
  - from the preview: its library style block (the one that opens ".v4l{--lb:"), its <main> and its script
    (prototypes/v4/library-e1.js), with the preview's "prototypes/v4/" prefix taken off every path;
  - the title says "Option E1"; the body takes the preview's extra class v4l1.

library-e1.js is the preview's script with one change: the stills and the voice clips load from FILES (beside
the page in the prototype, /assets/v4/ on the live site, as fly.js does), since the switch-over moves files and
does not rewrite script strings; the episode links keep the data's own base.

The stills (img/library/stills/p, t, u) and the voice clips (img/library/clips, from clips.json) came with the
preview. Run by hand when the preview changes; tools/v4_library_live.py publishes the result as library.html.

    python3 tools/v4_library_e1.py <the preview's index.html>
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "library-e.html")
OUT = os.path.join(V4, "library-e1.html")
STYLE = re.compile(r"<style>\n\.v4l\{--lb:.*?</style>", re.S)


def fail(msg):
    raise SystemExit("v4_library_e1: " + msg)


def one(pat, s, what):
    ms = list(pat.finditer(s)) if hasattr(pat, "finditer") else None
    if not ms or len(ms) != 1:
        fail("%s: expected one, found %d" % (what, len(ms or [])))
    return ms[0]


def main():
    if len(sys.argv) != 2:
        fail("give the preview's index.html")
    art = open(sys.argv[1], encoding="utf-8").read()
    s = open(SHELL, encoding="utf-8").read()
    # the preview's parts, its paths made relative to prototypes/v4/
    st = one(STYLE, art, "the preview's library style").group(0).replace("prototypes/v4/", "")
    a, b = art.find('<main id="v4-main">'), art.find("</main>")
    if a < 0 or b < 0 or art.count("</main>") != 1:
        fail("the preview's <main>")
    main_ = art[a:b + len("</main>")].replace("prototypes/v4/", "")
    if "prototypes/" in main_ + st:
        fail("a path still names prototypes/")
    # into the shell
    s = s[:one(STYLE, s, "option E's library style").start()] + st + s[one(STYLE, s, "option E's library style").end():]
    a, b = s.find('<main id="v4-main">'), s.find("</main>")
    s = s[:a] + main_ + s[b + len("</main>"):]
    s, n = re.subn(r'<script src="library-e\.js(\?v=[0-9a-f]+)?" defer></script>', '<script src="library-e1.js" defer></script>', s)
    if n != 1:
        fail("option E's script tag")
    s, n = re.subn(r"<title>Option E: ", "<title>Option E1: ", s)
    if n != 1:
        fail("option E's title")
    s, n = re.subn(r'<body class="v4-lib-log v4l">', '<body class="v4-lib-log v4l v4l1">', s)
    if n != 1:
        fail("option E's body class")
    open(OUT, "w", encoding="utf-8").write(s)
    print("v4 library E1: library-e1.html from the preview (%d bytes)" % len(s))


if __name__ == "__main__":
    main()
