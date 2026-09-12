/* Library page behaviour.
   Data comes from library-data.js. Durations are enriched at runtime from the
   podcast RSS feed through the existing Cloudflare Worker; if that fetch fails
   the page still works, it just hides the length filter. */
(function () {
  "use strict";

  var RSS = "https://anchor.fm/s/ed1344d8/podcast/rss";
  var PROXY = "https://restless-king-e534.aninder.workers.dev/?url=";
  var slow = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- embossed instrument glyphs, drawn on a 120x120 field ---------- */
  function ring(n, r1, r2) {
    var o = "", i, a;
    for (i = 0; i < n; i++) {
      a = i * 2 * Math.PI / n - Math.PI / 2;
      o += '<path d="M' + (60 + r1 * Math.cos(a)).toFixed(1) + " " + (60 + r1 * Math.sin(a)).toFixed(1) +
           " L" + (60 + r2 * Math.cos(a)).toFixed(1) + " " + (60 + r2 * Math.sin(a)).toFixed(1) + '"/>';
    }
    return o;
  }
  function spin(n, d) {
    var o = "", i;
    for (i = 0; i < n; i++) o += '<g transform="rotate(' + (i * 360 / n) + ' 60 60)"><path d="' + d + '"/></g>';
    return o;
  }

  var GLYPH = {
    "Navigators": '<circle cx="60" cy="60" r="41"/><circle cx="60" cy="60" r="31"/>' +
      '<path d="M60 21 L69 60 L60 99 L51 60 Z"/><path d="M21 60 L60 51 L99 60 L60 69 Z"/>' + ring(8, 44, 50),
    "Sky Gods": '<path d="M22 92 L60 28 L98 92 Z"/><path d="M41 92 L60 60 L79 92"/>' +
      '<circle cx="60" cy="16" r="6"/><path d="M34 22 L42 34"/><path d="M86 22 L78 34"/>',
    "Living the Dream": '<circle cx="60" cy="52" r="19"/><path d="M14 88 H106"/>' +
      '<path d="M26 72 Q60 42 94 72"/>' + ring(10, 25, 32),
    "World Cups": '<circle cx="60" cy="60" r="39"/><circle cx="60" cy="60" r="25"/><circle cx="60" cy="60" r="11"/>' +
      '<path d="M60 8 V26"/><path d="M60 94 V112"/><path d="M8 60 H26"/><path d="M94 60 H112"/>',
    "Risk vs Reward": '<circle cx="60" cy="60" r="40"/><path d="M60 20 V100"/><path d="M28 44 H92"/>' +
      '<path d="M32 44 V56"/><path d="M88 44 V56"/><circle cx="32" cy="66" r="10"/><circle cx="88" cy="66" r="10"/>',
    "Resources, Tools and Tips": '<circle cx="60" cy="60" r="33"/><circle cx="60" cy="60" r="15"/>' + ring(8, 33, 43),
    "Weather Patterns": '<path d="M18 42 Q60 16 102 42"/><path d="M18 60 Q60 34 102 60"/>' +
      '<path d="M18 78 Q60 52 102 78"/><path d="M78 94 L100 84 L92 104"/>',
    "Brand Stories": '<path d="M60 16 L98 38 L98 82 L60 104 L22 82 L22 38 Z"/>' +
      '<path d="M60 32 L84 46 L84 74 L60 88 L36 74 L36 46 Z"/><path d="M44 60 H76"/>',
    "Storytellers": '<circle cx="60" cy="60" r="37"/>' + spin(6, "M60 23 L92 41") + '<circle cx="60" cy="60" r="9"/>',
    "The Dark Side": '<circle cx="56" cy="60" r="34"/><circle cx="74" cy="52" r="34"/>' + ring(12, 40, 47),
    "Flight Mechanics": '<path d="M20 72 Q50 44 100 56 Q64 70 20 72 Z"/><path d="M14 44 H72"/>' +
      '<path d="M14 88 H84"/><path d="M66 40 L74 44 L66 48"/>',
    "New Technologies": '<circle cx="60" cy="60" r="13"/><path d="M60 47 V20"/><path d="M60 73 V100"/>' +
      '<path d="M47 60 H20"/><path d="M73 60 H100"/><circle cx="60" cy="16" r="6"/>' +
      '<circle cx="60" cy="104" r="6"/><circle cx="16" cy="60" r="6"/><circle cx="104" cy="60" r="6"/>' +
      '<path d="M34 34 L50 50"/><path d="M86 86 L70 70"/>',
    "Know Your Equipment": '<rect x="33" y="18" width="54" height="84" rx="27"/>' +
      '<path d="M87 46 L57 30"/><path d="M33 62 H87"/><circle cx="60" cy="86" r="9"/>'
  };

  function emboss(p) {
    return '<g class="gl" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">' +
      '<g class="gl-cut" transform="translate(1.4,1.7)">' + p + '</g>' +
      '<g class="gl-hi" transform="translate(-1.3,-1.6)">' + p + '</g>' +
      '<g class="gl-face">' + p + '</g></g>';
  }

  function slab(k, w, h) {
    var id = "g" + k.replace(/\W/g, "");
    return '<svg viewBox="0 0 ' + w + " " + h + '" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' +
      '<defs><linearGradient id="' + id + '" x1="0" y1="0" x2="0.65" y2="1">' +
      '<stop offset="0" stop-color="var(--stone-hi)"/><stop offset="1" stop-color="var(--stone-lo)"/>' +
      '</linearGradient></defs>' +
      '<rect width="' + w + '" height="' + h + '" fill="url(#' + id + ')"/>' +
      '<rect width="' + w + '" height="' + h + '" filter="url(#grain2)" opacity="0.3" style="mix-blend-mode:overlay"/>' +
      '<rect width="' + w + '" height="' + h + '" filter="url(#grain)" opacity="0.42" style="mix-blend-mode:overlay"/>' +
      '<g fill="none" stroke-width="1.4" class="hud-tick">' +
      '<path d="M14 ' + (h - 14) + " H" + (w * 0.3) + '"/><path d="M' + (w - 14) + " 14 H" + (w * 0.7) + '"/></g>' +
      '<g fill="none" stroke-width="2" class="hud-brk">' +
      '<path d="M12 26 V12 H26"/><path d="M' + (w - 26) + " " + (h - 12) + " H" + (w - 12) + " V" + (h - 26) + '"/></g>' +
      '<g class="seamsweep"><rect x="0" y="' + (h * 0.5) + '" width="' + w + '" height="1" fill="var(--orange)" opacity="0.28"/></g>' +
      '<g transform="translate(' + ((w - 120) / 2) + "," + ((h - 120) / 2) + ')">' + emboss(GLYPH[k] || "") + '</g>' +
      '</svg>';
  }

  /* ---------- helpers ---------- */
  var $ = function (id) { return document.getElementById(id); };

  /* every reference to an episode across the site resolves to one page */
  function episodeHref(id) {
    var pages = window.EPISODE_PAGES || {};
    return pages[id] ? "episodes/" + pages[id] + ".html"
                     : "https://www.youtube.com/watch?v=" + id;
  }
  function esc(t) {
    return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function hhmm(s) {
    var h = Math.floor(s / 3600), m = Math.round((s % 3600) / 60);
    return h ? h + "h " + (m < 10 ? "0" + m : m) + "m" : m + " min";
  }
  function norm(t) {
    return String(t).toLowerCase().replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim();
  }
  function inTopic(k) {
    return LIB_EPISODES.filter(function (e) { return e.topic === k; });
  }

  var EDGES = ["edge-lb", "edge-tr", "edge-b", "edge-l"];
  var REST = Object.keys(LIB_TOPICS).filter(function (k) {
    return LIB_FEATURED.indexOf(k) === -1;
  });

  /* ---------- landing ---------- */
  function tileHTML(k, n, big) {
    var c = inTopic(k).length;
    return '<a class="tile ' + EDGES[n % 4] + (c ? "" : " zero") + '" href="#s=' +
      encodeURIComponent(k) + '" data-t="' + encodeURIComponent(k) + '">' +
      '<div class="shot">' + slab(k, 200, big ? 150 : 138) + "</div>" +
      "<h3>" + esc(k) + "</h3>" +
      '<div class="meta">' + (c ? c + (c === 1 ? " episode" : " episodes") + " in " + LIB_TOPICS[k]
        : "Coming soon in " + LIB_TOPICS[k]) + "</div></a>";
  }
  $("feat").innerHTML = LIB_FEATURED.map(function (k, n) { return tileHTML(k, n, true); }).join("");
  $("rest").innerHTML = REST.map(function (k, n) { return tileHTML(k, n + 1, false); }).join("");
  $("seriesCount").textContent = Object.keys(LIB_TOPICS).length + " series, " +
    LIB_EPISODES.length + " episodes";

  /* ---------- filters ---------- */
  var LEN = [
    ["Any length", function () { return true; }],
    ["Under 20 min", function (e) { return e.secs && e.secs < 1200; }],
    ["20 to 60 min", function (e) { return e.secs && e.secs >= 1200 && e.secs <= 3600; }],
    ["Over an hour", function (e) { return e.secs && e.secs > 3600; }]
  ];
  var SRT = [
    ["Newest first", function (a, b) { return a.order - b.order; }],
    ["Oldest first", function (a, b) { return b.order - a.order; }],
    ["Shortest first", function (a, b) { return (a.secs || 1e9) - (b.secs || 1e9); }],
    ["Longest first", function (a, b) { return (b.secs || 0) - (a.secs || 0); }]
  ];

  var topic = null, q = "", fl = 0, fs = 0, haveDurations = false;

  function bar() {
    var html = "";
    if (haveDurations) {
      html += LEN.map(function (x, n) {
        return '<button class="pill' + (n === fl ? " on" : "") + '" data-k="l" data-n="' + n + '" type="button">' + x[0] + "</button>";
      }).join("") + '<span class="bargap"></span>';
    }
    html += SRT.slice(0, haveDurations ? 4 : 2).map(function (x, n) {
      return '<button class="pill' + (n === fs ? " on" : "") + '" data-k="s" data-n="' + n + '" type="button">' + x[0] + "</button>";
    }).join("");
    $("bar").innerHTML = html;
    Array.prototype.forEach.call($("bar").querySelectorAll(".pill"), function (b) {
      b.addEventListener("click", function () {
        var n = +b.getAttribute("data-n");
        if (b.getAttribute("data-k") === "l") fl = n; else fs = n;
        draw();
      });
    });
  }

  var EXPAND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M9 4H4v5"/><path d="M15 20h5v-5"/><path d="M4 4l6 6"/><path d="M20 20l-6-6"/></svg>';

  function card(e) {
    /* The same card the knowledge base series pages use. This page used to draw
       a bare image with text under it, which is why it read as belonging to a
       different site.

       The still is maxresdefault, a true 16:9 frame. It asked for hqdefault,
       which is 480x360: a 4:3 frame with black bars baked in, then cropped to
       16:10, so real picture was being cut out of the middle of every tile.
       This was the last place on the site still doing that. */
    var d = (window.LIB_MODAL || {})[e.page] || null;
    var href = e.page ? 'episodes/' + e.page + '.html' : episodeHref(e.id);
    var dur = e.secs ? hhmm(e.secs) : '';
    var epno = d && d.epno ? d.epno : '';
    var guest = d && d.shownGuest ? d.shownGuest : '';
    var title = d && d.shownTitle ? d.shownTitle : e.title;
    var chapters = d && d.nchapters
      ? (d.nchapters === 1 ? '1 chapter' : d.nchapters + ' chapters')
      : '<span class="dim">No chapters yet</span>';
    var audio = (d && !d.video) ? '<span class="ep-audio">Audio only</span>' : '';
    return '<a class="ep-tile" href="' + href + '"' +
      (e.page ? ' data-ep-slug="' + esc(e.page) + '"' : ' target="_blank" rel="noopener"') + '>' +
      '<span class="ep-stamp">' + esc(epno) + '<i>' + esc(dur) + '</i></span>' +
      '<span class="ep-th"><img loading="lazy" src="https://i.ytimg.com/vi/' + e.id +
      '/maxresdefault.jpg" alt="" onerror="this.onerror=null;this.src=' +
      "'https://i.ytimg.com/vi/" + e.id + "/mqdefault.jpg'" + '">' + audio + '</span>' +
      '<span class="ep-tile-body"><span class="ep-tile-title">' + esc(title) + '</span>' +
      (guest ? '<span class="ep-tile-guest">' + esc(guest) + '</span>' : '') + '</span>' +
      '<span class="ep-foot">' + chapters + '<i>' + EXPAND + '</i></span></a>';
  }

  function draw() {
    bar();
    var hits = LIB_EPISODES.filter(function (e) {
      return (!topic || e.topic === topic) && LEN[fl][1](e) &&
        (!q || norm(e.title).indexOf(q) !== -1);
    }).slice().sort(SRT[fs][1]);
    $("eps").innerHTML = hits.map(card).join("");
    $("cnt").textContent = hits.length + (hits.length === 1 ? " episode" : " episodes");
    $("none").classList.toggle("lib-hidden", hits.length > 0);
  }
  function reset() { q = ""; fl = 0; fs = 0; }

  function show(t, title, sub) {
    topic = t;
    var r = $("results");
    var entering = r.classList.contains("lib-hidden");
    $("landing").classList.add("lib-hidden");
    r.classList.remove("lib-hidden");
    $("rT").textContent = title;
    $("rS").textContent = sub;
    draw();
    if (entering) {                /* not on every keystroke */
      window.scrollTo({ top: 0 });
      r.classList.remove("opening");
      void r.offsetWidth;
      r.classList.add("opening");
    }
  }
  function home() {
    ["q", "q2"].forEach(function (id) { var el = $(id); if (el) el.value = ""; });
    $("results").classList.add("lib-hidden");
    $("landing").classList.remove("lib-hidden");
    topic = null;
    reset();
    window.scrollTo({ top: 0 });
  }
  function route() {
    var h = decodeURIComponent(location.hash.replace(/^#/, ""));
    if (h.indexOf("s=") === 0) {
      var k = h.slice(2);
      // LIB_TOPICS holds the CATEGORY a series sits in, not a label, so
      // appending "series" produced "Core series series" on every filtered
      // view. The category is what the subtitle should say, on its own.
      if (LIB_TOPICS[k]) { reset(); show(k, k, LIB_TOPICS[k]); return; }
    }
    if (h === "all") { reset(); show(null, "All episodes", "Everything published, newest first."); return; }
    home();
  }
  window.addEventListener("hashchange", route);

  /* ---------- portal ---------- */
  var portal = $("portal"), pbox = portal.querySelector(".pbox");
  function openPortal(shot, hash) {
    if (slow) { location.hash = hash; return; }
    var r = shot.getBoundingClientRect();
    pbox.className = "pbox";
    pbox.style.cssText = "left:" + r.left + "px;top:" + r.top + "px;width:" +
      r.width + "px;height:" + r.height + "px;";
    portal.classList.add("live");
    void pbox.offsetWidth;
    pbox.classList.add("grow");
    setTimeout(function () { pbox.classList.add("seam"); }, 300);
    setTimeout(function () { location.hash = hash; pbox.classList.add("open"); }, 580);
    setTimeout(function () {
      portal.classList.remove("live");
      pbox.className = "pbox";
      pbox.style.cssText = "";
    }, 1260);
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest ? ev.target.closest(".tile") : null;
    if (!a || a.classList.contains("zero")) return;
    ev.preventDefault();
    openPortal(a.querySelector(".shot"), "#s=" + a.getAttribute("data-t"));
  });

  $("back").addEventListener("click", function () { location.hash = ""; });
  $("allBtn").addEventListener("click", function () { location.hash = "all"; });
  $("widen").addEventListener("click", function () { reset(); draw(); });
  /* The search box used to live only inside #landing, and show() hides #landing.
     So the first keystroke hid the box the user was typing into, and the handler
     also cleared its value, which meant a query could never be longer than one
     character. There are now two boxes, one per view, kept in sync, and neither
     is cleared while typing. */
  function onSearch(v) {
    v = String(v).trim();
    if (!v) {                      /* emptying the box goes back, it does not sit on a stale result */
      q = "";
      if (topic === null) { location.hash = ""; } else { draw(); }
      return;
    }
    q = norm(v);
    show(null, "Search results", 'Matching "' + v + '" across every episode.');
  }
  function syncBoxes(from, v) {
    ["q", "q2"].forEach(function (id) {
      var el = $(id);
      if (el && el !== from && el.value !== v) el.value = v;
    });
  }
  /* Keeping the two boxes in sync was not enough. #q lives inside #landing, and
     the first keystroke calls show(), which hides #landing. A hidden input
     cannot hold focus, so the browser dropped the caret and the reader had to
     click into the other box to type a second character. That is the "it
     searches after one letter and then I have to click again" report. Whenever
     the box being typed into has just been hidden by a view swap, hand the caret
     to its visible twin and put it back at the end of the text. */
  function keepCaret(from) {
    if (!from) return;
    if (from.offsetParent !== null) return;        /* still on screen, nothing to do */
    var twin = $(from.id === "q" ? "q2" : "q");
    if (!twin || twin.offsetParent === null) return;
    twin.focus();
    var end = twin.value.length;
    try { twin.setSelectionRange(end, end); } catch (e) { /* older browsers */ }
  }
  ["q", "q2"].forEach(function (id) {
    var el = $(id);
    if (!el) return;
    el.addEventListener("input", function (ev) {
      var typing = ev.target;
      syncBoxes(typing, typing.value);
      onSearch(typing.value);
      keepCaret(typing);
    });
  });

  /* ---------- enrich with real durations from the podcast feed ---------- */
  function enrich() {
    fetch(PROXY + encodeURIComponent(RSS))
      .then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); })
      .then(function (xml) {
        var doc = new DOMParser().parseFromString(xml, "application/xml");
        var items = doc.querySelectorAll("item");
        if (!items.length) return;
        var byTitle = {};
        Array.prototype.forEach.call(items, function (it) {
          var t = it.querySelector("title"), d = it.getElementsByTagName("itunes:duration")[0];
          if (!t || !d) return;
          var parts = d.textContent.trim().split(":").map(Number);
          var secs = parts.length === 3 ? parts[0] * 3600 + parts[1] * 60 + parts[2]
            : parts.length === 2 ? parts[0] * 60 + parts[1] : parts[0];
          if (secs) byTitle[norm(t.textContent)] = secs;
        });
        var keys = Object.keys(byTitle), matched = 0;
        LIB_EPISODES.forEach(function (e) {
          var n = norm(e.title);
          if (byTitle[n]) { e.secs = byTitle[n]; matched++; return; }
          /* titles differ slightly between YouTube and the feed, so fall back
             to the best word overlap above a confident threshold */
          var words = n.split(" "), best = 0, bestKey = null;
          keys.forEach(function (k) {
            var kw = k.split(" "), hit = 0;
            words.forEach(function (w) { if (w.length > 3 && kw.indexOf(w) !== -1) hit++; });
            var score = hit / Math.max(6, Math.min(words.length, kw.length));
            if (score > best) { best = score; bestKey = k; }
          });
          if (best >= 0.7 && bestKey) { e.secs = byTitle[bestKey]; matched++; }
        });
        if (matched > 10) { haveDurations = true; if (!$("results").classList.contains("lib-hidden")) draw(); }
      })
      .catch(function () { /* feed unavailable: the page works without durations */ });
  }

  route();
  enrich();
})();
