#!/usr/bin/env python3
"""
Write the episode cards and series filters into prototypes/v2/library.html.

The v2 library is a browser: search, series filters and paging on screen. The
cards are written into the HTML here, every one of them a real link, so a
crawler reading the page finds every episode without running a script.
prototypes/v2/v2-library.js only shows, hides, sorts and pages them.

Sources: library-data.js (LIB_TOPICS, LIB_FEATURED, LIB_EPISODES; the series
each episode sits in) and library-episodes.js (LIB_MODAL: guest, shown title,
episode number, length, chapters, video or audio). Same card as the live
library and the knowledge base series pages (.ep-tile).

    python3 tools/v2_library_cards.py
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(S.DIR, "library.html")

EXPAND = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 4H4v5"/>'
          '<path d="M15 20h5v-5"/><path d="M4 4l6 6"/><path d="M20 20l-6-6"/></svg>')


def js_object(src, name):
    m = re.search(r"const %s\s*=\s*(\{.*?\n\});" % name, src, re.S)
    body = re.sub(r"//[^\n]*", "", m.group(1))
    body = re.sub(r",\s*}", "}", body)
    return json.loads(body)


def load():
    src = open(os.path.join(ROOT, "library-data.js"), encoding="utf-8").read()
    topics = js_object(src, "LIB_TOPICS")
    featured = json.loads(re.search(r"const LIB_FEATURED\s*=\s*(\[.*?\]);", src).group(1))
    eps = []
    for m in re.finditer(r'\{ order: (\d+), id: "([^"]*)", page: "([^"]*)", topic: "([^"]+)", title: "((?:[^"\\]|\\.)*)" \}', src):
        eps.append(dict(order=int(m.group(1)), id=m.group(2), page=m.group(3), topic=m.group(4),
                        title=json.loads('"%s"' % m.group(5))))
    msrc = open(os.path.join(ROOT, "library-episodes.js"), encoding="utf-8").read()
    modal = json.loads(msrc[msrc.index("{"):msrc.rindex("}") + 1])
    return topics, featured, eps, modal


def norm(t):
    t = re.sub(r"[^a-z0-9 ]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def card(e, d):
    e_ = html.escape
    href = "episodes/%s.html" % e["page"] if e["page"] else "https://www.youtube.com/watch?v=%s" % e["id"]
    dur = d.get("dur", "")
    mins = re.match(r"(\d+)", dur)
    title = d.get("shownTitle") or e["title"]
    guest = d.get("shownGuest") or ""
    n = d.get("nchapters")
    chapters = ("1 chapter" if n == 1 else "%d chapters" % n) if n else '<span class="dim">No chapters yet</span>'
    audio = '<span class="ep-audio">Audio only</span>' if d and not d.get("video") else ""
    if e["id"]:
        img = "https://i.ytimg.com/vi/%s/mqdefault.jpg" % e["id"]
    else:
        art = "assets/podcast/artwork/%s.jpg" % e["page"]
        img = art if os.path.exists(os.path.join(ROOT, art)) else "assets/images/artwork-needed.png"
    find = norm(" ".join([e["title"], title, guest, e["topic"]]))
    attrs = ' data-ep-slug="%s"' % e_(e["page"]) if e["page"] else ' target="_blank" rel="noopener"'
    return (
        '<a class="ep-tile" href="%s"%s data-s="%s" data-o="%d" data-m="%s" data-f="%s">'
        '<span class="ep-stamp">%s<i>%s</i></span>'
        '<span class="ep-th"><img loading="lazy" src="%s" alt="" width="320" height="180">%s</span>'
        '<span class="ep-tile-body"><span class="ep-tile-title">%s</span>%s</span>'
        '<span class="ep-foot">%s<i>%s</i></span></a>'
    ) % (href, attrs, e_(e["topic"]), e["order"], mins.group(1) if mins else "", e_(find),
         e_(d.get("epno", "")), e_(dur), img, audio, e_(title),
         '<span class="ep-tile-guest">%s</span>' % e_(guest) if guest else "", chapters, EXPAND)


def main():
    topics, featured, eps, modal = load()
    order = featured + [k for k in topics if k not in featured]
    count = {k: sum(1 for e in eps if e["topic"] == k) for k in topics}
    chips = ['<button class="tg-chip v2-chip" type="button" data-s="" aria-pressed="true">All <i>%d</i></button>' % len(eps)]
    for k in order:
        if count[k]:
            chips.append('<button class="tg-chip v2-chip" type="button" data-s="%s" aria-pressed="false">%s <i>%d</i></button>'
                         % (html.escape(k), html.escape(k), count[k]))
    tiles = []
    for n, k in enumerate(order):
        c = count[k]
        meta = ("%d %s in %s" % (c, "episode" if c == 1 else "episodes", topics[k])) if c else "Coming soon in %s" % topics[k]
        tiles.append('<a class="tile %s%s%s" href="#s=%s" data-t="%s"><div class="shot"></div><h3>%s</h3><div class="meta">%s</div></a>'
                     % (["edge-lb", "edge-tr", "edge-b", "edge-l"][n % 4], " is-feat" if k in featured else "",
                        "" if c else " zero", html.escape(k.replace(" ", "%20")), html.escape(k), html.escape(k), meta))
    cards = "\n".join(card(e, modal.get(e["page"], {})) for e in sorted(eps, key=lambda e: e["order"]))

    page = open(PAGE, encoding="utf-8").read()
    for name, body in (("tiles", "\n".join(tiles)), ("chips", "\n".join(chips)), ("cards", cards)):
        page = re.sub(r"(<!-- v2:%s -->).*?(<!-- /v2:%s -->)" % (name, name),
                      lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), page, flags=re.S)
    page = re.sub(r'data-v2-count>[^<]*<', 'data-v2-count>%d episodes in %d series<' % (len(eps), sum(1 for k in topics if count[k])), page)
    open(PAGE, "w", encoding="utf-8").write(page)
    print("library: %d cards, %d series" % (len(eps), len(order)))


if __name__ == "__main__":
    main()
