#!/usr/bin/env python3
"""
Check every page of the hidden v2 prototype (prototypes/v2/) before it can
replace the live site.

Static checks (every page, no browser):
  links      every relative href/src/srcset in the page resolves to a file
  robots     the page carries noindex (v2 must never be indexed as a prototype)
  structure  one <h1>, a lang, alt on every <img>
  parity     against the live page it will replace (the same path at the site
             root): title, meta description, canonical, og:title,
             og:description, og:image, twitter:card, the JSON-LD @types, the
             PodcastEpisode name / date / duration, the <h1> text, and no less
             body text and no fewer transcript chapters than live. Search
             engines and answer engines read these; v2 must keep all of them.

Browser checks (headless Chromium on the preview server, at 390, 768, 1440):
  errors     uncaught page errors, console errors from the site's own files
  overflow   no sideways scroll
  names      every link and button has an accessible name
  targets    on the phone width, links and buttons (not inline text links)
             smaller than 40px either way are counted (warn only)

    python3 tools/v2_check.py                    # everything
    python3 tools/v2_check.py --static           # no browser
    python3 tools/v2_check.py --only episodes/   # pages whose path starts so
    python3 tools/v2_check.py --shots DIR        # also save a screenshot per width

Needs the preview server (python3 -m http.server 8765 at the repo root) for
the browser checks. Exit status 1 if anything FAILs.
"""
import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = S.DIR
BASE = "http://127.0.0.1:8765/" + S.URL_PATH
WIDTHS = (390, 768, 1440)
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

SKIP = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#|\{|\$|%|data:)", re.I)
ATTR = re.compile(r'\s(?:href|src|poster|data-src)="([^"]*)"', re.I)
LOOP = re.compile(r'\sdata-loop="([^"]*)"')      # a prefix: <prefix>-720.mp4 and the rest
# Deliberate differences from the live page, with the reason (reported, not failed).
EXEMPT = {
    "index.html": {"words": "the owner cut the homepage text on purpose; the trip details it dropped are on the destination pages"},
}
FILLER = {"a", "an", "the", "with", "and", "of", "to", "in", "on", "for", "talk", "conversation", "interview", "chat", "ft", "feat"}
SRCSET = re.compile(r'\ssrcset="([^"]*)"', re.I)


def pages(only=""):
    out = []
    for d, _, fs in os.walk(V2):
        for f in fs:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(d, f), V2).replace(os.sep, "/")
                if rel.startswith(only):
                    out.append(rel)
    return sorted(out)


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def meta(src, key, attr="name"):
    m = re.search(r'<meta\s+%s="%s"\s+content="([^"]*)"' % (attr, re.escape(key)), src)
    if not m:
        m = re.search(r'<meta\s+content="([^"]*)"\s+%s="%s"' % (attr, re.escape(key)), src)
    return html.unescape(m.group(1)).strip() if m else None


