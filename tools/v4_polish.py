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
    as before (v2-immersive.js). Reduced motion: the page as it was. Arriving
    with a series in the address, the page stays unseen for the instant it
    takes v2-library.js to open it on the list (at most 1.2 s). With a
    series chosen the list opens on the series' introduction (v2-library.js):
    its drawing, category, name, its question and knowledge base page (read
    here from the knowledge base page into window.V4_SX) and its figures.
  - knowledge base (roadmap step 3): on the hub, the climb in the opening
    keeps its route, dimmer, and a bright trace climbs it with the scroll with
    a glider at its tip, from 600 m to 4,000 m as the opening scrolls away;
    each level's big outlined number fills in orange while that level is in
    the middle of the screen; each level's row of episodes glides in from the
    side as it comes into view (on a phone it fades in, so the page never
    widens). On the 18 category pages: the opening's
    drawing drifts slower than the page and, on a desktop, leans towards the
    mouse; the questions glide open and closed, their answer fading up.
    Reduced motion: the pages as they were.
    And the look (owner, 20 Oct 2026, from a side-by-side preview): on the
    hub each level's number is solid white and larger with its altitude in
    orange, its series are larger panels with the question in readable grey,
    and its episodes are pictures with their titles under them, the pictures
    grey and dimmed as before until the pointer is on one; on the category
    pages the opening's drawing is larger behind a larger title on a wide
    screen (a drawing with its own words in it keeps its size, so they never
    meet the page's); on a tablet, where drawings ran under the opening's
    words before this pass too, the drawing draws smaller towards the right,
    clear of them; and the
    questions have more room, larger type and an answer column clear of the
    open question's orange edge; each answer is as large as its question
    (owner: small answers were hard to read), its sources at body size; the
    note under the questions' heading at body size and, on the hub, the
    episode titles at 16 px (reading text, from the owner's preview: the
    series' questions stay as they were).

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
  /* arriving with a series (or #all) in the address: the page stays unseen for the moment it takes
     v2-library.js to put the list in view, so it opens on the list rather than flashing the top first;
     v2-library.js lifts this, and so does a timer, so the page can never stay unseen */
  if (/(?:^|[#&])s=|^#all$/.test(location.hash)) {
    var h0 = document.documentElement; h0.classList.add('v4-land');
    setTimeout(function () { h0.classList.remove('v4-land'); }, 1200);
  }
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

KB_HUB_CSS = (
    # visual (owner, 20 Oct 2026: "go ahead with all", the pictures lit only on hover)
    # the level numbers solid and larger, the altitude beside them in orange
    "html body .clb-idx{color:var(--white);-webkit-text-stroke:0;font-size:clamp(3rem,7vw,5.5rem)}"
    "html body .clb-alt b{color:var(--orange);font-weight:700;font-size:clamp(1.05rem,1.9vw,1.35rem)}"
    # the series panels: larger, the series in white, its question readable under it
    "html body .clb-topics{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:.8rem}"
    "html body .clb-topics .clb-topic{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1fr) auto;align-content:start;"
    "gap:.55rem 1rem;min-height:6.5rem;padding:1.15rem 1.3rem;border-radius:10px;border:1px solid var(--line);background:var(--card);"
    "font-family:var(--font-display);font-weight:600;font-size:1.05rem;color:var(--white)}"
    "html body .clb-topics .clb-topic:hover{border-color:var(--live)}"
    "html body .clb-topics .clb-topic b{font-size:1rem}"
    "html body .clb-topics .clb-topic .v4-q{font-family:var(--font-body);font-weight:400;font-size:.95rem;line-height:1.45;color:var(--gray-light)}"
    # the episodes: a picture with its title under it; the picture keeps its grey until the pointer is on it
    "html body .clb-strip{grid-auto-columns:minmax(200px,1fr);gap:1rem}"
    "html body .clb-strip:has(> .clb-face:only-child){grid-auto-columns:minmax(200px,260px)}"
    "html body .clb-face{aspect-ratio:auto;overflow:visible;background:none;border:0;border-radius:0}"
    "html body .clb-face img{aspect-ratio:16/9;height:auto;border-radius:8px;border:1px solid var(--edge)}"
    "html body .clb-face:hover img{transform:none}"
    "html body .clb-face .clb-face-t{position:static;background:none;border:0;padding:.65rem .1rem 0;font-size:1rem;line-height:1.35;"
    "color:var(--gray-light);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;transition:color .3s var(--ease)}"
    "html body .clb-face:is(:hover,:focus-visible) .clb-face-t{color:var(--white)}"
    "@media (max-width:760px){html body .clb-strip{grid-auto-columns:minmax(180px,64vw)}}"
    # the trace: the route stays, dimmer; a bright copy climbs it with the scroll, a glider at its tip
    "html.v4-kbm .v4-climb-line{opacity:.32}"
    "html.v4-kbm .v4-climb .v4p-trace{fill:none;stroke:var(--orange);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}"
    "html.v4-kbm .v4-climb .v4p-glider{fill:var(--orange);filter:drop-shadow(0 0 6px rgba(255,117,23,.8))}"
    # the level numbers: an outline until their level is in the middle of the screen, then filled in orange
    "html.v4-kbm .clb-idx{transition:color .6s var(--ease),-webkit-text-stroke-color .6s var(--ease)}"
    "html.v4-kbm .clb-station.v4p-on .clb-idx{color:var(--orange);-webkit-text-stroke-color:var(--orange)}"
    # the episode rows glide in from the side as they come into view
    "html.v4-kbm .clb-strip{transition:transform .9s var(--ease),opacity .9s var(--ease)}"
    "html.v4-kbm .clb-strip:not(.v4p-in){opacity:0}"
    "@media (min-width:900px){html.v4-kbm .clb-strip:not(.v4p-in){transform:translateX(48px)}}"
)
KB_HUB_JS = r"""(function () {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;
  var html = document.documentElement; html.classList.add('v4-kbm');
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    var NS = 'http://www.w3.org/2000/svg';
    var line = document.querySelector('.v4-climb .v4-climb-line'), hero = document.querySelector('.clb-hero'), trace = null, glider = null, L = 0;
    if (line && line.getTotalLength) {
      L = line.getTotalLength();
      trace = document.createElementNS(NS, 'path'); trace.setAttribute('d', line.getAttribute('d')); trace.setAttribute('class', 'v4p-trace');
      trace.style.strokeDasharray = L; line.parentNode.insertBefore(trace, line.nextSibling);
      glider = document.createElementNS(NS, 'circle'); glider.setAttribute('r', '5'); glider.setAttribute('class', 'v4p-glider');
      line.parentNode.insertBefore(glider, trace.nextSibling);
    }
    var raf = 0;
    function tick() {
      raf = 0; if (!trace || !hero) return;
      var p = Math.min(1, Math.max(0, window.scrollY / Math.max(1, hero.offsetHeight * 0.85)));
      p = 0.04 + p * 0.96;
      trace.style.strokeDashoffset = (L * (1 - p)).toFixed(1);
      var pt = line.getPointAtLength(L * p); glider.setAttribute('cx', pt.x.toFixed(1)); glider.setAttribute('cy', pt.y.toFixed(1));
    }
    window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
    tick();
    var mid = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('v4p-on', e.isIntersecting); }); },
      { rootMargin: '-42% 0px -42% 0px' });
    document.querySelectorAll('.clb-station').forEach(function (st) { mid.observe(st); });
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('v4p-in'); io.unobserve(e.target); } }); },
      { rootMargin: '0px 0px -12% 0px' });
    document.querySelectorAll('.clb-strip').forEach(function (st) { io.observe(st); });
  });
})();"""

KB_CAT_CSS = (
    # visual: the opening more like a poster, the drawing larger behind a larger title
    "html body .k-hero{overflow:hidden}"
    "@media (min-width:1200px){html body .k-hero-media:not(:has(text)){transform:scale(1.28);transform-origin:88% 50%}"
    "html body .k-hero-copy h1{font-size:clamp(2.6rem,4.6vw,4.4rem);max-width:15ch}}"
    # on a tablet the drawing ran under the opening's words (it did before this pass too): it draws smaller,
    # towards the right, clear of them
    "@media (min-width:761px) and (max-width:1199px){html body .k-hero-media{transform:scale(.72);transform-origin:100% 50%}}"
    "@media (min-width:1200px) and (max-width:1439px){html body .k-hero-media:has(text){transform:scale(.86);transform-origin:100% 50%}}"
    # the questions: more room, larger questions, a readable answer clear of the open question's orange edge
    "html body .faq-r summary{padding:1.35rem 0;font-size:clamp(1.08rem,1.5vw,1.3rem);line-height:1.35}"
    "html body .faq-r details[open]{padding-left:1.5rem;margin-left:-1.625rem}"
    # the answer as large as its question (owner, 20 Oct 2026: small answers were hard to read), its colour,
    # weight and face kept; the column wider to suit; the sources under it at the page's body size
    "html body[data-v2] .faq .faq-r details p{font-size:clamp(1.08rem,1.5vw,1.3rem);line-height:1.7;max-width:46rem}"
    "html body .faq-r details .src{font-size:var(--fs-body)}html body .faq-r details .src span{font-size:inherit}"
    "html body .faq-r details .src{display:inline-block;margin-bottom:1.3rem}"
    # the note under the questions' heading at the page's body size (owner, 20 Oct 2026: reading text, approved)
    "html body .faq .faq-l p{font-size:var(--fs-body);line-height:1.65;color:var(--gray-light)}"
    "@media (max-width:760px){html body .faq-r details[open]{margin-left:0;padding-left:1rem}"
    "html body .faq-r details .src{display:block;margin:0 0 .5rem}html body .faq-r details .src + .src{margin-left:0}"
    "html body .faq-r details .src:last-of-type{margin-bottom:1.3rem}}"
    "html.v4-kbc .k-hero-media{perspective:1200px}"
    "html.v4-kbc .k-hero-media>svg{transform:translate3d(0,var(--py,0px),0) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));"
    "transition:transform .9s var(--ease);will-change:transform}"
    "html.v4-kbc .faq-r details{overflow:hidden}"
)
KB_CAT_JS = r"""(function () {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var html = document.documentElement; html.classList.add('v4-kbc');
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    /* the hero drawing: drifts slower than the page, and on a desktop leans towards the mouse */
    var media = document.querySelector('.k-hero-media'), art = media && media.querySelector('svg'), raf = 0;
    function tick() {
      raf = 0; if (!art) return;
      var y = Math.min(window.scrollY, window.innerHeight);
      art.style.setProperty('--py', (y * 0.25).toFixed(1) + 'px');
    }
    if (art) {
      window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
      if (window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches) {
        var hero = document.querySelector('.k-hero');
        hero.addEventListener('pointermove', function (e) {
          if (e.pointerType !== 'mouse') return;
          var r = hero.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, yy = (e.clientY - r.top) / r.height - 0.5;
          art.style.setProperty('--ry', (x * 6).toFixed(2) + 'deg'); art.style.setProperty('--rx', (-yy * 4).toFixed(2) + 'deg');
        });
        hero.addEventListener('pointerleave', function () { art.style.removeProperty('--rx'); art.style.removeProperty('--ry'); });
      }
    }
    /* the questions glide open and closed */
    var EASE = 'cubic-bezier(.2,.8,.2,1)';
    document.querySelectorAll('.faq-r details').forEach(function (d) {
      var sum = d.querySelector('summary'); if (!sum || !d.animate) return;
      var anim = null;
      sum.addEventListener('click', function (e) {
        e.preventDefault();
        if (anim) anim.cancel();
        var start = d.offsetHeight;
        if (d.open) {
          var end = sum.offsetHeight;
          anim = d.animate({ height: [start + 'px', end + 'px'] }, { duration: 380, easing: EASE });
          anim.onfinish = function () { d.open = false; anim = null; d.style.height = ''; };
        } else {
          d.style.height = start + 'px'; d.open = true;
          var full = d.scrollHeight; d.style.height = '';
          anim = d.animate({ height: [start + 'px', full + 'px'] }, { duration: 460, easing: EASE });
          anim.onfinish = function () { anim = null; };
          var kids = [].slice.call(d.children).filter(function (k) { return k !== sum; });
          kids.forEach(function (k, i) { k.animate({ opacity: [0, 1], transform: ['translateY(6px)', 'none'] }, { duration: 420, delay: 80 + i * 40, easing: EASE, fill: 'backwards' }); });
        }
      });
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
    "html.v4-land body{opacity:0}"
    # the series' introduction (v2-library.js): its drawing, then its words and figures
    ".v4-sx{display:grid;grid-template-columns:minmax(220px,340px) minmax(0,1fr);gap:clamp(1.5rem,4vw,3.5rem);align-items:center;"
    "margin:0 0 var(--sp-5);padding-bottom:var(--sp-5);border-bottom:1px solid var(--line)}"
    ".v4-sx[hidden]{display:none}"
    ".v4-sx-art{border-radius:12px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.45);aspect-ratio:200/138;background:var(--card)}"
    ".v4-sx-art svg{width:100%;height:100%;display:block}"
    ".v4-sx-k{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--orange);margin:0 0 .7rem}"
    ".v4-sx-h{font-family:var(--font-display);font-weight:700;font-size:clamp(2.4rem,5vw,4rem);line-height:1.02;margin:0 0 .9rem;color:var(--white)}"
    ".v4-sx-q{font-size:clamp(1.05rem,1.5vw,1.3rem);line-height:1.5;color:var(--gray-light);margin:0 0 1.6rem;max-width:34ch}"
    ".v4-sx-n{display:flex;flex-wrap:wrap;gap:1.2rem clamp(1.6rem,4vw,3rem);margin:0 0 1.6rem;padding-top:1.1rem;border-top:1px solid var(--line);max-width:34rem}"
    ".v4-sx-n b{display:block;font-family:var(--font-display);font-weight:700;font-size:clamp(1.6rem,2.6vw,2.2rem);line-height:1;color:var(--white);font-variant-numeric:tabular-nums}"
    ".v4-sx-n span{display:block;margin-top:.45rem;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gray)}"
    ".v4-sx-a{color:var(--white);text-decoration:none;border-bottom:1px solid var(--orange);padding-bottom:.2rem;font-weight:600;"
    "transition:color .3s var(--ease)}"
    ".v4-sx-a:hover{color:var(--orange)}"
    "@media (max-width:760px){.v4-sx{grid-template-columns:1fr}}"
    ),
}
PAGES["knowledge-base.html"] = KB_HUB_CSS
SCRIPTS = {"podcast.html": POD_JS, "library.html": LIB_JS, "knowledge-base.html": KB_HUB_JS}
for _f in sorted(os.listdir(os.path.join(V4, "knowledge-base"))):
    if _f.endswith(".html"):
        PAGES["knowledge-base/" + _f] = KB_CAT_CSS
        SCRIPTS["knowledge-base/" + _f] = KB_CAT_JS


def series_intro():
    """window.V4_SX for the library's series introduction (v2-library.js): each library series' question and
    knowledge base page, read from the knowledge base page's own panels; the question in sentence case. Every
    series must be found, or this stops."""
    import html as H
    import json
    kb = open(os.path.join(V4, "knowledge-base.html"), encoding="utf-8").read()
    lib = open(os.path.join(V4, "library.html"), encoding="utf-8").read()
    K = {m.group(1): H.unescape(m.group(2)) for m in re.finditer(
        r'<a class="clb-topic" href="knowledge-base/([a-z0-9-]+)\.html"><span>[^<]*</span><b>\d+</b><span class="v4-q">([^<]*)</span>', kb)}
    out = {}
    for t in (H.unescape(x) for x in re.findall(r'<a class="tile[^"]*" href="[^"]*" data-t="([^"]*)"', lib)):
        w = re.sub(r"[^a-z0-9 ]", "", t.lower().replace("&", " ")).split()
        hit = [x for x in ("-".join(w), "-".join(y for y in w if y != "and")) if x in K]
        if not hit:
            raise SystemExit("v4_polish: the library series %r has no knowledge base panel" % t)
        q = K[hit[0]].lower()
        q = re.sub(r"\bi\b", "I", q[:1].upper() + q[1:])
        out[t] = {"q": q, "u": "knowledge-base/%s.html" % hit[0]}
    return "window.V4_SX=" + json.dumps(out, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";\n"


def main():
    for rel, css in PAGES.items():
        p = os.path.join(V4, rel)
        html = open(p, encoding="utf-8").read()
        html = re.sub(r"<!--v4p:polish-->.*?<!--/v4p:polish-->\n", "", html, flags=re.S)
        if html.count("<!-- site-schema -->") != 1:
            raise SystemExit("v4_polish: no single <!-- site-schema --> in " + rel)
        html = html.replace("<!-- site-schema -->",
                            "<!--v4p:polish--><style>%s</style>%s<!--/v4p:polish-->\n<!-- site-schema -->"
                            % (css, "<script>%s</script>" % ((series_intro() if rel == "library.html" else "") + SCRIPTS[rel])
                               if rel in SCRIPTS else ""), 1)
        if rel == "podcast.html" and POD_LOADER[1] not in html:
            if html.count(POD_LOADER[0]) != 1:
                raise SystemExit("v4_polish: podcast.html: the globe loader is not there once")
            html = html.replace(POD_LOADER[0], POD_LOADER[1])
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print("v4_polish: " + rel)


if __name__ == "__main__":
    main()
