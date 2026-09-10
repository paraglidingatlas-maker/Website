/* Mandated check 3 for the sitemap.
   Stub the DOM, actually run the graph script, and assert that it does not
   throw and that no x attribute inside a translated node group exceeds 200.
   The node group is already translated to the node's position, so anything
   inside it is RELATIVE. An absolute coordinate leaking in applies the offset
   twice and flings the label off screen; it shows up as a large x.

   Usage: node tools/check_sitemap_render.js
   Exits non-zero on failure so it can gate a push. */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'sitemap.html'), 'utf8');
const js = fs.readFileSync(path.join(ROOT, 'sitemap-graph.js'), 'utf8');

/* pull the graph data out of the generated page */
const m = html.match(/window\.SITEMAP_GRAPH\s*=\s*(\{[\s\S]*?\});/);
if (!m) { console.error('FAIL: could not find window.SITEMAP_GRAPH in sitemap.html'); process.exit(1); }
const GRAPH = JSON.parse(m[1]);

let created = 0;
function makeEl(tag) {
  created++;
  const e = {
    tagName: tag,
    attrs: Object.create(null),
    children: [],
    parent: null,
    textContent: '',
    style: {},
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    setAttribute(k, v) { this.attrs[k] = v; },
    getAttribute(k) { return this.attrs[k]; },
    removeAttribute(k) { delete this.attrs[k]; },
    hasAttribute(k) { return k in this.attrs; },
    appendChild(c) { c.parent = this; this.children.push(c); return c; },
    removeChild(c) { const i = this.children.indexOf(c); if (i >= 0) this.children.splice(i, 1); return c; },
    insertBefore(c) { return this.appendChild(c); },
    listeners: Object.create(null),
    addEventListener(type, fn) { (this.listeners[type] = this.listeners[type] || []).push(fn); },
    removeEventListener() {},
    fire(type, ev) { (this.listeners[type] || []).forEach((f) => f(ev || {})); },
    setPointerCapture() {},
    releasePointerCapture() {},
    getBoundingClientRect() { return { x: 0, y: 0, width: 1180, height: 660, top: 0, left: 0, right: 1180, bottom: 660 }; },
    href: '',
    innerHTML: '',
    querySelector(sel) {
      const tag = String(sel).replace(/^[.#]/, '');
      let found = null;
      const scan = (e) => {
        if (found) return;
        e.children.forEach((c) => {
          if (found) return;
          if (c.tagName === tag || c.attrs.class === tag || c.attrs.id === tag) { found = c; return; }
          scan(c);
        });
      };
      scan(this);
      return found;
    },
    querySelectorAll() { return []; },
    focus() {},
    get firstChild() { return this.children[0] || null; },
    get lastChild() { return this.children[this.children.length - 1] || null; },
  };
  return e;
}

const svg = makeEl('svg');
/* sm-info is the description bar under the graph. The click handler writes the
   node's name and the "Open this page" link into it, so it must exist or every
   click throws. */
const info = makeEl('div');
info.appendChild(makeEl('a'));
const byId = {
  'sm-svg': svg,
  'sm-info': info,
  'sm-in': makeEl('button'),
  'sm-out': makeEl('button'),
  'sm-reset': makeEl('button'),
};

const document = {
  createElementNS: (ns, tag) => makeEl(tag),
  createElement: (tag) => makeEl(tag),
  getElementById: (id) => byId[id] || null,
  querySelector: () => null,
  querySelectorAll: () => [],
  addEventListener() {},
  body: makeEl('body'),
  documentElement: makeEl('html'),
};

const sandbox = {
  window: null,
  document,
  console,
  SITEMAP_GRAPH: GRAPH,
  requestAnimationFrame: (fn) => { setTimeout(() => fn(Date.now()), 0); return 1; },
  cancelAnimationFrame: () => {},
  setTimeout, clearTimeout, setInterval, clearInterval,
  Math, Date, JSON, parseInt, parseFloat, isNaN, String, Number, Array, Object,
  performance: { now: () => Date.now() },
};
sandbox.window = sandbox;
sandbox.window.SITEMAP_GRAPH = GRAPH;
sandbox.window.matchMedia = () => ({ matches: false, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} });
sandbox.window.addEventListener = () => {};
sandbox.window.getComputedStyle = () => ({ getPropertyValue: () => '' });
/* leaf nodes navigate rather than expand, so these must exist or the click throws */
let navigations = 0;
sandbox.window.location = { get href() { return ''; }, set href(v) { navigations++; } };
sandbox.window.open = () => { navigations++; return null; };
sandbox.window.innerWidth = 1180;
sandbox.window.innerHeight = 660;
sandbox.globalThis = sandbox;

/* Episode labels only draw when their branch is the focused one, so an expanded
   render with focus on home still never lays out a long episode title. Find the
   series holding the longest label and focus that, which is the real case the
   longer RSS titles change. */
function longestEpisodeParent() {
  let worstNode = null;
  GRAPH.nodes.forEach((n) => {
    if (n.kind === 'episode' && (!worstNode || n.label.length > worstNode.label.length)) worstNode = n;
  });
  const link = GRAPH.links.find((l) => l.t === worstNode.id);
  return { parent: link ? link.s : null, node: worstNode };
}

function render(expandAll, focusId) {
  const data = JSON.parse(JSON.stringify(GRAPH));
  /* The script sets n.open = n.depth < 1 at init, so the opening state only
     draws the four nav nodes and the long episode labels never render. For the
     second pass force that one initialiser open so every label is actually
     drawn. Layout and draw are untouched; only the starting fold state differs. */
  let source = js;
  if (expandAll) {
    const before = source;
    source = source.replace('n.open = n.depth < 1;', 'n.open = true;');
    if (source === before) {
      console.error('FAIL: could not force the expanded state, the initialiser moved. Fix this harness.');
      process.exit(1);
    }
  }
  if (focusId) {
    const before = source;
    source = source.replace('var focus = "home";', 'var focus = ' + JSON.stringify(focusId) + ';');
    if (source === before) {
      console.error('FAIL: could not force focus, the declaration moved. Fix this harness.');
      process.exit(1);
    }
  }
  const root = makeEl('svg');
  byId['sm-svg'] = root;
  sandbox.window.SITEMAP_GRAPH = data;
  sandbox.SITEMAP_GRAPH = data;
  let err = null;
  try { vm.runInContext(source, sandbox, { filename: 'sitemap-graph.js' }); }
  catch (e) { err = e; }
  return { root, err };
}

vm.createContext(sandbox);
const collapsed = render(false);
const expanded = render(true);
const LP = longestEpisodeParent();
const focused = render(true, LP.parent);
let threw = collapsed.err || expanded.err || focused.err;
const svgCollapsed = collapsed.root;
svg.children = expanded.root.children;

if (threw) {
  console.error('FAIL: the graph script threw while rendering');
  console.error('   ' + threw.message);
  process.exit(1);
}

/* walk everything the script built and find the translated node groups */
function walk(el, out) {
  out.push(el);
  el.children.forEach((c) => walk(c, out));
  return out;
}
const all = walk(svg, []);
/* Only the PER NODE groups. The outer pan/zoom group is also a translate, but
   it carries a scale() too and everything inside it is legitimately absolute,
   so matching it here would flag the whole graph. Node groups are a bare
   translate(x,y) with no scale. */
const groups = all.filter((e) => typeof e.attrs.transform === 'string'
  && /^translate\([^)]*\)\s*$/.test(e.attrs.transform));

