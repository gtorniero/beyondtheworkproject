"""Estáticos 1:1 (1080×1080) e 1,91:1 (1200×628) dos heróis aprovados ADC-RZ-08-v1 e ADC-RZ-09-v1.
Coluna da direita do Facebook (não aceita vídeo), busca, Messenger e Audience Network. Derivados da capa aprovada:
mesmo título, mesma tela real do app (quadro da captura usada na capa), mesmo CTA, URL e assinatura. Não substitui os vídeos 9:16.
Uso: python3 rz_estaticos.py <quadros RZ-08> <quadros RZ-09> <pasta saída>"""
import sys, base64, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import ff, svg, A
from playwright.sync_api import sync_playwright

RZ = A / 'retrozap'
FONTS = ff('Bricolage Grotesque', 'Bricolage-800.woff2', '800') + ff('DM Sans', 'DMSans-var.woff2', '400 700')

ADS = {
    'ADC-RZ-08-v1': dict(frames=0, src=79.2, casa='grupo', bg='#1A0B2E', txt='#FFF4E0', hl='#FFC23C', pill='#FFC23C', pilltxt='#1A0B2E',
                         blobs=('#A98BFF', '#FF4F8B'), shadow='0 6px 30px rgba(26,11,46,.55)', wm=.12,
                         title='Quem ri *mais*\nno seu grupo?', cta='Faça a retrospectiva 2026 do *seu grupo.*'),
    'ADC-RZ-09-v1': dict(frames=1, src=116.0, casa='casal', bg='#FFF3EC', txt='#5E0B2B', hl='#E0245E', pill='#E0245E', pilltxt='#FFF3EC',
                         blobs=('#FF4F8B', '#FFB59A'), shadow='0 4px 24px rgba(255,243,236,.9)', wm=.10,
                         title='Quantas mensagens\nvocês trocaram\nem *2026*?', cta='Façam a retrospectiva *de vocês.*'),
}
# formato: (W, H, texto x, logo y/altura, título y/tamanho, cta tamanho, celular x/y/largura, rotação Y)
FMTS = {
    'feed-coluna-1x1': dict(W=1080, H=1080, tx=64, tw=540, ly=96, lh=66, ty=250, ts=90, ts3=74, cs=42, px=622, py=150, pw=420, ry=-10),
    'busca-audience-1.91x1': dict(W=1200, H=628, tx=56, tw=720, ly=52, lh=46, ty=140, ts=78, ts3=60, cs=32, px=830, py=56, pw=292, ry=-10),
}


def hl(s, color):
    s = re.sub(r'\*([^*]+)\*', lambda m: f'<span style="color:{color}">{m.group(1)}</span>', s)
    return s.replace('\n', '<br>')


def logo(casa, h):
    """Assinatura oficial sem o retângulo de fundo do arquivo (o fundo da peça já é a cor da marca)."""
    return re.sub(r'<rect width="520" height="140" fill="[^"]+"/>', '', svg(RZ / f'logo-assinatura-{casa}.svg', h=h), count=1)


def page(ad, f, shot):
    a = ADS[ad]; W, H = f['W'], f['H']; pw = f['pw']; b = round(pw * .036); sw = pw - 2 * b; ph = round(sw * 16 / 9 + 2 * b); r = round(pw * .135)
    ts = f['ts3'] if a['title'].count('\n') == 2 else f['ts']
    img = base64.b64encode(Path(shot).read_bytes()).decode()
    b1, b2 = a['blobs']
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:{a['bg']};position:relative;font-family:'DM Sans',sans-serif}}
.abs{{position:absolute}}
.blob{{position:absolute;border-radius:50%;filter:blur({round(H * .11)}px)}}
.hd{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.035em;color:{a['txt']};text-shadow:{a['shadow']}}}
.url{{font-weight:700;background:{a['pill']};color:{a['pilltxt']};border-radius:999px;display:inline-block;white-space:nowrap}}
</style></head><body>
<div class="blob" style="left:{-W * .2:.0f}px;top:{H * .3:.0f}px;width:{H * .7:.0f}px;height:{H * .7:.0f}px;background:{b1};opacity:.5"></div>
<div class="blob" style="right:{-W * .18:.0f}px;top:{-H * .15:.0f}px;width:{H * .75:.0f}px;height:{H * .75:.0f}px;background:{b2};opacity:.34"></div>
<div class="abs" style="right:{-H * .1:.0f}px;bottom:{-H * .12:.0f}px;opacity:{a['wm']};transform:rotate(10deg)">{svg(RZ / f"logo-simbolo-{a['casa']}.svg", w=round(H * .6))}</div>
<div class="abs" style="left:{f['px']}px;top:{f['py']}px;width:{pw}px;height:{ph}px;transform:perspective(2400px) rotateY({f['ry']}deg) rotateX(3deg);
 border-radius:{r}px;background:#0b0b0d;box-shadow:0 {H * .04:.0f}px {H * .08:.0f}px rgba(0,0,0,.35)">
 <div class="abs" style="left:{b}px;top:{b}px;right:{b}px;bottom:{b}px;border-radius:{r - b}px;overflow:hidden;background:url(data:image/jpeg;base64,{img}) center/cover"></div>
</div>
<div class="abs" style="left:{f['tx'] - f['lh'] * .14:.0f}px;top:{f['ly']}px">{logo(a['casa'], f['lh'])}</div>
<div class="abs hd" style="left:{f['tx']}px;top:{f['ty']}px;width:{f['tw']}px;font-size:{ts}px;line-height:.98">{hl(a['title'], a['hl'])}</div>
<div class="abs" id="foot" style="left:{f['tx']}px;bottom:{H * .085:.0f}px;width:{f['tw'] - 20}px">
 <div class="hd" style="font-size:{f['cs']}px;line-height:1.08;letter-spacing:-.02em;margin-bottom:{f['cs'] * .5:.0f}px">{hl(a['cta'], a['hl'])}</div>
 <span class="url" style="font-size:{f['cs'] * .95:.0f}px;padding:{f['cs'] * .32:.0f}px {f['cs'] * .7:.0f}px">retrozap.com.br</span>
</div></body></html>"""


def main():
    fr = [Path(sys.argv[1]), Path(sys.argv[2])]; out = Path(sys.argv[3])
    with sync_playwright() as p:
        br = p.chromium.launch()
        for ad, a in ADS.items():
            shot = fr[a['frames']] / f"{round(a['src'] * 30):05d}.jpg"
            d = out / ad; d.mkdir(parents=True, exist_ok=True)
            for name, f in FMTS.items():
                pg = br.new_page(viewport={'width': f['W'], 'height': f['H']})
                pg.set_content(page(ad, f, shot)); pg.wait_for_timeout(300)
                dst = d / f'{ad}_{name}.png'; pg.screenshot(path=str(dst)); pg.close(); print(dst)
        br.close()


if __name__ == '__main__':
    main()
