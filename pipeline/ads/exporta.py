"""Exporta para ads/aprovados todo AD aprovado na versão atual que ainda não tem pasta.
Uso: python3 exporta.py <db/ads (ArtifactData list com out_dir)> <pasta com media/ da Mesa p/ estáticos e reels antigos>
Modelo novo (reel + motions em pipeline/out/media): copia direto. Estático do lote 2: placements.static. Reel antigo: placements.reel."""
import json, shutil, sys, importlib.util
from pathlib import Path
R = Path(__file__).resolve().parent.parent; REPO = R.parent
spec = importlib.util.spec_from_file_location('pl', R / 'ads' / 'placements.py'); pl = importlib.util.module_from_spec(spec); spec.loader.exec_module(pl)
db, mesa = Path(sys.argv[1]), Path(sys.argv[2])
ads = json.loads((R / 'ads' / 'S02.json').read_text()); out = REPO / 'ads' / 'aprovados'; novos = []
for a in ads:
    f = db / f"S02_{a['id']}.json"
    if not f.exists(): continue
    r = json.loads(f.read_text())
    if r.get('status') != 'aprovado' or r.get('hash') != a.get('hash') and r.get('version') != a['version']: continue
    if r.get('version') != a['version']: continue
    v = a['version']; d = out / pl.SLUG[a['brand']] / v
    if d.exists(): continue
    d.mkdir(parents=True)
    m = R / 'out' / 'media'
    if a['fmt'] == 'reel' and a.get('arquivos'):
        shutil.copy(m / a['media'][0], d / f'{v}_reels-stories-9x16.mp4'); shutil.copy(m / a['cover'], d / f'{v}_capa-reels-stories-9x16.jpg')
        for x in a['arquivos']:
            n = 'video-feed-4x5.mp4' if 'feed45' in x['path'] else 'video-feed-instream-1x1.mp4'
            shutil.copy(R / 'out' / x['path'], d / f'{v}_{n}')
    elif a['fmt'] == 'reel': pl.reel(a, mesa, d)
    else: pl.static(a, mesa, d)
    pl.leiame(a, d, sorted(x.name for x in d.iterdir() if x.name != 'LEIA-ME.md')); novos.append(a)
    print('exportado', v, len(list(d.iterdir())))
base = 'https://github.com/gtorniero/beyondtheworkproject/tree/social/ads/aprovados'
by = {a['version']: a for a in ads}; rows = []
for d in sorted(out.glob('*/*')):
    a = by.get(d.name); t = a.get('title', '') if a else '(versão anterior)'; i = d.name.rsplit('-v', 1)[0]
    atual = 'atual' if a else 'anterior'
    rows.append(f"| {d.parent.name} | {i} | {d.name.split('-')[-1]} | {atual} | {t} | {base}/{d.parent.name}/{d.name} |")
(out / 'INDEX.md').write_text("# ADs aprovados · arquivos por posicionamento da Meta\n\nCada pasta tem os arquivos nomeados por posicionamento e um LEIA-ME.md com copy, CTA e URL final. \"anterior\" = versão aprovada que já foi substituída na Mesa. Nada foi enviado à conta de anúncios.\n\n| Marca | AD | Versão | Situação | Título | Pasta |\n|---|---|---|---|---|---|\n" + '\n'.join(rows) + '\n')
