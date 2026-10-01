"""Deep links into episode chapters (and other cross-page #fragments) on the LIVE site.

python3 deeplink.py cold [phone|desktop|both] [limit]   cold-load every cross-page fragment target
python3 deeplink.py click [phone|desktop|both] [limit]  click a mid chapter in the rail, then 'Continue reading'
python3 deeplink.py one <path#frag> [phone|desktop]     single URL, verbose
"""
import sys, os, json, time, concurrent.futures as cf
sys.path.insert(0, "/home/user/Website/tools/stress")
import lib

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8895
VP = {"phone": dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True),
      "desktop": dict(viewport={"width": 1280, "height": 800})}

MEASURE = r"""(id) => {
  const t = document.getElementById(id);
  if (!t) return {missing: true};
  const vh = innerHeight, vw = innerWidth;
  let hdr = 0, hdrSel = null;
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if ((cs.position === 'fixed' || cs.position === 'sticky') && cs.visibility !== 'hidden' && cs.display !== 'none'
        && parseFloat(cs.opacity) > 0.05) {
      const b = el.getBoundingClientRect();
      if (b.top <= 2 && b.bottom > 0 && b.bottom < vh * 0.5 && b.width > vw * 0.5 && b.height > 0 && b.bottom > hdr) {
        hdr = b.bottom; hdrSel = el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '');
      }
    }
  }
  const r = t.getBoundingClientRect();
  let clip = null, a = t.parentElement;
  while (a && a !== document.body) {
    const cs = getComputedStyle(a);
    if (/(hidden|clip)/.test(cs.overflowY) && a.scrollHeight > a.clientHeight + 4) {
      const ar = a.getBoundingClientRect();
      clip = {cls: a.className, id: a.id, top: ar.top, bottom: ar.bottom, scrollTop: a.scrollTop,
              scrollH: a.scrollHeight, clientH: a.clientHeight};
      break;
    }
    a = a.parentElement;
  }
  let op = 1;
  for (let e = t; e && e.nodeType === 1; e = e.parentElement) op *= parseFloat(getComputedStyle(e).opacity);
  const top = Math.max(r.top, hdr, clip ? clip.top : -1e9), bot = Math.min(r.bottom, vh, clip ? clip.bottom : 1e9);
  const hx = r.left + Math.min(24, r.width / 2), hy = Math.max(r.top, hdr) + 8;
  const hit = (hy < vh && hy > 0) ? document.elementFromPoint(hx, hy) : null;
  const hitOk = !!hit && (t.contains(hit) || hit.contains(t));
  let hitSel = hit ? hit.tagName.toLowerCase() + (hit.className && typeof hit.className === 'string' ? '.' + hit.className.trim().split(/\s+/)[0] : '') : null;
  const head = (t.querySelector('h1,h2,h3,h4,.cd-block-title,strong') || t).textContent.trim().slice(0, 60);
  const more = document.querySelector('.cd-more');
  let moreR = null;
  if (more) { const m = more.getBoundingClientRect(); moreR = {top: m.top, bottom: m.bottom, text: more.textContent.trim().replace(/\s+/g, ' ').slice(0, 60)}; }
  return {top: r.top, bottom: r.bottom, height: r.height, hdr, hdrSel, clip, opacity: +op.toFixed(3),
          visiblePx: Math.max(0, bot - top), hitOk, hitSel, scrollY: scrollY, vh, head, more: moreR,
          docH: document.documentElement.scrollHeight};
}"""


def verdict(m):
    if m.get("missing"):
        return "missing"
    if m["opacity"] < 0.5:
        return "transparent"
    if m["top"] < m["hdr"] - 4 and m["bottom"] > m["hdr"]:
        return "start-under-header"
    if m["top"] >= m["vh"] or m["bottom"] <= m["hdr"]:
        return "not-in-view"
    if m["clip"] and m["clip"]["scrollTop"] > 0:
        return "inside-scrolled-clip"
    if m["top"] > m["hdr"] + 0.4 * m["vh"]:
        return "lands-low"
    if not m["hitOk"]:
        return "covered"
    return "ok"


def _ctx(b, mode):
    ctx = b.new_context(**VP[mode])
    base = "http://127.0.0.1:%d/" % PORT
    ctx.route("**/*", lambda route: route.continue_() if route.request.url.startswith(base) else route.abort())
    return ctx


def cold_job(args):
    items, mode = args
    out = []
    base = "http://127.0.0.1:%d/" % PORT
    with lib.browser() as b:
        ctx = _ctx(b, mode)
        pg = ctx.new_page()
        for path, frag in items:
            rec = {"url": path + "#" + frag, "mode": mode}
            try:
                pg.goto(base + path + "#" + frag, wait_until="load", timeout=30000)
                pg.wait_for_timeout(1500)
                m1 = pg.evaluate(MEASURE, frag)
                pg.wait_for_timeout(1500)
                m2 = pg.evaluate(MEASURE, frag)
                rec.update(m1=m1, m2=m2, v1=verdict(m1), v2=verdict(m2))
            except Exception as e:
                rec["error"] = str(e)[:200]
            out.append(rec)
            pg.goto("about:blank")
        ctx.close()
    return out


