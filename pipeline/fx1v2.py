"""D-FX1 v2 (rodada 18): só RACKET DNA, 100% na paleta do RACKET (site sportdna.com.br/racket: --bg #08222C, --surface #0E3442, --pri #7FD0E6, --ball #DDF247, --ink #EAF4F6, --muted #9BB8C1).
Números da página do RACKET (23/11): 183 raquetes medidas, 670 avaliações lidas, 44 variáveis, 21 estudos, 379 casos em 3 idiomas, 3.000 perfis, 0 marcas pagando."""
import asyncio
from pathlib import Path
src = (Path(__file__).parent / 'fix.py').read_text(); exec(src[:src.index('# A · GRANDES')])
BG, SUR, PRI, BALL, INK, MUT = '#08222C', '#0E3442', '#7FD0E6', '#DDF247', '#EAF4F6', '#9BB8C1'
CSS = CSS.replace('background:#0A0A0A;color:#fff', f'background:{BG};color:{INK}').replace('rgba(255,255,255,.05)', 'rgba(127,208,230,.07)')
def card(n, tot, body, c=BALL, swipe=True):
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="k"><div class="grid"></div>'
            f'<div class="blob" style="left:-300px;top:820px;width:720px;height:720px;background:{c};opacity:.16"></div>'
            f'<div class="blob" style="right:-320px;top:-200px;width:760px;height:760px;background:{PRI};opacity:.22"></div>'
            f'<div class="a" style="left:64px;top:58px">{APP["rk"]}</div><div class="a mono" style="right:64px;top:70px;font-size:22px;color:{MUT}">{n} / {tot}</div>'
            f'{body}' + (f'<div class="a" style="right:64px;bottom:58px;font-weight:800;font-size:34px;color:{c}">arraste →</div>' if swipe else '') + '</div>')
def txt(t, top, size=40, w=952, color=INK, weight=600): return f'<div class="a" style="left:64px;top:{top}px;width:{w}px;font-size:{size}px;font-weight:{weight};line-height:1.3;color:{color}">{t}</div>'
T = 8; A = []
A.append(card(1, T, title('O que tem por trás *da sua raquete ideal.*', BALL, 220, 116) + txt('Antes de recomendar uma raquete, o RACKET DNA leu, mediu e testou isto:', 640, 44, 900, MUT, 500)))
BIG = [('183', 'raquetes medidas', 'cada uma com ficha técnica completa', BALL), ('670', 'avaliações lidas', 'de testadores e de jogadores', PRI),
       ('44', 'variáveis por raquete', 'peso, balanço, rigidez, padrão e mais', BALL), ('379', 'casos de especialistas', 'em 3 idiomas, usados na calibração', PRI),
       ('21', 'estudos científicos', 'sobre braço e equipamento', BALL), ('0', 'marcas pagando para aparecer', 'Mesmas respostas, mesmo resultado.', PRI)]
for i, (n, l1, l2, c) in enumerate(BIG, 2):
    A.append(card(i, T, f'<div class="a num" style="left:56px;top:300px;font-size:{250 if len(n) >= 3 else 330}px;color:{c}">{n}</div>' + txt(l1, 700, 66, 952, INK, 800) + txt(l2, 900, 40, 900, MUT, 500), c))
CTA = (f'<div class="a" style="left:64px;right:64px;bottom:150px"><div style="display:flex;align-items:center;justify-content:center;background:{BALL};color:{BG};border-radius:24px;height:130px;font-weight:800;font-size:54px">Faça o teste →</div>'
       f'<div class="mono" style="margin-top:22px;text-align:center;font-size:30px;color:{INK}">sportdna.com.br/racket</div>'
       f'<div style="margin-top:28px;text-align:center;font-size:34px;font-weight:700;color:{MUT}">🔖 Salva este post para quando for comprar.</div></div>')
A.append(card(8, T, title('Antes de comprar, *faça o teste.*', BALL, 220, 110) + txt('Prévia grátis. Sem cadastro. Você vê a análise antes de pagar.', 560, 42, 900, MUT, 500) + CTA, swipe=False))
async def main():
    async with K.async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, h in enumerate(A, 1):
            await pg.set_content(h); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(150)
            await pg.screenshot(path=str(OUT / f'D-FX1v2-{i}.png'))
        await b.close()
asyncio.run(main())
from PIL import Image
S = Image.new('RGB', (8 * 270, 340), 'white')
for i in range(8):
    I = Image.open(OUT / f'D-FX1v2-{i + 1}.png').convert('RGB'); I.thumbnail((265, 335)); S.paste(I, (i * 270, 0))
S.save(OUT / 'D-FX1v2-sheet.jpg'); print('ok')
