"""Static content/data integrity over the live pages (repo root, not prototypes/).

    python3 static_check.py [check ...]

checks: links ids svgrefs idrefs jsonld imgs size meta sitemap dupes kbdata parse   (default: all)
Read-only on the repo. Writes static_<check>.json next to this file and prints a summary.
"""
import collections
import html
import json
import os
import posixpath
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib  # noqa: E402

ROOT = lib.ROOT
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://paraglidingatlas.com/"
HOSTS = ("paraglidingatlas.com", "www.paraglidingatlas.com")
PAGES = lib.pages("live")

URL_ATTRS = {
    "a": ["href"], "area": ["href"], "link": ["href"], "script": ["src"], "img": ["src", "srcset"],
    "source": ["src", "srcset"], "video": ["src", "poster"], "audio": ["src"], "track": ["src"],
    "iframe": ["src"], "embed": ["src"], "object": ["data"], "form": ["action"], "input": ["src"],
    "use": ["href", "xlink:href"], "image": ["href", "xlink:href"], "feimage": ["href", "xlink:href"],
    "textpath": ["href", "xlink:href"], "lineargradient": ["href", "xlink:href"],
    "radialgradient": ["href", "xlink:href"], "pattern": ["href", "xlink:href"], "mpath": ["href", "xlink:href"],
    "animate": ["href", "xlink:href"], "set": ["href", "xlink:href"],
}
SVG_URL_ATTRS = ("fill", "stroke", "clip-path", "mask", "filter", "marker-start", "marker-mid", "marker-end", "style")
IDREF_ATTRS = ("aria-labelledby", "aria-describedby", "aria-controls", "aria-owns", "aria-activedescendant",
               "aria-details", "aria-errormessage", "aria-flowto", "for", "list", "headers", "form")
SVG_TAGS = {"svg", "use", "symbol", "defs", "g", "path", "lineargradient", "radialgradient", "stop", "clippath",
            "mask", "filter", "pattern", "marker", "text", "tspan", "circle", "rect", "line", "polyline", "polygon",
            "ellipse", "image", "textpath", "fegaussianblur", "feimage", "feturbulence", "fedisplacementmap"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []          # (id, tag, line, ctx) ctx in {"", "svg", "template", "noscript"}
        self.names = []        # a[name]
        self.refs = []         # (tag, attr, value, line)
        self.svgrefs = []      # (tag, attr, frag, line)
        self.idrefs = []       # (tag, attr, idref, line)
        self.imgs = []         # dict per img
        self.metas = []
        self.links = []
        self.title = None
        self.scripts = []      # (attrs, text, line)
        self.styles = []       # text
        self.tags = 0
        self.stack = []
        self._cur = None
        self._buf = []
        self.data_attrs = []   # elements with data-ep-*
        self.svg_depth = 0
        self.tmpl_depth = 0
        self.nos_depth = 0

    def ctx(self):
        if self.tmpl_depth:
            return "template"
        if self.nos_depth:
            return "noscript"
        return "svg" if self.svg_depth else ""

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, selfclose=False)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, selfclose=True)

    def _start(self, tag, attrs, selfclose):
        self.tags += 1
        line = self.getpos()[0]
        a = {}
        for k, v in attrs:
            if k not in a:
                a[k] = v if v is not None else ""
        if tag == "svg" and not selfclose:
            self.svg_depth += 1
        if tag == "template" and not selfclose:
            self.tmpl_depth += 1
        if tag == "noscript" and not selfclose:
            self.nos_depth += 1
        if not selfclose and tag not in VOID:
            self.stack.append(tag)
        if "id" in a:
            self.ids.append((a["id"], tag, line, self.ctx()))
        if tag == "a" and "name" in a:
            self.names.append(a["name"])
        for attr in URL_ATTRS.get(tag, []):
            if attr in a:
                self.refs.append((tag, attr, a[attr], line))
        if tag == "meta":
            self.metas.append(a)
            if a.get("property") in ("og:image", "og:url", "twitter:image") or a.get("name") in ("twitter:image",):
                self.refs.append((tag, a.get("property") or a.get("name"), a.get("content", ""), line))
        if tag == "link":
            self.links.append(a)
        for attr in SVG_URL_ATTRS:
            v = a.get(attr)
            if v and "url(" in v:
                for m in re.finditer(r"url\(\s*['\"]?#([^'\")\s]+)['\"]?\s*\)", v):
                    self.svgrefs.append((tag, attr, m.group(1), line))
        if tag in ("use", "textpath", "mpath", "lineargradient", "radialgradient", "pattern", "feimage", "image"):
            for attr in ("href", "xlink:href"):
                v = a.get(attr)
                if v and v.startswith("#"):
                    self.svgrefs.append((tag, attr, v[1:], line))
        for attr in IDREF_ATTRS:
            if attr == "for" and tag != "label" and tag != "output":
                continue
            if attr in ("list", "form") and tag not in ("input", "button", "select", "textarea", "fieldset",
                                                        "output", "object"):
                continue
            if attr == "headers" and tag not in ("td", "th"):
                continue
            v = a.get(attr)
            if v:
                for ref in v.split():
                    self.idrefs.append((tag, attr, ref, line))
        if tag == "img":
            self.imgs.append(dict(a, _line=line, _ctx=self.ctx()))
        if any(k.startswith("data-ep-") for k in a):
            self.data_attrs.append(dict(a, _tag=tag, _line=line))
        if tag in ("script", "style", "title"):
            self._cur = (tag, a, line)
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "svg" and self.svg_depth:
            self.svg_depth -= 1
        if tag == "template" and self.tmpl_depth:
            self.tmpl_depth -= 1
        if tag == "noscript" and self.nos_depth:
            self.nos_depth -= 1
        if tag in self.stack:
            while self.stack:
                if self.stack.pop() == tag:
                    break
        if self._cur and tag == self._cur[0]:
            text = "".join(self._buf)
            if tag == "script":
                self.scripts.append((self._cur[1], text, self._cur[2]))
            elif tag == "style":
                self.styles.append(text)
            elif tag == "title" and self.title is None and not self.svg_depth:
                self.title = text
            self._cur = None

    def handle_data(self, data):
        if self._cur:
            self._buf.append(data)


