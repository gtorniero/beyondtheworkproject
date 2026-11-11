"""KVs SPORT DNA (RACKET e SURF) no look da referência ADC-RZ-08 / dna_ref.py: preto com grade técnica e luz na cor do esporte,
título Archivo enorme e provocativo, BIG NUMBERS do motor (Syne 800) e o celular com a tela REAL do site
(dna_capture.py + kv_dna_stills.py). Números só os que o site mostra (conferidos em 10/11/2026).

- Hero 4:5: uma função por KV (composição fina, é o que o Gui aprova).
- Adaptações (1:1, 9:16, 1,91:1, 16:9) e motions (4:5, 1:1, 9:16, 12 s, sem áudio): layout genérico a partir de SPEC.
  O motion 4:5 é o próprio hero animado (o último quadro = o hero aprovado).

Uso:
  python3 kv_dna.py hero  <telas> <saida> [IDs]          → <ID>-v<n>-feed45.png
  python3 kv_dna.py adapt <telas> <saida> [IDs]          → -sq.png -story.png -land.png -16x9.png
  python3 kv_dna.py motion <telas> <saida> [IDs]         → -motion-feed45.mp4 -motion-sq.mp4 -motion-story.mp4
  (saída em <saida>/<ID>-v<n>/)"""
import asyncio, base64, re, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import ff, svg, A
from playwright.async_api import async_playwright

SCR = None
INK, MUTED, PETROL = '#0A0A0A', '#A3A3A0', '#0E4D64'
SD = A / 'sportdna'
FONTS = ff('Archivo', 'Archivo-800.woff2', '800') + ff('Syne', 'Syne-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700') + ff('JetBrains Mono', 'JBMono-var.woff2', '400 700')
SP = {
    'racket': dict(c='#DDF247', logo='racketdna-logo-fundo-escuro.svg', cta='Descobrir minha raquete', url='sportdna.com.br/racket', fine='Você vê o diagnóstico antes de pagar.'),
    'surf': dict(c='#6CCFF6', logo='surfdna-logo-fundo-escuro.svg', cta='Descobrir minha prancha', url='sportdna.com.br/surf', fine='Prévia grátis · 3 minutos · sem cadastro.'),
}
FMT = {'feed45': (1080, 1350), 'sq': (1080, 1080), 'story': (1080, 1920), 'land': (1200, 628), '16x9': (1920, 1080)}
MOTION_T = 12.0
CTX = dict(anim=False, ni=0)  # anim: motion; ni: contador de números (ordem de entrada)


def t_num(i): return 2.0 + 1.5 * i
def t_post(): return t_num(CTX['ni'])
def t_cta(): return max(6.6, t_post() + 1.0)


def A_(kind, t, d=.8):
    if not CTX['anim']: return ''
    ease = 'cubic-bezier(.2,.8,.2,1)' if kind != 'pop' else 'cubic-bezier(.34,1.4,.64,1)'
    return f'animation:{kind} {d}s {ease} {t:.2f}s 1 both;'


def img(name):
    return 'data:image/jpeg;base64,' + base64.b64encode((SCR / name).read_bytes()).decode()


def hl(s):  # *palavra* → destaque na cor do esporte
    out, on = '', False
    for part in s.split('*'):
        out += (f'<span class="hl">{part}</span>' if on else part); on = not on
    return out


def phone(src, w, x, y, rot=(-9, 4, 2), zoom=1.0, fx=.5, fy=0.0):
    """Celular genérico com a tela real. zoom/fx/fy: aproximação na própria tela (o elemento em foco fica inteiro)."""
    b = 13; sw = w - 2 * b; sh = sw * 1919 / 1080; h = sh + 2 * b
    ry, rx, rz = rot
    inner = (f'<img src="{img(src)}" style="position:absolute;left:0;top:0;width:{sw}px;height:{sh:.0f}px;'
             f'transform-origin:{fx * 100:.0f}% {fy * 100:.0f}%;transform:scale({zoom})">')
    ph = (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;transform:perspective(2200px) rotateY({ry}deg) rotateX({rx}deg) rotateZ({rz}deg)">'
          f'<div class="ph" style="width:{w}px;height:{h:.0f}px;border-radius:{w * .11:.0f}px">'
          f'<div class="scr" style="left:{b}px;top:{b}px;right:{b}px;bottom:{b}px;border-radius:{w * .11 - b:.0f}px">{inner}</div>'
          f'<div class="gl"></div></div></div>')
    return f'<div style="position:absolute;inset:0;{A_("phin", .7, 1.1)}">{ph}</div>' if CTX['anim'] else ph


