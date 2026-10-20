#!/usr/bin/env python3
"""
The awwwards-direction polish (owner, 20 Oct 2026): what the record page did
best, kept where it makes a page richer and never by taking motion away (the
owner turned down a pass that stilled the home page). One page at a time, each
page's own look in one <style> between <!--v4p:polish--> and <!--/v4p:polish-->
right before <!-- site-schema -->, so v2.css and every other page are as they
were. Rewritten whole each run, so the pass is idempotent.

  - podcast: the opening's three figures (100,000+ streams, 136 countries
    reached, 80+ expert insights) are solid in the display face, large and
    tabular, instead of thin outlined numerals; their labels in quiet small
    capitals. Every word and number is the page's own.
  - podcast, scroll (owner, 20 Oct 2026: "push it to the page directly"):
    three moments driven by the scroll alone, eased, nothing taken away:
    the guest names behind the opening slide sideways in rows, alternate
    rows the other way and each row at its own pace, as the opening scrolls
    away; the pull quote lights up word by word, dim to white in reading
    order, as it crosses the screen; and the globe turns with the scroll
    while it is in view, at most 6 degrees a frame so a jump to it does not
    spin it round (its own spin, drag, zoom and pins as before). The
    globe is the live globe.js, untouched: the page's own loader calls
    window.v4BeforeGlobe just before it loads globe.js, which notes the first
    orthographic projection the globe makes, and the scroll turns that; the
    globe's own spin draws it. With reduced motion or without JavaScript the
    page is as it was.
  - library (owner's roadmap, step 2, 20 Oct 2026): the opening's chart
    arrives once and settles (the bars grow from the baseline, the dots
    settle on them, then the longest episode's marker and its guide draw)
    and drifts up more slowly than the page as the opening scrolls away; on
    a desktop the series tiles lean towards the mouse in 3D with a soft light
    where it is, and glide back level. The tiles' drawings draw themselves in
    as before (v2-immersive.js). Reduced motion: the page as it was.

    python3 tools/v4_polish.py            # every page done so far

It runs in tools/v4_build.py after v4_ux.
"""
import os
import re

POD_JS = r"""(function () {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var proj = null;
  window.v4BeforeGlobe = function () {
    var d3 = window.d3; if (!d3 || !d3.geoOrthographic || d3.geoOrthographic.v4) return;
    var orig = d3.geoOrthographic;
    d3.geoOrthographic = function () { var p = orig.apply(this, arguments); if (!proj) proj = p; return p; };
    d3.geoOrthographic.v4 = 1;
  };
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    var html = document.documentElement;
    /* the pull quote, a word at a time */
    var q = document.querySelector('.v2-pull p'), words = [];
    if (q && !q.querySelector('.v4w')) {
      var parts = q.textContent.split(/\s+/).filter(Boolean);
      q.textContent = '';
      parts.forEach(function (w, i) {
        var sp = document.createElement('span'); sp.className = 'v4w'; sp.textContent = w;
        q.appendChild(sp); if (i < parts.length - 1) q.appendChild(document.createTextNode(' '));
        words.push(sp);
      });
      html.classList.add('v4-scrub');
    }
    /* the guest names, in rows */
    var vp = document.querySelector('.v4-voices p'), names = vp ? [].slice.call(vp.children) : [], rowOf = [];
    function rows() {
      var tops = [];
      names.forEach(function (n) { var t = n.offsetTop; if (tops.indexOf(t) < 0) tops.push(t); });
      tops.sort(function (a, b) { return a - b; });
      rowOf = names.map(function (n) { return tops.indexOf(n.offsetTop); });
    }
    if (names.length) { html.classList.add('v4-rows'); rows(); }
    var hero = document.querySelector('.v4-voices-hero'), map = document.getElementById('map');
    var lastY = window.scrollY, lit = -1, raf = 0;
    function tick() {
      raf = 0;
      var vh = window.innerHeight, y = window.scrollY;
      if (hero && names.length) {
        var hb = hero.getBoundingClientRect();
        if (hb.bottom > 0) {
          var p = Math.min(1, Math.max(0, -hb.top / Math.max(1, hb.height)));
          for (var i = 0; i < names.length; i++) {
            var r = rowOf[i], dir = r % 2 ? 1 : -1, sp = 130 + (r % 3) * 90;
            names[i].style.transform = 'translate3d(' + (dir * p * sp).toFixed(1) + 'px,0,0)';
          }
        }
      }
      if (words.length) {
        var qb = q.getBoundingClientRect();
        var t = Math.min(1, Math.max(0, (vh * 0.86 - qb.top) / (qb.height + vh * 0.36)));
        var n = Math.round(t * words.length);
        if (n !== lit) { for (var j = 0; j < words.length; j++) words[j].classList.toggle('on', j < n); lit = n; }
      }
      if (proj && map && !document.body.classList.contains('kb-modal-open')) {
        var mb = map.getBoundingClientRect();
        if (mb.bottom > 0 && mb.top < vh) { var rr = proj.rotate(), turn = Math.max(-6, Math.min(6, (y - lastY) * 0.09)); proj.rotate([rr[0] - turn, rr[1], rr[2] || 0]); }
      }
      lastY = y;
    }
    window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
    window.addEventListener('resize', function () { if (names.length) rows(); if (!raf) raf = requestAnimationFrame(tick); });
    tick();
  });
})();"""

