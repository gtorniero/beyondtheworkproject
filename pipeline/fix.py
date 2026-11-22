"""SPORT DNA · 3 carrosséis didáticos para FIXAR no perfil (pedido do Gui via Growth, 22/11). 4:5, números da home do site (sportdna.com.br, 22/11).
A · Grandes números  B · Como fazer o teste (RACKET de exemplo; SURF e RUN igual)  C · Os motores (RACKET na metade dos cards)."""
import sys, asyncio
from pathlib import Path
W = Path(__file__).resolve().parent.parent; N = W / 'n1'; sys.path.insert(0, str(N)); sys.argv = sys.argv[:1]
import kvx
K = kvx.K; OUT = W / 'fix'; OUT.mkdir(exist_ok=True)
LOGO = K.svg(K.SD / 'sportdna-logo-fundo-escuro.svg', h=44)
APP = {'rk': K.svg(K.SD / 'racketdna-logo-fundo-escuro.svg', h=40), 'sf': K.svg(K.SD / 'surfdna-logo-fundo-escuro.svg', h=40), 'rn': K.svg(K.SD / 'rundna-logo-fundo-escuro.svg', h=40)}
COR = {'rk': '#DDF247', 'sf': '#6CCFF6', 'rn': '#FF8A3D', 'sd': '#DDF247'}
CSS = K.FONTS + """*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden}
.k{position:relative;width:1080px;height:1350px;overflow:hidden;background:#0A0A0A;color:#fff;font-family:'DM Sans',sans-serif}.a,.abs{position:absolute}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.05) 2px,transparent 2px);background-size:90px 90px}
.blob{position:absolute;border-radius:50%;filter:blur(140px)}
.hd{font-family:Archivo,sans-serif;font-weight:800;letter-spacing:-.035em;line-height:1.0}
.num{font-family:Syne,sans-serif;font-weight:800;letter-spacing:-.05em;line-height:.85}
.mono{font-family:'JetBrains Mono',monospace;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.chip{display:inline-block;border:2px solid rgba(255,255,255,.3);border-radius:14px;padding:12px 20px;margin:0 12px 14px 0;font-weight:700;font-size:32px}
.ph{position:relative;background:#1d1d1f;box-shadow:0 0 0 3px rgba(255,255,255,.28),0 50px 110px rgba(0,0,0,.7)}.ph .scr{position:absolute;overflow:hidden;background:#fff}
.ph .gl{position:absolute;inset:0;border-radius:inherit;background:linear-gradient(125deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,0) 26%)}"""
def card(n, tot, body, c='#DDF247', app=None, swipe=True):
    head = APP[app] if app else LOGO
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="k"><div class="grid"></div>'
            f'<div class="blob" style="left:-300px;top:820px;width:720px;height:720px;background:{c};opacity:.20"></div>'
            f'<div class="blob" style="right:-320px;top:-200px;width:760px;height:760px;background:#0E4D64;opacity:.55"></div>'
            f'<div class="a" style="left:64px;top:58px">{head}</div><div class="a mono" style="right:64px;top:70px;font-size:22px;color:#A3A3A0">{n} / {tot}</div>'
            f'{body}' + (f'<div class="a" style="right:64px;bottom:58px;font-weight:800;font-size:34px;color:{c}">arraste →</div>' if swipe else '') + '</div>')
hl = lambda s, c: s.replace('*', f'<span style="color:{c}">', 1).replace('*', '</span>', 1)
def title(t, c, top=150, size=88, w=952): return f'<div class="a hd" style="left:64px;top:{top}px;width:{w}px;font-size:{size}px">{hl(t, c)}</div>'
def txt(t, top, size=40, w=952, color='#fff', weight=600): return f'<div class="a" style="left:64px;top:{top}px;width:{w}px;font-size:{size}px;font-weight:{weight};line-height:1.3;color:{color}">{t}</div>'
def ph(src, x, y, w=360, zoom=1.0, fy=0.0): return K.phone(src, w, x, y, (-10, 4, 2.5), zoom, .5, fy)
def cta(c, extra='', app_url='sportdna.com.br'):
    return (f'<div class="a" style="left:64px;right:64px;bottom:150px"><div style="display:flex;align-items:center;justify-content:center;background:{c};color:#0A0A0A;border-radius:24px;height:130px;font-weight:800;font-size:54px">Faça o teste →</div>'
            f'<div class="mono" style="margin-top:22px;text-align:center;font-size:30px;color:#fff">{app_url}</div>'
            f'<div style="margin-top:28px;text-align:center;font-size:34px;font-weight:700;color:#D9D9D6">🔖 Salva este post para quando for comprar.</div>{extra}</div>')

