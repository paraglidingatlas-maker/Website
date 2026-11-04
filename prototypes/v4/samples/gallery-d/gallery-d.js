/* Comp gallery, designer D (Trim), "Proof Sheet". Without this script the page is finished: the sheet is drawn by CSS,
   the day strip is links, each frame links to its 2400 px web copy. The script adds: the day strip following the
   page, the wing colours that light frames (never hide them), the video playing in place, and the viewer, where the
   frame lifts out of its cell, and Save and Original sit under it. Motion: transform and opacity only. */
(function () {
  "use strict";
  var d = document, w = window;
  var BASE = "https://paraglidingatlas-maker.github.io/media-2026/srs-piedrahita/";
  function mm(q) { return !!(w.matchMedia && w.matchMedia(q).matches); }
  function reduced() { return mm("(prefers-reduced-motion: reduce)"); }
  function coarse() { return mm("(pointer: coarse)"); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ready(f) { if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", f); else f(); }
  var stripH = function () { var s = d.querySelector(".gd-days"); return s ? s.getBoundingClientRect().height : 0; };

  /* ---------------------------------------------------------------- the day strip follows the page ---- */
  function strip() {
    var bar = d.querySelector(".gd-days"); if (!bar) return;
    var row = bar.querySelector(".gd-days-row");
    var links = [].slice.call(bar.querySelectorAll(".gd-day"));
    var secs = links.map(function (a) { return d.getElementById(a.getAttribute("href").slice(1)); });
    var cur = -2, raf = 0;
    function set(i) {
      if (i === cur) return; cur = i;
      links.forEach(function (a, k) { if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      var a = links[i];
      if (a && row && row.scrollWidth > row.clientWidth + 1) {
        var l = a.offsetLeft - (row.clientWidth - a.offsetWidth) / 2;
        row.scrollTo({ left: Math.max(0, l), behavior: "auto" });
      }
    }
    function look() {
      raf = 0; var y = stripH() + 48, i = -1;
      for (var k = 0; k < secs.length; k++) { if (secs[k] && secs[k].getBoundingClientRect().top <= y) i = k; }
      if (i >= 0 && secs[i]) { var r = secs[i].getBoundingClientRect(); if (r.bottom < y && i === secs.length - 1) i = secs.length - 1; }
      set(i);
    }
    w.addEventListener("scroll", function () { if (!raf) raf = requestAnimationFrame(look); }, { passive: true });
    w.addEventListener("resize", function () { if (!raf) raf = requestAnimationFrame(look); });
    look();
  }

  /* ---------------------------------------------------------------- wing colours: light, never hide ---- */
  function colours() {
    [].slice.call(d.querySelectorAll(".gd-wc")).forEach(function (box) {
      var sec = box.closest(".gd-sec"), sheet = sec && sec.querySelector(".gd-sheet"); if (!sheet) return;
      var btns = [].slice.call(box.querySelectorAll("button[data-c]"));
      var figs = [].slice.call(sheet.querySelectorAll(".gd-ph"));
      var live = box.querySelector(".gd-wc-say");
      box.hidden = false;
      function pick(c) {
        btns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-c") === c)); });
        if (!c) { sheet.classList.remove("is-lit"); figs.forEach(function (f) { f.classList.remove("is-on"); }); if (live) live.textContent = "All photos shown."; return; }
        var n = 0;
        figs.forEach(function (f) {
          var cs = (f.getAttribute("data-c") || "").split(" "), on = cs.indexOf(c) >= 0 || cs.indexOf("any") >= 0;
          f.classList.toggle("is-on", on); if (on) n++;
        });
        sheet.classList.add("is-lit");
        if (live) live.textContent = n + " of " + figs.length + " photos lit for " + c + "; a gaggle shot stays lit, anyone can be in it.";
      }
      btns.forEach(function (b) {
        b.addEventListener("click", function () {
          var c = b.getAttribute("data-c");
          pick(b.getAttribute("aria-pressed") === "true" && c ? "" : c);
        });
      });
    });
  }

  /* ---------------------------------------------------------------- the day's video plays in place ---- */
  function videos() {
    d.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest(".gd-vid[data-vid]"); if (!b) return;
      e.preventDefault();
      var box = b.parentNode, f = box.querySelector(".gd-vid-f");
      if (f) { f.parentNode.removeChild(f); b.setAttribute("aria-expanded", "false"); return; }
      f = d.createElement("div"); f.className = "gd-vid-f";
      var ifr = d.createElement("iframe");
      ifr.src = "https://www.youtube-nocookie.com/embed/" + b.getAttribute("data-vid") + "?autoplay=1&rel=0&modestbranding=1&playsinline=1";
      ifr.title = b.getAttribute("data-title") || "Video";
      ifr.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen"; ifr.allowFullscreen = true;
      f.appendChild(ifr); box.appendChild(f); b.setAttribute("aria-expanded", "true");
    });
  }

  /* ---------------------------------------------------------------- the viewer ---- */
  function viewer() {
    var v = d.getElementById("gd-v"); if (!v || typeof v.showModal !== "function") return;   // no dialog: each frame stays a link to its file
    var stage = v.querySelector(".gd-v-stage"), img = v.querySelector(".gd-v-img"), bar = v.querySelector(".gd-v-bar");
    var nameEl = v.querySelector(".gd-v-name"), posEl = v.querySelector(".gd-v-pos"), topEl = v.querySelector(".gd-v-top");
    var save = v.querySelector(".gd-save"), buy = v.querySelector(".gd-buy"), panel = v.querySelector(".gd-v-buy");
    var buyName = v.querySelector(".gd-v-buy-name b"), pay = v.querySelector(".gd-pay"), said = v.querySelector(".gd-v-said");
    var copy = v.querySelector(".gd-copy"), back = v.querySelector(".gd-v-back"), mark = v.querySelector(".gd-v-mark");
    var prev = v.querySelector(".gd-v-p"), next = v.querySelector(".gd-v-nx"), shut = v.querySelector(".gd-v-x");
    var S = { set: [], i: 0, fig: null, open: false, busy: false, s: 1, x: 0, y: 0, L: 0, T: 0, W: 0, H: 0, pushed: false,
      ptrs: {}, pinch: null, g: null, moved: 0, blob: null, blobName: "", big: "" };
    var EASE = "cubic-bezier(.2,.8,.2,1)", FLY = 320;
    try { if ("scrollRestoration" in history) history.scrollRestoration = "manual"; } catch (e) {}

    function info(a) {
      var f = a.closest("figure");
      return { a: a, fig: f, name: f.id, r: parseFloat(f.style.getPropertyValue("--r")) || 1.5, c: f.style.getPropertyValue("--c"),
        task: f.getAttribute("data-task"), alt: (a.querySelector("img") || {}).alt || "" };
    }
    function paid() { try { return JSON.parse(localStorage.getItem("gd-pay") || "[]"); } catch (e) { return []; } }
    function label() {
      var it = S.set[S.i];
      nameEl.textContent = it.name;
      posEl.textContent = it.task + " · " + (S.i + 1) + " of " + S.set.length;
      if (topEl) topEl.textContent = "Tapalpa 2026 · " + it.task;
      buyName.textContent = it.name;
      save.textContent = "Save, free"; save.removeAttribute("data-state");
      save.href = BASE + it.name + "-2400.webp"; save.setAttribute("download", it.name + ".webp");
      if (mark) mark.hidden = paid().indexOf(it.name) < 0;
      prev.hidden = S.i <= 0; next.hidden = S.i >= S.set.length - 1;
      img.alt = it.alt; img.style.setProperty("--c", it.c);
      said.textContent = "";
    }
    /* the frame's box: as large as the stage allows, at its own ratio */
    function fit(it) {
      v.style.setProperty("--gd-bar", Math.ceil(bar.getBoundingClientRect().height + (innerWidth < 700 ? 4 : 8)) + "px");
      var r = stage.getBoundingClientRect(), pad = innerWidth < 700 ? 0 : 24;
      var sw = r.width - pad * 2, sh = r.height - (innerWidth < 700 ? 8 : 16), ww = sw, hh = ww / it.r;
      if (hh > sh) { hh = sh; ww = hh * it.r; }
      S.W = Math.round(ww); S.H = Math.round(hh); S.L = Math.round(r.left + (r.width - S.W) / 2); S.T = Math.round(r.top + (r.height - S.H) / 2);
      // S.L and S.T are screen positions (the flight is measured on screen); the image is placed inside the stage
      img.style.width = S.W + "px"; img.style.height = S.H + "px"; img.style.left = (S.L - r.left) + "px"; img.style.top = (S.T - r.top) + "px";
    }
    function tf(x, y, s) { return "translate3d(" + x.toFixed(1) + "px," + y.toFixed(1) + "px,0) scale(" + s.toFixed(4) + ")"; }
    function apply(t) { img.style.transition = t || "none"; img.style.transform = tf(S.x, S.y, S.s); v.classList.toggle("is-zoom", S.s > 1.01); }
    function fromCell(fig) { var c = fig.getBoundingClientRect(); return tf(c.left - S.L, c.top - S.T, c.width / S.W); }
    /* the large copy swaps in under the flown 800, same box: no visible change. 1600 unless the screen needs more or you zoom */
    function sharpen(force) {
      var it = S.set[S.i], dpr = w.devicePixelRatio || 1;
      var want = (force || S.W * dpr * S.s > 1700) ? "2400" : "1600";
      if (S.big === it.name + want || (S.big === it.name + "2400")) return;
      var u = BASE + it.name + "-" + want + ".webp", pre = new Image(), name = it.name;
      pre.decoding = "async";
      pre.onload = function () { if (S.open && S.set[S.i].name === name) { img.src = u; S.big = name + want; } };
      pre.src = u;
    }
    /* lock the page under the viewer; where a scrollbar takes room, keep its width so nothing behind shifts */
    function lock(on) {
      var h = d.documentElement;
      if (on) { var sb = innerWidth - h.clientWidth; h.classList.add("gd-lock"); d.body.style.paddingRight = sb > 0 ? sb + "px" : ""; }
      else { h.classList.remove("gd-lock"); d.body.style.paddingRight = ""; }
    }

    function open(a, set, fromHash) {
      if (S.open || S.busy) return;
      S.set = set.map(info); S.i = Math.max(0, set.indexOf(a)); S.s = 1; S.x = S.y = 0; S.big = "";
      var it = S.set[S.i], cellImg = a.querySelector("img");
      img.src = cellImg.currentSrc || cellImg.src;
      label();
      lock(true); v.showModal(); S.open = true; v.classList.remove("is-in", "is-landed", "is-buy");
      fit(it);
      S.fig = it.fig;
      if (!fromHash) { try { history.pushState({ gd: it.name }, "", "#" + it.name); S.pushed = true; } catch (e) { S.pushed = false; } }
      else { try { history.replaceState({ gd: it.name }, "", "#" + it.name); } catch (e) {} S.pushed = false; }
      if (reduced()) { apply(); v.classList.add("is-in", "is-landed"); it.fig.classList.add("is-out"); sharpen(); return; }
      S.busy = true;
      img.style.transition = "none"; img.style.transform = fromCell(it.fig); img.style.opacity = "1";
      it.fig.classList.add("is-out");
      void img.offsetWidth;
      requestAnimationFrame(function () {
        v.classList.add("is-in");
        img.style.transition = "transform " + FLY + "ms " + EASE; img.style.transform = tf(0, 0, 1);
        setTimeout(function () { S.busy = false; v.classList.add("is-landed"); sharpen(); }, FLY + 20);
      });
    }

    function go(k) {
      var j = S.i + k; if (!S.open || S.busy || j < 0 || j >= S.set.length) { if (S.open && !S.busy) settle(); return; }
      v.classList.remove("is-buy");
      var was = S.set[S.i], it = S.set[j], dx = k > 0 ? -1 : 1, rm = reduced();
      S.busy = true;
      img.style.transition = rm ? "none" : "transform .16s " + EASE + ", opacity .16s " + EASE;
      img.style.transform = tf(S.x + dx * 28, S.y, S.s); img.style.opacity = "0";
      setTimeout(function () {
        was.fig.classList.remove("is-out"); it.fig.classList.add("is-out"); S.fig = it.fig;
        S.i = j; S.s = 1; S.x = S.y = 0; S.big = "";
        var cellImg = it.a.querySelector("img");
        img.src = cellImg.currentSrc || cellImg.src || (BASE + it.name + "-800.webp");
        if (!cellImg.complete) img.src = BASE + it.name + "-800.webp";
        label(); fit(it);
        try { history.replaceState({ gd: it.name }, "", "#" + it.name); } catch (e) {}
        img.style.transition = "none"; img.style.transform = tf(-dx * 28, 0, 1);
        void img.offsetWidth;
        img.style.transition = rm ? "none" : "transform .2s " + EASE + ", opacity .2s " + EASE;
        img.style.transform = tf(0, 0, 1); img.style.opacity = "1";
        setTimeout(function () { S.busy = false; sharpen(); }, rm ? 0 : 200);
      }, rm ? 0 : 160);
    }
    function settle() { S.x = S.s > 1.01 ? S.x : 0; S.y = S.s > 1.01 ? S.y : 0; apply("transform .22s " + EASE); v.querySelector(".gd-v-bg").style.opacity = ""; }

    /* close: the frame goes back into its cell; if you swiped far, the sheet is brought to it first */
    function shutNow() {
      if (!S.open) return; var it = S.set[S.i];
      v.classList.remove("is-buy", "is-landed");
      var c = it.fig.getBoundingClientRect(), top = stripH() + 8;
      if (c.top < top || c.bottom > innerHeight - 8) {
        var y = (w.scrollY || w.pageYOffset) + c.top - Math.max(top, (innerHeight - c.height) / 2);
        w.scrollTo(0, Math.max(0, y));
      }
      function done() {
        it.fig.classList.add("is-snap"); it.fig.classList.remove("is-out");
        requestAnimationFrame(function () { requestAnimationFrame(function () { it.fig.classList.remove("is-snap"); }); });
        v.classList.remove("is-in", "is-zoom", "is-drag"); v.querySelector(".gd-v-bg").style.opacity = "";
        if (v.open) v.close(); lock(false); S.open = false; S.busy = false;
        img.removeAttribute("src"); img.style.transform = ""; img.style.transition = "none";
        var a = it.a; try { a.focus({ preventScroll: true }); } catch (e) { a.focus(); }
      }
      if (reduced()) { done(); return; }
      S.busy = true;
      v.classList.remove("is-in"); v.querySelector(".gd-v-bg").style.opacity = "0";
      img.style.transition = "transform " + FLY + "ms " + EASE; img.style.transform = fromCell(it.fig);
      setTimeout(done, FLY + 20);
    }
    function close() {
      if (!S.open || S.busy) return;
      if (S.pushed) { S.pushed = false; history.back(); return; }      // popstate shuts it
      var sec = S.set[S.i].fig.closest(".gd-sec");
      try { history.replaceState(null, "", sec ? "#" + sec.id : location.pathname + location.search); } catch (e) {}
      shutNow();
    }
    w.addEventListener("popstate", function () { if (S.open) { S.pushed = false; S.busy = false; shutNow(); } });

    /* zoom and pan, origin at the box's top left */
    function clampPan() {
      var st = stage.getBoundingClientRect(), sw = S.W * S.s, sh = S.H * S.s;
      if (sw <= st.width) S.x = (S.W - sw) / 2; else S.x = clamp(S.x, st.right - S.L - sw, st.left - S.L);
      if (sh <= st.height) S.y = (S.H - sh) / 2; else S.y = clamp(S.y, st.bottom - S.T - sh, st.top - S.T);
    }
    function zoomAt(k, cx, cy, t) {
      var s1 = clamp(S.s * k, 1, 5), px = (cx - S.L - S.x) / S.s, py = (cy - S.T - S.y) / S.s;
      S.s = s1; S.x = cx - S.L - s1 * px; S.y = cy - S.T - s1 * py;
      if (S.s <= 1.001) { S.s = 1; S.x = S.y = 0; } else clampPan();
      apply(t); if (S.s > 1.3) sharpen(true);
    }

    /* the sheet's frames open the viewer */
    [].slice.call(d.querySelectorAll(".gd-sheet")).forEach(function (g) {
      var set = [].slice.call(g.querySelectorAll(".gd-ph > a"));
      set.forEach(function (a) { a.addEventListener("click", function (e) { if (e.metaKey || e.ctrlKey || e.shiftKey) return; e.preventDefault(); open(a, set); }); });
    });
    prev.addEventListener("click", function (e) { e.stopPropagation(); go(-1); });
    next.addEventListener("click", function (e) { e.stopPropagation(); go(1); });
    shut.addEventListener("click", function (e) { e.stopPropagation(); close(); });
    v.addEventListener("cancel", function (e) { e.preventDefault(); if (v.classList.contains("is-buy")) { v.classList.remove("is-buy"); buy.focus(); } else close(); });
    d.addEventListener("keydown", function (e) {
      if (!S.open) return;
      if (e.key === "ArrowRight") { e.preventDefault(); go(1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
      else if (e.key === "+" || e.key === "=") zoomAt(1.4, S.L + S.W / 2, S.T + S.H / 2, "transform .18s " + EASE);
      else if (e.key === "-") zoomAt(1 / 1.4, S.L + S.W / 2, S.T + S.H / 2, "transform .18s " + EASE);
      else if (e.key === "0") zoomAt(1 / S.s, 0, 0, "transform .18s " + EASE);
    });
    stage.addEventListener("wheel", function (e) { if (!S.open || S.busy) return; e.preventDefault(); zoomAt(Math.exp(-clamp(e.deltaY, -80, 80) * 0.004), e.clientX, e.clientY); }, { passive: false });
    w.addEventListener("resize", function () { if (!S.open || S.busy) return; S.s = 1; S.x = S.y = 0; fit(S.set[S.i]); apply(); });

    /* touch: pinch to zoom, drag to pan when zoomed, swipe sideways for the next, swipe down to close, tap to come closer */
    stage.addEventListener("pointerdown", function (e) {
      if (S.busy) return;
      S.ptrs[e.pointerId] = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY }; S.moved = 0;
      var ids = Object.keys(S.ptrs);
      if (ids.length === 2) { var A = S.ptrs[ids[0]], B = S.ptrs[ids[1]]; S.pinch = { span: Math.hypot(A.x - B.x, A.y - B.y), cx: (A.x + B.x) / 2, cy: (A.y + B.y) / 2 }; S.g = null; }
      if (stage.setPointerCapture) try { stage.setPointerCapture(e.pointerId); } catch (x) {}
      if (S.s > 1.01) v.classList.add("is-drag");
    });
    stage.addEventListener("pointermove", function (e) {
      var p = S.ptrs[e.pointerId]; if (!p || S.busy) return;
      var dx = e.clientX - p.x, dy = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY; S.moved += Math.abs(dx) + Math.abs(dy);
      var ids = Object.keys(S.ptrs);
      if (ids.length >= 2 && S.pinch) {
        var A = S.ptrs[ids[0]], B = S.ptrs[ids[1]], span = Math.hypot(A.x - B.x, A.y - B.y), cx = (A.x + B.x) / 2, cy = (A.y + B.y) / 2;
        if (S.pinch.span > 0) zoomAt(span / Math.max(1, S.pinch.span), cx, cy);
        S.x += cx - S.pinch.cx; S.y += cy - S.pinch.cy; S.pinch.span = span; S.pinch.cx = cx; S.pinch.cy = cy; clampPan(); apply(); return;
      }
      if (S.s > 1.01) { S.x += dx; S.y += dy; clampPan(); apply(); return; }
      var tx = e.clientX - p.sx, ty = e.clientY - p.sy;
      if (!S.g && (Math.abs(tx) > 8 || Math.abs(ty) > 8)) S.g = Math.abs(tx) > Math.abs(ty) ? "x" : (ty > 0 ? "y" : "n");
      if (S.g === "x") { S.x = tx; S.y = 0; apply(); }
      else if (S.g === "y") {
        var k = clamp(ty / 600, 0, .5); S.x = tx * .4 + S.W * k * .2; S.y = ty + S.H * k * .2; S.s = 1 - k * .4;
        img.style.transition = "none"; img.style.transform = tf(S.x, S.y, S.s);
        v.querySelector(".gd-v-bg").style.opacity = String(1 - k * 1.4);
        S.s = 1;      // the pull is a gesture, not a zoom
      }
    });
    function up(e) {
      var p = S.ptrs[e.pointerId]; delete S.ptrs[e.pointerId];
      var ids = Object.keys(S.ptrs); if (ids.length < 2) S.pinch = null; v.classList.remove("is-drag");
      if (!p || ids.length || S.busy) return;
      if (v.classList.contains("is-buy") && S.moved < 8) { S.g = null; v.classList.remove("is-buy"); return; }
      var tx = e.clientX - p.sx, ty = e.clientY - p.sy, g = S.g; S.g = null;
      if (g === "x") { if (Math.abs(tx) > 60) go(tx < 0 ? 1 : -1); else settle(); return; }
      if (g === "y") { if (ty > 90) close(); else { S.s = 1; settle(); } return; }
      if (g === "n") { settle(); return; }
      if (S.moved < 8 && e.type === "pointerup") {
        var r = img.getBoundingClientRect(), on = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
        if (on) zoomAt((S.s < 1.5 ? 2.5 : 1) / S.s, e.clientX, e.clientY, "transform .22s " + EASE); else close();
      }
    }
    stage.addEventListener("pointerup", up); stage.addEventListener("pointercancel", up);
    v.querySelector(".gd-v-bg").addEventListener("click", function () { close(); });

    /* Save, free: the 2400 web copy, named by its frame. A phone gets the share sheet (Save Image, Instagram, WhatsApp);
       a computer gets a download. The file lives on another domain, so a plain download link would only open it:
       fetch it (the host allows it) and hand it over. If the phone wants a fresh tap after the wait, it asks for one. */
    function saveLabel(t, st) { save.textContent = t; if (st) save.setAttribute("data-state", st); else save.removeAttribute("data-state"); }
    function hand(b, name) {
      var file = null; try { file = new File([b], name + ".webp", { type: "image/webp" }); } catch (x) {}
      if (file && coarse() && navigator.canShare && navigator.canShare({ files: [file] })) {
        navigator.share({ files: [file], title: name }).then(function () { saveLabel("Saved"); setTimeout(function () { saveLabel("Save, free"); }, 1800); })
          .catch(function (err) { if (err && err.name === "NotAllowedError") saveLabel("Tap to save", "ready"); else saveLabel("Save, free"); });
        return;
      }
      var u = URL.createObjectURL(b), a = d.createElement("a");
      a.href = u; a.download = name + ".webp"; a.style.display = "none"; v.appendChild(a); a.click(); v.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(u); }, 5000);
      saveLabel("Saved"); setTimeout(function () { if (save.textContent === "Saved") saveLabel("Save, free"); }, 1800);
    }
    save.addEventListener("click", function (e) {
      e.preventDefault(); e.stopPropagation();
      var name = S.set[S.i].name, url = BASE + name + "-2400.webp";
      if (S.blob && S.blobName === name) { hand(S.blob, name); return; }
      if (save.getAttribute("data-state") === "busy") return;
      saveLabel("Preparing", "busy");
      fetch(url, { mode: "cors" }).then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.blob(); })
        .then(function (b) { S.blob = b; S.blobName = name; if (S.set[S.i].name === name) hand(b, name); })
        .catch(function () { saveLabel("Save, free"); w.open(url, "_blank", "noopener"); });
    });

    /* Original, EUR 1: one panel under the photo. The payment link is [to supply]; our page keeps no form and no email */
    buy.addEventListener("click", function (e) { e.stopPropagation(); v.classList.add("is-buy"); setTimeout(function () { pay.focus(); }, 60); });
    back.addEventListener("click", function (e) { e.stopPropagation(); v.classList.remove("is-buy"); buy.focus(); });
    copy.addEventListener("click", function (e) {
      e.stopPropagation(); var name = S.set[S.i].name;
      var ok = function () { copy.textContent = "Copied"; setTimeout(function () { copy.textContent = "Copy name"; }, 1600); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(name).then(ok, function () { said.textContent = "Select the name to copy it: " + name; });
      else said.textContent = "Select the name to copy it: " + name;
    });
    pay.addEventListener("click", function (e) {
      var link = pay.getAttribute("data-link");
      var name = S.set[S.i].name;
      try { var l = paid(); if (l.indexOf(name) < 0) { l.push(name); localStorage.setItem("gd-pay", JSON.stringify(l)); } } catch (x) {}
      if (mark) mark.hidden = false;
      if (!link) { e.preventDefault(); said.textContent = "This sample has no payment link yet: it is [to supply]. On the real page it opens in a new tab, and this photo stays open here."; return; }
    });

    /* a link to one photo (#SRS_5_T2_133-2) opens it, from its own place in the sheet */
    function fromHash() {
      var id = decodeURIComponent((location.hash || "").slice(1)); if (!id) return;
      var f = d.getElementById(id); if (!f || !f.classList.contains("gd-ph")) return;
      var a = f.querySelector("a"), g = f.closest(".gd-sheet"); if (!a || !g) return;
      var set = [].slice.call(g.querySelectorAll(".gd-ph > a"));
      var r = f.getBoundingClientRect();
      if (r.top < stripH() || r.bottom > innerHeight) w.scrollTo(0, (w.scrollY || w.pageYOffset) + r.top - Math.max(stripH() + 16, (innerHeight - r.height) / 2));
      requestAnimationFrame(function () { open(a, set, true); });
    }
    if (d.readyState === "complete") fromHash(); else w.addEventListener("load", fromHash);
    w.addEventListener("hashchange", function () { if (!S.open && !S.busy) fromHash(); });
  }

  ready(function () { d.documentElement.classList.add("gd-js"); strip(); colours(); videos(); viewer(); });
})();
