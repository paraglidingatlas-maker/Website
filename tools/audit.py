#!/usr/bin/env python3
"""Full site audit for Paragliding Atlas. One command, every check.

    python3 tools/audit.py            # report
    python3 tools/audit.py --quiet    # only failures
    python3 tools/audit.py --drift    # also check generated files are in sync

Exits non-zero if any check fails, so it can gate a push.

WHY THIS EXISTS
Four separate audits this project ran by hand each found a category the previous
one had not thought of: dropped transcript text, dangling rail anchors, a
noindex page in sitemap.xml, unused diarised transcripts, no 404, no RSS link,
heading levels skipping, unlabelled form fields. Relying on remembering to look
is the bug. Every check below is one that already caught something real.

TWO TRAPS BAKED IN, BOTH OF WHICH PRODUCED FALSE ALARMS BEFORE
  1. `grep -r --include=*.html . | grep -v prototypes` does NOT exclude that
     directory: the filtered lines are bare URLs that never contain the word.
     Exclusion happens on the path here, not the output.
  2. The site is served from /Website/, so an absolute link like
     /Website/styles.css must resolve against the repo root. Otherwise every
     link on 404.html looks broken.
"""
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SKIP_DIRS = ("prototypes/", "templates/", "node_modules/", ".git/")
BASE_PATH = "/Website/"

QUIET = "--quiet" in sys.argv
DRIFT = "--drift" in sys.argv

results = []          # (severity, category, message)


def fail(cat, msg):
    results.append(("FAIL", cat, msg))


def warn(cat, msg):
    results.append(("WARN", cat, msg))


def ok(cat, msg):
    results.append(("ok", cat, msg))


def html_pages():
    out = []
    for dirpath, dirnames, filenames in os.walk("."):
        rel = os.path.relpath(dirpath, ".").replace(os.sep, "/")
        rel = "" if rel == "." else rel + "/"
        if any(rel.startswith(s) for s in SKIP_DIRS):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if not (rel + d + "/").startswith(SKIP_DIRS)]
        for f in filenames:
            if f.endswith(".html"):
                out.append((rel + f))
    return sorted(out)


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def resolve(page, url):
    """Resolve a link the way a browser on the deployed site would."""
    url = url.split("#")[0].split("?")[0]
    if not url:
        return None
    if url.startswith(BASE_PATH):
        return url[len(BASE_PATH):]
    if url.startswith("/"):
        return url.lstrip("/")
    return os.path.normpath(os.path.join(os.path.dirname(page), url))


PAGES = html_pages()
META = json.load(open("episode-meta.json", encoding="utf-8"))
BY_SLUG = {e["slug"]: e for e in META}


# ---------------------------------------------------------------- links ----
def check_links():
    broken = Counter()
    for p in PAGES:
        h = read(p)
        for u in re.findall(r'(?:href|src|srcset)="([^"]+)"', h):
            if u.startswith(("http", "//", "mailto:", "tel:", "#", "data:", "javascript:")):
                continue
            t = resolve(p, u)
            if t and not os.path.exists(t):
                broken[u] += 1
    if broken:
        fail("links", "%d broken: %s" % (sum(broken.values()), dict(broken)))
    else:
        ok("links", "every relative and absolute link resolves")

    # links that live inside JS data rather than markup: invisible to a grep of HTML
    jsbad = Counter()
    for f in ("globe.js", "library-data.js", "episode-search-data.js", "episode-links.js"):
        if not os.path.exists(f):
            continue
        h = read(f)
        for u in set(re.findall(r'["\']((?:episodes|destinations|knowledge-base)/[a-z0-9\-]+\.html)["\']', h)):
            if not os.path.exists(u):
                jsbad["%s -> %s" % (f, u)] += 1
        for slug in set(re.findall(r'page:\s*"([a-z0-9\-]+)"', h)):
            if not os.path.exists("episodes/%s.html" % slug):
                jsbad["%s -> episodes/%s" % (f, slug)] += 1
    if jsbad:
        fail("links-js", "broken inside JS data: %s" % dict(jsbad))
    else:
        ok("links-js", "episode links inside JS data files all resolve")

    dangling = Counter()
    for p in PAGES:
        h = read(p)
        ids = set(re.findall(r'id="([^"]+)"', h))
        for a in set(re.findall(r'href="#([^"]+)"', h)):
            if a and a not in ids:
                dangling[p] += 1
    if dangling:
        fail("anchors", "in-page anchors with no target: %s" % dict(dangling))
    else:
        ok("anchors", "every in-page anchor has a target")

    dead = Counter()
    for p in PAGES:
        for m in re.finditer(r'<a[^>]+href="#"[^>]*>(.*?)</a>', read(p), re.S):
            dead[re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()[:24]] += 1
    if dead:
        warn("placeholders", "%d dead href=\"#\" links: %s" % (sum(dead.values()), dict(dead.most_common(6))))
    else:
        ok("placeholders", "no dead placeholder links")


