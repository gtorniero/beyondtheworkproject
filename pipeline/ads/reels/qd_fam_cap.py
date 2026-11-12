"""KV Quiddo Família e Amigos (ADC-QD-11..15): captura REAL do app local (src-quiddo, vite :5173), modo Amigos & família (tema festa).
Telão 1920×1080 e celular 1080 de largura, em cada etapa: lobby, pergunta aberta, toque, revelação, ranking, pódio (fotos, sem animação travada).
Uso: python3 qd_fam_cap.py <tema> <saida>   (tema: familia|amigos|chabar|despedida|confra)"""
import json, sys, time, uuid
from pathlib import Path
from playwright.sync_api import sync_playwright
# mesmo tratamento do qd10_cap.py: fontes locais, sem selo de teste/WhatsApp/localhost, QR desfocado
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


T = {
 'familia':  dict(tit='Noite de jogos da família', vis='floresta', q='Quem ronca mais alto no Natal?', o=['O vô', 'A tia do pavê', 'O cachorro', 'Todo mundo'], c=0,
                  eu='Neta', nicks=['Vó', 'Tio', 'Prima', 'Cunhado', 'Dinda', 'Primo', 'Tia', 'Vô'], ans=[0, 0, 3, 1, 0, 2, 0, 0]),
 'amigos':   dict(tit='Quiz da turma', vis='espaco', q='Quem do grupo manda o maior áudio?', o=['O que dirige', 'A que mora fora', 'O do churrasco', 'Todo mundo'], c=1,
                  eu='Sumida', nicks=['Pontual', 'DJ', 'Do churras', 'Atrasado', 'Do áudio', 'Fotógrafa', 'Caçula', 'Organizador'], ans=[1, 1, 3, 1, 0, 1, 2, 1]),
 'chabar':   dict(tit='Chá da casa nova', vis='amor', q='Onde foi o primeiro encontro?', o=['No cinema', 'Numa pizzaria', 'Num casamento', 'Na fila do pão'], c=1,
                  eu='Madrinha', nicks=['Padrinho', 'Sogra', 'Prima', 'Irmão', 'Vizinha', 'Amigo de infância', 'Cunhada', 'Tia'], ans=[1, 0, 1, 2, 1, 3, 1, 1]),
 'despedida':dict(tit='Despedida de solteiro', vis='entretenimento', q='Qual mania do noivo a turma não aguenta mais?', o=['Contar a mesma piada', 'Chegar atrasado', 'Mandar áudio longo', 'Falar de futebol'], c=2,
                  eu='Padrinho', nicks=['Irmão', 'Primo', 'Amigo da facul', 'Vizinho', 'Cunhado', 'Do futebol', 'Colega', 'Sobrinho'], ans=[2, 0, 2, 2, 3, 2, 1, 2]),
 'confra':   dict(tit='Confra de fim de ano', vis='floresta', q='Quem chegou atrasado em todas as confras?', o=['Quem mora mais perto', 'Quem organizou', 'O amigo secreto', 'Ninguém lembra'], c=0,
                  eu='Capitã', nicks=['Levantador', 'Reserva', 'Técnico', 'Torcida', 'Goleira', 'Do saque', 'Novato', 'Veterana'], ans=[0, 0, 3, 0, 1, 0, 2, 0]),
}
tema, OUT = sys.argv[1], Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True); C = T[tema]
BASE = 'http://localhost:5173'
QUIZ = {'id': str(uuid.uuid4()), 'titulo': C['tit'], 'tema': 'festa', 'visual': C['vis'], 'tempo': 30, 'dobroUltima': False,
        'marca': {'name': '', 'color': ''}, 'logo': '', 'atualizado': int(time.time() * 1000),
        'perguntas': [{'t': C['q'], 'o': C['o'], 'c': C['c'], 'tl': 30}]}
def act(pg):
    el = pg.query_selector('button[data-act="start"], button[data-act="mostrar"], button[data-act="reveal"], button[data-act="next"]')
    if el: el.evaluate('e=>e.click()'); return el.get_attribute('data-act')