POD_LOADER = ('      s.src = SRC[i]; s.onload = s.onerror = function () { next(i + 1); };\n',
              '      s.src = SRC[i]; s.onload = s.onerror = function () {\n'
              '        if (/globe\\.js$/.test(SRC[i + 1] || "") && window.v4BeforeGlobe) window.v4BeforeGlobe();   // v4p: the scroll turns the globe\n'
              '        next(i + 1);\n'
              '      };\n')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")

LIB_JS = r"""(function () {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var html = document.documentElement;
  html.classList.add('v4-grow');
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    /* the chart drifts up more slowly than the page as the opening scrolls away */
    var chart = document.querySelector('.dk-tg-library'), raf = 0;
    function tick() {
      raf = 0; if (!chart) return;
      var y = Math.min(window.scrollY, window.innerHeight);
      chart.style.transform = 'translate3d(0,' + (y * 0.22).toFixed(1) + 'px,0)';
    }
    window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
    /* the series tiles lean towards the mouse, with a soft light on them */
    if (!(window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches)) return;
    html.classList.add('v4-tilt');
    document.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      var t = e.target.closest && e.target.closest('.v2-tiles .tile'); if (!t) return;
      var s = t.querySelector('.shot'); if (!s) return;
      var r = s.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      if (x < 0 || x > 1 || y < 0 || y > 1) return;
      s.style.setProperty('--ry', ((x - 0.5) * 10).toFixed(2) + 'deg');
      s.style.setProperty('--rx', ((0.5 - y) * 8).toFixed(2) + 'deg');
      s.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
      s.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    }, { passive: true });
    document.addEventListener('pointerout', function (e) {
      var t = e.target.closest && e.target.closest('.v2-tiles .tile');
      if (!t || (e.relatedTarget && t.contains(e.relatedTarget))) return;
      var s = t.querySelector('.shot'); if (s) { s.style.removeProperty('--rx'); s.style.removeProperty('--ry'); }
    });
  });
})();"""

