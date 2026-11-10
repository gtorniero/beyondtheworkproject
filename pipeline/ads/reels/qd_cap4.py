"""v7 (10/11, linha corporativa QD-07/08/09): igual ao qd_cap3 + fotos da TV do anfitrião (lobby cheio, revelação de cada pergunta, ranking) em <saida>/tv_*.png.
v5 (10/11, fluidez): igual ao qd_cap2, mas o CELULAR roda em câmera lenta real (JS: performance.now/rAF/timers ÷K; CSS/Web Animations: Animation.setPlaybackRate 1/K)
e a TV não é gravada (só hospeda). Na montagem, os trechos de animação tocam com rate=K → quadros reais ≈ fps da captura × K.
Uso: python3 qd_cap3.py <config.json> <saida> [K=3] [nperguntas]; depois python3 qd_cap2.py --cfr <saida> (só cel).
Original: Modelo novo (10/11): grava uma partida REAL do Quiddo local (npm run dev em src-quiddo) em alta, por screencast (CDP):
TV do anfitrião 1024×576 @1,875 (1920×1080) e celular da protagonista 390×844 @2,77 (1080 px de largura). Os outros jogadores entram em páginas próprias.
Uso: python3 qd_cap2.py <config.json> <saida>   → <saida>/tv/NNNNN.jpg, <saida>/cel/NNNNN.jpg, <saida>/marcas.json (tempos em s, relógio único)
Depois: python3 qd_cap2.py --cfr <saida>  monta tv.mp4 e cel.mp4 em 30 fps na velocidade real."""
import base64, json, subprocess, sys, time, uuid
from pathlib import Path

if sys.argv[1] == '--cfr':
    D = Path(sys.argv[2]); m = json.loads((D / 'marcas.json').read_text())
    for k in ('tv', 'cel'):
        ts = m['frames'][k]; t_end = m['fim']
        with open(D / f'{k}.txt', 'w') as f:
            f.write(f"file '{k}/00000.jpg'\nduration {max(ts[0], 0.001):.4f}\n")  # segura o 1º quadro desde t=0
            for i, t in enumerate(ts):
                d = (ts[i + 1] if i + 1 < len(ts) else t_end) - t
                f.write(f"file '{k}/{i:05d}.jpg'\nduration {max(d, 0.001):.4f}\n")
            f.write(f"file '{k}/{len(ts) - 1:05d}.jpg'\n")
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(D / f'{k}.txt'), '-vf', 'fps=30,format=yuv420p',
                        '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', str(D / f'{k}.mp4')], check=True)
    print('ok'); sys.exit()

from playwright.sync_api import sync_playwright
CFG = json.loads(Path(sys.argv[1]).read_text()); OUT = Path(sys.argv[2]); K = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
KP = float(sys.argv[5]) if len(sys.argv) > 5 else K
if len(sys.argv) > 4: CFG['quiz']['perguntas'] = CFG['quiz']['perguntas'][:int(sys.argv[4])]
for k in ('cel',): (OUT / k).mkdir(parents=True, exist_ok=True)
BASE = 'http://localhost:5173'
QUIZ = dict(CFG['quiz'], id=str(uuid.uuid4()), dobroUltima=False, marca={'name': '', 'color': ''}, logo='', atualizado=int(time.time() * 1000))
JOG, HERO = CFG['jogadores'], CFG['hero']
CSS = """aside[style*='position:fixed']{display:none!important}.btn.wa{display:none!important}.limite-gratis,.plano{display:none!important}.qr{filter:blur(9px)}"""
JS = """setInterval(()=>{if(!document.body)return;
document.querySelectorAll('.url').forEach(e=>{const b=e.querySelector('b');if(b&&!e.dataset.ok){e.dataset.ok=1;e.innerHTML='quiddo.com.br/<b>'+b.textContent+'</b>'}});
document.querySelectorAll('aside').forEach(a=>{if(/TESTE LOCAL/.test(a.textContent))a.remove()});
const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){if(n.nodeValue.includes('localhost:5173'))n.nodeValue=n.nodeValue.replace('localhost:5173','quiddo.com.br')}
if(!document.getElementById('qdcss')){const s=document.createElement('style');s.id='qdcss';s.textContent=window.__QDCSS||'';document.head.appendChild(s)}},40);"""
import base64 as _b
_F = Path(__file__).resolve().parent.parent.parent / 'fonts'
_d = lambda f: _b.b64encode((_F / f).read_bytes()).decode()
FONTCSS = (f"@font-face{{font-family:'Fraunces';font-weight:900;src:url(data:font/woff2;base64,{_d('Fraunces-900.woff2')}) format('woff2')}}"
           f"@font-face{{font-family:'Nunito';font-weight:600 900;src:url(data:font/woff2;base64,{_d('Nunito-var.woff2')}) format('woff2')}}")
