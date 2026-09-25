/* v3 prototypes: footage. A <video data-src="…/hero-1080"> becomes that loop
   (WebM where the browser is sure, MP4 otherwise; 720p on small screens),
   plays only while on screen, and never for reduced motion, Save-Data or 2G/3G. */
(function () {
  var mm = function (q) { return window.matchMedia && matchMedia(q).matches; };
  var c = navigator.connection || {};
  if (mm("(prefers-reduced-motion: reduce)") || c.saveData || /(^|-)(2g|3g)$/.test(c.effectiveType || "")) return;
  var small = mm("(max-width: 820px)");
  document.querySelectorAll("video[data-src]").forEach(function (v) {
    var base = v.getAttribute("data-src").replace(/-1080$/, small ? "-720" : "-1080");
    var webm = v.canPlayType && v.canPlayType('video/webm; codecs="vp9"') === "probably";
    var loaded = false;
    var load = function () { if (loaded) return; loaded = true; v.src = base + (webm ? ".webm" : ".mp4");
      if (webm) v.addEventListener("error", function () { v.src = base + ".mp4"; }, { once: true }); };
    v.addEventListener("playing", function () { v.classList.add("on"); }, { once: true });
    new IntersectionObserver(function (en) {
      if (en[0].isIntersecting) { load(); var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause();
    }, { rootMargin: "200px" }).observe(v.parentNode);
  });
})();
