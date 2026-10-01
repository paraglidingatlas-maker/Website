"""CPU, animation and memory stress on the live Paragliding Atlas templates.

    python3 perf.py load     [pages...] [--rates 4,6] [--runs 3]
    python3 perf.py scroll   [pages...] [--rate 4]    [--runs 3]
    python3 perf.py idle1x   [pages...]               [--runs 3]
    python3 perf.py ablate   [pages...] [--rate 4] [--where top,bottom] [--runs 3]
    python3 perf.py inp      [pages...] [--rate 4] [--runs 3]   tap responsiveness (Event Timing) top/bottom; KB door
    python3 perf.py vario    [pages...] [--rate 4] [--runs 3]   Kenya vario loop left running off screen after a quick pass
    python3 perf.py interact [scenarios...]           [--runs 3]   (globe rail modal kenya_map kenya_gallery podcast nav)

Phases
  load     cold load, Fast 3G + CPU throttle (4x and 6x): TBT, long tasks, LCP, DCL, FCP, load, LoAF attribution
  scroll   CPU 4x, no network throttle: idle-at-top CPU (5 s), 30-step scroll rAF frame gaps,
           idle-after-scroll CPU (5 s), heap after GC, DOM nodes, listeners
  idle1x   the two idle windows again at 1x (desktop) CPU, for reference
  interact the heavy interactive parts used 20 times x 3 batches, heap after forced GC per batch

Read-only on the repo. Serves the repo root on port 8890 via lib.server, external hosts fail fast through
--host-resolver-rules (they are blocked by this environment anyway). The podcast page's two live feeds go
through a Cloudflare worker that is unreachable here; they are answered with a synthetic feed (10 videos,
100 episodes) so the page runs its real code path (rails populated) instead of the error path.
Outputs JSON next to this file: out_<phase>[_<tag>].json
"""
import json
import os
import statistics as st
import sys
import time

sys.path.insert(0, "/home/user/Website/tools/stress")
import lib  # noqa: E402

PORT = 8890
HERE = os.path.dirname(os.path.abspath(__file__))
UA = ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/141.0.0.0 Mobile Safari/537.36")
FAST3G = dict(offline=False, latency=562.5, downloadThroughput=180000, uploadThroughput=84375,
              connectionType="cellular3g")
LAUNCH = dict(args=["--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1",
                    "--disable-features=HttpsUpgrades"])

INIT = r"""
(() => {
  if (window.__perf) return;
  const P = window.__perf = {lt: [], loaf: [], lcp: null, raf: 0, st: 0, si: 0, trace: false, stacks: {}};
  const oRAF = window.requestAnimationFrame.bind(window);
  const oST = window.setTimeout.bind(window);
  const oSI = window.setInterval.bind(window);
  window.__origRAF = oRAF; window.__origST = oST;
  function site() {
    const s = (new Error().stack || '').split('\n');
    return (s[3] || '?').trim().replace(/^at /, '').replace(/\?v=[0-9a-f]+/, '').replace(/https?:\/\/127\.0\.0\.1:\d+\//, '');
  }
  window.requestAnimationFrame = function (cb) {
    P.raf++;
    if (P.trace || P.block) {
      const k = site();
      if (P.trace) P.stacks[k] = (P.stacks[k] || 0) + 1;
      if (P.block && P.block.some((b) => k.includes(b))) { P.blocked = (P.blocked || 0) + 1; return 0; }
    }
    return oRAF(cb);
  };
  window.setTimeout = function (f, ms, ...a) {
    P.st++;
    if (P.trace) { const k = 'setTimeout ' + site(); P.stacks[k] = (P.stacks[k] || 0) + 1; }
    return oST(f, ms, ...a);
  };
  window.setInterval = function (f, ms, ...a) { P.si++; return oSI(f, ms, ...a); };
  const name = (el) => !el ? '' : el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
      (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  try {
    new PerformanceObserver((l) => { for (const e of l.getEntries()) P.lt.push([e.startTime, e.duration]); })
      .observe({type: 'longtask', buffered: true});
  } catch (e) {}
  try {
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) {
        if (e.duration < 50) continue;
        P.loaf.push({s: e.startTime, d: e.duration, blk: e.blockingDuration,
          sl: e.styleAndLayoutStart ? Math.max(0, e.startTime + e.duration - e.styleAndLayoutStart) : 0,
          scripts: (e.scripts || []).map((x) => ({u: (x.sourceURL || '').replace(/^https?:\/\/127\.0\.0\.1:\d+\//, '').replace(/\?v=[0-9a-f]+/, ''),
              f: x.sourceFunctionName || '', inv: (x.invoker || '').slice(0, 80), d: x.duration, fs: x.forcedStyleAndLayoutDuration || 0}))});
      }
    }).observe({type: 'long-animation-frame', buffered: true});
  } catch (e) {}
  try {
    new PerformanceObserver((l) => {
      const es = l.getEntries(); const e = es[es.length - 1];
      P.lcp = {t: e.startTime, el: name(e.element), url: (e.url || '').replace(/^https?:\/\/127\.0\.0\.1:\d+\//, ''), size: e.size};
    }).observe({type: 'largest-contentful-paint', buffered: true});
  } catch (e) {}
})();
"""

