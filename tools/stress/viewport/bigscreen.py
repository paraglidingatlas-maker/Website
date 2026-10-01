#!/usr/bin/env python3
"""Line length and type size at 2560x1440 and 3840x2160 (DSF 1).
Measures, for every visible text block (p, li, dd, blockquote, figcaption) with >= 80 characters, the real
characters per line: widest rendered line in px / average glyph advance of that block (sum of line widths /
characters). Flags blocks whose lines exceed 120 characters, and reports body/paragraph font sizes.

python3 bigscreen.py [--pages all|templates|a.html,b.html] [--sizes 2560x1440,3840x2160] [--out FILE]
"""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib  # noqa: E402
from run_viewport import router, PORT  # noqa: E402

JS = r"""() => {
  const vis = e => !e.checkVisibility || e.checkVisibility({opacityProperty: true, visibilityProperty: true});
  const sel = el => { const p = []; let e = el; for (let i = 0; i < 4 && e && e.nodeType === 1; i++) {
      let s = e.tagName.toLowerCase(); if (e.id) { p.unshift(s + '#' + e.id); break; }
      const c = [...e.classList].slice(0, 2); if (c.length) s += '.' + c.join('.'); p.unshift(s); e = e.parentElement; } return p.join(' > '); };
  const rg = document.createRange(); const out = [];
  for (const el of document.querySelectorAll('p,li,dd,blockquote,figcaption')) {
    if (el.querySelector('p,li,dd,blockquote,ul,ol')) continue;
    const t = (el.textContent || '').replace(/\s+/g, ' ').trim(); if (t.length < 80 || !vis(el)) continue;
    rg.selectNodeContents(el);
    const rs = [...rg.getClientRects()].filter(r => r.width > 1 && r.height > 1); if (!rs.length) continue;
    const lines = []; // merge rects on the same line
    for (const r of rs) { const m = (r.top + r.bottom) / 2; const L = lines.find(l => Math.abs(l.m - m) < r.height / 2);
      if (L) { L.l = Math.min(L.l, r.left); L.r = Math.max(L.r, r.right); } else lines.push({m, l: r.left, r: r.right}); }
    const widths = lines.map(l => l.r - l.l); const sum = widths.reduce((a, b) => a + b, 0);
    const adv = sum / t.length; const widest = Math.max(...widths);
    const cpl = Math.round(widest / adv);
    out.push({sel: sel(el), chars: t.length, lines: lines.length, cpl, wpx: Math.round(widest), fs: parseFloat(getComputedStyle(el).fontSize),
      text: t.slice(0, 50)});
  }
  const ps = out.map(o => o.fs).sort((a, b) => a - b);
  return {vw: innerWidth, bodyFont: parseFloat(getComputedStyle(document.body).fontSize), rootFont: parseFloat(getComputedStyle(document.documentElement).fontSize),
    blocks: out.length, fsMedian: ps.length ? ps[Math.floor(ps.length / 2)] : null, fsMin: ps[0] || null,
    long: out.filter(o => o.cpl > 120).sort((a, b) => b.cpl - a.cpl).slice(0, 8), nLong: out.filter(o => o.cpl > 120).length,
    maxCpl: out.length ? Math.max(...out.map(o => o.cpl)) : null};
}"""
SIZES = {"2560x1440": (2560, 1440), "3840x2160": (3840, 2160)}


def worker(tasks, base, q):
    with lib.browser(args=["--disable-gpu"]) as b:
        for path, s in tasks:
            w, h = SIZES[s]
            ctx = b.new_context(viewport={"width": w, "height": h})
            ctx.route("**/*", router(base))
            pg = ctx.new_page()
            rec = {"page": path, "size": s}
            try:
                pg.goto(base + path, wait_until="load", timeout=30000)
                pg.wait_for_timeout(500)
                if pg.query_selector("#irisSkip"):
                    pg.wait_for_timeout(2500)
                    pg.evaluate("document.getElementById('irisSkip') && document.getElementById('irisSkip').click()")
                    pg.wait_for_timeout(1500)
                mx = pg.evaluate("document.documentElement.scrollHeight - innerHeight")
                for y in range(0, mx + h, h):
                    pg.evaluate("y => window.scrollTo({top:y,behavior:'instant'})", y)
                    pg.wait_for_timeout(60)
                pg.wait_for_timeout(300)
                rec.update(pg.evaluate(JS))
            except Exception as e:  # noqa: BLE001
                rec["error"] = str(e)[:200]
            ctx.close()
            q.put(rec)
    q.put(None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="all")
    ap.add_argument("--sizes", default="2560x1440,3840x2160")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=os.path.join(HERE, "results_bigscreen.json"))
    a = ap.parse_args()
    pages = lib.pages("live") if a.pages == "all" else lib.TEMPLATES["live"] if a.pages == "templates" else a.pages.split(",")
    tasks = [(p, s) for s in a.sizes.split(",") for p in pages]
    n = min(a.workers, len(tasks))
    res = []
    t0 = time.time()
    with lib.server(PORT) as base:
        c = mp.get_context("spawn")
        q = c.Queue()
        ps = [c.Process(target=worker, args=(tasks[i::n], base, q)) for i in range(n)]
        for p in ps:
            p.start()
        done = 0
        while done < n:
            r = q.get()
            if r is None:
                done += 1
            else:
                res.append(r)
        for p in ps:
            p.join(10)
    json.dump(res, open(a.out, "w"), indent=1)
    print("wrote", a.out, len(res), "in %.0fs" % (time.time() - t0))
    for s in a.sizes.split(","):
        xs = [r for r in res if r["size"] == s and not r.get("error")]
        lg = [r for r in xs if r.get("nLong")]
        print("%s: %d pages, %d with a text block over 120 chars/line; body font %s; median block font <14px on %d pages" % (
            s, len(xs), len(lg), sorted(set(r["bodyFont"] for r in xs)), sum(1 for r in xs if r["fsMedian"] and r["fsMedian"] < 14)))
        for r in sorted(lg, key=lambda r: -r["maxCpl"])[:12]:
            print("   %-60s max %d cpl; %s" % (r["page"], r["maxCpl"], "; ".join("%s cpl=%d lines=%d fs=%s" % (l["sel"][-45:], l["cpl"], l["lines"], l["fs"]) for l in r["long"][:2])))


if __name__ == "__main__":
    main()
