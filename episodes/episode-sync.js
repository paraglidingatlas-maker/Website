/* The episode page follows the conversation.
 *
 * Any timestamp in the transcript (and each chapter's own time) jumps the video
 * to that moment and plays it. While the video plays, the line being spoken is
 * lit and the chapter rail follows the playback instead of the scroll.
 *
 * It talks to the YouTube embed through the same postMessage protocol the
 * YouTube iframe API uses, so no YouTube script is loaded into this page: the
 * embed carries enablejsapi=1 (generate_chapter_deck.py), this file says
 * "listening", and the player answers with its time.
 *
 * If the player never answers (blocked, offline, a browser that refuses), the
 * page is exactly what it was, and a timestamp still works: it reloads the
 * embed at that second instead. Nothing here is needed to read the page.
 */
(function () {
  "use strict";
  var frame = document.querySelector(".cd-player iframe");
  var lines = [].slice.call(document.querySelectorAll(".cd-line"));
  if (!frame || !lines.length) return;

  function secs(t) {
    var p = (t || "").trim().split(":").map(Number);
    if (p.some(isNaN)) return null;
    return p.reduce(function (a, b) { return a * 60 + b; }, 0);
  }

  // Every line's start time, in order.
  var times = lines.map(function (l) {
    var ts = l.querySelector(".cd-ts");
    return ts ? secs(ts.textContent) : null;
  });
  var chaps = [].slice.call(document.querySelectorAll(".cd-chap"));
  var chapTimes = chaps.map(function (a) {
    var t = a.querySelector("time");
    return t ? secs(t.textContent) : null;
  });

  var live = false;          // the player has answered at least once
  var playing = false;
  var now = -1;              // index of the lit line
  var origin = "*";

  function send(func, args) {
    try {
      frame.contentWindow.postMessage(JSON.stringify(
        { event: "command", func: func, args: args || [], id: 1, channel: "widget" }), origin);
    } catch (e) {}
  }

  // Say "listening" until the player answers; that is what makes it start
  // sending its time. Retries for a while, because the embed loads lazily.
  var tries = 0;
  function hello() {
    if (live || tries++ > 60) return;
    try {
      frame.contentWindow.postMessage(JSON.stringify(
        { event: "listening", id: 1, channel: "widget" }), "*");
    } catch (e) {}
    setTimeout(hello, 500);
  }
  frame.addEventListener("load", function () { tries = 0; hello(); });
  hello();

  window.addEventListener("message", function (e) {
    if (e.source !== frame.contentWindow) return;
    var m;
    try { m = typeof e.data === "string" ? JSON.parse(e.data) : e.data; } catch (err) { return; }
    if (!m || !m.event) return;
    live = true;
    if (/^https:\/\/www\.youtube(-nocookie)?\.com$/.test(e.origin)) origin = e.origin;
    var info = m.info || {};
    if (typeof info.playerState === "number") {
      playing = info.playerState === 1;
      document.body.classList.toggle("cd-playing", playing);
    }
    if (typeof info.currentTime === "number") follow(info.currentTime);
  });

  function follow(t) {
    // the last line that has started
    var i = -1;
    for (var k = 0; k < times.length; k++) {
      if (times[k] !== null && times[k] <= t + 0.25) i = k;
      else if (times[k] !== null && times[k] > t + 0.25) break;
    }
    if (i !== now) {
      if (now >= 0 && lines[now]) lines[now].classList.remove("is-now");
      if (i >= 0) lines[i].classList.add("is-now");
      now = i;
    }
    if (!playing) return;
    var c = -1;
    for (var j = 0; j < chapTimes.length; j++) {
      if (chapTimes[j] !== null && chapTimes[j] <= t + 0.25) c = j;
    }
    chaps.forEach(function (a, j) { a.classList.toggle("active", j === c); });
  }

  // A timestamp is a control. Keyboard reachable, with a label that says so.
  function arm(el, t) {
    if (t === null || !el) return;
    el.setAttribute("role", "button");
    el.setAttribute("tabindex", "0");
    el.setAttribute("aria-label", "Play from " + el.textContent.trim());
    el.classList.add("cd-seek");
    var go = function () { seek(t); };
    el.addEventListener("click", go);
    el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); }
    });
  }
  lines.forEach(function (l, k) { arm(l.querySelector(".cd-ts"), times[k]); });
  [].forEach.call(document.querySelectorAll(".cd-block"), function (b) {
    var bt = b.querySelector(".cd-block-time");
    if (bt) arm(bt, secs(bt.textContent));
  });

  function seek(t) {
    if (live) {
      send("seekTo", [t, true]);
      send("playVideo");
    } else {
      // No answer from the player: load it again at that second.
      var u = frame.src.split("?")[0] + "?enablejsapi=1&autoplay=1&start=" + Math.floor(t);
      frame.src = u;
    }
    follow(t);
    // Bring the video into view if it has scrolled away; smooth unless the
    // visitor asked for less motion.
    var r = frame.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) {
      var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
      frame.scrollIntoView({ block: "center", behavior: still ? "auto" : "smooth" });
    }
  }
})();
