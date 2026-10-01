"""Diagnostic: scroll jank on the knowledge base pages at CPU 4x, as-is and with one cause removed at a time
(test browser only; repo untouched). Usage: python3 fixsim.py [pages...]"""
import sys, time, statistics as st
sys.path.insert(0, "/home/user/Website/tools/stress/perf")
import perf, lib
pages = sys.argv[1:] or ["knowledge-base.html#x", "knowledge-base/navigators.html"]
TEXT2DATA = r"""() => { const d = Object.getOwnPropertyDescriptor(Node.prototype, 'textContent');
  Object.defineProperty(Node.prototype, 'textContent', {configurable: true, get: d.get, set(v) {
    if (this.childNodes.length === 1 && this.firstChild.nodeType === 3) this.firstChild.data = v; else d.set.call(this, v); }}); }"""
NOHAS = r"""() => { function walk(list, owner) { for (let i = list.length - 1; i >= 0; i--) { const r = list[i];
      if (r.selectorText && r.selectorText.includes(':has(')) owner.deleteRule(i); else if (r.cssRules) walk(r.cssRules, r); } }
  for (const sh of document.styleSheets) { try { walk(sh.cssRules, sh); } catch (e) {} } }"""
def variants(p):
    own = p.split("#")[0].split("/")[-1]
    return {"as-is": [], "textContent->text node data": [TEXT2DATA], "no :has() rules": [NOHAS],
            "page scroll rAF blocked (raf:%s)" % own: ["BLOCK:" + own]}
with lib.server(perf.PORT) as base:
    with lib.browser(**perf.LAUNCH) as b:
        for p in pages:
            for name, acts in variants(p).items():
                rs = []
                for run in range(2):
                    ctx, pg, cdp = perf.new_page(b, base, p)
                    cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
                    perf.goto(pg, base + p, 30000)
                    time.sleep(1.5)
                    for a in acts:
                        if a.startswith("BLOCK:"):
                            pg.evaluate("(b) => { window.__perf.block = [b]; }", a[6:])
                        else:
                            pg.evaluate(a)
                    time.sleep(0.5)
                    rs.append(pg.evaluate(perf.SCROLL, [30, 200]))
                    ctx.close()
                print("%-36s %-44s frames>50 %s  >100 %s  p95 %s  max %s  TBT %s" % (p, name, [r["over50"] for r in rs],
                      [r["over100"] for r in rs], [r["p95"] for r in rs], [r["max"] for r in rs], [r["tbt"] for r in rs]), flush=True)
