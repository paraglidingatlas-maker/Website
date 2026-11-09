/* The comp gallery (chat 20, built by tools/v4_comp_gallery.py): designer F's "Fly the Comp" (the task line, one
   task at a time, the glider flies to the task you tap), with D's lift-out viewer (the photo leaves its cell and goes
   back to it) and an every-task view. Save hands over a JPEG made here from the 2400 px web copy (phones' Instagram
   and WhatsApp may refuse WebP). Moves are transform and opacity only. No JS: every task is stacked in order and each
   photo links to its web copy. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  var main = d.querySelector(".gf"); if (!main) return;
  root.classList.add("gf-js");
  var mq = w.matchMedia ? w.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  function reduced() { return mq.matches; }
  var EASE = "cubic-bezier(.2,.8,.2,1)";
  var data = {}; try { data = JSON.parse(d.getElementById("gf-data").textContent); } catch (e) {}
  var line = d.querySelector(".gf-line"), glw = line.querySelector(".gf-glw"), glider = line.querySelector(".gf-glider"),
      flown = line.querySelector(".gf-flown"), body = d.querySelector(".gf-body");
  var tps = [].slice.call(line.querySelectorAll(".gf-tp")), days = [].slice.call(d.querySelectorAll(".gf-day"));
  var N = days.length;

  /* ---------------------------------------------------------------- today, in the comp's own time zone */
  function todayIn(tz) {
    try { return new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date()); }
    catch (e) { var t = new Date(); return t.getFullYear() + "-" + ("0" + (t.getMonth() + 1)).slice(-2) + "-" + ("0" + t.getDate()).slice(-2); }
  }
  var q = {}; try { q = new URLSearchParams(location.search); } catch (e) { q = { get: function () { return null; } }; }
  function okDate(s) { return s && /^\d{4}-\d{2}-\d{2}$/.test(s) ? s : null; }
  // the sample pins its evening (data-on); the live page leaves it out and counts from today in Tapalpa
  var on = okDate(q.get("on")) || todayIn(data.tz || "UTC");

  var latest = -1, flownTo = -1;
  days.forEach(function (sec, i) {
    var date = sec.getAttribute("data-date") || "", has = !!sec.querySelector(".gf-ph"), st;
    // a task with photos shows them whatever the date; a task without a date (a comp gone by) is flown
    if (has) st = "photos"; else if (date && date > on) st = "soon"; else st = date === on ? "today" : "coming";
    sec.setAttribute("data-state", st); tps[i].setAttribute("data-state", st);
    if (st === "photos") latest = i;
    if (has || !date || date <= on) flownTo = i;
    var info = (data.days || [])[i] || {}, a = tps[i].querySelector("a");
    var say = { photos: (info.n || 0) + (info.n === 1 ? " photo" : " photos"), today: "flying today, photos tonight", coming: "photos coming", soon: "to come" }[st];
    a.setAttribute("aria-label", (info.name || "Task " + (i + 1)) + ", " + (info.label || "") + ", " + say);
  });
  line.style.setProperty("--flown", Math.max(0, flownTo));
  // every task on one page only makes sense once two tasks have photos
  var withPhotos = days.filter(function (s) { return s.getAttribute("data-state") === "photos"; }).length;
  [].forEach.call(d.querySelectorAll(".gf-mode"), function (m) { m.hidden = withPhotos < 2; });
  days.forEach(function (sec, i) {
    var a = sec.querySelector("[data-latest]"); if (!a) return;
    if (latest >= 0 && latest !== i) {
      var info = (data.days || [])[latest] || {};
      a.href = "#" + days[latest].id; a.setAttribute("data-go", latest); a.hidden = false;
      a.firstChild.nodeValue = "See " + (info.name || "Task " + (latest + 1)) + ", " + info.n + (info.n === 1 ? " photo " : " photos ");
    } else a.hidden = true;
  });

  /* ---------------------------------------------------------------- the line: the glider flies the leg */
  var cur = -1, flight = null, bank = null;
  function pct(i) { return (i + 0.5) * 100 / N; }
  function glX() {   // where the glider is now, mid-flight or not, as a share of the line
    var m = getComputedStyle(glw).transform, wd = glw.offsetWidth || 1;
    if (!m || m === "none") return pct(Math.max(cur, 0));
    var v = m.match(/matrix\(([^)]+)\)/); if (!v) return pct(Math.max(cur, 0));
    return parseFloat(v[1].split(",")[4]) / wd * 100;
  }
  function fly(from, to) {
    var x0 = from == null ? glX() : pct(from), x1 = pct(to);
    if (flight) flight.cancel(); if (bank) bank.cancel();
    line.style.setProperty("--open", to);
    if (reduced() || !glw.animate || Math.abs(x1 - x0) < 0.5) return;
    var legs = Math.abs(x1 - x0) / (100 / N), dir = x1 > x0 ? 1 : -1, ms = Math.min(1000, 380 + 150 * legs);
    var mid = (x0 + x1) / 2, lift = -Math.min(9, 5 + legs);
    flight = glw.animate([
      { transform: "translateX(" + x0 + "%) translateY(0px)" },
      { transform: "translateX(" + mid + "%) translateY(" + lift + "px)", offset: 0.5 },
      { transform: "translateX(" + x1 + "%) translateY(0px)" }
    ], { duration: ms, easing: "cubic-bezier(.45,0,.25,1)" });
    bank = glider.animate([
      { transform: "rotate(0deg)" }, { transform: "rotate(" + (dir * 9) + "deg)", offset: 0.3 },
      { transform: "rotate(" + (dir * 4) + "deg)", offset: 0.72 }, { transform: "rotate(0deg)" }
    ], { duration: ms, easing: "ease-in-out" });
  }

  // the line sticks under the nav when the nav comes back (transform only, and only once it is stuck)
  var sentinel = d.createElement("i"); sentinel.setAttribute("aria-hidden", "true"); sentinel.style.cssText = "display:block;height:1px;margin-bottom:-1px";
  body.insertBefore(sentinel, line);
  if (w.IntersectionObserver) new IntersectionObserver(function (es) {
    es.forEach(function (e) { line.classList.toggle("is-stuck", !e.isIntersecting && e.boundingClientRect.top < 0); });
  }).observe(sentinel);

  /* ---------------------------------------------------------------- one day at a time */
  function openDay(i, o) {
    o = o || {};
    if (i < 0 || i >= N) return;
    var prev = cur;
    if (i !== prev) {
      days.forEach(function (s, k) { s.classList.toggle("is-open", k === i); });
      tps.forEach(function (t, k) {
        t.classList.toggle("is-open", k === i);
        var a = t.querySelector("a"); if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
      cur = i;
    }
    if (o.arrive) fly(0, i); else if (prev >= 0 && i !== prev) fly(null, i); else line.style.setProperty("--open", i);
    if (o.scroll) {
      var top = body.getBoundingClientRect().top;
      if (top < 0) {             // down among the photos: bring the new day's head up under the line;
        // the jump is upward, so the site's nav comes back: leave its height free above the line
        var nh = parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 0;
        w.scrollTo(0, Math.max(0, w.scrollY + top - nh));
      }
    }
    if (prev >= 0 && i !== prev && !reduced() && days[i].animate) {
      var dir = i > prev ? 1 : -1;
      days[i].animate([{ opacity: 0, transform: "translateX(" + (dir * 18) + "px)" }, { opacity: 1, transform: "none" }], { duration: 380, easing: EASE });
    }
    if (!o.keepHash) setHash("#" + days[i].id);
  }
  var all = false;
  function setAll(on2) {
    all = !!on2; main.classList.toggle("is-all", all);
    [].forEach.call(d.querySelectorAll(".gf-mode button"), function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-m") === "all" ? String(all) : String(!all)); });
  }
  d.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".gf-mode button"); if (!b) return;
    var want = b.getAttribute("data-m") === "all"; setAll(want);
    if (want) { var t = d.querySelector(".gf-day[data-state=photos]"); if (t) { var nh = parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 0; var top = t.getBoundingClientRect().top; if (top < 0) w.scrollTo(0, Math.max(0, w.scrollY + top - nh - 90)); } setHash(""); }
    else openDay(cur, { scroll: true });
  });
  function setHash(h) { try { history.replaceState(null, "", location.pathname + location.search + h); } catch (e) {} }

  d.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".gf-tp a, [data-go]");
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault();
    if (all) {   // every task is on the page: the line takes you to the task, and the glider flies there
      var j = a.hasAttribute("data-go") ? +a.getAttribute("data-go") : +a.closest(".gf-tp").getAttribute("data-i");
      if (days[j].getAttribute("data-state") === "photos") {
        fly(null, j); cur = j;
        tps.forEach(function (t, k) { t.classList.toggle("is-open", k === j); });
        var nh = parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 0;
        w.scrollTo(0, Math.max(0, w.scrollY + days[j].getBoundingClientRect().top - nh - 90));
        return;
      }
      setAll(false);
    }
    var i = a.hasAttribute("data-go") ? +a.getAttribute("data-go") : +a.closest(".gf-tp").getAttribute("data-i");
    openDay(i, { scroll: true });
    if (a.closest(".gf-df, .gf-wait")) { var h = days[i].querySelector("h2"); h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
  });

  /* ---------------------------------------------------------------- the viewer (from v4-media.js viewer(): tap to come closer, pinch, drag, swipe) */
  var lb = d.getElementById("gfv"), stage = lb.querySelector(".gfv-stage"), img = stage.querySelector("img");
  var bPrev = lb.querySelector(".gfv-prev"), bNext = lb.querySelector(".gfv-next"), pos = lb.querySelector(".gfv-pos");
  var nameEl = lb.querySelector(".gfv-name"), whereEl = lb.querySelector(".gfv-where"), pxEl = lb.querySelector(".gfv-px");
  var save = lb.querySelector(".gfv-save"), buy = lb.querySelector(".gfv-buy"), pay = lb.querySelector(".gfv-pay"), back = lb.querySelector(".gfv-back");
  var copy = lb.querySelector(".gfv-copy"), refs = lb.querySelectorAll(".gfv-ref-n, .gfv-ref-n2"), payNote = lb.querySelector(".gfv-paynote");
  var Z = { s: 1, x: 0, y: 0, ptrs: {}, pinch: null, moved: 0, closing: 0, set: [], i: 0, req: {}, got: {} };
  var blobs = {};
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function apply() { img.style.transform = "translate(" + Z.x.toFixed(1) + "px," + Z.y.toFixed(1) + "px) scale(" + Z.s.toFixed(3) + ")"; lb.classList.toggle("is-zoomed", Z.s > 1.01); }
  function clampPan() {
    var iw = img.clientWidth, ih = img.clientHeight, sw = stage.clientWidth, sh = stage.clientHeight;
    var mx = Math.max(0, (iw * Z.s - sw) / 2 + 24), my = Math.max(0, (ih * Z.s - sh) / 2 + 24);
    if (iw * Z.s <= sw) mx = 0; if (ih * Z.s <= sh) my = 0; Z.x = clamp(Z.x, -mx, mx); Z.y = clamp(Z.y, -my, my);
  }
  function zoomAt(k, cx, cy) {
    var r = stage.getBoundingClientRect(), px = cx - (r.left + r.width / 2), py = cy - (r.top + r.height / 2), s1 = clamp(Z.s * k, 1, 6), ratio = s1 / Z.s;
    Z.x = px - ratio * (px - Z.x); Z.y = py - ratio * (py - Z.y); Z.s = s1; if (Z.s <= 1.001) { Z.x = Z.y = 0; } clampPan(); apply();
    if (Z.s > 1.3) want(2400);      // the 2400 copy only once someone comes closer
  }
  function url(a, size) { return (data.base || "") + a.getAttribute("data-stem") + "-" + size + ".webp"; }
  function want(size) {     // ask for a bigger copy once; show it when it is in, never a smaller one over a bigger
    var a = Z.set[Z.i]; if (!a) return; var k = a.getAttribute("data-stem");
    if ((Z.req[k] || 0) >= size) return; Z.req[k] = size;
    var pre = new Image();
    pre.onload = function () { Z.got[k] = Math.max(Z.got[k] || 0, size); if (Z.set[Z.i] === a && Z.got[k] === size) img.src = pre.src; };
    pre.src = url(a, size);
  }
  function dayOf(a) { return +a.closest(".gf-day").getAttribute("data-i"); }
  function show(a) {
    var th = a.querySelector("img"), stem = a.getAttribute("data-stem"), di = dayOf(a), info = (data.days || [])[di] || {};
    Z.s = 1; Z.x = Z.y = 0; lb.classList.remove("is-zoomed", "is-drag");
    img.src = Z.got[stem] ? url(a, Z.got[stem]) : (th.currentSrc || th.src); img.alt = th.alt || "";
    want(1600);
    nameEl.textContent = stem;
    whereEl.textContent = (info.name || "Task " + (di + 1)) + (info.label ? " · " + info.label : "");
    pxEl.textContent = a.getAttribute("data-W") + " × " + a.getAttribute("data-H") + " px";
    pos.textContent = (Z.i + 1) + " of " + Z.set.length;
    bPrev.disabled = Z.i <= 0; bNext.disabled = Z.i >= Z.set.length - 1;
    save.href = url(a, 2400); save.setAttribute("download", stem + ".jpg");
    resetSave();
    [].forEach.call(refs, function (r) { r.textContent = stem; });
    copy.textContent = "Copy name"; payNote.classList.remove("is-lit");
    apply();
    setHash("#" + stem);
  }
  function openLb(a, o) {
    o = o || {};
    Z.set = [].slice.call((all ? main : a.closest(".gf-grid")).querySelectorAll(all ? ".gf-day[data-state=photos] a[data-stem]" : "a[data-stem]"));
    Z.i = Math.max(0, Z.set.indexOf(a)); Z.ptrs = {}; Z.pinch = null; Z.closing = 0;
    lb.classList.remove("is-in", "is-buy"); img.style.transform = "";
    show(a);
    if (lb.showModal) { if (!lb.open) lb.showModal(); } else lb.setAttribute("open", "");
    if (reduced() || !img.animate) { lb.classList.add("is-in"); return; }
    lb.classList.add("is-lift-out");          // ground clear, chrome hidden: only the photo shows, over its cell
    var started = false;
    function start() {
      if (started || !lb.open) return; started = true;
      lift(a.querySelector("img"), true);
      requestAnimationFrame(function () { lb.classList.remove("is-lift-out"); lb.classList.add("is-in"); });
    }
    // the photo must have its size before it can fly (the thumbnail is in the cache, so this is a frame or two)
    if (img.complete && img.naturalWidth) requestAnimationFrame(start);
    else { if (img.decode) img.decode().then(start, start); img.addEventListener("load", start, { once: true }); setTimeout(start, 300); }
  }
  function flip(from, to) {   // the transform that puts the viewer's photo (at `to`) over a cell (at `from`)
    var s = from.width / Math.max(1, to.width);
    return "translate(" + (from.left + from.width / 2 - (to.left + to.width / 2)).toFixed(1) + "px," +
      (from.top + from.height / 2 - (to.top + to.height / 2)).toFixed(1) + "px) scale(" + s.toFixed(4) + ")";
  }
  function lift(th, opening, done) {
    var c = th.getBoundingClientRect(), v = img.getBoundingClientRect();
    if (!c.width || !v.width || c.bottom < 0 || c.top > innerHeight) { if (done) done(); return; }
    var at = flip(c, v);
    lb.classList.add("is-lift");
    var an = img.animate(opening ? [{ transform: at }, { transform: "none" }] : [{ transform: "none" }, { transform: at }],
      { duration: opening ? 340 : 280, easing: opening ? EASE : "cubic-bezier(.4,0,.2,1)", fill: opening ? "none" : "forwards" });
    an.onfinish = function () { lb.classList.remove("is-lift"); if (done) done(); };
    an.oncancel = an.onfinish;
  }
  function go(k) {
    var j = Z.i + k; if (!lb.open || j < 0 || j >= Z.set.length) return;
    Z.i = j; lb.classList.remove("is-buy");
    if (reduced()) { show(Z.set[j]); return; }
    img.style.opacity = "0";
    setTimeout(function () {
      show(Z.set[Z.i]);
      var done = function () { img.style.opacity = ""; };
      if (img.complete) done(); else { img.onload = done; setTimeout(done, 700); }
    }, 150);
  }
  function closeLb() {
    if (!lb.open || Z.closing) return; Z.closing = 1;
    var a = Z.set[Z.i];
    if (a && !all && dayOf(a) !== cur) openDay(dayOf(a), { keepHash: true });
    var f0 = a && a.closest(".gf-ph");
    // the photo goes back into its own cell (D): bring the cell on screen behind the viewer first, then fly there
    if (f0 && !reduced() && img.animate && Z.s <= 1.01) {
      var r0 = f0.getBoundingClientRect();
      if (r0.top < 90 || r0.bottom > innerHeight) f0.scrollIntoView({ block: "center" });
      lb.classList.remove("is-buy"); lb.classList.add("is-lift-out");
      lift(a.querySelector("img"), false, function () { finish(); });
      return;
    }
    lb.classList.remove("is-in", "is-buy");
    setTimeout(finish, reduced() ? 0 : 200);
    function finish() {
      if (lb.open) lb.close(); img.getAnimations && img.getAnimations().forEach(function (x) { x.cancel(); });
      img.removeAttribute("src"); lb.classList.remove("is-in", "is-zoomed", "is-drag", "is-lift", "is-lift-out"); Z.closing = 0;
      if (a) {   // back to the cell of the last photo seen (Trim's idea), so the place among 50 is never lost
        var f = a.closest(".gf-ph"), r = f.getBoundingClientRect();
        if (r.top < 90 || r.bottom > innerHeight) f.scrollIntoView({ block: "center" });
        a.focus({ preventScroll: true });
        if (!reduced()) { f.classList.remove("is-last"); void f.offsetWidth; f.classList.add("is-last"); }
        setHash(all ? "" : "#" + days[dayOf(a)].id);
      }
    }
  }
  days.forEach(function (sec) {
    [].forEach.call(sec.querySelectorAll("a[data-stem]"), function (a) {
      a.addEventListener("click", function (e) { if (e.metaKey || e.ctrlKey || e.shiftKey) return; e.preventDefault(); openLb(a); });
    });
  });
  bPrev.addEventListener("click", function () { go(-1); });
  bNext.addEventListener("click", function () { go(1); });
  lb.querySelector(".gfv-x").addEventListener("click", closeLb);
  lb.addEventListener("cancel", function (e) { e.preventDefault(); if (lb.classList.contains("is-buy")) closeSheet(); else closeLb(); });
  stage.addEventListener("click", function (e) {
    if (Z.moved > 6) { Z.moved = 0; return; }
    var r = img.getBoundingClientRect(), onImg = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
    if (onImg) { var next = Z.s < 1.5 ? 2 : Z.s < 3 ? 3.5 : 1; zoomAt(next / Z.s, e.clientX, e.clientY); return; }
    closeLb();
  });
  stage.addEventListener("wheel", function (e) { e.preventDefault(); zoomAt(Math.exp(-clamp(e.deltaY, -80, 80) * 0.004), e.clientX, e.clientY); }, { passive: false });
  stage.addEventListener("pointerdown", function (e) {
    Z.ptrs[e.pointerId] = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY }; var ids = Object.keys(Z.ptrs); Z.moved = 0;
    if (ids.length === 2) { var A = Z.ptrs[ids[0]], B = Z.ptrs[ids[1]]; Z.pinch = { span: Math.hypot(A.x - B.x, A.y - B.y), cx: (A.x + B.x) / 2, cy: (A.y + B.y) / 2 }; }
    if (stage.setPointerCapture) stage.setPointerCapture(e.pointerId); if (e.target === img && Z.s > 1.01) lb.classList.add("is-drag"); e.preventDefault();
  });
  stage.addEventListener("pointermove", function (e) {
    var p = Z.ptrs[e.pointerId]; if (!p) return; var dx = e.clientX - p.x, dy = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY; Z.moved += Math.abs(dx) + Math.abs(dy);
    var ids = Object.keys(Z.ptrs);
    if (ids.length >= 2 && Z.pinch) {
      var A = Z.ptrs[ids[0]], B = Z.ptrs[ids[1]], span = Math.hypot(A.x - B.x, A.y - B.y), cx = (A.x + B.x) / 2, cy = (A.y + B.y) / 2;
      if (Z.pinch.span > 0) zoomAt(span / Math.max(1, Z.pinch.span), cx, cy);
      Z.x += cx - Z.pinch.cx; Z.y += cy - Z.pinch.cy; Z.pinch.span = span; Z.pinch.cx = cx; Z.pinch.cy = cy; clampPan(); apply(); return;
    }
    if (Z.s > 1.01) { Z.x += dx; Z.y += dy; clampPan(); apply(); }
  });
  function up(e) {
    var p = Z.ptrs[e.pointerId]; delete Z.ptrs[e.pointerId]; var ids = Object.keys(Z.ptrs); if (ids.length < 2) Z.pinch = null; lb.classList.remove("is-drag");
    if (p && !ids.length && Z.s <= 1.01 && !Z.pinch) { var dx = e.clientX - p.sx, dy = e.clientY - p.sy; if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) { Z.moved = 99; go(dx < 0 ? 1 : -1); } }
  }
  stage.addEventListener("pointerup", up); stage.addEventListener("pointercancel", up);
  d.addEventListener("keydown", function (e) {
    if (!lb.open || lb.classList.contains("is-buy")) return;
    if (e.key === "+" || e.key === "=") zoomAt(1.3, innerWidth / 2, innerHeight / 2);
    else if (e.key === "-") zoomAt(1 / 1.3, innerWidth / 2, innerHeight / 2);
    else if (e.key === "0") zoomAt(1 / Z.s, 0, 0);
    else if (e.key === "ArrowRight") { e.preventDefault(); go(1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
  });

  /* ---------------------------------------------------------------- Save, free: the 2400 web copy, by name */
  var saveLabel = save.textContent;
  function resetSave() { save.textContent = saveLabel; save.classList.remove("is-busy"); save.removeAttribute("aria-busy"); }
  function say(t, busy) { save.textContent = t; save.classList.toggle("is-busy", !!busy); if (busy) save.setAttribute("aria-busy", "true"); else save.removeAttribute("aria-busy"); }
  function toFile(stem) { var b = blobs[stem]; try { return new File([b], stem + ".jpg", { type: b.type || "image/jpeg" }); } catch (e) { return null; } }
  function toJpeg(b) {   // WebP in, JPEG out (same pixels, quality .92); the WebP itself if the browser cannot
    return new Promise(function (res) {
      var u = URL.createObjectURL(b), im = new Image();
      im.onload = function () {
        try {
          var c = d.createElement("canvas"); c.width = im.naturalWidth; c.height = im.naturalHeight;
          c.getContext("2d").drawImage(im, 0, 0);
          c.toBlob(function (j) { URL.revokeObjectURL(u); res(j || b); }, "image/jpeg", 0.92);
        } catch (e) { URL.revokeObjectURL(u); res(b); }
      };
      im.onerror = function () { URL.revokeObjectURL(u); res(b); };
      im.src = u;
    });
  }
  function deliver(stem) {
    var file = toFile(stem), touch = w.matchMedia && matchMedia("(pointer: coarse)").matches;
    if (touch && file && navigator.canShare && navigator.canShare({ files: [file] })) {
      // phones: the share sheet (Save Image puts it in Photos; or straight into Instagram or WhatsApp)
      return navigator.share({ files: [file], title: stem }).then(function () { say("Saved"); }, function (err) {
        if (err && err.name === "AbortError") { resetSave(); return; }
        say("Tap again to save");   // the fetch took longer than the tap allows: the copy is ready now
      });
    }
    var u = URL.createObjectURL(blobs[stem]), a = d.createElement("a");
    a.href = u; a.download = stem + (blobs[stem].type === "image/jpeg" ? ".jpg" : ".webp"); a.style.display = "none"; d.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(u); }, 4000);
    say("Saved");
  }
  save.addEventListener("click", function (e) {
    var a = Z.set[Z.i]; if (!a || !w.fetch || !w.Blob) return;   // no fetch: the plain link opens the copy
    e.preventDefault();
    var stem = a.getAttribute("data-stem");
    if (blobs[stem]) { deliver(stem); return; }
    say("Getting it", true);
    fetch(url(a, 2400), { mode: "cors" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.blob(); })
      .then(toJpeg).then(function (b) { blobs[stem] = b; if (Z.set[Z.i] === a) deliver(stem); })
      .catch(function () { resetSave(); w.open(url(a, 2400), "_blank", "noopener"); });
  });

  /* ---------------------------------------------------------------- Original, EUR 1: the sheet */
  function openSheet() { lb.classList.add("is-buy"); setTimeout(function () { lb.querySelector(".gfv-sheet-t").focus({ preventScroll: true }); }, reduced() ? 0 : 60); }
  function closeSheet() { lb.classList.remove("is-buy"); if (buy) buy.focus({ preventScroll: true }); }
  if (buy) buy.addEventListener("click", openSheet);     // the EUR 1 original: off while the Patreon button stands in
  back.addEventListener("click", closeSheet);
  pay.addEventListener("click", function (e) {
    var link = data.pay || "";
    if (link) { pay.href = link.replace("{stem}", encodeURIComponent(Z.set[Z.i].getAttribute("data-stem"))); pay.target = "_blank"; pay.rel = "noopener"; return; }
    e.preventDefault(); payNote.classList.add("is-lit");   // the owner's PayPal is not set up yet: the link is [to supply]
  });
  copy.addEventListener("click", function () {
    var stem = Z.set[Z.i].getAttribute("data-stem");
    function ok() { copy.textContent = "Copied"; }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(stem).then(ok, function () {});
    else { var r = d.createRange(); r.selectNodeContents(lb.querySelector(".gfv-ref-n")); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  });

  /* ---------------------------------------------------------------- where to start */
  function fromHash(o) {
    var h = decodeURIComponent((location.hash || "").slice(1));
    var di = days.findIndex ? days.findIndex(function (s) { return s.id === h; }) : -1;   // a task by its own name (#task-1, #practice)
    if (di >= 0) { openDay(di, o); return true; }
    if (h) {
      var f = d.getElementById(h);
      if (f && f.classList.contains("gf-ph") && f.closest(".gf-day").getAttribute("data-state") === "photos") {
        openDay(dayOf(f.querySelector("a")), { keepHash: true, arrive: o.arrive });
        openLb(f.querySelector("a"));
        return true;
      }
    }
    return false;
  }
  var startAt = latest >= 0 ? latest : Math.max(0, Math.min(N - 1, flownTo));
  if (!fromHash({ arrive: false, keepHash: true })) openDay(startAt, { keepHash: true });
  // the arrival: the glider flies the comp so far, from Task 1 to the day that opens, as the flown line draws
  if (!reduced() && cur > 0 && glw.animate) {
    var target = cur;
    line.style.setProperty("--open", 0);
    var go2 = function () {
      fly(0, target);
      if (flown.animate) flown.animate([{ transform: "scaleX(0)" }, { transform: "scaleX(" + (Math.max(0, flownTo) / Math.max(1, N - 1)) + ")" }], { duration: Math.min(1000, 380 + 150 * target), easing: "cubic-bezier(.45,0,.25,1)" });
    };
    setTimeout(function () { requestAnimationFrame(go2); }, 450);
  }
  w.addEventListener("hashchange", function () { if (!lb.open) fromHash({ scroll: true }); });
})();
