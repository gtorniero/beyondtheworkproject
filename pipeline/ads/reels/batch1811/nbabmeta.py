"""Metadados das versões COM e SEM preço (18/11, pedido do Gui)."""
import re
from nb18meta import ADS as A18, DIR
from nbmeta import ADS as A17
B = {a['id']: a for a in A17 + A18}
_lm = open('/tmp/claude-0/-home-user-beyondtheworkproject/d7452b64-01ec-54a7-b200-d4dc961592d6/scratchpad/social/ads/aprovados/retrozap/ADC-RZ-18-v2/LEIA-ME.md').read()
B['ADC-RZ-18'] = dict(B['ADC-RZ-18'], copy=_lm.split('## Copy\n')[1].split('\n\nTítulo')[0].strip(), titulo='Retrospectiva de casal do seu zap', title='Retrospectiva de casal do seu zap')
CTA = {'Retrozap': 'Na arte: "Teste o de vocês agora". Botão do anúncio: Saiba mais.', 'SPORT DNA': 'Na arte: "Teste o seu agora". Botão do anúncio: Saiba mais.'}
def semp(t):
    t = re.sub(r'[^.\n]*R\$ ?[\d.,]+[^.\n]*\.\s*', '', t)
    return re.sub(r'\n{3,}', '\n\n', t).strip()
ADS = []
for aid, ver in (('ADC-RZ-18', 'v3'), ('ADC-RZ-19', 'v2'), ('ADC-RZ-20', 'v2'), ('ADC-RZ-21', 'v2'), ('ADC-RZ-22', 'v2'), ('ADC-RK-17', 'v2'), ('ADC-SF-14', 'v2'), ('ADC-SF-16', 'v2')):
    b = dict(B[aid]); b['cta'] = CTA[b['brand']]
    cp = dict(b, ver=ver, title=b['title'].replace(' (com preço)', '') + ' · COM preço (preço depois)',
              mudou=f'{ver} (18/11, seu pedido: "preço logo no começo não faz sentido; outro CTA, Teste o seu agora"): o preço saiu do topo e virou o 2º número (no motion aparece depois); botão "{b["cta"].split(chr(34))[1]}". Tem a versão SEM preço ao lado ({aid}-SP).')
    cp['url'] = re.sub(r'utm_content=[^&]*', f'utm_content={aid}-{ver}', b['url'])
    sp = dict(b, id=aid + '-SP', ver='v1', title=b['title'].replace(' (com preço)', '') + ' · SEM preço', copy=semp(b['copy']),
              objetivo=re.sub(r' \(R\$[^)]*\)', '', b['objetivo']), notes='Sem preço na arte nem na copy: a pessoa vê o valor no site.',
              mudou=f'Nova (18/11, seu pedido: versão sem preço; CTA "{b["cta"].split(chr(34))[1]}"). Par da {aid}-{ver} (com preço).')
    sp['url'] = re.sub(r'utm_content=[^&]*', f'utm_content={aid}-SP-v1', b['url'])
    ADS += [cp, sp]
for a in ADS:
    if a['id'].endswith('-SP'): assert 'R$' not in a['copy'], a['id']
