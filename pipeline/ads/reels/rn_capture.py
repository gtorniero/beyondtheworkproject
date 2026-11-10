"""ADC-RN-03 · captura real do RUN DNA (site local, /run/) em 1080×1920, com toques visíveis.
Uso: python3 rn_capture.py <url base, ex. http://localhost:8124> <pasta de saída>
Gera f/NNNNN.jpg com carimbo de tempo (frames.json) e marcas (marks.json). Depois: rn_cfr() em rn03.py vira 30 fps constantes."""
import base64, json, sys, time, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
sys.path.insert(0, str(Path(__file__).parent))
from rk_capture_fonts import gfonts_css
BASE, OUT = sys.argv[1], Path(sys.argv[2]); (OUT / 'f').mkdir(parents=True, exist_ok=True)
K = 5.6  # a página roda K vezes mais devagar na captura; os tempos são divididos por K
SLOWJS = "(()=>{const K=%s;const st=window.setTimeout.bind(window),si=window.setInterval.bind(window);window.setTimeout=(f,d,...a)=>st(f,(d||0)*K,...a);window.setInterval=(f,d,...a)=>si(f,(d||0)*K,...a);})()" % K
TAP = """addEventListener('pointerdown', e => { const d = document.createElement('div');
 d.style.cssText = 'position:fixed;left:'+(e.clientX-24)+'px;top:'+(e.clientY-24)+'px;width:48px;height:48px;border-radius:50%;background:rgba(255,138,61,.45);border:2px solid rgba(10,10,10,.35);pointer-events:none;z-index:2147483647;transition:opacity .5s,transform .5s';
 document.documentElement.appendChild(d); requestAnimationFrame(() => { d.style.opacity = '0'; d.style.transform = 'scale(1.6)'; }); setTimeout(() => d.remove(), 600); }, true);"""
# corredor coerente: 72 kg, pé normal, joelho reclama, gasta o calcanhar por fora, 2 a 5 anos, 20 a 40 km/sem, 5:00 a 6:00, asfalto, meia maratona
ANS = {'largura': 'Normal', 'dor': 'Joelho', 'pisada': 'Calcanhar, mais por fora', 'tempo': '2 a 5 anos', 'km': '20 a 40 km', 'pace': '5:00 a 6:00 /km',
       'terreno': 'Asfalto', 'calor': 'Às vezes', 'obj': 'Meia maratona', 'treino': 'Às vezes', 'sens': 'Equilíbrio', 'prior': 'Conforto', 'neutro': 'Não',
       'orc': 'R$ 500 a 1.000', 'marca': 'Sem preferência', 'uso': 'Não, só para correr', 'pares': 'Sim, único par'}
