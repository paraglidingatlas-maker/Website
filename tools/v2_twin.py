#!/usr/bin/env python3
"""
Build the v2 twin of a live page whose content v2 keeps as it is, in the kit.

The page is copied from the live file and given only the kit's frame, exactly
as the first hand-made samples were (knowledge-base/flight-mechanics.html,
tags/safety.html, privacy-policy.html):

  kb   knowledge-base/<category>.html  body marked data-v2="kb"; v2.css styles
                                       the category page under that marker
  tg   tags/<topic>.html               body marked data-v2="tg"; the topic
                                       header becomes the kit hero
  pg   the text pages                  body marked data-v2="pg"; the policy
                                       header becomes the kit page hero; a page
                                       with its own header (partners) keeps it

Everything else (words, links, schema, the head) stays the live page's, so
the page keeps its search and answer-engine visibility; tools/v2_check.py
checks that. Redirect stubs are not twinned: they stay live as they are.
Run tools/v2_localize.py afterwards.

    python3 tools/v2_twin.py            # every page of the three kinds
    python3 tools/v2_twin.py tags/safety.html privacy-policy.html
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = S.DIR
TEXT_PAGES = ["privacy-policy.html", "mission.html", "partners.html", "corrections.html",
              "safety-and-disclosure.html", "cookie-policy.html", "terms.html",
              "participant-agreement.html"]


def kind(rel):
    if rel.startswith("knowledge-base/"):
        return "kb"
    if rel.startswith("tags/"):
        return "tg"
    if rel in TEXT_PAGES:
        return "pg"
    return None


def everything():
    out = []
    for sub, k in (("knowledge-base", "kb"), ("tags", "tg")):
        for f in sorted(os.listdir(os.path.join(ROOT, sub))):
            if f.endswith(".html"):
                out.append(sub + "/" + f)
    out += TEXT_PAGES
    return [r for r in out if not is_stub(os.path.join(ROOT, r))]


def is_stub(path):
    with open(path, encoding="utf-8") as fh:
        return 'http-equiv="refresh"' in fh.read(4000)


def hero_tg(m):
    body = m.group(1)
    body = body.replace('<span class="kicker">', '<span class="kit-kicker">', 1)
    body = body.replace('<p class="tg-count">', '<p class="kit-intro">', 1)
    return '<header class="kit-hero is-sky v2-tg-hero">\n  <div class="kit-hero-copy">%s  </div>\n</header>' % body


def hero_pg(m):
    body = m.group(1)
    body = body.replace('<span class="kicker">', '<span class="kit-kicker">', 1)
    body = body.replace('<p class="pol-meta">', '<p class="kit-intro v2-meta">', 1)
    body = "\n".join(("  " + ln) if ln.strip() else ln for ln in body.split("\n"))
    return '<header class="kit-hero is-sky v2-page-hero">\n  <div class="kit-hero-copy">%s  </div>\n</header>' % body.rstrip(" ")


def build(rel):
    k = kind(rel)
    if not k:
        raise SystemExit("not a twin page: " + rel)
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        src = fh.read()
    src, n = re.subn(r"<body(\s[^>]*)?>", lambda m: '<body data-v2="%s"%s>' % (k, m.group(1) or ""), src, count=1)
    if not n:
        raise SystemExit("no <body> in " + rel)
    if k == "tg":
        src = re.sub(r'<header class="tg-hero">(.*?)</header>', hero_tg, src, count=1, flags=re.S)
    elif k == "pg":
        src = re.sub(r'<header class="pol-hero">(.*?)</header>', hero_pg, src, count=1, flags=re.S)
    out = os.path.join(V2, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(src)
    return k


def main(args):
    rels = args or everything()
    counts = {}
    for r in rels:
        k = build(r)
        counts[k] = counts.get(k, 0) + 1
    print("v2 twins: " + ", ".join("%d %s" % (n, k) for k, n in sorted(counts.items())))


if __name__ == "__main__":
    main(sys.argv[1:])
