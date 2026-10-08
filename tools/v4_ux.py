#!/usr/bin/env python3
"""
The usability pass on v4 (owner's brief, 7 Oct 2026; docs/ux-report.md).

Everything the pass puts into the v4 pages. It uses only words and facts the
pages already carry, and is idempotent: it runs after every other v4
generator and pass, and a rerun changes nothing.

    python3 tools/v4_ux.py              # every v4 page (never the samples)
    python3 tools/v4_ux.py --check      # say what would change, write nothing

Rebuild order for v4: the generators and passes in docs/v4-report.md, then
python3 tools/v4_phone_media.py (the phone pictures and clips), python3
tools/v4_search.py (the search files), this, python3 tools/v4_min.py and
python3 tools/v2_localize.py --site v4.

Where the rest lives
  src/v4-ux.css        the pass's rules for one kind of page: each "@page"
                       section goes, minified, into those pages only, right
                       after v2.css; "@small" (22) is a list of labels, each
                       page getting the ones it carries.
  src/v2.css           (its end) the few rules every page needs, and those the
                       live audit must not find inside a page.
  src/v4-ux-*.js       the pass's scripts, inlined only where used (the hero
                       clips, the footage's Pause, the newest episode, the
                       enquiry form, the in-page search); the library's
                       search extras ride in library-find.js (tools/v4_search.py).
  <!--v4u-name-->      the marks around what this writes into a page.

What it does, by the brief's numbers: 1, 2, 4, 5, 7 the trip pages (the phone
bar's price, the dates after the route, the enquiry on a departure, every
question shown, Flying Etiquette's band, the bar's price and Hold a place);
6 weight (phone cuts of the heroes, clips and stills, pictures that wait,
every drawing in relative steps); 10 episode labels; 11 the podcast's wall
and the Listening mode button; 14 and 15 the knowledge base's jump rows and
hub; 17 the library's search; 19 the podcast's newest episode; 20 topics;
21 one main per page; 22 small labels; 23 the footage's Pause; 24 Tap on
touch; 26 image sizes; 27 the enquiry form's messages.
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


HOLD_MARK = ("<!--v4u-hold-->", "<!--/v4u-hold-->")
HOLD_HEAD = ("<!--v4u-holding-->", "<!--/v4u-holding-->")


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
    """6c. The home page's four expedition photographs: a phone cut each (tools/v4_phone_media.py), and all four
    wait until the visitor first scrolls or the fly-through comes into view; without script the first one still
    shows (a noscript copy)."""
    m = re.search(r'<div class="v2-fb-stage" aria-hidden="true">(.*?)\n  </div>', src, re.S)
    if not m:
        return src
    stage = m.group(1)
    if "<noscript>" not in stage:
        first = re.search(r"<picture>.*?</picture>", stage, re.S).group(0)
        stage = stage.replace("</picture>", "</picture><noscript>%s</noscript>" % first, 1)

    def shot(mm):
        pic = mm.group(2)
        if PHONE_MEDIA not in pic:
            jpg = re.search(r'(?:data-v4-src|\bsrc)="([^"]+\.jpg)"', pic).group(1)
            phone = "img/hero/home-%s-p" % os.path.basename(jpg)[:-4]
            if not os.path.exists(os.path.join(V4, phone + ".webp")):
                raise SystemExit("v4_ux: run tools/v4_phone_media.py first (%s)" % phone)
            pic = ('<source media="%s" srcset="%s.webp" type="image/webp"><source media="%s" srcset="%s.jpg">'
                   % (PHONE_MEDIA, phone, PHONE_MEDIA, phone)) + pic
        pic = re.sub(r'(<source\b[^>]*?\s)srcset=', r"\1data-v4-srcset=", pic)
        pic = re.sub(r'(<img\b[^>]*?\s)src=', r"\1data-v4-src=", pic)
        return mm.group(1) + pic + mm.group(3)
    parts = re.split(r"(<noscript>.*?</noscript>)", stage, flags=re.S)
    stage = "".join(p if p.startswith("<noscript>") else
                    re.sub(r'(<div class="v2-fb-shot[^"]*"><picture>)(.*?)(</picture>)', shot, p, flags=re.S) for p in parts)
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


def _parts(title):
    return [p.strip() for p in re.split(r"\s+[:|]\s+|:\s+|\s+\|\s*|\s+-\s+", title.strip()) if p.strip()]


def _first_parts():
    seen = {}
    for m in meta().values():
        if not (m.get("guest") or "").strip() or m.get("guest") == "Aninder Singh":
            k = _norm(_parts(m["title"])[0])
            seen[k] = seen.get(k, 0) + 1
    return seen


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


def _wordy(s):
    return bool(s) and " " in s.strip() and "." not in s       # "Mid-Air Collision", not "hochzwei.media"


def link_label(m):
    x = describe(m)
    what = x["d"] or (x["paren"] if _wordy(x["paren"]) else "") or x["tag"] or x["paren"]
    if x["guest"] and what:
        return "%s: %s" % (x["guest"], what)
    return x["guest"] or what or m["title"]


def episode_labels(src):
    """10. Related Episodes and Up next say who and what: the guest and the descriptive part of the title
    (no more "Sky Gods" nine times, or the guest's name twice on one card). The phone bar's Next too."""
    E = meta()

    def slug(href):
        return href.split("/")[-1].split("#")[0][:-5]

    def rel_link(mm):
        e = E.get(slug(mm.group(2)))
        return mm.group(1) + (html.escape(link_label(e), quote=False) if e else mm.group(3)) + mm.group(4)

    def related(mm):
        return re.sub(r'(<a class="cd-link" href="([^"]+)">)(.*?)(</a>)', rel_link, mm.group(0))
    src = re.sub(r"<h2>Related Episodes</h2>.*?</div>", related, src, count=1, flags=re.S)

    def card(mm, twice):
        e = E.get(slug(mm.group(2)))
        if not e:
            return mm.group(0)
        x = describe(e)
        t = x["d"] or (x["paren"] if x["guest"] and _wordy(x["paren"]) else "") or x["guest"] or x["tag"] or e["title"]
        if t in twice and x["guest"] and t != x["guest"]:
            t = "%s: %s" % (x["guest"], t)               # two "Navigating India" in one row: say whose
        who = x["guest"] if x["guest"] and x["guest"] not in t else (x["tag"] if x["tag"] and x["tag"] not in t else "")
        dur = re.search(r"\d+\s*min\b", mm.group(5))
        meta_line = " &middot; ".join(y for y in (html.escape(who, quote=False), dur.group(0) if dur else "") if y)
        return mm.group(1) + mm.group(3) + html.escape(t, quote=False) + mm.group(4) + meta_line + mm.group(6)
    CARD = re.compile(r'(<a class="ep2-card" href="([^"]+)">.*?)(<span class="ep2-card-t">).*?(</span><span class="ep2-card-m">)(.*?)(</span>)', re.S)

    def grid(gm):
        g = gm.group(0)
        firsts = []
        for mm in CARD.finditer(g):
            e = E.get(slug(mm.group(2)))
            if e:
                x = describe(e)
                firsts.append(x["d"] or (x["paren"] if x["guest"] and _wordy(x["paren"]) else "") or x["guest"] or x["tag"] or e["title"])
        twice = {t for t in firsts if firsts.count(t) > 1}
        return CARD.sub(lambda mm: card(mm, twice), g)
    src = re.sub(r'<div class="ep2-next-grid">.*?</div>\s*</section>', grid, src, flags=re.S)

    def nxt(mm):
        e = E.get(slug(mm.group(2)))
        if not e:
            return mm.group(0)
        x = describe(e)
        return mm.group(1) + html.escape(x["guest"] or x["d"] or e["title"], quote=False) + mm.group(4)
    src = re.sub(r'(<a class="btn-lines v4-next" href="([^"]+)"><span class="v4-next-k">Next</span> )(.*?)(</a>)', nxt, src, count=1)
    return src


# ------------------------------------------------------------------------------------------------ 11, 12
LISTEN_BTN = ('<button type="button" class="v4-ls-open"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 15v-3a8 8 0 0 1 16 0v3"/>'
              '<rect x="3" y="14" width="4" height="7" rx="1.2"/><rect x="17" y="14" width="4" height="7" rx="1.2"/></svg>'
              '<span>Listening mode</span></button>')


def episode_listen_button(src):
    """11. The Listening mode button is in the page from the start (it was added by script after the page had
    drawn, and the hero grew under the reader: 35 px at 1440). The script uses it (src/v2-immersive.js part 10);
    without script it is not shown. 12: its aria-controls is set only once the screen it opens exists."""
    if 'class="v4-ls-open"' in src or 'data-v2="ep"' not in src or 'class="cd-line"' not in src:
        return src
    m = re.search(r'<div class="ep2-hero-media">', src)
    if not m or 'class="cd-player' not in src:
        return src
    a, b = element_span(src, m.start(), "div")
    close = b - len("</div>")
    return src[:close] + "  " + LISTEN_BTN + "\n      " + src[close:]


# ------------------------------------------------------------------------------------------------ 14
def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", plain(s).lower()).strip("-")


def kb_jump(src):
    """14. A knowledge base page's own jump row under its opening, as on the trip pages: each idea by its
    kicker (the page's own word for it: Consequence, Capacity, Fear...), then Worth Remembering, FAQ and the
    conversations, in the page's order. The idea sections get ids to land on."""
    ids = set(re.findall(r'\sid="([^"]+)"', src))
    links = []

    def idea(m):
        sec, body = m.group(1), m.group(2)
        k = re.match(r'<div class="l"><span class="num">[^<]*</span><span class="kicker">([^<]+)</span><h2>', m.string[m.end():m.end() + 300])
        if not k:
            return m.group(0)
        ident = re.search(r'\sid="([^"]+)"', sec)
        if not ident:
            base, n = "k-" + _slug(k.group(1)), 2
            new = base
            while new in ids:
                new, n = "%s-%d" % (base, n), n + 1
            ids.add(new)
            sec = sec[:-1] + ' id="%s">' % new
            ident = new
        else:
            ident = ident.group(1)
        links.append((ident, plain(k.group(1))))
        return sec + body
    src = re.sub(r'(<section class="k-sec (?:bg|card)"[^>]*>)(<div class="band">)', idea, src)
    if not links:
        return src
    order = []
    for m in re.finditer(r'<section class="k-sec[^"]*"[^>]*\sid="([^"]+)"', src):
        order.append(m.group(1))
    names = dict(links)
    names.update({"takeaways": "Worth Remembering", "questions": "FAQ"})
    ep = re.search(r'<section class="k-sec[^"]*" id="episodes"><div class="k-head"><h2>([^<]+)</h2>', src)
    if ep:
        names["episodes"] = plain(ep.group(1))
    row = "".join('\n    <a href="#%s">%s</a>' % (i, html.escape(names[i], quote=False)) for i in order if i in names)
    block = ('<div class="dst-jump v4u-jump" role="navigation" aria-label="On this page">\n  <div class="dst-jump-in">%s\n  </div>\n</div>\n'
             % row)
    if '<div class="dst-jump v4u-jump"' in src:
        a = src.index('<div class="dst-jump v4u-jump"')
        a, b = element_span(src, a, "div")
        return src[:a] + block.rstrip("\n") + src[b:]
    h = re.search(r'<header[^>]*class="k-hero[^"]*"', src)
    if not h:
        return src
    a, b = element_span(src, h.start(), "header")
    return src[:b] + "\n" + block + src[b:].lstrip("\n")


# ------------------------------------------------------------------------------------------------ 15
FIND_FORM = ('<form class="v4u-find" role="search" action="sitemap.html" data-v4-find>'
             '<label class="v4u-find-lab" for="v4uFind">Search episodes, the knowledge base and trips</label>'
             '<input id="v4uFind" type="search" name="q" autocomplete="off" placeholder="Search" aria-controls="v4uHits">'
             '<ol class="v4-hits v4u-hits" id="v4uHits" aria-live="polite"></ol></form>\n      ')


def kb_question(href):
    """The question a knowledge base page asks: its own h1."""
    with open(os.path.join(V4, href.split("#")[0]), encoding="utf-8") as fh:
        s = fh.read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    return re.sub(r"\s+", " ", plain(m.group(1))) if m else ""


def kb_hub(src):
    """15. The knowledge base hub: each series says what it is about (its own page's question, under its name),
    and the site search sits at the top. The small type is CSS."""
    def chip(m):
        q = kb_question(m.group(1))
        return ('<a class="clb-topic" href="%s"><span>%s</span><b>%s</b>%s</a>'
                % (m.group(1), m.group(2), m.group(3), ('<span class="v4-q">%s</span>' % html.escape(q, quote=False)) if q else ""))
    src = re.sub(r'<a class="clb-topic" href="([^"]+)"><span>([^<]*)</span><b>([^<]*)</b>(?:<span class="v4-q">[^<]*</span>)?</a>', chip, src)
    if 'class="v4u-find"' not in src:
        src = src.replace('<details class="clb-how">', FIND_FORM + '<details class="clb-how">', 1)

    # the altitude links on the climb: a band 90 units tall round each level's dot (46 px on a phone, where the
    # words alone were an 18 px target); the levels are 100 units apart or more, so the bands never overlap
    def lv(m):
        a = m.group(0)
        if "v4-climb-hit" in a:
            return a
        y = float(re.search(r'<circle class="v4-climb-dot" cx="[^"]+" cy="([0-9.]+)"', a).group(1))
        return a.replace(">", '><rect class="v4-climb-hit" x="0" y="%.1f" width="640" height="90"/>' % (y - 45), 1)
    return re.sub(r'<a class="v4-climb-lv"[^>]*>.*?</a>', lv, src, flags=re.S)


# ------------------------------------------------------------------------------------------------ 17
def library_search(src):
    """17. The library's search under its title (it sat 3.1 phone screens down, below the series), with the
    first results right under it; it also matches topics, chapter titles and summaries (v2-library.js and
    library-find.js, tools/v4_search.py), so its placeholder no longer says "by title or guest"."""
    m = re.search(r'\s*<label class="v2-find">.*?</label>', src, re.S)
    if not m or 'id="qHits"' in src:
        return src
    find = m.group(0).strip().replace('placeholder="Search by title or guest"', 'placeholder="Search episodes"')
    src = src[:m.start()] + src[m.end():]
    block = ('\n    <div class="v4u-libfind" role="search">%s\n      <ol class="v4-hits v4u-hits" id="qHits" aria-live="polite"></ol>\n    </div>'
             % find)
    return re.sub(r'(<header class="kit-hero is-sky v2-lib-hero[^"]*">\s*<div class="kit-hero-copy">.*?<p class="kit-intro">.*?</p>)',
                  lambda mm: mm.group(1) + block, src, count=1, flags=re.S)


WALL_MARK = ("<!--v4u-wall-->", "<!--/v4u-wall-->")
WALL_JS = ("<script>(function(d){var r=d.documentElement,done=0;function show(){if(!done){done=1;r.classList.remove('v4u-wall');}}"
           "r.classList.add('v4u-wall');setTimeout(show,2500);"
           "try{d.fonts.load('600 1em Poppins').then(function(){requestAnimationFrame(function(){requestAnimationFrame(show);});},show);}"
           "catch(e){show();}})(document);</script>")


def podcast_wall(src):
    """11. The podcast's wall of names waits, hidden, for its typeface (it re-wrapped when the face arrived and
    moved most of the opening: a layout shift of 0.55 at 1440); 2.5 s at most. Without script it simply shows."""
    if 'class="kit-hero-media v4-voices"' not in src:
        return src
    return put_block(src, WALL_MARK, WALL_JS, "</head>")


LATEST_MARK = ("<!--v4u-latest-->", "<!--/v4u-latest-->")
LATEST_JS_MARK = ("<!--v4u-latest-js-->", "<!--/v4u-latest-js-->")


def inline_js(name):
    """A source in prototypes/v4/src, minified as tools/v4_min.py does, to inline in the one page that uses it."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import v4_min
    with open(os.path.join(V4, "src", name), encoding="utf-8") as fh:
        return v4_min.js(fh.read()).strip()
PLAY_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path class="v4u-i-play" d="M8 5v14l11-7Z"/>'
            '<path class="v4u-i-pause" d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>')


def latest_episode():
    """The newest episode in the saved archive (episode-meta.json), with its audio (mp3-map.json), its page's
    own title and guest line, its number and length. None when the archive has no audio for it."""
    import json
    m = sorted(meta().values(), key=lambda x: x.get("published") or "", reverse=True)[0]
    with open(os.path.join(ROOT, "mp3-map.json"), encoding="utf-8") as fh:
        audio = (json.load(fh).get(m["slug"]) or {}).get("url")
    rel = "episodes/%s.html" % m["slug"]
    fp = os.path.join(V4, rel)
    if not audio or not os.path.exists(fp):
        return None
    ep = open(fp, encoding="utf-8").read()
    t = re.search(r'<span class="ep2-h1">(.*?)</span>', ep, re.S)
    w = re.search(r'<span class="ep2-with">(.*?)</span>', ep, re.S)
    return {"href": rel, "audio": audio, "title": t.group(1).strip() if t else html.escape(m["title"]),
            "with": w.group(1).strip() if w else "", "no": m.get("epno") or "", "len": m.get("duration_label") or "",
            "date": (m.get("published_label") or "").replace(" ", "&nbsp;")}


def podcast_latest(src):
    """19. The newest episode on screen one, with a play button, from the saved archive written into the page
    (it played only from the live feed, five phone screens down, and not at all when the feed failed). Its
    words are the episode's own: number, length, date, title, guest; the button is the feed's own "Play
    episode". src/v4-ux-latest.js, inlined here, plays it; without script the button is not shown and the title still links."""
    e = latest_episode()
    if not e or 'class="kit-hero v2-pod-hero' not in src:
        return src
    kick = " · ".join(x for x in (e["no"], e["len"], e["date"]) if x)
    block = ('<div class="v4u-latest" data-audio="%s"><button type="button" class="v4u-play" aria-label="Play episode" aria-pressed="false">%s</button>'
             '<p><span class="v4u-latest-k">%s</span> <a href="%s">%s</a>%s</p></div>'
             % (html.escape(e["audio"]), PLAY_SVG, kick, e["href"], e["title"],
                (' <span class="v4u-latest-w">%s</span>' % e["with"]) if e["with"] else ""))
    if LATEST_MARK[0] in src:
        src = put_block(src, LATEST_MARK, block, "")
    else:
        m = re.search(r'(<header class="kit-hero v2-pod-hero[^"]*">.*?<div class="kit-actions">.*?</div>)', src, re.S)
        if not m:
            return src
        src = src[:m.end()] + "\n      " + LATEST_MARK[0] + block + LATEST_MARK[1] + src[m.end():]
    return put_block(src, LATEST_JS_MARK, "<script>%s</script>" % inline_js("v4-ux-latest.js"), "</body>")


# ------------------------------------------------------------------------------------------------ 20
TOPIC_CASE = (("Srs", "SRS"), ("Ccc", "CCC"))


def topic_case(src):
    """20. Two topic names were written by a title-casing step ("Srs", "Ccc"); the site writes them SRS and CCC
    everywhere else (the episodes, their transcripts). The same words, in the site's own case, on every page
    and in the search files; the page title and its structured data stay as the live page has them (the parity gate), until the
    name is corrected at its source, episode-meta.json."""
    keep = r'(<title>.*?</title>|<meta property="og:title"[^>]*>|<meta name="twitter:title"[^>]*>|<script type="application/ld\+json">.*?</script>)'
    parts = re.split(keep, src, flags=re.S)    # the page title stays the live page's (the parity gate)
    for i in range(0, len(parts), 2):
        for a, b in TOPIC_CASE:
            parts[i] = re.sub(r"\b%s\b" % a, b, parts[i])
    return "".join(parts)


TG_FIND = ('<label class="v2-find v4u-tgfind"><span class="v2-sr">Search topics</span>'
           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/>'
           '<path d="M21 21l-4.3-4.3"/></svg><input class="v2-find-input" id="tgFind" type="search" placeholder="Search topics" '
           'autocomplete="off" aria-controls="tgCloud"></label>')
TG_JS_MARK = ("<!--v4u-topics-js-->", "<!--/v4u-topics-js-->")
TG_JS = ("<script>(function(d){var i=d.getElementById('tgFind'),c=d.getElementById('tgCloud'),n=d.getElementById('tgNone');if(!i||!c||!n)return;"
         "var t=[].slice.call(c.querySelectorAll('.tg-tile'));function f(s){return s.toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}"
         "t.forEach(function(a){a.v4f=f((a.getAttribute('href')||'').replace(/^.*\\//,'').replace(/\\.html$/,'')+' '+a.textContent.replace(/\\d+\\s*$/,''));});"
         "i.addEventListener('input',function(){var q=f(i.value),k=0;t.forEach(function(a){var on=!q||a.v4f.indexOf(q)>=0;a.hidden=!on;if(on)k++;});n.hidden=k>0;});"
         "})(document);</script>")


def topic_years():
    """The first and last years among the dated conversations the topic tiles trace (tools/v4_topics.py)."""
    years = []
    for f in os.listdir(os.path.join(V4, "tags")):
        if f.endswith(".html"):
            years += re.findall(r'<li class="tg-ep[^"]*" data-date="(\d{4})-', open(os.path.join(V4, "tags", f), encoding="utf-8").read())
    return (min(years), max(years)) if years else (None, None)


def topics_page(src):
    """20. The topics page: a box that narrows the 50 tiles as one types (they were a long list to scan on a
    phone: 50 rows), "Nothing found" with the library when none matches; and a caption for the traces on the
    tiles, in the words of the chart they shrink (each topic page's "conversations by date"), with its years.
    (Its first wording, "Each topic's conversations by date", had a word the site does not use; the
    independent check at the end of the pass caught it.)
    Without script the box is not shown."""
    if 'class="tg-cloud"' not in src:
        return src
    y0, y1 = topic_years()
    if 'id="tgFind"' not in src:
        cap = ('<p class="tg-spark-cap"><svg viewBox="0 0 40 12" aria-hidden="true" focusable="false"><path d="M1,10 C8,10 10,4 16,6 S26,10 30,3 '
               'S36,8 39,8"/></svg>Conversations by date, %s&nbsp;to&nbsp;%s</p>' % (y0, y1)) if y0 else ""
        src = re.sub(r'(<header class="kit-hero is-sky v2-tg-hero">\s*<div class="kit-hero-copy">.*?<p class="kit-intro">.*?</p>)',
                     lambda m: m.group(1) + "\n    <div class=\"v4u-tgtools\" role=\"search\">" + TG_FIND + "</div>" + cap, src, count=1, flags=re.S)
        src = src.replace('<div class="tg-cloud">', '<div class="tg-cloud" id="tgCloud">', 1)
        src = re.sub(r'(<div class="tg-cloud" id="tgCloud">.*?)(\n\s*</div>)',
                     lambda m: m.group(1) + m.group(2) + '\n<p class="v4u-tg-none" id="tgNone" hidden>Nothing found. <a href="library.html">Library</a></p>',
                     src, count=1, flags=re.S)
    if y0:   # the caption's words, kept current
        src = re.sub(r'(<p class="tg-spark-cap">.*?</svg>)[^<]*(</p>)',
                     lambda m: m.group(1) + "Conversations by date, %s&nbsp;to&nbsp;%s" % (y0, y1) + m.group(2), src, count=1, flags=re.S)
    return put_block(src, TG_JS_MARK, TG_JS, "</body>")


# ------------------------------------------------------------------------------------------------ 6 again
def film_stills(rel, src):
    """6, re-measured at the end. A knowledge base film strip now sits within a phone's first two screens (13:
    the ideas come first), where the browser fetches a lazy picture on arrival; its still was the 1600 x 900
    file (up to 309 KB). The still now waits until the strip is near (as the trip heroes' do), and on an upright
    screen it is the third such a screen shows (img/hero/film-<name>-p.webp, tools/v4_phone_media.py), the same
    framing. The strip is drawn without words and hidden from screen readers; without script it shows no still."""
    def wrap(m):
        img = m.group(2)
        s = re.search(r'\ssrc="([^"]+?)([^/"]+)\.jpg"', img)
        if not s:
            return m.group(0)
        name = s.group(2)
        if not os.path.exists(os.path.join(V4, "img", "hero", "film-%s-p.webp" % name)):
            return m.group(0)
        up = "../" * rel.count("/")
        img = img.replace(' src="', ' data-v4-src="', 1)
        return '%s<picture><source media="%s" data-v4-srcset="%simg/hero/film-%s-p.webp" type="image/webp">%s</picture>' % (
            m.group(1), PHONE_MEDIA, up, name, img)
    out = re.sub(r'(<section class="v4-breather v4-film"[^>]*>\s*<div class="v4-br-media">)(<img\b[^>]*>)', wrap, src)
    if 'class="v4-breather v4-film"' in out and "data-v4-src=" in out:
        out = put_block(out, FILM_MARK, FILM_JS, "</body>")
    return out


FILM_MARK = ("<!--v4u-film-->", "<!--/v4u-film-->")
FILM_JS = ("<script>(function(d,w){var im=[].slice.call(d.querySelectorAll('.v4-film img[data-v4-src]'));"
           "function go(i){var p=i.parentNode;if(p.tagName==='PICTURE')[].forEach.call(p.querySelectorAll('source[data-v4-srcset]'),"
           "function(s){s.srcset=s.getAttribute('data-v4-srcset');});i.src=i.getAttribute('data-v4-src');}"
           "if(!('IntersectionObserver' in w)){im.forEach(go);return;}"
           "var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){o.unobserve(e.target);go(e.target);}});},"
           "{rootMargin:'400px 0px'});im.forEach(function(i){o.observe(i);});})(document,window);</script>")


BREATHER_MARK = ("<!--v4u-breather-->", "<!--/v4u-breather-->")
BREATHER_JS = ("<script>(function(v){var m=location.pathname.match(/^(.*\\/prototypes\\/v\\d+\\/)/);"
               "if(v&&innerWidth/Math.max(1,innerHeight)<=2/3)v.setAttribute('data-loop',(m?m[1]:'/assets/v4/')+'img/clips/hero-p');})"
               "(document.querySelector('.v4-breather video[data-loop$=\"video/hero\"]'));</script>")


def podcast_breather(src):
    """6, re-measured at the end. The podcast's full-screen footage between the opening and the host was the
    16:9 720p clip on a phone too (1.1 MB, fetched on arrival as it comes into reach); on an upright screen it
    is now the clip cut for one (img/clips/hero-p-720, 0.4 MB, the same footage), set before script.js loads it."""
    m = re.search(r'<section class="v4-breather">.*?</section>', src, re.S)
    if not m or 'video/hero"' not in m.group(0):
        return src
    if BREATHER_MARK[0] in src:
        return put_block(src, BREATHER_MARK, BREATHER_JS, "")
    return src[:m.end()] + BREATHER_MARK[0] + BREATHER_JS + BREATHER_MARK[1] + src[m.end():]


# ------------------------------------------------------------------------- the pass's own CSS and scripts, by page
UXCSS_MARK = ("<!--v4u-css-->", "<!--/v4u-css-->")
FOOT_MARK = ("<!--v4u-footage-->", "<!--/v4u-footage-->")
FIND_MARK = ("<!--v4u-find-->", "<!--/v4u-find-->")
_UXCSS = None


def ux_groups(rel, src):
    """Which sections of src/v4-ux.css a page needs."""
    g = []
    if rel in TRIPS:
        g.append("trip")
    if 'id="enqForm"' in src:
        g.append("enquire")
    if rel.startswith("episodes/") and 'class="cd-wrap' in src:
        g.append("episode")
    if 'data-v2="kb"' in src:
        g.append("kb")
    for r, n in (("knowledge-base.html", "hub"), ("library.html", "library"), ("podcast.html", "podcast"), ("tags.html", "topics"),
                 ("sitemap.html", "sitemap")):
        if rel == r:
            g.append(n)
    if "v4u-touch" in src:
        g.append("touch")
    return g


JS_MADE = {"sky-g": "sitemap-sky.js", "ep-au-cur": "episode-audio.js", "ep-au-dur": "episode-audio.js"}


def small_rule(rel, src, small):
    """22: of the labels that take the micro size on a phone, the ones this page carries: in its own HTML, or
    made by a script it loads (JS_MADE)."""
    own = re.sub(r"%s.*?%s" % (re.escape(UXCSS_MARK[0]), re.escape(UXCSS_MARK[1])), "", src, flags=re.S)
    loads = set(os.path.basename(u) for u in re.findall(r'<script\b[^>]*\ssrc="([^"?]+)', src))

    def has(c):
        return re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(c), own) or JS_MADE.get(c) in loads
    keep = [sel for sel in small if all(has(c) for c in re.findall(r"\.([\w-]+)", sel) if len(c) > 2)]
    # :is() weighs as its heaviest selector, and the rule must weigh what it did as one list for every page
    top = max(small, key=lambda x: (len(re.findall(r"[.#\[:]", x)), len(re.findall(r"(?:^|[\s>+~])[a-z]", x))))
    if keep and top not in keep:
        keep.append(top)
    return "@media (max-width:760px){html body :is(%s){font-size:var(--fs-micro)}}" % ",".join(keep) if keep else ""


def ux_css(rel, src):
    """6, re-measured at the end. The pass's rules for one kind of page (src/v4-ux.css) go into those pages
    alone, minified, right after v2.css, so they cascade exactly as the end of v2.css did; every other page
    no longer carries them (they had made every page 12 to 14 KB heavier)."""
    global _UXCSS
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import v4_min
    if _UXCSS is None:
        text = open(os.path.join(V4, "src", "v4-ux.css"), encoding="utf-8").read()
        _UXCSS = {m.group(1): m.group(2) for m in re.finditer(r"/\* @page (\w+) \*/(.*?)(?=/\* @(?:page \w+|small) \*/|\Z)", text, re.S)}
        sm = re.search(r"/\* @small \*/(.*)\Z", text, re.S)
        _UXCSS[" small"] = [ln.strip() for ln in re.sub(r"/\*.*?\*/", "", sm.group(1), flags=re.S).splitlines() if ln.strip()] if sm else []
    css = "".join(v4_min.css(_UXCSS[g]).strip() for g in ux_groups(rel, src)) + small_rule(rel, src, _UXCSS[" small"])
    link = re.search(r'<link rel="stylesheet" href="[^"]*v2\.css(?:\?v=[0-9a-f]+)?">', src)
    if UXCSS_MARK[0] in src:
        if not css:
            i = src.index(UXCSS_MARK[0])
            return src[:i] + src[src.index(UXCSS_MARK[1], i) + len(UXCSS_MARK[1]):]
        return put_block(src, UXCSS_MARK, "<style>%s</style>" % css, "")
    if not css or not link:
        return src
    return src[:link.end()] + UXCSS_MARK[0] + "<style>%s</style>" % css + UXCSS_MARK[1] + src[link.end():]


def ux_scripts(rel, src):
    """23 and 15: the footage's Pause only on the pages with footage, the in-page search only where there is one."""
    if re.search(r"<video\b", src):
        src = put_block(src, FOOT_MARK, "<script>%s</script>" % inline_js("v4-ux-footage.js"), "</body>")
    if "data-v4-find" in src:
        src = put_block(src, FIND_MARK, "<script>%s</script>" % inline_js("v4-ux-find.js"), "</body>")
    return src


# ------------------------------------------------------------- 6 at the end: every drawing in relative steps
from decimal import Decimal as _D   # noqa: E402

_NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"
_ARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "Z": 0}


