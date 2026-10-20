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
   read and, on a phone, brings that chapter into view in the bar, flies
   the route (its camera and its lit lines) and, on a wide screen, the
   gallery's pinned run (its dissolves, its caption, its marks). Which
   chapter is being read is the one under the screen's centre line (an
   observer, aria-current); another observer sends the fly-through's words
   away before they reach the bar. The route and the gallery carry their own
   names on this page (.tm-calm, .v4c-g), so v2-immersive.js's trip map and
   pinned gallery (its parts 15 and 14) find nothing to run. Reduced motion:
   every value is set at once, the hero stays still and the gallery stays a
   column. */
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
    // the first step's words wait (.is-wait) until the Overview heading, which lies over the top of the stage,
    // has scrolled off and the photograph fills the screen; the first step is longer by the heading's height
    // (--v4c-ovh), so the words still hold at the foot once they come
    var head = d.querySelector(".v4t-fly .kov-open"), kfly = d.getElementById("kfly"), first = copies[0], at = 0, wait = null;
    if (!head || !kfly) return;
    add(function (y) {
      var on = y < at;
      if (on !== wait) { wait = on; first.classList.toggle("is-wait", on); }
      return false;
    }, function () {
      var h = head.offsetHeight;
      kfly.style.setProperty("--v4c-ovh", h + "px");
      at = absTop(head) + h;
    });
  }

  /* The gallery (the section .v4c-g, tools/v4_trip_calm.py): the owner's pinned fly-through on a wide screen
     (wider than 760 px) with motion; on a phone, with reduced motion and without the script it stays a column
     of plates, and this only asks for its photographs as it nears. The scroll picks the photograph (the pin's
     length in equal shares, one a photograph); the loop eases a position v toward it by the time passed, never
     faster than a photograph in 100 ms, so a flick passes through the run as quick dissolves and never strobes
     or lands on an empty frame. The photograph at floor(v) is whole and the next lies over it at a smoothstep
     of the rest, settling from a touch larger (--o, --s, which only the pinned layout reads). Each caption's
     --co comes from the same position: a caption shows only near its own photograph, rises only for the one
     the scroll has picked and only fades for the others, so the last is gone before the next comes, no two
     show, the one showing is the photograph's that is more than half in, and none rests half faded. The marks
     fill with v; the frame's top and foot take the page's dark only while it comes in and goes (--g-in,
     --g-out, straight from the scroll). Off screen the position is where the scroll is, with no glide. Within
     two screens of the section (at every width) all its photographs are asked for and decoded, so none is
     missing when it is needed. */
  var TAU = 300, PER = 100;
  function gallery() {
    var sec = d.querySelector(".v4c-g");
    if (!sec) return;
    var track = sec.querySelector(".v4c-g-track"), pin = sec.querySelector(".v4c-g-pin"), rail = sec.querySelector(".v4c-g-rail");
    var figs = [].slice.call(sec.querySelectorAll(".v4c-g-f")), n = figs.length, wide = w.matchMedia && matchMedia("(min-width: 761px)");
    var on = false, top = 0, span = 1, vh = 1, s0 = 0, s1 = 0, v = null, lvl = [], woke = false, last = {};
    if (!track || n < 2) return;
    function put(el, prop, key, val) { if (last[key] !== val) { last[key] = val; el.style.setProperty(prop, val); return true; } }
    function size() {
      var run = !still && !!wide && wide.matches;
      if (run !== on) { on = run; sec.classList.toggle("is-pin", on); v = null; last = {}; lvl = []; }
      vh = w.innerHeight; s0 = absTop(sec); s1 = s0 + sec.offsetHeight;
      top = absTop(track); span = Math.max(1, track.offsetHeight - vh);
    }
    if (wide && wide.addEventListener) wide.addEventListener("change", measure);
    add(function (y, dt) {
      if (!woke && y > s0 - 2 * vh && y < s1) {
        woke = true;
        figs.forEach(function (f) {
          var img = f.querySelector("img"), go = function () { if (img.decode) img.decode().catch(function () {}); };
          img.loading = "eager";
          if (img.complete) go(); else img.addEventListener("load", go, { once: true });
        });
      }
      if (!on) return false;
      var t = Math.max(0, Math.min(n - 1, Math.floor((y - top) / span * n)));
      if (v === null || y < top - 2 * vh || y > top + span + vh) v = t;
      else if (v !== t) {
        v += Math.max(-dt / PER, Math.min(dt / PER, (t - v) * (1 - Math.exp(-dt / TAU))));
        // the last fiftieth of a dissolve is about a thousandth of a step of light (the smoothstep): land
        if (Math.abs(t - v) < 0.02) v = t;
      }
      var b = Math.floor(v), f = v - b, s = f * f * (3 - 2 * f);
      figs.forEach(function (fig, k) {
        var pic = fig.firstChild, up = k === b + 1 && s > 0, o = k === b ? "1" : up ? s.toFixed(3) : "0";
        // the captions, from the same position: one shows only within a third of a step of its own photograph
        // (which is then at least 72% of the picture), rising as the run arrives there; one the run is leaving
        // can only fade, and one a flick passes never rises, so no two ever show, none flashes by, and at rest
        // the one showing is whole
        var near = clamp(1 - Math.abs(v - k) / 0.35), lv = k === t ? near : Math.min(lvl[k] || 0, near);
        lvl[k] = lv;
        if (put(pic, "--o", "o" + k, o)) pic.classList.toggle("is-up", o !== "0");
        put(pic, "--s", "s" + k, up ? (1.03 - 0.03 * s).toFixed(4) : "1");
        put(fig.lastChild, "--co", "c" + k, (lv * lv * (3 - 2 * lv)).toFixed(3));
      });
      if (rail) put(rail, "--p", "p", (v / (n - 1)).toFixed(4));
      put(pin, "--g-in", "i", clamp((top - y) / (0.3 * vh)).toFixed(3));
      put(pin, "--g-out", "u", clamp((y - top - span) / (0.3 * vh)).toFixed(3));
      return v !== t;
    }, size);
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
      // the heading leaves over the first half of the changeover, while the schematic's pool comes in; the
      // schematic's names and lines come over the second half, on the finished pool (v4-calm.css)
      put("head", clamp(1 - 2 * rt).toFixed(2), function (v) { head.style.opacity = v; });
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

  /* The page's three small scripts, once inline in it (tools/v4_trip_calm.py now leaves their marks empty, for
     the page's weight): the phone's booking bar rises once the hero has scrolled away and steps aside while
     the departures' cards (each has its own Hold a place), the call (once its buttons are in view) or the
     footer is on screen; in the fly-through an observer on a line across the centre says which step owns the
     middle of the screen and swaps the photograph to match; Flying Etiquette's button opens and closes its
     list. With reduced motion too: none of them moves anything. */
  function chores() {
    var IO = w.IntersectionObserver;
    var mob = d.getElementById("dstMobar"), call = d.getElementById("enquire"), seen = [];
    var watch = [".khero, .dst-hero", ".kdates-grid", "footer"].map(function (s) { return d.querySelector(s); }).filter(Boolean);
    if (mob && watch.length && IO) {
      var note = function (es) {
        es.forEach(function (e) { var i = seen.indexOf(e.target); if (e.isIntersecting) { if (i < 0) seen.push(e.target); } else if (i >= 0) seen.splice(i, 1); });
        mob.classList.toggle("show", !seen.length);
      }, io = new IO(note, { threshold: 0 });
      watch.forEach(function (el) { io.observe(el); });
      if (call) new IO(note, { rootMargin: "0px 0px -35% 0px", threshold: 0 }).observe(call);
    }
    var kf = d.getElementById("kfly");
    if (kf && IO) {
      var steps = [].slice.call(kf.querySelectorAll(".kfly-step")), slides = kf.querySelectorAll(".kfly-slide"), marks = kf.querySelectorAll(".kfly-marks i"), at = 0;
      if (steps.length === slides.length) {
        var so = new IO(function (es) {
          es.forEach(function (e) {
            var k = steps.indexOf(e.target);
            if (!e.isIntersecting || k === at) return;
            slides[at].classList.remove("is-on"); steps[at].classList.remove("is-on");
            at = k;
            slides[at].classList.add("is-on"); steps[at].classList.add("is-on");
            [].forEach.call(marks, function (m, i) { m.classList.toggle("is-on", i <= at); });
          });
        }, { rootMargin: "-50% 0px -50% 0px", threshold: 0 });
        steps.forEach(function (s) { so.observe(s); });
      }
    }
    var tg = d.getElementById("etqToggle"), body = d.getElementById("etqBody"), txt = tg && tg.querySelector(".etq-toggle-txt");
    if (tg && body) tg.addEventListener("click", function () {
      var open = body.hidden;
      body.hidden = !open;
      tg.setAttribute("aria-expanded", open ? "true" : "false");
      if (txt) txt.textContent = open ? "Hide the rules" : "Read the nine rules";
    });
  }

  function init() {
    chores();
    // the gallery and the fly-through first: they set the run's and the first step's lengths before the
    // others measure the page
    gallery(); fly(); hero(); bar(); route();
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
