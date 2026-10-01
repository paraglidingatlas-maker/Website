#!/usr/bin/env python3
"""Interaction abuse on the LIVE Paragliding Atlas pages (repo root, served locally).

    python3 abuse.py <check> [<check> ...] [--pages templates|all] [--limit N]

checks: nav navland search tagsort enquire newsletter modal race player audio
        carousel faq kit marquee resize history scroll   (or: all)

Read-only on the repo. Every external request is aborted (the environment blocks
them anyway), so nothing is ever posted to a real service. Results are written
to results_<check>.json next to this file.
"""
import argparse
import json
import math
import os
import random
import re
import struct
import sys
import time

sys.path.insert(0, "/home/user/Website/tools/stress")
import lib  # noqa: E402

PORT = 8813
HERE = os.path.dirname(os.path.abspath(__file__))
EXT_RX = re.compile(r"https?://(?!127\.0\.0\.1:%d)" % PORT)
LONGTASK_JS = """
window.__lt = [];
try { new PerformanceObserver(function (l) { l.getEntries().forEach(function (e) { window.__lt.push(Math.round(e.duration)); }); })
      .observe({type: 'longtask', buffered: true}); } catch (e) {}
"""


# --------------------------------------------------------------------------- harness
class Ctx:
    """One browser context + page with error capture and external requests aborted."""

    def __init__(self, b, base, w=1440, h=900, audio=None, reduced=False, touch=False, door=False):
        self.base = base
        kw = dict(viewport={"width": w, "height": h})
        if reduced:
            kw["reduced_motion"] = "reduce"
        if touch:
            kw["has_touch"] = True
        self.ctx = b.new_context(**kw)
        self.audio = audio
        self.ctx.route("**/*", self._route)
        self.ctx.add_init_script(LONGTASK_JS)
        if not door:  # the knowledge base door covers the whole page on a first visit; skip it like a returning reader
            self.ctx.add_init_script("try { sessionStorage.setItem('pga.kb.iris.seen', '1'); } catch (e) {}")
        self.page = self.ctx.new_page()
        self.events = []
        self.launched, self.blocked = [], []
        self.page.on("pageerror", lambda e: self.events.append(
            {"kind": "pageerror", "text": str(e)[:400], "stack": (e.stack or "")[:600], "url": self.page.url}))
        self.page.on("console", self._console)
        self.cdp = self.ctx.new_cdp_session(self.page)
        self.cdp.send("Page.enable")
        self.cdp.send("Performance.enable")
        self.navreq = []
        self.cdp.on("Page.frameRequestedNavigation",
                    lambda p: self.navreq.append({"reason": p.get("reason"), "url": p.get("url", "")}))

    def _route(self, r):
        u = r.request.url
        if u.startswith(self.base):
            return r.continue_()
        if self.audio and ("anchor.fm" in u or "cloudfront.net" in u) and r.request.resource_type == "media":
            return r.fulfill(status=200, body=self.audio, headers={"Content-Type": "audio/wav"})
        return r.abort()

    def _console(self, m):
        if m.type == "info" and "external handler" in m.text:
            self.launched.append(m.text[:80])
        if m.type == "error" and m.text.startswith("Not allowed to launch"):
            self.blocked.append(m.text[:80])
            return
        if m.type not in ("error", "warning"):
            return
        loc = (m.location or {}).get("url", "")
        self.events.append({"kind": "console-" + m.type, "text": m.text[:400], "loc": loc, "url": self.page.url})

    def goto(self, path, wait="load", settle=300):
        self.page.goto(self.base + path, wait_until=wait, timeout=30000)
        if settle:
            self.page.wait_for_timeout(settle)

    def js(self, expr, arg=None):
        return self.page.evaluate(expr, arg) if arg is not None else self.page.evaluate(expr)

    def metrics(self, gc=True):
        if gc:
            try:
                self.cdp.send("HeapProfiler.enable")
                self.cdp.send("HeapProfiler.collectGarbage")
            except Exception:
                pass
        m = {x["name"]: x["value"] for x in self.cdp.send("Performance.getMetrics")["metrics"]}
        return {k: m.get(k) for k in ("JSHeapUsedSize", "Nodes", "JSEventListeners", "LayoutCount",
                                       "RecalcStyleCount", "TaskDuration", "ScriptDuration", "LayoutDuration")}

    def errors(self, mark=0):
        """Split captured events into the site's own and the environment's."""
        own, env = [], []
        for e in self.events[mark:]:
            t = e["text"]
            if e["kind"] == "pageerror":
                (own if self.base in e.get("stack", "") or not EXT_RX.search(e.get("stack", "")) else env).append(e)
                continue
            if e["kind"] == "console-warning":
                continue
            if t.startswith("Failed to load resource"):
                (own if e.get("loc", "").startswith(self.base) else env).append(e)
            elif EXT_RX.search(t) or not e.get("loc", "").startswith(self.base):
                env.append(e)
            else:
                own.append(e)
        return own, env

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def short(errs, n=5):
    return [{"kind": e["kind"], "text": e["text"][:220], "at": (e.get("stack") or e.get("loc") or "")[:200]}
            for e in errs[:n]]


def raf(c, n=1):
    c.js("n => new Promise(r => { let i = 0; const f = () => { if (++i > n) r(); else requestAnimationFrame(f); }; requestAnimationFrame(f); })", n)


def center(c, sel, scroll=True):
    return c.js("""([s, sc]) => { const el = typeof s === 'string' ? document.querySelector(s) : s;
        if (!el) return null; if (sc) el.scrollIntoView({block: 'center', inline: 'center', behavior: 'instant'});
        const r = el.getBoundingClientRect(); return {x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height}; }""",
                [sel, scroll])


def pages_for(args, candidates=None):
    ps = lib.TEMPLATES["live"] if args.pages == "templates" else lib.pages("live")
    if candidates is not None:
        ps = [p for p in ps if p in candidates]
    return ps[: args.limit] if args.limit else ps


def uses(path, needle):
    try:
        return needle in open(os.path.join(lib.ROOT, path), encoding="utf-8").read()
    except Exception:
        return False


def wav(seconds=90, rate=8000):
    n = seconds * rate
    hdr = b"RIFF" + struct.pack("<I", 36 + n) + b"WAVEfmt " + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate, 1, 8) + \
        b"data" + struct.pack("<I", n)
    return hdr + bytes([128]) * n


# --------------------------------------------------------------------------- nav
NAV_STATE = """() => {
  const nav = document.querySelector('.page-wrap > nav'), btn = document.querySelector('.nav-toggle');
  const links = nav && nav.querySelector('.nav-links');
  const cs = links ? getComputedStyle(links) : null;
  const y0 = scrollY; scrollTo({top: 400, behavior: 'instant'}); const canScroll = scrollY > 0 || document.documentElement.scrollHeight <= innerHeight + 5;
  scrollTo({top: y0, behavior: 'instant'});
  return {
    open: nav ? nav.classList.contains('is-open') : null,
    aria: btn ? btn.getAttribute('aria-expanded') : null,
    label: btn ? btn.getAttribute('aria-label') : null,
    toggles: document.querySelectorAll('.nav-toggle').length,
    navs: document.querySelectorAll('.page-wrap > nav').length,
    navLinksIds: document.querySelectorAll('#nav-links').length,
    bars: document.querySelectorAll('.nav-toggle-bars').length,
    linksDisplay: cs ? cs.display : null,
    bodyOverflow: getComputedStyle(document.body).overflowY, htmlOverflow: getComputedStyle(document.documentElement).overflowY,
    canScroll: canScroll,
    active: document.activeElement ? (document.activeElement.className || document.activeElement.tagName) : null,
    focusOnBtn: document.activeElement === btn,
  };
}"""

NAV_REC = """() => {
  const btn = document.querySelector('.nav-toggle'); window.__navlog = [];
  new MutationObserver(ms => ms.forEach(() => window.__navlog.push(btn.getAttribute('aria-expanded'))))
    .observe(btn, {attributes: true, attributeFilter: ['aria-expanded']});
}"""

PANEL = """() => {
  const nav = document.querySelector('.page-wrap > nav'), links = nav.querySelector('.nav-links');
  const r = links.getBoundingClientRect(), a = [...links.querySelectorAll('a')];
  const vis = a.filter(x => { const q = x.getBoundingClientRect(); return q.height > 0 && q.bottom <= innerHeight && q.top >= 0; });
  const hit = a.filter(x => { const q = x.getBoundingClientRect(); if (!q.height) return false;
     const e = document.elementFromPoint(q.left + q.width / 2, Math.min(innerHeight - 1, q.top + q.height / 2)); return e && x.contains(e); });
  return {top: Math.round(r.top), bottom: Math.round(r.bottom), h: Math.round(r.height), links: a.length, inView: vis.length,
          hittable: hit.length, navPos: getComputedStyle(nav).position, vh: innerHeight,
          minLinkH: a.length ? Math.min(...a.map(x => Math.round(x.getBoundingClientRect().height))) : null};
}"""


