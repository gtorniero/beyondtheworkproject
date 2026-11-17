"""Fecha o batch: música no motion 9:16, mídia da Mesa, entradas no manifesto e pastas no GitHub (só formato principal + LEIA-ME)."""
import json, re, hashlib, subprocess, shutil
from pathlib import Path
from PIL import Image
from nbmeta import ADS, DIR
N = Path(__file__).resolve().parent; W = N.parent; M = W / 'mesa'; S = W.parent / 'social'; MK = W.parent / 'mk'
OUT = N / 'out'
def run(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *map(str, a)], check=True)
def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)]))
def addmus(src, track, ss, out):
    T = dur(src)
    run('-i', src, '-ss', ss, '-i', track, '-filter_complex', f'[1:a]atrim=0:{T},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st={T-0.8}:d=0.8,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a]',
        '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', T, '-movflags', '+faststart', out)
H5 = lambda p: hashlib.md5(Path(p).read_bytes()).hexdigest()[:10]
s = (M / 'index.html').read_text()
m = re.search(r'(<script id="manifest" type="application/json">)(.*?)(</script>)', s, re.S); d = json.loads(m.group(2))
UP = []
BR = {'SPORT DNA': 'sportdna', 'Retrozap': 'retrozap'}
RAW = 'https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/ads/aprovados'
for a in reversed(ADS):
    v = a['id'] + '-v1'; o = OUT / v
    mot = o / f'{v}-motion-story.mp4'; assert mot.exists(), mot
    dst = S / 'ads' / 'aprovados' / BR[a['brand']] / v; dst.mkdir(parents=True, exist_ok=True)
    tid, ss = a['track']
    addmus(mot, MK / f'{tid}.mp3', ss, dst / f'{v}_reels-stories-9x16.mp4')
    shutil.copy(o / f'{v}-sq.png', dst / f'{v}_feed-1x1.png')
    # LEIA-ME
    lm = (f"# {a['id']} · {a['title']}\n\nVersão: {v} · {a['brand']} · aguardando aprovação na Mesa (formato principal)\n\n"
          f"- **Objetivo:** {a['objetivo']}\n- **Público:** {a['publico']}\n- **CTA:** {a['cta']}\n- **URL final:** {a['url']}\n"
          + (f"- **Atenção:** {a['notes']}\n" if a['notes'] else '') +
          f"\n## Copy\n\n{a['copy']}\n\nTítulo: {a['titulo']}\n\n## Arquivos\n\n- `{v}_reels-stories-9x16.mp4`: motion 9:16, 12 s, com música de banco (Mixkit).\n- `{v}_feed-1x1.png`: estático 1:1.\n\n"
          "Depois da aprovação entram aqui os outros posicionamentos: estáticos 4:5, 9:16, 1,91:1 e 16:9; motions 4:5 e 1:1; versões sem áudio.\n\n"
          "Sem voz de IA: não precisa do rótulo de IA da Meta.\n\nNada foi enviado à conta de anúncios.\n")
    (dst / 'LEIA-ME.md').write_text(lm)
    # Mesa
    run('-i', dst / f'{v}_reels-stories-9x16.mp4', '-vf', 'scale=720:-2', '-c:v', 'libx264', '-crf', '24', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', M / 'media' / f'{v}.mp4'); UP.append(f'media/{v}.mp4')
    Image.open(o / f'{v}-story.png').convert('RGB').resize((720, 1280)).save(M / 'media' / f'{v}-capa.jpg', quality=86); UP.append(f'media/{v}-capa.jpg')
    Image.open(o / f'{v}-sq.png').convert('RGB').save(M / 'media' / f'{v}-1x1.jpg', quality=88); UP.append(f'media/{v}-1x1.jpg')
    e = dict(id=a['id'], brand=a['brand'], fmt='kv', lote='performance-1711', title=a['title'], version=v, v=1, hash=H5(dst / f'{v}_reels-stories-9x16.mp4'),
             media=[f'{v}.mp4'], cover=f'{v}-capa.jpg', static=f'{v}-1x1.jpg', duration=12.0,
             formato='Motion 9:16 · 12 s · música de banco + estático 1:1 (formatos principais). Resto das dimensões depois da aprovação.',
             objetivo=a['objetivo'], publico=a['publico'], hipotese=a['hipotese'], copy=a['copy'], titulo=a['titulo'], cta=a['cta'], url=a['url'],
             direitos=a['direitos'], notes=(a['notes'] + ' ' if a['notes'] else '') + DIR, producao='pronto para revisão',
             mudou='Peça nova: batch performance de 17/11 (brief do Growth + seu pedido de ir no estilo do RK-05).',
             arquivos=[dict(label='LEIA-ME', path=f"{RAW}/{BR[a['brand']]}/{v}/LEIA-ME.md")])
    d['ads'] = [x for x in d['ads'] if x['id'] != a['id']]; d['ads'].insert(0, e)
nota = ('17/11 · Batch performance, no estilo do RK-05 que você curtiu (título direto, número grande, tela real no celular, botão). '
        'RACKET: RK-11 (qual raquete é a certa) e RK-12 (Black Friday, até 27/11). SURF: SF-11 (qual prancha) e SF-12 (Black Friday, até 27/11). '
        'Retrozap, literal: RZ-16 (3 passos), RZ-17 (o que vem nela) e RZ-18 (casal, R$ 13,99). Cada card tem o motion 9:16 com música e o estático 1:1: '
        'aprove os dois; o resto das dimensões sai depois.')
d['adsLote'] = [nota] + [x for x in d['adsLote'] if not x.startswith('17/11 · Batch performance')]
d['rodada'] = 13
js = json.dumps(d, ensure_ascii=False).replace('</', '<\\/')
s = s[:m.start(2)] + js + s[m.end(2):]
(M / 'index.html').write_text(s)
print('UP', len(UP)); (N / 'up.json').write_text(json.dumps(UP))
