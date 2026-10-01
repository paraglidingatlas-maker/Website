"""Shared helpers for the website stress test. Read-only on the repo.

    import sys; sys.path.insert(0, "/home/user/Website/tools/stress")
    import lib
    with lib.server(8811) as base:            # base = "http://127.0.0.1:8811/"
        with lib.browser() as b:
            pg = b.new_page(viewport={"width": 390, "height": 844})
            pg.goto(base + lib.V4 + "index.html")

SITES: {"live": "", "v4": "prototypes/v4/"}: prefixes under the repo root.
pages(site) -> list of page paths relative to that site's prefix.
TEMPLATES[site] -> representative pages, one per template.
The server is a child process started for this block and killed after it:
never leave anything running.
"""
import contextlib
import json
import os
import re
import socket
import subprocess
import sys
import time

ROOT = "/home/user/Website"
OUT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
AXE = os.path.join(OUT, "node_modules", "axe-core", "axe.min.js")   # npm install axe-core@4 in tools/stress first
V4 = "prototypes/v4/"
SITES = {"live": "", "v4": V4}


def pages(site):
    if site == "live":
        s = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
        locs = re.findall(r"<loc>https://paraglidingatlas.com/([^<]*)</loc>", s)
        out = ["index.html" if not l else l for l in locs]
        return sorted(set(out + ["404.html"]))
    base = os.path.join(ROOT, V4)
    out = []
    for d, _, fs in os.walk(base):
        if "/src" in d:
            continue
        for f in fs:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(d, f), base).replace(os.sep, "/"))
    return sorted(out)


TEMPLATES = {
    "live": ["index.html", "destinations/kenya.html", "destinations/india.html", "enquire.html", "library.html",
             "podcast.html", "knowledge-base.html", "knowledge-base/flight-mechanics.html",
             "knowledge-base/navigators.html", "episodes/sky-gods-flying-8000ers-antoine-girard.html", "tags/safety.html",
             "sitemap.html", "404.html", "about.html", "partners.html"],
    "v4": ["index.html", "destinations/kenya.html", "destinations/india.html", "enquire.html", "library.html",
           "podcast.html", "knowledge-base.html", "knowledge-base/flight-mechanics.html", "knowledge-base/navigators.html",
           "episodes/sky-gods-flying-8000ers-antoine-girard.html", "tags/safety.html", "sitemap.html", "404.html",
           "about.html", "partners.html", "fly-options.html", "samples/drawings-all.html"],
}


def _free(port):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


@contextlib.contextmanager
def server(port):
    """Serve the repo root on port for this block only."""
    if not _free(port):
        raise SystemExit("port %d busy: pick another" % port)
    p = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=ROOT,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            if not _free(port):
                break
            time.sleep(.05)
        yield "http://127.0.0.1:%d/" % port
    finally:
        p.terminate()
        try:
            p.wait(5)
        except Exception:
            p.kill()


@contextlib.contextmanager
def browser(**kw):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME, **kw)
        try:
            yield b
        finally:
            b.close()


def own(url, base):
    """True when a request/console location belongs to the site (not an external host)."""
    return (url or "").startswith(base)


def save(name, data):
    fp = os.path.join(OUT, name)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, default=str)
    return fp
