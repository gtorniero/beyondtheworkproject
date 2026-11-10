"""ADC-QD-01 v3: grava uma partida real do Quiddo rodando local (npm run dev em src-quiddo).
TV (anfitrião) 1280x720 e o celular da Mariana 390x844 são gravados; outros 7 jogadores entram em páginas sem gravação.
Saída: <out>/tv.webm, <out>/cel.webm e <out>/marcas.json (tempo de cada etapa, em segundos desde o início de cada gravação)."""
import json, sys, time, uuid, random
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:5173'
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
PROBE = len(sys.argv) > 2 and sys.argv[2] == 'probe'

QUIZ = {
  'id': str(uuid.uuid4()), 'titulo': 'Integração · Turma de novembro', 'tema': 'corp', 'visual': 'escritorio', 'tempo': 20,
  'dobroUltima': False, 'marca': {'name': '', 'color': ''}, 'logo': '', 'atualizado': int(time.time() * 1000),
  'perguntas': [
    {'t': 'Chegou um e-mail pedindo a sua senha com urgência. O que você faz?', 'o': ['Passa a senha', 'Clica no link', 'Avisa a TI', 'Ignora'], 'c': 2, 'tl': 20},
    {'t': 'O crachá pode ser emprestado para um colega entrar no prédio.', 'o': ['Verdadeiro', 'Falso'], 'c': 1, 'tl': 20, 'vf': True},
    {'t': 'Viu um risco de acidente no seu setor. Qual é o primeiro passo?', 'o': ['Tenta resolver', 'Avisa o líder', 'Espera o turno', 'Ignora'], 'c': 1, 'tl': 20},
  ],
}
# (nome, respostas por pergunta, atraso de resposta em s depois de liberar)
JOG = [('Carlos', [2, 1, 1], 2.2), ('Juliana', [2, 1, 1], 1.4), ('Rafael', [1, 1, 1], 3.1), ('Patrícia', [2, 0, 1], 4.0),
       ('Bruno', [3, 1, 0], 2.7), ('Fernanda', [2, 1, 1], 3.6), ('Diego', [2, 1, 3], 5.2)]
HERO = ('Mariana', [2, 1, 1], 1.8)

# Esconde o que não é do produto no ar: selo de teste local, convite por app de terceiros, limite/oferta da sala grátis;
# troca o endereço local por quiddo.com.br e desfoca o QR (aponta para o localhost).
CSS = """aside[style*='position:fixed']{display:none!important}.btn.wa{display:none!important}.limite-gratis,.plano{display:none!important}
.qr{filter:blur(9px)}"""
JS = """setInterval(()=>{if(!document.body)return;
document.querySelectorAll('.url').forEach(e=>{const b=e.querySelector('b');if(b&&!e.dataset.ok){e.dataset.ok=1;e.innerHTML='quiddo.com.br/<b>'+b.textContent+'</b>'}});
document.querySelectorAll('aside').forEach(a=>{if(/TESTE LOCAL/.test(a.textContent))a.remove()});
const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){if(n.nodeValue.includes('localhost:5173'))n.nodeValue=n.nodeValue.replace('localhost:5173','quiddo.com.br')}
if(!document.getElementById('qdcss')){const s=document.createElement('style');s.id='qdcss';s.textContent=window.__QDCSS||'';document.head.appendChild(s)}},40);"""
def prep(ctx):
    ctx.add_init_script("Element.prototype.requestFullscreen=function(){return Promise.resolve()};window.__QDCSS=%s;" % json.dumps(CSS) + JS)

marks = {}
def avancar(pg, opcional=False):
    sel = 'button[data-act="start"], button[data-act="mostrar"], button[data-act="reveal"], button[data-act="showRanking"], button[data-act="next"], button[data-act="podio"]'
    el = pg.query_selector(sel)
    if el:
        el.evaluate('e=>e.click()'); return
    pg.keyboard.press('ArrowRight')
