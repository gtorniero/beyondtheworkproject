"""Junta na Mesa (sobre a versão PUBLICADA, lida do artifact) as sequências de stories, o pack Quiddo educação e o card sem preço do R-C8.
Gera media novos em work/mesa/media e grava work/mesa/index.html; lista o que publicar e o que apagar."""
import json, re, hashlib, glob
from pathlib import Path
from PIL import Image
W = Path(__file__).resolve().parent; S = W.parent / 'social'; M = W / 'mesa'; MED = M / 'media'
LIVE = W.parent / 'artifact-files' / '9327c3d4-8cce-48f2-a7b4-3f3d7f0ad80c' / 'index.html'
s = LIVE.read_text()
m = re.search(r'(<script id="manifest" type="application/json">)(.*?)(</script>)', s, re.S); d = json.loads(m.group(2))
H5 = lambda p: hashlib.md5(Path(p).read_bytes()).hexdigest()[:10]
UP = []
# CSS do carrossel que sumiu na versão publicada + proporção 9:16 para sequências
CSSADD = '.frame.fcar{aspect-ratio:4/5!important;max-height:none!important;width:100%}.frame.f11.fcar{aspect-ratio:1/1!important}.fcar .strip img{width:100%;height:100%;object-fit:cover;max-height:none!important;display:block}.adcard .fcar{max-width:380px}.frame.f916.fcar{aspect-ratio:9/16!important;max-width:380px}'
if '.frame.fcar{' not in s: s = s.replace('[hidden]:not([hidden=until-found i]){display:none!important}', '[hidden]:not([hidden=until-found i]){display:none!important}' + CSSADD, 1)
elif '.f916.fcar' not in s: s = s.replace('.adcard .fcar{max-width:380px}', '.adcard .fcar{max-width:380px}.frame.f916.fcar{aspect-ratio:9/16!important;max-width:380px}', 1)
s = s.replace("<div class=\"frame ${p.ratio==='1x1'?'f11':'f45'} fcar\">", "<div class=\"frame ${p.ratio==='1x1'?'f11':p.ratio==='9x16'?'f916':'f45'} fcar\">")
assert "p.ratio==='9x16'" in s

DAY = {'17/11': -5, '18/11': -4, '19/11': -3, '20/11': -2, '21/11': -0.5, '22/11': -1, **{f'{n}/11': n - 22 for n in range(23, 30)}, '30/11': 8,
       **{f'{n:02d}/12': 8 + n for n in range(1, 7)}, '07/12': 15}
d['days'].update({'-4': 'S02 · qua 18/11', '-2': 'S02 · sex 20/11', '-1': 'S02 · dom 22/11', '-40': 'Quiddo educação · a programar'})
P = {p['id']: p for p in d['pieces']}
meta = json.loads((W / 'seq' / 'meta.json').read_text())
def base_png(sid):
    for g in [f'{S}/packs/*/*/stories/{sid}.png', f'{S}/packs/extras-stories/{sid}.png', f'{S}/packs/*/*/stories/{sid}-v*.png']:
        f = sorted(glob.glob(g))
        if f: return Path(f[-1])
    raise SystemExit('sem quadro 1: ' + sid)
groups = {}
for f in meta: groups.setdefault(f['base'], []).append(f)
BR = {'Quiddo': 'quiddo', 'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna'}
novos = []
for base, fr in groups.items():
    fr = sorted(fr, key=lambda x: x['n']); f0 = fr[0]
    imgs = ([W / 'seq' / f'{base}.png'] if f0['n'] == 1 else [base_png(base)]) + [W / 'seq' / f"{x['id']}.png" for x in fr if x['n'] > 1]
    T = Image.new('RGB', (3 * 540 + 2 * 24, 960), (255, 255, 255))
    for k, im in enumerate(imgs):
        I = Image.open(im).convert('RGB').resize((540, 960)); T.paste(I, (k * 564, 0))
    nm = f'SEQ-{base}.jpg'; T.save(MED / nm, quality=84); names = [nm]; UP.append('media/' + nm)
    q = f0['brand'] == 'Quiddo'
    titulo = (fr[0]['title'] if q else (P[base]['title'] if base in P else base)) + ' · sequência de 3'
    mud = ('Pedido do Gui (17/11): o story vira historinha de 3 quadros. Quadro 1 refeito com a matéria (' + fr[0]['title'].split(':')[0].replace('Quiz de ', '') + ') e o aviso "a resposta está no próximo story"; quadro 2 resposta e explicação; quadro 3 CTA de ' + ('sala de aula' if 'aula' in fr[2]['title'] else 'treinamento') + ' com tela real do Quiddo (partida gravada).'
           if q else 'Pedido do Gui (17/11): o story vira historinha de 3 quadros. Quadro 1 é o já aprovado; entram o 2 (o gancho vira produto) e o 3 (CTA claro, sem preço).')
    e = dict(P.get(base, {}))
    e.update(id=base, brand=f0['brand'], fmt='adaptacao', imgs=[dict(src=names[0], label='Quadro 1 → 2 → 3 (postar em sequência)', w='100%')], day=DAY[f0['data']], dia=f"{f0['sem']} {f0['data']}", slot='12h', title=titulo, kind='story',
             caption='(story, sem legenda; postar os 3 quadros em sequência, no mesmo horário)', notes=' / '.join(x['notes'] for x in fr),
             version=f'SEQ-{base}-v1', v=1, hash=H5(imgs[-1]), media=names, previews=names, sticker='', duration=None, mudou=mud)
    for k in ('poster', 'cover', 'cover45', 'editable'): e.pop(k, None)
    if base in P: d['pieces'] = [e if p['id'] == base else p for p in d['pieces']]
    else: d['pieces'].append(e)
    novos.append(base)

