#!/usr/bin/env python3
"""Destination hero slideshow on Slow 3G: what a phone actually shows, second by second.

    python3 hero_slideshow.py [destinations/india.html] [--profile slow3g|fast3g]

Samples every 500 ms: which slide is on, whether its photograph has arrived, whether
the other slides have been let into layout (.khero-par.is-warm), readyState. Runs the
page twice: default, and with prefers-reduced-motion (the slideshow timer is off, so
is-warm only comes 600 ms after load, the intended behaviour).
"""
import json
import sys
import time
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import lib  # noqa: E402

PORT = 8812
NET = {"slow3g": dict(latency=400, downloadThroughput=50000, uploadThroughput=50000),
       "fast3g": dict(latency=150, downloadThroughput=200000, uploadThroughput=93750)}

SAMPLE = r"""() => {
  const par = document.querySelector('.khero-par');
  const slides = [...document.querySelectorAll('.khero-slide')];
  const on = slides.findIndex(s => s.classList.contains('is-on'));
  const img = on >= 0 ? slides[on].querySelector('img') : null;
  const loaded = slides.map(s => { const i = s.querySelector('img'); return i ? (i.complete && i.naturalWidth > 0) : null; });
  return {t: Math.round(performance.now()), ready: document.readyState, warm: par ? par.classList.contains('is-warm') : null,
          on, onImgLoaded: img ? (img.complete && img.naturalWidth > 0) : null, loaded,
          onSrc: img ? (img.currentSrc || img.src).split('/').pop() : null};
}"""


def run(b, base, path, prof, reduced):
    kw = dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    if reduced:
        kw["reduced_motion"] = "reduce"
    ctx = b.new_context(**kw)
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    cdp.send("Network.emulateNetworkConditions", dict(offline=False, **NET[prof]))
    page.goto(base + path, wait_until="commit", timeout=60000)
    samples = []
    t0 = time.time()
    load_at = None
    while time.time() - t0 < 110:
        try:
            s = page.evaluate(SAMPLE)
        except Exception:
            page.wait_for_timeout(300)
            continue
        samples.append(s)
        if s["ready"] == "complete" and load_at is None:
            load_at = s["t"]
        if load_at is not None and s["t"] > load_at + 3000:
            break
        page.wait_for_timeout(500)
    res = page.evaluate("""() => performance.getEntriesByType('resource')
        .filter(r => /destinations\\/[a-z]+\\/(hero|gallery)\\//.test(r.name) || /assets\\/video\\//.test(r.name))
        .map(r => ({f: r.name.split('/').slice(-2).join('/'), end: Math.round(r.responseEnd), kb: Math.round(r.transferSize/1024)}))""")
    nav = page.evaluate("() => { const n = performance.getEntriesByType('navigation')[0]; return {load: Math.round(n.loadEventEnd), dcl: Math.round(n.domContentLoadedEventEnd)}; }")
    ctx.close()
    # seconds (while the page was loading) during which the showing slide had no photograph
    blank = [s for s in samples if s["on"] is not None and s["on"] >= 0 and s["onImgLoaded"] is False]
    first_warm = next((s["t"] for s in samples if s["warm"]), None)
    first_img = next((s["t"] for s in samples if s["onImgLoaded"]), None)
    slide_changes = []
    prev = None
    for s in samples:
        if s["on"] != prev:
            slide_changes.append((s["t"], s["on"], s["onImgLoaded"]))
            prev = s["on"]
    return {"path": path, "profile": prof, "reduced_motion": reduced, "nav": nav, "warm_at_ms": first_warm,
            "first_sample_with_photo_ms": first_img, "samples": len(samples),
            "blank_hero_samples": len(blank), "blank_hero_s_approx": round(len(blank) * 0.5 + 0.0, 1),
            "slide_changes": slide_changes[:20], "hero_resources": sorted(res, key=lambda r: r["end"]),
            "last": samples[-1] if samples else None}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prof = "slow3g"
    if "--profile" in sys.argv:
        prof = sys.argv[sys.argv.index("--profile") + 1]
        args = [a for a in args if a != prof]
    pages = args or ["destinations/india.html", "destinations/kenya.html"]
    out = []
    with lib.server(PORT) as base, lib.browser() as b:
        for p in pages:
            for reduced in (False, True):
                r = run(b, base, p, prof, reduced)
                out.append(r)
                print(json.dumps({k: v for k, v in r.items() if k not in ("hero_resources",)}, default=str)[:1500])
                print("  hero resources:", r["hero_resources"])
    lib.save("network/out/hero_slideshow_%s.json" % prof, out)


if __name__ == "__main__":
    main()
