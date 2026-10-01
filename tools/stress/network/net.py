#!/usr/bin/env python3
"""Network stress test for the LIVE Paragliding Atlas pages (repo root).

Read-only on /home/user/Website. Serves the repo root on port 8812 through
lib.server and drives Chromium through lib.browser.

    python3 net.py throttle [--pages a.html,b.html] [--profiles slow3g,fast3g,slow3g_nonetinfo]
    python3 net.py inject   [--pages ...] [--conds normal,fonts,js,css,images,external,nojs,stall] [--vps mobile,desktop]
    python3 net.py offline
    python3 net.py sweep    [--pages ...]          # all 180 pages, own-host 4xx/5xx + failed requests
    python3 net.py static                          # all 180 pages, own-asset references missing on disk
    python3 net.py all

Results: out/<mode>.json next to this file, plus a printed summary.
"""
import argparse
import gzip
import json
import os
import queue
import re
import sys
import threading
import time
import traceback
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import lib  # noqa: E402

PORT = 8812
OUTDIR = os.path.join(HERE, "out")
os.makedirs(OUTDIR, exist_ok=True)

PROFILES = {
    # bytes per second for CDP
    "slow3g": dict(latency=400, downloadThroughput=400 * 1000 / 8, uploadThroughput=400 * 1000 / 8),
    "fast3g": dict(latency=150, downloadThroughput=1600 * 1000 / 8, uploadThroughput=750 * 1000 / 8),
}
# variants (same network, one thing changed), only run on the pages they concern
PROFILES["slow3g_nonetinfo"] = PROFILES["slow3g"]      # no Network Information API (Safari, Firefox)
PROFILES["slow3g_reducedmotion"] = PROFILES["slow3g"]  # slideshow timer off (control for the hero slideshow)
PROFILES["fast3g_novideo"] = PROFILES["fast3g"]        # assets/video/* blocked (control for the hero video)
VARIANT_PAGES = {"slow3g_nonetinfo": ("index.html", "destinations/india.html"),
                 "slow3g_reducedmotion": ("destinations/india.html", "destinations/kenya.html"),
                 "fast3g_novideo": ("index.html", "destinations/india.html")}

MOBILE = dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
DESKTOP = dict(viewport={"width": 1280, "height": 800})

TEXT_EXT = {".html", ".css", ".js", ".json", ".svg", ".xml", ".txt", ".map", ".webmanifest"}

INIT = r"""
(() => {
  window.__lcp = null; window.__lcpAll = [];
  function d(el){ if(!el||!el.tagName) return null; let s=el.tagName.toLowerCase();
    if(el.id) s+='#'+el.id; if(el.classList&&el.classList.length) s+='.'+[...el.classList].slice(0,3).join('.'); return s; }
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) {
      const rec = {t: Math.round(e.startTime), size: e.size, url: (e.url||'').slice(0,200), el: d(e.element),
                   text: (e.element && !e.url) ? (e.element.textContent||'').trim().replace(/\s+/g,' ').slice(0,60) : ''};
      window.__lcp = rec; window.__lcpAll.push(rec); } })
    .observe({type:'largest-contentful-paint', buffered:true}); } catch(e) {}
  try { performance.setResourceTimingBufferSize(5000); } catch(e) {}
})();
"""

NO_NETINFO = r"""
try { Object.defineProperty(Navigator.prototype, 'connection', {get(){ return undefined; }, configurable:true}); } catch(e) {}
"""

COLLECT = r"""
() => {
  const nav = performance.getEntriesByType('navigation')[0] || {};
  const paint = {}; performance.getEntriesByType('paint').forEach(p => paint[p.name] = Math.round(p.startTime));
  const res = performance.getEntriesByType('resource').map(r => ({
    name: r.name, it: r.initiatorType, transfer: r.transferSize, enc: r.encodedBodySize, dec: r.decodedBodySize,
    start: Math.round(r.startTime), end: Math.round(r.responseEnd), rb: r.renderBlockingStatus || '', status: r.responseStatus || 0}));
  const c = navigator.connection;
  return {dcl: Math.round(nav.domContentLoadedEventEnd||0), load: Math.round(nav.loadEventEnd||0),
          ttfb: Math.round(nav.responseStart||0), docTransfer: nav.transferSize||0,
          fcp: paint['first-contentful-paint'] || null, fp: paint['first-paint'] || null,
          lcp: window.__lcp, lcpAll: (window.__lcpAll||[]).slice(-12), lcpCount: (window.__lcpAll||[]).length, res,
          conn: c ? {ect: c.effectiveType, downlink: c.downlink, rtt: c.rtt, saveData: c.saveData} : null,
          readyState: document.readyState};
}
"""

