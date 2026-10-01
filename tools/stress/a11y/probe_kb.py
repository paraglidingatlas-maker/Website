"""Targeted keyboard probes with screenshots (evidence for the findings).

python3 probe_kb.py iris        # knowledge-base.html: Tab past Skip goes behind the opaque intro overlay
python3 probe_kb.py marquee     # podcast.html: focused testimonial link keeps sliding away, no pause
python3 probe_kb.py mobar       # destinations: Enquire in the hidden mobile booking bar takes focus / bar covers focus
python3 probe_kb.py oclip       # index.html: focus ring of rail cards clipped by overflow
python3 probe_kb.py sitemap     # sitemap.html: what sits on top of the focused graph nodes
python3 probe_kb.py libmodal    # library.html: episode popup opened from a search result, focus trap / Escape
python3 probe_kb.py lightbox    # destinations/kenya.html: lightbox focus escape, then Escape
python3 probe_kb.py all
"""
import sys, json, os
sys.path.insert(0, "/home/user/Website/tools/stress")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, keyboard as K
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots"); os.makedirs(SHOTS, exist_ok=True)
INFO = "() => __kb.info(false)"


def tab_until(pg, js, limit=300):
    for i in range(limit):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(40)
        if pg.evaluate(js): return i + 1
    return None


def iris(b, base, vp="desktop"):
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, "knowledge-base.html")
    pg.wait_for_timeout(2500)
    out = {"vp": vp, "iris": pg.evaluate("() => { const i=document.getElementById('iris'), cs=getComputedStyle(i); return {role: i.getAttribute('role'), modal: i.getAttribute('aria-modal'), position: cs.position, z: cs.zIndex, bg: cs.backgroundColor, display: cs.display, rect: [i.getBoundingClientRect().width, i.getBoundingClientRect().height]}; }"),
           "active_before_tab": pg.evaluate("() => __kb.desc(document.activeElement)"), "stops": []}
    for n in range(1, 13):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(700)
        inf = pg.evaluate(INFO)
        top = pg.evaluate("() => { const e=document.activeElement; if (!e || e===document.body) return null; const r=e.getBoundingClientRect(); const h=document.elementFromPoint(Math.min(Math.max(r.left+r.width/2,0),innerWidth-1), Math.min(Math.max(r.top+r.height/2,0),innerHeight-1)); return h ? __kb.path(h) : null; }")
        out["stops"].append({"n": n, "d": inf.get("d"), "text": inf.get("text"), "rect": inf.get("rect"), "inside_iris": pg.evaluate("() => !!document.activeElement.closest('#iris')"), "on_top_at_center": top})
        if n in (1, 2, 5):
            pg.screenshot(path=os.path.join(SHOTS, "iris_%s_tab%d.png" % (vp, n)))
    behind = [s for s in out["stops"] if not s["inside_iris"]]
    out["stops_behind_overlay"] = len(behind)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
    out["escape_dismisses"] = pg.evaluate("() => !document.getElementById('iris')")
    ctx.close(); return out


def marquee(b, base, vp="mobile"):
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, "podcast.html")
    n = tab_until(pg, "() => document.activeElement.classList.contains('testi-video')")
    out = {"vp": vp, "tabs_to_first_testimonial": n, "timeline": []}
    for t in (0, 1000, 3000, 6000):
        if t: pg.wait_for_timeout(t - out["timeline"][-1]["t"])
        r = pg.evaluate("() => { const e=document.activeElement, r=e.getBoundingClientRect(), w=document.querySelector('.testimonials-wrap').getBoundingClientRect(); return {focused: e.classList.contains('testi-video'), left: Math.round(r.left), right: Math.round(r.right), wrap_left: Math.round(w.left), wrap_right: Math.round(w.right), visible_px: Math.max(0, Math.min(r.right, w.right, innerWidth) - Math.max(r.left, w.left, 0))}; }")
        r["t"] = t; out["timeline"].append(r)
        if t == 3000: pg.screenshot(path=os.path.join(SHOTS, "marquee_%s_3s.png" % vp))
    out["pause_controls"] = pg.evaluate("() => [...document.querySelectorAll('.testimonials-wrap button, [aria-label*=ause i], [class*=pause i]')].map(e => __kb.desc(e))")
    out["focusin_pauses"] = out["timeline"][0]["left"] == out["timeline"][-1]["left"]
    ctx.close(); return out


