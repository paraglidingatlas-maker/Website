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

/* the trip finder: filters the departures table and takes you there */
(function () {
  var f = document.querySelector('[data-finder]'); if (!f) return;
  var out = document.querySelector('[data-found]'), box = document.querySelector('.v2-deps');
  var rows = [].slice.call(document.querySelectorAll('.v2-dep[data-place]'));
  var names = { india: 'India', kenya: 'Kenya', kazakhstan: 'Kazakhstan', peru: 'Peru' };
  function go() {
    var d = document.getElementById('dates');
    if (d) d.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  }
  function run(scroll) {
    var place = f.place.value, month = f.month.value, n = 0;
    rows.forEach(function (r) {
      var ok = (!place || r.dataset.place === place) && (!month || r.dataset.month === month);
      r.hidden = !ok; if (ok) n++;
    });
    if (box) box.hidden = !n;
    if (out) out.innerHTML = (!place && !month) ? '' : n
      ? '<b>' + n + (n === 1 ? ' departure' : ' departures') + '</b> match' + (place ? ' ' + names[place] : '') + (month ? ', ' + f.month.options[f.month.selectedIndex].text : '') + '. <button type="button" data-clear>Show all</button>'
      : 'No departure matches that yet. <button type="button" data-clear>Show all</button> or <a href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener">book a call</a> and we will find one.';
    if (scroll) go();
  }
  f.addEventListener('submit', function (e) { e.preventDefault(); run(true); });
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-clear],[data-pick]'); if (!t) return;
    if (t.hasAttribute('data-clear')) { f.place.value = ''; f.month.value = ''; run(false); return; }
    e.preventDefault(); f.place.value = t.dataset.pick; f.month.value = ''; run(true);
  });
})();
