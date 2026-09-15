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
import tempfile
import sys
import threading
import time

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

    # NOT "is it positioned correctly" but "can a person see and press it". The
    # player once laid out perfectly, reported the right size and position, and
    # was clipped out of sight by an ancestor's overflow:hidden. Geometry checks
    # all passed. A hit test at the button's own centre is what catches that.
    for vw in (1280, 390):
        pg.set_viewport_size({"width": vw, "height": 900})
        pg.evaluate("document.querySelector('.cd-player-audio').scrollIntoView({block:'center'})")
        pg.wait_for_timeout(400)
        hit = pg.evaluate("""()=>{const el=document.querySelector('.ep-au-play');
          if(!el) return false;
          const r=el.getBoundingClientRect();
          if(r.width<1||r.height<1) return false;
          const h=document.elementFromPoint(Math.round(r.left+r.width/2),
                                            Math.round(r.top+r.height/2));
          return !!(h && (h===el || el.contains(h)));}""")
        check(hit, "player", "the play button is actually clickable at %dpx" % vw)
    pg.set_viewport_size({"width": 1280, "height": 900})


def globe(pg, base):
    """The globe was measured once, at the width the page first loaded at.

    Nothing listened for resize, so rotating a phone or narrowing a window left
    the projection at the old size: the sphere overflowed its container and the
    pins sat outside the screen, which is why that area stopped responding to
    taps. Loading wide and then narrowing is the case that caught it.

    Runs under reduced motion on purpose. The globe auto-rotates otherwise, so a
    pin measured and then clicked has moved in between and the check fails at
    random. The question here is geometry, which rotation does not affect."""
    pg.set_viewport_size({"width": 1280, "height": 900})
    pg.goto(base + "/index.html", wait_until="load")
    pg.wait_for_timeout(2500)
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.wait_for_timeout(1200)
    pg.evaluate("document.getElementById('epMap').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(700)
    d = pg.evaluate("""()=>{const m=document.getElementById('epMap');
      if(!m) return null;
      const c=m.querySelector('circle'), r=m.getBoundingClientRect();
      if(!c) return {fits:false, pin:null};
      const rad=+c.getAttribute('r');
      const pins=[...m.querySelectorAll('g.pin')];
      let pin=null;
      for(const p of pins){const b=p.getBoundingClientRect();
        if(b.width>0&&b.top>0&&b.bottom<innerHeight&&b.left>0&&b.right<innerWidth){
          pin=[Math.round(b.left+b.width/2),Math.round(b.top+b.height/2)];break;}}
      return {fits: rad>4 && rad*2<=Math.min(r.width,r.height)+2, pin:pin};}""")
    check(bool(d) and d["fits"], "globe",
          "the sphere still fits its container after a width change")
    if d and d["pin"]:
        pg.mouse.click(d["pin"][0], d["pin"][1])
        pg.wait_for_timeout(900)
        check(pg.evaluate("document.getElementById('mapPopup').classList.contains('visible')"),
              "globe", "a pin is clickable after a width change")
    else:
        check(False, "globe", "a pin is clickable after a width change",
              "no pin landed on screen")
    pg.set_viewport_size({"width": 1280, "height": 900})


def touch_gestures(browser, base):
    """One finger rotates, two fingers zoom, and neither does the other's job.

    Real touch events through the browser input pipeline, not synthetic ones in
    JS, because the thing that broke this was event ordering: d3-drag calls
    stopImmediatePropagation on touchmove, so the pinch handler has to run in the
    capture phase to be reached at all. A JS-dispatched event would not exercise
    that."""
    ctx = browser.new_context(viewport={"width": 390, "height": 844},
                              has_touch=True, is_mobile=True,
                              reduced_motion="reduce")
    pg = ctx.new_page()
    cdp = ctx.new_cdp_session(pg)
    try:
        pg.goto(base + "/index.html", wait_until="load")
        pg.wait_for_timeout(2800)
        pg.evaluate("document.getElementById('epMap').scrollIntoView({block:'center'})")
        pg.wait_for_timeout(800)
        c = pg.evaluate("""()=>{const r=document.getElementById('epMap').getBoundingClientRect();
            return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)};}""")
        rad = lambda: pg.evaluate("+document.querySelector('#epMap circle').getAttribute('r')")
        rot = lambda: pg.evaluate(
            "document.querySelectorAll('#epMap path')[0].getAttribute('d').slice(0,80)")

        r0, a0 = rad(), rot()
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart",
                 "touchPoints": [{"x": c["x"], "y": c["y"], "id": 1}]})
        for i in range(1, 10):
            cdp.send("Input.dispatchTouchEvent", {"type": "touchMove",
                     "touchPoints": [{"x": c["x"] + i * 11, "y": c["y"], "id": 1}]})
            time.sleep(0.02)
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
        pg.wait_for_timeout(600)
        check(rot() != a0, "touch", "one finger rotates the globe")
        check(abs(rad() - r0) < 1, "touch", "one finger does not zoom it")

        r1 = rad()
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart",
                 "touchPoints": [{"x": c["x"] - 30, "y": c["y"], "id": 1}]})
        time.sleep(0.04)
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [
                 {"x": c["x"] - 30, "y": c["y"], "id": 1},
                 {"x": c["x"] + 30, "y": c["y"], "id": 2}]})
        for i in range(1, 9):
            g = 30 + i * 14
            cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [
                     {"x": c["x"] - g, "y": c["y"], "id": 1},
                     {"x": c["x"] + g, "y": c["y"], "id": 2}]})
            time.sleep(0.03)
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
        pg.wait_for_timeout(700)
        check(rad() > r1 * 1.05, "touch", "two fingers pinch to zoom in",
              "%d -> %d" % (r1, rad()))
    finally:
        ctx.close()


