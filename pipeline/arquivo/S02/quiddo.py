"""Quiddo · Pack Semanal 02. Fraunces 900 + Nunito; creme/tinta/mata; contorno grosso e sombra dura.
Bichos, olho, símbolos e cortinas saem do código do site (assets/quiddo/art.json, gerado de src/lib)."""
import json, re
import common as C
from common import TL, at, doc, add

AQ = C.A / 'quiddo'
ART = json.loads((AQ / 'art.json').read_text())
INK = '#0E2A22'

FONTS = (C.font_face('Fraunces', 'Fraunces-900.woff2', '900') +
         C.font_face('Nunito', 'Nunito-var.woff2', '600 900'))

CSS = """
:root{--creme:#FFF6E6;--tinta:#0E2A22;--mata:#0B5D45;--verde:#13A07A;--amarelo:#FFC83D;--laranja:#FF7A1A;--azul:#1E7FD6;--vermelho:#E5383B;--ceu:#5BC0EB;--branco:#fff;--txt2:#4A5E56;
--ease-pop:cubic-bezier(.34,1.56,.64,1);--ease-rise:cubic-bezier(.2,.8,.2,1);--ease-grow:cubic-bezier(.2,.8,.2,1);--ease-slideL:cubic-bezier(.2,.8,.2,1);--ease-slideR:cubic-bezier(.2,.8,.2,1);--ease-fade:linear;--ease-drop:cubic-bezier(.3,1.3,.5,1)}
.page{background:var(--creme);color:var(--tinta);font-family:Nunito,sans-serif;font-weight:700}
.page.esc{background:var(--mata);color:var(--creme)}
.t{font-family:Fraunces,serif;font-weight:900;letter-spacing:-.02em;line-height:.98}
.mt{display:inline-block;background:var(--amarelo);color:var(--tinta);padding:0 .14em;margin:0 -.04em;transform:rotate(-2deg);border-radius:.08em}
.card{background:#fff;border:6px solid var(--tinta);border-radius:34px;box-shadow:0 12px 0 var(--tinta);color:var(--tinta)}
.chip{display:inline-flex;align-items:center;gap:12px;border:5px solid var(--tinta);border-radius:999px;padding:10px 26px;font-weight:900;font-size:30px;background:#fff;color:var(--tinta);box-shadow:0 6px 0 var(--tinta)}
.resp{display:flex;align-items:center;gap:22px;border:6px solid var(--tinta);border-radius:28px;box-shadow:0 10px 0 var(--tinta);padding:22px 28px;font-weight:900;font-size:40px;color:#fff}
.resp .sym{width:58px;height:58px;flex:none;color:#fff;--cut:transparent}
.resp.a{background:var(--verde)}.resp.b{background:var(--laranja)}.resp.c{background:var(--azul)}.resp.d{background:var(--vermelho)}
.resp .l{font-family:Fraunces;font-size:44px;opacity:.9;width:40px}
.av{display:block}
.mini{font-size:28px;font-weight:800}
.url{font-weight:900;font-size:34px;letter-spacing:.01em}
.sticker{position:absolute;border-radius:28px}
"""

def av(key, size, style=''):
    s = ART['av'][key]
    s = s.replace('width="120" height="120"', f'width="{size}" height="{size}"')
    return f'<span class="abs-av" style="display:inline-block;width:{size}px;height:{size}px;{style}">{s}</span>'

def sym(k, size=58, color='#fff'):
    return ART['sim'][k].replace('class="sym"', f'class="sym" style="width:{size}px;height:{size}px;color:{color}"')

def logo(kind='cor', w=300):
    f = {'cor': 'quiddo-cor.svg', 'neg': 'quiddo-negativo.svg', 'uma': 'quiddo-uma-cor.svg',
         'cor-s': 'quiddo-cor-slogan.svg', 'neg-s': 'quiddo-negativo-slogan.svg'}[kind]
    return C.svg_sized(AQ / f, w=w)

def mini(v, size):
    return ART['mini'][v].replace('class="mini-visual"', f'class="mini-visual" width="{size}" height="{size}"')

def cortina(v, w, h):
    return ART['cortina'][v].replace('<svg ', f'<svg width="{w}" height="{h}" ', 1)

LET = 'abcd'

def resp(k, text, style='', extra=''):
    return f'<div class="resp {LET[k]}" style="{style}">{sym(k)}<span>{text}</span>{extra}</div>'

def page(body, w=1080, h=1350, cls=''):
    return f'<section class="page {cls}" style="width:{w}px;height:{h}px">{body}</section>'

def piece(**kw):
    kw.setdefault('brand', 'Quiddo')
    return add(kw)

def cover_from_feed(feed_html_body, cls='', bg='var(--creme)'):
    """Capa 9:16 com a arte 4:5 no centro (y 285–1635): a grade mostra a arte inteira."""
    return doc('capa', FONTS, CSS, f'<section class="page {cls}" style="width:1080px;height:1920px;background:{bg}"><div class="abs" style="left:0;top:285px;width:1080px;height:1350px;overflow:hidden">{feed_html_body}</div></section>', 1080, 1920)

