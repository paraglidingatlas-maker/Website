"""Headless integrity checks on the live pages (repo root).

    python3 browser_check.py pages   [--only PAGE ...]   all 180 pages: live DOM size, live duplicate ids, live
                                                       IDREF/SVG url(#) refs, JS-generated links + fragments,
                                                       own 4xx/5xx requests, own JS errors
    python3 browser_check.py cls     [--only PAGE ...]   CLS (layout-shift entries) on the 15 templates,
                                                       phone 390x844 + desktop 1280x800, throttled
    python3 browser_check.py imgshift [--only PAGE ...]  img box height while the image is still loading vs
                                                       after it loaded (layout-shift risk), per <img>
    python3 browser_check.py search                     homepage episode search: result links resolve?
    python3 browser_check.py smgraph                    sitemap.html graph: audio episodes under their series?
Port 8816 (override with --port N). External hosts are aborted (they are blocked here anyway); for
imgshift, i.ytimg.com thumbnails are fulfilled with a local 320x180 stand-in so they behave as in production.
"""
import collections
import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib  # noqa: E402
import static_check as sc  # noqa: E402

ARGS = sys.argv[1:]
MODE = ARGS[0] if ARGS else "pages"
PORT = int(ARGS[ARGS.index("--port") + 1]) if "--port" in ARGS else 8816
ONLY = ARGS[ARGS.index("--only") + 1:] if "--only" in ARGS else None
if ONLY:
    ONLY = [x for x in ONLY if not x.startswith("--")]

LIVE_JS = r"""() => {
  const all = document.getElementsByTagName('*');
  const ids = {};
  for (const el of document.querySelectorAll('[id]')) { ids[el.id] = (ids[el.id] || 0) + 1; }
  const dups = Object.entries(ids).filter(([k, v]) => v > 1).map(([k, v]) => {
    const els = [...document.querySelectorAll('[id]')].filter(e => e.id === k);
    return [k, v, els.slice(0, 3).map(e => e.tagName.toLowerCase() + (e.closest('svg') ? '(svg)' : '') +
      (e.closest('template') ? '(template)' : ''))];
  });
  const missingRefs = [];
  const refAttrs = ['aria-labelledby', 'aria-describedby', 'aria-controls', 'aria-owns', 'aria-activedescendant',
                    'aria-details', 'aria-errormessage'];
  for (const a of refAttrs) for (const el of document.querySelectorAll('[' + a + ']'))
    for (const r of (el.getAttribute(a) || '').split(/\s+/).filter(Boolean))
      if (!document.getElementById(r)) missingRefs.push([el.tagName.toLowerCase(), a, r]);
  for (const el of document.querySelectorAll('label[for]'))
    if (el.htmlFor && !document.getElementById(el.htmlFor)) missingRefs.push(['label', 'for', el.htmlFor]);
  const svgMissing = [];
  for (const a of ['fill', 'stroke', 'clip-path', 'mask', 'filter', 'marker-start', 'marker-mid', 'marker-end', 'style'])
    for (const el of document.querySelectorAll('[' + a + '*="url(#"]')) {
      const v = el.getAttribute(a);
      for (const m of v.matchAll(/url\(\s*['"]?#([^'")\s]+)/g))
        if (!document.getElementById(m[1])) svgMissing.push([el.tagName, a, m[1]]);
    }
  for (const el of document.querySelectorAll('use, textPath, mpath')) {
    const h = el.getAttribute('href') || el.getAttribute('xlink:href');
    if (h && h[0] === '#' && !document.getElementById(h.slice(1))) svgMissing.push([el.tagName, 'href', h.slice(1)]);
  }
  const links = [...new Set([...document.querySelectorAll('a[href], area[href]')].map(a => a.href))];
  const imgs = [...new Set([...document.querySelectorAll('img')].map(i => i.currentSrc || i.src).filter(Boolean))];
  return { n: all.length, dups, missingRefs, svgMissing, links, imgs, ids: Object.keys(ids) };
}"""


def ctx_with_routes(b, base, viewport=None, hold_images=False, fake_yt=None, held=None):
    ctx = b.new_context(viewport=viewport or {"width": 1280, "height": 800})

    def handler(route):
        req = route.request
        u = req.url
        if hold_images and req.resource_type == "image":
            held.append(route)          # never resolved: the image stays "loading"
            return
        if u.startswith(base):
            route.continue_()
        elif fake_yt is not None and "i.ytimg.com" in u:
            route.fulfill(status=200, content_type="image/jpeg", body=fake_yt)
        else:
            route.abort()
    ctx.route("**/*", handler)
    return ctx


