#!/usr/bin/env python3
"""
The trip pages' gallery as a fly-through (owner, 1 Oct 2026: "a", from the
three gallery options). In place of the cover-flow carousel: the section holds
still while the photographs pass one at a time, full screen, each drifting
slowly closer; its caption comes up from below, a counter says which frame,
and a gold line along the foot fills as the reader goes. A "Skip the
pictures" link jumps past it.

The photographs, their order, captions and alt text are the ones each page
already carries (the old cards' data-title and alt). A photograph without a
title shows its number only. The behaviour is v2-immersive.js part 14 and the
look is in v2.css (THE FLY-THROUGH). Reduced motion or no script: a plain
column of photographs with their captions.

    python3 tools/v4_flythrough.py      # rewrites #gallery on the India and Kenya pages (idempotent)
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
PAGES = ["destinations/india.html", "destinations/kenya.html"]


def esc(s):
    return html.escape(s, quote=True)


def section(src):
    i = src.index('id="gallery"')
    i = src.rindex("<section", 0, i)
    j = src.index("</section>", i) + len("</section>")
    return i, j, src[i:j]


def frames_from_cards(sec):
    out = []
    for title, inner in re.findall(r'<button type="button" class="cfl-card" data-title="([^"]*)"[^>]*>(.*?)</button>', sec, re.S):
        img = re.search(r"<img[^>]*>", inner).group(0)
        wh = re.search(r'width="(\d+)" height="(\d+)"', img)
        out.append(dict(title=html.unescape(title), alt=html.unescape(re.search(r'alt="([^"]*)"', img).group(1)),
                        webp=re.search(r'<source srcset="([^"]+)"', inner).group(1), jpg=re.search(r' src="([^"]+)"', img).group(1),
                        w=int(wh.group(1)) if wh else 1400, h=int(wh.group(2)) if wh else 933))
    return out


def frames_from_flythrough(sec):
    out = []
    for m in re.finditer(r'<figure class="gxa-f[^"]*"[^>]*data-title="([^"]*)">(.*?)</figure>', sec, re.S):
        title, inner = m.group(1), m.group(2)
        img = re.search(r"<img[^>]*>", inner).group(0)
        wh = re.search(r'width="(\d+)" height="(\d+)"', img)
        out.append(dict(title=html.unescape(title), alt=html.unescape(re.search(r'alt="([^"]*)"', img).group(1)),
                        webp=re.search(r'<source srcset="([^"]+)"', inner).group(1), jpg=re.search(r' src="([^"]+)"', img).group(1),
                        w=int(wh.group(1)), h=int(wh.group(2))))
    return out


def build(fs, kicker, h2, after):
    n = len(fs)
    figs = ""
    for k, f in enumerate(fs):
        cap = '<span class="gxa-n">%02d</span>' % (k + 1)
        if f["title"]:
            cap += "<b>%s</b>" % esc(f["title"])
            if f["alt"] and f["alt"].strip().lower() != f["title"].strip().lower():
                cap += '<span class="gxa-alt">%s</span>' % esc(f["alt"])
        figs += ('<figure class="gxa-f%s" data-title="%s"><picture><source srcset="%s" type="image/webp">'
                 '<img src="%s" alt="%s" width="%d" height="%d"%s decoding="async"></picture><figcaption>%s</figcaption></figure>'
                 % (" is-on" if k == 0 else "", esc(f["title"]), f["webp"], f["jpg"], esc(f["alt"]), f["w"], f["h"],
                    "" if k < 2 else ' loading="lazy"', cap))
    ticks = "".join('<i style="left:%.3f%%"></i>' % (100 * k / max(1, n - 1)) for k in range(n))
    return ('<section class="dst-sec gxa" id="gallery" aria-labelledby="gallery-h" style="--n:%d">\n'
            '  <div class="gxa-track"><div class="gxa-pin">\n    %s\n'
            '    <div class="gxa-head"><span class="kicker">%s</span><h2 id="gallery-h">%s</h2></div>\n'
            '    <div class="gxa-count" aria-hidden="true"><b>01</b> / %02d</div>\n'
            '    <div class="gxa-rail" aria-hidden="true"><span class="gxa-fill"></span>%s</div>\n'
            '    <a class="gxa-skip" href="#%s">Skip the pictures <i aria-hidden="true">&darr;</i></a>\n'
            '  </div></div>\n</section>' % (n, figs, esc(kicker), esc(h2), n, ticks, after))


def main():
    for rel in PAGES:
        p = os.path.join(V4, rel)
        src = open(p, encoding="utf-8").read()
        i, j, sec = section(src)
        fs = frames_from_cards(sec) or frames_from_flythrough(sec)
        head = re.search(r'<span class="kicker">([^<]*)</span>\s*<h2 id="gallery-h">([^<]*)</h2>', sec)
        nxt = re.search(r'<section[^>]*\sid="([^"]+)"', src[j:])
        new = build(fs, html.unescape(head.group(1)), html.unescape(head.group(2)), nxt.group(1) if nxt else "dates")
        src = src[:i] + new + src[j:]
        src = re.sub(r'<script defer src="\.\./kenya-gallery\.js[^"]*"></script>\s*', "", src)
        open(p, "w", encoding="utf-8").write(src)
        print("v4 fly-through: %s, %d frames, skips to #%s" % (rel, len(fs), nxt.group(1) if nxt else "dates"))


if __name__ == "__main__":
    main()