def num(n, label, x, y, w, size=150, lsize=30):
    t = t_num(CTX['ni']); CTX['ni'] += 1
    m = re.search(r'\d[\d.,]*', re.sub(r'<[^>]+>', lambda g: '\0' * len(g.group(0)), n))  # 1º número fora das tags
    if m and CTX['anim']:
        tok = n[m.start():m.end()]; dec = len(tok.split(',')[1]) if ',' in tok else 0
        to = float(tok.replace('.', '').replace(',', '.'))
        n = f'{n[:m.start()]}<span class="cv" data-to="{to}" data-dec="{dec}" data-t="{t + .15:.2f}">{tok}</span>{n[m.end():]}'
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;{A_("rise", t)}"><div class="num" style="font-size:{size}px">{n}</div>'
            f'<div class="lab" style="font-size:{lsize}px;margin-top:{size * .07:.0f}px">{label}</div></div>')


def sub(text, x, y, w, size, when='post'):
    t = 1.5 if when == 'pre' else None  # 'post' entra depois dos números (o tempo sai no frame(), via classe)
    return f'<div class="abs sub {"" if t else "post"}" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;{A_("rise", t) if t else ""}">{text}</div>'


def kick(text, x, y, size=21):
    return f'<div class="abs kick" style="left:{x}px;top:{y}px;font-size:{size}px;{A_("fade", t_num(CTX["ni"]) - .2, .6)}">{text}</div>'


def rule(x, y, w):
    return f'<div class="abs rule" style="left:{x}px;top:{y}px;width:{w}px;{A_("fade", t_num(CTX["ni"]) - .3, .6)}"></div>'


def chips(items, x, y, w, size=26):
    return (f'<div class="abs post" style="left:{x}px;top:{y}px;width:{w}px">'
            + ''.join(f'<span class="chip" style="font-size:{size}px;padding:{size * 8 / 26:.0f}px {size * 16 / 26:.0f}px">{c}</span>' for c in items) + '</div>')


SEEK = """<script>
window.fit=()=>{document.querySelectorAll('.num').forEach(n=>{const w=n.parentElement.clientWidth;let f=parseFloat(getComputedStyle(n).fontSize),i=0;while(n.scrollWidth>w&&i<60){f*=.97;n.style.fontSize=f+'px';i++}});
 document.querySelectorAll('.hd[data-maxh]').forEach(h=>{let f=parseFloat(getComputedStyle(h).fontSize),i=0;while(h.scrollHeight>+h.dataset.maxh&&i<40){f*=.96;h.style.fontSize=f+'px';i++}});document.documentElement.dataset.ok=1};
const nf=(v,d)=>d?v.toFixed(d).replace('.',','):Math.round(v).toLocaleString('pt-BR');
window.seek=t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});
 document.querySelectorAll('.cv').forEach(e=>{const p=Math.max(0,Math.min(1,(t-+e.dataset.t)/1.3)),k=1-Math.pow(1-p,3);e.textContent=nf(+e.dataset.to*k,+e.dataset.dec)})};
</script>"""

G45 = dict(pad=64, logo_y=58, logo_h=50, kick_y=74, kick=21, cta_b=58, cta=34, cta_p=(20, 30), url=24, fine=22, blob=(300, 760, 720, 820))


