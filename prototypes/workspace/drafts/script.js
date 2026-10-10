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

/* ===== Feedback, haptics and page transitions ==============================
 * Shared by every page. tools/inject_nav_menu.py adds this file to any page
 * that did not already load it, so the episode pages, the library and the
 * sitemap get it too. The visual side is the Feedback and Page transitions
 * sections at the end of styles.css; this is only what CSS cannot do.
 */
(function () {
  "use strict";
  var d = document;
  var PGA = window.PGA = window.PGA || {};

  /* THE SKY KEEPS THE VISITOR'S TIME. dawn, day, dusk or night from their own
   * clock, read into data-sky on <html>; the colours are in styles.css. Checked
   * again every ten minutes, so a page left open drifts from one to the next. */
  function sky() {
    var h = new Date().getHours();
    d.documentElement.setAttribute("data-sky",
      h >= 5 && h < 9 ? "dawn" : h >= 9 && h < 17 ? "day" : h >= 17 && h < 21 ? "dusk" : "night");
  }
  sky(); setInterval(sky, 600000);

  /* LOOPING FOOTAGE. <video data-loop="../assets/video/bir"> becomes that loop,
   * in WebM where the browser is sure of it and MP4 otherwise (and as the
   * fallback), 1080p or 720p by screen, or 720p always with data-loop-size.
   * It plays only while on screen and, with data-loop-when, only while the
   * named ancestor carries is-on (a slideshow slide). It fades in over the
   * photograph it sits on once it is actually playing. Nobody gets it who
   * asked for less: reduced motion, Save-Data, or a 2G/3G connection keep the
   * photograph. The homepage hero has its own copy of this, inline, so it can
   * start before this file loads. */
  (function () {
    var vids = [].slice.call(d.querySelectorAll("video[data-loop]"));
    if (!vids.length) return;
    var mm = function (q) { return window.matchMedia && matchMedia(q).matches; };
    var c = navigator.connection || {};
    if (mm("(prefers-reduced-motion: reduce)") || c.saveData || /(^|-)(2g|3g)$/.test(c.effectiveType || "")) return;
    var small = Math.max(screen.width, screen.height) * Math.min(devicePixelRatio || 1, 2) < 1700 || mm("(max-width: 820px)");
    vids.forEach(function (v) {
      if (!v.play) return;
      var base = v.getAttribute("data-loop") + "-" + (v.getAttribute("data-loop-size") || (small ? "720" : "1080"));
      var webm = v.canPlayType && v.canPlayType('video/webm; codecs="vp9"') === "probably";
      var host = v.getAttribute("data-loop-when") ? v.closest(v.getAttribute("data-loop-when")) : null;
      var seen = false, loaded = false;
      function want() { return seen && (!host || host.classList.contains("is-on")) && !d.hidden; }
      function sync() {
        if (!want()) { v.pause(); return; }
        if (!loaded) {
          loaded = true;
          v.src = base + (webm ? ".webm" : ".mp4");
          if (webm) v.addEventListener("error", function () { v.src = base + ".mp4"; sync(); }, { once: true });
        }
        var p = v.play(); if (p && p.catch) p.catch(function () {});
      }
      v.addEventListener("playing", function () { v.classList.add("is-playing"); });
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (en) { seen = en[0].isIntersecting; sync(); },
                                 { rootMargin: "200px 0px" }).observe(v);
      } else { seen = true; }
      if (host) new MutationObserver(sync).observe(host, { attributes: true, attributeFilter: ["class"] });
      d.addEventListener("visibilitychange", sync);
      sync();
    });
  })();

  // iOS applies :active only while something on the page listens for
  // touchstart. Without this the pressed state never shows under a finger.
  d.addEventListener("touchstart", function () {}, { passive: true });

  /* HAPTICS. The helper the knowledge base door introduced, moved here so the
   * door and the key buttons share one. Android and Chrome get
   * navigator.vibrate. iOS has no vibrate, but Safari 18 gives a tick when a
   * <input type="checkbox" switch> is toggled, and toggling one through its
   * label from inside a real tap counts. Hover-capable screens are left alone.
   *
   * The hidden label stops its own click from travelling: the menu closes on
   * any click outside the header, so a click bubbling from a label at the end
   * of <body> would shut the menu the moment the button opened it. */
  var hapIOS = null;
  PGA.haptic = function (ms) {
    try { if (navigator.vibrate) { navigator.vibrate(ms || 12); return; } } catch (e) {}
    try {
      if (!window.matchMedia || !matchMedia("(hover: none)").matches) return;
      if (!hapIOS) {
        hapIOS = d.createElement("label");
        hapIOS.setAttribute("aria-hidden", "true");
        hapIOS.style.cssText = "position:fixed;left:-9999px;top:0;width:1px;height:1px;" +
                               "overflow:hidden;opacity:0;pointer-events:none;";
        var inp = d.createElement("input");
        inp.type = "checkbox"; inp.setAttribute("switch", ""); inp.tabIndex = -1;
        hapIOS.appendChild(inp);
        hapIOS.addEventListener("click", function (e) { e.stopPropagation(); });
        d.body.appendChild(hapIOS);
      }
      hapIOS.click();
    } catch (e) {}
  };

  // The key actions: Book a Call, Enquire Now, and the menu. Capture phase,
  // because the menu button stops its own click from bubbling.
  var KEY = ".nav-toggle, .nav-cta, a[href*='calendar.app.google'], " +
            "a[href$='enquire.html'], a[href='#enquire']";
  d.addEventListener("click", function (e) {
    var t = e.target && e.target.closest ? e.target.closest(KEY) : null;
    if (t) PGA.haptic(10);
  }, true);

  /* PAGE TRANSITIONS. The cross-fade and the still header are pure CSS. Two
   * things need a script.
   *
   * THE THUMBNAIL. Every episode page names its player ep-<slug>. Following a
   * link to an episode gives the picture you clicked the same name, so the
   * browser morphs one into the other. Names go on at the last moment and on
   * one element only: two elements with one name cancel the whole transition,
   * and every named element is captured separately, which costs on a page with
   * ninety thumbnails. Skipped when the link has a #chapter, because the new
   * page opens scrolled and the player may not be on screen.
   *
   * THE HEADER. It is held still across the fade, which only looks right when
   * it is actually on screen at the top. Scrolled away, or under the episode
   * popup or the knowledge base door, it fades with the page instead.
   *
   * Listening on window, so every handler on document has run first and a
   * click the episode popup keeps for itself is already marked prevented. */
  var named = null;
  function unname() {
    if (!named) return;
    named.style.removeProperty("view-transition-name");
    named.style.removeProperty("view-transition-class");
    named = null;
  }
  function slugOf(u) {
    var m = /\/episodes\/([a-z0-9-]+)\.html$/.exec(u.pathname);
    return m ? m[1] : null;
  }
  function thumbFor(a) {
    var img = a.querySelector("img");
    if (!img) {
      var card = a.closest(".kb-card");
      if (card) img = card.querySelector(".kb-med img");
    }
    if (!img) return null;
    var r = img.getBoundingClientRect();
    if (r.width < 40 || r.bottom <= 0 || r.top >= innerHeight) return null;
    return img;
  }
  window.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a || (a.target && a.target !== "_self") || a.hasAttribute("download")) return;
    var u;
    try { u = new URL(a.href, location.href); } catch (err) { return; }
    if (u.origin !== location.origin || u.hash || u.pathname === location.pathname) return;
    var slug = slugOf(u), img = slug && thumbFor(a);
    if (!img) return;
    unname();
    img.style.setProperty("view-transition-name", "ep-" + slug);
    img.style.setProperty("view-transition-class", "ep-thumb");
    named = img;
  });

  /* THE NEXT PAGE IS READY BEFORE THE CLICK LANDS. A link that is hovered for
   * a moment, or pressed by a finger, has its page prepared in the background
   * (Chrome, Edge and Android; other browsers ignore the rules). The page
   * transition then has nothing to wait for, which is most of what made it
   * stutter: the fade could not start until the next page had loaded and run
   * its scripts. Same-site pages only, never a link that opens a new tab,
   * downloads, or only moves within the page. */
  try {
    if (HTMLScriptElement.supports && HTMLScriptElement.supports("speculationrules") &&
        !d.querySelector('script[type="speculationrules"]')) {
      var rules = d.createElement("script");
      rules.type = "speculationrules";
      // The knowledge base is only fetched ahead, not prepared: prepared, its
      // door would start its opening animation before anyone arrived.
      var skip = "[target=_blank], [download], [href^='#'], [href^='mailto:'], [href^='tel:']";
      rules.textContent = JSON.stringify({
        prerender: [{
          where: { and: [
            { href_matches: "/*" },
            { not: { href_matches: "/knowledge-base.html" } },
            { not: { selector_matches: skip } }
          ] },
          eagerness: "moderate"
        }],
        prefetch: [{
          where: { and: [
            { href_matches: "/knowledge-base.html" },
            { not: { selector_matches: skip } }
          ] },
          eagerness: "moderate"
        }]
      });
      d.head.appendChild(rules);
    }
  } catch (e) {}

  function header() { return d.querySelector(".page-wrap > nav"); }
  // Hit testing is already switched off when pageswap runs (every point answers
  // <html>), so whether the header is covered is read at the click that starts
  // the navigation. Without a recent click, the scroll position decides alone.
  var navHidden = null, readAt = 0;
  d.addEventListener("click", function () {
    var nav = header();
    if (!nav) return;
    var r = nav.getBoundingClientRect(), hit = null;
    if (r.bottom > 0) {
      var top = Math.max(r.top, 0);
      hit = d.elementFromPoint(r.left + r.width / 2, top + (r.bottom - top) / 2);
    }
    navHidden = !hit || !nav.contains(hit);
    readAt = Date.now();
  }, true);
  window.addEventListener("pageswap", function (e) {
    if (!e.viewTransition) return;
    var nav = header();
    if (nav) {
      nav.style.removeProperty("view-transition-name");
      var hidden = (Date.now() - readAt < 8000 && navHidden !== null)
        ? navHidden : nav.getBoundingClientRect().bottom <= 0;
      if (hidden) nav.style.setProperty("view-transition-name", "none");
    }
    // A name left on a thumbnail for somewhere else would give that thumbnail
    // a layer of its own for nothing.
    var to = e.activation && e.activation.entry && e.activation.entry.url;
    if (named && to) {
      var u = new URL(to);
      if (u.hash || named.style.getPropertyValue("view-transition-name") !== "ep-" + slugOf(u)) unname();
    }
  });
  // Coming back through the history cache the name is still on the thumbnail,
  // which is what lets the player fly back into it. Cleared once it has.
  window.addEventListener("pagereveal", function (e) {
    var nav = header();
    if (nav) nav.style.removeProperty("view-transition-name");
    if (e.viewTransition) e.viewTransition.finished.then(unname, unname);
    else unname();
  });
})();
