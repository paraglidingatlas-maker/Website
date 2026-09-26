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

/* THE CONTOURS CARRY THE SCROLL. In the survey-map backdrop (.v2-topo, the
   enquire page) a few lines light up in the site's orange as the section
   scrolls: each section draws three lines at random from a pool, and each
   glow starts at a random point, travels a random stretch of its line, and
   fades in and out on its own part of the scroll, so they seem to come from
   anywhere. The paths come from tools/v2_art.py (the same drawing as
   img/contours.svg) and sit exactly over it. The movement is CSS
   scroll-driven (v2.css, .v2-trail), so nothing runs while the page is still;
   without support, or with reduced motion, the backdrop is as it was. */
(function () {
  var TRAILS = [/*v2-trails*/"M516 0 Q552 10 564 13 Q576 17 588 21 Q600 24 618 30 Q635 36 648 40 Q660 44 672 48 Q684 52 696 56 Q708 60 725 66 Q741 72 755 77 Q768 83 780 89 Q792 95 801 102 Q809 108 819 120 Q828 132 831 144 Q835 156 834 174 Q833 192 830 204 Q826 216 819 228 Q813 240 802 252 Q792 263 784 270 Q776 276 766 282 Q756 288 744 294 Q732 300 718 306 Q705 312 690 318 Q675 324 661 329 Q648 334 636 339 Q624 344 612 349 Q600 354 588 359 Q576 365 564 372 Q552 379 541 387 Q530 396 523 405 Q516 415 511 429 Q506 444 505 456 Q504 468 505 480 Q506 492 511 510 Q515 528 520 540 Q525 552 530 564 Q536 576 544 588 Q551 600 558 607 Q564 615 576 623 Q588 631 600 635 Q612 638 630 642 Q648 646 660 648 Q672 651 690 655 Q707 660 720 664 Q732 668 744 673 Q756 677 768 683 Q780 688 792 694 Q804 700 816 706 Q828 712 840 719 Q852 726 864 732 Q876 739 888 746 Q900 753 912 761 Q924 768 933 774 Q942 780 951 787 Q960 795 970 805 Q980 816 987 828 Q994 840 997 852 Q1000 864 998 882 Q996 900 990 912 Q984 924 978 930 Q972 936 954 940 Q936 945 919 940 Q902 936 889 931 Q876 925 864 920 Q852 915 840 909 Q828 903 816 897 Q804 892 792 885 Q780 879 768 872 Q756 866 745 859 Q734 852 725 846 Q717 840 706 832 Q696 823 686 814 Q675 804 668 796 Q660 788 651 778 Q643 768 633 756 Q624 745 618 737 Q612 729 604 718 Q596 708 586 697 Q576 685 569 679 Q561 672 549 666 Q537 660 521 657 Q504 654 486 653 Q468 652 450 653 Q432 653 414 653 Q396 654 378 654 Q360 655 342 655 Q324 655 306 655 Q288 655 270 653 Q252 652 237 650 Q223 648 207 644 Q192 641 180 637 Q168 633 156 627 Q144 622 132 614 Q120 607 108 598 Q96 589 89 582 Q82 576 71 564 Q60 553 54 545 Q48 538 41 527 Q33 516 27 504 Q20 492 15 480 Q10 468 6 450 Q1 432 1 428 L0 423","M396 23 Q372 36 366 44 Q360 51 356 68 Q352 84 352 102 Q352 120 353 138 Q353 156 353 174 Q353 192 351 210 Q349 228 345 240 Q341 252 334 264 Q327 276 319 282 Q312 289 300 294 Q288 300 270 304 Q252 309 240 310 Q228 312 210 313 Q192 315 174 316 Q156 317 138 319 Q120 320 108 323 Q96 325 81 330 Q66 336 57 342 Q48 348 38 360 Q29 372 25 384 Q21 396 21 414 Q20 432 23 444 Q25 456 30 471 Q36 486 42 497 Q48 509 55 518 Q61 528 72 540 Q82 552 89 559 Q96 565 108 575 Q120 584 132 592 Q144 599 156 605 Q168 611 180 616 Q192 620 204 623 Q216 626 234 629 Q252 633 270 634 Q288 635 306 636 Q324 636 342 635 Q360 634 378 632 Q396 631 414 628 Q432 624 444 621 Q456 617 468 610 Q480 602 485 589 Q490 576 489 558 Q488 540 486 522 Q483 504 482 488 Q480 472 480 462 Q480 452 483 436 Q486 420 492 408 Q498 396 507 387 Q516 379 528 371 Q540 364 552 358 Q564 352 576 347 Q588 342 600 337 Q612 332 624 327 Q636 322 649 317 Q661 312 675 306 Q688 300 700 294 Q712 288 722 282 Q732 276 744 267 Q756 258 765 249 Q773 240 781 228 Q788 216 792 204 Q795 192 795 174 Q794 156 788 144 Q782 132 775 125 Q768 118 756 109 Q744 101 732 94 Q720 88 708 82 Q696 77 684 72 Q672 67 660 63 Q648 58 633 53 Q618 48 603 43 Q588 38 576 35 Q564 32 548 28 Q531 24 518 21 Q504 19 486 17 Q468 15 450 16 Q432 16 414 19 L396 23","M444 45 Q420 55 410 64 Q401 72 394 84 Q387 96 384 108 Q381 120 379 138 Q376 156 375 174 Q374 192 373 207 Q372 222 370 237 Q368 252 364 264 Q360 277 351 288 Q343 300 333 306 Q323 312 306 317 Q288 322 276 324 Q264 326 246 328 Q228 330 210 331 Q192 332 174 334 Q156 335 144 337 Q132 338 114 343 Q96 348 85 354 Q73 360 66 366 Q60 372 52 384 Q45 396 43 414 Q40 432 44 450 Q47 468 53 480 Q58 492 65 503 Q72 514 78 522 Q84 530 95 541 Q107 552 114 558 Q122 564 133 571 Q144 579 156 585 Q168 591 180 596 Q192 600 210 605 Q228 610 240 612 Q252 614 270 615 Q288 617 306 617 Q324 616 342 615 Q360 613 372 611 Q384 609 398 604 Q412 600 423 594 Q433 588 443 576 Q452 564 455 552 Q457 540 457 522 Q458 504 457 490 Q456 476 456 460 Q455 444 457 432 Q458 420 463 406 Q468 391 476 382 Q485 372 494 366 Q504 359 516 354 Q528 348 543 342 Q559 336 573 331 Q588 325 600 320 Q612 316 624 311 Q636 306 648 300 Q660 295 672 289 Q684 282 696 275 Q708 267 717 259 Q726 252 735 242 Q744 232 750 220 Q756 209 759 195 Q761 180 758 168 Q756 156 748 144 Q740 132 730 123 Q720 115 708 107 Q696 99 684 93 Q672 87 660 82 Q648 77 636 72 Q624 67 612 63 Q600 59 582 54 Q564 49 552 47 Q540 44 522 42 Q504 40 486 40 Q468 41 456 43 L444 45","M456 70 Q432 84 426 91 Q420 97 414 109 Q408 120 403 138 Q398 156 397 168 Q396 180 395 198 Q394 216 393 234 Q393 252 392 270 Q391 288 387 300 Q384 312 372 322 Q360 331 348 334 Q336 338 318 340 Q300 342 282 344 Q264 345 246 346 Q228 347 216 348 Q204 348 186 350 Q168 352 150 355 Q132 358 120 362 Q108 367 96 374 Q84 382 78 389 Q72 397 67 414 Q62 432 65 450 Q67 468 73 480 Q78 492 87 504 Q95 516 102 523 Q108 530 120 540 Q132 550 143 557 Q154 564 166 570 Q178 576 191 581 Q204 585 216 589 Q228 592 246 594 Q264 597 282 597 Q300 598 318 597 Q336 595 352 592 Q368 588 382 582 Q395 576 403 570 Q411 564 418 552 Q425 540 428 522 Q431 504 431 486 Q431 468 430 450 Q429 432 429 414 Q429 396 431 384 Q434 372 445 362 Q456 351 468 347 Q480 342 492 338 Q504 335 522 329 Q540 324 552 321 Q564 317 576 313 Q588 309 600 304 Q612 299 625 294 Q637 288 649 282 Q660 276 672 268 Q684 260 695 250 Q706 240 713 230 Q720 219 724 206 Q729 192 725 174 Q721 156 715 147 Q708 137 698 129 Q689 120 680 114 Q671 108 660 102 Q648 96 635 90 Q621 84 605 78 Q588 73 576 70 Q564 67 546 64 Q528 61 510 61 Q492 61 474 65 L456 70","M746 0 Q780 3 798 5 Q816 6 833 9 Q850 12 863 16 Q876 20 888 26 Q900 31 911 40 Q922 48 929 56 Q936 64 942 75 Q948 86 952 103 Q956 120 956 138 Q955 156 953 174 Q951 192 949 204 Q947 216 945 234 Q943 252 942 270 Q941 288 939 306 Q938 324 934 336 Q930 348 921 356 Q912 364 894 366 Q876 368 858 367 Q840 366 822 365 Q804 364 786 364 Q768 364 750 366 Q732 368 720 370 Q708 372 690 377 Q672 382 660 387 Q648 392 636 398 Q624 405 615 412 Q605 420 597 432 Q589 444 587 456 Q585 468 589 480 Q592 492 599 504 Q607 516 616 524 Q624 531 636 539 Q648 546 660 552 Q672 558 684 563 Q696 567 708 572 Q720 576 737 582 Q753 588 767 593 Q780 599 792 604 Q804 610 816 616 Q828 622 840 629 Q852 636 862 642 Q873 648 883 654 Q894 660 904 666 Q915 672 926 678 Q937 684 948 690 Q960 696 972 702 Q984 708 996 715 Q1008 721 1020 728 Q1032 735 1044 743 Q1056 751 1066 759 Q1076 768 1084 778 Q1092 787 1098 797 Q1104 807 1110 823 Q1116 838 1119 851 Q1122 864 1124 882 Q1127 900 1127 914 Q1128 928 1128 944 Q1129 960 1129 978 L1129 996","M972 0 Q996 24 1002 32 Q1008 40 1014 50 Q1020 60 1026 78 Q1032 96 1033 108 Q1034 120 1033 138 Q1033 156 1031 168 Q1030 180 1029 198 Q1028 216 1029 234 Q1030 252 1033 264 Q1035 276 1040 291 Q1044 305 1049 321 Q1054 336 1057 348 Q1060 360 1061 378 Q1063 396 1059 413 Q1056 431 1050 442 Q1044 452 1036 460 Q1029 468 1018 475 Q1008 482 996 487 Q984 492 966 497 Q948 502 936 504 Q924 506 906 507 Q888 508 875 506 Q861 504 850 498 Q839 492 828 482 Q816 473 806 464 Q795 456 784 450 Q773 444 759 440 Q744 436 726 438 Q708 439 696 447 Q684 454 684 466 Q684 477 691 485 Q698 492 710 498 Q723 504 739 508 Q756 513 768 515 Q780 517 798 520 Q816 522 828 526 Q840 529 852 537 Q864 546 873 555 Q882 564 891 573 Q900 582 910 591 Q919 600 928 607 Q936 613 948 622 Q960 630 972 637 Q984 645 996 651 Q1008 657 1020 663 Q1032 669 1044 674 Q1056 680 1068 686 Q1080 692 1092 699 Q1104 706 1113 713 Q1122 720 1131 729 Q1140 739 1146 748 Q1152 756 1158 769 Q1164 781 1170 799 Q1176 816 1179 828 Q1182 840 1185 855 Q1188 871 1190 885 Q1193 900 1195 918 Q1197 936 1197 954 Q1198 972 1198 984 L1197 996","M642 0 Q672 9 684 12 Q696 15 714 19 Q732 22 744 24 Q756 26 774 29 Q792 32 804 34 Q816 37 834 42 Q852 47 864 54 Q876 60 883 66 Q891 72 899 84 Q908 96 912 108 Q915 120 916 138 Q917 156 915 174 Q912 192 910 204 Q907 216 904 230 Q900 243 894 259 Q888 274 882 283 Q876 293 864 302 Q853 312 840 317 Q828 322 816 325 Q804 329 787 332 Q771 336 757 339 Q744 342 731 345 Q718 348 701 353 Q684 358 672 362 Q660 366 648 371 Q636 375 624 381 Q612 387 600 395 Q588 403 580 412 Q571 420 565 432 Q559 444 558 462 Q557 480 561 492 Q565 504 572 516 Q580 528 590 538 Q600 548 612 556 Q623 564 635 570 Q647 576 659 581 Q672 586 684 591 Q696 595 708 599 Q720 603 732 608 Q744 612 758 618 Q772 624 785 630 Q797 636 809 642 Q821 648 832 654 Q843 660 853 666 Q864 672 876 679 Q888 685 900 692 Q912 698 924 705 Q936 711 948 718 Q960 724 972 731 Q984 737 996 745 Q1008 752 1019 760 Q1031 768 1037 774 Q1044 780 1054 792 Q1064 804 1071 816 Q1077 828 1081 840 Q1085 852 1088 870 Q1091 888 1091 900 Q1092 912 1092 924 Q1092 936 1091 954 Q1091 972 1090 984 L1090 996","M914 0 Q936 14 948 25 Q960 35 966 43 Q972 51 978 62 Q984 73 989 90 Q993 108 994 126 Q994 144 992 162 Q991 180 989 198 Q987 216 987 234 Q987 252 990 270 Q992 288 995 300 Q998 312 1003 330 Q1007 348 1009 360 Q1010 372 1008 384 Q1007 396 1000 408 Q993 420 983 427 Q972 435 954 439 Q936 443 918 441 Q900 438 888 435 Q876 431 863 425 Q851 420 836 414 Q821 408 807 404 Q792 399 780 397 Q768 396 750 395 Q732 395 720 397 Q708 398 691 403 Q674 408 662 414 Q650 420 643 426 Q636 432 629 444 Q623 456 624 468 Q625 480 633 492 Q641 504 650 511 Q660 519 672 525 Q684 532 696 537 Q708 542 723 547 Q739 552 753 557 Q768 562 780 566 Q792 571 804 576 Q816 581 828 588 Q840 594 852 601 Q864 609 876 616 Q888 624 897 630 Q907 636 917 642 Q926 648 937 654 Q948 660 960 667 Q972 673 984 679 Q996 685 1008 691 Q1020 697 1032 703 Q1044 709 1056 716 Q1068 723 1080 732 Q1092 740 1100 748 Q1108 756 1117 768 Q1126 780 1132 792 Q1138 804 1142 816 Q1146 828 1149 840 Q1152 852 1155 870 Q1158 888 1160 906 Q1162 924 1162 942 Q1163 960 1163 978 L1163 996","M583 0 Q612 10 624 14 Q636 18 648 21 Q660 25 678 31 Q696 36 708 39 Q720 42 732 45 Q744 48 762 53 Q780 58 792 62 Q804 65 816 71 Q828 76 840 84 Q852 93 858 100 Q864 108 870 125 Q876 142 876 155 Q877 168 875 180 Q873 192 869 207 Q864 223 858 235 Q852 247 846 256 Q840 264 828 275 Q816 286 804 292 Q792 299 780 304 Q768 310 756 314 Q744 318 732 322 Q720 326 706 331 Q692 336 676 342 Q660 347 648 352 Q636 356 624 361 Q612 367 600 373 Q588 379 576 387 Q564 395 557 401 Q550 408 543 420 Q535 432 532 450 Q529 468 532 486 Q536 504 541 516 Q546 528 554 540 Q562 552 569 559 Q576 567 588 576 Q600 585 612 591 Q624 598 636 602 Q648 607 660 611 Q672 616 685 620 Q698 624 715 630 Q732 636 744 641 Q756 646 768 651 Q780 656 792 662 Q804 668 816 674 Q828 681 840 687 Q852 694 864 700 Q876 707 888 714 Q899 720 910 726 Q921 732 932 738 Q942 744 953 750 Q963 756 973 763 Q984 770 996 780 Q1008 790 1015 797 Q1022 804 1029 816 Q1037 828 1042 840 Q1047 852 1049 870 Q1052 888 1051 906 Q1050 924 1047 942 Q1045 960 1043 972 Q1041 984 1040 990 L1039 996","M1596 424 Q1560 422 1548 419 Q1536 415 1524 409 Q1512 402 1501 393 Q1490 384 1483 378 Q1476 371 1464 360 Q1452 350 1444 343 Q1435 336 1426 329 Q1416 322 1404 314 Q1392 306 1380 299 Q1368 291 1356 285 Q1344 279 1332 273 Q1320 268 1308 263 Q1296 258 1284 255 Q1272 251 1254 250 Q1236 248 1224 253 Q1212 258 1205 267 Q1198 276 1194 294 Q1189 312 1188 324 Q1188 336 1188 348 Q1189 360 1191 378 Q1193 396 1197 411 Q1200 426 1205 441 Q1211 456 1217 467 Q1224 479 1230 485 Q1236 492 1248 501 Q1260 510 1272 516 Q1284 522 1296 527 Q1308 533 1320 540 Q1332 546 1340 555 Q1349 564 1349 582 Q1350 600 1344 612 Q1339 624 1332 636 Q1324 648 1316 660 Q1309 672 1302 683 Q1296 694 1291 707 Q1285 720 1283 732 Q1280 744 1279 762 Q1278 780 1281 798 Q1284 816 1288 828 Q1292 840 1299 852 Q1305 864 1313 874 Q1320 884 1328 892 Q1336 900 1346 908 Q1356 916 1368 922 Q1380 928 1398 929 Q1416 930 1428 927 Q1440 924 1458 919 Q1476 915 1488 912 Q1500 910 1518 908 Q1536 905 1554 906 Q1572 906 1584 910 L1596 914","M1596 376 Q1572 372 1557 366 Q1541 360 1531 354 Q1520 348 1510 342 Q1500 336 1488 328 Q1476 320 1464 312 Q1452 304 1440 296 Q1428 288 1418 282 Q1409 276 1399 270 Q1390 264 1379 257 Q1368 251 1356 243 Q1344 236 1332 228 Q1320 220 1308 212 Q1296 204 1287 198 Q1279 192 1269 185 Q1260 178 1248 168 Q1236 159 1227 151 Q1218 144 1209 137 Q1200 130 1183 131 Q1166 132 1159 143 Q1152 153 1146 167 Q1140 180 1137 192 Q1133 204 1131 222 Q1129 240 1130 258 Q1130 276 1133 294 Q1136 312 1138 325 Q1140 337 1143 355 Q1146 372 1148 390 Q1150 408 1151 420 Q1152 432 1153 450 Q1154 468 1155 486 Q1155 504 1156 522 Q1158 540 1163 552 Q1168 564 1178 573 Q1188 582 1200 591 Q1212 599 1219 606 Q1225 612 1231 628 Q1236 643 1236 657 Q1236 670 1235 683 Q1235 696 1235 714 Q1235 732 1235 745 Q1236 757 1238 775 Q1240 792 1244 810 Q1248 828 1251 840 Q1254 852 1258 864 Q1262 876 1267 889 Q1272 903 1277 919 Q1282 936 1282 954 Q1283 972 1280 984 L1277 996","M1022 0 Q1043 24 1050 33 Q1056 42 1062 53 Q1068 64 1073 80 Q1078 96 1079 108 Q1080 120 1080 132 Q1079 144 1077 162 Q1076 180 1074 198 Q1073 216 1074 234 Q1076 252 1078 264 Q1081 276 1086 294 Q1090 312 1094 324 Q1097 336 1100 353 Q1104 370 1106 383 Q1107 396 1107 414 Q1106 432 1104 444 Q1101 456 1096 468 Q1091 480 1082 492 Q1073 504 1064 511 Q1056 519 1044 528 Q1032 536 1022 544 Q1011 552 1005 564 Q998 576 1003 588 Q1008 600 1020 610 Q1032 619 1044 626 Q1056 633 1068 639 Q1080 645 1092 650 Q1104 655 1116 662 Q1128 668 1140 676 Q1152 684 1158 690 Q1164 696 1172 708 Q1180 720 1185 732 Q1190 744 1195 761 Q1200 777 1203 791 Q1207 804 1209 816 Q1212 828 1216 846 Q1221 864 1223 876 Q1226 888 1230 906 Q1233 924 1235 941 Q1236 957 1236 965 Q1236 972 1235 984 L1234 996"/*/v2-trails*/];
  var d = document, NS = "http://www.w3.org/2000/svg";
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function init() {
    if (!TRAILS.length) return;
    if (!(window.CSS && CSS.supports && CSS.supports("animation-timeline: view()"))) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    d.querySelectorAll(".v2-topo, .enq-wrap").forEach(function (sec) {
      var svg = d.createElementNS(NS, "svg");
      svg.setAttribute("class", "v2-trails");
      svg.setAttribute("viewBox", "0 0 1600 1000");
      svg.setAttribute("aria-hidden", "true");
      var pool = TRAILS.slice();
      for (var k = 0; k < 3 && pool.length; k++) {
        var p = pool.splice(Math.floor(Math.random() * pool.length), 1)[0];
        var r0 = rnd(0, 35), style = "--o:" + rnd(0, .65).toFixed(3) + ";--t:" + rnd(.22, .38).toFixed(3) +
          ";--r0:" + r0.toFixed(0) + "%;--r1:" + (r0 + rnd(45, 65)).toFixed(0) + "%";
        ["v2-trail-tail", "v2-trail"].forEach(function (cls) {   // tail first, head over it
          var path = d.createElementNS(NS, "path");
          path.setAttribute("d", p);
          path.setAttribute("pathLength", "1");
          path.setAttribute("class", cls);
          path.setAttribute("style", style);
          svg.appendChild(path);
        });
      }
      sec.appendChild(svg);
    });
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();
