#!/usr/bin/env python3
"""
India's departures move to 2027 across v4 (owner, 24 Oct 2026: "move dates of india to 15th april for the first tour
and then 1 day later the next one", then "keep the older india dates for 2027 so make that tour visible as well
accordingly everywhere needed"). Four departures of ten days, as the home opening already shows them:

    Tour 1  15 to 24 Apr 2027      Tour 3  21 to 30 Oct 2027
    Tour 2  25 Apr to 4 May 2027   Tour 4  3 to 12 Nov 2027

This rewrites the v4 pages that state India's 2026 dates (the India page's dates, strap, FAQ and structured data;
the home page's departures and fly-by; every episode's "Fly With Us" rows, Kenya now first as the sooner trip; the
"Fly it yourself" links; the About page's tour card). The generators that write the same facts carry the new dates
themselves (v4_expeditions*.py, v2_fly_options.py, v2_episode.py, v4_pass.py, v4_trip_calm.py), and the search
description's change is the owner's fact in tools/data/v4_facts.json (india_2027), which tools/v2_check.py accepts.
Live pages are the owner's and are not touched. Idempotent: a page already moved is left as it is.

    python3 tools/v4_india_2027.py
"""
import datetime as dt
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
D = dt.date
TOURS = [(D(2027, 4, 15), D(2027, 4, 24)), (D(2027, 4, 25), D(2027, 5, 4)),
         (D(2027, 10, 21), D(2027, 10, 30)), (D(2027, 11, 3), D(2027, 11, 12))]
NEXT = "15 to 24 Apr 2027"
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
MONTH = "January February March April May June July August September October November December".split()


def short(a, b):
    """15 to 24 Apr 2027, 25 Apr to 4 May 2027"""
    if a.month == b.month:
        return "%d to %d %s %d" % (a.day, b.day, MON[a.month - 1], b.year)
    return "%d %s to %d %s %d" % (a.day, MON[a.month - 1], b.day, MON[b.month - 1], b.year)


def long(a, b):
    if a.month == b.month:
        return "%d to %d %s %d" % (a.day, b.day, MONTH[a.month - 1], b.year)
    return "%d %s to %d %s %d" % (a.day, MONTH[a.month - 1], b.day, MONTH[b.month - 1], b.year)


def rd(path):
    return open(path, encoding="utf-8").read()


def wr(path, s, old):
    if s != old:
        open(path, "w", encoding="utf-8").write(s)
        print("  " + os.path.relpath(path, V4))


# ---------- every page ----------
FLY_IN = re.compile(r'( *)(<a class="ep2-fly-row" href="\.\./destinations/india\.html"><b>India</b><span>)21 to 30 Oct 2026( &middot;[^\n]*</a>)\n'
                    r'( *<a class="ep2-fly-row" href="\.\./destinations/kenya\.html">[^\n]*</a>)\n')


def everywhere(s):
    # the episodes' "Fly With Us": the sooner trip first
    s = FLY_IN.sub(lambda m: m.group(4) + "\n" + m.group(1) + m.group(2) + NEXT + m.group(3) + "\n", s)
    s = s.replace("<span>Fly it yourself</span> Bir Billing, 21 to 30 Oct 2026", "<span>Fly it yourself</span> Bir Billing, " + NEXT)
    s = s.replace("<dt>Next</dt><dd><b>21 to 30 Oct 2026</b></dd>", "<dt>Next</dt><dd><b>%s</b></dd>" % NEXT)
    s = s.replace("<dt>Next</dt><dd>21 to 30 Oct 2026</dd>", "<dt>Next</dt><dd>%s</dd>" % NEXT)
    return s


# ---------- the home page: the departures, in the order they fly ----------
DEP = re.compile(r'( *)<a class="v2-dep" href="destinations/india\.html" data-place="india" data-month="2026-1[01]">.*?</a>\n', re.S)


