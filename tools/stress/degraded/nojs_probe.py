#!/usr/bin/env python3
"""JavaScript disabled: targeted checks. Port 8814. Read-only on the repo.
usage: python3 nojs_probe.py [transcript|hidden|stats|all] [episode-page ...]
  transcript  episode transcript clip: visible height vs full height, no-js class, does 'Continue reading' do anything
  hidden      sections that CSS hides (opacity 0) until a script adds a class: knowledge-base.html, kenya, india, podcast
  stats       podcast.html counters without JS
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lib  # noqa: E402
from degraded import new_ctx, goto  # noqa: E402


def transcript(b, base, pages):
    pages = pages or ["episodes/sky-gods-flying-8000ers-antoine-girard.html", "episodes/navigating-colombia-pal-takats.html",
                      "episodes/a-note-of-thanks.html"]
    for p in pages:
        ctx = new_ctx(b, base, java_script_enabled=False)
        pg = ctx.new_page()
        goto(pg, base + p)
        m = pg.evaluate("""() => { const t = document.getElementById('transcript-body'); if (!t) return null;
            const words = t.textContent.trim().split(/\\s+/).length; const visFrac = t.clientHeight / t.scrollHeight;
            return {htmlClass: document.documentElement.className, maxHeight: getComputedStyle(t).maxHeight, clientH: t.clientHeight,
                    scrollH: t.scrollHeight, words, visibleWordsApprox: Math.round(words * visFrac)}; }""")
        moved = None
        if m and pg.locator(".cd-more").count():
            pg.click(".cd-more")
            time.sleep(0.5)
            moved = pg.evaluate("document.getElementById('transcript-body').clientHeight")
        print("%-70s %s  after clicking 'Continue reading': clientH=%s" % (p, m, moved))
        ctx.close()


def hidden(b, base, pages):
    pages = pages or ["knowledge-base.html", "destinations/kenya.html", "destinations/india.html", "podcast.html"]
    for p in pages:
        res = {}
        for js in (False, True):
            ctx = new_ctx(b, base, java_script_enabled=js)
            pg = ctx.new_page()
            goto(pg, base + p)
            time.sleep(0.6 if js else 0)
            if js:
                for y in range(0, 30000, 600):
                    pg.evaluate("y => window.scrollTo(0, y)", y)
                    time.sleep(0.08)
                time.sleep(1.2)
            res[js] = pg.evaluate("""() => [...document.querySelectorAll('.clb-station, .kfly-copy, .fly-better h2, .cfl-card-cap')]
                .map(e => ({sel: e.tagName.toLowerCase() + '.' + [...e.classList].join('.') + (e.id ? '#' + e.id : ''), op: getComputedStyle(e).opacity,
                            chars: e.textContent.replace(/\\s+/g, ' ').trim().length}))""")
            ctx.close()
        off = res[False]
        hid = [x for x in off if x["op"] == "0"]
        print("%-28s JS off: %d of %d blocks at opacity 0, %d chars hidden; JS on after scrolling: %d at opacity 0" % (
            p, len(hid), len(off), sum(x["chars"] for x in hid), sum(1 for x in res[True] if x["op"] == "0")))
        for x in hid[:6]:
            print("      ", x)


def stats(b, base, pages):
    ctx = new_ctx(b, base, java_script_enabled=False)
    pg = ctx.new_page()
    goto(pg, base + "podcast.html")
    print("podcast.html JS off #animStats:", pg.evaluate(
        "[...document.querySelectorAll('#animStats .stat-item')].map(s => s.innerText.replace(/\\s+/g, ' '))"))
    ctx.close()


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    pages = sys.argv[2:]
    with lib.server(8814) as base:
        with lib.browser() as b:
            for name, fn in (("transcript", transcript), ("hidden", hidden), ("stats", stats)):
                if what in (name, "all"):
                    print("=== " + name)
                    fn(b, base, pages)
