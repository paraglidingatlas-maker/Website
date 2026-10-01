#!/usr/bin/env python3
"""Group results_sizes.json (from run_viewport.py sizes) by root cause. python3 aggregate.py [results.json]"""
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
fp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results_sizes.json")
R = json.load(open(fp))
W = {"280x653": 280, "320x568": 320, "844x390": 844, "2560x1440": 2560, "3840x2160": 3840}
H = {"280x653": 653, "320x568": 568, "844x390": 390, "2560x1440": 1440, "3840x2160": 2160}


def tail(sel, n=2):
    s = re.sub(r"\.(in|is-on|is-front|active|is-hot|kr)\b", "", sel)
    return " > ".join(s.split(" > ")[-n:])


def show(title, groups, n=10):
    print("\n=== " + title)
    for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        pages = sorted(set(p for p, _, _ in v))
        sizes = sorted(set(s for _, s, _ in v))
        print("  [%d recs, %d pages, sizes %s] %s" % (len(v), len(pages), ",".join(sizes), k))
        for p, s, info in v[:3]:
            print("      e.g. %s @%s %s" % (p, s, info))
        print("      pages: " + ", ".join(pages[:n]) + (" ..." if len(pages) > n else ""))


errs = [(x["page"], x["size"], x.get("error")) for x in R if x.get("error")]
print("records", len(R), "errors", len(errs))
for e in errs[:10]:
    print("  ERR", e)
pe = collections.Counter()
for x in R:
    for e in x.get("pageErrors", []):
        pe[e[:120]] += 1
print("page JS errors:", pe.most_common(8))

# 1 horizontal overflow
ov = collections.defaultdict(list)
for x in R:
    if x.get("error"):
        continue
    vw = W[x["size"]]
    if x["scrollWidth"] > vw + 1 or x["innerWidth"] > vw + 1:
        offs = x["overflow"]["offenders"]
        key = tail(offs[0]["sel"]) + (" [hidden]" if offs and offs[0]["hidden"] else "") + (" [fixed]" if offs and offs[0]["fixed"] else "") if offs else "(no offender found)"
        ov[key].append((x["page"], x["size"], "sw=%d iw=%d right=%s w=%s parentW=%s" % (
            x["scrollWidth"], x["innerWidth"], offs[0]["right"] if offs else None, offs[0]["w"] if offs else None,
            offs[0]["parentW"] if offs else None)))
show("HORIZONTAL OVERFLOW (scrollWidth or innerWidth > viewport) by top offender", ov)

# 2 clipped text (partial, not intentional truncation)
cl = collections.defaultdict(list)
for x in R:
    for c in x.get("clipped", []):
        if c["partial"] == 0:
            continue
        tag = "intentional(ellipsis/clamp)" if (c["ellipsis"] or c["clamp"]) else ("aria-hidden" if c["ariaHidden"] else "")
        cl[tail(c["anc"]) + " axis=" + c["axis"] + " " + tag].append(
            (x["page"], x["size"], "over=%dpx partial=%d full=%d fs=%s text=%r" % (c["over"], c["partial"], c["full"], c.get("fs"), c["text"][:40])))
show("TEXT CLIPPED BY ITS OWN BOX (partial)", cl)

# 3 text beyond viewport
ot = collections.defaultdict(list)
for x in R:
    for c in x.get("offscreenText", []):
        ot[tail(c["sel"])].append((x["page"], x["size"], "over=%d n=%d full=%d text=%r ah=%s" % (c["over"], c["n"], c["full"], c["text"][:30], c["ariaHidden"])))
show("TEXT BEYOND VIEWPORT EDGE (not in a scroller)", ot)

# 4 covered interactive
cv = collections.defaultdict(list)
for x in R:
    for c in x.get("coveredConfirmed", []):
        cv[tail(c["sel"], 2) + "  <-covered-by-  " + tail(c["centred"].get("by", ""), 2) + " (" + str(c["centred"].get("byPos", ""))[:40] + ")"].append(
            (x["page"], x["size"], "text=%r at=%s,%s" % (c["text"][:30], c["centred"].get("x"), c["centred"].get("y"))))
