// The SRS 2027 calendar cover in the F1 HUD style (SRS_6_T1_51). Same facts as the cover it replaces.
const { chromium } = require('playwright'); const fs = require('fs');
const D = process.argv[2], F = '/home/user/website/assets/fonts';
const ff = (fam, f, w) => `@font-face{font-family:"${fam}";font-weight:${w};src:url(file://${F}/${f}-latin-${w}-normal.woff2)}`;
const C = '#5ff4ff', O = '#ff6a1a', R = '#e8112d';
const brk = (x, y, w, h, L, col, sw = 1.5) => `<path d="M${x} ${y + L}V${y}H${x + L}M${x + w - L} ${y}H${x + w}V${y + L}M${x + w} ${y + h - L}V${y + h}H${x + w - L}M${x + L} ${y + h}H${x}V${y + h - L}" fill="none" stroke="${col}" stroke-width="${sw}"/>`;
const ret = (cx, cy, r, col) => `<g fill="none" stroke="${col}" stroke-width="1.3"><circle cx="${cx}" cy="${cy}" r="${r}" stroke-dasharray="${(r * 1.2).toFixed(1)} ${(r * .37).toFixed(1)}"/><circle cx="${cx}" cy="${cy}" r="${r * .55}" stroke-opacity=".5"/><path d="M${cx - r - 10} ${cy}h12M${cx + r - 2} ${cy}h12M${cx} ${cy - r - 10}v12M${cx} ${cy + r - 2}v12"/></g>`;
const leader = (x1, y1, x2, y2, col) => `<path d="M${x1} ${y1}L${x2} ${y2}H${x2 + (x2 > x1 ? 50 : -50)}" fill="none" stroke="${col}" stroke-width="1"/><circle cx="${x1}" cy="${y1}" r="2.5" fill="${col}"/>`;
const streaks = (w, h, n, seed) => { let s = '', r = seed; const rnd = () => (r = (r * 9301 + 49297) % 233280) / 233280;
  for (let i = 0; i < n; i++) { const y = rnd() * h, x = rnd() * w, l = 60 + rnd() * 240; s += `<line x1="${x}" y1="${y}" x2="${x + l}" y2="${y}" stroke="#bff8ff" stroke-opacity="${(.05 + rnd() * .14).toFixed(2)}" stroke-width="${rnd() < .8 ? 1 : 2}"/>`; } return s; };
const ROUNDS = [['01', 'Lijak', 'Slovenia', '15–21 Mar', 'Confirmed'], ['02', 'St Jean Montclar', 'France', '20–27 Jun', 'Provisional'], ['03', 'Gemona', 'Italy', '17–24 Jul', 'Confirmed'],
  ['04', 'Krushevo', 'North Macedonia', '22–29 Aug', 'Confirmed'], ['05', 'St André', 'France', '12–19 Sep', 'Confirmed']];