def check_nav(b, base, args, w=390, h=844):
    out = []
    for p in pages_for(args):
        c = Ctx(b, base, w, h)
        r = {"page": p, "vw": w, "vh": h}
        try:
            c.goto(p, wait="domcontentloaded", settle=150)
            if not c.js("() => !!document.querySelector('.nav-toggle')"):
                r["missing_toggle"] = True
                r["has_nav"] = c.js("() => !!document.querySelector('.page-wrap > nav')")
                r["links_display"] = c.js("() => { const l = document.querySelector('.nav-links'); return l ? getComputedStyle(l).display : null; }")
                out.append(r)
                continue
            c.js(NAV_REC)
            pt = center(c, ".nav-toggle", scroll=False)
            r["btn"] = {k: round(v) for k, v in pt.items()}
            t0 = time.time()
            for _ in range(50):
                c.page.mouse.click(pt["x"], pt["y"])
            r["click50_s"] = round(time.time() - t0, 2)
            raf(c, 2)
            log = c.js("() => window.__navlog.splice(0)")
            r["click_flips"] = len(log)
            r["click_alternates"] = all(log[i] != log[i + 1] for i in range(len(log) - 1))
            r["after_clicks"] = c.js(NAV_STATE)
            # keyboard: Enter x50, Space x2
            c.js("() => document.querySelector('.nav-toggle').focus()")
            for _ in range(50):
                c.page.keyboard.press("Enter")
            for _ in range(2):
                c.page.keyboard.press(" ")
            raf(c, 2)
            log = c.js("() => window.__navlog.splice(0)")
            r["key_flips"] = len(log)
            r["after_keys"] = c.js(NAV_STATE)
            # open, Escape
            c.page.keyboard.press("Enter")
            c.page.keyboard.press("Tab")
            c.page.keyboard.press("Escape")
            raf(c, 2)
            r["after_escape"] = c.js(NAV_STATE)
            # open, click outside (body)
            c.page.mouse.click(pt["x"], pt["y"])
            r["panel_open"] = c.js(PANEL)
            c.js("() => document.body.click()")
            raf(c, 2)
            r["after_outside"] = c.js(NAV_STATE)
            # open then resize to desktop
            c.page.mouse.click(pt["x"], pt["y"])
            c.page.set_viewport_size({"width": 1440, "height": 900})
            raf(c, 3)
            r["after_resize_desktop"] = c.js(NAV_STATE)
            c.page.set_viewport_size({"width": w, "height": h})
            raf(c, 3)
            r["after_resize_back"] = c.js(NAV_STATE)
            own, env = c.errors()
            r["own_errors"] = short(own)
            r["env_errors"] = len(env)
            probs = []
            for k in ("after_clicks", "after_keys", "after_escape", "after_outside", "after_resize_desktop", "after_resize_back"):
                s = r[k]
                if s["open"] or s["aria"] != "false":
                    probs.append(k + ": left open")
                if s["toggles"] != 1 or s["navs"] != 1 or s["bars"] != 1 or s["navLinksIds"] > 1:
                    probs.append(k + ": duplicated elements %s" % {x: s[x] for x in ("toggles", "navs", "bars", "navLinksIds")})
                if s["bodyOverflow"] == "hidden" or s["htmlOverflow"] == "hidden" or not s["canScroll"]:
                    probs.append(k + ": scroll locked")
            if r["click_flips"] != 50 or not r["click_alternates"]:
                probs.append("50 clicks gave %d flips" % r["click_flips"])
            if r["key_flips"] != 52:
                probs.append("52 key presses gave %d flips" % r["key_flips"])
            if not r["after_escape"]["focusOnBtn"]:
                probs.append("focus not returned to toggle after Escape: " + str(r["after_escape"]["active"]))
            if r["after_clicks"]["linksDisplay"] != "none":
                probs.append("closed panel still displayed")
            po = r["panel_open"]
            if po["inView"] < po["links"] or po["hittable"] < po["links"]:
                probs.append("open panel: %d/%d links in view, %d hittable" % (po["inView"], po["links"], po["hittable"]))
            if own:
                probs.append("%d own errors" % len(own))
            r["problems"] = probs
        except Exception as e:
            r["exception"] = repr(e)[:300]
        finally:
            c.close()
        out.append(r)
        if r.get("problems") or r.get("exception") or r.get("missing_toggle"):
            print("  nav", p, w, h, r.get("problems"), r.get("exception", ""), "MISSING" if r.get("missing_toggle") else "")
    return out


def check_navland(b, base, args):
    """Landscape phones and small phones: is every link of the open panel reachable?"""
    out = []
    for (w, h) in ((844, 390), (740, 360), (320, 568), (390, 844)):
        for p in pages_for(args):
            c = Ctx(b, base, w, h)
            try:
                c.goto(p, wait="domcontentloaded", settle=150)
                if not c.js("() => !!document.querySelector('.nav-toggle') && getComputedStyle(document.querySelector('.nav-toggle')).display !== 'none'"):
                    continue
                pt = center(c, ".nav-toggle", scroll=False)
                c.page.mouse.click(pt["x"], pt["y"])
                raf(c, 2)
                a = c.js(PANEL)
                # can the reader scroll to reach links below the fold?
                c.page.mouse.wheel(0, 600)
                c.page.wait_for_timeout(150)
                a2 = c.js(PANEL)
                a["after_scroll_inView"] = a2["inView"]
                a["after_scroll_hittable"] = a2["hittable"]
                a["still_open_after_scroll"] = c.js("() => document.querySelector('.page-wrap > nav').classList.contains('is-open')")
                a.update(page=p, vw=w, vh=h)
                out.append(a)
            except Exception as e:
                out.append({"page": p, "vw": w, "vh": h, "exception": repr(e)[:200]})
            finally:
                c.close()
    bad = [x for x in out if "links" in x and max(x["inView"], x["after_scroll_inView"]) < x["links"]]
    for x in bad:
        print("  navland", x["page"], x["vw"], x["vh"], "links", x["links"], "inView", x["inView"], "afterScroll", x["after_scroll_inView"], x["navPos"])
    return out


# --------------------------------------------------------------------------- search / filter
PAYLOADS = {
    "long500": ("paraglider thermal wing " * 25)[:500],
    "emoji": "\U0001FA82\U0001F3D4️\U0001F468‍\U0001F469‍\U0001F467 flying \U0001F525",
    "rtl": "مرحبا بالعالم שלום",
    "regex": ".*+?[](){}|\\^$",
    "html_img": "<img src=x onerror=window.__x=1>",
    "html_svg": "\"><svg onload=window.__x=1><b>bold</b>",
    "accent_free": "Piedrahita",
    "accented": "Peñas",
}
XSS_STATE = """() => ({x: window.__x === 1, imgs: document.querySelectorAll('img[src="x"]').length,
  svgs: document.querySelectorAll('svg[onload]').length, bolds: [...document.querySelectorAll('b')].filter(b => b.textContent === 'bold').length})"""


def check_search(b, base, args):
    out = {"home": [], "library": [], "library_hash": []}
    # ---- homepage episode search
    c = Ctx(b, base, 1440, 900)
    try:
        c.goto("index.html", settle=600)
        for name, text in PAYLOADS.items():
            mark = len(c.events)
            c.js("() => { const i = document.getElementById('epSearchInput'); i.value = ''; i.dispatchEvent(new Event('input')); }")
            c.js("() => document.getElementById('epSearchInput').scrollIntoView({block:'center'})")
            c.page.click("#epSearchInput")
            t0 = time.time()
            c.page.keyboard.type(text)
            dt = time.time() - t0
            for _ in range(20):
                c.page.keyboard.press("Enter")
            c.page.click("#epSearchBtn")
            raf(c, 2)
            st = c.js("""() => { const b = document.getElementById('epSearchResults');
                return {value: document.getElementById('epSearchInput').value, active: b.classList.contains('active'),
                        results: b.querySelectorAll('.ep-search-result').length, empty: !!b.querySelector('.ep-search-empty'),
                        children: b.children.length}; }""")
            st.update(c.js(XSS_STATE))
            own, env = c.errors(mark)
            st.update(payload=name, typed_len=len(text), value_ok=st.pop("value") == text, type_s=round(dt, 2),
                      own_errors=short(own), longtasks=c.js("() => window.__lt.splice(0)"))
            out["home"].append(st)
    finally:
        c.close()
    # ---- library search (two boxes, view swap on first keystroke)
    for name, text in PAYLOADS.items():
        c = Ctx(b, base, 1440, 900)
        try:
            c.goto("library.html", settle=400)
            c.page.click("#q")
            t0 = time.time()
            c.page.keyboard.type(text)
            dt = time.time() - t0
            raf(c, 2)
            st = c.js("""() => ({q: document.getElementById('q').value, q2: document.getElementById('q2').value,
                active: document.activeElement && document.activeElement.id, cnt: document.getElementById('cnt').textContent,
                tiles: document.querySelectorAll('#eps .ep-tile').length, total: (window.LIB_EPISODES || []).length,
                rT: document.getElementById('rT').textContent, rS: document.getElementById('rS').textContent,
                noneShown: !document.getElementById('none').classList.contains('lib-hidden'), hash: location.hash})""")
            vis = st["q2"] if st["active"] == "q2" else st["q"]
            st.update(c.js(XSS_STATE))
            own, env = c.errors()
            st.update(payload=name, typed=text, value_ok=(vis == text), type_s=round(dt, 2), own_errors=short(own),
                      longtasks=c.js("() => window.__lt.splice(0)"))
            st["rS"] = st["rS"][:160]
            st.pop("q"); st.pop("q2")
            out["library"].append(st)
            # clear with 30 fast select-all + backspace + retype cycles
            if name == "long500":
                t0 = time.time()
                for _ in range(15):
                    c.page.keyboard.press("Control+A")
                    c.page.keyboard.press("Backspace")
                    c.page.keyboard.type("wing")
                raf(c, 2)
                st["retype15_s"] = round(time.time() - t0, 2)
                st["after_retype"] = c.js("() => ({active: document.activeElement && document.activeElement.id, val: document.activeElement && document.activeElement.value, tiles: document.querySelectorAll('#eps .ep-tile').length, hash: location.hash})")
        finally:
            c.close()
    # ---- library hash routes (the filter is also addressable)
    for h in ["#s=%3Cimg%20src%3Dx%20onerror%3Dwindow.__x%3D1%3E", "#s=__proto__", "#s=constructor", "#s=toString",
              "#s=%E0%A4%A", "#s=" + "A" * 5000, "#all"]:
        c = Ctx(b, base, 1440, 900)
        try:
            c.goto("library.html" + h, settle=400)
            st = c.js("""() => ({results: !document.getElementById('results').classList.contains('lib-hidden'),
                 rT: document.getElementById('rT').textContent.slice(0, 80), rS: document.getElementById('rS').textContent.slice(0, 80),
                 tiles: document.querySelectorAll('#eps .ep-tile').length})""")
            st.update(c.js(XSS_STATE))
            own, env = c.errors()
            st.update(hash=h[:60], own_errors=short(own))
            out["library_hash"].append(st)
        finally:
            c.close()
    for sec, rows in out.items():
        for r in rows:
            print("  search", sec, r.get("payload", r.get("hash")), {k: r.get(k) for k in ("results", "tiles", "cnt", "empty", "value_ok", "x", "imgs", "type_s", "rT", "rS")}, r.get("own_errors") or "")
    return out


