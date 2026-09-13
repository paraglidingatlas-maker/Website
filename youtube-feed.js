// YouTube "Glimpse of the Show" feed. Fetches real videos live from the
// channel's own RSS feed (no API key needed), same raw-XML + DOMParser
// technique that worked for the podcast RSS feed. Isolated in its own file
// on purpose, so editing the rest of the page can't accidentally corrupt it.
//
// WHAT THIS RENDERS NOW
// A drifting rail, the same device the homepage uses for episodes, rather than
// a featured card beside a scrolling playlist. Ten videos, not six.
//
// The track holds the list TWICE so the loop is seamless: the animation
// translates by exactly -50%, which lands the second copy where the first
// started. Twenty cards in the DOM but only ten unique thumbnail URLs, so the
// browser fetches ten and serves the duplicates from cache.
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
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7Z"/></svg>
          </span>
        </span>
        <span class="yt-title">${esc(v.title)}</span>
        <span class="yt-date">${esc(v.date)}</span>
      </a>`;
  }

  // ---------------------------------------------------------------- lightbox
  let box = null;
  let lastFocus = null;

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

  trackEl.addEventListener('click', function (e) {
    const a = e.target.closest('.yt-card');
    if (!a) return;
    // leave modified clicks alone so "open in new tab" still works
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    const id = a.dataset.yt;
    if (!id) return;
    e.preventDefault();
    openBox(id, a.dataset.title);
  });

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
        const id = entry.getElementsByTagNameNS('*', 'videoId')[0]?.textContent || '';
        const published = entry.getElementsByTagNameNS('*', 'published')[0]?.textContent || '';
        const date = published
          ? new Date(published).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
          : '';
        return { title: title, link: link, thumb: thumb, id: id, date: date };
      });

      // twice, so translateX(-50%) loops with no seam
      trackEl.innerHTML = videos.map(card).join('') + videos.map(card).join('');
      if (statusEl) statusEl.textContent = `Live from YouTube. Showing the ${videos.length} most recent videos.`;
    })
    .catch(function (err) {
      if (statusEl) statusEl.textContent = 'Could not reach the YouTube feed right now.';
      console.warn('YouTube feed error:', err);
    });
})();
