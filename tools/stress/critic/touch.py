"""Touch-only gestures on a phone (390x844, DPR 2, mobile, has_touch) on the LIVE site.

python3 touch.py gest            real touch swipes (CDP Input.synthesizeScrollGesture, gestureSourceType=touch)
                                 on every swipeable component, horizontal and vertical
python3 touch.py scan [limit]    all 180 pages: share of the screen where a vertical finger swipe cannot
                                 scroll the page (computed touch-action none/pan-x up the ancestor chain)
python3 touch.py globe           vertical swipes down the homepage, through the globe, versus a control column
"""
import sys, os, json, time, concurrent.futures as cf
sys.path.insert(0, "/home/user/Website/tools/stress")
import lib

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8895
BASE = "http://127.0.0.1:%d/" % PORT
PHONE = dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
             user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36")


def ctx_for(b):
    ctx = b.new_context(**PHONE)
    ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
    # Knowledge Base door already seen, so it does not cover the page
    ctx.add_init_script("try{sessionStorage.setItem('pga.kb.iris.seen','1')}catch(e){}")
    return ctx


def swipe(cdp, x, y, dx=0, dy=0, steps=12):
    """A raw finger: touchStart, `steps` touchMoves by (dx, dy) in total, touchEnd (CDP Input.dispatchTouchEvent).
    Travel is centred on (x, y) and both ends are kept on screen."""
    x0 = max(8, min(382, x - dx / 2)); y0 = max(8, min(836, y - dy / 2))
    cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x0, "y": y0}]})
    for i in range(1, steps + 1):
        cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x0 + dx * i / steps, "y": y0 + dy * i / steps}]})
    cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})


STATE = {
    "khero": """() => { const s=[...document.querySelectorAll('.khero-slide')]; return {slide: s.findIndex(e=>e.classList.contains('is-on')), y: scrollY}; }""",
    "cfl": """() => { const f=document.querySelector('.cfl-card.is-front,.cfl-card.front,[data-front],.cfl-card[aria-current]');
                      const c=[...document.querySelectorAll('.cfl-card')];
                      const tr=c.slice(0,4).map(e=>getComputedStyle(e).transform).join('|');
                      return {front: f ? c.indexOf(f) : null, sig: tr.slice(0,120), y: scrollY}; }""",
    "rail": """(sel) => { const v=document.querySelector(sel); const t=v && (v.firstElementChild);
                      return {tx: t ? getComputedStyle(t).transform : null, sl: v ? v.scrollLeft : null, y: scrollY}; }""",
    "kmap": """() => { const s=document.querySelector('.kmap-stage'); const t=document.querySelector('.kmap-view');
                      return {tx: t ? getComputedStyle(t).transform : null, vb: s && s.querySelector('svg') ? s.querySelector('svg').getAttribute('viewBox') : null, y: scrollY}; }""",
    "globe": """() => { const p=[...document.querySelectorAll('#epMap svg path')].find(e=>(e.getAttribute('d')||'').length>20); return {d: p ? (p.getAttribute('d')||'').slice(0,60) : null, y: scrollY}; }""",
}


def center_of(pg, sel):
    return pg.evaluate("""(sel) => { const e=document.querySelector(sel); if(!e) return null; e.scrollIntoView({block:'center', behavior:'instant'});
        const r=e.getBoundingClientRect(); const ta=getComputedStyle(e).touchAction;
        return {x: r.left + r.width/2, y: r.top + r.height/2, w: r.width, h: r.height, ta}; }""", sel)


