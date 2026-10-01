#!/usr/bin/env python3
"""Evaluate a JS expression on a page at a size: python3 probe.py PAGE WxH WAIT_MS 'js expression (arrow fn body returning JSON)'"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lib
from run_viewport import router
page_path, size, wait, js = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
w, h = map(int, size.split("x")); mob = w < 900
with lib.server(8811) as base, lib.browser() as b:
    ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob, device_scale_factor=1)
    ctx.route("**/*", router(base))
    pg = ctx.new_page(); pg.goto(base + page_path, wait_until="load"); pg.wait_for_timeout(wait)
    print(json.dumps(pg.evaluate("() => {" + js + "}"), indent=1)[:6000])
