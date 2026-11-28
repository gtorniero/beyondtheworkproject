"""Mesa S05: troca o manifesto da Mesa no ar (index.html lido do artifact) pelo pack S05, mantendo os ADs e o template.
Gera mesa5/media (mídia leve) e mesa5/files.json (uploads + remoções). Uso: python3 mesa5.py <index.html no ar> <lista de arquivos no ar>"""
import json, re, subprocess, sys, importlib
from pathlib import Path
from PIL import Image
import common as C, guia
for m in ('quiddo', 'retrozap', 'sportdna'): importlib.import_module(m)
R = Path(__file__).parent; O = C.OUT; W = R / 'mesa5'; MD = W / 'media'; MD.mkdir(parents=True, exist_ok=True)
live = Path(sys.argv[1]).read_text(); RX = r'(<script id="manifest" type="application/json">)(.*?)(</script>)'
m = re.search(RX, live, re.S); d = json.loads(m.group(2))
man = {}
for f in O.glob('manifest-*.json'):
    for p in json.loads(f.read_text())['pieces']: man[p['id']] = p
order = [p['id'] for p in C.PIECES]; SRC = {p['id']: p for p in C.PIECES}
def jpg(src, dst, w, crop=None, q=82):
    im = Image.open(src).convert('RGB')
    if crop: im = im.crop(crop)
    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(dst, quality=q, optimize=True, progressive=True)
UP = []; P = []
GH = f'https://github.com/gtorniero/beyondtheworkproject/blob/social/packs/{C.PACK}'
SL = {'Quiddo': 'quiddo', 'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna'}
for pid in order:
    p = dict(man[pid]); s = SRC[pid]; px = f'{C.PACK}-{pid}'
    for k in ('slot', 'title', 'notes', 'sticker', 'kind'): p[k] = s.get(k, p.get(k))
    p['editable'] = f"{GH}/{SL[p['brand']]}/editaveis/{pid}.html"
    if p['fmt'] == 'reel':
        dst = MD / f'{px}.mp4'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(O / 'media' / p['media'][0]), '-vf', 'scale=720:-2', '-c:v', 'libx264', '-crf', '24', '-preset', 'medium',
                        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(dst)], check=True)
        jpg(O / 'media' / f'{pid}-capa.png', MD / f'{px}-capa.jpg', 720); jpg(O / 'media' / f'{pid}-capa.png', MD / f'{px}-capa45.jpg', 600, crop=(0, 285, 1080, 1635))
        p['media'] = [f'{px}.mp4']; p['poster'] = f'{px}-capa.jpg'; p['cover'] = f'{px}-capa.jpg'; p['cover45'] = f'{px}-capa45.jpg'
        UP += [f'media/{px}.mp4', f'media/{px}-capa.jpg', f'media/{px}-capa45.jpg']
    else:
        prev = []
        for f in p['media']:
            n = f'{C.PACK}-' + f.replace('.png', '.jpg'); jpg(O / 'media' / f, MD / n, 720); prev.append(n); UP.append(f'media/{n}')
        p['previews'] = prev
    p['mudou'] = 'Peça nova do Pack S05 (08–14/12).'
    P.append(p)
# candidata: D-FX1 v2 (reprovada a v1 na rodada 18; a v2 ficou sem decisão quando a Mesa do S03 fechou)
old = {q['id']: q for q in d['pieces']}
fx = dict(old['D-FX1']); fx.update(day=2, dia=C.DIAS[2], slot='12h30', version=f'{C.PACK}-D-FX1-v2', v=2,
         title='CANDIDATA · FIXAR · RACKET DNA: o que tem por trás da sua raquete ideal',
         notes='Candidata do S03 (mesma arte da v2, sem decisão na Mesa). v2 feita na rodada 18: só RACKET, 100% nas cores do RACKET. Data nova: qua 09/12, 12h30, como post extra para FIXAR no perfil.',
         mudou='Vem do S03 sem decisão: mesma arte, data nova (09/12).')
P.append(fx)
d['arquivo'] = d.get('arquivo', []) + [dict(id=q['id'], title=q['title'], dia=q.get('dia'), version=q['version']) for q in d['pieces'] if q['id'] != 'D-FX1']
d.update(pack=C.PACK, rodada=1, titulo=f'PACK SEMANAL {C.NUM} · {C.SEMANA}', days={str(k): f'Dia {k} · {v}' for k, v in C.DIAS.items()}, pieces=P, grade={}, final={},
         guiaHtml=__import__('markdown').markdown(guia.guia_md(P), extensions=['tables', 'fenced_code']), prompt=guia.PROMPT)
d['adsLote'] = ['28/11 · Pack S05 (08–14/12) na Mesa: 42 peças novas (por marca 3 reels, 4 carrosséis e 7 sequências de story) + D-FX1 v2 como candidata. Sem preço, cada peça da SPORT DNA numa cor só, reels com música de banco e saída suave.'] + d.get('adsLote', [])
js = json.dumps(d, ensure_ascii=False).replace('</', '<\\/'); html = live[:m.start(2)] + js + live[m.end(2):]
(W / 'index.html').write_text(html)
# remoções: tudo que o novo manifesto não cita
live_files = [l.split('"')[1] for l in Path(sys.argv[2]).read_text().splitlines() if l.startswith('- "')]
DEL = [f for f in live_files if f != 'index.html' and f.split('/', 1)[-1] not in js]
F = {x: str(W / x) for x in UP}; F.update({x: None for x in DEL})
(W / 'files.json').write_text(json.dumps(F, indent=0)); print('pieces', len(P), 'up', len(UP), 'del', len(DEL), 'keep', len(live_files) - len(DEL) - 1)