COLLECT_LOAD = r"""
() => {
  const P = window.__perf, nav = performance.getEntriesByType('navigation')[0] || {};
  const fcp = (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime || null;
  const tbt = P.lt.reduce((a, x) => a + Math.max(0, x[1] - 50), 0);
  const tbtLoad = P.lt.filter((x) => !nav.loadEventEnd || x[0] < nav.loadEventEnd).reduce((a, x) => a + Math.max(0, x[1] - 50), 0);
  const by = {};
  for (const f of P.loaf) for (const s of f.scripts) { const k = (s.u || '(inline/none)') + ' :: ' + (s.inv || s.f); by[k] = (by[k] || 0) + s.d; }
  const top = Object.entries(by).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([k, v]) => [k, Math.round(v)]);
  const sl = P.loaf.reduce((a, f) => a + f.sl, 0);
  return {tbt: Math.round(tbt), tbt_to_load: Math.round(tbtLoad), n_long: P.lt.length,
          longest: Math.round(Math.max(0, ...P.lt.map((x) => x[1]))),
          lcp: P.lcp ? Math.round(P.lcp.t) : null, lcp_el: P.lcp ? P.lcp.el + ' ' + P.lcp.url : null,
          dcl: Math.round(nav.domContentLoadedEventEnd || 0), load: Math.round(nav.loadEventEnd || 0),
          fcp: fcp && Math.round(fcp), loaf_top: top, loaf_style_layout: Math.round(sl),
          long_list: P.lt.map((x) => [Math.round(x[0]), Math.round(x[1])]).slice(0, 40)};
}
"""

SCROLL = r"""
async ([steps, wait]) => {
  const P = window.__perf, gaps = []; let last = 0, run = true;
  const t0 = performance.now();
  P.lt0 = P.lt.length; P.loaf0 = P.loaf.length;
  function f(t) { if (last) gaps.push(t - last); last = t; if (run) __origRAF(f); }
  __origRAF(f);
  const ys = [];
  for (let i = 1; i <= steps; i++) {
    const H = document.documentElement.scrollHeight - innerHeight;
    window.scrollTo({top: Math.round(H * i / steps), behavior: 'instant'});
    ys.push(Math.round(scrollY));
    await new Promise((r) => __origST(r, wait));
  }
  await new Promise((r) => __origST(r, 300));
  run = false;
  const t1 = performance.now();
  const s = gaps.slice().sort((a, b) => a - b);
  const p = (q) => s.length ? s[Math.min(s.length - 1, Math.floor(q * s.length))] : null;
  const lt = P.lt.slice(P.lt0), lf = P.loaf.slice(P.loaf0);
  const by = {};
  for (const fr of lf) for (const sc of fr.scripts) { const k = (sc.u || '(none)') + ' :: ' + (sc.inv || sc.f); by[k] = (by[k] || 0) + sc.d; }
  const worst = lf.slice().sort((a, b) => b.d - a.d).slice(0, 3).map((fr) => ({d: Math.round(fr.d), sl: Math.round(fr.sl),
      scripts: fr.scripts.slice(0, 3).map((x) => [x.u, x.inv, Math.round(x.d), Math.round(x.fs)])}));
  return {frames: gaps.length, over50: gaps.filter((g) => g > 50).length, over100: gaps.filter((g) => g > 100).length,
          p95: Math.round(p(0.95) * 10) / 10, p50: Math.round(p(0.5) * 10) / 10, max: Math.round(s[s.length - 1] || 0),
          dur: Math.round(t1 - t0), n_long: lt.length, tbt: Math.round(lt.reduce((a, x) => a + Math.max(0, x[1] - 50), 0)),
          loaf_top: Object.entries(by).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, v]) => [k, Math.round(v)]),
          worst: worst, final_y: Math.round(scrollY), H: document.documentElement.scrollHeight};
}
"""


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), 1) if xs else None


def metrics(cdp):
    return {m["name"]: m["value"] for m in cdp.send("Performance.getMetrics")["metrics"]}


def new_page(b, base, page, stub_feeds=True):
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True,
                        has_touch=True, user_agent=UA)
    ctx.add_init_script(INIT)
    pg = ctx.new_page()
    if stub_feeds and page == "podcast.html":
        pg.route("**/restless-king-e534.aninder.workers.dev/**", feed_stub)
    cdp = ctx.new_cdp_session(pg)
    cdp.send("Performance.enable")
    return ctx, pg, cdp


