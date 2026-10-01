"""What moves the nav 6px on phones under a slow network? python3 probe_nav_shift.py [page]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib
page = sys.argv[1] if len(sys.argv) > 1 else "tags/safety.html"
INIT = r"""
window.__log = [];
const t0 = performance.now();
function snap(tag) {
  const n = document.querySelector('nav'); const c = document.querySelector('.nav-cta');
  if (!n) return;
  const r = n.getBoundingClientRect(), rc = c ? c.getBoundingClientRect() : {y:0,height:0};
  const cs = getComputedStyle(n);
  window.__log.push([Math.round(performance.now()), tag, Math.round(r.height*10)/10, Math.round(rc.y*10)/10, Math.round(rc.height*10)/10,
    cs.paddingTop, cs.position, cs.fontFamily.slice(0,20), document.fonts ? document.fonts.status : '', n.className,
    document.querySelectorAll('link[rel=stylesheet]').length, document.styleSheets.length]);
}
new MutationObserver(ms => { for (const m of ms) { const t = m.target; const d = (t.tagName||'#') + (t.id?'#'+t.id:'') + (t.className&&typeof t.className==='string'?'.'+t.className.split(' ')[0]:''); snap('mut ' + m.type + ' ' + d + ' ' + (m.attributeName||'') + ' +' + [...m.addedNodes].map(n => n.nodeName + (n.className&&typeof n.className==='string'?'.'+n.className.split(' ')[0]:'')).join(',').slice(0,80)); } }).observe(document, {subtree: true, childList: true, attributes: true, attributeFilter: ['class', 'style']});
const iv = setInterval(() => snap('tick'), 100); setTimeout(() => clearInterval(iv), 6000);
new PerformanceObserver(l => { for (const e of l.getEntries()) snap('SHIFT ' + e.value.toFixed(4)); }).observe({type: 'layout-shift', buffered: true});
"""
with lib.server(8816) as base:
    with lib.browser() as b:
        ctx = b.new_context(viewport={"width": 390, "height": 844})
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        ctx.add_init_script(INIT)
        pg = ctx.new_page()
        reqs = []
        pg.on("requestfinished", lambda r: reqs.append((r.url[len(base):][:60], round(r.timing["responseEnd"]))) if r.url.startswith(base) else None)
        cdp = ctx.new_cdp_session(pg)
        cdp.send("Network.enable")
        cdp.send("Network.emulateNetworkConditions", dict(offline=False, latency=150, downloadThroughput=200000, uploadThroughput=90000))
        pg.goto(base + page, wait_until="load")
        pg.wait_for_timeout(2500)
        log = pg.evaluate("() => window.__log")
        last = None
        for row in log:
            key = tuple(row[2:])
            if key != last or row[1].startswith("SHIFT") or (1300 < row[0] < 1700 and not row[1].startswith('tick')):
                print(row)
            last = key
        print("requests (url, responseEnd ms since request start):")
        for r in reqs: print("  ", r)
