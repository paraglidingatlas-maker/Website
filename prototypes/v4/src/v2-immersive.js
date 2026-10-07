/* V2 IMMERSION (prototypes/v4/ only). One flight across the whole site.

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
    var m = /\/prototypes\/v\d+\/(.*)$/.exec(path) || [null, path.replace(/^\//, "")];
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
      var block = a.closest(".v2-flyby");
      var img = block && block.querySelector(".v2-fb-shot.is-on img");
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
      d.querySelectorAll(".v2-fb-shot img").forEach(function (i) { i.style.viewTransitionName = ""; });
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
    // v4, the award pass (owner, 4 Oct): no instrument in the header; the bar
    // holds the name, the four places, search and Enquire, nothing else
    var slot = null;
    if (slot) {
      hud = slot;
      slot.classList.add("v2-hud");
      slot.setAttribute("aria-hidden", "true");
      slot.innerHTML = '<span class="v2-hud-att"><i></i></span><span class="v2-hud-row"><b>ALT</b><em class="a"></em></span>' +
                       '<span class="v2-hud-row"><b>HDG</b><em class="h"></em></span>';
      hudAlt = slot.querySelector(".a"); hudHdg = slot.querySelector(".h"); hudLine = slot.querySelector(".v2-hud-att i");
    }
    function pad3(n) { n = ((Math.round(n) % 360) + 360) % 360; return (n < 10 ? "00" : n < 100 ? "0" : "") + n; }
    /* The numbers fly with the hero's footage, not with the scroll: while the
       page's hero video plays, altitude climbs through its loop (the homepage
       clip climbs through cloud and breaks out above the peaks) and heading
       drifts like a slow turn; both start again with the loop. The readout is
       shown only while that footage is moving behind it (v2.css .is-flying):
       not on the nav that returns on the way up, not on pages without a hero
       video. (Decorative instrument numbers; not telemetry from the flight.) */
    function paintHud(f) {
      if (!hud) return;
      f = f || 0;                                   // 0..1 through the loop
      var climb = BASE - 450 + f * 700;             // a climb of 700 m over the clip
      var turn = HDG + Math.sin(f * Math.PI * 2) * 9 + f * 14;
      hudAlt.textContent = (Math.round(climb / 10) * 10).toLocaleString("en-US") + " m";
      hudHdg.textContent = pad3(turn) + "°";
    }
    var heroVid = d.querySelector(".page-wrap > .kit-hero video, .page-wrap > header video, #v4-main > .kit-hero video, #v4-main > header video, .khero video");
    if (heroVid && hud) {
      // the readout shows only while there is flight footage moving behind it
      var flying = function () { hud.classList.toggle("is-flying", !heroVid.paused && !heroVid.ended); };
      ["playing", "pause", "ended", "emptied"].forEach(function (ev) { heroVid.addEventListener(ev, flying); });
      heroVid.addEventListener("timeupdate", function () {
        var dur = heroVid.duration;
        if (dur && isFinite(dur)) paintHud(heroVid.currentTime / dur);
      });
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
      // its arrow buttons sit outside the rail: a press pauses the drift so their smooth scroll can run
      var sec = rail.closest("section") || rail.parentNode;
      sec.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest("button");
        if (b && !rail.contains(b)) { pause(); later(); }
      }, true);
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
      // v4, the award pass: in the footer, beside "Install the app", not in the header
      var foot = d.querySelector(".footer-bottom");
      if (!foot) return;
      btn = d.createElement("button");
      btn.type = "button"; btn.className = "v2-wind"; btn.setAttribute("aria-pressed", String(on));
      btn.setAttribute("aria-label", "Wind sound"); btn.title = "Wind sound";
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">' +
        '<path d="M3 9h11a3 3 0 1 0-3-3"/><path d="M3 14h15a3 3 0 1 1-3 3"/><path d="M3 19h7"/></svg><span class="v4-wind-l" aria-hidden="true">Wind sound</span>';
      btn.classList.toggle("is-on", on);
      btn.addEventListener("click", function () { set(!on); });
      foot.appendChild(btn);
      footage(foot, btn);
      // remembered as on: a browser only lets sound start after the visitor
      // touches the page, so it waits for the first press or key
      if (on) {
        var first = function () { d.removeEventListener("pointerdown", first, true); d.removeEventListener("keydown", first, true); if (on) start(); };
        d.addEventListener("pointerdown", first, true); d.addEventListener("keydown", first, true);
      }
    }
    // the usability pass (23): beside it, the page's footage can be paused, and
    // stays paused from page to page until it is played again (script.js
    // starts each loop as it comes on screen; a paused visitor's loops are
    // stopped as they start). Only where footage plays: not for reduced motion.
    function footage(foot, after) {
      if (!d.querySelector("video") || (w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches)) return;
      var still = keep.get("v4-still") === "on", b = d.createElement("button");
      b.type = "button"; b.className = "v2-wind v4u-still";
      function own(v) { return v.tagName === "VIDEO" && !v.closest(".cd-player, .v4-ls"); }
      function label() {
        var t = still ? "Play" : "Pause";
        b.setAttribute("aria-label", t); b.title = t;
        b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
          (still ? '<path d="M7 5l12 7-12 7z"/>' : '<path d="M8 5v14"/><path d="M16 5v14"/>') + '</svg><span class="v4-wind-l" aria-hidden="true">' + t + '</span>';
      }
      function inView(v) {
        var r = v.getBoundingClientRect(), when = v.getAttribute("data-loop-when"), host = when && v.closest(when);
        return r.bottom > 0 && r.top < w.innerHeight && r.width > 0 && (!host || host.classList.contains("is-on"));
      }
      d.addEventListener("play", function (e) { if (still && own(e.target)) e.target.pause(); }, true);
      b.addEventListener("click", function () {
        still = !still; keep.set("v4-still", still ? "on" : "off"); label();
        [].forEach.call(d.querySelectorAll("video"), function (v) {
          if (!own(v)) return;
          if (still) v.pause();
          else if ((v.currentSrc || v.getAttribute("src")) && inView(v)) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        });
      });
      label();
      if (still) [].forEach.call(d.querySelectorAll("video"), function (v) { if (own(v)) v.pause(); });
      foot.insertBefore(b, after.nextSibling);
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
    var hero = d.querySelector(".page-wrap > .kit-hero, .page-wrap > header, #v4-main > .kit-hero, #v4-main > header");
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
    if (dy < -4 && Date.now() > hold) show(true);
    else if (dy > 4) show(false);
  }
  /* A card opened over a map (the podcast globe) must never sit under the
     nav: the nav steps aside, and if the card runs off the top or bottom of
     the screen the page moves just enough to show all of it. That move is
     ours, so it does not count as the visitor scrolling up. */
  var hold = 0;
  d.querySelectorAll(".map-popup").forEach(function (card) {
    new MutationObserver(function () {
      if (!card.classList.contains("visible")) return;
      show(false); hold = Date.now() + 900;
      requestAnimationFrame(function () {
        var r = card.getBoundingClientRect(), pad = 16, by = 0;
        if (r.top < pad) by = r.top - pad;
        else if (r.bottom > innerHeight - pad) by = Math.min(r.bottom - innerHeight + pad, r.top - pad);
        if (by) w.scrollBy({ top: by, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
      });
    }).observe(card, { attributes: true, attributeFilter: ["class"] });
  });
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

/* V4 ADDITIONS (prototypes/v4 only)
   6. CARDS OPEN INTO THE PAGE. Pressing an episode card grows its picture into
      the episode's player (a cross-document view transition). The card's
      picture takes the name ep-<slug> as the page is left; the player on the
      episode page carries the same name. Where the browser has no
      cross-document view transitions it is an ordinary link; reduced motion
      turns it off. Going back, the player shrinks into its card
      again (6b), and pages are prerendered from a resting pointer (6c).
   7. THE ALTIMETER. On long pages, a tape down the left edge: ticks, a mark
      at each section, and the glider descending as the page is read.
      Decoration only (aria-hidden), wide screens, off under reduced motion. */
(function () {
  "use strict";
  var d = document, w = window;
  var still = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var store = { get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
                set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} } };
  function slugOf(href) {
    var m = /\/episodes\/([^\/?#]+)\.html/.exec(href || "");
    return m ? m[1] : null;
  }

  /* ------------------------------------------ 6. cards open into the page */
  if (!still) {
    d.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
      var a = e.target.closest && e.target.closest('a[href*="episodes/"]');
      if (!a) return;
      var slug = slugOf(a.href);
      var box = a.closest(".ep-modal, [class*='ep-modal'], .map-popup");
      var img = a.querySelector(".ep-art img, .ep-th img, .ep2-card-art img, .kit-card-media img, img") ||
                (box && box.querySelector("img"));
      if (!slug || !img) return;
      d.querySelectorAll("[data-v4-vt]").forEach(function (x) { x.style.viewTransitionName = ""; x.removeAttribute("data-v4-vt"); });
      img.style.viewTransitionName = "ep-" + slug;
      img.setAttribute("data-v4-vt", "");
      store.set("v4-card", slug);
    }, true);
    w.addEventListener("pagereveal", function (e) {
      var slug = store.get("v4-card"); store.set("v4-card", "");
      if (!slug || !e.viewTransition) return;
      var p = d.querySelector(".ep2-hero-media .cd-player");
      if (p && !p.style.viewTransitionName) {
        p.style.viewTransitionName = "ep-" + slug;
        var off = function () { p.style.viewTransitionName = ""; };
        e.viewTransition.finished.then(off, off);
      }
    });
    w.addEventListener("pageshow", function () {
      d.querySelectorAll("[data-v4-vt]").forEach(function (x) { x.style.viewTransitionName = ""; x.removeAttribute("data-v4-vt"); });
    });
  }

  /* ------------------------------- 6b. back out of an episode, into its card
     Going back from an episode, the player shrinks into the card that opened
     it (the episode page's player carries the name ep-<slug>). Only a card
     on screen takes the name, and only one. */
  if (!still) {
    w.addEventListener("pagereveal", function (e) {
      var nav = w.navigation, act = nav && nav.activation;
      if (!e.viewTransition || !act || act.navigationType !== "traverse" || !act.from) return;
      var slug = slugOf(act.from.url);
      if (!slug) return;
      var vh = w.innerHeight, img = null;
      d.querySelectorAll('a[href*="episodes/' + slug + '.html"]').forEach(function (a) {
        if (img) return;
        var i = a.querySelector(".ep-art img, .ep-th img, .ep2-card-art img, .kit-card-media img, img");
        if (!i) return;
        var r = i.getBoundingClientRect();
        if (r.width && r.bottom > 0 && r.top < vh) img = i;
      });
      if (!img) return;
      d.querySelectorAll("[data-v4-vt]").forEach(function (x) { x.style.viewTransitionName = ""; x.removeAttribute("data-v4-vt"); });
      img.style.viewTransitionName = "ep-" + slug;
      var off = function () { img.style.viewTransitionName = ""; };
      e.viewTransition.finished.then(off, off);
    });
  }

  /* ------------------------------------- 6c. the next page is already there
     Where the browser can, a page in this site is prerendered while the
     pointer rests on its link (or a finger is down on it), so it opens at
     once and the transition plays without a wait. Not on Save-Data. */
  (function () {
    var c = navigator.connection;
    if (c && c.saveData) return;
    if (!(w.HTMLScriptElement && HTMLScriptElement.supports && HTMLScriptElement.supports("speculationrules"))) return;
    var m = /^(.*\/prototypes\/v\d+\/)/.exec(location.pathname);
    var s = d.createElement("script");
    s.type = "speculationrules";
    s.textContent = JSON.stringify({ prerender: [{ where: { and: [
      { href_matches: (m ? m[1] : "/") + "*" },
      { not: { selector_matches: "[target], [download], [href*='enquire']" } }
    ] }, eagerness: "moderate" }] });
    d.head.appendChild(s);
  })();

  /* ------------------------------------------------------- 7. the altimeter */
  function altimeter() {
    return;   // v4, the award pass (owner, 4 Oct): one progress mark, the bar at the top, is enough
    if (still || !w.matchMedia("(min-width: 1180px)").matches) return;
    var H = d.documentElement.scrollHeight, vh = w.innerHeight;
    if (H < vh * 3.5) return;
    var fl = d.querySelector(".flightline");
    if (fl) fl.style.display = "none";
    var el = d.createElement("div");
    el.className = "v4-alti";
    el.setAttribute("aria-hidden", "true");
    var ticks = "";
    for (var i = 0; i <= 20; i++) ticks += '<i class="t' + (i % 5 ? "" : " is-maj") + '" style="--p:' + (i * 5) + '%"></i>';
    el.innerHTML = '<span class="v4-alti-tape">' + ticks + '</span><span class="v4-alti-marks"></span><b class="v4-alti-g"></b>';
    d.body.appendChild(el);
    var marks = el.querySelector(".v4-alti-marks");
    function place() {
      var max = d.documentElement.scrollHeight - w.innerHeight;
      if (max <= 0) return;
      var html = "";
      d.querySelectorAll(".cd-center h2, main:not(#v4-main) h2, .page-wrap > section h2, #v4-main > section h2, .dst-main h2").forEach(function (h) {
        if (h.closest("details:not([open]), footer, nav, [hidden]")) return;
        var y = h.getBoundingClientRect().top + w.scrollY - w.innerHeight * .3;
        var p = Math.max(0, Math.min(1, y / max));
        html += '<i style="--p:' + (p * 100).toFixed(2) + '%"></i>';
      });
      marks.innerHTML = html;
    }
    place();
    w.addEventListener("load", place);
    w.addEventListener("resize", place, { passive: true });
    d.addEventListener("toggle", place, true);
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", altimeter); else altimeter();
})();

/* V4 MENU (prototypes/v4 only)
   8. THE FULL-SCREEN MENU AND THE ONE SEARCH (v4-menu.js, loaded the first
      time the menu is opened, so no page carries it on arrival). The search
      button in the header, and on a phone the menu toggle, open it. */
(function () {
  "use strict";
  var d = document, w = window;
  var m = /^(.*\/prototypes\/v\d+\/)/.exec(location.pathname);
  var SRC = m ? m[1] + "v4-menu.js" : "/assets/v4/v4-menu.js";
  var loading = false, failed = false;
  // if v4-menu.js cannot load (offline, blocked, too slow), the tap still does something:
  // the toggle falls back to the small panel (nav-menu.js), the search to the sitemap
  function fallback(from) {
    failed = true;
    if (from && from.classList.contains("nav-toggle")) from.click();
    else location.href = (m ? m[1] : "/") + "sitemap.html";
  }
  function open(focusSearch, from) {
    if (w.V4_MENU) { w.V4_MENU.open(focusSearch); return; }
    if (loading) return;
    loading = true;
    var s = d.createElement("script"), done = false;
    var t = setTimeout(function () { if (!done) { done = true; loading = false; fallback(from); } }, 6000);
    s.src = SRC;
    s.onload = function () { if (done) return; done = true; clearTimeout(t); loading = false; if (w.V4_MENU) w.V4_MENU.open(focusSearch); else fallback(from); };
    s.onerror = function () { if (done) return; done = true; clearTimeout(t); loading = false; fallback(from); };
    d.head.appendChild(s);
  }
  // the usability pass (15): a search field in the page itself ([data-v4-find]: the knowledge base's) runs the
  // same search into its own list, loading v4-menu.js on first use. Enter goes to the first result; without
  // script the form goes to the sitemap, which lists every page.
  var waiting = null;
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
  function finder(form) {
    var q = form.querySelector("input[type=search]"), ol = form.querySelector("ol");
    if (!q || !ol) return;
    function go() { get(function () { w.V4_MENU.find(q.value, ol); }); }
    q.addEventListener("focus", function () { get(function () {}); });
    q.addEventListener("input", go);
    form.addEventListener("submit", function (e) {
      var a = ol.querySelector("a[href]");
      if (a) { e.preventDefault(); location.href = a.href; } else if (w.V4_MENU) { e.preventDefault(); go(); }
    });
  }
  function mount() {
    [].forEach.call(d.querySelectorAll("[data-v4-find]"), finder);
    var nav = d.querySelector(".page-wrap > nav");
    if (!nav) return;
    var cta = nav.querySelector(".nav-cta");
    var b = d.createElement("button");
    b.type = "button";
    b.className = "v4-open";
    b.setAttribute("aria-expanded", "false");     // aria-controls comes with the menu (v4-menu.js), once it exists
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg><span>Search</span>';
    b.addEventListener("click", function () { open(true, b); });
    if (cta) nav.insertBefore(b, cta); else nav.appendChild(b);
    // anything marked data-v4-search opens the search (the 404 page's button; a link to the sitemap without JS)
    d.addEventListener("click", function (e) {
      var s = e.target.closest && e.target.closest("[data-v4-search]");
      if (s && !failed) { e.preventDefault(); open(true, s); }
    });
    // the phone's menu toggle opens the full-screen menu instead of the small panel
    d.addEventListener("click", function (e) {
      var t = e.target.closest && e.target.closest(".nav-toggle");
      if (!t || failed) return;
      e.preventDefault(); e.stopImmediatePropagation();
      open(false, t);
    }, true);
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", mount); else mount();
})();

/* 9. EPISODES ON A PHONE: Play and Next in a bar at the foot of the screen,
      once the opening has scrolled away (like the trips' booking bar). Play
      starts the audio player, or brings the video player into view. */
(function () {
  "use strict";
  var d = document;
  function init() {
  var bar = d.getElementById("v4Epbar");
  if (!bar) return;
  var hero = d.querySelector(".ep2-hero"), foot = d.querySelector("footer");
  bar.querySelector(".v4-play").addEventListener("click", function () {
    var au = d.querySelector(".ep-au-play");
    var pl = d.querySelector(".ep2-hero-media .cd-player");
    if (pl) pl.scrollIntoView({ behavior: "smooth", block: "center" });
    if (au) au.click();
    else if (pl) { var f = pl.querySelector("iframe"); if (f) f.focus(); }
  });
  if (!("IntersectionObserver" in window) || !hero) { bar.classList.add("show"); return; }
  var seen = new Set();
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) seen.add(e.target); else seen.delete(e.target); });
    bar.classList.toggle("show", seen.size === 0);
    bar.inert = seen.size !== 0;   // off screen it takes no Tab stops
  }, { threshold: 0 });
  io.observe(hero); if (foot) io.observe(foot);
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();

