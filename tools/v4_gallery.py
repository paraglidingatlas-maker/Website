#!/usr/bin/env python3
"""
Every knowledge base drawing on one prototype page (owner, 26 Sep 2026: "gimme
on an html proto page all of them"): prototypes/v4/samples/drawings-all.html.

Grouped by lens, each drawing with the page it sits on; the drawings that
have a phone version show it beside the wide one. The drawings not yet taken
by a lens follow at the end, as they are. Prototype-only, noindex (the shell
from tools/v4_samples.py).

    python3 tools/v4_gallery.py
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_lens  # noqa: E402
import v4_samples as SM  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
KB = os.path.join(V4, "knowledge-base")

LENS = {
    "Computed": ("Physics the page states, worked out rather than sketched.",
                 ["kb-flight-mechanics-brakes", "kb-sky-gods-speed", "kb-weather-patterns-millibars",
                  "kb-weather-patterns-resolution", "kb-new-technologies-airfoil", "kb-know-your-equipment-jerk",
                  "kb-risk-vs-reward-altitude", "kb-weather-patterns"]),
    "Painted": ("Scenes composed as pictures: ridges paling with distance, one light, orange only on the subject.",
                ["kb-meteorology", "kb-sky-gods", "kb-risk-vs-reward", "kb-sky-gods-section", "kb-storytellers-section",
                 "kb-weather-patterns-section", "kb-navigators-section", "kb-navigators-cauca"]),
    "Made for a phone": ("Charts and diagrams redrawn with the kit, each with its own phone version, stacked and at "
                         "reading size.",
                         ["kb-navigators", "kb-world-cups-weight", "kb-sky-gods-hours", "kb-the-dark-side-speed",
                          "kb-risk-vs-reward-stepup", "kb-new-technologies-drag", "kb-know-your-equipment-helmet",
                          "kb-flight-mechanics-thermal", "kb-living-the-dream-chain", "kb-living-the-dream-kit",
                          "kb-living-the-dream-team", "kb-resources-tools-tips-cameras", "kb-risk-vs-reward-ladder",
                          "kb-storytellers-then", "kb-storytellers-heights", "kb-world-cups-task",
                          "kb-brand-stories-tubercles", "kb-brand-stories-rescue", "kb-navigators-thirds"]),
    "The Dark Side, from other episodes": ("Drawn with the kit from the page's own words, on the owner's word.",
                                           ["kb-the-dark-side", "kb-the-dark-side-section", "kb-the-dark-side-brazil"]),
}

CSS = SM.SPEC_CSS + """
.ga-sec{padding:var(--sp-5) var(--gutter) 0;max-width:1320px;margin:0 auto;}
.ga-sec>h2{font-family:var(--font-display);font-size:var(--fs-h2);color:var(--white);margin:0 0 var(--sp-1);}
.ga-sec>p{color:var(--gray-light);max-width:70ch;line-height:1.7;margin:0 0 var(--sp-3);}
.ga-n{color:var(--orange);font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;}
.ga-item{margin:0 0 var(--sp-4);padding:var(--sp-2);background:#141519;border:1px solid var(--line);}
.ga-item h3{font-size:var(--fs-body);color:var(--white);margin:0 0 .2rem;font-weight:600;}
.ga-item .ga-where{font-size:var(--fs-small);color:var(--gray);margin:0 0 var(--sp-2);}
.ga-item .ga-where a{color:var(--orange);}
.ga-row{display:grid;grid-template-columns:1fr;gap:var(--sp-2);align-items:start;}
.ga-row.has-p .ga-p{max-width:360px;margin-top:var(--sp-2);}
.ga-row svg,.ga-row img{display:block;width:100%;height:auto;}
.ga-lab{display:block;font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;color:var(--gray);margin-bottom:.4rem;}
.ga-rest{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,26rem),1fr));gap:var(--sp-3);}
"""


def where():
    """name -> (page file, page title) for every figure on the knowledge base pages."""
    out = {}
    for fn in sorted(os.listdir(KB)):
        s = open(os.path.join(KB, fn), encoding="utf-8").read()
        t = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        title = re.sub(r"<[^>]+>", "", t.group(1)).strip() if t else fn
        for m in re.finditer(r'data-kb="(kb-[a-z0-9-]+)"', s):
            out.setdefault(m.group(1), (fn, html.unescape(title)))
    return out


def title_of(svg):
    m = re.search(r"<title[^>]*>(.*?)</title>", svg, re.S)
    return html.unescape(m.group(1)) if m else ""


def item(name, pages):
    wide, phone = v4_lens.build(name)
    fn, ptitle = pages.get(name, ("", ""))
    link = ('<a href="knowledge-base/%s">%s</a>' % (fn, html.escape(ptitle))) if fn else "not placed"
    # ids stay unique on this page: each drawing already carries its own prefix
    row = '<div class="ga-row%s"><div><span class="ga-lab">Wide</span>%s</div>%s</div>' % (
        " has-p" if phone else "", wide,
        '<div class="ga-p"><span class="ga-lab">Phone</span>%s</div>' % phone if phone else "")
    return '<article class="ga-item"><h3>%s</h3><p class="ga-where">%s · on %s</p>%s</article>' % (
        html.escape(title_of(wide)), name, link, row)


def page():
    pages = where()
    done = set()
    body = ('<header class="kit-hero is-sky v2-page-hero"><div class="kit-hero-copy"><span class="kit-kicker">Sample, not live</span>'
            '<h1>Every drawing</h1><p class="kit-intro">All the knowledge base drawings in v4, grouped by the approach each '
            'takes. Where a drawing has its own phone version, it sits beside the wide one. Each links to the page it '
            'sits on.</p></div></header>')
    for lens, (why, names) in LENS.items():
        names = [n for n in names if n in v4_lens.names()]
        done.update(names)
        body += '<section class="ga-sec"><span class="ga-n">%d drawings</span><h2>%s</h2><p>%s</p>%s</section>' % (
            len(names), lens, why, "".join(item(n, pages) for n in names))
    extra = [n for n in v4_lens.names() if n not in done]
    if extra:
        body += '<section class="ga-sec"><h2>Also redrawn</h2>%s</section>' % "".join(item(n, pages) for n in extra)
        done.update(extra)
    rest = sorted(n for n in pages if n not in done)
    cards = []
    for n in rest:
        fn, ptitle = pages[n]
        cards.append('<article class="ga-item"><h3>%s</h3><p class="ga-where"><a href="knowledge-base/%s">%s</a></p>'
                     '<img src="img/kb/%s.svg" alt="" loading="lazy" decoding="async"></article>' % (
                         n, fn, html.escape(ptitle), n))
    body += ('<section class="ga-sec"><span class="ga-n">%d drawings</span><h2>As they are</h2><p>Not yet taken by a lens: '
             'the flight mechanics three-view and the drawings whose job is already done. Shown as files, so their '
             'type is not the page\'s.</p><div class="ga-rest">%s</div></section>' % (len(rest), "".join(cards)))
    body += '<div style="height:var(--sp-6)"></div>'
    return SM.shell("Every drawing", "All the knowledge base drawings in v4, by lens, with their phone versions.", body, CSS)


def main():
    out = os.path.join(V4, "samples", "drawings-all.html")
    open(out, "w", encoding="utf-8").write(page())
    print("v4 gallery: samples/drawings-all.html, %d KB" % (os.path.getsize(out) // 1024))


if __name__ == "__main__":
    main()
