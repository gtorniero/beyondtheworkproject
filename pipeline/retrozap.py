"""Retrozap · Pack Semanal 02. Bricolage Grotesque 800 / DM Sans / DM Mono.
Casa Grupo: Noite + Manga (apoio Chiclete, Goiaba, Piscina, Uva). Casa Casal: Creme + Cereja/Vinho, sem roxo.
Ícones: só os 69 oficiais (assets/retrozap/icones-*). Dados de exemplo: Turma do Churras, Dani & Cris."""
import common as C
from common import TL, at, doc, add

AR = C.A / 'retrozap'
FONTS = (C.font_face('Bricolage Grotesque', 'Bricolage-800.woff2', '800') +
         C.font_face('DM Sans', 'DMSans-var.woff2', '400 700') +
         C.font_face('DM Mono', 'DMMono-Regular.woff2', '400') + C.font_face('DM Mono', 'DMMono-Medium.woff2', '500'))

CSS = """
:root{--noite:#1A0B2E;--acai:#3D1A5C;--acai2:#2A1242;--linha:#4E2E6E;--manga:#FFC23C;--chiclete:#FF4F8B;--goiaba:#FF7A59;--piscina:#2EC4F1;--uva:#A98BFF;--areia:#FFF4E0;--neblina:#B9A8CC;
--creme:#FFF3EC;--rosa1:#FFD6E2;--rosa2:#FFE6EC;--clinha:#F4C3D1;--rosa:#FF4F8B;--cereja:#E0245E;--cerejaA:#CC1D59;--cerejaE:#B5174D;--vinho:#5E0B2B;--vinho2:#87445C;--pessego:#FFB59A;
--ease-pop:cubic-bezier(.34,1.56,.64,1);--ease-rise:cubic-bezier(.2,.8,.2,1);--ease-grow:cubic-bezier(.2,.8,.2,1);--ease-slideL:cubic-bezier(.2,.8,.2,1);--ease-slideR:cubic-bezier(.2,.8,.2,1);--ease-fade:linear;--ease-drop:cubic-bezier(.3,1.3,.5,1);--ease-stamp:cubic-bezier(.3,1.3,.5,1)}
.page{background:var(--noite);color:var(--areia);font-family:'DM Sans',sans-serif;font-weight:500}
.page.casal{background:var(--creme);color:var(--vinho)}
.t{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.03em;line-height:.95}
.hl{color:var(--manga)} .casal .hl{color:var(--cereja)}
.mono{font-family:'DM Mono',monospace}
.tag{display:inline-block;border-radius:999px;padding:12px 26px;font-weight:700;font-size:30px;background:var(--acai);color:var(--areia);border:3px solid var(--linha)}
.casal .tag{background:var(--rosa1);color:var(--vinho);border-color:var(--clinha)}
.selo{display:inline-block;background:var(--manga);color:var(--noite);padding:18px 44px;transform:rotate(-3deg)}
.casal .selo{background:var(--cereja);color:var(--creme)}
.box{background:var(--acai);border-radius:34px}
.casal .box{background:var(--rosa1)}
.foot{position:absolute;left:0;right:0;text-align:center;font-weight:700;font-size:32px}
.sim{font-family:'DM Mono',monospace;font-size:26px;opacity:.7;letter-spacing:.04em}
@property --n{syntax:'<integer>';inherits:false;initial-value:0}
.cnt{counter-reset:c var(--n)}.cnt::after{content:counter(c)}
"""

def icon(name, size, casa='grupo', style=''):
    d = 'icones-casal' if casa == 'casal' else 'icones-grupo'
    return f'<span style="display:inline-block;width:{size}px;height:{size}px;{style}">{C.svg_sized(AR / d / (name + ".svg"), w=size, h=size)}</span>'

def taca(size, casa='grupo', inv=False):
    s = C.svg_sized(AR / f'logo-simbolo-{casa}.svg', w=size, h=size)
    if inv:  # combinação oficial "Grupo, invertido": taça Noite, pontinhos Manga
        s = s.replace('#FFC23C', '#TMP').replace('#1A0B2E', '#FFC23C').replace('#TMP', '#1A0B2E')
    return s

def assinatura(w, casa='grupo', inv=False):
    s = C.svg_sized(AR / f'logo-assinatura-{casa}.svg', w=w)
    if inv:
        s = s.replace('#FFC23C', '#TMP').replace('#1A0B2E', '#FFC23C').replace('#TMP', '#1A0B2E')
    return s

def dots(x, y, size, color, t0, reps=3):
    """Assinatura animada: três pontinhos de 'digitando' sobem em sequência."""
    out = ''
    for i in range(3):
        anim = ','.join(f'dots .5s ease-in-out {t0 + i * .14 + r * .62:.2f}s 1' for r in range(reps))
        out += f'<div class="abs" style="left:{x + i * size * 1.5}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;background:{color};animation:{anim}"></div>'
    return out

def page(body, w=1080, h=1350, cls=''):
    return f'<section class="page {cls}" style="width:{w}px;height:{h}px">{body}</section>'

def cover_from_feed(feed_body, bg):
    return doc('capa', FONTS, CSS, f'<section class="page" style="width:1080px;height:1920px;background:{bg}"><div class="abs" style="left:0;top:285px;width:1080px;height:1350px;overflow:hidden">{feed_body}</div></section>', 1080, 1920)

def piece(**kw):
    kw.setdefault('brand', 'Retrozap')
    return add(kw)