# Quiddo educação: 4 Reels + 4 carrosséis
Q = W / 'qedu'
CAP = {
 'QE-R1': 'A revisão de Geografia virou jogo. 🌎\nA professora escreve as perguntas, abre a sala no telão e cada aluno responde pelo celular. A resposta aparece na hora e o pódio fecha a aula.\n\nManda pra um professor que ia gostar 👇\nQuiddo: grátis até 10 pessoas, sem baixar app. Link na bio.\n#quiddo #professor #geografia #saladeaula #educacao #quiz',
 'QE-R2': 'História do Brasil, valendo pódio. 📜\nLei Áurea, Independência, República: a revisão vira quiz, a turma responde pelo celular e a resposta aparece no telão.\n\nMarca o professor de História 👇\nQuiddo: grátis até 10 pessoas, sem baixar app. Link na bio.\n#quiddo #professor #historia #saladeaula #educacao #quiz',
 'QE-R3': 'Proparoxítona? A sala respondeu em segundos. ✏️\nAcentuação, concordância, plural: a revisão de Português vira jogo, com ranking a cada rodada e pódio no fim.\n\nManda pra quem dá aula de Português 👇\nQuiddo: grátis até 10 pessoas, sem baixar app. Link na bio.\n#quiddo #professor #portugues #saladeaula #educacao #quiz',
 'QE-R4': 'O treinamento que a equipe não esquece. 💼\nEscreva as perguntas do treinamento, abra a sala no telão e a equipe responde pelo celular. Ranking a cada rodada e pódio no fim.\n\nManda pra quem cuida do treinamento na sua empresa 👇\nQuiddo. Link na bio.\n#quiddo #treinamento #rh #onboarding #endomarketing #quiz',
 'QE-C1': '5 perguntas de Geografia pra abrir a aula. 🌎\nArraste, responda de cabeça e confira o gabarito no fim.\n\nNo Quiddo, a turma responde pelo celular e a resposta aparece no telão. Grátis até 10 pessoas. Link na bio.\n#quiddo #geografia #professor #saladeaula #quiz',
 'QE-C2': '5 perguntas de Português que a turma erra. ✏️\nArraste, responda de cabeça e confira o gabarito no fim.\n\nNo Quiddo, a revisão vira jogo: ranking a cada rodada e pódio no fim. Grátis até 10 pessoas. Link na bio.\n#quiddo #portugues #professor #saladeaula #quiz',
 'QE-C3': '5 perguntas de História do Brasil valendo pódio. 📜\nArraste, responda de cabeça e confira o gabarito no fim.\n\nNo Quiddo, a turma responde pelo celular e a resposta aparece no telão. Grátis até 10 pessoas. Link na bio.\n#quiddo #historia #professor #saladeaula #quiz',
 'QE-C4': 'O treinamento que a equipe não esquece, em 4 passos. 💼\n1. Escreva as perguntas.\n2. Abra a sala no telão.\n3. A equipe responde pelo celular.\n4. Resposta e ranking no telão.\n\nQuiddo. Link na bio.\n#quiddo #treinamento #rh #onboarding #quiz',
}
TIT = {'QE-R1': 'Reel: a revisão de Geografia virou jogo', 'QE-R2': 'Reel: História do Brasil valendo pódio', 'QE-R3': 'Reel: Português, proparoxítona em segundos', 'QE-R4': 'Reel: o treinamento que a equipe não esquece',
       'QE-C1': 'Carrossel: 5 perguntas de Geografia + gabarito', 'QE-C2': 'Carrossel: 5 perguntas de Português + gabarito', 'QE-C3': 'Carrossel: 5 perguntas de História + gabarito', 'QE-C4': 'Carrossel: treinamento em quiz, 4 passos'}
