#!/usr/bin/env python3
"""Comp gallery pages: one page per comp the owner covers, pilots browse by task, save the web copy free, buy the
original (chat 20, 4 Nov 2026).

Owner's answers (4 Nov): payment PayPal, EUR 1 a photo, one link per photo carrying its file name; the original is
downloaded on the site after paying (needs private storage and a payment check, not built: until then the buy
button is [to supply]); the free 2400 px copy is CC BY-NC 4.0. The design (D, E or F, docs/designers/gallery/) is
the owner's pick, still open on 4 Nov: render() below takes the chosen sample's markup.

The photos come from the media repo (paraglidingatlas-maker/media-2026), <folder>/photos.json, written by
tools/media_webcopies.py: [{"stem", "day" (T1, T2 ...), "w", "h", "shot"}] in the owner's file order. "shot" (EXIF
time) is never shown or sorted on (the Piedrahita originals read 31 Aug, after the comp). No Drive id or folder link
ever goes on a page: the originals are what the owner sells.

The pages are owned pages (tools/v4_build.py owned() takes media*.html), live through NEW_PAGES in tools/v2_site.py.
After running this, build in a clean worktree and copy the pages back before committing (the build writes its own
?v= hashes; see docs/v4-next-session.md, chat 19).

    python3 tools/v4_comp_gallery.py [tapalpa|piedrahita ...] [--repo /home/user/media-2026]
"""
import html
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_media as M  # noqa: E402  (shell(), check(), TBD)

V4 = M.V4
E = html.escape
TBD = M.TBD
BASE = "https://paraglidingatlas-maker.github.io/media-2026/"
REPO = "/home/user/media-2026"
if "--repo" in sys.argv:
    REPO = sys.argv[sys.argv.index("--repo") + 1]

CREDIT = "Photo: Aninder Singh, Paragliding Atlas"
LICENCE = ('Free web copy, 2400 px, under <a href="https://creativecommons.org/licenses/by-nc/4.0/" rel="license noopener" '
           'target="_blank">CC BY-NC 4.0</a>: share it with the credit, not for commercial use.')
PRICE = "EUR 1"
PAYPAL = None          # [to supply]: the owner's PayPal set-up; buy_link() returns None until it exists
DELIVERY = "Download on this page right after paying"     # owner, 4 Nov: "The download has to be on site"

# Facts: only from the owner and docs/designers/gallery-brief.md; a task's date is set when the comp flies it
COMPS = {
    "tapalpa": dict(page="media-srs-tapalpa-2026.html", folder="srs-tapalpa", title="Tapalpa 2026",
                    kicker="SRS Advance Edition &middot; Tapalpa, Mexico",
                    intro="Tasks 8 to 14 Nov 2026: 7 tasks, up to 120 pilots from 44 countries.",
                    desc="SRS Advance Edition, Tapalpa, Mexico, 8 to 14 Nov 2026: every photo by task, free to save, "
                         "the original EUR 1. Photos by Paragliding Atlas.",
                    tasks=["T%d" % i for i in range(1, 8)], window=("2026-11-08", "2026-11-14"), dates={}),
    "piedrahita": dict(page="media-srs-piedrahita-2026.html", folder="srs-piedrahita", title="Piedrahita 2026",
                       kicker="SRS BGD Edition &middot; Piedrahita, Ávila, Spain",
                       intro="22 to 29 Aug 2026, FAI Category 2: 120 pilots from 54 countries.",
                       desc="SRS BGD Edition, Piedrahita, Spain, 22 to 29 Aug 2026: every photo by task, free to save, "
                            "the original EUR 1. Photos by Paragliding Atlas.",
                       tasks=["T1", "T2", "T3"], window=("2026-08-22", "2026-08-29"), dates={},
                       videos={"T1": "uCEfssE40u8", "T2": "NXUEyPQ3V4E"}, day1="cuGs7Lk6Dt4"),
}


def photos(comp):
    """the comp's photos.json, from the local media repo, else from the published site; [] before the first night"""
    c = COMPS[comp]
    p = os.path.join(REPO, c["folder"], "photos.json")
    try:
        return json.load(open(p))
    except OSError:
        pass
    try:
        with urllib.request.urlopen(BASE + c["folder"] + "/photos.json", timeout=20) as r:
            return json.load(r)
    except Exception:
        return []


def src(comp, stem, w):
    return "%s%s/%s-%d.webp" % (BASE, COMPS[comp]["folder"], stem, w)


def srcset(comp, stem, ws=(800, 1600, 2400)):
    return ", ".join("%s %dw" % (src(comp, stem, w), w) for w in ws)


def label(task):
    return "Task " + task[1:] if task.startswith("T") else task


def days(comp):
    """[(task, label, [photo rows])] for every task of the comp, in order, empty tasks included (they say when)"""
    rows = photos(comp)
    by = {}
    for r in rows:
        by.setdefault(r.get("day") or "", []).append(r)
    stray = [k for k in by if k not in COMPS[comp]["tasks"]]
    assert not stray, "photos with a day the comp does not have: %s (check --day-re)" % stray
    return [(t, label(t), by.get(t, [])) for t in COMPS[comp]["tasks"]]


def buy_link(stem):
    """the payment link for one photo, carrying its file name; None until the owner's PayPal set-up exists"""
    return PAYPAL(stem) if PAYPAL else None


def buy_note(stem):
    return ("%s, %s. %s." % (E(stem), PRICE, DELIVERY)) if buy_link(stem) else ("%s, %s: payment %s" % (E(stem), PRICE, TBD))


def render(comp):
    """the page's main, in the owner's chosen design; set DESIGN once they pick"""
    raise SystemExit("the owner has not picked the gallery design yet (D, E or F): see docs/v4-next-session.md")


def page(comp):
    c = COMPS[comp]
    rows = photos(comp)
    og = src(comp, rows[0]["stem"], 1600) if rows else "https://paraglidingatlas.com/assets/images/hero.jpg"
    out = M.shell(c["title"], c["desc"], c["page"], og, c["title"], render(comp))
    M.check(c["page"], out)
    body = out.split('<main id="v4-main">')[1].split("</main>")[0]
    assert "drive.google" not in body, "a Drive link on " + c["page"]
    return out


if __name__ == "__main__":
    which = [a for a in sys.argv[1:] if a in COMPS] or list(COMPS)
    for comp in which:
        s = page(comp)
        open(os.path.join(V4, COMPS[comp]["page"]), "w").write(s)
        print("wrote prototypes/v4/%s (%d photos)" % (COMPS[comp]["page"], len(photos(comp))))
