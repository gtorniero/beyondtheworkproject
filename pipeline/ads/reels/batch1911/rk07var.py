"""Brief Growth 19/11 · RK-07-v3 ("Vai comprar raquete? Espera.", CTR 7,1%): 2 variações com o "Espera" no quadro 0. Só música de banco (sem voz)."""
import sys, subprocess
from pathlib import Path
W = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(W))
import sport, render4
from sport import mk, hook, an
MK = W.parent / 'mk'; OUT = W / 'b1911'
def s183(): return f'<div class="abs" style="left:70px;top:330px"><div class="big" style="font-size:300px;{an("pop",0,.4)}">183</div><div class="t" style="font-size:96px;margin-top:10px"><span class="cx">raquetes medidas,</span><br><span class="cx">uma a uma.</span></div></div>'
V = {
 'ADC-RK-07-BF-v1': (mk('rk', [(0, 3, hook([('Vai comprar raquete', 0), ('na Black Friday?', 0), ('Espera.', 1)])), (3, 6, s183()),
                       (6, 9.2, f'<div class="abs" style="left:70px;right:70px;top:330px"><div class="t" style="font-size:96px"><span class="cx">Desconto bom em</span><br><span class="cx">raquete errada</span><br><span class="cx cxa" style="{an("pop",.5,.4)}">sai caro.</span></div></div>')],
                      {0: ('47279', 0.5, 600, 0), 1: ('45496', 1, 500, 0), 2: ('876', 1, 650, 0)}, '', 12, 9.2, ('Antes de comprar,', 'teste o seu agora.', 'PRÉVIA GRÁTIS')), ('1076', 10.0)),
 'ADC-RK-07-PR-v1': (mk('rk', [(0, 3, hook([('Vai dar raquete', 0), ('de presente?', 0), ('Espera.', 1)])), (3, 6, s183()),
                       (6, 9.2, f'<div class="abs" style="left:70px;right:70px;top:330px"><div class="t" style="font-size:96px"><span class="cx">As 3 que combinam</span><br><span class="cx cxa" style="{an("pop",.5,.4)}">com o jogo dele.</span></div></div>')],
                      {0: ('47279', 0.5, 600, 0), 1: ('45496', 1, 500, 0), 2: ('876', 1, 650, 0)}, '', 12, 9.2, ('Antes de presentear,', 'faça o teste junto.', 'PRÉVIA GRÁTIS')), ('1005', 12.0)),
}
for key, (d, (tid, ss)) in V.items():
    T = d['total']; html = render4.base.page(d['css'], d['bg'], d['scenes'], T, d.get('persist', ''))
    hp = OUT / f'{key}.html'; hp.write_text(html); fd = OUT / f'fr-{key}'; subprocess.run(['rm', '-rf', str(fd)]); fd.mkdir()
    subprocess.run(['node', str(W / 'cap.js'), str(hp), str(fd), str(T), '30'], check=True)
    bg = OUT / f'{key}-bg.mp4'; render4.bgtrack(d, bg, key)
    out = OUT / f'{key}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(bg), '-framerate', '30', '-i', str(fd / '%04d.png'), '-ss', str(ss), '-i', str(MK / f'{tid}.mp3'),
      '-filter_complex', f'[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v];[2:a]atrim=0:{T},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st={T-1.2}:d=1.2,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a]',
      '-map', '[v]', '-map', '[a]', '-t', str(T), '-c:v', 'libx264', '-crf', '18', '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(out)], check=True)
    subprocess.run(['rm', '-rf', str(fd)]); print(key, flush=True)
