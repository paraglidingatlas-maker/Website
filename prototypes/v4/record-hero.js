/* The Speed Record hero on record-attempt.html (styles in record-hero.css; data from tools/v4_record_hero_prep.py):
   a widescreen frame opens on the Kerio photograph, which moves in depth as the visitor scrolls; the push into his seat;
   then his logged run of 6 Feb 2025 over the escarpment, drawn from open terrain heights alone, with record pace
   (36.22 km/h) as a second light. Nothing moves unless the visitor scrolls. window.__snap (still frames only)
   makes the scroll's spring and the camera land at once. */
const CHUNKS = [[2,0],[3,0],[2,1],[3,1],[1,2],[2,2],[3,2],[1,3],[2,3],[3,3],[1,4],[2,4],[3,4],[1,5],[2,5],[3,5],[1,6],[2,6],[3,6],[0,7],[1,7],[2,7],[3,7],[0,8],[1,8],[2,8],[0,9],[1,9],[2,9],[0,10],[1,10],[2,10],[0,11],[1,11],[2,11],[0,12],[1,12],[2,12],[3,12],[1,13],[2,13],[3,13],[1,14],[2,14],[3,14],[1,15],[2,15],[3,15]];            // [i, j] of each 7.3 km terrain square along the escarpment
const FAR = {"x0":-19567.88,"z0":-12229.92,"w":88055.46,"h":146759.09};                  // the whole valley, coarse: world box in metres
const RIG = {"lines":[[[82.2,843.4],[480.5,1047.9]],[[120.1,775.9],[480.5,1047.9]],[[153.2,706.0],[480.5,1047.9]],[[480.5,1047.9],[1071,1493]],[[189.3,637.7],[552.6,924.9]],[[231.4,573.5],[552.6,924.9]],[[284.0,519.0],[552.6,924.9]],[[552.6,924.9],[1071,1493]],[[337.1,463.9],[651.2,823.3]],[[392.3,410.7],[651.2,823.3]],[[452.6,363.7],[651.2,823.3]],[[651.2,823.3],[1071,1493]],[[515.7,321.1],[769.3,746.0]],[[584.7,287.7],[769.3,746.0]],[[653.0,255.5],[769.3,746.0]],[[769.3,746.0],[1071,1493]],[[723.8,227.1],[899.1,688.8]],[[793.9,197.1],[899.1,688.8]],[[863.4,163.3],[899.1,688.8]],[[899.1,688.8],[1071,1493]],[[936.1,141.0],[1100.9,640.6]],[[1011.6,131.0],[1100.9,640.6]],[[1088.0,125.0],[1100.9,640.6]],[[1100.9,640.6],[1246,1470]],[[1164.2,123.0],[1242.7,636.1]],[[1241.2,123.4],[1242.7,636.1]],[[1316.9,128.4],[1242.7,636.1]],[[1242.7,636.1],[1246,1470]],[[1391.4,142.7],[1381.1,660.9]],[[1464.8,161.4],[1381.1,660.9]],[[1535.5,190.7],[1381.1,660.9]],[[1381.1,660.9],[1246,1470]],[[1605.9,219.0],[1511.0,716.3]],[[1674.7,252.4],[1511.0,716.3]],[[1739.6,291.8],[1511.0,716.3]],[[1511.0,716.3],[1246,1470]],[[1799.3,338.3],[1623.4,800.3]],[[1853.9,389.9],[1623.4,800.3]],[[1910.8,441.2],[1623.4,800.3]],[[1623.4,800.3],[1246,1470]],[[75.6,851.2],[690.6,1097.1]],[[151.7,707.7],[690.6,1097.1]],[[233.6,569.0],[690.6,1097.1]],[[345.7,453.3],[690.6,1097.1]],[[469.0,350.0],[690.6,1097.1]],[[690.6,1097.1],[1126,1606]],[[1371.8,136.9],[1462.6,918.2]],[[1524.4,183.2],[1462.6,918.2]],[[1671.0,248.5],[1462.6,918.2]],[[1802.4,338.6],[1462.6,918.2]],[[1916.7,449.7],[1462.6,918.2]],[[1462.6,918.2],[1268,1563]]],"risers":[[[1071,1493],[1127,1596]],[[1246,1470],[1229,1597]]]};                // the wing's lines and risers, in the photograph's pixels
const MPP = 9.554628535747527, CN = 768, CS = CN * MPP;
const DARK = true;                // B: the dark contour relief in place of the satellite colour

const $ = id => document.getElementById('srh-' + id);
/* files: on the live site the page sits at the root and v4's files under /assets/v4/, which the switch-over
   cannot rewrite inside a script; three.js is imported relative to this file */
const BASE = (/^(.*\/prototypes\/v\d+\/)/.exec(location.pathname) || [0, '/assets/v4/'])[1], HERO = BASE + 'img/record/hero/';
const LIVE = document.documentElement.classList.contains('wr-pin');     // set by the page when it may move: otherwise the still frames
{                                       // fine film grain over the opening: one tile of noise, moved only with the scroll
  const c = document.createElement('canvas'); c.width = c.height = 200; const x = c.getContext('2d'), d = x.createImageData(200, 200);
  let sd = 7; for (let i = 0; i < d.data.length; i += 4) { sd = (sd * 16807) % 2147483647; const v = 128 + ((sd / 2147483647) - .5) * 190; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
  x.putImageData(d, 0, 0); addEventListener('DOMContentLoaded', () => { $('grain').style.backgroundImage = `url(${c.toDataURL()})`; });
}
/* the title: SPEED RECORD solid white and sharp; WORLD and ATTEMPT recede, and change as the frame opens: frosted glass in
   the slit, then soft and dim as the lens pulls focus past them (the wing and its lines in front), then settling into the
   escarpment itself, warm inside the letters. Bound to the scroll, every step blended, so it runs the same both ways. */
let TIMG = null, TPOS = null;
function titleSetup() {
  if (titleSetup.done) return; titleSetup.done = true;
  $('wa').classList.add('srh-rec'); $('wd').classList.add('srh-rec');
  TIMG = new Image(); TIMG.onload = kick; TIMG.src = HERO + 'plate.jpg';
}
function drawTitle(M, bright) {
  const cv = $('tcv'), r = Math.min(devicePixelRatio || 1, 2), w = Math.round(W * r), h = Math.round(H * r);
  if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
  const c = cv.getContext('2d'); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, w, h);
  if (!TPOS || !TIMG || !TIMG.complete || TPOS.exitK >= 1) return;
  const { fs, ls, pos, exitK, eO } = TPOS, fade = 1 - exitK;
  const wa = 1 - ss(seg(eO, .3, .5)), wc = ss(seg(eO, .62, .85)), wb = Math.max(0, 1 - wa - wc);
  // each look comes in over the last, which stays at full strength until it is covered: the letters never thin out on the way
  const ka = Math.min(1, 2 * wa), kb = Math.min(1, 2 * wb), kc = Math.min(1, 2 * wc);
  const font = `700 ${fs}px Poppins`, spc = (ls * fs) + 'px';
  const words = [['wa', 'WORLD', -1], ['wd', 'ATTEMPT', 1]].map(([id, t, side]) => ({ t, x: pos[id][0] + side * exitK * W * .6, y: pos[id][1] + fs * .78 }));
  const text = (cx, stroke) => { cx.font = font; try { cx.letterSpacing = spc; } catch (e) {} cx.textBaseline = 'alphabetic'; for (const q of words) stroke ? cx.strokeText(q.t, q.x, q.y) : cx.fillText(q.t, q.x, q.y); };
  const buf = id => {
    const b = drawTitle[id] || (drawTitle[id] = document.createElement('canvas')); if (b.width !== w || b.height !== h) { b.width = w; b.height = h; }
    const x = b.getContext('2d'); x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = 'source-over'; x.filter = 'none'; x.clearRect(0, 0, w, h); x.setTransform(r, 0, 0, r, 0, 0); return [b, x];
  };
  // both words in one mask (cutting with each in turn would leave only where they overlap)
  const [mk, mc] = buf('mk'); mc.fillStyle = '#000'; text(mc);
  const fill = paint => { const [b, x] = buf('off'); paint(x); x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = 'destination-in'; x.drawImage(mk, 0, 0); return b; };
  c.setTransform(r, 0, 0, r, 0, 0);
  // a soft shadow under the letters, so they hold on sky and on rock
  c.save(); c.globalAlpha = fade * (.35 + .65 * (wa + wc)); c.shadowColor = 'rgba(6,8,12,.45)'; c.shadowBlur = 22; c.shadowOffsetY = 4; c.fillStyle = 'rgba(6,8,12,.3)'; text(c); c.restore();
  if (wa > .003) {        // a: frosted glass, the photograph behind seen blurred and lifted, a light edge
    const lift = .1 + .25 * (1 - bright);
    const b = fill(x => {
      x.filter = `blur(10px) brightness(${(1.12 * bright).toFixed(3)}) saturate(.8)`; x.drawImage(TIMG, L.tx, L.ty, 1920 * L.s, 1080 * L.s); x.filter = 'none';
      x.fillStyle = `rgba(246,244,244,${lift.toFixed(3)})`; x.fillRect(0, 0, W, H); x.fillStyle = 'rgba(20,21,25,.14)'; x.fillRect(0, 0, W, H);
    });
    c.globalAlpha = fade * ka; c.drawImage(b, 0, 0, W, H); c.lineWidth = 1.1; c.strokeStyle = 'rgba(255,255,255,.5)'; text(c, true);
  }
  if (wb > .003) {        // b: out of focus, dimmer
    c.save(); c.globalAlpha = fade * kb; c.filter = 'blur(1.4px)'; c.fillStyle = 'rgba(232,230,230,.82)'; text(c); c.restore();
  }
  if (wc > .003) {        // c: the escarpment's cliffs, darker and warm, inside the letters, a warm hairline
    c.font = font; try { c.letterSpacing = spc; } catch (e) {}
    const tw = words.map(q => c.measureText(q.t).width);
    const b = fill(x => { x.filter = 'brightness(.7) sepia(.35) saturate(1.35) contrast(1.15)'; words.forEach((q, i) => x.drawImage(TIMG, 260, 560, 900, 260, q.x - 4, q.y - fs * .78, tw[i] + 8, fs * .86)); x.filter = 'none'; });
    c.globalAlpha = fade * kc; c.drawImage(b, 0, 0, W, H); c.lineWidth = 1.1; c.strokeStyle = 'rgba(255,178,112,.9)'; text(c, true);
  }
  c.globalAlpha = 1;
  if (wb > .003 && M) {   // while out of focus they sit behind the wing: its shape is cut out of them
    c.save(); c.globalAlpha = kb * (1 - kc); c.globalCompositeOperation = 'destination-out'; c.setTransform(r * M[0], r * M[1], r * M[2], r * M[3], r * M[4], r * M[5]); c.drawImage($('wing'), 0, 0); c.restore();
  }
}
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, t) => a + (b - a) * t;
const seg = (x, a, b) => clamp((x - a) / (b - a));
const io = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const out = t => 1 - Math.pow(1 - t, 3);
const ss = t => t * t * (3 - 2 * t);
const lerpLog = (a, b, t) => Math.exp(lerp(Math.log(a), Math.log(b), t));

