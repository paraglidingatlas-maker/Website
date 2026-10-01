#!/usr/bin/env python3
"""
Two prototypes for the trip pages' route section, on a copy of the Kenya page
(owner, 1 Oct 2026: "fix the map section in kenya and then use same in india",
then "a", my pick, "but I wanna see a proto of c as well").

  A  flight down the Rift   the section holds still; the route is a line
                            diagram (stations spaced by the page's own leg
                            distances) that the camera follows site by site,
                            each site's photograph (or, where the page has
                            none, the chart's relief around it) full screen
                            behind, a km-along-the-route counter
  C  zoom from orbit        the section holds still; the camera falls from
                            the continent to Kenya to the Rift, then the route
                            draws itself site by site with each site's card

Everything shown is on the page already: site names, coordinates, lines,
legs (bearing and km), photographs, the chart's relief image. Outlines are
Natural Earth (public domain; tools/data/natural-earth-trips.json, from the
world-atlas package, 50m countries and 110m land). Reduced motion or no
script: the final picture, still, with the sites listed under it.

    python3 tools/v4_map_options.py   # writes prototypes/v4/samples/map-a.html and map-c.html
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "destinations", "kenya.html")
GEO = json.load(open(os.path.join(ROOT, "tools", "data", "natural-earth-trips.json")))
TERRAIN = "../../../assets/destinations/kenya/map/kenya-sheet-terrain.webp"
# the chart sheet's projection (assets/destinations/kenya/map/kenya-sheet.svg): 300 px a degree, 35°E at x 360, the equator at y 480
SHEET = dict(lon0=35 - 360 / 300.0, lat0=480 / 300.0, w=1800 / 300.0, h=1440 / 300.0)
K = 40.0                                   # this drawing: 40 units a degree, equirectangular


def X(lon):
    return (lon + 20) * K


def Y(lat):
    return (40 - lat) * K


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def esc(s):
    return html.escape(s, quote=True)


def ring_path(r):
    pts, last = [], None
    for lon, lat in r:
        p = (round(X(lon), 1), round(Y(lat), 1))
        if last is None or abs(p[0] - last[0]) + abs(p[1] - last[1]) >= .25:
            pts.append(p)
            last = p
    if len(pts) < 3:
        return ""
    return "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts) + "Z"


def sites(src):
    i = src.index('id="route"')
    i = src.rindex("<section", 0, i)
    j = src.index("</section>", i) + len("</section>")
    sec = src[i:j]
    out = []
    for panel in re.findall(r'class="kmap-row[^"]*"[^>]*data-panel="([^"]*)"', sec):
        p = html.unescape(panel)
        name = re.search(r"<h3>([^<]*)</h3>", p).group(1)
        co = re.search(r'<p class="kmap-coord">([^<]*)</p>', p).group(1)
        m = re.match(r"([\d.]+)°([NS]) · ([\d.]+)°([EW])", co)
        lat = float(m.group(1)) * (1 if m.group(2) == "N" else -1)
        lon = float(m.group(3)) * (1 if m.group(4) == "E" else -1)
        paras = re.findall(r"<p>([^<]*)</p>", p)
        leg = re.search(r'<p class="kmap-leg">([^<]*)</p>', p)
        km = int(re.search(r"(\d+) km", leg.group(1)).group(1)) if leg else 0
        pic = re.search(r"<picture>.*?</picture>", p, re.S)
        photo = None
        if pic:
            photo = dict(webp=re.search(r'srcset="([^"]+)"', pic.group(0)).group(1),
                         jpg=re.search(r' src="([^"]+)"', pic.group(0)).group(1),
                         alt=re.search(r'alt="([^"]*)"', pic.group(0)).group(1))
        out.append(dict(name=html.unescape(name), co=co, lat=lat, lon=lon, text=html.unescape(paras[0]) if paras else "",
                        leg=html.unescape(leg.group(1)) if leg else "", km=km, photo=photo))
    head = re.search(r'<span class="kicker">([^<]*)</span>\s*<h2 id="route-h">([^<]*)</h2>\s*<p>(.*?)</p>', sec, re.S)
    return out, (head.group(1), html.unescape(head.group(2)), re.sub(r"\s+", " ", html.unescape(head.group(3)))), (i, j)


def card(s, k, n):
    pic = ""
    if s["photo"]:
        pic = '<picture><source srcset="%s" type="image/webp"><img src="%s" alt="%s" loading="lazy" decoding="async"></picture>' % (
            s["photo"]["webp"], s["photo"]["jpg"], esc(s["photo"]["alt"]))
    return ('<article class="mp-card" data-i="%d">%s<div class="mp-card-t"><span class="mp-n">%02d / %02d</span><h3>%s</h3>'
            '<p class="mp-co">%s</p><p>%s</p>%s</div></article>'
            % (k, pic, k + 1, n, esc(s["name"]), esc(s["co"]), esc(s["text"]), '<p class="mp-leg">%s</p>' % esc(s["leg"]) if s["leg"] else ""))


COMMON_CSS = """
.mp{padding:0 !important;position:relative;background:#0d0e11;}
.mp-track{height:calc(var(--n) * 70vh + 140vh);position:relative;}
.mp-pin{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;}
.mp-head{position:absolute;z-index:4;left:var(--gutter);top:clamp(5.5rem,12vh,7.5rem);max-width:30rem;transition:opacity .6s ease;}
.mp-head h2{margin:.35rem 0 .5rem;font-size:var(--fs-h2);color:#fff;}
.mp-head p{margin:0;color:rgba(246,244,244,.75);font-size:var(--fs-body-s);line-height:1.6;}
.mp-km{position:absolute;z-index:4;right:var(--gutter);top:clamp(5.5rem,12vh,7.5rem);text-align:right;color:rgba(246,244,244,.65);font-size:var(--fs-micro);letter-spacing:.18em;text-transform:uppercase;}
.mp-km b{display:block;font-family:var(--font-display);font-size:clamp(2rem,4vw,3.2rem);color:#fff;letter-spacing:-.01em;font-variant-numeric:tabular-nums;text-transform:none;line-height:1;}
.mp-km b small{font-size:.45em;color:var(--orange);margin-left:.25rem;}
.mp-cards{position:absolute;z-index:4;left:var(--gutter);bottom:clamp(2rem,6vh,4rem);width:min(26rem,calc(100% - 2 * var(--gutter)));}
.mp-card{position:absolute;left:0;bottom:0;width:100%;background:rgba(14,15,18,.82);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  border:1px solid rgba(246,244,244,.1);border-top:2px solid var(--orange);opacity:0;transform:translateY(16px);transition:opacity .5s ease,transform .5s cubic-bezier(.2,.8,.2,1);pointer-events:none;}
.mp-card.is-on{opacity:1;transform:none;pointer-events:auto;}
.mp-card picture,.mp-card img{display:block;width:100%;aspect-ratio:16/8;object-fit:cover;}
.mp-card-t{padding:1rem 1.2rem 1.1rem;}
.mp-card h3{margin:.2rem 0 .1rem;font-size:1.25rem;color:#fff;}
.mp-n{font-size:var(--fs-micro);letter-spacing:.2em;color:var(--orange);font-weight:600;}
.mp-co{margin:0 0 .5rem;font-size:var(--fs-micro);letter-spacing:.12em;color:var(--gray);font-variant-numeric:tabular-nums;}
.mp-card p{font-size:var(--fs-small);line-height:1.55;color:rgba(246,244,244,.82);margin:0;}
.mp-card .mp-leg{margin-top:.6rem;color:var(--orange);font-size:var(--fs-micro);letter-spacing:.12em;}
.mp-skip{position:absolute;z-index:4;right:var(--gutter);bottom:clamp(1.4rem,4vh,2.2rem);min-height:44px;display:inline-flex;align-items:center;gap:.4rem;color:rgba(246,244,244,.7);font-size:var(--fs-small);text-decoration:none;}
.mp-skip:hover,.mp-skip:focus-visible{color:var(--orange);}
@media (max-width:760px){
  .mp-head{right:7.5rem;} .mp-head p{display:none;} .mp-head h2{font-size:var(--fs-h3);} .mp-cards{bottom:5.2rem;} .mp-card picture,.mp-card img{aspect-ratio:16/6;}
  .mp-card p:not(.mp-co):not(.mp-leg){display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}
  .mp-skip{left:var(--gutter);right:auto;bottom:4.6rem;}
}
@media (prefers-reduced-motion:reduce),(scripting:none){
  .mp-track{height:auto;} .mp-pin{position:static;height:auto;overflow:visible;display:flex;flex-direction:column;}
  .mp-head{position:static;padding:var(--sp-5) var(--gutter) var(--sp-3);order:-1;} .mp-km,.mp-skip{display:none;}
  .mp-cards{position:static;width:auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,18rem),1fr));gap:1rem;padding:var(--sp-3) var(--gutter) var(--sp-5);}
  .mp-card{position:static;opacity:1;transform:none;}
}
"""


# ---------------------------------------------------------------- C: zoom from orbit
def map_svg(ss, label_aria):
    land = "".join('<path d="%s"/>' % ring_path(r) for r in GEO["land"])
    ctry = ""
    for name, rings in GEO["countries"].items():
        d = "".join(ring_path(r) for r in rings)
        ctry += '<path class="%s" d="%s"/>' % ("mpc-ke" if name == "Kenya" else "mpc-nb", d)
    grat = ""
    for lon in range(-20, 61, 10):
        grat += '<path class="mpc-g1" d="M%s,%s V%s"/>' % (f(X(lon)), f(Y(40)), f(Y(-40)))
    for lat in range(-40, 41, 10):
        grat += '<path class="mpc-g1%s" d="M%s,%s H%s"/>' % (" mpc-eq" if lat == 0 else "", f(X(-20)), f(Y(lat)), f(X(60)))
    for lon in range(34, 40):
        grat += '<path class="mpc-g2" d="M%s,%s V%s"/>' % (f(X(lon)), f(Y(4)), f(Y(-5)))
    for lat in range(-4, 4):
        grat += '<path class="mpc-g2" d="M%s,%s H%s"/>' % (f(X(33)), f(Y(lat)), f(X(41)))
    tx, ty = X(SHEET["lon0"]), Y(SHEET["lat0"])
    terrain = '<image class="mpc-terrain" href="%s" x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none"/>' % (
        TERRAIN, f(tx), f(ty), f(SHEET["w"] * K), f(SHEET["h"] * K))
    pts = [(X(s["lon"]), Y(s["lat"])) for s in ss]
    route = "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts)
    marks = ""
    for k, (s, (x, y)) in enumerate(zip(ss, pts)):
        side = -1 if k in (1,) else 1
        end = " is-end" if k in (0, len(ss) - 1) else ""
        marks += ('<g class="mpc-site%s" data-i="%d"><circle class="mpc-ring" cx="%s" cy="%s" r="9"/><circle class="mpc-dot" cx="%s" cy="%s" r="3.2"/>'
                  '<text class="%s" x="%s" y="%s" text-anchor="%s">%s</text></g>'
                  % (end, k, f(x), f(y), f(x), f(y), "is-r" if side > 0 else "is-l", f(x), f(y), "start" if side > 0 else "end", esc(s["name"].upper())))
    ke = [p for r in GEO["countries"]["Kenya"] for p in r]
    kx = (min(p[0] for p in ke) + max(p[0] for p in ke)) / 2
    ky = (min(p[1] for p in ke) + max(p[1] for p in ke)) / 2
    keys = {"africa": [X(18), Y(2), 95 * K], "kenya": [X(kx), Y(ky), 11 * K],
            "sites": [[round(x, 1), round(y, 1)] for x, y in pts]}
    label = '<text class="mpc-cn" x="%s" y="%s" text-anchor="middle">KENYA</text>' % (f(X(kx + 1.6)), f(Y(ky + 1.4)))
    eq = '<text class="mpc-eqt" x="%s" y="%s">EQUATOR</text>' % (f(X(41.2)), f(Y(0) - 6))
    svg = ('<svg class="mpc-map" viewBox="%s" preserveAspectRatio="xMidYMid slice" role="img" aria-label="%s">'
           '<rect x="-4000" y="-4000" width="12000" height="12000" fill="#0d0e11"/>'
           '<g class="mpc-land">%s</g>%s<g class="mpc-grat">%s</g><g class="mpc-ctry">%s</g>%s%s'
           '<path class="mpc-route0" d="%s"/><path class="mpc-route" d="%s"/>%s</svg>'
           % ("%s %s %s %s" % (f(X(18) - 47.5 * K), f(Y(2) - 40 * K), f(95 * K), f(80 * K)), esc(label_aria),
              land, terrain, grat, ctry, label, eq, route, route, marks))
    return svg, keys


def proto_c(ss, head):
    n = len(ss)
    svg, keys = map_svg(ss, "Map of Africa narrowing to Kenya and the six sites of the route")
    cards = "".join(card(s, k, n) for k, s in enumerate(ss))
    kms = [sum(s["km"] for s in ss[:k + 1]) for k in range(n)]
    body = ('<section class="dst-sec mp mpc" id="route" aria-labelledby="route-h" style="--n:%d" data-keys="%s" data-km="%s">'
            '<div class="mp-track"><div class="mp-pin">'
            '%s'
            '<div class="mp-head"><span class="kicker">%s</span><h2 id="route-h">%s</h2><p>%s</p></div>'
            '<div class="mp-km" aria-hidden="true">along the route<b>0<small>km</small></b></div>'
            '<div class="mp-cards">%s</div>'
            '<a class="mp-skip" href="#gallery">Skip the map <i aria-hidden="true">&darr;</i></a>'
            '</div></div></section>'
            % (n, esc(json.dumps(keys)), esc(json.dumps(kms)), svg, esc(head[0]), esc(head[1]), esc(head[2]), cards))
    css = COMMON_CSS + MAP_CSS
    js = C_JS
    return body, css, js


MAP_CSS = """
.mpc-map{position:absolute;inset:0;width:100%;height:100%;display:block;}
.mpc-map path:not(.mpc-route),.mpc-map circle{vector-effect:non-scaling-stroke;}
.mpc-land path{fill:#16171c;stroke:rgba(246,244,244,.22);stroke-width:.8;}
.mpc-ctry .mpc-nb{fill:none;stroke:rgba(246,244,244,.18);stroke-width:.7;}
.mpc-ctry .mpc-ke{fill:rgba(255,179,92,.07);stroke:#ffcf94;stroke-width:1.4;}
.mpc-g1{fill:none;stroke:rgba(246,244,244,.06);stroke-width:.6;}
.mpc-g1.mpc-eq,.mpc-g2{fill:none;stroke:rgba(246,244,244,.14);stroke-width:.6;stroke-dasharray:6 5;}
.mpc-g2{opacity:var(--fine,0);}
.mpc-terrain{opacity:var(--ter,0);mix-blend-mode:screen;}
.mpc-cn{font:600 calc(var(--u,1) * 26px) var(--font-body);letter-spacing:.4em;fill:#ffcf94;opacity:var(--cn,0);}
.mpc-eqt{font:600 calc(var(--u,1) * 10px) var(--font-body);letter-spacing:.3em;fill:rgba(246,244,244,.45);opacity:var(--fine,0);}
.mpc-route0{fill:none;stroke:rgba(246,244,244,.18);stroke-width:1;stroke-dasharray:3 5;opacity:var(--fine,0);}
.mpc-route{fill:none;stroke:#ff7517;stroke-width:calc(var(--u,1) * 2.6px);stroke-linecap:round;stroke-linejoin:round;}
.mpc-site{opacity:var(--fine,0);}
.mpc-site .mpc-dot{r:calc(var(--u,1) * 5px);fill:#141519;stroke:rgba(246,244,244,.8);stroke-width:1.4;}
.mpc-site .mpc-ring{r:calc(var(--u,1) * 13px);fill:none;stroke:#ff7517;stroke-width:1.2;opacity:0;transition:opacity .4s ease;}
.mpc-site.is-past .mpc-dot{fill:#ff7517;stroke:#ff7517;}
.mpc-site.is-on .mpc-ring{opacity:1;}
.mpc-site text{font:600 calc(var(--u,1) * 13px) var(--font-body);letter-spacing:.16em;fill:rgba(246,244,244,.75);paint-order:stroke;stroke:#0d0e11;
  stroke-width:calc(var(--u,1) * 4px);stroke-linejoin:round;opacity:0;transition:opacity .4s ease;}
.mpc-site text.is-r{transform:translate(calc(var(--u,1) * 20px),calc(var(--u,1) * 4px));}
.mpc-site text.is-l{transform:translate(calc(var(--u,1) * -20px),calc(var(--u,1) * 4px));}
.mpc-site.is-end text{opacity:.7;}
.mpc-site.is-on text{opacity:1;fill:#fff;}
@media (max-width:760px){
  /* on a phone the site's name sits above its mark, so it never runs off the edge */
  .mpc-site text.is-r,.mpc-site text.is-l{text-anchor:middle;transform:translate(0,calc(var(--u,1) * -20px));}
}
@media (prefers-reduced-motion:reduce),(scripting:none){ .mpc-map{position:relative;height:70vh;} .mpc-g2,.mpc-route0,.mpc-site,.mpc-eqt,.mpc-site text{opacity:1;} .mpc-terrain{opacity:.8;} }
"""

C_JS = """
(function () {
  var sec = document.querySelector('.mpc'); if (!sec) return;
  var keys = JSON.parse(sec.dataset.keys), kms = JSON.parse(sec.dataset.km), n = keys.sites.length;
  var svg = sec.querySelector('.mpc-map'), track = sec.querySelector('.mp-track'), route = sec.querySelector('.mpc-route');
  var sites = [].slice.call(sec.querySelectorAll('.mpc-site')), cards = [].slice.call(sec.querySelectorAll('.mp-card'));
  var head = sec.querySelector('.mp-head'), km = sec.querySelector('.mp-km b'), len = route.getTotalLength(), raf = 0, at = -2;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // the route's extent: the camera's third stop, the whole Rift in view
  var xs = keys.sites.map(function (p) { return p[0]; }), ys = keys.sites.map(function (p) { return p[1]; });
  var rift = [(Math.min.apply(0, xs) + Math.max.apply(0, xs)) / 2, (Math.min.apply(0, ys) + Math.max.apply(0, ys)) / 2, (Math.max.apply(0, xs) - Math.min.apply(0, xs)) * 2.1];
  // the legs as fractions of the route's length on the drawing, so the line reaches each site as its card shows
  var cum = [0]; for (var i = 1; i < n; i++) { var a = keys.sites[i - 1], b = keys.sites[i]; cum.push(cum[i - 1] + Math.hypot(b[0] - a[0], b[1] - a[1])); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function cam(a, b, t) { t = t * t * (3 - 2 * t); return [lerp(a[0], b[0], t), lerp(a[1], b[1], t), Math.exp(lerp(Math.log(a[2]), Math.log(b[2]), t))]; }
  function view(c) {
    var r = svg.getBoundingClientRect(), w = c[2], h = w * r.height / Math.max(1, r.width);
    if (r.width < r.height) { h = c[2] * 1.15; w = h * r.width / r.height; }
    svg.setAttribute('viewBox', (c[0] - w / 2).toFixed(2) + ' ' + (c[1] - h / 2).toFixed(2) + ' ' + w.toFixed(2) + ' ' + h.toFixed(2));
    svg.style.setProperty('--u', (w / Math.max(1, r.width)).toFixed(4));   // map units per screen pixel: marks and words keep their size
  }
  function show(i) {
    if (i === at) return; at = i;
    cards.forEach(function (c, k) { c.classList.toggle('is-on', k === i); });
    sites.forEach(function (s, k) { s.classList.toggle('is-on', k === i); s.classList.toggle('is-past', k <= i && i >= 0); });
  }
  if (reduce) { view(rift); route.style.strokeDasharray = 'none'; sites.forEach(function (s) { s.classList.add('is-past'); }); return; }
  route.style.strokeDasharray = len; route.style.strokeDashoffset = len;
  function frame() {
    raf = 0;
    var r = track.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
    var c, fine = 0, ter = 0, cn = 0, drawn = 0, cur = -1;
    if (p < .22) { c = cam(keys.africa, keys.kenya, p / .22); cn = Math.max(0, (p - .1) / .12); }
    else if (p < .36) { var t = (p - .22) / .14; c = cam(keys.kenya, rift, t); cn = 1 - t; fine = t; ter = t * .85; }
    else {
      fine = 1; ter = .85;
      var q = (p - .36) / .64, x = Math.min(n - 1, q * (n - 1) * 1.08);
      cur = Math.min(n - 1, Math.round(x));
      var i0 = Math.floor(x), t2 = x - i0, s0 = keys.sites[i0], s1 = keys.sites[Math.min(n - 1, i0 + 1)];
      var focus = [lerp(s0[0], s1[0], t2), lerp(s0[1], s1[1], t2), rift[2] * .62];
      c = cam(rift, focus, Math.min(1, q * 4));
      drawn = lerp(cum[i0], cum[Math.min(n - 1, i0 + 1)], t2) / cum[n - 1];
      km.innerHTML = Math.round(lerp(i0 ? kms[i0] : 0, kms[Math.min(n - 1, i0 + 1)], i0 + 1 < n ? t2 : 1)) + '<small>km</small>';
    }
    if (cur < 0) km.innerHTML = '0<small>km</small>';
    view(c);
    svg.style.setProperty('--fine', fine.toFixed(3)); svg.style.setProperty('--ter', ter.toFixed(3)); svg.style.setProperty('--cn', Math.min(1, cn).toFixed(3));
    route.style.strokeDashoffset = (len * (1 - drawn)).toFixed(1);
    head.style.opacity = p < .3 ? 1 : Math.max(0, 1 - (p - .3) / .06);
    show(cur);
  }
  addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(frame); }, { passive: true });
  addEventListener('resize', frame); frame();
})();"""


# ---------------------------------------------------------------- A: flight down the Rift
def proto_a(ss, head):
    n = len(ss)
    legs = [s["km"] for s in ss[1:]]
    # stations spaced by the legs, the short ones held to a readable minimum
    gaps = [max(60.0, k) for k in legs]
    xs = [0.0]
    for g in gaps:
        xs.append(xs[-1] + g * 2.2)
    W = xs[-1]
    stations = ""
    for k, (s, x) in enumerate(zip(ss, xs)):
        up = k % 2 == 0
        stations += ('<g class="mpa-st" data-i="%d" transform="translate(%s,0)"><path class="mpa-tick" d="M0,%s V%s"/><circle class="mpa-ring" r="11"/><circle class="mpa-dot" r="4.5"/>'
                     '<text class="mpa-name" y="%s" text-anchor="middle">%s</text><text class="mpa-co" y="%s" text-anchor="middle">%s</text></g>'
                     % (k, f(x), -8 if up else 8, -26 if up else 26, -44 if up else 50, esc(s["name"].upper()), -32 if up else 64, esc(s["co"])))
    legl = ""
    for k, (a, b) in enumerate(zip(xs, xs[1:])):
        legl += '<text class="mpa-legt" x="%s" y="22" text-anchor="middle">%d KM</text>' % (f((a + b) / 2), legs[k])
    line = "M0,0 H%s" % f(W)
    backs = ""
    for k, s in enumerate(ss):
        if s["photo"]:
            backs += ('<div class="mpa-bg" data-i="%d"><picture><source srcset="%s" type="image/webp"><img src="%s" alt="" loading="lazy" decoding="async"></picture></div>'
                      % (k, s["photo"]["webp"], s["photo"]["jpg"]))
        else:
            # no photograph on the page for this site: the map, held on the site
            backs += '<div class="mpa-bg is-map" data-i="%d"></div>' % k
    msvg, mkeys = map_svg(ss, "Map of the route with the current site marked")
    backs = '<div class="mpa-mapbg">%s</div>' % msvg + backs
    cards = "".join(card(dict(s, photo=None), k, n) for k, s in enumerate(ss))
    kms = [sum(s["km"] for s in ss[:k + 1]) for k in range(n)]
    body = ('<section class="dst-sec mp mpa" id="route" aria-labelledby="route-h" style="--n:%d" data-x="%s" data-km="%s" data-w="%s" data-keys="%s">'
            '<div class="mp-track"><div class="mp-pin">'
            '<div class="mpa-bgs" aria-hidden="true">%s</div>'
            '<div class="mp-head"><span class="kicker">%s</span><h2 id="route-h">%s</h2><p>%s</p></div>'
            '<div class="mp-km" aria-hidden="true">along the route<b>0<small>km</small></b></div>'
            '<div class="mpa-line" aria-hidden="true"><svg viewBox="-200 -80 %s 170" preserveAspectRatio="xMinYMid slice"><g class="mpa-move">'
            '<path class="mpa-l0" d="%s"/><path class="mpa-l1" d="%s"/>%s%s</g></svg></div>'
            '<div class="mp-cards">%s</div>'
            '<a class="mp-skip" href="#gallery">Skip the route <i aria-hidden="true">&darr;</i></a>'
            '</div></div></section>'
            % (n, esc(json.dumps([round(x, 1) for x in xs])), esc(json.dumps(kms)), f(W), esc(json.dumps(mkeys)),
               backs, esc(head[0]), esc(head[1]), esc(head[2]), f(W + 400), line, line, legl, stations, cards))
    css = COMMON_CSS + MAP_CSS + """
.mpa-bgs{position:absolute;inset:0;}
.mpa-mapbg{position:absolute;inset:0;opacity:0;transition:opacity 1s ease;}
.mpa-mapbg.is-on{opacity:1;}
.mpa-bg.is-map{display:none;}
.mpa-mapbg .mpc-site text{display:none;}   /* the line diagram names the sites */
.mpa-mapbg .mpc-map{--fine:1;--ter:.9;--cn:0;}
.mpa-bg{position:absolute;inset:0;opacity:0;transition:opacity 1s ease;background-size:520% auto;background-color:#0d0e11;}
.mpa-bg.is-on{opacity:1;}
.mpa-bg picture,.mpa-bg img{display:block;width:100%;height:100%;object-fit:cover;}
.mpa-bg img{transform:scale(calc(1.1 - .08 * var(--t,0)));}
.mpa-bgs::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,14,17,.7) 0%,rgba(13,14,17,.15) 35%,rgba(13,14,17,.35) 60%,rgba(13,14,17,.92) 100%);}
.mpa-line{position:absolute;z-index:3;left:0;right:0;bottom:clamp(14rem,32vh,18rem);height:150px;}
.mpa-line svg{width:100%;height:100%;overflow:visible;}
.mpa-move{transform:translateX(var(--sx,0px));}
.mpa-line path:not(.mpa-l1),.mpa-line circle{vector-effect:non-scaling-stroke;}
.mpa-l0{stroke:rgba(246,244,244,.35);stroke-width:1.5;stroke-dasharray:4 6;fill:none;}
.mpa-l1{stroke:#ff7517;stroke-width:3;fill:none;stroke-linecap:round;}
.mpa-tick{stroke:rgba(246,244,244,.4);stroke-width:1;}
.mpa-dot{fill:#0d0e11;stroke:#f6f4f4;stroke-width:1.5;transition:fill .3s ease;}
.mpa-ring{fill:none;stroke:#ff7517;stroke-width:1.2;opacity:0;transition:opacity .3s ease;}
.mpa-st.is-past .mpa-dot{fill:#ff7517;stroke:#ff7517;}
.mpa-st.is-on .mpa-ring{opacity:1;}
.mpa-name{font:600 13px var(--font-body);letter-spacing:.16em;fill:rgba(246,244,244,.6);transition:fill .3s ease;}
.mpa-st.is-on .mpa-name{fill:#fff;}
.mpa-co{font:500 10px var(--font-body);letter-spacing:.1em;fill:rgba(246,244,244,.45);}
.mpa-legt{font:600 10px var(--font-body);letter-spacing:.18em;fill:#ffcf94;opacity:.75;}
@media (max-width:760px){ .mpa-line{bottom:calc(5rem + 42vh);height:130px;} .mpa-co{display:none;} }
@media (prefers-reduced-motion:reduce),(scripting:none){
  .mpa-bgs{display:none;} .mpa-line{position:static;height:auto;padding:0 var(--gutter);overflow-x:auto;} .mpa-line svg{height:170px;width:auto;min-width:900px;}
  .mpa-st .mpa-dot{fill:#ff7517;stroke:#ff7517;}
}
"""
    js = """
(function () {
  var sec = document.querySelector('.mpa'); if (!sec) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var xs = JSON.parse(sec.dataset.x), kms = JSON.parse(sec.dataset.km), W = +sec.dataset.w, n = xs.length;
  var track = sec.querySelector('.mp-track'), move = sec.querySelector('.mpa-move'), l1 = sec.querySelector('.mpa-l1');
  var svg = sec.querySelector('.mpa-line svg'), sts = [].slice.call(sec.querySelectorAll('.mpa-st')), cards = [].slice.call(sec.querySelectorAll('.mp-card'));
  var bgs = [].slice.call(sec.querySelectorAll('.mpa-bg')), head = sec.querySelector('.mp-head'), km = sec.querySelector('.mp-km b'), at = -2, raf = 0;
  l1.style.strokeDasharray = W; l1.style.strokeDashoffset = W;
  var mapbg = sec.querySelector('.mpa-mapbg'), msvg = mapbg.querySelector('svg'), mkeys = JSON.parse(sec.dataset.keys);
  var msites = [].slice.call(mapbg.querySelectorAll('.mpc-site')), mroute = mapbg.querySelector('.mpc-route');
  var xs2 = mkeys.sites.map(function (p) { return p[0]; }), span = (Math.max.apply(0, xs2) - Math.min.apply(0, xs2)) * 1.1;
  function mapOn(i) {
    var r = msvg.getBoundingClientRect(), c = mkeys.sites[i], w = span, h = w * r.height / Math.max(1, r.width);
    if (r.width < r.height) { h = span * 1.2; w = h * r.width / r.height; }
    msvg.setAttribute('viewBox', (c[0] - w * .5).toFixed(1) + ' ' + (c[1] - h * .4).toFixed(1) + ' ' + w.toFixed(1) + ' ' + h.toFixed(1));
    msvg.style.setProperty('--u', (w / Math.max(1, r.width)).toFixed(4));
    msites.forEach(function (s, k) { s.classList.toggle('is-on', k === i); s.classList.toggle('is-past', k <= i); });
  }
  function frame() {
    raf = 0;
    var r = track.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
    var q = Math.max(0, (p - .08) / .9), x = Math.min(n - 1, q * (n - 1)), i0 = Math.floor(x), t = x - i0, i1 = Math.min(n - 1, i0 + 1);
    var pos = xs[i0] + (xs[i1] - xs[i0]) * t, cur = Math.min(n - 1, Math.round(x));
    // the camera: the current point of the line held a third of the way across the screen
    var vb = svg.viewBox.baseVal, scale = svg.getBoundingClientRect().height / vb.height;
    var want = (innerWidth * (innerWidth < 760 ? .5 : .36)) / scale + vb.x;
    move.style.setProperty('--sx', (want - pos).toFixed(1) + 'px');
    l1.style.strokeDashoffset = (W - pos).toFixed(1);
    km.innerHTML = Math.round((i0 ? kms[i0] : 0) + ((i1 ? kms[i1] : 0) - (i0 ? kms[i0] : 0)) * t) + '<small>km</small>';
    head.style.opacity = p < .06 ? 1 : Math.max(0, 1 - (p - .06) / .05);
    if (cur !== at) {
      at = cur;
      sts.forEach(function (s, k) { s.classList.toggle('is-on', k === cur); s.classList.toggle('is-past', k <= cur); });
      cards.forEach(function (c, k) { c.classList.toggle('is-on', k === cur && p > .06); });
      bgs.forEach(function (b, k) { b.classList.toggle('is-on', k === cur); });
      var isMap = bgs[cur] && bgs[cur].classList.contains('is-map');
      mapbg.classList.toggle('is-on', !!isMap);
      if (isMap) mapOn(cur);
    }
    if (bgs[cur]) bgs[cur].style.setProperty('--t', t.toFixed(3));
    cards.forEach(function (c, k) { if (k === cur) c.classList.toggle('is-on', p > .06); });
  }
  addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(frame); }, { passive: true });
  addEventListener('resize', frame); frame();
})();"""
    return body, css, js


BANNER = ('<div class="v4s-banner">Sample, not live: the Kenya page with the route as %s. '
          '<a href="map-a.html">A flight down the Rift</a> &middot; <a href="map-c.html">C zoom from orbit</a> &middot; '
          '<a href="../destinations/kenya.html#route">today\'s</a></div>')
BANNER_CSS = (".v4s-banner{position:relative;z-index:5;background:#ff7517;color:#141519;font-weight:600;text-align:center;padding:.5rem 1rem;font-size:.85rem;}"
              ".v4s-banner a{color:#141519;text-decoration:underline;}")


def build(key, fn, label):
    src = open(SRC, encoding="utf-8").read()
    ss, head, (i, j) = sites(src)
    body, css, js = fn(ss, head)
    src = src[:i] + body + src[j:]
    src = re.sub(r"<title>(.*?)</title>", lambda m: "<title>%s (sample: route %s)</title>" % (m.group(1), label), src, 1, flags=re.S)
    src = src.replace("</head>", "<style>%s%s</style>\n</head>" % (BANNER_CSS, css), 1)
    src = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + BANNER % label, src, 1)
    src = src.replace("</body>", "<script>%s</script>\n</body>" % js, 1)
    out = os.path.join(V4, "samples", "map-%s.html" % key)
    open(out, "w", encoding="utf-8").write(src)
    print("v4 map options: samples/map-%s.html (%d sites, %d kB)" % (key, len(ss), len(body) // 1024))


def main():
    build("a", proto_a, "A, a flight down the Rift")
    build("c", proto_c, "C, a zoom from orbit")


if __name__ == "__main__":
    main()