# =====================================================================================
# Q-R4 · Reel meme · "POV" curto, feito para loop e áudio em alta (entra no app)
# =====================================================================================
def q_r4():
    T = 9.6
    tl = TL(T)
    fam = [('jabuti.palha.redondos.3', 'Tia Neide'), ('tucano.bone.-.5', 'Primo Davi'), ('capivara.-.escuros.1', 'Beto'), ('onca.coroa.-.2', 'Mãe')]
    rosto = ''.join(f'''<div style="text-align:center;--r:{(-1)**i*4}deg;{at(2.0 + i*.18, 'drop', .5)}">{av(k, 200)}<div style="font-size:30px;font-weight:900;margin-top:10px">{n}</div>
        <div class="t" style="font-size:96px;color:var(--vermelho);margin-top:-6px;{at(3.0 + i*.15, 'pop')}">?</div></div>''' for i, (k, n) in enumerate(fam))
    s1 = f'''<div {tl.scene(0, 6.0, fin=False, fout=False)}>
      <div class="abs t" style="left:80px;top:300px;width:920px;font-size:84px;{at(.05,'rise')}">POV: você fez um quiz da família e a pergunta 3 era</div>
      <div class="abs card" style="left:80px;top:640px;width:920px;padding:34px 40px;{at(.9,'pop')}"><div class="t" style="font-size:72px">"Qual é o nome completo do vô?"</div></div>
      <div class="abs" style="left:80px;top:960px;width:920px;display:flex;justify-content:space-between">{rosto}</div>
    </div>'''
    s2 = f'''<div {tl.scene(6.0, T, fout=False)}>
      <div class="abs" style="inset:0;background:var(--vermelho)"></div>
      <div class="abs t" style="left:0;right:0;top:520px;text-align:center;font-size:250px;color:#fff;{at(6.05,'pop')}">0 de 9</div>
      <div class="abs t" style="left:0;right:0;top:820px;text-align:center;font-size:80px;color:#fff;{at(6.5,'rise')}">acertaram.</div>
      <div class="abs t" style="left:0;right:0;top:960px;text-align:center;font-size:60px;color:#fff;{at(7.1,'rise')}">O vô acertou.</div>
      <div class="abs" style="left:0;right:0;top:1180px;text-align:center;{at(7.7,'pop')}"><span class="chip" style="font-size:40px;background:var(--amarelo)">Faça o seu. Teste grátis.</span></div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:90px;width:920px;font-size:84px">POV: você fez um quiz da família e a pergunta 3 era</div>
      <div class="abs card" style="left:80px;top:430px;width:920px;padding:34px 40px"><div class="t" style="font-size:72px">"Qual é o nome completo do vô?"</div></div>
      <div class="abs" style="left:80px;top:780px;width:920px;display:flex;justify-content:space-between">{''.join(f'<div style="text-align:center">{av(k, 200)}<div class="t" style="font-size:96px;color:var(--vermelho)">?</div></div>' for k, n in fam)}</div></div>'''
    piece(id='Q-R4', fmt='reel', day=6, slot='19h45', title='Meme POV: a pergunta do vô', total=T, poster=.3, kind='meme',
          html=doc('Q-R4', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, '', 'var(--creme)'),
          caption=('POV: a pergunta 3 do quiz da família era o nome completo do vô. 👴\n\n'
                   '0 de 9 acertaram. O vô acertou.\n\n'
                   'Manda no grupo da família e vê quem sabe 👇\n'
                   'Faça o seu, teste grátis: quiddo.com.br\n#quiz #familia #natalemfamilia #pov #meme #quiddo'),
          notes='Formato meme (POV com texto na tela), curto para rodar em loop. Feito para entrar com um áudio em alta no app (o DOT pega o áudio da semana). CTA de envio para o grupo da família, que é o sinal que mais espalha no Instagram.')


CSS += """
.mtw{display:inline-block;background:#fff;color:var(--tinta);padding:0 .14em;margin:0 -.04em;transform:rotate(-2deg);border-radius:.08em}
@property --n{syntax:'<integer>';inherits:false;initial-value:0}
.cnt{counter-reset:c var(--n)}.cnt::after{content:counter(c)}
"""

def cta_fim(y, cor='var(--amarelo)'):
    return f'<span class="chip" style="font-size:38px;background:{cor}">Faça o seu. Teste grátis.</span>'

# =====================================================================================
# Q-C3 · Carrossel · Desafio: bichos do Brasil (seg, capa amarela)
# =====================================================================================
BICHOS_Q = [
    ('tamandua.-.redondos.8', 'Quanto mede a língua do tamanduá-bandeira?', ['10 cm', '25 cm', 'Até 60 cm', '1,5 m'], 2, 'Até 60 cm. Ela entra no formigueiro e sai cheia.'),
    ('boto.-.-.9', 'Onde vive o boto-cor-de-rosa?', ['No mar', 'Nos rios da Amazônia', 'Em lagos de sal', 'No mangue'], 1, 'Nos rios da Amazônia. É golfinho de água doce.'),
    ('preguica.fone.-.2', 'A preguiça desce da árvore mais ou menos…', ['Toda hora', '1 vez por dia', '1 vez por semana', 'Nunca'], 2, '1 vez por semana, em geral para ir ao "banheiro".'),
    ('loboguara.-.-.1', 'Do que é boa parte da comida do lobo-guará?', ['Peixe', 'Fruta', 'Só carne', 'Folha de árvore'], 1, 'Fruta. A lobeira, ou fruta-do-lobo, é a preferida.'),
    ('jabuti.palha.-.3', 'Jabuti e tartaruga: qual vive só em terra?', ['Jabuti', 'Tartaruga', 'Os dois', 'Nenhum'], 0, 'Jabuti. A tartaruga vive na água.'),
]

