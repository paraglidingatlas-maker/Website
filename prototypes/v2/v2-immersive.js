/* V2 IMMERSION (prototypes/v2/ only). One flight across the whole site.

   1. DEPTH. Every page sits at an altitude: the homepage highest, the section
      pages (podcast, library, about, Kenya, India, topics, knowledge base) a
      level down, single episodes, topics and categories lowest. Moving to a
      deeper page descends (the old page lifts away, the new one rises from
      below), moving up climbs, same level glides sideways. Direction is
      decided on pageswap, remembered for the next page, and handed to CSS as
      a class on <html> for the length of the transition.
   2. THE INSTRUMENT. A small altitude and heading readout (wide screens)
      that follows the page and the scroll, and a line in it that banks with
      scroll speed. Decorative, aria-hidden.
   3. TOUCH. Under a fine pointer, cards tilt a little towards the pointer and
      carry a soft light; the hero sky shifts with the pointer. The episode
      rails lean with their own momentum.
   4. INTO THE PICTURE. Pressing a destination's picture on the homepage grows
      that picture into the destination's hero.
   5. WIND. An optional wind sound, off until asked for (button in the header),
      made in the browser (filtered noise, no file), gusting with scroll speed,
      silent while the tab is hidden. The choice is remembered.

   Nothing here runs on its own: every frame is caused by a scroll, a pointer
   or a transition, and stops when they do. Reduced motion: 1 to 4 are off
   (the page changes exactly as before); the wind stays available because it
   is sound, not motion. */
