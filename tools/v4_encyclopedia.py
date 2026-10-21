#!/usr/bin/env python3
"""
The encyclopedia in v4 (owner, 21 Oct 2026: "can we also connect the encyclopedia build", then, of the
two ways in: "for now let it stay accessible through knowledge base"). The Flying Atlas globe, the other
way in, waits for later (owner: "leave this one for later").

    python3 tools/v4_encyclopedia.py pages   # v4_build step 2: the pages, as v4 twins of the review copy
    python3 tools/v4_encyclopedia.py links   # after v4_ux: the ways into them from the knowledge base

The source is the encyclopedia's review copy, prototypes/workspace/drafts/knowledge-base/encyclopedia/:
built on 10 Oct by generate_answer_pages.py on the encyclopedia-pilot branch with ENC_SHOW_DRAFTS=1 (the
drafts listed), from kb_answers.py there, its sources and an independent fact-check
(docs/encyclopedia/ on that branch). It is the A to Z of the 165 questions the knowledge base answers
and the ten Flight Mechanics answers, each marked "Draft for review" until the owner has reviewed it.
Not a word of it is written here; a change to an answer is made there and the review copy built again.

pages: each page of the review copy becomes the v4 twin a live knowledge base page gets from
tools/v2_twin.py (<body data-v2="kb">) at prototypes/v4/knowledge-base/encyclopedia/, and the chain
after it (v4_pass, v2_localize, v4_ux, ...) gives it v4's frame as it does every knowledge base page.
Three things are put back as a live build would have them: the workspace made the links to pages it
did not copy absolute (https://paraglidingatlas.com/...), so they are made relative again (the head's
canonical, og and structured data stay absolute); the workspace's robots line goes (v2_localize writes
v4's own); the three new drawings (kb-enc-*) are not in the live assets, so they are copied to
prototypes/v4/img/enc/ and pointed at there. One fix: the A to Z's search and filters changed only its
count (its list's display rules overrode [hidden]; the same on the branch). The A to Z also gets a line to "Tell me why"
(samples/tell-me-why.html, report row 16), the show's own answers. Written again on every build, so the
pages follow the review copy and nothing is edited in them by hand.

links: the encyclopedia is prototype-only until the owner has reviewed it (tools/v2_site.py proto_only),
so every way into it sits between v4:needs marks and the switch-over and the search leave it out:
  - the knowledge base page, after the climb's last level: the A to Z's own title, words and counts,
    and its ten answers, each with the first sentence of its short answer, as on the series page; its
    button opens the Atlas, the globe that leads into the encyclopedia (owner: "I want that button to
    take us to globe and then to this"; tools/v4_atlas.py, written by pages as atlas.html);
  - Flight Mechanics, where the ten are filed: the review copy's "Answered In Depth" strip and its way
    into the A to Z, before the next strip;
  - every series and section page the A to Z links into: its FAQ answers get the ids the A to Z links
    to (generate_answer_pages.py's kb_layout.faq_id) and a link landing on one opens it. A link with no
    answer to land on stops the build.
Idempotent: each part is written between its own marks and found again by them.
"""
import html
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
DRAFTS = os.path.join(ROOT, "prototypes", "workspace", "drafts")
SRC = os.path.join(DRAFTS, "knowledge-base", "encyclopedia")
OUT = os.path.join(V4, "knowledge-base", "encyclopedia")
IMG = os.path.join(V4, "img", "enc")
SITE = "https://paraglidingatlas.com/"
HERE = "knowledge-base/encyclopedia"
AZ = HERE + "/index.html"
NEED = ("<!-- v4:needs %s -->" % AZ, S.NEEDS_CLOSE)


def fail(msg):
    raise SystemExit("v4_encyclopedia: " + msg)


def faq_id(q):
    """The anchor of one FAQ answer, as kb_layout.faq_id on the encyclopedia-pilot branch writes it."""
    return "q-" + re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:70].rstrip("-")


# ── pages ───────────────────────────────────────────────────────────────────
def relative(m):
    """https://paraglidingatlas.com/<page>#x, written by the workspace, back to the live page's own link."""
    path, frag = (m.group(2).split("#", 1) + [""])[:2]
    page = path or "index.html"
    if not (os.path.isfile(os.path.join(ROOT, page)) or os.path.isfile(os.path.join(V4, page))):
        return m.group(0)
    return m.group(1) + os.path.relpath(page, HERE).replace(os.sep, "/") + ("#" + frag if frag else "") + '"'


