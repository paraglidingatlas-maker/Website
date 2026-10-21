#!/usr/bin/env python3
"""
The Encarta pieces on the encyclopedia's v4 pages (owner, 21 Oct 2026, of the two ways to bring in the
10 Oct "Encarta" build, prototypes/workspace/encyclopedia/: "2 but also do option 1 so we save on pages
to click through"). Used by tools/v4_encyclopedia.py pages; nothing here is a page of its own.

  1. The answer pages keep every word, source and guest card for search, and gain the Encarta build's
     two moving pictures, drawn in the site's colours (read from its tokens) rather than its own:
       - Collapse: the opening's drawing becomes the wing seen from behind, hit by sinking air on one
         side, folding, the pilot leaning away, and reopening. It plays once when it comes into view
         and again on "Replay"; its six captions are written in the page (a list), so they read without
         JavaScript. Every step is the page's own answer (the short answer and "What should you do");
       - Collapse and Stall: the page's drawing of one profile at three angles ("Too low: collapse",
         "Flying", "Too high: stall") becomes the Encarta build's angle-of-attack lab: one profile, a
         slider that tilts it, the air bending round it or breaking away, and the page's own three
         captions lit in turn. No angle is printed: the drawing says it is schematic, not to scale.
         The still drawing stays in the page for anyone without JavaScript.
  2. The A to Z page opens with the Encarta front page's "Explore by subject" (its seven worlds, with
     its own one-line summaries) and its featured article, Collapse. A world filters the A to Z on the
     same page, so there is no page more to click through; each of the A to Z's 30 topics belongs to
     one world (the WORLDS table below).
  3. Every answer page's sources fold into one line (owner, 21 Oct, of the full list and "How this answer
     was made" box: "this whole section of the page can be made discreet and collapsed ... why are we
     wasting space"): "Sources, N cited in the text by number", opened on a click. The list stays in the
     page for search and answer engines; a citation number or the contents' "Sources" opens it on the
     way, and pointing at a number shows its source's title.
Motion: the collapse plays once, then only on Replay; the lab moves only with the slider. With reduced
motion the wing is drawn folded, standing still, and the captions are listed.
"""
import html
import re

E = html.escape

# The Encarta build's seven worlds (CATS: its names and summaries), each with the A to Z topics it holds.
WORLDS = [
    ("wing", "How wings fly", "Lift, glide, speed, aspect ratio",
     ["How a paraglider flies", "Glide ratio", "Speed", "Speed bar", "Aspect ratio", "Wing design and control"]),
    ("safety", "Safety and recovery", "Collapse, stall, active flying",
     ["Collapses", "Stalls and spins", "Active flying", "Accidents and safety culture", "Safety training", "Mid-air collisions"]),
    ("air", "Lift and weather", "Thermals, ridge, forecasts",
     ["Thermals and lift", "Weather and forecasting", "High altitude"]),
    ("gear", "Gear", "Reserves, harnesses, helmets",
     ["Reserve parachutes", "Harnesses", "Helmets and carabiners", "Certification", "Choosing and buying a wing"]),
    ("race", "Competition", "Scoring, tasks, racing",
     ["Competitions", "Competition scoring and tasks", "Competition rules and governance"]),
    ("places", "Places", "Colombia, Bir, Kenya, Australia",
     ["Places to fly", "Adventure and vol-biv", "Flying with a dog"]),
    ("mind", "Pilots and the mind", "Fear, risk, training",
     ["Mind, risk and judgement", "Body and fitness", "Pilots and the industry", "Filming and sponsorship"]),
]

COLLAPSE = "what-happens-if-a-paraglider-collapses.html"
LABS = (COLLAPSE, "what-is-a-stall-on-a-paraglider.html")
# the collapse, in the page's own words (its short answer and "What should you do"), and when each shows
STEPS = [(0.0, "Flying", "the wing pressurised overhead"),
         (1.5, "Sinking air", "hits one side"),
         (2.6, "Collapse", "one side folds"),
         (3.4, "Lean away", "a little brake on the open side"),
         (5.2, "Reopening", "let it come back"),
         (6.6, "Flying again", "")]