_cache = {}


def parse(rel):
    if rel not in _cache:
        fp = os.path.join(ROOT, rel)
        raw = open(fp, "rb").read()
        d = Doc()
        d.raw_len = len(raw)
        d.text = raw.decode("utf-8", errors="replace")
        d.feed(d.text)
        d.close()
        d.idset = {i for i, _, _, c in d.ids if c not in ("template", "noscript")} | set(d.names)
        _cache[rel] = d
    return _cache[rel]


def resolve(page, url):
    """-> (kind, target_rel_path_or_None, fragment, query). kind: internal|external|other|self"""
    url = (url or "").strip()
    if not url:
        return "self", page, "", ""
    if url.startswith("//"):
        u = urlsplit("https:" + url)
    else:
        u = urlsplit(url)
    if u.scheme and u.scheme not in ("http", "https"):
        return "other", None, "", ""
    if u.scheme or url.startswith("//"):
        if u.netloc.lower() not in HOSTS:
            return "external", None, u.fragment, u.query
        path = u.path or "/"
    else:
        path = u.path
    if not path:
        return "self", page, unquote(u.fragment), u.query
    path = unquote(path)
    if path.startswith("/"):
        rel = path.lstrip("/")
        trailing = path.endswith("/")
    else:
        rel = posixpath.join(posixpath.dirname(page), path)
        trailing = path.endswith("/")
    norm = posixpath.normpath(rel) if rel else ""
    if norm == ".":
        norm = ""
    if norm.startswith(".."):
        return "internal", "<outside-root>" + norm, unquote(u.fragment), u.query
    if trailing or norm == "":
        norm = (norm + "/index.html").lstrip("/")
    return "internal", norm, unquote(u.fragment), u.query


def target_file(rel):
    """Return (exists, resolved_rel, how)."""
    if rel.startswith("<outside-root>"):
        return False, rel, "outside root"
    fp = os.path.join(ROOT, rel)
    if os.path.isfile(fp):
        return True, rel, "file"
    if os.path.isdir(fp) and os.path.isfile(os.path.join(fp, "index.html")):
        return True, rel + "/index.html", "dir-index (GitHub Pages redirects to trailing slash)"
    if os.path.isfile(fp + ".html"):
        return True, rel + ".html", "extensionless (GitHub Pages only; http.server 404s)"
    return False, rel, "missing"


def is_html(rel):
    return rel.endswith(".html") or rel.endswith(".htm")


