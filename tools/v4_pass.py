#!/usr/bin/env python3
"""
The v4 pass: v4's changes to the pages the v2 generators write.

The episode, knowledge base, topic and text pages in prototypes/v4/ are built
by the same generators as v2 (tools/v2_episode.py --site v4, tools/v2_twin.py
--site v4). Rather than branch those generators (v2 must stay byte-identical),
v4's changes to those pages live here and run after them. Idempotent.

    python3 tools/v4_pass.py                 # every v4 page
    python3 tools/v4_pass.py episodes/x.html

Rebuild order for v4:
    python3 tools/v2_episode.py --site v4 --all
    python3 tools/v2_twin.py --site v4
    python3 tools/v4_pass.py
    python3 tools/v2_localize.py --site v4
    ./build.sh

What it does
  titles   an episode's on-screen title is the short part; the rest of the
           title sits under it, smaller. Every word stays in the <h1>.
  kb fold  a knowledge base section's long paragraphs fold under "Read more";
           its title, summary line and sources stay in view.
  globe    an episode whose place is on the site's globe opens on a globe
           turned to it (tools/v4_globe.py), with its coordinates, range and
           bearing from Oslo in the instrument font.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
LONG = 50          # a big title longer than this is split
SHORT = 12         # ... but never into a head shorter than this


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def split_title(big):
    """(pre, head, tail) of an on-screen title: the head is shown large."""
    pre = ""
    # "Luc Armant talks about X" / "Bruce Goldsmith explains X": the speaker goes above
    m = re.match(r"^(.{3,40}?\b(?:talks about|explains|on))\s+(.+)$", big, re.I)
    if m and len(plain(m.group(2))) >= SHORT and re.match(r"^[A-Z]", m.group(1)) and len(plain(big)) > LONG:
        pre, big = m.group(1), m.group(2)
    if len(plain(big)) <= LONG:
        return pre, big, ""
    # the first natural break that leaves a head of a readable length
    best = None
    for sep in (": ", " - ", " – ", ", ", "? ", " | ", " #", " by ", " from ", " to ", " with ", " and ", " in the "):
        i = big.find(sep)
        while i != -1:
            head = big[:i + (1 if sep.startswith("?") else 0)]
            if SHORT <= len(plain(head)) <= LONG:
                if best is None or (i > best[0] and sep != " #"):
                    best = (i, sep)
            i = big.find(sep, i + 1)
        if best:
            break
    if not best:
        return pre, big, ""
    i, sep = best
    keep = sep.strip() if sep.strip() in ("?", ":") else ""
    head = big[:i] + keep
    tail = big[i + len(sep):]
    if sep == " #":
        tail = "#" + tail
    elif sep.strip() not in (",", ":", "-", "–", "|", "?"):
        tail = sep.strip() + " " + tail          # "by Brett Janaway" keeps its word
    return pre, head.strip(), tail.strip()


def titles(src):
    m = re.search(r'(<h1\b[^>]*>)(.*?)(</h1>)', src, re.S)
    if not m or 'class="ep2-h1"' not in m.group(2) or "ep2-pre" in m.group(2) or "is-split" in m.group(2):
        return src
    h = m.group(2)
    big = re.search(r'<span class="ep2-h1">(.*?)</span>', h, re.S)
    pre, head, tail = split_title(big.group(1))
    if not pre and not tail:
        return src
    new = '<span class="ep2-h1 is-split">%s</span>' % head
    if pre:
        new = '<span class="ep2-pre">%s</span> ' % pre + new
    h2 = h.replace(big.group(0), new, 1)
    if tail:
        sub = re.search(r'<span class="ep2-sub">(.*?)</span>', h2, re.S)
        if sub:
            h2 = h2.replace(sub.group(0), '<span class="ep2-sub">%s &middot; %s</span>' % (tail, sub.group(1)), 1)
        else:
            h2 = h2.replace(new, new + ' <span class="ep2-sub">%s</span>' % tail, 1)
    # the "with <name>" line says the name twice when the speaker line already does
    w = re.search(r'<span class="ep2-with">with <strong>(.*?)</strong></span>\s*', h2, re.S)
    if pre and w and plain(w.group(1)).split()[0] in plain(pre):
        h2 = h2.replace(w.group(0), "", 1)
    return src[:m.start(2)] + h2 + src[m.end(2):]


def kb_fold(src):
    """A knowledge base section shows its title and its one-line summary; the
    long paragraphs fold under "Read more" (still in the HTML). The sources
    (the "From" chips) stay in view."""
    def one(m):
        body = m.group(2)
        if not body.strip() or "v4-fold" in body:
            return m.group(0)
        return (m.group(1) + '<details class="v4-fold k-more"><summary>Read more</summary>' +
                body + '</details>' + m.group(3))
    return re.sub(r'(<div class="r">)(.*?)(<div class="chips">)', one, src, flags=re.S)


_pins = None


def pins():
    """The site's own globe pins (globe-episodes.js): slug -> the pin."""
    global _pins
    if _pins is None:
        src = open(os.path.join(ROOT, "globe-episodes.js"), encoding="utf-8").read()
        import json
        _pins = json.loads(src[src.index("{"):src.rindex("}") + 1])
    return _pins


