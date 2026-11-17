"""Carrosséis Quiddo educação (17/11), 1080×1350: Geografia, Português, História (5 perguntas + gabarito + CTA) e Treinamento (3 passos).
Telas reais gravadas no Quiddo (qedu/<cap>) e fotos do banco novo (clips2, uma diferente por carrossel)."""
import asyncio, base64, io, json, subprocess
from pathlib import Path
from PIL import Image
H = Path(__file__).resolve().parent; W = H.parent; CL = W / 'clips2'; OUT = H / 'car'; OUT.mkdir(exist_ok=True)
FD = W.parent / 'social' / 'pipeline' / 'fonts'
def font(fam, f, w): return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{base64.b64encode((FD / f).read_bytes()).decode()}) format('woff2');font-weight:{w}}}"
FONTS = font('Fraunces', 'Fraunces-900.woff2', 900) + font('Nunito', 'Nunito-var.woff2', '200 1000')
LOGO = (W.parent / 'social' / 'pipeline' / 'assets' / 'quiddo' / 'quiddo-negativo.svg').read_text().replace('<svg', '<svg width="230" height="76"', 1)
def b64(p, w=1400):
    im = Image.open(p).convert('RGB'); im.thumbnail((w, 4000)); bf = io.BytesIO(); im.save(bf, 'JPEG', quality=88); return 'data:image/jpeg;base64,' + base64.b64encode(bf.getvalue()).decode()
def celframe(cap, t, name):
    p = H / f'{name}.jpg'; subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', str(H / cap / 'cel.mp4'), '-frames:v', '1', '-q:v', '2', str(p)], check=True); return p
