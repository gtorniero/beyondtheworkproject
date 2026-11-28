"""SPORT DNA · Pack Semanal 03. Archivo ExtraBold / DM Sans / JetBrains Mono; Syne só em números de destaque e logos.
Marca-mãe ~90% preto, branco e off-white; cor do esporte como acento (RACKET #DDF247, SURF #6CCFF6, RUN #FF8A3D).
Números só do site no ar (sportdna.com.br, conferidos no repositório gtorniero/sportdna em 03/11/2026)."""
import common as C
from common import TL, at, doc, add

AS = C.A / 'sportdna'
FONTS = (C.font_face('Archivo', 'Archivo-800.woff2', '800') + C.font_face('DM Sans', 'DMSans-var.woff2', '400 700') +
         C.font_face('JetBrains Mono', 'JBMono-var.woff2', '400 700') + C.font_face('Syne', 'Syne-800.woff2', '800'))

CSS = """
:root{--ink:#0A0A0A;--off:#F4F4F2;--off2:#EAEAE7;--line:#2E2E2C;--lineL:#DCDCD7;--muted:#A3A3A0;--mutedL:#5C5C58;--surface:#1A1A1A;
--racket:#DDF247;--surf:#6CCFF6;--run:#FF8A3D;--petrol:#0E4D64;
--ease-pop:cubic-bezier(.2,.75,.15,1);--ease-rise:cubic-bezier(.2,.75,.15,1);--ease-grow:cubic-bezier(.2,.75,.15,1);--ease-slideL:cubic-bezier(.2,.75,.15,1);--ease-slideR:cubic-bezier(.2,.75,.15,1);--ease-fade:linear;--ease-wipe:cubic-bezier(.2,.75,.15,1)}
@keyframes pop{0%{opacity:0;transform:scale(.92)}100%{opacity:1;transform:scale(1)}}
@keyframes rise{0%{opacity:0;transform:translateY(30px)}100%{opacity:1;transform:none}}
.page{background:var(--ink);color:#fff;font-family:'DM Sans',sans-serif;font-weight:400}
.page.light{background:var(--off);color:var(--ink)}
.t{font-family:Archivo,sans-serif;font-weight:800;letter-spacing:-.025em;line-height:.98}
.n{font-family:Syne,sans-serif;font-weight:800;letter-spacing:-.03em;line-height:.9;white-space:nowrap}
.m{font-family:'JetBrains Mono',monospace;font-weight:500;letter-spacing:.02em}
.chip{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:28px;padding:10px 20px;border:2px solid currentColor;border-radius:999px}
.rule{height:2px;background:var(--line)} .light .rule{background:var(--lineL)}
.lbl{font-family:'JetBrains Mono',monospace;font-size:28px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)} .light .lbl{color:var(--mutedL)}
@property --n{syntax:'<integer>';inherits:false;initial-value:0}
.cnt{counter-reset:c var(--n)}.cnt::after{content:counter(c)}
@keyframes typing{0%{opacity:0}15%,85%{opacity:1}100%{opacity:0}}
"""

def logo(name, w):
    return C.svg_sized(AS / f'{name}.svg', w=w)

def page(body, w=1080, h=1350, cls=''):
    return f'<section class="page {cls}" style="width:{w}px;height:{h}px">{body}</section>'

def cover_from_feed(feed_body, bg):
    return doc('capa', FONTS, CSS, f'<section class="page" style="width:1080px;height:1920px;background:{bg}"><div class="abs" style="left:0;top:285px;width:1080px;height:1350px;overflow:hidden">{feed_body}</div></section>', 1080, 1920)

def piece(**kw):
    kw.setdefault('brand', 'SPORT DNA')
    return add(kw)

def chat_user(txt, style=''):
    return f'<div style="display:flex;justify-content:flex-end;{style}"><div style="max-width:78%;background:#2E2E2C;color:#fff;border-radius:34px 34px 8px 34px;padding:24px 30px;font-size:40px;line-height:1.3">{txt}</div></div>'

def chat_ia(txt, style=''):
    return (f'<div style="display:flex;gap:20px;align-items:flex-start;{style}"><div class="m" style="flex:none;width:72px;height:72px;border-radius:50%;background:var(--off);color:var(--ink);display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700">IA</div>'
            f'<div style="flex:1;font-size:40px;line-height:1.35;color:#fff;padding-top:8px">{txt}</div></div>')

def chat_dots(t0, x, y):
    return ''.join(f'<div class="abs" style="left:{x + i*34}px;top:{y}px;width:20px;height:20px;border-radius:50%;background:var(--muted);opacity:0;animation:typing 1.0s ease-in-out {t0 + i*.15:.2f}s 1 both"></div>' for i in range(3))

def simbolo_animado(size, t0):
    s = C.svg_sized(AS / 'sportdna-simbolo-cor-sem-fundo-escuro.svg', w=size, h=size)
    # os 3 arcos se desenham em sequência, no sentido do relógio; o S fica parado
    import re
    i = [0]
    def rep(m):
        k = i[0]; i[0] += 1
        return m.group(0).replace('stroke-dasharray="40.782 131.947"', f'stroke-dasharray="40.782 131.947" style="animation:arc{k} .7s cubic-bezier(.2,.75,.15,1) {t0 + k*.35:.2f}s 1 both"')
    s = re.sub(r'<circle[^>]*stroke-dasharray="40.782 131.947"[^>]*/>', rep, s)
    return s


import re

