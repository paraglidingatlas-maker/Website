#!/usr/bin/env python3
"""
The site in other languages (chat 27, 17 Nov 2026): German, French, Spanish, Simplified Chinese.

English is the source of truth. Every translated page is generated from the BUILT English page in
prototypes/v4 and is never edited by hand. The method (docs/v4-i18n.md has it in full):

  1. Segments. The English page is cut into segments: a block's text with its inline markup turned into
     placeholders (<x1>..</x1>, <x2/>), and the visible attributes (alt, title, aria-label, placeholder,
     meta descriptions, ...). Each segment is keyed by a hash of its locked English form; the translations
     live in tools/data/i18n/<lang>.json. A changed English segment gets a new key, so its old translation
     no longer applies (stale) and the page is not written until it is translated and checked again.
  2. Locked tokens. Numbers, dates, prices, URLs, emails and the names in tools/data/i18n/keep.txt are
     swapped for {1}, {2} ... before translating and put back after, by code: numbers and dates in the
     language's own format (CLDR, via babel), everything else verbatim. A translation that drops, adds or
     duplicates a token, or carries a digit of its own, fails.
  3. Glossary. tools/data/i18n/glossary.json, each term with its source (DHV, FFVL, ...). A segment that
     uses an English term must use the language's sourced term. Country names must be CLDR's.
  4. Review. Two independent translations (a, b), a third pass that picks or merges (tr), a blind
     back-translation into English (back), and a comparison of back with the English (check = "ok" or the
     reason it is not). Only "ok" segments are published.
  5. Pages whose English is binding (config english_binding) are not translated: see the plan.
  6. Every translated page says it is translated from English, links its English page and the
     corrections page ("Report a translation error").
  7. /de/, /fr/, /es/, /zh/; html lang; hreflang both ways; a language menu in the nav.

Commands:
  python3 tools/v4_i18n.py jobs           write tools/data/i18n/work/<lang>-todo.json: what still needs translating
  python3 tools/v4_i18n.py ingest LANG STAGE FILE   take an agent's output (STAGE a|b|tr|back|check) into <lang>.json
  python3 tools/v4_i18n.py prep LANG STAGE OUT [PAGE]   one pass's input (translate|review|back|compare), blind for back
  python3 tools/v4_i18n.py build          write every page whose segments all pass; mark the English pages
  python3 tools/v4_i18n.py check          the check report: tools/data/i18n/report.md (and .json); exit 1 on a FAIL
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
DATA = os.path.join(ROOT, "tools", "data", "i18n")
WORK = os.path.join(DATA, "work")
CFG = json.load(open(os.path.join(DATA, "config.json"), encoding="utf-8"))
LANGS = CFG["langs"]

# ---------------------------------------------------------------- tokenizer
RAW = re.compile(r"<!--.*?-->|<(script|style|textarea|svg|template|code|pre|kbd)\b[^>]*>.*?</\1\s*>|<![^>]*>|<[^>]+>|[^<]+", re.S | re.I)
INLINE = {"a", "abbr", "b", "bdi", "bdo", "br", "cite", "data", "dfn", "em", "i", "mark", "q", "s", "small",
          "span", "strong", "sub", "sup", "time", "u", "var", "wbr", "img"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
TAGNAME = re.compile(r"<\s*(/?)\s*([a-zA-Z][\w:-]*)")
# attributes that people read (data-l: the phone's column labels; data-lines: the home's headline variants, | between)
ATTRS = ("alt", "title", "aria-label", "placeholder", "aria-description", "data-share-title", "data-l", "data-lines",
         "aria-roledescription", "label")
META_NAMES = {"description", "og:title", "og:description", "twitter:title", "twitter:description", "og:image:alt",
              "twitter:image:alt", "apple-mobile-web-app-title"}
SKIP_CLASSES = {"rt-m", "sl-m", "word", "nav-coords", "notranslate", "gr-fn", "gr-ln", "gr-meta", "gr-rc-n", "gr-lp"}
I18N_BLOCK = re.compile(r"[ \t]*<!--i18n-->.*?<!--/i18n-->\n?", re.S)    # with its own indent, so a rebuild adds none


def tokens(src):
    out = []
    for m in RAW.finditer(src):
        t = m.group(0)
        if m.group(1) or t.startswith("<!"):
            out.append(("raw", t, None))
        elif t.startswith("<"):
            n = TAGNAME.match(t)
            if not n:
                out.append(("raw", t, None))
            else:
                end, name = n.group(1) == "/", n.group(2).lower()
                out.append(("end" if end else "tag", t, name))
        else:
            out.append(("text", t, None))
    return out


# ---------------------------------------------------------------- locking
MONTHS = {m: i + 1 for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                           "september", "october", "november", "december"])}
MON3 = {k[:3]: v for k, v in MONTHS.items()}
MON3["sept"] = 9
MONRX = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
DATE_RX = [
    ("dmdmy", re.compile(r"\b(\d{1,2}) (%s)\.? (?:to|–|-) (\d{1,2}) (%s)\.?(?: (\d{4}))?\b" % (MONRX, MONRX))),
    ("ddmy", re.compile(r"\b(\d{1,2}) ?(?:to|–|-) ?(\d{1,2}) (%s)\.?(?: (\d{4}))?\b" % MONRX)),
    ("dmy", re.compile(r"\b(\d{1,2}) (%s)\.?(?: (\d{4}))?\b" % MONRX)),
    ("my", re.compile(r"\b((?:January|February|March|April|May|June|July|August|September|October|November|December)) (\d{4})\b")),
]
URL_RX = re.compile(r"https?://[^\s<>\"']+|www\.[^\s<>\"']+|[\w.+-]+@[\w-]+\.[\w.-]+\w")
NUM_RX = re.compile(r"(?<![\w.,])(?:US\$|[$€£₹])?\d+(?:[,.:]\d+)*(?:(?![\w])|(?=(?:km|m|h|min|kg)(?![\w])))")     # 1,500m: the number, the unit stays
TOKEN_RX = re.compile(r"\{(\d+)\}")
TAG_PH = re.compile(r"</?x(\d+)/?>")


def keep_names():
    p = os.path.join(DATA, "keep.txt")
    names = []
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.split("#")[0].strip()
            if line:
                names.append(line)
    names.append("[to supply]")
    return sorted(set(names), key=len, reverse=True)


KEEP = keep_names()
KEEP_RX = re.compile("|".join(r"(?<![\w])%s(?![\w])" % re.escape(n) for n in KEEP)) if KEEP else None


def month_of(s):
    s = s.lower().rstrip(".")
    return MONTHS.get(s) or MON3.get(s[:4] if s.startswith("sept") else s[:3])


def lock_text(text, toks):
    """Swap the facts in a plain text for {n}; toks gets (kind, value) per n."""
    spans = []

    def take(rx, kind):
        for m in rx.finditer(text):
            if any(a < m.end() and m.start() < b for a, b, _, _ in spans):
                continue
            spans.append((m.start(), m.end(), kind, m))
    take(URL_RX, "url")
    take(re.compile(r"(?<![\w])[A-Za-z0-9]+(?:_[A-Za-z0-9]+)+(?![\w])"), "keep")     # file names: SRS_6_T1_4
    for kind, rx in DATE_RX:
        take(rx, kind)
    if KEEP_RX:
        take(KEEP_RX, "keep")
    take(LICENCE_RX, "keep")      # CC BY-SA 4.0: a licence's version, never a decimal (chat 28)
    take(BIG_RX, "big")
    take(DECADE_RX, "decade")
    take(ORD_RX, "ord")
    take(NUM_RX, "num")
    take(re.compile(r"[{}<>]"), "keep")
    spans.sort()
    out, pos = [], 0
    for a, b, kind, m in spans:
        out.append(text[pos:a])
        toks.append((kind, m.group(0)))
        out.append("{%d}" % len(toks))
        pos = b
    out.append(text[pos:])
    return "".join(out)


def fmt_num(v, lang):
    from babel.numbers import format_decimal
    s = v
    cur = ""
    m = re.match(r"(US\$|[$€£₹])(.*)$", v)
    if m:
        cur, s = m.group(1), m.group(2)
    if ":" in s or not re.match(r"^\d{1,3}(?:,\d{3})+(?:\.\d+)?$|^\d+\.\d+$", s):
        return v
    dec = len(s.split(".")[1]) if "." in s else 0
    n = float(s.replace(",", ""))
    out = format_decimal(n, format="#,##0" + ("." + "0" * dec if dec else ""), locale=LANGS[lang]["babel"])
    if lang == "es" and "." not in s and re.match(r"^\d,\d{3}$", s):
        out = s.replace(",", ".")          # 1.200: Spanish groups four digits too in prices and heights (RAE)
    return cur + out


def fmt_date(kind, v, lang):
    from babel.dates import format_skeleton, format_interval
    loc = LANGS[lang]["babel"]
    m = dict(DATE_RX)[kind].fullmatch(v)
    if not m:
        return v
    g = m.groups()
    try:
        if kind == "my":
            d = datetime.date(int(g[1]), month_of(g[0]), 1)
            return format_skeleton("yMMMM", d, locale=loc)
        if kind == "dmy":
            full = len(g[1].rstrip(".")) > 4 or g[1] in ("May", "June", "July")
            y = int(g[2]) if g[2] else 2027
            d = datetime.date(y, month_of(g[1]), int(g[0]))
            sk = ("y" if g[2] else "") + ("MMMM" if full else "MMM") + "d"
            return format_skeleton(sk, d, locale=loc)
        if kind == "ddmy":
            y = int(g[3]) if g[3] else 2027
            mo = month_of(g[2])
            a, b = datetime.date(y, mo, int(g[0])), datetime.date(y, mo, int(g[1]))
            sk = ("y" if g[3] else "") + ("MMMM" if len(g[2]) > 4 or g[2] in ("May", "June", "July") else "MMM") + "d"
            return format_interval(a, b, sk, locale=loc)
        if kind == "dmdmy":
            y = int(g[4]) if g[4] else 2027
            a, b = datetime.date(y, month_of(g[1]), int(g[0])), datetime.date(y, month_of(g[3]), int(g[2]))
            sk = ("y" if g[4] else "") + "MMMd"
            return format_interval(a, b, sk, locale=loc)
    except ValueError:
        return v
    return v


DECADE_RX = re.compile(r"(?<![\w])\d{3}0s(?![\w])")     # the 1960s: one locked fact, written the language's way
DECADE = {"de": "%ser", "fr": "années %s", "es": "años %s", "zh": "%s年代"}


ORD_RX = re.compile(r"(?<![\w])\d+(?:st|nd|rd|th)(?![\w])")     # 7th: an ordinal, written the language's way
ORD = {"de": "%s.", "fr": "%se", "es": "%s.º", "zh": "第%s"}


LICENCE_RX = re.compile(r"(?:(?<=CC BY )|(?<=CC BY-SA )|(?<=CC BY-ND )|(?<=CC BY-NC )|(?<=CC BY-NC-SA )|(?<=CC0 ))\d\.\d(?![\w.])")
BIG_RX = re.compile(r"(?<![\w.,])\d+(?:\.\d+)? (?:million|billion)(?![\w-])")   # 1.4 billion: one fact (zh 14亿)


def fmt_big(v, lang):
    from babel.numbers import format_compact_decimal
    num, word = v.split(" ")
    n = float(num) * (1e6 if word == "million" else 1e9)
    dec = len(num.split(".")[1]) if "." in num else 0
    return format_compact_decimal(n, format_type="short" if lang == "zh" else "long",
                                  locale=LANGS[lang]["babel"], fraction_digits=dec)


def render_tok(kind, v, lang):
    if kind == "big":
        return fmt_big(v, lang) if lang in LANGS else v
    if kind == "ord":
        n = v[:-2]
        return ("1er" if lang == "fr" and n == "1" else ORD.get(lang, "%s") % n) if lang in ORD else v
    if kind == "decade":
        return DECADE.get(lang, "%ss") % v[:-1]
    if kind == "num":
        return fmt_num(v, lang)
    if kind in dict(DATE_RX):
        return fmt_date(kind, v, lang)
    return v


# ---------------------------------------------------------------- segments
def letters(s):
    return len(re.findall(r"[A-Za-z]", s))


def translatable(prot):
    bare = TAG_PH.sub(" ", TOKEN_RX.sub(" ", prot))
    return letters(bare) >= 2


def seg_key(prot):
    return hashlib.sha1(prot.encode("utf-8")).hexdigest()[:12]


class Seg:
    """One segment on one page: its locked English, the tags and the token values of this occurrence."""
    def __init__(self, prot, tags, toks, where):
        self.prot, self.tags, self.toks, self.where = prot, tags, toks, where
        self.key = seg_key(prot)


def text_seg(raw_text, where):
    toks = []
    t = " ".join(html.unescape(raw_text).split())
    return Seg(lock_text(t, toks), [], toks, where)


def run_seg(run, where):
    """run: tokens (text / inline tags). Returns a Seg or None when the inline tags do not balance."""
    tags, toks, parts, stack = [], [], [], []
    opens = 0
    for kind, t, name in run:
        if kind == "text":
            parts.append(lock_text(html.unescape(t), toks).replace("\n", " "))
        elif kind == "tag":
            tags.append(t)
            opens += 1
            n = opens
            if name in VOID or t.rstrip().endswith("/>"):
                parts.append("<x%d/>" % n)
            else:
                stack.append((name, n))
                parts.append("<x%d>" % n)
        else:
            if not stack or stack[-1][0] != name:
                return None
            _, n = stack.pop()
            tags.append(t)
            parts.append("</x%d>" % n)
    if stack:
        return None
    prot = re.sub(r"[ \t\r\f\v\n]+", " ", "".join(parts)).strip()
    return Seg(prot, tags, toks, where)


def attr_rx(name):
    return re.compile(r'(\s%s=")([^"]*)(")' % re.escape(name))


def classes_of(tag):
    m = re.search(r'\sclass="([^"]*)"', tag)
    return set(m.group(1).split()) if m else set()


FACTS_LANG = [None]


def facts_only(t):
    """Text with no words (a price alone, "2,400 m"): its numbers and dates in the language's own format,
    while a page is being built; unchanged otherwise."""
    lang = FACTS_LANG[0]
    if not lang or not re.search(r"\d", t):
        return t
    toks = []
    prot = lock_text(html.unescape(t), toks)
    if not toks:
        return t
    out = TOKEN_RX.sub(lambda m: render_tok(*toks[int(m.group(1)) - 1], lang), prot)
    return t if html.unescape(t) == out else html.escape(out, quote=False)


def is_skip(tag):
    return bool(classes_of(tag) & SKIP_CLASSES) or 'translate="no"' in tag


def process(body, page, visit_text):
    """A run of text and inline tags -> its output. A run with text of its own at the top is one segment;
    a run of elements only (a nav's links, a label and its value) is taken element by element."""
    if not any(x[0] == "text" and letters(x[1]) for x in body):
        return "".join(facts_only(x[1]) if x[0] == "text" else x[1] for x in body)
    # the top-level items
    items, i, n = [], 0, len(body)
    while i < n:
        k, t, name = body[i]
        if k == "tag" and not (name in VOID or t.rstrip().endswith("/>")):
            depth, j = 0, i
            while j < n:
                kj, _, nj = body[j]
                if kj == "tag" and nj == name and not body[j][1].rstrip().endswith("/>"):
                    depth += 1
                elif kj == "end" and nj == name:
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j >= n:
                return visit_text(body, page) or "".join(facts_only(x[1]) if x[0] == "text" else x[1] for x in body)     # unbalanced: per text
            items.append(("el", body[i:j + 1]))
            i = j + 1
        elif k == "end":
            r = visit_text(body, page)
            return r if r is not None else "".join(facts_only(x[1]) if x[0] == "text" else x[1] for x in body)
        else:
            items.append(("x", [body[i]]))
            i += 1
    own_text = any(kind == "x" and it[0][0] == "text" and it[0][1].strip() for kind, it in items)
    if own_text:
        r = visit_text(body, page)
        return r if r is not None else "".join(facts_only(x[1]) if x[0] == "text" else x[1] for x in body)
    out = []
    for kind, it in items:
        if kind == "x":
            out.append(it[0][1])
        elif is_skip(it[0][1]):
            out.append("".join(x[1] for x in it))
        else:
            inner = it[1:-1]
            lead = trail = ""
            inner2 = list(inner)
            if inner2 and inner2[0][0] == "text":
                t0 = inner2[0][1]
                lead = t0[:len(t0) - len(t0.lstrip())]
                inner2[0] = ("text", t0.lstrip(), None)
            if inner2 and inner2[-1][0] == "text":
                t1 = inner2[-1][1]
                trail = t1[len(t1.rstrip()):]
                inner2[-1] = ("text", t1.rstrip(), None)
            inner2 = [x for x in inner2 if not (x[0] == "text" and x[1] == "")]
            out.append(it[0][1] + lead + process(inner2, page, visit_text) + trail + it[-1][1])
    return "".join(out)


def walk(src, page, visit_text, visit_attr):
    """Walk an English page. visit_text(run_tokens, where) -> replacement or None; visit_attr(value, where) ->
    replacement or None. Returns the page with the replacements."""
    toks = tokens(src)
    out, run, stack = [], [], []
    skip_depth = [0]

    def in_skip():
        return any(s[1] for s in stack)

    def flush():
        if not run:
            return
        r = list(run)
        run.clear()
        # leading/trailing whitespace stays outside the segment
        lead = trail = ""
        if r[0][0] == "text":
            lead = r[0][1][:len(r[0][1]) - len(r[0][1].lstrip())]
        if r[-1][0] == "text":
            t = r[-1][1]
            trail = t[len(t.rstrip()):]
        body = [x for x in r]
        if body and body[0][0] == "text":
            body[0] = ("text", body[0][1].lstrip(), None)
        if body and body[-1][0] == "text":
            body[-1] = ("text", body[-1][1].rstrip(), None)
        body = [x for x in body if not (x[0] == "text" and x[1] == "")]
        if in_skip():
            out.append("".join(x[1] for x in r))
            return
        if not any(x[0] == "text" and letters(x[1]) for x in body):
            out.append("".join(facts_only(x[1]) if x[0] == "text" else x[1] for x in r))
            return
        out.append(lead + process(body, page, visit_text) + trail)

    for kind, t, name in toks:
        if kind == "tag":
            t = translate_attrs(t, name, page, visit_attr, in_skip())
            if name in INLINE:
                run.append(("tag", t, name))
                if name not in VOID and not t.rstrip().endswith("/>"):
                    stack.append((name, bool(classes_of(t) & SKIP_CLASSES) or 'translate="no"' in t))
                continue
            flush()
            out.append(t)
            if name not in VOID and not t.rstrip().endswith("/>"):
                stack.append((name, bool(classes_of(t) & SKIP_CLASSES) or 'translate="no"' in t))
        elif kind == "end":
            if name in INLINE:
                run.append(("end", t, name))
            else:
                flush()
                out.append(t)
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == name:
                    del stack[i:]
                    break
        elif kind == "text":
            run.append(("text", t, None))
        else:
            flush()
            out.append(visit_raw(t, page, visit_attr))
    flush()
    return "".join(out)


def visit_raw(t, page, visit_attr):
    # the loading screen's page name (v4_loader.py): {"k":"page","n":"Enquire"}
    m = re.match(r'(<script type="application/json" id="v4ld-c">)(.*?)(</script>)$', t, re.S)
    if m:
        try:
            c = json.loads(m.group(2))
        except ValueError:
            return t
        changed = False
        for k in ("n", "f", "w"):
            if isinstance(c.get(k), str) and letters(c[k]) >= 2:
                r = visit_attr(c[k], page + " (loader)")
                if r is not None:
                    c[k] = r
                    changed = True
        if changed:
            return m.group(1) + json.dumps(c, ensure_ascii=False, separators=(",", ":")) + m.group(3)
    return t


def translate_attrs(t, name, page, visit_attr, skip):
    if skip:
        return t
    if name == "meta":
        m = re.search(r'\s(?:name|property)="([^"]+)"', t)
        if not m or m.group(1) not in META_NAMES:
            return t
        names = ("content",)
    elif name == "input" and re.search(r'\stype="(?:submit|button|reset)"', t):
        names = ATTRS + ("value",)
    else:
        names = ATTRS
    for a in names:
        rx = attr_rx(a)
        mm = rx.search(t)
        if not mm or letters(mm.group(2)) < 2:
            continue
        val = html.unescape(mm.group(2))
        if a == "data-lines":
            parts = [visit_attr(p, page) for p in val.split("|")]
            if any(p is None for p in parts):
                continue
            new = "|".join(parts)
        else:
            new = visit_attr(val, page)
            if new is None:
                continue
        t = t[:mm.start()] + mm.group(1) + html.escape(new, quote=True).replace("&#x27;", "&#x27;") + mm.group(3) + t[mm.end():]
    return t


def page_segments(page):
    """Every segment of an English page, in order."""
    src = I18N_BLOCK.sub("", open(os.path.join(V4, page), encoding="utf-8").read())
    segs = []

    def vt(body, where):
        s = run_seg(body, where)
        if s is None:
            for k, t, _ in body:
                if k == "text" and letters(t) >= 2:
                    s2 = text_seg(t, where)
                    if translatable(s2.prot):
                        segs.append(s2)
            return None
        if translatable(s.prot):
            segs.append(s)
        return None

    def va(val, where):
        s = text_seg(val, where + " (attribute)")
        if translatable(s.prot):
            segs.append(s)
        return None
    walk(src, page, vt, va)
    return segs


def ui_segments():
    return [text_seg(u, "_ui") for u in CFG["ui"]]


def js_segments():
    """What the page's scripts write (config "js"): taken as written, {n} standing for any part (v4-i18n.js
    looks that part up again, or keeps it)."""
    out = []
    for u in CFG.get("js", []):
        n = len(TOKEN_RX.findall(u))
        out.append(Seg(u, [], [("wild", "{%d}" % (i + 1)) for i in range(n)], "_js"))
    return out


# ---------------------------------------------------------------- memory
def mem_path(lang):
    return os.path.join(DATA, "%s.json" % lang)


def load_mem(lang):
    p = mem_path(lang)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save_mem(lang, mem):
    with open(mem_path(lang), "w", encoding="utf-8") as fh:
        json.dump(dict(sorted(mem.items())), fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def glossary():
    p = os.path.join(DATA, "glossary.json")
    if not os.path.exists(p):
        return []
    return json.load(open(p, encoding="utf-8")).get("terms", [])


def gloss_rx(en):
    w = re.escape(en).replace(r"\ ", r"[\s-]+")
    return re.compile(r"(?<![\w])%s(?:s|es)?(?![\w])" % w, re.I)


COUNTRIES = None


def countries(lang):
    global COUNTRIES
    if COUNTRIES is None:
        from babel import Locale
        en = Locale.parse("en").territories
        COUNTRIES = {}
        for l, c in LANGS.items():
            loc = Locale.parse(c["babel"]).territories
            COUNTRIES[l] = [(en[k], loc[k]) for k in en if re.match(r"^[A-Z]{2}$", k) and k in loc
                            and en[k] in ("Kenya", "India", "Mexico", "Peru", "Kazakhstan", "Norway", "Spain",
                                          "Italy", "Colombia", "France", "Germany", "Switzerland", "Austria",
                                          "Nepal", "Brazil", "Argentina", "Chile", "Turkey", "Greece", "Portugal",
                                          "Slovenia", "Bulgaria", "Poland", "Japan", "United Kingdom",
                                          "United States", "Canada", "Australia", "New Zealand", "South Africa",
                                          "Morocco", "Macedonia", "Romania", "Czechia", "Belgium", "Netherlands",
                                          "Ecuador", "Bolivia", "Venezuela", "Uganda", "Tanzania", "Ethiopia")]
    return COUNTRIES[lang]


def check_seg(lang, en, tr):
    """The mechanical checks of one translation. Returns a list of problems (empty: it passes)."""
    p = []
    if not tr or not tr.strip():
        return ["empty"]
    a, b = sorted(TOKEN_RX.findall(en)), sorted(TOKEN_RX.findall(tr))
    if a != b:
        p.append("locked tokens differ: English %s, translation %s" % (a, b))
    ta, tb = sorted(TAG_PH.findall(en)), sorted(TAG_PH.findall(tr))
    if sorted(re.findall(r"</?x\d+/?>", en)) != sorted(re.findall(r"</?x\d+/?>", tr)):
        p.append("markup placeholders differ")
    else:
        stack = []
        for m in re.finditer(r"<(/?)x(\d+)(/?)>", tr):
            if m.group(3):
                continue
            if not m.group(1):
                stack.append(m.group(2))
            elif not stack or stack.pop() != m.group(2):
                p.append("markup placeholders badly nested")
                break
    bare = TAG_PH.sub("", TOKEN_RX.sub("", tr))
    if re.search(r"\d", bare) and not re.search(r"\d", TAG_PH.sub("", TOKEN_RX.sub("", en))):
        p.append("a digit that is not in the English")
    if re.search(r"[{}]", bare):
        p.append("a stray brace")
    ratio = len(bare) / max(1, len(TAG_PH.sub("", TOKEN_RX.sub("", en))))
    lo, hi = (0.12, 1.6) if lang == "zh" else (0.45, 2.6)
    if len(en) > 25 and not lo <= ratio <= hi:
        p.append("length %.2f of the English" % ratio)
    ebare = TAG_PH.sub("", TOKEN_RX.sub("", en)).strip()
    # three or more ordinary (lower-case) words the same as the English: names and countries alone do not count
    if len(re.findall(r"(?<![\w])[a-z][a-z']+", ebare)) >= 3 and ebare.lower() == bare.strip().lower():
        p.append("left in English")
    low = tr.lower()
    wl = wrong_lang(lang, bare)
    if wl:
        p.append("reads as %s" % wl)
    for term in glossary():
        g = term.get(lang) or {}
        want = g.get("term", "")
        if not want or want == "[to supply]" or not g.get("source"):
            continue
        if gloss_rx(term["en"]).search(TOKEN_RX.sub(" ", en)):
            forms = [want] + list(g.get("also", []))
            if not any(f.lower().split(" (")[0] in low for f in forms):
                p.append('glossary: "%s" should be "%s"' % (term["en"], want))
    for en_c, loc_c in countries(lang):
        if re.search(r"(?<![\w])%s(?![\w])" % re.escape(en_c), en) and loc_c.lower() not in low:
            p.append('country: "%s" is "%s" (CLDR)' % (en_c, loc_c))
    return p


STOP = {
    "de": {"und", "der", "die", "das", "nicht", "mit", "für", "ist", "ein", "eine", "du", "dein", "auf", "zu", "von", "den", "im"},
    "fr": {"et", "le", "la", "les", "des", "du", "un", "une", "pour", "avec", "est", "vous", "votre", "sur", "dans", "pas"},
    "es": {"y", "el", "la", "los", "las", "del", "un", "una", "para", "con", "es", "tu", "por", "en", "que", "no"},
    "en": {"the", "and", "with", "for", "your", "you", "is", "of", "to", "on", "in", "are", "this", "that", "not"},
}


def wrong_lang(lang, text):
    """A translation that reads as another language (a file mixed up between two passes)."""
    if lang == "zh":
        latin = len(re.findall(r"[A-Za-z]", text))
        han = len(re.findall(r"[\u4e00-\u9fff]", text))
        eng = sum(w in STOP["en"] for w in re.findall(r"[a-z]+", text.lower()))
        return "not Chinese" if latin > 12 and han == 0 and eng >= 2 else ""
    words = re.findall(r"[a-zäöüßéèêàçñáíóúœ]+", text.lower())
    if len(words) < 6:
        return ""
    score = {l: sum(w in st for w in words) for l, st in STOP.items()}
    best = max(score, key=score.get)
    if best != lang and score[best] >= 3 and score[best] > 2 * score.get(lang, 0):
        return {"de": "German", "fr": "French", "es": "Spanish", "en": "English"}[best]
    return ""


SOFT = ("left in English", "country", "glossary", "length")


def status(lang, rec):
    """'ok' (publishable), or why not."""
    if not rec or not rec.get("tr"):
        return "missing"
    if rec.get("check") != "ok":
        return "review: %s" % (rec.get("check") or "no back-translation check yet")
    probs = check_seg(lang, rec["en"], rec["tr"])
    # only the soft checks can be waived, each with its reason; locked facts, markup and language never
    waived = [w for w in rec.get("waive", {}) if w in SOFT]
    probs = [x for x in probs if not any(x.startswith(w) for w in waived)]
    return "ok" if not probs else "fails: " + "; ".join(probs)


# ---------------------------------------------------------------- jobs / ingest
def all_segments():
    by = {}
    for page in CFG["pages"]:
        for s in page_segments(page):
            by.setdefault(s.key, s)
    for s in ui_segments() + js_segments():
        by.setdefault(s.key, s)
    return by


def cmd_jobs():
    os.makedirs(WORK, exist_ok=True)
    segs = all_segments()
    for lang in LANGS:
        mem = load_mem(lang)
        todo = {k: {"en": s.prot, "where": s.where} for k, s in segs.items() if not (mem.get(k) or {}).get("tr")}
        with open(os.path.join(WORK, "%s-todo.json" % lang), "w", encoding="utf-8") as fh:
            json.dump(todo, fh, ensure_ascii=False, indent=1)
        print("%s: %d segments to translate, %d in memory" % (lang, len(todo), len(mem)))
    allp = {k: {"en": s.prot, "where": s.where} for k, s in segs.items()}
    with open(os.path.join(WORK, "all-segments.json"), "w", encoding="utf-8") as fh:
        json.dump(allp, fh, ensure_ascii=False, indent=1)
    words = sum(len(TAG_PH.sub(" ", TOKEN_RX.sub(" ", s.prot)).split()) for s in segs.values())
    print("%d segments, %d English words" % (len(segs), words))


def cmd_ingest(lang, stage, path):
    mem = load_mem(lang)
    data = json.load(open(path, encoding="utf-8"))
    segs = json.load(open(os.path.join(WORK, "all-segments.json"), encoding="utf-8"))
    n = 0
    for k, v in data.items():
        rec = mem.get(k)
        if rec is None:
            if k not in segs:
                print("  unknown segment %s (skipped)" % k)
                continue
            rec = mem[k] = {"en": segs[k]["en"]}
        if stage == "check":
            if isinstance(v, dict):
                rec["check"] = v.get("verdict", "")
                if v.get("note"):
                    rec["check_note"] = v["note"]
            else:
                rec["check"] = v
        elif stage == "tr" and isinstance(v, dict):
            rec["tr"] = v.get("tr", "")
            if v.get("note"):
                rec["tr_note"] = v["note"]
            if v.get("waive"):
                rec["waive"] = v["waive"]      # {"left in English": "a person's name"}: a soft check, with its reason
            else:
                rec.pop("waive", None)
            rec.pop("check", None)
            rec.pop("back", None)
        else:
            rec[stage] = v
            if stage == "tr":
                rec.pop("check", None)
                rec.pop("back", None)
        rec["date"] = datetime.date.today().isoformat()
        n += 1
    save_mem(lang, mem)
    print("%s %s: %d taken" % (lang, stage, n))


def cmd_prep(lang, stage, out, page=None):
    """The input file of one pass (chat 28): STAGE translate | review | back | compare, for the segments of
    PAGE (a path prefix, e.g. destinations/kenya.html) or of every page. back gets the translation only (blind)."""
    segs = all_segments()
    mem = load_mem(lang)
    res = {}
    for k, s in segs.items():
        if page and not s.where.startswith(page):
            continue
        r = mem.get(k) or {}
        facts = {"{%d}" % (i + 1): "%s: %s" % (kind, v) + ("" if render_tok(kind, v, lang) == v else
                 " (printed as: %s)" % render_tok(kind, v, lang)) for i, (kind, v) in enumerate(s.toks)}
        if stage == "translate" and not r.get("tr") and not r.get("a" if out.endswith("-a.json") else "b"):
            res[k] = {"en": s.prot, "where": s.where, "facts": facts}
        elif stage == "review" and not r.get("tr") and r.get("a") and r.get("b"):
            res[k] = {"en": s.prot, "where": s.where, "facts": facts, "a": r["a"], "b": r["b"]}
        elif stage == "back" and r.get("tr") and not r.get("back"):
            res[k] = r["tr"]
        elif stage == "compare" and r.get("tr") and r.get("back") and not r.get("check"):
            res[k] = {"en": s.prot, "facts": facts, "translation": r["tr"], "back": r["back"]}
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    print("%s %s: %d segments -> %s" % (lang, stage, len(res), out))


# ---------------------------------------------------------------- build
def out_rel(page, lang):
    return "%s/%s" % (LANGS[lang]["dir"], page)


def render(seg, tr, lang):
    """A translation with this occurrence's tags and facts put back, as HTML."""
    def piece(s):
        out, pos = [], 0
        for m in re.finditer(r"\{(\d+)\}", s):
            out.append(html.escape(s[pos:m.start()], quote=False))
            kind, v = seg.toks[int(m.group(1)) - 1]
            out.append(html.escape(render_tok(kind, v, lang), quote=False))
            pos = m.end()
        out.append(html.escape(s[pos:], quote=False))
        return "".join(out)
    out, pos = [], 0
    for m in re.finditer(r"<(/?)x(\d+)(/?)>", tr):
        out.append(piece(tr[pos:m.start()]))
        n = int(m.group(2))
        # the n-th opening tag and its closing tag were stored in order: find them by count
        out.append(tag_for(seg, n, bool(m.group(1))))
        pos = m.end()
    out.append(piece(tr[pos:]))
    return "".join(out)


def tag_for(seg, n, closing):
    # seg.tags holds tags in source order; opening tags are numbered 1.. in order of appearance
    opens, idx = 0, {}
    stack = []
    for i, t in enumerate(seg.tags):
        if t.startswith("</"):
            m = stack.pop()
            idx[(m, True)] = t
        else:
            opens += 1
            idx[(opens, False)] = t
            nm = TAGNAME.match(t).group(2).lower()
            if not (nm in VOID or t.rstrip().endswith("/>")):
                stack.append(opens)
    return idx[(n, closing)]


def plain(seg, tr, lang):
    """A translation as plain text (attributes)."""
    s = TAG_PH.sub("", tr)
    return TOKEN_RX.sub(lambda m: render_tok(*seg.toks[int(m.group(1)) - 1], lang), s)


def published(lang):
    """The pages that can be written in lang now: every segment passes."""
    mem = load_mem(lang)
    out, why = [], {}
    for page in CFG["pages"]:
        bad = []
        for s in page_segments(page) + ui_segments() + js_segments():
            st = status(lang, mem.get(s.key))
            if st != "ok":
                bad.append((s.key, st))
        if bad:
            why[page] = bad
        else:
            out.append(page)
    return out, why


def relink(src, page, lang, pages_here):
    """Links of the English page, from its new place in /<dir>/: one level deeper; a link to a page that is
    also written in this language stays inside the language."""
    d = LANGS[lang]["dir"]
    here = os.path.dirname(page)

    def fix(url):
        if not url or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#|/|\{|\$|%|data:)", url, re.I):
            return url
        m = re.match(r"([^?#]*)(.*)$", url)
        path, tail = m.group(1), m.group(2)
        if not path:
            return url
        target = os.path.normpath(os.path.join(here, path)).replace(os.sep, "/")
        if target in pages_here:
            return url
        return "../" + url
    src = re.sub(r'(\s(?:href|src|poster|data-src|data-v4-src|data-poster|data-loop|action)=")([^"]*)(")',
                 lambda m: m.group(1) + fix(m.group(2)) + m.group(3), src)
    src = re.sub(r'(\s(?:srcset|data-srcset|data-v4-srcset)=")([^"]*)(")',
                 lambda m: m.group(1) + ", ".join(" ".join([fix(c.strip().split(" ")[0])] + c.strip().split(" ")[1:])
                                                  for c in m.group(2).split(",") if c.strip()) + m.group(3), src)
    src = re.sub(r'(url\(([\"\']?))([^)\"\']+)(\2\))', lambda m: m.group(1) + fix(m.group(3)) + m.group(4), src)
    return src


def up(page):
    return "../" * page.count("/")


def lang_menu(page, cur, avail):
    """The language menu for the nav: English first, then every language this page is written in."""
    pre = up(page)
    items = []
    root = pre + ("../" if cur != "en" else "")
    for code in ["en"] + [l for l in LANGS if l in avail]:
        name = "English" if code == "en" else LANGS[code]["name"]
        hl = "en" if code == "en" else LANGS[code]["hreflang"]
        href = root + ("" if code == "en" else LANGS[code]["dir"] + "/") + page
        cur_attr = ' aria-current="true"' if code == cur else ""
        items.append('<li><a href="%s" hreflang="%s" lang="%s"%s>%s</a></li>' % (href, hl, hl, cur_attr, html.escape(name)))
    short = "EN" if cur == "en" else LANGS[cur]["short"]
    label = UI.get(cur, {}).get("Language", "Language")
    return ('<!--i18n--><details class="v4-lang"><summary aria-label="%s: %s"><svg viewBox="0 0 24 24" width="15" height="15" '
            'aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/>'
            '<path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>'
            '<span>%s</span></summary><ul>%s</ul></details><!--/i18n-->'
            % (html.escape(label), html.escape("English" if cur == "en" else LANGS[cur]["name"]), html.escape(short), "".join(items)))


UI = {}


def head_links(page, avail):
    out = []
    base = "https://paraglidingatlas.com/"
    name = "" if page == "index.html" else page
    out.append('<link rel="alternate" hreflang="en" href="%s%s">' % (base, name))
    for l in LANGS:
        if l in avail:
            out.append('<link rel="alternate" hreflang="%s" href="%s%s/%s">' % (LANGS[l]["hreflang"], base, LANGS[l]["dir"], name))
    out.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (base, name))
    return out


def mark_english(page, avail, write=True):
    """hreflang links and the language menu on the English page (taken out again when no language has it)."""
    p = os.path.join(V4, page)
    src = open(p, encoding="utf-8").read()
    new = I18N_BLOCK.sub("", src)
    if avail:
        new = add_marks(new, page, "en", avail)
    if new != src and write:
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(new)
    return new


def css_hash():
    return hashlib.sha1(open(os.path.join(V4, "v4-i18n.css"), "rb").read()).hexdigest()[:8]


def add_marks(src, page, cur, avail):
    pre = up(page) + ("../" if cur != "en" else "")
    block = "<!--i18n-->\n" + "\n".join(head_links(page, avail)) + \
            '\n<link rel="stylesheet" href="%sv4-i18n.css?v=%s">\n<!--/i18n-->\n' % (pre, css_hash())
    src = src.replace("</head>", block + "</head>", 1)
    menu = lang_menu(page, cur, avail)
    if '<a href="' in src and 'class="nav-cta"' in src:
        src = re.sub(r'(\n\s*)(<a [^>]*class="nav-cta")', lambda m: m.group(1) + menu + m.group(1) + m.group(2), src, count=1)
    return src


def js_dict(page, lang, mem):
    """The checked dictionary v4-i18n.js uses on this page: the page's own short plain segments (a script may
    write them again) and every script string (config "js")."""
    exact, pat = {}, []
    for s in page_segments(page) + js_segments():
        rec = mem.get(s.key) or {}
        if not rec.get("tr") or TAG_PH.search(s.prot) or len(s.prot) > 160:
            continue
        if s.where != "_js" and not TOKEN_RX.search(s.prot):
            exact[s.prot] = rec["tr"]
        elif s.where == "_js" and not TOKEN_RX.search(s.prot):
            exact[s.prot] = rec["tr"]
        elif s.where == "_js" or all(k in ("num", "keep") for k, _ in s.toks):
            if [s.prot, rec["tr"]] not in pat:
                pat.append([s.prot, rec["tr"]])
    pat.sort(key=lambda p: -len(p[0]))
    return {"lang": LANGS[lang]["html"], "exact": exact, "pat": pat}


def build_page(page, lang, avail_by_page, mem):
    src = I18N_BLOCK.sub("", open(os.path.join(V4, page), encoding="utf-8").read())
    L = LANGS[lang]
    # <option>: the form keeps sending, and its script keeps matching, the English (data-en; value when it had none)
    src = re.sub(r"<option(\s[^>]*)?>([^<]*)</option>", lambda m: "<option%s data-en=\"%s\">%s</option>" % (
        (m.group(1) or "") + ("" if m.group(1) and " value=" in m.group(1) else ' value="%s"' % m.group(2).strip()),
        m.group(2).strip(), m.group(2)), src)
    src = re.sub(r"\.options\[([^\]]+)\]\.text\b", lambda m: ".options[%s].dataset.en" % m.group(1), src)

    def vt(body, where):
        s = run_seg(body, where)
        if s is None:
            # unbalanced inline tags: translate each text alone
            res = []
            for k, t, _ in body:
                if k == "text" and letters(t) >= 2:
                    s2 = text_seg(t, where)
                    if translatable(s2.prot):
                        lead = t[:len(t) - len(t.lstrip())]
                        trail = t[len(t.rstrip()):]
                        res.append(lead + render(s2, mem[s2.key]["tr"], lang) + trail)
                        continue
                res.append(t)
            return "".join(res)
        if not translatable(s.prot):
            return None
        return render(s, mem[s.key]["tr"], lang)

    def va(val, where):
        s = text_seg(val, where)
        if not translatable(s.prot):
            return None
        return plain(s, mem[s.key]["tr"], lang)
    FACTS_LANG[0] = lang
    try:
        out = walk(src, page, vt, va)
    finally:
        FACTS_LANG[0] = None
    here_pages = {p for p, av in avail_by_page.items() if lang in av}
    out = relink(out, page, lang, here_pages)
    out, binding = mark_binding(out, lang)
    out = re.sub(r'<html lang="en"', '<html lang="%s"' % L["html"], out, count=1)
    canon = "https://paraglidingatlas.com/%s/%s" % (L["dir"], "" if page == "index.html" else page)
    eng = "https://paraglidingatlas.com/%s" % ("" if page == "index.html" else page)
    out = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + canon + m.group(2), out, count=1)
    out = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + canon + m.group(2), out, count=1)
    if 'property="og:locale"' in out:
        out = re.sub(r'(<meta property="og:locale" content=")[^"]*(")', lambda m: m.group(1) + L["og"] + m.group(2), out, count=1)
    # structured data: the page's own address and language
    out = re.sub(r'("url"\s*:\s*")%s(")' % re.escape(eng), lambda m: m.group(1) + canon + m.group(2), out)
    out = re.sub(r'("inLanguage"\s*:\s*")en(?:-[A-Z]{2})?(")', lambda m: m.group(1) + L["hreflang"] + m.group(2), out)
    out = add_marks(out, page, lang, avail_by_page[page])
    d = json.dumps(js_dict(page, lang, mem), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = out.replace("<!--/i18n-->\n</head>", '<script type="application/json" id="v4-i18n-d">%s</script>\n'
                      '<script src="%s../v4-i18n.js?v=%s"></script>\n<!--/i18n-->\n</head>'
                      % (d, up(page), hashlib.sha1(open(os.path.join(V4, "v4-i18n.js"), "rb").read()).hexdigest()[:8]), 1)
    ui = UI[lang]
    eng_href = up(page) + "../" + page
    note = ('<!--i18n--><div class="v4-i18n-note" role="note"><p>%s <a href="%s" hreflang="en" lang="en">%s</a>'
            '<span aria-hidden="true"> · </span><a href="%s../%s">%s</a></p></div><!--/i18n-->\n'
            % (html.escape(ui["Translated from English."]), eng_href, html.escape(ui["Read the English page"]),
               up(page), CFG["report_error"], html.escape(ui["Report a translation error"])))
    if binding:
        note = note.replace("</p></div>", '</p><p class="v4-i18n-bind">%s %s</p></div>' % (
            html.escape(ui[BIND_UI]), html.escape(ui["The English version is binding."])), 1)
    # at the end of the page's main content, in the flow (the nav floats over the top of some pages)
    if "</main>" in out:
        out = out.replace("</main>", note + "</main>", 1)
    else:
        out = re.sub(r'(<main\b[^>]*>\n?)', lambda m: m.group(1) + note, out, count=1)
    return out


BIND_UI = "Our terms, privacy and safety pages are in English."


def mark_binding(src, lang):
    """Links to the pages whose English is binding (config english_binding, never translated): hreflang="en",
    the binding sentence as their title, and a small EN after a plain-text link. Returns (src, any link marked)."""
    names = "|".join(re.escape(p[:-5]) for p in CFG["english_binding"])
    rx = re.compile(r'<a(\s[^>]*?href="(?:\.\./)*(?:%s)\.html(?:#[^"]*)?"[^>]*)>(.*?)</a>' % names, re.S)
    title = html.escape(UI[lang]["The English version is binding."], quote=True)
    hit = [False]

    def mark(m):
        attrs, inner = m.group(1), m.group(2)
        hit[0] = True
        if "hreflang=" not in attrs:
            attrs += ' hreflang="en"'
        if "title=" not in attrs:
            attrs += ' title="%s"' % title
        if "<" not in inner and inner.strip():
            inner += '<span class="v4-en" lang="en" aria-hidden="true">EN</span>'
        return "<a%s>%s</a>" % (attrs, inner)
    return rx.sub(mark, src), hit[0]


def load_ui():
    mem = {l: load_mem(l) for l in LANGS}
    for l in LANGS:
        UI[l] = {}
        for s in ui_segments():
            rec = mem[l].get(s.key) or {}
            UI[l][s.prot] = rec.get("tr") or s.prot


def cmd_build():
    load_ui()
    avail_by_page = {p: [] for p in CFG["pages"]}
    blocked = {}
    for lang in LANGS:
        ok, why = published(lang)
        for p in ok:
            avail_by_page[p].append(lang)
        blocked[lang] = why
    written = []
    for lang in LANGS:
        mem = load_mem(lang)
        d = os.path.join(V4, LANGS[lang]["dir"])
        for page in CFG["pages"]:
            dst = os.path.join(d, page)
            if lang in avail_by_page[page]:
                out = build_page(page, lang, avail_by_page, mem)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                old = open(dst, encoding="utf-8").read() if os.path.exists(dst) else None
                if old != out:
                    with open(dst, "w", encoding="utf-8") as fh:
                        fh.write(out)
                written.append(out_rel(page, lang))
            elif os.path.exists(dst):
                os.remove(dst)          # not every segment passes: the page is not published
                print("  removed %s: %d segments not ready" % (out_rel(page, lang), len(blocked[lang][page])))
    for page in CFG["pages"]:
        mark_english(page, avail_by_page[page])
    print("i18n: %d pages written: %s" % (len(written), ", ".join(written) or "none"))
    for lang, why in blocked.items():
        for page, bad in why.items():
            print("  %s/%s not written: %d segments not ready (first: %s %s)" % (lang, page, len(bad), bad[0][0], bad[0][1]))


# ---------------------------------------------------------------- check report
def visible_text(src):
    """The page's text as a reader meets it: the words, and the attributes people read (placeholders, alt
    text, labels, the description); whitespace of every kind as one space."""
    b = re.sub(r"(?s)<(script|style|svg|template)\b[^>]*>.*?</\1>", " ", src)
    b = re.sub(r"(?s)<!--.*?-->", " ", b)
    attrs = " ".join(m.group(2) for m in re.finditer(r'\s(alt|title|aria-label|placeholder|content|value|data-l|data-lines)="([^"]*)"', b))
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", b) + " " + attrs).split())


def cmd_check():
    load_ui()
    rep = {"date": datetime.date.today().isoformat(), "langs": {}}
    fails = 0
    lines = ["# Translation check report", "", "Generated by `python3 tools/v4_i18n.py check` on %s." % rep["date"], ""]
    segs = all_segments()
    gl = glossary()
    lines += ["Segments on the pilot pages: **%d** (%d English words)." % (
        len(segs), sum(len(TAG_PH.sub(" ", TOKEN_RX.sub(" ", s.prot)).split()) for s in segs.values())), ""]
    for lang in LANGS:
        mem = load_mem(lang)
        counts = {}
        problems = []
        for k, s in segs.items():
            st = status(lang, mem.get(k))
            key = st.split(":")[0]
            counts[key] = counts.get(key, 0) + 1
            if st != "ok":
                problems.append((k, s.where, st, s.prot[:90]))
        waived = [(k, r["waive"]) for k, r in mem.items() if r.get("waive") and k in segs]
        sourced = sum(1 for t in gl if (t.get(lang) or {}).get("source"))
        lines += ["## %s (%s)" % (LANGS[lang]["name"], lang), "",
                  "| | segments |", "|---|---|"] + ["| %s | %d |" % (k, v) for k, v in sorted(counts.items())] + [""]
        lines.append("Glossary: %d of %d terms sourced for %s." % (sourced, len(gl), lang))
        # page-level checks on the written pages
        for page in CFG["pages"]:
            dst = os.path.join(V4, LANGS[lang]["dir"], page)
            if not os.path.exists(dst):
                lines.append("- `%s/%s`: **not written** (segments not ready)" % (LANGS[lang]["dir"], page))
                fails += 1
                continue
            en_src = I18N_BLOCK.sub("", open(os.path.join(V4, page), encoding="utf-8").read())
            tr_src = open(dst, encoding="utf-8").read()
            en_t, tr_t = visible_text(en_src), visible_text(I18N_BLOCK.sub("", tr_src))
            miss = []
            for s in page_segments(page):
                for kind, v in s.toks:
                    r = " ".join(html.unescape(render_tok(kind, v, lang)).split())
                    if r not in tr_t:
                        miss.append(r)
            # links: every relative link resolves
            broken = []
            here = os.path.dirname(dst)
            for m in re.finditer(r'\s(?:href|src)="([^"#?]+)', tr_src):
                u = html.unescape(m.group(1))
                if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|/|\{|\$|%|data:)", u, re.I):
                    continue
                t = os.path.normpath(os.path.join(here, u))
                if not os.path.exists(t) and not os.path.exists(os.path.normpath(os.path.join(ROOT, os.path.relpath(t, V4)))):
                    broken.append(u)
            ok = not miss and not broken
            fails += 0 if ok else 1
            lines.append("- `%s/%s`: %s facts checked%s%s" % (
                LANGS[lang]["dir"], page, "all" if not miss else "**%d missing**" % len(miss),
                "" if not miss else " (%s)" % ", ".join(sorted(set(miss))[:6]),
                "" if not broken else "; **broken links**: %s" % ", ".join(sorted(set(broken))[:6])))
        if problems:
            lines += ["", "<details><summary>%d segments not publishable</summary>" % len(problems), ""]
            lines += ["- `%s` %s: %s. _%s_" % (k, w, st, html.escape(p)) for k, w, st, p in problems[:200]]
            lines += ["", "</details>"]
            fails += 1
        if waived:
            lines += ["", "Waived checks (each with its reason):"] + ["- `%s`: %s" % (k, w) for k, w in waived]
        lines.append("")
        rep["langs"][lang] = {"counts": counts, "problems": len(problems)}
    with open(os.path.join(DATA, "report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(DATA, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=1)
    print("\n".join(lines))
    print("FAIL" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    if a[0] == "jobs":
        cmd_jobs()
    elif a[0] == "ingest" and len(a) == 4:
        cmd_ingest(a[1], a[2], a[3])
    elif a[0] == "build":
        cmd_build()
    elif a[0] == "check":
        sys.exit(cmd_check())
    elif a[0] == "validate" and len(a) in (3, 4):
        # an agent's file, before it is taken in: every key there, and the mechanical checks
        segs = json.load(open(os.path.join(WORK, "all-segments.json"), encoding="utf-8"))
        data = json.load(open(a[2], encoding="utf-8"))
        todo_p = a[3] if len(a) == 4 else os.path.join(WORK, "%s-todo.json" % a[1])
        want = json.load(open(todo_p, encoding="utf-8")) if os.path.exists(todo_p) else segs
        bad = 0
        for k in want:
            if k not in data:
                print("missing %s" % k)
                bad += 1
        for k, v in data.items():
            v = v.get("tr", "") if isinstance(v, dict) else v
            if k not in segs:
                print("unknown key %s" % k)
                bad += 1
                continue
            pr = check_seg(a[1], segs[k]["en"], v)
            waived = list(data[k].get("waive") or {}) if isinstance(data[k], dict) else []
            pr = [x for x in pr if not any(x.startswith(w) for w in waived if w in SOFT)]
            if pr:
                print("%s: %s | EN: %s | TR: %s" % (k, "; ".join(pr), segs[k]["en"][:80], v[:80]))
                bad += 1
        print("%d problems" % bad)
        sys.exit(1 if bad else 0)
    elif a[0] == "prep" and len(a) in (4, 5):
        cmd_prep(a[1], a[2], a[3], a[4] if len(a) == 5 else None)
    elif a[0] == "segments":
        for s in page_segments(a[1]):
            print(s.key, s.where, s.prot, s.toks)
    else:
        raise SystemExit(__doc__)