# A · GRANDES NÚMEROS
TA = 8; A = []
A.append(card(1, TA, title('O que tem por trás *do teste.*', '#DDF247', 220, 120) + txt('Raquete, prancha e tênis de corrida. Antes de recomendar, o motor leu, mediu e testou isto:', 560, 44, 900, '#D9D9D6', 500)
              + '<div class="a" style="left:64px;top:820px;display:flex;gap:22px">' + ''.join(f'<div style="padding:14px 24px;border-radius:14px;border:2px solid {COR[k]};color:{COR[k]};font-weight:800;font-size:34px">{n}</div>' for k, n in (('rk', 'RACKET'), ('sf', 'SURF'), ('rn', 'RUN'))) + '</div>'))
BIG = [('2.425', 'reviews e avaliações lidas', 'de testadores e de clientes', '#DDF247'), ('1.035', 'casos reais e indicações de especialistas', 'usados na calibração', '#DDF247'),
       ('62', 'estudos científicos', 'por trás das regras do motor', '#6CCFF6'), ('395', 'tênis e raquetes com ficha técnica', '212 tênis de corrida + 183 raquetes, mais 13 tipos de prancha', '#FF8A3D'),
       ('11.000', 'perfis simulados', 'para conferir segurança e viés antes de você fazer o teste', '#DDF247'), ('0', 'marcas pagando para aparecer', 'Mesmas respostas, mesmo resultado.', '#DDF247')]
for i, (n, l1, l2, c) in enumerate(BIG, 2):
    A.append(card(i, TA, f'<div class="a num" style="left:56px;top:300px;font-size:{330 if len(n) <= 3 else 220}px;color:{c}">{n}</div>' + txt(l1, 700, 66, 952, '#fff', 800) + txt(l2, 900, 40, 900, '#D9D9D6', 500), c))
A.append(card(8, TA, title('Antes de comprar, *faça o teste.*', '#DDF247', 220, 110) + txt('RACKET e SURF: prévia grátis. RUN: 100% grátis. Sem cadastro.', 560, 42, 900, '#D9D9D6', 500) + cta('#DDF247'), swipe=False))

# B · COMO FAZER O TESTE
TB = 6; B = []
B.append(card(1, TB, title('Como funciona o teste, *em 3 passos.*', '#DDF247', 200, 104, 620) + ph('racket_land.jpg', 680, 260, 340) + txt('Exemplo: RACKET DNA. O SURF e o RUN funcionam igual.', 760, 40, 580, '#D9D9D6', 500), app='rk'))
STEPS = [('1', 'Responda.', 'Corpo, nível, frequência, dor e o que você sente hoje no equipamento atual. <b>Sem cadastro.</b>', 'racket_q2.jpg'),
         ('2', 'Veja a análise grátis.', 'Seu perfil, as especificações ideais e o grau de confiança do resultado, antes de pagar qualquer coisa.', 'racket_free_ficha.jpg'),
         ('3', 'Receba os finalistas.', 'O relatório revela os modelos, com a ficha técnica e a comparação com o que você já tem.', 'racket_res.jpg')]
for i, (n, h, d, src) in enumerate(STEPS, 2):
    B.append(card(i, TB, f'<div class="a num" style="left:56px;top:190px;font-size:260px;color:#DDF247">{n}</div>' + title(h, '#DDF247', 440, 84, 600) + txt(d, 640, 38, 580, '#D9D9D6', 500) + ph(src, 690, 300, 330), app='rk'))
B.append(card(5, TB, title('SURF e RUN: *o mesmo caminho.*', '#6CCFF6', 170, 92) + ph('surf_res.jpg', 90, 430, 330) + ph('run2_res.jpg', 600, 430, 330)
              + f'<div class="a" style="left:120px;top:1100px;font-weight:800;font-size:36px;color:#6CCFF6">SURF DNA</div><div class="a" style="left:640px;top:1100px;font-weight:800;font-size:36px;color:#FF8A3D">RUN DNA</div>'
              + txt('No RUN, o relatório completo é grátis.', 1170, 36, 952, '#D9D9D6', 500), '#6CCFF6'))
B.append(card(6, TB, title('Faça o seu em *3 minutos.*', '#DDF247', 220, 110) + txt('Sem cadastro. Você vê a análise antes de pagar.', 470, 44, 900, '#D9D9D6', 500) + cta('#DDF247'), swipe=False))

# C · OS MOTORES
TC = 8; C = []
def lista(items, top, c, size=34):
    return f'<div class="a" style="left:64px;top:{top}px;width:952px">' + ''.join(f'<span class="chip" style="border-color:{c}66;font-size:{size}px">{x}</span>' for x in items) + '</div>'
