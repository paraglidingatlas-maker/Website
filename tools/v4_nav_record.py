#!/usr/bin/env python3
"""
The record attempt in the header (owner, 20 Oct 2026: "b9 is final, push it
live and connect the page"). From a sheet of twelve mock-ups the owner chose
B9: three short speed streaks in orange before "Speed Record", the fifth item
of the header's menu, after About, linking to record-attempt.html.

This writes that item into the header of every v4 page that has one
(<div class="nav-links v4-nav">), at the end of the menu, between
<!-- v4:needs record-attempt.html --> and <!-- /v4:needs --> with its
separator: the record page is prototype-only (tools/v2_site.py PROTO_ONLY)
until the owner's go, so the switch-over (tools/v2_switch.py) drops the item
whole while that page is not switched, and keeps it, unmarked, once it is.
On the record page and its option pages the item is the current one
(aria-current, is-here). A second run writes the same bytes.

The look is in src/v2.css (THE RECORD ATTEMPT IN THE HEADER); the phone's
full-screen menu (src/v4-menu.js) shows the same item when, and only when,
the header carries it, so it goes with the header item at the switch-over.

It runs in tools/v4_build.py after v4_ux. The pages their own generators own
(samples/**, record-*.html, expeditions*.html) are put back by v4_build as
committed, so they carry the item as this wrote it when it was run by hand;
after running one of those generators by hand, run this again.

    python3 tools/v4_nav_record.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")

OPEN, CLOSE = "<!-- v4:needs record-attempt.html -->", "<!-- /v4:needs -->"
STREAKS = ('<svg viewBox="0 0 16 10" aria-hidden="true" focusable="false">'
           '<path d="M6 1.5h9"/><path d="M2 5h13"/><path d="M8 8.5h7"/></svg>')
BLOCK = re.compile(r'(<div class="nav-links v4-nav">)(.*?)(\s*</div>)', re.S)
MINE = re.compile(r'\s*' + re.escape(OPEN) + r'<span class="nav-sep">\|</span>.*?' + re.escape(CLOSE), re.S)


def item(rel):
    up = "../" * rel.count("/")
    here = re.fullmatch(r"record-(?:attempt|[a-z])\.html", rel)
    return ("\n    " + OPEN + '<span class="nav-sep">|</span>\n    <a class="v4-wr%s" href="%srecord-attempt.html" title="Speed Record"%s>%sSpeed Record</a>'
            % (" is-here" if here else "", up, ' aria-current="page"' if here else "", STREAKS) + CLOSE)


def main():
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
            inner = MINE.sub("", m.group(2)) + item(rel)
            out = src[:m.start()] + m.group(1) + inner + m.group(3) + src[m.end():]
            if out != src:
                with open(p, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(out)
            n += 1
    print("v4_nav_record: the record attempt in the header of %d pages" % n)


if __name__ == "__main__":
    main()