def notif(nome, txt, hora, y, t, icon_name='speech-balloon'):
    return f'''<div class="abs" style="left:70px;width:940px;top:{y}px;background:var(--acai);border:3px solid var(--linha);border-radius:36px;padding:22px 30px;display:flex;gap:24px;align-items:center;{at(t,'rise', .35)}">
      <div style="flex:none;width:78px;height:78px;border-radius:22px;background:var(--areia);display:flex;align-items:center;justify-content:center">{icon(icon_name, 64)}</div>
      <div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;font-size:26px;color:var(--neblina);font-weight:700"><span>Turma do Churras</span><span>{hora}</span></div>
      <div style="font-size:38px;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"><b>{nome}:</b> {txt}</div></div></div>'''

FIM_GRUPO = lambda t: f'''<div class="abs" style="left:0;right:0;top:470px;display:flex;justify-content:center;{at(t + .1,'pop')}">{assinatura(700)}</div>
      <div class="abs t" style="left:0;right:0;top:760px;text-align:center;font-size:96px;{at(t + .4,'rise')}">e o seu grupo?</div>
      <div class="abs" style="left:0;right:0;top:920px;text-align:center;{at(t + .8,'rise')}"><span class="tag" style="background:var(--manga);color:var(--noite);border-color:var(--manga);font-size:36px">1º grupo grátis</span></div>
      <div class="foot" style="top:1080px;font-size:40px;{at(t + 1.0,'fade')}">retrozap.com.br</div>'''

# =====================================================================================
# R-C3 · Carrossel · Dicionário do grupo (seg, capa Manga)
# =====================================================================================
def r_c3():
    verbetes = [
        ('"Vamos marcar"', 'va·mos mar·car', 'Não vamos marcar.', 'spiral-calendar-pad'),
        ('"Tô chegando"', 'tô che·gan·do', 'Tô saindo do banho.', 'rocket'),
        ('"Quem topa?"', 'quem to·pa', 'Sete visualizações. Nenhuma resposta.', 'eyes'),
        ('"Depois eu vejo"', 'de·pois eu ve·jo', 'Não vai ver.', 'turtle'),
        ('"Gente, rapidinho"', 'gen·te ra·pi·di·nho', 'Textão chegando.', 'scroll'),
        ('"Bom dia, grupo"', 'bom di·a gru·po', 'Ninguém responde desde terça.', 'waving-hand-sign'),
    ]
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--manga)"></div>
      <div class="abs" style="left:80px;top:90px">{taca(110, inv=True)}</div>
      <div class="abs t" style="left:80px;top:300px;width:920px;font-size:150px;color:var(--noite)">Dicionário do grupo</div>
      <div class="abs" style="left:80px;top:640px;width:760px;font-size:46px;line-height:1.3;color:var(--noite);font-weight:700">O que cada mensagem quer dizer de verdade.</div>
      <div class="abs" style="left:700px;top:880px;transform:rotate(8deg)">{icon('books', 280)}</div>
      <div class="abs" style="left:80px;top:1180px"><span class="tag" style="background:var(--noite);border-color:var(--noite)">Arrasta →</span></div>''')]
    def verbete(w, pron, sig, ic, cor):
        return f'''<div style="display:flex;gap:34px;align-items:flex-start;padding:70px 0 80px;border-top:3px solid var(--linha)">
          {icon(ic, 150)}<div style="flex:1"><div class="t" style="font-size:88px;color:{cor}">{w}</div>
          <div class="mono" style="font-size:28px;color:var(--neblina);margin-top:10px">/{pron}/ · expressão de grupo</div>
          <div style="font-size:54px;font-weight:700;margin-top:24px;line-height:1.25">{sig}</div></div></div>'''
    cores = ['var(--manga)', 'var(--chiclete)', 'var(--piscina)']
    for i in range(3):
        a, b = verbetes[2*i], verbetes[2*i+1]
        pages.append(page(f'''
          <div class="abs mono" style="left:80px;top:90px;font-size:30px;color:{cores[i]}">DICIONÁRIO DO GRUPO · {2*i+1}–{2*i+2} DE 6</div>
          <div class="abs" style="left:80px;top:180px;width:920px">{verbete(*a, cores[i])}{verbete(*b, cores[i])}</div>'''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:100px">Faltou alguma? <span class="hl">Comenta.</span></div>
      <div class="abs" style="left:80px;top:420px;width:920px;font-size:46px;line-height:1.3">O Retrozap lê a conversa do seu grupo, no seu celular, e entrega os troféus de 2026 com número: quem fala mais, quem some, quem ri de tudo.</div>
      <div class="abs" style="left:80px;top:880px;font-size:40px;font-weight:700">Manda no grupo e vê quem se ofende.</div>
      <div class="abs" style="left:80px;top:1110px">{assinatura(420)}</div>
      <div class="abs" style="right:80px;top:1155px;font-size:34px;font-weight:700">retrozap.com.br</div>'''))
    piece(id='R-C3', fmt='carrossel', day=1, slot='12h30', title='Dicionário do grupo', w=1080, h=1350,
          html=doc('R-C3', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Dicionário do grupo: o que cada mensagem quer dizer de verdade. 📖\n\n'
                   '"Vamos marcar": não vamos marcar.\n"Tô chegando": tô saindo do banho.\n"Quem topa?": sete visualizações, nenhuma resposta.\n"Depois eu vejo": não vai ver.\n"Gente, rapidinho": textão chegando.\n"Bom dia, grupo": ninguém responde desde terça.\n\n'
                   'Faltou alguma? Comenta. E manda no grupo pra ver quem se ofende 👇\n'
                   'retrozap.com.br · 1º grupo grátis\n#retrozap #grupodeamigos #meme #amigos #resenha'),
          notes='Identidade (motivo de envio). Capa Manga com a taça invertida oficial; páginas Noite com acento por página.')