ASK = ('<!-- v4:needs samples/tell-me-why.html --><p class="az-ask">Or ask the show: '
       '<a href="../../samples/tell-me-why.html">Tell me why</a> finds where the guests talk about it, '
       'in their own words, each linked to its chapter.</p><!-- /v4:needs -->')


def twin(name):
    src = open(os.path.join(SRC, name), encoding="utf-8").read()
    head, body = src.split("</head>", 1)
    head = head.replace('<head><meta name="robots" content="noindex,nofollow">', "<head>", 1)
    body = re.sub(r'(\s(?:href)=")' + re.escape(SITE) + r'([^"]*)"', relative, body)
    body = re.sub(r'\.\./\.\./assets/images/(kb-enc-[a-z0-9-]+)\.(webp|jpg)', r"../../img/enc/\1.\2", body)
    body, n = re.subn(r"<body(\s[^>]*)?>", lambda m: '<body data-v2="kb"%s>' % (m.group(1) or ""), body, count=1)
    if not n:
        fail("no <body> in " + name)
    if name == "index.html":
        # the A to Z's filter hides a question with [hidden], which its own display rules (.az-list li flex,
        # .az-group grid) overrode, so only the count changed; the same bug is on the encyclopedia-pilot branch
        head += "<style>.az-list li[hidden],.az-group[hidden]{display:none}</style>\n"
        if body.count('<p class="az-ask">') != 1:
            fail("the A to Z's closing line is not there")
        body = re.sub(r'(<p class="az-ask">.*?</p>)', lambda m: m.group(1) + ASK, body, count=1, flags=re.S)
    if SITE in body.replace('href="' + SITE + '"', ""):
        left = sorted(set(re.findall(re.escape(SITE) + r'[^"\s<]*', body)))
        fail("%s: links to the site that have no page here: %s" % (name, left[:5]))
    return head + "</head>" + body


def pages():
    names = sorted(f for f in os.listdir(SRC) if f.endswith(".html"))
    if "index.html" not in names or len(names) < 2:
        fail("the review copy is not at " + os.path.relpath(SRC, ROOT))
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(IMG, exist_ok=True)
    for f in sorted(os.listdir(os.path.join(DRAFTS, "assets", "images"))):
        if f.startswith("kb-enc-"):
            a, b = os.path.join(DRAFTS, "assets", "images", f), os.path.join(IMG, f)
            if not os.path.exists(b) or open(a, "rb").read() != open(b, "rb").read():
                shutil.copyfile(a, b)
    import v4_atlas
    made = {name: twin(name) for name in names}
    made["atlas.html"] = v4_atlas.page(made["index.html"], SRC)    # the globe, the way in (tools/v4_atlas.py)
    for name, out in made.items():
        fp = os.path.join(OUT, name)
        if not os.path.exists(fp) or open(fp, encoding="utf-8").read() != out:
            open(fp, "w", encoding="utf-8").write(out)
    for f in os.listdir(OUT):            # a page the review copy dropped goes too
        if f.endswith(".html") and f not in made:
            os.remove(os.path.join(OUT, f))
    print("v4_encyclopedia: %d pages from the review copy (the A to Z and %d answers) and the Atlas"
          % (len(names), len(names) - 1))


# ── links ───────────────────────────────────────────────────────────────────
def answers():
    """The ten answers as the A to Z lists them: (href from the knowledge base, kicker, question, first sentence)."""
    fm = open(os.path.join(DRAFTS, "knowledge-base", "flight-mechanics.html"), encoding="utf-8").read()
    m = re.search(r'<section class="k-sec bg" id="in-depth">.*?</section>', fm, re.S)
    if not m:
        fail("the review copy's Flight Mechanics has no in-depth strip")
    cards = re.findall(r'<a class="nx-card" href="(encyclopedia/[a-z0-9-]+\.html)"><span class="kicker">([^<]*)</span>'
                       r'<strong>([^<]*)</strong><em>([^<]*)</em></a>', m.group(0))
    if not cards:
        fail("no answers in the in-depth strip")
    return m.group(0), cards