def cta_final(t=None, txt='Teste grátis e sem cadastro · sportdna.com.br'):
    return f'<div class="abs m" style="left:90px;top:820px;font-size:36px;{at(t,"fade") if t is not None else ""}">{txt}</div>'

def sim_tag(txt='SIMULAÇÃO · ASSISTENTE DE IA GENÉRICO'):
    return f'<div class="lbl" style="margin-bottom:26px">{txt}</div>'



CSS += """
@keyframes tierIn{0%{opacity:0;transform:translateY(-60px) scale(.9)}100%{opacity:1;transform:none}}
@keyframes knobOn{0%{transform:translateX(0)}100%{transform:translateX(96px)}}
@keyframes knobOff{0%{transform:translateX(96px)}100%{transform:translateX(0)}}
@keyframes trackOn{0%{background:#3A3A38}100%{background:var(--surf)}}
@keyframes trackOff{0%{background:var(--surf)}100%{background:#3A3A38}}
@keyframes strike{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}
.grid-bg{background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:60px 60px}
.light .grid-bg,.grid-bg.l{background-image:linear-gradient(rgba(0,0,0,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(0,0,0,.06) 2px,transparent 2px)}
"""

# ------------------------------------------------------------------ desenhos técnicos (linha, sem marca)

# =====================================================================================
# S05 · 08–14/12/2026 · cada peça numa cor só (RACKET lima, RUN laranja, SURF azul; marca-mãe em preto e branco)
# Gui, rodada 18: "racket tem que ser 100% com as cores do racket". Sem ilustração de equipamento.
# =====================================================================================
END = {'racket': C.PACKS / 'S04/sportdna/carrosseis/D-C11-5.png', 'run': C.PACKS / 'S04/sportdna/carrosseis/D-C12-6.png',
       'surf': C.PACKS / 'S03/sportdna/carrosseis/D-C9-6.png', 'sport': C.PACKS / 'S04/sportdna/carrosseis/D-C10-6.png'}
COR = {'racket': 'var(--racket)', 'run': 'var(--run)', 'surf': 'var(--surf)', 'sport': '#fff'}
LOGO = {'racket': 'racketdna-logo-fundo-escuro', 'run': 'rundna-logo-fundo-escuro', 'surf': 'surfdna-logo-fundo-escuro', 'sport': 'sportdna-logo-fundo-escuro'}
NOME = {'racket': 'RACKET DNA', 'run': 'RUN DNA', 'surf': 'SURF DNA', 'sport': 'SPORT DNA'}

def SC(tl, a, z):
    return tl.scene(max(0, a - .04), z, fin=False, fout=False)

CSS += """
.big{font-family:Syne,sans-serif;font-weight:800;letter-spacing:-.04em;line-height:.85}
.bar{height:28px;border-radius:14px;background:#2E2E2C;position:relative;overflow:hidden}
.bar i{position:absolute;left:0;top:0;bottom:0;border-radius:14px}
.tagm{display:inline-block;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:30px;letter-spacing:.06em;padding:10px 20px;border-radius:10px}
.bub{max-width:80%;border-radius:30px;padding:20px 28px;font-size:42px;line-height:1.25}
"""

def head(sp, txt, n=None):
    c = COR[sp]
    return (f'<div class="abs m" style="left:80px;top:70px;font-size:26px;letter-spacing:.1em;color:{c}">{NOME[sp]} · {txt}</div>'
            + (f'<div class="abs m" style="right:80px;top:70px;font-size:26px;color:var(--muted)">{n}</div>' if n else ''))

def pe(sp):
    return f'<div class="abs" style="left:80px;top:1240px">{logo(LOGO[sp], 260)}</div>'

# -------------------------------------------------------------------------------------
# D-C13 · Carrossel RACKET (ter 08/12) · Cabeça da raquete: 98, 100 ou 105?
# -------------------------------------------------------------------------------------
CABECAS = [('98', 'Mais controle', 'Área útil menor: exige golpe no centro, devolve precisão. Pra quem já bate firme e quer direcionar.', 45),
           ('100', 'O meio-termo', 'Equilíbrio entre controle e ajuda na potência. É o tamanho mais comum nas raquetes de adulto.', 62),
           ('105+', 'Mais perdão', 'Sweet spot maior e mais potência fácil. Ajuda quem erra fora do centro ou tem golpe curto.', 86)]

