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
def q_r7():
    T = 16.0
    tl = TL(T)
    dorm = [('capivara.-.-.1', -8), ('tucano.bone.-.5', 6), ('jabuti.palha.-.3', -5), ('onca.-.escuros.2', 7)]
    sofa = ''.join(f'<div style="position:relative;transform:rotate({r}deg)">{av(k, 205)}'
                   f'<div class="zz" style="position:absolute;right:-6px;top:-40px;font-size:56px;animation:blink 1.6s linear {i*.3:.1f}s infinite">z</div></div>'
                   for i, (k, r) in enumerate(dorm))
    s1 = f'''<div {tl.scene(0, 6.2, fin=False, fade=.12)}>
      <div class="abs" style="inset:0;background:var(--tinta)"></div>
      <div class="abs" style="left:90px;top:330px;{at(.05,'fade')}"><span class="chip">Domingo, 16h</span></div>
      <div class="abs t" style="left:90px;top:460px;width:900px;font-size:100px;color:var(--creme);{at(.2,'rise')}">Modo quiz da família:</div>
      <div class="abs" style="left:90px;top:700px;height:200px;display:flex;align-items:center;{at(.4,'rise')}">{toggle(t=4.3, size=1.3)}
        <span class="t" style="font-size:100px;color:#9AA7A1;margin-left:120px;animation:fadeOut .2s linear 4.3s 1 forwards">desligado</span></div>
      <div class="abs t" style="left:600px;top:745px;font-size:100px;color:var(--verde);opacity:0;animation:fade .2s linear 4.45s 1 both">ligado.</div>
      <div class="abs" style="left:90px;top:1010px;width:900px;display:flex;justify-content:space-between">{sofa}</div>
      <div class="abs" style="left:90px;top:1300px;width:900px;font-size:50px;font-weight:800;color:var(--creme);{at(1.4,'fade')}">Cada um no seu celular. Ninguém fala nada.</div>
      {C.tap(250, 800, 4.0, 130)}
    </div>'''
    opts = ['Tatu', 'Bolacha', 'Magrelo', 'Foguete']
    grid = ''.join(resp(j, o, f'height:140px;font-size:44px;{at(8.0 + j*.12, "pop")}') for j, o in enumerate(opts))
    gira = [('capivara.coroa.-.1', -8), ('tucano.festa.-.5', 6), ('jabuti.faixa.-.3', -5), ('onca.coroa.escuros.2', 7)]
    festa = ''.join(f'<div style="--r:{r}deg;{at(6.5 + i*.14, "drop")}">{av(k, 200)}</div>' for i, (k, r) in enumerate(gira))
    s2 = f'''<div {tl.scene(6.2, 13.2, fade=.08)}>
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs" style="left:90px;top:300px;height:150px;display:flex;align-items:center">{toggle(on=True, size=.8)}<span class="t" style="font-size:72px;margin-left:30px">ligado.</span></div>
      <div class="abs" style="left:90px;top:490px;width:900px;display:flex;justify-content:space-between">{festa}</div>
      <div class="abs card" style="left:90px;top:760px;width:900px;padding:34px 40px;{at(7.2,'pop')}"><div class="mini" style="color:var(--txt2)">PERGUNTA 1</div><div class="t" style="font-size:70px;margin-top:6px">Qual era o apelido do pai na escola?</div></div>
      <div class="abs" style="left:90px;top:1090px;width:900px;display:grid;grid-template-columns:1fr 1fr;gap:26px">{grid}</div>
      <div class="abs" style="left:300px;top:1420px;--r:-3deg;{at(10.6,'stamp')}"><div class="t" style="background:var(--tinta);color:var(--amarelo);border:7px solid var(--tinta);padding:14px 36px;font-size:64px;box-shadow:0 10px 0 var(--vermelho)">1º lugar: a vó.</div></div>
    </div>'''
    s3 = f'''<div {tl.scene(13.2, T, fout=False)}>
      <div class="abs" style="inset:0;background:var(--tinta)"></div>
      <div class="abs" style="left:240px;top:560px;{at(13.3,'pop')}">{logo('neg', 600)}</div>
      <div class="abs t" style="left:0;right:0;top:840px;text-align:center;font-size:64px;color:var(--creme);{at(13.6,'rise')}">Liga o modo quiz.</div>
      <div class="abs" style="left:0;right:0;top:970px;text-align:center;{at(13.9,'rise')}">{cta_fim(0)}</div>
      <div class="abs url" style="left:0;right:0;top:1100px;text-align:center;color:var(--amarelo);{at(14.1,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:var(--tinta)">
      <div class="abs t" style="left:80px;top:90px;width:920px;font-size:104px;color:var(--creme)">Modo quiz da família:</div>
      <div class="abs" style="left:80px;top:360px;display:flex;align-items:center;gap:40px">{toggle(on=True, size=1.25)}<span class="t" style="font-size:120px;color:var(--verde);margin-left:90px">ligado.</span></div>
      <div class="abs" style="left:80px;top:680px;width:920px;display:flex;justify-content:space-between">{''.join(f'<div style="transform:rotate({r}deg)">{av(k, 215)}</div>' for k, r in gira)}</div>
      <div class="abs" style="left:80px;top:1060px"><span class="chip" style="background:var(--amarelo);font-size:40px">Domingo, 16h</span></div></div>'''
    piece(id='Q-R7', fmt='reel', day=1, slot='19h45', title='Trend ligar/desligar: modo quiz da família ativado', total=T, poster=.6, kind='trend',
          html=doc('Q-R7', FONTS, CSS + C.REC_CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, '', 'var(--tinta)'),
          caption=('Domingo, 16h. Modo quiz da família: desligado. 😴\n'
                   'Cada um no seu celular, ninguém fala nada.\n\n'
                   'Liga o modo quiz e a pergunta 1 já vira assunto: qual era o apelido do pai na escola?\n\n'
                   'Manda no grupo da família e liga o modo quiz no próximo almoço 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#familia #domingoemfamilia #quiz #trend #jogosemfamilia #quiddo'),
          notes='Trend "ligar/desligar" (doc do DOT, 06/11; circulação no Brasil sem validação). Interruptor desenhado pela marca, sem copiar interface de terceiros. Escuro para abrir a semana depois do azul do Q-C6. Áudio em alta no app.')

