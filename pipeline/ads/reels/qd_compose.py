"""ADC-QD-01 v3: monta o reel 9:16 a partir das gravações reais (qd_capture.py).
Uso: python3 qd_compose.py <pasta da captura> <saida.mp4> <capa.jpg>"""
import base64, json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

P = Path(__file__).resolve().parents[2]
CAP, OUTV, OUTC = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
M = json.loads((CAP / 'marcas.json').read_text()); OFF = M['t_offset']
TMP = CAP / 'cmp'; TMP.mkdir(exist_ok=True)
def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
FONTS = (f"@font-face{{font-family:Fraunces;src:url(data:font/woff2;base64,{b64(P/'fonts/Fraunces-900.woff2')}) format('woff2');font-weight:900}}"
         f"@font-face{{font-family:Nunito;src:url(data:font/woff2;base64,{b64(P/'fonts/Nunito-var.woff2')}) format('woff2');font-weight:600 900}}")
LOGO = (P / 'assets/quiddo/quiddo-cor.svg').read_text()
INK, CREME, AMAR = '#0E2A22', '#FFF6E6', '#FFC83D'

# cena: (rótulo, duração, [(fonte, t0 no relógio da TV, crop x,y,w,h, destino x,y,w)], tipo de moldura)
L, Q, R, PD = (410, 0, 1100, 1050), (410, 70, 1100, 710), (410, 70, 1100, 760), (410, 120, 1100, 780)
CEL = (0, 0, 480, 1040)
def tv(t, crop): return [('tv', t, crop, (60, 450, 960))]
def cel(t): return [('cel', t, CEL, (285, 440, 510))]
T1, T2, T3, T4 = 'A turma entra pelo celular. Sem app, sem cadastro.', 'Todo mundo responde ao mesmo tempo.', 'A resposta certa aparece na hora.', 'No fim, o pódio. E você vê quem entendeu.'
S = [
  ('abre', 3.4, [], None),
  ('Você escreve as perguntas do treinamento.', 4.0, [('tv', M['tv_abrir'] - 4.3, (560, 0, 800, 1080), (139, 450, 802))], 'tv'),
  (T1, 4.4, cel(M['cel_form'] + 1.6), 'cel'),
  (T1, 3.0, tv(M['q0_prep'] - 4.2, L), 'tv'),
  (T2, 3.4, tv(M['q0_resp'] - 0.2, Q), 'tv'),
  (T2, 3.4, cel(M['q0_mari'] - 1.6), 'cel'),
  (T3, 3.0, tv(M['q0_reveal'] + 1.2, R), 'tv'),
  (T3, 3.0, cel(M['q0_reveal'] + 2.6), 'cel'),
  (T4, 5.2, tv(M['podio'] + 6.0, PD), 'tv'),
  ('fecha', 3.4, [], None),
]

def page(html, out):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(html); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200); pg.screenshot(path=str(out), omit_background=False); b.close()

BASE = f"""<style>{FONTS}*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1920px;background:{CREME};font-family:Nunito;color:{INK};position:relative;overflow:hidden}}
.lb{{position:absolute;left:70px;right:70px;top:270px;font:900 54px/1.08 Fraunces;letter-spacing:-.02em}}
.mt{{display:inline-block;background:{AMAR};padding:0 .14em;transform:rotate(-2deg);border-radius:.08em}}
.fr{{position:absolute;border:8px solid {INK};border-radius:22px;box-shadow:0 12px 0 {INK};background:#fff}}
.ph{{position:absolute;border:14px solid #111;border-radius:46px;background:#111;box-shadow:0 18px 40px rgba(0,0,0,.25)}}</style>"""