def check_tagsort(b, base, args):
    out = []
    ps = [p for p in pages_for(args, None) if uses(p, "tags-sort.js")] if args.pages == "all" else ["tags/safety.html", "tags.html"]
    for p in ps:
        c = Ctx(b, base, 390, 844)
        try:
            c.goto(p, wait="domcontentloaded", settle=100)
            n0 = c.js("() => [...document.querySelectorAll('.tg-list .tg-ep')].map(li => li.getAttribute('data-title'))")
            nb = c.js("() => document.querySelectorAll('.tg-sort .pill').length")
            if not nb:
                out.append({"page": p, "no_sort_bar": True, "items": len(n0)})
                continue
            seq = [random.Random(i).randrange(nb) for i in range(100)]
            t0 = time.time()
            c.js("seq => { const b = document.querySelectorAll('.tg-sort .pill'); seq.forEach(i => b[i].click()); }", seq)
            dt = time.time() - t0
            st = c.js("""() => ({items: [...document.querySelectorAll('.tg-list .tg-ep')].map(li => li.getAttribute('data-title')),
                bars: document.querySelectorAll('.tg-sort').length, on: [...document.querySelectorAll('.tg-sort .pill.on')].map(b => b.textContent),
                status: (document.querySelector('.tg-sort-status') || {}).textContent})""")
            last = st["on"]
            items = st.pop("items")
            probs = []
            if sorted(items, key=str) != sorted(n0, key=str):
                probs.append("item set changed %d -> %d" % (len(n0), len(items)))
            if st["bars"] != 1 or len(last) != 1:
                probs.append("bars %d, active pills %s" % (st["bars"], last))
            own, env = c.errors()
            out.append({"page": p, "n": len(items), "clicks": 100, "js_s": round(dt, 3), "problems": probs, "own_errors": short(own), **st})
            if probs or own:
                print("  tagsort", p, probs, short(own))
        finally:
            c.close()
    return out


# --------------------------------------------------------------------------- forms
BAD_EMAILS = ["plainaddress", "@no-local.com", "a@b", "a@b.", "a b@c.com", "a@b@c.com", "<script>@x.com",
              "x@y.z<svg onload=window.__x=1>", "测试@例子.广告", "a" * 300 + "@x.com", " ", "a@-.-"]
TENK = ("Lorem ipsum dolor sit amet, thermals and ridge lift. " * 200)[:10240]
ENQ_FIELDS = ["#name", "#email", "#country", "#when", "#rating", "#total", "#recent", "#wing", "#xc", "#message"]


def form_state(c, status_sel, form_sel="form"):
    return c.js("""([s, fs]) => { const f = document.querySelector(fs); const bad = f ? f.querySelector(':invalid') : null;
        return {url: location.pathname, status: (document.querySelector(s) || {}).textContent || '',
        native_valid: f ? f.checkValidity() : null, native_msg: bad ? (bad.name || bad.id) + ': ' + bad.validationMessage.slice(0, 80) : null,
        x: window.__x === 1, focus: document.activeElement && (document.activeElement.id || document.activeElement.tagName)}; }""", [status_sel, form_sel])


def clear_status(c, sel):
    c.js("s => { const e = document.querySelector(s); if (e) e.textContent = ''; }", sel)


def check_enquire(b, base, args):
    out = {}
    # ---- enquire.html
    res = []
    c = Ctx(b, base, 1440, 900)
    try:
        c.goto("enquire.html", settle=300)

        def fill(vals):
            c.js("""(v) => { for (const [s, x] of Object.entries(v)) { const e = document.querySelector(s); e.value = x;
                     e.dispatchEvent(new Event('input', {bubbles: true})); } document.getElementById('consent').checked = true; }""", vals)

        good = {"#name": "Test Pilot", "#email": "pilot@example.com", "#country": "", "#when": "", "#rating": "APPI 3", "#total": "120",
                "#recent": "30", "#wing": "", "#xc": "", "#message": "Hello, interested in Kenya."}
        # 10 kB in every field
        fill({s: (TENK if s != "#email" else "a" * 10220 + "@x.com") for s in ENQ_FIELDS})
        n0 = len(c.navreq)
        clear_status(c, "#enqStatus")
        c.page.click("button[type=submit]")
        c.page.wait_for_timeout(200)
        st = form_state(c, "#enqStatus", "#enqForm")
        st.update(case="10kB every field", mailto=len(c.navreq) - n0,
                  field_lens=c.js("f => f.map(s => document.querySelector(s).value.length)", ENQ_FIELDS))
        res.append(st)
        # 10 kB in the message only, other fields sane
        fill(good)
        fill({"#message": TENK})
        n0 = len(c.navreq)
        clear_status(c, "#enqStatus")
        c.page.click("button[type=submit]")
        c.page.wait_for_timeout(150)
        st = form_state(c, "#enqStatus", "#enqForm")
        st.update(case="10kB message", mailto=len(c.navreq) - n0)
        res.append(st)
        # invalid emails
        for em in BAD_EMAILS:
            fill(good)
            fill({"#email": em})
            n0 = len(c.navreq)
            clear_status(c, "#enqStatus")
            c.page.click("button[type=submit]")
            c.page.wait_for_timeout(80)
            st = form_state(c, "#enqStatus", "#enqForm")
            st.update(case="email " + em[:40], mailto=len(c.navreq) - n0,
                      validationMessage=c.js("() => document.getElementById('email').validationMessage")[:120])
            res.append(st)
        # 20 quick submits of a valid enquiry
        fill(good)
        n0 = len(c.navreq)
        l0, b0 = len(c.launched), len(c.blocked)
        mark = len(c.events)
        clear_status(c, "#enqStatus")
        pt = center(c, "button[type=submit]")
        for _ in range(20):
            c.page.mouse.click(pt["x"], pt["y"])
        c.page.wait_for_timeout(800)
        st = form_state(c, "#enqStatus", "#enqForm")
        own, env = c.errors(mark)
        st.update(case="20 quick valid submits", mailto=len(c.navreq) - n0, own_errors=short(own),
                  launched=len(c.launched) - l0, blocked=len(c.blocked) - b0,
                  mailto_urls=len(set(x["url"] for x in c.navreq[n0:])))
        # a plain double click
        c.page.wait_for_timeout(1500)
        n0, l0, b0 = len(c.navreq), len(c.launched), len(c.blocked)
        c.page.mouse.dblclick(pt["x"], pt["y"])
        c.page.wait_for_timeout(800)
        res.append({"case": "double click submit", "mailto": len(c.navreq) - n0, "launched": len(c.launched) - l0, "blocked": len(c.blocked) - b0})
        res.append(st)
        # 20 quick submits with Enter in a field
        n0 = len(c.navreq)
        c.page.focus("#name")
        for _ in range(20):
            c.page.keyboard.press("Enter")
        c.page.wait_for_timeout(500)
        st = form_state(c, "#enqStatus", "#enqForm")
        st.update(case="20 Enter submits", mailto=len(c.navreq) - n0)
        res.append(st)
        # how long can an ordinary message be before the form refuses it?
        words = ("I have been flying for six years, mostly in the Alps, and I would like to know "
                 "whether the Kenya trip suits a pilot who is comfortable thermalling but new to "
                 "big desert conditions. ").split()
        realistic = dict(good, **{"#country": "Norway", "#when": "February next year", "#wing": "Ozone Rush 6, EN B",
                                  "#xc": "Longest flight 85 km, one SIV course in 2023, comfortable in strong thermals"})
        maxw = 0
        for nw in range(10, 600, 5):
            msg = " ".join((words * 20)[:nw])
            fill(realistic)
            fill({"#message": msg})
            n0 = len(c.navreq)
            c.js("() => document.getElementById('enqForm').requestSubmit()")
            if len(c.navreq) - n0 == 0:
                break
            maxw = nw
        msg = " ".join((words * 20)[:maxw])
        res.append({"case": "longest accepted English message with a realistic form", "max_words": maxw, "max_chars": len(msg)})
        # same with a Hindi / Norwegian message
        for lang, sample in (("hindi", "मैं छह साल से उड़ रहा हूँ "),
                             ("norwegian", "Jeg har fløyet i seks år og lurer på om turen passer for meg. ")):
            mx = 0
            for n in range(1, 200):
                fill(realistic)
                fill({"#message": sample * n})
                n0 = len(c.navreq)
                c.js("() => document.getElementById('enqForm').requestSubmit()")
                if len(c.navreq) - n0 == 0:
                    break
                mx = len(sample * n)
            res.append({"case": "longest accepted %s message" % lang, "max_chars": mx})
        own, env = c.errors()
        out["enquire_errors"] = short(own)
    finally:
        c.close()
    out["enquire"] = res
    # ---- partners.html and podcast.html question form
    for page, form, status, fields in (
            ("partners.html", "#pwForm", "#pwStatus", ["#pw-name", "#pw-email", "#pw-brand", "#pw-site", "#pw-message"]),
            ("podcast.html", "#questionForm", "#qfStatus", ["#questionForm input[type=text]", "#questionForm input[type=email]", "#questionForm textarea"])):
        res = []
        c = Ctx(b, base, 1440, 900)
        try:
            c.goto(page, settle=300)

            def fill2(vals):
                c.js("(v) => { for (const [s, x] of Object.entries(v)) { const e = document.querySelector(s); e.value = x; } }", vals)
            email_sel = [f for f in fields if "email" in f][0]
            fill2({s: (TENK if s != email_sel else "a" * 10220 + "@x.com") for s in fields})
            n0 = len(c.navreq)
            clear_status(c, status)
            c.js("s => document.querySelector(s).requestSubmit()", form)
            c.page.wait_for_timeout(150)
            st = form_state(c, status, form)
            st.update(case="10kB every field", mailto=len(c.navreq) - n0)
            res.append(st)
            good = {fields[0]: "Test", email_sel: "t@example.com", fields[-1]: "A question about thermals please."}
            if page == "partners.html":
                good["#pw-brand"] = "Brand"
                good["#pw-site"] = ""
            for em in BAD_EMAILS:
                fill2(good)
                fill2({email_sel: em})
                n0 = len(c.navreq)
                clear_status(c, status)
                c.js("s => document.querySelector(s).requestSubmit()", form)
                c.page.wait_for_timeout(50)
                st = form_state(c, status, form)
                st.update(case="email " + em[:40], mailto=len(c.navreq) - n0)
                res.append(st)
            fill2(good)
            n0, l0, b0 = len(c.navreq), len(c.launched), len(c.blocked)
            mark = len(c.events)
            clear_status(c, status)
            btn = form + " button[type=submit], " + form + " button"
            pt = center(c, btn)
            for _ in range(20):
                c.page.mouse.click(pt["x"], pt["y"])
            c.page.wait_for_timeout(600)
            st = form_state(c, status, form)
            own, env = c.errors(mark)
            st.update(case="20 quick valid submits", mailto=len(c.navreq) - n0, own_errors=short(own),
                      launched=len(c.launched) - l0, blocked=len(c.blocked) - b0)
            res.append(st)
            own, env = c.errors()
            out[page + "_errors"] = short(own)
        finally:
            c.close()
        out[page] = res
    for k, rows in out.items():
        if isinstance(rows, list):
            for r in rows:
                if isinstance(r, dict):
                    print("  form", k, r.get("case"), "mailto=%s" % r.get("mailto"), "launched=%s blocked=%s" % (r.get("launched"), r.get("blocked")), "native=%s" % r.get("native_msg"), (r.get("status") or "")[:70], r.get("max_words", ""), r.get("max_chars", ""), r.get("own_errors") or "")
    return out


