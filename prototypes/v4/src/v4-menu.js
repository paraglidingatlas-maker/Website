/* v4-menu.js: the full-screen menu and the search (loaded on first use by
   v2-immersive.js, 8). */
/* V4 MENU (prototypes/v4 only)
   8. THE FULL-SCREEN MENU AND THE ONE SEARCH. The menu button (and on a
      phone the header's menu toggle) opens a full-screen menu: the four
      sections, each with its photograph, and one search across episodes, the
      knowledge base, trips and topics, from an index of the pages' own titles
      and descriptions (search-index.js, loaded when the search first opens).
      The photographs load only when the menu opens. Focus stays inside, Escape
      closes it and gives focus back. Reduced motion: it appears without the
      slide. */
(function () {
  "use strict";
  var d = document, w = window;
  var m = /^(.*\/prototypes\/v\d+\/)/.exec(location.pathname);
  var BASE = m ? m[1] : "/";                        // the prototype's root
  var LIVE = m ? BASE.replace(/prototypes\/v\d+\/$/, "") : "/"; // the site's root (the assets)
  // after the switch-over the pages sit at the root and this folder's files under assets/v4/
  var IDX = m ? BASE + "search-index.js" : "/assets/v4/search-index.js";
  var SECTIONS = [
    ["Expeditions", "index.html#destinations", "assets/destinations/india/hero/snowline.webp", [["India", "destinations/india.html"], ["Kenya", "destinations/kenya.html"]]],
    ["Podcast", "podcast.html", "assets/images/pod-hero-gemona.webp", [["Library", "library.html"], ["Topics", "tags.html"]]],
    ["Knowledge Base", "knowledge-base.html", "assets/images/kb-flight-mechanics.webp", []],
    ["About", "about.html", "assets/images/partners-aninder.webp", [["Mission Statement", "mission.html"], ["Partner With Me", "partners.html"]]]
  ];
  var menu = null, lastFocus = null, idx = null;

  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function build() {
    menu = d.createElement("div");
    menu.className = "v4-menu";
    menu.id = "v4Menu";
    menu.setAttribute("role", "dialog");
    menu.setAttribute("aria-modal", "true");
    menu.setAttribute("aria-label", "Menu and search");
    menu.hidden = true;
    var here = location.pathname.slice(BASE.length);
    var go = SECTIONS.map(function (s, i) {
      var cur = d.querySelector('.v4-nav a.is-here');
      var on = cur && cur.textContent.trim() === s[0];
      return '<li class="v4-mg' + (on ? " is-here" : "") + '"><a class="v4-mg-a" href="' + BASE + s[1] + '"' + (on ? ' aria-current="page"' : "") + '>' +
        '<span class="v4-mg-img" data-bg="' + LIVE + s[2] + '" aria-hidden="true"></span>' +
        '<span class="v4-mg-n" aria-hidden="true">0' + (i + 1) + '</span><span class="v4-mg-t">' + s[0] + '</span></a>' +
        (s[3].length ? '<span class="v4-mg-sub">' + s[3].map(function (x) { return '<a href="' + BASE + x[1] + '">' + x[0] + '</a>'; }).join("") + '</span>' : "") +
        '</li>';
    }).join("");
    menu.innerHTML =
      '<div class="v4-menu-in">' +
      '<div class="v4-menu-bar"><a class="v4-menu-home" href="' + BASE + 'index.html">Paragliding Atlas</a>' +
      '<button type="button" class="v4-menu-x" aria-label="Close menu"><span aria-hidden="true"></span></button></div>' +
      '<div class="v4-menu-search" role="search"><label class="v4-menu-lab" for="v4q">Search episodes, the knowledge base and trips</label>' +
      '<input id="v4q" type="search" autocomplete="off" placeholder="Search" aria-controls="v4hits">' +
      '<ol class="v4-hits" id="v4hits" aria-live="polite"></ol></div>' +
      '<ul class="v4-menu-go">' + go + '</ul>' +
      '<div class="v4-menu-foot"><a class="btn-solid" href="' + BASE + 'enquire.html"><span>Enquire Now</span></a>' +
      '<a class="btn-lines" href="' + BASE + 'sitemap.html">Sitemap</a></div>' +
      '</div>';
    d.body.appendChild(menu);
    menu.querySelector(".v4-menu-x").addEventListener("click", close);
    menu.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { e.preventDefault(); close(); return; }
      if (e.key !== "Tab") return;
      var f = [].slice.call(menu.querySelectorAll("a[href], button, input")).filter(function (x) { return x.offsetParent !== null; });
      if (!f.length) return;
      if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    });
    var q = menu.querySelector("#v4q");
    q.addEventListener("input", function () { search(q.value); });
    q.addEventListener("focus", loadIndex, { once: true });
  }
  function loadIndex() {
    if (idx || w.V4_SEARCH) { idx = w.V4_SEARCH; return; }
    var s = d.createElement("script");
    s.src = IDX;
    s.onload = function () { idx = w.V4_SEARCH || []; var q = menu.querySelector("#v4q"); if (q.value) search(q.value); };
    d.head.appendChild(s);
  }
  function search(v) {
    var ol = menu.querySelector("#v4hits");
    v = v.trim().toLowerCase();
    if (!v) { ol.innerHTML = ""; return; }
    if (!idx) { loadIndex(); return; }
    var words = v.split(/\s+/);
    var hits = [];
    for (var i = 0; i < idx.length && hits.length < 40; i++) {
      var e = idx[i], hay = (e.t + " " + e.d).toLowerCase(), t = e.t.toLowerCase();
      if (!words.every(function (x) { return hay.indexOf(x) !== -1; })) continue;
      var score = words.reduce(function (a, x) { return a + (t.indexOf(x) !== -1 ? 2 : 1); }, 0);
      hits.push([score, e]);
    }
    hits.sort(function (a, b) { return b[0] - a[0]; });
    ol.innerHTML = hits.length ? hits.slice(0, 8).map(function (h) {
      var e = h[1];
      return '<li><a href="' + BASE + e.u + '"><span class="v4-hit-k">' + esc(e.k) + '</span><span class="v4-hit-t">' + esc(e.t) + '</span></a></li>';
    }).join("") : '<li class="v4-hit-none">Nothing found</li>';
  }
  function open(focusSearch) {
    if (!menu) build();
    menu.querySelectorAll("[data-bg]").forEach(function (x) { x.style.backgroundImage = "url('" + x.getAttribute("data-bg") + "')"; x.removeAttribute("data-bg"); });
    lastFocus = d.activeElement;
    menu.hidden = false;
    d.documentElement.classList.add("v4-menu-open");
    requestAnimationFrame(function () { menu.classList.add("is-open"); });
    (focusSearch ? menu.querySelector("#v4q") : menu.querySelector(".v4-menu-x")).focus();
    syncButtons(true);
  }
  function close() {
    if (!menu || menu.hidden) return;
    menu.classList.remove("is-open");
    d.documentElement.classList.remove("v4-menu-open");
    menu.hidden = true;
    syncButtons(false);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function syncButtons(o) {
    d.querySelectorAll(".v4-open, .nav-toggle").forEach(function (b) { b.setAttribute("aria-expanded", o ? "true" : "false"); });
  }
  window.V4_MENU = { open: open, close: close };
  return;
  function mount() {
    var nav = d.querySelector(".page-wrap > nav");
    if (!nav) return;
    var cta = nav.querySelector(".nav-cta");
    var b = d.createElement("button");
    b.type = "button";
    b.className = "v4-open";
    b.setAttribute("aria-controls", "v4Menu");
    b.setAttribute("aria-expanded", "false");
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg><span>Search</span>';
    b.addEventListener("click", function () { open(true); });
    if (cta) nav.insertBefore(b, cta); else nav.appendChild(b);
    // the phone's menu toggle opens the full-screen menu instead of the small panel
    d.addEventListener("click", function (e) {
      var t = e.target.closest && e.target.closest(".nav-toggle");
      if (!t) return;
      e.preventDefault(); e.stopImmediatePropagation();
      open(false);
    }, true);
  }
})();

