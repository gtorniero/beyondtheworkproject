"""Helpers da referência ADC-RZ-08 (rz08.py) para os outros ADs do Retrozap: mesmo look (celular grande, fundo Noite com
manchas de luz, título enorme no topo, wipes de cor, CTA com assinatura) com roteiro próprio em cada AD."""
import sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import *

RZ = A / 'retrozap'
NOITE, ACAI, MANGA, CHIC, GOIABA, PISC, UVA, AREIA = '#1A0B2E', '#3D1A5C', '#FFC23C', '#FF4F8B', '#FF7A59', '#2EC4F1', '#A98BFF', '#FFF4E0'
FONTS = ff('Bricolage Grotesque', 'Bricolage-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700')
CSS = f"""
.hd{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.035em;color:{AREIA};z-index:30;text-shadow:0 6px 30px rgba(26,11,46,.55)}}
.hl{{color:{MANGA}}}
.sub{{font-family:'DM Sans',sans-serif;font-weight:700;letter-spacing:-.01em}}
.url{{font-family:'DM Sans',sans-serif;font-weight:700;background:{MANGA};color:{NOITE};border-radius:999px;display:inline-block;white-space:nowrap}}
.blob{{position:absolute;border-radius:50%;filter:blur(120px);opacity:.5}}
.ico svg{{display:block;filter:drop-shadow(0 18px 30px rgba(0,0,0,.4))}}
"""
LAY = {  # igual ao rz08.py
    'reel': dict(vp=(0, 0, 1080, 1920), ph=(160, 570, 760), q=(540, 1040), tx=(70, 285, 940), ts=124, z=1.0, scrim=720),
    'feed': dict(vp=(0, 0, 1080, 1350), ph=(240, 330, 600), q=(540, 830), tx=(60, 66, 960), ts=100, z=.95, scrim=380),
    'sq':   dict(vp=(500, 0, 580, 1080), ph=(70, 90, 440), q=(290, 560), tx=(56, 170, 430), ts=84, z=.82, scrim=0),
}


