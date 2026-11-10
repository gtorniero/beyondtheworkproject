"""Modelo novo dos ADs do Quiddo (10/11): TV e celular reais, sincronizados, na identidade do visual do próprio app.
make(cfg, fmt) devolve a composição (estudio.Comp). cfg: ver qd03.py / qd04.py. Formatos: reel (20 s), feed e sq (13 s, recompostos)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import Comp, ff, svg, frames, render, preview, A, SNAP, BACK, EASE

FONTS = ff('Fraunces', 'Fraunces-900.woff2', '900') + ff('Nunito', 'Nunito-var.woff2', '600 900')
PW_DIP = 390  # largura do celular gravado, em px CSS

def css(p):
    return f"""
.t{{font-family:Fraunces,serif;font-weight:900;letter-spacing:-.02em;color:{p['txt']}}}
.t .hl{{background:{p['hl_bg']};color:{p['hl_fg']};padding:0 .14em;margin:0 -.03em;border-radius:.1em;transform:rotate(-2deg)}}
.bgA{{background-color:{p['bg']};background-image:radial-gradient({p['dot']} 9px,transparent 10px),radial-gradient({p['dot']} 9px,transparent 10px);background-size:120px 120px;background-position:0 0,60px 60px}}
.bgB{{background-color:{p['bg2']};background-image:radial-gradient({p['dot2']} 9px,transparent 10px),radial-gradient({p['dot2']} 9px,transparent 10px);background-size:120px 120px;background-position:0 0,60px 60px}}
.fone{{position:relative;background:{p['ink']};border-radius:76px;box-shadow:0 14px 0 rgba(0,0,0,.28),0 50px 90px rgba(0,0,0,.35)}}
.fone .scr{{position:absolute;left:14px;top:14px;right:14px;bottom:14px;border-radius:62px;overflow:hidden;background:{p['bg2']}}}
.fone img.clip{{height:auto;position:absolute;left:0;top:0}}
.tv{{position:relative;background:{p['ink']};border-radius:30px;padding:14px;box-shadow:0 14px 0 rgba(0,0,0,.28),0 50px 90px rgba(0,0,0,.35)}}
.tv .scr{{position:relative;overflow:hidden;border-radius:18px}}
.tv .pe{{position:absolute;left:50%;bottom:-34px;width:260px;height:34px;margin-left:-130px;background:{p['ink']};clip-path:polygon(22% 0,78% 0,100% 100%,0 100%)}}
.pill{{display:inline-block;font-family:Nunito;font-weight:900;border:6px solid {p['ink']};border-radius:999px;box-shadow:0 9px 0 {p['ink']};background:{p['pill_bg']};color:{p['pill_fg']}}}
"""

def make(cfg, fmt):
    p, m, L = cfg['pal'], cfg['m'], cfg['txt']
    reel = fmt == 'reel'
    c = Comp(fmt, 20 if reel else 13, p['bg'], FONTS, css(p))
    _show = c.show; c.show = lambda t0, t1=None, fin=0.0, fout=0.002: _show(t0, t1, fin, fout)  # contorna show() com fout=0 (quadros-chave duplicados)
    W, H = c.W, c.H
    fd = cfg['frames']  # dict nome → (pasta, src0 do vídeo fonte)
    def clip(nome, src, t0, t1, style=''):
        folder, base = fd[nome]
        return c.clip(folder, src - base, t0, t1, style=style)
    def fone(inner, w, h, extra=''):
        return f'<div class="fone" style="width:{w}px;height:{h}px;{extra}">' + f'<div class="scr">{inner}</div></div>'
    def tv(inner, w):
        return f'<div class="tv" style="width:{w}px"><div class="scr" style="width:{w - 28}px;height:{(w - 28) * 9 / 16:.0f}px">{inner}</div><div class="pe"></div></div>'
    def deco(n, t0, t1, seed=0, ymin=None):
        out = ''
        for i in range(n):
            x = ((seed * 131 + i * 397) % 170 + 15) if i % 2 else (W - 190 + (seed * 53 + i * 211) % 110); y0 = (seed * 71 + i * 263) % max(120, H - 160 - (ymin or (560 if reel else 330))) + (ymin or (560 if reel else 330)); s = 70 + (i * 37) % 80; r = (i * 53) % 40 - 20
            k = c.kf([(t0, f'transform:translateY(40px) rotate({r}deg) scale(.4);opacity:0', BACK), (t0 + .5 + i * .06, f'transform:translateY(0) rotate({r}deg) scale(1);opacity:{p.get("deco_op", .9)}', 'ease-in-out'), (t1, f'transform:translateY(-70px) rotate({r + 10}deg) scale(1);opacity:{p.get("deco_op", .9)}')])
            out += f'<div class="abs" style="left:{x}px;top:{y0}px;width:{s}px;{c.an(k)}">{p["deco"]}</div>'
        return out
    c.add('<div class="fill bgA"></div>')

    # ------------------------------------------------------------ tempos
    if reel:
        tA, tB, tC, tD, tE, tF = 0, 2.5, 6.0, 9.5, 12.0, 17.0
    else:
        tA, tB, tC, tE, tF = 0, 2.2, 4.8, 7.6, 10.6; tD = None
    src_ab = m['q0_resp'] - tB           # o celular mostra "prepare-se" e libera as respostas em tB
    t_tap = m['q0_hero'] - src_ab
    src_c = m['q0_reveal'] - .3
    src_d = m['q0_rank'] + .3
    src_e = cfg['campeao'] - (2.2 if reel else 1.6)
    t_camp = tE + (2.2 if reel else 1.6)

    # ------------------------------------------------------------ layout
    if reel:
        pw, px, py = 440, 320, 1010; tvw, tvx, tvy = 860, 110, 500; ly, ls = 285, 98; hy, hs = 285, 112
        ppw, ppx, ppy = 560, 260, 530
    elif fmt == 'feed':
        pw, px, py = 520, 280, 350; tvw, tvx, tvy = 900, 90, 300; ly, ls = 70, 90; hy, hs = 70, 100
        ppw, ppx, ppy = 540, 270, 320
    else:
        pw, px, py = 470, 305, 270; tvw, tvx, tvy = 960, 60, 330; ly, ls = 52, 78; hy, hs = 52, 84
        ppw, ppx, ppy = 440, 320, 250
    k = (pw - 28) / PW_DIP
    bx = m['box']['q0']; tapx, tapy = 14 + (bx['x'] + bx['width'] / 2) * k, 14 + (bx['y'] + bx['height'] / 2) * k
    ph = H - py + 120  # o celular sai pela base do quadro

    # ------------------------------------------------------------ A+B: gancho → resposta no celular
    hook_dy = -270 if reel else 50
    cam = c.kf([(0, f'transform:translateY({hook_dy + 160}px) rotate(-7deg) scale({1.18 if reel else 1.0})', EASE), (.9, f'transform:translateY({hook_dy}px) rotate(-3deg) scale({1.18 if reel else 1.0})', 'ease-in-out'),
                (tB - .35, f'transform:translateY({hook_dy}px) rotate(-2deg) scale({1.18 if reel else 1.0})', SNAP), (tB + .15, 'transform:none', 'ease-in-out'),
                (t_tap - .55, 'transform:scale(1)', SNAP), (t_tap - .05, 'transform:scale(1.2)', 'ease-in-out'), (t_tap + 1.0, 'transform:scale(1.2)', SNAP), (t_tap + 1.5, 'transform:scale(1)')])
    vis_ab = c.show(0, tC)
    c.add(f'<div class="abs" style="left:{px}px;top:{py}px;transform-origin:{tapx:.0f}px {tapy:.0f}px;z-index:5;{c.an(cam, vis_ab)}">'
          + fone(clip('cel', src_ab, 0, tC, 'width:100%'), pw, ph) + '</div>')
    c.add(c.ring(px + tapx, py + tapy, t_tap, size=170, color=p['ring']).replace('z-index:40', 'z-index:8'))
    if reel:  # a TV desce junto com a pergunta
        tvk = c.kf([(tB - .5, 'transform:perspective(1800px) rotateX(14deg) translateY(-900px)', EASE), (tB + .1, 'transform:perspective(1800px) rotateX(4deg) translateY(0)')])
        c.add(f'<div class="abs" style="left:{tvx}px;top:{tvy}px;z-index:3;{c.an(tvk, c.show(tB - .5, tC))}">{tv(clip("tv", src_ab + .001, tB - .5, tC), tvw)}</div>')
    c.add(c.words(L['hook'], -.3, 60, hy, w=W - 120, size=hs, cls='t', out=tB - .3, step=.09, style='z-index:9;' + ('' if reel else f'text-shadow:0 6px 0 {p["bg"]};')))
    c.add(c.words(L['b'], tB + .25, 60, ly, w=W - 120, size=ls, cls='t', out=tC - .2, style='z-index:9'))

    # ------------------------------------------------------------ C: revelação (TV + celular no reel; TV nos motions)
    tC2 = tD if reel else tE
    punch = lambda t: c.kf([(t - .001, 'transform:scale(1.05)', EASE), (t + .4, 'transform:scale(1)', 'ease-in-out'), (t + 3.4, 'transform:scale(1.04)')])
    c.add(c.flash(tC, p['flash']))
    c.add(f'<div class="abs" style="left:{tvx}px;top:{tvy}px;z-index:3;transform-origin:50% 60%;{c.an(punch(tC), c.show(tC, tC2))}">{tv(clip("tv", src_c, tC, tC2), tvw)}</div>')
    if reel or fmt == 'feed':
        cpx, cpy, cpw = (px, py, pw) if reel else (330, 850, 420)
        c.add(f'<div class="abs" style="left:{cpx}px;top:{cpy}px;z-index:5;transform-origin:50% 20%;{c.an(punch(tC), c.show(tC, tC2))}">' + fone(clip('cel', src_c, tC, tC2, 'width:100%'), cpw, H - cpy + 120) + '</div>')
    c.add(c.words(L['c'], tC + .15, 60, ly, w=W - 120, size=ls, cls='t', out=tC2 - .2, style='z-index:9'))

    # ------------------------------------------------------------ D: ranking (só no reel)
    if reel:
        c.add(c.flash(tD, p['flash'], peak=.5))
        c.add(f'<div class="abs" style="left:{tvx}px;top:{tvy}px;z-index:3;transform-origin:50% 40%;{c.an(punch(tD), c.show(tD, tE))}">{tv(clip("tv", src_d, tD, tE), tvw)}</div>')
        c.add(f'<div class="abs" style="left:{px}px;top:{py}px;z-index:5;transform-origin:50% 20%;{c.an(punch(tD), c.show(tD, tE))}">' + fone(clip('cel', src_d, tD, tE, 'width:100%'), pw, ph) + '</div>')
        c.add(c.words(L['d'], tD + .15, 60, ly, w=W - 120, size=ls, cls='t', out=tE - .25, style='z-index:9'))

    # ------------------------------------------------------------ E: pódio (celular inteiro, confete do próprio app)
    c.add(c.wipe(tE, p['wipe'], dur=.6))
    c.add(f'<div class="fill bgB" style="z-index:10;{c.an(c.show(tE, tF))}">{deco(7, tE + .2, tF, 3)}</div>')
    pk = c.kf([(tE, 'transform:translateY(500px) rotate(-8deg) scale(.9)', BACK), (tE + .7, 'transform:rotate(-2deg) scale(1)', 'ease-in-out'), (t_camp - .1, 'transform:rotate(0deg) scale(1)', SNAP),
               (t_camp + .12, 'transform:rotate(1.5deg) scale(1.09)', BACK), (t_camp + .7, 'transform:rotate(0deg) scale(1.04)', 'ease-in-out'), (tF, 'transform:rotate(-1deg) scale(1.07)')])
    pph = round((ppw - 28) * 1688 / 780 + 28) if reel else H - ppy + 120
    c.add(f'<div class="abs" style="left:{ppx}px;top:{ppy}px;z-index:12;transform-origin:50% 35%;{c.an(pk, c.show(tE, tF))}">' + fone(clip('celp', src_e, tE, tF, 'width:100%'), ppw, pph) + '</div>')
    c.add(c.flash(t_camp, '#fff', dur=.35, peak=.7).replace('z-index:60', 'z-index:13'))
    c.add(c.words(L['e'], tE + .35, 60, ly - (10 if reel else 0), w=W - 120, size=ls + (10 if reel else 0), cls='t tE', out=tF - .25, style=f'z-index:14;color:{p["txt2"]};' + ('' if reel else f'text-shadow:0 5px 0 {p["bg2"]};')))

    # ------------------------------------------------------------ F: CTA (fundo igual ao quadro 0, para o loop)
    c.add(c.wipe(tF, p['wipe2'], dur=.6))
    cy = {'reel': 560, 'feed': 250, 'sq': 150}[fmt]; cs = {'reel': 150, 'feed': 150, 'sq': 132}[fmt]
    logo = svg(A / 'quiddo' / p['logo'], w={'reel': 400, 'feed': 380, 'sq': 320}[fmt])
    c.add(f'<div class="fill bgA" style="z-index:20;{c.an(c.show(tF))}">{deco(6, tF + .2, c.T, 9, ymin=int(cy + cs * 2.6))}'
          + c.words('Faça o seu.\n*Teste grátis.*', tF + .3, 0, cy, w=W, size=cs, cls='t', align='center', step=.11, lh=1.08)
          + f'<div class="abs" style="left:0;right:0;top:{cy + cs * 2.55:.0f}px;text-align:center;{c.an(c.enter(tF + 1.0, "pop", .5))}"><span class="pill" style="font-size:{cs * .38:.0f}px;padding:{cs * .12:.0f}px {cs * .34:.0f}px">quiddo.com.br</span></div>'
          + f'<div class="abs" style="left:0;right:0;top:{cy + cs * 4.0:.0f}px;text-align:center;{c.an(c.enter(tF + 1.25, "rise", .5))}">{logo}</div></div>')
    return c

def prepara(cap, pasta, m, campeao):
    """Extrai só os trechos usados (30 fps). Devolve o dict de clipes para cfg['frames']."""
    a = m['q0_resp'] - 3.0; fim = m['q0_rank'] + 4.0
    cel = frames(Path(cap) / 'cel.mp4', Path(pasta) / 'cel', start=a, dur=fim - a)[0]
    tv = frames(Path(cap) / 'tv.mp4', Path(pasta) / 'tv', start=a, dur=fim - a)[0]
    celp = frames(Path(cap) / 'cel.mp4', Path(pasta) / 'celp', start=campeao - 3.0, dur=9.0)[0]
    return {'cel': (cel, a), 'tv': (tv, a), 'celp': (celp, campeao - 3.0)}

def campeao_t(cap, m):
    """Instante (s) em que o celular revela o campeão: maior salto entre quadros depois de 'podio'."""
    from PIL import Image, ImageChops, ImageStat
    ts = m['frames']['cel']; best, bt, prev = 0, None, None
    for i, t in enumerate(ts):
        if t < m['podio'] + 4 or t > m['fim'] - 3: continue
        im = Image.open(Path(cap) / 'cel' / f'{i:05d}.jpg').convert('L').resize((78, 169)).crop((0, 10, 78, 40))  # faixa do título
        if prev is not None:
            d = ImageStat.Stat(ImageChops.difference(im, prev)).mean[0]
            if d > best: best, bt = d, t
        prev = im
    return bt

def entrega(cfg, ID, ver, out_media, tempos_reel, tempos_motion, prev_dir, so_preview=False):
    out_media = Path(out_media); prev_dir = Path(prev_dir); prev_dir.mkdir(parents=True, exist_ok=True)
    for fmt, nome in (('reel', out_media / f'{ID}-{ver}.mp4'), ('feed', out_media / 'ads' / f'{ID}-{ver}' / f'{ID}-{ver}-motion-feed45.mp4'), ('sq', out_media / 'ads' / f'{ID}-{ver}' / f'{ID}-{ver}-motion-sq.mp4')):
        c = make(cfg, fmt)
        if so_preview:
            preview(c, prev_dir / f'{ID}-{fmt}.jpg', tempos_reel if fmt == 'reel' else tempos_motion, cols=10 if fmt == 'reel' else 8, scale=.18 if fmt == 'reel' else .22)
        else:
            render(c, nome, cover=(out_media / f'{ID}-{ver}-capa.jpg', cfg['capa_t']) if fmt == 'reel' else None)
            print('ok', nome, flush=True)