def gest():
    cases = [
        ("destinations/kenya.html", ".khero", "khero", None, "hero slideshow"),
        ("destinations/india.html", ".khero", "khero", None, "hero slideshow"),
        ("destinations/kenya.html", ".cfl-stage", "cfl", None, "photo ring"),
        ("destinations/india.html", ".cfl-stage", "cfl", None, "photo ring"),
        ("destinations/kenya.html", ".kmap-stage", "kmap", None, "kenya map"),
        ("index.html", ".episodes-viewport", "rail", ".episodes-viewport", "homepage episode strip"),
        ("podcast.html", ".testimonials-wrap", "rail", ".testimonials-wrap", "testimonial marquee"),
        ("podcast.html", ".yt-rail", "rail", ".yt-rail", "youtube rail"),
        ("index.html", "#epMap svg", "globe", None, "globe"),
    ]
    out = []
    with lib.server(PORT), lib.browser() as b:
        for path, sel, kind, arg, label in cases:
            ctx = ctx_for(b)
            pg = ctx.new_page()
            pg.goto(BASE + path, wait_until="load")
            pg.wait_for_timeout(1200)
            cdp = ctx.new_cdp_session(pg)
            c = center_of(pg, sel)
            rec = {"page": path, "sel": sel, "label": label, "box": c}
            if not c:
                rec["missing"] = True; out.append(rec); ctx.close(); continue
            pg.wait_for_timeout(500)
            st = lambda: pg.evaluate(STATE[kind], arg) if arg else pg.evaluate(STATE[kind])
            # stop autoplay drift: sample twice with no input to see if the state changes on its own
            s0 = st(); pg.wait_for_timeout(250); s0b = st()
            rec["drifts_without_input"] = s0 != s0b
            # horizontal swipe left (finger moves right-to-left by 60% of width), then right
            res = []
            for dx in (-0.6, 0.6):
                a = st()
                swipe(cdp, c["x"], c["y"], dx=dx * min(c["w"], 390) * 0.8)
                pg.wait_for_timeout(900)
                z = st()
                res.append({"dx": dx, "before": a, "after": z, "changed": {k: a[k] != z[k] for k in a if k != "y"},
                            "page_scrolled_px": z["y"] - a["y"]})
            rec["horizontal"] = res
            # vertical swipe (finger moves up 300px) starting on the component: page should scroll
            c = center_of(pg, sel)
            pg.wait_for_timeout(300)
            a = st()
            swipe(cdp, c["x"], c["y"], dy=-300)
            pg.wait_for_timeout(700)
            z = st()
            rec["vertical_page_scroll_px"] = z["y"] - a["y"]
            # pointer events seen during a horizontal swipe on the component
            pg.evaluate("""(sel) => { window.__pe=[]; const e=document.querySelector(sel);
                ['pointerdown','pointermove','pointerup','pointercancel'].forEach(t=>e.addEventListener(t,ev=>__pe.push(t+':'+ev.pointerType),{capture:true}));}""", sel)
            c = center_of(pg, sel)
            pg.wait_for_timeout(300)
            swipe(cdp, c["x"], c["y"], dx=-0.6 * min(c["w"], 390) * 0.8)
            pg.wait_for_timeout(600)
            pe = pg.evaluate("window.__pe")
            from collections import Counter
            rec["pointer_events"] = dict(Counter(pe))
            out.append(rec)
            print(label, path, "ta=", rec["box"]["ta"], "| H:", [(r["dx"], r["changed"], r["page_scrolled_px"]) for r in res],
                  "| V page scroll:", rec["vertical_page_scroll_px"], "| events:", rec["pointer_events"], "| drift:", rec["drifts_without_input"])
            ctx.close()
    json.dump(out, open(os.path.join(HERE, "touch_gest.json"), "w"), indent=1)


SCAN = r"""async () => {
  const vw = innerWidth, vh = innerHeight;
  function blocked(x, y) {
    let e = document.elementFromPoint(x, y);
    const hit = e;
    let pan = true, who = null;
    for (; e && e !== document.documentElement; e = e.parentElement || (e.getRootNode && e.getRootNode().host)) {
      const ta = getComputedStyle(e).touchAction;
      if (ta === 'none' || ta === 'pinch-zoom' || (/pan-x|pan-left|pan-right/.test(ta) && !/pan-y|pan-up|pan-down/.test(ta)) || ta === 'manipulation' && false) {
        pan = false; who = e; break;
      }
      const cs = getComputedStyle(e);
      if (e !== document.body && /(auto|scroll)/.test(cs.overflowY) && e.scrollHeight > e.clientHeight + 2) break; // nested scroller takes the pan
    }
    if (pan) return null;
    const d = who;
    return (d.tagName.toLowerCase() + (d.id ? '#' + d.id : '') + (typeof d.className === 'string' && d.className ? '.' + d.className.trim().split(/\s+/).slice(0, 2).join('.') : (d.className && d.className.baseVal ? '.' + d.className.baseVal.split(' ')[0] : ''))) + ' [' + getComputedStyle(d).touchAction + ']';
  }
  const H = document.documentElement.scrollHeight;
  const xs = [0.15, 0.5, 0.85].map(f => f * vw), ys = [0.25, 0.5, 0.75].map(f => f * vh);
  const steps = []; let worst = {frac: 0};
  for (let y0 = 0; y0 < H - vh * 0.5; y0 += Math.round(vh * 0.6)) {
    window.scrollTo({top: y0, behavior: 'instant'}); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    let n = 0, b = 0; const whos = {};
    for (const x of xs) for (const y of ys) { n++; const w = blocked(x, y); if (w) { b++; whos[w] = (whos[w] || 0) + 1; } }
    const midcol = ys.filter(y => blocked(vw / 2, y)).length;
    const s = {y: scrollY, frac: b / n, midcol, whos};
    steps.push(s); if (s.frac > worst.frac) worst = s;
  }
  window.scrollTo(0, 0);
  return {H, steps: steps.length, blockedSteps: steps.filter(s => s.frac > 0).length,
          fullSteps: steps.filter(s => s.frac >= 0.99).length, worst};
}"""


