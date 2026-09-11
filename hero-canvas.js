// Hero particle field — a drifting layer of glowing dust/embers over the hero
// photo, with subtle parallax that follows the cursor.
//
// This used to run on three.js. It used exactly nine symbols from it, and the
// library cost 654 KB, almost all of which was WebGLRenderer dragging in three's
// entire shader and material system in order to draw soft dots. Tree-shaking got
// that to 454 KB, which was still absurd for this. It is now plain 2D canvas
// with no dependency at all.
//
// Every constant here is the one the three.js version used: 500/1200 particles
// in a 24 x 14 x 16 box, rise speed 0.15 to 0.35 scaled by 0.008 a frame,
// wrapping from y > 7 back to -7, the same white-to-ember sprite gradient, the
// same 0.55 opacity, the same 55 degree field of view from z = 12, and the same
// 0.04 lerp toward a cursor target scaled by 1.4. Additive blending uses the
// 'lighter' composite operation, which is what WebGL AdditiveBlending does.
//
// Falls back to just the photo if 2D canvas is unavailable or the person has
// asked for reduced motion.
(function () {
  const container = document.querySelector('.hero-media');
  const hero = document.querySelector('.hero');
  if (!container || !hero) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  canvas.style.position = 'absolute';
  canvas.style.inset = '0';
  canvas.style.zIndex = '2';
  canvas.style.pointerEvents = 'none';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  container.appendChild(canvas);

  let width = 0, height = 0, dpr = 1;
  function resize() {
    width = hero.clientWidth;
    height = hero.clientHeight;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.max(1, Math.round(width * dpr));
    canvas.height = Math.max(1, Math.round(height * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize();

  /* The same soft circular sprite, drawn once to an offscreen canvas. */
  const SPRITE = (function () {
    const size = 64;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const g = c.getContext('2d');
    const grad = g.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.4, 'rgba(255,200,150,0.6)');
    grad.addColorStop(1, 'rgba(255,150,50,0)');
    g.fillStyle = grad;
    g.fillRect(0, 0, size, size);
    return c;
  })();

  const COUNT = window.innerWidth < 700 ? 500 : 1200;
  const CAM_Z = 12;
  const FOV = 55 * Math.PI / 180;
  const POINT_SIZE = 0.09;

  const px = new Float32Array(COUNT);
  const py = new Float32Array(COUNT);
  const pz = new Float32Array(COUNT);
  const speed = new Float32Array(COUNT);
  for (let i = 0; i < COUNT; i++) {
    px[i] = (Math.random() - 0.5) * 24;
    py[i] = (Math.random() - 0.5) * 14;
    pz[i] = (Math.random() - 0.5) * 16;
    speed[i] = 0.15 + Math.random() * 0.35;
  }

  let targetX = 0, targetY = 0, camX = 0, camY = 0;
  hero.addEventListener('mousemove', function (e) {
    const r = hero.getBoundingClientRect();
    targetX = ((e.clientX - r.left) / r.width - 0.5) * 1.4;
    targetY = ((e.clientY - r.top) / r.height - 0.5) * 1.4;
  });

  /* Only run while the hero is on screen. Without this the loop competes with
     the page's scroll smoothing further down and makes scrolling feel heavy. */
  let visible = true;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; },
                             { threshold: 0 }).observe(hero);
  }

  function frame() {
    requestAnimationFrame(frame);
    if (!visible || width === 0) return;

    camX += (targetX - camX) * 0.04;
    camY += (targetY - camY) * 0.04;

    ctx.clearRect(0, 0, width, height);
    ctx.globalCompositeOperation = 'lighter';
    ctx.globalAlpha = 0.55;

    /* Perspective divide, matching a 55 degree camera sitting at z = 12.
       Depth drives both position and size, so near particles drift further
       under the cursor than distant ones, which is the parallax. */
    const f = (height / 2) / Math.tan(FOV / 2);
    const hw = width / 2, hh = height / 2;

    for (let i = 0; i < COUNT; i++) {
      py[i] += speed[i] * 0.008;
      if (py[i] > 7) py[i] = -7;

      const depth = CAM_Z - pz[i];
      if (depth < 0.1) continue;
      const k = f / depth;
      const sx = hw + (px[i] - camX) * k;
      const sy = hh - (py[i] + camY) * k;
      const s = POINT_SIZE * k;
      if (s < 0.35 || sx < -s || sx > width + s || sy < -s || sy > height + s) continue;
      ctx.drawImage(SPRITE, sx - s / 2, sy - s / 2, s, s);
    }

    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'source-over';
  }
  frame();

  window.addEventListener('resize', resize);
})();