def frame(sp, body, title, tsize=96, ty=150, tw=940, kick='', W=1080, H=1350, g=G45, maxh=None, tx=None):
    S = SP[sp]; C = S['c']; p = g['pad']; tx = p if tx is None else tx
    css = f"""*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;overflow:hidden;background:{INK}}}
.kv{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{INK};color:#fff;font-family:'DM Sans',sans-serif}}
.abs{{position:absolute}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.05) 2px,transparent 2px);background-size:90px 90px}}
.blob{{position:absolute;border-radius:50%;filter:blur(130px)}}
.hd{{font-family:Archivo,sans-serif;font-weight:800;letter-spacing:-.035em;line-height:.98;color:#fff;text-wrap:balance}}
.hl{{color:{C}}}
.num{{display:inline-block;font-family:Syne,sans-serif;font-weight:800;letter-spacing:-.045em;line-height:.88;color:{C};white-space:nowrap}}
.lab{{font-weight:700;line-height:1.2;color:#fff}}
.sub{{font-weight:400;line-height:1.35;color:#D9D9D6}}
.kick{{font-family:'JetBrains Mono',monospace;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{MUTED};font-size:21px}}
.chip{{display:inline-block;font-weight:700;border:2px solid rgba(255,255,255,.28);border-radius:12px;font-size:26px;color:#fff;margin:0 8px 10px 0}}
.cta{{display:inline-flex;align-items:center;gap:14px;background:{C};color:{INK};border-radius:16px;padding:{g['cta_p'][0]}px {g['cta_p'][1]}px;font-weight:700;font-size:{g['cta']}px;white-space:nowrap}}
.url{{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:{g['url']}px;color:#fff;letter-spacing:.02em}}
.fine{{font-size:{g['fine']}px;color:{MUTED}}}
.ph{{position:relative;background:#1d1d1f;box-shadow:0 0 0 3px rgba(255,255,255,.28),0 0 120px {C}55,0 50px 110px rgba(0,0,0,.7)}}
.ph .scr{{position:absolute;overflow:hidden;background:#fff}}
.ph .gl{{position:absolute;inset:0;border-radius:inherit;background:linear-gradient(125deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,0) 26%);pointer-events:none}}
.rule{{position:absolute;height:2px;background:rgba(255,255,255,.18)}}
"""
    if CTX['anim']:
        css += ("@keyframes rise{0%{opacity:0;transform:translateY(46px)}100%{opacity:1;transform:none}}@keyframes fade{0%{opacity:0}100%{opacity:1}}"
                "@keyframes pop{0%{opacity:0;transform:scale(.7)}100%{opacity:1;transform:none}}"
                "@keyframes phin{0%{opacity:0;transform:translateX(200px) rotate(5deg)}100%{opacity:1;transform:none}}"
                "@keyframes d1{0%,100%{transform:translate(0,0)}50%{transform:translate(150px,110px)}}@keyframes d2{0%,100%{transform:translate(0,0)}50%{transform:translate(-140px,-120px)}}"
                f".post{{{A_('rise', t_post())}}}")
    b1, s1, b2, s2 = g['blob']
    top = (f'<div class="abs" style="left:{p}px;top:{g["logo_y"]}px;height:{g["logo_h"]}px;{A_("fade", 0, .6)}">{svg(SD / S["logo"], h=g["logo_h"])}</div>'
           + (f'<div class="abs kick" style="right:{p}px;top:{g["kick_y"]}px;font-size:{g["kick"]}px;{A_("fade", 0, .6)}">{kick}</div>' if kick and g.get('kick') else ''))
    tit = f'<div class="abs hd" {f"data-maxh={maxh}" if maxh else ""} style="left:{tx}px;top:{ty}px;width:{tw}px;font-size:{tsize}px;{A_("rise", .15, .9)}">{hl(title)}</div>'
    cta = (f'<div class="abs" style="left:{p}px;bottom:{g["cta_b"]}px;display:flex;flex-direction:column;align-items:flex-start;gap:{g.get("gap", 14)}px;{A_("pop", t_cta(), .7)}">'
           f'<span class="cta">{S["cta"]} <span style="font-size:.9em">→</span></span>'
           f'<div class="url">{S["url"]} <span class="fine" style="font-family:\'DM Sans\';font-weight:400;letter-spacing:0">· {S["fine"]}</span></div></div>')
    an1 = 'animation:d1 12s ease-in-out 0s infinite;' if CTX['anim'] else ''
    an2 = 'animation:d2 12s ease-in-out 0s infinite;' if CTX['anim'] else ''
    bg = (f'<div class="grid"></div><div class="blob" style="left:-260px;top:{b1}px;width:{s1}px;height:{s1}px;background:{C};opacity:.30;{an1}"></div>'
          f'<div class="blob" style="right:-300px;top:{b2}px;width:{s2}px;height:{s2}px;background:{PETROL};opacity:.55;{an2}"></div>')
    return f'<!doctype html><meta charset="utf-8"><style>{FONTS}{css}</style><div class="kv">{bg}{body}{top}{tit}{cta}</div>{SEEK}'