# =====================================================================================
# R-R4 · Reel meme · POV: o grupo tentando marcar o churrasco do feriado (ter, Noite)
# =====================================================================================
def r_r4():
    T = 15.4
    tl = TL(T)
    s0 = f'''<div {tl.scene(0, 2.8, fin=False)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:120px;{at(.05,'rise')}">POV: o grupo tentando marcar o churrasco do <span class="hl">feriado.</span></div>
      <div class="abs" style="left:780px;top:1050px;--r:8deg;{at(.9,'pop')}">{icon('hamburger', 200)}</div>
    </div>'''
    msgs = [('Lu', 'churras no feriado?', '19:02'), ('Caio', 'bora', '19:02'), ('Pedrão', 'sábado?', '19:05'), ('Bia', 'sábado não posso', '19:11'),
            ('Caio', 'sexta é o feriado gente', '19:12'), ('Rafa', 'sexta eu viajo', '19:40'), ('Lu', 'domingo?', '20:03'), ('Pedrão', 'domingo tem almoço da vó', '20:04'),
            ('Bia', 'então dezembro?', '21:30')]
    stack = ''.join(notif(n, t, h, 290 + i * 140, 2.95 + i * .5) for i, (n, t, h) in enumerate(msgs))
    s1 = f'''<div {tl.scene(2.8, 8.4)}>{stack}<div class="abs sim" style="left:70px;top:1560px">SIMULAÇÃO · NOMES DE EXEMPLO</div></div>'''
    s2 = f'''<div {tl.scene(8.4, 12.2)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:130px;{at(8.5,'rise')}">52 mensagens.</div>
      <div class="abs t" style="left:90px;top:600px;width:900px;font-size:130px;{at(9.2,'rise')}"><span class="hl">0</span> datas.</div>
      <div class="abs" style="left:90px;top:860px;width:900px;font-size:48px;font-weight:700;line-height:1.3;{at(10.0,'fade')}">Fechou: "a gente vê".</div>
      <div class="abs" style="left:760px;top:1040px;--r:-8deg;{at(10.4,'stamp')}">{icon('spiral-calendar-pad', 220)}</div>
    </div>'''
    s3 = f'<div {tl.scene(12.2, T, fout=False)}>{FIM_GRUPO(12.2)}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{s1}{s2}{s3}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:100px;width:920px;font-size:110px">POV: o grupo tentando marcar o churrasco do <span class="hl">feriado.</span></div>
      <div style="position:absolute;left:0;top:0;width:1080px;height:1350px">{notif('Pedrão', 'sábado?', '19:05', 640, 0).replace('animation','x-a')}{notif('Bia', 'sábado não posso', '19:11', 790, 0).replace('animation','x-a')}{notif('Bia', 'então dezembro?', '21:30', 940, 0).replace('animation','x-a')}</div>
      <div class="abs sim" style="left:80px;top:1130px">SIMULAÇÃO · NOMES DE EXEMPLO</div></div>'''
    piece(id='R-R4', fmt='reel', day=2, slot='19h45', title='Meme POV: marcar o churrasco do feriado', total=T, poster=.5, kind='meme',
          html=doc('R-R4', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--noite)'),
          caption=('POV: o grupo tentando marcar o churrasco do feriado. 🍔\n\n'
                   '52 mensagens. 0 datas. Fechou: "a gente vê".\n(Simulação com nomes de exemplo.)\n\n'
                   'Manda no grupo que ainda não marcou nada 👇\n'
                   'retrozap.com.br · 1º grupo grátis\n#retrozap #feriado #churrasco #grupodeamigos #meme #pov'),
          notes='Meme POV com notificações genéricas (sem marca de app) e etiqueta de simulação. Áudio em alta no app.')

# =====================================================================================
# R-C4 · Carrossel casal · As 5 mensagens que todo casal manda (qua, Creme)
# =====================================================================================
def r_c4():
    top = [(5, '"Manda foto"', 96, 'camera-with-flash'), (4, '"Tá onde?"', 198, 'right-pointing-magnifying-glass'), (3, '"O que vamos jantar?"', 287, 'hamburger'),
           (2, '"Já tô indo"', 351, 'rocket'), (1, '"Chegou?"', 412, 'incoming-envelope')]
    pages = [page(f'''
      <div class="abs" style="left:80px;top:90px">{taca(110, 'casal')}</div>
      <div class="abs t" style="left:80px;top:280px;width:920px;font-size:126px">As 5 mensagens que todo casal manda <span class="hl">todo dia.</span></div>
      <div class="abs" style="left:80px;top:860px;display:flex;gap:26px">{''.join(icon(i, 150, 'casal') for *_, i in top[::-1])}</div>
      <div class="abs sim" style="left:80px;top:1230px">CONTAGEM DE EXEMPLO · DANI &amp; CRIS · 2026</div>''', cls='casal')]
    def item(n, txt, num, ic, big=False):
        return f'''<div style="display:flex;align-items:center;gap:34px;padding:{50 if big else 40}px 0;border-top:3px solid var(--clinha)">
          <span class="t" style="font-size:{140 if big else 110}px;color:var(--cereja);width:{120 if big else 100}px">{n}</span>{icon(ic, 150 if big else 120, 'casal')}
          <div><div class="t" style="font-size:{86 if big else 66}px">{txt}</div><div class="mono" style="font-size:34px;margin-top:10px">{num} vezes em 2026</div></div></div>'''
    pages.append(page(f'''<div class="abs mono" style="left:80px;top:90px;font-size:30px;color:var(--cereja)">5º AO 3º LUGAR</div>
      <div class="abs" style="left:80px;top:200px;width:920px">{item(*top[0])}{item(*top[1])}{item(*top[2])}</div>
      <div class="abs sim" style="left:80px;top:1230px">DADOS DE EXEMPLO · DANI &amp; CRIS</div>''', cls='casal'))
    pages.append(page(f'''<div class="abs" style="inset:0;background:var(--rosa1)"></div><div class="abs mono" style="left:80px;top:90px;font-size:30px;color:var(--cereja)">2º LUGAR</div>
      <div class="abs" style="left:80px;top:220px;width:920px">{item(*top[3], big=True)}</div>
      <div class="abs" style="left:80px;top:720px;width:560px;font-size:50px;line-height:1.3">Dito por quem ainda está procurando a chave.</div>
      <div class="abs" style="left:680px;top:820px;transform:rotate(8deg)">{icon('rocket', 300, 'casal')}</div>
      <div class="abs sim" style="left:80px;top:1230px">DADOS DE EXEMPLO · DANI &amp; CRIS</div>''', cls='casal'))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--cereja)"></div>
      <div class="abs mono" style="left:80px;top:90px;font-size:30px;color:var(--creme)">1º LUGAR</div>
      <div class="abs" style="left:80px;top:200px">{icon('incoming-envelope', 220, 'casal')}</div>
      <div class="abs t" style="left:80px;top:500px;width:920px;font-size:200px;color:var(--creme)">"Chegou?"</div>
      <div class="abs t" style="left:80px;top:760px;font-size:96px;color:var(--vinho)">412 vezes.</div>
      <div class="abs" style="left:80px;top:900px;width:880px;font-size:44px;line-height:1.3;color:var(--creme)">Amor também é avisar que chegou.</div>
      <div class="abs sim" style="left:80px;top:1230px;color:var(--creme)">DADOS DE EXEMPLO · DANI &amp; CRIS</div>''', cls='casal'))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:104px">E no de vocês, qual <span class="hl">ganha?</span></div>
      <div class="abs" style="left:80px;top:440px;width:900px;font-size:46px;line-height:1.3">O Retrozap Casais conta as mensagens de vocês dois em 2026, com a conversa lida no seu celular.</div>
      <div class="abs" style="left:80px;top:830px;font-size:42px;font-weight:700">Manda pro seu amor e aposta.</div>
      <div class="abs" style="left:80px;top:1100px">{assinatura(420, 'casal')}</div>
      <div class="abs" style="right:80px;top:1145px;font-size:34px;font-weight:700">retrozap.com.br</div>''', cls='casal'))
    piece(id='R-C4', fmt='carrossel', day=3, slot='12h30', title='Casal: as 5 mensagens de todo dia', w=1080, h=1350,
          html=doc('R-C4', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('As 5 mensagens que todo casal manda todo dia. 💌\n\n'
                   '5. "Manda foto"\n4. "Tá onde?"\n3. "O que vamos jantar?"\n2. "Já tô indo"\n1. "Chegou?"\n\n'
                   '(Contagem de exemplo, do casal Dani & Cris.) No Retrozap Casais, a conta é a de vocês dois.\n'
                   'Manda pro seu amor e aposta qual ganha no de vocês 👇\nretrozap.com.br\n'
                   '#retrozap #casal #namorados #amor #retrospectiva2026'),
          notes='Casa Casal: creme, rosa, cereja e vinho, sem roxo. Números de exemplo (Dani & Cris), marcados em todas as páginas.')

# =====================================================================================
# R-R5 · Reel trend · Me diga que você está no grupo da família sem dizer (qui, Noite)
# =====================================================================================
def r_r5():
    T = 15.0
    tl = TL(T)
    itens = [('"Bom dia" com flor às 6h.', 'black-sun-with-rays', 'var(--manga)'), ('"Quem é esse número?"', 'right-pointing-magnifying-glass', 'var(--piscina)'),
             ('Áudio de 3 minutos da tia.', 'studio-microphone', 'var(--chiclete)'), ('"Lindo!" em todas as fotos.', 'sparkles', 'var(--goiaba)'),
             ('A foto do almoço de domingo.', 'slice-of-pizza', 'var(--uva)')]
    s0 = f'''<div {tl.scene(0, 3.0, fin=False)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:110px;{at(.05,'rise')}">Me diga que você está no grupo da família sem <span class="hl">dizer.</span></div>
    </div>'''
    sc = ''
    t = 3.0
    for i, (txt, ic, cor) in enumerate(itens):
        sc += f'''<div {tl.scene(t, t + 1.9, fade=.08)}>
          <div class="abs" style="inset:0;background:{cor}"></div>
          <div class="abs mono" style="left:90px;top:330px;font-size:34px;color:var(--noite)">{i+1} DE 5</div>
          <div class="abs" style="left:90px;top:440px;{at(t + .05,'pop')}">{icon(ic, 260)}</div>
          <div class="abs t" style="left:90px;top:800px;width:900px;font-size:110px;color:var(--noite);{at(t + .15,'rise')}">{txt}</div>
        </div>'''
        t += 1.9
    s6 = f'''<div {tl.scene(t, t + 2.4)}>
      <div class="abs t" style="left:90px;top:440px;width:900px;font-size:96px;{at(t + .1,'rise')}">O grupo da família também ganha <span class="hl">troféu.</span></div>
      <div class="abs" style="left:390px;top:860px;{at(t + .6,'pop')}">{taca(300)}</div>
    </div>'''
    t += 2.4
    s7 = f'<div {tl.scene(t, T, fout=False)}>{FIM_GRUPO(t)}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{sc}{s6}{s7}</section>'
    cells = ''.join(f'<div style="height:180px;border-radius:30px;background:{c};display:flex;align-items:center;justify-content:center">{icon(i, 120)}</div>' for _, i, c in itens[:4])
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:110px;width:920px;font-size:104px">Me diga que você está no grupo da família sem <span class="hl">dizer.</span></div>
      <div class="abs" style="left:80px;top:720px;width:920px;display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:20px">{cells}</div>
      <div class="abs" style="left:80px;top:960px;font-size:40px;font-weight:700">"Bom dia" com flor às 6h. Já entendemos.</div></div>'''
    piece(id='R-R5', fmt='reel', day=4, slot='19h45', title='Trend "me diga sem dizer": grupo da família', total=T, poster=.12, kind='trend',
          html=doc('R-R5', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--noite)'),
          caption=('Me diga que você está no grupo da família sem dizer. ☀️\n\n'
                   '"Bom dia" com flor às 6h. "Quem é esse número?" Áudio de 3 minutos da tia. "Lindo!" em todas as fotos. A foto do almoço de domingo.\n\n'
                   'O grupo da família também ganha troféu no Retrozap.\n'
                   'Manda no grupo da família (se tiver coragem) 👇\nretrozap.com.br · 1º grupo grátis\n'
                   '#retrozap #grupodafamilia #familia #meme #trend'),
          notes='Trend "me diga X sem dizer X". Sem conversa simulada: só frases e ícones oficiais. Uma cor de apoio por cena, corte seco. Áudio em alta no app.')

# =====================================================================================
# R-C5 · Carrossel · O grupo que viaja junto, em 6 fases (sex 20/11, Chiclete)
# =====================================================================================
def r_c5():
    fases = [('"Bora viajar no feriado?"', 'Dia 1. Todo mundo topa.', 'rocket'), ('A planilha.', 'Alguém sempre faz. Ninguém preenche.', 'clipboard'),
             ('"Quem leva o quê?"', '3 levam gelo. Ninguém leva carvão.', 'handshake'), ('"Racha a conta"', 'Cada um faz uma conta diferente.', 'receipt'),
             ('600 fotos.', '4 prestam. Ninguém sabe quem tirou.', 'camera-with-flash'), ('"Ano que vem de novo?"', 'E o ciclo recomeça.', 'spiral-calendar-pad')]
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--chiclete)"></div>
      <div class="abs t" style="left:80px;top:110px;width:920px;font-size:138px;color:var(--noite)">O grupo que viaja junto, em 6 fases.</div>
      <div class="abs" style="left:80px;top:860px;display:flex;gap:22px">{''.join(icon(i, 140) for *_, i in fases[:5])}</div>
      <div class="abs" style="left:80px;top:1180px"><span class="tag" style="background:var(--noite);border-color:var(--noite)">Feriadão · arrasta →</span></div>''')]
    cores = ['var(--manga)', 'var(--piscina)', 'var(--uva)']
    for i in range(3):
        a, b = fases[2*i], fases[2*i+1]
        blk = lambda f, n, y: f'''<div class="abs box" style="left:80px;top:{y}px;width:920px;height:520px;padding:46px 50px;{'background:' + cores[i] + ';color:var(--noite)' if n % 2 == 0 else ''}">
            <div style="display:flex;justify-content:space-between;align-items:flex-start"><span class="mono" style="font-size:32px">FASE {n}</span>{icon(f[2], 150)}</div>
            <div class="t" style="font-size:100px;margin-top:20px">{f[0]}</div>
            <div style="font-size:48px;font-weight:700;margin-top:24px">{f[1]}</div></div>'''
        pages.append(page(blk(a, 2*i+1, 90) + blk(b, 2*i+2, 680)))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:100px">Em que fase o seu grupo <span class="hl">está?</span></div>
      <div class="abs" style="left:80px;top:440px;width:900px;font-size:46px;line-height:1.3">Depois do feriado, a conversa continua. E no fim do ano, vira troféu no Retrozap.</div>
      <div class="abs" style="left:80px;top:800px;font-size:42px;font-weight:700">Manda no grupo da viagem.</div>
      <div class="abs" style="left:80px;top:1100px">{assinatura(420)}</div>
      <div class="abs" style="right:80px;top:1145px;font-size:34px;font-weight:700">retrozap.com.br</div>'''))
    piece(id='R-C5', fmt='carrossel', day=5, slot='12h30', title='Feriadão: o grupo que viaja junto, em 6 fases', w=1080, h=1350,
          html=doc('R-C5', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('O grupo que viaja junto, em 6 fases. 🧳\n\n'
                   '1. "Bora viajar no feriado?"\n2. A planilha.\n3. "Quem leva o quê?"\n4. "Racha a conta."\n5. 600 fotos.\n6. "Ano que vem de novo?"\n\n'
                   'Em que fase o seu grupo está? Manda no grupo da viagem 👇\n'
                   'retrozap.com.br · 1º grupo grátis\n#retrozap #feriado #viagemcomamigos #grupodeamigos #feriadao'),
          notes='Sexta 20/11 é feriado. Capa Chiclete (cor de apoio) entre a Noite de quinta e a de sábado.')

# =====================================================================================
# R-R6 · Reel produto · A retrospectiva do seu grupo em 3 passos (sáb, Noite)
# =====================================================================================
def r_r6():
    T = 16.0
    tl = TL(T)
    s0 = f'''<div {tl.scene(0, 3.0, fin=False)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:120px;{at(.05,'rise')}">A retrospectiva do seu grupo em <span class="hl">3 passos.</span></div>
      {dots(90, 900, 50, 'var(--manga)', .8)}
    </div>'''
    passos = [('1', 'Exporte a conversa do grupo.', 'Pelo próprio app de mensagens, no celular.', 'mobile-phone-with-rightwards-arrow-at-left', 'var(--piscina)'),
              ('2', 'Abra no retrozap.com.br.', 'O arquivo é lido no seu navegador. Nada vai para servidor.', 'lock', 'var(--chiclete)'),
              ('3', 'Receba os troféus.', 'Um vencedor por categoria, revelado um por um.', None, 'var(--manga)')]
    sc = ''
    t = 3.0
    for n, tit, sub, ic, cor in passos:
        art = icon(ic, 240) if ic else taca(240, inv=True)
        sc += f'''<div {tl.scene(t, t + 3.0, fade=.1)}>
          <div class="abs" style="inset:0;background:{cor}"></div>
          <div class="abs t" style="left:90px;top:300px;font-size:300px;color:var(--noite);{at(t + .05,'pop')}">{n}</div>
          <div class="abs" style="left:700px;top:360px;{at(t + .3,'pop')}">{art}</div>
          <div class="abs t" style="left:90px;top:720px;width:900px;font-size:104px;color:var(--noite);{at(t + .2,'rise')}">{tit}</div>
          <div class="abs" style="left:90px;top:1060px;width:880px;font-size:48px;font-weight:700;line-height:1.3;color:var(--noite);{at(t + .8,'fade')}">{sub}</div>
        </div>'''
        t += 3.0
    s4 = f'''<div {tl.scene(t, T, fout=False)}>
      <div class="abs" style="left:0;right:0;top:420px;display:flex;justify-content:center;{at(t + .1,'pop')}">{assinatura(700)}</div>
      <div class="abs t" style="left:0;right:0;top:700px;text-align:center;font-size:110px;{at(t + .4,'rise')}">1º grupo grátis.</div>
      <div class="abs" style="left:90px;right:90px;top:880px;text-align:center;font-size:46px;font-weight:700;line-height:1.3;{at(t + .8,'fade')}">Acesso completo por R$ 8,99, pagamento único.</div>
      <div class="foot" style="top:1060px;font-size:40px;{at(t + 1.0,'fade')}">retrozap.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{sc}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs" style="left:80px;top:80px">{taca(110)}</div>
      <div class="abs t" style="left:80px;top:250px;width:920px;font-size:120px">A retrospectiva do seu grupo em <span class="hl">3 passos.</span></div>
      <div class="abs" style="left:80px;top:800px;width:920px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
        {''.join(f'<div style="height:300px;border-radius:30px;background:{c};color:var(--noite);padding:26px"><div class="t" style="font-size:110px">{n}</div></div>' for n, _, _, _, c in passos)}</div></div>'''
    piece(id='R-R6', fmt='reel', day=6, slot='19h45', title='Produto: a retrospectiva do grupo em 3 passos', total=T, poster=.4, kind='produto',
          html=doc('R-R6', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--noite)'),
          caption=('A retrospectiva do seu grupo em 3 passos. 🏆\n\n'
                   '1. Exporte a conversa do grupo, no celular.\n2. Abra no retrozap.com.br: o arquivo é lido no seu navegador, nada vai para servidor.\n3. Receba os troféus, revelados um por um.\n\n'
                   '1º grupo grátis. Acesso completo por R$ 8,99, pagamento único.\n'
                   'Manda pro amigo que guarda todos os prints do grupo 👇\nretrozap.com.br (link na bio)\n'
                   '#retrozap #retrospectiva2026 #grupodeamigos #amigos'),
          notes='Peça de produto. Preço e privacidade iguais ao S01 (R$ 8,99, 1º grupo grátis, leitura no navegador). Sem nome de app de terceiros na arte.')

# =====================================================================================
# R-C6 · Carrossel · Grupo de amigos: 2016 × 2026 (dom, Uva)
# =====================================================================================
def r_c6():
    pares = [('"Rolê hoje?"', '"Rolê em 2027?"', 'party-popper', 'couch-and-lamp'), ('Balada até as 5h.', 'Dormi às 22h.', 'fire', 'crescent-moon'),
             ('300 mensagens por dia.', '1 meme por semana.', 'speech-balloon', 'turtle'), ('Foto da festa.', 'Foto do pet.', 'camera-with-flash', 'house-with-garden')]
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--uva)"></div>
      <div class="abs mono" style="left:80px;top:100px;font-size:34px;color:var(--noite)">ANTES × DEPOIS</div>
      <div class="abs t" style="left:80px;top:180px;width:920px;font-size:150px;color:var(--noite)">Grupo de amigos: 2016 × 2026</div>
      <div class="abs" style="left:80px;top:900px;display:flex;gap:30px;align-items:center">{icon('party-popper', 200)}<span class="t" style="font-size:90px;color:var(--noite)">→</span>{icon('couch-and-lamp', 200)}</div>''')]
    for i, (a, b, ia, ib) in enumerate(pares):
        pages.append(page(f'''
          <div class="abs" style="left:0;top:0;width:1080px;height:675px;background:var(--noite)">
            <div class="abs mono" style="left:80px;top:80px;font-size:34px;color:var(--neblina)">2016</div>
            <div class="abs t" style="left:80px;top:180px;width:640px;font-size:96px">{a}</div>
            <div class="abs" style="left:780px;top:200px">{icon(ia, 200)}</div></div>
          <div class="abs" style="left:0;top:675px;width:1080px;height:675px;background:var(--manga);color:var(--noite)">
            <div class="abs mono" style="left:80px;top:80px;font-size:34px">2026</div>
            <div class="abs t" style="left:80px;top:180px;width:640px;font-size:96px">{b}</div>
            <div class="abs" style="left:780px;top:200px">{icon(ib, 200)}</div></div>'''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:100px">Quanto o seu grupo <span class="hl">mudou?</span></div>
      <div class="abs" style="left:80px;top:440px;width:900px;font-size:46px;line-height:1.3">O Retrozap mostra há quanto tempo vocês existem e quanto falaram, ano a ano.</div>
      <div class="abs" style="left:80px;top:800px;font-size:42px;font-weight:700">Manda no grupo mais antigo que você tem.</div>
      <div class="abs" style="left:80px;top:1100px">{assinatura(420)}</div>
      <div class="abs" style="right:80px;top:1145px;font-size:34px;font-weight:700">retrozap.com.br</div>'''))
    piece(id='R-C6', fmt='carrossel', day=7, slot='12h30', title='Antes × depois: grupo de amigos 2016 × 2026', w=1080, h=1350,
          html=doc('R-C6', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Grupo de amigos: 2016 × 2026. 🕰️\n\n'
                   '"Rolê hoje?" virou "rolê em 2027?".\nBalada até as 5h virou dormir às 22h.\n300 mensagens por dia viraram 1 meme por semana.\nFoto da festa virou foto do pet.\n\n'
                   'Manda no grupo mais antigo que você tem 👇\n'
                   'O Retrozap mostra o seu grupo ano a ano. retrozap.com.br · 1º grupo grátis\n#retrozap #amigos #antesedepois #grupodeamigos #nostalgia'),
          notes='Formato antes × depois. Capa Uva fecha a semana; páginas divididas Noite (2016) e Manga (2026).')

