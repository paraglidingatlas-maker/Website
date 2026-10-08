#!/usr/bin/env python3
"""Encyclopedia: one page per question, and an A to Z of every question the
Knowledge Base answers.

    python3 generate_answer_pages.py                 # the real build
    ENC_SHOW_DRAFTS=1 python3 generate_answer_pages.py   # review build: drafts listed

WHERE THINGS LIVE
  kb_answers.py                      the content, one entry per question
  templates/kb/answer.css            the answer-page and A to Z layout
  knowledge-base/encyclopedia/       the output: <slug>.html and index.html
The pages reuse the series pages' stylesheet and script (templates/kb/category.*)
and the shared head, nav and footer from generate_kb_pages.py, read from that file
rather than copied, so a nav change lands here too.

WHAT THE BUILD CHECKS, AND FAILS ON
  - a citation [n] with no source n, and a source no citation uses
  - a guest chapter that does not exist on the episode page
  - a {{slug|text}} link, or a related slug, with no entry
  - a related FAQ question that no series or landing page carries
  - an em-dash anywhere in the copy; a question that does not end in "?"
  - a title over 70 characters with the site suffix, a description outside 70 to 165
  - a short answer outside 35 to 80 words
"""
import ast
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import site_config as cfg  # noqa: E402
import kb_layout  # noqa: E402
from kb_answers import ENTRIES  # noqa: E402
from kb_editorial import EDITORIAL  # noqa: E402
from kb_landing import LANDING  # noqa: E402

def E(s, quote=False):
    """Text escaping. Apostrophes stay literal in text: the title-case step treats an
    entity as a word break and would turn "paraglider&#x27;s" into "Paraglider'S".
    Attribute values pass quote=True."""
    return html.escape(s, quote=quote)


OUT_DIR = os.path.join(ROOT, "knowledge-base", "encyclopedia")
SHOW_DRAFTS = os.environ.get("ENC_SHOW_DRAFTS") == "1"
AUTHOR = {"@type": "Person", "name": "Aninder Singh", "url": cfg.url("about.html"),
          "jobTitle": "Host, Paragliding Atlas"}
SUFFIX = " | Paragliding Atlas"


def fail(msg):
    raise SystemExit("generate_answer_pages: " + msg)


# ── shared head, nav and footer, read from generate_kb_pages.py ──────────────
def _kb_templates():
    tree = ast.parse(open(os.path.join(ROOT, "generate_kb_pages.py"), encoding="utf-8").read())
    got = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in ("NAV_HEADER", "NAV_FOOTER")):
            got[node.targets[0].id] = ast.literal_eval(node.value)
    if len(got) != 2:
        fail("could not read NAV_HEADER and NAV_FOOTER from generate_kb_pages.py")
    return got["NAV_HEADER"], got["NAV_FOOTER"]


NAV_HEADER, NAV_FOOTER = _kb_templates()
# The series header carries its own <title> and CollectionPage block; an answer
# page brings its own, so keep everything from the favicon onwards.
HEAD_TAIL = NAV_HEADER[NAV_HEADER.index('<link rel="icon"'):]
CSS = kb_layout.CSS + open(os.path.join(ROOT, "templates", "kb", "answer.css"), encoding="utf-8").read()
JS = kb_layout.JS


def deeper(h):
    """The shared templates are written for knowledge-base/; these pages sit one level lower."""
    return h.replace('"../', '"../../')


# ── the knowledge base around the encyclopedia ───────────────────────────────
def breadcrumb_of(series):
    """(category slug, category title, series title) from the series page's own breadcrumb."""
    path = os.path.join(ROOT, "knowledge-base", series + ".html")
    if not os.path.exists(path):
        fail("no series page knowledge-base/%s.html" % series)
    m = re.search(r'<p class="breadcrumb">(.*?)</p>', open(path, encoding="utf-8").read(), re.S)
    links = re.findall(r'<a href="([^"]+)\.html">([^<]+)</a>', m.group(1))
    cat_slug, cat_title = links[-1]
    tail = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)).split("/")[-1].strip())
    return cat_slug, html.unescape(cat_title), tail


