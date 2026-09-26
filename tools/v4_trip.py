#!/usr/bin/env python3
"""
The v4 trip pages: India and Kenya in the fly-through style.

Reads the v2 page (prototypes/v2/destinations/<trip>.html, never written) and
writes prototypes/v4/destinations/<trip>.html:

  first read   the hero, the facts, a trust strip, the fly-through (one screen
               per idea, the photograph behind it), the routes, the pictures,
               the departures with "Hold a place", who guides, from the show,
               the questions, the call. About 800 words.
  folded       everything else, word for word, in <details>: the long
               paragraphs, the travel essentials, what the trip is like, the
               packing list, the etiquette. Search and answer engines read it;
               a link to an anchor inside a fold opens the fold.

Kept exactly: dates, prices (India in GBP, Kenya in US$), places, the
departures, the enquiry links, the structured data, every anchor other pages
link to (#dates, #route, and every section id).

    python3 tools/v4_trip.py            # india and kenya
    python3 tools/v4_trip.py india
    then: python3 tools/v2_localize.py --site v4
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "prototypes", "v2", "destinations")
OUT = os.path.join(ROOT, "prototypes", "v4", "destinations")
CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"

# The trust strip: facts from the booking terms and the participant agreement,
# in their words (docs/v4-plan.md decision 10).
TRUST = [
    ("Registered in Norway", "Organisasjonsnummer 937116934", "../terms.html"),
    ("Package travel rights", "Under Norwegian and EU law", "../terms.html"),
    ("Refunds within 14 days", "Where a refund is due", "../terms.html"),
    ("Not a waiver", "Of our responsibility to you", "../participant-agreement.html"),
]


def trust_strip():
    items = "".join('<li><a href="%s"><b>%s</b><span>%s</span></a></li>' % (h, a, b) for a, b, h in TRUST)
    return ('\n<aside class="v4t-trust" aria-label="Booking with us">\n  <ul>%s</ul>\n</aside>\n' % items)


def fold(inner, summary, cls="v4-fold", ident=None, open_=False):
    return '<details class="%s"%s%s><summary>%s</summary>%s</details>' % (
        cls, ' id="%s"' % ident if ident else "", " open" if open_ else "", summary, inner)


def cut(src, start, end, inclusive=True):
    """(before, block, after) around the first block from start to end."""
    i = src.index(start)
    j = src.index(end, i) + (len(end) if inclusive else 0)
    return src[:i], src[i:j], src[j:]


def section(src, ident):
    m = re.search(r'<section\b[^>]*\bid="%s"[^>]*>.*?</section>' % ident, src, re.S)
    if not m:
        raise SystemExit("no section #" + ident)
    return m


def head_fold(sec_html, sec_id, extra_cls=""):
    """Turn a whole section into a titled fold: its kicker and <h2> become the
    summary, the rest (every word) the body. The section keeps its id."""
    m = re.match(r'(<section\b)([^>]*)>(.*)</section>$', sec_html, re.S)
    attrs, body = m.group(2), m.group(3)
    h = re.search(r'<div class="dst-head[^"]*">\s*(<span class="kicker">.*?</span>)\s*(<h2\b.*?</h2>)(.*?)</div>', body, re.S)
    if h:
        summary = h.group(1) + h.group(2)
        rest = h.group(3)
        body = body[:h.start()] + ('<div class="dst-head">%s</div>' % rest if rest.strip() else "") + body[h.end():]
    else:
        h = re.search(r'(<span class="kicker">[^<]*</span>)\s*(<h2\b.*?</h2>)', body, re.S)
        summary = h.group(1) + h.group(2)
        body = body[:h.start()] + body[h.end():]
    attrs = re.sub(r'\sclass="([^"]*)"', lambda c: ' class="%s v4t-foldsec%s"' % (c.group(1), (" " + extra_cls) if extra_cls else ""), attrs)
    if "class=" not in attrs:
        attrs += ' class="v4t-foldsec"'
    return '%s%s>%s</section>' % (m.group(1), attrs, fold(body, '<span class="v4t-fs-t">%s</span><span class="v4t-fs-mark" aria-hidden="true"></span>' % summary, "v4t-fs"))


def india():
    src = open(os.path.join(SRC, "india.html"), encoding="utf-8").read()

    # ---- hero: the facts in the hero, "Hold a place" first -----------------------
    src = src.replace(
        '<a href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener" class="btn-solid" data-hover><span>Book a Call</span></a>\n'
        '      <a href="#practical" class="listen-btn" data-hover><span>See the trip</span></a>',
        '<a href="#dates" class="btn-solid" data-hover><span>Hold a place</span></a>\n'
        '      <a href="%s" target="_blank" rel="noopener" class="btn-lines" data-hover>Book a Call</a>' % CALL, 1)
    src = src.replace('<a class="khero-cue" href="#practical">', '<a class="khero-cue" href="#overview">', 1)
    # the section jump bar: the first-read sections, then the folds
    src = re.sub(r'<div class="dst-jump">.*?</div>\s*</div>', '''<div class="dst-jump">
  <div class="dst-jump-in">
    <a href="#overview">Overview</a>
    <a href="#route">Routes</a>
    <a href="#gallery">Gallery</a>
    <a href="#dates">Dates</a>
    <a href="#guides">Guides</a>
    <a href="#faq">FAQ</a>
    <a href="#reality">Before You Book</a>
    <a href="#enquire" class="last">Enquire</a>
  </div>
</div>''', src, count=1, flags=re.S)

    # ---- the facts row, then the trust strip ------------------------------------
    b, spec, a = cut(src, '<section class="dst-spec">', '</section>')
    src = b + spec.replace('<section class="dst-spec">', '<section class="dst-spec v4t-spec">', 1) + trust_strip() + a

    # ---- pull the sections out, to put them back in the new order ----------------
    practical = section(src, "practical").group(0)
    overview = section(src, "overview").group(0)
    route = section(src, "route").group(0)
    gallery = section(src, "gallery").group(0)
    dates = section(src, "dates").group(0)
    reality = section(src, "reality").group(0)
    faq = section(src, "faq").group(0)
    packing = section(src, "packing").group(0)
    ground = section(src, "ground").group(0)
    hear = re.search(r'<section class="dst-sec">\s*<div class="dst-head">\s*<span class="kicker">Before You Come</span>.*?</section>', src, re.S).group(0)
    shell_start = src.index('<div class="dst-shell">')
    shell_end = src.index('<section class="cta-band" id="enquire">')
    before, after = src[:shell_start], src[shell_end:]

    # ---- the fly-through: five screens, the photograph behind -----------------------
    ov = overview
    lede = re.search(r'\s*<p class="dst-lede">.*?</p>', ov, re.S).group(0)
    ov = ov.replace(lede, "", 1)
    kair = re.search(r'\s*<div class="kair">.*?</div>\s*</div>\s*</div>\s*(?=<div class="kov-quiet">)', ov, re.S).group(0)
    quiet = re.search(r'\s*<div class="kov-quiet">.*?</div>\s*</div>\s*(?=<div class="kov-close">)', ov, re.S).group(0)
    close = re.search(r'\s*<div class="kov-close">.*?</div>\s*</div>', ov, re.S).group(0)
    for x in (kair, quiet, close):
        ov = ov.replace(x, "", 1)
    # two more screens: cloudbase and the season, from the instruments' own figures
    slides_add = (
        '<div class="kfly-slide"><picture><source srcset="../../../assets/destinations/india/gallery/ridge-cumulus.webp" type="image/webp">'
        '<img src="../../../assets/destinations/india/gallery/ridge-cumulus.jpg" width="1400" height="933" loading="lazy" draggable="false" '
        'alt="Cumulus building over the ridge"></picture></div>'
        '<div class="kfly-slide"><picture><source srcset="../../../assets/destinations/india/gallery/sky-of-wings.webp" type="image/webp">'
        '<img src="../../../assets/destinations/india/gallery/sky-of-wings.jpg" width="1400" height="933" loading="lazy" draggable="false" '
        'alt="A sky full of wings above the range"></picture></div>')
    ov = ov.replace('<div class="kfly-scrim" aria-hidden="true"></div>', slides_add + '\n      <div class="kfly-scrim" aria-hidden="true"></div>', 1)
    ov = ov.replace('<div class="kfly-marks" aria-hidden="true"><i class="is-on"></i><i></i><i></i></div>',
                    '<div class="kfly-marks" aria-hidden="true"><i class="is-on"></i><i></i><i></i><i></i><i></i></div>', 1)
    steps_add = '''
      <div class="kfly-step">
        <div class="kfly-copy">
          <span class="kfly-n">04 &middot; Cloudbase</span>
          <p class="kfly-big">3 to 3.6 km on the front range,</p>
          <dl class="v4t-read"><div><dt>Launch</dt><dd>2.4 km</dd></div><div><dt>Front range cloudbase</dt><dd>3-3.6 km</dd></div><div><dt>Deep in the back, mid November</dt><dd>5.8 km</dd></div></dl>
        </div>
      </div>
      <div class="kfly-step">
        <div class="kfly-copy">
          <span class="kfly-n">05 &middot; The season</span>
          <p class="kfly-big">October to November.</p>
          <dl class="v4t-read"><div><dt>Peak season</dt><dd>Oct to Nov</dd></div><div><dt>Guiding</dt><dd>1 guide to 3 pilots</dd></div></dl>
        </div>
      </div>
    </div>
  </div>'''
    ov = re.sub(r'(<p class="kfly-tail">.*?</p>\s*</div>\s*</div>)\s*</div>\s*</div>', lambda m: m.group(1) + steps_add, ov, count=1, flags=re.S)
    more = fold('<div class="v4t-more-in">' + lede + kair + quiet + close + "</div>",
                "The whole overview: cloudbase, season, retrieves, traffic", "v4-fold v4t-more")
    ov = ov.replace("\n</section>", "\n  " + more + "\n</section>")
    ov = ov.replace('class="dst-sec is-loud kov"', 'class="dst-sec is-loud kov v4t-fly"', 1)

    # ---- routes: the drawing and the three lines; each route's paragraph folds -------
    route = re.sub(r'(<span class="iroute-km">.*?</span>)\s*(<p>.*?</p>)',
                   lambda m: m.group(1) + "\n      " + fold(m.group(2), "More", "v4-fold v4t-rfold"), route, flags=re.S)

    # ---- departures: "Hold a place" opens the enquiry with that departure filled in -----
    def hold(m):
        when = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        q = "enquire.html?trip=india&amp;when=" + when.replace(" ", "+")
        return m.group(0)
    def card(m):
        c = m.group(0)
        when = re.sub(r"<[^>]+>", "", re.search(r'<p class="kdates-when">(.*?)</p>', c, re.S).group(1)).strip()
        href = "../enquire.html?trip=india&amp;when=" + re.sub(r"\s+", "+", when)
        return re.sub(r'<a href="https://calendar\.app\.google/[^"]*" target="_blank" rel="noopener" class="btn-solid is-outline" data-hover><span>Book a Call</span></a>',
                      '<a href="%s" class="btn-solid" data-hover><span>Hold a place</span></a>' % href, c, count=1)
    dates = re.sub(r'<article class="kdates-card">.*?</article>', card, dates, flags=re.S)
    dates = dates.replace('<p class="kdates-terms">', '<p class="kdates-terms"><span class="v4t-hold-note">Hold a place sends an enquiry for that departure.</span> ', 1)

    # ---- who guides: out of "what it is like", into the first read -----------------
    guides = re.search(r'\s*<div class="kguides" aria-labelledby="guides-h">.*?<p class="kguides-note">.*?</p>\s*</div>', reality, re.S).group(0)
    reality = reality.replace(guides, "", 1)
    g = guides.strip()
    g = re.sub(r'(<span class="kguide-role">.*?</span>)\s*(<p>.*?</p>)', lambda m: m.group(1) + "\n        " + fold(m.group(2), "About", "v4-fold v4t-gfold"), g, flags=re.S)
    guides_sec = ('<section class="dst-sec v4t-guides" id="guides">\n  ' + g +
                  '\n  <div class="v4t-proof"><span class="kicker">From past pilots</span>'
                  '<p><i class="v2-tbd">[to supply]</i></p></div>\n</section>')

    # ---- what it is like: the head and the one line stay; the rest folds -------------
    rm = re.match(r'(<section\b[^>]*>)(.*)</section>$', reality, re.S)
    rbody = rm.group(2)
    open_ = re.search(r'<div class="kreal-open">.*?</div>\s*<div>.*?</div>\s*</div>', rbody, re.S).group(0)
    rest = rbody.replace(open_, "", 1)
    open2 = re.sub(r'\s*<p class="dst-lede">.*?</p>', "", open_, count=1, flags=re.S)
    lede_r = re.search(r'<p class="dst-lede">.*?</p>', open_, re.S).group(0)
    reality = (rm.group(1).replace('class="dst-sec is-loud"', 'class="dst-sec is-loud v4t-real"') + open2 +
               "\n  " + fold('<div class="v4t-more-in">' + lede_r + rest + "</div>", "How a day runs, and who it is for", "v4-fold v4t-more") + "\n</section>")

    # ---- the reference folds: travel essentials, packing, etiquette ---------------------
    practical_f = head_fold(practical, "practical")
    packing_f = head_fold(packing, "packing")
    ground_f = head_fold(ground, "ground")

    # ---- the call: the pitch folds -------------------------------------------------
    after = re.sub(r'(<section class="cta-band" id="enquire">.*?</div>\s*)(<p class="cta-body">.*?</ol>)',
                   lambda m: m.group(1) + fold(m.group(2), "We'll break down", "v4-fold v4t-cfold"), after, count=1, flags=re.S)
    after = after.replace('class="listen-btn" data-hover>\n      <span>', 'class="btn-lines v4-wa" data-hover>\n      <span>', 1)
    # the phone bar: hold a place, and the next departure
    after = after.replace('<a class="btn-solid" href="#enquire" data-hover><span>Enquire</span></a>',
                          '<a class="btn-solid" href="#dates" data-hover><span>Hold a place</span></a>', 1)

    body = ('<div class="dst-shell">\n<div class="dst-main">\n' + ov + "\n\n" + route + "\n\n" + gallery + "\n\n" + dates +
            "\n\n" + guides_sec + "\n\n" + hear.replace('<section class="dst-sec">', '<section class="dst-sec v4t-show" id="from-the-show">', 1) +
            "\n\n" + faq + "\n\n" + reality +
            '\n\n<div class="v4t-ref" aria-label="Before you go">\n' + practical_f + "\n" + packing_f + "\n" + ground_f + "\n</div>\n"
            "\n</div>\n</div>\n\n")
    out = before + body + after
    out = out.replace('<body class="dst v2-dst">', '<body class="dst v2-dst v4-trip">', 1)
    out = add_script(out)
    return out


OPEN_JS = """<script>
/* v4: a link to an anchor inside a fold (#packing, a FAQ answer) opens the
   fold first, so the page lands on the words, not on a closed title. */
(function () {
  function openTo(id) {
    var el = id && document.getElementById(id);
    if (!el) return;
    for (var d = el; d; d = d.parentElement) if (d.tagName === 'DETAILS') d.open = true;
    if (el.tagName === 'SECTION') { var f = el.querySelector(':scope > details'); if (f) f.open = true; }
  }
  function go() { try { openTo(decodeURIComponent(location.hash.slice(1))); } catch (e) {} }
  window.addEventListener('hashchange', go);
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (a) openTo(a.getAttribute('href').slice(1));
  });
  go();
})();
</script>
"""


def add_script(src):
    return src.replace("</body>", OPEN_JS + "</body>", 1)


def main(args):
    os.makedirs(OUT, exist_ok=True)
    for trip in args or ["india"]:
        page = {"india": india}[trip]()
        open(os.path.join(OUT, trip + ".html"), "w", encoding="utf-8").write(page)
        print("v4 trip:", trip)


if __name__ == "__main__":
    main(sys.argv[1:])