def library(pg, base):
    """The library opens on a landing screen, not a grid.

    Worth stating because it looks broken otherwise: #eps is empty and hidden on
    load, and only fills once you choose All or a series. That is by design, and
    checking it here means nobody has to rediscover it."""
    pg.set_viewport_size({"width": 1280, "height": 900})
    pg.goto(base + "/library.html", wait_until="load")
    pg.wait_for_timeout(2500)
    btn = pg.query_selector("#allBtn")
    check(bool(btn) and btn.is_visible(), "library", "the landing screen offers a way in")
    if not btn:
        return
    btn.click()
    pg.wait_for_timeout(1800)
    n = pg.evaluate("(document.getElementById('eps')||{children:[]}).children.length")
    check(n > 50, "library", "choosing All fills the grid", "%s rows" % n)
    card = pg.query_selector("#eps a")
    if card:
        card.click()
        pg.wait_for_timeout(1200)
        check(pg.evaluate("()=>{const o=document.getElementById('epModalOverlay');"
                          "return !!o&&o.className.includes('active');}"),
              "library", "a library card opens the popup")
    else:
        check(False, "library", "a library card opens the popup", "no card rendered")


def search(pg, base):
    """The homepage episode search, including what it says when it finds nothing."""
    pg.goto(base + "/index.html", wait_until="load")
    pg.wait_for_timeout(2500)
    pg.fill("#epSearchInput", "reserve")
    pg.click("#epSearchBtn")
    pg.wait_for_timeout(1200)
    n = pg.evaluate("document.getElementById('epSearchResults').children.length")
    check(n > 0, "search", "a real query returns results", "%s results" % n)
    pg.fill("#epSearchInput", "zzzqqqxyz")
    pg.click("#epSearchBtn")
    pg.wait_for_timeout(1000)
    txt = pg.evaluate("document.getElementById('epSearchResults').textContent.trim()")
    check(len(txt) > 0, "search", "a query with no matches says so, rather than going blank")


