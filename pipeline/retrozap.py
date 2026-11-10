"""Retrozap · Pack Semanal 03. Bricolage Grotesque 800 / DM Sans / DM Mono.
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
# S03 · 23–29/11/2026
# =====================================================================================
CSS += """
@keyframes knob{0%{transform:translateX(0)}100%{transform:translateX(var(--kx,74px))}}
@keyframes blinkk{0%,100%{opacity:1}50%{opacity:.3}}
.note{background:#FFF4E0;color:var(--noite);border-radius:30px;box-shadow:0 30px 60px rgba(0,0,0,.35);
  background-image:repeating-linear-gradient(transparent 0 78px,#E9D9BC 78px 81px)}
.ck{flex:none;width:58px;height:58px;border-radius:16px;border:5px solid var(--noite);display:flex;align-items:center;justify-content:center;font:800 40px/1 'Bricolage Grotesque'}
.esc{display:inline-block;color:var(--chiclete);font-weight:700;transform:rotate(-1.5deg)}
.lbl{display:inline-block;font-family:'DM Mono',monospace;font-weight:500;border-radius:14px;padding:12px 24px}
"""

SIM = '<span class="sim">simulação · nomes de exemplo</span>'

def fim(t, frase='e o seu grupo?', top=470):
    """Encerramento dos reels do S03 (sem preço e sem '1º grupo grátis' na arte)."""
    return f'''<div class="abs" style="left:0;right:0;top:{top}px;display:flex;justify-content:center;{at(t + .1,'pop')}">{assinatura(700)}</div>
      <div class="abs t" style="left:90px;right:90px;top:{top + 290}px;text-align:center;font-size:88px;{at(t + .4,'rise')}">{frase}</div>
      <div class="foot" style="top:{top + 640}px;font-size:42px;{at(t + .9,'fade')}">retrozap.com.br</div>'''

def chat_head(sub='Lu, Caio, Pedrão, Bia, Rafa, você'):
    return f'''<div style="height:110px;background:var(--noite);color:var(--areia);display:flex;align-items:center;gap:18px;padding:0 26px">
      <div style="width:70px;height:70px;border-radius:50%;background:var(--manga);display:flex;align-items:center;justify-content:center">{icon('hamburger', 50)}</div>
      <div><div style="font:800 34px/1.1 'Bricolage Grotesque'">Turma do Churras</div><div style="font-size:22px;color:var(--neblina)">{sub}</div></div></div>'''

def toggle(t_on, cor='var(--manga)', kx=74, stuck=False):
    """Chave liga/desliga desenhada pela marca (não copia interface de terceiros)."""
    k = (f'animation:knob .45s cubic-bezier(.2,.8,.2,1) {t_on:.2f}s 1 both,blinkk .7s linear {t_on + .5:.2f}s 4' if stuck
         else f'animation:knob .4s cubic-bezier(.34,1.56,.64,1) {t_on:.2f}s 1 both')
    on = '' if stuck else f'<div style="position:absolute;inset:0;border-radius:48px;background:{cor};opacity:0;animation:fade .25s linear {t_on:.2f}s 1 both"></div>'
    return (f'<div style="position:relative;flex:none;width:170px;height:96px;border-radius:48px;background:var(--linha)">{on}'
            f'<div style="position:absolute;left:10px;top:10px;width:76px;height:76px;border-radius:50%;background:var(--areia);box-shadow:0 4px 10px rgba(0,0,0,.3);--kx:{kx}px;{k}"></div></div>')

def toggle_static(on=True, cor='var(--manga)', half=False):
    x = 37 if half else (74 if on else 0)
    return (f'<div style="position:relative;flex:none;width:170px;height:96px;border-radius:48px;background:{cor if on and not half else "var(--linha)"}">'
            f'<div style="position:absolute;left:{10 + x}px;top:10px;width:76px;height:76px;border-radius:50%;background:var(--areia)"></div></div>')

# =====================================================================================
# R-R8 · Reel trend "ligar/desligar" · Modo dezembro ativado no grupo (seg, Noite)
# =====================================================================================
LINHAS_DEZ = [
    ('party-popper', 'Amigo secreto', 'var(--manga)', False, None),
    ('sparkles', 'Figurinha de Natal', 'var(--piscina)', False, None),
    ('incoming-envelope', 'Lista de presentes com link', 'var(--chiclete)', False, None),
    ('spiral-calendar-pad', 'Confra marcada', 'var(--goiaba)', True, 'em votação desde outubro'),
    ('marca', 'Retrospectiva do grupo', 'var(--manga)', False, None),
]

def r_r8():
    T = 17.0
    tl = TL(T)
    s0 = f'''<div {tl.scene(0, 3.4, fin=False)}>
      <div class="abs mono" style="left:90px;top:420px;font-size:36px;color:var(--neblina);{at(.05,'fade')}">TURMA DO CHURRAS · CONFIGURAÇÕES</div>
      <div class="abs t" style="left:90px;top:500px;width:900px;font-size:150px;{at(.15,'rise')}">Modo dezembro:</div>
      <div class="abs" style="left:90px;top:820px;display:flex;align-items:center;gap:40px;transform:scale(1.6);transform-origin:left center">{toggle(1.3)}</div>
      <div class="abs t hl" style="left:470px;top:790px;font-size:130px;opacity:0;{at(1.5,'stamp')}">ATIVADO</div>
    </div>'''
    rows, t = '', 3.7
    for i, (ic, txt, cor, stuck, sub) in enumerate(LINHAS_DEZ):
        last = i == len(LINHAS_DEZ) - 1
        subh = f'<div class="mono" style="font-size:32px;color:var(--goiaba);margin-top:6px;{at(t + 1.0,"fade")}">{sub}…</div>' if sub else ''
        rows += f'''<div style="display:flex;align-items:center;gap:28px;background:{'var(--acai)' if not last else 'var(--acai2)'};border:{'5px solid var(--manga)' if last else '3px solid var(--linha)'};border-radius:36px;padding:32px 32px;margin-bottom:28px;{at(t,'slideR')}">
          <div style="flex:none;width:100px;height:100px;border-radius:26px;background:var(--areia);display:flex;align-items:center;justify-content:center">{icon(ic, 80)}</div>
          <div style="flex:1;min-width:0"><div style="font-size:50px;font-weight:700;line-height:1.15">{txt}</div>{subh}</div>{toggle(t + .7, cor, stuck=stuck, kx=37 if stuck else 74)}</div>'''
        t += 1.7 if not stuck else 2.4
    s1 = f'''<div {tl.scene(3.4, 13.6)}>
      <div class="abs mono" style="left:90px;top:300px;font-size:32px;color:var(--neblina)">MODO DEZEMBRO · ATIVADO</div>
      <div class="abs" style="left:70px;top:370px;width:940px">{rows}</div>
    </div>'''
    s2 = f'<div {tl.scene(13.6, T, fout=False)}>{fim(13.6, "Dezembro chegou no grupo.")}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{s1}{s2}</section>'
    crow = ''.join(f'''<div style="display:flex;align-items:center;gap:24px;background:var(--acai);border:3px solid var(--linha);border-radius:30px;padding:18px 26px;margin-bottom:18px">
        <div style="flex:none;width:80px;height:80px;border-radius:22px;background:var(--areia);display:flex;align-items:center;justify-content:center">{icon(ic, 64)}</div>
        <div style="flex:1;font-size:40px;font-weight:700">{txt}</div>{toggle_static(True, cor, half=stuck)}</div>''' for ic, txt, cor, stuck, _ in LINHAS_DEZ)
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:120px">Modo dezembro: <span class="hl">ativado.</span></div>
      <div class="abs" style="left:80px;top:400px;width:920px">{crow}</div></div>'''
    piece(id='R-R8', fmt='reel', day=1, slot='19h45', title='Trend liga/desliga: modo dezembro ativado no grupo', total=T, poster=.55, kind='trend',
          html=doc('R-R8', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--noite)'),
          caption=('Modo dezembro: ativado no grupo. 🎄\n\n'
                   'Amigo secreto: ligado.\nFigurinha de Natal: ligada.\nLista de presentes com link: ligada.\nConfra marcada: em votação desde outubro.\n\n'
                   'Manda no grupo que ainda não marcou a confra 👇\n'
                   'No fim do ano, o Retrozap transforma a conversa do grupo em retrospectiva. retrozap.com.br\n'
                   '#retrozap #dezembro #amigosecreto #confraternizacao #grupodeamigos #trend'),
          notes='Trend "liga/desliga" (doc do DOT de 06/11): chaves desenhadas pela marca, sem interface de terceiros. A chave da confra trava no meio (piada). Motivo de envio: marcar o grupo que não marcou a confra. Áudio em alta no app.')

# =====================================================================================
# R-C7 · Carrossel · Amigo secreto do grupo: o regulamento (bloco de notas) (ter, capa Manga)
# =====================================================================================
REGRAS = [
    ('Valor: R$&nbsp;50.', 'Alguém vai dar um de R$&nbsp;20 e dizer que "achou a sua cara".'),
    ('Sorteio até sexta.', 'Vai ser refeito 3 vezes. Alguém sempre tira a si mesmo.'),
    ('Cada um manda a lista de desejos.', 'Uma pessoa manda. O resto: "qualquer coisa tá bom".'),
    ('Ninguém revela quem tirou.', 'Revelado no mesmo dia. Por áudio.'),
    ('Troca no dia da confra.', 'Alguém vai esquecer o presente em casa.'),
]

def r_c7():
    def nota(inner, h=1090, rot=0):
        return (f'<div class="abs note" style="left:90px;top:150px;width:900px;height:{h}px;transform:rotate({rot}deg);overflow:hidden">'
                f'<div style="height:110px;background:#F6E7C8;display:flex;align-items:center;justify-content:space-between;padding:0 40px;font:700 30px/1 \'DM Sans\';color:#8A6A2E">'
                f'<span>‹ Notas</span><span>amigo secreto 2026</span><span>Feito</span></div>'
                f'<div style="padding:40px 50px">{inner}</div></div>')
    capa_nota = nota(f'''<div class="t" style="font-size:96px;line-height:1">Regulamento do amigo secreto</div>
        <div style="font-size:40px;margin-top:30px;line-height:1.5;font-weight:700">Turma do Churras · 2026</div>
        <div style="margin-top:50px;font-size:40px;line-height:2;font-weight:500">1. Valor…<br>2. Sorteio…<br>3. Lista…</div>''', 760, -3)
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--manga)"></div>
      {capa_nota.replace('top:150px', 'top:100px')}
      <div class="abs" style="left:760px;top:760px;transform:rotate(10deg)">{icon('party-popper', 230)}</div>
      <div class="abs t" style="left:90px;top:960px;width:900px;font-size:76px;color:var(--noite)">O que está escrito × o que vai acontecer.</div>
      <div class="abs" style="left:90px;top:1200px"><span class="tag" style="background:var(--noite);border-color:var(--noite)">Arrasta →</span></div>''')]
    for i in range(0, len(REGRAS), 2):
        bloco = ''
        for j, (regra, real) in enumerate(REGRAS[i:i + 2]):
            n = i + j + 1
            bloco += f'''<div style="display:flex;gap:26px;align-items:flex-start;margin-bottom:70px">
              <div class="ck">✓</div><div style="flex:1"><div class="t" style="font-size:86px;line-height:1.02">{n}. {regra}</div>
              <div class="esc" style="font-size:52px;line-height:1.3;margin-top:26px">→ {real}</div></div></div>'''
        if i + 2 > len(REGRAS):
            bloco += f'''<div style="display:flex;gap:26px;align-items:flex-start;margin-bottom:70px">
              <div class="ck"></div><div style="flex:1"><div class="t" style="font-size:86px;line-height:1.02">6. ________</div>
              <div class="esc" style="font-size:52px;line-height:1.3;margin-top:22px">→ comenta a regra que falta no seu grupo.</div></div></div>'''
        pages.append(page(f'''
          {nota(bloco, 1050, 1.5 if i % 4 else -1.5)}
          <div class="abs mono" style="left:90px;top:1250px;font-size:28px;color:var(--neblina)">{f'REGRAS {i+1}–{i+2}' if i + 2 <= len(REGRAS) else f'REGRA {i+1}'} DE {len(REGRAS)}</div>'''))
    pages.append(page(f'''
      <div class="abs" style="left:80px;top:120px">{icon('incoming-envelope', 200)}</div>
      <div class="abs t" style="left:80px;top:380px;width:920px;font-size:100px">Cola no grupo antes do <span class="hl">sorteio.</span></div>
      <div class="abs" style="left:80px;top:700px;width:900px;font-size:46px;line-height:1.3">E em dezembro, o Retrozap lê a conversa do grupo e entrega os troféus do ano.</div>
      <div class="abs" style="left:80px;top:1110px">{assinatura(420)}</div>
      <div class="abs" style="right:80px;top:1155px;font-size:34px;font-weight:700">retrozap.com.br</div>'''))
    piece(id='R-C7', fmt='carrossel', day=2, slot='12h30', title='Amigo secreto do grupo: o regulamento (bloco de notas)', kind='engajamento', w=1080, h=1350,
          html=doc('R-C7', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Regulamento do amigo secreto do grupo: o que está escrito × o que vai acontecer. 🎁\n\n'
                   '1. Valor: R$ 50. Alguém vai dar um de R$ 20.\n2. Sorteio até sexta. Vai ser refeito 3 vezes.\n3. Lista de desejos. "Qualquer coisa tá bom."\n4. Ninguém revela quem tirou. Revelado no mesmo dia, por áudio.\n5. Troca no dia da confra. Alguém esquece o presente.\n\n'
                   'Manda no grupo do amigo secreto antes do sorteio 👇\n'
                   'retrozap.com.br\n#amigosecreto #amigooculto #retrozap #grupodeamigos #natal'),
          notes='Bloco de notas genérico (sem marca de app) com o "realidade" rabiscado em Chiclete. Motivo de envio: colar no grupo antes do sorteio. Capa Manga, páginas Noite.')

# =====================================================================================
# R-R9 · Reel meme · "gente, preciso contar uma coisa" (qua, capa Piscina)
# =====================================================================================
MSGS_R9 = [
    ('gente, preciso contar uma coisa', 'Lu', '22:14', False, 3.9),
    ('FALA', 'Pedrão', '22:14', False, 5.0),
    ('conta logo', 'Bia', '22:14', False, 5.6),
    ('é bom ou ruim??', 'Caio', '22:15', False, 6.2),
    ('oi', 'Rafa', '22:15', False, 6.9),
    ('liga aqui agora', None, '22:15', True, 7.6),
    ('deixa, amanhã eu conto', 'Lu', '22:31', False, 9.4),
]

def r_r9():
    T = 16.0
    tl = TL(T)
    s0 = f'''<div {tl.scene(0, 3.6, fin=False)}>
      <div class="abs" style="inset:0;background:var(--piscina)"></div>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:120px;color:var(--noite);{at(.05,'rise')}">Ninguém:</div>
      <div class="abs t" style="left:90px;top:640px;width:900px;font-size:92px;color:var(--noite);{at(.9,'rise')}">O grupo depois de um "preciso contar uma coisa":</div>
    </div>'''
    bl = ''.join(f'<div style="{at(t,"rise",.3)}">{C.bubble(txt, me=me, nome=n or "", hora=h, bg_me="#FFE3A3", fs=31)}</div>' for txt, n, h, me, t in MSGS_R9)
    tela = f'<div style="position:absolute;inset:0;background:#F3EDE2">{chat_head()}<div style="padding-top:18px">{bl}</div></div>'
    s1 = f'''<div {tl.scene(3.6, 12.6)}>
      <div class="abs" style="left:150px;top:290px">{C.phone(tela, 780, 1240, screen='#F3EDE2', frame='#0B0414', status_color='#1A0B2E', hora='22:31')}</div>
      <div class="abs" style="left:330px;top:1080px;--r:-5deg;white-space:nowrap;{at(7.1,'pop')}"><span class="lbl" style="background:var(--manga);color:var(--noite);font-size:30px;box-shadow:0 8px 0 var(--noite)">← o Rafa, sumido desde março</span></div>
      <div class="abs" style="left:150px;top:560px;--r:-4deg;{at(10.4,'stamp')}"><div class="t" style="background:var(--chiclete);color:var(--areia);padding:18px 40px;font-size:84px;box-shadow:0 12px 0 var(--noite)">Ninguém dormiu.</div></div>
      <div class="abs" style="left:0;right:0;top:1545px;text-align:center;color:var(--neblina)">{SIM}</div>
    </div>'''
    s2 = f'<div {tl.scene(12.6, T, fout=False)}>{fim(12.6, "Todo grupo tem uma Lu.")}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{s1}{s2}</section>'
    bls = ''.join(C.bubble(txt, me=me, nome=n or '', hora=h, bg_me='#FFE3A3', fs=30) for txt, n, h, me, t in MSGS_R9[:5])
    tela_c = f'<div style="position:absolute;inset:0;background:#F3EDE2">{chat_head()}<div style="padding-top:14px">{bls}</div></div>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:var(--piscina);color:var(--noite)">
      <div class="abs t" style="left:70px;top:90px;width:460px;font-size:84px">"Gente, preciso contar uma coisa."</div>
      <div class="abs" style="left:70px;top:620px;width:420px;font-size:40px;font-weight:700;line-height:1.3">E o grupo inteiro acordou.</div>
      <div class="abs" style="left:530px;top:70px">{C.phone(tela_c, 500, 1000, screen='#F3EDE2', frame='#0B0414', status_color='#1A0B2E', hora='22:15')}</div>
      <div class="abs" style="left:70px;top:820px">{icon('eyes', 200)}</div></div>'''
    piece(id='R-R9', fmt='reel', day=3, slot='19h45', title='Meme "Ninguém:": o grupo depois de um "preciso contar uma coisa"', total=T, poster=.62, kind='meme',
          html=doc('R-R9', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--piscina)'),
          caption=('Ninguém:\nO grupo depois de um "gente, preciso contar uma coisa": 👀\n\n'
                   'FALA. Conta logo. É bom ou ruim? Até o Rafa, sumido desde março, apareceu.\n'
                   'E a resposta: "deixa, amanhã eu conto".\n\n'
                   'Marca a Lu do seu grupo 👇\n'
                   'retrozap.com.br\n#retrozap #grupodeamigos #meme #amigos #fofoca'),
          notes='Meme "Ninguém:" com conversa num celular genérico (sem marca de app), etiqueta "simulação · nomes de exemplo", Turma do Churras. Motivo de envio: marcar a "Lu" do grupo. Capa Piscina.')

# =====================================================================================
# R-C8 · Carrossel casal · 5 apostas que a conversa de vocês responde (qui, Casa Casal, Creme)
# =====================================================================================
APOSTAS = [
    ('Quem manda "bom dia" primeiro?', 'black-sun-with-rays'),
    ('Quem demora mais para responder?', 'turtle'),
    ('Quem pede desculpa primeiro?', 'face-with-pleading-eyes'),
    ('Quem manda mais áudio?', 'studio-microphone'),
    ('Quem manda foto da comida antes de comer?', 'hamburger'),
]

def r_c8():
    def chips(sel=None):
        c = lambda t, on: (f'<div style="flex:1;text-align:center;border-radius:28px;padding:30px 0;font:800 58px/1 \'Bricolage Grotesque\';'
                           f'background:{"var(--cereja)" if on else "#fff"};color:{"var(--creme)" if on else "var(--vinho)"};border:4px solid var(--cereja)">{t}</div>')
        return f'<div style="display:flex;gap:26px">{c("EU", sel == 0)}{c("VOCÊ", sel == 1)}</div>'
    pages = [page(f'''
      <div class="abs mono" style="left:80px;top:100px;font-size:32px;color:var(--cereja)">TESTE DO CASAL · 5 APOSTAS</div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:128px">A conversa de vocês sabe a <span class="hl">resposta.</span></div>
      <div class="abs" style="left:80px;top:720px;width:560px;background:#fff;border-radius:40px;padding:40px;box-shadow:0 20px 50px rgba(94,11,43,.15);transform:rotate(-2deg)">
        <div style="font-size:40px;font-weight:700;margin-bottom:30px">Quem manda "bom dia" primeiro?</div>{chips()}</div>
      <div class="abs" style="left:700px;top:820px;transform:rotate(8deg)">{icon('revolving-hearts', 280, 'casal')}</div>
      <div class="abs" style="left:80px;top:1200px"><span class="tag">Arrasta e responde junto →</span></div>''', cls='casal')]
    for i, (q, ic) in enumerate(APOSTAS):
        pages.append(page(f'''
          <div class="abs mono" style="left:80px;top:100px;font-size:32px;color:var(--cereja)">APOSTA {i+1} DE 5</div>
          <div class="abs" style="left:80px;top:180px;width:920px;height:960px;background:#fff;border-radius:48px;box-shadow:0 24px 60px rgba(94,11,43,.14)">
            <div class="abs" style="left:60px;top:60px">{icon(ic, 240, 'casal')}</div>
            <div class="abs t" style="left:60px;top:360px;width:800px;font-size:104px">{q}</div>
            <div class="abs" style="left:60px;top:740px;width:800px">{chips()}</div></div>
          <div class="abs" style="left:80px;top:1200px;font-size:36px;font-weight:700">Cada um responde. Depois confiram na conversa.</div>''', cls='casal'))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--cereja)"></div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:104px;color:var(--creme)">Quantas vocês acertaram juntos?</div>
      <div class="abs" style="left:80px;top:500px;width:900px;font-size:46px;line-height:1.3;color:var(--creme)">O Retrozap faz a retrospectiva do casal com a conversa de vocês, lida no seu celular.</div>
      <div class="abs" style="left:80px;top:830px;font-size:44px;font-weight:700;color:var(--creme)">Manda pro seu amor e apostem.</div>
      <div class="abs" style="left:80px;top:1110px">{assinatura(420, 'casal', inv=True)}</div>
      <div class="abs" style="right:80px;top:1155px;font-size:34px;font-weight:700;color:var(--creme)">retrozap.com.br</div>''', cls='casal'))
    piece(id='R-C8', fmt='carrossel', day=4, slot='12h30', title='Casal: 5 apostas que a conversa de vocês responde', kind='engajamento', w=1080, h=1350,
          html=doc('R-C8', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('5 apostas para o casal. A conversa de vocês sabe a resposta. 💬❤️\n\n'
                   '1. Quem manda "bom dia" primeiro?\n2. Quem demora mais para responder?\n3. Quem pede desculpa primeiro?\n4. Quem manda mais áudio?\n5. Quem manda foto da comida antes de comer?\n\n'
                   'Manda pro seu amor, cada um responde e depois confiram 👇\n'
                   'retrozap.com.br\n#casal #namorados #retrozap #casais #teste'),
          notes='Casa Casal (Creme + Cereja, sem roxo). Cartão de aposta com botões EU/VOCÊ. Motivo de envio: mandar pro parceiro e apostar. Não promete métrica específica do produto.')

# =====================================================================================
# R-R10 · Reel trend "minivlog com rótulos" · Black Friday no grupo (sex 27/11, Noite)
# =====================================================================================
VLOG = [
    ('00:01', 'Chega o primeiro link de promoção.', 'incoming-envelope', 'var(--manga)'),
    ('08:30', '"Alguém divide o frete comigo?"', 'handshake', 'var(--piscina)'),
    ('12:15', 'Print do carrinho. Sem contexto.', 'camera-with-flash', 'var(--chiclete)'),
    ('15:40', '"Tá mais caro que semana passada."', 'right-pointing-magnifying-glass', 'var(--goiaba)'),
    ('21:00', '"Comprei. Não precisava."', 'face-with-pleading-eyes', 'var(--uva)'),
    ('23:59', '"Alguém sabe como devolve?"', 'wastebasket', 'var(--manga)'),
]

def r_r10():
    T = 19.0
    tl = TL(T)
    s0 = f'''<div {tl.scene(0, 3.0, fin=False)}>
      <div class="abs" style="left:90px;top:380px;{at(.05,'pop')}"><span class="lbl" style="background:var(--chiclete);color:var(--areia);font-size:34px">SEX 27/11 · MINIVLOG</span></div>
      <div class="abs t" style="left:90px;top:480px;width:900px;font-size:136px;{at(.2,'rise')}">Black Friday no <span class="hl">grupo.</span></div>
      <div class="abs" style="left:700px;top:960px;--r:8deg;{at(.7,'drop')}">{icon('receipt', 260)}</div>
    </div>'''
    sc, t, d = '', 3.0, 2.15
    seg = lambda k: ''.join(f'<div style="flex:1;height:10px;border-radius:5px;background:{"var(--areia)" if j <= k else "var(--linha)"}"></div>' for j in range(len(VLOG)))
    for i, (h, txt, ic, cor) in enumerate(VLOG):
        sc += f'''<div {tl.scene(t, t + d, fade=.08)}>
          <div class="abs" style="left:90px;right:90px;top:300px;display:flex;gap:10px">{seg(i)}</div>
          <div class="abs" style="left:90px;top:400px;--r:-3deg;{at(t + .02,'stamp')}"><span class="lbl" style="background:{cor};color:var(--noite);font-size:64px;padding:16px 34px">{h}</span></div>
          <div class="abs" style="left:90px;top:620px;width:900px;height:600px;border-radius:48px;background:{cor};{at(t + .05,'pop')}">
            <div class="abs" style="left:310px;top:110px">{icon(ic, 380)}</div></div>
          <div class="abs t" style="left:90px;top:1270px;width:900px;font-size:76px;{at(t + .2,'rise')}">{txt}</div>
        </div>'''
        t += d
    s7 = f'<div {tl.scene(t, T, fout=False)}>{fim(t, "Esse grupo merece uma retrospectiva.")}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{sc}{s7}</section>'
    cells = ''.join(f'<div style="border-radius:30px;background:{c};padding:22px;display:flex;flex-direction:column;align-items:center;gap:12px"><span class="lbl" style="background:var(--noite);color:var(--areia);font-size:30px;padding:8px 16px">{h}</span>{icon(i, 130)}</div>' for h, _, i, c in VLOG)
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs" style="left:80px;top:90px"><span class="lbl" style="background:var(--chiclete);color:var(--areia);font-size:32px">MINIVLOG · 00:01 → 23:59</span></div>
      <div class="abs t" style="left:80px;top:190px;width:920px;font-size:130px">Black Friday no <span class="hl">grupo.</span></div>
      <div class="abs" style="left:80px;top:620px;width:920px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px">{cells}</div></div>'''
    piece(id='R-R10', fmt='reel', day=5, slot='19h45', title='Trend minivlog com rótulos: Black Friday no grupo', total=T, poster=.4, kind='trend',
          html=doc('R-R10', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--noite)'),
          caption=('Black Friday no grupo, um minivlog. 🛒\n\n'
                   '00:01 chega o primeiro link de promoção.\n08:30 "alguém divide o frete comigo?"\n12:15 print do carrinho, sem contexto.\n15:40 "tá mais caro que semana passada."\n21:00 "comprei. não precisava."\n23:59 "alguém sabe como devolve?"\n\n'
                   'Manda no grupo que virou central de cupom hoje 👇\n'
                   'retrozap.com.br\n#blackfriday #retrozap #grupodeamigos #meme #trend'),
          notes='Trend "minivlog com rótulos" (doc do DOT de 06/11) no dia da Black Friday. Rótulos de hora e barra de progresso desenhados pela marca, ícones oficiais. Sem marca de loja. Sai no dia: se perder a janela, cai. Áudio em alta no app.')

# =====================================================================================
# R-C9 · Carrossel · O ano do grupo em 12 meses (sáb, capa Goiaba)
# =====================================================================================
MESES = [
    ('JAN', 'Lista de metas do grupo: viagem, academia e churrasco todo mês.'),
    ('FEV', 'Carnaval: 214 fotos. As mesmas 3 pessoas em todas.'),
    ('MAR', 'Alguém troca a foto do grupo. Começa a guerra.'),
    ('ABR', '11 dias de silêncio. Ninguém sabe por quê.'),
    ('MAI', 'O churrasco do mês, finalmente. O primeiro.'),
    ('JUN', 'Bolão da Copa: 9 palpitaram, 1 pagou.'),
    ('JUL', 'Festa julina: "quem leva o quê" em 80 mensagens.'),
    ('AGO', 'Aniversário do grupo. Ninguém lembrou.'),
    ('SET', 'Sai o primeiro "bora marcar a confra?"'),
    ('OUT', 'Abre a votação da data da confra.'),
    ('NOV', '"Esse ano passou rápido, hein."'),
]

def r_c9():
    def folha(m, txt, cor):
        holes = ''.join('<span style="width:22px;height:22px;border-radius:50%;background:var(--noite)"></span>' for _ in range(8))
        return f'''<div style="background:var(--areia);color:var(--noite);border-radius:30px;overflow:hidden;margin-bottom:30px;display:flex;height:300px">
          <div style="flex:none;width:250px;background:{cor};display:flex;flex-direction:column;align-items:center;justify-content:center">
            <div style="display:flex;gap:6px;margin-bottom:20px">{holes[:len(holes)//2]}</div><div class="t" style="font-size:96px">{m}</div><div class="mono" style="font-size:24px;margin-top:6px">2026</div></div>
          <div style="flex:1;padding:0 40px;display:flex;align-items:center;font:700 46px/1.25 'DM Sans'">{txt}</div></div>'''
    cores = ['var(--manga)', 'var(--piscina)', 'var(--chiclete)', 'var(--goiaba)', 'var(--uva)']
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--goiaba)"></div>
      <div class="abs" style="left:80px;top:90px">{icon('spiral-calendar-pad', 220)}</div>
      <div class="abs t" style="left:80px;top:380px;width:920px;font-size:150px;color:var(--noite)">O ano do grupo em 12 meses.</div>
      <div class="abs" style="left:80px;top:900px;width:860px;font-size:46px;font-weight:700;line-height:1.3;color:var(--noite)">Confere se o seu foi assim. Dezembro está na última página.</div>
      <div class="abs" style="left:80px;top:1200px"><span class="tag" style="background:var(--noite);border-color:var(--noite)">Arrasta →</span></div>''')]
    for p in range(0, 11, 3):
        fs = ''.join(folha(m, txt, cores[(p + k) % len(cores)]) for k, (m, txt) in enumerate(MESES[p:p + 3]))
        pages.append(page(f'<div class="abs" style="left:70px;top:{150 if p < 9 else 330}px;width:940px">{fs}</div>'))
    pages.append(page(f'''
      <div class="abs" style="left:70px;top:110px;width:940px">{folha('DEZ', 'O grupo ganha troféu.', 'var(--manga)')}</div>
      <div class="abs" style="left:80px;top:500px;width:900px;font-size:46px;line-height:1.3">O Retrozap lê a conversa do ano inteiro, no seu celular, e entrega a retrospectiva do grupo.</div>
      <div class="abs t" style="left:80px;top:800px;width:900px;font-size:76px">Manda no grupo e vê se foi <span class="hl">assim.</span></div>
      <div class="abs" style="left:80px;top:1110px">{assinatura(420)}</div>
      <div class="abs" style="right:80px;top:1155px;font-size:34px;font-weight:700">retrozap.com.br</div>'''))
    piece(id='R-C9', fmt='carrossel', day=6, slot='12h30', title='O ano do grupo em 12 meses (calendário)', kind='engajamento', w=1080, h=1350,
          html=doc('R-C9', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('O ano do grupo em 12 meses. 🗓️\n\n'
                   'Jan: metas do grupo. Fev: 214 fotos de carnaval. Mar: a guerra da foto do grupo. Jun: bolão da Copa, 1 pagou. Ago: ninguém lembrou do aniversário do grupo. Out: votação da data da confra.\n'
                   'Dez: o grupo ganha troféu.\n\n'
                   'Manda no grupo e vê se o de vocês foi assim 👇\n'
                   'retrozap.com.br\n#retrozap #retrospectiva2026 #grupodeamigos #amigos #fimdeano'),
          notes='Folhas de calendário com os 11 meses e dezembro como gancho para a retrospectiva. Copa do Mundo foi em jun–jul/2026 (bolão é verdadeiro como referência de época). Capa Goiaba, páginas Noite.')

# =====================================================================================
# R-R11 · Reel meme · "Manda pro amigo que some o ano todo e volta em dezembro" (dom, capa Uva)
# =====================================================================================
def r_r11():
    T = 16.0
    tl = TL(T)
    s0 = f'''<div {tl.scene(0, 3.8, fin=False)}>
      <div class="abs" style="inset:0;background:var(--uva)"></div>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:112px;color:var(--noite);{at(.05,'rise')}">Manda pro amigo que some o ano todo e volta em dezembro.</div>
      <div class="abs" style="left:700px;top:1060px;--r:8deg;{at(.8,'drop')}">{icon('ghost', 260)}</div>
    </div>'''
    meses = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV']
    cel = ''.join(f'''<div style="height:170px;border-radius:28px;background:var(--acai);border:3px solid var(--linha);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;{at(4.0 + i * .5,'pop',.3)}">
        <span class="mono" style="font-size:30px;color:var(--neblina)">{m}</span><span class="t" style="font-size:52px">0</span></div>''' for i, m in enumerate(meses))
    s1 = f'''<div {tl.scene(3.8, 10.4)}>
      <div class="abs mono" style="left:90px;top:300px;font-size:34px;color:var(--neblina)">MENSAGENS DO FANTASMA NO GRUPO · 2026</div>
      <div class="abs" style="left:90px;top:380px;width:900px;display:grid;grid-template-columns:repeat(4,1fr);gap:20px">{cel}</div>
      <div class="abs" style="left:90px;top:1180px;display:flex;align-items:center;gap:30px;{at(8.4,'rise')}">{icon('ghost', 150)}<span class="t" style="font-size:66px">visto por último:<br><span class="hl">em março</span></span></div>
    </div>'''
    s2 = f'''<div {tl.scene(10.4, 13.4)}>
      <div class="abs" style="left:90px;top:320px"><span class="lbl" style="background:var(--manga);color:var(--noite);font-size:44px">DEZ</span></div>
      <div class="abs" style="left:90px;top:460px;width:900px;background:#F3EDE2;color:#111;border-radius:40px;padding:40px 46px;box-shadow:0 20px 50px rgba(0,0,0,.4);{at(10.5,'pop')}">
        <div style="display:flex;align-items:center;gap:20px;margin-bottom:16px">{icon('ghost', 80)}<b style="font-size:34px;color:#C2185B">o fantasma</b></div>
        <div class="t" style="font-size:96px">GENTE!!! bora marcar a confra?</div></div>
      <div class="abs" style="left:300px;top:1040px;--r:-4deg;{at(11.6,'stamp')}"><div class="t" style="background:var(--chiclete);color:var(--areia);padding:18px 40px;font-size:80px;box-shadow:0 12px 0 #0B0414">Dezembro chegou.</div></div>
    </div>'''
    s3 = f'<div {tl.scene(13.4, T, fout=False)}>{fim(13.4, "Em dezembro, até o fantasma ganha troféu.")}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{s1}{s2}{s3}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:var(--uva);color:var(--noite)">
      <div class="abs t" style="left:80px;top:90px;width:920px;font-size:104px">Manda pro amigo que some o ano todo e volta em dezembro.</div>
      <div class="abs" style="left:80px;top:720px;width:640px;background:#F3EDE2;color:#111;border-radius:36px;padding:30px 36px;transform:rotate(-2deg)">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:10px">{icon('ghost', 60)}<b style="font-size:28px;color:#C2185B">o fantasma</b></div>
        <div class="t" style="font-size:64px">GENTE!!! bora marcar a confra?</div></div>
      <div class="abs" style="left:770px;top:820px;transform:rotate(8deg)">{icon('ghost', 230)}</div></div>'''
    piece(id='R-R11', fmt='reel', day=7, slot='19h45', title='Meme "manda pro amigo que…": o fantasma que volta em dezembro', total=T, poster=.7, kind='meme',
          html=doc('R-R11', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--uva)'),
          caption=('Manda pro amigo que some o ano todo e volta em dezembro. 👻\n\n'
                   'Jan a nov: 0 mensagens. Visto por último em março.\n'
                   'Dezembro: "GENTE!!! bora marcar a confra?"\n\n'
                   'Marca o fantasma do seu grupo 👇\n'
                   'retrozap.com.br\n#retrozap #grupodeamigos #meme #confraternizacao #amigos'),
          notes='Meme "manda pro amigo que…" (marcação). Contador de meses com ícone oficial do fantasma. Capa Uva fecha a semana, como na grade do S02 (alterna com a Noite do R-R10).')

# =====================================================================================
# Stories · Frase pro grupo (frases novas, 3 desenhos alternados, sem adesivo)
# =====================================================================================
FRASES_S03 = [
    (1, 'Todo grupo tem alguém que só aparece para mandar link de promoção.', 'receipt', 'nota'),
    (2, 'Amigo secreto: 12 pessoas, 1 sorteio e 3 semanas para decidir o valor.', 'party-popper', 'cor'),
    (3, 'Ninguém sabe quem criou o grupo. Todo mundo sabe quem silenciou.', 'sleuth-or-spy', 'balao'),
    (4, '"Tanto faz" é a resposta mais perigosa do casal.', 'serious-face-with-symbols-covering-mouth', 'casal'),
    (5, 'Black Friday: o grupo vira central de cupom por 24 horas.', 'label', 'nota'),
    (6, 'A foto da confra do ano passado ainda é a foto do grupo.', 'frame-with-picture', 'cor'),
    (7, 'Domingo à noite: o grupo volta à vida só para reclamar da segunda.', 'crescent-moon', 'balao'),
]

def r_stories():
    for n, (d, txt, ic, lay) in enumerate(FRASES_S03):
        fs = 120 if len(txt) < 50 else 106
        if lay == 'nota':  # papel de cupom/recibo
            corpo = f'''<div class="abs" style="left:110px;top:330px;width:860px;background:var(--areia);color:var(--noite);border-radius:12px;padding:60px 60px 70px;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(0,0,0,.4);
                -webkit-mask:radial-gradient(18px at 50% 100%,#0000 98%,#000) 0 0/52px 100% repeat-x">
              <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:4px dashed var(--noite);padding-bottom:30px;margin-bottom:40px">
                <span class="mono" style="font-size:30px">GRUPO · {C.DIAS[d].upper()}</span>{icon(ic, 120)}</div>
              <div class="t" style="font-size:{fs}px">{txt}</div></div>'''
            bg, cls = 'var(--noite)', ''
        elif lay == 'balao':  # mensagem única gigante, sem marca de app
            corpo = f'''<div class="abs" style="left:80px;top:330px">{icon(ic, 200)}</div>
              <div class="abs" style="left:80px;top:580px;width:920px;background:var(--areia);color:var(--noite);border-radius:50px 50px 50px 12px;padding:56px 56px 40px;box-shadow:0 20px 50px rgba(0,0,0,.35)">
                <div class="t" style="font-size:{fs}px">{txt}</div><div class="mono" style="text-align:right;font-size:28px;opacity:.5;margin-top:24px">21:07 ✓✓</div></div>'''
            bg, cls = 'var(--noite)', ''
        elif lay == 'casal':
            corpo = f'''<div class="abs" style="left:80px;top:330px">{icon(ic, 240, 'casal')}</div>
              <div class="abs" style="left:80px;top:640px;width:920px;background:#fff;border-radius:50px;padding:60px;box-shadow:0 24px 60px rgba(94,11,43,.18)"><div class="t" style="font-size:{fs + 10}px">{txt}</div></div>'''
            bg, cls = 'var(--creme)', 'casal'
        else:  # cor chapada com ícone
            corpo = f'''<div class="abs" style="left:80px;top:320px">{icon(ic, 260)}</div>
              <div class="abs t" style="left:80px;top:660px;width:920px;font-size:{fs + 8}px;color:var(--noite)">{txt}</div>'''
            bg, cls = 'var(--manga)', ''
        claro = bg == 'var(--manga)'
        cor_cta = 'var(--noite)' if claro else ('var(--cereja)' if cls else 'var(--manga)')
        casa = 'casal' if cls else 'grupo'
        body = f'''<section class="page {cls}" style="width:1080px;height:1920px;background:{bg}">{corpo}
          <div class="abs" style="left:80px;top:1350px;width:920px;font-size:44px;font-weight:700;color:{cor_cta}">{'Tira print e manda pro seu amor.' if cls else 'Tira print e manda no grupo.'}</div>
          <div class="abs" style="left:80px;top:1440px">{assinatura(300, casa, inv=claro)}</div>
        </section>'''
        sid = f'R-S{13 + n}'
        piece(id=sid, fmt='story', day=d, title=f'Frase pro grupo: {txt}', w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker='', kind='story',
              notes={'nota': 'Frase num papel de recibo (cupom). ', 'balao': 'Frase como mensagem única, sem marca de app. ', 'casal': 'Casa Casal, sem roxo. ', 'cor': 'Cor chapada com ícone oficial. '}[lay] + 'Sem adesivo, sem preço, sem etiqueta. Motivo de envio: print no grupo.')

def build():
    r_r8(); r_c7(); r_r9(); r_c8(); r_r10(); r_c9(); r_r11(); r_stories()

build()
