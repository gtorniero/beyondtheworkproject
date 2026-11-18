"""Corrige o PROMPT-GPT-SUBIR-ADS-1811.md depois dos pacotes por posicionamento (pack1811.py):
- regra: um anúncio = um tipo de mídia em todos os posicionamentos (nunca PNG no Feed + MP4 em Stories/Reels);
- arquivos de cada AD separados em anúncio de VÍDEO (9:16 / 4:5 / 1:1) e anúncio ESTÁTICO (9:16 / 4:5 / 1:1 / 1,91:1);
- rótulo de IA conforme o áudio real dos finais (lote 17–18/11: só música Mixkit, sem voz → não precisa);
- ADs ainda sem pacote completo: aviso de subir só o formato que existe, num anúncio de um tipo só.
Uso: python3 prompt1811_fix.py"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
P = REPO / 'ads' / 'PROMPT-GPT-SUBIR-ADS-1811.md'
AP = REPO / 'ads' / 'aprovados'
RAW = 'https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/ads/aprovados'
SEM_VOZ = re.compile(r'ADC-(RZ-(1[6-9]|2\d|3[0-2])|RK-1[1-9]|SF-1[1-6]|RN-0[6-9])(-SP)?-v\d+$')
s = P.read_text()

s = s.replace('# PROMPT · SUBIR NOVOS ANÚNCIOS NA META (18/11/2026 · rodada 16: tudo aprovado, inclusive RN-06 a RN-09)',
              '# PROMPT · SUBIR NOVOS ANÚNCIOS NA META (18/11/2026 · rodada 16: tudo aprovado, inclusive RN-06 a RN-09)\n\n'
              '> **Atualizado em 18/11 (Estúdio):** pacotes completos por posicionamento; arquivos separados em anúncio de VÍDEO e anúncio ESTÁTICO; '
              'rótulo de IA corrigido (os ADs do lote 17–18/11 têm só música, sem voz). Esta versão substitui a anterior.')
old4 = s[s.index('4. **Posicionamentos:**'):s.index('5. **Nome do anúncio')]
s = s.replace(old4, '''4. **Posicionamentos: Advantage+ (automático), com UMA regra obrigatória (Gui):** cada anúncio mantém o mesmo criativo e o MESMO tipo de mídia em todos os posicionamentos. **Nunca** misture PNG no Feed com MP4 em Stories/Reels no mesmo anúncio.
   - **Anúncio de VÍDEO:** `_reels-stories-9x16.mp4` em Stories e Reels; `_video-feed-4x5.mp4` no Feed; `_video-feed-coluna-1x1.mp4` nos demais posicionamentos que aceitam vídeo.
   - **Anúncio ESTÁTICO** (se quiser rodar também, é OUTRO anúncio): `_stories-reels-9x16.png` em Stories e Reels; `_feed-4x5.png` no Feed; `_feed-1x1.png` na coluna da direita, Marketplace e demais; `_busca-audience-1.91x1.png` em busca e Audience Network (quando existir).
   - Se um AD não tiver o pacote completo, suba só o tipo de mídia que existe, nos posicionamentos dele (está avisado no AD).
   - Carrossel: os cards na ordem dos números.
''')
s = s.replace('7. **Rótulo de IA da Meta:** marque só onde está escrito "SIM".',
              '7. **Rótulo de IA da Meta:** marque só onde está escrito "SIM" (só os ADs com narração de voz de IA; os ADs com só música não precisam).')

def files(v):
    d = next(AP.glob(f'*/{v}'), None)
    return d, (sorted(x.name for x in d.iterdir() if x.name != 'LEIA-ME.md') if d else [])

def fix(m):
    head, body = m.group(1), m.group(2); v = head.strip()[4:].strip()
    if SEM_VOZ.match(v):
        body = re.sub(r'- \*\*Rótulo de IA da Meta:\*\* .*', '- **Rótulo de IA da Meta:** não precisa (só música de banco, sem voz)', body)
    d, fs = files(v)
    if not d or 'carrossel' in ' '.join(fs): return head + body
    br = d.parent.name; u = lambda n: f'  - {RAW}/{br}/{v}/{v}_{n}'
    vid = [n for n in ('reels-stories-9x16.mp4', 'video-feed-4x5.mp4', 'video-feed-coluna-1x1.mp4') if f'{v}_{n}' in fs]
    est = [n for n in ('stories-reels-9x16.png', 'feed-4x5.png', 'feed-1x1.png', 'busca-audience-1.91x1.png') if f'{v}_{n}' in fs]
    if len(vid) < 3 and not any(f'{v}_{n}' in fs for n in ('video-feed-4x5.mp4', 'feed-4x5_hero.png')):
        av = ('- **Atenção:** este AD ainda não tem o pacote completo. Suba só como anúncio de VÍDEO 9:16, em Stories e Reels (sem PNG no mesmo anúncio).' if vid else
              '- **Atenção:** este AD só tem o estático 1:1. Suba só como anúncio ESTÁTICO 1:1 (Feed, coluna da direita e demais), sem vídeo no mesmo anúncio.')
        if '**Atenção:**' not in body: body = body.replace('- **Arquivos:**', av + '\n- **Arquivos:**', 1)
        return head + body
    if not vid or 'video-feed-4x5.mp4' not in ' '.join(vid): return head + body  # pacotes antigos (RK-08, SF-08, RK-09): já completos
    new = ('- **Arquivos · anúncio de VÍDEO** (9:16 em Stories/Reels · 4:5 no Feed · 1:1 nos demais):\n' + '\n'.join(u(n) for n in vid) + '\n'
           '- **Arquivos · anúncio ESTÁTICO** (outro anúncio, opcional):\n' + '\n'.join(u(n) for n in est) + '\n')
    body = re.sub(r'- \*\*Arquivos:\*\*\n(  - .*\n?)+', new, body)
    return head + body

s = re.sub(r'(### ADC-[^\n]+\n)(.*?)(?=\n### |\n## |\Z)', fix, s, flags=re.S)
P.write_text(s)
print('ok')
