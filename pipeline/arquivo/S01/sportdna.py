"""SPORT DNA · Pack Semanal 01. Archivo ExtraBold / DM Sans / JetBrains Mono; Syne só em números de destaque e logos.
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

def raquete(stroke='#fff', w=420, accent='var(--racket)', anim_t=None):
    """Desenho técnico em linha (silhueta genérica de raquete) com cotas."""
    d = '' if anim_t is None else f'style="stroke-dasharray:2400;animation:draw 1.4s cubic-bezier(.2,.75,.15,1) {anim_t}s 1 both;--len:2400"'
    strings = ''.join(f'<line x1="{x}" y1="40" x2="{x}" y2="380" stroke="{stroke}" stroke-width="1.5" opacity=".35"/>' for x in range(80, 341, 22))
    strings += ''.join(f'<line x1="50" y1="{y}" x2="370" y2="{y}" stroke="{stroke}" stroke-width="1.5" opacity=".35"/>' for y in range(70, 361, 20))
    return f'''<svg width="{w}" height="{w*2.3:.0f}" viewBox="0 0 420 966" fill="none">
      <defs><clipPath id="hd"><ellipse cx="210" cy="210" rx="160" ry="185"/></clipPath></defs>
      <g clip-path="url(#hd)">{strings}</g>
      <ellipse cx="210" cy="210" rx="170" ry="196" stroke="{stroke}" stroke-width="6" {d}/>
      <path d="M150 395 L196 560 M270 395 L224 560 M196 560 L196 900 Q196 930 210 930 Q224 930 224 900 L224 560" stroke="{stroke}" stroke-width="6" {d}/>
      <line x1="20" y1="14" x2="400" y2="14" stroke="{accent}" stroke-width="3"/><line x1="40" y1="4" x2="40" y2="24" stroke="{accent}" stroke-width="3"/><line x1="380" y1="4" x2="380" y2="24" stroke="{accent}" stroke-width="3"/>
    </svg>'''

def prancha(stroke='#fff', w=300, accent='var(--surf)', anim_t=None):
    d = '' if anim_t is None else f'style="stroke-dasharray:3000;animation:draw 1.6s cubic-bezier(.2,.75,.15,1) {anim_t}s 1 both;--len:3000"'
    return f'''<svg width="{w}" height="{w*3.6:.0f}" viewBox="0 0 300 1080" fill="none">
      <path d="M150 20 C230 120 262 330 262 560 C262 800 236 960 186 1050 L150 1030 L114 1050 C64 960 38 800 38 560 C38 330 70 120 150 20Z" stroke="{stroke}" stroke-width="6" {d}/>
      <line x1="150" y1="40" x2="150" y2="1020" stroke="{stroke}" stroke-width="2" stroke-dasharray="10 12" opacity=".5"/>
      <path d="M130 960 l-10 60 M170 960 l10 60 M150 940 v70" stroke="{accent}" stroke-width="5"/>
      <line x1="8" y1="560" x2="292" y2="560" stroke="{accent}" stroke-width="3"/><line x1="8" y1="545" x2="8" y2="575" stroke="{accent}" stroke-width="3"/><line x1="292" y1="545" x2="292" y2="575" stroke="{accent}" stroke-width="3"/>
    </svg>'''

# =====================================================================================
# D-R1 · Reel · RACKET · 4 números da ficha técnica
# =====================================================================================
def chat_user(txt, style=''):
    return f'<div style="display:flex;justify-content:flex-end;{style}"><div style="max-width:78%;background:#2E2E2C;color:#fff;border-radius:34px 34px 8px 34px;padding:24px 30px;font-size:40px;line-height:1.3">{txt}</div></div>'

def chat_ia(txt, style=''):
    return (f'<div style="display:flex;gap:20px;align-items:flex-start;{style}"><div class="m" style="flex:none;width:72px;height:72px;border-radius:50%;background:var(--off);color:var(--ink);display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700">IA</div>'
            f'<div style="flex:1;font-size:40px;line-height:1.35;color:#fff;padding-top:8px">{txt}</div></div>')

def chat_dots(t0, x, y):
    return ''.join(f'<div class="abs" style="left:{x + i*34}px;top:{y}px;width:20px;height:20px;border-radius:50%;background:var(--muted);opacity:0;animation:typing 1.0s ease-in-out {t0 + i*.15:.2f}s 1 both"></div>' for i in range(3))

def d_r1():
    """v2: simulação de quem pergunta para uma IA genérica qual raquete comprar. Parece simples, não é."""
    T = 21.0
    tl = TL(T)
    s1 = f"""<div {tl.scene(0, 8.2, fin=False)}>
      <div class="abs t" style="left:90px;top:300px;width:900px;font-size:96px;{at(.05,'rise', .6)}">Perguntei pra IA qual raquete comprar.</div>
      <div class="abs" style="left:90px;top:600px;width:900px;background:var(--surface);border-radius:40px;padding:36px 36px 44px;height:820px">
        <div class="lbl" style="margin-bottom:30px">ASSISTENTE DE IA · SIMULAÇÃO</div>
        <div style="{at(.7,'rise', .4)}">{chat_user('qual a melhor raquete de tênis pra mim?')}</div>
        <div style="margin-top:40px;{at(2.6,'fade', .3)}">{chat_ia('Para quem está começando, uma raquete leve e com cabeça grande costuma ser uma boa escolha. Experimente algumas na loja!')}</div>
      </div>
      {chat_dots(1.5, 230, 940)}
    </div>"""
    s2 = f"""<div {tl.scene(8.2, 10.8, fade=.1)}>
      <div class="abs t" style="left:90px;top:440px;width:900px;font-size:116px;white-space:nowrap;{at(8.25,'rise', .5)}">Parece simples.</div>
      <div class="abs t" style="left:90px;top:620px;width:900px;font-size:150px;color:var(--racket);{at(9.1,'pop', .4)}">Não é.</div>
    </div>"""
    itens = [('BRAÇO', 'Já sentiu o cotovelo?'), ('JOGO', 'Bate chapado ou com spin?'), ('NÍVEL', 'Há quanto tempo joga?'), ('FICHA', '62 raquetes medidas')]
    lista = ''.join(f'<div style="display:flex;gap:30px;align-items:baseline;padding:26px 0;border-top:2px solid var(--line);{at(11.2 + i*.45, "rise", .45)}"><span class="lbl" style="width:150px;color:var(--racket)">{k}</span><span class="t" style="font-size:56px">{v}</span></div>' for i, (k, v) in enumerate(itens))
    s3 = f"""<div {tl.scene(10.8, 15.6, fade=.1)}>
      <div class="abs t" style="left:90px;top:320px;width:900px;font-size:80px;{at(10.85,'rise', .5)}">O que a resposta não sabia:</div>
      <div class="abs" style="left:90px;top:560px;width:900px">{lista}</div>
    </div>"""
    s4 = f"""<div {tl.scene(15.6, 18.6, fade=.1)}>
      <div class="abs t" style="left:90px;top:380px;width:900px;font-size:92px;{at(15.65,'rise', .5)}">O RACKET DNA foi calibrado com atletas e esportistas.</div>
      <div class="abs" style="left:90px;top:840px;width:880px;font-size:50px;line-height:1.3;color:var(--muted);{at(16.4,'fade', .5)}">E testado em vários perfis de jogo antes de ir ao ar.</div>
    </div>"""
    s5 = f"""<div {tl.scene(18.6, T, fout=False)}>
      <div class="abs" style="left:90px;top:600px;{at(18.65,'fade', .6)}">{logo('racketdna-logo-fundo-escuro', 900)}</div>
      <div class="abs m" style="left:90px;top:800px;font-size:36px;{at(19.1,'fade')}">Teste grátis e sem cadastro · sportdna.com.br</div>
    </div>"""
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}{s5}</section>'
    cover_body = f"""<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:110px;width:920px;font-size:100px">Perguntei pra IA qual raquete comprar.</div>
      <div class="abs" style="left:80px;top:470px;width:920px;background:var(--surface);border-radius:40px;padding:36px 36px 44px">
        <div class="lbl" style="margin-bottom:26px">ASSISTENTE DE IA · SIMULAÇÃO</div>
        {chat_user('qual a melhor raquete de tênis pra mim?')}
        <div style="margin-top:34px">{chat_ia('Para quem está começando, uma raquete leve e com cabeça grande costuma ser uma boa escolha…')}</div></div>
      <div class="abs t" style="left:80px;top:1150px;font-size:76px;color:var(--racket)">Parece simples. Não é.</div></div>"""
    piece(id='D-R1', fmt='reel', day=1, slot='19h45', title='RACKET: perguntei pra IA qual raquete comprar', total=T, poster=.2,
          html=doc('D-R1', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--ink)'),
          caption=('Perguntei pra IA qual raquete comprar. A resposta: "uma leve, com cabeça grande, experimenta na loja". 🎾\n\n'
                   'Parece simples. Não é. Faltou o seu braço, o seu jogo, o seu nível e a ficha técnica de cada raquete.\n\n'
                   'O RACKET DNA foi calibrado com atletas e esportistas e testado em vários perfis de jogo antes de ir ao ar. Ele cruza tudo isso com 62 raquetes medidas.\n\n'
                   'Teste grátis e sem cadastro. Link na bio.\n#racketdna #sportdna #tenis #raquetedetenis #tenisbrasil #ia'),
          notes='v2 (você reprovou a v1 da ficha técnica). Nova linha do feedback geral: simulação de IA genérica, "parece simples, mas não é", modelo calibrado com atletas e esportistas. IA sem marca e com etiqueta de simulação.')

# =====================================================================================
# D-C1 · Carrossel · SURF · Litragem
# =====================================================================================
def d_c1():
    pages = [page(f'''
      <div class="abs lbl" style="left:80px;top:90px;color:var(--surf)">SURF DNA · GUIA RÁPIDO</div>
      <div class="abs n" style="left:70px;top:200px;font-size:200px;color:var(--surf)">37,6<span style="font-size:110px"> L</span></div>
      <div class="abs t" style="left:80px;top:520px;width:600px;font-size:88px">O número que decide se você rema.</div>
      <div class="abs" style="left:850px;top:230px">{prancha(w=180)}</div>
      <div class="abs m" style="left:80px;top:1210px;font-size:28px;color:var(--muted)">Arrasta →</div>''')]
    pages.append(page(f'''
      <div class="abs lbl" style="left:80px;top:90px">1 · O QUE É</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:96px">Litragem é o volume da prancha.</div>
      <div class="abs" style="left:80px;top:520px;width:880px;font-size:48px;line-height:1.3">Mais litros, mais a prancha flutua e mais fácil fica remar. Menos litros, mais ela afunda na curva e responde rápido.</div>
      <div class="abs" style="left:80px;top:960px;width:920px;display:flex;gap:20px"><span class="chip" style="color:var(--surf)">+ litros = + flutuação</span><span class="chip" style="color:var(--muted)">− litros = + resposta</span></div>''', cls='light'))
    pages.append(page(f'''
      <div class="abs lbl" style="left:80px;top:90px">2 · DEPENDE DE</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:96px">Três coisas. Nenhuma é a marca.</div>
      <div class="abs" style="left:80px;top:500px;width:920px">
        <div style="display:flex;align-items:baseline;gap:40px;padding:34px 0;border-top:2px solid var(--line)"><span class="n" style="font-size:110px;color:var(--surf);width:120px">1</span><span class="t" style="font-size:72px">Seu peso</span></div>
        <div style="display:flex;align-items:baseline;gap:40px;padding:34px 0;border-top:2px solid var(--line)"><span class="n" style="font-size:110px;color:var(--surf);width:120px">2</span><span class="t" style="font-size:72px">Seu nível</span></div>
        <div style="display:flex;align-items:baseline;gap:40px;padding:34px 0;border-top:2px solid var(--line);border-bottom:2px solid var(--line)"><span class="n" style="font-size:110px;color:var(--surf);width:120px">3</span><span class="t" style="font-size:72px">O seu mar</span></div></div>'''))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--surf)"></div>
      <div class="abs lbl" style="left:80px;top:90px;color:var(--ink)">3 · O ERRO MAIS COMUM</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:100px;color:var(--ink)">Pouco volume para o nível.</div>
      <div class="abs" style="left:80px;top:560px;width:600px;font-size:48px;line-height:1.3;color:var(--ink)">A prancha afunda, você rema mais, chega atrasado na onda e acha que o problema é você.</div>
      <div class="abs" style="left:760px;top:420px">{prancha(stroke='#0A0A0A', w=230, accent='#0A0A0A')}</div>'''))
    pages.append(page(f'''
      <div class="abs lbl" style="left:80px;top:90px">4 · NÃO É SÓ LITRO</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:92px">Mesmo volume, prancha diferente.</div>
      <div class="abs" style="left:80px;top:520px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:20px">
        {''.join(f'<div style="border:2px solid var(--line);border-radius:24px;padding:30px"><div class="lbl">{a}</div><div class="t" style="font-size:52px;margin-top:12px">{b}</div></div>' for a, b in [('COMPRIMENTO','mais remada'),('LARGURA','mais estabilidade'),('RABETA','muda a curva'),('QUILHAS','mudam o controle')])}</div>
      <div class="abs" style="left:80px;top:1130px;width:900px;font-size:40px;color:var(--muted)">O SURF DNA olha tudo junto: são 13 tipos de prancha.</div>'''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:100px">Calcule a sua.</div>
      <div class="abs" style="left:80px;top:330px;width:900px;font-size:48px;line-height:1.3;color:var(--mutedL)">Calculadora de litragem grátis, a partir do seu peso, do seu nível e do seu mar.</div>
      <div class="abs m" style="left:80px;top:620px;font-size:40px">sportdna.com.br/ferramentas/litragem</div>
      <div class="abs lbl" style="left:80px;top:1200px">SURF DNA · SPORT DNA</div>''', cls='light'))
    piece(id='D-C1', fmt='carrossel', day=2, slot='12h30', title='SURF: litragem, o número que decide se você rema', w=1080, h=1350,
          html=doc('D-C1', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Litragem: o número que decide se você rema. 🏄\n\n'
                   'É o volume da prancha. Mais litros, mais flutuação e remada fácil. Menos litros, mais resposta.\n'
                   'Depende de três coisas: o seu peso, o seu nível e o seu mar. Nenhuma delas é a marca.\n\n'
                   'Salva para a próxima compra e calcula a sua na calculadora grátis: sportdna.com.br/ferramentas/litragem\n'
                   '#surfdna #sportdna #surf #pranchadesurf #surfbrasil #litragem'),
          notes='Guia editorial. 37,6 L é a medida de exemplo usada pela marca (chips de medida do manual de movimento). Sem fórmulas inventadas.')

# =====================================================================================
# D-R2 · Reel · RUN · Custo por km
# =====================================================================================
def d_r2():
    T = 17.4
    tl = TL(T)
    s1 = f'''<div {tl.scene(0, 3.0, fin=False)}>
      <div class="abs lbl" style="left:90px;top:330px;color:var(--run)">RUN DNA · CONTA RÁPIDA</div>
      <div class="abs t" style="left:90px;top:400px;width:900px;font-size:124px;{at(.1,'rise', .6)}">Quanto custa cada km do seu <span style="color:var(--run)">tênis?</span></div>
    </div>'''
    s2 = f'''<div {tl.scene(3.0, 10.6, fade=.12)}>
      <div class="abs lbl" style="left:90px;top:330px">PREÇO DO PAR</div>
      <div class="abs n" style="left:80px;top:400px;font-size:130px;{at(3.1,'rise', .5)}"><span style="font-size:80px">R$ </span>664,99</div>
      <div class="abs lbl" style="left:90px;top:680px;{at(4.6,'fade')}">DURABILIDADE ESTIMADA</div>
      <div class="abs n" style="left:80px;top:750px;font-size:130px;{at(4.7,'rise', .5)}"><span style="color:var(--muted)">÷ </span>700<span style="font-size:80px"> km</span></div>
      <div class="abs rule" style="left:90px;right:90px;top:1010px;height:4px;background:#fff;transform-origin:left;{at(6.3,'grow', .5)}"></div>
      <div class="abs n" style="left:80px;top:1060px;font-size:180px;color:var(--run);{at(6.6,'rise', .5)}"><span style="font-size:100px">R$ </span>0,95</div>
      <div class="abs t" style="left:90px;top:1280px;font-size:64px;{at(7.2,'fade')}">por quilômetro.</div>
    </div>'''
    s3 = f'''<div {tl.scene(10.6, 14.2)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:104px;{at(10.7,'rise', .6)}">O tênis mais barato nem sempre é o mais barato <span style="color:var(--run)">por km.</span></div>
    </div>'''
    s4 = f'''<div {tl.scene(14.2, T, fout=False)}>
      <div class="abs" style="left:90px;top:440px;width:900px;font-size:54px;line-height:1.3;{at(14.3,'rise', .6)}">O RUN DNA mostra o custo por km de cada finalista, entre 212 tênis.</div>
      <div class="abs t" style="left:90px;top:760px;font-size:96px;color:var(--run);{at(14.8,'fade', .6)}">RUN DNA</div>
      <div class="abs m" style="left:90px;top:900px;font-size:34px;{at(15.2,'fade')}">Relatório R$ 9,99 · sportdna.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:var(--run);color:var(--ink)">
      <div class="abs lbl" style="left:80px;top:90px;color:var(--ink)">RUN DNA · CONTA RÁPIDA</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:112px">Quanto custa cada km do seu tênis?</div>
      <div class="abs n" style="left:70px;top:820px;font-size:200px"><span style="font-size:110px">R$ </span>0,95</div>
      <div class="abs m" style="left:80px;top:1110px;font-size:34px">R$ 664,99 ÷ 700 km</div></div>'''
    piece(id='D-R2', fmt='reel', day=4, slot='19h45', title='RUN: custo por km', total=T, poster=.5,
          html=doc('D-R2', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--run)'),
          caption=('Quanto custa cada km do seu tênis? 🏃\n\n'
                   'R$ 664,99 ÷ 700 km de durabilidade = R$ 0,95 por km.\n'
                   'O tênis mais barato nem sempre é o mais barato por km.\n\n'
                   'O RUN DNA mostra o custo por km de cada finalista, entre 212 tênis, e o mês certo de trocar. Relatório: R$ 9,99. Link na bio.\n'
                   '#rundna #sportdna #corrida #corridaderua #running #tenisdecorrida'),
          notes='Conta feita com o exemplo do site (R$ 664,99, 700 km, R$ 0,95/km). Capa laranja para a grade alternar com preto.')

# =====================================================================================
# D-C2 · Carrossel · Como o motor escolhe (PRODUTO)
# =====================================================================================
def d_c2():
    pages = [page(f'''
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:128px">Nenhuma marca paga para aparecer.</div>
      <div class="abs" style="left:80px;top:760px;width:860px;font-size:48px;line-height:1.3;color:var(--muted)">Como a SPORT DNA escolhe o seu equipamento, em 4 passos.</div>
      <div class="abs" style="left:80px;top:1120px;display:flex;gap:18px">{logo('racketdna-icone', 110)}{logo('surfdna-icone', 110)}{logo('rundna-icone', 110)}</div>''')]
    steps = [
        ('01', 'Você responde.', 'Corpo, nível, estilo e o equipamento que usa hoje. Teste grátis e sem cadastro.', None),
        ('02', 'O motor cruza com as fichas técnicas.', None, [('62', 'raquetes', 'var(--racket)'), ('13', 'tipos de prancha', 'var(--surf)'), ('212', 'tênis de corrida', 'var(--run)')]),
        ('03', 'E com casos reais.', '422 casos reais calibram o SURF DNA. Reviews de especialistas entram em cada análise.', None),
    ]
    for num, tit, txt, stats in steps:
        if stats:
            inner = ''.join(f'<div style="display:flex;align-items:baseline;gap:30px;padding:26px 0;border-top:2px solid var(--line)"><span class="n" style="font-size:140px;color:{c};width:330px">{v}</span><span class="t" style="font-size:54px">{l}</span></div>' for v, l, c in stats)
            body = f'<div class="abs" style="left:80px;top:560px;width:920px">{inner}</div>'
        else:
            body = f'<div class="abs" style="left:80px;top:600px;width:880px;font-size:52px;line-height:1.3">{txt}</div>'
        pages.append(page(f'''
          <div class="abs n" style="left:70px;top:90px;font-size:120px;color:var(--muted)">{num}</div>
          <div class="abs t" style="left:80px;top:260px;width:920px;font-size:96px">{tit}</div>{body}'''))
    # 04 resultado: card
    pages.append(page(f'''
      <div class="abs n" style="left:70px;top:90px;font-size:120px;color:var(--mutedL)">04</div>
      <div class="abs t" style="left:80px;top:260px;width:920px;font-size:96px">Você recebe o finalista e o porquê.</div>
      <div class="abs" style="left:80px;top:560px;width:920px;background:var(--ink);color:#fff;border-radius:36px;padding:50px">
        <div class="lbl" style="color:var(--racket)">EXEMPLO · RACKET DNA</div>
        <div style="display:flex;align-items:flex-end;gap:30px;margin-top:20px"><span class="n" style="font-size:200px;color:var(--racket)">95%</span><span class="t" style="font-size:48px;padding-bottom:30px">DNA Score</span></div>
        <div class="m" style="font-size:32px;margin-top:20px;color:var(--muted)">295 g · 100 pol² · 61 RA · 16×19</div>
        <div style="font-size:36px;margin-top:20px">escolhida entre 62 raquetes, com grip, corda e tensão.</div></div>''', cls='light'))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:110px">Teste grátis. Relatório de R$ 9,99 a R$ 19,99.</div>
      <div class="abs" style="left:80px;top:640px;width:860px;font-size:46px;line-height:1.3;color:var(--muted)">Menos que errar a compra. Raquete de tênis, prancha de surf e tênis de corrida.</div>
      <div class="abs" style="left:80px;top:1060px">{logo('sportdna-logo-fundo-escuro', 760)}</div>
      <div class="abs m" style="left:80px;top:1200px;font-size:32px">sportdna.com.br</div>'''))
    piece(id='D-C2', fmt='carrossel', day=5, slot='12h30', title='Como o motor escolhe (produto)', kind='produto', w=1080, h=1350,
          html=doc('D-C2', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Nenhuma marca paga para aparecer. ⚙️ Como a SPORT DNA escolhe o seu equipamento:\n\n'
                   '01 Você responde: corpo, nível, estilo. Grátis e sem cadastro.\n'
                   '02 O motor cruza com as fichas técnicas: 62 raquetes, 13 tipos de prancha, 212 tênis.\n'
                   '03 E com casos reais: 422 casos calibram o SURF DNA.\n'
                   '04 Você recebe o finalista com DNA Score e o porquê de cada escolha.\n\n'
                   'Teste grátis. Relatório de R$ 9,99 a R$ 19,99. Link na bio.\n'
                   '#sportdna #tenis #surf #corrida #equipamentoesportivo'),
          notes='Peça de produto 2 de 2. Números do site no ar (62 raquetes, 212 tênis, 13 tipos, 422 casos; preços R$ 9,99–19,99).')

# =====================================================================================
# D-R3 · Reel · Três esportes, um DNA (marca-mãe)
# =====================================================================================
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

def d_r3():
    T = 16.6
    tl = TL(T)
    arcs = ''.join(f'@keyframes arc{k}{{from{{stroke-dasharray:0 172.729}}to{{stroke-dasharray:40.782 131.947}}}}' for k in range(3))
    s1 = f'''<div {tl.scene(0, 2.8, fin=False)}>
      <div class="abs t" style="left:90px;top:440px;width:900px;font-size:140px;{at(.1,'rise', .6)}">Equipamento não é tamanho único.</div>
    </div>'''
    sports = [('RACKET', 'Seu braço.', 'var(--racket)', 'racketdna-icone', 'peso · balanço · rigidez · cordas'),
              ('SURF', 'Seu mar.', 'var(--surf)', 'surfdna-icone', 'litragem · medidas · rabeta · quilhas'),
              ('RUN', 'Seu ritmo.', 'var(--run)', 'rundna-icone', 'amortecimento · drop · custo por km')]
    sc = ''
    t = 2.8
    for nome, frase, cor, ic, spec in sports:
        sc += f'''<div {tl.scene(t, t + 2.6, fade=.08)} >
          <div class="abs" style="inset:0;background:{cor}"></div>
          <div class="abs" style="left:90px;top:360px;{at(t + .05,'pop', .5)}">{logo(ic, 200)}</div>
          <div class="abs t" style="left:90px;top:640px;width:900px;font-size:170px;color:var(--ink);{at(t + .15,'rise', .5)}">{frase}</div>
          <div class="abs m" style="left:90px;top:900px;font-size:36px;color:var(--ink);{at(t + .5,'fade')}">{nome} DNA · {spec}</div>
        </div>'''
        t += 2.6
    s5 = f'''<div {tl.scene(t, t + 3.2)}>
      <div class="abs" style="left:340px;top:380px">{simbolo_animado(400, t + .1)}</div>
      <div class="abs t" style="left:0;right:0;top:880px;text-align:center;font-size:80px;{at(t + 1.2,'rise', .6)}">Um DNA. O seu.</div>
    </div>'''
    t += 3.2
    s6 = f'''<div {tl.scene(t, T, fout=False)}>
      <div class="abs" style="left:110px;top:520px;{at(t + .05,'fade', .6)}">{logo('sportdna-logo-fundo-escuro', 860)}</div>
      <div class="abs" style="left:110px;top:720px;width:860px;font-size:48px;line-height:1.3;{at(t + .5,'rise', .6)}">O equipamento certo para o seu jeito de jogar, surfar e correr.</div>
      <div class="abs m" style="left:110px;top:940px;font-size:34px;color:var(--muted);{at(t + .9,'fade')}">Teste grátis · sportdna.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{sc}{s5}{s6}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:130px">Equipamento não é tamanho único.</div>
      <div class="abs" style="left:80px;top:760px;width:920px;display:flex;gap:20px">
        <div style="flex:1;height:420px;background:var(--racket);border-radius:30px;padding:30px">{logo('racketdna-icone', 110)}<div class="t" style="font-size:48px;color:var(--ink);margin-top:150px">Seu braço.</div></div>
        <div style="flex:1;height:420px;background:var(--surf);border-radius:30px;padding:30px">{logo('surfdna-icone', 110)}<div class="t" style="font-size:48px;color:var(--ink);margin-top:150px">Seu mar.</div></div>
        <div style="flex:1;height:420px;background:var(--run);border-radius:30px;padding:30px">{logo('rundna-icone', 110)}<div class="t" style="font-size:48px;color:var(--ink);margin-top:150px">Seu ritmo.</div></div></div></div>'''
    piece(id='D-R3', fmt='reel', day=7, slot='19h45', title='Três esportes, um DNA (marca)', total=T, poster=.82,
          html=doc('D-R3', FONTS, CSS + tl.style() + arcs, body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--ink)'),
          caption=('Equipamento não é tamanho único. 🧬\n\n'
                   'Raquete: o seu braço. Prancha: o seu mar. Tênis de corrida: o seu ritmo.\n'
                   'A SPORT DNA cruza o seu jeito com a ficha técnica de cada equipamento e mostra o porquê de cada escolha. Nenhuma marca paga para aparecer.\n\n'
                   'Teste grátis, link na bio.\n#sportdna #racketdna #surfdna #rundna #tenis #surf #corrida'),
          notes='Assinatura animada oficial: os 3 arcos do símbolo se desenham em sequência; o S fica parado. Troca de esporte com corte seco.')

# =====================================================================================
# Stories
# =====================================================================================
def story(body, cls='', bg=''):
    return f'<section class="page {cls}" style="width:1080px;height:1920px;{bg}">{body}</section>'

def d_stories():
    S = []
    S.append(('D-S1', 1, 'Enquete: já comprou equipamento errado?', story(f'''
      <div class="abs lbl" style="left:80px;top:290px">PERGUNTA RÁPIDA</div>
      <div class="abs t" style="left:80px;top:350px;width:920px;font-size:120px">Você já comprou equipamento errado?</div>
      <div class="abs" style="left:80px;top:1440px;display:flex;gap:18px">{logo('racketdna-icone', 96)}{logo('surfdna-icone', 96)}{logo('rundna-icone', 96)}</div>'''),
      'Adesivo de ENQUETE em y≈950–1250: "Sim, já errei" / "Acertei de primeira".', 'Mesma enquete do lançamento, agora com resultado comentado no story seguinte.'))
    S.append(('D-S2', 2, 'Quiz: qual número é a rigidez?', story(f'''
      <div class="abs" style="inset:0;background:var(--racket)"></div>
      <div class="abs lbl" style="left:80px;top:290px;color:var(--ink)">RACKET DNA · QUIZ</div>
      <div class="abs t" style="left:80px;top:350px;width:920px;font-size:104px;color:var(--ink)">Na ficha da raquete, qual número fala da rigidez?</div>
      <div class="abs" style="left:80px;top:1400px">{logo('racketdna-logo-preto', 640)}</div>'''),
      'Adesivo QUIZ em y≈880–1300: 295 g / 100 pol² / 61 RA (correta) / 16×19.', 'v2: saiu o desenho da raquete; entrou o logo oficial do RACKET DNA.'))
    S.append(('D-S3', 3, 'Enquete: pediu dica de prancha pra IA?', story(f'''
      <div class="abs" style="left:80px;top:280px;width:920px;background:var(--surface);border-radius:40px;padding:34px 34px 40px">
        <div class="lbl" style="margin-bottom:26px">ASSISTENTE DE IA · SIMULAÇÃO</div>
        {chat_user('qual prancha de surf eu devo comprar?')}
        <div style="margin-top:34px">{chat_ia('Uma boa opção para começar é uma prancha de 7 pés, com bastante volume!')}</div></div>
      <div class="abs t" style="left:80px;top:880px;width:920px;font-size:100px">Parece simples. <span style="color:var(--surf)">Não é.</span></div>
      <div class="abs" style="left:80px;top:1100px;width:900px;font-size:44px;line-height:1.3;color:var(--muted)">Faltou o seu peso, o seu nível e o seu mar.</div>'''),
      'Adesivo de ENQUETE em y≈1260–1520: "Já pedi dica pra IA" / "Nunca pedi".', 'v2 (você reprovou a caixa de perguntas). Nova linha: simulação de IA genérica, junto com o reel D-R1.'))
    S.append(('D-S4', 5, 'A IA disse: bom amortecimento', story(f'''
      <div class="abs" style="inset:0;background:var(--run)"></div>
      <div class="abs lbl" style="left:80px;top:290px;color:var(--ink)">A IA DISSE · SIMULAÇÃO</div>
      <div class="abs t" style="left:80px;top:350px;width:920px;font-size:104px;color:var(--ink)">"Escolha um tênis com bom amortecimento."</div>
      <div class="abs t" style="left:80px;top:780px;font-size:150px;color:var(--ink);text-decoration:line-through;text-decoration-thickness:12px">Todos têm.</div>
      <div class="abs" style="left:80px;top:1000px;width:900px;font-size:46px;line-height:1.3;color:var(--ink)">O RUN DNA compara 212 tênis com o seu corpo, o seu ritmo e as suas dores. Calibrado com atletas e corredores.</div>'''),
      'Adesivo de LINK (sportdna.com.br) em y≈1300–1500.', 'v2 (você reprovou a caixa de perguntas). Nova linha: o que a IA genérica responde e o que falta.'))
    S.append(('D-S5', 6, 'Link: teste grátis', story(f'''
      <div class="abs" style="left:80px;top:290px">{logo('sportdna-simbolo-cor', 160)}</div>
      <div class="abs t" style="left:80px;top:520px;width:920px;font-size:130px">Teste grátis e sem cadastro.</div>
      <div class="abs" style="left:80px;top:900px;width:900px;font-size:46px;line-height:1.3;color:var(--muted)">Raquete, prancha ou tênis de corrida. O relatório só se você quiser.</div>'''),
      'Adesivo de LINK (sportdna.com.br) em y≈1200–1400.', 'Fecha a semana.'))
    for sid, day, title, body, sticker, notes in S:
        piece(id=sid, fmt='story', day=day, title=title, w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker=sticker, notes=notes, kind='story')

d_r1(); d_c1(); d_r2(); d_c2(); d_r3(); d_stories()
CTA = {
    'D-S1': ('enquete', 930, ['Sim, já errei', 'Acertei de primeira'], 'Responde no direct.'),
    'D-S2': ('quiz', 860, ['295 g', '100 pol²', '61 RA', '16×19'], 'Manda o seu chute no direct.'),
    'D-S3': ('enquete', 1240, ['Já pedi dica pra IA', 'Nunca pedi'], 'Responde no direct.'),
    'D-S4': ('link', 1320, None, 'Link na bio · sportdna.com.br'),
    'D-S5': ('link', 1220, None, 'Link na bio · sportdna.com.br'),
}
def _st(i):
    dark = i in ('D-S1', 'D-S3', 'D-S5')
    return {'bgs': ['#1A1A1A'] if dark else ['#0A0A0A'], 'fg': '#fff', 'tfont': 'Archivo', 'bfont': "'DM Sans'", 'border': '2px solid #2E2E2C' if dark else '0',
            'radius': '24px', 'shadow': 'none', 'txt_color': '#A3A3A0' if dark else '#0A0A0A', 'fs': 46, 'ts_big': 44}
C.apply_ctas(CTA, _st)