def episode_globe(rel, src):
    """An episode whose story has a place on the site's globe opens on a globe
    turned to it; the others keep the usual opening. The pin, the range and
    the bearing are the podcast globe's own (from Oslo, as its popup says)."""
    if "v4-globe-wrap" in src:
        return src
    slug = rel.split("/")[-1][:-5]
    p = pins().get(slug)
    if not p or p.get("home"):
        return src
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import v4_globe as G
    lat, lon = p["lat"], p["lon"]
    ns, ew = ("N" if lat >= 0 else "S"), ("E" if lon >= 0 else "W")
    coord = "%.2f\u00b0%s %.2f\u00b0%s" % (abs(lat), ns, abs(lon), ew)
    title = "A globe turned to %s, where this episode is from" % coord
    desc = "The episode's pin on the podcast globe, %s, %s km %s of Oslo." % (coord, format(p["km"], ","), p["card"])
    svg = G.globe(lat, lon, slug[:24], title, desc)
    block = '\n  <div class="v4-globe-wrap">%s</div>' % svg
    line = '<p class="v4-coord"><span>%s</span><span>%s km %s of Oslo</span></p>' % (coord, format(p["km"], ","), p["card"])
    src = src.replace('<header class="cd-head">', '<header class="cd-head v4-has-globe">' + block, 1)
    src = re.sub(r'(<p class="cd-epno">.*?</p>)', lambda m: m.group(1) + "\n    " + line, src, count=1, flags=re.S)
    return src


_meta = None


def meta():
    global _meta
    if _meta is None:
        import json
        _meta = {e["slug"]: e for e in json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))}
    return _meta


def minutes(e):
    m = re.match(r"(\d+)", e.get("duration_label") or "")
    return int(m.group(1)) if m else 0


