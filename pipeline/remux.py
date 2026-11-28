"""Troca só a trilha dos reels já renderizados (sem refazer os quadros). Uso: python3 remux.py IDs"""
import sys, json, subprocess, importlib
import common as C
for m in ('quiddo', 'retrozap', 'sportdna'): importlib.import_module(m)
for p in C.PIECES:
    if p['fmt'] != 'reel' or (sys.argv[1:] and p['id'] not in sys.argv[1:]): continue
    mp4 = C.OUT / 'media' / f"{p['id']}.mp4"; m4a = C.OUT / f"{p['id']}.m4a"; tmp = C.OUT / f"{p['id']}-tmp.mp4"
    C.trilha(C.PACKS / p['music'], p['total'], m4a)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(mp4), '-i', str(m4a), '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', '-movflags', '+faststart', str(tmp)], check=True)
    tmp.replace(mp4); m4a.unlink(); print(p['id'])