/* ---------- the scroll, in screen heights: about three for the whole hero ---------- */
const A = { open: .8, glide: .4, trans: .4, out: 1.15, turn: .5, ret: .85, hand: .3 };     // 4.4 screen heights in all
const U_OPEN = A.open, U_GLIDE = U_OPEN + A.glide, U_TRANS = U_GLIDE + A.trans, U_ORB = U_TRANS + A.out, U_TURN = U_ORB + A.turn, U_FLY = U_TURN + A.ret, U_END = U_FLY + A.hand;
const hero = document.getElementById('wr-goal'), stage = $('stage');
if (LIVE) hero.style.height = `calc(${(U_END + 1) * 100}vh)`;

/* ---------- the photograph ---------- */
const PW = 1920, PH = 1080;
const CUT = { x: 470, y: 52, k: .5 };        // the yellow wing's cut-out on the Kerio photograph, at half its pixels
const ANCH = { x: 1165, y: 1575 };              // the hang point in the cut-out's pixels
const WING_M = 10.5;

let W = 0, H = 0, dpr = 1, phone = false, L = {};
function layout() {
  W = innerWidth; H = innerHeight; dpr = Math.min(devicePixelRatio || 1, 2);
  // the site's menu sits in the page's flow above the hero: the hero slides up under it, so the curtain fills the first screen
  const nav = document.querySelector('.page-wrap > nav');
  if (nav && !nav.classList.contains('v2-nav-pinned')) hero.style.marginTop = -nav.offsetHeight + 'px';
  phone = W < 720 || W / H < .9;
  for (const c of [$('rig'), $('fx')]) { c.width = Math.round(W * dpr); c.height = Math.round(H * dpr); }
  // the photograph covers the screen; on a phone it is framed on the pilot's line, the wing's tips run off the edges
  const s = Math.max(W / PW, H / PH) * (phone ? 1.0 : 1.0);
  const fx = phone ? CUT.x + 1060 * CUT.k : PW / 2, fy = PH / 2;
  let tx = W / 2 - fx * s, ty = H / 2 - fy * s;
  tx = clamp(tx, W - PW * s, 0); ty = clamp(ty, H - PH * s, 0);
  L = { s, tx, ty };
  // the wordmark: each word's width in em at its final tracking, measured once
  const em = {};
  for (const id of ['wa', 'wb', 'wc', 'wd']) { const el = $(id); el.style.fontSize = '100px'; el.style.letterSpacing = '-.025em'; em[id] = (el.offsetWidth + 2.5) / 100; }
  const g = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gut')) || 24, SP = .3;
  const line = em.wa + em.wb + em.wc + em.wd + 2 * SP;
  // in the slit: one small line; open: one line edge to edge on a wide screen, four stacked lines on a phone
  const ls0 = phone ? .3 : .5, chars = 25;
  L.fs0 = phone ? Math.min(W * .05, (W / 2 - g - 20) / (Math.max(em.wa, em.wb, em.wc, em.wd) + ls0 * 7)) : Math.min(W * .026, 38, (W - 2 * g - 40) / (line + ls0 * chars)); L.ls0 = ls0;
  L.fs = phone ? Math.min(W * .16, (W - 2 * g) / Math.max(em.wa, em.wb, em.wc, em.wd)) : Math.min(H * .17, (W - 2 * g - W * .08) / line);
  L.em = em; L.g = g; L.SP = SP;
}

