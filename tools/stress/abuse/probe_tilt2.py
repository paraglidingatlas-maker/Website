"""Rest the pointer on a 5x5 grid across the front photo (desktop), let the lean settle, click.
Counts clicks that do not open the full-size view. python3 probe_tilt2.py [page]   (REDUCED=1 for the control run)"""
import sys
sys.path.insert(0, "/home/user/Website/tools/stress/abuse")
import abuse, lib
import os
REDUCED = os.environ.get("REDUCED") == "1"
pages = sys.argv[1:] or ["destinations/kenya.html", "destinations/india.html"]
with lib.server(8813) as base:
    with lib.browser() as b:
        for p in pages:
            c = abuse.Ctx(b, base, 1440, 900, reduced=REDUCED)
            c.goto(p, settle=500)
            abuse.center(c, ".cfl")
            c.page.wait_for_timeout(800)
            r = c.js("() => { const q = document.querySelector('.cfl-card.is-front').getBoundingClientRect(); return {l: q.left, t: q.top, w: q.width, h: q.height}; }")
            miss, hits, tot = [], 0, 0
            for i in range(5):
                for j in range(5):
                    x = r["l"] + r["w"] * (0.1 + 0.2 * i); y = r["t"] + r["h"] * (0.1 + 0.2 * j)
                    c.page.mouse.move(x, y, steps=4)
                    c.page.wait_for_timeout(700)
                    hit = c.js("pt => { const e = document.elementFromPoint(pt[0], pt[1]); const k = e && e.closest('.cfl-card'); return k ? (k.classList.contains('is-front') ? 'front' : 'other card') : (e ? e.className : 'none'); }", [x, y])
                    c.page.mouse.down(); c.page.mouse.up()
                    abuse.raf(c, 1)
                    s = c.js(abuse.CFL_STATE)
                    tot += 1
                    if s["lbOpen"]:
                        hits += 1
                        c.page.keyboard.press("Escape"); abuse.raf(c, 1)
                        c.page.mouse.move(x, y)
                    else:
                        miss.append({"at": [round(0.1 + 0.2 * i, 1), round(0.1 + 0.2 * j, 1)], "hit": hit, "front_now": s["front"]})
                    c.page.wait_for_timeout(150)
            print(p, "reduced-motion" if REDUCED else "full-motion", "clicks on the front photo that opened it: %d/%d" % (hits, tot))
            for m in miss[:25]: print("   miss", m)
            c.close()
