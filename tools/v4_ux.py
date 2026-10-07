#!/usr/bin/env python3
"""
The usability pass on v4 (owner's brief, 7 Oct 2026; docs/ux-report.md).

The page changes that live in HTML. The look and the behaviour are in
src/v2.css and src/v2-immersive.js ("THE USABILITY PASS"). Every change here
uses only words and facts the pages already carry, and is idempotent: it runs
after every other v4 generator and pass, and a rerun changes nothing.

    python3 tools/v4_ux.py              # every v4 page
    python3 tools/v4_ux.py --check      # say what would change, write nothing

Rebuild order for v4: the generators and passes in docs/v4-report.md, then
this, then python3 tools/v4_min.py and python3 tools/v2_localize.py --site v4.

What it does, by the brief's numbers
  1  the trips' phone bar leads with the price the departures already show
     ("£1,100 per pilot", "From US$2,100"), then the length and the next
     departure.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
TRIPS = ("destinations/india.html", "destinations/kenya.html")


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def trip_price(src):
    """The departures' own price line: (label, amount), e.g. ("Per pilot", "£1,100"), ("Starting from", "US$2,100")."""
    m = re.search(r'<p class="kdates-price"><span>([^<]*)</span><b>([^<]*)</b></p>', src)
    if not m:
        raise SystemExit("v4_ux: no departure price")
    return plain(m.group(1)), plain(m.group(2))


# ------------------------------------------------------------------------------------------------ 1
def trip_bar(src):
    """1. The phone action bar: the price first, then the length and the next departure."""
    m = re.search(r'<div class="dst-mobar-l"><span class="n">([^<]+)</span><span class="w">([^<]+)</span></div>', src)
    if not m:
        return src            # done already
    length, nxt = m.group(1).strip(), m.group(2).strip()
    label, amount = trip_price(src)
    if label.lower().endswith("from"):
        n = '<small>From</small> %s' % amount
    else:
        n = '%s <small>%s</small>' % (amount, label.lower())
    new = ('<div class="dst-mobar-l v4u-bar"><span class="n">%s</span>'
           '<span class="w"><span>%s</span> &middot; <span>%s</span></span></div>' % (n, length, nxt))
    return src[:m.start()] + new + src[m.end():]


# ------------------------------------------------------------------------------------------------ 2
def section_span(src, ident):
    """(start, end) of <section ... id="ident">...</section>, with the blank lines after it."""
    i = src.index('id="%s"' % ident)
    a = src.rindex("<section", 0, i)
    depth, pos = 0, a
    tok = re.compile(r"<(/?)section\b[^>]*>")
    for t in tok.finditer(src, a):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            b = t.end()
            while src[b:b + 1] == "\n":
                b += 1
            return a, b
    raise SystemExit("v4_ux: unclosed section " + ident)


def section_ids(src):
    return re.findall(r'<section\b[^>]*\sid="([^"]+)"', src)


def trip_dates_first(src):
    """2. Dates right after the route; the gallery after them. The jump row and the two skip links follow."""
    ids = section_ids(src)
    if ids.index("dates") != ids.index("route") + 1:
        a, b = section_span(src, "dates")
        dates = src[a:b]
        src = src[:a] + src[b:]
        g = section_span(src, "gallery")[0]
        src = src[:g] + dates + src[g:]
    ids = section_ids(src)
    after_gallery = ids[ids.index("gallery") + 1]
    src = re.sub(r'(class="tm-skip" href="#)[^"]+(")', r"\g<1>dates\2", src, count=1)
    src = re.sub(r'(class="gxa-skip" href="#)[^"]+(")', r"\g<1>%s\2" % after_gallery, src, count=1)
    # the jump row in the page's order
    src = re.sub(r'(<a href="#gallery">Gallery</a>)(\s*)(<a href="#dates">Dates</a>)', r"\3\2\1", src, count=1)
    return src


# ------------------------------------------------------------------------------------------------ 5
def element_span(src, start, tag):
    """(start, end) of the <tag> element that opens at start, counting nested tags of the same name."""
    depth = 0
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tag, src[start:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return start, start + t.end()
    raise SystemExit("v4_ux: unclosed <%s>" % tag)


def trip_questions_shown(src):
    """5a. Every question in view: the "One more question" / "Five more questions" fold opens out."""
    m = re.search(r'<details class="v4-fold v4t-faqmore"><summary>[^<]*</summary>', src)
    if not m:
        return src
    a, b = element_span(src, m.start(), "details")
    inner = src[m.end():b - len("</details>")]
    return src[:a] + inner.strip("\n") + src[b:]


def trip_etiquette_band(src):
    """5b. Flying Etiquette as its own band, its heading and first lines in view, right after Before You Book."""
    m = re.search(r'<section class="dst-sec etq v4t-foldsec" id="ground"><details class="v4t-fs"><summary>'
                  r'<span class="v4t-fs-t">(.*?)</span><span class="v4t-fs-mark" aria-hidden="true"></span></summary>', src, re.S)
    if m:
        a, b = element_span(src, m.start() + len('<section class="dst-sec etq v4t-foldsec" id="ground">'), "details")
        body = src[m.end():b - len("</details>")]
        head = '<div class="dst-head v4u-etq-head">%s</div>' % m.group(1)
        sa, sb = element_span(src, m.start(), "section")
        band = '<section class="dst-sec etq v4u-etq" id="ground">%s%s</section>' % (head, body)
        src = src[:sa] + src[sb:]
        r = section_span(src, "reality")[1]
        src = src[:r] + band + "\n\n" + src[r:]
    # the jump row names it
    if 'href="#ground"' not in src[:src.find('</div>', src.find('class="dst-jump-in"'))]:
        src = re.sub(r'(<a href="#reality">[^<]*</a>)', r'\1\n    <a href="#ground">Flying Etiquette</a>', src, count=1)
    return src


# ------------------------------------------------------------------------------------------------ 7
def trip_subnav(src):
    """7. The sub-navigation on a wide screen: the price and Hold a place beside Enquire."""
    if "v4u-jbook" in src:
        return src
    label, amount = trip_price(src)
    price = ('<small>From</small> %s' % amount) if label.lower().endswith("from") else ('%s <small>%s</small>' % (amount, label.lower()))
    return re.sub(r'(<a href="#enquire" class="last">Enquire</a>)',
                  r'\1\n    <span class="v4u-jbook"><span class="v4u-jprice">%s</span>'
                  r'<a href="#dates" class="btn-solid" data-hover><span>Hold a place</span></a></span>' % price.replace("\\", r"\\"),
                  src, count=1)


def page(rel, src):
    if rel in TRIPS:
        src = trip_bar(src)
    return src


def main(args):
    check = "--check" in args
    rels = [a for a in args if not a.startswith("--")] or sorted(
        os.path.relpath(os.path.join(d, f), V4).replace(os.sep, "/")
        for d, _, fs in os.walk(V4) for f in fs if f.endswith(".html") and "/src/" not in os.path.join(d, f))
    changed = []
    for rel in rels:
        fp = os.path.join(V4, rel)
        src = open(fp, encoding="utf-8").read()
        out = page(rel, src)
        if out != src:
            changed.append(rel)
            if not check:
                open(fp, "w", encoding="utf-8").write(out)
    print("v4 ux: %d page%s %s%s" % (len(changed), "" if len(changed) == 1 else "s",
                                     "would change" if check else "changed", (": " + ", ".join(changed[:8])) if changed else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
