"""SPORT DNA · Pack Semanal 03. Archivo ExtraBold / DM Sans / JetBrains Mono; Syne só em números de destaque e logos.
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



CSS += """
@keyframes tierIn{0%{opacity:0;transform:translateY(-60px) scale(.9)}100%{opacity:1;transform:none}}
@keyframes knobOn{0%{transform:translateX(0)}100%{transform:translateX(96px)}}
@keyframes knobOff{0%{transform:translateX(96px)}100%{transform:translateX(0)}}
@keyframes trackOn{0%{background:#3A3A38}100%{background:var(--surf)}}
@keyframes trackOff{0%{background:var(--surf)}100%{background:#3A3A38}}
@keyframes strike{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}
.grid-bg{background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:60px 60px}
.light .grid-bg,.grid-bg.l{background-image:linear-gradient(rgba(0,0,0,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(0,0,0,.06) 2px,transparent 2px)}
"""

# ------------------------------------------------------------------ desenhos técnicos (linha, sem marca)
def svg_drop(cor, ink='#fff', w=900):
    """Tênis de perfil, só a sola: calcanhar mais alto que a ponta, com as cotas."""
    return f'''<svg width="{w}" height="{int(w*.52)}" viewBox="0 0 900 470" fill="none" font-family="JetBrains Mono" font-size="26">
      <path d="M90 300 C90 200 140 150 230 140 L420 120 C520 110 600 150 690 210 L800 270 C840 292 840 330 800 340 L130 340 C100 340 90 325 90 300 Z" stroke="{ink}" stroke-width="5" opacity=".9"/>
      <path d="M90 300 L90 410 L800 410 C830 410 845 380 840 350 L800 340 L130 340" stroke="{ink}" stroke-width="5"/>
      <path d="M92 372 L800 372" stroke="{cor}" stroke-width="5" stroke-dasharray="14 10"/>
      <path d="M60 340 L60 410" stroke="{cor}" stroke-width="4"/><path d="M48 340 L72 340 M48 410 L72 410" stroke="{cor}" stroke-width="4"/>
      <path d="M870 350 L870 410" stroke="{cor}" stroke-width="4"/><path d="M858 350 L882 350 M858 410 L882 410" stroke="{cor}" stroke-width="4"/>
      <text x="16" y="455" fill="{cor}">32 mm</text><text x="790" y="455" fill="{cor}">24 mm</text>
      <text x="300" y="455" fill="{ink}" opacity=".75">calcanhar → ponta</text>
    </svg>'''

def svg_entressola(cor, ink='#fff', w=900):
    return f'''<svg width="{w}" height="{int(w*.5)}" viewBox="0 0 900 450" fill="none" font-family="JetBrains Mono" font-size="26">
      <path d="M100 250 C100 160 150 120 240 110 L430 92 C530 84 610 120 700 180 L800 236 C836 256 836 286 800 292 L120 292 C104 292 100 275 100 250 Z" stroke="{ink}" stroke-width="5"/>
      <path d="M100 292 L100 360 C100 372 110 376 124 376 L790 376 C826 376 842 340 830 300 L800 292 Z" fill="{cor}" stroke="{ink}" stroke-width="5"/>
      <path d="M124 376 L124 398 L800 398 C820 398 830 390 830 376" stroke="{ink}" stroke-width="5"/>
      <text x="520" y="70" fill="{ink}" opacity=".75">cabedal</text><path d="M560 80 L560 120" stroke="{ink}" stroke-width="3" opacity=".75"/>
      <text x="350" y="345" fill="#0A0A0A" font-weight="700">ENTRESSOLA</text>
      <text x="120" y="440" fill="{ink}" opacity=".75">solado (borracha)</text>
    </svg>'''

def svg_prancha(cor, ink='#fff', w=360, fill='none', rail=None):
    """Prancha vista de cima (funboard genérico)."""
    r = f'<path d="M180 30 C268 120 300 300 296 520 C292 690 262 790 216 840 L144 840 C98 790 68 690 64 520 C60 300 92 120 180 30 Z" stroke="{rail}" stroke-width="26" fill="none" opacity=".95"/>' if rail else ''
    return f'''<svg width="{w}" height="{int(w*2.4)}" viewBox="0 0 360 870" fill="none">
      <path d="M180 30 C268 120 300 300 296 520 C292 690 262 790 216 840 L144 840 C98 790 68 690 64 520 C60 300 92 120 180 30 Z" stroke="{ink}" stroke-width="6" fill="{fill}"/>{r}
      <path d="M180 60 L180 820" stroke="{cor}" stroke-width="3" stroke-dasharray="10 10" opacity=".8"/>
    </svg>'''

def svg_borda(cor, ink='#fff', w=900):
    """Corte transversal da prancha: a borda arredondada ou mais quina."""
    return f'''<svg width="{w}" height="{int(w*.42)}" viewBox="0 0 900 380" fill="none" font-family="JetBrains Mono" font-size="26">
      <path d="M150 150 C300 110 600 110 750 150 C830 170 850 200 810 225 C700 260 200 260 90 225 C50 200 70 170 150 150 Z" stroke="{ink}" stroke-width="5"/>
      <circle cx="95" cy="196" r="64" stroke="{cor}" stroke-width="6"/><circle cx="805" cy="196" r="64" stroke="{cor}" stroke-width="6"/>
      <text x="40" y="320" fill="{cor}">borda</text><text x="760" y="320" fill="{cor}">borda</text>
      <text x="380" y="100" fill="{ink}" opacity=".75">deck</text><text x="370" y="300" fill="{ink}" opacity=".75">fundo</text>
    </svg>'''

def svg_cabo(cor, ink='#fff', w=520):
    """Corte do cabo da raquete: um octógono, com a medida em volta."""
    return f'''<svg width="{w}" height="{w}" viewBox="0 0 520 520" fill="none" font-family="JetBrains Mono" font-size="28">
      <path d="M190 80 L330 80 L430 180 L430 340 L330 440 L190 440 L90 340 L90 180 Z" stroke="{ink}" stroke-width="6"/>
      <circle cx="260" cy="250" r="205" stroke="{cor}" stroke-width="5" stroke-dasharray="16 12"/>
      <text x="200" y="272" fill="{ink}" opacity=".8">cabo</text>
      <text x="150" y="512" fill="{cor}">L1 · L2 · L3 · L4</text>
    </svg>'''

def svg_overgrip(cor, ink='#fff', w=360):
    voltas = ''.join(f'<path d="M60 {120+i*70} L300 {160+i*70}" stroke="{cor}" stroke-width="30" opacity="{.95 if i%2==0 else .75}"/>' for i in range(8))
    return f'''<svg width="{w}" height="{int(w*2)}" viewBox="0 0 360 720" fill="none">
      <rect x="60" y="80" width="240" height="600" rx="30" stroke="{ink}" stroke-width="6"/>
      <clipPath id="cg"><rect x="63" y="83" width="234" height="594" rx="28"/></clipPath><g clip-path="url(#cg)">{voltas}</g>
      <rect x="60" y="80" width="240" height="600" rx="30" stroke="{ink}" stroke-width="6"/>
    </svg>'''

def svg_rigidez(cor, ink='#fff', w=900):
    return f'''<svg width="{w}" height="{int(w*.5)}" viewBox="0 0 900 450" fill="none" font-family="JetBrains Mono" font-size="26">
      <path d="M80 120 L820 120" stroke="{ink}" stroke-width="10" stroke-linecap="round" opacity=".35"/>
      <path d="M80 120 C330 125 600 170 820 250" stroke="{ink}" stroke-width="10" stroke-linecap="round"/>
      <path d="M80 120 C330 122 600 140 820 170" stroke="{cor}" stroke-width="10" stroke-linecap="round"/>
      <path d="M820 70 L820 110 M808 98 L820 112 L832 98" stroke="{ink}" stroke-width="4"/>
      <text x="560" y="300" fill="{ink}">flexível: dobra mais</text><text x="380" y="80" fill="{cor}">rígida: dobra menos</text>
      <path d="M80 380 L820 380" stroke="{ink}" stroke-width="4" opacity=".5"/>
      {''.join(f'<path d="M{80+i*148} 366 L{80+i*148} 394" stroke="{ink}" stroke-width="4" opacity=".5"/><text x="{62+i*148}" y="436" fill="{ink}" opacity=".75">{55+i*5}</text>' for i in range(6))}
      <rect x="450" y="368" width="370" height="24" fill="{cor}" opacity=".9"/>
    </svg>'''

def svg_mostrador(cor, ink='#fff', ang=40, w=520):
    """Mostrador de tensão (genérico): agulha em ang graus (−90 a 90)."""
    import math
    a = math.radians(ang - 90)
    x, y = 260 + 180 * math.cos(a), 300 + 180 * math.sin(a)
    tk = ''.join(f'<path d="M{260+200*math.cos(math.radians(-180+i*18)):.0f} {300+200*math.sin(math.radians(-180+i*18)):.0f} L{260+225*math.cos(math.radians(-180+i*18)):.0f} {300+225*math.sin(math.radians(-180+i*18)):.0f}" stroke="{ink}" stroke-width="5"/>' for i in range(11))
    return f'''<svg width="{w}" height="{int(w*.7)}" viewBox="0 0 520 360" fill="none" font-family="JetBrains Mono" font-size="26">
      <path d="M35 300 A225 225 0 0 1 485 300" stroke="{ink}" stroke-width="6" opacity=".5"/>{tk}
      <path d="M260 300 L{x:.0f} {y:.0f}" stroke="{cor}" stroke-width="10" stroke-linecap="round"/><circle cx="260" cy="300" r="18" fill="{cor}"/>
      <text x="20" y="350" fill="{ink}" opacity=".8">potência</text><text x="400" y="350" fill="{ink}" opacity=".8">controle</text>
    </svg>'''

# =====================================================================================
# D-R8 · Reel meme · RACKET: tier list das desculpas depois de perder (seg 23/11, preto)
# =====================================================================================
def d_r8():
    T = 18.0
    tl = TL(T)
    tiers = [('S', 'var(--racket)'), ('A', '#BFE3F5'), ('B', '#F4F4F2'), ('C', '#A3A3A0'), ('D', '#5C5C58')]
    itens = [('D', 'o adversário só devolve'), ('C', 'a bola tava nova'), ('B', 'o sol na cara'), ('A', 'o vento'), ('S', 'o tênis apertado'), ]
    def board(t0=None, final=False, rh=196, fs=44):
        rows = ''
        for k, c in tiers:
            got = [txt for tk, txt in itens if tk == k]
            cells = ''.join(f'<span style="display:inline-block;background:#2E2E2C;color:#fff;border-radius:16px;padding:16px 24px;font:700 {fs}px/1.1 \'DM Sans\';{at(t0 + itens.index((k, x)) * 1.1, "tierIn", .4) if t0 is not None else ""}">{x}</span>' for x in got)
            if final and k == 'S':
                cells = (f'<span style="display:inline-block;background:#2E2E2C;color:#fff;border-radius:16px;padding:16px 24px;font:700 {fs-6}px/1.1 \'DM Sans\';opacity:.35;text-decoration:line-through">o tênis apertado</span>'
                         f'<span style="display:inline-block;background:var(--racket);color:var(--ink);border-radius:16px;padding:16px 24px;font:800 {fs+4}px/1.1 Archivo;{at(10.6,"stamp",.5) if t0 is not None else "transform:rotate(-3deg)"}">a raquete</span>')
            rows += f'''<div style="display:flex;align-items:stretch;min-height:{rh}px;border-bottom:4px solid var(--ink)">
              <div class="t" style="flex:none;width:{int(rh*.8)}px;background:{c};color:var(--ink);display:flex;align-items:center;justify-content:center;font-size:{int(rh*.5)}px">{k}</div>
              <div style="flex:1;background:#1A1A1A;display:flex;align-items:center;gap:14px;padding:0 20px;flex-wrap:wrap">{cells}</div></div>'''
        return f'<div style="border:4px solid var(--ink);border-radius:20px;overflow:hidden">{rows}</div>'
    s1 = f'''<div {tl.scene(0, 3.0, fin=False)}>
      <div class="abs lbl" style="left:90px;top:380px;color:var(--racket);{at(.05,'fade')}">TIER LIST · TÊNIS</div>
      <div class="abs t" style="left:90px;top:450px;width:900px;font-size:118px;{at(.1,'rise', .6)}">As desculpas depois de perder o jogo.</div>
    </div>'''
    s2 = f'''<div {tl.scene(3.0, 9.6)}>
      <div class="abs t" style="left:90px;top:330px;width:900px;font-size:60px">Desculpas depois de perder:</div>
      <div class="abs" style="left:90px;top:440px;width:900px">{board(3.3)}</div>
    </div>'''
    s3 = f'''<div {tl.scene(9.6, 13.4)}>
      <div class="abs t" style="left:90px;top:330px;width:900px;font-size:60px">Só uma dá pra resolver:</div>
      <div class="abs" style="left:90px;top:440px;width:900px">{board(None, True)}</div>
      <div class="abs t" style="left:90px;top:1460px;width:900px;font-size:58px;color:var(--racket);{at(11.4,'rise',.5)}">Raquete errada também perde jogo.</div>
    </div>'''
    s4 = f'''<div {tl.scene(13.4, T, fout=False)}>
      <div class="abs t" style="left:90px;top:440px;width:900px;font-size:84px;{at(13.45,'rise',.5)}">O RACKET DNA cruza o seu jogo com <span style="color:var(--racket)">62 raquetes.</span></div>
      <div class="abs" style="left:90px;top:860px;{at(14.4,'fade',.6)}">{logo('racketdna-logo-fundo-escuro', 760)}</div>
      <div class="abs m" style="left:90px;top:1040px;font-size:36px;{at(15.0,'fade')}">Teste grátis e sem cadastro · sportdna.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs lbl" style="left:80px;top:90px;color:var(--racket)">TIER LIST · TÊNIS</div>
      <div class="abs t" style="left:80px;top:150px;width:920px;font-size:96px">As desculpas depois de perder o jogo.</div>
      <div class="abs" style="left:80px;top:470px;width:920px">{board(None, True, 160, 40)}</div></div>'''
    piece(id='D-R8', fmt='reel', day=1, slot='19h45', title='Meme tier list: as desculpas depois de perder', total=T, poster=.62, kind='meme',
          html=doc('D-R8', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--ink)'),
          caption=('Tier list: as desculpas depois de perder o jogo. 🎾\n\n'
                   'D: o adversário só devolve.\nC: a bola tava nova.\nB: o sol na cara.\nA: o vento.\nS: …a raquete. A única que dá pra resolver.\n\n'
                   'Marca o parceiro de quadra que usa todas 👇\n'
                   'O RACKET DNA cruza o seu jogo com 62 raquetes. Teste grátis, link na bio.\n#racketdna #sportdna #tenis #tierlist #meme #tenisamador'),
          notes='Meme no formato tier list (identidade + marcação do parceiro de quadra). Ironia com o produto no fim, sem desenho de raquete. 62 raquetes: número do site. Áudio em alta no app.')

# =====================================================================================
# D-C7 · Carrossel · RUN: a tabela de pace para salvar (ter 24/11, claro)
# =====================================================================================
PACES = [('5:00', '25min', '50min', '1h45'), ('5:30', '27min30', '55min', '1h56'), ('6:00', '30min', '1h00', '2h07'), ('6:30', '32min30', '1h05', '2h17'), ('7:00', '35min', '1h10', '2h28')]

def d_c7():
    def band(hl=None, dark=False, fs=50, pad=22):
        bg, fg, ln = ('#1A1A1A', '#fff', 'var(--line)') if dark else ('#fff', 'var(--ink)', 'var(--lineL)')
        head = ''.join(f'<div class="lbl" style="font-size:24px;color:{"var(--muted)" if dark else "var(--mutedL)"}">{h}</div>' for h in ('PACE /KM', '5 KM', '10 KM', '21 KM'))
        rows = ''.join(f'''<div style="display:contents">{''.join(f'<div class="{"n" if j == 0 else "t"}" style="font-size:{fs + 6 if j == 0 else fs - 6}px;padding:{pad}px 0;border-top:3px solid {ln};{"color:var(--run)" if (hl is not None and i == hl) or j == 0 else ""};{"background:rgba(255,138,61,.12)" if hl is not None and i == hl else ""}">{v}</div>' for j, v in enumerate(r))}</div>''' for i, r in enumerate(PACES))
        return (f'<div style="background:{bg};color:{fg};border-radius:36px;padding:34px 40px;box-shadow:0 30px 60px rgba(0,0,0,.18)">'
                f'<div style="display:grid;grid-template-columns:1.15fr 1.15fr 1fr 1fr;column-gap:18px;align-items:center">{head}{rows}</div></div>')
    pages = [page(f'''
      <div class="abs lbl" style="left:80px;top:90px">RUN DNA · PARA SALVAR</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:120px">A tabela de pace que todo corredor <span style="color:var(--run)">precisa.</span></div>
      <div class="abs" style="left:80px;top:640px;width:920px;transform:rotate(-2deg)">{band(2)}</div>''', cls='light')]
    pages.append(page(f'''
      <div class="abs lbl" style="left:80px;top:90px">COMO LER</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:96px">Pace é quanto tempo você leva em 1 km.</div>
      <div class="abs n" style="left:70px;top:500px;font-size:230px;color:var(--run)">6:00</div>
      <div class="abs t" style="left:80px;top:760px;font-size:64px">= 6 minutos por quilômetro.</div>
      <div class="abs" style="left:80px;top:900px;width:880px;font-size:50px;line-height:1.3;color:var(--mutedL)">Quanto menor o número, mais rápido você corre.</div>''', cls='light'))
    pages.append(page(f'''
      <div class="abs lbl" style="left:80px;top:90px">A TABELA · TEMPO TOTAL</div>
      <div class="abs" style="left:80px;top:170px;width:920px">{band(None, True, 64, 40)}</div>
      <div class="abs" style="left:80px;top:1180px;width:900px;font-size:36px;color:var(--muted)">21 km = meia maratona (21,1 km), arredondado no minuto.</div>'''))
    pages.append(page(f'''
      <div class="abs lbl" style="left:80px;top:90px">A CONTA DE CABEÇA</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:96px">Pace × distância = tempo de prova.</div>
      <div class="abs" style="left:80px;top:540px;width:920px;background:#fff;border-radius:36px;padding:44px 48px;transform:rotate(1.5deg);box-shadow:0 30px 60px rgba(0,0,0,.14)">
        <div class="m" style="font-size:52px;line-height:1.6">6:30 × 10 km<br>= 65 min<br><span style="color:var(--run)">= 1h05</span></div></div>
      <div class="abs" style="left:80px;top:1050px;width:880px;font-size:46px;line-height:1.3;color:var(--mutedL)">Na prova, sai um pouco mais leve que o pace-alvo e guarda perna pro fim.</div>''', cls='light'))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--run)"></div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:104px;color:var(--ink)">O pace é seu. O tênis também devia ser.</div>
      <div class="abs" style="left:80px;top:600px;width:860px;font-size:48px;line-height:1.3;color:var(--ink)">O RUN DNA compara 212 tênis com o seu corpo, o seu ritmo e as suas dores.</div>
      <div class="abs" style="left:80px;top:880px;font-size:44px;color:var(--ink);font-weight:700">Salva e manda pro grupo da corrida.</div>
      <div class="abs" style="left:80px;top:1080px">{logo('rundna-logo-preto', 560)}</div>
      <div class="abs m" style="left:80px;top:1230px;font-size:32px;color:var(--ink)">Teste grátis · sportdna.com.br</div>'''))
    piece(id='D-C7', fmt='carrossel', day=2, slot='12h30', title='RUN: a tabela de pace para salvar', kind='engajamento', w=1080, h=1350,
          html=doc('D-C7', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('A tabela de pace que todo corredor precisa. ⏱️\n\n'
                   'Pace 5:00 → 5 km em 25min · 10 km em 50min · 21 km em 1h45\n'
                   'Pace 5:30 → 27min30 · 55min · 1h56\n'
                   'Pace 6:00 → 30min · 1h00 · 2h07\n'
                   'Pace 6:30 → 32min30 · 1h05 · 2h17\n'
                   'Pace 7:00 → 35min · 1h10 · 2h28\n\n'
                   'Salva pra próxima prova e manda pro grupo da corrida 👇\n'
                   'O RUN DNA compara 212 tênis com o seu corpo e o seu ritmo. Teste grátis, link na bio.\n#rundna #sportdna #corrida #pace #corridaderua #meiamaratona'),
          notes='Utilidade (salvar e mandar no grupo de corrida). Contas conferidas por script: tempo = pace × distância; meia maratona 21,0975 km arredondada no minuto. Objeto concreto: "pace band" de prova. 212 tênis: número do site.')

# =====================================================================================
# D-R9 · Reel trend · SURF: ligar/desligar, "modo prancha certa" (qua 25/11, azul surf)
# =====================================================================================
def d_r9():
    T = 17.0
    tl = TL(T)
    def toggle(label, on_t=None, off_t=None, on=False, fs=54):
        if on_t is not None:
            tr, kn = f'animation:trackOn .25s linear {on_t:.2f}s 1 both', f'animation:knobOn .25s cubic-bezier(.2,.75,.15,1) {on_t:.2f}s 1 both'
        elif off_t is not None:
            tr, kn = f'animation:trackOff .25s linear {off_t:.2f}s 1 both', f'animation:knobOff .25s cubic-bezier(.2,.75,.15,1) {off_t:.2f}s 1 both'
        else:
            tr, kn = (f'background:{"var(--surf)" if on else "#3A3A38"}', f'transform:translateX({96 if on else 0}px)')
        return (f'<div style="display:flex;align-items:center;justify-content:space-between;padding:30px 0;border-top:2px solid var(--line)">'
                f'<span class="t" style="font-size:{fs}px">{label}</span>'
                f'<span style="position:relative;width:184px;height:88px;border-radius:44px;{tr}"><span style="position:absolute;left:8px;top:8px;width:72px;height:72px;border-radius:50%;background:#fff;{kn}"></span></span></div>')
    s1 = f'''<div {tl.scene(0, 4.2, fin=False)}>
      <div class="abs lbl" style="left:90px;top:330px;color:var(--surf)">SURF DNA · CONFIGURAÇÕES</div>
      <div class="abs t" style="left:90px;top:400px;width:900px;font-size:96px;{at(.05,'rise',.5)}">Escolhendo prancha nova.</div>
      <div class="abs t" style="left:90px;top:1140px;width:900px;font-size:58px;color:var(--muted);{at(1.6,'fade')}">Desliga isso.</div>
      <div class="abs" style="left:90px;top:700px;width:900px">{toggle('Modo "pela foto"', off_t=2.3)}{toggle('Modo "a do amigo"', off_t=2.9)}</div>
    </div>'''
    s2 = f'''<div {tl.scene(4.2, 11.0)}>
      <div class="abs lbl" style="left:90px;top:330px;color:var(--surf)">LIGA ISSO</div>
      <div class="abs" style="left:90px;top:420px;width:580px">{toggle('Seu peso', on_t=5.0, fs=60)}{toggle('Seu nível', on_t=6.4, fs=60)}{toggle('Seu mar', on_t=7.8, fs=60)}{toggle('Sua prancha', on_t=9.2, fs=60)}</div>
      <div class="abs" style="left:730px;top:400px;{at(4.4,'fade',.6)}">{svg_prancha('var(--surf)', '#fff', 280)}</div>
      <div class="abs" style="left:90px;top:1240px;width:900px;font-size:46px;line-height:1.3;color:var(--muted);{at(10.0,'fade')}">É isso que decide a prancha.</div>
    </div>'''
    s3 = f'''<div {tl.scene(11.0, 14.0, fade=.1)}>
      <div class="abs" style="inset:0;background:var(--surf)"></div>
      <div class="abs t" style="left:90px;top:420px;width:620px;font-size:118px;color:var(--ink);{at(11.05,'rise',.5)}">Modo prancha certa: ativado.</div>
      <div class="abs" style="left:700px;top:380px;{at(11.4,'pop',.5)}">{svg_prancha('var(--ink)', 'var(--ink)', 300, fill='rgba(255,255,255,.45)')}</div>
      <div class="abs" style="left:90px;top:1060px;width:560px;font-size:44px;line-height:1.3;color:var(--ink);{at(12.0,'fade')}">13 tipos de prancha, cruzados com o seu jeito.</div>
    </div>'''
    s4 = f'''<div {tl.scene(14.0, T, fout=False)}>
      <div class="abs" style="left:90px;top:600px;{at(14.05,'fade',.6)}">{logo('surfdna-logo-fundo-escuro', 820)}</div>
      {cta_final(14.5)}
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:var(--surf);color:var(--ink)">
      <div class="abs lbl" style="left:80px;top:100px;color:var(--ink)">SURF DNA</div>
      <div class="abs t" style="left:80px;top:170px;width:600px;font-size:120px">Modo prancha certa: ativado.</div>
      <div class="abs" style="left:700px;top:130px">{svg_prancha('var(--ink)', 'var(--ink)', 300, fill='rgba(255,255,255,.45)')}</div>
      <div class="abs" style="left:80px;top:800px;width:560px;background:var(--ink);color:#fff;border-radius:30px;padding:10px 34px">{toggle('Seu peso', on=True)}{toggle('Seu nível', on=True)}{toggle('Seu mar', on=True)}</div></div>'''
    piece(id='D-R9', fmt='reel', day=3, slot='19h45', title='Trend ligar/desligar: modo prancha certa', total=T, poster=.45, kind='trend',
          html=doc('D-R9', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--surf)'),
          caption=('Modo prancha certa: ativado. 🌊\n\n'
                   'Desliga: "pela foto" e "a do amigo".\n'
                   'Liga: seu peso, seu nível, seu mar e a prancha que você tem hoje.\n\n'
                   'O SURF DNA cruza tudo isso com 13 tipos de prancha.\n'
                   'Manda pro amigo que vai trocar de prancha 👇\nTeste grátis e sem cadastro. Link na bio.\n#surfdna #sportdna #surf #pranchadesurf #surfbrasil #trend'),
          notes='Trend "ligar/desligar" (doc de trends do DOT, 06/11; circulação no Brasil sem validação). Interface de chaves desenhada pela marca, sem copiar app de terceiros. Prancha em desenho técnico de linha, sem marca. 13 tipos: número do site. Áudio em alta no app.')

# =====================================================================================
# D-C8 · Carrossel · RACKET: a corda, a peça que você esquece (qui 26/11, preto)
# =====================================================================================
def d_c8():
    cal = ''.join(f'<div style="height:96px;border-radius:16px;display:flex;align-items:center;justify-content:center;font:700 30px \'JetBrains Mono\';{"background:var(--racket);color:var(--ink)" if m in ("JAN", "MAI", "SET") else "background:#1A1A1A;color:var(--muted)"}">{m}</div>' for m in ('JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'))
    pages = [page(f'''
      <div class="abs lbl" style="left:80px;top:90px;color:var(--racket)">RACKET DNA · MANUTENÇÃO</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:126px">A peça da raquete que você esquece: <span style="color:var(--racket)">a corda.</span></div>
      <div class="abs" style="left:300px;top:760px">{svg_mostrador('var(--racket)', '#fff', 30, 520)}</div>''')]
    pages.append(page(f'''
      <div class="abs n" style="left:70px;top:90px;font-size:200px;color:var(--racket)">01</div>
      <div class="abs t" style="left:80px;top:360px;width:920px;font-size:96px">A corda perde tensão até parada no armário.</div>
      <div class="abs" style="left:80px;top:820px;width:860px;font-size:50px;line-height:1.3;color:var(--mutedL)">Ela não precisa arrebentar para estar vencida.</div>''', cls='light'))
    pages.append(page(f'''
      <div class="abs n" style="left:70px;top:90px;font-size:200px;color:var(--racket)">02</div>
      <div class="abs t" style="left:80px;top:340px;width:920px;font-size:80px">Regra de bolso: troque, por ano, as vezes que você joga por semana.</div>
      <div class="abs" style="left:80px;top:720px;width:920px;display:grid;grid-template-columns:repeat(6,1fr);gap:14px">{cal}</div>
      <div class="abs" style="left:80px;top:1000px;width:880px;font-size:46px;line-height:1.3;color:var(--muted)">Joga 3 vezes por semana? 3 trocas por ano.</div>'''))
    pages.append(page(f'''
      <div class="abs n" style="left:70px;top:90px;font-size:200px;color:var(--ink)">03</div>
      <div class="abs t" style="left:80px;top:360px;width:920px;font-size:88px">Tensão mais baixa: mais potência. Mais alta: mais controle.</div>
      <div class="abs" style="left:280px;top:820px">{svg_mostrador('var(--ink)', 'var(--ink)', -20, 520)}</div>''', cls='light'))
    pages.append(page(f'''
      <div class="abs n" style="left:70px;top:90px;font-size:200px;color:var(--racket)">04</div>
      <div class="abs t" style="left:80px;top:360px;width:920px;font-size:90px">Sinais de que já passou da hora:</div>
      <div class="abs" style="left:80px;top:640px;width:920px">
        <div style="padding:30px 0;border-top:2px solid var(--line);font-size:52px;font-family:Archivo;font-weight:800">As cordas saem do lugar e não voltam.</div>
        <div style="padding:30px 0;border-top:2px solid var(--line);font-size:52px;font-family:Archivo;font-weight:800">A bola começa a sair longa sem você mudar o golpe.</div></div>'''))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--racket)"></div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:104px;color:var(--ink)">Corda nova em raquete errada não resolve.</div>
      <div class="abs" style="left:80px;top:600px;width:860px;font-size:48px;line-height:1.3;color:var(--ink)">O RACKET DNA cruza o seu braço, o seu jogo e o seu nível com 62 raquetes.</div>
      <div class="abs" style="left:80px;top:880px;font-size:44px;color:var(--ink);font-weight:700">Manda pro parceiro que joga com a corda de 2024.</div>
      <div class="abs" style="left:80px;top:1080px">{logo('racketdna-logo-preto', 600)}</div>
      <div class="abs m" style="left:80px;top:1230px;font-size:32px;color:var(--ink)">Teste grátis · sportdna.com.br</div>'''))
    piece(id='D-C8', fmt='carrossel', day=4, slot='12h30', title='RACKET: a corda, a peça que você esquece', kind='engajamento', w=1080, h=1350,
          html=doc('D-C8', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('A peça da raquete que você esquece: a corda. 🎾\n\n'
                   '01 Ela perde tensão até parada no armário.\n'
                   '02 Regra de bolso: troque, por ano, as vezes que você joga por semana.\n'
                   '03 Tensão mais baixa dá mais potência; mais alta, mais controle.\n'
                   '04 Corda que sai do lugar e bola saindo longa são sinais de troca.\n\n'
                   'Manda pro parceiro que joga com a corda de 2024 👇\n'
                   'O RACKET DNA cruza o seu jogo com 62 raquetes. Teste grátis, link na bio.\n#racketdna #sportdna #tenis #encordoamento #raquete #tenisamador'),
          notes='Utilidade de manutenção (salvar e marcar o parceiro). Regra de bolso de troca e efeito da tensão são orientações gerais do tênis, sem marca. Sem desenho de raquete: mostrador e calendário como objetos. 62 raquetes: número do site.')

# =====================================================================================
# D-R10 · Reel trend · RUN: antes × depois da escolha do tênis (sex 27/11, laranja)
# =====================================================================================
def d_r10():
    T = 17.0
    tl = TL(T)
    antes = ['pela cor', 'porque o amigo usa', 'pelo maior desconto']
    depois = ['pelo seu peso', 'pela sua pisada', 'pelo seu ritmo']
    def col(titulo, itens, cor, t0, strike=False, bg='#1A1A1A', fg='#fff'):
        li = ''.join(f'''<div style="position:relative;padding:36px 0;border-top:2px solid {'var(--line)' if bg == '#1A1A1A' else 'rgba(0,0,0,.15)'};font:800 64px/1.15 Archivo;{at(t0 + .3 + i*.7, 'rise', .4)}">{x}
            {f'<div style="position:absolute;left:0;right:20px;top:52%;height:8px;background:var(--run);transform-origin:left;animation:strike .35s ease-out {t0 + 2.6 + i*.25:.2f}s 1 both"></div>' if strike else ''}</div>''' for i, x in enumerate(itens))
        return f'<div style="background:{bg};color:{fg};border-radius:36px;padding:34px 40px"><div class="lbl" style="color:{cor}">{titulo}</div><div style="margin-top:14px">{li}</div></div>'
    s1 = f'''<div {tl.scene(0, 6.6, fin=False)}>
      <div class="abs t" style="left:90px;top:300px;width:900px;font-size:92px;{at(.05,'rise',.5)}">Escolhendo tênis de corrida.</div>
      <div class="abs t" style="left:90px;top:500px;font-size:150px;color:var(--muted);{at(.6,'pop',.4)}">ANTES</div>
      <div class="abs" style="left:90px;top:720px;width:900px">{col('ESCOLHI', antes, 'var(--muted)', .9, True)}</div>
    </div>'''
    s2 = f'''<div {tl.scene(6.6, 12.4)}>
      <div class="abs" style="inset:0;background:var(--run)"></div>
      <div class="abs t" style="left:90px;top:300px;width:900px;font-size:92px;color:var(--ink);{at(6.65,'rise',.5)}">Escolhendo tênis de corrida.</div>
      <div class="abs t" style="left:90px;top:500px;font-size:150px;color:var(--ink);{at(7.0,'pop',.4)}">DEPOIS</div>
      <div class="abs" style="left:90px;top:720px;width:900px">{col('ESCOLHI', depois, 'var(--ink)', 7.3, False, '#fff', 'var(--ink)')}</div>
    </div>'''
    s3 = f'''<div {tl.scene(12.4, T, fout=False)}>
      <div class="abs t" style="left:90px;top:400px;width:900px;font-size:88px;{at(12.45,'rise',.5)}">O RUN DNA compara <span style="color:var(--run)">212 tênis</span> com o seu jeito de correr.</div>
      <div class="abs" style="left:90px;top:860px;{at(13.4,'fade',.6)}">{logo('rundna-logo-fundo-escuro', 760)}</div>
      <div class="abs m" style="left:90px;top:1040px;font-size:36px;{at(14.0,'fade')}">Teste grátis · relatório R$ 9,99 · sportdna.com.br</div>
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}</section>'
    def col_static(titulo, itens, strike, bg, fg, cor):
        li = ''.join(f'<div style="position:relative;padding:20px 0;border-top:2px solid {"var(--line)" if bg == "#1A1A1A" else "rgba(0,0,0,.15)"};font:800 34px/1.15 Archivo;white-space:nowrap">{x}{"<div style=\"position:absolute;left:0;right:10px;top:52%;height:7px;background:var(--run)\"></div>" if strike else ""}</div>' for x in itens)
        return f'<div style="flex:1;background:{bg};color:{fg};border-radius:30px;padding:28px 30px"><div class="lbl" style="color:{cor}">{titulo}</div><div style="margin-top:10px">{li}</div></div>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px;background:var(--run);color:var(--ink)">
      <div class="abs lbl" style="left:80px;top:100px;color:var(--ink)">RUN DNA</div>
      <div class="abs t" style="left:80px;top:170px;width:920px;font-size:112px">Tênis de corrida: antes × depois.</div>
      <div class="abs" style="left:80px;top:640px;width:920px;display:flex;gap:24px">{col_static('ANTES', antes, True, '#1A1A1A', '#fff', 'var(--muted)')}{col_static('DEPOIS', depois, False, '#fff', 'var(--ink)', 'var(--ink)')}</div></div>'''
    piece(id='D-R10', fmt='reel', day=5, slot='19h45', title='Trend antes × depois: como escolher o tênis', total=T, poster=.55, kind='trend',
          html=doc('D-R10', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--run)'),
          caption=('Escolhendo tênis de corrida: antes × depois. 👟\n\n'
                   'Antes: pela cor, porque o amigo usa, pelo maior desconto.\n'
                   'Depois: pelo seu peso, pela sua pisada, pelo seu ritmo.\n\n'
                   'O RUN DNA compara 212 tênis com o seu jeito de correr.\n'
                   'Manda pro amigo que escolhe tênis pela cor 👇\nTeste grátis, relatório R$ 9,99. Link na bio.\n#rundna #sportdna #corrida #tenisdecorrida #antesedepois #trend'),
          notes='Trend "antes/depois" (doc de trends do DOT, 06/11: compra por aparência × escolha pelo próprio jeito). Sem promessa de desempenho. Cai na sexta da Black Friday, mas sem falar de desconto (o S02 já fez). Preço e 212 tênis do site. Áudio em alta no app.')

# =====================================================================================
# D-C9 · Carrossel · SURF: checklist da trip no bloco de notas (sáb 28/11, claro)
# =====================================================================================
def d_c9():
    itens = [('Parafina', 'e o pente para raspar a velha.'), ('Leash', 'confere se a cordinha não está ressecada.'), ('Quilhas e a chave', 'a chave some primeiro.'),
             ('Protetor solar', 'rosto, orelha e nuca.'), ('Roupa para a água', 'lycra ou roupa de borracha, conforme a temperatura.'), ('Capa da prancha', 'sol no carro também amassa.'),
             ('Previsão das ondas', 'tamanho, vento e maré, na véspera.')]
    def nota(lst, marcados, titulo='trip de surf ✔', y0=0, big=False):
        rows = ''.join(f'''<div style="display:flex;gap:22px;align-items:flex-start;padding:{34 if big else 20}px 0;border-bottom:2px solid #EFE7C8">
            <span style="flex:none;width:44px;height:44px;margin-top:4px;border:4px solid #B9A66A;border-radius:12px;display:flex;align-items:center;justify-content:center;{"background:#0A0A0A;border-color:#0A0A0A" if i in marcados else ""}">{"<svg width=\"26\" height=\"26\" viewBox=\"0 0 26 26\"><path d=\"M4 13 L11 20 L22 6\" stroke=\"#6CCFF6\" stroke-width=\"5\" fill=\"none\"/></svg>" if i in marcados else ""}</span>
            <span><span style="font:800 {58 if big else 44}px/1.15 Archivo;color:#2B2B28">{a}</span><br><span style="font:500 {40 if big else 32}px/1.3 'DM Sans';color:#8C8572">{b}</span></span></div>''' for i, (a, b) in lst)
        return f'''<div style="background:#FFFBEA;border-radius:34px;padding:40px 46px;box-shadow:0 30px 60px rgba(0,0,0,.16)">
          <div style="font:700 28px 'DM Sans';color:#B08A1E">‹ Notas</div><div style="font:800 64px/1.1 Archivo;color:#2B2B28;margin-top:16px">{titulo}</div>{rows}</div>'''
    E = list(enumerate(itens))
    pages = [page(f'''
      <div class="abs lbl" style="left:80px;top:90px">SURF DNA · PARA SALVAR</div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:120px">Checklist da trip de <span style="color:var(--petrol)">surf.</span></div>
      <div class="abs" style="left:150px;top:560px;width:780px;transform:rotate(-3deg)">{nota(E[:3], {0})}</div>''', cls='light')]
    pages.append(page(f'''<div class="abs" style="left:80px;top:90px;width:920px">{nota(E[:4], {0, 1, 2, 3}, 'o básico', big=True)}</div>''', cls='light'))
    pages.append(page(f'''<div class="abs" style="left:80px;top:90px;width:920px">{nota(E[4:], {4, 5, 6}, 'o que todo mundo esquece', big=True)}</div>''', cls='light'))
    pages.append(page(f'''
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:104px">Faltou um item: a prancha certa pro seu <span style="color:var(--surf)">nível.</span></div>
      <div class="abs" style="left:700px;top:560px;transform:rotate(12deg)">{svg_prancha('var(--surf)', '#fff', 240)}</div>
      <div class="abs" style="left:80px;top:640px;width:560px;font-size:46px;line-height:1.3;color:var(--muted)">O SURF DNA cruza o seu peso, o seu nível e o seu mar com 13 tipos de prancha.</div>'''))
    pages.append(page(f'''
      <div class="abs" style="inset:0;background:var(--surf)"></div>
      <div class="abs t" style="left:80px;top:160px;width:920px;font-size:110px;color:var(--ink)">Salva e manda no grupo da trip.</div>
      <div class="abs" style="left:80px;top:560px;width:860px;font-size:48px;line-height:1.3;color:var(--ink)">Quem esquecer a chave das quilhas paga o açaí.</div>
      <div class="abs" style="left:80px;top:1080px">{logo('surfdna-logo-preto', 560)}</div>
      <div class="abs m" style="left:80px;top:1230px;font-size:32px;color:var(--ink)">Teste grátis · sportdna.com.br</div>'''))
    piece(id='D-C9', fmt='carrossel', day=6, slot='12h30', title='SURF: checklist da trip no bloco de notas', kind='engajamento', w=1080, h=1350,
          html=doc('D-C9', FONTS, CSS, ''.join(pages), 1080, 1350),
          caption=('Checklist da trip de surf. 🏄\n\n'
                   '✔ Parafina (e o pente)\n✔ Leash sem ressecar\n✔ Quilhas e a chave\n✔ Protetor solar\n✔ Lycra ou roupa de borracha\n✔ Capa da prancha\n✔ Previsão das ondas na véspera\n\n'
                   'Salva e manda no grupo da trip. Quem esquecer a chave das quilhas paga o açaí 👇\n'
                   'Faltou a prancha certa? O SURF DNA cruza seu peso, nível e mar com 13 tipos. Teste grátis, link na bio.\n#surfdna #sportdna #surf #surftrip #checklist #surfbrasil'),
          notes='Utilidade em bloco de notas (objeto concreto) para salvar e mandar no grupo da trip. Itens gerais, sem marca. 13 tipos: número do site. Capa off-white entre o laranja de sexta e o preto de domingo.')

# =====================================================================================
# D-R11 · Reel meme · RUN: "alguém indica um tênis?" no grupo da corrida (dom 29/11, preto)
# =====================================================================================
def d_r11():
    T = 19.0
    tl = TL(T)
    msgs = [('Lia', 'o meu é ótimo, compra igual', '07:02'), ('Rafa', 'compra o mais caro que dura mais', '07:03'), ('Bia', 'o que tiver em promoção kkk', '07:03'),
            ('Téo', 'corre descalço, é o natural', '07:04'), ('Gu', 'uso o mesmo há 4 anos, nunca troquei', '07:05'), ('Duda', 'depende', '07:06')]
    def chat(t0=None, n=None):
        n = len(msgs) if n is None else n
        b = C.bubble('gente, qual tênis eu compro pra começar a correr?', me=True, hora='07:01', fs=31)
        for i, (nome, txt, h) in enumerate(msgs[:n]):
            st = at(t0 + i * 1.05, 'rise', .3) if t0 is not None else ''
            b += f'<div style="{st}">{C.bubble(txt, nome=nome, hora=h, fs=31)}</div>'
        head = (f'<div style="height:110px;background:#1F2C2A;color:#fff;display:flex;align-items:center;gap:20px;padding:0 26px">'
                f'<span style="width:70px;height:70px;border-radius:50%;background:var(--run);display:flex;align-items:center;justify-content:center;font:800 30px Archivo;color:var(--ink)">CD</span>'
                f'<span><span style="font:700 34px \'DM Sans\'">Corrida de domingo</span><br><span style="font:400 24px \'DM Sans\';opacity:.7">Lia, Rafa, Bia, Téo, Gu, Duda, você</span></span></div>')
        return C.phone(f'{head}<div style="background:#ECE5DD;position:absolute;left:0;right:0;top:110px;bottom:0;padding-top:16px">{b}</div>', 760, 1300, screen='#ECE5DD', frame='#111', status_color='#fff', hora='07:06')
    s1 = f'''<div {tl.scene(0, 9.6, fin=False)}>
      <div class="abs" style="left:160px;top:270px;{at(.05,'rise',.5)}">{chat(1.0)}</div>
    </div>'''
    s2 = f'''<div {tl.scene(9.6, 13.0, fade=.1)}>
      <div class="abs n" style="left:80px;top:430px;font-size:300px;color:var(--run);{at(9.65,'pop',.4)}">6</div>
      <div class="abs t" style="left:90px;top:760px;width:900px;font-size:110px;{at(10.0,'rise',.5)}">respostas.</div>
      <div class="abs t" style="left:90px;top:900px;width:900px;font-size:110px;color:var(--muted);{at(10.8,'rise',.5)}">Nenhuma sobre você.</div>
    </div>'''
    s3 = f'''<div {tl.scene(13.0, 16.2)}>
      <div class="abs t" style="left:90px;top:420px;width:900px;font-size:88px;{at(13.05,'rise',.5)}">Seu peso. Sua pisada. Seu ritmo. Suas dores.</div>
      <div class="abs" style="left:90px;top:860px;width:880px;font-size:50px;line-height:1.3;color:var(--muted);{at(14.0,'fade',.5)}">O RUN DNA compara 212 tênis com isso tudo.</div>
    </div>'''
    s4 = f'''<div {tl.scene(16.2, T, fout=False)}>
      <div class="abs" style="left:90px;top:620px;{at(16.25,'fade',.6)}">{logo('rundna-logo-fundo-escuro', 800)}</div>
      {cta_final(16.7)}
    </div>'''
    body = f'<section class="page" style="width:1080px;height:1920px">{s1}{s2}{s3}{s4}</section>'
    cover_body = f'''<div class="page" style="width:1080px;height:1350px">
      <div class="abs t" style="left:80px;top:110px;width:420px;font-size:84px">"Alguém indica um tênis?"</div>
      <div class="abs t" style="left:80px;top:640px;width:400px;font-size:64px;color:var(--run)">6 respostas. Nenhuma sobre você.</div>
      <div class="abs" style="left:520px;top:60px;transform:scale(.72);transform-origin:top left">{chat()}</div></div>'''
    piece(id='D-R11', fmt='reel', day=7, slot='19h45', title='Meme: "alguém indica um tênis?" no grupo da corrida', total=T, poster=.4, kind='meme',
          html=doc('D-R11', FONTS, CSS + tl.style(), body, 1080, 1920, reel=True, total=T),
          cover=cover_from_feed(cover_body, 'var(--ink)'),
          caption=('"Gente, qual tênis eu compro pra começar a correr?" 🏃\n\n'
                   '"O meu é ótimo." "Compra o mais caro." "O que tiver em promoção." "Corre descalço." "Uso o mesmo há 4 anos." "Depende."\n'
                   '6 respostas. Nenhuma sobre você.\n\n'
                   'Manda no grupo da corrida e vê quem se reconhece 👇\n'
                   'O RUN DNA compara 212 tênis com o seu peso, pisada, ritmo e dores. Teste grátis, link na bio.\n#rundna #sportdna #corrida #corridaderua #meme #grupodecorrida'),
          notes='Meme de comportamento de grupo (identidade: todo grupo de corrida tem essas respostas). Conversa num celular genérico, sem marca de app, nomes fictícios. 212 tênis: número do site. Áudio em alta no app.')

# =====================================================================================
# Stories · Dicionário DNA com desenho técnico (sem adesivo)
# =====================================================================================
TERMOS3 = [
    (1, 'RUN', 'Drop', 'A diferença de altura entre o calcanhar e a ponta do tênis. 32 mm atrás e 24 mm na frente: drop de 8 mm.', 'var(--run)', 'rundna', 'drop', False),
    (2, 'RACKET', 'Rigidez', 'O quanto a raquete dobra na batida. Mais rígida: mais potência e mais vibração no braço.', 'var(--racket)', 'racketdna', 'rigidez', True),
    (3, 'SURF', 'Borda', 'A lateral da prancha. Mais redonda perdoa mais; mais fina corta melhor a onda.', 'var(--surf)', 'surfdna', 'borda', False),
    (4, 'RACKET', 'Cabo', 'A grossura da empunhadura, de L1 a L4. Cabo errado cansa a mão.', 'var(--racket)', 'racketdna', 'cabo', True),
    (5, 'RUN', 'Entressola', 'A espuma entre o cabedal e a sola. É onde mora o amortecimento.', 'var(--run)', 'rundna', 'entressola', False),
    (6, 'SURF', 'Deck', 'A parte de cima da prancha, onde vai a parafina e onde você fica de pé.', 'var(--surf)', 'surfdna', 'deck', True),
    (7, 'RACKET', 'Overgrip', 'A fita fina por cima do cabo. Segura o suor e é barata de trocar.', 'var(--racket)', 'racketdna', 'overgrip', False),
]

TIPO_SO = {'drop', 'entressola', 'deck', 'overgrip'}  # S03 rodada 1: Gui reprovou as ilustrações; voltam no layout tipográfico aprovado no S02

def d_story_tipo(n, d, sp, termo, defi, cor, lg, light):
    body = f'''<section class="page {'light' if light else ''}" style="width:1080px;height:1920px">
      <div class="abs lbl" style="left:80px;top:300px">DICIONÁRIO DNA · {sp}</div>
      <div class="abs" style="left:80px;top:360px;width:920px;height:6px;background:{cor}"></div>
      <div class="abs t" style="left:80px;top:470px;width:920px;font-size:{200 if len(termo) < 8 else 170}px;{'color:' + cor if not light else ''}">{termo}</div>
      <div class="abs" style="left:80px;top:780px;width:900px;font-size:64px;line-height:1.25;font-family:Archivo;font-weight:800">{defi}</div>
      <div class="abs" style="left:80px;top:1300px;font-size:42px;{'color:var(--mutedL)' if light else 'color:var(--muted)'}">Salva e manda pro seu parceiro de treino.</div>
      <div class="abs" style="left:80px;top:1400px">{logo(lg + ('-logo-fundo-claro' if light else '-logo-fundo-escuro'), 460)}</div>
    </section>'''
    sid = f'D-S{13 + n}'
    piece(id=sid, fmt='story', day=d, title=f'Dicionário DNA: {termo}', w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
          caption='(story, sem legenda)', sticker='', kind='story',
          notes='v2 (rodada 1): sem ilustração, no layout tipográfico do Dicionário DNA aprovado no S02. Definição geral, sem marca.')

def d_stories3():
    for n, (d, sp, termo, defi, cor, lg, des, light) in enumerate(TERMOS3):
        if des in TIPO_SO:
            d_story_tipo(n, d, sp, termo, defi, cor, lg, {'drop': False, 'entressola': True, 'deck': False, 'overgrip': True}[des]); continue
        ink = '#0A0A0A' if light else '#fff'
        draw = {'drop': lambda: svg_drop(cor, ink, 900), 'rigidez': lambda: svg_rigidez('#0A0A0A' if light else cor, ink, 900),
                'borda': lambda: svg_borda(cor, ink, 900), 'cabo': lambda: svg_cabo('#0A0A0A' if light else cor, ink, 480),
                'entressola': lambda: svg_entressola(cor, ink, 900), 'deck': lambda: svg_prancha('#0A0A0A', ink, 230, fill='rgba(108,207,246,.55)'),
                'overgrip': lambda: svg_overgrip(cor, ink, 280)}[des]()
        tall = des in ('deck', 'overgrip')
        if tall:
            art = f'<div class="abs" style="left:{720 if des == "deck" else 700}px;top:{320 if des == "deck" else 520}px">{draw}</div>'
            txt_w = 600
            defi_top, defi_w = 760, 580
        elif des == 'cabo':
            art = f'<div class="abs" style="left:300px;top:560px">{draw}</div>'
            txt_w, defi_top, defi_w = 920, 1110, 920
        else:
            art = f'<div class="abs" style="left:90px;top:580px">{draw}</div>'
            txt_w, defi_top, defi_w = 920, 1110, 920
        acc = '#0A0A0A' if light else cor
        body = f'''<section class="page {'light' if light else ''}" style="width:1080px;height:1920px">
          <div class="abs grid-bg {'l' if light else ''}" style="inset:0"></div>
          {f'<div class="abs" style="inset:0;background:{cor};opacity:.9"></div>' if light and sp != 'RACKET' else ''}
          {f'<div class="abs" style="inset:0;background:var(--racket)"></div>' if light and sp == 'RACKET' else ''}
          <div class="abs lbl" style="left:80px;top:290px;{'color:#0A0A0A' if light else ''}">DICIONÁRIO DNA · {sp} · FICHA {n+1:02d}</div>
          <div class="abs t" style="left:80px;top:350px;width:{txt_w}px;font-size:{150 if len(termo) < 8 else 124}px;color:{acc}">{termo}</div>
          {art}
          <div class="abs" style="left:80px;top:{defi_top}px;width:{defi_w}px;font-size:52px;line-height:1.25;font-family:Archivo;font-weight:800;{'color:#0A0A0A' if light else ''}">{defi}</div>
          <div class="abs" style="left:80px;top:1440px;font-size:38px;{'color:#0A0A0A' if light else 'color:var(--muted)'}">Salva e manda pro seu parceiro de treino.</div>
          <div class="abs" style="right:80px;top:1500px">{logo(lg + ('-logo-preto' if light else '-logo-fundo-escuro'), 330)}</div>
        </section>'''
        sid = f'D-S{13 + n}'
        piece(id=sid, fmt='story', day=d, title=f'Dicionário DNA: {termo}', w=1080, h=1920, html=doc(sid, FONTS, CSS, body, 1080, 1920),
              caption='(story, sem legenda)', sticker='', kind='story',
              notes='Sem adesivo. Ficha do Dicionário DNA com desenho técnico de linha (objeto concreto), sem marca. Termo novo, não usado no S02. Definição geral.')


d_r8(); d_c7(); d_r9(); d_c8(); d_r10(); d_c9(); d_r11(); d_stories3()
