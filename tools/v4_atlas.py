#!/usr/bin/env python3
"""
The Atlas: the way into the encyclopedia (owner, 21 Oct 2026: "this is a further extention of the globe
right? So I want that button to take us to globe and then to this"). The knowledge base page's button opens
this globe; from its pins and its questions the visitor goes on to the encyclopedia's answers and the FAQ
answers on the series pages.

    prototypes/v4/knowledge-base/encyclopedia/atlas.html   written by tools/v4_encyclopedia.py pages

Every pin and every word on it is read from the site:
  - the conversations: globe-episodes.js (tools/generate_globe_episodes.py), the same pins as the home and
    podcast globes, each placed where its story comes from (globe.js: inferred from the guest's nationality,
    a named place or a brand's home), with its range and bearing from Oslo, the coordinate in the site's
    navigation. Conversations at one place share one pin;
  - the questions each conversation answers: the FAQ answers on the v4 series and section pages, through
    the episode chapter each one cites; a question links to its answer there (the id the A to Z uses);
  - the ten answers in depth: the encyclopedia's review copy, each question, its short answer and the
    guests its "From the show" cards cite; choosing one draws lines from Oslo to those guests' pins;
  - the land: Natural Earth 1:110m (public domain, tools/data/ne-LICENSE.md), drawn as a field of dots.
The globe is drawn on a canvas with the site's own colours (read from its tokens), no library and no
image. It moves only when the visitor moves it: no turning on its own. With reduced motion it jumps
where a flight would glide and the lines are drawn at once. Without JavaScript, and for search engines
and screen readers, the same pins are a list under it (every conversation and the questions it answers).
"""
import html
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
LAND = os.path.join(ROOT, "tools", "data", "ne_110m_land.geojson")
OSLO = (59.9139, 10.7522)
STEP = 1.2            # degrees between dots, north to south (east to west it widens with the latitude)
E = html.escape


def fail(msg):
    raise SystemExit("v4_atlas: " + msg)


def faq_id(q):
    return "q-" + re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:70].rstrip("-")


# ── the land, as rows of dots ───────────────────────────────────────────────
def land_rows():
    """[[columns, hex bits], ...] from the south: a row every STEP degrees, its columns spaced evenly round
    the globe at that latitude, a bit set where the dot falls on land."""
    from PIL import Image, ImageDraw
    W, H = 2880, 1440                                    # 1/8 degree
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    g = json.load(open(LAND, encoding="utf-8"))
    for f in g["features"]:
        geo = f["geometry"]
        polys = geo["coordinates"] if geo["type"] == "MultiPolygon" else [geo["coordinates"]]
        for poly in polys:
            for k, ring in enumerate(poly):
                pts = [((lon + 180) * W / 360, (90 - lat) * H / 180) for lon, lat in ring]
                d.polygon(pts, fill=0 if k else 255)
    px = im.load()
    rows = []
    lat = -90 + STEP / 2
    while lat < 90:
        n = max(1, int(round(360 * math.cos(math.radians(lat)) / STEP)))
        bits = []
        for j in range(n):
            lon = -180 + (j + 0.5) * 360 / n
            x = min(W - 1, int((lon + 180) * W / 360))
            y = min(H - 1, int((90 - lat) * H / 180))
            bits.append(1 if px[x, y] else 0)
        bits += [0] * (-len(bits) % 4)
        rows.append([n, "".join("%x" % int("".join(map(str, bits[i:i + 4])), 2) for i in range(0, len(bits), 4))])
        lat += STEP
    return rows


# ── the conversations, their places and their questions ─────────────────────
def episodes():
    src = open(os.path.join(ROOT, "globe-episodes.js"), encoding="utf-8").read()
    return json.loads(src[src.index("{"):src.rindex("}") + 1])


def faqs():
    """(series page, question, its anchor, the episode slugs it cites), from the v4 series and section pages."""
    out = []
    kb = os.path.join(V4, "knowledge-base")
    for f in sorted(os.listdir(kb)):
        if not f.endswith(".html"):
            continue
        s = open(os.path.join(kb, f), encoding="utf-8").read()
        for m in re.finditer(r'<details[^>]*><summary><h3>(.*?)</h3></summary>(.*?)</details>', s, re.S):
            q = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
            eps = sorted(set(re.findall(r'href="\.\./episodes/([a-z0-9-]+)\.html', m.group(2))))
            if q.endswith("?") and eps:
                out.append((f, q, faq_id(q), eps))
    return out


def answers(src_dir):
    """The ten answers in depth: (slug, question, topic, short answer, [(guest, episode slug)])."""
    fm = open(os.path.join(os.path.dirname(src_dir), "flight-mechanics.html"), encoding="utf-8").read()
    cards = re.findall(r'<a class="nx-card" href="encyclopedia/([a-z0-9-]+)\.html"><span class="kicker">([^<]*)</span>'
                       r'<strong>([^<]*)</strong>', fm)
    topic = {slug: k for slug, k, _ in cards}
    asked = {slug: q for slug, _, q in cards}      # the question as the strip writes it (the page's h1 is title-cased)
    out = []
    for f in sorted(os.listdir(src_dir)):
        if not f.endswith(".html") or f == "index.html":
            continue
        s = open(os.path.join(src_dir, f), encoding="utf-8").read()
        slug = f[:-5]
        q = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        short = re.search(r'<p class="a-lede">(.*?)</p>', s, re.S)
        show = s[s.find('id="from-the-show"'):s.find('id="sources"')] if 'id="from-the-show"' in s else ""
        guests = []
        for name, ep in re.findall(r'<span class="n">([^<]+)</span>.*?href="[^"]*episodes/([a-z0-9-]+)\.html', show, re.S):
            if (name, ep) not in guests:
                guests.append((html.unescape(name), ep))
        if not (q and short):
            fail("%s: no question or short answer" % f)
        q = asked.get(slug) or re.sub(r"<[^>]+>", "", q.group(1))
        out.append((slug, html.unescape(q).strip(), html.unescape(topic.get(slug, "")),
                    html.unescape(re.sub(r"<[^>]+>", "", short.group(1))).strip(), guests))
    order = list(topic)
    out.sort(key=lambda a: order.index(a[0]) if a[0] in order else 99)
    return out


