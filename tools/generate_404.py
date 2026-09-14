#!/usr/bin/env python3
"""Build 404.html from its template so its paths move with the domain.

404.html has to use root-absolute paths: it is served for any URL at any depth,
so "assets/logo/favicon.png" would resolve differently for /x.html than for
/episodes/y.html. Root-absolute is correct, but it hard-codes the project path.

That made it the last thing standing between here and the custom domain. A dry
run of the move left 35 broken links and 2 missing preloads, every one of them
in this file, because nothing rewrote it. Now the prefix comes from
site_config.PATH like everything else.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import site_config as cfg

tpl = open(os.path.join(ROOT, "templates", "404-template.html"), encoding="utf-8").read()
out = tpl.replace("{{BASEPATH}}", cfg.PATH)
open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(out)
print("404.html written with base path %s" % cfg.PATH)
