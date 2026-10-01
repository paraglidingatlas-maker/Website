"""Static inventory of the live site's security surface (read-only).

python3 inventory.py            -> writes inventory.json and prints a summary
Scans all live pages (lib.pages("live")) plus redirect stubs for:
 script srcs, inline scripts, iframes, target=_blank links w/o noopener,
 http: resources, forms, mailto links, external hosts, meta CSP, SRI.
Then scans every JS file loaded + inline blocks for DOM-XSS sinks and sources.
"""
import json, os, re, sys, glob
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
sys.path.insert(0, "/home/user/Website/tools/stress")
import lib

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = lib.ROOT
FAKE = "https://paraglidingatlas.com/"

STUBS = []
for d in ["about", "contact", "mission", "podcast", "privacy", "terms-condition", "trips", "atlas/kenya"]:
    if os.path.exists(os.path.join(ROOT, d, "index.html")):
        STUBS.append(d + "/index.html")
# also any index.html redirect stubs inside knowledge-base subfolders
for fp in glob.glob(os.path.join(ROOT, "knowledge-base", "**", "index.html"), recursive=True):
    STUBS.append(os.path.relpath(fp, ROOT))


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.scripts, self.inline, self.iframes, self.blank, self.http, self.forms = [], [], [], [], [], []
        self.mailto, self.links, self.meta, self.cur = [], [], [], None
        self.cur_attrs = None
        self.buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script":
            if a.get("src"):
                self.scripts.append(a)
            else:
                self.cur = "script"; self.cur_attrs = a; self.buf = []
        if tag == "iframe":
            self.iframes.append(a)
        if tag == "a":
            href = a.get("href") or ""
            self.links.append(a)
            if (a.get("target") or "").lower() == "_blank":
                rel = (a.get("rel") or "").lower().split()
                if "noopener" not in rel and "noreferrer" not in rel:
                    self.blank.append(a)
            if href.lower().startswith("mailto:"):
                self.mailto.append(href)
        if tag == "form":
            self.forms.append(a)
        if tag == "meta":
            self.meta.append(a)
        for k in ("src", "href", "poster", "data", "action", "srcset"):
            v = a.get(k)
            if v and v.strip().lower().startswith("http:"):
                if tag == "a" and k == "href":
                    continue  # plain navigation links are not mixed content
                if tag == "link" and (a.get("rel") or "") in ("canonical", "alternate"):
                    continue
                self.http.append((tag, k, v))

    def handle_data(self, data):
        if self.cur == "script":
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.cur == "script":
            self.inline.append((self.cur_attrs, "".join(self.buf)))
            self.cur = None


SINKS = {
    "innerHTML": r"\.innerHTML\s*[+]?=",
    "outerHTML": r"\.outerHTML\s*[+]?=",
    "insertAdjacentHTML": r"insertAdjacentHTML\s*\(",
    "document.write": r"document\.write(ln)?\s*\(",
    "eval": r"(?<![\w.])eval\s*\(",
    "new Function": r"new\s+Function\s*\(",
    "setTimeout/Interval string": r"set(Timeout|Interval)\s*\(\s*['\"`]",
    "location assign": r"(location(\.href)?\s*=(?!=)|location\.(assign|replace)\s*\()",
    "href/src assign": r"\.(href|src|action|formAction)\s*=(?!=)",
    "setAttribute href/src": r"setAttribute\(\s*['\"](href|src|action|srcdoc|on\w+)['\"]",
    "jQuery html": r"\$\([^)]*\)\.(html|append|prepend|after|before)\(",
    "createContextualFragment": r"createContextualFragment",
    "DOMParser": r"DOMParser",
    "window.open": r"window\.open\s*\(",
}
SOURCES = {
    "location.search": r"location\.search",
    "location.hash": r"location\.hash",
    "location.href(read)": r"location\.href(?!\s*=[^=])",
    "URLSearchParams": r"URLSearchParams",
    "document.referrer": r"document\.referrer",
    "postMessage listener": r"addEventListener\(\s*['\"]message['\"]|onmessage\s*=",
    "localStorage": r"localStorage",
    "sessionStorage": r"sessionStorage",
    "window.name": r"window\.name",
    "document.cookie": r"document\.cookie",
    "fetch": r"\bfetch\s*\(",
    "XMLHttpRequest": r"XMLHttpRequest",
}
SECRETS = {
    "google api key": r"AIza[0-9A-Za-z_\-]{35}",
    "aws key": r"AKIA[0-9A-Z]{16}",
    "github token": r"gh[pousr]_[0-9A-Za-z]{30,}",
    "slack token": r"xox[abprs]-[0-9A-Za-z-]{10,}",
    "stripe": r"(sk|rk)_(live|test)_[0-9A-Za-z]{10,}",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "bearer": r"[Bb]earer\s+[A-Za-z0-9\-_\.=]{20,}",
    "generic secret assign": r"(api[_-]?key|secret|token|passwd|password|client_secret)['\"]?\s*[:=]\s*['\"][^'\"\s]{12,}['\"]",
    "hex32 (IndexNow-like)": r"\b[0-9a-f]{32}\b",
    "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
    "mailerlite/convertkit/etc": r"(mailerlite|convertkit|mailchimp|formspree|sendgrid|resend)[^\n]{0,80}",
}


