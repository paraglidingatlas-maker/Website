"""Screenshots of the homepage globe: normal vs a malformed #pin= hash.
python3 globe_shot.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/user/Website/tools/stress")
import lib, dynamic
with lib.server(dynamic.PORT) as base:
    with lib.browser() as b:
        for name, h in [("globe_el_baseline.png", ""), ("globe_el_pin_percent.png", "#pin=%")]:
            log = {}
            ctx = dynamic.new_ctx(b, base, log, mock={"unpkg.com/world-atlas": dynamic.TINY_LAND})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(base + "index.html" + h, wait_until="load")
            pg.wait_for_timeout(1200)
            el = pg.locator("#epMap")
            el.scroll_into_view_if_needed()
            pg.wait_for_timeout(1500)
            el.screenshot(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), name))
            print(name, errs, pg.evaluate("document.querySelectorAll('#epMap circle').length"))
            ctx.close()
