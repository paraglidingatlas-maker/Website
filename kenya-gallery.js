/* Kenya photograph carousel.
 *
 * A ring, not a row: cards take the shortest way round, so there is no end to
 * reach in either direction. The one card that has to jump from the far right
 * to the far left does it while it is invisible, which is why the wrap is never
 * seen.
 *
 * Spread is measured against the stage, not the card. Measured against the card
 * it changed every time the card shape changed, which looked like the spacing
 * drifting on its own.
 *
 * Crops are centred on the canopy, not on the middle of the frame. A 2:3
 * portrait card keeps 44% of a 3:2 photograph, so centring matters: the wing
 * position in each picture was found by saturation and is baked into
 * data-x and data-y by tools/build_kenya_gallery.py.
 *
 * NO setPointerCapture. It is in the gotcha notes and it is what broke the
 * homepage rail.
 */
(function () {
  var root = document.querySelector('.cfl');
  if (!root) return;

  var stage = root.querySelector('.cfl-stage');
  var tiltEl = root.querySelector('.cfl-tilt');
  var cards = [].slice.call(root.querySelectorAll('.cfl-card'));
  var live = root.querySelector('.cfl-live');
  var dots = [].slice.call(root.querySelectorAll('.cfl-dot'));
  var bgs = [].slice.call(root.querySelectorAll('.cfl-bg'));
  var clouds = [].slice.call(root.querySelectorAll('.cfl-cloud'));
  var lb = root.querySelector('.cfl-lb');
  var lbImgs = [].slice.call(root.querySelectorAll('.cfl-full'));
  var lbCap = root.querySelector('.cfl-lb-cap');
  if (!stage || cards.length < 2) return;

  var N = cards.length, VIS = Math.min(5, Math.floor(N / 2));
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');
  var at = 0, moved = 0;

  function ring(i) {
    var d = ((i - at) % N + N) % N;
    return d > N / 2 ? d - N : d;
  }

  function layout() {
    var unit = stage.getBoundingClientRect().width * 0.30;
    var gap = 0.42, rot = 32, fall = 0.085, depth = 150;
    cards.forEach(function (c, i) {
      var d = ring(i), a = Math.abs(d), hidden = a >= VIS;
      c.style.transform = 'translate(-50%,-50%) translateX(' + (d * unit * gap).toFixed(1) +
        'px) translateZ(' + (-a * depth) + 'px) rotateY(' +
        (d === 0 ? 0 : (d < 0 ? rot : -rot)) + 'deg) scale(' +
        Math.max(0.45, 1 - a * fall).toFixed(3) + ')';
      c.style.zIndex = String(100 - a);
      c.style.filter = 'brightness(' + (d === 0 ? 1 : Math.max(0.52, 1 - a * 0.13)) + ')';
      c.style.opacity = hidden ? '0' : String(Math.max(0.5, 1 - a * 0.1));
      c.style.pointerEvents = hidden ? 'none' : 'auto';
      /* a card only crosses the ring while invisible; leaving the transition on
         would send it flying the width of the section to get home */
      c.style.transitionProperty = hidden ? 'none' : 'transform,filter,opacity';
      c.setAttribute('aria-hidden', hidden ? 'true' : 'false');
      c.tabIndex = d === 0 ? 0 : -1;
    });
    cards.forEach(function (c, i) { c.classList.toggle('is-front', ring(i) === 0); });
    if (live) live.textContent = cards[at].getAttribute('data-title') || '';
    dots.forEach(function (e, i) {
      e.classList.toggle('is-on', i === at);
      e.setAttribute('aria-current', i === at);
    });
    bgs.forEach(function (e, i) { e.classList.toggle('is-on', i === at); });
  }

  function go(n) { at = ((n % N) + N) % N; layout(); }

  cards.forEach(function (c, i) {
    c.addEventListener('click', function () {
      if (Math.abs(moved) > 6) return;          /* that was a drag */
      var d = ring(i);
      if (d === 0) openLb(i); else go(at + d);
    });
  });
  dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });
  var prev = root.querySelector('.cfl-prev'), next = root.querySelector('.cfl-next');
  if (prev) prev.addEventListener('click', function () { go(at - 1); });
  if (next) next.addEventListener('click', function () { go(at + 1); });

  /* ---- full size ------------------------------------------------------- */
  var lbAt = 0;
  function openLb(i) {
    lbAt = i;
    lbImgs.forEach(function (f, n) { f.classList.toggle('is-on', n === i); });
    if (lbCap) lbCap.textContent = cards[i].getAttribute('data-title') || '';
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
    var x = lb.querySelector('.cfl-lb-x');
    if (x) x.focus();
  }
  function closeLb() {
    lb.hidden = true;
    document.body.style.overflow = '';
    cards[at].focus();
  }
  function stepLb(n) {
    lbAt = ((n % N) + N) % N;
    lbImgs.forEach(function (f, k) { f.classList.toggle('is-on', k === lbAt); });
    if (lbCap) lbCap.textContent = cards[lbAt].getAttribute('data-title') || '';
    go(lbAt);
  }
  if (lb) {
    lb.addEventListener('click', function (e) {
      if (e.target.closest('.cfl-lb-nav, .cfl-full')) return;
      closeLb();
    });
    lb.querySelector('.cfl-lb-x').addEventListener('click', closeLb);
    lb.querySelector('.cfl-lb-prev').addEventListener('click', function () { stepLb(lbAt - 1); });
    lb.querySelector('.cfl-lb-next').addEventListener('click', function () { stepLb(lbAt + 1); });
  }

  root.addEventListener('keydown', function (e) {
    var open = lb && !lb.hidden;
    if (e.key === 'Escape' && open) { closeLb(); e.preventDefault(); return; }
    if (e.key === 'ArrowRight') { open ? stepLb(lbAt + 1) : go(at + 1); }
    else if (e.key === 'ArrowLeft') { open ? stepLb(lbAt - 1) : go(at - 1); }
    else if ((e.key === 'Enter' || e.key === ' ') && !open &&
             document.activeElement === cards[at]) { openLb(at); }
    else return;
    e.preventDefault();
  });

  /* ---- drag ------------------------------------------------------------ */
  var x0 = null;
  stage.addEventListener('pointerdown', function (e) {
    if (e.target.closest('button')) return;
    x0 = e.clientX; moved = 0;
    if (e.pointerType !== 'touch') e.preventDefault();
  });
  window.addEventListener('pointermove', function (e) {
    if (x0 !== null) moved = e.clientX - x0;
  }, { passive: true });
  window.addEventListener('pointerup', function () {
    if (x0 === null) return;
    if (Math.abs(moved) > 45) go(at + (moved < 0 ? 1 : -1));
    x0 = null;
  });
  window.addEventListener('pointercancel', function () { x0 = null; });

  /* ---- cursor lean ----------------------------------------------------- */
  var wantX = 0, wantY = 0, haveX = 0, haveY = 0, running = false;
  root.addEventListener('pointermove', function (e) {
    var r = root.getBoundingClientRect();
    wantX = ((e.clientX - r.left) / r.width) * 2 - 1;
    wantY = ((e.clientY - r.top) / r.height) * 2 - 1;
  });
  root.addEventListener('pointerleave', function () { wantX = 0; wantY = 0; });

  /* ---- clouds ---------------------------------------------------------- */
  function drift() {
    running = false;
    var r = root.getBoundingClientRect();
    var p = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
    clouds.forEach(function (c) {
      var sp = parseFloat(c.getAttribute('data-sp')) || 0;
      /* 210 gave 344px of vertical travel across the whole page, which is
         real and not noticeable. 760 gives 576px across the gallery alone. */
      c.style.transform = 'translate3d(' + (p * sp * 90).toFixed(1) + 'px,' +
        (p * sp * 760).toFixed(1) + 'px,0)';
    });
  }
  window.addEventListener('scroll', function () {
    if (!running) { running = true; requestAnimationFrame(drift); }
  }, { passive: true });

  function frame() {
    haveX += (wantX - haveX) * 0.065;
    haveY += (wantY - haveY) * 0.065;
    if (tiltEl) {
      tiltEl.style.transform = 'rotateY(' + (haveX * 9).toFixed(2) + 'deg) rotateX(' +
        (-haveY * 5).toFixed(2) + 'deg) translateX(' + (-haveX * 23).toFixed(1) + 'px)';
    }
    stage.style.setProperty('--px', (50 + haveX * 14).toFixed(1) + '%');
    stage.style.setProperty('--py', (50 + haveY * 8).toFixed(1) + '%');
    requestAnimationFrame(frame);
  }

  window.addEventListener('resize', layout);
  layout();
  drift();
  if (!calm.matches) frame();
})();
