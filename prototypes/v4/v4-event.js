/* The event landing pages (chat 22): designer F's "The Season Opens Here", built by tools/v4_comp_gallery.py.
   Runs after v4-gallery.js where a page has photos; alone on a films-only page (no photo viewer there).
   1. The season: the event on air today is marked "On air now" (its dates, in the visitor's own day; no JS: the dates).
   2. A day with its film and no photos is state "film", never "Photos coming" (v4-gallery.js knows only photo days);
      its film's end card offers no photos.
   3. Films-only events: one stop at a time from the line, the glider flies the leg, the line sticks under the nav.
   4. A film stops when its stop closes (no sound from a hidden stop).
   5. The arrival: the event's dates on the season line open, down the orange fan, into its own task line (the track
      grows out of the lit dates, the turnpoints drop into place left to right). Once, about 1.2 s, transform and
      opacity only, only with the line on screen at load and the page not scrolled. Reduced motion and no JS: the
      finished page, as it stands. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  var main = d.querySelector(".ev"); if (!main) return;
  var mq = w.matchMedia ? w.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  function reduced() { return mq.matches; }
  function navH() { return parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 0; }
  var line = d.querySelector(".gf-line"), season = d.querySelector(".ev-season"), body = d.querySelector(".gf-body");
  var films = main.classList.contains("ev-films");

  /* ---------------------------------------------------------------- 1. on air now */
  var t = new Date(), today = t.getFullYear() + "-" + ("0" + (t.getMonth() + 1)).slice(-2) + "-" + ("0" + t.getDate()).slice(-2);
  [].forEach.call(d.querySelectorAll("[data-first][data-last]"), function (el) {
    if (el.getAttribute("data-first") <= today && today <= el.getAttribute("data-last")) el.classList.add("is-now");
  });

  /* ---------------------------------------------------------------- 2. a day with its film and no photos */
  var tps = line ? [].slice.call(line.querySelectorAll(".gf-tp")) : [], days = [].slice.call(d.querySelectorAll(".gf-day"));
  days.forEach(function (sec, i) {
    if (!sec.hasAttribute("data-film-only")) return;
    sec.setAttribute("data-state", "film");
    var tp = tps[i]; if (!tp) return;
    tp.setAttribute("data-state", "film");
    var a = tp.querySelector("a"), h = sec.querySelector("h2");
    if (a) a.setAttribute("aria-label", (h ? h.textContent : "Day") + ", its film, no photos this day");
  });
  var fv = d.getElementById("gffv");
  if (fv) d.addEventListener("click", function (e) {
    var p = e.target.closest && e.target.closest(".gff-play, [data-film-cue]"); if (!p) return;
    var day = p.closest(".gf-day");
    fv.classList.toggle("ev-nophotos", !!(day && day.hasAttribute("data-film-only")));
  }, true);

  /* ---------------------------------------------------------------- 3. films-only: one stop at a time */
  if (films && line) {
    root.classList.add("gf-js");
    var glw = line.querySelector(".gf-glw"), glider = line.querySelector(".gf-glider"), N = days.length, cur = -1, fl = null, bk = null;
    var pct = function (i) { return (i + 0.5) * 100 / N; };
    var fly = function (a, b) {
      line.style.setProperty("--open", b);
      if (reduced() || !glw || !glw.animate || a === b || a < 0) return;
      if (fl) fl.cancel(); if (bk) bk.cancel();
      var legs = Math.abs(b - a), dir = b > a ? 1 : -1, ms = Math.min(1000, 380 + 150 * legs);
      fl = glw.animate([{ transform: "translateX(" + pct(a) + "%)" }, { transform: "translateX(" + (pct(a) + pct(b)) / 2 + "%) translateY(" + (-Math.min(9, 5 + legs)) + "px)", offset: .5 }, { transform: "translateX(" + pct(b) + "%)" }], { duration: ms, easing: "cubic-bezier(.45,0,.25,1)" });
      bk = glider.animate([{ transform: "rotate(0)" }, { transform: "rotate(" + dir * 9 + "deg)", offset: .3 }, { transform: "rotate(" + dir * 4 + "deg)", offset: .72 }, { transform: "rotate(0)" }], { duration: ms, easing: "ease-in-out" });
    };
    var open = function (i, o) {
      o = o || {};
      if (i < 0 || i >= N || i === cur) return;
      var prev = cur; cur = i;
      days.forEach(function (s, k) { s.classList.toggle("is-open", k === i); });
      tps.forEach(function (tp, k) { tp.classList.toggle("is-open", k === i); var a = tp.querySelector("a"); if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      fly(prev, i);
      if (prev >= 0 && !reduced() && days[i].animate) {
        var dir = i > prev ? 1 : -1;
        days[i].animate([{ opacity: 0, transform: "translateX(" + dir * 18 + "px)" }, { opacity: 1, transform: "none" }], { duration: 380, easing: "cubic-bezier(.2,.8,.2,1)" });
      }
      if (o.scroll) { var top = body.getBoundingClientRect().top; if (top < 0) w.scrollTo(0, Math.max(0, w.scrollY + top - navH())); }
      if (!o.keepHash) try { history.replaceState(null, "", location.pathname + location.search + "#" + days[i].id); } catch (e) {}
    };
    // the line sticks under the nav when the nav comes back (as the gallery's)
    var sentinel = d.createElement("i"); sentinel.setAttribute("aria-hidden", "true"); sentinel.style.cssText = "display:block;height:1px;margin-bottom:-1px";
    line.parentNode.insertBefore(sentinel, line);
    if (w.IntersectionObserver) new IntersectionObserver(function (es) {
      es.forEach(function (e) { line.classList.toggle("is-stuck", !e.isIntersecting && e.boundingClientRect.top < 0); });
    }).observe(sentinel);
    var start = 0, hit = -1, h = location.hash.slice(1);
    days.forEach(function (s, k) { if (s.classList.contains("is-open")) start = k; if (s.id === h) hit = k; s.classList.remove("is-open"); });
    open(hit >= 0 ? hit : start, { keepHash: true });
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest(".gf-tp a, .gf-df [data-go], .ev-have a[href^='#']");
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
      var id = (a.getAttribute("href") || "").slice(1), k = -1;
      days.forEach(function (s, j) { if (s.id === id) k = j; });
      if (k < 0) return;
      e.preventDefault(); open(k, { scroll: true });
      if (a.closest(".ev-have")) w.scrollTo({ top: Math.max(0, w.scrollY + body.getBoundingClientRect().top - navH()), behavior: reduced() ? "auto" : "smooth" });
    });
    w.addEventListener("hashchange", function () { days.forEach(function (s, j) { if ("#" + s.id === location.hash) open(j, { keepHash: true }); }); });
  }

  /* the opening's "325 photos" / "3 films": once v4-gallery.js has opened the day, bring it up under the line */
  if (!films) d.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".ev-have a[href^='#']"); if (!a) return;
    setTimeout(function () {
      var tg = d.getElementById(a.getAttribute("href").slice(1)); if (!tg) return;
      var day = tg.closest(".gf-day") || tg, top = day.getBoundingClientRect().top;
      w.scrollTo({ top: Math.max(0, w.scrollY + top - navH() - (line ? line.offsetHeight : 0) - 8), behavior: reduced() ? "auto" : "smooth" });
    }, 60);
  });

  /* ---------------------------------------------------------------- 4. a closed stop stops its film */
  function hush(sec) {
    [].forEach.call(sec.querySelectorAll(".md-frame.is-on"), function (fr) {
      var f = fr.querySelector("iframe"); if (f) f.parentNode.removeChild(f); fr.classList.remove("is-on");
    });
  }
  if (w.MutationObserver) new MutationObserver(function (ms) {
    ms.forEach(function (m) { var s = m.target; if (s.classList && s.classList.contains("gf-day") && !s.classList.contains("is-open") && !main.classList.contains("is-all")) hush(s); });
  }).observe(main, { subtree: true, attributes: true, attributeFilter: ["class"] });

  /* ---------------------------------------------------------------- 5. the arrival: the season opens into the line */
  if (!season || !line || reduced() || !line.animate) return;
  var lit = season.querySelector(".ev-bar.is-lit"), track = line.querySelector(".gf-track"), fan = season.querySelector(".ev-fan");
  if (!lit || !track) return;
  var r = line.getBoundingClientRect();
  if (r.top > innerHeight || r.bottom < 0 || w.scrollY > 40) return;
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
  tps.forEach(function (tp, i) {
    var q = tp.getBoundingClientRect(), off = cx - (q.left + q.width / 2);
    tp.animate([{ transform: "translateX(" + off * .35 + "px)", opacity: 0 }, { transform: "none", opacity: 1 }],
               { duration: 560, delay: T0 + 420 + i * 70, easing: "cubic-bezier(.2,.8,.2,1)", fill: "backwards" });
  });
  var gl = line.querySelector(".gf-glc");
  if (gl) gl.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 400, delay: T0 + 900, fill: "backwards" });
})();
