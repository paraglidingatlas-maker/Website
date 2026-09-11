import os
import sys
_R = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _R)
import site_config as _cfg  # single source of truth for the site address
#!/usr/bin/env python3
"""Build /tags.html and one hub page per tag.

Why pages rather than a JavaScript filter: a filter is invisible to a crawler and
to an answer engine. A tag page is a real URL with a real heading, a real list of
episodes and its own structured data, so "paragliding reserve parachutes" can
land somebody on a page that is actually about that, holding seven conversations
on it.

THRESHOLD is 3. A page listing two episodes is thin content: it splits link
equity and gives a visitor almost nothing. Tags below the threshold still render
on the episode page, just as plain text rather than a link.

Run: python3 generate_tag_pages.py
"""
import hashlib
import html
import json
import os
import re
import shutil
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = _cfg.BASE   # see site_config.py and MIGRATION.md
THRESHOLD = 3
OUT = os.path.join(ROOT, "tags")


def _sortver():
    """Content hash of tags-sort.js, appended to its src.

    Lesson 16 on this project: a script that changes behind a stale browser
    cache looks exactly like a script that is broken, and cost two rounds of
    confusion before. Keying on the file's own contents means the URL changes
    if and only if the behaviour does.
    """
    p = os.path.join(ROOT, "tags-sort.js")
    if not os.path.exists(p):
        return "0"
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:8]


def sort_key(title):
    """Title reduced to what a reader would actually alphabetise by.

    Episode titles here open with punctuation, quotes, series numbers and
    accented guest names. Sorting the raw string puts anything starting with a
    quote or a digit in its own clump at one end, which reads as broken rather
    than as ordered. This strips leading articles and non-alphanumerics and
    folds case, so "The Russell Ogden Interview" files under R.

    Emitted as data-title so the browser sorts on the same value the generator
    chose, rather than re-deriving it in two places and drifting.
    """
    t = (title or "").lower()
    t = t.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^(the|a|an) ", "", t)
    return t


def slug(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


def esc(s):
    return html.escape(str(s or ""), quote=True)


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}assets/images/hero.jpg">
<meta property="og:url" content="{base}{path}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{jsonld}
</script>
<link rel="icon" type="image/png" href="{root}assets/logo/favicon.png">
<link rel="apple-touch-icon" href="{root}assets/logo/apple-touch-icon.png">
<meta name="theme-color" content="#141519">
<link rel="alternate" type="application/rss+xml" title="Paragliding Atlas Podcast" href="https://anchor.fm/s/ed1344d8/podcast/rss">
<link rel="preload" href="{root}assets/fonts/poppins-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/poppins-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/dm-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/dm-sans-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}fonts.css">
<link rel="stylesheet" href="{root}styles.css">
<link rel="stylesheet" href="{root}tags.css">
</head>
<body>

<div class="page-wrap">

<nav>
  <span class="nav-corner-l"></span>
  <span class="nav-corner-r"></span>
  <span class="nav-coords">59.9139&deg;N &middot; 10.7522&deg;E</span>
  <a href="{root}index.html" class="wordmark"><img src="{root}assets/logo/atlas-logo-white.png" alt="Paragliding Atlas" class="logo-img"></a>
  <div class="nav-links">
    <a href="{root}about.html">About Us</a>
    <span class="nav-sep">|</span>
    <a href="{root}knowledge-base.html">Knowledge Base</a>
    <span class="nav-sep">|</span>
    <a href="{root}podcast.html">Podcast</a>
    <span class="nav-sep">|</span>
    <a href="{root}sitemap.html">Sitemap</a>
  </div>
  <a href="{root}enquire.html" class="nav-cta" data-hover><span>Enquire Now</span></a>
</nav>
<div class="nav-chevron"></div>

{body}

</div><!-- /.page-wrap -->

