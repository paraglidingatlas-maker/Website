// F1-style HUD wallpaper from SRS_6_T1_51 (fan-art HUD look). No invented telemetry: every number is a real fact.
const { chromium } = require('playwright'); const fs = require('fs');
const D = process.argv[2], F = '/home/user/website/assets/fonts';
const ff = (fam, f, w) => `@font-face{font-family:"${fam}";font-weight:${w};src:url(file://${F}/${f}-latin-${w}-normal.woff2)}`;
const C = '#5ff4ff', O = '#ff6a1a';
const CSS = `${ff('Poppins', 'poppins', 700)}${ff('Poppins', 'poppins', 800)}${ff('DM Sans', 'dm-sans', 500)}${ff('DM Sans', 'dm-sans', 600)}
*{margin:0;padding:0;box-sizing:border-box}html,body{background:#020507;overflow:hidden;color:#e6fbff;font-family:"DM Sans"}
.pg{position:relative;overflow:hidden}
.img{position:absolute;display:block}
.scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(95,244,255,.035) 0 1px,transparent 1px 3px);pointer-events:none}
.vig{position:absolute;inset:0;background:radial-gradient(120% 90% at 40% 50%,transparent 55%,rgba(0,0,0,.55))}
svg{position:absolute;inset:0;overflow:visible}
.k{font:600 var(--k,10px)/1 "DM Sans";letter-spacing:.3em;text-transform:uppercase}
.c{color:${C}}.o{color:${O}}
.ttl{font:800 var(--fs)/.82 Poppins;letter-spacing:-.04em;text-transform:uppercase;transform:skewX(-14deg);white-space:nowrap;
 background:linear-gradient(180deg,#ffffff 0%,#d9f9ff 45%,#6bd6e6 52%,#f0fdff 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 0 18px rgba(95,244,255,.35))}
.chk{height:var(--h,10px);background:repeating-conic-gradient(#e6fbff 0 25%,transparent 0 50%) 0 0/var(--h,10px) var(--h,10px)}
.slash{height:6px;background:${O};transform:skewX(-30deg)}
.rd{display:grid;grid-template-columns:38px 1fr auto;gap:10px;align-items:baseline;padding:6px 0;border-bottom:1px solid rgba(95,244,255,.18)}
.rd b{font:800 12px/1 Poppins;color:${O};font-style:italic}.rd span{font:700 13px/1 Poppins;text-transform:uppercase}.rd i{font:600 12px/1 "DM Sans";font-style:normal;color:${C}}`;
const ROUNDS = [['R01', 'Lijak, Slovenia', '15–21 Mar'], ['R02', 'St Jean Montclar, France*', '20–27 Jun'], ['R03', 'Gemona, Italy', '17–24 Jul'], ['R04', 'Krushevo, N. Macedonia', '22–29 Aug'], ['R05', 'St André, France', '12–19 Sep']];
// a bracket box: four corners
const brk = (x, y, w, h, L, col, sw = 1.5) => `<path d="M${x} ${y + L}V${y}H${x + L}M${x + w - L} ${y}H${x + w}V${y + L}M${x + w} ${y + h - L}V${y + h}H${x + w - L}M${x + L} ${y + h}H${x}V${y + h - L}" fill="none" stroke="${col}" stroke-width="${sw}"/>`;
// a reticle: ring, gaps, crosshair ticks
const ret = (cx, cy, R, col) => `<g fill="none" stroke="${col}" stroke-width="1.3"><circle cx="${cx}" cy="${cy}" r="${R}" stroke-dasharray="${(R * 1.2).toFixed(1)} ${(R * .37).toFixed(1)}"/><circle cx="${cx}" cy="${cy}" r="${R * .55}" stroke-opacity=".5"/>
<path d="M${cx - R - 10} ${cy}h12M${cx + R - 2} ${cy}h12M${cx} ${cy - R - 10}v12M${cx} ${cy + R - 2}v12"/></g>`;
// a gauge: an arc of ticks, part filled; no value, only a label
const gauge = (cx, cy, R, frac, col) => { let s = ''; const a0 = 140, a1 = 400, n = 40;
  for (let i = 0; i <= n; i++) { const a = (a0 + (a1 - a0) * i / n) * Math.PI / 180, l = i % 5 ? 6 : 12, on = i / n <= frac;
    s += `<line x1="${(cx + Math.cos(a) * R).toFixed(1)}" y1="${(cy + Math.sin(a) * R).toFixed(1)}" x2="${(cx + Math.cos(a) * (R - l)).toFixed(1)}" y2="${(cy + Math.sin(a) * (R - l)).toFixed(1)}" stroke="${on ? O : col}" stroke-width="${on ? 2.2 : 1.2}" stroke-opacity="${on ? 1 : .55}"/>`; }
  const A = (d) => d * Math.PI / 180, p = (d, r) => `${(cx + Math.cos(A(d)) * r).toFixed(1)} ${(cy + Math.sin(A(d)) * r).toFixed(1)}`;
  return s + `<path d="M${p(a0, R + 6)} A${R + 6} ${R + 6} 0 1 1 ${p(a1, R + 6)}" fill="none" stroke="${col}" stroke-opacity=".35"/>`; };
const leader = (x1, y1, x2, y2, col) => `<path d="M${x1} ${y1}L${x2} ${y2}H${x2 + (x2 > x1 ? 60 : -60)}" fill="none" stroke="${col}" stroke-width="1"/><circle cx="${x1}" cy="${y1}" r="2.5" fill="${col}"/>`;
const streaks = (w, h, n, seed) => { let s = '', r = seed; const rnd = () => (r = (r * 9301 + 49297) % 233280) / 233280;
  for (let i = 0; i < n; i++) { const y = rnd() * h, x = rnd() * w, l = 60 + rnd() * 260; s += `<line x1="${x}" y1="${y}" x2="${x + l}" y2="${y}" stroke="#bff8ff" stroke-opacity="${(.06 + rnd() * .16).toFixed(2)}" stroke-width="${rnd() < .8 ? 1 : 2}"/>`; } return s; };