CLIP = {'QE-R1': 'Mixkit 35954 (sala de aula)', 'QE-R2': 'Mixkit 48165 (sala de aula)', 'QE-R3': 'Mixkit 6676 (sala de aula)', 'QE-R4': 'Mixkit 45957 (treinamento)',
        'QE-C1': 'foto do Mixkit 21995', 'QE-C2': 'foto do Mixkit 36046', 'QE-C3': 'foto do Mixkit 5940', 'QE-C4': 'foto do Mixkit 46750'}
NOTA = ('Pedido do Gui (17/11): Quiddo voltado para sala de aula, educação e treinamento, com perguntas por matéria. Telas REAIS: partidas gravadas no Quiddo (código do repositório, modo Escola com os visuais Sala, Álbum e Espaço; '
        'modo Corporativo com Escritório), alunos e equipe com apelidos fictícios. Imagens de banco NOVAS (biblioteca ampliada hoje, 68 clipes), uma diferente por peça: ')
for k in ['QE-R1', 'QE-R2', 'QE-R3', 'QE-R4']:
    for suf, src in (('.mp4', Q / 'out' / f'{k}.mp4'), ('-capa.jpg', Q / 'out' / f'{k}-capa.jpg')):
        nm = k + suf
        if suf == '.mp4':
            import subprocess; subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(src), '-vf', 'scale=720:-2', '-c:v', 'libx264', '-crf', '24', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(MED / nm)], check=True)
        else:
            I = Image.open(src).convert('RGB'); I.thumbnail((720, 1280)); I.save(MED / nm, quality=86)
        UP.append('media/' + nm)
    e = dict(id=k, brand='Quiddo', fmt='reel', day=-40, dia='a programar', slot='19h45', title=TIT[k], kind='educacao', caption=CAP[k],
             notes=NOTA + CLIP[k] + '. Música Mixkit. Sem voz.', version=f'{k}-v1', v=1, hash=H5(Q / 'out' / f'{k}.mp4'), media=[f'{k}.mp4'],
             cover=f'{k}-capa.jpg', cover45=f'{k}-capa.jpg', poster=f'{k}-capa.jpg', duration=14.8, sticker='', mudou='Peça nova: Quiddo educação.')
    d['pieces'] = [p for p in d['pieces'] if p['id'] != k] + [e]
for k in ['QE-C1', 'QE-C2', 'QE-C3', 'QE-C4']:
    fs = sorted((Q / 'car').glob(f'{k}-*.png'), key=lambda x: int(x.stem.split('-')[-1])); names = []
    for f in fs:
        nm = f.stem + '.jpg'; I = Image.open(f).convert('RGB'); I.save(MED / nm, quality=86); names.append(nm); UP.append('media/' + nm)
    e = dict(id=k, brand='Quiddo', fmt='carrossel', day=-40, dia='a programar', slot='12h30', title=TIT[k], kind='educacao', caption=CAP[k],
             notes=NOTA + CLIP[k] + '. Último card: CTA claro.', version=f'{k}-v1', v=1, hash=H5(fs[-1]), media=names, previews=names, sticker='', duration=None, mudou='Peça nova: Quiddo educação.')
    d['pieces'] = [p for p in d['pieces'] if p['id'] != k] + [e]

# R-C8: card final sem preço (rodada 13: "tira o preço de todas")
rc8 = S / 'packs' / 'S03' / 'retrozap' / 'carrosseis' / 'R-C8-8.png'
Image.open(W / 'n1' / 'ec' / 'rzc13-45.png').save(rc8)
nm = 'R-C8-8-v3.jpg'; Image.open(rc8).convert('RGB').save(MED / nm, quality=86); UP.append('media/' + nm)
p = next(x for x in d['pieces'] if x['id'] == 'R-C8')
p['previews'] = [x for x in p['previews'] if not x.startswith('R-C8-8')] + [nm]
p.update(version='S03-R-C8-v3', v=3, hash=H5(rc8), mudou='v3 (rodada 13: tirar o preço de todas): no card final saiu "R$ 13,99"; ficou "Pagamento único · sem assinatura". Resto igual.')

d['adsLote'] = [('17/11 · Stories viraram historinhas de 3 quadros (63 sequências, 17/11 a 07/12) e o Quiddo ganhou o pack educação: 4 Reels (Geografia, História, Português, treinamento) e 4 carrosséis, '
                 'com partidas reais gravadas no Quiddo e imagens novas do banco (68 clipes novos, nenhuma repetida entre as peças). Sem preço no orgânico (rodada 13).')] + d['adsLote']
d['rodada'] = max(d.get('rodada', 0), 14)
js = json.dumps(d, ensure_ascii=False).replace('</', '<\\/')
m = re.search(r'(<script id="manifest" type="application/json">)(.*?)(</script>)', s, re.S)
s = s[:m.start(2)] + js + s[m.end(2):]
(M / 'index.html').write_text(s)
(W / 'mesa_up.json').write_text(json.dumps(UP)); print('novos', len(UP), 'seq', len(novos))
