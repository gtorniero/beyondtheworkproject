"""ADC-RN-03 v1 · RUN DNA · "Seu tênis combina com você?" (modelo novo, estudio.py)
Uso: python3 rn03.py <pasta da captura (rn_capture.py)> <preview|render> [reel|feed|sq]
Reel 9:16 (20,5 s) e motions 4:5 e 1:1 (11 s). Captura real de /run/; números = os da tela (212 tênis, 13 marcas, 96/94/91%)."""
import json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import *

CAP = Path(sys.argv[1]); MODE = sys.argv[2]; ONLY = sys.argv[3:] or ['reel', 'feed', 'sq']
OUT = R / 'out' / 'media'
MK = json.loads((CAP / 'marks.json').read_text())
INFO = json.loads((CAP / 'info.json').read_text())
N_TENIS, PCT = int(INFO['modelos']), [int(p.strip('%')) for p in INFO['pcts']]


def cfr():
    """Quadros com carimbo de tempo → 30 fps constantes (links), na velocidade real."""
    d = CAP / 'cfr'
    if d.exists(): return d
    d.mkdir(); fr = json.loads((CAP / 'frames.json').read_text()); j = 0
    for i in range(int(MK['end'] * 30)):
        while j + 1 < len(fr) and fr[j + 1]['t'] <= i / 30: j += 1
        os.link(CAP / 'f' / fr[j]['f'], d / f'{i:05d}.jpg')
    return d


FD = cfr()
INK, OFF, RUN, PET = '#0A0A0A', '#F4F4F2', '#FF8A3D', '#0E4D64'
FONTS = ff('Archivo', 'Archivo-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700') + ff('JetBrains Mono', 'JBMono-var.woff2', '400 700') + ff('Syne', 'Syne-800.woff2', '800')
CSS = f"""
.hd{{font-family:Archivo;font-weight:800;letter-spacing:-.03em;color:#fff}}
.hl{{color:{RUN}}}
.mono{{font-family:'JetBrains Mono';font-weight:700;letter-spacing:.08em;text-transform:uppercase}}
.num{{font-family:Syne;font-weight:800;letter-spacing:-.04em;line-height:.85}}
.grid{{background-image:linear-gradient(rgba(255,255,255,.055) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.055) 2px,transparent 2px);background-size:90px 90px}}
.chip{{display:inline-block;background:{RUN};color:{INK};border-radius:14px;padding:14px 26px}}
.stage{{position:absolute;left:0;top:0;transform-origin:0 0;will-change:transform}}
"""
BZ, SW = 18, 640          # moldura e largura da tela do celular na base
B = SW / 1080             # px da captura → px da base


def vis(c, t0, t1=None):
    """Visível só entre t0 e t1, corte seco. (Contorna o show() do kit: dois keyframes no mesmo tempo viram fade.)"""
    p = []
    if t0 > 0: p += [(t0 - .004, 'opacity:0;visibility:hidden', 'linear')]
    p += [(t0, 'opacity:1;visibility:visible', 'linear')]
    if t1 is not None and t1 < c.T: p += [(t1 - .004, 'opacity:1;visibility:visible', 'linear'), (t1, 'opacity:0;visibility:hidden', 'linear')]
    return c.kf(p, 'linear')


def cam(c, pts, ease=SNAP):
    """Câmera: pts = [(t, cx, cy, z, sx, sy)]: o ponto (cx, cy) da captura (px de 1080×1920) vai para (sx, sy) do quadro, com a captura na escala z."""
    k = []
    for t, cx, cy, z, sx, sy in pts:
        s = z / B
        k.append((t, f'transform:translate({sx - s * (BZ + cx * B):.1f}px,{sy - s * (BZ + cy * B):.1f}px) scale({s:.4f})'))
    return c.kf(k, ease)