<footer>
  <div class="footer-content">
  <div class="footer-top">
    <div class="footer-col footer-brand">
      <span class="wordmark"><img src="{root}assets/logo/atlas-logo-white.png" alt="Paragliding Atlas" class="logo-img" loading="lazy"></span>
      <p>Conversations, transcripts and guided flying.<br>Touch the Sky With Glory.</p>
      <p class="footer-addr">Organisasjonsnummer: 937116934<br>Olav Troviks Vei M 46<br>Oslo, Norway</p>
    </div>
    <div class="footer-col">
      <h2>Listen</h2>
      <a href="{root}library.html">All Episodes</a>
      <a href="{root}tags.html">Topics</a>
      <a href="{root}knowledge-base.html">Knowledge Base</a>
      <a href="{root}podcast.html">Podcast</a>
    </div>
    <div class="footer-col">
      <h2>Fly With Us</h2>
      <a href="{root}index.html#destinations">Destinations</a>
      <a href="{root}destinations/kenya.html">Kenya Tour</a>
      <a href="{root}enquire.html">Enquire</a>
      <a href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener">Book a Call</a>
    </div>
    <div class="footer-col">
      <h2>About</h2>
      <a href="{root}about.html">About Us</a>
      <a href="{root}mission.html">Mission Statement</a>
      <a href="{root}safety-and-disclosure.html">Safety &amp; Disclosure</a>
      <a href="{root}corrections.html">Corrections</a>
    </div>
  </div>
  <div class="footer-bottom">
    <a href="{root}terms.html">Terms &amp; Conditions</a>
    <a href="{root}privacy-policy.html">Privacy Policy</a>
    <a href="{root}cookie-policy.html">Cookie Policy</a>
    <span>Paragliding Atlas 2026</span>
  </div>
  </div>
  <div class="footer-graphic">
    <img src="{root}assets/footer/mountains.png" alt="Paragliding Atlas &mdash; Touch the Sky with Glory">
  </div>
</footer>

