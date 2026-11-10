"""Grava a tela real do Retrozap (site local, pasta public/ do repo gtorniero/retrozap) no fluxo de verdade:
escolher o arquivo exportado → turma → Ato I → categorias → troféus (pódio, raspadinha, palpite) → card → Gran Finale.
Screencast do Chromium (CDP) em 1080×1920 (viewport 390×693, DPR 2,77), com marcas de tempo por etapa.
Uso: python3 captura_rz.py <pasta public> <arquivo .txt> <saida>"""
import asyncio, base64, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
PUB, CHAT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT + '/frames', exist_ok=True)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8782', '-d', PUB], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
# indicador de toque (como "mostrar toques" da gravação de tela do celular); não muda a interface do produto
TAP = """addEventListener('pointerdown', e => { const d = document.createElement('div');
 d.style.cssText = 'position:fixed;left:'+(e.clientX-22)+'px;top:'+(e.clientY-22)+'px;width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.55);border:2px solid rgba(0,0,0,.25);pointer-events:none;z-index:2147483647;transition:opacity .6s,transform .6s';
 document.documentElement.appendChild(d); requestAnimationFrame(() => { d.style.opacity = '0'; d.style.transform = 'scale(1.5)'; }); setTimeout(() => d.remove(), 700); }, true);"""
frames, marks = [], {}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 693}, device_scale_factor=1080 / 390, has_touch=False)
        await ctx.add_init_script(TAP)
        pg = await ctx.new_page()
        await pg.goto('http://localhost:8782/'); await pg.wait_for_timeout(800)
        if await pg.query_selector('.cookies button'): await pg.click('.cookies button')
        await pg.click('#comecar'); await pg.wait_for_selector('#v2Tenho'); await pg.wait_for_timeout(600)
        cdp = await ctx.new_cdp_session(pg)
        def on_frame(ev):
            frames.append((ev['metadata']['timestamp'], ev['data']))
            asyncio.ensure_future(cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']}))
        cdp.on('Page.screencastFrame', on_frame)
        await cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 92, 'maxWidth': 1080, 'maxHeight': 1920, 'everyNthFrame': 1})
        t0 = time.time()
        def M(k): marks[k] = time.time() - t0; print(f'{k:>14} {marks[k]:6.2f}', flush=True)
        w = pg.wait_for_timeout
        async def tap(sel):
            el = await pg.wait_for_selector(sel); await el.scroll_into_view_if_needed(); bb = await el.bounding_box()
            await pg.mouse.move(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2, steps=8); await w(250)
            await pg.mouse.down(); await w(90); await pg.mouse.up()
        async def rola(dy, ms=1400):
            n = max(1, ms // 40)
            for _ in range(n): await pg.mouse.wheel(0, dy / n); await w(40)
        await pg.mouse.move(195, 600); await w(500)
        M('comecar'); await w(2600)
        async with pg.expect_file_chooser() as fc: await tap('#v2Tenho')
        await w(900); f = await fc.value; await f.set_files(CHAT); M('arquivo')
        await w(3200)  # lembrete de privacidade
        M('lembrete_ok'); await tap('#lbOk')
        await pg.wait_for_selector('#go', timeout=30000); M('turma'); await w(3000)
        if await pg.query_selector('#cmp') and await pg.is_checked('#cmp'): await pg.uncheck('#cmp')
        await rola(260, 1600); await w(1600); M('turma_fim')
        await tap('#go'); await pg.wait_for_selector('.persona', timeout=30000); M('ato1'); await w(4200)
        await rola(320, 1800); await w(2200); M('ato1_fim')
        await tap('#go'); await w(700); M('spoiler')
        if await pg.query_selector('#spX'): await w(2600); await tap('#spX')
        await w(500); M('categorias'); await w(3000); await rola(420, 2000); await w(1500); M('categorias_fim')
        await rola(-600, 600); await tap('#go'); await w(600); M('p1'); await w(2200)  # O Tagarela (pódio)
        await tap('#rvl'); M('p1_rvl'); await w(5200); M('p1_fim')
        await tap('#card'); M('card'); await w(3800); M('card_fim'); await tap('#cl'); await w(700)
        await tap('#next'); await w(600); M('p2'); await w(2200)  # Podcaster (pódio)
        await tap('#rvl'); M('p2_rvl'); await w(5200); M('p2_fim')
        await tap('#next'); await w(600); M('p3'); await w(2400)  # Boca-Suja (raspadinha)
        cv = await pg.query_selector('.scratch canvas'); bb = await cv.bounding_box(); M('p3_raspa')
        await pg.mouse.move(bb['x'] + 20, bb['y'] + 25); await pg.mouse.down()
        for i in range(5):  # raspa devagar, como um dedo de verdade (~3 s)
            y = bb['y'] + 22 + i * (bb['height'] - 40) / 4
            for x in range(0, 31):
                await pg.mouse.move(bb['x'] + 20 + (bb['width'] - 40) * (x / 30 if i % 2 == 0 else 1 - x / 30), y + x / 3); await w(10)
        await pg.mouse.up(); await w(4200); M('p3_fim')
        await tap('#next'); await w(600); M('p4'); await w(3000)  # Rei(nha) do Kkkk (palpite)
        opts = await pg.query_selector_all('.opt'); alvo = None
        for o in opts:
            if (await o.text_content()).strip() == 'Lu': alvo = o
        bb = await (alvo or opts[0]).bounding_box(); await pg.mouse.move(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2, steps=8); await w(300)
        await pg.mouse.down(); await w(90); await pg.mouse.up(); M('p4_palpite'); await w(5000); M('p4_fim')
        # pula o resto da cerimônia (fora do vídeo) até o Gran Finale
        for _ in range(40):
            if '/premios/' not in pg.url: break
            await pg.evaluate("(() => { const o = document.querySelector('.opt:not([disabled])'); if (o) { o.click(); return; } const n = document.querySelector('#next'); if (n) n.click(); })()")
            await w(450)
        await w(800); M('finale')
        await tap('#rl'); await w(3600); M('f1')
        await tap('#rl'); await w(3600); M('f2')
        for _ in range(12):
            if not (await pg.query_selector('#rl') and await pg.is_visible('#rl')): break
            await pg.click('#rl'); await w(500)
        await w(1500); M('fim'); await w(3500); M('fim_fim')
        await cdp.send('Page.stopScreencast'); await b.close()
asyncio.run(main()); srv.terminate()
ts0 = frames[0][0]
for i, (ts, data) in enumerate(frames):
    open(f'{OUT}/frames/{i:05d}.jpg', 'wb').write(base64.b64decode(data))
# marcas no relógio dos frames (diferença pequena entre o relógio do Python e o do Chromium)
json.dump({'frames': [round(ts - ts0, 4) for ts, _ in frames], 'marks': marks, 'offset': 0}, open(f'{OUT}/capture.json', 'w'), indent=0)
print(len(frames), 'frames')
