"""Remapeia a captura do qd_cap3 para o tempo real do produto: os trechos gravados em câmera lenta (marks['lento'], fator K) são comprimidos K×.
Gera <saida>/cel.mp4 (30 fps) e <saida>/marcas_rt.json (marcas no tempo novo) e mede fps reais por trecho.
Uso: python3 qd_remap.py <saida da captura>"""
import json, subprocess, sys
from pathlib import Path
D = Path(sys.argv[1]); m = json.loads((D / 'marcas.json').read_text()); K = m['K']
L = m['lento']; W = []
for i, x in enumerate(L):
    a, b = x[0], x[1]; k = x[2] if len(x) > 2 else K
    if b is None: b = L[i + 1][0] if i + 1 < len(L) else m['fim']
    if W and a < W[-1][1]: a = W[-1][1]
    W.append((a, b, k))
def rt(t):
    o = t
    for a, b, k in W:
        if t > a: o -= (min(t, b) - a) * (1 - 1 / k)
    return o
ts = [rt(t) for t in m['frames']['cel']]; fim = rt(m['fim'])
with open(D / 'cel_rt.txt', 'w') as f:
    f.write(f"file 'cel/00000.jpg'\nduration {max(ts[0], .001):.4f}\n")
    for i, t in enumerate(ts):
        d = (ts[i + 1] if i + 1 < len(ts) else fim) - t
        f.write(f"file 'cel/{i:05d}.jpg'\nduration {max(d, .001):.4f}\n")
    f.write(f"file 'cel/{len(ts) - 1:05d}.jpg'\n")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(D / 'cel_rt.txt'), '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', str(D / 'cel.mp4')], check=True)
mk = {k: round(rt(v), 3) for k, v in m.items() if isinstance(v, (int, float)) and k != 'K'}
(D / 'marcas_rt.json').write_text(json.dumps(mk, indent=1))
import collections
for a, b, k in W:
    n = sum(1 for t in m['frames']['cel'] if a <= t <= b); c = collections.Counter(int((t - a) / k) for t in m['frames']['cel'] if a <= t <= b)
    print(f'trecho lento {rt(a):6.1f}-{rt(b):6.1f}s K={k}: média {n / ((b - a) / k):5.1f} quadros/s reais; por segundo: {[c.get(i, 0) for i in range(int((b - a) / k) + 1)]}')
n = sum(1 for t in m['frames']['cel'] if not any(a <= t <= b for a, b, _ in W)); tot = sum(b - a for a, b, _ in W)
print(f'fora dos trechos lentos: {n / (m["fim"] - tot):.1f} quadros/s'); print(json.dumps(mk))
