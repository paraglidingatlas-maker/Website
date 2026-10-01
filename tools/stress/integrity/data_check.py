"""Data and JS integrity for the live site (repo root).

    python3 data_check.py [--port 8816]

1. node --check on every own JS file the 180 pages load (+ inline classic scripts via Function()).
2. Loads each data script (the way the pages do, as a classic <script>) in headless Chromium and reads the
   globals: EPISODE_SEARCH_DATA, LIB_TOPICS/LIB_FEATURED/LIB_EPISODES, LIB_MODAL (library + home),
   GLOBE_EP, EPISODE_PAGES, ATLAS_WAVEFORMS, SITEMAP_GRAPH (inline in sitemap.html).
3. Cross-references every record: page files, tag pages, series pages, chapter anchors (and whether the
   anchor's chapter title matches), YouTube ids vs the id embedded in the episode page, topic keys,
   tiles on index.html / KB pages that need a modal record.
4. Parses the root *.json files and checks slugs/images they reference.
Writes data_check.json next to this file.
"""
import collections
import glob
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib  # noqa: E402
import static_check as sc  # noqa: E402

ROOT = lib.ROOT
PORT = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8816
EP = lambda slug: os.path.join(ROOT, "episodes", slug + ".html")  # noqa: E731

problems = collections.defaultdict(list)
stats = collections.Counter()


def P(kind, **kw):
    problems[kind].append(kw)


# ------------------------------------------------------------------ episode page facts
_ep_cache = {}


