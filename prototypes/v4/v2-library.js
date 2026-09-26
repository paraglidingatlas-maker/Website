/* v2 library: a real browser. The cards are already in the HTML
   (tools/v2_library_cards.py), every one a real link; this only shows, hides,
   sorts and pages them. Search, series filter and sort sit together at the top.
   The stone tiles stay as the entrance to a series: pressing one opens the
   same stone portal as before and lands on the browser with that series
   chosen. The address keeps #s=<series> so old links (the popup's "In series")
   still land on the series. Glyphs and stones are the live library's (library.js). */
(function () {
  "use strict";
  var slow = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
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

  var $ = function (id) { return document.getElementById(id); };
  var PER = document.body.classList.contains("v4-lib-log") || document.body.classList.contains("v4-lib-wall") ? 24 : 12;
  var eps = $("eps"), cards = [].slice.call(eps.querySelectorAll(".ep-tile"));
  var chips = [].slice.call(document.querySelectorAll(".v2-chip"));
  var state = { s: "", q: "", sort: "new", page: 1 };

  document.querySelectorAll(".v2-tiles .tile").forEach(function (t) {
    var big = t.classList.contains("is-feat");
    t.querySelector(".shot").innerHTML = slab(t.getAttribute("data-t"), 200, 138);
  });

  function norm(t) { return String(t).toLowerCase().replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim(); }
  var SORT = {
    "new": function (a, b) { return a.dataset.o - b.dataset.o; },
    "old": function (a, b) { return b.dataset.o - a.dataset.o; },
    "short": function (a, b) { return (+a.dataset.m || 1e9) - (+b.dataset.m || 1e9); },
    "long": function (a, b) { return (+b.dataset.m || 0) - (+a.dataset.m || 0); }
  };

  function hash() {
    var h = state.s ? "#s=" + encodeURIComponent(state.s) : "";
    if (state.page > 1) h += (h ? "&" : "#") + "p=" + state.page;
    if (location.hash !== h) history.replaceState(null, "", h || location.pathname + location.search);
  }

  function draw(scroll) {
    var words = norm(state.q).split(" ").filter(Boolean);
    var hits = cards.filter(function (c) {
      if (state.s && c.dataset.s !== state.s) return false;
      var f = c.dataset.f;
      return words.every(function (w) { return f.indexOf(w) !== -1; });
    }).sort(SORT[state.sort]);
    var pages = Math.max(1, Math.ceil(hits.length / PER));
    if (state.page > pages) state.page = pages;
    var from = (state.page - 1) * PER, show = hits.slice(from, from + PER);
    // reorder in the DOM only when the order changed, so the cards keep their images
    var frag = document.createDocumentFragment();
    hits.forEach(function (c) { frag.appendChild(c); });
    cards.forEach(function (c) { if (hits.indexOf(c) === -1) frag.appendChild(c); });
    eps.appendChild(frag);
    cards.forEach(function (c) { c.hidden = show.indexOf(c) === -1; });

    $("none").hidden = hits.length > 0;
    $("cnt").textContent = hits.length
      ? (hits.length === 1 ? "1 episode" : hits.length + " episodes") +
        (state.s ? " in " + state.s : "") + (words.length ? " matching “" + state.q.trim() + "”" : "") +
        (pages > 1 ? " · page " + state.page + " of " + pages : "")
      : "";
    $("browseH").textContent = state.s || (words.length ? "Search results" : "All episodes");
    chips.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.s === state.s)); });

    var pg = $("pager");
    pg.hidden = pages < 2;
    if (pages > 1) {
      var h = '<button type="button" class="v2-pg" data-p="' + (state.page - 1) + '"' + (state.page === 1 ? " disabled" : "") + ' aria-label="Previous page">&larr;</button>';
      for (var i = 1; i <= pages; i++) {
        h += '<button type="button" class="v2-pg' + (i === state.page ? " is-on" : "") + '" data-p="' + i + '"' +
          (i === state.page ? ' aria-current="page"' : "") + ">" + i + "</button>";
      }
      h += '<button type="button" class="v2-pg" data-p="' + (state.page + 1) + '"' + (state.page === pages ? " disabled" : "") + ' aria-label="Next page">&rarr;</button>';
      pg.innerHTML = h;
    }
    hash();
    if (scroll) {
      var top = $("browse").getBoundingClientRect().top + scrollY - 70;
      if (Math.abs(scrollY - top) > 40) scrollTo({ top: top, behavior: slow ? "auto" : "smooth" });
    }
  }

  $("pager").addEventListener("click", function (e) {
    var b = e.target.closest(".v2-pg"); if (!b || b.disabled) return;
    state.page = +b.dataset.p; draw(true);
  });
  chips.forEach(function (b) {
    b.addEventListener("click", function () { state.s = b.dataset.s; state.page = 1; draw(false); });
  });
  $("q").addEventListener("input", function () { state.q = this.value; state.page = 1; draw(false); });
  $("sort").addEventListener("change", function () { state.sort = this.value; state.page = 1; draw(false); });
  $("widen").addEventListener("click", function () { state.s = ""; state.q = ""; $("q").value = ""; state.page = 1; draw(false); });

  function route() {
    var h = decodeURIComponent(location.hash.replace(/^#/, "")), m;
    var s = (m = /(?:^|&)s=([^&]*)/.exec(h)) ? m[1] : "";
    if (s && !chips.some(function (b) { return b.dataset.s === s; })) s = "";
    state.s = s;
    state.page = (m = /(?:^|&)p=(\d+)/.exec(h)) ? +m[1] : 1;
    draw(!!(s || h === "all"));
  }
  window.addEventListener("hashchange", route);

  /* the stone portal, as on the live library */
  var portal = $("portal"), pbox = portal.querySelector(".pbox");
  function openPortal(shot, done) {
    if (slow) { done(); return; }
    var r = shot.getBoundingClientRect();
    pbox.className = "pbox";
    pbox.style.cssText = "left:" + r.left + "px;top:" + r.top + "px;width:" + r.width + "px;height:" + r.height + "px;";
    portal.classList.add("live");
    void pbox.offsetWidth;
    pbox.classList.add("grow");
    setTimeout(function () { pbox.classList.add("seam"); }, 300);
    setTimeout(function () { done(true); pbox.classList.add("open"); }, 580);
    setTimeout(function () { portal.classList.remove("live"); pbox.className = "pbox"; pbox.style.cssText = ""; }, 1260);
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest ? ev.target.closest(".v2-tiles .tile") : null;
    if (!a || a.classList.contains("zero")) return;
    ev.preventDefault();
    openPortal(a.querySelector(".shot"), function (instant) {
      state.s = a.getAttribute("data-t"); state.page = 1; state.q = ""; $("q").value = "";
      draw(false);
      var top = $("browse").getBoundingClientRect().top + scrollY - 70;
      scrollTo({ top: top, behavior: instant || slow ? "auto" : "smooth" });
    });
  });

  route();
})();