# =====================================================================================
# Q-C7 · Carrossel · Último dia de aula: 6 perguntas para o quiz da turma (ter, caderno)
# =====================================================================================
PERG_TURMA = [
    ('Qual foi a palavra que a professora mais falou este ano?', '"Silêncio", "Gente!" ou outra? A turma vota.'),
    ('Quem chegou atrasado mais vezes?', 'Vale a turma inteira responder ao mesmo tempo.'),
    ('Qual foi o passeio ou evento mais lembrado do ano?', 'Boa para abrir conversa e lembrar fotos.'),
    ('Qual matéria teve a prova mais difícil?', 'Ninguém vai concordar. É essa a graça.'),
    ('Que música a turma mais cantou este ano?', 'Quem errar canta o refrão.'),
    ('O que a turma quer lembrar daqui a 10 anos?', 'A última pergunta fica para o mural da sala.'),
]

def q_c7():
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--creme)"></div>
      <div class="abs caderno" style="left:60px;top:60px;width:960px;height:1230px;transform:rotate(-1.2deg)">
        <div class="abs" style="left:160px;top:60px"><span class="chip" style="background:var(--amarelo)">Último dia de aula</span></div>
        <div class="abs t" style="left:160px;top:190px;width:760px;font-size:104px">6 perguntas para o quiz da <span class="mt">turma.</span></div>
        <div class="abs" style="left:160px;top:700px;transform:rotate(-5deg)">{av('tucano.bone.-.5', 300)}</div>
        <div class="abs" style="left:500px;top:680px;transform:rotate(6deg)">{av('coruja.-.redondos.6', 330)}</div>
        <div class="abs mini" style="left:160px;top:1110px;color:var(--txt2)">Para professores e para a turma. Salva.</div>
      </div>''')]
    bichos = ['tucano.bone.-.5', 'sapo.-.escuros.4', 'mico.festa.-.7', 'gato.fone.-.6', 'papagaio.-.estrela.2', 'arara.flor.-.4']
    for i, (q, dica) in enumerate(PERG_TURMA):
        rot = -1.2 if i % 2 else 1.0
        pages.append(page(f'''
          <div class="abs" style="inset:0;background:{'#fff' if i % 2 else 'var(--creme)'}"></div>
          <div class="abs caderno" style="left:60px;top:60px;width:960px;height:1230px;transform:rotate({rot}deg)">
            <div class="abs t" style="left:160px;top:70px;font-size:200px;color:var(--azul);-webkit-text-stroke:6px {INK}">{i+1}</div>
            <div class="abs" style="right:70px;top:90px;transform:rotate({6 if i % 2 else -6}deg)">{av(bichos[i], 230)}</div>
            <div class="abs t" style="left:160px;top:360px;width:740px;font-size:80px">{q}</div>
            <div class="abs" style="left:160px;top:720px;width:740px;font-size:34px;font-weight:900;color:var(--vermelho)">RESPOSTA DA TURMA:</div>
            <div class="abs" style="left:160px;top:800px;width:740px;height:70px;border-bottom:6px dashed {INK};opacity:.5"></div>
            <div class="abs" style="left:160px;top:960px;width:740px;font-size:40px;font-weight:800;line-height:1.35;color:var(--txt2)">{dica}</div>
            <div class="abs mini" style="left:160px;top:1120px;color:var(--txt2)">{i+1} / 6</div>
          </div>'''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:100px;color:var(--creme)">Monta as 6 e joga no último dia de <span class="mt">aula.</span></div>
      <div class="abs card" style="left:80px;top:560px;width:920px;padding:40px 46px;font-size:42px;font-weight:800;line-height:1.35">Cada um responde pelo celular e o pódio sai no fim. A turma inteira junto.</div>
      <div class="abs" style="left:80px;top:900px">{cta_fim(0)}</div>
      <div class="abs" style="left:80px;top:1120px">{logo('neg', 260)}</div>
      <div class="abs url" style="right:80px;top:1155px;color:var(--amarelo)">quiddo.com.br</div>''', cls='esc'))
    piece(id='Q-C7', fmt='carrossel', day=2, slot='12h30', title='Último dia de aula: 6 perguntas para o quiz da turma', kind='engajamento', w=1080, h=1350,
          html=doc('Q-C7', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Último dia de aula chegando. 6 perguntas para o quiz da turma. 📒\n\n'
                   '1. Qual foi a palavra que a professora mais falou este ano?\n2. Quem chegou atrasado mais vezes?\n3. Qual foi o passeio ou evento mais lembrado do ano?\n'
                   '4. Qual matéria teve a prova mais difícil?\n5. Que música a turma mais cantou este ano?\n6. O que a turma quer lembrar daqui a 10 anos?\n\n'
                   'Salva e manda pra professora ou pro grupo da turma 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#ultimodiadeaula #professor #escola #turma #quiz #quiddo'),
          notes='Utilidade sazonal (fim do ano letivo em dezembro). Motivo de envio: mandar para a professora ou o grupo da turma. Design de caderno pautado (objeto concreto). Sem dado factual.')

