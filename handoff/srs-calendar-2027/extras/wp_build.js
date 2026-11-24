// SRS wallpaper (broadcast style) from SRS_6_T6_68: a phone and a desktop size. Every word on it is a fact.
const { chromium } = require('playwright'); const fs = require('fs');
const D = process.argv[2], F = '/home/user/website/assets/fonts';
const font = (fam, f, w) => `@font-face{font-family:"${fam}";font-weight:${w};src:url(file://${F}/${f}-latin-${w}-normal.woff2)}`;
const CSS = `${font('Poppins', 'poppins', 700)}${font('Poppins', 'poppins', 800)}${font('DM Sans', 'dm-sans', 400)}${font('DM Sans', 'dm-sans', 500)}${font('DM Sans', 'dm-sans', 600)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#05080d;color:#f6f4f4;font-family:"DM Sans",sans-serif;overflow:hidden}
.k{font:600 var(--k,9px)/1 "DM Sans";letter-spacing:.28em;text-transform:uppercase;color:#9fb1bd}
.o{color:#ff7517}
.big{font:800 var(--fs)/.8 Poppins;text-transform:uppercase;letter-spacing:-.04em;transform:skewX(-12deg);white-space:nowrap}
.fill{background:linear-gradient(180deg,#ffffff 0%,#ffd7b8 55%,rgba(255,117,23,.0) 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.line{-webkit-text-stroke:1px rgba(246,244,244,.55);color:transparent}
.tag{display:inline-flex;align-items:center;height:var(--th,22px);padding:0 14px;background:#ff7517;color:#05080d;font:800 var(--tf,11px)/1 Poppins;letter-spacing:.06em;transform:skewX(-16deg)}
.tag>span{transform:skewX(16deg)}
.rule{position:relative;height:1px;background:linear-gradient(90deg,rgba(246,244,244,.55),rgba(246,244,244,.08))}
.rule i{position:absolute;top:-3px;width:1px;height:7px;background:rgba(246,244,244,.5)}
.corner{position:absolute;width:18px;height:18px;border:1.5px solid rgba(246,244,244,.6)}
`;
const ticks = n => Array.from({ length: n }, (_, i) => `<i style="left:${(100 * i / (n - 1)).toFixed(2)}%"></i>`).join('');
const ROUNDS = [['01', 'Lijak', 'Slovenia', '15–21 Mar'], ['02', 'St Jean Montclar', 'France · provisional', '20–27 Jun'], ['03', 'Gemona', 'Italy', '17–24 Jul'],
  ['04', 'Krushevo', 'North Macedonia', '22–29 Aug'], ['05', 'St André', 'France', '12–19 Sep']];

// phone: 393 x 852 css px at 3x (1179 x 2556)
const phone = `<style>${CSS}
.pg{position:relative;width:393px;height:852px;overflow:hidden}
.ph,.cut{position:absolute;inset:0;background:url(file://${D}/work/graded.jpg) 46% 0/auto 100% no-repeat}
.cut{background-image:url(file://${D}/work/wingcut.png)}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,8,13,.35) 0%,rgba(5,8,13,0) 18%,rgba(5,8,13,0) 55%,rgba(5,8,13,.85) 82%,#05080d 100%)}
.w1{position:absolute;left:-6px;top:236px;--fs:104px;opacity:.95}
.w2{position:absolute;left:-2px;top:600px;--fs:86px}
.cn{left:18px;top:56px;border-right:0;border-bottom:0}.cn2{right:18px;top:56px;border-left:0;border-bottom:0}
.foot{position:absolute;left:22px;right:22px;top:690px}
.row{display:flex;align-items:center;justify-content:space-between;margin-top:12px}
.cr{position:absolute;left:22px;right:22px;top:772px;display:flex;justify-content:space-between;--k:7px}
.side{position:absolute;right:10px;top:300px;writing-mode:vertical-rl;--k:7.5px;opacity:.75}
</style><div class="pg"><div class="ph"></div><div class="shade"></div>
<div class="big line w1">SRS</div>
<div class="cut"></div>
<div class="corner cn"></div><div class="corner cn2"></div>
<div class="side k">Paragliding Atlas · SRS 2026 · Task 6</div>
<div class="big fill w2">Tapalpa</div>
<div class="foot"><div class="rule">${ticks(13)}</div>
<div class="row"><span class="tag"><span>TASK 06</span></span><span class="k">SRS <span class="o">/</span> 2026</span><span class="k">Mexico</span></div></div>
<div class="cr"><span class="k">Photo · Aninder Singh</span><span class="k">Paragliding Atlas</span></div></div>`;

