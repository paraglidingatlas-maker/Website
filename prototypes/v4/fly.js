/* The India page's flight (option E): the Dhauladhar as live 3D terrain, flown by the scroll
   and, when the visitor takes the controls, dragged, pinched and turned by hand. Built from
   open 19 m terrain data (tools/data/india-dem.json, prototypes/v4/img/india/dem/) with
   three.js (prototypes/v4/lib/). Generated page: tools/v4_india_e.py. Nothing moves on its own:
   the scroll, the pointer and the fingers are the only inputs. */
import * as THREE from "./lib/three.module.min.js";

(function () {
  var s = document.getElementById("flight"); if (!s) return;
  var dataEl = document.getElementById("v4i-fl-data"); if (!dataEl) return;
  var D; try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var mq = window.matchMedia || function () { return { matches: false }; };
  if (mq("(prefers-reduced-motion: reduce)").matches) return;
  var canvas = s.querySelector(".v4i-fl-canvas"); if (!canvas) return;
  var gl = null; try { gl = canvas.getContext("webgl2", { antialias: true, alpha: false, powerPreference: "high-performance" }); } catch (e) {}
  if (!gl) return;                                        // the still page stays
  var small = mq("(max-width: 700px)").matches, coarse = mq("(pointer: coarse)").matches, lite = /[?&]lite=1/.test(location.search);
  var pin = s.querySelector(".v4i-fl-pin"), map = s.querySelector(".v4i-fl-map"), ov = s.querySelector(".v4i-fl-ov"), lead = s.querySelector(".v4i-fl-lead");
  var kmEl = s.querySelector(".v4i-fl-km b"), atEl = s.querySelector(".v4i-fl-at"), altEl = s.querySelector(".v4i-fl-alt b");
  var chs = [].slice.call(s.querySelectorAll(".v4i-fl-c")), cards = [].slice.call(s.querySelectorAll(".v4i-fl-card"));
  var tie = lead.querySelector(".v4i-fl-tie"), dot = lead.querySelector(".v4i-fl-dot"), halo = lead.querySelector(".v4i-fl-halo");
  var head = s.querySelector(".v4i-fl-head"), pls = [].slice.call(ov.querySelectorAll(".v4i-fl-pl")), mks = [].slice.call(s.querySelectorAll(".v4i-fl-mk"));
  var chBox = s.querySelector(".v4i-fl-ch"), readBox = s.querySelector(".v4i-fl-read"), ctlBox = s.querySelector(".v4i-fl-ctl");
  function rectOf(el) { if (!el) return null; var r = el.getBoundingClientRect(), m = map.getBoundingClientRect(); return [r.left - m.left - 8, r.top - m.top - 8, r.right - m.left + 8, r.bottom - m.top + 8]; }
  var KR = { read: null, ctl: null, head: null, ch: null, top: 120, gut: 24 };   // the plates the pins keep out of, measured when they change
  function measureKeep() { KR.read = rectOf(readBox); KR.ctl = rectOf(ctlBox); KR.head = rectOf(head); KR.ch = rectOf(s.querySelector(".v4i-fl-c.is-on")); KR.top = head ? head.offsetHeight + (head.offsetTop || 0) + 10 : 120; KR.gut = head ? head.offsetLeft || 24 : 24; }
  var ctl = s.querySelector(".v4i-fl-ctl"), dlg = document.getElementById("v4i-fl-dlg"), hint = s.querySelector(".v4i-fl-hint");
  var G = D.grid, mpp = G.mpp, exag = G.exag, base = G.base_m, sizeX = G.w * mpp, sizeY = G.h * mpp;
  var TEX = (small || lite) ? D.textures.phone : D.textures.desktop, src = s.getAttribute("data-src") || "";
  var n = 0; D.per_leg.forEach(function (k) { n += k; }); n += 1;      // frames along the flight
  var MAXL = small ? D.phonePins : (D.maxPins || 9), FAR = D.farKm * 1000;
  s.classList.add("is-live");

  /* ---------- helpers ---------- */
  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function smooth(u) { return u * u * (3 - 2 * u); }
  var last = {}; function put(k, v, fn) { if (last[k] !== v) { last[k] = v; fn(v); } }
  function toWorld(px, py, h) { return new THREE.Vector3(px * mpp - sizeX / 2, sizeY / 2 - py * mpp, (h - base) * exag); }
  function gridOf(v) { return [(v.x + sizeX / 2) / mpp, (sizeY / 2 - v.y) / mpp]; }
  var H = null, HW = 0, HH = 0;                          // heights, bottom row first, at the texture's resolution
  function sampleH(A, AW, AH, gw, gh, px, py) {          // bilinear metres from a decoded height image laid over a gw by gh grid
    var sx = AW / gw, sy = AH / gh, x = clamp(px * sx, 0, AW - 1.001), y = clamp((gh - py) * sy, 0, AH - 1.001);
    var x0 = Math.floor(x), y0 = Math.floor(y), tx = x - x0, ty = y - y0, i = y0 * AW + x0;
    return lerp(lerp(A[i], A[i + 1], tx), lerp(A[i + AW], A[i + AW + 1], tx), ty);
  }
  function heightAt(px, py) {                            // metres at a grid position (reference grid px); a loaded inset answers inside its box
    for (var k = 0; k < layers.length; k++) { var L = layers[k]; if (L.H && px >= L.x0 && px <= L.x1 && py >= L.y0 && py <= L.y1) return sampleH(L.H, L.HW, L.HH, L.w, L.h, (px - L.x0) / L.scale, (py - L.y0) / L.scale); }
    if (!H) return base;
    return sampleH(H, HW, HH, G.w, G.h, px, py);
  }
  function groundZ(v) { var g = gridOf(v); return (heightAt(g[0], g[1]) - base) * exag; }

  /* ---------- the flight path: centripetal Catmull-Rom through the keys, eased per leg ---------- */
  var K = D.keys, cams = K.map(function (k) { return k.cam; }), tgts = K.map(function (k) { return k.tgt; });
  function catmull(pts, i, t) {
    var p0 = pts[Math.max(i - 1, 0)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(i + 2, pts.length - 1)];
    function tj(ti, a, b) { var d = Math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2])); return ti + Math.pow(Math.max(d, 1e-6), 0.5); }
    var t0 = 0, t1 = tj(t0, p0, p1), t2 = tj(t1, p1, p2), t3 = tj(t2, p2, p3), tt = t1 + (t2 - t1) * t;
    function L(a, b, u) { return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u]; }
    function seg(pa, pb, ta, tb) { return L(pa, pb, tb === ta ? 0 : (tt - ta) / (tb - ta)); }
    var A1 = seg(p0, p1, t0, t1), A2 = seg(p1, p2, t1, t2), A3 = seg(p2, p3, t2, t3), B1 = seg(A1, A2, t0, t2), B2 = seg(A2, A3, t1, t3);
    return seg(B1, B2, t1, t2);
  }
  function poseAt(f) {                                   // f: 0 .. n-1
    f = clamp(f, 0, n - 1); var leg = 0, acc = 0;
    while (leg < D.per_leg.length - 1 && f >= acc + D.per_leg[leg]) { acc += D.per_leg[leg]; leg++; }
    var u = smooth(clamp((f - acc) / D.per_leg[leg], 0, 1));
    if (f >= n - 1) { leg = D.per_leg.length - 1; u = 1; }
    var c = catmull(cams, leg, u), t = catmull(tgts, leg, u), a = K[leg], b = K[leg + 1];
    return { cam: toWorld(c[0], c[1], c[2]), tgt: toWorld(t[0], t[1], t[2]), fov: lerp(a.fov, b.fov, u), fog0: lerp(a.fog[0], b.fog[0], u), fog1: lerp(a.fog[1], b.fog[1], u), leg: leg,
             sun: (a.sun && b.sun) ? [lerp(a.sun[0], b.sun[0], u), lerp(a.sun[1], b.sun[1], u)] : (a.sun || b.sun || null) };
  }

  /* ---------- the scene ---------- */
  var renderer = new THREE.WebGLRenderer({ canvas: canvas, context: gl, antialias: true, alpha: false });
  renderer.setClearColor(new THREE.Color(D.light.fog), 1); renderer.outputColorSpace = THREE.SRGBColorSpace;
  var scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(48, 16 / 9, 80, 400000); camera.up.set(0, 0, 1);
  var az = THREE.MathUtils.degToRad(D.light.az), el = THREE.MathUtils.degToRad(D.light.el);
  var sunDir = new THREE.Vector3(Math.cos(el) * Math.sin(az), Math.cos(el) * Math.cos(az), Math.sin(el)).normalize();
  var uniforms = {
    hmap: { value: null }, cmap: { value: null }, wmap: { value: null }, hasW: { value: 0 }, texel: { value: new THREE.Vector2(1, 1) }, mppTex: { value: new THREE.Vector2(mpp, mpp) }, edge: { value: 0 }, lift: { value: 0 },
    base: { value: base }, exag: { value: exag }, sunDir: { value: sunDir }, sunI: { value: D.light.sun }, amb: { value: D.light.amb },
    exposure: { value: D.light.exposure }, fogColor: { value: new THREE.Color(D.light.fog) }, fogNear: { value: 9000 }, fogFar: { value: 60000 }, camPos: { value: new THREE.Vector3() }
  };
  var VS = [
      "uniform sampler2D hmap; uniform float base, exag, lift; varying vec2 vUv; varying vec3 vW;",
      "void main(){ vUv = uv; float h = texture2D(hmap, uv).r; vec3 p = vec3(position.xy, (h - base) * exag + lift); vW = (modelMatrix * vec4(p, 1.0)).xyz;",
      "  gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }"].join("\n");
  var FS = [
      "precision highp float; uniform sampler2D hmap, cmap, wmap; uniform float hasW; uniform vec2 texel, mppTex; uniform float exag, sunI, amb, exposure, fogNear, fogFar, edge;",
      "uniform vec3 sunDir, fogColor, camPos; varying vec2 vUv; varying vec3 vW;",
      "vec3 aces(vec3 x){ return clamp((x*(2.51*x+0.03))/(x*(2.43*x+0.59)+0.14), 0.0, 1.0); }",
      "void main(){",
      "  float hl = texture2D(hmap, vUv - vec2(texel.x, 0.0)).r, hr = texture2D(hmap, vUv + vec2(texel.x, 0.0)).r;",
      "  float hd = texture2D(hmap, vUv - vec2(0.0, texel.y)).r, hu = texture2D(hmap, vUv + vec2(0.0, texel.y)).r;",
      "  vec3 nrm = normalize(vec3(-(hr - hl) * exag / (2.0 * mppTex.x), -(hu - hd) * exag / (2.0 * mppTex.y), 1.0));",
      "  vec3 c = texture2D(cmap, vUv).rgb;",                      // sRGB texture: the sampler returns linear
      "  float d = max(dot(nrm, sunDir), 0.0); float hemi = nrm.z * 0.5 + 0.5;",
      "  vec3 sky = vec3(0.415, 0.44, 0.50), ground = vec3(0.125, 0.13, 0.153);",
      "  vec3 col = c * (d * sunI * vec3(1.0, 0.94, 0.88) + amb * mix(ground, sky, hemi)) * 0.3183;",
      "  if (hasW > 0.5) { float wv = texture2D(wmap, vUv).r; if (wv > 0.25) {",                                  // water: flat, dark, a sheen towards the light, a glint under the sun
      "    vec3 V = normalize(camPos - vW); float fr = pow(1.0 - max(V.z, 0.0), 3.0); vec3 R = reflect(-sunDir, vec3(0.0, 0.0, 1.0));",
      "    float gl = pow(max(dot(R, V), 0.0), 60.0); vec3 wc = wv > 0.75 ? vec3(0.030, 0.052, 0.080) : vec3(0.020, 0.056, 0.110);",
      "    col = wc * (0.6 + amb * 0.5) + sky * fr * 0.18 + vec3(1.0, 0.96, 0.9) * gl * 0.35 * sunI * 0.3; } }",
      "  col = aces(col * exposure / 0.6);",
      "  float f = smoothstep(fogNear, fogFar, distance(vW, camPos)); col = mix(col, fogColor, f);",         // THREE.Color is linear
      "  float ed = min(min(vUv.x, 1.0 - vUv.x), min(vUv.y, 1.0 - vUv.y)); float al = edge > 0.0 ? smoothstep(0.0, edge, ed) : 1.0;",   // an inset fades into the ground around it
      "  gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), al); }"].join("\n");
  uniforms.edge.value = D.edge_fade || 0;                 // the ground's outer edge can dissolve into the sky instead of ending in a line
  var material = new THREE.ShaderMaterial({ uniforms: uniforms, vertexShader: VS, fragmentShader: FS, transparent: !!D.edge_fade });
  material.polygonOffset = true; material.polygonOffsetFactor = 2; material.polygonOffsetUnits = 2;   // the base sits a hair behind any inset
  /* the insets: finer ground over the parts of the map that matter, loaded as the camera nears them */
  var layers = (D.layers || []).map(function (L) { var tx = (small || lite) ? L.textures.phone : L.textures.desktop; return { name: L.name, w: L.w, h: L.h, scale: L.scale, x0: L.px0[0], y0: L.px0[1], x1: L.px0[0] + L.w * L.scale, y1: L.px0[1] + L.h * L.scale, near: (L.near_km || 80) * 1000, tex: tx, H: null, started: false, mesh: null }; });
  var mesh = null, ready = false, started = false;
  function decodeHeights(img) {                          // a height image (R*256+G metres, rows north first) -> floats bottom row first, and a texture
    var w = img.naturalWidth, h = img.naturalHeight, cv = document.createElement("canvas"); cv.width = w; cv.height = h;
    var cx = cv.getContext("2d", { willReadFrequently: true }); cx.drawImage(img, 0, 0);
    var px = cx.getImageData(0, 0, w, h).data, half = new Uint16Array(w * h), A = new Float32Array(w * h);
    for (var y = 0; y < h; y++) for (var x = 0; x < w; x++) { var i = ((h - 1 - y) * w + x) * 4, hm = px[i] * 256 + px[i + 1], j = y * w + x; A[j] = hm; half[j] = THREE.DataUtils.toHalfFloat(hm); }
    var ht = new THREE.DataTexture(half, w, h, THREE.RedFormat, THREE.HalfFloatType); ht.minFilter = ht.magFilter = THREE.LinearFilter; ht.generateMipmaps = false; ht.needsUpdate = true;
    return { A: A, w: w, h: h, tex: ht };
  }
  function loadLayer(L) {
    if (L.started) return; L.started = true;
    var img = new Image(); img.decoding = "async";
    img.onload = function () {
      var d = decodeHeights(img); L.H = d.A; L.HW = d.w; L.HH = d.h;
      var sx = L.w * L.scale * mpp, sy = L.h * L.scale * mpp;
      var u = Object.assign({}, uniforms, { hmap: { value: d.tex }, cmap: { value: null }, wmap: { value: null }, hasW: { value: 0 }, texel: { value: new THREE.Vector2(1 / d.w, 1 / d.h) }, mppTex: { value: new THREE.Vector2(sx / d.w, sy / d.h) }, edge: { value: 0.08 }, lift: { value: 10 * exag } });
      if (L.tex.w) new THREE.TextureLoader().load(src + L.tex.w, function (wt) { wt.minFilter = wt.magFilter = THREE.LinearFilter; u.wmap.value = wt; u.hasW.value = 1; dirty = true; });
      new THREE.TextureLoader().load(src + L.tex.c, function (ct) {
        ct.colorSpace = THREE.SRGBColorSpace; ct.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy()); u.cmap.value = ct;
        var m = new THREE.ShaderMaterial({ uniforms: u, vertexShader: VS, fragmentShader: FS, transparent: true });
        var mesh = new THREE.Mesh(new THREE.PlaneGeometry(sx, sy, L.tex.seg[0], L.tex.seg[1]), m); mesh.frustumCulled = false;
        var c = toWorld(L.x0 + L.w * L.scale / 2, L.y0 + L.h * L.scale / 2, base); mesh.position.set(c.x, c.y, 0); mesh.renderOrder = 1; scene.add(mesh); L.mesh = mesh; dirty = true;
      });
    };
    img.src = src + L.tex.h;
  }
  function load() {
    if (started) return; started = true;
    var img = new Image(); img.decoding = "async";
    img.onload = function () {
      var d = decodeHeights(img), w = d.w, h = d.h; H = d.A; HW = w; HH = h;
      uniforms.hmap.value = d.tex; uniforms.texel.value.set(1 / w, 1 / h); uniforms.mppTex.value.set(sizeX / w, sizeY / h);
      if (TEX.w) new THREE.TextureLoader().load(src + TEX.w, function (wt) { wt.minFilter = wt.magFilter = THREE.LinearFilter; uniforms.wmap.value = wt; uniforms.hasW.value = 1; dirty = true; });
      new THREE.TextureLoader().load(src + TEX.c, function (ct) {
        ct.colorSpace = THREE.SRGBColorSpace; ct.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy()); uniforms.cmap.value = ct;
        var geo = new THREE.PlaneGeometry(sizeX, sizeY, TEX.seg[0], TEX.seg[1]);
        mesh = new THREE.Mesh(geo, material); mesh.frustumCulled = false; scene.add(mesh);
        buildTracks(); buildBorders(); if (free) showTracks(true);
        ready = true; dirty = true; s.classList.add("is-ready");
      });
    };
    img.src = src + TEX.h;
    cards.forEach(function (f) { var im = f.querySelector("img"); if (im) { im.loading = "eager"; if (im.decode) im.decode().catch(function () {}); } });
  }

  /* ---------- the camera: the flight, or the visitor's hands ---------- */
  var W = 1, Hh = 1, cur = -1, target = 0, free = false, blend = 0, blendFrom = null, dirty = true, raf = 0, lastP = -1;
  var O = { tgt: new THREE.Vector3(), dist: 10000, yaw: 0, pitch: 0.6, fov: 48 };     // the free pose, yaw 0 = camera south of its target, facing north
  var B = D.bounds, PITCH = [THREE.MathUtils.degToRad(B.pitch[0]), THREE.MathUtils.degToRad(B.pitch[1])], YAW = [THREE.MathUtils.degToRad(B.yaw[0]), THREE.MathUtils.degToRad(B.yaw[1])];
  var bSW = toWorld(B.sw[0], B.sw[1], 0), bNE = toWorld(B.ne[0], B.ne[1], 0);
  function freeCam() {
    var cp = Math.cos(O.pitch);
    var cam = new THREE.Vector3(O.tgt.x + O.dist * cp * Math.sin(O.yaw), O.tgt.y - O.dist * cp * Math.cos(O.yaw), O.tgt.z + O.dist * Math.sin(O.pitch));
    var minZ = groundZ(cam) + (B.alt_min - base) * exag * 0.3; if (cam.z < minZ) cam.z = minZ;
    return cam;
  }
  function clampFree(snap) {
    O.tgt.x = clamp(O.tgt.x, bSW.x, bNE.x); O.tgt.y = clamp(O.tgt.y, bSW.y, bNE.y);
    if (snap || O.tgt.z !== O.tgt.z) O.tgt.z = groundZ(O.tgt);
    O.dist = clamp(O.dist, B.dist[0], B.dist[1]); O.pitch = clamp(O.pitch, PITCH[0], PITCH[1]); O.yaw = clamp(O.yaw, YAW[0], YAW[1]);
  }
  function settleZ() {                                   // the target's height eases to the ground under it: no bob over a ridge
    var gz = groundZ(O.tgt), dz = gz - O.tgt.z; if (Math.abs(dz) < 0.5) { O.tgt.z = gz; return false; } O.tgt.z += dz * 0.14; return true;
  }
  function enterFree() {
    if (free) return; var p = poseAt(flightF); free = true; blend = 0; lastP = progress();
    O.tgt.copy(p.tgt); var v = p.cam.clone().sub(p.tgt); O.dist = v.length(); O.pitch = Math.asin(clamp(v.z / O.dist, -1, 1)); O.yaw = Math.atan2(v.x, -v.y); O.fov = p.fov;
    clampFree(true); s.classList.add("is-free"); if (ctl) ctl.textContent = ctl.getAttribute("data-back"); showTracks(true); dirty = true; requestAnimationFrame(measureKeep);
  }
  function leaveFree() {
    if (!free) return; blendFrom = currentPose(); free = false; blend = 1; glide = null; s.classList.remove("is-free"); if (ctl) ctl.textContent = ctl.getAttribute("data-take"); showTracks(false); dirty = true; requestAnimationFrame(measureKeep);
  }
  var flightF = 0;
  function portrait(p) {                                 // a tall screen sees a narrow slice: stand back and open the lens
    if (W >= Hh) return p;
    var v = p.cam.clone().sub(p.tgt).multiplyScalar(1.45); p.cam = p.tgt.clone().add(v); p.fov = Math.min(82, p.fov * 1.3);
    var k = 0; while (k++ < 12 && p.cam.z < groundZ(p.cam) + (B.alt_min - base) * exag * 0.3) { p.cam.z += 250 * exag; }
    return p;
  }
  function currentPose() {
    if (free) { var cam = freeCam(), fp = poseAt(flightF), dd = cam.distanceTo(O.tgt);   // the haze opens with the distance, so a far view still shows the ground
      return portrait({ cam: cam, tgt: O.tgt.clone(), fov: O.fov, fog0: Math.max(9000, fp.fog0 * 0.6, dd * 0.9), fog1: Math.max(60000, fp.fog1 * 0.8, dd * 3.2), leg: fp.leg, sun: fp.sun, free: true }); }
    var p = poseAt(flightF);
    if (blend > 0 && blendFrom) { var t = smooth(1 - blend); p.cam.lerp(blendFrom.cam, 1 - t); p.tgt.lerp(blendFrom.tgt, 1 - t); p.fov = lerp(blendFrom.fov, p.fov, t); }
    return portrait(p);
  }

  /* ---------- the hands: the ground follows the finger; pinch comes closer; two fingers twist to turn and
     slide to tilt; the right button or the on-screen buttons do the same with a mouse ---------- */
  var ptrs = {}, grab = null, vel = [0, 0], lastMove = 0, two = null;
  var rcNd = new THREE.Vector2(), rc = new THREE.Raycaster();
  function rayGround(px, py, planeZ) {                      // where the pointer's ray meets the horizontal plane at planeZ
    var nd = rcNd.set(px / W * 2 - 1, -(py / Hh) * 2 + 1); rc.setFromCamera(nd, camera);
    var o = rc.ray.origin, d = rc.ray.direction; if (Math.abs(d.z) < 1e-4) return null;
    var t = (planeZ - o.z) / d.z; if (t <= 0) return null; return o.clone().addScaledVector(d, t);
  }
  function groundUnder(px, py) {                             // the terrain under the pointer: march the ray against the heights
    var nd = rcNd.set(px / W * 2 - 1, -(py / Hh) * 2 + 1); rc.setFromCamera(nd, camera);
    var o = rc.ray.origin, d = rc.ray.direction, step = 150, pos = o.clone(), last = o.clone();
    for (var i = 0; i < 1200; i++) { last.copy(pos); pos.addScaledVector(d, step); if (pos.z < groundZ(pos)) { return last.lerp(pos, 0.5); } if (pos.z < -1000) break; step = Math.min(600, step * 1.03); }
    return null;
  }
  function panTo(p0, px, py) {                               // move the target so the grabbed point p0 sits under the pointer again
    var p1 = rayGround(px, py, p0.z); if (!p1) return;
    O.tgt.x += p0.x - p1.x; O.tgt.y += p0.y - p1.y; clampFree(); dirty = true;
  }
  function pan(dx, dy) {                                     // keyboard and buttons: a step across the ground
    var p = currentPose(), k = 2 * p.cam.distanceTo(p.tgt) * Math.tan(THREE.MathUtils.degToRad(p.fov / 2)) / Hh;
    var fwd = new THREE.Vector3(Math.sin(O.yaw), Math.cos(O.yaw), 0), right = new THREE.Vector3(fwd.y, -fwd.x, 0);
    O.tgt.addScaledVector(fwd, dy * k).addScaledVector(right, -dx * k); clampFree(); dirty = true;
  }
  function orbit(dx, dy) { O.yaw += dx * 0.005; O.pitch += dy * 0.005; clampFree(); dirty = true; }
  function zoom(k, px, py) {                                  // closer or further; with a pointer, towards the ground under it
    var at = (px !== undefined) ? groundUnder(px, py) : null;
    O.dist *= k; if (at) { O.tgt.x += (at.x - O.tgt.x) * (1 - k); O.tgt.y += (at.y - O.tgt.y) * (1 - k); } clampFree(); dirty = true;
  }
  function local(e) { var r = map.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
  map.addEventListener("pointerdown", function (e) {
    if (e.target.closest && e.target.closest(".v4i-fl-mk, .v4i-fl-lm, .v4i-fl-ab, .v4i-fl-btn, .v4i-fl-tk, .v4i-fl-tcard, .v4i-fl-card.is-on")) return;
    var l0 = local(e); tap = { g: lifeAt(l0[0], l0[1]), x: l0[0], y: l0[1], t: performance.now() };   // a figure under the finger: a tap opens its story, a drag still drags
    if (coarse && !free) return;                             // a finger scrolls the page until the controls are taken
    var l = local(e); ptrs[e.pointerId] = { x: l[0], y: l[1], sx: l[0], sy: l[1], b: e.button };
    var ids = Object.keys(ptrs);
    if (ids.length === 1) { grab = { p0: free ? groundUnder(l[0], l[1]) : null, moved: 0, mode: (e.button === 2 || e.ctrlKey || e.shiftKey) ? "orbit" : "pan" }; vel = [0, 0]; }
    if (ids.length === 2) { var A = ptrs[ids[0]], B2 = ptrs[ids[1]]; two = { span: Math.hypot(A.x - B2.x, A.y - B2.y), ang: Math.atan2(B2.y - A.y, B2.x - A.x), cy: (A.y + B2.y) / 2 }; grab = null; }
    map.setPointerCapture && map.setPointerCapture(e.pointerId);
    if (free) e.preventDefault();
  });
  map.addEventListener("pointermove", function (e) {
    var p = ptrs[e.pointerId]; if (!p) { if (!coarse) { var lh = local(e); lifeHover(lifeAt(lh[0], lh[1])); } return; }
    var l = local(e), dx = l[0] - p.x, dy = l[1] - p.y, ids = Object.keys(ptrs); p.x = l[0]; p.y = l[1];
    if (ids.length >= 2 && two) {
      var A = ptrs[ids[0]], B2 = ptrs[ids[1]], span = Math.hypot(A.x - B2.x, A.y - B2.y), ang = Math.atan2(B2.y - A.y, B2.x - A.x), cy = (A.y + B2.y) / 2;
      if (two.span > 0) zoom(two.span / Math.max(1, span));
      var da = ang - two.ang; if (da > Math.PI) da -= 2 * Math.PI; if (da < -Math.PI) da += 2 * Math.PI; O.yaw += da;
      O.pitch += (cy - two.cy) * 0.004;                      // two fingers sliding up tilt the view flatter, down more top-down
      two.span = span; two.ang = ang; two.cy = cy; clampFree(); dirty = true; e.preventDefault(); return;
    }
    if (!grab) return;
    grab.moved += Math.abs(dx) + Math.abs(dy);
    if (!free) { if (grab.moved > 6) { enterFree(); grab.p0 = groundUnder(p.sx, p.sy); } else return; }
    if (grab.mode === "orbit") orbit(dx, dy);
    else { if (!grab.p0) grab.p0 = groundUnder(l[0], l[1]); if (grab.p0) panTo(grab.p0, l[0], l[1]); var now = performance.now(), dt = Math.max(8, now - lastMove); vel = [dx / dt * 16, dy / dt * 16]; lastMove = now; }
    e.preventDefault();
  });
  function up(e) {
    if (tap && e.type === "pointerup") { var tg = tap; tap = null; if (tg.g && performance.now() - tg.t < 700) { var lu = local(e); if (Math.hypot(lu[0] - tg.x, lu[1] - tg.y) < 8) openDlg(tg.g.L.c); } }
    delete ptrs[e.pointerId]; var ids = Object.keys(ptrs);
    if (!ids.length) { if (grab && grab.mode === "pan" && free && performance.now() - lastMove < 80 && Math.hypot(vel[0], vel[1]) > 2) glide = vel.slice(); grab = null; two = null; }
    else if (ids.length === 1) { two = null; var q = ptrs[ids[0]]; grab = { p0: groundUnder(q.x, q.y), moved: 10, mode: "pan" }; }
  }
  var glide = null;
  function coast() {                                          // the ground keeps sliding a little after the finger lets go
    if (!glide || !free) { glide = null; return; }
    var p = currentPose(), k = 2 * p.cam.distanceTo(p.tgt) * Math.tan(THREE.MathUtils.degToRad(p.fov / 2)) / Hh / Math.max(0.35, Math.cos(O.pitch));
    var fwd = new THREE.Vector3(Math.sin(O.yaw), Math.cos(O.yaw), 0), right = new THREE.Vector3(fwd.y, -fwd.x, 0);
    O.tgt.addScaledVector(fwd, glide[1] * k).addScaledVector(right, -glide[0] * k); clampFree(); dirty = true;
    glide[0] *= 0.9; glide[1] *= 0.9; if (Math.hypot(glide[0], glide[1]) < 0.3) glide = null;
  }
  map.addEventListener("pointerup", up); map.addEventListener("pointercancel", up); map.addEventListener("lostpointercapture", up);
  map.addEventListener("contextmenu", function (e) { if (free) e.preventDefault(); });
  map.addEventListener("wheel", function (e) { if (!free) return; e.preventDefault(); var l = local(e); zoom(Math.exp(clamp(e.deltaY, -60, 60) * 0.004), l[0], l[1]); }, { passive: false });
  if (ctl) ctl.addEventListener("click", function () { if (free) leaveFree(); else enterFree(); });
  [].slice.call(s.querySelectorAll(".v4i-fl-btn")).forEach(function (b) {
    b.addEventListener("click", function () { if (!free) enterFree(); var k = b.getAttribute("data-do");
      if (k === "in") zoom(0.72); else if (k === "out") zoom(1.38); else if (k === "left") { O.yaw -= 0.35; clampFree(); dirty = true; } else if (k === "right") { O.yaw += 0.35; clampFree(); dirty = true; }
      else if (k === "up") { O.pitch -= 0.15; clampFree(); dirty = true; } else if (k === "down") { O.pitch += 0.15; clampFree(); dirty = true; } });
  });
  s.addEventListener("keydown", function (e) {
    if (!free) return; var k = e.key;
    if (k === "ArrowLeft") pan(40, 0); else if (k === "ArrowRight") pan(-40, 0); else if (k === "ArrowUp") pan(0, -40); else if (k === "ArrowDown") pan(0, 40);
    else if (k === "+" || k === "=") zoom(0.8); else if (k === "-") zoom(1.25); else if (k === "Escape") leaveFree(); else return; e.preventDefault();
  });

  /* ---------- the pins and the photo markers: projected live, hidden behind the ground ---------- */
  var WP = D.waypoints, wpWorld = {};
  Object.keys(WP).forEach(function (c) { var w = WP[c]; wpWorld[c] = toWorld(w.px[0], w.px[1], w.elev); });
  function hidden(pt, cam) {                              // does the ground stand between the camera and the point
    var steps = 28, dx = (pt.x - cam.x) / steps, dy = (pt.y - cam.y) / steps, dz = (pt.z - cam.z) / steps, x = cam.x, y = cam.y, z = cam.z;
    for (var i = 1; i < steps - 1; i++) { x += dx; y += dy; z += dz; if (groundZ({ x: x, y: y }) > z + 40 * exag) return true; }
    return false;
  }
  var v3 = new THREE.Vector3();
  function project(pt) { v3.copy(pt).project(camera); return [(v3.x + 1) / 2 * W, (1 - v3.y) / 2 * Hh, v3.z > -1 && v3.z < 1]; }

  /* ---------- the tracks: real flights drawn on the ground when the controls are taken ---------- */
  var TR = D.tracks || [], trackObjs = [], activeTrack = -1, tkList = s.querySelector(".v4i-fl-tks"), tcard = s.querySelector(".v4i-fl-tcard");
  var trackMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xff7517), transparent: true, opacity: 0.55, fog: true, depthWrite: false });
  var trackMatOn = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xff7517), transparent: true, opacity: 1, fog: true, depthWrite: false });
  var trackMatDim = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xf6f4f4), transparent: true, opacity: 0.16, fog: true, depthWrite: false });
  var routeMat = new THREE.LineDashedMaterial({ color: new THREE.Color(0xf6f4f4), dashSize: 700, gapSize: 500, transparent: true, opacity: 0.6, depthTest: false, fog: false });
  var borderMat = new THREE.LineDashedMaterial({ color: new THREE.Color(0xf6f4f4), dashSize: 1800, gapSize: 1200, transparent: true, opacity: 0.42, depthTest: false, fog: true });
  function buildBorders() {                                // international borders from Natural Earth, dashed, a little above the ground
    (D.borders || []).forEach(function (bd) {
      var pts = bd.pts.map(function (q) { return toWorld(q[0], q[1], heightAt(q[0], q[1]) + 60); });
      if (pts.length < 2) return;
      var ln = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), borderMat); ln.computeLineDistances(); ln.renderOrder = 2; scene.add(ln);
    });
  }
  function buildTracks() {                                 // a flight is drawn in the pieces that lie on the map
    TR.forEach(function (t, i) {
      var grp = new THREE.Group(), all = [];
      (t.segs || [t.points]).forEach(function (seg) {
        var pts = seg.map(function (q) { return toWorld(q[0], q[1], q[2]); }); if (pts.length < 2) return;
        var curve = new THREE.CatmullRomCurve3(pts, false, "centripetal", 0.5);
        var geo = new THREE.TubeGeometry(curve, Math.min(1200, pts.length * 2), 45, 5, false);
        var m = new THREE.Mesh(geo, trackMat); m.renderOrder = 2; grp.add(m); all = all.concat(pts);
      });
      if (!all.length) return;
      grp.visible = false; scene.add(grp);
      var o = { mesh: grp, start: all[0], end: all[all.length - 1], box: new THREE.Box3().setFromPoints(all), route: null };
      if (t.route && t.route.length === 5) {                 // the scored route: the triangle's three legs, or the four legs of a free flight
        var rp = t.route.map(function (q) { return toWorld(q[0], q[1], q[2] + 150); }), tri = t.type !== "free flight";
        var ln = new THREE.Line(new THREE.BufferGeometry().setFromPoints(tri ? [rp[1], rp[2], rp[3], rp[1]] : rp), routeMat);
        ln.computeLineDistances(); ln.renderOrder = 3; ln.visible = false; scene.add(ln); o.route = ln;
      }
      trackObjs.push(o);
    });
  }
  function niceDate(d) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d || ""); if (!m) return d || ""; return (+m[3]) + " " + ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][+m[2] - 1] + " " + m[1]; }
  function showTracks(on) { trackObjs.forEach(function (o) { o.mesh.visible = on; }); if (tkList) tkList.hidden = !on || !TR.length; if (!on) setTrack(-1); dirty = true; }
  function setTrack(i) {
    activeTrack = i; s.classList.toggle("is-tracked", i >= 0);   // a flight chosen: the page steps back, the ground and the line stay
    trackObjs.forEach(function (o, k) { var mat = i < 0 ? trackMat : (k === i ? trackMatOn : trackMatDim); o.mesh.children.forEach(function (m) { m.material = mat; }); if (o.route) o.route.visible = free && k === i; });
    [].slice.call(s.querySelectorAll(".v4i-fl-tk")).forEach(function (b, k) { b.classList.toggle("is-on", k === i); b.setAttribute("aria-pressed", k === i ? "true" : "false"); });
    if (tcard) { if (i < 0) { tcard.hidden = true; } else { var t = TR[i];
      tcard.querySelector(".v4i-fl-tn").textContent = t.name; tcard.querySelector(".v4i-fl-td").textContent = niceDate(t.date);
      tcard.querySelector(".v4i-fl-tkm b").textContent = t.distance_km.toLocaleString("en-GB", { maximumFractionDigits: 0 });
      tcard.querySelector(".v4i-fl-tkm span").textContent = "km \u00b7 " + (t.closed ? "closed " : "") + t.type;
      tcard.querySelector(".v4i-fl-tsp b").textContent = t.avg_kmh.toLocaleString("en-GB", { maximumFractionDigits: 1 });
      var note = tcard.querySelector(".v4i-fl-tnote"); if (note) note.textContent = t.ground_km.toLocaleString("en-GB", { maximumFractionDigits: 0 }) + " km flown over the ground" +
        (t.off_map && t.off_map.km >= 1 ? ", " + t.off_map.km.toLocaleString("en-GB", { maximumFractionDigits: 0 }) + " km of it " + t.off_map.side + " of the map" : "") +
        (t.points ? " \u00b7 " + t.points.toLocaleString("en-GB", { maximumFractionDigits: 1 }) + " points by the XContest rules" : "");
      tcard.querySelector(".v4i-fl-tal b").textContent = t.max_alt_m.toLocaleString("en-GB");
      tcard.querySelector(".v4i-fl-tdu b").textContent = Math.floor(t.duration_min / 60) + "h " + (t.duration_min % 60) + "m"; tcard.hidden = false; } }
    dirty = true;
  }
  function flyToTrack(i) {                                   // frame the whole flight from the south
    var o = trackObjs[i]; if (!o) return; if (!free) enterFree();
    var c = o.box.getCenter(new THREE.Vector3()), sz = o.box.getSize(new THREE.Vector3());
    O.tgt.set(c.x, c.y, 0); O.tgt.z = groundZ(O.tgt); O.yaw = 0; O.pitch = THREE.MathUtils.degToRad(38);
    O.dist = clamp(Math.max(sz.x, sz.y * 1.4) * 0.9 / Math.tan(THREE.MathUtils.degToRad(O.fov / 2)) * 0.6, B.dist[0], B.dist[1]); clampFree(true); dirty = true;
  }
  if (tkList) [].slice.call(tkList.querySelectorAll(".v4i-fl-tk")).forEach(function (b, i) { b.addEventListener("click", function () { if (activeTrack === i) { setTrack(-1); return; } setTrack(i); flyToTrack(i); }); });
  if (tcard) { var tx = tcard.querySelector(".v4i-fl-tx"); if (tx) tx.addEventListener("click", function () { setTrack(-1); }); }

  /* ---------- the dialog: the photographs of a place ---------- */
  function openDlg(code) {
    if (!dlg) return;
    var grp = null;
    [].slice.call(dlg.querySelectorAll(".v4i-fl-dg")).forEach(function (g) { var on = g.getAttribute("data-c") === code; g.hidden = !on; if (on) grp = g; });
    if (!grp) return;
    var ttl = dlg.querySelector(".v4i-fl-dt"); if (ttl) ttl.textContent = grp.getAttribute("data-t") || WP[code].label;
    dlg.classList.toggle("is-text", !grp.querySelector("figure"));
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
  }
  mks.forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); openDlg(b.getAttribute("data-c")); }); });
  /* a landmark: its name is the button, a dotted line under it the hint; no ring */
  var lmBtn = {};
  [].slice.call(s.querySelectorAll(".v4i-fl-lm")).forEach(function (b) {
    var c = b.getAttribute("data-c"), g = pls.filter(function (q) { return q.getAttribute("data-c") === c; })[0]; if (!g) return;
    lmBtn[c] = b;
    var ln = document.createElementNS("http://www.w3.org/2000/svg", "line"); ln.setAttribute("class", "v4i-fl-ul"); ln.setAttribute("y1", "9"); ln.setAttribute("y2", "9"); g.appendChild(ln); g._ul = ln;
    b.addEventListener("pointerenter", function () { g.classList.add("is-hot"); }); b.addEventListener("pointerleave", function () { g.classList.remove("is-hot"); });
    b.addEventListener("focus", function () { g.classList.add("is-hot"); }); b.addEventListener("blur", function () { g.classList.remove("is-hot"); });
    b.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); openDlg(c); });
  });
  if (dlg) { var cl = dlg.querySelector(".v4i-fl-dx"); if (cl) cl.addEventListener("click", function () { dlg.close(); }); dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); }); }

  /* ---------- the lightbox: a photograph floating on the dimmed page; wheel or pinch to zoom, drag to move ---------- */
  var lb = document.getElementById("v4i-fl-lb"), lbImg = lb && lb.querySelector("img"), lbStage = lb && lb.querySelector(".v4i-fl-lbs"), lbCap = lb && lb.querySelector(".v4i-fl-lbc");
  var lbPrev = lb && lb.querySelector(".v4i-fl-lbp"), lbNext = lb && lb.querySelector(".v4i-fl-lbnx");
  var Z = { s: 1, x: 0, y: 0, ptrs: {}, pinch: null, moved: 0, closing: 0, set: [], i: 0 };
  function lbApply() { lbImg.style.transform = (lb.classList.contains("is-in") ? "" : "scale(.96) ") + "translate(" + Z.x.toFixed(1) + "px," + Z.y.toFixed(1) + "px) scale(" + Z.s.toFixed(3) + ")"; lb.classList.toggle("is-zoomed", Z.s > 1.01); }
  function lbClampPan() {
    var iw = lbImg.clientWidth, ih = lbImg.clientHeight, sw = lbStage.clientWidth, sh = lbStage.clientHeight;
    var mx = Math.max(0, (iw * Z.s - sw) / 2 + 24), my = Math.max(0, (ih * Z.s - sh) / 2 + 24);
    if (iw * Z.s <= sw) mx = 0; if (ih * Z.s <= sh) my = 0; Z.x = clamp(Z.x, -mx, mx); Z.y = clamp(Z.y, -my, my);
  }
  function lbZoomAt(k, cx, cy) {                           // the point under the pointer stays put
    var r = lbStage.getBoundingClientRect(), px = cx - (r.left + r.width / 2), py = cy - (r.top + r.height / 2), s1 = clamp(Z.s * k, 1, 6), ratio = s1 / Z.s;
    Z.x = px - ratio * (px - Z.x); Z.y = py - ratio * (py - Z.y); Z.s = s1; if (Z.s <= 1.001) { Z.x = Z.y = 0; } lbClampPan(); lbApply();
  }
  function lbShow(im) {                                      // the photograph, its title, and where it sits in its set
    var fig = im.closest && im.closest("figure"), cap = fig && fig.querySelector("figcaption b");
    Z.s = 1; Z.x = Z.y = 0; lb.classList.remove("is-zoomed", "is-drag"); lbImg.src = im.src; lbImg.alt = im.alt || "";
    if (lbCap) { lbCap.textContent = cap ? cap.textContent : ""; if (Z.set.length > 1) { var k = document.createElement("span"); k.className = "v4i-fl-lbi"; k.textContent = (Z.i + 1) + " / " + Z.set.length; lbCap.appendChild(k); } }
    if (lbPrev) lbPrev.hidden = Z.i <= 0; if (lbNext) lbNext.hidden = Z.i >= Z.set.length - 1;
    lbApply();
  }
  function lbOpen(im, set) {
    if (!lb || !lbImg) return;
    Z.set = (set && set.length) ? set : [im]; Z.i = Math.max(0, Z.set.indexOf(im)); Z.ptrs = {}; Z.pinch = null; lb.classList.remove("is-in"); lbImg.style.transform = "";
    lbShow(im);
    if (lb.showModal) lb.showModal(); else lb.setAttribute("open", "");
    requestAnimationFrame(function () { requestAnimationFrame(function () { lb.classList.add("is-in"); lbApply(); }); });
  }
  function lbGo(d) {                                          // the next or the previous of the set, with a short fade
    var j = Z.i + d; if (!lb.open || j < 0 || j >= Z.set.length) return; Z.i = j;
    lbImg.style.opacity = "0";
    setTimeout(function () { lbShow(Z.set[Z.i]); var done = function () { lbImg.style.opacity = ""; }; if (lbImg.complete) done(); else { lbImg.onload = done; setTimeout(done, 900); } }, 160);
  }
  function lbClose() {
    if (!lb || !lb.open || Z.closing) return; Z.closing = 1; lb.classList.remove("is-in");
    setTimeout(function () { if (lb.open) lb.close(); lbImg.removeAttribute("src"); lb.classList.remove("is-zoomed", "is-drag"); Z.closing = 0; }, 220);
  }
  if (lb) {
    var plateImgs = cards.map(function (c) { return c.querySelector("img"); }).filter(Boolean), rowImgs = [].slice.call(document.querySelectorAll(".v4i-fl-row figure img"));
    cards.forEach(function (card) { card.addEventListener("click", function (e) { if (!card.classList.contains("is-on")) return; var im = card.querySelector("img"); if (im) { e.preventDefault(); e.stopPropagation(); lbOpen(im, plateImgs); } }); });
    rowImgs.forEach(function (im) { im.addEventListener("click", function (e) { e.preventDefault(); lbOpen(im, rowImgs); }); });
    if (lbPrev) lbPrev.addEventListener("click", function (e) { e.stopPropagation(); lbGo(-1); if (lbPrev.hidden) lb.focus(); }); if (lbNext) lbNext.addEventListener("click", function (e) { e.stopPropagation(); lbGo(1); if (lbNext.hidden) lb.focus(); });
  }
  if (dlg && lb) {
    dlg.addEventListener("click", function (e) { var im = e.target && e.target.closest && e.target.closest(".v4i-fl-dg img"); if (im) { e.preventDefault(); e.stopPropagation(); var grp = im.closest(".v4i-fl-dg"); lbOpen(im, grp ? [].slice.call(grp.querySelectorAll("img")) : null); } }, true);
    lb.addEventListener("cancel", function (e) { e.preventDefault(); lbClose(); });
    lb.querySelector(".v4i-fl-lbx").addEventListener("click", function (e) { e.stopPropagation(); lbClose(); });
    lb.addEventListener("click", function (e) {
      if (e.target.closest(".v4i-fl-lbx, .v4i-fl-lbn")) return;
      if (Z.moved > 6) { Z.moved = 0; return; }                              // the end of a drag is not a click
      var r = lbImg.getBoundingClientRect(), onImg = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;   // the pointer capture makes the stage the target
      if (onImg) { var next = Z.s < 1.5 ? 2 : Z.s < 3 ? 3.5 : 1; lbZoomAt(next / Z.s, e.clientX, e.clientY); return; }   // closer, closer, back out
      lbClose();
    });
    lb.addEventListener("wheel", function (e) { e.preventDefault(); lbZoomAt(Math.exp(-clamp(e.deltaY, -80, 80) * 0.004), e.clientX, e.clientY); }, { passive: false });
    lbStage.addEventListener("pointerdown", function (e) {
      Z.ptrs[e.pointerId] = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY, t: performance.now() }; var ids = Object.keys(Z.ptrs); Z.moved = 0;
      if (ids.length === 2) { var A = Z.ptrs[ids[0]], B2 = Z.ptrs[ids[1]]; Z.pinch = { span: Math.hypot(A.x - B2.x, A.y - B2.y), cx: (A.x + B2.x) / 2, cy: (A.y + B2.y) / 2 }; }
      lbStage.setPointerCapture && lbStage.setPointerCapture(e.pointerId); if (e.target === lbImg && Z.s > 1.01) lb.classList.add("is-drag"); e.preventDefault();
    });
    lbStage.addEventListener("pointermove", function (e) {
      var p = Z.ptrs[e.pointerId]; if (!p) return; var dx = e.clientX - p.x, dy = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY; Z.moved += Math.abs(dx) + Math.abs(dy);
      var ids = Object.keys(Z.ptrs);
      if (ids.length >= 2 && Z.pinch) {
        var A = Z.ptrs[ids[0]], B2 = Z.ptrs[ids[1]], span = Math.hypot(A.x - B2.x, A.y - B2.y), cx = (A.x + B2.x) / 2, cy = (A.y + B2.y) / 2;
        if (Z.pinch.span > 0) lbZoomAt(span / Math.max(1, Z.pinch.span), cx, cy);
        Z.x += cx - Z.pinch.cx; Z.y += cy - Z.pinch.cy; Z.pinch.span = span; Z.pinch.cx = cx; Z.pinch.cy = cy; lbClampPan(); lbApply(); return;
      }
      if (Z.s > 1.01) { Z.x += dx; Z.y += dy; lbClampPan(); lbApply(); }
    });
    function lbUp(e) {
      var p = Z.ptrs[e.pointerId]; delete Z.ptrs[e.pointerId]; var ids = Object.keys(Z.ptrs); if (ids.length < 2) Z.pinch = null; lb.classList.remove("is-drag");
      if (p && !ids.length && Z.s <= 1.01 && !Z.pinch) { var dx = e.clientX - p.sx, dy = e.clientY - p.sy; if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) lbGo(dx < 0 ? 1 : -1); }   // a swipe when not zoomed
    }
    lbStage.addEventListener("pointerup", lbUp); lbStage.addEventListener("pointercancel", lbUp);
    document.addEventListener("keydown", function (e) { if (!lb.open) return; if (e.key === "+" || e.key === "=") lbZoomAt(1.3, innerWidth / 2, innerHeight / 2); else if (e.key === "-") lbZoomAt(1 / 1.3, innerWidth / 2, innerHeight / 2); else if (e.key === "0") lbZoomAt(1 / Z.s, 0, 0); else if (e.key === "ArrowRight") { e.preventDefault(); lbGo(1); } else if (e.key === "ArrowLeft") { e.preventDefault(); lbGo(-1); } });
  }

  /* ---------- the frame ---------- */

  /* ---------- the life: elephants, flamingos, runners, cattle, baobabs; emoji figures that keep to their ground, drift a little, and open their place's story ---------- */
  var NS = "http://www.w3.org/2000/svg", LIFE = D.life || [], LREACH = (D.lifeKm || 60) * 1000, lifeOn = false, lifeT = 0, lifeFr = 0, tap = null, hotG = null;
  var calm = mq("(prefers-reduced-motion: reduce)").matches, mksBox = s.querySelector(".v4i-fl-mks");
  /* per kind: height against the others, pace in metres a second (brisk, so the drift shows from the air), spacing in metres, which way the drawing faces (-1 left, 1 right, 0 either) */
  var KIND = { elephant: [1, 110, 700, -1], giraffe: [1.25, 120, 650, -1], zebra: [.9, 150, 420, -1], rhino: [.95, 70, 900, -1], hippo: [.85, 40, 380, -1], buffalo: [.95, 100, 440, -1], lion: [.8, 50, 700, 0],
               flamingo: [.8, 30, 170, -1], runner: [.9, 260, 320, 1], cattle: [.9, 80, 380, -1], walker: [.9, 80, 300, 1], crocodile: [.8, 20, 500, 1], baobab: [1.5, 0, 1600, 0] };
  function rng(seed) { return function () { seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  var lifeG = LIFE.map(function (L, gi) {
    var k = KIND[L.kind] || KIND.elephant, r = rng(gi * 7919 + 17), n = L.n || 1, sp = k[2], still = L.mode === "still";
    var hr = still ? (L.km || 3) * 1000 : sp * Math.sqrt(n) * 0.75, R = Math.max((L.km || 2) * 1000, hr * 1.4);   // the ground a group spreads over, and the ground it roams
    var a = toWorld(L.px[0], L.px[1], base), el = document.createElementNS(NS, "g"); el.setAttribute("class", "v4i-fl-an is-" + L.kind); el.style.display = "none"; ov.appendChild(el);
    var ms = [], homes = [];
    for (var i = 0; i < n; i++) {
      var hx = 0, hy = 0, ok = false, tries = 0;
      while (!ok && tries++ < 60) { var ang = r() * 6.2832, rad = Math.sqrt(r()) * hr; hx = Math.cos(ang) * rad; hy = Math.sin(ang) * rad; ok = true; for (var q = 0; q < homes.length; q++) if (Math.hypot(homes[q][0] - hx, homes[q][1] - hy) < sp * 0.7) { ok = false; break; } }
      homes.push([hx, hy]);
      var u = document.createElementNS(NS, "use"); u.setAttribute("href", "#v4i-em-" + L.kind); u.setAttribute("width", "128"); u.setAttribute("height", "128"); u.style.display = "none"; el.appendChild(u);   // a symbol fills its use: give it the drawing's own size
      ms.push({ el: u, hx: hx, hy: hy, x: hx, y: hy, th: r() * 6.2832, ph: r() * 6.2832, w1: .25 + r() * .3, w2: .2 + r() * .3, face: r() < .5 ? -1 : 1, sc: still ? .75 + r() * .55 : .92 + r() * .16, hid: false, shown: false, sx: 0, sy: 0, hw: 0, hh: 0 });
    }
    var b = null;
    if (mksBox && WP[L.c]) {                                 // a small button at the group's middle, for keys and fingers; the figures themselves answer the pointer
      b = document.createElement("button"); b.className = "v4i-fl-ab"; b.type = "button"; b.hidden = true; b.setAttribute("aria-label", "About " + (L.name || L.kind) + " at " + WP[L.c].label);
      b.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); openDlg(L.c); });
      b.addEventListener("focus", function () { el.classList.add("is-hot"); }); b.addEventListener("blur", function () { el.classList.remove("is-hot"); }); mksBox.appendChild(b);
    }
    var to = L.to ? toWorld(L.to[0], L.to[1], base) : null, len = to ? Math.hypot(to.x - a.x, to.y - a.y) : 0;
    return { L: L, k: k, a: a, el: el, btn: b, ms: ms, cx: 0, cy: 0, th: r() * 6.2832, rot: 0, u: r() * len * 2, R: R, on: false, dir: to ? [(to.x - a.x) / len, (to.y - a.y) / len] : null, len: len };
  });
  var lv = new THREE.Vector3(), lv2 = new THREE.Vector3();
  function life(now) {
    var dt = lifeT ? Math.min(0.1, (now - lifeT) / 1000) : 0; lifeT = now; if (calm) dt = 0; lifeFr++;
    var t = now / 1000, cam = camera.position, any = false;
    lifeG.forEach(function (G) {
      var L = G.L, k = G.k, dist = Math.hypot(G.a.x - cam.x, G.a.y - cam.y, G.a.z - cam.z), on = dist < LREACH;
      if (on) { lv.set(G.a.x + G.cx, G.a.y + G.cy, G.a.z); var pr = project(lv); on = pr[2] && pr[0] > -120 && pr[0] < W + 120 && pr[1] > -120 && pr[1] < Hh + 120; }
      if (!on) { if (G.on) { G.on = false; G.el.style.display = "none"; if (G.btn) G.btn.hidden = true; G.ms.forEach(function (m) { m.shown = false; m.el.style.display = "none"; }); } return; }
      if (!G.on) { G.on = true; G.el.style.display = ""; G.a.z = groundZ(G.a); }
      any = true;
      var v = k[1], mode = L.mode || "herd";
      if (mode === "herd" || mode === "flock") {              // the group wanders, and turns back when it reaches the edge of its ground
        G.th += (Math.random() - .5) * 0.8 * dt; if (Math.hypot(G.cx, G.cy) > G.R) G.th = Math.atan2(-G.cy, -G.cx) + (Math.random() - .5) * 0.6;
        G.cx += Math.cos(G.th) * v * dt; G.cy += Math.sin(G.th) * v * dt; if (mode === "flock") G.rot += 0.05 * dt;
      } else if (mode === "line" && G.dir) G.u = (G.u + v * dt) % (2 * G.len);
      var hb = clamp((small ? 24 : 27) * Math.pow(16000 / Math.max(dist, 1500), 0.4), 12, 48) * k[0], fade = smooth(clamp((LREACH - dist) / (LREACH * 0.2), 0, 1)), chk = (lifeFr + G.ms.length) % 6 === 0 || !G.ms[0].shown;
      var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9, shownN = 0;
      G.ms.forEach(function (m, i) {
        var vx = 0, vy = 0;
        if (mode === "herd") { var A = k[2] * 0.35; m.x = G.cx + m.hx + A * Math.sin(t * m.w1 + m.ph); m.y = G.cy + m.hy + A * Math.cos(t * m.w2 + m.ph); vx = Math.cos(G.th) * v; vy = Math.sin(G.th) * v; }
        else if (mode === "flock") { var c = Math.cos(G.rot), sn = Math.sin(G.rot), A2 = k[2] * 0.3, rx = c * m.hx - sn * m.hy, ry = sn * m.hx + c * m.hy; m.x = G.cx + rx + A2 * Math.sin(t * m.w1 + m.ph); m.y = G.cy + ry + A2 * Math.cos(t * m.w2 + m.ph); vx = -ry * 0.05 + Math.cos(G.th) * v; vy = rx * 0.05 + Math.sin(G.th) * v; }
        else if (mode === "solo") {                              // each on its own: a walk, a pause, a turn
          var go = smooth(clamp((Math.sin(t * 0.12 + m.ph) + 0.5) / 1.2, 0, 1)); m.th += (Math.random() - .5) * 1.4 * dt; if (Math.hypot(m.x, m.y) > G.R) m.th = Math.atan2(-m.y, -m.x) + (Math.random() - .5) * 0.5;
          vx = Math.cos(m.th) * v * go; vy = Math.sin(m.th) * v * go; m.x += vx * dt; m.y += vy * dt;
        } else if (mode === "line" && G.dir) {                   // in single file along the road, out and back
          var uu = (G.u + i * k[2]) % (2 * G.len), fwd = uu < G.len, sg = fwd ? uu : 2 * G.len - uu; m.x = G.dir[0] * sg + m.hx * 0.15; m.y = G.dir[1] * sg + m.hy * 0.15; vx = G.dir[0] * (fwd ? v : -v); vy = G.dir[1] * (fwd ? v : -v);
        }
        var wx = G.a.x + m.x, wy = G.a.y + m.y, z = groundZ({ x: wx, y: wy });
        lv.set(wx, wy, z); var p1 = project(lv), sx = p1[0], sy = p1[1], inn = p1[2] && sx > -30 && sx < W + 30 && sy > -30 && sy < Hh + 30;
        if (inn && chk && H) m.hid = hidden(lv, cam);
        if (!inn || m.hid) { if (m.shown) { m.shown = false; m.el.style.display = "none"; } return; }
        if (vx || vy) { lv2.set(wx + vx * 2, wy + vy * 2, z); var p2 = project(lv2), dxs = p2[0] - sx; if (dxs > 0.15) m.face = 1; else if (dxs < -0.15) m.face = -1; }
        var hh = hb * m.sc, sc = hh / 128, fx = k[3] === 0 || m.face === k[3] ? 1 : -1;
        m.el.setAttribute("transform", "translate(" + sx.toFixed(1) + " " + sy.toFixed(1) + ") scale(" + (sc * fx).toFixed(4) + " " + sc.toFixed(4) + ") translate(-64 -118)");
        if (!m.shown) { m.shown = true; m.el.style.display = ""; } m.el.style.opacity = fade.toFixed(2);
        m.sx = sx; m.sy = sy; m.hw = hh * 0.5; m.hh = hh; if (sx - m.hw < x0) x0 = sx - m.hw; if (sx + m.hw > x1) x1 = sx + m.hw; if (sy - hh < y0) y0 = sy - hh; if (sy > y1) y1 = sy; shownN++;
      });
      if (G.btn) { if (!shownN) G.btn.hidden = true; else { G.btn.hidden = false; G.btn.style.transform = "translate(" + ((x0 + x1) / 2).toFixed(0) + "px," + ((y0 + y1) / 2).toFixed(0) + "px)"; } }
    });
    lifeOn = any;
  }
  function lifeAt(x, y) {                                     // the group whose figure is under the pointer
    for (var gi = 0; gi < lifeG.length; gi++) { var G = lifeG[gi]; if (!G.on) continue;
      for (var i = 0; i < G.ms.length; i++) { var m = G.ms[i]; if (m.shown && x > m.sx - m.hw - 4 && x < m.sx + m.hw + 4 && y > m.sy - m.hh - 4 && y < m.sy + 4) return G; } }
    return null;
  }
  function lifeHover(G) { if (G === hotG) return; if (hotG) hotG.el.classList.remove("is-hot"); hotG = G; if (G) G.el.classList.add("is-hot"); map.classList.toggle("is-hand", !!G); }
  function size() {
    var r = map.getBoundingClientRect(); W = Math.max(1, r.width); Hh = Math.max(1, r.height);
    dprHi = lite ? 1 : Math.min(1.5, window.devicePixelRatio || 1); dprLo = lite ? 1 : Math.max(0.7, dprHi * 0.66); dprNow = 0; setDpr(dprHi);
    camera.aspect = W / Hh; camera.updateProjectionMatrix();
    ov.setAttribute("viewBox", "0 0 " + W.toFixed(0) + " " + Hh.toFixed(0)); lead.setAttribute("viewBox", "0 0 " + W.toFixed(0) + " " + Hh.toFixed(0));
    pls.forEach(function (g) { var tx = g.querySelector("text"); g._tx = tx; try { g._tw = tx.getComputedTextLength() || tx.textContent.length * 7.3; } catch (e) { g._tw = tx.textContent.length * 7.3; } });
    last = {}; cards.forEach(function (f) { f._side = -1; f._w = f.offsetWidth; f._h = f.offsetHeight; }); dirty = true; measureKeep();
  }
  var dprHi = 1, dprLo = 1, dprNow = 0, lastR = 0, settleT = 0;
  function setDpr(d) { if (d === dprNow) return; dprNow = d; renderer.setPixelRatio(d); renderer.setSize(W, Hh, false); }
  function render() {
    var now = performance.now(), moving = now - lastR < 90; lastR = now;   // frames in quick succession: the view is moving
    setDpr(moving ? dprLo : dprHi); clearTimeout(settleT); if (moving) settleT = setTimeout(function () { lastR = 0; dirty = true; }, 170);
    var p = currentPose();
    camera.position.copy(p.cam); camera.lookAt(p.tgt); camera.fov = p.fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
    uniforms.fogNear.value = p.fog0; uniforms.fogFar.value = p.fog1; uniforms.camPos.value.copy(p.cam);
    if (p.sun) { var sa = THREE.MathUtils.degToRad(p.sun[0]), se = THREE.MathUtils.degToRad(p.sun[1]); uniforms.sunDir.value.set(Math.cos(se) * Math.sin(sa), Math.cos(se) * Math.cos(sa), Math.sin(se)).normalize(); }
    if (layers.length && ready) { var tg = gridOf(p.tgt); layers.forEach(function (L) { if (L.started) return; var qx = clamp(tg[0], L.x0, L.x1), qy = clamp(tg[1], L.y0, L.y1); if (Math.hypot(qx - tg[0], qy - tg[1]) * mpp < L.near) loadLayer(L); }); }
    if (ready) renderer.render(scene, camera);
    var dist = p.cam.distanceTo(p.tgt), km = 2 * dist * Math.tan(THREE.MathUtils.degToRad(p.fov / 2)) * (W / Hh) / 1000;
    put("km", Math.round(km), function (v) { if (kmEl) kmEl.textContent = v; });
    put("alt", Math.round((p.cam.z / exag + base) / 50) * 50, function (v) { if (altEl) altEl.textContent = v.toLocaleString("en-GB"); });
    put("ch", D.chapter[p.leg], function (v) { chs.forEach(function (el, k) { el.classList.toggle("is-on", k === v); }); KR.ch = rectOf(s.querySelector(".v4i-fl-c.is-on")); });
    var top = KR.top, fy1 = Hh - (small ? 20 : 150), f = flightF;
    /* the plates, only on the flight */
    var lit = null, lw = 0, cardBoxes = [];
    cards.forEach(function (card, k) {
      var cd = D.cards[k], w = free ? 0 : Math.min(1, (f - cd.a) / 1.6, (cd.b - f) / 1.6); w = w < 0 ? 0 : w; w = smooth(w);
      if (w <= 0) { put("w" + k, "0", function () { card.style.setProperty("--w", "0"); card.classList.remove("is-on"); card._side = -1; }); return; }
      var pt = wpWorld[cd.c], pr = project(pt); if (!pr[2]) { put("w" + k, "0", function () { card.style.setProperty("--w", "0"); card.classList.remove("is-on"); }); return; }
      var ax = pr[0], ay = pr[1], off = ax < 6 || ax > W - 6 || ay < 6 || ay > Hh - 6; ax = clamp(ax, 6, W - 6); ay = clamp(ay, 6, Hh - 6);
      var cw = card._w || (card._w = card.offsetWidth), chh = card._h || (card._h = card.offsetHeight), g = 44, x, y, gut = KR.gut;
      var keepR = [KR.ch, KR.read, KR.ctl].filter(Boolean), fx0 = gut, fy0 = top, fx1 = W - gut, fy1c = Hh - (small ? 20 : 170);
      function clear(rx, ry) { for (var q = 0; q < keepR.length; q++) { var o = keepR[q]; if (rx < o[2] && rx + cw > o[0] && ry < o[3] && ry + chh > o[1]) return false; } return true; }
      function covers(rx, ry) { return ax > rx - 18 && ax < rx + cw + 18 && ay > ry - 18 && ay < ry + chh + 18; }   // the plate must never sit on its own pin
      if (small) {                                           // a phone: four slots, under the head or above the chapter, left or right; the first that is clear of the pin
        var botY = Math.max(fy0 + 6, (KR.ch ? KR.ch[1] : fy1c) - chh - 8), slots = [[gut, fy0 + 6], [W - gut - cw, fy0 + 6], [gut, botY], [W - gut - cw, botY]];
        if (card._side < 0 || covers(slots[card._side][0], slots[card._side][1]) || !clear(slots[card._side][0], slots[card._side][1])) {
          card._side = -2; for (var qs = 0; qs < 4; qs++) { if (clear(slots[qs][0], slots[qs][1]) && !covers(slots[qs][0], slots[qs][1])) { card._side = qs; break; } }
          if (card._side < 0) { var bd2 = -1; for (var qt = 0; qt < 4; qt++) { var dd = Math.hypot(slots[qt][0] + cw / 2 - ax, slots[qt][1] + chh / 2 - ay); if (dd > bd2) { bd2 = dd; card._side = qt; } } }
        }
        x = slots[card._side][0]; y = slots[card._side][1];
      } else {
        var cand = [[ax - g - cw, ay - g - chh], [ax + g, ay - g - chh], [ax - g - cw, ay + g], [ax + g, ay + g]];
        function fits(cc) { return cc[0] >= fx0 && cc[1] >= fy0 && cc[0] + cw <= fx1 && cc[1] + chh <= fy1c; }
        function at(q) { return [clamp(cand[q][0], fx0, fx1 - cw), clamp(cand[q][1], fy0, fy1c - chh)]; }
        if (card._side < 0 || covers(at(card._side)[0], at(card._side)[1])) {
          card._side = -2;
          for (var q = 0; q < 4; q++) { var cc = cand[q]; if (fits(cc) && clear(cc[0], cc[1]) && !covers(cc[0], cc[1])) { card._side = q; break; } }
          if (card._side < 0) for (var q1 = 0; q1 < 4; q1++) { var c1 = at(q1); if (clear(c1[0], c1[1]) && !covers(c1[0], c1[1])) { card._side = q1; break; } }
          if (card._side < 0) for (var q3 = 0; q3 < 4; q3++) { var c3 = at(q3); if (!covers(c3[0], c3[1])) { card._side = q3; break; } }
          if (card._side < 0) card._side = 0;
        }
        var pos = at(card._side); x = pos[0]; y = pos[1];
        if (!clear(x, y)) { for (var q2 = 0; q2 < keepR.length; q2++) { var o2 = keepR[q2]; if (x < o2[2] && x + cw > o2[0] && y < o2[3] && y + chh > o2[1]) {
          var yy = o2[1] - chh - 8; if (yy >= fy0 && !covers(x, yy)) y = yy; else if (o2[2] + 8 + cw <= fx1 && !covers(o2[2] + 8, y)) x = o2[2] + 8; else if (o2[0] - 8 - cw >= fx0 && !covers(o2[0] - 8 - cw, y)) x = o2[0] - 8 - cw; else y = Math.max(fy0, yy); } } }   // above it, else beside it
        if (covers(x, y)) {                                  // still on the pin after the clamps: slide off sideways, else vertically
          if (ax + g + cw <= fx1) x = ax + g; else if (ax - g - cw >= fx0) x = ax - g - cw;
          else if (ay + g + chh <= fy1c) y = ay + g; else if (ay - g - chh >= fy0) y = ay - g - chh;
        }
      }
      if (w > .05) cardBoxes.push([x - 6, y - 6, x + cw + 6, y + chh + 6]);
      put("w" + k, w.toFixed(3), function (v) { card.style.setProperty("--w", v); card.classList.toggle("is-on", parseFloat(v) > 0.5); });
      put("x" + k, x.toFixed(1) + "|" + y.toFixed(1), function () { card.style.setProperty("--x", x.toFixed(1) + "px"); card.style.setProperty("--y", y.toFixed(1) + "px"); });
      if (w > lw) { lw = w; var cs = [[x, y], [x + cw, y], [x, y + chh], [x + cw, y + chh]], bc = cs[0], bdd = 1e9; cs.forEach(function (q) { var d = Math.hypot(q[0] - ax, q[1] - ay); if (d < bdd) { bdd = d; bc = q; } }); lit = { ax: ax, ay: ay, bx: bc[0], by: bc[1], w: w, off: off, near: cd.near }; }
    });
    put("lit", lit ? [lit.ax.toFixed(1), lit.ay.toFixed(1), lit.bx.toFixed(1), lit.by.toFixed(1), lit.w.toFixed(3), lit.off ? 1 : 0, lit.near ? 1 : 0].join("|") : "", function () {
      if (!lit) { tie.style.opacity = dot.style.opacity = halo.style.opacity = "0"; return; }
      var o = (lit.w * (lit.off ? .35 : 1)).toFixed(3); tie.setAttribute("x1", lit.ax); tie.setAttribute("y1", lit.ay); tie.setAttribute("x2", lit.bx); tie.setAttribute("y2", lit.by); tie.style.opacity = o;
      dot.setAttribute("cx", lit.ax); dot.setAttribute("cy", lit.ay); dot.style.opacity = o; halo.setAttribute("cx", lit.ax); halo.setAttribute("cy", lit.ay); halo.classList.toggle("is-near", !!lit.near); halo.setAttribute("r", lit.near ? 14 : 9); halo.style.opacity = (lit.w * (lit.near ? .22 : .8) * (lit.off ? .35 : 1)).toFixed(3);
    });
    /* the pins: priority order, in frame, near enough, not behind the ground, not on another label or a plate */
    var best = null, bd = 99, boxes = cardBoxes.slice(), shown = 0, cx = W / 2, cy = Hh / 2, keep = [KR.ch, KR.read, KR.ctl, KR.head].filter(Boolean);
    boxes = boxes.concat(keep);
    function inKeep(x, y) { for (var q = 0; q < keep.length; q++) { var o = keep[q]; if (x > o[0] && x < o[2] && y > o[1] && y < o[3]) return true; } return false; }
    pls.forEach(function (g) {
      var c = g.getAttribute("data-c"), pt = wpWorld[c], pr = project(pt), dist = pt.distanceTo(p.cam), x = pr[0], y = pr[1], tw = g._tw || 60, show = false, side = 0, far = false;
      var town = g.classList.contains("is-town"), story = g.classList.contains("is-story"), reach = g.classList.contains("is-country") ? FAR * 9 : (town || story) ? FAR * 3 : FAR;   // towns and stories are the orientation layer: they stay through a wide view
      var inView = pr[2] && x > 8 && x < W - 8 && y > 8 && y < Hh - 8 && dist < reach && !inKeep(x, y), occ = inView && H && hidden(pt, p.cam);
      if (inView && !occ && shown < MAXL) {
        far = dist > reach * .6; side = x + 9 + tw < W - 8 ? 0 : x - 9 - tw > 8 ? 1 : -1;
        if (side >= 0) { var bx = side ? x - 9 - tw : x + 9, box = [Math.min(bx, x) - 8, y - 11, Math.max(bx + tw, x) + 8, y + 11], ok = true;
          for (var q = 0; q < boxes.length; q++) { var o = boxes[q]; if (box[0] < o[2] && box[2] > o[0] && box[1] < o[3] && box[3] > o[1]) { ok = false; break; } }
          if (ok) { show = true; boxes.push(box); shown++; } }
      }
      put("pl" + c, show ? x.toFixed(1) + "," + y.toFixed(1) + "," + side + "," + (far ? 1 : 0) : "", function (v) {
        var b = lmBtn[c];
        if (!v) { g.style.display = "none"; if (b) b.hidden = true; return; } var a = v.split(","); g.style.display = ""; g.classList.toggle("is-far", a[3] === "1"); g.setAttribute("transform", "translate(" + a[0] + " " + a[1] + ")");
        var l = a[2] === "1", o = g.hasAttribute("data-mk") ? 19 : 7, tw2 = g._tw || 60;
        if (g._tx) { g._tx.setAttribute("x", l ? -o : o); g._tx.classList.toggle("is-l", l); }
        if (g._ul) { g._ul.setAttribute("x1", (l ? -o - tw2 : o).toFixed(1)); g._ul.setAttribute("x2", (l ? -o : o + tw2).toFixed(1)); }
        if (b) { b.hidden = false; b.style.width = (tw2 + 12).toFixed(0) + "px"; b.style.transform = "translate(" + (parseFloat(a[0]) + (l ? -o - tw2 - 6 : o - 6)).toFixed(0) + "px," + a[1] + "px)"; } });
      g._mk = { x: x, y: y, on: inView && !occ };
      if (inView && !occ) { var d = Math.hypot((x - cx) / W * 16, (y - cy) / Hh * 9); if (d < bd) { bd = d; best = g.getAttribute("data-l"); } }
    });
    put("at", best ? (bd < 1.3 ? "over " : "nearest ") + best : "", function (v) { if (atEl) { var sp = v.indexOf(" "); atEl.innerHTML = v ? "<i>" + v.slice(0, sp) + "</i> " + v.slice(sp + 1) : ""; } });
    /* the tracks' launch pins while the controls are taken */
    [].slice.call(s.querySelectorAll(".v4i-fl-tp")).forEach(function (b, i) {
      var o = trackObjs[i]; b.classList.toggle("is-on", i === activeTrack); if (!o || !free) { put("tp" + i, "", function () { b.hidden = true; }); return; }
      var pr = project(o.start), on = pr[2] && pr[0] > 8 && pr[0] < W - 8 && pr[1] > 8 && pr[1] < Hh - 8 && !(H && hidden(o.start, p.cam)) && !inKeep(pr[0], pr[1]);
      put("tp" + i, on ? pr[0].toFixed(0) + "," + pr[1].toFixed(0) : "", function (v) { if (!v) { b.hidden = true; return; } var a2 = v.split(","); b.hidden = false; b.style.transform = "translate(" + a2[0] + "px," + a2[1] + "px)"; });
    });
    /* the markers: a photograph's place, tappable */
    mks.forEach(function (b) {
      var c = b.getAttribute("data-c"), g = pls.filter(function (q) { return q.getAttribute("data-c") === c; })[0], m = g && g._mk;
      var on = m && m.on; var under = false;
      if (on) for (var q = 0; q < cardBoxes.length; q++) { var o = cardBoxes[q]; if (m.x > o[0] - 14 && m.x < o[2] + 14 && m.y > o[1] - 14 && m.y < o[3] + 14) under = true; }   // a ring half under a plate is hidden too
      put("mk" + c, on && !under ? m.x.toFixed(0) + "," + m.y.toFixed(0) : "", function (v) { if (!v) { b.hidden = true; return; } var a = v.split(","); b.hidden = false; b.style.transform = "translate(" + a[0] + "px," + a[1] + "px)"; });
    });
  }
  function progress() { var r = s.getBoundingClientRect(), h = r.height - window.innerHeight; if (h <= 0) return 0; var p = -r.top / h; return p < 0 ? 0 : p > 1 ? 1 : p; }
  function tick() {
    var p = progress(); target = p * (n - 1);
    if (free && lastP >= 0 && Math.abs(p - lastP) > 0.004) leaveFree();
    lastP = p;
    if (cur < 0) { cur = target; dirty = true; } else { var d = target - cur; if (d > .02 || d < -.02) { cur += d * .2; dirty = true; } else if (cur !== target) { cur = target; dirty = true; } }
    flightF = cur;
    if (blend > 0) { blend = Math.max(0, blend - 0.05); dirty = true; }
    if (free && !grab && !two && settleZ()) dirty = true;
    if (glide) coast();
    if (dirty) { dirty = false; render(); }
    if (ready && lifeG.length) life(performance.now());
    raf = requestAnimationFrame(tick);
  }
  function run(on) { if (on) { if (!raf) raf = requestAnimationFrame(tick); } else if (raf) { cancelAnimationFrame(raf); raf = 0; } }
  size();
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (e) { for (var k = 0; k < e.length; k++) if (e[k].isIntersecting) load(); }, { rootMargin: "150% 0px" }).observe(s);
    new IntersectionObserver(function (e) { var on = false; for (var k = 0; k < e.length; k++) if (e[k].isIntersecting) on = true; run(on); }, { rootMargin: "20% 0px" }).observe(s);
  } else { load(); run(true); }
  var rz = 0; function resized() { cancelAnimationFrame(rz); rz = requestAnimationFrame(size); }
  window.addEventListener("resize", resized); if (window.visualViewport) window.visualViewport.addEventListener("resize", resized);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(size);
  function goTo(px, py, dist) { if (!free) enterFree(); O.tgt.copy(toWorld(px, py, base)); O.tgt.z = groundZ(O.tgt); if (dist) O.dist = dist; clampFree(); dirty = true; }   // the controls taken, over a grid position
  window.__v4iFly = { enterFree: enterFree, leaveFree: leaveFree, pan: pan, zoom: zoom, orbit: orbit, setTrack: setTrack, flyToTrack: flyToTrack, goTo: goTo, state: function () { return { free: free, ready: ready, f: flightF, track: activeTrack, tracks: TR.length, life: lifeG.filter(function (G) { return G.on; }).map(function (G) { return G.L.c + ":" + G.L.kind + ":" + G.ms.filter(function (m) { return m.shown; }).length; }), layers: layers.map(function (L) { return L.name + ":" + (L.mesh ? "on" : L.started ? "loading" : "off"); }), O: { dist: O.dist, yaw: O.yaw, pitch: O.pitch, tgt: [O.tgt.x, O.tgt.y] } }; } };
})();
