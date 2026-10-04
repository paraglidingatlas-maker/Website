#!/usr/bin/env python3
"""
The owner's flying footage in v4 (owner, 4 Oct 2026: "I want the
immersiveness to the max").

The twelve clips the owner gave on 3 Oct are encoded in assets/video/alps-N
(1080p and 720p, WebM and MP4, a still each; tools/v6_build.py). They play
through the site's own looping footage code (script.js, LOOPING FOOTAGE): only
on screen, never for reduced motion, Save-Data or a slow connection, fading in
over the still.

Where they go, and why there:
  - a full-width film strip (the podcast page's "breather") on the four
    knowledge base pages whose subject the clip shows, before the questions:
    the headers keep their drawings, which are those pages' own moment;
  - behind the plain sky headers of Mission and Enquire;
  - behind the homepage's "Why fly with us" band.

Captions and alt text: none. The clips are decoration (aria-hidden); where
they were filmed is not known yet, so nothing names a place.

Also fixed here: the podcast breather's clip waited for an "is-on" class
nothing ever set, so it never played. Breathers play on screen like any loop.

    python3 tools/v4_footage.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")

# page -> (clip, kind, anchor the block goes before (strip) or inside (bg))
PLAN = {
    "knowledge-base/meteorology.html": (1, "strip", '<section class="k-sec card"'),
    "knowledge-base/weather-patterns.html": (4, "strip", '<section class="k-sec card"'),
    "knowledge-base/risk-vs-reward.html": (3, "strip", '<section class="k-sec card"'),
    "knowledge-base/flight-mechanics.html": (10, "strip", '<section class="k-sec card"'),
    "mission.html": (12, "bg", '<header class="kit-hero is-sky v2-page-hero">'),
    "enquire.html": (7, "bg", '<header class="kit-hero is-sky v2-page-hero">'),
    "index.html": (11, "bg", '<section class="kit-band v2-join v2-topo">'),
}
START, END = "<!-- v4-footage -->", "<!-- /v4-footage -->"


def media(rel, n):
    up = os.path.relpath(ROOT, os.path.join(V4, os.path.dirname(rel))).replace(os.sep, "/")
    base = "%s/assets/video/alps-%d" % (up, n)
    return ('<img src="%s-poster.jpg" alt="" loading="lazy" decoding="async">'
            '<video data-loop="%s" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>'
            % (base, base))


def main():
    for rel, (n, kind, anchor) in PLAN.items():
        p = os.path.join(V4, rel)
        html = open(p, encoding="utf-8").read()
        html = re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)
        marked = anchor[:-1] + " data-v4-footage>"
        html = html.replace(marked, anchor)
        if anchor not in html:
            raise SystemExit("v4_footage: %s: anchor not found" % rel)
        if kind == "strip":
            block = (START + '<section class="v4-breather v4-film" aria-hidden="true"><div class="v4-br-media">%s</div></section>' % media(rel, n) + END)
            html = html.replace(anchor, block + anchor, 1)
        else:
            block = START + '<div class="v4-bg" aria-hidden="true">%s<span class="v4-bg-shade"></span></div>' % media(rel, n) + END
            html = html.replace(anchor, marked + block, 1)
        open(p, "w", encoding="utf-8").write(html)
        print("v4_footage: %-40s clip %d (%s)" % (rel, n, kind))
    # the podcast breather plays on screen, like every other loop
    p = os.path.join(V4, "podcast.html")
    html = open(p, encoding="utf-8").read()
    new = html.replace(' data-loop-when=".v4-breather"', "")
    if new != html:
        open(p, "w", encoding="utf-8").write(new)
        print("v4_footage: podcast breather now plays")


if __name__ == "__main__":
    main()