# =====================================================================================
# Stories · "Manda no grupo" (frases para print, sem adesivo)
# =====================================================================================
FRASES = [
    (1, 'O print mais perigoso do ano está no seu grupo.', 'eyes', 'grupo', 'var(--noite)', 'var(--areia)', 'var(--manga)'),
    (2, 'Ninguém lê a descrição do grupo.', 'scroll', 'grupo', 'var(--manga)', 'var(--noite)', 'var(--noite)'),
    (3, 'Casal que manda meme um pro outro no mesmo sofá.', 'couch-and-lamp', 'casal', 'var(--creme)', 'var(--vinho)', 'var(--cereja)'),
    (4, 'Todo grupo tem um "kkkk" que não riu.', 'face-with-tears-of-joy', 'grupo', 'var(--noite)', 'var(--areia)', 'var(--manga)'),
    (5, 'Feriado: o único dia em que o grupo marca alguma coisa.', 'spiral-calendar-pad', 'grupo', 'var(--manga)', 'var(--noite)', 'var(--noite)'),
    (6, 'Aniversário no grupo: 40 "parabéns" e nenhum bolo.', 'birthday-cake', 'grupo', 'var(--noite)', 'var(--areia)', 'var(--manga)'),
    (7, '1º grupo grátis. O resto é história.', None, 'grupo', 'var(--manga)', 'var(--noite)', 'var(--noite)'),
]

