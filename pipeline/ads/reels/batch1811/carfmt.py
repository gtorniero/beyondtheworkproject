"""Carrosséis aprovados (ADC-RZ-15-v1, 5 cards; ADC-RK-10-v2, 7 cards): 4:5 e 9:16 do MESMO card 1:1, mais um vídeo vertical da mesma sequência.
Cada card 1:1 aprovado entra INTEIRO e sem escala (1080×1080, pixel por pixel); nada é redesenhado, cortado ou gerado por IA.
O espaço a mais do formato é só fundo: a última linha do card continua para fora e se funde, em poucos pixels, na cor do fundo
do próprio card (cor do canto). Quando o celular do print encosta na borda do card (RZ-15, cards 1–4), o card fica com essa borda
na base do quadro (4:5) ou na linha da zona de interface (9:16), e o fundo continua por baixo.
Uso: python3 carfmt.py <saída>"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[4]
AP = REPO / 'ads' / 'aprovados'
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
# id: (pasta, nº de cards, y do card no 4:5, y do card no 9:16, segundos por card no vídeo)
CAR = {'ADC-RZ-15-v1': ('retrozap', 5, 270, 500, 2.8),   # cards 1–4: celular sangra na base → card encostado embaixo
       'ADC-RK-10-v2': ('sportdna', 7, 135, 420, 3.4)}   # nada sangra → card centralizado; mais texto → mais tempo


def corner(a, top):
    rows = a[4:24] if top else a[-24:-4]
    return np.concatenate([rows[:, 4:44], rows[:, -44:-4]], 1).reshape(-1, 3).mean(0)


GP = 90  # grade do fundo dos cards (linhas de 2 px a cada 90 px, a partir do 0)


def grid_delta(a, top=True):
    """Se o card tem a grade de fundo, devolve o quanto a linha da grade clareia o fundo perto daquela borda (por coluna, RGB);
    senão None. Linha 0 (topo) e 990 (base) são linhas da grade; 4 e 994 são só fundo."""
    y = 0 if top else (a.shape[0] - 1) // GP * GP
    d = a[y] - a[y + 4]
    off = np.ones(a.shape[1], bool); off[(np.arange(a.shape[1]) % GP) < 2] = False
    return d if d[off].mean() > 4 and abs(float((a[GP] - a[GP + 4])[off].mean() - d[off].mean())) < 4 else None


def band(a, h, top, bleed=False):
    """h linhas de fundo, a partir da borda do card: começa no fundo da borda e vai, com curva suave, para a cor de base do fundo do card.
    Com grade, a grade continua no mesmo passo. Se o print do celular sangra nessa borda (bleed), ele se funde
    no fundo em poucos pixels, para não esticar o print."""
    if h <= 0: return np.zeros((0, a.shape[1], 3), np.float32)
    g = grid_delta(a, top)
    edge = (a[4] if top else a[-5]).astype(np.float32) if g is not None else (a[1] if top else a[-2]).astype(np.float32)
    if bleed: edge = (a[-6:-1] if not top else a[1:6]).astype(np.float32).mean(0)   # média das últimas linhas: sem riscos de compressão
    base = corner(a, True).astype(np.float32)      # cor de base do fundo do card (canto de cima, sem brilho nem print)
    fade = 48 if bleed else (150 if top else 240)
    d = np.arange(1, h + 1, dtype=np.float32)[:, None, None]          # distância até o card (1 = linha colada)
    t = np.clip(d / fade, 0, 1); t = t * t * (3 - 2 * t)
    b = edge[None] * (1 - t) + base[None, None] * t
    if g is not None:
        # linhas horizontais da grade: no card elas estão em y % 90 ∈ {0, 1}; fora dele, continuam no mesmo passo
        ys = (-d[:, 0, 0]) if top else (a.shape[0] - 1 + d[:, 0, 0])
        on = (np.mod(ys, GP) < 2)[:, None, None]
        b = b + on * g[None]
    return b[::-1] if top else b


def frame(card, H, y, bleed=False):
    a = np.asarray(card.convert('RGB'), np.float32)
    top, bot = band(a, y, True), band(a, H - y - a.shape[0], False, bleed)
    return Image.fromarray(np.clip(np.concatenate([top, a, bot]), 0, 255).astype(np.uint8))


def ff(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *a], check=True)


for v, (br, n, y45, y916, sec) in CAR.items():
    d = AP / br / v; o = OUT / v; o.mkdir(exist_ok=True)
    cards = [Image.open(d / f'{v}_carrossel-1x1-card{i}.png') for i in range(1, n + 1)]
    for i, c in enumerate(cards, 1):
        assert c.size == (1080, 1080), (v, i, c.size)
        bl = v == 'ADC-RZ-15-v1' and i <= 4          # print do celular encosta na base do card
        frame(c, 1350, y45, bl).save(o / f'{v}_carrossel-feed-4x5-card{i}.png')
        frame(c, 1920, y916, bl).save(o / f'{v}_carrossel-stories-9x16-card{i}.png')
    # anúncio de VÍDEO (separado do carrossel): os mesmos cards, na mesma ordem, com fusão curta entre eles; sem áudio
    # (o carrossel aprovado não tem trilha). 9:16 para Reels/Stories, 4:5 para Feed e 1:1 (o próprio card) para os demais.
    X = .35
    for src, name in ((lambda i: o / f'{v}_carrossel-stories-9x16-card{i}.png', 'video-sequencia-reels-stories-9x16'),
                      (lambda i: o / f'{v}_carrossel-feed-4x5-card{i}.png', 'video-sequencia-feed-4x5'),
                      (lambda i: d / f'{v}_carrossel-1x1-card{i}.png', 'video-sequencia-1x1')):
        ins = []
        for i in range(1, n + 1): ins += ['-loop', '1', '-t', f'{sec + X:.2f}', '-framerate', '30', '-i', str(src(i))]
        # offset do xfade = tempo na saída acumulada: cada card ocupa "sec" segundos (o último, sec + X)
        fc = []; last = '0:v'
        for i in range(1, n):
            lab = f'x{i}'; fc.append(f'[{last}][{i}:v]xfade=transition=fade:duration={X}:offset={i * sec:.3f}[{lab}]'); last = lab
        ff(*ins, '-filter_complex', ';'.join(fc) + f';[{last}]format=yuv420p[v]', '-map', '[v]', '-r', '30', '-c:v', 'libx264', '-crf', '18',
           '-preset', 'slow', '-movflags', '+faststart', str(o / f'{v}_{name}.mp4'))
    print('ok', v, flush=True)