def srcset_urls(v):
    out = []
    for part in v.split(","):
        part = part.strip()
        if part:
            out.append(part.split()[0])
    return out


def is_redirect_stub(d):
    return any(m.get("http-equiv", "").lower() == "refresh" for m in d.metas)


def meta(d, **kw):
    for m in d.metas:
        if all(m.get(k) == v for k, v in kw.items()):
            return m.get("content")
    return None


def expected_url(page):
    if page == "index.html":
        return SITE
    return SITE + page


# --------------------------------------------------------------------------------------------- checks

def check_links():
    broken = []          # missing target file
    badfrag = []         # file exists, fragment id missing (static)
    stub_links = collections.Counter()  # links into redirect stubs
    nonstd = []
    inbound = collections.defaultdict(set)
    total = 0
    for p in PAGES:
        d = parse(p)
        for tag, attr, val, line in d.refs:
            if attr in ("og:url",):
                continue
            urls = srcset_urls(val) if attr == "srcset" else [val]
            for url in urls:
                kind, rel, frag, q = resolve(p, url)
                if kind in ("external", "other"):
                    continue
                total += 1
                if kind == "self":
                    tgt, ok, how = p, True, "self"
                else:
                    ok, tgt, how = target_file(rel)
                if not ok:
                    broken.append(dict(page=p, line=line, tag=tag, attr=attr, url=url, resolved=tgt))
                    continue
                if how not in ("file", "self"):
                    nonstd.append(dict(page=p, line=line, tag=tag, url=url, resolved=tgt, how=how))
                if is_html(tgt) and tag in ("a", "area"):
                    if tgt != p:
                        inbound[tgt].add(p)
                    td = parse(tgt)
                    if is_redirect_stub(td):
                        stub_links[(tgt, url)] += 1
                    if frag and frag.lower() != "top" and frag not in td.idset:
                        # text fragments (#:~:text=) are not ids
                        if frag.startswith(":~:"):
                            continue
                        badfrag.append(dict(page=p, line=line, url=url, target=tgt, fragment=frag))
    orphans = [p for p in PAGES if p not in inbound and p not in ("index.html", "404.html")]
    out = dict(total_internal_refs=total, broken=broken, bad_fragment=badfrag, nonstandard=nonstd,
               links_to_redirect_stubs=[dict(target=t, url=u, count=c) for (t, u), c in stub_links.items()],
               zero_inbound_pages=orphans, inbound_counts={p: len(inbound.get(p, ())) for p in PAGES})
    return out


def check_ids():
    dup = []
    for p in PAGES:
        d = parse(p)
        c = collections.Counter(i for i, _, _, ctx in d.ids if ctx not in ("template", "noscript"))
        for i, n in c.items():
            if n > 1:
                where = [(t, l, ctx) for (j, t, l, ctx) in d.ids if j == i]
                dup.append(dict(page=p, id=i, count=n, where=where))
        empty = [(t, l) for (j, t, l, ctx) in d.ids if not j.strip()]
        if empty:
            dup.append(dict(page=p, id="<empty>", count=len(empty), where=empty))
    return dict(duplicates=dup)


def check_svgrefs():
    miss = []
    total = 0
    for p in PAGES:
        d = parse(p)
        refs = list(d.svgrefs)
        for css in d.styles:
            for m in re.finditer(r"url\(\s*['\"]?#([^'\")\s]+)['\"]?\s*\)", css):
                refs.append(("<style>", "css", m.group(1), 0))
        for tag, attr, frag, line in refs:
            total += 1
            if frag not in d.idset:
                miss.append(dict(page=p, tag=tag, attr=attr, ref="#" + frag, line=line))
    return dict(total=total, missing=miss)


def check_idrefs():
    miss = []
    total = 0
    for p in PAGES:
        d = parse(p)
        for tag, attr, ref, line in d.idrefs:
            total += 1
            if ref not in d.idset:
                miss.append(dict(page=p, tag=tag, attr=attr, ref=ref, line=line))
    return dict(total=total, missing_static=miss)


