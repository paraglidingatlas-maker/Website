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
  /* Wheel rolls, counted so the map can earn its way forward. Two lifts it
     above the weather drifting down from the gallery, four opens the chart.
     A burst of trackpad events inside 150ms is one roll, or a single flick
     would count as a dozen and skip both stages at once. */
  var rolls = 0, lastRoll = 0;
  var k = 1, tx = 0, ty = 0;

  function size() { return stage.getBoundingClientRect(); }

  /* The stage has a 1px border. getBoundingClientRect measures the border box,
     but .kmap-view and .kmap-pins are both inset:0, so they span the padding
     box inside it. Mixing the two leaves a constant offset that gets multiplied
     by the zoom: 2px of error at 1x became 40px at 6.5x. */
  function inner() { return { w: stage.clientWidth, h: stage.clientHeight }; }

  function clamp() {
    var b = inner();
    tx = Math.min(0, Math.max(b.w * (1 - k), tx));
    ty = Math.min(0, Math.max(b.h * (1 - k), ty));
  }

  function apply(animate) {
    clamp();
    view.style.transition = animate && !calm.matches
      ? 'transform 260ms cubic-bezier(.4,0,.2,1)' : 'none';
    view.style.transform = 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) +
      'px) scale(' + k.toFixed(4) + ')';
    /* Markers live outside this surface, so they are repositioned here rather
       than carried along. This call is the whole registration between map and
       markers: without it they sit still while the map moves under them. */
    place();
    /* will-change only while a gesture is running. Left on permanently it pins
       the layer to a single rasterisation and everything blurs as it scales. */
    view.style.willChange = live.size ? 'transform' : 'auto';
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

  function reset(animate) {
    k = 1; tx = 0; ty = 0; rolls = 0;
    /* the chart stays above the weather: dropping back under it at the exact
       moment it opens is the opposite of what the lift is for */
    if (!sheetOn) root.classList.remove('is-lifted');
    apply(animate);
  }

  /* Two stages, driven by however the person is zooming. Lift above the
     weather at two, open the chart at four.

     A phone has no wheel, so counting wheel events left both stages
     unreachable on touch.

     Converting pinch scale through the wheel's own step does not work: four
     rolls is only 1.69x, and an ordinary pinch passes that in one gesture, so
     the chart opened on the first small pinch. Touch gets its own thresholds,
     chosen so a normal pinch lifts the map and opening the chart takes a
     deliberate second one. */
  var LIFT_SCALE = 1.5, SHEET_SCALE = 3.5;

  function applyStages(n) {
    rolls = Math.max(0, n);
    /* unconditional once the chart is open: recomputing from the count alone
       dropped it back under the weather on the next roll after the switch */
    root.classList.toggle('is-lifted', rolls >= 2 || sheetOn);
    if (rolls >= 4 && !sheetOn && !loading) setSheet(true);
  }

  function countRoll(zoomingOut) {
    var now = (window.performance && performance.now) ? performance.now() : Date.now();
    /* a burst of trackpad events inside 150ms is one roll */
    if (now - lastRoll > 150) applyStages(rolls + (zoomingOut ? -1 : 1));
    lastRoll = now;
  }

  function stagesFromScale() {
    applyStages(k >= SHEET_SCALE ? 4 : (k >= LIFT_SCALE ? 2 : 0));
  }

  var live = new Map(), startK = 1, startD = 0, startMid = null, moved = 0;

  function local(e) {
    var r = size();
    return { x: e.clientX - r.left - stage.clientLeft,
             y: e.clientY - r.top - stage.clientTop };
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
      stagesFromScale();
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
    countRoll(out);
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
      var c = inner();
      if (b.dataset.z === 'in') zoomAt(k * 1.6, c.w / 2, c.h / 2, true);
      else if (b.dataset.z === 'out') zoomAt(k / 1.6, c.w / 2, c.h / 2, true);
      else reset(true);
    });
  }

  /* Markers live outside the transform surface, so their position is computed
     from the same translate and scale the surface uses.
     
     An SVG does not fill its box. preserveAspectRatio defaults to xMidYMid
     meet, so it scales by min(w/vbW, h/vbH) and centres the slack. Here the
     stage is a hair wider than 1900:1500, so the map fits by height and sits
     0.27px in from the left. Assuming it filled the box put every marker out by
     a fraction that the zoom then multiplied.
     
     The two maps have different viewBoxes, so this reads the live one rather
     than hardcoding either. smoke.py checks the result against the browser's
     own getScreenCTM, which is independent of this arithmetic. */
  function place() {
    var b = inner();
    var key = sheetOn ? 'sheet' : 'plate';
    var svg = root.querySelector(sheetOn ? '.kmap-sheet svg' : '.kmap-plate svg');
    if (!svg) return;
    var vb = svg.viewBox.baseVal;
    var s = Math.min(b.w / vb.width, b.h / vb.height);
    var ox = (b.w - vb.width * s) / 2;
    var oy = (b.h - vb.height * s) / 2;
    pins.forEach(function (p) {
      var d = JSON.parse(p.getAttribute('data-' + key));
      var vx = (d.x / 100) * vb.width;
      var vy = (d.y / 100) * vb.height;
      p.style.left = (tx + (ox + vx * s) * k).toFixed(2) + 'px';
      p.style.top = (ty + (oy + vy * s) * k).toFixed(2) + 'px';
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
    root.classList.toggle('is-lifted', on);
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
    var c = inner(), step = 40;
    if (e.key === '+' || e.key === '=') zoomAt(k * 1.5, c.w / 2, c.h / 2, true);
    else if (e.key === '-') zoomAt(k / 1.5, c.w / 2, c.h / 2, true);
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

  /* A window resize is not the only thing that changes this stage's size. An
     image loading further up the page reflows it without any resize event, and
     the markers are positioned in px from that width, so they end up stale:
     measured 11.4px out at 6.6x zoom after the gallery was added above. Watch
     the element, not the window. */
  if ('ResizeObserver' in window) {
    new ResizeObserver(function () { apply(false); }).observe(stage);
  }
  window.addEventListener('resize', function () { apply(false); });
  apply(false);
  place();
  select(0);
})();