def shot(c, t0, t1, src, pts, rate=1.0, tilt=None, ease=SNAP):
    """Uma cena: celular com o clipe real + câmera. tilt = [(t, rotY, rotX)] opcional (perspectiva)."""
    ph = c.phone(c.clip(FD, src, t0, t1, rate), w=SW + 2 * BZ, bezel=BZ, radius=70, notch=False)
    if tilt:
        tk = c.kf([(t, f'transform:perspective(2200px) rotateY({ry}deg) rotateX({rx}deg)') for t, ry, rx in tilt], EASE)
        ph = f'<div style="transform-origin:50% 40%;{c.an(tk)}">{ph}</div>'
    return f'<div class="fill" style="{c.an(vis(c, t0, t1))}"><div class="stage" style="{c.an(cam(c, pts, ease))}">{ph}</div></div>'


def bg(c):
    drift = c.kf([(0, 'transform:translate(0,0)'), (c.T, 'transform:translate(-90px,-180px)')], 'linear')
    glow = c.kf([(0, 'transform:translate(-20%,10%) scale(1)'), (c.T * .5, 'transform:translate(25%,-8%) scale(1.25)'), (c.T, 'transform:translate(-20%,10%) scale(1)')], 'ease-in-out')
    return (f'<div class="abs grid" style="inset:-200px;{c.an(drift)}"></div>'
            f'<div class="abs" style="left:10%;top:38%;width:80%;height:46%;border-radius:50%;background:radial-gradient(closest-side,rgba(255,138,61,.30),rgba(255,138,61,0));filter:blur(30px);{c.an(glow)}"></div>')


def scrim(c, h):
    """Faixa escura no topo para o título ler por cima do celular em close."""
    return f'<div class="abs" style="left:0;right:0;top:0;height:{h}px;background:linear-gradient({INK} 0%,{INK} 80%,rgba(10,10,10,0) 100%);z-index:10"></div>'


def title(c, text, t, out, y, size, x=70):
    return c.words(text, t, x, y, w=c.W - 2 * x, size=size, cls='hd', out=out, step=.06, dur=.45, style='z-index:20;white-space:nowrap;', lh=1.02)


def tag(c, text, t0, t1, x, y, size=30):
    a = c.enter(t0, 'left', .4, 40); o = c.exit(t1, 'fade', .2)
    return f'<div class="abs" style="left:{x}px;top:{y}px;z-index:20;{c.an(o)}"><div class="mono chip" style="font-size:{size}px;{c.an(a)}">{text}</div></div>'


def cta(c, t0, ty, ts, mid, zc):
    W, H = c.W, c.H; reel = c.fmt == 'reel'
    lg = svg(A / 'sportdna' / 'rundna-logo-fundo-escuro.svg', h=round(ts * .62))
    pose = cam(c, [(0, 540, 900, .62 * zc, W / 2, mid + 40)])
    tk = c.kf([(t0 + .1, 'opacity:0;transform:perspective(2200px) translateY(500px) rotateY(18deg) rotateX(-6deg)', EASE), (t0 + 1.0, 'opacity:1;transform:perspective(2200px) translateY(0) rotateY(-16deg) rotateX(9deg)')])
    ph = c.phone(c.clip(FD, MK['type_peso'] - .9, t0, c.T, 0.0), w=SW + 2 * BZ, bezel=BZ, radius=70, notch=False)
    py = (H - c.bot - 150) if reel else H - 235
    return (f'<div class="fill" style="background:{INK};z-index:30;{c.an(vis(c, t0))}">{bg(c)}'
            f'<div class="stage" style="{c.an(pose)}"><div style="transform-origin:50% 40%;{c.an(tk)}">{ph}</div></div>'
            + scrim(c, ty + ts * 2.04 + 130)
            + f'<div class="abs" style="left:70px;top:{ty - ts * .3:.0f}px;z-index:20;{c.an(c.enter(t0 + .05, "fade", .4))}">{lg}</div>'
            + c.words('Antes de comprar,\nfaça o *teste.*', t0 + .15, 70, ty + ts * .62, w=W - 140, size=ts, cls='hd', step=.08, dur=.5, style='z-index:20;white-space:nowrap;', lh=1.02)
            + f'<div class="abs" style="left:0;right:0;top:{py}px;text-align:center;z-index:20;{c.an(c.enter(t0 + .9, "pop", .5))}"><div class="chip" style="font:700 {ts * .5:.0f}px \'DM Sans\';border-radius:999px;padding:{ts * .24:.0f}px {ts * .5:.0f}px;box-shadow:0 20px 50px rgba(0,0,0,.5)">sportdna.com.br/run</div></div>'
            + f'<div class="abs" style="left:0;right:0;top:{py + ts * 1.42:.0f}px;text-align:center;z-index:20;{c.an(c.enter(t0 + 1.2, "fade", .4))}"><span class="mono" style="display:inline-block;background:{INK};color:#fff;border-radius:10px;padding:10px 18px;font-size:{ts * .24:.0f}px">{INFO["nQ"]} perguntas · {N_TENIS} tênis · {INFO["nBr"]} marcas</span></div></div>')