# ------------------------------------------------------------- headings ----
def check_headings():
    skips, unbal, noh1, multih1 = [], [], [], []
    for p in PAGES:
        h = read(p)
        levels = [int(x) for x in re.findall(r"<h([1-6])[\s>]", h)]
        if any(b - a > 1 for a, b in zip(levels, levels[1:])):
            skips.append(p)
        for n in range(1, 7):
            if h.count("<h%d" % n) != h.count("</h%d>" % n):
                unbal.append("%s h%d" % (p, n))
                break
        c = levels.count(1)
        if c == 0:
            noh1.append(p)
        elif c > 1:
            multih1.append(p)
    for name, lst, sev in (("skips a level", skips, fail), ("unbalanced tags", unbal, fail),
                           ("no h1", noh1, warn), ("multiple h1", multih1, fail)):
        if lst:
            sev("headings", "%d pages %s: %s" % (len(lst), name, lst[:4]))
        else:
            ok("headings", "none %s" % name)


# ------------------------------------------------------------------ seo ----
def check_seo():
    def indexable(h):
        return "noindex" not in h
    for key, label in (("canonical", "canonical"), ("og:title", "og:title"),
                       ("og:image", "og:image"), ("application/ld+json", "JSON-LD"),
                       ('name="description"', "meta description"),
                       ("apple-touch-icon", "apple-touch-icon"),
                       ("theme-color", "theme-color"),
                       ("application/rss+xml", "RSS alternate")):
        missing = [p for p in PAGES if indexable(read(p)) and key not in read(p)]
        if missing:
            fail("seo", "%d indexable pages missing %s: %s" % (len(missing), label, missing[:3]))
        else:
            ok("seo", "every indexable page has %s" % label)

    bad = []
    for p in PAGES:
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', read(p), re.S):
            try:
                json.loads(m.group(1))
            except Exception:
                bad.append(p)
    if bad:
        fail("seo", "invalid JSON-LD on %s" % sorted(set(bad))[:3])
    else:
        ok("seo", "all JSON-LD parses")

    for field, pat in (("<title>", r"<title>(.*?)</title>"),
                       ("meta description", r'name="description" content="([^"]*)"')):
        c = Counter()
        for p in PAGES:
            m = re.search(pat, read(p), re.S)
            if m and m.group(1).strip():
                c[m.group(1).strip()] += 1
        dup = {k[:60]: v for k, v in c.items() if v > 1}
        if dup:
            warn("seo", "duplicate %s: %s" % (field, dup))
        else:
            ok("seo", "no duplicate %s" % field)

    empty = [p for p in PAGES if re.search(r'name="description" content="\s*"', read(p))]
    if empty:
        warn("seo", "%d pages have an EMPTY description: %s" % (len(empty), empty[:3]))
    else:
        ok("seo", "no empty descriptions")