SLOWJS = """(()=>{const pn=performance.now.bind(performance);let K=1,br=pn(),bv=br;const v=()=>bv+(pn()-br)/K;
window.__setK=k=>{bv=v();br=pn();K=k};performance.now=v;
const raf=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=f=>raf(()=>f(v()));
const st=window.setTimeout.bind(window),si=window.setInterval.bind(window);window.setTimeout=(f,d,...a)=>st(f,(d||0)*K,...a);window.setInterval=(f,d,...a)=>si(f,(d||0)*K,...a);})()"""
def prep(ctx):
    # o proxy bloqueia o Google Fonts: serve as mesmas fontes do site (Fraunces 900 e Nunito) a partir de pipeline/fonts
    ctx.route('**/fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=FONTCSS))
    ctx.add_init_script("Element.prototype.requestFullscreen=function(){return Promise.resolve()};window.__QDCSS=%s;" % json.dumps(CSS) + JS)

T0 = time.time(); now = lambda: time.time() - T0
marks = {'frames': {'tv': [], 'cel': []}, 'box': {}}
def M(k): marks[k] = round(now(), 3); print(f'{k:>12} {marks[k]:7.2f}', flush=True)
def cast(ctx, pg, key, w, h):
    cdp = ctx.new_cdp_session(pg)
    def on(ev):
        i = len(marks['frames'][key]); (OUT / key / f'{i:05d}.jpg').write_bytes(base64.b64decode(ev['data'])); marks['frames'][key].append(round(now(), 4))
        try: cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame', on)
    cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 88, 'maxWidth': w, 'maxHeight': h, 'everyNthFrame': 1})
    return cdp
def avancar(pg):
    el = pg.query_selector('button[data-act="start"], button[data-act="mostrar"], button[data-act="reveal"], button[data-act="showRanking"], button[data-act="next"], button[data-act="podio"]')
    if el: el.evaluate('e=>e.click()')
    else: pg.keyboard.press('ArrowRight')

