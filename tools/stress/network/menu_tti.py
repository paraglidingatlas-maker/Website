#!/usr/bin/env python3
"""When can a phone visitor on a slow network open the site menu?

    python3 menu_tti.py [page ...] [--profile slow3g|fast3g]

Phone viewport (390x844). Below 820px the header links are display:none and the
only way to them is the .nav-toggle button, which nav-menu.js (defer) inserts at
DOMContentLoaded. Polls every 250 ms from navigation: first paint of the nav bar,
when the toggle exists, and whether a real tap on it opens the menu.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import lib  # noqa: E402

PORT = 8812
NET = {"slow3g": dict(latency=400, downloadThroughput=50000, uploadThroughput=50000),
       "fast3g": dict(latency=150, downloadThroughput=200000, uploadThroughput=93750)}
DEFAULT = ["index.html", "knowledge-base.html", "destinations/kenya.html", "destinations/india.html",
           "library.html", "podcast.html", "enquire.html", "episodes/sky-gods-flying-8000ers-antoine-girard.html"]

POLL = r"""() => {
  const nav = document.querySelector('.page-wrap > nav');
  const r = nav ? nav.getBoundingClientRect() : null;
  const links = nav ? nav.querySelector('.nav-links') : null;
  const t = document.querySelector('.nav-toggle');
  const tr = t ? t.getBoundingClientRect() : null;
  const fcp = (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime;
  return {t: Math.round(performance.now()), ready: document.readyState, fcp: fcp ? Math.round(fcp) : null,
          nav: !!(r && r.height > 0), linksShown: !!(links && getComputedStyle(links).display !== 'none'),
          toggle: !!(tr && tr.width > 0 && tr.height > 0)};
}"""


def run(b, base, path, prof):
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    cdp.send("Network.emulateNetworkConditions", dict(offline=False, **NET[prof]))
    page.goto(base + path, wait_until="commit", timeout=60000)
    t0 = time.time()
    first_nav = first_fcp = toggle_at = opened_at = dcl = None
    while time.time() - t0 < 90:
        try:
            s = page.evaluate(POLL)
        except Exception:
            page.wait_for_timeout(250)
            continue
        if s["fcp"] and first_fcp is None:
            first_fcp = s["fcp"]
        if s["nav"] and first_nav is None and s["fcp"]:
            first_nav = s["t"]
        if s["ready"] != "loading" and dcl is None:
            dcl = s["t"]
        if s["toggle"] and toggle_at is None:
            toggle_at = s["t"]
            try:
                page.tap(".nav-toggle", timeout=3000)
                page.wait_for_timeout(400)
                opened = page.evaluate("() => { const n=document.querySelector('.page-wrap > nav'); const l=n.querySelector('.nav-links'); const r=l.getBoundingClientRect(); return n.classList.contains('is-open') && r.height > 0 && getComputedStyle(l).display !== 'none'; }")
                if opened:
                    opened_at = page.evaluate("() => Math.round(performance.now())")
            except Exception as e:
                opened_at = "tap failed: %s" % str(e)[:80]
            break
        page.wait_for_timeout(250)
    ctx.close()
    gap = (toggle_at - first_fcp) if (toggle_at and first_fcp) else None
    return {"path": path, "profile": prof, "fcp_ms": first_fcp, "dom_interactive_ms": dcl, "toggle_present_ms": toggle_at,
            "menu_opened_ms": opened_at, "no_menu_after_paint_ms": gap}


def main():
    prof = "slow3g"
    argv = sys.argv[1:]
    if "--profile" in argv:
        i = argv.index("--profile")
        prof = argv[i + 1]
        del argv[i:i + 2]
    pages = argv or DEFAULT
    out = []
    with lib.server(PORT) as base, lib.browser() as b:
        for p in pages:
            r = run(b, base, p, prof)
            out.append(r)
            print(json.dumps(r))
    lib.save("network/out/menu_tti_%s.json" % prof, out)


if __name__ == "__main__":
    main()
