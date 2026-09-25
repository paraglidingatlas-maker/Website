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
/* the trip finder (direction D): filters the departures table and takes you there */
(function () {
  var f = document.querySelector("[data-finder]"); if (!f) return;
  var out = document.querySelector("[data-found]"), rows = [].slice.call(document.querySelectorAll(".dep[data-place]"));
  var names = { india: "India", kenya: "Kenya", kazakhstan: "Kazakhstan", peru: "Peru" };
  function run(scroll) {
    var place = f.place.value, month = f.month.value, n = 0;
    rows.forEach(function (r) {
      var ok = (!place || r.dataset.place === place) && (!month || r.dataset.month === month);
      r.hidden = !ok; if (ok) n++;
    });
    var box = document.querySelector(".deps"); if (box) box.hidden = !n;
    if (out) {
      out.innerHTML = (!place && !month) ? "" : n
        ? "<b>" + n + (n === 1 ? " departure" : " departures") + "</b> match" + (place ? " " + names[place] : "") + (month ? ", " + f.month.options[f.month.selectedIndex].text : "") + ". <button type=button data-clear>Show all</button>"
        : "No departure matches that yet. <button type=button data-clear>Show all</button> or <a href=\"https://calendar.app.google/HaJMYuiomt5Db9eh8\" target=\"_blank\" rel=\"noopener\">book a call</a> and we will find one.";
    }
    if (scroll) document.getElementById("dates").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }
  f.addEventListener("submit", function (e) { e.preventDefault(); run(true); });
  document.addEventListener("click", function (e) {
    if (e.target.closest && e.target.closest("[data-clear]")) { f.place.value = ""; f.month.value = ""; run(false); }
  });
})();
