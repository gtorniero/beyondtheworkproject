"""Reels Quiddo educação (17/11): abertura com clipe de banco NOVO (diferente em cada Reel) + partida REAL gravada no Quiddo (celular e telão) + CTA.
Uso: python3 reels.py → out/QE-R*.mp4 + capas"""
import asyncio, base64, io, json, subprocess, sys
from pathlib import Path
from PIL import Image
H = Path(__file__).resolve().parent; W = H.parent; CL = W / 'clips2'; MK = W.parent / 'mk'; OUT = H / 'out'; OUT.mkdir(exist_ok=True); TMP = H / 'tmp'; TMP.mkdir(exist_ok=True)
sys.path.insert(0, str(W.parent / 'social' / 'pipeline'))
FD = W.parent / 'social' / 'pipeline' / 'fonts'
def font(fam, f, w): return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{base64.b64encode((FD / f).read_bytes()).decode()}) format('woff2');font-weight:{w}}}"
FONTS = font('Fraunces', 'Fraunces-900.woff2', 900) + font('Nunito', 'Nunito-var.woff2', '200 1000')
LOGO = (W.parent / 'social' / 'pipeline' / 'assets' / 'quiddo' / 'quiddo-negativo.svg').read_text()
def run(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *map(str, a)], check=True)
def b64(p):
    im = Image.open(p).convert('RGB'); bf = io.BytesIO(); im.save(bf, 'JPEG', quality=90); return 'data:image/jpeg;base64,' + base64.b64encode(bf.getvalue()).decode()

R = [
 dict(id='QE-R1', cap='geo', clip=('sala_de_aula', '35954', 3.0), track=('830', 2.0), bg='#0B5D45',
      t=['A revisão de Geografia virou jogo.', 'Cada aluno responde no celular.', 'A resposta aparece no telão.', 'Ranking e pódio na hora.'],
      cta='Monte o quiz da sua aula.'),
 dict(id='QE-R2', cap='hist', clip=('sala_de_aula', '48165', 1.0), track=('801', 1.0), bg='#1E4FC2',
      t=['História do Brasil, valendo pódio.', 'A turma toda responde junta.', 'No telão: 1888, Lei Áurea.', 'Quem acertou mais sobe.'],
      cta='Monte o quiz da sua aula.'),
 dict(id='QE-R3', cap='port', clip=('sala_de_aula', '6676', 4.0), track=('5', 0.0), bg='#14163A',
      t=['Proparoxítona? A sala respondeu em segundos.', 'Cada um no seu celular.', 'Lâmpada: a resposta no telão.', 'Revisão de Português com pódio.'],
      cta='Monte o quiz da sua aula.'),
 dict(id='QE-R4', cap='treino', clip=('treinamento', '45957', 2.0), track=('1057', 0.0), bg='#3A3FC2',
      t=['O treinamento que a equipe não esquece.', 'A equipe responde pelo celular.', 'A resposta certa no telão.', 'Ranking da turma na hora.'],
      cta='Transforme o treinamento em quiz.'),
]
D = [2.8, 3.6, 3.0, 2.6, 2.8]

def cap_html(txt, bg=None, top=150):
    return f"""<html><style>{FONTS}body{{margin:0;width:1080px;height:1920px;{'background:' + bg if bg else 'background:linear-gradient(180deg,rgba(0,0,0,.72) 0,rgba(0,0,0,.5) 520px,rgba(0,0,0,0) 900px)'}}}
.c{{position:absolute;left:80px;top:{top}px;width:920px;font-family:Fraunces;font-weight:900;font-size:86px;line-height:1.02;color:#fff;letter-spacing:-.01em;text-shadow:0 4px 30px rgba(0,0,0,.35)}}</style><div class="c">{txt}</div></html>"""

