#!/usr/bin/env python3
"""Redirect stubs from the OLD paraglidingatlas.com URLs to the new pages.

WHY THIS EXISTS
paraglidingatlas.com is currently serving a different, older website. When the
domain is pointed at this repo that site disappears, and its addresses go with
it. The old site uses extensionless paths (`/about`, `/atlas/kenya`); this one
uses `about.html` and `destinations/kenya.html`. Without these stubs every
saved link, every share and anything still in an index lands on a 404.

MEASURED, NOT ASSUMED. The mapping below covers only URLs actually observed on
the live old site. `/trips` and `/faqs` were fetched and BOTH already return 404
there, so nothing is being lost for them; `/trips` is still mapped because it
costs nothing, `/faqs` is not because this site has no FAQ page to send it to.
Three old URLs have NO equivalent here and are deliberately absent rather than
pointed somewhere plausible: /passion, /faqs and /unsubscribe. Sending a reader
to a page that does not answer why they clicked is worse than a clean 404, and
404.html is a real page with the way back on it.

HOW THE REDIRECT WORKS
Each stub is a directory index, so `/about` and `/about/` both resolve without
relying on the server guessing an extension. It carries, in order:
  - `noindex`, so the stub itself never competes with its destination.
  - `canonical` at the destination, which is how a crawler that does read it
    still credits the right page.
  - a `<meta http-equiv="refresh">` at 0 seconds, which needs no JavaScript.
  - a visible link, so the page is not blank if refresh is blocked.
This is NOT a 301. GitHub Pages serves static files and cannot issue one. A
meta refresh is the strongest redirect available on this host and search engines
treat an instant one as equivalent. If a true 301 is ever needed, the user
already runs a Cloudflare Worker and that is where it would go.

Paths are RELATIVE so they survive the domain move untouched. The canonical is
absolute and comes from site_config, so it moves with DOMAIN and PATH like
everything else.

Run via ./build.sh, never on its own.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import site_config as cfg

# old path on paraglidingatlas.com  ->  page in this repo
REDIRECTS = {
    "about":         "about.html",
    "knowledge-base": "knowledge-base.html",
    "podcast":       "podcast.html",
    "atlas/kenya":   "destinations/kenya.html",
    "contact":       "enquire.html",
    "mission":       "mission.html",
    "privacy":       "privacy-policy.html",
    "trips":         "index.html#destinations",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>Moved: {title} | Paragliding Atlas</title>
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0; url={rel}">
<meta name="theme-color" content="#141519">
<style>
body{{background:#141519;color:#b4b4b4;font-family:system-ui,sans-serif;
  display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;padding:2rem;text-align:center;}}
a{{color:#ff7517;}}
</style>
</head>
<body>
<p>This page has moved.<br><a href="{rel}">Continue to {title}</a></p>
</body>
</html>
"""


def build():
    written = []
    for old, target in sorted(REDIRECTS.items()):
        depth = old.count("/") + 1          # /about -> about/index.html is one level down
        rel = "../" * depth + target
        canonical = cfg.BASE + target.split("#")[0]
        if "#" in target:
            canonical = cfg.BASE + target.split("#")[0]
        title = target.split("/")[-1].replace(".html", "").replace("-", " ").title()
        out = os.path.join(old, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        html = TEMPLATE.format(title=title, canonical=canonical, rel=rel)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(out)
    print("redirect stubs written: %d" % len(written))
    for w in written:
        print("   /%s  ->  %s" % (os.path.dirname(w), REDIRECTS[os.path.dirname(w)]))


if __name__ == "__main__":
    build()
