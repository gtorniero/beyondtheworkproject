"""Detecta e remove o chiado do TTS: rajada curta de ruído agudo (quase toda energia > 4 kHz), sem voz por perto.
Uso: python3 hiss.py scan a.wav ... | python3 hiss.py fix in.wav out.wav"""
import numpy as np, subprocess, sys, wave
SR = 24000; HOP = int(.01 * SR); N = 512
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768
def frames(v):
    fr = np.fft.rfftfreq(N, 1 / SR); out = []
    for i in range(0, len(v) - N, HOP):
        S = np.abs(np.fft.rfft(v[i:i + N] * np.hanning(N))) ** 2
        lo = S[(fr > 80) & (fr < 3500)].sum(); hi = S[fr > 4000].sum(); tot = S.sum()
        out.append((10 * np.log10(tot + 1e-12), 10 * np.log10(hi + 1e-12) - 10 * np.log10(lo + 1e-12)))
    return np.array(out)
def find(v):
    F = frames(v); db, r = F[:, 0], F[:, 1]
    ref = np.percentile(db[db > db.max() - 60], 90)
    loud = db > ref - 35          # há som
    voiced = loud & (r < -12)     # fala com corpo (vogais)
    noisy = loud & (r > -10)      # som dominado por agudo
    hits = []; i = 0
    while i < len(F):
        if noisy[i]:
            j = i
            while j + 1 < len(F) and (noisy[j + 1] or (loud[j + 1] and not voiced[j + 1])): j += 1
            a, b = i, j
            pre = voiced[max(0, a - 6):a].any(); post = voiced[b + 1:b + 7].any()
            if not pre and not post and 3 <= b - a + 1 <= 45:
                hits.append((round(a * HOP / SR, 2), round((b + 1) * HOP / SR + N / SR, 2), round(float(db[a:b + 1].max() - ref), 1)))
            i = j + 1
        else: i += 1
    return hits
def fix(src, dst):
    v = load(src).copy(); hits = find(v)
    for a, b, _ in hits:
        ia, ib = int((a - .01) * SR), int((b + .02) * SR); f = int(.005 * SR)
        g = np.zeros(ib - ia); g[:f] = np.linspace(1, 0, f); g[-f:] = np.linspace(0, 1, f)
        v[ia:ib] *= g
    with wave.open(str(dst), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype('<i2').tobytes())
    return hits
if __name__ == '__main__':
    if sys.argv[1] == 'scan':
        for p in sys.argv[2:]: print(p, find(load(p)))
    else: print(fix(sys.argv[2], sys.argv[3]))
