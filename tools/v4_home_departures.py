#!/usr/bin/env python3
"""
The home page's departures (owner, 25 Oct 2026: "do what you can yourself", option A "One Line, Two Postures", the
designers' majority pick): the opening's season line carried down across the top, the nine departures as rows under
it, each with a thin bar at its real dates; on a phone the line stands upright in the margin, one card per departure.
It takes the place of the old fly-by, line of months and table (<section id="destinations">).

Its source is the sample the owner reviewed, prototypes/v4/samples/departures/index.html (a full copy of the home
page). This copies from it into prototypes/v4/index.html:

  - its styles (the <style> before the section, every rule already under .sl) into the head, between marks;
  - the section itself (the line, the rows, the call band and its small script) in place of the old one, between
    marks, the sample's ../../ links made the home page's own.

Run it by hand after a change to the sample (like tools/v4_home_opening.py); the build keeps what it wrote.
Idempotent. tools/v4_polish.py reads the departures from these rows (.sl-row) for the Destinations count.

    python3 tools/v4_home_departures.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "samples", "departures", "index.html")
PAGE = os.path.join(V4, "index.html")
MARK = ("<!-- v4-home-departures: tools/v4_home_departures.py -->", "<!-- /v4-home-departures -->")
HEAD = ("<!-- v4-home-departures-head -->", "<!-- /v4-home-departures-head -->")
OLD = re.compile(r'<!-- =+ PART 1: FLY =+ -->\n<section id="destinations" class="kit-band v2-fly">.*?\n</section>', re.S)


def main():
    src = open(SRC, encoding="utf-8").read()
    m = re.search(r"<!-- =+ DEPARTURES:[^\n]*-->\n<style>\n(.*?)</style>\n(<section id=\"destinations\".*?\n</section>)", src, re.S)
    if not m:
        raise SystemExit("v4_home_departures: the sample's styles and section are not where they were")
    css, sec = m.group(1), m.group(2)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = "".join(line.strip() for line in css.splitlines())
    sec = sec.replace('href="../../', 'href="')
    if "../../" in sec:
        raise SystemExit("v4_home_departures: a sample path is left in the section")

    page = open(PAGE, encoding="utf-8").read()
    block = MARK[0] + "\n" + sec + "\n" + MARK[1]
    if MARK[0] in page:
        page = re.sub(re.escape(MARK[0]) + r".*?" + re.escape(MARK[1]), lambda _: block, page, flags=re.S)
    else:
        if len(OLD.findall(page)) != 1:
            raise SystemExit("v4_home_departures: the home page's old departures are not where they were")
        page = OLD.sub(lambda _: block, page)
    headblock = HEAD[0] + "<style>" + css + "</style>" + HEAD[1]
    if HEAD[0] in page:
        page = re.sub(re.escape(HEAD[0]) + r".*?" + re.escape(HEAD[1]), lambda _: headblock, page, flags=re.S)
    else:
        page = page.replace("</head>", headblock + "\n</head>", 1)
    open(PAGE, "w", encoding="utf-8").write(page)
    print("v4 home departures: %d rows in index.html" % sec.count('<li class="sl-row'))


if __name__ == "__main__":
    main()