def kit(fmt, T, FR, blobs=(UVA, CHIC)):
    L = LAY[fmt]; c = Comp(fmt, T, NOITE, FONTS, CSS)
    px, py, pw = L['ph']; b = 16; sw = pw - 2 * b; sh = sw * 16 / 9; qx, qy = L['q']; vx, vy, vw, vh = L['vp']
    stage = []

    def cam(fx=None, fy=None, s=1.0):
        if fx is None: return f'transform:translate(0px,0px) scale({s})'
        s = 1 + (s - 1) * L['z']
        return f'transform:translate({qx - px - s * (b + sw * fx):.1f}px,{qy - py - s * (b + sh * fy):.1f}px) scale({s:.3f})'

    def rot(y=0, x=0, z=0): return f'transform:perspective(2400px) rotateY({y}deg) rotateX({x}deg) rotateZ({z}deg)'

    def shot(t0, t1, src0, cams, rots=None, rate=1.0):
        k = c.kf(cams, EASE); r = c.kf(rots or [(t0, rot())], EASE)
        stage.append(f'<div class="abs" style="left:{px}px;top:{py}px;transform-origin:0 0;{c.an(k, c.show(t0, t1))}">'
                     f'<div style="transform-origin:50% 50%;{c.an(r)}">{c.phone(c.clip(FR, src0, t0, t1, rate), pw)}</div></div>')

    def txt(s, t, out, size=None, **kw):
        x, y, w = L['tx']
        kw.setdefault('lh', .98)
        return c.add(c.words(s, t, x, y, w, size=size or L['ts'], cls='hd', out=out, **kw))

    def num(a, b_, t0, t1, label, out, fmt_='mil', nsize=None, t_in=None, pre='', suf=''):
        """Título de número gigante: o número roda de a até b (t0→t1) e a legenda entra embaixo."""
        x, y, w = L['tx']; ns = nsize or round(L['ts'] * (1.55 if fmt == 'sq' else 2.1)); t_in = t0 if t_in is None else t_in
        e = c.enter(t_in, 'pop', .4); o = c.exit(out, 'up', .25, 40)
        c.add(f'<div class="hd" style="position:absolute;left:{x}px;top:{y - ns * .12:.0f}px;width:{w}px;{c.an(o)}">'
              f'<div class="hl" style="font-size:{ns}px;line-height:.9;transform-origin:0 60%;{c.an(e)}">{c.count(a, b_, t0, t1, fmt=fmt_, pre=pre, suf=suf)}</div>'
              + c.words(label, t_in + .25, size=round(L['ts'] * .62), step=.06, dur=.4, lh=1.02, style='margin-top:10px') + '</div>')

    def ico(name, x, y, t0, t1, size=150, r=-8, casa='grupo'):
        """Ícone oficial flutuando como elemento de cena (coordenadas do formato reel; some nos outros se sair do quadro)."""
        if fmt == 'sq': return
        if fmt == 'feed': y = round(y * 1350 / 1920); size = round(size * .85)
        e = c.kf([(t0, f'opacity:0;transform:scale(.3) rotate({r - 30}deg)', BACK), (t0 + .45, f'opacity:1;transform:scale(1) rotate({r}deg)', 'ease-in-out'),
                  (t1 - .2, f'opacity:1;transform:translateY(-26px) scale(1.04) rotate({r + 6}deg)', SNAP), (t1, f'opacity:0;transform:translateY(-60px) scale(.7) rotate({r}deg)')])
        c.add(f'<div class="abs ico" style="left:{x}px;top:{y}px;z-index:25;{c.an(e, c.show(t0 - .01, t1 + .01))}">{svg(RZ / f"icones-{casa}" / f"{name}.svg", w=size, h=size)}</div>')

    def mount(t_cta):
        d1 = c.kf([(0, 'transform:translate(0,0)'), (T / 2, 'transform:translate(160px,120px)', 'ease-in-out'), (T, 'transform:translate(0,0)')], 'ease-in-out')
        d2 = c.kf([(0, 'transform:translate(0,0)'), (T / 2, 'transform:translate(-140px,-160px)', 'ease-in-out'), (T, 'transform:translate(0,0)')], 'ease-in-out')
        bg = (f'<div class="blob" style="left:-260px;top:{c.H * .25:.0f}px;width:760px;height:760px;background:{blobs[0]};{c.an(d1)}"></div>'
              f'<div class="blob" style="right:-300px;top:{c.H * .6:.0f}px;width:800px;height:800px;background:{blobs[1]};opacity:.32;{c.an(d2)}"></div>'
              f'<div class="abs" style="left:{vx}px;top:{vy}px;width:{vw}px;height:{vh}px;overflow:hidden">{"".join(stage)}</div>')
        if L['scrim']:
            bg += f'<div class="abs" style="left:0;top:0;width:100%;height:{L["scrim"]}px;z-index:20;background:linear-gradient({NOITE} 0%,{NOITE} 74%,rgba(26,11,46,0));{c.an(c.show(0, t_cta))}"></div>'
        c.layers.insert(0, bg)

    def cta(t_cta, lines, wipe=MANGA, blob=UVA, direction='up'):
        reel = fmt == 'reel'; n = lines.count('\n') + 1
        c.add(c.wipe(t_cta, wipe, .55, direction))
        cx, cw = (90, 900) if fmt != 'sq' else (80, 920)
        cy = {'reel': 520, 'feed': 330, 'sq': 200}[fmt]; cs = {'reel': 128, 'feed': 124, 'sq': 100}[fmt]
        if n == 3: cy += round(cs * .4)
        taca = c.kf([(t_cta, 'transform:rotate(-24deg) scale(.6);opacity:0', BACK), (t_cta + .7, 'transform:rotate(12deg) scale(1);opacity:.12'), (T, 'transform:rotate(8deg) scale(1.04);opacity:.12')])
        c.add(f'<div class="fill" style="background:{NOITE};z-index:45;{c.an(c.show(t_cta))}">'
              f'<div class="blob" style="left:-200px;top:{c.H * .1:.0f}px;width:700px;height:700px;background:{blob}"></div>'
              f'<div class="abs" style="right:-120px;bottom:{c.bot - 40 if reel else -60}px;{c.an(taca)}">{svg(RZ / "logo-simbolo-grupo.svg", w=620)}</div>'
              f'<div class="abs" style="left:{cx}px;top:{cy - cs * 1.5:.0f}px;{c.an(c.enter(t_cta + .15, "left", .45))}">{svg(RZ / "logo-assinatura-grupo.svg", h=round(cs * .78))}</div>'
              + c.words(lines, t_cta + .25, cx, cy, cw, size=cs, cls='hd', step=.07, dur=.45, lh=1.0)
              + f'<div class="abs" style="left:{cx}px;top:{cy + cs * (n + .5):.0f}px;{c.an(c.enter(t_cta + 1.05, "pop", .45))}"><span class="url" style="font-size:{cs * .46:.0f}px;padding:{cs * .2:.0f}px {cs * .42:.0f}px">retrozap.com.br</span></div>'
              f'</div>')

    return SimpleNamespace(c=c, L=L, fmt=fmt, T=T, reel=fmt == 'reel', cam=cam, rot=rot, shot=shot, txt=txt, num=num, ico=ico, mount=mount, cta=cta)


