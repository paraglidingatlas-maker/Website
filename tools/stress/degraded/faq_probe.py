#!/usr/bin/env python3
"""Why is the FAQ printed blank on the knowledge-base topic pages? Print variants and compare ink on the FAQ page.
usage: python3 faq_probe.py [page]   (default knowledge-base/navigators.html). Port 8814. Read-only on the repo."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "pylib"))
import lib
from degraded import new_ctx, goto, scroll_through, pdf_stats
from print_probe import pdf_text, MARGIN
page = sys.argv[1] if len(sys.argv) > 1 else "knowledge-base/navigators.html"
VARIANTS = {"as-is": None, "no-border-image": "details,.faq-r *{border-image:none!important}",
            "details-as-div": "details{display:block!important;contain:none!important}", "no-kb-atmos": ".kb-atmos{display:none!important}",
            "details-open": "details>*{display:block!important}",
            "no-kr-transition": ".kr,.in{opacity:1!important;transform:none!important;transition:none!important}",
            "faq-color-black": "summary,details p{color:#000!important}",
            "fq-in-static": ".fq-in,.faq-l h2{position:static!important}",
            "faq-block": ".faq{display:block!important}"}
with lib.server(8814) as base:
    with lib.browser() as b:
        for name, css in VARIANTS.items():
            ctx = new_ctx(b, base); pg = ctx.new_page(); goto(pg, base + page); time.sleep(0.8)
            scroll_through(pg, pause=0.12); time.sleep(2.2)
            info = pg.evaluate("""() => { const s = document.querySelector('.faq-r summary') || document.querySelector('summary');
                const d = s.closest('details'); const cs = getComputedStyle(d), ss = getComputedStyle(s);
                return {cls: d.className, op: cs.opacity, tf: cs.transform, color: ss.color, fill: ss.webkitTextFillColor, filter: cs.filter,
                        mix: cs.mixBlendMode, parent: d.parentElement.className, pop: getComputedStyle(d.parentElement).opacity}; }""")
            if css: pg.add_style_tag(content=css); time.sleep(0.3)
            pdf = pg.pdf(format="A4", margin=MARGIN)
            st = pdf_stats(pdf); tx = pdf_text(pdf)
            i = next((k for k, t in enumerate(tx) if "?" in t and "FAQ" not in t[:40] and ("When" in t or "What" in t or "How" in t)), None)
            faq = [k + 1 for k, t in enumerate(tx) if "Questions these conversations answer" in t]
            q = [(k + 1, p["chars"], p["dark"]) for k, p in enumerate(st) if k + 1 in (faq[0], faq[0] + 1)] if faq else None
            print("%-18s pages=%d faq-heading-page=%s  (page, chars, ink3) around FAQ=%s  details style=%s" % (name, len(st), faq, q, info))
            ctx.close()
