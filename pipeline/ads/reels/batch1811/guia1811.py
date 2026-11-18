"""Acrescenta ao GUIA-ADS-AGORA.md (fila "prontos para usar") o lote 17–18/11 aprovado na Mesa (rodadas 15 e 16), só com o que tem pacote completo.
Uso: python3 guia1811.py"""
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]
G = REPO / 'ads' / 'aprovados' / 'GUIA-ADS-AGORA.md'
T = 'https://github.com/gtorniero/beyondtheworkproject/tree/social/ads/aprovados'
GRUPOS = [
    ('Retrozap · casal SEM preço (PRIORIDADE; novembro e dezembro)', 'retrozap', ['ADC-RZ-18-SP-v1', 'ADC-RZ-19-SP-v1', 'ADC-RZ-20-SP-v1', 'ADC-RZ-21-SP-v1', 'ADC-RZ-22-SP-v1', 'ADC-RZ-28-v1', 'ADC-RZ-30-v1', 'ADC-RZ-32-v1']),
    ('Retrozap · casal COM preço R$ 13,99 (teste A/B; pausar no fim de 30/11)', 'retrozap', ['ADC-RZ-18-v3', 'ADC-RZ-19-v2', 'ADC-RZ-20-v2', 'ADC-RZ-21-v2', 'ADC-RZ-22-v2']),
    ('Retrozap · grupo (sem preço)', 'retrozap', ['ADC-RZ-23-v1', 'ADC-RZ-24-v1', 'ADC-RZ-25-v1', 'ADC-RZ-26-v1', 'ADC-RZ-27-v1', 'ADC-RZ-29-v1', 'ADC-RZ-31-v1', 'ADC-RZ-16-v1', 'ADC-RZ-17-v1']),
    ('RACKET DNA (RK-12: Black Friday, só até 27/11; RK-14: só estático)', 'sportdna', ['ADC-RK-11-v1', 'ADC-RK-12-v1', 'ADC-RK-13-v1', 'ADC-RK-14-v1', 'ADC-RK-15-v1', 'ADC-RK-16-v1', 'ADC-RK-17-SP-v1', 'ADC-RK-17-v2', 'ADC-RK-18-v1', 'ADC-RK-19-v1']),
    ('SURF DNA (SF-12: Black Friday, só até 27/11)', 'sportdna', ['ADC-SF-11-v1', 'ADC-SF-12-v1', 'ADC-SF-13-v1', 'ADC-SF-14-SP-v1', 'ADC-SF-14-v2', 'ADC-SF-15-v1', 'ADC-SF-16-SP-v1', 'ADC-SF-16-v2']),
    ('TÊNIS DNA · Corredores (campanha nova)', 'sportdna', ['ADC-RN-06-v1', 'ADC-RN-07-v1', 'ADC-RN-08-v1', 'ADC-RN-09-v1']),
]
s = G.read_text()
assert 'Lote 17–18/11' not in s, 'já acrescentado'
blk = ['## Lote 17–18/11 · aprovados na Mesa e com pacote completo · acrescentado em 18/11', '',
       'Regra (Gui): **um anúncio = um tipo de mídia em todos os posicionamentos.** Anúncio de vídeo: 9:16 em Stories/Reels, 4:5 no Feed, 1:1 nos demais. '
       'Anúncio estático (outro anúncio): 9:16, 4:5, 1:1 e 1,91:1. Nunca PNG no Feed com MP4 em Stories/Reels. Nenhum destes tem voz (só música de banco): rótulo de IA não precisa.', '']
for t, br, ids in GRUPOS:
    blk += [f'### {t}', ''] + [f'- **{v}** → [`{br}/{v}/`]({T}/{br}/{v}) (copy, título e URL no LEIA-ME da pasta)' for v in ids] + ['']
s = s.replace('## Regras fixas', '\n'.join(blk) + '\n## Regras fixas', 1)
G.write_text(s)
print('ok')
