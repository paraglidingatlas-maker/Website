"""Hostile-input and security-surface checks on the LIVE site (repo root), served locally.

python3 dynamic.py [check ...] [--pages N] [--only KEY-SUBSTRING]   (--only filters the 'special' cases, e.g. --only "index#pin")
checks: sweep special postmessage mailto stubs feeds long   (default: all)
  sweep       every live page: baseline load (DOM/network surface) + hostile load
              (payload in 16 query params, #hash, window.name, referrer); detects
              execution (window.__xss), payload reaching an HTML/URL/code sink, and
              page errors that only happen under the hostile URL.
  special     targeted malformed/prototype-key inputs: index.html#pin=%,
              library.html#%, library.html#s=constructor|__proto__|toString,
              knowledge-base.html?m=constructor|__proto__|valueOf, enquire.html?trip=<payload>
  postmessage episode pages: hostile messages from a mocked YouTube frame and from a
              cross-origin opener window
  mailto      enquire / partners / podcast question forms with header-injection input
  stubs       redirect stubs with open-redirect style params
  feeds       podcast/library pages with a hostile RSS / YouTube feed served by the
              (mocked) Cloudflare worker
  long        15 template pages with a 32 KB query + hash
Port 8817 only. Writes results to ./dynamic_<check>.json
"""
import json, os, sys, time, re
from urllib.parse import quote, urlparse, parse_qs, unquote
sys.path.insert(0, "/home/user/Website/tools/stress")
import lib

PORT = 8817
OUT = os.path.dirname(os.path.abspath(__file__))
MARK = "PGAX"
P_HTML = MARK + "\"'><img src=x onerror=\"window.__xss=(window.__xss||[]).concat(location.pathname+'|html')\">"
P_SVG = MARK + "<svg onload=\"window.__xss=(window.__xss||[]).concat(location.pathname+'|svg')\">"
P_JS = "javascript:window.__xss=(window.__xss||[]).concat(location.pathname+'|jsurl')//" + MARK
PARAMS = ["q", "trip", "m", "s", "pin", "url", "next", "redirect", "ref", "utm_source", "id", "search",
          "query", "name", "email", "subject"]

INIT = r"""
(() => {
  const M = '%s';
  window.__sinks = []; window.__msgL = []; window.__nav = [];
  const rec = (sink, v) => { try { const s = String(v); if (s.indexOf(M) !== -1)
      window.__sinks.push({sink: sink, v: s.slice(0, 240), at: (new Error().stack || '').split('\n').slice(2, 4).join(' | ').slice(0, 300)}); } catch (e) {} };
  const hookProp = (C, p, label) => { const d = Object.getOwnPropertyDescriptor(C.prototype, p); if (!d || !d.set) return;
    Object.defineProperty(C.prototype, p, {configurable: true, enumerable: d.enumerable,
      get() { return d.get.call(this); }, set(v) { rec(label, v); return d.set.call(this, v); }}); };
  hookProp(Element, 'innerHTML', 'innerHTML'); hookProp(Element, 'outerHTML', 'outerHTML');
  hookProp(HTMLAnchorElement, 'href', 'a.href'); hookProp(HTMLIFrameElement, 'src', 'iframe.src');
  hookProp(HTMLIFrameElement, 'srcdoc', 'iframe.srcdoc'); hookProp(HTMLScriptElement, 'src', 'script.src');
  hookProp(HTMLImageElement, 'src', 'img.src'); hookProp(HTMLMediaElement, 'src', 'media.src');
  hookProp(HTMLFormElement, 'action', 'form.action');
  const iah = Element.prototype.insertAdjacentHTML;
  Element.prototype.insertAdjacentHTML = function (p, v) { rec('insertAdjacentHTML', v); return iah.call(this, p, v); };
  const sa = Element.prototype.setAttribute;
  Element.prototype.setAttribute = function (n, v) { if (/^(href|src|srcdoc|action|formaction|on.*)$/i.test(n)) rec('setAttribute:' + n, v); return sa.call(this, n, v); };
  const dw = document.write; document.write = function () { rec('document.write', [].join.call(arguments, '')); return dw.apply(document, arguments); };
  const ev = window.eval; window.eval = function (s) { rec('eval', s); return ev(s); };
  const st = window.setTimeout; window.setTimeout = function (f) { if (typeof f === 'string') rec('setTimeout(str)', f); return st.apply(this, arguments); };
  const si = window.setInterval; window.setInterval = function (f) { if (typeof f === 'string') rec('setInterval(str)', f); return si.apply(this, arguments); };
  const ccf = Range.prototype.createContextualFragment; Range.prototype.createContextualFragment = function (s) { rec('createContextualFragment', s); return ccf.call(this, s); };
  const pfs = DOMParser.prototype.parseFromString; DOMParser.prototype.parseFromString = function (s, t) { if (t === 'text/html') rec('DOMParser(html)', s); return pfs.call(this, s, t); };
  const wo = window.open; window.open = function (u) { rec('window.open', u); window.__nav.push('open:' + u); return wo.apply(window, arguments); };
  const ael = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function (t, f, o) { if (t === 'message' && this === window) window.__msgL.push(String(f).slice(0, 120)); return ael.call(this, t, f, o); };
})();
""" % MARK