def topic_log(name, eps, ident):
    """The topic's conversations as a log: one bar per episode, placed by its
    publish date, as tall as it is long. Real dates, real lengths."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import datetime as dt
    import v4_draw as K
    dated = [(dt.date.fromisoformat(e["published"]), minutes(e), e) for e in eps if e.get("published")]
    if len(dated) < 2:
        return ""
    W, H = 640, 300
    x0, x1, yb, yt = 40, 610, 236, 46
    d0 = dt.date(min(x[0] for x in dated).year, 1, 1)
    d1 = dt.date(max(x[0] for x in dated).year + 1, 1, 1)
    span = (d1 - d0).days
    X = lambda day: x0 + (x1 - x0) * (day - d0).days / span
    top = max(x[1] for x in dated) or 1
    Y = lambda m: yb - (yb - yt) * m / top
    und = len(eps) - len(dated)
    d = K.Drawing(W, H, "tg-" + ident, "The %s conversations by date and length" % name, inline_css=False, desc=
                  ("Each bar is one of the %d conversations tagged %s, placed by the date it was published and as tall as it "
                  "is long; the longest is %d minutes.%s" % (len(eps), name, top,
                  (" %d has no publish date and is not drawn." % und) if und else "")))
    d.backdrop(glow=((x0 + x1) / 2, yb - 70), glow_r=200, sheet=False)
    d.line((x0, yb), (x1, yb), "outline")
    y = d0.year
    while dt.date(y, 1, 1) <= d1:
        xx = X(dt.date(y, 1, 1))
        d.line((xx, yb), (xx, yb + 8), "hair")
        if dt.date(y, 1, 1) < d1:
            d.text((xx + 4, yb + 22), str(y), "sub")
        for q in (4, 7, 10):
            if dt.date(y, q, 1) < d1:
                qx = X(dt.date(y, q, 1))
                d.line((qx, yb), (qx, yb + 4), "hair")
        y += 1
    longest = max(dated, key=lambda x: x[1])
    # every bar in one path and every top in another (a round cap on a zero
    # length segment is a dot): the same drawing in a fraction of the bytes
    bars, tops = [], []
    for day, m, e in sorted(dated, key=lambda x: x[0]):
        if e is longest[2]:
            continue
        xx = X(day)
        bars.append("M%s %sV%s" % (K.f(xx), K.f(yb), K.f(Y(m))))
        tops.append("M%s %sh0" % (K.f(xx), K.f(Y(m))))
    d.raw('<path class="d" d="%s"/>' % "".join(bars))
    d.raw('<path d="%s" stroke="#f6f4f4" stroke-width="4.4" stroke-linecap="round" fill="none"/>' % "".join(tops))
    lx0 = X(longest[0])
    d.line((lx0, yb), (lx0, Y(longest[1])), "accent")
    d.dot((lx0, Y(longest[1])), 2.2, accent=True)
    # the one dimension: the longest, in minutes
    lx = X(longest[0])
    d.line((x0 - 8, Y(longest[1])), (lx - 6, Y(longest[1])), "ghost")
    d.text((x0 - 8, Y(longest[1]) - 6), "%d min" % longest[1], "val")
    d.text((x1, yt - 22), "Minutes", "sub", "end")
    return d.svg("v4-tg-log")


def topic_page(rel, src):
    """A topic opens like the knowledge base: a drawing and a stats row; the
    three newest conversations lead as a featured row."""
    if "v4-tg-top" in src:
        return src
    slugs = re.findall(r'<a class="tg-ep-link" href="\.\./episodes/([^"]+)\.html"', src)
    eps = [meta()[x] for x in slugs if x in meta()]
    if not eps:
        return src
    name = re.sub(r"<[^>]+>", "", re.search(r"<h1>(.*?)</h1>", src, re.S).group(1)).lstrip("#").strip()
    mins = sum(minutes(e) for e in eps)
    chap = sum(len(e.get("chapters") or []) for e in eps)
    series = len(set(e.get("series") for e in eps if e.get("series")))
    stats = ('<dl class="v4-stats">'
             '<div><dt>Conversations</dt><dd>%d</dd></div>'
             '<div><dt>Listening</dt><dd>%dh %02dm</dd></div>'
             '<div><dt>Chapters</dt><dd>%d</dd></div>'
             '<div><dt>Series</dt><dd>%d</dd></div></dl>') % (len(eps), mins // 60, mins % 60, chap, series)
    log = topic_log(name, eps, rel.split("/")[-1][:-5])
    src = src.replace('<header class="kit-hero is-sky v2-tg-hero">', '<header class="kit-hero is-sky v2-tg-hero v4-tg-top">', 1)
    src = re.sub(r'(<p class="kit-intro">.*?</p>)(\s*</div>)', lambda m: m.group(1) + "\n  " + stats + m.group(2) +
                 ('\n  <figure class="v4-tg-fig">%s</figure>' % log if log else ""), src, count=1, flags=re.S)
    # the featured row: the three newest, larger
    items = re.findall(r'<li class="tg-ep"[^>]*data-date="([^"]*)"[^>]*>(.*?)</li>', src, re.S)
    items = sorted([i for i in items if i[0]], key=lambda i: i[0], reverse=True)[:3]
    if len(items) == 3:
        cards = ""
        for date, body in items:
            a = re.search(r'<a class="tg-ep-link" href="([^"]+)">(.*?)</a>', body, re.S)
            im = re.search(r'<span class="tg-thumb[^"]*">(.*?)</span>', a.group(2), re.S)
            img = im.group(1) if im else ""
            ser = re.search(r'<span class="tg-ep-series">(.*?)</span>', a.group(2), re.S).group(1)
            h = re.search(r"<h2>(.*?)</h2>", a.group(2), re.S).group(1)
            cards += ('<a class="v4-feat" href="%s"><span class="v4-feat-art">%s</span><span class="v4-feat-s">%s</span>'
                      '<span class="v4-feat-t">%s</span></a>' % (a.group(1), img, ser, h))
        row = ('\n<section class="v4-feat-row" aria-label="Newest"><div class="kit-in"><span class="kit-kicker">Newest</span>'
               '<div class="v4-feat-grid">%s</div></div></section>\n' % cards)
        src = src.replace('<p class="tg-answer">', row + '<p class="tg-answer">', 1)
    return src


# "Fly it yourself" (step 5): an episode whose place is within reach of a trip
# links to it. The trips' places and next dates as the site states them.
TRIPS = [("India", "Bir Billing", (32.04, 76.72), "21 to 30 Oct 2026", "destinations/india.html"),
         ("Kenya", "Kerio Valley", (0.72, 35.65), "18 to 29 Jan 2027", "destinations/kenya.html")]


def km(a, b):
    import math
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(h))


def episode_extras(rel, src):
    """The phone bar (Play, Next) and, where the place is a trip's, the bridge."""
    slug = rel.split("/")[-1][:-5]
    if "v4-epbar" not in src:
        nxt = re.search(r'<a class="ep2-card" href="([^"]+)">.*?<span class="ep2-card-t">(.*?)</span>', src, re.S)
        bar = '\n<div class="v4-epbar" id="v4Epbar"><button type="button" class="btn-solid v4-play"><span>Play</span></button>'
        if nxt:
            bar += '<a class="btn-lines v4-next" href="%s"><span class="v4-next-k">Next</span> %s</a>' % (nxt.group(1), nxt.group(2))
        bar += "</div>\n"
        src = src.replace("</div><!-- /.page-wrap -->", bar + "</div><!-- /.page-wrap -->", 1)
    p = pins().get(slug)
    if p and not p.get("home") and "v4-bridge" not in src:
        for name, place, at, when, href in TRIPS:
            if km((p["lat"], p["lon"]), at) < 400:
                link = '<a class="v4-bridge" href="../%s"><span>Fly it yourself</span> %s, %s <i aria-hidden="true">&rarr;</i></a>' % (href, place, when)
                src = src.replace('</p>', '</p>', 1)
                src = re.sub(r'(<p class="v4-coord">.*?</p>)', lambda m: m.group(1) + "\n    " + link, src, count=1, flags=re.S)
                break
    return src


