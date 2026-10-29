#!/usr/bin/env python3
"""
Breakers (owner, 29 Oct 2026, style A of three mock-ups): one big photograph, edge to edge, between two sections of
a long page, fading into the page black at top and bottom, with one short line and the place. A rest for the eye
and a feel for the place before the next block of words; once a page, on the long pages only (home, Kenya, India),
from the owner's own photographs. The look is in src/v2.css (BREAKERS). Written between <!--v4br--> marks just
before the section named, so a second run writes the same bytes. Run by tools/v4_build.py after tools/v4_footer.py.

    python3 tools/v4_breakers.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
MARK = ("<!--v4br-->", "<!--/v4br-->")
# page, the section it stands before, the photograph (from the repo root, without extension), its size, alt, line, place,
# and the point of the photograph that stays in a narrow crop (the wing)
BREAKERS = [
    ("index.html", "listen", "assets/images/himalayas-1", 1600, 1200, "Paraglider over snow-capped Himalayan peaks", "Touch The Sky With Glory", "Himalaya", "30% 35%"),
    ("destinations/kenya.html", "dates", "assets/destinations/kenya/gallery/kerio-valley", 1152, 768, "Paragliders over the green slopes of the Kerio Valley", "Six Sites Down The Rift", "Kerio Valley, Kenya", "70% 50%"),
    ("destinations/india.html", "dates", "assets/destinations/india/gallery/front-range", 1400, 933, "A pilot flying along the forested front range, snow peaks behind", "Along The Front Range", "Dhauladhar, India", "22% 45%"),
]


def block(rel, src, w, h, alt, line, place, focus):
    up = "../" * (rel.count("/") + 2)
    return ('%s<div class="v4br"><picture><source srcset="%s%s.webp" type="image/webp">'
            '<img src="%s%s.jpg" width="%d" height="%d" alt="%s" loading="lazy" decoding="async" style="object-position:%s"></picture>'
            '<p class="v4br-l">%s</p><span class="v4br-p">%s</span></div>%s\n'
            % (MARK[0], up, src, up, src, w, h, alt, focus, line, place, MARK[1]))


def main():
    for rel, before, src, w, h, alt, line, place, focus in BREAKERS:
        for ext in (".webp", ".jpg"):
            if not os.path.exists(os.path.join(ROOT, src + ext)):
                raise SystemExit("v4_breakers: missing " + src + ext)
        path = os.path.join(V4, rel)
        s = open(path, encoding="utf-8").read()
        s = re.sub(re.escape(MARK[0]) + ".*?" + re.escape(MARK[1]) + r"\n", "", s, flags=re.S)
        m = re.search(r'<section[^>]*\sid="%s"' % before, s)
        if not m:
            raise SystemExit("v4_breakers: %s has no #%s" % (rel, before))
        out = s[:m.start()] + block(rel, src, w, h, alt, line, place, focus) + s[m.start():]
        if out != open(path, encoding="utf-8").read():
            open(path, "w", encoding="utf-8").write(out)
    print("v4 breakers: %d pages" % len(BREAKERS))


if __name__ == "__main__":
    main()
