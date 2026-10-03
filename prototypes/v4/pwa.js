/* Paragliding Atlas, v4 app: registers the offline rules (sw.js) and offers
   "Install the app" in the footer. Written by tools/v4_pwa.py. */
(function () {
  'use strict';
  var root = document.currentScript ? document.currentScript.src.replace(/pwa\.js.*$/, '') : '';
  var standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  if (standalone) document.documentElement.classList.add('is-app');
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register(root + 'sw.js').catch(function () {});
    });
  }
  if (standalone) return;

  var deferred = null;
  var ios = /iphone|ipad|ipod/i.test(navigator.userAgent) && !window.MSStream;
  function button(label, onClick) {
    var bar = document.querySelector('.footer-bottom');
    if (!bar || bar.querySelector('.pwa-install')) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'pwa-install';
    b.textContent = label;
    b.addEventListener('click', onClick);
    bar.insertBefore(b, bar.firstChild);
  }
  function sheet() {
    var s = document.querySelector('.pwa-sheet');
    if (s) { s.hidden = false; s.querySelector('button').focus(); return; }
    s = document.createElement('div');
    s.className = 'pwa-sheet';
    s.setAttribute('role', 'dialog');
    s.setAttribute('aria-label', 'Install the app');
    s.innerHTML = '<p class="kicker">On iPhone and iPad</p>' +
      '<p>Tap <b>Share</b> at the bottom of Safari, then <b>Add to Home Screen</b>. ' +
      'Paragliding Atlas then opens from its own icon, full screen, and keeps every page you read for when there is no signal.</p>' +
      '<button type="button">Got it</button>';
    s.querySelector('button').addEventListener('click', function () { s.hidden = true; });
    document.body.appendChild(s);
    s.querySelector('button').focus();
  }
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    button('Install the app', function () {
      deferred.prompt();
      deferred.userChoice.finally(function () { deferred = null; });
    });
  });
  if (ios) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { button('Install the app', sheet); });
    else button('Install the app', sheet);
  }
})();