<script src="{root}script.js"></script>
<script src="{root}tags-sort.js?v={sortver}" defer></script>
</body>
</html>
"""


def answer_block(tag, eps):
    """A 40-60 word paragraph that directly answers "what does this site have on X".

    Research on AI citation is consistent that a short, self-contained paragraph
    placed immediately after the heading, written as ordinary prose rather than a
    blockquote or callout, is the shape answer engines lift most often.

    Every fact in it is counted from the data: the number of conversations, the
    named people, the adjacent subjects. Nothing is a definition of the topic,
    because writing definitions of paragliding concepts would mean inventing
    claims this site cannot stand behind.
    """
    named = [e.get("guest", "").strip() for e in eps if (e.get("guest") or "").strip()]
    seen, people = set(), []
    for n in named:
        if n.lower() not in seen:
            seen.add(n.lower())
            people.append(n)
    near = Counter(t for e in eps for t in (e.get("tags") or []) if t != tag)
    adjacent = [t for t, _ in near.most_common(4)]
    withT = sum(1 for e in eps if os.path.exists(os.path.join(ROOT, "transcripts",
                                                              e["slug"] + ".vtt")))
    bits = ["Paragliding Atlas has %d conversations tagged %s, %d of them with a complete "
            "transcript you can read and search on the page."
            % (len(eps), tag.lower(), withT)]
    if len(people) >= 2:
        picked = people[:4]
        bits.append("Guests include %s and %s." % (", ".join(picked[:-1]), picked[-1]))
    if adjacent:
        bits.append("The subject runs alongside %s." % ", ".join(a.lower() for a in adjacent[:3]))
    text = " ".join(bits)
    words = text.split()
    if len(words) > 62:
        text = " ".join(words[:60]).rstrip(",.") + "."
    return text


def build():
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    counts = Counter(t for e in meta for t in (e.get("tags") or []))
    paged = {t for t, n in counts.items() if n >= THRESHOLD}
    by_tag = defaultdict(list)
    for e in meta:
        for t in (e.get("tags") or []):
            if t in paged:
                by_tag[t].append(e)

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    # ---- one page per tag ----
    for tag in sorted(by_tag):
        eps = sorted(by_tag[tag], key=lambda e: (e.get("published") or "", e["title"]), reverse=True)
        s = slug(tag)
        desc = "%d Paragliding Atlas conversations about %s, each with a full transcript." % (
            len(eps), tag.lower())
        if len(desc) > 158:
            desc = desc[:155].rsplit(" ", 1)[0] + "..."
        rows = []
        for e in eps:
            others = [x for x in (e.get("tags") or []) if x != tag][:4]
            chips = "".join('<a class="tg-chip" href="%s.html">%s</a>' % (slug(o), esc(o))
                            for o in others if o in paged)
            rows.append(
                '    <li class="tg-ep" data-date="%s" data-title="%s" data-series="%s">\n'
                '      <a class="tg-ep-link" href="../episodes/%s.html">\n'
                '        <span class="tg-ep-series">%s</span>\n'
                '        <h2>%s</h2>\n'
                '        <p>%s</p>\n'
                '      </a>\n'
                '      <div class="tg-chips">%s</div>\n'
                '    </li>'
                % (esc(e.get("published") or ""),
                   esc(sort_key(e["title"])),
                   esc(e.get("series", "")),
                   e["slug"], esc(e.get("series", "")), esc(e["title"]),
                   esc((e.get("summary") or "")[:190]), chips))
        jsonld = json.dumps({
            "@context": "https://schema.org", "@type": "CollectionPage",
            "name": "%s episodes" % tag, "url": BASE + "tags/%s.html" % s,
            "description": desc,
            "isPartOf": {"@type": "WebSite", "name": "Paragliding Atlas", "url": BASE},
            "mainEntity": {"@type": "ItemList", "numberOfItems": len(eps),
                           "itemListElement": [
                               {"@type": "ListItem", "position": i + 1, "name": e["title"],
                                "url": BASE + "episodes/%s.html" % e["slug"]}
                               for i, e in enumerate(eps)]},
        }, ensure_ascii=False)
        body = (
            '<header class="tg-hero">\n'
            '  <p class="breadcrumb"><a href="../index.html">Home</a> / <a href="../tags.html">Topics</a> / %s</p>\n'
            '  <span class="kicker">Topic</span>\n'
            '  <h1><span class="tg-hash">#</span>%s</h1>\n'
            '  <p class="tg-count">%d conversation%s, every one with a full transcript.</p>\n'
            '</header>\n\n'
            '<p class="tg-answer">%s</p>\n\n'
            '<ul class="tg-list">\n%s\n</ul>\n\n'
            '<p class="tg-back"><a href="../tags.html">All topics</a> &middot; '
            '<a href="../library.html">Full episode library</a></p>\n'
            % (esc(tag), esc(tag), len(eps), "" if len(eps) == 1 else "s",
               esc(answer_block(tag, eps)), "\n".join(rows)))
        open(os.path.join(OUT, s + ".html"), "w", encoding="utf-8").write(
            HEAD.format(title=esc("%s | Paragliding Atlas episodes" % tag), desc=esc(desc),
                        ogtitle=esc(tag), base=BASE, path="tags/%s.html" % s,
                        jsonld=jsonld, root="../", body=body, sortver=_sortver()))

    # ---- the index ----
    groups = defaultdict(list)
    for t in sorted(by_tag, key=lambda x: -len(by_tag[x])):
        groups["all"].append(t)
    cards = "".join(
        '  <a class="tg-tile" href="tags/%s.html"><span class="tg-hash">#</span>%s<em>%d</em></a>\n'
        % (slug(t), esc(t), len(by_tag[t])) for t in groups["all"])
    desc = ("Every subject the Paragliding Atlas podcast has covered, from safety and certification "
            "to cross country, acro and the arguments about where the sport is going.")
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "name": "Topics",
        "url": BASE + "tags.html", "description": desc,
        "isPartOf": {"@type": "WebSite", "name": "Paragliding Atlas", "url": BASE},
    }, ensure_ascii=False)
    body = ('<header class="tg-hero">\n'
            '  <p class="breadcrumb"><a href="index.html">Home</a> / Topics</p>\n'
            '  <span class="kicker">Browse By Subject</span>\n'
            '  <h1>Topics</h1>\n'
            '  <p class="tg-count">%d subjects across %d conversations. '
            'Every episode carries a full transcript.</p>\n'
            '</header>\n\n<div class="tg-cloud">\n%s</div>\n\n'
            '<p class="tg-back"><a href="library.html">Full episode library</a> &middot; '
            '<a href="knowledge-base.html">Knowledge base</a></p>\n'
            % (len(by_tag), len(meta), cards))
    open(os.path.join(ROOT, "tags.html"), "w", encoding="utf-8").write(
        HEAD.format(title="Topics | Paragliding Atlas", desc=esc(desc), ogtitle="Topics",
                    base=BASE, path="tags.html", jsonld=jsonld, root="", body=body, sortver=_sortver()))

    print("tag pages built : %d  (threshold %d+ episodes)" % (len(by_tag), THRESHOLD))
    print("tags index      : tags.html, %d subjects" % len(by_tag))
    print("tags below cut  : %d, rendered as plain text on the episode page"
          % sum(1 for t, n in counts.items() if n < THRESHOLD))


if __name__ == "__main__":
    build()
