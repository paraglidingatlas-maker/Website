// The SRS 2027 cover in the owner's reference style (a car-on-black poster): the glider lit on black, its reflection,
// an orange brush word behind it, orange light falling from the top right, a centred mark and a short factual text.
// Our own identity only: the Paragliding Atlas logo once; no other brand's name, mark or type.
const { chromium } = require('playwright'); const fs = require('fs');
const O = process.argv[2], F = '/home/user/website/assets/fonts', SF = process.argv[3];
const ff = (fam, f, w) => `@font-face{font-family:"${fam}";font-weight:${w};src:url(file://${F}/${f}-latin-${w}-normal.woff2)}`;
const OR = '#ff7a1f';
const css = `${ff('Poppins', 'poppins', 600)}${ff('Poppins', 'poppins', 700)}${ff('DM Sans', 'dm-sans', 400)}${ff('DM Sans', 'dm-sans', 500)}${ff('DM Sans', 'dm-sans', 600)}
@font-face{font-family:"Brush";src:url(file://${SF}/MrDafoe.ttf)}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1123px;height:794px;background:#000;overflow:hidden;font-family:"DM Sans";color:#f2f2f2}
.pg{position:relative;width:1123px;height:794px;overflow:hidden;background:radial-gradient(60% 55% at 50% 58%,#0d0b0a 0%,#000 70%)}
.abs{position:absolute}
.k{font:600 var(--k,9px)/1 "DM Sans";letter-spacing:.34em;text-transform:uppercase}
.brush{left:0;right:0;top:350px;text-align:center;font:400 196px/1 "Brush";letter-spacing:-.01em;transform:rotate(-5deg);
 background:linear-gradient(180deg,#b9541a 0%,#86360c 60%,#3d1604 100%);-webkit-background-clip:text;background-clip:text;color:transparent;opacity:.85;
 -webkit-mask-image:url(file://${O}/brushtex.png);mask-image:url(file://${O}/brushtex.png);-webkit-mask-size:100% 100%;mask-size:100% 100%}
.floor{left:180px;right:180px;top:611px;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.18),transparent)}
.mark{left:0;right:0;top:40px;text-align:center}
.mark img{width:150px;display:inline-block}
.mark .k{display:block;margin-top:12px;--k:8.5px}
.mark i{display:block;width:140px;height:1px;margin:14px auto 0;background:linear-gradient(90deg,transparent,${OR},transparent)}
.txt{left:0;right:0;bottom:46px;text-align:center;font:400 11.5px/1.75 "DM Sans";color:#d8d8d8}
.txt b{font-weight:600;color:#fff}.txt .o{color:${OR}}
.rounds{display:block;margin:6px auto 0;font:500 10px/1.6 "DM Sans";letter-spacing:.06em;color:#bcbcbc}
.arc{left:50%;bottom:20px;transform:translateX(-50%)}`;
// the glider: the photo frame at 0.485 (2400 x 2000 canvas incl. the reflection), centred on the glider
const k = .485, gx = 561 - 985 * k, gy = 150 - 470 * k;
const html = `<style>${css}</style><div class="pg">
<img class="abs" src="file://${O}/streaks.png" style="left:0;top:0;width:1123px;height:794px;opacity:.72">
<div class="abs brush">SRS 2027</div>
<img class="abs" src="file://${O}/reflection.png" style="left:${gx}px;top:${gy}px;width:${2400 * k}px">
<div class="abs floor"></div>
<img class="abs" src="file://${O}/glider.png" style="left:${gx}px;top:${gy}px;width:${2400 * k}px">
<div class="abs mark"><img src="file:///home/user/website/assets/logo/atlas-logo-white.png" alt=""><span class="k">Sports-Class Racing Series · Race Calendar 2027</span><i></i></div>
<div class="abs txt">The Sports-Class Racing Series returns in 2027: <b>five rounds</b>, from Lijak in March to St André in September.<br>
<span class="rounds">Lijak 15–21 Mar · St Jean Montclar 20–27 Jun (provisional) · Gemona 17–24 Jul · Krushevo 22–29 Aug · St André 12–19 Sep</span>
<span class="k" style="display:block;margin-top:10px;--k:7.5px;color:#8f8f8f">Tapalpa, Mexico · SRS 2026 · Task 1 · Photo Aninder Singh</span></div>
<svg class="abs arc" width="46" height="14" viewBox="0 0 46 14"><path d="M2 13 Q23 -5 44 13" fill="none" stroke="${OR}" stroke-width="2.2" stroke-linecap="round"/></svg>
</div>`;
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 3 });
  fs.writeFileSync(`${O}/cover.html`, `<!doctype html><meta charset="utf-8">${html}`);
  await p.goto(`file://${O}/cover.html`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: `${O}/cover.png`, clip: { x: 0, y: 0, width: 1122.5, height: 793.7 } });
  await b.close();
})();