CAT_SHORT = {"technical": "Technical", "meteorology": "Meteorology", "core-series": "Core Series",
             "competitions": "Competitions", "industry": "Industry"}


def all_faqs():
    """Every question the series and landing pages answer: (question, href from encyclopedia/, series title, category)."""
    out = []
    for slug, ed in EDITORIAL.items():
        if ed.get("layout") != 2:
            continue
        cat, _, stitle = breadcrumb_of(slug)
        for f in ed.get("faq", []):
            out.append({"q": f["q"], "href": "../%s.html#%s" % (slug, kb_layout.faq_id(f["q"])),
                        "where": stitle, "cat": cat, "series": slug})
    for slug, ld in LANDING.items():
        for f in ld.get("faq", []):
            out.append({"q": f["q"], "href": "../%s.html#%s" % (slug, kb_layout.faq_id(f["q"])),
                        "where": html.unescape(ld["kicker"]), "cat": slug, "series": slug})
    return out


FAQS = all_faqs()
FAQ_BY_Q = {(f["series"], f["q"]): f for f in FAQS}
BY_SLUG = {a["slug"]: a for a in ENTRIES}


def listed(a):
    return a["status"] == "published" or SHOW_DRAFTS


# ── text: citations and cross-references ─────────────────────────────────────
CITE = re.compile(r"\[(\d+)\]")
XREF = re.compile(r"\{\{([a-z0-9-]+)\|([^}]+)\}\}")


def rich(text, a, used):
    """Escape, then turn [n] into a source link and {{slug|text}} into a page link."""
    if "—" in text:
        fail("em-dash in %s: %s" % (a["slug"], text[:60]))
    t = E(text)

    def cite(m):
        n = int(m.group(1))
        if not 1 <= n <= len(a["sources"]):
            fail("%s cites [%d] but has %d sources" % (a["slug"], n, len(a["sources"])))
        used.add(n)
        return '<sup class="cite"><a href="#s%d" aria-label="Source %d">[%d]</a></sup>' % (n, n, n)

    def xref(m):
        slug, label = m.group(1), m.group(2)
        if slug not in BY_SLUG:
            fail("%s links to unknown answer %s" % (a["slug"], slug))
        return '<a class="xref" href="%s.html">%s</a>' % (slug, label)

    t = CITE.sub(cite, t)
    t = XREF.sub(xref, t)
    return t


def plain(text):
    """The same text with citations and link markup removed, for meta tags and schema."""
    return re.sub(r"\s+", " ", XREF.sub(lambda m: m.group(2), CITE.sub("", text))).replace(" .", ".").strip()


def emph(t, terms):
    for term in terms or []:
        et = E(term)
        if et in t:
            t = t.replace(et, "<strong>%s</strong>" % et, 1)
    return t


def pic(name, alt, w, h, extra=""):
    for ext in ("jpg", "webp"):
        if not os.path.exists(os.path.join(ROOT, "assets", "images", "%s.%s" % (name, ext))):
            fail("missing image assets/images/%s.%s" % (name, ext))
    return ('<picture><source srcset="../../assets/images/%s.webp" type="image/webp">'
            '<img src="../../assets/images/%s.jpg" alt="%s" width="%d" height="%d"%s></picture>'
            % (name, name, E(alt, True), w, h, extra))


# ── one answer page ──────────────────────────────────────────────────────────
def figure(fig):
    caps = "".join("<div><span>%s</span>%s</div>" % (E(t), E(b)) for t, b in fig["captions"])
    return ('<figure class="band-draw">%s<figcaption class="bd-caps c%d">%s<p class="bd-src">%s</p></figcaption></figure>'
            % (pic(fig["img"], fig["alt"], fig["w"], fig["h"], ' loading="lazy" decoding="async"'),
               fig.get("cols", len(fig["captions"])), caps, fig["source_html"]))


