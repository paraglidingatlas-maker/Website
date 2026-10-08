/* THE CLIMB INTO THE FOOTAGE (owner, 8 Oct 2026: "change the background
   gradually from black to white and then show the video ... I want to feel an
   immersive experience before reaching the video part of the page").
   Inlined by tools/v4_ux.py in the pages with a footage band (.v4-breather),
   each of which follows a stretch of sky (.v4-ascent): the page's dark lifts to
   the white of cloud as you scroll, the site's own cloud layers (the Kenya
   page's) pass at three depths, and the footage comes out of the white as the
   cloud thins; under it the page darkens again (src/v4-ux.css, "ascent").
   This sets two numbers as you scroll: --a on the sky, 0 as it comes up the
   screen to 1 as its end leaves the top; --e on the footage, 0 as its top
   comes up the screen, 1 as it reaches the top, on to 1.5. It loads the clouds as the sky comes
   near (a phone gets the 1000 px copies, img/clouds). Reduced motion: the
   clouds arrive where they rest, the footage stands half out of the cloud
   (the CSS's own values) and nothing moves. */
(function () {
  var d = document, w = window;
  var skies = [].slice.call(d.querySelectorAll(".v4-ascent"));
  if (!skies.length) return;
  var m = /^(.*\/prototypes\/v\d+\/)/.exec(location.pathname);
  var BASE = m ? m[1] : "/assets/v4/", LIVE = m ? m[1].replace(/prototypes\/v\d+\/$/, "") : "/";
  var mq = function (q) { return w.matchMedia && w.matchMedia(q).matches; };
  var still = mq("(prefers-reduced-motion: reduce)"), small = mq("(max-width: 820px)");
  var pairs = skies.map(function (s) {
    var n = s.nextElementSibling;
    return { s: s, f: n && n.classList.contains("v4-breather") ? n : null, ns: false, nf: false };
  });
  function clouds(s) {
    if (s.v4c) return;
    s.v4c = 1;
    [].forEach.call(s.querySelectorAll("[data-v4-cloud]"), function (c) {
      var k = c.getAttribute("data-v4-cloud");
      c.style.backgroundImage = "url('" + (small ? BASE + "img/clouds/cloud-" + k + "-s.webp"
                                                 : LIVE + "assets/destinations/kenya/clouds/cloud-" + k + ".webp") + "')";
    });
  }
  var queued = false;
  function paint() {
    queued = false;
    var vh = w.innerHeight;
    pairs.forEach(function (p) {
      if (!p.ns && !p.nf) return;
      var r = p.s.getBoundingClientRect();
      p.s.style.setProperty("--a", Math.min(1, Math.max(0, (vh - r.top) / (r.height + vh))).toFixed(4));
      if (p.f) p.f.style.setProperty("--e", Math.min(1.5, Math.max(0, (vh - p.f.getBoundingClientRect().top) / vh)).toFixed(4));
    });
  }
  function ask() { if (!queued) { queued = true; w.requestAnimationFrame(paint); } }
  if (!("IntersectionObserver" in w)) {
    pairs.forEach(function (p) { clouds(p.s); p.ns = true; });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        pairs.forEach(function (p) {
          if (p.s === e.target) { p.ns = e.isIntersecting; if (e.isIntersecting) clouds(p.s); }
          if (p.f === e.target) p.nf = e.isIntersecting;
        });
      });
      ask();
    }, { rootMargin: "0px 0px 60% 0px" });
    pairs.forEach(function (p) { io.observe(p.s); if (p.f) io.observe(p.f); });
  }
  if (still) return;
  w.addEventListener("scroll", ask, { passive: true });
  w.addEventListener("resize", ask, { passive: true });
  ask();
})();
