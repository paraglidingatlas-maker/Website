#!/usr/bin/env python3
"""Degraded-mode stress test for the LIVE Paragliding Atlas pages (repo root).

usage:
  python3 degraded.py nojs    [page ...]   JS off vs JS on, all 180 live pages (or the pages given)
  python3 degraded.py forms   [page ...]   submit every form with JS off (defaults: enquire, podcast, partners, index)
  python3 degraded.py motion  [page ...]   prefers-reduced-motion: reduce on the 15 templates
  python3 degraded.py colors  [page ...]   forced-colors: active / prefers-color-scheme: light on the templates
  python3 degraded.py print   [page ...]   A4 PDF on the templates
  python3 degraded.py spacing [page ...]   WCAG 1.4.12 text spacing on the templates
  python3 degraded.py all
Results are written to ./out/<part>.json next to this script. Port 8814 only.
Read-only on /home/user/Website.
"""
import json
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, "pylib"))
import lib  # noqa: E402

PORT = 8814
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
WORKERS = 4


def dump(name, data):
    fp = os.path.join(OUT, name)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, default=str)
    return fp


def new_ctx(b, base, **kw):
    kw.setdefault("viewport", {"width": 1280, "height": 900})
    ctx = b.new_context(**kw)
    # External hosts are blocked by the environment's proxy anyway; abort them at once
    # instead of waiting for the proxy, so both modes see the same (failed) externals.
    ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) or
              r.request.url.startswith("data:") or r.request.url.startswith("blob:") else r.abort())
    return ctx


def goto(pg, url, timeout=25000):
    try:
        pg.goto(url, wait_until="load", timeout=timeout)
    except Exception as e:  # keep measuring what did load
        return str(e)[:200]
    return None


def scroll_through(pg, step=700, pause=0.12):
    h = pg.evaluate("Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0)")
    y = 0
    while y < h:
        y += step
        pg.evaluate("y => window.scrollTo({top: y, behavior: 'instant'})", y)
        time.sleep(pause)
        h = pg.evaluate("Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0)")
        if y > 60000:
            break
    time.sleep(0.4)
    pg.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    time.sleep(0.3)


# ---------------------------------------------------------------- shared in-page helpers
HELPERS = r"""
window.__dg = (function(){
  const V = el => el.checkVisibility ? el.checkVisibility({opacityProperty:true, visibilityProperty:true}) : true;
  const P = el => { const p = []; let e = el;
    for (let i = 0; i < 5 && e && e.nodeType === 1 && e !== document.body && e !== document.documentElement; i++) {
      let s = e.tagName.toLowerCase();
      if (e.id) { p.unshift(s + '#' + CSS.escape(e.id)); break; }
      const c = [...e.classList].filter(c => !/^(visible|reveal|is-|js-)/.test(c)).slice(0, 2).map(c => CSS.escape(c)).join('.');
      if (c) s += '.' + c;
      p.unshift(s); e = e.parentElement; }
    return p.join(' > '); };
  const clipCache = new Map();
  function clipped(el, r) {           // selector of an overflow:hidden/clip ancestor that hides r entirely
    for (let e = el.parentElement; e && e !== document.documentElement; e = e.parentElement) {
      const cs = getComputedStyle(e);
      const ox = cs.overflowX, oy = cs.overflowY;
      if (ox === 'visible' && oy === 'visible') continue;
      const a = e.getBoundingClientRect();
      const hiding = (ox === 'hidden' || ox === 'clip' || oy === 'hidden' || oy === 'clip');
      if (a.width < 2 || a.height < 2) return P(e);
      if (hiding && (r.right <= a.left + 1 || r.left >= a.right - 1 || r.bottom <= a.top + 1 || r.top >= a.bottom - 1)) return P(e);
      if (cs.position === 'fixed') break;
    }
    return null;
  }
  function why(el) {
    let disp = null, opa = null, vis = null;
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.display === 'none') disp = e;
      if (parseFloat(cs.opacity) === 0) opa = e;
      if (cs.visibility !== 'visible') vis = e;
      if (cs.contentVisibility === 'hidden') disp = e;
    }
    if (disp) return {sel: P(disp), prop: 'display:none'};
    if (opa) return {sel: P(opa), prop: 'opacity:0', inline: (opa.getAttribute('style')||'').slice(0,80)};
    if (vis) return {sel: P(vis), prop: 'visibility:hidden'};
    return null;
  }
  function textNodes(root) {
    const out = [];
    const tw = document.createTreeWalker(root || document.body, NodeFilter.SHOW_TEXT);
    for (let n; (n = tw.nextNode());) {
      const t = n.nodeValue.replace(/\s+/g, ' ').trim();
      if (!t) continue;
      const el = n.parentElement;
      if (!el || /^(SCRIPT|STYLE|TEMPLATE|TITLE)$/.test(el.tagName)) continue;
      out.push([n, el, t]);
    }
    return out;
  }
  const rng = document.createRange();
  function nodeRect(n) { rng.selectNodeContents(n); return rng.getBoundingClientRect(); }
  function nodeRects(n) { rng.selectNodeContents(n); return [...rng.getClientRects()]; }
  return {V, P, clipped, why, textNodes, nodeRect, nodeRects};
})();
"""

