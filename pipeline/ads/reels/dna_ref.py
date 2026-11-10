"""SPORT DNA na referência do Gui (ADC-RZ-08): celular grande em perspectiva com a tela real do teste, câmera entrando no toque,
fundo preto com luz na cor do esporte, título enorme e BIG NUMBERS do motor e da recomendação (Syne 800, rodando com count()).
Um arquivo curto por AD (rn03.py, rk01.py, sf03.py) define o dicionário D e chama main(D).
Uso: python3 <ad>.py <pasta de quadros 30 fps> <saida media> [reel|feed|sq|all] [preview]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import *

INK, OFF, MUTED = '#0A0A0A', '#F4F4F2', '#A3A3A0'
SD = A / 'sportdna'
FONTS = ff('Archivo', 'Archivo-800.woff2', '800') + ff('Syne', 'Syne-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700') + ff('JetBrains Mono', 'JBMono-var.woff2', '400 700')

LAY = {  # vp = recorte onde o celular vive; ph = (x, y, largura); q = para onde o zoom leva o foco; tx = título; nb = faixa dos números (x, y, w, corpo)
    'reel': dict(vp=(0, 0, 1080, 1920), ph=(160, 570, 760), q=(540, 1010), q3=950, tx=(70, 285, 940), ts=104, z=1.0, scrim=700, nb=(70, 1250, 940, 240), wall=(90, 560, 200)),
    'feed': dict(vp=(0, 0, 1080, 1350), ph=(240, 300, 600), q=(540, 700), q3=670, tx=(60, 62, 960), ts=92, z=.9, scrim=340, nb=(60, 1000, 960, 210), wall=(80, 330, 150)),
    'sq':   dict(vp=(520, 0, 560, 1080), ph=(50, 70, 460), q=(280, 500), q3=470, tx=(56, 96, 470), ts=70, z=.8, scrim=0, nb=(56, 540, 450, 150), wall=(70, 210, 110)),
}


def build(D, fmt, FR):
    L = LAY[fmt]; reel = fmt == 'reel'; C = D['color']
    T = 20.5 if reel else 12.0
    css = f"""
