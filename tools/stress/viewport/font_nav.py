#!/usr/bin/env python3
"""Browser text size (Chrome Settings > Font size, via CDP Page.setFontSizes) vs the header CTA and the footer.

For each page, viewport and default font size, reports whether the nav 'Enquire Now' CTA and the footer's
right-most link are inside the viewport and hit-testable, and document scrollWidth.
python3 font_nav.py [page,...] [--shots]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib  # noqa: E402
from run_viewport import router, PORT  # noqa: E402

pages = [a for a in sys.argv[1:] if not a.startswith("--")]
pages = pages[0].split(",") if pages else ["index.html", "library.html", "episodes/sky-gods-flying-8000ers-antoine-girard.html"]
shots = "--shots" in sys.argv
JS = r"""() => {
  const q = (sel) => { const e = document.querySelector(sel); if (!e) return null; const r = e.getBoundingClientRect();
    const cx = Math.min(Math.max((r.left + r.right) / 2, 0), innerWidth - 1), cy = (r.top + r.bottom) / 2;
    const vis = r.left >= -1 && r.right <= innerWidth + 1;
    const h = (cy >= 0 && cy < innerHeight) ? document.elementFromPoint((r.left + r.right) / 2, cy) : null;
    return {l: Math.round(r.left), r: Math.round(r.right), fullyInView: vis, hittable: !!h && (h === e || e.contains(h))}; };
  const links = [...document.querySelectorAll('footer a')];
  let worst = null; for (const a of links) { const r = a.getBoundingClientRect(); if (!worst || r.right > worst.r) worst = {t: a.textContent.trim().slice(0, 30), r: Math.round(r.right)}; }
  return {root: getComputedStyle(document.documentElement).fontSize, sw: document.documentElement.scrollWidth, iw: innerWidth,
    navCta: q('nav .nav-cta'), toggle: q('nav .nav-toggle'), footerRightmost: worst};
}"""
with lib.server(PORT) as base, lib.browser() as b:
    for p in pages:
        for (w, h, mob) in [(390, 844, True), (1280, 800, False), (1440, 900, False), (1920, 1080, False)]:
            for fs in (16, 20, 24, 32):
                ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob)
                ctx.route("**/*", router(base))
                pg = ctx.new_page()
                cdp = ctx.new_cdp_session(pg)
                cdp.send("Page.enable")
                cdp.send("Page.setFontSizes", {"fontSizes": {"standard": fs, "fixed": int(fs * 13 / 16)}})
                pg.goto(base + p, wait_until="load")
                pg.wait_for_timeout(600)
                if pg.query_selector("#irisSkip"):
                    pg.wait_for_timeout(2500)
                    pg.evaluate("document.getElementById('irisSkip').click()")
                    pg.wait_for_timeout(1500)
                r = pg.evaluate(JS)
                print("%s %dx%d font=%dpx(%d%%): sw=%d navCta=%s toggle=%s footerRightmost=%s" % (
                    p, w, h, fs, fs * 100 // 16, r["sw"], r["navCta"], r["toggle"], r["footerRightmost"]))
                if shots and fs == 32:
                    out = os.path.join(HERE, "shots", "font32_%s_%d.png" % (p.replace("/", "_").replace(".html", ""), w))
                    pg.screenshot(path=out)
                    if mob:
                        pg.evaluate("document.querySelector('footer').scrollIntoView({block:'start',behavior:'instant'})")
                        pg.wait_for_timeout(400)
                        pg.screenshot(path=out.replace(".png", "_footer.png"))
                ctx.close()
