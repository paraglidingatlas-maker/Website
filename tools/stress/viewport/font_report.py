#!/usr/bin/env python3
"""Compare baseline vs 200% text (Chrome default font size 32px via CDP Page.setFontSizes, and a
html{font-size:200%!important} stylesheet) from results_font200.json. python3 font_report.py [file]"""
import json, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results_font200.json")))
W = {"390x844": 390, "1280x800": 1280}
by = {(x["page"], x["size"], x["font"]): x for x in R}
def clip(x):
    return [c for c in x.get("clipped", []) if c["partial"] and not (c["ellipsis"] or c["clamp"] or c["ariaHidden"])]
print("errors:", [(x["page"], x["size"], x["font"], x["error"][:80]) for x in R if x.get("error")])
for size in W:
    print("\n##", size)
    for page in sorted(set(x["page"] for x in R)):
        row = []
        for fm in (None, "setfont32", "css200"):
            x = by.get((page, size, fm))
            if not x or x.get("error"):
                row.append("%s: ERR" % fm); continue
            fx = x.get("fixedScroll", [])
            u = max([f["unionFrac"] for f in fx] or [0])
            big = max([i["frac"] for f in fx for i in f["items"] if i["stuck"] and i["wfrac"] >= .5 and i["pe"] != "none"] or [0])
            row.append("%s root=%s p=%s sw=%d off=%d clip=%d offTxt=%d cov=%d fixU=%.2f" % (
                fm or "base", x["rootFont"], x.get("paraFsMedian"), x["scrollWidth"], x["overflow"]["nOffenders"], len(clip(x)),
                x.get("nOffscreenText", 0), len(x.get("coveredConfirmed", [])), max(u, big)))
        print(" ", page); [print("     ", r) for r in row]
print("\n## new problems under 200% text (not present in baseline)")
for (page, size, fm), x in sorted(by.items(), key=lambda kv: str(kv[0])):
    if fm is None or x.get("error"): continue
    b = by.get((page, size, None))
    if not b or b.get("error"): continue
    bk = {(c["anc"], c["axis"]) for c in clip(b)}
    newc = [c for c in clip(x) if (c["anc"], c["axis"]) not in bk]
    bo = {o["sel"] for o in b["overflow"]["offenders"]}
    newo = [o for o in x["overflow"]["offenders"] if not o["hidden"] and not o["fixed"] and o["sel"] not in bo]
    bt = {o["sel"] for o in b.get("offscreenText", [])}
    newt = [o for o in x.get("offscreenText", []) if o["sel"] not in bt]
    bcv = {c["sel"] for c in b.get("coveredConfirmed", [])}
    newcv = [c for c in x.get("coveredConfirmed", []) if c["sel"] not in bcv]
    if newc or newo or newt or newcv or x["scrollWidth"] > W[size] + 1:
        print("  %s @%s %s: sw=%d" % (page, size, fm, x["scrollWidth"]))
        for o in newo[:4]: print("     overflow", o["sel"][-60:], "right", o["right"], "w", o["w"], "parentW", o["parentW"], repr(o["text"][:30]))
        for c in newc[:5]: print("     clipped", c["anc"][-60:], c["axis"], "over", c["over"], "fs", c.get("fs"), repr(c["text"][:40]))
        for t in newt[:4]: print("     offscreen", t["sel"][-60:], "over", t["over"], repr(t["text"][:30]))
        for c in newcv[:4]: print("     covered", c["sel"][-50:], "by", c["centred"].get("by", "")[-50:], c["centred"].get("byPos"))
