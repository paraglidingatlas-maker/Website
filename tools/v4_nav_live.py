#!/usr/bin/env python3
"""
The header's slot after Speed Record: "Live from SRS" while a comp the owner covers is running (owner, 9 Nov 2026:
"a small yet subtle cue in the nav bar saying live from SRS so people can navigate to the media"), and otherwise
the SRS 2027 race calendar (owner, 23 Nov 2026: "put this online and put the lable in the place next instead of
srs lvie").

Live: a pulsing orange dot and the words, linking to that comp's gallery, only while today is within LIVE's dates
(the comp, plus a few days for the last photos); it leaves by itself at the next build after that.
Otherwise STAND: a small calendar mark (no dot, nothing pulses: nothing is live) and "SRS 2027 Calendar", linking
to srs-2027-calendar.html (tools/v4_srs_calendar.py). Either way the words shorten on narrower screens ("Live",
"Calendar"), then the mark alone; the phone's full-screen menu (src/v4-menu.js) carries the same item with the
header's own mark and words (data-sub, when there is one, is its second line there).

Same marks idea as tools/v4_nav_record.py; a second run writes the same bytes. It runs in tools/v4_build.py after
v4_nav_record; owned pages (samples/**, record-*, expeditions*, media*, srs-*) keep what a hand run wrote, so run
this by hand after their generators and commit them.

The translated pages (tools/v4_i18n.py): the item's words are segments like any other, so a NEW label needs its
translations in tools/data/i18n/<lang>.json before the build, or the home and Enquire lose their languages.

    python3 tools/v4_nav_live.py
"""
import datetime
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
LIVE = {"page": "media-srs-tapalpa-2026.html", "label": "Live from SRS", "short": "Live",
        "title": "Live from SRS: the photos and videos", "sub": "Tapalpa, Mexico &middot; photos and videos",
        "first": datetime.date(2026, 11, 7), "last": datetime.date(2026, 11, 17)}
# the slot when nothing is live (owner, 23 Nov 2026); None leaves it empty. The title is the label, so the
# translations need one string less.
STAND = {"page": "srs-2027-calendar.html", "label": "SRS 2027 Calendar", "short": "Calendar", "title": "SRS 2027 Calendar",
         "mark": '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><rect x="2" y="3.5" width="12" height="10.5" rx="1.5"/>'
                 '<path d="M2 7.2h12M5.5 1.8v3M10.5 1.8v3"/></svg>'}
OPEN, CLOSE = "<!-- v4:live -->", "<!-- /v4:live -->"
BLOCK = re.compile(r'(<div class="nav-links v4-nav">)(.*?)(\s*</div>)', re.S)
MINE = re.compile(r'\s*' + re.escape(OPEN) + r'.*?' + re.escape(CLOSE), re.S)


def item(rel, it):
    up = "../" * rel.count("/")
    here = rel == it["page"]
    return ('\n    %s<span class="nav-sep">|</span>\n    <a class="v4-live%s%s" href="%s%s" title="%s"%s%s>'
            '%s<span class="v4-live-l">%s</span><span class="v4-live-s" aria-hidden="true">%s</span></a>%s'
            % (OPEN, " v4-cal" if "mark" in it else "", " is-here" if here else "", up, it["page"], it["title"],
               ' data-sub="%s"' % it["sub"] if it.get("sub") else "", ' aria-current="page"' if here else "",
               it.get("mark", '<i aria-hidden="true"></i>'), it["label"], it["short"], CLOSE))


def main(today=None):
    today = today or datetime.date.today()
    it = LIVE if LIVE["first"] <= today <= LIVE["last"] else STAND
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
            inner = MINE.sub("", m.group(2)) + (item(rel, it) if it else "")
            out = src[:m.start()] + m.group(1) + inner + m.group(3) + src[m.end():]
            if out != src:
                with open(p, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(out)
            n += 1
    print("v4_nav_live: %s on %d pages" % (it["label"] if it else "an empty slot", n))


if __name__ == "__main__":
    main()
