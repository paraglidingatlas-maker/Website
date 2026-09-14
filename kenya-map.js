/* Kenya route map. Two states, one pan and zoom surface.
 *
 * Overview is the axonometric plate: the whole country, recognisable, no room
 * for detail. The sheet is the aviation chart cropped to the corridor, which
 * carries towns, the graticule and per-leg bearings but cannot say where in
 * Kenya any of it is. Each covers the other's gap, which is why the plate is
 * not replaced when the chart opens: it travels to the corner as the locator.
 *
 * Both projections are exact linear functions of longitude and latitude, so a
 * marker's position in each is computed rather than placed by eye. The two sets
 * are baked into data-plate and data-sheet by tools/build_kenya_plate.py and
 * tools/build_kenya_sheet.py, from the coordinates the page already publishes.
 *
 * NO setPointerCapture ANYWHERE. It is in the gotcha notes and it is what broke
 * the homepage rail: capture retargets every later pointer event to the
 * captured element, so a pointerup landing outside never arrives where it is
 * expected. Pointers are tracked in a Map and released on window instead.
 */
(function () {
  var root = document.querySelector('.kmap');
  if (!root) return;

  var stage = root.querySelector('.kmap-stage');
  var view = root.querySelector('.kmap-view');
  var sheetLayer = root.querySelector('.kmap-sheet');
  var pins = [].slice.call(root.querySelectorAll('.kmap-pin'));
  var rows = [].slice.call(root.querySelectorAll('.kmap-row'));
  var panel = root.querySelector('.kmap-panel');
  var zoom = root.querySelector('.kmap-zoom');
  var ctl = root.querySelector('.kmap-ctl');
  if (!stage || !view || !pins.length) return;

  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');
  var MINK = 1, MAXK = 7;
  var at = -1, sheetOn = false, loading = false, loaded = false;
  var k = 1, tx = 0, ty = 0;

  function size() { return stage.getBoundingClientRect(); }

  function clamp() {
    var r = size();
    tx = Math.min(0, Math.max(r.width * (1 - k), tx));
    ty = Math.min(0, Math.max(r.height * (1 - k), ty));
  }

  function apply(animate) {
    clamp();
    view.style.transition = animate && !calm.matches
      ? 'transform 260ms cubic-bezier(.4,0,.2,1)' : 'none';
    view.style.transform = 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) +
      'px) scale(' + k.toFixed(4) + ')';
    /* Markers ride the surface but must not grow with it, or a 44px target
       becomes 300px and the labels swamp the map. */
    view.style.setProperty('--kz', (1 / k).toFixed(4));
    stage.classList.toggle('is-zoomed', k > 1.001);
    /* At rest a finger crossing the map must still scroll the page. Once
       zoomed, the gesture belongs to the map. */
    stage.style.touchAction = k > 1.001 ? 'none' : 'pan-y';
    if (ctl) {
      ctl.querySelector('[data-z="in"]').disabled = k >= MAXK - 0.001;
      ctl.querySelector('[data-z="out"]').disabled = k <= MINK + 0.001;
    }
  }

  function zoomAt(nk, ax, ay, animate) {
    nk = Math.min(MAXK, Math.max(MINK, nk));
    if (Math.abs(nk - k) < 0.0005) return;
    tx = ax - (ax - tx) * (nk / k);
    ty = ay - (ay - ty) * (nk / k);
    k = nk;
    apply(animate);
  }

  function reset(animate) { k = 1; tx = 0; ty = 0; apply(animate); }

  var live = new Map(), startK = 1, startD = 0, startMid = null, moved = 0;

  function local(e) {
    var r = size();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  }

  function pair() {
    var a = [];
    live.forEach(function (v) { a.push(v); });
    return a;
  }

  stage.addEventListener('pointerdown', function (e) {
    if (e.target.closest('.kmap-ctl, .kmap-zoom')) return;
    live.set(e.pointerId, local(e));
    moved = 0;
    if (live.size === 2) {
      var p = pair();
      startD = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
      startK = k;
      startMid = { x: (p[0].x + p[1].x) / 2, y: (p[0].y + p[1].y) / 2 };
    }
    /* stops the native image drag, which fires pointercancel instead of
       pointerup and swallows the gesture on the way out */
    if (e.pointerType !== 'touch') e.preventDefault();
  });

  window.addEventListener('pointermove', function (e) {
    if (!live.has(e.pointerId)) return;
    var prev = live.get(e.pointerId);
    var now = local(e);
    live.set(e.pointerId, now);

    if (live.size === 2 && startD > 0) {
      var p = pair();
      var d = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
      var mid = { x: (p[0].x + p[1].x) / 2, y: (p[0].y + p[1].y) / 2 };
      moved += 10;
      zoomAt(startK * (d / startD), mid.x, mid.y, false);
      tx += mid.x - startMid.x;
      ty += mid.y - startMid.y;
      startMid = mid;
      apply(false);
      return;
    }
    if (live.size === 1 && k > 1.001) {
      tx += now.x - prev.x;
      ty += now.y - prev.y;
      moved += Math.abs(now.x - prev.x) + Math.abs(now.y - prev.y);
      apply(false);
    }
  }, { passive: true });

  function release(e) {
    live.delete(e.pointerId);
    if (live.size < 2) { startD = 0; startMid = null; }
  }
  window.addEventListener('pointerup', release);
  window.addEventListener('pointercancel', release);

  stage.addEventListener('wheel', function (e) {
    var out = e.deltaY > 0;
    /* Fully zoomed out and still scrolling out: hand it back to the page, so
       the map can never trap the scroll. */
    if (out && k <= MINK + 0.001) return;
    e.preventDefault();
    var p = local(e);
    zoomAt(k * (out ? 0.88 : 1.14), p.x, p.y, false);
  }, { passive: false });

  stage.addEventListener('dblclick', function (e) {
    if (e.target.closest('.kmap-ctl, .kmap-zoom')) return;
    var p = local(e);
    if (k > 1.001) reset(true); else zoomAt(2.6, p.x, p.y, true);
  });

  if (ctl) {
    ctl.addEventListener('click', function (e) {
      var b = e.target.closest('[data-z]');
      if (!b) return;
      var r = size();
      if (b.dataset.z === 'in') zoomAt(k * 1.6, r.width / 2, r.height / 2, true);
      else if (b.dataset.z === 'out') zoomAt(k / 1.6, r.width / 2, r.height / 2, true);
      else reset(true);
    });
  }

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

  pins.forEach(function (p, i) {
    p.addEventListener('click', function (e) {
      /* a pan that happens to end on a marker is a pan, not a choice */
      if (moved > 6) { e.preventDefault(); return; }
      select(i);
    });
  });
  rows.forEach(function (r, i) {
    r.addEventListener('click', function () { select(i); });
  });

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
        requestAnimationFrame(function () { requestAnimationFrame(then); });
      })
      .catch(function () {
        loading = false;
        if (zoom) { zoom.disabled = true; zoom.textContent = 'Chart unavailable'; }
      });
  }

  function setSheet(on) {
    if (on && !loaded) { loadSheet(function () { setSheet(true); }); return; }
    sheetOn = on;
    stage.classList.toggle('is-sheet', on);
    reset(false);
    place();
    if (zoom) {
      zoom.setAttribute('aria-pressed', on);
      zoom.textContent = on ? 'Back to the overview' : 'Open the chart';
    }
  }

  if (zoom) zoom.addEventListener('click', function () { setSheet(!sheetOn); });

  root.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (k > 1.001) reset(true);
      else if (sheetOn) setSheet(false);
      return;
    }
    if (!stage.contains(document.activeElement)) return;
    var r = size(), step = 40;
    if (e.key === '+' || e.key === '=') zoomAt(k * 1.5, r.width / 2, r.height / 2, true);
    else if (e.key === '-') zoomAt(k / 1.5, r.width / 2, r.height / 2, true);
    else if (e.key === 'ArrowLeft' && k > 1.001) { tx += step; apply(true); }
    else if (e.key === 'ArrowRight' && k > 1.001) { tx -= step; apply(true); }
    else if (e.key === 'ArrowUp' && k > 1.001) { ty += step; apply(true); }
    else if (e.key === 'ArrowDown' && k > 1.001) { ty -= step; apply(true); }
    else return;
    e.preventDefault();
  });

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
    } catch (err) { /* getTotalLength throws on a detached node */ }
  }

  window.addEventListener('resize', function () { apply(false); });
  apply(false);
  place();
  select(0);
})();