def d_c13():
    R = 'var(--racket)'
    pages = [page(f'''<div class="abs" style="inset:0;background:{R}"></div>
      <div class="abs m" style="left:80px;top:70px;font-size:26px;letter-spacing:.1em;color:var(--ink)">RACKET DNA · TAMANHO DA CABEÇA</div><div class="abs m" style="right:80px;top:70px;font-size:26px;color:var(--ink)">1/6</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:96px;color:var(--ink)">Cabeça da raquete: qual o seu número?</div>
      <div class="abs" style="left:80px;top:560px;display:flex;gap:26px;align-items:flex-end;color:var(--ink)">
        <span class="big" style="font-size:112px;opacity:.45">98</span><span class="big" style="font-size:150px">100</span><span class="big" style="font-size:112px;opacity:.45">105</span></div>
      <div class="abs m" style="left:80px;top:860px;font-size:30px;color:var(--ink)">polegadas quadradas (pol²)</div>
      <div class="abs" style="left:80px;top:1000px;font-size:40px;font-weight:700;color:var(--ink)">Arrasta e salva antes de comprar →</div>
      <div class="abs" style="left:80px;top:1240px">{logo('racketdna-logo-preto', 260)}</div>''')]
    for i, (n, tit, txt, pct) in enumerate(CABECAS):
        pages.append(page(f'''<div class="abs grid-bg" style="inset:0"></div>{head('racket', 'TAMANHO DA CABEÇA', f'{i + 2}/6')}
          <div class="abs big" style="left:70px;top:{150 if len(n) < 4 else 190}px;font-size:{330 if len(n) < 4 else 250}px;color:{R}">{n}</div>
          <div class="abs t" style="left:80px;top:520px;width:920px;font-size:88px">{tit}</div>
          <div class="abs" style="left:80px;top:680px;width:900px;font-size:44px;line-height:1.35">{txt}</div>
          <div class="abs m" style="left:80px;top:980px;font-size:26px;color:var(--muted)">TAMANHO DO SWEET SPOT</div>
          <div class="abs bar" style="left:80px;top:1030px;width:920px"><i style="width:{pct}%;background:{R}"></i></div>{pe('racket')}'''))
    pages.append(page(f'''<div class="abs grid-bg" style="inset:0"></div>{head('racket', 'O QUE MAIS PESA', '5/6')}
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:88px">A cabeça não decide sozinha.</div>
      <div class="abs" style="left:80px;top:470px;width:920px;display:grid;gap:22px">{''.join(f'<div style="display:flex;justify-content:space-between;border-bottom:2px solid var(--line);padding:22px 0;font-size:46px"><span>{a}</span><span class="m" style="color:{R}">{b}</span></div>' for a, b in [('Peso', 'g'), ('Balanço', 'pontos'), ('Swingweight', 'kg·cm²'), ('Padrão de cordas', '16×19 · 18×20')])}</div>
      <div class="abs" style="left:80px;top:1010px;width:920px;font-size:44px;line-height:1.35">O RACKET DNA cruza tudo isso com o seu jogo em 183 raquetes medidas.</div>{pe('racket')}'''))
    pages.append(C.endcard(END['racket']))
    piece(id='D-C13', fmt='carrossel', day=1, slot='12h30', title='RACKET: cabeça da raquete, 98, 100 ou 105?', kind='utilidade', w=1080, h=1350,
          html=doc('D-C13', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Cabeça da raquete: 98, 100 ou 105? 🎾\n'
                   'Cabeça menor dá controle e pede golpe no centro. Maior dá sweet spot maior e potência mais fácil. 100 é o meio-termo.\n'
                   'Mas peso, balanço, swingweight e cordas mudam tudo junto.\n\n'
                   '🔖 Salva e manda pro seu parceiro de quadra antes da próxima compra.\n'
                   'Faça o teste grátis: link na bio.\n#tenis #raquete #racketdna #tenisamador #beachtennis'),
          notes='100% nas cores do RACKET (lima, preto e branco), conforme a rodada 18. Sem ilustração de raquete: números grandes e barra abstrata. 183 raquetes = número da home (conferido em 22/11 no S03/S04; sem acesso ao repo do site nesta sessão). Card final = CTA RACKET aprovado do S04 (D-C11-5).')

# -------------------------------------------------------------------------------------
# D-R19 · Reel MEME RACKET (qua 09/12) · Tênis às 14h em dezembro: expectativa × realidade
# -------------------------------------------------------------------------------------
def d_r19():
    T = 14.0; tl = TL(T); R = 'var(--racket)'
    s1 = f'''<div {SC(tl, 0, 4.2)}>
      <div class="abs grid-bg" style="inset:0"></div>
      <div class="abs" style="left:90px;top:300px;{at(.05,'fade')}"><span class="tagm" style="background:#2E2E2C;color:#fff">EXPECTATIVA</span></div>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:110px;{at(.25,'rise')}">Tênis às 14h em dezembro.</div>
      <div class="abs" style="left:90px;top:800px;width:900px;font-size:56px;color:var(--muted);{at(1.2,'fade')}">"Treino leve, sol bonito, volto renovado."</div>
    </div>'''
    s2 = f'''<div {SC(tl, 4.2, 10.6)}>
      <div class="abs" style="inset:0;background:{R}"></div>
      <div class="abs" style="left:90px;top:300px;{at(4.25,'stamp')}"><span class="tagm" style="background:var(--ink);color:{R}">REALIDADE</span></div>
      <div class="abs big" style="left:80px;top:420px;font-size:330px;color:var(--ink);{at(4.5,'pop')}">37°</div>
      <div class="abs" style="left:90px;top:780px;width:900px;color:var(--ink)">
        <div class="t" style="font-size:72px;{at(5.4,'rise')}">A quadra frita.</div>
        <div class="t" style="font-size:72px;margin-top:20px;{at(6.6,'rise')}">A bola voa mais.</div>
        <div class="t" style="font-size:72px;margin-top:20px;{at(7.8,'rise')}">E a corda perde tensão.</div></div>
      <div class="abs m" style="left:90px;top:1380px;width:900px;font-size:34px;color:var(--ink);{at(9.0,'fade')}">Dica: não deixa a raquete no carro no sol.</div>
    </div>'''
    s3 = f'''<div {SC(tl, 10.6, T)}>
      <div class="abs" style="inset:0;background:var(--ink)"></div>
      <div class="abs" style="left:90px;top:520px;{at(10.7,'pop')}">{logo(LOGO['racket'], 640)}</div>
      <div class="abs t" style="left:90px;top:760px;width:900px;font-size:76px;{at(11.0,'rise')}">A raquete certa pro seu jogo, no verão e no inverno.</div>
      <div class="abs m" style="left:90px;top:1080px;font-size:36px;color:{R};{at(11.6,'fade')}">Teste grátis e sem cadastro · sportdna.com.br/racket</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:{R};color:var(--ink)">
      <div class="abs" style="left:80px;top:80px"><span class="tagm" style="background:var(--ink);color:{R}">EXPECTATIVA × REALIDADE</span></div>
      <div class="abs t" style="left:80px;top:190px;width:920px;font-size:96px">Tênis às 14h em dezembro.</div>
      <div class="abs big" style="left:70px;top:600px;font-size:340px">37°</div>
      <div class="abs t" style="left:80px;top:1060px;width:920px;font-size:60px">E a corda perde tensão.</div></div>'''
    piece(id='D-R19', fmt='reel', day=2, slot='19h45', title='RACKET · Meme expectativa × realidade: tênis às 14h em dezembro', total=T, poster=.55, kind='meme',
          music='S03/sportdna/reels/D-R16.mp4',
          html=doc('D-R19', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, R),
          caption=('Tênis às 14h em dezembro. Expectativa: treino leve. Realidade: 37 graus. 🥵\n'
                   'Com calor, a bola voa mais e a corda perde tensão mais rápido. Dica: não deixa a raquete no carro no sol.\n\n'
                   'Manda pro parceiro que marca jogo às 14h 👇\n'
                   'Faça o teste grátis: link na bio.\n#tenis #raquete #racketdna #verao #beachtennis'),
          notes='Meme expectativa × realidade, 100% nas cores do RACKET. Fato de uso comum (calor aumenta a perda de tensão da corda; bola fica mais viva no calor), sem número de desempenho. 37° é ilustrativo. Música de banco do D-R16 aprovado, fade de saída.')