STRIP_CSS = (
    # the review copy's own lines for the strip (templates/kb/category.css on the encyclopedia-pilot branch)
    "#in-depth .nx-depth{grid-template-columns:repeat(3,minmax(0,1fr));}"
    "#in-depth .nx-depth em{font-size:var(--fs-small);}"
    ".az-link{max-width:1300px;margin:1.6rem auto 0;}"
    ".az-link a{color:var(--orange);text-decoration:none;font-weight:600;font-size:var(--fs-body-s);}"
    ".az-link a:hover{text-decoration:underline;}"
    "@media(max-width:980px){#in-depth .nx-depth{grid-template-columns:1fr 1fr;}}"
    "@media(max-width:600px){#in-depth .nx-depth{grid-template-columns:1fr;}}"
)
OPEN = ("<!--v4e:open-->", "<!--/v4e:open-->")
OPEN_JS = ('<script>(function(){function open(){var id=decodeURIComponent(location.hash.slice(1)),'
           'el=id&&document.getElementById(id);if(el&&el.tagName==="DETAILS")el.open=true;}'
           'open();window.addEventListener("hashchange",open);})();</script>')
STRIP = ("<!--v4e:depth-->", "<!--/v4e:depth-->")
BAND = ("<!--v4e:band-->", "<!--/v4e:band-->")


def cut(src, marks):
    """The part between the marks, and the line end written after it."""
    return re.sub(re.escape(marks[0]) + r".*?" + re.escape(marks[1]) + r"\n?", "", src, flags=re.S)


def ids(src, rel):
    """Every FAQ answer on the page gets its anchor."""
    def one(m):
        q = html.unescape(re.sub(r"<[^>]+>", "", m.group(3)))
        return '<details id="%s"%s><summary><h3>%s</h3>' % (faq_id(q), m.group(2), m.group(3))
    return re.sub(r'<details(?: id="q-[a-z0-9-]*")?((\s+open)?)><summary><h3>(.*?)</h3>', lambda m: one(m), src)


def band(cards):
    """The way in from the knowledge base page: the A to Z's own kicker, title, words and counts (read from
    the review copy's header), and its answers."""
    src = open(os.path.join(SRC, "index.html"), encoding="utf-8").read()
    hd = re.search(r'<header class="k-hero[^"]*az-hero".*?</header>', src, re.S)
    hd = hd.group(0) if hd else ""
    k = re.search(r'<span class="kicker">([^<]*)</span>', hd)
    t = re.search(r'<h1[^>]*>(.*?)</h1>', hd, re.S)
    words = re.search(r'<p class="lead">(.*?)</p>', hd, re.S)
    stats = re.findall(r'<span><b>(\d+)</b>([^<]+)</span>', hd)
    if not (k and t and words and stats):
        fail("the A to Z's kicker, title, words or counts are not there")
    lis = "".join('<li><a href="%s"><span class="v4e-n">%02d</span><span class="v4e-k">%s</span><strong>%s</strong><em>%s</em></a></li>'
                  % (h, i + 1, kk, q, s) for i, (h, kk, q, s) in enumerate(cards))
    figs = "".join("<li><b>%s</b><span>%s</span></li>" % (n, w.strip()) for n, w in stats)
    return (BAND[0] + NEED[0] +
            '<section class="v4e-band" id="encyclopedia" aria-labelledby="v4eT"><div class="v4e-in">'
            '<div class="v4e-head"><span class="kit-kicker">%s</span><h2 class="kit-title" id="v4eT">%s</h2>'
            '<p class="kit-intro">%s</p><ul class="v4e-figs">%s</ul>'
            '<a class="btn-lines" href="knowledge-base/encyclopedia/atlas.html" data-hover>Explore the Atlas</a></div>'
            '<ol class="v4e-list">%s</ol></div></section>'
            % (k.group(1).strip(), t.group(1).strip(), words.group(1).strip(), figs, lis.replace('href="encyclopedia/', 'href="knowledge-base/encyclopedia/'))
            + NEED[1] + BAND[1])


