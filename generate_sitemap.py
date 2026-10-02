#!/usr/bin/env python3
"""Build sitemap.html from the site's own data so it cannot drift out of date.

Sources: library-data.js (series and episodes), episode-meta.json (which episodes
have a full page), knowledge-base/ (which series pages exist).
Run: python3 generate_sitemap.py
"""
import json, re, os, glob, html

ROOT = os.path.dirname(os.path.abspath(__file__))

lib = open(os.path.join(ROOT, 'library-data.js')).read()
_blk = __import__('re').search(r'const LIB_TOPICS\s*=\s*\{(.*?)\};', lib, __import__('re').S).group(1)
TOPICS = {}
for k, v in __import__('re').findall(r'"([^"]+)"\s*:\s*"([^"]+)"', _blk):
    TOPICS[k] = v

TITLE_RE = re.compile(r'title:\s*("(?:\\.|[^"\\])*")')
EPS = []
for _row in re.findall(r"\{([^{}]*)\}", lib.rsplit("LIB_EPISODES", 1)[-1]):
    _o = re.search(r"order:\s*(\d+)", _row)
    _i = re.search(r'id:\s*"([^"]*)"', _row)      # may be empty: audio-only episodes
    _p = re.search(r'page:\s*"([^"]+)"', _row)
    _t = re.search(r'topic:\s*"([^"]+)"', _row)
    _ti = re.search(TITLE_RE, _row)
    if _o and _i and _t and _ti:
        EPS.append({"order": int(_o.group(1)), "id": _i.group(1),
                    "page": _p.group(1) if _p else "",
                    "topic": _t.group(1), "title": json.loads(_ti.group(1))})
META = json.load(open(os.path.join(ROOT, 'episode-meta.json')))
PAGE = {m["video_id"]: m for m in META if m.get("video_id")}
# Audio-only episodes have no YouTube id, so they can never match on one. Fall
# back to the page slug, which library-data.js carries for every episode.
BYSLUG = {m["slug"]: m for m in META}

# EVERY EPISODE PAGE, NOT ONLY THE LIBRARY'S. The library leaves out six pages
# on purpose (a note of thanks, four Oslo reels and the show trailer, listed at
# the top of library-data.js) and is missing New Technologies 5, so the sitemap
# listed 86 of the 93 episode pages. The rest are added here from
# episode-meta.json, under the series that file gives them. The 94th file in
# episodes/ is not a page: it is a redirect left behind by a renamed slug.
_listed = {(PAGE.get(e["id"]) or BYSLUG.get(e.get("page", "")) or {}).get("slug") for e in EPS}
for _n, _m in enumerate(m for m in META if m["slug"] not in _listed):
    if _m.get("series") in TOPICS:
        EPS.append({"order": 10000 + _n, "id": _m.get("video_id") or "", "page": _m["slug"],
                    "topic": _m["series"], "title": _m["title"]})

KB_PAGE = {}
for f in glob.glob(os.path.join(ROOT, 'knowledge-base', '*.html')):
    KB_PAGE[os.path.basename(f)[:-5]] = True

def kb_slug(series):
    s = series.lower().replace(',', '').replace(' ', '-')
    for cand in (s, s.replace('-and-', '-'), s.replace('the-', '')):
        if cand in KB_PAGE: return cand
    return None

# Nine titles arrive from the YouTube export already cut at YouTube's own 100
# character limit, ending in a literal "...". The untruncated titles live in
# episode-titles.json, taken verbatim from the show's RSS feed, which has no
# such limit. That file is the single source of truth and is keyed by video ID,
# not by the truncated string, so a title changing by one character cannot
# silently reintroduce the cut. Do not hard code title corrections here again.
TITLES = json.load(open("episode-titles.json", encoding="utf-8"))["titles"]

def fix_title(vid, t):
    return TITLES.get(vid, (t or "").strip())

def esc(t): return html.escape(str(t), quote=True)

CATS = []
for name, cat in TOPICS.items():
    for c, items in CATS:
        if c == cat: items.append(name); break
    else:
        CATS.append((cat, [name]))

