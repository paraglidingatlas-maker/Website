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

EPS = [{"order": int(o), "id": i, "topic": t, "title": json.loads(ti)}
       for o, i, t, ti in re.findall(
           r'\{ order: (\d+), id: "([^"]+)", topic: "([^"]+)", title: (".*?") \},', lib)]
META = json.load(open(os.path.join(ROOT, 'episode-meta.json')))
PAGE = {m["video_id"]: m for m in META if m.get("video_id")}

KB_PAGE = {}
for f in glob.glob(os.path.join(ROOT, 'knowledge-base', '*.html')):
    KB_PAGE[os.path.basename(f)[:-5]] = True

def kb_slug(series):
    s = series.lower().replace(',', '').replace(' ', '-')
    for cand in (s, s.replace('-and-', '-'), s.replace('the-', '')):
        if cand in KB_PAGE: return cand
    return None

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
            m = PAGE.get(e["id"])
            if m:
                links.append('<li><a href="episodes/%s.html">%s</a></li>'
                             % (m["slug"], esc(e["title"].split('[')[0].strip())))
            else:
                links.append('<li><a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" class="sm-out">%s</a></li>'
                             % (e["id"], esc(e["title"].split('[')[0].strip())))
        withpage = sum(1 for e in eps if e["id"] in PAGE)
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

tmpl = open(os.path.join(ROOT, 'sitemap-template.html')).read()
out = tmpl.replace('{{TREE}}', "\n".join(rows))
out = out.replace('{{EPCOUNT}}', str(len(EPS)))
out = out.replace('{{PAGECOUNT}}', str(sum(1 for e in EPS if e["id"] in PAGE)))
out = out.replace('{{SERIESCOUNT}}', str(len(TOPICS)))
open(os.path.join(ROOT, 'sitemap.html'), 'w').write(out)
print("sitemap.html built: %d series, %d episodes, %d with pages"
      % (len(TOPICS), len(EPS), sum(1 for e in EPS if e["id"] in PAGE)))