SET_NAME = "if (!window.name) window.name = %s;" % json.dumps(P_HTML)


def stubs():
    import glob
    out = []
    for fp in glob.glob(os.path.join(lib.ROOT, "**", "index.html"), recursive=True):
        rel = os.path.relpath(fp, lib.ROOT)
        if rel.startswith(("prototypes", "node_modules", "docs", "templates", "tools")):
            continue
        html = open(fp, encoding="utf-8").read()
        if 'http-equiv="refresh"' in html:
            out.append(rel)
    return sorted(out)


def hostile_url(base, path):
    qs = "&".join("%s=%s" % (k, quote(P_HTML if i % 3 == 0 else P_SVG if i % 3 == 1 else P_JS, safe=""))
                  for i, k in enumerate(PARAMS))
    return base + path + "?" + qs + "#" + quote(P_HTML, safe="")


def new_ctx(b, base, log, mock=None, **kw):
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, **kw)
    ctx.add_init_script(INIT)

    def route(r):
        u = r.request.url
        if mock:
            for pat, body in mock.items():
                if pat in u:
                    log.setdefault("mocked", []).append(u)
                    if callable(body):
                        return body(r)
                    ct = "application/xml" if body.lstrip().startswith("<") else "application/json"
                    return r.fulfill(status=200, body=body, headers={"Content-Type": ct, "Access-Control-Allow-Origin": "*"})
        if u.startswith(base) or u.startswith("data:") or u.startswith("blob:"):
            return r.continue_()
        log.setdefault("external", []).append(u)
        return r.abort()
    ctx.route("**/*", route)
    return ctx


def snap_dom(pg):
    return pg.evaluate(r"""() => {
      const blank = [...document.querySelectorAll('a[target=_blank]')].filter(a => {
        const r = (a.getAttribute('rel') || '').toLowerCase().split(/\s+/); return !r.includes('noopener') && !r.includes('noreferrer'); })
        .map(a => a.outerHTML.slice(0, 160));
      const jsu = [...document.querySelectorAll('a[href],area[href],iframe[src],form[action]')]
        .map(e => e.getAttribute('href') || e.getAttribute('src') || e.getAttribute('action'))
        .filter(h => /^\s*(javascript|data|vbscript):/i.test(h || ''));
      const ifr = [...document.querySelectorAll('iframe')].map(f => ({src: f.getAttribute('src'), sandbox: f.getAttribute('sandbox'),
        loading: f.getAttribute('loading'), allow: f.getAttribute('allow'), referrerpolicy: f.getAttribute('referrerpolicy')}));
      const forms = [...document.querySelectorAll('form')].map(f => ({id: f.id, cls: f.className, action: f.getAttribute('action'), method: f.getAttribute('method')}));
      const csp = [...document.querySelectorAll('meta[http-equiv]')].filter(m => /content-security-policy/i.test(m.httpEquiv)).map(m => m.content);
      const refpol = [...document.querySelectorAll('meta[name=referrer]')].map(m => m.content);
      return {blank, jsu, ifr, forms, csp, refpol, msgL: window.__msgL.length, msgSrc: window.__msgL};
    }""")