def fail(msg):
    raise SystemExit("v4_enc_lab: " + msg)


# ── the answer pages ────────────────────────────────────────────────────────
def hero(body):
    """Collapse's opening drawing becomes the moving wing (the still drawing's place, the same size)."""
    m = re.search(r'<div class="k-hero-media">.*?</div>', body, re.S)
    if not m:
        fail("Collapse has no opening drawing")
    steps = "".join('<li data-t="%s"><b>%s</b>%s</li>' % (t, E(a), (" &middot; " + E(b)) if b else "") for t, a, b in STEPS)
    stage = ('<div class="k-hero-media enc-hero"><canvas aria-hidden="true"></canvas></div>'
             '<div class="enc-hero-cap"><ol class="enc-steps" aria-label="The collapse, step by step">%s</ol>'
             '<button type="button" class="enc-replay" hidden>Replay</button><span class="enc-view">Seen from behind</span></div>'
             % steps)
    return body[:m.start()] + stage + body[m.end():]


def lab(body):
    """The three-angle drawing becomes the angle-of-attack lab; its captions stay and light in turn."""
    m = re.search(r'<figure class="band-draw">(<picture><source srcset="[^"]*kb-enc-aoa\.webp".*?</picture>)(<figcaption class="bd-caps c3">.*?</figcaption>)</figure>',
                  body, re.S)
    if not m:
        fail("no three-angle drawing to turn into the lab")
    pic, caps = m.group(1), m.group(2)
    tool = ('<div class="enc-lab" hidden><svg class="enc-foil" viewBox="0 0 520 300" role="img" '
            'aria-label="One profile at the angle chosen with the slider, the air bending round it"></svg>'
            '<label class="enc-range"><span>Tilt the wing</span><input type="range" min="-10" max="26" value="6" step="0.5" '
            'aria-label="Angle of attack, from too low to too high"><span class="enc-ends"><i>lower</i><i>higher</i></span></label></div>')
    new = '<figure class="band-draw enc-lab-fig"><div class="enc-still">%s</div>%s%s</figure>' % (pic, tool, caps)
    return body[:m.start()] + new + body[m.end():]


def sources(body):
    """The sources and the note on how the answer was made, folded into one line (see the docstring)."""
    m = re.search(r'<section class="k-sec bg" id="sources"><div class="k-head"><h2>Sources</h2><span class="kicker">([^<]*)</span></div>'
                  r'(<div class="a-sources">.*?</div></div>)</section>', body, re.S)
    if not m:
        fail("no sources section")
    fold = ('<section class="k-sec bg enc-src" id="sources"><details class="enc-src-fold"><summary><h2>Sources</h2>'
            '<span class="kicker">%s</span></summary>%s</details></section>'
            % (m.group(1), m.group(2)))
    return body[:m.start()] + fold + body[m.end():]


def answer(name, body):
    if name == COLLAPSE:
        body = hero(body)
    if name in LABS:
        body = lab(body)
    body = sources(body)
    return body.replace("</body>", "<style>%s</style><script>%s</script>\n</body>" % (CSS, JS), 1)