(function () {
  "use strict";
  var d = document, root = d.documentElement, w = window;
  var mm = function (q) { return w.matchMedia && w.matchMedia(q).matches; };
  var still = mm("(prefers-reduced-motion: reduce)");
  var fine = mm("(hover: hover) and (pointer: fine)");
  var store = { get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
                set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} } };
  var keep = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
               set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };

  /* ---------------------------------------------------------------- depth */
  function depthOf(path) {
    var m = /\/prototypes\/v2\/(.*)$/.exec(path) || [null, path.replace(/^\//, "")];
    var p = m[1] || "index.html";
    if (p === "" || p === "index.html") return 0;
    if (/^(episodes|tags|knowledge-base)\//.test(p)) return 2;
    if (/^destinations\//.test(p)) return 1;
    return 1;
  }
  var here = depthOf(location.pathname);
  root.setAttribute("data-depth", here);

  w.addEventListener("pageswap", function (e) {
    if (!e.viewTransition || !e.activation || !e.activation.entry) return;
    var to = depthOf(new URL(e.activation.entry.url).pathname);
    var dir = to > here ? "descend" : to < here ? "climb" : "glide";
    root.classList.add("vt-" + dir);
    store.set("v2-vt", dir);
  });
  w.addEventListener("pagereveal", function (e) {
    var dir = store.get("v2-vt"); store.set("v2-vt", "");
    if (!e.viewTransition || !dir) return;
    root.classList.add("vt-" + dir);
    var done = function () { root.classList.remove("vt-descend", "vt-climb", "vt-glide"); };
    e.viewTransition.finished.then(done, done);
  });
  // coming back with the browser's back button restores the page from cache:
  // clear the class the swap left on it
  w.addEventListener("pageshow", function () { root.classList.remove("vt-descend", "vt-climb", "vt-glide"); });

  /* ------------------------------------------------ into the picture (4) */
  if (!still) {
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[href*="destinations/"]');
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey) return;
      var block = a.closest(".v2-dest");
      var img = block && block.querySelector(".kit-feature-media img");
      if (!img) return;
      img.style.viewTransitionName = "v2-dest";
      store.set("v2-dest", "1");
    }, true);
    w.addEventListener("pagereveal", function (e) {
      if (store.get("v2-dest") !== "1") return;
      store.set("v2-dest", "");
      var img = d.querySelector(".khero-slide.is-on img, .khero-slide img");
      if (!img || !e.viewTransition) return;
      img.style.viewTransitionName = "v2-dest";
      var off = function () { img.style.viewTransitionName = ""; };
      e.viewTransition.finished.then(off, off);
    });
    w.addEventListener("pageshow", function () {
      d.querySelectorAll(".kit-feature-media img").forEach(function (i) { i.style.viewTransitionName = ""; });
    });
  }

  /* the rest needs the page itself; this file loads in the head so that the
     transition listeners above are in place before the first frame */
  var wind = { gust: function () {} };
  function ready() {
  /* --------------------------------------------------- the instrument (2) */
    var hud = null, hudAlt, hudHdg, hudLine, lastY = w.scrollY, lastT = 0, bank = 0, bankRaf = 0;
    var BASE = [4200, 3100, 2200][here] || 3100;
    var HDG = (function () { var h = 0, s = location.pathname; for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 360; return h; })();
    // docked in the header's coordinate slot, so it never sits over content
    var slot = d.querySelector(".page-wrap > nav .nav-coords");
    if (slot) {
      hud = slot;
      slot.classList.add("v2-hud");
      slot.setAttribute("aria-hidden", "true");
      slot.innerHTML = '<span class="v2-hud-att"><i></i></span><span class="v2-hud-row"><b>ALT</b><em class="a"></em></span>' +
                       '<span class="v2-hud-row"><b>HDG</b><em class="h"></em></span>';
      hudAlt = slot.querySelector(".a"); hudHdg = slot.querySelector(".h"); hudLine = slot.querySelector(".v2-hud-att i");
    }
    function pad3(n) { n = ((Math.round(n) % 360) + 360) % 360; return (n < 10 ? "00" : n < 100 ? "0" : "") + n; }
    function paintHud() {
      if (!hud) return;
      var max = Math.max(1, root.scrollHeight - innerHeight), p = Math.min(1, w.scrollY / max);
      hudAlt.textContent = (Math.round((BASE - p * 900) / 10) * 10).toLocaleString("en-US") + " m";
      hudHdg.textContent = pad3(HDG + p * 24) + "°";
    }
    function settleBank() {
      bank *= 0.86;
      if (hudLine) hudLine.style.transform = "rotate(" + bank.toFixed(2) + "deg)";
      root.style.setProperty("--v2-gust", Math.min(1, Math.abs(bank) / 14).toFixed(3));
      if (Math.abs(bank) > 0.05) bankRaf = requestAnimationFrame(settleBank); else { bankRaf = 0; bank = 0; }
    }
    var scrollQueued = false;
    w.addEventListener("scroll", function () {
      if (scrollQueued) return; scrollQueued = true;
      requestAnimationFrame(function () {
        scrollQueued = false;
        var t = performance.now(), y = w.scrollY, v = (y - lastY) / Math.max(16, t - lastT);
        lastY = y; lastT = t;
        bank = Math.max(-14, Math.min(14, bank + v * 6));
        paintHud();
        wind.gust(Math.min(1, Math.abs(v) / 3));
        if (!bankRaf) bankRaf = requestAnimationFrame(settleBank);
      });
    }, { passive: true });
    paintHud();

    /* ------------------------------------------------------------ touch (3) */
    var CARDS = ".kit-card, .kit-panel, .ep-card, .ep-tile, .tg-v2 .tg-ep, .v2-door, .tile, .cd-box, .ep2-card";
    if (!still && fine) {
      var cur = null, raf = 0, px = 0, py = 0;
      var apply = function () {
        raf = 0; if (!cur) return;
        var r = cur.getBoundingClientRect(), x = (px - r.left) / r.width, y = (py - r.top) / r.height;
        cur.style.setProperty("--mx", (x * 100).toFixed(1) + "%");
        cur.style.setProperty("--my", (y * 100).toFixed(1) + "%");
        cur.style.transform = "perspective(900px) rotateX(" + ((0.5 - y) * 5).toFixed(2) + "deg) rotateY(" + ((x - 0.5) * 6).toFixed(2) + "deg)";
      };
      var leave = function (el) {
        // ease back to flat, then hand the transition list back to the card
        el.style.transition = "transform .5s cubic-bezier(.2,.8,.2,1), translate .26s cubic-bezier(.2,.8,.2,1), scale .16s cubic-bezier(.2,.8,.2,1)";
        el.style.transform = ""; el.classList.remove("v2-lit");
        setTimeout(function () { if (el !== cur) el.style.transition = ""; }, 520);
      };
      d.addEventListener("pointermove", function (e) {
        if (e.pointerType !== "mouse") return;
        var el = e.target.closest && e.target.closest(CARDS);
        if (el !== cur) {
          if (cur) leave(cur);
          cur = el;
          if (cur) {
            cur.style.transition = "";
            cur.classList.add("v2-lit");
            if (!cur.querySelector(":scope > .v2-glint")) {
              var g = d.createElement("i"); g.className = "v2-glint"; g.setAttribute("aria-hidden", "true"); cur.appendChild(g);
            }
          }
        }
        px = e.clientX; py = e.clientY;
        if (cur && !raf) raf = requestAnimationFrame(apply);
      }, { passive: true });
      d.addEventListener("pointerleave", function () { if (cur) { leave(cur); cur = null; } }, true);

      // the hero sky follows the pointer a little
      var hero = d.querySelector(".kit-hero:not(.is-sky)");
      if (hero) {
        var hraf = 0, hx = 0, hy = 0;
        hero.addEventListener("pointermove", function (e) {
          hx = e.clientX / innerWidth - 0.5; hy = e.clientY / innerHeight - 0.5;
          if (!hraf) hraf = requestAnimationFrame(function () {
            hraf = 0;
            hero.style.setProperty("--hx", (hx * -18).toFixed(1) + "px");
            hero.style.setProperty("--hy", (hy * -12).toFixed(1) + "px");
          });
        }, { passive: true });
      }
    }
    // rails lean with their momentum (touch too: it is the scroll that drives it)
    if (!still) {
      d.querySelectorAll(".v2-rail").forEach(function (rail) {
        var lx = rail.scrollLeft, lean = 0, lraf = 0;
        var settle = function () {
          lean *= 0.82;
          rail.style.setProperty("--lean", lean.toFixed(2));
          if (Math.abs(lean) > 0.05) lraf = requestAnimationFrame(settle); else { lraf = 0; rail.style.setProperty("--lean", "0"); }
        };
        rail.addEventListener("scroll", function () {
          var dx = rail.scrollLeft - lx; lx = rail.scrollLeft;
          lean = Math.max(-9, Math.min(9, lean + dx * 0.12));
          if (!lraf) lraf = requestAnimationFrame(settle);
        }, { passive: true });
      });
    }

    // rails: drag with the mouse; data-auto rails also drift on their own,
    // but only while on screen, untouched and unhovered, and never for reduced motion
    d.querySelectorAll(".v2-rail").forEach(function (rail) {
      var down = false, sx = 0, sl = 0, moved = 0, dragged = 0;
      rail.addEventListener("dragstart", function (e) { e.preventDefault(); });
      rail.addEventListener("pointerdown", function (e) {
        if (e.pointerType !== "mouse" || e.button !== 0) return;
        down = true; moved = 0; sx = e.clientX; sl = rail.scrollLeft;
      });
      w.addEventListener("pointermove", function (e) {
        if (!down) return;
        var dx = e.clientX - sx;
        if (Math.abs(dx) > 4) { rail.classList.add("is-dragging"); moved = Math.max(moved, Math.abs(dx)); }
        if (moved) rail.scrollLeft = sl - dx;
      }, { passive: true });
      var up = function () { if (!down) return; down = false; if (moved > 6) dragged = Date.now(); rail.classList.remove("is-dragging"); };
      w.addEventListener("pointerup", up); w.addEventListener("pointercancel", up);
      rail.addEventListener("click", function (e) { if (Date.now() - dragged < 300) { e.preventDefault(); e.stopPropagation(); } }, true);

      if (!rail.hasAttribute("data-auto") || still) return;
      var kids = [].slice.call(rail.children);
      kids.forEach(function (k) {
        var c = k.cloneNode(true); c.setAttribute("aria-hidden", "true"); c.setAttribute("tabindex", "-1");
        c.querySelectorAll("a,button").forEach(function (a) { a.setAttribute("tabindex", "-1"); });
        rail.appendChild(c);
      });
      rail.classList.add("is-auto");
      var x = rail.scrollLeft, set = x, seen = false, hold = 0, raf = 0, resume = 0;
      var half = function () { return rail.scrollWidth / 2; };
      var go = function () {
        raf = 0;
        if (!seen || hold || down || d.hidden) return;   // down: being dragged
        if (Math.abs(rail.scrollLeft - set) > 2) x = rail.scrollLeft;   // the visitor moved it
        x += 0.45; if (x >= half()) x -= half();
        rail.scrollLeft = x; set = rail.scrollLeft;
        raf = requestAnimationFrame(go);
      };
      var wake = function () { if (!raf) raf = requestAnimationFrame(go); };
      var pause = function () { hold = 1; clearTimeout(resume); };
      var later = function () { clearTimeout(resume); resume = setTimeout(function () { hold = 0; x = rail.scrollLeft; wake(); }, 2500); };
      // hovering does not stop it; grabbing or pressing it does, and it drifts on again after
      rail.addEventListener("pointerdown", pause);
      w.addEventListener("pointerup", function () { if (hold) later(); });
      rail.addEventListener("touchstart", pause, { passive: true }); rail.addEventListener("touchend", later);
      rail.addEventListener("focusin", pause); rail.addEventListener("focusout", later);
      rail.addEventListener("wheel", function () { pause(); later(); }, { passive: true });
      // manual scrolling past the clones wraps too, so the strip never runs out
      rail.addEventListener("scroll", function () { if (hold && rail.scrollLeft >= half()) rail.scrollLeft -= half(); }, { passive: true });
      d.addEventListener("visibilitychange", wake);
      if ("IntersectionObserver" in w) new IntersectionObserver(function (en) { seen = en[0].isIntersecting; if (seen) wake(); }).observe(rail);
      else { seen = true; wake(); }
    });
    wind = makeWind();
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", ready); else ready();

  /* ------------------------------------------------------------- wind (5) */
  function makeWind() {
    var ctx = null, gain, filt, on = keep.get("v2-wind") === "on", btn = null, target = 0;
    function build() {
      var AC = w.AudioContext || w.webkitAudioContext; if (!AC) return false;
      ctx = new AC();
      var len = ctx.sampleRate * 4, buf = ctx.createBuffer(2, len, ctx.sampleRate);
      for (var c = 0; c < 2; c++) {             // brown noise: soft, low, like air moving
        var data = buf.getChannelData(c), last = 0;
        for (var i = 0; i < len; i++) { var white = Math.random() * 2 - 1; last = (last + 0.02 * white) / 1.02; data[i] = last * 3.2; }
      }
      var src = ctx.createBufferSource(); src.buffer = buf; src.loop = true;
      filt = ctx.createBiquadFilter(); filt.type = "lowpass"; filt.frequency.value = 420; filt.Q.value = 0.7;
      var lfo = ctx.createOscillator(), lfoGain = ctx.createGain();
      lfo.frequency.value = 0.07; lfoGain.gain.value = 180; lfo.connect(lfoGain); lfoGain.connect(filt.frequency);
      gain = ctx.createGain(); gain.gain.value = 0;
      src.connect(filt); filt.connect(gain); gain.connect(ctx.destination);
      src.start(); lfo.start();
      return true;
    }
    function level(v, t) { if (ctx) gain.gain.setTargetAtTime(v, ctx.currentTime, t || 0.8); }
    function start() {
      if (!ctx && !build()) return;
      if (ctx.state === "suspended") ctx.resume();
      target = 0.16; level(target, 1.2);
    }
    function stop() { target = 0; level(0, 0.4); }
    function set(v) {
      on = v; keep.set("v2-wind", v ? "on" : "off");
      if (btn) { btn.setAttribute("aria-pressed", String(v)); btn.classList.toggle("is-on", v); }
      if (v) start(); else stop();
    }
    function mount() {
      var nav = d.querySelector(".page-wrap > nav"), cta = nav && nav.querySelector(".nav-cta");
      if (!nav || !cta) return;
      btn = d.createElement("button");
      btn.type = "button"; btn.className = "v2-wind"; btn.setAttribute("aria-pressed", String(on));
      btn.setAttribute("aria-label", "Wind sound"); btn.title = "Wind sound";
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">' +
        '<path d="M3 9h11a3 3 0 1 0-3-3"/><path d="M3 14h15a3 3 0 1 1-3 3"/><path d="M3 19h7"/></svg>';
      btn.classList.toggle("is-on", on);
      btn.addEventListener("click", function () { set(!on); });
      nav.insertBefore(btn, cta);
      // remembered as on: a browser only lets sound start after the visitor
      // touches the page, so it waits for the first press or key
      if (on) {
        var first = function () { d.removeEventListener("pointerdown", first, true); d.removeEventListener("keydown", first, true); if (on) start(); };
        d.addEventListener("pointerdown", first, true); d.addEventListener("keydown", first, true);
      }
    }
    d.addEventListener("visibilitychange", function () {
      if (!ctx) return;
      if (d.hidden) level(0, 0.2); else if (on) level(target, 0.8);
    });
    w.addEventListener("pagehide", function () { if (ctx) level(0, 0.1); });
    mount();
    return {
      gust: function (g) {
        if (!ctx || !on || d.hidden) return;
        level(0.16 + g * 0.22, 0.25);
        filt.frequency.setTargetAtTime(420 + g * 900, ctx.currentTime, 0.3);
        clearTimeout(this._t);
        this._t = setTimeout(function () { level(0.16, 1.4); filt.frequency.setTargetAtTime(420, ctx.currentTime, 1.4); }, 180);
      }
    };
  }
})();

