"""Entra no pack S03 (agenda, STATUS, LEGENDAS) e na Mesa: 8 reels dos buracos (24/26/28) + 3 carrosséis FIXAR do SPORT DNA.
Também: coluna "como" = postar.py em todas as agendas e coluna "serie" (vazia nas peças novas, que não são série)."""
import csv, io, json, re, shutil, subprocess, hashlib, glob
from pathlib import Path
from PIL import Image
W = Path(__file__).resolve().parent.parent; S = W.parent / 'social'; PK = S / 'packs'; M = W / 'mesa'; MED = M / 'media'
RAW = 'https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/packs/S03'
H5 = lambda p: hashlib.md5(Path(p).read_bytes()).hexdigest()[:10]
BR = {'R': ('Retrozap', 'retrozap'), 'Q': ('Quiddo', 'quiddo'), 'D': ('SPORT DNA', 'sportdna')}
DOW = {'23/11': 'seg', '24/11': 'ter', '25/11': 'qua', '26/11': 'qui', '27/11': 'sex', '28/11': 'sáb', '29/11': 'dom'}
DAY = {'23/11': 1, '24/11': 2, '25/11': 3, '26/11': 4, '27/11': 5, '28/11': 6, '29/11': 7}
REELS = {
 'R-R16': ('24/11', 'Sexta, 23h: 214 mensagens não lidas', 'Sexta, 23h. 214 mensagens não lidas. 🫠\nTudo sobre o churrasco que ninguém confirmou.\n\nManda pro grupo que mais fala 📲\nA retrospectiva do seu grupo: link na bio. O 1º grupo é grátis.\n#retrozap #whatsapp #grupodewhatsapp #amigos #churrasco'),
 'R-R17': ('26/11', 'Quem manda mais boa noite?', 'Quem manda mais boa noite? 🌙\nEla jura que é ela. A conversa diz outra coisa.\n\nManda pro seu amor e tira a prova ❤️\nA retrospectiva de vocês dois: link na bio.\n#retrozap #casal #namoro #whatsapp'),
 'R-R18': ('28/11', 'Grupo da família: ativado', 'Dezembro chegando: grupo da família ativado. 🎄\nBom dia da tia às 6h e a eterna pergunta: quem leva a farofa?\n\nManda no grupo da família 👇\nA retrospectiva do grupo: link na bio. O 1º grupo é grátis.\n#retrozap #familia #natal #grupodafamilia'),
 'D-R16': ('24/11', 'RACKET · POV: você ia comprar raquete hoje', 'Você ia comprar raquete hoje. Aí veio a pergunta: qual o peso dela? 🎾\nPeso, balanço e swingweight mudam o seu jogo. O RACKET DNA cruza o seu corpo e o seu jogo com 183 raquetes medidas.\n\n🔖 Salva pra quando for comprar.\nFaça o teste: link na bio.\n#tenis #raquete #racketdna #tenisamador'),
 'D-R17': ('26/11', 'SURF · Primeira prancha escolhida pela cor', 'Primeira prancha escolhida pela cor. No mar, ela não rema. 🏄\nEra litragem, não cor. O SURF DNA calcula os seus litros pelo seu peso, o seu nível e o seu mar.\n\n🔖 Salva pra quando for comprar.\nFaça o teste: link na bio.\n#surf #prancha #surfdna #surfista'),
 'D-R18': ('28/11', 'RACKET · Treina 2x por semana com a raquete do ídolo', 'Treina 2x por semana e joga com a raquete do ídolo? 🎾\nModelo de profissional tem mais peso e swingweight: o golpe chega atrasado. O RACKET DNA mostra a raquete do seu jogo.\n\n🔖 Salva pra quando for comprar.\nFaça o teste: link na bio.\n#tenis #raquete #racketdna'),
 'Q-R15': ('26/11', 'Treinamento, slide 47', 'Treinamento, slide 47. Metade da sala no celular. 📱\nE se o celular fosse o jogo? No Quiddo, a equipe responde pelo celular e o ranking aparece no telão.\n\nManda pra quem organiza o treinamento 📲\nFaça o seu. Teste grátis: link na bio.\n#quiddo #treinamento #rh #quiz'),
 'Q-R16': ('28/11', 'Última aula antes das férias', 'Última aula antes das férias. Ninguém presta atenção... até o quiz começar. 🍎\nA revisão vira jogo: a turma responde pelo celular e o pódio sai no telão.\n\nManda pra um professor 👇\nFaça o seu. Teste grátis: link na bio.\n#quiddo #professor #saladeaula #quiz'),
}
FX = {
 'D-FX1': ('25/11', 'FIXAR · O que tem por trás do teste (grandes números)', 8, 'O que tem por trás do teste do SPORT DNA. 📊\n2.425 reviews lidas, 1.035 casos reais, 62 estudos científicos, 395 tênis e raquetes com ficha técnica, 13 tipos de prancha e 11.000 perfis simulados. E 0 marcas pagando para aparecer.\n\n🔖 Salva pra quando for comprar raquete, prancha ou tênis.\nFaça o teste: link na bio.\n#sportdna #racketdna #surfdna #rundna'),
 'D-FX2': ('27/11', 'FIXAR · Como funciona o teste, em 3 passos', 6, 'Como funciona o teste, em 3 passos. ✅\n1. Responda, sem cadastro.\n2. Veja a análise grátis: seu perfil, as especificações ideais e o grau de confiança.\n3. Receba os finalistas.\nO SURF e o RUN funcionam igual; no RUN, o relatório completo é grátis.\n\n🔖 Salva pra quando for comprar.\nFaça o teste: link na bio.\n#sportdna #racketdna #surfdna #rundna'),
 'D-FX3': ('29/11', 'FIXAR · Os motores: o que você informa → o que a gente calcula', 8, 'O que você informa → o que a gente calcula. ⚙️\nRACKET: peso, balanço, swingweight, rigidez, cabeça, padrão, corda e tensão, grip. SURF: shape, litragem, rabeta, quilhas. RUN: drop, espuma, custo por km.\nMesmas respostas, mesmo resultado. Nenhuma marca no comando.\n\n🔖 Salva pra quando for comprar.\nFaça o teste: link na bio.\n#sportdna #racketdna #surfdna #rundna'),
}
for t in [c for _, _, c in REELS.values()] + [c for *_, c in FX.values()]:
    assert not re.search(r'exemplo|simula[çc][ãa]o|fict[íi]ci|feito por IA|R\$', t, re.I), t
