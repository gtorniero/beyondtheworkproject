"""v7 (10/11, linha corporativa QD-07/08/09): igual ao v6 + cena opcional da TV do anfitrião (foto real da tela, cfg["tv"]) no lugar do ranking, com big number (cfg["tvbig"]), e estáticos (estatico()).
v6 (10/11, QD-01 v5 reprovado: "animações muito rápidas, não dá pra entender msg, tem que deixar ler melhor"): mesma captura fluida, tempos mais longos (reel 25 s, motions 15 s), câmera mais lenta, textos entrando em 0,7 s, cada tela parada ≥ 1,2 s após a animação.
, "tela do jogo travando… mais curto ou simples"): só o celular do jogador, captura fluida (qd_cap3 + qd_remap: animações gravadas em câmera lenta real e devolvidas à velocidade do app, ≥ 30 quadros reais/s), 4 cenas: toque → Mandou bem → ranking → pódio → CTA. Reel 17 s, motions 11 s. Celular menor (proporção real da tela).
Base: ADs do Quiddo na REFERÊNCIA OFICIAL (ADC-RZ-08): celular do jogador grande e central, câmera entrando no toque,
fundo vivo com blobs na paleta do visual do app, título Fraunces enorme, big numbers reais da partida e assets do site
(bichos do avatarSvg, símbolos das respostas, logo). A TV do anfitrião entra como inserção na revelação (só no reel).
Captura: qd_cap2.py <partida.json> <pasta> e depois qd_cap2.py --cfr <pasta> (celular 780 px de largura; acima disso o screencast cai para 2 a 6 quadros/s nesta máquina).
Uso (pelos arquivos por AD, ex. qd03_ref.py): entrega(cfg, sys.argv)  →  args: <captura> <trabalho> [reel|feed|sq|all] [preview|podio]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import *

AQ = A / 'quiddo'
ART = json.loads((AQ / 'art.json').read_text())
FONTS = ff('Fraunces', 'Fraunces-900.woff2', '900') + ff('Nunito', 'Nunito-var.woff2', '600 900')
RESP = ['#13A07A', '#FF7A1A', '#1E7FD6', '#E5383B']  # folha, sol, gota, flor (cores das respostas do site)
ASP = 2336 / 1080  # tela do celular gravado

LAY = {  # vp = recorte onde o celular vive; ph = (x, y, largura); q = ponto para onde o zoom leva o foco; tx = (x, y, largura) do título
    'reel': dict(vp=(0, 0, 1080, 1920), ph=(210, 640, 660), q=(540, 1180), tx=(70, 285, 960), ts=116, z=.5, scrim=680),
    'feed': dict(vp=(0, 0, 1080, 1350), ph=(275, 360, 530), q=(540, 900), tx=(60, 62, 980), ts=98, z=.5, scrim=360),
    'sq':   dict(vp=(500, 0, 580, 1080), ph=(60, 80, 460), q=(290, 560), tx=(54, 150, 440), ts=80, z=.5, scrim=0),
}


_AV = [0]
def av(key, size):
    """Bicho oficial (avatarSvg do site). Os ids internos do SVG ganham sufixo: o mesmo bicho pode aparecer duas vezes na página."""
    import re
    _AV[0] += 1; u = f'_{_AV[0]}'
    s = ART['av'][key].replace('width="120" height="120"', f'width="{size}" height="{size}"')
    s = re.sub(r'id="([^"]+)"', lambda m: f'id="{m.group(1)}{u}"', s); s = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{m.group(1)}{u})', s); s = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{m.group(1)}{u}"', s)
    return f'<span style="display:inline-block;width:{size}px;height:{size}px">{s}</span>'


def sym(k, size, color):
    return ART['sim'][k].replace('class="sym"', f'class="sym" style="width:{size}px;height:{size}px;color:{color}"')


def css(p):
    return f"""