# -------------------------------------------------------------- crawler ----
def check_crawler():
    for f in ("robots.txt", "sitemap.xml", "404.html"):
        if os.path.exists(f):
            ok("crawler", "%s present" % f)
        else:
            fail("crawler", "%s MISSING" % f)
    if not os.path.exists("sitemap.xml"):
        return
    sm = read("sitemap.xml")
    listed = set(re.findall(r"<loc>[^<]*/Website/([^<]+)</loc>", sm))
    indexable = {p for p in PAGES if "noindex" not in read(p)}
    missing = sorted(indexable - listed)
    extra = sorted(listed - {p for p in PAGES})
    noindexed = sorted(listed & {p for p in PAGES if "noindex" in read(p)})
    if missing:
        fail("crawler", "%d indexable pages absent from sitemap.xml: %s" % (len(missing), missing[:4]))
    else:
        ok("crawler", "sitemap.xml lists every indexable page")
    if extra:
        fail("crawler", "sitemap.xml lists files that do not exist: %s" % extra[:4])
    if noindexed:
        fail("crawler", "sitemap.xml advertises noindex pages: %s" % noindexed)
    else:
        ok("crawler", "no noindex page is advertised in sitemap.xml")
    # 404 must use absolute paths: it is served at any depth
    if os.path.exists("404.html"):
        rel = [u for u in re.findall(r'(?:href|src)="([^"]+)"', read("404.html"))
               if not u.startswith(("http", "/", "#", "data:", "mailto"))]
        if rel:
            fail("crawler", "404.html uses relative paths, which break at depth: %s" % rel[:4])
        else:
            ok("crawler", "404.html uses absolute paths")


# --------------------------------------------------------- accessibility ----
def check_a11y():
    noalt = sum(len([1 for m in re.finditer(r"<img[^>]*>", read(p)) if "alt=" not in m.group(0)])
                for p in PAGES)
    (ok if noalt == 0 else fail)("a11y", "images without alt: %d" % noalt)
    nolang = [p for p in PAGES if not re.search(r"<html[^>]+lang=", read(p))]
    (ok if not nolang else fail)("a11y", "pages without html lang: %s" % (nolang[:3] or 0))
    novp = [p for p in PAGES if "width=device-width" not in read(p)]
    (ok if not novp else fail)("a11y", "pages without a viewport meta: %s" % (novp[:3] or 0))
    unl = []
    for p in PAGES:
        h = read(p)
        if "<form" not in h:
            continue
        labelled = set(re.findall(r'<label[^>]+for="([^"]+)"', h))
        for m in re.finditer(r"<(?:input|select|textarea)\b[^>]*>", h):
            tag = m.group(0)
            if 'type="hidden"' in tag or 'type="submit"' in tag or "aria-label" in tag:
                continue
            idm = re.search(r'id="([^"]+)"', tag)
            if not idm or idm.group(1) not in labelled:
                unl.append(p)
    (ok if not unl else fail)("a11y", "unlabelled form fields on: %s" % (sorted(set(unl)) or 0))


# --------------------------------------------------------- third parties ----
def check_third_party():
    gf = [p for p in PAGES if "fonts.googleapis" in read(p) or "fonts.gstatic" in read(p)]
    (ok if not gf else fail)("privacy", "pages loading Google Fonts: %s" % (gf[:3] or 0))
    cdn = [p for p in PAGES if re.search(r'<script[^>]+src="https?://', read(p))]
    (ok if not cdn else fail)("privacy", "pages loading third-party scripts: %s" % (cdn[:3] or 0))
    store = []
    for f in [f for f in os.listdir(".") if f.endswith(".js")]:
        if re.search(r"document\.cookie|localStorage|sessionStorage", read(f)):
            store.append(f)
    (ok if not store else warn)("privacy", "files touching cookies/storage: %s" % (store or 0))
    yt = sum(read(p).count("youtube.com/embed") for p in PAGES)
    (ok if yt == 0 else fail)("privacy", "non-nocookie YouTube embeds: %d" % yt)


