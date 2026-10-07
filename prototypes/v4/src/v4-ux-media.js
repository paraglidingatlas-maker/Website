/* v4-ux-media.js: the usability pass, item 6 (and 23). Inlined in the head of the
   home page and the trip pages by tools/v4_ux.py, so it runs before the clip
   loader in script.js; edit here, then run python3 tools/v4_ux.py.

   6. Weight on a phone. A picture that waits (data-v4-src, written by
      tools/v4_ux.py) is fetched only when it is about to be seen: a trip hero's
      slide just before the slideshow turns to it (or at once, when a tab or a
      swipe asks for it), the home page's four expedition photographs when the
      fly-through comes near. The hero clips: on a phone held upright, the clip
      cut to what an upright screen shows (img/clips, tools/v4_phone_media.py,
      a third of the bytes); elsewhere the 1080p or the 720p file by the width
      the clip fills, not by the screen (23), changed over if the window grows. */
(function () {
  "use strict";
  var d = document, w = window;
  var m = location.pathname.match(/^(.*\/prototypes\/v\d+\/)/), BASE = m ? m[1] : "/assets/v4/";
  var PHONE_CLIPS = { bir: 1, hero: 1 };
  function upright() { return w.innerWidth / Math.max(1, w.innerHeight) <= 2 / 3; }
  function big() { return w.innerWidth > 820 && w.innerWidth * Math.min(w.devicePixelRatio || 1, 2) > 1400; }
  function want(v) {
    var base = v.getAttribute("data-v4u-base"), name = base.split("/").pop();
    return upright() && PHONE_CLIPS[name] ? BASE + "img/clips/" + name + "-p-720" : base + (big() ? "-1080" : "-720");
  }
  function fit(v) {
    if (v.hasAttribute("data-v4u-base") || !v.hasAttribute("data-loop") || v.hasAttribute("data-loop-size")) return;
    if (!v.closest || !v.closest(".khero, .v2-home-hero")) return;
    v.setAttribute("data-v4u-base", v.getAttribute("data-loop"));
    var t = want(v), i = t.lastIndexOf("-");
    v.setAttribute("data-loop", t.slice(0, i));           // script.js adds "-" + the size
    v.setAttribute("data-loop-size", t.slice(i + 1));
  }
  // the loader in script.js reads these as it runs, at the end of the page: set them as the clips arrive
  var mo = w.MutationObserver && new MutationObserver(function (rs) {
    rs.forEach(function (r) { [].forEach.call(r.addedNodes, function (n) {
      if (n.nodeType !== 1) return;
      if (n.tagName === "VIDEO") fit(n); else if (n.querySelectorAll) [].forEach.call(n.querySelectorAll("video[data-loop]"), fit);
    }); });
  });
  if (mo) mo.observe(d.documentElement, { childList: true, subtree: true });
  var rt = 0;
  w.addEventListener("resize", function () {
    clearTimeout(rt);
    rt = setTimeout(function () {
      [].forEach.call(d.querySelectorAll("video[data-v4u-base]"), function (v) {
        var s = v.currentSrc || "", t = want(v);
        if (!s || s.indexOf(t.split("/").pop() + ".") !== -1) return;
        if (/-1080\./.test(s) && /-720$/.test(t) && t.indexOf("-p-720") === -1) return;     // never trade down for a smaller window
        var at = v.currentTime, on = !v.paused;
        v.src = t + s.slice(s.lastIndexOf("."));
        v.addEventListener("loadedmetadata", function () { try { v.currentTime = at; } catch (e) {} }, { once: true });
        if (on) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }      // preload="none": play is what loads it
      });
    }, 400);
  });

  function wake(el) {
    if (!el) return;
    [].forEach.call(el.querySelectorAll ? el.querySelectorAll("[data-v4-src],[data-v4-srcset]") : [], function (x) {
      if (x.dataset.v4Srcset) { x.srcset = x.dataset.v4Srcset; x.removeAttribute("data-v4-srcset"); }
      if (x.dataset.v4Src) { x.src = x.dataset.v4Src; x.removeAttribute("data-v4-src"); }
    });
  }
  function init() {
    if (mo) { mo.disconnect(); [].forEach.call(d.querySelectorAll("video[data-loop]"), fit); }
    // a trip hero: the slide on screen and the next one, as the slideshow turns
    var slides = [].slice.call(d.querySelectorAll(".khero-slide"));
    if (slides.length > 1) {
      var next = function () {
        var i = slides.findIndex(function (s) { return s.classList.contains("is-on"); });
        wake(slides[i]); wake(slides[(i + 1) % slides.length]);
      };
      slides.forEach(function (s) { new MutationObserver(next).observe(s, { attributes: true, attributeFilter: ["class"] }); });
      // the slideshow first turns 6.5 s after load: the second photograph comes 2 s before that
      var soon = function () { setTimeout(function () { wake(slides[1]); }, 4500); };
      if (d.readyState === "complete") soon(); else w.addEventListener("load", soon, { once: true });
    }
    // the home page's expedition photographs: on the visitor's first scroll, or when the fly-through shows
    var fb = d.querySelector(".v2-fb-stage");
    if (fb && fb.querySelector("[data-v4-src]")) {
      var go = function () { w.removeEventListener("scroll", go); if (io) io.disconnect(); wake(fb); }, io = null;
      w.addEventListener("scroll", go, { passive: true });
      if ("IntersectionObserver" in w) { io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.intersectionRatio > 0; })) go(); }); io.observe(fb.closest(".v2-flyby") || fb); }
      else go();
    }
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();
