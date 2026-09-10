/* Sitemap network graph.
   A small force directed layout written from scratch so the page carries no
   external dependency. Nodes start collapsed below the section level; clicking a
   node with children expands it, clicking a leaf opens the page. */
(function () {
  "use strict";

  var data = window.SITEMAP_GRAPH;
  var svg = document.getElementById("sm-svg");
  if (!data || !svg) return;

  var NS = "http://www.w3.org/2000/svg";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var R = { root: 15, section: 11, category: 8.5, series: 7, episode: 4.5 };
  var kids = {}, parents = {};
  data.links.forEach(function (l) {
    (kids[l.s] = kids[l.s] || []).push(l.t);
    (parents[l.t] = parents[l.t] || []).push(l.s);
  });

  var byId = {};
  data.nodes.forEach(function (n) {
    byId[n.id] = n;
    n.x = 0; n.y = 0; n.vx = 0; n.vy = 0;
    n.open = n.depth < 2;          // home, sections and categories visible at first
    n.shown = n.depth <= 2;
  });

  function recompute() {
    data.nodes.forEach(function (n) { n.shown = n.depth === 0; });
    (function walk(id) {
      var n = byId[id];
      if (!n || !n.open) return;
      (kids[id] || []).forEach(function (k) {
        byId[k].shown = true;
        walk(k);
      });
    })("home");
  }

  /* place new nodes near their parent so the layout does not explode */
  function seed() {
    data.nodes.forEach(function (n) {
      if (n.x || n.y) return;
      var p = (parents[n.id] || [])[0];
      var pn = p && byId[p];
      var a = Math.random() * Math.PI * 2;
      var d = 70 + n.depth * 18;
      n.x = (pn ? pn.x : 0) + Math.cos(a) * d;
      n.y = (pn ? pn.y : 0) + Math.sin(a) * d;
    });
  }

  var W = 900, H = 620, view = { x: 0, y: 0, k: 1 };

  function tick(steps) {
    var live = data.nodes.filter(function (n) { return n.shown; });
    var i, j, a, b, dx, dy, d, f;
    for (var s = 0; s < steps; s++) {
      /* repulsion */
      for (i = 0; i < live.length; i++) {
        for (j = i + 1; j < live.length; j++) {
          a = live[i]; b = live[j];
          dx = b.x - a.x; dy = b.y - a.y;
          d = Math.sqrt(dx * dx + dy * dy) || 0.01;
          if (d > 260) continue;
          f = 1400 / (d * d);
          dx = dx / d * f; dy = dy / d * f;
          a.vx -= dx; a.vy -= dy; b.vx += dx; b.vy += dy;
        }
      }
      /* springs */
      data.links.forEach(function (l) {
        a = byId[l.s]; b = byId[l.t];
        if (!a.shown || !b.shown) return;
        dx = b.x - a.x; dy = b.y - a.y;
        d = Math.sqrt(dx * dx + dy * dy) || 0.01;
        var rest = 58 + (a.depth + b.depth) * 9;
        f = (d - rest) * 0.035;
        dx = dx / d * f; dy = dy / d * f;
        a.vx += dx; a.vy += dy; b.vx -= dx; b.vy -= dy;
      });
      /* gentle pull to centre, and pin the root */
      live.forEach(function (n) {
        n.vx -= n.x * 0.0032;
        n.vy -= n.y * 0.0032;
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
    var pad = 70;
    var k = Math.min(W / (maxx - minx + pad * 2), H / (maxy - miny + pad * 2), 1.5);
    view.k = k;
    view.x = W / 2 - (minx + maxx) / 2 * k;
    view.y = H / 2 - (miny + maxy) / 2 * k;
  }

  function draw() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var defs = document.createElementNS(NS, "defs");
    defs.innerHTML =
      '<marker id="arw" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">' +
      '<path d="M0 0 L8 4 L0 8 z" fill="rgba(255,117,23,0.5)"/></marker>';
    svg.appendChild(defs);

    var g = document.createElementNS(NS, "g");
    g.setAttribute("transform", "translate(" + view.x + "," + view.y + ") scale(" + view.k + ")");
    svg.appendChild(g);

    data.links.forEach(function (l) {
      var a = byId[l.s], b = byId[l.t];
      if (!a.shown || !b.shown) return;
      var dx = b.x - a.x, dy = b.y - a.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
      var r = R[b.kind] + 4;
      var ln = document.createElementNS(NS, "line");
      ln.setAttribute("x1", a.x); ln.setAttribute("y1", a.y);
      ln.setAttribute("x2", b.x - dx / d * r); ln.setAttribute("y2", b.y - dy / d * r);
      ln.setAttribute("class", "sm-edge sm-edge-" + b.kind);
      ln.setAttribute("marker-end", "url(#arw)");
      g.appendChild(ln);
    });

    data.nodes.forEach(function (n) {
      if (!n.shown) return;
      var has = (kids[n.id] || []).length;
      var grp = document.createElementNS(NS, "g");
      grp.setAttribute("class", "sm-node sm-" + n.kind + (has && !n.open ? " sm-closed" : ""));
      grp.setAttribute("transform", "translate(" + n.x + "," + n.y + ")");
      grp.setAttribute("tabindex", "0");
      grp.setAttribute("role", "button");
      grp.setAttribute("aria-label", n.label + (has ? ", " + has + " below" : ""));

      var c = document.createElementNS(NS, "circle");
      c.setAttribute("r", R[n.kind]);
      grp.appendChild(c);

      if (has && !n.open) {
        var plus = document.createElementNS(NS, "text");
        plus.setAttribute("class", "sm-plus");
        plus.setAttribute("dy", "0.35em");
        plus.textContent = "+";
        grp.appendChild(plus);
      }

      if (n.kind !== "episode" || n.open) {
        var t = document.createElementNS(NS, "text");
        t.setAttribute("class", "sm-label");
        t.setAttribute("x", R[n.kind] + 6);
        t.setAttribute("dy", "0.34em");
        t.textContent = n.label.length > 34 ? n.label.slice(0, 33) + "\u2026" : n.label;
        grp.appendChild(t);
      }

      grp.addEventListener("click", function (ev) { hit(n, ev); });
      grp.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); hit(n, ev); }
      });
      grp.addEventListener("mouseenter", function () { info(n); });
      g.appendChild(grp);
    });
  }

  var panel = document.getElementById("sm-info");
  function info(n) {
    if (!panel) return;
    var has = (kids[n.id] || []).length;
    panel.innerHTML = '<strong>' + n.label + '</strong>' +
      (has ? '<span>' + has + ' below. Click to ' + (n.open ? 'collapse' : 'expand') + '.</span>'
           : '<span>Click to open the page.</span>');
  }

  function hit(n, ev) {
    var has = (kids[n.id] || []).length;
    if (has && !(ev && (ev.metaKey || ev.ctrlKey))) {
      n.open = !n.open;
      recompute();
      seed();
      tick(reduce ? 300 : 220);
      fit();
      draw();
      info(n);
      return;
    }
    if (n.url) {
      if (/^https?:/.test(n.url)) window.open(n.url, "_blank", "noopener");
      else window.location.href = n.url;
    }
  }

  /* pan and zoom */
  var drag = null;
  svg.addEventListener("pointerdown", function (e) {
    if (e.target.closest(".sm-node")) return;
    drag = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y };
    svg.setPointerCapture(e.pointerId);
  });
  svg.addEventListener("pointermove", function (e) {
    if (!drag) return;
    view.x = drag.vx + (e.clientX - drag.x);
    view.y = drag.vy + (e.clientY - drag.y);
    draw();
  });
  ["pointerup", "pointercancel"].forEach(function (t) {
    svg.addEventListener(t, function () { drag = null; });
  });
  svg.addEventListener("wheel", function (e) {
    e.preventDefault();
    var k = view.k * (e.deltaY < 0 ? 1.12 : 0.89);
    view.k = Math.max(0.25, Math.min(2.5, k));
    draw();
  }, { passive: false });

  var expandAll = document.getElementById("sm-expand");
  if (expandAll) expandAll.addEventListener("click", function () {
    var all = data.nodes.every(function (n) { return !(kids[n.id] || []).length || n.open; });
    data.nodes.forEach(function (n) { n.open = all ? n.depth < 2 : true; });
    expandAll.textContent = all ? "Expand everything" : "Collapse back down";
    recompute(); seed(); tick(reduce ? 500 : 400); fit(); draw();
  });

  recompute();
  seed();
  tick(reduce ? 400 : 320);
  fit();
  draw();
})();
