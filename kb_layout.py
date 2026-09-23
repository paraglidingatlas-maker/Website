"""Category page layout for the knowledge base (the Flight Mechanics design).

WHY
The first version of this design was a hand-built file in templates/kb/. That
works for one page and fails for twenty. This module renders the same page from
a content dict in kb_editorial.py, so a new category is content plus images,
never markup. generate_kb_pages.py calls render() when a slug has "layout": 2.

WHAT A CATEGORY ENTRY NEEDS (see kb_editorial.py for the Flight Mechanics one)
  kicker, h1, lead, sub, seo_title, seo_desc, hero_alt
  hero image: assets/images/kb-<slug>.jpg (+ .webp); optional
  bands: list of {num, kicker, heading, short, paras, bold, chips:[(name, ep)],
                  figure: None | {panels:[{img,w,h,title,text,alt}], cols, source_html}}
  quote_band: {after_band, img, alt, kicker, quote, who, cite_ep, cite_ch, cite_label, caption} | None
  callout: {kicker, heading, text, ep, ch, who, numbers:[(big, small, label)]} | None
  groups: [(label, [ (title, body, ep, ch, who) ])]
  faq: [{q, a, ep, ch, who}]
  next: {main:(href, title, blurb), cards:[(kicker, href, title, blurb)]}
Chapter links are validated against the episode pages at build time.
"""
import html, os, re

E = html.escape
ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(ROOT, "templates", "kb", "category.css"), encoding="utf-8").read()
JS = open(os.path.join(ROOT, "templates", "kb", "category.js"), encoding="utf-8").read()

_ch_cache = {}


def chapter_title(ep, cid):
    key = (ep, cid)
    if key not in _ch_cache:
        path = os.path.join(ROOT, "episodes", ep + ".html")
        if not os.path.exists(path):
            raise SystemExit("kb_layout: no episode page for %s" % ep)
        page = open(path, encoding="utf-8").read()
        m = re.search(r'<div class="cd-block" id="%s">\s*<h2>(.*?)</h2>' % re.escape(cid), page, re.S)
        if not m:
            raise SystemExit("kb_layout: no chapter %s on %s" % (cid, ep))
        _ch_cache[key] = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    return _ch_cache[key]


def src(ep, ch, who):
    return ('<a class="src" href="../episodes/%s.html#%s">%s <span>%s</span></a>'
            % (ep, ch, E(who), E(chapter_title(ep, ch))))


def link(ep, ch, label):
    chapter_title(ep, ch)  # validates
    return '<a href="../episodes/%s.html#%s">%s</a>' % (ep, ch, E(label))


def pic(name, alt, w, h, extra=""):
    return ('<picture><source srcset="../assets/images/%s.webp" type="image/webp">'
            '<img src="../assets/images/%s.jpg" alt="%s" width="%d" height="%d"%s></picture>'
            % (name, name, E(alt), w, h, extra))


def bold(text, terms):
    t = E(text)
    for term in terms or []:
        et = E(term)
        if et in t:
            t = t.replace(et, "<strong>%s</strong>" % et, 1)
    return t


def hero(slug, ed, stats):
    img = "kb-" + slug
    has_img = os.path.exists(os.path.join(ROOT, "assets", "images", img + ".jpg"))
    media = ('<div class="k-hero-media">%s</div>' % pic(img, ed.get("hero_alt", ""), 2400, 900,
             ' fetchpriority="high" decoding="async"')) if has_img else ""
    stat_html = "".join("<span><b>%s</b>%s</span>" % (E(str(v)), E(l)) for v, l in stats)
    sub = '<p class="sub">%s</p>' % E(ed["sub"]) if ed.get("sub") else ""
    return ('<header class="k-hero">%s<div class="k-hero-copy">'
            '<p class="breadcrumb"><a href="../knowledge-base.html">Knowledge Base</a> / <a href="%s.html">%s</a> / %s</p>'
            '<span class="kicker">%s</span><h1>%s</h1><p class="lead">%s</p>%s'
            '<div class="k-stats">%s</div></div></header>'
            % (media, ed["_cat_slug"], E(ed["_cat_title"]), E(ed["kicker"]), E(ed["kicker"]), E(ed["h1"]),
               E(ed["lead"]), sub, stat_html))