def scan_job(items):
    out = []
    with lib.browser() as b:
        ctx = ctx_for(b)
        pg = ctx.new_page()
        for path in items:
            rec = {"page": path}
            try:
                pg.goto(BASE + path, wait_until="load", timeout=30000)
                pg.wait_for_timeout(900)
                rec.update(pg.evaluate(SCAN))
            except Exception as e:
                rec["error"] = str(e)[:200]
            out.append(rec)
        ctx.close()
    return out


def scan(limit):
    items = lib.pages("live")[:limit]
    n = (len(items) + 3) // 4
    res = []
    with lib.server(PORT):
        with cf.ProcessPoolExecutor(4) as ex:
            for r in ex.map(scan_job, [items[i:i + n] for i in range(0, len(items), n)]):
                res.extend(r)
    json.dump(res, open(os.path.join(HERE, "touch_scan.json"), "w"), indent=1)
    flagged = [r for r in res if r.get("blockedSteps")]
    print("pages", len(res), "errors", sum(1 for r in res if "error" in r), "pages with any no-vertical-pan area", len(flagged))
    from collections import Counter
    who = Counter()
    for r in flagged:
        for k in r["worst"]["whos"]:
            who[k] += 1
    print("blocking elements (pages):", who.most_common(15))
    for r in sorted(flagged, key=lambda r: -r["worst"]["frac"])[:25]:
        print(" %-70s worst %.2f midcol %d/3 at y=%d  steps blocked %d/%d full %d" % (
            r["page"], r["worst"]["frac"], r["worst"]["midcol"], r["worst"]["y"], r["blockedSteps"], r["steps"], r["fullSteps"]))


def globe():
    """Swipe up the homepage from the top, in the centre column (through the globe) and near the edge."""
    with lib.server(PORT), lib.browser() as b:
        for x in (195, 20):
            ctx = ctx_for(b)
            pg = ctx.new_page()
            pg.goto(BASE + "index.html", wait_until="load"); pg.wait_for_timeout(1200)
            cdp = ctx.new_cdp_session(pg)
            g = pg.evaluate("""() => { const s=document.querySelector('#epMap svg');
                const r=s.getBoundingClientRect(); return {top: r.top + scrollY, h: r.height, w: r.width, left: r.left, ta: getComputedStyle(s).touchAction, sel: s.tagName + '#' + s.id + '.' + (s.getAttribute('class')||'')}; }""")
            # start just above the globe, then keep swiping up 400px at a time from y=600
            pg.evaluate("(y) => window.scrollTo(0, y)", max(0, g["top"] - 300))
            pg.wait_for_timeout(400)
            log = []
            for i in range(10):
                y0 = pg.evaluate("scrollY")
                under = pg.evaluate("""(p) => { const e=document.elementFromPoint(p[0],p[1]); return e ? e.tagName.toLowerCase()+'.'+((typeof e.className==='string'?e.className:(e.className&&e.className.baseVal))||'').split(' ')[0] : null; }""", [x, 600])
                swipe(cdp, x, 600, dy=-400)
                pg.wait_for_timeout(500)
                y1 = pg.evaluate("scrollY")
                log.append((under, y1 - y0))
            print("x=%d globe box %s | swipes (element under finger, page scroll px):" % (x, {k: (round(v) if isinstance(v, float) else v) for k, v in g.items()}))
            for l in log:
                print("   ", l)
            ctx.close()


if __name__ == "__main__":
    t0 = time.time()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "gest"
    if cmd == "gest":
        gest()
    elif cmd == "scan":
        scan(int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 6)
    elif cmd == "globe":
        globe()
    print("secs", round(time.time() - t0))
