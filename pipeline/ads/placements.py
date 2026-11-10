"""Adapta ADs aprovados para todos os posicionamentos da Meta e organiza em ads/aprovados/<marca>/<ID>-v<n>/.
Reels (9:16 com fundo chapado): 4:5 e 1:1 com o vídeo inteiro centralizado no mesmo fundo; 16:9 (in-stream) com painel de texto à esquerda.
Estáticos: já saem do kit em 4:5 (hero), 1:1, 9:16, 1,91:1 e motion 9:16, 4:5, 1:1; aqui só são renomeados por posicionamento.
Uso: python3 placements.py <pasta com media/ da Mesa> <saida ads/aprovados>"""
import json, shutil, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parent.parent; A = R / 'assets'; F = R / 'fonts'
import base64
def ff(fam, file, w): return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{base64.b64encode((F/file).read_bytes()).decode()}) format('woff2');font-weight:{w}}}"
SLUG = {'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna', 'Quiddo': 'quiddo'}
# fundo chapado dos reels e painel 16:9 (texto = o CTA que já está no vídeo aprovado)
REEL = {
 'ADC-RZ-01': dict(bg='#17092C', hd='Faça a retrospectiva do seu grupo.', url='retrozap.com.br', acc='#FFC23C', logo=A/'retrozap'/'logo-assinatura-grupo.svg', font=('Bricolage Grotesque','Bricolage-800.woff2','800')),
 'ADC-RZ-02': dict(bg='#17092C', hd='Faça a retrospectiva 2026 do seu grupo.', url='retrozap.com.br', acc='#FFC23C', logo=A/'retrozap'/'logo-assinatura-grupo.svg', font=('Bricolage Grotesque','Bricolage-800.woff2','800')),
 'ADC-RK-01': dict(bg='#090909', hd='Antes de comprar, faça o teste.', url='sportdna.com.br/racket', acc='#DDF247', logo=A/'sportdna'/'racketdna-logo-fundo-escuro.svg', font=('Archivo','Archivo-800.woff2','800')),
}
STATIC = {'feed45.png': 'feed-4x5_hero.png', 'sq.png': 'feed-coluna-1x1.png', 'story.png': 'stories-reels-9x16.png', 'land.png': 'busca-audience-1.91x1.png',
          'motion-feed45.mp4': 'video-feed-4x5.mp4', 'motion-sq.mp4': 'video-feed-instream-1x1.mp4', 'motion-story.mp4': 'video-stories-reels-9x16.mp4'}

def run(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *a], check=True)