# ------------------------------------------------------------------ data ----
def check_data():
    pageset = {os.path.basename(p)[:-5] for p in PAGES if p.startswith("episodes/")}
    slugs = {e["slug"] for e in META}
    missing = sorted(slugs - pageset)
    (ok if not missing else fail)("data", "meta entries with no page: %s" % (missing or 0))
    extra = sorted(p for p in pageset - slugs if "noindex" not in read("episodes/%s.html" % p))
    (ok if not extra else fail)("data", "episode pages with no meta entry: %s" % (extra or 0))
    for k in ("slug", "title"):
        d = {a: b for a, b in Counter(e[k] for e in META).items() if b > 1}
        (ok if not d else fail)("data", "duplicate %s: %s" % (k, d or 0))
    d = {a: b for a, b in Counter(e["video_id"] for e in META if e.get("video_id")).items() if b > 1}
    (ok if not d else fail)("data", "duplicate video_id: %s" % (d or 0))
    ids = {i["video_id"] for i in json.load(open("youtube_video_ids.json", encoding="utf-8"))}
    bogus = sorted({e["video_id"] for e in META if e.get("video_id")} - ids)
    (ok if not bogus else fail)("data", "video_id not in the export: %s" % (bogus or 0))
    orphan = [f for f in os.listdir("transcripts")
              if f.endswith(".vtt") and f[:-4] not in slugs]
    (ok if not orphan else fail)("data", "transcript files matching no episode: %s" % (orphan or 0))
    longname = [f for f in os.listdir("transcripts") if f.endswith(".vtt") and len(f) > 70]
    (ok if not longname else warn)("data", "suspiciously long transcript filenames: %s" % (longname or 0))


# -------------------------------------------------------------- content ----
def secs(t):
    b = [float(x) for x in str(t).split(":")]
    while len(b) < 3:
        b.insert(0, 0.0)
    return b[0] * 3600 + b[1] * 60 + b[2]


def check_content():
    frag = [(e["slug"], c["title"]) for e in META for c in (e.get("chapters") or [])
            if c["title"].endswith(("...", "\u2026")) or c["title"][:1].islower()]
    (ok if not frag else fail)("content", "fragment chapter titles: %s" % (frag[:3] or 0))
    past = []
    for e in META:
        p = "transcripts/%s.vtt" % e["slug"]
        if not os.path.exists(p):
            continue
        ts = re.findall(r"([\d:.]+)\s*-->", read(p))
        if not ts:
            continue
        end = secs(ts[-1])
        for c in (e.get("chapters") or []):
            if c.get("at") and secs(c["at"]) > end + 2:
                past.append((e["slug"], c["title"][:24]))
    (ok if not past else fail)("content", "chapters past the end of their transcript: %s" % (past[:3] or 0))
    nochap = [e["slug"] for e in META
              if os.path.exists("transcripts/%s.vtt" % e["slug"]) and not e.get("chapters")]
    (ok if not nochap else warn)("content", "transcript episodes with no chapters: %s" % (nochap or 0))
    clip = [e["slug"] for e in META
            if os.path.exists("episodes/%s.html" % e["slug"])
            and "display:none" in read("episodes/%s.html" % e["slug"])]
    (ok if not clip else fail)("content", "transcript clipping rule broken on: %s" % (clip or 0))
    noprov = [e["slug"] for e in META
              if os.path.exists("transcripts/%s.vtt" % e["slug"])
              and "cd-tnote" not in read("episodes/%s.html" % e["slug"])]
    (ok if not noprov else fail)("content", "transcript pages with no provenance note: %s" % (noprov or 0))
    ph = [p for p in PAGES if "Placeholder" in read(p)]
    (ok if not ph else warn)("content", "pages containing the word Placeholder: %s" % (ph or 0))


