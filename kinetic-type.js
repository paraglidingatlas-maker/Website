// Kinetic typography: splits the pull-quote text into individual words and
// reveals them with a staggered cascade when scrolled into view, instead of
// a simple fade. Isolated in its own file per the site's established pattern
// of keeping features separate so edits elsewhere can't break this.
//
// Uses IntersectionObserver (the same well-tested pattern already used
// elsewhere on this page) rather than a continuous scroll-linked animation,
// deliberately kept simple and robust after the earlier smooth-scroll
// experiment didn't work out.
(function () {
  const el = document.getElementById('kineticQuote');
  if (!el) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Split into words, wrapping each in its own span, preserving the
  // original spacing exactly.
  const words = el.textContent.trim().split(/\s+/);
  el.innerHTML = words
    .map((word) => `<span class="kinetic-word">${word}</span>`)
    .join(' ');

  if (reducedMotion) {
    el.querySelectorAll('.kinetic-word').forEach((w) => w.classList.add('visible'));
    return;
  }

  const wordEls = el.querySelectorAll('.kinetic-word');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          wordEls.forEach((w, i) => {
            setTimeout(() => w.classList.add('visible'), i * 40);
          });
          observer.disconnect();
        }
      });
    },
    { threshold: 0.4 }
  );
  observer.observe(el);
})();
