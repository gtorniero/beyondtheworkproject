"""Pré-visualização rápida: estáticos (todas as páginas) ou frames de reels numa folha de contato."""
import asyncio, sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright
import common as C
import importlib
for m in ('quiddo','retrozap','sportdna'):
    try: importlib.import_module(m)
    except ModuleNotFoundError: pass

async def main(pid, times):
    p = next(x for x in C.PIECES if x['id'] == pid)
    d = C.OUT / '_prev'; d.mkdir(parents=True, exist_ok=True)
    hp = d / f'{pid}.html'; hp.write_text(p['html'])
    imgs = []
    async with async_playwright() as pw:
        br = await pw.chromium.launch(); pg = await br.new_page()
        await pg.set_viewport_size({'width': p.get('w', 1080), 'height': p.get('h', 1920)})
        if p['fmt'] == 'reel':
            await pg.goto(hp.as_uri() + '?render=1'); await pg.evaluate('document.fonts.ready')
            el = await pg.query_selector('.page')
            for t in times:
                await pg.evaluate(f'window.seek({t})'); f = d / f'{pid}-{t}.png'
                await el.screenshot(path=str(f)); imgs.append(f)
            if p.get('cover'):
                ch = d / f'{pid}-capa.html'; ch.write_text(p['cover']); await pg.goto(ch.as_uri()); await pg.evaluate('document.fonts.ready')
                f = d / f'{pid}-capa.png'; await (await pg.query_selector('.page')).screenshot(path=str(f)); imgs.append(f)
        else:
            await pg.goto(hp.as_uri()); await pg.evaluate('document.fonts.ready')
            for i, el in enumerate(await pg.query_selector_all('.page')):
                f = d / f'{pid}-{i}.png'; await el.screenshot(path=str(f)); imgs.append(f)
        await br.close()
    ims = [Image.open(f) for f in imgs]
    sc = 0.3; w = int(ims[0].width * sc); h = max(int(i.height * sc) for i in ims)
    cols = min(len(ims), 4); rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (w + 10), rows * (h + 10)), '#444')
    for i, im in enumerate(ims):
        im = im.convert('RGB').resize((w, int(im.height * sc)))
        sheet.paste(im, ((i % cols) * (w + 10), (i // cols) * (h + 10)))
    out = d / f'{pid}-sheet.jpg'; sheet.save(out, quality=85); print(out)

asyncio.run(main(sys.argv[1], [float(x) for x in sys.argv[2:]]))
