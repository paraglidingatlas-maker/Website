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
    and drifts up more slowly than the page as the opening scrolls away
    (never further than the room under it in the opening, so it never runs
    over the next section; fixed 21 Oct after the review found it did on a
    phone); on
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
  - topics (owner, 20 Oct 2026, from a preview: "the bigger picture will
    overlap with text so adjust accordingly"): on the 50 topic pages each
    episode's picture is larger in its own column, so it never meets the
    words (narrower on a narrow card; on a phone above the words, full
    width), grey and dimmed until the pointer is on the card (on a touch
    screen, while the card is mid-screen); the descriptions at 16 px and the
    titles a step larger. Sorting (the live tags-sort.js) glides each card on
    screen from its old place to its new one. On the Topics page the topics
    rise in a row at a time as they come into view, each trend line drawing
    left to right after its topic; the pointer on a topic makes its line glow
    and draw again; and the topic search glides the topics left to their new
    places instead of the grid jumping. Reduced motion: no motion, the look
    kept.
  - From the 21 Oct review of every page type (owner: "complete all"): on the
    podcast, the live feed's failure line (rss-feed.js, which promises an
    archive below that is not there) says so and points to the library; on
    home, a soft dark shadow behind the small orange line over the footage,
    so it reads on snow; on the topic pages, the phone chart's words at
    reading size; corrections in the text of every page that has them (an
    episode description that lost its maker's name, from its own title;
    Kenya's "It's"; topic pages that promised a full transcript for every
    conversation, now giving their own count); and About's India card takes
    a photograph not used elsewhere on the site (owner: no photograph
    twice).
  - About (owner, 21 Oct 2026, from side-by-side previews): the opening's
    figures (500+, 4, 10+) large and solid, counting up once (the real
    figure kept for screen readers and at the end, the width held so nothing
    moves); the origin story flies as on the live about.html: its drawing
    (read from the live page each run) across the page under the story's
    words, flown once as it comes into view, each step (the v4 page's own
    three) arriving as the line reaches it, at 16 px; the promises' words at
    16 px; Navigate, Aviate, Communicate as giant rows of pure type, each
    filling white from an outline as it reaches the middle of the screen;
    the trips lean towards the mouse with a soft light, as the library's
    tiles. The photo already comes closer with the scroll (v2.css).
  - Mission: On this page follows the reading (the section being read lit
    and marked current, the ones read marked, the line beside the list
    filling orange down to the reader); the verse's translation lights word
    by word as it crosses the screen, as the podcast's pull quote; the photo
    at the top comes closer as the page scrolls, its own slow drift kept.
    Reduced motion: no motion (On this page still follows the reading).

    python3 tools/v4_polish.py            # every page done so far