PAGES = {
    "podcast.html": (
        ".v2-pod-hero .kit-stats{gap:var(--sp-3) clamp(2.2rem,5vw,4rem);max-width:48rem;flex-wrap:nowrap}"
        ".v2-pod-hero .kit-stat b{-webkit-text-stroke:0;-webkit-text-fill-color:var(--white);color:var(--white);"
        "font-family:var(--font-display);font-weight:700;font-size:clamp(2rem,4.2vw,3.25rem);line-height:1;"
        "letter-spacing:-.02em;font-variant-numeric:tabular-nums}"
        ".v2-pod-hero .kit-stat span{color:var(--gray-light);margin-top:.55rem}"
        "@media (max-width:560px){.v2-pod-hero .kit-stats{gap:1.2rem;justify-content:space-between}"
        ".v2-pod-hero .kit-stat b{font-size:clamp(1.45rem,7vw,1.9rem)}}"
        "html.v4-rows .v4-voices p span{display:inline-block;will-change:transform}"
        "html.v4-rows .v4-voices span + span::before{white-space:pre}"
        "html.v4-scrub .v2-pull .v4w{color:var(--edge-hi);transition:color .45s var(--ease)}"
        "html.v4-scrub .v2-pull .v4w.on{color:var(--white)}"
    ),
    "library.html": (
        # the chart arrives: the bars grow from the baseline, the dots settle on them, the longest's marker draws
        "@keyframes v4p-rise{from{transform:scaleY(0)}}"
        "@keyframes v4p-dots{from{opacity:0;transform:translateY(14px)}}"
        "@keyframes v4p-mark{from{transform:scaleY(0)}}"
        "@keyframes v4p-guide{from{transform:scaleX(0)}}"
        "@keyframes v4p-fade{from{opacity:0}}"
        "html.v4-grow .dk-tg-library{will-change:transform}"
        "html.v4-grow .dk-tg-library .d{transform-box:fill-box;transform-origin:50% 100%;animation:v4p-rise 1.4s var(--ease) .2s both}"
        "html.v4-grow .dk-tg-library path[stroke-width]{animation:v4p-dots .9s var(--ease) 1s both}"
        "html.v4-grow .dk-tg-library .a{transform-box:fill-box;transform-origin:50% 100%;animation:v4p-mark .8s var(--ease) 1.4s both}"
        "html.v4-grow .dk-tg-library .g{transform-box:fill-box;transform-origin:100% 50%;animation:v4p-guide .8s var(--ease) 1.8s both}"
        "html.v4-grow .dk-tg-library :is(.fa,.val){animation:v4p-fade .6s var(--ease) 2.1s both}"
        # the tiles lean towards the mouse, a soft light where it is
        "html.v4-tilt .v2-tiles .tile .shot{position:relative;transform:perspective(800px) translateY(var(--ty,0px)) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));"
        "transition:transform .6s var(--ease),box-shadow .4s var(--ease)}"
        "html.v4-tilt .v2-tiles .tile:is(:hover,:focus-visible) .shot{--ty:-4px;transition:transform .18s var(--ease),box-shadow .4s var(--ease)}"
        "html.v4-tilt .v2-tiles .tile .shot::after{content:\"\";position:absolute;inset:0;pointer-events:none;opacity:0;"
        "background:radial-gradient(60% 60% at var(--mx,50%) var(--my,50%),rgba(246,244,244,.14),transparent 70%);transition:opacity .4s var(--ease)}"
        "html.v4-tilt .v2-tiles .tile:hover .shot::after{opacity:1}"
    ),
}
SCRIPTS = {"podcast.html": POD_JS, "library.html": LIB_JS}


def main():
    for rel, css in PAGES.items():
        p = os.path.join(V4, rel)
        html = open(p, encoding="utf-8").read()
        html = re.sub(r"<!--v4p:polish-->.*?<!--/v4p:polish-->\n", "", html, flags=re.S)
        if html.count("<!-- site-schema -->") != 1:
            raise SystemExit("v4_polish: no single <!-- site-schema --> in " + rel)
        html = html.replace("<!-- site-schema -->",
                            "<!--v4p:polish--><style>%s</style>%s<!--/v4p:polish-->\n<!-- site-schema -->"
                            % (css, "<script>%s</script>" % SCRIPTS[rel] if rel in SCRIPTS else ""), 1)
        if rel == "podcast.html" and POD_LOADER[1] not in html:
            if html.count(POD_LOADER[0]) != 1:
                raise SystemExit("v4_polish: podcast.html: the globe loader is not there once")
            html = html.replace(POD_LOADER[0], POD_LOADER[1])
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print("v4_polish: " + rel)


if __name__ == "__main__":
    main()
