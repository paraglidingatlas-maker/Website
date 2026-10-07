#!/usr/bin/env python3
"""
The usability pass on v4 (owner's brief, 7 Oct 2026): every item measured the
same way before and after, in headless Chromium, so a change is judged by a
number and not by eye.

    python3 tools/ux_measure.py                    # every item, a table
    python3 tools/ux_measure.py 1 2 17             # only these items
    python3 tools/ux_measure.py --save before      # also write docs/ux-measure/before.json
    python3 tools/ux_measure.py --compare before   # the table with the saved numbers beside
    python3 tools/ux_measure.py --site v2 ...      # the same on another prototype

Sizes: phone 390 x 844 (touch, mobile), tablet 768 x 1024, desktop 1440 x 900;
item 1 also 320 to 414 px wide, item 23 also 1920 x 1080. Hosts other than the
preview server are blocked (YouTube and the feeds are blocked here anyway), so
a feed that never answers is the state measured. Needs the preview server
(python3 -m http.server 8765 --bind 127.0.0.1) and, for items 9 and 21,
axe-core (npm install axe-core in /tmp/claude-0/axe, or AXE=path/axe.min.js).

Each item prints its numbers and "done" when its own finish line in the brief
is met ("-" where only a look at the screenshots can tell).
"""
import gzip
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
AXE = os.environ.get("AXE", "/tmp/claude-0/axe/node_modules/axe-core/axe.min.js")
SITE = "v4"
OUTDIR = os.path.join(ROOT, "docs", "ux-measure")

