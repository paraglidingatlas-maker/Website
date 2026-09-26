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
PROTO_ONLY = {"styleguide.html", "fly-options.html"}


def proto_only(rel):
    return rel in PROTO_ONLY or rel.startswith("samples/")


if not os.path.isdir(DIR):
    raise SystemExit("no such prototype: %s" % os.path.relpath(DIR, ROOT))