def lineof(text, idx):
    return text.count("\n", 0, idx) + 1


def scan_js(text, name):
    hits = []
    for kind, rx in list(SINKS.items()) + list(SOURCES.items()):
        for m in re.finditer(rx, text):
            ln = lineof(text, m.start())
            line = text.splitlines()[ln - 1] if text.splitlines() else ""
            hits.append({"file": name, "line": ln, "kind": kind,
                         "cls": "sink" if kind in SINKS else "source", "code": line.strip()[:220]})
    return hits


def main():
    pages = lib.pages("live")
    allp = pages + STUBS
    res = {"pages": {}, "scripts": {}, "hosts": {}, "iframes": [], "blank": [], "http": [], "forms": [],
           "mailto": {}, "csp": [], "sri_missing": [], "inline_count": 0, "inline_handlers": 0}
    inline_texts = {}
    for p in allp:
        fp = os.path.join(ROOT, p)
        if not os.path.exists(fp):
            res["pages"][p] = "MISSING"; continue
        html = open(fp, encoding="utf-8", errors="replace").read()
        pr = P(); pr.feed(html)
        url = FAKE + p
        srcs = []
        for a in pr.scripts:
            full = urljoin(url, a["src"])
            u = urlparse(full)
            if u.netloc != "paraglidingatlas.com":
                res["hosts"].setdefault(u.netloc, set()).add(p)
                if "integrity" not in a:
                    res["sri_missing"].append((p, full))
            else:
                res["scripts"].setdefault(u.path.lstrip("/"), set()).add(p)
            srcs.append(full)
        for a in pr.iframes:
            res["iframes"].append({"page": p, **{k: a.get(k) for k in ("src", "sandbox", "loading", "allow", "title")}})
            if a.get("src"):
                res["hosts"].setdefault(urlparse(urljoin(url, a["src"])).netloc, set()).add(p)
        for a in pr.blank:
            res["blank"].append({"page": p, "href": a.get("href"), "rel": a.get("rel")})
        for t in pr.http:
            res["http"].append({"page": p, "tag": t[0], "attr": t[1], "val": t[2]})
        for a in pr.forms:
            res["forms"].append({"page": p, **a})
        for m in pr.mailto:
            res["mailto"].setdefault(m, set()).add(p)
        for m in pr.meta:
            if (m.get("http-equiv") or "").lower() == "content-security-policy":
                res["csp"].append((p, m.get("content")))
        # stylesheets / fonts from external hosts
        for m in re.finditer(r"<link[^>]+href=\"(https?://[^\"]+)\"", html):
            h = urlparse(m.group(1)).netloc
            if h != "paraglidingatlas.com":
                res["hosts"].setdefault("link:" + h, set()).add(p)
        res["inline_handlers"] += len(re.findall(r"\son[a-z]+\s*=\s*\"", html))
        for attrs, body in pr.inline:
            typ = (attrs.get("type") or "").lower()
            if typ in ("application/ld+json", "application/json", "text/template"):
                continue
            res["inline_count"] += 1
            key = re.sub(r"\s+", " ", body.strip())[:4000]
            inline_texts.setdefault(key, {"pages": [], "body": body})["pages"].append(p)
        res["pages"][p] = {"scripts": srcs, "inline": len(pr.inline), "iframes": len(pr.iframes)}

    # JS files scan
    hits = []
    for js in sorted(res["scripts"]):
        fp = os.path.join(ROOT, js)
        if not os.path.exists(fp):
            hits.append({"file": js, "kind": "MISSING FILE"}); continue
        hits += scan_js(open(fp, encoding="utf-8", errors="replace").read(), js)
    inline_list = []
    for i, (k, v) in enumerate(sorted(inline_texts.items(), key=lambda kv: -len(kv[1]["pages"]))):
        name = "inline#%d(%d pages, e.g. %s)" % (i, len(v["pages"]), v["pages"][0])
        h = scan_js(v["body"], name)
        hits += h
        inline_list.append({"id": i, "pages": len(v["pages"]), "example": v["pages"][0], "len": len(v["body"]),
                            "sinks": sorted(set(x["kind"] for x in h))})
    # secrets across all served text files (html/js/json/txt/xml) at root + subdirs excluding prototypes/node_modules
    secrets = []
    for fp in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(("prototypes", ".git", "node_modules")) or "/node_modules/" in rel or not os.path.isfile(fp):
            continue
        if not rel.endswith((".html", ".js", ".json", ".txt", ".xml", ".md", ".py", ".yml", ".css", ".sh", ".toml")):
            continue
        if os.path.getsize(fp) > 5_000_000:
            continue
        t = open(fp, encoding="utf-8", errors="replace").read()
        for kind, rx in SECRETS.items():
            for m in re.finditer(rx, t):
                if kind == "hex32 (IndexNow-like)" and rel.endswith(".html") and "episodes/" in rel:
                    pass
                secrets.append({"file": rel, "line": lineof(t, m.start()), "kind": kind, "match": m.group(0)[:120]})
    res["hosts"] = {k: sorted(v) for k, v in res["hosts"].items()}
    res["scripts"] = {k: len(v) for k, v in res["scripts"].items()}
    res["mailto"] = {k: len(v) for k, v in res["mailto"].items()}
    res["hits"] = hits
    res["inline_list"] = inline_list
    res["secrets"] = secrets
    fp = os.path.join(OUT, "inventory.json")
    json.dump(res, open(fp, "w"), indent=1, default=list)
    # also dump inline script bodies for reading
    with open(os.path.join(OUT, "inline_scripts.txt"), "w") as f:
        for i, (k, v) in enumerate(sorted(inline_texts.items(), key=lambda kv: -len(kv[1]["pages"]))):
            f.write("\n\n######## inline#%d pages=%d e.g. %s\n" % (i, len(v["pages"]), v["pages"][:3]))
            f.write(v["body"])
    print("pages scanned:", len(allp), "stubs:", len(STUBS))
    print("own scripts:", json.dumps(res["scripts"], indent=0))
    print("external hosts:", {k: len(v) for k, v in res["hosts"].items()})
    print("iframes:", len(res["iframes"]), "blank w/o noopener:", len(res["blank"]), "http:", len(res["http"]),
          "forms:", len(res["forms"]), "csp metas:", len(res["csp"]), "inline scripts:", res["inline_count"],
          "unique inline:", len(inline_list), "inline handlers:", res["inline_handlers"])
    print("mailto:", res["mailto"])
    print("sri missing:", len(res["sri_missing"]))
    from collections import Counter
    print("sink/source hits:", Counter((h.get("kind")) for h in hits))
    print("secret hits:", Counter(s["kind"] for s in secrets))


if __name__ == "__main__":
    main()