# ---------------------------------------------------------------- page probes (injection)
PROBE = r"""
async (noasync) => {
  const cache = new Map();
  function eff(el) {                     // effective opacity (0 when hidden)
    if (!el || el.nodeType !== 1) return 1;
    if (cache.has(el)) return cache.get(el);
    const cs = getComputedStyle(el);
    let o;
    if (cs.display === 'none') o = 0;
    else o = parseFloat(cs.opacity) * eff(el.parentElement);
    cache.set(el, o); return o;
  }
  function vis(el) {
    if (!el) return false;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.visibility === 'collapse') return false;
    if (eff(el) < 0.05) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }
  function sel(el) {
    if (!el || !el.tagName) return '';
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.classList && el.classList.length) s += '.' + [...el.classList].slice(0, 3).join('.');
    const p = el.parentElement;
    if (p && p !== document.body && p.tagName) {
      let ps = p.tagName.toLowerCase(); if (p.id) ps += '#' + p.id;
      else if (p.classList && p.classList.length) ps += '.' + p.classList[0];
      s = ps + ' > ' + s;
    }
    return s;
  }
  const out = {};
  // --- h1
  const h1 = document.querySelector('h1');
  out.h1 = null;
  if (h1) {
    window.scrollTo({top: 0, left: 0, behavior: 'instant'});
    h1.scrollIntoView({block: 'center', behavior: 'instant'});
    if (!noasync) await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    const r = h1.getBoundingClientRect();
    const cs = getComputedStyle(h1);
    let covered = null;
    if (r.width > 0 && r.height > 0) {
      const x = Math.min(innerWidth - 1, Math.max(0, r.left + r.width / 2)), y = Math.min(innerHeight - 1, Math.max(0, r.top + r.height / 2));
      const hit = document.elementFromPoint(x, y);
      if (hit && !(h1.contains(hit) || hit.contains(h1))) covered = sel(hit);
    }
    out.h1 = {text: h1.innerText.trim().replace(/\s+/g, ' ').slice(0, 80), w: Math.round(r.width), h: Math.round(r.height),
              left: Math.round(r.left), right: Math.round(r.right), opacity: +eff(h1).toFixed(2), visibility: cs.visibility,
              color: cs.color, fillColor: cs.webkitTextFillColor, covered,
              visible: vis(h1) && r.right > 0 && r.left < document.documentElement.clientWidth && !covered,
              font: cs.fontFamily.slice(0, 60)};
  }
  window.scrollTo({top: 0, left: 0, behavior: 'instant'});
  // --- text
  const root = document.querySelector('main') || document.body;
  out.root = root === document.body ? 'body' : 'main';
  out.innerText = (root.innerText || '').replace(/\s+/g, ' ').trim().length;
  let visText = 0, allText = 0;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const pvis = new Map();
  let n;
  while ((n = walker.nextNode())) {
    const t = n.nodeValue.replace(/\s+/g, ' ').trim();
    if (!t) continue;
    const p = n.parentElement;
    if (!p || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(p.tagName)) continue;
    allText += t.length;
    let v = pvis.get(p);
    if (v === undefined) { v = vis(p); pvis.set(p, v); }
    if (v) visText += t.length;
  }
  out.visText = visText; out.allText = allText;
  // --- overflow
  const de = document.documentElement, cw = de.clientWidth;
  out.scrollWidth = Math.max(de.scrollWidth, document.body ? document.body.scrollWidth : 0);
  out.clientWidth = cw;
  out.overflow = out.scrollWidth > cw + 1;
  out.culprits = [];
  if (out.overflow) {
    const clipOK = new Map();
    function clipped(el) {   // an ancestor clips horizontally
      for (let a = el.parentElement; a && a !== document.body && a !== de; a = a.parentElement) {
        if (clipOK.has(a)) { if (clipOK.get(a)) return true; continue; }
        const ox = getComputedStyle(a).overflowX; const c = ox !== 'visible';
        clipOK.set(a, c); if (c) return true;
      }
      return false;
    }
    const cands = [];
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.width <= 0 || r.right <= cw + 1) continue;
      if (getComputedStyle(el).position === 'fixed') continue;
      if (clipped(el)) continue;
      cands.push([el, r.right]);
    }
    const set = new Set(cands.map(c => c[0]));
    const outer = cands.filter(([el]) => !(el.parentElement && set.has(el.parentElement)));
    outer.sort((a, b) => b[1] - a[1]);
    out.culprits = outer.slice(0, 4).map(([el, right]) => ({sel: sel(el), right: Math.round(right),
      w: Math.round(el.getBoundingClientRect().width)}));
  }
  // --- stuck loading states
  const stuck = [];
  const q = '[aria-busy="true"],[class*="loading" i],[class*="skeleton" i],[class*="spinner" i],[class*="loader" i],[class*="shimmer" i],[id*="loading" i],[id*="spinner" i]';
  for (const el of document.querySelectorAll(q)) {
    if (vis(el)) stuck.push({sel: sel(el), text: (el.innerText || '').trim().slice(0, 80)});
  }
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while ((n = tw.nextNode())) {
    const t = n.nodeValue.trim();
    if (/\b(loading|connecting to|fetching|please wait)\b/i.test(t) && t.length < 140) {
      const p = n.parentElement;
      if (p && !/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(p.tagName) && vis(p)) stuck.push({sel: sel(p), text: t.slice(0, 100)});
    }
  }
  out.stuck = stuck.slice(0, 10);
  // --- images that failed/are broken but visible
  out.brokenImgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.currentSrc && vis(i)).length;
  out.imgs = document.images.length;
  return out;
}
"""

HIDE_H1_TEXT = "h1, h1 * { color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow: none !important; }"


def own_path(url, base):
    """Map an own-host URL to a file on disk (GitHub Pages semantics)."""
    p = urllib.parse.urlsplit(url).path
    p = urllib.parse.unquote(p).lstrip("/")
    fp = os.path.join(lib.ROOT, p)
    if p == "" or p.endswith("/"):
        fp = os.path.join(fp, "index.html")
    return fp


def gz_size(fp):
    try:
        with open(fp, "rb") as f:
            data = f.read()
    except OSError:
        return None, None
    return len(data), len(gzip.compress(data, 6))


PARTIAL = [None]