def home(s):
    rows = list(DEP.finditer(s))
    if not rows:
        return order(s)
    pad = rows[0].group(1)
    proto = rows[0].group(0)
    new = []
    for i, (a, b) in enumerate(TOURS):
        r = re.sub(r'data-month="\d{4}-\d{2}"', 'data-month="%d-%02d"' % (a.year, a.month), proto)
        r = re.sub(r"<em>Tour \d</em>", "<em>Tour %d</em>" % (i + 1), r)
        r = re.sub(r'<span data-l="Dates">[^<]*</span>', '<span data-l="Dates">%s</span>' % short(a, b), r)
        new.append(r)
    for m in reversed(rows):
        s = s[:m.start()] + s[m.end():]
    # all departure rows, India's among them, by month (a stable sort keeps each trip's tours in order)
    allrows = list(re.finditer(r' *<a class="v2-dep" [^>]*data-month="(\d{4}-\d{2})">.*?</a>\n', s, re.S))
    if not allrows:
        raise SystemExit("v4_india_2027: index.html: the departures are not there")
    start, end = allrows[0].start(), allrows[-1].end()
    keep = [(m.group(1), m.group(0)) for m in allrows]
    for r in new:
        keep.append((re.search(r'data-month="(\d{4}-\d{2})"', r).group(1), r))
    return order(s[:start] + "".join(r for _, r in keep) + s[end:])


def order(s):
    """The departure rows by month; in the same month a dated tour before a planned one (Peru, November 2027)."""
    allrows = list(re.finditer(r' *<a class="v2-dep" [^>]*data-month="(\d{4}-\d{2})">.*?</a>\n', s, re.S))
    if not allrows:
        return s
    start, end = allrows[0].start(), allrows[-1].end()
    keep = sorted(((m.group(1), "trip=" in m.group(0)[:200], m.group(0)) for m in allrows), key=lambda t: t[:2])
    return s[:start] + "".join(r for _, _, r in keep) + s[end:]


# ---------- the India page ----------
def band():
    """The season band: April to November 2027, a tick at each month, the four tours at their days."""
    first, last = D(2027, 4, 1), D(2027, 11, 30)
    total = (last - first).days + 1
    p = lambda d: 100.0 * (d - first).days / total
    months = [D(2027, m, 1) for m in range(4, 12)]
    ticks = "".join('<i class="kdates-tick" style="--p:%.2f"></i>\n' % p(m) for m in months[1:])
    tours = "".join('<i class="kdates-tour" style="--a:%.2f;--w:%.2f;--i:%d"><b>%02d</b><span>%s</span></i>\n'
                    % (p(a), 100.0 * ((b - a).days + 1) / total, i, i + 1, short(a, b).rsplit(" ", 1)[0])
                    for i, (a, b) in enumerate(TOURS))
    mos = "".join('<span style="--p:%s">%s</span>' % (("%.2f" % p(m)) if m != first else "0", MON[m.month - 1]) for m in months)
    return ('<div class="kdates-band" aria-hidden="true">\n<div class="kdates-track">\n' + ticks + tours + '</div>\n'
            '<div class="kdates-months">\n' + mos + '\n</div>\n'
            '<p class="kdates-legend">Two departures in spring, back to back from 15 April to 4 May. Two in autumn, inside the '
            'season that runs from about 10 October well into November, three days apart.</p>\n</div>\n')


def when_html(a, b):
    if a.month == b.month:
        return '<time datetime="%s">%d</time> to <time datetime="%s">%d %s</time> %d' % (a, a.day, b, b.day, MONTH[b.month - 1], b.year)
    return '<time datetime="%s">%d %s</time> to <time datetime="%s">%d %s</time> %d' % (
        a, a.day, MONTH[a.month - 1], b, b.day, MONTH[b.month - 1], b.year)


def meta_line(a, b):
    f1, f2 = a + dt.timedelta(days=1), b - dt.timedelta(days=1)
    fly = ("%d to %d %s" % (f1.day, f2.day, MON[f2.month - 1]) if f1.month == f2.month
           else "%d %s to %d %s" % (f1.day, MON[f1.month - 1], f2.day, MON[f2.month - 1]))
    return "Arrive %d %s &middot; eight flying days, %s &middot; leave %d %s" % (a.day, MON[a.month - 1], fly, b.day, MON[b.month - 1])


