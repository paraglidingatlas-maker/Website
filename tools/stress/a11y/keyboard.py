"""Keyboard-only checks on the LIVE templates (repo root).

python3 keyboard.py                         # everything: tab runs (desktop+mobile), menu, search, modals, lightbox, form
python3 keyboard.py --only tab --vp desktop --pages index.html
python3 keyboard.py --only menu|search|modal|lightbox|form [--pages ...] [--vp mobile|desktop]

Tab run: presses Tab up to 300 times, records each focused element, flags focus on
hidden/offscreen/obscured elements, focus lost to <body> mid-page, traps, skip link,
and compares computed styles of every focused element against its unfocused state
(element, ::before/::after, parent, descendants). Elements with no style change are
re-checked with a screenshot diff (focused vs blurred).
"""
import argparse, io, json, os, sys, time, multiprocessing as mp
sys.path.insert(0, "/home/user/Website/tools/stress")
import lib

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8815
VPS = {"desktop": {"width": 1440, "height": 900}, "mobile": {"width": 390, "height": 844}}

HELPERS = r"""
window.__kb = (() => {
  const desc = n => { if (!n || n.nodeType !== 1) return String(n && n.nodeName);
    let s = n.tagName.toLowerCase(); if (n.id) s += '#' + n.id;
    const c = (n.getAttribute('class') || '').trim().split(/\s+/).filter(Boolean).slice(0, 3);
    if (c.length) s += '.' + c.join('.'); return s; };
  const path = n => { const a = []; for (let x = n; x && x.nodeType === 1 && a.length < 4; x = x.parentElement) a.unshift(desc(x)); return a.join(' > '); };
  const PROPS = ['outline-style','outline-width','outline-color','outline-offset','box-shadow','border-top-color','border-right-color',
    'border-bottom-color','border-left-color','border-top-width','border-bottom-width','background-color','background-image','color',
    'text-decoration-line','text-decoration-color','transform','translate','scale','filter','opacity','fill','stroke'];
  const one = (n, ps) => { const cs = getComputedStyle(n, ps); const o = {};
    for (const p of PROPS) o[p] = cs.getPropertyValue(p);
    if (ps) { o.content = cs.content; o.width = cs.width; o.height = cs.height; o.display = cs.display; }
    return o; };
  const snap = el => { const o = {self: one(el), before: one(el, '::before'), after: one(el, '::after'),
      parent: el.parentElement ? one(el.parentElement) : null, kids: []};
    const ks = el.querySelectorAll('*');
    for (let i = 0; i < ks.length && i < 25; i++) { o.kids.push(one(ks[i])); o.kids.push(one(ks[i], '::after')); o.kids.push(one(ks[i], '::before')); }
    return o; };
  const hidden = el => {
    const why = []; const r = el.getBoundingClientRect();
    const cs0 = getComputedStyle(el);
    if ((r.width < 2 || r.height < 2) && cs0.display !== 'contents') why.push('zero-size ' + Math.round(r.width) + 'x' + Math.round(r.height));
    if (cs0.visibility !== 'visible') why.push('visibility:' + cs0.visibility);
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (parseFloat(cs.opacity) < 0.1) why.push('opacity ' + cs.opacity + ' on ' + desc(n));
      if (n.getAttribute('aria-hidden') === 'true') why.push('inside aria-hidden ' + desc(n));
      if (n.inert) why.push('inert ' + desc(n));
      if (cs.clipPath && /inset\(50%|circle\(0/.test(cs.clipPath)) why.push('clip-path on ' + desc(n));
      if (n !== el && n !== document.body && n !== document.documentElement && /hidden|clip|scroll|auto/.test(cs.overflowX + cs.overflowY)) {
        const pr = n.getBoundingClientRect();
        if (pr.width > 0 && (r.right <= pr.left + 1 || r.left >= pr.right - 1 || r.bottom <= pr.top + 1 || r.top >= pr.bottom - 1))
          why.push('clipped by overflow of ' + desc(n));
      }
    }
    if (r.right <= 0 || r.bottom <= 0 || r.left >= innerWidth || r.top >= innerHeight)
      why.push('offscreen at ' + Math.round(r.left) + ',' + Math.round(r.top));
    return why; };
  const obscured = el => { const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2 || r.bottom <= 0 || r.top >= innerHeight || r.right <= 0 || r.left >= innerWidth) return null;
    const pts = [[r.left + r.width / 2, r.top + r.height / 2], [r.left + 3, r.top + 3], [r.right - 3, r.bottom - 3]];
    let bad = 0, by = null;
    for (const [x, y] of pts) { const cx = Math.min(Math.max(x, 0), innerWidth - 1), cy = Math.min(Math.max(y, 0), innerHeight - 1);
      const h = document.elementFromPoint(cx, cy);
      if (h && h !== el && !el.contains(h) && !h.contains(el)) { bad++; by = by || desc(h) + ' [' + path(h) + ']'; } }
    return bad === 3 ? by : null; };
  const outlineClip = el => { const cs = getComputedStyle(el);
    if (cs.outlineStyle === 'none' || parseFloat(cs.outlineWidth) === 0) return null;
    const e = parseFloat(cs.outlineOffset || 0) + parseFloat(cs.outlineWidth); const r = el.getBoundingClientRect();
    const R = {l: r.left - e, t: r.top - e, r: r.right + e, b: r.bottom + e};
    for (let n = el.parentElement; n && n !== document.body; n = n.parentElement) {
      const c = getComputedStyle(n); if (!/hidden|clip|scroll|auto/.test(c.overflowX + c.overflowY)) continue;
      const p = n.getBoundingClientRect(); const sides = [];
      if (R.l < p.left - 0.5) sides.push('left'); if (R.t < p.top - 0.5) sides.push('top');
      if (R.r > p.right + 0.5) sides.push('right'); if (R.b > p.bottom + 0.5) sides.push('bottom');
      if (sides.length) return {by: desc(n), sides}; }
    return null; };
  let idx = 0;
  const info = (withSnap) => { const el = document.activeElement;
    if (!el || el === document.body || el === document.documentElement) return {body: true, scrollY: Math.round(scrollY)};
    if (!el.dataset.kbi) el.dataset.kbi = String(idx++);
    const r = el.getBoundingClientRect();
    return {kbi: +el.dataset.kbi, d: desc(el), path: path(el),
      text: (el.getAttribute('aria-label') || el.innerText || el.value || el.getAttribute('title') || '').trim().replace(/\s+/g, ' ').slice(0, 60),
      href: el.getAttribute('href'), tag: el.tagName, tabindex: el.getAttribute('tabindex'),
      rect: [r.left, r.top, r.width, r.height].map(Math.round), hid: hidden(el), obs: obscured(el), oclip: outlineClip(el),
      inHeader: !!el.closest('.page-wrap > nav'), inMain: !!el.closest('main, [role=main]'),
      fv: el.matches(':focus-visible'), snap: withSnap ? snap(el) : null, scrollY: Math.round(scrollY)}; };
  return {desc, path, snap, hidden, obscured, info};
})();
"""

