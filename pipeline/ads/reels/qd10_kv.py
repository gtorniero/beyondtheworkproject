"""ADC-QD-10 v1 · KV Quiddo Empresas (estático 4:5). Telão e celular com a captura REAL do modo Corporativo (qd10_cap.py),
mesma pergunta nos dois. Uso: python3 qd10_kv.py <pasta da captura> <saida.png> [variacao a|b|c] [jpg720]"""
import asyncio, base64, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from estudio import ff, svg, A
from playwright.async_api import async_playwright
CAP, OUT, VAR = Path(sys.argv[1]), Path(sys.argv[2]), (sys.argv[3] if len(sys.argv) > 3 else 'a')
Q = A / 'quiddo'
CREME, TINTA, MATA, VERDE, AMARELO = '#FFF6E6', '#0E2A22', '#0B5D45', '#13A07A', '#FFC83D'
def uri(p): return 'data:image/png;base64,' + base64.b64encode(Path(p).read_bytes()).decode()
FONTS = ff('Fraunces', 'Fraunces-900.woff2', '900') + ff('Nunito', 'Nunito-var.woff2', '600 900')
TV, CEL = uri(CAP / 'tv_q3.png'), uri(CAP / 'cel_q.png')
LOGO = {'cor': svg(Q / 'quiddo-cor.svg', w=230), 'neg': svg(Q / 'quiddo-negativo.svg', w=230)}
SIMS = ''.join(svg(Q / f'{s}.svg', w=74, style=f'transform:rotate({r}deg)') for s, r in (('folha', -8), ('sol', 6), ('gota', -4), ('flor', 8)))
CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;overflow:hidden}}
.kv{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Nunito,sans-serif;color:{TINTA}}}
.abs{{position:absolute}}
.t{{font-family:Fraunces,serif;font-weight:900;letter-spacing:-.025em;line-height:.98}}
.mt{{display:inline-block;background:{AMARELO};color:{TINTA};padding:0 .12em;transform:rotate(-2deg);border-radius:.08em;border:5px solid {TINTA};box-shadow:0 7px 0 {TINTA}}}
.tv{{background:#111;border-radius:22px;padding:14px;border:6px solid {TINTA};box-shadow:0 16px 0 {TINTA}}}
.tv img{{display:block;width:100%;border-radius:10px}}
.ph{{background:#0b0b0d;border-radius:54px;padding:12px;border:6px solid {TINTA};box-shadow:0 14px 0 {TINTA}}}
.ph .s{{border-radius:42px;overflow:hidden}} .ph img{{display:block;width:100%}}
.cta{{display:inline-flex;align-items:center;gap:14px;background:{AMARELO};color:{TINTA};border:6px solid {TINTA};box-shadow:0 10px 0 {TINTA};border-radius:999px;padding:18px 34px;font-weight:900;font-size:40px}}
.url{{font-weight:900;font-size:32px}}
.sub{{font-weight:700;font-size:34px;line-height:1.3}}
"""
def tv(w, crop=1030): return f'<div class="tv" style="width:{w}px"><div style="overflow:hidden;border-radius:10px;aspect-ratio:1920/{crop}"><img src="{TV}"></div></div>'
def ph(w, h_ratio=1.62): return f'<div class="ph" style="width:{w}px"><div class="s" style="aspect-ratio:1080/{int(1080*h_ratio)}"><img src="{CEL}"></div></div>'
TIT = 'Sua apresentação<br>vira <span class="mt">participação.</span>'
SUB = 'Quiz ao vivo para apresentações e treinamentos. Você pergunta. O público responde pelo celular.'
def var_a():  # creme: título em cima, telão grande, celular sobreposto à direita, CTA embaixo
    return f'''<div class="kv" style="background:{CREME}">
      <div class="abs" style="left:70px;top:64px">{LOGO['cor']}</div>
      <div class="abs t" style="left:70px;top:150px;width:960px;font-size:92px">{TIT}</div>
      <div class="abs" style="left:52px;top:420px;transform:rotate(-1.5deg)">{tv(760)}</div>
      <div class="abs" style="left:700px;top:470px;transform:rotate(3deg)">{ph(320)}</div>
      <div class="abs sub" style="left:70px;top:900px;width:590px">{SUB}</div>
      <div class="abs" style="left:70px;top:1150px;display:flex;align-items:center;gap:26px"><span class="cta">Crie seu quiz</span><span class="url">quiddo.com.br</span></div>
      <div class="abs" style="right:66px;top:1225px;display:flex;gap:10px">{SIMS}</div></div>'''
def var_b():  # tinta: palco escuro como a sala, telão no alto, celular embaixo à direita
    return f'''<div class="kv" style="background:{TINTA};color:{CREME}">
      <div class="abs" style="left:-200px;top:300px;width:1480px;height:760px;border-radius:50%;background:radial-gradient({MATA},transparent 70%);opacity:.9"></div>
      <div class="abs" style="left:70px;top:64px">{LOGO['neg']}</div>
      <div class="abs t" style="left:70px;top:150px;width:960px;font-size:92px;color:{CREME}">{TIT}</div>
      <div class="abs" style="left:70px;top:430px">{tv(940)}</div>
      <div class="abs" style="left:792px;top:905px;transform:rotate(4deg)">{ph(250)}</div>
      <div class="abs sub" style="left:70px;top:1010px;width:620px;color:{CREME}">{SUB}</div>
      <div class="abs" style="left:70px;top:1196px;display:flex;align-items:center;gap:26px"><span class="cta">Crie seu quiz</span><span class="url" style="color:{AMARELO}">quiddo.com.br</span></div></div>'''
def var_c():  # verde mata: celular grande à esquerda (protagonista), telão atrás à direita
    return f'''<div class="kv" style="background:{MATA};color:{CREME}">
      <div class="abs" style="left:70px;top:64px">{LOGO['neg']}</div>
      <div class="abs t" style="left:70px;top:150px;width:960px;font-size:92px;color:{CREME}">{TIT}</div>
      <div class="abs" style="left:330px;top:440px;transform:rotate(2deg)">{tv(700)}</div>
      <div class="abs" style="left:70px;top:520px;transform:rotate(-3deg)">{ph(360)}</div>
      <div class="abs sub" style="left:500px;top:900px;width:520px;color:{CREME}">{SUB}</div>
      <div class="abs" style="left:500px;top:1150px;display:flex;flex-direction:column;gap:18px"><span class="cta">Crie seu quiz</span><span class="url" style="color:{AMARELO}">quiddo.com.br</span></div></div>'''
HTML = f'<!doctype html><meta charset="utf-8"><style>{FONTS}{CSS}</style>' + {'a': var_a, 'b': var_b, 'c': var_c}[VAR]()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        await pg.set_content(HTML); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(OUT)); await b.close()
asyncio.run(main())
if len(sys.argv) > 4:
    from PIL import Image
    im = Image.open(OUT).convert('RGB'); im.resize((720, 900), Image.LANCZOS).save(sys.argv[4], quality=88)
