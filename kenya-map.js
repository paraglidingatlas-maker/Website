/* Kenya route map. Two states over one set of sites.
 *
 * Overview is the axonometric plate: the whole country, recognisable, no room
 * for detail. The sheet is the aviation chart cropped to the corridor, which
 * carries towns, the graticule and per-leg bearings but cannot say where in
 * Kenya any of it is. Each covers the other's gap, which is why the plate stays
 * on screen as the locator rather than being replaced.
 *
 * Both projections are exact linear functions of longitude and latitude, so a
 * marker's position in each is computed rather than placed by eye. The two
 * position sets are baked into data-plate and data-sheet by the generators in
 * tools/, from the same coordinates the page already publishes.
 *
 * The sheet is fetched on first open. Most visitors never open it and it is
 * 22KB gzipped plus a 25KB terrain raster, which is not worth spending on load.
 *
 * Below 820px the sheet does not appear at all. Its smallest type lands under
 * 3px on a phone, which is not a detail view, it is a smudge. The bearings and
 * distances it carries are in the panel as text instead, which is better on a
 * phone than a chart nobody can read.
 */
(function () {
  var root = document.querySelector('.kmap');
  if (!root) return;

  var stage = root.querySelector('.kmap-stage');
  var sheetLayer = root.querySelector('.kmap-sheet');
  var pins = [].slice.call(root.querySelectorAll('.kmap-pin'));
  var rows = [].slice.call(root.querySelectorAll('.kmap-row'));
  var panel = root.querySelector('.kmap-panel');
  var zoom = root.querySelector('.kmap-zoom');
  if (!stage || !pins.length) return;

  var wide = window.matchMedia('(min-width: 821px)');
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');
  var at = -1, sheetOn = false, loading = false, loaded = false;

  function place() {
    var key = sheetOn ? 'sheet' : 'plate';
    pins.forEach(function (p) {
      var d = JSON.parse(p.getAttribute('data-' + key));
      p.style.left = d.x + '%';
      p.style.top = d.y + '%';
    });
  }

  function select(i) {
    if (i === at) return;
    at = i;
    pins.forEach(function (p, n) {
      p.classList.toggle('is-on', n === i);
      p.setAttribute('aria-pressed', n === i);
    });
    rows.forEach(function (r, n) {
      r.classList.toggle('is-on', n === i);
      r.setAttribute('aria-pressed', n === i);
    });
    var src = rows[i];
    if (!panel || !src) return;
    panel.innerHTML = src.getAttribute('data-panel');
    panel.hidden = false;
  }

  function loadSheet(then) {
    if (loaded) { then(); return; }
    if (loading) return;
    loading = true;
    fetch(sheetLayer.getAttribute('data-src'))
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      })
      .then(function (svg) {
        sheetLayer.innerHTML = svg;
        loaded = true;
        loading = false;
        /* a frame, so the browser has the new nodes laid out before the
           transition class lands, or the sheet jumps instead of growing */
        requestAnimationFrame(function () { requestAnimationFrame(then); });
      })
      .catch(function () {
        loading = false;
        if (zoom) {
          zoom.disabled = true;
          zoom.textContent = 'Chart unavailable';
        }
      });
  }

  function setSheet(on) {
    if (on && !wide.matches) return;
    if (on && !loaded) { loadSheet(function () { setSheet(true); }); return; }
    sheetOn = on;
    stage.classList.toggle('is-sheet', on);
    place();
    if (zoom) {
      zoom.setAttribute('aria-pressed', on);
      zoom.textContent = on ? 'Back to the overview' : 'Open the chart';
    }
  }

  pins.forEach(function (p, i) {
    p.addEventListener('click', function () { select(i); });
  });
  rows.forEach(function (r, i) {
    r.addEventListener('click', function () { select(i); });
  });

  if (zoom) {
    zoom.addEventListener('click', function () { setSheet(!sheetOn); });
  }
  root.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sheetOn) { setSheet(false); }
  });
  wide.addEventListener('change', function () {
    if (!wide.matches && sheetOn) setSheet(false);
    if (zoom) zoom.hidden = !wide.matches;
  });

  /* Draw the course in once the section is on screen. It is a single path with
     its dash pattern set to its own length, so nothing is measured by hand. */
  var course = root.querySelector('.kmap-plate .kmap-course');
  if (course && !calm.matches && 'IntersectionObserver' in window) {
    try {
      var L = course.getTotalLength();
      course.style.strokeDasharray = L;
      course.style.strokeDashoffset = L;
      new IntersectionObserver(function (es, obs) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          course.style.transition = 'stroke-dashoffset 1600ms cubic-bezier(.5,.05,.2,1)';
          course.style.strokeDashoffset = 0;
          obs.disconnect();
        });
      }, { threshold: 0.25 }).observe(stage);
    } catch (err) { /* getTotalLength can throw on a detached node */ }
  }

  if (zoom) zoom.hidden = !wide.matches;
  place();
  select(0);
})();
