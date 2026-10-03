#!/usr/bin/env python3
"""
v4 as an app on the phone (owner, 3 Oct 2026: "go with option 1 in v4").

Option 1 is an installable web app: the same pages, added to the home screen
with their own icon, opening full screen without the browser bar, and still
readable with no signal. A store app (option 3, owner: "at some point") would
start from the same manifest, icons and offline rules.

What this writes into prototypes/v4/:
  manifest.webmanifest   name, icons, colours, opens full screen at the home page
  img/app-*.png          the icons, from the site's own logo on its own black
  sw.js                  the service worker (offline rules below)
  pwa.js                 registers it; "Install the app" in the footer
  offline.html           shown for a page that was never opened while online
and adds the manifest, the iOS home-screen tags and pwa.js to every v4 page.

OFFLINE RULES (sw.js)
  - A page is fetched from the network first and kept; with no signal the kept
    copy is shown, or offline.html when there is none. So every page read
    once is readable on the hill.
  - Styles, scripts, fonts and pictures are served from the phone and
    refreshed in the background.
  - Video, audio and anything from another site (YouTube, the podcast host)
    is never stored: it is large, and a stored copy of a stream does not play.
  - The cache name carries a hash of the app files, so a new build replaces
    the old copies.

Idempotent. Run after any tool that rewrites v4 pages.

    python3 tools/v4_pwa.py
"""
import hashlib
import json
import os
import re
import subprocess
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
BG = (20, 21, 25)                     # --bg
LOGO = os.path.join(ROOT, "assets", "logo", "atlas-favicon-source.png")


