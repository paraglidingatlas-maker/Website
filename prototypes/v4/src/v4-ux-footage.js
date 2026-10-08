/* THE FOOTAGE'S PAUSE (the usability pass, 23). Inlined at the end of the pages
   that carry footage, by tools/v4_ux.py; no other page carries it. Beside Wind
   sound in the footer (v2-immersive.js puts that there as the page is ready;
   this runs just after it), the page's footage can be paused, and stays paused
   from page to page until it is played again: script.js starts each loop as it
   comes on screen, and a paused visitor's loops are stopped as they start. Not
   offered for reduced motion, which has no footage. */
(function () {
  var d = document, w = window;
  function keep(v) { try { if (v === undefined) return localStorage.getItem("v4-still"); localStorage.setItem("v4-still", v); } catch (e) { return null; } }
  function init() {
    var wind = d.querySelector(".footer-bottom .v2-wind");
    if (!wind || d.querySelector(".v4u-still") || (w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches)) return;
    var still = keep() === "on", b = d.createElement("button");
    b.type = "button"; b.className = "v2-wind v4u-still"; b.style.marginLeft = "-.4rem";
    function own(v) { return v.tagName === "VIDEO" && !v.closest(".cd-player, .v4-ls"); }
    function label() {
      var t = still ? "Play" : "Pause";
      b.setAttribute("aria-label", t); b.title = t;
      b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        (still ? '<path d="M7 5l12 7-12 7z"/>' : '<path d="M8 5v14"/><path d="M16 5v14"/>') + '</svg><span class="v4-wind-l" aria-hidden="true">' + t + "</span>";
    }
    function inView(v) {
      var r = v.getBoundingClientRect(), when = v.getAttribute("data-loop-when"), host = when && v.closest(when);
      return r.bottom > 0 && r.top < w.innerHeight && r.width > 0 && (!host || host.classList.contains("is-on"));
    }
    function each(f) { [].forEach.call(d.querySelectorAll("video"), function (v) { if (own(v)) f(v); }); }
    d.addEventListener("play", function (e) { if (still && own(e.target)) e.target.pause(); }, true);
    b.addEventListener("click", function () {
      still = !still; keep(still ? "on" : "off"); label();
      each(function (v) {
        if (still) v.pause();
        else if ((v.currentSrc || v.getAttribute("src")) && inView(v)) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      });
    });
    label();
    if (still) each(function (v) { v.pause(); });
    wind.parentNode.insertBefore(b, wind.nextSibling);
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();