def check_newsletter(b, base, args):
    out = []
    for page, blk in (("index.html", "[data-nl]"), ("podcast.html", "[data-nl]")):
        c = Ctx(b, base, 1440, 900)
        try:
            c.goto(page, settle=300)
            if not c.js("s => !!document.querySelector(s)", blk):
                out.append({"page": page, "no_block": True})
                continue
            posts = []
            c.page.on("request", lambda r: posts.append(r.url) if "mailerlite" in r.url else None)
            inp = blk + " input[type=email]"
            res = {"page": page, "cases": []}
            for em in BAD_EMAILS[:6] + ["pilot@example.com"]:
                c.page.fill(inp, em)
                n0 = len(posts)
                pt = center(c, blk + " button")
                for _ in range(20):
                    c.page.mouse.click(pt["x"], pt["y"])
                c.page.wait_for_timeout(400)
                st = c.js("""s => ({status: (document.querySelector(s + ' [data-nl-status]') || {}).textContent,
                      disabled: document.querySelector(s + ' button').disabled, value: document.querySelector(s + ' input[type=email]').value})""", blk)
                st.update(email=em[:30], requests=len(posts) - n0)
                res["cases"].append(st)
            own, env = c.errors()
            res["own_errors"] = short(own)
            out.append(res)
            for x in res["cases"]:
                print("  newsletter", page, x["email"], "requests", x["requests"], "disabled", x["disabled"], (x["status"] or "")[:70])
        finally:
            c.close()
    return out


# --------------------------------------------------------------------------- episode modal
MODAL_STATE = """() => { const o = document.getElementById('epModalOverlay');
  return {active: o ? o.classList.contains('active') : null, closing: o ? o.classList.contains('is-closing') : null,
          cards: o ? o.querySelectorAll('.kb-card').length : null, overlays: document.querySelectorAll('.ep-modal-overlay').length,
          bodyLock: document.body.classList.contains('kb-modal-open'), bodyOverflow: getComputedStyle(document.body).overflow,
          hist: history.length, pushes: window.__push || 0, focus: document.activeElement && (document.activeElement.className || document.activeElement.tagName).toString().slice(0, 40),
          url: location.pathname + location.hash}; }"""
PUSH_HOOK = "() => { const p = history.pushState.bind(history); window.__push = 0; history.pushState = function () { window.__push++; return p.apply(null, arguments); }; }"


def modal_pages(args):
    ps = [p for p in lib.pages("live") if uses(p, "episode-modal.js")]
    return ps[: args.limit] if args.limit else ps


def first_tile(c):
    return c.js("""() => { const t = [...document.querySelectorAll('[data-ep-slug],[data-ep-index]')].filter(e => e.getAttribute('aria-hidden') !== 'true');
        if (!t.length) return null; const el = t[0]; el.setAttribute('data-abuse-tile', '1'); return t.length; }""")


def backdrop_point(c):
    return c.js("""() => { const o = document.getElementById('epModalOverlay');
       for (const [x, y] of [[4, innerHeight - 4], [innerWidth - 4, innerHeight - 4], [4, 4], [innerWidth / 2, innerHeight - 3], [innerWidth - 4, innerHeight / 2]]) {
         if (document.elementFromPoint(x, y) === o) return {x, y}; } return null; }""")


def open_tile(c):
    c.js("() => document.querySelector('[data-abuse-tile]').scrollIntoView({block: 'center', behavior: 'instant'})")
    ensure_tile(c)
    pt = center(c, "[data-abuse-tile]", scroll=False)
    c.page.mouse.move(pt["x"], pt["y"])
    pt = center(c, "[data-abuse-tile]", scroll=False)
    c.page.mouse.click(pt["x"], pt["y"])
    return pt


def wait_modal(c, active, ms=1500):
    t0 = time.time()
    while time.time() - t0 < ms / 1000:
        if c.js("() => document.getElementById('epModalOverlay').classList.contains('active')") == active:
            return round((time.time() - t0) * 1000)
        c.page.wait_for_timeout(20)
    return None


def ensure_tile(c):
    """Tag a tile that is fully on screen now (the homepage rail keeps moving the old one away)."""
    c.js("""() => { const old = document.querySelector('[data-abuse-tile]');
        if (old) { const q = old.getBoundingClientRect(); if (q.left >= 0 && q.right <= innerWidth && q.width > 0) return; old.removeAttribute('data-abuse-tile'); }
        const t = [...document.querySelectorAll('[data-ep-slug],[data-ep-index]')].filter(e => e.getAttribute('aria-hidden') !== 'true');
        let el = t.find(e => { const q = e.getBoundingClientRect(); return q.width > 0 && q.left >= 0 && q.right <= innerWidth; });
        if (!el) { el = t.find(e => e.closest('.ep-track')) ? [...document.querySelectorAll('.ep-track [data-ep-slug]')].find(e => { const q = e.getBoundingClientRect(); return q.width > 0 && q.left >= 0 && q.right <= innerWidth; }) : t[0]; }
        (el || t[0]).setAttribute('data-abuse-tile', '1'); }""")


def check_modal(b, base, args):
    out = []
    ps = modal_pages(args) if args.pages == "all" else ["index.html", "library.html", "knowledge-base/flight-mechanics.html", "knowledge-base/navigators.html"]
    for p in ps:
        for (w, h) in ((1440, 900), (390, 844)):
            c = Ctx(b, base, w, h)
            r = {"page": p, "vw": w}
            try:
                c.goto(p + ("#all" if p == "library.html" else ""), settle=700)
                n = first_tile(c)
                r["tiles"] = n
                if not n:
                    out.append(r)
                    continue
                c.js(PUSH_HOOK)
                m0 = c.metrics()
                h0 = c.js("() => history.length")
                methods = ["escape", "backdrop", "back"]
                fails, close_ms = [], []
                t0 = time.time()
                for i in range(30):
                    ensure_tile(c)
                    open_tile(c)
                    if wait_modal(c, True, 800) is None:
                        fails.append((i, "did not open", c.js(MODAL_STATE)))
                        continue
                    s = c.js(MODAL_STATE)
                    if s["cards"] != 1 or not s["bodyLock"]:
                        fails.append((i, "open state", s))
                    how = methods[i % 3]
                    if how == "escape":
                        c.page.keyboard.press("Escape")
                    elif how == "backdrop":
                        bp = backdrop_point(c)
                        if bp:
                            c.page.mouse.click(bp["x"], bp["y"])
                        else:
                            c.page.keyboard.press("Escape")
                    else:
                        c.js("() => history.back()")
                    ms = wait_modal(c, False, 1500)
                    close_ms.append(ms)
                    s = c.js(MODAL_STATE)
                    if ms is None or s["bodyLock"] or s["cards"]:
                        fails.append((i, "close-" + how, s))
                r["cycle_s"] = round(time.time() - t0, 2)
                r["close_ms"] = [min(x for x in close_ms if x is not None), max(x for x in close_ms if x is not None)] if any(x is not None for x in close_ms) else None
                c.page.wait_for_timeout(600)
                s_end = c.js(MODAL_STATE)
                m1 = c.metrics()
                r["end"] = s_end
                r["history_growth"] = s_end["hist"] - h0
                r["pushes"] = s_end["pushes"]
                r["heap_kb"] = [round(m0["JSHeapUsedSize"] / 1024), round(m1["JSHeapUsedSize"] / 1024)]
                r["nodes"] = [m0["Nodes"], m1["Nodes"]]
                r["listeners"] = [m0["JSEventListeners"], m1["JSEventListeners"]]
                r["fails"] = fails[:6]
                r["fail_count"] = len(fails)
                # a single click after the loop still opens exactly once and pushes once
                ensure_tile(c)
                p0 = c.js("() => window.__push")
                open_tile(c)
                raf(c, 2)
                s = c.js(MODAL_STATE)
                r["single_open_pushes"] = s["pushes"] - p0
                r["single_open_active"] = s["active"]
                if c.js("() => !!document.querySelector('#epModalOverlay button.kb-med')"):
                    for _ in range(5):
                        c.js("() => { const m = document.querySelector('#epModalOverlay button.kb-med'); if (m) m.click(); }")
                    r["iframes_after_play"] = c.js("() => document.querySelectorAll('#epModalOverlay iframe').length")
                c.page.keyboard.press("Escape")
                wait_modal(c, False, 1500)
                r["final"] = c.js(MODAL_STATE)
                own, env = c.errors()
                r["own_errors"] = short(own)
                r["env_errors"] = len(env)
            except Exception as e:
                r["exception"] = repr(e)[:300]
            finally:
                c.close()
            out.append(r)
            print("  modal", p, w, "tiles", r.get("tiles"), "fails", r.get("fail_count"), r.get("fails", [])[:1], "closeMs", r.get("close_ms"),
                  "histGrowth", r.get("history_growth"), "pushes", r.get("pushes"),
                  "heap", r.get("heap_kb"), "nodes", r.get("nodes"), "listeners", r.get("listeners"), "single", r.get("single_open_pushes"),
                  "end", {k: (r.get("end") or {}).get(k) for k in ("active", "bodyLock", "cards")}, r.get("own_errors") or "", r.get("exception", ""))
    return out


