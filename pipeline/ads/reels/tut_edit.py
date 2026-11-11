"""Tutoriais Retrozap (11/11): monta o vídeo didático a partir da captura real (tut_cap.py).
Layout 9:16: faixa de cima com o passo e UMA instrução grande; celular grande com a tela real; zoom só onde ajuda a ler;
nota de rodapé quando precisa; prévia curta do resultado no começo; cartão final com URL e oferta conferida no site.
Sem áudio (deliberado). Uso: python3 tut_edit.py <grupo|casal> <pasta da captura> <saida.mp4> [preview]"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import *

RZ = A / 'retrozap'
TEMA = {
    'grupo': dict(bg='#1A0B2E', fg='#FFF4E0', hl='#FFC23C', sub='#CFC2EA', pill='#3D1A5C', blob=('#A98BFF', '#FF4F8B'), casa='grupo', ring='#FFC23C'),
    'casal': dict(bg='#FFF3EC', fg='#5E0B2B', hl='#E0245E', sub='#8A3A57', pill='#FFE6EC', blob=('#FFB59A', '#FF4F8B'), casa='casal', ring='#E0245E'),
}
FONTS = ff('Bricolage Grotesque', 'Bricolage-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700')
# celular: tela 9:16 (viewport 390×693 da captura)
PX, PY, PW, BZ = 170, 700, 740, 18
SW = PW - 2 * BZ; SH = SW * 16 / 9
QX, QY = 540, 1290  # ponto da tela que fica no centro do quadro quando há zoom


def junta(t):
    """Pontuação colada no destaque (o words() separa por espaço)."""
    return re.sub(r'\*([^*]+)\*([.,:;!?]+)', r'*\1\2*', t)


def build(modo, CAP, roteiro):
    th = TEMA[modo]
    css = f"""
