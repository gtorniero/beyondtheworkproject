"""Renderiza as peças registradas: editável HTML, PNG/JPG e MP4 (H.264, 30 fps)."""
import asyncio, hashlib, json, shutil, subprocess, sys, time
from pathlib import Path
from playwright.async_api import async_playwright
import common as C

FPS = 30

async def render_static(page, p, html_path, media_dir):
    await page.set_viewport_size({'width': p['w'], 'height': p['h']})
    await page.goto(html_path.as_uri())
    await page.evaluate('document.fonts.ready')
    els = await page.query_selector_all('.page')
    files = []
    for i, el in enumerate(els, 1):
        name = f"{p['id']}-{i}.png" if len(els) > 1 else f"{p['id']}.png"
        await el.screenshot(path=str(media_dir / name))
        files.append(name)
    return files

async def render_reel(page, p, html_path, media_dir, tmp):
    await page.set_viewport_size({'width': 1080, 'height': 1920})
    await page.goto(html_path.as_uri() + '?render=1')
    await page.evaluate('document.fonts.ready')
    fr = tmp / p['id']
    if fr.exists(): shutil.rmtree(fr)
    fr.mkdir(parents=True)
    n = int(round(p['total'] * FPS))
    for i in range(n):
        await page.evaluate(f'window.seek({i / FPS:.5f})')
        await page.screenshot(path=str(fr / f'{i:05d}.jpg'), type='jpeg', quality=92, clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1920})
    out = media_dir / f"{p['id']}.mp4"
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%05d.jpg'),
           '-f', 'lavfi', '-t', f"{p['total']}", '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
           '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium',
           '-r', str(FPS), '-c:a', 'aac', '-b:a', '64k', '-shortest', '-movflags', '+faststart', str(out)]
    subprocess.run(cmd, check=True)
    # pôster para a ferramenta (frame de meio)
    shutil.copy(fr / f'{min(n - 1, int(n * p.get("poster", .55))):05d}.jpg', media_dir / f"{p['id']}-poster.jpg")
    shutil.rmtree(fr)
    files = [f"{p['id']}.mp4"]
    # capa
    if p.get('cover'):
        ch = html_path.with_name(p['id'] + '-capa.html')
        ch.write_text(p['cover'])
        await page.set_viewport_size({'width': 1080, 'height': 1920})
        await page.goto(ch.as_uri())
        await page.evaluate('document.fonts.ready')
        el = await page.query_selector('.page')
        await el.screenshot(path=str(media_dir / f"{p['id']}-capa.png"))
        files.append(f"{p['id']}-capa.png")
    return files

async def main(only=None, part='all'):
    out = C.OUT
    ed = out / 'editaveis'; md = out / 'media'; tmp = out / '_frames'
    for d in (ed, md, tmp): d.mkdir(parents=True, exist_ok=True)
    vfile = out / f'versions-{part}.json'
    versions = {}
    for vf in sorted(out.glob('versions-*.json')):
        for k, val in json.loads(vf.read_text()).items():
            if k not in versions or val['v'] > versions[k]['v']: versions[k] = val
    manifest_f = out / f'manifest-{part}.json'
    manifest = {m['id']: m for m in json.loads(manifest_f.read_text())['pieces']} if manifest_f.exists() else {}
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        page = await br.new_page(device_scale_factor=1)
        for p in C.PIECES:
            if only and not any(p['id'].startswith(o) for o in only):
                continue
            t0 = time.time()
            hp = ed / f"{p['id']}.html"
            hp.write_text(p['html'])
            h = hashlib.sha256((p['html'] + p.get('cover', '') + p['caption']).encode()).hexdigest()[:10]
            prev = versions.get(p['id'])
            if not prev: v = 1
            elif prev['hash'] != h: v = prev['v'] + 1
            else: v = prev['v']
            versions[p['id']] = {'v': v, 'hash': h}
            if p['fmt'] == 'reel':
                files = await render_reel(page, p, hp, md, tmp)
            else:
                files = await render_static(page, p, hp, md)
            # hash de mídia (muda quando a arte muda)
            mh = hashlib.sha256(b''.join((md / f).read_bytes() for f in files)).hexdigest()[:10]
            manifest[p['id']] = {
                'id': p['id'], 'brand': p['brand'], 'fmt': p['fmt'], 'day': p['day'], 'dia': C.DIAS[p['day']],
                'slot': p.get('slot', ''), 'title': p['title'], 'kind': p.get('kind', 'engajamento'),
                'caption': p['caption'], 'notes': p.get('notes', ''), 'version': f"{C.PACK}-{p['id']}-v{v}",
                'v': v, 'hash': mh, 'media': files, 'editable': f"editaveis/{p['id']}.html",
                'duration': p.get('total'), 'sticker': p.get('sticker', ''),
            }
            print(f"{p['id']}: v{v} {files} {time.time() - t0:.1f}s", flush=True)
        await br.close()
    vfile.write_text(json.dumps(versions, indent=1))
    order = {m['id']: i for i, m in enumerate(C.PIECES)}
    pieces = sorted(manifest.values(), key=lambda m: order.get(m['id'], 999))
    manifest_f.write_text(json.dumps({'pack': C.PACK, 'pieces': pieces}, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    import importlib
    for m in ('quiddo', 'retrozap', 'sportdna'):
        try: importlib.import_module(m)
        except ModuleNotFoundError as e: print('sem', m, e)
    args = sys.argv[1:]
    part = 'all'
    if args and args[0].startswith('--part='):
        part = args[0][7:]; args = args[1:]
    asyncio.run(main(args or None, part))
