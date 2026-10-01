"""Kenya/India FAQ: two clicks on a question N ms apart (a human double-click is ~80-300 ms),
then up to four single clicks a second apart. Reports whether the answer is visible.
python3 probe_faq2.py"""
import sys
sys.path.insert(0, "/home/user/Website/tools/stress/abuse")
import abuse, lib
ST = """() => { const d = document.querySelector('.kfaq .kfaq-item'), s = d.querySelector('summary'), bd = d.querySelector('.kfaq-body');
  const shown = Math.round(d.getBoundingClientRect().height - s.getBoundingClientRect().height);
  return {open: d.open, answerPx: shown, styleH: bd.style.height, stuck: d.open && shown < 8}; }"""
with lib.server(8813) as base:
    with lib.browser() as b:
        for p in ("destinations/kenya.html", "destinations/india.html"):
            for gap in (10, 40, 80, 150, 250, 400):
                c = abuse.Ctx(b, base, 1440, 900)
                c.goto(p, settle=300)
                sm = abuse.center(c, ".kfaq .kfaq-item summary")
                c.page.mouse.click(sm["x"], sm["y"])
                c.page.wait_for_timeout(gap)
                c.page.mouse.click(sm["x"], sm["y"])
                c.page.wait_for_timeout(1000)
                seq = [c.js(ST)]
                for k in range(4):
                    c.page.mouse.click(sm["x"], sm["y"])
                    c.page.wait_for_timeout(1000)
                    seq.append(c.js(ST))
                print(p, "gap %3dms" % gap, "->", seq[0], "| next clicks stuck:", [x["stuck"] for x in seq[1:]], "open:", [x["open"] for x in seq[1:]])
                c.close()
