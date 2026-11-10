"""Grava a retrospectiva de CASAL real do Retrozap (site local, pasta public/ do repo gtorniero/retrozap):
tipo Casal → escolher o arquivo → nomes → Ato I → categorias → troféus (pódio, palpite, raspadinha) → Gran Finale.
Screencast do Chromium em 1080×1920 (viewport 390×693, DPR 2,77), com toques visíveis e marcas por etapa.
Uso: python3 captura_casal.py <pasta public> <arquivo .txt> <saida>"""
import asyncio, base64, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
PUB, CHAT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT + '/frames', exist_ok=True)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8783', '-d', PUB], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
TAP = """addEventListener('pointerdown', e => { const d = document.createElement('div');
 d.style.cssText = 'position:fixed;left:'+(e.clientX-22)+'px;top:'+(e.clientY-22)+'px;width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.6);border:2px solid rgba(94,11,43,.3);pointer-events:none;z-index:2147483647;transition:opacity .6s,transform .6s';
 document.documentElement.appendChild(d); requestAnimationFrame(() => { d.style.opacity = '0'; d.style.transform = 'scale(1.5)'; }); setTimeout(() => d.remove(), 700); }, true);"""
frames, marks = [], {}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 693}, device_scale_factor=1080 / 390)
        await ctx.add_init_script(TAP); pg = await ctx.new_page()
        await pg.goto('http://localhost:8783/?zerar=1'); await pg.wait_for_timeout(900)
        if await pg.query_selector('.cookies button'): await pg.click('.cookies button')
        await pg.click('#comecar'); await pg.wait_for_selector('#v2Tenho'); await pg.wait_for_timeout(500)
        cdp = await ctx.new_cdp_session(pg)
        def on_frame(ev):
            frames.append((ev['metadata']['timestamp'], ev['data'])); asyncio.ensure_future(cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']}))
        cdp.on('Page.screencastFrame', on_frame)
        await cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 92, 'maxWidth': 1080, 'maxHeight': 1920, 'everyNthFrame': 1})
        t0 = time.time(); w = pg.wait_for_timeout
        def M(k): marks[k] = round(time.time() - t0, 2); print(f'{k:>18} {marks[k]:6.2f}', flush=True)
        async def tap(sel, el=None):
            el = el or await pg.wait_for_selector(sel, timeout=20000); await el.scroll_into_view_if_needed(); bb = await el.bounding_box()
            await pg.mouse.move(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2, steps=8); await w(250); await pg.mouse.down(); await w(90); await pg.mouse.up()
        async def vis(sel):
            e = await pg.query_selector(sel); return e if e and await e.is_visible() else None
        async def rola(dy, ms=1400):
            n = max(1, ms // 40)
            for _ in range(n): await pg.mouse.wheel(0, dy / n); await w(40)
        await pg.mouse.move(195, 600); await w(600); M('inicio')
        if await vis('[data-tipo="casal"]'): await tap('[data-tipo="casal"]'); await w(1400); M('tipo_casal')
        async with pg.expect_file_chooser() as fc: await tap('#v2Tenho')
        await w(800); f = await fc.value; await f.set_files(CHAT); M('arquivo')
        for _ in range(30):
            await w(500)
            if await vis('#lbOk'): await w(2000); await tap('#lbOk'); M('lembrete_ok')
            if await vis('#pcSim'): await w(1500); await tap('#pcSim'); M('somos_casal')
            if await vis('#go'): break
        M('nomes'); await w(3000)
        if await vis('#cmp') and await pg.is_checked('#cmp'): await pg.uncheck('#cmp')
        await rola(260, 1400); await w(1200); await tap('#go'); M('ato1'); await w(4500)
        await rola(320, 1800); await w(2400); M('ato1_fim')
        n = 0
        for _ in range(140):  # cerimônia: avança tela a tela, interagindo como gente
            url = pg.url; h = (await pg.evaluate("(document.querySelector('h1,h2')||{}).textContent||''")).strip()[:40]
            if await vis('#spX'): await w(2200); await tap('#spX'); M(f'spoiler'); await w(800); continue
            if await vis('.scratch canvas'):
                cv = await pg.query_selector('.scratch canvas'); bb = await cv.bounding_box(); n += 1; M(f't{n}_raspa {h}')
                await pg.mouse.move(bb['x'] + 20, bb['y'] + 25); await pg.mouse.down()
                for i in range(5):
                    y = bb['y'] + 22 + i * (bb['height'] - 40) / 4
                    for x in range(0, 31): await pg.mouse.move(bb['x'] + 20 + (bb['width'] - 40) * (x / 30 if i % 2 == 0 else 1 - x / 30), y + x / 3); await w(10)
                await pg.mouse.up(); await w(4200); M(f't{n}_fim')
                if await vis('#next'): await tap('#next'); await w(700)
                continue
            if await vis('.opt:not([disabled])'):
                n += 1; M(f't{n}_palpite {h}'); await w(2600)
                await tap(None, (await pg.query_selector_all('.opt:not([disabled])'))[0]); await w(4600); M(f't{n}_fim')
                if await vis('#next'): await tap('#next'); await w(700)
                continue
            if await vis('#rvl'):
                n += 1; M(f't{n}_podio {h}'); await w(2400); await tap('#rvl'); M(f't{n}_rvl'); await w(5200); M(f't{n}_fim')
                if await vis('#next'): await tap('#next'); await w(700)
                continue
            if await vis('#rl'): break
            if await vis('#go'):
                txt = (await (await pg.query_selector('#go')).text_content()).strip()[:30]; M(f'go {txt} | {h}'); await w(3000)
                await tap('#go'); await w(900); continue
            if await vis('#next'): M(f'next | {h}'); await w(1500); await tap('#next'); await w(800); continue
            await w(800)
        M('finale'); await w(2500)
        for i in range(14):
            if not await vis('#rl'): break
            await tap('#rl'); M(f'f{i}'); await w(3400)
        await w(1500); M('fim'); await w(3500); M('fim_fim')
        await cdp.send('Page.stopScreencast'); await b.close()
asyncio.run(main()); srv.terminate()
ts0 = frames[0][0]
for i, (ts, data) in enumerate(frames): open(f'{OUT}/frames/{i:05d}.jpg', 'wb').write(base64.b64decode(data))
json.dump({'frames': [round(ts - ts0, 4) for ts, _ in frames], 'marks': marks}, open(f'{OUT}/capture.json', 'w'), indent=0)
print(len(frames), 'frames')
