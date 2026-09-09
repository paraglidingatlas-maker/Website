// Homepage episode search — filters the real episode list (EPISODE_SEARCH_DATA,
// loaded from episode-search-data.js) by title, and links each result straight
// to the real YouTube video. Isolated in its own file per the site's
// established pattern of keeping features separate.
(function () {
  const input = document.getElementById('epSearchInput');
  const btn = document.getElementById('epSearchBtn');
  const resultsBox = document.getElementById('epSearchResults');
  if (!input || !btn || !resultsBox || typeof EPISODE_SEARCH_DATA === 'undefined') return;

  function runSearch() {
    const query = input.value.trim().toLowerCase();
    if (!query) {
      resultsBox.classList.remove('active');
      resultsBox.innerHTML = '';
      return;
    }

    const matches = EPISODE_SEARCH_DATA.filter((ep) =>
      ep.title.toLowerCase().includes(query)
    ).slice(0, 8); // cap results so the dropdown stays manageable

    if (matches.length === 0) {
      resultsBox.innerHTML = '<div class="ep-search-empty">No episodes found matching that search.</div>';
    } else {
      resultsBox.innerHTML = matches
        .map(
          (ep) =>
            `<a class="ep-search-result" href="https://www.youtube.com/watch?v=${ep.video_id}" target="_blank" rel="noopener">${ep.title}</a>`
        )
        .join('');
    }
    resultsBox.classList.add('active');
  }

  input.addEventListener('input', runSearch);
  btn.addEventListener('click', runSearch);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') runSearch();
  });

  // Close results when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.ep-search-section')) {
      resultsBox.classList.remove('active');
    }
  });
})();