# ------------------------------------------------------------------ heros 4:5 (o que o Gui aprova)
def rk03():  # braço (v1 aprovada)
    b = (phone('racket_arm.jpg', 400, 610, 400, rot=(-10, 4, 2.5))
         + kick('Por trás do motor', 64, 470)
         + num('21', 'estudos científicos sobre braço e equipamento', 64, 515, 470, 168)
         + num('46', 'variáveis cruzadas para cada raquete', 64, 790, 470, 168)
         + sub('Rigidez, peso, balanço e a articulação que dói, avaliados antes de pagar.', 64, 1060, 500, 27))
    return frame('racket', b, 'Raquete errada, *o braço* paga.', 104, kick='Conforto no braço')


def rk03b():  # braço v2: "Da pra botar números mais chamativos" → 3.000 em corpo gigante, 183 e 21
    b = (num('3.000', 'perfis simulados em cada teste de segurança, para barrar recomendações arriscadas', 64, 372, 952, 250, 29)
         + phone('racket_arm.jpg', 300, 712, 690, rot=(-10, 4, 2.5))
         + num('183', 'raquetes com specs medidas: rigidez, peso e balanço avaliados antes de você pagar', 64, 740, 580, 230, 28))
    return frame('racket', b, 'Raquete errada, *o braço* paga.', 104, kick='Conforto no braço')


def rk04():  # são seis
    b = (phone('racket_l_seis.jpg', 320, 700, 690, rot=(-11, 4, 3))
         + num('279.990', 'combinações de raquete, grip, corda, espessura e tensão. O seu setup é uma delas.', 64, 380, 950, 210, 30)
         + chips(('Modelo', 'Cabeça', 'Grip', 'Corda', 'Espessura', 'Tensão'), 64, 700, 580)
         + sub('Uma decisão errada anula as outras certas.', 64, 840, 560, 28)
         + num('8.418', 'comparações entre você e o catálogo a cada teste', 64, 920, 560, 96, 26))
    return frame('racket', b, 'Raquete não é uma escolha. São *seis.*', 92, tw=900, kick='Por que é fácil errar')


def rk05():  # 183, uma é a sua
    b = (phone('racket_res.jpg', 420, 600, 360, rot=(-9, 3, 2), zoom=1.0)
         + num('183', 'raquetes com specs medidas, cruzadas uma a uma com o seu jogo', 64, 400, 500, 200, 28)
         + rule(64, 700, 470)
         + num('3.000', 'perfis simulados em cada teste de segurança', 64, 740, 500, 104, 26)
         + num('670', 'avaliações de testadores e sites lidas', 64, 950, 500, 104, 26))
    return frame('racket', b, '183 raquetes. *Uma* é a sua.', 104, kick='O motor')


def rk06():  # raquete do ídolo
    b = (phone('racket_card.jpg', 410, 610, 420, rot=(-10, 4, 2.5), zoom=1.18, fx=.5, fy=.25)
         + sub('Modelo de profissional tem mais peso e swingweight. Jogando duas vezes por semana, o golpe atrasa e o braço cansa.', 64, 420, 500, 30, 'pre')
         + num('379', 'casos de especialistas, em 3 idiomas, para calibrar o motor', 64, 690, 480, 150, 27)
         + num('670', 'avaliações de testadores e sites lidas', 64, 930, 480, 150, 27))
    return frame('racket', b, 'Raquete do ídolo, *golpe atrasado.*', 96, tw=960, kick='Erro comum')


RS = '<span style="font-size:.5em;letter-spacing:-.02em">R$</span>&nbsp;'


def sf04():  # custa caro
    b = (phone('surf_top3.jpg', 400, 620, 420, rot=(-10, 4, 2.5))
         + kick('Prancha nova', 64, 430)
         + num(RS + '4.000', 'é quanto pode custar uma prancha nova (de R$ 1.500 a R$ 4.000)', 64, 470, 540, 124, 27)
         + rule(64, 720, 500)
         + kick('Acertar a escolha', 64, 760)
         + num(RS + '19,99', 'é o relatório completo do SURF DNA, pagamento único', 64, 800, 540, 124, 27))
    return frame('surf', b, 'Errar a prancha custa *caro.*', 108, kick='Antes de comprar')


