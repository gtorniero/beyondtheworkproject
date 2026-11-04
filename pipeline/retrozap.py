"""Retrozap · Pack Semanal 01. Bricolage Grotesque 800 / DM Sans / DM Mono.
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

# =====================================================================================
# R-R1 · Reel · Podcaster do Grupo (cerimônia) · Grupo
# =====================================================================================
def onda(n=34, h=120, color='var(--noite)', seed=3):
    bars = ''
    for i in range(n):
        v = 20 + ((i * 37 + seed * 11) % 100) * (h - 20) / 100
        bars += f'<div style="width:10px;height:{v:.0f}px;border-radius:5px;background:{color}"></div>'
    return f'<div style="display:flex;align-items:center;gap:8px;height:{h}px">{bars}</div>'

def r_r1():
    T = 17.6
    tl = TL(T)
    s1 = f'''<div {tl.scene(0, 3.6, fin=False)}>
      <div class="abs t" style="left:90px;top:330px;width:900px;font-size:110px;{at(.05,'rise')}">Todo grupo tem alguém que manda áudio de <span class="hl">4 minutos.</span></div>
      <div class="abs" style="left:90px;top:900px;width:900px;height:200px;background:var(--areia);border-radius:100px;display:flex;align-items:center;gap:30px;padding:0 50px;{at(.7,'pop')}">
        <div style="width:0;height:0;border-left:56px solid var(--noite);border-top:36px solid transparent;border-bottom:36px solid transparent"></div>
        {onda(30, 110)}<span class="mono" style="color:var(--noite);font-size:44px;font-weight:500">4:07</span></div>
      <div class="abs" style="left:800px;top:1150px;--r:8deg;{at(1.2,'pop')}">{icon('studio-microphone', 190)}</div>
    </div>'''
    s2 = f'''<div {tl.scene(3.6, 7.2)}>
      <div class="abs sim" style="left:90px;top:320px">DADOS DE EXEMPLO · TURMA DO CHURRAS</div>
      <div class="abs t" style="left:90px;top:390px;width:900px;font-size:92px">Na Turma do Churras, 2026 teve:</div>
      <div class="abs box" style="left:90px;top:640px;width:430px;height:330px;padding:40px;{at(3.9,'pop')}"><div class="t hl" style="font-size:150px">312</div><div style="font-size:40px;font-weight:700;margin-top:14px">áudios</div></div>
      <div class="abs box" style="left:560px;top:640px;width:430px;height:330px;padding:40px;background:var(--chiclete);color:var(--noite);{at(4.2,'pop')}"><div class="t" style="font-size:150px">11 h</div><div style="font-size:40px;font-weight:700;margin-top:14px">de áudio no total</div></div>
      <div class="abs" style="left:90px;top:1060px;width:900px;font-size:46px;font-weight:700;{at(5.0,'rise')}">Mais da metade veio de uma pessoa só.</div>
    </div>'''
    s3 = f'''<div {tl.scene(7.2, 10.0)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:104px;text-align:center;{at(7.3,'rise')}">E o troféu de <span class="hl">Podcaster do Grupo</span> vai para…</div>
      {dots(420, 940, 60, 'var(--manga)', 8.0)}
    </div>'''
    s4 = f'''<div {tl.scene(10.0, 14.0)}>
      <div class="abs" style="left:390px;top:330px;{at(10.0,'pop')}">{taca(300)}</div>
      <div class="abs" style="left:0;right:0;top:690px;text-align:center;--r:-3deg;{at(10.5,'drop', .6)}"><span class="selo t" style="font-size:150px">Juninho</span></div>
      <div class="abs" style="left:0;right:0;top:960px;text-align:center;{at(11.2,'rise')}"><span class="tag" style="font-size:36px">Podcaster do Grupo</span></div>
      <div class="abs" style="left:90px;right:90px;top:1080px;text-align:center;font-size:52px;font-weight:700;{at(11.7,'rise')}">171 áudios. 6 h 12 min só dele.</div>
    </div>'''
    s5 = f'''<div {tl.scene(14.0, T, fout=False)}>
      <div class="abs" style="left:0;right:0;top:470px;display:flex;justify-content:center;{at(14.1,'pop')}">{assinatura(700)}</div>
      <div class="abs t" style="left:0;right:0;top:760px;text-align:center;font-size:96px;{at(14.5,'rise')}">e o seu grupo?</div>
      <div class="abs" style="left:0;right:0;top:920px;text-align:center;{at(14.9,'rise')}"><span class="tag" style="background:var(--manga);color:var(--noite);border-color:var(--manga);font-size:36px">1º grupo grátis</span></div>
      <div class="foot" style="top:1080px;font-size:40px;{at(15.2,'fade')}">retrozap.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}{s5}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs" style="left:80px;top:80px">{taca(110)}</div>
      <div class="abs t" style="left:80px;top:250px;width:920px;font-size:104px">Todo grupo tem alguém que manda áudio de <span class="hl">4 minutos.</span></div>
      <div class="abs" style="left:80px;top:830px;width:920px;height:190px;background:var(--areia);border-radius:95px;display:flex;align-items:center;gap:28px;padding:0 46px">
        <div style="width:0;height:0;border-left:52px solid var(--noite);border-top:34px solid transparent;border-bottom:34px solid transparent"></div>{onda(30, 100)}<span class="mono" style="color:var(--noite);font-size:42px">4:07</span></div>
      <div class="abs" style="left:800px;top:1080px;transform:rotate(8deg)">{icon('studio-microphone', 170)}</div></div>'''
    piece(id='R-R1', fmt='reel', day=1, slot='19h45', title='Podcaster do Grupo (cerimônia)', total=T, poster=.65,
          html=doc('R-R1', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--noite)'),
          caption=('Todo grupo tem alguém que manda áudio de 4 minutos. 🎙️\n\n'
                   'No Retrozap, essa pessoa ganha troféu: Podcaster do Grupo, com a conta exata de áudios e de horas.\n'
                   '(Dados de exemplo. Os do seu grupo saem da sua conversa, no seu celular.)\n\n'
                   'Marca o podcaster da sua turma 👇\nretrozap.com.br · 1º grupo grátis\n'
                   '#retrozap #retrospectiva2026 #grupodeamigos #audio #resenha'),
          notes='Cerimônia: suspense de 0,5 s com os pontinhos antes do nome; selo Manga cai girando. Efeitos: tambor, aplauso curto.')

# =====================================================================================
# R-C1 · Carrossel · Tier list dos membros de todo grupo · Grupo
# =====================================================================================
def membro(icon_name, nome, txt, bg='var(--acai)', fg='var(--areia)', rot=0, w=900):
    return f'''<div class="box" style="width:{w}px;padding:34px 40px;display:flex;gap:32px;align-items:center;background:{bg};color:{fg};transform:rotate({rot}deg)">
      {icon(icon_name, 150)}<div><div class="t" style="font-size:62px">{nome}</div><div style="font-size:36px;font-weight:500;margin-top:10px;line-height:1.25">{txt}</div></div></div>'''

def tier_badge(letter, bg, size=220, fg='var(--noite)'):
    return f'<div class="t" style="width:{size}px;height:{size}px;border-radius:40px;background:{bg};color:{fg};display:flex;align-items:center;justify-content:center;font-size:{size*.7:.0f}px">{letter}</div>'

def r_c1():
    tiers = [('S', 'var(--manga)'), ('A', 'var(--chiclete)'), ('B', 'var(--piscina)'), ('C', 'var(--uva)')]
    capa_rows = ''.join(f'<div style="display:flex;gap:20px;margin-bottom:20px;align-items:center">{tier_badge(l, c, 120)}<div style="flex:1;height:120px;border-radius:30px;background:var(--acai2)"></div></div>' for l, c in tiers)
    pages = [page(f'''
      <div class="abs t" style="left:80px;top:90px;width:920px;font-size:112px">Tier list dos membros de <span class="hl">todo grupo</span></div>
      <div class="abs" style="left:80px;top:560px;width:920px">{capa_rows}</div>
      <div class="abs" style="left:780px;top:560px;transform:rotate(8deg)">{icon('ghost', 160)}</div>
      <div class="abs" style="left:620px;top:840px;transform:rotate(-6deg)">{icon('face-with-tears-of-joy', 140)}</div>
      <div class="abs" style="left:80px;top:1230px;font-size:30px;font-weight:700;opacity:.8">Arrasta. E discorda nos comentários.</div>''')]
    # S: vertical stack
    pages.append(page(f'''
      <div class="abs" style="left:80px;top:90px">{tier_badge('S', 'var(--manga)')}</div>
      <div class="abs t" style="left:340px;top:120px;width:660px;font-size:70px">Sem eles, o grupo morre.</div>
      <div class="abs" style="left:80px;top:420px">{membro('high-voltage-sign', 'O Puxa-Assunto', 'Manda "bom dia" às 7h e o grupo acorda.', rot=-1)}</div>
      <div class="abs" style="left:80px;top:800px">{membro('heart-hands', 'O Coração Mole', 'Lembra de todo aniversário. Até do cachorro.', 'var(--manga)', 'var(--noite)', 1)}</div>'''))
    # A: big card + side
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--chiclete)"></div>
      <div class="abs" style="right:80px;top:90px">{tier_badge('A', 'var(--noite)', fg='var(--chiclete)')}</div>
      <div class="abs t" style="left:80px;top:110px;width:600px;font-size:72px;color:var(--noite)">Fazem o grupo valer a pena.</div>
      <div class="abs" style="left:80px;top:420px;width:920px;height:440px;background:var(--noite);border-radius:40px;padding:50px">
        <div style="display:flex;gap:36px;align-items:center">{icon('face-with-tears-of-joy', 200)}<div class="t" style="font-size:80px">O Rei do Kkkk</div></div>
        <div style="font-size:42px;margin-top:30px;line-height:1.25">Ri de tudo. Até de figurinha repetida.</div></div>
      <div class="abs" style="left:80px;top:910px;width:920px;color:var(--noite)">{membro('speech-balloon', 'O Tagarela', 'Responde antes de você terminar de digitar.', 'var(--areia)', 'var(--noite)')}</div>'''))
    # B: two columns
    col = lambda i, n, t, bg: f'''<div style="width:440px;height:640px;background:{bg};border-radius:40px;padding:40px;color:var(--noite)">{icon(i, 170)}<div class="t" style="font-size:66px;margin-top:30px">{n}</div><div style="font-size:36px;margin-top:20px;line-height:1.25">{t}</div></div>'''
    pages.append(page(f'''
      <div class="abs" style="left:80px;top:90px">{tier_badge('B', 'var(--piscina)')}</div>
      <div class="abs t" style="left:340px;top:120px;width:660px;font-size:70px">Amamos. Com moderação.</div>
      <div class="abs" style="left:80px;top:440px;width:920px;display:flex;justify-content:space-between">
        {col('studio-microphone', 'O Podcaster', 'Áudio de 4 minutos que começa com "rapidinho".', 'var(--piscina)')}
        {col('serious-face-with-symbols-covering-mouth', 'O Boca-Suja', 'Ninguém lê o grupo em voz alta perto da avó.', 'var(--goiaba)')}</div>'''))
    # C: lista com riscado
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--uva)"></div>
      <div class="abs" style="left:80px;top:90px">{tier_badge('C', 'var(--noite)', fg='var(--uva)')}</div>
      <div class="abs t" style="left:340px;top:120px;width:660px;font-size:70px;color:var(--noite)">Sabemos que estão aí. Em algum lugar.</div>
      <div class="abs" style="left:80px;top:470px;width:920px;color:var(--noite)">
        <div style="display:flex;gap:34px;align-items:flex-start;margin-bottom:60px">{icon('ghost', 190)}<div><div class="t" style="font-size:76px">O Fantasma</div><div style="font-size:40px;margin-top:14px;line-height:1.25">Visualiza. Some. Reaparece no dia do churrasco.</div></div></div>
        <div style="display:flex;gap:34px;align-items:flex-start">{icon('wastebasket', 190)}<div><div class="t" style="font-size:76px">O Apaga Mensagens</div><div class="mono" style="font-size:36px;margin-top:14px">"mensagem apagada" · 02:14</div></div></div></div>'''))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:100px">Discorda? <span class="hl">Prova.</span></div>
      <div class="abs" style="left:80px;top:420px;width:920px;font-size:46px;font-weight:500;line-height:1.3">O Retrozap lê a conversa do seu grupo no seu celular e entrega os troféus com número: quem fala mais, quem some, quem ri de tudo.</div>
      <div class="abs" style="left:80px;top:860px;display:flex;gap:24px">{icon('speech-balloon',130)}{icon('ghost',130)}{icon('face-with-tears-of-joy',130)}{icon('studio-microphone',130)}{icon('heart-hands',130)}</div>
      <div class="abs" style="left:80px;top:1130px">{assinatura(420)}</div>
      <div class="abs" style="right:80px;top:1175px;font-size:34px;font-weight:700">retrozap.com.br</div>'''))
    piece(id='R-C1', fmt='carrossel', day=2, slot='12h30', title='Tier list dos membros de todo grupo', w=1080, h=1350,
          html=doc('R-C1', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Tier list oficial dos membros de todo grupo. 🏆\n\n'
                   'S: o Puxa-Assunto e o Coração Mole.\nA: o Rei do Kkkk e o Tagarela.\nB: o Podcaster e o Boca-Suja.\nC: o Fantasma e o Apaga Mensagens.\n\n'
                   'Discorda? Comenta a sua. E marca o Fantasma (se ele aparecer) 👻\n'
                   'retrozap.com.br\n#retrozap #grupodeamigos #tierlist #amigos #resenha'),
          notes='Uma cor de apoio por página (Manga, Chiclete, Piscina, Uva) e uma composição diferente em cada tier.')

# =====================================================================================
# R-R2 · Reel · Duelo do casal (Dani × Cris) · Casal
# =====================================================================================
def r_r2():
    T = 18.2
    tl = TL(T)
    kf = []
    def contador(name, val, t0, dur=1.1):
        kf.append(f'@keyframes {name}{{from{{--n:0}}to{{--n:{val}}}}}')
        return f'<span class="cnt" style="animation:{name} {dur}s cubic-bezier(.2,.8,.2,1) {t0:.2f}s 1 both"></span>'
    s1 = f'''<div {tl.scene(0, 3.2, fin=False)}>
      <div class="abs t" style="left:90px;top:400px;width:900px;font-size:150px;text-align:center;{at(.05,'pop')}">Dani <span class="hl">×</span> Cris</div>
      <div class="abs t" style="left:90px;top:640px;width:900px;font-size:84px;text-align:center;{at(.6,'rise')}">2026 inteiro. Quem ama mais, em números?</div>
      <div class="abs" style="left:430px;top:1000px;{at(1.1,'pop')}">{icon('two-hearts', 220, 'casal')}</div>
    </div>'''
    rounds = [('Quem puxou a conversa', 214, 151, 'heart-with-arrow'), ('"Boa noite"', 188, 301, 'crescent-moon'), ('"Te amo"', 97, 96, 'heavy-black-heart')]
    sc = ''
    t = 3.2
    for i, (cat, a, b, ic) in enumerate(rounds):
        win = 'a' if a > b else 'b'
        ca = 'var(--cereja)' if win == 'a' else 'var(--vinho)'
        cb = 'var(--cereja)' if win == 'b' else 'var(--vinho)'
        sc += f'''<div {tl.scene(t, t + 3.4)}>
          <div class="abs" style="left:0;right:0;top:320px;text-align:center"><span class="tag" style="font-size:34px">Rodada {i+1} de 3</span></div>
          <div class="abs t" style="left:60px;right:60px;top:420px;text-align:center;font-size:96px">{cat}</div>
          <div class="abs" style="left:90px;top:640px;width:420px;height:640px;border-radius:40px;background:{ca};color:var(--creme);padding:40px;text-align:center;{at(t + .15,'slideL')}">
            <div class="t" style="font-size:70px">Dani</div><div class="t" style="font-size:190px;margin-top:80px">{contador(f'ca{i}', a, t + .4)}</div></div>
          <div class="abs" style="left:570px;top:640px;width:420px;height:640px;border-radius:40px;background:{cb};color:var(--creme);padding:40px;text-align:center;{at(t + .15,'slideR')}">
            <div class="t" style="font-size:70px">Cris</div><div class="t" style="font-size:190px;margin-top:80px">{contador(f'cb{i}', b, t + .4)}</div></div>
          <div class="abs" style="left:{90 if win=='a' else 570}px;top:1200px;width:420px;text-align:center;--r:-4deg;{at(t + 1.8,'stamp')}"><span class="t" style="display:inline-block;background:var(--creme);color:var(--cereja);border:6px solid var(--cereja);padding:10px 28px;font-size:52px;border-radius:14px">ponto!</span></div>
          <div class="abs" style="left:465px;top:880px;{at(t + .3,'pop')}">{icon(ic, 150, 'casal')}</div>
        </div>'''
        t += 3.4
    s5 = f'''<div {tl.scene(t, t + 2.6)}>
      <div class="abs t" style="left:60px;right:60px;top:460px;text-align:center;font-size:120px">Dani 2 <span class="hl">×</span> 1 Cris</div>
      <div class="abs" style="left:0;right:0;top:720px;text-align:center;--r:-3deg;{at(t + .5,'drop')}"><span class="selo t" style="font-size:76px">Quem perdeu paga o jantar.</span></div>
      <div class="abs" style="left:440px;top:950px;{at(t + 1.0,'pop')}">{icon('receipt', 200, 'casal')}</div>
    </div>'''
    t += 2.6
    s6 = f'''<div {tl.scene(t, T, fout=False)}>
      <div class="abs" style="left:0;right:0;top:470px;display:flex;justify-content:center;{at(t + .1,'pop')}">{assinatura(700, 'casal')}</div>
      <div class="abs t" style="left:0;right:0;top:760px;text-align:center;font-size:100px;{at(t + .4,'rise')}">e o de vocês?</div>
      <div class="foot" style="top:940px;font-size:40px;{at(t + .8,'fade')}">retrozap.com.br</div>
    </div>'''
    body = f'<section class="page casal" style="width:1080px;height:1920px"><div class="abs sim" style="right:90px;top:1500px">DADOS DE EXEMPLO</div>{s1}{sc}{s5}{s6}</section>'
    cover_body = f'''<div class="page casal" style="width:1080px;height:1350px">
      <div class="abs" style="left:80px;top:80px">{taca(110, 'casal')}</div>
      <div class="abs t" style="left:80px;top:250px;width:920px;font-size:150px">Dani <span class="hl">×</span> Cris</div>
      <div class="abs t" style="left:80px;top:440px;width:920px;font-size:84px">Quem ama mais, em números?</div><div class="abs sim" style="right:80px;top:1250px">DADOS DE EXEMPLO</div>
      <div class="abs" style="left:80px;top:720px;width:430px;height:500px;border-radius:40px;background:var(--cereja);color:var(--creme);padding:40px;text-align:center"><div class="t" style="font-size:64px">Dani</div><div class="t" style="font-size:170px;margin-top:60px">214</div></div>
      <div class="abs" style="left:570px;top:720px;width:430px;height:500px;border-radius:40px;background:var(--vinho);color:var(--creme);padding:40px;text-align:center"><div class="t" style="font-size:64px">Cris</div><div class="t" style="font-size:170px;margin-top:60px">151</div></div></div>'''
    piece(id='R-R2', fmt='reel', day=4, slot='19h45', title='Duelo do casal: Dani × Cris', total=T, poster=.3,
          html=doc('R-R2', FONTS, CSS + tl.style() + ''.join(kf), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--creme)'),
          caption=('Dani × Cris. 2026 inteiro. Quem ama mais, em números? 💘\n\n'
                   'No Retrozap Casais vocês recebem o "um contra o outro": quem puxou mais conversa, quem mandou mais boa noite, quem disse mais te amo.\n'
                   'Quem perde paga o jantar. (Regra da casa, não do app.)\n\n'
                   'Marca quem vai pagar 👇\nretrozap.com.br\n#retrozap #casal #namorados #retrospectiva2026 #amor'),
          notes='Casa Casal: creme, cereja e vinho, sem roxo. Contadores sobem de 0 até o valor. Dados de exemplo (Dani & Cris).')

# =====================================================================================
# R-C2 · Carrossel · O que vem na sua retrospectiva (PRODUTO) · Grupo
# =====================================================================================
def r_c2():
    pages = []
    pages.append(page(f'''
      <div class="abs" style="left:80px;top:90px">{assinatura(380)}</div>
      <div class="abs t" style="left:80px;top:330px;width:920px;font-size:150px">Seu 2026, <span class="hl">premiado.</span></div>
      <div class="abs" style="left:80px;top:700px;width:760px;font-size:46px;line-height:1.3">O que vem na retrospectiva do seu grupo, ato por ato.</div>
      <div class="abs" style="left:660px;top:880px;transform:rotate(6deg)">{taca(340)}</div>
      <div class="abs" style="left:80px;top:1180px"><span class="tag">Arrasta →</span></div>'''))
    # Ato I: gráfico ano a ano (exemplo)
    anos = [('2021', 18), ('2022', 34), ('2023', 52), ('2024', 61), ('2025', 78), ('2026', 100)]
    barras = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px;justify-content:flex-end;height:420px"><div style="width:110px;height:{v*3.6:.0f}px;border-radius:18px 18px 6px 6px;background:{"var(--manga)" if a=="2026" else "var(--piscina)"}"></div><span class="mono" style="font-size:28px">{a}</span></div>' for a, v in anos)
    pages.append(page(f'''
      <div class="abs mono" style="left:80px;top:90px;font-size:30px;color:var(--manga)">ATO I · CONHECENDO O GRUPO</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:90px">Há quanto tempo vocês existem e quanto falaram.</div>
      <div class="abs" style="left:80px;top:620px;width:920px;display:flex;justify-content:space-between">{barras}</div>
      <div class="abs sim" style="left:80px;top:1200px">MENSAGENS POR ANO · DADOS DE EXEMPLO</div>'''))
    # Ato II: troféus
    cats = [('speech-balloon', 'O Tagarela'), ('studio-microphone', 'Podcaster do Grupo'), ('serious-face-with-symbols-covering-mouth', 'Boca-Suja'),
            ('face-with-tears-of-joy', 'Rei do Kkkk'), ('high-voltage-sign', 'Puxa-Assunto'), ('ghost', 'O Fantasma'), ('heart-hands', 'Coração Mole')]
    lst = ''.join(f'<div style="display:flex;align-items:center;gap:26px;height:104px">{icon(i, 88)}<span class="t" style="font-size:52px">{n}</span></div>' for i, n in cats)
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--manga)"></div>
      <div class="abs mono" style="left:80px;top:90px;font-size:30px;color:var(--noite)">ATO II · OS TROFÉUS</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:90px;color:var(--noite)">Um vencedor por categoria. Revelado um por um.</div>
      <div class="abs" style="left:80px;top:460px;width:920px;color:var(--noite)">{lst}</div>'''))
    # Ato III
    pages.append(page(f'''
      <div class="abs mono" style="left:80px;top:90px;font-size:30px;color:var(--manga)">ATO III · GRAN FINALE</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:90px">Nosso 2026, o assunto do ano e o Top 3.</div>
      <div class="abs" style="left:80px;top:540px;width:920px;display:grid;grid-template-columns:1fr 1fr;gap:28px">
        <div class="box" style="padding:40px;height:300px"><div class="t hl" style="font-size:110px">18.402</div><div style="font-size:36px;margin-top:10px">mensagens em 2026</div></div>
        <div class="box" style="padding:40px;height:300px;background:var(--chiclete);color:var(--noite)"><div class="t" style="font-size:110px">Top 8%</div><div style="font-size:36px;margin-top:10px">dos grupos do Brasil</div></div>
        <div class="box" style="padding:40px;height:300px;background:var(--piscina);color:var(--noite);grid-column:span 2;display:flex;align-items:center;gap:40px">{icon('slice-of-pizza',170)}<div><div style="font-size:34px">assunto mais falado</div><div class="t" style="font-size:96px">pizza</div></div></div></div>
      <div class="abs sim" style="left:80px;top:1230px">DADOS DE EXEMPLO · TURMA DO CHURRAS</div>'''))
    # Privacidade
    pages.append(page(f'''
      <div class="abs" style="left:80px;top:150px">{icon('lock', 240)}</div>
      <div class="abs t" style="left:80px;top:480px;width:920px;font-size:104px">Sua conversa não sai do seu <span class="hl">celular.</span></div>
      <div class="abs" style="left:80px;top:860px;width:900px;font-size:44px;line-height:1.35">O arquivo é lido no seu próprio navegador. Nenhuma mensagem, nome ou telefone vai para servidor nenhum.</div>'''))
    # Preço
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--manga)"></div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:150px;color:var(--noite)">1º grupo grátis.</div>
      <div class="abs" style="left:80px;top:480px;width:920px;background:var(--noite);border-radius:40px;padding:50px">
        <div class="t" style="font-size:96px;color:var(--manga)">R$ 8,99</div>
        <div style="font-size:42px;margin-top:20px;line-height:1.35">Pagamento único, no Pix ou no cartão: grupos ilimitados, casal, mídias especiais e vídeo para baixar.</div></div>
      <div class="abs" style="left:80px;top:1110px">{assinatura(420, inv=True)}</div>
      <div class="abs" style="right:80px;top:1155px;font-size:36px;font-weight:700;color:var(--noite)">retrozap.com.br</div>'''))
    pages[-1] = pages[-1].replace('<section class="page ', '<section class="page ', 1)
    piece(id='R-C2', fmt='carrossel', day=5, slot='12h30', title='O que vem na sua retrospectiva (produto)', kind='produto', w=1080, h=1350,
          html=doc('R-C2', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Seu 2026, premiado. 🏆 O que vem na retrospectiva do seu grupo:\n\n'
                   'Ato I: há quanto tempo vocês existem e quanto falaram, ano a ano.\n'
                   'Ato II: os troféus, um vencedor por categoria, revelados um por um.\n'
                   'Ato III: o 2026 em números, o assunto do ano e o Top 3.\n\n'
                   'Sua conversa não sai do celular: tudo é lido no seu navegador.\n'
                   '1º grupo grátis. Acesso completo por R$ 8,99, pagamento único.\n'
                   'retrozap.com.br (link na bio)\n#retrozap #retrospectiva2026 #grupodewhatsapp #amigos'),
          notes='Peça de produto 1 de 2 da semana. Preço conferido no CLAUDE.md do repositório (R$ 8,99 desde 01/11). Números do Ato III são de exemplo e estão marcados.')

# =====================================================================================
# R-R3 · Reel · Notificações das 3h12 · Grupo
# =====================================================================================
def notif(nome, txt, hora, y, t, icon_name='speech-balloon', audio=False):
    corpo = (f'<span style="display:inline-flex;align-items:center;gap:14px">{icon("microphone", 46)} Áudio · {txt}</span>' if audio else txt)
    return f'''<div class="abs" style="left:70px;width:940px;top:{y}px;background:var(--acai);border:3px solid var(--linha);border-radius:36px;padding:26px 30px;display:flex;gap:24px;align-items:center;{at(t,'rise', .35)}">
      <div style="flex:none;width:84px;height:84px;border-radius:22px;background:var(--areia);display:flex;align-items:center;justify-content:center">{icon(icon_name, 70)}</div>
      <div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;font-size:28px;color:var(--neblina);font-weight:700"><span>Turma do Churras</span><span>{hora}</span></div>
      <div style="font-size:38px;margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"><b>{nome}:</b> {corpo}</div></div></div>'''

def r_r3():
    T = 18.8
    tl = TL(T)
    s0 = f'''<div {tl.scene(0, 3.0, fin=False)}>
      <div class="abs t" style="left:0;right:0;top:400px;text-align:center;font-size:260px;{at(.05,'fade', .3)}">03:12</div>
      <div class="abs t" style="left:90px;right:90px;top:760px;text-align:center;font-size:84px;{at(.6,'rise')}">E o grupo <span class="hl">ainda</span> está acordado.</div>
      {dots(450, 1050, 50, 'var(--manga)', 1.2)}
    </div>'''
    msgs = [('Caio', 'alguém viu meu carregador branco?', '03:12'), ('Lu', 'gente quem leva o gelo sábado', '03:12'),
            ('Pedrão', 'eu levo', '03:13'), ('Pedrão', 'mentira não levo kkkkk', '03:13'),
            ('Bia', '1:48', '03:14', True), ('Pedrão', 'bom dia pra quem já tá acordado', '03:15'),
            ('Pedrão', 'e pra quem não tá também', '03:15'), ('Rafa', 'pedrão vai dormir', '03:16')]
    stack = ''
    for i, m in enumerate(msgs):
        nome, txt, hora = m[:3]
        stack += notif(nome, txt, hora, 300 + i * 158, 3.15 + i * .55, audio=len(m) > 3)
    s1 = f'''<div {tl.scene(3.0, 9.0)}>{stack}<div class="abs sim" style="left:70px;top:1590px">SIMULAÇÃO · NOMES DE EXEMPLO</div></div>'''
    s2 = f'''<div {tl.scene(9.0, 12.2)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:120px;{at(9.1,'rise')}">47 mensagens.</div>
      <div class="abs t" style="left:90px;top:600px;width:900px;font-size:120px;{at(9.9,'rise')}"><span class="hl">19</span> do Pedrão.</div>
      <div class="abs" style="left:90px;top:900px;font-size:44px;{at(10.6,'fade')}">Às 3 da manhã. De uma terça.</div>
    </div>'''
    s3 = f'''<div {tl.scene(12.2, 15.6)}>
      <div class="abs t" style="left:0;right:0;top:380px;text-align:center;font-size:76px;{at(12.3,'rise')}">O Tagarela de 2026 é…</div>
      {dots(450, 560, 50, 'var(--manga)', 12.7, 1)}
      <div class="abs" style="left:420px;top:540px;{at(13.4,'pop')}">{icon('speech-balloon', 240)}</div>
      <div class="abs" style="left:0;right:0;top:850px;text-align:center;--r:-3deg;{at(13.6,'drop', .6)}"><span class="selo t" style="font-size:160px">Pedrão</span></div>
      <div class="abs" style="left:0;right:0;top:1130px;text-align:center;font-size:46px;font-weight:700;{at(14.3,'rise')}">E ninguém ficou surpreso.</div>
    </div>'''
    s4 = f'''<div {tl.scene(15.6, T, fout=False)}>
      <div class="abs" style="left:0;right:0;top:470px;display:flex;justify-content:center;{at(15.7,'pop')}">{assinatura(700)}</div>
      <div class="abs t" style="left:0;right:0;top:760px;text-align:center;font-size:96px;{at(16.0,'rise')}">e o seu grupo?</div>
      <div class="foot" style="top:920px;font-size:40px;{at(16.4,'fade')}">retrozap.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s0}{s1}{s2}{s3}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:0;right:0;top:120px;text-align:center;font-size:250px">03:12</div>
      <div class="abs t" style="left:80px;right:80px;top:430px;text-align:center;font-size:84px">E o grupo <span class="hl">ainda</span> está acordado.</div>
      <div style="position:absolute;left:0;top:-30px;width:1080px;height:1350px">{notif('Caio', 'alguém viu meu carregador branco?', '03:12', 720, 0).replace('animation','x-a')}{notif('Pedrão', 'mentira não levo kkkkk', '03:13', 880, 0).replace('animation','x-a')}{notif('Bia', '1:48', '03:14', 1040, 0, audio=True).replace('animation','x-a')}</div></div>'''
    piece(id='R-R3', fmt='reel', day=7, slot='19h45', title='03:12 e o grupo acordado (Tagarela)', total=T, poster=.4,
          html=doc('R-R3', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--noite)'),
          caption=('03:12. E o grupo ainda está acordado. 🌙\n\n'
                   '47 mensagens, 19 do mesmo amigo. Todo grupo tem o seu Tagarela, e o Retrozap faz a conta certinha.\n'
                   '(Simulação com nomes de exemplo.)\n\n'
                   'Marca o Pedrão da sua turma 👇\nretrozap.com.br · 1º grupo grátis\n'
                   '#retrozap #grupodeamigos #madrugada #tagarela #resenha #retrospectiva2026'),
          notes='Notificações genéricas (sem marca de app). Etiqueta "simulação" visível. Som: notificação genérica, nunca a do WhatsApp.')

# =====================================================================================
# Stories
# =====================================================================================
def story(body, cls='', bg=''):
    return f'<section class="page {cls}" style="width:1080px;height:1920px;{bg}">{body}</section>'

def r_stories():
    S = []
    S.append(('R-S1', 1, 'Enquete: seu grupo tem um Fantasma?', story(f'''
      <div class="abs" style="inset:0;background:var(--uva)"></div>
      <div class="abs" style="left:80px;top:290px">{icon('ghost', 260)}</div>
      <div class="abs t" style="left:80px;top:620px;width:920px;font-size:130px;color:var(--noite)">Seu grupo tem um Fantasma?</div>'''),
      'Adesivo de ENQUETE em y≈1150–1400: "Tem" / "Sou eu".', 'Uva + Noite (mapa do guia para Fantasma).'))
    S.append(('R-S2', 3, 'Enquete: o troféu mais disputado', story(f'''
      <div class="abs" style="inset:0;background:var(--piscina)"></div>
      <div class="abs t" style="left:80px;top:300px;width:920px;font-size:112px;color:var(--noite)">Qual troféu seria o mais disputado na sua turma?</div>
      <div class="abs" style="left:80px;top:1380px;display:flex;gap:24px">{icon('speech-balloon',140)}{icon('ghost',140)}{icon('face-with-tears-of-joy',140)}{icon('studio-microphone',140)}</div>'''),
      'Adesivo de ENQUETE com 4 opções em y≈850–1320: Tagarela / Fantasma / Rei do Kkkk / Podcaster.', 'Piscina + Noite.'))
    S.append(('R-S3', 4, 'Casal: quem manda mais boa noite?', story(f'''
      <div class="abs" style="left:80px;top:290px">{icon('crescent-moon', 220, 'casal')}</div>
      <div class="abs t" style="left:80px;top:580px;width:920px;font-size:120px">Quem manda mais "boa noite" aí?</div>
      <div class="abs" style="left:80px;top:1400px;font-size:40px;width:900px">No Retrozap Casais, a gente conta.</div>''', 'casal'),
      'Adesivo de SLIDER em y≈1050–1300 (ícone de coração do Instagram).', 'Casa Casal. Sem roxo.'))
    S.append(('R-S4', 5, 'Privacidade em uma frase', story(f'''
      <div class="abs" style="left:80px;top:300px">{icon('lock', 220)}</div>
      <div class="abs mono" style="left:80px;top:600px;font-size:32px;color:var(--manga)">EM UMA FRASE</div>
      <div class="abs t" style="left:80px;top:660px;width:920px;font-size:118px">Sua conversa não sai do seu <span class="hl">celular.</span></div>
      <div class="abs" style="left:80px;top:1150px;width:900px;font-size:42px;line-height:1.35">O arquivo é lido no seu navegador. Nada de mensagem, nome ou telefone vai para servidor.</div>'''),
      'Sem adesivo (ou adesivo de link para a página de privacidade).', 'Editorial de confiança.'))
    S.append(('R-S5', 6, 'Link: faça o do seu grupo', story(f'''
      <div class="abs" style="inset:0;background:var(--manga)"></div>
      <div class="abs" style="left:80px;top:290px">{taca(200, inv=True)}</div>
      <div class="abs t" style="left:80px;top:540px;width:920px;font-size:130px;color:var(--noite)">Faça o do seu grupo.</div>
      <div class="abs t" style="left:80px;top:840px;width:920px;font-size:84px;color:var(--noite)">O 1º é grátis.</div>
      <div class="abs" style="left:80px;top:1450px;font-size:38px;font-weight:700;color:var(--noite)">retrozap.com.br</div>'''),
      'Adesivo de LINK em y≈1100–1350.', 'Grupo invertido: taça Noite sobre Manga.'))
    for sid, day, title, body, sticker, notes in S:
        piece(id=sid, fmt='story', day=day, title=title, w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker=sticker, notes=notes, kind='story')

r_r1(); r_c1(); r_r2(); r_c2(); r_r3(); r_stories()
CTA = {
    'R-S1': ('enquete', 1130, ['Tem', 'Sou eu'], 'Responde no direct.'),
    'R-S2': ('enquete', 820, ['Tagarela', 'Fantasma', 'Rei do Kkkk', 'Podcaster'], 'Vota no direct.'),
    'R-S3': ('slider', 1060, None, 'De 0 a 10? Responde no direct.'),
    'R-S5': ('link', 1120, None, 'Link na bio · retrozap.com.br'),
}
def _st(i):
    if i == 'R-S3':
        return {'bgs': ['#FFD6E2'], 'fg': '#5E0B2B', 'tfont': "'Bricolage Grotesque'", 'bfont': "'DM Sans'", 'border': '0', 'radius': '34px', 'shadow': 'none', 'txt_color': '#5E0B2B'}
    if i == 'R-S5':
        return {'bgs': ['#1A0B2E'], 'fg': '#FFC23C', 'tfont': "'Bricolage Grotesque'", 'bfont': "'DM Sans'", 'border': '0', 'radius': '999px', 'shadow': 'none', 'txt_color': '#1A0B2E', 'ts_big': 48}
    return {'bgs': ['#1A0B2E'], 'fg': '#FFF4E0', 'tfont': "'Bricolage Grotesque'", 'bfont': "'DM Sans'", 'border': '0', 'radius': '30px', 'shadow': 'none', 'txt_color': '#1A0B2E', 'fs': 46}
C.apply_ctas(CTA, _st)
