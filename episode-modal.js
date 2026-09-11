/**
 * Episode popup for the Knowledge Base series pages.
 *
 * TWO MODES, on purpose.
 *
 * RICH. A page that ships a <script type="application/json" id="kbEpisodes">
 * block gets the full card: pull quote, chapters linking into the transcript,
 * topic chips linking to their topic pages, a spec sheet, a share button and a
 * coordinate stamp from the episode's own globe pin.
 *
 * PLAIN. A page without that block falls back to the old title / guest /
 * description card. Every knowledge base page except the one being piloted is
 * still in this mode, so nothing regresses while the rich version is reviewed.
 *
 * WHAT THE TILES ARE NOW
 * Tiles used to be <div>, so a crawler reading storytellers.html found no route
 * onward at all: 17 pages passing zero links to 93 episode pages. They are now
 * <a href> to the episode page. The click is intercepted for people and left
 * alone for machines, and a modified click (ctrl, cmd, middle, shift) is not
 * swallowed, so "open in new tab" still works.
 *
 * DISMISSAL: back button, Escape, click outside. There is no close cross, by
 * the user's decision. Back is the one that matters on a phone, where it is
 * reachable with a thumb and a 24px strip of backdrop is not, so opening pushes
 * a history entry and closing pops it.
 */
(function () {
  'use strict';

  var tiles = document.querySelectorAll('.ep-tile');
  if (!tiles.length) return;

  var DATA = null;
  var holder = document.getElementById('kbEpisodes');
  if (holder) {
    try { DATA = JSON.parse(holder.textContent); } catch (e) { DATA = null; }
  }

  var overlay = document.createElement('div');
  overlay.className = 'ep-modal-overlay';
  overlay.id = 'epModalOverlay';
  document.body.appendChild(overlay);

  var lastFocus = null;
  var pushed = false;

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function shortTime(at) {
    var s = String(at || '');
    return s.indexOf('00:') === 0 ? s.slice(3) : s;
  }

  function coordText(d) {
    if (d.lat == null || d.lon == null) return esc(d.series || '');
    var ns = d.lat >= 0 ? 'N' : 'S', ew = d.lon >= 0 ? 'E' : 'W';
    return Math.abs(d.lat).toFixed(4) + '\u00B0' + ns + ' / ' +
           Math.abs(d.lon).toFixed(4) + '\u00B0' + ew;
  }

  var PLAY_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7Z"/></svg>';
  var SHARE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M4 12v7a1 1 0 001 1h14a1 1 0 001-1v-7"/><path d="M12 3v13"/>' +
    '<path d="M8 7l4-4 4 4"/></svg>';

  function mediaHTML(d) {
    if (d.video) {
      /* maxresdefault is a true 16:9 frame. hqdefault, which this file used to
         request, is 480x360: a 4:3 frame with black bars baked in, so cropping
         it to 16:9 cut real picture out of the middle. mqdefault is the
         fallback and is also true 16:9, so nothing is ever cropped. */
      return '<button class="kb-med" type="button" aria-label="Play episode">' +
        '<img src="https://i.ytimg.com/vi/' + esc(d.video) + '/maxresdefault.jpg" alt="" ' +
        'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/' + esc(d.video) +
        '/mqdefault.jpg\'">' +
        '<span class="kb-play">' + PLAY_SVG + '</span></button>';
    }
    /* Audio only. No video exists, so no play button is offered: a control that
       cannot do what it promises is worse than no control. */
    var art = d.artwork || '../assets/images/artwork-needed.png';
    return '<div class="kb-med kb-med-audio"><img src="' + esc(art) + '" alt="">' +
           '<p class="kb-audio-note">Audio episode. This one was never filmed.</p></div>';
  }

  function chaptersHTML(d) {
    if (!d.chapters || !d.chapters.length) return '';
    var items = d.chapters.map(function (c) {
      var inner = '<span class="kb-at">' + esc(shortTime(c.at)) + '</span>' +
                  '<span class="kb-ct">' + esc(c.title) + '</span>';
      /* No anchor means that chapter is not on the episode page, because it had
         no transcript under it. Rendered as text rather than as a link that
         would land in the wrong place. */
      return c.anchor
        ? '<li><a class="kb-chl" href="' + esc(d.page) + '#' + esc(c.anchor) + '">' + inner + '</a></li>'
        : '<li><span class="kb-chl kb-chl-plain">' + inner + '</span></li>';
    }).join('');
    return '<p class="kb-lbl">// Inside</p><ul class="kb-ch">' + items + '</ul>';
  }

  function tagsHTML(d) {
    if (!d.tags || !d.tags.length) return '';
    var chips = d.tags.map(function (t) {
      return t.page
        ? '<a class="kb-tg" href="../' + esc(t.page) + '">' + esc(t.name) + '</a>'
        : '<span class="kb-tg kb-tg-plain">' + esc(t.name) + '</span>';
    }).join('');
    return '<p class="kb-lbl kb-sp">// Topics</p><div class="kb-tags">' + chips + '</div>';
  }

  function specHTML(d) {
    var rows = [];
    if (d.series) {
      rows.push(['Series', d.seriesPage
        ? '<a class="kb-lk" href="' + esc(d.seriesPage) + '">' + esc(d.series) + '</a>'
        : esc(d.series)]);
    }
    if (d.epno) rows.push(['Episode', esc(d.epno)]);
    if (d.dur) rows.push(['Runtime', esc(d.dur)]);
    if (d.nchapters) rows.push(['Chapters', String(d.nchapters)]);
    if (d.pos && d.nser) {
      rows.push(['In series', '<a class="kb-lk" href="../library.html#s=' +
        encodeURIComponent(d.series) + '">' + d.pos + ' of ' + d.nser + '</a>']);
    }
    if (!rows.length) return '';
    return '<table class="kb-spec">' + rows.map(function (r) {
      return '<tr><td class="kb-k">' + r[0] + '</td><td class="kb-v">' + r[1] + '</td></tr>';
    }).join('') + '</table>';
  }

  function richHTML(d) {
    var opening = d.quote
      ? '<blockquote class="kb-q">' + esc(d.quote) + '</blockquote>' +
        (d.guest ? '<p class="kb-attrib">' + esc(d.guest) + '</p>' : '')
      /* 17 episodes have no pull quote. The summary stands in, so the card does
         not lose its opening. Neither is ever invented. */
      : (d.summary ? '<p class="kb-sum">' + esc(d.summary) + '</p>' +
                     (d.guest ? '<p class="kb-attrib">' + esc(d.guest) + '</p>' : '')
                   : (d.guest ? '<p class="kb-attrib">' + esc(d.guest) + '</p>' : ''));

    var listen = (!d.video && d.spotify)
      ? '<a class="kb-ghost" href="' + esc(d.spotify) + '" target="_blank" rel="noopener">Listen</a>'
      : '';

    return '<div class="kb-card" role="dialog" aria-modal="true" aria-label="' +
      esc(d.title) + '" tabindex="-1">' +
      '<div class="kb-stamp"><a class="kb-coord" href="../index.html#pin=' + esc(d.slug) +
        '" title="Open this episode on the globe">' + coordText(d) + '</a>' +
        '<span class="kb-dt">' + esc(String(d.date || '').toUpperCase()) + '</span></div>' +
      mediaHTML(d) +
      '<div class="kb-bd">' + opening + '<hr>' +
        '<div class="kb-cols">' +
          '<div><h3><a class="kb-lk" href="' + esc(d.page) + '">' + esc(d.title) + '</a></h3>' +
            chaptersHTML(d) + '</div>' +
          '<div>' + specHTML(d) + tagsHTML(d) + '</div>' +
        '</div>' +
        '<div class="kb-row">' +
          '<a class="kb-cta" href="' + esc(d.page) + '">Open the episode<span>&rarr;</span></a>' +
          '<span class="kb-actions">' + listen +
          '<button class="kb-sh" type="button" data-url="' + esc(d.shareUrl || d.page) +
            '" data-title="' + esc(d.title) + '" aria-label="Share this episode">' + SHARE_SVG +
            '<span class="kb-lab">Share</span></button></span>' +
        '</div>' +
      '</div></div>';
  }

  function plainHTML(tile) {
    var title = tile.dataset.title || '';
    var guest = tile.dataset.guest || '';
    var desc = tile.dataset.desc || 'Full episode details and show notes coming soon.';
    var href = tile.getAttribute('href') || tile.dataset.readmore || '../podcast.html';
    var yt = tile.dataset.ytId || '';
    var media = yt
      ? '<button class="kb-med" type="button" aria-label="Play episode">' +
        '<img src="https://i.ytimg.com/vi/' + esc(yt) + '/maxresdefault.jpg" alt="" ' +
        'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/' + esc(yt) +
        '/mqdefault.jpg\'"><span class="kb-play">' + PLAY_SVG + '</span></button>'
      : '';
    return '<div class="kb-card kb-card-plain" role="dialog" aria-modal="true" aria-label="' +
      esc(title) + '" tabindex="-1">' + media +
      '<div class="kb-bd"><h3>' + esc(title) + '</h3>' +
      (guest ? '<p class="kb-attrib">' + esc(guest) + '</p>' : '') +
      '<p class="kb-sum">' + esc(desc) + '</p>' +
      '<div class="kb-row"><a class="kb-cta" href="' + esc(href) +
      '">Open the episode<span>&rarr;</span></a></div></div></div>';
  }

  function openModal(tile) {
    lastFocus = tile;
    var idx = tile.dataset.epIndex;
    var d = (DATA && idx != null) ? DATA[Number(idx)] : null;
    overlay.innerHTML = d ? richHTML(d) : plainHTML(tile);
    overlay.classList.add('active');
    document.body.classList.add('kb-modal-open');

    var card = overlay.querySelector('.kb-card');
    if (card) {
      /* The shine runs twice when the card appears, so people who never hover
         anything still see it, then once per hover afterwards. */
      card.classList.add('opening');
      card.addEventListener('animationend', function (ev) {
        if (ev.target.classList && ev.target.classList.contains('kb-coord')) {
          card.classList.remove('opening');
        }
      });
      card.focus();
    }

    var med = overlay.querySelector('button.kb-med');
    if (med) {
      med.addEventListener('click', function () {
        var vid = d ? d.video : (tile.dataset.ytId || '');
        if (!vid) return;
        var f = document.createElement('iframe');
        f.className = 'kb-frame';
        f.src = 'https://www.youtube-nocookie.com/embed/' + vid + '?autoplay=1';
        f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture';
        f.setAttribute('allowfullscreen', '');
        f.setAttribute('title', d ? d.title : title2(tile));
        med.parentNode.replaceChild(f, med);
      });
    }

    if (!pushed) {
      try { history.pushState({ kbModal: true }, ''); pushed = true; } catch (e) {}
    }
  }

  function title2(tile) { return tile.dataset.title || ''; }

  function closeModal(fromPop) {
    if (!overlay.classList.contains('active')) return;
    overlay.classList.remove('active');
    overlay.innerHTML = '';
    document.body.classList.remove('kb-modal-open');
    if (lastFocus) { lastFocus.focus(); lastFocus = null; }
    if (fromPop) {
      pushed = false;
    } else if (pushed) {
      pushed = false;
      try { history.back(); } catch (e) {}
    }
  }

  Array.prototype.forEach.call(tiles, function (tile) {
    tile.addEventListener('click', function (ev) {
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey || ev.button !== 0) return;
      ev.preventDefault();
      openModal(tile);
    });
  });

  overlay.addEventListener('click', function (ev) {
    if (ev.target === overlay) closeModal();
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') closeModal();
  });
  window.addEventListener('popstate', function () { closeModal(true); });

  overlay.addEventListener('click', function (ev) {
    var btn = ev.target.closest ? ev.target.closest('.kb-sh') : null;
    if (!btn) return;
    var url = btn.dataset.url, title = btn.dataset.title;
    if (navigator.share) {
      navigator.share({ title: title, url: url }).catch(function () {});
      return;
    }
    var done = function (ok) {
      var lab = btn.querySelector('.kb-lab');
      var before = lab ? lab.textContent : null;
      btn.classList.add('copied');
      if (lab) lab.textContent = ok ? 'Link copied' : 'Copy failed';
      setTimeout(function () {
        btn.classList.remove('copied');
        if (lab) lab.textContent = before;
      }, 1800);
    };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(function () { done(true); },
                                              function () { done(false); });
      return;
    }
    var ta = document.createElement('textarea');
    ta.value = url; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    done(ok);
  });
})();