/* 10. THE KENYA CHART'S RELIEF, IN THE PREVIEW. The chart (kenya-map.js) is
      fetched and placed in the page; its relief picture is named from the
      live page's folder (../assets/), which misses from the preview's
      deeper folder. In the preview only, point it at the same file. */
(function () {
  "use strict";
  var m = /^(.*\/)prototypes\/v\d+\//.exec(location.pathname);
  function init() {
    var sheet = document.querySelector(".kmap-sheet");
    if (!m || !sheet || !("MutationObserver" in window)) return;
    new MutationObserver(function () {
      sheet.querySelectorAll("image").forEach(function (im) {
        var h = im.getAttribute("href") || "";
        if (h.indexOf("../assets/") === 0) im.setAttribute("href", m[1] + h.slice(3));
      });
    }).observe(sheet, { childList: true });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();

/* 11. THE DRAWINGS DRAW THEMSELVES (owner, 27 Sep 2026). A knowledge base
      drawing, as it comes into view, traces its lines, then its words
      arrive, and the orange lands last. The kit's strokes keep one width at
      any size (vector-effect), so a dash is measured in screen pixels: each
      line's length is measured at the moment it draws, and the dash is
      taken off again once it has drawn, leaving the drawing exactly as made.
      Lines marked .fl keep moving (air along the computed streamlines, a
      climb, a breeze); that is CSS. Reduced motion, or no script: the
      drawing is simply there. */
(function () {
  "use strict";
  var w = window, d = document;
  if (!("IntersectionObserver" in w) || (w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches)) return;
  var SHAPES = "path,polyline,line,circle,ellipse,polygon";
  var MAX = 700;                                   // a drawing with more lines than this fades in instead
  function lines(svg) {
    return Array.prototype.filter.call(svg.querySelectorAll(SHAPES), function (s) {
      if (s.closest("defs,pattern,clipPath,mask") || s.classList.contains("fl")) return false;
      var cs = getComputedStyle(s);
      return cs.stroke !== "none" && cs.strokeDasharray === "none" && parseFloat(cs.strokeWidth) > 0;
    });
  }
  function draw(svg) {
    var ls = svg.__kd || [];
    var m = svg.getScreenCTM && svg.getScreenCTM();
    var k = m ? Math.sqrt(m.a * m.a + m.b * m.b) : 0;
    ls.forEach(function (s) {
      var L = 0;
      try { L = s.getTotalLength() * k; } catch (e) { L = 0; }
      if (!(L > 1)) { s.classList.remove("kd-h"); return; }
      s.style.strokeDasharray = L + " " + L;
      s.style.strokeDashoffset = L;
    });
    svg.getBoundingClientRect();                    // commit the start before the change
    ls.forEach(function (s, i) {
      var cs = getComputedStyle(s);
      var late = /255, 117, 23|#ff7517/i.test(cs.stroke);
      s.style.transition = "stroke-dashoffset 1.5s cubic-bezier(.65,0,.2,1) " + ((late ? .55 : 0) + Math.min(i * .006, .35)) + "s";
      s.classList.remove("kd-h");
      s.style.strokeDashoffset = 0;
      s.addEventListener("transitionend", end);
      s.addEventListener("transitioncancel", end);   // cut short (hidden by the wide/phone swap): end clean too
      function end() {
        s.removeEventListener("transitionend", end);
        s.removeEventListener("transitioncancel", end);
        s.style.strokeDasharray = s.style.strokeDashoffset = s.style.transition = "";
      }
    });
    svg.classList.add("kd-in");
  }
  function init() {
    var svgs = d.querySelectorAll("svg.kbd");
    if (!svgs.length) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        // most drawings wait until a fifth is on screen; one wider than the screen (a hero
        // shifted sideways on a phone) may never get there, so it draws once its box is in view
        var r = e.boundingClientRect, wide = r.width > (w.innerWidth || 0) * 1.2;
        if (e.intersectionRatio < .2 && !wide) return;
        io.unobserve(e.target);
        draw(e.target);
      });
    }, { threshold: [0, .05, .2] });
    Array.prototype.forEach.call(svgs, function (svg) {
      var ls = lines(svg);
      svg.classList.add("kd", ls.length > MAX ? "kd-fade" : "kd-draw");
      svg.__kd = ls.length > MAX ? [] : ls;
      svg.__kd.forEach(function (s) { s.classList.add("kd-h"); });
      io.observe(svg);
    });
  }
  // printing: every drawing finished, whether or not it was scrolled to
  function finish() {
    Array.prototype.forEach.call(d.querySelectorAll("svg.kd:not(.kd-in)"), function (svg) {
      (svg.__kd || []).forEach(function (s) { s.classList.remove("kd-h"); });
      svg.classList.add("kd-in");
    });
  }
  w.addEventListener("beforeprint", finish);
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();

/* 12. KEYBOARD (docs/v4-stress-test.md). A skip link past the header, and any
      open dialog that says it is modal keeps Tab inside it: the knowledge
      base door, the photo lightbox, the episode card. */
(function () {
  "use strict";
  var d = document;
  function skip() {
    var h = d.querySelector("main") || d.querySelector("h1");   // the page's one main (the usability pass, 21)
    if (!h || d.querySelector(".v4-skip")) return;
    var t = h.tagName === "MAIN" ? h : (h.closest("header, section, article") || h);
    if (!t.id) t.id = "v4-main";
    if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "-1");
    var a = d.createElement("a");
    a.className = "v4-skip"; a.href = "#" + t.id; a.textContent = "Skip to content";
    d.body.insertBefore(a, d.body.firstChild);
  }
  var FOC = 'a[href],button:not([disabled]),input:not([disabled]),select,textarea,summary,[tabindex]:not([tabindex="-1"])';
  function shown(el) {
    if (!el.getClientRects().length) return false;
    var cs = getComputedStyle(el);
    return cs.visibility !== "hidden" && cs.display !== "none";
  }
  d.addEventListener("keydown", function (e) {
    if (e.key !== "Tab") return;
    var ms = [].filter.call(d.querySelectorAll('[aria-modal="true"]'), shown);
    var m = ms[ms.length - 1];
    if (!m) return;
    var f = [].filter.call(m.querySelectorAll(FOC), shown);
    if (!f.length) { e.preventDefault(); return; }
    var a = d.activeElement, first = f[0], last = f[f.length - 1];
    if (!m.contains(a)) { e.preventDefault(); (e.shiftKey ? last : first).focus(); }
    else if (e.shiftKey && a === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && a === last) { e.preventDefault(); first.focus(); }
  });
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", skip); else skip();
})();

