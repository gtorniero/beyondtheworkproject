"""Quiddo · Pack Semanal 03. Fraunces 900 + Nunito; creme/tinta/mata; contorno grosso e sombra dura.
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


CSS += """
.mtw{display:inline-block;background:#fff;color:var(--tinta);padding:0 .14em;margin:0 -.04em;transform:rotate(-2deg);border-radius:.08em}
@property --n{syntax:'<integer>';inherits:false;initial-value:0}
.cnt{counter-reset:c var(--n)}.cnt::after{content:counter(c)}
"""

def cta_fim(y, cor='var(--amarelo)'):
    return f'<span class="chip" style="font-size:38px;background:{cor}">Faça o seu. Teste grátis.</span>'


FONTS += C.font_face('DM Sans', 'DMSans-var.woff2', '400 800')

CSS += """
.tg{position:relative;width:300px;height:150px;border-radius:999px;border:7px solid var(--tinta);background:#9AA7A1;box-shadow:0 10px 0 var(--tinta)}
.tg .k{position:absolute;left:12px;top:12px;width:112px;height:112px;border-radius:50%;background:#fff;border:6px solid var(--tinta)}
@keyframes knob{to{transform:translateX(150px)}}
@keyframes trk{to{background:#13A07A}}
@keyframes bgflip{0%{opacity:0}100%{opacity:1}}
.zz{font-family:Fraunces,serif;font-weight:900;color:var(--creme);opacity:.8}
.nota{background:#FFE58A;border:6px solid var(--tinta);border-radius:18px;box-shadow:0 12px 0 var(--tinta);
  background-image:repeating-linear-gradient(transparent 0 66px,rgba(14,42,34,.18) 66px 69px);background-position:0 120px}
.caderno{background:#fff;border:6px solid var(--tinta);border-radius:24px;box-shadow:0 12px 0 var(--tinta);overflow:hidden;
  background-image:linear-gradient(90deg,transparent 118px,#E5383B 118px 122px,transparent 122px),repeating-linear-gradient(transparent 0 70px,#BFD8F2 70px 73px)}
.tag{position:relative;display:inline-block;background:var(--amarelo);color:var(--tinta);border:6px solid var(--tinta);border-radius:20px 20px 20px 20px;box-shadow:0 10px 0 var(--tinta);padding:26px 40px 26px 86px}
.tag::before{content:'';position:absolute;left:28px;top:50%;width:30px;height:30px;margin-top:-15px;border-radius:50%;background:var(--creme);border:5px solid var(--tinta)}
.carta{background:#fff;border:6px solid var(--tinta);border-radius:30px;box-shadow:0 12px 0 var(--tinta);color:var(--tinta)}
.rot{display:inline-block;background:var(--tinta);color:var(--creme);font-family:Nunito;font-weight:900;font-size:54px;padding:14px 30px;border-radius:16px}
"""

def toggle(on=False, t=None, size=1.0):
    """Interruptor desenhado pela marca. t = momento em que liga (anima)."""
    if t is None:
        trk = 'background:#13A07A' if on else ''
        kn = 'transform:translateX(150px)' if on else ''
    else:
        trk = f'animation:trk .3s linear {t:.2f}s 1 both'
        kn = f'animation:knob .35s cubic-bezier(.3,1.4,.5,1) {t:.2f}s 1 both'
    return f'<div class="tg" style="{trk};transform:scale({size});transform-origin:left center"><div class="k" style="{kn}"></div></div>'

# =====================================================================================
# Q-R7 · Reel trend · "Ligar/desligar": modo quiz da família ativado (seg 23/11, escuro)

# =====================================================================================
# S05 · 08–14/12/2026 (grade de dezembro: carrossel ter/qui/sáb/seg, reel qua/sex/dom)
# Animações um pouco mais lentas que no S03 (Gui, rodada 14: "levemente mais lentas no Quiddo").
# =====================================================================================
END_Q = C.PACKS / 'S04' / 'quiddo' / 'carrosseis' / 'Q-C12-7.png'   # card final de CTA aprovado (S04)
SLOW = 1.35  # fator das durações de entrada

def SC(tl, a, z):
    """Cena com corte seco; começa 1 quadro antes para nunca aparecer o fundo da página entre cenas."""
    return tl.scene(max(0, a - .04), z, fin=False, fout=False)

def sat(t, anim='pop', extra=''):
    d = {'pop': .42, 'rise': .45, 'drop': .55, 'fade': .3, 'stamp': .5, 'slideL': .45, 'slideR': .45, 'grow': .9}.get(anim, .45) * SLOW
    return at(t, anim, d, extra)

CSS += """
.q5card{background:#fff;border:6px solid var(--tinta);border-radius:34px;box-shadow:0 12px 0 var(--tinta)}
.num{font-family:Fraunces,serif;font-weight:900;line-height:1}
.selo5{display:inline-block;font-family:Nunito;font-weight:900;font-size:30px;letter-spacing:.04em;text-transform:uppercase;padding:10px 22px;border-radius:12px;background:var(--tinta);color:var(--amarelo)}
.mapa{background:#BFE6D6;border:6px solid var(--tinta);border-radius:34px;box-shadow:0 12px 0 var(--tinta);
  background-image:radial-gradient(circle at 20% 30%,rgba(19,160,122,.35) 0 90px,transparent 91px),radial-gradient(circle at 75% 70%,rgba(19,160,122,.3) 0 120px,transparent 121px)}
.pin{width:64px;height:64px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);border:6px solid var(--tinta);background:var(--vermelho)}
.prato{width:300px;height:300px;border-radius:50%;background:#fff;border:7px solid var(--tinta);box-shadow:0 10px 0 var(--tinta),inset 0 0 0 26px #FFF6E6}
.telao{background:var(--tinta);border-radius:30px;padding:22px;box-shadow:0 14px 0 rgba(0,0,0,.25)}
.telao .in{background:var(--creme);border-radius:18px;overflow:hidden;position:relative}
"""

def opcoes(opts, ok=None, fs=40, h=130, cols=2, t0=None):
    out = ''
    for j, o in enumerate(opts):
        st = f'height:{h}px;font-size:{fs}px;'
        if ok is not None and j != ok: st += 'opacity:.35;filter:grayscale(.6);'
        if t0 is not None: st += sat(t0 + j * .15, 'pop')
        chk = '<span style="margin-left:auto;font-size:52px">✓</span>' if ok is not None and j == ok else ''
        out += resp(j, o, st, chk)
    return f'<div style="display:grid;grid-template-columns:{"1fr 1fr" if cols == 2 else "1fr"};gap:24px">{out}</div>'

def podio(bichos, size=170, base=True):
    """Pódio com bichos do site (1º no meio)."""
    hs = [230, 320, 170]; ordem = [1, 0, 2]
    cols = ''
    for k, i in enumerate(ordem):
        b = bichos[i]
        cols += (f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end">{av(b, size)}'
                 f'<div style="width:{size + 30}px;height:{hs[k]}px;margin-top:-6px;border:6px solid var(--tinta);border-radius:18px 18px 0 0;'
                 f'background:{["var(--laranja)", "var(--amarelo)", "var(--azul)"][k]};display:flex;justify-content:center;padding-top:18px">'
                 f'<span class="num" style="font-size:80px;color:var(--tinta)">{i + 1}</span></div></div>')
    return f'<div style="display:flex;gap:16px;align-items:flex-end;justify-content:center">{cols}</div>'

# -------------------------------------------------------------------------------------
# Q-C13 · Carrossel (ter 08/12) · Quiz de Ciências: 5 perguntas pra última semana de aula (escola)
# -------------------------------------------------------------------------------------
CIENCIAS = [
    ('Qual é o único mamífero que voa de verdade?', ['Morcego', 'Esquilo', 'Pinguim', 'Avestruz'], 0, 'morcego'),
    ('Que gás as plantas tiram do ar para fazer fotossíntese?', ['Oxigênio', 'Gás carbônico', 'Nitrogênio', 'Hélio'], 1, ''),
    ('Qual é o maior órgão do corpo humano?', ['Fígado', 'Pele', 'Coração', 'Cérebro'], 1, ''),
    ('Ao nível do mar, a água ferve a quantos graus Celsius?', ['50 °C', '80 °C', '100 °C', '120 °C'], 2, ''),
    ('Qual planeta é chamado de "planeta vermelho"?', ['Júpiter', 'Vênus', 'Marte', 'Saturno'], 2, ''),
]

def q_c13():
    bich = ['coruja.-.redondos.6', 'sapo.-.escuros.4', 'tatu.fone.-.3', 'gato.bone.-.6', 'arara.-.estrela.2']
    pages = [page(f'''
      <div class="abs caderno" style="left:60px;top:60px;width:960px;height:1230px;transform:rotate(1deg)">
        <div class="abs" style="left:160px;top:64px"><span class="chip" style="background:var(--verde);color:#fff">Quiz de Ciências</span></div>
        <div class="abs t" style="left:160px;top:190px;width:760px;font-size:100px">5 perguntas pra última semana de <span class="mt">aula.</span></div>
        <div class="abs" style="left:160px;top:640px;transform:rotate(-6deg)">{av('coruja.-.redondos.6', 280)}</div>
        <div class="abs" style="left:470px;top:700px;transform:rotate(5deg)">{av('sapo.-.escuros.4', 250)}</div>
        <div class="abs" style="left:700px;top:760px;transform:rotate(-3deg)">{av('tatu.fone.-.3', 210)}</div>
        <div class="abs mini" style="left:160px;top:1100px;color:var(--txt2)">Gabarito no fim. Professor: salva pra revisão.</div>
      </div>''', cls='')]
    for i, (q, opts, ok, _) in enumerate(CIENCIAS):
        bg = 'var(--amarelo)' if i % 2 == 0 else 'var(--mata)'
        pages.append(page(f'''
          <div class="abs" style="inset:0;background:{bg}"></div>
          <div class="abs q5card" style="left:70px;top:90px;width:940px;height:1150px;transform:rotate({-1 if i % 2 else 1}deg)">
            <div class="abs" style="left:50px;top:46px"><span class="chip" style="background:var(--verde);color:#fff">Ciências · {i + 1} de 5</span></div>
            <div class="abs" style="right:40px;top:-70px;transform:rotate(8deg)">{av(bich[i], 190)}</div>
            <div class="abs t" style="left:50px;top:200px;width:840px;font-size:{80 if len(q) < 44 else 70}px">{q}</div>
            <div class="abs" style="left:50px;top:620px;width:840px">{opcoes(opts)}</div>
            <div class="abs" style="left:50px;top:1010px;font-size:36px;font-weight:900;color:var(--txt2)">Responde de cabeça. Gabarito no último card.</div>
          </div>'''))
    gab = ''.join(f'<div style="display:flex;align-items:center;gap:26px;padding:20px 0;border-bottom:5px dashed rgba(14,42,34,.25)">'
                  f'<span class="num" style="font-size:64px;width:60px">{i + 1}</span>{resp(ok, opts[ok], "flex:1;height:110px;font-size:40px")}</div>'
                  for i, (q, opts, ok, _) in enumerate(CIENCIAS))
    pages.append(page(f'''
      <div class="abs caderno" style="left:60px;top:60px;width:960px;height:1230px;transform:rotate(-1deg)">
        <div class="abs t" style="left:160px;top:70px;font-size:96px">Gabarito</div>
        <div class="abs" style="left:160px;top:210px;width:740px">{gab}</div>
        <div class="abs" style="left:160px;top:1080px;font-size:38px;font-weight:900">Quantas a turma acertou? Manda pra um professor.</div>
      </div>'''))
    pages.append(C.endcard(END_Q))
    piece(id='Q-C13', fmt='carrossel', day=1, slot='12h30', title='Quiz de Ciências: 5 perguntas pra última semana de aula', kind='engajamento', w=1080, h=1350,
          html=doc('Q-C13', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Última semana de aula: a revisão de Ciências pode virar jogo. 🔬\n'
                   '5 perguntas com gabarito no fim. Quantas você acerta sem pesquisar?\n\n'
                   'Manda pra um professor (ou pro grupo da turma) 👇\n'
                   'No Quiddo, a turma responde pelo celular e o pódio sai no telão.\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#quiddo #professor #saladeaula #ciencias #quiz #revisao'),
          notes='Versão de escola por matéria (pedido do Gui no Q-C11, rodada 18). Perguntas conferidas (morcego é o único mamífero com voo verdadeiro; fotossíntese usa gás carbônico; pele é o maior órgão; água ferve a 100 °C ao nível do mar; Marte). Card final = CTA aprovado do S04 (Q-C12-7). Motivo de envio: mandar pra professor.')

# -------------------------------------------------------------------------------------
# Q-R17 · Reel MEME (qua 09/12) · Os 4 tipos de jogador no quiz de fim de ano
# -------------------------------------------------------------------------------------
def q_r17():
    T = 15.0; tl = TL(T)
    tipos = [('O relâmpago', 'Responde antes de terminar de ler.', 'onca.-.escuros.2', 'var(--laranja)', 'A'),
             ('O advogado', '"Essa pergunta tá errada."', 'coruja.cartola.redondos.6', 'var(--azul)', 'B'),
             ('O sortudo', 'Chuta tudo. Acerta tudo.', 'capivara.flor.-.1', 'var(--verde)', 'C'),
             ('O da revanche', '"Mais uma rodada. Só mais uma."', 'tucano.festa.-.5', 'var(--vermelho)', 'D')]
    s0 = f'''<div {SC(tl, 0, 2.4)}>
      <div class="abs" style="inset:0;background:var(--tinta)"></div>
      <div class="abs" style="left:90px;top:520px;{sat(.1,'fade')}"><span class="chip" style="background:var(--amarelo)">Quiz de fim de ano</span></div>
      <div class="abs t" style="left:90px;top:640px;width:900px;font-size:118px;color:var(--creme);{sat(.3,'rise')}">Os 4 tipos de <span class="mt">jogador.</span></div>
      <div class="abs" style="left:90px;top:1060px;font-size:46px;font-weight:800;color:var(--creme);{sat(.9,'fade')}">Qual é você?</div>
    </div>'''
    scenes = ''
    for i, (nome, frase, b, cor, letra) in enumerate(tipos):
        a, z = 2.4 + i * 2.5, 2.4 + (i + 1) * 2.5
        scenes += f'''<div {SC(tl, a, z)}>
          <div class="abs" style="inset:0;background:{cor}"></div>
          <div class="abs" style="left:90px;top:300px;{sat(a + .05,'fade')}"><span class="selo5">Tipo {i + 1} de 4</span></div>
          <div class="abs" style="left:0;right:0;top:420px;display:flex;justify-content:center;--r:{-5 if i % 2 else 5}deg;{sat(a + .1,'drop')}">{av(b, 520)}</div>
          <div class="abs card" style="left:90px;top:1000px;width:900px;padding:34px 44px;{sat(a + .35,'rise')}">
            <div class="t" style="font-size:96px">{nome}</div>
            <div style="font-size:50px;font-weight:900;margin-top:14px;color:var(--txt2)">{frase}</div></div>
        </div>'''
    e = 2.4 + 4 * 2.5
    s9 = f'''<div {SC(tl, e, T)}>
      <div class="abs" style="inset:0;background:var(--creme)"></div>
      <div class="abs" style="left:90px;top:360px;width:900px;display:flex;justify-content:space-between">{''.join(f'<div style="--r:{(-1) ** k * 6}deg;{sat(e + k * .12,"pop")}">{av(t[2], 200)}</div>' for k, t in enumerate(tipos))}</div>
      <div class="abs t" style="left:90px;top:640px;width:900px;font-size:92px;{sat(e + .5,'rise')}">Marca o seu tipo <span class="mt">(e o do tio).</span></div>
      <div class="abs" style="left:90px;top:1010px;{sat(e + 1.0,'pop')}">{logo('cor', 420)}</div>
      <div class="abs" style="left:90px;top:1200px;transform:scale(1.35);transform-origin:left top;{sat(e + 1.2,'rise')}">{cta_fim(0)}</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{scenes}{s9}</section>'
    grid = ''.join(f'<div style="background:{t[3]};border:6px solid var(--tinta);border-radius:30px;box-shadow:0 10px 0 var(--tinta);height:430px;position:relative;overflow:hidden">'
                   f'<div style="position:absolute;left:0;right:0;top:20px;display:flex;justify-content:center">{av(t[2], 270)}</div>'
                   f'<div style="position:absolute;left:20px;bottom:20px"><span class="t" style="display:inline-block;background:#fff;border:5px solid {INK};border-radius:14px;padding:6px 16px;font-size:46px">{t[0]}</span></div></div>' for t in tipos)
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:var(--tinta)">
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:100px;color:var(--creme)">Os 4 tipos de <span class="mt">jogador.</span></div>
      <div class="abs" style="left:80px;top:330px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:28px">{grid}</div></div>'''
    piece(id='Q-R17', fmt='reel', day=2, slot='19h45', title='Meme: os 4 tipos de jogador no quiz de fim de ano', total=T, poster=.3, kind='meme',
          music='S03/quiddo/reels/Q-R15.mp4',
          html=doc('Q-R17', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, '', 'var(--tinta)'),
          caption=('Os 4 tipos de jogador no quiz de fim de ano. 🏆\n'
                   'O relâmpago, o advogado, o sortudo e o da revanche. Todo grupo tem os quatro.\n\n'
                   'Marca o seu tipo nos comentários e manda pro grupo que vai jogar esse fim de ano 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#quiddo #quiz #fimdeano #confraternizacao #meme'),
          notes='Meme de tipologia (formato "os X tipos"), com os bichos do site. Ideia nova: Q-R2 era "que bicho você seria"; aqui é o jeito de jogar. Música de banco (Mixkit) do Q-R15 aprovado, com entrada e saída suaves (sem corte seco). Motivo de envio: marcar o próprio tipo e o do amigo.')

# -------------------------------------------------------------------------------------
# Q-C14 · Carrossel (qui 10/12) · Quiz da viagem de férias: em que estado fica?
# -------------------------------------------------------------------------------------
DESTINOS = [
    ('Fernando de Noronha', ['Pernambuco', 'Paraíba', 'Rio Grande do Norte', 'Bahia'], 0),
    ('Lençóis Maranhenses', ['Piauí', 'Maranhão', 'Ceará', 'Pará'], 1),
    ('Cataratas do Iguaçu (lado brasileiro)', ['Santa Catarina', 'Mato Grosso do Sul', 'Paraná', 'São Paulo'], 2),
    ('Bonito, das águas cristalinas', ['Goiás', 'Mato Grosso', 'Tocantins', 'Mato Grosso do Sul'], 3),
    ('Chapada Diamantina', ['Bahia', 'Minas Gerais', 'Goiás', 'Sergipe'], 0),
]

def q_c14():
    pins = [(150, 120), (560, 90), (380, 330), (720, 300), (230, 470)]
    pins_html = ''.join(f'<div class="abs pin" style="left:{x}px;top:{y}px"></div>' for x, y in pins)
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--ceu)"></div>
      <div class="abs mapa" style="left:70px;top:430px;width:940px;height:620px;transform:rotate(-1.5deg)">{pins_html}</div>
      <div class="abs" style="left:80px;top:70px"><span class="chip" style="background:var(--amarelo)">Quiz da viagem</span></div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:96px">Em que estado fica? <span class="mt">5 destinos.</span></div>
      <div class="abs" style="left:700px;top:330px;transform:rotate(6deg)">{av('arara.palha.escuros.4', 240)}</div>
      <div class="abs" style="left:80px;top:1130px;width:900px;font-size:40px;font-weight:900">Pra jogar no carro, no ônibus ou na fila do aeroporto.</div>''')]
    for i, (lugar, opts, ok) in enumerate(DESTINOS):
        dark = i % 2 == 1
        pages.append(page(f'''
          <div class="abs" style="inset:0;background:{'var(--mata)' if dark else 'var(--creme)'}"></div>
          <div class="abs" style="left:80px;top:70px"><span class="chip">Destino {i + 1} de 5</span></div>
          <div class="abs" style="left:80px;top:190px;font-size:44px;font-weight:900;color:{'var(--creme)' if dark else 'var(--txt2)'}">Em que estado fica…</div>
          <div class="abs q5card" style="left:80px;top:270px;width:920px;padding:40px 46px;transform:rotate({1 if dark else -1}deg)">
            <div style="display:flex;align-items:center;gap:26px"><div class="pin" style="flex:none"></div><div class="t" style="font-size:{84 if len(lugar) < 22 else 66}px">{lugar}?</div></div></div>
          <div class="abs" style="left:80px;top:{560 if len(lugar) < 22 else 600}px;width:920px">{opcoes(opts, fs=38, h=140)}</div>
          <div class="abs" style="right:90px;top:930px;transform:rotate({-7 if dark else 7}deg)">{av(['tucano.palha.-.5', 'jabuti.bone.-.3', 'quati.palha.redondos.4', 'peixeboi.-.escuros.1', 'tatu.palha.-.2'][i], 220)}</div>
          <div class="abs" style="left:80px;top:1150px;font-size:38px;font-weight:900;color:{'var(--amarelo)' if dark else 'var(--tinta)'}">Resposta no último card →</div>'''))
    gab = ''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:22px 0;border-bottom:5px dashed rgba(14,42,34,.25)">'
                  f'<span style="font-size:40px;font-weight:900">{l}</span><span class="t" style="font-size:52px;color:var(--mata)">{o[k]}</span></div>' for l, o, k in DESTINOS)
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs q5card" style="left:70px;top:80px;width:940px;height:1180px;padding:50px 56px">
        <div class="t" style="font-size:92px">Respostas</div>
        <div style="margin-top:30px">{gab}</div>
        <div style="margin-top:46px;font-size:40px;font-weight:900">Quem acertou as 5 escolhe a música da viagem.</div>
      </div>'''))
    pages.append(C.endcard(END_Q))
    piece(id='Q-C14', fmt='carrossel', day=3, slot='12h30', title='Quiz da viagem: em que estado fica? (5 destinos)', kind='engajamento', w=1080, h=1350,
          html=doc('Q-C14', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Quiz da viagem de férias: em que estado fica? 🗺️\n'
                   'Fernando de Noronha, Lençóis Maranhenses, Cataratas do Iguaçu, Bonito e Chapada Diamantina. Respostas no último card.\n\n'
                   'Manda no grupo da viagem e vê quem acerta as 5 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#quiddo #ferias #viagem #quiz #brasil'),
          notes='Tema novo (férias e viagem). Conferido: Noronha (PE), Lençóis (MA), Cataratas, lado brasileiro (PR), Bonito (MS), Chapada Diamantina (BA). Mapa abstrato desenhado (sem mapa real). Card final = CTA aprovado do S04. Motivo de envio: grupo da viagem.')

# -------------------------------------------------------------------------------------
# Q-R18 · Reel MEME (sex 11/12) · Tradução simultânea do quiz da família
# -------------------------------------------------------------------------------------
def q_r18():
    T = 15.0; tl = TL(T)
    pares = [('"Lê a pergunta de novo?"', 'Não faço ideia.', 'jabuti.palha.-.3'),
             ('"Essa tava difícil."', 'Errei.', 'preguica.-.redondos.2'),
             ('"O celular travou."', 'Errei de novo.', 'quati.bone.-.4'),
             ('"Quem escreveu essa pergunta?"', 'Fui eu. E errei.', 'tamandua.gorro.-.7')]
    s0 = f'''<div {SC(tl, 0, 2.3)}>
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs t" style="left:90px;top:560px;width:900px;font-size:116px;{sat(.1,'rise')}">Tradução simultânea do quiz da <span class="mtw">família.</span></div>
    </div>'''
    sc = ''
    for i, (diz, trad, b) in enumerate(pares):
        a, z = 2.3 + i * 2.6, 2.3 + (i + 1) * 2.6
        sc += f'''<div {SC(tl, a, z)}>
          <div class="abs" style="inset:0;background:{'var(--creme)' if i % 2 == 0 else '#fff'}"></div>
          <div class="abs" style="left:90px;top:320px;--r:{-4 if i % 2 else 4}deg;{sat(a + .05,'pop')}">{av(b, 300)}</div>
          <div class="abs" style="left:90px;top:680px;{sat(a + .15,'fade')}"><span class="selo5">O que dizem</span></div>
          <div class="abs t" style="left:90px;top:770px;width:900px;font-size:96px;{sat(a + .25,'rise')}">{diz}</div>
          <div class="abs" style="left:90px;top:1110px;{sat(a + 1.0,'fade')}"><span class="selo5" style="background:var(--vermelho);color:#fff">Tradução</span></div>
          <div class="abs" style="left:90px;top:1200px;--r:-2deg;{sat(a + 1.1,'stamp')}"><span class="t" style="display:inline-block;background:var(--tinta);color:var(--amarelo);padding:16px 34px;font-size:86px;border-radius:14px">{trad}</span></div>
        </div>'''
    e = 2.3 + 4 * 2.6
    s9 = f'''<div {SC(tl, e, T)}>
      <div class="abs" style="inset:0;background:var(--tinta)"></div>
      <div class="abs" style="left:0;right:0;top:300px;{sat(e + .1,'pop')}">{podio(['tamandua.gorro.-.7', 'jabuti.palha.-.3', 'quati.bone.-.4'], 160)}</div>
      <div class="abs t" style="left:90px;top:900px;width:900px;font-size:84px;color:var(--creme);text-align:center;{sat(e + .5,'rise')}">No pódio, ninguém precisa de tradução.</div>
      <div class="abs" style="left:0;right:0;top:1180px;text-align:center;{sat(e + 1.0,'rise')}">{cta_fim(0)}</div>
      <div class="abs url" style="left:0;right:0;top:1310px;text-align:center;color:var(--amarelo);{sat(e + 1.2,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{sc}{s9}</section>'
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:var(--amarelo)">
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:96px">Tradução simultânea do quiz da <span class="mtw">família.</span></div>
      <div class="abs card" style="left:80px;top:560px;width:920px;padding:36px 44px;transform:rotate(-1.5deg)">
        <div class="selo5">O que dizem</div><div class="t" style="font-size:72px;margin-top:16px">"O celular travou."</div>
        <div class="selo5" style="background:var(--vermelho);color:#fff;margin-top:30px">Tradução</div><div class="t" style="font-size:72px;margin-top:16px">Errei.</div></div>
      <div class="abs" style="left:700px;top:1010px;transform:rotate(8deg)">{av('quati.bone.-.4', 280)}</div></div>'''
    piece(id='Q-R18', fmt='reel', day=4, slot='19h45', title='Meme: tradução simultânea do quiz da família', total=T, poster=.45, kind='meme',
          music='S03/quiddo/reels/Q-R16.mp4',
          html=doc('Q-R18', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, '', 'var(--amarelo)'),
          caption=('Tradução simultânea do quiz da família. 😅\n'
                   '"O celular travou" = errei. "Quem escreveu essa pergunta?" = fui eu, e errei.\n\n'
                   'Manda no grupo da família e marca quem fala "o celular travou" 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#quiddo #familia #natal #quiz #meme'),
          notes='Meme "o que dizem × tradução" (formato novo para o Quiddo). Natal só na hashtag (dezembro, liberado). Música de banco do Q-R16 aprovado, com fade de saída. Motivo de envio: marcar o parente.')

# -------------------------------------------------------------------------------------
# Q-C15 · Carrossel (sáb 12/12) · Quiz da ceia: de onde vem cada prato?
# -------------------------------------------------------------------------------------
CEIA = [
    ('Panetone', 'O panetone nasceu em qual país?', ['Itália', 'França', 'Alemanha', 'Portugal'], 0, 'Nasceu em Milão, no norte da Itália.'),
    ('Bacalhau', 'O bacalhau na ceia é herança de qual país?', ['Noruega', 'Espanha', 'Portugal', 'Itália'], 2, 'O peixe é pescado no Atlântico Norte, mas o costume veio de Portugal.'),
    ('Peru', 'O peru é uma ave nativa de qual lugar?', ['Europa', 'América do Norte', 'África', 'Ásia'], 1, 'É nativo da América do Norte.'),
    ('Rabanada', 'A rabanada de Natal chegou ao Brasil por influência de…', ['Portugal', 'Itália', 'Estados Unidos', 'Japão'], 0, 'Em Portugal ela também é doce de Natal.'),
]

def q_c15():
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--vermelho)"></div>
      <div class="abs" style="left:80px;top:70px"><span class="chip" style="background:var(--amarelo)">Quiz da ceia</span></div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:104px;color:#fff">De onde vem cada <span class="mt">prato?</span></div>
      <div class="abs" style="left:110px;top:640px"><div class="prato"></div></div>
      <div class="abs" style="left:150px;top:560px;transform:rotate(-8deg)">{av('peixeboi.gorro.-.1', 240)}</div>
      <div class="abs" style="left:560px;top:620px;transform:rotate(7deg)">{av('mico.gorro.estrela.7', 300)}</div>
      <div class="abs" style="left:80px;top:1130px;font-size:42px;font-weight:900;color:#fff">4 perguntas pra jogar antes de servir.</div>''')]
    for i, (prato, q, opts, ok, info) in enumerate(CEIA):
        light = i % 2 == 0
        pages.append(page(f'''
          <div class="abs" style="inset:0;background:{'var(--creme)' if light else 'var(--mata)'}"></div>
          <div class="abs" style="left:80px;top:70px"><span class="chip">Prato {i + 1} de 4 · {prato}</span></div>
          <div class="abs t" style="left:80px;top:190px;width:920px;font-size:{78 if len(q) < 40 else 68}px;color:{'var(--tinta)' if light else 'var(--creme)'}">{q}</div>
          <div class="abs" style="left:80px;top:560px;width:920px">{opcoes(opts, fs=40, h=140)}</div>
          <div class="abs q5card" style="left:80px;top:930px;width:920px;padding:28px 36px;transform:rotate(180deg)">
            <div style="font-size:34px;font-weight:900;color:var(--txt2)">Resposta: {"ABCD"[ok]} · {opts[ok]}. {info}</div></div>
          <div class="abs" style="left:80px;top:1150px;font-size:34px;font-weight:900;color:{'var(--txt2)' if light else 'var(--amarelo)'}">A resposta está de cabeça pra baixo.</div>'''))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs t" style="left:80px;top:90px;width:920px;font-size:96px">E a farofa?</div>
      <div class="abs t" style="left:80px;top:220px;width:920px;font-size:96px"><span class="mtw">Brasil, claro.</span></div>
      <div class="abs" style="left:0;right:0;top:470px">{podio(['peixeboi.gorro.-.1', 'mico.gorro.estrela.7', 'capivara.gorro.-.2'], 170)}</div>
      <div class="abs" style="left:80px;top:1110px;width:920px;font-size:40px;font-weight:900">Manda no grupo da família antes da ceia.</div>'''))
    pages.append(C.endcard(END_Q))
    piece(id='Q-C15', fmt='carrossel', day=5, slot='12h30', title='Quiz da ceia: de onde vem cada prato?', kind='engajamento', w=1080, h=1350,
          html=doc('Q-C15', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Quiz da ceia: de onde vem cada prato? 🎄\n'
                   'Panetone, bacalhau, peru e rabanada. A resposta está de cabeça pra baixo em cada card.\n\n'
                   'Manda no grupo da família e joga antes de servir 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#quiddo #natal #ceiadenatal #familia #quiz'),
          notes='Natal liberado (dezembro). Conferido: panetone de Milão; bacalhau na ceia como herança portuguesa (peixe do Atlântico Norte); peru nativo da América do Norte; rabanada de Natal também em Portugal. Prato desenhado sem comida realista. Card final = CTA aprovado do S04. Motivo de envio: grupo da família antes da ceia.')

# -------------------------------------------------------------------------------------
# Q-R19 · Reel TREND antes × depois (dom 13/12) · Encontro de fim de ano dos amigos
# -------------------------------------------------------------------------------------
def q_r19():
    T = 15.0; tl = TL(T)
    papo = ['"E o trabalho?"', '"Tudo certo."', '"E você?"', '"Também."']
    balao = ''.join(f'<div class="abs" style="left:{110 + (k % 2) * 330}px;top:{760 + k * 130}px;{sat(.8 + k * .55,"pop")}"><span style="display:inline-block;background:#fff;color:var(--tinta);border:5px solid #9AA7A1;border-radius:30px;padding:16px 34px;font-size:56px;font-weight:800">{t}</span></div>' for k, t in enumerate(papo))
    s1 = f'''<div {SC(tl, 0, 5.4)}>
      <div class="abs" style="inset:0;background:#3B4A45"></div>
      <div class="abs" style="left:90px;top:300px;{sat(.05,'fade')}"><span class="selo5" style="background:#9AA7A1;color:var(--tinta);font-size:40px">Antes</span></div>
      <div class="abs t" style="left:90px;top:410px;width:900px;font-size:88px;color:#D9DED9;{sat(.2,'rise')}">Encontro de fim de ano, minuto 20: papo de elevador.</div>
      {balao}
      <div class="abs" style="left:640px;top:1250px;opacity:.55;filter:grayscale(1)">{av('preguica.-.-.2', 260)}</div>
    </div>'''
    s2 = f'''<div {SC(tl, 5.4, 11.8)}>
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs" style="left:90px;top:300px;{sat(5.45,'stamp')}"><span class="selo5" style="font-size:40px">Depois</span></div>
      <div class="abs card" style="left:90px;top:420px;width:900px;padding:32px 40px;{sat(5.7,'pop')}"><div class="mini" style="color:var(--txt2)">PERGUNTA 3 · SOBRE O GRUPO</div>
        <div class="t" style="font-size:70px;margin-top:8px">Quem do grupo já dormiu no cinema?</div></div>
      <div class="abs" style="left:90px;top:760px;width:900px">{opcoes(['Bia', 'Caio', 'Lu', 'Todo mundo'], fs=46, h=130, t0=6.4)}</div>
      <div class="abs" style="left:90px;top:1110px;width:900px;display:flex;justify-content:space-between">{''.join(f'<div style="--r:{(-1) ** k * 7}deg;{sat(8.2 + k * .15,"drop")}">{av(b, 190)}</div>' for k, b in enumerate(['preguica.festa.-.2', 'gato.coroa.-.6', 'sapo.festa.escuros.4', 'boto.gorro.-.3']))}</div>
      <div class="abs t" style="left:90px;top:1380px;font-size:64px;{sat(9.6,'rise')}">47 minutos de risada.</div>
    </div>'''
    s3 = f'''<div {SC(tl, 11.8, T)}>
      <div class="abs" style="inset:0;background:var(--tinta)"></div>
      <div class="abs" style="left:240px;top:520px;{sat(11.9,'pop')}">{logo('neg', 600)}</div>
      <div class="abs t" style="left:90px;right:90px;top:820px;text-align:center;font-size:66px;color:var(--creme);{sat(12.3,'rise')}">Perguntas sobre o seu grupo, no celular de cada um.</div>
      <div class="abs" style="left:0;right:0;top:1090px;text-align:center;{sat(12.8,'rise')}">{cta_fim(0)}</div>
      <div class="abs url" style="left:0;right:0;top:1220px;text-align:center;color:var(--amarelo);{sat(13.0,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:var(--amarelo)">
      <div class="abs" style="left:0;top:0;width:540px;height:1350px;background:#3B4A45"></div>
      <div class="abs" style="left:60px;top:80px"><span class="selo5" style="background:#9AA7A1;color:var(--tinta)">Antes</span></div>
      <div class="abs" style="left:600px;top:80px"><span class="selo5">Depois</span></div>
      <div class="abs t" style="left:60px;top:200px;width:440px;font-size:70px;color:#D9DED9">"E o trabalho?"</div>
      <div class="abs t" style="left:600px;top:200px;width:430px;font-size:70px">Quem já dormiu no cinema?</div>
      <div class="abs" style="left:110px;top:760px;opacity:.55;filter:grayscale(1)">{av('preguica.-.-.2', 330)}</div>
      <div class="abs" style="left:650px;top:740px;transform:rotate(8deg)">{av('preguica.festa.-.2', 340)}</div>
      <div class="abs" style="left:60px;top:1180px;font-size:40px;font-weight:900;color:#fff">Encontro de fim de ano</div></div>'''
    piece(id='Q-R19', fmt='reel', day=6, slot='19h45', title='Trend antes × depois: o encontro de fim de ano dos amigos', total=T, poster=.55, kind='trend',
          music='S04/quiddo/reels/Q-R13.mp4',
          html=doc('Q-R19', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, '', 'var(--amarelo)'),
          caption=('Encontro de fim de ano dos amigos. Antes: "e o trabalho?", "tudo certo". 😐\n'
                   'Depois: "quem do grupo já dormiu no cinema?" e 47 minutos de risada.\n\n'
                   'Manda no grupo dos amigos e já escolhe a primeira pergunta 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#quiddo #amigos #fimdeano #quiz #antesedepois'),
          notes='Trend "antes × depois" (doc de trends do DOT, 06/11; circulação no Brasil sem validação). Público novo para o Quiddo: amigos. Antes cinza, depois amarelo da marca. Nomes de exemplo nas opções. Música de banco do Q-R13 aprovado (S04), com fade de saída.')

# -------------------------------------------------------------------------------------
# Q-C16 · Carrossel (seg 14/12) · Quiz de Matemática: 5 contas de cabeça (escola)
# -------------------------------------------------------------------------------------
MATE = [('7 × 8', ['54', '56', '58', '64'], 1), ('15% de 200', ['15', '20', '30', '35'], 2),
        ('Quantos segundos tem 1 hora?', ['360', '600', '3.600', '6.000'], 2),
        ('Qual é o próximo número primo depois do 7?', ['9', '11', '13', '15'], 1), ('2³ (dois ao cubo)', ['6', '8', '9', '12'], 1)]

def q_c16():
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--azul)"></div>
      <div class="abs caderno" style="left:60px;top:60px;width:960px;height:1230px;transform:rotate(-1deg);background-image:linear-gradient(90deg,transparent 118px,#E5383B 118px 122px,transparent 122px),linear-gradient(#DCEBFA 3px,transparent 3px),linear-gradient(90deg,#DCEBFA 3px,transparent 3px);background-size:auto,60px 60px,60px 60px">
        <div class="abs" style="left:160px;top:64px"><span class="chip" style="background:var(--azul);color:#fff">Quiz de Matemática</span></div>
        <div class="abs t" style="left:160px;top:190px;width:760px;font-size:104px">5 contas de <span class="mt">cabeça.</span></div>
        <div class="abs t" style="left:160px;top:470px;font-size:200px;color:var(--azul);-webkit-text-stroke:6px {INK}">7×8=?</div>
        <div class="abs" style="left:600px;top:760px;transform:rotate(6deg)">{av('jacare.cartola.redondos.5', 300)}</div>
        <div class="abs mini" style="left:160px;top:1100px;color:var(--txt2)">Sem calculadora. Gabarito no fim.</div>
      </div>''')]
    for i, (q, opts, ok) in enumerate(MATE):
        big = len(q) < 9; mid = 9 <= len(q) < 14
        pages.append(page(f'''
          <div class="abs" style="inset:0;background:{'#fff' if i % 2 else 'var(--creme)'}"></div>
          <div class="abs" style="left:80px;top:70px"><span class="chip" style="background:var(--azul);color:#fff">Matemática · {i + 1} de 5</span></div>
          <div class="abs t" style="left:80px;top:{200 if big else 210}px;width:920px;font-size:{170 if big else (120 if mid else 82)}px;color:{'var(--azul)' if big or mid else 'var(--tinta)'};{'-webkit-text-stroke:6px ' + INK if big or mid else ''}">{q}{' = ?' if big or mid else ''}</div>
          <div class="abs" style="right:90px;top:880px;transform:rotate({(-1) ** i * 7}deg)">{av(['jacare.cartola.redondos.5', 'gato.-.escuros.6', 'loboguara.fone.-.2', 'coruja.bone.redondos.6', 'caramelo.-.estrela.3'][i], 230)}</div>
          <div class="abs" style="left:80px;top:{520 if big else (560 if mid else 580)}px;width:920px">{opcoes(opts, fs=52, h=150)}</div>
          <div class="abs" style="left:80px;top:1150px;font-size:36px;font-weight:900;color:var(--txt2)">Responde de cabeça. Gabarito no último card.</div>'''))
    gab = ''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:20px 0;border-bottom:5px dashed rgba(14,42,34,.25)">'
                  f'<span style="font-size:40px;font-weight:900">{i + 1}. {q}</span><span class="t" style="font-size:60px;color:var(--azul)">{o[k]}</span></div>' for i, (q, o, k) in enumerate(MATE))
    pages.append(page(f'''
      <div class="abs caderno" style="left:60px;top:60px;width:960px;height:1230px;transform:rotate(1deg)">
        <div class="abs t" style="left:160px;top:70px;font-size:96px">Gabarito</div>
        <div class="abs" style="left:160px;top:210px;width:740px">{gab}</div>
        <div class="abs" style="left:160px;top:1060px;width:740px;font-size:38px;font-weight:900">5 de 5? Manda pro grupo da turma e desafia.</div>
      </div>'''))
    pages.append(C.endcard(END_Q))
    piece(id='Q-C16', fmt='carrossel', day=7, slot='12h30', title='Quiz de Matemática: 5 contas de cabeça', kind='engajamento', w=1080, h=1350,
          html=doc('Q-C16', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('5 contas de cabeça, sem calculadora. ➗\n'
                   'Da tabuada à porcentagem. Gabarito no último card.\n\n'
                   'Manda pro grupo da turma (ou pra um professor de Matemática) e desafia 👇\n'
                   'No Quiddo, a turma responde pelo celular e o pódio sai no telão.\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#quiddo #matematica #professor #quiz #escola'),
          notes='Segunda versão de escola por matéria (pedido do Gui no Q-C11). Contas conferidas: 56, 30, 3.600, 11, 8. Caderno quadriculado para diferenciar do Q-C13 (pautado). Card final = CTA aprovado do S04.')

# -------------------------------------------------------------------------------------
# Stories (1 sequência de 3 quadros por dia, 12h, sem adesivo): Quiz por matéria
# -------------------------------------------------------------------------------------
QS5 = [
    (1, 'Ciências', 'Qual destes animais é um anfíbio?', ['Sapo', 'Jacaré', 'Tartaruga', 'Cobra'], 0, 'O sapo nasce na água (girino) e vive em terra depois de adulto: é um anfíbio. Jacaré, tartaruga e cobra são répteis.', 'sapo.gorro.-.4', 'escola'),
    (2, 'Matemática', 'Quanto é a metade de um quarto?', ['1/2', '1/4', '1/6', '1/8'], 3, 'Um quarto dividido em duas partes iguais dá um oitavo: 1/4 ÷ 2 = 1/8.', 'coruja.gorro.redondos.6', 'familia'),
    (3, 'Geografia', 'Qual é o maior estado do Brasil em área?', ['Pará', 'Amazonas', 'Mato Grosso', 'Minas Gerais'], 1, 'O Amazonas tem cerca de 1,5 milhão de km²: é o maior estado do país.', 'boto.gorro.-.1', 'empresa'),
    (4, 'História', 'Em que ano foi proclamada a República no Brasil?', ['1822', '1888', '1889', '1930'], 2, 'A República foi proclamada em 15 de novembro de 1889.', 'tucano.cartola.-.5', 'escola'),
    (5, 'Português', 'Qual palavra está escrita certo?', ['Excessão', 'Exceção', 'Esceção', 'Exessão'], 1, 'Exceção, com "xc" e "ç". O "ss" fica para "excesso".', 'gato.gorro.redondos.6', 'amigos'),
    (6, 'Inglês', 'O que significa "Christmas Eve"?', ['Dia de Natal', 'Véspera de Natal', 'Ano-Novo', 'Ceia'], 1, '"Eve" é a véspera: Christmas Eve é a noite de 24 de dezembro.', 'arara.gorro.-.4', 'familia'),
    (7, 'Música', 'Quantas notas tem a escala de dó a si?', ['5', '6', '7', '8'], 2, 'Dó, ré, mi, fá, sol, lá, si: são 7 notas.', 'mico.fone.-.7', 'empresa'),
]
CTA_Q = {
    'escola': ('Na sala de aula, a revisão vira jogo.', 'Escreva as perguntas da matéria e a turma responde pelo celular. Ranking e pódio no telão.'),
    'familia': ('No almoço de família, a pergunta vira assunto.', 'Escreva perguntas sobre a família e cada um responde pelo celular. Pódio no telão da sala.'),
    'empresa': ('No treinamento da equipe, o conteúdo vira quiz.', 'Escreva as perguntas do treinamento e a equipe responde pelo celular. Ranking e pódio no telão.'),
    'amigos': ('No encontro dos amigos, o grupo vira pergunta.', 'Perguntas sobre o próprio grupo, no celular de cada um. Pódio no telão.'),
}

def telao(bichos):
    return (f'<div class="telao" style="width:620px"><div class="in" style="height:360px">'
            f'<div style="position:absolute;left:0;right:0;top:20px;text-align:center;font-family:Fraunces;font-weight:900;font-size:34px">E quem venceu foi…</div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0;transform:scale(.62);transform-origin:bottom center">{podio(bichos, 150)}</div></div></div>'
            f'<div style="width:160px;height:40px;background:var(--tinta);margin:0 auto;border-radius:0 0 12px 12px"></div>')

def q_stories():
    for n, (d, mat, q, opts, ok, expl, b, pub) in enumerate(QS5):
        sid = f'Q-S{28 + n}'
        rot = -1.2 if n % 2 else 1.2
        f1 = f'''<section class="page" style="width:1080px;height:1920px;background:var(--amarelo)">
          <div class="abs carta" style="left:70px;top:290px;width:940px;height:1180px;transform:rotate({rot}deg)">
            <div class="abs" style="left:50px;top:50px"><span class="chip" style="background:var(--laranja);color:#fff;border-color:var(--tinta)">Quiz de {mat}</span></div>
            <div class="abs" style="right:40px;top:-70px;transform:rotate(8deg)">{av(b, 210)}</div>
            <div class="abs t" style="left:50px;top:200px;width:840px;font-size:{84 if len(q) < 40 else 74}px">{q}</div>
            <div class="abs" style="left:50px;top:600px;width:840px">{opcoes(opts, fs=42, h=140)}</div>
            <div class="abs" style="left:50px;top:1010px;width:840px;font-size:40px;font-weight:900">Responde de cabeça. A resposta está no próximo story →</div>
          </div>
          <div class="abs" style="left:80px;top:1520px">{logo('cor', 190)}</div></section>'''
        f2 = f'''<section class="page" style="width:1080px;height:1920px;background:var(--amarelo)">
          <div class="abs carta" style="left:70px;top:290px;width:940px;height:1120px;transform:rotate({-rot}deg)">
            <div class="abs" style="left:50px;top:50px"><span class="chip" style="background:var(--laranja);color:#fff;border-color:var(--tinta)">Quiz de {mat}</span></div>
            <div class="abs" style="left:50px;top:180px;width:840px;font-size:38px;font-weight:800;color:var(--txt2)">{q}</div>
            <div class="abs" style="left:50px;top:330px;width:840px">{resp(ok, opts[ok], 'height:160px;font-size:56px', '<span style="margin-left:auto;font-size:60px">✓</span>')}</div>
            <div class="abs" style="left:50px;top:580px;width:840px;font-size:44px;font-weight:800;line-height:1.35">{expl}</div>
            <div class="abs" style="right:50px;top:900px;transform:rotate(-6deg)">{av(b, 190)}</div>
          </div>
          <div class="abs t" style="left:80px;top:1470px;width:920px;font-size:56px">Acertou? Manda pra quem ia errar.</div></section>'''
        h, sub = CTA_Q[pub]
        f3 = f'''<section class="page" style="width:1080px;height:1920px;background:var(--mata);color:var(--creme)">
          <div class="abs" style="left:80px;top:300px">{logo('neg', 260)}</div>
          <div class="abs t" style="left:80px;top:420px;width:920px;font-size:92px">{h}</div>
          <div class="abs" style="left:80px;top:760px;width:900px;font-size:44px;font-weight:700;line-height:1.35">{sub}</div>
          <div class="abs" style="left:230px;top:980px">{telao(['tucano.festa.-.5', 'onca.coroa.escuros.2', 'capivara.-.-.1'])}</div>
          <div class="abs" style="left:80px;top:1440px;width:920px;height:140px;border-radius:30px;background:var(--amarelo);color:var(--tinta);display:flex;align-items:center;justify-content:center;font-family:Fraunces;font-weight:900;font-size:60px">Faça o seu. Teste grátis. →</div>
          <div class="abs url" style="left:0;right:0;top:1620px;text-align:center">quiddo.com.br</div></section>'''
        piece(id=sid, fmt='story', day=d, slot='12h', title=f'Quiz de {mat}: {q} · sequência de 3', w=1080, h=1920, frames=3,
              html=doc(sid, FONTS, CSS, f1 + f2 + f3, 1080, 1920), caption='(story, sem legenda; postar os 3 quadros em sequência, no mesmo horário)', sticker='', kind='story',
              notes=f'Sequência de 3 sem adesivo (formato aprovado no S03): pergunta → resposta → CTA ({pub}). Fato conferido. Motivo de envio: "manda pra quem ia errar". Sem "até 10 pessoas".')

def build():
    q_c13(); q_r17(); q_c14(); q_r18(); q_c15(); q_r19(); q_c16(); q_stories()

build()
