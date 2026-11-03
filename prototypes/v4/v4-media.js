/* Media pages (tools/v4_media.py): the photo viewer of the India page (fly.js), the videos played in place
   (youtube-nocookie, loaded only on a tap, as on the home page), and the showreel's list and chips. */
(function () {
  "use strict";
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function ready(f) { if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", f); else f(); }
  ready(function () {

  /* ---------- a video plays where it is ---------- */
  function play(fr) {
    if (!fr || fr.classList.contains("is-on")) return;
    var v = fr.getAttribute("data-vid"), f = document.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + v + "?autoplay=1&rel=0&playsinline=1&modestbranding=1";
    f.title = (fr.querySelector(".md-play") || {}).getAttribute ? fr.querySelector(".md-play").getAttribute("aria-label") : "Video";
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen"; f.allowFullscreen = true;
    fr.appendChild(f); fr.classList.add("is-on");
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".md-play");
    if (a && !document.documentElement.hasAttribute("data-md-out")) { e.preventDefault(); play(a.closest(".md-frame")); }
  });

  /* ---------- a poster that holds an example: the showreel plays it where it is ---------- */
  document.addEventListener("click", function (e) {
    var p = e.target.closest && e.target.closest(".md-poster[data-play]"); if (!p) return;
    var fr = document.querySelector('.md-main .md-frame[data-vid="' + p.getAttribute("data-play") + '"]'); if (!fr) return;
    e.preventDefault();
    fr.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "center" });
    if (!document.documentElement.hasAttribute("data-md-out")) play(fr);
  });

  /* ---------- the showreel: the list loads a video into the big frame; the chips filter by comp ---------- */
  var reel = document.querySelector(".md-reel");
  if (reel) {
    var main = reel.querySelector(".md-main"), list = [].slice.call(reel.querySelectorAll(".md-list li")), chips = [].slice.call(reel.querySelectorAll(".v2-chip"));
    reel.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest(".md-list button"); if (!b) return;
      var v = b.getAttribute("data-vid"), fr = main.querySelector(".md-frame"), nf = fr.cloneNode(false);
      nf.setAttribute("data-vid", v); nf.className = "md-frame";
      var img = document.createElement("img"); img.src = "https://i.ytimg.com/vi/" + v + "/maxresdefault.jpg"; img.alt = ""; img.width = 1280; img.height = 720; nf.appendChild(img);
      var pa = fr.querySelector(".md-play").cloneNode(true), t = b.querySelector("b").textContent, sm = b.querySelector("small").textContent.split(" · ");
      pa.href = "https://www.youtube.com/watch?v=" + v; pa.setAttribute("aria-label", "Play " + t + ", " + sm[0]); nf.appendChild(pa);
      fr.parentNode.replaceChild(nf, fr);
      main.querySelector("h3").textContent = sm[0] + ", " + t;
      var ps = main.querySelectorAll(".md-now p > span"); ps[0].textContent = sm.slice(1).join(" · "); ps[1].textContent = b.getAttribute("data-date") || "";
      var ep = main.querySelector(".md-ep"), eu = b.getAttribute("data-ep"); if (ep) { ep.hidden = !eu; if (eu) ep.querySelector("a").href = eu; }
      list.forEach(function (li) { var bb = li.querySelector("button"); if (bb === b) bb.setAttribute("aria-current", "true"); else bb.removeAttribute("aria-current"); });
      if (!document.documentElement.hasAttribute("data-md-out")) play(nf);   // a preview without a player opens YouTube from the button
      var r = nf.getBoundingClientRect(); if (r.top < 0 || r.bottom > innerHeight) nf.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "center" });
    });
    function only(c) {
      chips.forEach(function (ch) { ch.setAttribute("aria-pressed", String((ch.getAttribute("data-comp") || "") === c)); });
      list.forEach(function (li) { li.hidden = !!c && li.getAttribute("data-comp") !== c; });
    }
    chips.forEach(function (ch) { ch.addEventListener("click", function () { only(ch.getAttribute("data-comp") || ""); }); });
    document.addEventListener("click", function (e) {      // a comp card opens the showreel on that comp
      var a = e.target.closest && e.target.closest('a[href="#watch"][data-comp]'); if (a) only(a.getAttribute("data-comp"));
    });
  }

  /* ---------- the stills in justified rows: every frame whole, the rows as even as they can be ---------- */
  [].slice.call(document.querySelectorAll(".md-grid")).forEach(function (g) {
    var figs = [].slice.call(g.querySelectorAll(".md-ph")), rs = figs.map(function (f) { return parseFloat(f.style.getPropertyValue("--r")) || 1.5; }), lastW = 0;
    function lay() {
      var W = g.clientWidth; if (!W || W === lastW) return; lastW = W;
      var gap = parseFloat(getComputedStyle(g).columnGap) || 8, t = W < 700 ? 150 : Math.max(150, Math.min(270, W * .19)), n = rs.length, best = [0], cut = [0];
      for (var j = 1; j <= n; j++) {
        best[j] = Infinity;
        for (var i = j - 1, sum = 0; i >= 0; i--) {
          sum += rs[i]; var h = (W - gap * (j - i - 1)) / sum; if (h < t * .45) break;
          var c = best[i] + Math.pow(h - t, 2) * (j === n && h > t ? .35 : 1); if (c < best[j]) { best[j] = c; cut[j] = i; }
        }
      }
      var rows = [], j2 = n; while (j2 > 0) { rows.unshift([cut[j2], j2]); j2 = cut[j2]; }
      rows.forEach(function (rw) {
        var sum = 0, k; for (k = rw[0]; k < rw[1]; k++) sum += rs[k];
        var room = W - gap * (rw[1] - rw[0] - 1), h = room / sum, last = rw[1] === n && h > t * 1.35 && n > 1;
        if (last) h = t * 1.35;
        var used = 0; for (k = rw[0]; k < rw[1]; k++) { var w = (k === rw[1] - 1 && !last) ? room - used : Math.floor(rs[k] * h); figs[k].style.width = w + "px"; used += w; }
      });
      g.classList.add("is-js");
    }
    lay(); window.addEventListener("resize", lay);
    if (window.ResizeObserver) new ResizeObserver(lay).observe(g);
  });

  /* ---------- the viewer: a photograph floating on the dimmed page; tap to come closer, pinch, drag, arrows (fly.js) ---------- */
  var lb = document.getElementById("v4i-fl-lb"); if (!lb) return;
  var lbImg = lb.querySelector("img"), lbStage = lb.querySelector(".v4i-fl-lbs"), lbCap = lb.querySelector(".v4i-fl-lbc");
  var lbPrev = lb.querySelector(".v4i-fl-lbp"), lbNext = lb.querySelector(".v4i-fl-lbnx");
  var Z = { s: 1, x: 0, y: 0, ptrs: {}, pinch: null, moved: 0, closing: 0, set: [], i: 0 };
  function lbApply() { lbImg.style.transform = (lb.classList.contains("is-in") ? "" : "scale(.96) ") + "translate(" + Z.x.toFixed(1) + "px," + Z.y.toFixed(1) + "px) scale(" + Z.s.toFixed(3) + ")"; lb.classList.toggle("is-zoomed", Z.s > 1.01); }
  function lbClampPan() {
    var iw = lbImg.clientWidth, ih = lbImg.clientHeight, sw = lbStage.clientWidth, sh = lbStage.clientHeight;
    var mx = Math.max(0, (iw * Z.s - sw) / 2 + 24), my = Math.max(0, (ih * Z.s - sh) / 2 + 24);
    if (iw * Z.s <= sw) mx = 0; if (ih * Z.s <= sh) my = 0; Z.x = clamp(Z.x, -mx, mx); Z.y = clamp(Z.y, -my, my);
  }
  function lbZoomAt(k, cx, cy) {
    var r = lbStage.getBoundingClientRect(), px = cx - (r.left + r.width / 2), py = cy - (r.top + r.height / 2), s1 = clamp(Z.s * k, 1, 6), ratio = s1 / Z.s;
    Z.x = px - ratio * (px - Z.x); Z.y = py - ratio * (py - Z.y); Z.s = s1; if (Z.s <= 1.001) { Z.x = Z.y = 0; } lbClampPan(); lbApply();
  }
  function lbShow(a) {
    var im = a.querySelector("img"), fig = a.closest("figure"), cap = fig && fig.querySelector("figcaption b");
    Z.s = 1; Z.x = Z.y = 0; lb.classList.remove("is-zoomed", "is-drag");
    lbImg.src = im.currentSrc || im.src; var big = a.getAttribute("data-full");           // the shown copy first, the large one as soon as it is in
    if (big) { var pre = new Image(); pre.onload = function () { if (Z.set[Z.i] === a) lbImg.src = big; }; pre.src = big; }
    lbImg.alt = im.alt || "";
    if (lbCap) { lbCap.textContent = cap ? cap.textContent : ""; if (Z.set.length > 1) { var k = document.createElement("span"); k.className = "v4i-fl-lbi"; k.textContent = (Z.i + 1) + " / " + Z.set.length; lbCap.appendChild(k); } }
    lbPrev.hidden = Z.i <= 0; lbNext.hidden = Z.i >= Z.set.length - 1;
    lbApply();
  }
  function lbOpen(a, set) {
    Z.set = set; Z.i = Math.max(0, set.indexOf(a)); Z.ptrs = {}; Z.pinch = null; lb.classList.remove("is-in"); lbImg.style.transform = "";
    lbShow(a);
    if (lb.showModal) lb.showModal(); else lb.setAttribute("open", "");
    requestAnimationFrame(function () { requestAnimationFrame(function () { lb.classList.add("is-in"); lbApply(); }); });
  }
  function lbGo(d) {
    var j = Z.i + d; if (!lb.open || j < 0 || j >= Z.set.length) return; Z.i = j;
    lbImg.style.opacity = "0";
    setTimeout(function () { lbShow(Z.set[Z.i]); var done = function () { lbImg.style.opacity = ""; }; if (lbImg.complete) done(); else { lbImg.onload = done; setTimeout(done, 900); } }, 160);
  }
  function lbClose() {
    if (!lb.open || Z.closing) return; Z.closing = 1; lb.classList.remove("is-in");
    setTimeout(function () { if (lb.open) lb.close(); lbImg.removeAttribute("src"); lb.classList.remove("is-zoomed", "is-drag"); Z.closing = 0; }, 220);
  }
  [].slice.call(document.querySelectorAll("[data-zoom]")).forEach(function (g) {
    var set = [].slice.call(g.querySelectorAll("a[data-full]"));
    set.forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); lbOpen(a, set); }); });
  });
  lbPrev.addEventListener("click", function (e) { e.stopPropagation(); lbGo(-1); if (lbPrev.hidden) lb.focus(); });
  lbNext.addEventListener("click", function (e) { e.stopPropagation(); lbGo(1); if (lbNext.hidden) lb.focus(); });
  lb.addEventListener("cancel", function (e) { e.preventDefault(); lbClose(); });
  lb.querySelector(".v4i-fl-lbx").addEventListener("click", function (e) { e.stopPropagation(); lbClose(); });
  lb.addEventListener("click", function (e) {
    if (e.target.closest(".v4i-fl-lbx, .v4i-fl-lbn")) return;
    if (Z.moved > 6) { Z.moved = 0; return; }
    var r = lbImg.getBoundingClientRect(), onImg = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
    if (onImg) { var next = Z.s < 1.5 ? 2 : Z.s < 3 ? 3.5 : 1; lbZoomAt(next / Z.s, e.clientX, e.clientY); return; }
    lbClose();
  });
  lb.addEventListener("wheel", function (e) { e.preventDefault(); lbZoomAt(Math.exp(-clamp(e.deltaY, -80, 80) * 0.004), e.clientX, e.clientY); }, { passive: false });
  lbStage.addEventListener("pointerdown", function (e) {
    Z.ptrs[e.pointerId] = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY }; var ids = Object.keys(Z.ptrs); Z.moved = 0;
    if (ids.length === 2) { var A = Z.ptrs[ids[0]], B = Z.ptrs[ids[1]]; Z.pinch = { span: Math.hypot(A.x - B.x, A.y - B.y), cx: (A.x + B.x) / 2, cy: (A.y + B.y) / 2 }; }
    if (lbStage.setPointerCapture) lbStage.setPointerCapture(e.pointerId); if (e.target === lbImg && Z.s > 1.01) lb.classList.add("is-drag"); e.preventDefault();
  });
  lbStage.addEventListener("pointermove", function (e) {
    var p = Z.ptrs[e.pointerId]; if (!p) return; var dx = e.clientX - p.x, dy = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY; Z.moved += Math.abs(dx) + Math.abs(dy);
    var ids = Object.keys(Z.ptrs);
    if (ids.length >= 2 && Z.pinch) {
      var A = Z.ptrs[ids[0]], B = Z.ptrs[ids[1]], span = Math.hypot(A.x - B.x, A.y - B.y), cx = (A.x + B.x) / 2, cy = (A.y + B.y) / 2;
      if (Z.pinch.span > 0) lbZoomAt(span / Math.max(1, Z.pinch.span), cx, cy);
      Z.x += cx - Z.pinch.cx; Z.y += cy - Z.pinch.cy; Z.pinch.span = span; Z.pinch.cx = cx; Z.pinch.cy = cy; lbClampPan(); lbApply(); return;
    }
    if (Z.s > 1.01) { Z.x += dx; Z.y += dy; lbClampPan(); lbApply(); }
  });
  function lbUp(e) {
    var p = Z.ptrs[e.pointerId]; delete Z.ptrs[e.pointerId]; var ids = Object.keys(Z.ptrs); if (ids.length < 2) Z.pinch = null; lb.classList.remove("is-drag");
    if (p && !ids.length && Z.s <= 1.01 && !Z.pinch) { var dx = e.clientX - p.sx, dy = e.clientY - p.sy; if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) { Z.moved = 99; lbGo(dx < 0 ? 1 : -1); } }
  }
  lbStage.addEventListener("pointerup", lbUp); lbStage.addEventListener("pointercancel", lbUp);
  document.addEventListener("keydown", function (e) { if (!lb.open) return; if (e.key === "+" || e.key === "=") lbZoomAt(1.3, innerWidth / 2, innerHeight / 2); else if (e.key === "-") lbZoomAt(1 / 1.3, innerWidth / 2, innerHeight / 2); else if (e.key === "0") lbZoomAt(1 / Z.s, 0, 0); else if (e.key === "ArrowRight") { e.preventDefault(); lbGo(1); } else if (e.key === "ArrowLeft") { e.preventDefault(); lbGo(-1); } });
  });
})();