# ---------------------------------------------------------------- part 1: JS off vs on
MEASURE_NOJS = r"""
() => {
  const {V, P, clipped, why, textNodes, nodeRect} = window.__dg;
  const vcache = new Map();
  function elVis(el) {
    if (vcache.has(el)) return vcache.get(el);
    let v = V(el);
    if (v) { const r = el.getBoundingClientRect(); if (clipped(el, r)) v = false; }
    vcache.set(el, v); return v;
  }
  const texts = {};   // key -> {v: visibleCount, h: hiddenCount, len, sel, why}
  let visLen = 0, allLen = 0;
  for (const [n, el, t] of textNodes()) {
    const r = nodeRect(n);
    const vis = r.width > 0 && r.height > 0 && elVis(el);
    const k = el.tagName + '|' + t.slice(0, 90);
    const o = texts[k] || (texts[k] = {v: 0, h: 0, len: t.length, sel: null, why: null});
    allLen += t.length;
    if (vis) { o.v++; visLen += t.length; if (!o.sel) o.sel = P(el); }
    else { o.h++; if (!o.why) { o.why = why(el) || {sel: P(el), prop: clipped(el, r) ? 'clipped-by:' + clipped(el, r) : 'zero-size'}; } }
  }
  const imgs = [...document.querySelectorAll('img')].map(im => {
    const r = im.getBoundingClientRect();
    const raw = im.getAttribute('src') || im.getAttribute('data-src') || im.getAttribute('data-lazy') || '';
    let key = raw; try { key = new URL(raw, location.href).href; } catch (e) {}
    return {key, src: im.getAttribute('src'), ds: im.getAttribute('data-src') || im.getAttribute('data-srcset') || null,
      loading: im.getAttribute('loading'), ok: im.complete && im.naturalWidth > 0,
      vis: V(im) && r.width > 1 && r.height > 1 && !clipped(im, r), w: Math.round(r.width), h: Math.round(r.height),
      sel: P(im), alt: im.getAttribute('alt'), why: V(im) ? null : why(im)};
  });
  // CSS background images on visible boxes
  const bgs = [];
  for (const el of document.querySelectorAll('body *')) {
    const bi = getComputedStyle(el).backgroundImage;
    if (!bi || bi.indexOf('url(') < 0) continue;
    const r = el.getBoundingClientRect();
    bgs.push({url: bi.slice(0, 200), vis: V(el) && r.width > 1 && r.height > 1, sel: P(el)});
  }
  // empty containers: no text, no media, but a box (candidates for script-filled holes)
  const empties = [];
  const MEDIA = 'img,svg,video,canvas,iframe,picture,input,select,textarea,button,audio,object,embed';
  for (const el of document.querySelectorAll('body div, body section, body ul, body ol, body main, body article, body aside, body p, body table, body tbody, body figure, body nav, body span, body dl, body output')) {
    if (el.closest('noscript,template')) continue;
    if (el.textContent.trim()) continue;
    if (el.querySelector(MEDIA)) continue;
    if (!el.id && !el.className) continue;
    const r = el.getBoundingClientRect();
    empties.push({sel: P(el), id: el.id || null, w: Math.round(r.width), h: Math.round(r.height), vis: V(el)});
  }
  const links = [...document.querySelectorAll('a[href]')];
  const visLinks = links.filter(a => { const r = a.getBoundingClientRect(); return r.width > 0 && r.height > 0 && V(a); });
  const deadCtl = [...document.querySelectorAll('button:not([type=submit]), a[href="#"], a[href^="javascript:"], [role=button]')]
      .filter(e => !e.closest('form') || e.getAttribute('type') === 'button')
      .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && V(e); })
      .map(e => ({sel: P(e), label: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 50)}));
  const forms = [...document.querySelectorAll('form')].map(f => ({sel: P(f), action: f.getAttribute('action'), method: f.getAttribute('method'),
      vis: V(f), fields: f.querySelectorAll('input,textarea,select').length}));
  return {visLen, allLen, innerText: document.body.innerText.length, texts, imgs, bgs, empties,
          links: links.length, visLinks: visLinks.length, deadCtl, forms,
          noscript: document.querySelectorAll('noscript').length,
          docH: document.documentElement.scrollHeight};
}
"""

CONTAINER_TEXT = r"""
(sels) => {
  const {V} = window.__dg;
  const out = {};
  for (const s of sels) {
    let el = null; try { el = document.querySelector(s); } catch (e) {}
    if (!el) { out[s] = null; continue; }
    const r = el.getBoundingClientRect();
    out[s] = {txt: V(el) ? el.innerText.replace(/\s+/g, ' ').trim().length : 0,
              media: el.querySelectorAll('img,svg,video,canvas,iframe').length, w: Math.round(r.width), h: Math.round(r.height),
              sample: (el.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 80)};
  }
  return out;
}
"""

MOBILE_NAV = r"""
() => {
  const {V} = window.__dg;
  const nav = document.querySelector('.page-wrap > nav') || document.querySelector('nav');
  const vis = a => { const r = a.getBoundingClientRect(); return r.width > 0 && r.height > 0 && V(a); };
  const nl = nav ? [...nav.querySelectorAll('.nav-links a, a')] : [];
  const footer = document.querySelector('footer');
  return {hasNav: !!nav, navLinks: nl.length, navVisible: nl.filter(vis).map(a => a.innerText.trim()).filter(Boolean),
          toggle: !!document.querySelector('.nav-toggle'),
          footerVisible: footer ? [...footer.querySelectorAll('a')].filter(vis).length : 0};
}
"""


def nojs_page(args):
    base, path = args
    res = {"path": path}
    with lib.browser() as b:
        sels = []
        for mode, js in (("off", False), ("on", True)):
            ctx = new_ctx(b, base, java_script_enabled=js)
            if js:
                ctx.add_init_script(HELPERS)
            pg = ctx.new_page()
            err = goto(pg, base + path)
            if not js:
                pg.evaluate(HELPERS)
            time.sleep(0.5 if js else 0.05)
            scroll_through(pg, step=800 if js else 3000, pause=0.12 if js else 0.02)
            time.sleep(1.0 if js else 0.05)
            m = pg.evaluate(MEASURE_NOJS)
            m["err"] = err
            res[mode] = m
            if not js:
                sels = [e["sel"] for e in m["empties"]][:400]
            else:
                # containers that are empty without JS: how much do they hold with JS?
                res["filled"] = pg.evaluate(CONTAINER_TEXT, sels) if sels else {}
            ctx.close()
        # phone-width header navigation, JS off vs on (toggle opened)
        nav = {}
        for mode, js in (("off", False), ("on", True)):
            ctx = new_ctx(b, base, java_script_enabled=js, viewport={"width": 390, "height": 844}, is_mobile=True,
                          has_touch=True)
            pg = ctx.new_page()
            goto(pg, base + path)
            pg.evaluate(HELPERS)
            if js:
                time.sleep(0.3)
                try:
                    pg.click(".nav-toggle", timeout=2000)
                    time.sleep(0.4)
                except Exception:
                    pass
            nav[mode] = pg.evaluate(MOBILE_NAV)
            ctx.close()
        res["mnav"] = nav
    return res