def check_sweep(b, base, pages):
    res = {"pages": {}, "summary": {}}
    hosts = {}
    httpreq = []
    t0 = time.time()
    for i, p in enumerate(pages):
        rec = {}
        # baseline
        log = {}
        ctx = new_ctx(b, base, log)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e, errs=errs: errs.append(str(e)[:200]))
        try:
            pg.goto(base + p, wait_until="load", timeout=20000)
        except Exception as e:
            rec["base_goto"] = str(e)[:120]
        pg.wait_for_timeout(500)
        try:
            pg.mouse.wheel(0, 2500); pg.wait_for_timeout(250)
            rec["dom"] = snap_dom(pg)
        except Exception as e:
            rec["dom_err"] = str(e)[:150]
        rec["base_errors"] = errs
        for u in log.get("external", []):
            h = urlparse(u).netloc
            hosts.setdefault(h, set()).add(p)
            if u.startswith("http:"):
                httpreq.append((p, u))
        ctx.close()
        # hostile
        log = {}
        ctx = new_ctx(b, base, log)
        ctx.add_init_script(SET_NAME)
        pg = ctx.new_page()
        errs2 = []
        pg.on("pageerror", lambda e, errs2=errs2: errs2.append(str(e)[:200]))
        try:
            pg.goto(hostile_url(base, p), wait_until="load", timeout=20000,
                    referer="http://evil.example/?r=" + quote(P_HTML, safe=""))
        except Exception as e:
            rec["host_goto"] = str(e)[:120]
        pg.wait_for_timeout(600)
        try:
            pg.mouse.wheel(0, 2500); pg.wait_for_timeout(200)
            r = pg.evaluate("() => ({xss: window.__xss || null, sinks: window.__sinks, url: location.href.slice(0, 80), injected: document.querySelectorAll('img[src=x],svg[onload]').length})")
        except Exception as e:
            r = {"eval_err": str(e)[:150]}
        rec["hostile"] = r
        rec["hostile_errors"] = errs2
        rec["new_errors"] = [e for e in errs2 if e not in errs]
        ctx.close()
        res["pages"][p] = rec
        if (i + 1) % 20 == 0:
            print("  sweep %d/%d %.0fs" % (i + 1, len(pages), time.time() - t0), flush=True)
    pp = res["pages"]
    res["summary"] = {
        "pages": len(pp),
        "executed": {p: v["hostile"].get("xss") for p, v in pp.items() if v["hostile"].get("xss")},
        "injected_nodes": {p: v["hostile"].get("injected") for p, v in pp.items() if v["hostile"].get("injected")},
        "payload_reached_sink": {p: v["hostile"].get("sinks") for p, v in pp.items() if v["hostile"].get("sinks")},
        "new_errors_under_hostile_url": {p: v["new_errors"] for p, v in pp.items() if v["new_errors"]},
        "baseline_errors": {p: v["base_errors"] for p, v in pp.items() if v["base_errors"]},
        "blank_without_noopener": {p: v["dom"]["blank"] for p, v in pp.items() if v.get("dom", {}).get("blank")},
        "js_or_data_urls": {p: v["dom"]["jsu"] for p, v in pp.items() if v.get("dom", {}).get("jsu")},
        "message_listeners": {p: v["dom"]["msgL"] for p, v in pp.items() if v.get("dom", {}).get("msgL")},
        "forms": {p: v["dom"]["forms"] for p, v in pp.items() if v.get("dom", {}).get("forms")},
        "csp_meta": sum(1 for v in pp.values() if v.get("dom", {}).get("csp")),
        "referrer_meta": sum(1 for v in pp.values() if v.get("dom", {}).get("refpol")),
        "iframes_total": sum(len(v.get("dom", {}).get("ifr", [])) for v in pp.values()),
        "iframes_sandboxed": sum(1 for v in pp.values() for f in v.get("dom", {}).get("ifr", []) if f.get("sandbox") is not None),
        "iframes_lazy": sum(1 for v in pp.values() for f in v.get("dom", {}).get("ifr", []) if f.get("loading") == "lazy"),
        "iframe_hosts": sorted({urlparse(f.get("src") or "").netloc for v in pp.values() for f in v.get("dom", {}).get("ifr", [])}),
        "third_party_request_hosts": {h: len(v) for h, v in hosts.items()},
        "insecure_http_requests": httpreq[:50],
        "secs": round(time.time() - t0),
    }
    return res


TINY_LAND = json.dumps({"type": "Topology", "objects": {"land": {"type": "GeometryCollection", "geometries": [
    {"type": "Polygon", "arcs": [[0]]}]}}, "arcs": [[[-10, 40], [40, 40], [40, 70], [-10, 70], [-10, 40]]]})