def mobar(b, base, vp="mobile", page="destinations/kenya.html"):
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, page)
    out = {"vp": vp, "page": page}
    out["bar_state_at_load"] = pg.evaluate("() => { const m=document.getElementById('dstMobar'); const r=m.getBoundingClientRect(); return {show: m.classList.contains('show'), top: Math.round(r.top), vh: innerHeight, aria_hidden: m.getAttribute('aria-hidden'), inert: m.inert, focusables: [...m.querySelectorAll('a,button')].map(e => __kb.desc(e) + ' tabindex=' + e.tabIndex)}; }")
    # focus the hidden bar's link by keyboard at the top of the page: Shift+Tab from the first stop wraps backwards
    pg.keyboard.press("Tab"); pg.wait_for_timeout(100)
    pg.keyboard.press("Shift+Tab"); pg.wait_for_timeout(100); pg.keyboard.press("Shift+Tab"); pg.wait_for_timeout(400)
    out["shift_tab_wrap_lands_on"] = pg.evaluate("() => { const e=document.activeElement, r=e.getBoundingClientRect(); return {d: __kb.desc(e), in_bar: !!e.closest('#dstMobar'), bar_show: document.getElementById('dstMobar').classList.contains('show'), top: Math.round(r.top), vh: innerHeight}; }")
    pg.screenshot(path=os.path.join(SHOTS, "mobar_%s_hidden_focus.png" % page.split('/')[-1][:-5]))
    # obscured: walk Tab; count stops whose centre is under the bar while it is shown
    pg.evaluate("() => { document.activeElement.blur(); scrollTo(0,0); }"); pg.wait_for_timeout(400)
    cov = []
    for i in range(140):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(450)
        r = pg.evaluate("() => { const e=document.activeElement; if (!e || e===document.body) return null; const m=document.getElementById('dstMobar'); if (e.closest('#dstMobar')) return null; const r=e.getBoundingClientRect(), b=m.getBoundingClientRect(); if (!m.classList.contains('show')) return null; const covered = Math.max(0, Math.min(r.bottom, b.bottom) - Math.max(r.top, b.top)); return covered > 0 ? {d: __kb.desc(e), text: (e.innerText||'').trim().slice(0,40), el_top: Math.round(r.top), el_bottom: Math.round(r.bottom), bar_top: Math.round(b.top), covered_px: Math.round(covered), covered_frac: +(covered / Math.max(1, r.height)).toFixed(2)} : null; }")
        if r:
            cov.append(r)
            if len(cov) == 1: pg.screenshot(path=os.path.join(SHOTS, "mobar_%s_covers_focus.png" % page.split('/')[-1][:-5]))
    out["focus_under_bar"] = cov
    out["fully_covered"] = sum(1 for c in cov if c["covered_frac"] >= 0.99)
    out["scroll_padding_bottom"] = pg.evaluate("() => getComputedStyle(document.documentElement).scrollPaddingBottom")
    ctx.close(); return out


def oclip(b, base, vp="desktop"):
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, "index.html")
    n = tab_until(pg, "() => document.activeElement.classList.contains('ep-card')")
    pg.wait_for_timeout(900)
    r = pg.evaluate("() => { const e=document.activeElement, r=e.getBoundingClientRect(), cs=getComputedStyle(e); const v=e.closest('.episodes-viewport').getBoundingClientRect(); return {d: __kb.desc(e), rect:[r.left,r.top,r.width,r.height].map(Math.round), outline: cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + cs.outlineColor + ' offset ' + cs.outlineOffset, viewport_rect:[v.left,v.top,v.width,v.height].map(Math.round), viewport_overflow: getComputedStyle(e.closest('.episodes-viewport')).overflow}; }")
    x, y, w, h = r["rect"]
    pg.screenshot(path=os.path.join(SHOTS, "oclip_index_%s.png" % vp), clip={"x": max(0, x - 20), "y": max(0, y - 20), "width": min(w + 40, 1400), "height": h + 40})
    r["tabs"] = n
    ctx.close(); return r


def sitemap(b, base, vp="desktop"):
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, "sitemap.html")
    n = tab_until(pg, "() => document.activeElement.classList && document.activeElement.classList.contains('sm-node')")
    pg.wait_for_timeout(700)
    r = pg.evaluate("() => { const e=document.activeElement, r=e.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); const cs=getComputedStyle(h); return {focused: __kb.desc(e), top: __kb.desc(h), fill: cs.fill, fill_opacity: cs.fillOpacity, opacity: cs.opacity, pointer: cs.pointerEvents, is_before_or_after_node: h.compareDocumentPosition(e) & 2 ? 'top element is after focused in DOM' : 'before'}; }")
    r["tabs"] = n
    pg.screenshot(path=os.path.join(SHOTS, "sitemap_%s_node_focus.png" % vp))
    ctx.close(); return r


