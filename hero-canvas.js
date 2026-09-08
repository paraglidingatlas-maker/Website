// Hero WebGL particle field — a drifting layer of glowing dust/embers over the
// hero photo, with subtle camera parallax that follows the cursor. Falls back
// to nothing (just the photo) if WebGL or Three.js isn't available, or if the
// person has reduced-motion enabled.
(function () {
  const container = document.querySelector('.hero-media');
  const hero = document.querySelector('.hero');
  if (!container || !hero || !window.THREE) return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) return;

  let width = hero.clientWidth;
  let height = hero.clientHeight;

  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(width, height);
  renderer.domElement.style.position = 'absolute';
  renderer.domElement.style.inset = '0';
  renderer.domElement.style.zIndex = '2';
  renderer.domElement.style.pointerEvents = 'none';
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 100);
  camera.position.z = 12;

  // Soft circular sprite for each particle, drawn on a canvas (no external image needed)
  function makeSprite() {
    const size = 64;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');
    const grad = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.4, 'rgba(255,200,150,0.6)');
    grad.addColorStop(1, 'rgba(255,150,50,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, size, size);
    return new THREE.CanvasTexture(c);
  }

  const particleCount = window.innerWidth < 700 ? 500 : 1200;
  const positions = new Float32Array(particleCount * 3);
  const speeds = new Float32Array(particleCount);

  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 24;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 14;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 16;
    speeds[i] = 0.15 + Math.random() * 0.35;
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

  const material = new THREE.PointsMaterial({
    size: 0.09,
    map: makeSprite(),
    transparent: true,
    opacity: 0.55,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });

  const points = new THREE.Points(geometry, material);
  scene.add(points);

  // Cursor parallax target, smoothed with simple lerp each frame
  let targetX = 0, targetY = 0, camX = 0, camY = 0;
  hero.addEventListener('mousemove', (e) => {
    const rect = hero.getBoundingClientRect();
    targetX = ((e.clientX - rect.left) / rect.width - 0.5) * 1.4;
    targetY = ((e.clientY - rect.top) / rect.height - 0.5) * 1.4;
  });

  function animate() {
    requestAnimationFrame(animate);

    const pos = geometry.attributes.position.array;
    for (let i = 0; i < particleCount; i++) {
      pos[i * 3 + 1] += speeds[i] * 0.008;
      if (pos[i * 3 + 1] > 7) pos[i * 3 + 1] = -7;
    }
    geometry.attributes.position.needsUpdate = true;

    camX += (targetX - camX) * 0.04;
    camY += (targetY - camY) * 0.04;
    camera.position.x = camX;
    camera.position.y = -camY;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    width = hero.clientWidth;
    height = hero.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  });
})();
