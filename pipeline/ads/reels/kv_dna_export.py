"""Exporta KVs SPORT DNA aprovados (kv_dna.py hero/adapt/motion) para ads/aprovados/sportdna/<versão>/ com nomes por posicionamento
e LEIA-ME.md, e refaz ads/aprovados/INDEX.md. Uso: python3 kv_dna_export.py <pasta com <versão>/ renderizada> <versões...>"""
import importlib.util, json, shutil, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent.parent; REPO = R.parent
spec = importlib.util.spec_from_file_location('pl', R / 'ads' / 'placements.py'); pl = importlib.util.module_from_spec(spec); spec.loader.exec_module(pl)
NOMES = dict(pl.STATIC, **{'16x9.png': 'instream-16x9.png'})
src, vers = Path(sys.argv[1]), sys.argv[2:]
ads = json.loads((R / 'ads' / 'S02.json').read_text()); by = {a['version']: a for a in ads}
out = REPO / 'ads' / 'aprovados'
for v in vers:
    a = by[v]; d = out / 'sportdna' / v; d.mkdir(parents=True, exist_ok=True)
    for suf, nome in NOMES.items(): shutil.copy(src / v / f'{v}-{suf}', d / f'{v}_{nome}')
    pl.leiame(a, d, sorted(x.name for x in d.iterdir() if x.name != 'LEIA-ME.md'))
    print('exportado', v, len(list(d.iterdir())))
base = 'https://github.com/gtorniero/beyondtheworkproject/tree/social/ads/aprovados'; rows = []
for d in sorted(out.glob('*/*')):
    if not d.is_dir(): continue
    a = by.get(d.name); t = a.get('title', '') if a else '(versão anterior)'; i = d.name.rsplit('-v', 1)[0]
    rows.append(f"| {d.parent.name} | {i} | {d.name.split('-')[-1]} | {'atual' if a else 'anterior'} | {t} | {base}/{d.parent.name}/{d.name} |")
(out / 'INDEX.md').write_text("# ADs aprovados · arquivos por posicionamento da Meta\n\nCada pasta tem os arquivos nomeados por posicionamento e um LEIA-ME.md com copy, CTA e URL final. \"anterior\" = versão aprovada que já foi substituída na Mesa. Nada foi enviado à conta de anúncios.\n\n| Marca | AD | Versão | Situação | Título | Pasta |\n|---|---|---|---|---|---|\n" + '\n'.join(rows) + '\n')
