// Shared episode popup modal for Knowledge Base sub-series pages.
// Any element with class "ep-tile" and data-title/data-guest/data-desc/
// data-readmore/data-yt attributes will open this modal on click instead of
// navigating away directly. Clicking the play button inside the modal embeds
// the actual YouTube video (if a real video ID is known via data-yt-id) or
// opens a YouTube search for the title on the channel as an honest fallback.
(function () {
  const overlay = document.createElement('div');
  overlay.className = 'ep-modal-overlay';
  overlay.id = 'epModalOverlay';
  overlay.innerHTML = `
    <div class="ep-modal">
      <button class="ep-modal-close" id="epModalClose">&times;</button>
      <div class="ep-modal-media">
        <img class="ep-modal-thumb" id="epModalThumb" src="" alt="">
        <button class="ep-modal-play" id="epModalPlay">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7Z"/></svg>
        </button>
        <iframe class="ep-modal-iframe" id="epModalIframe" allow="autoplay; encrypted-media" allowfullscreen></iframe>
      </div>
      <div class="ep-modal-info">
        <h3 id="epModalTitle"></h3>
        <p class="ep-modal-guest" id="epModalGuest"></p>
        <p class="ep-modal-desc" id="epModalDesc"></p>
        <a class="ep-modal-readmore" id="epModalReadMore" target="_blank" rel="noopener">Read More →</a>
      </div>
    </div>`;
  document.body.appendChild(overlay);

  const thumb = document.getElementById('epModalThumb');
  const playBtn = document.getElementById('epModalPlay');
  const iframe = document.getElementById('epModalIframe');
  const titleEl = document.getElementById('epModalTitle');
  const guestEl = document.getElementById('epModalGuest');
  const descEl = document.getElementById('epModalDesc');
  const readMoreEl = document.getElementById('epModalReadMore');
  const closeBtn = document.getElementById('epModalClose');

  function closeModal() {
    overlay.classList.remove('active');
    iframe.src = '';
    iframe.style.display = 'none';
    thumb.style.display = 'block';
    playBtn.style.display = 'flex';
  }

  function openModal(tile) {
    const title = tile.dataset.title || '';
    const guest = tile.dataset.guest || '';
    const desc = tile.dataset.desc || 'Full episode details and show notes coming soon.';
    const ytId = tile.dataset.ytId || '';
    const spotify = tile.dataset.spotify || '';
    const readMore = tile.dataset.readmore || '../podcast.html';
    const thumbSrc = ytId
      ? `https://img.youtube.com/vi/${ytId}/hqdefault.jpg`
      : tile.dataset.thumb || '';

    titleEl.textContent = title;
    guestEl.textContent = guest;
    descEl.textContent = desc;
    readMoreEl.href = readMore;
    thumb.src = thumbSrc;
    thumb.style.display = 'block';
    playBtn.style.display = 'flex';
    iframe.style.display = 'none';
    iframe.src = '';

    playBtn.onclick = () => {
      if (ytId) {
        iframe.src = `https://www.youtube.com/embed/${ytId}?autoplay=1`;
        iframe.style.display = 'block';
        thumb.style.display = 'none';
        playBtn.style.display = 'none';
      } else if (spotify) {
        // No YouTube video confirmed, but a real Spotify link is — send there
        // instead of guessing at a YouTube search.
        window.open(spotify, '_blank', 'noopener');
      } else {
        // Honest last-resort fallback instead of a broken embed
        window.open(`https://www.youtube.com/@ParaglidingAtlas/search?query=${encodeURIComponent(title)}`, '_blank', 'noopener');
      }
    };

    overlay.classList.add('active');
  }

  document.querySelectorAll('.ep-tile').forEach((tile) => {
    tile.addEventListener('click', (e) => {
      e.preventDefault();
      openModal(tile);
    });
  });

  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
})();
