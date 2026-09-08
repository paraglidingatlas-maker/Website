const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const dot = document.getElementById('cursorDot');

if (!reduced && dot && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  window.addEventListener('mousemove', (e) => {
    dot.style.left = e.clientX + 'px';
    dot.style.top = e.clientY + 'px';
  });

  document.querySelectorAll('[data-hover]').forEach((el) => {
    el.addEventListener('mouseenter', () => {
      dot.style.transform = 'translate(-50%,-65%) scale(1.8)';
      dot.style.background = 'var(--orange)';
    });
    el.addEventListener('mouseleave', () => {
      dot.style.transform = 'translate(-50%,-65%) scale(1)';
      dot.style.background = 'var(--white)';
    });
  });
}