OPC = ['#13A07A', '#FFC83D', '#1E7FD6', '#E5383B']; LET = 'ABCD'
CSS = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;overflow:hidden;font-family:Nunito}}
.p{{position:relative;width:1080px;height:1350px;overflow:hidden}}.a{{position:absolute}}.f{{font-family:Fraunces;font-weight:900;letter-spacing:-.01em;line-height:1.02}}
.chip{{display:inline-block;padding:10px 22px;border-radius:999px;font-weight:900;font-size:30px}}
.op{{display:flex;align-items:center;gap:22px;border-radius:24px;padding:0 28px;height:190px;font-weight:900;font-size:52px;color:#fff;box-shadow:0 6px 0 rgba(0,0,0,.25)}}
.op b{{width:62px;height:62px;border-radius:50%;background:rgba(255,255,255,.9);display:grid;place-items:center;font-size:32px}}
.tv{{background:#111;border-radius:22px;padding:14px;box-shadow:0 30px 70px rgba(0,0,0,.4)}}.tv img{{display:block;width:100%;border-radius:8px}}
.ph{{background:#141414;border-radius:56px;padding:16px;box-shadow:0 30px 70px rgba(0,0,0,.4)}}.ph img{{display:block;width:100%;border-radius:42px}}
.pg{{font-family:'Nunito';font-weight:900;font-size:26px;letter-spacing:.12em;text-transform:uppercase}}"""
def page(bg, body, fg='#fff'): return f'<html><style>{CSS}</style><div class="p" style="background:{bg};color:{fg}">{body}</div></html>'
def tv(img, x, y, w, rot=0): return f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)"><div class="tv"><img src="{img}"></div><div style="margin:0 auto;width:{w*.14:.0f}px;height:{w*.045:.0f}px;background:#111"></div><div style="margin:0 auto;width:{w*.36:.0f}px;height:{w*.018:.0f}px;border-radius:8px;background:#111"></div></div>'
def logo(x, y): return f'<div class="a" style="left:{x}px;top:{y}px">{LOGO}</div>'
def cta(cor, titulo, sub, img):
    return page(cor, logo(70, 64) + f'<div class="a pg" style="right:70px;top:84px;opacity:.75">Faça o seu</div>'
                f'<div class="a f" style="left:70px;top:190px;width:940px;font-size:96px">{titulo}</div>' + tv(img, 190, 480, 700) +
                f'<div class="a" style="left:70px;top:930px;width:940px;font-size:36px;font-weight:800;line-height:1.3">{sub}</div>'
                f'<div class="a f" style="left:70px;top:1080px;width:940px;height:132px;border-radius:30px;background:#FFC83D;color:#0E2A22;display:flex;align-items:center;justify-content:center;font-size:62px">Criar meu quiz grátis →</div>'
                f'<div class="a" style="left:70px;top:1240px;width:940px;text-align:center;font-size:34px;font-weight:900">quiddo.com.br · grátis até 10 pessoas · sem baixar app</div>')

SUBJ = [
 dict(id='QE-C1', mat='Geografia', cor='#1E7FD6', cap='geo', foto=('sala_de_aula', '21995', 'a'), titulo='5 perguntas de Geografia pra abrir a aula.',
      q=[('Qual é a capital da Austrália?', ['Sydney', 'Melbourne', 'Camberra', 'Perth'], 2),
         ('Qual é o maior bioma do Brasil?', ['Cerrado', 'Mata Atlântica', 'Amazônia', 'Caatinga'], 2),
         ('Qual é o maior oceano do mundo?', ['Atlântico', 'Índico', 'Pacífico', 'Ártico'], 2),
         ('Quantos estados tem o Brasil (fora o Distrito Federal)?', ['24', '25', '26', '27'], 2),
         ('Qual é o menor país do mundo?', ['Mônaco', 'Vaticano', 'San Marino', 'Malta'], 1)]),
 dict(id='QE-C2', mat='Português', cor='#E5383B', cap='port', foto=('sala_de_aula', '36046', 'b'), titulo='5 perguntas de Português que a turma erra.',
      q=[('Qual destas palavras é proparoxítona?', ['Café', 'Lâmpada', 'Caju', 'Janela'], 1),
         ('Complete: "___ dois anos que a gente não se vê."', ['Faz', 'Fazem', 'Fizeram', 'Faziam'], 0),
         ('Qual é o plural de "cidadão"?', ['Cidadões', 'Cidadães', 'Cidadãos', 'Cidadãoes'], 2),
         ('Ele é um ___ perdedor.', ['mal', 'mau'], 1),
         ('Qual frase está correta?', ['Houveram muitos problemas.', 'Houve muitos problemas.'], 1)]),
 dict(id='QE-C3', mat='História', cor='#FF7A1A', cap='hist', foto=('sala_de_aula', '5940', 'a'), titulo='5 perguntas de História do Brasil valendo pódio.',
      q=[('Em que ano foi assinada a Lei Áurea?', ['1822', '1888', '1889', '1930'], 1),
         ('Quem proclamou a Independência do Brasil?', ['Tiradentes', 'Dom Pedro I', 'Dom Pedro II', 'Deodoro da Fonseca'], 1),
         ('Em que ano foi proclamada a República no Brasil?', ['1822', '1888', '1889', '1891'], 2),
         ('Qual era a capital do Brasil antes de Brasília?', ['Salvador', 'São Paulo', 'Rio de Janeiro', 'Belo Horizonte'], 2),
         ('Em que ano o ser humano pisou na Lua pela primeira vez?', ['1959', '1965', '1969', '1972'], 2)]),
]

def subj_pages(s):
    cor = s['cor']; th, cid, ab = s['foto']; foto = b64(CL / th / 'stills' / f'{cid}-{ab}.jpg', 1600)
    tvimg = b64(H / s['cap'] / 'tv_q0_rev.png'); rank = b64(H / s['cap'] / ('tv_q1_rank.png'))
    P = [page('#000', f'<img class="a" src="{foto}" style="left:0;top:0;width:1080px;height:1350px;object-fit:cover;filter:brightness(.62)">'
              f'<div class="a" style="inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,0) 55%,rgba(0,0,0,.55))"></div>' + logo(70, 64) +
              f'<div class="a" style="left:70px;top:190px"><span class="chip" style="background:{cor};color:#fff">Quiz de {s["mat"]}</span></div>'
              f'<div class="a f" style="left:70px;top:290px;width:940px;font-size:104px">{s["titulo"]}</div>' + tv(tvimg, 300, 790, 700, -2) +
              f'<div class="a" style="left:70px;top:1220px;font-size:36px;font-weight:900">Arraste e responda de cabeça →</div>')]
    for n, (q, o, ok) in enumerate(s['q'], 1):
        two = len(o) == 2
        ops = ''.join(f'<div class="op" style="background:{OPC[j]}"><b style="color:{OPC[j]}">{LET[j]}</b>{t}</div>' for j, t in enumerate(o))
        P.append(page('#FFF6E6', f'<div class="a pg" style="left:70px;top:80px;color:{cor}">{s["mat"]} · pergunta {n} de 5</div>'
                      f'<div class="a" style="right:70px;top:62px"><span class="chip" style="background:{cor};color:#fff">Quiddo</span></div>'
                      f'<div class="a f" style="left:70px;top:190px;width:940px;font-size:{86 if len(q) < 45 else 72}px;color:#0E2A22">{q}</div>'
                      f'<div class="a" style="left:70px;top:{600 if len(q) < 45 else 680}px;width:940px;display:grid;grid-template-columns:{"1fr" if two else "1fr 1fr"};gap:22px">{ops}</div>'
                      f'<div class="a" style="left:70px;top:1220px;font-size:34px;font-weight:900;color:#4A5E56">Gabarito no fim →</div>', '#0E2A22'))
    gab = ''.join(f'<div style="display:flex;gap:24px;align-items:baseline;padding:22px 0;border-top:3px dashed rgba(255,255,255,.35)"><span class="f" style="font-size:72px;color:#FFC83D">{n}</span><span style="font-size:56px;font-weight:900">{o[ok]}</span></div>' for n, (q, o, ok) in enumerate(s['q'], 1))
    P.append(page(cor, logo(70, 64) + f'<div class="a f" style="left:70px;top:190px;width:940px;font-size:110px">Gabarito</div>'
                  f'<div class="a" style="left:70px;top:380px;width:940px">{gab}</div>'
                  f'<div class="a" style="left:70px;top:1180px;width:940px;font-size:40px;font-weight:900">Quantas você acertou? Agora imagine a turma toda jogando.</div>'))
    P.append(cta('#0B5D45', 'Monte o quiz da sua aula.', f'Escreva as perguntas de {s["mat"]}, abra a sala no telão e a turma responde pelo celular. Ranking a cada rodada e pódio no fim.', rank))
    return P

def treino_pages():
    cor = '#3A3FC2'; foto = b64(CL / 'treinamento' / 'stills' / '46750-a.jpg', 1600); cap = 'treino'
    m = json.loads((H / cap / 'marcas.json').read_text())
    cel_q = b64(celframe(cap, m['q0_hero'] - 0.3, 'tr_q'), 900); cel_ok = b64(celframe(cap, m['q0_reveal'] + 6, 'tr_ok'), 900)
    criar = b64(H / 'criar3.png', 900); lobby = b64(H / cap / 'tv_lobby.png'); rev = b64(H / cap / 'tv_q1_rev.png'); rank = b64(H / cap / 'tv_q1_rank.png')
    def passo(n, t, sub, vis):
        return page('#F3F1FF', f'<div class="a pg" style="left:70px;top:80px;color:{cor}">Treinamento em quiz · passo {n} de 4</div>'
                    f'<div class="a f" style="left:70px;top:150px;width:940px;font-size:84px;color:#14163A">{t}</div>'
                    f'<div class="a" style="left:70px;top:{340 if len(t) < 30 else 420}px;width:940px;font-size:38px;font-weight:700;color:#3B3F5C;line-height:1.3">{sub}</div>' + vis, '#14163A')
    ph = lambda img, x, y, w: f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px"><div class="ph"><img src="{img}"></div></div>'
    P = [page('#000', f'<img class="a" src="{foto}" style="left:0;top:0;width:1080px;height:1350px;object-fit:cover;filter:brightness(.6)">'
              f'<div class="a" style="inset:0;background:linear-gradient(180deg,rgba(0,0,0,.6),rgba(0,0,0,0) 60%,rgba(0,0,0,.5))"></div>' + logo(70, 64) +
              f'<div class="a" style="left:70px;top:190px"><span class="chip" style="background:{cor};color:#fff">Treinamento corporativo</span></div>'
              '<div class="a f" style="left:70px;top:290px;width:940px;font-size:110px">O treinamento que a equipe não esquece.</div>'
              '<div class="a" style="left:70px;top:1220px;font-size:36px;font-weight:900">Em 4 passos →</div>'),
         passo(1, 'Escreva as perguntas.', 'Múltipla escolha ou verdadeiro ou falso, com o conteúdo do treinamento.', ph(criar, 300, 520, 480)),
         passo(2, 'Abra a sala no telão.', 'Aparecem um código e um QR. A equipe entra pelo celular, sem baixar app.', tv(lobby, 110, 520, 860)),
         passo(3, 'A equipe responde pelo celular.', 'Quem acerta mais rápido ganha mais pontos.', ph(cel_q, 120, 560, 400) + ph(cel_ok, 560, 600, 400)),
         passo(4, 'Resposta e ranking no telão.', 'A cada rodada, a disputa aparece para a sala toda. No fim, pódio.', tv(rev, 110, 500, 860)),
         cta('#0B5D45', 'Transforme o treinamento em quiz.', 'Onboarding, atendimento, segurança, produto: o conteúdo vira jogo e a equipe participa.', rank)]
    return P

async def main():
    from playwright.async_api import async_playwright
    jobs = [(s['id'], subj_pages(s)) for s in SUBJ] + [('QE-C4', treino_pages())]
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for cid, pages in jobs:
            for k, html in enumerate(pages, 1):
                await pg.set_content(html); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(120)
                await pg.screenshot(path=str(OUT / f'{cid}-{k}.png'))
            print(cid, len(pages), flush=True)
        await b.close()
asyncio.run(main())
