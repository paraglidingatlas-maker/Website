"""Generate sitemap.xml for the whole site.

robots.txt is written by generate_llms_txt.py, which owns it alongside llms.txt.
Two generators writing one file is how that file ends up depending on run order.

The site had neither. sitemap.html is a human facing graph; crawlers need the
XML. Run after adding or removing pages:  python3 generate_robots_sitemap.py
"""
import datetime, glob, os

BASE = "https://paraglidingatlas-maker.github.io/Website/"
SKIP = ("prototypes/", "templates/")

def priority(p):
    if p == "index.html": return "1.0"
    if p in ("podcast.html", "knowledge-base.html", "library.html", "about.html"): return "0.9"
    if p.startswith("knowledge-base/"): return "0.7"
    if p == "sitemap.html": return "0.4"
    return "0.6"                       # episode pages

def freq(p):
    return "weekly" if p in ("index.html", "podcast.html", "library.html") else "monthly"

def indexable(p):
    """Skip anything that tells crawlers not to index it. Redirect stubs carry
    noindex, and advertising them in the sitemap is a contradiction."""
    try:
        h = open(p, encoding="utf-8", errors="replace").read(4000)
    except OSError:
        return False
    return "noindex" not in h

pages = sorted(p.replace(os.sep, "/") for p in glob.glob("**/*.html", recursive=True)
               if not p.replace(os.sep, "/").startswith(SKIP) and indexable(p))

rows = []
for p in pages:
    ts = datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()
    rows.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n"
                "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
                % (BASE, p, ts, freq(p), priority(p)))

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")