def feed_stub(route):
    u = route.request.url
    if "youtube.com" in u:
        ents = "".join(
            '<entry><id>yt:video:vid%02dAAAAAA</id><yt:videoId>vid%02dAAAAAA</yt:videoId><title>Synthetic video %d</title>'
            '<link rel="alternate" href="https://www.youtube.com/watch?v=vid%02dAAAAAA"/><published>2026-0%d-01T10:00:00+00:00</published>'
            '<media:group><media:thumbnail url="https://i.ytimg.com/vi/vid%02dAAAAAA/hqdefault.jpg" width="480" height="360"/></media:group></entry>'
            % (i, i, i, i, 1 + i % 9, i) for i in range(15))
        body = ('<?xml version="1.0"?><feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" '
                'xmlns:media="http://search.yahoo.com/mrss/" xmlns="http://www.w3.org/2005/Atom">' + ents + '</feed>')
    else:
        its = "".join(
            '<item><title>Synthetic episode %d with a long realistic title about thermals</title><link>https://example.org/e%d</link>'
            '<pubDate>Mon, 0%d Sep 2025 10:00:00 GMT</pubDate><description><![CDATA[<p>%s</p>]]></description>'
            '<enclosure url="https://d3ctxlq1ktw2nl.cloudfront.net/e%d.mp3" type="audio/mpeg" length="1"/>'
            '<itunes:image href="https://d3t3ozftmdmh3i.cloudfront.net/e%d.jpg"/><itunes:duration>01:%02d:00</itunes:duration></item>'
            % (i, i, 1 + i % 9, "Show notes sentence. " * 30, i, i, i % 60) for i in range(100))
        body = ('<?xml version="1.0"?><rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">'
                '<channel><title>Synthetic</title>' + its + '</channel></rss>')
    route.fulfill(status=200, content_type="application/xml", body=body,
                  headers={"access-control-allow-origin": "*"})


def goto(pg, url, timeout):
    t = time.time()
    try:
        pg.goto(url, wait_until="load", timeout=timeout)
        ok = True
    except Exception as e:  # noqa: BLE001
        ok = "timeout" if "Timeout" in str(e) else str(e)[:120]
    return ok, round(time.time() - t, 2)


# ------------------------------------------------------------------ phases
def phase_load(b, base, pages, rates, runs):
    out = {}
    for rate in rates:
        for run in range(runs):
            for p in pages:
                ctx, pg, cdp = new_page(b, base, p)
                cdp.send("Network.enable")
                cdp.send("Network.emulateNetworkConditions", FAST3G)
                cdp.send("Emulation.setCPUThrottlingRate", {"rate": rate})
                ok, wall = goto(pg, base + p, 30000)
                pg.wait_for_timeout(1500)
                try:
                    d = pg.evaluate(COLLECT_LOAD)
                except Exception as e:  # noqa: BLE001
                    d = {"error": str(e)[:200]}
                d.update(loaded=ok, wall=wall)
                out.setdefault(p, {}).setdefault(str(rate), []).append(d)
                print("load x%d run%d %-55s TBT %5s n%3s LCP %6s DCL %6s load %6s %s" % (
                    rate, run, p, d.get("tbt"), d.get("n_long"), d.get("lcp"), d.get("dcl"), d.get("load"), ok), flush=True)
                ctx.close()
    summ = {}
    for p, byr in out.items():
        for r, ds in byr.items():
            summ.setdefault(p, {})[r] = {k: med([d.get(k) for d in ds]) for k in
                                          ("tbt", "tbt_to_load", "n_long", "longest", "lcp", "dcl", "fcp", "load", "loaf_style_layout")}
    return {"runs": out, "median": summ}


def idle_window(pg, cdp, secs):
    pg.evaluate("() => { const P = window.__perf; P.trace = true; P.stacks = {}; P.r0 = P.raf; P.s0 = P.st; P.l0 = P.lt.length; }")
    m0 = metrics(cdp)
    time.sleep(secs)
    m1 = metrics(cdp)
    d = pg.evaluate("""() => { const P = window.__perf; P.trace = false;
        return {raf: P.raf - P.r0, st: P.st - P.s0, lt: P.lt.length - P.l0,
                stacks: Object.entries(P.stacks).sort((a, b) => b[1] - a[1]).slice(0, 6)}; }""")
    wall = m1["Timestamp"] - m0["Timestamp"]
    d.update(cpu_pct=round(100 * (m1["TaskDuration"] - m0["TaskDuration"]) / wall, 2),
             script_pct=round(100 * (m1["ScriptDuration"] - m0["ScriptDuration"]) / wall, 2),
             style_pct=round(100 * (m1["RecalcStyleDuration"] - m0["RecalcStyleDuration"]) / wall, 2),
             layout_pct=round(100 * (m1["LayoutDuration"] - m0["LayoutDuration"]) / wall, 2),
             recalc=int(m1["RecalcStyleCount"] - m0["RecalcStyleCount"]),
             layouts=int(m1["LayoutCount"] - m0["LayoutCount"]), wall=round(wall, 2))
    return d


def heap(pg, cdp):
    cdp.send("HeapProfiler.enable")
    for _ in range(2):
        cdp.send("HeapProfiler.collectGarbage")
    m = metrics(cdp)
    dc = cdp.send("Memory.getDOMCounters")
    el = pg.evaluate("document.getElementsByTagName('*').length")
    return {"heap_mb": round(m["JSHeapUsedSize"] / 1048576, 2), "nodes": dc["nodes"],
            "listeners": dc["jsEventListeners"], "elements": el, "documents": dc["documents"]}