def kenya(pg, base):
    """24 accordions carry most of the copy on the longest page on the site."""
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1500)
    n = pg.evaluate("document.querySelectorAll('details').length")
    check(n > 10, "kenya", "the accordions are present", n)
    if not n:
        return
    pg.evaluate("document.querySelector('details').open=false")
    pg.wait_for_timeout(200)
    h0 = pg.evaluate("document.querySelector('details').getBoundingClientRect().height")
    pg.click("details summary")
    pg.wait_for_timeout(400)
    h1 = pg.evaluate("document.querySelector('details').getBoundingClientRect().height")
    check(h1 > h0 + 10, "kenya", "clicking one opens it", "%d -> %d px" % (h0, h1))


def enquire(pg, base):
    """The enquiry form is the only page that asks for something back.

    It has no action and no method: submitting builds a mailto. That is
    deliberate, there being no backend, and it says so on screen if no mail app
    picks it up. What must not break is the validation and the labelling."""
    pg.goto(base + "/enquire.html", wait_until="load")
    pg.wait_for_timeout(1200)
    d = pg.evaluate("""()=>{const f=document.getElementById('enqForm');
      if(!f) return null;
      const fields=[...f.querySelectorAll('input,select,textarea')];
      return {fields:fields.length, required:fields.filter(x=>x.required).length,
              unlabelled:fields.filter(x=>!x.id||!f.querySelector('label[for="'+x.id+'"]')).length,
              blocksEmpty:!f.checkValidity()};}""")
    check(bool(d), "enquire", "the form is on the page")
    if not d:
        return
    check(d["unlabelled"] == 0, "enquire", "every field has a label",
          "%s unlabelled" % d["unlabelled"])
    check(d["required"] > 0 and d["blocksEmpty"], "enquire",
          "an empty form will not submit")


def kenya_hero(pg, base):
    """The full bleed hero on the Kenya page.

    The swipe is the part worth guarding: an image is draggable by default, so a
    swipe across one starts a native drag and the browser sends pointercancel
    instead of pointerup. The gesture died on the way out and the slide never
    moved. Three separate things now stop it and any one of them is sufficient,
    so this only goes red when all three are gone. That is the real broken
    state, and it is what this was verified against.

    Full bleed is checked as a measurement, not an assumption. The hero is
    pulled up under a 92px transparent nav by a hard coded negative margin: if
    the nav ever changes height, the seam shows here first."""
    pg.set_viewport_size({"width": 1280, "height": 900})
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1800)
    cur = lambda: pg.evaluate("[...document.querySelectorAll('.khero-slide')]"
                              ".findIndex(s=>s.classList.contains('is-on'))")

    n = pg.evaluate("document.querySelectorAll('.khero-slide').length")
    check(n == 5, "hero", "all five photographs are on the page", n)
    check(pg.evaluate("[...document.querySelectorAll('.khero-slide')]"
                      ".filter(s=>getComputedStyle(s).visibility!=='hidden').length") == 1,
          "hero", "exactly one photograph is visible at a time")

    box = pg.evaluate("()=>{const r=document.querySelector('.khero').getBoundingClientRect();"
                      "return {t:Math.round(r.top),h:Math.round(r.height),w:Math.round(r.width),"
                      "vh:innerHeight,vw:innerWidth};}")
    check(box["t"] <= 0, "hero", "the photograph reaches the top of the screen", box["t"])
    check(box["h"] >= box["vh"] * 0.95, "hero", "the hero fills the viewport height",
          f"{box['h']} of {box['vh']}")
    check(box["w"] >= box["vw"], "hero", "the hero is full bleed", f"{box['w']} of {box['vw']}")

    # Autoplay. Silent to a reader and invisible in a screenshot, so it gets a
    # real wait rather than a check that the timer was merely armed.
    check(pg.evaluate("!!document.querySelector('.khero-tab.is-timing')"),
          "hero", "autoplay arms on load")
    a = cur()
    pg.wait_for_timeout(7600)
    check(cur() != a, "hero", "autoplay advances on its own", f"{a} then {cur()}")

    pg.evaluate("document.querySelectorAll('.khero-tab')[3].click()")
    pg.wait_for_timeout(700)
    check(cur() == 3, "hero", "a rail label jumps to its photograph", cur())
    check(not pg.evaluate("!!document.querySelector('.khero-tab.is-timing')"),
          "hero", "autoplay stops for good once a choice is made")
    check(pg.eval_on_selector(".khero-copy .kicker", "e=>e.textContent").strip() ==
          pg.eval_on_selector(".khero-tab.is-on", "e=>e.textContent").strip(),
          "hero", "the kicker names the photograph on screen")

    before = cur()
    # The start point has to be ON the image. The first version of this swiped
    # at 640,700, which is the CTA block: no image under the pointer means no
    # native drag, so it passed against a build with all three fixes stripped
    # out and was guarding nothing. Assert the target rather than trust the
    # coordinate, because the layout will move again.
    tgt = pg.evaluate("()=>{const e=document.elementFromPoint(1100,700);"
                      "return e ? e.tagName : 'none';}")
    check(tgt == "IMG", "hero", "the swipe test starts on the photograph itself", tgt)
    # ONE fast movement, not a stepped drag. The native image drag only kicks in
    # on a quick flick, and a stepped move does not reproduce it at all.
    pg.mouse.move(1100, 700)
    pg.mouse.down()
    pg.mouse.move(950, 700)
    pg.mouse.up()
    pg.wait_for_timeout(700)
    check(cur() != before, "hero", "a quick swipe across the photograph changes it")

    pg.evaluate("window.scrollTo(0,400)")
    pg.wait_for_timeout(400)
    check(pg.evaluate("getComputedStyle(document.querySelector('.khero-par')).transform")
          not in ("none", "matrix(1, 0, 0, 1, 0, 0)"),
          "hero", "the photograph drifts against the scroll")