def q_c3():
    row = ''.join(f'<div style="--r:{(-1)**i*5}deg;transform:rotate({(-1)**i*5}deg)">{av(k, 172)}</div>' for i, (k, *_ ) in enumerate(BICHOS_Q))
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs" style="left:80px;top:80px">{logo('cor', 210)}</div>
      <div class="abs" style="left:80px;top:250px"><span class="chip">Desafio · 5 perguntas</span></div>
      <div class="abs t" style="left:80px;top:370px;width:930px;font-size:112px">Bichos do Brasil: aposto que você erra <span class="mtw">2 de 5.</span></div>
      <div class="abs" style="left:70px;top:960px;width:940px;display:flex;justify-content:space-between">{row}</div>
      <div class="abs mini" style="left:80px;top:1210px">Arrasta. O gabarito está na última página.</div>''')]
    for i, (k, q, opts, ok, _) in enumerate(BICHOS_Q):
        dark = i % 2 == 1
        opts_html = ''.join(resp(j, o, 'height:150px;font-size:38px') for j, o in enumerate(opts))
        pages.append(page(f'''
          <div class="abs mini" style="left:80px;top:90px;color:{'var(--amarelo)' if dark else 'var(--txt2)'}">PERGUNTA {i+1} DE 5</div>
          <div class="abs" style="right:70px;top:110px;transform:rotate({6 if i%2 else -6}deg)">{av(k, 250)}</div>
          <div class="abs t" style="left:80px;top:170px;width:640px;font-size:76px">{q}</div>
          <div class="abs" style="left:80px;top:640px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:28px">{opts_html}</div>
          <div class="abs mini" style="left:80px;top:1180px;width:920px;color:{'var(--creme)' if dark else 'var(--txt2)'};opacity:.85">Anota a sua. Resposta na última página.</div>''', cls='esc' if dark else ''))
    gab = ''.join(f'''<div style="display:flex;align-items:center;gap:22px;margin-bottom:22px">
        <span class="t" style="font-size:52px;width:46px;color:var(--amarelo)">{i+1}</span>
        <span style="flex:none;width:64px;height:64px;border:5px solid {INK};border-radius:18px;background:{['var(--verde)','var(--laranja)','var(--azul)','var(--vermelho)'][ok]};display:flex;align-items:center;justify-content:center">{sym(ok, 40)}</span>
        <span style="font-size:34px;font-weight:800;line-height:1.2">{exp}</span></div>''' for i, (k, q, opts, ok, exp) in enumerate(BICHOS_Q))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:90px;font-size:96px">Gabarito</div>
      <div class="abs" style="left:80px;top:250px;width:920px">{gab}</div>
      <div class="abs t" style="left:80px;top:860px;width:920px;font-size:56px">Quantas você acertou? Manda pro grupo e vê quem sabe mais.</div>
      <div class="abs" style="left:80px;top:1060px">{cta_fim(0)}</div>
      <div class="abs" style="left:80px;top:1190px">{logo('neg', 230)}</div>
      <div class="abs url" style="right:80px;top:1215px;color:var(--amarelo)">quiddo.com.br</div>''', cls='esc'))
    piece(id='Q-C3', fmt='carrossel', day=1, slot='12h30', title='Desafio: 5 perguntas sobre bichos do Brasil', w=1080, h=1350,
          html=doc('Q-C3', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Bichos do Brasil: aposto que você erra 2 de 5. 🦥\n\n'
                   'Língua do tamanduá, casa do boto, agenda da preguiça, cardápio do lobo-guará e a diferença entre jabuti e tartaruga.\n'
                   'Arrasta, anota as suas e confere o gabarito na última página.\n\n'
                   'Manda no grupo e vê quem acerta mais 👇\n'
                   'Faça o seu quiz, teste grátis: quiddo.com.br\n'
                   '#bichosdobrasil #quiz #desafio #curiosidades #fauna #quiddo'),
          notes='Desafio (motivo de envio: "aposto que você erra"). Capa amarela para separar o mata do domingo (Q-R3) do creme de terça. Fatos conferidos: língua do tamanduá-bandeira até ~60 cm; boto é golfinho de rio; preguiça desce ~1x por semana; lobeira na dieta do lobo-guará; jabuti é terrestre.')