def phase_scroll(b, base, pages, rate, runs, steps=30, wait=200):
    out = {}
    for run in range(runs):
        for p in pages:
            ctx, pg, cdp = new_page(b, base, p)
            cdp.send("Emulation.setCPUThrottlingRate", {"rate": rate})
            ok, wall = goto(pg, base + p, 30000)
            time.sleep(2.0)
            d = {"loaded": ok}
            d["idle_top"] = idle_window(pg, cdp, 5)
            d["scroll"] = pg.evaluate(SCROLL, [steps, wait])
            time.sleep(1.0)
            d["idle_bottom"] = idle_window(pg, cdp, 5)
            d["mem"] = heap(pg, cdp)
            out.setdefault(p, []).append(d)
            s = d["scroll"]
            print("scroll x%d run%d %-55s idleTop %5.1f%% idleBot %5.1f%% frames %3d >50 %2d >100 %2d p95 %5.1f max %4d heap %5.1f nodes %5d" % (
                rate, run, p, d["idle_top"]["cpu_pct"], d["idle_bottom"]["cpu_pct"], s["frames"], s["over50"], s["over100"],
                s["p95"], s["max"], d["mem"]["heap_mb"], d["mem"]["nodes"]), flush=True)
            ctx.close()
    summ = {}
    for p, ds in out.items():
        summ[p] = {
            "idle_top_cpu": med([d["idle_top"]["cpu_pct"] for d in ds]),
            "idle_top_raf_per_s": med([d["idle_top"]["raf"] / 5 for d in ds]),
            "idle_bottom_cpu": med([d["idle_bottom"]["cpu_pct"] for d in ds]),
            "idle_bottom_raf_per_s": med([d["idle_bottom"]["raf"] / 5 for d in ds]),
            "frames": med([d["scroll"]["frames"] for d in ds]),
            "over50": med([d["scroll"]["over50"] for d in ds]),
            "over100": med([d["scroll"]["over100"] for d in ds]),
            "p95": med([d["scroll"]["p95"] for d in ds]),
            "max": med([d["scroll"]["max"] for d in ds]),
            "scroll_tbt": med([d["scroll"]["tbt"] for d in ds]),
            "heap_mb": med([d["mem"]["heap_mb"] for d in ds]),
            "nodes": med([d["mem"]["nodes"] for d in ds]),
            "elements": med([d["mem"]["elements"] for d in ds]),
            "listeners": med([d["mem"]["listeners"] for d in ds]),
        }
    return {"rate": rate, "runs": out, "median": summ}


def phase_idle1x(b, base, pages, runs):
    out = {}
    for run in range(runs):
        for p in pages:
            ctx, pg, cdp = new_page(b, base, p)
            goto(pg, base + p, 30000)
            time.sleep(2.0)
            top = idle_window(pg, cdp, 5)
            pg.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            time.sleep(1.5)
            bot = idle_window(pg, cdp, 5)
            out.setdefault(p, []).append({"top": top, "bottom": bot})
            print("idle1x run%d %-55s top %5.2f%% (raf %d) bottom %5.2f%% (raf %d)" % (
                run, p, top["cpu_pct"], top["raf"], bot["cpu_pct"], bot["raf"]), flush=True)
            ctx.close()
    summ = {p: {"top": med([d["top"]["cpu_pct"] for d in ds]), "bottom": med([d["bottom"]["cpu_pct"] for d in ds]),
                "top_raf_s": med([d["top"]["raf"] / 5 for d in ds]), "bottom_raf_s": med([d["bottom"]["raf"] / 5 for d in ds])}
            for p, ds in out.items()}
    return {"runs": out, "median": summ}


# ---------------------------------------------------------------- interact
def center(pg, sel, idx=0):
    return pg.evaluate("""([s, i]) => { const el = document.querySelectorAll(s)[i]; if (!el) return null;
        const r = el.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2, r.width, r.height]; }""", [sel, idx])


def drag(pg, x, y, dx, dy, steps=6):
    pg.mouse.move(x, y)
    pg.mouse.down()
    for i in range(1, steps + 1):
        pg.mouse.move(x + dx * i / steps, y + dy * i / steps)
    pg.mouse.up()


def into_view(pg, sel):
    pg.evaluate("(s) => document.querySelector(s).scrollIntoView({block: 'center', behavior: 'instant'})", sel)