def summarize_nojs(r):
    off, on = r["off"], r["on"]
    hidden, absent = [], []
    for k, o in on["texts"].items():
        if o["v"] == 0:
            continue
        f = off["texts"].get(k)
        fv = f["v"] if f else 0
        miss = o["v"] - fv
        if miss <= 0:
            continue
        if f and f["h"] > 0:
            hidden.append({"text": k.split("|", 1)[1][:70], "len": o["len"] * miss, "why": f["why"], "onsel": o["sel"]})
        else:
            absent.append({"text": k.split("|", 1)[1][:70], "len": o["len"] * miss, "onsel": o["sel"]})
    # images
    def imgset(m, need_ok):
        s = {}
        for im in m["imgs"]:
            if im["vis"] and (im["ok"] or not need_ok):
                s[im["key"]] = im
        return s
    on_ok = imgset(on, True)
    off_ok = imgset(off, True)
    on_box = imgset(on, False)
    off_all = {im["key"]: im for im in off["imgs"]}
    img_missing = []
    for k, im in on_box.items():
        if k in off_ok:
            continue
        o = off_all.get(k)
        if o is None:
            cause = "not in HTML (script-inserted)"
        elif not o["ok"]:
            cause = "in HTML, never loaded (src=%r data-src=%r loading=%r)" % (o["src"], o["ds"], o["loading"])
        elif not o["vis"]:
            cause = "loaded but hidden: %s" % (o["why"],)
        else:
            continue
        img_missing.append({"key": k[-90:], "sel": im["sel"], "cause": cause, "loaded_with_js": k in on_ok,
                            "w": im["w"], "h": im["h"]})
    filled = []
    for e in off["empties"]:
        f = r.get("filled", {}).get(e["sel"])
        if f and (f["txt"] >= 20 or f["media"] > 0):
            filled.append({"sel": e["sel"], "off_box": [e["w"], e["h"]], "on_txt": f["txt"], "on_media": f["media"],
                           "sample": f["sample"]})
    return {"path": r["path"], "visLen_on": on["visLen"], "visLen_off": off["visLen"],
            "innerText_on": on["innerText"], "innerText_off": off["innerText"],
            "ratio": round(off["visLen"] / on["visLen"], 3) if on["visLen"] else None,
            "img_vis_on": len(on_ok), "img_vis_off": len(off_ok), "img_box_on": len(on_box),
            "hidden_len": sum(h["len"] for h in hidden), "absent_len": sum(a["len"] for a in absent),
            "hidden": sorted(hidden, key=lambda x: -x["len"])[:40], "absent": sorted(absent, key=lambda x: -x["len"])[:40],
            "img_missing": img_missing, "filled": filled, "deadCtl_off": off["deadCtl"], "forms": off["forms"],
            "noscript": off["noscript"], "mnav": r["mnav"], "bgs_on": sum(1 for x in on["bgs"] if x["vis"]),
            "bgs_off": sum(1 for x in off["bgs"] if x["vis"]), "err": [off["err"], on["err"]],
            "docH": [off["docH"], on["docH"]], "visLinks": [off["visLinks"], on["visLinks"]]}


def part_nojs(pages):
    t = time.time()
    with lib.server(PORT) as base:
        with mp.get_context("fork").Pool(WORKERS) as pool:
            raw = []
            for i, r in enumerate(pool.imap_unordered(nojs_page, [(base, p) for p in pages])):
                raw.append(r)
                if i % 20 == 0:
                    print("  nojs %d/%d %.0fs" % (i + 1, len(pages), time.time() - t), flush=True)
    summ = sorted([summarize_nojs(r) for r in raw], key=lambda s: s["path"])
    dump("nojs.json", summ)
    print("nojs done in %.0fs -> %s" % (time.time() - t, os.path.join(OUT, "nojs.json")))
    return summ


# ---------------------------------------------------------------- part 1b: forms without JS
FILL = {"email": "tester@example.com", "text": "Test value", "tel": "12345678", "number": "3", "url": "https://example.com"}


def part_forms(pages):
    pages = pages or ["enquire.html", "podcast.html", "partners.html", "index.html"]
    out = []
    with lib.server(PORT) as base:
        with lib.browser() as b:
            for path in pages:
                ctx = new_ctx(b, base, java_script_enabled=False)
                pg = ctx.new_page()
                goto(pg, base + path)
                n = pg.evaluate("document.forms.length")
                for i in range(n):
                    goto(pg, base + path)
                    info = pg.evaluate("""i => { const f = document.forms[i]; const s = f.querySelector('[type=submit],button:not([type])');
                        const r = f.getBoundingClientRect();
                        return {id: f.id, cls: f.className, action: f.getAttribute('action'), method: f.getAttribute('method'),
                                vis: r.width > 0 && r.height > 0, submit: s ? s.innerText.trim() : null,
                                note: (f.closest('section,main,div') || f).innerText.replace(/\\s+/g,' ').slice(0, 0)}; }""", i)
                    if not info["vis"] or not info["submit"]:
                        info["result"] = "not visible or no submit button"
                        out.append({"path": path, "form": info})
                        continue
                    # fill every field
                    pg.evaluate("""([i, FILL]) => { const f = document.forms[i];
                        for (const el of f.querySelectorAll('input,textarea,select')) {
                          if (el.type === 'checkbox' || el.type === 'radio') { el.checked = true; continue; }
                          if (el.tagName === 'SELECT') { if (el.options.length > 1) el.selectedIndex = 1; continue; }
                          if (el.type === 'hidden' || el.type === 'submit') continue;
                          el.value = FILL[el.type] || 'Test value';
                        } }""", [i, FILL])
                    before = pg.url
                    reqs = []
                    pg.on("request", lambda r, reqs=reqs: reqs.append((r.method, r.url[:300])) if r.resource_type == "document" else None)
                    try:
                        with pg.expect_navigation(timeout=6000):
                            pg.evaluate("i => { const f = document.forms[i]; const s = f.querySelector('[type=submit],button:not([type])'); s.click(); }", i)
                        nav = True
                    except Exception:
                        nav = False
                    time.sleep(0.3)
                    after = pg.url
                    status = pg.evaluate("() => { const s = document.querySelector('[role=status], .enq-status, [aria-live]'); return s ? s.innerText.trim() : null; }")
                    info.update({"navigated": nav, "before": before, "after": after, "doc_requests": reqs,
                                 "status_text": status, "data_in_url": ("tester%40example.com" in after) or ("Test+value" in after)})
                    out.append({"path": path, "form": info})
                ctx.close()
    dump("forms.json", out)
    for o in out:
        f = o["form"]
        print(o["path"], f.get("id") or f.get("cls"), "action=%r method=%r navigated=%s after=%s status=%r" % (
            f.get("action"), f.get("method"), f.get("navigated"), (f.get("after") or "")[:140], f.get("status_text")))
    return out


