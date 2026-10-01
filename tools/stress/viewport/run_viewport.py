#!/usr/bin/env python3
"""Viewport and zoom extremes on the LIVE site (repo root), served locally on port 8811.

Usage:
  python3 run_viewport.py sizes   [--sizes 280x653,320x568,...] [--pages all|templates|p1.html,p2.html] [--workers 4] [--out FILE]
  python3 run_viewport.py font200 [--pages templates|...] [--workers 4] [--out FILE]

sizes:   per page and size -> overflow, clipped text, text beyond viewport, fixed/sticky coverage
         (at load, ~1.5 screens, mid, bottom), covered interactive elements (scan + verify), paragraph metrics.
font200: 15 templates at 390x844 (mobile) and 1280x800, three modes: baseline, browser default font size
         32px (CDP Page.setFontSizes = Chrome Settings > Font size) and html{font-size:200%!important}.

External hosts are blocked here: i.ytimg.com thumbnails are fulfilled with a 480x360 placeholder so layout
matches production, YouTube embeds get a blank page, everything else external is aborted.
Read-only on the repo; writes JSON next to this script.
"""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import lib  # noqa: E402

PORT = 8811
MEASURE = open(os.path.join(HERE, "measure.js"), encoding="utf-8").read()
SIZES = {"280x653": (280, 653, True), "320x568": (320, 568, True), "844x390": (844, 390, True),
         "2560x1440": (2560, 1440, False), "3840x2160": (3840, 2160, False)}
FONT_SIZES = {"390x844": (390, 844, True), "1280x800": (1280, 800, False)}
THUMB = ('<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">'
         '<rect width="480" height="360" fill="#555"/></svg>')


def router(base):
    def handle(route):
        u = route.request.url
        if u.startswith(base) or u.startswith("data:") or u.startswith("blob:"):
            return route.continue_()
        if "ytimg.com" in u:
            return route.fulfill(status=200, content_type="image/svg+xml", body=THUMB)
        if "youtube" in u and route.request.resource_type == "document":
            return route.fulfill(status=200, content_type="text/html", body="<html><body style='margin:0;background:#000'></body></html>")
        return route.abort()
    return handle


def ev(page, mode, vw, vh, **kw):
    o = {"mode": mode, "vw": vw, "vh": vh}
    o.update(kw)
    return page.evaluate("(%s)(%s)" % (MEASURE, json.dumps(o)))


