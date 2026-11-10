"""ADC-QD-10 v1 · adaptações do KV aprovado (var. b, fundo tinta) para 1:1, 9:16, 1,91:1, 16:9 e motions 9:16, 4:5, 1:1.
Mesmo texto, cores e capturas do hero; cronômetro igual no telão e no celular (quadros do mesmo instante:
tv_q + cel_q = 29 s, pergunta aberta; tv_q3 + cel_tap = 24 s, depois do toque em A).
Uso: python3 qd10_adapt.py <pasta da captura kv10g> <saida> [static|motion|all] [preview]"""
import asyncio, base64, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import ff, svg, A, Comp, render, preview, EASE, BACK
from playwright.async_api import async_playwright
CAP, OUT = Path(sys.argv[1]), Path(sys.argv[2]); WHICH = sys.argv[3] if len(sys.argv) > 3 else 'all'; PREV = len(sys.argv) > 4 and sys.argv[4] == 'preview'
ONLY = sys.argv[5] if len(sys.argv) > 5 else None  # story|feed45|sq
OUT.mkdir(parents=True, exist_ok=True)
V = 'ADC-QD-10-v1'; Q = A / 'quiddo'
CREME, TINTA, MATA, AMARELO = '#FFF6E6', '#0E2A22', '#0B5D45', '#FFC83D'
def uri(p): return 'data:image/png;base64,' + base64.b64encode(Path(p).read_bytes()).decode()
FONTS = ff('Fraunces', 'Fraunces-900.woff2', '900') + ff('Nunito', 'Nunito-var.woff2', '600 900')
TV0, CEL0, TV1, CEL1 = (uri(CAP / f) for f in ('tv_q.png', 'cel_q.png', 'tv_q3.png', 'cel_tap.png'))
NEG = (Q / 'quiddo-negativo.svg')
CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}
.kv{{position:relative;overflow:hidden;font-family:Nunito,sans-serif;background:{TINTA};color:{CREME}}}
.abs{{position:absolute}}
.t{{font-family:Fraunces,serif;font-weight:900;letter-spacing:-.025em;line-height:.98;color:{CREME}}}
.mt{{display:inline-block;background:{AMARELO};color:{TINTA};padding:0 .12em;transform:rotate(-2deg);border-radius:.08em;border:5px solid {TINTA};box-shadow:0 7px 0 {TINTA}}}
.tv{{background:#111;border-radius:22px;padding:14px;border:6px solid {TINTA};box-shadow:0 16px 0 {TINTA}}}
.tv .s{{position:relative;overflow:hidden;border-radius:10px;aspect-ratio:1920/1030}} .tv img{{position:absolute;left:0;top:0;width:100%}}
.ph{{background:#0b0b0d;border-radius:54px;padding:12px;border:6px solid {TINTA};box-shadow:0 14px 0 {TINTA}}}
.ph .s{{position:relative;border-radius:42px;overflow:hidden;aspect-ratio:1080/1749}} .ph img{{position:absolute;left:0;top:0;width:100%}}
.cta{{display:inline-flex;align-items:center;background:{AMARELO};color:{TINTA};border:6px solid {TINTA};box-shadow:0 10px 0 {TINTA};border-radius:999px;font-weight:900}}
.url{{font-weight:900;color:{AMARELO}}}
.sub{{font-weight:700;line-height:1.3;color:{CREME}}}
"""
TIT1, TIT2 = 'Sua apresentação', 'vira <span class="mt">participação.</span>'
SUB = 'Quiz ao vivo para apresentações e treinamentos. Você pergunta. O público responde pelo celular.'

# x, y, largura (ou tamanho de fonte) de cada bloco por formato
L = {
 'feed45': dict(W=1080, H=1350, logo=(70, 64, 230), tit=(70, 150, 960, 92), tv=(70, 430, 940, 0), ph=(792, 905, 250, 4),
                sub=(70, 1010, 620, 34), cta=(70, 1196, 40, 32), glow=(-200, 300, 1480, 760)),
 'sq':     dict(W=1080, H=1080, logo=(56, 48, 190), tit=(56, 118, 980, 74), tv=(56, 318, 700, 0), ph=(800, 360, 230, 4),
                sub=(56, 766, 700, 29), cta=(56, 950, 34, 28), glow=(-260, 200, 1400, 700)),
 'story':  dict(W=1080, H=1920, logo=(70, 290, 230), tit=(70, 384, 960, 104), tv=(90, 622, 900, 0), ph=(780, 1162, 220, 4),
                sub=(70, 1200, 640, 36), cta=(70, 1420, 40, 32), glow=(-240, 560, 1560, 900)),
 'land':   dict(W=1200, H=628, logo=(48, 40, 140), tit=(48, 98, 560, 52), tv=(620, 64, 540, 0), ph=(1050, 360, 118, 4),
                sub=(48, 240, 520, 22), cta=(48, 470, 24, 20), glow=(300, 0, 1000, 600)),
 '16x9':   dict(W=1920, H=1080, logo=(110, 96, 250), tit=(110, 210, 880, 92), tv=(1000, 130, 820, 0), ph=(1590, 622, 230, 4),
                sub=(110, 470, 760, 38), cta=(110, 760, 44, 36), glow=(500, 60, 1600, 1000)),
}

def blocks(f, an=None, tv_imgs=None, ph_imgs=None, ring=''):
    """an(nome) devolve o style de animação do bloco (motion) ou '' (estático)."""
    z = L[f]; an = an or (lambda k: ''); gx, gy, gw, gh = z['glow']
    lx, ly, lw = z['logo']; tx, ty, tw, ts = z['tit']; vx, vy, vw, _ = z['tv']; px, py, pw, pr = z['ph']
    sx, sy, sw, ss = z['sub']; cx, cy, cs, us = z['cta']
    tvi = tv_imgs or f'<img src="{TV0}">'; phi = ph_imgs or f'<img src="{CEL0}">'
    return (f'<div class="abs" style="left:{gx}px;top:{gy}px;width:{gw}px;height:{gh}px;border-radius:50%;background:radial-gradient({MATA},transparent 70%);opacity:.9"></div>'
            f'<div class="abs" style="left:{lx}px;top:{ly}px;{an("logo")}">{svg(NEG, w=lw)}</div>'
            f'<div class="abs t" style="left:{tx}px;top:{ty}px;width:{tw}px;font-size:{ts}px">'
            f'<div style="{an("t1")}">{TIT1}</div><div style="{an("t2")}">{TIT2}</div></div>'
            f'<div class="abs" style="left:{vx}px;top:{vy}px;{an("tv")}"><div class="tv" style="width:{vw}px;padding:{max(8, vw // 67)}px"><div class="s">{tvi}</div></div></div>'
            f'<div class="abs" style="left:{px}px;top:{py}px;{an("ph")}"><div style="transform-origin:100% 100%;{an("phz")}"><div style="transform:rotate({pr}deg)"><div class="ph" style="width:{pw}px;padding:{max(6, pw // 21)}px;border-radius:{pw * .22:.0f}px">'
            f'<div class="s" style="border-radius:{pw * .17:.0f}px">{phi}{ring}</div></div></div></div></div>'
            f'<div class="abs sub" style="left:{sx}px;top:{sy}px;width:{sw}px;font-size:{ss}px;{an("sub")}">{SUB}</div>'
            f'<div class="abs" style="left:{cx}px;top:{cy}px;display:flex;align-items:center;gap:{cs * .65:.0f}px;{an("cta")}">'
            f'<span class="cta" style="font-size:{cs}px;padding:{cs * .45:.0f}px {cs * .85:.0f}px;border-width:{max(3, cs // 7)}px">Crie seu quiz</span>'
            f'<span class="url" style="font-size:{us}px">quiddo.com.br</span></div>')

async def statics():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for f, name in (('sq', 'sq'), ('story', 'story'), ('land', 'land'), ('16x9', '16x9')):
            z = L[f]; pg = await b.new_page(viewport={'width': z['W'], 'height': z['H']})
            html = f'<!doctype html><meta charset="utf-8"><style>{FONTS}{CSS}</style><div class="kv" style="width:{z["W"]}px;height:{z["H"]}px">{blocks(f)}</div>'
            await pg.set_content(html); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f'{V}-{name}.png')); await pg.close(); print('ok', name)
        await b.close()

def motion(f, fmt_comp, out):
    T = 15.0; c = Comp(fmt_comp, T, TINTA, FONTS, CSS)
    TAP, SWAP = 6.4, 6.55
    A = {'logo': c.enter(.15, 'fade', .7), 't1': c.enter(.4, 'rise', .7, 50), 't2': c.enter(1.1, 'rise', .7, 50),
         'tv': c.enter(2.2, 'rise', .8, 80), 'ph': c.enter(3.0, 'right', .8, 120), 'sub': c.enter(8.4, 'rise', .7, 40), 'cta': c.enter(10.6, 'pop', .7)}
    zs = 1.28 if f == 'story' else 1.12
    A['phz'] = c.kf([(3.9, 'transform:scale(1)'), (5.1, f'transform:scale({zs})', EASE), (8.2, f'transform:scale({zs})', EASE), (9.4, 'transform:scale(1)')], EASE)
    an = lambda k: c.an(A[k])
    # telão e celular: quadro antes do toque (29 s) e depois do toque (24 s, 5 de 9 responderam), mesmo instante nos dois
    x0, x1 = c.show(0, SWAP, 0, .25), c.show(SWAP - .25, None, .25, 0)
    tv = f'<img src="{TV0}" style="{c.an(x0)}"><img src="{TV1}" style="{c.an(x1)}">'
    ph = f'<img src="{CEL0}" style="{c.an(x0)}"><img src="{CEL1}" style="{c.an(x1)}">'
    # toque no A (Entender a necessidade): ~28% da altura visível da tela do celular, metade da largura
    k = c.kf([(TAP - .01, 'opacity:0;transform:translate(-50%,-50%) scale(.3)', 'ease-out'), (TAP + .1, 'opacity:1;transform:translate(-50%,-50%) scale(.75)', 'ease-out'), (TAP + .8, 'opacity:0;transform:translate(-50%,-50%) scale(1.5)')])
    ring = f'<div class="abs" style="left:45%;top:35.5%;width:28%;aspect-ratio:1;border-radius:50%;border:6px solid rgba(255,255,255,.95);box-shadow:0 0 0 3px {TINTA};z-index:5;{c.an(k)}"></div>'
    # zoom suave no celular durante o toque, voltando ao KV completo
    z = c.kf([(3.8, 'transform:scale(1)'), (5.2, 'transform:scale(1.06)', EASE), (8.0, 'transform:scale(1.06)', EASE), (9.2, 'transform:scale(1)')], EASE)
    body = blocks(f, an, tv, ph, ring)
    c.add(f'<div class="kv" style="width:{c.W}px;height:{c.H}px">{body}</div>')
    if PREV:
        preview(c, out.with_suffix('.jpg'), [0, .6, 1.5, 2.6, 3.5, 5, 6.45, 6.7, 8, 9, 10.8, 14.9], cols=6, scale=.2); return
    render(c, out)

if WHICH in ('static', 'all') and not PREV: asyncio.run(statics())
if WHICH in ('motion', 'all'):
    for f, fc, n in (('story', 'reel', 'motion-story'), ('feed45', 'feed', 'motion-feed45'), ('sq', 'sq', 'motion-sq')):
        if ONLY and f != ONLY: continue
        motion(f, fc, OUT / f'{V}-{n}.mp4'); print('ok', n)
