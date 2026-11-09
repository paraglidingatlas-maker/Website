#!/usr/bin/env python3
"""
"Live from SRS" in the header while a comp the owner covers is running (owner, 9 Nov 2026: "a small yet subtle
cue in the nav bar saying live from SRS so people can navigate to the media"). A pulsing orange dot and the words,
after Speed Record, linking to that comp's gallery; on narrower screens "Live" alone, then the dot alone. The phone's
full-screen menu (src/v4-menu.js) carries the same item when the header does.

It goes in only while today is within LIVE's dates (the comp, plus a few days for the last photos), so it leaves the
site by itself at the next build after that. Same marks idea as tools/v4_nav_record.py; a second run writes the
same bytes. It runs in tools/v4_build.py after v4_nav_record; owned pages (samples/**, record-*, expeditions*,
media*) keep what a hand run wrote, so run this by hand after their generators and commit them.

    python3 tools/v4_nav_live.py
"""
import datetime
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
LIVE = {"page": "media-srs-tapalpa-2026.html", "label": "Live from SRS", "short": "Live",
        "first": datetime.date(2026, 11, 7), "last": datetime.date(2026, 11, 17)}
OPEN, CLOSE = "<!-- v4:live -->", "<!-- /v4:live -->"
BLOCK = re.compile(r'(<div class="nav-links v4-nav">)(.*?)(\s*</div>)', re.S)
MINE = re.compile(r'\s*' + re.escape(OPEN) + r'.*?' + re.escape(CLOSE), re.S)


def item(rel):
    up = "../" * rel.count("/")
    here = rel == LIVE["page"]
    return ('\n    %s<span class="nav-sep">|</span>\n    <a class="v4-live%s" href="%s%s" title="%s: the photos and videos"%s>'
            '<i aria-hidden="true"></i><span class="v4-live-l">%s</span><span class="v4-live-s" aria-hidden="true">%s</span></a>%s'
            % (OPEN, " is-here" if here else "", up, LIVE["page"], LIVE["label"], ' aria-current="page"' if here else "",
               LIVE["label"], LIVE["short"], CLOSE))


def main(today=None):
    today = today or datetime.date.today()
    on = LIVE["first"] <= today <= LIVE["last"]
    n = 0
    for d, dirs, fs in os.walk(V4):
        dirs[:] = [x for x in dirs if x != "src"]
        for f in fs:
            if not f.endswith(".html"):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, V4).replace(os.sep, "/")
            src = open(p, encoding="utf-8").read()
            m = BLOCK.search(src)
            if not m:
                continue
            inner = MINE.sub("", m.group(2)) + (item(rel) if on else "")
            out = src[:m.start()] + m.group(1) + inner + m.group(3) + src[m.end():]
            if out != src:
                with open(p, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(out)
            n += 1
    print("v4_nav_live: %s on %d pages" % ("the live cue" if on else "no live cue", n))


if __name__ == "__main__":
    main()