# ---------------------------------------------------------------- part 2: reduced motion
MOTION_INIT = r"""
(() => {
  window.__mo = {raf: 0, smooth: [], play: [], rafStart: 0};
  const oraf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) { window.__mo.raf++; return oraf(cb); };
  const osi = Element.prototype.scrollIntoView;
  Element.prototype.scrollIntoView = function (a) { if (a && typeof a === 'object' && a.behavior === 'smooth') window.__mo.smooth.push('scrollIntoView ' + (this.id || this.className)); return osi.apply(this, arguments); };
  for (const [obj, name] of [[window, 'scrollTo'], [window, 'scrollBy'], [Element.prototype, 'scrollTo'], [Element.prototype, 'scrollBy']]) {
    const o = obj[name];
    obj[name] = function (a) { if (a && typeof a === 'object' && a.behavior === 'smooth') window.__mo.smooth.push(name + ' ' + (this === window ? 'window' : (this.id || this.className))); return o.apply(this, arguments); };
  }
  const op = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function () { window.__mo.play.push((this.currentSrc || this.src || this.getAttribute('data-loop') || '').slice(-60)); return op.apply(this, arguments); };
})();
"""

MOTION_MEASURE = r"""
() => {
  const {P, V} = window.__dg;
  const anims = document.getAnimations().filter(a => a.playState === 'running').map(a => {
    const t = a.effect && a.effect.getComputedTiming ? a.effect.getComputedTiming() : {};
    const tgt = a.effect && a.effect.target;
    const pseudo = a.effect && a.effect.pseudoElement;
    let vis = null; if (tgt && tgt.nodeType === 1) { const r = tgt.getBoundingClientRect(); vis = V(tgt) && r.width > 0 && r.height > 0; }
    return {type: a.constructor.name, name: a.animationName || a.transitionProperty || a.id || '',
            target: tgt && tgt.nodeType === 1 ? P(tgt) + (pseudo || '') : null, visible: vis,
            iterations: t.iterations, duration: t.duration, timeline: a.timeline ? a.timeline.constructor.name : null};
  });
  const media = [...document.querySelectorAll('video,audio')].map(m => ({sel: P(m), autoplay: m.autoplay, paused: m.paused,
      t: m.currentTime, loop: m.loop, muted: m.muted, src: (m.currentSrc || '').slice(-60)}));
  const ifr = [...document.querySelectorAll('iframe')].map(f => f.src).filter(s => /autoplay=1/.test(s));
  const sb = getComputedStyle(document.documentElement).scrollBehavior;
  const sbEls = [...document.querySelectorAll('body *')].filter(e => getComputedStyle(e).scrollBehavior === 'smooth').map(P).slice(0, 10);
  let gsapActive = null;
  if (window.gsap && gsap.globalTimeline) {
    gsapActive = gsap.globalTimeline.getChildren(true, true, false).filter(t => t.isActive()).map(t => {
      const tg = t.targets ? t.targets() : []; return {dur: t.duration(), repeat: t.repeat ? t.repeat() : 0,
        target: tg[0] && tg[0].nodeType === 1 ? P(tg[0]) : String(tg[0]).slice(0, 40)}; });
  }
  return {anims, media, ifr, scrollBehavior: sb, smoothEls: sbEls, gsapActive, raf: window.__mo.raf,
          smoothCalls: window.__mo.smooth.slice(0, 20), plays: window.__mo.play.slice(0, 20)};
}
"""


def frame_diff(a_png, b_png):
    import io
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(io.BytesIO(a_png)).convert("L"), dtype=np.int16)
    b = np.asarray(Image.open(io.BytesIO(b_png)).convert("L"), dtype=np.int16)
    if a.shape != b.shape:
        return None
    d = np.abs(a - b) > 12
    if not d.any():
        return {"frac": 0.0}
    ys, xs = np.where(d)
    return {"frac": round(float(d.mean()), 4), "box": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]}


