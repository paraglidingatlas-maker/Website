#!/usr/bin/env python3
"""Library page when one of its data/scripts fails to arrive (flaky network, blocked file).

    python3 library_partial.py

For each case: series tiles rendered (#feat/#rest children), visible <noscript> index,
uncaught errors, and what 'Browse every episode' and search do.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import lib
OUT = os.path.join(HERE, "out")
M = dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
res = []
with lib.server(8812) as base, lib.browser() as b:
    for blk in [None, "library-data.js", "library.js", "library-episodes.js"]:
        ctx = b.new_context(**M); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
        if blk:
            pg.route("**/*", lambda r, q, blk=blk: r.abort() if (q.resource_type == "script" and q.url.split("?")[0].endswith("/" + blk)) else r.continue_())
        pg.goto(base + "library.html", wait_until="load"); pg.wait_for_timeout(1200)
        st = pg.evaluate("""() => ({feat: document.getElementById('feat').children.length, rest: document.getElementById('rest').children.length,
            seriesCount: document.getElementById('seriesCount').textContent, noscriptIndexShown: !!document.querySelector('.lib-index') && document.querySelector('.lib-index').getBoundingClientRect().height > 0,
            episodeLinksVisible: [...document.querySelectorAll('a[href*="episodes/"]')].filter(a => a.getBoundingClientRect().height > 0).length})""")
        if blk and blk != "library-episodes.js":
            pg.screenshot(path=os.path.join(OUT, "library_without_%s.png" % blk.replace(".", "_")), full_page=True)
        # try the controls
        pg.click("#allBtn", timeout=3000); pg.wait_for_timeout(800)
        after_all = pg.evaluate("""() => ({resultsShown: !document.getElementById('results').classList.contains('lib-hidden'),
            eps: document.getElementById('eps').children.length, cnt: document.getElementById('cnt').textContent.trim().slice(0, 60)})""")
        r = {"blocked": blk, "state": st, "after_browse_all": after_all, "errors": errs}
        res.append(r); print(json.dumps(r))
        ctx.close()
lib.save("network/out/library_partial.json", res)