# -------------------------------------------------------------------------------------
# D-C14 · Carrossel RUN (qui 10/12) · Dois pares de tênis faz sentido?
# -------------------------------------------------------------------------------------
RODIZIO = [('Cada treino pede um tênis.', 'Longão pede conforto. Tiro e ritmo pedem resposta. Um par só tenta fazer tudo.'),
           ('Os quilômetros se dividem.', 'Com dois pares, cada um roda metade. No calendário, os dois duram mais.'),
           ('Comparar mostra o cansaço.', 'Quando um par já perdeu amortecimento, o outro deixa a diferença clara.'),
           ('O segundo não precisa ser caro.', 'Pode ser o mais simples, pra trote e dia de chuva.')]

def d_c14():
    O = 'var(--run)'
    pages = [page(f'''<div class="abs" style="inset:0;background:{O};color:var(--ink)"></div>
      <div class="abs m" style="left:80px;top:70px;font-size:26px;letter-spacing:.1em;color:var(--ink)">RUN DNA · RODÍZIO</div>
      <div class="abs big" style="left:60px;top:150px;font-size:520px;color:var(--ink)">2</div>
      <div class="abs t" style="left:80px;top:640px;width:920px;font-size:104px;color:var(--ink)">pares de tênis: vale a pena?</div>
      <div class="abs" style="left:80px;top:1020px;font-size:42px;font-weight:700;color:var(--ink)">4 motivos. Arrasta →</div>
      <div class="abs" style="left:80px;top:1240px">{logo('rundna-logo-preto', 260)}</div>''')]
    for i, (t, sub) in enumerate(RODIZIO):
        pages.append(page(f'''<div class="abs grid-bg" style="inset:0"></div>{head('run', 'RODÍZIO', f'{i + 2}/6')}
          <div class="abs big" style="left:70px;top:150px;font-size:300px;color:{O}">0{i + 1}</div>
          <div class="abs t" style="left:80px;top:500px;width:920px;font-size:92px">{t}</div>
          <div class="abs" style="left:80px;top:{740 if len(t) < 24 else 840}px;width:900px;font-size:46px;line-height:1.35;color:#D6D6D3">{sub}</div>{pe('run')}'''))
    pages.append(C.endcard(END['run']))
    piece(id='D-C14', fmt='carrossel', day=3, slot='12h30', title='RUN: dois pares de tênis, vale a pena?', kind='utilidade', w=1080, h=1350,
          html=doc('D-C14', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Dois pares de tênis: vale a pena? 👟👟\n'
                   'Cada treino pede um tênis, os quilômetros se dividem, comparar mostra quando um par cansou e o segundo não precisa ser caro.\n\n'
                   '🔖 Salva e manda pro grupo da corrida.\n'
                   'O RUN DNA mostra o tênis certo pro seu jeito de correr. Relatório completo grátis: link na bio.\n#corrida #tenisdecorrida #rundna #corredores'),
          notes='100% nas cores do RUN (laranja, preto e branco). Sem promessa de desempenho ou de lesão. "Relatório completo grátis no RUN" = texto aprovado do D-FX2. Card final = CTA RUN aprovado do S04 (D-C12-6). Capa laranja para alternar com o preto do D-C13 na grade.')

