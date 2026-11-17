import json, subprocess, sys
from pathlib import Path
D = Path(sys.argv[1]); m = json.loads((D / 'marcas.json').read_text()); ts = m['frames']['cel']; t_end = m['fim']
with open(D / 'cel.txt', 'w') as f:
    f.write(f"file 'cel/00000.jpg'\nduration {max(ts[0], 0.001):.4f}\n")
    for i, t in enumerate(ts):
        d = (ts[i + 1] if i + 1 < len(ts) else t_end) - t
        f.write(f"file 'cel/{i:05d}.jpg'\nduration {max(d, 0.001):.4f}\n")
    f.write(f"file 'cel/{len(ts) - 1:05d}.jpg'\n")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(D / 'cel.txt'), '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', str(D / 'cel.mp4')], check=True)
