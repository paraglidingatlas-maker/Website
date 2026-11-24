// Five December key-art concepts (street-racing / open-world game feel; original, no film or game marks).
const { chromium } = require('playwright'); const fs = require('fs');
const O = process.argv[2], F = '/home/user/website/assets/fonts';
const ff = (fam, f, w) => `@font-face{font-family:"${fam}";font-weight:${w};src:url(file://${F}/${f}-latin-${w}-normal.woff2)}`;
const BASE = `${ff('Poppins', 'poppins', 700)}${ff('Poppins', 'poppins', 800)}${ff('DM Sans', 'dm-sans', 400)}${ff('DM Sans', 'dm-sans', 500)}${ff('DM Sans', 'dm-sans', 600)}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1200px;height:848px;overflow:hidden;background:#000;color:#fff;font-family:"DM Sans"}
.pg{position:relative;width:1200px;height:848px;overflow:hidden}
.ph{position:absolute;inset:0;background-size:cover;background-position:70% 40%}
.k{font:600 11px/1 "DM Sans";letter-spacing:.3em;text-transform:uppercase}
.cal{display:grid;grid-template-columns:repeat(31,1fr);gap:0}
.cal .d{display:flex;flex-direction:column;align-items:center;gap:7px}
.cal .d i{font:600 9px/1 "DM Sans";font-style:normal;letter-spacing:.1em;opacity:.6}
.cal .d b{font:700 17px/1 Poppins;font-variant-numeric:tabular-nums}
.cal .we b,.cal .we i{opacity:.45}`;
const WD = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
const cal = Array.from({ length: 31 }, (_, i) => { const wd = (i + 2) % 7; return `<div class="d${wd > 4 ? ' we' : ''}"><i>${WD[wd]}</i><b>${i + 1}</b></div>`; }).join(''); // 1 Dec 2027 is a Wednesday
const IMG = n => `file://${O}/${n}.jpg`;
const facts = `<span class="k">Tapalpa, Mexico · SRS 2026 · Task 6</span>`;
const credit = `<span class="k">Photo · Aninder Singh / Paragliding Atlas</span>`;
const P = {
// 1 NEON: a night sky, the title a neon tube
c1_neon: `<style>
.t{position:absolute;left:60px;top:430px;font:800 150px/1 Poppins;letter-spacing:-.02em;text-transform:uppercase;transform:skewX(-8deg);color:transparent;
 -webkit-text-stroke:3px #ff4fd8;text-shadow:0 0 8px #ff4fd8,0 0 24px #ff2fc0,0 0 60px rgba(255,47,192,.7)}
.t2{position:absolute;left:66px;top:400px;font:700 20px/1 Poppins;letter-spacing:.5em;color:#7ff6ff;text-shadow:0 0 10px #29e3ff,0 0 26px #29e3ff}
.top{position:absolute;left:60px;right:60px;top:44px;display:flex;justify-content:space-between;color:#7ff6ff}
.bar{position:absolute;left:60px;right:60px;bottom:58px;padding-top:16px;border-top:1px solid rgba(127,246,255,.5);box-shadow:0 -1px 12px rgba(41,227,255,.4);color:#e9fbff}
.cr{position:absolute;left:60px;right:60px;bottom:24px;display:flex;justify-content:space-between;color:rgba(233,251,255,.6)}</style>
<div class="pg"><div class="ph" style="background-image:url(${IMG('c1_neon')})"></div>
<div class="top"><span class="k">SRS / 2027</span><span class="k">12 / 12 · Season complete</span></div>
<div class="t2">2027 · SRS</div><div class="t">December</div>
<div class="bar"><div class="cal">${cal}</div></div><div class="cr">${facts}${credit}</div></div>`,
// 2 NITRO: a zoom burst, a heavy slanted metal title, a slanted calendar band
c2_nitro: `<style>
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,0) 30%,rgba(0,0,0,0) 62%,rgba(0,0,0,.8))}
.t{position:absolute;left:40px;top:512px;font:800 138px/.86 Poppins;letter-spacing:-.05em;text-transform:uppercase;transform:skewX(-16deg);
 background:linear-gradient(180deg,#fff 0%,#ffe0b0 38%,#ff8a2a 52%,#7a2b05 53%,#ffb35c 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 6px 0 #000) drop-shadow(0 0 30px rgba(255,120,30,.45))}
.tag{position:absolute;left:52px;top:466px;display:inline-flex;padding:8px 18px;background:#ff6a00;color:#000;font:800 16px/1 Poppins;letter-spacing:.12em;transform:skewX(-16deg)}
.band{position:absolute;left:-20px;right:-20px;bottom:-14px;padding:14px 72px 30px;background:rgba(0,0,0,.72);border-top:3px solid #ff6a00;transform:skewY(-2deg)}
.top{position:absolute;left:52px;right:52px;top:40px;display:flex;justify-content:space-between}</style>
<div class="pg"><div class="ph" style="background-image:url(${IMG('c2_nitro')})"></div><div class="sh"></div>
<div class="top">${facts}<span class="k">SRS / 2027 · 12 / 12</span></div>
<div class="tag">Season complete</div><div class="t">December</div>
<div class="band"><div class="cal">${cal}</div><div style="margin-top:10px;text-align:right">${credit}</div></div></div>`,
// 3 COLLAGE: key art in tilted panels, an inked look, a bold stacked title
c3_collage: `<style>
.bg{position:absolute;inset:0;background:url(${IMG('c3_collage')}) 72% 40%/cover}
.pn{position:absolute;border:8px solid #fff;box-shadow:0 16px 40px rgba(0,0,0,.55);background-size:cover}
.p1{left:40px;top:60px;width:330px;height:250px;transform:rotate(-4deg);background-image:url(${IMG('c3_collage')});background-size:1400px auto;background-position:-880px -680px}
.p2{left:70px;top:330px;width:300px;height:210px;transform:rotate(3deg);background-image:url(${IMG('c3_collage')});background-size:1100px auto;background-position:-540px -70px}
.t{position:absolute;left:40px;bottom:150px;font:800 118px/.84 Poppins;letter-spacing:-.04em;text-transform:uppercase;color:#fff;
 -webkit-text-stroke:2px #111;text-shadow:6px 6px 0 #e8112d,12px 12px 0 #111}
.yr{position:absolute;left:48px;bottom:118px;font:800 26px/1 Poppins;letter-spacing:.4em;color:#111;background:#ffd21f;padding:6px 12px;transform:rotate(-2deg)}
.card{position:absolute;left:40px;right:40px;bottom:24px;background:#fff;color:#111;padding:10px 20px;transform:rotate(-.6deg);box-shadow:0 10px 30px rgba(0,0,0,.4)}
.card .k{color:#333}.top{position:absolute;right:40px;top:30px;text-align:right;color:#111}
.top .k{display:block;margin-top:6px;background:#fff;padding:5px 8px}</style>
<div class="pg"><div class="bg"></div><div class="pn p1"></div><div class="pn p2"></div>
<div class="top"><span class="k">SRS / 2027 · 12 / 12</span><span class="k">Season complete</span></div>
<div class="t">December</div><div class="yr">2027</div>
<div class="card"><div class="cal">${cal}</div><div style="display:flex;justify-content:space-between;margin-top:8px">${facts}${credit}</div></div></div>`,
// 4 BLOCKBUSTER: letterbox bars, a wide tracked title, a billing block of facts
c4_blockbuster: `<style>
.ph{top:96px;bottom:150px}
.lb{position:absolute;left:0;right:0;background:#000}.lb1{top:0;height:96px}.lb2{bottom:0;height:150px}
.top{position:absolute;left:60px;right:60px;top:38px;display:flex;justify-content:space-between;color:#c9d6da}
.t{position:absolute;left:0;right:0;top:300px;text-align:center;font:700 92px/1 Poppins;letter-spacing:.38em;text-indent:.38em;text-transform:uppercase;color:#fff;text-shadow:0 0 40px rgba(0,0,0,.6)}
.st{position:absolute;left:0;right:0;top:404px;text-align:center;color:#ffd9a8}
.bl{position:absolute;left:60px;right:60px;bottom:20px;color:#9fb3b8}.bl .cal{margin-bottom:14px;color:#fff}
.bl .row{display:flex;justify-content:space-between}</style>
<div class="pg"><div class="ph" style="background-image:url(${IMG('c4_blockbuster')})"></div><div class="lb lb1"></div><div class="lb lb2"></div>
<div class="top"><span class="k">SRS / 2027</span><span class="k">12 / 12</span></div>
<div class="t">December</div><div class="st k">The season is complete</div>
<div class="bl"><div class="cal">${cal}</div><div class="row">${facts}${credit}</div></div></div>`,
// 5 RETRO: a striped sun, a chrome title with a horizon line through it
c5_retro: `<style>
.t{position:absolute;left:50px;top:520px;font:800 150px/1 Poppins;letter-spacing:-.03em;text-transform:uppercase;transform:skewX(-10deg);
 background:linear-gradient(180deg,#e9f6ff 0%,#9fd0ff 46%,#25113a 49%,#ff7ad5 52%,#ffe7a6 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 3px 0 #ff2aa0) drop-shadow(0 0 22px rgba(255,42,160,.55))}
.yr{position:absolute;left:62px;top:496px;font:700 22px/1 Poppins;letter-spacing:.6em;color:#ffe7a6;text-shadow:0 0 12px #ff8a3c}
.bar{position:absolute;left:50px;right:50px;bottom:46px;padding-top:14px;border-top:2px solid #ff7ad5;color:#ffeefa}
.cr{position:absolute;left:50px;right:50px;bottom:18px;display:flex;justify-content:space-between;color:rgba(255,238,250,.7)}
.top{position:absolute;left:50px;right:50px;top:40px;display:flex;justify-content:space-between;color:#ffe7a6}</style>
<div class="pg"><div class="ph" style="background-image:url(${IMG('c5_retro')})"></div>
<div class="top"><span class="k">SRS / 2027</span><span class="k">12 / 12 · Season complete</span></div>
<div class="yr">2027</div><div class="t">December</div>
<div class="bar"><div class="cal">${cal}</div></div><div class="cr">${facts}${credit}</div></div>`,
};
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1200, height: 848 }, deviceScaleFactor: 2 });
  for (const [n, html] of Object.entries(P)) {
    const f = `${O}/${n}.html`; fs.writeFileSync(f, `<!doctype html><meta charset="utf-8"><style>${BASE}</style>${html}`);
    await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
    await p.screenshot({ path: `${O}/page-${n}.png` });
  }
  await b.close();
})();