def check_race(b, base, args):
    """Close, then open another episode straight away.
    mouse: the second click lands while the first popup is fading out.
    key: Escape then Enter on the tile focus returns to, which does not depend on hit testing, so only
         the history.back() of the first close can shut the second popup."""
    out = []
    for p in ("library.html#all", "knowledge-base/flight-mechanics.html", "index.html"):
        for mode, gap in (("mouse", 0), ("mouse", 100), ("mouse", 200), ("mouse", 350), ("key", 0), ("key", 20), ("key", 60)):
            c = Ctx(b, base, 1440, 900)
            try:
                c.goto(p, settle=700)
                first_tile(c)
                open_tile(c)
                wait_modal(c, True, 800)
                c.page.wait_for_timeout(300)
                c.js("""() => { window.__log = []; const t0 = performance.now(); const L = m => window.__log.push(Math.round(performance.now() - t0) + ' ' + m);
                     addEventListener('popstate', () => L('popstate'));
                     document.addEventListener('click', e => L('click on ' + (e.target.id || e.target.className || e.target.tagName).toString().slice(0, 24)), true); }""")
                h0 = c.js("() => history.length")
                c.page.keyboard.press("Escape")
                if gap:
                    c.page.wait_for_timeout(gap)
                if mode == "mouse":
                    pt = center(c, "[data-abuse-tile]", scroll=False)
                    hit = c.js("pt => { const e = document.elementFromPoint(pt.x, pt.y); return e ? (e.id || e.className || e.tagName).toString().slice(0, 30) : null; }", pt)
                    c.page.mouse.click(pt["x"], pt["y"])
                else:
                    hit = c.js("() => document.activeElement && document.activeElement.hasAttribute('data-abuse-tile')")
                    c.page.keyboard.press("Enter")
                c.page.wait_for_timeout(900)
                s = c.js(MODAL_STATE)
                s.update(page=p, mode=mode, gap_ms=gap, hit=hit, hist_delta=s["hist"] - h0, log=c.js("() => window.__log"))
                out.append(s)
                print("  race", p, mode, "gap", gap, "hit/focus", hit, "-> open", s["active"], "bodyLock", s["bodyLock"], s["log"])
            finally:
                c.close()
    return out


def check_stucklock(b, base, args):
    """Escape, then Enter on the tile that focus returns to, within the close fade. Is the page left
    scroll-locked with no popup? Swept over the delay, then run once on every page with the popup."""
    out = {"sweep": [], "pages": []}
    for gap in (0, 50, 100, 150, 200, 250, 300, 400):
        c = Ctx(b, base, 1440, 900)
        try:
            c.goto("knowledge-base/flight-mechanics.html", settle=600)
            first_tile(c)
            open_tile(c)
            wait_modal(c, True, 800)
            c.page.wait_for_timeout(300)
            c.page.keyboard.press("Escape")
            if gap:
                c.page.wait_for_timeout(gap)
            c.page.keyboard.press("Enter")
            c.page.wait_for_timeout(1200)
            s = c.js(MODAL_STATE)
            out["sweep"].append({"gap_ms": gap, "active": s["active"], "bodyLock": s["bodyLock"], "stuck": s["bodyLock"] and not s["active"]})
            print("  stucklock sweep gap", gap, out["sweep"][-1])
        finally:
            c.close()
    for p in modal_pages(args):
        for (w, h) in ((1440, 900), (390, 844)):
            c = Ctx(b, base, w, h)
            r = {"page": p, "vw": w}
            try:
                c.goto(p + ("#all" if p == "library.html" else ""), settle=700)
                if not first_tile(c):
                    r["tiles"] = 0
                    out["pages"].append(r)
                    continue
                ensure_tile(c)
                open_tile(c)
                r["opened"] = wait_modal(c, True, 800) is not None
                c.page.wait_for_timeout(300)
                c.page.keyboard.press("Escape")
                c.page.keyboard.press("Enter")
                c.page.wait_for_timeout(1200)
                s = c.js(MODAL_STATE)
                r.update(active=s["active"], bodyLock=s["bodyLock"], bodyOverflow=s["bodyOverflow"])
                r["stuck"] = s["bodyLock"] and not s["active"]
                y0 = c.js("() => scrollY")
                c.page.mouse.move(w / 2, h / 2)
                c.page.mouse.wheel(0, 1200)
                c.page.wait_for_timeout(500)
                r["wheel_scrolled_px"] = c.js("() => scrollY") - y0
                c.page.keyboard.press("Escape")
                c.js("() => history.back()")
                c.page.wait_for_timeout(600)
                s2 = c.js(MODAL_STATE)
                r["after_escape_and_back"] = {"active": s2["active"], "bodyLock": s2["bodyLock"]}
                own, env = c.errors()
                r["own_errors"] = short(own)
            except Exception as e:
                r["exception"] = repr(e)[:200]
            finally:
                c.close()
            out["pages"].append(r)
            print("  stucklock", p, w, {k: r.get(k) for k in ("opened", "active", "bodyLock", "stuck", "wheel_scrolled_px", "after_escape_and_back")}, r.get("exception", ""))
    return out


# --------------------------------------------------------------------------- episode players
def check_player(b, base, args):
    """YouTube pages: timestamp (seek) spam while the player cannot answer."""
    out = []
    ps = [p for p in lib.pages("live") if p.startswith("episodes/") and uses(p, "episode-sync.js") and uses(p, "<iframe")]
    if args.pages != "all":
        ps = ["episodes/sky-gods-flying-8000ers-antoine-girard.html"] + ps[:4]
    if args.limit:
        ps = ps[: args.limit]
    for p in ps:
        c = Ctx(b, base, 1440, 900)
        r = {"page": p}
        try:
            c.goto(p, wait="domcontentloaded", settle=200)
            n = c.js("() => document.querySelectorAll('.cd-seek').length")
            r["seekers"] = n
            if not n:
                out.append(r)
                continue
            seq = [random.Random(p + str(i)).randrange(n) for i in range(50)]
            t0 = time.time()
            c.js("seq => { const s = document.querySelectorAll('.cd-seek'); seq.forEach(i => s[i].click()); }", seq)
            r["js50_s"] = round(time.time() - t0, 2)
            # 10 real clicks and 10 keyboard activations
            for i in seq[:10]:
                pt = c.js("i => { const e = document.querySelectorAll('.cd-seek')[i]; e.scrollIntoView({block: 'center', behavior: 'instant'}); const q = e.getBoundingClientRect(); return {x: q.left + q.width / 2, y: q.top + q.height / 2}; }", i)
                c.page.mouse.click(pt["x"], pt["y"])
            for i in seq[10:20]:
                c.js("i => document.querySelectorAll('.cd-seek')[i].focus()", i)
                c.page.keyboard.press("Enter")
            last = seq[19]
            c.page.wait_for_timeout(800)
            st = c.js("""(i) => { const s = document.querySelectorAll('.cd-seek')[i]; const f = document.querySelector('.cd-player iframe');
                 const q = f.getBoundingClientRect();
                 return {iframes: document.querySelectorAll('.cd-player iframe').length, src: f.src.replace(/^https:\\/\\/[^/]+/, ''),
                         lastLabel: s.getAttribute('aria-label'), now: document.querySelectorAll('.cd-line.is-now').length,
                         activeChap: document.querySelectorAll('.cd-chap.active').length, frameInView: q.top < innerHeight && q.bottom > 0}; }""", last)
            r.update(st)
            m = re.search(r"start=(\d+)", st["src"])
            lab = re.search(r"Play from ([\d:]+)", st["lastLabel"] or "")
            if m and lab:
                parts = [int(x) for x in lab.group(1).split(":")]
                want = 0
                for x in parts:
                    want = want * 60 + x
                r["start_matches_last"] = int(m.group(1)) == want
            own, env = c.errors()
            r["own_errors"] = short(own)
            r["env_errors"] = len(env)
        except Exception as e:
            r["exception"] = repr(e)[:300]
        finally:
            c.close()
        out.append(r)
        if r.get("own_errors") or r.get("exception") or r.get("iframes", 1) != 1 or r.get("start_matches_last") is False or r.get("now", 0) > 1:
            print("  player", p, {k: r.get(k) for k in ("iframes", "start_matches_last", "now", "frameInView")}, r.get("own_errors"), r.get("exception", ""))
    print("  player pages:", len(out))
    return out


