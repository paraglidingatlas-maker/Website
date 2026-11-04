/* Media kit, designer E (Cloudbase): "Pull Back To The Coverage".
   1. The pull back: the first screen is one shot of a race; as the visitor scrolls, the camera pulls back until
      that shot is the second of four posters (Daily Highlights) and the other three slide in, in event order.
      Scroll drives it both ways: scroll up and the camera flies back in. Nothing moves on its own; it stops off
      screen; under reduced motion, or without this script, the page is the finished page.
   2. "Check dates" anywhere picks its package in the dates form.
   3. On a phone, one bar with the one action once the opening is gone, hidden at the form and the footer.
   v4-media.js (the site's) runs the showreel, the play-in-place videos and the photo viewer. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  var mm = function (q) { return w.matchMedia && w.matchMedia(q).matches; };
  root.classList.add("e-js");
  function ready(f) { if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", f); else f(); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function band(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
  function inout(t) { return -(Math.cos(Math.PI * t) - 1) / 2; }
  function out3(t) { return 1 - Math.pow(1 - t, 3); }

  ready(function () {
    pull();
    picks();
    bar();
    board();
  });

  /* ---------------------------------------------------------------- 1. the pull back ---- */
  function pull() {
    var wrap = d.querySelector(".e-pull"); if (!wrap) return;
    var stage = wrap.querySelector(".e-stage"), hero = stage.querySelector(".e-hero"), cam = hero.querySelector(".e-cam"),
        img = cam.querySelector("img"), shade = hero.querySelector(".e-shade"), copy = hero.querySelector(".e-copy"),
        bug = hero.querySelector(".e-bug"), four = stage.querySelector(".e-four"), head = four.querySelector(".e-four-head"),
        slotLi = four.querySelector(".e-pl.is-cam"), slot = slotLi.querySelector(".e-poster"),
        others = [].slice.call(four.querySelectorAll(".e-pl:not(.is-cam)")), line = four.querySelector(".e-line"),
        note = four.querySelector(".e-four-note"), nav = d.querySelector(".page-wrap > nav");
    var ok = !mm("(prefers-reduced-motion: reduce)") && w.CSS && CSS.supports("position", "sticky") &&
             CSS.supports("clip-path", "inset(0 0 0 0 round 4px)");
    if (!ok) return;
    root.classList.add("e-move");

    var A = 1600 / 2400;              // the photo's own shape (SRS_5_T2_133-2, portrait)
    var G = {};                       // geometry, measured
    var P = 0, T = 0, raf = 0, near = true;

    function measure() {
      var navH = nav ? nav.offsetHeight : 93;
      if (nav && nav.classList.contains("v2-nav-pinned")) navH = parseFloat(getComputedStyle(root).getPropertyValue("--e-nav")) || navH;
      root.style.setProperty("--e-nav", navH + "px");
      var sr = stage.getBoundingClientRect();
      G.W = sr.width; G.H = sr.height;
      // the slot is measured where it rests (its own box never moves; only its words fade)
      var r = slot.getBoundingClientRect();
      G.sx = r.left - sr.left; G.sy = r.top - sr.top; G.sw = r.width; G.sh = r.height;
      G.phone = G.W < 701;
      // the opening's framing: the wing a little right of centre on a wide screen, high on a phone
      G.ox0 = G.phone ? .5 : .6; G.oy0 = G.phone ? .3 : .47; G.z0 = G.phone ? 1.06 : 1;
      G.ox1 = .5; G.oy1 = .3;                                   // the poster's own crop (.e-p2-img)
      // the base size the photo is laid out at: it covers the whole stage
      G.bh = Math.max(G.H, G.W / A) * G.z0; G.bw = G.bh * A;
      img.style.setProperty("--e-bw", G.bw.toFixed(1) + "px"); img.style.setProperty("--e-bh", G.bh.toFixed(1) + "px");
      // the travel: how far the visitor scrolls while the camera pulls back
      var travel = Math.round(G.H * (G.phone ? .8 : .85));
      wrap.style.setProperty("--e-travel", travel + "px");
      G.start = 0;
      G.end = wrap.getBoundingClientRect().top + w.scrollY + travel;   // the pin ends here
      others.forEach(function (li) { li.style.transform = ""; });
      G.others = others.map(function (li, i) {
        var rr = li.getBoundingClientRect();
        var cx = rr.left + rr.width / 2 - (r.left + r.width / 2), cy = rr.top + rr.height / 2 - (r.top + r.height / 2);
        return { li: li, dx: Math.sign(cx) * Math.min(90, Math.abs(cx) * .25), dy: Math.sign(cy) * Math.min(60, Math.abs(cy) * .2), a: .5 + i * .06 };
      });
    }

    function render(p) {
      var e = inout(band(p, 0, .86));
      // the frame: from the whole screen to the slot
      var x = lerp(0, G.sx, e), y = lerp(0, G.sy, e), fw = lerp(G.W, G.sw, e), fh = lerp(G.H, G.sh, e), rad = lerp(0, 4, e);
      // the photo inside it, always covering the frame, its framing easing to the poster's
      var z = lerp(G.z0, 1, e), hd = Math.max(fh, fw / A) * z, wd = hd * A;
      var ox = lerp(G.ox0, G.ox1, e), oy = lerp(G.oy0, G.oy1, e);
      var left = x + (fw - wd) * ox, top = y + (fh - hd) * oy, k = wd / G.bw;
      img.style.transform = "translate3d(" + left.toFixed(2) + "px," + top.toFixed(2) + "px,0) scale(" + k.toFixed(5) + ")";
      cam.style.clipPath = "inset(" + y.toFixed(2) + "px " + (G.W - x - fw).toFixed(2) + "px " + (G.H - y - fh).toFixed(2) + "px " + x.toFixed(2) + "px round " + rad.toFixed(2) + "px)";
      // the opening's words leave first, then its shade
      var g = out3(band(p, 0, .26));
      copy.style.opacity = bug.style.opacity = (1 - g).toFixed(3);
      copy.style.transform = "translate3d(0," + (-28 * g).toFixed(1) + "px,0)";
      bug.style.transform = "translate3d(0," + (-14 * g).toFixed(1) + "px,0)";
      shade.style.opacity = (1 - band(p, .05, .5)).toFixed(3);
      // the other three pieces slide in, in event order
      G.others.forEach(function (o) {
        var t = out3(band(p, o.a, o.a + .32));
        o.li.style.opacity = t.toFixed(3);
        o.li.style.transform = "translate3d(" + ((1 - t) * o.dx).toFixed(1) + "px," + ((1 - t) * o.dy).toFixed(1) + "px,0)";
      });
      var h = out3(band(p, .62, .94));
      head.style.opacity = h.toFixed(3); head.style.transform = "translate3d(0," + ((1 - h) * 18).toFixed(1) + "px,0)";
      note.style.opacity = out3(band(p, .8, 1)).toFixed(3);
      if (line) { line.style.setProperty("--e-ln", inout(band(p, .72, 1)).toFixed(4)); line.style.opacity = out3(band(p, .62, .86)).toFixed(3); }
      slot.style.setProperty("--e-t2", out3(band(p, .8, 1)).toFixed(3));
      stage.classList.toggle("is-gone", g > .6);
      stage.classList.toggle("is-four", p > .97);
      stage.classList.toggle("is-done", p >= .999);
    }

    function target() { return clamp((w.scrollY - G.start) / Math.max(1, G.end - G.start), 0, 1); }
    function tick() {
      raf = 0;
      var d1 = T - P;
      P = Math.abs(d1) < .0008 || !near ? T : P + d1 * .2;      // a touch of weight, never a lag off screen
      render(P);
      if (P !== T) raf = requestAnimationFrame(tick);
    }
    function onScroll() { T = target(); if (!raf) raf = requestAnimationFrame(tick); }

    measure(); P = T = target(); render(P);
    w.addEventListener("scroll", onScroll, { passive: true });
    var rt = 0;
    w.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { measure(); P = T = target(); render(P); }, 120); });
    w.addEventListener("load", function () { measure(); P = T = target(); render(P); });
    if (w.IntersectionObserver) new IntersectionObserver(function (en) { near = en[0].isIntersecting; }, { rootMargin: "50% 0px" }).observe(wrap);

    // a keyboard visitor never lands on a hidden poster or a hidden button: focus takes the camera there
    four.addEventListener("focusin", function () { if (T < 1) w.scrollTo({ top: Math.ceil(G.end) + 1, behavior: "auto" }); });
    hero.addEventListener("focusin", function () { if (T > 0) w.scrollTo({ top: 0, behavior: "auto" }); });
    w.addEventListener("beforeprint", function () { root.classList.remove("e-move"); });
    w.addEventListener("afterprint", function () { root.classList.add("e-move"); measure(); render(P); });
  }

  /* ---------------------------------------------------------------- 2. the package a "Check dates" was pressed for ---- */
  function picks() {
    var sel = d.getElementById("e-pkg");
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[data-pkg]"); if (!a) return;
      var v = a.getAttribute("data-pkg");
      if (sel) for (var i = 0; i < sel.options.length; i++) if (sel.options[i].text === v) sel.selectedIndex = i;
      var href = a.getAttribute("href") || "";
      if (/^#pk-/.test(href)) {                               // a poster: show the package it belongs to
        var card = d.querySelector(href); if (!card) return;
        card.classList.add("is-lit"); setTimeout(function () { card.classList.remove("is-lit"); }, 1800);
      }
    });
    try {                                                     // ?package=Season from another page
      var q = new URLSearchParams(location.search).get("package");
      if (q && sel) for (var j = 0; j < sel.options.length; j++) if (sel.options[j].text.toLowerCase() === q.toLowerCase()) sel.selectedIndex = j;
    } catch (err) {}
  }

  /* ---------------------------------------------------------------- 3. the phone bar ---- */
  function bar() {
    var b = d.getElementById("eMobar"), dates = d.getElementById("dates"), foot = d.querySelector("body > footer"), wrap = d.querySelector(".e-pull");
    if (!b || !w.IntersectionObserver) return;
    var atForm = false, atFoot = false, past = false;
    function set() { b.classList.toggle("show", past && !atForm && !atFoot); }
    new IntersectionObserver(function (en) { atForm = en[0].isIntersecting; set(); }, { rootMargin: "0px 0px -20% 0px" }).observe(dates);
    if (foot) new IntersectionObserver(function (en) { atFoot = en[0].isIntersecting; set(); }).observe(foot);
    var q = 0;
    w.addEventListener("scroll", function () {
      if (q) return; q = requestAnimationFrame(function () {
        q = 0; var end = wrap ? wrap.getBoundingClientRect().bottom : 0;
        past = end < innerHeight * .35; set();
      });
    }, { passive: true });
  }

  /* ---------------------------------------------------------------- 4. the views board fills once, when it is seen ---- */
  function board() {
    var bd = d.querySelector(".e-board"); if (!bd) return;
    if (!w.IntersectionObserver || mm("(prefers-reduced-motion: reduce)")) { bd.classList.add("is-in"); return; }
    var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { bd.classList.add("is-in"); io.disconnect(); } }, { threshold: .4 });
    io.observe(bd);
    w.addEventListener("beforeprint", function () { bd.classList.add("is-in"); });
  }
})();
