import sys
sys.path.insert(0, "/home/user/Website/tools/stress/abuse")
import abuse, lib
with lib.server(8813) as base:
    with lib.browser() as b:
        for gap in (int(a) for a in (sys.argv[1:] or ["400", "900"])):
            c = abuse.Ctx(b, base, 1440, 900)
            c.goto("knowledge-base/flight-mechanics.html", settle=600)
            abuse.first_tile(c); abuse.open_tile(c); abuse.wait_modal(c, True, 800); c.page.wait_for_timeout(300)
            c.js("""() => { window.__log = []; const t0 = performance.now(); const L = m => window.__log.push(Math.round(performance.now() - t0) + ' ' + m);
                 const o = document.getElementById('epModalOverlay');
                 o.addEventListener('animationstart', e => L('animstart ' + e.animationName + ' on ' + (e.target.id || e.target.className).toString().slice(0, 20)));
                 o.addEventListener('animationend', e => L('animend ' + e.animationName + ' on ' + (e.target.id || e.target.className).toString().slice(0, 20)));
                 addEventListener('popstate', () => L('popstate'));
                 new MutationObserver(() => L('overlay=' + o.className + ' body=' + document.body.className)).observe(o, {attributes: true});
                 document.addEventListener('keydown', e => L('key ' + e.key + ' focus=' + (document.activeElement.className || '').toString().slice(0, 20)), true); }""")
            c.page.keyboard.press("Escape")
            c.page.wait_for_timeout(gap)
            c.page.keyboard.press("Enter")
            c.page.wait_for_timeout(1200)
            print("gap", gap); print("\n".join("   " + x for x in c.js("() => window.__log")))
            print("  ", c.js(abuse.MODAL_STATE))
            c.close()