def data(src_dir):
    eps = episodes()
    places, at = [], {}
    for slug, e in sorted(eps.items(), key=lambda kv: (kv[1]["km"], kv[0])):
        key = (e["lat"], e["lon"])
        if key not in at:
            at[key] = len(places)
            places.append({"lat": e["lat"], "lon": e["lon"], "km": e["km"], "card": e["card"], "home": bool(e["home"]),
                           "eps": [], "qs": [], "deep": []})
        places[at[key]]["eps"].append(slug)
    by_ep = {slug: at[(e["lat"], e["lon"])] for slug, e in eps.items()}
    qs = []
    for page, q, qid, cited in faqs():
        where = sorted({by_ep[s] for s in cited if s in by_ep})
        if not where:
            continue
        qi = len(qs)
        qs.append({"q": q, "href": "../%s#%s" % (page, qid)})
        for p in where:
            places[p]["qs"].append(qi)
    ans = []
    for i, (slug, q, topic, short, guests) in enumerate(answers(src_dir)):
        gs = [{"name": n, "ep": ep, "p": by_ep[ep]} for n, ep in guests if ep in by_ep]
        ans.append({"slug": slug, "q": q, "topic": topic, "short": short, "guests": gs})
        for p in sorted({g["p"] for g in gs}):
            places[p]["deep"].append(i)
    epi = {slug: {"t": e["title"], "g": e["guest"], "s": e["series"], "n": e["epno"], "d": e["dur"]} for slug, e in eps.items()}
    return {"oslo": OSLO, "places": places, "eps": epi, "qs": qs, "answers": ans,
            "land": {"step": STEP, "rows": land_rows()}}



