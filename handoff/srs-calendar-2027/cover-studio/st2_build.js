// The SRS 2027 cover in the owner's second reference style (a studio car shot): slate backdrop, top spotlight, floor,
// the glider matted (not cut) and lit, a soft shadow, a speed smear; the logo once; the same facts as the live cover.
const { chromium } = require('playwright'); const fs = require('fs');
const O = process.argv[2], F = '/home/user/website/assets/fonts';
const ff = (fam, f, w) => `@font-face{font-family:"${fam}";font-weight:${w};src:url(file://${F}/${f}-latin-${w}-normal.woff2)}`;
const OR = '#ff7a1f';
const html = `<style>${ff('Poppins', 'poppins', 800)}${ff('DM Sans', 'dm-sans', 400)}${ff('DM Sans', 'dm-sans', 500)}${ff('DM Sans', 'dm-sans', 600)}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1123px;height:794px;background:#0b0d0f;overflow:hidden;font-family:"DM Sans";color:#eef0f2}
.pg{position:relative;width:1123px;height:794px;overflow:hidden}.abs{position:absolute}.full{left:0;top:0;width:1123px;height:794px}
.k{font:600 var(--k,9px)/1 "DM Sans";letter-spacing:.34em;text-transform:uppercase}
.big{left:0;right:0;top:268px;text-align:center;font:800 230px/1 Poppins;letter-spacing:-.04em;color:rgba(255,255,255,.075);
 text-shadow:0 2px 0 rgba(0,0,0,.25),0 -1px 0 rgba(255,255,255,.04)}
.mark{left:0;right:0;top:36px;text-align:center}.mark img{width:140px;display:inline-block}
.mark .k{display:block;margin-top:12px;--k:8.5px;color:#d9dde1}
.mark i{display:block;width:120px;height:1px;margin:13px auto 0;background:linear-gradient(90deg,transparent,${OR},transparent)}
.txt{left:0;right:0;bottom:40px;text-align:center;font:400 11.5px/1.75 "DM Sans";color:#cfd3d7}
.txt b{font-weight:600;color:#fff}
.rounds{display:block;margin-top:5px;font:500 10px/1.6 "DM Sans";letter-spacing:.06em;color:#aab0b6}
</style><div class="pg"><img class="abs full" src="file://${O}/backdrop.png">
<div class="abs big">SRS 2027</div>
<img class="abs full" src="file://${O}/glider_layer.png">
<div class="abs mark"><img src="file:///home/user/website/assets/logo/atlas-logo-white.png" alt=""><span class="k">Sports-Class Racing Series · Race Calendar 2027</span><i></i></div>
<div class="abs txt">The Sports-Class Racing Series returns in 2027: <b>five rounds</b>, from Lijak in March to St André in September.
<span class="rounds">Lijak 15–21 Mar · St Jean Montclar 20–27 Jun (provisional) · Gemona 17–24 Jul · Krushevo 22–29 Aug · St André 12–19 Sep</span>
<span class="k" style="display:block;margin-top:10px;--k:7.5px;color:#868c92">Tapalpa, Mexico · SRS 2026 · Task 1 · Photo Aninder Singh</span></div></div>`;
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 3 });
  fs.writeFileSync(`${O}/cover.html`, `<!doctype html><meta charset="utf-8">${html}`);
  await p.goto(`file://${O}/cover.html`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: `${O}/cover.png`, clip: { x: 0, y: 0, width: 1122.5, height: 793.7 } });
  await b.close();
})();