def check_special(b, base):
    out = {}

    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None

    def out_run(key, *a, **kw):
        if only and only not in key:
            return
        out[key] = run(*a, **kw)

    def run(path, mock=None, steps=None, wait=1500, ctxkw=None, shot=None):
        log = {}
        ctx = new_ctx(b, base, log, mock=mock, **(ctxkw or {}))
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.goto(base + path, wait_until="load", timeout=20000)
        pg.wait_for_timeout(wait)
        r = steps(pg) if steps else {}
        r["errors"] = errs
        r["xss"] = pg.evaluate("window.__xss || null")
        r["feed_or_land_requests"] = [u.split("?")[0][:60] for u in log.get("mocked", [])]
        if shot:
            pg.evaluate("document.getElementById('epMap') && document.getElementById('epMap').scrollIntoView({block:'center'})")
            pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(OUT, shot))
            r["screenshot"] = os.path.join(OUT, shot)
        ctx.close()
        return r

    land = {"unpkg.com/world-atlas": TINY_LAND}

    def globe_probe(pg):
        st = pg.evaluate("""() => { const m = document.getElementById('epMap'); const land = m && m.querySelectorAll('path');
          const ds = land ? [...land].map(p => (p.getAttribute('d') || '').length) : [];
          return {svg: !!(m && m.querySelector('svg')), paths: ds.length, longest_path_d: Math.max(0, ...ds),
                  pins: m ? m.querySelectorAll('circle').length : 0,
                  popup: (() => { const p = document.getElementById('mapPopup'); if (!p) return null; const cs = getComputedStyle(p);
                     return {display: cs.display, opacity: cs.opacity, cls: p.className, title: (p.querySelector('.popup-title')||{}).textContent}; })(),
                  globe_snapshot: m ? m.innerHTML.length : 0}; }""")
        # drag the globe: does the drawing change?
        box = pg.evaluate("(() => { const r = document.getElementById('epMap').getBoundingClientRect(); return [r.x, r.y, r.width, r.height]; })()")
        pg.evaluate("document.getElementById('epMap').scrollIntoView({block:'center'})")
        pg.wait_for_timeout(300)
        box = pg.evaluate("(() => { const r = document.getElementById('epMap').getBoundingClientRect(); return [r.x, r.y, r.width, r.height]; })()")
        before = pg.evaluate("[...document.querySelectorAll('#epMap path')].map(p => p.getAttribute('d')).join('|')")
        cx, cy = box[0] + box[2] / 2, box[1] + box[3] / 2
        pg.mouse.move(cx, cy); pg.mouse.down(); pg.mouse.move(cx + 160, cy + 20, steps=8); pg.mouse.up()
        pg.wait_for_timeout(300)
        after = pg.evaluate("[...document.querySelectorAll('#epMap path')].map(p => p.getAttribute('d')).join('|')")
        st["drag_changes_globe"] = before != after
        # a valid pin link followed afterwards (hashchange)
        pg.evaluate("location.hash = '#pin=sky-gods-flying-8000ers-antoine-girard'")
        pg.wait_for_timeout(2600)
        st["popup_after_valid_hashchange"] = pg.evaluate("""() => { const p = document.getElementById('mapPopup'); const cs = getComputedStyle(p);
             return {display: cs.display, opacity: cs.opacity, cls: p.className, title: (p.querySelector('.popup-title')||{}).textContent}; }""")
        return st

    out_run("index#pin=valid", "index.html#pin=sky-gods-flying-8000ers-antoine-girard", land, globe_probe, 3000)
    out_run("index#none(shot)", "index.html", land, None, 2500, shot="globe_baseline.png")
    out_run("index#pin=%(shot)", "index.html#pin=%", land, None, 2500, shot="globe_pin_percent.png")
    out_run("index#none", "index.html", land, globe_probe, 2000)
    out_run("index#pin=%", "index.html#pin=%", land, globe_probe, 2000)
    out_run("index#pin=%E0%A4%A", "index.html#pin=%E0%A4%A", land, globe_probe, 2000)
    out_run("index#pin=<payload>", "index.html#pin=" + quote(P_HTML, safe=""), land, globe_probe, 2000)

    rss = """<?xml version="1.0"?><rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"><channel>""" + "".join(
        "<item><title>Ep %d</title><itunes:duration>00:%02d:00</itunes:duration></item>" % (i, 10 + i) for i in range(15)) + "</channel></rss>"
    worker = {"aninder.workers.dev": rss}

    def lib_probe(pg):
        r = pg.evaluate("""() => ({tiles: document.querySelectorAll('#feat .tile, #rest .tile').length,
             landing_hidden: document.getElementById('landing').classList.contains('lib-hidden'),
             rT: document.getElementById('rT').textContent, rS: document.getElementById('rS').textContent,
             eps: document.querySelectorAll('#eps .ep-tile').length, cnt: document.getElementById('cnt').textContent})""")
        pg.evaluate("location.hash = 'all'"); pg.wait_for_timeout(500)
        r["after_#all"] = pg.evaluate("""() => ({eps: document.querySelectorAll('#eps .ep-tile').length,
             length_filter_pills: document.querySelectorAll('#bar .pill[data-k=l]').length,
             sort_pills: document.querySelectorAll('#bar .pill[data-k=s]').length})""")
        return r
    out_run("library#none", "library.html", worker, lib_probe)
    out_run("library#%", "library.html#%", worker, lib_probe)
    out_run("library#s=%E0%A4%A", "library.html#s=%E0%A4%A", worker, lib_probe)
    for k in ["constructor", "__proto__", "toString", "hasOwnProperty"]:
        out_run("library#s=" + k, "library.html#s=" + k, worker, lib_probe)
    out_run("library#s=<payload>", "library.html#s=" + quote(P_HTML, safe=""), worker, lib_probe)

    def kb_probe(pg):
        def st():
            return pg.evaluate("""() => { const i = document.getElementById('iris'); const cv = document.getElementById('irisCv');
              let lit = null; try { const c = cv.getContext('2d'); const d = c.getImageData(0, 0, cv.width, cv.height).data; let n = 0;
                for (let k = 3; k < d.length; k += 16) if (d[k] > 0) n++; lit = n; } catch (e) { lit = 'err:' + e.message; }
              return {iris_present: !!i, iris_on: document.documentElement.classList.contains('iris-on'), canvas_lit_samples: lit}; }""")
        a = st()
        # visitor tries to get through: click the core
        try:
            pg.click("#irisCore", timeout=2000)
        except Exception as e:
            a["click_err"] = str(e)[:100]
        pg.wait_for_timeout(1800)
        a["after_click"] = st()
        return a
    out_run("kb?m=sphere", "knowledge-base.html?m=sphere", None, kb_probe, 1500)
    for k in ["constructor", "__proto__", "valueOf"]:
        out_run("kb?m=" + k, "knowledge-base.html?m=" + k, None, kb_probe, 1500)

    def enq_probe(pg):
        return pg.evaluate("() => ({trip: document.getElementById('trip').value, idx: document.getElementById('trip').selectedIndex})")
    out_run("enquire?trip=kenya", "enquire.html?trip=kenya", None, enq_probe, 300)
    out_run("enquire?trip=<payload>", "enquire.html?trip=" + quote(P_HTML, safe=""), None, enq_probe, 300)
    out_run("enquire?trip=%", "enquire.html?trip=%", None, enq_probe, 300)
    return out


