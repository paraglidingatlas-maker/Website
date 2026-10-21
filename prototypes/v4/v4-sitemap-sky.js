/* v4-sitemap-sky.js: written by tools/v4_sitemap_sky.py from the live sitemap-sky.js, with its random
   background field replaced by the real sky, in depth, zooming slowly and moving with the camera and the
   pointer. Do not edit; change sitemap-sky.js or the tool and run it.
   Star positions and magnitudes: d3-celestial 0.7.35 (npm), data/stars.6.json; star data XHIP: An Extended Hipparcos Compilation, Anderson E., Francis C. (2012), VizieR V/137D, converted by Olaf Frohn. Copyright (c) 2015, Olaf Frohn. All rights reserved. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. */
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
    if (!ground.querySelector('.sky-g')) ground.innerHTML = h + '</div>';
  })();

  /* ---- Camera ---- */
  var cam = { x: W / 2, y: H / 2, k: 0.5 }, camT = { x: W / 2, y: H / 2, k: 0.5 }, camS = {};
  var vw = 0, vh = 0, dpr = 1, bg = [], raf = 0, t0 = 0, shoot = null, shootT = 0, ambient = 0;

  /* v4: the background is the real sky (tools/v4_sitemap_sky.py; the data's credit is at the head of this
     file). REAL is [x, y, magnitude] in stereographic units about RA 95, Dec -25, looking up; the field is
     3.5 by 2 units, drawn to cover the view with room to move. Brighter stars are nearer: they move and
     zoom more. */
  var REAL = [[-0.106,-0.143,-1.44],[-0.011,0.493,-0.62],[0.29,-0.283,0.18],[-0.373,-0.528,0.4],[0.672,0.904,0.45],[0.117,-0.58,0.45],[-0.415,-1.0,1.16],[-1.178,-0.592,1.36],[-0.148,0.075,1.5],[0.258,-0.556,1.64],[-0.293,0.915,1.67],[0.2,-0.417,1.69],[0.179,-0.404,1.74],[-0.336,0.444,1.75],[-0.19,0.033,1.83],[-0.294,0.678,1.86],[-0.085,-0.755,1.93],[-0.386,0.614,1.93],[-0.011,-0.123,1.98],[-0.861,-0.178,1.99],[-1.27,-0.789,2.01],[1.552,0.391,2.04],[0.141,-0.266,2.07],[-1.896,-0.56,2.14],[-1.035,1.124,2.2],[-0.353,0.307,2.21],[-0.421,0.737,2.21],[-0.546,0.444,2.23],[0.22,-0.433,2.25],[1.135,0.923,2.4],[-0.245,0.091,2.45],[-0.479,0.67,2.47],[0.973,-0.435,2.54],[-1.644,-0.787,2.56],[0.198,-0.118,2.58],[-0.932,1.014,2.58],[-1.668,0.465,2.58],[0.147,0.165,2.65],[-1.642,0.689,2.65],[-0.769,0.746,2.69],[-0.201,0.225,2.71],[-0.511,0.963,2.74],[0.199,-0.331,2.75],[0.325,-0.337,2.78],[-0.756,1.123,2.79],[0.212,-0.065,2.81],[-0.431,0.031,2.83],[0.557,0.919,2.86],[-0.014,-0.88,2.87],[0.686,0.445,2.88],[-0.318,-0.591,2.89],[-0.409,0.879,2.92],[-0.087,0.458,2.94],[-1.769,0.508,2.94],[-1.063,-0.901,2.97],[0.622,-0.135,2.97],[-1.863,0.954,2.99],[-0.001,0.088,3.02],[-0.172,-0.014,3.02],[-1.539,0.554,3.02],[-0.115,-0.935,3.06],[-0.753,-0.508,3.11],[-1.221,0.133,3.11],[-0.612,1.059,3.11],[0.104,0.192,3.12],[-0.478,0.719,3.16],[-0.058,0.322,3.17],[0.302,-0.026,3.19],[0.428,-0.559,3.19],[-0.064,0.671,3.24],[-0.226,0.342,3.25],[0.21,0.977,3.26],[0.284,-0.139,3.29],[-0.373,0.996,3.29],[0.282,0.581,3.3],[-0.539,0.902,3.3],[0.025,-0.88,3.31],[0.938,0.841,3.32],[0.278,0.735,3.33],[-1.629,-0.628,3.33],[-0.356,0.027,3.34],[-0.12,-0.686,3.35],[0.253,-0.392,3.35],[-0.709,-0.523,3.38],[-0.518,0.868,3.39],[0.213,-0.626,3.39],[0.937,0.716,3.41],[-0.41,0.723,3.43],[-1.252,-0.889,3.43],[-0.269,0.536,3.46],[1.524,0.115,3.46],[1.075,-0.396,3.47],[-1.185,-0.714,3.48],[-0.161,0.058,3.49],[1.257,0.144,3.49],[-0.11,0.135,3.5],[-0.291,-0.868,3.5],[-1.012,-0.563,3.52],[-0.57,0.721,3.52],[0.706,-0.192,3.52],[-0.561,-0.594,3.53],[-1.205,0.587,3.54],[0.448,0.214,3.55],[0.141,-0.175,3.55],[0.677,0.724,3.56],[-1.396,0.186,3.56],[1.86,0.263,3.56],[-0.411,-0.919,3.57],[-0.279,-0.756,3.58],[0.143,-0.04,3.59],[-1.798,-0.148,3.59],[0.279,-0.309,3.59],[-0.388,0.577,3.6],[-0.647,0.428,3.6],[1.455,0.021,3.6],[-1.055,-0.035,3.61],[-0.298,0.257,3.62],[-0.542,1.12,3.63],[-0.532,0.227,3.68],[0.419,-0.533,3.68],[0.727,0.774,3.69],[-0.44,0.834,3.69],[0.752,0.067,3.7],[0.101,-0.188,3.71],[-0.312,0.308,3.71],[0.4,-0.473,3.71],[0.757,-0.187,3.72],[1.275,0.002,3.74],[-0.504,0.504,3.75],[0.104,0.686,3.76],[0.117,-0.069,3.76],[-0.039,-0.316,3.76],[0.187,-0.392,3.77],[-0.248,0.804,3.77],[-0.435,0.465,3.77],[-0.083,0.846,3.78],[-0.627,0.906,3.78],[-0.318,-0.994,3.78],[-0.308,0.055,3.8],[0.733,0.214,3.8],[0.396,0.14,3.81],[-0.579,0.849,3.81],[1.316,-0.329,3.82],[-1.095,0.091,3.83],[0.318,0.809,3.84],[-0.358,0.733,3.84],[-1.32,-0.501,3.84],[-0.762,0.703,3.84],[0.417,0.37,3.85],[0.094,0.467,3.85],[-0.008,0.148,3.85],[-0.776,0.545,3.85],[-1.039,1.103,3.85],[0.175,0.193,3.86],[0.439,-0.154,3.86],[-0.456,0.46,3.87],[1.095,1.041,3.88],[-1.105,-0.96,3.88],[-0.136,-0.01,3.89],[-0.841,-0.418,3.89],[0.94,-0.151,3.89],[-0.962,-0.319,3.9],[-0.76,0.914,3.9],[-0.578,-0.331,3.91],[-0.98,1.083,3.91],[0.657,-0.52,3.91],[1.104,0.943,3.93],[0.831,0.8,3.93],[-0.126,0.901,3.93],[-0.652,0.943,3.93],[0.475,-0.355,3.93],[0.766,0.954,3.94],[-0.359,-0.252,3.94],[-0.322,0.096,3.94],[-0.717,-0.776,3.94],[-0.069,-0.099,3.95],[0.068,0.315,3.96],[-0.375,0.783,3.96],[0.424,0.212,3.97],[-0.107,0.797,3.97],[-0.506,0.261,3.97],[-0.901,1.046,3.97],[0.023,-0.33,3.99],[-0.316,1.068,3.99],[1.121,0.211,3.99],[-0.313,0.844,4.0],[-1.675,-0.468,4.0],[-0.213,-0.839,4.01],[-0.214,0.042,4.01],[0.432,-0.362,4.01],[-0.59,0.137,4.02],[-1.489,0.59,4.02],[-1.81,-0.305,4.04],[0.581,-0.273,4.04],[-0.141,1.006,4.05],[-0.475,0.398,4.05],[-1.624,-0.341,4.05],[-1.387,0.269,4.06],[-0.369,-0.974,4.06],[0.402,0.982,4.08],[-0.148,-0.224,4.08],[-0.46,0.762,4.08],[-1.249,0.206,4.08],[1.083,-0.326,4.08],[0.814,0.13,4.08],[0.204,-0.614,4.09],[-0.278,0.41,4.1],[0.751,0.471,4.11],[-0.185,-0.158,4.11],[-0.451,0.396,4.11],[-0.941,-0.017,4.11],[-0.237,1.141,4.11],[-0.665,1.066,4.11],[0.383,0.95,4.12],[0.083,-0.623,4.12],[0.249,-0.294,4.13],[-0.043,-0.833,4.13],[-0.661,-0.513,4.14],[-0.238,-0.428,4.15],[0.539,0.29,4.17],[-0.392,-0.003,4.2],[0.231,-0.549,4.2],[-0.283,0.444,4.22],[0.625,0.058,4.22],[-0.405,-1.019,4.23],[0.701,0.637,4.24],[0.97,-0.03,4.24],[0.475,1.098,4.25],[-1.29,1.078,4.25],[0.314,-0.271,4.25],[0.588,0.456,4.26],[0.353,0.533,4.26],[-0.782,-0.633,4.26],[1.461,-0.471,4.26],[0.69,0.045,4.26],[1.755,-0.365,4.27],[-0.952,0.374,4.28],[0.261,-0.196,4.29],[-0.653,0.825,4.29],[-1.244,0.701,4.29],[0.776,-0.388,4.29],[0.533,0.317,4.3],[-0.684,-0.463,4.3],[-1.514,-0.925,4.3],[-1.672,-0.112,4.3],[-0.611,1.101,4.3],[-1.789,0.512,4.3],[1.283,0.571,4.3],[1.186,-0.502,4.3],[-0.334,0.701,4.31],[0.414,-0.058,4.32],[-0.642,-0.13,4.32],[-0.98,-0.881,4.32],[-0.636,1.131,4.32],[-0.323,-0.603,4.33],[0.072,0.747,4.34],[-0.047,-0.027,4.34],[-0.138,1.018,4.34],[-0.437,0.705,4.34],[-0.578,0.595,4.34],[-0.042,0.499,4.35],[-0.196,0.837,4.35],[-0.716,-0.51,4.35],[0.426,-0.597,4.35],[0.65,1.142,4.36],[0.761,1.054,4.36],[0.288,-0.197,4.36],[0.081,0.182,4.36],[-0.152,-0.135,4.36],[-0.499,-0.359,4.36],[1.281,-0.496,4.36],[0.393,-0.324,4.36],[0.012,0.177,4.37],[-0.233,0.012,4.37],[-0.92,0.664,4.37],[1.389,1.121,4.38],[0.816,0.694,4.39],[-0.017,-0.528,4.39],[-0.479,-0.464,4.39],[-1.169,-0.544,4.39],[0.214,-0.618,4.39],[-0.348,0.045,4.4],[-0.455,-0.059,4.4],[-0.082,0.514,4.41],[1.586,1.133,4.41],[-0.246,-1.048,4.41],[-0.074,-0.117,4.42],[-0.171,0.358,4.42],[-0.213,0.035,4.42],[-0.387,0.323,4.42],[-1.557,-0.782,4.42],[0.059,-0.723,4.42],[0.682,-0.15,4.43],[0.562,-0.261,4.43],[0.298,0.675,4.44],[0.331,0.337,4.44],[-0.3,-0.027,4.44],[-0.381,0.307,4.44],[-0.421,0.262,4.44],[1.693,0.543,4.44],[1.862,-0.326,4.44],[0.795,0.319,4.45],[0.294,-0.216,4.45],[-0.661,-0.465,4.45],[-0.537,0.393,4.45],[-0.613,0.847,4.45],[-1.508,-0.09,4.45],[1.466,-0.366,4.45],[0.039,-0.712,4.45],[-1.25,0.337,4.46],[-0.933,1.013,4.46],[0.678,-0.335,4.46],[0.311,-0.487,4.46],[-0.03,0.133,4.47],[-0.061,-0.579,4.47],[-0.292,0.469,4.47],[-0.246,0.958,4.47],[-0.94,-0.962,4.47],[-1.014,0.877,4.47],[0.93,0.063,4.47],[0.379,-0.461,4.47],[0.31,0.743,4.48],[-0.129,-0.486,4.48],[-1.12,-0.3,4.48],[0.407,0.128,4.49],[-0.114,-0.692,4.49],[-0.163,0.396,4.49],[-0.32,0.278,4.49],[0.079,0.561,4.5],[-0.374,0.653,4.5],[-0.605,0.792,4.5],[0.19,-0.516,4.5],[-0.682,0.344,4.51],[-0.444,0.805,4.51],[0.65,1.142,4.53],[0.09,-0.387,4.53],[-0.279,0.198,4.53],[-0.06,-0.035,4.54],[-0.92,-0.327,4.54],[0.271,0.206,4.55],[-0.334,-0.663,4.55],[1.789,0.561,4.55],[0.321,0.731,4.56],[0.554,0.38,4.57],[0.201,-0.35,4.58],[-0.652,0.574,4.58],[-0.579,0.909,4.58],[1.013,0.918,4.59],[0.555,0.319,4.59],[-0.898,-0.297,4.59],[-0.617,0.773,4.59],[-0.633,0.971,4.59],[1.602,0.876,4.59],[0.247,-0.495,4.59],[-1.022,-0.03,4.6],[-0.986,0.565,4.6]];
  var WHITE = (getComputedStyle(document.documentElement).getPropertyValue('--white') || '').trim() || '#f6f4f4';
  var skyOn = true, mx = 0, my = 0, mxE = 0, myE = 0, home = null;
  function realSky() {
    var s = Math.max(vw / 3.5, vh / 2) * 1.2, rk = Math.max(0.75, Math.min(1.3, s / 492));
    bg = REAL.map(function (st) {
      var t = Math.max(0, Math.min(1, (st[2] + 1.5) / 6.1));
      return [st[0] * s, st[1] * s, (1.7 - 1.15 * t) * rk, 0.85 - 0.6 * t, 1 - t];
    });
  }
  function sky(now) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, vw, vh);
    ctx.fillStyle = WHITE;
    if (!home) home = { x: cam.x, y: cam.y, k: cam.k };
    var breathe = reduce ? 0 : (1 - Math.cos(now / 1000 * 6.2832 / 160)) / 2;
    var ck = Math.pow(cam.k / home.k, 0.15);
    var px0 = Math.max(-1, Math.min(1, (cam.x - home.x) / 1500)) * -vw * 0.07;
    var py0 = Math.max(-1, Math.min(1, (cam.y - home.y) / 900)) * -vh * 0.07;
    if (!reduce) { mxE += (mx - mxE) * 0.04; myE += (my - myE) * 0.04; }
    var cx = vw / 2, cy = vh / 2;
    for (var i = 0; i < bg.length; i++) {
      var st = bg[i], d = 0.35 + 0.65 * st[4];
      var z = (1 + 0.12 * breathe * (0.4 + d)) * (1 + (ck - 1) * d);
      var x = cx + st[0] * z + (px0 - mxE * 22) * d, y = cy + st[1] * z + (py0 - myE * 14) * d;
      if (x < -4 || x > vw + 4 || y < -4 || y > vh + 4) continue;
      ctx.globalAlpha = st[3];
      ctx.beginPath(); ctx.arc(x, y, st[2], 0, 6.2832); ctx.fill();
    }
  }
  view.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse') return;
    var r = view.getBoundingClientRect();
    mx = (e.clientX - r.left) / r.width * 2 - 1; my = (e.clientY - r.top) / r.height * 2 - 1;
  });
  view.addEventListener('pointerleave', function () { mx = 0; my = 0; });
  if (window.IntersectionObserver) new IntersectionObserver(function (en) { skyOn = en[0].isIntersecting; }).observe(view);
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
    sky(now);
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
    else if (!reduce && skyOn && !document.hidden) sky(now);
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
    realSky();
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