def bezel_html():
    return """<html><style>body{margin:0;width:1080px;height:1920px;background:transparent}</style>
<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><defs><mask id="m"><rect width="1080" height="1920" fill="#fff"/><rect x="160" y="440" width="760" height="1340" rx="56" fill="#000"/></mask></defs>
<rect x="140" y="420" width="800" height="1380" rx="74" fill="#141414" mask="url(#m)"/><rect x="140" y="420" width="800" height="1380" rx="74" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="4"/></svg></html>"""

def tv_html(r, img, txt):
    return f"""<html><style>{FONTS}body{{margin:0;width:1080px;height:1920px;background:{r['bg']}}}
.c{{position:absolute;left:80px;top:150px;width:920px;font-family:Fraunces;font-weight:900;font-size:86px;line-height:1.02;color:#fff}}</style>
<div class="c">{txt}</div><div style="position:absolute;left:50px;top:640px;width:980px"><div style="background:#111;border-radius:24px;padding:18px;box-shadow:0 40px 90px rgba(0,0,0,.5)"><img src="{img}" style="display:block;width:100%;border-radius:10px"></div>
<div style="margin:0 auto;width:150px;height:46px;background:#111"></div><div style="margin:0 auto;width:380px;height:18px;border-radius:9px;background:#111"></div></div></html>"""

def cta_html(r, img):
    return f"""<html><style>{FONTS}body{{margin:0;width:1080px;height:1920px;background:{r['bg']};font-family:Nunito}}</style>
<div style="position:absolute;left:80px;top:170px;width:300px">{LOGO.replace('<svg', '<svg width="300" height="100"', 1)}</div>
<div style="position:absolute;left:80px;top:340px;width:920px;font-family:Fraunces;font-weight:900;font-size:104px;line-height:1;color:#fff">{r['cta']}</div>
<div style="position:absolute;left:180px;top:760px;width:720px"><div style="background:#111;border-radius:22px;padding:14px"><img src="{img}" style="display:block;width:100%;border-radius:8px"></div><div style="margin:0 auto;width:110px;height:34px;background:#111"></div><div style="margin:0 auto;width:280px;height:14px;border-radius:7px;background:#111"></div></div>
<div style="position:absolute;left:80px;top:1340px;width:920px;font-size:40px;font-weight:800;color:#fff;line-height:1.3">A turma responde pelo celular, sem baixar app. Grátis até 10 pessoas.</div>
<div style="position:absolute;left:80px;top:1500px;width:920px;height:150px;border-radius:34px;background:#FFC83D;color:#0E2A22;display:flex;align-items:center;justify-content:center;font-family:Fraunces;font-weight:900;font-size:66px">Criar meu quiz grátis →</div>
<div style="position:absolute;left:80px;top:1690px;width:920px;text-align:center;font-size:44px;font-weight:900;color:#fff">quiddo.com.br</div></html>"""