CSS = (
    ".atl-stage{display:grid;grid-template-columns:minmax(0,25rem) minmax(0,1fr);grid-template-areas:\"copy globe\" \"qs globe\";"
    "column-gap:clamp(1.5rem,4vw,4rem);max-width:1560px;margin:0 auto;padding:var(--sp-4) var(--gutter) var(--sp-5);"
    "min-height:calc(100svh - var(--nav-h,72px));grid-template-rows:auto 1fr}"
    ".atl-copy{grid-area:copy;padding-top:var(--sp-4)}"
    ".atl-copy .breadcrumb{margin-bottom:var(--sp-3)}"
    ".atl-title{font-family:var(--font-display);font-weight:700;font-size:clamp(2.3rem,4.4vw,3.9rem);line-height:1.02;margin:.6rem 0 0;color:var(--white)}"
    ".atl-title em{font-style:normal;color:var(--orange)}"
    ".atl-lead{margin:var(--sp-3) 0 0;color:var(--gray-light);font-size:1.02rem;line-height:1.65;max-width:30rem}"
    ".atl-qs{grid-area:qs;padding-top:var(--sp-4)}"
    ".atl-qs-h{display:block;font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gray);margin-bottom:.4rem}"
    ".atl-qs ol{list-style:none;margin:0;padding:0;border-top:1px solid var(--edge)}"
    ".atl-qs li a{display:grid;grid-template-columns:2.2rem minmax(0,1fr);align-items:baseline;padding:.62rem 0;"
    "border-bottom:1px solid var(--edge);color:var(--gray-light);text-decoration:none;font-size:.95rem;line-height:1.35;"
    "transition:color .3s var(--ease),padding .35s var(--ease)}"
    ".atl-qs li a span{font-family:var(--font-display);font-size:.78rem;color:var(--orange);font-variant-numeric:tabular-nums}"
    ".atl-qs li a:is(:hover,:focus-visible),.atl-qs li a[aria-current=true]{color:var(--white);padding-left:.45rem}"
    ".atl-qs li a[aria-current=true]{box-shadow:inset 2px 0 0 var(--orange)}"
    ".atl-az{display:inline-block;margin-top:var(--sp-3);color:var(--orange);font-weight:600;font-size:.9rem;text-decoration:none}"
    ".atl-az:hover{text-decoration:underline}"
    ".atl-globe{grid-area:globe;position:relative;min-height:min(84svh,820px);outline:none}"
    ".atl-globe canvas{position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab;touch-action:none;"
    "opacity:0;transition:opacity 1.1s var(--ease)}"
    ".atl.is-live .atl-globe canvas{opacity:1}"
    # zoomed in, the globe meets the edges of its box: there it fades out rather than stops in a line
    "@media (min-width:901px){.atl-globe canvas{"
    "-webkit-mask-image:linear-gradient(90deg,transparent,black 72px),linear-gradient(180deg,transparent,black 56px,black calc(100% - 56px),transparent);"
    "-webkit-mask-composite:source-in;"
    "mask-image:linear-gradient(90deg,transparent,black 72px),linear-gradient(180deg,transparent,black 56px,black calc(100% - 56px),transparent);"
    "mask-composite:intersect}}"
    ".atl-globe.is-drag canvas{cursor:grabbing}.atl-globe.is-pin canvas{cursor:pointer}"
    ".atl-globe:focus-visible{box-shadow:inset 0 0 0 1px var(--orange)}"
    ".atl-tip{position:absolute;z-index:3;pointer-events:none;transform:translate(-50%,calc(-100% - 14px));padding:.45rem .7rem;"
    "background:color-mix(in srgb,var(--bg) 92%,transparent);border:1px solid var(--edge-hi);font-size:.78rem;line-height:1.35;"
    "color:var(--white);white-space:nowrap;max-width:18rem;overflow:hidden;text-overflow:ellipsis}"
    ".atl-tip b{display:block;font-weight:600}.atl-tip span{color:var(--gray-light)}"
    ".atl-ctl{position:absolute;right:0;bottom:0;z-index:2;display:flex;gap:6px}"
    ".atl-ctl button{min-width:40px;height:40px;padding:0 .7rem;background:color-mix(in srgb,var(--bg) 80%,transparent);"
    "border:1px solid var(--edge-hi);color:var(--white);font:inherit;font-size:.9rem;cursor:pointer;transition:border-color .3s var(--ease)}"
    ".atl-ctl button:is(:hover,:focus-visible){border-color:var(--orange)}"
    ".atl-hint{position:absolute;left:0;bottom:0;margin:0;z-index:2;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gray)}"
    ".atl-panel{position:absolute;z-index:4;top:var(--sp-3);right:0;width:min(25rem,100%);max-height:calc(100% - 64px - var(--sp-3));overflow:auto;"
    "padding:var(--sp-4) var(--sp-4) var(--sp-3);background:color-mix(in srgb,var(--bg) 90%,transparent);border:1px solid var(--edge-hi);"
    "-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);opacity:0;transform:translateY(10px);"
    "transition:opacity .45s var(--ease),transform .45s var(--ease);overscroll-behavior:contain}"
    ".atl-panel.is-open{opacity:1;transform:none}.atl-panel[hidden]{display:none}"
    ".atl-x{position:absolute;top:.6rem;right:.6rem;width:36px;height:36px;background:none;border:1px solid var(--edge);color:var(--gray-light);"
    "font-size:1.2rem;line-height:1;cursor:pointer}.atl-x:is(:hover,:focus-visible){color:var(--white);border-color:var(--orange)}"
    ".atl-k{display:block;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);margin-right:2.5rem}"
    ".atl-panel h2{font-family:var(--font-display);font-size:1.45rem;line-height:1.2;margin:.5rem 2.2rem 0 0;color:var(--white)}"
    ".atl-panel p{color:var(--gray-light);font-size:.92rem;line-height:1.6;margin:.8rem 0 0}"
    ".atl-panel h3{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gray);margin:var(--sp-3) 0 .3rem;font-weight:500}"
    ".atl-panel ul{list-style:none;margin:0;padding:0}"
    ".atl-panel li{border-bottom:1px solid var(--edge)}"
    ".atl-panel li a,.atl-panel li button{display:block;width:100%;text-align:left;padding:.55rem 0;background:none;border:0;"
    "color:var(--gray-light);font:inherit;font-size:.9rem;line-height:1.4;text-decoration:none;cursor:pointer}"
    ".atl-panel li a:is(:hover,:focus-visible),.atl-panel li button:is(:hover,:focus-visible){color:var(--white)}"
    ".atl-panel li small{display:block;color:var(--gray);font-size:.74rem;margin-bottom:.15rem}"
    ".atl-go{display:inline-block;margin-top:var(--sp-3);padding:.75rem 1.1rem;background:var(--orange);color:var(--bg);font-weight:600;"
    "font-size:.9rem;text-decoration:none}.atl-go:is(:hover,:focus-visible){background:var(--white)}"
    ".atl-more{margin-top:.5rem;font-size:.8rem;color:var(--gray)}"
    ".atl-list{max-width:1300px;margin:0 auto;padding:var(--sp-section) var(--gutter);border-top:1px solid var(--edge)}"
    ".atl-list>h2{font-family:var(--font-display);font-size:clamp(1.6rem,3vw,2.3rem);margin:0;color:var(--white)}"
    ".atl-list>p{color:var(--gray-light);max-width:40rem;margin:.7rem 0 var(--sp-4)}"
    ".atl-places{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--sp-3) var(--sp-4);list-style:none;margin:0;padding:0}"
    ".atl-places>li{border-top:1px solid var(--edge);padding-top:var(--sp-3)}"
    ".atl-places h3{font-family:var(--font-display);font-size:1.02rem;line-height:1.3;margin:0;color:var(--white)}"
    ".atl-places .atl-k{margin:0 0 .35rem}"
    ".atl-places ul{list-style:none;margin:.5rem 0 0;padding:0}"
    ".atl-places ul a{color:var(--gray-light);font-size:.86rem;line-height:1.45;text-decoration:none}"
    ".atl-places ul a:hover{color:var(--orange)}"
    ".atl-places li li{padding:.2rem 0}"
    ".atl-places details{margin-top:.5rem}.atl-places summary{cursor:pointer;color:var(--gray);font-size:.8rem}"
    "@media (max-width:1100px){.atl-places{grid-template-columns:repeat(2,minmax(0,1fr))}}"
    "@media (max-width:900px){.atl-stage{grid-template-columns:minmax(0,1fr);grid-template-areas:\"copy\" \"globe\" \"qs\";min-height:0}"
    ".atl-globe{min-height:0;aspect-ratio:1/1.08;margin:0 calc(var(--gutter) * -1)}"
    ".atl-hint,.atl-ctl{margin:0 var(--gutter)}.atl-ctl{right:0}"
    ".atl-panel{position:fixed;top:auto;right:0;left:0;bottom:0;width:auto;max-height:46svh;border-width:1px 0 0;z-index:60;"
    "padding:var(--sp-4) var(--gutter) var(--sp-4)}}"
    "@media (max-width:600px){.atl-places{grid-template-columns:minmax(0,1fr)}.atl-hint{display:none}}"
    "@media (prefers-reduced-motion:reduce){.atl-globe canvas,.atl-panel,.atl-qs li a{transition:none}}"
)

