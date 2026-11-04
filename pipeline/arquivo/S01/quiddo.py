"""Quiddo · Pack Semanal 01. Fraunces 900 + Nunito; creme/tinta/mata; contorno grosso e sombra dura.
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
# Q-R1 · Reel · "Quem é mais provável…" (Floresta, fundo escuro)
# =====================================================================================
def q_r1():
    T = 17.0
    tl = TL(T)
    opts = [('tucano.bone.-.5', 'Primo Davi'), ('capivara.palha.-.1', 'Tia Neide'),
            ('coruja.-.redondos.6', 'Vó Lurdes'), ('preguica.fone.-.2', 'Beto')]
    # cena 1: gancho
    s1 = f'''<div {tl.scene(0, 3.7, fin=False)}>
      <div class="abs" style="left:90px;top:330px;{at(.05,'pop')}"><span class="chip" style="background:var(--amarelo)">Pergunta 4 de 10</span></div>
      <div class="abs t" style="left:90px;top:450px;width:900px;font-size:104px;color:var(--creme);{at(.2,'rise')}">Quem é mais provável de chegar <span class="mt">atrasado</span> no amigo secreto?</div>
      <div class="abs" style="left:640px;top:1150px;--r:6deg;{at(.9,'drop')}">{av('preguica.fone.-.2', 300)}</div>
      <div class="abs" style="left:150px;top:1220px;--r:-7deg;{at(1.2,'drop')}">{av('tucano.bone.-.5', 230)}</div>
    </div>'''
    # cena 2: opções + contagem do olho (5 s)
    rows = ''
    for i, (k, n) in enumerate(opts):
        rows += f'<div style="{at(3.9 + i * .18, "slideL")}">' + resp(i, n, 'height:150px;margin-bottom:26px;padding-left:20px', '') .replace(f'{sym(i)}', f'{sym(i)}<span style="margin-left:-6px">{av(k, 104)}</span>', 1) + '</div>'
    olho = f'''<svg width="250" height="250" viewBox="0 0 300 300"><circle cx="150" cy="150" r="136" fill="#13A07A" stroke="{INK}" stroke-width="8"/>
      <circle cx="150" cy="150" r="105" fill="none" stroke="#0B5D45" stroke-width="14"/>
      <circle cx="150" cy="150" r="105" fill="none" stroke="#FFC83D" stroke-width="14" stroke-linecap="round" pathLength="100" stroke-dasharray="100 200" transform="rotate(-90 150 150)" style="animation:drain 5s linear 3.8s 1 both"/>
      <circle cx="150" cy="150" r="88" fill="#5BC0EB" stroke="{INK}" stroke-width="7"/><circle cx="150" cy="150" r="62" fill="#fff" stroke="{INK}" stroke-width="4"/></svg>'''
    nums = ''.join(f'<div class="abs t" style="left:0;right:0;top:78px;text-align:center;font-size:96px;color:{INK};opacity:0;animation:fade .01s linear {3.8 + j}s 1 both{",fadeOut .01s linear " + str(3.8 + j + 1) + "s 1 forwards" if j < 4 else ""}">{5 - j}</div>' for j in range(5))
    s2 = f'''<div {tl.scene(3.7, 9.0)}>
      <div class="abs t" style="left:90px;top:300px;width:620px;font-size:56px;color:var(--creme)">Quem é mais provável de chegar <span class="mt">atrasado</span> no amigo secreto?</div>
      <div class="abs" style="left:760px;top:290px;width:250px;height:250px">{olho}{nums}</div>
      <div class="abs" style="left:90px;top:640px;width:900px">{rows}</div>
    </div>'''
    # cena 3: resultado
    votos = [1, 1, 0, 7]
    bars = ''
    for i, (k, n) in enumerate(opts):
        w = 120 + votos[i] * 92
        win = i == 3
        bars += f'''<div style="display:flex;align-items:center;gap:22px;height:150px;margin-bottom:22px">
          {av(k, 120)}
          <div style="flex:1"><div class="mini" style="color:var(--creme);margin-bottom:8px">{n}</div>
          <div style="height:58px;width:{w}px;border:5px solid {INK};border-radius:18px;background:{['var(--verde)','var(--laranja)','var(--azul)','var(--vermelho)'][i]};box-shadow:0 6px 0 {INK};transform-origin:left;{at(9.3 + i * .12, 'grow')}"></div></div>
          <div class="t" style="font-size:64px;color:{'var(--amarelo)' if win else 'var(--creme)'};width:120px;text-align:right;{at(9.9, 'fade')}">{votos[i]}</div></div>'''
    s3 = f'''<div {tl.scene(9.0, 13.2)}>
      <div class="abs mini" style="left:90px;top:320px;color:var(--amarelo);{at(9.1,'fade')}">9 PESSOAS VOTARAM</div>
      <div class="abs" style="left:90px;top:400px;width:900px">{bars}</div>
      <div class="abs t" style="left:90px;top:1200px;width:900px;font-size:92px;color:var(--creme);{at(10.6,'pop')}">Beto, de <span class="mt">novo.</span></div>
      <div class="abs" style="left:90px;top:1330px;font-size:40px;color:var(--creme);{at(11.3,'rise')}">Ninguém ficou surpreso. Nem o Beto.</div>
    </div>'''
    # cena 4: fim
    s4 = f'''<div {tl.scene(13.2, T, fout=False)}>
      <div class="abs" style="left:190px;top:560px;{at(13.35,'pop')}">{logo('neg', 700)}</div>
      <div class="abs t" style="left:0;right:0;top:860px;text-align:center;font-size:72px;color:var(--creme);{at(13.8,'rise')}">Quiz ao vivo, do seu jeito.</div>
      <div class="abs" style="left:0;right:0;top:990px;text-align:center;{at(14.2,'rise')}"><span class="chip" style="font-size:38px;background:var(--amarelo)">Faça o seu. Teste grátis.</span></div>
      <div class="abs url" style="left:0;right:0;top:1120px;text-align:center;color:var(--amarelo);{at(14.5,'fade')}">quiddo.com.br</div>
    </div>'''
    css = CSS + tl.style() + '@keyframes fadeOut{to{opacity:0}}@keyframes drain{from{stroke-dashoffset:0}to{stroke-dashoffset:100}}'
    body = f'<section class="page esc" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}</section>'
    cover_body = f'''<div class="page esc" style="width:1080px;height:1350px">
      <div class="abs" style="left:80px;top:80px">{logo('neg', 210)}</div>
      <div class="abs t" style="left:80px;top:270px;width:920px;font-size:100px">Quem é mais provável de chegar <span class="mt">atrasado</span> no amigo secreto?</div>
      <div class="abs" style="left:610px;top:860px;transform:rotate(6deg)">{av('preguica.fone.-.2', 360)}</div>
      <div class="abs" style="left:120px;top:960px;transform:rotate(-7deg)">{av('tucano.bone.-.5', 250)}</div></div>'''
    piece(id='Q-R1', fmt='reel', day=1, slot='19h45', title='Quem é mais provável… (amigo secreto)', total=T,
          html=doc('Q-R1', FONTS, css, body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'esc', 'var(--mata)'),
          caption=('Toda família tem um Beto. 🦥\n\nNo Quiddo, além do quiz que vale ponto, tem a pergunta "Quem é mais provável…": '
                   'as opções são as pessoas da sala e todo mundo vota pelo celular.\n\n'
                   'Use no amigo secreto, no Natal ou na confraternização. Faça o seu, teste grátis.\n'
                   'Marca aqui o Beto da sua família 👇\n\nquiddo.com.br (link na bio)\n'
                   '#amigosecreto #natalemfamilia #quiz #quizaovivo #brincadeira #resenha #quiddo'),
          notes='Floresta, fundo mata. Áudio: tique da contagem (5 s), plim no resultado. Música em alta a 20–30%.')

# =====================================================================================
# Q-C1 · Carrossel · Confraternização (Escritório, claro)
# =====================================================================================
POSTIT = ['#FFC23D', '#FF8FB0', '#8FA6FF', '#7FE0B5']

def postit(x, y, s, rot, cor, inner='', fs=30):
    return f'<div class="abs" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{cor};border:5px solid {INK};transform:rotate({rot}deg);box-shadow:0 8px 0 {INK};padding:26px;font-weight:900;font-size:{fs}px;line-height:1.15;color:{INK}">{inner}</div>'

def q_c1():
    pages = []
    # 1 capa
    pages.append(page(f'''
      <div class="abs" style="left:80px;top:80px">{logo('cor', 210)}</div>
      <div class="abs chip" style="left:80px;top:250px;background:var(--amarelo)">Salva pra confraternização</div>
      <div class="abs t" style="left:80px;top:360px;width:930px;font-size:108px">7 perguntas que não constrangem <span class="mt">ninguém</span> na festa da firma</div>
      <div class="abs" style="left:-40px;top:980px;width:1160px;height:420px;overflow:hidden;border-top:6px solid {INK}">{cortina('escritorio', 1160, 700)}</div>
      <div class="abs" style="right:80px;top:880px;transform:rotate(6deg)">{av('tucano.bone.redondos.5', 200)}</div>'''))
    # 2 quiz com números (lista vertical)
    pages.append(page(f'''
      <div class="abs mini" style="left:80px;top:90px;color:var(--txt2)">1 / 7 · QUIZ · VALE PONTO</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:84px">Quantos cafés a copa serve num dia <span class="mt">normal?</span></div>
      <div class="abs" style="left:80px;top:520px;width:920px">
        {resp(0,'40','margin-bottom:26px')}{resp(1,'120','margin-bottom:26px')}{resp(2,'300','margin-bottom:26px')}{resp(3,'Ninguém tem coragem de contar')}</div>
      <div class="abs mini" style="left:80px;top:1220px;width:920px;color:var(--txt2)">Antes da festa, pergunte na copa. A resposta certa vira assunto.</div>'''))
    # 3 quem é mais provável (avatares em linha)
    people = [('gato.-.escuros.6', 'Lu'), ('jabuti.-.redondos.3', 'Marcão'), ('arara.flor.-.4', 'Dri'), ('tatu.cartola.-.9', 'Seu Zé')]
    cells = ''.join(f'<div style="width:215px;text-align:center"><div style="height:200px">{av(k,190)}</div><div class="resp {LET[i]}" style="justify-content:center;padding:14px 8px;font-size:30px;margin-top:20px">{sym(i,36)}{n}</div></div>' for i, (k, n) in enumerate(people))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs mini" style="left:80px;top:90px">2 / 7 · QUEM É MAIS PROVÁVEL</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:92px">Quem responde <span style="white-space:nowrap">e-mail</span> às 23h?</div>
      <div class="abs" style="left:80px;top:600px;width:920px;display:flex;justify-content:space-between">{cells}</div>
      <div class="abs card" style="left:80px;top:1060px;width:920px;padding:30px 36px;font-size:32px;font-weight:800">As opções são as pessoas da sala. Ninguém erra, todo mundo ri.</div>'''))
    # 4 enquete (barras)
    bars = [('A reunião de alinhamento do alinhamento', 46, 0), ('A daily que durou 1 hora', 31, 1), ('A que começou "rapidinho"', 23, 2)]
    bh = ''.join(f'''<div style="margin-bottom:40px"><div style="font-size:36px;font-weight:800;margin-bottom:12px">{t}</div>
        <div style="display:flex;align-items:center;gap:20px"><div style="height:64px;width:{p*14}px;background:{['var(--verde)','var(--laranja)','var(--azul)'][k]};border:5px solid {INK};border-radius:16px;box-shadow:0 6px 0 {INK}"></div><span class="t" style="font-size:56px">{p}%</span></div></div>''' for t, p, k in bars)
    pages.append(page(f'''
      <div class="abs mini" style="left:80px;top:90px;color:var(--txt2)">3 / 7 · ENQUETE · NINGUÉM ERRA</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:88px">Qual reunião podia ter sido um <span class="mt">e-mail?</span></div>
      <div class="abs" style="left:80px;top:560px;width:920px">{bh}</div>
      <div class="abs mini" style="left:80px;top:1230px;color:var(--txt2)">Resultado ilustrativo. O da sua firma sai ao vivo.</div>'''))
    # 5 complete a frase (post-its)
    pages.append(page(f'''
      <div class="abs mini" style="left:80px;top:90px;color:var(--txt2)">4 / 7 · COMPLETE</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:96px">"Vamos alinhar…"</div>
      {postit(90, 470, 400, -5, POSTIT[0], '<span style="font-family:Fraunces;font-size:56px">A</span><br>…na segunda', 46)}
      {postit(570, 450, 400, 4, POSTIT[1], '<span style="font-family:Fraunces;font-size:56px">B</span><br>…offline', 46)}
      {postit(110, 900, 400, 3, POSTIT[2], '<span style="font-family:Fraunces;font-size:56px">C</span><br>…as expectativas', 46)}
      {postit(560, 880, 400, -4, POSTIT[3], '<span style="font-family:Fraunces;font-size:56px">D</span><br>…depois do almoço', 46)}'''))
    # 6 template da empresa
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--mata)"></div>
      <div class="abs mini" style="left:80px;top:90px;color:var(--amarelo)">5 / 7 · QUIZ · VALE PONTO</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:96px;color:var(--creme)">Em que ano a empresa <span class="mt">nasceu?</span></div>
      <div class="abs" style="left:80px;top:560px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:28px">
        {resp(0,'2009')}{resp(1,'2012')}{resp(2,'2015')}{resp(3,'2018')}</div>
      <div class="abs card" style="left:80px;top:1000px;width:920px;padding:30px 36px;font-size:32px;font-weight:800;background:var(--creme)">Troque pelos dados da sua empresa. Pergunta de casa vale mais que trivia.</div>'''))
    # 7 perguntas 6 e 7 juntas + fechamento
    pages.append(page(f'''
      <div class="abs mini" style="left:80px;top:90px;color:var(--txt2)">6 E 7 / 7 · PARA FECHAR</div>
      <div class="abs card" style="left:80px;top:160px;width:920px;padding:36px 40px;transform:rotate(-1.5deg)"><div class="t" style="font-size:60px">Quem é mais provável de ganhar o amigo secreto e trocar?</div></div>
      <div class="abs card" style="left:80px;top:500px;width:920px;padding:36px 40px;transform:rotate(1.2deg);background:var(--amarelo)"><div class="t" style="font-size:60px">Qual é o melhor momento do ano na firma?</div><div style="font-size:30px;margin-top:12px">Enquete. Deixe a resposta mais votada para o discurso.</div></div>
      <div class="abs t" style="left:80px;top:930px;width:920px;font-size:64px">Pódio no fim, foto pro grupo.</div>
      <div class="abs" style="left:80px;top:1040px"><span class="chip" style="font-size:38px;background:var(--amarelo)">Faça o seu. Teste grátis.</span></div>
      <div class="abs" style="left:80px;top:1170px">{logo('cor', 240)}</div>
      <div class="abs url" style="right:80px;top:1210px">quiddo.com.br</div>'''))
    body = ''.join(pages)
    piece(id='Q-C1', fmt='carrossel', day=2, slot='12h30', title='7 perguntas para a festa da firma', w=1080, h=1350,
          html=doc('Q-C1', FONTS, CSS, body, 1080, 1350),
          caption=('7 perguntas para a confraternização que não constrangem ninguém. 💼\n\n'
                   'Tem quiz que vale ponto, enquete em que ninguém erra e "quem é mais provável", que é onde a sala ri de verdade.\n'
                   'Arrasta, salva e troca os dados pelos da sua empresa.\n\n'
                   'Marca aqui quem organiza a festa 👇\nFaça o seu, teste grátis: quiddo.com.br\n'
                   '#confraternizacao #festadefimdeano #endomarketing #rh #dinamicadegrupo #quiz #quiddo'),
          notes='Escritório (post-its do site). Página 1 usa a cortina oficial do visual Escritório.')

# =====================================================================================
# Q-R2 · Reel · "Que bicho você seria?" (Álbum de figurinhas, escuro)
# =====================================================================================
def figurinha(k, n, nome, fundo, size=560, rot=-4):
    return f'''<div style="width:{size}px;color:{INK};background:#fff;border:7px solid {INK};border-radius:30px;box-shadow:0 14px 0 {INK};padding:26px;transform:rotate({rot}deg)">
      <div style="background:{fundo};border:5px solid {INK};border-radius:20px;height:{size-120}px;display:flex;align-items:center;justify-content:center;position:relative">{av(k, size-180)}
      <span class="abs t" style="left:18px;top:12px;font-size:40px">Nº {n:02d}</span></div>
      <div class="t" style="font-size:44px;margin-top:18px;text-align:center">{nome}</div></div>'''

def q_r2():
    T = 19.4
    tl = TL(T)
    slots = ''.join(f'<div style="border:5px dashed rgba(255,246,230,.25);border-radius:26px"></div>' for _ in range(12))
    grid = f'<div class="abs" style="left:60px;top:60px;right:60px;bottom:60px;display:grid;grid-template-columns:repeat(3,1fr);gap:40px">{slots}</div>'
    s1 = f'''<div {tl.scene(0, 3.5, fin=False)}>
      <div class="abs t" style="left:90px;top:360px;width:900px;font-size:110px;color:var(--creme);{at(.1,'rise')}">Diz qual bicho você <span class="mt">escolhe.</span></div>
      <div class="abs t" style="left:90px;top:640px;width:900px;font-size:80px;color:var(--amarelo);{at(.9,'rise')}">Eu digo como você joga.</div>
      <div class="abs" style="left:200px;top:880px;{at(1.3,'drop')}">{figurinha('onca.coroa.-.2', 3, 'Onça', '#FFF0CC', 520, -5)}</div>
    </div>'''
    tipos = [('capivara.bone.-.7', 7, 'Capivara de boné', '#E3F2C8', 'Responde por último.', 'Acerta tudo.', 4),
             ('onca.coroa.escuros.2', 3, 'Onça de coroa', '#FFF0CC', 'Entra na sala', 'já se achando campeã.', -3),
             ('preguica.fone.-.5', 12, 'Preguiça de fone', '#DCEBFA', 'Ainda está lendo', 'a pergunta 2.', 5),
             ('sapo.festa.estrela.4', 18, 'Sapo de chapéu de festa', '#FDE2E1', 'Veio pela resenha.', 'Ficou pelo pódio.', -4)]
    sc = ''
    t = 3.5
    for k, n, nome, fundo, l1, l2, rot in tipos:
        sc += f'''<div {tl.scene(t, t + 3.2)}>
          <div class="abs" style="left:250px;top:300px;{at(t + .05,'drop')}">{figurinha(k, n, nome, fundo, 580, rot)}</div>
          <div class="abs t" style="left:90px;top:1080px;width:900px;font-size:76px;color:var(--creme);text-align:center;{at(t + .55,'rise')}">{l1}</div>
          <div class="abs t" style="left:90px;top:1180px;width:900px;font-size:76px;text-align:center;{at(t + 1.0,'pop')}"><span class="mt">{l2}</span></div>
        </div>'''
        t += 3.2
    small = ['tucano.-.-.0', 'arara.flor.-.4', 'tamandua.gorro.-.8', 'boto.-.coracao.9', 'loboguara.faixa.-.1', 'caramelo.bone.bigode.3']
    row = ''.join(f'<div style="--r:{(-1)**i*6}deg;{at(16.4 + i*.1,"pop")}">{av(k, 150)}</div>' for i, k in enumerate(small))
    s6 = f'''<div {tl.scene(16.3, T, fout=False)}>
      <div class="abs" style="left:60px;right:60px;top:380px;display:flex;justify-content:space-between">{row}</div>
      <div class="abs t" style="left:90px;top:640px;width:900px;font-size:92px;color:var(--creme);text-align:center;{at(16.7,'rise')}">20 bichos. 13.200 combinações. Qual é <span class="mt">o seu?</span></div>
      <div class="abs" style="left:240px;top:1080px;{at(17.4,'pop')}">{logo('neg', 600)}</div>
      <div class="abs" style="left:0;right:0;top:1330px;text-align:center;{at(17.7,'rise')}"><span class="chip" style="font-size:38px;background:var(--amarelo)">Faça o seu. Teste grátis.</span></div>
      <div class="abs url" style="left:0;right:0;top:1460px;text-align:center;color:var(--amarelo);{at(17.9,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page esc" style="width:1080px;height:1920px">{grid}{s1}{sc}{s6}</section>'
    cover_body = f'''<div class="page esc" style="width:1080px;height:1350px">
      <div class="abs" style="left:80px;top:80px">{logo('neg', 210)}</div>
      <div class="abs t" style="left:80px;top:260px;width:920px;font-size:96px">Diz qual bicho você <span class="mt">escolhe.</span> Eu digo como você joga.</div>
      <div class="abs" style="left:110px;top:720px">{figurinha('capivara.bone.-.7', 7, 'Capivara de boné', '#E3F2C8', 420, -6)}</div>
      <div class="abs" style="left:560px;top:760px">{figurinha('preguica.fone.-.5', 12, 'Preguiça de fone', '#DCEBFA', 420, 5)}</div></div>'''
    piece(id='Q-R2', fmt='reel', day=4, slot='19h45', title='Que bicho você seria? (tipologia)', total=T, poster=.3,
          html=doc('Q-R2', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'esc', 'var(--mata)'),
          caption=('Diz qual bicho você escolhe e a gente diz como você joga. 🐸\n\n'
                   'Capivara de boné: responde por último e acerta tudo.\n'
                   'Onça de coroa: entra na sala já se achando campeã.\n'
                   'Preguiça de fone: ainda está lendo a pergunta 2.\n'
                   'Sapo de chapéu de festa: veio pela resenha, ficou pelo pódio.\n\n'
                   'No Quiddo são 20 bichos do Brasil e 13.200 jeitos de montar o seu. Qual é o seu? Comenta 👇\nFaça o seu, teste grátis: quiddo.com.br\n'
                   '#bichosdobrasil #capivara #quiz #resenha #jogoemgrupo #quiddo'),
          notes='Visual Álbum de figurinhas sobre fundo mata. Bichos gerados pelo avatarSvg do site.')

# =====================================================================================
# Q-C2 · Carrossel · 5 regras (Sala de aula, claro)
# =====================================================================================
def caderno(margin=True):
    lines = ''.join(f'<div class="abs" style="left:0;right:0;top:{y}px;height:3px;background:#C9D8F5"></div>' for y in range(200, 1350, 72))
    m = '<div class="abs" style="left:150px;top:0;bottom:0;width:4px;background:rgba(229,56,59,.55)"></div>' if margin else ''
    return f'<div class="abs" style="inset:0;background:#FFFDF5"></div>{lines}{m}'

def q_c2():
    regras = [
        ('Comece fácil.', 'A primeira pergunta é para a sala inteira acertar. Ela ensina o jogo sem ninguém explicar.', 'folha'),
        ('Uma pergunta, uma ideia.', 'Se a pergunta precisa de vírgula, ela vira duas perguntas.', 'sol'),
        ('Misture os tipos.', 'Quiz vale ponto. Enquete ninguém erra. "Quem é mais provável" é onde a sala ri.', 'gota'),
        ('A difícil vai no meio.', 'No fim, a turma quer virada, não frustração. Guarde a última para a mais divertida.', 'flor'),
        ('Feche com o pódio.', 'Revele do 3º para o 1º, devagar. Depois, todo mundo junto para a foto.', 'folha'),
    ]
    pages = [page(f'''{caderno()}
      <div class="abs" style="left:200px;top:90px">{logo('cor', 210)}</div>
      <div class="abs t" style="left:200px;top:300px;width:800px;font-size:112px">Como fazer um quiz que ninguém <span class="mt">esquece</span></div>
      <div class="abs" style="left:200px;top:820px;font-size:40px;font-weight:800;width:760px">5 regras para a próxima festa, aula ou resenha.</div>
      <div class="abs" style="left:640px;top:960px;transform:rotate(6deg)">{av('coruja.-.redondos.6', 300)}</div>
      <div class="abs t" style="left:210px;top:1080px;background:var(--vermelho);color:#fff;border:7px solid {INK};padding:12px 36px;font-size:76px;box-shadow:0 10px 0 {INK};transform:rotate(-6deg)">Nota 10</div>''')]
    for i, (tit, txt, s) in enumerate(regras):
        # composições alternadas: número gigante à esquerda, cartão, etc.
        if i % 2 == 0:
            inner = f'''<div class="abs t" style="left:190px;top:120px;font-size:400px;color:var(--amarelo);-webkit-text-stroke:8px {INK}">{i+1}</div>
              <div class="abs t" style="left:200px;top:620px;width:820px;font-size:92px">{tit}</div>
              <div class="abs" style="left:200px;top:780px;width:780px;font-size:44px;font-weight:700;line-height:1.3">{txt}</div>'''
        else:
            inner = f'''<div class="abs card" style="left:200px;top:220px;width:800px;padding:50px 50px 60px;transform:rotate({-1.5 if i==1 else 1.5}deg)">
                <div class="t" style="font-size:150px;color:var(--verde)">{i+1}.</div>
                <div class="t" style="font-size:86px;margin-top:10px">{tit}</div>
                <div style="font-size:42px;font-weight:700;line-height:1.3;margin-top:30px">{txt}</div></div>'''
        pages.append(page(f'''{caderno()}{inner}<div class="abs mini" style="left:200px;top:1250px;color:var(--txt2)">{i+1} / 5</div>'''))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--verde)"></div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:104px;color:#fff">Agora é só <span class="mt">montar.</span></div>
      <div class="abs card" style="left:80px;top:470px;width:920px;padding:44px 48px;font-size:42px;font-weight:800;line-height:1.35">
        Escreve as perguntas, manda o código da sala e a turma joga pelo celular. Sem baixar app.</div>
      <div class="abs" style="left:80px;top:860px"><span class="chip" style="font-size:38px;background:var(--amarelo)">Faça o seu. Teste grátis.</span></div>
      <div class="abs" style="left:80px;top:1060px">{logo('neg', 300)}</div>
      <div class="abs url" style="right:80px;top:1120px;color:#fff">quiddo.com.br</div>'''))
    piece(id='Q-C2', fmt='carrossel', day=5, slot='12h30', title='Como fazer um quiz que ninguém esquece', w=1080, h=1350,
          html=doc('Q-C2', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('5 regras para um quiz que ninguém esquece. 📒\n\n'
                   '1. Comece fácil.\n2. Uma pergunta, uma ideia.\n3. Misture os tipos.\n4. A difícil vai no meio.\n5. Feche com o pódio.\n\n'
                   'Salva para a próxima festa, aula ou resenha. E manda para quem sempre organiza.\n'
                   'Faça o seu, teste grátis: quiddo.com.br\n#quiz #professor #saladeaula #dinamicadegrupo #gincana #dicas #quiddo'),
          notes='Sala de aula: folha de caderno. Composições alternam número gigante e cartão.')

# =====================================================================================
# Q-R3 · Reel · Virada no último segundo (Espaço, escuro)
# =====================================================================================
def q_r3():
    T = 18.6
    tl = TL(T)
    stars = ''.join(f'<div class="abs" style="left:{(i*149)%1060+10}px;top:{(i*83)%1880+20}px;width:{6 if i%4 else 9}px;height:{6 if i%4 else 9}px;border-radius:50%;background:#fff;opacity:.8"></div>' for i in range(70))
    bg = f'<div class="abs" style="inset:0;background:#0B1033"></div>{stars}'
    players = [('Lua', 'boto.-.estrela.9', 4820), ('Caio', 'quati.bone.-.1', 4610), ('Nina', 'gato.coroa.-.6', 4400),
               ('Tati', 'tamandua.fone.redondos.2', 4390), ('Ju', 'mico.flor.-.7', 3900)]
    s1 = f'''<div {tl.scene(0, 2.9, fin=False)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:120px;color:#fff;{at(.05,'rise')}">Faltava 1 pergunta.</div>
      <div class="abs t" style="left:90px;top:720px;width:900px;font-size:120px;{at(.8,'pop')}"><span class="mt">A Tati estava em 4º.</span></div>
      <div class="abs" style="left:700px;top:1050px;{at(1.2,'drop')}">{av('tamandua.fone.redondos.2', 260)}</div>
    </div>'''
    def row(i, nome, k, pts, y, extra='', hl=False):
        return f'''<div class="abs" style="left:90px;width:900px;top:{y}px;height:150px;display:flex;align-items:center;gap:24px;background:{'var(--amarelo)' if hl else '#fff'};border:6px solid {INK};border-radius:30px;box-shadow:0 10px 0 {INK};padding:0 34px 0 18px;{extra}">
          <span class="t" style="font-size:56px;width:60px;text-align:center">{i}</span>{av(k, 112)}<span style="font-size:46px;font-weight:900;flex:1">{nome}</span><span class="t" style="font-size:56px">{pts:,}</span></div>'''.replace(',', '.') if False else f'''<div class="abs" style="left:90px;width:900px;top:{y}px;height:150px;display:flex;align-items:center;gap:24px;background:{'var(--amarelo)' if hl else '#fff'};border:6px solid {INK};border-radius:30px;box-shadow:0 10px 0 {INK};padding:0 34px 0 18px;{extra}">
          <span class="t" style="font-size:56px;width:60px;text-align:center">{i}</span>{av(k, 112)}<span style="font-size:46px;font-weight:900;flex:1">{nome}</span><span class="t" style="font-size:56px">{f"{pts:,}".replace(",", ".")}</span></div>'''
    rows = ''.join(row(i + 1, n, k, p, 520 + i * 180, at(3.0 + i * .12, 'slideR'), hl=(n == 'Tati')) for i, (n, k, p) in enumerate(players))
    s2 = f'''<div {tl.scene(2.9, 7.6)}>
      <div class="abs" style="left:90px;top:320px;{at(2.95,'pop')}"><span class="chip" style="background:var(--amarelo)">Placar · antes da pergunta 10</span></div>
      {rows}</div>'''
    q = f'''<div {tl.scene(7.6, 11.4)}>
      <div class="abs mini" style="left:90px;top:320px;color:var(--amarelo)">PERGUNTA 10 DE 10</div>
      <div class="abs t" style="left:90px;top:380px;width:900px;font-size:84px;color:#fff">Qual planeta tem o dia mais longo?</div>
      <div class="abs" style="left:90px;top:720px;width:900px;display:grid;grid-template-columns:1fr 1fr;gap:28px">
        <div style="{at(7.8,'pop')}">{resp(0,'Marte','height:150px')}</div>
        <div style="position:relative;{at(7.9,'pop')}">{resp(1,'Vênus','height:150px')}<div class="abs" style="inset:-14px;border:8px solid var(--amarelo);border-radius:38px;{at(9.6,'pop')}"></div></div>
        <div style="{at(8.0,'pop')}">{resp(2,'Júpiter','height:150px')}</div>
        <div style="{at(8.1,'pop')}">{resp(3,'Netuno','height:150px')}</div></div>
      <div class="abs card" style="left:90px;top:1140px;width:900px;padding:28px 34px;display:flex;align-items:center;gap:24px;{at(10.0,'rise')}">{av('tamandua.fone.redondos.2', 110)}<span style="font-size:38px;font-weight:900">Tati acertou em 1,2 s · +980</span></div>
      <div class="abs" style="left:90px;top:1360px;width:900px;font-size:30px;color:#fff;opacity:.85;{at(10.3,'fade')}">Um dia em Vênus dura mais que o ano de lá.</div>
    </div>'''
    # ranking depois: Tati sobe de 4º para 1º
    after = [('Tati', 'tamandua.fone.redondos.2', 5370), ('Lua', 'boto.-.estrela.9', 5290), ('Caio', 'quati.bone.-.1', 5010), ('Nina', 'gato.coroa.-.6', 4400), ('Ju', 'mico.flor.-.7', 4300)]
    before_pos = {'Lua': 0, 'Caio': 1, 'Nina': 2, 'Tati': 3, 'Ju': 4}
    mv = ''
    rows2 = ''
    for i, (n, k, p) in enumerate(after):
        b = before_pos[n]
        name = f'mv{n}'
        dy = (b - i) * 180
        mv += f'@keyframes {name}{{0%{{transform:translateY({dy}px)}}100%{{transform:translateY(0)}}}}'
        rows2 += row(i + 1, n, k, p, 520 + i * 180, f'animation:{name} .9s cubic-bezier(.34,1.3,.64,1) 12.0s 1 both;z-index:{5 if n=="Tati" else 1}', hl=(n == 'Tati'))
    crown = '<svg width="150" height="102" viewBox="-34 -26 68 46"><path d="M-26 12 L-29 -14 L-14 -1 L0 -20 L14 -1 L29 -14 L26 12Z" fill="#FFC83D" stroke="#0E2A22" stroke-width="4" stroke-linejoin="round"/><circle cx="0" cy="2" r="4" fill="#E5383B"/><circle cx="-15" cy="5" r="3" fill="#1E7FD6"/><circle cx="15" cy="5" r="3" fill="#13A07A"/></svg>'
    s4 = f'''<div {tl.scene(11.4, 15.4)}>
      <div class="abs" style="left:90px;top:320px"><span class="chip" style="background:var(--amarelo)">Placar final</span></div>
      {rows2}
      <div class="abs" style="left:150px;top:430px;--r:-12deg;{at(13.0,'drop')}">{crown}</div>
    </div>'''
    s5 = f'''<div {tl.scene(15.4, T, fout=False)}>
      <div class="abs t" style="left:0;right:0;top:420px;text-align:center;font-size:110px;color:#fff;{at(15.5,'rise')}">De 4º para 1º.</div>
      <div class="abs" style="left:300px;top:610px;--r:-6deg;{at(15.8,'stamp')}"><div class="t" style="background:var(--vermelho);color:#fff;border:7px solid {INK};padding:14px 40px;font-size:80px;box-shadow:0 10px 0 {INK}">Na Lua!</div></div>
      <div class="abs" style="left:240px;top:950px;{at(16.3,'pop')}">{logo('neg', 600)}</div>
      <div class="abs" style="left:0;right:0;top:1200px;text-align:center;{at(16.6,'rise')}"><span class="chip" style="font-size:38px;background:var(--amarelo)">Faça o seu. Teste grátis.</span></div>
      <div class="abs url" style="left:0;right:0;top:1330px;text-align:center;color:var(--amarelo);{at(16.8,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{bg}{s1}{s2}{q}{s4}{s5}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:#0B1033">{stars}
      <div class="abs" style="left:80px;top:80px">{logo('neg', 210)}</div>
      <div class="abs t" style="left:80px;top:270px;width:920px;font-size:112px;color:#fff">Faltava 1 pergunta. <span class="mt">Ela estava em 4º.</span></div>
      <div class="abs" style="left:620px;top:830px;transform:rotate(5deg)">{av('tamandua.fone.redondos.2', 340)}</div>
      <div class="abs" style="left:140px;top:900px">{mini('espaco', 300)}</div></div>'''
    piece(id='Q-R3', fmt='reel', day=7, slot='19h45', title='A virada no último segundo (Espaço)', total=T, poster=.7,
          html=doc('Q-R3', FONTS, CSS + tl.style() + mv, body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, '', '#0B1033'),
          caption=('Faltava uma pergunta. A Tati estava em 4º. 🚀\n\n'
                   'No Quiddo, quem acerta mais rápido ganha mais ponto. Por isso dá virada até na última pergunta.\n'
                   'E sim: um dia em Vênus dura mais que o ano de lá.\n\n'
                   'Monte o seu com o visual Espaço. Faça o seu, teste grátis: quiddo.com.br\n'
                   '#quiz #quizaovivo #espaco #astronomia #curiosidades #quiddo'),
          notes='Visual Espaço (selo "Na Lua!" é o carimbo oficial do pódio da cena lua). Áudio: plim na resposta, fanfarra na virada.')

# =====================================================================================
# Stories (5)
# =====================================================================================
def story(body, cls='', bg=''):
    return f'<section class="page {cls}" style="width:1080px;height:1920px;{bg}">{body}</section>'

def q_stories():
    out = []
    # S1 enquete
    out.append(('Q-S1', 1, 'Enquete: amigo secreto ou quiz?', story(f'''
      <div class="abs" style="left:80px;top:270px">{logo('cor', 230)}</div>
      <div class="abs t" style="left:80px;top:470px;width:920px;font-size:110px">Na confraternização deste ano vai ter…</div>
      <div class="abs" style="left:120px;top:1300px;transform:rotate(-6deg)">{av('onca.festa.-.2', 230)}</div>
      <div class="abs" style="left:730px;top:1300px;transform:rotate(6deg)">{av('capivara.laranja.escuros.7', 230)}</div>'''),
      'Enquete', 'Adesivo de ENQUETE no centro (y≈900–1200): "Amigo secreto" / "Quiz". Espaço livre já reservado.',
      'Story de enquete. Sem legenda de feed.'))
    # S2 caixa de perguntas
    out.append(('Q-S2', 2, 'Caixa: a pergunta que derruba a família', story(f'''
      <div class="abs t" style="left:80px;top:330px;width:920px;font-size:104px;color:var(--creme)">Mande uma pergunta que <span class="mt">derrubaria</span> a sua família no Natal.</div>
      <div class="abs" style="left:80px;top:1370px;width:920px;font-size:36px;color:var(--creme);opacity:.9">As melhores viram um quiz pronto aqui no perfil.</div>
      <div class="abs" style="left:760px;top:1480px;transform:rotate(8deg)">{av('peixeboi.gorro.-.9', 200)}</div>''', 'esc'),
      'Caixa de perguntas', 'Adesivo CAIXA DE PERGUNTAS em y≈950–1300.', 'Story. Sem legenda de feed.'))
    # S3 quiz sticker
    row = ''.join(av(k, 168) for k in ['capivara.bone.-.1', 'boto.-.-.9', 'onca.coroa.-.2', 'sapo.festa.-.4', 'tucano.-.escuros.5'])
    out.append(('Q-S3', 3, 'Quiz: quantos bichos tem no Quiddo?', story(f'''
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs" style="left:80px;top:290px"><span class="chip">Pergunta valendo ponto</span></div>
      <div class="abs t" style="left:80px;top:400px;width:920px;font-size:96px">Quantos bichos do Brasil tem no Quiddo?</div>
      <div class="abs" style="left:80px;top:1330px;width:920px;display:flex;justify-content:space-between">{row}</div>
      <div class="abs mini" style="left:80px;top:1530px;width:920px">A resposta sai na sexta, aqui nos stories.</div>'''),
      'Quiz', 'Adesivo QUIZ em y≈780–1230: 8 / 12 / 20 (correta) / 30.', 'v3 (você reprovou a v2 do intruso). Pergunta direta, valendo ponto, como no jogo. Nada se sobrepõe: título em cima, adesivo no meio, bichos embaixo.'))
    # S4 bastidor 13.200
    out.append(('Q-S4', 5, 'Bastidor: 13.200 jeitos de montar o bicho', story(f'''
      <div class="abs mini" style="left:80px;top:290px;color:var(--txt2)">BASTIDOR</div>
      <div class="abs t" style="left:80px;top:350px;width:920px;font-size:96px">De onde vêm os 13.200 bichos?</div>
      <div class="abs" style="left:80px;top:700px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:28px">
        <div class="card" style="padding:30px"><div class="t" style="font-size:96px;color:var(--verde)">20</div><div style="font-size:34px">bichos do Brasil</div></div>
        <div class="card" style="padding:30px"><div class="t" style="font-size:96px;color:var(--laranja)">× 11</div><div style="font-size:34px">chapéus (ou nenhum)</div></div>
        <div class="card" style="padding:30px"><div class="t" style="font-size:96px;color:var(--azul)">× 6</div><div style="font-size:34px">óculos e bigodes (ou nada)</div></div>
        <div class="card" style="padding:30px"><div class="t" style="font-size:96px;color:var(--vermelho)">× 10</div><div style="font-size:34px">cores de fundo</div></div></div>
      <div class="abs" style="left:80px;top:1290px;display:flex;gap:26px">{av('tatu.cartola.bigode.3',150)}{av('arara.coroa.coracao.4',150)}{av('caramelo.palha.escuros.8',150)}{av('jabuti.fone.estrela.5',150)}{av('bemtevi.faixa.-.0',150)}</div>'''),
      'Bastidor', 'Sem adesivo. Opcional: adesivo de link no rodapé.', 'Story editorial. 20 × 11 × 6 × 10 = 13.200 (contagem do código do site).'))
    # S5 link
    out.append(('Q-S5', 6, 'Link: crie o quiz da confraternização', story(f'''
      <div class="abs" style="inset:0;background:var(--verde)"></div>
      <div class="abs t" style="left:80px;top:330px;width:920px;font-size:112px;color:#fff">Sem ideia para a <span class="mt">confra?</span></div>
      <div class="abs card" style="left:80px;top:760px;width:920px;padding:40px 44px;font-size:44px;font-weight:800;line-height:1.3">Escreve as perguntas, manda o código, a turma joga pelo celular.</div>
      <div class="abs" style="left:80px;top:1080px"><span class="chip" style="font-size:44px;background:var(--amarelo)">Faça o seu. Teste grátis.</span></div>
      <div class="abs" style="left:300px;top:1440px">{logo('neg', 480)}</div>'''),
      'Link', 'Adesivo de LINK (quiddo.com.br) em y≈1200–1400.', 'Story de conversão leve.'))
    for sid, day, title, body, kind, sticker, notes in out:
        piece(id=sid, fmt='story', day=day, title=title, w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker=sticker, notes=notes, kind='story')


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


def build():
    q_r1(); q_c1(); q_r2(); q_c2(); q_r4(); q_r3(); q_stories()

build()
CTA = {
    'Q-S1': ('enquete', 880, ['Amigo secreto', 'Quiz'], 'Responde no direct: A ou B.'),
    'Q-S2': ('caixa', 1000, None, 'Manda a sua pergunta no direct.'),
    'Q-S3': ('quiz', 790, ['8', '12', '20', '30'], 'Chuta no direct. A resposta sai na sexta.'),
    'Q-S5': ('link', 1230, None, 'Link na bio · quiddo.com.br'),
}
C.apply_ctas(CTA, lambda i: {'bgs': ['#13A07A', '#FF7A1A', '#1E7FD6', '#E5383B'] if i != 'Q-S2' else ['#FFC83D'], 'fg': '#fff' if i not in ('Q-S2', 'Q-S5') else INK,
    'tfont': 'Fraunces', 'bfont': 'Nunito', 'border': f'6px solid {INK}', 'radius': '28px', 'shadow': f'0 10px 0 {INK}', 'tw': 900, 'fs': 50,
    'txt_color': '#FFF6E6' if i == 'Q-S2' else INK, 'ts': 40, 'ts_big': 56} if i != 'Q-S5' else
    {'bgs': ['#FFC83D'], 'fg': INK, 'tfont': 'Fraunces', 'bfont': 'Nunito', 'border': f'6px solid {INK}', 'radius': '999px', 'shadow': f'0 10px 0 {INK}', 'txt_color': INK, 'ts_big': 48})
