"""Coloca os 2 tutoriais do Retrozap (grupo e casal) na Mesa existente, numa aba própria, sem tocar nas outras peças, votos ou ADs.
Na Mesa vai a versão para WhatsApp (leve); o master fica no GitHub. Capa = pôster = miniatura.
Uso: python3 tut_mesa.py <index.html publicado, sem o esqueleto> <pasta com os arquivos> <saida.html>"""
import hashlib, json, re, sys
from pathlib import Path

live, src, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
GH = 'https://github.com/gtorniero/beyondtheworkproject/tree/social/tutoriais/retrozap'
DAY, LABEL = -20, 'Tutoriais · WhatsApp'
TUT = {
    'TUT-RZ-GRUPO': dict(title='Tutorial: como fazer a retrospectiva do GRUPO (Android)', arq='TUT-RZ-GRUPO-v1'),
    'TUT-RZ-CASAL': dict(title='Tutorial: como fazer a retrospectiva de CASAL (iPhone)', arq='TUT-RZ-CASAL-v1'),
}
s = live.read_text()
m = re.search(r'(<script id="manifest" type="application/json">)(.*?)(</script>)', s, re.S)
M = json.loads(m.group(2).replace('<\\/', '</'))
have = {p['id'] for p in M['pieces']}
M['days'][str(DAY)] = LABEL
M['rodada'] = M.get('rodada', 0) + 1  # a rodada anterior já foi enviada; os tutoriais abrem a próxima
for pid, t in TUT.items():
    assert pid not in have, f'{pid} já está na Mesa'
    v = t['arq']; mp4 = src / f'{v}-whatsapp.mp4'
    meta = json.loads((src / f'{v}.json').read_text())
    M['pieces'].append(dict(id=pid, brand='Retrozap', fmt='reel', day=DAY, dia='tutorial', slot='', title=t['title'], kind='tutorial',
                            caption=meta['mensagem'], notes=meta['notas'], version=v, v=1, hash=hashlib.md5(mp4.read_bytes()).hexdigest()[:10],
                            media=[f'{v}-whatsapp.mp4'], editable=f'{GH}/{v}', duration=meta['duracao'], sticker='',
                            poster=f'{v}-capa.jpg', cover=f'{v}-capa.jpg', cover45=f'{v}-capa.jpg'))
js = json.dumps(M, ensure_ascii=False).replace('</', '<\\/')
out.write_text(s[:m.start(2)] + js + s[m.end(2):])
print('ok', len(M['pieces']), 'peças')