def _fmt(x):
    s = format(x.normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    if s.startswith("0."):
        s = s[1:]
    elif s.startswith("-0."):
        s = "-" + s[2:]
    return s


def _join(nums):
    out = ""
    for n in nums:
        t = _fmt(n)
        out += t if (not out or t.startswith("-") or out[-1].isalpha()) else " " + t
    return out


def _tokens(d):
    for m in re.finditer(r"([MmLlHhVvCcSsQqTtZz])|(%s)" % _NUM, d):
        yield m.group(1) or _D(m.group(2))


def path_relative(d):
    """A path's data with every segment relative (each subpath's M absolute): the same points exactly, worked
    in decimal, not in floating point. None when it holds arcs or anything else unexpected (left as it is)."""
    if re.search(r"[Aa]", d) or re.sub(r"([MmLlHhVvCcSsQqTtZz])|(%s)|[\s,]" % _NUM, "", d):
        return None
    toks = list(_tokens(d))
    out, i, cmd, cx, cy, sx, sy, last = [], 0, None, _D(0), _D(0), _D(0), _D(0), None
    while i < len(toks):
        t = toks[i]
        if isinstance(t, str):
            cmd = t
            i += 1
            if cmd in "Zz":
                if last != "z":
                    out.append("z")
                cx, cy, last = sx, sy, "z"
                continue
        elif cmd is None:
            return None
        up = cmd.upper()
        n = _ARGS[up]
        a = toks[i:i + n]
        if len(a) < n or any(isinstance(x, str) for x in a):
            return None
        i += n
        rel = cmd.islower()
        if up == "M":
            x, y = (cx + a[0], cy + a[1]) if rel else (a[0], a[1])
            out.append("M" + _join([x, y]))
            cx, cy, sx, sy, last = x, y, x, y, "M"
            cmd = "l" if rel else "L"          # what follows a moveto is a lineto
            continue
        if up == "H":
            x = cx + a[0] if rel else a[0]
            seg, letter = [x - cx], "h"
            cx = x
        elif up == "V":
            y = cy + a[0] if rel else a[0]
            seg, letter = [y - cy], "v"
            cy = y
        else:
            pts = []
            for k in range(0, n, 2):
                px, py = (cx + a[k], cy + a[k + 1]) if rel else (a[k], a[k + 1])
                pts += [px - cx, py - cy]
            seg, letter = pts, up.lower()
            cx, cy = cx + pts[-2], cy + pts[-1]
        if last == letter:
            body = _join(seg)
            out.append(body if body.startswith("-") else " " + body)
        else:
            out.append(letter + _join(seg))
        last = letter
    return "".join(out)


def poly_path(tag):
    """A <polyline> or <polygon> as the <path> it draws (the same points, relative), its other attributes kept."""
    m = re.search(r'\spoints="([^"]*)"', tag)
    if not m:
        return None
    nums = [_D(x) for x in re.findall(_NUM, m.group(1))]
    if len(nums) < 4 or len(nums) % 2:
        return None
    closed = tag.startswith("<polygon")
    cx, cy, seg = nums[0], nums[1], []
    for k in range(2, len(nums), 2):
        seg += [nums[k] - cx, nums[k + 1] - cy]
        cx, cy = nums[k], nums[k + 1]
    d = "M" + _join(nums[:2]) + "l" + _join(seg) + ("z" if closed else "")
    return "<path" + tag[len("polygon" if closed else "polyline") + 1:m.start()] + ' d="%s"' % d + tag[m.end():]


def drawings_relative(src):
    """6, re-measured at the end. Every drawing in the page (the knowledge base's, the episodes' globes and
    series marks, the topics' traces) spelt in relative steps, polylines as the paths they draw: the same
    points exactly, each check in decimal, and a third lighter (the Flight Mechanics page 150 KB, 60 KB as
    sent). Only where it is shorter; arcs left as they are; nothing inside scripts."""
    def svg(m):
        t = re.sub(r"<poly(?:line|gon)\b[^>]*>", lambda p: (lambda r: r if r and len(r) < len(p.group(0)) else p.group(0))(poly_path(p.group(0))), m.group(0))
        return re.sub(r'(<path\b[^>]*?\sd=")([^"]*)"',
                      lambda p: (lambda r: p.group(1) + r + '"' if r is not None and len(r) < len(p.group(2)) else p.group(0))(path_relative(p.group(2))), t)
    parts = re.split(r"(<script\b.*?</script>|<template\b.*?</template>)", src, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"<svg\b.*?</svg>", svg, parts[i], flags=re.S)
    return "".join(parts)


def kb_tile_art(rel, src):
    """6, re-measured at the end. A knowledge base tile with the episode's own artwork showed the 1280 x 720
    file (50 KB) at 120 px wide on a phone; there it gets the 400 px copy (img/art, tools/v4_phone_media.py)."""
    up = "../" * rel.count("/")

    def add(m):
        name = m.group(2)
        if not os.path.exists(os.path.join(V4, "img", "art", name + "-s.webp")):
            return m.group(0)
        return '%s<source media="(max-width: 760px)" srcset="%simg/art/%s-s.webp" type="image/webp">%s' % (
            m.group(1), up, name, m.group(0)[len(m.group(1)):])
    return re.sub(r'(<span class="ep-th"><picture>)<source srcset="[^"]*/assets/podcast/artwork/([^"/]+)\.webp"', add, src)


def about_still(src):
    """6, re-measured at the end. The About opening's still on an upright phone: the window of it the phone's
    box shows (img/hero/about-alps-11-still-p.webp, tools/v4_phone_media.py), 36 KB instead of 92 KB."""
    if "about-alps-11-still-p.webp" in src or not os.path.exists(os.path.join(V4, "img", "hero", "about-alps-11-still-p.webp")):
        return src
    return src.replace('<picture><source srcset="img/alps-11-still.webp" type="image/webp">',
                       '<picture><source media="%s" srcset="img/hero/about-alps-11-still-p.webp" type="image/webp">'
                       '<source srcset="img/alps-11-still.webp" type="image/webp">' % PHONE_MEDIA, 1)


ART_MARK = ("<!--v4u-art-->", "<!--/v4u-art-->")
ART_JS = ("<script>(function(d,w){var m=location.pathname.match(/^(.*\\/prototypes\\/v\\d+\\/)/),B=m?m[1]:'/assets/v4/',"
          "s=[].slice.call(d.querySelectorAll('[data-v4-art]'));function go(e){e.style.setProperty('--art',\"url('\"+B+e.getAttribute('data-v4-art')+\"')\");}"
          "if(!('IntersectionObserver' in w)){s.forEach(go);return;}var o=new IntersectionObserver(function(es){es.forEach(function(e){"
          "if(e.isIntersecting){o.unobserve(e.target);go(e.target);}});},{rootMargin:'600px 0px'});s.forEach(function(e){o.observe(e);});})(document,window);</script>")


def hub_art(src):
    """6, re-measured at the end. The knowledge base hub's four drawings behind its altitudes (img/kb, 173 KB,
    the meteorology one 132 KB) were fetched on arrival though the first is three screens down; each now
    arrives as its altitude comes near. Without script the altitudes show without their faint drawing."""
    out = re.sub(r'(<section class="clb-station"[^>]*?) style="(--i:\d+);--art:url\(\'(img/kb/[^\']+)\'\)"',
                 r'\1 style="\2" data-v4-art="\3"', src)
    if "data-v4-art=" in out:
        out = put_block(out, ART_MARK, ART_JS, "</body>")
    return out


def library_words(src):
    """6, re-measured at the end. Each library card's search words (data-f) carried its title twice; once is
    enough to match it (5.6 KB of the page)."""
    def one(m):
        w = m.group(1).split(" ")
        for size in range(len(w) // 2, 2, -1):
            for i in range(0, len(w) - 2 * size + 1):
                if w[i:i + size] == w[i + size:i + 2 * size]:
                    return ' data-f="%s"' % " ".join(w[:i + size] + w[i + 2 * size:])
        return m.group(0)
    return re.sub(r' data-f="([^"]*)"', one, src)


# ------------------------------------------------------------------------------------------------ 24
TOUCH = (("Drag to rotate. Click a pin to see the episode.", "Drag to rotate. Tap a pin to see the episode."),
         ("Click a star to find its constellation. Drag to look around.", "Tap a star to find its constellation. Drag to look around."))


def touch_words(src):
    """24. The helper lines under the globe and the night sky said "Click" on a phone too. On a touch screen
    they say "Tap", the site's own word for it ("Tap the centre to come inside", "Tap anywhere to take off
    again"); with a mouse they read as before. The headings ("Click A Pin, Hear The Story") are not touched."""
    if "v4u-touch" in src:
        return src
    for a, b in TOUCH:
        src = src.replace(">%s<" % a, '><span class="v4u-ptr">%s</span><span class="v4u-touch">%s</span><' % (a, b))
    return src


# ------------------------------------------------------------------------------------------------ 26
YT_SIZE = {"maxresdefault": (1280, 720), "sddefault": (640, 480), "hqdefault": (480, 360), "mqdefault": (320, 180), "default": (120, 90)}
_SIZES = {}


def _size(path):
    if path not in _SIZES:
        try:
            from PIL import Image
            with Image.open(path) as im:
                _SIZES[path] = im.size
        except Exception:      # noqa: BLE001 - not an image Pillow reads (an SVG): left as it is
            _SIZES[path] = None
    return _SIZES[path]


def image_sizes(rel, src):
    """26. Width and height on every image in a page's HTML, so its room is kept while it loads: the file's own
    size for the site's images, YouTube's fixed sizes for its thumbnails (maxres 1280 by 720, mq 320 by 180...).
    The attributes only give the shape; the stylesheet still sets the size shown."""
    here = os.path.dirname(os.path.join(V4, rel))

    def fix(m):
        tag = m.group(0)
        if re.search(r"\swidth=", tag) and re.search(r"\sheight=", tag):
            return tag
        s = re.search(r'\ssrc="([^"]+)"', tag) or re.search(r'\sdata-v4-src="([^"]+)"', tag)   # or the picture that waits (6)
        if not s:
            return tag
        u = html.unescape(s.group(1)).split("?")[0]
        wh = None
        y = re.search(r"ytimg\.com/vi(?:_webp)?/[^/]+/(\w+)\.(?:jpg|webp)$", u)
        if y:
            wh = YT_SIZE.get(y.group(1))
        elif not re.match(r"^(?:[a-z]+:|//)", u):
            wh = _size(os.path.normpath(os.path.join(here, u)))
        if not wh:
            return tag
        w0, h0 = re.search(r'\swidth="(\d+)"', tag), re.search(r'\sheight="(\d+)"', tag)
        if w0:       # one of the two given: keep it, and the other by the file's shape
            wh = (int(w0.group(1)), round(int(w0.group(1)) * wh[1] / wh[0]))
        elif h0:
            wh = (round(int(h0.group(1)) * wh[0] / wh[1]), int(h0.group(1)))
        tag = re.sub(r'\s(?:width|height)="[^"]*"', "", tag)
        return tag[:4] + ' width="%d" height="%d"' % wh + tag[4:]
    parts = re.split(r"(<script\b.*?</script>)", src, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"<img\b[^>]*>", fix, parts[i])
        # the globe's card: its picture is a YouTube still put in by globe.js, 16 by 9 like every one of them
        parts[i] = parts[i].replace('<div class="mp-th"><img alt="" loading="lazy">', '<div class="mp-th"><img width="1280" height="720" alt="" loading="lazy">')
    return "".join(parts)


# ------------------------------------------------------------------------------------------------ 27
FORM_JS_MARK = ("<!--v4u-form-js-->", "<!--/v4u-form-js-->")


def enquire_messages(src):
    """27. The enquiry form says under each field what it still needs, and brings the first into view
    (src/v4-ux-form.js, inlined here only)."""
    if 'id="enqForm"' not in src:
        return src
    return put_block(src, FORM_JS_MARK, "<script>%s</script>" % inline_js("v4-ux-form.js"), "</body>")


# ------------------------------------------------------------------------------------------------ 21
def _masked(src):
    """src with script bodies and comments blanked (same length), so tags are counted only where they are tags."""
    return re.sub(r"<script\b.*?</script>|<!--.*?-->", lambda m: " " * len(m.group(0)), src, flags=re.S)


def _close(src, start, tag):
    """End offset of the </tag> that closes the <tag> opening at start (scripts and comments ignored)."""
    depth = 0
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tag, _masked(src)[start:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return start + t.start()
    return None


MAIN_OPEN = '<main id="v4-main">'   # the skip link's script makes it focusable (tabindex -1) as it adds the link


def main_landmark(rel, src):
    """21. One main landmark on every page, and it is where the skip link goes (most pages had none: axe
    landmark-one-main failed on 33 of 60 views; the skip link landed on a header outside any main).
    A page with no main: everything between the header and the end of .page-wrap goes in one (the header
    and the footer stay outside). An episode: its main was only the centre column, after the title and the
    player; the whole episode (.cd-wrap) becomes the main and the column a div, so the classes, and every
    rule that reads them, are unchanged. The 404 and the flight options already have one."""
    if 'id="v4-main"' in src:
        return src
    m = re.search(r'<div class="cd-wrap[^"]*"', src)
    if m and src.count('<main class="cd-center">') == 1:
        end = _close(src, m.start(), "div")
        if end is None:
            return src
        src = src[:m.start()] + "<main" + src[m.start() + 4:end] + "</main>" + src[end + 6:]
        src = src.replace('<main class="cd-wrap', '<main id="v4-main" class="cd-wrap', 1)
        i = src.index('<main class="cd-center">')
        j = _close(src, i, "main")
        return src[:i] + '<div class="cd-center">' + src[i + len('<main class="cd-center">'):j] + "</div>" + src[j + 7:]
    if "<main" in src:
        return src
    a = src.find('<div class="nav-chevron"></div>')
    b = src.find("</div><!-- /.page-wrap -->")
    if a < 0 or b < a:
        return src
    a += len('<div class="nav-chevron"></div>')
    return src[:a] + "\n" + MAIN_OPEN + src[a:b] + "</main>\n" + src[b:]


MEDIA_MARK = ("<!--v4u-media-->", "<!--/v4u-media-->")


def media_script(src):
    """6/23. The phone clips, the hero clip by the width it fills, and the pictures that wait: a short script
    inlined in the head (it must run before script.js reads the clips), from src/v4-ux-media.js."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import v4_min
    with open(os.path.join(V4, "src", "v4-ux-media.js"), encoding="utf-8") as fh:
        js = v4_min.js(fh.read()).strip()
    return put_block(src, MEDIA_MARK, "<script>%s</script>" % js, "</head>")


def hold_data():
    out = {}
    for rel in TRIPS:
        s = open(os.path.join(V4, rel), encoding="utf-8").read()
        out[rel.split("/")[-1][:-5]] = {"len": trip_length(s), "deps": trip_departures(s)}
    return out


def migrate(src):
    """Pages built by earlier runs: the pass's marks in their short form, the main without its tabindex
    (6 at the end: a few dozen bytes on every page)."""
    src = re.sub(r"<!-- (/?)(v4u-[\w-]+)(?:[:,][^>]*?)? -->", r"<!--\1\2-->", src)
    return src.replace(' id="v4-main" tabindex="-1"', ' id="v4-main"')


def page(rel, src):
    src = migrate(src)
    src = topic_case(src)
    src = image_sizes(rel, src)
    if rel in ("index.html", "podcast.html", "sitemap.html"):
        src = touch_words(src)
    if rel == "enquire.html":
        src = enquire_messages(src)
    if rel == "tags.html":
        src = topics_page(src)
    if rel == "enquire.html":
        src = enquire_hold(src, hold_data())
    if rel == "index.html":
        src = home_flyby_weight(src)
        src = media_script(src)
    if rel == "podcast.html":
        src = podcast_wall(src)
        src = podcast_latest(src)
        src = podcast_breather(src)
    if rel.startswith("episodes/"):
        src = episode_labels(src)
        src = episode_listen_button(src)
    if rel.startswith("knowledge-base/"):
        src = kb_jump(src)
        src = film_stills(rel, src)
        src = kb_tile_art(rel, src)
    if rel == "knowledge-base.html":
        src = kb_hub(src)
    if rel == "library.html":
        src = library_search(src)
        src = library_words(src)
    if rel == "about.html":
        src = about_still(src)
    if rel == "knowledge-base.html":
        src = hub_art(src)
    if rel in TRIPS:
        src = trip_bar(src)
        src = trip_dates_first(src)
        src = trip_questions_shown(src)
        src = trip_etiquette_band(src)
        src = trip_hero_weight(rel, src)
        src = gallery_lazy(src)
        src = trip_subnav(src)
        src = media_script(src)
    src = ux_scripts(rel, src)
    src = ux_css(rel, src)
    src = drawings_relative(src)
    return main_landmark(rel, src)


def main(args):
    check = "--check" in args
    rels = [a for a in args if not a.startswith("--")] or sorted(
        os.path.relpath(os.path.join(d, f), V4).replace(os.sep, "/")
        for d, _, fs in os.walk(V4) for f in fs if f.endswith(".html") and "/src/" not in os.path.join(d, f)
        and "/samples" not in d)                                 # the samples are another chat's: never touched
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
