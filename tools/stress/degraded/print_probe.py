#!/usr/bin/env python3
"""Targeted print (A4 PDF) checks on the live pages. Port 8814. Read-only on the repo.

usage: python3 print_probe.py [reveal|kbdoor|kfly|transcript|all]
  reveal      print right after load (no scrolling) vs after scrolling through: blank pages from scroll-reveal
  kbdoor      knowledge-base.html: print with the door (iris) up, and after pressing Skip
  kfly        Kenya/India 'flying day' steps: is their copy in the printout?
  transcript  episode page: how much of the transcript reaches the printout
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, "pylib"))
import lib  # noqa: E402
from degraded import new_ctx, goto, scroll_through, pdf_stats, HELPERS  # noqa: E402

PORT = 8814
MARGIN = {"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}


def pdf_text(pdf):
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf)
    return [" ".join((doc[i].get_textpage().get_text_range() or "").split()) for i in range(len(doc))]


def show(label, pdf):
    st = pdf_stats(pdf)
    blank = [i + 1 for i, p in enumerate(st) if p["chars"] < 5]
    invis = [i + 1 for i, p in enumerate(st) if p["chars"] >= 150 and p["dark"] < 0.001]
    print("  %-28s pages=%2d chars=%6d blank_pages=%s text_but_no_ink_pages=%s" % (
        label, len(st), sum(p["chars"] for p in st), blank, invis))
    return st


def reveal(b, base):
    for path in ["index.html", "knowledge-base/flight-mechanics.html", "knowledge-base/navigators.html",
                 "knowledge-base/weather-patterns.html", "about.html", "podcast.html"]:
        print(path)
        for variant in ("load-then-print", "scroll-then-print"):
            ctx = new_ctx(b, base)
            pg = ctx.new_page()
            goto(pg, base + path)
            time.sleep(1.0)
            if variant == "scroll-then-print":
                scroll_through(pg, pause=0.12)
                time.sleep(1.0)
            hidden = pg.evaluate("""() => [...document.querySelectorAll('body *')].filter(e => getComputedStyle(e).opacity === '0'
                    && e.innerText && e.innerText.trim().length > 30).filter(e => !e.parentElement.closest('*') || getComputedStyle(e.parentElement).opacity !== '0')
                    .map(e => (e.className && e.className.baseVal === undefined ? e.tagName.toLowerCase() + '.' + [...e.classList].join('.') : e.tagName)).slice(0, 8)""")
            show(variant, pg.pdf(format="A4", margin=MARGIN))
            if variant == "load-then-print":
                print("    opacity:0 blocks with text at print time:", hidden)
            ctx.close()


def kbdoor(b, base):
    path = "knowledge-base.html"
    print(path)
    for variant in ("door-up", "after-skip"):
        ctx = new_ctx(b, base)
        pg = ctx.new_page()
        goto(pg, base + path)
        time.sleep(1.5)
        st = pg.evaluate("() => { const i = document.getElementById('iris'); const cs = i && getComputedStyle(i);"
                         " return {htmlClass: document.documentElement.className, iris: cs ? [cs.display, cs.position, cs.zIndex] : null}; }")
        if variant == "after-skip":
            try:
                pg.click("#irisSkip", timeout=3000)
            except Exception as e:
                print("   skip click failed:", str(e)[:100])
            time.sleep(2.5)
            st = pg.evaluate("() => { const i = document.getElementById('iris'); const cs = i && getComputedStyle(i);"
                             " return {htmlClass: document.documentElement.className, iris: cs ? [cs.display, cs.position, cs.zIndex] : null}; }")
        scroll_through(pg, pause=0.12)
        time.sleep(1.0)
        print("   state:", st)
        show(variant, pg.pdf(format="A4", margin=MARGIN))
        ctx.close()


def kfly(b, base):
    for path in ["destinations/kenya.html", "destinations/india.html"]:
        ctx = new_ctx(b, base)
        ctx.add_init_script(HELPERS)
        pg = ctx.new_page()
        goto(pg, base + path)
        time.sleep(1.0)
        scroll_through(pg, pause=0.12)
        time.sleep(1.0)
        copies = pg.evaluate("() => [...document.querySelectorAll('.kfly-copy')].map(c => ({op: getComputedStyle(c).opacity,"
                             " on: c.closest('.kfly-step').classList.contains('is-on'), t: c.innerText.replace(/\\s+/g, ' ').trim()}))")
        pdf = pg.pdf(format="A4", margin=MARGIN)
        txt = " ".join(pdf_text(pdf)).replace(" ", "").lower()
        print(path)
        show("scroll-then-print", pdf)
        for c in copies:
            probe = c["t"][20:60].replace(" ", "").lower()
            print("   kfly-copy opacity=%s is-on=%s chars=%d in_pdf=%s  %r" % (c["op"], c["on"], len(c["t"]), probe in txt, c["t"][:60]))
        ctx.close()


def transcript(b, base):
    path = "episodes/sky-gods-flying-8000ers-antoine-girard.html"
    ctx = new_ctx(b, base)
    pg = ctx.new_page()
    goto(pg, base + path)
    time.sleep(1.0)
    dom = pg.evaluate("() => { const t = document.getElementById('transcript-body'); const cs = getComputedStyle(t);"
                      " return {chars: t.textContent.replace(/\\s+/g, '').length, maxHeight: cs.maxHeight, overflow: cs.overflow, h: t.clientHeight, sh: t.scrollHeight}; }")
    pdf = pg.pdf(format="A4", margin=MARGIN)
    txt = pdf_text(pdf)
    print(path)
    print("   #transcript-body in DOM:", dom)
    show("print (as loaded)", pdf)
    # how much of the transcript is in the printout: count the last transcript words
    last = pg.evaluate("() => document.getElementById('transcript-body').innerText.trim().split(/\\s+/).slice(-8).join('')")
    print("   last transcript words in PDF:", last.lower() in "".join(txt).replace(" ", "").lower())
    ctx.close()


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    with lib.server(PORT) as base:
        with lib.browser() as b:
            for name, fn in (("reveal", reveal), ("kbdoor", kbdoor), ("kfly", kfly), ("transcript", transcript)):
                if what in (name, "all"):
                    print("=== " + name)
                    fn(b, base)