# arquivos no pack
P3 = PK / 'S03'; rows_new = []; st = json.loads((P3 / 'STATUS.json').read_text()); leg_add = {}
for k, (dt, tit, cap) in REELS.items():
    br, bd = BR[k[0]]; d = P3 / bd / 'reels'; shutil.copy(W / 'gap' / k / f'{k}.mp4', d / f'{k}.mp4'); shutil.copy(W / 'gap' / k / f'{k}-capa.png', d / f'{k}-capa.png')
    v = f'S03-{k}-v1'; files = [f'{k}.mp4', f'{k}-capa.png']
    rows_new.append(dict(data=f'{dt}/2026 ({DOW[dt]})', hora='19h45', marca=br, formato='reel', peca=k, versao=v, como='postar.py', arquivos=', '.join(files), links=' '.join(f'{RAW}/{bd}/reels/{f}' for f in files), adesivo='', titulo=tit, serie='', observacao='buraco de reel (série bloqueada pela trava); esqueleto e fundo novos'))
    st['pecas'].append(dict(peca=k, marca=br, formato='reel', dia=f'{DOW[dt]} {dt}', hora='19h45', versao=v, liberado=False, status_mesa='aguardando aprovação na Mesa'))
    leg_add.setdefault(bd, []).append(f'{v} · {DOW[dt]} {dt} · 19h45 · REEL · {tit}\nArquivos: {", ".join(files)}\nÁudio: música de banco (Mixkit), sem voz.\n\nLEGENDA\n{cap}\n\nNotas: buraco de reel; esqueleto e fundo novos (nenhum clipe repetido).\n\n' + '-' * 60 + '\n')
