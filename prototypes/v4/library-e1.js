/* The library, option E1: the ridge and the voices on one screen. The page arrives once (the still pulls back, the sentence forms on rails, the ridge grows),
   then nothing moves unless the visitor hovers, taps, presses or scrolls. Sound only on a press of the voice row, and only when a clip exists. */
(function () {
  "use strict";
  var dataEl = document.getElementById("v4l-data"); if (!dataEl) return;
  var D; try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var NS = "http://www.w3.org/2000/svg", EPS = D.eps, bySlug = {}; EPS.forEach(function (e) { bySlug[e.s] = e; });
  var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var smallMq = window.matchMedia && window.matchMedia("(max-width: 700px)"), small = !!(smallMq && smallMq.matches);   // the phone layout, under 700 px
  var EASE = "cubic-bezier(.2,.7,.2,1)";                      // the one easing of the hero
  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function mix(a, b) { var o = {}, k; for (k in a) o[k] = a[k]; for (k in b) o[k] = b[k]; return o; }
  function fmt(s) { s = Math.max(0, Math.round(s)); var m = Math.floor(s / 60), r = s % 60; return (m < 10 ? "0" : "") + m + ":" + (r < 10 ? "0" : "") + r; }
  var BASE = D.base || "";
  // stills and clips are files: in the prototype beside the page, on the live site under /assets/v4/ (the switch-over moves files, not pages, and does not rewrite script strings)
  var FILES = (/^(.*\/prototypes\/v\d+\/)/.exec(location.pathname) || [0, "/assets/v4/"])[1];
  function still(e) { return e.i ? FILES + "img/library/stills/s/" + e.i + ".webp" : ""; }
  function epUrl(s) { return BASE + "episodes/" + s + ".html"; }

  /* ---------- the ridge: one column a conversation, drawn into an svg ---------- */
  function drawRidge(svg, H, pad, opts) {                     // returns the lines by slug; opts.hits adds a wide invisible stroke to take the pointer
    var W = 1000, lines = {}, pts = [], id = opts && opts.gid || "v4l-g";
    var defs = document.createElementNS(NS, "defs"); defs.innerHTML = '<linearGradient id="' + id + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7517" stop-opacity=".12"/><stop offset="1" stop-color="#141519" stop-opacity="0"/></linearGradient>'; svg.appendChild(defs);
    var area = document.createElementNS(NS, "path"); area.setAttribute("class", opts && opts.hits ? "v4l1-area" : "v4l-area"); svg.appendChild(area);
    var dated = EPS.filter(function (e) { return e.x >= 0; }), cols = document.createElementNS(NS, "g"), hits = document.createElementNS(NS, "g");
    dated.forEach(function (e, k) {
      var x = pad + e.x * (W - 2 * pad), h = Math.max(6, e.h * H * 0.9); pts.push([x, H - h]);
      var l = document.createElementNS(NS, "line"); l.setAttribute("x1", x.toFixed(1)); l.setAttribute("x2", x.toFixed(1)); l.setAttribute("y1", H); l.setAttribute("y2", (H - h).toFixed(1)); l.setAttribute("data-s", e.s); l.setAttribute("vector-effect", "non-scaling-stroke");
      if (opts && opts.hits) { l.setAttribute("class", "v4l1-col"); var hl = l.cloneNode(false); hl.setAttribute("class", "v4l1-hit"); hits.appendChild(hl); }
      cols.appendChild(l); lines[e.s] = { el: l, x: x, y: H - h, k: k, e: e };
    });
    area.setAttribute("d", "M" + pad + " " + H + " " + pts.map(function (p) { return "L" + p[0].toFixed(1) + " " + (p[1] + 8).toFixed(1); }).join(" ") + " L" + (W - pad) + " " + H + " Z");
    svg.appendChild(cols); if (opts && opts.hits) svg.appendChild(hits);
    lines._order = dated.map(function (e) { return e.s; }); lines._area = area;
    return lines;
  }

  /* ---------- the hero: one screen, one voice ---------- */
  var hero = document.getElementById("voices"), filterShelf = null;       // filterShelf is set by the finder below
  var nav = document.querySelector("nav");
  function navH() { if (nav) document.documentElement.style.setProperty("--v4l1-nav", nav.offsetHeight + "px"); }
  navH(); window.addEventListener("resize", navH);
  if (hero) {
    var svg = hero.querySelector(".v4l1-rs"), plot = hero.querySelector(".v4l1-plot"), voice = hero.querySelector(".v4l1-voice"), bgs = [].slice.call(hero.querySelectorAll(".v4l1-bg img"));
    var face = hero.querySelector(".v4l1-face"), qn = hero.querySelector(".v4l1-qn"), qs = hero.querySelector(".v4l1-qs"), qd = hero.querySelector(".v4l1-qd"), qt = hero.querySelector(".v4l1-qt"), qw = hero.querySelector(".v4l1-qw");
    var pos = hero.querySelector(".v4l1-pos"), pi = hero.querySelector(".v4l1-pi"), live = hero.querySelector(".v4l1-live"), tip = hero.querySelector(".v4l1-tip"), dotOn = hero.querySelector(".v4l1-dot-on"), dotHot = hero.querySelector(".v4l1-dot-hot"), axis = hero.querySelector(".v4l1-axis");
    var facebox = hero.querySelector(".v4l1-facebox"), bgEl = hero.querySelector(".v4l1-bg"), stem = hero.querySelector(".v4l1-stem"), ticks = [].slice.call(hero.querySelectorAll(".v4l1-ticks b")), pim = hero.querySelector(".v4l1-pim"), kickF = hero.querySelector(".v4l1-kick-f");
    var act = hero.querySelector(".v4l1-act"), hear = hero.querySelector(".v4l1-hear"), ring = hero.querySelector(".v4l1-ring"), say = hero.querySelector(".v4l1-say"), sayT = hero.querySelector(".v4l1-say-t"), sayAt = hero.querySelector(".v4l1-at"), sayLen = hero.querySelector(".v4l1-len"), cv = hero.querySelector(".v4l1-wave"), sayM = hero.querySelector(".v4l1-say-m"), keep = hero.querySelector(".v4l1-keep"), navEl = hero.querySelector(".v4l1-nav");
    var pad = 16, H = 300, lines = drawRidge(svg, H, pad, { hits: true, gid: "v4l1-g" }), order = lines._order, STOPS = D.stops, cur = "", hot = "", swapT = 0, hoverT = 0, keyT = 0;
    STOPS.forEach(function (s) { if (lines[s]) lines[s].el.classList.add("is-path"); });
    // the marked path: a dotted line from voice to voice over the ridge
    var path = document.createElementNS(NS, "path"); path.setAttribute("class", "v4l1-path");
    path.setAttribute("d", STOPS.map(function (s, k) { var l = lines[s]; return (k ? "L" : "M") + l.x.toFixed(1) + " " + (l.y - 10).toFixed(1); }).join(" ")); svg.insertBefore(path, svg.querySelector("g"));
    // the years along the bottom, each at its own date
    var yrs = D.yrs.filter(function (y, k) { return !(k === 0 && D.yrs.length > 1 && D.yrs[1][1] - y[1] < 0.06); });
    axis.innerHTML = yrs.map(function (y) { return '<span' + (y[1] === 0 ? ' class="is-edge"' : "") + ' style="left:' + ((pad + y[1] * (1000 - 2 * pad)) / 10).toFixed(2) + '%">' + y[0] + "</span>"; }).join("");
    function placeDot(dot, l) { dot.style.left = (l.x / 10) + "%"; dot.style.top = (l.y / H * 100) + "%"; }
    function pct(l) { return { x: (l.x / 10) + "%", y: (l.y / H * 100) + "%" }; }
    var bgOn = 0, bgSeq = 0;
    function own(im) { function set() { if (im.naturalWidth) { im.width = im.naturalWidth; im.height = im.naturalHeight; } } im.addEventListener("load", set); if (im.complete) set(); }   // width and height follow the still's own pixels (they vary; no layout depends on them)
    bgs.forEach(own); if (face) own(face);
    function wide(e) { return e.i ? FILES + "img/library/stills/" + (small ? "p" : "w") + "/" + e.i + ".webp" : ""; }   // the phone takes the portrait crop: the thumbnail's lettering stays outside the frame
    function mastBottom() {                                   // the phone: the foot of the masthead (its numbers line), in the photo box's pixels
      var t = hero.querySelector(".v4l1-top"), s = hero.querySelector(".v4l1-sum"); if (!t || !s || !s.offsetHeight) return 122;
      return t.offsetTop + s.offsetTop + s.offsetHeight - bgEl.offsetTop;
    }
    function landing(e) {                                     // the phone's landing frame: how far down the still sits so the face starts under the masthead, eyes well clear of it, chin inside the box
      var f = e && e.fy && e.fy.length === 3 ? e.fy : [.02, .2, .55], ph = bgEl.clientHeight, mb = mastBottom();   // no face found: these stills carry the head high
      function y(fr) { return ph * (.35 + (fr - .35) * 1.03); }                                                       // the still is 100 % of the box, scaled 1.03 about 50% 35%
      var T = Math.max(mb - 24 - y(f[0]), mb + 56 - y(f[1])); T = Math.min(T, ph - 8 - y(f[2]), mb);
      hero.style.setProperty("--v4l1-mb", Math.round(mb) + "px");
      return Math.round(Math.max(16, T));
    }
    function frame(im, e) {                                   // the phone: object-position so the face (e.fx across the still) sits at the middle of the box; cleared over 700 px
      if (!small) { im.style.objectPosition = ""; im.style.removeProperty("--v4l1-land"); return; }
      if (small) {                                            // the portrait crop: eyes in the upper third; the dark steers off the side the face is not on
        im.style.objectPosition = "50% 32%"; var fx = e && typeof e.fx === "number" ? e.fx : .5;
        if (bgs.indexOf(im) >= 0) im.style.setProperty("--v4l1-land", landing(e) + "px");   // used until the masthead folds; folded, the still sits at -12 px as before
        bgEl.classList.toggle("is-vl", fx > .58); bgEl.classList.toggle("is-vr", fx < .42); return;
      }
      var bw = bgEl.clientWidth, bh = bgEl.clientHeight, iw = bh * 4 / 3, fx = e && typeof e.fx === "number" ? e.fx : .5, p = iw > bw ? clamp((fx * iw - bw / 2) / (iw - bw), 0, 1) : .5;
      im.style.objectPosition = (p * 100).toFixed(1) + "% 50%";
    }
    function prepBg(e) {                                      // the phone: the next still into the hidden image before a slide, so the swap at its end is a cut
      var want = wide(e), on = bgs[bgOn], off = bgs[1 - bgOn]; if (!want || on.getAttribute("src") === want) return Promise.resolve();
      frame(off, e); return new Promise(function (ok) { if (off.getAttribute("src") !== want) { off.onload = null; off.setAttribute("src", want); } if (off.complete && off.naturalWidth) ok(); else { off.addEventListener("load", ok, { once: true }); off.addEventListener("error", ok, { once: true }); setTimeout(ok, 400); } });
    }
    function showBg(e, cut) {                                  // cut: the phone's slide has already moved the picture; the swap is instant, no fade, no pull-back
      var want = wide(e);
      var on = bgs[bgOn], off = bgs[1 - bgOn]; if (!want) { on.classList.remove("is-on"); return; }
      if (on.getAttribute("src") === want) { on.classList.add("is-on"); return; }
      frame(off, e); var seq = ++bgSeq, done = false; off.onload = function () {
        if (seq !== bgSeq || done) return; done = true;
        if (cut) { bgEl.classList.add("is-cut"); if (off.getAnimations) off.getAnimations().forEach(function (a) { a.cancel(); }); }
        off.classList.add("is-on"); on.classList.remove("is-on"); bgOn = 1 - bgOn;
        if (cut) { void off.offsetWidth; bgEl.classList.remove("is-cut"); return; }
        if (!calm && off.animate) { off.getAnimations().forEach(function (a) { a.cancel(); }); off.animate([{ transform: "scale(1.16)" }, { transform: "scale(1.03)" }], { duration: 7000, easing: "cubic-bezier(.2,.7,.2,1)", fill: "forwards" }); }
      };
      if (off.getAttribute("src") !== want) off.setAttribute("src", want); if (off.complete && off.naturalWidth) off.onload();
    }
    /* still: after a while without a hand on the page, the hero turns through the five most watched, one every few seconds; any touch, key or scroll holds it.
       The clock is armed from the rest frame of the arrival, not from load, and waits 14 s after a clip. */
    var TOP = D.top || [], topI = -1, lastAct = performance.now(), idleT = 0, heroSeen = true, ahead = "";
    function armIdle() {
      clearTimeout(idleT); if (!TOP.length || calm) return; idleT = setTimeout(idleTurn, 6000);
      // the next still only, not the five: the one the turn will show
      var k = (topI + 1) % TOP.length; if (TOP[k] === cur) k = (k + 1) % TOP.length; var e = bySlug[TOP[k]], w = e ? wide(e) : "";
      if (w && w !== ahead) { ahead = w; var im = new Image(); im.decoding = "async"; im.src = w; }
    }
    function idleTurn() {
      if (document.hidden || !heroSeen || hot || arriving || V.st === "playing" || V.st === "loading" || performance.now() - lastAct < 5500) { armIdle(); return; }
      topI = (topI + 1) % TOP.length; if (TOP[topI] === cur) topI = (topI + 1) % TOP.length; show(TOP[topI]); armIdle();
    }
    function acted() { lastAct = performance.now(); }
    ["pointerdown", "keydown", "wheel", "touchstart"].forEach(function (ev) { hero.addEventListener(ev, acted, { passive: true }); });
    if (plot) plot.addEventListener("pointermove", acted, { passive: true });      // a hand over the ridge holds the turn; a pointer elsewhere does not
    window.addEventListener("scroll", acted, { passive: true });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { heroSeen = es.some(function (x) { return x.isIntersecting; }); }, { threshold: 0.35 }).observe(hero);

    /* ---------- the voice: a press plays the guest saying the sentence. Nothing is fetched or played before the press. ----------
       With a clip: the label dissolves, the clip is fetched and decoded, its real envelope is drawn (2 px columns at 3 px pitch, a hairline playhead), the trace wakes
       left to right behind a soft front over 320 ms, the light leaves everything but the sentence and the line (the hero's is-voice numbers, 900 ms), live amplitude lifts
       ten columns around the playhead. At the end the trace sleeps over 600 ms, the light returns over 1200 ms, and 350 ms later "Keep listening from mm:ss" floats in
       where "Open the episode" sat. Without a clip, or when one does not come within 4 s: the label reads "Read it at mm:ss in the episode" and a press opens it. */
    var AC = window.AudioContext || window.webkitAudioContext, DPR = Math.min(2, window.devicePixelRatio || 1), PITCH = 3, PAD = small ? 10 : 12;
    var V = { st: "rest", e: null, ctx: null, buf: null, env: null, src: null, an: null, t0: 0, dur: 0, raf: 0, seq: 0, cache: {}, wake: 0, sleep: 0, loadT: 0, keepT: 0, slow: 0, tdata: null };
    function sayText(e) { return "Hear " + (e.p || "them") + " say it"; }
    function voiceRow(e) {                                     // the row for a voice, at rest
      stopClip(); V.e = e; V.st = "rest"; V.env = null; V.fake = null; var c = V.cache[e.s]; V.buf = c ? c.buf : null;
      hero.classList.remove("is-voice", "is-done"); hear.classList.remove("is-live"); keep.hidden = true;
      var secs = V.buf ? V.buf.duration : e.cl;
      sayT.textContent = sayText(e); sayAt.textContent = e.a ? "at " + e.a : ""; sayLen.textContent = e.c && secs ? Math.round(secs) + " s" : "";
      hear.setAttribute("aria-label", sayText(e) + (e.a ? " at " + e.a : "") + (e.c ? (secs ? ", a clip of " + Math.round(secs) + " seconds" : "") : ", in the episode"));
      if (e.c) hear.setAttribute("data-clip", e.c); else hear.removeAttribute("data-clip");
      keep.href = epUrl(e.s); keep.querySelector(".v4l1-keep-at").hidden = !e.a; if (e.a) keep.querySelector("b").textContent = e.a;
      draw();
    }
    function readState() {                                     // no clip, or one that did not come: the row points into the episode
      var e = V.e; stopClip(); V.st = "read"; hero.classList.remove("is-voice", "is-done"); hear.classList.remove("is-live");
      var t = e.a ? "Read it at " + e.a + " in the episode" : "Read it in the episode";
      sayT.textContent = t; var i = document.createElement("i"); i.textContent = "→"; sayT.appendChild(i); sayAt.textContent = ""; sayLen.textContent = "";
      hear.setAttribute("aria-label", t); draw();
    }
    function stopClip() {
      V.seq++; clearTimeout(V.loadT); clearTimeout(V.keepT);
      try { if (V.src) { V.src.onended = null; V.src.stop(); } } catch (x) {} V.src = null; V.an = null;
      if (V.raf) cancelAnimationFrame(V.raf); V.raf = 0;
    }
    function startClip(e) {
      var seq = ++V.seq;
      try { V.ctx = V.ctx || new AC(); if (V.ctx.state === "suspended") V.ctx.resume(); } catch (x) { readState(); return; }
      V.st = "loading"; V.slow = performance.now(); hero.classList.remove("is-done"); hero.classList.add("is-voice");
      hear.classList.add("is-live"); if (!calm) ring.animate([{ transform: "scale(1)" }, { transform: "scale(.94)", offset: .3 }, { transform: "scale(1)" }], { duration: 260, easing: EASE });
      if (document.fonts && document.fonts.load) document.fonts.load('11px "DM Mono"', "0123456789:").catch(function () {});
      V.loadT = setTimeout(function () { if (seq === V.seq && V.st === "loading") readState(); }, 4000);
      var ready = V.cache[e.s] ? Promise.resolve(V.cache[e.s].buf) : fetch(FILES + e.c).then(function (r) { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); }).then(function (ab) { return new Promise(function (ok, no) { V.ctx.decodeAudioData(ab, ok, no); }); });
      ready.then(function (buf) { if (seq !== V.seq) return; clearTimeout(V.loadT); V.cache[e.s] = { buf: buf }; V.buf = buf; playBuf(buf); }, function () { if (seq === V.seq) readState(); });
      loop();
    }
    function playBuf(buf) {
      var ctx = V.ctx, seq = V.seq, src = ctx.createBufferSource(), an = ctx.createAnalyser(); an.fftSize = 512; src.buffer = buf; src.connect(an); an.connect(ctx.destination);
      V.st = "playing"; V.dur = buf.duration; V.env = null; V.src = src; V.an = an; V.tdata = new Uint8Array(an.fftSize); V.wake = performance.now();
      V.t0 = ctx.currentTime + 0.2; src.start(V.t0);          // the voice begins as the trace finishes waking
      sayLen.textContent = Math.round(buf.duration) + " s";
      src.onended = function () { if (seq === V.seq && V.st === "playing") endClip(); };
      live.textContent = "Playing the clip"; loop();
    }
    function endClip() {
      var e = V.e; if (!e) return; stopClip();
      V.st = "done"; V.sleep = performance.now(); hear.classList.remove("is-live");
      hero.classList.remove("is-voice"); hero.classList.add("is-done");
      sayT.textContent = "Hear it again"; sayAt.textContent = e.a || ""; sayLen.textContent = ""; hear.setAttribute("aria-label", "Hear it again" + (e.a ? ", at " + e.a : ""));
      lastAct = performance.now() + 7000;                      // the idle turn waits 14 s after the clip
      V.keepT = setTimeout(function () {
        keep.hidden = false; if (!calm) keep.animate([{ opacity: 0, transform: "translateY(12px)" }, { opacity: 1, transform: "none" }], { duration: 500, easing: EASE });
        live.textContent = "Keep listening from " + (e.a || "the start") + ", in the episode"; draw();
      }, calm ? 300 : 1550);
      loop();
    }
    hear.addEventListener("click", function () {
      var e = V.e; if (!e) return; acted();
      if (V.st === "playing" || V.st === "loading") { endClip(); return; }
      if (!e.c || V.st === "read" || !AC || !window.fetch) { if (V.st !== "read") readState(); location.href = epUrl(e.s); return; }
      startClip(e);
    });
    function envelope(buf, n) {                                // RMS per column of the clip, scaled to its loudest
      var ch = buf.numberOfChannels, L = buf.length, per = L / n, out = new Float32Array(n), mx = 0, data = [], c, i, k;
      for (c = 0; c < ch; c++) data.push(buf.getChannelData(c));
      for (i = 0; i < n; i++) {
        var a = Math.floor(i * per), b = Math.min(L, Math.floor((i + 1) * per)), s = 0, cnt = 0, step = Math.max(1, Math.floor((b - a) / 400));
        for (k = a; k < b; k += step) { for (c = 0; c < ch; c++) { var v = data[c][k]; s += v * v; } cnt += ch; }
        out[i] = cnt ? Math.sqrt(s / cnt) : 0; if (out[i] > mx) mx = out[i];
      }
      if (mx > 0) for (i = 0; i < n; i++) out[i] = Math.min(1, out[i] / mx);
      return out;
    }
    function region(awake) {                                   // the pixels of the row the trace may use: awake, everything right of the ring; asleep, between the words and the way in
      var rb = act.getBoundingClientRect(), rg = ring.getBoundingClientRect(), x0 = rg.right - rb.left + 14, x1 = rb.width;
      if (!awake) {
        var sb = say.getBoundingClientRect(); if (sb.width && getComputedStyle(say).display !== "none") x0 = sb.right - rb.left + 16;
        if (small && sb.width) { var mb = sayM.getBoundingClientRect(); if (mb.width) x0 = mb.right - rb.left + 12; }
        var rt = keep, tb = rt.getBoundingClientRect(); if (!keep.hidden && tb.width && tb.top < rg.bottom && tb.bottom > rg.top && getComputedStyle(rt).display !== "none") x1 = tb.left - rb.left - 16;
      }
      return { x0: Math.round(x0), x1: Math.round(x1), w: rb.width };
    }
    function liveLift() {
      if (!V.an) return 0; V.an.getByteTimeDomainData(V.tdata); var s = 0, n = V.tdata.length;
      for (var i = 0; i < n; i++) { var v = (V.tdata[i] - 128) / 128; s += v * v; }
      return Math.min(1, Math.sqrt(s / n) * 4) * 0.32;
    }
    function fakeEnv(n, s) {                                   // the phone's trace asleep before the clip has ever been fetched: a quiet pattern of the voice's own (from its slug), not its sound; the real envelope takes over after one play
      var x = 7, i; for (i = 0; i < s.length; i++) x = (x * 31 + s.charCodeAt(i)) & 0x7fffffff;
      var out = new Float32Array(n), v = .5; for (i = 0; i < n; i++) { x = (x * 1103515245 + 12345) & 0x7fffffff; var r = (x >>> 8) / 8388608; v = v * .5 + r * .5; out[i] = .28 + .72 * v * (.55 + .45 * Math.abs(Math.sin(i * .23 + x % 7))); }
      return out;
    }
    function draw(now) {
      var w = Math.round(act.getBoundingClientRect().width), h = cv.clientHeight || 76; if (!w) return;
      if (cv.width !== Math.round(w * DPR) || cv.height !== Math.round(h * DPR)) { cv.width = Math.round(w * DPR); cv.height = Math.round(h * DPR); }
      var g = cv.getContext("2d"); g.setTransform(DPR, 0, 0, DPR, 0, 0); g.clearRect(0, 0, w, h);
      now = now || performance.now();
      var awake = V.st === "playing" || V.st === "loading", r = region(awake), span = r.x1 - r.x0, mid = h / 2, TH = h - 2 * PAD; if (span < 24) return;
      var n = Math.floor(span / PITCH), env = V.buf ? (V.env && V.env.length === n ? V.env : (V.env = envelope(V.buf, n))) : null;
      if (!env && small && !awake && V.st === "rest" && V.e && V.e.c) env = V.fake && V.fake.length === n ? V.fake : (V.fake = fakeEnv(n, V.e.s));
      if (small && !awake) { var cb = cv.getBoundingClientRect(), mb2 = sayM.getBoundingClientRect(); if (mb2.height && cb.height) mid = mb2.top + mb2.height / 2 - cb.top; }
      g.font = '11px "DM Mono",ui-monospace,monospace'; g.textBaseline = "top";
      if (V.st === "loading") {
        g.fillStyle = "rgba(201,201,207,.35)"; for (var j = 0; j < n; j++) g.fillRect(r.x0 + j * PITCH, mid, 1, 1);
        if (now - V.slow > 600) { g.fillStyle = "rgba(154,154,163," + (0.5 + 0.4 * Math.sin(now / 240)).toFixed(2) + ")"; g.fillText("loading", r.x0, mid - 6); }
        return;
      }
      var ph = -1, el = 0;
      if (V.st === "playing") { el = clamp(V.ctx.currentTime - V.t0, 0, V.dur); ph = Math.min(n - 1, Math.floor(el / V.dur * n)); }
      var wakeK = V.st === "playing" && !calm ? Math.min(1, (now - V.wake) / 320) : 1, front = wakeK * (span + 40);
      var sleepK = V.st === "done" && !calm ? Math.min(1, (now - V.sleep) / 600) : 1, lift = ph >= 0 ? liveLift() : 0;
      var hmax = awake ? TH * 0.96 : small ? 14 : TH / 3, fade = V.st === "done" ? sleepK : 1;
      for (var i = 0; i < n; i++) {
        var x = r.x0 + i * PITCH, a = env ? env[i] : 0, k = 1;
        if (awake) { k = clamp((front - i * PITCH) / 40, 0, 1); k = k * k * (3 - 2 * k); }
        var hh = env ? Math.max(1, a * hmax * k) : 1;
        if (ph >= 0 && lift && Math.abs(i - ph) <= 5) hh *= 1 + lift * (1 - Math.abs(i - ph) / 6);
        g.fillStyle = awake ? (i <= ph ? "rgba(255,117,23,.9)" : "rgba(201,201,207,.22)") : "rgba(201,201,207," + (0.35 * fade).toFixed(2) + ")";
        g.fillRect(x, mid - hh / 2, env ? 2 : 1, hh);
      }
      if (ph >= 0) {
        var px = r.x0 + ph * PITCH + 1, at = V.e.as || 0; g.fillStyle = "#ff7517"; g.fillRect(px, PAD - 2, 1, TH + 4);
        var tc = fmt(at + el), tw = g.measureText(tc).width; g.fillText(tc, clamp(px + 6, r.x0, r.x1 - tw), 0);
        var te = fmt(at + V.dur), ew = g.measureText(te).width; if (clamp(px + 6, r.x0, r.x1 - tw) + tw < r.x1 - ew - 10) { g.fillStyle = "rgba(201,201,207,.7)"; g.fillText(te, r.x1 - ew, 0); }
      }
    }
    function loop() {
      if (V.raf) cancelAnimationFrame(V.raf);
      V.raf = requestAnimationFrame(function tick(now) {
        V.raf = 0; draw(now);
        var on = V.st === "playing" || V.st === "loading" || (V.st === "done" && now - V.sleep < 650);
        if (on) V.raf = requestAnimationFrame(tick);
      });
    }
    function reframe() { bgs.forEach(function (im) { var s = im.getAttribute("src") || "", e = null; EPS.some(function (x) { if (wide(x) === s) { e = x; return true; } }); if (e) frame(im, e); }); }
    window.addEventListener("resize", function () { draw(); placeStem(); reframe(); if (PH.folded) fitKick(); });
    if (smallMq && smallMq.addEventListener) smallMq.addEventListener("change", function (ev) { small = ev.matches; draw(); placeStem(); reframe(); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { draw(); reframe(); });
    document.addEventListener("visibilitychange", function () { if (document.hidden && (V.st === "playing" || V.st === "loading")) endClip(); });

    function show(s, instant, cut) {                           // the voice: a sentence, a face, a link; cut: the phone's slide has moved the picture already
      var e = bySlug[s]; if (!e || s === cur) return; var l = lines[s];
      if (arriving) restFrame();                               // a change of voice during the arrival lands on the rest frame first
      if (cur && small) fold();                                // the phone: the masthead folds on the first change of voice, by any means, once
      if (cur && lines[cur]) lines[cur].el.classList.remove("is-on");
      if (l) { l.el.classList.add("is-on"); placeDot(dotOn, l); }
      var fill = function () {
        qn.textContent = e.n ? "Episode " + e.n : "Conversation"; qs.textContent = D.shelves[e.sh]; qd.textContent = e.d || "";
        var q = e.q || ""; qt.textContent = q || e.t; qt.classList.toggle("is-title", !q); qt.setAttribute("data-len", q.length > 150 ? "long" : q.length <= 90 ? "short" : "mid");
        qw.innerHTML = "<b></b> <span></span>"; qw.querySelector("b").textContent = e.g || D.shelves[e.sh]; qw.querySelector("span").textContent = (q ? e.t : "") + (e.m ? (q ? " · " : "") + e.m + " min" : ""); 
        if (face) { if (e.i) face.src = still(e); if (facebox) facebox.hidden = !e.i; }
        voiceRow(e); placeStem(s);
        voice.classList.remove("is-swap");
      };
      clearTimeout(swapT); showBg(e, cut);
      var k = STOPS.indexOf(s); pos.classList.toggle("is-off", k < 0); pi.textContent = k >= 0 ? k + 1 : "";    // "voice N of 12" only for the twelve; any other column reads "12 voices"
      if (pim) pim.textContent = k >= 0 ? String(k + 1) : "\u00b7"; navEl.classList.toggle("is-off", k < 0);          // the phone's band: the tick and "N / 12", or a dimmed band and a dot
      ticks.forEach(function (b, i) { b.classList.toggle("is-on", i === k); });
      if (instant || calm) fill(); else { voice.classList.add("is-swap"); swapT = setTimeout(fill, 180); }
      live.textContent = (e.n ? "Episode " + e.n + ", " : "") + (e.g ? e.g + ", " : "") + (e.d || "");
      cur = s;
      if (small) [nearest(1), nearest(-1)].forEach(function (s2) { var w = s2 && bySlug[s2] ? wide(bySlug[s2]) : ""; if (w && !PRE[w]) { PRE[w] = 1; var im = new Image(); im.decoding = "async"; im.src = w; } });   // the neighbours' stills, so a swipe never waits
    }
    /* ---------- the phone: the stem from the voice's column up to the row; the masthead's fold ---------- */
    var PH = { folded: false, sliding: false, peek: null, drag: null, swiped: 0 }, PRE = {};
    function placeStem(s) {
      if (!stem || !small) return; var l = lines[s || cur]; if (!l) { stem.style.height = "0"; return; }
      var pr = plot.getBoundingClientRect(), ar = act.getBoundingClientRect(); if (!pr.height) return;
      var top = Math.round(ar.bottom - pr.top), tip = (l.y - (l.lift || 0)) / H * pr.height;
      stem.style.left = (l.x / 10) + "%"; stem.style.top = top + "px"; stem.style.height = Math.max(0, tip - top).toFixed(1) + "px";
    }
    function fitKick() { if (!kickF) return; kickF.classList.remove("is-short"); if (kickF.scrollWidth > kickF.clientWidth + 1) kickF.classList.add("is-short"); }   // the folded line at 11 px, or just "Episode Library" when it does not fit
    function fold() { if (PH.folded) return; PH.folded = true; fitKick(); hero.classList.add("is-folded"); }
    var arriving = false;
    if (small && bySlug[STOPS[0]] && wide(bySlug[STOPS[0]])) bgs[0].setAttribute("src", wide(bySlug[STOPS[0]]));   // the phone starts on the head crop
    frame(bgs[0], bySlug[STOPS[0]]); show(STOPS[0], true);

    /* ---------- the arrival, once per page load: the still fades in dark and makes one decelerating pull-back while a pool of light lifts the face; the kicker types in;
       rails with ruler ticks and line numbers draw under the sentence's real lines and the words form on them, a tick before each; at the lock the bracket becomes the
       orange quote mark, the episode number turns orange and the words go white; the rails fade; the name line, the chrome and the voice row land (the row last, alone);
       the ridge grows by date and the voice's column lights. Then the rest frame, which is the hero's normal state, and the idle clock is armed from it.
       Reduced motion: a 300 ms fade to the rest frame. Any press or key skips to the rest frame. ---------- */
    var arrAnims = [], arrHud = null, arrText = "", arrDoneT = 0;
    function A(el, kf, o) { var a = el.animate(kf, mix({ fill: "both", easing: EASE }, o)); arrAnims.push(a); return a; }
    function later(el, kf, o) { return A(el, kf, mix({ fill: "forwards" }, o)); }        // a later change of the same property: no backwards fill
    function restFrame() {
      if (!arriving) return; arriving = false; clearTimeout(arrDoneT);
      hero.classList.remove("is-arriving");
      arrAnims.forEach(function (a) { try { a.cancel(); } catch (x) {} }); arrAnims = [];
      if (arrHud && arrHud.parentNode) arrHud.parentNode.removeChild(arrHud); arrHud = null;
      if (arrText) { qt.textContent = arrText; arrText = ""; } qt.style.opacity = "";
      lastAct = performance.now(); armIdle(); draw(); placeStem();
    }
    function skipArrival() { if (!arriving) return; arrAnims.forEach(function (a) { try { a.finish(); } catch (x) {} }); restFrame(); }
    function arrive() {
      arriving = true;
      var img = bgs[bgOn], hasStill = !!img.getAttribute("src") && getComputedStyle(img).display !== "none";
      var waitImg = hasStill && !(img.complete && img.naturalWidth) ? new Promise(function (ok) { img.addEventListener("load", ok, { once: true }); img.addEventListener("error", ok, { once: true }); setTimeout(ok, 1500); }) : Promise.resolve();
      var fonts = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
      hero.addEventListener("pointerdown", skipArrival); hero.addEventListener("keydown", skipArrival); hero.addEventListener("wheel", skipArrival, { passive: true });
      Promise.all([waitImg, fonts]).then(run, run);
      function run() {
        if (!arriving) return;
        var inEl = hero.querySelector(".v4l1-in"), veil = hero.querySelector(".v4l1-veil"), pool = hero.querySelector(".v4l1-pool");
        if (calm) {                                            // reduced motion: the rest frame, in one short fade
          hero.classList.remove("is-arriving"); A(inEl, [{ opacity: 0 }, { opacity: 1 }], { duration: 300 }); if (hasStill) A(img, [{ opacity: 0 }, { opacity: 1 }], { duration: 300 });
          arrDoneT = setTimeout(restFrame, 320); return;
        }
        var cs = getComputedStyle(hero), LUM = parseFloat(cs.getPropertyValue("--v4l1-lum")) || .5, BLUR = (cs.getPropertyValue("--v4l1-blur") || "1.5px").trim();
        function f(b) { return "grayscale(.15) brightness(" + b + ") blur(" + BLUR + ")"; }
        var per = small ? 30 : 38, t0 = 650;
        // the still: one move, the camera stepping back from the face; the light lifts the face, holds, steps down as the words lock, then settles at the rest number
        if (hasStill) {
          A(img, [{ opacity: 0 }, { opacity: 1 }], { duration: 400 });
          A(img, [{ transform: "scale(1.34)" }, { transform: "scale(1.03)" }], { duration: 2800 });
          A(img, [{ filter: f(.30) }, { filter: f(.62), offset: .35 }, { filter: f(.62), offset: .58 }, { filter: f(.45), offset: .77 }, { filter: f(LUM) }], { duration: 2600 });
          A(veil, [{ opacity: 1 }, { opacity: 0 }], { duration: 720 });
          A(pool, [{ opacity: 1 }, { opacity: 1, offset: .7 }, { opacity: 0 }], { duration: 2600 });
        } else { A(veil, [{ opacity: 0 }, { opacity: 0 }], { duration: 1 }); A(pool, [{ opacity: 0 }, { opacity: 0 }], { duration: 1 }); }
        // the readout, first thing on the instrument
        var kEl = hero.querySelector(".v4l1-k"), fb = hero.querySelector(".v4l1-facebox"), topEl = hero.querySelector(".v4l1-top"); A(kEl, [{ opacity: 1 }, { opacity: 1 }], { duration: 1 });
        if (small) {                                           // the phone: the masthead lands first, kicker, title, numbers, within 500 ms
          A(topEl, [{ opacity: 1 }, { opacity: 1 }], { duration: 1 });
          [".v4l1-kick", ".v4l1-h1", ".v4l1-sum"].forEach(function (c, i) { var el = topEl.querySelector(c); if (el) A(el, [{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "none" }], { duration: 300, delay: i * 100 }); });
        } else {
          if (fb) A(fb, [{ opacity: 0 }, { opacity: 1 }], { duration: 400, delay: 380 });
          [].slice.call(kEl.children).forEach(function (el, i) { A(el, [{ opacity: 0, transform: "translateY(4px)" }, { opacity: 1, transform: "none" }], { duration: 300, delay: 380 + i * 130 }); });
        }
        // the sentence: words in plain inline spans, so the lines break exactly as the text does; the rails are measured from them
        arrText = qt.textContent; qt.textContent = "";
        var words = arrText.split(/\s+/).filter(Boolean).map(function (w, i) { var s = document.createElement("span"); s.className = "v4l1-w"; s.innerHTML = "<i></i>"; s.appendChild(document.createTextNode(w)); if (i) qt.appendChild(document.createTextNode(" ")); qt.appendChild(s); return s; });
        qt.style.opacity = "1";
        var qr = qt.getBoundingClientRect(), lns = [];
        words.forEach(function (w) { var r = w.getBoundingClientRect(), top = r.top - qr.top, L = null; for (var k = 0; k < lns.length; k++) if (Math.abs(lns[k].top - top) < 4) L = lns[k]; if (!L) { L = { top: top, h: r.height, words: [] }; lns.push(L); } L.words.push(w); });
        var hud = document.createElement("span"); hud.className = "v4l1-hud"; qt.appendChild(hud); arrHud = hud;
        var colW = qt.clientWidth, idx = 0, curKF = [];
        var curEl = document.createElement("span"); curEl.className = "v4l1-cur"; curEl.style.left = (small ? -12 : -18) + "px"; curEl.style.height = (lns[0].h * .78) + "px"; hud.appendChild(curEl);
        lns.forEach(function (L, i) {
          var rail = document.createElement("span"); rail.className = "v4l1-rail"; rail.innerHTML = "<u></u>"; rail.style.top = (L.top + L.h * .86) + "px"; rail.style.width = colW + "px"; hud.appendChild(rail);
          var rs = Math.max(0, t0 + idx * per - 220);
          A(rail, [{ transform: "scaleX(0)" }, { transform: "scaleX(1)" }], { duration: 460, delay: rs });
          var no = document.createElement("span"); no.className = "v4l1-rno"; no.textContent = (i < 9 ? "0" : "") + (i + 1);
          if (small) { no.style.right = "0"; no.style.top = (L.top + L.h * .86 - 13) + "px"; } else { no.style.left = (colW + 14) + "px"; no.style.top = (L.top + L.h * .86 - 5) + "px"; }
          hud.appendChild(no); A(no, [{ opacity: 0 }, { opacity: 1 }], { duration: 200, delay: rs + 320 });
          L.rail = rail; L.no = no; curKF.push({ t: t0 + idx * per, top: L.top + L.h * .1 });
          L.words.forEach(function (w) {
            var d = t0 + idx * per; idx++;
            A(w.firstChild, [{ opacity: 0 }, { opacity: 1, offset: .2 }, { opacity: 1, offset: .55 }, { opacity: 0 }], { duration: 300, delay: d - 130, easing: "linear" });
            A(w, [{ opacity: 0, top: "5px", color: "#9a9aa3" }, { opacity: 1, top: "0px", color: "#c9c9cf" }], { duration: 320, delay: d });
          });
        });
        var tEnd = t0 + idx * per, lock = tEnd + 90;
        // the bracket marks the line being written, then returns to the first line and becomes the quote mark
        var cKF = [{ opacity: 0, top: curKF[0].top + "px", offset: 0 }, { opacity: 1, top: curKF[0].top + "px", offset: Math.max(0, (curKF[0].t - 120) / lock) }];
        curKF.forEach(function (k) { cKF.push({ opacity: 1, top: k.top + "px", offset: k.t / lock }); }); cKF.push({ opacity: 1, top: curKF[0].top + "px", offset: 1 }); cKF.forEach(function (k) { k.easing = "steps(1,end)"; });
        A(curEl, cKF, { duration: lock, easing: "linear" }); later(curEl, [{ opacity: 1 }, { opacity: 0 }], { duration: 200, delay: lock + 60 });
        try { arrAnims.push(qt.animate([{ opacity: 0 }, { opacity: 1 }], { pseudoElement: "::before", duration: 360, delay: lock, fill: "both", easing: EASE })); } catch (x) {}
        words.forEach(function (w) { later(w, [{ color: "#c9c9cf" }, { color: "#f6f4f4" }], { duration: 500, delay: lock }); });
        A(qn, [{ color: "#c9c9cf" }, { color: "#c9c9cf", offset: lock / (lock + 300) }, { color: "#ff7517" }], { duration: lock + 300 });
        lns.forEach(function (L, i) { later(L.rail, [{ opacity: 1 }, { opacity: 0 }], { duration: 420, delay: lock + 100 + i * 70 }); later(L.no, [{ opacity: 1 }, { opacity: 0 }], { duration: 300, delay: lock + 100 + i * 70 }); });
        // then the rest of the page comes online, quietly: the name line, the chrome, the voice row last and alone
        function up(el, d, dur) { return A(el, [{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "none" }], { duration: dur || 460, delay: d }); }
        if (small) { up(qw, lock + 330); [].slice.call(kEl.children).forEach(function (el, i) { A(el, [{ opacity: 0, transform: "translateY(4px)" }, { opacity: 1, transform: "none" }], { duration: 300, delay: lock + 450 + i * 90 }); }); up(act, lock + 600); up(navEl, lock + 700); }
        else { up(qw, lock + 330); up(topEl, lock + 520); up(navEl, lock + 520); up(act, lock + 800); }
        // the ridge rises by date, left to right, over about 700 ms; then the voice's column lights
        var rStart = lock + 800, n = order.length;
        A(svg, [{ opacity: 0 }, { opacity: 1 }], { duration: 1, delay: rStart });
        A(lines._area, [{ opacity: 0 }, { opacity: 1 }], { duration: 500, delay: rStart + 300 }); A(path, [{ opacity: 0 }, { opacity: 1 }], { duration: 500, delay: rStart + 400 });
        order.forEach(function (s, k) { A(lines[s].el, [{ transform: "scaleY(0)" }, { transform: "scaleY(1)" }], { duration: 400, delay: rStart + k * (300 / n) }); });
        up(hero.querySelector(".v4l1-ridge-top"), rStart + 100); up(axis, rStart + 400); up(hero.querySelector(".v4l1-key"), rStart + 500);
        if (cur && lines[cur]) A(lines[cur].el, [{ stroke: "#c9c9cf", strokeWidth: 2 }, { stroke: "#ff7517", strokeWidth: 3 }], { duration: 400, delay: rStart + 650 });
        A(dotOn, [{ opacity: 0 }, { opacity: 1 }], { duration: 300, delay: rStart + 750 });
        if (small && stem) { placeStem(); A(stem, [{ opacity: 0 }, { opacity: 1 }], { duration: 300, delay: rStart + 650 }); }
        arrDoneT = setTimeout(restFrame, rStart + 1100);
      }
    }
    if (window.Element && Element.prototype.animate && window.Promise) arrive(); else { hero.classList.remove("is-arriving"); armIdle(); }

    // previous and next voice: along the marked path, from wherever the visitor is
    function nearest(dir) {
      var x = lines[cur] ? lines[cur].x : -1, best = -1;
      STOPS.forEach(function (s, k) { var lx = lines[s].x; if (dir > 0 ? lx > x + 0.01 : lx < x - 0.01) { if (best < 0 || (dir > 0 ? lx < lines[STOPS[best]].x : lx > lines[STOPS[best]].x)) best = k; } });
      if (best < 0) best = dir > 0 ? 0 : STOPS.length - 1;
      return STOPS[best];
    }
    qt.addEventListener("click", function () { if (cur && !arriving && performance.now() - PH.swiped > 400) location.href = epUrl(cur); });   // the sentence itself is a way into the episode (a swipe is not a tap)
    qw.addEventListener("click", function () { if (cur && !arriving) location.href = epUrl(cur); });   // so is the name line
    // and so is the still behind: a press on the open ground of the hero's picture side, away from any control
    function onStill(ev) { if (ev.target.closest("a,button,input,.v4l1-plot,.v4l1-ridge,.v4l1-act,.v4l1-nav,.v4l1-qt,.v4l1-qw,.v4l1-count,.v4l1-top")) return false; var r = hero.getBoundingClientRect(); return ev.clientX >= r.left + r.width * (small ? 0 : 0.32); }
    hero.addEventListener("pointermove", function (ev) { hero.classList.toggle("is-overstill", !small && onStill(ev)); });
    hero.addEventListener("click", function (ev) { if (onStill(ev) && cur && !arriving && !small) location.href = epUrl(cur); });
    hero.querySelector(".v4l1-prev").addEventListener("click", function () { if (small) slide(-1, nearest(-1), 0); else show(nearest(-1)); });
    hero.querySelector(".v4l1-next").addEventListener("click", function () { if (small) slide(1, nearest(1), 0); else show(nearest(1)); });
    /* ---------- the phone: a horizontal swipe on the picture or the sentence moves to the previous or next of the twelve; the face and the words move as one card.
       A drag follows the finger with the neighbour's card beside it; past a quarter of the width it commits, under it snaps back. 380 ms on the one easing, a 60 ms crossfade at each end. ---------- */
    function lenOf(q) { return q.length > 150 ? "long" : q.length <= 90 ? "short" : "mid"; }
    function makePeek(e) {                                     // the neighbour's card: its still (already in the cache) and its sentence, styled exactly as the real one
      var p = document.createElement("div"); p.className = "v4l1-peek"; p.setAttribute("aria-hidden", "true");
      var b = document.createElement("div"); b.className = "v4l1-bg"; var im = document.createElement("img"); im.className = "is-on"; im.alt = ""; own(im); im.src = wide(e); frame(im, e); b.appendChild(im);
      var fog = document.createElement("span"); fog.className = "v4l1-fog"; b.appendChild(fog);
      var q = document.createElement("p"); q.className = "v4l1-qt" + (e.q ? "" : " is-title"); q.setAttribute("data-len", lenOf(e.q || "")); q.textContent = e.q || e.t;
      p.appendChild(b); p.appendChild(q); hero.appendChild(p); p._s = e.s;
      p._ready = Promise.all([im.decode ? im.decode().catch(function () {}) : null, prepBg(e)]);
      return p;
    }
    function killPeek() { if (PH.peek && PH.peek.parentNode) PH.peek.parentNode.removeChild(PH.peek); PH.peek = null; }
    function cancelAnims(el) { if (el.getAnimations) el.getAnimations().forEach(function (a) { a.cancel(); }); }
    function setCard(x) { var tr = x ? "translateX(" + x + "px)" : ""; bgEl.style.transform = tr; qt.style.transform = tr; }
    function slide(dir, to, from) {                            // dir 1: the cards move left (next); -1: right (previous)
      var e = bySlug[to]; if (!e || PH.sliding || !small) return; if (to === cur) return; acted(); if (arriving) skipArrival();
      var W = hero.clientWidth, endX = -dir * W, peek = PH.peek && PH.peek._s === to ? PH.peek : (killPeek(), PH.peek = makePeek(e)), pFrom = from + dir * W;
      var dur = calm ? 0 : Math.max(160, Math.round(380 * Math.abs(endX - from) / W)), x = Math.min(1, 60 / Math.max(1, dur));
      PH.sliding = true; hero.classList.add("is-sliding");
      peek._ready.then(function () {
        if (!PH.sliding) return;
        var o = { duration: dur, easing: EASE, fill: "forwards" }, kf = [{ transform: "translateX(" + from + "px)", opacity: 1 }, { opacity: 1, offset: 1 - x }, { transform: "translateX(" + endX + "px)", opacity: 0 }];
        var a = bgEl.animate(kf, o); qt.animate(kf, o);
        peek.animate([{ transform: "translateX(" + pFrom + "px)", opacity: 0 }, { opacity: 1, offset: x }, { transform: "translateX(0px)", opacity: 1 }], o);
        var end = function () { if (!PH.sliding) return; show(to, true, true); cancelAnims(bgEl); cancelAnims(qt); setCard(0); killPeek(); PH.sliding = false; hero.classList.remove("is-sliding"); };
        if (dur) a.onfinish = end; else end();
      });
    }
    function snapBack(dx, dir) {
      var W = hero.clientWidth, peek = PH.peek, dur = calm ? 0 : 220, o = { duration: dur, easing: EASE, fill: "forwards" };
      PH.sliding = true; var a = bgEl.animate([{ transform: "translateX(" + dx + "px)" }, { transform: "translateX(0px)" }], o); qt.animate([{ transform: "translateX(" + dx + "px)" }, { transform: "translateX(0px)" }], o);
      if (peek) peek.animate([{ transform: "translateX(" + (dx + dir * W) + "px)" }, { transform: "translateX(" + (dir * W) + "px)" }], o);
      var end = function () { cancelAnims(bgEl); cancelAnims(qt); setCard(0); killPeek(); PH.sliding = false; };
      if (dur) a.onfinish = end; else end();
    }
    function cardHit(ev) {
      if (!small || PH.sliding || !ev.isPrimary) return false; var t = ev.target;
      if (t.closest && t.closest("button,a,input,.v4l1-plot,.v4l1-ridge,.v4l1-act,.v4l1-nav,.v4l1-qw,.v4l1-k")) return false;
      return ev.clientY - hero.getBoundingClientRect().top < bgEl.offsetHeight;
    }
    hero.addEventListener("pointerdown", function (ev) { if (!cardHit(ev)) return; PH.drag = { id: ev.pointerId, x: ev.clientX, y: ev.clientY, dx: 0, on: false, dir: 0, to: "" }; });
    hero.addEventListener("pointermove", function (ev) {
      var d = PH.drag; if (!d || ev.pointerId !== d.id) return;
      var dx = ev.clientX - d.x, dy = ev.clientY - d.y;
      if (!d.on) {
        if (Math.abs(dy) > 8 && Math.abs(dy) >= Math.abs(dx)) { PH.drag = null; return; } if (Math.abs(dx) < 8) return;
        d.on = true; if (arriving) skipArrival(); try { hero.setPointerCapture(d.id); } catch (x) {}
      }
      if (ev.cancelable) ev.preventDefault(); d.dx = dx; var dir = dx < 0 ? 1 : -1;
      if (dir !== d.dir) { d.dir = dir; d.to = nearest(dir); killPeek(); if (d.to && d.to !== cur) PH.peek = makePeek(bySlug[d.to]); }
      setCard(dx); if (PH.peek) PH.peek.style.transform = "translateX(" + (dx + dir * hero.clientWidth) + "px)";
    });
    function dragEnd(ev) {
      var d = PH.drag; if (!d || ev.pointerId !== d.id) return; PH.drag = null; if (!d.on) return; PH.swiped = performance.now(); acted();
      if (Math.abs(d.dx) >= hero.clientWidth * .25 && d.to && d.to !== cur) slide(d.dir, d.to, d.dx); else snapBack(d.dx, d.dir);
    }
    hero.addEventListener("pointerup", dragEnd); hero.addEventListener("pointercancel", dragEnd);
    // a column answers the pointer: the guest at its tip, and the voice swaps
    function placeTip(l, e) {
      tip.hidden = false; tip.querySelector("b").textContent = e.g || e.t; tip.querySelector("span").textContent = (e.n ? "Episode " + e.n : "") + (e.d ? " · " + e.d : "") + (e.m ? " · " + e.m + " min" : "");
      if (tip._s !== l.e.s) { tip._s = l.e.s; tip.classList.add("is-in"); requestAnimationFrame(function () { tip.classList.remove("is-in"); }); }
      if (!WAVE || wave.x < 0) { var pw = plot.clientWidth, tw = tip.offsetWidth; tip.style.left = clamp(l.x / 1000 * pw, tw / 2 + 2, pw - tw / 2 - 2).toFixed(0) + "px"; }
    }
    function hover(s) {
      if (hot && lines[hot]) lines[hot].el.classList.remove("is-hot"); hot = s;
      if (!s) { tip.hidden = true; dotHot.classList.remove("is-on"); return; }
      var l = lines[s]; l.el.classList.add("is-hot"); placeDot(dotHot, l); dotHot.classList.toggle("is-on", s !== cur); placeTip(l, l.e);
    }
    function slugAt(ev) { var t = ev.target; return t && t.tagName === "line" ? t.getAttribute("data-s") : ""; }
    /* the wave: the columns near the pointer rise, most under it, less to each side; the crest follows the pointer with a little lag and settles when it leaves */
    var WAVE = !calm, wave = { x: -1, tx: -1, amp: 0, tamp: 0, raf: 0 }, SIG = 46;
    var glow = document.createElement("div"); glow.className = "v4l1-glow"; var glowC = document.createElement("div"); glowC.className = "v4l1-glow-c"; plot.insertBefore(glowC, svg); plot.insertBefore(glow, svg);
    function nearestAt(px) { var best = "", bd = 1e9; for (var k = 0; k < order.length; k++) { var d = Math.abs(lines[order[k]].x - px); if (d < bd) { bd = d; best = order[k]; } } return bd < 18 ? best : ""; }
    function waveTick() {
      wave.raf = 0; if (wave.x < 0) wave.x = wave.tx;
      wave.x += (wave.tx - wave.x) * 0.16; wave.amp += (wave.tamp - wave.amp) * 0.14;
      var done = Math.abs(wave.tamp - wave.amp) < 0.004 && Math.abs(wave.tx - wave.x) < 0.05;
      if (done && wave.tamp === 0) { wave.amp = 0; wave.x = -1; }
      for (var k = 0; k < order.length; k++) {
        var l = lines[order[k]], d = (l.x - (wave.x < 0 ? -1e9 : wave.x)) / SIG, g = wave.amp * Math.exp(-d * d), lift = g * (0.22 * (H - l.y) + 16);
        l.lift = lift; l.el.setAttribute("y2", (l.y - lift).toFixed(1)); l.el.style.strokeOpacity = g > 0.02 ? Math.min(1, 0.55 + 0.45 * g).toFixed(3) : "";
      }
      if (hot && lines[hot]) { var lh = lines[hot]; dotHot.style.top = ((lh.y - lh.lift) / H * 100) + "%"; }
      if (!tip.hidden) { var pw = plot.clientWidth, tw = tip.offsetWidth || 160; tip.style.left = clamp(wave.x / 1000 * pw, tw / 2 + 2, pw - tw / 2 - 2).toFixed(1) + "px"; }
      if (cur && lines[cur]) { var lc = lines[cur]; dotOn.style.top = ((lc.y - lc.lift) / H * 100) + "%"; if (small) placeStem(); }
      glow.style.left = glowC.style.left = (wave.x < 0 ? 0 : wave.x / 10) + "%"; glow.style.opacity = wave.amp.toFixed(3); glowC.style.opacity = (wave.amp * 0.9).toFixed(3);
      if (!done) wave.raf = requestAnimationFrame(waveTick);
    }
    function waveAt(px) { wave.tx = px; wave.tamp = 1; if (!wave.raf) wave.raf = requestAnimationFrame(waveTick); }
    function waveOff() { wave.tamp = 0; if (!wave.raf) wave.raf = requestAnimationFrame(waveTick); }
    var touching = false;
    svg.addEventListener("pointermove", function (ev) {
      if (ev.pointerType === "touch" && !touching) return;
      if (arriving) skipArrival();
      var rw = svg.getBoundingClientRect(), px = (ev.clientX - rw.left) / rw.width * 1000;
      if (WAVE) waveAt(px);
      var s = slugAt(ev) || nearestAt(px); if (!s || s === hot) return;
      hover(s); clearTimeout(hoverT); hoverT = setTimeout(function () { show(s); dotHot.classList.remove("is-on"); }, 70);
    });
    var overTip = false, leaveT = 0;
    svg.addEventListener("pointerleave", function () { if (touching) return; clearTimeout(hoverT); clearTimeout(leaveT); leaveT = setTimeout(function () { if (overTip) return; hover(""); if (WAVE) waveOff(); }, 120); });
    // the label is a way in: a hand on it keeps it, a press opens the episode it names
    tip.addEventListener("pointerenter", function () { overTip = true; clearTimeout(leaveT); });
    tip.addEventListener("pointerleave", function () { overTip = false; leaveT = setTimeout(function () { if (!overTip) { hover(""); if (WAVE) waveOff(); } }, 120); });
    tip.addEventListener("click", function () { if (tip._s) location.href = epUrl(tip._s); });
    /* a finger: drag along the ridge and the wave and the voice follow; lift it and the wave settles, the voice stays */
    svg.addEventListener("pointerdown", function (ev) { if (ev.pointerType !== "touch") return; touching = true; try { svg.setPointerCapture(ev.pointerId); } catch (e) {}
      var rw = svg.getBoundingClientRect(), px = (ev.clientX - rw.left) / rw.width * 1000; if (WAVE) waveAt(px); var s = nearestAt(px); if (s) { hover(s); show(s); dotHot.classList.remove("is-on"); } });
    function touchEnd(ev) { if (ev.pointerType !== "touch" || !touching) return; touching = false; clearTimeout(hoverT); if (WAVE) waveOff(); setTimeout(function () { if (!touching) hover(""); }, 900); }
    svg.addEventListener("pointerup", touchEnd); svg.addEventListener("pointercancel", touchEnd);
    svg.addEventListener("click", function (ev) {
      var s = slugAt(ev); if (!s) return; clearTimeout(hoverT);
      if (s === cur && !small) { location.href = epUrl(s); return; }
      show(s); hover(s);
    });
    // the keyboard: arrows walk the columns by date, Enter opens the one in view
    plot.addEventListener("keydown", function (ev) {
      var k = order.indexOf(cur), n = order.length, to = -1;
      if (ev.key === "ArrowRight" || ev.key === "ArrowDown") to = Math.min(n - 1, k + 1); else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") to = Math.max(0, k - 1);
      else if (ev.key === "Home") to = 0; else if (ev.key === "End") to = n - 1; else if (ev.key === "PageDown") { ev.preventDefault(); show(nearest(1)); hover(cur); return; } else if (ev.key === "PageUp") { ev.preventDefault(); show(nearest(-1)); hover(cur); return; }
      else if (ev.key === "Enter" && cur) { location.href = epUrl(cur); return; } else return;
      ev.preventDefault(); if (to >= 0) { show(order[to]); hover(order[to]); }
    });
    plot.addEventListener("blur", function () { hover(""); });
    // the key: a shelf lights its columns; a press takes the finder to that shelf
    var lit = null;
    function light(set) { Object.keys(lines).forEach(function (s) { if (s.charAt(0) === "_") return; var on = set ? !!set[s] : false; lines[s].el.classList.toggle("is-dim", !!set && !on); lines[s].el.classList.toggle("is-lit", !!set && on); }); }
    function shelfSet(i) { var set = {}; EPS.forEach(function (e) { if (e.sh === i) set[e.s] = 1; }); return set; }
    [].slice.call(hero.querySelectorAll(".v4l1-ki")).forEach(function (b) {
      var i = +b.getAttribute("data-sh");
      b.addEventListener("pointerenter", function () { light(shelfSet(i)); }); b.addEventListener("focus", function () { light(shelfSet(i)); });
      b.addEventListener("pointerleave", function () { light(lit); }); b.addEventListener("blur", function () { light(lit); });
      b.addEventListener("click", function () { if (filterShelf) filterShelf(i); });
    });
    // the shelves, guests and topics below also light the big ridge when the visitor comes back up
    hero._light = function (set) { lit = set; light(set); [].slice.call(hero.querySelectorAll(".v4l1-ki")).forEach(function (b) { b.classList.toggle("is-on", !!set && set._sh === +b.getAttribute("data-sh")); }); };
  }

  /* ---------- the finder and the rows ---------- */
  var find = document.getElementById("find"), rowsBox = document.getElementById("browse"); if (!find || !rowsBox) return;
  var rows = [].slice.call(rowsBox.querySelectorAll(".v4l-row")), more = rowsBox.querySelector(".v4l-more"), none = rowsBox.querySelector(".v4l-none"), filt = rowsBox.querySelector(".v4l-filter"), hn = rowsBox.querySelector(".v4l-hn");
  var mini = rowsBox.querySelector(".v4l-mini svg"), miniLines = drawRidge(mini, 80, 4, null), miniBox = rowsBox.querySelector(".v4l-mini");
  var input = find.querySelector("input"), hits = find.querySelector(".v4l-hits"), sbox = find.querySelector(".v4l-sbox"), sis = [].slice.call(find.querySelectorAll(".v4l-si")), gs = [].slice.call(find.querySelectorAll(".v4l-g")), ts = [].slice.call(find.querySelectorAll(".v4l-t"));
  var F = { sh: -1, g: "", t: "", q: "" }, PAGE = 24, shown = PAGE, HITS = 6;
  /* the search: every word typed must be in the episode's words: its title, guest, tags and quote, and (e.f, from the generator) its chapter titles and summary */
  var U = (function () { try { return new RegExp("[^\\p{L}\\p{N} ]+", "gu"); } catch (x) { return /[^a-z0-9 ]+/g; } })();
  function words(s) { return (s || "").toLowerCase().replace(U, " ").split(" ").filter(Boolean); }
  function hay(e) { return e._f || (e._f = " " + words(e.t + " " + e.g + " " + e.k.join(" ") + " " + e.q).join(" ") + " " + (e.f || "") + " "); }
  function match(e) {
    if (F.sh >= 0 && e.sh !== F.sh) return false;
    if (F.g && e.g !== F.g) return false;
    if (F.t && e.k.indexOf(F.t) < 0) return false;
    if (F.q) { var ws = words(F.q), h = hay(e); for (var i = 0; i < ws.length; i++) if (h.indexOf(ws[i]) < 0) return false; }
    return true;
  }
  /* the state in the address, as the live library writes it: #s=<shelf>, #g=<guest>, #t=<topic>, #q=<words>, joined with &. A press of a shelf, a guest or a topic
     adds a history entry; typing replaces the entry. The live library's #s=<series name> is read as that series' shelf; #all clears. The page's own anchors (#find, #browse) are left alone. */
  function hashOf() { var p = []; if (F.sh >= 0) p.push("s=" + F.sh); if (F.g) p.push("g=" + encodeURIComponent(F.g)); if (F.t) p.push("t=" + encodeURIComponent(F.t)); if (F.q) p.push("q=" + encodeURIComponent(F.q)); return p.length ? "#" + p.join("&") : ""; }
  function writeHash(mode) {
    if (!mode) return; var h = hashOf(); if (location.hash === h || (!h && !location.hash)) return;
    try { history[mode === "push" ? "pushState" : "replaceState"](null, "", h || location.pathname + location.search); } catch (x) {}
  }
  function route(scroll) {                                   // true when the address names a filter (or #all); the filter is then applied from it
    var h = location.hash.replace(/^#/, ""); if (h !== "all" && !/(?:^|&)[sgtq]=/.test(h)) return false;
    function get(k) { var m = new RegExp("(?:^|&)" + k + "=([^&]*)").exec(h); if (!m) return ""; try { return decodeURIComponent(m[1].replace(/\+/g, " ")).trim(); } catch (x) { return ""; } }
    var s = get("s"), g = get("g"), t = get("t"), q = get("q"), sh = -1;
    if (/^\d+$/.test(s) && +s < D.shelves.length) sh = +s; else if (s && D.sx && D.sx[s] !== undefined) sh = D.sx[s];
    if (g && !gs.some(function (b) { return b.getAttribute("data-g") === g; })) g = ""; if (t && !ts.some(function (b) { return b.getAttribute("data-t") === t; })) t = "";
    F = { sh: sh, g: g, t: t, q: q.slice(0, 80) }; input.value = F.q; shown = PAGE; apply(scroll && (sh >= 0 || g || t || q) ? scroll : false, null); return true;
  }
  function heading(on) {                                     // "All 86 conversations"; "17 conversations in Risk and safety"; "No conversations match"
    var parts = [];
    if (F.sh >= 0) parts.push("in " + D.shelves[F.sh]); if (F.g) parts.push("with " + F.g); if (F.t) parts.push("on " + F.t); if (F.q) parts.push("for “" + F.q + "”");
    if (!parts.length) return "All " + on + " conversations";
    return on ? on + " conversation" + (on === 1 ? " " : "s ") + parts.join(" ") : "No conversations match";
  }
  function apply(scroll, hashMode) {
    var on = 0, set = null, any = F.sh >= 0 || F.g || F.t || F.q, top = [];
    if (any) set = {};
    rows.forEach(function (r) { var e = bySlug[r.getAttribute("data-s")], ok = e && match(e); if (ok) { on++; if (set) set[e.s] = 1; if (top.length < HITS) top.push(e); } r.hidden = !ok || on > shown; });
    more.hidden = on <= shown; more.textContent = "Show " + Math.min(PAGE, on - shown) + " more of " + on; none.hidden = on > 0; hn.textContent = heading(on);
    filt.hidden = !any; filt.textContent = ""; if (any) { var b = document.createElement("button"); b.type = "button"; b.textContent = "clear"; b.addEventListener("click", function () { clear("push"); }); filt.appendChild(b); }
    sis.forEach(function (b) { b.classList.toggle("is-on", +b.getAttribute("data-sh") === F.sh); }); gs.forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-g") === F.g); }); ts.forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-t") === F.t); });
    Object.keys(miniLines).forEach(function (s) { if (s.charAt(0) !== "_") miniLines[s].el.classList.toggle("is-lit", !!set && !!set[s]); }); miniBox.classList.toggle("is-filtered", !!set);
    if (set && F.sh >= 0) set._sh = F.sh;
    if (hero && hero._light) hero._light(set);
    showHits(F.q ? top : null, on);
    writeHash(hashMode === undefined ? "replace" : hashMode);
    if (scroll) rowsBox.scrollIntoView({ behavior: scroll === "auto" || calm ? "auto" : "smooth", block: "start" });
  }
  /* the hits: up to six titles under the box while the visitor types, each a way into its episode; Escape, an empty box or leaving the box hides them; the rows below filter as ever */
  function showHits(list, on) {
    if (!hits) return;
    if (!list) { hits.hidden = true; hits.innerHTML = ""; return; }
    hits.innerHTML = "";
    list.forEach(function (e) {
      var a = document.createElement("a"); a.className = "v4l-hit"; a.href = epUrl(e.s);
      var i = document.createElement("i"); i.textContent = e.n || ""; var b = document.createElement("b"); b.textContent = e.t; var sp = document.createElement("span"); sp.textContent = e.g || D.shelves[e.sh];
      a.appendChild(i); a.appendChild(b); a.appendChild(sp); hits.appendChild(a);
    });
    var n = document.createElement("p"); n.className = "v4l-hits-n"; n.textContent = on ? (on === 1 ? "1 conversation, in the rows below" : on + " conversations, " + (on > list.length ? "the first " + list.length + " here, all " : "") + "in the rows below") : "Nothing matches"; hits.appendChild(n);
    hits.hidden = false;
  }
  input.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && hits && !hits.hidden) { ev.preventDefault(); showHits(null); } });
  if (sbox) sbox.addEventListener("focusout", function (ev) { if (!ev.relatedTarget || !sbox.contains(ev.relatedTarget)) setTimeout(function () { if (!sbox.contains(document.activeElement)) showHits(null); }, 120); });
  input.addEventListener("focus", function () { if (F.q && hits && hits.hidden && input.value.trim() === F.q) apply(false, null); });
  function clear(mode) { F = { sh: -1, g: "", t: "", q: "" }; input.value = ""; shown = PAGE; apply(false, mode === undefined ? "push" : mode); }
  sis.forEach(function (b) { b.addEventListener("click", function () { var v = +b.getAttribute("data-sh"); F.sh = F.sh === v ? -1 : v; F.g = ""; F.t = ""; shown = PAGE; apply(true, "push"); }); });
  filterShelf = function (v) { F.sh = v; F.g = ""; F.t = ""; F.q = ""; input.value = ""; shown = PAGE; apply(true, "push"); };
  gs.forEach(function (b) { b.addEventListener("click", function () { var v = b.getAttribute("data-g"); F.g = F.g === v ? "" : v; F.sh = -1; F.t = ""; shown = PAGE; apply(true, "push"); }); });
  ts.forEach(function (b) { b.addEventListener("click", function () { var v = b.getAttribute("data-t"); F.t = F.t === v ? "" : v; F.sh = -1; F.g = ""; shown = PAGE; apply(true, "push"); }); });
  var typing = 0; input.addEventListener("input", function () { clearTimeout(typing); typing = setTimeout(function () { F.q = input.value.trim().slice(0, 80); F.sh = -1; F.g = ""; F.t = ""; shown = PAGE; apply(false, "replace"); }, 180); });
  more.addEventListener("click", function () { shown += PAGE; apply(false, null); });
  window.addEventListener("hashchange", function () { if (!route("smooth")) { var h = location.hash.replace(/^#/, ""); if (!h && (F.sh >= 0 || F.g || F.t || F.q)) clear(null); } });
  var gall = find.querySelector(".v4l-gall"), gbox = find.querySelector(".v4l-guests");            // all the faces, on request
  if (gall && gbox) gall.addEventListener("click", function () {
    var open = !gbox.classList.contains("is-all"); gbox.classList.toggle("is-all", open); gall.setAttribute("aria-expanded", open ? "true" : "false");
    gall.innerHTML = (open ? gall.getAttribute("data-few") : gall.getAttribute("data-all")) + ' <i aria-hidden="true">&darr;</i>';
  });
  /* the shelves: a hand on a row (pointer or keyboard focus) brings its newest conversation's still up behind the list at low opacity; it leaves with the hand.
     The still is fetched on the first hand, not before. */
  var sbd = find.querySelector(".v4l-sbd"), sbdImg = sbd && sbd.querySelector("img"), sbdHot = null, sbdT = 0;
  if (sbd && sbdImg) {
    var isFV = function (b) { try { return b.matches(":focus-visible"); } catch (x) { return false; } };
    var bdOn = function (b) {
      var src = b.getAttribute("data-bd"); clearTimeout(sbdT); sbdHot = b; if (!src) { sbd.classList.remove("is-on"); return; }
      if (sbdImg.getAttribute("src") === BASE + src) { sbd.classList.add("is-on"); return; }
      sbd.classList.remove("is-on"); sbdImg.onload = function () { if (sbdHot === b) sbd.classList.add("is-on"); };
      sbdImg.src = BASE + src; if (sbdImg.complete && sbdImg.naturalWidth) sbdImg.onload();
    };
    var bdOff = function (b) { if (sbdHot !== b) return; sbdHot = null; clearTimeout(sbdT); sbdT = setTimeout(function () { if (!sbdHot) sbd.classList.remove("is-on"); }, 60); };
    sis.forEach(function (b) {
      b.addEventListener("pointerenter", function (ev) { if (ev.pointerType !== "touch") bdOn(b); });
      b.addEventListener("pointerleave", function () { if (!isFV(b)) bdOff(b); });
      b.addEventListener("focus", function () { if (isFV(b)) bdOn(b); });
      b.addEventListener("blur", function () { bdOff(b); });
    });
  }
  /* the films: the inline script after the panel drew four of the pool before first paint (b.v4lDraw); "Another draw" draws again with a short crossfade,
     "Show all" opens the rest in place and the readout follows */
  var fg = rowsBox.querySelector(".v4l-film-g"), fall = rowsBox.querySelector(".v4l-fall"), fdraw = rowsBox.querySelector(".v4l-fdraw"), fn = rowsBox.querySelector(".v4l-fn"), FILM_FIT = 4, fSwap = false;
  function filmsCount() { if (fn && fg) fn.textContent = fg.classList.contains("is-all") ? fg.children.length : Math.min(FILM_FIT, fg.children.length); }
  if (fg && fall) fall.addEventListener("click", function () {
    var open = !fg.classList.contains("is-all"); fg.classList.toggle("is-all", open); fall.setAttribute("aria-expanded", open ? "true" : "false");
    fall.innerHTML = (open ? fall.getAttribute("data-few") : fall.getAttribute("data-all")) + ' <i aria-hidden="true">&darr;</i>'; filmsCount();
  });
  if (fg && fdraw && typeof fg.v4lDraw === "function") fdraw.addEventListener("click", function () {
    if (fSwap) return; fSwap = true;
    var go = function () { fg.v4lDraw(true); fg.classList.remove("is-swap"); filmsCount(); setTimeout(function () { fSwap = false; }, calm ? 0 : 260); };
    if (calm) go(); else { fg.classList.add("is-swap"); setTimeout(go, 230); }
  });
  // the mini ridge: a column answers a touch with the row
  mini.addEventListener("click", function (ev) { var t = ev.target; if (t && t.tagName === "line") location.href = epUrl(t.getAttribute("data-s")); });
  [].slice.call(mini.querySelectorAll("line")).forEach(function (l) { l.style.cursor = "pointer"; var s = l.getAttribute("data-s"), e = bySlug[s]; var tt = document.createElementNS(NS, "title"); tt.textContent = (e.g ? e.g + " · " : "") + e.t; l.appendChild(tt); });
  if (!route("auto")) apply(false, null);
})();