def sf05():  # 10 litros
    b = (phone('surf_tras.jpg', 400, 620, 440, rot=(-10, 4, 2.5))
         + num('10&nbsp;L', 'de diferença entre duas pranchas do mesmo tamanho. É a litragem que decide se você rema e entra na onda.', 64, 470, 520, 210, 28)
         + rule(64, 840, 500)
         + num('416', 'tamanhos de 35 modelos, comparados medida por medida', 64, 880, 520, 120, 26))
    return frame('surf', b, 'Duas 6\'0" podem ter *10 litros* de diferença.', 88, tw=960, kick='Litragem')


def sf06():  # 200 trilhões
    b = (phone('surf_card.jpg', 410, 620, 450, rot=(-10, 4, 2.5), zoom=1.18, fx=.5, fy=.25)
         + num('200 tri', 'de pranchas possíveis. O motor calcula cada medida para o seu surf.', 64, 470, 540, 168, 28)
         + rule(64, 770, 500)
         + num('13', 'tipos de prancha disputam o seu resultado', 64, 810, 250, 120, 25)
         + num('17', 'medidas na ficha técnica para qualquer shaper', 330, 810, 250, 120, 25))
    return frame('surf', b, 'Mais de *200 trilhões* de pranchas. A sua sai sob medida.', 84, tw=960, kick='O motor')


def sf07():  # prancha do amigo
    b = (phone('surf_nivel.jpg', 400, 620, 440, rot=(-10, 4, 2.5))
         + sub('A litragem foi pensada para outro peso, outro nível e outro mar.', 64, 450, 520, 30, 'pre')
         + num('422', 'casos reais de lojas, revistas, marcas, atletas e fóruns na calibração', 64, 640, 520, 150, 26)
         + num('1.000+', 'fontes de surf mapeadas, em mais de 400 sites', 64, 900, 520, 150, 26))
    return frame('surf', b, 'A prancha do amigo foi feita pra *outro surfista.*', 88, tw=960, kick='Erro comum')


HERO = {'ADC-RK-03-v1': rk03, 'ADC-RK-03-v2': rk03b, 'ADC-RK-04-v1': rk04, 'ADC-RK-05-v1': rk05, 'ADC-RK-06-v1': rk06,
        'ADC-SF-04-v1': sf04, 'ADC-SF-05-v1': sf05, 'ADC-SF-06-v1': sf06, 'ADC-SF-07-v1': sf07}