# =====================================================================================
# Q-R8 · Reel meme · O grupo ignora o quiz até aparecer o prêmio (qua, mata)
# =====================================================================================
def q_r8():
    T = 14.0
    tl = TL(T)
    def b(txt, t, me=False, nome='', hora='19:02'):
        return f'<div style="{at(t, "rise", .3)}">{C.bubble(txt, me=me, nome=nome, hora=hora, fs=42)}</div>'
    topo = ('<div style="height:96px;background:#0B5D45;color:#fff;display:flex;align-items:center;gap:18px;padding:0 26px;font:800 34px/1 \'DM Sans\',sans-serif">'
            f'<span style="width:62px;height:62px;border-radius:50%;background:var(--amarelo);display:inline-flex;align-items:center;justify-content:center">{sym(1, 38, INK)}</span>'
            '<span>Família (14)</span></div>')
    conv1 = (topo + '<div style="background:#EFE7DC;height:1200px;padding-top:16px">'
             + b('Gente, quiz da família no sábado?', .9, me=True, hora='19:02')
             + f'<div style="text-align:center;margin:26px 0;font:700 34px/1 \'DM Sans\',sans-serif;color:#667;{at(2.0, "fade")}">visto por 14</div>'
             + f'<div style="text-align:center;margin:26px 0;font:700 34px/1 \'DM Sans\',sans-serif;color:#667;{at(3.2, "fade")}">2 horas depois</div>'
             + b('Alguém?', 3.6, me=True, hora='21:07') + '</div>')
    conv2 = (topo + '<div style="background:#EFE7DC;height:1200px;padding-top:16px">'
             + b('Quem ganhar escolhe a pizza.', 6.6, me=True, hora='21:15')
             + b('EU', 7.4, nome='Tio Beto', hora='21:15') + b('tô dentro', 7.7, nome='Prima Lu', hora='21:15')
             + b('que horas??', 8.0, nome='Mãe', hora='21:15')
             + b('vou estudar o álbum', 8.4, nome='Vó', hora='21:16') + '</div>')
    s1 = f'''<div {tl.scene(0, 6.3, fin=False)}>
      <div class="abs t" style="left:90px;top:270px;width:900px;font-size:70px;color:var(--creme);{at(.05,'rise')}">O grupo da família quando você chama pro quiz:</div>
      <div class="abs" style="left:100px;top:450px;{at(.4,'rise')}">{C.phone(conv1, w=880, h=1120, screen='#EFE7DC', frame='#0E2A22', status_color='#111', hora='19:02')}</div>
    </div>'''
    s2 = f'''<div {tl.scene(6.3, 11.4)}>
      <div class="abs t" style="left:90px;top:270px;width:680px;font-size:70px;color:var(--creme);{at(6.35,'rise')}">O mesmo grupo quando tem <span class="mt">prêmio:</span></div>
      <div class="abs" style="left:100px;top:450px">{C.phone(conv2, w=880, h=1120, screen='#EFE7DC', frame='#0E2A22', status_color='#111', hora='21:15')}</div>
      <div class="abs" style="left:800px;top:240px;--r:6deg;{at(9.2,'drop')}">{av('jabuti.palha.redondos.3', 200)}</div>
    </div>'''
    s3 = f'''<div {tl.scene(11.4, T, fout=False)}>
      <div class="abs" style="left:190px;top:560px;{at(11.5,'pop')}">{logo('neg', 700)}</div>
      <div class="abs t" style="left:0;right:0;top:860px;text-align:center;font-size:62px;color:var(--creme);{at(11.8,'rise')}">A pizza é por conta do pódio.</div>
      <div class="abs" style="left:0;right:0;top:990px;text-align:center;{at(12.1,'rise')}">{cta_fim(0)}</div>
      <div class="abs url" style="left:0;right:0;top:1120px;text-align:center;color:var(--amarelo);{at(12.3,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page esc" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    mini_conv = (topo + '<div style="background:#EFE7DC;height:900px;padding-top:12px">'
                 + C.bubble('Quem ganhar escolhe a pizza.', me=True, hora='21:15', fs=40) + C.bubble('EU', nome='Tio Beto', hora='21:15', fs=40)
                 + C.bubble('tô dentro', nome='Prima Lu', hora='21:15', fs=40) + C.bubble('que horas??', nome='Mãe', hora='21:15', fs=40) + '</div>')
    cover_body = f'''<div class="page esc" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:84px;color:var(--creme)">O grupo da família quando tem <span class="mt">prêmio:</span></div>
      <div class="abs" style="left:80px;top:370px">{C.phone(mini_conv, w=700, h=940, screen='#EFE7DC', frame='#0E2A22', status_color='#111', hora='21:15')}</div>
      <div class="abs" style="left:770px;top:760px;transform:rotate(6deg)">{av('jabuti.palha.redondos.3', 260)}</div></div>'''
    piece(id='Q-R8', fmt='reel', day=3, slot='19h45', title='Meme: o grupo da família quando tem prêmio', total=T, poster=.62, kind='meme',
          html=doc('Q-R8', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'esc', 'var(--mata)'),
          caption=('O grupo da família quando você chama pro quiz: visto por 14. 🦗\n'
                   'O mesmo grupo quando "quem ganhar escolhe a pizza": 5 respostas em 1 minuto.\n\n'
                   'Manda no grupo da família e vê quem responde primeiro 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#meme #familia #grupodafamilia #quiz #pizza #quiddo'),
          notes='Meme de comportamento (antes/depois dentro da conversa). Celular e conversa genéricos, sem marca de app, nomes fictícios. Fundo mata alterna com o creme de terça e o amarelo de quinta.')

# =====================================================================================
# Q-C8 · Carrossel · Bloco de notas: as regras da casa na noite do quiz (qui, amarelo)
# =====================================================================================
REGRAS = [
    ('Celular na mão só para responder.', 'Pesquisar a resposta desclassifica na hora.', 'coruja.-.escuros.6'),
    ('Quem ficar em último lava a louça.', 'Sem recurso. Sem "melhor de 3".', 'capivara.-.-.1'),
    ('A vó tem 5 segundos a mais.', 'Regra criada depois que ela ganhou mesmo assim.', 'jabuti.palha.redondos.3'),
    ('Pergunta sobre a família vale ponto em dobro.', 'Quem não sabe o nome do cachorro do tio, aprende.', 'caramelo.bone.-.8'),
    ('O campeão escolhe o tema do próximo.', 'E aguenta ser cobrado o mês todo.', 'onca.coroa.-.2'),
]

def q_c8():
    lista = ''.join(f'<div style="display:flex;gap:18px;font-size:44px;font-weight:800;line-height:1.25;margin-bottom:22px"><span style="flex:none;width:44px;height:44px;border:5px solid {INK};border-radius:10px;margin-top:4px"></span>{r}</div>' for r, *_ in REGRAS)
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--amarelo)"></div>
      <div class="abs nota" style="left:90px;top:100px;width:900px;height:1150px;transform:rotate(-1.5deg);background-color:#FFF6E6">
        <div class="abs mini" style="left:50px;top:40px;color:var(--txt2)">NOTAS · sábado</div>
        <div class="abs t" style="left:50px;top:110px;width:800px;font-size:96px">Regras da casa na noite do quiz</div>
        <div class="abs" style="left:50px;top:470px;width:800px">{lista}</div>
      </div>
      <div class="abs" style="left:760px;top:1040px;transform:rotate(8deg)">{av('onca.coroa.-.2', 230)}</div>''')]
    for i, (r, sub, k) in enumerate(REGRAS):
        pages.append(page(f'''
          <div class="abs" style="inset:0;background:{'var(--creme)' if i % 2 == 0 else '#fff'}"></div>
          <div class="abs nota" style="left:90px;top:110px;width:900px;height:1000px;transform:rotate({-1.4 if i % 2 else 1.2}deg)">
            <div class="abs mini" style="left:50px;top:40px;color:var(--txt2)">REGRA {i+1} DE 5</div>
            <div class="abs" style="left:50px;top:130px;width:72px;height:72px;border:7px solid {INK};border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center">
              <svg width="50" height="50" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6" stroke="{INK}" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
            <div class="abs t" style="left:50px;top:250px;width:800px;font-size:86px">{r}</div>
            <div class="abs" style="left:50px;top:720px;width:560px;font-size:42px;font-weight:800;line-height:1.3">{sub}</div>
          </div>
          <div class="abs" style="left:700px;top:880px;transform:rotate({6 if i % 2 else -6}deg)">{av(k, 280)}</div>'''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:100px;color:var(--creme)">Faltou a regra 6? Escreve no <span class="mt">grupo.</span></div>
      <div class="abs card" style="left:80px;top:560px;width:920px;padding:40px 46px;font-size:42px;font-weight:800;line-height:1.35">E a noite do quiz fica marcada: perguntas da família, celular na mão e pódio no fim.</div>
      <div class="abs" style="left:80px;top:900px">{cta_fim(0)}</div>
      <div class="abs" style="left:80px;top:1120px">{logo('neg', 260)}</div>
      <div class="abs url" style="right:80px;top:1155px;color:var(--amarelo)">quiddo.com.br</div>''', cls='esc'))
    piece(id='Q-C8', fmt='carrossel', day=4, slot='12h30', title='Bloco de notas: regras da casa na noite do quiz', kind='engajamento', w=1080, h=1350,
          html=doc('Q-C8', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Regras da casa na noite do quiz. 📝\n\n'
                   '1. Celular na mão só para responder.\n2. Quem ficar em último lava a louça.\n3. A vó tem 5 segundos a mais.\n'
                   '4. Pergunta sobre a família vale ponto em dobro.\n5. O campeão escolhe o tema do próximo.\n\n'
                   'Faltou a regra 6? Escreve nos comentários e manda no grupo pra já combinar 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#noitedejogos #familia #quiz #regras #amigos #quiddo'),
          notes='Identidade e marcação ("manda no grupo pra já combinar"). Design de bloco de notas com caixa marcada, sem marca de app. Capa amarela entre o mata de quarta e o vermelho de sexta. Regras são humor, sem dado factual.')

# =====================================================================================
# Q-R9 · Reel meme · Black Friday da família: etiquetas de desconto (sex 27/11, vermelho)
# =====================================================================================
ETIQ = [
    ('Paciência do tio na 3ª rodada', '−90%'),
    ('Vontade de lavar a louça', 'esgotada'),
    ('Revanche', 'leve 3, pague 1'),
    ('Desculpa de quem perdeu', 'frete grátis'),
]

def q_r9():
    T = 15.0
    tl = TL(T)
    tags = ''.join(f'''<div style="margin-bottom:34px;--r:{(-1)**i*2}deg;{at(2.6 + i*1.6, 'slideR')}"><div class="tag" style="transform:rotate({(-1)**i*2}deg)">
        <div style="font-size:44px;font-weight:900">{n}</div><div class="t" style="font-size:92px;color:var(--vermelho);margin-top:4px">{p}</div></div></div>''' for i, (n, p) in enumerate(ETIQ))
    s1 = f'''<div {tl.scene(0, 10.4, fin=False)}>
      <div class="abs" style="inset:0;background:var(--tinta)"></div>
      <div class="abs t" style="left:90px;top:280px;width:640px;font-size:100px;color:#fff;{at(.05,'rise')}">Black Friday da <span class="mt">família.</span></div>
      <div class="abs" style="left:90px;top:560px;width:900px">{tags}</div>
      <div class="abs" style="left:760px;top:330px;--r:8deg;{at(.6,'drop')}">{av('tatu.cartola.bigode.3', 240)}</div>
    </div>'''
    s2 = f'''<div {tl.scene(10.4, 12.8)}>
      <div class="abs" style="inset:0;background:var(--vermelho)"></div>
      <div class="abs t" style="left:90px;top:560px;width:900px;font-size:110px;color:#fff;{at(10.45,'rise')}">O pódio?</div>
      <div class="abs" style="left:90px;top:760px;--r:-4deg;{at(10.9,'stamp')}"><div class="t" style="background:#fff;color:var(--tinta);border:7px solid var(--tinta);padding:16px 40px;font-size:84px;box-shadow:0 12px 0 var(--tinta)">Não está à venda.</div></div>
      <div class="abs" style="left:650px;top:1020px;--r:6deg;{at(11.4,'drop')}">{av('onca.coroa.escuros.2', 280)}</div>
    </div>'''
    s3 = f'''<div {tl.scene(12.8, T, fout=False)}>
      <div class="abs" style="inset:0;background:var(--tinta)"></div>
      <div class="abs" style="left:240px;top:580px;{at(12.85,'pop')}">{logo('neg', 600)}</div>
      <div class="abs" style="left:0;right:0;top:880px;text-align:center;{at(13.1,'rise')}">{cta_fim(0)}</div>
      <div class="abs url" style="left:0;right:0;top:1010px;text-align:center;color:var(--amarelo);{at(13.3,'fade')}">quiddo.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    ctags = ''.join(f'<div style="margin-bottom:26px"><div class="tag" style="transform:rotate({(-1)**i*2}deg);padding:24px 40px 24px 86px"><div style="font-size:42px;font-weight:900">{n}</div><div class="t" style="font-size:84px;color:var(--vermelho)">{p}</div></div></div>' for i, (n, p) in enumerate(ETIQ[:3]))
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:var(--vermelho)">
      <div class="abs t" style="left:80px;top:80px;width:700px;font-size:104px;color:#fff">Black Friday da família.</div>
      <div class="abs" style="left:760px;top:90px;transform:rotate(8deg)">{av('tatu.cartola.bigode.3', 230)}</div>
      <div class="abs" style="left:80px;top:430px;width:920px">{ctags}</div></div>'''
    piece(id='Q-R9', fmt='reel', day=5, slot='19h45', title='Meme Black Friday da família: etiquetas de desconto', total=T, poster=.45, kind='meme',
          html=doc('Q-R9', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, '', 'var(--vermelho)'),
          caption=('Black Friday da família. 🏷️\n\n'
                   'Paciência do tio na 3ª rodada: −90%.\nVontade de lavar a louça: esgotada.\nRevanche: leve 3, pague 1.\nDesculpa de quem perdeu: frete grátis.\n\n'
                   'O pódio? Não está à venda.\n\n'
                   'Manda pro tio que já está pedindo revanche 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#blackfriday #meme #familia #quiz #humor #quiddo'),
          notes='Meme do dia da Black Friday (sex 27/11), feito com etiquetas de preço (objeto concreto). Não fala de preço do Quiddo nem de desconto real. Vermelho/tinta alterna com o amarelo de quinta e o claro de sábado.')

# =====================================================================================
# Q-C9 · Carrossel · Desafio: complete o ditado (sáb, cartas brancas)
# =====================================================================================
DITADOS = [
    ('Quem não tem cão, caça com…', ['gato', 'rede', 'vara', 'cachorro do vizinho'], 0, 'Quem não tem cão, caça com gato.', 'gato.-.redondos.6'),
    ('De grão em grão, a galinha…', ['bota um ovo', 'enche o papo', 'atravessa a rua', 'vai longe'], 1, 'De grão em grão, a galinha enche o papo.', 'arara.-.-.4'),
    ('Água mole em pedra dura…', ['logo some', 'vira areia', 'tanto bate até que fura', 'não faz nada'], 2, 'Água mole em pedra dura, tanto bate até que fura.', 'boto.-.-.9'),
    ('A cavalo dado não se olham…', ['o rabo', 'a sela', 'as patas', 'os dentes'], 3, 'A cavalo dado não se olham os dentes.', 'caramelo.-.-.8'),
    ('Em casa de ferreiro…', ['espeto de pau', 'ninguém dorme', 'tudo é de ferro', 'falta martelo'], 0, 'Em casa de ferreiro, espeto de pau.', 'tatu.palha.-.9'),
]

def q_c9():
    leque = ''.join(f'<div class="abs carta" style="left:{90 + i*150}px;top:{790 - abs(i-2)*30}px;width:300px;height:420px;transform:rotate({(i-2)*9}deg);transform-origin:50% 120%;display:flex;align-items:center;justify-content:center">{av(k, 220)}</div>' for i, (*_, k) in enumerate(DITADOS))
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--creme)"></div>
      <div class="abs" style="left:80px;top:80px"><span class="chip">Desafio · 5 cartas</span></div>
      <div class="abs t" style="left:80px;top:200px;width:930px;font-size:104px">Complete o ditado. Aposto que a vó acerta <span class="mt">5 de 5.</span></div>
      {leque}''')]
    for i, (q, opts, ok, _, k) in enumerate(DITADOS):
        cores = ['var(--verde)', 'var(--laranja)', 'var(--azul)', 'var(--vermelho)', 'var(--amarelo)']
        opts_html = ''.join(resp(j, o, 'height:130px;font-size:36px') for j, o in enumerate(opts))
        pages.append(page(f'''
          <div class="abs" style="inset:0;background:{cores[i]}"></div>
          <div class="abs carta" style="left:70px;top:70px;width:940px;height:1210px;transform:rotate({(-1)**i*1.2}deg)">
            <div class="abs mini" style="left:56px;top:50px;color:var(--txt2)">CARTA {i+1} DE 5</div>
            <div class="abs" style="right:50px;top:40px;transform:rotate({(-1)**i*6}deg)">{av(k, 220)}</div>
            <div class="abs t" style="left:56px;top:290px;width:830px;font-size:92px">{q}</div>
            <div class="abs" style="left:56px;top:720px;width:830px;display:grid;grid-template-columns:1fr 1fr;gap:24px">{opts_html}</div>
            <div class="abs mini" style="left:56px;top:1110px;color:var(--txt2)">Anota. Respostas na última carta.</div>
          </div>'''))
    gab = ''.join(f'''<div style="display:flex;align-items:center;gap:22px;margin-bottom:24px">
        <span style="flex:none;width:64px;height:64px;border:5px solid {INK};border-radius:18px;background:{['var(--verde)','var(--laranja)','var(--azul)','var(--vermelho)'][ok]};display:flex;align-items:center;justify-content:center">{sym(ok, 40)}</span>
        <span style="font-size:36px;font-weight:800;line-height:1.2">{full}</span></div>''' for q, opts, ok, full, k in DITADOS)
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:90px;font-size:96px;color:var(--creme)">Gabarito</div>
      <div class="abs" style="left:80px;top:250px;width:920px;color:var(--creme)">{gab}</div>
      <div class="abs t" style="left:80px;top:840px;width:920px;font-size:56px;color:var(--creme)">Quantas você fez? Manda no grupo e desafia a vó.</div>
      <div class="abs" style="left:80px;top:1040px">{cta_fim(0)}</div>
      <div class="abs" style="left:80px;top:1180px">{logo('neg', 230)}</div>
      <div class="abs url" style="right:80px;top:1205px;color:var(--amarelo)">quiddo.com.br</div>''', cls='esc'))
    piece(id='Q-C9', fmt='carrossel', day=6, slot='12h30', title='Desafio: complete o ditado (5 cartas)', kind='engajamento', w=1080, h=1350,
          html=doc('Q-C9', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Complete o ditado. Aposto que a vó acerta 5 de 5. 👵\n\n'
                   'Quem não tem cão, caça com… De grão em grão… Água mole em pedra dura…\n'
                   'Arrasta, anota as suas e confere o gabarito na última carta.\n\n'
                   'Manda no grupo da família e desafia a vó 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#ditadospopulares #desafio #quiz #familia #vó #quiddo'),
          notes='Desafio com marcação (desafiar a vó). Formato de cartas, diferente do desafio de bichos do S02. Ditados conferidos na forma tradicional (A cavalo dado não se olham os dentes). Capa creme clara, cartas coloridas por dentro.')

# =====================================================================================
# Q-R10 · Reel trend · Minivlog com rótulos: o domingo do quiz da família (dom, azul)
# =====================================================================================
def q_r10():
    T = 18.0
    tl = TL(T)
    cenas = [
        (0.0, '13h · almoço', 'Mesa cheia. Todo mundo quieto no prato.', [('capivara.-.-.1', 'Pai'), ('onca.flor.-.2', 'Mãe'), ('jabuti.palha.redondos.3', 'Vó')], 'var(--azul)'),
        (3.4, '14h30 · alguém sugere', '"E se a gente fizesse um quiz?"', [('mico.festa.-.7', 'Prima')], 'var(--laranja)'),
        (6.4, '14h35 · código no grupo', 'Cada um entra pelo celular.', None, 'var(--verde)'),
        (9.4, '15h10 · pergunta 6', '"Em que cidade o vô nasceu?"', [('tucano.bone.-.5', 'Primo'), ('sapo.-.escuros.4', 'Tio')], 'var(--vermelho)'),
        (12.4, '15h40 · pódio', 'A vó em 1º. De novo.', 'podio', 'var(--amarelo)'),
    ]
    scenes = ''
    for n, (t0, rot, txt, who, bg) in enumerate(cenas):
        extra = ''
        if n == 0:
            extra = f'<div class="abs" style="left:70px;top:1260px;width:940px;height:56px;border-radius:20px;background:#8A5A34;border:7px solid {INK};box-shadow:0 10px 0 {INK};{at(t0 + .3,"rise")}"></div>'
        if n == 3:
            extra = f'<div class="abs" style="left:90px;top:700px;width:900px;display:grid;grid-template-columns:1fr 1fr;gap:22px">' + ''.join(resp(j, o, f'height:120px;font-size:42px;{at(t0 + .5 + j*.1, "pop")}') for j, o in enumerate(['Recife', 'Santos', 'Itu', 'Garanhuns'])) + '</div>'
        t1 = cenas[n + 1][0] if n + 1 < len(cenas) else 15.6
        light = bg in ('var(--amarelo)',)
        fg = 'var(--tinta)' if light else '#fff'
        if who == 'podio':
            pod = [('tucano.bone.-.5', 2, 280), ('jabuti.coroa.redondos.3', 1, 380), ('onca.flor.-.2', 3, 220)]
            mid = ''.join(f'''<div style="display:flex;flex-direction:column;align-items:center;width:280px;{at(t0 + .3 + j*.15,'rise')}">{av(k, 270 if p == 1 else 210)}
                <div class="card" style="width:250px;height:{h}px;margin-top:14px;display:flex;justify-content:center;padding-top:20px"><span class="t" style="font-size:96px">{p}º</span></div></div>''' for j, (k, p, h) in enumerate(pod))
            mid = f'<div class="abs" style="left:90px;top:760px;width:900px;display:flex;justify-content:space-between;align-items:flex-end;height:640px">{mid}</div>'
        elif who is None:
            mid = f'''<div class="abs card" style="left:170px;top:760px;width:740px;padding:50px;text-align:center;transform:rotate(-2deg);{at(t0 + .4,'pop')}">
                <div class="mini" style="color:var(--txt2)">CÓDIGO DA SALA · EXEMPLO</div><div class="t" style="font-size:190px;letter-spacing:.06em;margin-top:10px">B4R9</div></div>
              <div class="abs" style="left:90px;top:1200px;width:900px;display:flex;justify-content:space-around">{''.join(f'<div style="{at(t0 + .9 + j*.12,"pop")}">{av(k, 165)}</div>' for j, k in enumerate(['capivara.-.-.1','onca.flor.-.2','jabuti.palha.redondos.3','mico.festa.-.7','tucano.bone.-.5']))}</div>'''
        else:
            top = 1000 if n == 3 else 900
            mid = f'<div class="abs" style="left:90px;top:{top}px;width:900px;display:flex;justify-content:space-around">' + ''.join(
                f'<div style="text-align:center;--r:{(-1)**j*5}deg;{at(t0 + .4 + j*.15,"drop")}">{av(k, {1: 400, 2: 300, 3: 270}[len(who)] if n != 3 else 230)}<div style="font-size:44px;font-weight:900;margin-top:10px;color:{fg}">{nm}</div></div>' for j, (k, nm) in enumerate(who)) + '</div>'
        scenes += f'''<div {tl.scene(t0, t1, fade=.12, fin=n > 0)}>
          <div class="abs" style="inset:0;background:{bg}"></div>
          <div class="abs" style="left:90px;top:300px;{at(t0 + .05,'slideL')}"><span class="rot">{rot}</span></div>
          <div class="abs t" style="left:90px;top:440px;width:900px;font-size:104px;color:{fg};{at(t0 + .2,'rise')}">{txt}</div>
          {extra}{mid}</div>'''
    scenes += f'''<div {tl.scene(15.6, T, fout=False)}>
      <div class="abs" style="inset:0;background:var(--creme)"></div>
      <div class="abs" style="left:190px;top:560px;{at(15.7,'pop')}">{logo('cor', 700)}</div>
      <div class="abs t" style="left:0;right:0;top:860px;text-align:center;font-size:62px;{at(15.9,'rise')}">Domingo que vira assunto.</div>
      <div class="abs" style="left:0;right:0;top:990px;text-align:center;{at(16.2,'rise')}">{cta_fim(0)}</div>
      <div class="abs url" style="left:0;right:0;top:1120px;text-align:center;{at(16.4,'fade')}">quiddo.com.br</div></div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{scenes}</section>'
    rots = ''.join(f'<div style="margin-bottom:24px;transform:rotate({(-1)**i*1.5}deg)"><span class="rot" style="font-size:54px">{r}</span></div>' for i, r in enumerate(['13h · almoço', '14h30 · alguém sugere', '14h35 · código no grupo', '15h10 · pergunta 6', '15h40 · pódio']))
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:var(--azul)">
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:112px;color:#fff">O domingo do quiz da família</div>
      <div class="abs" style="left:80px;top:400px">{rots}</div>
      <div class="abs" style="left:660px;top:880px;transform:rotate(6deg)">{av('jabuti.coroa.redondos.3', 340)}</div></div>'''
    piece(id='Q-R10', fmt='reel', day=7, slot='19h45', title='Trend minivlog com rótulos: o domingo do quiz da família', total=T, poster=.75, kind='trend',
          html=doc('Q-R10', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, '', 'var(--azul)'),
          caption=('O domingo do quiz da família, em 5 rótulos. ☀️\n\n'
                   '13h · almoço\n14h30 · alguém sugere um quiz\n14h35 · código no grupo\n15h10 · "em que cidade o vô nasceu?"\n15h40 · a vó em 1º. De novo.\n\n'
                   'Manda no grupo da família e marca o próximo domingo 👇\n'
                   'Faça o seu. Teste grátis: quiddo.com.br\n#domingoemfamilia #minivlog #familia #quiz #almocodedomingo #quiddo'),
          notes='Trend "minivlog com rótulos" (doc do DOT, 06/11; sem validação no Brasil). Domingo é o melhor dia para reels. Código da sala é de exemplo e está marcado. Capa azul fecha a semana; não fica ao lado do azul do Q-C6 na grade.')

# =====================================================================================
# Stories · "Pergunta do dia" em cartão, com a resposta numa aba de cabeça pra baixo
# =====================================================================================
PERGUNTAS_S03 = [
    (1, 'Quantas patas tem uma aranha?', ['6', '8', '10', '12'], 1, '8', 'tamandua.-.redondos.8', False),
    (2, 'Qual é a capital da Austrália?', ['Sydney', 'Melbourne', 'Canberra', 'Perth'], 2, 'Canberra', 'tucano.bone.-.5', True),
    (3, 'Quantos jogadores de cada time ficam em quadra no vôlei?', ['5', '6', '7', '11'], 1, '6', 'mico.fone.-.7', False),
    (4, 'Qual é o maior oceano do mundo?', ['Atlântico', 'Índico', 'Pacífico', 'Ártico'], 2, 'Pacífico', 'peixeboi.-.-.3', True),
    (5, 'Quantos minutos tem um dia?', ['1.240', '1.440', '1.640', '2.400'], 1, '1.440 (24 × 60)', 'coruja.-.escuros.6', False),
    (6, 'Qual é o menor país do mundo?', ['Mônaco', 'Vaticano', 'San Marino', 'Malta'], 1, 'Vaticano', 'gato.coroa.-.6', True),
    (7, 'Em que ano o ser humano pisou na Lua pela primeira vez?', ['1959', '1969', '1979', '1989'], 1, '1969', 'sapo.-.estrela.4', False),
]

def q_stories():
    for n, (d, q, opts, ok, ans, k, dark) in enumerate(PERGUNTAS_S03):
        grid = ''.join(resp(j, o, 'height:140px;font-size:40px') for j, o in enumerate(opts))
        bg = 'var(--mata)' if dark else 'var(--amarelo)'
        fs = 84 if len(q) < 40 else 72
        body = f'''<section class="page" style="width:1080px;height:1920px;background:{bg}">
          <div class="abs carta" style="left:70px;top:270px;width:940px;height:1180px;transform:rotate({-1.2 if n % 2 else 1.2}deg)">
            <div class="abs" style="left:50px;top:46px"><span class="chip" style="background:var(--amarelo)">Pergunta do dia · {C.DIAS[d].split()[1]}</span></div>
            <div class="abs" style="right:40px;top:-60px;transform:rotate(8deg)">{av(k, 200)}</div>
            <div class="abs t" style="left:50px;top:200px;width:840px;font-size:{fs}px">{q}</div>
            <div class="abs" style="left:50px;top:580px;width:840px;display:grid;grid-template-columns:1fr 1fr;gap:24px">{grid}</div>
            <div class="abs" style="left:50px;top:940px;width:840px;border-top:5px dashed rgba(14,42,34,.35);padding-top:24px;transform:rotate(180deg);text-align:right">
              <span class="mini" style="color:var(--txt2)">Resposta: {"ABCD"[ok]} · {ans}</span></div>
            <div class="abs" style="left:50px;top:1060px;font-size:40px;font-weight:900">Tira print e manda no grupo: quem acerta?</div>
          </div>
          <div class="abs" style="left:80px;top:1490px">{logo('neg' if dark else 'cor', 170)}</div>
        </section>'''
        sid = f'Q-S{13 + n}'
        piece(id=sid, fmt='story', day=d, title=f'Pergunta do dia: {q}', w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker='', kind='story',
              notes='Sem adesivo: resposta de cabeça pra baixo, na aba do cartão. Motivo de envio: print no grupo. Fato conferido. Design novo em cartão (S02 era chip solto), fundo alternando amarelo e mata.')

def build():
    q_r7(); q_c7(); q_r8(); q_c8(); q_r9(); q_c9(); q_r10(); q_stories()

build()
