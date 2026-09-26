#!/usr/bin/env python3
"""
The v4 library, two ways (docs/v4-plan.md decision 6): a flight log and a
poster wall, from the same cards (tools/v2_library_cards.py --site v4 writes
them; prototypes/v4/v2-library.js shows, hides, sorts and pages them).

  flight log   prototypes/v4/library.html. Every episode a row in a pilot's
               log: number, date, the episode and its guest, series, length,
               chapters, in the instrument font; the whole library drawn as a
               log above it (one bar per episode, by date, as tall as it is
               long) with a stats row. 24 rows a page.
  poster wall  prototypes/v4/samples/library-wall.html (hidden sample). The
               episode stills edge to edge, the title over the picture.

The stronger one is the library; the other stays as a sample page. Every card
keeps its link, words and data; the log adds the date and guest, from
episode-meta.json.

    python3 tools/v2_library_cards.py --site v4
    python3 tools/v4_library.py
    python3 tools/v2_localize.py --site v4
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_pass as P  # noqa: E402
import v4_samples as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
PAGE = os.path.join(V4, "library.html")


def augment(card):
    """The card gains the log's columns: date, guest, series (from the data)."""
    if "ep-log-date" in card:
        return card
    slug = re.search(r'data-ep-slug="([^"]+)"', card).group(1)
    e = P.meta().get(slug, {})
    date = e.get("published", "")
    label = e.get("published_label", "")
    guest = e.get("guest", "")
    series = re.search(r'data-s="([^"]*)"', card).group(1)
    cols = ('<span class="ep-log-date">%s</span>' % (
        html.escape(label) if date else '<i class="v2-tbd">[to supply]</i>') +
        ('' if 'class="ep-tile-guest"' in card else '<span class="ep-log-guest">%s</span>' % html.escape(guest)))
    card = card.replace('<span class="ep-tile-body">', cols + '<span class="ep-tile-body">', 1)
    # the number and the length in their own columns (the same words)
    card = re.sub(r'<span class="ep-stamp">([^<]*)<i>', lambda m: '<span class="ep-stamp"><b class="ep-no">%s</b><i>' % m.group(1), card, count=1)
    card = re.sub(r'<span class="ep-foot">([^<]*)<i>', lambda m: '<span class="ep-foot"><b class="ep-ch">%s</b><i>' % m.group(1), card, count=1)
    return card


def library_log(eps):
    """The whole library as a log drawing."""
    return P.topic_log("library", eps, "library", where="in the library").replace("The library conversations", "Every conversation in the library")


def build():
    src = open(PAGE, encoding="utf-8").read()
    a, b = src.index("<!-- v2:cards -->"), src.index("<!-- /v2:cards -->")
    cards = src[a:b]
    cards = re.sub(r'<a class="ep-tile".*?</a>', lambda m: augment(m.group(0)), cards, flags=re.S)
    src = src[:a] + cards + src[b:]
    # the log's head row (decoration for sighted readers; each row carries its own words)
    if "ep-log-head" not in src:
        src = src.replace('<div class="eps v2-eps" id="eps"', '<div class="ep-log-head" aria-hidden="true"><span>No.</span><span>Date</span>'
                          '<span>Episode</span><span>Series</span><span>Length</span><span>Chapters</span></div>\n    <div class="eps v2-eps" id="eps"', 1)
    # the stats and the drawing in the hero (built once, refreshed on every run after)
    slugs = re.findall(r'data-ep-slug="([^"]+)"', cards)
    eps = [P.meta()[x] for x in slugs if x in P.meta()]
    mins = sum(P.minutes(e) for e in eps)
    chap = sum(len(e.get("chapters") or []) for e in eps)
    stats = ('<dl class="v4-stats"><div><dt>Episodes</dt><dd>%d</dd></div><div><dt>Listening</dt><dd>%dh %02dm</dd></div>'
             '<div><dt>Chapters</dt><dd>%s</dd></div><div><dt>Series</dt><dd>%d</dd></div></dl>'
             % (len(eps), mins // 60, mins % 60, format(chap, ","), len(set(e.get("series") for e in eps if e.get("series")))))
    if "v4-lib-top" in src:
        src = re.sub(r'<dl class="v4-stats">.*?</dl>', lambda _: stats, src, count=1, flags=re.S)
        src = re.sub(r'(<figure class="v4-tg-fig">).*?(</figure>)', lambda x: x.group(1) + library_log(eps) + x.group(2),
                     src, count=1, flags=re.S)
    else:
        m = re.search(r'<header class="kit-hero is-sky([^"]*)">(.*?)</header>', src, re.S)
        inner = m.group(2)
        inner = re.sub(r'(\s*</div>\s*)$', lambda x: "\n    " + stats + x.group(1), inner, count=1)
        new = '<header class="kit-hero is-sky%s v4-lib-top">%s\n  <figure class="v4-tg-fig">%s</figure>\n</header>' % (m.group(1), inner, library_log(eps))
        src = src[:m.start()] + new + src[m.end():]
    if "v4-lib-log" not in src:
        src = src.replace("<body>", '<body class="v4-lib-log">', 1)
    open(PAGE, "w", encoding="utf-8").write(src)
    # the poster wall: the same page, laid out as a wall, as a hidden sample
    wall = src.replace('<body class="v4-lib-log">', '<body class="v4-lib-wall">', 1)
    wall = re.sub(r'<title>(.*?)</title>', r'<title>Library as a poster wall (v4 sample)</title>', wall, count=1, flags=re.S)
    wall = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://paraglidingatlas.com/library.html">', wall)
    wall = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", wall, flags=re.S)
    wall = S.deeper(wall)
    os.makedirs(os.path.join(V4, "samples"), exist_ok=True)
    open(os.path.join(V4, "samples", "library-wall.html"), "w", encoding="utf-8").write(wall)
    print("v4 library: flight log (library.html), poster wall (samples/library-wall.html)")


if __name__ == "__main__":
    build()