PHONE = dict(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
TABLET = dict(viewport={"width": 768, "height": 1024}, has_touch=True, is_mobile=True, device_scale_factor=2)
DESK = dict(viewport={"width": 1440, "height": 900})
WIDE = dict(viewport={"width": 1920, "height": 1080})

TRIPS = {"india": "destinations/india.html", "kenya": "destinations/kenya.html"}
PRICE = {"india": "£1,100", "kenya": "US$2,100"}
EPISODE = "episodes/sky-gods-flying-8000ers-antoine-girard.html"
TEMPLATES = ["index.html", "podcast.html", "library.html", "about.html", "mission.html", "partners.html",
             "enquire.html", "sitemap.html", "tags.html", "tags/safety.html", "knowledge-base.html",
             "knowledge-base/flight-mechanics.html", EPISODE, "episodes/anatomy-of-a-dream-with-damien-lacaze.html",
             "destinations/india.html", "destinations/kenya.html", "terms.html", "privacy-policy.html",
             "404.html", "fly-options.html"]


def base():
    return "http://127.0.0.1:8765/prototypes/%s/" % SITE


class B:
    """One browser for the run; a fresh context per page."""

    def __init__(self, p):
        self.b = p.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else p.chromium.launch()

    def page(self, rel, opts=PHONE, wait=1200, block=True, until="load", extra=None):
        ctx = self.b.new_context(**dict(opts, **(extra or {})))
        pg = ctx.new_page()
        if block:
            pg.route(lambda u: "127.0.0.1" not in u, lambda r: r.abort())
        pg.goto(base() + rel, wait_until=until, timeout=60000)
        if wait:
            pg.wait_for_timeout(wait)
        pg._ctx = ctx
        return pg

    @staticmethod
    def done(pg):
        pg._ctx.close()

    def close(self):
        self.b.close()


def scroll_through(pg, step=700):
    """Walk the page once so scroll-driven reveals and lazy parts have run."""
    pg.evaluate("""async (step) => { const H = document.documentElement.scrollHeight;
      for (let y = 0; y < H; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
      scrollTo(0, 0); }""", step)
    pg.wait_for_timeout(500)


def axe(pg, rules):
    if not os.path.exists(AXE):
        return None
    pg.add_script_tag(path=AXE)
    return pg.evaluate("""async (rules) => { const r = await axe.run(document, {runOnly: {type: 'rule', values: rules},
      resultTypes: ['violations']}); return r.violations.map(v => ({id: v.id, n: v.nodes.length,
      targets: v.nodes.slice(0, 6).map(x => x.target.join(' '))})); }""", rules)


# --------------------------------------------------------------------------------------------- A. trips

def item1(b):
    """The phone action bar: price, length, next departure; readable 320 to 414 px, at most 80 px tall."""
    out, ok = {}, True
    for trip, rel in TRIPS.items():
        for w in (320, 360, 375, 390, 414):
            pg = b.page(rel, dict(PHONE, viewport={"width": w, "height": 844}), wait=600)
            pg.evaluate("scrollTo(0, innerHeight * 3)")
            pg.wait_for_timeout(700)
            r = pg.evaluate("""(price) => { const bar = document.getElementById('dstMobar'); if (!bar) return null;
              const r = bar.getBoundingClientRect(), cs = getComputedStyle(bar);
              let small = 99, clipped = 0;
              bar.querySelectorAll('*').forEach(e => { if (!e.childNodes.length) return;
                const t = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
                if (t && e.getClientRects().length) { small = Math.min(small, parseFloat(getComputedStyle(e).fontSize));
                  if (e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow !== 'visible') clipped++; } });
              const over = bar.scrollWidth > bar.clientWidth + 1 || r.right > innerWidth + 1;
              return {h: Math.round(r.height), shown: cs.display !== 'none' && r.top < innerHeight && r.bottom > 0,
                text: bar.innerText.replace(/\\s+/g, ' ').trim(), price: bar.innerText.includes(price),
                small: small, clipped: clipped, over: over}; }""", PRICE[trip])
            B.done(pg)
            out["%s@%d" % (trip, w)] = r
            ok &= bool(r and r["price"] and r["h"] <= 80 and not r["over"] and not r["clipped"] and r["small"] >= 12)
    s = out["india@390"]
    return dict(summary="India 390: \"%s\" %dpx; Kenya 390: \"%s\"" % (s["text"], s["h"], out["kenya@390"]["text"]),
                data=out, done=ok)


SECTIONS_JS = """() => { const vh = innerHeight, H = document.documentElement.scrollHeight, o = {screens: +(H / vh).toFixed(1)};
  for (const id of ['overview', 'route', 'gallery', 'dates']) { const e = document.getElementById(id);
    if (!e) continue; const r = e.getBoundingClientRect();
    o[id] = [+((r.top + scrollY) / vh).toFixed(1), +(r.height / vh).toFixed(1)]; }
  return o; }"""


def item2(b):
    """Dates sooner on a phone: Dates start by screen 12; the gallery's pinned run at most 3 screens."""
    out, ok = {}, True
    for trip, rel in TRIPS.items():
        pg = b.page(rel, PHONE)
        r = pg.evaluate(SECTIONS_JS)
        B.done(pg)
        out[trip] = r
        ok &= r["dates"][0] <= 12 and r["gallery"][1] <= 3
    f = lambda t: "%s dates at %.1f of %.0f (fly-through %.1f, route %.1f, gallery %.1f)" % (
        t, out[t]["dates"][0], out[t]["screens"], out[t]["overview"][1], out[t]["route"][1], out[t]["gallery"][1])
    return dict(summary="%s; %s" % (f("india"), f("kenya")), data=out, done=ok)


def item3(b):
    """Gallery framing on a 390 x 844 phone at 3x: how much of each photograph shows, and how far it is enlarged."""
    out, worst = {}, 1.0
    for trip, rel in TRIPS.items():
        pg = b.page(rel, dict(PHONE, device_scale_factor=3))
        pg.evaluate("document.getElementById('gallery').scrollIntoView()")
        pg.wait_for_timeout(600)
        r = pg.evaluate("""() => [...document.querySelectorAll('#gallery figure img')].map(im => {
            const r = im.getBoundingClientRect(), cs = getComputedStyle(im);
            const nw = +im.getAttribute('width') || im.naturalWidth, nh = +im.getAttribute('height') || im.naturalHeight;
            const fit = cs.objectFit, s = fit === 'cover' ? Math.max(r.width / nw, r.height / nh) : Math.min(r.width / nw, r.height / nh);
            const shown = fit === 'cover' ? Math.min(1, (r.width * r.height) / (nw * nh * s * s)) : 1;
            return {alt: im.alt.slice(0, 60), box: [Math.round(r.width), Math.round(r.height)], img: [nw, nh], fit: fit,
                    pos: cs.objectPosition, shown: +shown.toFixed(2), x3: +(s * 3).toFixed(2)}; })""")
        B.done(pg)
        out[trip] = r
        worst = min([worst] + [x["shown"] for x in r])
    allp = [x for t in out.values() for x in t]
    mean = sum(x["shown"] for x in allp) / max(1, len(allp))
    mx = max(x["x3"] for x in allp)
    focal = sum(1 for x in allp if x["pos"] not in ("50% 50%", "60% 50%"))
    return dict(summary="%d photos: %.0f%% of each shows on average (least %.0f%%), enlarged up to %.1fx on a 3x phone; %d with a focal point"
                % (len(allp), 100 * mean, 100 * worst, mx, focal),
                data=out, done=True if worst >= .99 else None)


def item4(b):
    """'Hold a place' in context: the enquiry opens on the trip, dates and price, the form starts on screen one."""
    url = "enquire.html?trip=india&when=21+to+30+October+2026"
    pg = b.page(url, PHONE)
    r = pg.evaluate("""() => { const vh = innerHeight, h1 = document.querySelector('h1');
      const f = [...document.querySelectorAll('#enqForm input:not([type=hidden]):not([tabindex="-1"]), #enqForm select, #enqForm textarea')]
        .find(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden');
      const first = document.body.innerText.slice(0, 4000);
      const scr = [...document.querySelectorAll('h1, h2, p, b, span, time, strong, li, dd, dt')].filter(e => { const r = e.getBoundingClientRect();
        return r.height && r.top < vh && r.bottom > 0; }).map(e => e.textContent).join(' ');
      const cta = document.querySelector('.page-wrap > nav .nav-cta');
      const msg = document.getElementById('message');
      return {h1: h1 && h1.textContent.replace(/\\s+/g, ' ').trim(), field: f ? Math.round(f.getBoundingClientRect().top + scrollY) : null,
        fieldId: f && f.id, dates: scr.includes('21 to 30 October 2026'), price: scr.includes('£1,100'), trip: /India|Bir/.test(scr),
        msgRequired: !!(msg && msg.required), headerEnquire: !!(cta && cta.getClientRects().length && getComputedStyle(cta).visibility !== 'hidden')}; }""")
    B.done(pg)
    ok = r["field"] is not None and r["field"] < 844 and r["dates"] and r["price"] and r["trip"] and not r["msgRequired"] and not r["headerEnquire"]
    return dict(summary="h1 \"%s\"; first field at y=%s; screen one shows trip %s, dates %s, price %s; message required %s; header Enquire %s"
                % (r["h1"], r["field"], r["trip"], r["dates"], r["price"], r["msgRequired"], r["headerEnquire"]), data=r, done=ok)


FOLD_JS = """() => { const vis = e => { for (let p = e.parentElement; p; p = p.parentElement) {
      if (p.tagName === 'DETAILS' && !p.open && !p.querySelector(':scope > summary').contains(e)) return false; }
      return !!e.getClientRects().length; };
  const qs = [...document.querySelectorAll('#faq .kfaq-item')];
  const g = document.getElementById('ground'), ps = g ? [...g.querySelectorAll('p')] : [];
  const shown = ps.filter(vis).map(p => p.textContent.trim()).join(' ');
  const outer = g && g.querySelector(':scope > details');
  const sec = [...document.querySelectorAll('body section[id]')].map(s => s.id);
  return {faq: qs.length, faqShown: qs.filter(vis).length, etqChars: shown.length, etqFolded: !!(outer && !outer.open),
          etqAfter: sec[sec.indexOf('ground') - 1] || null}; }"""


def item5(b):
    """Nothing important folded away: every trip question shown; Flying Etiquette its own band, first lines visible."""
    out, ok = {}, True
    for trip, rel in TRIPS.items():
        pg = b.page(rel, PHONE, wait=600)
        r = pg.evaluate(FOLD_JS)
        B.done(pg)
        out[trip] = r
        ok &= r["faqShown"] == r["faq"] and r["etqChars"] > 120 and not r["etqFolded"]
    f = lambda t: "%s %d of %d questions shown, etiquette %s with %d characters showing" % (
        t, out[t]["faqShown"], out[t]["faq"], "folded" if out[t]["etqFolded"] else "a band", out[t]["etqChars"])
    return dict(summary="%s; %s" % (f("india"), f("kenya")), data=out, done=ok)


def weigh(b, rel):
    sizes = {}

    def on(resp):
        if "127.0.0.1:8765" not in resp.url:
            return
        try:
            body = resp.body()
        except Exception:      # noqa: BLE001 - redirects, aborted media
            return
        text = re.search(r"\.(html?|css|js|json|svg|txt|webmanifest)(\?|$)", resp.url) or resp.url.endswith("/")
        sizes[resp.url] = (len(body), len(gzip.compress(body, 6)) if text else len(body))
    ctx = b.b.new_context(**dict(PHONE, device_scale_factor=3))
    pg = ctx.new_page()
    pg.route(lambda u: "127.0.0.1" not in u, lambda r: r.abort())
    pg.on("response", on)
    pg.goto(base() + rel, wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(2500)
    ctx.close()
    return sum(v[0] for v in sizes.values()), sum(v[1] for v in sizes.values()), sizes


WEIGHT_PAGES = ["index.html", "destinations/india.html", "destinations/kenya.html", "podcast.html", "library.html",
                "about.html", "knowledge-base.html", "knowledge-base/flight-mechanics.html", EPISODE, "enquire.html"]


def item6(b, before=None):
    """Weight on a phone: own-host bytes on arrival (3x phone, network settled, nothing scrolled), the lightest of two loads.
    raw = as the preview server sends it (the brief's figures: India 4.1, home 2.6, Kenya 1.6 MB); served = text
    gzipped as GitHub Pages sends it. MB = 1,000,000 bytes."""
    out = {}
    for rel in WEIGHT_PAGES:
        best = None
        for _ in range(2):
            raw, srv, sizes = weigh(b, rel)
            if best is None or srv < best[1]:
                best = (raw, srv, sizes)
        top = sorted(best[2].items(), key=lambda kv: -kv[1][1])[:5]
        out[rel] = {"raw": best[0], "served": best[1], "top": [(u.split("8765")[1][:90], v[1]) for u, v in top]}
    mb = lambda r, k="raw": out[r][k] / 1e6
    ok = mb("index.html") < 1.8 and mb("destinations/india.html") < 1.8
    if before:
        ok &= all(out[r][k] <= before["data"][r][k] * 1.005 for r in out if r in before["data"] for k in ("raw", "served"))
    return dict(summary="India %.2f MB, home %.2f MB, Kenya %.2f MB (gzipped as served: %.2f / %.2f / %.2f MB)" % (
        mb("destinations/india.html"), mb("index.html"), mb("destinations/kenya.html"),
        mb("destinations/india.html", "served"), mb("index.html", "served"), mb("destinations/kenya.html", "served")),
        data=out, done=ok)


def item7(b):
    """Desktop: the trip sub-navigation carries the from price and Hold a place, and stays in view."""
    out, ok = {}, True
    for trip, rel in TRIPS.items():
        pg = b.page(rel, DESK, wait=600)
        pg.evaluate("scrollTo(0, document.getElementById('route').getBoundingClientRect().top + scrollY + 200)")
        pg.wait_for_timeout(600)
        r = pg.evaluate("""(price) => { const j = document.querySelector('.dst-jump'); if (!j) return null;
          const r = j.getBoundingClientRect(), t = j.innerText.replace(/\\s+/g, ' ').trim();
          const hold = [...j.querySelectorAll('a')].find(a => /Hold a place/.test(a.textContent));
          return {text: t, price: t.includes(price), hold: !!hold, inView: r.top >= -1 && r.bottom <= innerHeight && r.height > 0}; }""", PRICE[trip])
        B.done(pg)
        out[trip] = r
        ok &= bool(r and r["price"] and r["hold"] and r["inView"])
    return dict(summary="India: \"%s\"" % out["india"]["text"], data=out, done=ok)


# --------------------------------------------------------------------------------------------- B. episodes

def item8(b):
    """The transcript on a phone: column width and characters a line."""
    pg = b.page(EPISODE, PHONE, wait=800)
    r = pg.evaluate("""() => { const ps = [...document.querySelectorAll('#transcript-body .cd-line p')].slice(0, 40);
      const cpl = ps.map(p => { const lh = parseFloat(getComputedStyle(p).lineHeight) || 1.6 * parseFloat(getComputedStyle(p).fontSize);
        const lines = Math.max(1, Math.round(p.getBoundingClientRect().height / lh)); return p.textContent.length / lines; })
        .filter((x, i) => ps[i].getBoundingClientRect().height > 60);
      const w = ps.length ? ps[0].getBoundingClientRect().width : 0;
      const ts = document.querySelector('#transcript-body .cd-ts'), p0 = ps[0];
      const above = ts && p0 ? ts.getBoundingClientRect().bottom <= p0.getBoundingClientRect().top + 2 : false;
      cpl.sort((a, b) => a - b);
      return {width: Math.round(w), cpl: cpl.length ? Math.round(cpl[Math.floor(cpl.length / 2)]) : 0,
              font: ps.length ? parseFloat(getComputedStyle(ps[0]).fontSize) : 0, tsAbove: above}; }""")
    B.done(pg)
    return dict(summary="paragraph %dpx wide, %d characters a line (median), %.1fpx type, timestamp above %s"
                % (r["width"], r["cpl"], r["font"], r["tsAbove"]), data=r, done=r["cpl"] >= 40)


def item9(b):
    """Chapters on a phone: a vertical list, and no chapter target that fails axe target-size."""
    pg = b.page(EPISODE, PHONE, wait=900)
    scroll_through(pg)
    r = pg.evaluate("""() => { const ch = [...document.querySelectorAll('.cd-chap')].filter(e => e.getClientRects().length);
      const rs = ch.map(e => e.getBoundingClientRect());
      const vertical = rs.length > 1 && rs.every((r, i) => !i || r.top >= rs[i - 1].bottom - 1);
      const ticks = [...document.querySelectorAll('.ep2-tick')].filter(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden')
        .map(e => e.getBoundingClientRect());
      return {cards: ch.length, w: rs.length ? Math.round(rs[0].width) : 0, h: rs.length ? Math.round(rs[0].height) : 0, vertical: vertical,
              ticks: ticks.length, tickMin: ticks.length ? +Math.min(...ticks.map(r => Math.min(r.width, r.height))).toFixed(1) : null}; }""")
    v = axe(pg, ["target-size"])
    B.done(pg)
    r["axe"] = v
    n = sum(x["n"] for x in v) if v is not None else None
    # the narrowest tick on any touch screen, over a few episodes (a short chapter makes a thin tick)
    thin, axe_more = [], 0
    for rel in ("episodes/navigating-india-eddie-colfox.html", "episodes/anatomy-of-a-dream-with-damien-lacaze.html",
                "episodes/tom-lolies-explains-the-science-of-wing-design-and.html"):
        for opts in (PHONE, TABLET):
            pg = b.page(rel, opts, wait=700)
            t = pg.evaluate("""() => [...document.querySelectorAll('.ep2-tick, .cd-chapter-mark, [class*="chap"][class*="mark"]')]
                .filter(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden').map(e => { const r = e.getBoundingClientRect(); return Math.min(r.width, r.height); })""")
            vv = axe(pg, ["target-size"])
            B.done(pg)
            if t:
                thin.append(min(t))
            axe_more += sum(x["n"] for x in vv) if vv else 0
    r["thinTouch"] = round(min(thin), 1) if thin else None
    r["axeMore"] = axe_more
    return dict(summary="%d chapters, %dx%d px, %s; ticks: narrowest %s px here, %s px on any touch screen; axe target-size: %s here, %d on three more"
                % (r["cards"], r["w"], r["h"], "a vertical list" if r["vertical"] else "a sideways row", r["tickMin"], r["thinTouch"],
                   "pass" if n == 0 else "%s nodes fail" % n, axe_more), data=r, done=r["vertical"] and n == 0 and axe_more == 0)


def labels():
    """Related Episodes links and Up next cards on every v4 episode page (static)."""
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    series = {m["series"].strip().lower() for m in meta if m.get("series")}
    import html as H
    d = os.path.join(ROOT, "prototypes", SITE, "episodes")
    plain = lambda s: H.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    bad_series, bad_repeat, n_labels, pages, examples = 0, 0, 0, 0, []
    for f in sorted(os.listdir(d)):
        src = open(os.path.join(d, f), encoding="utf-8").read()
        if 'http-equiv="refresh"' in src[:4000]:
            continue
        pages += 1
        m = re.search(r"<h2>Related Episodes</h2>(.*?)</div>", src, re.S)
        rel = [plain(x) for x in re.findall(r'<a class="cd-link"[^>]*>(.*?)</a>', m.group(1), re.S)] if m else []
        cards = re.findall(r'<span class="ep2-card-t">(.*?)</span><span class="ep2-card-m">(.*?)</span>', src, re.S)
        ups = [plain(t) for t, _ in cards]
        for blk in (rel, ups):
            n_labels += len(blk)
            for x in blk:
                if x.lower() in series:
                    bad_series += 1
                    examples.append((f[:40], x))
            if len(set(x.lower() for x in blk)) < len(blk):
                bad_repeat += 1
                examples.append((f[:40], "repeat: " + " | ".join(blk)))
        for t, mm in cards:      # the guest twice in one card
            g = plain(mm).split("·")[0].strip()
            if plain(t).lower() == g.lower():
                bad_repeat += 1
                examples.append((f[:40], "card twice: " + plain(t)))
    return dict(pages=pages, labels=n_labels, series=bad_series, repeats=bad_repeat, examples=examples[:12])


def item10(b):
    """Titles that say something: no Related Episodes or Up next label equals a series name or repeats in its block."""
    r = labels()
    return dict(summary="%d episode pages, %d labels: %d equal a series name, %d repeats in a block (e.g. %s)"
                % (r["pages"], r["labels"], r["series"], r["repeats"], "; ".join("%s" % x[1] for x in r["examples"][:3]) or "none"),
                data=r, done=r["series"] == 0 and r["repeats"] == 0)


CLS_INIT = """window.__cls = 0; window.__shifts = [];
new PerformanceObserver(l => { for (const e of l.getEntries()) { if (!e.hadRecentInput) { window.__cls += e.value;
  window.__shifts.push([Math.round(e.startTime), +e.value.toFixed(3), (e.sources || []).map(s => (s.node && (s.node.id || s.node.className || s.node.nodeName) || '').toString().slice(0, 40)).join(',')]); } } })
  .observe({type: 'layout-shift', buffered: true});
document.addEventListener('DOMContentLoaded', () => { const h = document.querySelector('h1'); window.__h1 = h ? h.getBoundingClientRect().top : null; });"""


def cls(b, rel, opts=DESK):
    ctx = b.b.new_context(**opts)
    pg = ctx.new_page()
    pg.route(lambda u: "127.0.0.1" not in u, lambda r: r.abort())
    pg.add_init_script(CLS_INIT)
    pg.goto(base() + rel, wait_until="load", timeout=60000)
    pg.wait_for_timeout(4000)
    r = pg.evaluate("""() => { const h = document.querySelector('h1');
      return {cls: +window.__cls.toFixed(3), moved: h && window.__h1 !== null ? Math.round(h.getBoundingClientRect().top - window.__h1) : null,
              shifts: window.__shifts.slice(0, 8)}; }""")
    ctx.close()
    return r


def item11(b):
    """Layout jumps at 1440: cumulative layout shift on load (4 s) and how far the hero's title moves."""
    out = {}
    for rel in ("podcast.html", EPISODE, "episodes/navigating-india-eddie-colfox.html", "index.html"):
        best = None
        for _ in range(2):
            r = cls(b, rel)
            if best is None or r["cls"] > best["cls"]:
                best = r
        out[rel] = best
    worst = max(v["cls"] for v in out.values())
    return dict(summary="CLS podcast %.2f, episode %.2f (title moves %s px), India episode %.2f, home %.2f"
                % (out["podcast.html"]["cls"], out[EPISODE]["cls"], out[EPISODE]["moved"],
                   out["episodes/navigating-india-eddie-colfox.html"]["cls"], out["index.html"]["cls"]), data=out, done=worst < .05)


def item12(b):
    """aria-controls on load points only at ids that exist."""
    bad = {}
    for rel in ("index.html", EPISODE, "destinations/india.html", "knowledge-base.html", "library.html"):
        for opts in (PHONE, DESK):
            pg = b.page(rel, opts, wait=1000)
            r = pg.evaluate("""() => [...document.querySelectorAll('[aria-controls]')].flatMap(e => e.getAttribute('aria-controls').split(/\\s+/)
                 .filter(id => id && !document.getElementById(id)).map(id => (e.className || e.tagName).toString().slice(0, 30) + ' -> ' + id))""")
            B.done(pg)
            for x in r:
                bad[x] = bad.get(x, 0) + 1
    return dict(summary="%d dangling: %s" % (len(bad), ", ".join(sorted(bad)) or "none"), data=bad, done=not bad)


# --------------------------------------------------------------------------------------------- C. knowledge base

FIRST_IDEA = """() => { const vh = innerHeight;
  const s = [...document.querySelectorAll('section.k-sec')].find(x => x.id !== 'episodes' && !x.classList.contains('k-next') && x.querySelector('h2'));
  const h = s && s.querySelector('h2'); const e = document.getElementById('episodes');
  return {idea: h ? +((h.getBoundingClientRect().top + scrollY) / vh).toFixed(2) : null, title: h && h.textContent.trim().slice(0, 50),
          tiles: e ? +(e.getBoundingClientRect().height / vh).toFixed(2) : null,
          screens: +(document.documentElement.scrollHeight / vh).toFixed(1)}; }"""


def item13(b):
    """Ideas first: on a phone the first idea within 1.5 screens."""
    out = {}
    for rel in ("knowledge-base/flight-mechanics.html", "knowledge-base/risk-vs-reward.html", "knowledge-base/sky-gods.html"):
        pg = b.page(rel, PHONE, wait=900)
        out[rel] = pg.evaluate(FIRST_IDEA)
        B.done(pg)
    worst = max(v["idea"] for v in out.values())
    return dict(summary="first idea at screen %.1f (Flight Mechanics), %.1f (Risk vs Reward), %.1f (Sky Gods); tiles take %.1f / %.1f screens"
                % (out["knowledge-base/flight-mechanics.html"]["idea"], out["knowledge-base/risk-vs-reward.html"]["idea"],
                   out["knowledge-base/sky-gods.html"]["idea"], out["knowledge-base/flight-mechanics.html"]["tiles"],
                   out["knowledge-base/risk-vs-reward.html"]["tiles"]), data=out, done=worst <= 1.5)


def kb_pages():
    d = os.path.join(ROOT, "prototypes", SITE, "knowledge-base")
    return ["knowledge-base/" + f for f in sorted(os.listdir(d)) if f.endswith(".html")]


def item14(b):
    """Series pages: how many phone screens, and whether a jump row leads into them."""
    out = {}
    for rel in kb_pages():
        pg = b.page(rel, PHONE, wait=300)
        out[rel] = pg.evaluate("""() => ({screens: +(document.documentElement.scrollHeight / innerHeight).toFixed(1),
          jump: !!document.querySelector('.dst-jump, .v4-jump'), links: document.querySelectorAll('.dst-jump a, .v4-jump a').length})""")
        B.done(pg)
    sc = [v["screens"] for v in out.values()]
    j = sum(1 for v in out.values() if v["jump"])
    return dict(summary="%d pages, %.0f to %.0f phone screens; %d with a jump row" % (len(out), min(sc), max(sc), j),
                data=out, done=j == len(out))


SMALL_JS = """() => { let all = 0, small = 0, min = 99; const sizes = {};
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = w.nextNode());) { const t = n.textContent.replace(/\\s+/g, ''); if (!t) continue;
    const e = n.parentElement; if (!e || e.closest('svg, script, style, noscript, template, [aria-hidden="true"] svg')) continue;
    if (!e.getClientRects().length) continue; const cs = getComputedStyle(e);
    if (cs.visibility === 'hidden' || +cs.opacity === 0 && !e.closest('[class*="reveal"], .kr, .v2-surface')) continue;
    let hid = false; for (let p = e; p; p = p.parentElement) { if (p.tagName === 'DETAILS' && !p.open && !p.querySelector(':scope > summary').contains(e)) { hid = true; break; } }
    if (hid) continue;
    const fs = parseFloat(cs.fontSize); all += t.length;
    if (fs < 11.95) { small += t.length; min = Math.min(min, fs); const k = (e.className || e.tagName).toString().slice(0, 28) + ' ' + fs.toFixed(1);
      sizes[k] = (sizes[k] || 0) + t.length; } }
  return {pct: all ? +(100 * small / all).toFixed(1) : 0, chars: small, min: min === 99 ? null : +min.toFixed(1),
          top: Object.entries(sizes).sort((a, b) => b[1] - a[1]).slice(0, 6)}; }"""


def item15(b):
    """The knowledge base hub on a phone: small type, the altitude links, a question under each series, search at the top."""
    pg = b.page("knowledge-base.html", PHONE, wait=900)
    small = pg.evaluate(SMALL_JS)
    r = pg.evaluate("""() => { const lv = [...document.querySelectorAll('.v4-climb-lv')].filter(e => e.getClientRects().length).map(e => Math.round(e.getBoundingClientRect().height));
      const topics = [...document.querySelectorAll('.clb-topic')];
      const q = topics.filter(t => { const x = t.querySelector('.v4-q') || (t.nextElementSibling && t.nextElementSibling.classList.contains('v4-q') ? t.nextElementSibling : null); return x && /\\?/.test(x.textContent); }).length;
      const s = [...document.querySelectorAll('input[type=search]')].find(i => i.getClientRects().length);
      return {levels: lv, series: topics.length, questions: q, search: s ? +((s.getBoundingClientRect().top + scrollY) / innerHeight).toFixed(2) : null}; }""")
    B.done(pg)
    r["small"] = small
    ok = small["pct"] == 0 and r["levels"] and min(r["levels"]) >= 44 and r["questions"] == r["series"] and r["search"] is not None and r["search"] < 1
    return dict(summary="%.0f%% of characters under 12px (smallest %s); altitude links %s px tall; %d of %d series with their question; search at %s"
                % (small["pct"], small["min"], r["levels"][:5], r["questions"], r["series"], r["search"]), data=r, done=ok)


MEASURE_JS = """(sel) => { const ps = [...document.querySelectorAll(sel)].filter(p => p.getClientRects().length && p.textContent.trim().length > 140);
  let max = 0, at = ''; const sizes = {};
  for (const p of ps) { const cs = getComputedStyle(p), lh = parseFloat(cs.lineHeight) || 1.6 * parseFloat(cs.fontSize);
    const lines = Math.max(1, Math.round(p.getBoundingClientRect().height / lh)); if (lines < 2) continue;
    const c = p.textContent.replace(/\\s+/g, ' ').trim().length / lines; if (c > max) { max = c; at = p.textContent.trim().slice(0, 40); }
    const fs = parseFloat(cs.fontSize); if (fs >= 14 && fs <= 18.5) { const k = fs.toFixed(1); sizes[k] = (sizes[k] || 0) + 1; } }
  return {max: Math.round(max), at: at, sizes: sizes, n: ps.length}; }"""


def item16(b):
    """Reading measure at 1440: characters a line (a paragraph's length over its lines, folds open) in the knowledge
    base and on the trips, and the sizes running text uses (paragraphs of 140+ characters set at 14 to 18.5 px)."""
    out = {}
    for rel in ("knowledge-base/flight-mechanics.html", "knowledge-base/risk-vs-reward.html", "destinations/kenya.html", "destinations/india.html"):
        pg = b.page(rel, DESK, wait=900)
        pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        scroll_through(pg, 900)
        pg.wait_for_timeout(400)
        out[rel] = pg.evaluate(MEASURE_JS, "main p, .page-wrap p, section p, article p, details p")
        B.done(pg)
    sizes = sorted({float(k) for v in out.values() for k in v["sizes"]})
    mx = max(v["max"] for v in out.values())
    kb = max(out[r]["max"] for r in out if r.startswith("knowledge"))
    return dict(summary="longest lines: knowledge base %d characters, Kenya %d, India %d; %d body sizes (%s px)"
                % (kb, out["destinations/kenya.html"]["max"], out["destinations/india.html"]["max"], len(sizes),
                   ", ".join("%.1f" % s for s in sizes)), data=out, done=mx <= 80 and len(sizes) <= 2)


# --------------------------------------------------------------------------------------------- D. finding

def item17(b):
    """The library on a phone: where the search sits, and what collapse, reserve and thermal find."""
    pg = b.page("library.html", PHONE, wait=1000)
    pos = pg.evaluate("() => { const q = document.getElementById('q'); return q ? +((q.getBoundingClientRect().top + scrollY) / innerHeight).toFixed(2) : null; }")
    res = {}
    for w in ("collapse", "reserve", "thermal", "zzqx"):
        pg.fill("#q", "")
        pg.fill("#q", w)
        pg.wait_for_timeout(500)
        res[w] = pg.evaluate("""() => { const rows = [...document.querySelectorAll('.ep-card, .ep-log-row, [data-lib-card]')].filter(e => e.getClientRects().length);
          const none = [...document.querySelectorAll('.v2-empty, .lib-empty, [data-empty], .v4-empty')].find(e => e.getClientRects().length);
          const status = document.querySelector('.v2-find-count, [aria-live]');
          return {shown: rows.length, none: none ? none.innerText.replace(/\\s+/g, ' ').trim().slice(0, 120) : null,
                  topics: none ? none.querySelectorAll('a[href*="tags"]').length : 0, status: status ? status.textContent.trim().slice(0, 60) : null}; }""")
    B.done(pg)
    ok = pos is not None and pos <= 1 and all(res[w]["shown"] > 0 for w in ("collapse", "reserve", "thermal")) and res["zzqx"]["topics"] > 0
    return dict(summary="search at screen %s; collapse %d, reserve %d, thermal %d results; empty state offers %d topics"
                % (pos, res["collapse"]["shown"], res["reserve"]["shown"], res["thermal"]["shown"], res["zzqx"]["topics"]),
                data=dict(pos=pos, res=res), done=ok)


def site_search(pg, q):
    pg.evaluate("q => { const i = document.getElementById('v4q'); i.value = q; i.dispatchEvent(new Event('input', {bubbles: true})); }", q)
    pg.wait_for_timeout(700)
    return pg.evaluate("""() => [...document.querySelectorAll('#v4hits li')].map(li => { const a = li.querySelector('a');
        return {u: a ? a.getAttribute('href').replace(/^.*prototypes\\/v\\d+\\//, '') : null, text: li.innerText.replace(/\\s+/g, ' ').trim().slice(0, 140),
                line: !!li.querySelector('.v4-hit-s'), links: li.querySelectorAll('a').length}; })""")


def item18(b):
    """The site search: the Kenya trip for "how much does kenya cost", a matching line under each result, a helpful empty state."""
    pg = b.page("index.html", DESK, wait=800)
    pg.evaluate("() => document.querySelector('.v4-open').click()")
    pg.wait_for_function("() => document.getElementById('v4q')", timeout=15000)
    site_search(pg, "kenya")
    pg.wait_for_timeout(1200)
    out = {}
    for q in ("how much does kenya cost", "india price", "reserve", "qqzzx"):
        out[q] = site_search(pg, q)
    B.done(pg)
    hits = out["how much does kenya cost"]
    rank = next((i + 1 for i, h in enumerate(hits) if h["u"] and h["u"].endswith("destinations/kenya.html")), None)
    lines = sum(1 for h in hits if h["line"])
    none = out["qqzzx"][0] if out["qqzzx"] else {"links": 0, "text": ""}
    ok = rank == 1 and hits and lines == len(hits) and none["links"] >= 3
    return dict(summary="Kenya trip ranked %s for \"how much does kenya cost\"; %d of %d results show a matching line; empty state: \"%s\" (%d links)"
                % (rank, lines, len(hits), none["text"][:60], none["links"]), data=out, done=ok)


def item19(b):
    """The podcast page on a phone: the first episode link, and a listen control on screen one."""
    pg = b.page("podcast.html", PHONE, wait=1500)
    r = pg.evaluate("""() => { const vh = innerHeight;
      const a = [...document.querySelectorAll('a[href*="episodes/"]')].filter(e => e.getClientRects().length && e.getBoundingClientRect().height > 0)
        .map(e => (e.getBoundingClientRect().top + scrollY) / vh).sort((x, y) => x - y)[0];
      const play = [...document.querySelectorAll('button, audio')].filter(e => e.getClientRects().length && /play|listen/i.test(e.getAttribute('aria-label') || e.textContent || e.tagName))
        .map(e => (e.getBoundingClientRect().top + scrollY) / vh).sort((x, y) => x - y)[0];
      return {link: a !== undefined ? +a.toFixed(2) : null, play: play !== undefined ? +play.toFixed(2) : null}; }""")
    B.done(pg)
    ok = r["link"] is not None and r["link"] < 1 and r["play"] is not None and r["play"] < 1
    return dict(summary="first episode link at screen %s, first listen control at %s (feeds blocked)" % (r["link"], r["play"]), data=r, done=ok)


def item20(b):
    """Topics: Srs and Ccc written as the site writes them, a filter box, the sparkline captioned."""
    pg = b.page("tags.html", PHONE, wait=800)
    r = pg.evaluate("""() => { const t = document.body.innerText;
      return {srs: /\\bSrs\\b/.test(t), ccc: /\\bCcc\\b/.test(t), filter: !![...document.querySelectorAll('input')].find(i => i.getClientRects().length),
              caption: !!document.querySelector('.v4-spark-cap, figcaption.tg-cap, .tg-spark-cap')}; }""")
    B.done(pg)
    ok = not r["srs"] and not r["ccc"] and r["filter"] and r["caption"]
    return dict(summary="\"Srs\" %s, \"Ccc\" %s, filter box %s, sparkline caption %s"
                % ("shown" if r["srs"] else "gone", "shown" if r["ccc"] else "gone", r["filter"], r["caption"]), data=r, done=ok)


# --------------------------------------------------------------------------------------------- E. every template

def item21(b):
    """One main landmark per page (axe landmark-one-main), 20 templates at phone, tablet and desktop, and the skip link's target."""
    fails, views, skip_bad = [], 0, []
    for rel in TEMPLATES:
        for name, opts in (("phone", PHONE), ("tablet", TABLET), ("desktop", DESK)):
            pg = b.page(rel, opts, wait=500)
            v = axe(pg, ["landmark-one-main", "landmark-no-duplicate-main"])
            s = pg.evaluate("""() => { const a = document.querySelector('a.v4-skip, a[href="#v4-main"], .skip-link'); if (!a) return 'no skip link';
                const t = document.getElementById((a.getAttribute('href') || '').slice(1)); return t ? (t.tagName === 'MAIN' || t.closest('main') ? '' : t.tagName) : 'no target'; }""")
            B.done(pg)
            views += 1
            if v:
                fails.append("%s@%s" % (rel, name))
            if s and name == "desktop":
                skip_bad.append("%s: %s" % (rel, s))
    return dict(summary="landmark-one-main fails on %d of %d page views; skip link not on main on %d templates" % (len(fails), views, len(skip_bad)),
                data=dict(fails=fails, skip=skip_bad), done=not fails and not skip_bad)


def item22(b):
    """Small text on a phone: share of characters under 12px (drawings excepted)."""
    out = {}
    for rel in ("index.html", "knowledge-base.html", "library.html", "sitemap.html", "fly-options.html", "about.html",
                "podcast.html", EPISODE, "destinations/india.html", "knowledge-base/flight-mechanics.html", "tags.html", "enquire.html"):
        pg = b.page(rel, PHONE, wait=900)
        scroll_through(pg)
        out[rel] = pg.evaluate(SMALL_JS)
        B.done(pg)
    allmin = min([v["min"] for v in out.values() if v["min"]] or [12])
    f = lambda r: "%s %.0f%%" % (r.split("/")[-1].replace(".html", ""), out[r]["pct"])
    return dict(summary="; ".join(f(r) for r in ("index.html", "knowledge-base.html", "library.html", "sitemap.html", "fly-options.html",
                                                  "about.html")) + "; smallest %.1fpx" % allmin,
                data=out, done=all(v["chars"] == 0 for v in out.values()))


def item23(b):
    """Footage: a pause control beside Wind sound; the hero label's shade; the 1080p clip at 1920."""
    pg = b.page("index.html", DESK, wait=1500)
    r = pg.evaluate("""() => { const w = [...document.querySelectorAll('button')].find(x => /wind/i.test(x.textContent + (x.getAttribute('aria-label') || '')));
      const p = [...document.querySelectorAll('button')].find(x => /pause|play.*(film|footage|video)|stop the (film|footage)/i.test(x.textContent + ' ' + (x.getAttribute('aria-label') || '')));
      return {wind: !!w, pause: !!p, near: !!(w && p && w.parentElement === p.parentElement)}; }""")
    B.done(pg)
    pg = b.page("index.html", WIDE, wait=3500)
    v = pg.evaluate("""() => [...document.querySelectorAll('video')].filter(v => v.getClientRects().length && v.currentSrc).map(v => {
        const r = v.getBoundingClientRect(); return {src: v.currentSrc.split('/').pop(), box: Math.round(r.width), vw: v.videoWidth}; })""")
    B.done(pg)
    hero = v[0] if v else {}
    r["hero1920"] = hero
    ok = r["pause"] and r["near"] and hero and "1080" in hero.get("src", "")
    return dict(summary="pause control %s (beside Wind sound %s); at 1920 the hero plays %s in a %s px box"
                % (r["pause"], r["near"], hero.get("src"), hero.get("box")), data=r, done=ok)


def item24(b):
    """Touch wording: no 'Click a ...' helper line on a touch screen (headings stay as they are)."""
    out = {}
    for rel in ("index.html", "podcast.html", "sitemap.html"):
        pg = b.page(rel, PHONE, wait=900)
        out[rel] = pg.evaluate("""() => [...document.querySelectorAll('p, span, small, div')].filter(e => e.getClientRects().length &&
            [...e.childNodes].some(n => n.nodeType === 3 && /\\bclick (a|on)\\b/i.test(n.textContent))).map(e => e.textContent.trim().slice(0, 60))""")
        B.done(pg)
    n = sum(len(v) for v in out.values())
    return dict(summary="%d helper lines say click on a phone: %s" % (n, "; ".join(x for v in out.values() for x in v)[:160] or "none"),
                data=out, done=n == 0)


def item25(b):
    """The sitemap's stars on a phone: their hit areas."""
    pg = b.page("sitemap.html", PHONE, wait=2500)
    r = pg.evaluate("""() => { const st = [...document.querySelectorAll('.sky-stars a, .sky-stars button, .sky-stars [role=button], .sky-stars [tabindex], .sky-star, [data-star]')]
        .filter(e => e.getClientRects().length);
      const rs = st.map(e => e.getBoundingClientRect()); const m = rs.map(r => Math.min(r.width, r.height)).sort((a, b) => a - b);
      return {n: st.length, min: m.length ? +m[0].toFixed(1) : null, median: m.length ? +m[Math.floor(m.length / 2)].toFixed(1) : null,
              tag: st[0] ? st[0].tagName + '.' + (st[0].className.baseVal !== undefined ? st[0].className.baseVal : st[0].className) : null}; }""")
    v = axe(pg, ["target-size"])
    B.done(pg)
    r["axe"] = v
    n = sum(x["n"] for x in v) if v is not None else None
    return dict(summary="%d stars, hit areas %s px (median %s); axe target-size %s" % (r["n"], r["min"], r["median"], "pass" if n == 0 else "%s fail" % n),
                data=r, done=r["n"] > 0 and r["min"] is not None and r["min"] >= 24 and n == 0)


def item26(b):
    """Width and height on images (static: every <img> in the page's HTML)."""
    out = {}
    for rel in ("partners.html", "knowledge-base.html", "fly-options.html", "index.html", "about.html", "podcast.html"):
        src = open(os.path.join(ROOT, "prototypes", SITE, rel), encoding="utf-8").read()
        src = re.sub(r"<script\b.*?</script>", "", src, flags=re.S)
        ims = re.findall(r"<img\b[^>]*>", src)
        miss = [i for i in ims if not (re.search(r"\swidth=", i) and re.search(r"\sheight=", i))]
        out[rel] = (len(miss), len(ims))
    return dict(summary=", ".join("%s %d of %d missing" % (r.replace(".html", ""), a, b_) for r, (a, b_) in out.items()),
                data=out, done=all(a == 0 for a, _ in out.values()))


def item27(b):
    """The enquiry form: an empty send shows a message under each field that needs one, and brings the first into view."""
    pg = b.page("enquire.html", PHONE, wait=600)
    pg.evaluate("document.getElementById('message') && (document.getElementById('message').value = '')")
    pg.evaluate("scrollTo(0, document.documentElement.scrollHeight)")
    pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('#enqForm button[type=submit]').click()")
    pg.wait_for_timeout(900)
    r = pg.evaluate("""() => { const inv = [...document.querySelectorAll('#enqForm :invalid')].filter(e => e.tagName !== 'FORM' && e.tagName !== 'FIELDSET');
      const first = inv[0]; const msgs = [...document.querySelectorAll('#enqForm .enq-err')].filter(e => e.getClientRects().length && e.textContent.trim());
      const r = first ? first.getBoundingClientRect() : null;
      return {invalid: inv.length, messages: msgs.length, described: inv.filter(e => (e.getAttribute('aria-describedby') || '').split(' ').some(id => { const m = document.getElementById(id); return m && m.textContent.trim(); })).length,
              firstInView: !!(r && r.top >= 0 && r.bottom <= innerHeight), focused: document.activeElement === first, firstId: first && first.id}; }""")
    B.done(pg)
    ok = r["invalid"] and r["messages"] >= r["invalid"] and r["described"] == r["invalid"] and r["firstInView"] and r["focused"]
    return dict(summary="%d fields need attention: %d messages under them, first (%s) in view %s, focused %s"
                % (r["invalid"], r["messages"], r["firstId"], r["firstInView"], r["focused"]), data=r, done=ok)


ITEMS = {i: globals()["item%d" % i] for i in range(1, 28)}
TITLES = {1: "Price in the phone action bar", 2: "Dates sooner", 3: "Gallery framing", 4: "Hold a place in context",
          5: "Nothing important folded away", 6: "Weight on a phone", 7: "Desktop sub-navigation",
          8: "Transcript on phones", 9: "Chapters on phones", 10: "Titles that say nothing", 11: "Layout jumps at 1440",
          12: "aria-controls before the target exists", 13: "Ideas first", 14: "Series pages: a jump row",
          15: "The knowledge base hub", 16: "Reading measure", 17: "Library search", 18: "Site search",
          19: "Podcast: latest episode first", 20: "Topics", 21: "One main landmark", 22: "Small text on phones",
          23: "Footage", 24: "Touch wording", 25: "Sitemap stars", 26: "Image width and height", 27: "Enquiry form messages"}


def main():
    global SITE
    args = sys.argv[1:]
    save = compare = None
    if "--site" in args:
        i = args.index("--site")
        SITE = args[i + 1]
        del args[i:i + 2]
    if "--save" in args:
        i = args.index("--save")
        save = args[i + 1]
        del args[i:i + 2]
    if "--compare" in args:
        i = args.index("--compare")
        compare = args[i + 1]
        del args[i:i + 2]
    want = [int(a) for a in args] or list(ITEMS)
    old = {}
    if compare:
        old = json.load(open(os.path.join(OUTDIR, compare + ".json"), encoding="utf-8"))
    path = os.path.join(OUTDIR, (save or "") + ".json")
    res = json.load(open(path, encoding="utf-8")) if save and os.path.exists(path) else {}
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = B(p)
        for i in want:
            t0 = time.time()
            try:
                if i == 6:
                    r = item6(b, old.get("6"))
                else:
                    r = ITEMS[i](b)
            except Exception as e:      # noqa: BLE001 - one item failing must not stop the others
                r = dict(summary="ERROR %s" % str(e)[:200], data=None, done=False)
            r["title"] = TITLES[i]
            res[str(i)] = r
            mark = {True: "done", False: "    ", None: "  - "}[r["done"]]
            print("%2d %s %-36s %s  (%.0fs)" % (i, mark, TITLES[i], r["summary"], time.time() - t0))
            if str(i) in old:
                print("   %s %-36s %s" % ("    ", "  before:", old[str(i)]["summary"]))
            sys.stdout.flush()
        b.close()
    if save:
        os.makedirs(OUTDIR, exist_ok=True)
        res["_when"] = time.strftime("%Y-%m-%d %H:%M")
        res["_site"] = SITE
        json.dump(res, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
        print("saved %s" % os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