# ── the A to Z page ─────────────────────────────────────────────────────────
def front(body, featured):
    """The Encarta front: the seven worlds, which filter the A to Z on this page, and the featured article."""
    topics = re.findall(r'<section class="az-group" id="[^"]+" data-topic="([^"]+)"', body)
    if not topics:
        fail("the A to Z has no topics")
    world = {}
    for key, _, _, ts in WORLDS:
        for t in ts:
            world[t] = key
    left = sorted(set(html.unescape(t) for t in topics) - set(world))
    if left:
        fail("A to Z topics with no world: %s" % left)
    counts = {}

    def mark(m):
        t = html.unescape(m.group(2))
        i = body.find("</section>", m.end())
        counts[world[t]] = counts.get(world[t], 0) + body[m.end():i].count('<li ')
        return '%s data-world="%s"' % (m.group(1), world[t])
    body = re.sub(r'(<section class="az-group" id="[^"]+" data-topic="([^"]+)")', mark, body)
    tiles = "".join('<li><button type="button" class="enc-w" data-w="%s" aria-pressed="false"><b>%s</b><small>%s</small>'
                    '<span>%d questions</span></button></li>' % (k, E(n), E(s), counts.get(k, 0)) for k, n, s, _ in WORLDS)
    href, q, short = featured
    feat = ('<a class="enc-feat" href="%s"><span class="enc-feat-art"><canvas aria-hidden="true"></canvas></span>'
            '<span class="enc-feat-t"><span class="enc-k">Featured &middot; animated</span><b>%s</b><em>%s</em>'
            '<span class="enc-go">Watch it fold and reopen, and tilt the wing yourself &rarr;</span></span></a>' % (href, E(q), E(short)))
    block = ('<section class="enc-front" aria-labelledby="encWT"><div class="enc-front-in">'
             '<div class="enc-front-h"><h2 id="encWT">Explore By Subject</h2><span class="enc-k">Seven worlds</span></div>'
             '<ul class="enc-worlds">%s</ul>%s</div></section>' % (tiles, feat))
    i = body.find('<section class="k-sec bg" id="a-to-z">')
    if i < 0:
        fail("the A to Z's list is not there")
    return body[:i] + block + body[i:].replace("</body>", "<style>%s</style><script>%s</script>\n</body>" % (CSS, JS), 1)