# -------------------------------------------------------------------------------------
# D-R20 · Reel TREND minivlog com rótulos RUN (sex 11/12) · Domingo de longão em dezembro
# -------------------------------------------------------------------------------------
def d_r20():
    T = 15.0; tl = TL(T); O = 'var(--run)'
    passos = [('5h40', 'despertador. sem soneca.'), ('5h55', 'água e banana.'), ('6h05', 'tênis do longão (não o de tiro).'),
              ('6h15', 'sai antes do sol.'), ('7h50', '16 km. sombra, enfim.'), ('8h10', 'café com o grupo da corrida.')]
    s0 = f'''<div {SC(tl, 0, 2.4)}>
      <div class="abs" style="inset:0;background:{O}"></div>
      <div class="abs t" style="left:90px;top:560px;width:900px;font-size:120px;color:var(--ink);{at(.05,'rise')}">Domingo de longão em dezembro.</div>
    </div>'''
    sc = ''
    for k, (h, txt) in enumerate(passos):
        a, z = 2.4 + k * 1.7, 2.4 + (k + 1) * 1.7
        sc += f'''<div {SC(tl, a, z)}>
          <div class="abs grid-bg" style="inset:0;background-color:{'var(--ink)' if k % 2 == 0 else 'var(--surface)'}"></div>
          <div class="abs big" style="left:80px;top:460px;font-size:200px;color:{O};{at(a + .02,'pop')}">{h}</div>
          <div class="abs t" style="left:90px;top:780px;width:900px;font-size:92px;{at(a + .25,'rise')}">{txt}</div>
          <div class="abs" style="left:90px;top:1300px;width:900px;display:flex;gap:12px">{''.join(f'<div style="flex:1;height:10px;border-radius:5px;background:{O if j <= k else "#2E2E2C"}"></div>' for j in range(6))}</div>
        </div>'''
    e = 2.4 + 6 * 1.7
    s9 = f'''<div {SC(tl, e, T)}>
      <div class="abs" style="inset:0;background:var(--ink)"></div>
      <div class="abs t" style="left:90px;top:400px;width:900px;font-size:92px;{at(e + .05,'rise')}">Cada treino pede um tênis.</div>
      <div class="abs" style="left:90px;top:700px;{at(e + .5,'pop')}">{logo(LOGO['run'], 600)}</div>
      <div class="abs m" style="left:90px;top:920px;font-size:36px;color:{O};{at(e + .9,'fade')}">Relatório completo grátis · sportdna.com.br/run</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{sc}{s9}</section>'
    lista = ''.join(f'<div style="display:flex;gap:30px;padding:16px 0;border-bottom:2px solid var(--line)"><span class="m" style="color:{O};font-size:40px;width:130px">{h}</span><span style="font-size:40px">{t}</span></div>' for h, t in passos)
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:var(--ink)">
      <div class="abs grid-bg" style="inset:0"></div>
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:100px">Domingo de longão em dezembro.</div>
      <div class="abs" style="left:80px;top:450px;width:920px">{lista}</div>
      <div class="abs" style="left:80px;top:1200px">{logo(LOGO['run'], 280)}</div></div>'''
    piece(id='D-R20', fmt='reel', day=4, slot='19h45', title='RUN · Trend minivlog com rótulos: domingo de longão em dezembro', total=T, poster=.4, kind='trend',
          music='S04/sportdna/reels/D-R14.mp4',
          html=doc('D-R20', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, 'var(--ink)'),
          caption=('Domingo de longão em dezembro: 5h40 despertador, 6h15 sai antes do sol, 8h10 café com o grupo. ☀️\n'
                   'E às 6h05, o detalhe que muda o treino: o tênis do longão, não o de tiro.\n\n'
                   'Manda pro grupo da corrida e combina o longão de domingo 👇\n'
                   'O RUN DNA mostra o tênis certo pro seu jeito de correr. Link na bio.\n#corrida #longao #rundna #corredores #domingo'),
          notes='Trend "minivlog com rótulos" (doc de trends do DOT, 06/11: "percurso, preferência, equipamento"), sem pessoa e sem marca. 100% nas cores do RUN. Horários e km ilustrativos, sem promessa. Música de banco do D-R14 aprovado (S04), fade de saída.')

# -------------------------------------------------------------------------------------
# D-C15 · Carrossel SURF (sáb 12/12) · Aula de surf nas férias: 4 perguntas antes de alugar a prancha
# -------------------------------------------------------------------------------------
ALUGUEL = [('Quanto você pesa?', 'A litragem certa depende do seu peso. Prancha que boia pouco não rema.'),
           ('Qual é o seu nível de verdade?', 'Primeira vez? Prancha grande e com bastante volume equilibra melhor.'),
           ('Como está o mar hoje?', 'Onda pequena e fraca pede mais volume pra pegar a onda.'),
           ('Tem prancha macia?', 'Pra começar, a de espuma (soft) é mais segura e perdoa as quedas.')]

