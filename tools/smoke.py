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
    """The FAQ still uses accordions; packing and etiquette no longer do."""
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1500)
    n = pg.evaluate("document.querySelectorAll('details').length")
    check(n >= 6, "kenya", "the FAQ accordions are present", n)

    kit = pg.evaluate("document.querySelectorAll('.kkit-item').length")
    check(kit >= 30, "kenya", "the packing kit is present", kit)
    if kit:
        # The groups load collapsed (since 16 Sep), so the first item cannot
        # be clicked until its group is opened, the way a reader would.
        pg.click(".kkit-ghead")
        pg.wait_for_timeout(500)
        opened = pg.evaluate("document.querySelector('.kkit-ghead').getAttribute('aria-expanded')")
        check(opened == "true", "kenya", "clicking a kit group header opens it", opened)
        pg.click(".kkit-item")
        pg.wait_for_timeout(250)
        done = pg.evaluate("document.getElementById('kkitDone').textContent")
        pressed = pg.evaluate("document.querySelector('.kkit-item').getAttribute('aria-pressed')")
        check(done == "1" and pressed == "true", "kenya",
              "ticking an item counts it", "%s packed" % done)

    rules = pg.evaluate("document.querySelectorAll('.etq-card').length")
    check(rules == 8, "kenya", "the eight etiquette rules are present", rules)

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
    pg.click(".kmap-swap")
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

    # ---- registration ----------------------------------------------------
    # The check that would have caught all of it. Markers are positioned by
    # arithmetic in kenya-map.js; this asks the browser where the same point in
    # the SVG actually lands, via getScreenCTM, and compares. Independent of the
    # code under test, which is the whole point.
    #
    # Three bugs hid from every other check here. Markers that never moved at
    # all, because place() was not being called on zoom. A constant offset from
    # measuring the border box while the map spans the padding box. And the
    # assumption that an SVG fills its box, when preserveAspectRatio centres the
    # slack instead. All three looked perfectly fine at 1x.
    reg = """(steps)=>{
      for(let i=0;i<steps;i++) document.querySelector('[data-z="in"]').click();
      return new Promise(r=>setTimeout(()=>{
        const svg=document.querySelector('.kmap-plate svg'), ctm=svg.getScreenCTM();
        const vb=svg.viewBox.baseVal;
        const errs=[...document.querySelectorAll('.kmap-pin')].map(p=>{
          const d=JSON.parse(p.getAttribute('data-plate'));
          const pt=svg.createSVGPoint();
          pt.x=d.x/100*vb.width; pt.y=d.y/100*vb.height;
          const t=pt.matrixTransform(ctm), b=p.getBoundingClientRect();
          return Math.hypot(b.left+b.width/2-t.x, b.top+b.height/2-t.y);
        });
        r({k:+getComputedStyle(document.querySelector('.kmap-view'))
             .transform.match(/matrix\\(([\\d.]+)/)[1], worst:Math.max(...errs)});
      },1400));
    }"""
    for steps in (0, 2, 4):
        pg.goto(base + "/destinations/kenya.html", wait_until="load")
        pg.wait_for_timeout(1300)
        # Instant, because scroll-behavior is smooth site-wide.
        pg.evaluate("""()=>{const r=document.querySelector('.kmap').getBoundingClientRect();
          window.scrollTo({top:Math.round(r.top+scrollY),behavior:'instant'});}""")
        try:
            pg.wait_for_function(
                "()=>[...document.images].filter(i=>i.getBoundingClientRect().top<innerHeight*3)"
                ".every(i=>i.complete)", timeout=12000)
        except Exception:
            pass
        pg.wait_for_timeout(900)
        # Poll until the reading stops moving instead of guessing a delay. At
        # 1.5s this measured 225px, 51px and 620px on three consecutive runs and
        # 0.05px on all three at 4s: it is settling, not drifting, and a fixed
        # wait only decides how often the check lies.
        d = pg.evaluate(reg, steps)
        for _ in range(12):
            pg.wait_for_timeout(400)
            again = pg.evaluate(reg, 0)
            if abs(again["worst"] - d["worst"]) < 0.2:
                break
            d = again
        check(d["worst"] < 3, "map",
              "markers sit on the map at %.1fx zoom" % d["k"],
              "worst %.2f px" % d["worst"])

    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1300)
    pg.evaluate("document.querySelector('.kmap').scrollIntoView({block:'start'})")
    pg.wait_for_timeout(600)
    # the registration block reloaded the page, and a drag only pans a zoomed map
    pg.evaluate("document.querySelector('[data-z=\"in\"]').click()")
    pg.wait_for_timeout(600)

    tf = lambda: pg.evaluate("getComputedStyle(document.querySelector('.kmap-view')).transform")
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

    # The reset button became the chart toggle, so the ways back to the full
    # view are a double click and escape. Double click is used here because
    # escape needs focus inside the map and a drag does not give it that,
    # which is worth knowing: the keyboard route is not reachable by mouse
    # alone. Losing the labelled button is the cost of putting the two related
    # actions in one place.
    pg.mouse.dblclick(box["x"], box["y"])
    pg.wait_for_timeout(700)
    check(abs(scale() - 1) < 0.01, "map",
          "a double click returns the map to its full view", scale())

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
    pg.mouse.dblclick(box["x"], box["y"])
    pg.wait_for_timeout(300)


