"""ADC-RK-01 v3 · monta o reel a partir da captura real (rk_capture.py).
Uso: python3 rk_compose.py <pasta da captura> <saída .mp4> <saída capa .jpg>"""
import base64, json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
CAP, OUT, CAPA = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
R = Path(__file__).resolve().parents[2]  # pipeline/
FONTS, SVG = R / 'fonts', R / 'assets' / 'sportdna'
W, H, FPS = 1080, 1920, 30
PX, PY, PW, PH, RAD = 150, 520, 780, 960, 40   # tela do produto (captura 2x de 390×480)
BG, ACC = '#0A0A0A', '#DDF247'
fr = json.loads((CAP / 'frames.json').read_text()); mk = json.loads((CAP / 'marks.json').read_text())
# cenas: (início no vídeo, duração, manchete, trecho da captura [a, b] em tempo do mundo)
S = [
 (0.0, 5.0, 'Qual raquete combina<br><em>com o seu jogo?</em>', (0.2, 5.2)),
 (5.0, 5.0, '19 a 28 perguntas sobre<br><em>corpo, braço e jogo.</em>', (mk['q1'] + 0.3, mk['q1'] + 5.3)),
 (10.0, 4.0, 'Até se o braço<br><em>já doeu.</em>', (mk['q2'] + 0.2, mk['q2'] + 4.2)),
 (14.0, 4.0, 'O teste cruza tudo com<br><em>183 raquetes.</em>', (mk['analysis'] + 0.05, mk['preview'] + 0.1)),
 (18.0, 5.0, 'As 3 que mais<br><em>combinam com você.</em>', (mk['preview'] + 1.2, mk['top3'] + 2.8)),
 (23.0, 4.5, 'E o que está<br><em>por trás da conta.</em>', (mk['tras_go'], mk['tras'] + 2.7)),
 (27.5, 4.5, 'Seu DNA de jogo<br><em>em um card.</em>', (mk['dna_go'], mk['dna'] + 2.7)),
]
END_T, END_D, FADE = 32.0, 3.6, 0.35
TOTAL = END_T + END_D

def ff(fam, f, w): return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{base64.b64encode((FONTS / f).read_bytes()).decode()}) format('woff2');font-weight:{w}}}"
CSS = ff('Archivo', 'Archivo-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700') + f"""
*{{margin:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;background:transparent;position:relative;color:#fff;font-family:'DM Sans'}}
h1{{position:absolute;left:70px;width:940px;top:300px;font:800 76px/1.04 Archivo;white-space:nowrap;letter-spacing:-.025em}} h1 em{{font-style:normal;color:{ACC}}}"""
def logo(h): 
    s = (SVG / 'racketdna-logo-fundo-escuro.svg').read_text(); return s.replace('<svg ', f'<svg height="{h}" style="width:auto" ', 1).replace('width="4344" height="512"', '')

def shot(pg, html, path, transparent=True):
    pg.set_content(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>{html}'); pg.evaluate('document.fonts.ready')
    pg.screenshot(path=str(path), omit_background=transparent)

work = CAP.parent / 'comp'; work.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
    for i, s in enumerate(S): shot(pg, f'<h1>{s[2]}</h1>', work / f'h{i}.png')
    shot(pg, f'<div style="position:absolute;left:0;right:0;top:1500px;display:flex;justify-content:center">{logo(46)}</div>', work / 'logo.png')
    shot(pg, f'''<div style="position:absolute;inset:0;background:{BG}"></div>
      <div style="position:absolute;left:0;right:0;top:560px;display:flex;justify-content:center">{logo(92)}</div>
      <h1 style="top:760px;left:40px;width:1000px;text-align:center;font-size:100px">Antes de comprar,<br><em>faça o teste.</em></h1>
      <div style="position:absolute;left:0;right:0;top:1100px;text-align:center"><span style="display:inline-block;background:{ACC};color:{BG};border-radius:999px;padding:22px 48px;font:700 50px 'DM Sans'">sportdna.com.br/racket</span></div>
      <p style="position:absolute;left:0;right:0;top:1250px;text-align:center;font:400 38px 'DM Sans';color:#A3A3A0">Você vê a prévia antes de pagar.</p>''', work / 'end.png', False)
    b.close()

def at(t):
    """quadro da captura no tempo t (mundo)."""
    lo, hi = 0, len(fr) - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if fr[m]['t'] <= t: lo = m
        else: hi = m - 1
    return CAP / 'f' / fr[lo]['f']

mask = Image.new('L', (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, PW - 1, PH - 1), RAD, fill=255)
base = Image.new('RGB', (W, H), BG); ImageDraw.Draw(base).rounded_rectangle((PX - 3, PY - 3, PX + PW + 2, PY + PH + 2), RAD + 3, fill='#2E2E2C')
heads = [Image.open(work / f'h{i}.png').convert('RGBA') for i in range(len(S))]
lg = Image.open(work / 'logo.png').convert('RGBA'); end = Image.open(work / 'end.png').convert('RGB')
ease = lambda k: 1 - (1 - min(1, max(0, k))) ** 3

def frame(t):
    if t >= END_T + FADE: return end
    i = max(j for j, s in enumerate(S) if t >= s[0] or j == 0) if t < END_T else len(S) - 1
    s0, d, _, (a, bb) = S[i]; k = min(1, (t - s0) / d)
    im = base.copy(); scr = Image.open(at(a + (bb - a) * k)).convert('RGB')
    if scr.size != (PW, PH): scr = scr.resize((PW, PH), Image.LANCZOS)
    im.paste(scr, (PX, PY), mask)
    e = 1 if i == 0 else ease((t - s0 - 0.18) / 0.42); o = min(1, (t - s0) / 0.18); h = heads[i]  # abertura: manchete já no 1º quadro
    if e < 1:
        if i > 0 and o < 1:  # manchete anterior sai rápido, antes da nova entrar
            prev = heads[i - 1].copy(); prev.putalpha(prev.getchannel('A').point(lambda v: int(v * (1 - o)))); im.paste(prev, (0, 0), prev)
        if e > 0:
            h = h.copy(); h.putalpha(h.getchannel('A').point(lambda v: int(v * e)))
            im.paste(h, (0, int(24 * (1 - e))), h)
    else: im.paste(h, (0, 0), h)
    im.paste(lg, (0, 0), lg)
    if t >= END_T: im = Image.blend(im, end, ease((t - END_T) / FADE))
    return im

N = int(round(TOTAL * FPS))
ff_ = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-an', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-r', str(FPS), '-movflags', '+faststart', str(OUT)], stdin=subprocess.PIPE)
for n in range(N): ff_.stdin.write(frame(n / FPS).tobytes())
ff_.stdin.close(); ff_.wait()
# capa: manchete de abertura + tela do resultado (top 3); arte importante no recorte 4:5 central
c = base.copy(); scr = Image.open(at(mk['top3'] + 1.5)).convert('RGB'); c.paste(scr, (PX, PY), mask); c.paste(heads[0], (0, 0), heads[0]); c.paste(lg, (0, 0), lg)
c.save(CAPA, quality=92)
print('ok', TOTAL, 's', N, 'frames')
