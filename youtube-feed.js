// YouTube "Glimpse of the Show" feed — fetches real videos live from the
// channel's own RSS feed (no API key needed), same raw-XML + DOMParser
// technique that worked for the podcast RSS feed. Isolated in its own file
// on purpose, so editing the rest of the page can't accidentally corrupt it.
(function () {
  const featuredEl = document.getElementById('ytFeatured');
  const playlistEl = document.getElementById('ytPlaylist');
  const statusEl = document.getElementById('ytStatus');
  if (!featuredEl || !playlistEl) return;

  const channelId = 'UC0xDTfl8kurPl9CgpsLTr2Q';
  const feedUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`;
  const proxyUrl = `https://corsproxy.io/?url=${encodeURIComponent(feedUrl)}`;

  function renderFeatured(video) {
    featuredEl.innerHTML = `
      <div class="featB-media">
        <img id="featBImg" class="thumb" src="${video.thumb}" alt="">
        <span class="featB-tag">Featured</span>
        <div class="featB-play"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7Z"/></svg></div>
      </div>
      <div class="featB-info">
        <p class="featB-title">${video.title}</p>
        <p class="featB-guest">Paragliding Atlas</p>
      </div>`;
    featuredEl.onclick = () => window.open(video.link, '_blank', 'noopener');
    syncPlaylistHeight();
    const img = featuredEl.querySelector('img');
    if (img) img.addEventListener('load', syncPlaylistHeight);
  }

  function syncPlaylistHeight() {
    // Match the playlist's max-height to the featured card's actual rendered
    // height, so the two columns always end at the same line regardless of
    // title length or viewport width.
    requestAnimationFrame(() => {
      const h = featuredEl.offsetHeight;
      if (h > 0) playlistEl.style.maxHeight = h + 'px';
    });
  }
  window.addEventListener('resize', syncPlaylistHeight);

  function renderPlaylist(videos, activeIndex) {
    playlistEl.innerHTML = videos.map((v, i) => `
      <div class="playlistB-item${i === activeIndex ? ' active' : ''}" data-index="${i}">
        <div class="playlistB-thumb"><img class="thumb" src="${v.thumb}" alt=""></div>
        <div class="playlistB-mid">
          <div class="playlistB-title">${v.title}</div>
          <div class="playlistB-guest">${v.date}</div>
        </div>
      </div>`).join('');

    playlistEl.querySelectorAll('.playlistB-item').forEach((item) => {
      item.addEventListener('click', () => {
        const idx = parseInt(item.dataset.index, 10);
        renderFeatured(videos[idx]);
        renderPlaylist(videos, idx);
      });
    });
  }

  fetch(proxyUrl)
    .then((res) => {
      if (!res.ok) throw new Error('YouTube feed request failed');
      return res.text();
    })
    .then((xmlText) => {
      const xml = new DOMParser().parseFromString(xmlText, 'application/xml');
      if (xml.querySelector('parsererror')) throw new Error('YouTube feed XML failed to parse');

      const entries = Array.from(xml.getElementsByTagNameNS('*', 'entry'));
      if (!entries.length) throw new Error('YouTube feed returned no videos');

      const videos = entries.slice(0, 6).map((entry) => {
        const title = entry.getElementsByTagNameNS('*', 'title')[0]?.textContent || 'Untitled';
        const link = entry.getElementsByTagNameNS('*', 'link')[0]?.getAttribute('href') || '#';
        const thumb = entry.getElementsByTagNameNS('*', 'thumbnail')[0]?.getAttribute('url') || '';
        const published = entry.getElementsByTagNameNS('*', 'published')[0]?.textContent || '';
        const date = published
          ? new Date(published).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
          : '';
        return { title, link, thumb, date };
      });

      renderFeatured(videos[0]);
      renderPlaylist(videos, 0);
      if (statusEl) statusEl.textContent = `Live from YouTube — showing ${videos.length} most recent videos.`;
    })
    .catch((err) => {
      if (statusEl) statusEl.textContent = 'Could not reach the YouTube feed right now.';
      console.warn('YouTube feed error:', err);
    });
})();
