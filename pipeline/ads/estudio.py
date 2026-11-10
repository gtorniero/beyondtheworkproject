"""Estúdio de ADs (modelo novo, 10/11/2026): composição em HTML/CSS com câmera, tipografia cinética, cortes e
captura REAL do produto como clipe (sequência de quadros), renderizada quadro a quadro (30 fps, H.264, sem áudio).

Uso típico (ver DIRECAO.md):
    c = Comp('reel', total=20, bg='#1A0B2E', fonts=FONTS, css=CSS)
    cam = c.kf([(0, 'transform:scale(1)'), (2, 'transform:scale(1.6) translate(-8%,6%)')])
    c.add(f'<div class="abs" style="{c.an(cam, c.show(0, 4))}">{c.clip(frames_dir, src0=12.4, t0=0, t1=4)}</div>')
    c.add(c.words('Quem ri *mais* no grupo?', t=0.1, x=80, y=300, size=120))
    render(c, 'out.mp4', cover=('capa.jpg', 1.2))
Tempos sempre absolutos, em segundos da linha do tempo final. Clipes: extraia antes com frames(video, pasta)."""
import asyncio, base64, json, re, subprocess
from pathlib import Path
from playwright.async_api import async_playwright

R = Path(__file__).resolve().parent.parent
A, F = R / 'assets', R / 'fonts'
FPS = 30
# formato: largura, altura, zona segura (topo, base) em px. No reel nada importante fora da zona segura.
FMT = {'reel': (1080, 1920, 270, 370), 'feed': (1080, 1350, 70, 70), 'sq': (1080, 1080, 60, 60)}
EASE = 'cubic-bezier(.2,.8,.2,1)'      # saída suave (padrão)
SNAP = 'cubic-bezier(.7,0,.2,1)'       # corte de câmera rápido, com peso
BACK = 'cubic-bezier(.34,1.56,.64,1)'  # com quique


def ff(fam, file, weight):
    b = base64.b64encode((F / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b}) format('woff2');font-weight:{weight};font-display:block}}"


def svg(path, w=None, h=None, style=''):
    s = re.sub(r'<\?xml[^>]*>', '', Path(path).read_text()).strip()
    tag = re.search(r'<svg\b[^>]*>', s).group(0)
    new = re.sub(r'\s(width|height)="[^"]*"', '', tag)
    add = (f' width="{w}"' if w else '') + (f' height="{h}"' if h else '') + (f' style="{style}"' if style else '')
    return s.replace(tag, new.replace('<svg', '<svg' + add, 1), 1)


def frames(video, out, start=None, dur=None, width=None, fps=FPS, q=3):
    """Extrai quadros JPG (00000.jpg…) de um vídeo de captura. Devolve (pasta, n)."""
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    if not any(out.iterdir()):
        cmd = ['ffmpeg', '-y', '-v', 'error']
        if start is not None: cmd += ['-ss', f'{start}']
        cmd += ['-i', str(video)]
        if dur is not None: cmd += ['-t', f'{dur}']
        vf = f'fps={fps}' + (f',scale={width}:-2:flags=lanczos' if width else '')
        subprocess.run(cmd + ['-vf', vf, '-q:v', str(q), '-start_number', '0', str(out / '%05d.jpg')], check=True)
    return out, len(list(out.glob('*.jpg')))