let worst = 0, offenders = [];
groups.forEach((g) => {
  walk(g, []).forEach((e) => {
    ['x', 'x1', 'x2', 'cx'].forEach((k) => {
      const v = parseFloat(e.attrs[k]);
      if (!isNaN(v)) {
        if (Math.abs(v) > worst) worst = Math.abs(v);
        if (Math.abs(v) > 200) offenders.push({ tag: e.tagName, attr: k, val: v });
      }
    });
  });
});

function nodeGroups(rootEl) {
  return walk(rootEl, []).filter((e) => typeof e.attrs.transform === 'string'
    && /^translate\([^)]*\)\s*$/.test(e.attrs.transform));
}
let maxLines = 0, longest = '';
nodeGroups(svg).forEach((g) => {
  walk(g, []).forEach((e) => {
    if (e.tagName === 'text') {
      const spans = e.children.filter((c) => c.tagName === 'tspan');
      if (spans.length > maxLines) { maxLines = spans.length; longest = spans.map((x) => x.textContent).join(' '); }
    }
  });
});

console.log('elements created      : ' + created);
console.log('node groups, collapsed: ' + nodeGroups(svgCollapsed).length);
console.log('node groups, expanded : ' + nodeGroups(svg).length);
console.log('most label lines drawn: ' + maxLines);
console.log('longest label         : ' + longest.slice(0, 70) + (longest.length > 70 ? '...' : ''));

/* the focused pass: this is where multi line episode labels actually render */
let fLines = 0, fLabel = '', fMaxX = 0, fOffenders = [];
nodeGroups(focused.root).forEach((g) => {
  walk(g, []).forEach((e) => {
    if (e.tagName === 'text') {
      const spans = e.children.filter((c) => c.tagName === 'tspan');
      if (spans.length > fLines) { fLines = spans.length; fLabel = spans.map((x) => x.textContent).join(' '); }
    }
    ['x', 'x1', 'x2', 'cx'].forEach((k) => {
      const v = parseFloat(e.attrs[k]);
      if (!isNaN(v)) {
        if (Math.abs(v) > fMaxX) fMaxX = Math.abs(v);
        if (Math.abs(v) > 200) fOffenders.push({ tag: e.tagName, attr: k, val: v });
      }
    });
  });
});
console.log('--- focused on "' + LP.parent + '" ---');
console.log('most label lines drawn: ' + fLines);
console.log('longest rendered label: ' + fLabel.slice(0, 70) + (fLabel.length > 70 ? '...' : ''));
console.log('largest |x| inside one: ' + fMaxX.toFixed(1) + '  (limit 200)');
if (fOffenders.length) {
  console.error('FAIL: absolute coordinates inside a node group in the focused render');
  fOffenders.slice(0, 8).forEach((o) => console.error(`   <${o.tag} ${o.attr}="${o.val}">`));
  process.exit(1);
}
if (fLines < 2) {
  console.error('FAIL: no multi line episode label rendered, so the long titles were never exercised');
  process.exit(1);
}
console.log('translated node groups: ' + groups.length);
console.log('largest |x| inside one: ' + worst.toFixed(1) + '  (limit 200)');

if (nodeGroups(svg).length <= 10) {
  console.error('FAIL: the expanded render produced only ' + nodeGroups(svg).length + ' node groups, so the episode labels were never exercised');
  process.exit(1);
}
if (groups.length === 0) {
  console.error('FAIL: draw() ran but produced no translated node groups, so this check proved nothing');
  process.exit(1);
}
if (offenders.length) {
  console.error('FAIL: absolute coordinates leaked inside a translated node group');
  offenders.slice(0, 10).forEach((o) => console.error(`   <${o.tag} ${o.attr}="${o.val}">`));
  process.exit(1);
}

