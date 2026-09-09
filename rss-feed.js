  // ============================================================
  // ⚠️ CONFIRMED WORKING — DO NOT MODIFY WITHOUT EXPLICIT REQUEST
  // This is the live RSS integration. It took several failed attempts
  // (rss2json's free tier silently capped at 10 items regardless of what
  // was requested) before landing on this approach: fetch the RAW feed XML
  // through a CORS proxy, then parse it natively with the browser's own
  // DOMParser — no third-party item-count cap. User confirmed this actually
  // works correctly for the first time. Leave this block untouched in future
  // edits unless the user specifically asks to change the RSS logic itself.
  // ============================================================
  (function () {
    const statusEl = document.getElementById('liveFeedStatus');
    const gridEl = document.getElementById('liveFeedGrid');
    const rssUrl = 'https://anchor.fm/s/ed1344d8/podcast/rss';
    const proxyUrl = `https://corsproxy.io/?url=${encodeURIComponent(rssUrl)}`;

    const audio = new Audio();
    let activeRow = null;

    function formatTime(sec) {
      if (!isFinite(sec) || sec < 0) return '0:00';
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60).toString().padStart(2, '0');
      return `${m}:${s}`;
    }

    function formatDate(dateStr) {
      const d = new Date(dateStr);
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }

    function formatDuration(sec) {
      if (!sec) return '';
      const h = Math.floor(sec / 3600);
      const m = Math.floor((sec % 3600) / 60);
      if (h > 0) return `${h}h ${m}min`;
      return `${m} min`;
    }

    const seeMoreBtn = document.getElementById('seeMoreBtn');
    const liveCounter = document.getElementById('liveCounter');
    const liveFeedFooter = document.getElementById('liveFeedFooter');
    const BATCH_SIZE = 15;
    let allItems = [];
    let renderedCount = 0;

    function buildRowHtml(item, i) {
      const title = (item.querySelector('title')?.textContent || '').replace(/</g, '&lt;');
      const link = item.querySelector('link')?.textContent || '';
      const pubDate = item.querySelector('pubDate')?.textContent || '';
      const enclosure = item.querySelector('enclosure');
      const audioUrl = enclosure ? enclosure.getAttribute('url') : '';
      const itunesImage = item.getElementsByTagNameNS('*', 'image')[0];
      const cover = itunesImage ? itunesImage.getAttribute('href') : 'assets/logo/favicon.png';
      const durationEl = item.getElementsByTagNameNS('*', 'duration')[0];
      const durationSec = durationEl ? parseDuration(durationEl.textContent) : 0;

      return `
        <div class="ep-row" data-index="${i}" data-audio="${audioUrl}" data-duration="${durationSec}">
          <div class="ep-row-main">
            <img class="ep-cover" src="${cover}" alt="">
            <button class="ep-play-btn" aria-label="Play episode">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7Z"/></svg>
            </button>
            <div class="ep-row-mid">
              <div class="ep-row-title">${title}</div>
              <div class="ep-row-show">Paragliding Atlas Podcast</div>
            </div>
            <div class="ep-row-meta">
              <span>${formatDate(pubDate)}</span>
              <span>${formatDuration(durationSec)}</span>
            </div>
            <div class="ep-row-icons">
              <a class="ep-icon-btn" href="${audioUrl}" download title="Download">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 4v12M6 12l6 6 6-6M5 20h14"/></svg>
              </a>
              <a class="ep-icon-btn" href="${link}" target="_blank" rel="noopener" title="Open on Spotify">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 17L17 7M17 7H8M17 7v9"/></svg>
              </a>
            </div>
          </div>
          <div class="ep-player">
            <div class="ep-progress-row">
              <span class="ep-time start">0:00</span>
              <div class="ep-progress-track"><div class="ep-progress-fill"></div></div>
              <span class="ep-time end">${formatTime(durationSec)}</span>
            </div>
            <div class="ep-skip-controls">
              <button class="ep-skip-btn" data-skip="-15">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 12a9 9 0 1 0 3-6.7M3 4v5h5"/></svg>
                15
              </button>
              <button class="ep-play-btn-lg">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7Z"/></svg>
              </button>
              <button class="ep-skip-btn" data-skip="15">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 12a9 9 0 1 1-3-6.7M21 4v5h-5"/></svg>
                15
              </button>
            </div>
          </div>
        </div>`;
    }

    function parseDuration(str) {
      // itunes:duration can be "SS", "MM:SS", or "HH:MM:SS"
      if (!str) return 0;
      const parts = str.split(':').map(Number);
      if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
      if (parts.length === 2) return parts[0] * 60 + parts[1];
      return parts[0] || 0;
    }

    function renderNextBatch() {
      const nextItems = allItems.slice(renderedCount, renderedCount + BATCH_SIZE);
      const html = nextItems.map((item, idx) => buildRowHtml(item, renderedCount + idx)).join('');
      gridEl.insertAdjacentHTML('beforeend', html);

      // Wire up only the newly-added rows, leaving already-playing rows untouched
      const newRows = Array.from(gridEl.querySelectorAll('.ep-row')).slice(renderedCount);
      wireUpPlayers(newRows);

      renderedCount += nextItems.length;
      liveCounter.textContent = `Showing ${renderedCount} of ${allItems.length}`;
      seeMoreBtn.disabled = renderedCount >= allItems.length;
      seeMoreBtn.textContent = renderedCount >= allItems.length ? 'All episodes loaded' : `See ${Math.min(BATCH_SIZE, allItems.length - renderedCount)} More →`;
    }

    seeMoreBtn.addEventListener('click', renderNextBatch);

    fetch(proxyUrl)
      .then((res) => {
        if (!res.ok) throw new Error('Feed request failed');
        return res.text();
      })
      .then((xmlText) => {
        const xml = new DOMParser().parseFromString(xmlText, 'application/xml');
        if (xml.querySelector('parsererror')) throw new Error('Feed XML failed to parse');
        allItems = Array.from(xml.querySelectorAll('item'));
        if (!allItems.length) throw new Error('Feed returned no items');

        renderNextBatch();
        liveFeedFooter.style.display = 'flex';
        statusEl.textContent = `Pulled live from your RSS feed just now — ${allItems.length} episodes available via the feed.`;
      })
      .catch((err) => {
        statusEl.textContent = 'Could not reach the live feed right now — showing the saved archive below instead.';
        gridEl.innerHTML = '';
        console.warn('RSS live feed error:', err);
      });

    function setRowIcon(row, playing) {
      const icon = playing
        ? '<path d="M7 5h4v14H7zM13 5h4v14h-4z"/>'
        : '<path d="M8 5v14l11-7Z"/>';
      row.querySelectorAll('.ep-play-btn svg, .ep-play-btn-lg svg').forEach((svg) => {
        svg.innerHTML = icon;
      });
    }

    function playRow(row) {
      const url = row.dataset.audio;
      if (!url) return;

      if (activeRow && activeRow !== row) {
        activeRow.classList.remove('playing');
        setRowIcon(activeRow, false);
      }

      if (activeRow === row && !audio.paused) {
        audio.pause();
        row.classList.remove('playing');
        setRowIcon(row, false);
        return;
      }

      if (activeRow === row && audio.paused) {
        audio.play();
        row.classList.add('playing');
        setRowIcon(row, true);
        return;
      }

      audio.src = url;
      audio.play();
      activeRow = row;
      row.classList.add('playing');
      setRowIcon(row, true);
    }

    function wireUpPlayers(rows) {
      rows.forEach((row) => {
        row.querySelector('.ep-play-btn').addEventListener('click', () => playRow(row));
        row.querySelector('.ep-play-btn-lg').addEventListener('click', () => playRow(row));

        row.querySelectorAll('.ep-skip-btn').forEach((btn) => {
          btn.addEventListener('click', () => {
            if (activeRow !== row) return;
            audio.currentTime = Math.max(0, Math.min(audio.duration || Infinity, audio.currentTime + parseInt(btn.dataset.skip, 10)));
          });
        });

        const track = row.querySelector('.ep-progress-track');
        track.addEventListener('click', (e) => {
          if (activeRow !== row || !audio.duration) return;
          const rect = track.getBoundingClientRect();
          const pct = (e.clientX - rect.left) / rect.width;
          audio.currentTime = pct * audio.duration;
        });
      });
    }

    // Registered once — updates whichever row is currently active, regardless
    // of how many "See More" batches have been loaded since.
    audio.addEventListener('timeupdate', () => {
      if (!activeRow) return;
      const fill = activeRow.querySelector('.ep-progress-fill');
      const startTime = activeRow.querySelector('.ep-time.start');
      const endTime = activeRow.querySelector('.ep-time.end');
      const pct = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
      fill.style.width = pct + '%';
      startTime.textContent = formatTime(audio.currentTime);
      if (audio.duration) endTime.textContent = formatTime(audio.duration);
    });

    audio.addEventListener('ended', () => {
      if (activeRow) {
        activeRow.classList.remove('playing');
        setRowIcon(activeRow, false);
      }
    });
  })();
