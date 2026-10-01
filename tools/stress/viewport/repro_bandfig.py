#!/usr/bin/env python3
"""KB band figures: is the absolutely positioned caption (.bf-q) cut off by the figure's overflow:hidden?
python3 repro_bandfig.py [page,...] [--sizes 1280x800,1440x900,1920x1080,2560x1440,3840x2160]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lib
from run_viewport import router, PORT
args = [a for a in sys.argv[1:] if not a.startswith("--")]
pages = args[0].split(",") if args else ["knowledge-base/storytellers.html", "knowledge-base/weather-patterns.html", "knowledge-base/sky-gods.html"]
sizes = "1280x800,1440x900,1920x1080,2560x1440,3840x2160"
for a in sys.argv[1:]:
    if a.startswith("--sizes="): sizes = a.split("=", 1)[1]
JS = r"""async () => {
  const out = [];
  for (const f of document.querySelectorAll('figure.band-fig')) {
    f.scrollIntoView({block: 'center', behavior: 'instant'});
    await new Promise(r => setTimeout(r, +(new URLSearchParams(location.search).get("wait") || 3000)));
    const q = f.querySelector('.bf-q'); if (!q) continue;
    const fr = f.getBoundingClientRect(), qr = q.getBoundingClientRect();
    const lost = [...q.children].filter(c => { const r = c.getBoundingClientRect(); return r.bottom > fr.bottom + 2 || r.top < fr.top - 2; })
      .map(c => c.className + ': ' + c.textContent.trim().replace(/\s+/g, ' ').slice(0, 40));
    out.push({figH: Math.round(fr.height), capH: Math.round(qr.height), capTopInFig: Math.round(qr.top - fr.top), overBottom: Math.round(qr.bottom - fr.bottom),
      overTop: Math.round(fr.top - qr.top), transform: getComputedStyle(q).transform, cutChildren: lost});
  }
  return out;
}"""
with lib.server(PORT) as base, lib.browser() as b:
    for p in pages:
        for s in sizes.split(","):
            w, h = map(int, s.split("x"))
            ctx = b.new_context(viewport={"width": w, "height": h}); ctx.route("**/*", router(base))
            pg = ctx.new_page(); pg.goto(base + p + "?wait=" + os.environ.get("WAIT", "3000"), wait_until="load"); pg.wait_for_timeout(400)
            for i, r in enumerate(pg.evaluate(JS)):
                if r["overBottom"] > 2 or r["overTop"] > 2:
                    print(p, s, "fig", i, r)
                else:
                    print(p, s, "fig", i, "ok (figH %d capH %d)" % (r["figH"], r["capH"]))
            ctx.close()