/* ---------- the path: north into Turn 2, round it, and back south to land ---------- */
let PATH = null, PROF = null, GAP = null, OUTP = null, SIDE = 0;
const OK = [.2, .37, .8, 1];             // the out leg, as a share of its scroll: first person, swing out, side on, swing back
const RECORD_KMH = 36.22;               // the open 200 km out-and-return record pace (FAI, 19 Jan 2014)
const TURN_TIME = '13:01';              // Turn 2 in the log, local time
const TA = 110;                         // samples either side of the turn that the wide shot holds (3.3 km)
async function loadPath() {
  const j = await (await fetch(HERO + 'path.json')).json();
  const n = j.x.length;
  PATH = { n, x: Float32Array.from(j.x), y: Float32Array.from(j.y), z: Float32Array.from(j.z), t: Float32Array.from(j.t), v: Float32Array.from(j.v), turn: j.turn };
  // his progress along the course against a flyer at record pace who set off level with him: metres, + when he is ahead
  const g = new Float32Array(n); for (let i = 0; i < n; i++) g[i] = i * j.step - RECORD_KMH / 3.6 * (PATH.t[i] - PATH.t[0]);
  GAP = { g, at: s => at(g, s) };
  { const sm = new Float32Array(n), R = 18; for (let i = 0; i < n; i++) { let a = 0, w = 0; for (let k = -R; k <= R; k++) { const q = clamp(i + k, 0, n - 1), e = Math.exp(-k * k / 72); a += g[q] * e; w += e; } sm[i] = a / w; } GAP.sm = s => at(sm, s); }
  // the out leg runs faster through the side-on view, so the gap can be seen opening
  { const N = 400, c = new Float64Array(N + 1), r = f => lerp(1, 2.2, ss(seg(f, OK[0] + .04, OK[1] + .06))) * lerp(1, .8, ss(seg(f, OK[2], 1)));
    for (let i = 1; i <= N; i++) c[i] = c[i - 1] + (r((i - .5) / N)) / N; for (let i = 0; i <= N; i++) c[i] /= c[N]; OUTP = { N, c }; }
  // the return's time warp: slow off the turn, faster and faster, a gentle arrival
  const N = 400, w = new Float64Array(N + 1), c = new Float64Array(N + 1);
  for (let i = 0; i <= N; i++) { const f = i / N; w[i] = .06 + Math.pow(ss(seg(f, 0, .7)), 1.5) * (1 - .82 * ss(seg(f, .86, 1))); }
  for (let i = 1; i <= N; i++) c[i] = c[i - 1] + (w[i] + w[i - 1]) / 2;
  let wm = 0; for (let i = 0; i <= N; i++) wm = Math.max(wm, w[i]);
  PROF = { N, w, c, tot: c[N], wm };
}
function flightAt(u) {                 // the scroll -> where he is on the path, which act, the orbit's angle and the warp
  const n = PATH.n, kT = PATH.turn, s1 = kT - TA, s2 = kT + TA;
  const uo = seg(u, U_TRANS, U_ORB), ut = seg(u, U_ORB, U_TURN), ur = seg(u, U_TURN, U_FLY);
  if (u < U_ORB) {
    const x = uo * OUTP.N, i = Math.min(OUTP.N - 1, Math.floor(x)), c = OUTP.c[i] + (OUTP.c[i + 1] - OUTP.c[i]) * (x - i);
    const sw = ss(seg(uo, OK[0], OK[1])) * (1 - ss(seg(uo, OK[2], OK[3])));
    return { act: 0, s: s1 * c, uo, ut: 0, ur: 0, sw, cw: 0, warpPos: .18 + .3 * ss(uo) };
  }
  if (u < U_TURN) return { act: 1, s: lerp(s1, s2, ut), uo: 1, ut, ur: 0, sw: 0, cw: 0, warpPos: .48 * (1 - ss(seg(ut, 0, .35))) + .1 };
  const N = PROF.N, x = ur * N, i = Math.min(N - 1, Math.floor(x)), r = x - i, c = PROF.c[i] + (PROF.c[i + 1] - PROF.c[i]) * r;
  return { act: 2, s: s2 + (n - 1 - s2) * c / PROF.tot, uo: 1, ut: 1, ur, sw: 0, cw: ss(seg(ur, .02, .2)), warpPos: (PROF.w[i] + (PROF.w[i + 1] - PROF.w[i]) * r) / PROF.wm };
}
function at(arr, s) { const i = clamp(Math.floor(s), 0, PATH.n - 2), f = clamp(s - i, 0, 1); return arr[i] + (arr[i + 1] - arr[i]) * f; }
function pos(s) {
  const n = PATH.n, i = clamp(Math.floor(s), 0, n - 2), f = clamp(s - i, 0, 1);
  const g = k => clamp(k, 0, n - 1), i0 = g(i - 1), i1 = i, i2 = g(i + 1), i3 = g(i + 2);
  const cr = a => { const p0 = a[i0], p1 = a[i1], p2 = a[i2], p3 = a[i3]; return .5 * ((2 * p1) + (-p0 + p2) * f + (2 * p0 - 5 * p1 + 4 * p2 - p3) * f * f + (-p0 + 3 * p1 - 3 * p2 + p3) * f * f * f); };
  return [cr(PATH.x), cr(PATH.y), cr(PATH.z)];
}
function dirAt(s, h) { const a = pos(Math.max(0, s - h)), b = pos(Math.min(PATH.n - 1, s + h)); const dx = b[0] - a[0], dz = b[2] - a[2], l = Math.hypot(dx, dz) || 1; return [dx / l, dz / l]; }
function camHeading(s) {               // smoothed and lagged: the camera never jolts
  let x = 0, z = 0;
  for (let k = 0; k < 16; k++) { const w = Math.exp(-k / 5), d = dirAt(Math.max(0, s - k * 2), 6); x += d[0] * w; z += d[1] * w; }
  const l = Math.hypot(x, z) || 1; return [x / l, z / l];
}
function bankAt(s) {                   // only the big bends, never past 8 degrees
  const a = dirAt(Math.max(0, s - 12), 8), b = dirAt(Math.min(PATH.n - 1, s + 12), 8);
  return clamp(Math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) * 1.1, -.14, .14);
}
function turnBank(s) {                 // round the turn: the log's own shape, smoothed, up to about 35 degrees
  const a = dirAt(Math.max(0, s - 5), 3), b = dirAt(Math.min(PATH.n - 1, s + 5), 3);
  return clamp(Math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) * 1.6, -.62, .62);
}
const hhmm = t => { t = Math.round(t / 60); return String(Math.floor(t / 60) % 24).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0'); };

/* ---------- 3D ---------- */
let G = null;
async function init3D() {
  const THREE = await import('./lib/three.module.min.js');
  const TILES = HERO + (phone ? 't/p/' : 't/');      // the heights, at half the resolution on a phone
  const canvas = $('gl');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
  const PR = Math.min(devicePixelRatio || 1, phone ? 1.25 : 1.5);
  renderer.setPixelRatio(PR); renderer.setSize(W, H, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene(), front = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, W / H, 1, 95000);
  const SUN = new THREE.Vector3(.8, .5, .3).normalize();

  const DK = { value: 1 }, CR = { value: 1 };             // the sky at dusk; how far out the contours are drawn
  const sky = new THREE.Mesh(new THREE.SphereGeometry(80000, 32, 16), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, uniforms: { sun: { value: SUN }, dk: DK },
    vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
    fragmentShader: `uniform vec3 sun; uniform float dk; varying vec3 vD;
      vec3 skyc(float e, vec3 zen, vec3 mid, vec3 hor, vec3 haze, float hz){ vec3 c = mix(hor, mid, smoothstep(.0,.16,e)); c = mix(c, zen, smoothstep(.14,.75,e)); return mix(c, haze, (1.-smoothstep(-.02,hz,e))*.6); }
      void main(){ float e = clamp(vD.y,-.2,1.), g = max(dot(normalize(vD), sun), 0.);
        vec3 day = skyc(e, vec3(.33,.53,.80), vec3(.58,.72,.87), vec3(.83,.87,.90), vec3(.90,.88,.83), .08) + vec3(1.,.95,.85)*(pow(g,48.)*.35 + pow(g,6.)*.08);
        vec3 dusk = skyc(e, vec3(.02,.025,.04), vec3(.06,.065,.09), vec3(.18,.15,.145), vec3(.38,.22,.12), .1);   // a warm band low over the valley
        dusk += vec3(1.,.52,.2)*(pow(g,5.)*.12 + pow(g,36.)*.16) * (1.-smoothstep(0.,.3,e));
        gl_FragColor = vec4(mix(day, dusk, dk),1.); }`
  }));
  sky.renderOrder = -10; scene.add(sky);

  const TV = `varying vec3 vW; varying vec2 vUv; void main(){ vUv = uv; vec4 w = modelMatrix * vec4(position,1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`;
  const TF = `precision highp float;
    uniform sampler2D nmap; uniform vec3 cam; uniform float fogD, detail, cut, cr;
    varying vec3 vW; varying vec2 vUv;
    float h21(vec2 p){ p = fract(p*vec2(123.34,456.21)); p += dot(p,p+45.32); return fract(p.x*p.y); }
    float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.-2.*f);
      return mix(mix(h21(i),h21(i+vec2(1,0)),f.x), mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x), f.y); }
    void main(){
      float dist = length(vW - cam);
      if (cut > 0. && length(vW.xz - cam.xz) < cut) discard;
      vec4 nm = texture2D(nmap, vUv); vec3 n = nm.xyz*2.-1.; float ao = nm.a;
      float near = (1. - smoothstep(120., 2200., dist)) * detail;
      vec2 q = mod(vW.xz, 8192.);
      n = normalize(n + vec3(vn(q*.3)-.5, 0., vn(q*.3+9.)-.5)*.45*near + vec3(vn(q*1.3)-.5, 0., vn(q*1.3+3.)-.5)*.25*near);
      // the ground is drawn from heights alone: graphite, a low sun raking from the east, contours every 22 m and an index line every 110 m
      vec3 sr = normalize(vec3(1., .15, .1));
      float lr = max(dot(n, sr), 0.);
      vec3 d = vec3(.068,.072,.088)*(.45 + .55*ao) + vec3(.36,.35,.36)*pow(lr, 1.3)*(.5 + .5*ao) + vec3(.016,.018,.026)*(.5 + .5*n.y);
      float hc = vW.y / 22., fw = max(fwidth(hc), 1e-4), dl = abs(fract(hc - .5) - .5) / fw;
      float hi = vW.y / 110., fwi = max(fwidth(hi), 1e-4), di = abs(fract(hi - .5) - .5) / fwi;
      float close = 1. - smoothstep(150. * cr, 1400. * cr, dist);
      float fade = (1. - smoothstep(1000. * cr, 5000. * cr, dist)) * clamp(1.1 - fw * 5., 0., 1.);
      float fadeI = (1. - smoothstep(2000. * cr, 7000. * cr, dist)) * clamp(1.15 - fwi * 5., 0., 1.);
      float ln = (1. - smoothstep(mix(.42, .22, close), mix(1.2, .78, close), dl)) * mix(.24, .44, close) * fade + (1. - smoothstep(.5, 1.35, di)) * .23 * fadeI;
      d = mix(d, vec3(.84,.84,.86), ln);
      float fd = 1. - exp(-pow(dist / (fogD * 1.15 * (1. + .35 * (cr - 1.))), 1.6));
      d = mix(d, mix(vec3(.11,.105,.12), vec3(.21,.15,.12), smoothstep(5000., 16000., dist)), clamp(fd, 0., 1.));
      gl_FragColor = vec4(d, 1.);
    }`;
  const tmat = (nmap, opts = {}) => new THREE.ShaderMaterial({
    uniforms: { nmap: { value: nmap }, cam: { value: new THREE.Vector3() }, fogD: { value: phone ? 8000 : 10500 }, detail: { value: opts.detail ?? 1 }, cut: { value: 0 }, cr: CR },
    vertexShader: TV, fragmentShader: TF, polygonOffset: !!opts.back, polygonOffsetFactor: opts.back ? 4 : 0, polygonOffsetUnits: opts.back ? 4 : 0
  });

  async function heights(url) {
    const blob = await (await fetch(url)).blob();
    let bmp; try { bmp = await createImageBitmap(blob, { colorSpaceConversion: 'none', premultiplyAlpha: 'none' }); } catch (e) { bmp = await createImageBitmap(blob); }
    const w = bmp.width, h = bmp.height, cv = new OffscreenCanvas(w, h), cx = cv.getContext('2d', { willReadFrequently: true });
    cx.drawImage(bmp, 0, 0); const px = cx.getImageData(0, 0, w, h).data, A = new Float32Array(w * h);
    for (let i = 0, j = 0; i < A.length; i++, j += 4) A[i] = (px[j] * 256 + px[j + 1]) / 16 + 500;
    return { A, w, h };
  }
  function normals(D, m) {
    const { A, w, h } = D, px = new Uint8Array(w * h * 4);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const l = A[y * w + Math.max(0, x - 1)], r = A[y * w + Math.min(w - 1, x + 1)], u = A[Math.max(0, y - 1) * w + x], d = A[Math.min(h - 1, y + 1) * w + x];
      let nx = (l - r) / (2 * m), nz = (u - d) / (2 * m), ny = 1; const k = 1 / Math.hypot(nx, ny, nz); nx *= k; ny *= k; nz *= k;
      const R = 3, xa = Math.max(0, x - R), xb = Math.min(w - 1, x + R), ya = Math.max(0, y - R), yb = Math.min(h - 1, y + R), c0 = A[y * w + x];
      const mean = (A[ya * w + xa] + A[ya * w + xb] + A[yb * w + xa] + A[yb * w + xb] + A[ya * w + x] + A[yb * w + x] + A[y * w + xa] + A[y * w + xb]) / 8;
      const ao = clamp(.55 + (c0 - mean) / (m * R) * 1.6);
      const i = (y * w + x) * 4; px[i] = (nx * .5 + .5) * 255; px[i + 1] = (ny * .5 + .5) * 255; px[i + 2] = (nz * .5 + .5) * 255; px[i + 3] = ao * 255;
    }
    const t = new THREE.DataTexture(px, w, h, THREE.RGBAFormat); t.flipY = false; t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter; t.magFilter = THREE.LinearFilter; t.needsUpdate = true; return t;
  }
  function grid(S, x0, z0, size, hfn) {      // (S+1)^2 vertices over a square and a skirt from its edge
    const nv = (S + 1) * (S + 1), ns = 4 * S, P = new Float32Array((nv + ns) * 3), UV = new Float32Array((nv + ns) * 2), idx = [];
    for (let j = 0; j <= S; j++) for (let i = 0; i <= S; i++) {
      const u = i / S, v = j / S, k = j * (S + 1) + i;
      P[k * 3] = x0 + u * size; P[k * 3 + 1] = hfn(u, v); P[k * 3 + 2] = z0 + v * size; UV[k * 2] = u; UV[k * 2 + 1] = v;
    }
    for (let j = 0; j < S; j++) for (let i = 0; i < S; i++) { const a = j * (S + 1) + i, b = a + 1, c = a + S + 1, d = c + 1; idx.push(a, c, b, b, c, d); }
    const ring = []; for (let i = 0; i < S; i++) ring.push(i); for (let j = 0; j < S; j++) ring.push(j * (S + 1) + S); for (let i = S; i > 0; i--) ring.push(S * (S + 1) + i); for (let j = S; j > 0; j--) ring.push(j * (S + 1));
    ring.forEach((k, r) => { const q = nv + r; P[q * 3] = P[k * 3]; P[q * 3 + 1] = P[k * 3 + 1] - 60; P[q * 3 + 2] = P[k * 3 + 2]; UV[q * 2] = UV[k * 2]; UV[q * 2 + 1] = UV[k * 2 + 1]; });
    for (let r = 0; r < ring.length; r++) { const a = ring[r], b = ring[(r + 1) % ring.length], c = nv + r, d = nv + (r + 1) % ring.length; idx.push(a, b, c, b, d, c); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('uv', new THREE.BufferAttribute(UV, 2));
    g.setIndex(nv + ns > 65535 ? new THREE.Uint32BufferAttribute(idx, 1) : new THREE.Uint16BufferAttribute(idx, 1)); return g;
  }

  /* the whole valley, coarse */
  const far = { mesh: null };
  (async () => {
    const D = await heights(TILES + 'far-h.webp');
    far.D = D; const m = FAR.w / D.w;
    const S = phone ? 160 : 240, Sz = Math.round(S * D.h / D.w);
    const g = new THREE.BufferGeometry(); const P = [], UV = [], idx = [];
    for (let j = 0; j <= Sz; j++) for (let i = 0; i <= S; i++) {
      const u = i / S, v = j / Sz, hx = Math.min(D.w - 1, Math.round(u * (D.w - 1))), hz = Math.min(D.h - 1, Math.round(v * (D.h - 1)));
      P.push(FAR.x0 + u * FAR.w, D.A[hz * D.w + hx] - 25, FAR.z0 + v * FAR.h); UV.push(u, v);
    }
    for (let j = 0; j < Sz; j++) for (let i = 0; i < S; i++) { const a = j * (S + 1) + i, b = a + 1, cc = a + S + 1, d = cc + 1; idx.push(a, cc, b, b, cc, d); }
    g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(UV, 2)); g.setIndex(idx);
    far.mesh = new THREE.Mesh(g, tmat(normals(D, m), { detail: 0, back: true })); far.mesh.renderOrder = -5; far.mesh.frustumCulled = false; scene.add(far.mesh);
    if (G) G.dirty = true; kick();
  })();

  /* the squares near the camera */
  const sq = new Map(), key = (i, j) => i + ',' + j;
  CHUNKS.forEach(([i, j]) => sq.set(key(i, j), { i, j, state: 0 }));
  const holes = []; {
    const is = CHUNKS.map(c => c[0]), js = CHUNKS.map(c => c[1]);
    for (let i = Math.min(...is) - 3; i <= Math.max(...is) + 3; i++) for (let j = Math.min(...js) - 3; j <= Math.max(...js) + 3; j++) if (!sq.has(key(i, j))) holes.push([i, j]);
  }
  let loading = 0;
  function sampleH(x, z) {
    const i = Math.floor(x / CS), j = Math.floor(z / CS), Q = sq.get(key(i, j));
    if (Q && Q.D) {
      const w = Q.D.w, m = CS / w, fx = clamp((x - i * CS) / m - .5, 0, w - 1.001), fz = clamp((z - j * CS) / m - .5, 0, w - 1.001), x0 = Math.floor(fx), z0 = Math.floor(fz), a = fx - x0, b = fz - z0, A = Q.D.A;
      return A[z0 * w + x0] * (1 - a) * (1 - b) + A[z0 * w + x0 + 1] * a * (1 - b) + A[(z0 + 1) * w + x0] * (1 - a) * b + A[(z0 + 1) * w + x0 + 1] * a * b;
    }
    if (far.D) { const D = far.D, u = clamp((x - FAR.x0) / FAR.w) * (D.w - 1), v = clamp((z - FAR.z0) / FAR.h) * (D.h - 1); return D.A[Math.round(v) * D.w + Math.round(u)]; }
    return NaN;
  }
  async function loadSq(Q) {
    Q.state = 1; loading++;
    try {
      const k = `${Q.i}_${Q.j}`;
      const D = await heights(`${TILES}hm${k}.webp`);
      Q.D = D; Q.n = normals(D, CS / D.w); Q.state = 2;
      for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const N = sq.get(key(Q.i + di, Q.j + dj)); if (N && N.mesh) N.lod = -1; }
    } catch (e) { Q.state = 0; }
    loading--; if (G) G.dirty = true; kick();
  }
  function meshSq(Q, S) {
    if (Q.mesh) { scene.remove(Q.mesh); Q.mesh.geometry.dispose(); }
    const x0 = Q.i * CS, z0 = Q.j * CS;
    if (!Q.mat) Q.mat = tmat(Q.n);
    Q.mesh = new THREE.Mesh(grid(S, x0, z0, CS, (u, v) => sampleH(x0 + u * CS, z0 + v * CS)), Q.mat); Q.lod = S; scene.add(Q.mesh);
  }
  function dropSq(Q) {
    if (Q.mesh) { scene.remove(Q.mesh); Q.mesh.geometry.dispose(); Q.mesh = null; }
    if (Q.mat) { Q.mat.dispose(); Q.mat = null; }
    Q.n && Q.n.dispose(); Q.D = null; Q.n = null; Q.state = 0; Q.lod = 0;
  }
  const LOADR = phone ? 9000 : 12000, DROPR = 20000;
  function manage(cx, cz, ahead) {
    const want = [];
    for (const Q of sq.values()) {
      const dd = (ax, az) => Math.hypot(Math.max(Q.i * CS - ax, 0, ax - (Q.i + 1) * CS), Math.max(Q.j * CS - az, 0, az - (Q.j + 1) * CS));
      const d = dd(cx, cz); let da = 1e9; for (const [ax, az] of ahead) da = Math.min(da, dd(ax, az));
      Q.dist = d;
      if (Q.state === 0 && Math.min(d, da) < LOADR) want.push([Math.min(d, da), Q]);
      if (Q.state === 2 && d > DROPR && da > DROPR) dropSq(Q);
    }
    want.sort((a, b) => a[0] - b[0]);
    for (const [, Q] of want) { if (loading >= 4) break; loadSq(Q); }
    let nearR = 1e9, rebuilt = 0, pending = 0;
    for (const Q of sq.values()) if (Q.state !== 2 && Q.dist < 6000) pending++;
    for (const [i, j] of holes) nearR = Math.min(nearR, Math.hypot(Math.max(i * CS - cx, 0, cx - (i + 1) * CS), Math.max(j * CS - cz, 0, cz - (j + 1) * CS)));
    for (const Q of sq.values()) {
      if (Q.state !== 2) { nearR = Math.min(nearR, Q.dist); continue; }
      const S = Q.dist < 3000 ? (phone ? 160 : 256) : Q.dist < 8000 ? (phone ? 64 : 96) : 32;
      if (Q.lod !== S && rebuilt < 2) { meshSq(Q, S); rebuilt++; }
      if (Q.lod !== S) G.dirty = true;
    }
    if (far.mesh) far.mesh.material.uniforms.cut.value = nearR > 1e8 ? 0 : Math.max(0, nearR - 400);
    window.__terrain = { pending, far: !!far.mesh, rebuilding: [...sq.values()].some(Q => Q.state === 2 && Q.dist < 3000 && Q.lod < 100) };
  }

  /* no wing on screen in the run: you are the pilot. Record pace is a cool light with a trail; side on, he is a warm one */
  const ptMat = col => new THREE.ShaderMaterial({ transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { op: { value: 0 }, col: { value: new THREE.Vector3(...col) }, sz: { value: (phone ? 30 : 34) * Math.min(devicePixelRatio || 1, 1.5) } },
    vertexShader: `uniform float sz; void main(){ gl_PointSize = sz; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
    fragmentShader: `uniform float op; uniform vec3 col; void main(){ vec2 d = gl_PointCoord - .5; float r = length(d) * 2.; float a = exp(-r * r * 6.) + .9 * exp(-r * r * 60.); gl_FragColor = vec4(mix(col, vec3(1.), exp(-r * r * 80.)) * a * op, a * op); }` });
  const point = col => { const m = ptMat(col), o = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(3), 3)), m); o.frustumCulled = false; front.add(o); return o; };
  const ribbon = col => {
    const N = 64, P = new Float32Array(N * 6), S = new Float32Array(N * 2), A = new Float32Array(N * 2), I = [];
    for (let i = 0; i < N; i++) { S[i * 2] = -1; S[i * 2 + 1] = 1; if (i < N - 1) { const k = i * 2; I.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); } }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('side', new THREE.BufferAttribute(S, 1)); g.setAttribute('a', new THREE.BufferAttribute(A, 1)); g.setIndex(I);
    const m = new THREE.Mesh(g, new THREE.ShaderMaterial({ transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
      uniforms: { col: { value: new THREE.Vector3(...col) } },
      vertexShader: `attribute float side, a; varying float vS, vA; void main(){ vS = side; vA = a; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
      fragmentShader: `uniform vec3 col; varying float vS, vA; void main(){ gl_FragColor = vec4(col, vA * exp(-vS * vS * 2.6)); }` }));
    m.frustumCulled = false; front.add(m); return { m, P, A, N };
  };
  const COOL = [.72, .86, 1.], WARM = [1., .66, .3];
  const gpt = point(COOL), mpt = point(WARM), gtr = ribbon(COOL), mtr = ribbon(WARM);

  /* flecks near the ground, part of the streaming scenery */
  const NP = phone ? 120 : 320, fp = new Float32Array(NP * 4), fpos = new Float32Array(NP * 6), fal = new Float32Array(NP * 2);
  let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const spawn = (k, far0) => { fp[k * 4] = far0 ? -15 + rnd() * 260 : 180 + rnd() * 90; fp[k * 4 + 1] = (rnd() - .5) * 140; fp[k * 4 + 2] = rnd() < .75 ? .4 + rnd() * 4 : 6 + rnd() * 34; fp[k * 4 + 3] = .4 + rnd() * .6; };
  for (let k = 0; k < NP; k++) spawn(k, true);
  const fg = new THREE.BufferGeometry(); fg.setAttribute('position', new THREE.BufferAttribute(fpos, 3)); fg.setAttribute('a', new THREE.BufferAttribute(fal, 1));
  const flecks = new THREE.LineSegments(fg, new THREE.ShaderMaterial({
    transparent: true, depthWrite: false,
    vertexShader: `attribute float a; varying float vA; void main(){ vA = a; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
    fragmentShader: `varying float vA; void main(){ gl_FragColor = vec4(.97,.93,.80, vA); }`
  }));
  flecks.frustumCulled = false; scene.add(flecks);

  /* B: the line of flight ahead, a thin orange thread draped along the ridge */
  const NL = 520, lpos = new Float32Array(NL * 3), lal = new Float32Array(NL);
  const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.BufferAttribute(lpos, 3)); lg.setAttribute('a', new THREE.BufferAttribute(lal, 1));
  const route = new THREE.Line(lg, new THREE.ShaderMaterial({ transparent: true, depthWrite: false,
    vertexShader: `attribute float a; varying float vA; void main(){ vA = a; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
    fragmentShader: `varying float vA; void main(){ gl_FragColor = vec4(1.,.56,.22, vA); }` }));
  route.frustumCulled = false; scene.add(route);
  const gpos = new Float32Array(NL * 2 * 3), gside = new Float32Array(NL * 2), gal = new Float32Array(NL * 2), gidx = [];
  for (let i = 0; i < NL; i++) { gside[i * 2] = -1; gside[i * 2 + 1] = 1; if (i < NL - 1) { const a = i * 2; gidx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } }
  const gg = new THREE.BufferGeometry(); gg.setAttribute('position', new THREE.BufferAttribute(gpos, 3)); gg.setAttribute('side', new THREE.BufferAttribute(gside, 1)); gg.setAttribute('a', new THREE.BufferAttribute(gal, 1)); gg.setIndex(gidx);
  const glow = new THREE.Mesh(gg, new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
    vertexShader: `attribute float side, a; varying float vS, vA; void main(){ vS = side; vA = a; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
    fragmentShader: `varying float vS, vA; void main(){ gl_FragColor = vec4(1.,.46,.09, vA * exp(-vS*vS*3.2) * .55); }` }));
  glow.frustumCulled = false; scene.add(glow);

  /* the time warp: the scenery is drawn to a target, then streaked toward the vanishing point; the wing goes on top */
  const rt = new THREE.WebGLRenderTarget(Math.round(W * PR), Math.round(H * PR), { depthBuffer: true });
  const NS = phone ? 7 : 12;
  const post = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({
    depthTest: false, depthWrite: false,
    uniforms: { tex: { value: rt.texture }, vp: { value: new THREE.Vector2(.5, .55) }, k: { value: 0 }, ca: { value: 0 }, asp: { value: W / H }, zoom: { value: 0 }, dof: { value: 0 }, lin: { value: 0 }, ldir: { value: new THREE.Vector2(1, 0) } },
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy,0.,1.); }`,
    fragmentShader: `uniform sampler2D tex; uniform vec2 vp, ldir; uniform float k, ca, asp, zoom, dof, lin; varying vec2 vUv;
      void main(){
        vec2 uv = vp + (vUv - vp) * (1. - zoom * (1. - lin));
        float r = length((uv - vp) * vec2(asp, 1.));
        vec2 d = mix(uv - vp, ldir * .3, lin);
        float m = mix(smoothstep(.05, .75, r), .5, lin) * k;
        float e = smoothstep(.35, .95, r) * ca;
        vec3 c = vec3(0.);
        for (int i = 0; i < ${NS}; i++) { float t = float(i) / float(${NS - 1}); vec2 o = d * m * t + vec2(cos(float(i) * 2.4), sin(float(i) * 2.4) * asp) * dof * sqrt(t + .08);
          c.r += texture2D(tex, uv - o * (1. + e * 6.) - d * e * .5).r; c.g += texture2D(tex, uv - o).g; c.b += texture2D(tex, uv - o * (1. - e * 6.) + d * e * .5).b; }
        gl_FragColor = vec4(c / float(${NS}), 1.);
      }`
  }));
  const postScene = new THREE.Scene(), postCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1); postScene.add(post);

  G = { gpt, mpt, gtr, mtr, CR, glow, gpos, gal, DK, route, lpos, lal, THREE, renderer, scene, front, camera, flecks, fp, fpos, fal, spawn, sampleH, manage, far, sq, sky, rt, post, postScene, postCam, PR, dirty: true };
  onResize(); kick();
}