def kenya_facts(pg, base):
    """The practical facts read at a glance instead of behind six clicks.

    An accordion is for content long enough to be worth collapsing. Every
    answer here was one line, so six of them cost six clicks to learn that the
    capital is Nairobi."""
    pg.set_viewport_size({"width": 1400, "height": 900})
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1300)
    n = pg.evaluate("document.querySelectorAll('#practical .fact').length")
    check(n == 6, "facts", "every fact has its own cell", n)
    check(pg.evaluate("document.querySelectorAll('#practical details').length") == 0,
          "facts", "nothing is hidden behind a click any more")
    check(pg.evaluate("document.querySelectorAll('#practical .fact-i').length") == 6,
          "facts", "every fact carries an icon")
    # the icons inherit colour, so a hardcoded fill would break the palette
    check(pg.evaluate("[...document.querySelectorAll('#practical .fact-i')]"
                      ".every(i=>i.getAttribute('stroke')==='currentColor')"),
          "facts", "icons take their colour from the stylesheet, not the markup")
    # and the stylesheet gives them a palette token, not a one-off hex
    icol = pg.evaluate("getComputedStyle(document.querySelector('#practical .fact-i')).color")
    ocol = pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--orange').trim()")
    want = "rgb(255, 117, 23)"
    check(icol == want, "facts", "the icons use the site orange", f"{icol} against {ocol}")
    # three across means six facts fill two rows with no orphan
    cols = pg.evaluate("getComputedStyle(document.querySelector('.fact-grid'))"
                       ".gridTemplateColumns.split(' ').length")
    check(cols == 3, "facts", "three across, so the six make two full rows", cols)
    # the values have to be readable, not decorative
    vis = pg.evaluate("""()=>[...document.querySelectorAll('#practical .fact-v')]
      .every(e=>e.textContent.trim().length>2 && +getComputedStyle(e).opacity===1)""")
    check(vis, "facts", "every value is present and visible")
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.wait_for_timeout(600)
    one = pg.evaluate("getComputedStyle(document.querySelector('.fact-grid'))"
                      ".gridTemplateColumns.split(' ').length")
    check(one == 1, "facts", "one column on a phone", one)
    pg.set_viewport_size({"width": 1400, "height": 900})


def kenya_overview(pg, base):
    """The Overview: a pinned sequence, two instruments, and a sign-off that
    lights word by word.

    The stage is position:sticky inside a wrapper three screens tall, so it
    has to sit at exactly 0 through every beat and release afterwards. An
    ancestor with overflow:hidden would break that silently (overflow:clip on
    .page-wrap does not), which is why the pin is measured rather than assumed.
    Scrolling is behavior:'instant' because scroll-behavior is smooth site-wide."""
    pg.set_viewport_size({"width": 1440, "height": 900})
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_function("()=>document.fonts.status==='loaded'")
    top = lambda s: pg.evaluate("s=>document.querySelector(s).getBoundingClientRect().top+scrollY", s)
    go = lambda y: (pg.evaluate("y=>window.scrollTo({top:y,behavior:'instant'})", y),
                    pg.wait_for_function("y=>Math.abs(window.scrollY-y)<2", arg=y))

    fly = round(top('#kfly'))
    pins, tracks = [], []
    for k in range(3):
        go(fly + k * 900)
        pg.wait_for_timeout(500)
        st = pg.evaluate("""()=>{const s=document.querySelector('.kfly-stage').getBoundingClientRect();
          const on=[...document.querySelectorAll('.kfly-slide')].findIndex(e=>e.classList.contains('is-on'));
          const so=[...document.querySelectorAll('.kfly-step')].findIndex(e=>e.classList.contains('is-on'));
          return {top:Math.round(s.top),slide:on,step:so};}""")
        pins.append(st["top"]); tracks.append((st["slide"], st["step"], k))
    check(all(p == 0 for p in pins), "overview", "the stage pins at the top through all three beats", pins)
    check(all(a == b == c for a, b, c in tracks), "overview",
          "the photograph, the words and the scroll position agree on which beat this is", tracks)
    go(fly + 3 * 900 + 300); pg.wait_for_timeout(200)
    after = pg.evaluate("()=>Math.round(document.querySelector('.kfly-stage').getBoundingClientRect().top)")
    check(after < -200, "overview", "and releases once the sequence is over", after)
    # every beat's words are the owner's and every photograph has a real alt
    check(pg.evaluate("[...document.querySelectorAll('.kfly-slide img')].every(i=>i.alt.length>10)"),
          "overview", "every slide has an alt text")

    # the instruments: the vario has to sweep off zero when it comes into view
    go(round(top('.kair')) - 120); pg.wait_for_timeout(2400)
    read = pg.evaluate("parseFloat(document.querySelector('.kvario .read').textContent)")
    check(4.0 < read < 6.0, "overview", "the vario reads in the midday band once in view", read)
    check(pg.evaluate("document.querySelector('.kseason').classList.contains('is-on')"),
          "overview", "the season ring lights when it comes into view")
    lit = pg.evaluate("[...document.querySelectorAll('.kseason .seg.on')].length")
    check(lit == 4, "overview", "four months are lit, December to March", lit)

    # the sign-off: only the five words carry the reveal, and it runs left to right
    words = pg.evaluate("[...document.querySelectorAll('.kov-w')].map(w=>w.textContent.trim()).join(' ')")
    check(words == "Touch The Sky With Glory", "overview", "only Touch The Sky With Glory lights", words)
    gy = round(top('#kovGlory'))
    go(gy - int(0.62 * 900)); pg.wait_for_timeout(300)
    t = pg.evaluate("[...document.querySelectorAll('.kov-w')].map(w=>parseFloat(getComputedStyle(w).getPropertyValue('--t')||1))")
    check(t[0] > t[-1] + 0.2, "overview", "mid-scroll the first word is further lit than the last", t)
    go(gy - int(0.35 * 900)); pg.wait_for_timeout(300)
    t = pg.evaluate("[...document.querySelectorAll('.kov-w')].map(w=>parseFloat(getComputedStyle(w).getPropertyValue('--t')||1))")
    check(min(t) > 0.95, "overview", "and the whole phrase is orange by the time it reaches the middle", t)

    # no rule and no frame around the map: two-class selectors, verified not assumed
    edges = pg.evaluate("""()=>({route:getComputedStyle(document.querySelector('#route')).borderTopWidth,
      stage:getComputedStyle(document.querySelector('.kmap-stage')).borderTopWidth})""")
    check(all(v == "0px" for v in edges.values()), "overview", "no rule above the route and no frame around the map", str(edges))

    pg.set_viewport_size({"width": 390, "height": 844})
    pg.wait_for_timeout(500)
    fly = round(top('#kfly')); go(fly + 844); pg.wait_for_timeout(500)
    mob = pg.evaluate("()=>Math.round(document.querySelector('.kfly-stage').getBoundingClientRect().top)")
    check(mob == 0, "overview", "the stage pins on a phone too", mob)
    pg.set_viewport_size({"width": 1400, "height": 900})