// desktop 1280 x 720 (2x); the photo at 0.5333: wing x 443-597 y 171-445, pod x 427-613 y 603-688
const desk = `<style>${CSS}.pg{width:1280px;height:720px}</style><div class="pg">
<img class="img" src="file://${D}/work/hud.jpg" style="left:0;top:-80px;width:1280px">
<svg width="1280" height="720">${streaks(1280, 720, 70, 7)}
${brk(24, 24, 1232, 672, 26, C, 1.5)}
${brk(432, 160, 182, 322, 18, C)}${leader(597, 190, 680, 150, C)}
${ret(522, 646, 52, O)}${leader(570, 660, 690, 610, O)}
<line x1="522" y1="486" x2="522" y2="590" stroke="${C}" stroke-opacity=".35" stroke-dasharray="3 5"/>
${gauge(1130, 560, 82, .62, C)}
<path d="M60 360H360M60 366H300" stroke="${O}" stroke-width="2"/></svg>
<div class="scan"></div><div class="vig"></div>
<div style="position:absolute;left:52px;top:44px;display:flex;gap:18px;align-items:center"><span class="k c">Paragliding Atlas</span><span class="k">SRS <span class="o">/</span> 2026</span><span class="k">Tapalpa, Mexico</span></div>
<div style="position:absolute;right:52px;top:44px;display:flex;gap:12px;align-items:center"><div class="chk" style="width:60px;--h:8px"></div><span class="k">Task 01</span></div>
<div class="k c" style="position:absolute;left:688px;top:136px;--k:9px">Canopy · tracking</div>
<div class="k o" style="position:absolute;left:698px;top:596px;--k:9px">Pilot · pod</div>
<div style="position:absolute;left:60px;top:390px"><div class="ttl" style="--fs:118px">Tapalpa</div><div class="k c" style="margin-top:14px;--k:11px">Mexico · SRS 2026 · Task 1</div></div>
<img class="img" src="file://${D}/work/hud_cut.png" style="left:0;top:-80px;width:1280px">
<div style="position:absolute;left:58px;top:212px"><div class="slash" style="width:90px"></div><div class="k" style="margin-top:10px">Race view</div></div>
<div style="position:absolute;right:60px;top:186px;width:330px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><span class="k o">SRS 2027 · calendar</span><span class="k c" style="--k:8px">5 rounds</span></div>${ROUNDS.map(r => `<div class="rd"><b>${r[0]}</b><span>${r[1]}</span><i>${r[2]}</i></div>`).join('')}<div class="k" style="--k:8px;margin-top:8px;opacity:.6">* provisional</div></div>
<div style="position:absolute;left:1130px;top:552px;transform:translateX(-50%);text-align:center"><div style="font:800 30px/1 Poppins;font-style:italic;color:#e6fbff">T1</div><div class="k c" style="--k:8px;margin-top:6px">Task</div></div>
<div class="k" style="position:absolute;left:52px;bottom:42px;--k:9px;opacity:.75">Photo · Aninder Singh / Paragliding Atlas</div>
<div class="chk" style="position:absolute;right:52px;bottom:44px;width:120px;--h:6px;opacity:.7"></div></div>`;

// phone 393 x 852 (3x); the photo at 0.5325, left -326: wing x 116-270 y 250-524, pod x 100-286 y 682-767
const phone = `<style>${CSS}.pg{width:393px;height:852px}</style><div class="pg">
<img class="img" src="file://${D}/work/hud.jpg" style="left:-326px;top:0;height:852px">
<svg width="393" height="852">${streaks(393, 852, 40, 3)}
${brk(14, 50, 365, 760, 18, C, 1.3)}
${brk(104, 238, 178, 300, 14, C)}${leader(270, 270, 300, 238, C)}
${ret(196, 724, 46, O)}
<line x1="196" y1="538" x2="196" y2="672" stroke="${C}" stroke-opacity=".35" stroke-dasharray="3 5"/>
${gauge(70, 600, 40, .62, C)}</svg>
<div class="scan"></div><div class="vig"></div>
<div class="k c" style="position:absolute;left:300px;top:226px;--k:7px">Canopy</div>
<div style="position:absolute;right:14px;top:300px;writing-mode:vertical-rl;transform:rotate(180deg)"><div class="ttl" style="--fs:74px;transform:skewY(10deg)">Tapalpa</div></div>
<div style="position:absolute;left:70px;top:592px;transform:translateX(-50%);text-align:center"><div style="font:800 17px/1 Poppins;font-style:italic">T1</div></div>
<div style="position:absolute;left:28px;right:28px;top:790px;display:flex;justify-content:space-between;align-items:center"><span class="k" style="--k:7.5px">SRS <span class="o">/</span> 2026 · Tapalpa</span><div class="chk" style="width:44px;--h:6px"></div></div>
<div class="k" style="position:absolute;left:28px;top:812px;--k:6.5px;opacity:.7">Photo · Aninder Singh / Paragliding Atlas</div></div>`;

(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  for (const [n, html, w, h, s] of [['desktop', desk, 1280, 720, 2], ['phone', phone, 393, 852, 3]]) {
    const f = `${D}/work/hud-${n}.html`; fs.writeFileSync(f, `<!doctype html><meta charset="utf-8">${html}`);
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: s });
    await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
    await p.screenshot({ path: `${D}/work/hud-${n}.png` });
  }
  await b.close();
})();
