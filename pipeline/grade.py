"""Folha de contato da grade do perfil: feed do pack anterior + feed do pack novo, por marca,
na ordem do Instagram (mais recente no canto de cima à esquerda). Uso: python3 grade.py [saida.jpg]"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw
import common as C

R = Path(__file__).parent
PREVD = R.parent / 'packs' / C.PREV
SLUG = {'Quiddo': 'quiddo', 'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna'}

def thumb(path, reel, w=300):
    im = Image.open(path).convert('RGB')
    if reel: im = im.crop((0, 285, 1080, 1635))
    return im.resize((w, int(w * 1.25)))

def feed():
    out = {b: [] for b in SLUG}
    now = {}
    for f in sorted((C.OUT).glob('manifest-*.json')):
        for p in json.loads(f.read_text())['pieces']: now[p['id']] = p
    if (PREVD / 'manifest.json').exists():
        for p in json.loads((PREVD / 'manifest.json').read_text())['pieces']:
            if p['fmt'] == 'story' or p['id'] in now: continue
            sub = 'reels' if p['fmt'] == 'reel' else 'carrosseis'
            f = PREVD / SLUG[p['brand']] / sub / (f"{p['id']}-capa.png" if p['fmt'] == 'reel' else p['media'][0])
            out[p['brand']].append((0, p['day'], p['id'], f, p['fmt'] == 'reel'))
    for p in now.values():
        if p['fmt'] == 'story': continue
        f = C.OUT / 'media' / (f"{p['id']}-capa.png" if p['fmt'] == 'reel' else p['media'][0])
        out[p['brand']].append((1, p['day'], p['id'], f, p['fmt'] == 'reel'))
    return out

def main(dst):
    w, gap = 300, 6
    cols = []
    for b, items in feed().items():
        items = sorted(items, reverse=True)[:12]
        rows = (len(items) + 2) // 3
        sheet = Image.new('RGB', (3 * w + 2 * gap, 50 + rows * (int(w * 1.25) + gap)), '#fff')
        d = ImageDraw.Draw(sheet); d.text((8, 16), f'{b} · grade (novo pack: marcador verde)', fill='#000')
        for i, (new, day, pid, f, reel) in enumerate(items):
            x, y = (i % 3) * (w + gap), 50 + (i // 3) * (int(w * 1.25) + gap)
            sheet.paste(thumb(f, reel, w), (x, y))
            d.rectangle((x, y, x + 70, y + 22), fill='#13A07A' if new else '#888'); d.text((x + 4, y + 5), pid, fill='#fff')
        cols.append(sheet)
    H = max(c.height for c in cols)
    out = Image.new('RGB', (sum(c.width for c in cols) + 40 * (len(cols) - 1), H), '#ddd')
    x = 0
    for c in cols: out.paste(c, (x, 0)); x += c.width + 40
    out.save(dst, quality=82); print(dst)

if __name__ == '__main__':
    import importlib
    main(sys.argv[1] if len(sys.argv) > 1 else str(C.OUT / 'grade.jpg'))
