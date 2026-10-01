"""axe-core scan of the LIVE site (repo root).

python3 axe_scan.py                 # all 180 pages @390x844 + 15 templates @1440x900
python3 axe_scan.py --mobile-only   # only the 390x844 pass
python3 axe_scan.py --desktop-only  # only the templates @1440x900
python3 axe_scan.py --pages index.html,about.html [--rule color-contrast]
python3 axe_scan.py --workers 2

Writes raw results to results_axe_<vp>.json and an aggregate summary to
summary_axe.json (grouped by rule id). External hosts are aborted (the proxy blocks
them anyway) so pages do not stall on them.
"""
import argparse, json, os, sys, time, multiprocessing as mp
sys.path.insert(0, "/home/user/Website/tools/stress")
import lib

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8815
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"]

SCROLL_JS = """async () => {
  const h = () => Math.max(document.body ? document.body.scrollHeight : 0, document.documentElement.scrollHeight);
  let y = 0, steps = 0;
  while (y < h() && steps < 80) { y += innerHeight * 0.9; scrollTo(0, y); steps++;
    await new Promise(r => setTimeout(r, 60)); }
  scrollTo(0, 0); await new Promise(r => setTimeout(r, 400)); return steps; }"""

AXE_JS = """async (tags) => {
  const r = await axe.run(document, {runOnly: {type: 'tag', values: tags}, resultTypes: ['violations','incomplete'],
                                     elementRef: false});
  const pick = v => ({id: v.id, impact: v.impact, help: v.help, tags: v.tags,
    nodes: v.nodes.map(n => ({target: n.target, html: (n.html || '').slice(0, 300),
      summary: (n.failureSummary || '').slice(0, 400),
      data: (n.any.concat(n.all, n.none).map(c => c.data).filter(Boolean)[0]) || null}))});
  return {violations: r.violations.map(pick), incomplete: r.incomplete.map(v => ({id: v.id, n: v.nodes.length,
    ex: v.nodes.slice(0, 2).map(n => ({target: n.target, why: (n.any.concat(n.all, n.none).map(c => c.message))[0] || ''}))}))};
}"""


def worker(args):
    base, paths, vp, rule = args
    out = {}
    with lib.browser() as b:
        ctx = b.new_context(viewport=vp)
        ctx.route("**/*", lambda route: route.continue_() if lib.own(route.request.url, base) or
                  route.request.url.startswith("data:") or route.request.url.startswith("blob:") else route.abort())
        for p in paths:
            t0 = time.time()
            pg = ctx.new_page()
            rec = {"page": p}
            try:
                pg.goto(base + p, wait_until="load", timeout=45000)
                pg.wait_for_timeout(800)
                rec["scroll_steps"] = pg.evaluate(SCROLL_JS)
                pg.wait_for_timeout(700)
                pg.add_script_tag(path=lib.AXE)
                tags = TAGS
                if rule:
                    pg.evaluate("r => axe.configure({rules: []})", rule)
                res = pg.evaluate(AXE_JS, tags)
                if rule:
                    res["violations"] = [v for v in res["violations"] if v["id"] == rule]
                    res["incomplete"] = [v for v in res["incomplete"] if v["id"] == rule]
                rec.update(res)
            except Exception as e:
                rec["error"] = str(e)[:500]
            rec["secs"] = round(time.time() - t0, 1)
            pg.close()
            out[p] = rec
            print("%-70s %5.1fs viol=%s" % (p, rec["secs"], len(rec.get("violations", [])) if "violations" in rec else rec.get("error")), flush=True)
        ctx.close()
    return out


def run(base, paths, vp, workers, rule):
    chunks = [paths[i::workers] for i in range(workers)]
    with mp.Pool(workers) as pool:
        parts = pool.map(worker, [(base, c, vp, rule) for c in chunks if c])
    res = {}
    for part in parts:
        res.update(part)
    return {p: res[p] for p in paths if p in res}


def aggregate(results):
    rules = {}
    for p, rec in results.items():
        for v in rec.get("violations", []):
            r = rules.setdefault(v["id"], {"id": v["id"], "impact": v["impact"], "help": v["help"],
                                           "tags": [t for t in v["tags"] if t.startswith("wcag") or t == "best-practice"],
                                           "nodes": 0, "pages": [], "examples": [], "_seen": set()})
            r["nodes"] += len(v["nodes"])
            r["pages"].append(p)
            for n in v["nodes"]:
                key = n["html"][:120]
                if len(r["examples"]) < 4 and key not in r["_seen"]:
                    r["_seen"].add(key)
                    r["examples"].append({"page": p, "target": n["target"], "html": n["html"][:220],
                                          "summary": n["summary"][:300], "data": n.get("data")})
    out = []
    for r in sorted(rules.values(), key=lambda r: (-len(r["pages"]), -r["nodes"])):
        r.pop("_seen")
        r["page_count"] = len(r["pages"])
        out.append(r)
    inc = {}
    for p, rec in results.items():
        for v in rec.get("incomplete", []):
            i = inc.setdefault(v["id"], {"nodes": 0, "pages": 0, "ex": v["ex"]})
            i["nodes"] += v["n"]; i["pages"] += 1
    errors = {p: rec["error"] for p, rec in results.items() if "error" in rec}
    return {"rules": out, "incomplete": inc, "errors": errors, "pages_scanned": len(results)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mobile-only", action="store_true")
    ap.add_argument("--desktop-only", action="store_true")
    ap.add_argument("--pages")
    ap.add_argument("--rule")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    t0 = time.time()
    summary = {}
    with lib.server(PORT) as base:
        passes = []
        if not a.desktop_only:
            passes.append(("mobile", {"width": 390, "height": 844},
                           a.pages.split(",") if a.pages else lib.pages("live")))
        if not a.mobile_only:
            passes.append(("desktop", {"width": 1440, "height": 900},
                           a.pages.split(",") if a.pages else lib.TEMPLATES["live"]))
        for name, vp, paths in passes:
            res = run(base, paths, vp, min(a.workers, len(paths)), a.rule)
            suffix = "" if not a.pages else "_subset"
            with open(os.path.join(HERE, "results_axe_%s%s.json" % (name, suffix)), "w") as f:
                json.dump(res, f, indent=1)
            summary[name] = aggregate(res)
    summary["secs"] = round(time.time() - t0)
    fp = os.path.join(HERE, "summary_axe%s.json" % ("" if not a.pages else "_subset"))
    json.dump(summary, open(fp, "w"), indent=1, default=str)
    for name in ("mobile", "desktop"):
        if name not in summary: continue
        s = summary[name]
        print("\n== %s: %d pages, %d errors" % (name, s["pages_scanned"], len(s["errors"])))
        for r in s["rules"]:
            print("  %-32s %-9s nodes=%-5d pages=%-4d e.g. %s" % (r["id"], r["impact"], r["nodes"], r["page_count"], ", ".join(r["pages"][:3])))
        print("  incomplete:", {k: (v["nodes"], v["pages"]) for k, v in s["incomplete"].items()})
    print("total %ss -> %s" % (summary["secs"], fp))
