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

/* "See dates" and the next-departure card: show that trip's rows in the dates table */
(function () {
  var out = document.querySelector('[data-found]'), rows = [].slice.call(document.querySelectorAll('.v2-dep[data-place]'));
  if (!rows.length) return;
  var names = { india: 'India', kenya: 'Kenya', kazakhstan: 'Kazakhstan', peru: 'Peru' };
  function show(place) {
    var n = 0;
    rows.forEach(function (r) { var ok = !place || r.dataset.place === place; r.hidden = !ok; if (ok) n++; });
    if (out) out.innerHTML = place ? '<b>' + n + (n === 1 ? ' departure' : ' departures') + '</b> for ' + names[place] + '. <button type="button" data-clear>Show all</button>' : '';
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-clear],[data-pick]'); if (!t) return;
    if (t.hasAttribute('data-clear')) { show(''); return; }
    e.preventDefault(); show(t.dataset.pick);
    var d = document.getElementById('dates');
    if (d) d.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  });
})();

/* The four expeditions, flown through: the step in the middle of the screen
   picks the picture held behind it and lights its name on the altimeter.
   Scroll-driven only; nothing runs while the page is still. */
(function () {
  var box = document.querySelector('[data-flyby]');
  if (!box || !('IntersectionObserver' in window)) return;
  var shots = box.querySelectorAll('.v2-fb-shot'), alts = box.querySelectorAll('.v2-fb-alt li'),
      steps = [].slice.call(box.querySelectorAll('.v2-fb-step'));
  function show(i) {
    [shots, alts, steps].forEach(function (list) {
      [].forEach.call(list, function (el, k) { el.classList.toggle('is-on', k === i); });
    });
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) show(steps.indexOf(en.target)); });
  }, { rootMargin: '-45% 0px -45% 0px' });
  steps.forEach(function (s) { io.observe(s); });
  box.classList.add('is-live');
})();
