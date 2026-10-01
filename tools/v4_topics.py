#!/usr/bin/env python3
"""
The topics page in the Gold line (owner, 1 Oct 2026: "go", the Awwwards list):
each topic tile carries a small trace of its conversations over time, counted
per quarter from the dated episodes its own page lists (data-date on each
li.tg-ep). Episodes without a date are left out, so nothing is estimated. The
same reading as the chart on each topic page, at the size of a tile.

    python3 tools/v4_topics.py      # rewrites the traces in prototypes/v4/tags.html (idempotent)
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
W, H = 120, 26


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def quarter(d):
    y, m = int(d[:4]), int(d[5:7])
    return y * 4 + (m - 1) // 3


def dates(slug):
    p = os.path.join(V4, "tags", slug + ".html")
    if not os.path.exists(p):
        return []
    s = open(p, encoding="utf-8").read()
    return re.findall(r'<li class="tg-ep[^"]*" data-date="(\d{4}-\d\d-\d\d)"', s)


def smooth(pts):
    d = "M%s,%s" % (f(pts[0][0]), f(pts[0][1]))
    p = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(pts)):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        c1, c2 = (c1[0], min(c1[1], H - 3)), (c2[0], min(c2[1], H - 3))   # never below the baseline
        d += " C%s,%s %s,%s %s,%s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return d


def spark(qs, q0, q1, top):
    n = q1 - q0 + 1
    counts = [0] * n
    for q in qs:
        counts[q - q0] += 1
    xs = [2 + (W - 4) * i / (n - 1) for i in range(n)]
    pts = [(x, H - 3 - (H - 7) * c / top) for x, c in zip(xs, counts)]
    line = smooth(pts)
    area = line + " L%s,%s L%s,%s Z" % (f(xs[-1]), H - 3, f(xs[0]), H - 3)
    last = max(i for i, c in enumerate(counts) if c) if any(counts) else n - 1
    return ('<svg class="tg-spark" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            '<path class="tg-sp-a" d="%s"/><path class="tg-sp-b" d="M2,%s H%s"/><path class="tg-sp-l" d="%s"/>'
            '<circle class="tg-sp-d" cx="%s" cy="%s" r="1.6"/></svg>'
            % (W, H, area, H - 3, W - 2, line, f(pts[last][0]), f(pts[last][1])))


def main():
    p = os.path.join(V4, "tags.html")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'<svg class="tg-spark".*?</svg>', "", s, flags=re.S)
    tiles = re.findall(r'<a class="tg-tile" href="tags/([^"]+)\.html">', s)
    per = {t: [quarter(d) for d in dates(t)] for t in tiles}
    allq = [q for v in per.values() for q in v]
    q0, q1 = min(allq), max(allq)
    top = max(max([v.count(q) for q in set(v)] or [1]) for v in per.values())
    n = 0

    def put(m):
        nonlocal n
        qs = per.get(m.group(1), [])
        if not qs:
            return m.group(0)
        n += 1
        return m.group(0) + spark(qs, q0, q1, top)
    s = re.sub(r'<a class="tg-tile" href="tags/([^"]+)\.html">', put, s)
    open(p, "w", encoding="utf-8").write(s)
    print("v4 topics: %d traces, quarters %d-Q%d to %d-Q%d, highest quarter %d" % (n, q0 // 4, q0 % 4 + 1, q1 // 4, q1 % 4 + 1, top))


if __name__ == "__main__":
    main()
