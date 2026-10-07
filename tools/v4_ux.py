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
  2  Dates come right after the route (the gallery after them), with the
     jump row and the two skip links in the same order; on a phone the
     gallery's pinned run is under three screens and the route's shorter
     (src/v2.css).
  3  (src/v2.css only) the gallery on an upright phone or tablet: each photo
     whole, in a landscape frame.
  4  enquire.html?trip=..&when=..: the departure's facts (as the trip page
     states them) under the title, the form next, the message optional.
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


# ------------------------------------------------------------------------------------------------ 4
def trip_departures(src):
    """The departures as the trip page states them: title, dates (as Hold a place sends them), price."""
    out = []
    for card in re.findall(r'<article class="kdates-card">(.*?)</article>', src, re.S):
        title = plain(re.search(r"<h3>(.*?)</h3>", card, re.S).group(1))
        when = re.search(r'href="\.\./enquire\.html\?trip=\w+&amp;when=([^"]+)"', card).group(1).replace("+", " ")
        label, amount = re.search(r'<p class="kdates-price"><span>([^<]*)</span><b>([^<]*)</b></p>', card).groups()
        out.append({"title": title, "when": html.unescape(when), "label": plain(label), "price": plain(amount)})
    return out


def trip_length(src):
    m = re.search(r'<span class="l">Duration</span><span class="v">([^<]+)</span>', src)
    return plain(m.group(1)) if m else ""


HOLD_MARK = ("<!-- v4u-hold: tools/v4_ux.py -->", "<!-- /v4u-hold -->")
HOLD_HEAD = ("<!-- v4u-holding: tools/v4_ux.py -->", "<!-- /v4u-holding -->")


def put_block(src, marks, block, anchor, before=True):
    """Write block between marks; replace it if it is there, else put it next to anchor."""
    a, b = marks
    new = a + block + b
    if a in src:
        i = src.index(a)
        j = src.index(b, i) + len(b)
        return src[:i] + new + src[j:]
    k = src.index(anchor)
    return src[:k] + new + "\n" + src[k:] if before else src[:k + len(anchor)] + "\n" + new + src[k + len(anchor):]


HOLD_JS = r"""<script>
/* v4, the usability pass (4): arriving from "Hold a place" (?trip=..&when=..), the
   page opens on that departure: the trip, its dates, its length and its price as
   the trip page states them, then the form; the message becomes optional. Any
   other arrival, or dates the trip page does not list, gets the plain form.
   The mailto and the worker hook below are unchanged. */
(function () {
  var de = document.documentElement, box = document.getElementById('v4uHold');
  function plainForm() { de.classList.remove('v4u-holding'); }
  var data, q;
  try { data = JSON.parse(document.getElementById('v4uHoldData').textContent); q = new URLSearchParams(location.search); }
  catch (e) { plainForm(); return; }
  var t = data[(q.get('trip') || '').toLowerCase()], when = q.get('when') || '', dep = null;
  if (t) t.deps.forEach(function (d) { if (d.when === when) dep = d; });
  if (!box || !dep) { plainForm(); return; }
  var sel = document.getElementById('trip');
  function put(k, v) { var e = box.querySelector('[data-k="' + k + '"]'); if (e) e.textContent = v; }
  var place = sel && sel.selectedIndex > 0 ? (sel.options[sel.selectedIndex].text.match(/\(([^)]+)\)/) || [])[1] : '';
  put('trip', dep.title + (place ? ' (' + place + ')' : ''));
  put('when', dep.when);
  put('len', t.len);
  put('price', /from$/i.test(dep.label) ? 'From ' + dep.price : dep.price + ' ' + dep.label.toLowerCase());
  box.hidden = false;
  var m = document.getElementById('message'), lab = document.querySelector('label[for="message"]');
  if (m) m.required = false;
  if (lab && !lab.querySelector('.opt')) { var o = document.createElement('span'); o.className = 'opt'; o.textContent = '(optional)'; lab.appendChild(document.createTextNode(' ')); lab.appendChild(o); }
})();
</script>
"""

HOLD_BOX = """<div class="v4u-hold" id="v4uHold" hidden>
      <p><span class="l">Destination</span><span class="v" data-k="trip"></span></p>
      <p><span class="l">Dates</span><span class="v" data-k="when"></span></p>
      <p><span class="l">Duration</span><span class="v" data-k="len"></span></p>
      <p><span class="l">Price</span><span class="v" data-k="price"></span></p>
    </div>
    """