CSS = (
    # Collapse's moving wing, where the still drawing was
    ".enc-hero canvas{position:absolute;inset:0;width:100%;height:100%;display:block}"
    ".enc-hero-cap{position:absolute;z-index:2;right:var(--gutter);bottom:var(--sp-4);display:flex;flex-direction:column;"
    "align-items:flex-end;gap:.6rem;text-align:right;max-width:min(26rem,46%)}"
    ".enc-steps{list-style:none;margin:0;padding:0;font-size:.92rem;color:var(--gray-light)}"
    ".enc-steps b{color:var(--white);font-weight:600}"
    ".enc-hero.is-live~.enc-hero-cap .enc-steps li{display:none}"
    ".enc-hero.is-live~.enc-hero-cap .enc-steps li.is-on{display:block}"
    ".enc-view{font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gray)}"
    ".enc-replay{min-height:40px;padding:0 1rem;background:color-mix(in srgb,var(--bg) 70%,transparent);border:1px solid var(--edge-hi);"
    "color:var(--white);font:inherit;font-size:.85rem;cursor:pointer}"
    ".enc-replay:is(:hover,:focus-visible){border-color:var(--orange)}"
    # on a phone the title keeps the opening; the wing and its caption follow it, a block of their own
    "@media (max-width:980px){.a-hero:has(.enc-hero){flex-wrap:wrap;min-height:0}"
    ".a-hero .k-hero-copy{order:1}"
    ".k-hero-media.enc-hero{position:relative;inset:auto;z-index:0;order:2;flex:0 0 100%;height:min(64vw,420px);margin-top:var(--sp-3)}"
    ".enc-hero-cap{position:relative;order:3;flex:0 0 100%;right:auto;bottom:auto;align-items:flex-start;text-align:left;"
    "max-width:none;padding:0 var(--gutter) var(--sp-4)}}"
    # the angle-of-attack lab, in the drawing's place
    ".enc-lab{display:grid;gap:var(--sp-3);padding:var(--sp-3) 0}"
    ".enc-lab:not([hidden])~.bd-caps>div{transition:color .3s var(--ease),opacity .3s var(--ease);opacity:.45}"
    ".enc-lab:not([hidden])~.bd-caps>div.is-on{opacity:1}"
    ".enc-lab:not([hidden])~.bd-caps>div.is-on span{color:var(--orange)}"
    ".enc-foil{width:100%;max-width:760px;height:auto;margin:0 auto;display:block}"
    ".enc-foil .fl{fill:none;stroke:var(--gray);stroke-width:1.3;opacity:.55}"
    ".enc-foil .fl.off{stroke:var(--orange);stroke-dasharray:3 5;opacity:.9}"
    ".enc-foil .pf{fill:color-mix(in srgb,var(--white) 6%,var(--bg));stroke:var(--white);stroke-width:2}"
    ".enc-foil .pf.bad{fill:color-mix(in srgb,var(--orange) 18%,var(--bg))}"
    ".enc-foil .lf{stroke:var(--orange);stroke-width:3;fill:var(--orange)}"
    ".enc-foil text{fill:var(--orange);font-size:13px}"
    ".enc-range{display:grid;gap:.4rem;max-width:520px;width:100%;margin:0 auto;font-size:.78rem;letter-spacing:.14em;"
    "text-transform:uppercase;color:var(--gray-light)}"
    ".enc-range input{width:100%;accent-color:var(--orange);min-height:32px;cursor:pointer}"
    ".enc-ends{display:flex;justify-content:space-between;color:var(--gray);letter-spacing:.1em}.enc-ends i{font-style:normal}"
    # the sources, folded into one quiet line
    ".k-sec.enc-src{padding-top:var(--sp-4);padding-bottom:var(--sp-4)}"
    ".enc-src-fold{max-width:1300px;margin:0 auto}"
    ".enc-src-fold>summary{display:flex;align-items:baseline;flex-wrap:wrap;gap:.4rem 1.2rem;cursor:pointer;list-style:none;"
    "padding:var(--sp-2) 0;border-top:1px solid var(--edge);border-bottom:1px solid var(--edge)}"
    ".enc-src-fold>summary::-webkit-details-marker{display:none}"
    ".enc-src-fold>summary h2{font-size:var(--fs-h4);margin:0}"
    ".enc-src-fold>summary .kicker{color:var(--gray-light);font-size:var(--fs-small);margin-right:auto}"
    ".enc-src-fold>summary:hover h2{color:var(--orange)}"
    ".enc-src-fold[open]>.a-sources{padding-top:var(--sp-4)}"
    # the A to Z's front: the seven worlds and the featured article
    ".enc-front{padding:var(--sp-5) clamp(1.5rem,5vw,4rem) 0}"
    ".enc-front-in{max-width:1300px;margin:0 auto}"
    ".enc-front-h{display:flex;align-items:baseline;justify-content:space-between;gap:1rem;margin-bottom:var(--sp-3)}"
    ".enc-front-h h2{font-family:var(--font-display);font-size:clamp(1.5rem,2.6vw,2.1rem);margin:0;color:var(--white)}"
    ".enc-k{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--orange)}"
    ".enc-worlds{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:10px}"
    ".enc-w{display:flex;flex-direction:column;align-items:flex-start;gap:.35rem;width:100%;height:100%;padding:1rem .9rem;text-align:left;"
    "background:color-mix(in srgb,var(--white) 3%,transparent);border:1px solid var(--edge);color:var(--white);font:inherit;cursor:pointer;"
    "transition:border-color .3s var(--ease),background .3s var(--ease),transform .35s var(--ease)}"
    ".enc-w b{font-family:var(--font-display);font-size:1rem;line-height:1.2}"
    ".enc-w small{color:var(--gray-light);font-size:.78rem;line-height:1.4}"
    ".enc-w span{margin-top:auto;padding-top:.4rem;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gray)}"
    ".enc-w:is(:hover,:focus-visible){border-color:var(--orange);transform:translateY(-2px)}"
    ".enc-w[aria-pressed=true]{border-color:var(--orange);background:color-mix(in srgb,var(--orange) 10%,transparent)}"
    ".enc-w[aria-pressed=true] span{color:var(--orange)}"
    ".enc-feat{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);align-items:center;gap:clamp(1rem,4vw,3rem);"
    "margin-top:var(--sp-4);padding:var(--sp-3);border:1px solid var(--edge);color:inherit;text-decoration:none;"
    "transition:border-color .3s var(--ease)}"
    ".enc-feat:is(:hover,:focus-visible){border-color:var(--orange)}"
    ".enc-feat-art{position:relative;aspect-ratio:16/8;background:color-mix(in srgb,var(--white) 2%,transparent)}"
    ".enc-feat-art canvas{position:absolute;inset:0;width:100%;height:100%}"
    ".enc-feat-t{display:flex;flex-direction:column;gap:.6rem}"
    ".enc-feat-t b{font-family:var(--font-display);font-size:clamp(1.3rem,2.2vw,1.8rem);line-height:1.2;color:var(--white)}"
    ".enc-feat-t em{font-style:normal;color:var(--gray-light);line-height:1.6}"
    ".enc-go{color:var(--orange);font-weight:600;font-size:.92rem}"
    "#a-to-z[data-w] .az-group:not(.is-w){display:none}"
    "@media (max-width:1100px){.enc-worlds{grid-template-columns:repeat(4,minmax(0,1fr))}}"
    "@media (max-width:700px){.enc-worlds{grid-template-columns:repeat(2,minmax(0,1fr))}.enc-feat{grid-template-columns:minmax(0,1fr)}}"
    "@media (prefers-reduced-motion:reduce){.enc-w,.enc-feat{transition:none}.enc-w:hover{transform:none}}"
)