def kenya_dates(pg, base):
    """Season packages and Before You Book.

    The band places the two tours by percentage of a 121 day window from
    1 December, so the bars must land where the arithmetic says and not
    merely somewhere orange. 18 Jan is day 48 of that window and 1 Feb is
    day 62, both twelve days long. The day timeline and the bars animate on
    an observer, so this also proves they are not left in their zero state."""
    pg.set_viewport_size({"width": 1440, "height": 900})
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_function("()=>document.fonts.status==='loaded'")
    top = lambda s: pg.evaluate("s=>document.querySelector(s).getBoundingClientRect().top+scrollY", s)
    go = lambda y: (pg.evaluate("y=>window.scrollTo({top:y,behavior:'instant'})", y),
                    pg.wait_for_function("y=>Math.abs(window.scrollY-y)<2", arg=y))

    go(round(top('#dates')) - 90)
    pg.wait_for_timeout(1800)
    check(pg.evaluate("document.querySelector('.kdates').classList.contains('is-on')"),
          "dates", "the season band lights when it scrolls in")
    bars = pg.evaluate("""()=>[...document.querySelectorAll('.kdates-tour')].map(e=>{
      const r=e.getBoundingClientRect(), k=e.parentElement.getBoundingClientRect();
      return [Math.round((r.left-k.left)/k.width*1000)/10, Math.round(r.width/k.width*1000)/10];})""")
    want = [(39.7, 9.9), (51.2, 9.9)]
    ok = len(bars) == 2 and all(abs(a - w[0]) < 1 and abs(b - w[1]) < 1 for (a, b), w in zip(bars, want))
    check(ok, "dates", "both tours sit where the calendar puts them, twelve days wide", bars)
    for txt in ("18 to 29 January", "1 to 12 February"):
        check(pg.evaluate("t=>document.querySelector('#dates').textContent.includes(t)", txt),
              "dates", "the dates block says " + txt)
    check(pg.evaluate("document.querySelectorAll('#dates .btn-solid.is-outline').length") == 2,
          "dates", "each departure has its own outlined Book a Call")
    rest = pg.evaluate("getComputedStyle(document.querySelector('#dates .btn-solid.is-outline')).backgroundColor")
    check("rgba(0, 0, 0, 0)" == rest, "dates", "and it is unfilled until hovered", rest)

    go(round(top('#kday')) - 90)
    pg.wait_for_timeout(2200)
    day = pg.evaluate("""()=>{const l=document.querySelector('.kday-line').getBoundingClientRect();
      const t=document.querySelector('.kday-track').getBoundingClientRect();
      return {on:document.getElementById('kday').classList.contains('is-on'),
              frac:Math.round(l.width/t.width*100), stops:document.querySelectorAll('.kday-stop').length};}""")
    check(day["on"] and day["frac"] > 95, "dates", "the day timeline draws itself in", day)
    check(day["stops"] == 5, "dates", "briefing, launch, fly, land, retrieve", day["stops"])
    fit = pg.evaluate("""()=>({yes:document.querySelectorAll('.kfit-yes li').length,
      no:document.querySelectorAll('.kfit-no li').length})""")
    check(fit["yes"] >= 3 and fit["no"] >= 3, "dates", "the verdict argues both sides", fit)

    # the timeline turns and runs down the left on a phone
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.wait_for_timeout(400)
    go(round(top('#kday')) - 60)
    pg.wait_for_timeout(2200)
    vert = pg.evaluate("""()=>{const l=document.querySelector('.kday-line').getBoundingClientRect();
      return Math.round(l.height) > Math.round(l.width);}""")
    check(vert, "dates", "and stands up on a phone")
    pg.set_viewport_size({"width": 1400, "height": 900})