# ------------------------------------------------------------------ conteúdo para as adaptações (mesmo texto do hero)
PH = lambda src, zoom=1.0, fy=0.0: dict(src=src, zoom=zoom, fy=fy)
SPEC = {
 'ADC-RK-03-v1': dict(sp='racket', title='Raquete errada, *o braço* paga.', kick='Conforto no braço', ph=PH('racket_arm.jpg'),
                      nums=[('21', 'estudos científicos sobre braço e equipamento'), ('46', 'variáveis cruzadas para cada raquete')],
                      post='Rigidez, peso, balanço e a articulação que dói, avaliados antes de pagar.'),
 'ADC-RK-03-v2': dict(sp='racket', title='Raquete errada, *o braço* paga.', kick='Conforto no braço', ph=PH('racket_arm.jpg'),
                      nums=[('3.000', 'perfis simulados em cada teste de segurança, para barrar recomendações arriscadas'), ('183', 'raquetes com specs medidas: rigidez, peso e balanço avaliados antes de você pagar')]),
 'ADC-RK-04-v1': dict(sp='racket', title='Raquete não é uma escolha. São *seis.*', kick='Por que é fácil errar', ph=PH('racket_l_seis.jpg'),
                      nums=[('279.990', 'combinações de raquete, grip, corda, espessura e tensão. O seu setup é uma delas.'), ('8.418', 'comparações entre você e o catálogo a cada teste')],
                      chips=('Modelo', 'Cabeça', 'Grip', 'Corda', 'Espessura', 'Tensão'), post='Uma decisão errada anula as outras certas.'),
 'ADC-RK-05-v1': dict(sp='racket', title='183 raquetes. *Uma* é a sua.', kick='O motor', ph=PH('racket_res.jpg'),
                      nums=[('183', 'raquetes com specs medidas, cruzadas uma a uma com o seu jogo'), ('3.000', 'perfis simulados em cada teste de segurança'), ('670', 'avaliações de testadores e sites lidas')]),
 'ADC-RK-06-v1': dict(sp='racket', title='Raquete do ídolo, *golpe atrasado.*', kick='Erro comum', ph=PH('racket_card.jpg', 1.18, .25),
                      pre='Modelo de profissional tem mais peso e swingweight. Jogando duas vezes por semana, o golpe atrasa e o braço cansa.',
                      nums=[('379', 'casos de especialistas, em 3 idiomas, para calibrar o motor'), ('670', 'avaliações de testadores e sites lidas')]),
 'ADC-SF-04-v1': dict(sp='surf', title='Errar a prancha custa *caro.*', kick='Antes de comprar', ph=PH('surf_top3.jpg'),
                      nums=[(RS + '4.000', 'é quanto pode custar uma prancha nova (de R$ 1.500 a R$ 4.000)', 'Prancha nova'), (RS + '19,99', 'é o relatório completo do SURF DNA, pagamento único', 'Acertar a escolha')]),
 'ADC-SF-05-v1': dict(sp='surf', title='Duas 6\'0" podem ter *10 litros* de diferença.', kick='Litragem', ph=PH('surf_tras.jpg'),
                      nums=[('10&nbsp;L', 'de diferença entre duas pranchas do mesmo tamanho. É a litragem que decide se você rema e entra na onda.'), ('416', 'tamanhos de 35 modelos, comparados medida por medida')]),
 'ADC-SF-06-v1': dict(sp='surf', title='Mais de *200 trilhões* de pranchas. A sua sai sob medida.', kick='O motor', ph=PH('surf_card.jpg', 1.18, .25),
                      nums=[('200 tri', 'de pranchas possíveis. O motor calcula cada medida para o seu surf.'), ('13', 'tipos de prancha disputam o seu resultado'), ('17', 'medidas na ficha técnica para qualquer shaper')]),
 'ADC-SF-07-v1': dict(sp='surf', title='A prancha do amigo foi feita pra *outro surfista.*', kick='Erro comum', ph=PH('surf_nivel.jpg'),
                      pre='A litragem foi pensada para outro peso, outro nível e outro mar.',
                      nums=[('422', 'casos reais de lojas, revistas, marcas, atletas e fóruns na calibração'), ('1.000+', 'fontes de surf mapeadas, em mais de 400 sites')]),
}
ROT = (-10, 4, 2.5)


