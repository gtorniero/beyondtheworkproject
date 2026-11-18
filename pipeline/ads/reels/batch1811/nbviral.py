"""Fecha os 6 virais do Retrozap (RZ-27 a RZ-32): música, pasta no GitHub e entrada na Mesa (motion 9:16; estáticos depois da aprovação)."""
import json, re, hashlib, subprocess
from pathlib import Path
from PIL import Image
from nb18meta import RZP, U
N = Path(__file__).resolve().parent; W = N.parent; M = W / 'mesa'; S = W.parent / 'social'; MK = W.parent / 'mk'; OUT = N / 'out'
def run(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *map(str, a)], check=True)
def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)]))
H5 = lambda p: hashlib.md5(Path(p).read_bytes()).hexdigest()[:10]
LOOK = {'A': 'A · Conversa: o chat do grupo estoura na tela, o contador dispara e o pôster entra.',
        'B': 'B · Stories de pôsteres: os pôsteres reais do app em tela cheia, um por vez, com barra de stories.',
        'C': 'C · Placar ao vivo: cara de transmissão esportiva, grupo contra o Brasil / um contra o outro.'}
G = dict(publico='Adultos de 18 a 45 anos com grupos ativos no WhatsApp (amigos, família, trabalho).', objetivo='Gerar retrospectivas de grupo (1º grupo grátis) e levar ao Premium.',
         cta='Na arte: "Teste o seu grupo." + botão "Teste agora". Botão do anúncio: Saiba mais.', camp='rz_grupo_viral')
C = dict(publico='Casais de 20 a 40 anos (relacionamento, presentes, Natal).', objetivo='Vender a retrospectiva de casal.',
         cta='Na arte: "Teste o de vocês." + botão "Teste agora". Botão do anúncio: Saiba mais.', camp='rz_casal_viral')
