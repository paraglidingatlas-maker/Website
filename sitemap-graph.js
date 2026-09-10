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

  /* small helper the marker drawing relies on */
  function el(parent, tag, attrs) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    parent.appendChild(e);
    return e;
  }

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

  var W = 900, H = 640, view = { x: 0, y: 0, k: 1 };
  var COLW = 268, ROWH = 48;

  /* Primary parent, so the two-parent series still form a clean tree.
     The second edge is drawn as a cross link on top of it. */
  function primary(id) {
    var n = byId[id];
    if (n && n.via && byId[n.via] && byId[n.via].shown && byId[n.via].open) return n.via;
    var ps = parents[id] || [];
    for (var i = 0; i < ps.length; i++) if (byId[ps[i]].shown) return ps[i];
    return ps[0];
  }

  /* Tidy tree: column by depth, leaves take the next free row, parents centre
     on their children. Anything already open therefore sits to the LEFT of
     whatever you just opened, and the new branch extends to the right. */
  function layout() {
    var row = 0;
    (function place(id) {
      var n = byId[id];
      var ch = (kids[id] || []).filter(function (k) {
        return byId[k].shown && primary(k) === id;
      });
      n.tx = n.depth * COLW;
      if (!ch.length || !n.open) {
        n.ty = row * ROWH; row += 1; return;
      }
      var first = row;
      ch.forEach(place);
      if (row === first) { n.ty = row * ROWH; row += 1; }
      else n.ty = (byId[ch[0]].ty + byId[ch[ch.length - 1]].ty) / 2;
    })("home");

  }

  /* The canvas is wider than the frame on purpose. Rather than rescaling to fit
     everything, the camera travels: it keeps whatever you just opened a third of
     the way in from the left, so the columns you came through stay behind you
     and the new branch has clear space ahead. Zoom never changes by itself,
     which is what stops the whole thing lurching. */
  function camera() {
    var f = byId[focus] || byId.home;
    if (f.tx === undefined) return;
    view.x = W * 0.33 - f.tx * view.k;
    view.y = H * 0.5 - f.ty * view.k;
  }

  var anim = null;
  function settle(instant) {
    if (anim) { cancelAnimationFrame(anim); anim = null; }
    /* new arrivals slide out from their parent rather than in from nowhere */
    data.nodes.forEach(function (n) {
      if (n.tx === undefined || n.x || n.y || n.id === "home") return;
      var p = byId[primary(n.id)];
      if (p) { n.x = p.x; n.y = p.y; }
    });
    if (instant || reduce) {
      data.nodes.forEach(function (n) {
        if (n.tx !== undefined) { n.x = n.tx; n.y = n.ty; }
      });
      camera(); draw(); return;
    }
    var from = {};
    data.nodes.forEach(function (n) { from[n.id] = { x: n.x, y: n.y }; });
    var v0 = { x: view.x, y: view.y };
    camera();
    var v1 = { x: view.x, y: view.y };
    var t0 = performance.now(), DUR = 620;
    (function step(now) {
      var q = Math.min(1, (now - t0) / DUR);
      /* gentle ease in and out, no overshoot, nothing snappy */
      var e = q < 0.5 ? 4 * q * q * q : 1 - Math.pow(-2 * q + 2, 3) / 2;
      data.nodes.forEach(function (n) {
        if (n.tx === undefined) return;
        n.x = from[n.id].x + (n.tx - from[n.id].x) * e;
        n.y = from[n.id].y + (n.ty - from[n.id].y) * e;
      });
      view.x = v0.x + (v1.x - v0.x) * e;
      view.y = v0.y + (v1.y - v0.y) * e;
      draw();
      anim = q < 1 ? requestAnimationFrame(step) : null;
    })(t0);
  }

  /* ---------------- shapes: instrument rather than dot ---------------- */
  /* Marker pack, chosen from the blade studies:
       root and section  -> Warden, its two lightest treatments
       category, series,
       episode           -> Interceptor, its three fullest treatments
     Detail level is fixed per tier; only the radius changes with depth. */
  function warden(g, r, light) {
    var h = [], i, a;
    for (i = 0; i < 6; i++) {
      a = Math.PI / 6 + i * Math.PI / 3;
      h.push([Math.cos(a) * r * 1.25, Math.sin(a) * r * 1.25]);
    }
    for (i = 0; i < 6; i++) {
      if (light && i % 2) continue;            /* the lighter one drops alternate walls */
      var A = h[i], B = h[(i + 1) % 6];
      el(g, "path", { d: "M" + (A[0] + (B[0] - A[0]) * 0.14).toFixed(1) + " " +
        (A[1] + (B[1] - A[1]) * 0.14).toFixed(1) + " L" +
        (A[0] + (B[0] - A[0]) * 0.86).toFixed(1) + " " +
        (A[1] + (B[1] - A[1]) * 0.86).toFixed(1),
        "class": "sm-glyph", fill: "none" });
    }
    el(g, "path", { d: "M" + (r * 0.72) + " 0 L" + (-r * 0.5) + " " + (-r * 0.55) +
      " L" + (-r * 0.24) + " 0 L" + (-r * 0.5) + " " + (r * 0.55) + " Z",
      "class": "sm-glyph", fill: light ? "none" : "#171921" });
  }

  function interceptor(g, r, level) {
    el(g, "path", { d: "M" + (r * 1.15) + " 0 L" + (-r * 0.72) + " " + (-r * 0.95) +
      " L" + (-r * 0.34) + " 0 L" + (-r * 0.72) + " " + (r * 0.95) + " Z",
      "class": "sm-glyph", fill: "#171921" });
    el(g, "line", { x1: -r * 0.34, y1: 0, x2: r * 0.7, y2: 0,
      stroke: "#101116", "stroke-width": 1.5 });
    if (level < 2) {
      el(g, "path", { d: "M" + (-r * 0.6) + " " + (-r * 0.62) + " L" + (-r * 1.12) + " " + (-r * 0.9),
        "class": "sm-glyph", fill: "none" });
      el(g, "path", { d: "M" + (-r * 0.6) + " " + (r * 0.62) + " L" + (-r * 1.12) + " " + (r * 0.9),
        "class": "sm-glyph", fill: "none" });
    }
    if (level < 1) el(g, "circle", { cx: r * 0.6, cy: 0, r: r * 0.13,
      fill: "rgba(246,244,244,0.85)" });
  }

  function shape(n, into) {
    var r = SIZE[n.kind];
    el(into, "circle", { r: r + 6, "class": "sm-hit", fill: "transparent" });
    if (n.kind === "root")          warden(into, r, false);
    else if (n.kind === "section")  warden(into, r, true);
    else if (n.kind === "category") interceptor(into, r, 0);
    else if (n.kind === "series")   interceptor(into, r, 1);
    else                            interceptor(into, r, 2);
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
      var base = 0;   /* the tree grows rightward, so hints point right */
      var count = Math.min(has, 5), spread = Math.PI * 0.5;
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
        n.label + (has ? ", " + has + " below" : ""));
      shape(n, grp);

      if (n.kind !== "episode" || t[n.id] === 0) {
        var pad = SIZE[n.kind] * 1.35 + 8;
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

      grp.addEventListener("click", function () { hit(n); });
      grp.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); hit(n); }
      });
      
      g.appendChild(grp);
    });

    var vig = document.createElementNS(NS, "rect");
    vig.setAttribute("width", W); vig.setAttribute("height", H);
    vig.setAttribute("fill", "url(#smvig)");
    vig.setAttribute("pointer-events", "none");
    svg.appendChild(vig);
  }

  var panel = document.getElementById("sm-info");
  var WHAT = {
    root: "the front page", section: "a main section",
    category: "a group of series", series: "a series",
    episode: "an episode"
  };
  function info(n) {
    if (!panel) return;
    var has = (kids[n.id] || []).length;
    var where = (parents[n.id] || []).map(function (p) { return byId[p].label; }).join(" and ");
    var line = WHAT[n.kind] || "";
    if (where) line += ", under " + where;
    if (has) line += ". " + has + (n.open ? " below, click to fold away" : " below, click to open out");
    var link = n.url
      ? ' <a class="sm-go" href="' + n.url + '"' +
        (/^https?:/.test(n.url) ? ' target="_blank" rel="noopener"' : '') + '>Open this page</a>'
      : "";
    panel.innerHTML = "<strong>" + n.label + "</strong><span>" + line + "</span>" + link;
  }

  function hit(n) {
    var has = (kids[n.id] || []).length;
    if (has) {
      n.open = !n.open;
      /* Opening carries you forward to the new branch. Folding away pulls back
         to the parent, so you land where you came from with this node and its
         siblings in view rather than sitting on a node with nothing under it. */
      if (n.open) {
        /* remember the way in, so folding away retraces the path you took
           rather than the first parent in the data */
        (kids[n.id] || []).forEach(function (k) { byId[k].via = n.id; });
        focus = n.id;
      } else {
        focus = n.via || (parents[n.id] || [])[0] || "home";
      }
      recompute(); layout(); settle();
    } else {
      focus = n.id;
      settle();          /* no children: just travel to it */
    }
    info(n);
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
    var f = byId[focus] || byId.home;
    var before = view.k;
    view.k = Math.max(0.45, Math.min(2.2, view.k * mult));
    if (f.tx !== undefined) {          /* zoom about the node you are on */
      view.x = W * 0.33 - f.tx * view.k;
      view.y = H * 0.5 - f.ty * view.k;
    } else {
      view.x = W / 2 - (W / 2 - view.x) * (view.k / before);
      view.y = H / 2 - (H / 2 - view.y) * (view.k / before);
    }
    draw();
  }
  /* Wheel zooms while the pointer is over the map, the way the globe on the
     home page does. The difference: once you are fully zoomed out and keep
     scrolling out, the event is left alone so the page scrolls on past instead
     of trapping you inside the graph. Same at full zoom in. */
  var MINK = 0.45, MAXK = 2.2;
  svg.addEventListener("wheel", function (e) {
    var out = e.deltaY > 0;
    if ((out && view.k <= MINK + 0.001) || (!out && view.k >= MAXK - 0.001)) return;
    e.preventDefault();
    var before = view.k;
    view.k = Math.max(MINK, Math.min(MAXK, view.k * (out ? 0.94 : 1.064)));
    /* keep the point under the cursor roughly still */
    var r = svg.getBoundingClientRect();
    var cx = (e.clientX - r.left) * (W / r.width);
    var cy = (e.clientY - r.top) * (H / r.height);
    view.x = cx - (cx - view.x) * (view.k / before);
    view.y = cy - (cy - view.y) * (view.k / before);
    draw();
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
    recompute(); layout(); view.k = 1; settle();
  });

  recompute(); layout(); settle(true);
})();
