#!/usr/bin/env python3
"""
The trip pages' route section: a zoom from orbit with the route as a line
diagram over it (owner, 1 Oct 2026: "C with A route overlay", after the two
prototypes in samples/map-a.html and map-c.html).

The section holds still while the camera falls from the continent to the
country to the flying region; then the route takes over: each site's card
comes up, the line diagram along the foot (stations spaced by the page's own
leg distances) slides to it and fills in orange, the map follows the site,
and a counter gives the km along the route. "Skip the map" jumps past it.

Everything shown is on the page already (site names, coordinates, lines,
legs, photographs, the Kenya chart's relief). Outlines: Natural Earth (public
domain), tools/data/natural-earth-trips.json. The look is v2.css (THE TRIP
MAP), the behaviour v2-immersive.js part 15. Reduced motion or no script: the
region still, with the line diagram and every card listed under it.

    python3 tools/v4_tripmap.py     # rewrites #route on the Kenya page (idempotent)
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_map_options as MO  # noqa: E402

ROOT = MO.ROOT
V4 = MO.V4
GEO = MO.GEO
X, Y, f, esc, ring_path, K = MO.X, MO.Y, MO.f, MO.esc, MO.ring_path, MO.K


def bbox(rings):
    pts = [p for r in rings for p in r]
    return min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)


def map_svg(cfg, pts, names):
    land = "".join('<path d="%s"/>' % ring_path(r) for r in GEO["land"])
    ctry = ""
    for name, rings in GEO[cfg["geo"]].items():
        ctry += '<path class="%s" d="%s"/>' % ("tm-hl" if name == cfg["country"] else "tm-nb", "".join(ring_path(r) for r in rings))
    lo0, la0, lo1, la1 = cfg["world"]
    grat = ""
    for lon in range(int(lo0), int(lo1) + 1, 10):
        grat += '<path class="tm-g1" d="M%s,%s V%s"/>' % (f(X(lon)), f(Y(la1)), f(Y(la0)))
    for lat in range(int(la0), int(la1) + 1, 10):
        grat += '<path class="tm-g1%s" d="M%s,%s H%s"/>' % (" tm-eq" if lat == 0 else "", f(X(lo0)), f(Y(lat)), f(X(lo1)))
    a0, b0, a1, b1 = cfg["fine"]
    for lon in range(a0, a1 + 1):
        grat += '<path class="tm-g2" d="M%s,%s V%s"/>' % (f(X(lon)), f(Y(b1)), f(Y(b0)))
    for lat in range(b0, b1 + 1):
        grat += '<path class="tm-g2" d="M%s,%s H%s"/>' % (f(X(a0)), f(Y(lat)), f(X(a1)))
    terrain = ""
    if cfg.get("terrain"):
        S = MO.SHEET
        terrain = '<image class="tm-terrain" href="%s" x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none"/>' % (
            MO.TERRAIN, f(X(S["lon0"])), f(Y(S["lat0"])), f(S["w"] * K), f(S["h"] * K))
    route = "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts) if len(pts) > 1 else ""
    marks = ""
    for k, ((x, y), nm) in enumerate(zip(pts, names)):
        end = " is-end" if k in (0, len(pts) - 1) else ""
        marks += ('<g class="tm-site%s" data-i="%d"><circle class="tm-ring" cx="%s" cy="%s" r="9"/><circle class="tm-dot" cx="%s" cy="%s" r="3"/>'
                  '<text class="is-r" x="%s" y="%s">%s</text></g>' % (end, k, f(x), f(y), f(x), f(y), f(x), f(y), esc(nm.upper())))
    hb = bbox(GEO[cfg["geo"]][cfg["country"]])
    label = '<text class="tm-cn" x="%s" y="%s" text-anchor="middle">%s</text>' % (
        f(X((hb[0] + hb[2]) / 2 + cfg.get("label_dx", 0))), f(Y((hb[1] + hb[3]) / 2 + cfg.get("label_dy", 0))), esc(cfg["country"].upper()))
    eq = '<text class="tm-eqt" x="%s" y="%s">EQUATOR</text>' % (f(X(a1 + .2)), f(Y(0) - 6)) if b0 <= 0 <= b1 else ""
    lines = ('<path class="tm-route0" d="%s"/><path class="tm-route" d="%s"/>' % (route, route)) if route else ""
    return ('<svg class="tm-map" viewBox="0 0 10 10" preserveAspectRatio="xMidYMid slice" role="img" aria-label="%s">'
            '<rect x="-8000" y="-8000" width="24000" height="24000" fill="#0d0e11"/>'
            '<g class="tm-land">%s</g>%s<g class="tm-grat">%s</g><g class="tm-ctry">%s</g>%s%s%s%s</svg>'
            % (esc(cfg["aria"]), land, terrain, grat, ctry, label, eq, lines, marks))


def strip(stations, legs):
    """The line diagram: stations spaced by the legs (short ones held to a readable minimum)."""
    xs = [0.0]
    for km in legs:
        xs.append(xs[-1] + max(60.0, km) * 2.2)
    W = xs[-1]
    st = ""
    for k, (s, x) in enumerate(zip(stations, xs)):
        up = k % 2 == 0
        st += ('<g class="tm-st" data-i="%d" transform="translate(%s,0)"><path class="tm-tick" d="M0,%s V%s"/><circle class="tm-sring" r="11"/>'
               '<circle class="tm-sdot" r="4.5"/><text class="tm-sname" y="%s" text-anchor="middle">%s</text>%s</g>'
               % (k, f(x), -8 if up else 8, -26 if up else 26, -44 if up else 50, esc(s["name"].upper()),
                  '<text class="tm-sco" y="%s" text-anchor="middle">%s</text>' % (-32 if up else 64, esc(s["co"])) if s.get("co") else ""))
    lt = "".join('<text class="tm-legt" x="%s" y="22" text-anchor="middle">%s</text>' % (f((a + b) / 2), esc(lbl))
                 for (a, b), lbl in zip(zip(xs, xs[1:]), [s.get("leglabel", "%d KM" % s["km"]) for s in stations[1:]]))
    return xs, W, ('<div class="tm-line" aria-hidden="true"><svg viewBox="-200 -80 %s 170" preserveAspectRatio="xMinYMid slice"><g class="tm-move">'
                   '<path class="tm-l0" d="M0,0 H%s"/><path class="tm-l1" d="M0,0 H%s"/>%s%s</g></svg></div>' % (f(W + 400), f(W), f(W), lt, st))


def card(s, k, n):
    pic = ""
    if s.get("photo"):
        pic = '<picture><source srcset="%s" type="image/webp"><img src="%s" alt="%s" loading="lazy" decoding="async"></picture>' % (
            s["photo"]["webp"], s["photo"]["jpg"], esc(s["photo"]["alt"]))
    link = ' <a href="%s">%s</a>.' % (esc(s["link"][0]), esc(s["link"][1])) if s.get("link") else ""
    return ('<article class="tm-card" data-i="%d">%s<div class="tm-card-t"><span class="tm-n">%02d / %02d</span><h3>%s</h3>%s<p>%s%s</p>%s</div></article>'
            % (k, pic, k + 1, n, esc(s["name"]), '<p class="tm-co">%s</p>' % esc(s["co"]) if s.get("co") else "", esc(s["text"]), link,
               '<p class="tm-leg">%s</p>' % esc(s["leg"]) if s.get("leg") else ""))


def section(cfg, stations, legs, head, skip_to, pts, focus, overlay=None, hl=None):
    n = len(stations)
    xs, W, line = strip(stations, legs) if overlay is None else ([0.0] * n, 1, overlay)
    hb = bbox(GEO[cfg["geo"]][cfg["country"]])
    keys = {"world": [X(cfg["world_c"][0]), Y(cfg["world_c"][1]), cfg["world_w"] * K],
            "country": [X((hb[0] + hb[2]) / 2), Y((hb[1] + hb[3]) / 2), (hb[2] - hb[0]) * 1.25 * K],
            "region": [X(cfg["region"][0]), Y(cfg["region"][1]), cfg["region"][2] * K],
            "focus": [[round(x, 1), round(y, 1)] for x, y in focus], "zoom": cfg.get("zoom", .62)}
    kms = [sum(legs[:k]) for k in range(n)] if cfg.get("km") else []
    names = [s["name"] for s in stations] if cfg.get("map_names") is None else cfg["map_names"]
    svg = map_svg(cfg, pts, names)
    # without script the map is still framed on the flying region
    rc = keys["region"]
    ys = [y for _, y in pts]
    hh = max((max(ys) - min(ys)) * 1.35, rc[2] * .5)
    ww = max(rc[2], hh * 2.03)                       # the still map is about 1280 x 630
    cy = (max(ys) + min(ys)) / 2
    svg = svg.replace('viewBox="0 0 10 10"', 'viewBox="%s %s %s %s" style="--u:%.4f;--fine:1;--ter:.85"' % (
        f(rc[0] - ww / 2), f(cy - hh / 2), f(ww), f(hh), ww / 1280.0), 1)
    cards = "".join(card(s, k, n) for k, s in enumerate(stations))
    km = '<div class="tm-km" aria-hidden="true">along the route<b>0<small>km</small></b></div>' if kms else ""
    hla = ' data-hl="%s"' % esc(json.dumps(hl)) if hl else ""
    return ('<section class="dst-sec tm" id="route" aria-labelledby="route-h" style="--n:%d" data-keys="%s" data-km="%s" data-x="%s" data-w="%s"%s>\n'
            '  <div class="tm-track"><div class="tm-pin">%s'
            '<div class="tm-head"><span class="kicker">%s</span><h2 id="route-h">%s</h2>%s</div>%s%s'
            '<div class="tm-cards">%s</div>'
            '<a class="tm-skip" href="#%s">Skip the map <i aria-hidden="true">&darr;</i></a>'
            '</div></div>\n</section>'
            % (n, esc(json.dumps(keys)), esc(json.dumps(kms)), esc(json.dumps([round(x, 1) for x in xs])), f(W), hla,
               svg, esc(head[0]), esc(head[1]), "<p>%s</p>" % esc(head[2]) if head[2] else "", km, line, cards, skip_to))


KENYA = dict(page="destinations/kenya.html", geo="countries", country="Kenya", world=(-20, -40, 60, 40), world_c=(18, 2), world_w=95,
             fine=(33, -5, 41, 4), terrain=True, region=None, km=True, label_dx=1.6, label_dy=1.4,
             aria="Map of Africa narrowing to Kenya and the six sites of the route")


def kenya():
    p = os.path.join(V4, KENYA["page"])
    src = open(p, encoding="utf-8").read()
    i = src.rindex("<section", 0, src.index('id="route"'))
    j = src.index("</section>", i) + len("</section>")
    old = src[i:j]
    if 'class="dst-sec tm"' in old:
        ss = json.loads(html.unescape(re.search(r'data-v4-sites="([^"]*)"', src).group(1)))
        head = json.loads(html.unescape(re.search(r'data-v4-head="([^"]*)"', src).group(1)))
    else:
        ss, head, _ = MO.sites(src)
    legs = [s["km"] for s in ss[1:]]
    pts = [(X(s["lon"]), Y(s["lat"])) for s in ss]
    xs = [s["lon"] for s in ss]
    ys = [s["lat"] for s in ss]
    cfg = dict(KENYA, region=((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (max(xs) - min(xs)) * 2.1))
    nxt = re.search(r'<section[^>]*\sid="([^"]+)"', src[j:]).group(1)
    sec = section(cfg, ss, legs, head, nxt, pts, pts)
    # the source facts ride along on the section, so the tool can rebuild from its own output
    sec = sec.replace('<section class="dst-sec tm" id="route"',
                      '<section class="dst-sec tm" id="route" data-v4-sites="%s" data-v4-head="%s"' % (esc(json.dumps(ss)), esc(json.dumps(list(head)))), 1)
    src = src[:i] + sec + src[j:]
    src = re.sub(r'<script defer src="\.\./\.\./\.\./kenya-map\.js[^"]*"></script>\s*', "", src)
    open(p, "w", encoding="utf-8").write(src)
    print("v4 trip map: %s, %d sites, %d legs, %d kB, skips to #%s" % (KENYA["page"], len(ss), len(legs), len(sec) // 1024, nxt))


INDIA = dict(page="destinations/india.html", geo="asia", country="India", world=(40, 0, 110, 50), world_c=(76, 24), world_w=96,
             fine=(74, 30, 80, 34), terrain=False, region=None, km=False, label_dx=-1.5, label_dy=2,
             aria="Map of South Asia narrowing to India and Bir Billing in Himachal Pradesh")


def india():
    p = os.path.join(V4, INDIA["page"])
    src = open(p, encoding="utf-8").read()
    i = src.rindex("<section", 0, src.index('id="route"'))
    j = src.index("</section>", i) + len("</section>")
    old = src[i:j]
    # the route section as the page had it before this tool, kept in tools/data (the source of the cards and the schematic)
    srcf = os.path.join(ROOT, "tools", "data", "india-route-section.txt")
    if 'class="dst-sec tm"' in old:
        old = open(srcf, encoding="utf-8").read()
    else:
        open(srcf, "w", encoding="utf-8").write(old)
    head = (html.unescape(re.search(r'<span class="kicker">([^<]*)</span>', old).group(1)),
            html.unescape(re.search(r'<h2 id="route-h">([^<]*)</h2>', old).group(1)), "")
    schem = re.search(r'<svg class="iroute-svg".*?</svg>', old, re.S).group(0)
    cap = re.sub(r'<span class="iroute-hint">.*?</span>', "", re.search(r"<figcaption>(.*?)</figcaption>", old, re.S).group(1)).strip()
    intro = html.unescape(re.sub(r"<[^>]+>", "", re.search(r'<details class="v4-fold v4t-rintro">.*?<p>(.*?)</p>', old, re.S).group(1)))
    cards = [dict(name="Billing launch", leg="about 2,400m", text=intro)]
    for li in re.findall(r'<li class="iroute-item[^"]*">(.*?)</li>', old, re.S):
        h3 = html.unescape(re.search(r"<h3>(.*?)</h3>", li).group(1))
        km = html.unescape(re.search(r'<span class="iroute-km">(.*?)</span>', li).group(1))
        para = re.search(r"<p>(.*?)</p>", li, re.S).group(1)
        a = re.search(r'\s*<a href="([^"]+)">([^<]+)</a>\.?', para)
        text = html.unescape(re.sub(r"<[^>]+>", "", para[:a.start()] if a else para)).strip()
        cards.append(dict(name=h3, leg=km, text=text, link=(a.group(1), html.unescape(a.group(2))) if a else None))
    hl = ["ir-home", "ir-west", "ir-east", "ir-over"][:len(cards)]
    co = re.search(r"([\d.]+)°N · ([\d.]+)°E", src)
    lat, lon = float(co.group(1)), float(co.group(2))
    pt = (X(lon), Y(lat))
    # Bir framed to the left of the schematic panel (which sits on the right of the screen)
    # the region frame wide enough to show the ranges around Bir, not one flat field (visual review, 5 Oct: 3.4 to 10)
    # the offset grows with the frame, so Bir stays left of the schematic panel (1.0 * 10 / 3.4)
    cfg = dict(INDIA, region=(lon + 2.9, lat - .25, 10), zoom=1, map_names=["Bir Billing"])
    overlay = ('<div class="tm-line tm-schem" data-on="">%s<p class="tm-schem-cap">%s</p></div>' % (schem, cap))
    nxt = re.search(r'<section[^>]*\sid="([^"]+)"', src[j:]).group(1)
    fp = (X(lon + 2.9), Y(lat - .25))
    sec = section(cfg, cards, [], head, nxt, [pt], [fp] * len(cards), overlay=overlay, hl=hl)
    src = src[:i] + sec + src[j:]
    open(p, "w", encoding="utf-8").write(src)
    print("v4 trip map: %s, %d cards, the schematic as the route, %.4f N %.4f E, skips to #%s" % (INDIA["page"], len(cards), lat, lon, nxt))


def main():
    kenya()
    india()


if __name__ == "__main__":
    main()
