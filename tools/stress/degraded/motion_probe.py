#!/usr/bin/env python3
"""prefers-reduced-motion: reduce on index.html: what still moves at rest? Frame diffs at several scroll positions,
which elements sit under the changed pixels, and which functions keep requesting animation frames.
usage: python3 motion_probe.py [page]    Port 8814. Read-only on the repo."""
import io, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lib
from degraded import new_ctx, goto, HELPERS
page = sys.argv[1] if len(sys.argv) > 1 else "index.html"
INIT = r"""(() => { window.__rafSrc = {}; const o = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) { const k = (cb.name || '') + ':' + String(cb).replace(/\s+/g, ' ').slice(0, 90);
    window.__rafSrc[k] = (window.__rafSrc[k] || 0) + 1; return o(cb); }; })();"""
def regions(a, b):
    import numpy as np
    from scipy import ndimage  # noqa
    return None
with lib.server(8814) as base:
    with lib.browser() as b:
        import numpy as np
        from PIL import Image
        ctx = new_ctx(b, base, reduced_motion="reduce")
        ctx.add_init_script(HELPERS); ctx.add_init_script(INIT)
        pg = ctx.new_page(); goto(pg, base + page); time.sleep(3)
        pg.evaluate("window.__rafSrc = {}"); time.sleep(2)
        src = pg.evaluate("window.__rafSrc")
        print("rAF requests in 2 s at rest (reduced motion):")
        for k, v in sorted(src.items(), key=lambda kv: -kv[1])[:6]: print("   %4d  %s" % (v, k))
        H = pg.evaluate("document.documentElement.scrollHeight")
        for y in range(0, H, 900):
            pg.evaluate("y => window.scrollTo({top: y, behavior: 'instant'})", y); time.sleep(1.2)
            a = np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert("L"), dtype=np.int16); time.sleep(1.0)
            c = np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert("L"), dtype=np.int16)
            d = np.abs(a - c) > 12
            if d.mean() > 0.0005:
                # coarse grid of changed cells -> elements under them
                cells = set()
                for gy in range(0, d.shape[0], 60):
                    for gx in range(0, d.shape[1], 80):
                        if d[gy:gy+60, gx:gx+80].mean() > 0.05: cells.add((gx + 40, gy + 30))
                under = pg.evaluate("""pts => { const {P} = window.__dg; const m = {}; for (const [x, y] of pts) { const e = document.elementFromPoint(x, y); if (e) { const k = P(e); m[k] = (m[k] || 0) + 1; } } return m; }""", list(cells))
                print("scrollY=%5d changed=%.1f%% of viewport; elements under changed cells: %s" % (y, 100 * d.mean(), sorted(under.items(), key=lambda kv: -kv[1])[:4]))
        ctx.close()
