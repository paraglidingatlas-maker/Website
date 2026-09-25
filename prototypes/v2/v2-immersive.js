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
    var CARDS = ".kit-card, .kit-panel, .ep-card, .ep-tile, .tg-v2 .tg-ep, .v2-door, .tile, .cd-box";
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
   visitor scrolls up it slides down, pinned, on a dark glass with the sky's
   cool light in its top-right corner, and it goes again on the next scroll
   down. Back at the top it drops into its place in the page. Not on the trip
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