/* ---------- the cameras: his eyes, the side-on view of the ridge, and the swing between them ---------- */
const EYE = 75;                          // his eyes ride 75 m over the line of flight: about 115 m over the ridge line
const softMax = (a, b, k) => b + k * Math.log1p(Math.exp((a - b) / k));      // max(a, b), with no corner in it
function fpRig(F) {                   // his eyes: high over the line of flight, looking along the escarpment, the head rolling gently with the bends
  const s = F.s, p = pos(s), h = camHeading(s), eye = [p[0], p[1] + EYE, p[2]];
  const tw = F.act === 1 ? ss(seg(F.ut, 0, .3)) * (1 - ss(seg(F.ut, .7, 1))) : 0;
  const roll = lerp(bankAt(s) * .9, clamp(turnBank(s) * .75, -.46, .46), F.act === 1 ? ss(seg(F.ut, 0, .25)) * (1 - ss(seg(F.ut, .75, 1))) : 0);
  if (G) { const g = G.sampleH(eye[0], eye[2]); if (g === g) eye[1] = softMax(eye[1], g + 70, 25); }
  const pitch = Math.tan(13 * Math.PI / 180) * 400;
  // in the turn the eyes lead round it: they look at the line a few hundred metres on, so the orange curve stays in view
  const q = pos(Math.min(PATH.n - 1, s + 14)), lk = [eye[0] + h[0] * 400, eye[1] - pitch, eye[2] + h[1] * 400], lt = [q[0], q[1] - 40, q[2]];
  return { p, h, bank: roll, cam: eye, look: lk.map((v, i) => lerp(v, lt[i], tw * .85)), fov: 10 + 6 * tw, tw };
}
function ghostS(s, sw) {              // where record pace is on the path: in his eyes a softly clamped lead; side on, the log's real gap
  const gap = GAP.sm(s), fp = s + (90 + 560 * Math.tanh(Math.max(0, -gap) / 2600)) / 30;
  const dm = phone ? 2600 : 6000, side = s - Math.sign(gap) * dm * Math.tanh(Math.abs(gap) / dm) / 30;
  return clamp(lerp(fp, side, sw), 0, PATH.n - 1);
}
function valleySide() {               // which side of the escarpment the valley lies, from the coarse heights, once
  if (SIDE || !G || !G.far.D) return SIDE || 1;
  let sum = 0;
  for (let k = 100; k <= 420; k += 40) { const p = pos(k), d = dirAt(k, 20), nx = -d[1], nz = d[0]; sum += G.sampleH(p[0] + nx * 2500, p[2] + nz * 2500) - G.sampleH(p[0] - nx * 2500, p[2] - nz * 2500); }
  return SIDE = sum < 0 ? 1 : -1;
}
function sideRig(F) {                 // side on, from out over the valley: the ridge runs across the screen, both racers on it
  const s = F.s, sg = ghostS(s, 1), P = pos(s), Q = pos(sg), m = pos((s + sg) / 2);
  const a = pos(Math.max(0, Math.min(s, sg) - 40)), b = pos(Math.min(PATH.n - 1, Math.max(s, sg) + 40));
  let rx = b[0] - a[0], rz = b[2] - a[2]; const rl = Math.hypot(rx, rz) || 1; rx /= rl; rz /= rl;
  const sd = valleySide(), nx = -rz * sd, nz = rx * sd;
  const sep = Math.hypot(Q[0] - P[0], Q[2] - P[2]), vf = ((phone ? 64 : 48) + (phone ? 12 : 4)) * Math.PI / 360, hf = Math.atan(Math.tan(vf) * W / H);
  const D = Math.max(phone ? 2600 : 1900, sep / ((phone ? .64 : .5) * 2 * Math.tan(hf)));
  // a little over the line of flight, out over the valley: the escarpment's face below, its rim and the plateau running across the frame
  const cam = [m[0] + nx * D, m[1] + 80 + D * .085, m[2] + nz * D];
  if (G) { const g = G.sampleH(cam[0], cam[2]); if (g === g) cam[1] = softMax(cam[1], g + 250, 60); }
  return { p: P, h: [rx, rz], bank: 0, cam, look: [m[0], m[1] - D * .06, m[2]], fov: phone ? 12 : 4, tw: 0, D, rd: [rx, rz] };
}
/* the escarpment's edge: for each point of the course, the top of the steepest drop toward the valley, found once
   from the coarse heights and smoothed; drawn in the side view and the chase as a thin warm line */