def figure(fig):
    """One wide drawing with a caption per panel underneath, then a source line."""
    if not fig:
        return ""
    caps = "".join("<div><span>%s</span>%s</div>" % (E(a), E(b)) for a, b in fig["captions"])
    return ('<figure class="band-draw">%s<figcaption class="bd-caps c%d">%s<p class="bd-src">%s</p></figcaption></figure>'
            % (pic(fig["img"], fig["alt"], fig["w"], fig["h"], ' loading="lazy"'), fig.get("cols", len(fig["captions"])),
               caps, fig["source_html"]))


def bands(ed):
    out = []
    for i, b in enumerate(ed["bands"]):
        chips = '<span class="lab">From</span>' + "".join(
            '<a href="../episodes/%s.html">%s</a>' % (ep, E(name)) for name, ep in b["chips"])
        paras = "".join("<p>%s</p>" % bold(p, b.get("bold")) for p in b["paras"])
        out.append('<section class="k-sec %s"><div class="band"><div class="l"><span class="num">%s</span>'
                   '<span class="kicker">%s</span><h2>%s</h2><p class="short">%s</p></div>'
                   '<div class="r">%s<div class="chips">%s</div></div></div>%s</section>'
                   % ("bg" if i % 2 == 0 else "card", b["num"], E(b["kicker"]), E(b["heading"]), E(b["short"]),
                      paras, chips, figure(b.get("figure"))))
        q = ed.get("quote_band")
        if q and q["after_band"] == i:
            out.append(quote_band(q))
    return "".join(out)


def quote_band(q):
    return ('<figure class="band-fig"><div class="bf-media">%s</div>'
            '<figcaption class="bf-q"><span class="kicker">%s</span><p class="qt">%s</p>'
            '<p class="who">%s %s</p><p class="cap">%s</p></figcaption></figure>'
            % (pic(q["img"], q["alt"], 2400, 1000, ' loading="lazy"'), E(q["kicker"]), E(q["quote"]), E(q["who"]),
               link(q["cite_ep"], q["cite_ch"], q["cite_label"]), E(q["caption"])))


def callout(c):
    if not c:
        return ""
    nums = "".join('<div><b>%s%s</b><span>%s</span></div>'
                   % (E(big), "<small>%s</small>" % E(small) if small else "", E(label))
                   for big, small, label in c["numbers"])
    return ('<div class="check"><div class="ck-l"><span class="kicker">%s</span><h3>%s</h3><p>%s</p>%s</div>'
            '<div class="ck-n">%s</div></div>'
            % (E(c["kicker"]), E(c["heading"]), E(c["text"]), src(c["ep"], c["ch"], c["who"]), nums))


def groups(ed):
    out, i = [], 0
    for gi, (label, items) in enumerate(ed["groups"], 1):
        cards = ""
        for title, body, ep, ch, who in items:
            i += 1
            cards += ('<div class="cardx"><span class="n">%02d</span><h3>%s</h3><p>%s</p>%s</div>'
                      % (i, E(title), E(body), src(ep, ch, who)))
        out.append('<div class="tk-row"><div class="tk-lab"><span class="kicker">%02d</span><h3>%s</h3></div>'
                   '<div class="cards">%s</div></div>' % (gi, E(label), cards))
    return "".join(out)


def faq(ed, n_eps):
    items = "".join(
        '<details%s><summary><h3>%s</h3></summary><p>%s</p>%s</details>'
        % (" open" if i == 0 else "", E(f["q"]), E(f["a"]), src(f["ep"], f["ch"], f["who"]))
        for i, f in enumerate(ed["faq"]))
    for f in ed["faq"]:
        if not f["q"].strip().endswith("?"):
            raise SystemExit("kb_layout: FAQ question must end with ?: " + f["q"])
    return ('<div class="faq"><div class="faq-l"><div class="fq-in"><span class="kicker">FAQ</span>'
            '<h2>%s</h2><p>Each answer links to the chapter of the episode where the guest says it.</p>'
            '<div class="fq-n"><div><b>%d</b><span>questions</span></div><div><b>%d</b><span>episodes</span></div></div>'
            '</div></div><div class="faq-r">%s</div></div>'
            % (E(ed.get("faq_heading", "Questions these conversations answer")), len(ed["faq"]), n_eps, items))