def table(tb, a, used):
    head = "".join("<th scope=\"col\">%s</th>" % E(c) for c in tb["cols"])
    rows = ""
    for r in tb["rows"]:
        if len(r) != len(tb["cols"]):
            fail("%s: table row %r does not match its columns" % (a["slug"], r))
        cells = ""
        for i, v in enumerate(r):
            num = ' class="num"' if re.match(r"^[\d.,+ -]+$|^about \d|^\d+ to \d+$", v) else ""
            cells += '<td data-l="%s"%s>%s</td>' % (E(tb["cols"][i], True), num, rich(v, a, used))
        rows += "<tr>%s</tr>" % cells
    return ('<div class="a-table-wrap"><table class="a-table"><caption>%s</caption><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (rich(tb["caption"], a, used), head, rows))


def callout(c, a, used):
    n = len(c["numbers"])
    nums = "".join('<div><b>%s%s</b><span>%s</span></div>'
                   % (E(big), "<small>%s</small>" % E(small) if small else "", E(label))
                   for big, small, label in c["numbers"])
    refs = "".join(rich("[%d]" % i, a, used) for i in c.get("cite", []))
    return ('<div class="check"><div class="ck-l"><span class="kicker">%s</span><h3>%s</h3><p>%s</p>'
            '<span class="ck-src">Sources %s</span></div><div class="ck-n n%d">%s</div></div>'
            % (E(c["kicker"]), E(c["heading"]), E(c["text"]), refs, n, nums))


def section(i, s, a, used):
    if not s["h"].strip():
        fail("%s: section without a heading" % a["slug"])
    body = "".join("<p>%s</p>" % emph(rich(p, a, used), s.get("bold")) for p in s.get("paras", []))
    if s.get("list"):
        body += '<ul class="a-list">%s</ul>' % "".join(
            "<li>%s</li>" % emph(rich(x, a, used), s.get("bold")) for x in s["list"])
    if s.get("table"):
        body += table(s["table"], a, used)
    body += "".join("<p>%s</p>" % emph(rich(p, a, used), s.get("bold")) for p in s.get("after", []))
    out = ('<section class="k-sec %s" id="%s"><div class="band"><div class="l"><span class="num">%02d</span>'
           '<span class="kicker">%s</span><h2>%s</h2><p class="short">%s</p></div><div class="r">%s</div></div>'
           % ("bg" if i % 2 == 0 else "card", sec_id(s), i + 1, E(s["kicker"]), E(s["h"]),
              rich(s["short"], a, used), body))
    if s.get("figure"):
        out += figure(s["figure"])
    if s.get("callout"):
        out += callout(s["callout"], a, used)
    return out + "</section>"


def sec_id(s):
    return re.sub(r"[^a-z0-9]+", "-", s["kicker"].lower()).strip("-")


def related_items(a):
    items = []
    for r in a["related"]:
        if isinstance(r, str):
            if r not in BY_SLUG:
                fail("%s: related answer %s does not exist" % (a["slug"], r))
            b = BY_SLUG[r]
            items.append(("In depth", "%s.html" % r, b["q"], first_sentence(b["short"]), b))
        else:
            _, series, q = r
            f = FAQ_BY_Q.get((series, q))
            if not f:
                fail("%s: related FAQ not found on %s: %s" % (a["slug"], series, q))
            items.append((f["where"], f["href"], q, "A short answer from the guests, on the %s page." % f["where"],
                          None))
    return items


def first_sentence(t):
    m = re.match(r"(.+?[.?!])(\s|$)", t)
    return m.group(1) if m else t


def related_strip(a):
    items = related_items(a)
    # Only answers that are listed can be linked from a published page.
    items = [x for x in items if x[4] is None or listed(x[4])]
    cards = "".join('<a class="nx-card" href="%s"><span class="kicker">%s</span><strong>%s</strong><em>%s</em></a>'
                    % (h, E(k), E(q), E(blurb)) for k, h, q, blurb, _ in items)
    return ('<section class="k-sec bg k-next" id="related"><div class="k-head"><h2>Related questions</h2>'
            '<span class="kicker"><a href="index.html">Every question, A to Z</a></span></div>'
            '<div class="nx nx-rel">%s</div></section>' % cards)


def show_section(a):
    if not a["show"]:
        return ""
    cards = ""
    for who, ep, ch, title, text in a["show"]:
        kb_layout.chapter_title(ep, ch)  # fails the build on a chapter that does not exist
        if "—" in text:
            fail("em-dash in show text on %s" % a["slug"])
        cards += ('<div class="cardx"><span class="n">%s</span><h3>%s</h3><p>%s</p>'
                  '<a class="src" href="../../episodes/%s.html#%s">%s <span>%s</span></a></div>'
                  % (E(who), E(title), E(text), ep, ch, E(who), E(kb_layout.chapter_title(ep, ch))))
    return ('<section class="k-sec card" id="from-the-show"><div class="k-head"><h2>From the show</h2>'
            '<span class="kicker">What the guests add</span></div>'
            '<p class="show-note">Paraphrased from Paragliding Atlas episodes, never quoted, because the transcripts '
            'are automatic captions. Each card links to the chapter where it is said.</p>'
            '<div class="cards">%s</div></section>' % cards)


def sources_section(a, used):
    lis = ""
    for i, (title, pub, url, kind) in enumerate(a["sources"], 1):
        lis += ('<li id="s%d"><a href="%s" rel="noopener" target="_blank">%s</a><span>%s<i>%s</i></span></li>'
                % (i, E(url, quote=True), E(title), E(pub), E(kind)))
    rev = a.get("reviewed")
    method = ('<div class="a-method"><span class="kicker">How this answer was made</span>'
              '<h3>Sources first, then the show</h3>'
              '<p>The explanation is rewritten in plain language from the sources listed here, which you can '
              'check for yourself. Government handbooks are used where they exist; manufacturer manuals, federations '
              'and test houses for what is specific to paragliders. Numbers worked out on this page rather than '
              'quoted are labelled as worked examples.</p>'
              '<p>The guest cards add what was said on the show, paraphrased and linked to the chapter.</p>'
              '<p>%s Spotted a mistake? <a href="../../corrections.html">Tell me</a> and I will fix it.</p></div>'
              % (("Reviewed by Aninder Singh on %s." % human_date(rev)) if rev else
                 "Draft: not yet reviewed."))
    return ('<section class="k-sec bg" id="sources"><div class="k-head"><h2>Sources</h2>'
            '<span class="kicker">%d sources, cited in the text by number</span></div>'
            '<div class="a-sources"><ol>%s</ol>%s</div></section>' % (len(a["sources"]), lis, method))


def human_date(d):
    dt = datetime.date.fromisoformat(d)
    return "%d %s %d" % (dt.day, dt.strftime("%b"), dt.year)


def validate(a):
    q = a["q"].strip()
    if not q.endswith("?"):
        fail("question must end with ?: " + q)
    words = len(a["short"].split())
    if not 35 <= words <= 80:
        fail("%s: short answer is %d words, keep it 35 to 80" % (a["slug"], words))
    title = a["seo_title"] + SUFFIX
    if len(title) > 70:
        fail("%s: title is %d characters with the suffix (max 70): %s" % (a["slug"], len(title), title))
    if not 70 <= len(a["seo_desc"]) <= 165:
        fail("%s: description is %d characters (70 to 165)" % (a["slug"], len(a["seo_desc"])))
    if CITE.search(a["short"]) or XREF.search(a["short"]):
        fail("%s: the short answer must stand alone, without citations or links" % a["slug"])
    for field in ("short", "seo_title", "seo_desc", "q"):
        if "—" in a[field]:
            fail("em-dash in %s.%s" % (a["slug"], field))
    if a["status"] not in ("draft", "published"):
        fail("%s: status must be draft or published" % a["slug"])
    if a["status"] == "published" and not a.get("reviewed"):
        fail("%s: a published page needs a reviewed date" % a["slug"])


def schema(a, page, image):
    url = cfg.public_url(page)
    cat, cat_title, series_title = breadcrumb_of(a["series"])
    answer = {"@type": "Answer", "text": plain(a["short"]), "url": url + "#answer", "author": AUTHOR}
    web = {"@type": "WebPage", "url": url, "name": a["seo_title"] + SUFFIX, "description": a["seo_desc"],
           "inLanguage": "en", "isPartOf": {"@type": "WebSite", "name": "Paragliding Atlas", "url": cfg.BASE},
           "primaryImageOfPage": image,
           "mainEntity": {"@type": "Question", "name": a["q"], "acceptedAnswer": answer}}
    if a.get("reviewed"):
        web["reviewedBy"] = AUTHOR
        web["lastReviewed"] = a["reviewed"]
    eps = []
    for who, ep, ch, _, _ in a["show"]:
        u = cfg.url("episodes/%s.html" % ep)
        if u not in [e["url"] for e in eps]:
            eps.append({"@type": "PodcastEpisode", "url": u})
    art = {"@type": "Article", "@id": url + "#article", "headline": a["q"], "description": plain(a["short"]),
           "author": AUTHOR, "publisher": {"@id": cfg.ORG_ID}, "image": image, "inLanguage": "en",
           "datePublished": a["updated"], "dateModified": a["updated"], "mainEntityOfPage": url,
           "isPartOf": {"@type": "CollectionPage", "name": series_title,
                        "url": cfg.url("knowledge-base/%s.html" % a["series"])},
           "about": {"@type": "Thing", "name": a["topic"]},
           "citation": [{"@type": "CreativeWork", "name": t, "url": u,
                         "publisher": {"@type": "Organization", "name": p}} for t, p, u, _ in a["sources"]],
           "mentions": eps}
    data = {"@context": "https://schema.org", "@graph": [web, art]}
    return json.dumps(data, ensure_ascii=False, indent=1)


def head(title, desc, canonical, image, ld, noindex):
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n%s'
            '<link rel="canonical" href="%s">\n<meta property="og:type" content="article">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:image" content="%s">\n<meta property="og:url" content="%s">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<script type="application/ld+json">\n%s\n</script>\n'
            % (E(title), E(desc, quote=True), robots, canonical, E(title, quote=True), E(desc, quote=True), image,
               canonical, ld))


