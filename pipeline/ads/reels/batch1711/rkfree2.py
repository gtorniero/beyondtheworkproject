import sys, asyncio
from pathlib import Path
R=Path('../../social/pipeline/ads/reels').resolve()
src=(R/'rk_capture.py').read_text().split('async def main')[0].replace("BASE, OUT = sys.argv[1], Path(sys.argv[2]); (OUT / 'f').mkdir(parents=True, exist_ok=True)","BASE,OUT='https://sportdna.com.br',Path('rk')").replace("Path(__file__).parent / 'fonts'","R/'fonts'")
exec(src)
exec(open('rkcap3.py').read().split('SHOTS=')[0].split("exec(src)")[1])  # BR, BLUR
_ans=answer
async def answer(pg,slow):
    o=pg.locator('#rlist .ropt[data-v]')
    if await o.count() and await o.first.is_visible() and not await pg.locator('#rlist .ropt.sel').count():
        await o.nth(2).click(); await pg.wait_for_timeout(400)
    await _ans(pg,slow)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':390,'height':693},device_scale_factor=1080/390)
        CSS=gfonts_css()
        await ctx.route('**/fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=CSS))
        await ctx.route('**/*googletagmanager*/**',lambda r:r.abort()); await ctx.route('**/*cloudflareinsights*/**',lambda r:r.abort())
        pg=await ctx.new_page(); await pg.goto(BASE+'/racket/'); await pg.wait_for_timeout(2000)
        bt=pg.get_by_role('button',name='Recusar')
        if await bt.count(): await bt.first.click()
        await pg.click('#start'); await pg.wait_for_timeout(800)
        for i in range(14):
            if not await pg.evaluate("()=>!document.querySelector('#quiz').hidden"): break
            await answer(pg,False); await answer(pg,False); await pg.click('#next'); await pg.wait_for_timeout(500)
        await pg.wait_for_selector('#preview:not([hidden]),#report:not([hidden])',timeout=60000); await pg.wait_for_timeout(4000)
        await pg.evaluate(BLUR,BR); await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(500)
        for k,txt,off in [('match','O MATCH DA SUA RAQUETE',.04),('pesa','ONDE ELA ACERTA',.10),('ficha','SUA FICHA IDEAL',.05)]:
            el=pg.get_by_text(txt,exact=False).first
            y=await el.evaluate("(e,off)=>Math.max(0,e.getBoundingClientRect().top+scrollY-innerHeight*off-90)",off)
            await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(900); await pg.screenshot(path=f'scr/racket_free_{k}.jpg',type='jpeg',quality=93)
        await b.close()
asyncio.run(main())
