"""Monta as versões novas com CTA maior (ADC-RZ-18-SP-v2, ADC-RZ-19-SP-v2) para aprovação, sem mexer nas v1 aprovadas.
- ads/em-aprovacao/retrozap/<ID>/: pacote completo por posicionamento, com os nomes finais (vídeo 9:16/4:5/1:1; estático 9:16/4:5/1:1/1,91:1)
  e LEIA-ME. Os três vídeos recebem a MESMA música da v1 aprovada (copiada do 9:16 da v1; durações conferidas).
- ads/mesa/: o que vai para a Mesa (motion 9:16 leve com som e o estático 1:1 em JPG).
Depois da aprovação na Mesa, a pasta passa para ads/aprovados/retrozap/ (e PROMPT, GUIA e INDEX são atualizados).
Uso: python3 packcta.py <out do adapt1811>"""
import shutil, subprocess, sys
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[4]
OUT = Path(sys.argv[1])
AP = REPO / 'ads' / 'aprovados' / 'retrozap'
EA = REPO / 'ads' / 'em-aprovacao' / 'retrozap'
MESA = REPO / 'ads' / 'mesa'
IDS = {'ADC-RZ-18-SP-v2': 'ADC-RZ-18-SP-v1', 'ADC-RZ-19-SP-v2': 'ADC-RZ-19-SP-v1'}


def ff(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *a], check=True)
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


for v, old in IDS.items():
    o = OUT / v; d = EA / v; d.mkdir(parents=True, exist_ok=True)
    a916 = AP / old / f'{old}_reels-stories-9x16.mp4'
    for fmt, name in (('story', 'reels-stories-9x16'), ('feed45', 'video-feed-4x5'), ('sq', 'video-feed-coluna-1x1')):
        m = o / f'{v}-motion-{fmt}.mp4'
        assert abs(dur(m) - dur(a916)) < 0.15, (v, fmt, dur(m), dur(a916))
        ff('-i', str(m), '-i', str(a916), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', str(d / f'{v}_{name}.mp4'))
    for fmt, name in (('story', 'stories-reels-9x16'), ('feed45', 'feed-4x5'), ('sq', 'feed-1x1'), ('land', 'busca-audience-1.91x1')):
        shutil.copy(o / f'{v}-{fmt}.png', d / f'{v}_{name}.png')
    # Mesa: motion 9:16 leve (720p, com a música) + estático 1:1
    ff('-i', str(d / f'{v}_reels-stories-9x16.mp4'), '-vf', 'scale=720:1280', '-c:v', 'libx264', '-crf', '26', '-preset', 'slow', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(MESA / f'{v}.mp4'))
    Image.open(o / f'{v}-sq.png').convert('RGB').save(MESA / f'{v}-1x1.jpg', quality=88)
    # LEIA-ME: o da v1, com versão, status, URL (utm_content) e a lista de arquivos da v2
    s = (AP / old / 'LEIA-ME.md').read_text().replace(old, v)
    s = s.replace('· aprovado na Mesa (rodada 16, 18/11/2026)', '· **EM APROVAÇÃO na Mesa** (rodada 17, 18/11/2026). Ainda não subir: até a aprovação, a versão em uso é a v1 (ads/aprovados).')
    s = s.replace('## Arquivos (todos do mesmo criativo aprovado)', '## O que mudou na v2\n\n'
                  f'Comentário do Gui na Mesa sobre a v1: {"“deixe o CTA bem maior”" if "18" in v else "“CTA MAIOR”"}. '
                  'Mesmo criativo da v1 (título, número, tela, texto, cores, música); só o botão "Teste o de vocês agora" ficou bem maior em todos os formatos '
                  '(cerca de 1,6× a fonte, botão mais alto e mais largo), no mesmo lugar. No 4:5, o visual da direita ficou um pouco menor para o botão não '
                  'cobrir nada; nada foi cortado.\n\n## Arquivos (todos do mesmo criativo)')
    s = s.replace('(o vídeo aprovado na Mesa)', '(o vídeo da Mesa)').replace('o estático aprovado na Mesa; ', 'o estático da Mesa; ')
    s = s.replace('O 9:16 e o 1:1 aprovados não foram alterados.', 'Os formatos da Mesa são o motion 9:16 e o estático 1:1.')
    s = s.replace('Áudio: só música de banco (Mixkit), a mesma faixa nos três vídeos.', 'Áudio: só música de banco (Mixkit), a mesma faixa da v1, nos três vídeos.')
    (d / 'LEIA-ME.md').write_text(s)
    print('ok', v, sorted(x.name for x in d.iterdir()), flush=True)
