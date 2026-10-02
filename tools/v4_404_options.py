#!/usr/bin/env python3
"""
Three 404 pages for v4, as samples on a copy of the current one (owner,
2 Oct 2026: "I'd like to make an interesting 404 page, give me a few examples
in protos"). Same words and the same four doors as today's 404; only the
moment changes.

  A  lost the lift   a vario in the Gold line: the needle swings down into
                     sink and holds at -4.04, the barogram climbs, then falls
                     to the ground
  B  off the map     a contour sheet; the flight track wanders off the edge of
                     the map, and the four doors are turnpoints on it
  C  outland it      a small game: the wing drifts down, steer it (pointer,
                     touch or arrow keys) onto one of four landing fields, each
                     a door; the doors are links underneath as well

Reduced motion: A and B still, C a still picture with the fields as links.

    python3 tools/v4_404_options.py   # writes prototypes/v4/samples/404-a.html, -b, -c
"""
import math
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_samples as SM  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "404.html")


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def P(pts, close=False):
    return "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts) + (" Z" if close else "")


def doors(src):
    """The current 404's four doors: (title, line, href)."""
    out = re.findall(r'<a class="kit-panel v2-door" href="([^"]+)"><h2>([^<]+)</h2><p>([^<]+)</p>', src)
    return [(t, l, h) for h, t, l in out]


def copy(src):
    m = re.search(r'<main class="kit-hero[^"]*v2-nf">(.*?)</main>', src, re.S).group(1)
    kicker = re.search(r'<span class="kit-kicker">([^<]*)</span>', m).group(1)
    h1 = re.search(r"<h1>([^<]*)</h1>", m).group(1)
    intro = re.search(r'<p class="kit-intro">([^<]*)</p>', m).group(1)
    find = re.search(r'<p class="v4-404-find">.*?</p>', m, re.S).group(0)
    return kicker, h1, intro, find