# =====================================================================================
# Q-R5 · Reel meme · "Ninguém: / A tia no quiz da família:" (ter, claro)
# =====================================================================================
def q_r5():
    T = 12.4
    tl = TL(T)
    tia = 'capivara.palha.redondos.1'
    s1 = f'''<div {tl.scene(0, 2.4, fin=False)}>
      <div class="abs t" style="left:90px;top:520px;font-size:140px;{at(.05,'rise')}">Ninguém:</div>
      <div class="abs" style="left:96px;top:720px;width:14px;height:110px;background:var(--tinta);animation:blink .8s steps(1) 0s 3"></div>
    </div>'''
    s2 = f'''<div {tl.scene(2.4, 6.9)}>
      <div class="abs t" style="left:90px;top:330px;width:900px;font-size:84px;{at(2.45,'rise')}">A tia, na pergunta 1 do quiz da família:</div>
      <div class="abs card" style="left:90px;top:680px;width:900px;padding:40px 44px;{at(3.1,'pop')}"><div class="t" style="font-size:70px">"Quem fez essas perguntas? Tá impossível."</div></div>
      <div class="abs" style="left:620px;top:1060px;--r:6deg;{at(3.6,'drop')}">{av(tia, 340)}</div>
      <div class="abs mini" style="left:110px;top:1240px;width:460px;{at(4.6,'fade')}">Tia Célia, 3 segundos depois de reclamar, acertando em 1,4 s.</div>
    </div>'''
    rows = [('1', 'Tia Célia', tia, '5.120', True), ('2', 'Primo Leo', 'tucano.bone.-.5', '4.300', False), ('3', 'Mãe', 'onca.flor.-.2', '4.180', False), ('4', 'Você', 'sapo.-.escuros.4', '2.010', False)]
    rr = ''.join(f'''<div style="height:140px;margin-bottom:22px;display:flex;align-items:center;gap:22px;background:{'var(--amarelo)' if hl else '#fff'};border:6px solid {INK};border-radius:30px;box-shadow:0 10px 0 {INK};padding:0 30px 0 16px;{at(7.1 + i*.15,'slideR')}">
        <span class="t" style="font-size:54px;width:54px;text-align:center">{n}</span>{av(k, 104)}<span style="font-size:44px;font-weight:900;flex:1">{nome}</span><span class="t" style="font-size:54px">{pts}</span></div>''' for i, (n, nome, k, pts, hl) in enumerate(rows))
    s3 = f'''<div {tl.scene(6.9, 9.8)}>
      <div class="abs" style="left:90px;top:320px"><span class="chip" style="background:var(--amarelo)">Placar final</span></div>
      <div class="abs" style="left:90px;top:450px;width:900px">{rr}</div>
      <div class="abs" style="left:540px;top:1140px;--r:-5deg;{at(8.2,'stamp')}"><div class="t" style="background:var(--vermelho);color:#fff;border:7px solid {INK};padding:12px 36px;font-size:72px;box-shadow:0 10px 0 {INK}">De novo.</div></div>
    </div>'''
    s4 = f'''<div {tl.scene(9.8, T, fout=False)}>
      <div class="abs" style="left:190px;top:560px;{at(9.9,'pop')}">{logo('cor', 700)}</div>
      <div class="abs t" style="left:0;right:0;top:860px;text-align:center;font-size:66px;{at(10.2,'rise')}">Toda família tem uma tia dessas.</div>
      <div class="abs" style="left:0;right:0;top:990px;text-align:center;{at(10.5,'rise')}">{cta_fim(0)}</div>
      <div class="abs url" style="left:0;right:0;top:1120px;text-align:center;{at(10.7,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:90px;font-size:110px">Ninguém:</div>
      <div class="abs t" style="left:80px;top:300px;width:920px;font-size:76px">A tia, na pergunta 1 do quiz da família:</div>
      <div class="abs card" style="left:80px;top:560px;width:920px;padding:36px 42px"><div class="t" style="font-size:64px">"Quem fez essas perguntas? Tá impossível."</div></div>
      <div class="abs" style="left:620px;top:900px;transform:rotate(6deg)">{av(tia, 360)}</div></div>'''
    piece(id='Q-R5', fmt='reel', day=2, slot='19h45', title='Meme "Ninguém:": a tia no quiz da família', total=T, poster=.62, kind='meme',
          html=doc('Q-R5', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, '', 'var(--creme)'),
          caption=('Ninguém:\nA tia, na pergunta 1 do quiz da família: "quem fez essas perguntas? tá impossível." 🙄\n\n'
                   'Placar final: Tia Célia em 1º. De novo.\n\n'
                   'Manda pra tia do grupo da família 👇\n'
                   'Faça o seu, teste grátis: quiddo.com.br\n#meme #familia #tia #quiz #natalemfamilia #quiddo'),
          notes='Meme no formato "Ninguém: / Fulano:". Curto (12 s) para loop, com áudio em alta no app. Nomes de exemplo.')