It runs in tools/v4_build.py after v4_ux.
"""
import os
import re

POD_JS = r"""(function () {
  /* the live feed (rss-feed.js, never edited) says on failure that "the saved archive is below instead", and
     nothing is below it: on v4 the line says so and points to the library, where every episode is */
  function fix() {
    var st = document.getElementById('liveFeedStatus');
    if (!st || !/saved archive is below/.test(st.textContent)) return;
    st.innerHTML = 'Could not reach the live feed right now. Every episode is in the <a href="library.html">library</a>.';
  }
  function watch() {
    var st = document.getElementById('liveFeedStatus'); if (!st) return;
    fix(); if (window.MutationObserver) new MutationObserver(fix).observe(st, { childList: true, characterData: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', watch); else watch();
})();
(function () {
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
    /* the chart drifts up more slowly than the page as the opening scrolls away, never further than the room
       left under it in the opening, so it never runs over the next section's heading (on a phone that room is
       small and the chart barely moves) */
    var chart = document.querySelector('.dk-tg-library'), box = chart && (chart.closest('header, section') || chart.parentNode);
    var raf = 0, cur = 0, room = 0;
    function measure() {
      if (!chart) return;
      room = Math.max(0, box.getBoundingClientRect().bottom - (chart.getBoundingClientRect().bottom - cur) - 8);
    }
    function tick() {
      raf = 0; if (!chart) return;
      cur = Math.min(Math.min(window.scrollY, window.innerHeight) * 0.22, room);
      chart.style.transform = 'translate3d(0,' + cur.toFixed(1) + 'px,0)';
    }
    measure();
    window.addEventListener('load', function () { measure(); tick(); });
    window.addEventListener('resize', function () { measure(); if (!raf) raf = requestAnimationFrame(tick); });
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

TG_CSS = (
    # the pictures larger (owner, 20 Oct 2026, from the preview), in their own column so they never meet the
    # words; the column narrows on a narrow card and on a phone the picture goes above the words, full width
    "html body .tg-v2 .tg-ep{container-type:inline-size}"
    "html body .tg-v2 .tg-ep-link{grid-template-columns:15rem minmax(0,1fr);column-gap:1.4rem}"
    "@container (max-width:36rem){html body .tg-v2 .tg-ep-link{grid-template-columns:12rem minmax(0,1fr);column-gap:1.1rem}}"
    "@container (max-width:30rem){html body .tg-v2 .tg-ep-link{grid-template-columns:minmax(0,1fr)}"
    "html body .tg-v2 .tg-thumb{grid-row:auto;grid-column:1/-1;margin-bottom:1rem}html body .tg-v2 .tg-ep p{grid-column:1/-1;margin-top:0}}"
    # grey and dimmed until the pointer is on the card (on a touch screen, while it is mid-screen), then in colour
    "html body .tg-v2 .tg-thumb{border-radius:8px}"
    "html body .tg-v2 .tg-thumb img{opacity:1;filter:grayscale(1) brightness(.68);transition:filter .5s var(--ease),transform .9s var(--ease)}"
    "html body .tg-v2 .tg-ep:is(:hover,:focus-within,.v4-lit) .tg-thumb img{filter:none;transform:scale(1.04)}"
    # reading text at 16 px, the titles a step larger
    "html body .tg-v2 .tg-ep p{font-size:1rem;line-height:1.65}"
    "html body .tg-v2 .tg-ep h2{font-size:1.12rem;line-height:1.35}"
    "@media (prefers-reduced-motion:reduce){html body .tg-v2 .tg-ep .tg-thumb img{transform:none}}"
    # on a phone the chart draws at about half its size, so its words were about 5 px: larger in the drawing
    "@media (max-width:600px){html body .dk.v4-tg-log :is(.sub,.val){font-size:21px}}"
)
TG_JS = r"""(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EASE = 'cubic-bezier(.2,.8,.2,1)';
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    var list = document.querySelector('.tg-list'); if (!list) return;
    /* a touch screen has no pointer to rest on a card: the card mid-screen shows its picture in colour */
    if (window.matchMedia && matchMedia('(hover: none)').matches && window.IntersectionObserver) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { e.target.classList.toggle('v4-lit', e.isIntersecting); });
      }, { rootMargin: '-40% 0px -40% 0px' });
      list.querySelectorAll('.tg-ep').forEach(function (li) { io.observe(li); });
    }
    if (reduce || !list.animate) return;
    /* sorting (the live tags-sort.js reorders the cards): each card on screen glides from where it was to
       where it is now, on top of its own rise; one from far away fades in on its way */
    var first = null;
    document.addEventListener('click', function (e) {
      if (!e.target.closest || !e.target.closest('.tg-sort button')) return;
      first = new Map();
      list.querySelectorAll('.tg-ep').forEach(function (li) { first.set(li, li.getBoundingClientRect()); });
      requestAnimationFrame(glide);
    }, true);
    function glide() {
      var f = first, vh = window.innerHeight, k = 0; first = null; if (!f) return;
      list.querySelectorAll('.tg-ep').forEach(function (li) {
        var o = f.get(li), r = li.getBoundingClientRect();
        if (!o || r.bottom < -80 || r.top > vh + 80) return;
        var dx = o.left - r.left, dy = o.top - r.top, far = Math.abs(dy) > vh * 0.9;
        if (Math.abs(dx) < 1 && Math.abs(dy) < 1) return;
        if (far) dy = (dy < 0 ? -1 : 1) * vh * 0.35;
        if (li.v4g) li.v4g.cancel();
        var kf = { transform: ['translate(' + dx.toFixed(1) + 'px,' + dy.toFixed(1) + 'px)', 'translate(0,0)'] };
        if (far) kf.opacity = [0, 1];
        li.v4g = li.animate(kf, { duration: 720, delay: Math.min(k++, 8) * 28, easing: EASE, fill: 'backwards', composite: 'add' });
      });
    }
  });
})();"""

TG_HUB_CSS = (
    # the topics rise in as they come into view (TG_HUB_JS), their trend lines drawing left to right after them
    "html.v4-tgh .tg-cloud .tg-tile:not(.v4-in){opacity:0}"
    # on the pointer the trend line glows and draws again, its last point grows
    "html body[data-v2=\"tg\"] .tg-tile .tg-spark{transition:filter .4s var(--ease)}"
    "html body[data-v2=\"tg\"] .tg-tile:is(:hover,:focus-visible) .tg-spark{filter:drop-shadow(0 0 4px rgba(255,117,23,.55))}"
    "html body[data-v2=\"tg\"] .tg-tile .tg-sp-d{transform-box:fill-box;transform-origin:50% 50%;transition:transform .4s var(--ease)}"
    "html body[data-v2=\"tg\"] .tg-tile:is(:hover,:focus-visible) .tg-sp-d{transform:scale(1.7)}"
    "#tgNone{transition:opacity .4s var(--ease)}"
)
TG_HUB_JS = r"""(function () {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!window.IntersectionObserver || !document.documentElement.animate) return;
  var html = document.documentElement, EASE = 'cubic-bezier(.2,.8,.2,1)';
  html.classList.add('v4-tgh');
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  var WIPE = ['inset(-6px 100% -6px 0)', 'inset(-6px -6px -6px 0)'];
  function draw(t, delay, ms) {
    var sp = t.querySelector('.tg-spark'); if (!sp) return;
    if (sp.v4d) sp.v4d.cancel();
    sp.v4d = sp.animate({ clipPath: WIPE }, { duration: ms, delay: delay, easing: EASE, fill: 'backwards' });
  }
  ready(function () {
    var cloud = document.getElementById('tgCloud');
    if (!cloud) { html.classList.remove('v4-tgh'); return; }
    var tiles = [].slice.call(cloud.querySelectorAll('.tg-tile'));
    function show(t, i) {
      t.classList.add('v4-in');
      t.animate({ opacity: [0, 1], transform: ['translateY(18px)', 'none'] }, { duration: 650, delay: i * 30, easing: EASE, fill: 'backwards' });
      draw(t, i * 30 + 240, 1000);
    }
    /* each topic rises in as it comes into view, a row at a time */
    var io = new IntersectionObserver(function (es) {
      var k = 0;
      es.filter(function (e) { return e.isIntersecting; })
        .sort(function (a, b) { return tiles.indexOf(a.target) - tiles.indexOf(b.target); })
        .forEach(function (e) { io.unobserve(e.target); if (!e.target.classList.contains('v4-in')) show(e.target, Math.min(k++, 10)); });
    }, { rootMargin: '0px 0px -6% 0px' });
    tiles.forEach(function (t) { io.observe(t); });
    window.addEventListener('beforeprint', function () { tiles.forEach(function (t) { t.classList.add('v4-in'); }); });
    /* the pointer on a topic draws its trend line again */
    tiles.forEach(function (t) {
      t.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse' && t.classList.contains('v4-in')) draw(t, 0, 800); });
    });
    /* the topic search (its own script hides what does not match): the topics left glide to their new
       places and those that come back rise in, instead of the grid jumping */
    var find = document.getElementById('tgFind'), none = document.getElementById('tgNone');
    if (!find) return;
    document.addEventListener('input', function (e) {
      if (e.target !== find) return;
      var f = new Map(), wasNone = none && !none.hidden;
      tiles.forEach(function (t) { if (!t.hidden) f.set(t, t.getBoundingClientRect()); });
      requestAnimationFrame(function () {
        var k = 0;
        tiles.forEach(function (t) {
          if (t.hidden) return;
          var o = f.get(t);
          if (t.v4g) t.v4g.cancel();
          if (!o) {
            t.classList.add('v4-in');
            t.v4g = t.animate({ opacity: [0, 1], transform: ['scale(.94)', 'none'] }, { duration: 460, delay: Math.min(k++, 10) * 25, easing: EASE, fill: 'backwards' });
            return;
          }
          var r = t.getBoundingClientRect(), dx = o.left - r.left, dy = o.top - r.top;
          if (Math.abs(dx) < 1 && Math.abs(dy) < 1) return;
          t.v4g = t.animate({ transform: ['translate(' + dx.toFixed(1) + 'px,' + dy.toFixed(1) + 'px)', 'none'] }, { duration: 560, easing: EASE });
        });
        if (none && !none.hidden && !wasNone) none.animate({ opacity: [0, 1], transform: ['translateY(8px)', 'none'] }, { duration: 420, easing: EASE });
      });
    }, true);
  });
})();"""

ABOUT_CSS = (
    # the opening's three figures large and solid, as on the podcast page (ABOUT_JS counts them up once)
    "html body .kit-hero .kit-stats{gap:var(--sp-3) clamp(2.2rem,5vw,4rem)}"
    "html body .kit-hero .kit-stat b{font-family:var(--font-display);font-weight:700;font-size:clamp(2rem,4.2vw,3.25rem);line-height:1;"
    "letter-spacing:-.02em;font-variant-numeric:tabular-nums}"
    "html body .kit-hero .kit-stat span{color:var(--gray-light);margin-top:.55rem}"
    # (while counting, the figure is a span inside it: it keeps the figure's look, not the label's)
    "html body .kit-hero .kit-stat b>span{display:inline;margin:0;font:inherit;color:inherit;letter-spacing:inherit;text-transform:none}"
    "html body .kit-hero .kit-stat b>.v4-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}"
    # the origin story: its words alone in the grid, the flight under them across the page
    "html body .v2-origin-grid{grid-template-columns:minmax(0,1fr);max-width:46rem}"
    # the flight, as the live About page draws it (about.html's own rules, the steps at 16 px)
    ".v2-origin .ab2-flight{margin:clamp(2.5rem,6vw,4.5rem) 0 0}"
    ".ab2-track{display:block;width:100%;height:auto;overflow:visible}"
    ".ab2-track path,.ab2-track rect,.ab2-track circle{fill:none;vector-effect:non-scaling-stroke}"
    ".ab2-alt path{stroke:var(--line);stroke-dasharray:2 8}"
    ".ab2-ridge{stroke:var(--edge-hi);stroke-width:1.2}"
    ".ab2-track .ab2-ridge-fill{fill:var(--card);stroke:none;opacity:.6}"
    ".ab2-line{stroke:var(--orange);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}"
    ".ab2-future{stroke:var(--orange);stroke-width:1.4;stroke-dasharray:3 7;opacity:.55}"
    ".ab2-drop{stroke:var(--edge);stroke-dasharray:2 5}"
    ".ab2-track .ab2-mark{fill:var(--bg);stroke:var(--orange);stroke-width:1.6}"
    ".ab2-wing path,.ab2-wing circle{stroke:var(--white);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}"
    ".ab2-track .ab2-wing circle{fill:var(--white)}"
    ".ab2-log{list-style:none;margin:1.4rem 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(1.2rem,3vw,2.5rem)}"
    ".ab2-log li{border-top:1px solid;border-image:linear-gradient(90deg,var(--orange),var(--line) 45%,transparent) 1;padding-top:1rem}"
    ".ab2-tag{display:block;font-family:var(--font-display);font-weight:700;font-size:var(--fs-h4);color:var(--orange);margin-bottom:.45rem}"
    ".ab2-log p{color:var(--gray-light);font-size:1rem;line-height:1.65;margin:0;max-width:30rem}"
    "@media (max-width:600px){.ab2-log{grid-template-columns:1fr;gap:1.4rem}}"
    # flown once when it comes into view: the line draws, each waypoint and its step arrive as the line reaches them
    "html.v4-fly .ab2-line{stroke-dasharray:var(--L,none);stroke-dashoffset:0;transition:stroke-dashoffset 2.6s cubic-bezier(.45,0,.2,1) .2s}"
    "html.v4-fly :is(.ab2-way,.ab2-wing,.ab2-future){transition:opacity .5s var(--ease)}"
    "html.v4-fly .ab2-way{transition-delay:var(--d)}html.v4-fly :is(.ab2-wing,.ab2-future){transition-delay:2.6s}"
    "html.v4-fly .ab2-log li{transition:opacity .7s var(--ease),transform .7s var(--ease)}"
    "html.v4-fly .ab2-log li:nth-child(1){transition-delay:.3s}html.v4-fly .ab2-log li:nth-child(2){transition-delay:.95s}"
    "html.v4-fly .ab2-log li:nth-child(3){transition-delay:1.6s}"
    "html.v4-fly .ab2-flight:not(.in) .ab2-line{stroke-dashoffset:var(--L,0)}"
    "html.v4-fly .ab2-flight:not(.in) :is(.ab2-way,.ab2-wing,.ab2-future){opacity:0}"
    "html.v4-fly .ab2-flight:not(.in) .ab2-log li{opacity:0;transform:translateY(12px)}"
    # the promises' words at 16 px (reading text)
    "html body .v2-promise p{font-size:1rem;line-height:1.65}"
    # Navigate, Aviate, Communicate: giant rows, pure type; with motion each fills white as it reaches the
    # middle of the screen (ABOUT_JS), outlined until then
    "html body .v4-nac{list-style:none;margin:var(--sp-5) 0 0;padding:0}"
    "html body .v4-nac li{display:grid;grid-template-columns:clamp(2.5rem,5vw,4rem) minmax(0,1fr);align-items:center;"
    "padding:clamp(.6rem,1.4vw,1rem) 0;border-top:1px solid var(--line)}"
    "html body .v4-nac li:last-child{border-bottom:1px solid var(--line)}"
    "html body .v4-nac small{font-family:var(--font-display);font-weight:600;font-size:.9rem;letter-spacing:.1em;color:var(--orange)}"
    "html body .v4-nac b{font-family:var(--font-display);font-weight:800;font-size:clamp(2.2rem,8vw,7.4rem);line-height:1;"
    "letter-spacing:-.03em;color:var(--white)}"
    "html.v4-nacm .v4-nac b{color:transparent;-webkit-text-stroke:1px var(--edge-hi);"
    "transition:color .6s var(--ease),-webkit-text-stroke-color .6s var(--ease)}"
    "html.v4-nacm .v4-nac small{color:var(--gray);transition:color .6s var(--ease)}"
    "html.v4-nacm .v4-nac li.on b{color:var(--white);-webkit-text-stroke-color:transparent}"
    "html.v4-nacm .v4-nac li.on small{color:var(--orange)}"
    # the trips lean towards the mouse, a soft light where it is (as the library's tiles)
    "html.v4-tilt .v2-tours .kit-card-media{position:relative;transform:perspective(800px) translateY(var(--ty,0px)) "
    "rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .6s var(--ease)}"
    "html.v4-tilt .v2-tours .kit-card:is(:hover,:focus-visible) .kit-card-media{--ty:-4px;transition:transform .18s var(--ease)}"
    "html.v4-tilt .v2-tours .kit-card-media::after{content:\"\";position:absolute;inset:0;pointer-events:none;opacity:0;"
    "background:radial-gradient(60% 60% at var(--mx,50%) var(--my,50%),rgba(246,244,244,.14),transparent 70%);transition:opacity .4s var(--ease)}"
    "html.v4-tilt .v2-tours .kit-card:hover .kit-card-media::after{opacity:1}"
)
ABOUT_JS = r"""(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var html = document.documentElement;
  if (reduce) return;
  if (window.IntersectionObserver) html.classList.add('v4-fly', 'v4-nacm');
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    /* the opening's figures count up once, the real figure kept for screen readers and at the end */
    document.querySelectorAll('.kit-hero .kit-stat b').forEach(function (b, k) {
      var real = b.textContent, m = real.match(/^(\d+)(\D*)$/); if (!m) return;
      var n = +m[1], w = b.getBoundingClientRect().width, show = document.createElement('span'), t0 = 0;
      show.setAttribute('aria-hidden', 'true');
      b.textContent = ''; b.appendChild(show);
      var sr = document.createElement('span'); sr.className = 'v4-sr'; sr.textContent = real; b.appendChild(sr);
      b.style.display = 'inline-block'; b.style.minWidth = w + 'px';
      function step(now) {
        if (!t0) t0 = now;
        var t = Math.min(1, Math.max(0, (now - t0 - 250 - k * 120) / 1400)), e = 1 - Math.pow(1 - t, 3);
        show.textContent = Math.round(n * e) + m[2];
        if (t < 1) requestAnimationFrame(step); else { b.textContent = real; b.style.display = b.style.minWidth = ''; }
      }
      requestAnimationFrame(step);
    });
    /* the flight is flown once, when it first comes into view; its line is measured on screen so the drawing
       ends exactly at the tip (the live page's way) */
    var fl = document.querySelector('.ab2-flight');
    if (fl && window.IntersectionObserver) {
      var line = fl.querySelector('.ab2-line'), art = fl.querySelector('svg');
      var measure = function () {
        if (!line.getTotalLength) return;
        line.style.setProperty('--L', (Math.ceil(line.getTotalLength() * art.getBoundingClientRect().width / 1200) + 2) + 'px');
      };
      measure();
      var io = new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) { measure(); fl.classList.add('in'); io.disconnect(); }
      }, { threshold: 0.35 });
      io.observe(fl);
      window.addEventListener('beforeprint', function () { fl.classList.add('in'); });
    }
    /* Navigate, Aviate, Communicate: each fills as it reaches the middle of the screen, in order */
    var rows = [].slice.call(document.querySelectorAll('.v4-nac li')), raf = 0;
    function tick() {
      raf = 0; var mid = window.innerHeight * 0.62;
      rows.forEach(function (li) { var r = li.getBoundingClientRect(); li.classList.toggle('on', r.top + r.height / 2 < mid); });
    }
    if (rows.length) {
      window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
      window.addEventListener('beforeprint', function () { rows.forEach(function (li) { li.classList.add('on'); }); });
      tick();
    }
    /* the trips lean towards the mouse, with a soft light on them */
    if (!(window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches)) return;
    html.classList.add('v4-tilt');
    document.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      var c = e.target.closest && e.target.closest('.v2-tours .kit-card'); if (!c) return;
      var s = c.querySelector('.kit-card-media'); if (!s) return;
      var r = s.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      if (x < 0 || x > 1 || y < 0 || y > 1) return;
      s.style.setProperty('--ry', ((x - 0.5) * 10).toFixed(2) + 'deg');
      s.style.setProperty('--rx', ((0.5 - y) * 8).toFixed(2) + 'deg');
      s.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
      s.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    }, { passive: true });
    document.addEventListener('pointerout', function (e) {
      var c = e.target.closest && e.target.closest('.v2-tours .kit-card');
      if (!c || (e.relatedTarget && c.contains(e.relatedTarget))) return;
      var s = c.querySelector('.kit-card-media'); if (s) { s.style.removeProperty('--rx'); s.style.removeProperty('--ry'); }
    });
  });
})();"""
FLIGHT = ("<!--v4p:flight-->", "<!--/v4p:flight-->")
NAC = ("<!--v4p:nac-->", "<!--/v4p:nac-->")


def about_markup(html):
    """The About page's origin story as the live page flies it, and its three words as giant rows. The drawing
    is read from the live about.html each run (it stops if it is not there once); the three steps keep the v4
    page's own words. Both are written between marks, so a second run writes the same bytes."""
    import html as H
    live = open(os.path.join(ROOT, "about.html"), encoding="utf-8").read()
    svg = re.findall(r'<svg class="ab2-track".*?</svg>', live, re.S)
    if len(svg) != 1:
        raise SystemExit("v4_polish: the live about.html's flight (svg.ab2-track) is not there once")
    m = re.search(r'\s*<ol class="kit-rows v2-log">(.*?)</ol>(\s*</div>)', html, re.S)
    if m:
        steps = re.findall(r'<li class="kit-row"><span class="kit-kicker">(.*?)</span><p>(.*?)</p></li>', m.group(1))
    else:
        mm = re.search(re.escape(FLIGHT[0]) + r".*?" + re.escape(FLIGHT[1]), html, re.S)
        if not mm:
            raise SystemExit("v4_polish: about.html: neither the story's steps nor the flight is there")
        steps = re.findall(r'<li><span class="ab2-tag">(.*?)</span><p>(.*?)</p></li>', mm.group(0))
    if len(steps) != 3:
        raise SystemExit("v4_polish: about.html: the story does not have three steps")
    block = (FLIGHT[0] + '\n    <div class="ab2-flight">\n      ' + svg[0] + '\n      <ol class="ab2-log">\n'
             + "".join('        <li><span class="ab2-tag">%s</span><p>%s</p></li>\n' % s for s in steps)
             + "      </ol>\n    </div>" + FLIGHT[1])
    if m:
        html = html[:m.start()] + m.group(2) + "\n    " + block + html[m.end():]
    else:
        html = re.sub(re.escape(FLIGHT[0]) + r".*?" + re.escape(FLIGHT[1]), lambda _: block, html, count=1, flags=re.S)
    old = re.search(r'<p class="v2-nac" aria-label="[^"]*">(.*?)</p>', html, re.S)
    mine = re.search(re.escape(NAC[0]) + r".*?" + re.escape(NAC[1]), html, re.S)
    words = (re.findall(r"<span>(.*?)</span>", old.group(1)) if old else
             re.findall(r"<b>(.*?)</b>", mine.group(0)) if mine else [])
    if len(words) != 3:
        raise SystemExit("v4_polish: about.html: Navigate, Aviate, Communicate is not there")
    nac = (NAC[0] + '<ol class="v4-nac" aria-label="%s">' % H.escape(", ".join(H.unescape(w) for w in words))
           + "".join('<li><small aria-hidden="true">%02d</small><b>%s</b></li>' % (i + 1, w) for i, w in enumerate(words))
           + "</ol>" + NAC[1])
    if old:
        html = html[:old.start()] + nac + html[old.end():]
    else:
        html = re.sub(re.escape(NAC[0]) + r".*?" + re.escape(NAC[1]), lambda _: nac, html, count=1, flags=re.S)
    return html


MISSION_CSS = (
    # the photo at the top comes closer as the page scrolls (its own slow drift kept, on the picture inside)
    "@keyframes v4p-near{to{transform:scale(1.12) translateY(2%)}}"
    "@supports (animation-timeline: scroll()){@media (prefers-reduced-motion:no-preference){"
    "html body .v2-page-hero .v4-bg{animation:v4p-near linear both;animation-timeline:scroll(root);animation-range:0 100vh}}}"
    # On this page follows the reading: the section being read lit, the ones read marked, the line beside the
    # list filling orange down to where the reader is (MISSION_JS)
    "html.v4-toc .pol-toc::after{content:\"\";position:absolute;left:-2px;top:0;width:2px;height:var(--f,0px);"
    "background:var(--orange);box-shadow:0 0 10px rgba(255,117,23,.5)}"
    "html.v4-toc .pol-toc a{transition:color .3s var(--ease)}"
    "html.v4-toc .pol-toc a.done{color:var(--gray-light)}"
    "html.v4-toc .pol-toc a.on{color:var(--white)}"
    # the verse's translation, a word at a time as it crosses the screen (as the podcast's pull quote)
    "html.v4-vw .pol-verse-en .v4w{color:var(--edge-hi);transition:color .45s var(--ease)}"
    "html.v4-vw .pol-verse-en .v4w.on{color:var(--white)}"
)
MISSION_JS = r"""(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var html = document.documentElement;
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    var toc = document.querySelector('.pol-toc'), body = document.querySelector('.pol-body');
    var links = toc ? [].slice.call(toc.querySelectorAll('a[href^="#"]')) : [];
    var heads = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
    if (heads.some(function (h) { return !h; })) links = [];
    if (links.length && body) {
      html.classList.add('v4-toc');
      if (getComputedStyle(toc).position === 'static') toc.style.position = 'relative';
    }
    /* the verse's translation, a word at a time */
    var q = reduce ? null : document.querySelector('.pol-verse-en'), words = [];
    if (q && !q.querySelector('.v4w') && !q.children.length) {
      var parts = q.textContent.split(/\s+/).filter(Boolean);
      q.textContent = '';
      parts.forEach(function (w, i) {
        var sp = document.createElement('span'); sp.className = 'v4w'; sp.textContent = w;
        q.appendChild(sp); if (i < parts.length - 1) q.appendChild(document.createTextNode(' '));
        words.push(sp);
      });
      html.classList.add('v4-vw');
    }
    var raf = 0, lit = -1, cur = -2;
    function tick() {
      raf = 0;
      var vh = window.innerHeight;
      if (words.length) {
        var qb = q.getBoundingClientRect();
        var t = Math.min(1, Math.max(0, (vh * 0.86 - qb.top) / (qb.height + vh * 0.36)));
        var n = Math.round(t * words.length);
        if (n !== lit) { for (var j = 0; j < words.length; j++) words[j].classList.toggle('on', j < n); lit = n; }
      }
      if (links.length && body) {
        var line = vh * 0.35, i = -1, tops = heads.map(function (h) { return h.getBoundingClientRect().top; });
        tops.forEach(function (tp, k) { if (tp <= line) i = k; });
        var bb = body.getBoundingClientRect(), f;
        if (i < 0) {
          f = links[0].offsetTop * Math.min(1, Math.max(0, (line - bb.top) / Math.max(1, tops[0] - bb.top)));
        } else {
          var end = i + 1 < tops.length ? tops[i + 1] : bb.bottom;
          var fr = Math.min(1, Math.max(0, (line - tops[i]) / Math.max(1, end - tops[i])));
          var a = links[i], nx = links[i + 1];
          f = a.offsetTop + fr * ((nx ? nx.offsetTop : toc.offsetHeight) - a.offsetTop);
        }
        toc.style.setProperty('--f', f.toFixed(1) + 'px');
        if (i !== cur) {
          links.forEach(function (a, k) {
            a.classList.toggle('on', k === i); a.classList.toggle('done', k < i);
            if (k === i) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
          });
          cur = i;
        }
      }
    }
    window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
    window.addEventListener('resize', function () { if (!raf) raf = requestAnimationFrame(tick); });
    tick();
  });
})();"""


HOME_CSS = (
    "html body .v2-home-hero .kit-kicker{text-shadow:0 1px 2px color-mix(in srgb,var(--bg) 85%,transparent),"
    "0 0 16px color-mix(in srgb,var(--bg) 75%,transparent)}"
    # B: the opening's figures (home_markup), large and solid as on the podcast and About pages
    ".v4-hfig{display:flex;flex-wrap:wrap;gap:var(--sp-3) clamp(2rem,5vw,4rem);margin:var(--sp-4) 0 0;padding:var(--sp-3) 0 0;"
    "border-top:1px solid color-mix(in srgb,var(--white) 18%,transparent);list-style:none}"
    ".v4-hfig b{display:block;font-family:var(--font-display);font-weight:700;font-size:clamp(2rem,4vw,3.1rem);line-height:1;"
    "color:var(--white);font-variant-numeric:tabular-nums;text-shadow:0 2px 18px color-mix(in srgb,var(--bg) 60%,transparent)}"
    ".v4-hfig b>span{display:inline}.v4-hfig .v4-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}"
    ".v4-hfig li>span{display:block;margin-top:.5rem;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gray-light)}"
    # B: every departure on one line of months (home_markup), drawing in as it comes into view
    ".v4-tl{margin:var(--sp-4) 0 var(--sp-5)}"
    ".v4-tl ol{list-style:none;margin:0 0 12px;padding:0;display:grid;gap:10px}"
    ".v4-tl li{position:relative;height:28px}"
    ".v4-tl li b{position:absolute;top:0;height:28px;min-width:6px;border-radius:4px;background:var(--orange);transform-origin:0 50%}"
    ".v4-tl li.is-plan b{background:transparent;border:1px dashed color-mix(in srgb,var(--orange) 70%,transparent)}"
    ".v4-tl li span{position:absolute;top:5px;font-size:.8rem;color:var(--gray-light);white-space:nowrap}"
    ".v4-tl li span em{font-style:normal;color:var(--gray);margin-left:.4rem}"
    ".v4-tl .v4-tl-ax{display:grid;border-top:1px solid var(--line);font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gray)}"
    ".v4-tl .v4-tl-ax span{padding:.5rem 0 0 .35rem;border-left:1px solid var(--line);white-space:nowrap;overflow:hidden}"
    # on a phone the dates go under each name (the axis has no room for the years) and the three figures keep one row
    "@media (max-width:760px){.v4-tl li{height:36px}.v4-tl li b{top:4px}.v4-tl li span{top:1px;font-size:.8rem;line-height:1.3}"
    ".v4-tl li span em{display:block;margin:0;font-size:.72rem}.v4-tl .v4-tl-ax{font-size:.6rem;letter-spacing:.04em}"
    ".v4-tl .v4-tl-ax span{padding-left:.15rem}.v4-tl .v4-tl-ax i{display:none}"
    ".v4-hfig{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:var(--sp-3) 1.5rem}"
    ".v4-hfig li>span{font-size:.64rem;letter-spacing:.1em;line-height:1.35}}"
    "html.v4-tld .v4-tl li b{transform:scaleX(0);transition:transform .9s var(--ease)}"
    "html.v4-tld .v4-tl li span{opacity:0;transition:opacity .6s var(--ease)}"
    "html.v4-tld .v4-tl.is-in li b{transform:none}html.v4-tld .v4-tl.is-in li span{opacity:1}"
    # A: the episode cards lean towards the mouse with a soft light where it is
    "html.v4-tilt .v2-rail .ep-card .ep-art{transform:perspective(800px) translateY(var(--ty,0px)) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));"
    "transition:transform .6s var(--ease)}"
    "html.v4-tilt .v2-rail .ep-card:is(:hover,:focus-visible) .ep-art{--ty:-4px;transition:transform .18s var(--ease)}"
    "html.v4-tilt .v2-rail .ep-card .ep-art::after{content:\"\";position:absolute;inset:0;pointer-events:none;opacity:0;z-index:3;"
    "background:radial-gradient(60% 60% at var(--mx,50%) var(--my,50%),color-mix(in srgb,var(--white) 14%,transparent),transparent 70%);"
    "transition:opacity .4s var(--ease)}"
    "html.v4-tilt .v2-rail .ep-card:hover .ep-art::after{opacity:1}"
)
HOME_JS = r"""(function () {
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches, html = document.documentElement;
  if (!still && window.IntersectionObserver) html.classList.add('v4-tld');
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    /* B. the opening's figures count up once (the real figure kept for screen readers, its width held) */
    if (!still) document.querySelectorAll('.v4-hfig b').forEach(function (b, k) {
      var real = b.textContent, m = real.match(/^(\d+)(\D*)$/); if (!m) return;
      var n = +m[1], w = b.getBoundingClientRect().width, show = document.createElement('span'), t0 = 0;
      show.setAttribute('aria-hidden', 'true'); b.textContent = ''; b.appendChild(show);
      var sr = document.createElement('span'); sr.className = 'v4-sr'; sr.textContent = real; b.appendChild(sr);
      b.style.display = 'inline-block'; b.style.minWidth = w + 'px';
      (function step(now) {
        if (!t0) t0 = now;
        var t = Math.min(1, Math.max(0, (now - t0 - 450 - k * 120) / 1400)), e = 1 - Math.pow(1 - t, 3);
        show.textContent = Math.round(n * e) + m[2];
        if (t < 1) requestAnimationFrame(step); else { b.textContent = real; b.style.display = b.style.minWidth = ''; }
      })(performance.now());
    });
    /* B. the departures' line draws in once, as it comes into view */
    var tl = document.querySelector('.v4-tl');
    if (tl && html.classList.contains('v4-tld')) {
      var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { tl.classList.add('is-in'); io.disconnect(); } }, { threshold: 0.3 });
      io.observe(tl);
      tl.querySelectorAll('li').forEach(function (li, k) { var b = li.querySelector('b'), s = li.querySelector('span');
        if (b) b.style.transitionDelay = (k * 0.12) + 's'; if (s) s.style.transitionDelay = (0.4 + k * 0.12) + 's'; });
      window.addEventListener('beforeprint', function () { tl.classList.add('is-in'); });
    }
    /* A. each held photograph comes slowly closer as the visitor reads about its trip */
    var trips = [].slice.call(document.querySelectorAll('.v2-fb-step:not(.v2-fb-intro)'));
    var shots = [].slice.call(document.querySelectorAll('.v2-fb-shot picture')), raf = 0;
    if (!still && trips.length && shots.length) {
      var tick = function () {
        raf = 0;
        var mid = window.innerHeight * 0.5;
        trips.forEach(function (t, k) {
          if (!shots[k]) return;
          var r = t.getBoundingClientRect(), u = Math.min(1, Math.max(0, (mid - r.top) / Math.max(1, r.height)));
          shots[k].style.transform = 'scale(' + (1 + 0.06 * u).toFixed(4) + ')';
        });
      };
      window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
      window.addEventListener('resize', function () { if (!raf) raf = requestAnimationFrame(tick); });
      tick();
    }
    /* A. the episode cards lean towards the mouse, with a soft light on them */
    if (still || !(window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches)) return;
    html.classList.add('v4-tilt');
    document.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      var c = e.target.closest && e.target.closest('.v2-rail .ep-card'); if (!c) return;
      var s = c.querySelector('.ep-art'); if (!s) return;
      var r = s.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      if (x < 0 || x > 1 || y < 0 || y > 1) return;
      s.style.setProperty('--ry', ((x - 0.5) * 10).toFixed(2) + 'deg'); s.style.setProperty('--rx', ((0.5 - y) * 8).toFixed(2) + 'deg');
      s.style.setProperty('--mx', (x * 100).toFixed(1) + '%'); s.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    }, { passive: true });
    document.addEventListener('pointerout', function (e) {
      var c = e.target.closest && e.target.closest('.v2-rail .ep-card');
      if (!c || (e.relatedTarget && c.contains(e.relatedTarget))) return;
      var s = c.querySelector('.ep-art'); if (s) { s.style.removeProperty('--rx'); s.style.removeProperty('--ry'); }
    });
  });
})();"""
HFIG = ("<!--v4p:fig-->", "<!--/v4p:fig-->")
TL = ("<!--v4p:tl-->", "<!--/v4p:tl-->")
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def home_markup(html):
    """B on the home page: the opening's figures and every departure on one line of months. Both are read from the
    site at each build (the feed's episode count, the podcast page's countries, the departures listed on this page)
    and written between marks, so a second run writes the same bytes."""
    import calendar
    import html as H
    pod = open(os.path.join(V4, "podcast.html"), encoding="utf-8").read()
    mc = re.search(r'<b>(\d+)</b><span>Countries', pod)
    deps = re.findall(r'<a class="v2-dep" href="[^"]*" data-place="([a-z]+)" data-month="(\d{4})-(\d{2})">'
                      r'<span class="v2-dep-trip"><b>([^<]+)</b>(?: <em>([^<]+)</em>)?</span><span data-l="Dates">([^<]+)</span>', html)
    if not mc or not deps:
        raise SystemExit("v4_polish: index.html: the figures' or the departures' source is not there")
    figs = [(str(feed_count()), "Conversations"), (mc.group(1), "Countries listening"), (str(len({d[0] for d in deps})), "Destinations")]
    fig = (HFIG[0] + '<ul class="v4-hfig">' + "".join('<li><b>%s</b><span>%s</span></li>' % f for f in figs) + "</ul>" + HFIG[1])
    html = re.sub(re.escape(HFIG[0]) + r".*?" + re.escape(HFIG[1]), "", html, flags=re.S)
    m = re.search(r'(<header class="kit-hero v2-home-hero".*?<div class="kit-actions">.*?</div>)', html, re.S)
    if not m:
        raise SystemExit("v4_polish: index.html: the opening's actions are not there")
    html = html[:m.end()] + fig + html[m.end():]
    # the line of months: from the first departure's month to the last's
    rows = []
    for place, yy, mm, name, tour, dates in deps:
        y, mo = int(yy), int(mm)
        dm = re.match(r"(\d+) to (\d+) [A-Z][a-z]{2} \d{4}$", dates)
        if dm:
            a, b = int(dm.group(1)), int(dm.group(2)); plan = False
        else:
            a, b = 1, calendar.monthrange(y, mo)[1]; plan = True
        rows.append((y * 12 + mo - 1, a, b, plan, name + (", " + tour.lower() if tour else ""), H.unescape(dates)))
    m0 = min(r[0] for r in rows); m1 = max(r[0] for r in rows); n = m1 - m0 + 1
    def pos(mi, day):
        y, mo = divmod(mi, 12)
        return 100.0 * ((mi - m0) + (day - 1) / calendar.monthrange(y, mo + 1)[1]) / n
    lis = []
    for mi, a, b, plan, label, dates in rows:
        x0 = pos(mi, a); x1 = pos(mi, b + 1); right = x1 > 72
        lab = ('<span style="%s">%s<em>%s</em></span>' % (
            ("right:calc(%.2f%% + 10px)" % (100 - x0)) if right else ("left:calc(%.2f%% + 10px)" % x1), H.escape(label), H.escape(dates)))
        lis.append('<li%s><b style="left:%.2f%%;width:%.2f%%"></b>%s</li>' % (' class="is-plan"' if plan else "", x0, x1 - x0, lab))
    ax = []
    for mi in range(m0, m1 + 1):
        y, mo = divmod(mi, 12)
        ax.append("<span>%s%s</span>" % (MONTHS[mo], "<i> %d</i>" % y if mi == m0 or mo == 0 else ""))
    tl = (TL[0] + '<div class="v4-tl" aria-hidden="true"><ol>' + "".join(lis) + '</ol><div class="v4-tl-ax" style="grid-template-columns:repeat(%d,1fr)">' % n
          + "".join(ax) + "</div></div>" + TL[1])
    html = re.sub(re.escape(TL[0]) + r".*?" + re.escape(TL[1]) + "\n  ", "", html, flags=re.S)
    anchor = '<p class="v2-found" data-found'
    if html.count(anchor) != 1:
        raise SystemExit("v4_polish: index.html: the departures' place is not there")
    return html.replace(anchor, tl + "\n  " + anchor, 1)

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
PAGES["tags.html"], SCRIPTS["tags.html"] = TG_HUB_CSS, TG_HUB_JS
PAGES["index.html"], SCRIPTS["index.html"] = HOME_CSS, HOME_JS
PAGES["about.html"], SCRIPTS["about.html"] = ABOUT_CSS, ABOUT_JS
PAGES["mission.html"], SCRIPTS["mission.html"] = MISSION_CSS, MISSION_JS
for _f in sorted(os.listdir(os.path.join(V4, "tags"))):
    if _f.endswith(".html"):
        PAGES["tags/" + _f], SCRIPTS["tags/" + _f] = TG_CSS, TG_JS


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


# (wrong, right) in the text of every v4 page that has it (the pages their own generators own are left to them)
TEXT_FIXES = [
    # the episode description lost its maker's name; the episode's own title gives it
    ("the innovative designer from .", "the innovative designer from AirDesign."),
    ("Took It\u2019s First Steps", "Took Its First Steps"),
]
# About's India card showed the home page's India photograph: no photograph twice on the site (owner, 21 Oct)
ABOUT_INDIA = ('<picture><source srcset="../../assets/images/himalayas-1.webp" type="image/webp"><img width="1600" height="1200" '
               'src="../../assets/images/himalayas-1.jpg" alt="Paraglider over snow-capped Himalayan peaks" loading="lazy"></picture>',
               '<picture><source srcset="../../assets/destinations/india/gallery/red-wing.webp" type="image/webp"><img width="1400" '
               'height="933" src="../../assets/destinations/india/gallery/red-wing.jpg" alt="A pilot on a red wing turning over steep snow" '
               'loading="lazy"></picture>')


def feed_count():
    """The episode count is the RSS feed's (owner, 21 Oct 2026: "whatever the RSS feed shows, it's the correct count"):
    the episodes in episode-meta.json that went out on the feed (a publish date); the YouTube-only videos have none."""
    import json
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    return sum(1 for e in meta if e.get("published"))


def words(n):
    ones = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
    tens = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
    if n < 20:
        return ones[n]
    if n < 100:
        return tens[n // 10] + ("" if n % 10 == 0 else " " + ones[n % 10])
    return str(n)


def episode_count(rel, html):
    """Pages that counted every episode page (93, with the YouTube-only videos) give the feed's count."""
    n = feed_count()
    if rel == "sitemap.html":
        html = re.sub(r"(13 series &middot; )\d+( episodes)", lambda m: m.group(1) + str(n) + m.group(2), html)
        html = re.sub(r'("sub": "13 series, )\d+( episodes")', lambda m: m.group(1) + str(n) + m.group(2), html)
    if rel == "mission.html":
        num = r"(?:Twenty|Thirty|Forty|Fifty|Sixty|Seventy|Eighty|Ninety)(?: (?:one|two|three|four|five|six|seven|eight|nine))?"
        html = re.sub(num + r" conversations( with designers| is a lot of ground)",
                      lambda m: words(n).capitalize() + " conversations" + m.group(1), html)
    return html


def transcripts(rel, html):
    """A topic page promised a full transcript for every conversation; its own answer below gives the count."""
    if rel == "tags.html":
        return html.replace(" Every episode carries a full transcript.</p>", "</p>")
    m = re.search(r"(\d+) conversations tagged [^,<]+, (\d+) of them with a complete transcript", html)
    if m and int(m.group(2)) < int(m.group(1)):
        html = html.replace('<p class="kit-intro">%s conversations, every one with a full transcript.</p>' % m.group(1),
                            '<p class="kit-intro">%s conversations, %s with a full transcript.</p>' % (m.group(1), m.group(2)))
    return html


def corrections():
    import glob
    n = 0
    for p in glob.glob(os.path.join(V4, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, V4).replace(os.sep, "/")
        if rel.startswith(("samples/", "src/")) or re.match(r"(record-|expeditions)", rel):
            continue
        html = open(p, encoding="utf-8").read()
        # the page's own words only: the head (description, og:description) must stay the live page's (the switch-over checks it)
        cut = html.find("</head>") + 1 if "</head>" in html else 0
        body = html[cut:]
        for a, b in TEXT_FIXES:
            body = body.replace(a, b)
        out = html[:cut] + body
        if rel == "tags.html" or rel.startswith("tags/"):
            out = transcripts(rel, out)
        if rel == "about.html":
            out = out.replace(*ABOUT_INDIA)
        if rel in ("sitemap.html", "mission.html"):
            out = out[:cut] + episode_count(rel, out[cut:])
        if out != html:
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            n += 1
    print("v4_polish: corrections on %d pages" % n)


def main():
    corrections()
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
        if rel == "about.html":
            html = about_markup(html)
        if rel == "index.html":
            html = home_markup(html)
        if rel == "podcast.html" and POD_LOADER[1] not in html:
            if html.count(POD_LOADER[0]) != 1:
                raise SystemExit("v4_polish: podcast.html: the globe loader is not there once")
            html = html.replace(POD_LOADER[0], POD_LOADER[1])
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print("v4_polish: " + rel)


if __name__ == "__main__":
    main()