# ---------------------------------------------------------------- A: lost the lift
def opt_a(src):
    kicker, h1, intro, find = copy(src)
    c, R = (300, 300), 230
    ticks = ""
    for k in range(41):
        a = math.radians(-225 + 270 * k / 40)
        l = 22 if k % 5 == 0 else 11
        ticks += '<path d="%s" class="na-t%s"/>' % (P([(c[0] + R * math.cos(a), c[1] + R * math.sin(a)), (c[0] + (R - l) * math.cos(a), c[1] + (R - l) * math.sin(a))]),
                                                  " is-maj" if k % 5 == 0 else "")
    labels = ""
    for k, v in enumerate(range(-5, 6, 1)):
        a = math.radians(-225 + 270 * k / 10)
        labels += '<text x="%s" y="%s" text-anchor="middle">%s</text>' % (f(c[0] + (R - 48) * math.cos(a)), f(c[1] + (R - 48) * math.sin(a) + 6), ("+%d" % v) if v > 0 else str(v))
    sink = ""
    a0, a1 = math.radians(-225), math.radians(-225 + 270 * 0.5)
    sink_arc = [(c[0] + (R + 12) * math.cos(a0 + (a1 - a0) * i / 40), c[1] + (R + 12) * math.sin(a0 + (a1 - a0) * i / 40)) for i in range(41)]
    sink = '<path class="na-sink" d="%s"/>' % P(sink_arc)
    # the barogram: a climb in steps, then the long fall to the ground
    rnd = random.Random(4)
    pts, y = [], 250.0
    for i in range(0, 260, 4):
        y -= (1.6 + rnd.uniform(-1.2, 1.4)) if i < 150 else -(2.4 + rnd.uniform(-.6, .8))
        pts.append((i, max(20, min(258, y))))
    baro = P(pts)
    svg = ('<svg class="na-svg" viewBox="0 0 600 600" aria-hidden="true">'
           '<defs><linearGradient id="naG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6f4f4"/><stop offset="1" stop-color="#ffcf94"/></linearGradient></defs>'
           '<circle cx="300" cy="300" r="268" class="na-bezel"/><circle cx="300" cy="300" r="%d" class="na-face"/>%s%s'
           '<g class="na-labels">%s</g>'
           '<g class="na-needle"><path d="M300,300 L300,98" class="na-nd"/><circle cx="300" cy="300" r="14" class="na-hub"/></g>'
           '<text x="300" y="398" text-anchor="middle" class="na-read">-4.04</text><text x="300" y="428" text-anchor="middle" class="na-unit">M/S &middot; SINK</text>'
           '<text x="300" y="214" text-anchor="middle" class="na-unit">VARIO</text></svg>' % (R, ticks, sink, labels))
    barog = ('<svg class="na-baro" viewBox="0 -10 260 280" preserveAspectRatio="none" aria-hidden="true">'
             '<path class="na-grd" d="M0,262 H260"/><path class="na-b" d="%s"/></svg>' % baro)
    body = ('<main class="nf nf-a"><div class="nf-copy"><span class="kit-kicker">%s &middot; sink</span><h1>%s</h1><p class="kit-intro">%s</p>%s</div>'
            '<div class="nf-art">%s<div class="na-trace">%s<span class="na-tl">ALT, the last ten minutes</span></div></div></main>' % (kicker, h1, intro, find, svg, barog))
    css = """
.nf{position:relative;min-height:clamp(620px,100svh,980px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:center;gap:var(--sp-5);
  padding:7rem var(--gutter) var(--sp-5);max-width:1400px;margin:0 auto;}
@media (max-width:900px){ .nf{grid-template-columns:1fr;padding-top:6rem;} }
.nf-copy h1{font-family:var(--font-display);font-size:var(--fs-display);line-height:1.02;margin:.6rem 0 1rem;color:#fff;}
.nf-a .nf-art{position:relative;}
.na-svg{width:min(100%,560px);display:block;margin:0 auto;}
.na-bezel{fill:#121318;stroke:rgba(255,207,148,.25);stroke-width:1.5;}
.na-face{fill:none;stroke:url(#naG);stroke-width:1.2;}
.na-t{stroke:rgba(246,244,244,.45);stroke-width:1.2;} .na-t.is-maj{stroke:#f6f4f4;stroke-width:2;}
.na-labels text{font:600 18px var(--font-body);fill:rgba(246,244,244,.65);}
.na-sink{fill:none;stroke:#ff7517;stroke-width:6;stroke-linecap:round;opacity:.85;}
.na-needle{transform-origin:300px 300px;transform:rotate(-55deg);animation:na-sink 2.6s cubic-bezier(.2,.8,.2,1) .3s forwards, na-wob 3.2s ease-in-out 3s infinite;}
@keyframes na-sink{from{transform:rotate(30deg);}to{transform:rotate(-116deg);}}
@keyframes na-wob{0%,100%{transform:rotate(-116deg);}50%{transform:rotate(-112deg);}}
.na-nd{stroke:#ff7517;stroke-width:5;stroke-linecap:round;} .na-hub{fill:#141519;stroke:#ffcf94;stroke-width:2;}
.na-read{font:700 64px var(--font-display);fill:#fff;letter-spacing:-.02em;} .na-unit{font:600 13px var(--font-body);letter-spacing:.3em;fill:rgba(246,244,244,.55);}
.na-trace{position:absolute;right:0;bottom:-1rem;width:42%;height:120px;}
.na-baro{width:100%;height:100%;overflow:visible;}
.na-b{fill:none;stroke:#ffcf94;stroke-width:2;vector-effect:non-scaling-stroke;stroke-dasharray:1200;stroke-dashoffset:1200;animation:na-draw 3s ease 1s forwards;}
.na-grd{stroke:rgba(246,244,244,.3);stroke-width:1;vector-effect:non-scaling-stroke;stroke-dasharray:3 4;}
@keyframes na-draw{to{stroke-dashoffset:0;}}
.na-tl{display:block;font-size:var(--fs-micro);letter-spacing:.18em;text-transform:uppercase;color:var(--gray);margin-top:.4rem;}
@media (prefers-reduced-motion:reduce){ .na-needle{animation:none;transform:rotate(-116deg);} .na-b{animation:none;stroke-dashoffset:0;} }
"""
    return body, css, ""