function findCrest() {
  const sd = valleySide(), lines = [], kT = PATH.turn;
  let zOut = -1e9; for (let k = 0; k <= kT; k++) zOut = Math.max(zOut, PATH.z[k]);
  const run = (k0, k1, flip) => {
    const T = [], K = [];
    for (let k = k0; k <= k1; k += 2) {
      const p = pos(k), d = dirAt(k, 20), f = flip ? -1 : 1, nx = -d[1] * sd * f, nz = d[0] * sd * f;
      if (flip && p[2] < zOut + 300) { if (T.length > 4) lines.push({ T: T.splice(0), K: K.splice(0) }); else { T.length = 0; K.length = 0; } continue; }
      const H = t => G.sampleH(p[0] + nx * t, p[2] + nz * t);
      let best = -1e9, tb = 0;
      for (let t = -1000; t <= 2500; t += 50) { const dr = H(t) - H(t + 300); if (dr > best) { best = dr; tb = t; } }
      let t = tb; while (t > -1200 && H(t - 50) - H(t) > best * .12) t -= 50;      // walk up the face to where it eases off: the edge
      T.push(t); K.push([k, nx, nz]);
    }
    if (T.length > 4) lines.push({ T, K });
  };
  run(0, kT - 30, false); run(kT + 1, PATH.n - 60, true);
  return lines.map(({ T, K }) => {
    // the edge runs in and out of every gully: a running median, then a wide smoothing, gives the line of the escarpment
    const N = T.length, M = new Float32Array(N), S = new Float32Array(N);
    for (let i = 0; i < N; i++) { const w = []; for (let j = -6; j <= 6; j++) w.push(T[clamp(i + j, 0, N - 1)]); w.sort((a, b) => a - b); M[i] = w[6]; }
    for (let i = 0; i < N; i++) { let a = 0, w = 0; for (let j = -18; j <= 18; j++) { const q = clamp(i + j, 0, N - 1), e = Math.exp(-j * j / 72); a += M[q] * e; w += e; } S[i] = a / w; }
    const P = new Float32Array(N * 2); for (let i = 0; i < N; i++) { const [k, nx, nz] = K[i], p = pos(k); P[i * 2] = p[0] + nx * S[i]; P[i * 2 + 1] = p[2] + nz * S[i]; }
    return P;
  });
}
function chaseRig(F) {                // after the turn: high above and behind the rear light, both racers on the ridge ahead of the lens
  const s = F.s, sg = ghostS(s, 1), r = Math.min(s, sg), f = Math.max(s, sg), m = pos((s + sg) / 2), P = pos(s), pr = pos(r), pf = pos(f);
  const d = dirAt((s + sg) / 2, 40), sep = Math.hypot(pf[0] - pr[0], pf[2] - pr[2]);
  const sd = valleySide(), nx = -d[1] * sd, nz = d[0] * sd;
  const back = 900 + .55 * sep, up = 520 + .3 * sep, out = 350 + .2 * sep;
  const cam = [pr[0] - d[0] * back + nx * out, pr[1] + up, pr[2] - d[1] * back + nz * out];
  if (G) { const g = G.sampleH(cam[0], cam[2]); if (g === g) cam[1] = softMax(cam[1], g + 300, 60); }
  return { p: P, h: d, bank: 0, cam, look: [m[0] + d[0] * .15 * sep, m[1] - 60, m[2] + d[1] * .15 * sep], fov: phone ? 10 : 2, tw: 0, D: back, rd: d };
}
function flightRig(F) {
  const A = fpRig(F), side = F.sw > 0, k = side ? F.sw : (F.cw || 0);
  if (!(k > 0)) return A;
  const B = side ? sideRig(F) : chaseRig(F);
  // the eyes' look, carried out to the distance of the side view's subject, so the swing turns smoothly onto it
  const d = A.look.map((v, i) => v - A.cam[i]), dl = Math.hypot(...d), L = Math.hypot(...B.look.map((v, i) => v - A.cam[i]));
  const la = A.cam.map((v, i) => v + d[i] / dl * L);
  const cam = A.cam.map((v, i) => lerp(v, B.cam[i], k)); cam[1] += Math.sin(Math.PI * k) * B.D * .06;
  return { p: A.p, h: (() => { const x = lerp(A.h[0], B.h[0], k), z = lerp(A.h[1], B.h[1], k), l = Math.hypot(x, z) || 1; return [x / l, z / l]; })(), bank: A.bank * (1 - k), cam, look: la.map((v, i) => lerp(v, B.look[i], k)), fov: lerp(A.fov, B.fov, k), tw: 0, sw: side ? k : 0, cw: side ? 0 : k, D: B.D, rd: B.rd };
}
/* the camera itself: the angles follow the rig with a short lag and never turn faster than a set rate, whatever the scroll does */
let CAM = null;
const wrapA = a => Math.atan2(Math.sin(a), Math.cos(a));
function settle(R, dt) {
  const dx = R.look[0] - R.cam[0], dy = R.look[1] - R.cam[1], dz = R.look[2] - R.cam[2];
  const T = { yaw: Math.atan2(-dx, -dz), pitch: Math.atan2(dy, Math.hypot(dx, dz)), roll: R.bank, fov: R.fov || 0 };
  if (!CAM || dt <= 0 || window.__snap) { CAM = { ...T }; return 0; }
  const k = 1 - Math.exp(-dt / .11);
  const step = (cur, tgt, rate) => { const d = wrapA(tgt - cur); return cur + clamp(d * k, -rate * dt, rate * dt); };
  CAM.yaw = step(CAM.yaw, T.yaw, 2.2); CAM.pitch = step(CAM.pitch, T.pitch, .8); CAM.roll = step(CAM.roll, T.roll, .9); CAM.fov += (T.fov - CAM.fov) * k;
  return Math.abs(wrapA(T.yaw - CAM.yaw)) + Math.abs(T.pitch - CAM.pitch) + Math.abs(T.roll - CAM.roll);
}
function placeCamera(R, warp) {
  const { camera } = G;
  camera.fov = (phone ? 64 : 48) + CAM.fov + (phone ? 14 : 20) * warp; camera.updateProjectionMatrix();
  camera.position.set(R.cam[0], R.cam[1], R.cam[2]); camera.rotation.order = 'YXZ'; camera.rotation.set(CAM.pitch, CAM.yaw, -CAM.roll); camera.updateMatrixWorld();
}

/* ---------- state, eased in time; nothing moves unless the visitor scrolls ---------- */
/* ---------- the photograph in depth: the land slides back under him, the far ridge drifts, the sky holds ---------- */
const PV = [1100, 560];                 // where he is heading, in the photograph's pixels
const PIL = [1052, 700];                // just over his head: the push passes through it, into his seat
const PIV = [1000, 330];                // the wing swings about a point up in its lines
let PG = null;
function initPhoto() {
  const cv = $('pgc'); const o = { alpha: false, antialias: false, depth: false };
  let gl = cv.getContext('webgl2', o); const v2 = !!gl; if (!gl) gl = cv.getContext('webgl', o); if (!gl) return;
  const sh = (t, src) => { const x = gl.createShader(t); gl.shaderSource(x, src); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(x)); return x; };
  const pr = gl.createProgram();
  gl.attachShader(pr, sh(gl.VERTEX_SHADER, `attribute vec2 p; varying vec2 vUv; void main(){ vUv = p * .5 + .5; gl_Position = vec4(p, 0., 1.); }`));
  // each screen pixel finds the photograph's pixel that the forward move has carried there: nearer land (higher depth) moves more
  gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, `precision highp float;
    uniform sampler2D img, dep; uniform vec2 res, V; uniform vec3 L; uniform float dz, lat, rise; varying vec2 vUv;
    const vec2 PS = vec2(1920., 1080.);
    void main(){
      vec2 q = vec2(vUv.x, 1. - vUv.y) * res, pq = (q - L.yz) / L.x, p = pq;
      for (int i = 0; i < 5; i++) { float z = texture2D(dep, p / PS).r; p = V + (pq - V - vec2(lat, rise) * z * 1080.) * (1. - dz * z); }
      gl_FragColor = vec4(texture2D(img, clamp(p / PS, vec2(.0003), vec2(.9997))).rgb, 1.);
    }`));
  gl.linkProgram(pr); gl.useProgram(pr);
  const vb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const ap = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(ap); gl.vertexAttribPointer(ap, 2, gl.FLOAT, false, 0, 0);
  const U = {}; for (const k of ['img', 'dep', 'res', 'V', 'L', 'dz', 'lat', 'rise']) U[k] = gl.getUniformLocation(pr, k);
  const tex = (im, unit, mip) => {
    const t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    if (mip && v2) { gl.generateMipmap(gl.TEXTURE_2D); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR); }
    else gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  };
  const load = src => new Promise((ok, no) => { const im = new Image(); im.onload = () => ok(im); im.onerror = no; im.src = src; });
  Promise.all([load(HERO + 'plate.jpg'), load(HERO + 'depth.png')]).then(([im, dp]) => {
    tex(im, 0, true); tex(dp, 1, false); gl.uniform1i(U.img, 0); gl.uniform1i(U.dep, 1); gl.uniform2f(U.V, PV[0], PV[1]);
    PG = { gl, U, cv, key: '' }; $('plate').style.visibility = 'hidden'; kick();
  }).catch(() => {});
}
function drawPhoto(dz, lat, rise) {
  if (!PG) return;
  const { gl, U, cv } = PG, r = Math.min(devicePixelRatio || 1, 2), w = Math.round(W * r), h = Math.round(H * r);
  const key = [w, h, L.s, L.tx, L.ty, dz.toFixed(5), lat.toFixed(5), rise.toFixed(5)].join();
  if (key === PG.key) return; PG.key = key;
  if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
  gl.viewport(0, 0, w, h);
  gl.uniform2f(U.res, W, H); gl.uniform3f(U.L, L.s, L.tx, L.ty); gl.uniform1f(U.dz, dz); gl.uniform1f(U.lat, lat); gl.uniform1f(U.rise, rise);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
}
// 2D affine maps [a, b, c, d, e, f], as CSS writes them
const aff = (A, B) => [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1], A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3], A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]];
const affAt = (M, x, y) => [M[0] * x + M[2] * y + M[4], M[1] * x + M[3] * y + M[5]];
const about = (c, k, th) => { const co = Math.cos(th) * k, si = Math.sin(th) * k; return [co, si, -si, co, c[0] - co * c[0] + si * c[1], c[1] - si * c[0] - co * c[1]]; };