def mode_pages():
    pages = ONLY or sc.PAGES
    res = {}
    t0 = time.time()
    with lib.server(PORT) as base:
        with lib.browser() as b:
            ctx = ctx_with_routes(b, base)
            for i, p in enumerate(pages):
                pg = ctx.new_page()
                bad_resp, page_err, cons = [], [], []
                pg.on("response", lambda r: bad_resp.append([r.status, r.url[len(base):]])
                      if r.url.startswith(base) and r.status >= 400 else None)
                pg.on("pageerror", lambda e: page_err.append(str(e)[:300]))
                pg.on("console", lambda m: cons.append([m.text[:300], (m.location or {}).get("url", "")])
                      if m.type == "error" else None)
                rec = dict(page=p)
                try:
                    pg.goto(base + p, wait_until="load", timeout=30000)
                    pg.wait_for_timeout(300)
                    pg.evaluate("() => window.scrollTo(0, document.documentElement.scrollHeight)")
                    pg.wait_for_timeout(400)
                    live = pg.evaluate(LIVE_JS)
                    rec.update(live)
                except Exception as e:
                    rec["error"] = str(e)[:300]
                rec["bad_responses"] = bad_resp
                rec["pageerrors"] = page_err
                own_cons = [c for c in cons if c[1].startswith(base) or (base in c[0])]
                rec["console_errors_own"] = own_cons
                rec["console_errors_external"] = len(cons) - len(own_cons)
                res[p] = rec
                pg.close()
                if i % 30 == 0:
                    print("  %d/%d %.0fs" % (i, len(pages), time.time() - t0), flush=True)
            ctx.close()
    # ---- analysis
    out = dict(pages=len(pages), seconds=round(time.time() - t0))
    out["dom_over_3000"] = sorted([[p, r["n"]] for p, r in res.items() if r.get("n", 0) > 3000], key=lambda x: -x[1])
    out["dom_top10"] = sorted([[p, r.get("n", 0)] for p, r in res.items()], key=lambda x: -x[1])[:10]
    out["live_duplicate_ids"] = {p: r["dups"] for p, r in res.items() if r.get("dups")}
    out["live_missing_idrefs"] = {p: r["missingRefs"] for p, r in res.items() if r.get("missingRefs")}
    out["live_missing_svg_refs"] = {p: r["svgMissing"] for p, r in res.items() if r.get("svgMissing")}
    out["own_bad_responses"] = {p: r["bad_responses"] for p, r in res.items() if r.get("bad_responses")}
    out["pageerrors"] = {p: r["pageerrors"] for p, r in res.items() if r.get("pageerrors")}
    out["console_errors_own"] = {p: r["console_errors_own"] for p, r in res.items() if r.get("console_errors_own")}
    out["console_errors_external_total"] = sum(r.get("console_errors_external", 0) for r in res.values())
    out["load_errors"] = {p: r["error"] for p, r in res.items() if r.get("error")}
    live_ids = {p: set(r.get("ids", [])) for p, r in res.items()}
    # links present in the live DOM, including those built by JS
    broken, badfrag, nonid = [], [], collections.Counter()
    static_links = {}
    for p in pages:
        d = sc.parse(p.split("#")[0])
        s = set()
        for tag, attr, val, line in d.refs:
            if tag in ("a", "area"):
                k, rel, frag, _ = sc.resolve(p, val)
                if k in ("internal", "self"):
                    s.add((rel, frag))
        static_links[p] = s
    js_only = 0
    for p, r in res.items():
        for href in r.get("links", []):
            if not href.startswith(base):
                continue
            path = href[len(base):]
            k, rel, frag, q = sc.resolve("x.html", "/" + path.split("#")[0].split("?")[0]
                                         + ("#" + href.split("#", 1)[1] if "#" in href else ""))
            ok, tgt, how = sc.target_file(rel)
            generated = (tgt, frag) not in static_links.get(p, set()) and (rel, frag) not in static_links.get(p, set())
            if generated:
                js_only += 1
            if not ok:
                broken.append(dict(page=p, href=href[len(base):], js_generated=generated))
                continue
            if frag and sc.is_html(tgt) and frag.lower() != "top":
                if frag in sc.parse(tgt).idset or frag in live_ids.get(tgt, set()):
                    continue
                if tgt == "library.html" and (frag.startswith("s=") or frag == "all"):
                    nonid["library.html#" + frag.split("=")[0]] += 1
                    continue
                if tgt == p.split("#")[0] and frag == "":
                    continue
                badfrag.append(dict(page=p, href=href[len(base):], target=tgt, fragment=frag,
                                    js_generated=generated))
    out["live_links_js_generated"] = js_only
    out["live_broken_links"] = broken
    out["live_bad_fragments"] = badfrag
    out["live_hash_routes_ok"] = nonid
    # images referenced at runtime that are missing (own)
    missing_imgs = []
    for p, r in res.items():
        for u in r.get("imgs", []):
            if u.startswith(base):
                k, rel, _, _ = sc.resolve("x.html", "/" + u[len(base):].split("?")[0])
                if not sc.target_file(rel)[0]:
                    missing_imgs.append([p, u[len(base):]])
    out["live_missing_images"] = missing_imgs
    fp = lib.save("integrity/browser_pages.json", out)
    lib.save("integrity/browser_pages_raw.json", {p: {k: v for k, v in r.items() if k not in ("ids",)}
                                                   for p, r in res.items()})
    for k, v in out.items():
        print("%-28s %s" % (k, json.dumps(v if not isinstance(v, (list, dict)) else len(v))))
    print("saved", fp)