def check_jsonld():
    bad = []
    stats = collections.Counter()
    url_mismatch = []

    def strict_const(x):
        raise ValueError("non-JSON constant " + x)

    for p in PAGES:
        d = parse(p)
        canon = next((l.get("href") for l in d.links if "canonical" in (l.get("rel") or "").split()), None)
        for attrs, text, line in d.scripts:
            if (attrs.get("type") or "").lower() != "application/ld+json":
                continue
            stats["blocks"] += 1
            try:
                obj = json.loads(text, parse_constant=strict_const)
            except Exception as e:
                bad.append(dict(page=p, line=line, problem="parse", error=str(e)[:200], snippet=text.strip()[:120]))
                continue
            items = obj if isinstance(obj, list) else [obj]
            for it in items:
                if not isinstance(it, dict):
                    bad.append(dict(page=p, line=line, problem="not an object"))
                    continue
                if "@context" not in it:
                    bad.append(dict(page=p, line=line, problem="missing @context", keys=list(it)[:8]))
                if "@graph" in it:
                    for g in it["@graph"]:
                        if "@type" not in g:
                            bad.append(dict(page=p, line=line, problem="@graph item missing @type",
                                            keys=list(g)[:8]))
                elif "@type" not in it:
                    bad.append(dict(page=p, line=line, problem="missing @type", keys=list(it)[:8]))
                # page-level url should agree with canonical
                nodes = it.get("@graph", [it])
                for n in nodes:
                    t = n.get("@type")
                    ts = t if isinstance(t, list) else [t]
                    if any(x in ("WebPage", "CollectionPage", "AboutPage", "ContactPage", "Article", "PodcastEpisode",
                                 "BlogPosting", "FAQPage", "ItemPage", "ProfilePage") for x in ts):
                        u = n.get("url") or (n.get("@id") if str(n.get("@id", "")).startswith("http") else None)
                        if u and canon:
                            if u.split("#")[0] != canon:
                                url_mismatch.append(dict(page=p, type=t, url=u, canonical=canon))
    return dict(stats=stats, problems=bad, url_vs_canonical=url_mismatch)


def check_imgs():
    rows = []
    n = 0
    for p in PAGES:
        d = parse(p)
        for im in d.imgs:
            n += 1
            has_w = "width" in im and im["width"].strip() != ""
            has_h = "height" in im and im["height"].strip() != ""
            st = im.get("style", "")
            ar = "aspect-ratio" in st
            if not (has_w and has_h) and not ar:
                rows.append(dict(page=p, line=im["_line"], src=im.get("src", "")[:120], cls=im.get("class", ""),
                                 loading=im.get("loading", ""), width=im.get("width"), height=im.get("height")))
    return dict(total_imgs=n, without_dims=rows, pages_affected=sorted({r["page"] for r in rows}))


def check_size():
    big = []
    rows = []
    for p in PAGES:
        d = parse(p)
        rows.append(dict(page=p, bytes=d.raw_len, tags=d.tags))
        if d.raw_len > 500 * 1024:
            big.append(dict(page=p, bytes=d.raw_len))
    rows.sort(key=lambda r: -r["bytes"])
    return dict(over_500k=big, top10=rows[:10], static_tag_over_3000=[r for r in rows if r["tags"] > 3000])


def check_meta():
    issues = []
    for p in PAGES:
        d = parse(p)
        canons = [l.get("href") for l in d.links if "canonical" in (l.get("rel") or "").lower().split()]
        ogu = [m.get("content") for m in d.metas if m.get("property") == "og:url"]
        robots = (meta(d, name="robots") or "").lower()
        exp = expected_url(p)
        if p == "404.html":
            if canons:
                issues.append(dict(page=p, problem="404 has canonical", value=canons))
            continue
        if len(canons) != 1:
            issues.append(dict(page=p, problem="canonical count %d" % len(canons), value=canons))
        elif canons[0] != exp:
            issues.append(dict(page=p, problem="canonical != own url", value=canons[0], expected=exp))
        if len(ogu) != 1:
            issues.append(dict(page=p, problem="og:url count %d" % len(ogu), value=ogu))
        elif ogu[0] != exp:
            issues.append(dict(page=p, problem="og:url != own url", value=ogu[0], expected=exp))
        if "noindex" in robots:
            issues.append(dict(page=p, problem="noindex page listed in sitemap", value=robots))
        if not (d.title or "").strip():
            issues.append(dict(page=p, problem="missing <title>"))
        if not (meta(d, name="description") or "").strip():
            issues.append(dict(page=p, problem="missing meta description"))
        ogimg = meta(d, property="og:image")
        if ogimg:
            kind, rel, _, _ = resolve(p, ogimg)
            if kind == "internal":
                ok, _, _ = target_file(rel)
                if not ok:
                    issues.append(dict(page=p, problem="og:image file missing", value=ogimg))
            if not ogimg.startswith("http"):
                issues.append(dict(page=p, problem="og:image not absolute", value=ogimg))
        else:
            issues.append(dict(page=p, problem="no og:image"))
        lang = re.search(r"<html[^>]*\blang=\"([^\"]+)\"", d.text[:2000])
        if not lang:
            issues.append(dict(page=p, problem="no <html lang>"))
    return dict(issues=issues)