.hd{{font-family:Archivo,sans-serif;font-weight:800;letter-spacing:-.03em;color:#fff;z-index:30;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.hl{{color:{C}}}
.num{{font-family:Syne,sans-serif;font-weight:800;letter-spacing:-.04em;line-height:.9;color:{C}}}
.lab{{font-family:'DM Sans',sans-serif;font-weight:700;color:#fff;line-height:1.15}}
.kick{{font-family:'JetBrains Mono',monospace;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:{MUTED}}}
.url{{font-family:'DM Sans',sans-serif;font-weight:700;background:{C};color:{INK};border-radius:14px;display:inline-block;white-space:nowrap}}
.chip{{font-family:'DM Sans',sans-serif;font-weight:700;background:{C};color:{INK};border-radius:16px;display:inline-block}}
.blob{{position:absolute;border-radius:50%;filter:blur(130px)}}
.ph{{box-shadow:0 0 0 3px rgba(255,255,255,.3),0 0 110px {C}55,0 60px 120px rgba(0,0,0,.6)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.05) 2px,transparent 2px);background-size:90px 90px}}
"""
    c = Comp(fmt, T, INK, FONTS, css)
    px, py, pw = L['ph']; b = 16; sw = pw - 2 * b; sh = sw * 16 / 9; qx, qy = L['q']; vx, vy, vw, vh = L['vp']

    def S(s): return 1 + (s - 1) * L['z']

    def cam(fx=None, fy=None, s=1.0, q=None):
        if fx is None: return f'transform:translate(0px,0px) scale({s})'
        s = S(s); y = q or qy
        return f'transform:translate({qx - px - s * (b + sw * fx):.1f}px,{y - py - s * (b + sh * fy):.1f}px) scale({s:.3f})'

    def rot(y=0, x=0, z=0): return f'transform:perspective(2400px) rotateY({y}deg) rotateX({x}deg) rotateZ({z}deg)'

    def shot(t0, t1, src0, cams, rots=None, rate=1.0):
        k = c.kf(cams, EASE); r = c.kf(rots or [(t0, rot())], EASE)
        return (f'<div class="abs" style="left:{px}px;top:{py}px;transform-origin:0 0;{c.an(k, c.show(t0, t1))}">'
                f'<div style="transform-origin:50% 50%;{c.an(r)}">{c.phone(c.clip(FR, src0, t0, t1, rate), pw, frame="#1d1d1f")}</div></div>')

    def txt(s, t, out, size=None, **kw):
        x, y, w = L['tx']
        return c.words(s, t, x, y, w, size=size or L['ts'], cls='hd', out=out, lh=1.0, **kw)

    def bscrim(t0, t1, y_solid, fade=110):  # preto por baixo: esconde o que não é foco (e o botão com preço) e dá base aos números
        y0 = max(0, y_solid - fade)
        return (f'<div class="abs" style="left:{vx}px;width:{vw}px;top:{vy + y0:.0f}px;bottom:0;z-index:21;'
                f'background:linear-gradient(rgba(10,10,10,0) 0px,{INK} {fade}px);{c.an(c.show(t0, t1))}"></div>')

    nx, ny, nw, ns = L['nb']

    def bignum(val, t0, t1, label, fmtn='int', suf='', dur=1.3, size=None):
        size = size or ns
        e = c.an(c.show(t0, t1), c.enter(t0, 'rise', .4, 50))
        return (f'<div class="abs" style="left:{nx}px;top:{ny}px;width:{nw}px;z-index:32;{e}">'
                f'<div class="num" style="font-size:{size}px">{c.count(0, val, t0 + .05, t0 + dur, fmt=fmtn, suf=suf)}</div>'
                f'<div class="lab" style="font-size:{max(30, size * .19):.0f}px;margin-top:{size * .05:.0f}px">{label}</div></div>')

    # ---- fundo vivo: preto, grade técnica e luz na cor do esporte
    d1 = c.kf([(0, 'transform:translate(0,0)'), (T / 2, 'transform:translate(170px,120px)', 'ease-in-out'), (T, 'transform:translate(0,0)')], 'ease-in-out')
    d2 = c.kf([(0, 'transform:translate(0,0)'), (T / 2, 'transform:translate(-150px,-160px)', 'ease-in-out'), (T, 'transform:translate(0,0)')], 'ease-in-out')
    c.add(f'<div class="grid"></div><div class="blob" style="left:-280px;top:{c.H * .22:.0f}px;width:780px;height:780px;background:{C};opacity:.34;{c.an(d1)}"></div>'
          f'<div class="blob" style="right:-320px;top:{c.H * .6:.0f}px;width:820px;height:820px;background:{D.get("color2", "#0E4D64")};opacity:.5;{c.an(d2)}"></div>')

    # ---- tempos
    if reel: t_i2, t_mot, t_wall, t_top, t_why, t_cta = 2.6, 4.6, 7.2, 9.6, 14.2, 17.5
    else:    t_i2, t_mot, t_wall, t_top, t_why, t_cta = None, 2.8, None, 5.2, None, 9.0
    stage = []
    # 1 · gancho: o dedo no teste (toque em 1.5)
    fx0, fy = D['hook_f']; tap = 1.5; fx = .5 + (fx0 - .5) * .35
    stage.append(shot(0, t_i2 or t_mot, D['hook_tap'] - tap,
                      [(0, cam(.5, .5, .92)), (.85, cam(), SNAP), (1.15, cam(), SNAP), (1.6, cam(fx, fy, 1.26)), (t_i2 or t_mot, cam(fx, fy, 1.34))],
                      [(0, rot(-22, 10, -3)), (.85, rot(-6, 3, 0)), (1.6, rot(0, 0, 0))]))
    c.add(c.ring(vx + qx + S(1.26) * (fx0 - fx) * sw, vy + qy, tap, size=170, color=C))
    c.add(txt(D['hook'], -.3, (t_i2 or t_mot) - .22, step=.06, dur=.4))
    if reel:
        # 2 · segunda interação (toque em t_i2 + .8)
        fx2, fy2 = D['i2_f']; tap2 = t_i2 + .8
        stage.append(shot(t_i2, t_mot, D['i2_tap'] - .8,
                          [(t_i2, cam(fx2, fy2, 1.5)), (t_i2 + .4, cam(fx2, fy2, 1.24)), (t_mot, cam(fx2, fy2, 1.32))], [(t_i2, rot(9, 0, 0)), (t_mot, rot(3, 0, 0))]))
        c.add(c.flash(t_i2, C, .2, .4)); c.add(c.ring(vx + qx, vy + qy, tap2, size=170, color=C))
        c.add(txt(D['i2'], t_i2 + .1, t_mot - .22))
    # 3 · o motor: análise real + número gigante
    c.add(c.wipe(t_mot, C, .5, 'up'))
    t_m1 = t_wall or t_top
    fxa, fya = D.get('ana_f', (.5, .36))
    stage.append(shot(t_mot, t_m1, D['ana'] - .15, [(t_mot, cam(fxa, fya, 1.36)), (t_mot + .45, cam(fxa, fya, 1.12)), (t_m1, cam(fxa, fya, 1.18))],
                      [(t_mot, rot(-8, 3, 0)), (t_m1, rot(-3, 1, 0))], rate=D.get('ana_rate', .5)))
    y_m = ny - 40
    if fmt != 'sq': c.add(bscrim(t_mot, t_m1, y_m))
    c.add(txt(D['motor'], t_mot + .2, t_m1 - .22))
    c.add(bignum(D['n_main'][0], t_mot + .35, t_m1 - .05, D['n_main'][2], D['n_main'][1], dur=1.4))
    if reel:
        # 3b · parede de números do motor (tela cheia)
        wx, wy, ws = L['wall']
        rows = ''
        def em(v, f): d = len(str(int(v))); return 1.1 * d + (.45 if f == 'mil' and d > 3 else 0)
        for i, (val, f, lab) in enumerate(D['wall']):
            t = t_wall + .12 + i * .5
            rows += (f'<div style="margin-bottom:{ws * .22:.0f}px;{c.an(c.enter(t, "left", .45, 90))}">'
                     f'<div class="num" style="font-size:{min(ws * (1.4 if i == 0 else 1), (c.W - 2 * wx) / em(val, f)):.0f}px;{"" if i == 0 else "color:#fff"}">{c.count(0, val, t, t + 1.0, fmt=f)}</div>'
                     f'<div class="lab" style="font-size:{ws * .27:.0f}px;margin-top:{ws * .06:.0f}px;color:{MUTED if i else "#fff"}">{lab}</div></div>')
        c.add(f'<div class="fill" style="z-index:25;background:{INK};{c.an(c.show(t_wall, t_top))}"><div class="grid"></div>'
              f'<div class="blob" style="left:-240px;top:{c.H * .5:.0f}px;width:760px;height:760px;background:{C};opacity:.3"></div>'
              f'<div class="abs kick" style="left:{wx}px;top:{wy - 250}px;font-size:40px;{c.an(c.enter(t_wall + .05, "fade", .3))}">{D["kick"]}</div>'
              f'<div class="abs" style="left:{wx}px;top:{wy - 190}px">{c.words(D["wall_hd"], t_wall + .05, size=78, cls="hd", step=.05, dur=.35)}</div>'
              f'<div class="abs" style="left:{wx}px;top:{wy + 40}px;width:{c.W - 2 * wx}px">{rows}</div></div>')
        c.add(c.flash(t_wall, '#fff', .2, .35))
    # 4 · a recomendação: top 3 com as porcentagens batendo uma a uma
    r1, r2, r3 = D['rows']; fmid = (r1 + r3) / 2; s3 = D.get('top_s', 1.18); q3 = L['q3']
    t_e = t_why or t_cta
    stage.append(shot(t_top, t_e, D['top'], [(t_top, cam(.5, fmid, s3 + .3, q3)), (t_top + .45, cam(.5, fmid, s3, q3)), (t_e, cam(.5, fmid, s3 + .06, q3))],
                      [(t_top, rot(7, 2, 0)), (t_top + 1.6, rot(0, 0, 0))], rate=D.get('top_rate', .6)))
    y_btn = q3 + S(s3) * (D['btn'] - fmid) * sh - 14
    c.add(bscrim(t_top, t_e, y_btn if fmt == 'sq' else min(y_btn, ny - 30), fade=90))
    c.add(c.flash(t_top, '#fff', .28, .65))
    c.add(txt(D['top_hd'], t_top + .15, t_e - .22, kind='pop', dur=.4))
    cells = ''
    for i, (pct, r) in enumerate(zip(D['pcts'], D['rows'])):
        t = t_top + .7 + i * (.75 if reel else .6)
        c.add(c.ring(vx + qx + S(s3) * (.88 - .5) * sw, vy + q3 + S(s3) * (r - fmid) * sh, t, size=130, color=C))
        cells += (f'<div style="{c.an(c.enter(t, "pop", .4))}"><div class="kick" style="font-size:{ns * .15:.0f}px;color:#fff">{i + 1}º</div>'
                  f'<div class="num" style="font-size:{ns * (.58 if i == 0 else .43):.0f}px;{"" if i == 0 else "color:#fff"}">{c.count(0, pct, t, t + .6)}<span style="font-size:.42em;letter-spacing:0">%</span></div></div>')
    c.add(f'<div class="abs" style="left:{nx}px;top:{ny - ns * .08:.0f}px;width:{nw}px;z-index:32;display:flex;align-items:flex-end;gap:{nw * .04:.0f}px;{c.an(c.show(t_top, t_e))}">{cells}'
          + '</div>')
    if reel:
        # 5 · o porquê: o card do DNA
        fxc, fyc = D['card_f']
        stage.append(shot(t_why, t_cta, D['card'], [(t_why, cam(fxc, fyc, 1.35, L['q3'])), (t_why + .45, cam(fxc, fyc, 1.0, L['q3'])), (t_cta, cam(fxc, fyc, 1.07, L['q3']))],
                          [(t_why, rot(-14, 5, 0)), (t_cta, rot(-6, 2, 0))], rate=D.get('card_rate', .5)))
        c.add(c.flash(t_why, C, .2, .4))
        c.add(bscrim(t_why, t_cta, ny + 30))
        c.add(txt(D['why_hd'], t_why + .12, t_cta - .22))
        c.add(f'<div class="abs" style="left:{nx}px;top:{ny + 70}px;width:{nw}px;z-index:32;{c.an(c.show(t_why, t_cta), c.enter(t_why + .6, "rise", .45))}">'
              f'<div class="kick" style="font-size:30px;margin-bottom:14px">{D["chip_k"]}</div><span class="chip" style="font-size:52px;padding:18px 30px;line-height:1.1">{D["chip"]}</span></div>')
    c.add(f'<div class="abs" style="left:{vx}px;top:{vy}px;width:{vw}px;height:{vh}px;overflow:hidden">{"".join(stage)}</div>')
    if L['scrim']:
        c.add(f'<div class="abs" style="left:0;top:0;width:100%;height:{L["scrim"]}px;z-index:20;background:linear-gradient({INK} 0%,{INK} 74%,rgba(10,10,10,0));{c.an(c.show(0, t_cta))}"></div>')

    # ---- CTA
    c.add(c.wipe(t_cta, C, .55, 'up'))
    cx, cw = (90, 900) if fmt != 'sq' else (80, 920)
    cy = {'reel': 600, 'feed': 380, 'sq': 250}[fmt]; cs = {'reel': 132, 'feed': 124, 'sq': 100}[fmt]
    ico = c.kf([(t_cta, 'transform:rotate(-24deg) scale(.6);opacity:0', BACK), (t_cta + .7, 'transform:rotate(10deg) scale(1);opacity:.22'), (T, 'transform:rotate(6deg) scale(1.05);opacity:.22')])
    c.add(f'<div class="fill" style="background:{INK};z-index:45;{c.an(c.show(t_cta))}"><div class="grid"></div>'
          f'<div class="blob" style="left:-220px;top:{c.H * .08:.0f}px;width:720px;height:720px;background:{C};opacity:.34"></div>'
          f'<div class="abs" style="right:-110px;bottom:{c.bot - 60 if reel else -70}px;{c.an(ico)}">{svg(SD / D["icon"], w=640)}</div>'
          f'<div class="abs" style="left:{cx}px;top:{cy - cs * 1.45:.0f}px;{c.an(c.enter(t_cta + .15, "left", .45))}">{svg(SD / D["logo"], h=round(cs * .66))}</div>'
          + c.words('Antes de\ncomprar,\nfaça o *teste.*', t_cta + .25, cx, cy, cw, size=cs, cls='hd', step=.07, dur=.45, lh=1.0)
          + f'<div class="abs" style="left:{cx}px;top:{cy + cs * 3.5:.0f}px;{c.an(c.enter(t_cta + 1.0, "pop", .45))}"><span class="url" style="font-size:{cs * .44:.0f}px;padding:{cs * .19:.0f}px {cs * .36:.0f}px">{D["url"]}</span></div>'
          f'<div class="abs kick" style="left:{cx}px;top:{cy + cs * 4.75:.0f}px;font-size:{cs * .2:.0f}px;{c.an(c.enter(t_cta + 1.3, "fade", .4))}">{D["cta_k"]}</div>'
          f'</div>')
    return c


def main(D):
    FR = Path(sys.argv[1]); OUT = Path(sys.argv[2]); which = sys.argv[3] if len(sys.argv) > 3 else 'all'; prev = len(sys.argv) > 4
    V = D['v']
    for fmt in (['reel', 'feed', 'sq'] if which == 'all' else [which]):
        c = build(D, fmt, FR)
        if prev:
            n = int(c.T * 2)
            print(preview(c, OUT / f'_prev_{V}_{fmt}.jpg', [i * .5 + .25 for i in range(n)], cols=10 if fmt == 'reel' else 8, scale=.2 if fmt == 'reel' else .25))
        elif fmt == 'reel':
            render(c, OUT / f'{V}.mp4', cover=(OUT / f'{V}-capa.jpg', 1.35)); (OUT / f'{V}.html').unlink(missing_ok=True)
        else:
            d = OUT / 'ads' / V; d.mkdir(parents=True, exist_ok=True); o = d / f'{V}-motion-{"feed45" if fmt == "feed" else "sq"}.mp4'
            render(c, o); o.with_suffix('.html').unlink(missing_ok=True)
