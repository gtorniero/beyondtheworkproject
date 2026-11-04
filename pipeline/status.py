"""Gera STATUS.json (o que está liberado para o DOT) a partir das decisões da Mesa.
Uso: python3 status.py <pasta reviews/*.json> <saida STATUS.json> [manifest.json]"""
import json, sys
from pathlib import Path
rev_dir = Path(sys.argv[1])
M = json.loads(Path(sys.argv[3]).read_text()) if len(sys.argv) > 3 else json.loads((Path(__file__).parent / 'out' / 'manifest.json').read_text())
pack = M['pack']
rev = {}
for f in rev_dir.glob('*.json'):
    d = json.loads(f.read_text()); d = d.get('data', d)
    k = f.stem
    if pack != 'S01':
        if not k.startswith(pack + '_'): continue
        k = k[len(pack) + 1:]
    rev[k] = d
out = []
for p in M['pieces']:
    r = rev.get(p['id'], {})
    ok = r.get('status') == 'aprovado' and r.get('hash') == p['hash']
    out.append({'peca': p['id'], 'marca': p['brand'], 'formato': p['fmt'], 'dia': p['dia'], 'hora': p.get('slot') or ('12h' if p['fmt'] == 'story' else '12h30'),
                'versao': p['version'], 'liberado': ok, 'status_mesa': r.get('status') or 'pendente'})
Path(sys.argv[2]).write_text(json.dumps({'pack': pack, 'liberadas': sum(o['liberado'] for o in out), 'total': len(out), 'pecas': out}, ensure_ascii=False, indent=1))
print(sum(o['liberado'] for o in out), '/', len(out), 'liberadas')