def answer_page(a):
    validate(a)
    page = "knowledge-base/encyclopedia/%s.html" % a["slug"]
    canonical = cfg.public_url(page)
    cat, cat_title, series_title = breadcrumb_of(a["series"])
    hero_img = "kb-" + a["series"]
    image = cfg.url("assets/images/%s.jpg" % hero_img)
    used = set()

    secs = "".join(section(i, s, a, used) for i, s in enumerate(a["sections"]))
    toc = "".join('<li><a href="#%s">%s</a></li>' % (sec_id(s), E(s["h"])) for s in a["sections"])
    if a["show"]:
        toc += '<li><a href="#from-the-show">From the show</a></li>'
    toc += '<li><a href="#sources">Sources</a></li>'
    also = ('<p class="a-also"><b>Also asked as:</b> %s</p>' % E(" · ".join(a["also"]))) if a.get("also") else ""
    safety = ('<p class="a-safety"><b>Safety.</b> This page explains how things work; it is not flying instruction. '
              'Learn and practise these situations with a qualified instructor, ideally on a safety (SIV) course '
              'over water, and follow the manual for your own wing, which takes precedence over anything here.</p>'
              if a.get("safety") else "")
    short = rich(a["short"], a, used)
    guests = sorted({who for who, *_ in a["show"]})
    meta = ['<span>By <a href="../../about.html">Aninder Singh</a></span>',
            "<span>Updated %s</span>" % human_date(a["updated"]),
            "<span>%d sources</span>" % len(a["sources"])]
    if guests:
        meta.append("<span>%d %s from the show</span>" % (len(guests), "guest" if len(guests) == 1 else "guests"))
    draft = '<span class="a-draft">Draft for review</span>' if a["status"] == "draft" else ""

    hero = ('<header class="k-hero a-hero"><div class="k-hero-media">%s</div><div class="k-hero-copy">'
            '<p class="breadcrumb"><a href="../../knowledge-base.html">Knowledge Base</a> / '
            '<a href="../%s.html">%s</a> / <a href="../%s.html">%s</a> / %s</p>%s'
            '<span class="kicker">Encyclopedia · %s</span><h1>%s</h1><p class="a-meta">%s</p></div></header>'
            % (pic(hero_img, "", 2400, 900, ' fetchpriority="high" decoding="async"'), cat, E(cat_title),
               a["series"], E(series_title), E(a["q"]), draft, E(series_title), E(a["q"]), "".join(meta)))
    short_sec = ('<section class="k-sec card a-short" id="answer"><div class="a-short-in"><div>'
                 '<span class="kicker">The short answer</span><p class="a-lede">%s</p>%s%s</div>'
                 '<nav class="a-toc" aria-label="On this page"><span class="kicker">On this page</span><ol>%s</ol></nav>'
                 '</div></section>' % (short, also, safety, toc))
    body = hero + short_sec + secs + show_section(a) + sources_section(a, used) + related_strip(a)

    unused = set(range(1, len(a["sources"]) + 1)) - used
    if unused:
        fail("%s: sources never cited: %s" % (a["slug"], sorted(unused)))

    html_out = (head(a["seo_title"] + SUFFIX, a["seo_desc"], canonical, image, schema(a, page, image),
                     a["status"] == "draft")
                + deeper(HEAD_TAIL).format(css=CSS, body=body) + deeper(NAV_FOOTER))
    html_out = html_out.replace("</body>", JS + "\n</body>", 1)
    return page, html_out