def build(fmt):
    reel = fmt == 'reel'
    T = 20.5 if reel else 11.0
    c = Comp(fmt, T, INK, FONTS, CSS)
    W, H = c.W, c.H
    ts = 100 if reel else (96 if fmt == 'feed' else 84)          # título
    ty = c.top + 24 if reel else c.top                            # topo do título
    band = ty + ts * 2.04 + 90                                       # fim da faixa do título
    mid = (band + (H - (c.bot if reel else 0))) / 2 + (20 if reel else 30)   # centro vertical da área do produto
    zc = 1.0 if reel else (.92 if fmt == 'feed' else .78)         # zoom dos closes
    c.add(bg(c))
    # tempos das cenas
    if reel: t = dict(hook=0, dor=2.0, pace=4.0, ana=6.0, top=8.5, k1=13.0, k2=14.5, k3=16.0, cta=17.5)
    else:    t = dict(hook=0, dor=2.0, ana=3.5, top=5.5, cta=8.5)
    # 1 · gancho: toque no campo e "72" digitado, celular em perspectiva, câmera entrando
    c.add(shot(c, 0, t['dor'], MK['type_peso'] - .9, [(0, 540, 900, .62 * zc, W / 2, mid + 40), (1.9, 540, 880, 1.14 * zc, W / 2, mid - 20)],
               tilt=[(0, -16, 9), (1.7, 0, 0)], ease=EASE))
    c.add(scrim(c, band + 40))
    c.add(title(c, 'Seu tênis combina\ncom *você?*', -1.5, t['dor'] - .12, ty, ts))
    # 2 · interação: onde dói (toque em "Joelho")
    t2 = t.get('pace', t['ana'])
    c.add(shot(c, t['dor'], t2, MK['tap_dor'] - .45, [(t['dor'], 540, 800, .95 * zc, W / 2, mid), (t['dor'] + 1.2, 540, 925, 1.17 * zc, W / 2, mid)], rate=.8, tilt=[(t['dor'], 9, 4), (t['dor'] + 1.0, 0, 0)], ease=EASE))
    c.add(c.ring(W / 2, mid, t['dor'] + .84, 200, RUN))
    c.add(title(c, 'O teste pergunta\n*onde dói.*', t['dor'] + .05, t2 - .12, ty, ts))
    if reel:
        # 3 · interação: ritmo (toque em "5:00 a 6:00 /km")
        c.add(shot(c, t['pace'], t['ana'], MK['tap_pace'] - .45, [(t['pace'], 540, 760, 1.0, W / 2, mid), (t['pace'] + 1.2, 540, 925, 1.17, W / 2, mid)], rate=.7, tilt=[(t['pace'], -9, 4), (t['pace'] + 1.0, 0, 0)], ease=EASE))
        c.add(c.ring(W / 2, mid, t['pace'] + .95, 200, RUN))
        c.add(title(c, 'E *como*\nvocê corre.', t['pace'] + .05, t['ana'] - .12, ty, ts))
    # 4 · análise: a lista real marcando + número rodando
    ax, ay = 540, 760; ta, tb = t['ana'], t['top']
    c.add(c.wipe(ta, RUN, .5, 'up'))
    c.add(shot(c, ta, tb, MK['analysis'] - .05, [(ta, ax, ay, .9 * zc, W / 2, mid + (150 if reel else 110) * zc), (tb, ax, ay + 40, 1.08 * zc, W / 2, mid + (150 if reel else 110) * zc)], rate=.78 if reel else .95, ease='linear'))
    ns = ts * 1.75
    c.add(f'<div class="abs" style="left:70px;top:{ty - 6}px;z-index:20;{c.an(vis(c, ta, tb - .1))}"><div class="num hl" style="font-size:{ns:.0f}px">{c.count(0, N_TENIS, ta + .1, ta + 1.5)}</div></div>')
    c.add(c.words('tênis cruzados com *você.*', ta + .35, 70, ty + ns * 1.0, size=ts * .6, cls='hd', out=tb - .12, style='z-index:20;white-space:nowrap;'))
    # 5 · recompensa: os 3 que mais combinam
    rx, ry = 540, 900; t5 = t['top']; t5b = t.get('k1', t['cta'])
    c.add(c.flash(t5, '#fff', .3, .9))
    z1 = 1.0 * zc; push = t5 + 2.6
    pts = [(t5, rx, ry, 1.6 * zc, W / 2, mid), (t5 + .7, rx, ry, z1, W / 2, mid), (push, rx, ry, z1 * 1.03, W / 2, mid)]
    if reel: pts += [(push + .7, 545, 720, 1.17, W / 2, mid - 40), (t5b, 545, 740, 1.21, W / 2, mid - 40)]
    c.add(shot(c, t5, t5b, MK['top3'] + 1.05, pts, rate=.7, ease=EASE))
    c.add(title(c, 'Os *3* tênis que\nmais combinam.', t5 + .1, t5b - .12, ty, ts))
    for i, y in enumerate((642, 868, 1130)):  # 96%, 94%, 91% da tela real
        c.add(c.ring(W / 2 + (930 - rx) * z1 * 1.01, mid + (y - ry) * z1 * 1.01, t5 + 1.0 + i * .45, 170, RUN))
    if reel:
        # 6 · prova: 3 cortes de outras telas reais
        c.add(title(c, 'E o *porquê*\nde cada um.', t['k1'] + .05, t['cta'] - .12, ty, ts))
        for mk, a, b, x, y, z in (('tras', t['k1'], t['k2'], 540, 800, 1.15), ('perfil', t['k2'], t['k3'], 540, 1020, .72), ('mapa', t['k3'], t['cta'], 540, 800, 1.02)):
            sg = 8 if mk != 'perfil' else -8
            c.add(shot(c, a, b, MK[mk] + .3, [(a, x, y, z * .86, W / 2, mid), (b, x, y, z, W / 2, mid)], tilt=[(a, sg, 3), (a + .8, 0, 0)], ease=EASE))
        c.add(tag(c, f'{N_TENIS} modelos avaliados', t['k1'] + .15, t['k2'] - .1, 70, band - 30))
        c.add(tag(c, 'seu perfil de corredor', t['k2'] + .15, t['k3'] - .1, 70, band - 30))
        c.add(tag(c, 'seus finalistas no catálogo', t['k3'] + .15, t['cta'] - .1, 70, band - 30))
    # 7 · CTA
    c.add(c.wipe(t['cta'], RUN, .5, 'down'))
    c.add(cta(c, t['cta'], ty, ts, mid, zc))
    return c


NAMES = {'reel': OUT / 'ADC-RN-03-v1.mp4', 'feed': OUT / 'ads' / 'ADC-RN-03-v1' / 'ADC-RN-03-v1-motion-feed45.mp4', 'sq': OUT / 'ads' / 'ADC-RN-03-v1' / 'ADC-RN-03-v1-motion-sq.mp4'}
if __name__ == '__main__':
    for f in ONLY:
        c = build(f)
        if MODE == 'preview':
            n = int(c.T / .5)
            print(preview(c, CAP / f'pv_{f}.jpg', [i * .5 + .25 for i in range(n)] , cols=7 if f == 'reel' else 6, scale=.25 if f == 'reel' else .3))
        else:
            NAMES[f].parent.mkdir(parents=True, exist_ok=True)
            render(c, NAMES[f], cover=(OUT / 'ADC-RN-03-v1-capa.jpg', 1.3) if f == 'reel' else None)
            print(NAMES[f])