# ---------------------------------------------------------------- B: off the map
def opt_b(src, ds):
    kicker, h1, intro, find = copy(src)
    W, H = 1400, 800
    rnd = random.Random(7)
    con = ""
    for (cx, cy, R, ph) in ((380, 420, 300, .4), (1040, 300, 240, 1.7), (900, 640, 170, 2.9)):
        for k in range(9):
            r = R * (1 - k * .1)
            pts = [(cx + r * (1 + .13 * math.sin(3 * t + ph + k * .3) + .07 * math.sin(5 * t + 2 * ph)) * math.cos(t),
                    cy + r * .66 * (1 + .13 * math.sin(3 * t + ph + k * .3) + .07 * math.sin(5 * t + 2 * ph)) * math.sin(t))
                   for t in [2 * math.pi * i / 90 for i in range(90)]]
            con += '<path class="nb-c%s" d="%s"/>' % (" is-idx" if k % 4 == 0 else "", P(pts, True))
    grid = "".join('<path class="nb-g" d="M%d,60 V%d"/>' % (x, H - 60) for x in range(160, W - 60, 200))
    grid += "".join('<path class="nb-g" d="M60,%d H%d"/>' % (y, W - 60) for y in range(160, H - 60, 160))
    # the track: in from the south west, wandering, then off the sheet at the north east
    # glides between thermals, a few turns in each, and finally off the top of the sheet
    tr, x, y, hd = [], 90.0, 730.0, -0.45
    climbs = {14: 4, 30: 3, 47: 3, 60: 2}
    step = 0
    while x < W + 160 and y > -160:
        tr.append((x, y))
        if step in climbs:
            cx, cy, r = x, y - 26, 26
            for i in range(1, climbs[step] * 24 + 1):
                a = math.pi / 2 + 2 * math.pi * i / 24
                tr.append((cx + r * math.cos(a) * (1 + .002 * i), cy + r * math.sin(a) - i * 1.1))
            x, y = tr[-1]
        hd += rnd.uniform(-.28, .28)
        hd = max(-1.1, min(.15, hd))
        x += 24 * math.cos(hd) + 4
        y += 24 * math.sin(hd)
        step += 1
    track = P(tr)
    tps = [(960, 230), (1200, 330), (1000, 500), (1240, 640)]   # the right half, clear of the words
    tp = ""
    for (t, l, h), (px, py) in zip(ds, tps):
        tp += ('<a class="nb-tp" href="%s"><circle cx="%d" cy="%d" r="58" class="nb-cyl"/><circle cx="%d" cy="%d" r="5" class="nb-tpd"/>'
               '<text x="%d" y="%d" text-anchor="middle" class="nb-tpt">%s</text><text x="%d" y="%d" text-anchor="middle" class="nb-tpl">TURNPOINT</text></a>'
               % (h, px, py, px, py, px, py + 82, t.upper(), px, py + 100))
    svg = ('<svg class="nb-svg" viewBox="0 0 %d %d" preserveAspectRatio="xMaxYMid slice" role="group" aria-label="A contour map with four turnpoints, each a way back into the site">'
           '<rect x="60" y="60" width="%d" height="%d" class="nb-neat"/><g class="nb-par">%s%s</g>'
           '<path class="nb-trk0" d="%s"/><path class="nb-trk" d="%s"/>%s'
           '<g class="nb-you" transform="translate(%d,40)"><circle r="8" class="nb-ydot"/><text x="16" y="5" class="nb-yt">YOU ARE HERE, OFF THE SHEET</text></g>'
           '<text x="76" y="%d" class="nb-sheet">SHEET 404 &middot; NOT ON THIS MAP</text></svg>'
           % (W, H, W - 120, H - 120, grid, con, track, track, tp, W - 420, H - 74))
    body = ('<main class="nf nf-b"><div class="nb-map">%s</div><div class="nf-copy nb-copy"><span class="kit-kicker">%s</span><h1>%s</h1><p class="kit-intro">%s</p>%s'
            '<p class="nb-hint">Pick a turnpoint to fly back in.</p></div></main>' % (svg, kicker, h1, intro, find))
    css = """
.nf-b{position:relative;min-height:clamp(640px,100svh,1000px);overflow:hidden;display:flex;flex-direction:row;align-items:flex-end;justify-content:flex-start;padding:7rem var(--gutter) var(--sp-5);}
.nb-map{position:absolute;inset:0;}
.nb-svg{width:100%;height:100%;display:block;}
.nb-svg path,.nb-svg circle,.nb-svg rect{vector-effect:non-scaling-stroke;}
.nb-neat{fill:none;stroke:rgba(255,207,148,.35);stroke-width:1.2;}
.nb-g{stroke:rgba(246,244,244,.06);stroke-width:1;}
.nb-c{fill:none;stroke:rgba(246,244,244,.16);stroke-width:.8;} .nb-c.is-idx{stroke:rgba(255,207,148,.32);stroke-width:1.1;}
.nb-par{transform:translate(var(--mx,0px),var(--my,0px));transition:transform .8s cubic-bezier(.2,.8,.2,1);}
.nb-trk0{fill:none;stroke:rgba(246,244,244,.25);stroke-width:1;stroke-dasharray:3 6;}
.nb-trk{fill:none;stroke:#ff7517;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:6000;stroke-dashoffset:6000;animation:nb-draw 4.5s cubic-bezier(.4,0,.2,1) .4s forwards;}
@keyframes nb-draw{to{stroke-dashoffset:0;}}
.nb-cyl{fill:rgba(255,117,23,.04);stroke:#ffcf94;stroke-width:1.2;stroke-dasharray:4 4;transition:fill .3s ease,stroke .3s ease;}
.nb-tpd{fill:#ff7517;} .nb-tpt{font:600 15px var(--font-body);letter-spacing:.16em;fill:#fff;} .nb-tpl{font:600 10px var(--font-body);letter-spacing:.3em;fill:rgba(246,244,244,.45);}
.nb-tp:hover .nb-cyl,.nb-tp:focus-visible .nb-cyl{fill:rgba(255,117,23,.18);stroke:#ff7517;}
.nb-tp:focus-visible{outline:none;} .nb-tp:focus-visible .nb-tpt{fill:#ff7517;}
.nb-ydot{fill:none;stroke:#ff7517;stroke-width:2;animation:nb-pulse 1.6s ease-in-out infinite;} @keyframes nb-pulse{50%{r:14;opacity:.4;}}
.nb-yt{font:600 12px var(--font-body);letter-spacing:.22em;fill:#ff7517;}
.nb-sheet{font:600 12px var(--font-body);letter-spacing:.3em;fill:rgba(246,244,244,.45);}
.nb-copy{position:relative;z-index:2;max-width:34rem;background:rgba(13,14,17,.72);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);padding:var(--sp-4);border-top:2px solid var(--orange);}
.nb-copy h1{font-size:var(--fs-h1);}
.nb-hint{margin:.8rem 0 0;color:var(--gray);font-size:var(--fs-small);}
@media (max-width:760px){
  .nf-b{display:block;padding:0 0 var(--sp-5);min-height:0;}
  .nb-map{position:relative;height:72vh;margin-top:4.5rem;}
  .nb-svg{height:100%;}
  .nb-copy{margin:-3rem var(--gutter) 0;}
}
@media (prefers-reduced-motion:reduce){ .nb-trk{animation:none;stroke-dashoffset:0;} .nb-ydot{animation:none;} .nb-par{transition:none;} }
"""
    js = """
(function () {
  var m = document.querySelector('.nb-par'); if (!m || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  addEventListener('pointermove', function (e) { m.style.setProperty('--mx', ((e.clientX / innerWidth - .5) * -18).toFixed(1) + 'px'); m.style.setProperty('--my', ((e.clientY / innerHeight - .5) * -12).toFixed(1) + 'px'); }, { passive: true });
})();"""
    return body, css, js