# ── the A to Z ───────────────────────────────────────────────────────────────
# Topic for a series or landing FAQ, from its wording. First match wins; the
# encyclopedia entries carry their own topic. Ordered from specific to general.
TOPIC_RULES = [
    (r"\breserves?\b|\bmirror effect\b", "Reserve parachutes"),
    (r"\bharness|crumple|koroyd|submarine\b", "Harnesses"),
    (r"\bhelmet|carabiner", "Helmets and carabiners"),
    (r"\bdog\b", "Flying with a dog"),
    (r"collision", "Mid-air collisions"),
    (r"hypoxia|oxygen|acclimati|8,000|high altitude", "High altitude"),
    (r"x-alps|vol-biv|socotra", "Adventure and vol-biv"),
    (r"insurance", "Accidents and safety culture"),
    (r"colombia|roldanillo|\bbir\b|billing|delhi|back ranges|mount borah|panchgani|kenya|abroad|local guide|"
     r"land out|new site", "Places to fly"),
    (r"review|real performance differences|glider class|move up|more advanced wing|buy a new|cheap paragliding|"
     r"harnesses made in europe", "Choosing and buying a wing"),
    (r"\bcivl|proxy voting|governance|world cup association|licence to fly in the paragliding world cup",
     "Competition rules and governance"),
    (r"scor|leading points|discard|turnpoint|race and a time trial|sports racing series|category 2",
     "Competition scoring and tasks"),
    (r"competition|world cup|world championship|castelo|gaggle", "Competitions"),
    (r"weather|forecast|windy|millibar|wind barb|sounding|inversion|cloud base|convergence|overdevelop|gust front|"
     r"cloud suck|wind strongest|storm", "Weather and forecasting"),
    (r"thermal|flat country", "Thermals and lift"),
    (r"\ben certification|test report|certified|folding line|collapse done hands up", "Certification"),
    (r"collapse", "Collapses"),
    (r"stall|spin\b", "Stalls and spins"),
    (r"\bbrake|b risers|pitch-up|stable in pitch|trimming|two-liner|fewer lines|closed cells|wave leading edge|"
     r"kite risers|enzo|skymate|smart harness", "Wing design and control"),
    (r"siv|active flying", "Safety training"),
    (r"beer|eat and drink", "Body and fitness"),
    (r"afraid|fear|scared|calm|negative thoughts|visualisation|pre-flight routine|pushing too hard|less bold|"
     r"decide not to fly|instructor|advice from|intermediate syndrome|capacity|risk|went wrong",
     "Mind, risk and judgement"),
    (r"insurance|helicopter|fatalit|accident|dangerous|safer|responsible", "Accidents and safety culture"),
    (r"camera|filmmaker|followers|sponsor", "Filming and sponsorship"),
    (r"living|afford|hours a year|french paragliding team|ozone paragliders|brand|1990s|changed since|"
     r"ground handling|tactics", "Pilots and the industry"),
]