def check_postmessage(b, base):
    """Hostile postMessage traffic to episode pages (the only own 'message' listener: episodes/episode-sync.js)."""
    out = {}
    eps = [p for p in lib.pages("live") if p.startswith("episodes/")]
    sample = ["episodes/sky-gods-flying-8000ers-antoine-girard.html"] + eps[:4]
    hostile_msgs = [
        {"event": "infoDelivery", "info": {"currentTime": P_HTML, "playerState": P_HTML}},
        {"event": "infoDelivery", "info": {"currentTime": 1e309, "playerState": 1}},
        {"event": "infoDelivery", "info": {"currentTime": -1, "playerState": 1}},
        {"event": "infoDelivery", "info": {"currentTime": 123.4, "playerState": 1}},
        {"event": P_HTML, "info": {"__proto__": {"polluted": 1}}},
        "not json " + P_HTML,
        {"event": "x", "info": None},
    ]
    frame_html = "<!doctype html><script>var M=%s;var n=0;function go(){M.forEach(function(m){parent.postMessage(typeof m==='string'?m:JSON.stringify(m),'*');});if(++n<6)setTimeout(go,200);}go();</script>" % json.dumps(hostile_msgs)
    for p in sample:
        log = {}
        mock = {"youtube-nocookie.com/embed": lambda r: r.fulfill(status=200, body=frame_html, headers={"Content-Type": "text/html"})}
        ctx = new_ctx(b, base, log, mock=mock)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.goto(base + p, wait_until="load")
        pg.evaluate("document.querySelector('.cd-player iframe') && document.querySelector('.cd-player iframe').scrollIntoView()")
        pg.wait_for_timeout(2200)
        r = pg.evaluate("""() => ({xss: window.__xss || null, sinks: window.__sinks, polluted: ({}).polluted || null,
             playing: document.body.classList.contains('cd-playing'), lit: document.querySelectorAll('.cd-line.is-now').length,
             frame_src: (document.querySelector('.cd-player iframe')||{}).src, listeners: window.__msgL.length})""")
        r["errors"] = errs
        r["frame_mocked"] = len(log.get("mocked", []))
        ctx.close()
        out["frame->" + p] = r

    # cross-origin opener: attacker page on http://localhost (different origin from 127.0.0.1)
    p = sample[0]
    target = base + p
    attacker = base.replace("127.0.0.1", "localhost") + "__attacker.html"
    att_html = """<!doctype html><button id=b onclick="start()">go</button><script>
      var w, M = %s, n = 0, T = %s;
      function start(){ w = window.open(T, 'victim'); setTimeout(go, 800); }
      function go(){ try { M.forEach(function(m){ w.postMessage(typeof m==='string'?m:JSON.stringify(m), '*'); }); } catch(e) { document.title='err '+e; }
        if(++n < 10) setTimeout(go, 250); else document.title = 'sent'; }
    </script>""" % (json.dumps(hostile_msgs), json.dumps(target))
    log = {}
    ctx = b.new_context()
    ctx.add_init_script(INIT)
    def route(r):
        u = r.request.url
        if u.endswith("__attacker.html"):
            return r.fulfill(status=200, body=att_html, headers={"Content-Type": "text/html"})
        if u.startswith(base) or u.startswith(base.replace("127.0.0.1", "localhost")):
            return r.continue_()
        return r.abort()
    ctx.route("**/*", route)
    att = ctx.new_page()
    att.goto(attacker)
    with ctx.expect_page() as pinfo:
        att.click("#b")
    vic = pinfo.value
    errs = []
    vic.on("pageerror", lambda e: errs.append(str(e)[:200]))
    vic.wait_for_load_state("load")
    att.wait_for_timeout(3500)
    out["cross-origin-opener->" + p] = vic.evaluate("""() => ({xss: window.__xss || null, sinks: window.__sinks, playing: document.body.classList.contains('cd-playing'),
          lit: document.querySelectorAll('.cd-line.is-now').length, polluted: ({}).polluted || null})""")
    out["cross-origin-opener->" + p]["errors"] = errs
    out["cross-origin-opener->" + p]["attacker_title"] = att.title()
    ctx.close()
    return out


