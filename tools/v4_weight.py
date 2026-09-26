#!/usr/bin/env python3
"""
Bytes on arrival: what a page downloads before anyone scrolls, v4 against its
v2 twin (docs/v4-plan.md step 6: no v4 page heavier on arrival than v2).

Loads each page in Chromium at 1440 x 900, waits for the network to settle,
and sums every response from the preview server as the network would carry
it: text (HTML, CSS, JS, JSON, SVG) gzipped, as GitHub Pages serves it, and
binaries (images, fonts, video) as they are. The blocked third-party hosts
(YouTube, the feed) are left out: they are the same for both. Run with the
preview server up.

    python3 tools/v4_weight.py                     # the key pages
    python3 tools/v4_weight.py podcast.html index.html
    python3 tools/v4_weight.py --phone             # 390 x 844 as a touch phone
Each page is loaded three times per site and the lightest load counts.
"""
import gzip
import re
import sys

PAGES = ["index.html", "podcast.html", "library.html", "about.html", "destinations/india.html",
         "destinations/kenya.html", "knowledge-base.html", "knowledge-base/flight-mechanics.html",
         "tags/safety.html", "episodes/navigating-india-eddie-colfox.html",
         "episodes/anatomy-of-a-dream-with-damien-lacaze.html", "terms.html"]
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


def weigh(pg, url):
    sizes = {}

    def on(resp):
        if "127.0.0.1:8765" not in resp.url:
            return
        try:
            b = resp.body()
            text = re.search(r"\.(html?|css|js|json|svg|txt)(\?|$)", resp.url) or resp.url.endswith("/")
            sizes[resp.url] = len(gzip.compress(b, 6)) if text else len(b)
        except Exception:     # noqa: BLE001 - redirects, aborted media
            pass
    pg.on("response", on)
    pg.goto(url, wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(1500)
    pg.remove_listener("response", on)
    return sum(sizes.values()), sizes


def main(pages):
    from playwright.sync_api import sync_playwright
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for r in pages:
            res = []
            for site in ("v2", "v4"):
                # the lowest of RUNS loads: a font wanted only by hidden text (an accented name on a
                # card further down the list) is fetched or not depending on timing, in v2 and v4 alike
                best = None
                for _ in range(RUNS):
                    ctx = (b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
                           if PHONE else b.new_context(viewport={"width": 1440, "height": 900}))
                    pg = ctx.new_page()
                    got = weigh(pg, "http://127.0.0.1:8765/prototypes/%s/%s" % (site, r))
                    ctx.close()
                    if best is None or got[0] < best[0]:
                        best = got
                res.append(best)
            (a, sa), (c, sc) = res
            flag = "ok " if c <= a else "OVER"
            print("%s %-50s v2 %7.0f KB   v4 %7.0f KB   %+6.0f KB" % (flag, r, a / 1024, c / 1024, (c - a) / 1024))
            rows.append((r, a, c, sa, sc))
        b.close()
    return rows


PHONE = "--phone" in sys.argv
RUNS = 3

if __name__ == "__main__":
    rows = main([a for a in sys.argv[1:] if not a.startswith("--")] or PAGES)
    if "--why" in sys.argv:
        pass