/* 13. SMALL ACCESSIBILITY REPAIRS (docs/v4-stress-test.md): a box that scrolls
      sideways can be reached and scrolled by keyboard and has a name; an icon
      inside a link or button is not read out on top of its label. */
(function () {
  "use strict";
  var d = document;
  function run() {
    d.querySelectorAll(".iroute-scroll, .pol-tablewrap").forEach(function (el) {
      if (el.scrollWidth <= el.clientWidth + 1 || el.hasAttribute("tabindex")) return;
      el.setAttribute("tabindex", "0");
      if (!el.getAttribute("role")) el.setAttribute("role", "region");
      if (!el.getAttribute("aria-label")) {
        var h = el.closest("section") && el.closest("section").querySelector("h2, h3");
        el.setAttribute("aria-label", (h ? h.textContent.trim() + ", " : "") + "scrolls sideways");
      }
    });
    // an svg read as one picture cannot hold things to press (the sitemap's graph): it is a group
    d.querySelectorAll('svg[role="img"]').forEach(function (s) {
      if (s.querySelector('a[href], [tabindex]:not([tabindex="-1"]), button')) s.setAttribute("role", "group");
    });
    // the podcast page's feeds: if they have not arrived after 12 s, say so instead of "Connecting" for ever
    var st = [d.getElementById("ytStatus"), d.getElementById("liveFeedStatus")].filter(Boolean);
    if (st.length) setTimeout(function () {
      st.forEach(function (el) {
        if (!/^Connecting/.test(el.textContent.trim())) return;
        el.textContent = "The feed did not load. Every episode is in the ";
        var a = d.createElement("a"); a.href = "library.html"; a.textContent = "library"; a.style.color = "var(--orange)";
        el.appendChild(a); el.appendChild(d.createTextNode("."));
      });
    }, 12000);
    d.querySelectorAll("a svg:not([role]):not([aria-label]):not([aria-hidden]), button svg:not([role]):not([aria-label]):not([aria-hidden])").forEach(function (s) {
      var host = s.closest("a, button");
      if (host && host.textContent.trim()) s.setAttribute("aria-hidden", "true");
    });
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", run); else run();
})();

/* 14. THE FLY-THROUGH (tools/v4_flythrough.py): on the trip pages, the
      photographs pass one at a time while the section holds still; each
      drifts slowly closer, the counter and the gold line follow. Reduced
      motion: the CSS shows a column and this does nothing. */
(function () {
  "use strict";
  var d = document, w = window;
  function init() {
    var sec = d.querySelector(".gxa");
    if (!sec || (w.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) return;
    var track = sec.querySelector(".gxa-track"), figs = [].slice.call(sec.querySelectorAll(".gxa-f"));
    var count = sec.querySelector(".gxa-count b"), rail = sec.querySelector(".gxa-rail"), n = figs.length, at = -1, raf = 0;
    if (!n) return;
    function frame() {
      raf = 0;
      var r = track.getBoundingClientRect(), span = r.height - w.innerHeight;
      if (r.bottom < -200 || r.top > w.innerHeight + 200) return;
      var p = Math.min(1, Math.max(0, -r.top / Math.max(1, span)));
      var x = Math.min(n - .0001, p * n), i = Math.floor(x), t = x - i;
      if (i !== at) {
        figs.forEach(function (f, k) { f.classList.toggle("is-on", k === i); });
        // the next photograph starts loading while this one is on screen
        var nx = figs[i + 1] && figs[i + 1].querySelector("img");
        if (nx && nx.loading === "lazy") nx.loading = "eager";
        count.textContent = (i < 9 ? "0" : "") + (i + 1);
        at = i;
      }
      figs[i].style.setProperty("--t", t.toFixed(3));
      rail.style.setProperty("--p", (n > 1 ? x / n : 1).toFixed(4));
    }
    w.addEventListener("scroll", function () { if (!raf) raf = requestAnimationFrame(frame); }, { passive: true });
    w.addEventListener("resize", frame);
    frame();
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();

/* 15. THE TRIP MAP (tools/v4_tripmap.py): the camera falls from the continent
      to the country to the flying region, then follows the route site by
      site while the line diagram along the foot slides to each station and
      fills. Map marks keep their size at every zoom (--u, map units a pixel).
      Reduced motion: the CSS shows it all still and this only frames the map. */
(function () {
  "use strict";
  var d = document, w = window;
  function init() {
    var sec = d.querySelector(".tm");
    if (!sec) return;
    var keys = JSON.parse(sec.dataset.keys), kms = JSON.parse(sec.dataset.km || "[]"), xs = JSON.parse(sec.dataset.x), W = +sec.dataset.w;
    var svg = sec.querySelector(".tm-map"), track = sec.querySelector(".tm-track"), route = sec.querySelector(".tm-route");
    var sites = [].slice.call(sec.querySelectorAll(".tm-site")), cards = [].slice.call(sec.querySelectorAll(".tm-card"));
    var sts = [].slice.call(sec.querySelectorAll(".tm-st")), line = sec.querySelector(".tm-line svg"), move = sec.querySelector(".tm-move"), l1 = sec.querySelector(".tm-l1");
    var head = sec.querySelector(".tm-head"), km = sec.querySelector(".tm-km b"), n = cards.length, F = keys.focus, raf = 0, at = -2;
    var len = route ? route.getTotalLength() : 0;
    // India: the page's own schematic is the route; each card lights its line on it
    var schem = sec.querySelector(".tm-schem"), hl = JSON.parse(sec.dataset.hl || "[]");
    var cum = [0]; for (var i = 1; i < F.length; i++) cum.push(cum[i - 1] + Math.hypot(F[i][0] - F[i - 1][0], F[i][1] - F[i - 1][1]));
    function lerp(a, b, t) { return a + (b - a) * t; }
    function cam(a, b, t) { t = t * t * (3 - 2 * t); return [lerp(a[0], b[0], t), lerp(a[1], b[1], t), Math.exp(lerp(Math.log(a[2]), Math.log(b[2]), t))]; }
    function view(c) {
      var r = svg.getBoundingClientRect(), vw = c[2], vh = vw * r.height / Math.max(1, r.width);
      if (r.width < r.height) { vh = c[2] * 1.15; vw = vh * r.width / r.height; }
      svg.setAttribute("viewBox", (c[0] - vw / 2).toFixed(2) + " " + (c[1] - vh * (w.innerWidth < 760 ? .24 : .45)).toFixed(2) + " " + vw.toFixed(2) + " " + vh.toFixed(2));
      svg.style.setProperty("--u", (vw / Math.max(1, r.width)).toFixed(4));
    }
    function show(i) {
      if (i === at) return; at = i;
      cards.forEach(function (c, k) { c.classList.toggle("is-on", k === i); });
      sites.forEach(function (s, k) { s.classList.toggle("is-on", k === Math.min(i, sites.length - 1) && i >= 0); s.classList.toggle("is-past", i >= 0 && k <= i); });
      sts.forEach(function (s, k) { s.classList.toggle("is-on", k === i); s.classList.toggle("is-past", i >= 0 && k <= i); });
    }
    if (w.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) { view(keys.region); return; }
    if (route) { route.style.strokeDasharray = len; route.style.strokeDashoffset = len; }
    if (l1) { l1.style.strokeDasharray = W; l1.style.strokeDashoffset = W; }
    function frame() {
      raf = 0;
      var r = track.getBoundingClientRect();
      if (r.bottom < -100 || r.top > w.innerHeight + 100) return;
      var p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - w.innerHeight)));
      var c, fine = 0, ter = 0, cn = 0, rt = 0, cur = -1, x = 0;
      if (p < .2) { c = cam(keys.world, keys.country, p / .2); cn = Math.max(0, (p - .08) / .12); }
      else if (p < .32) { var t = (p - .2) / .12; c = cam(keys.country, keys.region, t); cn = 1 - t; fine = t; ter = t * .85; }
      else {
        fine = 1; ter = .85; rt = Math.min(1, (p - .32) / .05);
        var q = Math.min(1, (p - .32) / .64);
        x = Math.min(n - 1, q * (n - 1) * 1.06); cur = Math.min(n - 1, Math.round(x));
        var i0 = Math.floor(x), t2 = x - i0, f0 = F[Math.min(F.length - 1, i0)], f1 = F[Math.min(F.length - 1, i0 + 1)];
        c = cam(keys.region, [lerp(f0[0], f1[0], t2), lerp(f0[1], f1[1], t2), keys.region[2] * keys.zoom], Math.min(1, q * 5));
        if (route) {
          var g0 = cum[Math.min(cum.length - 1, i0)], g1 = cum[Math.min(cum.length - 1, i0 + 1)];
          route.style.strokeDashoffset = (len * (1 - lerp(g0, g1, t2) / Math.max(1, cum[cum.length - 1]))).toFixed(1);
        }
        if (schem) {
          schem.setAttribute("data-on", hl[cur] || "");
          // on a phone the schematic is framed on the line being described, at a size its words can be read
          var sv = schem.querySelector("svg"), crop = { "ir-home": "400 40 500 330", "ir-west": "200 60 600 330", "ir-east": "470 60 500 330", "ir-over": "460 20 500 330" };
          if (sv) {
            if (!sv.dataset.vb) sv.dataset.vb = sv.getAttribute("viewBox");
            sv.setAttribute("viewBox", w.innerWidth < 760 && crop[hl[cur]] ? crop[hl[cur]] : sv.dataset.vb);
          }
        }
        else {
          var pos = xs[i0] + ((xs[Math.min(n - 1, i0 + 1)]) - xs[i0]) * t2;
          var vb = line.viewBox.baseVal, scale = line.getBoundingClientRect().height / vb.height;
          move.style.setProperty("--sx", ((w.innerWidth * (w.innerWidth < 760 ? .5 : .62)) / scale + vb.x - pos).toFixed(1) + "px");
          l1.style.strokeDashoffset = (W - pos).toFixed(1);
        }
        if (km && kms.length) km.innerHTML = Math.round(lerp(kms[i0], kms[Math.min(n - 1, i0 + 1)], t2)) + "<small>km</small>";
      }
      if (cur < 0) { if (route) route.style.strokeDashoffset = len; if (km) km.innerHTML = "0<small>km</small>"; }
      view(c);
      svg.style.setProperty("--fine", fine.toFixed(3)); svg.style.setProperty("--ter", ter.toFixed(3)); svg.style.setProperty("--cn", Math.min(1, cn).toFixed(3));
      sec.style.setProperty("--route", rt.toFixed(3));
      sec.classList.toggle("is-route", rt > 0);
      head.style.opacity = p < .2 ? 1 : Math.max(0, 1 - (p - .2) / .05);   // gone before the map lands under it
      show(cur);
    }
    w.addEventListener("scroll", function () { if (!raf) raf = requestAnimationFrame(frame); }, { passive: true });
    w.addEventListener("resize", frame);
    frame();
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();

/* 10. LISTENING MODE (v4-listen.js, loaded the first time it is opened, so
       no page carries it on arrival). A button under the player on episode
       pages with a transcript; #listen opens it straight away. */
(function () {
  "use strict";
  var d = document, w = window;
  var m = /^(.*\/prototypes\/v\d+\/)/.exec(location.pathname);
  var SRC = m ? m[1] + "v4-listen.js" : "/assets/v4/v4-listen.js";
  function init() {
    if (d.body.getAttribute("data-v2") !== "ep") return;
    var player = d.querySelector(".cd-player");
    if (!player || !d.querySelector(".cd-line")) return;
    var host = d.querySelector(".ep2-hero-media") || player.parentNode;
    // the usability pass (11): tools/v4_ux.py puts the button in the page, so the hero does not grow
    // under the reader once it has drawn; made here only where the page does not carry it
    var b = d.querySelector(".v4-ls-open"), loading = false;
    if (!b) {
      b = d.createElement("button");
      b.type = "button";
      b.className = "v4-ls-open";
      b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="7" rx="1.2"/><rect x="17" y="14" width="4" height="7" rx="1.2"/></svg><span>Listening mode</span>';
      host.appendChild(b);
    }
    // (12) it names the screen it opens only once that screen exists
    function named() { if (d.getElementById("v4Listen")) b.setAttribute("aria-controls", "v4Listen"); }
    function open() {
      if (w.V4_LISTEN) { w.V4_LISTEN.open(b); named(); return; }
      if (loading) return;
      loading = true;
      var s = d.createElement("script");
      s.src = SRC;
      s.onload = function () { loading = false; if (w.V4_LISTEN) { w.V4_LISTEN.open(b); named(); } };
      s.onerror = function () { loading = false; b.hidden = true; };
      d.head.appendChild(s);
    }
    b.addEventListener("click", open);
    if (location.hash === "#listen") open();
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();

/* 16. THE GLOW AND THE GROUND (owner, 4 Oct 2026: "the immersiveness to the
       max"). The episode's own picture, blurred, glows behind its player and
       behind the listening screen. Hero pictures, footage and the episode
       globe shift a few pixels against the pointer, or against a phone's
       tilt where the phone gives it without asking (an iPhone asks first, so
       there it stays still). Reduced motion: nothing moves. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  function glow() {
    var p = d.querySelector(".ep2-hero-media .cd-player");
    var v = p && p.style.getPropertyValue("--cd-poster");
    if (!v) return;
    p.parentNode.style.setProperty("--v4-glow", v);
    var mo = new MutationObserver(function () {
      var ls = d.getElementById("v4Listen");
      if (ls) { ls.style.setProperty("--v4-glow", v); mo.disconnect(); }
    });
    mo.observe(d.body, { childList: true });
  }
  function ground() {
    if (w.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var tx = 0, ty = 0, x = 0, y = 0, raf = 0, on = false;
    function loop() {
      x += (tx - x) * 0.08; y += (ty - y) * 0.08;
      root.style.setProperty("--px", x.toFixed(3));
      root.style.setProperty("--py", y.toFixed(3));
      raf = (Math.abs(tx - x) + Math.abs(ty - y) > 0.002) ? requestAnimationFrame(loop) : 0;
    }
    function aim(a, b) {
      tx = Math.max(-1, Math.min(1, a)); ty = Math.max(-1, Math.min(1, b));
      if (!on) { on = true; root.classList.add("v4-px"); }
      if (!raf) raf = requestAnimationFrame(loop);
    }
    if (w.matchMedia("(hover: hover) and (pointer: fine)").matches) {
      w.addEventListener("pointermove", function (e) { aim(e.clientX / w.innerWidth * 2 - 1, e.clientY / w.innerHeight * 2 - 1); }, { passive: true });
      return;
    }
    if (!("DeviceOrientationEvent" in w) || typeof DeviceOrientationEvent.requestPermission === "function") return;
    var b0 = null;
    w.addEventListener("deviceorientation", function (e) {
      if (e.gamma === null || e.beta === null) return;
      if (b0 === null) b0 = e.beta;
      b0 += (e.beta - b0) * 0.01;          // the way it is held drifts back to level
      aim(e.gamma / 22, (e.beta - b0) / 22);
    }, { passive: true });
  }
  // the ground parallax is off (the award pass, owner 4 Oct: one motion language);
  // ground() stays for a later look
  function init() { glow(); }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();

/* ===========================================================================
   LIVE FROM THE FEED (podcast, "Night flight"): the ring around the playing
   episode's art fills with the episode. rss-feed.js (do-not-modify, untouched)
   already writes the progress bar's width; this copies it into --p on the row,
   which the ring in v2.css reads.
   ========================================================================= */
(function () {
  var grid = document.getElementById("liveFeedGrid");
  if (!grid || !window.MutationObserver) return;
  new MutationObserver(function (list) {
    for (var i = 0; i < list.length; i++) {
      var t = list[i].target;
      if (!t.classList || !t.classList.contains("ep-progress-fill")) continue;
      var row = t.closest(".ep-row");
      if (row) row.style.setProperty("--p", ((parseFloat(t.style.width) || 0) / 100).toFixed(4));
    }
  }).observe(grid, { subtree: true, attributes: true, attributeFilter: ["style"] });
})();
