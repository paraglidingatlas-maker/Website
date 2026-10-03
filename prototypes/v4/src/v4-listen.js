/* LISTENING MODE (prototypes/v4 episode pages; loaded the first time it is
   opened, by v2-immersive.js, so no page carries it on arrival).

   The episode as one screen: the player, the chapter dial, the series'
   drawing and the transcript. While it plays:
     - the line being spoken is lit, and the transcript keeps it in view
       (unless the reader has just scrolled it themselves);
     - the dial's ring of chapters turns so the chapter playing sits at the
       top, and the globe turns with it;
     - the series' drawing draws itself as the episode goes, complete at the
       end.
   Everything comes from the page: the transcript's own timestamps, the
   chapter rail, the header globe, the series mark. The time comes from the
   player: the YouTube embed's own messages (the protocol episode-sync.js
   already speaks), or the audio element.

   The video is not moved (moving an iframe reloads it): it is laid over a
   frame in the listening screen, and goes back when the screen closes.
   Reduced motion: nothing turns or draws, every state is still shown. */
(function () {
  "use strict";
  var d = document, w = window;
  var still = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var player = d.querySelector(".ep2-hero-media .cd-player, .cd-player");
  var lines = [].slice.call(d.querySelectorAll(".cd-line"));
  if (!player || !lines.length) return;
  var frame = player.querySelector("iframe");
  var audio = player.querySelector("audio");
  var au = player.querySelector(".ep-au");

  function secs(t) {
    var p = (t || "").trim().split(":").map(Number);
    if (!p.length || p.some(isNaN)) return null;
    return p.reduce(function (a, b) { return a * 60 + b; }, 0);
  }
  function clock(s) {
    s = Math.max(0, Math.floor(s || 0));
    var h = Math.floor(s / 3600), m = Math.floor(s / 60) % 60, x = s % 60;
    return (h ? h + ":" + (m < 10 ? "0" : "") : "") + m + ":" + (x < 10 ? "0" : "") + x;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---- what the page already says ---- */
  var times = lines.map(function (l) { var t = l.querySelector(".cd-ts"); return t ? secs(t.textContent) : null; });
  var chaps = [].slice.call(d.querySelectorAll(".cd-rail .cd-chap")).map(function (a) {
    var t = a.querySelector("time");
    var title = a.cloneNode(true);
    [].forEach.call(title.querySelectorAll("time, .cd-chap-n, .cd-num"), function (x) { x.remove(); });
    return { id: (a.getAttribute("href") || "").replace("#", ""), at: t ? secs(t.textContent) : null, title: title.textContent.replace(/\s+/g, " ").trim() };
  }).filter(function (c) { return c.at !== null; });
  var lineChap = lines.map(function (l) {
    var b = l.closest(".cd-block");
    for (var k = 0; k < chaps.length; k++) if (b && chaps[k].id === b.id) return k;
    return -1;
  });
  var total = (au && Number(au.getAttribute("data-duration"))) || 0;
  if (!total) {
    // the page's "67 min", read span by span (the date sits right before it)
    [].forEach.call(d.querySelectorAll(".cd-submeta span"), function (sp) {
      var dm = /^\s*(\d+)\s*min\s*$/.exec(sp.textContent);
      if (dm) total = Number(dm[1]) * 60;
    });
  }
  var lastT = times.filter(function (t) { return t !== null; }).pop() || 0;
  if (total < lastT) total = lastT + 30;
  var h1 = d.querySelector(".ep2-h1") || d.querySelector("h1");
  var title = h1 ? h1.textContent.trim() : d.title;

  /* ---- the screen ---- */
  var el = d.createElement("div");
  el.className = "v4-ls" + (frame ? " has-video" : " is-audio");
  el.id = "v4Listen";
  el.hidden = true;
  el.setAttribute("role", "dialog");
  el.setAttribute("aria-modal", "true");
  el.setAttribute("aria-label", "Listening mode: " + title);

  var ring = "", R = 112, C = 130, gap = chaps.length > 1 ? 1.2 : 0;
  var marks = [];
  chaps.forEach(function (c, k) {
    var a0 = c.at / total * 360, a1 = (k + 1 < chaps.length ? chaps[k + 1].at : total) / total * 360;
    var mid = (a0 + a1) / 2;
    marks.push(mid);
    var s = a0 + gap / 2, e = Math.max(s + 0.4, a1 - gap / 2);
    function pt(a) { var r = (a - 90) * Math.PI / 180; return (C + R * Math.cos(r)).toFixed(1) + "," + (C + R * Math.sin(r)).toFixed(1); }
    ring += '<path class="v4-ls-arc" data-k="' + k + '" d="M' + pt(s) + "A" + R + "," + R + " 0 " + (e - s > 180 ? 1 : 0) + " 1 " + pt(e) + '"/>';
  });
  var ticks = "";
  for (var a = 0; a < 360; a += 10) {
    var r0 = (a - 90) * Math.PI / 180, big = a % 30 === 0;
    ticks += "M" + (C + 124 * Math.cos(r0)).toFixed(1) + "," + (C + 124 * Math.sin(r0)).toFixed(1) +
             "L" + (C + (big ? 131 : 128) * Math.cos(r0)).toFixed(1) + "," + (C + (big ? 131 : 128) * Math.sin(r0)).toFixed(1);
  }
  var globe = d.querySelector(".v4-globe");
  var mark = d.querySelector(".v4-series svg");

  el.innerHTML =
    '<div class="v4-ls-in">' +
      '<div class="v4-ls-bar">' +
        '<p class="v4-ls-k">Listening mode</p>' +
        '<p class="v4-ls-t">' + esc(title) + '</p>' +
        '<button type="button" class="v4-ls-x" aria-label="Close listening mode"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg></button>' +
      '</div>' +
      '<div class="v4-ls-stage">' +
        (frame ? '<div class="v4-ls-video" aria-hidden="true"></div>' : '') +
        '<div class="v4-ls-now">' +
          '<div class="v4-ls-dial" aria-hidden="true">' +
            '<div class="v4-ls-globe"></div>' +
            '<svg class="v4-ls-ring" viewBox="0 0 260 260"><path class="v4-ls-ticks" d="' + ticks + '"/><g class="v4-ls-turn">' + ring + '</g><path class="v4-ls-index" d="M130,4L125,14L135,14Z"/></svg>' +
          '</div>' +
          '<div class="v4-ls-chap">' +
            '<p class="v4-ls-chno"></p>' +
            '<p class="v4-ls-chname" aria-live="polite"></p>' +
            '<div class="v4-ls-art" aria-hidden="true"></div>' +
          '</div>' +
        '</div>' +
        '<div class="v4-ls-ctl">' +
          '<button type="button" class="v4-ls-prev" aria-label="Previous chapter"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5v14M18 5l-9 7 9 7z" fill="currentColor"/></svg></button>' +
          '<button type="button" class="v4-ls-play" aria-label="Play"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-play" d="M8 5l12 7-12 7z" fill="currentColor"/><path class="i-pause" d="M7 5h4v14H7zM14 5h4v14h-4z" fill="currentColor"/></svg></button>' +
          '<button type="button" class="v4-ls-next" aria-label="Next chapter"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17 5v14M6 5l9 7-9 7z" fill="currentColor"/></svg></button>' +
          '<p class="v4-ls-time"><span class="v4-ls-cur">0:00</span> / ' + clock(total) + '</p>' +
        '</div>' +
        '<div class="v4-ls-prog" role="group" aria-label="Chapters">' +
          chaps.map(function (c, k) {
            var end = k + 1 < chaps.length ? chaps[k + 1].at : total;
            return '<button type="button" class="v4-ls-seg" data-k="' + k + '" style="flex-grow:' + Math.max(1, end - c.at) + '" aria-label="Play chapter ' + (k + 1) + ': ' + esc(c.title) + '"><i></i></button>';
          }).join("") +
        '</div>' +
      '</div>' +
      '<div class="v4-ls-text" tabindex="-1">' +
        lines.map(function (l, k) {
          var p = l.querySelector("p");
          var head = (lineChap[k] >= 0 && (k === 0 || lineChap[k - 1] !== lineChap[k]))
            ? '<p class="v4-ls-h">' + esc(chaps[lineChap[k]].title) + '</p>' : "";
          return head + '<p class="v4-ls-line" data-k="' + k + '">' + (times[k] !== null ? '<button type="button" class="v4-ls-ts" aria-label="Play from ' + clock(times[k]) + '">' + clock(times[k]) + '</button>' : "") +
                 '<span>' + (p ? p.innerHTML : esc(l.textContent)) + '</span></p>';
        }).join("") +
      '</div>' +
      '<button type="button" class="v4-ls-back" hidden>Back to the voice</button>' +
    '</div>';
  d.body.appendChild(el);

  var $ = function (s) { return el.querySelector(s); };
  if (globe) $(".v4-ls-globe").appendChild(globe.cloneNode(true));
  else el.classList.add("no-globe");
  if (mark) {
    // a faint trace of the whole drawing, and over it the drawing as far as
    // the episode has gone: strokes draw, fills and dashed lines come in
    var ghost = mark.cloneNode(true), art = mark.cloneNode(true);
    ghost.classList.add("v4-ls-ghost");
    $(".v4-ls-art").appendChild(ghost);
    $(".v4-ls-art").appendChild(art);
    [].forEach.call(art.querySelectorAll("rect"), function (r) { r.setAttribute("fill", "none"); });
    [].forEach.call(art.querySelectorAll("path, circle, polyline, line, ellipse"), function (p) {
      var st = p.getAttribute("stroke");
      // a stroke is drawn by its dash, measured in the drawing's own units,
      // so it stops keeping its screen width here (vector-effect)
      if (st && st !== "none" && !p.getAttribute("stroke-dasharray") && !p.classList.contains("fl")) { p.removeAttribute("vector-effect"); p.classList.add("v4-ls-draw"); }
      else p.classList.add("v4-ls-fill");
    });
  }
  var draws = [].slice.call(el.querySelectorAll(".v4-ls-draw")), fills = [].slice.call(el.querySelectorAll(".v4-ls-fill"));
  var text = $(".v4-ls-text"), outLines = [].slice.call(el.querySelectorAll(".v4-ls-line"));
  var segs = [].slice.call(el.querySelectorAll(".v4-ls-seg")), arcs = [].slice.call(el.querySelectorAll(".v4-ls-arc"));

  /* ---- the player ---- */
  var t = 0, playing = false, live = false, origin = "*", lastBeat = 0;
  function send(func, args) {
    if (!frame) return;
    try { frame.contentWindow.postMessage(JSON.stringify({ event: "command", func: func, args: args || [], id: 1, channel: "widget" }), origin); } catch (e) {}
  }
  function hello() {
    if (!frame || live) return;
    try { frame.contentWindow.postMessage(JSON.stringify({ event: "listening", id: 1, channel: "widget" }), "*"); } catch (e) {}
  }
  if (frame) {
    w.addEventListener("message", function (e) {
      if (e.source !== frame.contentWindow) return;
      var m; try { m = typeof e.data === "string" ? JSON.parse(e.data) : e.data; } catch (x) { return; }
      if (!m || !m.event) return;
      live = true;
      if (/^https:\/\/www\.youtube(-nocookie)?\.com$/.test(e.origin)) origin = e.origin;
      var info = m.info || {};
      if (typeof info.duration === "number" && info.duration > lastT) total = info.duration;
      if (typeof info.playerState === "number") { playing = info.playerState === 1; }
      if (typeof info.currentTime === "number") { t = info.currentTime; lastBeat = Date.now(); }
      paint();
    });
  }
  if (audio) {
    ["timeupdate", "play", "pause", "ended", "seeked"].forEach(function (ev) {
      audio.addEventListener(ev, function () { t = audio.currentTime || 0; playing = !audio.paused && !audio.ended; paint(); });
    });
  }
  function play() {
    if (audio) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); return; }
    if (live) send("playVideo");
    else seek(t, true);
  }
  function pause() {
    if (audio) audio.pause(); else send("pauseVideo");
  }
  function seek(s, go) {
    s = Math.max(0, Math.min(total - 1, s));
    t = s;
    if (audio) {
      try { audio.currentTime = s; } catch (e) {}
      if (go !== false) play();
    } else if (frame) {
      if (live) { send("seekTo", [s, true]); if (go !== false) send("playVideo"); }
      else frame.src = frame.src.split("?")[0] + "?enablejsapi=1&rel=0&autoplay=1&start=" + Math.floor(s);
    }
    follow = true;
    paint(true);
  }

  /* ---- following the voice ---- */
  var follow = true, quietUntil = 0, cur = -2, curC = -2, turn = 0;
  function lineAt(s) {
    var i = -1;
    for (var k = 0; k < times.length; k++) {
      if (times[k] === null) continue;
      if (times[k] <= s + 0.25) i = k; else break;
    }
    return i;
  }
  function chapAt(s) {
    var c = 0;
    for (var k = 0; k < chaps.length; k++) if (chaps[k].at <= s + 0.25) c = k;
    return c;
  }
  function paint(jump) {
    if (el.hidden) return;
    el.classList.toggle("is-playing", playing);
    var pb = $(".v4-ls-play");
    pb.setAttribute("aria-label", playing ? "Pause" : "Play");
    $(".v4-ls-cur").textContent = clock(t);
    var i = lineAt(t), c = chaps.length ? chapAt(t) : -1;
    if (i !== cur) {
      outLines.forEach(function (p, k) { p.classList.toggle("is-on", k === i); p.classList.toggle("is-past", k < i); });
      cur = i;
      if (i >= 0 && (jump || (follow && Date.now() > quietUntil))) keep(outLines[i], jump);
    }
    if (c !== curC && c >= 0) {
      curC = c;
      $(".v4-ls-chno").textContent = "Chapter " + (c + 1) + " of " + chaps.length;
      $(".v4-ls-chname").textContent = chaps[c].title;
      arcs.forEach(function (a, k) { a.classList.toggle("is-on", k === c); a.classList.toggle("is-past", k < c); });
      // turn the shortest way to put this chapter at the top
      var want = -marks[c], diff = ((want - turn) % 360 + 540) % 360 - 180;
      turn += diff;
      el.style.setProperty("--turn", turn.toFixed(2) + "deg");
    }
    var f = total ? Math.min(1, t / total) : 0;
    el.style.setProperty("--done", f.toFixed(4));
    draws.forEach(function (p) {
      if (!p._len) { try { p._len = p.getTotalLength() || 1; } catch (e) { p._len = 1; } p.style.strokeDasharray = p._len.toFixed(2); }
      p.style.strokeDashoffset = (p._len * (1 - f)).toFixed(2);
    });
    fills.forEach(function (p) { p.style.opacity = (0.12 + 0.88 * f).toFixed(3); });
    segs.forEach(function (s, k) {
      var a0 = chaps[k].at, a1 = k + 1 < chaps.length ? chaps[k + 1].at : total;
      s.style.setProperty("--f", Math.max(0, Math.min(1, (t - a0) / Math.max(1, a1 - a0))).toFixed(3));
      s.classList.toggle("is-on", k === c);
    });
  }
  function keep(p, jump) {
    var box = text.getBoundingClientRect(), r = p.getBoundingClientRect();
    var y = text.scrollTop + (r.top - box.top) - box.height * 0.32;
    text.scrollTo({ top: y, behavior: still || jump === "now" ? "auto" : "smooth" });
    $(".v4-ls-back").hidden = true;
  }
  // the reader scrolls the transcript: stop following for a while, and offer the way back
  ["wheel", "touchmove", "keydown"].forEach(function (ev) {
    text.addEventListener(ev, function (e) {
      if (ev === "keydown" && !/^(ArrowUp|ArrowDown|PageUp|PageDown|Home|End)$/.test(e.key)) return;
      quietUntil = Date.now() + 6000;
      if (cur >= 0) $(".v4-ls-back").hidden = false;
    }, { passive: true });
  });
  $(".v4-ls-back").addEventListener("click", function () { quietUntil = 0; if (cur >= 0) keep(outLines[cur]); });

  /* ---- controls ---- */
  $(".v4-ls-play").addEventListener("click", function () { if (playing) pause(); else play(); });
  $(".v4-ls-prev").addEventListener("click", function () {
    var c = chapAt(t);
    // early in a chapter, back to the one before; otherwise to this one's start
    seek(chaps[(t - chaps[c].at < 4 && c > 0) ? c - 1 : c].at);
  });
  $(".v4-ls-next").addEventListener("click", function () {
    var c = chapAt(t);
    if (c + 1 < chaps.length) seek(chaps[c + 1].at);
  });
  segs.forEach(function (s, k) { s.addEventListener("click", function () { seek(chaps[k].at); }); });
  text.addEventListener("click", function (e) {
    var b = e.target.closest(".v4-ls-ts");
    if (b) seek(times[Number(b.parentNode.getAttribute("data-k"))], true);
  });

  /* ---- the video, laid over its frame ---- */
  var slot = $(".v4-ls-video"), raf = 0;
  function place() {
    if (!slot || el.hidden) return;
    var r = slot.getBoundingClientRect();
    var s = player.style;
    s.position = "fixed"; s.left = r.left + "px"; s.top = r.top + "px"; s.width = r.width + "px"; s.height = r.height + "px";
    s.margin = "0"; s.zIndex = "231"; s.maxWidth = "none";
  }
  function unplace() {
    ["position", "left", "top", "width", "height", "margin", "zIndex", "maxWidth"].forEach(function (k) { player.style[k] = ""; });
  }
  function onResize() { cancelAnimationFrame(raf); raf = requestAnimationFrame(place); }

  /* ---- open and close ---- */
  var opener = null;
  function keys(e) {
    if (el.hidden) return;
    if (e.key === "Escape") { e.preventDefault(); close(); return; }
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea") return;
    if (e.key === " " && tag !== "button") { e.preventDefault(); if (playing) pause(); else play(); }
    else if (e.key === "ArrowRight" && e.target.closest && !e.target.closest(".v4-ls-text")) { e.preventDefault(); $(".v4-ls-next").click(); }
    else if (e.key === "ArrowLeft" && e.target.closest && !e.target.closest(".v4-ls-text")) { e.preventDefault(); $(".v4-ls-prev").click(); }
    else if (e.key === "Tab") {
      // keep the keyboard inside the screen
      var f = [].slice.call(el.querySelectorAll("button:not([hidden]), [tabindex='0']")).filter(function (x) { return x.offsetParent !== null; });
      if (!f.length) return;
      if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  }
  function open(from) {
    opener = from || d.activeElement;
    el.hidden = false;
    d.documentElement.classList.add("v4-ls-on");
    // the opening frame first, then the moving parts, so the screen does not arrive mid-turn
    el.classList.add("is-still");
    cur = -2; curC = -2;
    if (audio) t = audio.currentTime || 0;
    paint("now");
    requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.remove("is-still"); }); });
    place();
    w.addEventListener("resize", onResize);
    w.addEventListener("scroll", onResize, { passive: true });
    d.addEventListener("keydown", keys);
    hello();
    $(".v4-ls-play").focus();
    if (location.hash !== "#listen") try { history.replaceState(history.state, "", "#listen"); } catch (e) {}
  }
  function close() {
    el.hidden = true;
    d.documentElement.classList.remove("v4-ls-on");
    unplace();
    w.removeEventListener("resize", onResize);
    w.removeEventListener("scroll", onResize);
    d.removeEventListener("keydown", keys);
    if (location.hash === "#listen") try { history.replaceState(history.state, "", location.pathname + location.search); } catch (e) {}
    if (opener && opener.focus) opener.focus();
  }
  el.querySelector(".v4-ls-x").addEventListener("click", close);
  // keep time while closed too, so it opens where the voice is
  setInterval(function () { if (!el.hidden && frame && !live) hello(); }, 1000);

  w.V4_LISTEN = { open: open, close: close };
})();
