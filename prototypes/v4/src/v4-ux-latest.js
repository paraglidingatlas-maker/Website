/* THE NEWEST EPISODE (podcast, the usability pass 19): on screen one, from the
   saved archive tools/v4_ux.py writes into the page, so it plays whether or
   not the feeds answer. Inlined at the end of the podcast page only
   (tools/v4_ux.py), so no other page carries it. One player at a time: playing it pauses the feed's
   playing row, and pressing a row's play pauses it. The ring fills with the
   episode, as the feed's rows do. */
(function () {
  var d = document;
  function init() {
    var box = d.querySelector(".v4u-latest"), btn = box && box.querySelector(".v4u-play");
    if (!btn) return;
    var audio, quiet = false, grid = d.getElementById("liveFeedGrid");
    function set(on) { box.classList.toggle("playing", on); btn.setAttribute("aria-pressed", on ? "true" : "false"); }
    btn.addEventListener("click", function () {
      if (!audio) {
        audio = new Audio();
        audio.preload = "none";
        audio.src = box.getAttribute("data-audio");
        audio.addEventListener("play", function () {
          set(true);
          var r = grid && grid.querySelector(".ep-row.playing .ep-play-btn");
          if (r) { quiet = true; r.click(); quiet = false; }
        });
        audio.addEventListener("pause", function () { set(false); });
        audio.addEventListener("ended", function () { set(false); });
        audio.addEventListener("timeupdate", function () {
          if (audio.duration) box.style.setProperty("--p", (audio.currentTime / audio.duration).toFixed(4));
        });
      }
      if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () { set(false); }); }
      else audio.pause();
    });
    if (grid) grid.addEventListener("click", function (e) {
      if (!quiet && audio && !audio.paused && e.target.closest && e.target.closest(".ep-play-btn, .ep-play-btn-lg")) audio.pause();
    });
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();