def motion_page(args):
    base, path = args
    res = {"path": path}
    with lib.browser() as b:
        for mode in ("reduce", "no-preference"):
            ctx = new_ctx(b, base, reduced_motion=mode)
            ctx.add_init_script(HELPERS)
            ctx.add_init_script(MOTION_INIT)
            pg = ctx.new_page()
            goto(pg, base + path)
            time.sleep(2.5)
            m0 = pg.evaluate(MOTION_MEASURE)
            r0 = pg.evaluate("window.__mo.raf")
            time.sleep(2.0)
            r1 = pg.evaluate("window.__mo.raf")
            # visual motion at rest: viewport shots 1s apart at 3 scroll positions
            frames = []
            h = pg.evaluate("document.documentElement.scrollHeight")
            for y in (0, max(0, h // 3), max(0, 2 * h // 3)):
                pg.evaluate("y => window.scrollTo({top: y, behavior: 'instant'})", y)
                time.sleep(1.2)
                a = pg.screenshot()
                time.sleep(1.0)
                c = pg.screenshot()
                fd = frame_diff(a, c)
                if fd and fd["frac"] > 0:
                    # which elements sit in the changing box
                    bx = fd["box"]
                    fd["under"] = pg.evaluate("""b => { const {P} = window.__dg; const s = new Set();
                        for (const [x, y] of [[(b[0]+b[2])/2, (b[1]+b[3])/2], [b[0]+2, b[1]+2], [b[2]-2, b[3]-2]]) {
                          const e = document.elementFromPoint(x, y); if (e) s.add(P(e)); } return [...s]; }""", bx)
                fd["y"] = y
                frames.append(fd)
            pg.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
            scroll_through(pg, pause=0.12)
            time.sleep(1.5)
            m1 = pg.evaluate(MOTION_MEASURE)
            # smooth scroll: in-page anchor jump and wheel
            anchor = pg.evaluate("""() => { const a = [...document.querySelectorAll('a[href^="#"]')].find(a => a.getAttribute('href').length > 1 && document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))) && a.getBoundingClientRect().width > 0);
                return a ? a.getAttribute('href') : null; }""")
            jump = None
            if anchor:
                pg.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
                time.sleep(0.3)
                pg.evaluate("h => { const a = [...document.querySelectorAll('a[href^=\"#\"]')].find(a => a.getAttribute('href') === h); a.click(); }", anchor)
                y1 = pg.evaluate("scrollY")
                time.sleep(0.05)
                y2 = pg.evaluate("scrollY")
                time.sleep(1.2)
                y3 = pg.evaluate("scrollY")
                jump = {"href": anchor, "y_immediate": y1, "y_50ms": y2, "y_1250ms": y3,
                        "animated": (y3 > 0 and abs(y3 - y2) > 5)}
            # controls on the page that scroll it for you: Kenya/India etiquette dots, episode transcript toggle
            probes = []
            for sel, clicks in ((".etq-dot", 1), (".cd-more", 2)):
                if not pg.evaluate("s => !!document.querySelector(s)", sel):
                    continue
                pg.evaluate("window.__mo.smooth.length = 0")
                target = sel + (":last-of-type" if sel == ".etq-dot" else "")
                pg.evaluate("s => { const e = document.querySelector(s); e.scrollIntoView({block: 'center', behavior: 'instant'}); }", target)
                time.sleep(0.4)
                for _ in range(clicks):
                    y0 = pg.evaluate("scrollY")
                    try:
                        pg.click(target, timeout=3000)
                    except Exception as e:
                        probes.append({"sel": target, "err": str(e)[:120]})
                        break
                    time.sleep(0.05)
                    ya = pg.evaluate("scrollY")
                    time.sleep(0.25)
                    yb = pg.evaluate("scrollY")
                    time.sleep(1.2)
                    yc = pg.evaluate("scrollY")
                    probes.append({"sel": target, "y_before": y0, "y_50ms": ya, "y_300ms": yb, "y_1500ms": yc,
                                   "animated": abs(yc - ya) > 20 and abs(yc - y0) > 20,
                                   "smooth_calls": pg.evaluate("window.__mo.smooth.slice()")})
            pg.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
            time.sleep(0.3)
            pg.mouse.move(640, 450)
            pg.mouse.wheel(0, 600)
            time.sleep(0.03)
            w1 = pg.evaluate("scrollY")
            time.sleep(0.8)
            w2 = pg.evaluate("scrollY")
            res[mode] = {"load": m0, "after_scroll": m1, "raf_per_s_at_rest": round((r1 - r0) / 2.0, 1),
                         "frames": frames, "anchor": jump, "wheel": {"y_30ms": w1, "y_830ms": w2}, "probes": probes}
            ctx.close()
    return res


def part_motion(pages):
    pages = pages or lib.TEMPLATES["live"]
    t = time.time()
    with lib.server(PORT) as base:
        with mp.get_context("fork").Pool(WORKERS) as pool:
            res = sorted(pool.map(motion_page, [(base, p) for p in pages]), key=lambda r: r["path"])
    dump("motion.json", res)
    for r in res:
        m = r["reduce"]
        run = [a for a in m["after_scroll"]["anims"] if a["visible"] is not False]
        inf = [a for a in run if a["iterations"] in (None, float("inf")) or str(a["iterations"]) == "Infinity"]
        print("%-55s raf/s=%5s anims(load)=%d anims(after)=%d infinite=%d media=%s frames=%s anchor=%s wheel=%s sb=%s" % (
            r["path"], m["raf_per_s_at_rest"], len(m["load"]["anims"]), len(run), len(inf),
            [x for x in m["load"]["media"] if not x["paused"]], [f["frac"] for f in m["frames"]],
            (m["anchor"] or {}).get("animated"), m["wheel"], m["load"]["scrollBehavior"]))
    print("motion done in %.0fs" % (time.time() - t))
    return res


# ---------------------------------------------------------------- part 3: forced colors / light scheme
COLLECT_BOXES = r"""
() => {
  const {V, P, textNodes, nodeRects} = window.__dg;
  const sx = scrollX, sy = scrollY;
  const texts = [];
  const seen = new Set();
  for (const [n, el, t] of textNodes()) {
    if (texts.length > 900) break;
    if (!V(el) || el.closest('noscript,[aria-hidden=true]')) continue;
    const rs = nodeRects(n).filter(r => r.width > 3 && r.height > 5).slice(0, 2);
    if (!rs.length) continue;
    const cs = getComputedStyle(el);
    for (const r of rs) texts.push({sel: P(el), t: t.slice(0, 50), x: r.left + sx, y: r.top + sy, w: r.width, h: r.height,
        color: cs.color, fca: cs.forcedColorAdjust, fs: parseFloat(cs.fontSize)});
  }
  const icons = [];
  const add = (el, kind) => { if (seen.has(el)) return; seen.add(el);
    const r = el.getBoundingClientRect(); if (r.width < 3 || r.height < 3 || r.width > 900 || r.height > 900) return;
    if (!V(el)) return;
    const ctl = el.closest('a,button,[role=button],label,summary');
    icons.push({sel: P(el), kind, x: r.left + sx, y: r.top + sy, w: r.width, h: r.height, ctl: ctl ? P(ctl) : null,
                label: ctl ? (ctl.getAttribute('aria-label') || ctl.innerText || '').trim().slice(0, 40) : null}); };
  document.querySelectorAll('svg').forEach(s => { if (!s.parentElement.closest('svg')) add(s, 'svg'); });
  document.querySelectorAll('img').forEach(i => { if (i.complete && i.naturalWidth) add(i, 'img'); });
  document.querySelectorAll('canvas').forEach(c => add(c, 'canvas'));
  for (const el of document.querySelectorAll('body *')) {
    if (seen.has(el) || el.closest('svg')) continue;
    if (el.textContent.trim()) continue;
    if (el.querySelector('svg,img,canvas,video')) continue;
    const cs = getComputedStyle(el);
    const bg = cs.backgroundColor, bi = cs.backgroundImage, mk = cs.maskImage || cs.webkitMaskImage;
    const hasBg = bg && !/rgba\(0, 0, 0, 0\)|transparent/.test(bg);
    const hasBi = bi && bi !== 'none';
    const hasMask = mk && mk !== 'none';
    const hasBorder = parseFloat(cs.borderTopWidth) > 0 || parseFloat(cs.borderLeftWidth) > 0;
    if (hasBg || hasBi || hasMask || hasBorder) add(el, hasMask ? 'mask' : hasBi ? (bi.indexOf('url(') >= 0 ? 'bg-url' : 'bg-gradient') : hasBg ? 'bg-color' : 'border');
  }
  return {texts, icons, H: document.documentElement.scrollHeight, W: document.documentElement.scrollWidth};
}
"""


def _lum(rgb):
    import numpy as np
    c = rgb / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def ink(img, box, pad=0):
    """95th percentile contrast ratio between pixels in box and the box's dominant colour."""
    import numpy as np
    x, y, w, h = [int(round(v)) for v in box]
    H, W = img.shape[:2]
    x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return None
    crop = img[y0:y1, x0:x1, :3].reshape(-1, 3).astype(np.float64)
    q = (crop // 16).astype(np.int32)
    code = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]
    vals, counts = np.unique(code, return_counts=True)
    dom_code = vals[counts.argmax()]
    dom = crop[code == dom_code].mean(axis=0)
    L = _lum(crop)
    Ld = float(_lum(dom[None, :])[0])
    cr = (np.maximum(L, Ld) + 0.05) / (np.minimum(L, Ld) + 0.05)
    return round(float(np.percentile(cr, 97)), 2)


COLOR_MODES = {
    "dark": dict(color_scheme="dark"), "light": dict(color_scheme="light"),
    "forced-dark": dict(color_scheme="dark", forced_colors="active"),
    "forced-light": dict(color_scheme="light", forced_colors="active"),
    "dark390": dict(color_scheme="dark", viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True),
    "forced-dark390": dict(color_scheme="dark", forced_colors="active", viewport={"width": 390, "height": 844},
                           is_mobile=True, has_touch=True),
}
COLOR_PAIRS = (("light", "dark"), ("forced-dark", "dark"), ("forced-light", "dark"), ("forced-dark390", "dark390"))


def colors_page(args):
    base, path = args
    import io
    import numpy as np
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    res = {"path": path}
    with lib.browser() as b:
        for mode, kw in COLOR_MODES.items():
            ctx = new_ctx(b, base, reduced_motion="reduce", **kw)
            ctx.add_init_script(HELPERS)
            pg = ctx.new_page()
            goto(pg, base + path)
            time.sleep(0.8)
            scroll_through(pg, pause=0.08)
            time.sleep(0.8)
            boxes = pg.evaluate(COLLECT_BOXES)
            W = pg.viewport_size["width"]
            H = min(boxes["H"], 14000)
            png = pg.screenshot(full_page=True, clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            img = np.asarray(im)
            im.resize((W // 2, max(1, H // 2))).save(os.path.join(OUT, "shots", path.replace("/", "__") + "." + mode + ".png"))
            for t in boxes["texts"]:
                t["ink"] = ink(img, (t["x"], t["y"], t["w"], t["h"])) if t["y"] + t["h"] < H else None
            for i in boxes["icons"]:
                i["ink"] = ink(img, (i["x"], i["y"], i["w"], i["h"]), pad=2) if i["y"] + i["h"] < H else None
            res[mode] = boxes
            ctx.close()
    return res


def summarize_colors(r):
    out = {"path": r["path"]}
    for mode, basemode in COLOR_PAIRS:
        base = r[basemode]
        bt = {}
        for t in base["texts"]:
            bt.setdefault((t["sel"], t["t"]), []).append(t)
        bi = {}
        for i in base["icons"]:
            bi.setdefault((i["sel"], round(i["x"]), round(i["w"])), []).append(i)
        m = r[mode]
        lost_text, low_text, lost_icons = [], [], []
        for t in m["texts"]:
            if t["ink"] is None:
                continue
            b0 = bt.get((t["sel"], t["t"]))
            b_ink = b0[0]["ink"] if b0 else None
            if t["ink"] < 1.35:
                (lost_text if (b_ink or 0) >= 2.0 else low_text).append(
                    {"sel": t["sel"], "text": t["t"], "ink": t["ink"], "base_ink": b_ink, "color": t["color"],
                     "fca": t["fca"], "xywh": [round(t["x"]), round(t["y"]), round(t["w"]), round(t["h"])]})
        for i in m["icons"]:
            if i["ink"] is None:
                continue
            b0 = bi.get((i["sel"], round(i["x"]), round(i["w"])))
            b_ink = b0[0]["ink"] if b0 else None
            if b_ink and b_ink >= 1.8 and i["ink"] < 1.2:
                lost_icons.append({"sel": i["sel"], "kind": i["kind"], "ink": i["ink"], "base_ink": b_ink, "ctl": i["ctl"],
                                   "label": i["label"], "xywh": [round(i["x"]), round(i["y"]), round(i["w"]), round(i["h"])]})
        out[mode] = {"texts": len(m["texts"]), "icons": len(m["icons"]), "lost_text": lost_text, "low_text_both": low_text,
                     "lost_icons": lost_icons}
    out["dark_low_text"] = [{"sel": t["sel"], "text": t["t"], "ink": t["ink"]} for t in r["dark"]["texts"]
                            if t["ink"] is not None and t["ink"] < 1.35]
    return out


def part_colors(pages):
    pages = pages or lib.TEMPLATES["live"]
    os.makedirs(os.path.join(OUT, "shots"), exist_ok=True)
    t = time.time()
    with lib.server(PORT) as base:
        with mp.get_context("fork").Pool(WORKERS) as pool:
            raw = pool.map(colors_page, [(base, p) for p in pages])
    dump("colors_raw.json", raw)
    summ = sorted([summarize_colors(r) for r in raw], key=lambda s: s["path"])
    dump("colors.json", summ)
    for s in summ:
        print("%-55s " % s["path"] + " | ".join("%s: lostT=%d lowT=%d lostI=%d" % (
            m, len(s[m]["lost_text"]), len(s[m]["low_text_both"]), len(s[m]["lost_icons"]))
            for m, _ in COLOR_PAIRS) + " darkLow=%d" % len(s["dark_low_text"]))
    print("colors done in %.0fs" % (time.time() - t))
    return summ


# ---------------------------------------------------------------- part 4: print
PRINT_MEASURE = r"""
(pw) => {
  const {V, P, textNodes, nodeRect} = window.__dg;
  const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && V(e); };
  const navs = [...document.querySelectorAll('nav, header, [role=navigation], .nav-links, .nav-toggle')].filter(vis).map(P);
  const fixed = [...document.querySelectorAll('body *')].filter(e => { const p = getComputedStyle(e).position; return (p === 'fixed' || p === 'sticky') && vis(e); })
      .map(e => { const r = e.getBoundingClientRect(); return {sel: P(e), pos: getComputedStyle(e).position, w: Math.round(r.width), h: Math.round(r.height),
                  txt: (e.innerText || '').trim().slice(0, 40)}; });
  const modals = [...document.querySelectorAll('dialog, [role=dialog], [aria-modal=true], .modal, [class*=modal], [class*=cookie], [class*=overlay]')].filter(vis).map(P);
  let white = 0, total = 0; const whiteSamples = [];
  let over = [];
  for (const [n, el, t] of textNodes()) {
    if (!V(el)) continue;
    const r = nodeRect(n); if (r.width <= 0 || r.height <= 0) continue;
    total += t.length;
    const c = getComputedStyle(el).color.match(/[\d.]+/g).map(Number);
    const lin = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    const L = 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
    const a = c.length > 3 ? c[3] : 1;
    const cr = 1.05 / (L + 0.05);
    if (cr < 1.6 || a < 0.15) { white += t.length; if (whiteSamples.length < 6) whiteSamples.push({sel: P(el), t: t.slice(0, 40), color: getComputedStyle(el).color}); }
    if (r.right > pw + 2 && r.left < pw + 2 || r.left < -2) { if (over.length < 12) over.push({sel: P(el), t: t.slice(0, 40), left: Math.round(r.left), right: Math.round(r.right)}); }
  }
  const hiddenOpacity = [...document.querySelectorAll('body *')].filter(e => { const s = e.getAttribute('style') || ''; return /opacity:\s*0(\D|$)/.test(s) && e.textContent.trim().length > 20; }).map(P).slice(0, 12);
  return {navs, fixed: fixed.slice(0, 20), modals, lightTextChars: white, textChars: total, lightSamples: whiteSamples,
          overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth, cutText: over, inlineOpacity0: hiddenOpacity};
}
"""


def pdf_stats(pdf_bytes):
    import numpy as np
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf_bytes)
    pages = []
    for i in range(len(doc)):
        p = doc[i]
        tp = p.get_textpage()
        txt = tp.get_text_range() or ""
        chars = len("".join(txt.split()))
        bm = p.render(scale=60 / 72).to_numpy()  # ~60 dpi
        a = bm[..., :3].astype(np.float64)
        L = _lum(a)
        cr = 1.05 / (L + 0.05)                 # contrast of each pixel against white paper
        nonwhite = float((cr >= 1.1).mean())
        ink15 = float((cr >= 1.5).mean())
        ink3 = float((cr >= 3.0).mean())
        pages.append({"chars": chars, "ink": round(nonwhite, 4), "ink15": round(ink15, 5), "dark": round(ink3, 5),
                      "text": " ".join(txt.split())[:400]})
    return pages


def print_page(args):
    base, path = args
    res = {"path": path}
    with lib.browser() as b:
        for variant in ("noscroll", "scrolled"):
            ctx = new_ctx(b, base, viewport={"width": 1280, "height": 900})
            ctx.add_init_script(HELPERS)
            pg = ctx.new_page()
            goto(pg, base + path)
            time.sleep(1.0)
            if variant == "scrolled":
                scroll_through(pg, pause=0.12)
                time.sleep(1.2)
            pdf = pg.pdf(format="A4", margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"})
            pdf_bg = pg.pdf(format="A4", print_background=True,
                            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}) if variant == "scrolled" else None
            with open(os.path.join(OUT, "pdf", path.replace("/", "__") + "." + variant + ".pdf"), "wb") as f:
                f.write(pdf)
            st = pdf_stats(pdf)
            v = {"pages": len(st), "per_page": st, "chars": sum(p["chars"] for p in st),
                 "empty_pages": [i + 1 for i, p in enumerate(st) if p["chars"] < 5 and p["ink"] < 0.01],
                 "textless_inked_pages": [i + 1 for i, p in enumerate(st) if p["chars"] < 5 and p["ink"] >= 0.01],
                 "invisible_text_pages": [i + 1 for i, p in enumerate(st) if p["chars"] >= 150 and p["dark"] < 0.001],
                 "ink3_total": round(sum(p["dark"] for p in st) / max(1, len(st)), 5)}
            if pdf_bg:
                sb = pdf_stats(pdf_bg)
                v["bg_pages"] = len(sb)
                v["bg_chars"] = sum(p["chars"] for p in sb)
            if variant == "scrolled":
                # layout under print media at the printable width (A4 190mm = 718px)
                pg.emulate_media(media="print")
                pg.set_viewport_size({"width": 718, "height": 1043})
                time.sleep(0.4)
                v["layout"] = pg.evaluate(PRINT_MEASURE, 718)
            res[variant] = v
            ctx.close()
    return res


def part_print(pages):
    pages = pages or lib.TEMPLATES["live"]
    os.makedirs(os.path.join(OUT, "pdf"), exist_ok=True)
    t = time.time()
    with lib.server(PORT) as base:
        with mp.get_context("fork").Pool(WORKERS) as pool:
            res = sorted(pool.map(print_page, [(base, p) for p in pages]), key=lambda r: r["path"])
    dump(os.environ.get("PRINT_OUT", "print.json"), res)
    for r in res:
        s, n = r["scrolled"], r["noscroll"]
        L = s["layout"]
        print("%-55s pages=%d(bg %s) chars=%d/noscroll %d  empty=%s textless=%s invisibleText=%s light=%d/%d nav=%d fixed=%d modals=%d ovX=%d cut=%d op0=%d" % (
            r["path"], s["pages"], s.get("bg_pages"), s["chars"], n["chars"], s["empty_pages"], s["textless_inked_pages"],
            len(s["invisible_text_pages"]), L["lightTextChars"], L["textChars"], len(L["navs"]), len(L["fixed"]),
            len(L["modals"]), L["overflowX"], len(L["cutText"]), len(L["inlineOpacity0"])))
    print("print done in %.0fs" % (time.time() - t))
    return res


# ---------------------------------------------------------------- part 5: text spacing
SPACING_CSS = """*,*::before,*::after{line-height:1.5 !important;letter-spacing:.12em !important;word-spacing:.16em !important;}
p{margin-bottom:2em !important;}"""

SPACING_MEASURE = r"""
() => {
  const {V, P, textNodes, nodeRects} = window.__dg;
  const sx = scrollX, sy = scrollY;
  const items = [];   // text line rects
  const clips = [];
  const clipSeen = new Set();
  const els = new Map();
  for (const [n, el, t] of textNodes()) {
    if (!V(el) || el.closest('noscript')) continue;
    const rs = nodeRects(n).filter(r => r.width > 1 && r.height > 1);
    if (!rs.length) continue;
    const id = els.has(el) ? els.get(el) : (els.set(el, els.size), els.size - 1);
    for (const r of rs) items.push({id, x0: r.left + sx, y0: r.top + sy, x1: r.right + sx, y1: r.bottom + sy});
    // clipping by an overflow:hidden/clip ancestor or by own truncation
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const cs = getComputedStyle(e);
      const hid = v => v === 'hidden' || v === 'clip';
      if (!hid(cs.overflowX) && !hid(cs.overflowY)) { if (cs.position === 'fixed') break; continue; }
      const a = e.getBoundingClientRect();
      if (a.width < 4 || a.height < 4) break;  // sr-only style boxes
      let cut = 0;
      for (const r of rs) {
        if (hid(cs.overflowY) && (r.bottom > a.bottom + 1.5 || r.top < a.top - 1.5)) cut = Math.max(cut, Math.round(Math.max(r.bottom - a.bottom, a.top - r.top)));
        if (hid(cs.overflowX) && (r.right > a.right + 1.5 || r.left < a.left - 1.5)) cut = Math.max(cut, Math.round(Math.max(r.right - a.right, a.left - r.left)));
      }
      if (cut > 2) {
        const k = P(e) + '|' + P(el);
        if (!clipSeen.has(k)) { clipSeen.add(k); clips.push({box: P(e), el: P(el), t: t.slice(0, 50), cut,
          ellipsis: cs.textOverflow === 'ellipsis' || cs.webkitLineClamp !== 'none', h: Math.round(a.height), w: Math.round(a.width)}); }
      }
      break;
    }
  }
  // truncation by text-overflow / line-clamp on the element itself
  const trunc = [];
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.webkitLineClamp !== 'none' || cs.textOverflow === 'ellipsis') {
      if (!V(el)) continue;
      if (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1)
        trunc.push({sel: P(el), t: (el.innerText || el.textContent || '').trim().slice(0, 50), sh: el.scrollHeight, ch: el.clientHeight, sw: el.scrollWidth, cw: el.clientWidth});
    }
  }
  const list = [...els.keys()];
  // overlaps between line boxes of different, unrelated text elements
  const B = 60, buckets = new Map();
  items.forEach((r, i) => { for (let b = Math.floor(r.y0 / B); b <= Math.floor(r.y1 / B); b++) { if (!buckets.has(b)) buckets.set(b, []); buckets.get(b).push(i); } });
  const pairs = new Map();
  for (const idx of buckets.values()) {
    for (let a = 0; a < idx.length; a++) for (let c = a + 1; c < idx.length; c++) {
      const r = items[idx[a]], s = items[idx[c]];
      if (r.id === s.id) continue;
      const w = Math.min(r.x1, s.x1) - Math.max(r.x0, s.x0), h = Math.min(r.y1, s.y1) - Math.max(r.y0, s.y0);
      if (w <= 2 || h <= 2) continue;
      const ar = Math.min((r.x1 - r.x0) * (r.y1 - r.y0), (s.x1 - s.x0) * (s.y1 - s.y0));
      if (w * h < 0.25 * ar) continue;
      const e1 = list[r.id], e2 = list[s.id];
      if (e1.contains(e2) || e2.contains(e1)) continue;
      const k = r.id < s.id ? r.id + ':' + s.id : s.id + ':' + r.id;
      if (!pairs.has(k)) pairs.set(k, {a: P(e1), b: P(e2), ta: (e1.innerText || e1.textContent || '').trim().slice(0, 40), tb: (e2.innerText || e2.textContent || '').trim().slice(0, 40),
          at: [Math.round(Math.max(r.x0, s.x0)), Math.round(Math.max(r.y0, s.y0))], area: Math.round(w * h),
          dec: !!(e1.closest('[aria-hidden=true]') || e2.closest('[aria-hidden=true]'))});
    }
  }
  return {clips, trunc: trunc.slice(0, 40), overlaps: [...pairs.values()].slice(0, 200), lines: items.length,
          overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth};
}
"""


def spacing_page(args):
    base, path = args
    res = {"path": path}
    with lib.browser() as b:
        for vp in ((1280, 900), (390, 844)):
            ctx = new_ctx(b, base, reduced_motion="reduce", viewport={"width": vp[0], "height": vp[1]},
                          is_mobile=vp[0] < 500, has_touch=vp[0] < 500)
            ctx.add_init_script(HELPERS)
            pg = ctx.new_page()
            goto(pg, base + path)
            time.sleep(0.8)
            scroll_through(pg, pause=0.08)
            time.sleep(0.5)
            b0 = pg.evaluate(SPACING_MEASURE)
            pg.add_style_tag(content=SPACING_CSS)
            time.sleep(0.8)
            scroll_through(pg, pause=0.05)
            time.sleep(0.4)
            b1 = pg.evaluate(SPACING_MEASURE)
            if vp[0] < 500:
                shot = os.path.join(OUT, "shots", path.replace("/", "__") + ".spacing390.png")
            else:
                shot = os.path.join(OUT, "shots", path.replace("/", "__") + ".spacing1280.png")
            try:
                pg.screenshot(path=shot, full_page=True, clip={"x": 0, "y": 0, "width": vp[0], "height": 8000})
            except Exception:
                pass
            clip0 = {(c["box"], c["el"]) for c in b0["clips"]}
            ov0 = {(o["a"], o["b"]) for o in b0["overlaps"]} | {(o["b"], o["a"]) for o in b0["overlaps"]}
            tr0 = {t["sel"] for t in b0["trunc"]}
            res["%d" % vp[0]] = {
                "new_clips": [c for c in b1["clips"] if (c["box"], c["el"]) not in clip0],
                "base_clips": len(b0["clips"]),
                "new_overlaps": [o for o in b1["overlaps"] if (o["a"], o["b"]) not in ov0],
                "base_overlaps": len(b0["overlaps"]),
                "new_trunc": [t for t in b1["trunc"] if t["sel"] not in tr0],
                "overflowX": [b0["overflowX"], b1["overflowX"]]}
            ctx.close()
    return res


def part_spacing(pages):
    pages = pages or lib.TEMPLATES["live"]
    os.makedirs(os.path.join(OUT, "shots"), exist_ok=True)
    t = time.time()
    with lib.server(PORT) as base:
        with mp.get_context("fork").Pool(WORKERS) as pool:
            res = sorted(pool.map(spacing_page, [(base, p) for p in pages]), key=lambda r: r["path"])
    dump("spacing.json", res)
    for r in res:
        print("%-55s " % r["path"] + " | ".join("%s: clips=%d overlaps=%d trunc=%d ovX=%s" % (
            k, len(r[k]["new_clips"]), len(r[k]["new_overlaps"]), len(r[k]["new_trunc"]), r[k]["overflowX"]) for k in ("1280", "390")))
    print("spacing done in %.0fs" % (time.time() - t))
    return res


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    pages = sys.argv[2:]
    if part in ("nojs", "all"):
        part_nojs(pages or lib.pages("live"))
    if part in ("forms", "all"):
        part_forms(pages if part == "forms" else [])
    if part in ("motion", "all"):
        part_motion(pages)
    if part in ("colors", "all"):
        part_colors(pages)
    if part in ("print", "all"):
        part_print(pages)
    if part in ("spacing", "all"):
        part_spacing(pages)
