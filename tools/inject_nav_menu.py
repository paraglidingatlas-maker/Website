#!/usr/bin/env python3
"""Put the nav-menu.js tag on every page that carries the header nav.

The nav markup is duplicated across 181 files and emitted by four generators and
three templates, so adding a script tag by hand would mean nineteen edits and a
standing risk that the next page added to the site quietly misses one. This walks
the pages the same way inject_site_schema does and writes the tag once per page,
between markers so it is idempotent and so removing the feature is one deletion.

Runs BEFORE tools/version_assets.py so the tag picks up a content hash like every
other asset link.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import site_config as cfg  # noqa: E402

SKIP = ("prototypes/", "templates/", "node_modules/", ".git/")
MARK_OPEN = "<!-- nav-menu -->"
MARK_CLOSE = "<!-- /nav-menu -->"
ASSET = "nav-menu.js"

# 404.html is served for any URL at any depth, so a relative src resolves
# differently for /x.html than for /episodes/y.html. It uses root-absolute paths
# for everything else for that reason, and the prefix comes from site_config so
# it moves with the domain rather than hard-coding /Website/. audit.py checks
# this, and caught it when this tool first shipped a relative path here.
ABSOLUTE_PAGES = ("404.html",)


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


def prefix(page):
    """How this page has to reach the repo root, relative or root-absolute."""
    if page in ABSOLUTE_PAGES:
        return cfg.PATH
    depth = page.count("/")
    return "../" * depth


def main():
    n = skipped = 0
    for p in pages():
        h = open(p, encoding="utf-8", errors="replace").read()
        # Only pages that actually carry the header nav.
        if 'class="nav-links"' not in h:
            skipped += 1
            continue
        if "</body>" not in h:
            skipped += 1
            continue
        h = re.sub(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?",
                   "", h, flags=re.S)
        tag = '%s\n<script defer src="%s%s"></script>\n%s\n' % (
            MARK_OPEN, prefix(p), ASSET, MARK_CLOSE)
        h = h.replace("</body>", tag + "</body>", 1)
        open(p, "w", encoding="utf-8").write(h)
        n += 1
    print("nav menu script on %d pages  (%d pages have no header nav)" % (n, skipped))
    if n == 0:
        raise SystemExit("inject_nav_menu matched no pages, which cannot be right")


if __name__ == "__main__":
    main()
