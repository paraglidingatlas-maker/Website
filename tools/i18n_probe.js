// The translations' browser check (chat 27): serve the repo (python3 -m http.server 8765 --bind 127.0.0.1), then
// node tools/i18n_probe.js LANG OUTDIR [shots]: English left on screen, sideways overflow, failed requests, screenshots at 1440 and 390.
// Its English-word detector over-reports (words like 'a', 'no', 'in' are also Spanish/German): read the list, it is a lead, not a verdict.
// usage: node probe.js lang outdir [shots]
const { chromium } = require('playwright');
const fs = require('fs');
const lang = process.argv[2], out = process.argv[3], shots = process.argv[4] === 'shots';
const pages = JSON.parse(fs.readFileSync('tools/data/i18n/config.json', 'utf8')).pages;
const keep = fs.readFileSync('tools/data/i18n/keep.txt', 'utf8').split('\n').map(l => l.split('#')[0].trim()).filter(Boolean);
(async () => {
  const browser = await chromium.launch();
  const report = {};
  for (const w of [1440, 390]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: w > 500 ? 900 : 844 }, deviceScaleFactor: shots ? 2 : 1, isMobile: w < 500, hasTouch: w < 500 });
    for (const p of pages) {
      const page = await ctx.newPage();
      const bad = [];
      page.on('response', r => { if (r.status() >= 400 && r.url().includes('127.0.0.1')) bad.push(r.status() + ' ' + r.url().replace('http://127.0.0.1:8765/', '')); });
      page.on('pageerror', e => bad.push('JS ' + e.message.slice(0, 120)));
      await page.goto(`http://127.0.0.1:8765/prototypes/v4/${lang}/${p}`, { waitUntil: 'load' });
      await page.waitForTimeout(2500);
      const res = await page.evaluate((keep) => {
        const left = new Set();
        const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = tw.nextNode())) {
          const el = n.parentElement;
          if (!el || el.closest('script,style,svg,noscript,template,.nav-coords,.gr-fn,.gr-ln,.gr-meta,.gr-rc-n,.rt-m,.sl-m,.word')) continue;
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          let t = n.textContent;
          for (const k of keep) t = t.split(k).join(' ');
          const ws = (t.toLowerCase().match(/[a-z']+/g) || []);
          const EN = ['the','and','with','for','your','you','is','of','to','on','in','are','this','that','not','from','at','by','we','our','it','be','a','an','or','photos','photo','see','play','next','task','share','copy','download','watch','film','days','planned','trip','search','skip','content','send','email','loading','previous'];
          const hits = ws.filter(w => EN.includes(w)).length;
          if ((ws.length && hits >= 2) || (ws.length <= 3 && hits >= 1 && !/^(email|e-mail|film)$/.test(t.trim().toLowerCase()))) left.add(n.textContent.trim().slice(0, 90));
        }
        const over = [];
        const W = document.documentElement.clientWidth;
        for (const el of document.querySelectorAll('h1,h2,h3,p,a,button,label,dt,dd,li,span')) {
          const r = el.getBoundingClientRect();
          if (r.width && r.right > W + 1 && getComputedStyle(el).position !== 'fixed' && !el.closest('[aria-hidden="true"],.trips,.sl-list,.gr-race,.gf-strip')) over.push(el.tagName + '.' + el.className + ' ' + Math.round(r.right) + ': ' + el.textContent.trim().slice(0, 40));
        }
        return { left: [...left], over: over.slice(0, 12), scrollW: document.documentElement.scrollWidth, W };
      }, keep);
      report[w + ' ' + p] = { ...res, bad };
      if (shots) await page.screenshot({ path: `${out}/${lang}-${p.replace('/', '_').replace('.html', '')}-${w}.png`, fullPage: false });
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(`${out}/probe-${lang}.json`, JSON.stringify(report, null, 1));
  for (const [k, v] of Object.entries(report)) {
    console.log('==', k, 'english-left', v.left.length, 'overflow', v.over.length, 'scrollW', v.scrollW, '/', v.W, 'bad', v.bad.length);
  }
})();
