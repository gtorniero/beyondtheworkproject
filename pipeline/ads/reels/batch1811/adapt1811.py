"""Adaptações dos ADs aprovados do lote 18/11 (mesmo criativo, motor kv_dna/kvx): estáticos sq/story/feed45/land e motion feed45/sq/story.
Uso: PYTHONPATH=../batch1711 python3 adapt1811.py <static|motion> <fmts> <IDs...>   → batch1711/out/<ID>/<ID>-<fmt>.png | <ID>-motion-<fmt>.mp4
ADC-RZ-18-v2 não estava no repositório: reconstruído do v1 com o título aprovado ("Retrospectiva de casal do seu zap.")."""
import sys, asyncio
import kvx
K = kvx.K
kvx.SPEC['ADC-RZ-18-v2'] = dict(kvx.SPEC['ADC-RZ-18-v1'], title='Retrospectiva de casal do seu *zap.*')
import kvab, kvrun, kvrz  # noqa: registram as variantes
# 4:5: o pôster de trás encostava no fim do título; desce 60 px (o resto do layout não muda)
kvrz.P['feed45'] = (410, 615, 430)

# 1,91:1: o layout genérico só mostrava o 1º número; o 2º (o preço, nas versões com preço) sumia.
# Com 2 números, os dois entram lado a lado (como no 16:9 do mesmo motor).
_orig = kvrz._body
def _land(s, fmt):
    if fmt == 'land' and 'nums' in s and len(s['nums']) > 1 and 'steps' not in s:
        ph = s['ph']; b = K.phone(ph['src'], 236, 920, 52, kvx.ROT, ph['zoom'], .5, ph['fy'])
        for i, n in enumerate(s['nums'][:2]): b += K.num(n[0], n[1], 40 + i * 370, 250, 330, 96, 19)
        return b
    return _orig(s, fmt)
kvrz._body = _land
mode, fmts, ids = sys.argv[1], sys.argv[2].split(','), sys.argv[3:]
out = kvx.HERE / 'out'
async def go():
    async with K.async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for v in ids: (out / v).mkdir(parents=True, exist_ok=True)
        if mode == 'static':
            for v in ids:
                for f in fmts:
                    W, H = K.FMT[f]; await K.shot(pg, K.page(v, f), out / v / f'{v}-{f}.png', W, H)
                print('ok', v, flush=True)
        else:
            jobs = [K.motion(b, v, f, out / v) for v in ids for f in fmts]
            for i in range(0, len(jobs), 6): await asyncio.gather(*jobs[i:i + 6]); print('motion', i + 6, '/', len(jobs), flush=True)
        await b.close()
asyncio.run(go())
