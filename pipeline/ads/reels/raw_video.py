"""Frames do screencast (com tempo) → vídeo CFR 30 fps na velocidade real. Uso: python3 raw_video.py <pasta da captura>"""
import json, subprocess, sys
D = sys.argv[1]; c = json.load(open(f'{D}/capture.json')); fr = c['frames']
with open(f'{D}/list.txt', 'w') as f:
    for i, t in enumerate(fr):
        dur = (fr[i + 1] - t) if i + 1 < len(fr) else 2.0
        f.write(f"file 'frames/{i:05d}.jpg'\nduration {max(dur, 0.001):.4f}\n")
    f.write(f"file 'frames/{len(fr) - 1:05d}.jpg'\n")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{D}/list.txt', '-vf', 'fps=30,scale=1080:1920:flags=lanczos,format=yuv420p',
                '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', f'{D}/raw.mp4'], check=True)
print('ok')