AU_STATE = """() => { const root = document.querySelector('.ep-au'), a = root.querySelector('audio'), b = root.querySelector('.ep-au-play');
  return {paused: a.paused, ui_playing: root.classList.contains('is-playing'), label: b.getAttribute('aria-label'),
          err: a.error ? a.error.code : null, net: a.networkState, ready: a.readyState, t: Math.round(a.currentTime * 10) / 10,
          fill: root.querySelector('.ep-au-fill').style.width, cur: root.querySelector('.ep-au-cur').textContent,
          status: (root.querySelector('[role=status], .ep-au-msg') || {}).textContent || null}; }"""


def check_audio(b, base, args):
    out = []
    ps = [p for p in lib.pages("live") if uses(p, "episode-audio.js")]
    if args.limit:
        ps = ps[: args.limit]
    snd = wav()
    for p in ps:
        for mode in ("served", "blocked"):
            c = Ctx(b, base, 1440, 900, audio=snd if mode == "served" else None)
            r = {"page": p, "mode": mode}
            try:
                c.goto(p, settle=300)
                pt = center(c, ".ep-au-play")
                # single play: what does a reader see?
                c.page.mouse.click(pt["x"], pt["y"])
                c.page.wait_for_timeout(1500)
                r["after_one_play"] = c.js(AU_STATE)
                # play/pause spam
                mark = len(c.events)
                for _ in range(31):
                    c.page.mouse.click(pt["x"], pt["y"])
                c.page.wait_for_timeout(1200)
                s = c.js(AU_STATE)
                r["after_spam31"] = s
                r["spam_consistent"] = (s["paused"] != s["ui_playing"]) and ((s["label"] == "Pause") == s["ui_playing"])
                own, env = c.errors(mark)
                r["spam_own_errors"] = len(own)
                r["spam_err_samples"] = short(own, 3)
                # seek spam on the bar
                bar = center(c, ".ep-au-bar")
                xs = [bar["x"] - bar["w"] / 2 + bar["w"] * random.Random(i).random() for i in range(50)]
                for x in xs:
                    c.page.mouse.click(x, bar["y"])
                c.page.wait_for_timeout(300)
                s = c.js(AU_STATE)
                frac = (xs[-1] - (bar["x"] - bar["w"] / 2)) / bar["w"]
                r["after_seek50"] = s
                r["seek_expected_fill"] = round(frac * 100, 1)
                # keyboard spam
                c.js("() => document.querySelector('.ep-au-bar').focus()")
                for k in ["ArrowRight"] * 40 + ["ArrowLeft"] * 10:
                    c.page.keyboard.press(k)
                c.page.wait_for_timeout(200)
                r["after_keys"] = c.js(AU_STATE)
                # chapter spam
                c.js("() => { const ch = document.querySelectorAll('.ep-au-chap'); for (let i = 0; i < 30; i++) ch[i % ch.length].click(); }")
                c.page.wait_for_timeout(600)
                r["after_chap30"] = c.js(AU_STATE)
                own, env = c.errors()
                r["own_errors_total"] = len(own)
                r["own_error_kinds"] = sorted(set(e["text"][:120] for e in own))[:6]
            except Exception as e:
                r["exception"] = repr(e)[:300]
            finally:
                c.close()
            out.append(r)
            print("  audio", p, mode, "one-play", {k: r.get("after_one_play", {}).get(k) for k in ("paused", "ui_playing", "label", "err")},
                  "spam-consistent", r.get("spam_consistent"), "spamErrs", r.get("spam_own_errors"), "errs", r.get("own_error_kinds"), r.get("exception", ""))
    return out


# --------------------------------------------------------------------------- carousels
CFL_STATE = """() => { const root = document.querySelector('.cfl'); const cards = [...root.querySelectorAll('.cfl-card')];
  const front = cards.map((c, i) => c.classList.contains('is-front') ? i : -1).filter(i => i >= 0);
  const dots = [...root.querySelectorAll('.cfl-dot')].map((d, i) => d.classList.contains('is-on') ? i : -1).filter(i => i >= 0);
  const lb = root.querySelector('.cfl-lb');
  const tf = front.length ? cards[front[0]].style.transform : '';
  return {n: cards.length, front, dots, live: (root.querySelector('.cfl-live') || {}).textContent,
          frontTitle: front.length ? cards[front[0]].getAttribute('data-title') : null, frontTransform: tf,
          lbOpen: lb ? !lb.hidden : null, bodyOverflow: document.body.style.overflow,
          fullOn: [...root.querySelectorAll('.cfl-full')].map((f, i) => f.classList.contains('is-on') ? i : -1).filter(i => i >= 0),
          focus: document.activeElement && document.activeElement.className.toString().slice(0, 30)}; }"""


def check_carousel(b, base, args):
    out = []
    for p in ("destinations/kenya.html", "destinations/india.html"):
        for (w, h) in ((1440, 900), (390, 844)):
            c = Ctx(b, base, w, h)
            r = {"page": p, "vw": w}
            try:
                c.goto(p, settle=500)
                s0 = c.js(CFL_STATE)
                N = s0["n"]
                m0 = c.metrics()
                nxt = center(c, ".cfl-next")
                prv = center(c, ".cfl-prev", scroll=False)
                t0 = time.time()
                for _ in range(100):
                    c.page.mouse.click(nxt["x"], nxt["y"])
                r["next100_s"] = round(time.time() - t0, 2)
                raf(c, 2)
                s = c.js(CFL_STATE)
                r["after_next100"] = {"front": s["front"], "dots": s["dots"], "expected": 100 % N}
                for _ in range(100):
                    c.page.mouse.click(prv["x"], prv["y"])
                raf(c, 2)
                s = c.js(CFL_STATE)
                r["after_prev100"] = {"front": s["front"], "dots": s["dots"], "expected": 0}
                rng = random.Random(7)
                exp = 0
                for _ in range(100):
                    if rng.random() < 0.5:
                        c.page.mouse.click(nxt["x"], nxt["y"])
                        exp += 1
                    else:
                        c.page.mouse.click(prv["x"], prv["y"])
                        exp -= 1
                c.page.wait_for_timeout(1200)
                s = c.js(CFL_STATE)
                r["after_mixed"] = {"front": s["front"], "dots": s["dots"], "expected": exp % N, "live_ok": s["live"] == s["frontTitle"],
                                    "settledTransform": s["frontTransform"][:80]}
                # keyboard arrows 100
                c.js("() => document.querySelector('.cfl-card.is-front').focus()")
                for _ in range(100):
                    c.page.keyboard.press("ArrowRight")
                raf(c, 2)
                s = c.js(CFL_STATE)
                r["after_arrow100"] = {"front": s["front"], "dots": s["dots"], "expected": (exp + 100) % N}
                # lightbox 30 cycles
                lbf = []
                for i in range(30):
                    fp = center(c, ".cfl-card.is-front")
                    c.page.mouse.click(fp["x"], fp["y"])
                    raf(c, 1)
                    s = c.js(CFL_STATE)
                    if not s["lbOpen"] or s["bodyOverflow"] != "hidden":
                        lbf.append((i, "open", s["lbOpen"], s["bodyOverflow"]))
                    if i % 3 == 0:
                        c.page.keyboard.press("Escape")
                    elif i % 3 == 1:
                        c.js("() => document.querySelector('.cfl-lb-x').click()")
                    else:
                        c.page.mouse.click(3, h - 3)
                    raf(c, 1)
                    s = c.js(CFL_STATE)
                    if s["lbOpen"] or s["bodyOverflow"] == "hidden":
                        lbf.append((i, "close", s["lbOpen"], s["bodyOverflow"]))
                r["lightbox_fails"] = lbf
                # lightbox next/prev 100 then close: carousel follows
                fp = center(c, ".cfl-card.is-front")
                c.page.mouse.click(fp["x"], fp["y"])
                for _ in range(100):
                    c.js("() => document.querySelector('.cfl-lb-next').click()")
                for _ in range(37):
                    c.js("() => document.querySelector('.cfl-lb-prev').click()")
                s_in = c.js(CFL_STATE)
                c.page.keyboard.press("Escape")
                raf(c, 2)
                s = c.js(CFL_STATE)
                r["lb_step"] = {"full_on": s_in["fullOn"], "front_after_close": s["front"], "lbOpen": s["lbOpen"], "overflow": s["bodyOverflow"]}
                # hero tabs (kenya/india) rapid 100
                if c.js("() => document.querySelectorAll('.khero-tab').length"):
                    nt = c.js("() => document.querySelectorAll('.khero-tab').length")
                    seq = [random.Random(i).randrange(nt) for i in range(100)]
                    c.js("() => window.scrollTo(0, 0)")
                    raf(c, 2)
                    for i in seq:
                        tp = c.js("i => { const q = document.querySelectorAll('.khero-tab')[i].getBoundingClientRect(); return {x: q.left + q.width / 2, y: q.top + q.height / 2, v: q.width > 0}; }", i)
                        if tp["v"]:
                            c.page.mouse.click(tp["x"], tp["y"])
                    raf(c, 2)
                    hs = c.js("""() => ({on: [...document.querySelectorAll('.khero-slide')].map((s, i) => s.classList.contains('is-on') ? i : -1).filter(i => i >= 0),
                        tabs: [...document.querySelectorAll('.khero-tab')].map((s, i) => s.classList.contains('is-on') ? i : -1).filter(i => i >= 0),
                        timing: document.querySelectorAll('.khero-tab.is-timing').length})""")
                    hs["expected"] = seq[-1]
                    r["hero_tabs"] = hs
                m1 = c.metrics()
                r["nodes"] = [m0["Nodes"], m1["Nodes"]]
                r["listeners"] = [m0["JSEventListeners"], m1["JSEventListeners"]]
                r["heap_kb"] = [round(m0["JSHeapUsedSize"] / 1024), round(m1["JSHeapUsedSize"] / 1024)]
                own, env = c.errors()
                r["own_errors"] = short(own)
            except Exception as e:
                r["exception"] = repr(e)[:300]
            finally:
                c.close()
            out.append(r)
            print("  carousel", p, w, {k: r.get(k) for k in ("after_next100", "after_prev100", "after_mixed", "after_arrow100", "lb_step", "hero_tabs")},
                  "lbfails", len(r.get("lightbox_fails", [])), r.get("own_errors") or "", r.get("exception", ""))
    return out


