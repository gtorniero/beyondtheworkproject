"""KVs estáticos SPORT DNA (RACKET e SURF), 4:5, no look da referência ADC-RZ-08 / dna_ref.py:
preto com grade técnica e luz na cor do esporte, título Archivo enorme e provocativo, BIG NUMBERS do motor (Syne 800)
e o celular com a tela REAL do site (dna_capture.py + kv_dna_stills.py). Números só os que o site mostra (conferidos em 10/11).
Uso: python3 kv_dna.py <pasta das telas> <pasta de saída> [IDs...]"""
import asyncio, base64, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import ff, svg, A
from playwright.async_api import async_playwright

SCR, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[3:])
INK, MUTED, PETROL = '#0A0A0A', '#A3A3A0', '#0E4D64'
SD = A / 'sportdna'
FONTS = ff('Archivo', 'Archivo-800.woff2', '800') + ff('Syne', 'Syne-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700') + ff('JetBrains Mono', 'JBMono-var.woff2', '400 700')
SP = {
    'racket': dict(c='#DDF247', logo='racketdna-logo-fundo-escuro.svg', cta='Descobrir minha raquete', url='sportdna.com.br/racket', fine='Você vê o diagnóstico antes de pagar.'),
    'surf': dict(c='#6CCFF6', logo='surfdna-logo-fundo-escuro.svg', cta='Descobrir minha prancha', url='sportdna.com.br/surf', fine='Prévia grátis · 3 minutos · sem cadastro.'),
}


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
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;transform:perspective(2200px) rotateY({ry}deg) rotateX({rx}deg) rotateZ({rz}deg)">'
            f'<div class="ph" style="width:{w}px;height:{h:.0f}px;border-radius:{w * .11:.0f}px">'
            f'<div class="scr" style="left:{b}px;top:{b}px;right:{b}px;bottom:{b}px;border-radius:{w * .11 - b:.0f}px">{inner}</div>'
            f'<div class="gl"></div></div></div>')


def num(n, label, x, y, w, size=150, lsize=30):
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px"><div class="num" style="font-size:{size}px">{n}</div>'
            f'<div class="lab" style="font-size:{lsize}px;margin-top:{size * .07:.0f}px">{label}</div></div>')


FIT = """<script>window.fit=()=>{document.querySelectorAll('.num').forEach(n=>{const w=n.parentElement.clientWidth;let f=parseFloat(getComputedStyle(n).fontSize),i=0;while(n.scrollWidth>w&&i<60){f*=.97;n.style.fontSize=f+'px';i++}});document.documentElement.dataset.ok=1};</script>"""