def run_pool(items, fn, workers=3, label=""):
    """Each worker thread has its own Playwright + Chromium."""
    q = queue.Queue()
    for it in items:
        q.put(it)
    results, lock = [], threading.Lock()
    done = [0]
    total = len(items)

    def worker():
        with lib.browser() as b:
            while True:
                try:
                    it = q.get_nowait()
                except queue.Empty:
                    return
                t0 = time.time()
                try:
                    r = fn(b, it)
                except Exception as e:  # keep going, record the failure
                    r = {"item": it, "harness_error": "%s: %s" % (type(e).__name__, str(e)[:300]),
                         "tb": traceback.format_exc()[-600:]}
                r["secs"] = round(time.time() - t0, 1)
                with lock:
                    results.append(r)
                    if PARTIAL[0]:
                        lib.save(PARTIAL[0], results)
                    done[0] += 1
                    print("[%s %d/%d] %s %.1fs" % (label, done[0], total, it, time.time() - t0), flush=True)

    ts = [threading.Thread(target=worker) for _ in range(min(workers, len(items)) or 1)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return results


# ================================================================== THROTTLE
def head_blocking(path):
    """Static list of render-blocking resources declared in <head>."""
    html = open(os.path.join(lib.ROOT, path), encoding="utf-8").read()
    head = html.split("</head>", 1)[0]
    out = []
    for m in re.finditer(r"<link\b[^>]*>", head, re.I):
        tag = m.group(0)
        if re.search(r"rel=[\"']?stylesheet", tag, re.I) and not re.search(r"media=[\"']?print", tag, re.I) \
                and "disabled" not in tag:
            href = re.search(r"href=[\"']([^\"']+)", tag)
            out.append(("css", href.group(1) if href else tag))
    for m in re.finditer(r"<script\b[^>]*>", head, re.I):
        tag = m.group(0)
        src = re.search(r"src=[\"']([^\"']+)", tag)
        if not src:
            continue
        if re.search(r"\b(async|defer)\b", tag) or re.search(r"type=[\"']?module", tag):
            continue
        out.append(("js", src.group(1)))
    # parser-blocking scripts in body (block DOMContentLoaded and everything after them)
    body = html.split("</head>", 1)[1] if "</head>" in html else ""
    body_sync = []
    for m in re.finditer(r"<script\b[^>]*>", body, re.I):
        tag = m.group(0)
        src = re.search(r"src=[\"']([^\"']+)", tag)
        if src and not re.search(r"\b(async|defer)\b", tag) and not re.search(r"type=[\"']?module", tag):
            body_sync.append(src.group(1))
    return out, body_sync


def throttle_one(b, item):
    path, prof = item
    base = BASE
    kw = dict(MOBILE)
    if prof.endswith("reducedmotion"):
        kw["reduced_motion"] = "reduce"
    ctx = b.new_context(**kw)
    ctx.add_init_script(INIT)
    if prof.endswith("nonetinfo"):
        ctx.add_init_script(NO_NETINFO)
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    reqs = {}
    doc_ts = [None]

    def on_rws(e):
        r = reqs.setdefault(e["requestId"], {"chunks": []})
        r.update(url=e["request"]["url"], type=e.get("type"), ts=e["timestamp"])
        if e.get("type") == "Document" and doc_ts[0] is None and e["request"]["url"].startswith(base):
            doc_ts[0] = e["timestamp"]

    def on_resp(e):
        r = reqs.setdefault(e["requestId"], {"chunks": []})
        r.update(status=e["response"]["status"], mime=e["response"].get("mimeType"),
                 url=e["response"]["url"], proto=e["response"].get("protocol"))

    def on_data(e):
        r = reqs.setdefault(e["requestId"], {"chunks": []})
        r["chunks"].append((e["timestamp"], e.get("encodedDataLength", 0), e.get("dataLength", 0)))

    def on_fin(e):
        r = reqs.setdefault(e["requestId"], {"chunks": []})
        r.update(fin=e["timestamp"], enc=e["encodedDataLength"])

    def on_fail(e):
        r = reqs.setdefault(e["requestId"], {"chunks": []})
        r.update(failed=e.get("errorText"), fin=e["timestamp"], canceled=e.get("canceled"))

    cdp.on("Network.requestWillBeSent", on_rws)
    cdp.on("Network.responseReceived", on_resp)
    cdp.on("Network.dataReceived", on_data)
    cdp.on("Network.loadingFinished", on_fin)
    cdp.on("Network.loadingFailed", on_fail)
    cdp.send("Network.enable")
    cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    cdp.send("Network.emulateNetworkConditions", dict(offline=False, **PROFILES[prof]))
    if prof.endswith("novideo"):
        cdp.send("Network.setBlockedURLs", {"urls": ["*assets/video/*"]})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)[:200]))
    t0 = time.time()
    load_timeout = False
    try:
        page.goto(base + path, wait_until="load", timeout=240000)
    except Exception as e:
        load_timeout = str(e)[:120]
    wall_load = time.time() - t0
    page.wait_for_timeout(3000)  # let LCP settle (no input, so LCP keeps updating)
    m = page.evaluate(COLLECT)
    ctx.close()

    # ---- bytes from CDP
    t_doc = doc_ts[0]
    load_ms = m["load"] or None
    own_before = own_total = ext_total = 0
    own_before_gz = 0
    rows = []
    for rid, r in reqs.items():
        url = r.get("url", "")
        if not url or url.startswith("data:"):
            continue
        is_own = url.startswith(base)
        enc = r.get("enc")
        if enc is None:  # unfinished / failed: sum what arrived
            enc = sum(c[1] or c[2] for c in r["chunks"])
        before = enc
        if load_ms and t_doc is not None:
            cutoff = t_doc + load_ms / 1000.0
            if r.get("fin") is not None and r["fin"] <= cutoff:
                before = enc
            else:
                before = sum((c[1] or c[2]) for c in r["chunks"] if c[0] <= cutoff)
        if is_own:
            own_total += enc
            own_before += before
            raw, gz = (None, None)
            fp = own_path(url, base)
            if os.path.splitext(fp)[1].lower() in TEXT_EXT and r.get("status") == 200:
                raw, gz = gz_size(fp)
            est = enc - raw + gz if (raw and gz and enc >= raw) else enc
            est_before = est if before >= enc else before
            own_before_gz += est_before
            rows.append({"url": url[len(base):][:120], "type": r.get("type"), "status": r.get("status"), "bytes": enc,
                         "before_load": before, "gz_est": est, "fin_ms": round((r["fin"] - t_doc) * 1000) if r.get("fin") and t_doc else None,
                         "failed": r.get("failed")})
        else:
            ext_total += enc
    rows.sort(key=lambda x: -x["bytes"])
    # bytes that had arrived before FCP / LCP / DCL (own host), raw and with text gzip-estimated
    def arrived(ms):
        if ms is None or t_doc is None:
            return None, None
        cut = t_doc + ms / 1000.0
        raw = est = 0
        for r in reqs.values():
            url = r.get("url", "")
            if not url.startswith(base):
                continue
            got = sum((c[1] or c[2]) for c in r["chunks"] if c[0] <= cut)
            if r.get("fin") is not None and r["fin"] <= cut and r.get("enc"):
                got = r["enc"]
            raw += got
            fp = own_path(url, base)
            ratio = 1.0
            if os.path.splitext(fp)[1].lower() in TEXT_EXT and r.get("status") == 200:
                rw, gz = gz_size(fp)
                if rw and gz:
                    ratio = gz / rw
            est += got * ratio
        return raw, int(est)
    lcp_ms = m["lcp"]["t"] if m["lcp"] else None
    before = {k: arrived(v) for k, v in (("fcp", m["fcp"]), ("lcp", lcp_ms), ("dcl", m["dcl"]), ("load", m["load"]))}
    ext_urls = sorted({r.get("url") for r in reqs.values() if r.get("url", "").startswith("http") and not r.get("url", "").startswith(base)})
    rb_timing = [x["name"][len(base):] for x in m["res"] if x["rb"] == "blocking" and x["name"].startswith(base)]
    head_rb, body_sync = head_blocking(path)
    own_req = [r for r in reqs.values() if r.get("url", "").startswith(base)]
    ext_req = [r for r in reqs.values() if r.get("url", "").startswith("http") and not r.get("url", "").startswith(base)]
    return {"item": [path, prof], "path": path, "profile": prof, "load_timeout": load_timeout,
            "wall_load_s": round(wall_load, 1), "ttfb": m["ttfb"], "fcp": m["fcp"], "lcp": m["lcp"],
            "dcl": m["dcl"], "load": m["load"], "conn": m["conn"],
            "own_requests": len(own_req), "ext_requests": len(ext_req),
            "own_bytes_before_load": own_before, "own_bytes_before_load_gz_est": own_before_gz,
            "own_bytes_total": own_total, "largest": rows[:8],
            "video": [r for r in rows if "/video/" in r["url"]],
            "arrived_before": before, "lcp_candidates": m.get("lcpAll"),
            "ext_unique": len(ext_urls), "ext_hosts": sorted({urllib.parse.urlsplit(u).netloc for u in ext_urls}),
            "render_blocking_timing": rb_timing, "head_render_blocking": head_rb, "body_parser_blocking": body_sync,
            "pageerrors": errors[:5]}


