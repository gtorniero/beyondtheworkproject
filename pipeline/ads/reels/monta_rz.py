"""Monta os reels ADC-RZ-01-v3 e ADC-RZ-02-v2 a partir da captura real (raw.mp4 + marcas).
RZ-01: tela inteira do celular numa moldura, manchete em cima (Noite). RZ-02: tela em tela cheia, reenquadrada com zoom lento, legenda em caixa Manga.
Sem áudio. Uso: python3 monta_rz.py <pasta da captura> <pasta de saída das mídias>"""
import base64, json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
CAP, OUT = Path(sys.argv[1]), Path(sys.argv[2]); TMP = CAP / 'comp'; TMP.mkdir(exist_ok=True)
R = Path(__file__).resolve().parents[2]; F = R / 'fonts'; A = R / 'assets' / 'retrozap'
M = json.load(open(CAP / 'capture.json'))['marks']; RAW = str(CAP / 'raw.mp4')
ff = lambda fam, f, w: f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{base64.b64encode((F / f).read_bytes()).decode()}) format('woff2');font-weight:{w}}}"
FONTS = ff('Bricolage', 'Bricolage-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700') + ff('DM Mono', 'DMMono-Medium.woff2', '500')
ASS = (A / 'logo-assinatura-grupo.svg').read_text()
NOITE, MANGA, AREIA = '#1A0B2E', '#FFC23C', '#FFF4E0'
CSS = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;background:transparent}}
.hd{{font-family:Bricolage;font-weight:800;letter-spacing:-.03em;line-height:1.02}} .hl{{color:{MANGA}}} .abs{{position:absolute}}"""

def png(html, out, transparent=False):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>{html}'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
        pg.screenshot(path=str(out), omit_background=transparent); b.close()
    return str(out)

ENC = ['-an', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', '-r', '30']
def run(args): subprocess.run(['ffmpeg', '-y', '-v', 'error', *args], check=True)

# ---------------- RZ-01: moldura de celular
PW, PH, PX, PY = 620, 1102, 230, 500  # tela 390×693 escalada 1,59×
def rz01_bg(txt, out):
    return png(f'<div style="width:1080px;height:1920px;background:{NOITE}"></div>'
               f'<div class="abs hd" style="left:80px;top:285px;width:920px;font-size:72px;color:{AREIA}">{txt}</div>', out)
def rz01_fg(out):  # cantos arredondados + borda da moldura por cima do vídeo
    return png(f'<div class="abs" style="left:{PX-10}px;top:{PY-10}px;width:{PW+20}px;height:{PH+20}px;border-radius:58px;border:10px solid #0B0414;'
               f'box-shadow:0 0 0 26px {NOITE},0 30px 80px rgba(0,0,0,.5)"></div>', out, transparent=True)
def rz01_seg(i, txt, t0, t1):
    bg = rz01_bg(txt, TMP / f'r1bg{i}.png'); d = t1 - t0; o = TMP / f'r1s{i}.mp4'
    run(['-loop', '1', '-t', f'{d:.2f}', '-i', bg, '-ss', f'{t0:.2f}', '-t', f'{d:.2f}', '-i', RAW, '-loop', '1', '-t', f'{d:.2f}', '-i', str(TMP / 'r1fg.png'),
         '-filter_complex', f'[1:v]scale={PW}:{PH}:flags=lanczos[v];[0:v][v]overlay={PX}:{PY}[a];[a][2:v]overlay=0:0,fps=30,format=yuv420p', '-t', f'{d:.2f}', *ENC, str(o)])
    return o, d

# ---------------- RZ-02: tela cheia reenquadrada
VY, VH = 470, 1100  # faixa do vídeo
def rz02_bg(txt, out):
    return png(f'<div style="width:1080px;height:1920px;background:{NOITE}"></div>'
               f'<div class="abs" style="left:70px;top:290px;max-width:940px;background:{MANGA};color:{NOITE};border-radius:22px;padding:16px 28px 20px;box-shadow:0 10px 0 rgba(0,0,0,.35)">'
               f'<div class="hd" style="font-size:58px">{txt}</div></div>'
               f'<div class="abs" style="left:80px;top:1610px;transform:scale(.62);transform-origin:left top">{ASS}</div>', out)
def rz02_fade(out):  # bordas suaves na faixa do vídeo (lista que rola some no fundo, sem corte seco)
    return png(f'<div class="abs" style="left:0;top:{VY}px;width:1080px;height:60px;background:linear-gradient({NOITE},rgba(26,11,46,0))"></div>'
               f'<div class="abs" style="left:0;top:{VY+VH-60}px;width:1080px;height:60px;background:linear-gradient(rgba(26,11,46,0),{NOITE})"></div>', out, transparent=True)
def rz02_clip(src_t0, d, y0, y1, out):
    """reenquadra a faixa [y0,y1] do quadro real (bordas em espaço vazio da tela) e encaixa em 1080×VH, centralizado, sem cortar nada."""
    h = y1 - y0; f = min(1.0, VH / h); w2, h2 = int(1080 * f) // 2 * 2, int(h * f) // 2 * 2
    run(['-ss', f'{src_t0:.2f}', '-t', f'{d:.2f}', '-i', RAW, '-vf',
         f"fps=30,crop=1080:{h}:0:{y0},scale={w2}:{h2}:flags=lanczos,pad=1080:{VH}:(ow-iw)/2:(oh-ih)/2:{NOITE}", *ENC, str(out)])
def rz02_seg(i, caps, partes):
    """partes: lista de (t0, t1, y0, y1) concatenadas na mesma cena (mesmo fundo/legendas)."""
    clips = []
    for k, (t0, t1, y0, y1) in enumerate(partes):
        c = TMP / f'r2c{i}_{k}.mp4'; rz02_clip(t0, t1 - t0, y0, y1, c); clips.append(c)
    clip = TMP / f'r2c{i}.mp4'
    if len(clips) > 1:
        (TMP / f'r2c{i}.txt').write_text(''.join(f"file '{c}'\n" for c in clips))
        run(['-f', 'concat', '-safe', '0', '-i', str(TMP / f'r2c{i}.txt'), *ENC, str(clip)])
    else: clip = clips[0]
    d = sum(t1 - t0 for t0, t1, _, _ in partes); o = TMP / f'r2s{i}.mp4'
    ins, fc = [], ''
    bgs = [rz02_bg(c, TMP / f'r2bg{i}_{k}.png') for k, (c, _, _) in enumerate(caps)]
    for b_ in bgs: ins += ['-loop', '1', '-t', f'{d:.2f}', '-i', b_]
    ins += ['-i', str(clip), '-loop', '1', '-t', f'{d:.2f}', '-i', str(TMP / 'r2fade.png')]
    base = '[0:v]'
    for k, (c, a_, z_) in enumerate(caps[1:], 1):
        fc += f"{base}[{k}:v]overlay=0:0:enable='between(t,{a_},{z_})'[b{k}];"; base = f'[b{k}]'
    fc += f"{base}[{len(bgs)}:v]overlay=0:{VY}[v];[v][{len(bgs)+1}:v]overlay=0:0,format=yuv420p"
    run([*ins, '-filter_complex', fc, '-t', f'{d:.2f}', *ENC, str(o)])
    return o, d

def cta(out_png, big, theme):
    if theme == 1:
        html = (f'<div style="width:1080px;height:1920px;background:{NOITE}"></div>'
                f'<div class="abs" style="left:80px;top:420px">{ASS}</div>'
                f'<div class="abs hd" style="left:80px;top:640px;width:920px;font-size:104px;color:{AREIA}">{big}</div>'
                f'<div class="abs" style="left:80px;top:1130px;background:{MANGA};color:{NOITE};border-radius:999px;padding:24px 48px;font:700 52px DM Sans">retrozap.com.br</div>')
    else:
        html = (f'<div style="width:1080px;height:1920px;background:{MANGA}"></div>'
                f'<div class="abs" style="left:80px;top:400px;border-radius:24px;overflow:hidden">{ASS}</div>'
                f'<div class="abs hd" style="left:80px;top:620px;width:920px;font-size:104px;color:{NOITE}">{big}</div>'
                f'<div class="abs" style="left:80px;top:1150px;background:{NOITE};color:{MANGA};border-radius:999px;padding:24px 48px;font:700 52px DM Sans">retrozap.com.br</div>')
    return png(html, out_png)
def cta_seg(name, big, theme, d=4.5):
    p = cta(TMP / f'{name}.png', big, theme); o = TMP / f'{name}.mp4'
    run(['-loop', '1', '-t', f'{d}', '-i', p, '-vf', 'fps=30,fade=t=in:st=0:d=0.35,format=yuv420p', *ENC, str(o)]); return o, d

def junta(segs, out):
    lst = TMP / (out.stem + '.txt'); lst.write_text(''.join(f"file '{s}'\n" for s, _ in segs))
    run(['-f', 'concat', '-safe', '0', '-i', str(lst), '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', '-r', '30', '-an', '-movflags', '+faststart', str(out)])
    return sum(d for _, d in segs)

if __name__ == '__main__':
    quais = sys.argv[3:] or ['RZ-01', 'RZ-02']
    if 'RZ-01' in quais:
        rz01_fg(TMP / 'r1fg.png')
        s = [rz01_seg(0, 'Seu WhatsApp de 2026 <span class="hl">virou premiação.</span>', M['p1_rvl'] + .25, M['p1_rvl'] + 4.6),
             rz01_seg(1, 'Exporta a conversa do grupo <span class="hl">e escolhe o arquivo.</span>', M['arquivo'] - .95, M['turma'] + 1.4),
             rz01_seg(2, 'Troféu por troféu, <span class="hl">revelado na hora.</span>', M['p2'] + .7, M['p2_fim'] - .25),
             rz01_seg(3, 'Tem troféu que você <span class="hl">raspa pra descobrir.</span>', M['p3_raspa'] - .6, M['p3_raspa'] + 6.2),
             cta_seg('r1cta', 'Faça a retrospectiva <span class="hl">do seu grupo.</span>', 1)]
        print('RZ-01', round(junta(s, OUT / 'ADC-RZ-01-v3.mp4'), 2))
    if 'RZ-02' in quais:
        rz02_fade(TMP / 'r2fade.png')
        s = [rz02_seg(0, [('Retrospectiva 2026 do seu grupo no WhatsApp.', 0, 0), ('Dá o seu palpite. O site revela.', M['p4_palpite'] - M['p4'] - .3, 99)],
                      [(M['p4'] + .4, M['p4_palpite'] + .1, 330, 1530), (M['p4_palpite'] + .1, M['p4_palpite'] + 4.2, 155, 1300)]),
             rz02_seg(1, [('O site lê o ano todo e conta tudo.', 0, 0)], [(M['ato1'] + .3, M['ato1'] + 6.4, 190, 1290)]),
             rz02_seg(2, [('8 troféus em disputa no grupo.', 0, 0)], [(M['categorias'] + .2, M['categorias'] + 6.2, 190, 1290)]),
             rz02_seg(3, [('Card pronto pro grupo.', 0, 0)], [(M['card'] + .25, M['card_fim'], 10, 1160)]),
             rz02_seg(4, [('E 2026 em números.', 0, 0)], [(M['finale'] + .25, M['f1'] - .05, 190, 1460)]),
             cta_seg('r2cta', 'Faça a retrospectiva 2026 do seu grupo.', 2)]
        print('RZ-02', round(junta(s, OUT / 'ADC-RZ-02-v2.mp4'), 2))
    # capas 9:16 (quadro do próprio vídeo)
    for v, t in (('ADC-RZ-01-v3', 2.8), ('ADC-RZ-02-v2', 1.6)):
        if (OUT / f'{v}.mp4').exists(): run(['-ss', str(t), '-i', str(OUT / f'{v}.mp4'), '-frames:v', '1', '-q:v', '2', str(OUT / f'{v}-capa.jpg')])
