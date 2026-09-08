const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Topo map parallax (About page) — subtle vertical drift as the section scrolls by
const topoBg = document.getElementById('topoBg');
const discoverSection = document.getElementById('discoverSection');
if (topoBg && discoverSection && !reduced) {
  let ticking = false;
  function updateParallax() {
    const rect = discoverSection.getBoundingClientRect();
    const viewportMid = window.innerHeight / 2;
    const sectionMid = rect.top + rect.height / 2;
    const offset = (viewportMid - sectionMid) * 0.08;
    topoBg.style.transform = `translateY(${offset}px)`;
    ticking = false;
  }
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(updateParallax);
      ticking = true;
    }
  });
  updateParallax();
}
if (!reduced) {
  const revealTargets = document.querySelectorAll(
    '.destination, .why-card, .cta-card, .ep-card, .newsletter, .ep-map-section'
  );

  if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    revealTargets.forEach((el, i) => {
      gsap.from(el, {
        opacity: 0,
        y: 40,
        duration: 0.9,
        delay: (i % 5) * 0.06,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          toggleActions: 'play none none none',
        },
      });
    });
  } else {
    // Fallback: plain CSS-transition reveal if GSAP failed to load
    revealTargets.forEach((el) => el.classList.add('reveal'));
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
    revealTargets.forEach((el) => observer.observe(el));
  }
}