with sync_playwright() as p:
    b = p.chromium.launch(args=['--force-device-scale-factor=1.5'])
    b2 = p.chromium.launch(args=['--force-device-scale-factor=2.77'])
    b3 = p.chromium.launch()  # os outros jogadores, leves  # o screencast só sai em alta com o fator forçado no navegador
    tv = b.new_context(viewport={'width': 1024, 'height': 576}, device_scale_factor=1.5); prep(tv); tvp = tv.new_page()  # UI grande: 1920×1080 no screencast
    tvp.goto(BASE + '/')
    tvp.evaluate("(q)=>{localStorage.setItem('sr:quizzes',JSON.stringify([q]));localStorage.setItem('sr:atual',JSON.stringify(q.id))}", QUIZ)
    tvp.goto(BASE + '/criar'); tvp.wait_for_timeout(2000)
    tvp.evaluate("document.querySelector('[data-act=abrir]').scrollIntoView({block:'center'})"); tvp.wait_for_timeout(500)
    tvp.click('button[data-act="abrir"]'); tvp.wait_for_url('**/host/**', timeout=20000); tvp.wait_for_timeout(1200)
    code = tvp.url.rstrip('/').split('/')[-1]; marks['code'] = code
    M('lobby')
    cel = b2.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2.77, has_touch=True); prep(cel); cel.add_init_script(SLOWJS); celp = cel.new_page()  # sem is_mobile: o screencast sai em 1080 de largura
    celp.goto(f'{BASE}/{code}'); celp.wait_for_selector('#nick'); cc = cast(cel, celp, 'cel', 1080, 2400); cc.send('Animation.enable'); marks['K'] = K; marks['lento'] = []
    def lento(on, kk=None):
        k = (kk or K) if on else 1
        celp.evaluate(f'window.__setK({k})'); cc.send('Animation.setPlaybackRate', {'playbackRate': 1 / k})
        if on and marks['lento'] and marks['lento'][-1][1] is None: marks['lento'][-1][1] = round(now(), 3)
        if on: marks['lento'].append([round(now(), 3), None, k])
        elif marks['lento'] and marks['lento'][-1][1] is None: marks['lento'][-1][1] = round(now(), 3)
    def entrar(pg, nome, lento=False):
        if pg is not celp: pg.goto(f'{BASE}/{code}'); pg.wait_for_selector('#nick', timeout=15000)
        for _ in range(CFG.get('sorteios', 1)): pg.click('button[data-act="sortear"]'); pg.wait_for_timeout(500 if lento else 150)
        pg.fill('#nick', ''); pg.type('#nick', nome, delay=130 if lento else 40); pg.wait_for_timeout(500 if lento else 200)
        pg.click('#fj button[type="submit"]')
    outros = []
    tvp.wait_for_timeout(1500)
    for j in JOG[:3]:
        c = b3.new_context(viewport={'width': 360, 'height': 640}); prep(c); pg = c.new_page(); entrar(pg, j[0]); outros.append(pg); tvp.wait_for_timeout(700)
    M('cel_form'); celp.wait_for_timeout(800); entrar(celp, HERO[0], lento=True); M('cel_entrou'); celp.wait_for_timeout(1200)
    for j in JOG[3:]:
        c = b3.new_context(viewport={'width': 360, 'height': 640}); prep(c); pg = c.new_page(); entrar(pg, j[0]); outros.append(pg); tvp.wait_for_timeout(700)
    tvp.wait_for_timeout(2500); M('lobby_cheio'); tvp.screenshot(path=str(OUT / 'tv_lobby.png'))
    todos = [(celp, HERO)] + list(zip(outros, JOG)); NQ = len(QUIZ['perguntas'])
    for q in range(NQ):
        avancar(tvp); M(f'q{q}_prep'); tvp.wait_for_timeout(1200)
        celp.wait_for_selector('button.ans:not([disabled])', timeout=90000); lento(True); M(f'q{q}_resp')
        t0 = time.time()
        for pg, (nome, resp, atraso) in sorted(todos, key=lambda x: x[1][2]):
            while time.time() - t0 < atraso: tvp.wait_for_timeout(40)
            sel = f'button.ans[data-v="{resp[q]}"]'
            try:
                if pg is celp:
                    bb = pg.query_selector(sel).bounding_box(); marks['box'][f'q{q}'] = bb; M(f'q{q}_hero'); pg.tap(sel)
                else: pg.click(sel, timeout=5000)
            except Exception as e: print('falhou', nome, e)
        tvp.wait_for_timeout(1500)
        if not tvp.query_selector('button[data-act="showRanking"], button[data-act="next"]'): avancar(tvp)
        M(f'q{q}_reveal'); tvp.wait_for_timeout(2600); tvp.screenshot(path=str(OUT / f'tv_q{q}_rev.png')); tvp.wait_for_timeout(max(0, int(5200 * K) - 2600))
        if q < NQ - 1: avancar(tvp); M(f'q{q}_rank'); tvp.wait_for_timeout(3500); tvp.screenshot(path=str(OUT / f'tv_q{q}_rank.png')); tvp.wait_for_timeout(max(0, int(6500 * K) - 3500)); lento(False)
    lento(True, KP); avancar(tvp); M('podio')
    for k in range(6): tvp.wait_for_timeout(int(3000 * KP)); avancar(tvp); M(f'podio{k}')
    tvp.wait_for_timeout(int(4000 * KP)); lento(False); M('fim')
    b.close(); b2.close(); b3.close()
(OUT / 'marcas.json').write_text(json.dumps(marks, ensure_ascii=False))
print('quadros cel', len(marks['frames']['cel']))
