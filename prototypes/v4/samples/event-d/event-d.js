/* Designer D (Trim), event landing page: the cut, the chapter bar, films in place, the photo viewer.
   Everything here is an addition: with no JavaScript the page is complete (the cover rests on its last frame,
   the bar's days are anchors, films link to YouTube, photos open full size). */
(function () {
  "use strict";
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cover = d.querySelector(".ev-cover"), slate = d.querySelector(".ev-slate");
  if (!cover || !slate) return;
  // the cover fills the first screen under the site's header, whatever its height on this device
  var nav = d.querySelector(".page-wrap > nav");
  function navh() { if (nav && getComputedStyle(nav).position !== "fixed") root.style.setProperty("--ev-nav", nav.offsetHeight + "px"); }
  navh(); window.addEventListener("resize", navh);
  var frames = [].slice.call(cover.querySelectorAll(".ev-f"));
  var days = [].slice.call(slate.querySelectorAll(".ev-s[data-f]"));
  var pp = slate.querySelector(".ev-pp");

  /* ---- the cut: one forward pass, a straight cut from day to day, then rest on the last frame ---- */
  var run = root.classList.contains("ev-run") && !reduce && frames.length > 1;
  var at = -1, held = false, offscreen = false, userHeld = false;

  function hold() {
    if (!run) return;
    held = offscreen || userHeld || d.hidden;
    root.classList.toggle("ev-held", held);
  }
  function show(i) {
    frames.forEach(function (f, k) { f.classList.toggle("is-on", k === i); });
    days.forEach(function (s, k) {
      s.classList.toggle("is-run", k === i);
      s.classList.toggle("is-past", k < i);
    });
    at = i;
  }
  function ready(i, cb) {
    var im = frames[i] && frames[i].querySelector("img");
    if (!im || (im.complete && im.naturalWidth)) return cb();
    im.loading = "eager";
    var done = function () { im.removeEventListener("load", done); im.removeEventListener("error", done); cb(); };
    im.addEventListener("load", done); im.addEventListener("error", done);
  }
  function end() {
    if (!run) return;
    run = false;
    root.classList.remove("ev-run", "ev-live", "ev-held");
    frames.forEach(function (f) { f.classList.remove("is-on"); });
    days.forEach(function (s) { s.classList.remove("is-run", "is-past"); });
    if (pp) pp.hidden = true;
    spy();
  }
  function next() {
    if (!run) return;
    var n = at + 1;
    if (n >= frames.length) return end();
    // never cut to a frame that has not arrived: the line waits, full, until it has
    ready(n, function () { if (run) show(n); });
  }
  if (run) {
    root.classList.add("ev-live");
    frames.forEach(function (f) { var im = f.querySelector("img"); if (im) im.loading = "eager"; });
    show(0);
    if (pp) {
      pp.hidden = false;
      pp.addEventListener("click", function () {
        userHeld = !userHeld; hold();
        pp.setAttribute("aria-label", userHeld ? "Play the cut" : "Pause the cut");
      });
    }
    slate.addEventListener("animationend", function (e) {
      if (e.animationName === "ev-fill") next();
    });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        offscreen = !es[0].isIntersecting; hold();
      }, { threshold: 0.35 }).observe(cover);
    }
    d.addEventListener("visibilitychange", hold);
    // a tap on a day, or scrolling into the days, ends the cut: the bar becomes the page's chapter bar
    slate.addEventListener("click", function (e) { if (e.target.closest(".ev-s, .ev-season-k")) end(); });
    window.addEventListener("scroll", function onS() {
      if (window.scrollY > cover.offsetHeight * 0.6) { window.removeEventListener("scroll", onS); end(); }
    }, { passive: true });
  } else {
    root.classList.remove("ev-run");
  }

  /* ---- the chapter bar: the day in view is lit ---- */
  var chs = [].slice.call(d.querySelectorAll(".ev-ch"));
  var links = [].slice.call(slate.querySelectorAll(".ev-s"));
  var current = null;
  function light(id) {
    if (run || id === current) return;
    current = id;
    links.forEach(function (li) {
      var on = li.querySelector("a").getAttribute("href") === "#" + id;
      li.classList.toggle("is-on", on);
      if (on) {
        var ol = li.parentNode, a = li.offsetLeft, b = a + li.offsetWidth;
        if (a < ol.scrollLeft || b > ol.scrollLeft + ol.clientWidth) ol.scrollTo({ left: a - 8, behavior: reduce ? "auto" : "smooth" });
      }
    });
  }
  function spy() {
    var y = (slate.getBoundingClientRect().bottom || 0) + window.innerHeight * 0.25, id = null;
    if (cover.getBoundingClientRect().bottom > window.innerHeight * 0.5) id = "";
    else chs.forEach(function (c) { if (c.getBoundingClientRect().top <= y) id = c.id; });
    if (id === null) id = "";
    light(id);
  }
  var tick = false;
  window.addEventListener("scroll", function () {
    if (tick) return; tick = true;
    requestAnimationFrame(function () { tick = false; spy(); });
  }, { passive: true });
  spy();

  /* ---- the films: play in place, youtube-nocookie, on a tap ---- */
  function play(fr, vid) {
    if (!fr || fr.querySelector("iframe")) return;
    var f = d.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + vid + "?autoplay=1&rel=0&playsinline=1&modestbranding=1";
    f.title = (fr.querySelector(".ev-play") || {}).getAttribute ? fr.querySelector(".ev-play").getAttribute("aria-label") : "Film";
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    fr.innerHTML = ""; fr.appendChild(f);
    f.focus();
  }
  d.addEventListener("click", function (e) {
    var a = e.target.closest(".ev-play");
    if (a) { e.preventDefault(); play(a.closest(".ev-fr"), a.closest(".ev-fr").getAttribute("data-vid")); return; }
    var s = e.target.closest(".ev-strip a");
    if (s) {
      e.preventDefault();
      var fr = s.closest(".ev-film").querySelector(".ev-fr");
      fr.scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" });
      play(fr, s.getAttribute("data-vid"));
    }
  });

  /* ---- the photo viewer ---- */
  var dlg = d.getElementById("evv");
  if (!dlg || !dlg.showModal) return;
  var all = [].slice.call(d.querySelectorAll(".ev-ph a"));
  var img = dlg.querySelector(".evv-stage img"), pos = dlg.querySelector(".evv-pos");
  var nm = dlg.querySelector(".evv-name b"), where = dlg.querySelector(".evv-name span");
  var save = dlg.querySelector(".evv-save"), cur = 0, opener = null;
  var title = (d.querySelector(".ev-h1") || {}).textContent || "";
  function size() { return (window.innerWidth * (window.devicePixelRatio || 1) > 1700) ? 2400 : 1600; }
  function open(i) {
    cur = (i + all.length) % all.length;
    var a = all[cur], stem = a.getAttribute("data-stem"), full = a.getAttribute("href");
    var sheet = a.closest(".ev-sheet"), n = sheet.querySelectorAll(".ev-ph").length;
    img.src = full.replace("-2400.webp", "-" + size() + ".webp");
    img.alt = a.querySelector("img").alt;
    pos.textContent = sheet.getAttribute("data-day") + " · " + a.getAttribute("data-i") + " of " + n;
    nm.textContent = stem;
    where.textContent = title.replace(/\s+/g, " ").trim() + ", " + sheet.getAttribute("data-day");
    save.href = full; save.setAttribute("download", stem + ".webp");
    // the next photo is fetched ahead, so a swipe is instant
    var nx = all[(cur + 1) % all.length]; if (nx) { var p = new Image(); p.src = nx.getAttribute("href").replace("-2400.webp", "-" + size() + ".webp"); }
  }
  all.forEach(function (a, i) {
    a.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault(); opener = a; open(i); dlg.showModal();
    });
  });
  dlg.querySelector(".evv-x").addEventListener("click", function () { dlg.close(); });
  dlg.querySelector(".evv-prev").addEventListener("click", function () { open(cur - 1); });
  dlg.querySelector(".evv-next").addEventListener("click", function () { open(cur + 1); });
  dlg.addEventListener("close", function () {
    img.removeAttribute("src");
    if (opener) { opener.focus({ preventScroll: true }); opener.scrollIntoView({ block: "nearest" }); }
  });
  dlg.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") open(cur + 1);
    else if (e.key === "ArrowLeft") open(cur - 1);
  });
  var x0 = null, y0 = 0;
  dlg.querySelector(".evv-stage").addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
  dlg.querySelector(".evv-stage").addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; x0 = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) open(cur + (dx < 0 ? 1 : -1));
    else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) dlg.close();
  });
})();
