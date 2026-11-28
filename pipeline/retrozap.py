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


SIM = '<span class="sim">simulação · nomes de exemplo</span>'
EXEMPLO = '<span class="sim">dados de exemplo · Turma do Churras</span>'

def fim(t, frase='e o seu grupo?', top=470):
    """Encerramento dos reels (sem preço na arte)."""
    return f'''<div class="abs" style="left:0;right:0;top:{top}px;display:flex;justify-content:center;{at(t + .1,'pop')}">{assinatura(700)}</div>
      <div class="abs t" style="left:90px;right:90px;top:{top + 290}px;text-align:center;font-size:88px;{at(t + .4,'rise')}">{frase}</div>
      <div class="foot" style="top:{top + 640}px;font-size:42px;{at(t + .9,'fade')}">retrozap.com.br</div>'''

def chat_head(sub='Lu, Caio, Pedrão, Bia, Rafa, você'):
    return f'''<div style="height:110px;background:var(--noite);color:var(--areia);display:flex;align-items:center;gap:18px;padding:0 26px">
      <div style="width:70px;height:70px;border-radius:50%;background:var(--manga);display:flex;align-items:center;justify-content:center">{icon('hamburger', 50)}</div>
      <div><div style="font:800 34px/1.1 'Bricolage Grotesque'">Turma do Churras</div><div style="font-size:22px;color:var(--neblina)">{sub}</div></div></div>'''

# =====================================================================================
# S05 · 08–14/12/2026 · Retrospectiva 2026 no centro, sem preço em nenhuma peça (Gui, rodada 18)
# =====================================================================================
END_RG = C.PACKS / 'S04' / 'retrozap' / 'carrosseis' / 'R-C10-6.png'   # card final aprovado (grupo)
END_RC = C.PACKS / 'S04' / 'retrozap' / 'carrosseis' / 'R-C12-5.png'   # card final aprovado (casal)

def SC(tl, a, z):
    return tl.scene(max(0, a - .04), z, fin=False, fout=False)

CSS += """
.bingo{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.bingo .c{background:var(--areia);color:var(--noite);border-radius:22px;height:208px;padding:16px 14px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;text-align:center;font-weight:700;font-size:25px;line-height:1.15}
.bingo .c.x{background:var(--manga)}
.ticket{background:var(--areia);color:var(--noite);border-radius:26px;position:relative;box-shadow:0 30px 60px rgba(0,0,0,.35)}
.ticket::after{content:'';position:absolute;left:0;right:0;bottom:-18px;height:36px;background:radial-gradient(circle at 18px 0,transparent 17px,var(--areia) 18px) repeat-x;background-size:36px 36px}
.flux{background:var(--acai);border:3px solid var(--linha);border-radius:26px;padding:22px 28px;font-weight:700;font-size:36px;line-height:1.2;text-align:center}
.flux.q{background:var(--manga);color:var(--noite);border-color:var(--manga)}
.seta{position:absolute;width:6px;background:var(--neblina);opacity:.7}
"""

# -------------------------------------------------------------------------------------
# R-C13 · Carrossel (ter 08/12) · Bingo do grupo em dezembro
# -------------------------------------------------------------------------------------
BINGO = [('camera-with-flash', 'Foto da árvore montada'), ('spiral-calendar-pad', '"Quem leva o quê?"'), ('sparkles', 'Figurinha de Papai Noel'), ('black-sun-with-rays', 'Bom dia com flor e glitter'),
         ('ghost', 'Sumido aparece no dia 24'), ('scroll', '"Feliz Natal" copiado de outro grupo'), ('hamburger', 'Foto do prato da ceia'), ('clipboard', 'Lista do amigo secreto'),
         ('wastebasket', 'Alguém sai do grupo (e volta)'), ('frame-with-picture', 'Foto de família de 2009'), ('clinking-beer-mugs', '"Vai ter churrasco dia 25?"'), ('incoming-envelope', 'Corrente de fim de ano'),
         ('speaker-with-three-sound-waves', 'Áudio cantando parabéns atrasado'), ('house-with-garden', '"A ceia é lá em casa"'), ('eyes', 'Visualizou e não respondeu'), ('party-popper', 'Contagem regressiva às 23h59')]

