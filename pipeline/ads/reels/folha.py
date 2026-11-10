"""Folha de contato de um vídeo: um quadro a cada N segundos. Uso: python3 folha.py <video> <saida.jpg> [passo]"""
import subprocess, sys, json
from PIL import Image
v, out = sys.argv[1], sys.argv[2]; step = float(sys.argv[3]) if len(sys.argv) > 3 else 2
d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
ims = []; t = 0.5
while t < d:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', v, '-frames:v', '1', '-vf', 'scale=270:480', '/tmp/_f.png'], check=True)
    ims.append(Image.open('/tmp/_f.png').copy()); t += step
c = 8; r = (len(ims) + c - 1) // c; sh = Image.new('RGB', (c * 275, r * 485), '#888')
for i, im in enumerate(ims): sh.paste(im, ((i % c) * 275, (i // c) * 485))
sh.save(out, quality=88); print(len(ims), 'quadros', round(d, 2), 's')