with sync_playwright() as p:
    b = p.chromium.launch(); b2 = p.chromium.launch(); b3 = p.chromium.launch()
    tv = b.new_context(viewport={'width': 1280, 'height': 720}, device_scale_factor=1.5); prep(tv); tvp = tv.new_page()
    tvp.goto(BASE + '/'); tvp.evaluate("(q)=>{localStorage.setItem('sr:quizzes',JSON.stringify([q]));localStorage.setItem('sr:atual',JSON.stringify(q.id))}", QUIZ)
    tvp.goto(BASE + '/criar'); tvp.wait_for_timeout(2000)
    tvp.evaluate("document.querySelector('[data-act=abrir]').scrollIntoView({block:'center'})"); tvp.wait_for_timeout(400)
    tvp.click('button[data-act="abrir"]'); tvp.wait_for_url('**/host/**', timeout=20000); tvp.wait_for_timeout(1200)
    code = tvp.url.rstrip('/').split('/')[-1]
    cel = b2.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2.77, has_touch=True); prep(cel); celp = cel.new_page()
    def entrar(pg, nome):
        pg.goto(f'{BASE}/{code}'); pg.wait_for_selector('#nick', timeout=15000)
        pg.click('button[data-act="sortear"]'); pg.wait_for_timeout(150); pg.fill('#nick', nome); pg.click('#fj button[type="submit"]')
    outros = []
    for n in C['nicks']:
        c = b3.new_context(viewport={'width': 360, 'height': 640}); prep(c); pg = c.new_page(); entrar(pg, n); outros.append(pg); tvp.wait_for_timeout(350)
    entrar(celp, C['eu']); tvp.wait_for_timeout(2500)
    tvp.screenshot(path=str(OUT / 'tv_lobby.png')); celp.screenshot(path=str(OUT / 'cel_lobby.png'))
    for _ in range(3):  # start (e "mostrar" se houver) até as respostas abrirem
        act(tvp); tvp.wait_for_timeout(1200)
        if celp.query_selector('button.ans:not([disabled])'): break
    celp.wait_for_selector('button.ans:not([disabled])', timeout=60000); tvp.wait_for_timeout(1200)
    tvp.screenshot(path=str(OUT / 'tv_q.png')); celp.screenshot(path=str(OUT / 'cel_q.png'))
    celp.tap(f'button.ans[data-v="{C["c"]}"]'); celp.wait_for_timeout(900)
    celp.screenshot(path=str(OUT / 'cel_tap.png'))
    for k, pg in enumerate(outros[:5]): pg.click(f'button.ans[data-v="{C["ans"][k]}"]'); tvp.wait_for_timeout(300)
    tvp.screenshot(path=str(OUT / 'tv_q2.png'))
    for k, pg in enumerate(outros[5:], 5): pg.click(f'button.ans[data-v="{C["ans"][k]}"]'); tvp.wait_for_timeout(250)
    tvp.wait_for_timeout(2600); tvp.screenshot(path=str(OUT / 'tv_rev.png')); celp.screenshot(path=str(OUT / 'cel_rev.png'))
    tvp.wait_for_timeout(2500); tvp.screenshot(path=str(OUT / 'tv_rev2.png')); celp.screenshot(path=str(OUT / 'cel_rev2.png'))
    passos = []
    for i in range(6):
        a = act(tvp); tvp.wait_for_timeout(3500)
        tvp.screenshot(path=str(OUT / f'tv_{i}_{a}.png')); celp.screenshot(path=str(OUT / f'cel_{i}_{a}.png')); passos.append(a)
        if a == 'next' and tvp.query_selector('.podio, [class*=podio]'): tvp.wait_for_timeout(4000); tvp.screenshot(path=str(OUT / 'tv_podio.png')); celp.screenshot(path=str(OUT / 'cel_podio.png')); break
        if a is None: break
    b.close(); b2.close(); b3.close()
print('ok', code, passos)
