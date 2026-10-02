#!/usr/bin/env python3
"""
Title Case on every page heading and section heading (h1 and h2), sitewide.

WHY A BUILD STEP. The site had two cases side by side: the homepage wrote its
headings in Title Case ("Click A Pin, Hear The Story") while mission, library,
enquire, the 404, About, the policies, the trip pages and every knowledge base
page wrote theirs in sentence case. The headings come from a dozen generators
and as many hand-written pages, so fixing each source once would drift again
the next time a knowledge base section or a policy clause is added. This runs
after the generators, like the nav and schema injectors, and is idempotent.

THE STYLE is the homepage's own: every word starts with a capital, small words
included ("Flying As A Way Of Seeing The World"), and each part of a hyphenated
word does too ("30-Minute", "Multi-Day"). A word that already has a capital or a
digit anywhere in it is left exactly as written, so "X-Alps", "DIY", "EN 966",
"iPhone" and "8,000" survive. Units stay lower case ("451 km").

LEFT ALONE, because they are names rather than headings:
  - episode titles, wherever they appear as a heading (the episode page h1,
    the lists on the topic pages), matched against episode-meta.json;
  - the chapter headings inside an episode transcript (div.cd-block > h2),
    which are the chapter names the chapter list and timeline also show.
h3 and below are card titles and questions, not section headings, and are not
touched.

    python3 tools/title_case_headings.py           # rewrite pages in place
    python3 tools/title_case_headings.py --dry     # list what would change
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "__pycache__", "node_modules", "templates", "prototypes", "docs"}
UNITS = {"km", "m", "cm", "mm", "kg", "g", "ft", "mph", "kph", "kmh", "min", "mins", "hrs", "h"}
HEADING = re.compile(r'(<(h[12])\b[^>]*>)(.*?)(</\2>)', re.S)
CHAPTER = re.compile(r'<div class="cd-block"[^>]*>\s*$')


def cap_word(w):
    """One space-separated token, punctuation and all."""
    if any(c.isupper() or c.isdigit() for c in w if c.isalpha() or c.isdigit()) and "-" not in w:
        return w
    parts = w.split("-")
    out = []
    for p in parts:
        letters = "".join(c for c in p if c.isalpha())
        if not letters or any(c.isupper() for c in p) or letters.lower() in UNITS:
            out.append(p)
            continue
        i = next(k for k, c in enumerate(p) if c.isalpha())
        if i and p[:i].isdigit():
            # "30minute" style tokens do not occur; leave anything odd alone
            out.append(p)
            continue
        out.append(p[:i] + p[i].upper() + p[i + 1:])
    return "-".join(out)


def title_text(t):
    return re.sub(r"\S+", lambda m: cap_word(m.group(0)), t)


def title_html(inner):
    """Title-case the text between tags, never inside a tag or an entity."""
    out = []
    for piece in re.split(r'(<[^>]+>|&[#\w]+;)', inner):
        if not piece or piece.startswith("<") or (piece.startswith("&") and piece.endswith(";")):
            out.append(piece)
        else:
            out.append(title_text(piece))
    return "".join(out)


def plain(inner):
    import html
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", inner))).strip()


def episode_titles():
    try:
        meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    out = set()
    for e in meta:
        for k in ("title", "short_title", "display_title"):
            if e.get(k):
                out.add(re.sub(r"\s+", " ", e[k]).strip())
    return out


def pages():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(base, f)


def main():
    dry = "--dry" in sys.argv
    titles = episode_titles()
    touched = 0
    for full in sorted(pages()):
        rel = os.path.relpath(full, ROOT)
        src = open(full, encoding="utf-8").read()

        def sub(m):
            open_tag, _tag, inner, close = m.groups()
            text = plain(inner)
            if not text or text in titles:
                return m.group(0)
            if CHAPTER.search(src[max(0, m.start() - 200):m.start()]):
                return m.group(0)
            new = title_html(inner)
            if new != inner and dry:
                print("%-48s %s  ->  %s" % (rel, text[:60], plain(new)[:60]))
            return open_tag + new + close

        out = HEADING.sub(sub, src)
        if out != src:
            touched += 1
            if not dry:
                open(full, "w", encoding="utf-8").write(out)
    print("title case: headings changed on %d pages%s" % (touched, " (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