def bg(i, label, items, kind):
    if label == 'abre':
        body = (f"<div style='position:absolute;left:80px;top:300px'>{LOGO.replace('<svg', '<svg width=\"300\"', 1)}</div>"
                f"<div class='lb' style='top:560px;font-size:118px;line-height:1.0'>Treinamento com a sala no celular?</div>"
                f"<div class='lb' style='top:1100px;font-size:118px'><span class='mt'>Use a favor.</span></div>")
    elif label == 'fecha':
        body = (f"<div class='lb' style='top:420px;font-size:120px;line-height:1.0'>Faça o seu.<br><span class='mt'>Teste grátis.</span></div>"
                f"<div style='position:absolute;left:80px;top:920px;display:inline-block;background:{INK};color:#fff;border-radius:999px;padding:24px 50px;font:900 58px Nunito'>quiddo.com.br</div>"
                f"<div style='position:absolute;left:80px;top:1180px'>{LOGO.replace('<svg', '<svg width=\"420\"', 1)}</div>")
    else:
        body = f"<div class='lb'>{label}</div>"
        for src, t, (cx, cy, cw, ch), (dx, dy, dw) in items:
            dh = round(ch * dw / cw)
            cls, pad = ('fr', 8) if src == 'tv' else ('ph', 14)
            body += f"<div class='{cls}' style='left:{dx-pad}px;top:{dy-pad}px;width:{dw+2*pad}px;height:{dh+2*pad}px'></div>"
    out = TMP / f'bg{i}.png'; page(BASE + body, out); return out

clips = []
for i, (label, dur, items, kind) in enumerate(S):
    png = bg(i, label, items, kind)
    args = ['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', f'{dur}', '-framerate', '30', '-i', str(png)]
    fc = []; last = '0:v'
    for k, (src, t, (cx, cy, cw, ch), (dx, dy, dw)) in enumerate(items):
        ts = t if src == 'tv' else t - OFF
        args += ['-ss', f'{ts:.3f}', '-t', f'{dur}', '-i', str(CAP / f'{src}.mp4')]
        dh = round(ch * dw / cw); dh += dh % 2; dw2 = dw + dw % 2
        fc.append(f'[{k+1}:v]crop={cw}:{ch}:{cx}:{cy},scale={dw2}:{dh}:flags=lanczos,setpts=PTS-STARTPTS[v{k}]')
        fc.append(f'[{last}][v{k}]overlay={dx}:{dy}:eof_action=repeat[o{k}]'); last = f'o{k}'
    fc.append(f'[{last}]fade=in:st=0:d=0.25:color=0xFFF6E6,fade=out:st={dur-0.25:.2f}:d=0.25:color=0xFFF6E6,format=yuv420p[out]')
    o = TMP / f'c{i}.mp4'
    subprocess.run(args + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-r', '30', '-t', f'{dur}', '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', str(o)], check=True)
    clips.append(o)
lst = TMP / 'lista.txt'; lst.write_text(''.join(f"file '{c}'\n" for c in clips))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-an', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', '-r', '30', '-movflags', '+faststart', str(OUTV)], check=True)
# capa: manchete + pódio real
t = M['podio'] + 8.0
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t}', '-i', str(CAP / 'tv.mp4'), '-frames:v', '1', str(TMP / 'podio.png')], check=True)
html = BASE + (f"<div style='position:absolute;left:80px;top:300px'>{LOGO.replace('<svg', '<svg width=\"240\"', 1)}</div>"
               f"<div class='lb' style='top:470px;font-size:84px;line-height:1.02'>Treinamento com a sala no celular? <span class='mt'>Use a favor.</span></div>"
               f"<div class='fr' style='left:52px;top:842px;width:976px;height:{round(780*960/1100)+16}px;overflow:hidden'>"
               f"<img src='data:image/png;base64,{b64(TMP/'podio.png')}' style='position:absolute;left:{-410*960/1100:.1f}px;top:{-120*960/1100:.1f}px;width:{1920*960/1100:.1f}px'></div>")
page(html, TMP / 'capa.png')
from PIL import Image
Image.open(TMP / 'capa.png').convert('RGB').save(OUTC, quality=90)
print(OUTV, sum(s[1] for s in S))