C.append(card(1, TC, title('O que você informa → *o que a gente calcula.*', '#DDF247', 220, 104) + txt('Os motores do SPORT DNA, um por esporte. Começando pela raquete.', 620, 44, 900, '#D9D9D6', 500)))
C.append(card(2, TC, '<div class="a mono" style="left:64px;top:170px;font-size:26px;color:#DDF247">RACKET · Você informa</div>' + title('O seu jogo e *o seu braço.*', '#DDF247', 220, 92)
              + lista(['Idade e força', 'Dor no braço', 'Medida da mão', 'Nível e frequência', 'Estilo, topspin e swing', 'Onde você erra', 'Raquete atual e sensação', 'Orçamento e corda'], 480, '#DDF247', 38), app='rk'))
C.append(card(3, TC, '<div class="a mono" style="left:64px;top:170px;font-size:26px;color:#DDF247">RACKET · A gente calcula</div>' + title('A raquete *por dentro.*', '#DDF247', 220, 92)
              + lista(['Peso', 'Balanço', 'Swingweight', 'Rigidez (RA)', 'Cabeça', 'Padrão', 'Corda e tensão', 'Grip'], 480, '#DDF247', 44), app='rk'))
C.append(card(4, TC, '<div class="a num" style="left:56px;top:260px;font-size:300px;color:#DDF247">183</div>' + txt('raquetes no catálogo, com ficha técnica medida.', 620, 60, 952, '#fff', 800)
              + txt('Cada uma comparada com as specs ideais que saem das suas respostas.', 820, 40, 900, '#D9D9D6', 500), app='rk'))
C.append(card(5, TC, '<div class="a mono" style="left:64px;top:170px;font-size:26px;color:#DDF247">RACKET · O resultado</div>' + title('A sua ficha ideal, *de graça.*', '#DDF247', 220, 92, 600) + ph('racket_free_ficha.jpg', 680, 300, 330)
              + txt('Peso, cabeça, swingweight e balanço ideais para você. O relatório completo revela as raquetes que mais combinam.', 560, 38, 580, '#D9D9D6', 500), app='rk'))
C.append(card(6, TC, '<div class="a mono" style="left:64px;top:170px;font-size:26px;color:#6CCFF6">SURF · Você informa → a gente calcula</div>' + title('Do seu mar *à sua prancha.*', '#6CCFF6', 220, 88)
              + lista(['Peso, altura e idade', 'Tempo de surf', 'Onda e força', 'Prancha atual'], 440, '#6CCFF6', 32) + '<div class="a" style="left:64px;top:690px;font-size:60px;color:#6CCFF6;font-weight:800">↓</div>'
              + lista(['Tipo de shape', 'Comprimento', 'Largura e espessura', 'Litragem', 'Rabeta e bordas', 'Quilhas'], 790, '#6CCFF6', 36), '#6CCFF6', app='sf'))
C.append(card(7, TC, '<div class="a mono" style="left:64px;top:170px;font-size:26px;color:#FF8A3D">RUN · Você informa → a gente calcula</div>' + title('Do seu treino *ao seu tênis.*', '#FF8A3D', 220, 88)
              + lista(['Peso e largura do pé', 'Km por semana e ritmo', 'Terreno', 'Objetivo e prova'], 440, '#FF8A3D', 32) + '<div class="a" style="left:64px;top:690px;font-size:60px;color:#FF8A3D;font-weight:800">↓</div>'
              + lista(['Altura de espuma', 'Drop', 'Peso', 'Durabilidade', 'Custo por km', 'Quando trocar'], 790, '#FF8A3D', 36), '#FF8A3D', app='rn'))
C.append(card(8, TC, title('Mesmas respostas, mesmo resultado. *Nenhuma marca no comando.*', '#DDF247', 200, 92) + cta('#DDF247'), swipe=False))

SETS = {'D-FX1': A, 'D-FX2': B, 'D-FX3': C}
async def main():
    async with K.async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for k, cs in SETS.items():
            for i, h in enumerate(cs, 1):
                await pg.set_content(h); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(150)
                await pg.screenshot(path=str(OUT / f'{k}-{i}.png'))
        await b.close()
asyncio.run(main())
from PIL import Image
for k, cs in SETS.items():
    T = Image.new('RGB', (len(cs) * 270, 340), 'white')
    for i in range(len(cs)):
        I = Image.open(OUT / f'{k}-{i + 1}.png').convert('RGB'); I.thumbnail((265, 335)); T.paste(I, (i * 270, 0))
    T.save(OUT / f'{k}-sheet.jpg')
print('ok')