def topic_of(q):
    low = q.lower()
    for rx, t in TOPIC_RULES:
        if re.search(rx, low):
            return t
    return "More questions"


def az_items():
    items = []
    for a in ENTRIES:
        if not listed(a):
            continue
        cat, _, stitle = breadcrumb_of(a["series"])
        items.append({"q": a["q"], "href": "%s.html" % a["slug"], "where": stitle, "cat": cat,
                      "topic": a["topic"], "deep": True})
    for f in FAQS:
        items.append(dict(f, topic=topic_of(f["q"]), deep=False))
    return items


def index_page():
    items = az_items()
    groups = {}
    for it in items:
        groups.setdefault(it["topic"], []).append(it)
    names = sorted(groups, key=lambda t: (t == "More questions", t.lower()))
    letters, body = [], ""
    for name in names:
        g = sorted(groups[name], key=lambda it: (not it["deep"], it["q"].lower()))
        gid = "t-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        L = name[0].upper()
        if L not in [x for x, _ in letters] and name != "More questions":
            letters.append((L, gid))
        lis = "".join('<li class="%s" data-cat="%s"><a href="%s">%s</a><span class="m">%s</span>%s</li>'
                      % ("deep" if it["deep"] else "", it["cat"], it["href"], E(it["q"]), E(it["where"]),
                         '<span class="b">In depth</span>' if it["deep"] else "") for it in g)
        n_deep = sum(1 for it in g if it["deep"])
        sub = "%d %s%s" % (len(g), "question" if len(g) == 1 else "questions",
                           (", %d in depth" % n_deep) if n_deep else "")
        body += ('<section class="az-group" id="%s" data-topic="%s"><h2>%s<small>%s</small></h2>'
                 '<ul class="az-list">%s</ul></section>' % (gid, E(name, True), E(name), sub, lis))
    n_deep = sum(1 for it in items if it["deep"])
    chips = '<button class="az-chip" type="button" data-cat="" aria-pressed="true">All</button>' + "".join(
        '<button class="az-chip" type="button" data-cat="%s" aria-pressed="false">%s</button>' % (c, t)
        for c, t in CAT_SHORT.items())
    chips += '<button class="az-chip" type="button" data-deep="1" aria-pressed="false">In depth only</button>'
    letter_bar = "".join('<a href="#%s">%s</a>' % (gid, L) for L, gid in letters)
    hero = ('<header class="k-hero a-hero az-hero"><div class="k-hero-copy">'
            '<p class="breadcrumb"><a href="../../knowledge-base.html">Knowledge Base</a> / Encyclopedia</p>'
            '<span class="kicker">Encyclopedia · A to Z</span><h1>Every Paragliding Question, Answered</h1>'
            '<p class="lead">Every question the Knowledge Base answers, from how a wing flies to how a race is '
            'scored. In-depth answers are built from open sources and the show; short answers come from the '
            'guests, linked to the chapter where they say it.</p>'
            '<div class="k-stats"><span><b>%d</b>questions</span><span><b>%d</b>in depth</span>'
            '<span><b>%d</b>topics</span></div></div></header>' % (len(items), n_deep, len(names)))
    tools = ('<div class="az-tools"><label class="az-count" for="az-q">Search the questions</label>'
             '<input class="az-search" id="az-q" type="search" placeholder="Try collapse, thermal, reserve, EN B" '
             'autocomplete="off"><div class="az-chips" role="group" aria-label="Filter by category">%s</div>'
             '<nav class="az-letters" aria-label="Topics A to Z">%s</nav><p class="az-count" id="az-n" '
             'aria-live="polite"></p></div>' % (chips, letter_bar))
    ask = ('<p class="az-ask">Cannot find your question? <a href="mailto:aninder@paraglidingatlas.com">Ask me</a> '
           'and it may become the next answer.</p>')
    script = """<script>
(function () {
  var d = document, q = d.getElementById("az-q"), n = d.getElementById("az-n"), cat = "", deep = false;
  var lis = [].slice.call(d.querySelectorAll(".az-list li")), groups = [].slice.call(d.querySelectorAll(".az-group"));
  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, ""); }
  lis.forEach(function (li) { li._t = norm(li.textContent + " " + li.parentNode.parentNode.dataset.topic); });
  function run() {
    var words = norm(q.value).split(/\\s+/).filter(Boolean), shown = 0;
    lis.forEach(function (li) {
      var ok = (!cat || li.dataset.cat === cat) && (!deep || li.classList.contains("deep")) &&
        words.every(function (w) { return li._t.indexOf(w) > -1; });
      li.hidden = !ok; if (ok) shown++;
    });
    groups.forEach(function (g) { g.hidden = !g.querySelector(".az-list li:not([hidden])"); });
    n.textContent = shown + (shown === 1 ? " question" : " questions");
    d.querySelector(".az-empty").style.display = shown ? "none" : "block";
  }
  q.addEventListener("input", run);
  [].forEach.call(d.querySelectorAll(".az-chip"), function (b) {
    b.addEventListener("click", function () {
      if (b.dataset.deep) { deep = !deep; b.setAttribute("aria-pressed", deep); }
      else {
        cat = b.dataset.cat;
        [].forEach.call(d.querySelectorAll(".az-chip[data-cat]"), function (x) { x.setAttribute("aria-pressed", x === b); });
      }
      run();
    });
  });
  run();
})();
</script>"""
    body_html = (hero + '<section class="k-sec bg" id="a-to-z">' + tools + '<div class="az-body">' + body
                 + '<p class="az-empty">No question matches that yet.</p></div>' + ask + "</section>")
    page = "knowledge-base/encyclopedia/index.html"
    canonical = cfg.public_url(page)
    title = "Paragliding Questions Answered, A to Z" + SUFFIX
    desc = ("Every paragliding question the Paragliding Atlas Knowledge Base answers, A to Z: in-depth answers with "
            "sources, and short answers from the guests on the show.")
    deep_items = [it for it in items if it["deep"]]
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "url": canonical, "name": title,
                     "description": desc, "inLanguage": "en",
                     "isPartOf": {"@type": "WebSite", "name": "Paragliding Atlas", "url": cfg.BASE},
                     "mainEntity": {"@type": "ItemList", "numberOfItems": len(deep_items),
                                    "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": it["q"],
                                                         "url": cfg.url("knowledge-base/encyclopedia/" + it["href"])}
                                                        for i, it in enumerate(deep_items)]}},
                    ensure_ascii=False, indent=1)
    # Until at least one answer is published nothing links here, so it stays out of the index.
    out = (head(title, desc, canonical, cfg.url("assets/images/kb-technical.jpg"), ld, n_deep == 0)
           + deeper(HEAD_TAIL).format(css=CSS, body=body_html) + deeper(NAV_FOOTER))
    out = out.replace("</body>", JS + "\n" + script + "\n</body>", 1)
    return page, out, len(items), n_deep


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    slugs = [a["slug"] for a in ENTRIES]
    if len(slugs) != len(set(slugs)):
        fail("duplicate slug")
    keep = {"index.html"}
    for a in ENTRIES:
        page, out = answer_page(a)
        open(page, "w", encoding="utf-8").write(out)
        keep.add(os.path.basename(page))
    page, out, n, n_deep = index_page()
    open(page, "w", encoding="utf-8").write(out)
    for f in os.listdir(OUT_DIR):           # an entry that was removed takes its page with it
        if f.endswith(".html") and f not in keep:
            os.remove(os.path.join(OUT_DIR, f))
    drafts = sum(1 for a in ENTRIES if a["status"] == "draft")
    print("encyclopedia: %d answer pages (%d draft), A to Z of %d questions, %d in depth%s"
          % (len(ENTRIES), drafts, n, n_deep, " [drafts shown]" if SHOW_DRAFTS else ""))


if __name__ == "__main__":
    main()