def r_c13():
    def cartela(marcadas=()):
        return '<div class="bingo">' + ''.join(f'<div class="c{" x" if k in marcadas else ""}">{icon(ic, 84)}<span>{t}</span></div>' for k, (ic, t) in enumerate(BINGO)) + '</div>'
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--manga)"></div>
      <div class="abs mono" style="left:80px;top:70px;font-size:28px;letter-spacing:.08em;color:var(--noite)">DEZEMBRO · 4 × 4</div>
      <div class="abs t" style="left:80px;top:130px;width:920px;font-size:128px;color:var(--noite)">Bingo do grupo em dezembro.</div>
      <div class="abs" style="left:110px;top:560px;width:860px;transform:rotate(-3deg);background:var(--noite);border-radius:34px;padding:22px;box-shadow:0 30px 60px rgba(26,11,46,.35);height:720px;overflow:hidden">
        <div style="transform:scale(.88);transform-origin:top left;width:927px">{cartela((0, 5, 10))}</div></div>''', cls='')]
    pages.append(page(f'''
      <div class="abs mono" style="left:80px;top:60px;font-size:26px;letter-spacing:.08em;color:var(--neblina)">A CARTELA · TIRA PRINT</div>
      <div class="abs" style="left:60px;top:120px;width:960px">{cartela()}</div>
      <div class="abs" style="left:80px;top:1060px;width:920px;font-size:40px;font-weight:700;line-height:1.3">Marca o que já aconteceu no seu grupo.<br><span class="hl">Fechou uma linha? Manda no grupo.</span></div>'''))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--areia)"></div>
      <div class="abs t" style="left:80px;top:90px;width:920px;font-size:96px;color:var(--noite)">E quem preencheu mais casas?</div>
      <div class="abs" style="left:80px;top:420px;width:920px;font-size:44px;font-weight:700;line-height:1.35;color:var(--noite)">Em janeiro, a retrospectiva do grupo conta quem mais falou, quem sumiu e quem só mandou áudio.</div>
      <div class="abs" style="left:80px;top:760px;display:flex;gap:30px">{icon('medalha-1', 170)}{icon('medalha-2', 170)}{icon('medalha-3', 170)}</div>
      <div class="abs" style="left:80px;top:1130px">{assinatura(330, inv=True)}</div>''', cls=''))
    pages.append(C.endcard(END_RG))
    piece(id='R-C13', fmt='carrossel', day=1, slot='12h30', title='Bingo do grupo em dezembro (cartela 4 × 4)', kind='engajamento', w=1080, h=1350,
          html=doc('R-C13', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Bingo do grupo em dezembro. 🎄\n'
                   'Foto da árvore, "quem leva o quê?", o sumido que aparece no dia 24… Tira print da cartela e marca o que já aconteceu.\n\n'
                   'Fechou uma linha? Manda no grupo e marca quem completou 👇\n'
                   'A retrospectiva do grupo: retrozap.com.br\n#retrozap #grupodewhatsapp #natal #bingo #amigos #familia'),
          notes='Formato novo (bingo de comportamento do grupo). Casas sem repetir piadas das últimas 4 semanas (link de promoção, áudio "tô chegando" e foto da confra ficaram de fora). Só ícones oficiais. Sem preço. Card final = CTA aprovado do S04 (R-C10-6). Motivo de envio: print da cartela no grupo.')

# -------------------------------------------------------------------------------------
# R-R19 · Reel MEME (qua 09/12) · As 4 reações quando a retrospectiva cai no grupo
# -------------------------------------------------------------------------------------
MSGS_R19 = [('RECONTAGEM. Eu não mandei 2 mil mensagens.', 'Lu', '21:02', False, 3.0, 'a que pede recontagem', 'right-pointing-magnifying-glass'),
            ('não vi nada. não tô aqui.', 'Caio', '21:03', False, 5.6, 'o que finge que não viu', 'eyes'),
            ('já mandei imprimir o meu troféu', 'Pedrão', '21:03', False, 8.2, 'o que já emoldurou', 'frame-with-picture'),
            ('mandando no grupo da família também', 'Bia', '21:04', False, 10.8, 'o que espalha', 'mobile-phone-with-rightwards-arrow-at-left')]