def kenya_map(pg, base):
    """The two state route map.

    The lazy load is the part worth guarding. The sheet is fetched on first
    open, so a wrong path or a rename fails silently: the button does nothing
    and the page looks fine. Nothing else on the page would notice.

    Marker positions are also checked for movement between the two states,
    because both sets are generated from the projections in tools/ and baked
    into data-plate and data-sheet. If a regeneration ever emits one set for
    both, the pins would sit still and still look plausible."""
    pg.set_viewport_size({"width": 1400, "height": 900})
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1500)
    pg.evaluate("document.querySelector('.kmap').scrollIntoView({block:'start'})")
    pg.wait_for_timeout(900)

    n = pg.evaluate("document.querySelectorAll('.kmap-pin').length")
    check(n == 6, "map", "all six sites are markers on the map", n)
    check(pg.evaluate("document.querySelectorAll('.kmap-row').length") == 6,
          "map", "all six sites are in the list")
    check(pg.evaluate("!!document.querySelector('.kmap-pin').style.left"),
          "map", "markers are positioned from their coordinates")
    check(pg.evaluate("[...document.querySelectorAll('.kmap-pin-name')]"
                      ".filter(e=>getComputedStyle(e).opacity!=='0').length") == 1,
          "map", "exactly one marker label shows at a time")

    pg.evaluate("document.querySelectorAll('.kmap-row')[4].click()")
    pg.wait_for_timeout(400)
    txt = pg.eval_on_selector(".kmap-panel", "e=>e.innerText")
    check("Machakos" in txt, "map", "choosing a site fills the panel", txt[:40])
    check(pg.evaluate("document.querySelectorAll('.kmap-pin')[4]"
                      ".classList.contains('is-on')"),
          "map", "the list and the map stay in step")

    # the chart must not be in the document until it is asked for
    check(pg.evaluate("document.querySelector('.kmap-sheet').children.length") == 0,
          "map", "the chart is not loaded until it is opened")
    before = pg.evaluate("document.querySelector('.kmap-pin').style.left")
    pg.click(".kmap-zoom")
    pg.wait_for_timeout(2600)
    check(pg.evaluate("document.querySelector('.kmap-sheet').querySelectorAll('svg').length") > 0,
          "map", "the chart loads when opened")
    check(pg.evaluate("document.querySelector('.kmap-stage').classList.contains('is-sheet')"),
          "map", "opening the chart switches the map state")
    after = pg.evaluate("document.querySelector('.kmap-pin').style.left")
    check(before != after, "map", "markers move to their position on the chart",
          f"{before} then {after}")

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(900)
    check(not pg.evaluate("document.querySelector('.kmap-stage').classList.contains('is-sheet')"),
          "map", "escape returns to the overview")

    # ---- pan and zoom ----------------------------------------------------
    tf = lambda: pg.evaluate("getComputedStyle(document.querySelector('.kmap-view')).transform")
    scale = lambda: pg.evaluate(
        "()=>{const m=getComputedStyle(document.querySelector('.kmap-view'))"
        ".transform.match(/matrix\\(([\\d.]+)/);return m?+m[1]:1}")
    check(abs(scale() - 1) < 0.01, "map", "the map starts unzoomed", scale())
    # Markers sit outside the transform surface and are positioned in px. Put
    # them back inside it and a counter-scale is needed, which lays the label
    # out at 12px, rasterises the glyphs at under 2px and lets the parent blow
    # that bitmap back up.
    #
    # getBoundingClientRect cannot see this: it returns the final composited
    # size, 115x22 either way, so a box comparison passes against the broken
    # build. The damage is in the pixels, so the pixels are what get measured.
    pg.evaluate("document.querySelector('[data-z=\"in\"]').click()")
    pg.wait_for_timeout(500)
    check(scale() > 1.3, "map", "the zoom control zooms in", scale())

    sc = pg.evaluate("()=>{const m=getComputedStyle(document.querySelector('.kmap-pin'))"
                     ".transform.match(/matrix\\(([\\d.]+)/);return m?+m[1]:1}")
    check(abs(sc - 1) < 0.01, "map", "markers are never scaled themselves", sc)

    shot = os.path.join(tempfile.gettempdir(), "kmap-label.png")
    try:
        pg.locator(".kmap-pin.is-on .kmap-pin-name").screenshot(path=shot)
        from PIL import Image
        im = Image.open(shot).convert("L")
        px = list(im.getdata())
        w, h = im.size
        # mean absolute difference between neighbouring pixels: crisp glyph edges
        # give a high number, an upscaled 2px raster gives a low one
        edges = sum(abs(px[i] - px[i - 1]) for i in range(1, len(px)) if i % w) / max(1, len(px))
        check(edges > 6, "map", "marker labels stay crisp when the map is zoomed",
              f"edge energy {edges:.1f} over {w}x{h}")
    except Exception as e:
        check(False, "map", "marker labels stay crisp when the map is zoomed", str(e)[:60])

    before = tf()
    box = pg.evaluate("()=>{const r=document.querySelector('.kmap-stage').getBoundingClientRect();"
                      "return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)};}")
    pg.mouse.move(box["x"], box["y"])
    pg.mouse.down()
    for i in range(1, 7):
        pg.mouse.move(box["x"] - 18 * i, box["y"] - 11 * i)
    pg.mouse.up()
    pg.wait_for_timeout(400)
    check(tf() != before, "map", "dragging pans the map when it is zoomed in")

    pg.evaluate("document.querySelector('[data-z=\"reset\"]').click()")
    pg.wait_for_timeout(500)
    check(abs(scale() - 1) < 0.01, "map", "reset returns the map to its full view", scale())

    # a pan must not register as choosing whichever marker it ended on
    pg.evaluate("document.querySelector('[data-z=\"in\"]').click()")
    pg.wait_for_timeout(400)
    chosen = pg.evaluate("[...document.querySelectorAll('.kmap-row')]"
                         ".findIndex(r=>r.classList.contains('is-on'))")
    pin = pg.evaluate("()=>{const r=document.querySelectorAll('.kmap-pin')[0]"
                      ".getBoundingClientRect();"
                      "return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)};}")
    pg.mouse.move(pin["x"] + 90, pin["y"] + 60)
    pg.mouse.down()
    for i in range(1, 7):
        pg.mouse.move(pin["x"] + 90 - 15 * i, pin["y"] + 60 - 10 * i)
    pg.mouse.up()
    pg.wait_for_timeout(400)
    check(pg.evaluate("[...document.querySelectorAll('.kmap-row')]"
                      ".findIndex(r=>r.classList.contains('is-on'))") == chosen,
          "map", "a pan that ends on a marker does not select it")
    pg.evaluate("document.querySelector('[data-z=\"reset\"]').click()")
    pg.wait_for_timeout(300)


