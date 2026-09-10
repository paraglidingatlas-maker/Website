/* Sitemap network graph.
   Small force directed layout written from scratch, no external dependency.
   Opens as the nav bar; everything below stays folded until asked for.
   Opening a branch pushes everything else back so attention lands on what just
   appeared. The wheel scrolls the page as normal; zoom is on the buttons, or
   ctrl/cmd with the wheel, or a trackpad pinch. */
(function () {
  "use strict";

  var data = window.SITEMAP_GRAPH;
  var svg = document.getElementById("sm-svg");
  if (!data || !svg) return;

  var NS = "http://www.w3.org/2000/svg";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SIZE = { root: 17, section: 13, category: 10, series: 8.5, episode: 5 };

  var kids = {}, parents = {}, byId = {};
  data.links.forEach(function (l) {
    (kids[l.s] = kids[l.s] || []).push(l.t);
    (parents[l.t] = parents[l.t] || []).push(l.s);
  });
  data.nodes.forEach(function (n) {
    byId[n.id] = n;
    n.x = 0; n.y = 0; n.vx = 0; n.vy = 0;
    n.open = n.depth < 1;
    n.shown = n.depth <= 1;
  });

  var focus = "home";

  function recompute() {
    data.nodes.forEach(function (n) { n.shown = n.depth === 0; });
    (function walk(id) {
      var n = byId[id];
      if (!n || !n.open) return;
      (kids[id] || []).forEach(function (k) { byId[k].shown = true; walk(k); });
    })("home");
  }

  /* tier 0 = what just opened and its children, 1 = the path back to home,
     2 = everything else, pushed into the background */
  function tiers() {
    var t = {};
    data.nodes.forEach(function (n) { t[n.id] = 2; });
    var up = focus, guard = 0;
    while (up && guard++ < 20) { t[up] = 1; up = (parents[up] || [])[0]; }
    t[focus] = 0;
    (kids[focus] || []).forEach(function (k) { t[k] = 0; });
    return t;
  }

  function seed() {
    data.nodes.forEach(function (n) {
      if (n.x || n.y) return;
      var p = (parents[n.id] || [])[0], pn = p && byId[p];
      var a = Math.random() * Math.PI * 2, d = 78 + n.depth * 16;
      n.x = (pn ? pn.x : 0) + Math.cos(a) * d;
      n.y = (pn ? pn.y : 0) + Math.sin(a) * d;
    });
  }

  var W = 900, H = 640, view = { x: 0, y: 0, k: 1 };

  function tick(steps) {
    var live = data.nodes.filter(function (n) { return n.shown; });
    for (var s = 0; s < steps; s++) {
      for (var i = 0; i < live.length; i++) {
        for (var j = i + 1; j < live.length; j++) {
          var a = live[i], b = live[j];
          var dx = b.x - a.x, dy = b.y - a.y;
          var d = Math.sqrt(dx * dx + dy * dy) || 0.01;
          if (d > 280) continue;
          var f = 1600 / (d * d);
          a.vx -= dx / d * f; a.vy -= dy / d * f;
          b.vx += dx / d * f; b.vy += dy / d * f;
        }
      }
      data.links.forEach(function (l) {
        var a = byId[l.s], b = byId[l.t];
        if (!a.shown || !b.shown) return;
        var dx = b.x - a.x, dy = b.y - a.y;
        var d = Math.sqrt(dx * dx + dy * dy) || 0.01;
        var f = (d - (66 + (a.depth + b.depth) * 9)) * 0.035;
        a.vx += dx / d * f; a.vy += dy / d * f;
        b.vx -= dx / d * f; b.vy -= dy / d * f;
      });
      live.forEach(function (n) {
        n.vx -= n.x * 0.0032; n.vy -= n.y * 0.0032;
        if (n.id === "home") { n.x = 0; n.y = 0; n.vx = 0; n.vy = 0; return; }
        n.vx *= 0.86; n.vy *= 0.86;
        n.x += n.vx; n.y += n.vy;
      });
    }
  }

  function fit() {
    var live = data.nodes.filter(function (n) { return n.shown; });
    if (!live.length) return;
    var xs = live.map(function (n) { return n.x; }), ys = live.map(function (n) { return n.y; });
    var minx = Math.min.apply(null, xs), maxx = Math.max.apply(null, xs);
    var miny = Math.min.apply(null, ys), maxy = Math.max.apply(null, ys);
    var pad = 110;
    view.k = Math.min(W / (maxx - minx + pad * 2), H / (maxy - miny + pad * 2), 1.4);
    view.x = W / 2 - (minx + maxx) / 2 * view.k;
    view.y = H / 2 - (miny + maxy) / 2 * view.k;
  }

  /* ---------------- shapes: instrument rather than dot ---------------- */
  function poly(sides, r, rot) {
    var pts = [];
    for (var i = 0; i < sides; i++) {
      var a = rot + i * 2 * Math.PI / sides;
      pts.push((Math.cos(a) * r).toFixed(1) + "," + (Math.sin(a) * r).toFixed(1));
    }
    return pts.join(" ");
  }

  function shape(n, into) {
    var r = SIZE[n.kind], el;
    if (n.kind === "root") {
      var hit = document.createElementNS(NS, "circle");
      hit.setAttribute("r", r + 4);
      hit.setAttribute("class", "sm-hit");
      into.appendChild(hit);
      [[r, "sm-ring"], [r * 0.5, "sm-core"]].forEach(function (p) {
        var c = document.createElementNS(NS, "circle");
        c.setAttribute("r", p[0]);
        c.setAttribute("class", p[1]);
        into.appendChild(c);
      });
      [[-r - 6, 0, -r - 2, 0], [r + 2, 0, r + 6, 0],
       [0, -r - 6, 0, -r - 2], [0, r + 2, 0, r + 6]].forEach(function (t) {
        var l = document.createElementNS(NS, "line");
        l.setAttribute("x1", t[0]); l.setAttribute("y1", t[1]);
        l.setAttribute("x2", t[2]); l.setAttribute("y2", t[3]);
        l.setAttribute("class", "sm-cross");
        into.appendChild(l);
      });
      return;
    }
    if (n.kind === "section") {
      el = document.createElementNS(NS, "polygon");
      el.setAttribute("points", poly(6, r, Math.PI / 6));
    } else if (n.kind === "category") {
      el = document.createElementNS(NS, "polygon");
      el.setAttribute("points", poly(4, r, 0));
    } else if (n.kind === "series") {
      el = document.createElementNS(NS, "rect");
      el.setAttribute("x", -r); el.setAttribute("y", -r * 0.7);
      el.setAttribute("width", r * 2); el.setAttribute("height", r * 1.4);
    } else {
      el = document.createElementNS(NS, "rect");
      el.setAttribute("x", -r * 0.62); el.setAttribute("y", -r * 0.62);
      el.setAttribute("width", r * 1.24); el.setAttribute("height", r * 1.24);
      el.setAttribute("transform", "rotate(45)");
    }
    el.setAttribute("class", "sm-glyph");
    into.appendChild(el);
  }

  function draw() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var t = tiers();

    var defs = document.createElementNS(NS, "defs");
    defs.innerHTML =
      '<pattern id="smgrid" width="34" height="34" patternUnits="userSpaceOnUse">' +
      '<path d="M34 0H0V34" fill="none" stroke="rgba(180,180,180,0.05)" stroke-width="1"/>' +
      '</pattern>' +
      '<radialGradient id="smvig" cx="50%" cy="50%" r="72%">' +
      '<stop offset="52%" stop-color="rgba(16,17,22,0)"/>' +
      '<stop offset="100%" stop-color="rgba(16,17,22,0.9)"/></radialGradient>';
    svg.appendChild(defs);

    var bg = document.createElementNS(NS, "rect");
    bg.setAttribute("width", W); bg.setAttribute("height", H);
    bg.setAttribute("fill", "url(#smgrid)");
    svg.appendChild(bg);

    var g = document.createElementNS(NS, "g");
    g.setAttribute("transform",
      "translate(" + view.x + "," + view.y + ") scale(" + view.k + ")");
    svg.appendChild(g);

    data.links.forEach(function (l) {
      var a = byId[l.s], b = byId[l.t];
      if (!a.shown || !b.shown) return;
      var dx = b.x - a.x, dy = b.y - a.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
      var pad = SIZE[b.kind] + 5;
      var tier = Math.max(t[a.id], t[b.id]);
      var ln = document.createElementNS(NS, "line");
      ln.setAttribute("x1", a.x); ln.setAttribute("y1", a.y);
      ln.setAttribute("x2", b.x - dx / d * pad);
      ln.setAttribute("y2", b.y - dy / d * pad);
      ln.setAttribute("class", "sm-edge t" + tier);
      g.appendChild(ln);
      var tk = document.createElementNS(NS, "circle");
      tk.setAttribute("cx", a.x + dx * 0.64);
      tk.setAttribute("cy", a.y + dy * 0.64);
      tk.setAttribute("r", 1.5);
      tk.setAttribute("class", "sm-flow t" + tier);
      g.appendChild(tk);
    });

    data.nodes.forEach(function (n) {
      var has = (kids[n.id] || []).length;
      if (!n.shown || !has || n.open) return;
      var p = (parents[n.id] || [])[0], pn = p && byId[p];
      var base = pn ? Math.atan2(n.y - pn.y, n.x - pn.x) : -Math.PI / 2;
      var count = Math.min(has, 5), spread = Math.PI * 0.62;
      for (var i = 0; i < count; i++) {
        var a = base + (count === 1 ? 0 : (i / (count - 1) - 0.5) * spread);
        var r0 = SIZE[n.kind] + 4, len = 13 + Math.min(has, 12);
        var ln = document.createElementNS(NS, "line");
        ln.setAttribute("x1", n.x + Math.cos(a) * r0);
        ln.setAttribute("y1", n.y + Math.sin(a) * r0);
        ln.setAttribute("x2", n.x + Math.cos(a) * (r0 + len));
        ln.setAttribute("y2", n.y + Math.sin(a) * (r0 + len));
        ln.setAttribute("class", "sm-stub t" + t[n.id]);
        g.appendChild(ln);
      }
    });

    data.nodes.forEach(function (n) {
      if (!n.shown) return;
      var has = (kids[n.id] || []).length;
      var grp = document.createElementNS(NS, "g");
      grp.setAttribute("class", "sm-node sm-" + n.kind + " t" + t[n.id] +
        (has && n.open ? " sm-open" : "") + (n.id === focus ? " sm-focus" : ""));
      grp.setAttribute("transform", "translate(" + n.x + "," + n.y + ")");
      grp.setAttribute("tabindex", "0");
      grp.setAttribute("role", "button");
      grp.setAttribute("aria-label",
        n.label + (has ? ", " + has + " below" : ", opens the page"));
      shape(n, grp);

      if (n.kind !== "episode" || t[n.id] === 0) {
        var pad = SIZE[n.kind] + 7;
        var lead = document.createElementNS(NS, "line");
        lead.setAttribute("x1", pad - 5); lead.setAttribute("y1", 0);
        lead.setAttribute("x2", pad); lead.setAttribute("y2", 0);
        lead.setAttribute("class", "sm-lead");
        grp.appendChild(lead);
        var tx = document.createElementNS(NS, "text");
        tx.setAttribute("class", "sm-label");
        tx.setAttribute("x", pad + 4);
        tx.setAttribute("dy", "0.34em");
        tx.textContent = n.label.length > 32 ? n.label.slice(0, 31) + "\u2026" : n.label;
        grp.appendChild(tx);
      }

      grp.addEventListener("click", function (ev) { hit(n, ev); });
      grp.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); hit(n, ev); }
      });
      grp.addEventListener("mouseenter", function () { info(n); });
      g.appendChild(grp);
    });

    var vig = document.createElementNS(NS, "rect");
    vig.setAttribute("width", W); vig.setAttribute("height", H);
    vig.setAttribute("fill", "url(#smvig)");
    vig.setAttribute("pointer-events", "none");
    svg.appendChild(vig);
  }

  var panel = document.getElementById("sm-info");
  function info(n) {
    if (!panel) return;
    var has = (kids[n.id] || []).length;
    panel.innerHTML = "<strong>" + n.label + "</strong><span>" +
      (has ? has + " below, click to " + (n.open ? "fold away" : "open out")
           : "click to open the page") + "</span>";
  }

  function hit(n, ev) {
    var has = (kids[n.id] || []).length;
    if (has && !(ev && (ev.metaKey || ev.ctrlKey))) {
      n.open = !n.open;
      focus = n.open ? n.id : ((parents[n.id] || [])[0] || "home");
      recompute(); seed(); tick(reduce ? 300 : 230); fit(); draw(); info(n);
      return;
    }
    if (n.url) {
      if (/^https?:/.test(n.url)) window.open(n.url, "_blank", "noopener");
      else window.location.href = n.url;
    }
  }

  var drag = null;
  svg.addEventListener("pointerdown", function (e) {
    if (e.target.closest && e.target.closest(".sm-node")) return;
    drag = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y };
    svg.setPointerCapture(e.pointerId);
  });
  svg.addEventListener("pointermove", function (e) {
    if (!drag) return;
    view.x = drag.vx + (e.clientX - drag.x);
    view.y = drag.vy + (e.clientY - drag.y);
    draw();
  });
  ["pointerup", "pointercancel"].forEach(function (evt) {
    svg.addEventListener(evt, function () { drag = null; });
  });

  function zoom(mult) {
    view.k = Math.max(0.3, Math.min(2.6, view.k * mult));
    draw();
  }
  /* only zoom on a deliberate gesture. A plain wheel is left alone so the
     page scrolls the way it should. */
  svg.addEventListener("wheel", function (e) {
    if (!e.ctrlKey && !e.metaKey) return;
    e.preventDefault();
    zoom(e.deltaY < 0 ? 1.1 : 0.91);
  }, { passive: false });

  function bind(id, fn) {
    var el = document.getElementById(id);
    if (el) el.addEventListener("click", fn);
  }
  bind("sm-in", function () { zoom(1.18); });
  bind("sm-out", function () { zoom(0.85); });
  bind("sm-reset", function () {
    data.nodes.forEach(function (n) { n.open = n.depth < 1; });
    focus = "home";
    recompute(); seed(); tick(reduce ? 400 : 320); fit(); draw();
  });

  recompute(); seed(); tick(reduce ? 400 : 340); fit(); draw();
})();
