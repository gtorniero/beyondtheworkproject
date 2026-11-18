import sys, asyncio
from pathlib import Path
R=Path('../../social/pipeline/ads/reels').resolve()
src=(R/'rk_capture.py').read_text().split('async def main')[0].replace("BASE, OUT = sys.argv[1], Path(sys.argv[2]); (OUT / 'f').mkdir(parents=True, exist_ok=True)","BASE,OUT='https://sportdna.com.br',Path('rk')").replace("Path(__file__).parent / 'fonts'","R/'fonts'")
exec(src)
BR=r"Mercado Livre|1080|v1[0-9]|Infinion|Nike|NIKE|Vomero|VOMERO|Asics|ASICS|Adidas|ADIDAS|Mizuno|MIZUNO|Olympikus|OLYMPIKUS|Hoka|HOKA|Brooks|BROOKS|Saucony|SAUCONY|New Balance|NEW BALANCE|Puma|PUMA|Fila|FILA|Pegasus|Novablast|Nimbus|Kayano|Clifton|Bondi|Ghost|Glycerin|Ultraboost|Adizero|Wave|Endorphin|Kinvara|Fresh Foam|Superblast|Magic Speed|Boston|Zoom|Gel-|Head|HEAD|Wilson|WILSON|Babolat|BABOLAT|Yonex|YONEX|Prince|PRINCE|Tecnifibre|Dunlop|Boom|Clash|Blade|Speed|Pure|Gravity|Radical|Extreme|Prestige|Ezone|EZONE|VCORE|Percept|Pro Staff|Ultra|Shift|Phantom|Coco|Gauff|Musetti|Navone|Trungelliti|Lorenzo|Mariano|Marco|Channel Islands|Lost|Pyzel|Firewire|Sharp Eye|Rusty|Merrick|Mayhem|Torq|Tokoro|Pukas|Surftech|Zampol|Lucas|DHD|JS "
BLUR="""(re)=>{const R=new RegExp(re);const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const ns=[];while(w.nextNode())ns.push(w.currentNode);
for(const n of ns){if(!R.test(n.textContent))continue;const p=n.parentElement;if(!p||p.closest('script,style'))continue;const s=document.createElement('span');s.style.filter='blur(7px)';n.replaceWith(s);s.append(n)}
document.querySelectorAll('img').forEach(i=>{if(/flag|bandeira/i.test(i.alt||''))i.style.filter='blur(7px)'})}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':390,'height':693},device_scale_factor=1080/390)
        CSS=gfonts_css()
        await ctx.route('**/fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=CSS))
        await ctx.route('**/*googletagmanager*/**',lambda r:r.abort()); await ctx.route('**/*cloudflareinsights*/**',lambda r:r.abort())
        pg=await ctx.new_page()
        await pg.goto(f'{BASE}/run/'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(2500)
        bt=pg.get_by_role('button',name='Recusar')
        if await bt.count(): await bt.first.click()
        await pg.evaluate(BLUR,BR); await pg.screenshot(path='scr/run2_land.jpg',type='jpeg',quality=93)
        await pg.evaluate("document.querySelector('#example').click()")
        await pg.wait_for_selector('#report:not([hidden]),#preview:not([hidden])',timeout=60000); await pg.wait_for_timeout(3500)
        await pg.evaluate(BLUR,BR)
        for k,txt,off in [('res','DNA Score',.30),('meli','Mercado Livre',.55),('km','por km',.45),('fin','finalistas',.10)]:
            el=pg.get_by_text(txt,exact=False).first
            if not await el.count(): print('sem',txt); continue
            y=await el.evaluate("(e,off)=>Math.max(0,e.getBoundingClientRect().top+scrollY-130-innerHeight*off)",off)
            await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(1200)
            await pg.evaluate(BLUR,BR)
            await pg.screenshot(path=f'scr/run2_{k}.jpg',type='jpeg',quality=93); print('ok',k)
        await b.close()
asyncio.run(main())
