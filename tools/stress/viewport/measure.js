// In-page measurement for the viewport/zoom stress test.
// Called as page.evaluate(`(${src})(opts)`) where opts = {vw, vh, mode}.
// mode "full": overflow, text clipping, paragraph metrics, covered scan.
// mode "fixed": only fixed/sticky coverage at the current scroll position.
// mode "verify": re-check covered candidates by index list (opts.idx).
(opts) => {
  const vw = opts.vw, vh = opts.vh;
  const de = document.documentElement, body = document.body;
  const CS = new Map();
  const cs = (el) => { let s = CS.get(el); if (!s) { s = getComputedStyle(el); CS.set(el, s); } return s; };
  const vis = (el) => !el.checkVisibility || el.checkVisibility({opacityProperty: true, visibilityProperty: true});
  const sel = (el) => {
    if (!el || el.nodeType !== 1) return String(el);
    const parts = [];
    let e = el;
    for (let i = 0; i < 4 && e && e.nodeType === 1; i++) {
      let s = e.tagName.toLowerCase();
      if (e.id) { parts.unshift(s + '#' + e.id); break; }
      const cls = [...e.classList].filter(c => c.length < 40).slice(0, 3);
      if (cls.length) s += '.' + cls.join('.');
      parts.unshift(s);
      if (e === body || e === de) break;
      e = e.parentElement;
    }
    return parts.join(' > ');
  };
  const txt = (el) => ((el && (el.innerText || el.textContent)) || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  const posOf = (el) => { // nearest fixed/sticky ancestor-or-self
    for (let e = el; e && e !== de; e = e.parentElement) {
      const p = cs(e).position;
      if (p === 'fixed' || p === 'sticky') return {pos: p, sel: sel(e)};
    }
    return null;
  };

  const INTER = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=link],[role=tab]';

  // ---------- fixed / sticky coverage at current scroll ----------
  function fixedCover() {
    const out = [];
    for (const el of body.querySelectorAll('*')) {
      const s = cs(el), p = s.position;
      if (p !== 'fixed' && p !== 'sticky') continue;
      if (!vis(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      const t = Math.max(0, r.top), b = Math.min(vh, r.bottom), l = Math.max(0, r.left), rr = Math.min(vw, r.right);
      if (b <= t || rr <= l) continue;
      const stuckTop = p === 'sticky' && s.top !== 'auto' && Math.abs(r.top - parseFloat(s.top)) < 1.5;
      const stuckBot = p === 'sticky' && s.bottom !== 'auto' && Math.abs((vh - r.bottom) - parseFloat(s.bottom)) < 1.5;
      out.push({sel: sel(el), pos: p, top: Math.round(r.top), h: Math.round(r.height), visH: Math.round(b - t),
        frac: +((b - t) / vh).toFixed(3), wfrac: +((rr - l) / vw).toFixed(3), stuck: p === 'fixed' || stuckTop || stuckBot,
        pe: s.pointerEvents, bg: s.backgroundColor, z: s.zIndex, text: txt(el).slice(0, 40)});
    }
    // union of vertical coverage by wide, stuck, non-stage overlays that take pointer events
    const iv = out.filter(o => o.stuck && o.wfrac >= 0.5 && o.pe !== 'none' && o.h < 0.9 * vh)
      .map(o => [Math.max(0, o.top), Math.min(vh, o.top + o.h)]).sort((a, b) => a[0] - b[0]);
    let cov = 0, cur = null;
    for (const [a, b] of iv) {
      if (!cur || a > cur[1]) { if (cur) cov += cur[1] - cur[0]; cur = [a, b]; } else cur[1] = Math.max(cur[1], b);
    }
    if (cur) cov += cur[1] - cur[0];
    const res = {scrollY: Math.round(scrollY), maxScroll: de.scrollHeight - vh, items: out, unionFrac: +(cov / vh).toFixed(3)};
    if (opts.cov) { // interactive elements in view whose centre is under a fixed/sticky layer
      const cv = [];
      for (const el of body.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,summary')) {
        if (!vis(el) || cs(el).pointerEvents === 'none') continue;
        const r = [...el.getClientRects()].find(r => r.width > 2 && r.height > 2); if (!r) continue;
        const x = (r.left + r.right) / 2, y = (r.top + r.bottom) / 2;
        if (x < 0 || x >= vw || y < 0 || y >= vh) continue;
        const hit = document.elementFromPoint(x, y);
        if (!hit || hit === el || el.contains(hit) || hit.contains(el)) continue;
        const po = posOf(hit);
        if (po && !posOf(el)) cv.push({sel: sel(el), text: txt(el).slice(0, 40), by: po.sel, byPos: po.pos, y: Math.round(y)});
      }
      res.coveredByFixed = cv.slice(0, 10); res.nCoveredByFixed = cv.length;
    }
    return res;
  }
  if (opts.mode === 'fixed') return fixedCover();

  // ---------- open modal dialogs / full-screen overlays ----------
  if (opts.mode === 'dialog') {
    const out = [];
    for (const d of body.querySelectorAll('[aria-modal=true],[role=dialog],dialog[open]')) {
      if (!vis(d)) continue;
      const r = d.getBoundingClientRect();
      if (r.width * r.height < 0.5 * vw * vh) continue;
      const ctrls = [...d.querySelectorAll(INTER)].filter(e => vis(e)).map(e => {
        const q = e.getBoundingClientRect();
        const cx = (q.left + q.right) / 2, cy = (q.top + q.bottom) / 2;
        const inView = q.width > 1 && cx >= 0 && cx < vw && cy >= 0 && cy < vh;
        const hit = inView ? document.elementFromPoint(cx, cy) : null;
        return {sel: sel(e), text: (e.getAttribute('aria-label') || txt(e)).slice(0, 40), l: Math.round(q.left), t: Math.round(q.top),
          r: Math.round(q.right), b: Math.round(q.bottom), inView, hittable: !!hit && (hit === e || e.contains(hit) || hit.contains(e)),
          by: hit && !(hit === e || e.contains(hit) || hit.contains(e)) ? sel(hit) : null};
      });
      out.push({sel: sel(d), label: d.getAttribute('aria-label'), cls: d.className, ctrls});
    }
    return out;
  }

  // ---------- interactive element collection (shared by full + verify) ----------
  const clipAncCache = new Map();
  function clipAncs(el) { // ancestors that clip or scroll on some axis
    const out = [];
    for (let e = el.parentElement; e && e !== body && e !== de; e = e.parentElement) {
      const s = cs(e);
      if (s.overflowX !== 'visible' || s.overflowY !== 'visible') out.push(e);
      if (s.position === 'fixed') break;
    }
    return out;
  }
  function visRect(el) { // visible part of the element's first line box, clipped by ancestors and the viewport
    const rs = [...el.getClientRects()].filter(r => r.width > 2 && r.height > 2);
    if (!rs.length) return null;
    let r = rs[0];
    let L = r.left, T = r.top, R = r.right, B = r.bottom;
    let anc = clipAncCache.get(el); if (!anc) { anc = clipAncs(el); clipAncCache.set(el, anc); }
    for (const a of anc) {
      const ar = a.getBoundingClientRect();
      const s = cs(a);
      if (s.overflowX !== 'visible') { L = Math.max(L, ar.left); R = Math.min(R, ar.right); }
      if (s.overflowY !== 'visible') { T = Math.max(T, ar.top); B = Math.min(B, ar.bottom); }
    }
    L = Math.max(L, 0); T = Math.max(T, 0); R = Math.min(R, vw); B = Math.min(B, vh);
    if (R - L < 2 || B - T < 2) return null;
    return {x: (L + R) / 2, y: (T + B) / 2};
  }
  // decorative links (aria-hidden and out of the tab order) are not interactive for anyone: skip them
  const inter = [...body.querySelectorAll(INTER)].filter(el => vis(el) && cs(el).pointerEvents !== 'none' && !el.disabled &&
    !(el.closest('[aria-hidden=true]') && el.getAttribute('tabindex') === '-1'));
  function hitTest(el) {
    const p = visRect(el);
    if (!p) return null; // not on screen at this scroll position
    const hit = document.elementFromPoint(p.x, p.y);
    if (!hit) return null;
    if (hit === el || el.contains(hit) || hit.contains(el)) return {ok: true};
    if (hit.tagName === 'LABEL' && hit.control === el) return {ok: true};
    const po = posOf(hit);
    return {ok: false, by: sel(hit), byText: txt(hit).slice(0, 40), byPos: po ? po.pos + ' ' + po.sel : cs(hit).position,
      x: Math.round(p.x), y: Math.round(p.y)};
  }
  const scrollTo = (y) => window.scrollTo({top: y, left: 0, behavior: 'instant'});

  if (opts.mode === 'verify') {
    const out = [];
    for (const i of opts.idx) {
      const el = inter[i];
      if (!el) { out.push({i, gone: true}); continue; }
      el.scrollIntoView({block: 'center', inline: 'nearest', behavior: 'instant'});
      out.push({i, sel: sel(el), r: hitTest(el)});
    }
    return out;
  }

  // ---------- full ----------
  const res = {};
  res.innerWidth = innerWidth; res.clientWidth = de.clientWidth; res.scrollWidth = de.scrollWidth;
  res.bodyScrollWidth = body.scrollWidth; res.scrollHeight = de.scrollHeight;
  res.vvScale = window.visualViewport ? +visualViewport.scale.toFixed(3) : null;
  res.ovx = {html: cs(de).overflowX, body: cs(body).overflowX};
  res.rootFont = parseFloat(cs(de).fontSize); res.bodyFont = parseFloat(cs(body).fontSize);

  const all = [...body.querySelectorAll('*')];

  // horizontal overflow offenders
  const contained = new Map();
  function isContained(el) {
    if (contained.has(el)) return contained.get(el);
    const p = el.parentElement;
    let v = false;
    if (!p || p === body || p === de) v = false;
    else { const s = cs(p); v = s.overflowX !== 'visible' || isContained(p); }
    contained.set(el, v);
    return v;
  }
  const offenders = [];
  let maxRight = 0;
  for (const el of all) {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (r.right <= vw + 1) continue;
    if (isContained(el)) continue;
    const s = cs(el);
    const fixedEl = !!(posOf(el) && posOf(el).pos === 'fixed');
    const hidden = !vis(el);
    const pr = el.parentElement ? el.parentElement.getBoundingClientRect() : null;
    const root = !pr || el.parentElement === body || pr.right <= vw + 1 || r.width > pr.width + 1;
    if (!hidden && !fixedEl) maxRight = Math.max(maxRight, r.right);
    if (root) offenders.push({sel: sel(el), right: Math.round(r.right), left: Math.round(r.left), w: Math.round(r.width),
      parentW: pr ? Math.round(pr.width) : null, ws: s.whiteSpace, minW: s.minWidth, text: txt(el).slice(0, 40),
      hidden, fixed: fixedEl, transform: s.transform !== 'none' ? s.transform.slice(0, 40) : ''});
  }
  offenders.sort((a, b) => (a.hidden || a.fixed) - (b.hidden || b.fixed) || b.right - a.right);
  res.overflow = {maxRight: Math.round(maxRight), offenders: offenders.slice(0, 8), nOffenders: offenders.filter(o => !o.hidden && !o.fixed).length,
    nHiddenOffenders: offenders.filter(o => o.hidden || o.fixed).length};

  // text clipping and text beyond the viewport
  const clipInfo = new Map();
  function clipChain(el) { // list of {el, x, y, scroll} for ancestors-or-self with non-visible overflow, up to first scroller
    if (clipInfo.has(el)) return clipInfo.get(el);
    const out = [];
    let fixed = false;
    for (let e = el; e && e !== body && e !== de; e = e.parentElement) {
      const s = cs(e);
      if (s.position === 'fixed') fixed = true;
      const x = s.overflowX, y = s.overflowY;
      if (x === 'visible' && y === 'visible') continue;
      const scroll = x === 'auto' || x === 'scroll' || y === 'auto' || y === 'scroll';
      out.push({el: e, cx: x === 'hidden' || x === 'clip', cy: y === 'hidden' || y === 'clip', scroll});
      if (scroll) break;
    }
    const v = {chain: out, fixed};
    clipInfo.set(el, v);
    return v;
  }
  const pvis = new Map();
  const clipped = new Map(); // key: anc sel -> record
  const offscreen = new Map();
  const range = document.createRange();
  const tw = document.createTreeWalker(body, NodeFilter.SHOW_TEXT);
  let nText = 0, tinyText = 0, tinyEx = null;
  const SKIP = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'OPTION', 'TITLE']);
  for (let n = tw.nextNode(); n; n = tw.nextNode()) {
    const t = n.nodeValue;
    if (!t || !t.trim()) continue;
    const pe = n.parentElement;
    if (!pe || SKIP.has(pe.tagName) || pe.closest('svg')) continue;
    let v = pvis.get(pe);
    if (v === undefined) { v = vis(pe); pvis.set(pe, v); }
    if (!v) continue;
    range.selectNodeContents(n);
    const rects = [...range.getClientRects()].filter(r => r.width >= 1 && r.height >= 1);
    if (!rects.length) continue;
    nText++;
    const fs = parseFloat(cs(pe).fontSize);
    if (fs < 12 && t.trim().length > 2) { tinyText++; if (!tinyEx) tinyEx = {sel: sel(pe), fs, text: t.trim().slice(0, 30)}; }
    const {chain, fixed} = clipChain(pe);
    let inScroller = false;
    for (const c of chain) {
      if (c.scroll) { inScroller = true; break; }
      const a = c.el;
      const ar = a.getBoundingClientRect();
      if (a.clientWidth <= 2 || a.clientHeight <= 2) break; // sr-only pattern
      const L = ar.left + a.clientLeft, T = ar.top + a.clientTop, R = L + a.clientWidth, B = T + a.clientHeight;
      let over = 0, axis = '', full = true;
      for (const r of rects) {
        const dx = c.cx ? Math.max(r.right - R, L - r.left) : 0;
        const dy = c.cy ? Math.max(r.bottom - B, T - r.top) : 0;
        if (dx > over) { over = dx; axis = 'x'; }
        if (dy > over) { over = dy; axis = 'y'; }
        const inside = r.right > L + 1 && r.left < R - 1 && r.bottom > T + 1 && r.top < B - 1;
        if (inside) full = false;
      }
      const fsz = parseFloat(cs(pe).fontSize);
      const need = axis === 'y' ? Math.max(3, 0.3 * fsz) : 2;
      if (over > need) {
        const as = cs(a);
        const key = sel(a) + '|' + axis;
        const rec = clipped.get(key) || {anc: sel(a), axis, over: 0, n: 0, full: 0, partial: 0, text: t.trim().slice(0, 50),
          ellipsis: as.textOverflow === 'ellipsis' || cs(pe).textOverflow === 'ellipsis',
          clamp: (as.webkitLineClamp && as.webkitLineClamp !== 'none') || (cs(pe).webkitLineClamp && cs(pe).webkitLineClamp !== 'none'),
          ariaHidden: !!pe.closest('[aria-hidden=true]'), ancW: a.clientWidth, ancH: a.clientHeight, pos: posOf(a), fs: fsz};
        rec.n++; if (full) rec.full++; else rec.partial++;
        if (over > rec.over) { rec.over = Math.round(over); if (!full) rec.text = t.trim().slice(0, 50); }
        clipped.set(key, rec);
        break;
      }
    }
    if (inScroller || fixed) continue;
    // text beyond the viewport horizontally (not inside a scroller)
    let ox = 0, fullOff = true;
    for (const r of rects) {
      ox = Math.max(ox, r.right - vw, -r.left);
      if (r.right > 1 && r.left < vw - 1) fullOff = false;
    }
    if (ox > 2) {
      // is it already clipped away by an ancestor? then it was reported above (or is intentionally hidden)
      if (chain.some(c => c.cx)) continue;
      const key = sel(pe);
      const rec = offscreen.get(key) || {sel: key, over: 0, n: 0, full: 0, text: t.trim().slice(0, 50), ariaHidden: !!pe.closest('[aria-hidden=true]')};
      rec.n++; if (fullOff) rec.full++;
      rec.over = Math.max(rec.over, Math.round(ox));
      offscreen.set(key, rec);
    }
  }
  res.nText = nText;
  res.tinyText = tinyText; res.tinyEx = tinyEx;
  res.clipped = [...clipped.values()].sort((a, b) => b.over - a.over).slice(0, 15);
  res.nClipped = clipped.size;
  res.offscreenText = [...offscreen.values()].sort((a, b) => b.over - a.over).slice(0, 10);
  res.nOffscreenText = offscreen.size;

  // paragraphs: line length and font size
  const paras = [];
  for (const p of body.querySelectorAll('p')) {
    const tc = (p.textContent || '').replace(/\s+/g, ' ').trim();
    if (tc.length < 120 || !vis(p)) continue;
    range.selectNodeContents(p);
    const rs = [...range.getClientRects()].filter(r => r.width > 1 && r.height > 1);
    if (!rs.length) continue;
    const tops = [];
    for (const r of rs) { const mid = (r.top + r.bottom) / 2; if (!tops.some(x => Math.abs(x - mid) < r.height / 2)) tops.push(mid); }
    const lines = tops.length;
    const s = cs(p);
    const probe = document.createElement('span');
    probe.style.cssText = 'display:inline-block;width:1ch;height:0;padding:0;margin:0;border:0;';
    p.appendChild(probe);
    const ch = probe.getBoundingClientRect().width || 8;
    probe.remove();
    const cw = p.clientWidth - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight);
    const widest = Math.max(...rs.map(r => r.right)) - Math.min(...rs.map(r => r.left));
    paras.push({sel: sel(p), fs: parseFloat(s.fontSize), lines, cpl: lines >= 3 ? Math.round(tc.length / (lines - 0.5)) : null,
      widthCh: Math.round(Math.min(widest, cw) / ch), wpx: Math.round(widest)});
    if (paras.length >= 80) break;
  }
  const fsz = paras.map(p => p.fs).sort((a, b) => a - b);
  res.paraN = paras.length;
  res.paraFsMedian = fsz.length ? fsz[Math.floor(fsz.length / 2)] : null;
  res.paraFsMin = fsz.length ? fsz[0] : null;
  const cpl = paras.filter(p => p.cpl);
  res.cplMax = cpl.length ? Math.max(...cpl.map(p => p.cpl)) : null;
  res.cplMin = cpl.length ? Math.min(...cpl.map(p => p.cpl)) : null;
  res.widthChMax = paras.length ? Math.max(...paras.map(p => p.widthCh)) : null;
  res.longLines = paras.filter(p => (p.cpl && p.cpl > 120) || p.widthCh > 120).sort((a, b) => (b.cpl || 0) - (a.cpl || 0)).slice(0, 5);
  res.nLongLines = paras.filter(p => (p.cpl && p.cpl > 120) || p.widthCh > 120).length;
  res.shortLines = paras.filter(p => p.cpl && p.cpl < 20).slice(0, 5);
  res.nShortLines = paras.filter(p => p.cpl && p.cpl < 20).length;
  const main = document.querySelector('main') || body;
  res.mainW = Math.round(main.getBoundingClientRect().width);

  // fixed / sticky at load (scroll 0)
  scrollTo(0);
  res.fixed0 = fixedCover();

  // interactive: covered at load, then a synchronous scroll scan
  res.nInter = inter.length;
  const st = inter.map(() => ({t: 0, ok: 0, cov: []}));
  const covered0 = [];
  inter.forEach((el, i) => {
    const h = hitTest(el);
    if (!h) return;
    st[i].t++;
    if (h.ok) st[i].ok++;
    else { st[i].cov.push(h); covered0.push({sel: sel(el), text: txt(el).slice(0, 40), ...h}); }
  });
  res.covered0 = covered0.slice(0, 15);
  res.nCovered0 = covered0.length;
  const maxScroll = Math.max(0, de.scrollHeight - vh);
  const step = Math.max(80, Math.round(vh * 0.55));
  let npos = 0;
  for (let y = step; y <= maxScroll + step - 1 && npos < 120; y += step, npos++) {
    scrollTo(Math.min(y, maxScroll));
    inter.forEach((el, i) => {
      const h = hitTest(el);
      if (!h) return;
      st[i].t++;
      if (h.ok) st[i].ok++;
      else if (st[i].cov.length < 2) st[i].cov.push({...h, scrollY: Math.round(scrollY)});
    });
  }
  scrollTo(0);
  res.scanPositions = npos + 1;
  res.nTested = st.filter(s => s.t > 0).length;
  res.candidates = st.map((s, i) => ({i, ...s})).filter(s => s.t > 0 && s.ok === 0)
    .map(s => ({i: s.i, sel: sel(inter[s.i]), text: txt(inter[s.i]).slice(0, 40), t: s.t, cov: s.cov}));
  res.neverOnScreen = st.map((s, i) => ({i, ...s})).filter(s => s.t === 0).slice(0, 5).map(s => sel(inter[s.i]));
  res.nNeverOnScreen = st.filter(s => s.t === 0).length;
  return res;
}