rows = []
for cat, series_list in CATS:
    cards = []
    for s in series_list:
        eps = sorted([e for e in EPS if e["topic"] == s], key=lambda e: e["order"])
        kb = kb_slug(s)
        links = []
        for e in eps:
            m = PAGE.get(e["id"]) or BYSLUG.get(e.get("page", ""))
            if m:
                links.append('<li><a href="episodes/%s.html">%s</a></li>'
                             % (m["slug"], esc(fix_title(e["id"], e["title"].split("[")[0]))))
            else:
                links.append('<li><a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" class="sm-out">%s</a></li>'
                             % (e["id"], esc(fix_title(e["id"], e["title"].split("[")[0]))))
        withpage = sum(1 for e in eps if e["id"] in PAGE or e.get("page") in BYSLUG)
        cards.append(
            '  <details class="sm-series">\n'
            '    <summary><span class="sm-name">%s</span>'
            '<span class="sm-count">%s, %d with full transcripts</span></summary>\n'
            '    <div class="sm-body">\n'
            '      <p class="sm-jump">%s<a href="library.html#s=%s">Open in the library</a></p>\n'
            '      <ul class="sm-eps">%s</ul>\n'
            '    </div>\n'
            '  </details>'
            % (esc(s), "%d episode%s" % (len(eps), "" if len(eps)==1 else "s"), withpage,
               ('<a href="knowledge-base/%s.html">Series guide</a>' % kb) if kb else '',
               s.replace(' ', '%20').replace(',', '%2C'), "".join(links)))
    rows.append('<section class="sm-cat">\n  <h2>%s</h2>\n%s\n</section>' % (esc(cat), "\n".join(cards)))


# ---------------- graph data ----------------
CAT_PAGE = {"Core series": "core-series", "Competitions": "competitions",
            "Meteorology": "meteorology", "Industry": "industry", "Technical": "technical"}

nodes, links = [], []
def node(nid, label, kind, url=None, depth=0):
    nodes.append({"id": nid, "label": label, "kind": kind, "url": url, "depth": depth})
def link(a, b):
    links.append({"s": a, "t": b})

node("home", "Home", "root", "index.html", 0)
node("about", "About Me", "section", "about.html", 1)
node("kb", "Knowledge Base", "section", "knowledge-base.html", 1)
node("pod", "Podcast", "section", "podcast.html", 1)
node("lib", "Episode Library", "section", "library.html", 2)
for a in ("about", "kb", "pod"): link("home", a)
link("pod", "lib")

for cat, series_list in CATS:
    cid = "cat:" + cat
    page = CAT_PAGE.get(cat)
    node(cid, cat, "category", ("knowledge-base/%s.html" % page) if page and page in KB_PAGE else "knowledge-base.html", 2)
    link("kb", cid)
    for sname in series_list:
        sid = "ser:" + sname
        kb = kb_slug(sname)
        node(sid, sname, "series",
             ("knowledge-base/%s.html" % kb) if kb else ("library.html#s=" + sname.replace(" ", "%20")), 3)
        link(cid, sid)
        link("lib", sid)          # the same series is reachable from the library too
        for e in sorted([x for x in EPS if x["topic"] == sname], key=lambda x: x["order"]):
            m = PAGE.get(e["id"]) or BYSLUG.get(e.get("page", ""))
            # By page, not by video id: the eight audio-only episodes have no
            # video id and all came out as "ep:", one point for eight episodes.
            eid = "ep:" + (m["slug"] if m else e["id"])
            node(eid, fix_title(e["id"], e["title"].split("[")[0]), "episode",
                 ("episodes/%s.html" % m["slug"]) if m else ("https://www.youtube.com/watch?v=%s" % e["id"]), 4)
            link(sid, eid)

GRAPH = json.dumps({"nodes": nodes, "links": links}, ensure_ascii=False)

# ---------------- the night sky (sitemap-sky.js) ----------------
def ep_url(e):
    m = PAGE.get(e["id"]) or BYSLUG.get(e.get("page", ""))
    return ("episodes/%s.html" % m["slug"]) if m else ("https://www.youtube.com/watch?v=%s" % e["id"])