JS = r"""(function () {
  var root = document.getElementById("atlas"), box = root && root.querySelector(".atl-globe");
  var cv = box && box.querySelector("canvas"), ctx = cv && cv.getContext && cv.getContext("2d");
  if (!ctx) return;
  var D = JSON.parse(document.getElementById("atlasData").textContent);
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var RAD = Math.PI / 180, DEG = 180 / Math.PI;
  root.classList.add("is-live");

  /* the site's colours, read from its tokens */
  function rgb(v) {
    var e = document.createElement("i"); e.style.color = "var(" + v + ")"; e.style.display = "none";
    document.body.appendChild(e); var m = getComputedStyle(e).color.match(/[\d.]+/g); e.remove();
    return m ? m.slice(0, 3).map(Number) : [128, 128, 128];
  }
  var C = { bg: rgb("--bg"), white: rgb("--white"), gray: rgb("--gray-light"), orange: rgb("--orange") };
  function col(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }
  var FONT = getComputedStyle(document.body).fontFamily;

  function vec(lat, lon) { lat *= RAD; lon *= RAD; return [Math.cos(lat) * Math.cos(lon), Math.cos(lat) * Math.sin(lon), Math.sin(lat)]; }

  /* the land: rows of dots, a bit per dot */
  var land = [];
  (function () {
    var step = D.land.step, lat = -90 + step / 2;
    D.land.rows.forEach(function (r) {
      var n = r[0], hex = r[1];
      for (var j = 0; j < n; j++) {
        if ((parseInt(hex.charAt(j >> 2), 16) >> (3 - (j & 3))) & 1) {
          var v = vec(lat, -180 + (j + 0.5) * 360 / n); land.push(v[0], v[1], v[2]);
        }
      }
      lat += step;
    });
    land = new Float32Array(land);
  })();
  var places = D.places.map(function (p, i) {
    var names = [];
    p.eps.forEach(function (s) { var g = D.eps[s].g; if (names.indexOf(g) < 0) names.push(g); });
    return { i: i, v: vec(p.lat, p.lon), p: p, names: names, x: 0, y: 0, z: 0, r: 0 };
  });
  var OSLO = vec(D.oslo[0], D.oslo[1]);

  /* the view */
  var view = { lat: 36, lon: 14, zoom: 1.05 }, home = { lat: 36, lon: 14, zoom: 1.05 };
  var W = 0, H = 0, dpr = 1, R = 0, cx = 0, cy = 0, F, Ea, N;
  function basis() {
    var la = view.lat * RAD, lo = view.lon * RAD;
    F = [Math.cos(la) * Math.cos(lo), Math.cos(la) * Math.sin(lo), Math.sin(la)];
    Ea = [-Math.sin(lo), Math.cos(lo), 0];
    N = [-Math.sin(la) * Math.cos(lo), -Math.sin(la) * Math.sin(lo), Math.cos(la)];
  }
  function size() {
    var r = box.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(1, Math.round(r.width * dpr)); H = Math.max(1, Math.round(r.height * dpr));
    cv.width = W; cv.height = H; shiftTo = !panel.hidden && window.innerWidth > 900 ? (panel.offsetWidth + 16) * dpr / 2 : 0;
    shift = shiftTo; draw();
  }

  var hover = -1, pick = -1, answer = -1, grow = 1, t0 = 0, shift = 0, shiftTo = 0;
  function draw() {
    basis();
    R = Math.min(W, H) * 0.43 * view.zoom; cx = W / 2 - shift; cy = H / 2;
    ctx.clearRect(0, 0, W, H);
    /* the air round it, then the sea */
    var g = ctx.createRadialGradient(cx, cy, R * 0.96, cx, cy, R * 1.16);
    g.addColorStop(0, col(C.orange, 0.13)); g.addColorStop(1, col(C.orange, 0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R * 1.16, 0, 7); ctx.fill();
    ctx.fillStyle = col(C.bg, 1); ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.fill();
    g = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.05, cx, cy, R);
    g.addColorStop(0, col(C.white, 0.075)); g.addColorStop(0.7, col(C.white, 0.02)); g.addColorStop(1, col(C.white, 0.0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.fill();
    ctx.strokeStyle = col(C.white, 0.1); ctx.lineWidth = dpr; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.stroke();
    /* the graticule, every 30 degrees */
    ctx.strokeStyle = col(C.white, 0.045); ctx.lineWidth = dpr;
    for (var la = -60; la <= 60; la += 30) line(function (t) { return vec(la, t * 360 - 180); }, 90);
    for (var lo = -180; lo < 180; lo += 30) line(function (t) { return vec(t * 180 - 90, lo); }, 60);
    /* the land, nearer dots brighter */
    var s0 = Math.max(1, 1.25 * dpr * Math.sqrt(view.zoom)), buckets = [[], [], [], []];
    for (var i = 0; i < land.length; i += 3) {
      var z = land[i] * F[0] + land[i + 1] * F[1] + land[i + 2] * F[2];
      if (z <= 0.02) continue;
      var x = land[i] * Ea[0] + land[i + 1] * Ea[1], y = land[i] * N[0] + land[i + 1] * N[1] + land[i + 2] * N[2];
      buckets[Math.min(3, (z * 4) | 0)].push(cx + R * x, cy - R * y);
    }
    var alpha = [0.13, 0.22, 0.32, 0.42];
    for (var b = 0; b < 4; b++) {
      var q = buckets[b], s = s0 * (0.8 + b * 0.12); ctx.fillStyle = col(C.gray, alpha[b]);
      for (var k = 0; k < q.length; k += 2) ctx.fillRect(q[k] - s / 2, q[k + 1] - s / 2, s, s);
    }
    /* an answer: lines from Oslo to the guests who explain it */
    if (answer >= 0) arcs();
    /* the pins */
    places.forEach(function (P) {
      var v = P.v; P.z = v[0] * F[0] + v[1] * F[1] + v[2] * F[2];
      P.x = cx + R * (v[0] * Ea[0] + v[1] * Ea[1]); P.y = cy - R * (v[0] * N[0] + v[1] * N[1] + v[2] * N[2]);
      P.r = (2.4 + 1.25 * Math.sqrt(P.p.eps.length)) * dpr;
    });
    var labels = [];
    places.slice().sort(function (a, b) { return a.z - b.z; }).forEach(function (P) {
      if (P.z <= 0) return;
      var on = P.i === hover || P.i === pick, lit = answer >= 0 && P.p.deep.indexOf(answer) >= 0;
      var a = Math.min(1, P.z * 3), r = P.r * (on ? 1.35 : 1);
      ctx.globalAlpha = answer >= 0 && !lit && !on ? a * 0.35 : a;
      ctx.fillStyle = col(C.orange, 0.16); ctx.beginPath(); ctx.arc(P.x, P.y, r * 2.4, 0, 7); ctx.fill();
      ctx.fillStyle = P.p.home ? col(C.white, 1) : col(C.orange, 1); ctx.beginPath(); ctx.arc(P.x, P.y, r, 0, 7); ctx.fill();
      if (P.p.home) { ctx.strokeStyle = col(C.orange, 1); ctx.lineWidth = 1.5 * dpr; ctx.beginPath(); ctx.arc(P.x, P.y, r + 2.5 * dpr, 0, 7); ctx.stroke(); }
      if (P.i === pick) { ctx.strokeStyle = col(C.white, 0.85); ctx.lineWidth = dpr; ctx.beginPath(); ctx.arc(P.x, P.y, r + 6 * dpr, 0, 7); ctx.stroke(); }
      if (lit) labels.push({ P: P, r: r, a: a, t: D.answers[answer].guests.filter(function (g) { return g.p === P.i; }).map(function (g) { return g.name; }).join(", ") });
      ctx.globalAlpha = 1;
    });
    names(labels);
  }
  /* each label to the right, left, above or below its pin, wherever it clears the ones already placed */
  function names(list) {
    var put = [], lh = 15 * dpr, pad = 4 * dpr;
    ctx.font = (11.5 * dpr) + "px " + FONT; ctx.textBaseline = "middle";
    list.forEach(function (L) {
      var w = ctx.measureText(L.t).width, x = L.P.x, y = L.P.y, g = L.r + 7 * dpr, spot = null;
      var tries = [[x + g, y], [x - g - w, y], [x - w / 2, y - g - lh / 2], [x - w / 2, y + g + lh / 2],
                   [x + g, y + lh * 1.1], [x + g, y - lh * 1.1], [x - g - w, y + lh * 1.1], [x - g - w, y - lh * 1.1]];
      for (var i = 0; i < tries.length && !spot; i++) {
        var b = [tries[i][0] - pad, tries[i][1] - lh / 2, w + 2 * pad, lh];
        if (b[0] < 0 || b[0] + b[2] > W || b[1] < 0 || b[1] + b[3] > H) continue;
        if (!put.some(function (o) { return b[0] < o[0] + o[2] && o[0] < b[0] + b[2] && b[1] < o[1] + o[3] && o[1] < b[1] + b[3]; })) spot = [tries[i], b];
      }
      if (!spot) spot = [tries[0], [tries[0][0] - pad, tries[0][1] - lh / 2, w + 2 * pad, lh]];
      put.push(spot[1]);
      ctx.globalAlpha = L.a; ctx.fillStyle = col(C.bg, 0.72); ctx.fillRect(spot[1][0], spot[1][1], spot[1][2], spot[1][3]);
      ctx.fillStyle = col(C.white, 0.95); ctx.fillText(L.t, spot[0][0], spot[0][1]); ctx.globalAlpha = 1;
    });
  }
  function proj(p) {
    var z = p[0] * F[0] + p[1] * F[1] + p[2] * F[2], x = p[0] * Ea[0] + p[1] * Ea[1], y = p[0] * N[0] + p[1] * N[1] + p[2] * N[2];
    return { x: cx + R * x, y: cy - R * y, ok: z > 0 || x * x + y * y > 1 };
  }
  function line(at, n) {
    ctx.beginPath(); var up = false;
    for (var i = 0; i <= n; i++) {
      var v = at(i / n), z = v[0] * F[0] + v[1] * F[1] + v[2] * F[2];
      if (z <= 0) { up = false; continue; }
      var p = proj(v); if (up) ctx.lineTo(p.x, p.y); else ctx.moveTo(p.x, p.y); up = true;
    }
    ctx.stroke();
  }
  function slerp(a, b, t) {
    var d = Math.max(-1, Math.min(1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2])), w = Math.acos(d);
    if (w < 1e-6) return a.slice();
    var s = Math.sin(w), p = Math.sin((1 - t) * w) / s, q = Math.sin(t * w) / s;
    return [a[0] * p + b[0] * q, a[1] * p + b[1] * q, a[2] * p + b[2] * q];
  }
  function arcs() {
    var A = D.answers[answer], seen = {};
    A.guests.forEach(function (g) {
      if (seen[g.p]) return; seen[g.p] = 1;
      var B = places[g.p].v, d = Math.acos(Math.max(-1, Math.min(1, OSLO[0] * B[0] + OSLO[1] * B[1] + OSLO[2] * B[2])));
      if (d < 0.01) return;
      var n = 64, end = Math.max(1, Math.round(n * grow)), lift = 0.08 + 0.25 * d / Math.PI;
      [[col(C.orange, 0.18), 5 * dpr], [col(C.orange, 0.95), 1.4 * dpr]].forEach(function (st) {
        ctx.strokeStyle = st[0]; ctx.lineWidth = st[1]; ctx.lineCap = "round"; ctx.beginPath(); var up = false;
        for (var i = 0; i <= end; i++) {
          var t = i / n, v = slerp(OSLO, B, t), h = 1 + lift * Math.sin(Math.PI * t);
          var p = proj([v[0] * h, v[1] * h, v[2] * h]);
          if (!p.ok) { up = false; continue; }
          if (up) ctx.lineTo(p.x, p.y); else ctx.moveTo(p.x, p.y); up = true;
        }
        ctx.stroke();
      });
    });
  }

  /* moving it: the visitor's hand, a gentle flight to a pin, the lines drawing in */
  var raf = 0, vel = null, flight = null;
  function frame(now) {
    raf = 0; var more = false;
    if (flight) {
      var t = Math.min(1, (now - flight.t) / flight.ms), e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      view.lat = flight.a.lat + (flight.b.lat - flight.a.lat) * e; view.lon = flight.a.lon + flight.dl * e;
      view.zoom = flight.a.zoom + (flight.b.zoom - flight.a.zoom) * e;
      if (t < 1) more = true; else flight = null;
    } else if (vel) {
      view.lon -= vel.x; view.lat = clampLat(view.lat + vel.y); vel.x *= 0.92; vel.y *= 0.92;
      if (Math.abs(vel.x) + Math.abs(vel.y) > 0.01) more = true; else vel = null;
    }
    if (answer >= 0 && grow < 1) { grow = Math.min(1, (now - t0) / 1100); more = more || grow < 1; }
    if (shift !== shiftTo) { shift += (shiftTo - shift) * 0.16; if (Math.abs(shiftTo - shift) < 0.5) shift = shiftTo; else more = true; }
    draw();
    if (more) raf = requestAnimationFrame(frame);
  }
  function kick() { if (!raf) raf = requestAnimationFrame(frame); }
  function clampLat(l) { return Math.max(-70, Math.min(75, l)); }
  function fly(lat, lon, zoom) {
    var b = { lat: clampLat(lat), lon: lon, zoom: zoom || view.zoom };
    var dl = ((b.lon - view.lon + 540) % 360) - 180;
    vel = null;
    if (still) { view.lat = b.lat; view.lon += dl; view.zoom = b.zoom; draw(); return; }
    flight = { a: { lat: view.lat, lon: view.lon, zoom: view.zoom }, b: b, dl: dl, t: performance.now(), ms: 950 }; kick();
  }

  var drag = null, pts = {}, moved = 0;
  cv.addEventListener("pointerdown", function (e) {
    pts[e.pointerId] = { x: e.clientX, y: e.clientY };
    cv.setPointerCapture(e.pointerId); flight = null; vel = null; moved = 0;
    drag = { x: e.clientX, y: e.clientY, t: performance.now(), vx: 0, vy: 0 };
    box.classList.add("is-drag");
  });
  cv.addEventListener("pointermove", function (e) {
    var ids = Object.keys(pts);
    if (pts[e.pointerId] && ids.length === 2) {       /* two fingers: zoom */
      var o = pts[ids[0]], p = pts[ids[1]], d0 = Math.hypot(o.x - p.x, o.y - p.y);
      pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      o = pts[ids[0]]; p = pts[ids[1]];
      var d1 = Math.hypot(o.x - p.x, o.y - p.y); if (d0 > 0) zoomBy(d1 / d0); moved = 99; return;
    }
    if (drag && pts[e.pointerId]) {
      var dx = e.clientX - drag.x, dy = e.clientY - drag.y, now = performance.now(), k = DEG / (R / dpr);
      moved += Math.abs(dx) + Math.abs(dy);
      view.lon -= dx * k; view.lat = clampLat(view.lat + dy * k);
      drag.vx = dx * k; drag.vy = dy * k; drag.x = e.clientX; drag.y = e.clientY; drag.t = now;
      hide(); kick(); return;
    }
    hit(e);
  });
  function up(e) {
    delete pts[e.pointerId];
    if (!drag) return;
    box.classList.remove("is-drag");
    if (moved < 6) { hit(e); if (hover >= 0) open(hover); }
    else if (!still && performance.now() - drag.t < 80) { vel = { x: drag.vx, y: drag.vy }; kick(); }
    drag = null;
  }
  cv.addEventListener("pointerup", up); cv.addEventListener("pointercancel", up);
  cv.addEventListener("pointerleave", function () { if (!drag) { hover = -1; hide(); box.classList.remove("is-pin"); draw(); } });
  /* a pinch on a trackpad comes as a wheel with ctrl; a plain wheel scrolls the page */
  cv.addEventListener("wheel", function (e) { if (!e.ctrlKey) return; e.preventDefault(); zoomBy(Math.exp(-e.deltaY * 0.01)); }, { passive: false });
  function zoomBy(f) { view.zoom = Math.max(0.8, Math.min(3.2, view.zoom * f)); flight = null; kick(); }
  box.addEventListener("keydown", function (e) {
    var k = { ArrowLeft: [0, -8], ArrowRight: [0, 8], ArrowUp: [6, 0], ArrowDown: [-6, 0] }[e.key];
    if (k) { e.preventDefault(); fly(view.lat + k[0], view.lon + k[1]); }
    else if (e.key === "+" || e.key === "=") zoomBy(1.25); else if (e.key === "-") zoomBy(0.8);
  });
  root.querySelectorAll(".atl-ctl button").forEach(function (b) {
    b.addEventListener("click", function () {
      var z = +b.getAttribute("data-z");
      if (z > 0) zoomBy(1.3); else if (z < 0) zoomBy(1 / 1.3); else { close(); fly(home.lat, home.lon, home.zoom); }
    });
  });

  /* pointing at a pin */
  var tip = box.querySelector(".atl-tip");
  function hit(e) {
    var r = cv.getBoundingClientRect(), x = (e.clientX - r.left) * dpr, y = (e.clientY - r.top) * dpr, best = -1, bd = 18 * dpr;
    places.forEach(function (P) {
      if (P.z <= 0.05) return; var d = Math.hypot(P.x - x, P.y - y) - P.r;
      if (d < bd) { bd = d; best = P.i; }
    });
    if (best !== hover) { hover = best; draw(); }
    box.classList.toggle("is-pin", best >= 0);
    if (best < 0) { hide(); return; }
    var P = places[best], n = P.p.eps.length;
    tip.innerHTML = "<b>" + esc(P.names.slice(0, 3).join(", ") + (P.names.length > 3 ? " and " + (P.names.length - 3) + " more" : "")) +
      "</b><span>" + (P.p.home ? "Oslo, home" : fmt(P.p.km) + " km " + P.p.card + " of Oslo") + " &middot; " + n + (n === 1 ? " conversation" : " conversations") + "</span>";
    tip.style.left = P.x / dpr + "px"; tip.style.top = (P.y - P.r) / dpr + "px"; tip.hidden = false;
  }
  function hide() { tip.hidden = true; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

  /* the panel: a pin's conversations and questions, or an answer */
  var panel = root.querySelector(".atl-panel"), body = panel.querySelector(".atl-body"), back = null;
  function room() {
    shiftTo = !panel.hidden && window.innerWidth > 900 ? (panel.offsetWidth + 16) * dpr / 2 : 0;
    if (still) shift = shiftTo; kick();
  }
  function show(html) {
    body.innerHTML = html; panel.hidden = false; panel.scrollTop = 0; room();
    body.querySelectorAll("a[data-u]").forEach(function (a) { a.setAttribute("href", a.getAttribute("data-u")); });
    requestAnimationFrame(function () { panel.classList.add("is-open"); });
  }
  function close() {
    panel.classList.remove("is-open"); panel.hidden = true; pick = -1; setAnswer(-1); room(); draw();
    if (back && back.focus) back.focus(); back = null;
  }
  panel.querySelector(".atl-x").addEventListener("click", close);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) close(); });
  function open(i) {
    var P = places[i], p = P.p; pick = i; setAnswer(-1); hide();
    var h = '<span class="atl-k">' + (p.home ? "Oslo, home" : fmt(p.km) + " km " + p.card + " of Oslo") + "</span><h2>" + esc(P.names.join(", ")) + "</h2>";
    h += "<h3>" + p.eps.length + (p.eps.length === 1 ? " conversation" : " conversations") + "</h3><ul>";
    p.eps.forEach(function (s) { var x = D.eps[s]; h += '<li><a data-u="../../episodes/' + s + '.html"><small>' + esc(x.n + " · " + x.s + " · " + x.d) + "</small>" + esc(x.t) + "</a></li>"; });
    h += "</ul>";
    if (p.deep.length) {
      h += "<h3>Answered in depth</h3><ul>";
      p.deep.forEach(function (k) { h += '<li><button type="button" data-a="' + k + '">' + esc(D.answers[k].q) + "</button></li>"; });
      h += "</ul>";
    }
    if (p.qs.length) {
      h += "<h3>" + p.qs.length + (p.qs.length === 1 ? " question" : " questions") + " these conversations answer</h3><ul>";
      p.qs.slice(0, 6).forEach(function (k) { h += '<li><a data-u="' + D.qs[k].href + '">' + esc(D.qs[k].q) + "</a></li>"; });
      h += "</ul>";
      if (p.qs.length > 6) h += '<p class="atl-more">And ' + (p.qs.length - 6) + ' more in the list under the globe.</p>';
    }
    show(h); fly(p.lat - 8, p.lon, Math.max(view.zoom, 1.15));
  }
  var qlinks = [].slice.call(root.querySelectorAll(".atl-qs a[data-a]"));
  function setAnswer(k) {
    answer = k; qlinks.forEach(function (a) { a.setAttribute("aria-current", String(+a.getAttribute("data-a") === k)); });
  }
  function openAnswer(k) {
    var A = D.answers[k]; pick = -1; setAnswer(k); hide(); grow = still ? 1 : 0; t0 = performance.now();
    var h = '<span class="atl-k">' + esc(A.topic || "Answered in depth") + "</span><h2>" + esc(A.q) + "</h2><p>" + esc(A.short) + "</p>";
    if (A.guests.length) {
      h += "<h3>From the show</h3><ul>";
      A.guests.forEach(function (g) { h += '<li><button type="button" data-p="' + g.p + '"><small>' + esc(D.eps[g.ep].s) + "</small>" + esc(g.name) + "</button></li>"; });
      h += "</ul>";
    }
    h += '<a class="atl-go" data-u="' + A.slug + '.html">Read the answer &rarr;</a>';
    show(h);
    /* turn to the middle of Oslo and the guests */
    var s = [OSLO[0], OSLO[1], OSLO[2]];
    A.guests.forEach(function (g) { var v = places[g.p].v; s[0] += v[0]; s[1] += v[1]; s[2] += v[2]; });
    var l = Math.hypot(s[0], s[1], s[2]) || 1;
    fly(Math.asin(s[2] / l) * DEG - 6, Math.atan2(s[1], s[0]) * DEG, 1); kick();
  }
  body.addEventListener("click", function (e) {
    var a = e.target.closest("[data-a]"), p = e.target.closest("[data-p]");
    if (a) openAnswer(+a.getAttribute("data-a")); else if (p) open(+p.getAttribute("data-p"));
  });
  qlinks.forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault(); back = a; openAnswer(+a.getAttribute("data-a"));
      if (window.innerWidth <= 900) box.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" });
    });
  });

  if (window.ResizeObserver) new ResizeObserver(size).observe(box); else window.addEventListener("resize", size);
  size();
})();
"""