def r_stories():
    for n, (d, txt, ic, casa, bg, fg, ac) in enumerate(FRASES):
        if d in (1, 5): continue  # v2 tangível (rodada 1 do S02): r_s6(), r_s10()
        art = icon(ic, 240, casa) if ic else taca(240, inv=True)
        last = d == 7
        body = f'''<section class="page {'casal' if casa == 'casal' else ''}" style="width:1080px;height:1920px;background:{bg};color:{fg}">
          <div class="abs" style="left:80px;top:300px">{art}</div>
          <div class="abs t" style="left:80px;top:620px;width:920px;font-size:{130 if len(txt) < 40 else 112}px">{txt}</div>
          <div class="abs" style="left:80px;top:1330px;width:920px;font-size:44px;font-weight:700;color:{ac}">{'retrozap.com.br' if last else 'Tira print e manda no grupo.'}</div>
          <div class="abs" style="left:80px;top:1430px">{assinatura(300, casa, inv=(bg not in ('var(--noite)', 'var(--creme)')))}</div>
        </section>'''
        sid = f'R-S{5 + n + 1}'
        piece(id=sid, fmt='story', day=d, title=f'Frase pro grupo: {txt}', w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker='', kind='story',
              notes='Sem adesivo: frase pronta para print (motivo de envio: identidade). ' + ('Casa Casal, sem roxo.' if casa == 'casal' else 'Casa Grupo.'))