RING = {"outline-style", "outline-width", "outline-color", "box-shadow", "border-top-color", "border-right-color",
        "border-bottom-color", "border-left-color", "border-top-width", "border-bottom-width", "background-color",
        "background-image", "text-decoration-line", "text-decoration-color", "content", "width", "height", "display",
        "fill", "stroke"}


def classify(f, u):
    """f focused snapshot, u unfocused. -> ('ring'|'weak'|'none', [changed props])"""
    changed = []
    def cmp(a, b, where):
        if not a or not b:
            return
        for k in a:
            if a.get(k) != b.get(k):
                if k == "outline-style" or k == "outline-width":
                    pass
                changed.append(where + ":" + k)
    cmp(f["self"], u["self"], "self")
    cmp(f["before"], u["before"], "::before")
    cmp(f["after"], u["after"], "::after")
    cmp(f["parent"], u["parent"], "parent")
    for i, (a, b) in enumerate(zip(f["kids"], u["kids"])):
        cmp(a, b, "kid%d" % (i // 3))
    # outline present on self while focused counts as a ring even if same as unfocused (e.g. always-on)
    so = f["self"]
    if so["outline-style"] != "none" and so["outline-width"] not in ("0px", "") and "rgba(0, 0, 0, 0)" not in so["outline-color"] \
            and any(c.startswith("self:outline") for c in changed):
        return "ring", changed
    if any(c.split(":", 1)[1] in RING for c in changed):
        return "ring", changed
    if changed:
        return "weak", changed
    return "none", changed


def new_ctx(b, base, vp, reduced=False):
    ctx = b.new_context(viewport=vp, reduced_motion="reduce" if reduced else "no-preference")
    ctx.route("**/*", lambda route: route.continue_() if lib.own(route.request.url, base) or
              route.request.url.startswith(("data:", "blob:")) else route.abort())
    return ctx


def load(ctx, base, path):
    pg = ctx.new_page()
    pg.goto(base + path, wait_until="load", timeout=45000)
    pg.wait_for_timeout(1200)
    pg.evaluate(HELPERS)
    return pg


def shot_diff(pg, rect):
    from PIL import Image, ImageChops
    vp = pg.viewport_size
    x = max(0, rect[0] - 10); y = max(0, rect[1] - 10)
    w = min(vp["width"], rect[0] + rect[2] + 10) - x; h = min(vp["height"], rect[1] + rect[3] + 10) - y
    if w < 4 or h < 4:
        return None
    clip = {"x": x, "y": y, "width": w, "height": h}
    return clip


def verify_none(pg, kbis):
    """Screenshot diff focused vs blurred for elements whose styles did not change."""
    from PIL import Image, ImageChops
    out = {}
    for k in kbis[:12]:
        sel = '[data-kbi="%d"]' % k
        try:
            pg.evaluate("s => document.querySelector(s).scrollIntoView({block:'center'})", sel)
            pg.wait_for_timeout(250)
            pg.keyboard.press("Shift")
            pg.evaluate("s => document.querySelector(s).focus()", sel)
            pg.wait_for_timeout(350)
            st = pg.evaluate("s => {const e=document.querySelector(s); const r=e.getBoundingClientRect(); return {a: document.activeElement===e, fv: e.matches(':focus-visible'), r:[r.left,r.top,r.width,r.height].map(Math.round)}}", sel)
            clip = shot_diff(pg, st["r"])
            if not clip:
                out[k] = {"skip": "no visible rect", **st}; continue
            a = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
            pg.evaluate("() => document.activeElement && document.activeElement.blur()")
            pg.wait_for_timeout(400)
            b2 = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
            pg.wait_for_timeout(400)
            b3 = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
            def frac(p, q):
                d = ImageChops.difference(p, q).convert("L").point(lambda v: 255 if v > 40 else 0)
                return round(sum(1 for v in d.getdata() if v) / (d.size[0] * d.size[1]), 4)
            out[k] = {"focused": st["a"], "fv": st["fv"], "diff_focus_vs_blur": frac(a, b2), "diff_blur_vs_blur": frac(b2, b3), "clip": clip}
        except Exception as e:
            out[k] = {"err": str(e)[:200]}
    return out


def tab_run(b, base, path, vpname, presses=300):
    vp = VPS[vpname]
    ctx = new_ctx(b, base, vp)
    pg = load(ctx, base, path)
    res = {"page": path, "vp": vpname}
    res["positive_tabindex"] = pg.evaluate("() => [...document.querySelectorAll('[tabindex]')].filter(e => +e.getAttribute('tabindex') > 0).map(e => __kb.desc(e))")
    res["has_main"] = pg.evaluate("() => !!document.querySelector('main, [role=main]')")
    seq, snaps = [], {}
    first, done, last_k, same = None, False, None, 0
    for i in range(presses):
        pg.keyboard.press("Tab")
        pg.wait_for_timeout(70)
        inf = pg.evaluate("w => __kb.info(w)", True)
        if inf.get("hid"):
            RECHK = "() => { const e=document.activeElement; if (!e || e===document.body) return null; const r=e.getBoundingClientRect(); const h=__kb.hidden(e); return h.length ? {why: h, rect: [r.left,r.top,r.width,r.height].map(Math.round), vh: innerHeight} : null; }"
            pg.wait_for_timeout(600)  # smooth scroll settles
            again = pg.evaluate(RECHK)
            if again:
                pg.wait_for_timeout(1600)  # reveal transitions (up to .9s + .42s delay) finish
                again = pg.evaluate(RECHK)
            inf["hid_after_800ms"] = again
        k = inf.get("kbi")
        if k is not None and k not in snaps:
            snaps[k] = inf["snap"]
        inf.pop("snap", None)
        inf["i"] = i + 1
        seq.append(inf)
        if k is not None:
            if first is None:
                first = k
            elif k == first:
                done = True
                break
            same = same + 1 if k == last_k else 0
            last_k = k
            if same >= 10:
                res["stuck_on"] = inf; break
    res["presses"] = len(seq)
    res["cycle_complete"] = done
    # body occurrences that are not the wrap at the end of the cycle
    lost = []
    for j, s in enumerate(seq):
        if s.get("body"):
            nxt = next((t for t in seq[j + 1:] if not t.get("body")), None)
            if nxt is not None and nxt.get("kbi") != first and nxt.get("kbi") is not None:
                prev = next((t for t in reversed(seq[:j]) if not t.get("body")), None)
                lost.append({"at_press": s["i"], "after": prev and prev["d"], "next": nxt["d"], "scrollY": s["scrollY"]})
    res["focus_lost_to_body"] = lost
    stops = [s for s in seq if not s.get("body")]
    uniq = []
    seen = set()
    for s in stops:
        if s["kbi"] not in seen:
            seen.add(s["kbi"]); uniq.append(s)
    res["tab_stops"] = len(uniq)
    res["iframes"] = [s["d"] for s in uniq if s["tag"] == "IFRAME"]
    # skip link
    f0 = uniq[0] if uniq else None
    res["first_stop"] = f0 and {"d": f0["d"], "text": f0["text"], "href": f0["href"]}
    res["skip_link"] = bool(f0 and (f0["href"] or "").startswith("#") and len(f0["href"]) > 1)
    first_out = next((n for n, s in enumerate(uniq) if not s["inHeader"]), None)
    res["stops_before_leaving_nav"] = first_out
    first_main = next((n for n, s in enumerate(uniq) if s["inMain"]), None)
    res["stops_before_main"] = first_main
    # hidden / offscreen / obscured
    res["hidden_focus"] = [{"i": s["i"], "d": s["d"], "path": s["path"], "text": s["text"], "why": s["hid"],
                            "after_2s": s.get("hid_after_800ms"), "rect": s["rect"]}
                           for s in stops if s.get("hid") and s.get("hid_after_800ms")]
    res["hidden_transient"] = [{"i": s["i"], "d": s["d"], "why": s["hid"]} for s in stops if s.get("hid") and not s.get("hid_after_800ms")]
    res["obscured"] = [{"i": s["i"], "d": s["d"], "text": s["text"], "by": s["obs"], "rect": s["rect"]} for s in stops if s.get("obs") and not s.get("hid")]
    res["outline_clipped"] = [{"i": s["i"], "d": s["d"], "text": s["text"], **s["oclip"]} for s in uniq if s.get("oclip")]
    res["not_focus_visible"] = [{"i": s["i"], "d": s["d"]} for s in uniq if not s["fv"]]
    # unfocused snapshots
    pg.evaluate("() => document.activeElement && document.activeElement.blur()")
    pg.mouse.move(vp["width"] - 2, vp["height"] - 2)
    pg.wait_for_timeout(600)
    unf = dict(pg.evaluate("() => [...document.querySelectorAll('[data-kbi]')].map(e => [+e.dataset.kbi, __kb.snap(e)])"))
    ind = {}
    for s in uniq:
        k = s["kbi"]
        if k not in unf or k not in snaps:
            ind[k] = ("gone", []); continue
        ind[k] = classify(snaps[k], unf[k])
    none = [s for s in uniq if ind[s["kbi"]][0] == "none" and not s.get("hid") and s["tag"] != "IFRAME"]
    weak = [s for s in uniq if ind[s["kbi"]][0] == "weak" and not s.get("hid")]
    ver = verify_none(pg, [s["kbi"] for s in none])
    res["indicator_counts"] = {c: sum(1 for v in ind.values() if v[0] == c) for c in ("ring", "weak", "none", "gone")}
    res["no_indicator"] = [{"i": s["i"], "d": s["d"], "path": s["path"], "text": s["text"], "href": s["href"], "rect": s["rect"],
                            "verify": ver.get(s["kbi"])} for s in none]
    res["weak_indicator"] = [{"i": s["i"], "d": s["d"], "text": s["text"], "changed": ind[s["kbi"]][1][:6]} for s in weak]
    res["sequence"] = [{"i": s["i"], "d": s.get("d", "BODY"), "text": s.get("text", ""), "rect": s.get("rect")} for s in seq]
    ctx.close()
    return res


def menu_test(b, base, path):
    ctx = new_ctx(b, base, VPS["mobile"])
    pg = load(ctx, base, path)
    r = {"page": path}
    for i in range(15):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(40)
        if pg.evaluate("() => document.activeElement.classList.contains('nav-toggle')"):
            r["toggle_reached_after"] = i + 1; break
    if "toggle_reached_after" not in r:
        r["toggle_reached_after"] = None
        r["first_stops"] = pg.evaluate("() => __kb.desc(document.activeElement)")
        ctx.close(); return r
    pg.keyboard.press("Enter"); pg.wait_for_timeout(400)
    r["expanded_after_enter"] = pg.evaluate("() => document.querySelector('.nav-toggle').getAttribute('aria-expanded')")
    r["focus_after_open"] = pg.evaluate("() => __kb.desc(document.activeElement)")
    items = []
    for i in range(12):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(60)
        inf = pg.evaluate("() => __kb.info(false)")
        inl = pg.evaluate("() => !!(document.activeElement.closest && document.activeElement.closest('.nav-links'))")
        items.append({"d": inf.get("d", "BODY"), "text": inf.get("text"), "in_menu": inl, "hid": inf.get("hid"), "obs": inf.get("obs")})
        if not inl:
            break
    r["tab_through_menu"] = items
    r["menu_items_reached"] = sum(1 for x in items if x["in_menu"])
    r["menu_links_total"] = pg.evaluate("() => document.querySelectorAll('.nav-links a').length")
    r["still_open_after_leaving"] = pg.evaluate("() => document.querySelector('.nav-toggle').getAttribute('aria-expanded')")
    r["left_to_obscured"] = items[-1]["obs"] if items and not items[-1]["in_menu"] else None
    # Escape from inside the menu
    pg.evaluate("() => { const t=document.querySelector('.nav-toggle'); if (t.getAttribute('aria-expanded')!=='true') t.click(); document.querySelector('.nav-links a').focus(); }")
    pg.wait_for_timeout(200)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    r["escape_closes"] = pg.evaluate("() => document.querySelector('.nav-toggle').getAttribute('aria-expanded') === 'false'")
    r["focus_after_escape"] = pg.evaluate("() => __kb.desc(document.activeElement)")
    # closed menu: next Tab from toggle must not land in hidden links
    pg.evaluate("() => document.querySelector('.nav-toggle').focus()")
    pg.keyboard.press("Tab"); pg.wait_for_timeout(60)
    r["after_close_next_tab"] = pg.evaluate("() => ({d: __kb.desc(document.activeElement), in_menu: !!document.activeElement.closest('.nav-links'), hid: __kb.hidden(document.activeElement)})")
    ctx.close()
    return r


def search_test(b, base, vpname):
    ctx = new_ctx(b, base, VPS[vpname])
    pg = load(ctx, base, "index.html")
    r = {"page": "index.html", "vp": vpname}
    # reach the input by Tab (keyboard only)
    n = 0
    for n in range(1, 400):
        pg.keyboard.press("Tab")
        if pg.evaluate("() => document.activeElement.id === 'epSearchInput'"):
            break
    else:
        n = None
    r["tabs_to_search_input"] = n
    if n is None:
        pg.focus("#epSearchInput")
    pg.keyboard.type("safety", delay=30); pg.wait_for_timeout(300)
    r["results_open"] = pg.evaluate("() => document.getElementById('epSearchResults').classList.contains('active')")
    r["results_count"] = pg.evaluate("() => document.querySelectorAll('#epSearchResults a').length")
    r["aria"] = pg.evaluate("""() => { const i=document.getElementById('epSearchInput'), b=document.getElementById('epSearchResults');
        return {input_role: i.getAttribute('role'), aria_expanded: i.getAttribute('aria-expanded'), aria_controls: i.getAttribute('aria-controls'),
          results_live: b.getAttribute('aria-live') || (b.closest('[aria-live]') && 'ancestor') || null, results_role: b.getAttribute('role'),
          any_status_region: !!document.querySelector('.ep-search-section [role=status], .ep-search-section [aria-live]')}; }""")
    pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(150)
    r["arrowdown_moves_into_results"] = pg.evaluate("() => !!document.activeElement.closest('#epSearchResults')")
    seq = []
    for i in range(3):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(80)
        seq.append(pg.evaluate("() => ({d: __kb.desc(document.activeElement), inResults: !!document.activeElement.closest('#epSearchResults')})"))
    r["tab_after_typing"] = seq
    pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
    r["escape_closes_results"] = not pg.evaluate("() => document.getElementById('epSearchResults').classList.contains('active')")
    # tab away past the results: do they close when focus leaves the section?
    for i in range(12):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(50)
        if not pg.evaluate("() => !!document.activeElement.closest('.ep-search-section')"):
            break
    pg.wait_for_timeout(200)
    r["focus_left_section_to"] = pg.evaluate("() => __kb.info(false)")
    r["results_still_open_after_focus_left"] = pg.evaluate("() => document.getElementById('epSearchResults').classList.contains('active')")
    r["results_box"] = pg.evaluate("() => { const b=document.getElementById('epSearchResults'), cs=getComputedStyle(b), q=b.getBoundingClientRect(); return {position: cs.position, rect:[q.left,q.top,q.width,q.height].map(Math.round), z: cs.zIndex}; }")
    ctx.close()
    # library search: is the filtered count announced?
    ctx = new_ctx(b, base, VPS[vpname])
    pg = load(ctx, base, "library.html")
    pg.focus("#q") if pg.evaluate("() => { const e=document.getElementById('q'); return !!(e && e.offsetParent); }") else pg.focus("#q2")
    before = pg.evaluate("() => document.querySelectorAll('[data-ep-slug]').length")
    pg.keyboard.type("safety", delay=30); pg.wait_for_timeout(600)
    r["library"] = {"tiles_before": before, "tiles_after": pg.evaluate("() => [...document.querySelectorAll('[data-ep-slug]')].filter(e => e.offsetParent).length"),
                    "live_regions": pg.evaluate("() => [...document.querySelectorAll('[aria-live],[role=status],[role=alert]')].map(e => __kb.desc(e) + ' = ' + (e.textContent||'').trim().slice(0,80))")}
    ctx.close()
    return r


def modal_test(b, base, path, vpname):
    """Episode popup (episode-modal.js). Open with Enter on a tile, then Tab / Shift+Tab / Escape."""
    out = {"page": path, "vp": vpname}
    ctx = new_ctx(b, base, VPS[vpname])
    pg = load(ctx, base, path)
    sel = pg.evaluate("""() => { const t=[...document.querySelectorAll('[data-ep-slug],[data-ep-index]')].find(e => { const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && getComputedStyle(e).visibility==='visible'; });
       if (!t) return null; t.setAttribute('data-kbt','1'); t.scrollIntoView({block:'center'}); return __kb.desc(t); }""")
    out["tile"] = sel
    if not sel:
        ctx.close(); out["skip"] = "no visible tile"; return out
    pg.wait_for_timeout(300)
    pg.keyboard.press("Shift")
    pg.focus('[data-kbt="1"]')
    pg.keyboard.press("Enter"); pg.wait_for_timeout(700)
    out["open"] = pg.evaluate("() => document.getElementById('epModalOverlay').classList.contains('active')")
    out["focus_on_open"] = pg.evaluate("() => ({d: __kb.desc(document.activeElement), inside: !!document.activeElement.closest('#epModalOverlay')})")
    out["dialog_attrs"] = pg.evaluate("() => { const c=document.querySelector('#epModalOverlay [role=dialog]'); return c && {role: c.getAttribute('role'), modal: c.getAttribute('aria-modal'), label: c.getAttribute('aria-label')}; }")
    out["focusables_in_dialog"] = pg.evaluate("() => document.querySelectorAll('#epModalOverlay a[href], #epModalOverlay button').length")
    out["background_inert"] = pg.evaluate("() => [...document.body.children].filter(e => e.id !== 'epModalOverlay' && (e.inert || e.getAttribute('aria-hidden')==='true')).length")
    seq = []
    for i in range(30):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(60)
        seq.append(pg.evaluate("() => ({d: __kb.desc(document.activeElement), inside: !!document.activeElement.closest('#epModalOverlay'), obs: document.activeElement===document.body ? null : __kb.obscured(document.activeElement)})"))
    out["tab_seq"] = seq
    esc_i = next((i for i, s in enumerate(seq) if not s["inside"]), None)
    out["focus_escaped_at_tab"] = None if esc_i is None else esc_i + 1
    out["escaped_to"] = None if esc_i is None else seq[esc_i]
    out["escaped_stops_obscured"] = sum(1 for s in seq if not s["inside"] and s["obs"])
    out["escaped_stops"] = sum(1 for s in seq if not s["inside"])
    out["still_open_while_focus_outside"] = pg.evaluate("() => document.getElementById('epModalOverlay').classList.contains('active')")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(900)
    out["escape_closes_even_when_focus_outside"] = not pg.evaluate("() => document.getElementById('epModalOverlay').classList.contains('active')")
    ctx.close()
    # fresh: Shift+Tab immediately, then Escape returns focus?
    ctx = new_ctx(b, base, VPS[vpname])
    pg = load(ctx, base, path)
    pg.evaluate("""() => { const t=[...document.querySelectorAll('[data-ep-slug],[data-ep-index]')].find(e => { const r=e.getBoundingClientRect(); return r.width>0 && r.height>0; }); t.setAttribute('data-kbt','1'); t.scrollIntoView({block:'center'}); }""")
    pg.wait_for_timeout(300)
    pg.keyboard.press("Shift"); pg.focus('[data-kbt="1"]')
    pg.keyboard.press("Enter"); pg.wait_for_timeout(700)
    pg.keyboard.press("Shift+Tab"); pg.wait_for_timeout(80)
    out["shift_tab_from_card"] = pg.evaluate("() => ({d: __kb.desc(document.activeElement), inside: !!document.activeElement.closest('#epModalOverlay')})")
    pg.keyboard.press("Tab"); pg.wait_for_timeout(80)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(900)
    out["closed_after_escape"] = not pg.evaluate("() => document.getElementById('epModalOverlay').classList.contains('active')")
    out["focus_after_escape"] = pg.evaluate("() => ({d: __kb.desc(document.activeElement), is_tile: document.activeElement.getAttribute('data-kbt')==='1'})")
    out["url_after_escape"] = pg.url
    ctx.close()
    return out


def lightbox_test(b, base, path, vpname):
    out = {"page": path, "vp": vpname}
    ctx = new_ctx(b, base, VPS[vpname])
    pg = load(ctx, base, path)
    if not pg.evaluate("() => !!document.querySelector('.cfl-lb')"):
        ctx.close(); out["skip"] = "no lightbox"; return out
    pg.evaluate("() => document.querySelector('.cfl').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(600)
    # reach the front card by Tab from the element before the gallery
    n = None
    for i in range(400):
        pg.keyboard.press("Tab")
        if pg.evaluate("() => document.activeElement.classList.contains('cfl-card')"):
            n = i + 1; break
    out["tabs_to_front_card"] = n
    out["card"] = pg.evaluate("() => __kb.info(false)")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
    out["open"] = pg.evaluate("() => !document.querySelector('.cfl-lb').hidden")
    out["focus_on_open"] = pg.evaluate("() => __kb.desc(document.activeElement)")
    seq = []
    for i in range(20):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(60)
        seq.append(pg.evaluate("() => ({d: __kb.desc(document.activeElement), inside: !!document.activeElement.closest('.cfl-lb'), inRoot: !!document.activeElement.closest('.cfl'), obs: document.activeElement===document.body ? null : __kb.obscured(document.activeElement)})"))
    out["tab_seq"] = seq
    esc_i = next((i for i, s in enumerate(seq) if not s["inside"]), None)
    out["focus_escaped_at_tab"] = None if esc_i is None else esc_i + 1
    out["escaped_to"] = None if esc_i is None else seq[esc_i]
    out["escaped_stops_obscured"] = sum(1 for s in seq if not s["inside"] and s["obs"])
    out["escaped_stops"] = sum(1 for s in seq if not s["inside"])
    out["focus_now"] = seq[-1]
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    out["escape_closes_when_focus_left_gallery"] = pg.evaluate("() => document.querySelector('.cfl-lb').hidden")
    out["body_overflow_after"] = pg.evaluate("() => document.body.style.overflow")
    ctx.close()
    # fresh: Escape straight away
    ctx = new_ctx(b, base, VPS[vpname])
    pg = load(ctx, base, path)
    pg.evaluate("() => document.querySelector('.cfl').scrollIntoView({block:'center'})"); pg.wait_for_timeout(600)
    pg.keyboard.press("Shift")
    pg.evaluate("() => [...document.querySelectorAll('.cfl-card')].find(c => c.tabIndex === 0).focus()")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    out["escape_closes_immediately"] = pg.evaluate("() => document.querySelector('.cfl-lb').hidden")
    out["focus_after_escape"] = pg.evaluate("() => ({d: __kb.desc(document.activeElement), front: document.activeElement.classList.contains('cfl-card') && document.activeElement.tabIndex===0})")
    out["lightbox_markup"] = pg.evaluate("() => { const l=document.querySelector('.cfl-lb'); return {role: l.getAttribute('role'), modal: l.getAttribute('aria-modal'), inside_root: !!l.closest('.cfl'), buttons: [...l.querySelectorAll('button')].map(b => (b.getAttribute('aria-label')||b.textContent).trim())}; }")
    ctx.close()
    return out


def form_test(b, base, vpname):
    ctx = new_ctx(b, base, VPS[vpname])
    pg = load(ctx, base, "enquire.html")
    r = {"page": "enquire.html", "vp": vpname}
    order = []
    for i in range(80):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(30)
        d = pg.evaluate("() => ({d: __kb.desc(document.activeElement), inForm: !!document.activeElement.closest('#enqForm'), type: document.activeElement.type || ''})")
        if d["inForm"]:
            order.append(d["d"])
        if d["type"] == "submit" and d["inForm"]:
            break
    r["form_tab_order"] = order
    pg.keyboard.press("Enter"); pg.wait_for_timeout(400)
    r["focus_after_empty_submit"] = pg.evaluate("() => __kb.desc(document.activeElement)")
    r["status_text"] = pg.evaluate("() => document.getElementById('enqStatus').textContent")
    ctx.close()
    return r


def job(args):
    kind, base, a1, a2 = args
    t0 = time.time()
    try:
        with lib.browser() as b:
            if kind == "tab": res = tab_run(b, base, a1, a2)
            elif kind == "menu": res = menu_test(b, base, a1)
            elif kind == "search": res = search_test(b, base, a2)
            elif kind == "modal": res = modal_test(b, base, a1, a2)
            elif kind == "lightbox": res = lightbox_test(b, base, a1, a2)
            elif kind == "form": res = form_test(b, base, a2)
    except Exception as e:
        res = {"page": a1, "vp": a2, "error": repr(e)[:600]}
    res["kind"] = kind; res["secs"] = round(time.time() - t0, 1)
    print("%-9s %-62s %-8s %5.1fs %s" % (kind, a1, a2, res["secs"], res.get("error", "")), flush=True)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--pages")
    ap.add_argument("--vp")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--out", default="results_keyboard.json")
    a = ap.parse_args()
    T = a.pages.split(",") if a.pages else lib.TEMPLATES["live"]
    vps = [a.vp] if a.vp else ["desktop", "mobile"]
    kinds = a.only.split(",") if a.only else ["tab", "menu", "search", "modal", "lightbox", "form"]
    t0 = time.time()
    with lib.server(PORT) as base:
        jobs = []
        if "tab" in kinds: jobs += [("tab", base, p, v) for v in vps for p in T]
        if "menu" in kinds: jobs += [("menu", base, p, "mobile") for p in T]
        if "search" in kinds: jobs += [("search", base, "index.html", v) for v in vps]
        if "modal" in kinds:
            mp_pages = [p for p in T if p in ("index.html", "library.html", "knowledge-base/flight-mechanics.html", "knowledge-base/navigators.html")] or T
            jobs += [("modal", base, p, v) for v in vps for p in mp_pages]
        if "lightbox" in kinds:
            lb_pages = [p for p in T if p.startswith("destinations/")] or T
            jobs += [("lightbox", base, p, v) for v in vps for p in lb_pages]
        if "form" in kinds: jobs += [("form", base, "enquire.html", v) for v in vps]
        with mp.Pool(a.workers) as pool:
            res = pool.map(job, jobs, chunksize=1)
    json.dump(res, open(os.path.join(HERE, a.out), "w"), indent=1, default=str)
    print("total %ds -> %s" % (time.time() - t0, os.path.join(HERE, a.out)))
