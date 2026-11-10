"""ADC-QD-10 (KV Quiddo Empresas): captura REAL do modo Corporativo no app local (src-quiddo, npm run dev :5173).
Telão (TV do anfitrião) 1920×1080 e celular 1080 px de largura com a MESMA pergunta aberta; depois o celular com a resposta A tocada.
Uso: python3 qd10_cap.py <saida>"""
import json, sys, time, uuid
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
CFG = {"quiz": {"titulo": "Kickoff Comercial · Vértice", "tema": "corp", "visual": "floresta", "tempo": 30,
  "perguntas": [{"t": "O que vem antes da proposta?", "o": ["Entender a necessidade", "Começar pelo desconto", "Escolher o contrato", "Enviar um catálogo"], "c": 0, "tl": 30}]}}
BASE = 'http://localhost:5173'
QUIZ = dict(CFG['quiz'], id=str(uuid.uuid4()), dobroUltima=False, marca={'name': '', 'color': ''}, logo='', atualizado=int(time.time() * 1000))
JOG, HERO = [], None
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


def avancar(pg):
    el = pg.query_selector('button[data-act="start"], button[data-act="mostrar"], button[data-act="reveal"], button[data-act="next"]')
    if el: el.evaluate('e=>e.click()')
    else: pg.keyboard.press('ArrowRight')
with sync_playwright() as p:
    b = p.chromium.launch(args=['--force-device-scale-factor=1.5']); b2 = p.chromium.launch(args=['--force-device-scale-factor=2.77']); b3 = p.chromium.launch()
    tv = b.new_context(viewport={'width': 1280, 'height': 720}, device_scale_factor=1.5); prep(tv); tvp = tv.new_page()
    tvp.goto(BASE + '/'); tvp.evaluate("(q)=>{localStorage.setItem('sr:quizzes',JSON.stringify([q]));localStorage.setItem('sr:atual',JSON.stringify(q.id))}", QUIZ)
    tvp.goto(BASE + '/criar'); tvp.wait_for_timeout(2000); tvp.screenshot(path=str(OUT / 'editor.png'), full_page=False)
    tvp.evaluate("document.querySelector('[data-act=abrir]').scrollIntoView({block:'center'})"); tvp.wait_for_timeout(400)
    tvp.click('button[data-act="abrir"]'); tvp.wait_for_url('**/host/**', timeout=20000); tvp.wait_for_timeout(1200)
    code = tvp.url.rstrip('/').split('/')[-1]
    cel = b2.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2.77, has_touch=True); prep(cel); celp = cel.new_page()
    def entrar(pg, nome):
        pg.goto(f'{BASE}/{code}'); pg.wait_for_selector('#nick', timeout=15000)
        pg.click('button[data-act="sortear"]'); pg.wait_for_timeout(200); pg.fill('#nick', nome); pg.click('#fj button[type="submit"]')
    outros = []
    for n in ['Carla', 'Diego', 'Fernanda', 'Rodrigo', 'Patrícia', 'Bruno', 'Aline', 'Marcos']:
        c = b3.new_context(viewport={'width': 360, 'height': 640}); prep(c); pg = c.new_page(); entrar(pg, n); outros.append(pg); tvp.wait_for_timeout(400)
    entrar(celp, 'Lucas'); tvp.wait_for_timeout(2500); tvp.screenshot(path=str(OUT / 'tv_lobby.png'))
    avancar(tvp); tvp.wait_for_timeout(800)
    celp.wait_for_selector('button.ans:not([disabled])', timeout=60000); tvp.wait_for_timeout(1500)
    tvp.screenshot(path=str(OUT / 'tv_q.png')); celp.screenshot(path=str(OUT / 'cel_q.png'))
    for k, pg in enumerate(outros[:4]): pg.click(f'button.ans[data-v="{[0,0,1,0][k]}"]'); tvp.wait_for_timeout(500)
    tvp.wait_for_timeout(800); tvp.screenshot(path=str(OUT / 'tv_q2.png'))
    celp.tap('button.ans[data-v="0"]'); celp.wait_for_timeout(1200); celp.screenshot(path=str(OUT / 'cel_tap.png')); tvp.screenshot(path=str(OUT / 'tv_q3.png'))
    b.close(); b2.close(); b3.close()
print('ok', code)