show("INTERACTIVE COVERED EVEN WHEN SCROLLED TO CENTRE", cv)

# 5 fixed / sticky coverage
fx = collections.defaultdict(list)
for x in R:
    vh = H[x["size"]]
    for f in x.get("fixedScroll", []):
        for it in f["items"]:
            if it["stuck"] and it["frac"] > 0.35 and it["wfrac"] >= 0.5 and it["h"] < 0.9 * vh and it["pe"] != "none":
                fx[tail(it["sel"]) + " " + it["pos"]].append((x["page"], x["size"], "y=%d frac=%.2f h=%d top=%d" % (f["scrollY"], it["frac"], it["h"], it["top"])))
        if f["unionFrac"] > 0.35:
            fx["UNION " + " + ".join(sorted(set(tail(i["sel"], 1) for i in f["items"] if i["stuck"] and i["wfrac"] >= .5)))].append(
                (x["page"], x["size"], "y=%d union=%.2f" % (f["scrollY"], f["unionFrac"])))
show("FIXED/STICKY > 35% OF VIEWPORT HEIGHT", fx)
um = collections.defaultdict(float)
for x in R:
    for f in x.get("fixedScroll", []):
        um[x["size"]] = max(um[x["size"]], f["unionFrac"])
print("  max union coverage per size:", dict(um))

# 6 covered by fixed at the page bottom (cannot be scrolled out)
cb = collections.defaultdict(list)
for x in R:
    fs = x.get("fixedScroll", [])
    if not fs:
        continue
    last = fs[-1]
    if last["scrollY"] >= last["maxScroll"] - 2:
        for c in last.get("coveredByFixed", []):
            cb[tail(c["sel"]) + " <- " + tail(c["by"], 1)].append((x["page"], x["size"], "text=%r y=%d" % (c["text"], c["y"])))
show("COVERED BY A FIXED LAYER AT MAX SCROLL", cb)

# 7 dialogs
for x in R:
    for d in x.get("dialogs", []):
        bad = [c for c in d["ctrls"] if not (c["inView"] and c["hittable"])]
        print("dialog", x["page"], x["size"], d["sel"], "controls", len(d["ctrls"]), "unreachable", [(c["text"], c["l"], c["t"], c["by"]) for c in bad][:5],
              "closed via", x.get("dialogClosedVia"))

# 8 large screens
print("\n=== LARGE SCREENS")
for s in ("2560x1440", "3840x2160"):
    xs = [x for x in R if x["size"] == s and not x.get("error")]
    ll = [x for x in xs if x.get("nLongLines")]
    small = [x for x in xs if x.get("paraFsMedian") and x["paraFsMedian"] < 14]
    print(" %s: pages with a paragraph >120ch: %d; pages with median paragraph font <14px: %d; body font sizes %s" % (
        s, len(ll), len(small), collections.Counter(x["bodyFont"] for x in xs).most_common(4)))
    g = collections.defaultdict(list)
    for x in ll:
        for l in x["longLines"]:
            g[tail(l["sel"])].append((x["page"], s, "widthCh=%s cpl=%s lines=%s fs=%s wpx=%s" % (l["widthCh"], l["cpl"], l["lines"], l["fs"], l["wpx"])))
    show("long lines @" + s, g)
    print("  small para font pages:", [(x["page"], x["paraFsMedian"]) for x in small][:12])
    print("  mainW", collections.Counter(x["mainW"] for x in xs).most_common(5))
tt = collections.defaultdict(list)
for x in R:
    if x.get("tinyText"):
        tt[x["size"]].append(x["tinyText"])
print("tiny text (<12px) nodes per page, by size: " + ", ".join("%s: median %s max %s" % (k, sorted(v)[len(v) // 2], max(v)) for k, v in tt.items()))