def do_throttle(pages, profiles):
    items = [(p, pr) for pr in profiles for p in pages if pr not in VARIANT_PAGES or p in VARIANT_PAGES[pr]]
    res = run_pool(items, throttle_one, workers=3, label="throttle")
    res.sort(key=lambda r: (r.get("profile", ""), r.get("path", "")))
    fp = lib.save("network/out/throttle.json", res)
    print("\n%-58s %-16s %6s %6s %6s %6s %5s %9s %9s %9s" % ("page", "profile", "FCP", "LCP", "DCL", "load", "req", "ownB<load", "gzEst<ld", "ownTotal"))
    for r in res:
        if "harness_error" in r:
            print(r["item"], r["harness_error"])
            continue
        lcp = r["lcp"]["t"] if r["lcp"] else None
        print("%-58s %-16s %6s %6s %6s %6s %5s %9d %9d %9d" % (r["path"][:58], r["profile"], r["fcp"], lcp, r["dcl"], r["load"],
              r["own_requests"], r["own_bytes_before_load"], r["own_bytes_before_load_gz_est"], r["own_bytes_total"]))
    print("\nFLAGS (LCP > 10 s on Slow 3G, or own-host > 2 MB before load):")
    for r in res:
        if "harness_error" in r:
            continue
        lcp = r["lcp"]["t"] if r["lcp"] else None
        if r["profile"].startswith("slow3g") and (lcp is None or lcp > 10000):
            print("  LCP", r["path"], r["profile"], lcp, r["lcp"])
        if r["own_bytes_before_load"] > 2_000_000:
            print("  BYTES", r["path"], r["profile"], r["own_bytes_before_load"], "gz est", r["own_bytes_before_load_gz_est"])
    print("saved", fp)
    return res


# ================================================================== INJECTION
BLOCKS = {
    "fonts": lambda req, base: req.resource_type == "font" or re.search(r"\.(woff2?|ttf|otf)(\?|$)", req.url),
    "js": lambda req, base: req.resource_type == "script",
    "css": lambda req, base: req.resource_type == "stylesheet",
    "images": lambda req, base: req.resource_type == "image",
    "external": lambda req, base: not req.url.startswith(base) and not req.url.startswith("data:"),
}