def r_r19():
    T = 16.0; tl = TL(T)
    s0 = f'''<div {SC(tl, 0, 2.8)}>
      <div class="abs" style="inset:0;background:var(--noite)"></div>
      <div class="abs t" style="left:90px;top:520px;width:900px;font-size:112px;{at(.05,'rise')}">Quando a retrospectiva cai no grupo:</div>
      <div class="abs" style="left:90px;top:1000px;{at(.6,'pop')}">{icon('party-popper', 200)}</div>
    </div>'''
    bl = ''
    for txt, n, h, me, t, lab, ic in MSGS_R19:
        bl += f'<div style="{at(t,"rise",.3)}">{C.bubble(txt, me=me, nome=n, hora=h, bg_me="#FFE3A3", fs=34)}</div>'
    tela = f'<div style="position:absolute;inset:0;background:#F3EDE2">{chat_head()}<div style="padding-top:18px"><div style="{at(2.9,"rise",.3)}">{C.bubble("🏆 Retrospectiva 2026 da Turma do Churras", me=True, hora="21:01", bg_me="#FFE3A3", fs=34)}</div>{bl}</div></div>'
    labels = ''
    for k, (txt, n, h, me, t, lab, ic) in enumerate(MSGS_R19):
        z = MSGS_R19[k + 1][4] if k < 3 else 13.3
        labels += (f'<div class="abs" style="left:110px;top:1260px;opacity:0;animation:fade .2s linear {t + .4:.2f}s 1 both,fadeOut .2s linear {z:.2f}s 1 forwards;display:flex;align-items:center;gap:20px">'
                   f'<div style="width:120px;height:120px;border-radius:30px;background:var(--areia);display:flex;align-items:center;justify-content:center">{icon(ic, 96)}</div>'
                   f'<span class="lbl" style="background:var(--manga);color:var(--noite);font-size:44px;font-weight:500">{lab}</span></div>')
    s1 = f'''<div {SC(tl, 2.8, 13.3)}>
      <div class="abs" style="inset:0;background:var(--acai2)"></div>
      <div class="abs" style="left:150px;top:260px">{C.phone(tela, 780, 980, screen='#F3EDE2', frame='#0B0414', status_color='#1A0B2E', hora='21:04')}</div>
      {labels}
      <div class="abs" style="left:0;right:0;top:1480px;text-align:center;color:var(--neblina)">{SIM}</div>
    </div>'''
    s2 = f'<div {SC(tl, 13.3, T)}><div class="abs" style="inset:0;background:var(--noite)"></div>{fim(13.3, "Qual é você?")}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{s1}{s2}</section>'
    grid = ''.join(f'<div style="background:var(--acai);border:3px solid var(--linha);border-radius:30px;padding:26px;display:flex;flex-direction:column;gap:18px;height:330px">'
                   f'<div style="width:120px;height:120px;border-radius:28px;background:var(--areia);display:flex;align-items:center;justify-content:center">{icon(ic, 96)}</div>'
                   f'<div class="t" style="font-size:48px">{lab}</div></div>' for _, _, _, _, _, lab, ic in MSGS_R19)
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:var(--noite)">
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:92px">Quando a retrospectiva cai no grupo:</div>
      <div class="abs" style="left:80px;top:420px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:26px">{grid}</div></div>'''
    piece(id='R-R19', fmt='reel', day=2, slot='19h45', title='Meme: as 4 reações quando a retrospectiva cai no grupo', total=T, poster=.6, kind='meme',
          music='S03/retrozap/reels/R-R17.mp4',
          html=doc('R-R19', FONTS, CSS + C.REC_CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, 'var(--noite)'),
          caption=('Quando a retrospectiva cai no grupo: 🏆\n'
                   'Uma pede recontagem, um finge que não viu, um já emoldurou o troféu e uma manda até no grupo da família.\n\n'
                   'Qual é você? Marca o resto do grupo 👇\n'
                   'A retrospectiva do seu grupo: retrozap.com.br\n#retrozap #grupodewhatsapp #retrospectiva2026 #amigos #meme'),
          notes='Meme de reações (comportamento de grupo), conversa em celular genérico com etiqueta "simulação · nomes de exemplo" (Turma do Churras). Ideia nova: R-R11 era o fantasma; aqui é a reação ao resultado. Música de banco do R-R17 aprovado, com fade de saída. Sem preço.')

# -------------------------------------------------------------------------------------
# R-C14 · Carrossel (qui 10/12) · A cerimônia de premiação do grupo, em 5 passos (confra)
# -------------------------------------------------------------------------------------
PASSOS = [('studio-microphone', 'Escolha o apresentador.', 'Quem fala mais no grupo, claro.'),
          ('lock', 'Guarde os troféus até a confra.', 'Ninguém vê antes. Suspense é tudo.'),
          ('scroll', 'Leia um prêmio por vez.', 'Primeiro a categoria, depois o nome. Pausa dramática.'),
          ('speaking-head-in-silhouette', 'O premiado faz discurso.', '15 segundos. Vale agradecer à família.'),
          ('camera-with-flash', 'Foto oficial com o troféu na tela.', 'E manda no grupo antes de a festa acabar.')]

def r_c14():
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--uva)"></div>
      <div class="abs" style="left:80px;top:80px">{taca(120, inv=True)}</div>
      <div class="abs t" style="left:80px;top:250px;width:920px;font-size:112px;color:var(--noite)">A cerimônia de premiação do grupo.</div>
      <div class="abs" style="left:80px;top:700px;font-size:46px;font-weight:700;color:var(--noite)">Roteiro em 5 passos pra confra.</div>
      <div class="abs" style="left:640px;top:850px;transform:rotate(8deg)">{icon('medalha-1', 300)}</div>
      <div class="abs mono" style="left:80px;top:1180px;font-size:28px;letter-spacing:.08em;color:var(--noite)">MANDA PRO ORGANIZADOR DA CONFRA</div>''')]
    for i, (ic, t, sub) in enumerate(PASSOS):
        pages.append(page(f'''
          <div class="abs mono" style="left:80px;top:70px;font-size:28px;letter-spacing:.08em;color:var(--neblina)">PASSO {i + 1} DE 5</div>
          <div class="abs n" style="left:60px;top:120px;font-family:'Bricolage Grotesque';font-weight:800;font-size:420px;line-height:1;color:var(--acai)">{i + 1}</div>
          <div class="abs" style="right:90px;top:180px;width:300px;height:300px;border-radius:70px;background:var(--areia);display:flex;align-items:center;justify-content:center;transform:rotate({(-1) ** i * 5}deg)">{icon(ic, 220)}</div>
          <div class="abs t" style="left:80px;top:640px;width:920px;font-size:100px">{t}</div>
          <div class="abs" style="left:80px;top:{900 if len(t) < 26 else 1000}px;width:920px;font-size:46px;font-weight:700;color:var(--manga)">{sub}</div>'''))
    pages.append(C.endcard(END_RG))
    piece(id='R-C14', fmt='carrossel', day=3, slot='12h30', title='A cerimônia de premiação do grupo, em 5 passos (confra)', kind='utilidade', w=1080, h=1350,
          html=doc('R-C14', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('A cerimônia de premiação do grupo, em 5 passos. 🎤\n'
                   'Apresentador, troféus guardados até a confra, um prêmio por vez, discurso de 15 segundos e foto oficial.\n\n'
                   'Manda pro organizador da confra 👇\n'
                   'Os troféus saem da retrospectiva do grupo: retrozap.com.br\n#retrozap #confraternizacao #amigos #retrospectiva2026 #grupodewhatsapp'),
          notes='Utilidade para a confra (usar a retrospectiva como cerimônia). Capa Uva para não repetir o Areia do R-R21 nem o Manga do R-C13/R-R20 na grade. Só ícones oficiais. Sem preço. Card final = CTA aprovado do S04 (R-C10-6). Motivo de envio: mandar pro organizador.')

# -------------------------------------------------------------------------------------
# R-R20 · Reel TREND antes × depois (sex 11/12) · O grupo silencioso × o grupo depois da retrospectiva
# -------------------------------------------------------------------------------------
def r_r20():
    T = 15.0; tl = TL(T)
    s1 = f'''<div {SC(tl, 0, 6.0)}>
      <div class="abs" style="inset:0;background:#2A2433"></div>
      <div class="abs" style="left:90px;top:300px;{at(.05,'fade')}"><span class="lbl" style="background:var(--linha);color:var(--neblina);font-size:40px">ANTES</span></div>
      <div class="abs" style="left:90px;top:420px;width:900px;background:var(--acai2);border-radius:36px;padding:34px 36px;{at(.2,'rise')}">
        <div style="font-size:30px;color:var(--neblina)">Turma do Churras · visto por último há 3 dias</div>
        <div style="margin-top:24px;display:inline-block;background:#3B3346;border-radius:24px;padding:20px 28px;font-size:44px">bom dia ☀️ <span style="font-size:26px;opacity:.6">08:12</span></div>
        <div style="margin-top:30px;font-size:34px;color:var(--neblina)">0 respostas</div></div>
      <div class="abs t" style="left:90px;top:900px;width:900px;font-size:100px;color:var(--neblina);{at(1.2,'rise')}">Grupo em silêncio desde segunda.</div>
      <div class="abs" style="left:90px;top:1280px;opacity:.45;{at(2.0,'fade')}">{icon('turtle', 180)}</div>
    </div>'''
    s2 = f'''<div {SC(tl, 6.0, 12.0)}>
      <div class="abs" style="inset:0;background:var(--manga);color:var(--noite)"></div>
      <div class="abs" style="left:90px;top:300px;{at(6.05,'stamp')}"><span class="lbl" style="background:var(--noite);color:var(--manga);font-size:40px">DEPOIS DA RETROSPECTIVA</span></div>
      <div class="abs" style="left:90px;top:440px;width:900px;background:var(--noite);color:var(--areia);border-radius:36px;padding:34px 36px;{at(6.3,'pop')}">
        <div style="display:flex;align-items:center;justify-content:space-between"><span style="font-size:32px;color:var(--neblina)">Turma do Churras</span>
          <span style="background:var(--chiclete);color:#fff;border-radius:40px;padding:8px 26px;font:800 44px/1 'Bricolage Grotesque'"><span class="cnt" style="--n:47;animation:cntup 2.4s cubic-bezier(.2,.8,.2,1) 6.8s 1 both"></span></span></div>
        <div style="margin-top:20px;font-size:40px">Lu: RECONTAGEM</div><div style="font-size:40px">Pedrão: quem me deu "Some e Volta"???</div><div style="font-size:40px">Rafa: apareci 👋</div></div>
      <div class="abs t" style="left:90px;top:1000px;width:900px;font-size:104px;color:var(--noite);{at(8.2,'rise')}">47 mensagens em 10 minutos.</div>
      <div class="abs" style="left:90px;top:1420px;color:var(--noite)">{SIM}</div>
    </div>'''
    s3 = f'<div {SC(tl, 12.0, T)}><div class="abs" style="inset:0;background:var(--noite)"></div>{fim(12.0, "Acorda o seu grupo.")}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:var(--manga);color:var(--noite)">
      <div class="abs" style="left:0;top:0;width:1080px;height:560px;background:#2A2433"></div>
      <div class="abs" style="left:80px;top:70px"><span class="lbl" style="background:var(--linha);color:var(--neblina);font-size:34px">ANTES</span></div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:88px;color:var(--neblina)">"bom dia" · 0 respostas</div>
      <div class="abs" style="left:80px;top:360px;opacity:.5">{icon('turtle', 150)}</div>
      <div class="abs" style="left:80px;top:630px"><span class="lbl" style="background:var(--noite);color:var(--manga);font-size:34px">DEPOIS DA RETROSPECTIVA</span></div>
      <div class="abs t" style="left:80px;top:740px;width:920px;font-size:120px">47 mensagens em 10 minutos.</div>
      <div class="abs" style="left:800px;top:1050px">{icon('fire', 180)}</div></div>'''
    piece(id='R-R20', fmt='reel', day=4, slot='19h45', title='Trend antes × depois: o grupo em silêncio × depois da retrospectiva', total=T, poster=.62, kind='trend',
          music='S04/retrozap/reels/R-R13.mp4',
          html=doc('R-R20', FONTS, CSS + C.REC_CSS + tl.style() + '@keyframes cntup{from{--n:0}to{--n:47}}', body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, 'var(--manga)'),
          caption=('Antes: "bom dia" com 0 respostas há 3 dias. 🐢\n'
                   'Depois da retrospectiva: 47 mensagens em 10 minutos e até o Rafa apareceu.\n\n'
                   'Manda no grupo que tá em silêncio 👇\n'
                   'A retrospectiva do seu grupo: retrozap.com.br\n#retrozap #grupodewhatsapp #antesedepois #retrospectiva2026 #amigos'),
          notes='Trend "antes × depois" (doc de trends do DOT, 06/11: "grupo silencioso versus premiação"; circulação no Brasil sem validação). Conversa simulada com etiqueta "simulação · nomes de exemplo". Música de banco do R-R13 aprovado (S04), fade de saída. Sem preço.')

# -------------------------------------------------------------------------------------
# R-C15 · Carrossel (sáb 12/12) · Bolão 2027 do grupo: 6 apostas pra conferir no fim do ano que vem
# -------------------------------------------------------------------------------------
BOLAO = [('speech-balloon', 'Quem vai mandar mais mensagem em 2027?'), ('spiral-calendar-pad', 'Quem vai ser o primeiro a dizer "vamos marcar"?'),
         ('studio-microphone', 'Quem vai mandar mais áudio?'), ('frame-with-picture', 'Quem vai trocar a foto do grupo?'),
         ('rocket', 'Quem vai sumir em março?'), ('heart-hands', 'Quem vai pedir pra fazer a retrospectiva primeiro?')]

def r_c15():
    pages = [page(f'''
      <div class="abs" style="inset:0;background:var(--piscina)"></div>
      <div class="abs mono" style="left:80px;top:70px;font-size:28px;letter-spacing:.08em;color:var(--noite)">BOLÃO 2027 · 6 APOSTAS</div>
      <div class="abs t" style="left:80px;top:140px;width:920px;font-size:120px;color:var(--noite)">Aposta agora. Confere em dezembro de 2027.</div>
      <div class="abs ticket" style="left:120px;top:720px;width:840px;padding:40px 46px;transform:rotate(-2.5deg)">
        <div class="mono" style="font-size:26px;letter-spacing:.08em;opacity:.6">APOSTA 1 · TURMA DO CHURRAS</div>
        <div class="t" style="font-size:64px;margin-top:14px">Quem vai mandar mais mensagem em 2027?</div>
        <div style="margin-top:24px;border-top:4px dashed var(--neblina);padding-top:18px;font-size:34px;font-weight:700">Meu palpite: ____________</div></div>''')]
    for i, (ic, q) in enumerate(BOLAO):
        pages.append(page(f'''
          <div class="abs mono" style="left:80px;top:70px;font-size:28px;letter-spacing:.08em;color:var(--neblina)">APOSTA {i + 1} DE 6</div>
          <div class="abs ticket" style="left:80px;top:170px;width:920px;padding:50px 56px 60px;transform:rotate({(-1) ** i * 1.5}deg)">
            <div style="display:flex;justify-content:space-between;align-items:center"><span class="mono" style="font-size:26px;letter-spacing:.08em;opacity:.6">BOLÃO 2027</span>{icon(ic, 120)}</div>
            <div class="t" style="font-size:88px;margin-top:30px">{q}</div>
            <div style="margin-top:60px;border-top:4px dashed var(--neblina);padding-top:26px;font-size:40px;font-weight:700">Meu palpite: ____________</div>
            <div style="margin-top:18px;font-size:40px;font-weight:700">Palpite do grupo: ____________</div></div>
          <div class="abs" style="left:80px;top:1170px;font-size:40px;font-weight:700;color:var(--manga)">Tira print e responde no grupo.</div>'''))
    pages.append(C.endcard(END_RG))
    piece(id='R-C15', fmt='carrossel', day=5, slot='12h30', title='Bolão 2027 do grupo: 6 apostas pra conferir no fim do ano que vem', kind='engajamento', w=1080, h=1350,
          html=doc('R-C15', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Bolão 2027 do grupo. 🎟️\n'
                   'Quem vai mandar mais mensagem? Quem vai sumir em março? Quem vai ser o primeiro a dizer "vamos marcar"?\n\n'
                   'Tira print, manda no grupo e cada um responde. Em dezembro de 2027, a conversa confere 👇\n'
                   'A retrospectiva do seu grupo: retrozap.com.br\n#retrozap #grupodewhatsapp #2027 #amigos #bolao'),
          notes='Formato novo (bolão de previsões com bilhete para preencher). Piscina na capa para variar a grade. Sem preço. Card final = CTA aprovado do S04 (R-C10-6). Motivo de envio: cada um responde no grupo.')

# -------------------------------------------------------------------------------------
# R-R21 · Reel MEME (dom 13/12) · "Eu quase não falo no grupo" × a retrospectiva
# -------------------------------------------------------------------------------------
def r_r21():
    T = 14.0; tl = TL(T)
    s1 = f'''<div {SC(tl, 0, 4.6)}>
      <div class="abs" style="inset:0;background:var(--areia);color:var(--noite)"></div>
      <div class="abs t" style="left:90px;top:330px;font-size:84px;color:var(--acai);{at(.05,'fade')}">Eu, todo ano:</div>
      <div class="abs t" style="left:90px;top:520px;width:900px;font-size:132px;color:var(--noite);{at(.3,'rise')}">"Eu quase não falo no grupo."</div>
      <div class="abs" style="left:90px;top:1100px;{at(1.4,'pop')}">{icon('face-with-no-good-gesture', 260)}</div>
    </div>'''
    s2 = f'''<div {SC(tl, 4.6, 10.6)}>
      <div class="abs" style="inset:0;background:var(--noite)"></div>
      <div class="abs t" style="left:90px;top:300px;font-size:84px;color:var(--manga);{at(4.65,'fade')}">A retrospectiva:</div>
      <div class="abs ticket" style="left:110px;top:470px;width:860px;padding:44px 50px 60px;transform:rotate(-2deg);{at(5.1,'pop')}">
        <div style="display:flex;align-items:center;gap:18px">{taca(56)}<span class="mono" style="font-size:24px;letter-spacing:.08em;opacity:.6">TURMA DO CHURRAS · 2026</span></div>
        <div class="mono" style="margin-top:30px;font-size:30px;letter-spacing:.06em">1º LUGAR · TAGARELA DO ANO</div>
        <div class="t" style="font-size:190px;margin-top:10px;{at(5.7,'pop')}">2.318</div>
        <div style="font-size:44px;font-weight:700">mensagens. Você.</div></div>
      <div class="abs" style="left:640px;top:1180px;--r:-6deg;{at(8.2,'stamp')}">{icon('face-with-tears-of-joy', 230)}</div>
      <div class="abs" style="left:110px;top:1440px;color:var(--neblina)">{EXEMPLO}</div>
    </div>'''
    s3 = f'<div {SC(tl, 10.6, T)}><div class="abs" style="inset:0;background:var(--noite)"></div>{fim(10.6, "Marca quem jura que é quieto.")}</div>'
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    cover = f'''<div class="page" style="width:1080px;height:1350px;background:var(--areia);color:var(--noite)">
      <div class="abs t" style="left:80px;top:80px;width:920px;font-size:104px">"Eu quase não falo no grupo."</div>
      <div class="abs ticket" style="left:120px;top:560px;width:840px;padding:40px 46px 54px;transform:rotate(-2deg);background:var(--noite);color:var(--areia)">
        <div class="mono" style="font-size:26px;letter-spacing:.06em;color:var(--manga)">A RETROSPECTIVA · TAGARELA DO ANO</div>
        <div class="t" style="font-size:180px;margin-top:10px;color:var(--manga)">2.318</div><div style="font-size:42px;font-weight:700">mensagens. Você.</div></div>'''
    cover = cover.replace('class="abs ticket"', 'class="abs"') + '</div>'
    piece(id='R-R21', fmt='reel', day=6, slot='19h45', title='Meme: "eu quase não falo no grupo" × a retrospectiva', total=T, poster=.55, kind='meme',
          music='S04/retrozap/reels/R-R12.mp4',
          html=doc('R-R21', FONTS, CSS + tl.style() + '@keyframes cntup{from{--n:0}to{--n:2318}}', body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover, 'var(--areia)'),
          caption=('Eu, todo ano: "eu quase não falo no grupo." 🤐\n'
                   'A retrospectiva: 2.318 mensagens. Tagarela do ano.\n\n'
                   'Marca quem jura que é quieto (e manda no grupo pra ele ver) 👇\n'
                   'A retrospectiva do seu grupo: retrozap.com.br\n#retrozap #grupodewhatsapp #meme #retrospectiva2026 #amigos'),
          notes='Meme "eu × a realidade". Número de exemplo com etiqueta "dados de exemplo · Turma do Churras". Fundo areia → noite. Música de banco do R-R12 aprovado (S04), fade de saída. Sem preço.')

# -------------------------------------------------------------------------------------
# R-C16 · Carrossel (seg 14/12) · Qual grupo fazer primeiro? (fluxograma)
# -------------------------------------------------------------------------------------
def r_c16():
    def caixa(x, y, w, txt, q=False, extra=''):
        return f'<div class="abs flux{" q" if q else ""}" style="left:{x}px;top:{y}px;width:{w}px;{extra}">{txt}</div>'
    def seta(x, y, h, lbl=''):
        return (f'<div class="seta" style="left:{x}px;top:{y}px;height:{h}px"></div>'
                + (f'<div class="abs mono" style="left:{x + 16}px;top:{y + h / 2 - 18}px;font-size:26px;color:var(--neblina)">{lbl}</div>' if lbl else ''))
    pages = [page(f'''
      <div class="abs mono" style="left:80px;top:70px;font-size:28px;letter-spacing:.08em;color:var(--neblina)">FLUXOGRAMA · 30 SEGUNDOS</div>
      <div class="abs t" style="left:80px;top:140px;width:920px;font-size:118px">Qual grupo fazer primeiro?</div>
      <div class="abs" style="left:80px;top:470px;font-size:44px;font-weight:700;color:var(--manga)">Família, amigos, firma ou casal. Arrasta →</div>
      <div class="abs" style="left:80px;top:700px;display:flex;gap:30px">{icon('house-with-garden', 180)}{icon('clinking-beer-mugs', 180)}{icon('briefcase', 180)}{icon('two-hearts', 180)}</div>''')]
    pages.append(page(f'''
      <div class="abs mono" style="left:80px;top:60px;font-size:26px;letter-spacing:.08em;color:var(--neblina)">COMECE AQUI</div>
      {caixa(190, 120, 700, 'O grupo teve mais de 1.000 mensagens este ano?', True)}
      {seta(300, 260, 120, 'sim')}{seta(780, 260, 120, 'não')}
      {caixa(80, 390, 480, 'Tem alguém que some e volta no Natal?', True)}
      {caixa(620, 390, 380, 'É só você e o seu amor?', True)}
      {seta(200, 560, 130, 'sim')}{seta(450, 560, 130, 'não')}{seta(720, 520, 170, 'sim')}{seta(930, 520, 170, 'não')}
      {caixa(60, 700, 300, icon('house-with-garden', 110) + '<br>Grupo da família')}
      {caixa(380, 700, 260, icon('clinking-beer-mugs', 110) + '<br>Grupo dos amigos')}
      {caixa(660, 700, 190, icon('two-hearts', 90) + '<br>Casal', extra='font-size:32px')}
      {caixa(870, 700, 170, icon('briefcase', 90) + '<br>Firma', extra='font-size:32px;padding:22px 10px')}
      <div class="abs" style="left:80px;top:1080px;width:920px;font-size:40px;font-weight:700">Deu família? Prepare-se pro troféu "Bom Dia com Flor".</div>'''))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--manga)"></div>
      <div class="abs t" style="left:80px;top:100px;width:920px;font-size:110px;color:var(--noite)">O primeiro grupo é grátis.</div>
      <div class="abs t" style="left:80px;top:400px;width:920px;font-size:110px;color:var(--noite)">Escolhe bem.</div>
      <div class="abs" style="left:80px;top:720px;width:900px;font-size:44px;font-weight:700;line-height:1.35;color:var(--noite)">Manda o fluxograma no grupo que você escolheu. Eles vão querer saber por quê.</div>
      <div class="abs" style="left:80px;top:1100px">{assinatura(360, inv=True)}</div>'''))
    pages.append(C.endcard(END_RG))
    piece(id='R-C16', fmt='carrossel', day=7, slot='12h30', title='Fluxograma: qual grupo fazer primeiro?', kind='utilidade', w=1080, h=1350,
          html=doc('R-C16', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Qual grupo fazer primeiro: família, amigos, firma ou casal? 🧭\n'
                   'Segue o fluxograma e descobre em 30 segundos.\n\n'
                   'Manda no grupo que você escolheu (eles vão querer saber por quê) 👇\n'
                   'O primeiro grupo é grátis: retrozap.com.br\n#retrozap #grupodewhatsapp #retrospectiva2026 #amigos #familia'),
          notes='Formato novo (fluxograma). Fala do 1º grupo grátis (oferta do site), sem preço. Só ícones oficiais. Card final = CTA aprovado do S04 (R-C10-6). Motivo de envio: mandar no grupo escolhido.')

