const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const dot = document.getElementById('cursorDot');

if (!reduced && dot && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  window.addEventListener('mousemove', (e) => {
    dot.style.left = e.clientX + 'px';
    dot.style.top = e.clientY + 'px';
  });

  document.querySelectorAll('[data-hover]').forEach((el) => {
    el.addEventListener('mouseenter', () => {
      dot.style.width = '28px';
      dot.style.height = '28px';
      dot.style.background = 'transparent';
      dot.style.border = '1px solid currentColor';
    });
    el.addEventListener('mouseleave', () => {
      dot.style.width = '10px';
      dot.style.height = '10px';
      dot.style.background = 'var(--ink)';
      dot.style.border = 'none';
    });
  });
}