def check_mailto(b, base):
    out = {}
    INJ_LINE = "Eve\r\nBcc: victim@evil.example\r\nX-Inj: 1"
    INJ_AMP = "Eve&bcc=victim@evil.example&cc=x@evil.example?to=y@evil.example"
    cases = {
        "enquire.html": dict(sel="#enqForm", fill={"#name": INJ_LINE, "#email": "a@b.co", "#rating": INJ_AMP,
                             "#total": "%0ABcc:evil@evil.example", "#recent": "1", "#message": "hi\r\nBcc: z@evil.example\n" + INJ_AMP},
                             check=["#consent"], submit="#enqForm button[type=submit], #enqForm [type=submit]"),
        "partners.html": dict(sel="#pwForm", fill={"#pw-name": INJ_LINE, "#pw-email": "a@b.co", "#pw-brand": INJ_AMP + "%0D%0ABcc:q@evil.example",
                             "#pw-message": "long enough message\r\nBcc: z@evil.example " + INJ_AMP}, check=[],
                             submit="#pwForm [type=submit]"),
        "podcast.html": dict(sel="#questionForm", fill={"#questionForm input[type=text]": INJ_LINE + INJ_AMP,
                             "#questionForm input[type=email]": "a@b.co", "#questionForm textarea": "question\r\nBcc: z@evil.example " + INJ_AMP},
                             check=[], submit="#questionForm [type=submit]"),
    }
    for p, c in cases.items():
        log = {}
        ctx = new_ctx(b, base, log)
        pg = ctx.new_page()
        cdp = ctx.new_cdp_session(pg)
        cdp.send("Page.enable")
        navs = []
        cdp.on("Page.frameRequestedNavigation", lambda e: navs.append(e.get("url")))
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.goto(base + p, wait_until="load")
        for s, v in c["fill"].items():
            pg.fill(s, v)
        for s in c["check"]:
            pg.check(s)
        vals = pg.evaluate("(sel) => [...document.querySelectorAll(sel + ' input, ' + sel + ' textarea')].filter(e => e.type !== 'checkbox').map(e => JSON.stringify(e.value).slice(0, 90))", c["sel"])
        pg.locator(c["submit"]).first.click()
        pg.wait_for_timeout(800)
        mails = [u for u in navs if u and u.startswith("mailto:")]
        r = {"field_values": vals, "navigations": navs[:5], "errors": errs}
        if mails:
            u = mails[0]
            addr, _, q = u[len("mailto:"):].partition("?")
            qs = parse_qs(q, keep_blank_values=True)
            subj = qs.get("subject", [""])[0]
            body = qs.get("body", [""])[0]
            r.update({"recipient": unquote(addr), "query_keys": sorted(qs.keys()),
                      "subject": subj[:200], "subject_has_crlf": bool(re.search(r"[\r\n]", subj)),
                      "body_header_like_lines": [l for l in body.splitlines() if re.match(r"^(bcc|cc|to|x-inj)\s*:", l, re.I)],
                      "raw_has_unencoded_amp_bcc": "&bcc=" in u.lower() or "&cc=" in u.lower(), "len": len(u)})
        out[p] = r
        ctx.close()
    return out


