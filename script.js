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
      dot.style.background = 'var(--bg)';
      dot.style.border = 'none';
    });
  });
}

// Episode map: click a pin to show its popup
const epMap = document.getElementById('epMap');
if (epMap) {
  const popup = document.getElementById('mapPopup');
  const popupGuest = popup.querySelector('.popup-guest');
  const popupTitle = popup.querySelector('.popup-title');
  const popupLink = popup.querySelector('.popup-link');

  epMap.querySelectorAll('.map-pin').forEach((pin) => {
    pin.addEventListener('click', (e) => {
      e.stopPropagation();
      popupGuest.textContent = pin.dataset.guest;
      popupTitle.textContent = pin.dataset.title;
      popupLink.href = pin.dataset.href;
      popup.style.left = pin.style.left;
      popup.style.top = pin.style.top;
      popup.classList.add('visible');
    });
  });

  document.addEventListener('click', () => {
    popup.classList.remove('visible');
  });
  popup.addEventListener('click', (e) => e.stopPropagation());
}