def contrast_h1(page, out):
    """Rendered contrast of the h1 against what is actually painted behind it."""
    try:
        from PIL import Image, ImageChops
        import io
        h1 = page.query_selector("h1")
        if not h1:
            return None
        page.evaluate("() => { window.scrollTo({top: 0, left: 0, behavior: 'instant'}); const h=document.querySelector('h1'); h && h.scrollIntoView({block:'center', behavior:'instant'}); }")
        page.wait_for_timeout(150)
        bb = h1.bounding_box()
        if not bb or bb["width"] < 2 or bb["height"] < 2:
            return None
        vw = page.viewport_size
        clip = {"x": max(0, bb["x"]), "y": max(0, bb["y"]), "width": min(bb["width"], vw["width"] - max(0, bb["x"])),
                "height": min(bb["height"], vw["height"] - max(0, bb["y"]))}
        if clip["width"] < 2 or clip["height"] < 2:
            return None
        a = Image.open(io.BytesIO(page.screenshot(clip=clip, animations="disabled"))).convert("RGB")
        st = page.add_style_tag(content=HIDE_H1_TEXT)
        page.wait_for_timeout(60)
        bgi = Image.open(io.BytesIO(page.screenshot(clip=clip, animations="disabled"))).convert("RGB")
        st.evaluate("e => e.remove()")
        if a.size != bgi.size:
            return None
        diff = ImageChops.difference(a, bgi).convert("L")
        gd = (lambda im: list(im.get_flattened_data())) if hasattr(a, "get_flattened_data") else (lambda im: list(im.getdata()))
        px_a, px_b, px_d = gd(a), gd(bgi), gd(diff)
        idx = sorted(range(len(px_d)), key=lambda i: -px_d[i])
        strong = [i for i in idx[: max(20, len(idx) // 20)] if px_d[i] > 0]
        if not strong:
            return {"ratio": None, "note": "text pixels identical to background (text invisible)", "diffmax": 0}

        def lum(c):
            def ch(v):
                v /= 255
                return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
            return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])
        ratios = []
        for i in strong:
            l1, l2 = lum(px_a[i]), lum(px_b[i])
            hi, lo = max(l1, l2), min(l1, l2)
            ratios.append((hi + 0.05) / (lo + 0.05))
        ratios.sort()
        med = ratios[len(ratios) // 2]
        return {"ratio": round(med, 2), "diffmax": max(px_d), "n": len(strong)}
    except Exception as e:
        return {"error": str(e)[:160]}


def inject_one(b, item):
    path, cond, vpn = item
    base = BASE
    kw = dict(MOBILE if vpn == "mobile" else DESKTOP)
    if vpn == "mobile":
        kw["device_scale_factor"] = 1
    if cond == "nojs":
        kw["java_script_enabled"] = False
    ctx = b.new_context(**kw)
    page = ctx.new_page()
    blocked = []
    stalled = []
    if cond in BLOCKS:
        pred = BLOCKS[cond]

        def handler(route, req, pred=pred):
            if pred(req, base):
                blocked.append(req.url[:120])
                route.abort()
            else:
                route.continue_()
        page.route("**/*", handler)
    elif cond == "stall":
        def handler(route, req):
            if not req.url.startswith(base) and not req.url.startswith("data:"):
                stalled.append(route)
                blocked.append(req.url[:120])
                return  # never answered: the request hangs
            route.continue_()
        page.route("**/*", handler)
    errors, cons = [], []
    page.on("pageerror", lambda e: errors.append({"msg": str(e)[:240], "stack": (getattr(e, "stack", "") or "")[:400]}))
    page.on("console", lambda m: cons.append({"type": m.type, "text": m.text[:240], "loc": (m.location or {}).get("url", "")[:160]})
            if m.type in ("error", "warning") else None)
    t0 = time.time()
    nav_err = None
    try:
        page.goto(base + path, wait_until=("domcontentloaded" if cond == "stall" else "load"), timeout=45000)
    except Exception as e:
        nav_err = str(e)[:200]
    page.wait_for_timeout(7000 if cond == "stall" else 2500)
    # read the page like a visitor: scroll to the end so scroll-triggered reveals fire, then back to the top
    try:
        if cond == "nojs":
            raise RuntimeError("no timers without JS")
        page.evaluate("""async () => { const h = () => document.documentElement.scrollHeight;
          for (let y = 0, i = 0; y < h() && i < 80; y += innerHeight * 0.8, i++) { window.scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 90)); }
          await new Promise(r => setTimeout(r, 1200)); window.scrollTo({top: 0, left: 0, behavior: 'instant'}); }""")
        page.wait_for_timeout(400)
    except Exception:
        pass
    try:
        probe = page.evaluate(PROBE, cond == "nojs")
    except Exception as e:
        probe = {"error": str(e)[:200]}
    con = contrast_h1(page, probe) if cond in ("normal", "images", "css", "fonts", "js") else None
    for rt in stalled:
        try:
            rt.abort()
        except Exception:
            pass
    ctx.close()
    own_err = []
    for e in errors:
        st = e["stack"] or ""
        ext = re.findall(r"https?://[^\s)]+", st)
        if any(u.startswith(base) for u in ext) or not ext:
            own_err.append(e)
    own_cons = [c for c in cons if c["type"] == "error" and c["loc"].startswith(base)
                and "Failed to load resource" not in c["text"]]
    return {"item": [path, cond, vpn], "path": path, "cond": cond, "vp": vpn, "nav_err": nav_err,
            "blocked": len(blocked), "blocked_sample": blocked[:4], "probe": probe, "contrast": con,
            "own_pageerrors": own_err, "all_pageerrors": len(errors), "own_console_errors": own_cons[:6],
            "load_s": round(time.time() - t0, 1)}


def do_inject(pages, conds, vps):
    items = []
    for vp in vps:
        for c in conds:
            if vp == "desktop" and c in ("stall",):
                continue
            for p in pages:
                items.append((p, c, vp))
    PARTIAL[0] = "network/out/inject_%s.partial.json" % "_".join(vps)
    res = run_pool(items, inject_one, workers=3, label="inject")
    PARTIAL[0] = None
    fp = lib.save("network/out/inject_%s.json" % "_".join(vps), res)
    # summary vs normal
    idx = {(r["path"], r["cond"], r["vp"]): r for r in res if "harness_error" not in r}
    print("\nINJECTION SUMMARY (only rows with a problem)")
    for r in sorted(idx.values(), key=lambda r: (r["vp"], r["path"], r["cond"])):
        pr = r["probe"]
        if "error" in pr:
            print(" ", r["vp"], r["path"], r["cond"], "PROBE ERROR", pr["error"])
            continue
        norm = idx.get((r["path"], "normal", r["vp"]))
        nv = norm["probe"].get("visText") if norm else None
        issues = []
        if pr["h1"] is None:
            issues.append("no h1")
        elif not pr["h1"]["visible"]:
            issues.append("h1 NOT visible %s" % json.dumps(pr["h1"]))
        if nv and pr["visText"] < 0.8 * nv:
            issues.append("visible text %d vs normal %d (%.0f%%)" % (pr["visText"], nv, 100 * pr["visText"] / nv))
        if pr["overflow"] and not (norm and norm["probe"].get("overflow")):
            issues.append("NEW overflow sw=%d cw=%d %s" % (pr["scrollWidth"], pr["clientWidth"], pr["culprits"][:2]))
        elif pr["overflow"]:
            issues.append("overflow (also in normal) sw=%d cw=%d %s" % (pr["scrollWidth"], pr["clientWidth"], pr["culprits"][:2]))
        if r["own_pageerrors"]:
            issues.append("own uncaught errors: %s" % [e["msg"][:120] for e in r["own_pageerrors"]][:3])
        if pr["stuck"]:
            issues.append("loading states: %s" % pr["stuck"][:3])
        if r["contrast"] and r["contrast"].get("ratio") is not None and r["contrast"]["ratio"] < 3:
            issues.append("h1 contrast %.2f" % r["contrast"]["ratio"])
        if r["contrast"] and r["contrast"].get("note"):
            issues.append("h1 contrast: %s" % r["contrast"]["note"])
        if issues:
            print("  [%s] %-50s %-8s %s" % (r["vp"], r["path"][:50], r["cond"], " | ".join(issues)))
    for r in res:
        if "harness_error" in r:
            print("HARNESS", r["item"], r["harness_error"])
    print("saved", fp)
    return res


# ================================================================== OFFLINE
def first_internal_link(page, base):
    return page.evaluate(r"""(base) => {
      const cur = location.href.split('#')[0];
      for (const a of document.querySelectorAll('main a[href], a[href]')) {
        const u = a.href.split('#')[0];
        if (!u.startsWith(base) || u === cur || !/\.html$|\/$/.test(u)) continue;
        const r = a.getBoundingClientRect(); const cs = getComputedStyle(a);
        if (r.width < 2 || r.height < 2 || cs.visibility === 'hidden' || +cs.opacity < 0.1) continue;
        if (a.target === '_blank') continue;
        a.setAttribute('data-net-test', '1');
        return {href: a.getAttribute('href'), abs: u, text: (a.innerText||'').trim().slice(0,40)};
      }
      return null; }""", base)


def offline_one(b, item):
    path, action = item
    base = BASE
    ctx = b.new_context(**MOBILE)
    page = ctx.new_page()
    errors, cons = [], []
    page.on("pageerror", lambda e: errors.append(str(e)[:240]))
    page.on("console", lambda m: cons.append(m.text[:200]) if m.type == "error" else None)
    page.goto(base + path, wait_until="load", timeout=45000)
    page.wait_for_timeout(1200)
    sw = page.evaluate("() => !!(navigator.serviceWorker && navigator.serviceWorker.controller)")
    out = {"item": [path, action], "path": path, "action": action, "service_worker_controls": sw}
    if action == "link":
        link = first_internal_link(page, base)
        out["link"] = link
        ctx.set_offline(True)
        if link:
            try:
                page.click("a[data-net-test]", timeout=5000, no_wait_after=False)
            except Exception as e:
                out["click_err"] = str(e)[:160]
            page.wait_for_timeout(2500)
            out["after_url"] = page.url[:160]
            try:
                out["after_title"] = page.title()
                out["after_text"] = page.evaluate("() => (document.body && document.body.innerText || '').trim().slice(0,160)")
            except Exception as e:
                out["after_err"] = str(e)[:120]
            out["chrome_error_page"] = page.url.startswith("chrome-error://") or "ERR_INTERNET_DISCONNECTED" in (out.get("after_text") or "")
    elif action == "audio":
        ctx.set_offline(True)
        btn = page.query_selector(".ep-au-play")
        out["has_button"] = bool(btn)
        if btn:
            btn.click()
            page.wait_for_timeout(6000)
            out["state"] = page.evaluate("""() => { const r=document.querySelector('.ep-au'); const a=r.querySelector('audio');
               const b=r.querySelector('.ep-au-play');
               return {is_playing_class: r.classList.contains('is-playing'), btn_label: b.getAttribute('aria-label'),
                       paused: a.paused, networkState: a.networkState, readyState: a.readyState,
                       error: a.error ? a.error.code + ' ' + (a.error.message||'') : null,
                       time_text: r.querySelector('.ep-au-cur').textContent,
                       visible_error_msg: [...r.parentElement.querySelectorAll('*')].some(e => /(offline|couldn.t|could not|unavailable|error|failed)/i.test(e.childElementCount?'' : e.textContent||'') && e.offsetParent)}; }""")
            # second click: can the visitor recover (toggle back to Play)?
            btn.click()
            page.wait_for_timeout(800)
            out["after_second_click"] = page.evaluate("""() => { const r=document.querySelector('.ep-au'); const a=r.querySelector('audio');
               return {is_playing_class: r.classList.contains('is-playing'), btn_label: r.querySelector('.ep-au-play').getAttribute('aria-label'), paused: a.paused}; }""")
    elif action == "online_audio_blocked":
        # online, but the audio host is unreachable (the case in this sandbox, a blocked CDN, a firewall)
        btn = page.query_selector(".ep-au-play")
        out["has_button"] = bool(btn)
        if btn:
            btn.click()
            page.wait_for_timeout(6000)
            out["state"] = page.evaluate("""() => { const r=document.querySelector('.ep-au'); const a=r.querySelector('audio');
               const b=r.querySelector('.ep-au-play');
               return {is_playing_class: r.classList.contains('is-playing'), btn_label: b.getAttribute('aria-label'),
                       paused: a.paused, networkState: a.networkState, readyState: a.readyState,
                       error: a.error ? a.error.code + ' ' + (a.error.message||'') : null,
                       time_text: r.querySelector('.ep-au-cur').textContent}; }""")
    elif action == "timestamp":
        ctx.set_offline(True)
        ts = page.query_selector(".cd-ts.cd-seek, .cd-block-time.cd-seek")
        out["has_seek"] = bool(ts)
        if ts:
            before = page.evaluate("() => document.querySelector('.cd-player iframe').src")
            ts.click()
            page.wait_for_timeout(2500)
            out["iframe_src_before"] = before[:140]
            out["iframe_src_after"] = page.evaluate("() => document.querySelector('.cd-player iframe').src")[:140]
            out["player_box"] = page.evaluate("() => { const r=document.querySelector('.cd-player').getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; }")
    elif action == "modal":
        ctx.set_offline(True)
        if page.query_selector("#allBtn"):
            page.click("#allBtn")
            page.wait_for_timeout(600)
        tile = page.query_selector("a.ep-tile")
        out["has_tile"] = bool(tile)
        if tile:
            tile.click()
            page.wait_for_timeout(2000)
            out["after_url"] = page.url[:160]
            out["modal_open"] = page.evaluate("() => !!document.querySelector('.kb-card[role=dialog]')")
            play = page.query_selector("button.kb-med")
            out["has_play"] = bool(play)
            if play:
                try:
                    play.click(timeout=3000)
                except Exception as e:
                    out["play_click_err"] = str(e)[:120]
                page.wait_for_timeout(2000)
                out["iframe_after_play"] = page.evaluate("() => { const f=document.querySelector('.kb-card iframe.kb-frame'); if(!f) return null; const r=f.getBoundingClientRect(); return {src: f.src.slice(0,100), w: Math.round(r.width), h: Math.round(r.height)}; }")
    out["pageerrors"] = errors
    out["console_errors"] = [c for c in cons if "ERR_INTERNET_DISCONNECTED" not in c][:5]
    ctx.close()
    return out


def do_offline(pages):
    items = [(p, "link") for p in pages]
    items += [("episodes/maxime-pinot-the-journey-within.html", "audio"),
              ("episodes/maxime-pinot-the-journey-within.html", "online_audio_blocked"),
              ("episodes/anatomy-of-a-dream-with-damien-lacaze.html", "audio"),
              ("episodes/sky-gods-flying-8000ers-antoine-girard.html", "timestamp"),
              ("library.html", "modal")]
    res = run_pool(items, offline_one, workers=3, label="offline")
    fp = lib.save("network/out/offline.json", res)
    for r in sorted(res, key=lambda r: (r.get("action", ""), r.get("path", ""))):
        if "harness_error" in r:
            print("HARNESS", r["item"], r["harness_error"])
            continue
        print(r["action"], r["path"], json.dumps({k: v for k, v in r.items() if k not in ("item", "path", "action", "secs")})[:600])
    print("saved", fp)
    return res


# ================================================================== SWEEP (all pages, normal speed)
def sweep_one(b, path):
    base = BASE
    ctx = b.new_context(**DESKTOP)
    page = ctx.new_page()
    bad, failed, errors = [], [], []
    page.on("response", lambda r: bad.append({"status": r.status, "url": r.url[len(base):][:160],
                                             "type": r.request.resource_type})
            if r.url.startswith(base) and r.status >= 400 else None)
    page.on("requestfailed", lambda r: failed.append({"url": r.url[len(base):][:160], "err": r.failure,
                                                      "type": r.resource_type})
            if r.url.startswith(base) else None)
    page.on("pageerror", lambda e: errors.append(str(e)[:200]))
    try:
        page.goto(base + path, wait_until="load", timeout=45000)
    except Exception as e:
        errors.append("NAV " + str(e)[:150])
    # scroll through the page so lazy images/iframes/videos below the fold ask for their files
    try:
        page.evaluate("""async () => { const h = () => document.documentElement.scrollHeight;
          for (let y = 0, i = 0; y < h() && i < 60; y += innerHeight * 0.9, i++) { window.scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 60)); }
          window.scrollTo({top: h(), behavior: 'instant'}); }""")
        page.wait_for_timeout(900)
    except Exception as e:
        errors.append("SCROLL " + str(e)[:120])
    ctx.close()
    # a 404 on the page's own document is expected only for 404.html (it is served 200 here anyway)
    failed = [f for f in failed if f["err"] not in ("net::ERR_ABORTED",) or f["type"] not in ("media",)]
    return {"item": path, "path": path, "bad": bad, "failed": failed, "pageerrors": errors[:5]}


def do_sweep(pages):
    res = run_pool(pages, sweep_one, workers=4, label="sweep")
    fp = lib.save("network/out/sweep.json", res)
    by_url = {}
    for r in res:
        for x in r.get("bad", []):
            by_url.setdefault((x["status"], x["url"]), []).append(r["path"])
    print("\nOWN-HOST 4xx/5xx: %d distinct" % len(by_url))
    for (st, u), ps in sorted(by_url.items(), key=lambda kv: -len(kv[1])):
        print("  %s %s  on %d pages e.g. %s" % (st, u, len(ps), ps[:5]))
    ff = {}
    for r in res:
        for x in r.get("failed", []):
            ff.setdefault((x["err"], x["url"]), []).append(r["path"])
    print("OWN-HOST failed requests: %d distinct" % len(ff))
    for (err, u), ps in sorted(ff.items(), key=lambda kv: -len(kv[1]))[:30]:
        print("  %s %s on %d pages e.g. %s" % (err, u, len(ps), ps[:4]))
    pe = [(r["path"], r["pageerrors"]) for r in res if r.get("pageerrors")]
    print("pages with uncaught errors at normal speed: %d" % len(pe))
    for p, e in pe[:15]:
        print("  ", p, e[:2])
    for r in res:
        if "harness_error" in r:
            print("HARNESS", r["item"], r["harness_error"])
    print("saved", fp)
    return res


# ================================================================== STATIC own-asset references
ATTR_RE = re.compile(r"""\b(src|href|poster|data-src|data-loop|srcset|data-srcset)\s*=\s*["']([^"']+)["']""", re.I)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")


def exists_like_pages(fp):
    if os.path.isfile(fp):
        return True
    if os.path.isdir(fp) and os.path.isfile(os.path.join(fp, "index.html")):
        return True
    if not os.path.splitext(fp)[1] and os.path.isfile(fp + ".html"):
        return True
    return False


def do_static(pages):
    missing = {}
    css_seen = set()
    link_missing = {}

    def check(ref, page_dir, where, kind, bucket):
        ref = ref.strip()
        if not ref or ref.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "http:", "https:", "//", "{", "$")):
            return
        if "${" in ref or "' +" in ref:
            return
        u = urllib.parse.urlsplit(ref)
        p = urllib.parse.unquote(u.path)
        if not p:
            return
        fp = os.path.normpath(os.path.join(lib.ROOT, p.lstrip("/")) if p.startswith("/") else os.path.join(page_dir, p))
        if not fp.startswith(lib.ROOT):
            bucket.setdefault((kind, os.path.relpath(fp, lib.ROOT)), set()).add(where)
            return
        if not exists_like_pages(fp):
            bucket.setdefault((kind, os.path.relpath(fp, lib.ROOT)), set()).add(where)

    for path in pages:
        full = os.path.join(lib.ROOT, path)
        html = open(full, encoding="utf-8").read()
        html_nocode = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S | re.I)
        page_dir = os.path.dirname(full)
        for m in re.finditer(r"<(\w+)\b[^>]*>", html_nocode):
            tag = m.group(0)
            tname = m.group(1).lower()
            for am in ATTR_RE.finditer(tag):
                attr, val = am.group(1).lower(), am.group(2)
                if attr in ("srcset", "data-srcset"):
                    for part in val.split(","):
                        check(part.strip().split(" ")[0], page_dir, path, "asset", missing)
                elif attr == "data-loop":
                    for ext in (("-720.webm", "-720.mp4", "-1080.webm", "-1080.mp4")):
                        check(val + ext, page_dir, path, "asset", missing)
                elif attr == "href" and tname == "a":
                    check(val, page_dir, path, "link", link_missing)
                elif attr == "href" and tname == "link":
                    rel = re.search(r"rel=[\"']([^\"']+)", tag)
                    if rel and rel.group(1).lower() in ("canonical", "alternate"):
                        continue
                    check(val, page_dir, path, "asset", missing)
                    if val.split("?")[0].endswith(".css"):
                        css_seen.add(os.path.normpath(os.path.join(page_dir, urllib.parse.unquote(val.split("?")[0]))))
                else:
                    check(val, page_dir, path, "asset", missing)
        for m in re.finditer(r"style=[\"']([^\"']*url\([^\"']*)[\"']", html_nocode):
            for um in CSS_URL_RE.finditer(m.group(1)):
                check(um.group(1), page_dir, path, "asset", missing)
    for css in sorted(css_seen):
        if not os.path.isfile(css):
            continue
        txt = open(css, encoding="utf-8").read()
        for um in CSS_URL_RE.finditer(txt):
            check(um.group(1), os.path.dirname(css), os.path.relpath(css, lib.ROOT), "css-asset", missing)
    out = {"missing_assets": [{"kind": k, "path": p, "pages": sorted(v)[:10], "count": len(v)} for (k, p), v in sorted(missing.items())],
           "missing_link_targets": [{"path": p, "pages": sorted(v)[:10], "count": len(v)} for (k, p), v in sorted(link_missing.items())]}
    fp = lib.save("network/out/static.json", out)
    print("missing own assets referenced in HTML/CSS: %d" % len(out["missing_assets"]))
    for x in out["missing_assets"][:40]:
        print("  ", x)
    print("internal <a href> targets missing on disk: %d" % len(out["missing_link_targets"]))
    for x in out["missing_link_targets"][:40]:
        print("  ", x)
    print("saved", fp)
    return out