def kenya_pinch(browser, base):
    """Two fingers on the map.

    This is why the chart is now offered on a phone at all. Its smallest type
    lands under 3px at 390px wide, so it was withheld; pinch turns it into a
    detail view you open rather than one you squint at.

    Synthetic mouse events cannot reproduce this. It needs real touch points
    through CDP, and it has to run in a touch context."""
    ctx = browser.new_context(viewport={"width": 390, "height": 844},
                              has_touch=True, is_mobile=True)
    pg = ctx.new_page()
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1500)
    pg.evaluate("document.querySelector('.kmap-stage').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(700)

    check(not pg.evaluate("document.querySelector('.kmap-zoom').hidden"),
          "pinch", "the chart is offered on a phone now that it can be zoomed")
    check(pg.evaluate("document.querySelector('.kmap-stage').style.touchAction") == "pan-y",
          "pinch", "an unzoomed map still lets the page scroll past it")

    cdp = ctx.new_cdp_session(pg)
    r = pg.evaluate("()=>{const b=document.querySelector('.kmap-stage').getBoundingClientRect();"
                    "return {x:b.left,y:b.top,w:b.width,h:b.height};}")
    cx, cy = r["x"] + r["w"] / 2, r["y"] + r["h"] / 2
    scale = lambda: pg.evaluate(
        "()=>{const m=getComputedStyle(document.querySelector('.kmap-view'))"
        ".transform.match(/matrix\\(([\\d.]+)/);return m?+m[1]:1}")

    def touch(kind, pts):
        cdp.send("Input.dispatchTouchEvent", {
            "type": kind,
            "touchPoints": [{"x": x, "y": y, "id": i} for i, (x, y) in enumerate(pts)]})

    touch("touchStart", [(cx - 30, cy), (cx + 30, cy)])
    for d in (50, 80, 120, 160):
        touch("touchMove", [(cx - d, cy), (cx + d, cy)])
        pg.wait_for_timeout(45)
    touch("touchEnd", [])
    pg.wait_for_timeout(400)
    check(scale() > 2, "pinch", "two fingers zoom the map in", scale())
    check(pg.evaluate("document.querySelector('.kmap-stage').style.touchAction") == "none",
          "pinch", "a zoomed map takes the gesture instead of the page")

    peak = scale()
    touch("touchStart", [(cx - 150, cy), (cx + 150, cy)])
    for d in (110, 70, 40, 20):
        touch("touchMove", [(cx - d, cy), (cx + d, cy)])
        pg.wait_for_timeout(45)
    touch("touchEnd", [])
    pg.wait_for_timeout(400)
    # measured against the peak, not against a constant. "< 2" passed against a
    # build where pinch never fired at all, because the scale had never left 1.
    check(scale() < peak - 0.5, "pinch", "two fingers zoom it back out",
          f"{peak:.2f} then {scale():.2f}")
    ctx.close()


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
            for fn in (rail, nav, player, library, search, kenya, kenya_hero, kenya_map, enquire, overflow):
                fn(pg, base)
            pg.close()
            pg2 = browser.new_page(viewport={"width": 1280, "height": 900},
                                   reduced_motion="reduce")
            globe(pg2, base)
            touch_gestures(browser, base)
            kenya_pinch(browser, base)
            errors(pg2, base)
            pg2.close()
            browser.close()
    finally:
        httpd.shutdown()

    print("\n%d interaction checks | %d FAIL" % (len(CHECKS), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
