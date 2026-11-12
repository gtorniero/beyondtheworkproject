"""KV Quiddo Família e Amigos (ADC-QD-11..15). Um conceito, 5 execuções.
Conceito: "a sala da turma" — fundo creme quente com os símbolos das respostas como confete, título enorme com marcador na cor do tema,
o telão da sala (captura REAL do app, visual festa do tema) + o celular de quem joga (captura REAL) + a turma de bichos do avatar do app
e balões de reação curtos (sem nome, sem depoimento). CTA "Criar meu quiz".
Uso: python3 qd_fam_kv.py <pasta das capturas (fam)> <tema|all> <static|video|all> [preview]"""
import asyncio, base64, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import estudio as E
from estudio import ff, svg, A, Comp, render, preview, EASE, SNAP, BACK
from playwright.async_api import async_playwright

CAPS, QUAL, WHAT = Path(sys.argv[1]), sys.argv[2], sys.argv[3]; PREV = len(sys.argv) > 4
OUTM = Path(__file__).resolve().parent.parent.parent / 'out' / 'media'
Q = A / 'quiddo'; ART = json.loads((Q / 'art.json').read_text())
CREME, TINTA, VERDE, AMARELO, LARANJA, AZUL, VERM, ROSA = '#FFF6E6', '#0E2A22', '#13A07A', '#FFC83D', '#FF7A1A', '#1E7FD6', '#E5383B', '#FF8FB1'
FONTS = ff('Fraunces', 'Fraunces-900.woff2', '900') + ff('Nunito', 'Nunito-var.woff2', '600 900')
LOGO = svg(Q / 'quiddo-cor.svg', w=210)
SIMS = {k: (Q / f'{k}.svg').read_text() for k in ('folha', 'sol', 'gota', 'flor')}

TEMAS = {  # id, título (com *destaque*), cor do destaque, chip, balões, bichos, URL term
 'familia':  dict(id='ADC-QD-11', tit='Quem conhece melhor\n*essa família?*', cor=AMARELO, chip='Noite de jogos em família',
                  bal=['Óbvio que é o vô 😂', 'Eu NÃO ronco!'], term='familia',
                  bichos=['capivara.gorro.redondos.3', 'jabuti.palha.redondos.3', 'onca.flor.-.2', 'tucano.bone.-.5']),
 'amigos':   dict(id='ADC-QD-12', tit='O grupo\nvirou *jogo.*', cor=AZUL, chip='Noite com os amigos', fg='#fff',
                  bal=['Isso é pessoal 😂', 'Pede recontagem!'], term='amigos',
                  bichos=['sapo.-.escuros.4', 'preguica.fone.-.2', 'tucano.bone.-.5', 'capivara.-.escuros.1']),
 'chabar':   dict(id='ADC-QD-13', tit='Quem conhece melhor\n*o casal?*', cor=ROSA, chip='Chá-bar e chá de casa nova',
                  bal=['Eu sabia!!', 'Jurava que era cinema!'], term='chabar',
                  bichos=['onca.flor.-.2', 'tucano.-.coracao.3', 'capivara.palha.redondos.1', 'jabuti.palha.-.3']),
 'despedida':dict(id='ADC-QD-14', tit='Quem conhece mesmo\n*quem vai casar?*', cor=LARANJA, chip='Despedida de solteiro ou solteira',
                  bal=['Ele vai negar 😂', 'Áudio de 4 minutos, sim'], term='despedida',
                  bichos=['tucano.bone.-.5', 'onca.coroa.-.2', 'sapo.-.escuros.4', 'preguica.fone.-.2']),
 'confra':   dict(id='ADC-QD-15', tit='As histórias da turma\nvalem *um pódio.*', cor=VERDE, chip='Confraternização da turma', fg='#fff',
                  bal=['Todo ano isso 😂', 'Calúnia!'], term='confra',
                  bichos=['capivara.-.escuros.1', 'onca.coroa.-.2', 'jabuti.palha.redondos.3', 'tucano.-.coracao.3']),
}
SUB = 'Crie perguntas sobre a sua turma.<br>Todo mundo joga pelo celular.'


def av(k, s):
    k = k if k in ART['av'] else next(x for x in ART['av'] if x.startswith(k.split('.')[0]))
    return ART['av'][k].replace('width="120" height="120"', f'width="{s}" height="{s}"')


def uri(p):
    return 'data:image/png;base64,' + base64.b64encode(Path(p).read_bytes()).decode()


