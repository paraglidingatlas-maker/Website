/* TRIPS, LESS BUT BETTER (owner, 19 Oct 2026). The script of a calmed trip
   page: tools/v4_trip_calm.py links it (and v4-calm.css) from India alone and
   puts html.v4-calm on that page, so Kenya and every other v4 page load none
   of it, and v2-immersive.js is as it was. Written to v4-calm.js by
   tools/v4_min.py.

   One requestAnimationFrame loop, the record page's (tools/v4_record.py, its
   part 6): each frame reads the scroll position, every value closes a share
   of its gap to where the scroll has put it (by the time passed: a glide
   with weight), and the loop stops once all have arrived; the next scroll or
   resize starts it again. Geometry is measured on resize, on load, once the
   fonts are in and when the page's height changes (a fold opening), never
   per frame. It moves the hero's photograph at 0.3 of the scroll while the
   hero is in view, fills the chapter bar's hairline under the chapter being
   read and, on a phone, brings that chapter into view in the bar, and flies
   the route: its camera and its lit lines. Which chapter is being read is
   the one under the screen's centre line (an observer, aria-current);
   another observer sends the fly-through's words away before they reach the
   bar. The route and the gallery carry their own names on this page
   (.tm-calm, .v4c-g), so v2-immersive.js's trip map and pinned gallery
   (its parts 15 and 14) find nothing to run. Reduced motion: every value is
   set at once and the hero stays still. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  if (!root.classList.contains("v4-calm")) return;
  var still = !!(w.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var steps = [], sizes = [], raf = 0, last = 0;
  function toward(v, to, dt, tau, eps) { return still || v === null || Math.abs(to - v) < eps ? to : v + (to - v) * (1 - Math.exp(-dt / tau)); }
  function clamp(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  // every step(y, dt) returns true while one of its values is still on its way
  function frame(t) {
    raf = 0;
    var dt = last ? Math.min(64, Math.max(1, t - last)) : 16, y = w.scrollY, busy = false;
    last = t;
    for (var i = 0; i < steps.length; i++) if (steps[i](y, dt)) busy = true;
    if (busy) raf = requestAnimationFrame(frame); else last = 0;
  }
  function kick() { if (!raf) raf = requestAnimationFrame(frame); }
  function measure() { for (var i = 0; i < sizes.length; i++) sizes[i](); kick(); }
  function add(step, size) { steps.push(step); if (size) { sizes.push(size); size(); } }
  function absTop(el) { return el.getBoundingClientRect().top + w.scrollY; }

  // the hero: one plate, at 0.3 of the scroll while in view
  function hero() {
    var par = d.querySelector(".khero-par");
    if (!par || still) return;
    var vh = 0, ty = null, wrote = "";
    add(function (y, dt) {
      var to = 0.3 * Math.min(Math.max(0, y), vh * 1.3);
      ty = toward(ty, to, dt, 140, 0.05);
      var s = ty.toFixed(1);
      if (s !== wrote) { wrote = s; par.style.transform = "translate3d(0," + s + "px,0)"; }
      return ty !== to;
    }, function () { vh = w.innerHeight; });
  }

  // the chapter bar: the chapter under the centre line, a hairline filling as each is read
  function bar() {
    var jump = d.querySelector(".dst-jump"), sc = jump && jump.querySelector(".dst-jump-in");
    if (!sc) return;
    var links = [].slice.call(sc.querySelectorAll(':scope > a[href^="#"]')), secs = [], lines = [];
    links = links.filter(function (a) { var s = d.getElementById(a.getAttribute("href").slice(1)); if (s) secs.push(s); return !!s; });
    if (!links.length) return;
    links.forEach(function (a) { var i = d.createElement("i"); i.className = "v4c-bar"; i.setAttribute("aria-hidden", "true"); a.appendChild(i); lines.push(i); });
    var tops = [], ends = [], vh = 0, ps = links.map(function () { return null; }), wrote = links.map(function () { return ""; });
    var cur = -1, sx = null, tx = null;
    // the chapter being read: the last whose top is above the centre line (before the first, the first)
    function current() {
      var c = 0, mid = w.innerHeight * 0.5;
      for (var k = 0; k < secs.length; k++) if (secs[k].getBoundingClientRect().top <= mid) c = k;
      set(c);
    }
    function set(c) {
      if (c === cur) return;
      cur = c;
      links.forEach(function (a, k) { if (k === c) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      // on a phone the bar scrolls; bring the chapter being read into view, eased by the loop, with
      // the one before it whole at the bar's left inset (never a word cut at the edge)
      if (sc.scrollWidth > sc.clientWidth + 1) {
        sx = sc.scrollLeft;
        tx = Math.max(0, Math.min(sc.scrollWidth - sc.clientWidth, links[Math.max(0, c - 1)].offsetLeft - links[0].offsetLeft));
        kick();
      }
    }
    if ("IntersectionObserver" in w) {
      var io = new IntersectionObserver(current, { rootMargin: "-50% 0px -50% 0px", threshold: 0 });
      secs.forEach(function (s) { io.observe(s); });
    }
    // a finger or a wheel on the bar is the visitor's own scroll: stop easing it
    ["pointerdown", "wheel", "touchstart"].forEach(function (ev) { sc.addEventListener(ev, function () { tx = null; }, { passive: true }); });
    add(function (y, dt) {
      var busy = false, mid = y + vh * 0.5, c = 0;
      // the same answer from the measured tops, for a jump that skips a chapter's edge (a link, the end of the page)
      for (var k = 0; k < tops.length; k++) if (tops[k] <= mid) c = k;
      set(c);
      for (k = 0; k < lines.length; k++) {
        var to = clamp((mid - tops[k]) / Math.max(1, ends[k] - tops[k]));
        ps[k] = toward(ps[k], to, dt, 140, 0.002);
        if (ps[k] !== to) busy = true;
        var s = ps[k].toFixed(3);
        if (s !== wrote[k]) { wrote[k] = s; lines[k].style.setProperty("--p", s); }
      }
      if (tx !== null) {
        sx = toward(sx, tx, dt, 140, 0.5);
        sc.scrollLeft = sx;
        if (sx === tx) tx = null; else busy = true;
      }
      return busy;
    }, function () {
      vh = w.innerHeight;
      tops = secs.map(absTop);
      ends = secs.map(function (s, k) { return k + 1 < secs.length ? tops[k + 1] : tops[k] + s.offsetHeight; });
      current();
    });
  }

  // the fly-through: a step's words leave once their top passes a line a little under the chapter bar, and
  // come back when it is below it again (v4-calm.css fades them); an observer, nothing per frame
  function fly() {
    var copies = [].slice.call(d.querySelectorAll(".kfly-copy"));
    if (!copies.length || still || !("IntersectionObserver" in w)) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle("is-gone", !!e.rootBounds && e.boundingClientRect.top < e.rootBounds.top); });
    }, { rootMargin: "-15% 0px 0px 0px", threshold: [0, 1] });
    copies.forEach(function (c) { io.observe(c); });
  }

  /* The route (the trip map of tools/v4_tripmap.py, flown here instead of by v2-immersive.js part 15). The
     camera falls from the continent to the country, India with Bir Billing at its centre (tools/
     v4_trip_calm.py), in the first sixth of the pin; the other five sixths are the cards', a fair share each,
     so the first is read as long as the last. As the schematic comes in the camera eases Bir Billing aside on
     a wide screen, to a fifth of the width, clear of the schematic on the right and the cards below. Each
     card's line on the schematic draws with the scroll through its mask. On a phone the schematic keeps one
     frame, Dharamshala to 360 and the launch to the landing, so every name on it is whole on every card. The
     viewBox is written only while the camera moves, attributes and classes only when they change. Reduced
     motion: the last frame, the lines whole. */
  var FALL = 0.18;
  function route() {
    var sec = d.querySelector(".tm-calm");
    if (!sec) return;
    var keys = JSON.parse(sec.dataset.keys), hl = JSON.parse(sec.dataset.hl || "[]"), F = keys.focus;
    var svg = sec.querySelector(".tm-map"), track = sec.querySelector(".tm-track"), head = sec.querySelector(".tm-head");
    var cards = [].slice.call(sec.querySelectorAll(".tm-card")), sites = [].slice.call(sec.querySelectorAll(".tm-site"));
    var schem = sec.querySelector(".tm-schem"), sv = schem && schem.querySelector("svg"), n = cards.length;
    if (!svg || !track || !n) return;
    var CROP = [180, 30, 620, 330], FULL = [0, 0, 1000, 400], MASK = { "ir-west": "irmW", "ir-east": "irmE", "ir-over": "irmO" };
    var top = 0, span = 1, mw = 1, mh = 1, phone = false, aside = 0, c = null, at = -2, last = {}, lit = [];
    function lerp(a, b, t) { return a + (b - a) * t; }
    function cam(a, b, t) { t = t * t * (3 - 2 * t); return [lerp(a[0], b[0], t), lerp(a[1], b[1], t), Math.exp(lerp(Math.log(a[2]), Math.log(b[2]), t))]; }
    function put(key, v, fn) { if (last[key] !== v) { last[key] = v; fn(v); } }
    function show(i) {
      if (i === at) return; at = i;
      cards.forEach(function (el, k) { el.classList.toggle("is-on", k === i); });
      sites.forEach(function (s, k) { s.classList.toggle("is-on", k === Math.min(i, sites.length - 1) && i >= 0); s.classList.toggle("is-past", i >= 0 && k <= i); });
      if (schem) schem.setAttribute("data-on", hl[i] || "");
    }
    if (sv) hl.forEach(function (k, i) {
      var m = MASK[k] && sv.querySelector("#" + MASK[k]);
      if (m) lit.push({ i: i, f: null, ps: [].slice.call(m.querySelectorAll("path")).map(function (p) {
        var L = p.getTotalLength();
        if (!still) p.style.strokeDasharray = L.toFixed(1);
        return { p: p, L: L };
      }) });
    });
    function frameOf(cx, cy, cw) {
      var vw = cw, vh = cw * mh / mw;
      if (mw < mh) { vh = cw * 1.15; vw = vh * mw / mh; }
      put("vb", (cx - vw / 2).toFixed(1) + " " + (cy - vh / 2).toFixed(1) + " " + vw.toFixed(1) + " " + vh.toFixed(1), function (v) { svg.setAttribute("viewBox", v); });
      put("u", (vw / mw).toFixed(4), function (v) { svg.style.setProperty("--u", v); });
    }
    function size() {
      top = absTop(track);
      span = Math.max(1, track.offsetHeight - w.innerHeight);
      var r = svg.getBoundingClientRect();
      mw = Math.max(1, r.width); mh = Math.max(1, r.height); phone = w.innerWidth < 760;
      aside = phone ? 0 : keys.region[2] * keys.zoom * .3;
      last.vb = "";
      if (sv) put("crop", (phone ? CROP : FULL).join(" "), function (v) { sv.setAttribute("viewBox", v); });
      if (still) frameOf(keys.region[0], keys.region[1], keys.region[2]);
    }
    if (still) { add(function () { return false; }, size); return; }
    add(function (y, dt) {
      var p = clamp((y - top) / span), busy = false, ct, k = 0, q = 0, x = 0, cur = -1;
      if (p < FALL) ct = cam(keys.world, keys.country, p / FALL);
      else {
        q = (p - FALL) / (1 - FALL); k = Math.min(1, q / .08);
        x = q * n; cur = Math.min(n - 1, Math.floor(x));
        ct = cam(keys.country, [F[Math.min(F.length - 1, cur)][0] + aside, F[Math.min(F.length - 1, cur)][1], keys.region[2] * keys.zoom], k);
      }
      // the camera: centre and width (the width in log terms, as the zoom is), eased
      var lw = Math.log(ct[2]);
      if (!c) c = [ct[0], ct[1], lw];
      var ep = ct[2] * .4 / mw;
      c[0] = toward(c[0], ct[0], dt, 140, ep); c[1] = toward(c[1], ct[1], dt, 140, ep); c[2] = toward(c[2], lw, dt, 140, .0003);
      if (c[0] !== ct[0] || c[1] !== ct[1] || c[2] !== lw) busy = true;
      frameOf(c[0], c[1], Math.exp(c[2]));
      // the country's name comes in as the fall ends and goes as the route comes in, with the heading; Bir
      // Billing's marker and the finer marks come in over the end of the fall and stay
      var rt = p < FALL ? 0 : Math.min(1, q / .06);
      var cn = p < FALL ? clamp((p / FALL - .4) / .6) : 1 - rt, fine = p < FALL ? clamp((p / FALL - .55) / .45) : 1;
      put("fine", fine.toFixed(2), function (v) { svg.style.setProperty("--fine", v); });
      put("ter", (fine * .85).toFixed(2), function (v) { svg.style.setProperty("--ter", v); });
      put("cn", cn.toFixed(2), function (v) { svg.style.setProperty("--cn", v); });
      put("rt", rt.toFixed(2), function (v) { sec.style.setProperty("--route", v); sec.classList.toggle("is-route", rt > 0); });
      put("head", (1 - rt).toFixed(2), function (v) { head.style.opacity = v; });
      show(cur);
      // each card's line draws over the first three quarters of its card and stays, eased, and never more than
      // a few hundredths of the line a frame, so a wheel's notch draws it rather than jumps
      lit.forEach(function (L) {
        var ft = cur < 0 ? 0 : clamp((x - L.i) / .75);
        var f = toward(L.f, ft, dt, 140, .002), cap = .06 / L.ps.length;
        L.f = L.f === null ? f : L.f + Math.max(-cap, Math.min(cap, f - L.f));
        if (L.f !== ft) busy = true;
        L.ps.forEach(function (s, j) {
          put("d" + L.i + "-" + j, (s.L * (1 - clamp(L.f * L.ps.length - j))).toFixed(1), function (v) { s.p.style.strokeDashoffset = v; });
        });
      });
      return busy;
    }, size);
  }

  function init() {
    hero(); bar(); fly(); route();
    kick();
    w.addEventListener("scroll", kick, { passive: true });
    var rz = 0;
    w.addEventListener("resize", function () { cancelAnimationFrame(rz); rz = requestAnimationFrame(measure); }, { passive: true });
    w.addEventListener("load", measure);
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(measure);
    // a fold opening moves every chapter below it
    var main = d.getElementById("v4-main"), h0 = 0;
    if (main && "ResizeObserver" in w) new ResizeObserver(function () {
      var h = main.offsetHeight;
      if (h !== h0) { h0 = h; cancelAnimationFrame(rz); rz = requestAnimationFrame(measure); }
    }).observe(main);
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();