let uT = 0, uS = 0, uV = 0, sPrev = -1, vel = 0, motion = 0, last = performance.now(), raf = 0;
function readScroll() { const r = hero.getBoundingClientRect(), tot = hero.offsetHeight - innerHeight; uT = clamp(-r.top / Math.max(1, tot)) * U_END; }
function kick() { if (!raf) { last = performance.now(); raf = requestAnimationFrame(frame); } }
addEventListener('scroll', () => { readScroll(); kick(); }, { passive: true });
function onResize() {
  layout(); readScroll();
  if (G) { G.renderer.setSize(W, H, false); G.rt.setSize(Math.round(W * G.PR), Math.round(H * G.PR)); G.camera.aspect = W / H; G.camera.updateProjectionMatrix(); G.post.material.uniforms.asp.value = W / H; G.dirty = true; }
  kick();
}
addEventListener('resize', onResize);

function frame(now) {
  raf = 0; const dt = Math.min(.05, (now - last) / 1000); last = now;
  // the scroll drives a critically damped spring, stepped finely, so a big jump is followed smoothly at any frame rate
  for (let t = dt; t > 1e-6; t -= 1 / 120) { const h = Math.min(t, 1 / 120), OM = 7.5; uV += (OM * OM * (uT - uS) - 2 * OM * uV) * h; uS += uV * h; }
  if ((Math.abs(uT - uS) < 2e-4 && Math.abs(uV) < 2e-3) || window.__snap) { uS = uT; uV = 0; }     // __snap: for stills only
  const u = uS;
  const eO = seg(u, 0, U_OPEN), eG = seg(u, U_OPEN * .4, U_GLIDE), eT = seg(u, U_GLIDE, U_TRANS), eE = seg(u, U_FLY, U_END);

  /* the opening: a widescreen frame opening out, a thin slit, then 2.39:1, then the whole screen; flares along its edges,
     the exposure rising from dark; the push-in is the photograph's own depth move (below), so the frame never shows its edges */
  $('cue').style.opacity = 1 - seg(eO, .02, .12);
  {
    const slit = H * (phone ? .03 : .04), lb = Math.min(H, W / 2.39);
    const h = lerp(lerp(slit, lb, ss(seg(eO, 0, .42))), H, io(seg(eO, .38, 1)));
    const bar = Math.max(0, (H - h) / 2);
    for (const id of ['lbt', 'lbb']) { const el = $(id); el.style.display = 'block'; el.style.height = bar + 'px'; el.style.visibility = bar > 0 ? 'visible' : 'hidden'; }
    const fl = (1 - seg(eO, .8, 1)) * (.55 + .45 * ss(seg(eO, 0, .3)));
    for (const el of document.querySelectorAll('.srh-lb i, .srh-lb em')) el.style.opacity = fl;
    $('grain').style.opacity = eT < 1 ? .09 : 0; $('grain').style.backgroundPosition = `${(u * 9137) % 200}px ${(u * 5651) % 200}px`;
  }
  const push = 1, bright = lerp(.3, 1, ss(seg(eO, .03, .95)));
  $('photo').style.filter = eO < 1 ? `brightness(${bright.toFixed(3)})` : 'none';
  $('plate').style.transform = `translate3d(${L.tx}px,${L.ty}px,0) scale(${L.s})`;
  // the words: grow from the slit, tracking tightens, the halves ride out to the edges
  {
    titleSetup();
    let fs = lerp(L.fs0, L.fs, out(seg(eO, 0, .85))), ls = lerp(L.ls0, -.025, out(seg(eO, 0, .9))), g = L.g, sp = (L.SP + Math.max(0, ls)) * fs;
    const ids = ['wa', 'wb', 'wc', 'wd'], w = {}, pos = {};
    const measure = f => { for (const id of ids) { const el = $(id); el.style.fontSize = f + 'px'; el.style.letterSpacing = ls + 'em'; w[id] = el.offsetWidth - ls * f; } };
    measure(fs);
    if (!phone) {        // the line never runs wider than the screen, at any moment of the opening
      const tot = w.wa + w.wb + w.wc + w.wd + 2 * sp + 28 + W * .04, avail = W - 2 * g;
      if (tot > avail) { fs *= avail / tot; sp *= avail / tot; measure(fs); }
    }
    const k = io(seg(eO, .05, 1)), exitK = io(seg(eT, 0, .6));
    if (!phone) {
      // one line: WORLD SPEED | RECORD ATTEMPT, the seam between the halves; the halves ride to the edges
      const y = lerp(H * .5, H * .6, io(eO)) - fs * .43;
      let cB = W / 2 - 14 - w.wb, cC = W / 2 + 14;
      const ovR = cC + w.wc + sp + w.wd - (W - g); if (ovR > 0) { cB -= ovR; cC -= ovR; }     // the longer right half: the whole line slides to fit
      const ovL = g - (cB - sp - w.wa); if (ovL > 0) { cB += ovL; cC += ovL; }
      const oA = g, oD = W - g - w.wd;
      let xb = lerp(cB, oA + w.wa + sp, k), xa = xb - sp - w.wa, xc = lerp(cC, oD - sp - w.wc, k), xd = xc + w.wc + sp;
      const dl = Math.max(0, g - xa); xa += dl; xb += dl;
      const dr = Math.min(0, W - g - (xd + w.wd)); xc += dr; xd += dr;
      Object.assign(pos, { wa: [xa, y], wb: [xb, y], wc: [xc, y], wd: [xd, y] });
    } else {
      // four rows: WORLD and SPEED to the left of the seam, RECORD and ATTEMPT to the right; they ride out to the edges
      const lh = fs * .9, yc = lerp(H * .5, H * .56, io(eO)) - fs * .43;
      ids.forEach((id, r) => {
        const left = r < 2, x = left ? lerp(W / 2 - 14 - w[id], g, k) : lerp(W / 2 + 14, W - g - w[id], k);
        pos[id] = [clamp(x, g, W - g - w[id]), yc + (r - 1.5) * lh];
      });
    }
    for (const id of ids) {
      const side = id === 'wa' || id === 'wb' ? -1 : 1, x = pos[id][0] + side * exitK * W * .6, y = pos[id][1];
      const el = $(id); el.style.transform = `translate3d(${x}px,${y}px,0)`; el.style.opacity = 1 - exitK;
    }
    TPOS = { fs, ls, pos, exitK, eO };
  }

  /* the glide: the land slides back under him, the far ridge drifts, he flies on; then the push into his seat */
  const ready = G && PATH;
  const gp = eE > 0 ? 0 : Math.max(ss(eG), .35 * ss(eO)), jT = io(eT);
  {
    const th = .016 * Math.sin(Math.PI * 1.5 * gp), sc = 1 + .05 * gp, dr = [(PV[0] - PIL[0]) * .07 * gp, (PV[1] - PIL[1]) * .07 * gp];
    const zoom = eE > 0 ? 1 : lerpLog(1, 7, io(seg(eT, 0, .85)));
    let M = [CUT.k, 0, 0, CUT.k, CUT.x, CUT.y];
    M = aff(about(PIV, sc, th), M); M[4] += dr[0]; M[5] += dr[1];
    M = aff(about(PIL, zoom, 0), M);
    M = aff([L.s, 0, 0, L.s, L.tx, L.ty], M);
    const photoA = eE > 0 ? ss(seg(eE, 0, .6)) : 1 - ss(seg(eT, .45, .9));
    const wingA = eE > 0 ? photoA : 1 - seg(eT, .5, .75);
    $('wing').style.transform = `matrix(${M.map(v => v.toFixed(5)).join(',')})`;
    $('wing').style.opacity = wingA; $('wing').style.visibility = wingA > 0 ? 'visible' : 'hidden';
    $('photo').style.opacity = photoA; $('photo').style.visibility = photoA > 0 ? 'visible' : 'hidden';
    if (photoA > 0) drawPhoto(eE > 0 ? 0 : .16 * gp + .3 * jT, -.01 * gp, eE > 0 ? 0 : -.03 * jT);
    drawRig(M, push, wingA * (eE > 0 ? 1 : 1 - seg(eT, .2, .5)));
    drawTitle(M, bright);
  }
  $('veil').style.opacity = 1 - seg(eT, .3, .8) * .45 * (1 - eE);

  /* the run */
  let s = 0, warpPos = 0, F = null;
  if (PATH && PROF) { F = flightAt(u); s = F.s; warpPos = F.warpPos; }
  if (sPrev < 0) sPrev = s;
  vel += (Math.abs(s - sPrev) * 30 / Math.max(dt, 1e-3) - vel) * (1 - Math.exp(-dt / .2)); sPrev = s;
  const moving = eT >= 1 && eE < 1 ? clamp(vel / 2500) : 0;
  motion += (moving - motion) * (1 - Math.exp(-dt / .25)); if (motion < .003 && moving === 0) motion = 0;
  // the warp: rises along the run, fully on while the visitor scrolls, a calm trace of it at rest
  const warp = eT >= 1 ? warpPos * (.35 + .65 * motion) * (1 - seg(eE, 0, .7)) : 0;
  const flyA = seg(eT, .55, 1) * (1 - seg(eE, 0, .45));
  $('read').style.opacity = flyA; $('leg').style.opacity = flyA; $('warpT').style.opacity = flyA * seg(warpPos, .1, .4);
  $('warpM').style.transform = `scaleX(${warp.toFixed(3)})`;
  { const a = seg(eE, .3, .85); $('srend').style.opacity = a; $('srend').classList.toggle('is-on', a > .5); $('credit').style.opacity = a; }
  $('veil').style.background = eE > 0 ? `linear-gradient(180deg,rgba(10,12,16,.4) 0%,rgba(10,12,16,0) 22%,rgba(10,12,16,0) ${lerp(56, 40, eE)}%,rgba(10,12,16,${lerp(.6, .82, eE).toFixed(2)}) 100%)` : '';
  $('vig').style.opacity = clamp(warp * .9);
  if (PATH) {
    $('legT').textContent = F.act === 0 ? 'Northbound, into Turn 2' : F.act === 1 ? 'Turn 2' : 'Southbound, back to land';
    { const gk = GAP.at(s); $('ghostb').style.opacity = gk > 150 && eT >= 1 ? flyA * (1 - Math.max(F.sw, F.cw)) : 0; $('gbk').textContent = (gk / 1000).toFixed(1); }
    { const k = F.act === 1 ? ss(seg(F.ut, .2, .4)) * (1 - ss(seg(F.ut, .7, .85))) : 0; $('turnm').style.opacity = k * flyA; }
    $('clk').textContent = hhmm(at(PATH.t, s)); $('spd').textContent = Math.round(at(PATH.v, s));
    const gk = Math.round(GAP.at(s) / 100) / 10; $('gap').textContent = (gk > 0 ? '+' : gk < 0 ? '\u2212' : '') + Math.abs(gk).toFixed(1) + ' km';
  }
  DRAIN = ss(seg(eT, .3, 1)); GFADE = 1 - seg(eE, 0, .45);
  const live3D = eT > 0 && eE < .6;
  $('gl').style.visibility = live3D ? 'visible' : 'hidden';
  { const gl = $('ghostl'), a = eT >= 1 && GHOSTXY && live3D ? flyA : 0; gl.style.opacity = a; if (GHOSTXY) gl.style.transform = `translate3d(${(GHOSTXY[0] + 10).toFixed(1)}px,${(GHOSTXY[1] - 4).toFixed(1)}px,0)`; }
  { const el = $('mel'), a = eT >= 1 && MEXY && F ? flyA * ss(seg(Math.max(F.sw, F.cw), .5, .9)) : 0; el.style.opacity = a; if (MEXY) el.style.transform = `translate3d(${(MEXY[0] + 10).toFixed(1)}px,${(MEXY[1] - 4).toFixed(1)}px,0)`; }
  let busy = false;
  if (ready && live3D) busy = render3D(eT < 1 ? flightAt(U_TRANS) : F, eT, warp, dt);
  else if (ready) { const R = fpRig(flightAt(U_TRANS)); G.manage(R.cam[0], R.cam[2], [[R.p[0], R.p[2]]]); G.dirty = false; CAM = null; }
  drawFx(warp, live3D && eT >= 1 && F ? (F.act === 2 ? 1 : F.sw > .02 ? 2 : 0) : 0, F ? F.sw : 0);
  if (Math.abs(uT - uS) > 1e-4 || uV !== 0 || motion > 0 || busy || (G && G.dirty)) raf = requestAnimationFrame(frame);
}