def check_stubs(b, base):
    out = {}
    tricks = "?url=https://evil.example/&next=//evil.example&redirect=https:%2F%2Fevil.example&to=javascript:alert(1)#//evil.example/%2F.."
    for s in stubs():
        log = {}
        ctx = new_ctx(b, base, log)
        pg = ctx.new_page()
        try:
            pg.goto(base + s + tricks, wait_until="load", timeout=15000)
            pg.wait_for_timeout(1200)
            final = pg.url
        except Exception as e:
            final = "ERR " + str(e)[:100]
        refresh = pg.evaluate("(document.querySelector('meta[http-equiv=refresh]')||{}).content || null") if not final.startswith("ERR") else None
        out[s] = {"final": final, "same_origin": final.startswith(base), "evil_requests": [u for u in log.get("external", []) if "evil" in u],
                  "refresh_on_final_page": refresh}
        ctx.close()
    # 404 page with hostile path/hash/query
    log = {}
    ctx = new_ctx(b, base, log)
    pg = ctx.new_page()
    pg.goto(base + "404.html?u=//evil.example#" + quote(P_HTML, safe=""), wait_until="load")
    pg.wait_for_timeout(800)
    out["404.html(hostile)"] = {"final": pg.url, "xss": pg.evaluate("window.__xss||null"), "sinks": pg.evaluate("window.__sinks")}
    ctx.close()
    return out


def evil_rss():
    x = 'x" onerror="window.__xss=(window.__xss||[]).concat(\'rss-cover\')'
    a = 'https://a.example/a.mp3" onmouseover="window.__xss=(window.__xss||[]).concat(\'rss-audio\')'
    items = []
    for i in range(8):
        items.append("""<item><title>Ep %d &lt;b&gt;bold&lt;/b&gt; &amp; "quotes" %s</title>
<link>javascript:window.__xss=(window.__xss||[]).concat('rss-link')</link><pubDate>Mon, 01 Sep 2026 10:00:00 GMT</pubDate>
<enclosure url="%s" type="audio/mpeg" length="1"/><itunes:image href="%s"/><itunes:duration>00:12:00</itunes:duration></item>""" % (
            i, MARK, a.replace('"', "&quot;"), x.replace('"', "&quot;")))
    return ('<?xml version="1.0"?><rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"><channel><title>t</title>'
            + "".join(items) + "</channel></rss>")


