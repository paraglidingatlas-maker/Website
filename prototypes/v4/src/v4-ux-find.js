/* A SEARCH FIELD IN THE PAGE (the usability pass, 15). Inlined in the pages
   that carry one ([data-v4-find]: the knowledge base's), by tools/v4_ux.py. It
   runs the site's one search (v4-menu.js, loaded on first use, as the header's
   search loads it) into its own list. Enter goes to the first result; without
   script the form goes to the sitemap, which lists every page. */
(function () {
  var d = document, w = window;
  var m = /^(.*\/prototypes\/v\d+\/)/.exec(location.pathname);
  var SRC = m ? m[1] + "v4-menu.js" : "/assets/v4/v4-menu.js", waiting = null;
  function get(cb) {
    if (w.V4_MENU) { cb(); return; }
    if (waiting) { waiting.push(cb); return; }
    waiting = [cb];
    var s = d.createElement("script");
    s.src = SRC;
    s.onload = function () { var q = waiting; waiting = null; if (w.V4_MENU) q.forEach(function (f) { f(); }); };
    s.onerror = function () { waiting = null; };
    d.head.appendChild(s);
  }
  [].forEach.call(d.querySelectorAll("[data-v4-find]"), function (form) {
    var q = form.querySelector("input[type=search]"), ol = form.querySelector("ol");
    if (!q || !ol) return;
    function go() { get(function () { w.V4_MENU.find(q.value, ol); }); }
    q.addEventListener("focus", function () { get(function () {}); });
    q.addEventListener("input", go);
    form.addEventListener("submit", function (e) {
      var a = ol.querySelector("a[href]");
      if (a) { e.preventDefault(); location.href = a.href; } else if (w.V4_MENU) { e.preventDefault(); go(); }
    });
  });
})();
