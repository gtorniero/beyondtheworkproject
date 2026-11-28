"""Prévia em lote (S05): estáticos (todas as páginas) e reels (frames + capa) numa folha por peça. Uso: python3 prev_all.py IDs..."""
import asyncio, sys, importlib
from PIL import Image
from playwright.async_api import async_playwright
import common as C
for m in ('quiddo', 'retrozap', 'sportdna'):
    try: importlib.import_module(m)
    except ModuleNotFoundError: pass
async def main(ids):
    d = C.OUT / '_prev'; d.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(); pg = await br.new_page()
        for p in [x for x in C.PIECES if not ids or x['id'] in ids]:
            hp = d / f"{p['id']}.html"; hp.write_text(p['html']); imgs = []
            await pg.set_viewport_size({'width': p.get('w', 1080), 'height': p.get('h', 1920)})
            if p['fmt'] == 'reel':
                await pg.goto(hp.as_uri() + '?render=1'); await pg.evaluate('document.fonts.ready')
                el = await pg.query_selector('.page'); T = p['total']
                for t in [x for x in (0.6, 1.8, 3.6, 4.9, 6.2, 7.4, 8.8, 10.0, 11.4, 12.6, 14.2) if x < T]:
                    await pg.evaluate(f'window.seek({t})'); f = d / f"{p['id']}-{t}.png"; await el.screenshot(path=str(f)); imgs.append(f)
                ch = d / f"{p['id']}-capa.html"; ch.write_text(p['cover']); await pg.goto(ch.as_uri()); await pg.evaluate('document.fonts.ready')
                f = d / f"{p['id']}-capa.png"; await (await pg.query_selector('.page')).screenshot(path=str(f)); imgs.append(f)
            else:
                await pg.goto(hp.as_uri()); await pg.evaluate('document.fonts.ready')
                for i, el in enumerate(await pg.query_selector_all('.page')):
                    f = d / f"{p['id']}-{i}.png"; await el.screenshot(path=str(f)); imgs.append(f)
            ims = [Image.open(f).convert('RGB') for f in imgs]
            sc = .25; w = int(1080 * sc); h = max(int(i.height * sc) for i in ims); cols = min(len(ims), 6); rows = (len(ims) + cols - 1) // cols
            sh = Image.new('RGB', (cols * (w + 8), rows * (h + 8)), '#555')
            for i, im in enumerate(ims):
                im = im.resize((w, int(im.height * sc))); sh.paste(im, ((i % cols) * (w + 8), (i // cols) * (h + 8)))
                if p['fmt'] == 'reel' and i < len(ims) - 1:  # guias da área segura
                    from PIL import ImageDraw
                    dr = ImageDraw.Draw(sh); x0, y0 = (i % cols) * (w + 8), (i // cols) * (h + 8)
                    dr.line((x0, y0 + 250 * sc, x0 + w, y0 + 250 * sc), fill='red'); dr.line((x0, y0 + 1570 * sc, x0 + w, y0 + 1570 * sc), fill='red')
            out = d / f"{p['id']}-sheet.jpg"; sh.save(out, quality=82); print(out, flush=True)
        await br.close()
asyncio.run(main(sys.argv[1:]))