def cel_crop(p, h=1640):
    """Celular: corta o rodapé do site (links), fica só o app."""
    from PIL import Image
    import io
    im = Image.open(p).convert('RGB').crop((0, 0, 1080, h)); b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def tit_html(t, cor, fg=TINTA):
    out = []
    for ln in t.split('\n'):
        parts = ln.split('*')
        s = ''.join(f'<span class="mk" style="background:{cor};color:{fg}">{x}</span>' if i % 2 else x for i, x in enumerate(parts))
        out.append(f'<span class="ln">{s}</span>')
    return ''.join(out)


CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}
.kv{{position:relative;overflow:hidden;background:{CREME};font-family:Nunito,sans-serif;color:{TINTA}}}
.abs{{position:absolute}}
.t{{font-family:Fraunces,serif;font-weight:900;letter-spacing:-.025em;line-height:1.02}}
.t .ln{{display:block}}
.mk{{display:inline-block;padding:0 .12em;margin:.04em 0;transform:rotate(-2deg);border-radius:.1em;border:5px solid {TINTA};box-shadow:0 7px 0 {TINTA}}}
.chip{{display:inline-block;background:#fff;border:5px solid {TINTA};box-shadow:0 6px 0 {TINTA};border-radius:999px;padding:8px 24px;font-weight:900;font-size:28px}}
.tv{{background:#14141a;border-radius:22px;padding:12px;border:6px solid {TINTA};box-shadow:0 14px 0 {TINTA}}}
.tv img{{display:block;width:100%;border-radius:10px}}
.ph{{background:#0b0b0d;border-radius:50px;padding:11px;border:6px solid {TINTA};box-shadow:0 14px 0 {TINTA}}}
.ph .s{{border-radius:40px;overflow:hidden}} .ph img{{display:block;width:100%}}
.bal{{background:#fff;border:5px solid {TINTA};box-shadow:0 8px 0 {TINTA};border-radius:30px 30px 30px 8px;padding:14px 24px;font-weight:900;white-space:nowrap}}
.bal.r{{border-radius:30px 30px 8px 30px}}
.cta{{display:inline-flex;align-items:center;background:{AMARELO};color:{TINTA};border:6px solid {TINTA};box-shadow:0 10px 0 {TINTA};border-radius:999px;padding:16px 34px;font-weight:900;white-space:nowrap}}
.url{{font-weight:900}} .sub{{font-weight:800;line-height:1.28}}
.bicho{{display:inline-block;filter:drop-shadow(0 6px 0 {TINTA})}}
.sim svg{{display:block;width:100%;height:auto}}
"""


def confete(W, H, n=9, seed=3):
    import random
    r = random.Random(seed); k = list(SIMS); out = []
    for i in range(n):
        x, y, s, rot = r.randint(0, W - 80), r.randint(0, H - 80), r.randint(46, 84), r.randint(-30, 30)
        out.append(f'<div class="abs sim" style="left:{x}px;top:{y}px;width:{s}px;transform:rotate({rot}deg);opacity:.16">{SIMS[k[i % 4]]}</div>')
    return ''.join(out)


# ---------- layouts por formato: posições (x, y, largura) e tamanhos
L = {
 'feed45': dict(W=1080, H=1350, logo=(64, 56), chip=(64, 150), tit=(64, 222, 960, 84), tv=(50, 525, 690, -2), ph=(738, 470, 300, 4),
                bal=[(560, 420, 34, 'r'), (590, 1000, 32, '')], bichos=(70, 945, 104), sub=(64, 1085, 34), cta=(64, 1190, 38), url=(470, 1212, 32)),
 'sq':     dict(W=1080, H=1080, logo=(56, 48), chip=(300, 52), tit=(56, 130, 980, 72), tv=(48, 380, 640, -2), ph=(720, 330, 300, 4),
                bal=[(480, 300, 30, 'r'), (40, 790, 30, '')], bichos=(360, 755, 96), sub=None, cta=(56, 950, 36), url=(460, 970, 30)),
 'story':  dict(W=1080, H=1920, logo=(64, 290), chip=(64, 380), tit=(64, 450, 960, 92), tv=(40, 700, 880, -2), ph=(690, 930, 345, 4),
                bal=[(600, 640, 36, 'r'), (64, 1360, 34, '')], bichos=(64, 1250, 96), sub=None, cta=(64, 1452, 40), url=(492, 1478, 30)),
 'land':   dict(W=1200, H=628, logo=(40, 34), chip=None, tit=(40, 100, 560, 50), tv=(600, 66, 440, -2), ph=(1000, 150, 170, 4),
                bal=[(820, 30, 22, 'r'), (40, 410, 22, '')], bichos=None, sub=(40, 300, 24), cta=(40, 520, 28), url=(330, 535, 24)),
 'wide':   dict(W=1920, H=1080, logo=(80, 70), chip=(80, 170), tit=(80, 250, 860, 74), tv=(980, 170, 760, -2), ph=(1570, 330, 300, 4),
                bal=[(1380, 90, 34, 'r'), (930, 760, 34, '')], bichos=(1030, 690, 104), sub=(80, 640, 36), cta=(80, 860, 40), url=(470, 884, 34)),
}


def blocos(t, f, imgs):
    """Blocos HTML do KV (cada um posicionado), para estático e vídeo. imgs: tv, cel."""
    C = TEMAS[t]; l = L[f]; fg = C.get('fg', TINTA); b = {}
    b['logo'] = f'<div class="abs" style="left:{l["logo"][0]}px;top:{l["logo"][1]}px">{svg(Q / "quiddo-cor.svg", w=int(210 * (0.75 if f == "land" else 1)))}</div>'
    if l['chip']: b['chip'] = f'<div class="abs" style="left:{l["chip"][0]}px;top:{l["chip"][1]}px"><span class="chip" style="font-size:{26 if f != "wide" else 30}px">{C["chip"]}</span></div>'
    x, y, w, s = l['tit']; b['tit'] = f'<div class="abs t" style="left:{x}px;top:{y}px;width:{w}px;font-size:{s}px">{tit_html(C["tit"], C["cor"], fg)}</div>'
    x, y, w, r = l['tv']; b['tv'] = f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({r}deg)"><div class="tv"><img id="tvimg" src="{imgs["tv"]}"></div></div>'
    x, y, w, r = l['ph']; b['ph'] = f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({r}deg)"><div class="ph"><div class="s"><img id="celimg" src="{imgs["cel"]}"></div></div></div>'
    for i, (x, y, s, cls) in enumerate(l['bal']):
        b[f'bal{i}'] = f'<div class="abs" style="left:{x}px;top:{y}px;transform:rotate({-3 if i else 3}deg)"><div class="bal {cls}" style="font-size:{s}px">{C["bal"][i]}</div></div>'
    if l['bichos']:
        x, y, s = l['bichos']; b['bichos'] = (f'<div class="abs" style="left:{x}px;top:{y}px;display:flex;gap:{s // 8}px">'
                                              + ''.join(f'<span class="bicho" style="transform:rotate({(-1) ** i * 6}deg)">{av(k, s)}</span>' for i, k in enumerate(C['bichos'])) + '</div>')
    if l['sub']: x, y, s = l['sub']; b['sub'] = f'<div class="abs sub" style="left:{x}px;top:{y}px;font-size:{s}px">{SUB}</div>'
    x, y, s = l['cta']; b['cta'] = f'<div class="abs" style="left:{x}px;top:{y}px"><span class="cta" style="font-size:{s}px">Criar meu quiz</span></div>'
    x, y, s = l['url']; b['url'] = f'<div class="abs url" style="left:{x}px;top:{y}px;font-size:{s}px">quiddo.com.br</div>'
    return b


ORD = ['logo', 'chip', 'tit', 'tv', 'ph', 'bichos', 'bal0', 'bal1', 'sub', 'cta', 'url']


def imgs_for(t, step='tap'):
    d = CAPS / t
    tv = {'q': 'tv_q.png', 'tap': 'tv_q2.png', 'rev': 'tv_rev2.png', 'pod': 'tv_1_None.png'}[step]
    cel = {'q': 'cel_q.png', 'tap': 'cel_tap.png', 'rev': 'cel_rev2.png', 'pod': 'cel_1_None.png'}[step]
    return dict(tv=uri(d / tv), cel=cel_crop(d / cel))


async def shot(html, W, H, out):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': W, 'height': H})
        await pg.set_content(html); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
        await pg.screenshot(path=str(out)); await b.close()


def static(t, f, out):
    l = L[f]; bl = blocos(t, f, imgs_for(t, 'rev' if f in ('land',) else 'tap'))
    html = (f'<!doctype html><meta charset="utf-8"><style>{FONTS}{CSS}</style><div class="kv" style="width:{l["W"]}px;height:{l["H"]}px">'
            + confete(l['W'], l['H']) + ''.join(bl[k] for k in ORD if k in bl) + '</div>')
    asyncio.run(shot(html, l['W'], l['H'], out))


# ---------- vídeo: o KV ganhando vida (14 s). Gancho no 1º segundo; telas reais trocam: pergunta → toque → revelação → pódio; CTA parado no fim.
E.FMT['wide'] = (1920, 1080, 60, 60)
VF = {'reel': 'story', 'feed': 'feed45', 'sq': 'sq', 'wide': 'wide'}


def video(t, vf, out, cover=None, prev=None):
    f = VF[vf]; l = L[f]; T = 14.0
    c = Comp(vf, T, CREME, FONTS, CSS)
    steps = {k: imgs_for(t, k) for k in ('q', 'tap', 'rev', 'pod')}
    b = blocos(t, f, steps['q'])
    c.add(f'<div class="fill">{confete(l["W"], l["H"])}</div>')
    an = lambda *ks: c.an(*ks)
    # logo, chip e título já no quadro 0 (gancho imediato); entram com movimento curto
    c.add(f'<div style="{an(c.enter(0.0, "fade", .4))}">{b["logo"]}</div>')
    if 'chip' in b: c.add(f'<div style="{an(c.enter(0.05, "pop", .5))}">{b["chip"]}</div>')
    c.add(f'<div style="{an(c.enter(0.0, "rise", .5, 30))}">{b["tit"]}</div>')
    # telão e celular: entram aos 0,5 s; as imagens trocam por etapa (pergunta 0,5–4 → toque 4–6,5 → revelação 6,5–9,5 → pódio 9,5–14)
    def stack(kind, key):
        blk = b[kind]
        layers = ''
        for s, (a, z) in {'q': (0, 4.0), 'tap': (4.0, 6.5), 'rev': (6.5, 9.5), 'pod': (9.5, T + 1)}.items():
            src = steps[s][key]
            layers += f'<img src="{src}" style="{"position:absolute;inset:0;width:100%;" if s != "q" else ""}display:block;{an(c.show(a, z if z < T else None))}">'
        tag = 'id="tvimg" ' if key == 'tv' else 'id="celimg" '
        import re
        return re.sub(r'<img ' + tag + r'src="[^"]*">', f'<div style="position:relative">{layers}</div>', blk)
    c.add(f'<div style="{an(c.enter(0.5, "rise", .7, 80))}">{stack("tv", "tv")}</div>')
    c.add(f'<div style="{an(c.enter(0.9, "right", .7, 120))}">{stack("ph", "cel")}</div>')
    # toque no celular aos 4 s (anel no centro do celular)
    x, y, w, _ = l['ph']; c.add(c.ring(x + w * .5, y + w * .62, 4.0, size=int(w * .45), color='rgba(14,42,34,.85)'))
    c.add(c.flash(6.5, '#fff', .25, .6)); c.add(c.flash(9.5, '#fff', .25, .6))
    if 'bichos' in b: c.add(f'<div style="{an(c.enter(6.7, "pop", .6))}">{b["bichos"]}</div>')
    c.add(f'<div style="{an(c.enter(7.0, "pop", .5))}">{b["bal0"]}</div>')
    c.add(f'<div style="{an(c.enter(8.0, "pop", .5))}">{b["bal1"]}</div>')
    if 'sub' in b: c.add(f'<div style="{an(c.enter(10.2, "rise", .7, 40))}">{b["sub"]}</div>')
    c.add(f'<div style="{an(c.enter(11.3, "pop", .6))}">{b["cta"]}</div>')
    c.add(f'<div style="{an(c.enter(11.6, "fade", .5))}">{b["url"]}</div>')
    if prev:
        return preview(c, prev, [0.1, 0.8, 2.0, 4.3, 6.0, 7.5, 9.0, 10.5, 12.0, 13.9], cols=5, scale=.22 if vf != 'wide' else .14)
    render(c, out, cover=cover)


if __name__ == '__main__':
    temas = list(TEMAS) if QUAL == 'all' else QUAL.split(',')
    for t in temas:
        I = TEMAS[t]['id'] + '-v1'; d = OUTM / 'ads' / I; d.mkdir(parents=True, exist_ok=True)
        if WHAT in ('hero', 'static', 'all', 'fix'):
            for f, suf in ((('story','story'),('land','land')) if WHAT=='fix' else (('feed45', 'feed45'), ('sq', 'sq'), ('story', 'story'), ('land', 'land'))[:1 if WHAT == 'hero' else 4]):
                static(t, f, d / f'{I}-{suf}.png'); print(t, f)
        if WHAT in ('video', 'all'):
            for vf, name in (('reel', None), ('feed', 'motion-feed45'), ('sq', 'motion-sq'), ('wide', 'motion-16x9')):
                if PREV:
                    print(video(t, vf, None, prev=Path('/tmp/claude-0/-home-claude-beyondtheworkproject/70ce8e8e-8c10-5997-ad90-074b6e8e0170/scratchpad/fam') / f'pv_{t}_{vf}.jpg')); continue
                out = (OUTM / f'{I}.mp4') if vf == 'reel' else (d / f'{I}-{name}.mp4')
                video(t, vf, out, cover=(OUTM / f'{I}-capa.jpg', 13.5) if vf == 'reel' else None)
                h = out.with_suffix('.html')
                if h.exists(): h.unlink()
                print(t, vf, 'ok')