ADS = [
 dict(id='ADC-RZ-27', look='A', b=G, track=('859', 30.0), title='Grupo · VIRAL A (conversa): "Abrimos o grupo. Socorro."',
      copy='Abrimos o grupo. Socorro. 😳\n10 mil mensagens, um fantasma e quem manda áudio de 4 minutos. A retrospectiva conta tudo e cada um ganha o seu pôster.\nTeste o seu grupo: o 1º é grátis. Nada sai do seu celular.', titulo='Teste o seu grupo'),
 dict(id='ADC-RZ-28', look='A', b=C, track=('1005', 20.0), title='Casal · VIRAL A (conversa): "Abrimos a conversa do casal."',
      copy='Abrimos a conversa do casal. 💌\nQuem manda mais "te amo", quem pede desculpa, quem dá boa noite: sai até o recibo do amor.\nTeste o de vocês. Nada sai do seu celular.', titulo='Teste o de vocês'),
 dict(id='ADC-RZ-29', look='B', b=G, track=('1076', 20.0), title='Grupo · VIRAL B (stories de pôsteres)',
      copy='Quem sumiu do grupo? Qual é a gíria oficial? 👻📻\nO 2026 do seu grupo vira pôster: procura-se, rádio, plantão e o ranking contra o Brasil.\nTeste o seu grupo: o 1º é grátis.', titulo='Teste o seu grupo'),
 dict(id='ADC-RZ-30', look='B', b=C, track=('801', 25.0), title='Casal · VIRAL B (stories de pôsteres)',
      copy='O mapa astral de vocês, o recibo do amor e o boletim do casal. ✨🧾\nTudo tirado da conversa de vocês dois, pronto pra postar.\nTeste o de vocês. Nada sai do seu celular.', titulo='Teste o de vocês'),
 dict(id='ADC-RZ-31', look='C', b=G, track=('5', 20.0), title='Grupo · VIRAL C (placar ao vivo): seu grupo contra o Brasil',
      copy='Seu grupo contra o Brasil. 🇧🇷\nRisada, madrugada, figurinhas: em que o seu grupo fica no Top do Brasil? Só os números saem do celular, sem nomes nem textos.\nTeste o seu grupo: o 1º é grátis.', titulo='Seu grupo contra o Brasil'),
 dict(id='ADC-RZ-32', look='C', b=C, track=('1063', 30.0), title='Casal · VIRAL C (placar ao vivo): quem ama mais?',
      copy='Quem ama mais? 💘\nMensagens, "te amo", boa noite, quem puxa o papo: o placar de vocês dois, um contra o outro.\nTeste o de vocês. Nada sai do seu celular.', titulo='Quem ama mais?'),
]
s = (M / 'index.html').read_text(); m = re.search(r'(<script id="manifest" type="application/json">)(.*?)(</script>)', s, re.S); d = json.loads(m.group(2)); UP = []
RAW = 'https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/ads/aprovados'
for a in reversed(ADS):
    v = a['id'] + '-v1'; o = OUT / v; b = a['b']; dst = S / 'ads' / 'aprovados' / 'retrozap' / v; dst.mkdir(parents=True, exist_ok=True)
    mot = o / f'{v}-motion-story.mp4'; T = dur(mot); tid, ss = a['track']
    run('-i', mot, '-ss', ss, '-i', MK / f'{tid}.mp3', '-filter_complex', f'[1:a]atrim=0:{T},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st={T-1.2}:d=1.2,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a]',
        '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', T, '-movflags', '+faststart', dst / f'{v}_reels-stories-9x16.mp4')
    Image.open(o / f'{v}-hook.png').convert('RGB').save(dst / f'{v}_capa-9x16.jpg', quality=90)
    url = f'https://retrozap.com.br/?{"m=casal&" if b is C else ""}{U}&utm_campaign={b["camp"]}&utm_content={v}'
    (dst / 'LEIA-ME.md').write_text(f"# {a['id']} · {a['title']}\n\nVersão: {v} · Retrozap · aguardando aprovação na Mesa\n\nLook & feel {LOOK[a['look']]}\n\n- **Objetivo:** {b['objetivo']}\n- **Público:** {b['publico']}\n- **CTA:** {b['cta']}\n- **URL final:** {url}\n\n## Copy\n{a['copy']}\n\nTítulo: {a['titulo']}\n\n## Arquivos\n- `{v}_reels-stories-9x16.mp4`: 12 s, música de banco (Mixkit), sem voz.\n- `{v}_capa-9x16.jpg`\n\nDepois da aprovação: 4:5, 1:1, 16:9, estáticos e sem áudio.\n\nNada foi enviado à conta de anúncios.\n")
    run('-i', dst / f'{v}_reels-stories-9x16.mp4', '-vf', 'scale=720:-2', '-c:v', 'libx264', '-crf', '24', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', M / 'media' / f'{v}.mp4'); UP.append(f'media/{v}.mp4')
    Image.open(o / f'{v}-hook.png').convert('RGB').resize((720, 1280)).save(M / 'media' / f'{v}-capa.jpg', quality=86); UP.append(f'media/{v}-capa.jpg')
    e = dict(id=a['id'], brand='Retrozap', fmt='reel', lote='viral-1811', title=a['title'], version=v, v=1, hash=H5(dst / f'{v}_reels-stories-9x16.mp4'), media=[f'{v}.mp4'], cover=f'{v}-capa.jpg',
             duration=round(T, 1), formato='Motion 9:16 · 12 s · música de banco. Outras dimensões depois da aprovação.', objetivo=b['objetivo'], publico=b['publico'],
             hipotese='Pedido do Gui (18/11): mais imersivo, diferente e viral, terminando em "Teste o seu grupo". Teste de 3 look & feel; este é o ' + LOOK[a['look']],
             copy=a['copy'], titulo=a['titulo'], cta=b['cta'], url=url, direitos=RZP, notes='Teste A/B/C de look & feel: compare A, B e C da mesma marca.', producao='pronto para revisão',
             mudou='Peça nova: teste de 3 look & feel do Retrozap (18/11).', arquivos=[dict(label='LEIA-ME', path=f'{RAW}/retrozap/{v}/LEIA-ME.md')])
    d['ads'] = [x for x in d['ads'] if x['id'] != a['id']]; d['ads'].insert(0, e)
d['adsLote'] = [('18/11 · Retrozap VIRAL, teste de 3 look & feel (seu pedido), grupo e casal, todos terminando em "Teste o seu grupo / Teste o de vocês": '
                 'A · Conversa (RZ-27 grupo, RZ-28 casal): o chat estoura, contador dispara, pôster entra. B · Stories de pôsteres (RZ-29, RZ-30): os pôsteres reais em tela cheia. '
                 'C · Placar ao vivo (RZ-31 grupo contra o Brasil, RZ-32 quem ama mais?). Aprove os looks que gostar; depois faço mais no look vencedor.')] + d['adsLote']
js = json.dumps(d, ensure_ascii=False).replace('</', '<\\/'); s = s[:m.start(2)] + js + s[m.end(2):]; (M / 'index.html').write_text(s)
(N / 'upv.json').write_text(json.dumps(UP)); print('UP', len(UP))
