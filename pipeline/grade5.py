"""Folha de contato da grade (S05): 9 últimas peças de feed antes do pack (S03 fim + S04, sem canceladas) + as 7 novas, ordem do Instagram."""
import csv, json, sys
from pathlib import Path
from PIL import Image, ImageDraw
import common as C
PK = C.PACKS; SL = {'Quiddo': 'quiddo', 'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna'}
CANC = {'Q-R11', 'R-R15', 'R-R16', 'R-R18'}
def thumb(f, reel, w=260):
    im = Image.open(f).convert('RGB')
    if reel: im = im.crop((0, 285, 1080, 1635))
    return im.resize((w, int(w * 1.25)))
def antigos(marca):
    out = []
    for pk in ('S03', 'S04'):
        for r in csv.DictReader(open(PK / pk / 'agenda.csv')):
            if r['marca'] != marca or r['formato'] == 'story' or r['peca'] in CANC or 'BLOQUEADO' in r.get('observacao', ''): continue
            d = r['data'][:10]; key = (d[6:10], d[3:5], d[:2], r['hora'])
            sub = 'reels' if r['formato'] == 'reel' else 'carrosseis'
            f = PK / pk / SL[marca] / sub / (f"{r['peca']}-capa.png" if r['formato'] == 'reel' else f"{r['peca']}-1.png")
            if f.exists(): out.append((key, r['peca'], f, r['formato'] == 'reel', False))
    return sorted(out)[-9:]
def novos(marca):
    man = {}
    for mf in C.OUT.glob('manifest-*.json'):
        for p in json.loads(mf.read_text())['pieces']: man[p['id']] = p
    out = []
    for p in man.values():
        if p['brand'] != marca or p['fmt'] == 'story': continue
        f = C.OUT / 'media' / (f"{p['id']}-capa.png" if p['fmt'] == 'reel' else p['media'][0])
        out.append((('2026', '12', f"{7 + p['day']:02d}", p['slot']), p['id'], f, p['fmt'] == 'reel', True))
    return sorted(out)
w, g = 260, 6; cols = []
for m in SL:
    items = list(reversed(antigos(m) + novos(m)))
    rows = (len(items) + 2) // 3
    sh = Image.new('RGB', (3 * w + 2 * g, 40 + rows * (int(w * 1.25) + g)), '#fff'); d = ImageDraw.Draw(sh)
    d.text((8, 12), f'{m} · verde = S05', fill='#000')
    for i, (k, pid, f, reel, new) in enumerate(items):
        x, y = (i % 3) * (w + g), 40 + (i // 3) * (int(w * 1.25) + g)
        sh.paste(thumb(f, reel, w), (x, y)); d.rectangle((x, y, x + 62, y + 18), fill='#13A07A' if new else '#777'); d.text((x + 3, y + 3), pid, fill='#fff')
    cols.append(sh)
out = Image.new('RGB', (sum(c.width for c in cols) + 30 * 2, max(c.height for c in cols)), '#ccc'); x = 0
for c in cols: out.paste(c, (x, 0)); x += c.width + 30
out.save(sys.argv[1] if len(sys.argv) > 1 else C.OUT / 'grade.jpg', quality=82); print('ok')