BAND_CSS = (
    ".v4e-band{position:relative;padding:var(--sp-section) var(--gutter);border-top:1px solid var(--edge)}"
    ".v4e-in{max-width:1300px;margin:0 auto;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);"
    "gap:clamp(2rem,6vw,6rem);align-items:start}"
    ".v4e-head{position:sticky;top:calc(var(--nav-h,72px) + var(--sp-4))}"
    ".v4e-head .kit-intro{max-width:34rem}"
    ".v4e-figs{display:flex;gap:clamp(1.5rem,4vw,3rem);margin:var(--sp-4) 0;padding:var(--sp-3) 0 0;list-style:none;"
    "border-top:1px solid var(--edge)}"
    ".v4e-figs b{display:block;font-family:var(--font-display);font-weight:700;font-size:clamp(1.8rem,3.4vw,2.6rem);"
    "line-height:1;color:var(--white);font-variant-numeric:tabular-nums}"
    ".v4e-figs span{display:block;margin-top:.45rem;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gray-light)}"
    ".v4e-list{list-style:none;margin:0;padding:0;border-top:1px solid var(--edge)}"
    ".v4e-list a{display:grid;grid-template-columns:3rem minmax(0,1fr);column-gap:var(--sp-3);row-gap:.3rem;"
    "padding:var(--sp-3) 0;border-bottom:1px solid var(--edge);color:inherit;text-decoration:none;transition:padding .35s var(--ease)}"
    ".v4e-n{grid-row:span 3;font-family:var(--font-display);font-size:.85rem;color:var(--orange);padding-top:.2rem;font-variant-numeric:tabular-nums}"
    ".v4e-k{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gray)}"
    ".v4e-list strong{font-family:var(--font-display);font-size:clamp(1.05rem,1.6vw,1.3rem);color:var(--white);line-height:1.25}"
    ".v4e-list em{font-style:normal;color:var(--gray-light);font-size:var(--fs-small);line-height:1.5}"
    ".v4e-list a:is(:hover,:focus-visible){padding-left:.6rem}"
    ".v4e-list a:is(:hover,:focus-visible) strong{color:var(--orange)}"
    "@media (max-width:900px){.v4e-in{grid-template-columns:minmax(0,1fr)}.v4e-head{position:static}}"
    "@media (max-width:600px){.v4e-list a{grid-template-columns:2.2rem minmax(0,1fr)}.v4e-figs{gap:1.25rem}}"
    "@media (prefers-reduced-motion:reduce){.v4e-list a{transition:none}}"
)


def targets(az):
    """series page -> the ids the A to Z links to on it."""
    out = {}
    for page, frag in re.findall(r'href="\.\./([a-z0-9-]+\.html)#(q-[a-z0-9-]+)"', az):
        out.setdefault("knowledge-base/" + page, set()).add(frag)
    return out


def links():
    az = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
    strip, cards = answers()
    want = targets(az)
    done = []
    for rel in sorted(set(want) | {"knowledge-base/flight-mechanics.html", "knowledge-base.html"}):
        fp = os.path.join(V4, rel)
        if not os.path.isfile(fp):
            fail("the A to Z links to %s, which v4 does not have" % rel)
        src = open(fp, encoding="utf-8").read()
        out = cut(cut(cut(src, OPEN), STRIP), BAND)
        if rel in want:
            out = ids(out, rel)
            have = set(re.findall(r'<details id="(q-[a-z0-9-]+)"', out))
            miss = sorted(want[rel] - have)
            if miss:
                fail("%s: the A to Z links to answers it does not carry: %s" % (rel, miss[:3]))
            out = out.replace("</body>", OPEN[0] + OPEN_JS + OPEN[1] + "\n</body>", 1)
        if rel == "knowledge-base/flight-mechanics.html":
            i = out.find('id="questions"')
            j = out.find("</section>", i)
            if i < 0 or j < 0:
                fail("Flight Mechanics has no questions section")
            j += len("</section>")
            block = (STRIP[0] + NEED[0] + "<style>%s</style>" % STRIP_CSS + strip.replace(
                "</section>", '<p class="az-link"><a href="encyclopedia/index.html">'
                "Every question in the Knowledge Base, A to Z &rarr;</a></p></section>", 1) + NEED[1] + STRIP[1])
            out = out[:j] + block + out[j:]
        if rel == "knowledge-base.html":
            i = out.rfind("</main>")
            if i < 0:
                fail("the knowledge base page has no </main>")
            # after the climb's last level, inside <main>
            out = out[:i] + band(cards).replace(NEED[0], NEED[0] + "<style>%s</style>" % BAND_CSS, 1) + "\n" + out[i:]
        if out != src:
            open(fp, "w", encoding="utf-8").write(out)
            done.append(rel)
    print("v4_encyclopedia: ways in on %d pages (%d series pages with their answers' ids)" % (len(done), len(want)))


if __name__ == "__main__":
    what = sys.argv[1:] or ["pages"]
    if what[0] == "pages":
        pages()
    elif what[0] == "links":
        links()
    else:
        fail("say pages or links")
