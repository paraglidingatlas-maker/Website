/* Paragliding Atlas, v4 app: offline rules. Written by tools/v4_pwa.py;
   edit that file, not this one. */
const VERSION = '2d8a99f462';
const SHELL = 'atlas-shell-' + VERSION;
const PAGES = 'atlas-pages';
const ASSETS = 'atlas-assets-' + VERSION;
const PAGE_LIMIT = 80;
const PRECACHE = ["offline.html", "v2.css", "v2.js", "v2-immersive.js", "v4-menu.js", "v4-listen.js", "pwa.js", "../../styles.css", "../../fonts.css", "../../assets/logo/atlas-logo-white.png", "img/app-192.png"];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(SHELL).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys
    .filter((k) => k.startsWith('atlas-') && k !== SHELL && k !== ASSETS && k !== PAGES)
    .map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

function trim(cache, max) {
  return cache.keys().then((keys) => keys.length > max
    ? cache.delete(keys[0]).then(() => trim(cache, max)) : null);
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;            /* YouTube, podcast host */
  if (req.headers.has('range') || /\.(mp4|webm|m4a|mp3)$/i.test(url.pathname)) return;

  if (req.mode === 'navigate') {
    /* Network first, kept for later; the kept copy or the offline page without signal. */
    e.respondWith(fetch(req).then((res) => {
      if (res.ok) {
        const copy = res.clone();
        caches.open(PAGES).then((c) => c.put(url.pathname, copy).then(() => trim(c, PAGE_LIMIT)));
      }
      return res;
    }).catch(() => caches.open(PAGES).then((c) => c.match(url.pathname))
      .then((hit) => hit || caches.match('offline.html', { ignoreSearch: true }))));
    return;
  }

  /* Everything else from this site: from the phone at once, refreshed behind. */
  e.respondWith(caches.match(req).then((hit) => {
    const net = fetch(req).then((res) => {
      if (res.ok && res.type === 'basic') {
        const copy = res.clone();
        caches.open(ASSETS).then((c) => c.put(req, copy));
      }
      return res;
    }).catch(() => hit || caches.match(req, { ignoreSearch: true }));
    return hit || net;
  }));
});
