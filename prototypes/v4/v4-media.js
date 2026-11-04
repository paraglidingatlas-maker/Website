/* Media pages (tools/v4_media.py), shared by media.html and the event pages.
   On every media page: the videos play where they are (youtube-nocookie, loaded only on a tap, as on the home page;
   in the claude.ai preview, html[data-md-out], a play button opens YouTube instead), the showreel's list and chips, the
   stills in justified rows, and the photo viewer of the India page (fly.js).
   On media.html (designer E, "Pull Back To The Coverage", docs/designers/media-build-spec.md):
     the slate counts down to the next comp, lights "On air now" during its task days, and drops the countdown after (H3);
     the pull-back: the first screen is one shot of a race; scrolling pulls the camera back until that shot is the second
       of four posters, the other three sliding in under it, the board's words showing once the shot has cleared them;
       the shot is the Daily Highlights link at every stage; on a touch screen a stop between the two ends finishes the
       move (P1 to P4). Scroll drives it both ways; nothing moves on its own; reduced motion and no JavaScript show the
       finished page;
     every Check dates and every package a poster names picks that package in the form (K2); an open month of 2027 fills
       the dates (S1); the form hands the name and email over in sessionStorage, never in the address bar (S3);
     the phone bar shows only when no other orange button is on screen (S4). */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  var OUT = root.hasAttribute("data-md-out");
  function mm(q) { return !!(w.matchMedia && w.matchMedia(q).matches); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function band(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
  function inout(t) { return -(Math.cos(Math.PI * t) - 1) / 2; }
  function out3(t) { return 1 - Math.pow(1 - t, 3); }
  function reduced() { return mm("(prefers-reduced-motion: reduce)"); }
  function smooth() { return reduced() ? "auto" : "smooth"; }
  function ready(f) { if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", f); else f(); }
  root.classList.add("md-js");

  /* ---------------------------------------------------------------- the videos and the showreel ---- */
  var R = { pick: function () { return false; }, comp: function () {} };
  function reel() {
    function play(fr) {
      if (!fr || fr.classList.contains("is-on")) return;
      var v = fr.getAttribute("data-vid"), f = d.createElement("iframe"), a = fr.querySelector(".md-play");
      f.src = "https://www.youtube-nocookie.com/embed/" + v + "?autoplay=1&rel=0&playsinline=1&modestbranding=1";
      f.title = a ? a.getAttribute("aria-label") : "Video";
      f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";      // the allow list grants fullscreen (qa-2-6)
      fr.appendChild(f); fr.classList.add("is-on");
    }
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest(".md-play");
      if (a && !OUT) { e.preventDefault(); play(a.closest(".md-frame")); }
    });
    var box = d.querySelector(".md-reel"); if (!box) return;
    var main = box.querySelector(".md-main"), list = [].slice.call(box.querySelectorAll(".md-list li")), chips = [].slice.call(box.querySelectorAll(".v2-chip"));
    function bring(el) { var r = el.getBoundingClientRect(); if (r.top < 0 || r.bottom > innerHeight) el.scrollIntoView({ behavior: smooth(), block: "center" }); }
    // the list loads a video into the big frame
    function load(b) {
      var v = b.getAttribute("data-vid"), fr = main.querySelector(".md-frame");
      if (fr.getAttribute("data-vid") !== v) {
        var nf = fr.cloneNode(false); nf.setAttribute("data-vid", v); nf.className = "md-frame";
        var img = d.createElement("img"); img.src = b.getAttribute("data-still"); img.alt = ""; img.width = 1280; img.height = 720; img.decoding = "async"; nf.appendChild(img);
        var pa = fr.querySelector(".md-play").cloneNode(true);
        pa.href = "https://www.youtube.com/watch?v=" + v; pa.setAttribute("aria-label", "Play " + b.getAttribute("data-title") + ", " + b.getAttribute("data-comp-name"));
        nf.appendChild(pa); fr.parentNode.replaceChild(nf, fr); fr = nf;
        // the title as the list sets it: the film, then its comp on a quieter line (critic-1-6)
        var ht = main.querySelector("[data-t]"), hc = main.querySelector("[data-c]");
        if (ht && hc) { ht.textContent = b.getAttribute("data-title"); hc.textContent = b.getAttribute("data-comp-name"); }
        else main.querySelector("h3").textContent = b.getAttribute("data-comp-name") + ", " + b.getAttribute("data-title");
        var m = main.querySelector("[data-m]"), ml = main.querySelector("[data-l]"), dt = main.querySelector("[data-d]"), ep = main.querySelector(".md-ep"), eu = b.getAttribute("data-ep");
        if (m) m.textContent = b.getAttribute("data-views");
        if (ml) ml.textContent = b.getAttribute("data-len");
        if (dt) dt.textContent = b.getAttribute("data-date") || "";
        if (ep) { ep.hidden = !eu; if (eu) ep.querySelector("a").href = eu; }
      }
      list.forEach(function (li) { var bb = li.querySelector("button"); if (bb === b) bb.setAttribute("aria-current", "true"); else bb.removeAttribute("aria-current"); });
      return fr;
    }
    function pick(b) { var fr = load(b); if (!OUT) play(fr); bring(fr); }    // the preview has no player: its button opens YouTube
    box.addEventListener("click", function (e) { var b = e.target.closest && e.target.closest(".md-list button"); if (b) pick(b); });
    function only(c) {
      chips.forEach(function (ch) { ch.setAttribute("aria-pressed", String((ch.getAttribute("data-comp") || "") === c)); });
      list.forEach(function (li) { li.hidden = !!c && li.getAttribute("data-comp") !== c; });
    }
    chips.forEach(function (ch) { ch.addEventListener("click", function () { only(ch.getAttribute("data-comp") || ""); }); });
    R.pick = function (v) { var b = box.querySelector('.md-list button[data-vid="' + v + '"]'); if (!b) return false; pick(b); return true; };
    R.comp = function (c) { only(c); var li = list.filter(function (x) { return x.getAttribute("data-comp") === c; })[0]; if (li) pick(li.querySelector("button")); };
    // a poster or the opening's shot holds an example: it plays here; a Watch on the season opens the showreel on that comp
    d.addEventListener("click", function (e) {
      var t = e.target.closest && e.target.closest('[data-play], a[href="#watch"][data-comp]'); if (!t) return;
      if (t.hasAttribute("data-play")) { if (R.pick(t.getAttribute("data-play"))) e.preventDefault(); }
      else { e.preventDefault(); R.comp(t.getAttribute("data-comp")); }
    });
  }

  /* ---------------------------------------------------------------- the stills in justified rows ---- */
  function rows() {
    [].slice.call(d.querySelectorAll(".md-grid")).forEach(function (g) {
      var figs = [].slice.call(g.querySelectorAll(".md-ph")), rs = figs.map(function (f) { return parseFloat(f.style.getPropertyValue("--r")) || 1.5; }), lastW = 0;
      function lay() {
        // the grid's own width to the fraction (clientWidth rounds it: 921.625 read as 922 at 1024 wide wrapped each
        // row's last frame), a hair under it so the browser's sub-pixel rounding never wraps one either
        var W = (parseFloat(getComputedStyle(g).width) || g.clientWidth) - .05; if (W <= 0 || Math.abs(W - lastW) < .01) return; lastW = W;
        var gap = parseFloat(getComputedStyle(g).columnGap) || 8, t = W < 700 ? 150 : Math.max(150, Math.min(270, W * .19)), n = rs.length, best = [0], cut = [0];
        for (var j = 1; j <= n; j++) {
          best[j] = Infinity;
          for (var i = j - 1, sum = 0; i >= 0; i--) {
            sum += rs[i]; var h = (W - gap * (j - i - 1)) / sum; if (h < t * .45) break;
            var c = best[i] + Math.pow(h - t, 2) * (j === n && h > t ? .35 : 1); if (c < best[j]) { best[j] = c; cut[j] = i; }
          }
        }
        var rws = [], j2 = n; while (j2 > 0) { rws.unshift([cut[j2], j2]); j2 = cut[j2]; }
        rws.forEach(function (rw) {
          var sum = 0, k; for (k = rw[0]; k < rw[1]; k++) sum += rs[k];
          var room = W - gap * (rw[1] - rw[0] - 1), h = room / sum, last = rw[1] === n && h > t * 1.35 && n > 1;
          if (last) h = t * 1.35;
          // whole pixels that still add up to the row (so nothing wraps), each frame within half a pixel of its own
          // width, and one height for the whole row, so every frame in it shares its top and its foot; the photo covers
          // its box, so the rounding crops under a pixel instead of stepping the row's foot (critic-3-2)
          var acc = 0, prev = 0, hh = Math.round(h);
          for (k = rw[0]; k < rw[1]; k++) {
            acc += rs[k] * h;
            var edge = (k === rw[1] - 1 && !last) ? room : Math.round(acc);
            figs[k].style.width = (edge - prev) + "px"; figs[k].style.height = hh + "px"; prev = edge;
          }
        });
        g.classList.add("is-js");
      }
      lay(); w.addEventListener("resize", lay);
      if (w.ResizeObserver) new ResizeObserver(lay).observe(g);
    });
  }

  /* ---------------------------------------------------------------- the viewer (fly.js): tap to come closer, pinch, drag, arrows ---- */
  function viewer() {
    var lb = d.getElementById("v4i-fl-lb"); if (!lb) return;
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
      if (lbCap) { lbCap.textContent = cap ? cap.textContent : ""; if (Z.set.length > 1) { var k = d.createElement("span"); k.className = "v4i-fl-lbi"; k.textContent = (Z.i + 1) + " / " + Z.set.length; lbCap.appendChild(k); } }
      lbPrev.hidden = Z.i <= 0; lbNext.hidden = Z.i >= Z.set.length - 1;
      lbApply();
    }
    function lbOpen(a, set) {
      Z.set = set; Z.i = Math.max(0, set.indexOf(a)); Z.ptrs = {}; Z.pinch = null; lb.classList.remove("is-in"); lbImg.style.transform = "";
      lbShow(a);
      if (lb.showModal) lb.showModal(); else lb.setAttribute("open", "");
      requestAnimationFrame(function () { requestAnimationFrame(function () { lb.classList.add("is-in"); lbApply(); }); });
    }
    function lbGo(k) {
      var j = Z.i + k; if (!lb.open || j < 0 || j >= Z.set.length) return; Z.i = j;
      lbImg.style.opacity = "0";
      setTimeout(function () { lbShow(Z.set[Z.i]); var done = function () { lbImg.style.opacity = ""; }; if (lbImg.complete) done(); else { lbImg.onload = done; setTimeout(done, 900); } }, 160);
    }
    function lbClose() {
      if (!lb.open || Z.closing) return; Z.closing = 1; lb.classList.remove("is-in");
      setTimeout(function () { if (lb.open) lb.close(); lbImg.removeAttribute("src"); lb.classList.remove("is-zoomed", "is-drag"); Z.closing = 0; }, 220);
    }
    [].slice.call(d.querySelectorAll("[data-zoom]")).forEach(function (g) {
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
    d.addEventListener("keydown", function (e) { if (!lb.open) return; if (e.key === "+" || e.key === "=") lbZoomAt(1.3, innerWidth / 2, innerHeight / 2); else if (e.key === "-") lbZoomAt(1 / 1.3, innerWidth / 2, innerHeight / 2); else if (e.key === "0") lbZoomAt(1 / Z.s, 0, 0); else if (e.key === "ArrowRight") { e.preventDefault(); lbGo(1); } else if (e.key === "ArrowLeft") { e.preventDefault(); lbGo(-1); } });
  }

  /* ---------------------------------------------------------------- the slate and the season's next comp (H3) ---- */
  function slate() {
    var up = [];
    try { up = JSON.parse((d.getElementById("md-up") || {}).textContent || "[]"); } catch (err) {}
    var now = new Date(), today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    function at(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
    var ev = null, state = "none";
    for (var i = 0; i < up.length; i++) if (at(up[i].last) >= today) { ev = up[i]; break; }
    if (ev) state = today < at(ev.first) ? "next" : "now";
    var el = d.querySelector("[data-slate]");
    if (el) {
      var k = el.querySelector("[data-slate-k]"), e1 = el.querySelector("[data-slate-e]"), nn = el.querySelector("[data-slate-n]");
      el.setAttribute("data-state", state);
      if (!ev) { k.textContent = "Next"; e1.innerHTML = '<i class="v2-tbd">[to supply]</i>'; nn.textContent = ""; }
      else {
        e1.textContent = ev.name + ", " + ev.place + " · " + ev.dates;
        if (state === "now") { k.textContent = "On air now"; nn.textContent = ""; }
        else { var n = Math.round((at(ev.first) - today) / 864e5); k.textContent = "Next"; nn.textContent = n === 1 ? "Tomorrow" : "In " + n + " days"; }
      }
    }
    // the season line: the next comp lit while it is on air, Today where the visitor is
    var se = d.querySelector(".e-season"); if (!se) return;
    var row = se.querySelector("[data-up-row]"), rk = row && row.querySelector("[data-up-k]");
    se.setAttribute("data-state", state);
    if (row) row.setAttribute("data-state", state);
    if (rk) rk.textContent = state === "now" ? "On air now" : state === "next" ? "Next" : "Latest";
    var tl = se.querySelector(".e-tl"), td = se.querySelector("[data-today]");
    if (tl && td && tl.getAttribute("data-from")) {
      var s0 = at(tl.getAttribute("data-from")), s1 = at(tl.getAttribute("data-to"));
      if (today >= s0 && today < s1) { td.style.setProperty("--x", ((today - s0) / (s1 - s0)).toFixed(4)); td.hidden = false; }
    }
  }

  /* ---------------------------------------------------------------- the pull-back (P1 to P4) ---- */
  function pull() {
    var wrap = d.querySelector(".e-pull"); if (!wrap) return;
    var stage = wrap.querySelector(".e-stage"), hero = stage.querySelector(".e-hero"), cam = hero.querySelector(".e-cam"),
        img = cam.querySelector(".e-cam-img"), shade = cam.querySelector(".e-shade"), lab = cam.querySelector(".e-cam-lab"), foot = cam.querySelector(".e-cam-foot"),
        tal = cam.querySelector(".e-cam-tally"), hin = hero.querySelector(".e-hero-in"), four = stage.querySelector(".e-four"),
        fin = four.querySelector(".e-four-in"), rail = four.querySelector(".e-posters"), items = [].slice.call(four.querySelectorAll(".e-pl")),
        slotLi = four.querySelector(".e-pl.is-cam"), slot = slotLi.querySelector(".e-poster"),
        others = items.filter(function (li) { return li !== slotLi; }),
        fades = [four.querySelector(".e-four-head"), slotLi.querySelector(".e-when"), slotLi.querySelector(".e-in"), four.querySelector(".e-four-note")];
    var A = 1600 / 2400;              // the shot's own shape: SRS_5_T2_133-2 is portrait
    var on = false, G = {}, P = -1, raf = 0, lastW = 0, lastH = 0;

    function can() { return !reduced() && w.CSS && CSS.supports("position", "sticky") && CSS.supports("clip-path", "inset(0px 0px 0px 0px round 4px)"); }
    function clear() {
      [img, cam, shade, hin, lab, foot, tal].forEach(function (el) { el.removeAttribute("style"); });
      items.forEach(function (li) { li.style.transform = li.style.opacity = li.style.webkitMaskImage = li.style.maskImage = li.style.clipPath = ""; li.style.removeProperty("--e-co"); });
      fades.forEach(function (f) { if (f) { f.style.opacity = f.style.visibility = f.style.pointerEvents = ""; } });
      rail.style.overflowX = "";
    }
    function rect(x, y, wd, ht) { return { x: x, y: y, w: wd, h: ht }; }
    // how far the shot's frame is from an element: more than 0 once they no longer touch
    function gapTo(o, x, y, fw, fh) { return Math.max(y - (o.y + o.h), o.y - (y + fh), x - (o.x + o.w), o.x - (x + fw)); }
    // the shot's frame at a point of the move (the same easing as render)
    function frameAt(p) { var e = inout(band(p, .035, .9)); return rect(e * G.sx, e * G.sy, lerp(G.W, G.sw, e), lerp(G.H, G.sh, e)); }
    // how far a card still at the start of its slide reaches out from under the frame f (its part on screen only)
    function outside(o, f) {
      var l = Math.max(0, o.x + o.dx), r = Math.min(G.W, o.x + o.dx + o.w), t = Math.max(0, o.y + o.dy), b = Math.min(G.H, o.y + o.dy + o.h);
      if (r <= l || b <= t) return 0;
      return Math.max(0, f.x - l, r - (f.x + f.w), f.y - t, b - (f.y + f.h));
    }
    var V = .12;                      // the label is on: from here the other three may show
    // on a phone the frame ends where the lifted photo ends (critic-3-1), so the board's pieces below that line are kept
    // unseen by a mask that fades each out along the photo's own feather (a to b, in the stage's coordinates); a piece
    // the shot has come down over, or the finished board (a = b = 0), has none
    // a mask is only paint: a tap would still reach the unseen part, so the same line also clips it (no ghost taps, P1)
    function feather(a, b) {
      G.rows.forEach(function (o) {
        var t = o.y + (o.gy || 0), m = "", c = "";
        if (b && b - t < o.h) {
          m = "linear-gradient(180deg,#000 " + (a - t).toFixed(1) + "px,transparent " + (b - t).toFixed(1) + "px)";
          c = "inset(0px 0px " + Math.max(0, o.h - (b - t)).toFixed(1) + "px 0px)";
        }
        if (o.m !== m) { o.li.style.webkitMaskImage = o.li.style.maskImage = m; o.li.style.clipPath = c; o.m = m; }
      });
    }

    function measure() {
      clear();
      var H = stage.clientHeight, W = stage.clientWidth;
      G.W = W; G.H = H; G.phone = W <= 700; G.tab = W > 700 && W <= 900;
      G.top = Math.round(wrap.getBoundingClientRect().top + w.scrollY);           // the nav sits above the opening
      root.style.setProperty("--e-nav", G.top + "px");
      // the opening's words must fit the screen, below the nav
      var hs = getComputedStyle(hin), need = hin.offsetHeight - (parseFloat(hs.paddingTop) || 0) + 12;
      if (need > H) return false;
      // the posters as big as the screen allows, the whole board inside the frame
      var fs = getComputedStyle(four), padT = parseFloat(fs.paddingTop) || 0, padB = parseFloat(fs.paddingBottom) || 0;
      var gap = parseFloat(getComputedStyle(rail).columnGap) || 12, cw = fin.clientWidth;
      var pw = G.phone ? Math.min(280, W * .74) : G.tab ? (cw - gap) / 2 : (cw - 3 * gap) / 4;
      four.style.setProperty("--e-pw", pw.toFixed(1) + "px");
      var rowsN = G.tab ? 2 : 1, ph = slot.getBoundingClientRect().height, fixed = fin.getBoundingClientRect().height - rowsN * ph;
      pw = Math.min(pw, (H - padT - padB - fixed) / rowsN * .75);
      if (pw < 150) return false;                                                 // too short a screen: the finished page instead
      four.style.setProperty("--e-pw", pw.toFixed(1) + "px");
      // on a phone the rail rests with the shot's poster in the middle, its neighbours either side
      if (G.phone) {
        var lr = slotLi.getBoundingClientRect(), rr = rail.getBoundingClientRect();
        G.home = Math.max(0, Math.round(rail.scrollLeft + (lr.left + lr.width / 2) - (rr.left + rr.width / 2)));
        rail.scrollLeft = G.home;
      }
      var sr = stage.getBoundingClientRect(), r = slot.getBoundingClientRect(), tr = slot.querySelector(".e-p-tally").getBoundingClientRect();
      G.sx = r.left - sr.left; G.sy = r.top - sr.top; G.sw = r.width; G.sh = r.height;
      G.tx = r.right - tr.left; G.ty = tr.top - r.top;
      // the dark foot runs 2px past the frame's foot, so the clip cuts it and no last row of the photo shows under it
      lab.style.width = G.sw.toFixed(1) + "px"; lab.style.height = G.sh.toFixed(1) + "px"; foot.style.height = (G.sh + 2).toFixed(1) + "px";
      // the photo moves from the opening's frame (r0) to its poster's crop (r1), both in the stage's coordinates. Wide:
      // the shot covers the screen, the wing right of centre. Phone: the static page's own frame, the shot as wide as the
      // screen and lifted by --e-lift so the wing sits under the nav, its foot feathered into the ground (critic-1-5)
      G.lift = G.phone ? (parseFloat(getComputedStyle(img).getPropertyValue("--e-lift")) || 0) : 0;
      if (G.lift) G.r0 = rect(0, -G.lift * W / A, W, W / A);
      else { var hb = Math.max(H, W / A), wb = hb * A; G.r0 = rect((W - wb) * .6, (H - hb) * .47, wb, hb); }
      var h1 = Math.max(G.sh, G.sw / A);
      G.r1 = rect(G.sx + (G.sw - h1 * A) * .5, G.sy + (G.sh - h1) * .3, h1 * A, h1);
      G.bw = G.r0.w; G.bh = G.r0.h;
      img.style.setProperty("--e-bw", G.bw.toFixed(1) + "px"); img.style.setProperty("--e-bh", G.bh.toFixed(1) + "px");
      // the lifted shot reaches the frame's foot at G.ec; until then its feather stays, after it the feather recedes
      var a0 = G.r0.y + G.r0.h - H, b0 = G.r1.y + G.r1.h - (G.sy + G.sh);
      G.ec = G.lift && a0 < 0 && b0 > 0 ? a0 / (a0 - b0) : 0;
      // the scroll the move takes: it starts once the nav has gone and the stage is pinned (the first scroll is a plain
      // one, and on a short phone it brings up the three numbers), and ends within 0.8 of a screen from the top (P4)
      G.S = Math.round(G.phone ? Math.max(G.top + H * .45, H * .8) : G.top + H * .82);
      wrap.style.setProperty("--e-travel", Math.max(0, G.S - G.top) + "px");
      G.snap = G.phone || mm("(pointer: coarse)");
      // the other three come in under the shot, in event order, never from beyond the screen's edge; their words wait
      // until the shot has cleared them (critic-1-1). Whenever they show they are opaque (P2, qa-2-2): at V each lies
      // wholly under the shot, its slide trimmed until it does, so the shrinking frame uncovers it; nothing fades in
      // over the ground. One the frame has uncovered sooner (a short screen) shows sooner, while it is still covered
      var fv = frameAt(V);
      G.others = others.map(function (li, i) {
        var q = li.getBoundingClientRect(), cx = q.left + q.width / 2 - (r.left + r.width / 2), cy = q.top + q.height / 2 - (r.top + r.height / 2);
        var room = Math.max(0, cx < 0 ? q.left - sr.left : sr.right - q.right);
        var o = { li: li, x: q.left - sr.left, y: q.top - sr.top, w: q.width, h: q.height, a: .15 + i * .05,
                  dx: Math.sign(cx) * Math.min(G.phone ? 64 : 140, Math.abs(cx) * .3, room), dy: Math.sign(cy) * Math.min(90, Math.abs(cy) * .25) };
        if (o.dx < 0) o.dx = Math.min(0, Math.max(o.dx, fv.x - o.x)); else if (o.dx > 0) o.dx = Math.max(0, Math.min(o.dx, fv.x + fv.w - o.x - o.w));
        if (o.dy < 0) o.dy = Math.min(0, Math.max(o.dy, fv.y - o.y)); else if (o.dy > 0) o.dy = Math.max(0, Math.min(o.dy, fv.y + fv.h - o.y - o.h));
        o.v = V;
        if (outside(o, fv) > 1.5) {
          for (var lo = .035, hi = V, k = 0; k < 12; k++) { var md = (lo + hi) / 2; if (outside(o, frameAt(md)) > 1.5) hi = md; else lo = md; }
          o.v = lo;
        }
        o.fin = gapTo(o, G.sx, G.sy, G.sw, G.sh);
        return o;
      });
      var sq = slotLi.getBoundingClientRect();
      G.rows = G.others.concat([{ li: slotLi, y: sq.top - sr.top, h: sq.height }]);
      G.fades = [];
      fades.forEach(function (f) {
        if (!f) return; var q = f.getBoundingClientRect(); if (!q.width || !q.height) return;
        var o = { el: f, x: q.left - sr.left, y: q.top - sr.top, w: q.width, h: q.height, late: f !== fades[0] };   // all but the heading wait for the others to land
        o.fin = gapTo(o, G.sx, G.sy, G.sw, G.sh); G.fades.push(o);
      });
      lastW = W; lastH = H;
      return true;
    }

    function render(p) {
      if (G.phone && Math.abs(rail.scrollLeft - G.home) > .5) {            // the visitor moved the rail: follow the poster
        var sr = stage.getBoundingClientRect(), r = slot.getBoundingClientRect(); G.sx = r.left - sr.left;
      }
      // the order of a clean pull-back (critic-1-1): the words cut out before anything moves; the shot pulls back; its
      // label rides on it; only then do the other three come in, as pictures; every word of the board comes last
      var e = inout(band(p, .035, .9)), done = e >= 1;
      // the frame: from the whole screen to the poster's place
      var x = e * G.sx, y = e * G.sy, fw = lerp(G.W, G.sw, e), fh = lerp(G.H, G.sh, e), rad = 4 * e;
      // the photo: from the opening's frame to the poster's crop (the poster follows the rail if it was moved)
      var r1x = G.sx + (G.sw - G.r1.w) * .5, iw = lerp(G.r0.w, G.r1.w, e), py = lerp(G.r0.y, G.r1.y, e);
      img.style.transform = "translate3d(" + lerp(G.r0.x, r1x, e).toFixed(2) + "px," + py.toFixed(2) + "px,0) scale(" + (iw / G.bw).toFixed(5) + ")";
      // the opening's words leave first, within a few per cent, so they never hang ghosted over a moving photo; the
      // buttons stop taking taps as they go (P1)
      var g = out3(band(p, 0, .035));
      var ly = y + fh, cb = y + fh, fa = 0, fb = 0;   // the label's foot, the frame's visible foot, the photo's feather
      if (G.lift) {                     // the feather holds while the lifted shot is short of the frame's foot, then recedes
        var k = G.ec < 1 ? band(e, G.ec, 1) : 1, m0 = lerp(64, 112, k), m1 = lerp(96, 144, k), ph = iw / A;
        img.style.setProperty("--e-m0", m0.toFixed(2) + "%"); img.style.setProperty("--e-m1", m1.toFixed(2) + "%");
        // until then the photo fades out above the frame's foot: the label rides where the photo ends, on the shot, never
        // on the bare ground below it (critic-2-1)
        ly = Math.min(ly, py + ph * m1 / 100);
        // and once the words are gone the frame ends there too, so no empty dark card hangs under the shot mid-move
        // (critic-3-1): the camera's view is the photo. The board below that line stays unseen, each piece fading out
        // along the photo's own feather, until the shot has come down over it; the phone's scrim leaves with the words,
        // so the frame's new foot meets the bare ground with no seam
        if (g >= 1) cb = ly;
        fa = done ? 0 : py + ph * m0 / 100; fb = done ? 0 : py + ph * m1 / 100;
      }
      cam.style.clipPath = "inset(" + y.toFixed(2) + "px " + (G.W - x - fw).toFixed(2) + "px " + (G.H - cb).toFixed(2) + "px " + x.toFixed(2) + "px round " + rad.toFixed(2) + "px)";
      shade.style.opacity = (G.lift ? 1 - g : 1 - band(p, .05, .5)).toFixed(3);
      hin.style.opacity = (1 - g).toFixed(3);
      hin.style.transform = g ? "translate3d(0," + (-20 * g).toFixed(1) + "px,0)" : "";
      // the Daily Highlights label and its tally ride on the shot, coming in as the words go, so no frame is left with
      // neither (P2, qa-2-3)
      var l = out3(band(p, .03, .12));
      lab.style.opacity = foot.style.opacity = tal.style.opacity = l.toFixed(3);
      lab.style.transform = "translate3d(" + x.toFixed(2) + "px," + (ly - G.sh).toFixed(2) + "px,0)";
      foot.style.transform = "translate3d(0," + (ly - G.sh).toFixed(2) + "px,0)";
      tal.style.transform = "translate3d(" + (x + fw - G.tx).toFixed(2) + "px," + (y + G.ty).toFixed(2) + "px,0)";
      // the other three: unseen until the label is on, then opaque, uncovered by the shot as it shrinks and sliding in
      // under it; their words only where the shot no longer covers them, together with the board's own words at the end
      G.others.forEach(function (o) {
        var t = out3(band(p, o.a, o.a + .4)), gx = (1 - t) * o.dx, gy = (1 - t) * o.dy;
        o.li.style.opacity = p < o.v ? "0" : "";
        o.li.style.transform = t < 1 ? "translate3d(" + gx.toFixed(1) + "px," + gy.toFixed(1) + "px,0)" : "";
        var co = done ? 1 : clamp(gapTo({ x: o.x + gx, y: o.y + gy, w: o.w, h: o.h }, x, y, fw, fh) / Math.max(1, Math.min(18, o.fin)), 0, 1) * band(p, .7, .86);
        o.li.style.setProperty("--e-co", co.toFixed(3));
        o.gy = gy;
      });
      if (G.lift) feather(fa, fb);
      // the heading, the shot's number and its package show only where the shot no longer covers them (P2)
      G.fades.forEach(function (f) {
        var op = done ? 1 : clamp(gapTo(f, x, y, fw, fh) / Math.max(1, Math.min(18, f.fin)), 0, 1) * (f.late ? band(p, .78, .9) : 1);
        f.el.style.opacity = op < 1 ? op.toFixed(3) : "";
        f.el.style.visibility = op <= 0 ? "hidden" : "";
        f.el.style.pointerEvents = op < .5 ? "none" : "";
      });
      stage.classList.toggle("is-pull", p > 0 && !done);
      stage.classList.toggle("is-gone", g > .5);
      stage.classList.toggle("is-done", done);
      if (G.phone) {
        var ov = done ? "" : "hidden"; if (rail.style.overflowX !== ov) rail.style.overflowX = ov;
        if (!done && !G.homing && Math.abs(rail.scrollLeft - G.home) > 1) {          // flying back in: the rail returns to its rest
          G.homing = 1; rail.scrollTo({ left: G.home, behavior: "smooth" }); setTimeout(function () { G.homing = 0; }, 700);
        }
      }
    }

    // nothing moves until the stage is pinned: the first scroll is a plain one (the nav leaves)
    function target() { return clamp((w.scrollY - G.top) / Math.max(1, G.S - G.top), 0, 1); }
    function tick() { raf = 0; if (!on) return; var p = target(); if (p !== P || G.phone && G.homing) { P = p; render(p); } }
    function onScroll() { if (on && !raf) raf = requestAnimationFrame(tick); }

    // a stop between the two ends on a touch screen finishes the move the way it was going (P4)
    var touching = 0, lastY = w.scrollY, dir = 0, idle = 0, settling = 0;
    function settle() {
      clearTimeout(idle); idle = 0;
      if (!on || !G.snap || touching || settling) return;
      var p = target(); if (p <= 0 || p >= .9) return;
      // on to the four, or back to the whole opening. Down, a small push finishes the move; up, it takes a real pull
      // (more than a third of the move) to fly back in, so a nudge to re-read the heading keeps the four (qa-2-4)
      var to = (dir >= 0 ? p > .12 : p > .62) ? G.S : G.top;
      settling = 1; w.scrollTo({ top: to, behavior: "smooth" });
      setTimeout(function () { settling = 0; }, 900);
    }
    w.addEventListener("scroll", function () {
      var y = w.scrollY; if (y !== lastY) { dir = y > lastY ? 1 : -1; lastY = y; }
      onScroll();
      if (on && G.snap) { clearTimeout(idle); idle = setTimeout(settle, "onscrollend" in w ? 400 : 160); }
    }, { passive: true });
    if ("onscrollend" in w) w.addEventListener("scrollend", function () { if (!touching) settle(); });
    w.addEventListener("touchstart", function () { touching = 1; }, { passive: true });
    function lift() { touching = 0; clearTimeout(idle); idle = setTimeout(settle, 160); }
    w.addEventListener("touchend", lift, { passive: true });
    w.addEventListener("touchcancel", lift, { passive: true });

    function enable() {
      if (on || !can()) return;
      root.classList.add("e-move"); on = true;
      if (!measure()) { disable(); return; }
      P = -1; tick();
    }
    function disable() {
      root.classList.remove("e-move"); on = false; clear();
      wrap.style.removeProperty("--e-travel"); four.style.removeProperty("--e-pw"); root.style.removeProperty("--e-nav");
      stage.classList.remove("is-pull", "is-gone", "is-done");
      if (G.phone) rail.scrollLeft = 0;
    }
    function remeasure() { if (!on) { enable(); return; } var p = target(); if (!measure()) { disable(); return; } P = -1; render(p); P = p; }

    enable();
    // a link from another page to a part below the opening still lands on it
    if (on && location.hash.length > 1) { var t = d.getElementById(location.hash.slice(1)); if (t && !wrap.contains(t)) t.scrollIntoView({ behavior: "instant" }); }
    var rt = 0;
    w.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () { if (stage.clientWidth !== lastW || Math.abs(stage.clientHeight - lastH) > 1 || !on) remeasure(); }, 120);
    });
    w.addEventListener("load", remeasure);
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(function () { if (on) remeasure(); });
    if (w.matchMedia) { var rq = w.matchMedia("(prefers-reduced-motion: reduce)"); var flip = function () { if (rq.matches) disable(); else enable(); }; if (rq.addEventListener) rq.addEventListener("change", flip); else if (rq.addListener) rq.addListener(flip); }
    // the shot is the Daily Highlights link at every stage of the move (P1)
    cam.addEventListener("click", function () { if (on && P > 0 && !stage.classList.contains("is-done")) slot.click(); });
    // a keyboard visitor never lands on a hidden poster or a hidden button: focus takes the camera there
    four.addEventListener("focusin", function () { if (on && target() < .9) w.scrollTo({ top: G.S, behavior: "instant" }); });
    hero.addEventListener("focusin", function () { if (on && target() > 0) w.scrollTo({ top: 0, behavior: "instant" }); });
    w.addEventListener("beforeprint", disable);
    w.addEventListener("afterprint", enable);
  }

  /* ---------------------------------------------------------------- the package a Check dates was pressed for (K2), the month (S1) ---- */
  function picks() {
    var sel = d.getElementById("e-pkg"), when = d.getElementById("e-when");
    var names = { "daily": "daily", "full": "full", "full event": "full", "season": "season", "unsure": "unsure", "not sure yet": "unsure" };
    function choose(v) { v = names[String(v || "").toLowerCase()]; if (sel && v) sel.value = v; }
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[data-pkg]");
      if (a) {
        choose(a.getAttribute("data-pkg"));
        var href = a.getAttribute("href") || "";
        if (/^#pk-/.test(href)) {                              // a poster or its package: light the package it is in
          var card = d.querySelector(href);
          if (card) { card.classList.add("is-lit"); clearTimeout(card._lit); card._lit = setTimeout(function () { card.classList.remove("is-lit"); }, 1800); }
        }
      }
      var m = e.target.closest && e.target.closest(".e-months button[data-when]");
      if (m && when) {
        when.value = m.getAttribute("data-when");
        [].forEach.call(d.querySelectorAll(".e-months li"), function (li) { li.classList.toggle("is-picked", li.contains(m)); });
        // the field it filled comes into view and shows the month for a moment (on a phone it is above the season)
        var fr = when.getBoundingClientRect(), navH = 90, barH = d.querySelector(".e-bar.show") ? 70 : 0;
        if (fr.top < navH || fr.bottom > innerHeight - barH) when.scrollIntoView({ behavior: smooth(), block: "center" });
        when.classList.remove("is-flash"); void when.offsetWidth; when.classList.add("is-flash");
        clearTimeout(when._fl); when._fl = setTimeout(function () { when.classList.remove("is-flash"); }, 1400);
      }
    });
    if (when) when.addEventListener("input", function () { [].forEach.call(d.querySelectorAll(".e-months li.is-picked"), function (li) { li.classList.remove("is-picked"); }); });
    try { var q = new URLSearchParams(location.search).get("package"); if (q) choose(q); } catch (err) {}
  }

  /* ---------------------------------------------------------------- the hand-off to enquire.html (S3) ---- */
  function handoff() {
    var f = d.querySelector("form[data-md-form]"); if (!f) return;
    f.addEventListener("submit", function () {
      var nm = d.getElementById("e-name"), em = d.getElementById("e-email");
      try { sessionStorage.setItem("v4-media-enq", JSON.stringify({ name: (nm ? nm.value : "").trim(), email: (em ? em.value : "").trim() })); } catch (err) {}
    });
  }

  /* ---------------------------------------------------------------- the phone bar (S4): never two orange buttons at once ---- */
  function bar() {
    var b = d.getElementById("eBar"); if (!b || !w.IntersectionObserver) return;
    // the packages count as one stop (each card holds a Check dates), so the bar does not flicker between them
    // (the nav that comes back on a scroll up carries no orange button on a phone here, v4-media.css, critic-2-2, so it
    // no longer hides the bar)
    var stops = [].slice.call(d.querySelectorAll(".e-pull, .e-pk-grid, [data-cd], #dates, body > footer, .page-wrap ~ footer")), seen = [];
    function set() {
      var any = false;
      for (var i = 0; i < seen.length && !any; i++) any = seen[i];
      b.classList.toggle("show", !any);
    }
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { seen[stops.indexOf(x.target)] = x.isIntersecting; }); set();
    });
    stops.forEach(function (el, i) { seen[i] = true; io.observe(el); });
  }

  /* ---------------------------------------------------------------- the phone's poster rail: words only on posters in view ---- */
  function railText() {
    var rail = d.querySelector(".e-posters"); if (!rail) return;
    var items = [].slice.call(rail.querySelectorAll(".e-pl")), raf = 0;
    function set() {
      raf = 0;
      var rr = rail.getBoundingClientRect(), scroller = rail.scrollWidth > rail.clientWidth + 2;
      items.forEach(function (li) {
        var r = li.getBoundingClientRect(), seen = r.width ? (Math.min(r.right, rr.right) - Math.max(r.left, rr.left)) / r.width : 1;
        li.classList.toggle("is-off", scroller && seen < .75);      // a slice peeking in: its picture and number only (critic-1-7)
      });
    }
    function ask() { if (!raf) raf = requestAnimationFrame(set); }
    rail.addEventListener("scroll", ask, { passive: true });
    w.addEventListener("resize", ask);
    w.addEventListener("load", ask);
    set();
    // a keyboard visitor: the poster that holds the focus (its link or its package line) comes to the middle of the
    // rail, so the focus is never off the screen (qa-2-1). Two frames later, once the move has reached the four and the
    // browser's own focus scroll is done
    rail.addEventListener("focusin", function (e) {
      var li = e.target.closest && e.target.closest(".e-pl"); if (!li) return;
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        if (rail.scrollWidth <= rail.clientWidth + 2 || !li.contains(d.activeElement)) return;
        var rr = rail.getBoundingClientRect(), r = li.getBoundingClientRect(),
            to = Math.round(rail.scrollLeft + (r.left + r.width / 2) - (rr.left + rr.width / 2));
        if (Math.abs(to - rail.scrollLeft) > 1) rail.scrollTo({ left: to, behavior: smooth() });
      }); });
    });
  }

  /* ---------------------------------------------------------------- the four titles on one line (critic-3-3) ---- */
  // a poster's words sit on its foot, so a one-line description (or a two-line title) put that poster's title a line
  // off its neighbours'. Where the posters stand side by side, each description takes the room the tallest block in its
  // row needs: the titles share one line, the "Watch" lines stay on the foot, the space falls under the shorter
  // description. The shot's own label in the move gets what its poster gets, so nothing jumps as the move ends. A
  // phone's rail shows one poster at a time and keeps its words as they are; so does the page without JavaScript
  function titles() {
    var rail = d.querySelector(".e-posters"); if (!rail) return;
    var items = [].slice.call(rail.querySelectorAll(".e-pl")), camTags = d.querySelector(".e-cam-lab .e-p-tags"), raf = 0, lastW = -1;
    function part(li, s) { return li.querySelector(s); }
    function set(force) {
      raf = 0;
      if (!force && rail.clientWidth === lastW) return; lastW = rail.clientWidth;
      items.forEach(function (li) { part(li, ".e-p-tags").style.minHeight = ""; });
      if (camTags) camTags.style.minHeight = "";
      if (getComputedStyle(rail).display !== "grid") return;          // the phone's rail (a flex row that swipes)
      var rows = {};                    // by row: the layout's own top, never a moving poster's
      items.forEach(function (li) { (rows[li.offsetTop] = rows[li.offsetTop] || []).push(li); });
      Object.keys(rows).forEach(function (k) {
        var row = rows[k], hs = row.map(function (li) { return part(li, ".e-poster").getBoundingClientRect().bottom - part(li, ".e-p-t").getBoundingClientRect().top; }),
            M = Math.max.apply(null, hs);
        row.forEach(function (li, i) {
          if (M - hs[i] < 1) return;
          var g = part(li, ".e-p-tags"), v = (g.getBoundingClientRect().height + M - hs[i]).toFixed(1) + "px";
          g.style.minHeight = v;
          if (camTags && li.classList.contains("is-cam")) camTags.style.minHeight = v;
        });
      });
    }
    set(true);
    // the rail's width changes with the window and with the move's own measure (the posters' size), so it is watched
    function ask() { if (!raf) raf = requestAnimationFrame(function () { set(false); }); }
    if (w.ResizeObserver) new ResizeObserver(ask).observe(rail); else w.addEventListener("resize", ask);
    w.addEventListener("load", function () { set(true); });
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(function () { set(true); });
  }

  /* ---------------------------------------------------------------- the menu's Enquire Now goes where the header's goes (H5) ---- */
  // the site's menu (v4-menu.js, built the first time it opens) ends on a solid Enquire Now to the pilots' trip
  // enquiry. On a page whose header sends Enquire Now to a part of the page itself (media.html: the dates form), the
  // menu's does the same, so an organiser never lands on the pilots' form; on a phone it is the only Enquire Now in
  // the header (qa-3-1). The menu closes itself for a link to this same page. Done here, not in the shared menu,
  // because the app's offline copy of v4-menu.js is not versioned and would keep the old one on an installed phone
  function menuCta() {
    var cta = d.querySelector(".page-wrap > nav .nav-cta"), to = cta && cta.getAttribute("href");
    if (!to || to.charAt(0) !== "#" || to.length < 2) return;
    function fix() {
      var a = d.querySelector("#v4Menu .v4-menu-foot .btn-solid");
      if (a && a.getAttribute("href") !== to) a.setAttribute("href", to);
      return !!a;
    }
    if (fix() || !w.MutationObserver) return;
    var mo = new MutationObserver(function () { if (fix()) mo.disconnect(); });
    mo.observe(d.body, { childList: true });
  }

  /* ---------------------------------------------------------------- the season's views fill once, when they are seen ---- */
  function season() {
    var s = d.querySelector(".e-season"); if (!s) return;
    if (!w.IntersectionObserver || reduced()) { s.classList.add("is-in"); return; }
    var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { s.classList.add("is-in"); io.disconnect(); } }, { threshold: .3 });
    io.observe(s);
    w.addEventListener("beforeprint", function () { s.classList.add("is-in"); });
  }

  ready(function () {
    reel();
    rows();
    viewer();
    slate();
    pull();
    picks();
    handoff();
    bar();
    railText();
    season();
    titles();
    menuCta();
  });
})();