def sc_globe(pg, i):
    """Click a visible pin (fly + popup), drag-rotate, wheel zoom, click away."""
    pins = pg.evaluate("""() => { const c = document.getElementById('epMap').getBoundingClientRect();
        return [...document.querySelectorAll('#epMap g.pin')].filter(g => g.style.display !== 'none').map(g => {
          const r = g.querySelector('.pin-core').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; })
          .filter(([x, y]) => x > c.left + 20 && x < c.right - 20 && y > c.top + 20 && y < c.bottom - 20); }""")
    if pins:
        x, y = pins[i % len(pins)]
        pg.mouse.click(x, y)
        pg.wait_for_timeout(800)
        ok = pg.evaluate("document.getElementById('mapPopup').classList.contains('visible')")
    else:
        ok = False
    cx, cy, w, h = center(pg, "#epMap svg")
    drag(pg, cx - 60, cy + h * 0.3, 120, -20)
    pg.wait_for_timeout(150)
    pg.mouse.move(cx, cy)
    pg.mouse.wheel(0, -240)
    pg.wait_for_timeout(120)
    pg.mouse.wheel(0, 240)
    pg.wait_for_timeout(120)
    hx, hy, _, _ = center(pg, ".ep-map-section h2") or (10, 10, 0, 0)
    pg.mouse.click(hx, hy)
    pg.wait_for_timeout(100)
    return ok


def sc_rail(pg, i):
    """Drag the homepage episode marquee, then open a visible card in the episode modal and close it."""
    cx, cy, w, h = center(pg, ".episodes-viewport")
    drag(pg, cx + 100, cy, -180, 0)
    pg.wait_for_timeout(400)
    card = pg.evaluate("""() => { const vw = innerWidth; const c = [...document.querySelectorAll('.ep-track .ep-card')]
        .map(e => e.getBoundingClientRect()).filter(r => r.left > 5 && r.right < vw - 5)[0];
        return c ? [c.left + c.width / 2, c.top + c.height / 2] : null; }""")
    ok = False
    if card:
        pg.mouse.click(card[0], card[1])
        pg.wait_for_timeout(450)
        ok = pg.evaluate("!!document.querySelector('.ep-modal-overlay.active .kb-card, .ep-modal-overlay.active')")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(700)
    pg.mouse.move(2, 2)
    return ok


def sc_modal(pg, i):
    """Library: switch a filter pill, open an episode tile in the modal, close it."""
    pills = pg.evaluate("document.querySelectorAll('#bar .pill').length")
    if pills:
        pg.evaluate("(i) => document.querySelectorAll('#bar .pill')[i].click()", i % pills)
        pg.wait_for_timeout(150)
    n = pg.evaluate("document.querySelectorAll('[data-ep-slug]').length")
    if n:
        pg.evaluate("""(i) => { const t = [...document.querySelectorAll('[data-ep-slug]')]; const el = t[i % t.length];
            el.scrollIntoView({block: 'center', behavior: 'instant'}); }""", i)
        pg.wait_for_timeout(80)
        c = pg.evaluate("""(i) => { const t = [...document.querySelectorAll('[data-ep-slug]')]; const r = t[i % t.length].getBoundingClientRect();
            return [r.left + r.width / 2, r.top + Math.min(r.height / 2, 20)]; }""", i)
        pg.mouse.click(c[0], c[1])
        pg.wait_for_timeout(450)
        ok = pg.evaluate("!!document.querySelector('.ep-modal-overlay.active')")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(700)
        return ok
    return False


def sc_kenya_map(pg, i):
    """Select a pin, zoom in/out with the controls, drag the map."""
    n = pg.evaluate("document.querySelectorAll('.kmap .kmap-pin').length")
    into_view(pg, ".kmap-stage")
    if n:
        c = center(pg, ".kmap .kmap-pin", i % n)
        if c and c[2] > 0:
            pg.mouse.click(c[0], c[1])
            pg.wait_for_timeout(250)
    for z in ("in", "out"):
        c = center(pg, '.kmap-ctl [data-z="%s"]' % z)
        if c and c[2] > 0:
            pg.mouse.click(c[0], c[1])
            pg.wait_for_timeout(200)
    cx, cy, w, h = center(pg, ".kmap-stage")
    drag(pg, cx, cy, 60, 30)
    pg.wait_for_timeout(150)
    return bool(n)


def sc_kenya_gallery(pg, i):
    """Next, open the front card in the lightbox, step it, close it."""
    into_view(pg, ".cfl-stage")
    c = center(pg, ".cfl-next")
    if c and c[2] > 0:
        pg.mouse.click(c[0], c[1])
        pg.wait_for_timeout(900)
    cx, cy, w, h = center(pg, ".cfl-stage")
    fc = center(pg, ".cfl-card.is-front")
    if fc:
        pg.mouse.click(fc[0], fc[1])
    pg.wait_for_timeout(400)
    ok = pg.evaluate("!!document.querySelector('.cfl-lb') && !document.querySelector('.cfl-lb').hidden")
    if ok:
        nb = center(pg, ".cfl-lb-next")
        if nb and nb[2] > 0:
            pg.mouse.click(nb[0], nb[1])
            pg.wait_for_timeout(250)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(300)
    drag(pg, cx + 80, cy, -160, 0)
    pg.wait_for_timeout(300)
    return ok


def sc_podcast(pg, i):
    """Drag the video rail and the testimonials rail; open/close a video card (iframe to blocked host)."""
    for sel in (".yt-rail", ".testimonials-wrap"):
        if pg.evaluate("(s) => !!document.querySelector(s)", sel):
            into_view(pg, sel)
            c = center(pg, sel)
            drag(pg, c[0] + 100, c[1], -160, 0)
            pg.wait_for_timeout(450)
    pg.mouse.move(2, 2)


