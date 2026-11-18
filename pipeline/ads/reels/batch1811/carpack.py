"""Fecha o pacote dos carrosséis aprovados ADC-RZ-15-v1 e ADC-RK-10-v2 (saída do carfmt.py), sem mexer nos cards 1:1 aprovados:
copia os novos formatos para ads/aprovados/<marca>/<ID>/, reescreve o LEIA-ME (status real e arquivos separados por anúncio),
atualiza o PROMPT-GPT-SUBIR-ADS-1811 (arquivos de cada anúncio), o GUIA-ADS-AGORA e o INDEX.
Uso: python3 carpack.py <saída do carfmt>"""
import re, shutil, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
AP = REPO / 'ads' / 'aprovados'
SRC = Path(sys.argv[1])
RAW = 'https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/ads/aprovados'
TREE = 'https://github.com/gtorniero/beyondtheworkproject/tree/social/ads/aprovados'
CAR = {'ADC-RZ-15-v1': ('retrozap', 5, 'aprovado na Mesa em 17/11/2026', 2.8, 'A retrospectiva do seu grupo, passo a passo (carrossel)'),
       'ADC-RK-10-v2': ('sportdna', 7, 'aprovado na Mesa em 18/11/2026', 3.4, 'Carrossel RACKET com história')}


def files(v, n):
    car = {k: [f'{v}_carrossel-{k}-card{i}.png' for i in range(1, n + 1)] for k in ('1x1', 'feed-4x5', 'stories-9x16')}
    vid = [f'{v}_video-sequencia-reels-stories-9x16.mp4', f'{v}_video-sequencia-feed-4x5.mp4', f'{v}_video-sequencia-1x1.mp4']
    return car, vid


for v, (br, n, st, sec, tit) in CAR.items():
    d = AP / br / v; car, vid = files(v, n)
    for f in car['feed-4x5'] + car['stories-9x16'] + vid: shutil.copy(SRC / v / f, d / f)
    for f in car['1x1']: assert (d / f).exists(), f            # originais 1:1 ficam como estão
    # ---- LEIA-ME
    s = (d / 'LEIA-ME.md').read_text()
    s = re.sub(r'\*\*aguardando aprovação na Mesa\*\*[^\n]*|aguardando aprovação na Mesa[^\n]*', f'**{st}** (status real no banco da Mesa)', s, count=1)
    s = s.replace('carrossel 1:1, 4 cards (a ordem é a dos números)', f'carrossel, {n} cards (a ordem é a dos números)')
    if '## Arquivos por posicionamento' in s: s = s[:s.index('## Arquivos por posicionamento')]
    s = re.sub(r'## Arquivos\n(- `[^\n]*\n)+\n?', '', s)                    # lista antiga (só 1:1); a seção Origem fica
    s = re.sub(r'\n- `[^`]*_carrossel-1x1-card\d\.png` \(CTA\)', '', s)
    s = s.rstrip() + '\n\n' + (
        '## Arquivos por posicionamento (18/11)\n\n'
        f'Os {n} cards 1:1 aprovados não mudaram. O 4:5 e o 9:16 são os MESMOS cards, inteiros e sem escala (o card 1:1 está pixel por pixel '
        'dentro de cada um, conferido), na mesma ordem. O espaço a mais é só o fundo do próprio card continuando (mesma cor e, quando o card tem, a mesma grade); '
        'nada foi redesenhado, cortado ou gerado por IA. Onde o print do celular encosta na base do card (RZ-15, cards 1 a 4), o fundo continua por baixo e o print se funde nele em poucos pixels. No 9:16, todo o card fica fora das zonas de interface (250 px no topo e 340 px embaixo).\n\n'
        f'**Anúncio CARROSSEL** (só imagens; os {n} cards na ordem dos números, a mesma URL em todos):\n'
        + '\n'.join(f'- card {i}: `{a}` (1:1, coluna da direita, Marketplace e demais) · `{b}` (Feed) · `{c}` (Stories e Reels)'
                    for i, (a, b, c) in enumerate(zip(car['1x1'], car['feed-4x5'], car['stories-9x16']), 1)) + '\n\n'
        '**Anúncio de VÍDEO** (OUTRO anúncio, opcional; para Reels quando o carrossel não entra lá): a mesma sequência de cards, na mesma ordem, '
        + f'{sec:g} s por card com fusão curta, {n * sec + .35:.1f} s no total:\n'.replace('.', ',') +
        f'- `{vid[0]}`: Reels e Stories.\n- `{vid[1]}`: Feed.\n- `{vid[2]}`: demais posicionamentos que aceitam vídeo.\n\n'
        'Nunca misture o carrossel (PNG) e o vídeo (MP4) no mesmo anúncio. Sem áudio (o carrossel aprovado não tem trilha; se quiser música, '
        'use a biblioteca da Meta). Sem voz: não precisa do rótulo de IA.\n\n'
        'Nada foi enviado à conta de anúncios.\n')
    if v != 'ADC-RZ-15-v1': s = s.replace('Onde o print do celular encosta na base do card (RZ-15, cards 1 a 4), o fundo continua por baixo e o print se funde nele em poucos pixels. ', '')
    (d / 'LEIA-ME.md').write_text(s)
    print('ok', v, len(list(d.iterdir())), flush=True)

