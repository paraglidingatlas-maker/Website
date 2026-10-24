/* The library, option E: the ridge and the voices. No sound here. Nothing moves unless the visitor scrolls or touches. */
(function () {
  "use strict";
  var dataEl = document.getElementById("v4l-data"); if (!dataEl) return;
  var D; try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var NS = "http://www.w3.org/2000/svg", EPS = D.eps, bySlug = {}; EPS.forEach(function (e) { bySlug[e.s] = e; });
  var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var small = window.matchMedia && window.matchMedia("(max-width: 700px)").matches;
  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function ease(u) { return u * u * (3 - 2 * u); }
  var BASE = D.base || "";
  function still(e) { return e.i ? BASE + "img/library/stills/s/" + e.i + ".webp" : ""; }
  function epUrl(s) { return BASE + "episodes/" + s + ".html"; }

  /* ---------- the ridge: one column a conversation, drawn into an svg ---------- */
  function drawRidge(svg, H, pad) {                          // returns the lines by slug
    var W = 1000, lines = {}, pts = [];
    var defs = document.createElementNS(NS, "defs"); defs.innerHTML = '<linearGradient id="v4l-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7517" stop-opacity=".10"/><stop offset="1" stop-color="#141519" stop-opacity="0"/></linearGradient>'; svg.appendChild(defs);
    var area = document.createElementNS(NS, "path"); area.setAttribute("class", "v4l-area"); svg.appendChild(area);
    var dated = EPS.filter(function (e) { return e.x >= 0; });
    dated.forEach(function (e) {
      var x = pad + e.x * (W - 2 * pad), h = Math.max(6, e.h * H * 0.9); pts.push([x, H - h]);
      var l = document.createElementNS(NS, "line"); l.setAttribute("x1", x.toFixed(1)); l.setAttribute("x2", x.toFixed(1)); l.setAttribute("y1", H); l.setAttribute("y2", (H - h).toFixed(1)); l.setAttribute("data-s", e.s); l.setAttribute("vector-effect", "non-scaling-stroke"); svg.appendChild(l); lines[e.s] = { el: l, x: x, y: H - h };
    });
    area.setAttribute("d", "M" + pad + " " + H + " " + pts.map(function (p) { return "L" + p[0].toFixed(1) + " " + (p[1] + 8).toFixed(1); }).join(" ") + " L" + (W - pad) + " " + H + " Z");
    return lines;
  }

  /* ---------- the flight ---------- */
  var fly = document.getElementById("flight");
  if (fly) {
    var pin = fly.querySelector(".v4l-fly-pin"), svg = fly.querySelector(".v4l-rs"), stops = [].slice.call(fly.querySelectorAll(".v4l-stop")), q = fly.querySelector(".v4l-q");
    var qn = q.querySelector(".v4l-qn"), qs = q.querySelector(".v4l-qs"), qd = q.querySelector(".v4l-qd"), qt = q.querySelector(".v4l-qt"), qw = q.querySelector(".v4l-qw"), qo = q.querySelector(".v4l-open");
    var yearB = fly.querySelector(".v4l-year b"), yi = fly.querySelector(".v4l-yi"), tip = fly.querySelector(".v4l-tip"), yrs = fly.querySelector(".v4l-yrs");
    var pad = 16, H = 300, lines = drawRidge(svg, H, pad), STOPS = D.stops, cur = -1, was = {};
    var mk = document.createElementNS(NS, "circle"); mk.setAttribute("class", "v4l-mk"); mk.setAttribute("r", "5"); var ring = document.createElementNS(NS, "circle"); ring.setAttribute("class", "v4l-ring"); ring.setAttribute("r", "12"); ring.setAttribute("vector-effect", "non-scaling-stroke"); svg.appendChild(ring); svg.appendChild(mk);
    // the years along the bottom
    var y0 = new Date(D.t0), y1 = new Date(D.t1), yl = [];
    for (var y = y0.getFullYear(); y <= y1.getFullYear(); y++) yl.push(y);
    yrs.innerHTML = yl.map(function (y) { return "<span>" + y + "</span>"; }).join("");
    function showStop(i, instant) {
      if (i === cur) return; var e = bySlug[STOPS[i]]; if (!e) return;
      stops.forEach(function (f, k) { f.classList.toggle("is-on", k === i); });
      if (cur >= 0) { var p = lines[STOPS[cur]]; if (p) { p.el.classList.remove("is-on"); p.el.classList.add("is-was"); if (!was[STOPS[cur]]) { var w = document.createElementNS(NS, "circle"); w.setAttribute("class", "v4l-was"); w.setAttribute("r", "3"); w.setAttribute("cx", p.x.toFixed(1)); w.setAttribute("cy", p.y.toFixed(1)); svg.insertBefore(w, ring); was[STOPS[cur]] = w; } } }
      var l = lines[e.s]; if (l) { l.el.classList.add("is-on"); l.el.classList.remove("is-was"); mk.setAttribute("cx", l.x.toFixed(1)); mk.setAttribute("cy", l.y.toFixed(1)); ring.setAttribute("cx", l.x.toFixed(1)); ring.setAttribute("cy", l.y.toFixed(1)); }
      var swap = function () {
        qn.textContent = e.n ? "Episode " + e.n : ""; qs.textContent = D.shelves[e.sh]; qd.textContent = e.d; qt.textContent = e.q; qw.innerHTML = "<b></b> <span></span>"; qw.querySelector("b").textContent = e.g; qw.querySelector("span").textContent = e.t + (e.m ? " · " + e.m + " min" : ""); qo.href = epUrl(e.s);
        yearB.textContent = e.d ? e.d.slice(-4) : ""; yi.textContent = i + 1; q.classList.remove("is-swap");
      };
      if (instant || calm || cur < 0) swap(); else { q.classList.add("is-swap"); setTimeout(swap, 260); }
      cur = i; fly.classList.toggle("is-flying", i > 0);
    }
    showStop(0, true);
    var raf = 0;
    function onScroll() {
      if (raf) return; raf = requestAnimationFrame(function () {
        raf = 0; var r = fly.getBoundingClientRect(), h = r.height - window.innerHeight; if (h <= 0) return;
        var p = clamp(-r.top / h, 0, 1), n = STOPS.length, i = Math.min(n - 1, Math.floor(p * n * 0.999));
        showStop(i);
      });
    }
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
    // a column answers a touch: the guest, the sentence, a link
    var hot = null, tipT = 0;
    function placeTip(l, e) {
      tip.hidden = false; var img = tip.querySelector("img"); img.src = still(e) || ""; img.style.visibility = e.i ? "" : "hidden"; tip.querySelector("b").textContent = e.g || e.t; tip.querySelector("i").textContent = e.q ? "“" + e.q + "”" : e.t; tip.querySelector("span").textContent = (e.d || "") + (e.m ? " · " + e.m + " min" : "") + " · tap to open";
      var rw = svg.getBoundingClientRect(), x = rw.left + l.x / 1000 * rw.width, y = rw.top + l.y / H * rw.height, rg = tip.parentNode.getBoundingClientRect(), pr = pin.getBoundingClientRect(), tw = tip.offsetWidth || 320, th = tip.offsetHeight || 90;
      var left = clamp(x - rg.left + 14, 8, rg.width - tw - 8), top = clamp(y - rg.top - th - 12, pr.top - rg.top + 8, rg.height - th - 8); tip.style.left = "0"; tip.style.top = "0"; tip.style.transform = "translate(" + left.toFixed(0) + "px," + top.toFixed(0) + "px)";
    }
    function hover(l, e) { if (hot && hot !== l) hot.el.classList.remove("is-hot"); hot = l; if (!l) { tip.hidden = true; return; } l.el.classList.add("is-hot"); placeTip(l, e); }
    svg.addEventListener("pointermove", function (ev) { var t = ev.target; if (t && t.tagName === "line") { var s = t.getAttribute("data-s"); hover(lines[s], bySlug[s]); } });
    svg.addEventListener("pointerleave", function () { clearTimeout(tipT); tipT = setTimeout(function () { hover(null); }, 200); });
    svg.addEventListener("click", function (ev) { var t = ev.target; if (t && t.tagName === "line") { var s = t.getAttribute("data-s"); if (hot && hot.el === t && !tip.hidden && !small) location.href = epUrl(s); else hover(lines[s], bySlug[s]); } });
    // a column takes the finger: wider than the stroke
    [].slice.call(svg.querySelectorAll("line")).forEach(function (l) { l.style.strokeWidth = small ? "6" : "4"; l.style.strokeOpacity = "1"; });
    // the shelves, guests and topics below also light the big ridge when the visitor comes back up
    fly._light = function (set) { Object.keys(lines).forEach(function (s) { lines[s].el.classList.toggle("is-dim", !!set && !set[s]); }); };
  }

  /* ---------- the finder and the rows ---------- */
  var find = document.getElementById("find"), rowsBox = document.getElementById("browse"); if (!find || !rowsBox) return;
  var rows = [].slice.call(rowsBox.querySelectorAll(".v4l-row")), more = rowsBox.querySelector(".v4l-more"), none = rowsBox.querySelector(".v4l-none"), filt = rowsBox.querySelector(".v4l-filter"), nEl = rowsBox.querySelector(".v4l-n");
  var mini = rowsBox.querySelector(".v4l-mini svg"), miniLines = drawRidge(mini, 80, 4), miniBox = rowsBox.querySelector(".v4l-mini");
  var input = find.querySelector("input"), sis = [].slice.call(find.querySelectorAll(".v4l-si")), gs = [].slice.call(find.querySelectorAll(".v4l-g")), ts = [].slice.call(find.querySelectorAll(".v4l-t"));
  var F = { sh: -1, g: "", t: "", q: "" }, PAGE = 24, shown = PAGE;
  function norm(s) { return (s || "").toLowerCase(); }
  function match(e) {
    if (F.sh >= 0 && e.sh !== F.sh) return false;
    if (F.g && e.g !== F.g) return false;
    if (F.t && e.k.indexOf(F.t) < 0) return false;
    if (F.q) { var q = norm(F.q); if (norm(e.t).indexOf(q) < 0 && norm(e.g).indexOf(q) < 0 && norm(e.k.join(" ")).indexOf(q) < 0 && norm(e.q).indexOf(q) < 0) return false; }
    return true;
  }
  function apply(scroll) {
    var on = 0, set = null, any = F.sh >= 0 || F.g || F.t || F.q;
    if (any) set = {};
    rows.forEach(function (r) { var e = bySlug[r.getAttribute("data-s")], ok = e && match(e); if (ok) { on++; if (set) set[e.s] = 1; } r.hidden = !ok || on > shown; });
    more.hidden = on <= shown; more.textContent = "Show " + Math.min(PAGE, on - shown) + " more of " + on; none.hidden = on > 0; nEl.textContent = on;
    var label = F.sh >= 0 ? D.shelves[F.sh] : F.g ? F.g : F.t ? F.t : F.q ? "“" + F.q + "”" : "";
    filt.hidden = !any; filt.innerHTML = any ? "" : ""; if (any) { filt.textContent = label + " "; var b = document.createElement("button"); b.type = "button"; b.textContent = "clear"; b.addEventListener("click", function () { clear(); }); filt.appendChild(b); }
    sis.forEach(function (b) { b.classList.toggle("is-on", +b.getAttribute("data-sh") === F.sh); }); gs.forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-g") === F.g); }); ts.forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-t") === F.t); });
    Object.keys(miniLines).forEach(function (s) { miniLines[s].el.classList.toggle("is-lit", !!set && !!set[s]); }); miniBox.classList.toggle("is-filtered", !!set);
    if (fly && fly._light) fly._light(set);
    if (scroll) rowsBox.scrollIntoView({ behavior: calm ? "auto" : "smooth", block: "start" });
  }
  function clear() { F = { sh: -1, g: "", t: "", q: "" }; input.value = ""; shown = PAGE; apply(false); }
  sis.forEach(function (b) { b.addEventListener("click", function () { var v = +b.getAttribute("data-sh"); F.sh = F.sh === v ? -1 : v; F.g = ""; F.t = ""; shown = PAGE; apply(true); }); });
  gs.forEach(function (b) { b.addEventListener("click", function () { var v = b.getAttribute("data-g"); F.g = F.g === v ? "" : v; F.sh = -1; F.t = ""; shown = PAGE; apply(true); }); });
  ts.forEach(function (b) { b.addEventListener("click", function () { var v = b.getAttribute("data-t"); F.t = F.t === v ? "" : v; F.sh = -1; F.g = ""; shown = PAGE; apply(true); }); });
  var typing = 0; input.addEventListener("input", function () { clearTimeout(typing); typing = setTimeout(function () { F.q = input.value.trim(); F.sh = -1; F.g = ""; F.t = ""; shown = PAGE; apply(false); }, 180); });
  more.addEventListener("click", function () { shown += PAGE; apply(false); });
  // the mini ridge: a column answers a touch with the row
  mini.addEventListener("click", function (ev) { var t = ev.target; if (t && t.tagName === "line") location.href = epUrl(t.getAttribute("data-s")); });
  [].slice.call(mini.querySelectorAll("line")).forEach(function (l) { l.style.cursor = "pointer"; var s = l.getAttribute("data-s"), e = bySlug[s]; var tt = document.createElementNS(NS, "title"); tt.textContent = (e.g ? e.g + " · " : "") + e.t; l.appendChild(tt); });
  apply(false);
})();
