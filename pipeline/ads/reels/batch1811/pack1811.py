"""Fecha o pacote por posicionamento dos ADs aprovados do lote 18/11 (rodada 16), sem mexer nos arquivos aprovados.
KV (motor kvx/kvrz/kvab/kvdna2/kvrun, via adapt1811.py): vídeo 4:5 e 1:1 renderizados no layout do próprio motor, com o áudio copiado
do 9:16 aprovado; estáticos 4:5, 9:16 e 1,91:1. Viral (rzviral, só 9:16): 4:5 e 1:1 = o 9:16 inteiro centralizado, laterais com o fundo do
próprio vídeo (borda repetida; nos pôsteres em tela cheia, a cor de fundo da marca). Também reescreve o LEIA-ME de cada pasta.
Uso: python3 pack1811.py <out do adapt1811> <pasta viral> <IDs...>"""
import re, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
AP = REPO / 'ads' / 'aprovados'
OUT, VIR, IDS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
VIRAL = {f'ADC-RZ-{n}-v1' for n in range(27, 33)}


def run(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *a], check=True)


def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


def leiame(v, d, viral, so_est=False):
    f = d / 'LEIA-ME.md'; s = f.read_text()
    s = re.sub(r'aguardando aprovação na Mesa( \(formato principal\))?', 'aprovado na Mesa (rodada 16, 18/11/2026)', s)
    a = s.index('## Arquivos'); b = s.index('Nada foi enviado')
    vid = [f'- `{v}_reels-stories-9x16.mp4`: Stories e Reels (o vídeo aprovado na Mesa).',
           f'- `{v}_video-feed-4x5.mp4`: Feed.',
           f'- `{v}_video-feed-coluna-1x1.mp4`: os demais posicionamentos que aceitam vídeo (coluna da direita, Marketplace, Explorar, busca).']
    est = [f'- `{v}_stories-reels-9x16.png`: Stories e Reels.', f'- `{v}_feed-4x5.png`: Feed.',
           f'- `{v}_feed-1x1.png`: ' + ('coluna da direita, Marketplace e os demais.' if viral else 'o estático aprovado na Mesa; coluna da direita, Marketplace e os demais.')]
    if not viral: est.append(f'- `{v}_busca-audience-1.91x1.png`: busca e Audience Network.')
    how = ('4:5 e 1:1 são o vídeo 9:16 inteiro, centralizado, com o fundo do próprio vídeo nas laterais: nada cortado, nenhum texto mexido. '
           'Não há 1,91:1: o vertical ficaria pequeno demais para ler; nesses posicionamentos a Meta usa o 1:1.' if viral else
           'Mesmo criativo aprovado, montado no layout de cada formato pelo mesmo motor (mesmos textos, números, telas e CTA; nada cortado). '
           'O 9:16 e o 1:1 aprovados não foram alterados.')
    blk = ('## Arquivos (todos do mesmo criativo aprovado)\n\n'
           + ('Este AD é só estático (o aprovado na Mesa não tem vídeo): suba como anúncio de imagem.\n\n' if so_est else
              '**Anúncio de VÍDEO** (um anúncio só de vídeo, em todos os posicionamentos):\n' + '\n'.join(vid) + '\n\n')
           + '**Anúncio ESTÁTICO** (outro anúncio, só de imagem):\n' + '\n'.join(est) + '\n\n'
           'Nunca misture PNG e MP4 no mesmo anúncio.\n\n' + how + '\n\n'
           + ('Sem áudio (estático): não precisa do rótulo de IA da Meta.\n\n' if so_est else
              'Áudio: só música de banco (Mixkit), a mesma faixa nos três vídeos. Sem voz: não precisa do rótulo de IA da Meta.\n\n'))
    f.write_text(s[:a] + blk + s[b:])


for v in IDS:
    d = next(AP.glob(f'*/{v}'))
    viral = v in VIRAL
    a916 = d / f'{v}_reels-stories-9x16.mp4'
    if viral:
        for n in ('video-feed-4x5.mp4', 'video-feed-coluna-1x1.mp4', 'feed-4x5.png', 'stories-reels-9x16.png'):
            shutil.copy(VIR / f'{v}_{n}', d / f'{v}_{n}')
        shutil.copy(VIR / f'{v}_feed-coluna-1x1.png', d / f'{v}_feed-1x1.png')
    else:
        o = OUT / v; so_est = not a916.exists()
        for fmt, name in ([] if so_est else (('feed45', 'video-feed-4x5'), ('sq', 'video-feed-coluna-1x1'))):
            m = o / f'{v}-motion-{fmt}.mp4'
            assert abs(dur(m) - dur(a916)) < 0.15, (v, fmt, dur(m), dur(a916))
            run('-i', str(m), '-i', str(a916), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', str(d / f'{v}_{name}.mp4'))
        for fmt, name in (('feed45', 'feed-4x5'), ('story', 'stories-reels-9x16'), ('land', 'busca-audience-1.91x1')):
            shutil.copy(o / f'{v}-{fmt}.png', d / f'{v}_{name}.png')
    leiame(v, d, viral, (not viral) and not a916.exists())
    print('ok', v, len(list(d.iterdir())), flush=True)
