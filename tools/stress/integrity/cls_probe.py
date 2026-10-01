"""Load-time CLS, by cause.

    python3 cls_probe.py [variant ...] [--pages P ...] [--profile phone-slow|phone|desktop]

variants: normal  nofonts (woff2 aborted: fallback font throughout, no swap)  nonav (nav-menu.js aborted)
          noimg (all images aborted)  reducedmotion (prefers-reduced-motion: reduce)
Only load-time shifts are measured (no scrolling): goto(load) + 2.5 s. i.ytimg.com thumbnails are fulfilled
with a 320x180 stand-in, as in production. Port 8816.
"""
import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib  # noqa: E402
from browser_check import CLS_INIT, session_cls, fake_thumb  # noqa: E402

A = sys.argv[1:]


def opt(name, default):
    if name in A:
        i = A.index(name)
        vals = []
        for x in A[i + 1:]:
            if x.startswith("--"):
                break
            vals.append(x)
        return vals
    return default


VARIANTS = [a for a in A[:A.index(next((x for x in A if x.startswith("--")), "--"))] if not a.startswith("--")] \
    if any(x.startswith("--") for x in A) else [a for a in A]
VARIANTS = VARIANTS or ["normal", "nofonts", "nonav"]
PAGES = opt("--pages", lib.TEMPLATES["live"])
PROFILE = opt("--profile", ["phone-slow"])[0]
PROFILES = {
    "phone-slow": ({"width": 390, "height": 844}, dict(latency=150, downloadThroughput=200000, uploadThroughput=90000)),
    "phone": ({"width": 390, "height": 844}, None),
    "desktop": ({"width": 1280, "height": 800}, None),
    "desktop-slow": ({"width": 1280, "height": 800}, dict(latency=150, downloadThroughput=200000,
                                                          uploadThroughput=90000)),
}

out = {}
yt = fake_thumb()
vp, net = PROFILES[PROFILE]
with lib.server(8816) as base:
    with lib.browser() as b:
        for variant in VARIANTS:
            for p in PAGES:
                ctx = b.new_context(viewport=vp, reduced_motion="reduce" if variant == "reducedmotion" else "no-preference")

                def make_handler(variant):
                    # Playwright passes (route, request) to a two-argument handler, so the variant is bound
                    # in a closure rather than as a default argument.
                    def handler(route):
                        u = route.request.url
                        if "i.ytimg.com" in u:
                            return route.fulfill(status=200, content_type="image/jpeg", body=yt)
                        if not u.startswith(base):
                            return route.abort()
                        if variant == "nofonts" and u.split("?")[0].endswith(".woff2"):
                            return route.abort()
                        if variant == "nonav" and "nav-menu.js" in u:
                            return route.abort()
                        if variant == "noimg" and route.request.resource_type == "image":
                            return route.abort()
                        return route.continue_()
                    return handler
                handler = make_handler(variant)
                ctx.route("**/*", handler)
                ctx.add_init_script(CLS_INIT)
                pg = ctx.new_page()
                if net:
                    cdp = ctx.new_cdp_session(pg)
                    cdp.send("Network.enable")
                    cdp.send("Network.emulateNetworkConditions", dict(offline=False, **net))
                t0 = time.time()
                pg.goto(base + p, wait_until="load", timeout=60000)
                ld = time.time() - t0
                pg.wait_for_timeout(2500)
                ent = pg.evaluate("() => window.__ls")
                has_toggle = pg.evaluate("() => !!document.querySelector('.nav-toggle')")
                top = sorted([e for e in ent if not e["r"]], key=lambda e: -e["v"])[:3]
                out.setdefault(variant, {})[p] = dict(cls=round(session_cls(ent), 4), load_s=round(ld, 1), nav_toggle=has_toggle,
                                                      top=[dict(t=round(e["t"]), v=round(e["v"], 4),
                                                                src=e["src"][:2]) for e in top])
                print("%-8s %-10s %-55s CLS %.4f  load %.1fs  toggle=%s  %s" % (
                    PROFILE, variant, p, out[variant][p]["cls"], ld, has_toggle,
                    "; ".join("%s %s->%s" % (s["node"], s["prev"], s["cur"]) for e in top[:1] for s in e["src"][:2])),
                    flush=True)
                ctx.close()
print("saved", lib.save("integrity/cls_probe_%s.json" % PROFILE, out))
