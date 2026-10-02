#!/usr/bin/env node
/*
 * Writes tools/data/episode-extras.json, which generate_chapter_deck.py reads:
 *
 *   glyphs  the library's own drawing for each series (library.js GLYPH), for
 *           the series emblem in the episode header;
 *   globes  for every episode with a place on the homepage globe, the small
 *           glass globe for the "On The Map" box, as finished inline SVG.
 *
 * WHY NODE, AND WHY A FILE. The globe is drawn once, when the page is built,
 * so the page carries no script for it: about 22 KB of SVG per episode. The
 * projection and the clipping to the visible hemisphere are d3-geo's, the same
 * code the homepage globe runs, loaded from the copy the site already hosts
 * (assets/js/d3.min.js). The result is committed, so building the pages needs
 * only Python; build.sh reruns this when node is available, and the output is
 * deterministic, so a rerun changes nothing unless the inputs did.
 *
 * THE VIEW. Centred on the point 62% of the way along the great circle from
 * Oslo to the episode, which keeps both ends on the visible side with the
 * episode nearer the middle. That is how the approved prototype framed it
 * (Oslo to Antoine Girard's 8000ers matched to a tenth of a pixel). Oslo studio
 * episodes are centred on Oslo and draw no route. The ring is the homepage
 * globe's compass ring at its phone size, with the index turned to the bearing.
 *
 *     node tools/episode_globes.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const d3 = require(path.join(ROOT, 'assets/js/d3.min.js'));
const read = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');
const after = (src, marker) => JSON.parse(src.slice(src.indexOf(marker) + marker.length).trim().replace(/;\s*$/, ''));

const WORLD = after(read('assets/js/globe-world.js'), 'window.GLOBE_WORLD =');
const EP = after(read('globe-episodes.js'), 'window.GLOBE_EP =');

/* ---- The series drawings, evaluated straight out of library.js. ---- */
function glyphs() {
  const src = read('library.js');
  const a = src.indexOf('function ring(');
  const b = src.indexOf('var GLYPH = {');
  const c = src.indexOf('\n  };', b);
  if (a < 0 || b < 0 || c < 0) throw new Error('library.js: GLYPH block not found');
  const code = src.slice(a, b) + src.slice(b, c + 5) + '\nreturn GLYPH;';
  return new Function(code)();
}

/* ---- One small globe. ---- */
const OSLO = [10.7522, 59.9139];
const C = 132, R = 92, VIEW = 264;
/* Every 30 degrees: at this size a 10 degree net is a grey wash. */
const GRAT = d3.geoGraticule().step([30, 30])();
const f1 = (v) => v.toFixed(1);

function stops(list) {
  return list.map((s) => '<stop offset="' + s[0] + '" style="stop-color:var(--' + s[1] + ');stop-opacity:' + s[2] + '"/>').join('');
}
const DEFS =
  '<defs>' +
  '<radialGradient id="mgShade" cx="0.36" cy="0.33" r="0.72">' + stops([[0, 'bg', 0], [0.48, 'bg', 0], [0.78, 'bg', 0.46], [1, 'bg', 0.84]]) + '</radialGradient>' +
  '<radialGradient id="mgHi" cx="0.33" cy="0.3" r="0.44">' + stops([[0, 'gray-light', 0.13], [1, 'gray-light', 0]]) + '</radialGradient>' +
  '<radialGradient id="mgLimb" cx="0.5" cy="0.5" r="0.5">' + stops([[0.7, 'bg', 0], [0.9, 'bg', 0.3], [1, 'bg', 0.72]]) + '</radialGradient>' +
  '<linearGradient id="mgRim" x1="0.15" y1="0.15" x2="0.85" y2="0.85">' + stops([[0, 'white', 0.9], [0.2, 'orange', 0.9], [0.55, 'orange', 0.22], [1, 'gray-light', 0.05]]) + '</linearGradient>' +
  '<clipPath id="mgClip"><circle cx="' + C + '" cy="' + C + '" r="' + R + '"/></clipPath>' +
  '</defs>';