def check_faq(b, base, args):
    """Kenya/India FAQ cards: fast double and triple clicks on a summary."""
    out = []
    for p in ("destinations/kenya.html", "destinations/india.html"):
        for pattern in ("single", "double", "triple", "spam20"):
            c = Ctx(b, base, 1440, 900)
            try:
                c.goto(p, settle=300)
                n = c.js("() => document.querySelectorAll('.kfaq .kfaq-item').length")
                res = {"page": p, "pattern": pattern, "items": n}
                sm = center(c, ".kfaq .kfaq-item summary")
                clicks = {"single": 1, "double": 2, "triple": 3, "spam20": 20}[pattern]
                for _ in range(clicks):
                    c.page.mouse.click(sm["x"], sm["y"])
                c.page.wait_for_timeout(1000)
                st = c.js("""() => { const d = document.querySelector('.kfaq .kfaq-item'), bd = d.querySelector('.kfaq-body');
                    return {open: d.open, h: Math.round(bd.getBoundingClientRect().height), styleH: bd.style.height, trans: bd.style.transition,
                            full: bd.scrollHeight}; }""")
                res.update(st)
                res["expected_open"] = clicks % 2 == 1
                res["stuck"] = (st["open"] and st["h"] < 5) or (st["open"] != res["expected_open"])
                # recovery: one more click, then wait
                c.page.mouse.click(sm["x"], sm["y"])
                c.page.wait_for_timeout(900)
                st2 = c.js("""() => { const d = document.querySelector('.kfaq .kfaq-item'), bd = d.querySelector('.kfaq-body');
                    return {open: d.open, h: Math.round(bd.getBoundingClientRect().height)}; }""")
                res["after_one_more"] = st2
                own, env = c.errors()
                res["own_errors"] = short(own)
                out.append(res)
                print("  faq", p, pattern, {k: res[k] for k in ("open", "h", "styleH", "expected_open", "stuck")}, "then", st2)
            finally:
                c.close()
    return out


def check_kit(b, base, args):
    """Kenya/India packing kit: group heads and tiles clicked fast."""
    out = []
    for p in ("destinations/kenya.html", "destinations/india.html"):
        for clicks in (2, 3, 51):
            c = Ctx(b, base, 1440, 900)
            try:
                c.goto(p, settle=300)
                if not c.js("() => document.querySelectorAll('.kkit-group').length"):
                    out.append({"page": p, "no_kit": True})
                    c.close()
                    break
                hp = center(c, ".kkit-group .kkit-ghead")
                for _ in range(clicks):
                    c.page.mouse.click(hp["x"], hp["y"])
                c.page.wait_for_timeout(700)
                st = c.js("""() => { const g = document.querySelector('.kkit-group'), h = g.querySelector('.kkit-ghead'), bd = g.querySelector('.kkit-gbody');
                    return {expanded: h.getAttribute('aria-expanded'), h: Math.round(bd.getBoundingClientRect().height), styleH: bd.style.height}; }""")
                st.update(page=p, clicks=clicks, expected=("true" if clicks % 2 else "false"))
                st["consistent"] = (st["expanded"] == "true") == (st["h"] > 5) and st["expanded"] == st["expected"]
                # tile spam: 51 clicks on first tile
                tp = center(c, ".kkit-group .kkit-item")
                if tp and tp["h"] > 0:
                    for _ in range(51):
                        c.page.mouse.click(tp["x"], tp["y"])
                    c.page.wait_for_timeout(500)
                    st["tile"] = c.js("() => ({pressed: document.querySelector('.kkit-item').getAttribute('aria-pressed'), done: (document.getElementById('kkitDone') || {}).textContent})")
                own, env = c.errors()
                st["own_errors"] = short(own)
                out.append(st)
                print("  kit", p, clicks, st)
            finally:
                c.close()
    return out


def check_marquee(b, base, args):
    """Homepage episode rail: drag spam, then is it still moving, and does a tap still open a card?"""
    out = []
    for (w, h, touch) in ((1440, 900, False), (390, 844, False)):
        c = Ctx(b, base, w, h, touch=touch)
        r = {"vw": w}
        try:
            c.goto("index.html", settle=800)
            vp = center(c, ".episodes-viewport")
            tr = lambda: c.js("() => document.querySelector('.ep-track').style.transform")
            c.page.mouse.move(5, 5)
            a = tr(); c.page.wait_for_timeout(400); bb = tr()
            r["moving_before"] = a != bb
            r["cards_before"] = c.js("() => document.querySelectorAll('.ep-track > *').length")
            rng = random.Random(3)
            for _ in range(30):
                x0 = vp["x"] + rng.uniform(-vp["w"] / 3, vp["w"] / 3)
                c.page.mouse.move(x0, vp["y"])
                c.page.mouse.down()
                c.page.mouse.move(x0 + rng.uniform(-400, 400), vp["y"] + rng.uniform(-30, 30), steps=3)
                c.page.mouse.up()
            # release far outside
            c.page.mouse.move(vp["x"], vp["y"])
            c.page.mouse.down()
            c.page.mouse.move(vp["x"] + 200, vp["y"] + 400, steps=4)
            c.page.mouse.move(2, h - 2, steps=2)
            c.page.mouse.up()
            c.page.wait_for_timeout(1300)
            a = tr(); c.page.wait_for_timeout(400); bb = tr()
            r["moving_after"] = a != bb
            r["cards_after"] = c.js("() => document.querySelectorAll('.ep-track > *').length")
            r["dragging_class"] = c.js("() => document.querySelector('.episodes-viewport').classList.contains('is-dragging')")
            # a tap on a card opens the popup
            c.js(PUSH_HOOK)
            pt = c.js("""() => { const cs = [...document.querySelectorAll('.ep-track [data-ep-slug]')]; const vr = document.querySelector('.episodes-viewport').getBoundingClientRect();
                 const el = cs.find(e => { const q = e.getBoundingClientRect(); return q.left > vr.left + 10 && q.right < vr.right - 10; });
                 if (!el) return null; const q = el.getBoundingClientRect(); return {x: q.left + q.width / 2, y: q.top + q.height / 2}; }""")
            if pt:
                c.page.mouse.move(pt["x"], pt["y"])
                c.page.wait_for_timeout(100)
                c.page.mouse.click(pt["x"], pt["y"])
                c.page.wait_for_timeout(400)
                r["tap_opens"] = c.js("() => document.getElementById('epModalOverlay').classList.contains('active')")
                c.page.keyboard.press("Escape")
            own, env = c.errors()
            r["own_errors"] = short(own)
        except Exception as e:
            r["exception"] = repr(e)[:300]
        finally:
            c.close()
        out.append(r)
        print("  marquee", r)
    return out


# --------------------------------------------------------------------------- resize storm
LAYOUT = """() => { const de = document.documentElement;
  const wide = [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > innerWidth + 2 && getComputedStyle(e).position !== 'fixed'; }).length;
  return {iw: innerWidth, sw: de.scrollWidth, docH: de.scrollHeight, els: document.getElementsByTagName('*').length,
          toggles: document.querySelectorAll('.nav-toggle').length, navOpen: !!document.querySelector('.page-wrap > nav.is-open'),
          overlays: document.querySelectorAll('.ep-modal-overlay').length, trackKids: (document.querySelector('.ep-track') || {children: []}).children.length,
          wide: wide, bodyOverflow: getComputedStyle(document.body).overflow}; }"""