TEXT_PAGES = ("terms.html", "privacy-policy.html", "cookie-policy.html", "participant-agreement.html",
              "corrections.html", "safety-and-disclosure.html", "mission.html")


def next_step(rel, src):
    """Every page ends on one clear next step (step 5), in words the site
    already uses: the text pages on the call, the library on the topics, a
    topic on the library."""
    if "v4-next" in src:
        return src
    up = "../" * rel.count("/")
    if rel in TEXT_PAGES:
        band = ('<section class="v4-next"><div class="v4-next-in"><span class="kit-kicker">Ready To Touch The Sky With Glory?</span>'
                '<a class="v4-next-a" href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener">'
                'Book a free 30-minute, no obligation virtual call <i aria-hidden="true">&rarr;</i></a></div></section>')
    elif rel == "library.html":
        band = ('<section class="v4-next"><div class="v4-next-in"><span class="kit-kicker">Browse by subject</span>'
                '<a class="v4-next-a" href="tags.html">Topics <i aria-hidden="true">&rarr;</i></a></div></section>')
    elif rel.startswith("tags"):
        def conv(m):
            inner = re.sub(r'<a href="([^"]*library\.html)">', r'<a class="is-next" href="\1">', m.group(2))
            return '<div class="%s v4-next v4-next-tg" role="navigation" aria-label="Next">%s</div>' % (m.group(1), inner)
        src = re.sub(r'<p class="(tg-back[^"]*)">(.*?)</p>', conv, src, count=1, flags=re.S)
        return src
    else:
        return src
    return src.replace("</div><!-- /.page-wrap -->", band + "\n</div><!-- /.page-wrap -->", 1)