async def _render_calmo(c, out, cover, crf=17):
    """Igual ao estudio.render, mas sem limite de tempo por quadro (máquina carregada estoura os 30 s do screenshot)."""
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    hp = out.with_suffix('.html'); hp.write_text(c.html())
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': c.W, 'height': c.H}, device_scale_factor=1); pg.set_default_timeout(0)
        await pg.goto(hp.as_uri()); await pg.evaluate('document.fonts.ready')
        if cover:
            await pg.evaluate(f'seek({cover[1]})'); await pg.screenshot(path=str(cover[0]), type='jpeg', quality=92)
        ffm = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-', '-an', '-c:v', 'libx264',
                                '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', str(crf), '-preset', 'medium', '-r', str(FPS), '-movflags', '+faststart', str(out)], stdin=subprocess.PIPE)
        for i in range(int(round(c.T * FPS))):
            await pg.evaluate(f'seek({i / FPS:.5f})')
            ffm.stdin.write(await pg.screenshot(type='jpeg', quality=95))
        ffm.stdin.close(); ffm.wait(); await b.close()
    hp.unlink(missing_ok=True)


def render(c, out, cover=None, **kw):
    asyncio.run(_render_calmo(c, out, cover))


def run(V, build, cover_t=1.2):
    """Uso: python3 <script>.py <pasta de quadros> <saida media> [reel|feed|sq|all] [preview]"""
    FR = Path(sys.argv[1]); OUT = Path(sys.argv[2]); which = sys.argv[3] if len(sys.argv) > 3 else 'all'; prev = len(sys.argv) > 4
    for fmt in (['reel', 'feed', 'sq'] if which == 'all' else [which]):
        c = build(fmt, FR)
        if prev:
            print(preview(c, OUT / f'_prev_{V}_{fmt}.jpg', [i * .5 + .25 for i in range(int(c.T * 2))], cols=10, scale=.2 if fmt == 'reel' else .25))
        elif fmt == 'reel':
            render(c, OUT / f'{V}.mp4', cover=(OUT / f'{V}-capa.jpg', cover_t)); (OUT / f'{V}.html').unlink(missing_ok=True)
        else:
            d = OUT / 'ads' / V; d.mkdir(parents=True, exist_ok=True); o = d / f'{V}-motion-{"feed45" if fmt == "feed" else "sq"}.mp4'
            render(c, o); o.with_suffix('.html').unlink(missing_ok=True)
