/* Designer E (Cloudbase), event landing pages, contest round 1: "Pull Back to the Race".
   1. The pull-back: one screen of scroll pulls the camera back from the event's lead frame until it sits in its own
      place on the race line (transform only: the frame's box scales, the picture inside is counter-scaled so it never
      stretches). Scroll drives it both ways; nothing moves on its own. Reduced motion, no JavaScript, or a screen too
      short for the race line: no move, the opening and the line stand one after the other.
   2. Taps: "Find your photos" / "All five films" drive the same move to its end; a task on the line flies in to its
      chapter (the shared gallery opens the task); a film's stills and the opening's Play play the film in place.
   3. Films-only pages: the bar marks the day on screen.
   4. The season: a comp on now says so (in its own time zone); a tap on another comp grows its frame to fill the
      screen, then that comp's page opens on the same picture. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  function mm(q) { return !!(w.matchMedia && w.matchMedia(q).matches); }
  function reduced() { return mm("(prefers-reduced-motion: reduce)"); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function band(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
  function inout(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function navH() { return parseFloat(getComputedStyle(root).getPropertyValue("--v2-nav-h")) || 72; }

  /* ---------------------------------------------------------------- 1. the pull-back */
  var stage = d.querySelector("[data-ev-stage]"), back, cam, shot, inner, img, copy, scrim, route, target, M = null, on = false, raf = 0;
  if (stage) {
    cam = stage.querySelector(".ev-cam"); shot = stage.querySelector("[data-shot]"); inner = shot.querySelector(".ev-shot-in");
    img = inner.querySelector("img"); copy = stage.querySelector(".ev-copy"); back = stage.querySelector(".ev-back"); scrim = stage.querySelector(".ev-scrim");
    route = stage.querySelector(".ev-route"); target = stage.querySelector("[data-target]");
  }
  function measure() {
    if (!stage || !target) return;
    var want = !reduced() && w.requestAnimationFrame;
    root.classList.add("ev-move");                              // lay out as the move would, then check it fits
    var nav = d.querySelector(".page-wrap>nav"); if (nav) root.style.setProperty("--ev-nav", nav.offsetHeight + "px");
    var H = cam.clientHeight, need = route.querySelector(".ev-route-in").getBoundingClientRect().height + (mm("(max-width:820px)") ? (nav ? nav.offsetHeight : 93) + 8 : 48);
    if (!want || need > H + 1) { root.classList.remove("ev-move"); on = false; reset(); return; }
    on = true;
    var c = cam.getBoundingClientRect(), t = target.getBoundingClientRect();
    // the shot's own box (it may be shorter than the screen: a film's frame on a phone)
    var sw = shot.offsetWidth, sh = shot.offsetHeight;
    var iw = +img.getAttribute("width") || 16, ih = +img.getAttribute("height") || 9;
    var c0 = Math.max(sw / iw, sh / ih), c1 = Math.max(t.width / iw, t.height / ih);
    // the picture at its own ratio, centred and uncut (an object-fit picture would be clipped to its box)
    var pw = iw * c0, ph = ih * c0;
    img.style.cssText = "position:absolute;left:50%;top:50%;max-width:none;width:" + pw + "px;height:" + ph + "px;margin:" + (-ph / 2) + "px 0 0 " + (-pw / 2) + "px";
    // travel: 0.9 of a screen on a phone, one screen on a desktop; then a short hold on the finished line
    M = { x0: shot.offsetLeft, y0: shot.offsetTop, sw: sw, sh: sh, tx: t.left - c.left, ty: t.top - c.top, tw: t.width, th: t.height, c0: c0, c1: c1, iw: iw, ih: ih,
          travel: Math.max(1, H * (mm("(max-width:820px)") ? .9 : 1)) };
    stage.style.setProperty("--ev-travel", M.travel + "px");
    stage.style.setProperty("--ev-hold", Math.round(H * .08) + "px");
    tick();
  }
  function reset() {
    if (!shot) return;
    shot.style.transform = inner.style.transform = ""; if (img) img.style.cssText = ""; if (back) { back.style.opacity = back.style.visibility = ""; } if (copy) { copy.style.opacity = ""; copy.style.transform = ""; copy.classList.remove("is-gone"); }
    if (scrim) scrim.style.opacity = ""; if (cam) cam.classList.remove("is-done");
  }
  function progress() { return on ? clamp(-stage.getBoundingClientRect().top / M.travel, 0, 1) : 0; }
  function tick() {
    raf = 0; if (!on || !M) return;
    var p = progress(), e = inout(band(p, .06, .92));
    // the words go first (within the first sixth), the scrim with them, so the picture is clean before it shrinks
    var q = band(p, 0, .16);
    copy.style.opacity = String(1 - q); copy.style.transform = "translate3d(0," + (-24 * q).toFixed(1) + "px,0)";
    copy.classList.toggle("is-gone", q > .5);
    if (back) { back.style.opacity = String(1 - band(p, 0, .08)); back.style.visibility = p > .08 ? "hidden" : ""; }
    scrim.style.opacity = String(1 - band(p, .02, .22));
    // the box: from the shot to the frame on the line (origin top left)
    var bw = M.sw + (M.tw - M.sw) * e, bh = M.sh + (M.th - M.sh) * e, bx = M.x0 + (M.tx - M.x0) * e, by = M.y0 + (M.ty - M.y0) * e;
    var Sx = bw / M.sw, Sy = bh / M.sh;
    shot.style.transform = "translate3d(" + (bx - M.x0).toFixed(2) + "px," + (by - M.y0).toFixed(2) + "px,0) scale(" + Sx.toFixed(5) + "," + Sy.toFixed(5) + ")";
    // the picture: one scale, always covering the box (geometric, so the zoom keeps one speed)
    var k = Math.max(bw / M.iw, bh / M.ih) / M.c0;
    inner.style.transform = "scale(" + (k / Sx).toFixed(5) + "," + (k / Sy).toFixed(5) + ")";
    cam.classList.toggle("is-done", p >= .999);
  }
  function req() { if (!raf) raf = requestAnimationFrame(tick); }
  if (stage) {
    w.addEventListener("scroll", req, { passive: true });
    var rt = 0; w.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(measure, 120); });
    if (w.matchMedia) { var mq = w.matchMedia("(prefers-reduced-motion: reduce)"); if (mq.addEventListener) mq.addEventListener("change", measure); }
    if (d.readyState === "complete") measure(); else { measure(); w.addEventListener("load", measure); }
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(measure);
  }

  /* ---------------------------------------------------------------- 2. taps */
  function smooth() { return reduced() ? "auto" : "smooth"; }
  function toY(y) { w.scrollTo({ top: Math.max(0, y), behavior: smooth() }); }
  function raceEnd() { return on ? stage.offsetTop + M.travel + 2 : route.getBoundingClientRect().top + w.scrollY - navH(); }
  function chapterTop(el) { return el.getBoundingClientRect().top + w.scrollY - (d.querySelector(".ev-bar") ? 64 : 0) - 8; }
  function playIn(sec) {
    var a = sec && sec.querySelector(".md-play"); if (!a) return;
    var fr = a.closest(".md-frame"); toY(chapterTop(sec));
    setTimeout(function () { a.click(); }, reduced() ? 0 : 450);
  }
  d.addEventListener("click", function (e) {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    var a = e.target.closest && e.target.closest("a"); if (!a) return;
    if (a.hasAttribute("data-ev-race")) { e.preventDefault(); toY(raceEnd()); return; }
    if (a.getAttribute("href") === "#season") { var se = d.getElementById("season"); if (se) { e.preventDefault(); toY(se.getBoundingClientRect().top + w.scrollY - 24); try { history.replaceState(null, "", "#season"); } catch (x) {} } return; }
    if (a.hasAttribute("data-ev-play")) { e.preventDefault(); playIn(d.getElementById(a.getAttribute("href").slice(1))); return; }
    var still = a.getAttribute("data-ev-still");
    if (still) { e.preventDefault(); playIn(a.closest(".ev-ch")); return; }
    // a task on the line, or Watch the films: the gallery (v4-gallery.js) has opened the task; bring it up
    if (a.closest(".ev-leg") || a.hasAttribute("data-ev-to")) {
      var id = (a.getAttribute("href") || "").slice(1), sec = id && d.getElementById(id); if (!sec) return;
      e.preventDefault();
      var line = d.querySelector(".gf-line");
      if (line) {   // the photos: the task's head just under the sticky task line
        setTimeout(function () { toY(sec.getBoundingClientRect().top + w.scrollY - line.offsetHeight - 12); }, 0);
      } else toY(chapterTop(sec));
      try { history.replaceState(null, "", "#" + id); } catch (x) {}
    }
  });

  /* ---------------------------------------------------------------- 3. films only: the bar follows the chapters */
  var bar = d.querySelector(".ev-bar");
  if (bar && w.IntersectionObserver) {
    var links = [].slice.call(bar.querySelectorAll(".ev-bar-in a")), seen = {};
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (x) { seen[x.target.id] = x.isIntersecting; });
      var cur = null; links.forEach(function (l) { var id = l.getAttribute("href").slice(1); if (seen[id]) cur = l; });
      links.forEach(function (l) { if (l === cur) l.setAttribute("aria-current", "true"); else l.removeAttribute("aria-current"); });
      if (cur && cur.scrollIntoView && bar.querySelector(".ev-bar-in").scrollWidth > bar.offsetWidth) {
        var box = bar.querySelector(".ev-bar-in"); box.scrollTo({ left: cur.offsetLeft - 16, behavior: smooth() });
      }
    }, { rootMargin: "-30% 0px -60% 0px" });
    links.forEach(function (l) { var s = d.getElementById(l.getAttribute("href").slice(1)); if (s) io.observe(s); });
    bar.addEventListener("click", function (e) {
      var a = e.target.closest("a"); if (!a || a.classList.contains("ev-line-s")) return;
      var s = d.getElementById(a.getAttribute("href").slice(1)); if (!s) return;
      e.preventDefault(); toY(chapterTop(s));
    });
  }

  /* ---------------------------------------------------------------- 4. the season */
  function todayIn(tz) {
    try { return new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date()); }
    catch (x) { return new Date().toISOString().slice(0, 10); }
  }
  [].forEach.call(d.querySelectorAll(".ev-s[data-window]"), function (li) {
    var win = li.getAttribute("data-window").split(","), t = todayIn(li.getAttribute("data-tz") || "UTC"), tag = li.querySelector("[data-now]");
    if (tag && t >= win[0] && t <= win[1]) tag.hidden = false;
  });
  d.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-fly]");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button || reduced()) return;
    var src = a.querySelector(".ev-s-f img") || (function () {      // Before / Next: fly from the season's frame of that comp
      var f = d.querySelector('.ev-s a[href="' + a.getAttribute("href") + '"] .ev-s-f img'); return f;
    })();
    if (!src || !src.animate) return;
    e.preventDefault();
    var r = src.getBoundingClientRect(), fly = d.createElement("div"), im = new Image();
    fly.className = "ev-fly"; im.src = src.currentSrc || src.src; im.alt = ""; fly.appendChild(im);
    fly.style.cssText = "left:0;top:0;width:" + innerWidth + "px;height:" + innerHeight + "px";
    d.body.appendChild(fly);
    var sx = r.width / innerWidth, sy = r.height / innerHeight;
    // the box from the frame to the screen; the picture counter-scaled so it covers without stretching
    var iw = src.naturalWidth || 16, ih = src.naturalHeight || 9;
    var u = Math.max(r.width / iw, r.height / ih) / Math.max(innerWidth / iw, innerHeight / ih);
    fly.animate([{ transform: "translate(" + r.left + "px," + r.top + "px) scale(" + sx + "," + sy + ")" }, { transform: "none" }],
      { duration: 520, easing: "cubic-bezier(.65,0,.25,1)", fill: "forwards" });
    im.animate([{ transform: "scale(" + u / sx + "," + u / sy + ")" }, { transform: "none" }],
      { duration: 520, easing: "cubic-bezier(.65,0,.25,1)", fill: "forwards" });
    setTimeout(function () { location.href = a.href; }, 470);
    w.addEventListener("pageshow", function (ev) { if (ev.persisted && fly.parentNode) fly.remove(); });
  });
})();