# ---------------------------------------------------------------- assets ----
def check_assets():
    refs = set()
    scan = PAGES + [f for f in os.listdir(".") if f.endswith((".js", ".css"))]
    for p in scan:
        for u in re.findall(r"[\"'(\s]((?:\.\./)*(?:/Website/)?assets/[^\"')\s]+)", read(p)):
            refs.add(os.path.normpath(u.replace("../", "").replace(BASE_PATH, "")))
    allf = set()
    for dp, _, fn in os.walk("assets"):
        for f in fn:
            allf.add(os.path.normpath(os.path.join(dp, f)))
    unused = sorted(allf - refs)
    (ok if not unused else warn)("assets", "%d asset files never referenced: %s"
                                 % (len(unused), unused[:4]))
    big = sorted(((os.path.getsize(f), f) for f in allf if os.path.getsize(f) > 400 * 1024),
                 reverse=True)
    (ok if not big else warn)("assets", "files over 400 KB: %s"
                              % ([("%dKB" % (s // 1024), f) for s, f in big[:4]] or 0))
    # every jpg referenced by a <picture> needs its webp sibling
    missing = []
    for p in PAGES:
        for m in re.finditer(r'<source srcset="([^"]+)"', read(p)):
            t = resolve(p, m.group(1))
            if t and not os.path.exists(t):
                missing.append(m.group(1))
    (ok if not missing else fail)("assets", "picture sources missing: %s" % (missing[:3] or 0))
    # fonts: both subsets, and every preload must resolve
    css = read("fonts.css") if os.path.exists("fonts.css") else ""
    if css:
        nf = len(re.findall(r"@font-face", css))
        ext = css.count("latin-ext")
        (ok if ext >= 10 else fail)("assets", "fonts.css: %d @font-face, latin-ext blocks %d" % (nf, ext))
        gone = [u for u in re.findall(r'url\("([^"]+)"\)', css) if not os.path.exists(u)]
        (ok if not gone else fail)("assets", "font files referenced but missing: %s" % (gone or 0))
    bad = []
    for p in PAGES:
        for u in re.findall(r'<link rel="preload" href="([^"]+)"', read(p)):
            t = resolve(p, u)
            if t and not os.path.exists(t):
                bad.append((p, u))
    (ok if not bad else fail)("assets", "preloads pointing at missing files: %s" % (bad[:3] or 0))


# ------------------------------------------------------------------- js ----
def check_js():
    files = [f for f in os.listdir(".") if f.endswith(".js")]
    files += ["tools/" + f for f in os.listdir("tools") if f.endswith(".js")]
    bad = []
    for f in files:
        r = subprocess.run(["node", "--check", f], capture_output=True, text=True)
        if r.returncode:
            bad.append((f, r.stderr.strip().split("\n")[0][:50]))
    (ok if not bad else fail)("js", "syntax errors: %s" % (bad or 0))


# ---------------------------------------------------------------- drift ----
def check_drift():
    """Regenerate everything and see if anything changes.

    A change means someone edited generated output by hand and the edit is about
    to be silently reverted. That has happened three times on this project:
    sitemap.html, the thin episode descriptions, and all 17 knowledge base pages
    losing their canonical and JSON-LD.
    """
    gens = ["generate_chapter_deck.py", "generate_sitemap.py", "generate_policies.py",
            "generate_kb_pages.py", "generate_robots_sitemap.py"]
    for g in gens:
        if os.path.exists(g):
            subprocess.run([sys.executable, g], capture_output=True)
    r = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    changed = [l[3:] for l in r.stdout.strip().split("\n") if l.strip()]
    if changed:
        fail("drift", "regenerating changed %d file(s), so hand edits are about to be lost: %s"
             % (len(changed), changed[:6]))
    else:
        ok("drift", "generated files are in sync with their generators")


def main():
    check_links(); check_headings(); check_seo(); check_crawler()
    check_a11y(); check_third_party(); check_data(); check_content()
    check_assets(); check_js()
    if DRIFT:
        check_drift()

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    by_cat = defaultdict(list)
    for sev, cat, msg in results:
        by_cat[cat].append((sev, msg))
    for cat in by_cat:
        for sev, msg in by_cat[cat]:
            if QUIET and sev == "ok":
                continue
            mark = {"FAIL": "FAIL", "WARN": "warn", "ok": "  ok"}[sev]
            print("%s  %-12s %s" % (mark, cat, msg))
    print("\n%d pages checked | %d checks | %d FAIL | %d warn"
          % (len(PAGES), len(results), len(fails), len(warns)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
