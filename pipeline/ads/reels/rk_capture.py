"""ADC-RK-01 v3 · captura real do RACKET DNA (site local) com o screencast do Chromium.
Uso: python3 rk_capture.py <url base, ex. http://localhost:8123> <pasta de saída>
Gera frames JPG com carimbo de tempo (frames.json) e marcas de cena (marks.json)."""
import base64, json, sys, time
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright
sys.path.insert(0, str(Path(__file__).parent))
BASE, OUT = sys.argv[1], Path(sys.argv[2]); (OUT / 'f').mkdir(parents=True, exist_ok=True)
NUM = {'q_age': '34', 'q_height': '178', 'q_weight': '76'}
PICK = {'arm': 'Já tive', 'joint': 'Cotovelo', 'painPast': 'Moderada', 'lvl': 'Intermediário', 'years': '3 a', 'freq': '2 a 3', 'swing': 'Médio',
        'spin': 'Médio', 'style': 'Ataco', 'opp': 'Variada', 'miss': 'longa', 'issue': 'braço', 'why': 'braço', 'want': 'Mais potência',
        'str': 'Na média', 'cond': 'Jogo a partida'}
frames, marks = [], {}
K = 2.2  # o mundo da página roda K vezes mais devagar durante a captura (timers e animações CSS); os tempos são divididos por K na montagem
SLOWJS = "(()=>{const K=%s;const st=window.setTimeout.bind(window),si=window.setInterval.bind(window);window.setTimeout=(f,d,...a)=>st(f,(d||0)*K,...a);window.setInterval=(f,d,...a)=>si(f,(d||0)*K,...a);})()" % K
T0 = None

def mark(k): marks[k] = (time.time() - T0) / K; print(k, round(marks[k], 2), flush=True)

async def answer(pg, slow):
    for q in await pg.query_selector_all('#qs fieldset.q'):
        if not await q.is_visible(): continue
        key = await q.get_attribute('data-q')
        for n in await q.query_selector_all('input[type=number]'):
            if not await n.input_value():
                v = NUM.get(await n.get_attribute('id'), await n.get_attribute('placeholder') or '1')
                if slow: await n.scroll_into_view_if_needed(); await n.click(); await n.type(v, delay=170 * K); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(500 * K)
                else: await n.fill(v)
        if key == 'cur':  # "Minha raquete não está na lista": sem marca de terceiro na tela
            b = await q.query_selector('button.chipbtn[data-v="other"]')
            if b and await b.get_attribute('aria-pressed') != 'true': await b.click()
            continue
        opts = [o for o in await q.query_selector_all('button.opt') if await o.is_visible()]
        if not opts: continue
        if any([await o.get_attribute('aria-pressed') == 'true' for o in opts]): continue
        want = PICK.get(key); ch = None
        for o in opts:
            if want and want.lower() in (await o.inner_text()).lower(): ch = o; break
        ch = ch or opts[min(1, len(opts) - 1)]
        if slow: await ch.scroll_into_view_if_needed(); await pg.wait_for_timeout(400 * K)
        await ch.click()
        if slow: await pg.wait_for_timeout(1000 * K)

async def smooth_to(pg, sel, ms=1600, off=8):
    await pg.evaluate("""([sel,ms,off])=>new Promise(r=>{const el=[...document.querySelectorAll('#preview .eyebrow')].find(e=>e.textContent.trim().toLowerCase()===sel).closest('.panel');const y0=scrollY,y1=el.getBoundingClientRect().top+scrollY-off;const t0=document.timeline.currentTime;
      const f=()=>{const t=document.timeline.currentTime;const k=Math.min(1,(t-t0)/ms),e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;scrollTo(0,y0+(y1-y0)*e);k<1?requestAnimationFrame(f):r()};requestAnimationFrame(f)})""", [sel, ms, off])

STOP = False
async def grab(cdp):
    """Captura a tela a ~30 fps (screenshots CDP em resolução 2x), com carimbo de tempo."""
    while not STOP:
        t = time.time()
        y = (await cdp.send('Runtime.evaluate', {'expression': 'scrollY', 'returnByValue': True}))['result']['value']
        r = await cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 90, 'optimizeForSpeed': True, 'clip': {'x': 0, 'y': y, 'width': 390, 'height': 480, 'scale': 2}})
        n = len(frames); fn = OUT / 'f' / f'{n:05d}.jpg'; fn.write_bytes(base64.b64decode(r['data']))
        frames.append({'f': fn.name, 't': (t - T0) / K})
        await asyncio.sleep(max(0, K / 30 - (time.time() - t)))