# ================================================================== ONE OWN SCRIPT FAILS (partial JS failure)
def own_scripts(path):
    html = open(os.path.join(lib.ROOT, path), encoding="utf-8").read()
    out = []
    for m in re.finditer(r"<script\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", html, re.I):
        src = m.group(1)
        if src.startswith(("http:", "https:", "//")):
            continue
        out.append(src.split("?")[0].split("/")[-1])
    return out


def jsone_one(b, item):
    path, script = item
    base = BASE
    ctx = b.new_context(**dict(MOBILE, device_scale_factor=1))
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append({"msg": str(e)[:200], "stack": (getattr(e, "stack", "") or "")[:300]}))
    if script:
        def handler(route, req):
            u = req.url.split("?")[0]
            if req.resource_type == "script" and u.startswith(base) and u.endswith("/" + script):
                route.abort()
            else:
                route.continue_()
        page.route("**/*", handler)
    try:
        page.goto(base + path, wait_until="load", timeout=45000)
    except Exception as e:
        errors.append({"msg": "NAV " + str(e)[:150], "stack": ""})
    page.wait_for_timeout(2000)
    try:
        page.evaluate("""async () => { const h = () => document.documentElement.scrollHeight;
          for (let y = 0, i = 0; y < h() && i < 80; y += innerHeight * 0.8, i++) { window.scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 80)); }
          await new Promise(r => setTimeout(r, 1000)); window.scrollTo({top: 0, left: 0, behavior: 'instant'}); }""")
    except Exception:
        pass
    probe = page.evaluate(PROBE, False)
    empties = page.evaluate("""() => [...document.querySelectorAll('main [id], body [id]')].filter(e => /^(DIV|UL|OL|SECTION)$/.test(e.tagName)
        && e.children.length === 0 && !(e.textContent||'').trim() && !e.closest('noscript')).map(e => '#' + e.id).slice(0, 40)""")
    ctx.close()
    own = [e for e in errors if (base in e["stack"]) or not re.findall(r"https?://", e["stack"])]
    return {"item": [path, script], "path": path, "blocked": script, "own_pageerrors": own,
            "visText": probe.get("visText"), "h1_visible": (probe.get("h1") or {}).get("visible"),
            "stuck": probe.get("stuck"), "empty_containers": empties}