# -------------------------------------------------------------------------------------
# Stories (1 sequência de 3 por dia, 12h, sem adesivo): Frase pro grupo
# -------------------------------------------------------------------------------------
FRASES5 = [
    (1, 'grupo', 'O grupo da família em dezembro: foto da árvore, foto da ceia, foto do prato.', 'camera-with-flash', 'Quem manda a primeira foto no seu?'),
    (2, 'grupo', 'Todo amigo secreto tem quem compra o presente no caminho da festa.', 'party-popper', 'Marca quem é no seu grupo.'),
    (3, 'casal', '"Chegou?" é o "te amo" de quem não gosta de falar "te amo".', 'heart-with-arrow', 'Manda pro seu amor.'),
    (4, 'grupo', 'Grupo do trabalho de 20/12 a 5/1: o silêncio mais bonito do ano.', 'briefcase', 'Quem vai quebrar o silêncio no seu?'),
    (5, 'grupo', 'Todo grupo tem quem manda "feliz Natal" copiado de outro grupo.', 'scroll', 'Marca o copia e cola.'),
    (6, 'casal', 'Casal: cada um jura que é o outro que esquece de responder.', 'love-letter', 'A conversa de vocês tem o placar.'),
    (7, 'grupo', 'Grupo dos amigos em dezembro: 14 "saudade" e nenhum encontro marcado.', 'spiral-calendar-pad', 'Manda no grupo e marca a data.'),
]