def icons():
    logo = Image.open(LOGO).convert("RGBA")
    out = os.path.join(V4, "img")
    os.makedirs(out, exist_ok=True)
    for size, frac, name in ((192, 0.78, "app-192.png"), (512, 0.78, "app-512.png"),
                             (512, 0.6, "app-maskable-512.png"), (180, 0.78, "app-180.png")):
        # The wordmark across the middle of a black square. A maskable icon
        # keeps it inside the centre 60%, which every launcher's mask leaves.
        im = Image.new("RGBA", (size, size), BG + (255,))
        w = int(size * frac)
        h = int(logo.height * w / logo.width)
        im.alpha_composite(logo.resize((w, h), Image.LANCZOS), ((size - w) // 2, (size - h) // 2))
        im.convert("RGB").save(os.path.join(out, name), optimize=True)


MANIFEST = {
    "name": "Paragliding Atlas",
    "short_name": "Atlas",
    "description": "The Paragliding Atlas podcast, knowledge base and trips, on your phone.",
    "id": "./",
    "start_url": "./index.html",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#141519",
    "theme_color": "#141519",
    "icons": [
        {"src": "img/app-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "img/app-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "img/app-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
    "shortcuts": [
        {"name": "Episode library", "url": "./library.html"},
        {"name": "Knowledge base", "url": "./knowledge-base.html"},
        {"name": "Trips", "url": "./index.html#destinations"},
    ],
}

SW = r"""/* Paragliding Atlas, v4 app: offline rules. Written by tools/v4_pwa.py;
   edit that file, not this one. */
const VERSION = '%(version)s';
const SHELL = 'atlas-shell-' + VERSION;
const PAGES = 'atlas-pages';
const ASSETS = 'atlas-assets-' + VERSION;
const PAGE_LIMIT = 80;
const PRECACHE = %(precache)s;

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
"""

PWA_JS = r"""/* Paragliding Atlas, v4 app: registers the offline rules (sw.js) and offers
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
"""

CSS = """
/* ===== The app (tools/v4_pwa.py) ===== */
.pwa-install{order:-1;background:none;border:1px solid var(--live);color:var(--white);
  font:600 var(--fs-small)/1 var(--font-body);padding:.6rem .9rem;min-height:44px;cursor:pointer;margin-right:.6rem;}
.pwa-install:hover,.pwa-install:focus-visible{border-color:var(--orange);color:var(--orange);}
.pwa-sheet{position:fixed;left:12px;right:12px;bottom:max(12px,env(safe-area-inset-bottom));z-index:1000;
  max-width:28rem;margin:0 auto;padding:1.1rem 1.2rem 1.2rem;background:var(--card);border:1px solid var(--live);
  display:grid;gap:.6rem;color:var(--gray-light);font-size:var(--fs-body-s);}
.pwa-sheet[hidden]{display:none;}
.pwa-sheet b{color:var(--white);}
.pwa-sheet button{justify-self:start;background:var(--orange);color:var(--ink);border:0;font-weight:700;
  padding:.65rem 1.1rem;min-height:44px;cursor:pointer;}
/* Opened from the home screen: no browser bar above the header. */
.is-app .page-wrap > nav{padding-top:max(1.5rem,env(safe-area-inset-top));}
"""

OFFLINE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>Offline: Paragliding Atlas</title>
<meta name="description" content="No signal. The pages you have read are still here.">
<link rel="canonical" href="https://paraglidingatlas.com/">
<link rel="icon" type="image/png" href="/prototypes/v4/img/favicon-96.png">
<meta name="theme-color" content="#141519">
<!-- Site-absolute links: this page is shown in place of a page in any folder,
     so a relative link would resolve against that folder. -->
<link rel="stylesheet" href="/fonts.css">
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/prototypes/v4/v2.css">
<style>
.off{max-width:46rem;margin:0 auto;padding:clamp(3rem,10vw,6rem) clamp(1.2rem,5vw,3rem);display:grid;gap:1.2rem;}
.off h1{font-family:var(--font-display);font-size:var(--fs-h1);line-height:1.1;margin:0;}
.off p{color:var(--gray-light);margin:0;max-width:36rem;}
.off ul{list-style:none;margin:.6rem 0 0;padding:0;border-top:1px solid var(--line);}
.off li{border-bottom:1px solid var(--line);}
.off li a{display:block;padding:.85rem 0;min-height:44px;color:var(--white);}
.off li a:hover{color:var(--orange);}
.off .none{color:var(--gray);}
</style>
</head>
<body>
<main class="off">
  <span class="kicker">No Signal</span>
  <h1>You Are Offline</h1>
  <p>This page was never opened while you had a connection, so it is not on your phone. Everything you have read before is still here.</p>
  <ul id="saved"><li class="none">Looking for saved pages&hellip;</li></ul>
</main>
<script>
(function () {
  var ul = document.getElementById('saved');
  if (!('caches' in window)) { ul.innerHTML = '<li class="none">Saved pages need a newer browser.</li>'; return; }
  caches.open('atlas-pages').then(function (c) { return c.keys().then(function (keys) {
    return Promise.all(keys.map(function (k) {
      return c.match(k).then(function (r) { return r.text(); }).then(function (t) {
        var m = /<title>([^<]*)<\\/title>/i.exec(t);
        return { url: k.url, title: m ? m[1].replace(/\\s*[|:]\\s*Paragliding Atlas$/, '') : k.url };
      });
    }));
  }); }).then(function (pages) {
    pages = pages.filter(function (p) { return !/offline\\.html/.test(p.url); });
    if (!pages.length) { ul.innerHTML = '<li class="none">Nothing saved yet. Pages you open while online are kept here.</li>'; return; }
    ul.innerHTML = '';
    pages.forEach(function (p) {
      var li = document.createElement('li'), a = document.createElement('a');
      a.href = p.url; a.textContent = p.title; li.appendChild(a); ul.appendChild(li);
    });
  }).catch(function () { ul.innerHTML = '<li class="none">Saved pages could not be read.</li>'; });
})();
</script>
</body>
</html>
"""


def pages():
    for d, dirs, files in os.walk(V4):
        dirs[:] = [x for x in dirs if x not in ("src", "samples", "fonts", "img")]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def main():
    icons()
    json.dump(MANIFEST, open(os.path.join(V4, "manifest.webmanifest"), "w"), indent=1)
    open(os.path.join(V4, "offline.html"), "w", encoding="utf-8").write(OFFLINE)
    open(os.path.join(V4, "pwa.js"), "w", encoding="utf-8").write(PWA_JS)

    # The app's own styles go at the end of v2.css's source, between markers,
    # and the minifier then writes v2.css from it as for every other v4 style.
    css = os.path.join(V4, "src", "v2.css")
    s = open(css, encoding="utf-8").read()
    s = re.sub(r"\n?/\* app:start \*/.*?/\* app:end \*/\n?", "", s, flags=re.S)
    open(css, "w", encoding="utf-8").write(s.rstrip("\n") + "\n/* app:start */" + CSS + "/* app:end */\n")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "v4_min.py")], check=True,
                   stdout=subprocess.DEVNULL)

    shell = ["offline.html", "v2.css", "v2.js", "v2-immersive.js", "v4-menu.js", "v4-listen.js", "pwa.js",
             "../../styles.css", "../../fonts.css", "../../assets/logo/atlas-logo-white.png",
             "img/app-192.png"]
    h = hashlib.sha256()
    for f in shell:
        h.update(open(os.path.normpath(os.path.join(V4, f)), "rb").read())
    h.update(SW.encode())
    open(os.path.join(V4, "sw.js"), "w", encoding="utf-8").write(
        SW % {"version": h.hexdigest()[:10], "precache": json.dumps(shell)})

    n = 0
    for fp in pages():
        rel = os.path.relpath(fp, V4)
        up = os.path.relpath(V4, os.path.dirname(fp)).replace(os.sep, "/")
        up = "" if up == "." else up + "/"
        s = open(fp, encoding="utf-8").read()
        s = re.sub(r"<!-- app -->.*?<!-- /app -->\n?", "", s, flags=re.S)
        if rel == "offline.html":
            continue
        tags = ('<!-- app --><link rel="manifest" href="%smanifest.webmanifest">\n'
                '<meta name="apple-mobile-web-app-capable" content="yes">\n'
                '<meta name="mobile-web-app-capable" content="yes">\n'
                '<meta name="apple-mobile-web-app-title" content="Atlas">\n'
                '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
                '<link rel="apple-touch-icon" sizes="180x180" href="%simg/app-180.png">\n'
                '<script defer src="%spwa.js"></script><!-- /app -->\n' % (up, up, up))
        s = s.replace("</head>", tags + "</head>", 1)
        open(fp, "w", encoding="utf-8").write(s)
        n += 1
    print("v4 app: manifest, icons, sw.js (%s), offline page, %d pages" % (h.hexdigest()[:10], n))


if __name__ == "__main__":
    main()
