/* Sitemap: the site as a landscape you fly across.
   True ground plane projection, undulating terrain, a camera that travels.
   Drag to fly. Click a node to travel there and open what is under it.
   Nothing here navigates; the bar below offers the page as an explicit link. */
(function () {
  "use strict";

  var data = window.SITEMAP_GRAPH;
  var svg = document.getElementById("sm-svg");
  if (!data || !svg) return;

  var NS = "http://www.w3.org/2000/svg";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var W = 1180, H = 660;

  var kids = {}, parents = {}, byId = {};
  data.links.forEach(function (l) {
    (kids[l.s] = kids[l.s] || []).push(l.t);
    (parents[l.t] = parents[l.t] || []).push(l.s);
  });
  data.nodes.forEach(function (n, i) {
    byId[n.id] = n;
    n.open = n.depth < 1;
    n.hover = (i * 37 % 11) * 5;      /* a little vertical scatter */
  });
  var focus = "home";

  function shown(n) {
    var up = primaryRaw(n.id), g = 0;
    while (up && g++ < 14) {
      if (!byId[up].open) return false;
      up = primaryRaw(up);
    }
    return true;
  }
  function primaryRaw(id) {
    var n = byId[id];
    if (n && n.via) return n.via;
    return (parents[id] || [])[0] || null;
  }
  function tier(n) {
    if (n.id === focus) return 0;
    if ((kids[focus] || []).indexOf(n.id) !== -1) return 0;
    var up = focus, g = 0;
    while (up && g++ < 14) { if (up === n.id) return 1; up = primaryRaw(up); }
    return 2;
  }

  /* ---------------- glyphs: thin HUD chevrons, one per family ---------------- */
  /* Drawn pointing along +X, roughly 26 units long, stroked not filled. */
  var GLYPH = [
    "M-11 -8 L2 0 L-11 8 M-2 -8 L11 0 L-2 8",                       /* nested pair */
    "M-11 -7 L4 0 L-11 7 M-11 0 H-3",                                /* split tail */
    "M-12 -8 L-2 0 L-12 8 M-4 -6 L4 0 L-4 6 M3 -4 L9 0 L3 4",        /* three stacked */
    "M-10 -8 L3 0 L-10 8 M-12 -10 V-6 M-12 10 V6 M8 -3 V3",          /* bracketed */
    "M-12 -8 L10 0 L-12 8 L-6 0 Z",                                  /* outline dart */
    "M-11 -8 L3 0 L-11 8 M-13 -4 L-7 -4 M-13 4 L-7 4",               /* slashed */
    "M-10 -9 L4 0 L-10 9 M-10 -3 L-1 -3 M-10 3 L-1 3"                /* ribbed */
  ];
  /* every category, and everything under it, gets its own arrow */
  var CATORDER = [], glyphOf = {};
  data.nodes.forEach(function (n) {
    if (n.kind === "category" && CATORDER.indexOf(n.id) === -1) CATORDER.push(n.id);
  });
  function glyphIndex(n) {
    if (n.kind === "root") return 3;
    if (n.kind === "section") return 1;
    if (glyphOf[n.id] !== undefined) return glyphOf[n.id];
    var up = n.id, g = 0, found = null;
    while (up && g++ < 14) {
      if (byId[up].kind === "category") { found = up; break; }
      up = primaryRaw(up);
    }
    var idx = found ? 2 + (CATORDER.indexOf(found) % 5) : 0;
    glyphOf[n.id] = idx;
    return idx;
  }

  /* ---------------- ground layout ---------------- */
  var COLX = 340, ROWZ = 150;
  function layout() {
    var row = 0;
    (function place(id) {
      var n = byId[id];
      var ch = (kids[id] || []).filter(function (k) {
        return byId[k].open !== undefined && primaryRaw(k) === id && shown(byId[k]);
      });
      n.gx = n.depth * COLX;
      if (!ch.length || !n.open) { n.gz = row * ROWZ; row++; return; }
      var first = row;
      ch.forEach(place);
      if (row === first) { n.gz = row * ROWZ; row++; }
      else n.gz = (byId[ch[0]].gz + byId[ch[ch.length - 1]].gz) / 2;
    })("home");
  }

  function ter(x, z) {
    return Math.sin(x * 0.0015) * 30 + Math.sin(z * 0.0019 + 1.3) * 24 +
           Math.sin((x + z) * 0.00085) * 18 + Math.sin(x * 0.0043 + z * 0.0031) * 7;
  }

  var cam = { x: 0, z: 0 };
  var FOCAL = 760, EYE = 380, HOR = H * 0.215, NEAR = 330;

  function project(gx, gz, alt) {
    var rz = (gz - cam.z) + NEAR;
    if (rz < 70) rz = 70;
    var s = FOCAL / rz;
    return { x: W / 2 + (gx - cam.x) * s, y: HOR + (EYE - (alt || 0)) * s, s: s,
             fog: Math.max(0, Math.min(1, (s - 0.30) / 0.95)) };
  }
  function el(p, t, a) {
    var e = document.createElementNS(NS, t);
    for (var k in a) e.setAttribute(k, a[k]);
    p.appendChild(e);
    return e;
  }
  function trunc(t, n) { return t.length > n ? t.slice(0, n - 1) + "\u2026" : t; }

  var DUST = [], STARS = [], i;
  for (i = 0; i < 90; i++) DUST.push({ gx: (Math.random() - 0.35) * 3600,
    gz: Math.random() * 2200 - 300, alt: Math.random() * 420 + 30, r: Math.random() * 1.2 + 0.5 });
  for (i = 0; i < 110; i++) STARS.push({ x: Math.random() * 1600 - 200,
    y: Math.random() * HOR * 0.95, r: Math.random() * 0.85 + 0.25 });

  function draw() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var defs = el(svg, "defs", {});
    defs.innerHTML =
      '<linearGradient id="sm-sky" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="#07080b"/><stop offset="62%" stop-color="#0d1017"/>' +
        '<stop offset="100%" stop-color="#161b26"/></linearGradient>' +
      '<linearGradient id="sm-hg" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="rgba(120,150,195,0)"/>' +
        '<stop offset="72%" stop-color="rgba(126,156,200,0.14)"/>' +
        '<stop offset="100%" stop-color="rgba(150,180,225,0.28)"/></linearGradient>' +
      '<linearGradient id="sm-fog" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="rgba(14,17,24,0.96)"/>' +
        '<stop offset="60%" stop-color="rgba(14,17,24,0.6)"/>' +
        '<stop offset="100%" stop-color="rgba(14,17,24,0)"/></linearGradient>' +
      '<radialGradient id="sm-vig" cx="50%" cy="52%" r="74%">' +
        '<stop offset="58%" stop-color="rgba(6,7,10,0)"/>' +
        '<stop offset="100%" stop-color="rgba(6,7,10,0.86)"/></radialGradient>' +
      '<radialGradient id="sm-hot"><stop offset="0" stop-color="rgba(255,196,120,0.4)"/>' +
        '<stop offset="55%" stop-color="rgba(255,150,50,0.1)"/>' +
        '<stop offset="100%" stop-color="rgba(255,150,50,0)"/></radialGradient>' +
      '<filter id="sm-far" x="-40%" y="-40%" width="180%" height="180%">' +
        '<feGaussianBlur stdDeviation="1.3"/></filter>';

    el(svg, "rect", { width: W, height: H, fill: "#0a0c11" });
    el(svg, "rect", { width: W, height: HOR + 3, fill: "url(#sm-sky)" });

    var sky = el(svg, "g", {});
    STARS.forEach(function (st) {
      var x = ((st.x - cam.x * 0.012) % 1600 + 1600) % 1600 - 200;
      el(sky, "circle", { cx: x, cy: st.y, r: st.r,
        fill: "rgba(198,214,240,0.55)", opacity: 0.15 + 0.38 * (st.y / HOR) });
    });
    el(svg, "rect", { width: W, height: HOR + 3, fill: "url(#sm-hg)" });

    var rp = "M-60 " + (HOR + 3), x, t, h;
    for (x = -60; x <= W + 60; x += 26) {
      t = (x + cam.x * 0.045) * 0.0042;
      h = Math.sin(t) * 15 + Math.sin(t * 2.3) * 8 + Math.sin(t * 0.66) * 20;
      rp += " L" + x + " " + (HOR - 16 - h);
    }
    el(svg, "path", { d: rp + " L" + (W + 60) + " " + (HOR + 3) + " Z",
      fill: "#0b0e15", stroke: "rgba(150,175,215,0.18)", "stroke-width": 1 });

    var grid = el(svg, "g", {}), gz, gx, pts, q;
    var z0 = Math.floor((cam.z - NEAR) / 150) * 150;
    for (gz = z0; gz < cam.z + 2900; gz += 150) {
      pts = [];
      for (gx = cam.x - 2700; gx <= cam.x + 2700; gx += 180) {
        q = project(gx, gz, ter(gx, gz));
        if (q.s > 0.03) pts.push(q.x.toFixed(1) + "," + q.y.toFixed(1));
      }
      if (pts.length < 2) continue;
      q = project(0, gz, 0);
      el(grid, "polyline", { points: pts.join(" "), fill: "none",
        stroke: "rgba(158,182,220,0.85)", "stroke-width": Math.max(0.4, q.s * 0.85),
        opacity: 0.07 + q.fog * 0.25 });
    }
    var x0 = Math.floor((cam.x - 2700) / 180) * 180;
    for (gx = x0; gx < cam.x + 2700; gx += 180) {
      pts = [];
      for (gz = Math.max(z0, cam.z - NEAR + 90); gz < cam.z + 2900; gz += 150) {
        q = project(gx, gz, ter(gx, gz));
        if (q.s > 0.03) pts.push(q.x.toFixed(1) + "," + q.y.toFixed(1));
      }
      if (pts.length > 1)
        el(grid, "polyline", { points: pts.join(" "), fill: "none",
          stroke: "rgba(158,182,220,0.7)", "stroke-width": 0.7, opacity: 0.09 });
    }

    var dust = el(svg, "g", {});
    DUST.forEach(function (m) {
      var p = project(m.gx, m.gz, m.alt);
      if (p.s < 0.07 || p.x < -50 || p.x > W + 50) return;
      el(dust, "circle", { cx: p.x, cy: p.y, r: m.r * p.s * 1.7,
        fill: "rgba(206,220,244,0.6)", opacity: 0.04 + p.fog * 0.14 });
    });

    var vis = data.nodes.filter(function (n) { return n.gx !== undefined && shown(n); });
    vis.forEach(function (n) {
      n.alt = ter(n.gx, n.gz) + 118 + n.hover;
      n.pr = project(n.gx, n.gz, n.alt);
      n.gr = project(n.gx, n.gz, ter(n.gx, n.gz));
    });
    var order = vis.slice().sort(function (a, b) { return a.pr.s - b.pr.s; });

    var farG = el(svg, "g", { filter: "url(#sm-far)" }), nearG = el(svg, "g", {});
    function bucket(n) { return n.pr.s < 0.30 ? farG : nearG; }

    order.forEach(function (n) {
      var p = byId[primaryRaw(n.id)];
      if (!p || !p.pr) return;
      var tr = Math.max(tier(n), tier(p));
      el(bucket(n), "line", { x1: p.pr.x, y1: p.pr.y, x2: n.pr.x, y2: n.pr.y,
        stroke: tr === 0 ? "rgba(255,206,150,1)" : "rgba(226,234,246,1)",
        "stroke-width": Math.max(0.5, n.pr.s * 1.1),
        "stroke-dasharray": (4 * n.pr.s).toFixed(1) + " " + (6 * n.pr.s).toFixed(1),
        opacity: (tr === 0 ? 0.46 : tr === 1 ? 0.22 : 0.09) * (0.3 + n.pr.fog * 0.7) });
    });

    order.forEach(function (n) {
      var tr = tier(n), q = n.pr;
      if (q.s < 0.045) return;
      var op = (tr === 0 ? 1 : tr === 1 ? 0.5 : 0.2) * (0.28 + q.fog * 0.72);
      var g = el(bucket(n), "g", { opacity: op, style: "cursor:pointer",
        tabindex: "0", role: "button" });
      g.setAttribute("aria-label", n.label);

      el(g, "line", { x1: q.x, y1: q.y, x2: n.gr.x, y2: n.gr.y,
        stroke: "rgba(200,216,242,0.55)", "stroke-width": Math.max(0.4, q.s * 0.5),
        opacity: 0.24 });
      el(g, "ellipse", { cx: n.gr.x, cy: n.gr.y, rx: 8 * q.s, ry: 2.6 * q.s,
        fill: "rgba(170,190,220,0.22)" });

      var p = byId[primaryRaw(n.id)];
      var ang = (p && p.pr) ? Math.atan2(q.y - p.pr.y, q.x - p.pr.x) * 180 / Math.PI : 0;
      var sc = q.s * (n.kind === "root" ? 1.9 : n.depth < 3 ? 1.35 : 0.95);

      if (tr === 0) el(g, "circle", { cx: q.x, cy: q.y,
        r: 42 * Math.max(q.s, 0.35), fill: "url(#sm-hot)" });

      /* thin stroked chevron rather than a solid delta */
      el(g, "path", { d: GLYPH[glyphIndex(n)],
        transform: "translate(" + q.x + "," + q.y + ") rotate(" + ang + ") scale(" + sc + ")",
        fill: "none",
        stroke: tr === 0 ? "rgba(232,238,248,0.92)" : "rgba(198,210,230,0.6)",
        "stroke-width": Math.max(0.9, 1.5 / Math.max(sc, 0.25)),
        "stroke-linecap": "round", "stroke-linejoin": "round" });

      if (q.s > 0.2 && (tr < 2 || n.depth < 3)) {
        var fs = Math.max(7.5, Math.min(13, 11 * q.s));
        var tx = el(g, "text", { x: q.x + 20 * q.s, y: q.y + fs * 0.35,
          fill: tr === 0 ? "rgba(255,205,145,0.95)" : "rgba(222,230,244,0.7)",
          "font-family": "var(--mono, monospace)", "font-size": fs,
          "letter-spacing": "0.08em" });
        tx.textContent = trunc(n.label.toUpperCase(), n.depth > 2 ? 20 : 22);
        if ((kids[n.id] || []).length && !n.open) {
          var pl = el(g, "text", { x: q.x + 20 * q.s, y: q.y + fs * 1.6,
            fill: "rgba(222,230,244,0.34)", "font-family": "var(--mono, monospace)",
            "font-size": fs * 0.78, "letter-spacing": "0.12em" });
          pl.textContent = "+ " + kids[n.id].length;
        }
      }
      g.addEventListener("click", function (e) { e.stopPropagation(); go(n); });
      g.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(n); }
      });
    });

    el(svg, "rect", { x: 0, y: HOR - 46, width: W, height: 205,
      fill: "url(#sm-fog)", "pointer-events": "none" });
    el(svg, "rect", { width: W, height: H, fill: "url(#sm-vig)", "pointer-events": "none" });
  }

  var anim = null;
  function fly(tx, tz, ms) {
    if (anim) cancelAnimationFrame(anim);
    var x0 = cam.x, z0 = cam.z, t0 = performance.now();
    if (reduce) { cam.x = tx; cam.z = tz; draw(); return; }
    (function step(now) {
      var q = Math.min(1, (now - t0) / ms);
      var e = q < 0.5 ? 4 * q * q * q : 1 - Math.pow(-2 * q + 2, 3) / 2;
      cam.x = x0 + (tx - x0) * e;
      cam.z = z0 + (tz - z0) * e;
      draw();
      anim = q < 1 ? requestAnimationFrame(step) : null;
    })(t0);
  }

  var panel = document.getElementById("sm-info");
  var WHAT = { root: "the front page", section: "a main section",
    category: "a group of series", series: "a series", episode: "an episode" };
  function info(n) {
    if (!panel) return;
    var has = (kids[n.id] || []).length;
    var where = (parents[n.id] || []).map(function (p) { return byId[p].label; }).join(" and ");
    var line = WHAT[n.kind] || "";
    if (where) line += ", under " + where;
    if (has) line += ". " + has + (n.open ? " ahead, click again to fold away" : " ahead, click to open");
    var link = n.url ? ' <a class="sm-go" href="' + n.url + '"' +
      (/^https?:/.test(n.url) ? ' target="_blank" rel="noopener"' : '') + '>Open this page</a>' : "";
    panel.innerHTML = "<strong>" + n.label + "</strong><span>" + line + "</span>" + link;
  }

  function go(n) {
    var has = (kids[n.id] || []).length;
    if (has) {
      n.open = !n.open;
      if (n.open) (kids[n.id] || []).forEach(function (k) { byId[k].via = n.id; });
      focus = n.open ? n.id : (n.via || primaryRaw(n.id) || "home");
    } else {
      focus = n.id;
    }
    layout();
    var f = byId[focus];
    fly(f.gx + COLX * 0.4, f.gz - 60, 950);
    info(n);
  }

  var drag = null;
  svg.addEventListener("pointerdown", function (e) {
    drag = { x: e.clientX, y: e.clientY, cx: cam.x, cz: cam.z };
    svg.setPointerCapture(e.pointerId);
  });
  svg.addEventListener("pointermove", function (e) {
    if (!drag) return;
    if (anim) { cancelAnimationFrame(anim); anim = null; }
    var r = svg.getBoundingClientRect(), k = W / r.width;
    cam.x = drag.cx - (e.clientX - drag.x) * k * 1.6;
    cam.z = drag.cz + (e.clientY - drag.y) * k * 2.6;
    draw();
  });
  ["pointerup", "pointercancel"].forEach(function (t) {
    svg.addEventListener(t, function () { drag = null; });
  });

  function bind(id, fn) { var e = document.getElementById(id); if (e) e.addEventListener("click", fn); }
  bind("sm-in", function () { EYE = Math.max(240, EYE - 45); draw(); });
  bind("sm-out", function () { EYE = Math.min(560, EYE + 45); draw(); });
  bind("sm-reset", function () {
    data.nodes.forEach(function (n) { n.open = n.depth < 1; n.via = null; });
    focus = "home"; EYE = 380; layout();
    fly(byId.home.gx + COLX * 0.4, byId.home.gz - 60, 1000);
    info(byId.home);
  });

  layout();
  cam.x = byId.home.gx + COLX * 0.4;
  cam.z = byId.home.gz - 60;
  draw();
  info(byId.home);
})();