frames, marks = [], {}; T0 = None; STOP = False
def mark(k): marks[k] = (time.time() - T0) / K; print(k, round(marks[k], 2), flush=True)

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
        CSS = gfonts_css() + f"@font-face{{font-family:'JetBrains Mono';font-style:normal;font-display:swap;font-weight:100 800;src:url(data:font/woff2;base64,{jb}) format('woff2')}}"  # o site também usa JetBrains Mono nos números
        await ctx.route('**/fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=CSS))
        await ctx.route('**/*googletagmanager*/**', lambda r: r.abort())
        pg = await ctx.new_page(); w = lambda ms: pg.wait_for_timeout(ms * K)
        await pg.goto(BASE + '/run/'); await pg.evaluate('document.fonts.ready'); await w(1200)
        bt = pg.get_by_role('button', name='Recusar')
        if await bt.count(): await bt.first.click()
        await w(400)
        cdp = await ctx.new_cdp_session(pg)
        await cdp.send('Animation.enable'); await cdp.send('Animation.setPlaybackRate', {'playbackRate': 1 / K})
        async def tap(el):
            await el.scroll_into_view_if_needed(); bb = await el.bounding_box()
            await pg.mouse.move(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2, steps=6); await w(180)
            await pg.mouse.down(); await w(70); await pg.mouse.up()
        async def glide(y, ms=900):
            await pg.evaluate("""([y1,ms])=>new Promise(r=>{const y0=scrollY,t0=document.timeline.currentTime;const f=()=>{const k=Math.min(1,(document.timeline.currentTime-t0)/ms),e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;scrollTo(0,y0+(y1-y0)*e);k<1?requestAnimationFrame(f):r()};requestAnimationFrame(f)})""", [y, ms])
        async def center(sel_or_el, ms=800, off=0.32):
            el = await pg.query_selector(sel_or_el) if isinstance(sel_or_el, str) else sel_or_el
            y = await el.evaluate("(e,off)=>Math.max(0,e.getBoundingClientRect().top+scrollY-innerHeight*off)", off); await glide(y, ms)
        async def pick(qid, slow=True):
            want = ANS[qid]
            for o in await pg.query_selector_all(f'[id^="o_{qid}_"]'):
                if (await o.inner_text()).strip().split('\n')[0].lower() == want.lower():
                    if slow: await center(o, 700, .45); await w(350); mark('tap_' + qid); await tap(o); await w(900)
                    else: await o.click()
                    return
            raise SystemExit('sem opção ' + qid)
        T0 = time.time(); task = asyncio.create_task(grab(cdp))
        mark('landing'); await w(2200)
        mark('start'); await tap(await pg.query_selector('#start')); await w(1300)
        mark('q_peso'); inp = await pg.query_selector('#q_peso'); await tap(inp); await w(400)
        mark('type_peso'); await pg.keyboard.type('72', delay=260 * K); await w(900)
        await pick('largura'); await pick('dor'); await pick('pisada')
        mark('next1'); await tap(await pg.query_selector('#next')); await w(1300)
        mark('q2'); await pick('tempo', False); await pick('km'); await pick('pace'); await pick('terreno', False); await pick('calor', False)
        await w(300); mark('next2'); await tap(await pg.query_selector('#next')); await w(1100)
        mark('q3'); await pick('obj'); await pick('treino', False)
        mark('next3'); await tap(await pg.query_selector('#next')); await w(1000)
        mark('q4')
        for q in ('sens', 'prior', 'neutro', 'orc', 'marca', 'uso', 'pares'): await pick(q, False)
        await center('#next', 900, .6); await w(500)
        mark('analysis_tap'); await tap(await pg.query_selector('#next'))
        await pg.wait_for_selector('#analysis:not([hidden])'); mark('analysis')
        await pg.wait_for_selector('#preview:not([hidden])', timeout=90000); mark('preview'); await w(1400)
        mark('top3'); await center('#preview .fin', 900, .30); await w(3600)
        mark('tras_go'); await center('#preview .kpis', 1100, .30); mark('tras'); await w(3200)
        mark('perfil_go'); await center('#cardPrev', 1100, .22); mark('perfil'); await w(3400)
        mark('mapa_go'); await center('#preview .tbl', 1100, .25); mark('mapa'); await w(3200)
        mark('end'); STOP = True; await task
        info = await pg.evaluate("()=>({modelos:document.querySelector('#preview .kpi b').textContent,pcts:[...document.querySelectorAll('#preview .pct')].map(e=>e.textContent),kpis:[...document.querySelectorAll('#preview .kpi')].map(e=>e.innerText),nQ:document.querySelector('#nQ').textContent,nBr:document.querySelector('#nBr').textContent,cat:document.querySelector('#preview .arm').innerText,perfil:[...document.querySelectorAll('#preview h3')].map(e=>e.textContent)})")
        (OUT / 'frames.json').write_text(json.dumps(frames)); (OUT / 'marks.json').write_text(json.dumps(marks, indent=1)); (OUT / 'info.json').write_text(json.dumps(info, ensure_ascii=False, indent=1))
        print(len(frames), 'frames', len(frames) / marks['end'], 'fps', info); await b.close()
asyncio.run(main())