BASE = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#000;overflow:hidden}
#st{position:relative;overflow:hidden}
.abs{position:absolute}
.fill{position:absolute;inset:0}
.w{display:inline-block;white-space:pre;will-change:transform,opacity,filter}
.ln{display:block}
img.clip{display:block;width:100%;height:100%;object-fit:cover}
.ph{position:relative;background:#0b0b0d;box-shadow:0 60px 120px rgba(0,0,0,.45),0 0 0 2px rgba(255,255,255,.08) inset}
.ph .scr{position:absolute;overflow:hidden;background:#000}
.ph .gl{position:absolute;inset:0;border-radius:inherit;background:linear-gradient(125deg,rgba(255,255,255,.16) 0%,rgba(255,255,255,0) 28%);pointer-events:none}
"""


class Comp:
    def __init__(s, fmt, total, bg, fonts='', css=''):
        s.fmt = fmt; s.W, s.H, s.top, s.bot = FMT[fmt]; s.T = float(total); s.bg = bg
        s.fonts, s.css = fonts, css; s.k, s.layers, s.clips, s.counts, s.n = [], [], [], [], 0

    # ---------- animação
    def kf(s, pts, ease=EASE):
        """pts = [(t, 'props css'[, ease do trecho seguinte]), …] em tempo absoluto. Antes do 1º ponto vale o 1º; depois do último, o último.
        Devolve o nome da animação; junte várias no mesmo elemento com an()."""
        s.n += 1; name = f'k{s.n}'; fr = []
        pts = sorted(pts, key=lambda p: p[0])
        if pts[0][0] > 0: fr.append(f'0%{{{pts[0][1]}}}')
        for p in pts:
            e = p[2] if len(p) > 2 else ease
            fr.append(f'{min(100, max(0, p[0] / s.T * 100)):.4f}%{{{p[1]};animation-timing-function:{e}}}')
        if pts[-1][0] < s.T: fr.append(f'100%{{{pts[-1][1]}}}')
        s.k.append(f'@keyframes {name}{{{"".join(fr)}}}')
        return name

    def an(s, *names):
        return 'animation:' + ','.join(f'{n} {s.T}s linear 0s 1 both' for n in names if n) + ';'

    def show(s, t0, t1=None, fin=0.0, fout=0.0):
        """Visível só entre t0 e t1 (corte seco por padrão; fin/fout = fade em segundos)."""
        t1 = s.T + 1 if t1 is None else t1
        fin, fout = max(fin, .002), max(fout, .002)  # keyframes no mesmo instante se fundem no CSS e viram fade longo
        p = []
        if t0 > 0: p += [(max(0, t0 - fin - 1e-3), 'opacity:0;visibility:hidden', 'linear'), (max(0, t0 - fin), 'opacity:0;visibility:visible', 'linear')]
        p += [(t0, 'opacity:1;visibility:visible', 'linear')]
        if t1 < s.T: p += [(t1, 'opacity:1;visibility:visible', 'linear'), (t1 + fout, 'opacity:0;visibility:visible', 'linear'), (t1 + fout + 1e-3, 'opacity:0;visibility:hidden', 'linear')]
        return s.kf(p, 'linear')

    def enter(s, t, kind='rise', dur=.5, dist=60, ease=None):
        """Entrada de um elemento no tempo t. kinds: rise, drop, left, right, pop, zoom (de grande para 1), blur, fade."""
        a = {'rise': f'opacity:0;transform:translateY({dist}px)', 'drop': f'opacity:0;transform:translateY(-{dist}px)',
             'left': f'opacity:0;transform:translateX(-{dist}px)', 'right': f'opacity:0;transform:translateX({dist}px)',
             'pop': 'opacity:0;transform:scale(.5)', 'zoom': 'opacity:0;transform:scale(1.6)',
             'blur': 'opacity:0;filter:blur(24px);transform:scale(1.08)', 'fade': 'opacity:0'}[kind]
        b = 'opacity:1;transform:none;filter:none'
        return s.kf([(t, a, ease or (BACK if kind == 'pop' else EASE)), (t + dur, b)])

    def exit(s, t, kind='fade', dur=.3, dist=60):
        b = {'fade': 'opacity:0', 'up': f'opacity:0;transform:translateY(-{dist}px)', 'down': f'opacity:0;transform:translateY({dist}px)',
             'shrink': 'opacity:0;transform:scale(.8)', 'blur': 'opacity:0;filter:blur(20px)'}[kind]
        return s.kf([(t, 'opacity:1', SNAP), (t + dur, b)])

    # ---------- camadas
    def add(s, html):
        s.layers.append(html); return s

    def clip(s, folder, src0, t0, t1, rate=1.0, style='', hold=True):
        """Clipe de captura real: mostra a pasta de quadros a partir de src0 (s do vídeo fonte) entre t0 e t1 da linha do tempo.
        rate<1 = câmera lenta. hold=True segura o primeiro/último quadro fora do intervalo (útil em transições)."""
        folder = Path(folder); n = len(list(folder.glob('*.jpg'))); s.n += 1; cid = f'c{s.n}'
        s.clips.append(dict(id=cid, dir=folder.resolve().as_uri(), src0=src0, t0=t0, t1=t1, rate=rate, n=n, hold=hold))
        return f'<img class="clip" id="{cid}" style="{style}">'

    def count(s, a, b, t0, t1, style='', fmt='int', suf='', pre=''):
        """Número que roda de a até b entre t0 e t1 (fmt: int | mil = 1.234 | dec1)."""
        s.n += 1; cid = f'n{s.n}'; s.counts.append(dict(id=cid, a=a, b=b, t0=t0, t1=t1, fmt=fmt, suf=suf, pre=pre))
        return f'<span id="{cid}" style="font-variant-numeric:tabular-nums;{style}"></span>'

    def words(s, text, t, x=None, y=None, w=None, size=110, step=.07, dur=.5, kind='rise', style='', cls='', out=None, align='left', lh=1.0):
        """Tipografia cinética: cada palavra entra em sequência. *palavra* = destaque (classe .hl); \\n quebra linha.
        out = tempo de saída (todas juntas). Devolve o bloco posicionado (ou inline se x/y forem None)."""
        i = 0; lines = []
        for line in text.split('\n'):
            ws = []
            for tok in re.findall(r'\*[^*]+\*|\S+', line):
                hl = tok.startswith('*'); tok = tok.strip('*')
                a = s.enter(t + i * step, kind, dur, dist=size * .5)
                ws.append(f'<span class="w{" hl" if hl else ""}" style="{s.an(a)}">{tok}</span>'); i += 1
            lines.append(f'<span class="ln">{" ".join(ws)}</span>')
        o = s.an(s.exit(out, 'up', .25, 40)) if out is not None else ''
        pos = f'position:absolute;left:{x}px;top:{y}px;' if x is not None else ''
        return (f'<div class="{cls}" style="{pos}{f"width:{w}px;" if w else ""}font-size:{size}px;line-height:{lh};text-align:{align};{o}{style}">'
                + ''.join(lines) + '</div>')

    def wipe(s, t, color, dur=.5, direction='up'):
        """Transição: painel de cor atravessa a tela e cobre tudo exatamente em t (troque a cena em t)."""
        ax, a, b = {'up': ('Y', 100, -100), 'down': ('Y', -100, 100), 'left': ('X', 100, -100), 'right': ('X', -100, 100)}[direction]
        k = s.kf([(t - dur / 2, f'transform:translate{ax}({a}%)', SNAP), (t, f'transform:translate{ax}(0%)', SNAP), (t + dur / 2, f'transform:translate{ax}({b}%)')])
        return f'<div class="fill" style="background:{color};z-index:50;{s.an(k)}"></div>'

    def flash(s, t, color='#fff', dur=.22, peak=.85):
        k = s.kf([(t - .03, 'opacity:0', 'linear'), (t, f'opacity:{peak}', 'ease-out'), (t + dur, 'opacity:0')])
        return f'<div class="fill" style="background:{color};z-index:60;pointer-events:none;{s.an(k)}"></div>'

    def ring(s, x, y, t, size=150, color='rgba(255,255,255,.9)'):
        """Pulso de toque/atenção centrado em (x, y)."""
        k = s.kf([(t - .01, 'opacity:0;transform:translate(-50%,-50%) scale(.3)', 'ease-out'), (t + .08, 'opacity:1;transform:translate(-50%,-50%) scale(.7)', 'ease-out'), (t + .6, 'opacity:0;transform:translate(-50%,-50%) scale(1.5)')])
        return f'<div class="abs" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;border:8px solid {color};z-index:40;{s.an(k)}"></div>'

    def phone(s, inner, w=620, h=None, bezel=16, radius=84, frame='#0b0b0d', notch=True):
        """Celular genérico (sem marca) com a tela = inner (normalmente um clip 9:16). Tamanho externo w×h."""
        h = h or round((w - 2 * bezel) * 16 / 9 + 2 * bezel)
        n = (f'<div class="abs" style="left:50%;top:{bezel + 14}px;width:{w * .26:.0f}px;height:{w * .05:.0f}px;margin-left:-{w * .13:.0f}px;border-radius:99px;background:{frame};z-index:3"></div>' if notch else '')
        return (f'<div class="ph" style="width:{w}px;height:{h}px;border-radius:{radius}px;background:{frame}">'
                f'<div class="scr" style="left:{bezel}px;top:{bezel}px;right:{bezel}px;bottom:{bezel}px;border-radius:{radius - bezel}px">{inner}</div>{n}<div class="gl"></div></div>')

    # ---------- saída
    def html(s):
        js = f"""<script>
const CLIPS={json.dumps(s.clips)},COUNTS={json.dumps(s.counts)};
function nf(v,f){{ if(f==='mil') return Math.round(v).toLocaleString('pt-BR'); if(f==='dec1') return v.toFixed(1).replace('.',','); return String(Math.round(v)); }}
window.seek=async function(t){{
  document.getAnimations().forEach(a=>{{a.pause();a.currentTime=t*1000;}});
  const ps=[];
  for(const c of CLIPS){{ if(!c.hold&&(t<c.t0-.05||t>c.t1+.05)) continue; if(c.hold&&(t<c.t0-1.5||t>c.t1+1.5)) continue;
    const el=document.getElementById(c.id); const tt=Math.max(c.t0,Math.min(c.t1,t));
    let i=Math.round((c.src0+(tt-c.t0)*c.rate)*{FPS}); i=Math.max(0,Math.min(c.n-1,i));
    const u=c.dir+'/'+String(i).padStart(5,'0')+'.jpg';
    if(el.dataset.u!==u){{ el.dataset.u=u; el.src=u; ps.push(el.decode().catch(()=>{{}})); }} }}
  for(const c of COUNTS){{ const el=document.getElementById(c.id); let p=Math.max(0,Math.min(1,(t-c.t0)/(c.t1-c.t0))); p=1-Math.pow(1-p,3);
    el.textContent=c.pre+nf(c.a+(c.b-c.a)*p,c.fmt)+c.suf; }}
  await Promise.all(ps);
}};
</script>"""
        return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{s.fonts}{BASE}{s.css}{"".join(s.k)}</style></head><body>'
                f'<div id="st" style="width:{s.W}px;height:{s.H}px;background:{s.bg}">{"".join(s.layers)}</div>{js}</body></html>')


async def _render(c, out, cover, t_from, t_to, crf, sheet):
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    hp = out.with_suffix('.html'); hp.write_text(c.html())
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': c.W, 'height': c.H}, device_scale_factor=1)
        await pg.goto(hp.as_uri()); await pg.evaluate('document.fonts.ready')
        if cover:
            await pg.evaluate(f'seek({cover[1]})'); await pg.screenshot(path=str(cover[0]), type='jpeg', quality=92)
        if sheet:  # folha de contato rápida: [(t, caminho)]
            for t, path in sheet:
                await pg.evaluate(f'seek({t})'); await pg.screenshot(path=str(path), type='jpeg', quality=80)
            await b.close(); return
        a, z = int(round((t_from or 0) * FPS)), int(round((t_to or c.T) * FPS))
        ffm = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-', '-an', '-c:v', 'libx264',
                                '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', str(crf), '-preset', 'medium', '-r', str(FPS), '-movflags', '+faststart', str(out)], stdin=subprocess.PIPE)
        for i in range(a, z):
            await pg.evaluate(f'seek({i / FPS:.5f})')
            ffm.stdin.write(await pg.screenshot(type='jpeg', quality=95))
        ffm.stdin.close(); ffm.wait(); await b.close()


def render(c, out, cover=None, t_from=None, t_to=None, crf=17):
    """Renderiza a composição em MP4. cover=(caminho.jpg, t) salva a capa."""
    asyncio.run(_render(c, out, cover, t_from, t_to, crf, None))


def preview(c, out_jpg, times, cols=6, scale=.25):
    """Folha de contato da composição nos tempos dados (olhe SEMPRE antes de renderizar)."""
    from PIL import Image
    out_jpg = Path(out_jpg); tmp = out_jpg.with_suffix(''); tmp.mkdir(parents=True, exist_ok=True)
    sheet = [(t, tmp / f'{i:03d}.jpg') for i, t in enumerate(times)]
    asyncio.run(_render(c, tmp / 'x.mp4', None, None, None, 17, sheet))
    ims = [Image.open(p) for _, p in sheet]; w, h = int(c.W * scale), int(c.H * scale)
    rows = (len(ims) + cols - 1) // cols; sh = Image.new('RGB', (cols * (w + 6), rows * (h + 6)), '#777')
    for i, im in enumerate(ims): sh.paste(im.resize((w, h)), ((i % cols) * (w + 6), (i // cols) * (h + 6)))
    sh.save(out_jpg, quality=85); return out_jpg
