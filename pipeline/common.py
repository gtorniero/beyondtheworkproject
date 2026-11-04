"""Framework do Pack Semanal: peças como HTML autocontido (editável) + render PNG/MP4."""
import base64, hashlib, json, os, re, subprocess, shutil
from pathlib import Path

ROOT = Path(__file__).parent
A = ROOT / 'assets'
FONTS = ROOT / 'fonts'
OUT = ROOT / 'out'
PACK = 'S02'  # Pack Semanal 02
NUM = '02'
SEMANA = '16–22/11'
SEMANA_LONGA = '16 a 22/11/2026'
PREV = 'S01'  # pack anterior (para a grade)

# Datas da semana do pack (dia 1 = segunda 16/11/2026)
DIAS = {1: 'seg 16/11', 2: 'ter 17/11', 3: 'qua 18/11', 4: 'qui 19/11', 5: 'sex 20/11', 6: 'sáb 21/11', 7: 'dom 22/11'}
DATAS = {1: '16/11/2026 (seg)', 2: '17/11/2026 (ter)', 3: '18/11/2026 (qua)', 4: '19/11/2026 (qui)',
         5: '20/11/2026 (sex)', 6: '21/11/2026 (sáb)', 7: '22/11/2026 (dom)'}

def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()

def font_face(family, file, weight='400', style='normal'):
    return (f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{b64(FONTS/file)}) format('woff2');"
            f"font-weight:{weight};font-style:{style};font-display:block}}")

def svg(path, **attrs):
    """SVG oficial inline (sem XML header), com atributos extras no <svg>."""
    s = Path(path).read_text()
    s = re.sub(r'<\?xml[^>]*>', '', s).strip()
    if attrs:
        extra = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
        s = re.sub(r'<svg\b', f'<svg {extra}', s, count=1)
        # remove width/height originais quando passamos novos
        if 'width' in attrs or 'height' in attrs:
            s = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"(?=[^>]*\b\2=)', r'\1', s, count=2)
    return s

def svg_sized(path, w=None, h=None, cls='', style=''):
    s = Path(path).read_text()
    s = re.sub(r'<\?xml[^>]*>', '', s).strip()
    m = re.search(r'<svg\b[^>]*>', s)
    tag = m.group(0)
    new = re.sub(r'\s(width|height)="[^"]*"', '', tag)
    add = ''
    if w: add += f' width="{w}"'
    if h: add += f' height="{h}"'
    if cls: add += f' class="{cls}"'
    if style: add += f' style="{style}"'
    new = new.replace('<svg', '<svg' + add, 1)
    return s.replace(tag, new, 1)

# ---------------------------------------------------------------- timeline (reels)
class TL:
    """Cenas com tempo absoluto. Gera @keyframes por cena (entra/sai) sobre a duração total."""
    def __init__(self, total):
        self.T = total
        self.css = []
        self.n = 0
        self.scenes = []  # (start,end,words)

    def scene(self, start, end, fade=0.18, fin=True, fout=True, kind='fade'):
        self.n += 1
        name = f'sc{self.n}'
        T = self.T
        p = lambda t: max(0, min(100, t / T * 100))
        a, b = start, start + (fade if fin else 0.001)
        c, d = end - (fade if fout else 0.001), end
        if end >= T - 0.01:
            c, d = T, T
        if kind == 'fade':
            k0, k1 = 'opacity:0', 'opacity:1'
        elif kind == 'up':
            k0, k1 = 'opacity:0;transform:translateY(40px)', 'opacity:1;transform:none'
        else:
            k0, k1 = 'opacity:0', 'opacity:1'
        frames = f'0%{{{k0}}}' if start > 0 else ''
        frames += f'{p(a):.4f}%{{{k0 if start>0 else k1}}}{p(b):.4f}%{{{k1}}}{p(c):.4f}%{{{k1}}}'
        if d < T:
            frames += f'{p(d):.4f}%{{opacity:0}}100%{{opacity:0}}'
        else:
            frames += '100%{' + k1 + '}'
        self.css.append(f'@keyframes {name}{{{frames}}}')
        self.scenes.append((start, end))
        return f'class="sc" style="animation:{name} {T}s linear 0s 1 both"'

    def style(self):
        return '\n'.join(self.css)

def at(t, anim='pop', dur=None, extra=''):
    """Atributo style para entrada de um elemento no tempo absoluto t."""
    d = dur or {'pop': .42, 'rise': .45, 'drop': .55, 'fade': .3, 'grow': .9, 'type': .5, 'slideL': .45, 'slideR': .45, 'stamp': .5, 'draw': .9, 'count': 1.0, 'wipe': .5}.get(anim, .45)
    return f'animation:{anim} {d}s var(--ease-{anim}, cubic-bezier(.34,1.56,.64,1)) {t:.3f}s 1 both;{extra}'