function drawRig(M, push, a) {      // the lines on the photograph's wing, 0.6 px at rest, thickening only as the push closes in
  const c = $('rig').getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
  if (a <= 0) return;
  const cx = W / 2, cy = H * .46, P = ([x, y]) => { const q = affAt(M, x - 13, y - 25); return [cx + (q[0] - cx) * push, cy + (q[1] - cy) * push]; };
  const s = Math.sqrt(Math.abs(M[0] * M[3] - M[1] * M[2])), z = s / (L.s * CUT.k);
  c.lineCap = 'round';
  c.strokeStyle = `rgba(20,21,25,${a})`; c.lineWidth = Math.max(.8, 4.2 * s * push);
  c.beginPath(); for (const [p, q] of RIG.risers) { const A = P(p), B = P(q); c.moveTo(A[0], A[1]); c.lineTo(B[0], B[1]); } c.stroke();
  c.strokeStyle = `rgba(246,244,244,${(a * (phone ? .22 : .36)).toFixed(3)})`; c.lineWidth = .6 * Math.pow(z, .6);
  c.beginPath(); for (const [p, q] of RIG.lines) { const A = P(p), B = P(q); c.moveTo(A[0], A[1]); c.lineTo(B[0], B[1]); } c.stroke();
}

let VP = [.5, .55], DRAIN = 0, GHOSTXY = null, MEXY = null, GFADE = 1, SDIR = [1, 0], DIM = null;
function render3D(F, eT, warp, dt) {
  const { THREE, renderer, scene, front, camera } = G, s = F.s;
  const R = flightRig(F), sw = R.sw || 0, cw = R.cw || 0, vw = Math.max(sw, cw);
  const lag = settle(R, dt);
  placeCamera(R, warp);
  const sg = ghostS(s, vw);
  const ahead = [pos(Math.min(PATH.n - 1, s + 150)), pos(Math.min(PATH.n - 1, s + 400)), pos(sg), pos((s + sg) / 2)].map(p => [p[0], p[2]]);
  G.dirty = false;
  G.manage(R.cam[0], R.cam[2], ahead);
  for (const Q of G.sq.values()) if (Q.mat) Q.mat.uniforms.cam.value.set(...R.cam);
  if (G.far.mesh) G.far.mesh.material.uniforms.cam.value.set(...R.cam);
  G.sky.position.set(...R.cam);
  if (!G.arc) {                  // the turn's real shape, a glowing arc in the air that fills in as he banks round
    const a0 = Math.max(0, PATH.turn - 60), a1 = Math.min(PATH.n - 1, PATH.turn + 60), N = a1 - a0 + 1;
    const P = new Float32Array(N * 6), S = new Float32Array(N * 2), A = new Float32Array(N * 2), I = [], LP = new Float32Array(N * 3), LA = new Float32Array(N);
    for (let i = 0; i < N; i++) {
      const p = pos(a0 + i), d = dirAt(a0 + i, 2), y = p[1] - 9, w = 1.6;
      P.set([p[0] - d[1] * w, y, p[2] + d[0] * w, p[0] + d[1] * w, y, p[2] - d[0] * w], i * 6); S[i * 2] = -1; S[i * 2 + 1] = 1; LP.set([p[0], y, p[2]], i * 3);
      if (i < N - 1) { const k = i * 2; I.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('side', new THREE.BufferAttribute(S, 1)); g.setAttribute('a', new THREE.BufferAttribute(A, 1)); g.setIndex(I);
    const glow = new THREE.Mesh(g, new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
      vertexShader: `attribute float side, a; varying float vS, vA; void main(){ vS = side; vA = a; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
      fragmentShader: `varying float vS, vA; void main(){ gl_FragColor = vec4(1.,.46,.09, vA * exp(-vS*vS*3.) * .8); }` }));
    const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.BufferAttribute(LP, 3)); lg.setAttribute('a', new THREE.BufferAttribute(LA, 1));
    const core = new THREE.Line(lg, new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      vertexShader: `attribute float a; varying float vA; void main(){ vA = a; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
      fragmentShader: `varying float vA; void main(){ gl_FragColor = vec4(1.,.66,.3, vA); }` }));
    glow.frustumCulled = core.frustumCulled = false; scene.add(glow); scene.add(core);
    G.arc = { a0, N, A, LA, glow, core };
  }
  {
    const { a0, N, A, LA, glow, core } = G.arc, vis = F.act === 1 ? ss(seg(F.ut, 0, .2)) * (1 - ss(seg(F.ut, .85, 1))) : 0;
    for (let i = 0; i < N; i++) { const j = a0 + i, ahead = ss(clamp((j - s - 3) / 6)), e = Math.min(1, Math.min(i, N - 1 - i) / 12); const a = vis * e * ahead; A[i * 2] = A[i * 2 + 1] = a; LA[i] = a; }      // the turn's shape, ahead of you, curving away
    glow.geometry.attributes.a.needsUpdate = true; core.geometry.attributes.a.needsUpdate = true; glow.visible = core.visible = vis > .005;
  }
  G.CR.value = 1 + 1.2 * vw;
  if (!G.crest && G.far.D) {
    G.crest = findCrest().map(P => {
      const N = P.length / 2, V = new Float32Array(N * 6), S = new Float32Array(N * 2), A = new Float32Array(N * 2), I = [];
      for (let i = 0; i < N; i++) { S[i * 2] = -1; S[i * 2 + 1] = 1; if (i < N - 1) { const k = i * 2; I.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); } }
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(V, 3)); g.setAttribute('side', new THREE.BufferAttribute(S, 1)); g.setAttribute('a', new THREE.BufferAttribute(A, 1)); g.setIndex(I);
      const m = new THREE.Mesh(g, new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
        vertexShader: `attribute float side, a; varying float vS, vA; void main(){ vS = side; vA = a; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
        fragmentShader: `varying float vS, vA; void main(){ gl_FragColor = vec4(1., .62, .3, vA * exp(-vS * vS * 2.4)); }` }));
      m.frustumCulled = false; m.renderOrder = 2; scene.add(m); return { P, N, V, A, m };
    });
  }
  if (G.crest) {                 // the edge, lit only in the side view and the chase; faint far off
    const cp = camera.position;
    for (const C of G.crest) {
      C.m.visible = vw > .01; if (!C.m.visible) continue;
      for (let i = 0; i < C.N; i++) {
        const x = C.P[i * 2], z = C.P[i * 2 + 1]; let y = G.sampleH(x, z); if (y !== y) y = 0; y += 4;
        const j = Math.min(C.N - 1, i + 1), jj = Math.max(0, i - 1), tx = C.P[j * 2] - C.P[jj * 2], tz = C.P[j * 2 + 1] - C.P[jj * 2 + 1];
        const vx = cp.x - x, vy = cp.y - y, vz = cp.z - z, dv = Math.hypot(vx, vy, vz);
        let c0 = -tz * vy, c1 = tz * vx - tx * vz, c2 = tx * vy; const cl = Math.hypot(c0, c1, c2) || 1, w = dv * (phone ? .0018 : .0013);
        c0 *= w / cl; c1 *= w / cl; c2 *= w / cl;
        C.V.set([x - c0, y - c1, z - c2, x + c0, y + c1, z + c2], i * 6);
        C.A[i * 2] = C.A[i * 2 + 1] = .5 * vw * GFADE * (1 - ss(seg(dv, 9000, 22000))) * Math.min(1, Math.min(i, C.N - 1 - i) / 6);
      }
      C.m.geometry.attributes.position.needsUpdate = true; C.m.geometry.attributes.a.needsUpdate = true;
    }
  }
  {                              // the route ahead, from a little in front of the wing to 15 km on; it comes in with the contour world
    const NL = G.lal.length;
    for (let i = 0; i < NL; i++) {
      const q = Math.min(PATH.n - 1, s + 3 + i), p = pos(q), pn = pos(Math.min(PATH.n - 1, q + 1)); let g = G.sampleH(p[0], p[2]); if (g !== g) g = p[1] - 40;
      const y = Math.max(g + 6, p[1] - 9), a = Math.min(1, ss(clamp(i / 12)) * (1 - i / NL) * DRAIN * (1 - .6 * (R.tw || 0)) * (1 - .65 * sw));      // the line of flight ahead, a little under your eyes
      G.lpos[i * 3] = p[0]; G.lpos[i * 3 + 1] = y; G.lpos[i * 3 + 2] = p[2]; G.lal[i] = .95 * a;
      let dx = pn[0] - p[0], dz = pn[2] - p[2]; const l = Math.hypot(dx, dz) || 1, w = 2.2 + i * .06; dx /= l; dz /= l;
      G.gpos.set([p[0] - dz * w, y, p[2] + dx * w, p[0] + dz * w, y, p[2] - dx * w], i * 6); G.gal[i * 2] = G.gal[i * 2 + 1] = a;
    }
    G.route.geometry.attributes.position.needsUpdate = true; G.route.geometry.attributes.a.needsUpdate = true;
    G.glow.geometry.attributes.position.needsUpdate = true; G.glow.geometry.attributes.a.needsUpdate = true;
  }
  {                              // record pace: a cool light on the path ahead when it leads; side on, both racers at the log's own gap
    const gap = GAP.sm(s), lead = gap < -150, pg = pos(sg), cp = camera.position;
    const trail = (rb, s0, s1, al) => {
      for (let i = 0; i < rb.N; i++) {
        const f = i / (rb.N - 1), q = lerp(s0, s1, f), p = pos(q), a = pos(Math.max(0, q - .5)), b = pos(Math.min(PATH.n - 1, q + .5));
        const t = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [cp.x - p[0], cp.y - p[1] - 1.5, cp.z - p[2]], dv = Math.hypot(...v);
        let c = [t[1] * v[2] - t[2] * v[1], t[2] * v[0] - t[0] * v[2], t[0] * v[1] - t[1] * v[0]]; const cl = Math.hypot(...c) || 1, w = dv * (phone ? .0034 : .0024);
        c = c.map(x => x / cl * w); rb.P.set([p[0] - c[0], p[1] + 1.5 - c[1], p[2] - c[2], p[0] + c[0], p[1] + 1.5 + c[1], p[2] + c[2]], i * 6);
        rb.A[i * 2] = rb.A[i * 2 + 1] = al * Math.pow(f, 1.6) * .8;
      }
      rb.m.geometry.attributes.position.needsUpdate = true; rb.m.geometry.attributes.a.needsUpdate = true; rb.m.visible = al > .01;
    };
    const ga = (lead ? 1 : vw) * seg(eT, .95, 1) * GFADE;
    G.gpt.geometry.attributes.position.array.set([pg[0], pg[1] + 1.5, pg[2]]); G.gpt.geometry.attributes.position.needsUpdate = true; G.gpt.material.uniforms.op.value = ga;
    trail(G.gtr, sg - lerp(Math.min(10, Math.max(0, sg - s - 3)), 40, vw), sg, ga * .7);
    const ma = vw * GFADE, pm = pos(s);
    G.mpt.geometry.attributes.position.array.set([pm[0], pm[1] + 1.5, pm[2]]); G.mpt.geometry.attributes.position.needsUpdate = true; G.mpt.material.uniforms.op.value = ma; G.mpt.visible = ma > .01;
    trail(G.mtr, Math.max(0, s - 40), s, ma * .8);
    const scr = p => { const t = new THREE.Vector3(p[0], p[1] + 1.5, p[2]).project(camera); return t.z < 1 && Math.abs(t.x) < 1 && Math.abs(t.y) < 1 ? [(t.x * .5 + .5) * W, (-t.y * .5 + .5) * H] : null; };
    const gs = scr(pg), ms = scr(pm);
    // labels: in his eyes, beside the light; side on, each over its own light, his running left from it, record pace's running right
    const gw = $('ghostl').offsetWidth, mw = $('mel').offsetWidth;
    GHOSTXY = ga > .01 && gs ? (vw > .3 ? [clamp(gs[0] - 14, 16, W - gw - 22), clamp(gs[1] - 26, 150, H - 140)] : [clamp(gs[0] + 14, 16, W - 200), clamp(gs[1] - 8, 150, H - 140)]) : null;
    MEXY = vw > .3 && ms ? [clamp(ms[0] - mw + 4, 6, W - mw - 22), clamp(ms[1] - 26, 150, H - 140)] : null;
    DIM = sw > .3 && gs && ms ? { a: ms, b: gs, km: Math.abs(GAP.at(s)) / 1000, al: ss(seg(sw, .55, .95)) * GFADE } : null;
    // the ridge's direction on the screen, for the streaks when side on
    if (R.rd) { const a2 = new THREE.Vector3(pm[0], pm[1], pm[2]).project(camera), b2 = new THREE.Vector3(pm[0] + R.rd[0] * 400, pm[1], pm[2] + R.rd[1] * 400).project(camera); const dx = (b2.x - a2.x) * W, dy = (b2.y - a2.y) * H, l = Math.hypot(dx, dy) || 1; SDIR = [dx / l, dy / l]; }
  }
  // where the run is heading, on the screen
  const f = new THREE.Vector3(R.cam[0] + R.h[0] * 3000, R.p[1] - 40, R.cam[2] + R.h[1] * 3000).project(camera);
  VP = [f.x * .5 + .5, f.y * .5 + .5];
  // flecks streaming past, in the camera's frame
  const { fp, fpos, fal } = G, NP = fal.length / 2, fw = [R.h[0], R.h[1]], rt = [-R.h[1], R.h[0]];
  const vis = 40 + 900 * warp, len = clamp(vis * .045, .3, 40);
  for (let k = 0; k < NP; k++) {
    fp[k * 4] -= vis * dt * (.6 + .4 * fp[k * 4 + 3]);
    if (fp[k * 4] < -14) G.spawn(k, false);
    const a = fp[k * 4], b = fp[k * 4 + 1], hg = fp[k * 4 + 2];
    const x = R.cam[0] + fw[0] * a + rt[0] * b, z = R.cam[2] + fw[1] * a + rt[1] * b;
    let g = G.sampleH(x, z); if (g !== g) g = R.p[1] - 40;
    const y = g + hg, al = warp * (hg > 5 ? .2 : .6) * fp[k * 4 + 3] * clamp((a + 14) / 30) * clamp((270 - a) / 60);
    const i6 = k * 6; fpos[i6] = x; fpos[i6 + 1] = y; fpos[i6 + 2] = z; fpos[i6 + 3] = x + fw[0] * len; fpos[i6 + 4] = y; fpos[i6 + 5] = z + fw[1] * len;
    fal[k * 2] = al; fal[k * 2 + 1] = 0;
  }
  G.flecks.geometry.attributes.position.needsUpdate = true; G.flecks.geometry.attributes.a.needsUpdate = true;
  G.flecks.visible = warp > .01 && F.act === 2 && cw < .5;
  // scenery, then the streak pass, then the wing on top
  const U = G.post.material.uniforms;
  U.lin.value = sw; U.ldir.value.set(SDIR[0], SDIR[1] * W / H);         // a unit step along the ridge on the screen, in the picture's own units
  U.vp.value.set(VP[0], VP[1]); U.k.value = .16 * Math.pow(warp, 1.3); U.ca.value = .006 * ss(seg(warp, .6, 1)); U.zoom.value = .025 * warp; U.dof.value = phone ? .0012 : .0016;
  renderer.setRenderTarget(G.rt); renderer.clear(); renderer.render(scene, camera);
  renderer.setRenderTarget(null); renderer.autoClear = true; renderer.render(G.postScene, G.postCam);
  renderer.autoClear = false; renderer.clearDepth(); renderer.render(front, camera); renderer.autoClear = true;
  return G.dirty || warp > .01 || lag > 1e-3;
}

/* streaks: radial from the vanishing point in his eyes, along the ridge when side on; and side on, the gap between the racers measured */
let fxs = 7;
function drawFx(w, mode, sw) {
  const c = $('fx').getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
  if (DIM && mode && DIM.al > .01) {
    const { a, b } = DIM, dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy);
    if (l > 40) {
      const ux = dx / l, uy = dy / l; let nx = -uy, ny = ux; if (ny < 0) { nx = -nx; ny = -ny; }
      const o = 26, A = [a[0] + nx * o, a[1] + ny * o], B = [b[0] + nx * o, b[1] + ny * o], al = DIM.al;
      c.lineWidth = 1; c.strokeStyle = `rgba(246,244,244,${(.42 * al).toFixed(3)})`;
      c.beginPath(); c.moveTo(A[0], A[1]); c.lineTo(B[0], B[1]);
      for (const P of [A, B]) { c.moveTo(P[0] - nx * 5, P[1] - ny * 5); c.lineTo(P[0] + nx * 5, P[1] + ny * 5); }
      c.stroke();
      c.setLineDash([2, 4]); c.strokeStyle = `rgba(246,244,244,${(.22 * al).toFixed(3)})`;
      c.beginPath(); c.moveTo(a[0] + nx * 8, a[1] + ny * 8); c.lineTo(A[0] - nx * 6, A[1] - ny * 6); c.moveTo(b[0] + nx * 8, b[1] + ny * 8); c.lineTo(B[0] - nx * 6, B[1] - ny * 6); c.stroke(); c.setLineDash([]);
      if (l > 70) {
        c.font = '400 10px "DM Mono", ui-monospace, monospace'; try { c.letterSpacing = '1.4px'; } catch (e) {}
        c.textAlign = 'center'; c.textBaseline = 'top'; c.fillStyle = `rgba(246,244,244,${(.85 * al).toFixed(3)})`;
        c.shadowColor = 'rgba(0,0,0,.6)'; c.shadowBlur = 8;
        c.fillText(`${DIM.km.toFixed(1)} KM`, (A[0] + B[0]) / 2 + nx * 10, (A[1] + B[1]) / 2 + ny * 10);
        c.shadowBlur = 0;
      }
    }
  }
  const k = mode === 2 ? w * sw : w;
  if (!mode || k < .04) return;
  const D = Math.hypot(W, H);
  let s = fxs = (fxs * 16807) % 2147483647; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  c.lineCap = 'round';
  const streak = (x0, y0, x1, y1, a, lw) => {
    const g = c.createLinearGradient(x0, y0, x1, y1);
    g.addColorStop(0, 'rgba(246,244,244,0)'); g.addColorStop(.6, `rgba(246,244,244,${a.toFixed(3)})`); g.addColorStop(1, 'rgba(246,244,244,0)');
    c.strokeStyle = g; c.lineWidth = lw; c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
  };
  if (mode === 1) {
    const cx = VP[0] * W, cy = (1 - VP[1]) * H, n = phone ? 30 : 64;
    for (let i = 0; i < n; i++) {
      const ang = rnd() * Math.PI * 2, r0 = D * (.2 + .35 * rnd()), r1 = r0 + D * (.08 + .5 * rnd()) * k;
      streak(cx + Math.cos(ang) * r0, cy + Math.sin(ang) * r0, cx + Math.cos(ang) * r1, cy + Math.sin(ang) * r1, k * (.1 + .22 * rnd()), .5 + rnd() * .8);
    }
  } else {                         // along the ridge: mostly low in the frame, over the land streaming by
    const ux = SDIR[0], uy = -SDIR[1], n = phone ? 22 : 46;
    for (let i = 0; i < n; i++) {
      const x = rnd() * W, y = H * (.35 + .62 * rnd()), L0 = D * (.04 + .22 * rnd()) * k;
      streak(x - ux * L0, y - uy * L0, x + ux * L0, y + uy * L0, k * (.08 + .16 * rnd()), .5 + rnd() * .6);
    }
  }
}

/* ---------- start ---------- */
if (LIVE) {
  layout(); readScroll(); kick();
  try { initPhoto(); } catch (e) { console.error(e); }
  loadPath().then(kick);
  const go3D = () => init3D().catch(e => console.error(e));
  if (document.readyState === 'complete') setTimeout(go3D, 200); else addEventListener('load', () => setTimeout(go3D, 200), { once: true });
  document.fonts && document.fonts.ready.then(() => { layout(); kick(); });
}
