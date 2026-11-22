"""Brief Growth 19/11 · variações de estático 1:1.
RK-02-v2 (ROAS 3,5): a) 183 raquetes medidas  b) cotovelo dói depois do jogo?  c) antes de gastar R$ 1.500. Sem preço do relatório; CTA "Teste o seu agora".
RZ-03-v2 (o estático do casal que vende): a) recibo do amor  b) quem paga o jantar  c) placar de vocês dois. Sem preço; "Teste o de vocês" + "Nada sai do seu celular"."""
import sys, asyncio, base64
from pathlib import Path
W = Path(__file__).resolve().parent.parent; N = W / 'n1'; sys.path.insert(0, str(N)); sys.argv = sys.argv[:1]
import kvx
K = kvx.K; OUT = W / 'b1911'
def b64(p): return 'data:image/jpeg;base64,' + base64.b64encode(Path(p).read_bytes()).decode()
RKLOGO = K.svg(K.SD / 'racketdna-logo-fundo-escuro.svg', h=40); RZLOGO = K.svg(N / 'rz-logo-c.svg', h=44)
BASE = K.FONTS + "*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1080px;overflow:hidden}.a{position:absolute}"
def hl(s, c): return s.replace('*', '<span style="color:%s">' % c, 1).replace('*', '</span>', 1)
def rk(title, sub, tiles):
    t = ''.join(f'<div style="background:#fff;border-radius:22px;padding:26px 28px"><div style="font-family:Syne,sans-serif;font-weight:800;font-size:{86 if len(n) < 6 else 70}px;letter-spacing:-.04em;line-height:.9;color:#0A0A0A">{n}</div><div style="font-size:27px;font-weight:500;margin-top:8px;color:#0A0A0A">{l}</div></div>' for n, l in tiles)
    return f"""<!doctype html><meta charset="utf-8"><style>{BASE}</style><div class="a" style="inset:0;background:#DDF247;color:#0A0A0A;font-family:'DM Sans',sans-serif">
<div class="a" style="left:60px;top:58px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:26px;letter-spacing:.08em">RACKET DNA · TESTE</div>
<div class="a" style="right:56px;top:42px;background:#0A0A0A;border-radius:14px;padding:12px 20px">{RKLOGO}</div>
<div class="a" style="left:60px;top:150px;width:960px;font-family:Archivo,sans-serif;font-weight:800;font-size:80px;letter-spacing:-.035em;line-height:1.0">{title}</div>
<div class="a" style="left:60px;top:430px;width:960px;font-size:30px;font-weight:500">{sub}</div>
<div class="a" style="left:60px;top:520px;width:960px;display:grid;grid-template-columns:1fr 1fr;gap:22px">{t}</div>
<div class="a" style="left:60px;bottom:58px;background:#0A0A0A;color:#fff;border-radius:16px;padding:22px 36px;font-weight:700;font-size:36px">Teste o seu agora →</div>
<div class="a" style="right:60px;bottom:78px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:24px">sportdna.com.br/racket</div></div>"""
def rz(title, sub, img, pos, zoom=1.0):
    return f"""<!doctype html><meta charset="utf-8"><style>{BASE}</style><div class="a" style="inset:0;background:#FFF3EC;color:#5E0B2B;font-family:'DM Sans',sans-serif">
<div class="a" style="left:60px;top:62px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:24px;letter-spacing:.12em;color:#B3174F">RETROZAP CASAIS</div>
<div class="a" style="right:60px;top:52px">{RZLOGO}</div>
<div class="a" style="left:60px;top:130px;width:560px;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:80px;letter-spacing:-.035em;line-height:.98">{title}</div>
<div class="a" style="left:60px;top:470px;width:540px;font-size:31px;font-weight:600;line-height:1.3">{sub}</div>
<div class="a" style="right:50px;top:150px;width:390px;height:700px;border-radius:24px;overflow:hidden;box-shadow:0 30px 70px rgba(94,11,43,.28);transform:rotate(3deg)"><img src="{img}" style="width:100%;height:100%;object-fit:cover;transform:scale({zoom});transform-origin:{pos}"></div>
<div class="a" style="left:60px;bottom:120px;background:#E0245E;color:#fff;border-radius:999px;padding:24px 44px;font-weight:800;font-size:40px">Teste o de vocês →</div>
<div class="a" style="left:66px;bottom:62px;font-size:26px;font-weight:600">retrozap.com.br · Nada sai do seu celular.</div></div>"""
PO = lambda n: b64(N / 'scr' / f'rzp_{n}.jpg')
TILES = [('183', 'raquetes com specs medidas'), ('379', 'casos de especialistas'), ('670', 'avaliações lidas'), ('Grátis', 'a prévia, antes de pagar')]
P = {
 'ADC-RK-02-A-v1': rk('183 raquetes medidas. <span style="background:#0A0A0A;color:#DDF247;padding:0 14px;border-radius:10px">Uma é a sua.</span>', 'Cruzadas com o seu corpo, o seu braço e o seu jogo.', TILES),
 'ADC-RK-02-B-v1': rk('Cotovelo dói depois do jogo? <span style="background:#0A0A0A;color:#DDF247;padding:0 14px;border-radius:10px">Confira a raquete.</span>', 'Rigidez, peso e balanço pesam no braço. O teste avalia o conforto da sua.',
                      [('Grátis', 'avaliação da raquete que você usa'), ('183', 'raquetes medidas para comparar'), ('3', 'raquetes que mais combinam'), ('670', 'avaliações lidas')]),
 'ADC-RK-02-C-v1': rk('Antes de gastar R$&nbsp;1.500 numa raquete, <span style="background:#0A0A0A;color:#DDF247;padding:0 14px;border-radius:10px">faça o teste.</span>', 'Parece simples. Não é. Veja a prévia grátis antes de comprar.', TILES),
 'ADC-RZ-03-A-v1': rz(hl('O recibo do amor de *vocês dois.*', '#E0245E'), 'Quem mandou mais "te amo", mais boa noite, quem puxou o papo: item por item.', PO('casal-recibo'), '50% 25%'),
 'ADC-RZ-03-B-v1': rz(hl('Quem paga o *jantar?*', '#E0245E'), 'O recibo do amor responde, tirado da conversa de vocês.', PO('casal-recibo'), '50% 72%', 1.7),
 'ADC-RZ-03-C-v1': rz(hl('O placar de *vocês dois.*', '#E0245E'), 'Mensagens, áudios, declarações de amor: um contra o outro.', PO('casal-placar'), '50% 20%'),
}
async def main():
    async with K.async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1080})
        for k, h in P.items():
            await pg.set_content(h); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT / f'{k}_feed-1x1.png'))
        await b.close()
asyncio.run(main())
from PIL import Image
T = Image.new('RGB', (3 * 360, 2 * 360), 'white')
for i, k in enumerate(P):
    I = Image.open(OUT / f'{k}_feed-1x1.png').convert('RGB'); I.thumbnail((355, 355)); T.paste(I, ((i % 3) * 360, (i // 3) * 360))
T.save(OUT / 'sheet.jpg')
