/* Homepage: the episode marquee, and the Library shine.
   ==========================================================================
   THE MARQUEE IS NO LONGER A CSS ANIMATION. It was `animation:ep-scroll 32s
   linear infinite`, which cannot be nudged by a finger: a CSS animation owns
   the transform and a drag would fight it. One rAF loop drives both the drift
   and the drag, so they cannot disagree.

   THE CARDS ARE CLONED ONCE, here rather than in the generator. The loop wraps
   at half the track width, which needs two identical halves, but the generator
   is the source of fifteen episodes and should not emit thirty. The clones are
   aria-hidden and untabbable so a screen reader and the keyboard see the strip
   once. */
(function () {
  'use strict';

  var reduce = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- marquee */
  (function marquee() {
    var vp = document.querySelector('.episodes-viewport');
    var trk = vp && vp.querySelector('.ep-track');
    if (!vp || !trk || !trk.children.length) return;
    if (reduce) return;                       /* CSS leaves it a plain scroller */

    var originals = Array.prototype.slice.call(trk.children);
    originals.forEach(function (el) {
      var c = el.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      c.setAttribute('tabindex', '-1');
      trk.appendChild(c);
    });

    var x = 0, half = 0, speed = 0.35;
    var paused = false, dragging = false;
    var startX = 0, startPos = 0, moved = 0, resumeTimer = null;

    function measure() { half = trk.scrollWidth / 2; }
    function wrap() {
      if (half <= 0) return;
      while (x <= -half) x += half;
      while (x > 0) x -= half;
    }
    function paint() { trk.style.transform = 'translate3d(' + x + 'px,0,0)'; }

    function tick() {
      if (!paused && !dragging) { x -= speed; wrap(); paint(); }
      requestAnimationFrame(tick);
    }

    measure();
    window.addEventListener('resize', measure);
    /* images change the track width as they arrive */
    window.addEventListener('load', measure);
    requestAnimationFrame(tick);

    /* pointing at the strip stops it, so a card can be read and clicked */
    vp.addEventListener('mouseenter', function () { paused = true; });
    vp.addEventListener('mouseleave', function () { if (!dragging) paused = false; });

    vp.addEventListener('pointerdown', function (e) {
      dragging = true; moved = 0; startX = e.clientX; startPos = x;
      vp.classList.add('is-dragging');
      try { vp.setPointerCapture(e.pointerId); } catch (err) {}
      if (resumeTimer) { clearTimeout(resumeTimer); resumeTimer = null; }
    });

    vp.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var dx = e.clientX - startX;
      if (Math.abs(dx) > moved) moved = Math.abs(dx);
      x = startPos + dx; wrap(); paint();
    });

    function release(e) {
      if (!dragging) return;
      dragging = false;
      vp.classList.remove('is-dragging');
      try { vp.releasePointerCapture(e.pointerId); } catch (err) {}
      /* A DRAG MUST NOT OPEN THE CARD UNDER YOUR FINGER. Anything past a few
         pixels is a drag, and the click that follows it is swallowed once. */
      if (moved > 6) {
        var kill = function (ev) { ev.preventDefault(); ev.stopPropagation(); };
        vp.addEventListener('click', kill, true);
        setTimeout(function () { vp.removeEventListener('click', kill, true); }, 0);
      }
      resumeTimer = setTimeout(function () { paused = false; }, 900);
    }
    vp.addEventListener('pointerup', release);
    vp.addEventListener('pointercancel', release);
  })();

  /* ---------------------------------------------------------------- Library */
  (function library() {
    var link = document.querySelector('.ep-search-library-link');
    if (!link) return;
    if (reduce) { link.classList.add('is-lit'); return; }
    if (!('IntersectionObserver' in window)) {
      link.classList.add('is-shining');
      setTimeout(function () { link.classList.add('is-lit'); }, 1750);
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.disconnect();
        link.classList.add('is-shining');
        /* the dots arrive just before the 1900ms shine ends, so the two read as
           one gesture rather than as two things happening at once */
        setTimeout(function () { link.classList.add('is-lit'); }, 1750);
      });
    }, { threshold: 0.6 });
    io.observe(link);
  })();
})();