def r_s6():
    """v2: a tela da retrospectiva no celular (Gui: mais tangível, mostrar o produto)."""
    trof = [('speech-balloon', 'O Tagarela', 'Pedrão', '3.940 mensagens', 'var(--manga)'), ('studio-microphone', 'Podcaster do Grupo', 'Juninho', '171 áudios', 'var(--piscina)'),
            ('ghost', 'O Fantasma', 'Rafa', 'visualizou 212 vezes sem responder', 'var(--uva)')]
    cards = ''.join(f'''<div style="margin:0 26px 20px;background:var(--acai);border-radius:30px;padding:24px 26px;display:flex;gap:22px;align-items:center">
        <div style="flex:none;width:96px;height:96px;border-radius:24px;background:{c};display:flex;align-items:center;justify-content:center">{icon(i, 80)}</div>
        <div style="min-width:0"><div class="mono" style="font-size:22px;color:var(--neblina)">{t.upper()}</div><div class="t" style="font-size:52px;margin-top:6px">{n}</div><div style="font-size:26px;margin-top:6px;color:var(--neblina)">{d}</div></div></div>''' for i, t, n, d, c in trof)
    tela = f'''<div style="position:absolute;inset:0;background:var(--noite);color:var(--areia)">
      <div style="padding:30px 26px 10px;display:flex;align-items:center;gap:18px">{taca(64)}<div><div class="t" style="font-size:40px">Turma do Churras</div><div class="mono" style="font-size:22px;color:var(--neblina)">RETROSPECTIVA 2026 · ATO II</div></div></div>
      <div class="t" style="font-size:58px;padding:20px 26px 26px">Os troféus</div>{cards}
      <div class="mono" style="text-align:center;font-size:22px;color:var(--neblina);margin-top:10px">toque para revelar o próximo →</div></div>'''
    body = f'''<section class="page" style="width:1080px;height:1920px">
      <div class="abs t" style="left:80px;top:260px;width:920px;font-size:76px">Assim chega a retrospectiva do seu <span class="hl">grupo.</span></div>
      <div class="abs" style="left:200px;top:500px">{C.phone(tela, 680, 950, screen='#1A0B2E', frame='#0B0414', status_color='#FFF4E0', hora='21:40')}</div>
      <div class="abs" style="left:80px;top:1480px">{assinatura(300)}</div>
    </section>'''
    piece(id='R-S6', fmt='story', day=1, title='A tela da retrospectiva no celular', w=1080, h=1920, html=doc('R-S6', FONTS, CSS, body, 1080, 1920),
          caption='(story, sem legenda)', sticker='', kind='story',
          notes='v3: sem "1º grupo grátis" e sem etiqueta (seu comentário: é conteúdo, não site). Tela da retrospectiva num celular, Ato II com três troféus.')

