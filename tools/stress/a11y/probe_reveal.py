"""Probe: does a Tab-focused .kr element (knowledge-base reveal) stay invisible?
python3 probe_reveal.py [page] [vp]"""
import sys, json
sys.path.insert(0, "/home/user/Website/tools/stress")
sys.path.insert(0, "/home/user/Website/tools/stress/a11y")
import lib, keyboard as K
page = sys.argv[1] if len(sys.argv) > 1 else "knowledge-base/navigators.html"
vp = sys.argv[2] if len(sys.argv) > 2 else "desktop"
with lib.server(8815) as base, lib.browser() as b:
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, page)
    for i in range(300):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(60)
        inf = pg.evaluate("() => __kb.info(false)")
        if inf.get("body"): break
        if any("opacity" in w for w in inf["hid"]):
            tl = []
            for t in (300, 800, 1500, 3000):
                pg.wait_for_timeout(t - (tl[-1]["t"] if tl else 60))
                s = pg.evaluate("""() => { const e=document.activeElement, r=e.getBoundingClientRect();
                   let o=1; for (let n=e;n&&n.nodeType===1;n=n.parentElement) o*=parseFloat(getComputedStyle(n).opacity);
                   const kr = e.closest('.kr'); return {top: Math.round(r.top), bottom: Math.round(r.bottom), vh: innerHeight, eff_opacity: +o.toFixed(3), kr_in: kr ? kr.classList.contains('in') : null, scrollY: Math.round(scrollY)}; }""")
                s["t"] = t; tl.append(s)
            print(json.dumps({"i": i + 1, "d": inf["d"], "text": inf["text"][:40], "timeline": tl}))
