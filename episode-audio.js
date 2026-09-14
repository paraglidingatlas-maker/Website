/* Episode audio player.
 *
 * These eight episodes were never filmed, so the page had a placeholder image
 * and two links out to Spotify and Apple. Nothing played here. This gives the
 * page its own player, over the episode artwork.
 *
 * THE WAVEFORM IS REAL OR IT IS ABSENT. Drawing a plausible looking squiggle
 * would be inventing data, and this site does not do that. Peaks come from
 * waveforms.json, produced by tools/generate_waveforms.py, which decodes the
 * actual audio with ffmpeg. Until that file exists the bar renders as a plain
 * track and everything else works exactly the same. Nothing here needs changing
 * when the peaks arrive.
 *
 * Peaks cannot be computed in the browser: the files run to 95MB and would have
 * to be fully downloaded and decoded before a single bar could be drawn.
 *
 * Chapter marks ARE real: they come from the episode's own chapter list.
 */
(function () {
  "use strict";

  function fmt(s) {
    if (!isFinite(s) || s < 0) s = 0;
    var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = Math.floor(s % 60);
    var mm = h ? (m < 10 ? "0" + m : "" + m) : "" + m;
    return (h ? h + ":" : "") + mm + ":" + (x < 10 ? "0" + x : x);
  }

  function init(root) {
    var audio = root.querySelector("audio");
    var btn = root.querySelector(".ep-au-play");
    var bar = root.querySelector(".ep-au-bar");
    var fill = root.querySelector(".ep-au-fill");
    var head = root.querySelector(".ep-au-head");
    var cur = root.querySelector(".ep-au-cur");
    var dur = root.querySelector(".ep-au-dur");
    if (!audio || !btn || !bar) return;

    var total = parseFloat(root.dataset.duration || "0") || 0;
    if (total) dur.textContent = fmt(total);

    /* Peaks, if the build produced them. A bar per peak, drawn as an SVG the
       fill clips, so the played part is orange and the rest is grey without
       drawing the shape twice. */
    var peaks = null;
    try {
      var slug = root.dataset.slug;
      if (window.ATLAS_WAVEFORMS && window.ATLAS_WAVEFORMS[slug]) {
        peaks = window.ATLAS_WAVEFORMS[slug];
      }
    } catch (e) { peaks = null; }

    if (peaks && peaks.length) {
      var n = peaks.length, w = 1000, gap = 0.28;
      var bw = w / n, d = "";
      for (var i = 0; i < n; i++) {
        var v = Math.max(0.04, Math.min(1, peaks[i] / 255));
        var h = v * 100, y = (100 - h) / 2;
        d += "M" + (i * bw + gap).toFixed(2) + "," + y.toFixed(2) +
             "h" + (bw - gap * 2).toFixed(2) + "v" + h.toFixed(2) +
             "h-" + (bw - gap * 2).toFixed(2) + "z";
      }
      var svg = '<svg class="ep-au-wave" viewBox="0 0 1000 100" preserveAspectRatio="none"' +
                ' aria-hidden="true"><path d="' + d + '"/></svg>';
      /* Twice: once grey in the track, once orange inside the fill. The fill
         clips to the played width, so the same shape reads as progress without
         drawing a second, differently shaped thing. The inner copy has to stay
         the width of the WHOLE bar or it would squash as the fill grows, so its
         width is set in pixels and kept in step on resize. */
      root.querySelector(".ep-au-track").innerHTML = svg;
      fill.innerHTML = svg;
      var inner = fill.querySelector(".ep-au-wave");
      var sync = function () { inner.style.width = bar.clientWidth + "px"; };
      sync();
      window.addEventListener("resize", sync);
      if (window.ResizeObserver) new ResizeObserver(sync).observe(bar);
      root.classList.add("has-wave");
    }

    function paint() {
      var p = total ? (audio.currentTime / total) : 0;
      if (p > 1) p = 1;
      fill.style.width = (p * 100).toFixed(3) + "%";
      head.style.left = (p * 100).toFixed(3) + "%";
      cur.textContent = fmt(audio.currentTime);
      bar.setAttribute("aria-valuenow", Math.round(p * 100));
    }

    btn.addEventListener("click", function () {
      if (audio.paused) { audio.play(); } else { audio.pause(); }
    });
    audio.addEventListener("play", function () {
      root.classList.add("is-playing");
      btn.setAttribute("aria-label", "Pause");
    });
    audio.addEventListener("pause", function () {
      root.classList.remove("is-playing");
      btn.setAttribute("aria-label", "Play");
    });
    audio.addEventListener("timeupdate", paint);
    audio.addEventListener("loadedmetadata", function () {
      if (isFinite(audio.duration) && audio.duration > 0) {
        total = audio.duration;
        dur.textContent = fmt(total);
      }
      paint();
    });

    /* Scrub. No setPointerCapture: it retargets the click, which is what broke
       the homepage rail. Track on window instead and release there too. */
    var dragging = false;
    function seekTo(clientX) {
      var r = bar.getBoundingClientRect();
      var p = (clientX - r.left) / r.width;
      p = p < 0 ? 0 : p > 1 ? 1 : p;
      if (total) { audio.currentTime = p * total; paint(); }
    }
    bar.addEventListener("pointerdown", function (e) {
      dragging = true; seekTo(e.clientX); e.preventDefault();
    });
    window.addEventListener("pointermove", function (e) {
      if (dragging) seekTo(e.clientX);
    });
    window.addEventListener("pointerup", function () { dragging = false; });
    window.addEventListener("pointercancel", function () { dragging = false; });

    bar.addEventListener("keydown", function (e) {
      if (!total) return;
      var step = e.shiftKey ? 60 : 15;
      if (e.key === "ArrowRight") { audio.currentTime = Math.min(total, audio.currentTime + step); e.preventDefault(); }
      else if (e.key === "ArrowLeft") { audio.currentTime = Math.max(0, audio.currentTime - step); e.preventDefault(); }
      else if (e.key === "Home") { audio.currentTime = 0; e.preventDefault(); }
      else if (e.key === " " || e.key === "Enter") { btn.click(); e.preventDefault(); }
      paint();
    });

    root.querySelectorAll(".ep-au-chap").forEach(function (c) {
      c.addEventListener("click", function (e) {
        e.stopPropagation();
        var t = parseFloat(c.dataset.at || "0");
        audio.currentTime = t;
        if (audio.paused) audio.play();
        paint();
      });
    });

    paint();
  }

  function boot() {
    document.querySelectorAll(".ep-au").forEach(init);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