def click_job(args):
    items, mode = args
    out = []
    base = "http://127.0.0.1:%d/" % PORT
    with lib.browser() as b:
        ctx = _ctx(b, mode)
        pg = ctx.new_page()
        for path in items:
            rec = {"page": path, "mode": mode}
            try:
                pg.goto(base + path, wait_until="load", timeout=30000)
                pg.wait_for_timeout(800)
                chaps = pg.eval_on_selector_all(".cd-chap", "els => els.map(e => e.getAttribute('href'))")
                rec["nchap"] = len(chaps)
                if len(chaps) < 3:
                    rec["skip"] = "fewer than 3 chapters"; out.append(rec); continue
                href = chaps[len(chaps) // 2]
                frag = href[1:]
                rec["chapter"] = href
                pg.locator('.cd-chap[href="%s"]' % href).first.click(timeout=5000)
                pg.wait_for_timeout(1400)
                m1 = pg.evaluate(MEASURE, frag)
                rec.update(after_click=m1, v_click=verdict(m1))
                # what the reader sees inside the clip box: text at the top of the visible clip window
                more = pg.locator(".cd-more").first
                if more.count() and m1.get("clip"):
                    rec["more_visible_after_click"] = (m1["more"] is not None and m1["more"]["top"] < m1["vh"] and m1["more"]["bottom"] > 0)
                    # reader scrolls a little to reach the button, as a person would
                    more.scroll_into_view_if_needed()
                    pg.wait_for_timeout(300)
                    m_before = pg.evaluate(MEASURE, frag)
                    more.click(timeout=5000)
                    pg.wait_for_timeout(1200)
                    m_after = pg.evaluate(MEASURE, frag)
                    rec.update(before_expand=m_before, after_expand=m_after, v_expand=verdict(m_after),
                               jump=round(m_after["top"] - m_before["top"]))
            except Exception as e:
                rec["error"] = str(e)[:300]
            out.append(rec)
        ctx.close()
    return out


def pool(fn, items, modes, workers=4):
    jobs = []
    for mode in modes:
        n = max(1, (len(items) + workers - 1) // workers)
        for i in range(0, len(items), n):
            jobs.append((items[i:i + n], mode))
    res = []
    with cf.ProcessPoolExecutor(max_workers=workers) as ex:
        for r in ex.map(fn, jobs):
            res.extend(r)
    return res


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "cold"
    arg2 = sys.argv[2] if len(sys.argv) > 2 and cmd != "one" else "both"
    modes = {"phone": ["phone"], "desktop": ["desktop"], "both": ["phone", "desktop"]}[arg2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 and cmd != "one" else 10 ** 6
    inv = json.load(open(os.path.join(HERE, "frag_inv.json")))
    t0 = time.time()
    with lib.server(PORT):
        if cmd == "cold":
            items = sorted((p, f) for p, fs in inv["targets"].items() for f in fs)[:limit]
            res = pool(cold_job, items, modes)
            from collections import Counter
            for mode in modes:
                rs = [r for r in res if r["mode"] == mode]
                print(mode, "v1", Counter(r.get("v1", "error") for r in rs), "v2", Counter(r.get("v2", "error") for r in rs))
            json.dump(res, open(os.path.join(HERE, "deeplink_cold.json"), "w"), indent=1)
        elif cmd == "click":
            items = sorted(p for p in lib.pages("live") if p.startswith("episodes/"))[:limit]
            res = pool(click_job, items, modes)
            from collections import Counter
            for mode in modes:
                rs = [r for r in res if r["mode"] == mode and "chapter" in r]
                print(mode, len(rs), "click", Counter(r.get("v_click", "error") for r in rs),
                      "expand", Counter(r.get("v_expand", "n/a") for r in rs))
                jumps = sorted(r["jump"] for r in rs if "jump" in r)
                if jumps:
                    print("  jump px after Continue reading: min", jumps[0], "median", jumps[len(jumps) // 2], "max", jumps[-1])
            json.dump(res, open(os.path.join(HERE, "deeplink_click.json"), "w"), indent=1)
        elif cmd == "one":
            path, frag = sys.argv[2].split("#")
            mode = sys.argv[3] if len(sys.argv) > 3 else "phone"
            r = cold_job(([(path, frag)], mode))
            print(json.dumps(r, indent=1))
    print("secs", round(time.time() - t0))


if __name__ == "__main__":
    main()
