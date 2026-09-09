// Smooth-scroll physics via Lenis — a contained addition, isolated in its
// own file per the site's established pattern of keeping features separate
// so edits elsewhere can't accidentally break this.
//
// Skips entirely if the person has requested reduced motion, falling back
// to normal native browser scrolling (no smooth-scroll library at all).
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (typeof Lenis === 'undefined') return;

  const lenis = new Lenis({
    duration: 1.1,          // how long a scroll "settles" for — higher = heavier/slower feel
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // smooth ease-out
    smoothWheel: true,
    touchMultiplier: 1.5,
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);
})();
