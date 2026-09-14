// YouTube "Glimpse of the Show" feed. Fetches real videos live from the
// channel's own RSS feed (no API key needed), same raw-XML + DOMParser
// technique that worked for the podcast RSS feed. Isolated in its own file
// on purpose, so editing the rest of the page can't accidentally corrupt it.
//
// WHAT THIS RENDERS NOW
// A drifting rail, the same device the homepage uses for episodes, rather than
// a featured card beside a scrolling playlist. Ten videos, not six.
//
// MOTION IS NOT A CSS ANIMATION, for the reason homepage-motion.js states at the
// top of its own marquee: a CSS animation owns the transform, so a drag fights
// it. I shipped this as `animation: ytDrift 80s linear infinite` and made
// exactly the mistake that file exists to record. One rAF loop now drives the
// drift AND the drag, so they cannot disagree.
//
// The cards are cloned HERE, after render, rather than emitted twice by the
// template. The loop wraps at half the track width, which needs two identical
// halves, but the second half is decoration: aria-hidden and untabbable, so a
// screen reader and the keyboard meet ten videos rather than twenty. Emitting
// them twice in the markup, which is what I did first, gave assistive tech
// twenty links to ten videos.
//
// Thumbnails run at full colour. They were held back in an earlier design where
// six sat stacked in a static column all competing at once; on a rail they are
// in motion behind an edge mask and read as a filmstrip, so that worry does not
// carry over.
//
// CLICKING PLAYS IN PLACE
// Each card is a real <a href> to YouTube, so a crawler finds a route onward and
// cmd, ctrl or middle click still opens a tab. A plain click is intercepted and
// opens a lightbox instead. The iframe is built AT THAT MOMENT, never on page
// load, so YouTube is not contacted at all until somebody chooses to watch, and
// it points at youtube-nocookie. tools/audit.py FAILS on a non-nocookie embed,
// which is the right severity for it.
(function () {
  const trackEl = document.getElementById('ytTrack');
  const statusEl = document.getElementById('ytStatus');
  if (!trackEl) return;

  const channelId = 'UC0xDTfl8kurPl9CgpsLTr2Q';
  const feedUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`;
  const proxyUrl = `https://restless-king-e534.aninder.workers.dev/?url=${encodeURIComponent(feedUrl)}`;
  const COUNT = 10;

  // THE VIDEO ID, from three sources rather than one.
  //
  // This was `getElementsByTagNameNS('*','videoId')` alone. If that returns
  // nothing the id is an empty string, the card gets data-yt="", and the click
  // handler hits `if (!id) return;` and bails without a sound. Every click,
  // every card, no error in the console. The version before this rewrite never
  // read videoId at all, so the dependency is entirely mine.
  //
  // Three sources, in order of how much I trust them:
  //   yt:videoId          the proper field
  //   <id>yt:video:XXX    the Atom id, same value with a prefix
  //   the watch link      ?v=XXX
  // If all three fail the card keeps its href and the browser opens YouTube,
  // which is a worse outcome than the lightbox but not a dead click.
  // TEMPORARY: which route each id came from, reported in the status line.
  // I have shipped two candidate fixes for a dead click without being able to
  // see a browser, and guessing again is worse than measuring once. Remove
  // idRoutes and the suffix on the status line as soon as the cause is known.
  const idRoutes = { videoId: 0, atom: 0, link: 0, none: 0 };

  function videoIdOf(entry, link) {
    const direct = entry.getElementsByTagNameNS('*', 'videoId')[0]?.textContent;
    if (direct && direct.trim()) { idRoutes.videoId++; return direct.trim(); }

    const atom = entry.getElementsByTagNameNS('*', 'id')[0]?.textContent || '';
    const m = atom.match(/yt:video:([\w-]+)/);
    if (m) { idRoutes.atom++; return m[1]; }

    const q = String(link).match(/[?&]v=([\w-]+)/);
    if (q) { idRoutes.link++; return q[1]; }

    idRoutes.none++;
    return '';
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[c]);
  }

  function card(v) {
    return `
      <a class="yt-card" href="${esc(v.link)}" target="_blank" rel="noopener"
         data-yt="${esc(v.id)}" data-title="${esc(v.title)}">
        <span class="yt-shot">
          <img src="${esc(v.thumb)}" alt="" loading="lazy">
          <span class="yt-play" aria-hidden="true">
            <!-- YouTube's own triangle geometry, not the generic one used
                 elsewhere on the site. In a 68 by 48 box the triangle runs
                 x 27-45, y 14-34: 26% of the width and 42% of the height. The
                 generic M8 5v14l11-7Z in a 24 box works out at 15% and 27%,
                 which is why it read as a small arrow rather than a play
                 button. The apex sits at 45 of 68 rather than dead centre,
                 which is how YouTube optically centres a triangle. -->
            <svg viewBox="0 0 68 48" fill="currentColor" aria-hidden="true">
              <path d="M45 24 27 14 27 34Z"/>
            </svg>
          </span>
        </span>
        <span class="yt-title">${esc(v.title)}</span>
        <span class="yt-date">${esc(v.date)}</span>
      </a>`;
  }

  // ---------------------------------------------------------------- lightbox
  let box = null;
  let lastFocus = null;
  let draggedAt = 0;        // shared with the rail's click swallower
  // WHICH CARD WAS PRESSED, recorded at pointerdown.
  // The click handler used to find the card with e.target.closest('.yt-card'),
  // and that stopped working the moment the rail got pointer capture:
  // setPointerCapture retargets the compatibility mouse events, click included,
  // to the capturing element, so e.target became the rail and closest() found
  // nothing. The handler returned early and the lightbox never opened.
  // homepage-motion.js has the same capture and never showed the fault, because
  // its cards are plain links that navigate by default and it never reads
  // e.target. Recording the card on pointerdown is immune to the retarget.
  let pressedCard = null;

  function closeBox() {
    if (!box) return;
    box.classList.remove('on');
    box.innerHTML = '';                    // tears the iframe down, stops playback
    document.body.style.overflow = '';
    if (lastFocus) { lastFocus.focus(); lastFocus = null; }
  }

  function openBox(id, title) {
    if (!box) {
      box = document.createElement('div');
      box.className = 'yt-lb';
      box.setAttribute('role', 'dialog');
      box.setAttribute('aria-modal', 'true');
      box.addEventListener('click', function (e) { if (e.target === box) closeBox(); });
      document.body.appendChild(box);
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeBox();
      });
    }
    lastFocus = document.activeElement;
    box.setAttribute('aria-label', title || 'Video');
    box.innerHTML = `
      <div class="yt-lb-inner">
        <button class="yt-lb-close" type="button" aria-label="Close video">Close</button>
        <iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}?autoplay=1"
                title="${esc(title || 'Video')}" allowfullscreen
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture"></iframe>
      </div>`;
    box.querySelector('.yt-lb-close').addEventListener('click', closeBox);
    box.classList.add('on');
    document.body.style.overflow = 'hidden';
    box.querySelector('.yt-lb-close').focus();
  }

  // BOUND DIRECTLY TO EACH CARD, not only delegated.
  //
  // Three of my theories about the dead click all live in the gap between the
  // card and the listener: delegation reading e.target, pointer capture
  // retargeting that e.target, and the drag's capture-phase swallower calling
  // stopPropagation on the way down. Binding the same handler to every card
  // removes all three from the path at once. The delegated one stays as a
  // backstop for anything the direct binding misses.
  function openFromCard(a, e) {
    if (!a) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    if (Date.now() - draggedAt < 350) return;   // a swipe must not open a video
    const id = a.dataset.yt;
    if (!id) return;
    e.preventDefault();
    openBox(id, a.dataset.title);
  }

  function bindCards() {
    trackEl.querySelectorAll('.yt-card').forEach(function (a) {
      if (a.dataset.bound) return;
      a.dataset.bound = '1';
      a.addEventListener('click', function (e) { openFromCard(a, e); });
    });
  }

  trackEl.addEventListener('click', function (e) {
    const a = (e.target.closest && e.target.closest('.yt-card')) || pressedCard;
    // Was `if (a.dataset.bound) return`, which is what made the clones
    // unreachable from here too. defaultPrevented asks the real question: has
    // something already handled this click?
    if (!a || e.defaultPrevented) return;
    // leave modified clicks alone so "open in new tab" still works
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    if (Date.now() - draggedAt < 350) return;   // a swipe must not open a video
    const id = a.dataset.yt;
    if (!id) return;
    e.preventDefault();
    openBox(id, a.dataset.title);
  });

  // ---------------------------------------------------------------- motion
  // Ported from homepage-motion.js rather than written again. Every awkward
  // detail below was found and fixed there once already: the native link drag,
  // the synthetic click after a touch swipe, the track width changing as images
  // decode. Reusing it also makes the two rails behave identically, which was
  // half the argument for choosing a rail here.
  const railEl = trackEl.parentElement;
  const reduce = window.matchMedia &&
                 window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function startRail() {
    if (reduce) return;                    // CSS leaves it a plain scroller
    if (!trackEl.children.length) return;

    Array.prototype.slice.call(trackEl.children).forEach(function (el) {
      const c = el.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      c.setAttribute('tabindex', '-1');
      // cloneNode copies attributes but NOT listeners, so the clone arrived
      // carrying data-bound="1" with nothing attached to it. bindCards then
      // skipped it as already done and the delegated backstop refused it for
      // the same reason, leaving every clone completely dead. The rail drifts,
      // so half the cards on screen at any moment were the dead ones.
      c.removeAttribute('data-bound');
      trackEl.appendChild(c);
    });
    bindCards();                          // the clones need it too

    let x = 0, half = 0;
    const speed = 0.35;
    let paused = false, dragging = false;
    let startX = 0, startPos = 0, moved = 0, resumeTimer = null;

    function measure() { half = trackEl.scrollWidth / 2; }
    function wrap() {
      if (half <= 0) return;
      while (x <= -half) x += half;
      while (x > 0) x -= half;
    }
    function paint() { trackEl.style.transform = 'translate3d(' + x + 'px,0,0)'; }
    function tick() {
      if (!paused && !dragging) { x -= speed; wrap(); paint(); }
      requestAnimationFrame(tick);
    }

    measure();
    window.addEventListener('resize', measure);
    // the width changes as thumbnails decode, and a wrong `half` makes the loop
    // jump, so watch the element rather than measuring once at load
    window.addEventListener('load', measure);
    if ('ResizeObserver' in window) new ResizeObserver(measure).observe(trackEl);
    requestAnimationFrame(tick);

    // Pointing at the strip stops it so a card can be read. This replaces a CSS
    // :hover plus :focus-within rule, and :focus-within was the bug: clicking a
    // card focused it, so the rail stayed stopped until you clicked away.
    railEl.addEventListener('mouseenter', function () { paused = true; });
    railEl.addEventListener('mouseleave', function () { if (!dragging) paused = false; });

    // the cards are links and browsers natively drag links
    railEl.addEventListener('dragstart', function (e) { e.preventDefault(); });

    railEl.addEventListener('pointerdown', function (e) {
      if (e.button !== undefined && e.button !== 0) return;
      pressedCard = e.target.closest ? e.target.closest('.yt-card') : null;
      dragging = true; moved = 0; startX = e.clientX; startPos = x;
      railEl.classList.add('is-dragging');
      try { railEl.setPointerCapture(e.pointerId); } catch (err) {}
      if (resumeTimer) { clearTimeout(resumeTimer); resumeTimer = null; }
    });

    railEl.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      const dx = e.clientX - startX;
      if (Math.abs(dx) > moved) moved = Math.abs(dx);
      x = startPos + dx; wrap(); paint();
    });

    // A drag must not open the card under your finger. A timestamp, not a
    // setTimeout: on touch the synthetic click arrives after a 0ms timeout, so
    // a swallower removed that way misses and a swipe opens a video.
    railEl.addEventListener('click', function (ev) {
      if (Date.now() - draggedAt < 350) { ev.preventDefault(); ev.stopPropagation(); }
    }, true);

    function release(e) {
      if (!dragging) return;
      dragging = false;
      railEl.classList.remove('is-dragging');
      try { railEl.releasePointerCapture(e.pointerId); } catch (err) {}
      if (moved > 6) draggedAt = Date.now();
      resumeTimer = setTimeout(function () { paused = false; }, 900);
    }
    railEl.addEventListener('pointerup', release);
    railEl.addEventListener('pointercancel', release);
  }

  // ---------------------------------------------------------------- fetch
  fetch(proxyUrl)
    .then(function (res) {
      if (!res.ok) throw new Error('YouTube feed request failed');
      return res.text();
    })
    .then(function (xmlText) {
      const xml = new DOMParser().parseFromString(xmlText, 'application/xml');
      if (xml.querySelector('parsererror')) throw new Error('YouTube feed XML failed to parse');

      const entries = Array.from(xml.getElementsByTagNameNS('*', 'entry'));
      if (!entries.length) throw new Error('YouTube feed returned no videos');

      const videos = entries.slice(0, COUNT).map(function (entry) {
        const title = entry.getElementsByTagNameNS('*', 'title')[0]?.textContent || 'Untitled';
        const link = entry.getElementsByTagNameNS('*', 'link')[0]?.getAttribute('href') || '#';
        const thumb = entry.getElementsByTagNameNS('*', 'thumbnail')[0]?.getAttribute('url') || '';
        const id = videoIdOf(entry, link);
        const published = entry.getElementsByTagNameNS('*', 'published')[0]?.textContent || '';
        const date = published
          ? new Date(published).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
          : '';
        return { title: title, link: link, thumb: thumb, id: id, date: date };
      });

      trackEl.innerHTML = videos.map(card).join('');
      bindCards();
      startRail();
      if (statusEl) {
        // TEMPORARY diagnostic suffix, remove once the click is understood
        const r = idRoutes;
        const bound = trackEl.querySelectorAll('.yt-card[data-bound]').length;
        const cards = trackEl.querySelectorAll('.yt-card').length;
        const via = `ids ${r.videoId}/${r.atom}/${r.link}/${r.none} · bound ${bound}/${cards}`;
        statusEl.textContent =
          `Live from YouTube. Showing the ${videos.length} most recent videos. [${via}]`;
      }
    })
    .catch(function (err) {
      if (statusEl) statusEl.textContent = 'Could not reach the YouTube feed right now.';
      console.warn('YouTube feed error:', err);
    });
})();