.hd{{font-family:Fraunces,serif;font-weight:900;letter-spacing:-.025em;color:{p['txt']};z-index:30}}
.hd .hl{{background:{p['hl_bg']};color:{p['hl_fg']};padding:0 .13em;margin:0 -.02em;border-radius:.09em;transform:rotate(-2deg)}}
.blob{{position:absolute;border-radius:50%;filter:blur(120px)}}
.fone{{position:relative;background:{p['ink']};box-shadow:0 18px 0 rgba(0,0,0,.3),0 60px 110px rgba(0,0,0,.4)}}
.fone .scr{{position:absolute;overflow:hidden;background:{p.get('scr', '#fff')}}}
.tv{{position:relative;background:{p['ink']};border-radius:34px;padding:16px;box-shadow:0 18px 0 rgba(0,0,0,.3),0 60px 110px rgba(0,0,0,.4)}}
.tv .scr{{position:relative;overflow:hidden;border-radius:20px}}
.pill{{display:inline-block;white-space:nowrap;font-family:Nunito,sans-serif;font-weight:900;border:6px solid {p['ink']};border-radius:999px;box-shadow:0 10px 0 {p['ink']};background:{p['pill_bg']};color:{p['pill_fg']}}}
.bicho{{filter:drop-shadow(0 10px 0 rgba(0,0,0,.28))}}
"""


def prepara(cap, work, m, camp):
    """Trechos do celular (cel.mp4 já no tempo real do app, ver qd_remap.py). Devolve {nome: (pasta, início no vídeo fonte)}."""
    cap, work = Path(cap), Path(work); out = {}
    for nome, a, d in [('a', m['q0_hero'] - 4.6, 8.0), ('c', m['q0_reveal'] - 1.0, 7.0), ('d', m['q0_rank'] - .6, 6.0), ('e', camp - 3.5, 9.0)]:
        out[nome] = (frames(cap / 'cel.mp4', work / nome, start=a, dur=d)[0], a)
    return out


def make(cfg, fmt):
    p, m, X, N = cfg['pal'], cfg['m'], cfg['txt'], cfg['num']
    L = LAY[fmt]; reel = fmt == 'reel'
    T = 25.0 if reel else 15.0
    c = Comp(fmt, T, p['bg'], FONTS, css(p))
    fd = cfg['frames']
    px, py, pw = L['ph']; b = 16; sw = pw - 2 * b; sh = sw * ASP; qx, qy = L['q']; rad = round(pw * .125)

    def clip(nome, src, t0, t1): folder, base = fd[nome]; return c.clip(folder, src - base, t0, t1)

    def fone(inner, w):
        s_w = w - 2 * b
        return (f'<div class="fone" style="width:{w}px;height:{s_w * ASP + 2 * b:.0f}px;border-radius:{rad}px">'
                f'<div class="scr" style="left:{b}px;top:{b}px;width:{s_w}px;height:{s_w * ASP:.0f}px;border-radius:{rad - b}px">{inner}</div></div>')

    def cam(fx=None, fy=None, s=1.0, dx=0, dy=0):
        if fx is None: return f'transform:translate({dx}px,{dy}px) scale({s})'
        s = 1 + (s - 1) * L['z']
        return f'transform:translate({qx - px - s * (b + sw * fx) + dx:.1f}px,{qy - py - s * (b + sh * fy) + dy:.1f}px) scale({s:.3f})'

    def rot(y=0, x=0, z=0): return f'transform:perspective(2400px) rotateY({y}deg) rotateX({x}deg) rotateZ({z}deg)'

    def shot(t0, t1, nome, src0, cams, rots=None):
        k = c.kf(cams, EASE); r = c.kf(rots or [(t0, rot())], EASE)
        return (f'<div class="abs" style="left:{px}px;top:{py}px;transform-origin:0 0;{c.an(k, c.show(t0, t1))}">'
                f'<div style="transform-origin:50% 40%;{c.an(r)}">{fone(clip(nome, src0, t0, t1), pw)}</div></div>')

    def txt(s, t, out, size=None, **kw):
        x, y, w = L['tx']
        return c.words(s, t, x, y, w, size=size or L['ts'], cls='hd', out=out, lh=1.0, **kw)

    def big(t, out, a, bnum, pre='', suf='', fmtn='int', linha='', dur=1.1, antes=''):
        """Big number: número real da partida rodando, em destaque, + uma linha de texto."""
        x, y, w = L['tx']; s = L['ts']
        e1 = c.an(c.enter(t, 'pop', .7)); e2 = c.an(c.enter(t + .3, 'rise', .7, dist=40)); o = c.an(c.exit(out, 'up', .35, 40))
        top = f'<span class="ln"><span class="w" style="{c.an(c.enter(t - .05, "rise", .4, dist=40))}">{antes}</span></span>' if antes else ''
        return (f'<div class="hd" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{s}px;line-height:1.0;{o}">{top}'
                f'<span class="ln"><span class="w hl" style="font-size:{1.0 if antes else 1.5}em;{e1}">{c.count(a, bnum, t, t + dur, fmt=fmtn, pre=pre, suf=suf)}</span>'
                + (f' <span class="w" style="{e2}">{linha}</span>' if antes else '') + '</span>'
                + ('' if antes else f'<span class="ln" style="margin-top:.14em;font-size:{.6 if fmt == 'sq' else .82}em"><span class="w" style="{e2}">{linha}</span></span>') + '</div>')

    # ---------------------------------------------------------------- fundo vivo + símbolos das respostas (assets do site)
    d1 = c.kf([(0, 'transform:translate(0,0)'), (T / 2, 'transform:translate(170px,130px)', 'ease-in-out'), (T, 'transform:translate(0,0)')], 'ease-in-out')
    d2 = c.kf([(0, 'transform:translate(0,0)'), (T / 2, 'transform:translate(-150px,-170px)', 'ease-in-out'), (T, 'transform:translate(0,0)')], 'ease-in-out')
    blobs = (f'<div class="blob" style="left:-280px;top:{c.H * .22:.0f}px;width:780px;height:780px;background:{p["blob1"]};opacity:{p.get("b1o", .55)};{c.an(d1)}"></div>'
             f'<div class="blob" style="right:-300px;top:{c.H * .58:.0f}px;width:820px;height:820px;background:{p["blob2"]};opacity:{p.get("b2o", .45)};{c.an(d2)}"></div>')
    c.add(blobs)
    sy = []
    for i, (x, y, s) in enumerate([(36, .40, 120), (c.W - 150, .50, 130), (20, .72, 110), (c.W - 140, .30, 100)]):
        if fmt == 'sq': x, y = [(40, .62, 0), (330, .78, 0), (190, .70, 0), (400, .60, 0)][i][:2]
        k = c.kf([(0, f'transform:translateY(0) rotate({-12 + i * 9}deg)'), (T / 2, f'transform:translateY({-50 if i % 2 else 50}px) rotate({8 - i * 6}deg)', 'ease-in-out'), (T, f'transform:translateY(0) rotate({-12 + i * 9}deg)')], 'ease-in-out')
        sy.append(f'<div class="abs" style="left:{x}px;top:{c.H * y:.0f}px;opacity:{p.get("sym_op", .5)};{c.an(k)}">{sym(i, s, p.get("sym_cor", [None] * 4)[i] or RESP[i])}</div>')
    c.add(''.join(sy))

    # ---------------------------------------------------------------- tempos
    fyb = (cfg['box']['y'] + cfg['box']['height'] / 2) / 844   # resposta tocada
    F = dict(rev=.2, rank=.2, pod=.36, fim=.47); F.update(cfg.get('foco', {}))
    t_tap = 4.0 if reel else 3.9
    if reel: tB, tC, tD, tE = 6.5, 10.7, 14.9, 21.1
    else: tB, tD, tE = 6.0, 9.2, 13.0; tC = None
    a0 = m['q0_hero'] - t_tap
    r0 = m['q0_reveal'] + cfg.get('rev_lag', .6) - .5 - tB   # src = r0 + t; o celular mostra o resultado ~1,5 s depois da marca da TV
    camp_at = 1.9 if reel else .7; t_camp = tD + camp_at
    e0 = cfg['campeao'] - t_camp             # src = e0 + t
    vx, vy, vw, vh = L['vp']
    stage = []
    # 1 · gancho + toque
    stage.append(shot(0, tB, 'a', a0,
                      [(0, cam(.5, .3, .94)), (1.3, cam(.5, .3, 1.12)), (t_tap - .9, cam(.5, .3, 1.16)), (t_tap - .1, cam(.5, fyb, 1.36)), (t_tap + .2, cam(.5, fyb, 1.4)), (t_tap + 1.3, cam(.5, .3, 1.2)), (tB, cam(.5, .3, 1.22))],
                      [(0, rot(-14, 6, -2)), (1.3, rot(0, 0, 0))]))
    # 2 · revelação no celular (+ TV entrando por trás no reel)
    if reel:
        stage.append(shot(tB, tC, 'c', r0 + tB,
                          [(tB, cam(.5, F['rev'], 1.4)), (tB + 1.0, cam(.5, F['rev'], 1.3)), (tC, cam(.5, F['rev'], 1.33))],
                          [(tB, rot(5, 0, 0)), (tB + 1.2, rot(0, 0, 0))]))
        # 3 · ranking
        d0 = m['q0_rank'] + .25 - tC
        if cfg.get('tv'):
            tw = vw - 40; fx, fy = cfg.get('tv_foco', (.5, .55))
            k = c.kf([(tC, 'transform:perspective(2400px) rotateX(10deg) scale(.9);opacity:.2', EASE), (tC + .9, 'transform:perspective(2400px) rotateX(0deg) scale(1.08);opacity:1'),
                      (tC + 2.0, 'transform:perspective(2400px) rotateX(0deg) scale(1.1);opacity:1', EASE), (tC + 3.2, 'transform:perspective(2400px) rotateX(0deg) scale(1.3);opacity:1'), (tD, 'transform:perspective(2400px) rotateX(0deg) scale(1.32);opacity:1')])
            stage.append(f'<div class="abs" style="left:20px;top:{820 if reel else 430}px;width:{tw}px;z-index:5;transform-origin:{fx * 100:.0f}% {fy * 100:.0f}%;{c.an(k, c.show(tC, tD))}"><div class="tv"><div class="scr"><img src="{Path(cfg["tv"]).resolve().as_uri()}" style="display:block;width:100%"></div></div></div>')
        else:
          stage.append(shot(tC, tD, 'd', d0 + tC,
                            [(tC, cam(.5, F['rank'], 1.6)), (tC + 1.0, cam(.5, F['rank'], 1.48)), (tC + 2.2, cam(.5, F['rank'], 1.5)), (tC + 3.1, cam(.5, F['rank'] + .26, 1.3)), (tD, cam(.5, F['rank'] + .27, 1.31))],
                            [(tC, rot(-6, 0, 0)), (tC + 1.2, rot(0, 0, 0))]))
    else:
        stage.append(shot(tB, tD, 'c', r0 + tB,
                          [(tB, cam(.5, F['rev'], 1.6)), (tB + 1.0, cam(.5, F['rev'], 1.48)), (tD, cam(.5, F['rev'], 1.5))], [(tB, rot(5, 0, 0)), (tB + 1.2, rot(0, 0, 0))]))
    # 4 · pódio
    stage.append(shot(tD, tE, 'e', e0 + tD,
                      [(tD, cam(.5, F['pod'], 1.45)), (tD + 1.0, cam(.5, F['pod'], 1.34)), (t_camp, cam(.5, F['pod'], 1.36)), (t_camp + .8, cam(.5, F['pod'], 1.44)), (t_camp + 2.2, cam(.5, F['pod'], 1.42)), (t_camp + 3.2, cam(.5, F['fim'], 1.32)), (tE, cam(.5, F['fim'], 1.33))],
                      [(tD, rot(0, 5, 0)), (tD + 1.2, rot(0, 0, 0))]))
    c.add(f'<div class="abs" style="left:{vx}px;top:{vy}px;width:{vw}px;height:{vh}px;overflow:hidden">{"".join(stage)}</div>')
    if L['scrim']:
        c.add(f'<div class="abs" style="left:0;top:0;width:100%;height:{L["scrim"]}px;z-index:20;background:linear-gradient({p["bg"]} 0%,{p["bg"]} 84%,{p["bg0"]});{c.an(c.show(0, tE))}"></div>')

    # bichos do site comemorando ao lado do celular, no pódio
    if fmt != 'sq':
        for i, (key, side) in enumerate(cfg['bichos'][:2]):
            x = 14 if side == 'l' else c.W - 184; y = (1180 if reel else 880) + i * 120
            k = c.kf([(t_camp + .15 + i * .12, f'transform:translateX({-200 if side == "l" else 200}px) rotate(0deg)', BACK), (t_camp + .7 + i * .12, f'transform:translateX(0) rotate({-10 if side == "l" else 10}deg)', 'ease-in-out'), (tE, f'transform:translateX(0) rotate({6 if side == "l" else -6}deg)')])
            c.add(f'<div class="abs bicho" style="left:{x}px;top:{y}px;z-index:25;{c.an(k, c.show(t_camp + .1, tE))}">{av(key, 170)}</div>')

    # toque e flashes
    s_tap = 1 + (1.56 - 1) * L['z']
    bx = (cfg['box']['x'] + cfg['box']['width'] * .5) / 390
    c.add(c.ring(vx + qx + s_tap * (bx - .5) * sw, vy + qy, t_tap, size=190, color=p['ring']))
    c.add(c.flash(t_tap + .1, p['flash'], .4, .35)); c.add(c.flash(t_camp + .05, '#fff', .45, .45))

    # ---------------------------------------------------------------- títulos e big numbers
    c.add(txt(X['hook'], -.3, t_tap + .4, step=.1, dur=.7))
    c.add(txt(X['b'], t_tap + .7, tB - .3, step=.12, dur=.7))
    c.add(c.wipe(tB, p['wipe'], .7, 'up'))
    if reel:
        c.add(big(tB + .6, tC - .3, 0, N['pts'], pre='+', linha=X['pts'], fmtn='mil', dur=1.4))
        c.add(c.wipe(tC, p['wipe2'], .7, 'left'))
        if cfg.get('tvbig'):
            nb, lb, pre, suf = cfg['tvbig']; c.add(big(tC + .5, tD - .3, 0, nb, pre=pre, suf=suf, linha=lb, dur=1.4))
        else: c.add(txt(X['d'], tC + .4, tD - .3, step=.12, dur=.7))
    else:
        c.add(big(tB + .6, tD - .3, 0, N['pts'], pre='+', linha=X['pts'], fmtn='mil', dur=1.4))
    c.add(c.wipe(tD, p['wipe3'], .7, 'up'))
    # total do pódio: a contagem termina ≥ 1 s antes da saída, para o último quadro mostrar o valor exato da tela
    tt = t_camp + .6; dur_t = max(.6, min(1.2, tE - 1.3 - tt))
    c.add(txt(X['e'], tD + .4, tt - .05 if reel else tE - .3, step=.12, dur=.7))
    if reel: c.add(big(tt, tE - .3, 0, N['total'], linha=X['total'], fmtn='mil', dur=dur_t))  # no motion o título fica até o fim (tempo de leitura)

    # ---------------------------------------------------------------- CTA
    c.add(c.wipe(tE, p['hl_bg'], .7, 'up'))
    cx = 90 if fmt != 'sq' else 80; cy = {'reel': 560, 'feed': 300, 'sq': 190}[fmt]; cs = {'reel': 150, 'feed': 136, 'sq': 112}[fmt]
    end = c.show(tE)
    row = ''
    for i, (key, _) in enumerate(cfg['bichos'][:4]):
        k = c.kf([(tE + .5 + i * .1, 'transform:translateY(160px) scale(.5);opacity:0', BACK), (tE + 1.0 + i * .1, f'transform:translateY(0) rotate({(-1) ** i * 7}deg) scale(1);opacity:1', 'ease-in-out'), (T, f'transform:translateY(-14px) rotate({(-1) ** i * -4}deg) scale(1);opacity:1')])
        row += f'<div class="bicho" style="{c.an(k)}">{av(key, {"reel": 200, "feed": 170, "sq": 150}[fmt])}</div>'
    c.add(f'<div class="fill" style="background:{p["bg"]};z-index:45;{c.an(end)}">{blobs}'
          f'<div class="abs" style="left:{cx}px;top:{cy - cs * 1.25:.0f}px;{c.an(c.enter(tE + .15, "left", .45))}">{svg(AQ / p["logo"], h=round(cs * .82))}</div>'
          + c.words('Faça o seu.\n*Teste grátis.*', tE + .3, cx, cy, c.W - 2 * cx, size=cs, cls='hd', step=.12, dur=.7, lh=1.06)
          + f'<div class="abs" style="left:{cx}px;top:{cy + cs * 2.55:.0f}px;{c.an(c.enter(tE + 1.0, "pop", .45))}"><span class="pill" style="font-size:{cs * .4:.0f}px;padding:{cs * .14:.0f}px {cs * .36:.0f}px">quiddo.com.br</span></div>'
          f'<div class="abs" style="left:{cx - 10}px;right:{cx - 10}px;top:{cy + cs * 3.75:.0f}px;display:flex;justify-content:space-between">{row}</div>'
          f'</div>')
    return c


def entrega(cfg_fn, argv):
    """cfg_fn(m, cap, work) → cfg. argv: <captura> <trabalho> [reel|feed|sq|all] [preview|podio]"""
    cap, work = Path(argv[1]), Path(argv[2]); which = argv[3] if len(argv) > 3 else 'all'; modo = argv[4] if len(argv) > 4 else ''
    m = json.loads((cap / 'marcas.json').read_text())
    if modo == 'podio':  # folha do celular no pódio, 1 quadro a cada 0,5 s, para achar o instante do campeão
        from PIL import Image
        fo, n = frames(cap / 'cel.mp4', work / 'podio', start=m['podio'], dur=m['fim'] - m['podio'], width=270, fps=2)
        ims = [Image.open(f) for f in sorted(fo.glob('*.jpg'))]; cols = 12; rows = (len(ims) + cols - 1) // cols
        shp = Image.new('RGB', (cols * 276, rows * (ims[0].height + 6)), '#777')
        for i, im in enumerate(ims): shp.paste(im, ((i % cols) * 276, (i // cols) * (im.height + 6)))
        shp.save(work / 'podio.jpg'); print(work / 'podio.jpg', 'podio em', m['podio'], '· quadro i = podio + i*0,5 s'); return
    cfg = cfg_fn(m); cfg['m'] = m; cfg['box'] = m['box']['q0']; cfg['frames'] = prepara(cap, work, m, cfg['campeao'])
    V = f"{cfg['id']}-{cfg['ver']}"; out = Path(__file__).resolve().parent.parent.parent / 'out' / 'media'
    for fmt in (['reel', 'feed', 'sq'] if which == 'all' else [which]):
        c = make(cfg, fmt)
        if modo == 'preview':
            print(preview(c, work / f'prev_{fmt}.jpg', [i * .5 + .25 for i in range(int(c.T * 2))], cols=10, scale=.2 if fmt == 'reel' else .25))
        elif fmt == 'reel':
            render(c, out / f'{V}.mp4', cover=(out / f'{V}-capa.jpg', cfg.get('capa_t', 1.7))); (out / f'{V}.html').unlink(missing_ok=True)
        else:
            d = out / 'ads' / V; d.mkdir(parents=True, exist_ok=True); f = d / f'{V}-motion-{"feed45" if fmt == "feed" else "sq"}.mp4'
            render(c, f); f.with_suffix('.html').unlink(missing_ok=True)


FMT['story'] = FMT['reel']; FMT['land'] = (1200, 628, 40, 40)
SLAY = {  # ph=(x,y,largura do celular), tx=(x,y,largura,tamanho), cta=(x,y,tamanho)
    'feed': dict(ph=(570, 250, 430), tx=(64, 120, 480, 88), cta=(64, 1010, 64)),
    'sq':   dict(ph=(600, 120, 400), tx=(56, 96, 520, 82), cta=(56, 800, 58)),
    'reel': dict(ph=(580, 790, 410), tx=(70, 290, 940, 104), cta=(70, 1230, 72)),
    'land': dict(ph=(900, 46, 230), tx=(48, 64, 780, 70), cta=(48, 440, 50)),
}


def estatico(cfg, fmt, still, out_png, hook=None):
    """Estático real: título do gancho + celular com uma tela real do jogo (still) + CTA, no visual do AD."""
    import asyncio
    from playwright.async_api import async_playwright
    p = cfg['pal']; L = SLAY[fmt]; key = 'story' if fmt == 'reel' else fmt
    c = Comp(key, 1, p['bg'], FONTS, css(p)); W, H = c.W, c.H
    c.add(f'<div class="blob" style="left:-260px;top:{H * .2:.0f}px;width:{W * .7:.0f}px;height:{W * .7:.0f}px;background:{p["blob1"]};opacity:{p.get("b1o", .55)}"></div>'
          f'<div class="blob" style="right:-280px;top:{H * .55:.0f}px;width:{W * .75:.0f}px;height:{W * .75:.0f}px;background:{p["blob2"]};opacity:{p.get("b2o", .45)}"></div>')
    for i, (x, y, sz) in enumerate([(.04, .62, .1), (.44, .86, .09), (.9, .1, .08)]):
        c.add(f'<div class="abs" style="left:{W * x:.0f}px;top:{H * y:.0f}px;opacity:{p.get("sym_op", .5)};transform:rotate({-12 + i * 14}deg)">{sym(i, round(W * sz), RESP[i])}</div>')
    px, py, pw = L['ph']; b = max(8, round(pw * .024)); sw = pw - 2 * b; rad = round(pw * .125)
    c.add(f'<div class="abs" style="left:{px}px;top:{py}px;transform:perspective(2400px) rotateY(-8deg) rotateZ(2deg)"><div class="fone" style="width:{pw}px;height:{sw * ASP + 2 * b:.0f}px;border-radius:{rad}px">'
          f'<div class="scr" style="left:{b}px;top:{b}px;width:{sw}px;height:{sw * ASP:.0f}px;border-radius:{rad - b}px"><img src="{Path(still).resolve().as_uri()}" style="display:block;width:100%;height:100%;object-fit:cover;object-position:top"></div></div></div>')
    tx, ty, tw, ts = L['tx']
    c.add(c.words(hook or cfg['txt']['hook'], -2, tx, ty, tw, size=ts, cls='hd', step=0, dur=.01, lh=1.02))
    cx, cy, cs = L['cta']
    logo = svg(AQ / p['logo'], h=round(cs * .7))
    bichos = ''.join(f'<span class="bicho" style="display:inline-block;transform:rotate({(-1) ** i * 7}deg);margin-right:{cs * .1:.0f}px">{av(k, round(cs * 1.25))}</span>' for i, (k, _) in enumerate(cfg['bichos'][:3]))
    if True:
        c.add(f'<div class="abs" style="left:{cx}px;top:{cy}px;z-index:40">'
              f'<div class="hd" style="font-size:{cs}px;line-height:1.05">Faça o seu.<br><span class="hl" style="display:inline-block">Teste grátis.</span></div>'
              f'<div style="margin-top:{cs * .35:.0f}px;display:flex;align-items:center;gap:{cs * .3:.0f}px"><span class="pill" style="font-size:{cs * .42:.0f}px;padding:{cs * .12:.0f}px {cs * .34:.0f}px">quiddo.com.br</span>{logo if fmt != "land" else ""}</div></div>')
        if fmt != 'land': c.add(f'<div class="abs" style="left:{cx}px;top:{cy - cs * 1.55:.0f}px;z-index:40">{bichos}</div>')
    hp = Path(out_png).with_suffix('.html'); hp.write_text(c.html())
    async def go():
        async with async_playwright() as pw_:
            br = await pw_.chromium.launch(args=['--allow-file-access-from-files']); pg = await br.new_page(viewport={'width': W, 'height': H})
            await pg.goto(hp.as_uri()); await pg.evaluate('document.fonts.ready'); await pg.evaluate('seek(0.5)'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(out_png)); await br.close()
    asyncio.run(go()); hp.unlink()
