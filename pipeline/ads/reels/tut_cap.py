"""Tutoriais Retrozap (11/11): grava a tela REAL do site (pasta public/ do repo gtorniero/retrozap, servida local) no fluxo
atual do onboarding v2, do início ao "Salvar ou compartilhar", com conversa fictícia exportada no formato do aparelho.
- Aparelho pelo user agent (o site escolhe a aba iPhone/Android sozinho).
- /api/cobranca responde como a produção (cobrança ligada, R$ 8,99, cartão): grupo = 1º grátis; casal = paywall depois do Ato I.
  No casal, o paywall real aparece e é gravado; depois a captura segue com acesso liberado (o pagamento em si não é gravado).
- O WhatsApp é outro app: aqui o toque em "Abrir o WhatsApp" é só marcado e a volta é a função real do site (v2Voltou).
- Toques visíveis (como "mostrar toques" do celular). Screencast CDP 1080×1920 (viewport 390×693).
Uso: python3 tut_cap.py <public> <grupo|casal> <android|iphone> <arquivo> <saida>"""
import asyncio, base64, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
PUB, MODO, HOW, CHAT, OUT = sys.argv[1:6]
os.makedirs(OUT + '/frames', exist_ok=True)
PORT = 8791 if MODO == 'grupo' else 8792
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '-d', PUB], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
UA = {'android': 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Mobile Safari/537.36',
      'iphone': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'}[HOW]
COR = '255,194,60' if MODO == 'grupo' else '200,22,82'
TAP = """addEventListener('pointerdown', e => { for (const k of [0, 1]) { const d = document.createElement('div'), s = k ? 70 : 46;
 d.style.cssText = 'position:fixed;left:'+(e.clientX-s/2)+'px;top:'+(e.clientY-s/2)+'px;width:'+s+'px;height:'+s+'px;border-radius:50%;pointer-events:none;z-index:2147483647;transition:opacity .8s,transform .8s;' + (k ? 'border:4px solid rgba(COR,.95)' : 'background:rgba(255,255,255,.7);border:3px solid rgba(COR,1)');
 document.documentElement.appendChild(d); requestAnimationFrame(() => { d.style.opacity = '0'; d.style.transform = 'scale(' + (k ? 1.9 : 1.2) + ')'; }); setTimeout(() => d.remove(), 900); } }, true);""".replace('COR', COR)
COBRANCA = json.dumps({'modo': 'ligada', 'pronto': True, 'preco': '8,99', 'cartao': True, 'cartaoTeste': False, 'precoCartao': '8,99'})
frames, marks = [], {}


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 693}, device_scale_factor=1080 / 390, user_agent=UA, locale='pt-BR')
        await ctx.add_init_script(TAP)
        await ctx.add_init_script("navigator.canShare = () => true; navigator.share = () => new Promise(r => setTimeout(r, 1200));")
        await ctx.route('**/api/cobranca', lambda r: r.fulfill(status=200, content_type='application/json', body=COBRANCA))
        pg = await ctx.new_page()
        await pg.goto(f'http://localhost:{PORT}/?zerar=1'); await pg.wait_for_timeout(1000)
        if await pg.query_selector('.cookies button'): await pg.click('.cookies button')
        await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(500)
        cdp = await ctx.new_cdp_session(pg)

        def on_frame(ev):
            frames.append((ev['metadata']['timestamp'], ev['data'])); asyncio.ensure_future(cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']}))
        cdp.on('Page.screencastFrame', on_frame)
        await cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 92, 'maxWidth': 1080, 'maxHeight': 1920, 'everyNthFrame': 1})
        t0 = time.time(); w = pg.wait_for_timeout

        def M(k): marks[k] = round(time.time() - t0, 2); print(f'{k:>22} {marks[k]:7.2f}', flush=True)

        async def vis(sel):
            e = await pg.query_selector(sel); return e if e and await e.is_visible() else None

        async def mira(sel=None, el=None):
            el = el or await pg.wait_for_selector(sel, timeout=30000); await el.scroll_into_view_if_needed(); await w(250); bb = await el.bounding_box()
            x, y = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2; await pg.mouse.move(x, y, steps=10); await w(300); return x, y

        async def tap(sel=None, el=None):
            await mira(sel, el); await pg.mouse.down(); await w(90); await pg.mouse.up()

        async def rola(dy, ms=1400):
            n = max(1, ms // 40)
            for _ in range(n): await pg.mouse.wheel(0, dy / n); await w(40)

        await pg.mouse.move(195, 640); await w(800); M('inicio'); await w(2200)
        if MODO == 'casal': await tap('[data-esc="casal"]'); M('casal'); await w(2200)
        await tap('#comecar'); M('caminho'); await w(3200)
        await tap('#v2Exportar'); await w(300)
        k = 1
        while True:
            M(f'passo{k}'); await w(5600)
            if not await vis('#v2Prox'): break
            await tap('#v2Prox'); k += 1; await w(300)
        # último passo: "Agora é no WhatsApp". O toque em Abrir o WhatsApp é marcado; o WhatsApp é outro app.
        x, y = await mira('#abreWa'); await w(600)
        await pg.evaluate(f"dispatchEvent(new PointerEvent('pointerdown', {{clientX: {x}, clientY: {y}, bubbles: true}}))"); M('abre_wa'); await w(1600)
        await pg.evaluate('state.esperandoWhats = true; V2.saiu = true; v2Voltou()'); await pg.evaluate('scrollTo(0,0)'); M('voltou'); await w(3800)
        async with pg.expect_file_chooser() as fc: await tap('#v2Drop')
        M('seletor'); await w(1200); f = await fc.value; await f.set_files(CHAT); M('arquivo')
        for _ in range(60):
            await w(400)
            if await vis('#lbOk'): M('lembrete'); await w(3000); await tap('#lbOk'); M('lembrete_ok')
            if await vis('#pcSim'): M('quem_sao'); await w(2600); await tap('#pcSim'); M('somos_casal')
            if await vis('#go'): break
        M('turma'); await w(3600); await rola(300, 1600); await w(1400); M('turma_fim')
        await tap('#go'); await pg.wait_for_selector('.persona', timeout=30000); M('ato1'); await w(4200)
        await rola(380, 2000); await w(2400); M('ato1_fim')
        await tap('#go'); await w(900)
        if MODO == 'casal':
            await pg.wait_for_selector('.pw', timeout=15000); M('paywall'); await w(4200); await rola(220, 1200); await w(1800); M('paywall_fim')
            await pg.evaluate("document.querySelector('.patro')?.remove(); localStorage.setItem('rz_acesso', 'RZ-TUTO-2026')")
            await tap('#go'); await w(900); M('pos_pagamento')
        n = 0
        for _ in range(160):  # cerimônia
            if await vis('#spX'): M('spoiler'); await w(2400); await tap('#spX'); await w(700); continue
            if n >= 2 and '/premios/' in pg.url:  # depois de 2 troféus, avança rápido (fica fora do vídeo)
                M('pula');
                for _ in range(60):
                    if '/premios/' not in pg.url: break
                    await pg.evaluate("(() => { const o = document.querySelector('.opt:not([disabled])'); if (o) { o.click(); return; } const r = document.querySelector('#rvl'); if (r) { r.click(); return; } const n = document.querySelector('#next'); if (n) n.click(); })()")
                    await w(350)
                continue
            if await vis('.scratch canvas'):
                cv = await pg.query_selector('.scratch canvas'); bb = await cv.bounding_box(); n += 1; M(f't{n}_raspa')
                await pg.mouse.move(bb['x'] + 20, bb['y'] + 25); await pg.mouse.down()
                for i in range(5):
                    yy = bb['y'] + 22 + i * (bb['height'] - 40) / 4
                    for xx in range(0, 31): await pg.mouse.move(bb['x'] + 20 + (bb['width'] - 40) * (xx / 30 if i % 2 == 0 else 1 - xx / 30), yy + xx / 3); await w(10)
                await pg.mouse.up(); await w(4200); M(f't{n}_fim')
                if await vis('#next'): await tap('#next'); await w(700)
                continue
            if await vis('.opt:not([disabled])'):
                n += 1; M(f't{n}_palpite'); await w(2600)
                await tap(el=(await pg.query_selector_all('.opt:not([disabled])'))[0]); await w(4600); M(f't{n}_fim')
                if await vis('#next'): await tap('#next'); await w(700)
                continue
            if await vis('#rvl'):
                n += 1; M(f't{n}_podio'); await w(2400); await tap('#rvl'); M(f't{n}_rvl'); await w(5200); M(f't{n}_fim')
                if await vis('#next'): await tap('#next'); await w(700)
                continue
            if await vis('#rl'): break
            if await vis('#go'):
                M('go'); await w(2600); await tap('#go'); await w(900); continue
            if await vis('#next'): M('next'); await w(1400); await tap('#next'); await w(800); continue
            await w(600)
        M('finale'); await w(2600)
        for i in range(16):
            if not await vis('#rl'): break
            await tap('#rl'); M(f'f{i}'); await w(3600)
        await w(1200); M('fim'); await w(4200)
        # compartilha uma imagem do carrossel (item 2): grupo = Diário da Turma (o vídeo do grupo é Premium); casal = Recibo do amor
        await tap('.carr-lado[data-carr="1"]'); M('carr_prox'); await w(2600)
        await mira('#sv14' if MODO == 'grupo' else '#sv6'); M('fim_botao'); await w(1500)
        await pg.mouse.down(); await w(90); await pg.mouse.up(); M('compartilhar'); await w(3500)
        M('compartilhou'); await w(3000); M('fim_fim')
        await cdp.send('Page.stopScreencast'); await b.close()

asyncio.run(main()); srv.terminate()
ts0 = frames[0][0]
for i, (ts, data) in enumerate(frames): open(f'{OUT}/frames/{i:05d}.jpg', 'wb').write(base64.b64decode(data))
json.dump({'frames': [round(ts - ts0, 4) for ts, _ in frames], 'marks': marks, 'offset': 0}, open(f'{OUT}/capture.json', 'w'), indent=0)
print(len(frames), 'frames')