def evil_yt():
    t = MARK + "\"'><img src=x onerror=\"window.__xss=(window.__xss||[]).concat('yt-title')\">"
    es = []
    for i in range(3):
        es.append("""<entry><id>yt:video:abc%d</id><yt:videoId>abc%d"&gt;&lt;img src=x onerror=alert(1)&gt;</yt:videoId><title>%s</title>
<link rel="alternate" href="javascript:window.__xss=(window.__xss||[]).concat('yt-link')"/><published>2026-09-01T00:00:00Z</published>
<media:group><media:thumbnail url="x&quot; onerror=&quot;window.__xss=(window.__xss||[]).concat('yt-thumb')" /></media:group></entry>""" % (
            i, i, t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")))
    return ('<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://www.youtube.com/xml/schemas/2015" '
            'xmlns:media="http://search.yahoo.com/mrss/">' + "".join(es) + "</feed>")


def check_feeds(b, base):
    out = {}
    def worker(r):
        u = unquote(r.request.url)
        body = evil_yt() if "youtube.com/feeds" in u else evil_rss()
        return r.fulfill(status=200, body=body, headers={"Content-Type": "application/xml", "Access-Control-Allow-Origin": "*"})
    for p in ["podcast.html", "library.html"]:
        log = {}
        ctx = new_ctx(b, base, log, mock={"aninder.workers.dev": worker})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.goto(base + p, wait_until="load")
        pg.wait_for_timeout(1500)
        r = {"mocked_requests": [unquote(u)[:140] for u in log.get("mocked", [])]}
        if p == "podcast.html":
            r["dom"] = pg.evaluate("""() => { const g = document.getElementById('liveFeedGrid'); const rows = g ? g.querySelectorAll('.ep-row') : [];
              const row = rows[0];
              return {rows: rows.length,
                img_attrs: row ? [...row.querySelector('img.ep-cover').attributes].map(a => a.name + '=' + a.value.slice(0, 60)) : null,
                row_attrs: row ? [...row.attributes].map(a => a.name) : null,
                spotify_href: row ? row.querySelectorAll('a.ep-icon-btn')[1].getAttribute('href') : null,
                title_html: row ? row.querySelector('.ep-row-title').innerHTML.slice(0, 120) : null,
                yt_cards: document.querySelectorAll('#ytTrack .yt-card').length,
                yt_first: (document.querySelector('#ytTrack .yt-card')||{outerHTML:''}).outerHTML.slice(0, 400)}; }""")
            # hover the first row (data-audio attribute breakout adds onmouseover) and click the "Open on Spotify" link
            try:
                pg.hover("#liveFeedGrid .ep-row .ep-row-title", timeout=2000)
                pg.wait_for_timeout(200)
                pg.click("#liveFeedGrid .ep-row a.ep-icon-btn[target=_blank]", timeout=2000)
                pg.wait_for_timeout(300)
            except Exception as e:
                r["interact_err"] = str(e)[:120]
        r["xss"] = pg.evaluate("window.__xss || null")
        r["errors"] = errs
        ctx.close()
        out[p] = r
    return out


def check_long(b, base):
    out = {}
    big = "A" * 32000
    for p in lib.TEMPLATES["live"]:
        log = {}
        ctx = new_ctx(b, base, log)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        t = time.time()
        try:
            resp = pg.goto(base + p + "?q=" + big + "&trip=" + big[:4000] + "&m=" + big[:4000] + "#" + big + "%", wait_until="load", timeout=30000)
            st = resp.status if resp else None
        except Exception as e:
            st = "ERR " + str(e)[:80]
        pg.wait_for_timeout(400)
        out[p] = {"status": st, "secs": round(time.time() - t, 2), "errors": errs,
                  "h1": pg.evaluate("(document.querySelector('h1')||{}).textContent || null") if not str(st).startswith("ERR") else None}
        ctx.close()
    return out


def main():
    argv = sys.argv[1:]
    if "--only" in argv:
        i = argv.index("--only"); argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    n = None
    if "--pages" in sys.argv:
        n = int(sys.argv[sys.argv.index("--pages") + 1])
        args = [a for a in args if a != str(n)]
    checks = args or ["sweep", "special", "postmessage", "mailto", "stubs", "feeds", "long"]
    pages = lib.pages("live")
    if n:
        pages = pages[:n]
    with lib.server(PORT) as base:
        with lib.browser() as b:
            for c in checks:
                t = time.time()
                print("== %s" % c, flush=True)
                if c == "sweep":
                    r = check_sweep(b, base, pages + stubs())
                    print(json.dumps(r["summary"], indent=1, default=list)[:6000])
                else:
                    r = globals()["check_" + c](b, base)
                    print(json.dumps(r, indent=1, default=list)[:9000])
                fp = os.path.join(OUT, "dynamic_%s.json" % c)
                json.dump(r, open(fp, "w"), indent=1, default=list)
                print("   -> %s (%.0fs)" % (fp, time.time() - t), flush=True)


if __name__ == "__main__":
    main()
