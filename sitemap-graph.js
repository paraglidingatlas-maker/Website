/* Sitemap: a top to bottom flow.
   Depth runs down the page and indents to the right, so every label gets the
   full width and nothing is ever shortened. No dragging, no zooming, no camera.
   Clicking opens or folds a branch; it never navigates. */
(function () {
  "use strict";

  var data = window.SITEMAP_GRAPH;
  var host = document.getElementById("sm-flow");
  if (!data || !host) return;

  var kids = {}, parents = {}, byId = {};
  data.links.forEach(function (l) {
    (kids[l.s] = kids[l.s] || []).push(l.t);
    (parents[l.t] = parents[l.t] || []).push(l.s);
  });
  data.nodes.forEach(function (n) { byId[n.id] = n; n.open = n.depth < 1; });

  /* thin HUD chevrons, one design per category, inherited by everything under it */
  var GLYPH = [
    "M2 4 L11 11 L2 18 M9 4 L18 11 L9 18",
    "M2 5 L14 11 L2 17 M2 11 H8",
    "M1 4 L8 11 L1 18 M7 5 L13 11 L7 17 M12 6 L17 11 L12 16",
    "M3 4 L14 11 L3 18 M1 2 V6 M1 20 V16 M17 8 V14",
    "M2 4 L18 11 L2 18 L7 11 Z",
    "M3 4 L14 11 L3 18 M1 8 H6 M1 14 H6",
    "M3 3 L15 11 L3 19 M3 8 H10 M3 14 H10"
  ];
  var CATORDER = [];
  data.nodes.forEach(function (n) {
    if (n.kind === "category") CATORDER.push(n.id);
  });
  function route(id) {
    var n = byId[id];
    return (n && n.via) || (parents[id] || [])[0] || null;
  }
  var glyphOf = {};
  function glyphIndex(n) {
    if (n.kind === "root") return 3;
    if (n.kind === "section") return 1;
    if (glyphOf[n.id] !== undefined) return glyphOf[n.id];
    var up = n.id, g = 0, found = null;
    while (up && g++ < 14) {
      if (byId[up].kind === "category") { found = up; break; }
      up = route(up);
    }
    glyphOf[n.id] = found ? 2 + (CATORDER.indexOf(found) % 5) : 0;
    return glyphOf[n.id];
  }

  var WHAT = { root: "The front page", section: "Section", category: "Category",
               series: "Series", episode: "Episode" };

  function esc(t) {
    return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function rowHTML(n, last) {
    var ch = kids[n.id] || [];
    var open = ch.length && n.open;
    var link = n.url
      ? '<a class="sm-open" href="' + esc(n.url) + '"' +
        (/^https?:/.test(n.url) ? ' target="_blank" rel="noopener"' : '') +
        '>Open<span class="sm-arrow" aria-hidden="true">&rarr;</span></a>'
      : "";
    var count = ch.length
      ? '<span class="sm-n">' + ch.length + '</span>'
      : "";
    return '' +
      '<div class="sm-row sm-' + n.kind + (open ? " is-open" : "") +
        (last ? " is-last" : "") + '" data-id="' + esc(n.id) + '">' +
        '<div class="sm-rail" aria-hidden="true"></div>' +
        '<button class="sm-hit" type="button"' +
          (ch.length ? ' aria-expanded="' + (open ? "true" : "false") + '"' : "") + '>' +
          '<svg class="sm-mark" viewBox="0 0 20 22" aria-hidden="true">' +
            '<path d="' + GLYPH[glyphIndex(n)] + '"/></svg>' +
          '<span class="sm-text">' +
            '<span class="sm-label">' + esc(n.label) + '</span>' +
            '<span class="sm-meta">' + WHAT[n.kind] +
              (ch.length ? ", " + ch.length + " below" : "") + '</span>' +
          '</span>' +
          count +
        '</button>' +
        link +
      '</div>';
  }

  function render() {
    var html = "";
    (function walk(id, depth) {
      var n = byId[id];
      html += '<div class="sm-lvl" style="--d:' + depth + '">' + rowHTML(n) + '</div>';
      if (!n.open) return;
      var ch = (kids[id] || []).filter(function (k) { return route(k) === id || !byId[k].placed; });
      ch.forEach(function (k, i) {
        byId[k].placed = true;
        byId[k].via = id;
        walk(k, depth + 1);
      });
    })("home", 0);
    host.innerHTML = html;

    host.querySelectorAll(".sm-hit").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.closest(".sm-row").getAttribute("data-id");
        var n = byId[id];
        if (!(kids[id] || []).length) return;
        n.open = !n.open;
        data.nodes.forEach(function (x) { if (x.depth > n.depth) x.placed = false; });
        render();
        var again = host.querySelector('.sm-row[data-id="' + id + '"] .sm-hit');
        if (again) again.focus({ preventScroll: true });
      });
    });
  }

  var expand = document.getElementById("sm-expandall");
  if (expand) expand.addEventListener("click", function () {
    var all = data.nodes.every(function (n) { return !(kids[n.id] || []).length || n.open; });
    data.nodes.forEach(function (n) { n.open = all ? n.depth < 1 : true; n.placed = false; });
    expand.textContent = all ? "Open everything" : "Close it back down";
    render();
  });
  var reset = document.getElementById("sm-reset");
  if (reset) reset.addEventListener("click", function () {
    data.nodes.forEach(function (n) { n.open = n.depth < 1; n.placed = false; n.via = null; });
    render();
    window.scrollTo({ top: host.offsetTop - 80, behavior: "smooth" });
  });

  render();
})();