def frame(sp, body, title, tsize=96, ty=150, tw=940, kick=''):
    S = SP[sp]; C = S['c']
    css = f"""*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;overflow:hidden;background:{INK}}}
.kv{{position:relative;width:1080px;height:1350px;overflow:hidden;background:{INK};color:#fff;font-family:'DM Sans',sans-serif}}
.abs{{position:absolute}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.05) 2px,transparent 2px);background-size:90px 90px}}
.blob{{position:absolute;border-radius:50%;filter:blur(130px)}}
.hd{{font-family:Archivo,sans-serif;font-weight:800;letter-spacing:-.035em;line-height:.98;color:#fff;text-wrap:balance}}
.hl{{color:{C}}}
.num{{display:inline-block;font-family:Syne,sans-serif;font-weight:800;letter-spacing:-.045em;line-height:.88;color:{C};white-space:nowrap}}
.lab{{font-weight:700;line-height:1.2;color:#fff}}
.sub{{font-weight:400;line-height:1.35;color:#D9D9D6}}
.kick{{font-family:'JetBrains Mono',monospace;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{MUTED};font-size:21px}}
.chip{{display:inline-block;font-weight:700;border:2px solid rgba(255,255,255,.28);border-radius:12px;padding:8px 16px;font-size:26px;color:#fff;margin:0 8px 10px 0}}
.cta{{display:inline-flex;align-items:center;gap:14px;background:{C};color:{INK};border-radius:16px;padding:20px 30px;font-weight:700;font-size:34px;white-space:nowrap}}
.url{{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:24px;color:#fff;letter-spacing:.02em}}
.fine{{font-size:22px;color:{MUTED}}}
.ph{{position:relative;background:#1d1d1f;box-shadow:0 0 0 3px rgba(255,255,255,.28),0 0 120px {C}55,0 50px 110px rgba(0,0,0,.7)}}
.ph .scr{{position:absolute;overflow:hidden;background:#fff}}
.ph .gl{{position:absolute;inset:0;border-radius:inherit;background:linear-gradient(125deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,0) 26%);pointer-events:none}}
.rule{{position:absolute;height:2px;background:rgba(255,255,255,.18)}}
"""
    top = (f'<div class="abs" style="left:64px;top:58px;height:50px">{svg(SD / S["logo"], h=50)}</div>'
           + (f'<div class="abs kick" style="right:64px;top:74px">{kick}</div>' if kick else ''))
    tit = f'<div class="abs hd" style="left:64px;top:{ty}px;width:{tw}px;font-size:{tsize}px">{hl(title)}</div>'
    cta = (f'<div class="abs" style="left:64px;bottom:58px;display:flex;flex-direction:column;align-items:flex-start;gap:14px">'
           f'<span class="cta">{S["cta"]} <span style="font-size:.9em">→</span></span>'
           f'<div class="url">{S["url"]} <span class="fine" style="font-family:\'DM Sans\';font-weight:400;letter-spacing:0">· {S["fine"]}</span></div></div>')
    bg = (f'<div class="grid"></div><div class="blob" style="left:-260px;top:300px;width:760px;height:760px;background:{C};opacity:.30"></div>'
          f'<div class="blob" style="right:-300px;top:720px;width:820px;height:820px;background:{PETROL};opacity:.55"></div>')
    return f'<!doctype html><meta charset="utf-8"><style>{FONTS}{css}</style><div class="kv">{bg}{body}{top}{tit}{cta}</div>{FIT}'


# ------------------------------------------------------------------ os 8 KVs
def rk03():  # braço
    b = (phone('racket_arm.jpg', 400, 610, 400, rot=(-10, 4, 2.5))
         + '<div class="abs kick" style="left:64px;top:470px">Por trás do motor</div>'
         + num('21', 'estudos científicos sobre braço e equipamento', 64, 515, 470, 168)
         + num('46', 'variáveis cruzadas para cada raquete', 64, 790, 470, 168)
         + '<div class="abs sub" style="left:64px;top:1060px;width:500px;font-size:27px">Rigidez, peso, balanço e a articulação que dói, avaliados antes de pagar.</div>')
    return frame('racket', b, 'Raquete errada, *o braço* paga.', 104, kick='Conforto no braço')


def rk04():  # são seis
    chips = ''.join(f'<span class="chip">{c}</span>' for c in ('Modelo', 'Cabeça', 'Grip', 'Corda', 'Espessura', 'Tensão'))
    b = (phone('racket_l_seis.jpg', 320, 700, 690, rot=(-11, 4, 3))
         + num('279.990', 'combinações de raquete, grip, corda, espessura e tensão. O seu setup é uma delas.', 64, 380, 950, 210, 30)
         + f'<div class="abs" style="left:64px;top:700px;width:580px">{chips}</div>'
         + '<div class="abs sub" style="left:64px;top:840px;width:560px;font-size:28px">Uma decisão errada anula as outras certas.</div>'
         + num('8.418', 'comparações entre você e o catálogo a cada teste', 64, 920, 560, 96, 26))
    return frame('racket', b, 'Raquete não é uma escolha. São *seis.*', 92, tw=900, kick='Por que é fácil errar')


def rk05():  # 183, uma é a sua
    b = (phone('racket_res.jpg', 420, 600, 360, rot=(-9, 3, 2), zoom=1.0)
         + num('183', 'raquetes com specs medidas, cruzadas uma a uma com o seu jogo', 64, 400, 500, 200, 28)
         + '<div class="rule" style="left:64px;top:700px;width:470px"></div>'
         + num('3.000', 'perfis simulados em cada teste de segurança', 64, 740, 500, 104, 26)
         + num('670', 'avaliações de testadores e sites lidas', 64, 950, 500, 104, 26))
    return frame('racket', b, '183 raquetes. *Uma* é a sua.', 104, kick='O motor')


