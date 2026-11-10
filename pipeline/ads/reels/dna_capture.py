"""Captura real dos testes da SPORT DNA (site local) em 1080×1920, com toques visíveis. Genérico para racket e surf (o RUN usa rn_capture.py).
Uso: python3 dna_capture.py <racket|surf> <url base, ex. http://localhost:8124> <pasta de saída>
Gera f/NNNNN.jpg + frames.json (tempo de cada quadro), marks.json (marcas de cena) e info.json (números que a tela mostrou)."""
import base64, json, sys, time, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
sys.path.insert(0, str(Path(__file__).parent))
from rk_capture_fonts import gfonts_css
SPORT, BASE, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]); (OUT / 'f').mkdir(parents=True, exist_ok=True)
CFG = {
 # jogador coerente: 34 anos, 178 cm, 76 kg, intermediário, ataca do fundo, já teve dor no cotovelo
 'racket': dict(color='221,242,71', NUM={'q_age': '34', 'q_height': '178', 'q_weight': '76'},
                PICK={'arm': 'Já tive', 'joint': 'Cotovelo', 'painPast': 'Moderada', 'lvl': 'Intermediário', 'years': '3 a', 'freq': '2 a 3', 'swing': 'Médio', 'spin': 'Médio',
                      'style': 'Ataco', 'opp': 'Variada', 'miss': 'longa', 'issue': 'braço', 'why': 'braço', 'want': 'Mais potência', 'str': 'Na média', 'cond': 'Jogo a partida'},
                slow=['arm', 'lvl', 'style']),
 # surfista coerente: 74 kg, 176 cm, 26 a 35, intermediário, 3 a 6 vezes por mês, onda de meio metro a 1 m
 'surf': dict(color='108,207,246', NUM={'q_peso': '74', 'q_altura': '176'},
              PICK={'idade': '26 a 35', 'fis': 'Razoável', 'dor': 'Nenhuma', 'motivo': 'Voltar a surfar', 'uso': 'Prancha única', 'atual_mod': 'Não tenho', 'nivel': 'Intermediário', 'tempo': '3 a 6',
                    'freq': '3 a 6 vezes', 'objv': 'manobra', 'estilo': 'Fazer curvas', 'tam': 'Meio metro a 1', 'forca': 'Mistas'},
              slow=['peso', 'nivel', 'freq', 'tam']),
}[SPORT]
K = 5.6  # a página roda K vezes mais devagar na captura; os tempos são divididos por K
SLOWJS = "(()=>{const K=%s;const st=window.setTimeout.bind(window),si=window.setInterval.bind(window);window.setTimeout=(f,d,...a)=>st(f,(d||0)*K,...a);window.setInterval=(f,d,...a)=>si(f,(d||0)*K,...a);})()" % K
TAP = """addEventListener('pointerdown', e => { const d = document.createElement('div');
 d.style.cssText = 'position:fixed;left:'+(e.clientX-24)+'px;top:'+(e.clientY-24)+'px;width:48px;height:48px;border-radius:50%;background:rgba(RGB,.5);border:2px solid rgba(10,10,10,.35);pointer-events:none;z-index:2147483647;transition:opacity .5s,transform .5s';
 document.documentElement.appendChild(d); requestAnimationFrame(() => { d.style.opacity = '0'; d.style.transform = 'scale(1.6)'; }); setTimeout(() => d.remove(), 600); }, true);""".replace('RGB', CFG['color'])
frames, marks = [], {}; T0 = None; STOP = False
def mark(k):
    if k not in marks: marks[k] = (time.time() - T0) / K; print(k, round(marks[k], 2), flush=True)

async def grab(cdp):
    while not STOP:
        t = time.time()
        y = (await cdp.send('Runtime.evaluate', {'expression': 'scrollY', 'returnByValue': True}))['result']['value']
        r = await cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 90, 'optimizeForSpeed': True, 'clip': {'x': 0, 'y': y, 'width': 390, 'height': 693, 'scale': 1080 / 390}})
        n = len(frames); (OUT / 'f' / f'{n:05d}.jpg').write_bytes(base64.b64decode(r['data']))
        frames.append({'f': f'{n:05d}.jpg', 't': (t - T0) / K})
        await asyncio.sleep(max(0, K / 30 - (time.time() - t)))