# ---------------------------------------------------------------- C: outland it
def opt_c(src, ds):
    kicker, h1, intro, find = copy(src)
    W, H = 1200, 700
    fields = ""
    xs = [150, 450, 750, 1050]
    for (t, l, h), x in zip(ds, xs):
        fields += ('<g class="nc-field" data-href="%s" data-x="%d"><rect x="%d" y="610" width="200" height="40" class="nc-fr"/>'
                   '<text x="%d" y="676" text-anchor="middle" class="nc-ft">%s</text></g>' % (h, x, x - 100, x, t.upper()))
    hills = "M0,610 C120,560 200,600 300,606 C380,612 420,560 520,600 C600,630 680,560 780,596 C860,622 940,560 1040,598 C1110,624 1160,590 1200,600 L1200,700 L0,700 Z"
    svg = ('<svg class="nc-svg" viewBox="0 0 %d %d" role="img" aria-label="A paraglider drifting down towards four landing fields">'
           '<path class="nc-hills" d="%s"/><g class="nc-fields">%s</g>'
           '<g class="nc-wing"><path class="nc-canopy" d="M-34,0 C-24,-16 24,-16 34,0 C22,-6 -22,-6 -34,0 Z"/>'
           '<path class="nc-lines" d="M-32,0 L0,34 M-12,-6 L0,34 M12,-6 L0,34 M32,0 L0,34"/><circle cx="0" cy="38" r="5" class="nc-pilot"/></g>'
           '<g class="nc-wind"></g></svg>' % (W, H, hills, fields))
    links = "".join('<li><a href="%s">%s</a> <span>%s</span></li>' % (h, t, l) for t, l, h in ds)
    body = ('<main class="nf nf-c"><div class="nf-copy nc-copy"><span class="kit-kicker">%s</span><h1>%s</h1><p class="kit-intro">%s</p>'
            '<p class="nc-how">Bring it in to land: steer with the pointer, a finger, or the arrow keys. Each field is a way back in.</p>%s'
            '<p class="nc-msg" aria-live="polite"></p></div>'
            '<div class="nc-stage">%s</div><ul class="nc-list">%s</ul></main>' % (kicker, h1, intro, find, svg, links))
    css = """
.nf-c{position:relative;padding:7rem var(--gutter) var(--sp-5);max-width:1400px;margin:0 auto;}
.nc-copy{max-width:44rem;} .nc-copy h1{font-size:var(--fs-h1);}
.nc-how{color:var(--gray-light);font-size:var(--fs-body-s);}
.nc-msg{min-height:1.6em;color:var(--orange);font-weight:600;}
.nc-stage{position:relative;margin-top:var(--sp-3);border:1px solid var(--line);background:radial-gradient(120% 80% at 50% 0%,rgba(255,179,92,.08),transparent 60%),#101115;touch-action:none;}
.nc-svg{display:block;width:100%;height:auto;}
.nc-hills{fill:#16171c;stroke:rgba(255,207,148,.35);stroke-width:1.2;}
.nc-fr{fill:rgba(255,117,23,.06);stroke:#ffcf94;stroke-width:1.2;stroke-dasharray:6 5;transition:fill .3s ease;}
.nc-field.is-near .nc-fr{fill:rgba(255,117,23,.2);stroke:#ff7517;}
.nc-ft{font:600 15px var(--font-body);letter-spacing:.16em;fill:#fff;}
.nc-canopy{fill:rgba(255,179,92,.18);stroke:#ffcf94;stroke-width:1.6;} .nc-lines{stroke:rgba(246,244,244,.6);stroke-width:.8;fill:none;} .nc-pilot{fill:#ff7517;}
.nc-wind path{stroke:rgba(246,244,244,.18);stroke-width:1;fill:none;stroke-dasharray:10 14;}
.nc-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,16rem),1fr));gap:1rem;list-style:none;padding:0;margin:var(--sp-3) 0 0;}
.nc-list a{color:#fff;font-weight:600;} .nc-list span{display:block;color:var(--gray);font-size:var(--fs-small);}
@media (prefers-reduced-motion:reduce){ .nc-how{display:none;} }
"""
    js = """
(function () {
  var st = document.querySelector('.nc-stage'); if (!st) return;
  var svg = st.querySelector('svg'), wing = st.querySelector('.nc-wing'), msg = document.querySelector('.nc-msg');
  var fields = [].slice.call(st.querySelectorAll('.nc-field'));
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = 1200, x = 120, y = 60, vx = 0, target = null, keys = 0, done = false, t0 = performance.now();
  wing.setAttribute('transform', 'translate(' + x + ',' + y + ')');
  fields.forEach(function (fd) { fd.style.cursor = 'pointer'; fd.addEventListener('click', function () { location.href = fd.dataset.href; }); });
  if (reduce) { wing.setAttribute('transform', 'translate(600,300)'); return; }
  function toSvg(e) { var r = svg.getBoundingClientRect(); return (e.clientX - r.left) / r.width * W; }
  st.addEventListener('pointermove', function (e) { target = toSvg(e); });
  st.addEventListener('pointerdown', function (e) { target = toSvg(e); });
  addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') keys = -1; else if (e.key === 'ArrowRight') keys = 1; else return; e.preventDefault(); });
  addEventListener('keyup', function (e) { if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') keys = 0; });
  var seen = false; new IntersectionObserver(function (es) { seen = es[0].isIntersecting; }).observe(st);
  function step(now) {
    var dt = Math.min(.05, (now - t0) / 1000); t0 = now;
    if (!done && seen) {
      var gust = Math.sin(now / 900) * 18 + Math.sin(now / 2300) * 26;        /* a little wind, for character */
      var want = target !== null ? Math.max(-120, Math.min(120, (target - x) * 1.2)) : 0;
      vx += ((keys ? keys * 140 : want) + gust - vx) * Math.min(1, dt * 2.2);
      x = Math.max(40, Math.min(W - 40, x + vx * dt)); y += 34 * dt;
      var tilt = Math.max(-18, Math.min(18, vx / 8));
      wing.setAttribute('transform', 'translate(' + x.toFixed(1) + ',' + y.toFixed(1) + ') rotate(' + tilt.toFixed(1) + ')');
      var near = null;
      fields.forEach(function (fd) { var on = Math.abs(+fd.dataset.x - x) < 100; fd.classList.toggle('is-near', on && y > 420); if (on) near = fd; });
      if (y >= 570) {
        done = true;
        if (near) { msg.textContent = 'Landed: ' + near.querySelector('text').textContent.toLowerCase() + '. Taking you there.'; setTimeout(function () { location.href = near.dataset.href; }, 1400); }
        else { msg.textContent = 'Outlanded, between the fields. Tap anywhere to take off again.'; st.addEventListener('pointerdown', again, { once: true }); addEventListener('keydown', again, { once: true }); }
      }
    }
    requestAnimationFrame(step);
  }
  function again() { x = 120; y = 60; vx = 0; done = false; msg.textContent = ''; }
  requestAnimationFrame(step);
})();"""
    return body, css, js


