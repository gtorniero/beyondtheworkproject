"""Brief Growth 19/11: 8 variações (6 estáticos 1:1 + 2 vídeos 9:16) → pastas em ads/em-aprovacao + Mesa (sobre a versão publicada)."""
import json, re, hashlib, subprocess, shutil
from pathlib import Path
from PIL import Image
B = Path(__file__).resolve().parent; W = B.parent; S = W.parent / 'social'
LIVE = W.parent / 'artifact-files' / '9327c3d4-8cce-48f2-a7b4-3f3d7f0ad80c' / 'index.html'
M = W / 'mesa'; MED = M / 'media'
H5 = lambda p: hashlib.md5(Path(p).read_bytes()).hexdigest()[:10]
U = 'utm_source=meta&utm_medium=paid_social'
RKD = ['Tela/arte própria do RACKET DNA. Números do site (183 raquetes, 379 casos, 670 avaliações; raquetes no site de R$ 1.600 a R$ 2.300). Sem preço do relatório na arte.', 'Sem promessa médica: fala de conforto no braço. Sem voz de IA.']
RZD = ['Pôsteres reais do app, conversa fictícia (Dani & Cris), sem rosto nem voz de pessoa real.', 'Sem preço na arte nem na copy (o CTR dos RZ-18/19 com preço foi 0,3%).']
A = [
 dict(id='ADC-RK-02-A', br='sportdna', base='ADC-RK-02-v2', kind='img', title='RACKET · variação do RK-02 · gancho de número', titulo='183 raquetes medidas', term='numero', camp='rk_rk02_variacoes', d=RKD,
      copy='183 raquetes medidas. Uma é a sua. 🎾\nO RACKET DNA cruza o seu corpo, o seu braço e o seu jogo com as raquetes do catálogo. Veja a prévia grátis antes de pagar.'),
 dict(id='ADC-RK-02-B', br='sportdna', base='ADC-RK-02-v2', kind='img', title='RACKET · variação do RK-02 · gancho de dor', titulo='Confira a sua raquete, grátis', term='dor', camp='rk_rk02_variacoes', d=RKD,
      copy='Cotovelo dói depois do jogo? Confira a raquete. 🎾\nRigidez, peso e balanço pesam no braço. O RACKET DNA avalia o conforto da sua raquete, de graça.'),
 dict(id='ADC-RK-02-C', br='sportdna', base='ADC-RK-02-v2', kind='img', title='RACKET · variação do RK-02 · gancho de economia', titulo='Antes de comprar, faça o teste', term='economia', camp='rk_rk02_variacoes', d=RKD,
      copy='Antes de gastar R$ 1.500 numa raquete, faça o teste. 🎾\nO RACKET DNA compara 183 raquetes medidas com o seu jogo e mostra as que combinam com você. Prévia grátis.'),
 dict(id='ADC-RZ-03-A', br='retrozap', base='ADC-RZ-03-v2', kind='img', title='Casal · variação do RZ-03 · recibo do amor', titulo='O recibo do amor', term='recibo', camp='rz_casal_estatico', d=RZD,
      copy='O recibo do amor de vocês dois. 🧾💌\nQuem mandou mais "te amo", mais boa noite, quem puxou o papo: item por item, tirado da conversa de vocês.\nTeste o de vocês. Nada sai do seu celular.'),
 dict(id='ADC-RZ-03-B', br='retrozap', base='ADC-RZ-03-v2', kind='img', title='Casal · variação do RZ-03 · quem paga o jantar', titulo='Quem paga o jantar?', term='jantar', camp='rz_casal_estatico', d=RZD,
      copy='Quem paga o jantar? 🍝\nO recibo do amor responde, item por item, tirado da conversa de vocês dois.\nTeste o de vocês. Nada sai do seu celular.'),
 dict(id='ADC-RZ-03-C', br='retrozap', base='ADC-RZ-03-v2', kind='img', title='Casal · variação do RZ-03 · placar de vocês dois', titulo='O placar de vocês dois', term='placar', camp='rz_casal_estatico', d=RZD,
      copy='O placar de vocês dois. 💘\nMensagens, áudios, "te amo": um contra o outro, tirado da conversa do casal.\nTeste o de vocês. Nada sai do seu celular.'),
 dict(id='ADC-RK-07-BF', br='sportdna', base='ADC-RK-07-v3', kind='vid', title='RACKET · variação do RK-07 "Espera" · Black Friday (até 27/11)', titulo='Black Friday? Espera.', term='bf', camp='rk_blackfriday', d=RKD + ['Vídeo de banco Mixkit (47279, 45496, 876), os mesmos do RK-07. Música Mixkit 1076.'],
      copy='Vai comprar raquete na Black Friday? Espera. 🎾\nDesconto bom em raquete errada sai caro. O RACKET DNA compara 183 raquetes medidas e mostra as 3 do seu jogo. Prévia grátis.', notes='Rodar só até 27/11.'),
 dict(id='ADC-RK-07-PR', br='sportdna', base='ADC-RK-07-v3', kind='vid', title='RACKET · variação do RK-07 "Espera" · presente (dezembro)', titulo='Raquete de presente? Espera.', term='presente', camp='rk_natal', d=RKD + ['Vídeo de banco Mixkit (47279, 45496, 876), os mesmos do RK-07. Música Mixkit 1005.'],
      copy='Vai dar raquete de presente? Espera. 🎄🎾\nFaça o teste junto com quem vai ganhar: o RACKET DNA mostra as 3 raquetes que combinam com o jogo dele. Prévia grátis.', notes='Natal: só a partir de 01/12.'),
]
s = LIVE.read_text(); RX = r'(<script id="manifest" type="application/json">)(.*?)(</script>)'
m = re.search(RX, s, re.S); d = json.loads(m.group(2)); UP = []
RAW = 'https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/ads/em-aprovacao'
for a in reversed(A):
    v = a['id'] + '-v1'; dst = S / 'ads' / 'em-aprovacao' / a['br'] / v; dst.mkdir(parents=True, exist_ok=True)
    host = 'sportdna.com.br/racket/' if a['br'] == 'sportdna' else 'retrozap.com.br/'
    url = f"https://{host}?{'m=casal&' if a['br'] == 'retrozap' else ''}{U}&utm_campaign={a['camp']}&utm_term={a['term']}&utm_content={v}"
    cta = 'Na arte: "Teste o de vocês". Botão do anúncio: Saiba mais.' if a['br'] == 'retrozap' else 'Na arte: "Teste o seu agora". Botão do anúncio: Saiba mais.'
    if a['kind'] == 'img':
        shutil.copy(B / f'{v}_feed-1x1.png', dst / f'{v}_feed-1x1.png'); arq = f'- `{v}_feed-1x1.png`: estático 1:1 (formato principal).'
        nm = f'{v}-1x1.jpg'; Image.open(dst / f'{v}_feed-1x1.png').convert('RGB').save(MED / nm, quality=88); UP.append('media/' + nm)
        e = dict(fmt='adaptacao', media=[nm], cover=nm, previews=[nm], imgs=[dict(src=nm, label='Estático 1:1 (feed)', w='100%')], duration=None, hash=H5(dst / f'{v}_feed-1x1.png'),
                 formato='Estático 1:1 (formato principal). 4:5, 9:16 e 1,91:1 depois da aprovação.')
    else:
        shutil.copy(B / f'{v}.mp4', dst / f'{v}_reels-stories-9x16.mp4'); arq = f'- `{v}_reels-stories-9x16.mp4`: vídeo 9:16, 12 s, música de banco, sem voz.'
        nm = f'{v}.mp4'; subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(dst / f'{v}_reels-stories-9x16.mp4'), '-vf', 'scale=720:-2', '-c:v', 'libx264', '-crf', '24', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(MED / nm)], check=True); UP.append('media/' + nm)
        cp = f'{v}-capa.jpg'; subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '0.5', '-i', str(MED / nm), '-frames:v', '1', str(MED / cp)], check=True); UP.append('media/' + cp)
        e = dict(fmt='reel', media=[nm], cover=cp, duration=12.0, hash=H5(dst / f'{v}_reels-stories-9x16.mp4'), formato='Vídeo 9:16 · 12 s · música de banco. Outras dimensões depois da aprovação.')
    (dst / 'LEIA-ME.md').write_text(f"# {a['id']} · {a['title']}\n\nVersão: {v} · aguardando aprovação na Mesa · brief do Growth (19/11), variação do {a['base']}\n\n- **CTA:** {cta}\n- **URL final:** {url}\n"
                                    + (f"- **Atenção:** {a['notes']}\n" if a.get('notes') else '') + f"\n## Copy\n\n{a['copy']}\n\nTítulo: {a['titulo']}\n\n## Arquivos\n\n{arq}\n\nSem voz de IA: não precisa do rótulo de IA da Meta.\n\nNada foi enviado à conta de anúncios.\n")
    e.update(id=a['id'], brand='SPORT DNA' if a['br'] == 'sportdna' else 'Retrozap', lote='brief-1911', title=a['title'], version=v, v=1,
             objetivo='Vender a retrospectiva de casal.' if a['br'] == 'retrozap' else 'Vender o relatório RACKET DNA a partir da prévia grátis.',
             publico='Casais de 20 a 40 anos.' if a['br'] == 'retrozap' else 'Tenistas amadores de 25 a 55 anos.',
             hipotese=f"Brief do Growth (19/11): variação do {a['base']}, o que mais vende/clica, para testar o gancho.", copy=a['copy'], titulo=a['titulo'], cta=cta, url=url,
             direitos=a['d'], notes=a.get('notes', ''), producao='pronto para revisão', mudou=f"Peça nova: variação do {a['base']} (brief do Growth, 19/11).",
             arquivos=[dict(label='LEIA-ME', path=f"{RAW}/{a['br']}/{v}/LEIA-ME.md")])
    d['ads'] = [x for x in d['ads'] if x['id'] != a['id']]; d['ads'].insert(0, e)
d['adsLote'] = ['19/11 · Brief do Growth (variações dos que mais vendem). RK-02 estático (ROAS 3,5): A número (183 raquetes), B dor (cotovelo), C economia (R$ 1.500). '
                'RZ-03 casal SEM preço: A recibo do amor, B quem paga o jantar, C placar de vocês dois. RK-07 "Espera" (CTR 7,1%): BF (até 27/11) e presente (dezembro), só música.'] + d['adsLote']
d['rodada'] = max(d.get('rodada', 0), 18)
js = json.dumps(d, ensure_ascii=False).replace('</', '<\\/'); s = s[:m.start(2)] + js + s[m.end(2):]; (M / 'index.html').write_text(s)
(B / 'files.json').write_text(json.dumps({x: 'work/mesa/' + x for x in UP})); print(len(UP))