// desktop: 1280 x 720 css px at 2x (2560 x 1440); the photo on the right, the season down the left
const rows = ROUNDS.map(r => `<div class="rd"><b>R${r[0]}</b><span class="pl">${r[1]}</span><span class="k cc">${r[2]}</span><span class="dt">${r[3]}</span></div>`).join('');
const desk = `<style>${CSS}
.pg{position:relative;width:1280px;height:720px;overflow:hidden;background:radial-gradient(120% 90% at 70% 30%,#0e1a24 0%,#05080d 60%)}
.ph,.cut{position:absolute;right:0;top:0;width:480px;height:720px;background:url(file://${D}/work/graded.jpg) 0 0/480px 720px no-repeat}
.ph{-webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 24%);mask-image:linear-gradient(90deg,transparent 0%,#000 24%)}
.cut{background-image:url(file://${D}/work/wingcut.png)}
.w1{position:absolute;left:40px;top:146px;--fs:212px}
.w0{position:absolute;left:52px;top:330px;--fs:64px}
.top{position:absolute;left:56px;right:56px;top:44px;display:flex;justify-content:space-between;--k:10px}
.cn{left:28px;top:28px;border-right:0;border-bottom:0}.cn2{right:28px;bottom:28px;border-left:0;border-top:0}
.sea{position:absolute;left:56px;top:446px;width:560px}
.sea .hd{display:flex;align-items:center;gap:16px;margin-bottom:14px;--th:24px;--tf:12px}
.rd{display:grid;grid-template-columns:44px 1fr 196px 92px;align-items:baseline;padding:7px 0;border-bottom:1px solid rgba(246,244,244,.1)}
.rd b{font:800 13px/1 Poppins;color:#ff7517;font-style:italic}
.rd .pl{font:700 15px/1 Poppins;text-transform:uppercase;letter-spacing:.01em}
.rd .cc{--k:9px}.rd .dt{font:600 13px/1 "DM Sans";text-align:right;font-variant-numeric:tabular-nums}
.cap{position:absolute;right:72px;bottom:48px;text-align:right;--k:9px}
.cap b{display:block;font:800 22px/1 Poppins;transform:skewX(-12deg);margin-bottom:8px;text-transform:uppercase}
</style><div class="pg"><div class="ph"></div>
<div class="corner cn"></div><div class="corner cn2"></div>
<div class="top"><span class="k">Paragliding Atlas</span><span class="k">SRS <span class="o">/</span> 2026 · Task 6</span></div>
<div class="big fill w1">Tapalpa</div>
<div class="cut"></div>
<div class="big line w0">Mexico</div>
<div class="sea"><div class="hd"><span class="tag"><span>SRS 2027</span></span><span class="k">The season · five rounds</span></div>
<div class="rule" style="margin-bottom:4px">${ticks(21)}</div>${rows}</div>
<div class="cap"><b>Tapalpa, Mexico</b><span class="k">SRS 2026 · Task 6 · Photo · Aninder Singh</span></div></div>`;

(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  for (const [name, html, w, h, s] of [['phone', phone, 393, 852, 3], ['desktop', desk, 1280, 720, 2]]) {
    const f = `${D}/work/${name}.html`; fs.writeFileSync(f, `<!doctype html><meta charset="utf-8">${html}`);
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: s });
    await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: `${D}/work/${name}.png` });
  }
  await b.close();
})();
