#!/usr/bin/env python3
"""Interaction checks. The audit reads files; this one uses the site.

WHY THIS EXISTS: the homepage rail stopped opening its popup in f2a5381 and
nobody noticed until a user reported it, months later. It survived 104 audit
checks because not one of them clicks anything. Everything here is a thing that
has actually broken, or the guard on a thing that has.

    python3 tools/smoke.py

Serves the repo on a free port, drives a real browser, exits non-zero on failure.
Skips cleanly if Playwright or its browser is missing, so it never blocks a
build on a machine that cannot run it.
"""
import http.server
import os
import socket
import socketserver
import sys
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")

FAILS, CHECKS = [], []


def check(ok, group, msg, detail=""):
    CHECKS.append(ok)
    if not ok:
        FAILS.append((group, msg, detail))
    print("%s  %-11s %s%s" % ("  ok" if ok else "FAIL", group, msg,
                              "" if ok else "   " + str(detail)))


def serve():
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=ROOT, **k)

        def log_message(self, *a):
            pass

    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    httpd = socketserver.TCPServer(("127.0.0.1", port), H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, "http://127.0.0.1:%d" % port


def rail(pg, base):
    """The homepage strip: a click opens the popup, a swipe must not."""
    pg.goto(base + "/index.html", wait_until="load")
    pg.wait_for_timeout(2500)
    pg.evaluate("document.querySelector('.ep-card').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(1000)

    def point():
        return pg.evaluate("""()=>{for(const c of document.querySelectorAll('.ep-card')){
            const r=c.getBoundingClientRect();
            if(r.left>60&&r.right<innerWidth-60&&r.width>40)
              return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)};}
            return null;}""")

    def open_state():
        return pg.evaluate("()=>{const o=document.getElementById('epModalOverlay');"
                           "return !!o&&o.className.includes('active');}")

    p = point()
    if not p:
        check(False, "rail", "a card was reachable to click")
        return
    pg.mouse.move(p["x"], p["y"]); pg.mouse.down(); pg.wait_for_timeout(90); pg.mouse.up()
    pg.wait_for_timeout(900)
    check(open_state(), "rail", "one click on a card opens the popup")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)

    p = point()
    pg.mouse.move(p["x"], p["y"]); pg.mouse.down()
    for k in range(1, 9):
        pg.mouse.move(p["x"] - k * 14, p["y"]); pg.wait_for_timeout(16)
    pg.mouse.up(); pg.wait_for_timeout(800)
    check(not open_state(), "rail", "a swipe does not open the popup")
    if open_state():
        pg.keyboard.press("Escape")


def nav(pg, base):
    """The phone menu. Four links were unreachable on 181 pages before it."""
    pg.set_viewport_size({"width": 390, "height": 800})
    pg.goto(base + "/index.html", wait_until="load")
    pg.wait_for_timeout(1200)
    btn = pg.query_selector(".nav-toggle")
    check(bool(btn) and btn.is_visible(), "nav", "menu button is present under 940px")
    if not btn:
        return
    b = btn.bounding_box()
    check(b and b["width"] >= 44 and b["height"] >= 44, "nav",
          "menu button is at least a 44px target",
          b and "%dx%d" % (b["width"], b["height"]))
    btn.click()
    pg.wait_for_timeout(400)
    n = pg.evaluate("[...document.querySelectorAll('.nav-links a')]"
                    ".filter(a=>a.getBoundingClientRect().height>0).length")
    check(n == 4, "nav", "opening the menu reveals all four links", "got %d" % n)
    check(pg.evaluate("document.querySelector('.nav-toggle').getAttribute('aria-expanded')") == "true",
          "nav", "aria-expanded follows the open state")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    check(pg.evaluate("document.querySelector('.nav-toggle').getAttribute('aria-expanded')") == "false",
          "nav", "Escape closes the menu")
    pg.set_viewport_size({"width": 1280, "height": 900})
    pg.goto(base + "/index.html", wait_until="load")
    pg.wait_for_timeout(900)
    t = pg.query_selector(".nav-toggle")
    check(not (t and t.is_visible()), "nav", "menu button is hidden above 940px")


def player(pg, base):
    """The audio player. These pages had no playback at all before it."""
    pg.set_viewport_size({"width": 1280, "height": 900})
    pg.goto(base + "/episodes/maxime-pinot-the-journey-within.html", wait_until="load")
    pg.wait_for_timeout(1200)
    d = pg.evaluate("""()=>{const r=document.querySelector('.ep-au');
      if(!r) return null;
      const chaps=[...r.querySelectorAll('.ep-au-chap')];
      const dur=parseFloat(r.dataset.duration||'0');
      return {play:!!r.querySelector('.ep-au-play'), audio:!!r.querySelector('audio'),
              src:(r.querySelector('audio')||{}).src||'',
              chaps:chaps.length,
              inRange:chaps.every(c=>{const t=parseFloat(c.dataset.at);
                 const l=parseFloat(c.style.left); return t>0&&t<dur&&l>0&&l<100;}),
              dur:dur};}""")
    check(bool(d), "player", "the audio player is on the page")
    if not d:
        return
    check(d["play"] and d["audio"] and d["src"].startswith("http"), "player",
          "play button and a real audio source")
    check(d["chaps"] > 0, "player", "chapter marks are rendered", d["chaps"])
    check(d["inRange"], "player", "every chapter mark sits inside the episode")


def overflow(pg, base):
    """Sideways scroll. The homepage had 59px of it at 390 until today."""
    pages = ["index.html", "about.html", "podcast.html", "destinations/kenya.html",
             "enquire.html", "library.html", "tags.html",
             "episodes/maxime-pinot-the-journey-within.html",
             "knowledge-base/sky-gods.html", "terms.html"]
    pg.set_viewport_size({"width": 390, "height": 844})
    bad = []
    for p in pages:
        pg.goto(base + "/" + p, wait_until="load")
        pg.wait_for_timeout(500)
        o = pg.evaluate("document.documentElement.scrollWidth-window.innerWidth")
        if o > 0:
            bad.append("%s +%dpx" % (p, o))
    check(not bad, "layout", "no page scrolls sideways at 390px", bad)


def errors(pg, base):
    """Uncaught script errors on the pages that carry the most behaviour."""
    seen = []
    pg.on("pageerror", lambda e: seen.append(str(e)[:90]))
    pg.set_viewport_size({"width": 1280, "height": 900})
    for p in ["index.html", "library.html", "knowledge-base/sky-gods.html",
              "episodes/maxime-pinot-the-journey-within.html"]:
        pg.goto(base + "/" + p, wait_until="load")
        pg.wait_for_timeout(1400)
    check(not seen, "scripts", "no uncaught errors on the interactive pages", seen[:3])


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed, skipping interaction checks")
        return 0

    httpd, base = serve()
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except Exception as e:
                print("no browser available, skipping interaction checks (%s)" % str(e)[:60])
                return 0
            pg = browser.new_page(viewport={"width": 1280, "height": 900},
                                  reduced_motion="no-preference")
            for fn in (rail, nav, player, overflow):
                fn(pg, base)
            pg.close()
            pg2 = browser.new_page(viewport={"width": 1280, "height": 900},
                                   reduced_motion="reduce")
            errors(pg2, base)
            pg2.close()
            browser.close()
    finally:
        httpd.shutdown()

    print("\n%d interaction checks | %d FAIL" % (len(CHECKS), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