CLS_INIT = r"""
window.__ls = [];
new PerformanceObserver(list => {
  for (const e of list.getEntries()) {
    window.__ls.push({ t: e.startTime, v: e.value, r: e.hadRecentInput,
      src: (e.sources || []).map(s => {
        const n = s.node; let d = '';
        if (n && n.nodeType === 1) {
          d = n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') +
              (n.className && typeof n.className === 'string' ? '.' + n.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
        } else if (n) { d = '#text:' + (n.textContent || '').trim().slice(0, 30); }
        return { node: d, prev: [s.previousRect.y, s.previousRect.height], cur: [s.currentRect.y, s.currentRect.height] };
      }) });
  }
}).observe({ type: 'layout-shift', buffered: true });
"""


def session_cls(entries):
    """Max session-window CLS (1s gap, 5s cap), excluding hadRecentInput."""
    best = cur = 0.0
    start = last = None
    for e in sorted(entries, key=lambda x: x["t"]):
        if e["r"]:
            continue
        if start is None or e["t"] - last > 1000 or e["t"] - start > 5000:
            start = e["t"]
            cur = 0.0
        cur += e["v"]
        last = e["t"]
        best = max(best, cur)
    return best


def mode_cls():
    pages = ONLY or lib.TEMPLATES["live"]
    profiles = [("phone-slow4g", {"width": 390, "height": 844}, True, dict(latency=150, downloadThroughput=200000,
                                                                          uploadThroughput=90000), 4),
                ("desktop-fast", {"width": 1280, "height": 800}, False, None, 1)]
    out = {}
    with lib.server(PORT) as base:
        with lib.browser() as b:
            for name, vp, mobile, net, cpu in profiles:
                for p in pages:
                    ctx = ctx_with_routes(b, base, viewport=vp)
                    ctx.add_init_script(CLS_INIT)
                    pg = ctx.new_page()
                    cdp = ctx.new_cdp_session(pg)
                    if net:
                        cdp.send("Network.enable")
                        cdp.send("Network.emulateNetworkConditions", dict(offline=False, **net))
                    if cpu > 1:
                        cdp.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
                    t0 = time.time()
                    try:
                        pg.goto(base + p, wait_until="load", timeout=60000)
                    except Exception as e:
                        out.setdefault(name, {})[p] = dict(error=str(e)[:200])
                        ctx.close()
                        continue
                    load_s = time.time() - t0
                    pg.wait_for_timeout(1500)
                    # scroll down the page like a reader, no input events (scrolling is not "recent input")
                    h = pg.evaluate("() => document.documentElement.scrollHeight")
                    y = 0
                    while y < h and y < 12000:
                        y += vp["height"] * 1.5
                        pg.evaluate("y => window.scrollTo(0, y)", y)
                        pg.wait_for_timeout(200)
                        h = pg.evaluate("() => document.documentElement.scrollHeight")
                    pg.wait_for_timeout(1000)
                    ent = pg.evaluate("() => window.__ls")
                    srcs = collections.Counter()
                    for e in ent:
                        if e["r"]:
                            continue
                        for s in e["src"][:3]:
                            srcs[s["node"]] += e["v"]
                    out.setdefault(name, {})[p] = dict(
                        load_s=round(load_s, 1), cls_session=round(session_cls(ent), 4),
                        cls_total=round(sum(e["v"] for e in ent if not e["r"]), 4), shifts=len(ent),
                        top_sources=[[k, round(v, 4)] for k, v in srcs.most_common(5)],
                        first_shifts=[dict(t=round(e["t"]), v=round(e["v"], 4), src=e["src"][:2]) for e in
                                      sorted(ent, key=lambda x: -x["v"])[:4]])
                    lib.save("integrity/browser_cls_partial.json", out)
                    print("%-13s %-55s CLS %.4f (sum %.4f, %d shifts, load %.1fs)" % (
                        name, p, out[name][p]["cls_session"], out[name][p]["cls_total"], len(ent), load_s), flush=True)
                    ctx.close()
    print("saved", lib.save("integrity/browser_cls.json", out))