function ring() {
  const r0 = R * 1.15, lenMin = 3, lenMed = 5, lenMaj = 7;
  const pt = (r, deg) => { const a = (deg - 90) * Math.PI / 180; return [C + r * Math.cos(a), C + r * Math.sin(a)]; };
  const tick = (r1, deg) => { const p = pt(r0, deg), q = pt(r1, deg); return 'M' + f1(p[0]) + ',' + f1(p[1]) + 'L' + f1(q[0]) + ',' + f1(q[1]); };
  let mi = '', me = '', ma = '';
  for (let a = 0; a < 360; a += 5) {
    if (a % 30 === 0) ma += tick(r0 + lenMaj, a);
    else if (a % 10 === 0) me += tick(r0 + lenMed, a);
    else mi += tick(r0 + lenMin, a);
  }
  return '<circle cx="' + C + '" cy="' + C + '" r="' + f1(r0) + '" fill="none" stroke="var(--line)"/>' +
    '<path d="' + mi + '" stroke="var(--edge)" fill="none"/>' +
    '<path d="' + me + '" stroke="var(--edge-hi)" fill="none"/>' +
    '<path d="' + ma + '" stroke="var(--gray-light)" fill="none"/>' +
    '<text class="mg-n" x="' + C + '" y="' + f1(C - r0 - lenMaj - 9) + '">N</text>';
}

/* The prototype's globe weighed about 22 KB. At 92px across, the 1:110m
   coastline has several points to every pixel, so each path is thinned on
   screen: a point closer than 3px to the last one kept is dropped (the first
   and last of every ring always stay), which is the prototype's own density. */
function thin(d, eps) {
  if (!d) return '';
  const out = [];
  d.replace(/M[^M]*/g, (sub) => {
    const closed = /Z\s*$/.test(sub);
    const pts = sub.replace(/[MZ]/g, ' ').trim().split('L').map((q) => q.split(',').map(Number));
    const keep = [pts[0]];
    for (let i = 1; i < pts.length - 1; i++) {
      const l = keep[keep.length - 1];
      if (Math.hypot(pts[i][0] - l[0], pts[i][1] - l[1]) >= eps) keep.push(pts[i]);
    }
    if (pts.length > 1) keep.push(pts[pts.length - 1]);
    if (closed && keep.length < 4) return '';
    if (!closed && keep.length < 2) return '';
    out.push('M' + keep.map((q) => q[0] + ',' + q[1]).join('L') + (closed ? 'Z' : ''));
    return '';
  });
  return out.join('');
}

function coord(x) {
  return Math.abs(x.lat).toFixed(4) + '°' + (x.lat >= 0 ? 'N' : 'S') + ' ' +
         Math.abs(x.lon).toFixed(4) + '°' + (x.lon >= 0 ? 'E' : 'W');
}