def page(shell, src_dir):
    """The Atlas page, in the frame of the A to Z's v4 twin (shell): its head's tail, nav and footer."""
    d = data(src_dir)
    n_eps, n_qs = len(d["eps"]), len(d["qs"])
    title = "The Atlas: Every Story And Answer On A Globe | Paragliding Atlas"
    desc = ("The %d conversations on the Paragliding Atlas podcast, each pinned where its story comes from, "
            "with the %d questions they answer and the encyclopedia's answers in depth." % (n_eps, n_qs))
    url = "https://paraglidingatlas.com/knowledge-base/encyclopedia/atlas.html"
    head, body = shell.split("</head>", 1)
    tail = head[head.index('<link rel="icon"'):]
    tail = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", tail, flags=re.S)
    tail = tail.replace("<style>.az-list li[hidden],.az-group[hidden]{display:none}</style>\n", "")
    head = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>%s</title>\n'
            '<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n'
            '<meta property="og:type" content="website">\n<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n'
            '<meta property="og:image" content="https://paraglidingatlas.com/assets/images/kb-technical.jpg">\n'
            '<meta property="og:url" content="%s">\n<meta name="twitter:card" content="summary_large_image">\n'
            % (E(title), E(desc, True), url, E(title, True), E(desc, True), url)) + tail + "<style>%s</style>\n" % CSS
    a = body.index('<header class="k-hero')
    b = body.index("</div><!-- /.page-wrap -->")
    # the shell's own scripts after the footer (the A to Z's list and the series pages' layer) do not belong here
    end = body[b:]
    end = re.sub(r"<script>.*?</script>\s*", "", end, flags=re.S)
    qs = "".join('<li><a href="%s.html" data-a="%d"><span>%02d</span>%s</a></li>' % (x["slug"], i, i + 1, E(x["q"]))
                 for i, x in enumerate(d["answers"]))
    lst = []
    for p in d["places"]:
        names = []
        for s in p["eps"]:
            if d["eps"][s]["g"] not in names:
                names.append(d["eps"][s]["g"])
        where = "Oslo, home" if p["home"] else "%s km %s of Oslo" % ("{:,}".format(p["km"]), p["card"])
        eps = "".join('<li><a href="../../episodes/%s.html">%s</a></li>' % (s, E(d["eps"][s]["t"])) for s in p["eps"])
        qq = ""
        if p["qs"]:
            qq = ('<details><summary>%d %s these conversations answer</summary><ul>%s</ul></details>'
                  % (len(p["qs"]), "question" if len(p["qs"]) == 1 else "questions",
                     "".join('<li><a href="%s">%s</a></li>' % (d["qs"][k]["href"], E(d["qs"][k]["q"])) for k in p["qs"])))
        lst.append('<li><span class="atl-k">%s</span><h3>%s</h3><ul>%s</ul>%s</li>' % (where, E(", ".join(names)), eps, qq))
    blob = json.dumps(d, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    main = (
        '<div class="atl" id="atlas">'
        '<section class="atl-stage" aria-labelledby="atlT">'
        '<div class="atl-copy"><p class="breadcrumb"><a href="../../knowledge-base.html">Knowledge Base</a> / '
        '<a href="index.html">Encyclopedia</a> / The Atlas</p>'
        '<span class="atl-k">Encyclopedia &middot; The Atlas</span>'
        '<h1 class="atl-title" id="atlT">Every Story, <em>Every Answer</em></h1>'
        '<p class="atl-lead">The %d conversations on the show, each pinned where its story comes from, and the %d '
        'questions they answer. Turn the globe and choose a pin, or start from a question.</p></div>'
        '<div class="atl-globe" tabindex="0" aria-label="The globe of the show&#x27;s conversations: drag or use the arrow keys '
        'to turn it. Every pin is also in the list under it."><canvas aria-hidden="true"></canvas>'
        '<div class="atl-tip" hidden></div><p class="atl-hint">Drag to turn the globe</p>'
        '<div class="atl-ctl"><button type="button" data-z="1" aria-label="Zoom in">+</button>'
        '<button type="button" data-z="-1" aria-label="Zoom out">&minus;</button>'
        '<button type="button" data-z="0">Reset</button></div>'
        '<aside class="atl-panel" hidden aria-live="polite"><button type="button" class="atl-x" aria-label="Close">&times;</button>'
        '<div class="atl-body"></div></aside></div>'
        '<div class="atl-qs"><span class="atl-qs-h">Answered in depth</span><ol>%s</ol>'
        '<a class="atl-az" href="index.html">Every question, A to Z &rarr;</a></div>'
        '</section>'
        '<section class="atl-list" aria-labelledby="atlListT"><h2 id="atlListT">Every Pin, As A List</h2>'
        '<p>The same conversations, nearest to Oslo first, with the questions each place&#x27;s conversations answer.</p>'
        '<ul class="atl-places">%s</ul></section>'
        '</div>\n'
        % (n_eps, n_qs, qs, "".join(lst)))
    data_tag = '<script type="application/json" id="atlasData">%s</script>\n<script>%s</script>\n' % (blob, JS)
    end = end.replace("</body>", data_tag + "</body>", 1)
    return head + "</head>" + body[:a] + main + end

if __name__ == "__main__":
    import sys
    d = data(os.path.join(ROOT, "prototypes", "workspace", "drafts", "knowledge-base", "encyclopedia"))
    s = json.dumps(d, separators=(",", ":"), ensure_ascii=False)
    print("places %d, episodes %d, questions %d (placed %d), answers %d, land rows %d, dots %d, json %d KB" % (
        len(d["places"]), len(d["eps"]), len(d["qs"]), sum(len(p["qs"]) for p in d["places"]), len(d["answers"]),
        len(d["land"]["rows"]), sum(bin(int(h, 16)).count("1") for _, h in d["land"]["rows"] if h), len(s) // 1024))
    for a in d["answers"]:
        print(" ", a["slug"][:40], [g["name"] for g in a["guests"]])
    sys.exit(0)
