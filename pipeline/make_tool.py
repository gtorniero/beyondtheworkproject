"""Monta a Mesa de Aprovação (tool/) e o pacote de entrega (entrega/ + zip) a partir de out/."""
import json, shutil, zipfile, markdown
import guia
from pathlib import Path
from PIL import Image
R = Path(__file__).parent; O = R / 'out'; T = R / 'tool'; E = R / 'entrega'
pieces = {}
for f in sorted(O.glob('manifest-*.json')):
    for p in json.loads(f.read_text())['pieces']: pieces[p['id']] = p
import common as C, importlib
for m in ('quiddo', 'retrozap', 'sportdna'): importlib.import_module(m)
order = [p['id'] for p in C.PIECES]
P = [pieces[i] for i in order if i in pieces]
# Canceladas pelo Gui (rodada 4): stories que dependiam de adesivo
CANCELADAS = {'Q-S1', 'Q-S2', 'Q-S3', 'Q-S5', 'R-S1', 'R-S2', 'R-S3', 'R-S5', 'D-S1', 'D-S2', 'D-S3', 'D-S4', 'D-S5'}
P = [p for p in P if p['id'] not in CANCELADAS]
missing = [i for i in order if i not in pieces]
SRC = {p['id']: p for p in C.PIECES}
for p in P:  # metadados vêm sempre do código (horário, título, notas, adesivo)
    for k in ('slot', 'title', 'notes', 'sticker', 'kind'):
        if k in SRC[p['id']]: p[k] = SRC[p['id']][k]
if missing: print('FALTAM', missing)
(T / 'media').mkdir(parents=True, exist_ok=True); (T / 'editaveis').mkdir(exist_ok=True)
def jpg(src, dst, w, crop=None, q=84):
    im = Image.open(src).convert('RGB')
    if crop: im = im.crop(crop)
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS); im.save(dst, quality=q, optimize=True, progressive=True)
for p in P:
    md = O / 'media'
    if p['fmt'] == 'reel':
        shutil.copy(md / p['media'][0], T / 'media' / p['media'][0])
        p['poster'] = f"{p['id']}-poster.jpg"; jpg(md / p['poster'], T / 'media' / p['poster'], 720)
        p['cover'] = f"{p['id']}-capa.jpg"; jpg(md / f"{p['id']}-capa.png", T / 'media' / p['cover'], 720)
        p['cover45'] = f"{p['id']}-capa45.jpg"; jpg(md / f"{p['id']}-capa.png", T / 'media' / p['cover45'], 600, crop=(0, 285, 1080, 1635))
    else:
        p['previews'] = []
        for f in p['media']:
            n = f.replace('.png', '.jpg'); jpg(md / f, T / 'media' / n, 720); p['previews'].append(n)
    shutil.copy(O / p['editable'], T / p['editable'])
MUDOU = {
 'Q-R1': 'Fim do vídeo e legenda com o CTA "Faça o seu. Teste grátis." no lugar de "grátis até 10 pessoas" (seu comentário).',
 'Q-R2': 'Entrou o CTA "Faça o seu. Teste grátis." no fim (regra nova do Quiddo, do seu comentário no Q-R1).',
 'Q-R3': 'Entrou o CTA "Faça o seu. Teste grátis." no fim (regra nova do Quiddo).',
 'Q-C1': 'Entrou o CTA "Faça o seu. Teste grátis." na última página (regra nova do Quiddo).',
 'Q-C2': 'Saiu "grátis até 10 pessoas"; entrou o CTA "Faça o seu. Teste grátis." (regra nova do Quiddo).',
 'Q-S5': 'Saiu "grátis até 10 pessoas"; entrou o CTA "Faça o seu. Teste grátis." (regra nova do Quiddo).',
 'Q-S3': 'Linha nova (você reprovou o intruso): pergunta direta valendo ponto, sem nada sobreposto. A resposta (20 bichos) sai no story de sexta.',
 'D-R1': 'Linha nova: simulação de uma IA genérica respondendo qual raquete comprar, "Parece simples. Não é." e o modelo calibrado com atletas e esportistas (feedback geral).',
 'D-S2': 'Saiu o desenho da raquete; entrou o logo oficial do RACKET DNA (seu comentário).',
 'D-S3': 'Linha nova: a IA genérica responde sobre prancha, "Parece simples. Não é." e enquete (feedback geral).',
 'D-S4': 'Linha nova: o que a IA responde e o que falta (feedback geral). CTA na arte no lugar do adesivo.',
}
STORIES_CTA = 'O Instagram não agenda adesivos e você não vai postar nada: a enquete/quiz/link virou CTA desenhado na arte ("responde no direct", "link na bio"). Assim o DOT agenda tudo.'
for p in P:
    if p['v'] > 1 and p['id'] in MUDOU: p['mudou'] = MUDOU[p['id']]
    if p['fmt'] == 'story' and 'Sem adesivo: o CTA' in p.get('sticker', ''): p['mudou'] = STORIES_CTA + (' ' + MUDOU[p['id']] if p['id'] in MUDOU and p['id'] != 'Q-S3' else '')