BANNER = ('<div class="v4s-banner">Sample, not live: the 404 page as %s. '
          '<a href="404-a.html">A lost the lift</a> &middot; <a href="404-b.html">B off the map</a> &middot; '
          '<a href="404-c.html">C outland it</a> &middot; <a href="404.html">today\'s</a></div>')
BANNER_CSS = (".v4s-banner{position:relative;z-index:5;background:#ff7517;color:#141519;font-weight:600;text-align:center;padding:.5rem 1rem;font-size:.85rem;}"
              ".v4s-banner a{color:#141519;text-decoration:underline;}")


def build(key, fn, label):
    src = open(SRC, encoding="utf-8").read()
    ds = doors(src)
    body, css, js = fn(src) if fn is opt_a else fn(src, ds)
    i = src.index('<main class="kit-hero')
    j = src.index("</main>", i) + len("</main>")
    out = src[:i] + body + src[j:]
    if fn is not opt_a:
        out = re.sub(r'<section class="kit-band v2-nf-links">.*?</section>\s*', "", out, flags=re.S)   # the doors are in the moment itself
    out = re.sub(r"<title>(.*?)</title>", lambda m: "<title>%s (sample: 404 %s)</title>" % (m.group(1), label), out, 1, flags=re.S)
    out = out.replace("</head>", "<style>%s%s</style>\n</head>" % (BANNER_CSS, css), 1)
    out = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + BANNER % label, out, 1)
    if js:
        out = out.replace("</body>", "<script>%s</script>\n</body>" % js, 1)
    # the page sits one folder deeper than 404.html: its relative links go up one more
    out = SM.deeper(out)
    for k in "abc":
        out = out.replace('href="../404-%s.html"' % k, 'href="404-%s.html"' % k)
    p = os.path.join(V4, "samples", "404-%s.html" % key)
    open(p, "w", encoding="utf-8").write(out)
    print("v4 404 options: samples/404-%s.html" % key)


def main():
    build("a", opt_a, "A, lost the lift")
    build("b", opt_b, "B, off the map")
    build("c", opt_c, "C, outland it")


if __name__ == "__main__":
    main()