async def shots(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for html, path, transp in jobs:
            await pg.set_content(html); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(120)
            await pg.screenshot(path=str(path), omit_background=transp)
        await b.close()

ENC = ['-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30']
for r in [x for x in R if len(sys.argv) < 2 or x['id'] in sys.argv[1:]]:
    i = r['id']; cap = H / r['cap']; m = json.loads((cap / 'marcas.json').read_text())
    rev = m['q0_reveal']; hero = m['q0_hero']; pod = m['podio2']
    jobs = [(cap_html(r['t'][0], top=170), TMP / f'{i}-c1.png', True), (cap_html(r['t'][1], r['bg']), TMP / f'{i}-bg2.png', False), (bezel_html(), TMP / 'bezel.png', True),
            (cap_html(r['t'][3], r['bg']), TMP / f'{i}-bg4.png', False), (tv_html(r, b64(cap / 'tv_q0_rev.png'), r['t'][2]), TMP / f'{i}-s3.png', False),
            (cta_html(r, b64(cap / ('tv_q1_rank.png' if (cap / 'tv_q1_rank.png').exists() else 'tv_q0_rev.png'))), TMP / f'{i}-s5.png', False)]
    asyncio.run(shots(jobs))
    th, cid, ss = r['clip']; src = CL / th / f'{cid}.mp4'
    # S1: clipe de banco, recorte 9:16, escurecido embaixo do título
    run('-ss', ss, '-i', src, '-i', TMP / f'{i}-c1.png', '-filter_complex',
        f"[0:v]scale=-2:1920,crop=1080:1920,eq=brightness=-0.06:saturation=1.1,setsar=1,fps=30[v];[v][1:v]overlay=0:0,trim=0:{D[0]},setpts=PTS-STARTPTS[o]",
        '-map', '[o]', *ENC, '-t', D[0], TMP / f'{i}-1.mp4')
    # S2: celular real (toque + "Mandou bem"), câmera lenta da captura volta ao normal (×2)
    a0, a1 = hero - 1.3, hero + 1.5; b0 = rev + 4.0; b1 = b0 + (D[1] - (a1 - a0) / 2) * 2
    cel = cap / 'cel.mp4'
    run('-i', TMP / f'{i}-bg2.png', '-i', cel, '-i', TMP / 'bezel.png', '-filter_complex',
        f"[1:v]split[x][y];[x]trim={a0}:{a1},setpts=(PTS-STARTPTS)/2[p];[y]trim={b0}:{b1},setpts=(PTS-STARTPTS)/2[q];[p][q]concat=n=2:v=1:a=0,crop=1080:1904:0:0,scale=760:1340,fps=30[c];"
        f"[0:v]loop=-1:1,fps=30[b];[b][c]overlay=160:440:shortest=1[v];[v][2:v]overlay=0:0,trim=0:{D[1]},setpts=PTS-STARTPTS[o]", '-map', '[o]', *ENC, '-t', D[1], TMP / f'{i}-2.mp4')
    # S3: telão real com zoom lento
    run('-loop', '1', '-i', TMP / f'{i}-s3.png', '-filter_complex', f"[0:v]scale=2160:3840,zoompan=z='1+0.035*on/{int(D[2] * 30)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,trim=0:{D[2]}[o]",
        '-map', '[o]', *ENC, '-t', D[2], TMP / f'{i}-3.mp4')
    # S4: pódio real no celular
    run('-i', TMP / f'{i}-bg4.png', '-i', cel, '-i', TMP / 'bezel.png', '-filter_complex',
        f"[1:v]trim={pod}:{pod + D[3] * 2},setpts=(PTS-STARTPTS)/2,crop=1080:1904:0:0,scale=760:1340,fps=30[c];[0:v]loop=-1:1,fps=30[b];[b][c]overlay=160:440:shortest=1[v];[v][2:v]overlay=0:0,trim=0:{D[3]},setpts=PTS-STARTPTS[o]",
        '-map', '[o]', *ENC, '-t', D[3], TMP / f'{i}-4.mp4')
    # S5: CTA
    run('-loop', '1', '-i', TMP / f'{i}-s5.png', '-filter_complex', f"[0:v]scale=2160:3840,zoompan=z='1.03-0.03*on/{int(D[4] * 30)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,trim=0:{D[4]}[o]",
        '-map', '[o]', *ENC, '-t', D[4], TMP / f'{i}-5.mp4')
    lst = TMP / f'{i}.txt'; lst.write_text(''.join(f"file '{TMP / f'{i}-{k}.mp4'}'\n" for k in range(1, 6)))
    run('-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', TMP / f'{i}-v.mp4')
    T = sum(D); tid, tss = r['track']
    run('-i', TMP / f'{i}-v.mp4', '-ss', tss, '-i', MK / f'{tid}.mp3', '-filter_complex',
        f'[1:a]atrim=0:{T},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st={T - 0.8}:d=0.8,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]',
        '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', T, '-movflags', '+faststart', OUT / f'{i}.mp4')
    run('-i', OUT / f'{i}.mp4', '-frames:v', '1', '-q:v', '2', OUT / f'{i}-capa.jpg')
    print(i, 'ok', flush=True)