def d_c15():
    S = 'var(--surf)'
    pages = [page(f'''<div class="abs" style="inset:0;background:var(--off);color:var(--ink)"></div>
      <div class="abs m" style="left:80px;top:70px;font-size:26px;letter-spacing:.1em;color:#0E4D64">SURF DNA · FÉRIAS</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:104px;color:var(--ink)">Aula de surf nas férias?</div>
      <div class="abs t" style="left:80px;top:420px;width:920px;font-size:104px;color:#0E4D64">4 perguntas antes de alugar a prancha.</div>
      <div class="abs big" style="left:640px;top:780px;font-size:380px;color:{S}">4</div>
      <div class="abs" style="left:80px;top:1240px">{logo('surfdna-logo-fundo-claro', 260)}</div>''', cls='light')]
    for i, (q, a) in enumerate(ALUGUEL):
        pages.append(page(f'''<div class="abs grid-bg" style="inset:0"></div>{head('surf', 'ALUGUEL', f'{i + 2}/6')}
          <div class="abs big" style="left:70px;top:150px;font-size:260px;color:{S}">{i + 1}</div>
          <div class="abs t" style="left:80px;top:470px;width:920px;font-size:92px">{q}</div>
          <div class="abs" style="left:80px;top:{720 if len(q) < 22 else 820}px;width:900px;font-size:46px;line-height:1.35;color:#D6D6D3">{a}</div>{pe('surf')}'''))
    pages.append(C.endcard(END['surf']))
    piece(id='D-C15', fmt='carrossel', day=5, slot='12h30', title='SURF: aula de surf nas férias, 4 perguntas antes de alugar a prancha', kind='utilidade', w=1080, h=1350,
          html=doc('D-C15', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Aula de surf nas férias? Antes de alugar a prancha, 4 perguntas. 🏄\n'
                   'Quanto você pesa, qual o seu nível de verdade, como está o mar e se tem prancha macia pra começar.\n\n'
                   '🔖 Salva e manda pra quem vai surfar pela primeira vez nessas férias.\n'
                   'O SURF DNA calcula os litros pelo seu peso, o seu nível e o seu mar. Link na bio.\n#surf #aulasdesurf #surfdna #ferias #verao'),
          notes='100% nas cores do SURF (azul, petróleo, preto e off-white). Tema novo (aluguel e aula nas férias). Sem desenho de prancha. Texto do SURF DNA igual ao aprovado no D-R17. Card final = CTA SURF aprovado (D-C9-6, S03). Capa clara para alternar a grade.')

# -------------------------------------------------------------------------------------
# D-R21 · Reel MEME SURF (dom 13/12) · Grupo do surf, 5h12
# -------------------------------------------------------------------------------------
def d_r21():
    T = 15.0; tl = TL(T); S = 'var(--surf)'
    msgs = [('Rafa', 'tá dando?', False, 1.0), ('Bia', 'meio metro e mexido', False, 2.2), ('Rafa', 'vou', False, 3.4),
            ('Bia', 'de quê?', False, 4.4), ('Rafa', 'da minha 5\'10, ué', False, 5.6), ('Bia', 'boa sorte remando 🫡', False, 7.0)]
    def bub(n, t, tt):
        return (f'<div style="margin:16px 0;{at(tt,"rise",.3)}"><div class="bub" style="background:#1F2A2E;color:#fff;display:inline-block">'
                f'<div class="m" style="font-size:24px;color:{S};margin-bottom:6px">{n}</div>{t}</div></div>')
    s1 = f'''<div {SC(tl, 0, 9.4)}>
      <div class="abs" style="inset:0;background:var(--ink)"></div>
      <div class="abs" style="left:90px;top:290px;width:900px;display:flex;align-items:center;gap:20px;border-bottom:2px solid var(--line);padding-bottom:22px">
        <div style="width:80px;height:80px;border-radius:50%;background:{S}"></div><div><div class="t" style="font-size:44px">grupo do surf</div><div class="m" style="font-size:24px;color:var(--muted)">5h12</div></div></div>
      <div class="abs" style="left:90px;top:440px;width:900px">{''.join(bub(n, t, tt) for n, t, me, tt in msgs)}</div>
      <div class="abs m" style="left:90px;top:1480px;font-size:24px;color:var(--muted)">SIMULAÇÃO · NOMES DE EXEMPLO</div>
    </div>'''
    s2 = f'''<div {SC(tl, 9.4, T)}>
      <div class="abs" style="inset:0;background:{S}"></div>
      <div class="abs t" style="left:90px;top:400px;width:900px;font-size:120px;color:var(--ink);{at(9.45,'rise')}">Meio metro pede volume.</div>
      <div class="abs" style="left:90px;top:800px;width:900px;font-size:52px;font-weight:700;color:var(--ink);line-height:1.3;{at(10.4,'fade')}">O SURF DNA calcula a prancha pro seu peso, o seu nível e o seu mar.</div>
      <div class="abs" style="left:90px;top:1150px;{at(11.2,'pop')}">{logo('surfdna-logo-preto', 560)}</div>
      <div class="abs m" style="left:90px;top:1330px;font-size:34px;color:var(--ink);{at(11.6,'fade')}">sportdna.com.br/surf</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}</section>'
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:var(--ink)">
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:96px">Grupo do surf, 5h12.</div>
      <div class="abs" style="left:80px;top:330px;width:920px">{''.join(f'<div style="margin:14px 0"><div class="bub" style="background:#1F2A2E;color:#fff;display:inline-block;font-size:46px"><div class="m" style="font-size:24px;color:{S}">{n}</div>{t}</div></div>' for n, t, me, tt in msgs[1:5])}</div>
      <div class="abs" style="left:80px;top:1160px"><span class="tagm" style="background:{S};color:var(--ink)">MEIO METRO PEDE VOLUME</span></div></div>'''
    piece(id='D-R21', fmt='reel', day=6, slot='19h45', title='SURF · Meme: o grupo do surf às 5h12', total=T, poster=.5, kind='meme',
          music='S03/sportdna/reels/D-R17.mp4',
          html=doc('D-R21', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, 'var(--ink)'),
          caption=('Grupo do surf, 5h12: "tá dando?" "meio metro e mexido" "vou" "de quê?" 🌊\n'
                   'Meio metro pede volume. A prancha do mar grande não é a do verão.\n\n'
                   'Manda no grupo do surf e marca quem vai de pranchinha mesmo assim 👇\n'
                   'O SURF DNA calcula a prancha pro seu peso, o seu nível e o seu mar. Link na bio.\n#surf #surfdna #verao #prancha #meme'),
          notes='Meme em conversa de grupo (genérica, sem marca de app), etiqueta "simulação · nomes de exemplo". 100% nas cores do SURF. Música de banco do D-R17 aprovado, fade de saída.')