def check_sitemap():
    s = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    locs = re.findall(r"<loc>([^<]*)</loc>", s)
    lastmods = re.findall(r"<lastmod>([^<]*)</lastmod>", s)
    rel = []
    problems = []
    for l in locs:
        u = urlsplit(l)
        if u.netloc not in HOSTS:
            problems.append(dict(loc=l, problem="foreign host"))
            continue
        r = u.path.lstrip("/") or "index.html"
        rel.append(r)
        ok, _, how = target_file(r)
        if not ok:
            problems.append(dict(loc=l, problem="file missing"))
        elif is_html(r):
            d = parse(r)
            if is_redirect_stub(d):
                problems.append(dict(loc=l, problem="sitemap lists a redirect stub"))
            canon = next((x.get("href") for x in d.links if "canonical" in (x.get("rel") or "").split()), None)
            if canon and canon != l:
                problems.append(dict(loc=l, problem="loc != page canonical", canonical=canon))
    dups = [k for k, v in collections.Counter(locs).items() if v > 1]
    for k in dups:
        problems.append(dict(loc=k, problem="duplicate loc"))
    bad_lm = [x for x in lastmods if not re.fullmatch(r"\d{4}-\d{2}-\d{2}(T[\d:+\-Z.]+)?", x)]
    future_lm = [x for x in lastmods if x[:10] > "2026-10-01"]
    disk = []
    for dp, dn, fs in os.walk(ROOT):
        relp = os.path.relpath(dp, ROOT)
        if relp.split(os.sep)[0] in ("prototypes", ".git", "node_modules", "templates", "docs", "tools"):
            continue
        for f in fs:
            if f.endswith(".html"):
                disk.append(os.path.normpath(os.path.join(relp, f)).replace(os.sep, "/"))
    not_in_sitemap = []
    for p in sorted(disk):
        if p in rel or p == "404.html":
            continue
        d = parse(p)
        robots = (meta(d, name="robots") or "").lower()
        not_in_sitemap.append(dict(page=p, redirect_stub=is_redirect_stub(d), noindex="noindex" in robots,
                                   title=(d.title or "").strip()[:80]))
    return dict(locs=len(locs), problems=problems, bad_lastmod=bad_lm, future_lastmod=future_lm,
                disk_html=len(disk),
                indexable_not_in_sitemap=[x for x in not_in_sitemap if not x["redirect_stub"] and not x["noindex"]],
                stubs_not_in_sitemap=len([x for x in not_in_sitemap if x["redirect_stub"]]))


def check_dupes():
    titles = collections.defaultdict(list)
    descs = collections.defaultdict(list)
    ogt = collections.defaultdict(list)
    h1s = collections.defaultdict(list)
    no_h1 = []
    multi_h1 = []
    for p in PAGES:
        if p == "404.html":
            continue
        d = parse(p)
        t = " ".join((d.title or "").split())
        titles[t].append(p)
        ds = " ".join((meta(d, name="description") or "").split())
        descs[ds].append(p)
        o = meta(d, property="og:title")
        if o:
            ogt[" ".join(o.split())].append(p)
        h = re.findall(r"<h1\b[^>]*>(.*?)</h1>", d.text, re.S)
        if not h:
            no_h1.append(p)
        elif len(h) > 1:
            multi_h1.append(dict(page=p, count=len(h)))
        else:
            h1s[" ".join(re.sub(r"<[^>]+>", "", html.unescape(h[0])).split())].append(p)
    f = lambda m: [dict(text=k, pages=v) for k, v in m.items() if len(v) > 1]
    lens = [dict(page=p, title_len=len(" ".join((parse(p).title or "").split())),
                 desc_len=len(" ".join((meta(parse(p), name="description") or "").split()))) for p in PAGES]
    return dict(dup_titles=f(titles), dup_descriptions=f(descs), dup_og_titles=f(ogt), dup_h1=f(h1s),
                no_h1=no_h1, multi_h1=multi_h1,
                title_over_70=[x for x in lens if x["title_len"] > 70],
                desc_over_170=[x for x in lens if x["desc_len"] > 170],
                desc_under_50=[x for x in lens if 0 < x["desc_len"] < 50])