def kenya_rolls(pg, base):
    """Wheel rolls on the map earn their way forward: two lift it above the
    weather drifting down from the gallery, four open the chart.

    A burst of trackpad events inside 150ms counts as one roll, or a single
    flick would skip both stages at once, so the check waits between rolls.

    The page is scrolled with behavior:'instant'. scroll-behavior is smooth
    site-wide and a rect read mid-animation puts the pointer off screen, where
    the wheel lands on nothing."""
    pg.set_viewport_size({"width": 1400, "height": 900})
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1500)
    pg.evaluate("window.scrollTo(0,document.body.scrollHeight)")
    pg.wait_for_timeout(1800)
    pg.evaluate("""()=>{const r=document.querySelector('.kmap-stage').getBoundingClientRect();
      window.scrollTo({top:Math.round(r.top+scrollY-(innerHeight-r.height)/2),
                       behavior:'instant'});}""")
    pg.wait_for_timeout(1100)
    mid = pg.evaluate("""()=>{const b=document.querySelector('.kmap-stage').getBoundingClientRect();
      return {x:Math.round(b.left+b.width/2),y:Math.round(b.top+b.height/2)};}""")
    check(pg.evaluate(f"()=>{{const e=document.elementFromPoint({mid['x']},{mid['y']});"
                      "return e ? !!e.closest('.kmap-stage') : false;}"),
          "rolls", "the wheel lands on the map")
    pg.mouse.move(mid["x"], mid["y"])

    lifted = lambda: pg.evaluate("document.querySelector('.kmap').classList.contains('is-lifted')")
    sheet = lambda: pg.evaluate("document.querySelector('.kmap-stage').classList.contains('is-sheet')")

    check(not lifted() and not sheet(), "rolls", "the map starts flat and in the overview")

    # One control, not two. Opening the chart used to be a separate button
    # below the map while the view controls sat inside it, which put two
    # related actions in two unrelated places.
    ctl = pg.evaluate("""()=>({old:!!document.querySelector('.kmap-zoom'),
      buttons:[...document.querySelectorAll('.kmap-ctl button')].map(b=>b.textContent.trim()),
      label:document.querySelector('.kmap-swap').textContent.trim()});""")
    check(not ctl["old"], "rolls", "the separate chart button is gone")
    check(len(ctl["buttons"]) == 3 and ctl["label"] == "Open the chart", "rolls",
          "the chart opens from the map's own controls", str(ctl["buttons"]))
    pg.mouse.wheel(0, -300); pg.wait_for_timeout(420)
    check(not lifted(), "rolls", "one roll only zooms")
    pg.mouse.wheel(0, -300); pg.wait_for_timeout(420)
    check(lifted(), "rolls", "two rolls lift the map above the weather")
    check(not sheet(), "rolls", "two rolls do not open the chart")
    pg.mouse.wheel(0, -300); pg.wait_for_timeout(420)
    check(not sheet(), "rolls", "three rolls still do not open the chart")
    pg.mouse.wheel(0, -300); pg.wait_for_timeout(1400)
    check(sheet(), "rolls", "four rolls open the chart")
    pg.mouse.wheel(0, -300); pg.wait_for_timeout(500)
    check(lifted(), "rolls", "the chart stays above the weather once open")

    pg.evaluate("document.querySelector('.kmap-swap').click()")
    pg.wait_for_timeout(1300)
    check(not sheet() and not lifted(), "rolls",
          "going back to the overview clears both")

    # Weather fills the empty part of the stage and never the map itself. It
    # sits UNDER the map layers. The chart paints an opaque ground across its
    # whole viewBox, so nothing may change inside that rectangle. The plate no
    # longer has a ground (its clouds pass behind the country now, since a
    # frameless map with a hidden rectangle read as a glitch), so for the plate
    # "the map itself" is the country's flat top face, TOP in the generator.
    # If a cloud is ever painted over it, this goes red.
    import tempfile as _t
    from PIL import Image as _I
    for state in ("overview", "chart"):
        if state == "chart":
            pg.evaluate("document.querySelector('.kmap-swap').click()")
            pg.wait_for_timeout(2000)
        box = pg.evaluate("""()=>{const st=document.querySelector('.kmap-stage').getBoundingClientRect();
          const on=document.querySelector('.kmap-stage').classList.contains('is-sheet');
          const svg=document.querySelector(on?'.kmap-sheet svg':'.kmap-plate svg');
          if(!svg) return null;
          const v=svg.getBoundingClientRect(), vb=svg.viewBox.baseVal;
          const sc=Math.min(v.width/vb.width, v.height/vb.height);
          const w=vb.width*sc, h=vb.height*sc;
          return [Math.round(v.left+(v.width-w)/2-st.left),
                  Math.round(v.top+(v.height-h)/2-st.top),
                  Math.round(w), Math.round(h)];}""")
        on = os.path.join(_t.gettempdir(), f"kw-on-{state}.png")
        off = os.path.join(_t.gettempdir(), f"kw-off-{state}.png")
        try:
            pg.locator(".kmap-stage").screenshot(path=on)
            pg.evaluate("document.querySelector('.kmap-weather').style.visibility='hidden'")
            pg.wait_for_timeout(400)
            pg.locator(".kmap-stage").screenshot(path=off)
            pg.evaluate("document.querySelector('.kmap-weather').style.visibility=''")
            A, B = _I.open(on).convert("L"), _I.open(off).convert("L")
            pa, pb, wd = list(A.getdata()), list(B.getdata()), A.size[0]
            x, y, mw, mh = box
            onmap = onmapt = grey = greyt = 0
            if state == "overview":
                # TOP = "#272a33" in tools/build_kenya_plate.py, as luminance
                face = round(0.299 * 0x27 + 0.587 * 0x2a + 0.114 * 0x33)
            for row in range(A.size[1]):
                for colx in range(wd):
                    i = row * wd + colx
                    inside = (x <= colx < x + mw) and (y <= row < y + mh)
                    if state == "overview":
                        inside = inside and abs(pb[i] - face) <= 2
                    hit = abs(pa[i] - pb[i]) > 4
                    if inside:
                        onmapt += 1
                        onmap += hit
                    else:
                        greyt += 1
                        grey += hit
            onpct = onmap / max(1, onmapt) * 100
            gpct = grey / max(1, greyt) * 100
            check(onpct < 1.5, "rolls",
                  f"no weather over the {state} map itself", f"{onpct:.1f}% of it")
            check(gpct > 4, "rolls",
                  f"weather fills the empty stage around the {state} map", f"{gpct:.1f}%")
        except Exception as e:
            check(False, "rolls", f"weather sits around the {state} map, not on it", str(e)[:50])


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
    # The gallery now sits above the map with eleven lazy images in it. They
    # load after the scroll, reflow the page, and move the map out from under
    # the touch points, so the gesture lands on nothing and the scale never
    # changes. Settle first, then take the coordinates.
    try:
        pg.wait_for_function(
            "()=>[...document.images].filter(i=>i.loading!=='lazy'||i.getBoundingClientRect().top<innerHeight*2)"
            ".every(i=>i.complete)", timeout=12000)
    except Exception:
        pass
    pg.evaluate("document.querySelector('.kmap-stage').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(900)

    check(not pg.evaluate("document.querySelector('.kmap-swap').hidden"),
          "pinch", "the chart is offered on a phone now that it can be zoomed")
    check(pg.evaluate("document.querySelector('.kmap-stage').style.touchAction") == "pan-y",
          "pinch", "an unzoomed map still lets the page scroll past it")

    cdp = ctx.new_cdp_session(pg)
    r = pg.evaluate("()=>{const b=document.querySelector('.kmap-stage').getBoundingClientRect();"
                    "return {x:b.left,y:b.top,w:b.width,h:b.height};}")
    cx, cy = r["x"] + r["w"] / 2, r["y"] + r["h"] / 2
    # assert the gesture will actually land on the map, rather than discovering
    # afterwards that the scale did not change and guessing why
    on = pg.evaluate(f"()=>{{const e=document.elementFromPoint({cx:.0f},{cy:.0f});"
                     "return e ? !!e.closest('.kmap-stage') : false;}")
    check(on, "pinch", "the gesture lands on the map", f"centre at {cx:.0f},{cy:.0f}")
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

    # The two stages have to be reachable on a phone as well. They were not:
    # they counted wheel events, and a phone has no wheel, so a touch user
    # could never lift the map or reach the chart however hard they pinched.
    check(pg.evaluate("document.querySelector('.kmap').classList.contains('is-lifted')"),
          "pinch", "a pinch lifts the map above the weather")
    for d in (60, 110, 170, 230, 300):
        touch("touchStart", [(cx - 30, cy), (cx + 30, cy)]) if d == 60 else None
        touch("touchMove", [(cx - d, cy), (cx + d, cy)])
        pg.wait_for_timeout(60)
    touch("touchEnd", [])
    pg.wait_for_timeout(1600)
    check(pg.evaluate("document.querySelector('.kmap-stage').classList.contains('is-sheet')"),
          "pinch", "pinching further opens the chart on a phone")

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


def kenya_gallery(pg, base):
    """The photograph carousel.

    Three of these guard specific things that were reported broken and looked
    fine in a screenshot: the indicator sitting on top of the front card, a
    lightbox translucent enough to show the carousel behind the photograph, and
    clouds too faint to notice.

    The clouds one measures pixels. Opacity and load state were both correct
    while the layer contributed almost nothing to the image, so the only honest
    test is to render with and without and difference the two."""
    pg.set_viewport_size({"width": 1400, "height": 900})
    pg.goto(base + "/destinations/kenya.html", wait_until="load")
    pg.wait_for_timeout(1800)
    pg.evaluate("document.querySelector('.cfl').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(1600)

    n = pg.evaluate("document.querySelectorAll('.cfl-card').length")
    check(n == 11, "gallery", "every photograph is a card", n)
    check(pg.evaluate("[...document.querySelectorAll('.cfl-card')]"
                      ".every(c=>c.querySelector('img').complete && c.querySelector('img').naturalWidth>0)"),
          "gallery", "every photograph actually loads")

    # crops are centred on the canopy, not on the middle of the frame
    off = pg.evaluate("[...document.querySelectorAll('.cfl-card img')]"
                      ".filter(i=>getComputedStyle(i).objectPosition!=='50% 50%').length")
    check(off >= 9, "gallery", "crops are centred on the wing, not the frame", off)

    # the indicator must sit clear of the cards
    gap = pg.evaluate("()=>{const f=document.querySelector('.cfl-frame').getBoundingClientRect();"
                      "const d=document.querySelector('.cfl-dots').getBoundingClientRect();"
                      "return Math.round(d.top-f.bottom);}")
    check(gap > 0, "gallery", "the indicator sits below the frame, not over the photograph",
          f"{gap}px clear")

    # it is a ring: stepping past the last card returns to the first
    first = pg.evaluate("[...document.querySelectorAll('.cfl-dot')].findIndex(d=>d.classList.contains('is-on'))")
    for _ in range(n):
        pg.evaluate("document.querySelector('.cfl-next').click()")
        pg.wait_for_timeout(90)
    pg.wait_for_timeout(900)
    check(pg.evaluate("[...document.querySelectorAll('.cfl-dot')]"
                      ".findIndex(d=>d.classList.contains('is-on'))") == first,
          "gallery", "the carousel loops instead of stopping at the end")
    check(pg.evaluate("[...document.querySelectorAll('.cfl-card')]"
                      ".filter(c=>+getComputedStyle(c).opacity>0.05).length") >= 7,
          "gallery", "cards flank both sides at every position")

    # full size shows one photograph and nothing behind it
    pg.evaluate("document.querySelectorAll('.cfl-card')[0].click()")
    pg.wait_for_timeout(800)
    check(not pg.evaluate("document.querySelector('.cfl-lb').hidden"),
          "gallery", "the front card opens full size")
    check(pg.evaluate("document.querySelectorAll('.cfl-full.is-on').length") == 1,
          "gallery", "exactly one photograph shows at full size")
    bg = pg.evaluate("getComputedStyle(document.querySelector('.cfl-lb')).backgroundColor")
    check("rgba" not in bg, "gallery",
          "the full size view is opaque, so nothing ghosts through behind it", bg)
    pg.evaluate("document.querySelector('.cfl-lb-next').click()")
    pg.wait_for_timeout(600)
    check(pg.evaluate("document.querySelectorAll('.cfl-full.is-on').length") == 1,
          "gallery", "stepping on keeps it to one photograph")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(500)
    check(pg.evaluate("document.querySelector('.cfl-lb').hidden"),
          "gallery", "escape closes the full size view")
    check(pg.evaluate("document.body.style.overflow") == "",
          "gallery", "closing gives the page its scroll back")

    # clouds have to be visible, not merely present
    import tempfile
    from PIL import Image
    # The cloud images are lazy, and an earlier check scrolls away from here, so
    # they have to be brought back into view before they will load at all.
    # Without this the measurement read 6.5% where the settled value is 56.5%,
    # and I spent a while "fixing" a feature that was never broken.
    pg.evaluate("document.querySelector('.cfl').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(600)
    try:
        pg.wait_for_function(
            "()=>[...document.querySelectorAll('.cfl-cloud')]"
            ".every(c=>c.complete && c.naturalWidth>0)", timeout=12000)
    except Exception:
        pass
    pg.wait_for_timeout(900)
    a = os.path.join(tempfile.gettempdir(), "cl-on.png")
    c = os.path.join(tempfile.gettempdir(), "cl-off.png")
    try:
        # Shoot the whole section, not the frame. Inside the frame the blurred
        # backdrop paints over the clouds once it fades in, so the same page
        # measured 68% before it settled and 6.5% after, which is what sent me
        # chasing a fault that did not exist. Around the frame, which is where
        # the clouds are meant to read, it is a stable 11%.
        pg.locator(".cfl").screenshot(path=a)
        pg.evaluate("document.querySelectorAll('.cfl-atmos').forEach(e=>e.style.visibility='hidden')")
        pg.wait_for_timeout(400)
        pg.locator(".cfl").screenshot(path=c)
        pg.evaluate("document.querySelectorAll('.cfl-atmos').forEach(e=>e.style.visibility='')")
        A = Image.open(a).convert("L"); C = Image.open(c).convert("L")
        pa, pc = list(A.getdata()), list(C.getdata())
        diff = [abs(x - y) for x, y in zip(pa, pc)]
        share = sum(1 for d in diff if d > 4) / max(1, len(diff)) * 100
        check(share > 6, "gallery", "the clouds are actually visible, not just present",
              f"{share:.1f}% of pixels moved")
    except Exception as e:
        check(False, "gallery", "the clouds are actually visible, not just present", str(e)[:50])

    # Clouds drift as the page scrolls, and by enough to notice. The site sets
    # scroll-behavior: smooth, so window.scrollTo animates and a measurement
    # taken 400ms later lands somewhere in the middle of the journey: readings
    # that looked like the parallax clamping were the scroll still moving.
    # behavior:'instant' or this measures nothing real.
    gy = pg.evaluate("Math.round(document.querySelector('.cfl').getBoundingClientRect().top+scrollY)")
    seen = []
    for off in (-900, -300, 300, 900, 1500):
        pg.evaluate(f"window.scrollTo({{top:{gy + off},behavior:'instant'}})")
        pg.wait_for_timeout(380)
        seen.append(pg.evaluate(
            "()=>Math.round(new DOMMatrix(getComputedStyle("
            "document.querySelectorAll('.cfl-cloud')[2]).transform).f)"))
    travel = max(seen) - min(seen)
    check(travel > 250, "gallery",
          "the clouds move vertically as the page scrolls", f"{travel}px of travel")

    # The gallery has to dissolve into the page rather than arrive as a box, and
    # the weather has to carry past it into the sections either side. Both were
    # asked for and both are invisible to any check that only looks inside the
    # component, so measure the geometry against the section itself.
    pg.evaluate("document.querySelector('.cfl').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(900)
    edge = pg.evaluate("""()=>{const f=document.querySelector('.cfl-frame');
      const cs=getComputedStyle(f);
      return {border:parseFloat(cs.borderTopWidth),
              bg:cs.backgroundColor,
              masked:(cs.maskImage||cs.webkitMaskImage||'none')!=='none'};}""")
    check(edge["masked"], "gallery", "the gallery fades into the page instead of ending at an edge")
    check(edge["border"] == 0 and "rgba(0, 0, 0, 0)" in edge["bg"], "gallery",
          "the gallery frame has no border or fill of its own",
          f"border {edge['border']}px, bg {edge['bg']}")

    over = pg.evaluate("""()=>{const sec=document.querySelector('.cfl').getBoundingClientRect();
      const cs=[...document.querySelectorAll('.cfl-cloud')].map(c=>c.getBoundingClientRect());
      return {above:Math.round(sec.top-Math.min(...cs.map(r=>r.top))),
              below:Math.round(Math.max(...cs.map(r=>r.bottom))-sec.bottom)};}""")
    check(over["above"] > 100 and over["below"] > 100, "gallery",
          "the clouds carry beyond the gallery into the sections either side",
          f"{over['above']}px above, {over['below']}px below")

    # No rules anywhere near the gallery. .dst-sec + .dst-sec draws one between
    # every pair of sections, and beating it needs two classes, not one: the
    # first attempt at removing it used .cfl and silently lost the cascade.
    rules = pg.evaluate("""()=>{const g=document.querySelector('.cfl');
      const n=g.nextElementSibling;
      return {gallery:getComputedStyle(g).borderTopWidth,
              next:n?getComputedStyle(n).borderTopWidth:'0px'};}""")
    check(all(v == "0px" for v in rules.values()), "gallery",
          "no rule is drawn above the gallery or below it", str(rules))

    # the cloud layer is faded on the horizontal axis too, or it ends in a
    # straight vertical edge down the side of the page
    mask = pg.evaluate("()=>{const cs=getComputedStyle(document.querySelector('.cfl-atmos:not(.cfl-atmos-back)'));"
                       "return (cs.maskImage||cs.webkitMaskImage||'');}")
    check(mask.count("gradient") >= 2, "gallery",
          "the clouds fade out sideways as well as vertically",
          f"{mask.count('gradient')} gradients in the mask")

    # A mask only fades what reaches it. img{max-width:100%} was capping the
    # cloud layers at the width of the section, so a layer set wider than the
    # viewport actually stopped at 92.6% and left a hard vertical edge just
    # inside where the fade begins. The mask looked right and the edge was
    # still there, so check the geometry, not the declaration.
    reach = pg.evaluate("""()=>{const c=document.querySelector('.cfl-atmos:not(.cfl-atmos-back) .cfl-cloud').getBoundingClientRect();
      return {left:Math.round(-c.left), right:Math.round(c.right-innerWidth)};}""")
    check(reach["left"] > 60 and reach["right"] > 20, "gallery",
          "the cloud layers run past both sides of the screen",
          f"{reach['left']}px past the left, {reach['right']}px past the right")

    # The clouds belong in front of the photographs and behind the words. The
    # frame is its own stacking context, so anything that has to sit above the
    # cards must be a sibling of the frame rather than a child of it: the
    # caption and arrows were moved out for exactly this reason.
    order = pg.evaluate("""()=>{const z=s=>{const e=document.querySelector(s);
      return e?parseInt(getComputedStyle(e).zIndex||0,10):null;};
      return {frame:z('.cfl-frame'),
              clouds:z('.cfl-atmos:not(.cfl-atmos-back)'),
              cloudsBack:z('.cfl-atmos-back'),
              arrows:z('.cfl-arrow')};}""")
    check(order["clouds"] > order["frame"], "gallery",
          "the clouds sit in front of the photographs", str(order))
    check(order["cloudsBack"] < order["frame"], "gallery",
          "the middle of the weather passes behind the gallery", str(order))
    check(order["arrows"] > order["clouds"],
          "gallery", "the arrows stay in front of the clouds", str(order))

    # The caption lives on the card now, not on a floating layer sized
    # independently of it, so it cannot run off the edges of the photograph.
    cap = pg.evaluate("""()=>{const f=document.querySelector('.cfl-card.is-front');
      if(!f) return null;
      const c=f.querySelector('.cfl-card-cap'); if(!c) return null;
      const a=f.getBoundingClientRect(), b=c.getBoundingClientRect();
      return {over:Math.round(Math.max(a.left-b.left, b.right-a.right)),
              text:c.textContent.trim(), shown:getComputedStyle(c).opacity};}""")
    check(cap is not None, "gallery", "the front card carries its own caption")
    if cap:
        check(cap["over"] <= 0, "gallery",
              "the caption cannot overflow the photograph", f"{cap['over']}px over the edge")
        check(cap["shown"] == "1", "gallery", "the caption is visible on the front card")

    # ---- drag ------------------------------------------------------------
    # The stack has to follow the pointer, not wait for release and jump. A
    # check that only compares before and after cannot tell the two apart, so
    # this samples the transform mid-gesture and requires it to change on every
    # step.
    #
    # The page is scrolled with behavior:'instant' first. scroll-behavior is
    # smooth site-wide, and a rect read mid-animation put the press coordinates
    # off screen entirely, where elementFromPoint returns null and nothing fires.
    pg.evaluate("window.scrollTo(0,document.body.scrollHeight)")
    pg.wait_for_timeout(1200)
    pg.evaluate("""()=>{const r=document.querySelector('.cfl-stage').getBoundingClientRect();
      window.scrollTo({top:Math.round(r.top+scrollY-(innerHeight-r.height)/2),behavior:'instant'});}""")
    pg.wait_for_timeout(1000)
    mid = pg.evaluate("""()=>{const b=document.querySelector('.cfl-stage').getBoundingClientRect();
      return {x:Math.round(b.left+b.width/2),y:Math.round(b.top+b.height/2)};}""")
    check(pg.evaluate(f"()=>{{const e=document.elementFromPoint({mid['x']},{mid['y']});"
                      "return e ? !!e.closest('.cfl-stage') : false;}"),
          "gallery", "the drag test presses on the gallery itself")

    before = pg.evaluate("[...document.querySelectorAll('.cfl-card')]"
                         ".findIndex(c=>c.classList.contains('is-front'))")
    pg.mouse.move(mid["x"], mid["y"])
    pg.mouse.down()
    frames = []
    for i in range(1, 7):
        pg.mouse.move(mid["x"] - 45 * i, mid["y"])
        pg.wait_for_timeout(70)
        frames.append(pg.evaluate(
            "getComputedStyle(document.querySelectorAll('.cfl-card')[0]).transform"))
    check(len(set(frames)) == len(frames), "gallery",
          "the tiles follow the pointer while dragging",
          f"{len(set(frames))} distinct positions over 6 steps")
    check(pg.evaluate("document.querySelector('.cfl-stage').classList.contains('is-dragging')"),
          "gallery", "the map knows a drag is in progress")
    pg.mouse.up()
    pg.wait_for_timeout(900)
    after = pg.evaluate("[...document.querySelectorAll('.cfl-card')]"
                        ".findIndex(c=>c.classList.contains('is-front'))")
    check(after != before, "gallery", "releasing lands on a different photograph",
          f"{before} then {after}")
    check(not pg.evaluate("document.querySelector('.cfl-stage').classList.contains('is-dragging')"),
          "gallery", "the drag state clears on release")
    check(pg.evaluate("getComputedStyle(document.querySelector('.cfl-stage')).touchAction") == "pan-y",
          "gallery", "a finger can still scroll the page past the gallery")

    # In front of everything except the photograph you are looking at: a third
    # mask layer opens a hole over the card at the front.
    #
    # Checked narrow as well as wide, because the card is not the same fraction
    # of the frame at both: 38%-62% at 1400, 27%-73% at 390. A hole sized for
    # the desktop card left cloud sitting on both edges of the mobile one and
    # the desktop check saw none of it.
    import tempfile as _t
    from PIL import Image as _I
    for vw in (1400, 390):
        pg.set_viewport_size({"width": vw, "height": 900})
        pg.wait_for_timeout(500)
        # Instant, and settle. scroll-behavior is smooth site-wide, so
        # scrollIntoView animates: the two screenshots below were being taken at
        # different scroll offsets and the difference between them was the page
        # moving, not weather. It read as 12.4% cloud on a card that measures
        # 0.0% when the page is still.
        pg.evaluate("""()=>{const r=document.querySelector('.cfl-wrap').getBoundingClientRect();
          window.scrollTo({top:Math.round(r.top+scrollY-(innerHeight-r.height)/2),
                           behavior:'instant'});}""")
        pg.wait_for_timeout(1300)
        on = f"/tmp/suite-on-{vw}.png"
        off = f"/tmp/suite-off-{vw}.png"
        try:
            # the card at the FRONT, not the first in the document. Earlier
            # tests leave the carousel on a different index, and measuring
            # card[0] meant measuring an off-centre card that never carries
            # cloud, so this passed without testing anything.
            box = pg.evaluate("""()=>{const w=document.querySelector('.cfl-wrap').getBoundingClientRect();
              const f=document.querySelector('.cfl-card.is-front')
                    ||document.querySelectorAll('.cfl-card')[0];
              const c=f.getBoundingClientRect();
              return [Math.round(c.left-w.left),Math.round(c.top-w.top),
                      Math.round(c.width),Math.round(c.height)];}""")
            # Freeze the cursor lean first. It lerps on requestAnimationFrame
            # forever, so it drifts between two captures taken 400ms apart and
            # shifts the whole scene by a fraction of a pixel. The difference
            # then shows the outline of every card, wing and letter, and reads
            # as 17% cloud when the real figure is zero.
            pg.add_style_tag(content=".cfl-tilt{transform:none!important}")
            pg.wait_for_timeout(500)
            pg.locator(".cfl-wrap").screenshot(path=on)
            # Only the FRONT weather is forbidden over the card. The back copy
            # is meant to pass behind the gallery and shows faintly at the
            # card's top and bottom, where the frame's mask fades out. Hiding
            # both copies counted that as a fault.
            pg.evaluate("document.querySelector('.cfl-atmos:not(.cfl-atmos-back)')"
                        ".style.visibility='hidden'")
            pg.wait_for_timeout(350)
            pg.locator(".cfl-wrap").screenshot(path=off)
            pg.evaluate("document.querySelector('.cfl-atmos:not(.cfl-atmos-back)')"
                        ".style.visibility=''")
            A, B = _I.open(on).convert("L"), _I.open(off).convert("L")
            if A.size != B.size:
                raise RuntimeError(f"frames differ in size, {A.size} vs {B.size}")
            pa, pb, wd = list(A.getdata()), list(B.getdata()), A.size[0]
            x, y, cw, ch = box
            hits = tot = 0
            for row in range(max(0, y + 6), min(A.size[1], y + ch - 6)):
                for colx in range(max(0, x + 6), min(wd, x + cw - 6)):
                    i = row * wd + colx
                    tot += 1
                    if abs(pa[i] - pb[i]) > 4:
                        hits += 1
            pct = hits / max(1, tot) * 100
            check(pct < 4, "gallery",
                  f"the card at the front stays clear of cloud at {vw}px",
                  f"{pct:.1f}% of it covered")

            # and the band just above it: the complaint was cloud crowding the
            # top edge, which is outside the card and so invisible to the check
            # above.
            bh = bt = 0
            for row in range(max(0, y - 70), max(0, y)):
                for colx in range(max(0, x), min(wd, x + cw)):
                    i = row * wd + colx
                    bt += 1
                    if abs(pa[i] - pb[i]) > 4:
                        bh += 1
            bpct = bh / max(1, bt) * 100
            check(bpct < 6, "gallery",
                  f"the space just above the front card is clear too at {vw}px",
                  f"{bpct:.1f}% of it covered")
        except Exception as e:
            check(False, "gallery",
                  f"the card at the front stays clear of cloud at {vw}px", str(e)[:60])
    pg.set_viewport_size({"width": 1400, "height": 900})


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


def guarded(fn, *args):
    """Run one check function. A crash is recorded as a FAIL and the run goes on.

    Before this, one exception (the Kenya kit click, from 16 Sep) ended the run
    with a traceback and no FAIL line, so check.sh still said clean while every
    check after it silently did not run."""
    try:
        fn(*args)
    except Exception as e:
        first = (str(e).strip().splitlines() or [""])[0]
        check(False, fn.__name__, "ran to the end without crashing",
              "%s: %s" % (type(e).__name__, first[:120]))


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
            for fn in (rail, nav, player, library, search, kenya, kenya_hero, kenya_map, kenya_gallery, kenya_facts, kenya_overview, kenya_dates, kenya_rolls, enquire, overflow):
                guarded(fn, pg, base)
            pg.close()
            pg2 = browser.new_page(viewport={"width": 1280, "height": 900},
                                   reduced_motion="reduce")
            guarded(globe, pg2, base)
            guarded(touch_gestures, browser, base)
            guarded(kenya_pinch, browser, base)
            guarded(errors, pg2, base)
            pg2.close()
            browser.close()
    finally:
        httpd.shutdown()

    print("\n%d interaction checks | %d FAIL" % (len(CHECKS), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
