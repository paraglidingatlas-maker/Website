/* Designer F (Turnpoint), event landing pages, round 1: "The Season Opens Here".
   1. The arrival: the event's dates on the season line open, down the orange fan, into its own task line
      (the track grows out of the lit dates, the turnpoints drop into place, left to right). Once, about 1 s,
      transform and opacity only, only when the line is on screen at load; reduced motion and no JS: finished page.
   2. Films-only events (no v4-gallery.js on the page): the same line, one stop at a time, the glider flies the leg.
   3. A film stops when its stop closes (no sound from a hidden stop). */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  var main = d.querySelector(".ef"); if (!main) return;
  var mq = w.matchMedia ? w.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  function reduced() { return mq.matches; }
  var line = d.querySelector(".gf-line"), season = d.querySelector(".ef-season");
  var films = main.classList.contains("ef-films");

  /* ---------------------------------------------------------------- 2. films-only: one stop at a time */
  if (films && line) {
    root.classList.add("gf-js");
    var tps = [].slice.call(line.querySelectorAll(".gf-tp")), stops = [].slice.call(d.querySelectorAll(".ef-stop"));
    var glw = line.querySelector(".gf-glw"), glider = line.querySelector(".gf-glider"), N = stops.length, cur = -1, fl = null, bk = null;
    var body = d.querySelector(".gf-body");
    function pct(i) { return (i + 0.5) * 100 / N; }
    function fly(a, b) {
      line.style.setProperty("--open", b);
      if (reduced() || !glw.animate || a === b || a < 0) return;
      if (fl) fl.cancel(); if (bk) bk.cancel();
      var legs = Math.abs(b - a), dir = b > a ? 1 : -1, ms = Math.min(1000, 380 + 150 * legs);
      fl = glw.animate([{ transform: "translateX(" + pct(a) + "%)" }, { transform: "translateX(" + (pct(a) + pct(b)) / 2 + "%) translateY(" + (-Math.min(9, 5 + legs)) + "px)", offset: .5 }, { transform: "translateX(" + pct(b) + "%)" }], { duration: ms, easing: "cubic-bezier(.45,0,.25,1)" });
      bk = glider.animate([{ transform: "rotate(0)" }, { transform: "rotate(" + dir * 9 + "deg)", offset: .3 }, { transform: "rotate(" + dir * 4 + "deg)", offset: .72 }, { transform: "rotate(0)" }], { duration: ms, easing: "ease-in-out" });
    }
    function open(i, o) {
      o = o || {};
      if (i < 0 || i >= N || i === cur) return;
      var prev = cur; cur = i;
      stops.forEach(function (s, k) { s.classList.toggle("is-open", k === i); });
      tps.forEach(function (t, k) { t.classList.toggle("is-open", k === i); var a = t.querySelector("a"); if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      fly(prev, i);
      if (prev >= 0 && !reduced() && stops[i].animate) {
        var dir = i > prev ? 1 : -1;
        stops[i].animate([{ opacity: 0, transform: "translateX(" + dir * 18 + "px)" }, { opacity: 1, transform: "none" }], { duration: 380, easing: "cubic-bezier(.2,.8,.2,1)" });
      }
      if (o.scroll) {
        var top = body.getBoundingClientRect().top;
        if (top < 0) { var nh = parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 0; w.scrollTo(0, Math.max(0, w.scrollY + top - nh)); }
      }
      if (!o.keepHash) try { history.replaceState(null, "", location.pathname + location.search + "#" + stops[i].id); } catch (e) {}
    }
    var start = stops.findIndex ? stops.findIndex(function (s) { return s.classList.contains("is-open"); }) : 1;
    var h = location.hash.slice(1), hit = -1;
    stops.forEach(function (s, k) { if (s.id === h) hit = k; });
    stops.forEach(function (s) { s.classList.remove("is-open"); });
    open(hit >= 0 ? hit : Math.max(0, start), { keepHash: hit < 0 });
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest(".gf-tp a, .ef-films [data-go], .ef-have a[href^='#']");
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
      var id = (a.getAttribute("href") || "").slice(1), k = -1;
      stops.forEach(function (s, j) { if (s.id === id) k = j; });
      if (k < 0) return;
      e.preventDefault(); open(k, { scroll: true });
      if (a.closest(".ef-have")) { var nh = parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 0; w.scrollTo({ top: Math.max(0, w.scrollY + body.getBoundingClientRect().top - nh), behavior: reduced() ? "auto" : "smooth" }); }
    });
    w.addEventListener("hashchange", function () { stops.forEach(function (s, j) { if ("#" + s.id === location.hash) open(j, { keepHash: true }); }); });
  }

  /* the opening's "325 photos" / "3 films": after the day opens, bring its head up under the line */
  d.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".ef-have a[href^='#']"); if (!a || films) return;
    setTimeout(function () {
      var dy = d.querySelector(".gf-days"); if (!dy) return;
      var nh = parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 0;
      w.scrollTo({ top: Math.max(0, w.scrollY + dy.getBoundingClientRect().top - nh - (line ? line.offsetHeight : 0)), behavior: reduced() ? "auto" : "smooth" });
    }, 60);
  });

  /* ---------------------------------------------------------------- 3. a closed stop stops its film */
  function hush(sec) {
    [].forEach.call(sec.querySelectorAll(".md-frame.is-on"), function (fr) {
      var f = fr.querySelector("iframe"); if (f) f.parentNode.removeChild(f); fr.classList.remove("is-on");
    });
  }
  if (w.MutationObserver) new MutationObserver(function (ms) {
    ms.forEach(function (m) { var s = m.target; if (s.classList && s.classList.contains("gf-day") && !s.classList.contains("is-open") && !main.classList.contains("is-all")) hush(s); });
  }).observe(main, { subtree: true, attributes: true, attributeFilter: ["class"] });

  /* ---------------------------------------------------------------- 1. the arrival: the season opens into the line */
  if (!season || !line || reduced() || !line.animate) return;
  var lit = season.querySelector(".ef-bar.is-lit"), track = line.querySelector(".gf-track"), fan = season.querySelector(".ef-fan");
  if (!lit || !track) return;
  var r = line.getBoundingClientRect();
  if (r.top > innerHeight || r.bottom < 0 || w.scrollY > 40) return;       // only on arrival, with the line in view
  var a = lit.getBoundingClientRect(), b = track.getBoundingClientRect();
  if (!b.width) return;
  var dx = a.left - b.left, sx = Math.max(0.02, a.width / b.width);
  var EASE = "cubic-bezier(.65,0,.2,1)", T0 = 260;
  track.style.transformOrigin = "0 50%";
  track.animate([{ transform: "translate(" + dx + "px,0) scaleX(" + sx + ")", opacity: .9 },
                 { transform: "translate(" + dx * .4 + "px,0) scaleX(" + (sx + (1 - sx) * .45) + ")", opacity: 1, offset: .45 },
                 { transform: "none", opacity: 1 }], { duration: 900, delay: T0, easing: EASE, fill: "backwards" });
  if (fan) fan.animate([{ transform: "scaleY(0)", opacity: 0 }, { transform: "scaleY(1)", opacity: 1 }], { duration: 620, delay: T0, easing: EASE, fill: "backwards" });
  var cx = a.left + a.width / 2;
  [].forEach.call(line.querySelectorAll(".gf-tp"), function (tp, i) {
    var q = tp.getBoundingClientRect(), off = cx - (q.left + q.width / 2);
    tp.animate([{ transform: "translateX(" + off * .35 + "px)", opacity: 0 }, { transform: "none", opacity: 1 }],
               { duration: 560, delay: T0 + 420 + i * 70, easing: "cubic-bezier(.2,.8,.2,1)", fill: "backwards" });
  });
  var gl = line.querySelector(".gf-glc");
  if (gl) gl.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 400, delay: T0 + 900, fill: "backwards" });
})();
