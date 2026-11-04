"""SPORT DNA · Pack Semanal 02. Archivo ExtraBold / DM Sans / JetBrains Mono; Syne só em números de destaque e logos.
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

# =====================================================================================
# D-C3 · Carrossel · Black Friday: 4 perguntas antes de comprar (seg, claro)
# =====================================================================================
def d_c3():
    pages = [page(f'''
      <div class="abs lbl" style="left:80px;top:90px">ANTES DA BLACK FRIDAY · 27/11</div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:124px">Desconto bom em equipamento errado continua caro.</div>
      <div class="abs" style="left:80px;top:860px;width:820px;font-size:46px;line-height:1.3;color:var(--mutedL)">4 perguntas antes de comprar raquete, prancha ou tênis de corrida.</div>
      <div class="abs" style="left:80px;top:1120px;display:flex;gap:18px">{logo('racketdna-icone', 100)}{logo('surfdna-icone', 100)}{logo('rundna-icone', 100)}</div>''', cls='light')]
    qs = [('01', 'O que você usa hoje te incomoda?', 'Dor no braço, prancha que não rema, tênis que machuca. O incômodo diz o que trocar.', 'var(--racket)'),
          ('02', 'Qual é o seu nível de verdade?', 'Não o que você quer ter em dezembro. O de hoje.', 'var(--surf)'),
          ('03', 'O desconto é no modelo certo para o seu corpo?', 'Preço baixo não muda peso, volume nem amortecimento.', 'var(--run)'),
          ('04', 'Quanto custa por uso?', 'Um tênis que dura mais pode sair mais barato por quilômetro.', '#fff')]
    for i, (n, q, a, c) in enumerate(qs):
        light = i % 2 == 1
        pages.append(page(f'''
          <div class="abs n" style="left:70px;top:90px;font-size:200px;color:{c if not light else 'var(--ink)'}">{n}</div>
          <div class="abs t" style="left:80px;top:380px;width:920px;font-size:96px">{q}</div>
          <div class="abs" style="left:80px;top:820px;width:860px;font-size:50px;line-height:1.3;color:{'var(--mutedL)' if light else 'var(--muted)'}">{a}</div>''', cls='light' if light else ''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:110px">Faça o teste antes do carrinho.</div>
      <div class="abs" style="left:80px;top:520px;width:860px;font-size:48px;line-height:1.3;color:var(--muted)">Grátis e sem cadastro. O SPORT DNA cruza o seu jeito com a ficha técnica de cada equipamento. Nenhuma marca paga para aparecer.</div>
      <div class="abs" style="left:80px;top:900px;font-size:42px">Manda pro amigo que já está com o carrinho cheio.</div>
      <div class="abs" style="left:80px;top:1090px">{logo('sportdna-logo-fundo-escuro', 700)}</div>
      <div class="abs m" style="left:80px;top:1230px;font-size:32px">sportdna.com.br</div>'''))
    piece(id='D-C3', fmt='carrossel', day=1, slot='12h30', title='Black Friday: 4 perguntas antes de comprar', w=1080, h=1350,
          html=doc('D-C3', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Desconto bom em equipamento errado continua caro. 🏷️\n\n'
                   'Antes da Black Friday (27/11), 4 perguntas:\n01 O que você usa hoje te incomoda?\n02 Qual é o seu nível de verdade?\n03 O desconto é no modelo certo para o seu corpo?\n04 Quanto custa por uso?\n\n'
                   'Salva e manda pro amigo que já está com o carrinho cheio 👇\n'
                   'Teste grátis e sem cadastro. Link na bio.\n#sportdna #blackfriday #tenis #surf #corrida #equipamentoesportivo'),
          notes='Utilidade com o gancho da Black Friday (27/11). Capa off-white depois do preto do D-R3. Sem número novo.')

# =====================================================================================
# D-R4 · Reel · RUN: 3 corredores, a mesma pergunta, a mesma resposta (ter, preto)
# =====================================================================================
def d_r4():
    T = 19.0
    tl = TL(T)
    perfis = [('52 kg · começando', 'var(--run)'), ('90 kg · treina para maratona', 'var(--surf)'), ('dor no joelho · 3× por semana', 'var(--racket)')]
    resposta = 'Escolha um tênis com bom amortecimento e conforto.'
    s1 = f'''<div {tl.scene(0, 2.8, fin=False)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:110px;{at(.05,'rise', .6)}">3 corredores. A mesma pergunta pra IA.</div>
    </div>'''
    cards = ''
    for i, (p, c) in enumerate(perfis):
        t0 = 2.9 + i * 1.9
        cards += f'''<div style="background:var(--surface);border-radius:34px;padding:28px 32px;margin-bottom:26px;{at(t0,'rise', .4)}">
          <div class="lbl" style="color:{c}">CORREDOR {i+1} · {p}</div>
          <div style="margin-top:16px">{chat_user('qual tênis de corrida eu compro?', 'margin-bottom:16px')}</div>
          <div style="{at(t0 + .8,'fade', .3)}">{chat_ia(resposta)}</div></div>'''
    s2 = f'''<div {tl.scene(2.8, 9.6)}>
      <div class="abs" style="left:90px;top:300px;width:900px">{sim_tag()}{cards}</div>
    </div>'''
    s3 = f'''<div {tl.scene(9.6, 12.4, fade=.1)}>
      <div class="abs t" style="left:90px;top:440px;width:900px;font-size:116px;{at(9.65,'rise', .5)}">Três corpos. Uma resposta.</div>
      <div class="abs t" style="left:90px;top:760px;width:900px;font-size:110px;{at(10.4,'rise', .5)}">Parece simples.</div>
      <div class="abs t" style="left:90px;top:900px;width:900px;font-size:150px;color:var(--run);{at(11.0,'pop', .4)}">Não é.</div>
    </div>'''
    s4 = f'''<div {tl.scene(12.4, 16.2, fade=.1)}>
      <div class="abs t" style="left:90px;top:380px;width:900px;font-size:88px;{at(12.45,'rise', .5)}">O RUN DNA foi calibrado com atletas e corredores.</div>
      <div class="abs" style="left:90px;top:800px;width:880px;font-size:50px;line-height:1.3;color:var(--muted);{at(13.2,'fade', .5)}">Compara 212 tênis com o seu corpo, o seu ritmo e as suas dores.</div>
    </div>'''
    s5 = f'''<div {tl.scene(16.2, T, fout=False)}>
      <div class="abs" style="left:90px;top:620px;{at(16.25,'fade', .6)}">{logo('rundna-logo-fundo-escuro', 800)}</div>
      {cta_final(16.7)}
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}{s5}</section>'
    mini_cards = ''.join(f'<div style="flex:1;background:var(--surface);border-radius:28px;padding:24px;height:400px"><div class="lbl" style="color:{c};font-size:22px">CORREDOR {i+1}</div><div style="font-size:30px;margin-top:12px;color:var(--muted)">{p}</div><div class="t" style="font-size:32px;margin-top:40px">"bom amortecimento e conforto"</div></div>' for i, (p, c) in enumerate(perfis))
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:110px;width:920px;font-size:104px">3 corredores. A mesma pergunta pra IA.</div>
      <div class="abs" style="left:80px;top:520px;width:920px;display:flex;gap:20px">{mini_cards}</div>
      <div class="abs lbl" style="left:80px;top:950px">SIMULAÇÃO · ASSISTENTE DE IA GENÉRICO</div>
      <div class="abs t" style="left:80px;top:1040px;font-size:76px;color:var(--run)">Parece simples. Não é.</div></div>'''
    piece(id='D-R4', fmt='reel', day=2, slot='19h45', title='RUN: 3 corredores, a mesma resposta da IA', total=T, poster=.4,
          html=doc('D-R4', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--ink)'),
          caption=('3 corredores. A mesma pergunta pra IA. A mesma resposta: "bom amortecimento e conforto". 🏃\n\n'
                   'Um tem 52 kg e está começando. Outro tem 90 kg e treina para maratona. O terceiro sente o joelho.\n'
                   'Parece simples. Não é.\n\n'
                   'O RUN DNA foi calibrado com atletas e corredores e compara 212 tênis com o seu corpo, o seu ritmo e as suas dores.\n'
                   'Manda pro seu parceiro de treino 👇\nTeste grátis e sem cadastro. Link na bio.\n#rundna #sportdna #corrida #corridaderua #tenisdecorrida #ia'),
          notes='Linha "simulação de IA" pedida pelo Gui, com gancho novo (três perfis, uma resposta). IA genérica, sem marca, com etiqueta de simulação. 212 tênis: número do site.')

# =====================================================================================
# D-C4 · Carrossel · SURF: qual prancha para cada mar (qua, azul surf)
# =====================================================================================
def d_c4():
    tipos = [('Longboard', 'Acima de 9 pés.', 'Onda pequena e fraca. Remada fácil e manobra no bico.'),
             ('Funboard', 'Entre 7 e 8 pés.', 'A ponte de quem está saindo da escolinha.'),
             ('Fish', 'Curta, larga, rabeta andorinha.', 'Onda pequena e sem força. Velocidade onde não tem.'),
             ('Shortboard', 'Fina e com pouco volume.', 'Onda com força e surfista com experiência.'),
             ('Gun', 'Longa e estreita.', 'Feita para onda grande. Não é a sua primeira.')]
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--surf)"></div>
      <div class="abs lbl" style="left:80px;top:90px;color:var(--ink)">SURF DNA · GUIA RÁPIDO</div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:136px;color:var(--ink)">Uma prancha para cada mar.</div>
      <div class="abs" style="left:80px;top:720px;width:820px;font-size:48px;line-height:1.3;color:var(--ink)">5 tipos, do longboard à gun. Salva para a próxima trip.</div>
      <div class="abs" style="left:80px;top:1100px">{logo('surfdna-logo-preto', 560)}</div>''')]
    for i, (n, med, uso) in enumerate(tipos):
        light = i % 2 == 0
        pages.append(page(f'''
          <div class="abs lbl" style="left:80px;top:90px;{'color:var(--ink)' if False else ''}">{i+1} DE 5</div>
          <div class="abs t" style="left:80px;top:200px;width:920px;font-size:160px;color:{'var(--ink)' if light else 'var(--surf)'}">{n}</div>
          <div class="abs m" style="left:80px;top:440px;font-size:40px;color:{'var(--petrol)' if light else 'var(--surf)'}">{med}</div>
          <div class="abs" style="left:80px;top:560px;width:880px;font-size:62px;line-height:1.2;font-family:Archivo;font-weight:800">{uso}</div>
          <div class="abs" style="left:80px;top:1150px;width:920px;height:6px;background:{'var(--lineL)' if light else 'var(--line)'}"><div style="width:{(i+1)*20}%;height:6px;background:var(--surf)"></div></div>''', cls='light' if light else ''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:100px">Não sabe qual é a sua?</div>
      <div class="abs" style="left:80px;top:440px;width:860px;font-size:48px;line-height:1.3;color:var(--muted)">O SURF DNA olha 13 tipos de prancha com o seu peso, o seu nível e o seu mar.</div>
      <div class="abs" style="left:80px;top:820px;font-size:42px">Manda pro amigo da trip.</div>
      <div class="abs" style="left:80px;top:1060px">{logo('surfdna-logo-fundo-escuro', 640)}</div>
      <div class="abs m" style="left:80px;top:1230px;font-size:32px">Teste grátis · sportdna.com.br</div>'''))
    piece(id='D-C4', fmt='carrossel', day=3, slot='12h30', title='SURF: uma prancha para cada mar', w=1080, h=1350,
          html=doc('D-C4', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Uma prancha para cada mar. 🌊\n\n'
                   'Longboard: acima de 9 pés, para onda pequena e fraca.\nFunboard: entre 7 e 8 pés, a ponte de quem sai da escolinha.\nFish: curta e larga, para onda sem força.\nShortboard: fina, para onda com força.\nGun: longa e estreita, para onda grande.\n\n'
                   'Salva para a próxima trip e manda pro amigo do surf 👇\n'
                   'O SURF DNA olha 13 tipos de prancha com o seu peso, nível e mar. Teste grátis, link na bio.\n#surfdna #sportdna #surf #pranchadesurf #surfbrasil'),
          notes='Guia editorial. Medidas são faixas gerais de mercado, sem marca. 13 tipos: número do site. Capa azul SURF entre o preto de terça e o de quinta.')

# =====================================================================================
# D-R5 · Reel meme · RACKET: POV, comprei a raquete "profissional" (qui, preto)
# =====================================================================================
def d_r5():
    T = 14.0
    tl = TL(T)
    s1 = f'''<div {tl.scene(0, 3.6, fin=False)}>
      <div class="abs t" style="left:90px;top:400px;width:900px;font-size:100px;{at(.05,'rise', .6)}">POV: você comprou a raquete mais pesada da loja porque "é a dos profissionais".</div>
    </div>'''
    sem = [('SEMANA 1', '"Que pancada."', '#fff'), ('SEMANA 2', '"Por que o braço cansa no 2º set?"', 'var(--muted)'), ('SEMANA 3', 'O cotovelo pediu pra conversar.', 'var(--racket)')]
    rows = ''.join(f'<div style="padding:34px 0;border-top:2px solid var(--line);{at(3.8 + i*1.4,"rise", .45)}"><div class="lbl" style="color:var(--racket)">{a}</div><div class="t" style="font-size:72px;margin-top:14px;color:{c}">{b}</div></div>' for i, (a, b, c) in enumerate(sem))
    s2 = f'''<div {tl.scene(3.6, 8.6)}>
      <div class="abs" style="left:90px;top:360px;width:900px">{rows}</div>
    </div>'''
    s3 = f'''<div {tl.scene(8.6, 11.4, fade=.1)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:104px;{at(8.65,'rise', .5)}">Raquete boa é a que combina com o <span style="color:var(--racket)">seu braço.</span></div>
      <div class="abs" style="left:90px;top:900px;width:880px;font-size:48px;line-height:1.3;color:var(--muted);{at(9.5,'fade', .5)}">O RACKET DNA cruza o seu jogo com 62 raquetes medidas.</div>
    </div>'''
    s4 = f'''<div {tl.scene(11.4, T, fout=False)}>
      <div class="abs" style="left:90px;top:620px;{at(11.45,'fade', .6)}">{logo('racketdna-logo-fundo-escuro', 900)}</div>
      {cta_final(11.9)}
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:110px;width:920px;font-size:92px">POV: você comprou a raquete mais pesada da loja porque "é a dos profissionais".</div>
      <div class="abs" style="left:80px;top:720px;width:920px">{''.join(f'<div style="padding:22px 0;border-top:2px solid var(--line)"><span class="lbl" style="color:var(--racket)">{a}</span><span class="t" style="font-size:52px;margin-left:24px;color:{c}">{b}</span></div>' for a, b, c in sem)}</div></div>'''
    piece(id='D-R5', fmt='reel', day=4, slot='19h45', title='Meme POV: a raquete "dos profissionais"', total=T, poster=.45, kind='meme',
          html=doc('D-R5', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--ink)'),
          caption=('POV: você comprou a raquete mais pesada da loja porque "é a dos profissionais". 🎾\n\n'
                   'Semana 1: "que pancada".\nSemana 2: o braço cansa no 2º set.\nSemana 3: o cotovelo pediu pra conversar.\n\n'
                   'Raquete boa é a que combina com o seu braço. O RACKET DNA cruza o seu jogo com 62 raquetes medidas.\n'
                   'Marca o seu parceiro de quadra que precisa ver isso 👇\nTeste grátis, link na bio.\n#racketdna #sportdna #tenis #beachtennis #raquete #meme'),
          notes='Meme POV, ironia com dado (linha da marca). Sem desenho de raquete (o Gui reprovou o ícone desenhado). Áudio em alta no app.')

# =====================================================================================
# D-C5 · Carrossel · RUN: 5 sinais de que o tênis já deu (sex 20/11, claro)
# =====================================================================================
def d_c5():
    sinais = [('A entressola tem vincos fundos.', 'Aquelas rugas na espuma do meio são amortecimento que já foi.'),
              ('A sola está lisa em alguns pontos.', 'Olhe embaixo, na ponta e no calcanhar.'),
              ('Apoiado na mesa, ele tomba.', 'Desgaste de um lado só deixa o tênis torto.'),
              ('Você sente mais o impacto.', 'Se o mesmo treino começou a pesar no corpo, desconfie do tênis.'),
              ('Já passou dos 500 a 800 km.', 'É a faixa em que a maioria dos tênis de corrida pede troca.')]
    pages = [page(f'''
      <div class="abs lbl" style="left:80px;top:90px">RUN DNA · LONGÃO DO FERIADO</div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:132px">5 sinais de que o seu tênis já <span style="color:var(--run)">deu.</span></div>
      <div class="abs" style="left:80px;top:820px;width:820px;font-size:46px;line-height:1.3;color:var(--mutedL)">Confere antes do longão de feriado.</div>
      <div class="abs" style="left:80px;top:1100px">{logo('rundna-logo-fundo-claro', 560)}</div>''', cls='light')]
    for i, (t, s) in enumerate(sinais):
        dark = i % 2 == 0
        pages.append(page(f'''
          <div class="abs n" style="left:70px;top:90px;font-size:260px;color:var(--run)">{i+1}</div>
          <div class="abs t" style="left:80px;top:440px;width:920px;font-size:100px">{t}</div>
          <div class="abs" style="left:80px;top:860px;width:860px;font-size:50px;line-height:1.3;color:{'var(--muted)' if dark else 'var(--mutedL)'}">{s}</div>''', cls='' if dark else 'light'))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--run)"></div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:104px;color:var(--ink)">Quando trocar? O RUN DNA mostra o mês certo.</div>
      <div class="abs" style="left:80px;top:560px;width:860px;font-size:48px;line-height:1.3;color:var(--ink)">E o custo por km de cada finalista, entre 212 tênis. Relatório R$ 9,99.</div>
      <div class="abs" style="left:80px;top:860px;font-size:42px;color:var(--ink)">Manda pro grupo da corrida.</div>
      <div class="abs" style="left:80px;top:1080px">{logo('rundna-logo-preto', 560)}</div>
      <div class="abs m" style="left:80px;top:1230px;font-size:32px;color:var(--ink)">sportdna.com.br</div>'''))
    piece(id='D-C5', fmt='carrossel', day=5, slot='12h30', title='RUN: 5 sinais de que o tênis já deu', w=1080, h=1350,
          html=doc('D-C5', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('5 sinais de que o seu tênis de corrida já deu. 👟\n\n'
                   '1. A entressola tem vincos fundos.\n2. A sola está lisa em alguns pontos.\n3. Apoiado na mesa, ele tomba.\n4. Você sente mais o impacto.\n5. Já passou dos 500 a 800 km.\n\n'
                   'Confere antes do longão do feriado e manda pro grupo da corrida 👇\n'
                   'O RUN DNA mostra o mês certo de trocar e o custo por km entre 212 tênis. Link na bio.\n#rundna #sportdna #corrida #corridaderua #tenisdecorrida #feriado'),
          notes='Utilidade (salvar e mandar no grupo de corrida). 500–800 km é a faixa geral de troca citada no mercado; sem marca. Capa off-white entre pretos.')

# =====================================================================================
# D-R6 · Reel · Black Friday: teste antes de comprar (sáb, preto)
# =====================================================================================
def d_r6():
    T = 15.0
    tl = TL(T)
    s1 = f'''<div {tl.scene(0, 3.2, fin=False)}>
      <div class="abs lbl" style="left:90px;top:330px">BLACK FRIDAY · 27/11</div>
      <div class="abs n" style="left:80px;top:420px;font-size:220px;{at(.05,'pop', .5)}">6 dias.</div>
      <div class="abs t" style="left:90px;top:760px;width:900px;font-size:88px;{at(.6,'rise', .5)}">E o carrinho já está cheio.</div>
    </div>'''
    sports = [('var(--racket)', 'racketdna-icone', 'Raquete leve demais pro seu jogo?'), ('var(--surf)', 'surfdna-icone', 'Prancha com pouco volume pro seu nível?'), ('var(--run)', 'rundna-icone', 'Tênis que não combina com a sua pisada?')]
    sc = ''
    t = 3.2
    for cor, ic, txt in sports:
        sc += f'''<div {tl.scene(t, t + 2.2, fade=.06)}>
          <div class="abs" style="inset:0;background:{cor}"></div>
          <div class="abs" style="left:90px;top:360px;{at(t + .05,'pop', .4)}">{logo(ic, 180)}</div>
          <div class="abs t" style="left:90px;top:640px;width:900px;font-size:116px;color:var(--ink);{at(t + .15,'rise', .4)}">{txt}</div>
          <div class="abs t" style="left:90px;top:1180px;font-size:80px;color:var(--ink);{at(t + 1.0,'fade', .2)}">−30% continua errado.</div>
        </div>'''
        t += 2.2
    s3 = f'''<div {tl.scene(t, t + 2.6, fade=.1)}>
      <div class="abs t" style="left:90px;top:440px;width:900px;font-size:110px;{at(t + .05,'rise', .5)}">Desconto em equipamento errado não é economia.</div>
    </div>'''
    t += 2.6
    s4 = f'''<div {tl.scene(t, T, fout=False)}>
      <div class="abs" style="left:110px;top:520px;{at(t + .05,'fade', .6)}">{logo('sportdna-logo-fundo-escuro', 860)}</div>
      <div class="abs" style="left:110px;top:720px;width:860px;font-size:50px;line-height:1.3;{at(t + .4,'rise', .5)}">Teste grátis e sem cadastro antes de comprar.</div>
      <div class="abs m" style="left:110px;top:900px;font-size:34px;color:var(--muted);{at(t + .8,'fade')}">Relatório de R$ 9,99 a R$ 19,99 · sportdna.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{sc}{s3}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs lbl" style="left:80px;top:100px">BLACK FRIDAY · 27/11</div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:118px">Desconto em equipamento errado não é economia.</div>
      <div class="abs" style="left:80px;top:860px;width:920px;display:flex;gap:20px">
        {''.join(f'<div style="flex:1;height:300px;background:{c};border-radius:30px;padding:30px">{logo(i, 110)}</div>' for c, i, _ in sports)}</div></div>'''
    piece(id='D-R6', fmt='reel', day=6, slot='19h45', title='Black Friday: desconto em equipamento errado', total=T, poster=.3, kind='trend',
          html=doc('D-R6', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--ink)'),
          caption=('Desconto em equipamento errado não é economia. 🛒\n\n'
                   'Faltam 6 dias para a Black Friday (27/11). Antes de fechar o carrinho:\n'
                   'raquete leve demais pro seu jogo? Prancha com pouco volume pro seu nível? Tênis que não combina com a sua pisada?\n\n'
                   'Teste grátis e sem cadastro. Relatório de R$ 9,99 a R$ 19,99. Link na bio.\n'
                   'Manda pro amigo do carrinho cheio 👇\n#sportdna #blackfriday #tenis #surf #corrida'),
          notes='Assunto da semana (Black Friday 27/11). "−30%" é ilustrativo, não é oferta. Preços do site.')

# =====================================================================================
# D-C6 · Carrossel produto · Por que o teste pergunta o que pergunta (dom, lima RACKET)
# =====================================================================================
def d_c6():
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--racket)"></div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:132px;color:var(--ink)">Por que o teste pergunta o que pergunta.</div>
      <div class="abs" style="left:80px;top:800px;width:820px;font-size:48px;line-height:1.3;color:var(--ink)">Calibrado com atletas e esportistas. Testado em vários perfis antes de ir ao ar.</div>
      <div class="abs" style="left:80px;top:1120px">{logo('sportdna-logo-preto', 600)}</div>''')]
    blocos = [('RACKET DNA', 'var(--racket)', 'racketdna-icone', [('Seu braço', 'Já sentiu o cotovelo? Peso e rigidez mudam tudo.'), ('Seu jogo', 'Bate chapado ou com spin?'), ('Seu nível', 'Há quanto tempo joga?')], '62 raquetes'),
              ('SURF DNA', 'var(--surf)', 'surfdna-icone', [('Seu peso', 'Define o volume que te faz remar.'), ('Seu nível', 'Muda o tipo de prancha.'), ('Seu mar', 'Onda fraca e onda forte pedem pranchas diferentes.')], '13 tipos de prancha'),
              ('RUN DNA', 'var(--run)', 'rundna-icone', [('Seu corpo', 'Peso e pisada pedem amortecimento diferente.'), ('Seu ritmo', 'Treino leve ou prova?'), ('Suas dores', 'Onde dói diz o que evitar.')], '212 tênis')]
    for i, (nome, cor, ic, qs, num) in enumerate(blocos):
        lst = ''.join(f'<div style="padding:30px 0;border-top:2px solid var(--line)"><div class="t" style="font-size:64px;color:{cor}">{a}</div><div style="font-size:40px;margin-top:10px;line-height:1.3;color:var(--muted)">{b}</div></div>' for a, b in qs)
        pages.append(page(f'''
          <div class="abs" style="left:80px;top:90px;display:flex;align-items:center;gap:26px">{logo(ic, 110)}<span class="t" style="font-size:72px">{nome} pergunta</span></div>
          <div class="abs" style="left:80px;top:300px;width:920px">{lst}</div>
          <div class="abs m" style="left:80px;top:1220px;font-size:32px;color:{cor}">e cruza com {num}</div>'''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:110px">Parece simples. <span style="color:var(--racket)">Não é.</span></div>
      <div class="abs" style="left:80px;top:480px;width:860px;font-size:48px;line-height:1.3;color:var(--muted)">Por isso o teste pergunta. E por isso nenhuma marca paga para aparecer.</div>
      <div class="abs" style="left:80px;top:820px;font-size:42px">Manda pro amigo que vai trocar de equipamento.</div>
      <div class="abs" style="left:80px;top:1060px">{logo('sportdna-logo-fundo-escuro', 700)}</div>
      <div class="abs m" style="left:80px;top:1220px;font-size:32px">Teste grátis e sem cadastro · sportdna.com.br</div>'''))
    piece(id='D-C6', fmt='carrossel', day=7, slot='12h30', title='Produto: por que o teste pergunta o que pergunta', kind='produto', w=1080, h=1350,
          html=doc('D-C6', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Por que o teste pergunta o que pergunta. 🧬\n\n'
                   'RACKET DNA: seu braço, seu jogo e seu nível, cruzados com 62 raquetes.\n'
                   'SURF DNA: seu peso, seu nível e seu mar, cruzados com 13 tipos de prancha.\n'
                   'RUN DNA: seu corpo, seu ritmo e suas dores, cruzados com 212 tênis.\n\n'
                   'Calibrado com atletas e esportistas e testado em vários perfis antes de ir ao ar. Parece simples. Não é.\n'
                   'Manda pro amigo que vai trocar de equipamento 👇\nTeste grátis e sem cadastro. Link na bio.\n#sportdna #racketdna #surfdna #rundna #esporte'),
          notes='Peça de produto com a mensagem pedida pelo Gui (calibrado com atletas e esportistas). Números do site. Capa lima RACKET fecha a semana.')

# =====================================================================================
# Stories · Dicionário DNA (sem adesivo)
# =====================================================================================
TERMOS = [
    (1, 'RUN', 'Drop', 'A diferença de altura entre o calcanhar e a ponta do tênis, em milímetros.', 'var(--run)', 'rundna'),
    (2, 'RACKET', 'Balanço', 'Onde fica o peso da raquete: mais na cabeça ou mais no cabo.', 'var(--racket)', 'racketdna'),
    (3, 'SURF', 'Rabeta', 'A parte de trás da prancha. O formato muda a curva e a saída da onda.', 'var(--surf)', 'surfdna'),
    (4, 'RUN', 'Pronação', 'O movimento natural do pé de rolar para dentro quando pisa.', 'var(--run)', 'rundna'),
    (5, 'RACKET', '16×19', 'O padrão de cordas: 16 cordas na vertical e 19 na horizontal.', 'var(--racket)', 'racketdna'),
    (6, 'SURF', 'Quilhas', 'As barbatanas embaixo da prancha. Dão direção e firmeza na onda.', 'var(--surf)', 'surfdna'),
    (7, 'SURF', 'Rocker', 'A curva da prancha, do bico à rabeta, vista de lado.', 'var(--surf)', 'surfdna'),
]

def d_stories():
    for n, (d, sp, termo, defi, cor, lg) in enumerate(TERMOS):
        if d in (1, 3): continue  # v2 tangível (rodada 1 do S02): d_s6(), d_s8()
        light = n % 2 == 1
        body = f'''<section class="page {'light' if light else ''}" style="width:1080px;height:1920px">
          <div class="abs lbl" style="left:80px;top:300px">DICIONÁRIO DNA · {sp}</div>
          <div class="abs" style="left:80px;top:360px;width:920px;height:6px;background:{cor}"></div>
          <div class="abs t" style="left:80px;top:470px;width:920px;font-size:{200 if len(termo) < 8 else 170}px;{'color:' + cor if not light else ''}">{termo}</div>
          <div class="abs" style="left:80px;top:780px;width:900px;font-size:64px;line-height:1.25;font-family:Archivo;font-weight:800">{defi}</div>
          <div class="abs" style="left:80px;top:1300px;font-size:42px;{'color:var(--mutedL)' if light else 'color:var(--muted)'}">Salva e manda pro seu parceiro de treino.</div>
          <div class="abs" style="left:80px;top:1400px">{logo(lg + ('-logo-fundo-claro' if light else '-logo-fundo-escuro'), 460)}</div>
        </section>'''
        sid = f'D-S{5 + n + 1}'
        piece(id=sid, fmt='story', day=d, title=f'Dicionário DNA: {termo}', w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker='', kind='story',
              notes='Sem adesivo: glossário para salvar e mandar. Definição geral, sem marca.')


def d_s6():
    """v2: o relatório do RUN DNA na tela do celular (exemplo)."""
    row = lambda k, v, c='#0A0A0A': f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:20px 0;border-top:2px solid var(--lineL)"><span class="lbl" style="color:var(--mutedL)">{k}</span><span class="t" style="font-size:40px;color:{c}">{v}</span></div>'
    tela = f'''<div style="position:absolute;inset:0;background:var(--off);color:var(--ink);padding:24px 34px">
      <div style="display:flex;align-items:center;justify-content:space-between">{logo('rundna-logo-fundo-claro', 300)}<span class="lbl" style="color:var(--mutedL);font-size:20px">EXEMPLO</span></div>
      <div class="lbl" style="margin-top:34px;color:var(--mutedL)">SEU FINALISTA</div>
      <div class="t" style="font-size:58px;margin-top:8px">Tênis de treino diário</div>
      <div style="display:flex;align-items:flex-end;gap:20px;margin-top:20px"><span class="n" style="font-size:110px;color:var(--run)">92%</span><span class="t" style="font-size:34px;padding-bottom:12px">DNA Score</span></div>
      <div style="margin-top:10px">{row('CUSTO POR KM', 'R$ 0,95', 'var(--run)')}{row('DURABILIDADE', '700 km')}{row('TROCAR EM', 'set/2027')}</div>
      <div style="margin-top:20px;background:#fff;border-radius:24px;padding:22px 24px;font-size:28px;line-height:1.35">Por que ele: amortecimento alto para o seu peso e o seu volume de treino, sem pesar no ritmo.</div></div>'''
    body = f'''<section class="page" style="width:1080px;height:1920px">
      <div class="abs t" style="left:80px;top:270px;width:920px;font-size:84px">Assim é o relatório do <span style="color:var(--run)">RUN DNA.</span></div>
      <div class="abs" style="left:200px;top:470px">{C.phone(tela, 680, 1010, screen='#F4F4F2', frame='#1A1A1A', status_color='#0A0A0A', hora='07:10')}</div>
      <div class="abs m" style="left:80px;top:1475px;font-size:34px">Teste grátis · relatório R$ 9,99</div>
      <div class="abs lbl" style="left:80px;top:1530px">RELATÓRIO DE EXEMPLO · MODELO SEM MARCA</div>
    </section>'''
    piece(id='D-S6', fmt='story', day=1, title='O relatório do RUN DNA no celular (exemplo)', w=1080, h=1920, html=doc('D-S6', FONTS, CSS, body, 1080, 1920),
          caption='(story, sem legenda)', sticker='', kind='story',
          notes='v2 (você reprovou o glossário): tela do relatório num celular genérico. Exemplo marcado; custo por km e 700 km são o exemplo do site; modelo sem marca.')

def d_s8():
    """v2: do bloco de notas para a prancha certa (Gui: "mto basico")."""
    linhas = ['78 kg', 'surfo há 2 anos, fim de semana', 'praia de tombo, onda média', 'a minha atual afunda na remada', 'orçamento: até a Black Friday']
    notas = ''.join(f'<div style="display:flex;gap:18px;align-items:center;padding:18px 0;border-bottom:2px solid #EFE7C8"><span style="width:34px;height:34px;border:3px solid #B9A66A;border-radius:50%;flex:none"></span><span style="font:500 36px/1.3 \'DM Sans\'">{l}</span></div>' for l in linhas)
    tela = f'''<div style="position:absolute;inset:0;background:#FFFBEA;color:#2B2B28;padding:26px 36px">
      <div style="font:700 26px 'DM Sans';color:#B08A1E">‹ Notas</div>
      <div style="font:800 60px/1.1 Archivo;margin-top:26px">prancha nova??</div>
      <div style="font-size:24px;color:#8C8572;margin-top:8px">hoje, 06:52</div>
      <div style="margin-top:20px">{notas}</div></div>'''
    body = f'''<section class="page" style="width:1080px;height:1920px">
      <div class="abs t" style="left:80px;top:270px;width:920px;font-size:84px">Do bloco de notas pra prancha <span style="color:var(--surf)">certa.</span></div>
      <div class="abs" style="left:70px;top:470px">{C.phone(tela, 580, 960, screen='#FFFBEA', frame='#1A1A1A', status_color='#2B2B28', hora='06:52')}</div>
      <div class="abs" style="left:640px;top:1020px;width:380px;background:var(--surf);color:var(--ink);border-radius:30px;padding:30px 32px;box-shadow:0 30px 60px rgba(0,0,0,.4)">
        <div class="lbl" style="color:var(--ink)">SURF DNA · RESULTADO DE EXEMPLO</div>
        <div class="t" style="font-size:56px;margin-top:12px">Funboard</div>
        <div style="font-size:28px;margin-top:10px;line-height:1.3">Mais volume que a atual, para chegar antes na onda.</div></div>
      <div class="abs" style="left:80px;top:1480px;width:920px;font-size:32px;color:var(--muted)">Peso, nível e mar contra 13 tipos de prancha. Teste grátis.</div>
    </section>'''
    piece(id='D-S8', fmt='story', day=3, title='Do bloco de notas pra prancha certa', w=1080, h=1920, html=doc('D-S8', FONTS, CSS, body, 1080, 1920),
          caption='(story, sem legenda)', sticker='', kind='story',
          notes='v2 (seu comentário: "mto basico"): bloco de notas num celular genérico e o resultado do SURF DNA ao lado, marcado como exemplo. 13 tipos: número do site.')

d_c3(); d_r4(); d_c4(); d_r5(); d_c5(); d_r6(); d_c6(); d_stories(); d_s6(); d_s8()