function globe(x) {
  const dest = [x.lon, x.lat];
  const centre = x.home ? OSLO : d3.geoInterpolate(OSLO, dest)(0.62);
  const rot = [-centre[0], -centre[1], 0];
  const proj = d3.geoOrthographic().scale(R).translate([C, C]).clipAngle(90).rotate(rot);
  const back = d3.geoOrthographic().scale(R).translate([C, C]).clipAngle(90).reflectX(true)
    .rotate([rot[0] + 180, -rot[1], 0]);
  proj.precision(2); back.precision(2);
  const gp = d3.geoPath(proj).digits(1), gb = d3.geoPath(back).digits(1);
  const p = (o) => thin(gp(o), 3), pb = (o) => thin(gb(o), 3);
  const land = p(WORLD.land);
  const pin = proj(dest);
  const label = x.home
    ? 'Globe showing the Oslo studio, ' + coord(x)
    : 'Globe showing the route from Oslo to ' + coord(x);

  let s = '<svg class="cd-globe" viewBox="0 0 ' + VIEW + ' ' + VIEW + '" role="img" aria-label="' + label + '">' + DEFS +
    '<circle cx="' + C + '" cy="' + C + '" r="' + R + '" fill="var(--card)"/>' +
    '<circle cx="' + C + '" cy="' + C + '" r="' + R + '" fill="var(--bg)" opacity="0.5"/>' +
    '<g clip-path="url(#mgClip)">' +
    '<path d="' + pb(WORLD.land) + '" fill="var(--gray-light)" opacity="0.07"/>' +
    '<path d="' + p(GRAT) + '" fill="none" stroke="var(--gray-light)" stroke-opacity="0.1"/>' +
    '<path d="' + land + '" fill="var(--gray-light)" fill-opacity="0.13"/>' +
    '<path d="' + p(WORLD.borders) + '" fill="none" stroke="var(--gray-light)" stroke-opacity="0.17" stroke-width="0.5"/>' +
    '<path d="' + land + '" fill="none" stroke="var(--gray-light)" stroke-opacity="0.78" stroke-width="0.8" stroke-linejoin="round"/>' +
    '</g>' +
    '<circle cx="' + C + '" cy="' + C + '" r="' + R + '" fill="url(#mgHi)"/>' +
    '<circle cx="' + C + '" cy="' + C + '" r="' + R + '" fill="url(#mgShade)"/>' +
    '<circle cx="' + C + '" cy="' + C + '" r="' + R + '" fill="url(#mgLimb)"/>';
  if (!x.home) {
    const o = proj(OSLO);
    s += '<path class="mg-route" d="' + gp({ type: 'LineString', coordinates: [OSLO, dest] }) +
      '" pathLength="1" fill="none" stroke="var(--orange)" stroke-width="1.4" stroke-linecap="round"/>' +
      '<circle cx="' + f1(o[0]) + '" cy="' + f1(o[1]) + '" r="3.2" fill="var(--bg)" stroke="var(--white)" stroke-width="1.2"/>';
  }
  s += '<g class="mg-pin">' +
    '<circle class="mg-pulse" cx="' + f1(pin[0]) + '" cy="' + f1(pin[1]) + '" r="9" fill="none" stroke="var(--orange)" stroke-width="1.1"/>' +
    '<circle cx="' + f1(pin[0]) + '" cy="' + f1(pin[1]) + '" r="3.4" fill="var(--orange)" stroke="var(--bg)" stroke-width="1"/>' +
    '</g>' +
    '<circle cx="' + C + '" cy="' + C + '" r="' + R + '" fill="none" stroke="url(#mgRim)" stroke-width="1.4"/>' +
    ring();
  if (!x.home) {
    const r0 = R * 1.15;
    s += '<path class="mg-index" style="--brg:' + x.brg + 'deg" d="M' + C + ',' + f1(C - (r0 - 11)) + 'L' + (C - 4.5) + ',' +
      f1(C - (r0 - 3)) + 'L' + (C + 4.5) + ',' + f1(C - (r0 - 3)) + 'Z" fill="var(--orange)"/>';
  }
  return s + '</svg>';
}

const out = { glyphs: glyphs(), globes: {} };
Object.keys(EP).sort().forEach((slug) => {
  const x = EP[slug];
  if (typeof x.lat !== 'number' || typeof x.lon !== 'number') return;
  out.globes[slug] = { svg: globe(x), co: coord(x), home: !!x.home, km: x.km, brg: x.brg, card: x.card };
});
const dest = path.join(ROOT, 'tools/data/episode-extras.json');
fs.writeFileSync(dest, JSON.stringify(out, null, 1) + '\n');
console.log('episode extras: %d series drawings, %d globes', Object.keys(out.glyphs).length, Object.keys(out.globes).length);