def enc(): return ['-an', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', '-r', '30', '-movflags', '+faststart']

def panel(cfg, out):
    fam, file, w = cfg['font']
    svg = cfg['logo'].read_text()
    html = f'''<!doctype html><meta charset="utf-8"><style>{ff(fam,file,w)}{ff('DM Sans','DMSans-var.woff2','400 700')}
    *{{margin:0;box-sizing:border-box}} body{{width:1920px;height:1080px;background:{cfg['bg']};position:relative;color:#fff}}
    .l{{position:absolute;left:150px;top:150px}} .l svg{{height:76px;width:auto}}
    h1{{position:absolute;left:150px;top:330px;width:900px;font:{w} 104px/1.02 '{fam}';letter-spacing:-.03em}}
    .u{{position:absolute;left:150px;top:800px;display:inline-block;background:{cfg['acc']};color:{cfg['bg']};border-radius:999px;padding:22px 44px;font:700 46px 'DM Sans'}}</style>
    <div class="l">{svg}</div><h1>{cfg['hd']}</h1><div class="u">{cfg['url']}</div>'''
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        pg.set_content(html); pg.evaluate('document.fonts.ready'); pg.screenshot(path=str(out)); b.close()

def reel(ad, src, dst):
    cfg = REEL[ad['id']]; v = ad['version']; bg = cfg['bg'].replace('#', '0x')
    i = str(src / 'media' / ad['media'][0])
    shutil.copy(i, dst / f'{v}_reels-stories-9x16_original.mp4')
    run('-i', i, '-vf', 'scale=1080:1920', *enc(), str(dst / f'{v}_reels-stories-9x16_sem-trilha.mp4'))
    run('-i', i, '-vf', f'scale=-2:1350,pad=1080:1350:(ow-iw)/2:0:{bg}', *enc(), str(dst / f'{v}_video-feed-4x5.mp4'))
    run('-i', i, '-vf', f'scale=-2:1080,pad=1080:1080:(ow-iw)/2:0:{bg}', *enc(), str(dst / f'{v}_video-feed-coluna-1x1.mp4'))
    pp = dst / '_painel.png'; panel(cfg, pp)
    run('-loop', '1', '-i', str(pp), '-i', i, '-filter_complex', '[1:v]scale=-2:1000[v];[0:v][v]overlay=1920-w-150:40:shortest=1', *enc(), str(dst / f'{v}_video-instream-16x9.mp4'))
    pp.unlink()
    for name, fmt in (('reels-stories-9x16', None), ('feed-4x5', (1080, 1350)), ('feed-1x1', (1080, 1080))):
        o = dst / f'{v}_capa-{name}.jpg'
        vf = 'select=eq(n\\,0)' + (f',scale=-2:{fmt[1]},pad={fmt[0]}:{fmt[1]}:(ow-iw)/2:0:{bg}' if fmt else '')
        run('-ss', '1.0', '-i', i, '-frames:v', '1', '-vf', vf.replace('select=eq(n\\,0),', '').replace('select=eq(n\\,0)', 'null'), '-q:v', '3', str(o))

def static(ad, src, dst):
    v = ad['version']; d = src / 'media' / 'ads' / v
    for suf, name in STATIC.items(): shutil.copy(d / f'{v}-{suf}', dst / f'{v}_{name}')

def leiame(ad, dst, files):
    t = f"# {ad['id']} · {ad.get('title', '')}\n\nVersão aprovada: {ad['version']} · {ad['brand']}\n\n"
    for k, l in (('objetivo', 'Objetivo'), ('publico', 'Público'), ('cta', 'CTA'), ('url', 'URL final')):
        if ad.get(k): t += f"- **{l}:** {ad[k] if not isinstance(ad[k], list) else '; '.join(ad[k])}\n"
    t += f"\n## Copy\n\n{ad.get('copy', '')}\n" + (f"\nTítulo: {ad['titulo']}\n" if ad.get('titulo') else '')
    t += '\n## Arquivos por posicionamento (Meta)\n\n' + '\n'.join(f'- `{f}`' for f in files) + '\n'
    t += ('\nMapa: Feed do Facebook e Instagram, Explorar, Marketplace → 4:5 (ou 1:1). Stories e Reels → 9:16. Coluna da direita, '
          'Messenger e resultados de busca → 1:1. Audience Network e links → 1,91:1. In-stream (vídeo) → 16:9 ou 1:1.\n'
          'Vídeos sem áudio: a música, se houver, entra pela biblioteca da Meta.\n\nNada foi enviado à conta de anúncios.\n')
    (dst / 'LEIA-ME.md').write_text(t)

if __name__ == '__main__':
    src, out = Path(sys.argv[1]), Path(sys.argv[2]); ids = sys.argv[3:]
    ads = {a['id']: a for a in json.loads((R / 'ads' / 'S02.json').read_text())}
    for i in ids:
        ad = ads[i]; dst = out / SLUG[ad['brand']] / ad['version']; dst.mkdir(parents=True, exist_ok=True)
        (reel if ad['fmt'] == 'reel' else static)(ad, src, dst)
        leiame(ad, dst, sorted(f.name for f in dst.iterdir() if f.name != 'LEIA-ME.md'))
        print(i, len(list(dst.iterdir())))
