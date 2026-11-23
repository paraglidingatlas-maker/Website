/* v4-calendar.js: the SRS 2027 race calendar (chat 29, 23 Nov 2026; tools/v4_srs_calendar.py).
   1. A page rises a little as it scrolls into view (class is-in; off under reduced motion, and nothing is hidden
      without this script).
   2. The viewer: a page opened large in a <dialog>. It first fits the screen; a click or tap shows it at full size,
      to be moved by scrolling or dragging a finger (on a phone the fitted page is small: one tap makes it readable).
      Arrows and swipes for the page before and the next, Escape or the cross to close, Download and Share in the bar.
      Without this script each page is a plain link to its large image. */
(function (w, d) {
  "use strict";
  var root = d.querySelector(".cal");
  if (!root) return;
  var calm = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 1. the rise
  var sheets = [].slice.call(root.querySelectorAll(".cal-sheet"));
  if (!calm && "IntersectionObserver" in w) {
    root.classList.add("cal-js");
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -12% 0px", threshold: .12 });
    sheets.forEach(function (s) { io.observe(s); });
  }

  // 2. the viewer
  var lb = d.getElementById("cal-lb");
  if (!lb || !lb.showModal) return;
  var img = lb.querySelector("img"), box = lb.querySelector(".cal-lb-s"), cap = lb.querySelector(".cal-lb-c"),
      dl = lb.querySelector(".cal-lb-dl"), sh = lb.querySelector(".cal-lb-sh"),
      prev = lb.querySelector(".cal-lb-p"), next = lb.querySelector(".cal-lb-nx");
  var items = sheets.map(function (s) {
    var a = s.querySelector(".cal-page"), i = a.querySelector("img"), h = s.querySelector("h3"), n = s.querySelector(".cal-no"),
        l = s.querySelector(".cal-dl"), b = s.querySelector("[data-share]");
    return { id: s.id, big: a.getAttribute("href"), small: i.currentSrc || i.src, alt: i.alt, name: h ? h.textContent : "",
             no: n ? n.textContent : "", file: l ? l.getAttribute("download") : "", title: b ? b.getAttribute("data-share-title") : "", a: a };
  });
  var at = -1, from = null;

  function show(k) {
    at = Math.max(0, Math.min(items.length - 1, k));
    var it = items[at];
    lb.classList.remove("is-zoom");
    img.src = it.small;                      // the small copy at once, the large one over it when it has loaded
    img.alt = it.alt;
    var big = new Image();
    big.onload = function () { if (items[at] === it) img.src = it.big; };
    big.src = it.big;
    cap.textContent = it.no === it.name ? it.name : it.no + " · " + it.name;
    dl.href = it.big; dl.setAttribute("download", it.file);
    sh.setAttribute("data-share-url", "#" + it.id); sh.setAttribute("data-share-title", it.title);
    prev.disabled = at === 0; next.disabled = at === items.length - 1;
  }
  function open(k, el) {
    from = el || null;
    show(k);
    if (!lb.open) lb.showModal();
  }
  function zoom(e) {
    var on = !lb.classList.contains("is-zoom");
    var r = img.getBoundingClientRect(), fx = e ? (e.clientX - r.left) / r.width : .5, fy = e ? (e.clientY - r.top) / r.height : .5;
    lb.classList.toggle("is-zoom", on);
    if (on) {                                 // keep the point that was clicked under the pointer
      box.scrollLeft = Math.max(0, fx * img.offsetWidth - box.clientWidth / 2);
      box.scrollTop = Math.max(0, fy * img.offsetHeight - box.clientHeight / 2);
    }
  }

  d.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-cal]");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    var k = -1, id = +a.getAttribute("data-cal");
    items.forEach(function (it, i) { if (+it.a.getAttribute("data-cal") === id) k = i; });
    if (k < 0) return;
    e.preventDefault();
    open(k, a);
  });
  img.addEventListener("click", zoom);
  box.addEventListener("click", function (e) { if (e.target === box) lb.close(); });
  lb.querySelector(".cal-lb-x").addEventListener("click", function () { lb.close(); });
  prev.addEventListener("click", function () { show(at - 1); });
  next.addEventListener("click", function () { show(at + 1); });
  lb.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") { show(at - 1); e.preventDefault(); }
    else if (e.key === "ArrowRight") { show(at + 1); e.preventDefault(); }
  });
  lb.addEventListener("close", function () { img.removeAttribute("src"); if (from && from.focus) from.focus({ preventScroll: true }); });

  // a swipe to the side on the fitted page: the page before or the next
  var x0 = null, y0 = 0;
  box.addEventListener("touchstart", function (e) { x0 = e.touches.length === 1 && !lb.classList.contains("is-zoom") ? e.touches[0].clientX : null; y0 = e.touches[0].clientY; }, { passive: true });
  box.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    x0 = null;
    if (Math.abs(dx) > 60 && Math.abs(dx) > 2 * Math.abs(dy)) show(at + (dx < 0 ? 1 : -1));
  }, { passive: true });
})(window, document);