FD = Path(__file__).parent / 'fonts'
LAT = 'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD'
def gfonts_css():
    # O proxy desta sessão bloqueia fonts.googleapis.com: servimos as MESMAS fontes do Google (pacotes @fontsource) para a captura sair fiel.
    d = lambda f: 'data:font/woff2;base64,' + base64.b64encode((FD / f).read_bytes()).decode()
    css = ''
    for fam, lat, ext, w, extra in (('Archivo', 'archivo-latin-wght-normal.woff2', 'archivo-latin-ext-wght-normal.woff2', '100 900', ''),
                                    ('DM Sans', 'dm-sans-latin-opsz-normal.woff2', 'dm-sans-latin-ext-opsz-normal.woff2', '100 1000', '')):
        css += f"@font-face{{font-family:'{fam}';font-style:normal;font-display:swap;font-weight:{w};src:url({d(ext)}) format('woff2');unicode-range:U+0100-02AF,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}"
        css += f"@font-face{{font-family:'{fam}';font-style:normal;font-display:swap;font-weight:{w};src:url({d(lat)}) format('woff2');unicode-range:{LAT}}}"
    for w in ('700', '800'):
        css += f"@font-face{{font-family:'Syne';font-style:normal;font-display:swap;font-weight:{w};src:url({d(f'syne-latin-{w}-normal.woff2')}) format('woff2')}}"
    return css

async def main():
    global T0, STOP
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 480}, device_scale_factor=2)
        await ctx.add_init_script(SLOWJS)
        CSS = gfonts_css()
        await ctx.route('**/fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=CSS))
        await ctx.route('**/*googletagmanager*/**', lambda r: r.abort())
        pg = await ctx.new_page()
        await pg.goto(BASE + '/racket/'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(1500 * K)
        bt = pg.get_by_role('button', name='Recusar')  # banner de cookies: a escolha de quem visita
        if await bt.count(): await bt.first.click()
        await pg.wait_for_timeout(500 * K)
        cdp = await ctx.new_cdp_session(pg)
        await cdp.send('Animation.enable'); await cdp.send('Animation.setPlaybackRate', {'playbackRate': 1 / K})
        T0 = time.time(); task = asyncio.create_task(grab(cdp))
        mark('landing'); await pg.wait_for_timeout(2500 * K)
        mark('start'); await pg.click('#start'); await pg.wait_for_timeout(1200 * K)
        mark('q1'); await answer(pg, True); await pg.wait_for_timeout(600 * K)
        await pg.click('#next'); await pg.wait_for_timeout(1000 * K)
        mark('q2'); await answer(pg, True); await answer(pg, True); await pg.wait_for_timeout(600 * K)
        await pg.click('#next'); await pg.wait_for_timeout(1000 * K)
        mark('q3'); await answer(pg, True); await pg.wait_for_timeout(500 * K)
        mark('fast')
        for _ in range(12):
            if not await pg.evaluate("()=>!document.querySelector('#quiz').hidden"): break
            await answer(pg, False); await answer(pg, False)
            await pg.evaluate("()=>scrollTo(0,0)"); await pg.wait_for_timeout(150 * K)
            mark('analysis'); await pg.click('#next'); await pg.wait_for_timeout(500 * K)
        await pg.wait_for_selector('#preview:not([hidden])', timeout=60000); mark('preview'); await pg.wait_for_timeout(900 * K)
        await smooth_to(pg, 'análise concluída', 1400); mark('top3'); await pg.wait_for_timeout(3400 * K)
        mark('tras_go'); await smooth_to(pg, 'o que está por trás', 1800, 20); mark('tras'); await pg.wait_for_timeout(3600 * K)
        mark('dna_go'); await smooth_to(pg, 'seu dna de jogo', 1800, 20); mark('dna'); await pg.wait_for_timeout(3800 * K)
        mark('end'); STOP = True; await task
        (OUT / 'frames.json').write_text(json.dumps(frames)); (OUT / 'marks.json').write_text(json.dumps(marks, indent=1))
        print(len(frames), 'frames'); await b.close()

asyncio.run(main())