JS = r"""(function () {
  var d = document, still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function tok(v) {
    var e = d.createElement("i"); e.style.color = "var(" + v + ")"; e.style.display = "none"; d.body.appendChild(e);
    var m = getComputedStyle(e).color.match(/[\d.]+/g); e.remove(); return m ? m.slice(0, 3).map(Number) : [128, 128, 128];
  }
  var OR = tok("--orange"), WH = tok("--white"), GR = tok("--gray-light"), BG = tok("--bg");
  function col(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + (a == null ? 1 : a) + ")"; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function fit(c) {
    var r = c.getBoundingClientRect(), s = Math.min(2, window.devicePixelRatio || 1);
    c.width = Math.max(1, Math.round(r.width * s)); c.height = Math.max(1, Math.round(r.height * s));
    var x = c.getContext("2d"); x.setTransform(s, 0, 0, s, 0, 0); return { x: x, w: r.width, h: r.height };
  }
  /* a paraglider seen from behind (the Encarta build's): canopy arc, lines, pilot; fold 0..1 folds the right third */
  function glider(x, cx, cy, W, fold, roll) {
    x.save(); x.translate(cx, cy); x.rotate(roll);
    var n = 40, pts = [], R = W / 2;
    for (var i = 0; i <= n; i++) {
      var u = i / n, a = Math.PI * (1.12 - 1.24 * u), px = Math.cos(a) * R, py = -Math.sin(a) * R * 0.55;
      if (u > 0.62 && fold > 0) { var k = (u - 0.62) / 0.38, f = fold * Math.pow(k, 0.8); px = lerp(px, R * 0.5, f * 0.7); py = lerp(py, -R * 0.12 + k * R * 0.35, f); }
      pts.push([px, py]);
    }
    var pilot = [0, R * 0.95];
    x.strokeStyle = col(GR, 0.35); x.lineWidth = 1;
    for (var j = 2; j < n; j += 4) { x.beginPath(); x.moveTo(pts[j][0], pts[j][1]); x.lineTo(pilot[0] + (pts[j][0] > 0 ? 4 : -4), pilot[1] - 6); x.stroke(); }
    x.lineCap = "round";
    function arc(from) { x.beginPath(); for (var q = from; q <= n; q++) q === from ? x.moveTo(pts[q][0], pts[q][1]) : x.lineTo(pts[q][0], pts[q][1]); x.stroke(); }
    x.lineWidth = Math.max(8, W * 0.05); x.strokeStyle = col(WH, 0.1); arc(0);
    x.lineWidth = 2; x.strokeStyle = col(WH, 0.95); arc(0);
    if (fold > 0.02) { x.strokeStyle = col(OR, Math.min(1, fold * 1.4)); x.lineWidth = Math.max(6, W * 0.04); arc(Math.floor(n * 0.62)); }
    x.fillStyle = col(WH); x.beginPath(); x.arc(pilot[0], pilot[1] - 2, Math.max(4, W * 0.025), 0, 7); x.fill();
    x.fillStyle = col(GR, 0.5); x.fillRect(pilot[0] - W * 0.03, pilot[1] + 2, W * 0.06, W * 0.05);
    x.restore();
  }
  function arrowDown(x, ax, ay, len, a) {
    x.globalAlpha = a; x.strokeStyle = col(OR); x.fillStyle = col(OR); x.lineWidth = 2.5;
    x.beginPath(); x.moveTo(ax, ay); x.lineTo(ax, ay + len); x.stroke();
    x.beginPath(); x.moveTo(ax - 7, ay + len - 9); x.lineTo(ax, ay + len + 2); x.lineTo(ax + 7, ay + len - 9); x.fill(); x.globalAlpha = 1;
  }

  /* 1. Collapse: the wing folds and reopens, once in view and on Replay */
  var hero = d.querySelector(".enc-hero");
  if (hero) {
    var cv = hero.querySelector("canvas"), steps = [].slice.call(d.querySelectorAll(".enc-steps li")), rep = d.querySelector(".enc-replay");
    var T = steps.map(function (li) { return +li.getAttribute("data-t"); }), END = 7.6, C, t0 = 0, raf = 0, wide;
    hero.classList.add("is-live"); rep.hidden = false;
    function frame(t) {
      var x = C.x, w = C.w, h = C.h, fold = 0, roll = 0, sink = 0;
      x.clearRect(0, 0, w, h);
      /* the wing and the falling air above it fit the box: about 1.05 wings high in all */
      var W = Math.min(wide ? w * 0.36 : w * 0.62, 400, (h - 24) / 1.05), cx = wide ? w * 0.72 : w * 0.5;
      var cy = 12 + 0.555 * W + Math.max(0, (h - 24 - 1.05 * W) / (wide ? 2.4 : 2));
      x.strokeStyle = col(GR, 0.08); x.lineWidth = 1;
      for (var i = 0; i < 7; i++) { var yy = (i / 7) * h + ((still ? 0 : t) * 12) % (h / 7); x.beginPath(); x.moveTo(cx - W, yy); x.lineTo(cx + W, yy); x.stroke(); }
      if (t >= 1.5 && t < 2.6) sink = (t - 1.5) / 1.1;
      else if (t >= 2.6 && t < 3.4) fold = ease((t - 2.6) / 0.8);
      else if (t >= 3.4 && t < 5.2) { fold = 1; roll = Math.sin((t - 3.4) / 1.8 * Math.PI) * 0.22; }
      else if (t >= 5.2 && t < 6.6) { fold = 1 - ease((t - 5.2) / 1.4); roll = fold * 0.1; }
      if (sink > 0 || (fold > 0 && t < 3.4)) for (var k = 0; k < 3; k++) arrowDown(x, cx + W * (0.2 + k * 0.14), Math.max(4, cy - W * 0.555) + sink * 20, W * 0.24, Math.min(1, sink + fold));
      glider(x, cx, cy, W, fold, roll);
      if (fold > 0.5 && t > 3.4 && t < 5.2) { x.fillStyle = col(WH, 0.9); x.font = "600 13px " + getComputedStyle(d.body).fontFamily; x.fillText("← lean", cx - W * 0.3, cy + W * 0.44); }
      var on = 0; T.forEach(function (s, i) { if (t >= s) on = i; });
      steps.forEach(function (li, i) { li.classList.toggle("is-on", i === on); });
    }
    function size() { wide = window.innerWidth > 980; C = fit(cv); frame(still ? 4 : (t0 ? Math.min(END, (performance.now() - t0) / 1000) : 0)); }
    function tick(now) { var t = (now - t0) / 1000; frame(Math.min(t, END)); raf = t < END ? requestAnimationFrame(tick) : 0; }
    function play() { if (still) { frame(4); return; } t0 = performance.now(); if (!raf) raf = requestAnimationFrame(tick); }
    rep.addEventListener("click", play);
    size(); window.addEventListener("resize", size);
    if (still) frame(4);
    else if (window.IntersectionObserver) {
      var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); play(); } }, { threshold: 0.35 });
      io.observe(hero);
    } else play();
  }

  /* 2. the angle-of-attack lab: one profile, tilted with the slider; the page's three captions light in turn */
  [].forEach.call(d.querySelectorAll(".enc-lab-fig"), function (fig) {
    var lab = fig.querySelector(".enc-lab"), svg = lab.querySelector("svg"), range = lab.querySelector("input");
    var caps = [].slice.call(fig.querySelectorAll(".bd-caps > div"));
    lab.hidden = false; fig.querySelector(".enc-still").hidden = true;
    function naca(n) {
      var up = [], lo = [], th = 0.17, m = 0.04, p = 0.32;
      for (var i = 0; i <= n; i++) {
        var xx = (1 - Math.cos(Math.PI * i / n)) / 2, yt = 5 * th * (0.2969 * Math.sqrt(xx) - 0.126 * xx - 0.3516 * xx * xx + 0.2843 * Math.pow(xx, 3) - 0.1036 * Math.pow(xx, 4));
        var yc = xx < p ? m / (p * p) * (2 * p * xx - xx * xx) : m / Math.pow(1 - p, 2) * ((1 - 2 * p) + 2 * p * xx - xx * xx);
        up.push([xx, yc + yt]); lo.push([xx, yc - yt]);
      }
      return [up, lo];
    }
    var base = naca(60);
    function draw(a) {
      var stall = a > 17 ? Math.min(1, (a - 17) / 5) : 0, deflate = a < -2 ? Math.min(1, (-2 - a) / 6) : 0;
      var C2 = 300, cx = 230, cy = 150, r = -a * Math.PI / 180;
      function P(pt, lower) {
        var xx = pt[0], yy = pt[1];
        if (deflate && !lower && xx < 0.35) { var w = Math.pow(xx / 0.35, 1.3); yy = lerp(-0.02, yy, w * (1 - deflate) + w * w * deflate * 0.3 + (1 - deflate) * (1 - w)); }
        var X = (xx - 0.3) * C2, Y = -yy * C2;
        return [cx + X * Math.cos(r) - Y * Math.sin(r), cy + X * Math.sin(r) + Y * Math.cos(r)];
      }
      var U = base[0].map(function (q) { return P(q, false); }), L = base[1].map(function (q) { return P(q, true); }).reverse();
      var pf = "M" + U.concat(L).map(function (q) { return q[0].toFixed(1) + " " + q[1].toFixed(1); }).join("L") + "Z";
      var s = "";
      for (var i = 0; i < 6; i++) {
        var y0 = 60 + i * 36, bend = (a / 25) * (i < 3 ? -26 : -14), off = stall && i < 3;
        s += '<path class="fl' + (off ? " off" : "") + '" d="' + (off
          ? "M10 " + y0 + " C 120 " + y0 + ", 170 " + (y0 + bend) + ", 230 " + (y0 + bend - 6) + " q 30 -20 50 0 t 50 0 t 50 0"
          : "M10 " + y0 + " C 140 " + y0 + ", 200 " + (y0 + bend) + ", 300 " + (y0 + bend * 0.6) + " S 460 " + (y0 + bend * 0.2) + ", 510 " + y0) + '"/>';
      }
      var lift = a > -2 && a < 17 ? 30 + a * 5 : a >= 17 ? Math.max(10, 115 - (a - 17) * 14) : 6;
      s += '<path class="pf' + (deflate || stall ? " bad" : "") + '" d="' + pf + '"/>';
      s += '<path class="lf" d="M230 140 V' + (140 - lift) + '"/><path class="lf" d="M222 ' + (148 - lift) + " L230 " + (134 - lift) + " L238 " + (148 - lift) + 'Z"/>';
      if (deflate) s += '<path class="lf" d="M150 20 V75"/><path class="lf" d="M142 66 L150 80 L158 66Z"/><text x="162" y="34">sinking air</text>';
      svg.innerHTML = s;
      var on = a < -2 ? 0 : a > 17 ? 2 : 1;
      caps.forEach(function (c, i) { c.classList.toggle("is-on", i === on); });
    }
    range.addEventListener("input", function () { draw(+range.value); });
    draw(+range.value);
  });

  /* the sources, folded: a citation or the contents' link opens them on the way; a number shows its source's title */
  var fold = d.querySelector(".enc-src-fold");
  if (fold) {
    var openFor = function (id) { var t = id && d.getElementById(id); if (t && (t === fold.parentNode || fold.contains(t))) fold.open = true; };
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]'); if (a) openFor(a.getAttribute("href").slice(1));
    }, true);
    openFor(decodeURIComponent(location.hash.slice(1)));
    window.addEventListener("hashchange", function () { openFor(decodeURIComponent(location.hash.slice(1))); });
    [].forEach.call(d.querySelectorAll(".cite a"), function (a) {
      var li = d.getElementById(a.getAttribute("href").slice(1)), t = li && li.querySelector("a");
      if (t) a.title = t.textContent + (li.querySelector("span") ? ", " + li.querySelector("span").firstChild.textContent : "");
    });
  }

  /* 3. the A to Z: a world filters the list on this page; the featured wing, still, folded */
  var list = d.getElementById("a-to-z");
  if (list) {
    var tiles = [].slice.call(d.querySelectorAll(".enc-w")), n = d.getElementById("az-n"), empty = d.querySelector(".az-empty");
    function count() {
      if (!list.hasAttribute("data-w")) return;
      var k = 0; [].forEach.call(list.querySelectorAll(".az-group.is-w .az-list li"), function (li) { if (!li.hidden) k++; });
      if (n) n.textContent = k + (k === 1 ? " question" : " questions");
      if (empty) empty.style.display = k ? "none" : "block";
    }
    tiles.forEach(function (b) {
      b.addEventListener("click", function () {
        var w = b.getAttribute("data-w"), on = list.getAttribute("data-w") !== w;
        tiles.forEach(function (x) { x.setAttribute("aria-pressed", String(on && x === b)); });
        if (on) list.setAttribute("data-w", w); else list.removeAttribute("data-w");
        [].forEach.call(list.querySelectorAll(".az-group"), function (g) { g.classList.toggle("is-w", g.getAttribute("data-world") === w); });
        if (!on) { var q = d.getElementById("az-q"); if (q) q.dispatchEvent(new Event("input")); }
        count();
        if (on) list.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" });
      });
    });
    list.addEventListener("input", function () { setTimeout(count, 0); });
    list.addEventListener("click", function () { setTimeout(count, 0); });
    var fc = d.querySelector(".enc-feat-art canvas");
    if (fc) { var paint = function () { var F = fit(fc), W = Math.min(F.w * 0.6, (F.h - 24) / 0.78); F.x.clearRect(0, 0, F.w, F.h);
      glider(F.x, F.w * 0.5, (F.h - 0.75 * W) / 2 + 0.275 * W, W, 0.85, 0.12); };
      paint(); window.addEventListener("resize", paint); }
  }
})();"""