async def main():
    global T0, STOP
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 693}, device_scale_factor=1080 / 390)
        await ctx.add_init_script(SLOWJS); await ctx.add_init_script(TAP)
        jb = base64.b64encode((Path(__file__).resolve().parent.parent.parent / 'fonts' / 'JBMono-var.woff2').read_bytes()).decode()
        CSS = gfonts_css() + f"@font-face{{font-family:'JetBrains Mono';font-style:normal;font-display:swap;font-weight:100 800;src:url(data:font/woff2;base64,{jb}) format('woff2')}}"
        await ctx.route('**/fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=CSS))
        await ctx.route('**/*googletagmanager*/**', lambda r: r.abort())
        pg = await ctx.new_page(); w = lambda ms: pg.wait_for_timeout(ms * K)
        await pg.goto(f'{BASE}/{SPORT}/'); await pg.evaluate('document.fonts.ready'); await w(1200)
        bt = pg.get_by_role('button', name='Recusar')
        if await bt.count(): await bt.first.click()
        await w(400)
        motor = await pg.evaluate("()=>[...document.querySelectorAll('[data-n]')].map(e=>[e.dataset.n,e.textContent.trim(),(e.parentElement.innerText||'').trim().slice(0,160)])")
        cdp = await ctx.new_cdp_session(pg)
        await cdp.send('Animation.enable'); await cdp.send('Animation.setPlaybackRate', {'playbackRate': 1 / K})
        async def tap(el):
            bb = await el.bounding_box()
            await pg.mouse.move(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2, steps=6); await w(180)
            await pg.mouse.down(); await w(70); await pg.mouse.up()
        async def glide(y, ms=900):
            await pg.evaluate("""([y1,ms])=>new Promise(r=>{const y0=scrollY,t0=document.timeline.currentTime;const f=()=>{const k=Math.min(1,(document.timeline.currentTime-t0)/ms),e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;scrollTo(0,y0+(y1-y0)*e);k<1?requestAnimationFrame(f):r()};requestAnimationFrame(f)})""", [y, ms])
        async def center(el, ms=800, off=0.32):
            if isinstance(el, str): el = await pg.query_selector(el)
            y = await el.evaluate("(e,off)=>Math.max(0,e.getBoundingClientRect().top+scrollY-innerHeight*off)", off); await glide(y, ms)
        async def answer():
            """Uma passada pelas perguntas visíveis; devolve quantas respondeu (a tela pode se redesenhar, então chame de novo)."""
            n = 0
            for q in await pg.query_selector_all('#qs fieldset.q'):
                try:
                    if not await q.is_visible(): continue
                    key = await q.get_attribute('data-q'); slow = key in CFG['slow']
                    for inp in await q.query_selector_all('input[type=number]'):
                        if await inp.input_value(): continue
                        iid = await inp.get_attribute('id'); v = CFG['NUM'].get(iid)
                        if v is None: continue
                        if slow or iid in ('q_peso', 'q_weight'):
                            await center(inp, 700, .4); await w(300); mark('tap_' + key); await tap(inp); await w(350); mark('type_' + key)
                            await pg.keyboard.type(v, delay=260 * K); await w(700); await pg.keyboard.press('Tab'); await w(400)
                        else: await inp.fill(v); await inp.dispatch_event('change')
                        n += 1
                    if key == 'cur':
                        bq = await q.query_selector('button.chipbtn[data-v="other"]')
                        if bq and await bq.get_attribute('aria-pressed') != 'true': await bq.click(); n += 1
                        continue
                    opts = [o for o in await q.query_selector_all('button.opt') if await o.is_visible()]
                    if not opts or any([await o.get_attribute('aria-pressed') == 'true' for o in opts]): continue
                    want = CFG['PICK'].get(key); ch = None
                    for o in opts:
                        if want and want.lower() in (await o.inner_text()).lower(): ch = o; break
                    ch = ch or opts[min(1, len(opts) - 1)]
                    if slow: await center(ch, 700, .45); await w(350); mark('tap_' + key); await tap(ch); await w(1000)
                    else: await ch.click()
                    n += 1
                except Exception as e:
                    if 'detached' in str(e) or 'not attached' in str(e): return n + 1
                    raise
            return n
        T0 = time.time(); task = asyncio.create_task(grab(cdp))
        mark('landing'); await w(2200)
        mark('start'); await tap(await pg.query_selector('#start')); await w(1300)
        for step in range(12):
            if await pg.evaluate("()=>document.querySelector('#quiz').hidden"): break
            mark(f'step{step}')
            for _ in range(6):
                if not await answer(): break
                await w(150)
            nx = await pg.query_selector('#next'); await center(nx, 700, .6); await w(300)
            mark(f'next{step}'); await tap(nx); await w(1100)
        await pg.wait_for_selector('#analysis:not([hidden]),#preview:not([hidden])', timeout=60000); mark('analysis')
        await pg.wait_for_selector('#preview:not([hidden])', timeout=90000); mark('preview'); await w(1400)
        mark('top3'); await center('#preview .fin', 900, .34); await w(3800)
        mark('tras_go'); await center('#preview .kpis', 1100, .30); mark('tras'); await w(3200)
        mark('card_go'); await center('#cardPrev', 1100, .16); mark('card'); await w(3600)
        mark('end'); STOP = True; await task
        info = await pg.evaluate("()=>({pcts:[...document.querySelectorAll('#preview .fin .pct')].map(e=>e.textContent),kpis:[...document.querySelectorAll('#preview .kpi')].map(e=>e.innerText),h:[...document.querySelectorAll('#preview h2,#preview h3')].map(e=>e.textContent)})")
        info['motor'] = motor; info['alist'] = await pg.evaluate("()=>[...document.querySelectorAll('#alist li')].map(e=>e.innerText)")
        (OUT / 'frames.json').write_text(json.dumps(frames)); (OUT / 'marks.json').write_text(json.dumps(marks, indent=1)); (OUT / 'info.json').write_text(json.dumps(info, ensure_ascii=False, indent=1))
        print(len(frames), 'frames', len(frames) / marks['end'], 'fps', json.dumps(info, ensure_ascii=False)); await b.close()
asyncio.run(main())