def check_resize(b, base, args):
    out = []
    for p in pages_for(args):
        c = Ctx(b, base, 1440, 900)
        r = {"page": p}
        try:
            c.goto(p, settle=1000)
            L0 = c.js(LAYOUT)
            m0 = c.metrics()
            mark = len(c.events)
            t0 = time.time()
            for i in range(20):
                c.page.set_viewport_size({"width": 390, "height": 844})
                if i == 3:  # open the phone menu mid-storm
                    c.js("() => { const b = document.querySelector('.nav-toggle'); if (b) b.click(); }")
                c.page.wait_for_timeout(15)
                c.page.set_viewport_size({"width": 1440, "height": 900})
                c.page.wait_for_timeout(15)
            r["storm_s"] = round(time.time() - t0, 2)
            c.page.wait_for_timeout(1500)
            L1 = c.js(LAYOUT)
            m1 = c.metrics()
            own, env = c.errors(mark)
            r.update(before=L0, after=L1, listeners=[m0["JSEventListeners"], m1["JSEventListeners"]], nodes=[m0["Nodes"], m1["Nodes"]],
                     own_errors=short(own), longtasks=sorted(c.js("() => window.__lt.splice(0)"), reverse=True)[:5])
            # compare with a fresh load at 1440
            c2 = Ctx(b, base, 1440, 900)
            try:
                c2.goto(p, settle=1000)
                r["fresh"] = c2.js(LAYOUT)
            finally:
                c2.close()
            probs = []
            if L1["sw"] > L1["iw"] + 1:
                probs.append("horizontal overflow %d > %d" % (L1["sw"], L1["iw"]))
            if L1["els"] != L0["els"]:
                probs.append("element count %d -> %d" % (L0["els"], L1["els"]))
            if L1["toggles"] != 1 or L1["overlays"] > 1 or L1["trackKids"] != L0["trackKids"]:
                probs.append("duplicates %s" % {k: L1[k] for k in ("toggles", "overlays", "trackKids")})
            if L1["navOpen"]:
                probs.append("phone menu still open at 1440")
            if abs(L1["docH"] - r["fresh"]["docH"]) > max(40, 0.02 * r["fresh"]["docH"]):
                probs.append("doc height %d vs fresh %d" % (L1["docH"], r["fresh"]["docH"]))
            if m1["JSEventListeners"] - m0["JSEventListeners"] > 5:
                probs.append("listeners %d -> %d" % (m0["JSEventListeners"], m1["JSEventListeners"]))
            if own:
                probs.append("%d own errors" % len(own))
            r["problems"] = probs
        except Exception as e:
            r["exception"] = repr(e)[:300]
        finally:
            c.close()
        out.append(r)
        print("  resize", p, r.get("problems"), "listeners", r.get("listeners"), "nodes", r.get("nodes"), r.get("exception", ""))
    return out


# --------------------------------------------------------------------------- back / forward
CHAIN = ["index.html", "about.html", "podcast.html", "library.html", "knowledge-base.html",
         "knowledge-base/flight-mechanics.html", "episodes/sky-gods-flying-8000ers-antoine-girard.html",
         "tags/safety.html", "sitemap.html", "enquire.html"]
PAGE_OK = """() => { const main = document.querySelector('main, .page-wrap');
  const op = [document.documentElement, document.body, main].filter(Boolean).map(e => +getComputedStyle(e).opacity);
  return {path: location.pathname, toggles: document.querySelectorAll('.nav-toggle').length, h1: !!document.querySelector('h1'),
          textLen: (document.body.innerText || '').length, minOpacity: Math.min(...op), ready: document.readyState,
          overlays: document.querySelectorAll('.ep-modal-overlay').length}; }"""


def check_history(b, base, args):
    out = {}
    for (w, h) in ((1440, 900), (390, 844)):
        c = Ctx(b, base, w, h)
        res = {}
        try:
            for p in CHAIN:
                c.goto(p, settle=250)
            mark = len(c.events)

            def spam(fn, n, gap):
                for _ in range(n):
                    try:
                        c.page.evaluate(fn)
                    except Exception:
                        pass
                    time.sleep(gap)

            for gap in (0.05, 0.0):
                spam("() => history.back()", 9, gap)
                c.page.wait_for_timeout(2500)
                try:
                    c.page.wait_for_load_state("load", timeout=5000)
                except Exception:
                    pass
                res["back_gap%d" % int(gap * 1000)] = c.js(PAGE_OK)
                spam("() => history.forward()", 9, gap)
                c.page.wait_for_timeout(2500)
                try:
                    c.page.wait_for_load_state("load", timeout=5000)
                except Exception:
                    pass
                res["fwd_gap%d" % int(gap * 1000)] = c.js(PAGE_OK)
            # ping-pong 20 times
            spam("() => history.back()", 1, 0.3)
            for i in range(20):
                spam("() => history.%s()" % ("back" if i % 2 else "forward"), 1, 0.02)
            c.page.wait_for_timeout(2500)
            res["pingpong"] = c.js(PAGE_OK)
            # verify every page in the chain still renders by stepping back slowly
            slow = []
            for i in range(9):
                c.page.go_back(wait_until="load", timeout=10000)
                c.page.wait_for_timeout(400)
                slow.append(c.js(PAGE_OK))
            res["slow_back"] = slow
            own, env = c.errors(mark)
            res["own_errors"] = short(own, 8)
            res["env_errors"] = len(env)
        except Exception as e:
            res["exception"] = repr(e)[:300]
        finally:
            c.close()
        out["%dx%d" % (w, h)] = res
        for k, v in res.items():
            if isinstance(v, dict):
                print("  history", w, k, v)
        print("  history", w, "slow back:", [(x["path"], x["minOpacity"], x["toggles"]) for x in res.get("slow_back", [])], res.get("own_errors"), res.get("exception", ""))
    return out


# --------------------------------------------------------------------------- scroll storm
FADED = """() => { const out = [];
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('[aria-hidden=true], nav, footer, .ep-modal-overlay')) continue;
    const t = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ');
    if (t.length < 12) continue;
    const r = e.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight || r.width === 0) continue;
    let o = 1, x = e; while (x && x !== document.documentElement) { o *= +getComputedStyle(x).opacity; x = x.parentElement; }
    const vis = getComputedStyle(e).visibility;
    if (o < 0.2 || vis === 'hidden') out.push((e.className || e.tagName).toString().slice(0, 40) + ' :: ' + t.slice(0, 40));
  } return out; }"""


def sample_faded(c, h):
    H = c.js("() => document.documentElement.scrollHeight")
    res = {}
    for f in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        y = int(max(0, H - h) * f)
        c.js("y => window.scrollTo({top: y, behavior: 'instant'})", y)
        c.page.wait_for_timeout(1300)
        res[str(f)] = c.js(FADED)
    return res


def check_scroll(b, base, args):
    out = {"heights": {}}
    # find the longest pages at phone width
    ps = pages_for(args)
    c = Ctx(b, base, 390, 844)
    try:
        for p in ps:
            try:
                c.goto(p, wait="domcontentloaded", settle=0)
                out["heights"][p] = c.js("() => document.documentElement.scrollHeight")
            except Exception as e:
                out["heights"][p] = -1
    finally:
        c.close()
    top = sorted(out["heights"].items(), key=lambda kv: -kv[1])[:3]
    out["longest"] = top
    print("  scroll longest", top)
    targets = [top[0][0], "index.html", "destinations/kenya.html"]
    runs = []
    for p in dict.fromkeys(targets):
        for (w, h) in ((390, 844), (1440, 900)):
            r = {"page": p, "vw": w}
            # control: fresh load, sample without abuse
            c = Ctx(b, base, w, h)
            try:
                c.goto(p, settle=800)
                r["control_faded"] = sample_faded(c, h)
            finally:
                c.close()
            c = Ctx(b, base, w, h)
            try:
                c.goto(p, settle=800)
                H = c.js("() => document.documentElement.scrollHeight")
                m0 = c.metrics(gc=False)
                mark = len(c.events)
                t0 = time.time()
                for _ in range(20):
                    c.js("H => window.scrollTo({top: H, behavior: 'instant'})", H)
                    raf(c, 1)
                    c.js("() => window.scrollTo({top: 0, behavior: 'instant'})")
                    raf(c, 1)
                # wheel storm too
                c.page.mouse.move(w / 2, h / 2)
                for i in range(20):
                    c.page.mouse.wheel(0, 20000 if i % 2 == 0 else -20000)
                    c.page.wait_for_timeout(30)
                # keyboard End / Home
                for i in range(10):
                    c.page.keyboard.press("End")
                    c.page.keyboard.press("Home")
                r["storm_s"] = round(time.time() - t0, 2)
                c.page.wait_for_timeout(1500)
                m1 = c.metrics(gc=False)
                r["docH"] = [H, c.js("() => document.documentElement.scrollHeight")]
                r["scrollY_end"] = c.js("() => scrollY")
                r["layout_ms"] = round((m1["LayoutDuration"] - m0["LayoutDuration"]) * 1000)
                r["script_ms"] = round((m1["ScriptDuration"] - m0["ScriptDuration"]) * 1000)
                r["longtasks"] = sorted(c.js("() => window.__lt.splice(0)"), reverse=True)[:6]
                r["faded"] = sample_faded(c, h)
                own, env = c.errors(mark)
                r["own_errors"] = short(own)
                ctrl = set(x for v in r["control_faded"].values() for x in v)
                aft = set(x for v in r["faded"].values() for x in v)
                r["newly_faded"] = sorted(aft - ctrl)[:15]
            except Exception as e:
                r["exception"] = repr(e)[:300]
            finally:
                c.close()
            runs.append(r)
            print("  scroll", p, w, {k: r.get(k) for k in ("docH", "storm_s", "layout_ms", "script_ms", "longtasks", "newly_faded")}, r.get("own_errors") or "", r.get("exception", ""))
    out["runs"] = runs
    return out


CHECKS = {"nav": check_nav, "navland": check_navland, "search": check_search, "tagsort": check_tagsort,
          "enquire": check_enquire, "newsletter": check_newsletter, "modal": check_modal, "race": check_race, "stucklock": check_stucklock,
          "player": check_player, "audio": check_audio, "carousel": check_carousel, "faq": check_faq, "kit": check_kit,
          "marquee": check_marquee, "resize": check_resize, "history": check_history, "scroll": check_scroll}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checks", nargs="+")
    ap.add_argument("--pages", default="templates", choices=["templates", "all"])
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    names = list(CHECKS) if args.checks == ["all"] else args.checks
    with lib.server(PORT) as base:
        with lib.browser() as b:
            for n in names:
                t0 = time.time()
                print("== %s (%s)" % (n, args.pages), flush=True)
                res = CHECKS[n](b, base, args)
                fp = os.path.join(HERE, "results_%s%s.json" % (n, "_all" if args.pages == "all" else ""))
                with open(fp, "w", encoding="utf-8") as f:
                    json.dump(res, f, indent=1, default=str)
                print("   -> %s in %.1fs" % (fp, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
