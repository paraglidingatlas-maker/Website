/* v2 homepage: the episode rail's two arrow buttons. The rail is a native
   horizontal scroller (finger, trackpad, keyboard, scroll snap), so nothing
   runs on its own: no animation frame loop, nothing while off screen. The
   buttons appear only when there is somewhere to go. */
(function () {
  var rail = document.querySelector('.v2-rail');
  var nav = document.querySelector('.v2-rail-nav');
  if (!rail || !nav) return;
  var btns = nav.querySelectorAll('button');
  function sync() {
    var max = rail.scrollWidth - rail.clientWidth - 2;
    nav.hidden = max <= 0;
    btns[0].disabled = rail.scrollLeft <= 2;
    btns[1].disabled = rail.scrollLeft >= max;
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      rail.scrollBy({ left: +b.dataset.dir * rail.clientWidth * 0.8, behavior: reduce ? 'auto' : 'smooth' });
    });
  });
  rail.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  window.addEventListener('load', sync);
  sync();
})();
