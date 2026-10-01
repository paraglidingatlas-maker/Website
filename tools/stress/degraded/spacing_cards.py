#!/usr/bin/env python3
"""Homepage guest cards under WCAG 1.4.12 text spacing: how many guest names / hooks overflow the card art box.
usage: python3 spacing_cards.py [width]   Port 8814. Read-only on the repo."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lib
from degraded import new_ctx, goto, SPACING_CSS
W = int(sys.argv[1]) if len(sys.argv) > 1 else 1280
Q = r"""() => [...document.querySelectorAll('.ep-track .ep-card')].map(c => { const art = c.querySelector('.ep-art').getBoundingClientRect();
   const out = []; for (const s of ['.ep-name', '.ep-hook']) { const e = c.querySelector(s); if (!e) continue;
     const rg = document.createRange(); rg.selectNodeContents(e); const rs = [...rg.getClientRects()];
     const over = Math.max(0, ...rs.map(r => Math.max(r.right - art.right, art.left - r.left, r.bottom - art.bottom)));
     out.push([s, e.textContent.trim().slice(0, 30), Math.round(over)]); } return out; })"""
with lib.server(8814) as base:
    with lib.browser() as b:
        ctx = new_ctx(b, base, reduced_motion="reduce", viewport={"width": W, "height": 900}, is_mobile=W < 500)
        pg = ctx.new_page(); goto(pg, base + "index.html"); time.sleep(1)
        before = pg.evaluate(Q)
        pg.add_style_tag(content=SPACING_CSS); time.sleep(0.6)
        after = pg.evaluate(Q)
        nb = sum(1 for c in before for x in c if x[2] > 1); na = sum(1 for c in after for x in c if x[2] > 1)
        cards = len(after)
        print("cards=%d  text runs past the card art box: before=%d after=%d" % (cards, nb, na))
        for c in after:
            for x in c:
                if x[2] > 1: print("   ", x)
        ctx.close()