const html = `<style>${ff('Poppins', 'poppins', 700)}${ff('Poppins', 'poppins', 800)}${ff('DM Sans', 'dm-sans', 500)}${ff('DM Sans', 'dm-sans', 600)}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1123px;height:794px;background:#020507;overflow:hidden;color:#e6fbff;font-family:"DM Sans"}
.pg{position:relative;width:1123px;height:794px;overflow:hidden}.img{position:absolute;left:0;top:0;height:794px}
.scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(95,244,255,.03) 0 1px,transparent 1px 3px)}
.vig{position:absolute;inset:0;background:radial-gradient(110% 90% at 42% 50%,transparent 55%,rgba(0,0,0,.6))}
svg{position:absolute;inset:0;overflow:visible}
.k{font:600 var(--k,9.5px)/1 "DM Sans";letter-spacing:.3em;text-transform:uppercase}.c{color:${C}}.o{color:${O}}
.srs{position:absolute;left:52px;top:150px;font:800 205px/.8 Poppins;letter-spacing:-.05em;transform:skewX(-12deg);
 background:linear-gradient(180deg,#ffffff 0%,#d9f9ff 46%,#6bd6e6 53%,#f0fdff 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(95,244,255,.3))}
.yr{position:absolute;left:56px;top:330px;font:800 150px/.8 Poppins;letter-spacing:-.04em;transform:skewX(-12deg);color:transparent;-webkit-text-stroke:1.4px rgba(230,251,255,.75)}
.rc{position:absolute;left:62px;top:478px;display:flex;align-items:center;gap:14px}.rc i{width:44px;height:4px;background:${O};transform:skewX(-30deg)}
.tw{position:absolute;right:44px;top:118px;width:300px;background:rgba(2,8,11,.72);border:1px solid rgba(95,244,255,.25);border-left:4px solid ${O}}
.tw .hd{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;border-bottom:1px solid rgba(95,244,255,.2)}
.chk{height:8px;width:48px;background:repeating-conic-gradient(#e6fbff 0 25%,transparent 0 50%) 0 0/8px 8px}
.row{display:grid;grid-template-columns:34px 1fr auto;gap:10px;padding:11px 14px;border-bottom:1px solid rgba(95,244,255,.12);align-items:center}
.row b{font:800 15px/1 Poppins;font-style:italic;color:${O}}
.row .p{font:700 14px/1.05 Poppins;text-transform:uppercase}.row .n{display:block;margin-top:4px;color:#9fc9d1;font:500 10.5px/1 "DM Sans"}
.row .d{text-align:right;font:700 12px/1 Poppins;color:${C}}.row .s{display:block;margin-top:5px;font:600 7.5px/1 "DM Sans";letter-spacing:.22em;text-transform:uppercase;color:#9fc9d1}
.row .s.pv{color:${O}}
</style><div class="pg"><img class="img" src="file://${D}/work/hud.jpg">
<svg width="1123" height="794">${streaks(1123, 794, 60, 11)}
${brk(20, 20, 1083, 754, 24, C, 1.4)}
${brk(405, 222, 160, 280, 16, C)}${leader(551, 250, 600, 92, C)}
${ret(484, 676, 46, O)}
<line x1="484" y1="506" x2="484" y2="622" stroke="${C}" stroke-opacity=".35" stroke-dasharray="3 5"/></svg>
<div class="scan"></div><div class="vig"></div>
<div class="srs">SRS</div><div class="yr">2027</div>
<img class="img" src="file://${D}/work/hud_cut.png">
<div class="rc"><i></i><span class="k" style="--k:14px;letter-spacing:.42em">Race calendar</span></div>
<div style="position:absolute;left:46px;top:46px;display:flex;gap:16px"><span class="k c">Sports-Class Racing Series</span></div>
<div class="k c" style="position:absolute;left:606px;top:78px;--k:8.5px">Canopy · tracking</div>
<div class="tw"><div class="hd"><span class="k o" style="--k:9px">Rounds · 2027</span><div class="chk"></div></div>
${ROUNDS.map(r => `<div class="row"><b>R${r[0]}</b><span><span class="p">${r[1]}</span><span class="n">${r[2]}</span></span><span><span class="d">${r[3]}</span><span class="s${r[4] == 'Provisional' ? ' pv' : ''}">${r[4]}</span></span></div>`).join('')}</div>
<div style="position:absolute;right:46px;bottom:44px;text-align:right"><div class="k" style="--k:8.5px">Tapalpa, Mexico · SRS 2026 · Task 1</div><div class="k" style="--k:7.5px;margin-top:8px;opacity:.65">Photo · Aninder Singh / Paragliding Atlas</div></div>
<div class="k c" style="position:absolute;left:546px;top:670px;--k:8.5px">Pilot · pod</div>
</div>`;
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 3 });
  fs.writeFileSync(`${D}/work/cover.html`, `<!doctype html><meta charset="utf-8">${html}`);
  await p.goto(`file://${D}/work/cover.html`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
  await p.screenshot({ path: `${D}/work/cover.png`, clip: { x: 0, y: 0, width: 1122.5, height: 793.7 } });
  await b.close();
})();