# ---- PROMPT: arquivos de cada anúncio
P = REPO / 'ads' / 'PROMPT-GPT-SUBIR-ADS-1811.md'; p = P.read_text()
for v, (br, n, st, sec, tit) in CAR.items():
    car, vid = files(v, n); u = lambda f: f'  - {RAW}/{br}/{v}/{f}'
    new = (f'- **Arquivos · anúncio CARROSSEL** ({n} cards, nesta ordem; em cada card: 1:1 nos demais · 4:5 no Feed · 9:16 em Stories/Reels):\n'
           + '\n'.join(f'  - card {i}:\n' + u(a).replace('  - ', '    - ') + '\n' + u(b).replace('  - ', '    - ') + '\n' + u(c).replace('  - ', '    - ')
                       for i, (a, b, c) in enumerate(zip(car['1x1'], car['feed-4x5'], car['stories-9x16']), 1)) + '\n'
           f'- **Arquivos · anúncio de VÍDEO** (OUTRO anúncio, opcional, para Reels; mesma sequência; 9:16 em Reels/Stories · 4:5 no Feed · 1:1 nos demais; sem áudio):\n'
           + '\n'.join(u(f) for f in vid) + '\n')
    a = p.index(f'### {v}\n'); b = p.index('- **Arquivos:**\n', a); e = p.index('\n\n', b) + 1
    assert b < p.index('\n### ', a + 5) if '\n### ' in p[a + 5:] else True
    p = p[:b] + new + p[e:]
    p = p.replace(f'### {v}\n', f'### {v}\n- **Nota (18/11):** formatos 4:5 e 9:16 do carrossel prontos (mesmos cards); vídeo da sequência como anúncio separado. Não misturar.\n', 1)
P.write_text(p)

# ---- GUIA e INDEX
G = AP / 'GUIA-ADS-AGORA.md'; g = G.read_text()
if 'Carrosséis com 4:5 e 9:16' not in g:
    blk = ['### Carrosséis com 4:5 e 9:16 (acrescentado em 18/11)', '',
           'Anúncio carrossel (cards 1:1/4:5/9:16, mesma ordem) e, separado, o vídeo da mesma sequência para Reels. Nunca no mesmo anúncio.', '']
    blk += [f'- **{v}** → [`{br}/{v}/`]({TREE}/{br}/{v}) ({n} cards; copy, título e URL no LEIA-ME da pasta)' for v, (br, n, *_) in CAR.items()]
    g = g.replace('## Regras fixas', '\n'.join(blk) + '\n\n## Regras fixas', 1); G.write_text(g)
I = AP / 'INDEX.md'; ix = I.read_text().rstrip('\n')
for v, (br, n, st, sec, tit) in CAR.items():
    aid, ver = v.rsplit('-', 1)
    if f'| {aid} | {ver} |' not in ix: ix += f'\n| {br} | {aid} | {ver} | atual | {tit} | {TREE}/{br}/{v} |'
I.write_text(ix + '\n')
print('prompt, guia, index ok')