# =====================================================================================
# Q-C4 · Carrossel meme · "Me diga que é Natal sem dizer Natal" (qua, vermelho)
# =====================================================================================
def q_c4():
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--vermelho)"></div>
      <div class="abs" style="left:80px;top:80px">{logo('neg', 210)}</div>
      <div class="abs t" style="left:80px;top:270px;width:930px;font-size:118px;color:#fff">Me diga que é Natal em família sem dizer <span class="mtw">Natal.</span></div>
      <div class="abs" style="left:110px;top:930px;transform:rotate(-6deg)">{av('onca.gorro.-.2', 300)}</div>
      <div class="abs" style="left:620px;top:900px;transform:rotate(7deg)">{av('capivara.gorro.redondos.7', 320)}</div>''')]
    itens = [
        ('"É pavê ou é pra comer?"', 'Todo ano. Mesma pessoa. Mesma risada.', 'tatu.cartola.bigode.3'),
        ('O primo que você só vê uma vez por ano.', 'E que cresceu 30 cm desde a última.', 'tucano.bone.-.5'),
        ('"E os namoradinhos?"', 'Pergunta feita antes do "oi".', 'coruja.flor.redondos.6'),
        ('A disputa pela última rabanada.', 'Sem regra. Sem juiz. Sem perdão.', 'quati.festa.-.1'),
        ('Alguém dormindo no sofá às 22h.', 'Antes da meia-noite, como manda a tradição.', 'preguica.gorro.-.2'),
    ]
    bgs = ['var(--creme)', '#fff', 'var(--creme)', '#fff', 'var(--creme)']
    for i, (tit, sub, k) in enumerate(itens):
        if i % 2 == 0:
            inner = f'''<div class="abs t" style="left:80px;top:150px;font-size:300px;color:var(--vermelho);-webkit-text-stroke:7px {INK}">{i+1}</div>
              <div class="abs t" style="left:80px;top:520px;width:920px;font-size:96px">{tit}</div>
              <div class="abs" style="left:80px;top:860px;width:560px;font-size:42px;font-weight:800;line-height:1.3">{sub}</div>
              <div class="abs" style="left:680px;top:830px;transform:rotate(6deg)">{av(k, 300)}</div>'''
        else:
            inner = f'''<div class="abs" style="left:80px;top:130px;transform:rotate(-5deg)">{av(k, 280)}</div>
              <div class="abs card" style="left:80px;top:500px;width:920px;padding:48px 50px 56px;transform:rotate(-1.2deg)">
                <div class="t" style="font-size:44px;color:var(--vermelho)">{i+1} / 5</div>
                <div class="t" style="font-size:86px;margin-top:14px">{tit}</div>
                <div style="font-size:40px;font-weight:800;margin-top:24px;line-height:1.3">{sub}</div></div>'''
        pages.append(page(f'<div class="abs" style="inset:0;background:{bgs[i]}"></div>{inner}<div class="abs mini" style="left:80px;top:1250px;color:var(--txt2)">{i+1} / 5 · sem dizer Natal</div>'))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:100px;color:var(--creme)">Faltou um: o quiz da <span class="mt">família.</span></div>
      <div class="abs card" style="left:80px;top:560px;width:920px;padding:40px 46px;font-size:42px;font-weight:800;line-height:1.35">A pergunta do vô, o placar do primo e o pódio antes da ceia. Todo mundo joga pelo celular.</div>
      <div class="abs" style="left:80px;top:930px">{cta_fim(0)}</div>
      <div class="abs" style="left:80px;top:1140px">{logo('neg', 260)}</div>
      <div class="abs url" style="right:80px;top:1175px;color:var(--amarelo)">quiddo.com.br</div>''', cls='esc'))
    piece(id='Q-C4', fmt='carrossel', day=3, slot='12h30', title='Meme: me diga que é Natal sem dizer Natal', kind='meme', w=1080, h=1350,
          html=doc('Q-C4', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Me diga que é Natal em família sem dizer Natal. 🎄\n\n'
                   '1. "É pavê ou é pra comer?"\n2. O primo que você só vê uma vez por ano.\n3. "E os namoradinhos?"\n4. A disputa pela última rabanada.\n5. Alguém dormindo no sofá às 22h.\n\n'
                   'Faltou um: o quiz da família. Faça o seu, teste grátis: quiddo.com.br\n'
                   'Manda no grupo da família e marca o tio do pavê 👇\n#natal #natalemfamilia #meme #familia #pave #quiddo'),
          notes='Carrossel de meme ("me diga X sem dizer X"). Capa vermelha (Natal) entre o creme de terça e o creme de quinta. Bichos de gorro do avatarSvg.')

# =====================================================================================
# Q-R6 · Reel trend · Expectativa × realidade: "um quiz rapidinho" (qui, claro)
# =====================================================================================
def q_r6():
    T = 13.6
    tl = TL(T)
    kf = '@keyframes rod{from{--n:1}to{--n:7}}'
    horas = ['21:00', '21:40', '22:30', '23:15', '00:05', '00:40']
    relogio = ''.join(f'<div class="abs t" style="left:0;top:0;font-size:150px;opacity:0;animation:fade .01s linear {4.6 + j*.55:.2f}s 1 both{",fadeOut .01s linear " + format(4.6 + (j+1)*.55, ".2f") + "s 1 forwards" if j < len(horas)-1 else ""}">{h}</div>' for j, h in enumerate(horas))
    s1 = f'''<div {tl.scene(0, 4.3, fin=False)}>
      <div class="abs" style="left:90px;top:320px;{at(.05,'pop')}"><span class="chip" style="background:var(--verde);color:#fff">EXPECTATIVA</span></div>
      <div class="abs t" style="left:90px;top:440px;width:900px;font-size:104px;{at(.3,'rise')}">"Um quiz rapidinho antes da pizza."</div>
      <div class="abs t" style="left:90px;top:900px;font-size:150px;{at(1.2,'fade')}">21:00</div>
      <div class="abs" style="left:90px;top:1080px;{at(1.5,'rise')}"><span class="chip">Rodada 1 de 1</span></div>
      <div class="abs" style="left:660px;top:930px;--r:6deg;{at(1.8,'drop')}">{av('caramelo.festa.-.8', 300)}</div>
    </div>'''
    s2 = f'''<div {tl.scene(4.3, 10.4, fade=.08)}>
      <div class="abs" style="inset:0;background:var(--tinta)"></div>
      <div class="abs" style="left:90px;top:320px;{at(4.35,'pop')}"><span class="chip" style="background:var(--vermelho);color:#fff">REALIDADE</span></div>
      <div class="abs" style="left:90px;top:440px;width:600px;height:160px;color:var(--creme)">{relogio}</div>
      <div class="abs" style="left:90px;top:640px;{at(4.6,'rise')}"><span class="chip" style="font-size:40px;background:var(--amarelo)">Rodada <span class="cnt" style="animation:rod 3s steps(6) 4.8s 1 both"></span></span></div>
      <div class="abs card" style="left:90px;top:820px;width:640px;padding:28px 34px;{at(6.6,'pop')}"><div class="t" style="font-size:56px">"Agora valendo de verdade."</div></div>
      <div class="abs card" style="left:350px;top:1080px;width:640px;padding:28px 34px;background:var(--amarelo);{at(8.0,'pop')}"><div class="t" style="font-size:56px">"Melhor de 9?"</div></div>
      <div class="abs" style="left:780px;top:760px;--r:8deg;{at(6.9,'drop')}">{av('onca.coroa.escuros.2', 220)}</div>
      <div class="abs" style="left:90px;top:1300px;font-size:38px;font-weight:800;color:var(--creme);{at(9.0,'fade')}">A pizza esfriou na rodada 3.</div>
    </div>'''
    s3 = f'''<div {tl.scene(10.4, T, fout=False)}>
      <div class="abs" style="left:190px;top:560px;{at(10.5,'pop')}">{logo('cor', 700)}</div>
      <div class="abs t" style="left:0;right:0;top:860px;text-align:center;font-size:66px;{at(10.8,'rise')}">Ninguém sai antes do pódio.</div>
      <div class="abs" style="left:0;right:0;top:990px;text-align:center;{at(11.1,'rise')}">{cta_fim(0)}</div>
      <div class="abs url" style="left:0;right:0;top:1120px;text-align:center;{at(11.3,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs" style="left:0;top:0;width:1080px;height:640px;background:var(--creme)">
        <div class="abs" style="left:80px;top:80px"><span class="chip" style="background:var(--verde);color:#fff">EXPECTATIVA</span></div>
        <div class="abs t" style="left:80px;top:190px;width:600px;font-size:76px">"Um quiz rapidinho."</div>
        <div class="abs t" style="left:80px;top:440px;font-size:110px">21:00</div>
        <div class="abs" style="left:700px;top:230px;transform:rotate(6deg)">{av('caramelo.festa.-.8', 300)}</div></div>
      <div class="abs" style="left:0;top:640px;width:1080px;height:710px;background:var(--tinta);color:var(--creme)">
        <div class="abs" style="left:80px;top:70px"><span class="chip" style="background:var(--vermelho);color:#fff">REALIDADE</span></div>
        <div class="abs t" style="left:80px;top:180px;width:600px;font-size:76px">"Melhor de 9?"</div>
        <div class="abs t" style="left:80px;top:420px;font-size:110px">00:40</div>
        <div class="abs" style="left:720px;top:220px;transform:rotate(-6deg)">{av('onca.coroa.escuros.2', 280)}</div></div></div>'''
    piece(id='Q-R6', fmt='reel', day=4, slot='19h45', title='Trend expectativa × realidade: "um quiz rapidinho"', total=T, poster=.55, kind='trend',
          html=doc('Q-R6', FONTS, CSS + tl.style() + kf + '@keyframes fadeOut{to{opacity:0}}', body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, '', 'var(--creme)'),
          caption=('Expectativa: "um quiz rapidinho antes da pizza." 🍕\nRealidade: 00:40, rodada 7, "melhor de 9?".\n\n'
                   'No Quiddo, ninguém sai antes do pódio.\n\n'
                   'Manda pro amigo que sempre pede revanche 👇\n'
                   'Faça o seu, teste grátis: quiddo.com.br\n#expectativavsrealidade #quiz #amigos #resenha #noitedejogos #quiddo'),
          notes='Trend "expectativa × realidade". Capa dividida creme/tinta (fica clara na grade). Áudio em alta no app.')

