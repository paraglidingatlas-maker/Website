/* V2 PROTOTYPE SHIM (prototypes/v2/ only; never loaded by a live page).

   v2 pages sit two or three folders deeper than the pages they will replace,
   and mirror the live folder layout, so every relative link in their HTML is
   the live link. tools/v2_localize.py rewrites the static ones once. This
   catches what the shared scripts build at run time (episode links from the
   search, the globe, the popup; artwork paths):

   - a link into /prototypes/v2/ whose page has no v2 twin yet is sent to the
     live page instead, at the moment it is used (pointerdown, click, focus);
   - an image or video that fails to load from /prototypes/v2/ is retried
     from the live path.

   V2_PAGES is the list of built pages; tools/v2_localize.py rewrites it. */
(function () {
  var V2_PAGES = [/*v2-pages*/"about.html","destinations/india.html","destinations/kenya.html","index.html","library.html","podcast.html","styleguide.html"/*/v2-pages*/];
  var M = location.pathname.match(/^(.*\/prototypes\/v2\/)/);
  if (!M) return;
  var BASE = M[1];
  var LIVE = BASE.replace(/prototypes\/v2\/$/, '');
  var have = {};
  V2_PAGES.forEach(function (p) { have[BASE + p] = 1; });

  function live(u) { return LIVE + u.pathname.slice(BASE.length) + u.search + u.hash; }
  function fixLink(a) {
    if (!a || !a.href || a.dataset.v2) return;
    var u; try { u = new URL(a.href, location.href); } catch (e) { return; }
    if (u.origin !== location.origin || u.pathname.indexOf(BASE) !== 0) return;
    var p = u.pathname; if (/\/$/.test(p)) p += 'index.html';
    // the globe moved from the homepage to the podcast page in v2
    if (p === BASE + 'index.html' && /^#pin=/.test(u.hash)) { a.href = BASE + 'podcast.html' + u.hash; a.dataset.v2 = 'pin'; return; }
    if (!have[p] && !/\.(css|js|json|xml|txt)$/.test(p)) { a.href = live(u); a.dataset.v2 = 'live'; }
  }
  ['pointerdown', 'click', 'focusin', 'auxclick', 'mouseover'].forEach(function (t) {
    document.addEventListener(t, function (e) { fixLink(e.target.closest && e.target.closest('a[href]')); }, true);
  });
  window.addEventListener('error', function (e) {
    var el = e.target;
    if (!el || !/^(IMG|VIDEO|SOURCE|AUDIO)$/.test(el.tagName) || el.dataset.v2) return;
    var src = el.currentSrc || el.src; if (!src) return;
    var u; try { u = new URL(src, location.href); } catch (x) { return; }
    if (u.pathname.indexOf(BASE) !== 0) return;
    el.dataset.v2 = 'live';
    var pic = el.parentNode && el.parentNode.tagName === 'PICTURE' ? el.parentNode : null;
    if (pic) pic.querySelectorAll('source').forEach(function (s) {
      s.srcset = s.srcset.split(',').map(function (c) {
        var bits = c.trim().split(/\s+/); try { bits[0] = live(new URL(bits[0], location.href)); } catch (x) {}
        return bits.join(' ');
      }).join(', ');
    });
    el.src = live(u);
  }, true);
})();