with sync_playwright() as p:
    b = p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    tv = b.new_context(viewport={'width': 1920, 'height': 1080}, record_video_dir=None if PROBE else str(OUT / 'tv'), record_video_size={'width': 1920, 'height': 1080}, device_scale_factor=1)
    prep(tv)
    tvp = tv.new_page(); t_tv = time.time()
    tvp.goto(BASE + '/')
    tvp.evaluate("(q)=>{localStorage.setItem('sr:quizzes',JSON.stringify([q]));localStorage.setItem('sr:atual',JSON.stringify(q.id))}", QUIZ)
    tvp.goto(BASE + '/criar'); tvp.wait_for_timeout(2500)
    marks['tv_editor'] = time.time() - t_tv
    if PROBE: tvp.screenshot(path=str(OUT / 'p1_editor.png'), full_page=True)
    tvp.wait_for_timeout(1200)
    # vai até as perguntas (rolagem suave), mostra, e desce até o botão de abrir a sala
    alvo = tvp.evaluate("(()=>{const h=[...document.querySelectorAll('h2,h3,.etapa-t,legend')].find(e=>/Perguntas/.test(e.textContent));return h?h.getBoundingClientRect().top+scrollY-20:2000})()")
    for k in range(60):
        tvp.evaluate(f"window.scrollTo(0,{alvo*(k+1)/60})"); tvp.wait_for_timeout(25)
    marks['tv_perguntas'] = time.time() - t_tv
    tvp.wait_for_timeout(3500)
    fim = tvp.evaluate("(()=>{const b=document.querySelector('[data-act=abrir]');return b.getBoundingClientRect().top+scrollY-innerHeight/2})()")
    for k in range(50):
        tvp.evaluate(f"window.scrollTo(0,{alvo+(fim-alvo)*(k+1)/50})"); tvp.wait_for_timeout(25)
    tvp.wait_for_timeout(1500)
    marks['tv_abrir'] = time.time() - t_tv
    tvp.click('button[data-act="abrir"]')
    tvp.wait_for_url('**/host/**', timeout=20000); tvp.wait_for_timeout(1500)
    code = tvp.url.rstrip('/').split('/')[-1]
    marks['code'] = code; marks['tv_lobby'] = time.time() - t_tv
    if PROBE: tvp.screenshot(path=str(OUT / 'p2_lobby.png'))
    # celular da Mariana (gravado)
    cel = b.new_context(viewport={'width': 480, 'height': 1040}, device_scale_factor=1, is_mobile=True, has_touch=True,
                        record_video_dir=None if PROBE else str(OUT / 'cel'), record_video_size={'width': 480, 'height': 1040})
    prep(cel); celp = cel.new_page(); t_cel = time.time()
    marks['t_offset'] = t_cel - t_tv  # tempo do celular = tempo da TV - offset
    def entrar(pg, nome):
        pg.goto(f'{BASE}/{code}'); pg.wait_for_selector('#nick', timeout=15000)
        pg.click('button[data-act="sortear"]'); pg.wait_for_timeout(300)
        pg.fill('#nick', ''); pg.type('#nick', nome, delay=90); pg.wait_for_timeout(400)
        pg.click('#fj button[type="submit"]')
    outros = []
    for i, (nome, _, _) in enumerate(JOG[:3]):
        c = b.new_context(viewport={'width': 390, 'height': 844}); prep(c); pg = c.new_page(); entrar(pg, nome); outros.append(pg); tvp.wait_for_timeout(900)
    celp.goto(f'{BASE}/{code}'); celp.wait_for_selector('#nick'); celp.wait_for_timeout(1200)
    marks['cel_form'] = time.time() - t_tv
    celp.click('button[data-act="sortear"]'); celp.wait_for_timeout(700); celp.click('button[data-act="sortear"]'); celp.wait_for_timeout(700)
    celp.type('#nick', HERO[0], delay=140); celp.wait_for_timeout(700)
    celp.click('#fj button[type="submit"]'); celp.wait_for_timeout(1500)
    marks['cel_sala'] = time.time() - t_tv
    if PROBE: celp.screenshot(path=str(OUT / 'p3_cel_sala.png'))
    for nome, _, _ in JOG[3:]:
        c = b.new_context(viewport={'width': 390, 'height': 844}); prep(c); pg = c.new_page(); entrar(pg, nome); outros.append(pg); tvp.wait_for_timeout(900)
    tvp.wait_for_timeout(2500)
    if PROBE: tvp.screenshot(path=str(OUT / 'p4_lobby_cheio.png'))
    todos = [(celp, HERO)] + list(zip(outros, JOG))
    for q in range(len(QUIZ['perguntas'])):
        avancar(tvp)  # começa / próxima pergunta
        marks[f'q{q}_prep'] = time.time() - t_tv
        tvp.wait_for_timeout(1200)
        if PROBE and q == 0: tvp.screenshot(path=str(OUT / 'p5_prep.png'))
        # espera as respostas liberarem no celular
        celp.wait_for_selector('button.ans:not([disabled])', timeout=30000)
        marks[f'q{q}_resp'] = time.time() - t_tv
        ordem = sorted(todos, key=lambda x: x[1][2])
        t0 = time.time()
        for pg, (nome, resp, atraso) in ordem:
            while time.time() - t0 < atraso: tvp.wait_for_timeout(50)
            try: pg.click(f'button.ans[data-v="{resp[q]}"]', timeout=5000)
            except Exception as e: print('falhou', nome, e)
            if pg is celp: marks[f'q{q}_mari'] = time.time() - t_tv
        tvp.wait_for_timeout(1500)
        if PROBE and q == 0: tvp.screenshot(path=str(OUT / 'p6_q_tv.png')); celp.screenshot(path=str(OUT / 'p6_q_cel.png'))
        # todos responderam: revela (se ainda não revelou sozinho)
        if not tvp.query_selector('button[data-act="showRanking"], button[data-act="next"]'):
            avancar(tvp)
        marks[f'q{q}_reveal'] = time.time() - t_tv
        tvp.wait_for_timeout(5000)
        if PROBE and q == 0: tvp.screenshot(path=str(OUT / 'p7_reveal_tv.png')); celp.screenshot(path=str(OUT / 'p7_reveal_cel.png'))
        if q < len(QUIZ['perguntas']) - 1:
            avancar(tvp); marks[f'q{q}_rank'] = time.time() - t_tv
            tvp.wait_for_timeout(6500)
            if PROBE and q == 0: tvp.screenshot(path=str(OUT / 'p8_rank_tv.png')); celp.screenshot(path=str(OUT / 'p8_rank_cel.png'))
    avancar(tvp); marks['podio'] = time.time() - t_tv
    for k in range(6):
        tvp.wait_for_timeout(3000)
        if PROBE: tvp.screenshot(path=str(OUT / f'p9_podio{k}.png'))
        avancar(tvp, opcional=True)
    tvp.wait_for_timeout(4000)
    if PROBE: celp.screenshot(path=str(OUT / 'p9_podio_cel.png'))
    marks['fim'] = time.time() - t_tv
    vids = {}
    tvp.close(); celp.close()
    if not PROBE:
        vids['tv'] = tvp.video.path(); vids['cel'] = celp.video.path()
    tv.close(); cel.close(); b.close()
    marks['videos'] = {k: str(v) for k, v in vids.items()}
(OUT / 'marcas.json').write_text(json.dumps(marks, indent=1, ensure_ascii=False))
print(json.dumps(marks, indent=1, ensure_ascii=False))