/* THE NAV COMES BACK ON THE WAY UP.
   Past the first screen the nav rides along out of sight; the moment the
   visitor scrolls up it slides down, pinned, on the page's own dark glass,
   and it goes again on the next scroll down. Back at the top it drops into its place in the page. Not on the trip
   pages: their jump bar (.dst-jump) already holds the top of the screen there.
   Scroll-driven only; no frame runs while the page is still. */
(function () {
  var d = document, w = window;
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
  function init() {
  var nav = d.querySelector(".page-wrap > nav");
  if (!nav || d.querySelector(".dst-jump")) return;
  var root = d.documentElement, spacer = null, pinned = false, shown = false, lastY = w.scrollY, queued = false;
  function threshold() {
    var hero = d.querySelector(".page-wrap > .kit-hero, .page-wrap > header");
    var h = hero ? hero.getBoundingClientRect().bottom + w.scrollY : 0;
    return Math.max(nav.offsetHeight * 3, Math.min(h, innerHeight));
  }
  function pin(on) {
    if (on === pinned) return;
    pinned = on;
    if (on) {
      if (getComputedStyle(nav).position === "relative" || getComputedStyle(nav).position === "static") {
        spacer = spacer || d.createElement("div");
        spacer.style.height = nav.offsetHeight + "px"; spacer.setAttribute("aria-hidden", "true");
        nav.parentNode.insertBefore(spacer, nav);
      }
      nav.classList.add("v2-nav-pinned");
      root.style.setProperty("--v2-nav-h", nav.offsetHeight + "px");
    } else {
      nav.classList.remove("v2-nav-pinned");
      if (spacer && spacer.parentNode) spacer.parentNode.removeChild(spacer);
    }
  }
  function show(on) {
    if (on === shown) return;
    shown = on;
    nav.classList.toggle("v2-nav-shown", on);
    root.classList.toggle("v2-nav-up", on);
  }
  function update() {
    queued = false;
    var y = w.scrollY, dy = y - lastY; lastY = y;
    if (nav.classList.contains("is-open")) return;          // the phone menu is open
    if (y <= 2) { show(false); pin(false); return; }
    if (!pinned) { if (y > threshold()) pin(true); else return; }
    if (dy < -4) show(true);
    else if (dy > 4) show(false);
  }
  w.addEventListener("scroll", function () {
    if (queued) return; queued = true; requestAnimationFrame(update);
  }, { passive: true });
  // a click inside the nav (a link, the menu) keeps it where it is
  nav.addEventListener("focusin", function () { if (pinned) show(true); });
  }
})();

