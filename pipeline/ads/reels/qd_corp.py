"""Linha corporativa do Quiddo (QD-07/08/09, 10/11). Uso: python3 qd0X.py <captura> <trabalho> [reel|feed|sq|all|est] [preview|podio]
Captura: qd_cap4.py <partida.json> <cap> 3 2 10 → qd_remap.py <cap> → prep_marcas(cap)."""
import json, subprocess, sys
from pathlib import Path
import qd_ref7 as R

PAL = dict(bg='#1E1B3A', bg0='rgba(30,27,58,0)', blob1='#4C6EF5', b1o=.6, blob2='#F06595', b2o=.4, ink='#120F26', txt='#FFF6E6', hl_bg='#FFC83D', hl_fg='#120F26', scr='#EEEAFB',
           ring='rgba(255,255,255,.95)', flash='#FFC83D', wipe='#4C6EF5', wipe2='#F06595', wipe3='#EEEAFB', pill_bg='#FFC83D', pill_fg='#120F26', logo='quiddo-negativo.svg', sym_op=.5)


def prep_marcas(cap):
    """Depois do qd_remap: marcas.json passa a ser o tempo real (+ box); o bruto fica em marcas_raw.json."""
    cap = Path(cap)
    if not (cap / 'marcas_raw.json').exists():
        raw = json.loads((cap / 'marcas.json').read_text()); (cap / 'marcas_raw.json').write_text(json.dumps(raw))
        rt = json.loads((cap / 'marcas_rt.json').read_text()); rt['box'] = raw['box']; (cap / 'marcas.json').write_text(json.dumps(rt))


def tv_crop(src, dst, top=.13, bot=.0):
    from PIL import Image
    im = Image.open(src); w, h = im.size; im.crop((0, int(h * top), w, int(h * (1 - bot)))).save(dst); return str(dst)


def roda(cfg_fn, argv):
    cap, work = Path(argv[1]), Path(argv[2]); work.mkdir(parents=True, exist_ok=True)
    if len(argv) > 3 and argv[3] == 'est':
        m = json.loads((cap / 'marcas.json').read_text()); cfg = cfg_fn(m); cfg['m'] = m
        V = f"{cfg['id']}-{cfg['ver']}"; d = Path(__file__).resolve().parent.parent.parent / 'out' / 'media' / 'ads' / V; d.mkdir(parents=True, exist_ok=True)
        still = work / 'still.jpg'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(cfg['still_t']), '-i', str(cap / 'cel.mp4'), '-frames:v', '1', '-q:v', '2', str(still)], check=True)
        for fmt, suf in (('feed', 'feed45'), ('sq', 'sq'), ('reel', 'story'), ('land', 'land')):
            R.estatico(cfg, fmt, still, d / f'{V}-{suf}.png', hook=cfg.get('est_hook')); print(d / f'{V}-{suf}.png')
        return
    R.entrega(cfg_fn, argv)