def sc_nav(pg, i):
    """Open and close the phone menu."""
    c = center(pg, ".nav-toggle")
    if c and c[2] > 0:
        pg.mouse.click(c[0], c[1])
        pg.wait_for_timeout(350)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(250)
        if pg.evaluate("document.querySelector('.nav-toggle').getAttribute('aria-expanded') === 'true'"):
            pg.mouse.click(c[0], c[1])
            pg.wait_for_timeout(250)


SCEN = {
    "globe": ("index.html", "#epMap", sc_globe),
    "rail": ("index.html", ".episodes-viewport", sc_rail),
    "modal": ("library.html#all", None, sc_modal),
    "kenya_map": ("destinations/kenya.html", ".kmap-stage", sc_kenya_map),
    "kenya_gallery": ("destinations/kenya.html", ".cfl-stage", sc_kenya_gallery),
    "podcast": ("podcast.html", None, sc_podcast),
    "nav": ("index.html", None, sc_nav),
}


def phase_interact(b, base, names, batches, reps=20):
    out = {}
    for name in names:
        page, view, fn = SCEN[name]
        ctx, pg, cdp = new_page(b, base, page)
        goto(pg, base + page, 30000)
        time.sleep(1.5)
        if view:
            into_view(pg, view)
            time.sleep(1.5)
        h0 = heap(pg, cdp)
        fn(pg, 0)                           # one warm-up use: lazy one-time allocations
        time.sleep(1.0)
        hw = heap(pg, cdp)
        res = {"page": page, "base": h0, "warm": hw, "batches": [], "errors": []}
        prev = hw
        for bi in range(batches):
            t = time.time()
            for i in range(reps):
                try:
                    if fn(pg, i + 1 + bi * reps):
                        res["hits"] = res.get("hits", 0) + 1
                except Exception as e:  # noqa: BLE001
                    res["errors"].append(str(e)[:160])
            time.sleep(1.0)
            h = heap(pg, cdp)
            h["growth_mb"] = round(h["heap_mb"] - prev["heap_mb"], 2)
            h["node_growth"] = h["nodes"] - prev["nodes"]
            h["listener_growth"] = h["listeners"] - prev["listeners"]
            h["secs"] = round(time.time() - t, 1)
            res["batches"].append(h)
            prev = h
            print("interact %-14s hits %3s batch%d heap %6.2f MB (%+.2f) nodes %6d (%+d) listeners %5d (%+d) %.1fs" % (
                name, res.get("hits", 0), bi, h["heap_mb"], h["growth_mb"], h["nodes"], h["node_growth"], h["listeners"],
                h["listener_growth"], h["secs"]), flush=True)
        res["total_growth_mb"] = round(prev["heap_mb"] - hw["heap_mb"], 2)
        res["median_batch_growth_mb"] = med([x["growth_mb"] for x in res["batches"]])
        res["median_batch_node_growth"] = med([x["node_growth"] for x in res["batches"]])
        res["median_batch_listener_growth"] = med([x["listener_growth"] for x in res["batches"]])
        res["console_errors"] = []
        out[name] = res
        ctx.close()
    return out


# ----------------------------------------------------------------- ablate
ABL = {
    "none": "",
    "smil": "document.querySelectorAll('svg').forEach((s) => s.pauseAnimations && s.pauseAnimations())",
    "css": "document.getAnimations().forEach((a) => a.pause())",
}
ABL_SETS = {
    "index.html": ["none", "smil", "raf:homepage-motion.js", "smil+raf:homepage-motion.js",
                   "smil+raf:homepage-motion.js+raf:ScrollTrigger+css"],
    "destinations/kenya.html": ["none", "raf:kenya-gallery.js", "css", "raf:kenya-gallery.js+css"],
    "podcast.html": ["none", "raf:podcast.html", "raf:youtube-feed.js", "raf:podcast.html+raf:youtube-feed.js",
                     "raf:podcast.html+raf:youtube-feed.js+css"],
}


def apply_ablation(pg, spec):
    blocks = []
    for part in spec.split("+"):
        if part.startswith("raf:"):
            blocks.append(part[4:])
        elif ABL.get(part):
            pg.evaluate("() => { " + ABL[part] + " }")
    if blocks:
        pg.evaluate("(b) => { window.__perf.block = b; }", blocks)