# =====================================================================================
# Q-C5 · Carrossel · Feriado com chuva: 5 temas de quiz (sex 20/11, escuro)
# =====================================================================================
def q_c5():
    temas = [
        ('Família', 'Em que cidade o vô e a vó se conheceram?', None, None, 'Só a família sabe. É aí que fica bom.', 'flor'),
        ('Brasil', 'Qual é a capital mais ao norte do Brasil?', ['Macapá', 'Boa Vista', 'Belém', 'Manaus'], 1, 'Boa Vista, em Roraima.', 'folha'),
        ('Comida', 'De que estado é o pão de queijo?', ['Minas Gerais', 'Goiás', 'São Paulo', 'Bahia'], 0, 'Minas Gerais.', 'sol'),
        ('Ciência', 'Quantos corações tem um polvo?', ['1', '2', '3', '4'], 2, 'Três.', 'gota'),
        ('Quem é mais provável', 'Quem é mais provável de dormir no meio do filme?', None, None, 'As opções são as pessoas da sala.', 'folha'),
    ]
    pages = [page(f'''
      <div class="abs" style="left:80px;top:80px">{logo('neg', 210)}</div>
      <div class="abs t" style="left:80px;top:260px;width:930px;font-size:112px;color:var(--creme)">Feriado com chuva? 5 temas de quiz pra salvar a <span class="mt">tarde.</span></div>
      <div class="abs" style="left:90px;top:900px;transform:rotate(-5deg)">{mini('sala', 260)}</div>
      <div class="abs" style="left:640px;top:860px;transform:rotate(6deg)">{av('preguica.fone.redondos.5', 340)}</div>
      <div class="abs mini" style="left:80px;top:1230px;color:var(--amarelo)">Salva para o feriado</div>''', cls='esc')]
    for i, (tema, q, opts, ok, rodape, s) in enumerate(temas):
        if opts:
            mid = f'''<div class="abs" style="left:80px;top:640px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:26px">{''.join(resp(j, o, 'height:136px;font-size:38px') for j, o in enumerate(opts))}</div>
              <div class="abs" style="left:80px;top:1010px;transform:rotate(-2deg)"><span class="chip" style="background:var(--amarelo)">Resposta: {"ABCD"[ok]} · {rodape}</span></div>'''
        else:
            pes = [('gato.-.escuros.6', 'Tio'), ('jabuti.-.redondos.3', 'Vó'), ('arara.flor.-.4', 'Prima'), ('tatu.cartola.-.9', 'Pai')]
            cells = ''.join(f'<div style="width:215px;text-align:center"><div style="height:190px">{av(k, 180)}</div><div class="resp {LET[j]}" style="justify-content:center;padding:12px 8px;font-size:30px;margin-top:14px">{sym(j, 34)}{n}</div></div>' for j, (k, n) in enumerate(pes)) if i == 4 else ''
            mid = (f'<div class="abs" style="left:80px;top:620px;width:920px;display:flex;justify-content:space-between">{cells}</div>' if cells else
                   f'<div class="abs" style="left:80px;top:640px;transform:rotate(-4deg)">{av("coruja.-.redondos.6", 300)}</div><div class="abs" style="left:440px;top:700px;transform:rotate(5deg)">{av("jabuti.palha.redondos.3", 280)}</div>')
            mid += f'<div class="abs card" style="left:80px;top:1010px;width:920px;padding:26px 34px;font-size:34px;font-weight:800">{rodape}</div>'
        pages.append(page(f'''
          <div class="abs mini" style="left:80px;top:90px;color:var(--txt2)">TEMA {i+1} DE 5</div>
          <div class="abs" style="left:80px;top:150px;display:flex;align-items:center;gap:20px">{sym(['folha','sol','gota','flor'].index(s), 70, INK)}<span class="t" style="font-size:84px">{tema}</span></div>
          <div class="abs t" style="left:80px;top:300px;width:920px;font-size:66px">{q}</div>{mid}'''))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--verde)"></div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:100px;color:#fff">Junta as 5 e chama a <span class="mt">turma.</span></div>
      <div class="abs card" style="left:80px;top:480px;width:920px;padding:40px 46px;font-size:42px;font-weight:800;line-height:1.35">Escreve as perguntas, manda o código da sala e todo mundo joga pelo celular. Sem baixar app.</div>
      <div class="abs" style="left:80px;top:860px">{cta_fim(0)}</div>
      <div class="abs" style="left:80px;top:1080px">{logo('neg', 280)}</div>
      <div class="abs url" style="right:80px;top:1120px;color:#fff">quiddo.com.br</div>'''))
    piece(id='Q-C5', fmt='carrossel', day=5, slot='12h30', title='Feriado com chuva: 5 temas de quiz', w=1080, h=1350,
          html=doc('Q-C5', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Feriado com chuva? 5 temas de quiz pra salvar a tarde. ☔\n\n'
                   '1. Família: em que cidade o vô e a vó se conheceram?\n2. Brasil: qual é a capital mais ao norte?\n3. Comida: de que estado é o pão de queijo?\n4. Ciência: quantos corações tem um polvo?\n5. Quem é mais provável de dormir no meio do filme?\n\n'
                   'Salva e manda no grupo de quem vai passar o feriado junto 👇\n'
                   'Faça o seu, teste grátis: quiddo.com.br\n#feriado #feriadao #quiz #diversaoemfamilia #jogosemfamilia #quiddo'),
          notes='Sexta 20/11 é feriado nacional. Utilidade (salvar e mandar no grupo). Respostas conferidas: Boa Vista é a capital mais ao norte; pão de queijo é de Minas; polvo tem 3 corações.')

# =====================================================================================
# Q-C6 · Carrossel produto · Natal em 1 mês: o quiz da família em 3 passos (dom, azul)
# =====================================================================================
def q_c6():
    vis = [('floresta', 'Floresta'), ('sala', 'Sala de aula'), ('album', 'Álbum'), ('espaco', 'Espaço'), ('escritorio', 'Escritório'), ('amor', 'Amor')]
    grid = ''.join(f'<div class="card" style="padding:18px;text-align:center">{mini(k, 220)}<div style="font-size:30px;font-weight:900;margin-top:8px">{n}</div></div>' for k, n in vis)
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--azul)"></div>
      <div class="abs" style="left:80px;top:80px">{logo('neg', 210)}</div>
      <div class="abs t" style="left:80px;top:260px;width:930px;font-size:120px;color:#fff">Natal em 1 mês. O quiz da família em <span class="mt">3 passos.</span></div>
      <div class="abs" style="left:640px;top:860px;transform:rotate(6deg)">{av('tucano.gorro.redondos.5', 330)}</div>
      <div class="abs" style="left:110px;top:940px;transform:rotate(-6deg)">{av('jabuti.gorro.bigode.3', 260)}</div>''')]
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:100px;font-size:180px;color:var(--azul);-webkit-text-stroke:6px {INK}">1</div>
      <div class="abs t" style="left:280px;top:150px;width:720px;font-size:84px">Escolha o visual.</div>
      <div class="abs" style="left:80px;top:420px;width:920px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px">{grid}</div>'''))
    tipos = [(0, 'Quiz que vale ponto', '"Qual é o nome completo do vô?"'), (1, 'Enquete, ninguém erra', '"Melhor prato da ceia?"'), (2, 'Quem é mais provável', '"…de abrir o presente antes?"')]
    rows = ''.join(f'<div class="resp {LET[k]}" style="margin-bottom:26px;flex-direction:column;align-items:flex-start;gap:6px;padding:26px 34px"><div style="display:flex;gap:18px;align-items:center">{sym(k, 48)}<span style="font-size:34px">{a}</span></div><span class="t" style="font-size:52px">{b}</span></div>' for k, a, b in tipos)
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:100px;font-size:180px;color:var(--laranja);-webkit-text-stroke:6px {INK}">2</div>
      <div class="abs t" style="left:280px;top:150px;width:720px;font-size:84px">Escreva as perguntas da família.</div>
      <div class="abs" style="left:80px;top:480px;width:920px">{rows}</div>'''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:100px;font-size:180px;color:var(--amarelo);-webkit-text-stroke:6px {INK}">3</div>
      <div class="abs t" style="left:280px;top:150px;width:720px;font-size:84px">Manda o código no grupo.</div>
      <div class="abs card" style="left:180px;top:480px;width:720px;padding:46px;text-align:center;transform:rotate(-2deg)">
        <div class="mini" style="color:var(--txt2)">CÓDIGO DA SALA · EXEMPLO</div>
        <div class="t" style="font-size:170px;letter-spacing:.06em;margin-top:10px">K7Q2</div></div>
      <div class="abs" style="left:80px;top:960px;width:920px;font-size:44px;font-weight:800;line-height:1.3">Cada um entra pelo celular. Sem baixar app.</div>''', cls=''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:104px;color:var(--creme)">No dia: celular na mão e pódio antes da <span class="mt">ceia.</span></div>
      <div class="abs" style="left:80px;top:700px">{cta_fim(0)}</div>
      <div class="abs" style="left:80px;top:900px;width:900px;font-size:40px;color:var(--creme);line-height:1.3">Manda este post no grupo da família e já avisa: este ano tem quiz.</div>
      <div class="abs" style="left:80px;top:1130px">{logo('neg', 280)}</div>
      <div class="abs url" style="right:80px;top:1170px;color:var(--amarelo)">quiddo.com.br</div>''', cls='esc'))
    piece(id='Q-C6', fmt='carrossel', day=7, slot='12h30', title='Natal em 1 mês: o quiz da família em 3 passos (produto)', kind='produto', w=1080, h=1350,
          html=doc('Q-C6', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Natal em 1 mês. O quiz da família em 3 passos. 🎄\n\n'
                   '1. Escolha o visual.\n2. Escreva as perguntas da família: quiz que vale ponto, enquete e "quem é mais provável".\n3. Manda o código no grupo. Cada um joga pelo celular, sem baixar app.\n\n'
                   'Manda no grupo da família e já avisa: este ano tem quiz 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#natal #natalemfamilia #quiz #ceiadenatal #familia #quiddo'),
          notes='Peça de produto. Visuais são as miniaturas oficiais do site (art.json). Código da sala é de exemplo e está marcado. Capa azul fecha a semana depois do creme do Q-R4.')