BASE_KEYFRAMES = """
@keyframes pop{0%{opacity:0;transform:scale(.4) rotate(var(--r,0deg))}60%{opacity:1;transform:scale(1.08) rotate(var(--r,0deg))}100%{opacity:1;transform:scale(1) rotate(var(--r,0deg))}}
@keyframes rise{0%{opacity:0;transform:translateY(46px) rotate(var(--r,0deg))}100%{opacity:1;transform:translateY(0) rotate(var(--r,0deg))}}
@keyframes drop{0%{opacity:0;transform:translateY(-220px) rotate(calc(var(--r,0deg) - 10deg))}70%{opacity:1;transform:translateY(10px) rotate(var(--r,0deg))}85%{transform:translateY(-6px) rotate(var(--r,0deg))}100%{opacity:1;transform:translateY(0) rotate(var(--r,0deg))}}
@keyframes fade{0%{opacity:0}100%{opacity:1}}
@keyframes slideL{0%{opacity:0;transform:translateX(-80px)}100%{opacity:1;transform:none}}
@keyframes slideR{0%{opacity:0;transform:translateX(80px)}100%{opacity:1;transform:none}}
@keyframes grow{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}
@keyframes growY{0%{transform:scaleY(0)}100%{transform:scaleY(1)}}
@keyframes stamp{0%{opacity:0;transform:scale(1.8) rotate(-8deg)}70%{opacity:1;transform:scale(.96) rotate(var(--r,-3deg))}100%{opacity:1;transform:scale(1) rotate(var(--r,-3deg))}}
@keyframes wipe{0%{clip-path:inset(0 100% 0 0)}100%{clip-path:inset(0 0 0 0)}}
@keyframes draw{0%{stroke-dashoffset:var(--len,1000)}100%{stroke-dashoffset:0}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes dots{0%,100%{transform:translateY(0)}30%{transform:translateY(-14px)}}
"""

# ---------------------------------------------------------------- documento
def doc(title, fonts_css, css, body, w, h, reel=False, total=0):
    js = ''
    if reel:
        # No navegador: toca sozinho e clique para recomeçar. No render: tempo controlado de fora.
        js = f"""<script>
window.__T={total};
window.seek=function(t){{document.getAnimations().forEach(function(a){{a.pause();a.currentTime=t*1000;}});}};
if(!/render=1/.test(location.search)){{document.addEventListener('click',function(){{document.getAnimations().forEach(function(a){{a.currentTime=0;a.play();}});}});}}
else{{document.documentElement.classList.add('render');}}
</script>"""
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>{title}</title>
<meta name="viewport" content="width={w}">
<style>
{fonts_css}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#222}}
.page{{width:{w}px;height:{h}px;position:relative;overflow:hidden}}
.page+.page{{margin-top:40px}}
.sc{{position:absolute;inset:0}}
.abs{{position:absolute}}
{BASE_KEYFRAMES}
{css}
</style></head><body>
{body}
{js}
</body></html>"""

# ---------------------------------------------------------------- registro de peças
PIECES = []

def add(piece):
    PIECES.append(piece)
    return piece

def words(s):
    return len(re.findall(r"[\wÀ-ÿ%$'’-]+", re.sub(r'<[^>]+>', ' ', s)))

# ---------------------------------------------------------------- stories sem adesivo
def cta_block(kind, y, opts, txt, st):
    """Bloco desenhado no lugar do adesivo do Instagram (o agendamento perde adesivos).
    st: estilo da marca — bgs (lista de fundos dos botões), fg, tfont, bfont, border, radius, shadow, txt_color."""
    btn = lambda i, o, extra='': (f'<div style="background:{st["bgs"][i % len(st["bgs"])]};color:{st["fg"]};border:{st["border"]};border-radius:{st["radius"]};'
                                  f'box-shadow:{st["shadow"]};font-family:{st["tfont"]};font-weight:{st.get("tw", 800)};font-size:{st.get("fs", 48)}px;padding:24px 32px;{extra}">'
                                  f'{"ABCD"[i] + " · " if kind in ("enquete", "quiz") and len(opts) > 2 or kind == "quiz" else ""}{o}</div>')
    if kind in ('enquete', 'quiz'):
        if len(opts) == 2:
            inner = f'<div style="display:grid;gap:20px">{btn(0, opts[0])}{btn(1, opts[1])}</div>'
        else:
            inner = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">{"".join(btn(i, o) for i, o in enumerate(opts))}</div>'
    elif kind == 'slider':
        inner = (f'<div style="background:{st["bgs"][0]};border:{st["border"]};border-radius:{st["radius"]};padding:34px 40px;color:{st["fg"]};font-family:{st["tfont"]};font-weight:800;font-size:48px">'
                 f'0 <span style="display:inline-block;vertical-align:middle;width:640px;height:14px;border-radius:7px;background:{st["fg"]};opacity:.35;margin:0 24px"></span> 10</div>')
    else:  # caixa / link: só o texto em destaque
        inner = ''
    tsz = st.get('ts', 40) if inner else st.get('ts_big', 56)
    t = f'<div style="margin-top:{24 if inner else 0}px;font-family:{st["bfont"]};font-weight:800;font-size:{tsz}px;line-height:1.25;color:{st["txt_color"]}">{txt}</div>'
    if not inner:
        t = f'<div style="display:inline-block;background:{st["bgs"][0]};color:{st["fg"]};border:{st["border"]};border-radius:{st["radius"]};box-shadow:{st["shadow"]};padding:26px 34px;font-family:{st["tfont"]};font-weight:800;font-size:{tsz}px;line-height:1.2">{txt}</div>'
    return f'<div class="abs" style="left:80px;top:{y}px;width:920px">{inner}{t}</div>'

def apply_ctas(table, st_for):
    """Desenha o CTA no lugar do adesivo e troca a instrução do adesivo, peça a peça."""
    for p in PIECES:
        if p['id'] in table:
            kind, y, opts, txt = table[p['id']]
            st = st_for(p['id'])
            blk = cta_block(kind, y, opts, txt, st)
            i = p['html'].rfind('</section>')
            p['html'] = p['html'][:i] + blk + p['html'][i:]
            p['sticker'] = 'Sem adesivo: o CTA já está na arte. Agendar no Business Suite.'