IMG_JS = r"""() => [...document.querySelectorAll('img')].map((im, i) => {
  const r = im.getBoundingClientRect(); const cs = getComputedStyle(im);
  let anc = im.parentElement, oof = false;
  for (let k = 0; im && k < 4 && anc; k++, anc = anc.parentElement) {}
  return { i, src: (im.getAttribute('src') || '').slice(0, 90), w: Math.round(r.width), h: Math.round(r.height),
           complete: im.complete, nat: [im.naturalWidth, im.naturalHeight], pos: cs.position, disp: cs.display,
           ar: cs.aspectRatio, attrs: [im.getAttribute('width'), im.getAttribute('height')],
           cls: (im.className || '').toString().slice(0, 40) };
})"""


def fake_thumb():
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", (320, 180), (60, 70, 80)).save(buf, "JPEG")
    return buf.getvalue()


def mode_imgshift():
    pages = ONLY or sorted(set(json.load(open(os.path.join(HERE, "static_imgs.json")))["pages_affected"])
                           | set(lib.TEMPLATES["live"]))
    yt = fake_thumb()
    out = {}
    with lib.server(PORT) as base:
        with lib.browser() as b:
            for vpname, vp in (("phone", {"width": 390, "height": 844}), ("desktop", {"width": 1280, "height": 800})):
                for p in pages:
                    held = []
                    c1 = ctx_with_routes(b, base, viewport=vp, hold_images=True, held=held)
                    pg = c1.new_page()
                    pg.goto(base + p, wait_until="domcontentloaded", timeout=30000)
                    pg.wait_for_timeout(1200)
                    before = pg.evaluate(IMG_JS)
                    sh_before = pg.evaluate("() => document.documentElement.scrollHeight")
                    c1.close()
                    c2 = ctx_with_routes(b, base, viewport=vp, fake_yt=yt)
                    pg = c2.new_page()
                    pg.goto(base + p, wait_until="load", timeout=30000)
                    pg.evaluate("() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
                    try:
                        pg.wait_for_function("() => [...document.images].every(i => i.complete)", timeout=15000)
                    except Exception:
                        pass
                    pg.wait_for_timeout(500)
                    after = pg.evaluate(IMG_JS)
                    sh_after = pg.evaluate("() => document.documentElement.scrollHeight")
                    c2.close()
                    rows = []
                    for a, z in zip(before, after):
                        if a["src"] != z["src"]:
                            continue
                        if z["disp"] == "none" or (z["w"] == 0 and z["h"] == 0):
                            continue
                        dh = z["h"] - a["h"]
                        if abs(dh) > 1:
                            rows.append(dict(i=a["i"], src=a["src"], cls=a["cls"], h_loading=a["h"], h_loaded=z["h"],
                                             w=z["w"], pos=z["pos"], attrs=z["attrs"], ar_loading=a["ar"]))
                    in_flow = [r for r in rows if r["pos"] not in ("absolute", "fixed")]
                    out.setdefault(vpname, {})[p] = dict(imgs=len(after), changed=len(rows), changed_in_flow=len(in_flow),
                                                         page_height_loading=sh_before, page_height_loaded=sh_after,
                                                         rows=in_flow[:40])
                    print("%-8s %-55s imgs %3d  box-height changes %3d (in flow %3d)  page height %d -> %d" % (
                        vpname, p, len(after), len(rows), len(in_flow), sh_before, sh_after), flush=True)
    print("saved", lib.save("integrity/browser_imgshift.json", out))


def mode_search():
    out = []
    with lib.server(PORT) as base:
        with lib.browser() as b:
            ctx = ctx_with_routes(b, base)
            pg = ctx.new_page()
            pg.goto(base + "index.html", wait_until="load")
            for q in ("snippet", "anatomy", "parakites", "gin seok", "maxime pinot", "pre flight rituals",
                      "neuroscience", "stephan stiegler", "thermal", "highlights"):
                pg.fill("#epSearchInput", q)
                pg.wait_for_timeout(150)
                res = pg.evaluate("""() => [...document.querySelectorAll('#epSearchResults a')].map(a =>
                    ({text: a.textContent.slice(0, 70), href: a.getAttribute('href'), abs: a.href}))""")
                for r in res:
                    if r["abs"].startswith(base):
                        st = pg.request.get(r["abs"]).status
                    else:
                        st = "external"
                    out.append(dict(query=q, text=r["text"], href=r["href"], status=st))
                    print("%-20s %-4s %-60s %s" % (q, st, r["text"][:60], r["href"][:90]))
            ctx.close()
    bad = [r for r in out if r["status"] not in (200, "external")]
    ext = [r for r in out if r["status"] == "external"]
    print("results %d, broken %d, sent off-site %d" % (len(out), len(bad), len(ext)))
    lib.save("integrity/browser_search.json", dict(results=out, broken=bad, external=ext))


def mode_smgraph():
    """Expand every series node in the sitemap graph and list the episode nodes it shows."""
    out = {}
    with lib.server(PORT) as base:
        with lib.browser() as b:
            ctx = ctx_with_routes(b, base, viewport={"width": 1400, "height": 1000})
            pg = ctx.new_page()
            pg.goto(base + "sitemap.html", wait_until="load")
            data = pg.evaluate("() => window.SITEMAP_GRAPH")
            kids = collections.defaultdict(list)
            for l in data["links"]:
                kids[l["s"]].append(l["t"])
            byid = {}
            for n in data["nodes"]:
                byid[n["id"]] = n
            series = [n for n in data["nodes"] if n["kind"] == "series"]

            def click_label(label):
                loc = pg.locator('#sm-svg g.sm-node[aria-label^="%s"]' % label.replace('"', '\\"')).first
                if loc.count() == 0:
                    return False
                loc.dispatch_event("click")
                pg.wait_for_timeout(700)
                return True

            # path: home is shown; open Knowledge Base, then each category, then each series
            parents = collections.defaultdict(list)
            for l in data["links"]:
                parents[l["t"]].append(l["s"])
            for s in series:
                pg.goto(base + "sitemap.html", wait_until="load")
                chain = []
                cur = s["id"]
                while cur and cur != "home":
                    chain.append(cur)
                    cur = (parents.get(cur) or [None])[0]
                ok = True
                for nid in reversed(chain):
                    if not click_label(byid[nid]["label"]):
                        ok = False
                        break
                shown = pg.evaluate("""() => [...document.querySelectorAll('#sm-svg g.sm-episode')].map(g =>
                    g.getAttribute('aria-label'))""")
                expected = [n["label"] for n in data["nodes"] if n["kind"] == "episode" and
                            any(l["s"] == s["id"] and l["t"] == n["id"] for l in data["links"])]
                # expected by URL: the static list in sitemap.html under that series
                out[s["label"]] = dict(opened=ok, shown=shown, expected_links=len(kids[s["id"]]),
                                       expected_labels=expected)
                miss = [e for e in expected if not any((x or "").startswith(e) for x in shown)]
                print("%-28s opened=%s shown %2d / links %2d  missing %s" % (s["label"], ok, len(shown),
                                                                           len(kids[s["id"]]), miss[:3]))
            ctx.close()
    print("saved", lib.save("integrity/browser_smgraph.json", out))


MODAL_LINKS = r"""() => {
  const o = document.querySelector('.ep-modal-overlay');
  if (!o) return null;
  return { open: o.classList.contains('open') || getComputedStyle(o).display !== 'none' && getComputedStyle(o).visibility !== 'hidden',
           text: (o.innerText || '').slice(0, 80),
           links: [...o.querySelectorAll('a[href]')].map(a => [a.getAttribute('href'), a.href, a.className]) };
}"""


def mode_modals():
    """Open every episode popup (KB series pages, library #all, homepage cards) and check its links."""
    targets = ONLY or (["index.html", "library.html#all"] +
                       [p for p in sc.PAGES if p.startswith("knowledge-base/")])
    out = dict(opened=0, not_opened=[], links=0, broken=[], bad_fragment=[], per_page={})
    with lib.server(PORT) as base:
        with lib.browser() as b:
            ctx = ctx_with_routes(b, base)
            for p in targets:
                pg = ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
                pg.goto(base + p, wait_until="load")
                pg.wait_for_timeout(400)
                tiles = pg.locator("[data-ep-slug],[data-ep-index]")
                n = tiles.count()
                opened = 0
                for i in range(n):
                    t = tiles.nth(i)
                    label = (t.get_attribute("data-ep-slug") or t.get_attribute("data-ep-index"))
                    try:
                        # the homepage cards sit in a moving marquee, so a synthetic click on the tile
                        # (what the popup script listens for) rather than a pointer click
                        t.dispatch_event("click")
                    except Exception as e:
                        out["not_opened"].append([p, label, "click: " + str(e)[:80]])
                        continue
                    pg.wait_for_timeout(250)
                    m = pg.evaluate(MODAL_LINKS)
                    if not m or not m["links"]:
                        out["not_opened"].append([p, label, "no modal links"])
                    else:
                        opened += 1
                        for href, absu, cls in m["links"]:
                            if not absu.startswith(base):
                                continue
                            out["links"] += 1
                            path, _, frag = absu[len(base):].partition("#")
                            k, rel, _, _ = sc.resolve("x.html", "/" + path.split("?")[0])
                            ok, tgt, how = sc.target_file(rel)
                            if not ok:
                                out["broken"].append(dict(page=p, tile=label, href=href, cls=cls))
                            elif frag and sc.is_html(tgt) and frag not in sc.parse(tgt).idset and not (
                                    tgt == "library.html" and (frag.startswith("s=") or frag == "all")):
                                out["bad_fragment"].append(dict(page=p, tile=label, href=href, cls=cls))
                    pg.keyboard.press("Escape")
                    pg.wait_for_timeout(200)
                    if "#" in p and pg.url != base + p:
                        pg.goto(base + p, wait_until="load")
                        pg.wait_for_timeout(300)
                        tiles = pg.locator("[data-ep-slug],[data-ep-index]")
                out["opened"] += opened
                out["per_page"][p] = dict(tiles=n, opened=opened, pageerrors=errs)
                print("%-45s tiles %3d opened %3d errors %d" % (p, n, opened, len(errs)), flush=True)
                pg.close()
            ctx.close()
    # #pin=<slug> is a globe deep link: valid only when the slug has a pin
    import re as _re
    gsrc = open(os.path.join(lib.ROOT, "globe-episodes.js"), encoding="utf-8").read()
    globe = json.loads(_re.search(r"window.GLOBE_EP = (\{.*\});", gsrc, _re.S).group(1))
    pins = [x for x in out["bad_fragment"] if "#pin=" in x["href"]]
    out["pin_links_without_pin"] = [x for x in pins if x["href"].split("#pin=")[1] not in globe]
    out["bad_fragment"] = [x for x in out["bad_fragment"] if "#pin=" not in x["href"]]
    out["pin_links_ok"] = len(pins) - len(out["pin_links_without_pin"])
    print("globe pin links ok %d, pointing at an episode with no pin %d (%d distinct)" % (
        out["pin_links_ok"], len(out["pin_links_without_pin"]),
        len({x["href"].split("#pin=")[1] for x in out["pin_links_without_pin"]})))
    print("modal links checked %d, broken %d, bad fragment %d, not opened %d" % (
        out["links"], len(out["broken"]), len(out["bad_fragment"]), len(out["not_opened"])))
    print("saved", lib.save("integrity/browser_modals.json", out))


if __name__ == "__main__":
    dict(modals=mode_modals, pages=mode_pages, cls=mode_cls, imgshift=mode_imgshift, search=mode_search, smgraph=mode_smgraph)[MODE]()
