#!/usr/bin/env python3
"""Episode chapter rail (aside.cd-rail, position:sticky) sliding over the full-width .cd-side boxes.

For each width x height, scrolls in 40px steps through the episode and records the largest overlap between
the rail and any .cd-side > .cd-box, and how many chapter links are hit-tested as covered at that point.

python3 repro_rail.py [page ...] [--sizes 844x390,1024x768,1100x800,1150x900,1151x900,1280x800]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib  # noqa: E402
from run_viewport import router, PORT  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
sizes = "844x390,1024x768,1100x800,1150x900,1151x900,1280x800"
for a in sys.argv[1:]:
    if a.startswith("--sizes="):
        sizes = a.split("=", 1)[1]
pages = args or ["episodes/sky-gods-flying-8000ers-antoine-girard.html"]
JS = r"""() => {
  const rail = document.querySelector('aside.cd-rail'); if (!rail || !rail.querySelector('.cd-chap')) return {noRail: true};
  const boxes = [...document.querySelectorAll('aside.cd-side > .cd-box')];
  const H = document.documentElement.scrollHeight - innerHeight; let best = {area: 0};
  for (let y = 0; y <= H; y += 40) {
    window.scrollTo({top: y, behavior: 'instant'});
    const r = rail.getBoundingClientRect();
    for (const b of boxes) { const q = b.getBoundingClientRect();
      const w = Math.min(r.right, q.right) - Math.max(r.left, q.left), h = Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top, 0);
      if (w > 0 && h > 0 && w * h > best.area) {
        let cov = 0, n = 0;
        for (const a of rail.querySelectorAll('.cd-chap')) { const c = a.getBoundingClientRect(); const cy = (c.top + c.bottom) / 2, cx = (c.left + c.right) / 2;
          if (cy < 0 || cy > innerHeight) continue; n++; const hit = document.elementFromPoint(cx, cy); if (hit && !a.contains(hit) && hit !== a) cov++; }
        best = {area: Math.round(w * h), scrollY: y, overlapW: Math.round(w), overlapH: Math.round(h), box: (b.textContent || '').trim().slice(0, 30),
          railPos: getComputedStyle(rail).position, chapsInView: n, chapsCovered: cov}; }
    }
  }
  return best;
}"""
with lib.server(PORT) as base, lib.browser() as b:
    for p in pages:
        for s in sizes.split(","):
            w, h = map(int, s.split("x"))
            ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=w < 900, has_touch=w < 900)
            ctx.route("**/*", router(base))
            pg = ctx.new_page()
            pg.goto(base + p, wait_until="load")
            pg.wait_for_timeout(500)
            print(p, s, pg.evaluate(JS))
            ctx.close()
