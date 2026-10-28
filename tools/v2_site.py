#!/usr/bin/env python3
"""
Which prototype the v2 tools build and check: prototypes/v2 (the default) or
another copy of it, such as prototypes/v4.

Every tools/v2_*.py imports this. The site comes from `--site <name>` on the
command line (taken out of sys.argv here, so each tool's own argument parsing
never sees it), else from the PA_SITE environment variable, else "v2".

    python3 tools/v2_check.py --site v4
    python3 tools/v2_switch.py --site v4 --dry-run

With no setting every tool behaves exactly as before (v2 stays byte-identical).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _take_site():
    argv = sys.argv
    for i, a in enumerate(argv[1:], 1):
        if a == "--site" and i + 1 < len(argv):
            name = argv[i + 1]
            del argv[i:i + 2]
            return name
        if a.startswith("--site="):
            del argv[i]
            return a.split("=", 1)[1]
    return os.environ.get("PA_SITE") or "v2"


NAME = _take_site()
if not re.match(r"^v\d+$", NAME):
    raise SystemExit("--site must look like v2 or v4, not %r" % NAME)
IS_V2 = NAME == "v2"
DIR = os.path.join(ROOT, "prototypes", NAME)          # the prototype's folder
URL_PATH = "prototypes/%s/" % NAME                     # its path on the site
ASSET_DIR = "assets/%s" % NAME                         # where the switch copies its files
STAGE = "/tmp/claude-0/%s-stage" % NAME                # the switch rehearsal's staging copy
# Pages that exist only in the prototype (no live twin, never switched):
# the style guide, the fly options, and anything under samples/ (v4 before/after pages).
# offline.html is the v4 app's no-signal page (tools/v4_pwa.py), not a site page
PROTO_ONLY = {"styleguide.html", "fly-options.html", "offline.html",
              "book.html",  # the booking page: drafts, switched off, waiting on the owner
              # the immersion chat's option pages (imported 28 Oct): India's sections go into india.html
              # (tools/v4_india_immersive.py); Kenya's and the library's wait on the owner
              "destinations/india-e.html", "destinations/kenya-e.html", "library-e.html", "library-e1.html",
              "library-live.html"}  # what the switch publishes as library.html (LIVE_FROM)
# A live page published from another v4 file than its own (tools/v2_switch.py transform): the library in the
# immersion chat's design (tools/v4_library_live.py writes library-live.html), while prototypes/v4/library.html
# stays the page the build's own library passes work on (owner, 28 Oct 2026)
LIVE_FROM = {} if NAME == "v2" else {"library.html": "library-live.html"}
# record-attempt.html went live on the owner's go (27 Oct: "go live"), its [to supply] gaps showing


def proto_only(rel):
    # record-a/b/c.html: the record page's design options stay prototype-only
    return (rel in PROTO_ONLY or rel.startswith("samples/") or re.match(r"record-[a-z]\.html$", rel) is not None
            or rel.startswith("expeditions-")  # the expeditions page's design options (owner, 19 Oct)
            or rel.startswith("knowledge-base/encyclopedia/"))  # drafts until the owner has reviewed them (21 Oct)


# A part of a page that leads to a page the switch does not carry yet (a
# prototype-only page) sits between marks that name that page, relative to
# the prototype's root:
#     <!-- v4:needs record-attempt.html --> ... <!-- /v4:needs -->
# While the named page is prototype-only the part is dropped whole, marks and
# all; once it is switched only the marks go. The switch (tools/v2_switch.py)
# and the search (tools/v4_search.py) both read pages through this.
NEEDS_MARK = re.compile(r"<!--\s*(/?)\s*v4:needs\b([^>]*?)-->")
NEEDS_OPEN = re.compile(r"<!-- v4:needs ([\w./-]+\.html) -->")
NEEDS_CLOSE = "<!-- /v4:needs -->"
NEEDS_BLOCK = re.compile(r"<!-- v4:needs ([\w./-]+\.html) -->(.*?)<!-- /v4:needs -->", re.S)


def needs(src, root=None):
    """src with its v4:needs parts resolved, and a list of problems: an
    unbalanced or nested mark, a mark not written as above, or one that names
    no page of the prototype at root (DIR by default). With a problem, src
    comes back unchanged and the caller fails."""
    root = root or DIR
    problems, depth = [], 0
    for m in NEEDS_MARK.finditer(src):
        if m.group(1):
            if m.group(0) != NEEDS_CLOSE:
                problems.append("a v4:needs mark not written as %s: %s" % (NEEDS_CLOSE, m.group(0)))
            depth -= 1
            if depth < 0:
                problems.append("a closing v4:needs mark with no opening one")
                depth = 0
            continue
        o = NEEDS_OPEN.fullmatch(m.group(0))
        if not o:
            problems.append("a v4:needs mark not written as <!-- v4:needs PAGE.html -->: %s" % m.group(0))
        elif not os.path.isfile(os.path.join(root, o.group(1))):
            problems.append("a v4:needs mark names no page of the prototype: %s" % o.group(1))
        depth += 1
        if depth > 1:
            problems.append("a v4:needs mark inside another")
    if depth > 0:
        problems.append("a v4:needs mark is never closed")
    if problems:
        return src, problems
    return NEEDS_BLOCK.sub(lambda m: "" if proto_only(m.group(1)) else m.group(2), src), []


# Pages the prototype adds to the site (no live twin, but switched): the switch
# writes them at the root, indexable, and lists them in sitemap.xml; the checks
# hold them to their own title, description and canonical instead of a live page's.
# expeditions.html: the menu's Expeditions tab gets its own page (owner, 19 Oct)
NEW_PAGES = set() if IS_V2 else {"expeditions.html", "destinations/panchgani.html", "record-attempt.html"}     # Panchgani: a new tour (chat 11)


if not os.path.isdir(DIR):
    raise SystemExit("no such prototype: %s" % os.path.relpath(DIR, ROOT))
