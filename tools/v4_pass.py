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


def main(args):
    rels = args or sorted(os.path.relpath(os.path.join(d, f), V4).replace(os.sep, "/")
                          for d, _, fs in os.walk(V4) for f in fs if f.endswith(".html"))
    n = {"titles": 0, "kb folds": 0}
    for rel in rels:
        fp = os.path.join(V4, rel)
        src = open(fp, encoding="utf-8").read()
        out = src
        if rel.startswith("episodes/"):
            out = titles(out)
            n["titles"] += out != src
        if rel.startswith("knowledge-base/"):
            before = out
            out = kb_fold(out)
            n["kb folds"] += out.count('class="v4-fold k-more"') if out != before else 0
        if out != src:
            open(fp, "w", encoding="utf-8").write(out)
    print("v4 pass: " + ", ".join("%s %d" % kv for kv in n.items()))


if __name__ == "__main__":
    main(sys.argv[1:])