# =====================================================================================
# Stories · "Pergunta do dia" (resposta de cabeça pra baixo, sem adesivo)
# =====================================================================================
PERGUNTAS_DIA = [
    (1, 'Qual é a maior ave do Brasil?', ['Tucano', 'Ema', 'Arara', 'Gavião'], 1, 'Ema', 'bemtevi.-.-.0', False),
    (2, 'Quantos ossos tem o corpo de um adulto?', ['106', '206', '306', '406'], 1, '206', 'coruja.-.redondos.6', True),
    (3, 'Qual é o maior roedor do mundo?', ['Rato-gigante', 'Capivara', 'Castor', 'Paca'], 1, 'Capivara', 'capivara.bone.-.7', False),
    (4, 'Qual é o planeta mais quente do Sistema Solar?', ['Mercúrio', 'Vênus', 'Marte', 'Júpiter'], 1, 'Vênus, não Mercúrio: a atmosfera segura o calor', 'gato.coroa.-.6', True),
    (5, 'Quantos estados tem o Brasil?', ['24', '25', '26', '27'], 2, '26, mais o Distrito Federal', 'arara.festa.-.4', False),
    (6, 'Qual é o maior bioma do Brasil?', ['Cerrado', 'Amazônia', 'Mata Atlântica', 'Pantanal'], 1, 'Amazônia', 'mico.flor.-.7', True),
    (7, 'Qual destes bichos é um mamífero?', ['Jacaré', 'Sapo', 'Boto', 'Tucano'], 2, 'Boto', 'boto.-.estrela.9', False),
]