def text_of(fragment):
    t = re.sub(r"<(script|style|noscript|svg)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def body_words(src):
    b = src[src.find("<body"):]
    b = re.sub(r"<nav\b.*?</nav>", " ", b, flags=re.S)
    b = re.sub(r"<footer\b.*?</footer>", " ", b, flags=re.S)
    return len(text_of(b).split())


def jsonld(src):
    types, eps = set(), []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        try:
            data = json.loads(block)
        except ValueError:
            types.add("!invalid")
            continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                t = x.get("@type")
                for tt in (t if isinstance(t, list) else [t]):
                    if tt:
                        types.add(tt)
                if t == "PodcastEpisode":
                    eps.append((x.get("name"), x.get("datePublished"), x.get("timeRequired") or x.get("duration")))
                stack.extend(x.values())
            elif isinstance(x, list):
                stack.extend(x)
    return types, sorted(eps, key=str)


def seo(src):
    t = re.search(r"<title>(.*?)</title>", src, re.S)
    c = re.search(r'<link rel="canonical" href="([^"]*)"', src)
    h1 = re.findall(r"<h1\b[^>]*>(.*?)</h1>", src, re.S)
    types, eps = jsonld(src)
    return {
        "title": html.unescape(t.group(1)).strip() if t else None,
        "description": meta(src, "description"),
        "canonical": c.group(1) if c else None,
        "og:title": meta(src, "og:title", "property"),
        "og:description": meta(src, "og:description", "property"),
        "og:image": meta(src, "og:image", "property"),
        "twitter:card": meta(src, "twitter:card"),
        "jsonld": sorted(types),
        "episode": eps,
        "h1": [text_of(h) for h in h1],
        "words": body_words(src),
        "chapters": len(set(re.findall(r'\bid="c(\d+)"', src))),
    }


def check_static(rel):
    fails, warns = [], []
    path = os.path.join(V2, rel)
    src = read(path)
    here = os.path.dirname(path)
    # links
    missing, other = set(), set()
    refs = ATTR.findall(src) + [u.strip().split(" ")[0] for s in SRCSET.findall(src) for u in s.split(",")]
    for u in refs:
        u = html.unescape(u).strip()
        if not u or SKIP.match(u) or u.startswith("/"):
            continue
        f = u.split("#")[0].split("?")[0]
        if not f:
            continue
        target = os.path.normpath(os.path.join(here, f))
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            missing.add(u)
        elif target.startswith(os.path.join(ROOT, "prototypes") + os.sep) and not target.startswith(V2 + os.sep):
            other.add(u)
    for u in LOOP.findall(src):
        if not os.path.exists(os.path.normpath(os.path.join(here, u + "-720.mp4"))):
            missing.add(u + "-720.mp4")
    if missing:
        fails.append("links: %d missing, e.g. %s" % (len(missing), sorted(missing)[:3]))
    if other:
        fails.append("links: %d into another prototype, e.g. %s" % (len(other), sorted(other)[:3]))
    if not S.IS_V2 and re.search(r"prototypes/v(?!%s/)\d+/" % S.NAME[1:], re.sub(r"<!--.*?-->", "", src, flags=re.S)):
        fails.append("links: names another prototype's folder")
    # robots
    if 'name="robots" content="noindex' not in src:
        fails.append("robots: no noindex")
    # structure
    n_h1 = len(re.findall(r"<h1\b", src))
    if n_h1 != 1 and not rel.endswith("404.html") and not S.proto_only(rel):
        fails.append("structure: %d <h1>" % n_h1)
    if not re.search(r'<html[^>]*\slang="', src):
        fails.append("structure: no lang")
    no_alt = len(re.findall(r"<img\b(?![^>]*\balt=)[^>]*>", src))
    if no_alt:
        fails.append("structure: %d <img> without alt" % no_alt)
    # parity
    live = os.path.join(ROOT, rel)
    if S.proto_only(rel):
        pass
    elif not os.path.exists(live):
        warns.append("parity: no live twin")
    else:
        a, b = seo(read(live)), seo(src)
        ex = EXEMPT.get(rel, {})
        for k in ("title", "description", "canonical", "og:title", "og:description", "og:image",
                  "twitter:card", "jsonld", "episode"):
            if a[k] != b[k]:
                fails.append("parity: %s differs (live %r, v2 %r)" % (k, str(a[k])[:80], str(b[k])[:80]))
        # the heading may be laid out differently, but must keep every word that carries meaning
        words = lambda hs: set(w for w in re.findall(r"[\w'’-]+", " ".join(hs).lower()) if w not in FILLER)
        lost = words(a["h1"]) - words(b["h1"])
        if len(a["h1"]) != len(b["h1"]) or lost:
            fails.append("parity: h1 loses %s (live %r)" % (sorted(lost), a["h1"][:1]))
        if b["words"] < a["words"] * 0.95:
            msg = "parity: body text %d words, live %d" % (b["words"], a["words"])
            (warns.append(msg + " (exempt: %s)" % ex["words"]) if "words" in ex else fails.append(msg))
        if b["chapters"] < a["chapters"]:
            fails.append("parity: %d chapters, live %d" % (b["chapters"], a["chapters"]))
    return fails, warns


BROWSER_JS = r"""() => {
  const out = {overflow: document.documentElement.scrollWidth - innerWidth, unnamed: [], small: 0};
  const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  document.querySelectorAll('a[href], button').forEach(el => {
    if (!vis(el) || el.closest('[aria-hidden="true"]')) return;
    const name = (el.getAttribute('aria-label') || el.getAttribute('title') || el.textContent ||
      [...el.querySelectorAll('img[alt]')].map(i => i.alt).join('')).trim();
    if (!name) out.unnamed.push(el.outerHTML.slice(0, 90));
    const inline = getComputedStyle(el).display === 'inline' && el.closest('p, li, dd, figcaption, .cd-line, .cd-seg');
    if (innerWidth < 500 && !inline) { const r = el.getBoundingClientRect();
      if (r.width < 40 || r.height < 40) out.small++; }
  });
  return out;
}"""


def check_browser(rels, shots=None):
    from playwright.sync_api import sync_playwright
    res = {r: ([], []) for r in rels}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else p.chromium.launch()
        for w in WIDTHS:
            # the phone width is a touch phone (pointer:coarse), as the site's touch sizes expect
            phone = w < 500
            ctx = b.new_context(viewport={"width": w, "height": 844 if phone else 900},
                                has_touch=phone, is_mobile=phone, device_scale_factor=2 if phone else 1)
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:140]))
            pg.on("console", lambda m: m.type == "error" and "127.0.0.1" in (m.location or {}).get("url", "") and errs.append("console: " + m.text[:140]))
            for r in rels:
                errs.clear()
                try:
                    pg.goto(BASE + r, wait_until="load", timeout=30000)
                    pg.wait_for_timeout(250)
                    o = pg.evaluate(BROWSER_JS)
                except Exception as ex:          # noqa: BLE001 - report and carry on
                    res[r][0].append("%d: load failed %s" % (w, str(ex)[:120]))
                    continue
                f, wn = res[r]
                for e in sorted(set(errs)):
                    f.append("%d: %s" % (w, e))
                if o["overflow"] > 0:
                    f.append("%d: sideways overflow %dpx" % (w, o["overflow"]))
                if o["unnamed"]:
                    f.append("%d: %d links/buttons without a name, e.g. %s" % (w, len(o["unnamed"]), o["unnamed"][0]))
                if o["small"]:
                    wn.append("%d: %d tap targets under 40px" % (w, o["small"]))
                if shots:
                    fn = os.path.join(shots, r.replace("/", "__")[:-5] + "-%d.png" % w)
                    pg.screenshot(path=fn)
            ctx.close()
        b.close()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--static", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--shots")
    ap.add_argument("--json")
    a = ap.parse_args()
    rels = pages(a.only)
    report = {}
    for r in rels:
        report[r] = check_static(r)
    if not S.IS_V2:
        for d, _, fs in os.walk(V2):
            for fn in fs:
                if fn.endswith((".js", ".css")):
                    code = re.sub(r"/\*.*?\*/", "", read(os.path.join(d, fn)), flags=re.S)
                    if re.search(r"prototypes/v(?!%s/)\d+/" % S.NAME[1:], code):
                        rels.append(os.path.relpath(os.path.join(d, fn), V2))
                        report[rels[-1]] = (["links: the file names another prototype's folder"], [])
    if not a.static:
        if a.shots:
            os.makedirs(a.shots, exist_ok=True)
        for r, (f, w) in check_browser([r for r in rels if r.endswith(".html")], a.shots).items():
            report[r][0].extend(f)
            report[r][1].extend(w)
    nf = nw = 0
    for r in rels:
        f, w = report[r]
        for x in f:
            print("FAIL  %-60s %s" % (r, x))
        for x in w:
            print("warn  %-60s %s" % (r, x))
        nf += len(f)
        nw += len(w)
        if not f and not w:
            print("  ok  %s" % r)
    print("\n%d %s pages checked | %d FAIL | %d warn" % (len(rels), S.NAME, nf, nw))
    if a.json:
        with open(a.json, "w") as fh:
            json.dump({r: {"fail": report[r][0], "warn": report[r][1]} for r in rels}, fh, indent=1)
    sys.exit(1 if nf else 0)


if __name__ == "__main__":
    main()