def ep_facts(slug):
    """chapters on the page: title -> anchor (from the chapter rail), ids, embedded video id."""
    if slug in _ep_cache:
        return _ep_cache[slug]
    fp = EP(slug)
    if not os.path.isfile(fp):
        _ep_cache[slug] = None
        return None
    t = open(fp, encoding="utf-8").read()
    rail = {}
    by_anchor = {}
    for anchor, label in re.findall(r'<a class="cd-chap[^"]*" href="#(c\d+)"[^>]*>(.*?)</a>', t, re.S):
        text = re.sub(r"<time>.*?</time>", "", label, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", "", text))
        text = re.sub(r"\s+", " ", text).strip()
        rail[text] = anchor
        by_anchor[anchor] = text
    vids = set(re.findall(r"(?:youtube(?:-nocookie)?\.com/embed/|youtu\.be/|[?&]v=)([A-Za-z0-9_-]{11})", t))
    d = dict(rail=rail, by_anchor=by_anchor, ids=sc.parse("episodes/%s.html" % slug).idset, vids=vids)
    _ep_cache[slug] = d
    return d


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()


def check_chapters(src, slug, chapters):
    f = ep_facts(slug)
    if f is None:
        return
    for i, ch in enumerate(chapters or []):
        stats["chapters"] += 1
        title = norm(ch.get("title"))
        a = ch.get("anchor")
        page_anchor = f["rail"].get(title)
        if a is None:
            stats["chapters_null_anchor"] += 1
            if page_anchor:
                P("chapter anchor null but the episode page has that chapter", source=src, slug=slug, index=i,
                  title=title, page_anchor=page_anchor)
        elif a not in f["ids"]:
            P("chapter anchor id missing in episode page", source=src, slug=slug, anchor=a, title=title)
        elif f["by_anchor"].get(a) and f["by_anchor"][a] != title:
            P("chapter anchor points at a different chapter", source=src, slug=slug, anchor=a, title=title,
              page_title=f["by_anchor"][a])


def exists(rel):
    return os.path.isfile(os.path.join(ROOT, rel))


def check_modal_record(src, key, r, base_dir):
    stats["modal_records"] += 1
    slug = r.get("slug") or key
    if key and r.get("slug") and key != r["slug"]:
        P("modal key != slug", source=src, key=key, slug=r["slug"])
    page = r.get("page")
    if page:
        kind, rel, _, _ = sc.resolve(base_dir + "x.html", page)
        if not exists(rel):
            P("modal page missing", source=src, slug=slug, page=page)
        elif rel != "episodes/%s.html" % slug:
            P("modal page != slug", source=src, slug=slug, page=page)
    if r.get("seriesPage"):
        kind, rel, _, _ = sc.resolve(base_dir + "x.html", r["seriesPage"])
        if not exists(rel):
            P("modal seriesPage missing", source=src, slug=slug, seriesPage=r["seriesPage"])
    for tg in r.get("tags") or []:
        if tg.get("page") and not exists(tg["page"]):
            P("modal tag page missing", source=src, slug=slug, tag=tg)
    if r.get("artwork"):
        kind, rel, _, _ = sc.resolve(base_dir + "x.html", r["artwork"])
        if kind == "internal" and not exists(rel):
            P("modal artwork missing", source=src, slug=slug, artwork=r["artwork"])
    f = ep_facts(slug)
    if f and r.get("video") and f["vids"] and r["video"] not in f["vids"]:
        P("modal video id != episode page embed", source=src, slug=slug, video=r["video"], page_vids=sorted(f["vids"]))
    if r.get("nchapters") is not None and f is not None:
        n_page = len(f["by_anchor"])
        if n_page and r["nchapters"] != n_page:
            P("modal nchapters != chapters on episode page", source=src, slug=slug, nchapters=r["nchapters"],
              page=n_page, page_c1=f["by_anchor"].get("c1"))
    check_chapters(src, slug, r.get("chapters"))


# ------------------------------------------------------------------ 1. JS syntax
def js_syntax():
    files = set()
    inline = []
    for p in sc.PAGES:
        d = sc.parse(p)
        for tag, attr, val, line in d.refs:
            if tag == "script" and attr == "src":
                kind, rel, _, _ = sc.resolve(p, val)
                if kind == "internal":
                    files.add(rel)
        for attrs, text, line in d.scripts:
            t = (attrs.get("type") or "").lower()
            if "src" not in attrs and t in ("", "text/javascript", "module") and text.strip():
                inline.append((p, line, t, text))
    for rel in sorted(files):
        stats["js_files"] += 1
        r = subprocess.run(["node", "--check", os.path.join(ROOT, rel)], capture_output=True, text=True)
        if r.returncode:
            P("JS syntax error", file=rel, error=r.stderr.strip()[-400:])
    # inline scripts: check with node vm.Script (syntax only)
    seen = {}
    for p, line, t, text in inline:
        h = hash(text)
        if h in seen:
            continue
        seen[h] = p
    stats["inline_scripts"] = len(inline)
    stats["inline_scripts_unique"] = len(seen)
    payload = json.dumps([[seen[h], next(x for x in inline if hash(x[3]) == h)[3]] for h in seen])
    js = ("const vm=require('vm');const a=JSON.parse(require('fs').readFileSync(0,'utf8'));let bad=[];"
          "for(const [p,src] of a){try{new vm.Script(src)}catch(e){bad.push([p,String(e).slice(0,200)])}}"
          "console.log(JSON.stringify(bad))")
    r = subprocess.run(["node", "-e", js], input=payload, capture_output=True, text=True)
    for p, err in json.loads(r.stdout or "[]"):
        P("inline script syntax error", page=p, error=err)
    return sorted(files)


# ------------------------------------------------------------------ 2. load data globals in the browser
DATA_JS = ["episode-search-data.js", "library-data.js", "library-episodes.js", "globe-episodes.js",
           "episode-links.js", "waveforms.js"]
GRAB = """() => {
  const g = {};
  try { g.EPISODE_SEARCH_DATA = EPISODE_SEARCH_DATA; } catch (e) {}
  try { g.LIB_TOPICS = LIB_TOPICS; g.LIB_FEATURED = LIB_FEATURED; g.LIB_EPISODES = LIB_EPISODES; } catch (e) {}
  g.LIB_MODAL = window.LIB_MODAL; g.GLOBE_EP = window.GLOBE_EP; g.EPISODE_PAGES = window.EPISODE_PAGES;
  g.ATLAS_WAVEFORMS = window.ATLAS_WAVEFORMS;
  return JSON.stringify(g);
}"""


def load_globals():
    out = {}
    with lib.server(PORT) as base:
        with lib.browser() as b:
            ctx = b.new_context()
            def handler(route):
                u = route.request.url
                if u.startswith(base + "__blank__.html"):
                    # a UTF-8 document, like the real pages, so classic scripts decode as UTF-8
                    route.fulfill(status=200, content_type="text/html; charset=utf-8",
                                  body='<!doctype html><meta charset="utf-8"><title>blank</title>')
                elif u.startswith(base):
                    route.continue_()
                else:
                    route.abort()
            ctx.route("**/*", handler)
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(base + "__blank__.html")
            for f in DATA_JS:
                try:
                    pg.add_script_tag(url=base + f)
                except Exception as e:
                    P("data script failed to load", file=f, error=str(e)[:200])
            g = json.loads(pg.evaluate(GRAB))
            for e in errs:
                P("data script runtime error", error=e[:300])
            out.update(g)
            # home LIB_MODAL is a separate file with the same global name: load it alone
            pg2 = ctx.new_page()
            pg2.goto(base + "__blank__.html")
            pg2.add_script_tag(url=base + "home-episodes.js")
            out["HOME_LIB_MODAL"] = json.loads(pg2.evaluate("() => JSON.stringify(window.LIB_MODAL)"))
            # sitemap graph is inline
            pg3 = ctx.new_page()
            pg3.goto(base + "sitemap.html", wait_until="domcontentloaded")
            out["SITEMAP_GRAPH"] = json.loads(pg3.evaluate("() => JSON.stringify(window.SITEMAP_GRAPH || null)"))
            ctx.close()
    return out


def cross_check(g):
    pages = g.get("EPISODE_PAGES") or {}
    stats["EPISODE_PAGES"] = len(pages)
    for vid, slug in pages.items():
        if not os.path.isfile(EP(slug)):
            P("EPISODE_PAGES slug has no page", video=vid, slug=slug)
        else:
            f = ep_facts(slug)
            if f["vids"] and vid not in f["vids"]:
                P("EPISODE_PAGES id not embedded on its page", video=vid, slug=slug, page_vids=sorted(f["vids"]))
    dup = [s for s, c in collections.Counter(pages.values()).items() if c > 1]
    for s in dup:
        P("EPISODE_PAGES two ids map to one page", slug=s, ids=[k for k, v in pages.items() if v == s])

    esd = g.get("EPISODE_SEARCH_DATA") or []
    stats["EPISODE_SEARCH_DATA"] = len(esd)
    for r in esd:
        if r.get("page") and not os.path.isfile(EP(r["page"])) and not r["page"].startswith("episodes/"):
            P("search record page missing", title=r.get("title"), page=r.get("page"))
        if r.get("video_id") and pages and r["video_id"] in pages and r.get("page") and pages[r["video_id"]] != r["page"]:
            P("search record page != EPISODE_PAGES[video_id]", title=r.get("title"), video=r["video_id"],
              page=r["page"], map=pages[r["video_id"]])
        if r.get("page") and r["page"].startswith("episodes/"):
            P("search record page holds a path, episode-search.js wraps it again", title=r.get("title"),
              page=r["page"], built_href="episodes/" + r["page"] + ".html")
        if not r.get("page"):
            stats["search_records_without_page"] += 1
            on_site = pages.get(r.get("video_id"))
            if not on_site:
                # match by YouTube id embedded on an episode page
                for fp in glob.glob(os.path.join(ROOT, "episodes", "*.html")):
                    slug = os.path.basename(fp)[:-5]
                    f = ep_facts(slug)
                    if f and r.get("video_id") in f["vids"]:
                        on_site = slug
                        break
            if on_site:
                P("search record without page although the episode has a page (result opens YouTube)",
                  title=r.get("title"), video=r.get("video_id"), page=on_site)

    topics = g.get("LIB_TOPICS") or {}
    for f in g.get("LIB_FEATURED") or []:
        if f not in topics:
            P("LIB_FEATURED not a topic", featured=f)
    le = g.get("LIB_EPISODES") or []
    stats["LIB_EPISODES"] = len(le)
    modal = g.get("LIB_MODAL") or {}
    for r in le:
        if r.get("topic") not in topics:
            P("LIB_EPISODES bad topic", title=r.get("title"), topic=r.get("topic"))
        if r.get("page"):
            if not os.path.isfile(EP(r["page"])):
                P("LIB_EPISODES page missing", title=r.get("title"), page=r["page"])
            if r["page"] not in modal:
                P("library tile has no LIB_MODAL record (popup cannot open rich card)", page=r["page"],
                  title=r.get("title"))
            if pages and r.get("id") in pages and pages[r["id"]] != r["page"]:
                P("LIB_EPISODES page != EPISODE_PAGES[id]", id=r["id"], page=r["page"], map=pages[r["id"]])
        else:
            stats["LIB_EPISODES_without_page"] += 1
    for k in ("id", "page", "order"):
        c = collections.Counter(r.get(k) for r in le if r.get(k) not in (None, ""))
        for v, n in c.items():
            if n > 1:
                P("LIB_EPISODES duplicate %s" % k, value=v, count=n)

    for key, r in modal.items():
        check_modal_record("library-episodes.js", key, r, "")
    home = g.get("HOME_LIB_MODAL") or {}
    for key, r in home.items():
        check_modal_record("home-episodes.js", key, r, "")
        # same record in library data should agree
        lr = modal.get(key)
        if lr:
            for fld in ("page", "video", "nchapters", "dur", "epno", "date", "series"):
                if lr.get(fld) != r.get(fld):
                    P("home vs library LIB_MODAL disagree", slug=key, field=fld, home=r.get(fld), library=lr.get(fld))
    # tiles on index.html that need a home modal record
    d = sc.parse("index.html")
    for a in d.data_attrs:
        s = a.get("data-ep-slug")
        if s is not None:
            stats["index_tiles"] += 1
            if s not in home:
                P("index.html tile slug not in home LIB_MODAL", slug=s, line=a["_line"])
            if a.get("href") and a["href"] != "episodes/%s.html" % s:
                P("index.html tile href != slug", slug=s, href=a["href"])

    globe = g.get("GLOBE_EP") or {}
    stats["GLOBE_EP"] = len(globe)
    for slug, r in globe.items():
        if not os.path.isfile(EP(slug)):
            P("GLOBE_EP slug has no page", slug=slug)
            continue
        f = ep_facts(slug)
        if r.get("video") and f["vids"] and r["video"] not in f["vids"]:
            P("GLOBE_EP video != episode page embed", slug=slug, video=r["video"], page_vids=sorted(f["vids"]))
        if r.get("nch") is not None and f["by_anchor"] and r["nch"] != len(f["by_anchor"]):
            P("GLOBE_EP nch != chapters on page", slug=slug, nch=r["nch"], page=len(f["by_anchor"]))
        for k in ("lat", "lon"):
            v = r.get(k)
            if v is None or not isinstance(v, (int, float)) or abs(v) > (90 if k == "lat" else 180):
                P("GLOBE_EP bad coordinate", slug=slug, field=k, value=v)
    all_eps = {os.path.basename(x)[:-5] for x in glob.glob(os.path.join(ROOT, "episodes", "*.html"))}
    stats["episode_pages_on_disk"] = len(all_eps)
    stats["episodes_not_on_globe"] = len(all_eps - set(globe))

    sg = g.get("SITEMAP_GRAPH")
    if not sg:
        P("SITEMAP_GRAPH missing")
    else:
        ids = {n["id"] for n in sg.get("nodes", [])}
        stats["SITEMAP_GRAPH_nodes"] = len(ids)
        for n in sg.get("nodes", []):
            u = n.get("url")
            if u:
                kind, rel, frag, _ = sc.resolve("sitemap.html", u)
                if kind == "internal":
                    ok, tgt, _ = sc.target_file(rel)
                    if not ok:
                        P("SITEMAP_GRAPH node url missing", node=n["id"], url=u)
                    elif frag and sc.is_html(tgt) and frag not in sc.parse(tgt).idset and not frag.startswith("s="):
                        P("SITEMAP_GRAPH node fragment missing", node=n["id"], url=u)
            if n.get("parent") and n["parent"] not in ids:
                P("SITEMAP_GRAPH parent missing", node=n["id"], parent=n["parent"])
        for e in sg.get("links", sg.get("edges", [])) or []:
            s_, t_ = (e.get("s", e.get("source")), e.get("t", e.get("target"))) if isinstance(e, dict) else (e[0], e[1])
            if s_ not in ids or t_ not in ids:
                P("SITEMAP_GRAPH edge to unknown node", edge=e)
        for k, c in collections.Counter(n["id"] for n in sg.get("nodes", [])).items():
            if c > 1:
                P("SITEMAP_GRAPH duplicate node id", id=k, count=c,
                  urls=[n.get("url") for n in sg.get("nodes", []) if n["id"] == k])
        # every sitemap.xml page reachable in the graph?
        urls = set()
        for n in sg.get("nodes", []):
            if n.get("url"):
                kind, rel, _, _ = sc.resolve("sitemap.html", n["url"])
                urls.add(rel)
        missing = [p for p in sc.PAGES if p not in urls and p != "404.html"]
        stats["sitemap_pages_not_in_graph"] = len(missing)
        if missing:
            problems["info: sitemap.xml pages not drawn in SITEMAP_GRAPH"].append(dict(count=len(missing),
                                                                                         examples=missing[:15]))

    # library.html#s=<series> links used across the site must be real topics
    L = json.load(open(os.path.join(HERE, "static_links.json"))) if os.path.exists(
        os.path.join(HERE, "static_links.json")) else {"bad_fragment": []}
    for x in L["bad_fragment"]:
        if x["target"] == "library.html" and x["fragment"].startswith("s="):
            stats["library_series_links"] += 1
            if x["fragment"][2:] not in topics:
                P("library.html#s= link to unknown series", page=x["page"], fragment=x["fragment"])
        else:
            P("fragment not an id (static)", **x)


def kb_inline():
    for p in sc.PAGES:
        d = sc.parse(p)
        for attrs, text, line in d.scripts:
            if attrs.get("id") == "kbEpisodes":
                data = json.loads(text)
                for r in data:
                    check_modal_record(p, None, r, p.rsplit("/", 1)[0] + "/" if "/" in p else "")


def root_json():
    for fp in sorted(glob.glob(os.path.join(ROOT, "*.json"))):
        rel = os.path.basename(fp)
        try:
            d = json.load(open(fp, encoding="utf-8"))
            stats["json_ok"] += 1
        except Exception as e:
            P("root JSON parse error", file=rel, error=str(e)[:200])
            continue
        if rel == "episode-meta.json":
            for r in d:
                if not os.path.isfile(EP(r["slug"])):
                    P("episode-meta slug has no page", slug=r["slug"])
                f = ep_facts(r["slug"])
                if f and r.get("video_id") and f["vids"] and r["video_id"] not in f["vids"]:
                    P("episode-meta video_id != page embed", slug=r["slug"], video=r["video_id"], page=sorted(f["vids"]))
        if rel == "mp3-map.json":
            for k in d:
                if not os.path.isfile(EP(k)):
                    P("mp3-map slug has no page", slug=k)
        if rel == "homepage-cards.json":
            for r in d:
                if not os.path.isfile(EP(r["slug"])):
                    P("homepage-cards slug has no page", slug=r["slug"])
                if r.get("img") and not exists(r["img"].lstrip("/")):
                    P("homepage-cards img missing", slug=r["slug"], img=r["img"])


if __name__ == "__main__":
    files = js_syntax()
    g = load_globals()
    cross_check(g)
    kb_inline()
    root_json()
    out = dict(stats=stats, js_files=files, problems=problems)
    with open(os.path.join(HERE, "data_check.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(json.dumps(stats))
    for k, v in problems.items():
        print("%4d  %s" % (len(v), k))
        for x in v[:3]:
            print("        ", json.dumps(x, default=str)[:300])