def enquire_hold(src, trips):
    """4. "Hold a place" in context: the departure's facts at the top, the form on screen one."""
    import json
    data = json.dumps(trips, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    src = put_block(src, HOLD_HEAD,
                    "<script>/[?&]trip=/.test(location.search) && /[?&]when=/.test(location.search) && "
                    "document.documentElement.classList.add('v4u-holding');</script>", "</head>")
    box = HOLD_BOX if 'id="v4uHold"' not in src else None
    if box:
        src = re.sub(r'(<h1>Tell Us About <em class="v2-accent">Your Flying</em></h1>\s*)', lambda m: m.group(1) + box, src, count=1)
    block = '<script type="application/json" id="v4uHoldData">%s</script>\n%s' % (data, HOLD_JS)
    src = put_block(src, HOLD_MARK, block, "<!-- nav-menu -->")
    return src


# ------------------------------------------------------------------------------------------------ 6
PHONE_MEDIA = '(max-aspect-ratio: 2/3)'


def trip_hero_weight(rel, src):
    """6a. The trip heroes: a phone cut of every slide (tools/v4_phone_media.py), and every slide but the first
    waits (data-v4-src): src/v2-immersive.js wakes a slide just before the slideshow shows it."""
    trip = rel.split("/")[-1][:-5]
    first = True

    def slide(m):
        nonlocal first
        pic = m.group(2)
        jpg = re.search(r'(?:data-v4-src|\bsrc)="([^"]+\.jpg)"', pic).group(1)
        name = os.path.basename(jpg)[:-4]
        phone = "../img/hero/%s-%s-p" % (trip, name)
        if not os.path.exists(os.path.join(V4, "destinations", phone + ".webp")):
            raise SystemExit("v4_ux: run tools/v4_phone_media.py first (%s)" % phone)
        if PHONE_MEDIA not in pic:
            pic = ('\n          <source media="%s" srcset="%s.webp" type="image/webp">'
                   '\n          <source media="%s" srcset="%s.jpg">' % (PHONE_MEDIA, phone, PHONE_MEDIA, phone)) + pic
        if not first:
            pic = re.sub(r'(<source\b[^>]*?\s)srcset=', r"\1data-v4-srcset=", pic)
            pic = re.sub(r'(<img\b[^>]*?\s)src=', r"\1data-v4-src=", pic)
        first = False
        return m.group(1) + pic + m.group(3)
    return re.sub(r'(<div class="khero-slide[^"]*">\s*<picture>)(.*?)(</picture>)', slide, src, flags=re.S)


def gallery_lazy(src):
    """6b. Every gallery photograph waits until the gallery comes near (the first two were fetched on arrival)."""
    return re.sub(r'(<figure class="gxa-f[^"]*"[^>]*><picture><source [^>]*><img (?:(?!loading=)[^>])*?)( decoding="async">)',
                  r'\1 loading="lazy"\2', src)


def home_flyby_weight(src):
    """6c. The home page's four expedition photographs wait until the fly-through comes near; without
    script the first one still shows (a noscript copy)."""
    m = re.search(r'<div class="v2-fb-stage" aria-hidden="true">(.*?)\n  </div>', src, re.S)
    if not m or "data-v4-srcset" in m.group(1):
        return src
    stage = m.group(1)
    first = re.search(r"<picture>.*?</picture>", stage, re.S).group(0)
    stage = re.sub(r'(<source\b[^>]*?\s)srcset=', r"\1data-v4-srcset=", stage)
    stage = re.sub(r'(<img\b[^>]*?\s)src=', r"\1data-v4-src=", stage)
    stage = stage.replace("</picture>", "</picture><noscript>%s</noscript>" % first, 1)
    return src[:m.start(1)] + stage + src[m.end(1):]


# ------------------------------------------------------------------------------------------------ 10
_META = None


def meta():
    global _META
    if _META is None:
        import json
        with open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8") as fh:
            _META = {m["slug"]: m for m in json.load(fh)}
    return _META


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", html.unescape(s).lower().replace("vs.", "vs")).strip()


SERIES_LIKE = ("flying filming", "new technologies", "brand stories", "storytellers", "storytime", "living the dream",
               "risk vs reward", "sky gods", "snippet")


def _first_parts():
    seen = {}
    for m in meta().values():
        if not (m.get("guest") or "").strip() or m.get("guest") == "Aninder Singh":
            k = _norm(_parts(m["title"])[0])
            seen[k] = seen.get(k, 0) + 1
    return seen


def _parts(title):
    return [p.strip() for p in re.split(r"\s+[:|]\s+|:\s+|\s+\|\s*|\s+-\s+", title.strip()) if p.strip()]


def describe(m):
    """The episode in its own title's words: {guest, d (the descriptive part: the title without the series'
    name and number and without the guest), paren (what the title adds in brackets after the guest's name),
    tag (the series-like label the title starts with)}. Any of them may be empty."""
    title, series, guest = m["title"].strip(), (m.get("series") or "").strip(), (m.get("guest") or "").strip()
    if guest == "Aninder Singh":
        guest = ""                                      # the host: his own episodes go by their title
    parts = _parts(title)
    s = _norm(series)
    gn = _norm(re.sub(r"\(.*?\)", "", guest))
    names = [_norm(re.sub(r"\(.*?\)", "", x)) for x in re.split(r"\s*&\s*", guest) if x] if guest else []
    keep, paren, tag = [], "", ""
    for p in parts:
        n = _norm(re.sub(r"\(.*?\)", "", p))
        if len(parts) > 1 and ((s and re.fullmatch(re.escape(s) + r"(?: \d+)?", n)) or
                               re.fullmatch(r"(?:%s)(?: \d+)?" % "|".join(SERIES_LIKE), n)):
            tag = tag or p                              # "Sky Gods", "Risk Vs Reward 3", "Flying & Filming 2"
            continue
        if gn and (n == gn or n in names):
            b = re.search(r"\(([^)]+)\)\s*$", p)
            if b and not re.fullmatch(r"(?i)bonus ep|whitepaper", b.group(1)) and _norm(b.group(1)) not in (gn, "robbie"):
                paren = b.group(1)                      # "Marko Milutinovic (Mid-Air Collision)"
            continue
        keep.append(p)
    # a part that is only the guest's interview ("The Russell Ogden Interview") gives way to the next one
    if len(keep) > 1 and gn and gn in _norm(keep[0]) and \
            not re.sub(r"\b(?:the|interview|with|by|of|s)\b", "", _norm(keep[0]).replace(gn, "")).strip():
        keep = keep[1:]
    d = keep[0] if keep else ""
    if not guest and d and _first_parts().get(_norm(d), 0) > 1:
        d = ": ".join(parts)                            # two "Bird's-Eye View of Oslo": the whole title
    for name in sorted(([guest, re.sub(r"\s*\(.*?\)", "", guest)] + re.split(r"\s*&\s*", guest)) if guest else [], key=len, reverse=True):
        if not name:
            continue
        d = re.sub(r"(?i)\s*(?:,|\|)?\s*(?:a talk with|explained by|ft\.|with|by|of)\s+" + re.escape(name) + r".*$", "", d)
        d = re.sub(r"(?i)^" + re.escape(name) + r"(?:'s|’s)?\s+(?:talks about|explains|answers!?|on)?\s*", "", d)
        d = re.sub(r"(?i)\s+" + re.escape(name) + r"\s+answers!?$", "", d)
    d = re.sub(r"\s*\((?:bonus ep|whitepaper)\)", "", d, flags=re.I).strip(" ,:|-")
    if d and d[0].islower():
        d = d[0].upper() + d[1:]
    return {"guest": guest, "d": d, "paren": paren, "tag": tag}


def link_label(m):
    x = describe(m)
    what = x["d"] or x["paren"] or x["tag"]
    if x["guest"] and what:
        return "%s: %s" % (x["guest"], what)
    return x["guest"] or what or m["title"]


def episode_labels(src):
    """10. Related Episodes and Up next say who and what: the guest and the descriptive part of the title
    (no more "Sky Gods" nine times, or the guest's name twice on one card)."""
    E = meta()

    def slug(href):
        return href.split("/")[-1].split("#")[0][:-5]

    def rel_link(mm):
        e = E.get(slug(mm.group(2)))
        return mm.group(1) + (html.escape(link_label(e), quote=False) if e else mm.group(3)) + mm.group(4)

    def related(mm):
        return re.sub(r'(<a class="cd-link" href="([^"]+)">)(.*?)(</a>)', rel_link, mm.group(0))
    src = re.sub(r"<h2>Related Episodes</h2>.*?</div>", related, src, count=1, flags=re.S)

    def card(mm):
        e = E.get(slug(mm.group(2)))
        if not e:
            return mm.group(0)
        x = describe(e)
        t = x["d"] or (x["paren"] if x["guest"] else "") or x["guest"] or x["tag"] or e["title"]
        who = x["guest"] if x["guest"] and t != x["guest"] else (x["tag"] if t != x["tag"] else "")
        dur = re.search(r"&middot;\s*(.*)$", mm.group(5))
        meta_line = " &middot; ".join(y for y in (html.escape(who, quote=False), dur.group(1) if dur else "") if y)
        return mm.group(1) + mm.group(3) + html.escape(t, quote=False) + mm.group(4) + meta_line + mm.group(6)
    src = re.sub(r'(<a class="ep2-card" href="([^"]+)">.*?)(<span class="ep2-card-t">).*?(</span><span class="ep2-card-m">)(.*?)(</span>)',
                 lambda mm: card(mm), src, flags=re.S)

    def nxt(mm):
        e = E.get(slug(mm.group(2)))
        if not e:
            return mm.group(0)
        x = describe(e)
        return mm.group(1) + html.escape(x["guest"] or x["d"] or e["title"], quote=False) + mm.group(4)
    src = re.sub(r'(<a class="btn-lines v4-next" href="([^"]+)"><span class="v4-next-k">Next</span> )(.*?)(</a>)', nxt, src, count=1)
    return src


def hold_data():
    out = {}
    for rel in TRIPS:
        s = open(os.path.join(V4, rel), encoding="utf-8").read()
        out[rel.split("/")[-1][:-5]] = {"len": trip_length(s), "deps": trip_departures(s)}
    return out


def page(rel, src):
    if rel == "enquire.html":
        src = enquire_hold(src, hold_data())
    if rel in TRIPS:
        src = trip_bar(src)
        src = trip_dates_first(src)
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
