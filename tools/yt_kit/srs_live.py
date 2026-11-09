import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':1280,'height':1600}); pg=await ctx.new_page()
        await pg.goto('https://srs.live/',wait_until='networkidle',timeout=60000); await pg.wait_for_timeout(3000)
        pages=[]
        ctx.on('page',lambda np: pages.append(np))
        await pg.get_by_text('Follow us Live').click(); await pg.wait_for_timeout(8000)
        tgt=pages[-1] if pages else pg
        try: await tgt.wait_for_load_state('networkidle',timeout=30000)
        except Exception: pass
        await tgt.wait_for_timeout(4000)
        print('URL',tgt.url)
        t=await tgt.evaluate('document.body.innerText'); open('live2.txt','w').write(t)
        await tgt.screenshot(path='live2.png'); await b.close()
asyncio.run(main())
