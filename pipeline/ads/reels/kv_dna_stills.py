"""Telas reais da página do RACKET/SURF DNA (seções do motor e dos erros comuns) para os KVs. Uso: python3 kv_dna_stills.py <pasta de saída> (site em localhost:8812)"""
import asyncio, sys
from playwright.async_api import async_playwright
OUT=sys.argv[1]
SHOTS={'racket':[('motor','O TRABALHO POR TRÁS DO MOTOR',.12),('seis','POR QUE É FÁCIL ERRAR',.10),('erros','Erros comuns na hora de escolher',.10),('hero','LABORATÓRIO DE RAQUETES',.0)],
       'surf':[('motor','Os números do motor',.06),('erros','Erros comuns na hora de escolher',.10),('hero','ANÁLISE TÉCNICA INDEPENDENTE',.0)]}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':390,'height':693},device_scale_factor=1080/390)
        pg=await ctx.new_page()
        for s,L in SHOTS.items():
            await pg.goto(f'http://localhost:8812/{s}/'); await pg.wait_for_timeout(2000)
            bt=pg.get_by_role('button',name='Recusar')
            if await bt.count(): await bt.first.click(); await pg.wait_for_timeout(400)
            for k,txt,off in L:
                el=pg.get_by_text(txt,exact=False).first
                y=await el.evaluate("(e,off)=>Math.max(0,e.getBoundingClientRect().top+scrollY-innerHeight*off)",off)
                await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(1500)
                await pg.screenshot(path=f'{OUT}/{s}_l_{k}.jpg',type='jpeg',quality=92)
        await b.close()
asyncio.run(main())