def next_strip(nx):
    href, title, blurb = nx["main"]
    main = ('<a class="nx-main" href="%s"><span class="kicker">Next in the Knowledge Base</span><strong>%s</strong>'
            '<em>%s</em><i>Read it &rarr;</i></a>' % (href, E(title), E(blurb)))
    cards = "".join('<a class="nx-card" href="%s"><span class="kicker">%s</span><strong>%s</strong><em>%s</em></a>'
                    % (h, E(k), E(t), E(b)) for k, h, t, b in nx["cards"])
    return '<section class="k-sec bg k-next"><div class="nx">%s%s</div></section>' % (main, cards)


def render(slug, ed, ep_html, n_eps, stats):
    """Body + style for one category page. The generator wraps it in head/nav/footer."""
    body = (hero(slug, ed, stats)
            + '<section class="k-sec bg" id="episodes"><div class="k-head"><h2>The %s conversations</h2>'
              '<span class="kicker">Open any tile for chapters, quotes and links</span></div>%s</section>'
              % (_words(n_eps), ep_html)
            + bands(ed)
            + '<section class="k-sec bg" id="takeaways"><div class="k-head"><h2>%s</h2>'
              '<span class="kicker">Each one links to the chapter where it is said</span></div>%s%s</section>'
              % (E(ed.get("takeaways_heading", "Worth remembering")), callout(ed.get("callout")), groups(ed))
            + '<section class="k-sec card" id="questions">%s</section>' % faq(ed, n_eps)
            + next_strip(ed["next"]))
    return CSS, body, JS


def _words(n):
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
            10: "ten", 11: "eleven", 12: "twelve"}.get(n, str(n))


def landing(slug, ld, cards_html, n_series):
    """Body for a category landing page: the lighter treatment. A hero, the series
    cards, and a short FAQ whose answers draw on the series pages and link to the
    chapters those pages already cite. Same stylesheet and script as the series
    pages; generate_kb_pages.py adds the card rules and wraps it in head and nav."""
    img = "kb-" + slug
    has_img = os.path.exists(os.path.join(ROOT, "assets", "images", img + ".jpg"))
    media = ('<div class="k-hero-media">%s</div>' % pic(img, ld.get("hero_alt", ""), 2400, 900,
             ' fetchpriority="high" decoding="async"')) if has_img else ""
    sub = '<p class="sub">%s</p>' % E(ld["sub"]) if ld.get("sub") else ""
    hero = ('<header class="k-hero">%s<div class="k-hero-copy">'
            '<p class="breadcrumb"><a href="../knowledge-base.html">Knowledge Base</a> / %s</p>'
            '<span class="kicker">%s</span><h1>%s</h1><p class="lead">%s</p>%s'
            '<div class="k-stats"><span><b>%d</b>series</span><span><b>%d</b>questions below</span></div></div></header>'
            % (media, E(ld["kicker"]), E(ld["kicker"]), E(ld["h1"]), E(ld["lead"]), sub, n_series, len(ld["faq"])))
    series = ('<section class="k-sec bg" id="series"><div class="k-head"><h2>%s</h2><span class="kicker">%s</span></div>'
              '<div class="series-grid">%s\n  </div></section>'
              % (E(ld.get("series_heading", "The series")),
                 E(ld.get("series_kicker", "Built from the episodes")), cards_html))
    items = ""
    for i, f in enumerate(ld["faq"]):
        if not f["q"].strip().endswith("?"):
            raise SystemExit("kb_layout: FAQ question must end with ?: " + f["q"])
        items += ('<details%s><summary><h3>%s</h3></summary><p>%s</p>%s</details>'
                  % (" open" if i == 0 else "", E(f["q"]), E(f["a"]),
                     "".join(src(ep, ch, who) for ep, ch, who in f["src"])))
    n_eps = len({ep for f in ld["faq"] for ep, _, _ in f["src"]})
    faq_html = ('<section class="k-sec card" id="questions"><div class="faq"><div class="faq-l"><div class="fq-in">'
                '<span class="kicker">FAQ</span><h2>%s</h2>'
                '<p>Each answer draws on the series pages and links to the chapters where the guests say it.</p>'
                '<div class="fq-n"><div><b>%d</b><span>questions</span></div><div><b>%d</b><span>episodes</span></div></div>'
                '</div></div><div class="faq-r">%s</div></div></section>'
                % (E(ld.get("faq_heading", "Questions across these series")), len(ld["faq"]), n_eps, items))
    return CSS, hero + series + faq_html, JS
