"""Tira o chiado do TTS direto do vídeo final: acha as rajadas na faixa só-voz e, nessas janelas,
corta os agudos da mixagem (passa-baixa empilhado) e silencia a faixa só-voz. Vídeo copiado sem recodificar."""
import subprocess, sys
from pathlib import Path
W = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(W)); import hiss
def windows(sovoz, minlvl=-10):
    h = [x for x in hiss.find(hiss.load(sovoz)) if x[2] > minlvl]; out = []
    for a, b, _ in h:
        a, b = a - .03, b + .04
        if out and a <= out[-1][1] + .05: out[-1][1] = max(out[-1][1], b)
        else: out.append([a, b])
    return [(round(a, 2), round(b, 2)) for a, b in out]
def apply(src, dst, win, mute=False):
    en = '+'.join(f'between(t,{a},{b})' for a, b in win)
    if mute: af = f"volume=0:enable='{en}'"
    else: af = ','.join([f"lowpass=f=2400:enable='{en}'"] * 4) + f",volume=1.6:enable='{en}'"
    tmp = Path(dst).with_suffix('.tmp.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(src), '-map', '0:v', '-map', '0:a', '-c:v', 'copy', '-af', af, '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(tmp)], check=True)
    tmp.replace(dst)
def has_audio(p):
    return bool(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout.strip())