def run_one(b, base, path, label, w, h, mobile, font_mode=None, scroll_checks=True):
    t0 = time.time()
    ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile,
                        device_scale_factor=2 if mobile else 1)
    ctx.route("**/*", router(base))
    if font_mode == "css200":
        ctx.add_init_script("""(() => { const add = () => { if (document.getElementById('__ua200')) return;
          const s = document.createElement('style'); s.id='__ua200'; s.textContent = 'html{font-size:200% !important}';
          (document.head || document.documentElement).appendChild(s); };
          if (document.documentElement) add(); document.addEventListener('DOMContentLoaded', () => {
          const s = document.getElementById('__ua200'); if (s) document.head.appendChild(s); else add(); }); })();""")
    page = ctx.new_page()
    if font_mode == "setfont32":
        cdp = ctx.new_cdp_session(page)
        cdp.send("Page.enable")
        cdp.send("Page.setFontSizes", {"fontSizes": {"standard": 32, "fixed": 26}})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    rec = {"page": path, "size": label, "font": font_mode}
    try:
        resp = page.goto(base + path, wait_until="load", timeout=30000)
        rec["status"] = resp.status if resp else None
        page.wait_for_timeout(700)
        dl = ev(page, "dialog", w, h)
        if dl:
            # let an intro door finish its entrance, measure its controls, then dismiss it like a user would
            page.wait_for_timeout(2600)
            dl = ev(page, "dialog", w, h)
            rec["dialogs"] = dl
            closed = page.evaluate("""() => { for (const d of document.querySelectorAll('[aria-modal=true],[role=dialog],dialog[open]')) {
                const b = [...d.querySelectorAll('button,a')].find(e => /^(skip|close|dismiss|accept|got it|ok|×|✕)$/i.test((e.textContent||'').trim()) || /close|skip/i.test(e.getAttribute('aria-label')||''));
                if (b) { b.click(); return (b.textContent||'').trim() || b.getAttribute('aria-label'); } } return null; }""")
            rec["dialogClosedVia"] = closed
            page.wait_for_timeout(1500)
        # fixed/sticky at load, before any scrolling
        fx = [ev(page, "fixed", w, h, cov=True)]
        # reveal pass: walk down the page (lets IntersectionObserver reveals run) and sample fixed/sticky
        # coverage at ~1.5 screens, mid page and the bottom, after scroll-linked JS has had time to react
        maxs = page.evaluate("document.documentElement.scrollHeight - innerHeight")
        samples = {min(maxs, int(1.5 * h)), maxs // 2, maxs} if (mobile and scroll_checks) else ({maxs // 2, maxs} if scroll_checks else set())
        step = max(200, int(1.2 * h))
        ys = sorted(set(list(range(step, max(1, maxs), step))[:40]) | samples | {maxs})
        for y in ys:
            page.evaluate("y => window.scrollTo({top:y,behavior:'instant'})", y)
            if y in samples:
                page.wait_for_timeout(350)
                fx.append(ev(page, "fixed", w, h, cov=True))
            else:
                page.wait_for_timeout(45)
        page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
        page.wait_for_timeout(350)
        rec["fixedScroll"] = fx
        m = ev(page, "full", w, h)
        rec.update(m)
        # verify covered candidates by centring each one (async, lets scroll-linked JS run)
        cands = m.get("candidates", [])[:25]
        confirmed = []
        for c in cands:
            ev(page, "verify", w, h, idx=[c["i"]])
            page.wait_for_timeout(120)
            r2 = ev(page, "verify", w, h, idx=[c["i"]])[0]
            if r2.get("r") and not r2["r"].get("ok"):
                confirmed.append({"sel": c["sel"], "text": c["text"], "scan": c["cov"][:1], "centred": r2["r"],
                                  "selMatch": r2.get("sel") == c["sel"]})
        rec["coveredConfirmed"] = confirmed
        rec["nCandidates"] = len(m.get("candidates", []))
        rec.pop("candidates", None)
    except Exception as e:  # noqa: BLE001
        rec["error"] = str(e)[:300]
    rec["pageErrors"] = errs[:5]
    rec["secs"] = round(time.time() - t0, 2)
    ctx.close()
    return rec


def worker(tasks, base, q, wid):
    with lib.browser(args=["--disable-gpu"]) as b:
        for t in tasks:
            try:
                r = run_one(b, base, *t)
            except Exception as e:  # noqa: BLE001
                r = {"page": t[0], "size": t[1], "font": t[5] if len(t) > 5 else None, "error": "worker: " + str(e)[:300]}
            q.put(r)
    q.put(("done", wid))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["sizes", "font200"])
    ap.add_argument("--sizes", default=None)
    ap.add_argument("--pages", default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.pages in (None, "all"):
        pages = lib.pages("live") if a.mode == "sizes" else lib.TEMPLATES["live"]
    elif a.pages == "templates":
        pages = lib.TEMPLATES["live"]
    else:
        pages = a.pages.split(",")
    tasks = []
    if a.mode == "sizes":
        sizes = a.sizes.split(",") if a.sizes else list(SIZES)
        for s in sizes:
            w, h, mob = SIZES[s]
            for p in pages:
                tasks.append((p, s, w, h, mob, None, True))
    else:
        for s, (w, h, mob) in FONT_SIZES.items():
            for fm in (None, "setfont32", "css200"):
                for p in pages:
                    tasks.append((p, s, w, h, mob, fm, True))
    # interleave so workers get a mix of heavy and light pages
    n = max(1, min(a.workers, len(tasks)))
    chunks = [tasks[i::n] for i in range(n)]
    out = a.out or os.path.join(HERE, "results_%s.json" % a.mode)
    t0 = time.time()
    results = []
    with lib.server(PORT) as base:
        ctx = mp.get_context("spawn")
        q = ctx.Queue()
        procs = [ctx.Process(target=worker, args=(chunks[i], base, q, i)) for i in range(n)]
        for p in procs:
            p.start()
        done = 0
        while done < n:
            r = q.get()
            if isinstance(r, tuple) and r[0] == "done":
                done += 1
                continue
            results.append(r)
            if len(results) % 25 == 0:
                print("%d/%d  %.0fs" % (len(results), len(tasks), time.time() - t0), flush=True)
        for p in procs:
            p.join(10)
            if p.is_alive():
                p.kill()
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    print("wrote", out, len(results), "records in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
