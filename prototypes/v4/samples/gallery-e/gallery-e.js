/* Comp gallery sample, designer E (Cloudbase): "Pull Back to the Comp".
   - The walls: true-ratio frames in justified rows, laid out here in whole pixels (CSS rows without JavaScript).
   - The camera: "Scan all" pulls back from the day to the whole comp, small enough to spot your own wing; "Days" flies
     back in. The frame you were on stays where it is on screen, the others travel to their places, and frames that
     only one view shows come in from (or leave toward) the edges as a camera would show them. Transform and opacity
     only, run by the compositor (Web Animations); only frames on or near the screen move, the rest cut.
   - The viewer: a frame grows from where it sits; swipe sideways for the next, pinch or tap to come closer, drag
     down (or Close, Esc, Back) to pull back into its frame, which is lit for a beat. Save, free, fetches the 2400 px
     copy only now and hands it to the phone's share sheet (a download on a computer). Original, EUR 1 opens a sheet
     with the photo's name; the payment link is [to supply].
   Reduced motion: every move is a cut. No JavaScript: the page shows every day, each frame links to its web copy. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  function mm(q) { return !!(w.matchMedia && w.matchMedia(q).matches); }
  function reduced() { return mm("(prefers-reduced-motion: reduce)"); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function $(s, el) { return (el || d).querySelector(s); }
  function $$(s, el) { return [].slice.call((el || d).querySelectorAll(s)); }
  var EASE = "cubic-bezier(.45,0,.2,1)", EASE_OUT = "cubic-bezier(.2,.8,.2,1)";
  var days = $(".g-days"); if (!days) return;
  root.classList.add("g-js");
  try { history.scrollRestoration = "manual"; } catch (e) {}

  /* ---------------------------------------------------------------- the stress test: 350 frames (photos repeated) */
  if (/[?&]stress\b/.test(location.search)) {
    var walls0 = $$(".g-wall"), per = Math.ceil(350 / walls0.length), made = 0;
    walls0.forEach(function (wl, k) {
      var src = $$(".g-f", wl), n = src.length, want = k === walls0.length - 1 ? 350 - made : per, j = n;
      for (; j < want; j++) wl.appendChild(src[j % n].cloneNode(true));
      made += want;
      var p = $(".g-head p", wl.parentNode); if (p) p.textContent = p.textContent.replace(/\d+ photos/, want + " frames (repeated)");
    });
    var sm = $(".g-sample"); if (sm) sm.innerHTML = "<b>Stress test</b>350 frames: the 20 stand-in photos repeated, to test the move at a real comp's size. <a href=\"./\">Back to the sample</a>";
  }

  var tiles = $$(".g-f");
  tiles.forEach(function (t, i) { t._r = parseFloat(t.style.getPropertyValue("--r")) || 1.5; t._i = i; });

  /* ---------------------------------------------------------------- the walls in justified rows, whole pixels */
  function rowH() { var scan = root.classList.contains("g-scan"), wide = w.innerWidth >= 1000; return scan ? (wide ? 76 : 50) : (wide ? 300 : 170); }
  function layWall(wl) {
    var W = Math.floor(wl.getBoundingClientRect().width), G = 4, H = rowH(), items = $$(".g-f", wl), rows = [], row = [], sum = 0;
    if (!W) return;
    function close(list, h, last) { rows.push({ it: list, h: h, last: last }); }
    items.forEach(function (it) {
      row.push(it); sum += it._r;
      var h = (W - G * (row.length - 1)) / sum;
      if (h >= H) return;
      if (row.length > 1) {
        var h0 = (W - G * (row.length - 2)) / (sum - it._r);
        if (h0 - H < H - h) { close(row.slice(0, -1), h0); row = [it]; sum = it._r; var h1 = W / sum; if (h1 < H) { close(row, h1); row = []; sum = 0; } return; }
      }
      close(row, h); row = []; sum = 0;
    });
    if (row.length) close(row, Math.min(H, (W - G * (row.length - 1)) / sum), true);
    var y = 0;
    rows.forEach(function (R) {
      var hh = Math.round(R.h), x = 0, n = R.it.length;
      R.it.forEach(function (it, j) {
        var ww = (j === n - 1 && !R.last) ? W - x : Math.round(it._r * R.h);
        it.style.width = ww + "px"; it.style.height = hh + "px"; it.style.left = x + "px"; it.style.top = y + "px";
        x += ww + G;
      });
      y += hh + G;
    });
    wl.style.height = Math.max(0, y - G) + "px";
  }
  function layAll() { $$(".g-wall").forEach(layWall); }
  layAll();
  var lastW = w.innerWidth;
  if (w.ResizeObserver) new ResizeObserver(function () { if (w.innerWidth !== lastW) { lastW = w.innerWidth; layAll(); lit(); } }).observe(days);
  w.addEventListener("load", layAll);

  /* ---------------------------------------------------------------- the day bar: lit where you are, taps that land clear */
  var bar = $(".g-bar"), chips = $$(".g-chip"), strip = $(".g-chips");
  var targets = chips.map(function (c) { return d.getElementById(c.getAttribute("href").slice(1)); });
  var litI = -1;
  function lit() {
    var line = w.innerHeight * 0.4, k = 0;
    for (var i = 0; i < targets.length; i++) if (targets[i] && targets[i].getBoundingClientRect().top <= line) k = i;
    if (k === litI) return; litI = k;
    chips.forEach(function (c, i) { c.classList.toggle("is-lit", i === k); if (i === k) c.setAttribute("aria-current", "true"); else c.removeAttribute("aria-current"); });
    if (strip && strip.scrollWidth > strip.clientWidth + 2) {
      var c = chips[k], x = c.offsetLeft - (strip.clientWidth - c.offsetWidth) / 2;
      strip.scrollTo({ left: Math.max(0, x), behavior: reduced() ? "auto" : "smooth" });
    }
  }
  var litQ = 0;
  w.addEventListener("scroll", function () { if (litQ) return; litQ = 1; requestAnimationFrame(function () { litQ = 0; lit(); }); }, { passive: true });
  lit();
  function navH() { return parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 77; }
  // the bar sits under the site's nav when it comes back: its top changes, and the move is played as a transform
  var wasUp = root.classList.contains("v2-nav-up");
  if (w.MutationObserver) new MutationObserver(function () {
    var up = root.classList.contains("v2-nav-up"); if (up === wasUp) return; wasUp = up;
    if (reduced() || !bar.animate) return;
    var top = parseFloat(getComputedStyle(bar).top) || 0, r = bar.getBoundingClientRect();
    if (Math.abs(r.top - top) > 1.5) return;                        // not stuck: it moves with the page
    var nh = navH();
    bar.animate([{ transform: "translateY(" + (up ? -nh : nh) + "px)" }, { transform: "translateY(0px)" }], { duration: up ? 380 : 280, easing: up ? EASE_OUT : "ease-in" });
  }).observe(root, { attributes: true, attributeFilter: ["class"] });
  function goTo(el) {
    var wide = w.innerWidth >= 1000, top = el.getBoundingClientRect().top + w.scrollY, up = top < w.scrollY;
    var off = (wide ? 24 : bar.offsetHeight + 12) + (up ? navH() : 0);
    w.scrollTo({ top: Math.max(0, top - off), behavior: reduced() ? "auto" : "smooth" });
  }
  chips.forEach(function (c, i) { c.addEventListener("click", function (e) { if (!targets[i]) return; e.preventDefault(); goTo(targets[i]); history.replaceState(null, "", "#" + targets[i].id); }); });
  $$('.g-now a[href^="#task-"]').forEach(function (a) { a.addEventListener("click", function (e) { var t = d.getElementById(a.getAttribute("href").slice(1)); if (!t) return; e.preventDefault(); goTo(t); history.replaceState(null, "", a.getAttribute("href")); }); });

  /* ---------------------------------------------------------------- the camera: Scan all (pull back) and Days (fly in) */
  var cam = $(".g-cam"), camL = $(".g-cam-l"), running = [], lastOpen = null;
  function inView(r, m) { return r.bottom > -m && r.top < w.innerHeight + m && r.right > -m && r.left < w.innerWidth + m; }
  function rect(el) { var r = el.getBoundingClientRect(); return { left: r.left, top: r.top, width: r.width, height: r.height, right: r.right, bottom: r.bottom }; }
  function T(from, to) {          // the transform that puts a frame laid out at `to` where `from` is
    return "translate(" + (from.left - to.left).toFixed(2) + "px," + (from.top - to.top).toFixed(2) + "px) scale(" + (from.width / to.width).toFixed(4) + "," + (from.height / to.height).toFixed(4) + ")";
  }
  function setScan(on) {
    running.forEach(function (a) { try { a.finish(); } catch (e) {} }); running = [];
    var vh = w.innerHeight, M = vh * 0.3;
    var old = tiles.map(rect), y0 = w.scrollY;
    var a = -1;                                                    // the anchor: the last opened frame if on screen, else the one nearest the middle
    if (lastOpen && inView(old[lastOpen._i], -40)) a = lastOpen._i;
    if (a < 0) { var best = 1e9; old.forEach(function (r, i) { if (!inView(r, 0)) return; var dd = Math.abs(r.top + r.height / 2 - vh * 0.5); if (dd < best) { best = dd; a = i; } }); }
    var openVisible = $(".g-open").getBoundingClientRect().bottom > 0;
    root.classList.toggle("g-scan", on);
    cam.setAttribute("aria-pressed", on ? "true" : "false");
    camL.textContent = on ? "Days" : "Scan all";
    cam.setAttribute("aria-label", on ? "Days: back to each day's photos, bigger" : "Scan all: every photo of the comp, small");
    layAll();
    if (a >= 0 && !openVisible) {                                 // keep the anchor where it was on screen
      var dy = tiles[a].getBoundingClientRect().top - old[a].top;
      if (Math.abs(dy) > 0.5) w.scrollTo({ top: y0 + dy, behavior: "instant" });
    }
    var nw = tiles.map(rect);
    lit();
    if (reduced() || a < 0 || !Element.prototype.animate) return;
    var A0 = old[a], A1 = nw[a], k = A0.height / A1.height;
    var ocx = A0.left + A0.width / 2, ocy = A0.top + A0.height / 2, ncx = A1.left + A1.width / 2, ncy = A1.top + A1.height / 2;
    function map(r, cx0, cy0, cx1, cy1, s) {                       // where the camera shows a frame from the other view
      var cx = cx1 + (r.left + r.width / 2 - cx0) * s, cy = cy1 + (r.top + r.height / 2 - cy0) * s, ww = r.width * s, hh = r.height * s;
      return { left: cx - ww / 2, top: cy - hh / 2, width: ww, height: hh };
    }
    var D = 560;
    tiles.forEach(function (t, i) {
      var ov = inView(old[i], M), nv = inView(nw[i], M);
      if (!ov && !nv) return;
      var from = ov ? old[i] : map(nw[i], ncx, ncy, ocx, ocy, k), to = nv ? nw[i] : map(old[i], ocx, ocy, ncx, ncy, 1 / k);
      running.push(t.animate([{ transform: T(from, nw[i]), opacity: ov ? 1 : 0 }, { transform: T(to, nw[i]), opacity: nv ? 1 : 0 }], { duration: D, easing: EASE }));
    });
    $$(".g-head, .g-vid, .g-wait, .g-soon, .g-terms").forEach(function (el) {    // the words come back once the frames are in
      if (!inView(el.getBoundingClientRect(), 0)) return;
      running.push(el.animate([{ opacity: 0 }, { opacity: 0, offset: 0.55 }, { opacity: 1 }], { duration: D, easing: "linear" }));
    });
  }
  cam.setAttribute("aria-pressed", "false");
  cam.addEventListener("click", function () { setScan(!root.classList.contains("g-scan")); });

  /* ---------------------------------------------------------------- the highlight videos play in place */
  $$(".g-vid[data-yt]").forEach(function (b) {
    b.setAttribute("aria-expanded", "false");
    b.addEventListener("click", function () {
      var nx = b.nextElementSibling;
      if (nx && nx.classList.contains("g-play")) { nx.parentNode.removeChild(nx); b.setAttribute("aria-expanded", "false"); return; }
      var box = d.createElement("div"); box.className = "g-play";
      box.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + b.getAttribute("data-yt") + '?autoplay=1&rel=0&playsinline=1" title="' + (b.querySelector("b") || b).textContent + '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
      b.parentNode.insertBefore(box, b.nextSibling); b.setAttribute("aria-expanded", "true");
    });
  });

  /* ---------------------------------------------------------------- the viewer */
  var dlg = $("#g-v"); if (!dlg || !dlg.showModal) return;
  var img = $(".g-v-img", dlg), stage = $(".g-v-stage", dlg), veil = $(".g-v-veil", dlg), foot = $(".g-v-foot", dlg);
  var vName = $(".g-v-name", dlg), vPos = $(".g-v-pos", dlg), save = $(".g-v-save", dlg), buyB = $(".g-v-buy", dlg);
  var sheet = $(".g-buy", dlg), toast = $(".g-toast", dlg), opening = $(".g-open-ph");
  var V = { i: -1, from: null, s: 1, x: 0, y: 0, b: null, ptr: {}, g: null, pushed: false, busy: false, big: 0 };
  var dayCount = {}; tiles.forEach(function (t) { var k = t.getAttribute("data-day"); (dayCount[k] = dayCount[k] || []).push(t); });

  function fit(t) {                                                // the photo's box in the stage, at its own ratio
    var sw = stage.clientWidth, sh = stage.clientHeight, r = t._r, ww = sw, hh = sw / r;
    if (hh > sh) { hh = sh; ww = sh * r; }
    return { l: (sw - ww) / 2, t: (sh - hh) / 2, w: ww, h: hh };
  }
  function place() { var b = V.b; img.style.left = b.l + "px"; img.style.top = b.t + "px"; img.style.width = b.w + "px"; img.style.height = b.h + "px"; }
  function apply() { img.style.transform = "translate(" + V.x.toFixed(1) + "px," + V.y.toFixed(1) + "px) scale(" + V.s.toFixed(4) + ")"; dlg.classList.toggle("is-zoomed", V.s > 1.01); }
  function fromBox() { var s = stage.getBoundingClientRect(); return { left: s.left + V.b.l, top: s.top + V.b.t, width: V.b.w, height: V.b.h }; }
  function uni(r) {                                                // a rect at the photo's own ratio, centred in r (the opening is cropped)
    var ratio = V.b.w / V.b.h, ww = r.width, hh = ww / ratio; if (hh < r.height) { hh = r.height; ww = hh * ratio; }
    return { left: r.left + (r.width - ww) / 2, top: r.top + (r.height - hh) / 2, width: ww, height: hh };
  }
  function Tu(r) { var b = fromBox(); return "translate(" + (r.left - b.left).toFixed(2) + "px," + (r.top - b.top).toFixed(2) + "px) scale(" + (r.width / b.width).toFixed(4) + ")"; }
  function show(i, src) {
    var t = tiles[i], n = t.getAttribute("data-n"), k = t.getAttribute("data-day"), set = dayCount[k] || [];
    V.i = i; V.s = 1; V.x = V.y = 0; V.big = 0;
    var thumb = t.querySelector("img");
    img.src = src || thumb.currentSrc || thumb.src; img.alt = thumb.alt || "";
    img.style.setProperty("--c", t.style.getPropertyValue("--c"));
    V.b = fit(t); place(); apply();
    vName.textContent = n;
    vPos.textContent = "Task " + k + " · " + (set.indexOf(t) + 1) + " of " + set.length;
    save.href = t.href; save.setAttribute("download", n + ".webp"); save.textContent = "Save, free"; V.file = null;
    var pre = new Image(), mid = t.href.replace("-2400.webp", "-1600.webp");    // the 1600 copy once the flight has landed; 2400 only on zoom or Save
    pre.onload = function () { if (V.i === i && !V.big) img.src = mid; };
    setTimeout(function () { if (V.i === i) pre.src = mid; }, reduced() ? 0 : 440);
    $$(".g-v-p, .g-v-nx", dlg).forEach(function (b, j) { b.hidden = j ? i >= tiles.length - 1 : i <= 0; });
  }
  function setFoot() { stage.style.bottom = foot.offsetHeight + "px"; dlg.style.setProperty("--foot", foot.offsetHeight + "px"); }
  function open(t, fromEl, quiet) {
    if (V.busy) return;
    lastOpen = t;
    dlg.showModal(); dlg.classList.remove("is-in"); sheetDown(true);
    setFoot();
    var srcEl = fromEl || t, fr = rect(srcEl);
    show(t._i, fromEl === opening ? opening.querySelector("img").currentSrc : null);
    srcEl.classList.add("is-out"); V.from = srcEl;
    if (!quiet && !V.pushed) { history.pushState({ gv: 1 }, "", "#" + t.getAttribute("data-n")); V.pushed = true; }
    if (reduced() || quiet || !img.animate) { veil.style.opacity = 1; dlg.classList.add("is-in"); return; }
    V.busy = true;
    var a = img.animate([{ transform: Tu(uni(fr)) }, { transform: "translate(0px,0px) scale(1)" }], { duration: 440, easing: EASE_OUT });
    veil.style.opacity = 1; veil.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 320, easing: "linear" });
    a.onfinish = function () { V.busy = false; dlg.classList.add("is-in"); };
  }
  function home(t) {                                                // the frame to land in: the opening if it is still that frame and in view
    if (V.from === opening && opening.getBoundingClientRect().bottom > 60) return opening;
    return t;
  }
  function close(fromPop) {
    if (!dlg.open || V.busy) return;
    if (V.pushed && !fromPop) { V.pushed = false; V.closeAfterPop = true; history.back(); return; }
    V.pushed = false;
    if (location.hash && !d.getElementById(location.hash.slice(1))) history.replaceState(null, "", location.pathname + location.search);
    var t = tiles[V.i], to = home(t);
    if (to === t) {                                                 // bring its frame into view behind the veil, then land in it
      var r0 = t.getBoundingClientRect(), topClear = (w.innerWidth >= 1000 ? 0 : bar.offsetHeight) + 8;
      if (r0.top < topClear || r0.bottom > w.innerHeight - 8) w.scrollTo({ top: w.scrollY + r0.top - (w.innerHeight - r0.height) / 2, behavior: "instant" });
    }
    if (V.from && V.from !== to) V.from.classList.remove("is-out");
    to.classList.add("is-out");
    var tr = rect(to);
    function done() {
      V.busy = false; dlg.classList.remove("is-in", "is-zoomed"); if (dlg.open) dlg.close();
      to.classList.remove("is-out"); img.removeAttribute("src"); veil.style.opacity = 0; img.style.transform = "";
      if (to !== opening) { to.classList.remove("is-home"); void to.offsetWidth; to.classList.add("is-home"); setTimeout(function () { to.classList.remove("is-home"); }, 1700); }
      (to.focus ? to : t).focus({ preventScroll: true });
    }
    sheetDown(true);
    if (reduced() || !img.animate) { done(); return; }
    V.busy = true; dlg.classList.remove("is-in");
    var now = getComputedStyle(img).transform; if (!now || now === "none") now = "translate(0px,0px) scale(1)";
    var target = to === opening ? uni(tr) : tr;
    var a = img.animate([{ transform: now }, { transform: Tu(target) }], { duration: 380, easing: EASE_OUT, fill: "forwards" });
    var v0 = parseFloat(getComputedStyle(veil).opacity); veil.animate([{ opacity: v0 }, { opacity: 0 }], { duration: 340, easing: "linear", fill: "forwards" });
    a.onfinish = function () { a.cancel(); veil.getAnimations().forEach(function (x) { x.cancel(); }); done(); };
  }
  w.addEventListener("popstate", function () { if (dlg.open) { V.pushed = false; close(true); } });

  function go(k) {
    var j = V.i + k; if (j < 0 || j >= tiles.length || V.busy) return;
    if (V.from) V.from.classList.remove("is-out");
    V.from = tiles[j]; lastOpen = tiles[j];
    history.replaceState(history.state, "", "#" + tiles[j].getAttribute("data-n"));
    if (reduced() || !img.animate) { show(j); return; }
    V.busy = true;
    var dx = k > 0 ? -24 : 24;
    var out = img.animate([{ opacity: 1, transform: img.style.transform }, { opacity: 0, transform: "translate(" + dx + "px,0px) scale(1)" }], { duration: 140, easing: "ease-in", fill: "forwards" });
    out.onfinish = function () {
      show(j); out.cancel();
      var inn = img.animate([{ opacity: 0, transform: "translate(" + (-dx) + "px,0px) scale(1)" }, { opacity: 1, transform: "translate(0px,0px) scale(1)" }], { duration: 200, easing: EASE_OUT });
      inn.onfinish = function () { V.busy = false; };
    };
  }

  /* zoom, pan, swipe, pull down */
  function zoomAt(k, cx, cy) {
    var b = fromBox(), s1 = clamp(V.s * k, 1, 6), u = (cx - b.left - V.x) / V.s, v = (cy - b.top - V.y) / V.s;
    V.x = cx - b.left - s1 * u; V.y = cy - b.top - s1 * v; V.s = s1;
    if (V.s <= 1.001) { V.s = 1; V.x = V.y = 0; }
    clampPan(); apply();
    if (V.s > 1.5 && !V.big) { V.big = 1; var i = V.i, big = new Image(); big.onload = function () { if (V.i === i) img.src = big.src; }; big.src = tiles[i].href; }
  }
  function clampPan() {
    var sw = stage.clientWidth, sh = stage.clientHeight, b = V.b, W = b.w * V.s, H = b.h * V.s;
    V.x = W <= sw ? (sw - W) / 2 - b.l : clamp(V.x, sw - W - b.l, -b.l);
    V.y = H <= sh ? (sh - H) / 2 - b.t : clamp(V.y, sh - H - b.t, -b.t);
    if (V.s === 1) { V.x = V.y = 0; }
  }
  stage.addEventListener("pointerdown", function (e) {
    if (V.busy) return;
    V.ptr[e.pointerId] = { x: e.clientX, y: e.clientY };
    var ids = Object.keys(V.ptr);
    if (ids.length === 2) { var A = V.ptr[ids[0]], B = V.ptr[ids[1]]; V.g = { kind: "pinch", span: Math.hypot(A.x - B.x, A.y - B.y), cx: (A.x + B.x) / 2, cy: (A.y + B.y) / 2 }; }
    else V.g = { kind: "", sx: e.clientX, sy: e.clientY, t0: Date.now(), dx: 0, dy: 0, moved: 0 };
    try { stage.setPointerCapture(e.pointerId); } catch (er) {}
  });
  stage.addEventListener("pointermove", function (e) {
    var p = V.ptr[e.pointerId], g = V.g; if (!p || !g) return;
    var mx = e.clientX - p.x, my = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY;
    var ids = Object.keys(V.ptr);
    if (g.kind === "pinch" && ids.length >= 2) {
      var A = V.ptr[ids[0]], B = V.ptr[ids[1]], span = Math.hypot(A.x - B.x, A.y - B.y), cx = (A.x + B.x) / 2, cy = (A.y + B.y) / 2;
      if (g.span > 0) zoomAt(span / g.span, cx, cy);
      V.x += cx - g.cx; V.y += cy - g.cy; g.span = span; g.cx = cx; g.cy = cy; clampPan(); apply(); return;
    }
    g.dx = e.clientX - g.sx; g.dy = e.clientY - g.sy; g.moved += Math.abs(mx) + Math.abs(my);
    if (V.s > 1.01) { V.x += mx; V.y += my; clampPan(); apply(); g.kind = "pan"; return; }
    if (!g.kind && Math.hypot(g.dx, g.dy) > 8) g.kind = Math.abs(g.dy) > Math.abs(g.dx) ? "pull" : "swipe";
    if (g.kind === "pull") {
      var dy = Math.max(0, g.dy), sh = stage.clientHeight, s = 1 - Math.min(0.45, dy / (sh * 1.6));
      img.style.transform = "translate(" + (g.dx * 0.6 + V.b.w * (1 - s) / 2).toFixed(1) + "px," + (dy + V.b.h * (1 - s) / 2).toFixed(1) + "px) scale(" + s.toFixed(4) + ")";
      veil.style.opacity = (1 - Math.min(0.85, dy / (sh * 0.7))).toFixed(3);
      dlg.classList.toggle("is-pulling", dy > 4);
    } else if (g.kind === "swipe") {
      img.style.transform = "translate(" + (g.dx * 0.5).toFixed(1) + "px,0px) scale(1)";
    }
  });
  function up(e) {
    var g = V.g; delete V.ptr[e.pointerId];
    if (Object.keys(V.ptr).length) return;
    V.g = null; if (!g) return;
    if (g.kind === "pinch" || g.kind === "pan") return;
    if (g.kind === "pull") {
      if (g.dy > 90) { close(); return; }
      var now = img.style.transform; dlg.classList.remove("is-pulling");
      if (img.animate && !reduced()) img.animate([{ transform: now }, { transform: "translate(0px,0px) scale(1)" }], { duration: 240, easing: EASE_OUT });
      if (veil.animate && !reduced()) veil.animate([{ opacity: veil.style.opacity }, { opacity: 1 }], { duration: 240 });
      veil.style.opacity = 1; apply(); return;
    }
    if (g.kind === "swipe") {
      if (Math.abs(g.dx) > 60 && ((g.dx < 0 && V.i < tiles.length - 1) || (g.dx > 0 && V.i > 0))) { go(g.dx < 0 ? 1 : -1); return; }
      var n2 = img.style.transform; if (img.animate && !reduced()) img.animate([{ transform: n2 }, { transform: "translate(0px,0px) scale(1)" }], { duration: 200, easing: EASE_OUT }); apply(); return;
    }
    if (g.moved < 8 && Date.now() - g.t0 < 500) {                  // a tap: on the photo, come closer; beside it, pull back
      var b = fromBox(), on = e.clientX >= b.left + V.x && e.clientX <= b.left + V.x + b.width * V.s && e.clientY >= b.top + V.y && e.clientY <= b.top + V.y + b.height * V.s;
      if (on) { var target = V.s < 1.5 ? 2.5 : 1; zoomAt(target / V.s, e.clientX, e.clientY); } else close();
    }
  }
  stage.addEventListener("pointerup", up); stage.addEventListener("pointercancel", function (e) { delete V.ptr[e.pointerId]; V.g = null; apply(); veil.style.opacity = 1; });
  stage.addEventListener("wheel", function (e) { e.preventDefault(); zoomAt(Math.exp(-clamp(e.deltaY, -80, 80) * 0.004), e.clientX, e.clientY); }, { passive: false });
  veil.addEventListener("click", function () { close(); });
  $(".g-v-x", dlg).addEventListener("click", function () { close(); });
  $(".g-v-p", dlg).addEventListener("click", function () { go(-1); });
  $(".g-v-nx", dlg).addEventListener("click", function () { go(1); });
  dlg.addEventListener("cancel", function (e) { e.preventDefault(); if (sheet.classList.contains("is-up")) sheetDown(); else close(); });
  d.addEventListener("keydown", function (e) {
    if (!dlg.open || sheet.classList.contains("is-up")) return;
    if (e.key === "ArrowRight") { e.preventDefault(); go(1); } else if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
    else if (e.key === "+" || e.key === "=") zoomAt(1.4, w.innerWidth / 2, w.innerHeight / 2);
    else if (e.key === "-") zoomAt(1 / 1.4, w.innerWidth / 2, w.innerHeight / 2);
  });
  w.addEventListener("resize", function () { if (!dlg.open) return; setFoot(); V.b = fit(tiles[V.i]); V.s = 1; V.x = V.y = 0; place(); apply(); });

  tiles.forEach(function (t) { t.addEventListener("click", function (e) { if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return; e.preventDefault(); open(t); }); });
  if (opening) opening.addEventListener("click", function (e) {
    var n = opening.getAttribute("data-open"), t = tiles.filter(function (x) { return x.getAttribute("data-n") === n; })[0];
    if (!t) return; e.preventDefault(); open(t, opening);
  });

  /* Save, free: the 2400 px copy, fetched only now (the photo host allows it), to the share sheet on a phone */
  function say(msg) { toast.textContent = msg; toast.classList.add("is-on"); clearTimeout(say.t); say.t = setTimeout(function () { toast.classList.remove("is-on"); }, 2400); }
  function hand(file) {
    var touch = mm("(pointer: coarse)");
    if (touch && navigator.canShare && navigator.share && navigator.canShare({ files: [file] })) {
      return navigator.share({ files: [file], title: file.name }).then(function () { say("Saved " + file.name); save.textContent = "Save, free"; }, function (err) {
        if (err && err.name === "NotAllowedError") { save.textContent = "Tap again to save"; V.file = file; }      // the phone wants a fresh tap
      });
    }
    var u = URL.createObjectURL(file), a = d.createElement("a"); a.href = u; a.download = file.name; d.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(u); }, 4000);
    save.textContent = "Save, free"; say("Saved " + file.name);
  }
  save.addEventListener("click", function (e) {
    e.preventDefault();
    if (V.file) { var f = V.file; V.file = null; hand(f); return; }
    if (save.getAttribute("aria-busy") === "true") return;
    var t = tiles[V.i], n = t.getAttribute("data-n"), url = t.href;
    save.setAttribute("aria-busy", "true"); save.textContent = "Saving";
    fetch(url, { mode: "cors" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.blob(); }).then(function (b) {
      save.removeAttribute("aria-busy");
      if (tiles[V.i] !== t) { save.textContent = "Save, free"; return; }
      return hand(new File([b], n + ".webp", { type: "image/webp" }));
    }).catch(function () { save.removeAttribute("aria-busy"); save.textContent = "Save, free"; w.open(url, "_blank", "noopener"); });
  });

  /* Original, EUR 1: the sheet with the photo's name; the payment page takes the email; the link is [to supply] */
  var bN = $(".g-buy-n", sheet), bTh = $(".g-buy-th", sheet), pay = $(".g-pay", sheet), note = $(".g-buy-note", sheet), copyB = $(".g-copy", sheet);
  function sheetUp() {
    var t = tiles[V.i], n = t.getAttribute("data-n"); bN.textContent = n; bTh.src = t.querySelector("img").currentSrc || t.querySelector("img").src; note.textContent = ""; copyB.textContent = "Copy name";
    sheet.classList.add("is-up"); sheet.removeAttribute("inert"); setTimeout(function () { pay.focus({ preventScroll: true }); }, reduced() ? 0 : 200);
  }
  function sheetDown(quiet) { var was = sheet.classList.contains("is-up"); sheet.classList.remove("is-up"); sheet.setAttribute("inert", ""); if (was && !quiet) buyB.focus({ preventScroll: true }); }
  sheetDown(true);
  buyB.addEventListener("click", sheetUp);
  $(".g-buy-no", sheet).addEventListener("click", function () { sheetDown(); });
  pay.addEventListener("click", function (e) {
    e.preventDefault();
    note.innerHTML = 'The payment link is <i class="v2-tbd">[to supply]</i>. On the real page this opens the checkout for EUR 1, with ' + bN.textContent + " as the reference.";
  });
  copyB.addEventListener("click", function () {
    var n = bN.textContent;
    function ok() { copyB.textContent = "Copied"; }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(n).then(ok, function () {}); else ok();
  });

  /* a link to one photo (#SRS_5_T2_133-2) opens it */
  var h = decodeURIComponent(location.hash.slice(1));
  if (h && !d.getElementById(h)) { var t0 = tiles.filter(function (x) { return x.getAttribute("data-n") === h; })[0]; if (t0) { t0.scrollIntoView({ block: "center", behavior: "instant" }); open(t0, null, true); } }
})();
