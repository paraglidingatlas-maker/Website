#!/usr/bin/env python3
"""
Make the hidden v2 prototype (prototypes/v2/) work where it lives.

v2 pages mirror the live folder layout (prototypes/v2/destinations/kenya.html
replaces destinations/kenya.html), so they are written with the LIVE page's
relative links. This rewrites every relative href/src/srcset/poster/url() in
them once:

  - the target exists next to the v2 page (a v2 twin, v2.css, v2.js) -> kept;
  - otherwise it is resolved as the live page would resolve it, and pointed
    at the live file (../../assets/..., ../../episodes/...).

It also makes sure every v2 page carries the robots noindex, loads
prototypes/v2/v2.css after styles.css and v2.js in the head, and writes the
list of built pages into v2.js (which sends run-time links to pages without a
v2 twin to the live page).

Idempotent. Not part of build.sh: the live build never touches v2 except for
version_assets.py, which hashes its links like any other page.

    python3 tools/v2_localize.py          # rewrite, report missing targets
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = S.DIR
SKIP = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#|/|\{|\$|%)", re.I)
ATTR = re.compile(r'(\s(?:href|src|poster|data-src|data-poster|data-loop)=")([^"]*)(")', re.I)
SRCSET = re.compile(r'(\s(?:srcset|data-srcset)=")([^"]*)(")', re.I)
CSSURL = re.compile(r'(url\((["\']?))([^)"\']+)(\2\))')


def exists(p):
    # data-loop="../assets/video/bir" names a family of files (bir-720.webm, ...)
    return os.path.exists(p) or os.path.exists(p + "-720.mp4")


def fix_url(u, page_dir, live_dir, missing):
    if not u or SKIP.match(u):
        return u
    m = re.match(r"([^?#]*)(.*)", u)
    path, tail = m.group(1), m.group(2)
    if not path:
        return u
    here = os.path.normpath(os.path.join(page_dir, path))
    if exists(here):
        target = here
        if target.startswith(V2 + os.sep):
            return u
    else:
        target = os.path.normpath(os.path.join(ROOT, live_dir, path))
    # a live page that has a v2 twin (built after this link was first rewritten)
    twin = os.path.join(V2, os.path.relpath(target, ROOT))
    if target.startswith(ROOT) and not target.startswith(V2) and os.path.isfile(twin):
        target = twin
    if exists(target) and target.startswith(ROOT):
        rel = os.path.relpath(target, page_dir).replace(os.sep, "/")
        if path.endswith("/") and not rel.endswith("/"):
            rel += "/"
        return rel + tail
    missing.add(u)
    return u


def main():
    pages = []
    for d, _, files in os.walk(V2):
        for f in files:
            if f.endswith(".html"):
                pages.append(os.path.join(d, f))
    pages.sort()
    problems = 0
    for fp in pages:
        rel = os.path.relpath(fp, V2).replace(os.sep, "/")
        page_dir = os.path.dirname(fp)
        live_dir = os.path.dirname(rel)
        html = open(fp, encoding="utf-8").read()
        missing = set()

        # skip inline <script> bodies: their strings are run-time paths, left to v2.js
        parts = re.split(r"(<script\b[^>]*>.*?</script>)", html, flags=re.S | re.I)
        for i, part in enumerate(parts):
            if i % 2 == 1:
                parts[i] = re.sub(r"^(<script\b[^>]*>)", lambda m: ATTR.sub(
                    lambda a: a.group(1) + fix_url(a.group(2), page_dir, live_dir, missing) + a.group(3),
                    m.group(1)), part)
                continue
            part = ATTR.sub(lambda a: a.group(1) + fix_url(a.group(2), page_dir, live_dir, missing) + a.group(3), part)
            part = SRCSET.sub(lambda a: a.group(1) + ", ".join(
                " ".join([fix_url(c.strip().split()[0], page_dir, live_dir, missing)] + c.strip().split()[1:])
                for c in a.group(2).split(",") if c.strip()) + a.group(3), part)
            part = CSSURL.sub(lambda a: a.group(1) + fix_url(a.group(3), page_dir, live_dir, missing) + a.group(4), part)
            parts[i] = part
        html = "".join(parts)

        up = os.path.relpath(V2, page_dir).replace(os.sep, "/")
        up = "" if up == "." else up + "/"
        if 'name="robots"' not in html:
            html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
        if "v2.css" not in html:
            html, n = re.subn(r'(<link rel="stylesheet" href="[^"]*styles\.css[^"]*">)',
                              r'\1\n<link rel="stylesheet" href="%sv2.css">' % up, html, count=1)
            if not n:
                print("  no styles.css link:", rel)
                problems += 1
        if "v2.js" not in html:
            html = html.replace("</head>", '<script src="%sv2.js"></script>\n</head>' % up, 1)
        if "v2-immersive.js" not in html:
            html = html.replace("</head>", '<script src="%sv2-immersive.js"></script>\n</head>' % up, 1)
        live_twin = os.path.join(ROOT, rel)
        live_has = os.path.exists(live_twin) and 'rel="canonical"' in open(live_twin, encoding="utf-8").read()
        if (live_has or not os.path.exists(live_twin)) and not re.search(r'<link rel="canonical" href="https://paraglidingatlas\.com/', html):
            print("  no live canonical:", rel)
            problems += 1
        open(fp, "w", encoding="utf-8").write(html)
        for u in sorted(missing):
            print("  missing target in %s: %s" % (rel, u))
            problems += 1

    js = os.path.join(V2, "v2.js")
    src = open(js, encoding="utf-8").read()
    lst = ",".join('"%s"' % os.path.relpath(p, V2).replace(os.sep, "/") for p in pages)
    src = re.sub(r"/\*v2-pages\*/.*?/\*/v2-pages\*/", "/*v2-pages*/" + lst + "/*/v2-pages*/", src)
    open(js, "w", encoding="utf-8").write(src)
    print("%s: %d pages, %d problems" % (S.NAME, len(pages), problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
