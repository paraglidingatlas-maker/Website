#!/usr/bin/env python3
"""Add the site-wide structured data every page should carry.

Runs AFTER every generator, as the last step of build.sh, so it does not matter
which generator produced a page. That is deliberate: patching five generators
separately is how the knowledge base pages silently lost their canonical tags.

What it adds, and why each one earns its place:

  Organization + WebSite with sameAs
      The site currently never states that it is the same entity as the YouTube
      channel, the Apple podcast or the Patreon. Answer engines resolve entities
      by corroboration across sources; without sameAs a brand can be well known
      and still not be recognised as a thing that exists.

  dateModified
      Freshness is a documented ranking input for time-sensitive queries. The
      date comes from git, so it is the truth rather than a build timestamp that
      would falsely claim every page changed on every deploy.

  BreadcrumbList
      Gives search results a real hierarchy rather than a bare URL, and helps an
      engine understand that an episode belongs to a series.

  FAQPage
      Applied only where the page genuinely is a list of questions and answers.
      Marking a page as an FAQ when it is not is a structured-data violation.

Run: python3 tools/inject_site_schema.py
"""
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import site_config as cfg  # noqa: E402

SKIP = ("prototypes/", "templates/", "node_modules/", ".git/")
MARK_OPEN = "<!-- site-schema -->"
MARK_CLOSE = "<!-- /site-schema -->"

# Every address this site has ever advertised. Whichever one appears in a page,
# it is normalised to whatever site_config currently says.
#
# This exists because "change one line in site_config" turned out to be false
# when it was actually tested: 986 absolute URLs did not move, because canonical
# and og:url are written by six different generators and by hand in the static
# pages. Rewriting them here means the claim is now true, and it is true for
# pages nothing generates as well.
KNOWN_BASES = [
    "https://paraglidingatlas-maker.github.io/Website/",
    "https://paraglidingatlas.com/",
    "https://www.paraglidingatlas.com/",
]


def normalise_urls(h):
    """Point every absolute self-reference at the configured base."""
    n = 0
    for b in KNOWN_BASES:
        if b != cfg.BASE and b in h:
            n += h.count(b)
            h = h.replace(b, cfg.BASE)
    return h, n


def pages():
    out = []
    for dp, dn, fn in os.walk("."):
        rel = os.path.relpath(dp, ".").replace(os.sep, "/")
        rel = "" if rel == "." else rel + "/"
        if any(rel.startswith(s) for s in SKIP):
            dn[:] = []
            continue
        dn[:] = [d for d in dn if not (rel + d + "/").startswith(SKIP)]
        out += [rel + f for f in fn if f.endswith(".html")]
    return sorted(out)


_dates = {}


def git_modified(path):
    """Last commit date for a file. Real history, not a build timestamp."""
    if path in _dates:
        return _dates[path]
    r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                       capture_output=True, text=True)
    d = r.stdout.strip() or None
    _dates[path] = d
    return d


def breadcrumb(page, h):
    """Build a trail from the page's own visible breadcrumb, never invented."""
    m = re.search(r'<p class="breadcrumb">(.*?)</p>', h, re.S)
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": cfg.BASE}]
    if m:
        pos = 1
        for a in re.finditer(r'<a href="([^"]+)">([^<]+)</a>', m.group(1)):
            name = html.unescape(a.group(2)).strip()
            if name.lower() == "home":
                continue
            pos += 1
            target = a.group(1).split("#")[0]
            full = os.path.normpath(os.path.join(os.path.dirname(page), target)) if target else page
            items.append({"@type": "ListItem", "position": pos, "name": name,
                          "item": cfg.url(full.replace(os.sep, "/"))})
        tail = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split("/")[-1].strip()
        if tail and tail.lower() not in [i["name"].lower() for i in items]:
            items.append({"@type": "ListItem", "position": pos + 1, "name": tail,
                          "item": cfg.url(page)})
    if len(items) < 2:
        return None
    return {"@type": "BreadcrumbList", "itemListElement": items}


def faq(h):
    """Extract genuine question-and-answer pairs.

    Only where a heading is literally a question and is followed by prose. A page
    of statements marked up as an FAQ is a structured-data violation, so the
    question mark is the gate.
    """
    qa = []
    for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>(.*?)(?=<h[23][^>]*>|</section>|$)", h, re.S):
        q = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        q = re.sub(r"^\d+\.\s*", "", q)
        if not q.endswith("?"):
            continue
        body = m.group(2)
        text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", p)).strip()
                        for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S))
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) < 40:
            continue
        qa.append({"@type": "Question", "name": q,
                   "acceptedAnswer": {"@type": "Answer", "text": text[:1200]}})
    return {"@type": "FAQPage", "mainEntity": qa} if len(qa) >= 2 else None


def build_block(page, h):
    graph = [cfg.organization(), cfg.website()]
    d = git_modified(page)
    web = {"@type": "WebPage", "@id": cfg.url(page) + "#webpage",
           "url": cfg.url(page), "isPartOf": {"@id": cfg.SITE_ID},
           "publisher": {"@id": cfg.ORG_ID}, "inLanguage": "en"}
    if d:
        web["dateModified"] = d
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    if t:
        web["name"] = html.unescape(re.sub(r"\s+", " ", t.group(1))).strip()
    graph.append(web)
    b = breadcrumb(page, h)
    if b:
        graph.append(b)
    f = faq(h)
    if f:
        graph.append(f)
    data = {"@context": "https://schema.org", "@graph": graph}
    return ('%s\n<script type="application/ld+json">\n%s\n</script>\n%s'
            % (MARK_OPEN, json.dumps(data, ensure_ascii=False, indent=1), MARK_CLOSE))


def main():
    n = faqs = crumbs = 0
    rewritten = [0]
    for p in pages():
        h = open(p, encoding="utf-8", errors="replace").read()
        if "noindex" in h:
            # No schema for a noindex page, but its canonical still has to move.
            h2, moved = normalise_urls(h)
            if moved:
                open(p, "w", encoding="utf-8").write(h2)
                rewritten[0] += moved
            continue
        h = re.sub(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?", "", h, flags=re.S)
        block = build_block(p, h)
        if "FAQPage" in block:
            faqs += 1
        if "BreadcrumbList" in block:
            crumbs += 1
        if "</head>" not in h:
            continue
        h = h.replace("</head>", block + "</head>", 1)
        h, moved = normalise_urls(h)
        rewritten[0] += moved
        open(p, "w", encoding="utf-8").write(h)
        n += 1
    print("site schema injected on %d pages  (%d with a breadcrumb trail, %d as FAQPage)"
          % (n, crumbs, faqs))
    if rewritten[0]:
        print("absolute URLs repointed at %s : %d" % (cfg.BASE, rewritten[0]))


if __name__ == "__main__":
    main()