def phase_ablate(b, base, pages, rate, runs, where):
    """Idle CPU with one suspected animation source switched off at a time (in the test browser only)."""
    out = {}
    for p in pages:
        for spec in ABL_SETS.get(p, ["none", "css", "smil"]):
            for pos in where:
                vals = []
                for run in range(runs):
                    ctx, pg, cdp = new_page(b, base, p)
                    cdp.send("Emulation.setCPUThrottlingRate", {"rate": rate})
                    goto(pg, base + p, 30000)
                    time.sleep(1.5)
                    if pos == "bottom":
                        pg.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
                    time.sleep(1.0)
                    apply_ablation(pg, spec)
                    time.sleep(0.5)
                    d = idle_window(pg, cdp, 5)
                    vals.append(d)
                    ctx.close()
                r = {"cpu": med([v["cpu_pct"] for v in vals]), "style": med([v["style_pct"] for v in vals]),
                     "recalc": med([v["recalc"] for v in vals]), "layouts": med([v["layouts"] for v in vals]),
                     "raf_s": med([v["raf"] / 5 for v in vals]), "runs": [v["cpu_pct"] for v in vals]}
                out.setdefault(p, {}).setdefault(pos, {})[spec] = r
                print("ablate x%d %-28s %-6s %-55s idle CPU %5.1f%% (runs %s) style %5.1f%% recalcs %s rAF/s %s" % (
                    rate, p, pos, spec, r["cpu"], r["runs"], r["style"], r["recalc"], r["raf_s"]), flush=True)
    return out


# -------------------------------------------------------------------- inp
EVT_INSTALL = r"""() => {
  window.__evt = [];
  new PerformanceObserver((l) => { for (const e of l.getEntries()) if (e.interactionId)
      window.__evt.push({id: e.interactionId, n: e.name, s: e.startTime, ps: e.processingStart, pe: e.processingEnd, d: e.duration}); })
    .observe({type: 'event', durationThreshold: 16, buffered: false});
  window.__doorGone = null;
  new MutationObserver(() => { if (!document.documentElement.classList.contains('iris-on') && window.__doorGone === null)
      window.__doorGone = performance.now(); }).observe(document.documentElement, {attributes: true, attributeFilter: ['class']});
}"""
EVT_COLLECT = r"""() => {
  const by = {};
  for (const e of window.__evt) { const g = by[e.id] || (by[e.id] = {d: 0, delay: 1e9, s: 1e12}); g.d = Math.max(g.d, e.d);
    g.delay = Math.min(g.delay, e.ps - e.s); g.s = Math.min(g.s, e.s); }
  window.__evt = [];
  return Object.values(by).map((g) => ({d: Math.round(g.d), delay: Math.round(g.delay), s: Math.round(g.s)}));
}"""
SAFE_SPOT = r"""() => {
  const bad = 'a,button,input,select,textarea,label,summary,video,iframe,[role=button],[onclick],[data-ep-slug],[tabindex],svg,canvas,.ep-map,.yt-rail,.testimonials-wrap,.episodes-viewport,.cfl,.kmap';
  for (let y = 300; y < innerHeight - 60; y += 37) for (let x = 40; x < innerWidth - 40; x += 31) {
    const el = document.elementFromPoint(x, y); if (el && !el.closest(bad)) return [x, y];
  }
  return null;
}"""


def taps(pg, n=5, gap=700):
    pt = pg.evaluate(SAFE_SPOT)
    if not pt:
        return None
    for _ in range(n):
        pg.touchscreen.tap(pt[0], pt[1])
        pg.wait_for_timeout(gap)
    ev = pg.evaluate(EVT_COLLECT)
    ds = [e["d"] for e in ev]
    return {"n_reported": len(ev), "taps": n, "max": max(ds) if ds else "<16", "median": med(ds + [16] * (n - len(ds))),
            "delays": [e["delay"] for e in ev], "durations": ds, "spot": pt}


def phase_inp(b, base, pages, rate, runs):
    """Tap responsiveness (Event Timing: input delay + duration) at CPU 4x on a neutral spot, top and after scroll.
    knowledge-base.html without a hash: the first-visit door; tap its core and time until the page is open."""
    out = {}
    for p in pages:
        for run in range(runs):
            ctx, pg, cdp = new_page(b, base, p)
            cdp.send("Emulation.setCPUThrottlingRate", {"rate": rate})
            goto(pg, base + p, 30000)
            time.sleep(2.0)
            pg.evaluate(EVT_INSTALL)
            d = {}
            if p == "knowledge-base.html" and pg.evaluate("document.documentElement.classList.contains('iris-on')"):
                c = center(pg, "#irisCore")
                t_tap = pg.evaluate("performance.now()")
                pg.touchscreen.tap(c[0], c[1])
                for _ in range(100):
                    if pg.evaluate("window.__doorGone !== null"):
                        break
                    time.sleep(0.1)
                gone = pg.evaluate("window.__doorGone")
                ev = pg.evaluate(EVT_COLLECT)
                d["door"] = {"tap_to_open_ms": round(gone - t_tap) if gone else None,
                             "tap_event": ev[:3]}
                time.sleep(1.0)
                pg.evaluate(EVT_INSTALL)
            d["top"] = taps(pg)
            if pg.evaluate("!!document.querySelector('.kvario')"):
                into_view(pg, ".kvario")     # a reader passing the vario on the way down (under 1.7 s)
                time.sleep(0.5)
            pg.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            time.sleep(1.5)
            d["bottom"] = taps(pg)
            out.setdefault(p, []).append(d)
            print("inp x%d run%d %-30s %s top %s bottom %s" % (rate, run, p,
                  ("door %s ms" % d["door"]["tap_to_open_ms"]) if "door" in d else "",
                  d["top"] and (d["top"]["median"], d["top"]["max"], d["top"]["delays"]),
                  d["bottom"] and (d["bottom"]["median"], d["bottom"]["max"], d["bottom"]["delays"])), flush=True)
            ctx.close()
    summ = {}
    for p, ds in out.items():
        summ[p] = {"top_median": med([x["top"]["median"] for x in ds if x["top"]]),
                   "top_max": med([x["top"]["max"] if isinstance(x["top"]["max"], int) else 16 for x in ds if x["top"]]),
                   "bottom_median": med([x["bottom"]["median"] for x in ds if x["bottom"]]),
                   "bottom_max": med([x["bottom"]["max"] if isinstance(x["bottom"]["max"], int) else 16 for x in ds if x["bottom"]])}
        if any("door" in x for x in ds):
            summ[p]["door_tap_to_open_ms"] = med([x["door"]["tap_to_open_ms"] for x in ds if "door" in x])
    return {"runs": out, "median": summ}