NAV = [("Expeditions", "index.html#destinations", ("destinations/", "enquire.html")),
       ("Podcast", "podcast.html", ("podcast.html", "library.html", "episodes/", "tags", "samples/library")),
       ("Knowledge Base", "knowledge-base.html", ("knowledge-base",)),
       ("About", "about.html", ("about.html", "mission.html", "partners.html"))]


def nav(rel, src):
    """The header (owner's decision 5): Expeditions, Podcast, Knowledge Base,
    About, then Enquire. Sitemap is in the footer. The current section is
    marked (aria-current)."""
    m = re.search(r'<div class="nav-links">.*?</div>', src, re.S)
    if not m or "v4-nav" in m.group(0):
        return src
    up = "../" * rel.count("/")
    items = []
    for i, (label, href, starts) in enumerate(NAV):
        here = any(rel.startswith(x) for x in starts)
        items.append('<a href="%s%s"%s>%s</a>' % (up, href, ' aria-current="page" class="is-here"' if here else "", label))
    new = '<div class="nav-links v4-nav">\n    ' + '\n    <span class="nav-sep">|</span>\n    '.join(items) + "\n  </div>"
    return src[:m.start()] + new + src[m.end():]


def main(args):
    rels = args or sorted(os.path.relpath(os.path.join(d, f), V4).replace(os.sep, "/")
                          for d, _, fs in os.walk(V4) for f in fs if f.endswith(".html"))
    n = {"titles": 0, "kb folds": 0, "globes": 0, "topics": 0, "nav": 0}
    for rel in rels:
        fp = os.path.join(V4, rel)
        src = open(fp, encoding="utf-8").read()
        out = next_step(rel, nav(rel, src))
        if rel.startswith("episodes/"):
            out = titles(out)
            n["titles"] += out != src
            g = episode_globe(rel, out)
            n["globes"] += g != out
            out = episode_extras(rel, g)
        if rel.startswith("tags/"):
            t = topic_page(rel, out)
            n["topics"] += t != out
            out = t
        if rel.startswith("knowledge-base/"):
            before = out
            out = kb_fold(out)
            n["kb folds"] += out.count('class="v4-fold k-more"') if out != before else 0
        n["nav"] += 'class="nav-links v4-nav"' in out and 'class="nav-links v4-nav"' not in src
        if out != src:
            open(fp, "w", encoding="utf-8").write(out)
    print("v4 pass: " + ", ".join("%s %d" % kv for kv in n.items()))


if __name__ == "__main__":
    main(sys.argv[1:])
