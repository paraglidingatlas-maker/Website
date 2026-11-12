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
    var say = { photos: (info.n || 0) + (info.n === 1 ? " photo" : " photos") + (info.film ? " and the highlights film" : ""), today: "flying today, photos tonight", coming: "photos coming", soon: "to come" }[st];
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
  var nameEl = lb.querySelector(".gfv-name"), whereEl = lb.querySelector(".gfv-where"), pxEl = lb.querySelector(".gfv-px"), crEl = lb.querySelector(".gfv-cr"), origEl = lb.querySelector(".gfv-orig");
  var shareB = lb.querySelector(".gfv-share");
  var save = lb.querySelector(".gfv-save"), buy = lb.querySelector(".gfv-buy"), pay = lb.querySelector(".gfv-pay"), back = lb.querySelector(".gfv-back");
  var copy = lb.querySelector(".gfv-copy"), refs = lb.querySelectorAll(".gfv-ref-n, .gfv-ref-n2"), payNote = lb.querySelector(".gfv-paynote");
  var Z = { s: 1, x: 0, y: 0, ptrs: {}, pinch: null, moved: 0, closing: 0, set: [], i: 0, req: {}, got: {} };
  var blobs = {};
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function apply() { img.style.transform = "translate(" + Z.x.toFixed(1) + "px," + Z.y.toFixed(1) + "px) scale(" + Z.s.toFixed(3) + ")"; Z.as = Z.s; Z.ax = Z.x; Z.ay = Z.y; lb.classList.toggle("is-zoomed", Z.s > 1.01); }
  function drawn() {   // the photo's size at scale 1, as the screen draws it (its box can differ from its pixels)
    var r = img.getBoundingClientRect(), k = Z.as || 1; return { w: r.width / k, h: r.height / k };
  }
  function fit() {     // the photo's height limit is the stage's real height (a % height does not hold in its grid)
    lb.style.setProperty("--gfv-h", stage.clientHeight + "px"); lb.style.setProperty("--gfv-w", stage.clientWidth + "px");
  }
  w.addEventListener("resize", function () { if (lb.open) { fit(); if (Z.s > 1.01) { clampPan(); apply(); } } });
  function fill() {    // the scale at which the photo covers the whole screen
    var b = drawn(); return b.w && b.h ? Math.max(innerWidth / b.w, innerHeight / b.h) : 2;
  }
  function clampPan() {
    if (Z.s <= 1.01) { Z.x = Z.y = 0; return; }
    // zoomed, the photo has the whole screen (owner, 9 Nov): its edges stop at the screen's, centred if smaller
    // the photo's resting centre: where it is drawn now, less the move applied to it
    var b = drawn(), iw = b.w * Z.s, ih = b.h * Z.s, q = img.getBoundingClientRect();
    var cx = q.left + q.width / 2 - (Z.ax || 0), cy = q.top + q.height / 2 - (Z.ay || 0), W = innerWidth, H = innerHeight;
    Z.x = iw <= W ? W / 2 - cx : clamp(Z.x, W - cx - iw / 2, iw / 2 - cx);
    Z.y = ih <= H ? H / 2 - cy : clamp(Z.y, H - cy - ih / 2, ih / 2 - cy);
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
    if (crEl) { if (crEl._d == null) crEl._d = crEl.textContent; crEl.textContent = info.cred ? "Photo: " + info.cred : crEl._d; }
    pos.textContent = (Z.i + 1) + " of " + Z.set.length;
    lb.style.setProperty("--gfv-p", ((Z.i + 1) / Z.set.length).toFixed(4));   // the dock's line on a phone
    bPrev.disabled = Z.i <= 0; bNext.disabled = Z.i >= Z.set.length - 1;
    save.href = url(a, 2400); save.setAttribute("download", stem + ".jpg");
    if (origEl) { if (data.orig) { origEl.href = data.orig + stem + ".jpg"; origEl.hidden = false; } else origEl.hidden = true; }
    resetSave();
    [].forEach.call(refs, function (r) { r.textContent = stem; });
    copy.textContent = "Copy name"; payNote.classList.remove("is-lit");
    apply();
    setHash("#" + stem);
    // Share: the photo's own preview page (v4_comp_gallery.py share_stubs), so a link preview shows this photo
    if (shareB) { shareB.setAttribute("data-share-url", "/photo/" + stem + ".html"); shareB.setAttribute("data-share-title", whereEl.textContent); }
  }
  function openLb(a, o) {
    o = o || {};
    Z.set = [].slice.call((all ? main : a.closest(".gf-grid")).querySelectorAll(all ? ".gf-day[data-state=photos] a[data-stem]" : "a[data-stem]"));
    Z.i = Math.max(0, Z.set.indexOf(a)); Z.ptrs = {}; Z.pinch = null; Z.closing = 0;
    lb.classList.remove("is-in", "is-buy"); img.style.transform = "";
    show(a);
    if (lb.showModal) { if (!lb.open) lb.showModal(); } else lb.setAttribute("open", "");
    fit();
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
  lb.addEventListener("cancel", function (e) {
    e.preventDefault();
    if (lb.classList.contains("is-buy")) closeSheet();
    else if (Z.s > 1.01) zoomAt(1 / Z.s, innerWidth / 2, innerHeight / 2);     // out of the zoom first
    else closeLb();
  });
  stage.addEventListener("click", function (e) {
    if (Z.moved > 6) { Z.moved = 0; return; }
    var r = img.getBoundingClientRect(), onImg = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
    // first tap: the photo fills the whole screen; second: closer still; third: back (owner, 9 Nov)
    if (onImg) { var f = Math.max(1.6, fill()), next = Z.s < 1.05 ? f : Z.s < f * 1.5 ? Math.min(6, f * 2) : 1; zoomAt(next / Z.s, e.clientX, e.clientY); return; }
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
    if (Z.s > 1.01) { Z.x += dx; Z.y += dy; clampPan(); apply(); return; }
    var tx = e.clientX - p.sx, ty = e.clientY - p.sy;
    if (ids.length === 1 && (Z.pull || (ty > 12 && ty > Math.abs(tx) * 1.3))) {
      Z.pull = Math.max(0, ty);
      img.style.transition = "none";
      img.style.transform = "translate(" + (tx * 0.3).toFixed(1) + "px," + Z.pull.toFixed(1) + "px) scale(" + (1 - Math.min(0.18, Z.pull / 1400)).toFixed(3) + ")";
      lb.style.backgroundColor = "rgba(14,15,18," + Math.max(0.25, 1 - Z.pull / 420).toFixed(3) + ")";
      lb.classList.add("is-pull");
    }
  });
  function up(e) {
    var p = Z.ptrs[e.pointerId]; delete Z.ptrs[e.pointerId]; var ids = Object.keys(Z.ptrs); if (ids.length < 2) Z.pinch = null; lb.classList.remove("is-drag");
    if (Z.pull) {                                  // a swipe down: far enough closes, else the photo settles back
      var far = Z.pull > 110; Z.pull = 0; Z.moved = 99; lb.classList.remove("is-pull");
      img.style.transition = ""; lb.style.backgroundColor = "";
      if (far) { closeLb(); } else { img.style.transform = ""; apply(); }
      return;
    }
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

  /* ---------------------------------------------------------------- the films (owner, 9 Nov 2026)
     A task with a Daily Highlights film opens with a band. Tapped, the band's photo lifts off the page and opens into
     the theatre, re-cropped as it grows (transform only), and the film plays there in YouTube's privacy-enhanced
     player, loaded only now. Where a visitor stopped is kept in this browser: the band shows how far they got and the
     film plays on from there. At its end the day's photos are one tap away. The lead carries the newest film's cue.
     No JS, or the claude.ai preview (html[data-md-out]): the band and the cue are links to the film on YouTube. */
  var film = { open: function () { return false; } };
  var fv = d.getElementById("gffv");
  if (fv && !root.hasAttribute("data-md-out")) {
    try { film = films(); } catch (err) { root.classList.remove("gff-js"); }
  }
  function films() {
    var F = data.films || {};
    var bands = [].slice.call(d.querySelectorAll(".gff[data-film]"));
    var frame = fv.querySelector(".gffv-frame"), pic = fv.querySelector(".gffv-pic"), pimg = pic.querySelector("img"),
        amb = fv.querySelector(".gffv-amb img"), box = fv.querySelector(".gffv-player"), endEl = fv.querySelector(".gffv-end"),
        resume = fv.querySelector(".gffv-resume"), photosA = fv.querySelector(".gffv-photos"), again = fv.querySelector(".gffv-again");
    var S = { id: "", band: null, from: null, player: null, timer: 0, start: 0, closing: false, hash: "", api: null };
    function fine() { return !!(w.matchMedia && w.matchMedia("(hover: hover) and (pointer: fine)").matches); }

    /* where a visitor stopped, in this browser only (a private window keeps nothing: the band simply says Play) */
    function load(id) { try { var v = JSON.parse(localStorage.getItem("gff-" + id) || "null"); return v && typeof v === "object" ? v : null; } catch (e) { return null; } }
    function keep(id, v) { try { localStorage.setItem("gff-" + id, JSON.stringify(v)); } catch (e) {} }
    function mmss(t) { t = Math.max(0, Math.floor(t)); return Math.floor(t / 60) + ":" + ("0" + t % 60).slice(-2); }
    function resumable(id) { var f = F[id] || {}, p = load(id); return p && !p.end && p.t >= 10 && p.t < (f.secs || 1e9) - 15 ? Math.floor(p.t) : 0; }
    function paint(band) {
      var id = band.getAttribute("data-film"), f = F[id]; if (!f) return;
      var p = load(id), at = resumable(id), mode = at ? "resume" : p && p.end ? "again" : "play";
      var a = band.querySelector(".gff-play"), cta = band.querySelector("[data-cta]"), sub = band.querySelector("[data-cta-s]");
      if (a._name == null) a._name = a.getAttribute("aria-label");
      band.setAttribute("data-mode", mode);
      band.style.setProperty("--done", at ? (100 * at / f.secs).toFixed(1) : "0");
      if (cta) cta.textContent = mode === "resume" ? "Resume the film" : mode === "again" ? "Watch again" : "Play the film";
      if (sub) sub.textContent = mode === "resume" ? "from " + mmss(at) + " of " + f.len : f.len;
      var note = band.querySelector(".gff-at");      // a phone shows no button words: the kicker says it
      if (note) { note.hidden = mode === "play"; note.textContent = mode === "resume" ? "Paused at " + mmss(at) : mode === "again" ? "Watched" : ""; }
      a.setAttribute("aria-label", mode === "resume" ? "Resume the film from " + mmss(at) + ", " + f.title + ", " + f.len
        : mode === "again" ? "Watch the film again, " + f.title + ", " + f.len : a._name);
    }
    bands.forEach(paint);

    /* the band's way in, once, as it comes on screen */
    root.classList.add("gff-js");
    function seen(b) { b.classList.add("is-seen"); }
    if (reduced() || !w.IntersectionObserver) bands.forEach(seen);
    else {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { seen(e.target); io.unobserve(e.target); } });
      }, { threshold: 0.2 });
      bands.forEach(function (b) { io.observe(b); });
    }
    /* a mouse: the play button leans towards the pointer (translate only) */
    if (fine() && !reduced()) bands.forEach(function (b) {
      var btn = b.querySelector(".gff-btn"), raf = 0, x = 0, y = 0;
      function set() { raf = 0; btn.style.translate = x.toFixed(1) + "px " + y.toFixed(1) + "px"; }
      b.addEventListener("pointermove", function (e) {
        if (e.pointerType !== "mouse") return;
        var q = btn.getBoundingClientRect(), cx = q.left + q.width / 2 - x, cy = q.top + q.height / 2 - y;
        var dx = e.clientX - cx, dy = e.clientY - cy, k = Math.max(0, 1 - Math.hypot(dx, dy) / 340);
        x = clamp(dx * 0.32 * k, -34, 34); y = clamp(dy * 0.32 * k, -26, 26);
        if (!raf) raf = requestAnimationFrame(set);
      });
      b.addEventListener("pointerleave", function () { x = y = 0; if (!raf) raf = requestAnimationFrame(set); });
    });

    /* YouTube: warm the connection on intent, load the player's code on the press, the player itself once open */
    var warmed = 0;
    function warm() {
      if (warmed) return; warmed = 1;
      ["https://www.youtube-nocookie.com", "https://www.youtube.com", "https://i.ytimg.com"].forEach(function (h) {
        var l = d.createElement("link"); l.rel = "preconnect"; l.href = h; d.head.appendChild(l);
      });
    }
    function api() {
      if (S.api) return S.api;
      S.api = new Promise(function (res, rej) {
        if (w.YT && w.YT.Player) { res(w.YT); return; }
        var prev = w.onYouTubeIframeAPIReady;
        w.onYouTubeIframeAPIReady = function () { if (typeof prev === "function") { try { prev(); } catch (e) {} } res(w.YT); };
        var s = d.createElement("script"); s.src = "https://www.youtube.com/iframe_api"; s.async = true;
        s.onerror = function () { rej(new Error("api")); };
        d.head.appendChild(s);
        setTimeout(function () { if (!(w.YT && w.YT.Player)) rej(new Error("slow")); }, 7000);
      });
      S.api.catch(function () { S.api = null; });
      return S.api;
    }
    function ready() { if (fv.open && !S.closing) { fv.classList.add("is-ready"); fv.classList.remove("is-loading"); } }
    function player() {
      var id = S.id, f = F[id], mount = d.createElement("div");
      box.textContent = ""; box.appendChild(mount);
      fv.classList.add("is-loading");
      api().then(function (YT) {
        if (S.id !== id || !fv.open || S.closing) return;
        S.player = new YT.Player(mount, {
          host: "https://www.youtube-nocookie.com", videoId: id, width: "100%", height: "100%",
          playerVars: { autoplay: 1, playsinline: 1, rel: 0, iv_load_policy: 3, start: S.start || 0, origin: location.origin },
          events: {
            onReady: function (e) {
              try { e.target.getIframe().title = f.title + ", on YouTube"; } catch (x) {}
              try { e.target.playVideo(); } catch (x) {}
              setTimeout(ready, 1500);       // autoplay refused (often on a phone): YouTube's own play button shows
            },
            onStateChange: function (e) { state(e.data); },
            onError: ready
          }
        });
      }, function () {                       // the player's code did not come: the player alone, as on the other media pages
        if (S.id !== id || !fv.open || S.closing) return;
        var fr = d.createElement("iframe");
        fr.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0&playsinline=1" + (S.start ? "&start=" + S.start : "");
        fr.title = f.title + ", on YouTube"; fr.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen"; fr.setAttribute("allowfullscreen", "");
        fr.addEventListener("load", function () { setTimeout(ready, 700); });
        if (mount.parentNode) box.replaceChild(fr, mount);
      });
    }
    function state(s) {
      if (s === 1) {
        ready(); if (!endEl.hidden) { endEl.hidden = true; fv.classList.remove("is-ended"); }
        if (!resume.hidden && !S.fade) S.fade = setTimeout(function () { resume.classList.add("is-gone"); }, 7000);
      }
      else if (s === 0) ended();
      if (s === 2) save();
    }
    function save() {
      var p = S.player, f = F[S.id]; if (!p || !p.getCurrentTime || !f) return;
      try {
        var t = p.getCurrentTime() || 0, du = p.getDuration() || f.secs;
        if (p.getPlayerState() === 0 || (t && t >= du - 15)) keep(S.id, { end: 1, at: Date.now() });
        else if (t > 0) keep(S.id, { t: Math.floor(t), at: Date.now() });
      } catch (e) {}
    }
    function ended() {
      var f = F[S.id]; if (!f) return;
      keep(S.id, { end: 1, at: Date.now() });
      var info = (data.days || [])[f.day] || {};
      fv.querySelector(".gffv-end-k").textContent = (info.name ? info.name + " · " : "") + "Daily Highlights";
      photosA.querySelector("span").textContent = info.n ? "See all " + info.n + " photos" : "See the photos";
      photosA.href = "#" + (days[f.day] ? days[f.day].id : "");
      endEl.hidden = false; fv.classList.add("is-ended");
      fv.classList.remove("is-ready");     // the film steps back: the end card lies over the day's own photo
      resume.classList.add("is-gone");
      if (!reduced() && endEl.animate) endEl.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 450, easing: EASE });
      photosA.focus({ preventScroll: true });
    }

    /* the theatre's geometry: the band's photo, re-cropped frame by frame as it becomes the film's frame.
       The frame scales from the band's box to its own (by transform, from its top left corner); the photo inside it is
       scaled back so it never stretches, and placed so the crop moves smoothly from the band's to the frame's. */
    function bez(x1, y1, x2, y2) {
      function c(t, a, b) { return ((1 - 3 * b + 3 * a) * t + (3 * b - 6 * a)) * t * t + 3 * a * t; }
      return function (x) {
        if (x <= 0 || x >= 1) return x <= 0 ? 0 : 1;
        var lo = 0, hi = 1, t = x;
        for (var i = 0; i < 24; i++) { var v = c(t, x1, x2); if (Math.abs(v - x) < 1e-5) break; if (v < x) lo = t; else hi = t; t = (lo + hi) / 2; }
        return c(t, y1, y2);
      };
    }
    var IN = bez(0.2, 0.8, 0.2, 1), OUT = bez(0.45, 0, 0.2, 1);
    function cover(bw, bh, nw, nh, ox, oy) {   // a photo laid to cover a box: its scale, and its centre's offset from the box's
      var s = Math.max(bw / nw, bh / nh);
      return { s: s, x: (nw * s - bw) * (0.5 - ox), y: (nh * s - bh) * (0.5 - oy) };
    }
    function opos(el) {
      var p = (getComputedStyle(el).objectPosition || "50% 50%").split(" ");
      function f(v) { return /%$/.test(v || "") ? parseFloat(v) / 100 : 0.5; }
      return [f(p[0]), f(p[1])];
    }
    function zoomOf(el) {   // the band photo's own scale at this moment (its hover, its way in)
      var cs = getComputedStyle(el), k = 1, m = cs.transform, v = m && m !== "none" && m.match(/matrix\(([^)]+)\)/);
      if (v) k *= parseFloat(v[1].split(",")[0]) || 1;
      if (cs.scale && cs.scale !== "none") k *= parseFloat(cs.scale) || 1;
      return k;
    }
    function morph(media, opening) {
      var bimg = media.querySelector("img"), B = media.getBoundingClientRect(), R = frame.getBoundingClientRect();
      var nw = +bimg.getAttribute("width") || 16, nh = +bimg.getAttribute("height") || 9;
      var oB = opos(bimg), k0 = zoomOf(bimg), cF = cover(R.width, R.height, nw, nh, 0.5, 0.5);
      var n = 30, kf = [], kp = [];
      for (var i = 0; i <= n; i++) {
        var e = opening ? IN(i / n) : 1 - OUT(i / n);
        var W = { l: B.left + (R.left - B.left) * e, t: B.top + (R.top - B.top) * e, w: B.width + (R.width - B.width) * e, h: B.height + (R.height - B.height) * e };
        var kz = k0 + (1 - k0) * e, cW = cover(W.w, W.h, nw, nh, oB[0] + (0.5 - oB[0]) * e, oB[1] + (0.5 - oB[1]) * e);
        var sx = W.w / R.width, sy = W.h / R.height, sW = cW.s * kz, ax = sW / (sx * cF.s), ay = sW / (sy * cF.s);
        var tx = cW.x * kz / sx - ax * cF.x, ty = cW.y * kz / sy - ay * cF.y;
        kf.push({ transform: "translate(" + (W.l - R.left).toFixed(2) + "px," + (W.t - R.top).toFixed(2) + "px) scale(" + sx.toFixed(5) + "," + sy.toFixed(5) + ")" });
        kp.push({ transform: "translate(" + tx.toFixed(2) + "px," + ty.toFixed(2) + "px) scale(" + ax.toFixed(5) + "," + ay.toFixed(5) + ")" });
      }
      var o = { duration: opening ? 720 : 520, easing: "linear", fill: "both" };
      pic.animate(kp, o);
      return frame.animate(kf, o);
    }
    function grow(from, opening) {   // from somewhere that is not a band (the lead's cue, a link): the frame grows out of it
      var R = frame.getBoundingClientRect(), r = from && from.getBoundingClientRect && from.getBoundingClientRect(), s = 0.14;
      var x0 = r && r.width ? r.left + r.width / 2 - (R.left + R.width / 2) : 0, y0 = r && r.width ? r.top + r.height / 2 - (R.top + R.height / 2) : 30;
      var at = "translate(" + (x0 + R.width * (1 - s) / 2).toFixed(1) + "px," + (y0 + R.height * (1 - s) / 2).toFixed(1) + "px) scale(" + s + ")";
      var kf = opening ? [{ transform: at, opacity: 0 }, { transform: "none", opacity: 1 }] : [{ transform: "none", opacity: 1 }, { transform: at, opacity: 0 }];
      return frame.animate(kf, { duration: opening ? 560 : 420, easing: opening ? EASE : "cubic-bezier(.45,0,.2,1)", fill: "both" });
    }
    function stop(el) { if (el.getAnimations) el.getAnimations().forEach(function (a) { a.cancel(); }); }

    /* open, close */
    function open(id, from) {
      var f = F[id]; if (!f || fv.open || lb.open) return false;
      warm(); api();
      S.id = id; S.from = from || null; S.band = d.getElementById(f.band); S.closing = false; S.start = resumable(id); S.t0 = Date.now();
      S.hash = location.hash;
      fv.querySelector(".gffv-t").textContent = f.title;
      fv.querySelector(".gffv-len").textContent = f.len;
      fv.querySelector(".gffv-line").textContent = f.line || "";
      fv.querySelector(".gffv-yt").href = "https://www.youtube.com/watch?v=" + id + (S.start ? "&t=" + S.start + "s" : "");
      var shF = fv.querySelector(".gffv-share");
      if (shF) { shF.setAttribute("data-share-url", "https://www.youtube.com/watch?v=" + id); shF.setAttribute("data-share-title", f.title); }
      resume.hidden = !S.start; resume.classList.remove("is-gone"); clearTimeout(S.fade); S.fade = 0;
      if (S.start) resume.querySelector("span").textContent = "Playing on from " + mmss(S.start) + ".";
      endEl.hidden = true;
      fv.classList.remove("is-in", "is-ready", "is-ended", "is-loading");
      var bimg = S.band && S.band.querySelector(".gff-media img");
      pimg.src = (bimg && (bimg.currentSrc || bimg.src)) || f.amb; amb.src = f.amb;
      var fromBand = !!(from && S.band && S.band.contains(from)) && S.band.offsetParent !== null;
      var go = function () { if (!fv.open || S.closing) return; stop(frame); stop(pic); player(); clearInterval(S.timer); S.timer = setInterval(save, 2000); };
      if (reduced() || !frame.animate) {
        if (fv.showModal) fv.showModal(); else fv.setAttribute("open", "");
        fv.classList.add("is-in"); frame.focus({ preventScroll: true }); setHash("#" + f.band); go(); return true;
      }
      fv.classList.add("is-pre");
      if (fv.showModal) fv.showModal(); else fv.setAttribute("open", "");
      frame.focus({ preventScroll: true });
      setHash("#" + f.band);
      var started = false;
      function start() {
        if (started || !fv.open || S.closing) return; started = true;
        var an = fromBand ? morph(S.band.querySelector(".gff-media"), true) : grow(from, true);
        if (fromBand) S.band.classList.add("is-lifted");
        fv.classList.remove("is-pre");
        requestAnimationFrame(function () { fv.classList.add("is-in"); });
        an.onfinish = go;
      }
      // the photo must be decoded before it flies (it is the band's own, in the cache: a frame or two)
      if (pimg.decode) pimg.decode().then(start, start); else pimg.onload = start;
      setTimeout(start, 260);
      return true;
    }
    function close(after) {
      if (!fv.open || S.closing) return; S.closing = true;
      save(); clearInterval(S.timer);
      try { if (S.player && S.player.pauseVideo) S.player.pauseVideo(); } catch (e) {}
      var band = S.band, fromBand = !!(S.from && band && band.contains(S.from)) && band.offsetParent !== null;
      stop(frame); stop(pic);
      fv.classList.remove("is-in", "is-ready", "is-loading");
      if (reduced() || !frame.animate) { finish(after); return; }
      if (fromBand) {   // the band must be on screen, behind the theatre, for the photo to fly back into it
        var r = band.getBoundingClientRect();
        if (r.bottom < 80 || r.top > innerHeight - 80) band.scrollIntoView({ block: "center" });
      }
      var gone = S.from && !fromBand ? S.from.getBoundingClientRect() : null;
      var an = fromBand ? morph(band.querySelector(".gff-media"), false)
        : grow(gone && gone.bottom > 0 && gone.top < innerHeight ? S.from : null, false);
      an.onfinish = function () { finish(after); };
    }
    function finish(after) {
      try { if (S.player && S.player.destroy) S.player.destroy(); } catch (e) {}
      S.player = null; box.textContent = "";
      if (fv.open) fv.close();
      stop(frame); stop(pic);
      fv.classList.remove("is-in", "is-ready", "is-loading", "is-ended", "is-pre");
      pimg.removeAttribute("src");
      if (S.band) {
        var bd = S.band; bd.classList.add("is-landing"); bd.classList.remove("is-lifted"); paint(bd);
        void bd.offsetWidth; requestAnimationFrame(function () { requestAnimationFrame(function () { bd.classList.remove("is-landing"); }); });
      }
      setHash(/^#film-/.test(S.hash) || !S.hash ? (all ? "" : "#" + days[Math.max(0, cur)].id) : S.hash);
      var back = S.from && d.body.contains(S.from) ? S.from : S.band && S.band.querySelector(".gff-play");
      if (back && !after) back.focus({ preventScroll: true });
      S.closing = false; S.id = "";
      if (after) after();
    }

    /* the ways in and out */
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest(".gff-play, [data-film-cue]");
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
      var b = a.closest(".gff"), id = a.getAttribute("data-film-cue") || (b && b.getAttribute("data-film"));
      if (!F[id]) return;
      e.preventDefault(); open(id, a);
    });
    d.addEventListener("pointerdown", function (e) { if (e.target.closest && e.target.closest(".gff-play, [data-film-cue]")) { warm(); api(); } });
    bands.forEach(function (b) { b.addEventListener("pointerenter", warm); b.addEventListener("focusin", warm); });
    [].forEach.call(d.querySelectorAll("[data-film-cue]"), function (c) { c.addEventListener("pointerenter", warm); c.addEventListener("focusin", warm); });
    fv.addEventListener("cancel", function (e) { e.preventDefault(); close(); });
    fv.querySelector(".gffv-x").addEventListener("click", function () { close(); });
    fv.addEventListener("click", function (e) {   // the dark ground closes it (not a double tap's second tap, just after opening)
      var t = e.target; if (Date.now() - S.t0 < 700) return;
      if (t === fv || t.classList.contains("gffv-stage") || t.classList.contains("gffv-bg")) close();
    });
    again.addEventListener("click", function () {
      endEl.hidden = true; fv.classList.remove("is-ended"); keep(S.id, { t: 0, at: Date.now() });
      try { S.player.seekTo(0, true); S.player.playVideo(); } catch (e) {}
      frame.focus({ preventScroll: true });
    });
    fv.querySelector(".gffv-over").addEventListener("click", function () {
      S.start = 0; resume.hidden = true; keep(S.id, { t: 0, at: Date.now() });
      try { S.player.seekTo(0, true); S.player.playVideo(); } catch (e) {}
      frame.focus({ preventScroll: true });
    });
    photosA.addEventListener("click", function (e) {
      e.preventDefault();
      var f = F[S.id]; if (!f) return; var di = f.day;
      close(function () {
        if (!all && cur !== di) openDay(di, { keepHash: true });
        setHash(all ? "" : "#" + days[di].id);
        var g = days[di].querySelector(".gf-grid") || days[di], top = g.getBoundingClientRect().top;
        w.scrollTo({ top: Math.max(0, w.scrollY + top - line.offsetHeight - 14), behavior: reduced() ? "auto" : "smooth" });
        var a = g.querySelector("a[data-stem]"); if (a) a.focus({ preventScroll: true });
      });
    });
    // the keys YouTube's own player answers to, while the theatre (not the player inside it) has the focus
    fv.addEventListener("keydown", function (e) {
      var p = S.player, k = e.key, onCtl = /^(BUTTON|A|INPUT)$/.test(e.target.tagName);
      if (!p || !p.getPlayerState || e.altKey || e.ctrlKey || e.metaKey) return;
      try {
        if ((k === " " && !onCtl) || k === "k" || k === "K") { e.preventDefault(); if (p.getPlayerState() === 1) p.pauseVideo(); else p.playVideo(); }
        else if (k === "ArrowRight" || k === "l" || k === "L") { e.preventDefault(); p.seekTo(Math.min(p.getDuration() - 0.5, p.getCurrentTime() + (k === "ArrowRight" ? 5 : 10)), true); }
        else if (k === "ArrowLeft" || k === "j" || k === "J") { e.preventDefault(); p.seekTo(Math.max(0, p.getCurrentTime() - (k === "ArrowLeft" ? 5 : 10)), true); }
        else if (k === "m" || k === "M") { if (p.isMuted()) p.unMute(); else p.mute(); }
        else if (k === "f" || k === "F") { var fr = p.getIframe(), rq = fr.requestFullscreen || fr.webkitRequestFullscreen; if (rq) rq.call(fr); }
      } catch (x) {}
    });
    w.addEventListener("pagehide", save);
    return { open: function (id, from) { return open(id, from); }, band: function (h) { var b = d.getElementById(h); return b && b.classList.contains("gff") ? b : null; } };
  }

  /* ---------------------------------------------------------------- where to start */
  function fromHash(o) {
    var h = decodeURIComponent((location.hash || "").slice(1));
    var di = days.findIndex ? days.findIndex(function (s) { return s.id === h; }) : -1;   // a task by its own name (#task-1, #practice)
    if (di >= 0) { openDay(di, o); return true; }
    var fb = film.band && /^film-/.test(h) ? film.band(h) : null;   // a task's film (#film-task-1): its task, then the theatre
    if (fb) {
      openDay(+fb.closest(".gf-day").getAttribute("data-i"), { keepHash: true, arrive: o.arrive });
      setTimeout(function () { film.open(fb.getAttribute("data-film"), null); }, 500);
      return true;
    }
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