def check_kbdata():
    """Inline <script type=application/json> blocks (KB episode data) and the tiles that index into them."""
    probs = []
    stats = collections.Counter()
    for p in PAGES:
        d = parse(p)
        for attrs, text, line in d.scripts:
            if (attrs.get("type") or "").lower() != "application/json":
                continue
            stats["blocks"] += 1
            try:
                data = json.loads(text)
            except Exception as e:
                probs.append(dict(page=p, line=line, problem="inline JSON parse", error=str(e)[:200]))
                continue
            if attrs.get("id") != "kbEpisodes":
                continue
            tiles = [a for a in d.data_attrs if "data-ep-index" in a]
            for t in tiles:
                stats["tiles"] += 1
                try:
                    i = int(t["data-ep-index"])
                    rec = data[i]
                except Exception:
                    probs.append(dict(page=p, line=t["_line"], problem="tile index out of range",
                                      index=t.get("data-ep-index"), n=len(data)))
                    continue
                if t.get("href") and rec.get("page") and t["href"] != rec["page"]:
                    probs.append(dict(page=p, line=t["_line"], problem="tile href != data[index].page",
                                      href=t["href"], data_page=rec["page"]))
            for i, rec in enumerate(data):
                stats["records"] += 1
                for key in ("page", "seriesPage"):
                    if rec.get(key):
                        kind, rel, frag, _ = resolve(p, rec[key])
                        ok, tgt, _ = target_file(rel) if kind == "internal" else (True, None, None)
                        if not ok:
                            probs.append(dict(page=p, problem="record %s missing" % key, index=i, value=rec[key]))
                for tg in rec.get("tags") or []:
                    if tg.get("page"):
                        # tag pages are root relative in this data ("tags/x.html")
                        r1 = posixpath.normpath(posixpath.join(posixpath.dirname(p), tg["page"]))
                        r2 = tg["page"]
                        if not (os.path.isfile(os.path.join(ROOT, r1)) or os.path.isfile(os.path.join(ROOT, r2))):
                            probs.append(dict(page=p, problem="tag page missing", index=i, value=tg["page"]))
                        elif not os.path.isfile(os.path.join(ROOT, r1)):
                            stats["tag_page_root_relative"] += 1
                if rec.get("page") and rec.get("chapters"):
                    kind, rel, _, _ = resolve(p, rec["page"])
                    if os.path.isfile(os.path.join(ROOT, rel)):
                        ep = parse(rel)
                        for ch in rec["chapters"]:
                            stats["chapters"] += 1
                            if ch.get("anchor") is None:
                                stats["chapters_without_anchor"] += 1
                            elif ch["anchor"] not in ep.idset:
                                probs.append(dict(page=p, problem="chapter anchor missing in episode page",
                                                  episode=rel, anchor=ch["anchor"], title=ch.get("title")))
                if rec.get("nchapters") is not None and rec.get("chapters") is not None:
                    if rec["nchapters"] != len(rec["chapters"]):
                        stats["nchapters_ne_len"] += 1
    return dict(stats=stats, problems=probs)


def check_parse():
    try:
        import html5lib
    except ImportError:
        return dict(error="html5lib not installed")
    by_code = collections.defaultdict(list)
    per_page = {}
    for p in PAGES:
        d = parse(p)
        parser = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
        parser.parse(d.text)
        per_page[p] = len(parser.errors)
        for (pos, code, dv) in parser.errors:
            by_code[code].append(dict(page=p, line=pos[0], col=pos[1], vars={k: str(v)[:60] for k, v in (dv or {}).items()}))
    summary = sorted(((k, len(v), len({x["page"] for x in v})) for k, v in by_code.items()), key=lambda x: -x[1])
    return dict(summary=[dict(code=k, errors=n, pages=np, examples=by_code[k][:12]) for k, n, np in summary],
                pages_with_errors=sum(1 for v in per_page.values() if v), per_page=per_page)


