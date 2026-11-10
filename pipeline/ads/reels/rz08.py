"""ADC-RZ-08 v1 · hero Retrozap no modelo novo (estudio.py + DIRECAO.md).
Gancho no palpite do Rei(nha) do Kkkk → pódio do Tagarela → raspadinha do Boca-Suja → 3 cortes de prova → CTA.
Captura real: pasta de quadros da gravação (captura_rz.py + raw_video.py + estudio.frames).
Uso: python3 rz08.py <pasta de quadros> <saida media> [reel|feed|sq|all] [preview]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import *

FR = Path(sys.argv[1]); OUT = Path(sys.argv[2]); WHICH = sys.argv[3] if len(sys.argv) > 3 else 'all'; PREV = len(sys.argv) > 4
V = 'ADC-RZ-08-v1'
RZ = A / 'retrozap'
NOITE, ACAI, MANGA, CHIC, GOIABA, PISC, UVA, AREIA = '#1A0B2E', '#3D1A5C', '#FFC23C', '#FF4F8B', '#FF7A59', '#2EC4F1', '#A98BFF', '#FFF4E0'
FONTS = ff('Bricolage Grotesque', 'Bricolage-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700')
CSS = f"""
.hd{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.035em;color:{AREIA};z-index:30;text-shadow:0 6px 30px rgba(26,11,46,.55)}}
.hl{{color:{MANGA}}}
.url{{font-family:'DM Sans',sans-serif;font-weight:700;background:{MANGA};color:{NOITE};border-radius:999px;display:inline-block;white-space:nowrap}}
.blob{{position:absolute;border-radius:50%;filter:blur(120px);opacity:.5}}
"""
# marcas da captura (s do vídeo fonte)
TAP4, POD_TAP, POD_JUMP, RASPA_REV = 80.2, 42.9, 44.85, 68.35

LAY = {  # vp = recorte onde o celular vive; ph = (x, y, largura) dentro do vp; q = ponto para onde o zoom leva o foco
    'reel': dict(vp=(0, 0, 1080, 1920), ph=(160, 570, 760), q=(540, 1040), tx=(70, 285, 940), ts=124, z=1.0, scrim=720),
    'feed': dict(vp=(0, 0, 1080, 1350), ph=(240, 330, 600), q=(540, 830), tx=(60, 66, 960), ts=100, z=.95, scrim=380),
    'sq':   dict(vp=(500, 0, 580, 1080), ph=(70, 90, 440), q=(290, 560), tx=(56, 170, 430), ts=84, z=.82, scrim=0),
}


def build(fmt):
    L = LAY[fmt]; reel = fmt == 'reel'
    T = 20.0 if reel else 12.0
    c = Comp(fmt, T, NOITE, FONTS, CSS)
    _show = c.show; c.show = lambda t0, t1=None, fin=0.0, fout=0.0: _show(t0, t1, fin, max(fout, .002))  # contorna show() com fout=0 (vira fade longo)
    px, py, pw = L['ph']; b = 16; sw = pw - 2 * b; sh = sw * 16 / 9; qx, qy = L['q']

    def cam(fx=None, fy=None, s=1.0):
        if fx is None: return f'transform:translate(0px,0px) scale({s})'
        s = 1 + (s - 1) * L['z']
        return f'transform:translate({qx - px - s * (b + sw * fx):.1f}px,{qy - py - s * (b + sh * fy):.1f}px) scale({s:.3f})'

    def rot(y=0, x=0, z=0): return f'transform:perspective(2400px) rotateY({y}deg) rotateX({x}deg) rotateZ({z}deg)'

    def shot(t0, t1, src0, cams, rots=None, rate=1.0):
        k = c.kf(cams, EASE); r = c.kf(rots or [(t0, rot())], EASE)
        return (f'<div class="abs" style="left:{px}px;top:{py}px;transform-origin:0 0;{c.an(k, c.show(t0, t1))}">'
                f'<div style="transform-origin:50% 50%;{c.an(r)}">{c.phone(c.clip(FR, src0, t0, t1, rate), pw)}</div></div>')

    def txt(s, t, out, size=None, **kw):
        x, y, w = L['tx']
        return c.words(s, t, x, y, w, size=size or L['ts'], cls='hd', out=out, lh=.98, **kw)

    # fundo vivo
    d1 = c.kf([(0, 'transform:translate(0,0)'), (T / 2, 'transform:translate(160px,120px)', 'ease-in-out'), (T, 'transform:translate(0,0)')], 'ease-in-out')
    d2 = c.kf([(0, 'transform:translate(0,0)'), (T / 2, 'transform:translate(-140px,-160px)', 'ease-in-out'), (T, 'transform:translate(0,0)')], 'ease-in-out')
    c.add(f'<div class="blob" style="left:-260px;top:{c.H * .25:.0f}px;width:760px;height:760px;background:{UVA};{c.an(d1)}"></div>'
          f'<div class="blob" style="right:-300px;top:{c.H * .6:.0f}px;width:800px;height:800px;background:{CHIC};opacity:.32;{c.an(d2)}"></div>')
    vx, vy, vw, vh = L['vp']
    stage = []

    # ---- 1 · gancho + palpite (toque em t=2.2)
    s0 = TAP4 - 2.2
    stage.append(shot(0, 4.5, s0,
                      [(0, cam(.5, .5, .92)), (.9, cam(), SNAP), (1.35, cam(), SNAP), (1.9, cam(.5, .69, 1.55)), (2.28, cam(.5, .69, 1.6), SNAP), (2.7, cam(.5, .3, 1.36)), (4.5, cam(.5, .3, 1.44))],
                      [(0, rot(-22, 10, -3)), (.9, rot(-6, 3, 0)), (1.9, rot(0, 0, 0))]))
    # ---- 2 · pódio (toque em 5.0, salto do layout em 7.1)
    p0 = POD_TAP - .5
    t_jump = 4.5 + (POD_JUMP - p0)
    stage.append(shot(4.5, 9.0, p0,
                      [(4.5, cam(.5, .76, 1.7)), (4.95, cam(.5, .76, 1.5)), (t_jump - .12, cam(.5, .76, 1.56), SNAP), (t_jump + .28, cam(.5, .3, 1.38)), (9.0, cam(.5, .3, 1.46))],
                      [(4.5, rot(8, 0, 0)), (6.5, rot(0, 0, 0))]))
    if reel:
        # ---- 3 · raspadinha (revela em 11.4)
        r0 = RASPA_REV - 2.15; t_rev = 11.15
        stage.append(shot(9.0, 13.0, r0,
                          [(9.0, cam(.5, .68, 1.85)), (9.45, cam(.5, .68, 1.62)), (t_rev - .05, cam(.5, .68, 1.7), SNAP), (t_rev + .35, cam(.5, .33, 1.4)), (13.0, cam(.5, .33, 1.47))],
                          [(9.0, rot(-8, 0, 0)), (11.0, rot(0, 0, 0))]))
        # ---- 4 · prova: 3 cortes
        stage.append(shot(13.0, 14.4, 90.5, [(13.0, cam(.5, .3, 1.7)), (13.35, cam(.5, .3, 1.5)), (14.4, cam(.5, .3, 1.56))], [(13.0, rot(-12, 4, 0)), (14.4, rot(-7, 2, 0))]))
        stage.append(shot(14.4, 15.7, 100.66, [(14.4, cam(.5, .42, 1.55)), (14.75, cam(.5, .42, 1.36)), (15.7, cam(.5, .42, 1.42))], [(14.4, rot(12, 4, 0)), (15.7, rot(7, 2, 0))], rate=.25))
        stage.append(shot(15.7, 17.0, 49.6, [(15.7, cam(.5, .33, 1.62)), (16.05, cam(.5, .33, 1.42)), (17.0, cam(.5, .33, 1.48))], [(15.7, rot(0, 8, 0)), (17.0, rot(0, 3, 0))]))
    c.add(f'<div class="abs" style="left:{vx}px;top:{vy}px;width:{vw}px;height:{vh}px;overflow:hidden">{"".join(stage)}</div>')
    t_cta = 17.0 if reel else 9.0
    if L['scrim']:
        c.add(f'<div class="abs" style="left:0;top:0;width:100%;height:{L["scrim"]}px;z-index:20;background:linear-gradient({NOITE} 0%,{NOITE} 74%,rgba(26,11,46,0));{c.an(c.show(0, t_cta))}"></div>')

    # toque (reforço do indicador da própria captura)
    s_tap = 1 + (1.6 - 1) * L['z']
    c.add(c.ring(vx + qx + s_tap * (.26 - .5) * sw, vy + qy + s_tap * (.745 - .69) * sh, 2.2, size=170, color=MANGA))
    c.add(c.flash(2.32, MANGA, .3, .5)); c.add(c.flash(t_jump + .08, '#fff', .28, .6))

    # textos
    c.add(txt('Quem ri *mais*\nno seu grupo?', -.3, 2.3, step=.06, dur=.4))
    c.add(txt('O Retrozap\n*sabe.*', 2.72, 4.25, kind='pop', dur=.4))
    c.add(c.wipe(4.5, CHIC, .5, 'up'))
    c.add(txt('E quem *fala*\n*demais?*', 4.72, t_jump - .15))
    c.add(txt('*Pódio* revelado\nna hora.', t_jump + .25, 8.8, kind='pop', dur=.4))
    if reel:
        c.add(c.wipe(9.0, GOIABA, .5, 'left'))
        c.add(txt('Raspa pra ver\no *Boca-Suja.*', 9.22, 11.0))
        c.add(c.flash(11.2, '#fff', .28, .6))
        c.add(txt('*Revelado.*', 11.5, 12.8, kind='pop', dur=.4))
        c.add(c.flash(13.0, MANGA, .22, .45)); c.add(c.flash(14.4, UVA, .2, .4)); c.add(c.flash(15.7, PISC, .2, .4))
        c.add(txt('E tem *muito*\n*mais.*', 13.08, 14.3))
        c.add(txt('O *top 3*\ndo ano.', 14.48, 15.6))
        c.add(txt('*Card* pronto\npro grupo.', 15.78, 16.85))

    # ---- CTA
    c.add(c.wipe(t_cta, MANGA, .55, 'up'))
    cx, cw = (90, 900) if fmt != 'sq' else (80, 920)
    cy = {'reel': 520, 'feed': 330, 'sq': 200}[fmt]; cs = {'reel': 128, 'feed': 124, 'sq': 100}[fmt]
    end = c.show(t_cta)
    taca = c.kf([(t_cta, 'transform:rotate(-24deg) scale(.6);opacity:0', BACK), (t_cta + .7, 'transform:rotate(12deg) scale(1);opacity:.12'), (T, 'transform:rotate(8deg) scale(1.04);opacity:.12')])
    c.add(f'<div class="fill" style="background:{NOITE};z-index:45;{c.an(end)}">'
          f'<div class="blob" style="left:-200px;top:{c.H * .1:.0f}px;width:700px;height:700px;background:{UVA}"></div>'
          f'<div class="abs" style="right:-120px;bottom:{c.bot - 40 if reel else -60}px;{c.an(taca)}">{svg(RZ / "logo-simbolo-grupo.svg", w=620)}</div>'
          f'<div class="abs" style="left:{cx}px;top:{cy - cs * 1.5:.0f}px;{c.an(c.enter(t_cta + .15, "left", .45))}">{svg(RZ / "logo-assinatura-grupo.svg", h=round(cs * .78))}</div>'
          + c.words('Faça a\nretrospectiva\n2026 do\n*seu grupo.*', t_cta + .25, cx, cy, cw, size=cs, cls='hd', step=.07, dur=.45, lh=1.0)
          + f'<div class="abs" style="left:{cx}px;top:{cy + cs * 4.5:.0f}px;{c.an(c.enter(t_cta + 1.05, "pop", .45))}"><span class="url" style="font-size:{cs * .46:.0f}px;padding:{cs * .2:.0f}px {cs * .42:.0f}px">retrozap.com.br</span></div>'
          f'</div>')
    return c


for fmt in (['reel', 'feed', 'sq'] if WHICH == 'all' else [WHICH]):
    c = build(fmt)
    if PREV:
        n = int(c.T * 2)
        print(preview(c, OUT / f'_prev_{fmt}.jpg', [i * .5 + .25 for i in range(n)], cols=10, scale=.2 if fmt == 'reel' else .25))
    elif fmt == 'reel':
        render(c, OUT / f'{V}.mp4', cover=(OUT / f'{V}-capa.jpg', 1.2))
    else:
        d = OUT / 'ads' / V; d.mkdir(parents=True, exist_ok=True)
        render(c, d / f'{V}-motion-{"feed45" if fmt == "feed" else "sq"}.mp4')