def do_jsone(pages):
    items = []
    for p in pages:
        items.append((p, None))
        for sc in dict.fromkeys(own_scripts(p)):
            items.append((p, sc))
    PARTIAL[0] = "network/out/jsone.partial.json"
    res = run_pool(items, jsone_one, workers=3, label="jsone")
    PARTIAL[0] = None
    fp = lib.save("network/out/jsone.json", res)
    base_by = {r["path"]: r for r in res if r.get("blocked") is None and "harness_error" not in r}
    print("\nONE OWN SCRIPT BLOCKED (rows with own uncaught errors, >20% visible text lost, or new empty containers)")
    for r in sorted(res, key=lambda r: (r.get("path", ""), r.get("blocked") or "")):
        if "harness_error" in r or r.get("blocked") is None:
            if "harness_error" in r:
                print("HARNESS", r["item"], r["harness_error"])
            continue
        n = base_by.get(r["path"])
        issues = []
        if r["own_pageerrors"]:
            issues.append("errors: %s" % [e["msg"][:100] for e in r["own_pageerrors"]][:3])
        if n and n["visText"] and r["visText"] < 0.8 * n["visText"]:
            issues.append("visible text %d vs %d (%.0f%%)" % (r["visText"], n["visText"], 100 * r["visText"] / n["visText"]))
        new_empty = sorted(set(r["empty_containers"]) - set(n["empty_containers"] if n else []))
        if new_empty:
            issues.append("empty now: %s" % new_empty[:8])
        if r["stuck"] and not (n and n["stuck"]):
            issues.append("loading: %s" % r["stuck"][:2])
        if issues:
            print("  %-45s %-28s %s" % (r["path"][:45], r["blocked"], " | ".join(issues)))
    print("saved", fp)
    return res


