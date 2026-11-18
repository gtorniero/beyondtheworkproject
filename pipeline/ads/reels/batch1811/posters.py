"""Exporta os pôsteres REAIS do Retrozap (canvas do app, site local public/, ?plano_teste=1 = Premium de teste e ranking simulado)
com conversas fictícias (Dani & Cris; Turma do Churras). Uso: python3 posters.py casal|grupo <chat.txt> <saida>"""
import asyncio, base64, subprocess, sys, time, os
from playwright.async_api import async_playwright
MODO, CHAT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True)
PUB = '/home/user/gtorniero/retrozap/public'; PORT = 8791 if MODO == 'casal' else 8792
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '-d', PUB], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
DRAW = {'casal': ['drawRecibo(state.data)', 'drawAstral()', 'drawBoletim()', 'drawPlacar(state.data)', 'drawCasal(state.data)', 'drawNosso2026()', 'drawResumo(state.data)', 'drawTop10()', 'drawRanking()'],
        'grupo': ['drawProcurado()', 'drawRadio()', 'drawPlantao()', 'drawDiario()', 'drawNumero()', 'drawNosso2026()', 'drawResumo(state.data)', 'drawTop10()', 'drawRanking()']}[MODO]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 390, 'height': 844})
        er = []; pg.on('pageerror', lambda e: er.append(str(e)))
        await pg.goto(f'http://localhost:{PORT}/?zerar=1&plano_teste=1'); await pg.wait_for_timeout(700)
        if await pg.query_selector('.cookies button'): await pg.click('.cookies button')
        if MODO == 'casal': await pg.click('[data-esc=casal]'); await pg.wait_for_timeout(300)
        await pg.click('#comecar'); await pg.wait_for_selector('#v2Tenho'); await pg.evaluate("V2.viaTenho=false; home()"); await pg.wait_for_selector('#file', state='attached')
        await pg.set_input_files('#file', CHAT); await pg.wait_for_timeout(800)
        for sel in ['#lbOk', '#lbSim', '#lbGo']:
            if await pg.query_selector(sel): await pg.click(sel); break
        await pg.wait_for_selector('#pcSim, #go', timeout=30000)
        if await pg.query_selector('#pcSim'): await pg.click('#pcSim')
        await pg.wait_for_selector('#go', timeout=30000); await pg.wait_for_timeout(400)
        if await pg.query_selector('#planoTeste [data-plano=premium]'): await pg.click('#planoTeste [data-plano=premium]'); await pg.wait_for_timeout(300)
        await pg.click('#go'); await pg.wait_for_timeout(2500)
        await pg.evaluate("state.planoTeste='premium'")
        # pula direto para o fim (Gran Finale) e garante o ranking
        await pg.evaluate("(async()=>{ try{ if (typeof comparar==='function') await comparar(); }catch(e){} fimTela(true); })()"); await pg.wait_for_timeout(4000)
        await pg.evaluate("""() => { try { state.comp = simula({total:8, audios:22, figurinhas:15, risadas:31, por_dia:6, madrugada:40, amor:3, coracoes:5, recorde:12, dias:45, hist_total:9, hist_audios:14}); } catch(e) {}
          state.compFeito = true; fimTela(true); }""")
        await pg.wait_for_timeout(9000)
        ims = await pg.evaluate("""async () => { const out = {}; for (const im of document.querySelectorAll('img.rimg')) { if (!im.src) continue;
            const r = await fetch(im.src); const b = await r.blob(); out[im.id] = await new Promise(ok => { const f = new FileReader(); f.onload = () => ok(f.result); f.readAsDataURL(b); }); } return out; }""")
        NM = {'rimg1':'resumo','rimg3':'trofeus','rimg4':'nosso2026','rimg5':'nos-dois','rimg6':'recibo','rimg7':'placar','rimg9':'numero','rimg10':'boletim','rimg13':'mapa-astral','rimg14':'diario','rimg15':'procura-se','rimg16':'radio','rimg17':'plantao','rimg18':'ranking'}
        for k, url in ims.items():
            open(f'{OUT}/{MODO}-{NM.get(k, k)}.png', 'wb').write(base64.b64decode(url.split(',')[1])); print('ok', k, NM.get(k))
        top = {'total':3,'audios':8,'risadas':2,'madrugada':6,'amor':1,'coracoes':4,'recorde':5,'por_dia':4,'figurinhas':9,'dias':40} if MODO=='casal' else {'total':4,'audios':12,'risadas':2,'madrugada':7,'figurinhas':5,'recorde':3,'por_dia':6,'palavrao':9,'furos':8,'dias':45}
        url = await pg.evaluate("""(top) => { state.comp = {pronto:true, n:4210, escopo:'tipo', top}; const r = drawRanking(); const p = typeof drawPlantao==='function' && state.modo!=='casal' ? drawPlantao() : null; return [r, p]; }""", top)
        for nm, u in zip(('ranking', 'plantao'), url):
            if u and isinstance(u, str) and u.startswith('data:'): open(f'{OUT}/{MODO}-{nm}.png', 'wb').write(base64.b64decode(u.split(',')[1])); print('ok', nm)
        await pg.screenshot(path=f'{OUT}/{MODO}-fim.png', full_page=True)
        print('erros', er[:5]); await b.close()
try: asyncio.run(main())
finally: srv.terminate()