def adapt(v, fmt):
    s = SPEC[v]; W, H = FMT[fmt]; ph = s['ph']; nums = s['nums']
    def N(i, x, y, w, size, ls):
        n = nums[i]; k = kick(n[2], x, y - ls - 20, max(16, ls - 6)) if len(n) > 2 else ''
        return k + num(n[0], n[1], x, y, w, size, ls)
    if fmt == 'sq':
        g = dict(pad=56, logo_y=46, logo_h=44, kick_y=60, kick=19, cta_b=46, cta=30, cta_p=(16, 26), url=20, fine=18, blob=(260, 640, 560, 700))
        b = phone(ph['src'], 330, 694, 318, ROT, ph['zoom'], .5, ph['fy']); y = 345
        if s.get('pre'): b += sub(s['pre'], 56, y, 590, 25, 'pre'); y += 125
        two = nums[:2]; sizes = (150, 104) if not s.get('pre') else (124, 96)
        for i in range(len(two)):
            yy = y + (24 if len(nums[i]) > 2 else 0); b += N(i, 56, yy, 590, sizes[i], 24); y = yy + sizes[i] * .88 + 100 + (10 if i == 0 else 0)
        return frame(s['sp'], b, s['title'], 80, ty=112, tw=968, kick=s['kick'], W=W, H=H, g=g, maxh=170)
    if fmt == 'story':
        g = dict(pad=64, logo_y=290, logo_h=52, kick_y=306, kick=22, cta_b=390, cta=38, cta_p=(22, 34), url=25, fine=23, blob=(700, 860, 1150, 900))
        b = phone(ph['src'], 360, 660, 745, ROT, ph['zoom'], .5, ph['fy']); y = 785
        if s.get('pre'): b += sub(s['pre'], 64, y, 520, 30, 'pre'); y += 190
        two = nums[:2] if not s.get('pre') else nums[:1]; sizes = (190, 128) if not s.get('pre') else (190,)
        for i in range(len(two)):
            yy = y + (30 if len(nums[i]) > 2 else 0); b += N(i, 64, yy, 540, sizes[i], 28); y = yy + sizes[i] * .88 + 140
        if s.get('chips') and y < 1330: b += chips(s['chips'], 64, y - 20, 540, 24)
        return frame(s['sp'], b, s['title'], 112, ty=380, tw=952, kick=s['kick'], W=W, H=H, g=g, maxh=360)
    if fmt == 'land':
        g = dict(pad=40, logo_y=32, logo_h=34, kick_y=0, kick=0, cta_b=32, cta=23, cta_p=(12, 20), url=16, fine=15, blob=(120, 460, 300, 500))
        b = phone(ph['src'], 236, 920, 52, ROT, ph['zoom'], .5, ph['fy']) + num(nums[0][0], nums[0][1], 40, 268, 700, 120, 21)
        return frame(s['sp'], b, s['title'], 54, ty=84, tw=800, W=W, H=H, g=g, maxh=118)
    if fmt == '16x9':
        g = dict(pad=90, logo_y=70, logo_h=56, kick_y=88, kick=22, cta_b=80, cta=38, cta_p=(22, 34), url=25, fine=23, blob=(200, 860, 500, 900))
        b = phone(ph['src'], 440, 1380, 112, ROT, ph['zoom'], .5, ph['fy'])
        two = nums[:2]
        for i in range(len(two)):
            b += N(i, 90 + i * 600, 500 if len(nums[i]) > 2 else 470, 540, 190, 27)
        extra = s.get('pre') or s.get('post')
        if extra: b += sub(extra, 90, 780, 1150, 29, 'post')
        return frame(s['sp'], b, s['title'], 104, ty=170, tw=1180, kick=s['kick'], W=W, H=H, g=g, maxh=230)


def page(v, fmt, anim=False):
    CTX['anim'] = anim; CTX['ni'] = 0
    return HERO[v]() if fmt == 'feed45' else adapt(v, fmt)


async def shot(pg, html, path, W, H):
    await pg.set_viewport_size({'width': W, 'height': H})
    await pg.set_content(html); await pg.evaluate('document.fonts.ready'); await pg.evaluate('fit()'); await pg.wait_for_timeout(200)
    await pg.screenshot(path=str(path))


async def motion(b, v, fmt, out):
    W, H = FMT[fmt]; pg = await b.new_page(viewport={'width': W, 'height': H})
    await pg.set_content(page(v, fmt, True)); await pg.evaluate('document.fonts.ready'); await pg.evaluate('fit()'); await pg.wait_for_timeout(200)
    fr = out / f'_fr_{fmt}'; fr.mkdir(exist_ok=True)
    for i in range(int(MOTION_T * 30)):
        await pg.evaluate(f'seek({i / 30})'); await pg.screenshot(path=str(fr / f'{i:05d}.jpg'), type='jpeg', quality=92)
    await pg.close()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-i', str(fr / '%05d.jpg'), '-an', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                    '-crf', '19', '-preset', 'medium', '-movflags', '+faststart', str(out / f'{v}-motion-{fmt}.mp4')], check=True)
    shutil.rmtree(fr)


async def main(mode, ids, outdir):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if mode == 'motion':
            jobs = [motion(b, v, f, outdir / v) for v in ids for f in ('feed45', 'sq', 'story')]
            for v in ids: (outdir / v).mkdir(parents=True, exist_ok=True)
            for i in range(0, len(jobs), 6): await asyncio.gather(*jobs[i:i + 6])
        else:
            pg = await b.new_page()
            for v in ids:
                d = outdir / v; d.mkdir(parents=True, exist_ok=True)
                for f in (('feed45',) if mode == 'hero' else ('sq', 'story', 'land', '16x9')):
                    W, H = FMT[f]; await shot(pg, page(v, f), d / f'{v}-{f}.png', W, H)
                print(v, flush=True)
        await b.close()


if __name__ == '__main__':
    mode, SCR, outdir = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    ids = sys.argv[4:] or [k for k in HERO if k != 'ADC-RK-03-v2']
    asyncio.run(main(mode, ids, outdir))