def r_s10():
    """v2: conversa do grupo no feriado, num celular (simulação, sem marca de app)."""
    head = f'''<div style="height:110px;background:var(--noite);color:var(--areia);display:flex;align-items:center;gap:18px;padding:0 26px">
      <div style="width:70px;height:70px;border-radius:50%;background:var(--manga);display:flex;align-items:center;justify-content:center">{icon('hamburger', 50)}</div>
      <div><div style="font:800 34px/1.1 'Bricolage Grotesque'">Turma do Churras</div><div style="font-size:22px;color:var(--neblina)">Lu, Caio, Pedrão, Bia, Rafa, você</div></div></div>'''
    msgs = (C.bubble('gente quem tá com a chave da casa?', nome='Lu', hora='09:12', fs=30) +
            C.bubble('tava comigo, deixei com a Bia', nome='Pedrão', hora='09:14', fs=30) + C.bubble('deixei embaixo do tapete', nome='Bia', hora='09:31', fs=30) +
            C.bubble('QUE TAPETE', nome='Rafa', hora='09:31', fs=30) + C.bubble('tô chegando', me=True, hora='09:40', bg_me='#FFE3A3', fs=30))
    tela = f'<div style="position:absolute;inset:0;background:#F3EDE2">{head}<div style="padding-top:16px">{msgs}</div></div>'
    body = f'''<section class="page" style="width:1080px;height:1920px;background:var(--manga);color:var(--noite)">
      <div class="abs t" style="left:80px;top:260px;width:920px;font-size:84px">Feriado no grupo, versão real.</div>
      <div class="abs" style="left:200px;top:470px">{C.phone(tela, 680, 980, screen='#F3EDE2', frame='#1A0B2E', status_color='#1A0B2E', hora='09:41')}</div>
      <div class="abs" style="left:80px;top:1475px;font-size:36px;font-weight:700">No fim do ano, isso vira troféu.</div>
    </section>'''
    piece(id='R-S10', fmt='story', day=5, title='Conversa do grupo no feriado (simulação)', w=1080, h=1920, html=doc('R-S10', FONTS, CSS, body, 1080, 1920),
          caption='(story, sem legenda)', sticker='', kind='story',
          notes='v3: sem etiqueta de simulação (seu comentário). Conversa do grupo no feriado num celular genérico, sem marca de app.')

r_c3(); r_r4(); r_c4(); r_r5(); r_c5(); r_r6(); r_c6(); r_stories(); r_s6(); r_s10()