# ------------------------------------------------------------------ vario
def phase_vario(b, base, rate, runs, pages=("destinations/kenya.html", "destinations/india.html")):
    """Vario needle (.kvario): pass it in under 1.7 s (fast scroller) vs dwell 2.5 s, then idle with it off screen."""
    out = {}
    for p in pages:
        for dwell in (500, 2500):
            for run in range(runs):
                ctx, pg, cdp = new_page(b, base, p)
                cdp.send("Emulation.setCPUThrottlingRate", {"rate": rate})
                goto(pg, base + p, 30000)
                time.sleep(1.5)
                into_view(pg, ".kvario")
                time.sleep(dwell / 1000)
                pg.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
                time.sleep(1.5)
                vis = pg.evaluate("(() => { const r = document.querySelector('.kvario').getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; })()")
                d = idle_window(pg, cdp, 5)
                d["vario_on_screen"] = vis
                d["drift_raf"] = sum(c for k, c in d["stacks"] if k.startswith("drift (destinations/"))
                out.setdefault(p, {}).setdefault(str(dwell), []).append(d)
                print("vario x%d %-24s dwell %4d ms run%d: on screen=%s, idle CPU %5.1f%%, style %5.1f%%, drift rAF calls in 5 s: %d, stacks %s" % (
                    rate, p, dwell, run, vis, d["cpu_pct"], d["style_pct"], d["drift_raf"], d["stacks"][:3]), flush=True)
                ctx.close()
    return {p: {k: {"cpu": med([x["cpu_pct"] for x in v]), "style": med([x["style_pct"] for x in v]),
                    "drift_raf": med([x["drift_raf"] for x in v]), "runs": v} for k, v in byd.items()} for p, byd in out.items()}


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    phase = a[0]
    opts, pos = {}, []
    i = 1
    while i < len(a):
        if a[i].startswith("--"):
            opts[a[i][2:]] = a[i + 1]
            i += 2
        else:
            pos.append(a[i])
            i += 1
    runs = int(opts.get("runs", 3))
    tag = opts.get("tag", "") or ("" if not pos else "custom")
    t = time.time()
    with lib.server(PORT) as base:
        with lib.browser(**LAUNCH) as b:
            if phase == "load":
                rates = [int(x) for x in opts.get("rates", "4,6").split(",")]
                res = phase_load(b, base, pos or lib.TEMPLATES["live"], rates, runs)
            elif phase == "scroll":
                res = phase_scroll(b, base, pos or lib.TEMPLATES["live"], int(opts.get("rate", 4)), runs)
            elif phase == "idle1x":
                res = phase_idle1x(b, base, pos or lib.TEMPLATES["live"], runs)
            elif phase == "ablate":
                res = phase_ablate(b, base, pos or list(ABL_SETS), int(opts.get("rate", 4)), runs,
                                   opts.get("where", "top,bottom").split(","))
            elif phase == "inp":
                res = phase_inp(b, base, pos or ["index.html", "podcast.html", "destinations/kenya.html", "knowledge-base.html",
                                                 "knowledge-base.html#x", "enquire.html"], int(opts.get("rate", 4)), runs)
            elif phase == "vario":
                res = phase_vario(b, base, int(opts.get("rate", 4)), runs, pos or ("destinations/kenya.html", "destinations/india.html"))
            elif phase == "interact":
                res = phase_interact(b, base, pos or ["globe", "rail", "modal", "kenya_map", "kenya_gallery"], runs, int(opts.get("reps", 20)))
            else:
                raise SystemExit("unknown phase " + phase)
    res["elapsed_s"] = round(time.time() - t, 1)
    fp = os.path.join(HERE, "out_%s%s.json" % (phase, ("_" + tag) if tag else ""))
    with open(fp, "w") as f:
        json.dump(res, f, indent=1, default=str)
    print("wrote", fp, "in", res["elapsed_s"], "s")


if __name__ == "__main__":
    main()
