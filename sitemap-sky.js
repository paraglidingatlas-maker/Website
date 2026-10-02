/* The sitemap as a night sky (sitemap.html).

   Every star is an episode and every constellation a series: the episodes sit
   along the lines of their series' drawing from the library, and the drawing
   is only drawn in once the constellation has been found. The knowledge base
   categories are regions of the sky. Every page that is not an episode is on
   the ground underneath, always in reach. Approved in the sitemap prototype,
   October 2026 ("Night sky").

   The data is window.SITEMAP_SKY, written into the page by generate_sitemap.py:
   the tree of the site, a little about each episode for its card, and the
   series drawings. Which constellations have been found is remembered in this
   browser only. Without script the page shows the full text index instead. */
(function () {
  'use strict';
  var root = document.querySelector('.sky');
  var DATA = window.SITEMAP_SKY;
  if (!root || !DATA) return;
  var TREE = DATA.tree, EP_META = DATA.meta;
  var NS = 'http://www.w3.org/2000/svg';
  var KEY = 'pa-sitemap-sky';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var view = root.querySelector('.sky-view');
  var svg = root.querySelector('.sky-svg');
  var canvas = root.querySelector('.sky-stars');
  var card = root.querySelector('.sky-card');
  var list = root.querySelector('.sky-list');
  var toast = root.querySelector('.sky-toast');
  var count = root.querySelector('.sky-count');
  var ground = root.querySelector('.sky-ground');
  var ctx = canvas.getContext('2d');
  var dead = false, toastT = null;

  /* The library's own series drawings, on a 120 by 120 field. They come from
     library.js through the build (tools/episode_globes.js), so a drawing
     changed in the library changes here too. */
  var GLYPH = DATA.glyphs || {};

  function el(parent, tag, attrs) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    parent.appendChild(e);
    return e;
  }
  function href(u) { return u; }
  function byLabel(arr, l) { for (var i = 0; i < arr.length; i++) if (arr[i].label === l) return arr[i]; return null; }
  var seed = 20261002;
  function rnd() {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }

  /* ---- What is in the sky ---- */
  var pod = byLabel(TREE.children, 'Podcast');
  var lib = byLabel(pod.children, 'Episode Library');
  var kb = byLabel(TREE.children, 'Knowledge Base');
  var seriesByName = {};
  lib.children.forEach(function (s) { seriesByName[s.label] = s; });

  var world = el(svg, 'g', {});
  var gRegions = el(world, 'g', {});
  var gCons = el(world, 'g', {});

  /* Regions are the knowledge base categories; their series sit inside them.
     Regions are packed into rows so the whole sky has roughly the shape of a
     screen and can be seen at once without the stars becoming specks. */
  var cons = [], regions = [], CELL = 370, ROWH = 590, MAXW = 2900;
  var rowX = 0, rowI = 0, rowW = [];
  kb.children.forEach(function (cat) {
    var names = cat.children.map(function (g) { return g.label; }).filter(function (n) { return seriesByName[n]; });
    var w = names.length * CELL + 90;
    if (rowX && rowX + w > MAXW) { rowW.push(rowX); rowX = 0; rowI++; }
    var reg = { d: cat, x0: rowX, w: w, row: rowI, names: names };
    regions.push(reg);
    rowX += w;
  });
  rowW.push(rowX);
  var W = Math.max.apply(null, rowW) + 160, H = (rowI + 1) * ROWH + 90;
  regions.forEach(function (reg) {
    var left = (W - rowW[reg.row]) / 2 + reg.x0, top = 60 + reg.row * ROWH;
    reg.cx = left + reg.w / 2; reg.y = top + 60;
    reg.names.forEach(function (name, i) {
      var sr = seriesByName[name], n = sr.children.length;
      var size = Math.max(210, Math.min(330, 200 + n * 9));
      cons.push({ d: sr, name: name, guide: byLabel(reg.d.children, name), region: reg, n: n, size: size,
                  x: left + 45 + (i + 0.5) * CELL, y: top + 310 + ((i % 2) ? 26 : -18) + (rnd() - 0.5) * 24, found: false, stars: [] });
    });
  });

  regions.forEach(function (r) {
    r.g = el(gRegions, 'g', { class: 'sky-region', tabindex: '0', role: 'button', transform: 'translate(' + r.cx + ',' + r.y + ')' });
    r.g.setAttribute('aria-label', r.d.label + ', knowledge base category');
    el(r.g, 'path', { d: 'M' + (-r.w / 2 + 50) + ',40H' + (r.w / 2 - 50), class: 'sky-region-rule' });
    var lab = el(r.g, 'g', { class: 'sky-lab' });
    el(lab, 'rect', { x: -170, y: -24, width: 340, height: 48, class: 'sky-hit' });
    var t = el(lab, 'text', { class: 'sky-region-name' });
    t.textContent = r.d.label;
  });

  cons.forEach(function (c) {
    var sc = c.size / 120;
    c.g = el(gCons, 'g', { class: 'sky-con', transform: 'translate(' + c.x.toFixed(1) + ',' + c.y.toFixed(1) + ')' });
    c.art = el(c.g, 'g', { class: 'sky-art', transform: 'scale(' + sc.toFixed(3) + ') translate(-60,-60)' });
    c.art.innerHTML = GLYPH[c.name] || '';
    c.lines = [].slice.call(c.art.querySelectorAll('circle,path,rect'));
    c.lines.forEach(function (ln) { ln.setAttribute('pathLength', '1'); });
    c.gStars = el(c.g, 'g', {});
    c.nameEl = el(c.g, 'g', { class: 'sky-name', tabindex: '0', role: 'button', transform: 'translate(0,' + (c.size / 2 + 34) + ')' });
    c.nameEl.setAttribute('aria-label', c.name + ', ' + c.n + (c.n === 1 ? ' episode' : ' episodes'));
    var nl = el(c.nameEl, 'g', { class: 'sky-lab' });
    el(nl, 'rect', { x: -140, y: -18, width: 280, height: 50, class: 'sky-hit' });
    var t1 = el(nl, 'text', { class: 'sky-name-main' }); t1.textContent = c.name;
    var t2 = el(nl, 'text', { class: 'sky-name-sub', y: 20 }); t2.textContent = c.n + (c.n === 1 ? ' episode' : ' episodes');
  });

  /* Each episode becomes a star placed on its series' emblem, spaced evenly
     along the lines of the drawing, so the stars really do make the shape. */
  function placeStars() {
    cons.forEach(function (c) {
      var base = c.g.getCTM();
      if (!base) return;
      var inv = base.inverse();
      var lens = c.lines.map(function (ln) { try { return ln.getTotalLength(); } catch (e) { return 0; } });
      var total = lens.reduce(function (a, b) { return a + b; }, 0) || 1;
      c.d.children.forEach(function (ep, k) {
        var at = (k + 0.5) / c.n * total, i = 0;
        while (i < lens.length - 1 && at > lens[i]) { at -= lens[i]; i++; }
        var ln = c.lines[i], p = ln.getPointAtLength(Math.min(at, lens[i]));
        var m = inv.multiply(ln.getCTM());
        var sx = p.x * m.a + p.y * m.c + m.e, sy = p.x * m.b + p.y * m.d + m.f;
        var g = el(c.gStars, 'g', { class: 'sky-star', tabindex: '0', role: 'button', transform: 'translate(' + sx.toFixed(1) + ',' + sy.toFixed(1) + ')' });
        g.setAttribute('aria-label', ep.label);
        el(g, 'circle', { r: 15, class: 'sky-hit' });
        var dot = el(g, 'g', { class: 'sky-dot' });
        el(dot, 'circle', { r: 9, class: 'sky-glow' });
        var r = 2.3 + rnd() * 1.5;
        var core = el(dot, 'circle', { r: r.toFixed(1), class: 'sky-core' });
        core.style.animationDelay = (-rnd() * 5).toFixed(2) + 's';
        c.stars.push({ d: ep, con: c, g: g, x: c.x + sx, y: c.y + sy });
      });
    });
  }

  /* ---- The ground: every page that is not an episode, always in reach ---- */
  (function () {
    var h = '<svg class="sky-ridge" viewBox="0 0 1200 40" preserveAspectRatio="none" aria-hidden="true"><path d="M0,34 L70,28 L130,14 L180,6 L225,12 L300,27 L380,32 L470,24 L540,30 L640,21 L720,31 L820,18 L900,29 L1010,23 L1100,31 L1200,26"/></svg><div class="sky-ground-in">';
    function group(title, items) {
      h += '<div class="sky-g"><h2>' + title + '</h2><ul>';
      items.forEach(function (it) {
        h += '<li><a href="' + href(it.url) + '">' + (it.img ? '<img src="' + it.img + '" alt="">' : '') +
             '<span>' + it.label + (it.sub && it.kind === 'trip' ? '<small>' + it.sub + '</small>' : '') + '</span></a></li>';
      });
      h += '</ul></div>';
    }
    var trips = byLabel(TREE.children, 'Trips'), about = byLabel(TREE.children, 'About Me'), legal = byLabel(TREE.children, 'Legal');
    group('Trips', trips.children);
    group('Listen And Learn', [{ label: 'Home', url: 'index.html' }, { label: 'Podcast', url: 'podcast.html' }, { label: 'Episode Library', url: 'library.html' },
                               { label: 'Topics', url: 'tags.html' }, { label: 'Knowledge Base', url: 'knowledge-base.html' }]);
    group('About', [{ label: 'About Me', url: 'about.html' }].concat(about.children));
    group('Legal', legal.children);
    ground.innerHTML = h + '</div>';
  })();

  /* ---- Camera ---- */
  var cam = { x: W / 2, y: H / 2, k: 0.5 }, camT = { x: W / 2, y: H / 2, k: 0.5 }, camS = {};
  var vw = 0, vh = 0, dpr = 1, bg = [], raf = 0, t0 = 0, shoot = null, shootT = 0, ambient = 0;
  var narrow = false;

  function clampCam(c) {
    var hw = vw / 2 / c.k, hh = vh / 2 / c.k, m = 260 / c.k;
    c.x = Math.max(Math.min(hw, W / 2) - m, Math.min(Math.max(W - hw, W / 2) + m, c.x));
    c.y = Math.max(Math.min(hh, H / 2) - m, Math.min(Math.max(H - hh, H / 2) + m, c.y));
  }
  function fitAll() {
    var top = narrow ? 0 : 172, bottom = narrow ? 0 : 62;       /* clear of the heading and the controls */
    var k = narrow ? vh / H : Math.min((vw - 60) / W, (vh - top - bottom) / H);
    camT.k = Math.max(0.3, k);
    camT.x = narrow ? vw / 2 / camT.k : W / 2;
    camT.y = H / 2 - ((top - bottom) / 2) / camT.k;
  }
  function frameCon(c) {
    var pad = narrow ? 40 : 150, top = narrow ? 30 : 130, bottom = narrow ? 190 : 90;
    var k = Math.min((vw - pad * 2 - (narrow ? 0 : 280)) / (c.size + 40), (vh - top - bottom) / (c.size + 90), 1.5);
    camT.k = Math.max(0.5, k);
    camT.x = c.x + (narrow ? 0 : 140 / camT.k);
    camT.y = c.y + 20 + ((bottom - top) / 2) / camT.k;
  }
  function sx(x) { return vw / 2 + (x - cam.x) * cam.k; }
  function sy(y) { return vh / 2 + (y - cam.y) * cam.k; }

  function draw(now) {
    world.setAttribute('transform', 'translate(' + (vw / 2 - cam.x * cam.k).toFixed(2) + ',' + (vh / 2 - cam.y * cam.k).toFixed(2) + ') scale(' + cam.k.toFixed(4) + ')');
    /* Stars and names shrink less than the sky does, so they stay readable
       when the whole of it is in view. */
    var ss = Math.max(1, Math.min(2.4, 0.95 / cam.k)), ls = Math.max(1, Math.min(1.5, 0.62 / cam.k));
    if (ss !== world._ss) { world.style.setProperty('--ss', ss.toFixed(3)); world.style.setProperty('--ls', ls.toFixed(3)); world._ss = ss; }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, vw, vh);
    ctx.fillStyle = 'rgb(180,180,180)';
    var ox = -cam.x * 0.14, oy = -cam.y * 0.14;
    for (var i = 0; i < bg.length; i++) {
      var s = bg[i];
      var px = ((s[0] + ox * s[4]) % vw + vw) % vw, py = ((s[1] + oy * s[4]) % vh + vh) % vh;
      ctx.globalAlpha = s[3];
      ctx.beginPath(); ctx.arc(px, py, s[2], 0, 6.2832); ctx.fill();
    }
    if (shoot) {
      var p = (now - shoot.t) / 900;
      if (p >= 1) shoot = null;
      else {
        var hx = shoot.x + shoot.dx * p, hy = shoot.y + shoot.dy * p, a = Math.sin(p * Math.PI);
        var grd = ctx.createLinearGradient(hx, hy, hx - shoot.dx * 0.22, hy - shoot.dy * 0.22);
        grd.addColorStop(0, 'rgba(246,244,244,' + (0.9 * a).toFixed(2) + ')');
        grd.addColorStop(1, 'rgba(255,117,23,0)');
        ctx.globalAlpha = 1; ctx.strokeStyle = grd; ctx.lineWidth = 1.6; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(hx, hy); ctx.lineTo(hx - shoot.dx * 0.22, hy - shoot.dy * 0.22); ctx.stroke();
      }
    }
    ctx.globalAlpha = 1;
    if (cardStar) placeCard();
  }
  function easeIO(t) { return t < 0 ? 0 : t > 1 ? 1 : (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2); }
  function go(instant) {
    cancelAnimationFrame(raf);
    camS = { x: cam.x, y: cam.y, k: cam.k };
    if (reduce || instant) { cam.x = camT.x; cam.y = camT.y; cam.k = camT.k; draw(performance.now()); return; }
    t0 = performance.now();
    (function tick(now) {
      if (dead) return;
      var c = easeIO((now - t0) / 950);
      cam.x = camS.x + (camT.x - camS.x) * c; cam.y = camS.y + (camT.y - camS.y) * c; cam.k = camS.k + (camT.k - camS.k) * c;
      draw(now);
      if (now - t0 < 950) raf = requestAnimationFrame(tick);
    })(t0);
  }
  /* Now and then a shooting star crosses, even when nothing else is moving. */
  function idle(now) {
    if (dead) return;
    if (!reduce && !shoot && now > shootT) {
      var fromLeft = rnd() > 0.5;
      shoot = { t: now, x: (fromLeft ? 0.1 : 0.9) * vw + (rnd() - 0.5) * vw * 0.3, y: rnd() * vh * 0.35,
                dx: (fromLeft ? 1 : -1) * (260 + rnd() * 240), dy: 120 + rnd() * 120 };
      shootT = now + 5000 + rnd() * 7000;
    }
    if (shoot) draw(now);
    ambient = requestAnimationFrame(idle);
  }

  /* ---- Finding ---- */
  function load() { try { var v = JSON.parse(window.localStorage.getItem(KEY) || 'null'); if (v && v.f) return v.f; } catch (e) {} return {}; }
  function save() {
    var f = {};
    cons.forEach(function (c) { if (c.found) f[c.name] = 1; });
    try { window.localStorage.setItem(KEY, JSON.stringify({ f: f })); } catch (e) {}
  }
  function foundCount() { return cons.filter(function (c) { return c.found; }).length; }
  function tally() {
    var n = foundCount();
    count.textContent = n === cons.length ? 'All ' + cons.length + ' constellations found' : n + ' of ' + cons.length + ' constellations found';
    root.classList.toggle('is-complete', n === cons.length);
  }
  function say(msg) {
    toast.textContent = msg; toast.classList.add('visible');
    clearTimeout(toastT);
    toastT = setTimeout(function () { toast.classList.remove('visible'); }, 3400);
  }
  function find(c, quiet) {
    if (c.found) return false;
    c.found = true;
    c.g.classList.add('is-found');
    c.lines.forEach(function (ln, i) { ln.style.transitionDelay = (quiet ? 0 : 0.05 * i).toFixed(2) + 's'; });
    if (!quiet) {
      save(); tally();
      var left = cons.length - foundCount();
      say(c.name + ' found. ' + (left ? left + (left === 1 ? ' constellation' : ' constellations') + ' still hidden.' : 'That is every constellation in the sky.'));
    }
    return true;
  }

  /* ---- Card and list ---- */
  var cardStar = null, cardPinned = false, openCon = null;
  function placeCard() {
    var px = sx(cardStar.x), py = sy(cardStar.y);
    var cw = card.offsetWidth, ch = card.offsetHeight;
    var left = Math.max(10, Math.min(px + 18, vw - cw - 10));
    /* On a phone the episode list rises from the bottom, so the card keeps above it. */
    var floor = vh - 10 - (narrow && list.classList.contains('visible') ? list.offsetHeight : 0);
    var top = py + 18;
    if (top + ch > floor) top = py - 18 - ch;
    if (top < 10) top = Math.max(10, floor - ch);
    card.style.left = left + 'px';
    card.style.top = top + 'px';
  }
  function showStar(s, pin) {
    var m = EP_META[s.d.url] || {};
    var h = '<p class="mp-kick">' + [s.con.found ? s.con.name : 'A star in an unnamed constellation', s.con.found ? m.epno : ''].filter(Boolean).join(' \u00B7 ') + '</p><p class="popup-title"></p>';
    if (m.guest) h += '<p class="mp-guest"></p>';
    h += '<div class="mp-rd">' + (m.nch ? '<span>' + (m.nch === 1 ? '1 chapter' : m.nch + ' chapters') + '</span>' : '') + (m.dur ? '<span>' + m.dur + '</span>' : '') + '</div>';
    h += '<a class="popup-link">Open the episode <i>&rarr;</i></a>';
    card.querySelector('.mp-bd').innerHTML = h;
    card.querySelector('.popup-title').textContent = s.d.label;
    var g = card.querySelector('.mp-guest'); if (g) g.textContent = m.guest;
    card.querySelector('.popup-link').href = href(s.d.url);
    if (cardStar) cardStar.g.classList.remove('is-picked');
    cardStar = s; cardPinned = !!pin;
    s.g.classList.add('is-picked');
    card.classList.add('visible');
    card.classList.toggle('pinned', cardPinned);
    placeCard();
  }
  function hideCard() {
    if (!cardStar) return;
    cardStar.g.classList.remove('is-picked');
    cardStar = null; cardPinned = false;
    card.classList.remove('visible', 'pinned');
  }
  function showList(c) {
    openCon = c;
    var h = '<p class="mp-kick">' + c.region.d.label + '</p><h2>' + c.name + '</h2><p class="sky-list-links">';
    if (c.guide) h += '<a href="' + href(c.guide.url) + '">Series guide</a>';
    h += '<a href="' + href(c.d.url) + '">Open in the library</a></p><ol>';
    c.stars.forEach(function (s, i) { h += '<li><button type="button" data-i="' + i + '"></button></li>'; });
    h += '</ol><button type="button" class="sky-list-close" aria-label="Close this list">&times;</button>';
    list.innerHTML = h;
    [].forEach.call(list.querySelectorAll('ol button'), function (b, i) { b.textContent = c.stars[i].d.label; });
    list.classList.add('visible');
    cons.forEach(function (o) { o.g.classList.toggle('is-open', o === c); });
  }
  function hideList() {
    openCon = null;
    list.classList.remove('visible');
    cons.forEach(function (o) { o.g.classList.remove('is-open'); });
  }
  function openConstellation(c) {
    find(c);
    showList(c);
    frameCon(c); go();
  }
  function regionCard(r) {
    hideCard();
    var h = '<p class="mp-kick">Knowledge base</p><p class="popup-title"></p><div class="mp-rd"><span>' + r.d.sub + '</span></div>' +
            '<a class="popup-link" href="' + href(r.d.url) + '">Open the category <i>&rarr;</i></a>';
    card.querySelector('.mp-bd').innerHTML = h;
    card.querySelector('.popup-title').textContent = r.d.label;
    cardStar = { x: r.cx, y: r.y, g: r.g, con: null }; cardPinned = true;
    card.classList.add('visible', 'pinned');
    placeCard();
  }

  /* ---- Pointer ---- */
  var ptrs = {}, dragged = false, last = null, pinch0 = 0, pinchK = 1;
  function local(e) { var r = view.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
  function starOf(t) {
    var g = t.closest ? t.closest('.sky-star') : null;
    if (!g) return null;
    for (var i = 0; i < cons.length; i++) for (var j = 0; j < cons[i].stars.length; j++) if (cons[i].stars[j].g === g) return cons[i].stars[j];
    return null;
  }
  function conOfName(t) {
    var g = t.closest ? t.closest('.sky-name') : null;
    if (!g) return null;
    for (var i = 0; i < cons.length; i++) if (cons[i].nameEl === g) return cons[i];
    return null;
  }
  function regionOf(t) {
    var g = t.closest ? t.closest('.sky-region') : null;
    if (!g) return null;
    for (var i = 0; i < regions.length; i++) if (regions[i].g === g) return regions[i];
    return null;
  }
  function zoomAt(px, py, k) {
    k = Math.max(0.3, Math.min(2.2, k));
    var wx = cam.x + (px - vw / 2) / cam.k, wy = cam.y + (py - vh / 2) / cam.k;
    cam.k = k; cam.x = wx - (px - vw / 2) / k; cam.y = wy - (py - vh / 2) / k;
    clampCam(cam);
    camT.x = cam.x; camT.y = cam.y; camT.k = cam.k;
    cancelAnimationFrame(raf); draw(performance.now());
  }
  function nearHint(p) {
    var wx = cam.x + (p[0] - vw / 2) / cam.k, wy = cam.y + (p[1] - vh / 2) / cam.k;
    cons.forEach(function (c) { c.g.classList.toggle('is-near', !c.found && Math.hypot(c.x - wx, c.y - wy) < c.size * 0.62); });
  }
  view.addEventListener('pointerdown', function (e) {
    if (e.target.closest('.sky-card, .sky-list, .sky-ctrl')) return;
    ptrs[e.pointerId] = local(e); dragged = false; last = local(e);
    var ids = Object.keys(ptrs);
    if (ids.length === 2) { var a = ptrs[ids[0]], b = ptrs[ids[1]]; pinch0 = Math.hypot(a[0] - b[0], a[1] - b[1]); pinchK = cam.k; }
  });
  view.addEventListener('pointermove', function (e) {
    var p = local(e);
    if (!ptrs[e.pointerId]) {
      if (e.pointerType === 'mouse') {
        nearHint(p);
        if (!cardPinned) { var s = starOf(e.target); if (s) { if (cardStar !== s) showStar(s, false); } else hideCard(); }
      }
      return;
    }
    ptrs[e.pointerId] = p;
    var ids = Object.keys(ptrs);
    if (ids.length === 2 && pinch0) {
      var a = ptrs[ids[0]], b = ptrs[ids[1]];
      dragged = true;
      zoomAt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, pinchK * Math.hypot(a[0] - b[0], a[1] - b[1]) / pinch0);
      return;
    }
    var dx = p[0] - last[0], dy = p[1] - last[1];
    if (!dragged && Math.hypot(dx, dy) < 5) return;
    if (!dragged) { dragged = true; view.classList.add('is-dragging'); try { view.setPointerCapture(e.pointerId); } catch (err) {} if (!cardPinned) hideCard(); }
    last = p;
    cancelAnimationFrame(raf);
    cam.x -= dx / cam.k; cam.y -= dy / cam.k;
    clampCam(cam);
    camT.x = cam.x; camT.y = cam.y; camT.k = cam.k;
    draw(performance.now());
  });
  function up(e) { delete ptrs[e.pointerId]; if (Object.keys(ptrs).length < 2) pinch0 = 0; view.classList.remove('is-dragging'); }
  view.addEventListener('pointerup', up);
  view.addEventListener('pointercancel', up);
  function act(target) {
    var s = starOf(target);
    if (s) {
      if (!s.con.found || openCon !== s.con) openConstellation(s.con);
      showStar(s, true);
      return true;
    }
    var c = conOfName(target);
    if (c) { hideCard(); openConstellation(c); return true; }
    var r = regionOf(target);
    if (r) { regionCard(r); return true; }
    return false;
  }
  view.addEventListener('click', function (e) {
    if (dragged) { dragged = false; return; }
    if (e.target.closest('.sky-card, .sky-list, .sky-ctrl')) return;
    if (act(e.target)) return;
    /* Stars are small, and smaller still when the whole sky is in view. A click
       or tap that lands close to one counts as landing on it. */
    var p = local(e), coarse = (e.pointerType && e.pointerType !== 'mouse') || window.matchMedia('(pointer: coarse)').matches;
    var best = null, bd = coarse ? 30 : 14;
    cons.forEach(function (c) { c.stars.forEach(function (st) {
      var d = Math.hypot(sx(st.x) - p[0], sy(st.y) - p[1]);
      if (d < bd) { bd = d; best = st; }
    }); });
    if (best) act(best.g); else hideCard();
  });
  view.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { hideCard(); hideList(); return; }
    if ((e.key === 'Enter' || e.key === ' ') && !e.target.closest('.sky-card, .sky-list, .sky-ctrl')) { if (act(e.target)) e.preventDefault(); }
  });
  view.addEventListener('wheel', function (e) {
    if (!e.ctrlKey && !e.metaKey) return;
    e.preventDefault();
    var p = local(e), pinchy = e.ctrlKey && Math.abs(e.deltaY) < 40;
    zoomAt(p[0], p[1], cam.k * Math.pow(2, -e.deltaY * (pinchy ? 0.02 : 0.004)));
  }, { passive: false });

  list.addEventListener('click', function (e) {
    if (e.target.closest('.sky-list-close')) { hideList(); hideCard(); fitAll(); go(); return; }
    var b = e.target.closest('ol button');
    if (b && openCon) showStar(openCon.stars[+b.dataset.i], true);
  });
  list.addEventListener('mouseover', function (e) {
    var b = e.target.closest('ol button');
    if (b && openCon && !cardPinned) showStar(openCon.stars[+b.dataset.i], false);
  });
  root.querySelector('.sky-ctrl').addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.z === 'reset') { hideCard(); hideList(); fitAll(); go(); return; }
    camT.k = Math.max(0.3, Math.min(2.2, cam.k * (b.dataset.z === 'in' ? 1.35 : 1 / 1.35)));
    camT.x = cam.x; camT.y = cam.y; clampCam(camT); go();
  });
  root.querySelector('.sky-actions').addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.a === 'random') {
      /* A way in for someone who does not know where to start. */
      var all = [];
      cons.forEach(function (c) { all = all.concat(c.stars); });
      var s = all[Math.floor(Math.random() * all.length)];
      openConstellation(s.con);
      showStar(s, true);
    } else if (b.dataset.a === 'all') {
      var on = !root.classList.contains('is-named');
      root.classList.toggle('is-named', on);
      b.textContent = on ? 'Hide the names again' : 'Name every constellation';
    } else if (b.dataset.a === 'again') {
      try { window.localStorage.removeItem(KEY); } catch (err) {}
      cons.forEach(function (c) { c.found = false; c.g.classList.remove('is-found'); });
      hideCard(); hideList(); tally(); fitAll(); go();
      say('The sky is unnamed again.');
    }
  });

  /* ---- Size ---- */
  function resize(first) {
    var w = view.clientWidth, h = view.clientHeight;
    if (!w || !h) return;
    vw = w; vh = h; narrow = w < 760;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    svg.setAttribute('width', w); svg.setAttribute('height', h);
    bg = [];
    var s0 = seed; seed = 77;
    for (var i = 0, n = Math.round(w * h / 2600); i < n; i++) bg.push([rnd() * w, rnd() * h, 0.3 + rnd() * 0.8, 0.06 + rnd() * rnd() * 0.5, 0.3 + rnd() * 1.3]);
    seed = s0;
    root.classList.toggle('is-narrow', narrow);
    if (first) {
      fitAll(); cam.x = camT.x; cam.y = camT.y; cam.k = camT.k;
      draw(performance.now());
      placeStars();
      var f = load();
      cons.forEach(function (c) { if (f[c.name]) find(c, true); });
      tally();
    } else if (openCon) { frameCon(openCon); go(true); }
    else { fitAll(); go(true); }
  }
  var ro = null, rt = null;
  if (window.ResizeObserver) {
    ro = new ResizeObserver(function () { clearTimeout(rt); rt = setTimeout(function () { resize(false); }, 100); });
    ro.observe(view);
  }
  resize(true);
  shootT = performance.now() + 2500;
  ambient = requestAnimationFrame(idle);

})();