def libmodal(b, base, vp="desktop"):
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, "library.html")
    out = {"vp": vp, "tiles_at_load": pg.evaluate("() => document.querySelectorAll('.ep-tile').length"),
           "visible_tiles_at_load": pg.evaluate("() => [...document.querySelectorAll('.ep-tile')].filter(e => e.getBoundingClientRect().width > 0).length")}
    n = tab_until(pg, "() => document.activeElement.matches('[data-ep-slug]')", 200)
    out["tabs_to_first_tile"] = n
    if not n:
        ctx.close(); return out
    pg.keyboard.press("Enter"); pg.wait_for_timeout(700)
    out["open"] = pg.evaluate("() => document.getElementById('epModalOverlay').classList.contains('active')")
    out["focus_on_open"] = pg.evaluate("() => __kb.desc(document.activeElement)")
    seq = []
    for i in range(25):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(50)
        seq.append(pg.evaluate("() => !!document.activeElement.closest('#epModalOverlay')"))
    out["escaped_at_tab"] = (seq.index(False) + 1) if False in seq else None
    pg.keyboard.press("Escape"); pg.wait_for_timeout(900)
    out["closed"] = not pg.evaluate("() => document.getElementById('epModalOverlay').classList.contains('active')")
    out["focus_after_escape"] = pg.evaluate("() => __kb.desc(document.activeElement) + (document.activeElement.matches('[data-ep-slug]') ? ' (the tile)' : '')")
    ctx.close(); return out


def lightbox(b, base, vp="desktop"):
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, "destinations/kenya.html")
    pg.evaluate("() => document.querySelector('.cfl').scrollIntoView({block:'center'})"); pg.wait_for_timeout(600)
    n = tab_until(pg, "() => document.activeElement.classList.contains('cfl-card')", 400)
    pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
    out = {"vp": vp, "open": pg.evaluate("() => !document.querySelector('.cfl-lb').hidden"), "focus_on_open": pg.evaluate("() => __kb.desc(document.activeElement)")}
    pg.screenshot(path=os.path.join(SHOTS, "lightbox_%s_open.png" % vp))
    for i in range(4):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(400)
    out["after_4_tabs"] = pg.evaluate("() => { const e=document.activeElement, r=e.getBoundingClientRect(); const h=document.elementFromPoint(Math.min(Math.max(r.left+r.width/2,0),innerWidth-1), Math.min(Math.max(r.top+r.height/2,0),innerHeight-1)); return {d: __kb.desc(e), text: (e.innerText||'').trim().slice(0,30), inside_lightbox: !!e.closest('.cfl-lb'), top_at_centre: h && __kb.path(h), lightbox_open: !document.querySelector('.cfl-lb').hidden}; }")
    pg.screenshot(path=os.path.join(SHOTS, "lightbox_%s_after4tabs.png" % vp))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    out["escape_closes"] = pg.evaluate("() => document.querySelector('.cfl-lb').hidden")
    out["body_overflow"] = pg.evaluate("() => document.body.style.overflow")
    pg.keyboard.press("Shift+Tab"); pg.wait_for_timeout(200); pg.keyboard.press("Shift+Tab"); pg.wait_for_timeout(200)
    pg.keyboard.press("Shift+Tab"); pg.wait_for_timeout(200)
    out["shift_tab_x3_back_inside"] = pg.evaluate("() => !!document.activeElement.closest('.cfl-lb')")
    ctx.close(); return out


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    if "all" in which: which = ["iris", "marquee", "mobar", "oclip", "sitemap", "libmodal", "lightbox"]
    res = {}
    with lib.server(K.PORT) as base, lib.browser() as b:
        for w in which:
            try:
                if w == "iris": res["iris"] = [iris(b, base, "desktop"), iris(b, base, "mobile")]
                if w == "marquee": res["marquee"] = [marquee(b, base, "mobile"), marquee(b, base, "desktop")]
                if w == "mobar": res["mobar"] = [mobar(b, base, "mobile", "destinations/kenya.html"), mobar(b, base, "mobile", "destinations/india.html")]
                if w == "oclip": res["oclip"] = [oclip(b, base, "desktop"), oclip(b, base, "mobile")]
                if w == "sitemap": res["sitemap"] = [sitemap(b, base, "desktop")]
                if w == "libmodal": res["libmodal"] = [libmodal(b, base, "desktop"), libmodal(b, base, "mobile")]
                if w == "lightbox": res["lightbox"] = [lightbox(b, base, "desktop"), lightbox(b, base, "mobile")]
            except Exception as e:
                res[w] = {"error": repr(e)[:400]}
            print(w, json.dumps(res.get(w), default=str)[:3000], "\n", flush=True)
    fn = "results_probe_kb.json" if len(which) > 2 else "results_probe_kb_%s.json" % "_".join(which)
    json.dump(res, open(os.path.join(HERE, fn), "w"), indent=1, default=str)
