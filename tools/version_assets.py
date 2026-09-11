#!/usr/bin/env python3
"""
Append a content hash to every local stylesheet AND script link, so a change
actually reaches a returning visitor.

WHY THIS EXISTS
Lesson 16 in the handoff says "cache bust any script that changes", and the
sitemap generator does exactly that for sitemap-graph.js. It was never applied
to CSS. Every stylesheet on the site was linked bare:

    <link rel="stylesheet" href="episode.css">

So a returning visitor with a warm cache kept the old file. This was found the
expensive way: two separate CSS-only changes to the episode tag styling were
built, audited, pushed, deployed green, and the user saw no difference on any
page, because their browser never refetched episode.css. A change that cannot be
seen is indistinguishable from a change that was never made, and it cost a round
of "did this work" either way.

SCRIPTS WERE ADDED LATER, AND FOR THE SAME REASON.
The first version of this tool covered CSS only. Two of the fourteen scripts on
the site were hand-versioned by their own generators and the other twelve,
including globe.js, script.js and episode-modal.js, were linked bare. The
episode popup was then rewritten from top to bottom, which a returning visitor
would never have seen. Same failure, same fix.

Any ?v= already present is stripped and replaced, so this tool is the single
mechanism. The md5 line in generate_sitemap.py that versions sitemap-graph.js
is now redundant; it is harmless because this runs after it and the pipeline is
deterministic, but it could go.

WHAT IT DOES
Rewrites href="foo.css" and src="foo.js" to carry ?v=<8 hex of sha256> on every
page, resolving each path against that page's own location so the file being
hashed is the file the browser will actually load.

Idempotent: any existing ?v= is stripped before the new one is appended, so the
hash tracks the file's contents rather than accumulating.

NOTES
- A query string does NOT change a stylesheet's base URL, so the relative
  url() calls inside fonts.css still resolve against /Website/. Verified.
- Font preloads are deliberately left alone. They point at woff2 files whose
  names already change when the font changes.
- External stylesheets are skipped. There are none today and there should not
  be any; see section 15 on why Google Fonts was removed.
- Runs from build.sh BEFORE inject_site_schema.py, like every other generator.
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = ("templates/", "node_modules/", ".git/", "__pycache__/")
LINK = re.compile(r'(<link[^>]*\shref=")([^"]+\.css)(\?v=[0-9a-f]+)?(")',
                  re.IGNORECASE)
SCRIPT = re.compile(r'(<script[^>]*\ssrc=")([^"]+\.js)(\?v=[0-9a-f]+)?(")',
                    re.IGNORECASE)

_cache = {}


def digest(path):
    if path not in _cache:
        with open(path, "rb") as fh:
            _cache[path] = hashlib.sha256(fh.read()).hexdigest()[:8]
    return _cache[path]


def resolve(page_rel, href):
    """The file this href actually loads, or None if it is not ours.

    Three shapes are in use and all three must work. `episode.css` sits beside
    the page. `../styles.css` climbs out of episodes/ or knowledge-base/.
    `/Website/styles.css` is absolute and appears on 404.html, which needs
    absolute paths because Pages serves it from any depth (see section 22).
    """
    if href.startswith(("http://", "https://", "//", "data:")):
        return None
    if href.startswith("/"):
        # served from /Website/, so strip that prefix to get a repo path
        rel = href.lstrip("/")
        if rel.startswith("Website/"):
            rel = rel[len("Website/"):]
        cand = os.path.join(ROOT, rel)
    else:
        cand = os.path.normpath(os.path.join(ROOT, os.path.dirname(page_rel), href))
    return cand if os.path.isfile(cand) else None


def main():
    pages = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs
                   if d not in (".git", "__pycache__", "node_modules", "templates")]
        for f in files:
            if f.endswith(".html"):
                pages.append(os.path.relpath(os.path.join(base, f), ROOT))

    touched = 0
    missing = []

    for rel in sorted(pages):
        if rel.startswith(SKIP_DIRS):
            continue
        full = os.path.join(ROOT, rel)
        src = open(full, encoding="utf-8").read()

        def sub(m):
            head, href, _old, tail = m.groups()
            target = resolve(rel, href)
            if target is None:
                if not href.startswith(("http://", "https://", "//", "data:")):
                    missing.append((rel, href))
                return head + href + tail
            return "%s%s?v=%s%s" % (head, href, digest(target), tail)

        out = SCRIPT.sub(sub, LINK.sub(sub, src))
        if out != src:
            open(full, "w", encoding="utf-8").write(out)
            touched += 1

    if missing:
        raise SystemExit(
            "version_assets: these asset links do not resolve to a file, which "
            "means they are 404ing on the live site: %s" % missing[:5])

    print("asset links versioned on %d pages" % touched)


if __name__ == "__main__":
    sys.exit(main())