def r_stories():
    for n, (d, casa, frase, ic, prompt) in enumerate(FRASES5):
        sid = f'R-S{30 + n}'
        cs = casa == 'casal'
        bg = 'var(--creme)' if cs else 'var(--noite)'
        fg = 'var(--vinho)' if cs else 'var(--areia)'
        acc = 'var(--cereja)' if cs else 'var(--manga)'
        tk_bg = '#fff' if cs else 'var(--areia)'
        f1 = f'''<section class="page {'casal' if cs else ''}" style="width:1080px;height:1920px;background:{bg}">
          <div class="abs" style="left:90px;top:320px;width:880px;background:{tk_bg};color:{'var(--vinho)' if cs else 'var(--noite)'};border-radius:26px;padding:46px 50px 70px;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(0,0,0,.3)">
            <div style="display:flex;justify-content:space-between;align-items:center"><span class="mono" style="font-size:26px;letter-spacing:.06em">{'CASAL' if cs else 'GRUPO'} · {C.DIAS[d].upper()}</span>
              <div style="width:110px;height:110px;border-radius:28px;background:{acc};display:flex;align-items:center;justify-content:center">{icon(ic, 84, casa)}</div></div>
            <div style="border-top:4px dashed {'var(--clinha)' if cs else 'var(--neblina)'};margin:28px 0"></div>
            <div class="t" style="font-size:{84 if len(frase) < 60 else 74}px;line-height:1.02">{frase}</div></div>
          <div class="abs" style="left:90px;top:1380px;font-size:46px;font-weight:700;color:{acc}">Tira print e manda {'pro seu amor' if cs else 'no grupo'}.</div>
          <div class="abs" style="left:90px;top:1480px">{assinatura(260, casa)}</div></section>'''
        f2 = f'''<section class="page {'casal' if cs else ''}" style="width:1080px;height:1920px;background:{bg};color:{fg}">
          <div class="abs t" style="left:90px;top:330px;width:900px;font-size:76px">{frase}</div>
          <div class="abs" style="left:90px;top:850px;width:320px;height:320px;border-radius:80px;background:{acc};display:flex;align-items:center;justify-content:center;transform:rotate(-4deg)">{icon(ic, 240, casa)}</div>
          <div class="abs t" style="left:90px;top:1330px;width:900px;font-size:70px;color:{acc}">{prompt}</div>
          <div class="abs" style="left:90px;top:1500px">{assinatura(240, casa)}</div></section>'''
        if cs:
            f3 = f'''<section class="page casal" style="width:1080px;height:1920px;background:var(--creme);color:var(--vinho)">
              <div class="abs" style="left:90px;top:300px">{assinatura(300, 'casal')}</div>
              <div class="abs t" style="left:90px;top:430px;width:900px;font-size:110px">A retrospectiva de <span class="hl">vocês dois.</span></div>
              <div class="abs" style="left:90px;top:860px;width:900px;font-size:46px;font-weight:700;line-height:1.5">✓ Troféus do casal, feitos da conversa<br>✓ Quem manda mais, quem responde mais rápido<br>✓ Nada sai do seu celular</div>
              <div class="abs" style="left:90px;top:1360px;width:900px;height:140px;border-radius:30px;background:var(--cereja);color:#fff;display:flex;align-items:center;justify-content:center;font:800 56px/1 'Bricolage Grotesque'">Fazer a de vocês →</div>
              <div class="abs mono" style="left:0;right:0;top:1550px;text-align:center;font-size:38px">retrozap.com.br</div></section>'''
        else:
            f3 = f'''<section class="page" style="width:1080px;height:1920px;background:var(--noite);color:var(--areia)">
              <div class="abs" style="left:90px;top:300px">{assinatura(300)}</div>
              <div class="abs t" style="left:90px;top:430px;width:900px;font-size:110px">A retrospectiva do seu grupo do WhatsApp.</div>
              <div class="abs" style="left:90px;top:900px;width:900px;font-size:46px;font-weight:700;line-height:1.5">✓ Um troféu pra cada um, feito da conversa do ano<br>✓ Quem fala mais, quem some, quem manda áudio<br>✓ Nada sai do seu celular</div>
              <div class="abs" style="left:90px;top:1360px;width:900px;height:140px;border-radius:30px;background:var(--manga);color:var(--noite);display:flex;align-items:center;justify-content:center;font:800 56px/1 'Bricolage Grotesque'">Fazer a do meu grupo →</div>
              <div class="abs mono" style="left:0;right:0;top:1550px;text-align:center;font-size:38px">retrozap.com.br</div></section>'''
        piece(id=sid, fmt='story', day=d, slot='12h', title=f'Frase pro grupo: {frase} · sequência de 3', w=1080, h=1920, frames=3,
              html=doc(sid, FONTS, CSS, f1 + f2 + f3, 1080, 1920), caption='(story, sem legenda; postar os 3 quadros em sequência, no mesmo horário)', sticker='', kind='story',
              notes=f'Sequência de 3 sem adesivo (formato aprovado no S03): frase em bilhete → pergunta de marcação → CTA ({casa}). Frase nova, sem repetir as das últimas 4 semanas. Sem preço. Motivo de envio: print no grupo.')

def build():
    r_c13(); r_r19(); r_c14(); r_r20(); r_c15(); r_r21(); r_c16(); r_stories()

build()