RODADA = max(p['v'] for p in P)
GUIA = guia.guia_md(P)
FINAL = {}
html = (R / 'tool_template.html').read_text().replace('/*MANIFEST*/', json.dumps({'pack': C.PACK, 'rodada': RODADA, 'pieces': P, 'guiaHtml': markdown.markdown(GUIA, extensions=['tables', 'fenced_code']), 'prompt': guia.PROMPT, 'final': '__FINAL__'}, ensure_ascii=False).replace('</', '<\\/'))
(T / 'index.html').write_text(html)
(O / 'manifest.json').write_text(json.dumps({'pack': C.PACK, 'pieces': P}, ensure_ascii=False, indent=1))
# ---- entrega
if E.exists(): shutil.rmtree(E)
slug = {'Quiddo': 'quiddo', 'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna'}
for b in slug.values():
    for d in ('reels', 'carrosseis', 'stories', 'editaveis'): (E / b / d).mkdir(parents=True, exist_ok=True)
leg = {}
for p in P:
    b = slug[p['brand']]; md = O / 'media'
    sub = {'reel': 'reels', 'carrossel': 'carrosseis', 'story': 'stories'}[p['fmt']]
    for f in p['media']: shutil.copy(md / f, E / b / sub / f)
    if p['fmt'] == 'reel': shutil.copy(md / f"{p['id']}-capa.png", E / b / sub / f"{p['id']}-capa.png")
    shutil.copy(O / p['editable'], E / b / 'editaveis' / Path(p['editable']).name)
    if p['fmt'] == 'reel' and (O / 'editaveis' / f"{p['id']}-capa.html").exists():
        shutil.copy(O / 'editaveis' / f"{p['id']}-capa.html", E / b / 'editaveis' / f"{p['id']}-capa.html")
    t = f"{p['version']} · {p['dia']}{' · ' + p['slot'] if p.get('slot') else ''} · {p['fmt'].upper()} · {p['title']}\n"
    t += f"Arquivos: {', '.join(p['media'])}{'  + capa ' + p['id'] + '-capa.png' if p['fmt']=='reel' else ''}\n"
    if p.get('sticker'): t += f"Adesivo: {p['sticker']}\n"
    if p['fmt'] != 'story': t += f"\nLEGENDA\n{p['caption']}\n"
    if p.get('notes'): t += f"\nNotas: {p['notes']}\n"
    leg.setdefault(b, []).append(t)
for b, ts in leg.items():
    head = f"{b.upper()} · PACK SEMANAL 01 (09–15/11/2026) · rodada {RODADA}\nReels: 1080×1920, 30 fps, H.264, áudio mudo (escolha o áudio no Instagram). Capa: 1080×1920 com a arte 4:5 no centro.\nFeed: 1080×1350. Stories: 1080×1920 com o espaço do adesivo já reservado.\nEditáveis: HTML com fontes e SVGs embutidos (abre no navegador; reels tocam sozinhos, clique para recomeçar).\n\n"
    (E / b / 'LEGENDAS.txt').write_text(head + ('\n' + '-' * 60 + '\n\n').join(ts))
(E / 'GUIA-PUBLICACAO-DOT.md').write_text(GUIA)
(E / 'agenda.csv').write_text(guia.agenda_csv(P))
for b in slug.values():
    shutil.copy(E / 'GUIA-PUBLICACAO-DOT.md', E / b / 'GUIA-PUBLICACAO-DOT.md')
    (E / b / 'agenda.csv').write_text(guia.agenda_csv([p for p in P if slug[p['brand']] == b]))
    for f in sorted((E / b).rglob('*')):
        if f.is_file():
            dst = T / 'final' / b / f.relative_to(E / b); dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy(f, dst)
            FINAL.setdefault(b, []).append(str(f.relative_to(E / b)))
html = html.replace('"__FINAL__"', json.dumps(FINAL, ensure_ascii=False))
(T / 'index.html').write_text(html)
z = R / f'pack-semanal-01-v{RODADA}.zip'
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in sorted(E.rglob('*')):
        if f.is_file(): zf.write(f, 'pack-semanal-01/' + str(f.relative_to(E)))
tot = sum(f.stat().st_size for f in T.rglob('*') if f.is_file())
print('tool files', sum(1 for f in T.rglob('*') if f.is_file()), 'MB', round(tot / 1e6, 1), '| zip MB', round(z.stat().st_size / 1e6, 1))