BASE = None


def main():
    global BASE
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["throttle", "inject", "jsone", "offline", "sweep", "static", "all"])
    ap.add_argument("--pages", default="")
    ap.add_argument("--profiles", default="slow3g,fast3g,slow3g_nonetinfo,slow3g_reducedmotion,fast3g_novideo")
    ap.add_argument("--conds", default="normal,fonts,js,css,images,external,nojs,stall")
    ap.add_argument("--vps", default="mobile,desktop")
    a = ap.parse_args()
    tpl = lib.TEMPLATES["live"]
    sel = [p for p in a.pages.split(",") if p] or None
    if a.mode == "static":
        do_static(sel or lib.pages("live"))
        return
    with lib.server(PORT) as base:
        BASE = base
        t0 = time.time()
        if a.mode in ("throttle", "all"):
            do_throttle(sel or tpl, a.profiles.split(","))
        if a.mode in ("inject", "all"):
            do_inject(sel or tpl, a.conds.split(","), a.vps.split(","))
        if a.mode in ("jsone", "all"):
            do_jsone(sel or tpl)
        if a.mode in ("offline", "all"):
            do_offline(sel or tpl)
        if a.mode in ("sweep", "all"):
            do_sweep(sel or lib.pages("live"))
        print("total %.0fs" % (time.time() - t0))
    if a.mode == "all":
        do_static(lib.pages("live"))


if __name__ == "__main__":
    main()