for k, (dt, tit, n, cap) in FX.items():
    d = P3 / 'sportdna' / 'carrosseis'; files = []
    for i in range(1, n + 1): shutil.copy(W / 'fix' / f'{k}-{i}.png', d / f'{k}-{i}.png'); files.append(f'{k}-{i}.png')
    v = f'S03-{k}-v1'
    rows_new.append(dict(data=f'{dt}/2026 ({DOW[dt]})', hora='12h30', marca='SPORT DNA', formato='carrossel', peca=k, versao=v, como='postar.py', arquivos=', '.join(files), links=' '.join(f'{RAW}/sportdna/carrosseis/{f}' for f in files), adesivo='', titulo=tit, serie='', observacao='FIXAR no perfil (o Gui fixa os três)'))
    st['pecas'].append(dict(peca=k, marca='SPORT DNA', formato='carrossel', dia=f'{DOW[dt]} {dt}', hora='12h30', versao=v, liberado=False, status_mesa='aguardando aprovação na Mesa · FIXAR'))
    leg_add.setdefault('sportdna', []).append(f'{v} · {DOW[dt]} {dt} · 12h30 · CARROSSEL · {tit}\nArquivos: {", ".join(files)}\n\nLEGENDA\n{cap}\n\nNotas: FIXAR no perfil. Números da home do site (22/11).\n\n' + '-' * 60 + '\n')
st['total'] = len(st['pecas']); st['liberadas'] = sum(1 for x in st['pecas'] if x.get('liberado'))
(P3 / 'STATUS.json').write_text(json.dumps(st, ensure_ascii=False, indent=1))
for bd, blocks in leg_add.items():
    lg = P3 / bd / 'LEGENDAS.txt'; lg.write_text(lg.read_text().rstrip('\n') + '\n\n' + '\n'.join(blocks))
# agendas: como → postar.py, coluna serie (+ observacao onde faltar)
SER = json.loads(subprocess.check_output(['git', '-C', str(S), 'show', 'origin/claude/sweet-hypatia-43ca1s:growth/postagem/series.json']))
PSER = {p: g for g, x in SER['grupos'].items() for p in x['pecas']}
for ag in sorted(PK.glob('*/agenda.csv')):
    rows = list(csv.DictReader(io.StringIO(ag.read_text())))
    if not rows: continue
    fields = list(rows[0].keys())
    for col in ('como', 'serie', 'observacao'):
        if col not in fields: fields.append(col)
    for r in rows:
        r['como'] = 'postar.py'; r.setdefault('serie', ''); r['serie'] = PSER.get(r['peca'], r.get('serie') or ''); r.setdefault('observacao', '')
    if ag.parent.name == 'S03':
        rows += rows_new
        rows.sort(key=lambda r: (r['data'][6:10], r['data'][3:5], r['data'][:2], r['hora'], r['marca']))
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n', extrasaction='ignore'); w.writeheader(); w.writerows(rows); ag.write_text(out.getvalue())
print('pack ok')
# Mesa (sobre o work/mesa/index.html = v84 publicada)
s = (M / 'index.html').read_text(); RX = r'(<script id="manifest" type="application/json">)(.*?)(</script>)'
m = re.search(RX, s, re.S); d = json.loads(m.group(2)); UP = []
for k, (dt, tit, cap) in REELS.items():
    br, bd = BR[k[0]]; src = W / 'gap' / k / f'{k}.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(src), '-vf', 'scale=720:-2', '-c:v', 'libx264', '-crf', '24', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(MED / f'S03-{k}.mp4')], check=True)
    I = Image.open(W / 'gap' / k / f'{k}-capa.png').convert('RGB'); I.thumbnail((720, 1280)); I.save(MED / f'S03-{k}-capa.jpg', quality=85)
    UP += [f'media/S03-{k}.mp4', f'media/S03-{k}-capa.jpg']
    e = dict(id=k, brand=br, fmt='reel', day=DAY[dt], dia=f'{DOW[dt]} {dt}', slot='19h45', title=tit, kind='reel', caption=cap, version=f'S03-{k}-v1', v=1, sticker='', duration=11.0,
             hash=H5(src), media=[f'S03-{k}.mp4'], poster=f'S03-{k}-capa.jpg', cover=f'S03-{k}-capa.jpg', cover45=f'S03-{k}-capa.jpg',
             notes='Buraco de reel (a trava de série do Growth bloqueou a peça do dia). Esqueleto novo e fundo de banco nunca usado; só música de banco.',
             mudou='Peça nova (22/11): preenche o buraco de reel do dia.')
    d['pieces'] = [p for p in d['pieces'] if p['id'] != k] + [e]
