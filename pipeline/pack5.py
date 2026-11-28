"""Monta packs/S05 (mídia, editáveis, LEGENDAS, agenda, guia, manifest, STATUS todo false) a partir de out/."""
import json, re, shutil, importlib
from pathlib import Path
import common as C, guia
for m in ('quiddo', 'retrozap', 'sportdna'): importlib.import_module(m)
O = C.OUT; PK = C.PACKS / C.PACK
if PK.exists(): shutil.rmtree(PK)
SL = {'Quiddo': 'quiddo', 'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna'}; SUB = {'reel': 'reels', 'carrossel': 'carrosseis', 'story': 'stories'}
man = {}
for f in O.glob('manifest-*.json'):
    for p in json.loads(f.read_text())['pieces']: man[p['id']] = p
SRC = {p['id']: p for p in C.PIECES}; P = []
for pid in [p['id'] for p in C.PIECES]:
    p = dict(man[pid])
    for k in ('slot', 'title', 'notes', 'sticker', 'kind', 'music', 'frames'): p[k] = SRC[pid].get(k, p.get(k))
    P.append(p)
# candidata do S03
live = open('/home/claude/mesa/index.html').read()
old = {q['id']: q for q in json.loads(re.search(r'<script id="manifest" type="application/json">(.*?)</script>', live, re.S).group(1))['pieces']}
fx_files = [f'D-FX1-{i}.png' for i in range(1, 9)]
P.append({'id': 'D-FX1', 'brand': 'SPORT DNA', 'fmt': 'carrossel', 'day': 2, 'dia': C.DIAS[2], 'slot': '12h30',
          'title': 'CANDIDATA · FIXAR · RACKET DNA: o que tem por trás da sua raquete ideal', 'kind': 'carrossel', 'caption': old['D-FX1']['caption'],
          'notes': 'Candidata do S03 (mesma arte da v2, sem decisão na Mesa). FIXAR no perfil. Data nova: qua 09/12, 12h30, post extra.',
          'version': f'{C.PACK}-D-FX1-v2', 'v': 2, 'hash': old['D-FX1']['hash'], 'media': fx_files, 'editable': '', 'duration': None, 'sticker': ''})
leg = {}
for p in P:
    b = SL[p['brand']]; d = PK / b / SUB[p['fmt']]; d.mkdir(parents=True, exist_ok=True)
    src = (C.PACKS / 'S03' / 'sportdna' / 'carrosseis') if p['id'] == 'D-FX1' else (O / 'media')
    for f in p['media']: shutil.copy(src / f, d / f)
    if p['fmt'] == 'reel': shutil.copy(O / 'media' / f"{p['id']}-capa.png", d / f"{p['id']}-capa.png")
    if p['id'] != 'D-FX1':
        e = PK / b / 'editaveis'; e.mkdir(exist_ok=True); shutil.copy(O / 'editaveis' / f"{p['id']}.html", e)
        if p['fmt'] == 'reel': shutil.copy(O / 'editaveis' / f"{p['id']}-capa.html", e)
    arqs = p['media'] + ([f"{p['id']}-capa.png"] if p['fmt'] == 'reel' else [])
    if p['fmt'] == 'story':
        for peca, ver, media, q, ant in guia.quadros(p):
            leg.setdefault(b, []).append(f"{ver} · {p['dia']} · 12h · STORY (quadro {q} de 3) · {p['title']}\nArquivos: {', '.join(media)}\n\nNotas: {p['notes']}\n")
        continue
    t = f"{p['version']} · {p['dia']} · {p['slot']} · {p['fmt'].upper()} · {p['title']}\nArquivos: {', '.join(arqs)}\n"
    if p['fmt'] == 'reel': t += f"Áudio: {guia.audio(p)}\n"
    t += f"\nLEGENDA\n{p['caption']}\n\nNotas: {p['notes']}\n"
    leg.setdefault(b, []).append(t)
for b, ts in leg.items():
    head = (f"{b.upper()} · PACK SEMANAL {C.NUM} ({C.SEMANA_LONGA})\nReels: 1080×1920, 30 fps, H.264, com música de banco (Mixkit) sem narração. Capa: 1080×1920 com a arte 4:5 no centro.\n"
            "Feed: 1080×1350. Stories: sequências de 3 quadros 1080×1920, sem adesivo (o CTA está na arte).\n\n" + '-' * 60 + '\n\n')
    (PK / b / 'LEGENDAS.txt').write_text(head + ('\n' + '-' * 60 + '\n\n').join(ts))
(PK / 'agenda.csv').write_text(guia.agenda_csv(P)); (PK / 'GUIA-PUBLICACAO.md').write_text(guia.guia_md(P))
(PK / 'manifest.json').write_text(json.dumps({'pack': C.PACK, 'pieces': P}, ensure_ascii=False, indent=1))
print(len(P), 'peças')
