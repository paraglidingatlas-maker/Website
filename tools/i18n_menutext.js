// The site menu's text as rendered (v4-menu.js builds it): node tools/i18n_menutext.js, with the repo served on 8765. Its strings go in config "js".
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const out = new Set();
  for (const w of [1300, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 }, isMobile: w < 500, hasTouch: w < 500 });
    for (const u of ['index.html', 'enquire.html']) {
      const p = await ctx.newPage(); await p.goto('http://127.0.0.1:8765/prototypes/v4/' + u); await p.waitForTimeout(1200);
      const before = await p.evaluate(() => document.body.innerText.length);
      await p.click(w < 500 ? '.nav-toggle' : '.v4-open'); await p.waitForTimeout(900);
      const t = await p.evaluate(() => { const m = (document.querySelector('.v4-menu-in')||{}).parentElement; const r = []; if (!m) return ['NO MENU'];
        const tw = document.createTreeWalker(m, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT); let n;
        while ((n = tw.nextNode())) { if (n.nodeType === 3) { const s = n.data.replace(/\s+/g, ' ').trim(); if (/[A-Za-z]{2}/.test(s)) r.push(s); } else { for (const a of ['placeholder', 'aria-label', 'title']) { const v = n.getAttribute(a); if (v) r.push(v); } } }
        return r; });
      t.forEach(s => out.add(s)); await p.close();
    }
    await ctx.close();
  }
  console.log(JSON.stringify([...out], null, 0)); await b.close();
})();
