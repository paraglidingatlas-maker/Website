#!/usr/bin/env python3
"""Isolate the FAQ block of a knowledge-base topic page and print it. usage: python3 faq_probe2.py [page]. Port 8814."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "pylib"))
import lib
from degraded import new_ctx, goto, scroll_through, pdf_stats
from print_probe import pdf_text, MARGIN
page = sys.argv[1] if len(sys.argv) > 1 else "knowledge-base/navigators.html"
with lib.server(8814) as base:
    with lib.browser() as b:
        for name, js, bg in (("faq-only", True, False), ("faq-only+bg", True, True), ("faq-only-no-anc-css", "strip", False)):
            ctx = new_ctx(b, base); pg = ctx.new_page(); goto(pg, base + page); time.sleep(0.8)
            scroll_through(pg, pause=0.12); time.sleep(2.2)
            pg.evaluate("""(mode) => { const q = document.getElementById('questions');
                for (let e = q; e && e !== document.body; e = e.parentElement) for (const s of e.parentElement.children) if (s !== e) s.style.display = 'none';
                if (mode === 'strip') for (const e of q.querySelectorAll('*')) { e.style.opacity = '1'; e.style.transform = 'none'; e.style.filter = 'none'; e.style.clipPath = 'none'; e.style.overflow = 'visible'; e.style.maskImage = 'none'; e.style.webkitMaskImage = 'none'; }
                const cs = getComputedStyle(q); return 0; }""", js)
            chain = pg.evaluate("""() => { const out = []; const s = document.querySelector('#questions summary');
                for (let e = s; e; e = e.parentElement) { const c = getComputedStyle(e); if (c.maskImage !== 'none' || c.webkitMaskImage !== 'none' || c.clipPath !== 'none' || c.filter !== 'none' || c.opacity !== '1' || c.overflow !== 'visible' || c.mixBlendMode !== 'normal' || c.isolation !== 'auto' || c.contain !== 'none')
                  out.push([e.tagName + '.' + e.className, c.maskImage.slice(0,60), c.clipPath, c.filter, c.opacity, c.overflow, c.mixBlendMode, c.contain]); } return out; }""")
            pdf = pg.pdf(format="A4", margin=MARGIN, print_background=bg)
            st = pdf_stats(pdf)
            open(os.path.join(HERE, "out", "pdf", "faq_" + name + ".pdf"), "wb").write(pdf)
            print(name, [(p["chars"], p["dark"]) for p in st], chain)
            ctx.close()