/* IMAGES ARRIVE SOFTLY. A lazy image that has not loaded yet is marked, and
   fades up out of a blur when it lands (v2.css .v2-img-wait / .v2-img-in).
   Images that are already there are left alone; one listener per image, and
   nothing runs once they have all arrived. Rails are built at run time, so
   images added later are picked up too. */
(function () {
  var d = document;
  function mark(img) {
    if (img.complete || img.dataset.v2Soft) return;
    img.dataset.v2Soft = "1";
    img.classList.add("v2-img-wait");
    function done() {
      img.classList.add("v2-img-in");
      requestAnimationFrame(function () { img.classList.remove("v2-img-wait"); });
    }
    img.addEventListener("load", done, { once: true });
    img.addEventListener("error", done, { once: true });
  }
  function scan(root) { (root.querySelectorAll ? root : d).querySelectorAll('img[loading="lazy"]').forEach(mark); }
  function init() {
    scan(d);
    if ("MutationObserver" in window) new MutationObserver(function (list) {
      list.forEach(function (m) { m.addedNodes.forEach(function (n) {
        if (n.nodeType !== 1) return;
        if (n.tagName === "IMG" && n.loading === "lazy") mark(n); else scan(n);
      }); });
    }).observe(d.body, { childList: true, subtree: true });
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();

/* EPISODE TIMELINE (the v2 episode page). A tick plays from its chapter by
   handing the tap to that chapter's own timestamp, which episode-sync.js has
   already made a control; and the ticks follow the chapter rail, which the
   sync keeps on the chapter being played. Nothing runs until one of them moves. */
(function () {
  var d = document;
  function init() {
    var ticks = [].slice.call(d.querySelectorAll(".ep2-tick"));
    if (!ticks.length) return;
    ticks.forEach(function (t) {
      t.addEventListener("click", function (ev) {
        var bt = d.querySelector("#c" + t.dataset.c + " .cd-block-time");
        if (bt) { ev.preventDefault(); bt.click(); }
      });
    });
    var chaps = [].slice.call(d.querySelectorAll(".cd-rail .cd-chap"));
    function follow() {
      var on = chaps.findIndex(function (c) { return c.classList.contains("active"); });
      ticks.forEach(function (t, k) { t.classList.toggle("is-on", k === on); t.classList.toggle("is-done", k < on); });
    }
    follow();
    if ("MutationObserver" in window && chaps.length) {
      var mo = new MutationObserver(follow);
      chaps.forEach(function (c) { mo.observe(c, { attributes: true, attributeFilter: ["class"] }); });
    }
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();

/* THE CONTOURS CARRY THE SCROLL. Two of the lines in the survey-map backdrop
   (.v2-topo, the enquire page) get an orange glow that travels down them as
   the section scrolls through the screen: bright at its head, fading behind.
   The paths come from tools/v2_art.py (the same drawing as img/contours.svg)
   and sit exactly over it. The movement is CSS scroll-driven (v2.css,
   .v2-trail), so nothing runs while the page is still; without support, or
   with reduced motion, there is no glow and the backdrop is as it was. */
(function () {
  var TRAILS = [/*v2-trails*/"M746 0 Q756 1 762 2 Q768 2 774 3 Q780 3 786 4 Q792 4 798 5 Q804 5 810 6 Q816 6 822 7 Q828 8 834 9 Q840 10 845 11 Q850 12 851 12 Q852 12 858 14 Q864 16 870 18 Q876 20 881 22 Q886 24 887 24 Q888 25 894 28 Q900 31 904 34 Q907 36 910 38 Q912 40 917 44 Q922 48 923 49 Q924 50 928 55 Q933 60 934 62 Q936 64 939 68 Q941 72 944 78 Q947 84 948 85 Q948 86 950 91 Q951 96 953 102 Q954 108 955 114 Q956 120 956 126 Q956 132 956 138 Q956 144 956 150 Q955 156 955 162 Q954 168 953 174 Q953 180 952 186 Q951 192 950 198 Q949 204 949 208 Q948 212 948 214 Q947 216 947 222 Q946 228 945 234 Q944 240 944 246 Q943 252 943 258 Q942 264 942 270 Q942 276 941 282 Q941 288 941 294 Q940 300 940 306 Q939 312 939 318 Q938 324 937 329 Q936 334 936 335 Q936 336 933 342 Q930 348 927 352 Q924 356 922 358 Q919 360 916 362 Q912 364 906 366 Q900 367 894 368 Q888 368 882 368 Q876 368 870 368 Q864 368 858 367 Q852 367 846 366 Q840 366 834 365 Q828 365 822 365 Q816 364 810 364 Q804 364 798 364 Q792 363 786 364 Q780 364 774 364 Q768 364 762 365 Q756 365 750 366 Q744 366 738 367 Q732 368 726 369 Q720 370 715 371 Q710 372 709 372 Q708 372 702 374 Q696 375 690 377 Q684 379 678 381 Q672 382 670 383 Q668 384 664 385 Q660 387 654 389 Q648 392 644 394 Q639 396 638 397 Q636 398 630 401 Q624 405 622 406 Q619 408 616 411 Q612 414 609 417 Q605 420 603 423 Q600 426 598 429 Q595 432 592 438 Q589 444 589 446 Q588 448 587 452 Q586 456 586 462 Q585 468 586 474 Q587 480 588 481 Q588 482 590 487 Q592 492 595 498 Q598 504 599 505 Q600 507 604 511 Q607 516 610 518 Q612 521 616 524 Q620 528 622 530 Q624 531 630 535 Q636 540 636 540 Q637 540 642 543 Q648 546 653 549 Q659 552 659 552 Q660 553 666 555 Q672 558 678 560 Q684 563 686 563 Q687 564 692 566 Q696 567 702 569 Q708 572 714 574 Q720 576 720 576 Q720 576 726 578 Q732 580 738 582 Q744 585 749 586 Q753 588 755 589 Q756 589 762 591 Q768 594 774 596 Q780 599 781 599 Q783 600 787 602 Q792 604 798 607 Q804 610 806 611 Q808 612 812 614 Q816 616 822 619 Q828 622 830 623 Q831 624 836 626 Q840 629 846 632 Q852 636 852 636 Q852 636 858 639 Q864 643 868 645 Q873 648 874 649 Q876 650 882 653 Q888 657 891 658 Q894 660 897 662 Q900 664 906 667 Q912 670 913 671 Q915 672 919 675 Q924 677 930 680 Q936 684 936 684 Q937 684 942 687 Q948 690 954 693 Q960 696 960 696 Q960 696 966 699 Q972 702 978 705 Q983 708 984 708 Q984 708 990 711 Q996 714 1001 717 Q1006 720 1007 720 Q1008 721 1014 724 Q1020 727 1024 730 Q1028 732 1030 733 Q1032 735 1038 738 Q1044 742 1045 743 Q1047 744 1051 747 Q1056 751 1059 753 Q1063 756 1065 758 Q1068 761 1072 764 Q1076 768 1078 770 Q1080 773 1083 776 Q1086 780 1089 784 Q1092 787 1094 790 Q1095 792 1099 798 Q1102 804 1103 806 Q1104 807 1106 812 Q1108 816 1110 822 Q1113 828 1114 833 Q1116 838 1116 839 Q1117 840 1118 846 Q1120 852 1121 858 Q1122 864 1123 870 Q1124 876 1125 882 Q1125 888 1126 894 Q1127 900 1127 906 Q1127 912 1128 918 Q1128 924 1128 926 Q1128 928 1128 932 Q1128 936 1128 942 Q1128 948 1129 954 Q1129 960 1129 966 Q1129 972 1129 978 Q1129 984 1129 990 L1129 996","M1596 376 Q1584 374 1579 373 Q1574 372 1573 372 Q1572 372 1566 370 Q1560 368 1554 366 Q1548 363 1545 362 Q1541 360 1539 359 Q1536 357 1530 354 Q1524 351 1522 349 Q1520 348 1516 346 Q1512 344 1506 340 Q1500 336 1500 336 Q1500 336 1494 332 Q1488 328 1485 326 Q1482 324 1479 322 Q1476 320 1470 316 Q1464 312 1464 312 Q1464 312 1458 308 Q1452 304 1449 302 Q1446 300 1443 298 Q1440 296 1434 292 Q1428 288 1428 288 Q1428 288 1422 284 Q1416 280 1412 278 Q1409 276 1406 274 Q1404 273 1398 269 Q1392 265 1391 265 Q1390 264 1385 261 Q1380 258 1375 255 Q1370 252 1369 251 Q1368 251 1362 247 Q1356 243 1353 242 Q1351 240 1347 238 Q1344 236 1338 232 Q1332 228 1332 228 Q1332 228 1326 224 Q1320 220 1317 218 Q1313 216 1311 214 Q1308 212 1302 208 Q1296 204 1296 204 Q1296 204 1290 200 Q1284 196 1281 194 Q1279 192 1275 189 Q1272 187 1267 183 Q1263 180 1261 179 Q1260 178 1254 173 Q1248 168 1248 168 Q1248 168 1242 163 Q1236 159 1234 157 Q1232 156 1228 152 Q1224 149 1221 146 Q1218 144 1215 141 Q1212 139 1207 135 Q1202 132 1201 131 Q1200 130 1194 127 Q1188 123 1182 123 Q1176 123 1171 127 Q1166 132 1165 133 Q1164 133 1161 139 Q1158 144 1155 149 Q1152 153 1151 155 Q1151 156 1148 162 Q1145 168 1143 174 Q1140 180 1140 180 Q1140 181 1138 186 Q1137 192 1135 198 Q1133 204 1132 210 Q1131 216 1130 222 Q1129 228 1129 234 Q1129 240 1129 246 Q1129 252 1129 258 Q1129 264 1130 270 Q1130 276 1131 282 Q1132 288 1133 294 Q1134 300 1135 306 Q1136 312 1137 318 Q1138 324 1139 330 Q1140 336 1140 337 Q1140 337 1141 343 Q1142 348 1143 354 Q1144 360 1145 366 Q1146 372 1146 378 Q1147 384 1148 390 Q1149 396 1149 402 Q1150 408 1151 414 Q1151 420 1152 425 Q1152 429 1152 431 Q1152 432 1153 438 Q1153 444 1153 450 Q1154 456 1154 462 Q1154 468 1154 474 Q1154 480 1155 486 Q1155 492 1155 498 Q1155 504 1155 510 Q1155 516 1156 522 Q1156 528 1157 534 Q1158 540 1160 546 Q1161 552 1163 555 Q1164 557 1166 561 Q1168 564 1172 568 Q1176 572 1178 574 Q1180 576 1184 579 Q1188 582 1192 585 Q1197 588 1198 589 Q1200 590 1206 595 Q1212 599 1213 600 Q1213 600 1219 605 Q1224 611 1225 611 Q1225 612 1228 618 Q1232 624 1234 630 Q1235 636 1236 640 Q1236 643 1236 646 Q1236 648 1236 654 Q1236 660 1236 665 Q1236 670 1236 671 Q1236 672 1236 678 Q1235 684 1235 690 Q1235 696 1235 702 Q1234 708 1234 714 Q1234 720 1234 726 Q1235 732 1235 738 Q1235 744 1235 750 Q1236 756 1236 757 Q1236 757 1236 763 Q1237 768 1238 774 Q1238 780 1239 786 Q1240 792 1241 798 Q1242 804 1244 810 Q1245 816 1246 822 Q1248 828 1248 829 Q1248 829 1249 835 Q1251 840 1253 846 Q1254 852 1256 858 Q1258 864 1259 867 Q1260 869 1261 873 Q1262 876 1265 882 Q1267 888 1269 894 Q1271 900 1272 901 Q1272 903 1274 907 Q1275 912 1277 918 Q1279 924 1281 930 Q1282 936 1283 942 Q1284 948 1284 954 Q1284 960 1283 966 Q1283 972 1282 978 Q1280 984 1279 990 L1277 996"/*/v2-trails*/];
  var d = document, NS = "http://www.w3.org/2000/svg";
  function init() {
    if (!TRAILS.length) return;
    if (!(window.CSS && CSS.supports && CSS.supports("animation-timeline: view()"))) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    d.querySelectorAll(".v2-topo, .enq-wrap").forEach(function (sec) {
      var svg = d.createElementNS(NS, "svg");
      svg.setAttribute("class", "v2-trails");
      svg.setAttribute("viewBox", "0 0 1600 1000");
      svg.setAttribute("aria-hidden", "true");
      TRAILS.forEach(function (p, k) {
        ["v2-trail-tail", "v2-trail"].forEach(function (cls) {   // tail first, head over it
          var path = d.createElementNS(NS, "path");
          path.setAttribute("d", p);
          path.setAttribute("pathLength", "1");
          path.setAttribute("class", cls + " v2-trail-" + k);
          svg.appendChild(path);
        });
      });
      sec.appendChild(svg);
    });
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();