def rk06():  # raquete do ídolo
    b = (phone('racket_card.jpg', 410, 610, 420, rot=(-10, 4, 2.5), zoom=1.18, fx=.5, fy=.25)
         + '<div class="abs sub" style="left:64px;top:420px;width:500px;font-size:30px">Modelo de profissional tem mais peso e swingweight. Jogando duas vezes por semana, o golpe atrasa e o braço cansa.</div>'
         + num('379', 'casos de especialistas, em 3 idiomas, para calibrar o motor', 64, 690, 480, 150, 27)
         + num('670', 'avaliações de testadores e sites lidas', 64, 930, 480, 150, 27))
    return frame('racket', b, 'Raquete do ídolo, *golpe atrasado.*', 96, tw=960, kick='Erro comum')


def sf04():  # custa caro
    b = (phone('surf_top3.jpg', 400, 620, 420, rot=(-10, 4, 2.5))
         + '<div class="abs kick" style="left:64px;top:430px">Prancha nova</div>'
         + num('<span style="font-size:.5em;letter-spacing:-.02em">R$</span>&nbsp;4.000', 'é quanto pode custar uma prancha nova (de R$ 1.500 a R$ 4.000)', 64, 470, 540, 124, 27)
         + '<div class="rule" style="left:64px;top:720px;width:500px"></div>'
         + '<div class="abs kick" style="left:64px;top:760px">Acertar a escolha</div>'
         + num('<span style="font-size:.5em;letter-spacing:-.02em">R$</span>&nbsp;19,99', 'é o relatório completo do SURF DNA, pagamento único', 64, 800, 540, 124, 27))
    return frame('surf', b, 'Errar a prancha custa *caro.*', 108, kick='Antes de comprar')


def sf05():  # 10 litros
    b = (phone('surf_tras.jpg', 400, 620, 440, rot=(-10, 4, 2.5))
         + num('10&nbsp;L', 'de diferença entre duas pranchas do mesmo tamanho. É a litragem que decide se você rema e entra na onda.', 64, 470, 520, 210, 28)
         + '<div class="rule" style="left:64px;top:840px;width:500px"></div>'
         + num('416', 'tamanhos de 35 modelos, comparados medida por medida', 64, 880, 520, 120, 26))
    return frame('surf', b, 'Duas 6\'0" podem ter *10 litros* de diferença.', 88, tw=960, kick='Litragem')


def sf06():  # 200 trilhões
    b = (phone('surf_card.jpg', 410, 620, 450, rot=(-10, 4, 2.5), zoom=1.18, fx=.5, fy=.25)
         + num('200 tri', 'de pranchas possíveis. O motor calcula cada medida para o seu surf.', 64, 470, 540, 168, 28)
         + '<div class="rule" style="left:64px;top:770px;width:500px"></div>'
         + num('13', 'tipos de prancha disputam o seu resultado', 64, 810, 250, 120, 25)
         + num('17', 'medidas na ficha técnica para qualquer shaper', 330, 810, 250, 120, 25))
    return frame('surf', b, 'Mais de *200 trilhões* de pranchas. A sua sai sob medida.', 84, tw=960, kick='O motor')


def sf07():  # prancha do amigo
    b = (phone('surf_nivel.jpg', 400, 620, 440, rot=(-10, 4, 2.5))
         + '<div class="abs sub" style="left:64px;top:450px;width:520px;font-size:30px">A litragem foi pensada para outro peso, outro nível e outro mar.</div>'
         + num('422', 'casos reais de lojas, revistas, marcas, atletas e fóruns na calibração', 64, 640, 520, 150, 26)
         + num('1.000+', 'fontes de surf mapeadas, em mais de 400 sites', 64, 900, 520, 150, 26))
    return frame('surf', b, 'A prancha do amigo foi feita pra *outro surfista.*', 88, tw=960, kick='Erro comum')


KVS = {'ADC-RK-03': rk03, 'ADC-RK-04': rk04, 'ADC-RK-05': rk05, 'ADC-RK-06': rk06,
       'ADC-SF-04': sf04, 'ADC-SF-05': sf05, 'ADC-SF-06': sf06, 'ADC-SF-07': sf07}


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for k, f in KVS.items():
            if ONLY and k not in ONLY: continue
            await pg.set_content(f()); await pg.evaluate('document.fonts.ready'); await pg.evaluate('fit()'); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / f'{k}-v1-feed45.png')); print(k, flush=True)
        await b.close()

asyncio.run(main())