def cards(proto):
    out = []
    for i, (a, b) in enumerate(TOURS):
        c = proto
        c = re.sub(r'<span class="kdates-n">\d+</span>', '<span class="kdates-n">%02d</span>' % (i + 1), c)
        c = re.sub(r"<h3>India Tour \d</h3>", "<h3>India Tour %d</h3>" % (i + 1), c)
        c = re.sub(r'<p class="kdates-when">.*?</p>', '<p class="kdates-when">%s</p>' % when_html(a, b), c, flags=re.S)
        c = re.sub(r'<p class="kdates-meta">.*?</p>', '<p class="kdates-meta">%s</p>' % meta_line(a, b), c, flags=re.S)
        c = re.sub(r'when=[^"]+"', 'when=%s"' % long(a, b).replace(" ", "+"), c)
        out.append(c)
    return "\n".join(out)


def trips_ld(s):
    sub = []
    for i, (a, b) in enumerate(TOURS):
        sub.append({"@type": "Trip", "name": "India Tour %d, %s" % (i + 1, long(a, b)), "departureTime": str(a), "arrivalTime": str(b),
                    "offers": {"@type": "Offer", "price": "1100", "priceCurrency": "GBP",
                               "url": "https://paraglidingatlas.com/destinations/india.html#dates", "validThrough": str(a)}})
    new = '"subTrip":' + json.dumps(sub, ensure_ascii=False, separators=(",", ":"))
    s2 = re.sub(r'"subTrip":\[\{"@type":"Trip","name":"India Tour 1, 21 to 30 October 2026".*?"validThrough":"2026-11-03"\}\}\]', lambda _: new, s)
    return s2.replace('"offerCount":2', '"offerCount":4') if s2 != s else s


TEXT = [
    ("Two departures in October and November 2026", "Four departures in 2027, in April, May, October and November"),
    ("<span>Two departures this autumn, £1,100.</span>", "<span>Four departures in 2027, £1,100.</span>"),
    ("<h2>Tour Dates For Autumn 2026</h2>", "<h2>Tour Dates For 2027</h2>"),
    ("<p>Two departures of ten days and nine nights in Bir, six pilots on each.</p>",
     "<p>Four departures of ten days and nine nights in Bir, six pilots on each.</p>"),
    ("Our two 2026 departures, 21 to 30 October and 3 to 12 November, sit inside that window.",
     "Our autumn departures, 21 to 30 October and 3 to 12 November 2027, sit inside that window; the two spring "
     "departures, 15 to 24 April and 25 April to 4 May 2027, come before it."),
    ("Both departures are guaranteed to run.", "All four departures are guaranteed to run."),
    ("with our first departure on 21 October, it is not something to leave late.",
     "with our first departure on 15 April, it is not something to leave late."),
    ("Both departures are guaranteed to run: we will not cancel either one for low numbers. Because both are less than "
     "120 days away, the full £1,100 is due when you book, as set out in our",
     "All four departures are guaranteed to run: we will not cancel any of them for low numbers. What is due when you "
     "book is set out in our"),
    ("<span>Next departure 21 Oct 2026</span>", "<span>Next departure 15 Apr 2027</span>"),
]


def india(s):
    for a, b in TEXT:
        s = s.replace(a, b)
    s = trips_ld(s)
    m = re.search(r'<div class="kdates-band" aria-hidden="true">.*?</div>\n</div>\n(?=<div class="kdates-grid">)', s, re.S)
    if m and "21 to 30 Oct" in m.group(0):
        s = s[:m.start()] + band() + s[m.end():]
    g = re.search(r'(<div class="kdates-grid">\n)(.*?)(\n</div>\n<p class="kdates-terms">)', s, re.S)
    if g and "2026-10-21" in g.group(2):
        proto = re.search(r'<article class="kdates-card">.*?</article>', g.group(2), re.S).group(0)
        s = s[:g.start()] + g.group(1) + cards(proto) + g.group(3) + s[g.end():]
    return s


def main():
    print("v4 India 2027:")
    for d, dirs, files in os.walk(V4):
        dirs[:] = [x for x in dirs if x not in ("samples", "src")]
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(d, f)
            old = rd(p)
            s = everywhere(old)
            rel = os.path.relpath(p, V4)
            if rel == "index.html":
                s = home(s)
            if rel == os.path.join("destinations", "india.html"):
                s = india(s)
            wr(p, s, old)


if __name__ == "__main__":
    main()