# -------------------------------------------------------------------------------------
# D-C16 · Carrossel SPORT DNA (seg 14/12) · Mito ou verdade? 5 frases de loja de esporte
# -------------------------------------------------------------------------------------
MITOS = [('RACKET', 'Corda mais esticada dá mais potência.', 'MITO', 'Mais tensão dá mais controle. Menos tensão devolve mais potência e conforto.'),
         ('RUN', 'Quanto mais amortecimento, melhor pra todo mundo.', 'MITO', 'Depende do seu peso, do ritmo e da distância. Macio demais pode tirar estabilidade.'),
         ('SURF', 'Prancha menor é pra quem surfa melhor.', 'DEPENDE', 'Prancha menor exige mais técnica. O volume certo vem do peso, do nível e do mar.'),
         ('RUN', 'O tênis mais caro é o melhor.', 'MITO', 'O certo é o que combina com a sua pisada, o seu ritmo e a sua distância.'),
         ('SURF', 'Parafina é tudo igual.', 'MITO', 'Tem parafina pra água fria e pra água quente. A errada escorrega ou derrete.')]

def d_c16():
    pages = [page(f'''<div class="abs" style="inset:0;background:var(--off);color:var(--ink)"></div>
      <div class="abs m" style="left:80px;top:70px;font-size:26px;letter-spacing:.1em;color:var(--mutedL)">SPORT DNA · MITO OU VERDADE</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:110px;color:var(--ink)">5 frases que você já ouviu na loja.</div>
      <div class="abs" style="left:80px;top:640px;display:flex;gap:24px"><span class="tagm" style="background:var(--ink);color:#fff;font-size:44px">MITO</span><span class="tagm" style="border:4px solid var(--ink);color:var(--ink);font-size:44px">VERDADE</span></div>
      <div class="abs" style="left:80px;top:1000px;font-size:42px;font-weight:700;color:var(--ink)">Arrasta e confere →</div>
      <div class="abs" style="left:80px;top:1240px">{logo('sportdna-logo-fundo-claro', 280)}</div>''', cls='light')]
    for i, (sp, frase, ver, exp) in enumerate(MITOS):
        pages.append(page(f'''<div class="abs grid-bg" style="inset:0"></div>
          <div class="abs m" style="left:80px;top:70px;font-size:26px;letter-spacing:.1em;color:var(--muted)">SPORT DNA · {sp}</div>
          <div class="abs m" style="right:80px;top:70px;font-size:26px;color:var(--muted)">{i + 2}/7</div>
          <div class="abs t" style="left:80px;top:170px;width:920px;font-size:{88 if len(frase) < 40 else 78}px">"{frase}"</div>
          <div class="abs" style="left:80px;top:620px;--r:-3deg;transform:rotate(-3deg)"><span class="tagm" style="background:#fff;color:var(--ink);font-size:72px;padding:14px 34px">{ver}</span></div>
          <div class="abs" style="left:80px;top:820px;width:900px;font-size:48px;line-height:1.35;color:#D6D6D3">{exp}</div>
          <div class="abs" style="left:80px;top:1240px">{logo('sportdna-logo-fundo-escuro', 260)}</div>'''))
    pages.append(C.endcard(END['sport']))
    piece(id='D-C16', fmt='carrossel', day=7, slot='12h30', title='Mito ou verdade? 5 frases de loja de esporte', kind='engajamento', w=1080, h=1350,
          html=doc('D-C16', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Mito ou verdade? 5 frases que você já ouviu na loja de esporte. 🤔\n'
                   '"Corda mais esticada dá mais potência." "O tênis mais caro é o melhor." "Parafina é tudo igual." Arrasta e confere.\n\n'
                   'Manda pro amigo que repete uma dessas 👇\n'
                   'Faça o teste grátis: link na bio.\n#sportdna #tenis #corrida #surf #mitoouverdade'),
          notes='Marca-mãe em preto, branco e off-white, sem misturar as cores dos esportes (rodada 18). Fatos de uso comum, sem número. Card final = CTA SPORT DNA aprovado do S04 (D-C10-6).')

# -------------------------------------------------------------------------------------
# Stories (1 sequência de 3 por dia, 12h, sem adesivo): Dicionário DNA, layout tipográfico
# -------------------------------------------------------------------------------------
DIC5 = [(1, 'racket', 'Swingweight', 'O quanto a raquete "pesa" no movimento, não na balança. Mais alto: mais estabilidade e potência, e mais esforço pra acelerar.',
         'Duas raquetes com o mesmo peso podem ter swingweight bem diferente. Na quadra, você sente.'),
        (2, 'run', 'Cabedal', 'A parte de cima do tênis, que envolve o pé. Tecido, malha e reforços.',
         'No calor, cabedal que respira faz diferença. Calcanhar firme segura o pé no lugar.'),
        (3, 'surf', 'Leash', 'A cordinha que prende a prancha ao tornozelo.',
         'O tamanho costuma acompanhar o da prancha: prancha de 6 pés, leash de 6 pés.'),
        (4, 'racket', 'Sweet spot', 'A área do encordoamento onde a bola sai limpa, com menos vibração e mais controle.',
         'Cabeça maior, sweet spot maior. Por isso a 105 perdoa mais o golpe fora do centro.'),
        (5, 'run', 'Placa de carbono', 'Placa rígida dentro da entressola de alguns tênis de corrida, que deixa a passada mais responsiva.',
         'É feita pra ritmo forte e prova. Pra trote e longão leve, nem todo corredor precisa.'),
        (6, 'surf', 'Espessura', 'O quanto a prancha é grossa, medido no ponto mais alto.',
         'Mais espessura, mais volume: a prancha boia e rema melhor. Menos espessura: mais sensibilidade.'),
        (7, 'racket', 'Híbrido', 'Encordoamento com duas cordas diferentes: uma nas verticais e outra nas horizontais.',
         'Junta o melhor das duas: por exemplo, controle de uma e conforto da outra.')]