def q_stories():
    for n, (d, q, opts, ok, ans, k, dark) in enumerate(PERGUNTAS_DIA):
        grid = ''.join(resp(j, o, 'height:150px;font-size:40px') for j, o in enumerate(opts))
        body = f'''<section class="page {'esc' if dark else ''}" style="width:1080px;height:1920px">
          <div class="abs" style="left:80px;top:290px"><span class="chip" style="background:var(--amarelo)">Pergunta do dia · {C.DIAS[d].split()[1]}</span></div>
          <div class="abs" style="right:80px;top:260px;transform:rotate(6deg)">{av(k, 190)}</div>
          <div class="abs t" style="left:80px;top:470px;width:920px;font-size:96px">{q}</div>
          <div class="abs" style="left:80px;top:890px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:28px">{grid}</div>
          <div class="abs" style="left:80px;top:1260px;width:920px;transform:rotate(180deg);text-align:right"><span class="mini" style="opacity:.75">Resposta: {"ABCD"[ok]} · {ans}</span></div>
          <div class="abs t" style="left:80px;top:1340px;width:920px;font-size:48px">Tira print e manda no grupo: quem acerta?</div>
          <div class="abs" style="left:80px;top:1510px">{logo('neg' if dark else 'cor', 170)}</div>
        </section>'''
        sid = f'Q-S{5 + n + 1}'
        piece(id=sid, fmt='story', day=d, title=f'Pergunta do dia: {q}', w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker='', kind='story',
              notes='Sem adesivo: a resposta está na arte, de cabeça pra baixo. Motivo de envio: print no grupo. Fato conferido.')

def build():
    q_c3(); q_r5(); q_c4(); q_r6(); q_c5(); q_r4(); q_c6(); q_stories()

build()