.hd{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.03em;color:{th['fg']}}}
.hl{{color:{th['hl']}}}
.sb{{font-family:'DM Sans',sans-serif;font-weight:700;color:{th['fg']}}}
.chip{{font-family:'DM Sans',sans-serif;font-weight:700;letter-spacing:.06em;font-size:34px;color:{th['bg']};background:{th['hl']};border-radius:999px;padding:10px 26px;display:inline-block}}
.pill{{font-family:'DM Sans',sans-serif;font-weight:700;font-size:40px;line-height:1.22;color:{th['fg']};background:{th['pill']};border-radius:34px;padding:26px 34px;box-shadow:0 24px 60px rgba(0,0,0,.28);border:3px solid {th['hl']}55}}
.blob{{position:absolute;border-radius:50%;filter:blur(120px);opacity:.45}}
.tag{{font-family:'DM Sans',sans-serif;font-weight:700;font-size:28px;color:{th['sub']}}}
"""
    T = sum(s['dur'] for s in roteiro['cenas']) + roteiro['fim_dur']
    c = Comp('reel', T, th['bg'], FONTS, css)
    FR = Path(CAP) / 'cfr'
    cams, layers, tops = [], [], []
    t = 0.0

    def cam(fx=None, fy=None, s=1.0):
        if fx is None: return 'transform:translate(0px,0px) scale(1)'
        return f'transform:translate({QX - PX - s * (BZ + SW * fx):.1f}px,{QY - PY - s * (BZ + SH * fy):.1f}px) scale({s:.3f})'

    prev_txt = None
    for i, s in enumerate(roteiro['cenas']):
        t0, t1 = t, t + s['dur']
        layers.append(c.clip(FR, s['src'], t0, t1, s.get('rate', 1.0), style=f'position:absolute;inset:0;{c.an(c.show(t0, t1))}', hold=False))
        # câmera: corte rápido no começo da cena e movimento lento dentro dela
        pts = s.get('cam') or [(0, None, None, 1.0)]
        for k, (dt, fx, fy, z) in enumerate(pts):
            cams.append((t0 + dt + (0.001 if k == 0 and i else 0), cam(fx, fy, z), SNAP if k == 0 else EASE))
        # texto de cima (só reanima quando muda)
        key = (s.get('passo'), s.get('txt'))
        if s.get('txt') and key != prev_txt:
            fim = t1
            for s2 in roteiro['cenas'][i + 1:]:
                if (s2.get('passo'), s2.get('txt')) != key: break
                fim += s2['dur']
            big = s.get('big', 76)
            tops.append(f'<div class="abs" style="left:70px;top:{205 if s.get("passo") else 240}px;width:940px;z-index:30;{c.an(c.show(t0, fim))}">'
                        + (f'<div style="{c.an(c.enter(t0, "left", .35))}"><span class="chip">{s["passo"]}</span></div>' if s.get('passo') else '')
                        + c.words(junta(s['txt']), t0 + .08 if t0 else -.5, size=big, cls='hd', step=.035, dur=.35, lh=1.04, style='margin-top:22px') + '</div>')
        prev_txt = key
        for (dt, d, txt) in s.get('notas', []):
            a = t0 + dt; b = min(t1, a + d) if d else t1
            tops.append(f'<div class="abs" style="left:90px;right:90px;bottom:{s.get("nota_y", 120)}px;z-index:35;{c.an(c.show(a, b, fout=.2), c.enter(a, "rise", .4, 40))}"><div class="pill">{txt}</div></div>')
        t = t1
    if cams[0][0] > 0: cams.insert(0, (0, cam(), EASE))
    k = c.kf(cams, EASE)
    tela = ''.join(layers)
    ph = (f'<div class="abs" style="left:{PX}px;top:{PY}px;transform-origin:0 0;z-index:10;{c.an(k, c.show(0, t))}">{c.phone(tela, PW, bezel=BZ, radius=96, notch=False)}</div>')
    # faixa de cima (fundo sólido para o texto ficar sempre legível, mesmo com zoom)
    faixa = (f'<div class="abs" style="left:0;top:0;width:1080px;height:640px;z-index:20;background:linear-gradient({th["bg"]} 0%,{th["bg"]} 86%,{th["bg"]}00);{c.an(c.show(0, t))}"></div>'
             f'<div class="abs" style="left:70px;top:92px;z-index:31;display:flex;align-items:center;gap:26px;{c.an(c.show(0, t))}">{svg(RZ / f"logo-assinatura-{th["casa"]}.svg", h=64)}'
             f'<span class="tag">{roteiro["etiqueta"]}</span></div>')
    blobs = (f'<div class="blob" style="left:-260px;top:520px;width:760px;height:760px;background:{th["blob"][0]}"></div>'
             f'<div class="blob" style="right:-300px;top:1240px;width:800px;height:800px;background:{th["blob"][1]};opacity:.3"></div>')
    c.layers.insert(0, blobs + ph + faixa + ''.join(tops))
    # cartão final
    tf = t; f = roteiro['fim']
    c.add(c.wipe(tf, th['hl'], .55, 'up'))
    c.add(f'<div class="fill" style="background:{th["bg"]};z-index:45;{c.an(c.show(tf))}">'
          f'<div class="blob" style="left:-260px;top:1000px;width:700px;height:700px;background:{th["blob"][0]}"></div>'
          f'<div class="abs" style="right:-120px;bottom:180px;opacity:.12"><div style="{c.an(c.enter(tf + .1, "pop", .7))}">{svg(RZ / f"logo-simbolo-{th["casa"]}.svg", w=620)}</div></div>'
          f'<div class="abs" style="left:90px;top:420px;{c.an(c.enter(tf + .15, "left", .45))}">{svg(RZ / f"logo-assinatura-{th["casa"]}.svg", h=96)}</div>'
          + c.words(junta(f['titulo']), tf + .25, 90, 600, 900, size=118, cls='hd', step=.06, dur=.4, lh=1.0)
          + f'<div class="abs" style="left:90px;top:{600 + 118 * (f["titulo"].count(chr(10)) + 1) + 70}px;width:900px;{c.an(c.enter(tf + .9, "pop", .45))}">'
            f'<span class="sb" style="display:inline-block;font-size:62px;background:{th["hl"]};color:{th["bg"]};border-radius:999px;padding:16px 44px">retrozap.com.br</span>'
            f'<div class="sb" style="font-size:44px;line-height:1.25;margin-top:44px;color:{th["fg"]}">{f["oferta"]}</div></div>'
          + '</div>')
    return c


def srt(roteiro, out):
    """Legendas (SRT) com o texto de cada cena e as notas, nos tempos do vídeo."""
    def ts(x):
        ms = int(round(x * 1000)); h, r = divmod(ms, 3600000); m, r = divmod(r, 60000); s, ms = divmod(r, 1000); return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
    limpa = lambda t: re.sub(r'<[^>]+>', '', t.replace('*', '')).replace('\n', ' ')
    blocos, t, prev = [], 0.0, None
    for s in roteiro['cenas']:
        txt = limpa(s.get('txt', '')) + ''.join(' ' + limpa(n[2]) for n in s.get('notas', []))
        if blocos and txt == prev: blocos[-1][1] = t + s['dur']
        else: blocos.append([t, t + s['dur'], txt])
        prev = txt; t += s['dur']
    f = roteiro['fim']; blocos.append([t, t + roteiro['fim_dur'], limpa(f['titulo']) + ' retrozap.com.br. ' + limpa(f['oferta'].replace('<br>', ' '))])
    Path(out).write_text('\n'.join(f'{i}\n{ts(a)} --> {ts(b)}\n{x}\n' for i, (a, b, x) in enumerate(blocos, 1)))


if __name__ == '__main__':
    modo, CAP, OUT = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    modo, _, how = modo.partition(':')  # grupo | casal | grupo:iphone | casal:android (complementos)
    import importlib.util
    spec = importlib.util.spec_from_file_location('r', Path(__file__).with_name(f'tut_roteiro_{modo}.py')); r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
    frames(CAP / 'raw.mp4', CAP / 'cfr')
    mk = json.load(open(CAP / 'capture.json'))['marks']
    R = r.roteiro(mk, how) if how else r.roteiro(mk)
    c = build(modo, CAP, R)
    print('duração', c.T)
    srt(R, OUT.with_suffix('.srt'))
    if len(sys.argv) > 4:
        print(preview(c, OUT.with_name(OUT.stem + '-prev.jpg'), [i * 1.0 + .6 for i in range(int(c.T))], cols=10, scale=.18))
    else:
        render(c, OUT, cover=(OUT.with_name(OUT.stem + '-capa.jpg'), 0.05))