CTA_D = {'racket': ('A raquete certa para o seu jogo e <span style="color:var(--racket)">o seu braço.</span>', ['183 raquetes medidas, cruzadas com você', 'Peso, balanço e swingweight pro seu jogo', 'Você vê a prévia antes de pagar'], 'Teste grátis · sem cadastro', 'Fazer o teste grátis →', 'sportdna.com.br/racket'),
         'run': ('O tênis certo para <span style="color:var(--run)">o seu jeito de correr.</span>', ['Drop, espuma e custo por km pro seu perfil', 'Relatório completo grátis', 'Nenhuma marca no comando'], 'Grátis · sem cadastro', 'Descobrir meu tênis →', 'sportdna.com.br/run'),
         'surf': ('A prancha certa para <span style="color:var(--surf)">o seu surf e o seu mar.</span>', ['Tipo, medidas e litragem certos para você', '13 tipos de prancha disputam o seu resultado', 'Você vê a prévia antes de decidir'], 'Prévia grátis · 3 minutos · sem cadastro', 'Descobrir minha prancha →', 'sportdna.com.br/surf')}

def d_stories():
    for n, (d, sp, termo, defi, prat) in enumerate(DIC5):
        sid = f'D-S{30 + n}'; c = COR[sp]; nm = NOME[sp].split()[0]
        f1 = f'''<section class="page" style="width:1080px;height:1920px">
          <div class="abs lbl" style="left:80px;top:300px">DICIONÁRIO DNA · {nm}</div>
          <div class="abs" style="left:80px;top:360px;width:920px;height:6px;background:{c}"></div>
          <div class="abs t" style="left:80px;top:440px;width:920px;font-size:{170 if len(termo) < 10 else 130}px;color:{c}">{termo}</div>
          <div class="abs t" style="left:80px;top:{760 if len(termo) < 10 else 900}px;width:920px;font-size:64px;line-height:1.15">{defi}</div>
          <div class="abs" style="left:80px;top:1380px;font-size:40px;color:var(--muted)">Salva e manda pro seu parceiro de treino.</div>
          <div class="abs" style="left:80px;top:1480px">{logo(LOGO[sp], 300)}</div></section>'''
        f2 = f'''<section class="page" style="width:1080px;height:1920px">
          <div class="abs lbl" style="left:80px;top:300px">NA PRÁTICA · {nm}</div>
          <div class="abs" style="left:80px;top:360px;width:920px;height:6px;background:{c}"></div>
          <div class="abs t" style="left:80px;top:440px;font-size:110px;color:{c}">{termo}</div>
          <div class="abs t" style="left:80px;top:660px;width:920px;font-size:68px;line-height:1.15">{prat}</div>
          <div class="abs" style="left:80px;top:1380px;font-size:40px;color:var(--muted)">Qual é o certo pra você? O teste responde →</div>
          <div class="abs" style="left:80px;top:1480px">{logo(LOGO[sp], 300)}</div></section>'''
        h, items, selo, botao, url = CTA_D[sp]
        f3 = f'''<section class="page" style="width:1080px;height:1920px">
          <div class="abs" style="left:80px;top:300px">{logo(LOGO[sp], 380)}</div>
          <div class="abs t" style="left:80px;top:430px;width:920px;font-size:104px">{h}</div>
          <div class="abs" style="left:80px;top:850px;width:920px;display:grid;gap:26px">{''.join(f'<div style="display:flex;gap:24px;align-items:center;font-size:46px;font-weight:700"><span style="flex:none;width:58px;height:58px;border-radius:50%;background:{c};color:var(--ink);display:flex;align-items:center;justify-content:center;font-size:34px">✓</span>{it}</div>' for it in items)}</div>
          <div class="abs" style="left:80px;top:1290px"><span style="display:inline-block;border:3px solid {c};color:{c};border-radius:14px;padding:10px 22px;font-size:34px;font-weight:700">{selo}</span></div>
          <div class="abs" style="left:80px;top:1390px;width:920px;height:140px;border-radius:30px;background:{c};color:var(--ink);display:flex;align-items:center;justify-content:center" class="t"><span class="t" style="font-size:60px">{botao}</span></div>
          <div class="abs m" style="left:0;right:0;top:1570px;text-align:center;font-size:38px">{url}</div></section>'''
        piece(id=sid, fmt='story', day=d, slot='12h', title=f'Dicionário DNA: {termo} · sequência de 3', w=1080, h=1920, frames=3,
              html=doc(sid, FONTS, CSS, f1 + f2 + f3, 1080, 1920), caption='(story, sem legenda; postar os 3 quadros em sequência, no mesmo horário)', sticker='', kind='story',
              notes=f'Sequência de 3 sem adesivo, layout tipográfico aprovado (sem ilustração de equipamento): termo → na prática → CTA {NOME[sp]}. Uma cor só ({NOME[sp]}). Termo novo (não usado nas últimas 4 semanas).')

def build():
    d_c13(); d_r19(); d_c14(); d_r20(); d_c15(); d_r21(); d_c16(); d_stories()

build()
