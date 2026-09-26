/* Five ways to show where we fly (prototypes/v4/fly-options.html, built by
   tools/v2_fly_options.py). Each layout wakes only on the visitor's pointer,
   tap, key or scroll; nothing runs while the page is still. */
(function () {
  "use strict";
  var d = document;

  /* 1. wing panels: point at one (or tap, or focus it) and it opens out */
  d.querySelectorAll("[data-fo1]").forEach(function (box) {
    var ps = [].slice.call(box.querySelectorAll(".fo1-p"));
    var fine = matchMedia("(hover:hover) and (pointer:fine) and (min-width:761px)");
    function open(p) {
      ps.forEach(function (q) {
        var on = q === p;
        q.classList.toggle("is-open", on);
        q.querySelector(".fo1-tab").setAttribute("aria-expanded", on ? "true" : "false");
      });
    }
    ps.forEach(function (p) {
      p.querySelector(".fo1-tab").addEventListener("click", function () { open(p); });
      p.addEventListener("pointerenter", function () { if (fine.matches) open(p); });
      p.addEventListener("focusin", function () { open(p); });
    });
  });

  /* 2. fly-through: the step in the middle of the screen picks the picture */
  d.querySelectorAll("[data-fo2]").forEach(function (box) {
    var shots = box.querySelectorAll(".fo2-shot"), alts = box.querySelectorAll("[data-alt]"),
        steps = box.querySelectorAll(".fo2-step");
    function show(i) {
      shots.forEach(function (s, k) { s.classList.toggle("is-on", k === i); });
      alts.forEach(function (s, k) { s.classList.toggle("is-on", k === i); });
      steps.forEach(function (s, k) { s.classList.toggle("is-on", k === i); });
    }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) show(+en.target.getAttribute("data-step")); });
    }, { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach(function (s) { io.observe(s); });
    show(0);
  });

  /* 3. swipe strip: native swipe, plus drag, arrows and keys on desktop */
  d.querySelectorAll("[data-fo3]").forEach(function (box) {
    var rail = box.querySelector(".fo3-rail"), slides = [].slice.call(rail.children),
        count = box.querySelector(".fo3-count b"), bar = box.querySelector(".fo3-prog i"),
        prev = box.querySelector('[data-dir="-1"]'), next = box.querySelector('[data-dir="1"]'), cur = -1;
    function at() {
      var best = 0, bd = Infinity, left = rail.getBoundingClientRect().left;
      slides.forEach(function (s, k) { var dx = Math.abs(s.getBoundingClientRect().left - left - parseFloat(getComputedStyle(rail).paddingLeft)); if (dx < bd) { bd = dx; best = k; } });
      if (rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 4) best = slides.length - 1;
      return best;
    }
    function mark() {
      var i = at(); if (i === cur) return; cur = i;
      slides.forEach(function (s, k) { s.classList.toggle("is-on", k === i); });
      count.textContent = "0" + (i + 1);
      bar.style.width = ((i + 1) / slides.length * 100) + "%";
      prev.disabled = i === 0; next.disabled = i === slides.length - 1;
    }
    function go(i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      rail.scrollTo({ left: slides[i].offsetLeft - slides[0].offsetLeft, behavior: "smooth" });
    }
    var q = false;
    rail.addEventListener("scroll", function () { if (q) return; q = true; requestAnimationFrame(function () { q = false; mark(); }); }, { passive: true });
    prev.addEventListener("click", function () { go(cur - 1); });
    next.addEventListener("click", function () { go(cur + 1); });
    rail.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowRight") { ev.preventDefault(); go(cur + 1); }
      if (ev.key === "ArrowLeft") { ev.preventDefault(); go(cur - 1); }
    });
    // mouse drag (touch already swipes natively)
    var down = false, sx = 0, sl = 0, moved = 0;
    rail.addEventListener("pointerdown", function (ev) {
      if (ev.pointerType !== "mouse" || ev.button) return;
      down = true; moved = 0; sx = ev.clientX; sl = rail.scrollLeft;
    });
    addEventListener("pointermove", function (ev) {
      if (!down) return;
      var dx = ev.clientX - sx; moved = Math.max(moved, Math.abs(dx));
      if (moved > 4) { rail.classList.add("is-drag"); rail.scrollLeft = sl - dx; }
    });
    addEventListener("pointerup", function () {
      if (!down) return; down = false;
      if (rail.classList.contains("is-drag")) {
        rail.classList.remove("is-drag");
        var i = at(); go(i);
      }
    });
    rail.addEventListener("click", function (ev) { if (moved > 4) { ev.preventDefault(); moved = 0; } }, true);
    mark();
  });

  /* 4. departure board: tabs change the stage */
  d.querySelectorAll("[data-fo4]").forEach(function (box) {
    var tabs = [].slice.call(box.querySelectorAll('[role="tab"]')), shots = box.querySelectorAll(".fo4-shot");
    function pick(i, focus) {
      tabs.forEach(function (t, k) {
        var on = k === i;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        d.getElementById(t.getAttribute("aria-controls")).hidden = !on;
        shots[k].classList.toggle("is-on", on);
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { pick(k); });
      t.addEventListener("keydown", function (ev) {
        var n = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[ev.key];
        if (n) { ev.preventDefault(); pick((k + n + tabs.length) % tabs.length, true); }
      });
    });
  });
})();
