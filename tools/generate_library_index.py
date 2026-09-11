#!/usr/bin/env python3
"""
Write the no-JS episode index into library.html, between the
LIBRARY-INDEX markers.

Why this exists
---------------
Every tile on library.html is drawn by JavaScript after load. Search engines
run JavaScript so they see it; most AI crawlers (GPTBot, ClaudeBot,
PerplexityBot) read the HTML they are served and do not. Before this, the
served HTML of the site's main archive carried 117 words and zero episode
titles, so it could not be quoted or cited by an answer engine.

This is the same pattern sitemap.html already uses and that lesson 20 calls
essential. It is Option A from handoff item 10, chosen over rebuilding the
tiles as real HTML because that would restructure a page which took five
prototype rounds to settle.

It renders inside <noscript>, so anyone with JavaScript sees no difference at
all. The stone slabs are untouched.

Reads library-data.js, which is the same source the page itself uses, so the
index cannot disagree with the tiles. Run from build.sh BEFORE
inject_site_schema.py, like every other generator.

Fails loudly rather than writing a broken index: a missing marker, a link to
an episode page that does not exist, or a topic with no category are all hard
errors.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "library-data.js")
PAGE = os.path.join(ROOT, "library.html")
START = "<!-- LIBRARY-INDEX:START"
END = "<!-- LIBRARY-INDEX:END -->"


def die(msg):
    raise SystemExit("generate_library_index: " + msg)


def read_js():
    """Pull LIB_TOPICS and LIB_EPISODES out of library-data.js.

    The file is JavaScript, not JSON, so it is parsed by structure rather than
    eval'd. Trailing commas and // comments are stripped before json.loads.
    """
    src = open(DATA, encoding="utf-8").read()

    m = re.search(r"const\s+LIB_TOPICS\s*=\s*\{(.*?)\n\};", src, re.S)
    if not m:
        die("could not find LIB_TOPICS in library-data.js")
    topics = {}
    for name, cat in re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', m.group(1)):
        topics[name] = cat

    m = re.search(r"const\s+LIB_EPISODES\s*=\s*\[(.*?)\n\];", src, re.S)
    if not m:
        die("could not find LIB_EPISODES in library-data.js")

    episodes = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        obj = re.match(r"(\{.*?\})\s*,?\s*(//.*)?$", line)
        if not obj:
            die("could not parse this row:\n  " + line[:120])
        raw = obj.group(1)
        # quote the bare keys, then it is valid JSON
        raw = re.sub(r"(\{|,)\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', raw)
        try:
            episodes.append(json.loads(raw))
        except json.JSONDecodeError as e:
            die("row is not valid JSON (%s):\n  %s" % (e, line[:120]))

    if not episodes:
        die("parsed zero episodes, refusing to write an empty index")
    return topics, episodes


def build(topics, episodes):
    # group by category, then by topic, preserving the order LIB_TOPICS
    # declares so the index reads in the same order as the page
    by_topic = {}
    for ep in episodes:
        t = ep.get("topic", "")
        if t not in topics:
            die("episode %r has topic %r which LIB_TOPICS does not define"
                % (ep.get("page"), t))
        by_topic.setdefault(t, []).append(ep)

    cats = []
    for topic, cat in topics.items():
        if cat not in [c for c, _ in cats]:
            cats.append((cat, []))
        for c, lst in cats:
            if c == cat:
                lst.append(topic)

    missing = []
    # Categories are h2 and series h3, which follows the page's own h1 without
    # skipping a level. The audit checks for that.
    out = ['<noscript>',
           '<div class="lib-index">']
    total = 0
    for cat, topic_names in cats:
        out.append("<h2>%s</h2>" % html.escape(cat))
        for topic in topic_names:
            rows = by_topic.get(topic, [])
            if not rows:
                continue
            out.append('<h3>%s</h3>' % html.escape(topic))
            out.append("<ul>")
            for ep in rows:
                page = ep.get("page", "")
                target = os.path.join(ROOT, "episodes", page + ".html")
                if not os.path.exists(target):
                    missing.append(page)
                out.append('<li><a href="episodes/%s.html">%s</a></li>'
                           % (html.escape(page), html.escape(ep.get("title", ""))))
                total += 1
            out.append("</ul>")
    out.append("</div>")
    out.append("</noscript>")

    if missing:
        die("these rows link to an episode page that does not exist: %s"
            % missing)
    return "\n".join(out), total


def main():
    topics, episodes = read_js()
    block, total = build(topics, episodes)

    page = open(PAGE, encoding="utf-8").read()
    i = page.find(START)
    j = page.find(END)
    if i == -1 or j == -1:
        die("LIBRARY-INDEX markers not found in library.html")
    if j < i:
        die("LIBRARY-INDEX markers are the wrong way round in library.html")

    head_end = page.find("-->", i) + 3
    new = page[:head_end] + "\n" + block + "\n" + page[j:]

    if new == page:
        print("library index unchanged (%d episodes)" % total)
        return
    open(PAGE, "w", encoding="utf-8").write(new)
    print("library index written: %d episodes across %d series"
          % (total, len({e.get('topic') for e in episodes})))


if __name__ == "__main__":
    sys.exit(main())
