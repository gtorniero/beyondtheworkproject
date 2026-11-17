import sys, asyncio
sys.argv=['x']; import kvx; K=kvx.K
async def go(ids, fmts):
    async with K.async_playwright() as p:
        b=await p.chromium.launch()
        await asyncio.gather(*[K.motion(b,v,f,kvx.HERE/'out'/v) for v in ids for f in fmts])
        await b.close()
import os
fm=os.environ.get('FMTS','story').split(',')
import os
ids=os.environ.get('IDS'); asyncio.run(go(ids.split(',') if ids else list(kvx.SPEC), fm))
