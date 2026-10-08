#!/usr/bin/env python3
"""
The owner's flying footage in v4 (owner, 4 Oct 2026: "I want the
immersiveness to the max").

The twelve clips the owner gave on 3 Oct are encoded in assets/video/alps-N
(1080p and 720p, WebM and MP4, a still each; tools/v6_build.py). They play
through the site's own looping footage code (script.js, LOOPING FOOTAGE): only
on screen, never for reduced motion, Save-Data or a slow connection, fading in
over the still.

Where they go (owner, 4 Oct: "dont overdo video if a still photo looks more
elegant than let it be"). Video only where the motion is the point:
  - film strips before the questions on Meteorology (climbing out of cloud,
    its still the moment the valley opens), Risk vs Reward (soaring along a
    cliff) and Flight Mechanics (straight down the lines);
  - stills, no video: Weather Patterns (the cloud wall), behind the Mission
    header (the limestone peaks), and the About header (above the glacier,
    in place of the Himalaya loop it shared with the India page);
  - nothing behind the homepage's Why band or the Enquire header: both carry
    a form, which reads better on the plain page.

Then (owner, 8 Oct 2026, after seeing them with a climb of cloud before
each: "remove these videos entirely from these pages ... only let them
remain in the tour" pages): the four knowledge base film strips are taken
out, as the podcast's breather is (by hand, its line kept on the page). The
footage plays on the trips and the home page only; the stills behind the
Mission and About headers stay.

Captions and alt text: only what is visible. Where the clips were filmed is
not known yet, so nothing names a place.

Also fixed here: the podcast breather's clip waited for an "is-on" class
nothing ever set, so it never played. Breathers play on screen like any loop.

    python3 tools/v4_footage.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")

# page -> (clip, kind, anchor the block goes before (strip) or inside (bg), still)
# still: None for the clip's own first frame, or a frame of it in prototypes/v4/img/
PLAN = {
    "mission.html": (12, "bg-still", '<header class="kit-hero is-sky v2-page-hero">', None),
}
# pages that carried footage in the first pass (4 Oct) and no longer do; the knowledge base's from 8 Oct
CLEAR = {"enquire.html": '<header class="kit-hero is-sky v2-page-hero">',
         "index.html": '<section class="kit-band v2-join v2-topo">',
         "knowledge-base/meteorology.html": '<section class="k-sec card"',
         "knowledge-base/weather-patterns.html": '<section class="k-sec card"',
         "knowledge-base/risk-vs-reward.html": '<section class="k-sec card"',
         "knowledge-base/flight-mechanics.html": '<section class="k-sec card"'}
# the About header: a still of clip 2 in place of the photograph and loop it shared with India
ABOUT_OLD = ('<picture><source srcset="../../assets/images/himalayas-1.webp" type="image/webp"><img src="../../assets/images/himalayas-1.jpg" alt="Paraglider over the Himalayas" fetchpriority="high"></picture>\n'
             '    <video data-loop="../../assets/video/bir" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>')
# (first the clip 2 frame of a pilot in an ATLAS harness; his helmet names someone
#  else, and an About Me page should not open on another person: the glacier instead)
ABOUT_V1 = ('<picture><source srcset="img/alps-2-still.webp" type="image/webp"><img src="img/alps-2-still.jpg" width="1920" height="1080" '
            'alt="A pilot in an ATLAS harness above a green valley" fetchpriority="high"></picture>')
ABOUT_NEW = ('<picture><source srcset="img/alps-11-still.webp" type="image/webp"><img src="img/alps-11-still.jpg" width="1920" height="1080" '
             'alt="Flying above a glacier, the wing tip in view" fetchpriority="high"></picture>')
START, END = "<!-- v4-footage -->", "<!-- /v4-footage -->"


def media(rel, n, still=None, video=True):
    up = os.path.relpath(ROOT, os.path.join(V4, os.path.dirname(rel))).replace(os.sep, "/")
    base = "%s/assets/video/alps-%d" % (up, n)
    if still:
        here = os.path.relpath(os.path.join(V4, "img"), os.path.join(V4, os.path.dirname(rel))).replace(os.sep, "/")
        img = ('<picture><source srcset="%s/%s.webp" type="image/webp"><img src="%s/%s.jpg" alt="" loading="lazy" decoding="async"></picture>'
               % (here, still, here, still))
    else:
        img = '<img src="%s-poster.jpg" alt="" loading="lazy" decoding="async">' % base
    if not video:
        return img
    return img + ('<video data-loop="%s" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>' % base)


def strip(html, anchor):
    html = re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)
    return html.replace(anchor[:-1] + " data-v4-footage>", anchor)


def main():
    for rel, (n, kind, anchor, still) in PLAN.items():
        p = os.path.join(V4, rel)
        html = strip(open(p, encoding="utf-8").read(), anchor)
        if anchor not in html:
            raise SystemExit("v4_footage: %s: anchor not found" % rel)
        moving = not kind.endswith("-still")
        body = media(rel, n, still, moving)
        if kind.startswith("strip"):
            block = START + '<section class="v4-breather v4-film" aria-hidden="true"><div class="v4-br-media">%s</div></section>' % body + END
            html = html.replace(anchor, block + anchor, 1)
        else:
            block = START + '<div class="v4-bg" aria-hidden="true">%s<span class="v4-bg-shade"></span></div>' % body + END
            html = html.replace(anchor, anchor[:-1] + " data-v4-footage>" + block, 1)
        open(p, "w", encoding="utf-8").write(html)
        print("v4_footage: %-40s clip %d (%s)" % (rel, n, kind))
    for rel, anchor in CLEAR.items():
        p = os.path.join(V4, rel)
        html = open(p, encoding="utf-8").read()
        new = strip(html, anchor)
        if new != html:
            open(p, "w", encoding="utf-8").write(new)
            print("v4_footage: %-40s footage taken out" % rel)
    p = os.path.join(V4, "about.html")
    html = open(p, encoding="utf-8").read()
    if ABOUT_OLD in html or ABOUT_V1 in html:
        open(p, "w", encoding="utf-8").write(html.replace(ABOUT_OLD, ABOUT_NEW, 1).replace(ABOUT_V1, ABOUT_NEW, 1))
        print("v4_footage: about.html                               still of clip 2")
    elif "img/alps-11-still." not in html:          # (tools/v4_ux.py then gives it a phone cut: still clip 11's)
        raise SystemExit("v4_footage: about.html: hero not found")
    # the podcast breather plays on screen, like every other loop
    p = os.path.join(V4, "podcast.html")
    html = open(p, encoding="utf-8").read()
    new = html.replace(' data-loop-when=".v4-breather"', "")
    if new != html:
        open(p, "w", encoding="utf-8").write(new)
        print("v4_footage: podcast breather now plays")


if __name__ == "__main__":
    main()
