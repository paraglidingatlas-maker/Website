"""Kenya/India hero slideshow: horizontal finger swipe on a phone (raw CDP touch events), as shipped vs with
.khero{touch-action:pan-y} injected (the fix the homepage strip and photo ring already use).
python3 hero_swipe.py"""
import sys; sys.path.insert(0,'/home/user/Website/tools/stress'); import lib
sys.path.insert(0,'/home/user/Website/tools/stress/critic'); import touch
SLIDE = "() => [...document.querySelectorAll('.khero-slide')].findIndex(e => e.classList.contains('is-on'))"
with lib.server(8895) as base, lib.browser() as b:
    for path in ("destinations/kenya.html", "destinations/india.html"):
        for fix in (False, True):
            ctx = touch.ctx_for(b); pg = ctx.new_page(); pg.goto(base + path); pg.wait_for_timeout(1200)
            if fix: pg.add_style_tag(content=".khero{touch-action:pan-y}")
            pg.evaluate("""() => { window.__pe=[]; const h=document.querySelector('.khero');
                ['pointerdown','pointerup','pointercancel'].forEach(t=>h.addEventListener(t,e=>__pe.push(t),true)); }""")
            cdp = ctx.new_cdp_session(pg)
            ta = pg.evaluate("getComputedStyle(document.querySelector('.khero')).touchAction")
            res = []
            for (dx, steps) in ((-240, 12), (-240, 30), (240, 12), (-120, 8)):
                s0 = pg.evaluate(SLIDE); pg.evaluate("window.__pe.length=0")
                u0 = pg.url
                touch.swipe(cdp, 195, 420, dx=dx, steps=steps); pg.wait_for_timeout(900)
                if pg.url != u0:
                    res.append({"finger_dx": dx, "moves": steps, "NAVIGATED_TO": pg.url}); break
                res.append({"finger_dx": dx, "moves": steps, "slide": "%d->%d" % (s0, pg.evaluate(SLIDE)), "events": pg.evaluate("(window.__pe||['<reloaded>']).join(',')")})
            print(path, "fix" if fix else "as shipped", "touch-action:", ta)
            for r in res: print("   ", r, flush=True)
            if not any("NAVIGATED_TO" in r for r in res):
                tab = pg.locator(".khero-tab").nth(2); s0 = pg.evaluate(SLIDE); tab.tap(timeout=5000); pg.wait_for_timeout(600)
                print("    tap on 3rd tab: slide %d->%d" % (s0, pg.evaluate(SLIDE)))
            ctx.close()