def plural(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")

lib_series = []
for _cat, series_list in CATS:
    for sname in series_list:
        eps = sorted([e for e in EPS if e["topic"] == sname], key=lambda e: e["order"])
        lib_series.append({"label": sname, "kind": "series", "series": sname,
                           "url": "library.html#s=" + sname.replace(" ", "%20").replace(",", "%2C"),
                           "sub": plural(len(eps), "episode"),
                           "children": [{"label": fix_title(e["id"], e["title"].split("[")[0]),
                                         "kind": "episode", "url": ep_url(e)} for e in eps]})
kb_cats = []
for cat, series_list in CATS:
    page = CAT_PAGE.get(cat)
    kb_cats.append({"label": cat, "kind": "category",
                    "url": ("knowledge-base/%s.html" % page) if page and page in KB_PAGE else "knowledge-base.html",
                    "sub": plural(len(series_list), "series").replace("seriess", "series"),
                    "children": [{"label": sn, "kind": "guide", "series": sn,
                                  "url": "knowledge-base/%s.html" % kb_slug(sn)}
                                 for sn in series_list if kb_slug(sn)]})
# The trips as the homepage presents them: its photographs (a small copy for
# a 34px circle) and the season or the date it is planned for.
TRIPS = [("Kenya", "destinations/kenya.html", "kenya-3", "December to March"),
         ("India", "destinations/india.html", "himalayas-1", "October to November"),
         ("Peru", "enquire.html?trip=peru", "peru-1", "Planned for November 2027"),
         ("Kazakhstan", "enquire.html?trip=kazakhstan", "kazakhstan-1", "Planned for June 2027")]
SKY_TREE = {"label": "Home", "kind": "root", "url": "index.html", "children": [
    {"label": "Podcast", "kind": "section", "url": "podcast.html",
     "sub": "%d series, %d episodes" % (len(TOPICS), len(EPS)), "children": [
        {"label": "Episode Library", "kind": "lib", "url": "library.html",
         "sub": "%d series" % len(TOPICS), "children": lib_series},
        {"label": "Topics", "kind": "page", "url": "tags.html"}]},
    {"label": "Knowledge Base", "kind": "section", "url": "knowledge-base.html",
     "sub": plural(len(kb_cats), "category").replace("categorys", "categories"), "children": kb_cats},
    {"label": "Trips", "kind": "section", "url": "index.html#destinations",
     "sub": "%d destinations" % len(TRIPS), "children":
        [{"label": l, "kind": "trip", "url": u, "img": "assets/images/%s-thumb.webp" % i, "sub": sub}
         for l, u, i, sub in TRIPS] + [{"label": "Enquire", "kind": "page", "url": "enquire.html"}]},
    {"label": "About Me", "kind": "section", "url": "about.html", "sub": "4 pages", "children": [
        {"label": "Mission Statement", "kind": "page", "url": "mission.html"},
        {"label": "Safety & Disclosure", "kind": "page", "url": "safety-and-disclosure.html"},
        {"label": "Corrections", "kind": "page", "url": "corrections.html"},
        {"label": "Partner With Me", "kind": "page", "url": "partners.html"}]},
    {"label": "Legal", "kind": "section", "url": None, "sub": "4 pages", "children": [
        {"label": "Terms & Conditions", "kind": "page", "url": "terms.html"},
        {"label": "Privacy Policy", "kind": "page", "url": "privacy-policy.html"},
        {"label": "Cookie Policy", "kind": "page", "url": "cookie-policy.html"},
        {"label": "Participant Agreement", "kind": "page", "url": "participant-agreement.html"}]}]}
SKY_META = {}
for m in META:
    SKY_META["episodes/%s.html" % m["slug"]] = {
        k: v for k, v in (("epno", m.get("epno")), ("guest", m.get("guest")),
                          ("nch", len(m.get("chapters") or []) or None), ("dur", m.get("duration_label")))
        if v}
try:
    _GLYPHS = json.load(open(os.path.join(ROOT, "tools", "data", "episode-extras.json"), encoding="utf-8"))["glyphs"]
except (OSError, ValueError, KeyError):
    _GLYPHS = {}
SKY = json.dumps({"tree": SKY_TREE, "meta": SKY_META, "glyphs": _GLYPHS}, ensure_ascii=False)
# </script> cannot appear inside the inline script
SKY = SKY.replace("</", "<\\/")

tmpl = open(os.path.join(ROOT, 'templates', 'sitemap-template.html')).read()
import sys as _sys, os as _os
_sys.path.insert(0, ROOT)
import site_config as _cfg
out = tmpl.replace('{{BASE}}', _cfg.BASE)
out = out.replace('{{TREE}}', "\n".join(rows))
out = out.replace('{{SKY}}', SKY)
out = out.replace('{{TRIPCOUNT}}', str(len(TRIPS)))
out = out.replace('{{EPCOUNT}}', str(len(EPS)))
out = out.replace('{{PAGECOUNT}}', str(sum(1 for e in EPS if e["id"] in PAGE or e.get("page") in BYSLUG)))
out = out.replace('{{SERIESCOUNT}}', str(len(TOPICS)))
open(os.path.join(ROOT, 'sitemap.html'), 'w').write(out)
print("sitemap.html built: %d series, %d episodes, %d with pages"
      % (len(TOPICS), len(EPS), sum(1 for e in EPS if e["id"] in PAGE or e.get("page") in BYSLUG)))