for k, (dt, tit, n, cap) in FX.items():
    names = []
    for i in range(1, n + 1):
        nm = f'S03-{k}-{i}.jpg'; Image.open(W / 'fix' / f'{k}-{i}.png').convert('RGB').save(MED / nm, quality=84); names.append(nm); UP.append('media/' + nm)
    e = dict(id=k, brand='SPORT DNA', fmt='carrossel', day=DAY[dt], dia=f'{DOW[dt]} {dt}', slot='12h30', title=tit, kind='carrossel', caption=cap, version=f'S03-{k}-v1', v=1, sticker='', duration=None,
             hash=H5(W / 'fix' / f'{k}-{n}.png'), media=names, previews=names, notes='FIXAR no perfil (pedido do Gui, 22/11). Números da home do site. RACKET em pelo menos metade dos cards.', mudou='Peça nova (22/11): carrossel didático para fixar.')
    d['pieces'] = [p for p in d['pieces'] if p['id'] != k] + [e]
DEL = []
for p in [p for p in d['pieces'] if -10 < p.get('day', 0) < 0]:
    d['pieces'].remove(p); d['arquivo'].append(dict(id=p['id'], title=p['title'], dia=p.get('dia'), version=p['version']))
    DEL += ['media/' + x for x in set((p.get('media') or []) + (p.get('previews') or []) + [p.get('cover'), p.get('poster'), p.get('cover45')]) if x]
d['final'] = {}
DEL += [f'final/{b}/{f}' for b in ('quiddo', 'retrozap', 'sportdna') for f in ('GUIA-PUBLICACAO-DOT.md', 'LEGENDAS.txt', 'agenda.csv')]
d['adsLote'] = ['22/11 · SPORT DNA: 3 carrosséis didáticos para FIXAR no perfil (D-FX1 grandes números, D-FX2 como funciona o teste, D-FX3 os motores). '
                'Reels novos para os buracos de 24, 26 e 28/11 (séries bloqueadas pela trava): Retrozap R-R16/17/18, SPORT DNA D-R16 (RACKET), D-R17 (SURF), D-R18 (RACKET), Quiddo Q-R15/16. '
                'Três esqueletos diferentes, alternados por dia (legenda embaixo · cartão no topo · palavra no centro), fundos de banco nunca usados, só música, CTA de salvar ou mandar pro grupo.'] + d['adsLote']
js = json.dumps(d, ensure_ascii=False).replace('</', '<\\/'); s = s[:m.start(2)] + js + s[m.end(2):]; (M / 'index.html').write_text(s)
DEL = [x for x in dict.fromkeys(DEL) if x.startswith('final/') or x.split('/', 1)[1] not in js]
F = {x: 'work/mesa/' + x for x in UP}; F.update({x: None for x in DEL})
(W / 'gap' / 'files.json').write_text(json.dumps(F)); print('mesa ok', len(UP), 'del', len(DEL))