def check_assets():
    """?v= cache-bust tokens vs the file's sha256[:8] (tools/version_assets.py), CSS url() targets,
    inline style url() targets, and site URLs inside JSON-LD."""
    import hashlib
    stale = []
    versions = collections.defaultdict(set)
    css_files = set()
    for p in PAGES:
        d = parse(p)
        for tag, attr, val, line in d.refs:
            if tag in ("link", "script") and "?v=" in val:
                kind, rel, _, q = resolve(p, val)
                if kind != "internal":
                    continue
                v = re.search(r"v=([0-9a-f]+)", q)
                fp = os.path.join(ROOT, rel)
                if os.path.isfile(fp) and v:
                    h = hashlib.sha256(open(fp, "rb").read()).hexdigest()[:8]
                    versions[rel].add(v.group(1))
                    if v.group(1) != h:
                        stale.append(dict(page=p, asset=rel, token=v.group(1), sha256_8=h))
            if tag == "link" and attr == "href" and val.split("?")[0].endswith(".css"):
                kind, rel, _, _ = resolve(p, val)
                if kind == "internal":
                    css_files.add(rel)
    missing = []
    checked = 0
    url_re = re.compile(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)")
    for css in sorted(css_files):
        fp = os.path.join(ROOT, css)
        if not os.path.isfile(fp):
            continue
        txt = open(fp, encoding="utf-8", errors="replace").read()
        for m in url_re.finditer(txt):
            u = m.group(2).strip()
            if u.startswith(("data:", "#", "http:", "https:", "//")):
                continue
            checked += 1
            kind, rel, _, _ = resolve(css, u)
            if not target_file(rel)[0]:
                missing.append(dict(css=css, url=u, line=txt[:m.start()].count("\n") + 1))
    inline_missing = []
    for p in PAGES:
        d = parse(p)
        blobs = list(d.styles) + re.findall(r'style="([^"]*url\([^"]*)"', d.text)
        for b in blobs:
            for m in url_re.finditer(html.unescape(b)):
                u = m.group(2).strip()
                if u.startswith(("data:", "#", "http:", "https:", "//")):
                    continue
                checked += 1
                kind, rel, _, _ = resolve(p, u)
                if not target_file(rel)[0]:
                    inline_missing.append(dict(page=p, url=u))
    ld_missing = []
    ld_checked = 0
    for p in PAGES:
        d = parse(p)
        for attrs, text, line in d.scripts:
            if (attrs.get("type") or "").lower() != "application/ld+json":
                continue
            try:
                obj = json.loads(text)
            except Exception:
                continue
            stack = [obj]
            while stack:
                o = stack.pop()
                if isinstance(o, dict):
                    stack.extend(o.values())
                elif isinstance(o, list):
                    stack.extend(o)
                elif isinstance(o, str) and o.startswith(SITE):
                    ld_checked += 1
                    kind, rel, frag, _ = resolve(p, o)
                    ok, tgt, _ = target_file(rel)
                    if not ok:
                        ld_missing.append(dict(page=p, url=o))
                    elif frag and is_html(tgt) and frag not in parse(tgt).idset:
                        ld_missing.append(dict(page=p, url=o, problem="fragment id missing (fine if it is a "
                                                                          "pure @id node identifier)"))
    return dict(stale_version_tokens=stale, multi_version_assets={k: sorted(v) for k, v in versions.items()
                                                                     if len(v) > 1},
                css_files=sorted(css_files), css_url_checked=checked, css_url_missing=missing,
                inline_style_url_missing=inline_missing, jsonld_site_urls_checked=ld_checked,
                jsonld_site_url_missing=ld_missing)


CHECKS = dict(assets=check_assets, links=check_links, ids=check_ids, svgrefs=check_svgrefs, idrefs=check_idrefs, jsonld=check_jsonld,
              imgs=check_imgs, size=check_size, meta=check_meta, sitemap=check_sitemap, dupes=check_dupes,
              kbdata=check_kbdata, parse=check_parse)


def brief(name, res):
    def n(x):
        return len(x) if isinstance(x, (list, dict)) else x
    keys = {k: n(v) for k, v in res.items() if k not in ("inbound_counts", "per_page")}
    print("%-8s %s" % (name, json.dumps(keys, default=str)[:600]))


if __name__ == "__main__":
    want = sys.argv[1:] or list(CHECKS)
    print("pages:", len(PAGES))
    for c in want:
        r = CHECKS[c]()
        with open(os.path.join(HERE, "static_%s.json" % c), "w") as f:
            json.dump(r, f, indent=1, default=str)
        brief(c, r)
